"""
Exceções customizadas do sistema de otimização de rotas.
"""


class HospitalRouteOptimizationError(Exception):
    """Exceção base para erros do sistema."""
    pass


class OptimizationError(HospitalRouteOptimizationError):
    """Erro durante o processo de otimização."""
    pass


class InvalidSolutionError(OptimizationError):
    """Solução inválida gerada pelo otimizador."""
    pass


class ConstraintViolationError(OptimizationError):
    """Violação de restrições do problema."""
    pass


class ReportGenerationError(HospitalRouteOptimizationError):
    """Erro durante a geração de relatório."""
    pass


class LLMConnectionError(ReportGenerationError):
    """Erro de conexão com o serviço de LLM."""
    pass


class InvalidConfigurationError(HospitalRouteOptimizationError):
    """Configuração inválida fornecida."""
    pass


class DataValidationError(HospitalRouteOptimizationError):
    """Erro de validação de dados."""
    pass

