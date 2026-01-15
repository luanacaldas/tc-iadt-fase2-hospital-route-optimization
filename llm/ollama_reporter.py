"""
Implementação do gerador de relatórios usando Ollama (LLM local).

Este módulo implementa o BaseReporter usando Ollama para execução local.
Ollama permite rodar modelos de LLM localmente sem necessidade de API keys.
"""

import json
from typing import List, Dict, Any, Optional

try:
    from langchain_ollama import ChatOllama
    from langchain.schema import HumanMessage, SystemMessage
    OLLAMA_AVAILABLE = True
    USE_DIRECT_API = False
except ImportError:
    # Fallback para uso direto da API do Ollama
    try:
        import ollama
        OLLAMA_AVAILABLE = True
        USE_DIRECT_API = True
    except ImportError:
        OLLAMA_AVAILABLE = False
        USE_DIRECT_API = False

from hospital_routes.core.interfaces import (
    BaseReporter,
    OptimizationResult,
    ReportResult,
    ReportRequest,
    ReportType,
    Delivery,
)
from hospital_routes.core.exceptions import ReportGenerationError, LLMConnectionError
from hospital_routes.llm.prompts import PromptTemplates
from hospital_routes.llm.ollama_helper import (
    get_best_available_model,
    check_ollama_running,
    list_available_models,
    get_model_full_name,
)


