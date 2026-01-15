"""
Chatbot para operadores do sistema de otimização de rotas.

Permite que operadores façam perguntas sobre rotas, entregas, veículos, etc.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

from hospital_routes.core.interfaces import (
    OptimizationResult,
    Delivery,
    RouteSolution,
)
from hospital_routes.llm.ollama_helper import (
    get_best_available_model,
    check_ollama_running,
    get_model_full_name,
)
from hospital_routes.core.exceptions import LLMConnectionError


@dataclass
class ChatMessage:
    """Mensagem do chat."""
    role: str  # "user" ou "assistant"
    content: str
    timestamp: datetime


class RouteChatbot:
    """
    Chatbot especializado em otimização de rotas hospitalares.
    
    Permite que operadores façam perguntas sobre:
    - Rotas otimizadas
    - Entregas e prioridades
    - Veículos e capacidade
    - Análise de rotas
    - Sugestões de melhorias
    """
    
    def __init__(
        self,
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        num_predict: int = 1500,
    ):
        """
        Args:
            model_name: Nome do modelo Ollama (None = auto-detect)
            temperature: Temperatura para geração
            num_predict: Máximo de tokens
        """
        if not check_ollama_running():
            raise LLMConnectionError(
                "Ollama não está rodando. "
                "Certifique-se de que o Ollama está instalado e rodando."
            )
        
        # Auto-detectar modelo se não especificado
        if model_name is None:
            model_name = get_best_available_model()
            if model_name is None:
                raise LLMConnectionError(
                    "Nenhum modelo Ollama disponível. "
                    "Execute: ollama pull llama3.2"
                )
        
        self.model_name = model_name
        self.temperature = temperature
        self.num_predict = num_predict
        self.conversation_history: List[ChatMessage] = []
        self.optimization_context: Optional[OptimizationResult] = None
        self._deliveries_cache: Optional[List[Delivery]] = None
        
        # Inicializar LLM
        try:
            import ollama
            self.ollama = ollama
        except ImportError:
            raise ImportError("Ollama não está instalado. Execute: pip install ollama")
    
    def set_optimization_context(
        self, 
        result: OptimizationResult,
        deliveries: Optional[List[Delivery]] = None,
    ) -> None:
        """
        Define o contexto de otimização para o chatbot.
        
        Args:
            result: Resultado da otimização
            deliveries: Lista de entregas (opcional, para métricas detalhadas)
        """
        self.optimization_context = result
        if deliveries:
            self._deliveries_cache = deliveries
        else:
            self._deliveries_cache = None
    
    def chat(self, user_message: str) -> str:
        """
        Processa mensagem do usuário e retorna resposta.
        
        Args:
            user_message: Mensagem do usuário
        
        Returns:
            str: Resposta do chatbot
        """
        # Adicionar mensagem do usuário ao histórico
        self.conversation_history.append(
            ChatMessage(role="user", content=user_message, timestamp=datetime.now())
        )
        
        # Preparar contexto
        context = self._build_context()
        
        # Construir mensagens para o LLM
        messages = self._build_messages(context, user_message)
        
        # Chamar Ollama
        try:
            # Obter nome completo do modelo (com tag se disponível)
            model_full_name = get_model_full_name(self.model_name) or self.model_name
            
            response = self.ollama.chat(
                model=model_full_name,
                messages=messages,
                options={
                    "temperature": self.temperature,
                    "num_predict": self.num_predict,
                },
            )
            
            assistant_message = response["message"]["content"]
            
            # Adicionar resposta ao histórico
            self.conversation_history.append(
                ChatMessage(
                    role="assistant",
                    content=assistant_message,
                    timestamp=datetime.now(),
                )
            )
            
            return assistant_message
        
        except Exception as e:
            raise LLMConnectionError(f"Erro ao chamar Ollama: {str(e)}") from e
    
    def _build_context(self) -> Dict[str, Any]:
        """Constrói contexto detalhado a partir do resultado de otimização."""
        if not self.optimization_context:
            return {}
        
        result = self.optimization_context
        solution = result.solution
        
        # Calcular métricas detalhadas por rota
        routes_details = []
        total_weight = 0
        total_critical = 0
        
        for i, route in enumerate(solution.routes):
            # Calcular distância da rota
            route_distance = 0.0
            route_weight = 0.0
            route_critical = 0
            
            # Se temos acesso às entregas, calcular métricas
            if hasattr(self, '_deliveries_cache') and self._deliveries_cache:
                from hospital_routes.utils.distance import calculate_distance
                delivery_dict = {d.id: d for d in self._deliveries_cache}
                
                for j in range(len(route) - 1):
                    if route[j] in delivery_dict and route[j + 1] in delivery_dict:
                        route_distance += calculate_distance(
                            delivery_dict[route[j]].location,
                            delivery_dict[route[j + 1]].location,
                        )
                
                for delivery_id in route:
                    if delivery_id in delivery_dict:
                        d = delivery_dict[delivery_id]
                        route_weight += d.weight
                        if d.priority == 1:
                            route_critical += 1
                        total_weight += d.weight
                        if d.priority == 1:
                            total_critical += 1
            
            routes_details.append({
                "vehicle_id": i + 1,
                "deliveries": route,
                "num_deliveries": len(route),
                "distance": route_distance if route_distance > 0 else solution.total_distance / len(solution.routes),
                "weight": route_weight,
                "critical_deliveries": route_critical,
            })
        
        return {
            "total_distance": solution.total_distance,
            "total_cost": solution.total_cost,
            "fitness_score": solution.fitness_score,
            "num_vehicles": len(solution.routes),
            "num_deliveries": sum(len(r) for r in solution.routes),
            "total_weight": total_weight,
            "total_critical_deliveries": total_critical,
            "execution_time": result.execution_time,
            "generations": result.generations_evolved,
            "routes": routes_details,
            "violations": solution.violations,
            "average_distance_per_vehicle": solution.total_distance / len(solution.routes) if solution.routes else 0,
            "average_deliveries_per_vehicle": sum(len(r) for r in solution.routes) / len(solution.routes) if solution.routes else 0,
        }
    
    def _build_messages(self, context: Dict[str, Any], user_message: str) -> List[Dict]:
        """Constrói mensagens para o LLM."""
        system_prompt = """Você é um assistente especializado em logística hospitalar e otimização de rotas.
