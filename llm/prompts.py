"""
Templates de prompts para geração de relatórios.

Este módulo contém os templates de prompts organizados por tipo de relatório,
seguindo o enum ReportType.
"""

from hospital_routes.core.interfaces import ReportType


class PromptTemplates:
    """
    Templates de prompts para diferentes tipos de relatório.
    
    Cada template recebe dados estruturados e gera um prompt formatado
    para o LLM.
    """
    
    @staticmethod
    def get_driver_instructions_prompt(
        route_data: dict,
        language: str = "pt-BR",
    ) -> dict:
        """
        Gera prompt para instruções do motorista.
        
        Args:
            route_data: Dados da rota em formato dict
            language: Idioma do relatório
        
        Returns:
            dict: Prompt com system e human messages
        """
        import json
        
        system_prompt = """Você é um assistente especializado em logística hospitalar.
Sua função é gerar instruções claras, amigáveis e diretivas para motoristas de entrega.

IMPORTANTE:
- Use APENAS os dados fornecidos. Não invente informações.
- Seja direto e objetivo.
- Destaque claramente as entregas CRÍTICAS (medicamentos).
- Use linguagem amigável mas profissional.
- Organize as instruções por veículo e por ordem de parada.
- Alerte sobre a importância das entregas críticas.
- Use formatação clara (listas, destaques, emojis quando apropriado)."""

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

Destaque especialmente as entregas marcadas como CRÍTICAS (priority=1 ou is_critical=true).
Use emojis e formatação para tornar o texto mais legível."""

        return {
            "system": system_prompt,
            "human": human_prompt,
        }
    
    @staticmethod
    def get_managerial_report_prompt(
        optimization_result: dict,
        additional_context: dict = None,
        language: str = "pt-BR",
    ) -> str:
        """
        Gera prompt para relatório gerencial.
        
        Args:
            optimization_result: Dados da otimização em formato dict
            additional_context: Contexto adicional (ex: custos anteriores)
            language: Idioma do relatório
        
        Returns:
            str: Prompt formatado
        """
        # TODO: Implementar template completo
        context_str = f"\nContexto adicional: {additional_context}" if additional_context else ""
        
        return f"""
        Gere um relatório gerencial completo em {language}.
        
        Use APENAS os dados fornecidos abaixo:
        {optimization_result}
        {context_str}
        
        O relatório deve incluir:
        1. Resumo executivo
        2. Economia gerada
        3. Eficiência operacional
        4. Métricas de performance
        """
    
    @staticmethod
    def get_daily_summary_prompt(
        optimization_result: dict,
        language: str = "pt-BR",
    ) -> str:
        """Gera prompt para resumo diário."""
        # TODO: Implementar
        return f"Gere resumo diário em {language}."
    
    @staticmethod
    def get_weekly_analysis_prompt(
        optimization_results: list,
        language: str = "pt-BR",
    ) -> str:
        """Gera prompt para análise semanal."""
        # TODO: Implementar
        return f"Gere análise semanal em {language}."