class OllamaReporter(BaseReporter):
    """
    Gerador de relatórios usando Ollama (LLM local).
    
    Implementa BaseReporter usando ChatOllama do LangChain ou API direta do Ollama.
    Requer que o Ollama esteja rodando localmente.
    """
    
    def __init__(
        self,
        model_name: str = "llama3.2",
        base_url: str = "http://localhost:11434",
        temperature: float = 0.7,
        num_predict: int = 2000,
    ):
        """
        Args:
            model_name: Nome do modelo Ollama (ex: "llama3.2", "mistral", "phi3")
            base_url: URL base do Ollama (padrão: http://localhost:11434)
            temperature: Temperatura para geração (0.0-2.0)
            num_predict: Número máximo de tokens a gerar
        """
        if not OLLAMA_AVAILABLE:
            raise ImportError(
                "Ollama não está disponível. "
                "Instale com: pip install langchain-ollama ou pip install ollama"
            )
        
        # Auto-detectar modelo se não especificado
        if model_name is None:
            model_name = get_best_available_model()
            if model_name is None:
                raise LLMConnectionError(
                    "Nenhum modelo Ollama disponível. "
                    "Execute: ollama pull llama3.2"
                )
            print(f"ℹ️  Usando modelo auto-detectado: {model_name}")
        
        self.model_name = model_name
        self.base_url = base_url
        self.temperature = temperature
        self.num_predict = num_predict
        self.use_direct_api = USE_DIRECT_API
        
        # Verificar se Ollama está rodando
        if not check_ollama_running():
            raise LLMConnectionError(
                "Ollama não está rodando. "
                "Certifique-se de que o Ollama está instalado e rodando."
            )
        
        # Inicializar LLM
        try:
            if self.use_direct_api:
                # Usar API direta do Ollama
                self.llm = None  # Será usado via chamadas diretas
                # Verificar se o modelo está disponível
                try:
                    available_models = list_available_models()
                    
                    # Verificar se modelo está disponível
                    model_found = model_name in available_models
                    
                    if not model_found:
                        # Tentar auto-detect
                        best_model = get_best_available_model([model_name])
                        if best_model:
                            print(f"ℹ️  Modelo '{model_name}' não encontrado. Usando '{best_model}'")
                            self.model_name = best_model
                        else:
                            print(f"⚠️  Aviso: Modelo '{model_name}' não encontrado localmente.")
                            print(f"   Modelos disponíveis: {', '.join(available_models) if available_models else 'nenhum'}")
                            print(f"   Execute: ollama pull {model_name}")
                except Exception as e:
                    print(f"⚠️  Aviso: Não foi possível verificar modelos: {e}")
            else:
                # Usar LangChain
                self.llm = ChatOllama(
                    model=model_name,
                    base_url=base_url,
                    temperature=temperature,
                    num_predict=num_predict,
                )
        except Exception as e:
            raise LLMConnectionError(
                f"Erro ao conectar com Ollama: {str(e)}\n"
                f"Certifique-se de que o Ollama está rodando em {base_url}"
            ) from e
    
    def generate_report(self, request: ReportRequest) -> ReportResult:
        """
        Gera um relatório baseado no resultado da otimização.
        
        Args:
            request: Request contendo resultado e tipo de relatório
        
        Returns:
            ReportResult: Relatório gerado
        """
        if request.report_type == ReportType.DRIVER_INSTRUCTIONS:
            return self.generate_driver_instructions(
                request.optimization_result, request.language
            )
        elif request.report_type == ReportType.MANAGERIAL_REPORT:
            return self.generate_managerial_report(
                request.optimization_result,
                request.language,
                request.additional_context,
            )
        elif request.report_type == ReportType.DAILY_SUMMARY:
            return self.generate_daily_summary(
                request.optimization_result, request.language
            )
        else:
            raise ReportGenerationError(
                f"Tipo de relatório não suportado: {request.report_type}"
            )
    
    def generate_driver_instructions(
        self,
        optimization_result: OptimizationResult,
        language: str = "pt-BR",
    ) -> ReportResult:
        """
        Gera instruções passo-a-passo para o motorista.
        
        Cria um texto amigável e diretivo, alertando sobre paradas críticas.
        
        Args:
            optimization_result: Resultado da otimização
            language: Idioma do relatório
        
        Returns:
            ReportResult: Instruções para o motorista
        """
        try:
            # Preparar dados da rota
            deliveries = optimization_result.solution.metadata.get("deliveries")
            route_data = self._prepare_route_data(optimization_result, deliveries)
            
            # Criar prompt
            prompt = self._create_driver_instructions_prompt(
                route_data, language
            )
            
            # Gerar instruções
            if self.use_direct_api:
                # Usar API direta do Ollama
                response = self._call_ollama_direct(
                    system_prompt=prompt["system"],
                    user_prompt=prompt["human"],
                )
                content = response
            else:
                # Usar LangChain
                messages = [
                    SystemMessage(content=prompt["system"]),
                    HumanMessage(content=prompt["human"]),
                ]
                response = self.llm.invoke(messages)
                content = response.content
            
            # Metadados
            metadata = {
                "model": self.model_name,
                "temperature": self.temperature,
                "num_predict": self.num_predict,
                "language": language,
                "provider": "ollama",
            }
            
            return ReportResult(
                content=content,
                report_type=ReportType.DRIVER_INSTRUCTIONS.value,
                metadata=metadata,
            )
        
        except Exception as e:
            raise ReportGenerationError(
                f"Erro ao gerar instruções do motorista: {str(e)}"
            ) from e
    
    def generate_managerial_report(
        self,
        optimization_result: OptimizationResult,
        language: str = "pt-BR",
        additional_context: Optional[Dict[str, Any]] = None,
    ) -> ReportResult:
        """
        Gera relatório gerencial de economia e eficiência.
        
        Args:
            optimization_result: Resultado da otimização
            language: Idioma do relatório
            additional_context: Contexto adicional
        
        Returns:
            ReportResult: Relatório gerencial
        """
        # TODO: Implementar quando necessário
        raise NotImplementedError("Relatório gerencial ainda não implementado")
    
    def generate_daily_summary(
        self,
        optimization_result: OptimizationResult,
        language: str = "pt-BR",
    ) -> ReportResult:
        """
        Gera resumo diário de operações.
        
        Args:
            optimization_result: Resultado da otimização
            language: Idioma do relatório
        
        Returns:
            ReportResult: Resumo diário
        """
        # TODO: Implementar quando necessário
        raise NotImplementedError("Resumo diário ainda não implementado")
    
    def generate_weekly_analysis(
        self,
        optimization_results: List[OptimizationResult],
        language: str = "pt-BR",
    ) -> ReportResult:
        """
        Gera análise semanal de performance.
        
        Args:
            optimization_results: Lista de resultados da semana
            language: Idioma do relatório
        
        Returns:
            ReportResult: Análise semanal
        """
        # TODO: Implementar quando necessário
        raise NotImplementedError("Análise semanal ainda não implementado")
    
    def _call_ollama_direct(
        self, system_prompt: str, user_prompt: str
    ) -> str:
        """
        Chama a API direta do Ollama.
        
        Args:
            system_prompt: Prompt do sistema
            user_prompt: Prompt do usuário
        
        Returns:
            str: Resposta do modelo
        """
        import ollama
        
        try:
            # Obter nome completo do modelo (com tag se disponível)
            model_full_name = get_model_full_name(self.model_name) or self.model_name
            
            response = ollama.chat(
                model=model_full_name,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                options={
                    "temperature": self.temperature,
                    "num_predict": self.num_predict,
                },
            )
            
            return response["message"]["content"]
        
        except Exception as e:
            raise LLMConnectionError(
                f"Erro ao chamar Ollama: {str(e)}\n"
                f"Certifique-se de que o Ollama está rodando e o modelo '{self.model_name}' está instalado."
            ) from e
    
    def _prepare_route_data(
        self, optimization_result: OptimizationResult, deliveries: Optional[List[Delivery]] = None
    ) -> Dict[str, Any]:
        """
        Prepara dados da rota em formato estruturado para o LLM.
        
        Args:
            optimization_result: Resultado da otimização
            deliveries: Lista de entregas (opcional, para enriquecer dados)
        
        Returns:
            dict: Dados estruturados da rota
        """
        solution = optimization_result.solution
        
        # Preparar rotas com informações detalhadas
        routes_data = []
        delivery_dict = {d.id: d for d in deliveries} if deliveries else {}
        
        for route_idx, route in enumerate(solution.routes):
            route_deliveries = []
            for delivery_id in route:
                delivery_info = {"id": delivery_id}
                if delivery_id in delivery_dict:
                    delivery = delivery_dict[delivery_id]
                    delivery_info.update({
                        "priority": delivery.priority,
                        "is_critical": delivery.priority == 1,
                        "weight": delivery.weight,
                    })
                route_deliveries.append(delivery_info)
            
            route_info = {
                "vehicle_id": route_idx + 1,
                "deliveries": route_deliveries,
                "num_deliveries": len(route),
            }
            routes_data.append(route_info)
        
        return {
            "total_distance_km": round(solution.total_distance, 2),
            "total_cost": round(solution.total_cost, 2),
            "num_vehicles": len(solution.routes),
            "routes": routes_data,
            "violations": solution.violations,
        }
    
    def _create_driver_instructions_prompt(
        self, route_data: Dict[str, Any], language: str
    ) -> Dict[str, str]:
        """
        Cria prompt para instruções do motorista.
        
        Args:
            route_data: Dados estruturados da rota
            language: Idioma
        
        Returns:
            dict: Prompt com system e human messages
        """
        return PromptTemplates.get_driver_instructions_prompt(route_data, language)
    
    def generate_driver_instructions_from_data(
        self,
        route_data: Dict[str, Any],
        deliveries: List[Delivery],
        language: str = "pt-BR",
    ) -> ReportResult:
        """
        Gera instruções do motorista a partir de dados de rota estruturados.
        
        Método alternativo que recebe route_data diretamente.
        
        Args:
            route_data: Dados da rota (pode ser dict ou OptimizationResult)
            deliveries: Lista de entregas (para identificar críticas)
            language: Idioma do relatório
        
        Returns:
            ReportResult: Instruções para o motorista
        """
        # Se route_data é OptimizationResult, converter
        if isinstance(route_data, OptimizationResult):
            return self.generate_driver_instructions(route_data, language)
        
        # Preparar dados com informações de prioridade
        enriched_route_data = self._enrich_route_data_with_priorities(
            route_data, deliveries
        )
        
        # Criar prompt
        prompt = self._create_driver_instructions_prompt(
            enriched_route_data, language
        )
        
        # Gerar instruções
        if self.use_direct_api:
            response = self._call_ollama_direct(
                system_prompt=prompt["system"],
                user_prompt=prompt["human"],
            )
            content = response
        else:
            messages = [
                SystemMessage(content=prompt["system"]),
                HumanMessage(content=prompt["human"]),
            ]
            response = self.llm.invoke(messages)
            content = response.content
        
        metadata = {
            "model": self.model_name,
            "temperature": self.temperature,
            "language": language,
            "provider": "ollama",
        }
        
        return ReportResult(
            content=content,
            report_type=ReportType.DRIVER_INSTRUCTIONS.value,
            metadata=metadata,
        )
    
    def _enrich_route_data_with_priorities(
        self, route_data: Dict[str, Any], deliveries: List[Delivery]
    ) -> Dict[str, Any]:
        """
        Enriquece dados da rota com informações de prioridade.
        
        Args:
            route_data: Dados básicos da rota
            deliveries: Lista de entregas
        
        Returns:
            dict: Dados enriquecidos com prioridades
        """
        delivery_dict = {d.id: d for d in deliveries}
        
        # Adicionar informações de prioridade para cada entrega
        enriched_routes = []
        for route_info in route_data.get("routes", []):
            enriched_route = route_info.copy()
            enriched_deliveries = []
            
            for delivery_id in route_info.get("deliveries", []):
                delivery = delivery_dict.get(delivery_id)
                if delivery:
                    delivery_info = {
                        "id": delivery_id,
                        "priority": delivery.priority,
                        "is_critical": delivery.priority == 1,
                        "weight": delivery.weight,
                        "location": delivery.location,
                    }
                    enriched_deliveries.append(delivery_info)
            
            enriched_route["deliveries"] = enriched_deliveries
            enriched_routes.append(enriched_route)
        
        enriched_data = route_data.copy()
        enriched_data["routes"] = enriched_routes
        
        return enriched_data