Sua função é ajudar operadores a entender e trabalhar com o sistema de otimização de rotas.

IMPORTANTE: Você DEVE usar os dados reais fornecidos no contexto para dar respostas específicas e úteis.
NÃO dê respostas genéricas. Analise os dados e forneça insights concretos baseados nos números reais.

MELHORIAS JÁ IMPLEMENTADAS NO SISTEMA:
- ✅ Balanceamento de carga: O algoritmo já considera balanceamento de carga na função de fitness
- ✅ Busca local: Após o GA, busca local (2-opt) é aplicada para refinar rotas
- ✅ Otimização de distância: O algoritmo minimiza distância total
- ✅ Priorização: Entregas críticas são priorizadas
- ✅ Restrições: Capacidade e autonomia são respeitadas

Quando perguntado sobre melhorias, você DEVE:
1. RECONHECER melhorias já implementadas (balanceamento, busca local)
2. IDENTIFICAR problemas ESPECÍFICOS nos dados fornecidos:
   - Compare números reais entre veículos
   - Identifique desbalanceamentos específicos (ex: "Veículo 2 tem 32.1 km vs média de 28.4 km")
   - Mencione entregas críticas específicas por veículo
3. SUGERIR melhorias CONCRETAS e ACIONÁVEIS:
   - "Redistribuir entrega X do Veículo Y para Veículo Z reduziria distância em N km"
   - "Veículo 3 está subutilizado (3 entregas vs média de 4.5)"
   - Use números específicos dos dados fornecidos
4. EVITAR sugestões genéricas como:
   - "Ajustar distribuição" (muito vago)
   - "Otimizar carga" (não específico)
   - "Revisar rotas" (não acionável)

FORMATO DE RESPOSTA PARA MELHORIAS:
1. Análise dos dados atuais (com números específicos)
2. Problemas identificados (com comparações entre veículos)
3. Melhorias sugeridas (específicas e acionáveis)
4. Impacto esperado (com estimativas numéricas)

Seja claro, objetivo e útil. SEMPRE use os dados concretos fornecidos."""

        # Adicionar contexto detalhado se disponível
        if context:
            routes_info = []
            for route in context.get('routes', []):
                routes_info.append(
                    f"  Veículo {route.get('vehicle_id', '?')}: "
                    f"{route.get('num_deliveries', 0)} entregas, "
                    f"{route.get('distance', 0):.2f} km, "
                    f"{route.get('weight', 0):.1f} kg, "
                    f"{route.get('critical_deliveries', 0)} críticas"
                )
            
            routes_str = "\n".join(routes_info) if routes_info else "Nenhuma rota detalhada disponível"
            
            context_str = f"""
=== CONTEXTO DA OTIMIZAÇÃO (USE ESTES DADOS REAIS) ===

