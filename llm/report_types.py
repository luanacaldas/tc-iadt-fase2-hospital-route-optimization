"""
Tipos de relatório suportados pelo sistema.

Este enum define explicitamente os tipos de relatório que podem ser gerados,
evitando "prompt spaghetti" e garantindo consistência.

NOTA: Este módulo é mantido para compatibilidade.
O enum principal está em hospital_routes.core.interfaces.ReportType
"""

from hospital_routes.core.interfaces import ReportType

__all__ = ["ReportType"]
    """
    Tipos de relatório disponíveis.
    
    DRIVER_INSTRUCTIONS: Instruções passo-a-passo para motorista
    DAILY_SUMMARY: Resumo diário de operações
    WEEKLY_ANALYSIS: Análise semanal de performance
    MANAGERIAL_REPORT: Relatório gerencial completo (economia e eficiência)
    """
    
    DRIVER_INSTRUCTIONS = "driver_instructions"
    DAILY_SUMMARY = "daily_summary"
    WEEKLY_ANALYSIS = "weekly_analysis"
    MANAGERIAL_REPORT = "managerial_report"
    
    def __str__(self) -> str:
        return self.value

