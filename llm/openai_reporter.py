"""
Implementação do gerador de relatórios usando OpenAI via LangChain.

Este módulo implementa o BaseReporter usando LangChain e OpenAI.
"""

import os
import json
from typing import List, Dict, Any, Optional

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.schema import HumanMessage, SystemMessage

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


class OpenAIReporter(BaseReporter):
    """
    Gerador de relatórios usando OpenAI via LangChain.
    
    Implementa BaseReporter usando ChatOpenAI do LangChain.
    """
    
    def __init__(
        self,
        model_name: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        api_key: Optional[str] = None,
    ):
        """
        Args:
            model_name: Nome do modelo OpenAI (ex: "gpt-4", "gpt-3.5-turbo")
            temperature: Temperatura para geração (0.0-2.0)
            max_tokens: Número máximo de tokens
            api_key: Chave da API OpenAI (usa OPENAI_API_KEY env se None)
        """
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Obter API key
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY não encontrada. "
                "Forneça via parâmetro ou variável de ambiente."
            )
        
        # Inicializar LLM
        try:
            self.llm = ChatOpenAI(
                model_name=model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                openai_api_key=api_key,
            )
        except Exception as e:
            raise LLMConnectionError(f"Erro ao conectar com OpenAI: {str(e)}") from e
    
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
            deliveries: Lista de entregas (opcional, para identificar críticas)
        
        Returns:
            ReportResult: Instruções para o motorista
        """
        try:
            # Preparar dados da rota
            # Nota: deliveries não está na interface, mas pode ser extraído de metadata se disponível
            deliveries = optimization_result.solution.metadata.get("deliveries")
            route_data = self._prepare_route_data(optimization_result, deliveries)
            
            # Criar prompt
            prompt = self._create_driver_instructions_prompt(
                route_data, language
            )
            
            # Gerar instruções
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
                "max_tokens": self.max_tokens,
                "language": language,
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
        system_prompt = """Você é um assistente especializado em logística hospitalar.
Sua função é gerar instruções claras, amigáveis e diretivas para motoristas de entrega.

IMPORTANTE:
- Use APENAS os dados fornecidos. Não invente informações.
- Seja direto e objetivo.
- Destaque claramente as entregas CRÍTICAS (medicamentos).
- Use linguagem amigável mas profissional.
- Organize as instruções por veículo e por ordem de parada.
- Alerte sobre a importância das entregas críticas."""

        human_prompt = f"""Gere instruções passo-a-passo para o motorista em {language}.

Dados da rota otimizada:
{json.dumps(route_data, indent=2, ensure_ascii=False)}

Formato esperado:
1. Título: "Instruções de Rota - [Data/Hora]"
2. Resumo: Distância total, número de veículos, tempo estimado
3. Para cada veículo:
   - Cabeçalho: "VEÍCULO [Número]"
   - Lista de paradas em ordem
   - Para cada parada:
     * Número da parada
     * ID da entrega
     * Se for CRÍTICA: ALERTA em destaque (ex: "⚠️ CRÍTICA - MEDICAMENTOS")
     * Instruções de direção (se disponível)
4. Observações finais sobre entregas críticas

Destaque especialmente as entregas marcadas como CRÍTICAS (priority=1).
Use emojis e formatação para tornar o texto mais legível."""

        return {
            "system": system_prompt,
            "human": human_prompt,
        }
    
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