Métricas Gerais:
- Distância total: {context.get('total_distance', 0):.2f} km
- Custo total: R$ {context.get('total_cost', 0):.2f}
- Veículos usados: {context.get('num_vehicles', 0)}
- Total de entregas: {context.get('num_deliveries', 0)}
- Peso total: {context.get('total_weight', 0):.1f} kg
- Entregas críticas: {context.get('total_critical_deliveries', 0)}
- Tempo de execução: {context.get('execution_time', 0):.2f}s
- Gerações do algoritmo: {context.get('generations', 0)}
- Fitness score: {context.get('fitness_score', 0):.4f}
- Violações: {context.get('violations', [])}

Métricas Médias:
- Distância média por veículo: {context.get('average_distance_per_vehicle', 0):.2f} km
- Entregas médias por veículo: {context.get('average_deliveries_per_vehicle', 0):.1f}

Detalhes por Rota:
{routes_str}

=== MELHORIAS JÁ IMPLEMENTADAS NO SISTEMA ===
✅ Balanceamento de carga: O algoritmo já penaliza desbalanceamento na função de fitness
✅ Busca local: Após o GA, busca local (2-opt) é aplicada automaticamente para refinar rotas
✅ Otimização de distância: O algoritmo minimiza distância total percorrida
✅ Priorização: Entregas críticas são priorizadas automaticamente
✅ Restrições: Capacidade e autonomia são respeitadas com penalidades altas

=== INSTRUÇÕES PARA SUGESTÕES DE MELHORIAS ===
Quando perguntado sobre melhorias, você DEVE:

1. RECONHECER melhorias já implementadas:
   - "O sistema já considera balanceamento de carga"
   - "Busca local já é aplicada automaticamente"
   - "Entregas críticas já são priorizadas"

2. IDENTIFICAR problemas ESPECÍFICOS nos dados:
   - Compare números REAIS entre veículos (ex: "Veículo 2: 32.1 km vs Veículo 3: 24.6 km")
   - Calcule desvios da média (ex: "Veículo 2 está 12% acima da média")
   - Identifique entregas críticas específicas (ex: "Veículo 1 tem 2 críticas, Veículo 2 tem 1")

3. SUGERIR melhorias CONCRETAS e ACIONÁVEIS:
   - "Mover entrega X do Veículo Y para Veículo Z reduziria distância em N km"
   - "Veículo 3 está subutilizado: apenas 3 entregas vs média de 4.5"
   - "Redistribuir 1 entrega crítica do Veículo 1 para Veículo 2 melhoraria balanceamento"
   - Use números ESPECÍFICOS dos dados acima

4. EVITAR sugestões genéricas:
   ❌ "Ajustar distribuição" → ✅ "Mover entrega HOSP_005 do Veículo 2 para Veículo 3"
   ❌ "Otimizar carga" → ✅ "Veículo 2 tem 52.8 kg (12% acima da média de 45.4 kg)"
   ❌ "Revisar rotas" → ✅ "Aplicar 2-opt na rota do Veículo 2 pode reduzir 2-3 km"

5. FORMATO DE RESPOSTA:
   a) Análise atual (com números específicos)
   b) Problemas identificados (com comparações)
   c) Melhorias sugeridas (específicas e acionáveis)
   d) Impacto esperado (com estimativas numéricas)

=== REGRAS GERAIS ===
- SEMPRE use os dados REAIS fornecidos acima
- NÃO invente números ou dados
- Seja ESPECÍFICO: mencione IDs de entregas, números de veículos, distâncias exatas
- NÃO dê respostas genéricas sem usar os dados acima
"""
        else:
            context_str = "Nenhum contexto de otimização disponível no momento."
        
        messages = [
            {
                "role": "system",
                "content": system_prompt + "\n\n" + context_str,
            },
        ]
        
        # Adicionar histórico de conversa (últimas 5 mensagens)
        recent_history = self.conversation_history[-10:]  # Últimas 10 mensagens
        for msg in recent_history:
            messages.append({
                "role": msg.role,
                "content": msg.content,
            })
        
        # Adicionar mensagem atual do usuário
        messages.append({
            "role": "user",
            "content": user_message,
        })
        
        return messages
    
    def clear_history(self) -> None:
        """Limpa histórico de conversa."""
        self.conversation_history.clear()
    
    def get_history(self) -> List[ChatMessage]:
        """Retorna histórico de conversa."""
        return self.conversation_history.copy()


class RouteAnalyzer:
    """
    Analisador inteligente de rotas usando LLM.
    
    Fornece análises profundas sobre rotas otimizadas.
    """
    
    def __init__(
        self,
        model_name: Optional[str] = None,
        temperature: float = 0.5,  # Mais baixo para análises mais consistentes
    ):
        """
        Args:
            model_name: Nome do modelo Ollama (None = auto-detect)
            temperature: Temperatura para geração
        """
        if not check_ollama_running():
            raise LLMConnectionError("Ollama não está rodando")
        
        if model_name is None:
            model_name = get_best_available_model()
            if model_name is None:
                raise LLMConnectionError("Nenhum modelo Ollama disponível")
        
        self.model_name = model_name
        self.temperature = temperature
        
        try:
            import ollama
            self.ollama = ollama
        except ImportError:
            raise ImportError("Ollama não está instalado")
    
    def analyze_route(
        self,
        optimization_result: OptimizationResult,
        deliveries: List[Delivery],
        accident_provider: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """
        Analisa uma rota otimizada de forma inteligente.
        
        Args:
            optimization_result: Resultado da otimização
            deliveries: Lista de entregas
            accident_provider: Provedor de dados de acidentes (opcional)
        
        Returns:
            dict: Análise detalhada
        """
        solution = optimization_result.solution
        
        # Preparar dados para análise
        analysis_data = {
            "routes": [],
            "total_distance": solution.total_distance,
            "total_cost": solution.total_cost,
            "fitness_score": solution.fitness_score,
            "num_vehicles": len(solution.routes),
            "violations": solution.violations,
        }
        
        # Adicionar detalhes de cada rota
        for route_idx, route in enumerate(solution.routes):
            route_info = {
                "vehicle_id": route_idx + 1,
                "deliveries": route,
                "num_deliveries": len(route),
            }
            
            # Adicionar informações de entregas
            route_deliveries = [
                {
                    "id": d.id,
                    "priority": d.priority,
                    "weight": d.weight,
                    "is_critical": d.priority == 1,
                }
                for d in deliveries
                if d.id in route
            ]
            route_info["delivery_details"] = route_deliveries
            
            # Adicionar análise de segurança se disponível
            if accident_provider:
                from hospital_routes.utils.distance import calculate_distance
                route_coords = []
                for delivery_id in route:
                    delivery = next((d for d in deliveries if d.id == delivery_id), None)
                    if delivery:
                        route_coords.append(delivery.location)
                
                if route_coords:
                    route_risk = accident_provider.get_route_risk(route_coords)
                    route_info["safety"] = route_risk
            
            analysis_data["routes"].append(route_info)
        
        # Gerar análise com LLM
        analysis_text = self._generate_analysis(analysis_data)
        
        return {
            "summary": analysis_text,
            "data": analysis_data,
            "recommendations": self._generate_recommendations(analysis_data),
        }
    
    def _generate_analysis(self, data: Dict[str, Any]) -> str:
        """Gera análise textual usando LLM."""
        import json
        
        prompt = f"""Analise esta otimização de rotas hospitalares e forneça uma análise detalhada.

Dados da otimização:
{json.dumps(data, indent=2, ensure_ascii=False)}

Forneça uma análise que inclua:
1. Avaliação geral da solução
2. Pontos fortes
3. Pontos de atenção
4. Eficiência de uso de veículos
5. Distribuição de entregas críticas
6. Segurança das rotas (se disponível)

Seja objetivo, técnico mas acessível."""
        
        try:
            # Obter nome completo do modelo
            model_full_name = get_model_full_name(self.model_name) or self.model_name
            
            response = self.ollama.chat(
                model=model_full_name,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um especialista em logística e otimização de rotas hospitalares.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                options={
                    "temperature": self.temperature,
                    "num_predict": 2000,
                },
            )
            
            return response["message"]["content"]
        except Exception as e:
            return f"Erro ao gerar análise: {str(e)}"
    
    def _generate_recommendations(self, data: Dict[str, Any]) -> List[str]:
        """Gera recomendações baseadas nos dados."""
        import json
        
        prompt = f"""Baseado nestes dados de otimização, forneça 3-5 recomendações práticas e acionáveis.

Dados:
{json.dumps(data, indent=2, ensure_ascii=False)}

Forneça recomendações em formato de lista, sendo específico e prático."""
        
        try:
            # Obter nome completo do modelo
            model_full_name = get_model_full_name(self.model_name) or self.model_name
            
            response = self.ollama.chat(
                model=model_full_name,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um consultor especializado em otimização logística.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                options={
                    "temperature": self.temperature,
                    "num_predict": 1000,
                },
            )
            
            # Extrair recomendações da resposta
            content = response["message"]["content"]
            # Tentar extrair lista de recomendações
            recommendations = []
            for line in content.split("\n"):
                line = line.strip()
                if line and (line.startswith("-") or line.startswith("•") or line[0].isdigit()):
                    recommendations.append(line.lstrip("- •0123456789. ").strip())
            
            return recommendations[:5]  # Máximo 5 recomendações
        except Exception as e:
            return [f"Erro ao gerar recomendações: {str(e)}"]
