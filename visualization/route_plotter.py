"""
Plotagem de rotas usando Matplotlib.

Este módulo gera visualizações comparativas de rotas.
Consome apenas DTOs, não entidades de domínio.
"""

from typing import List
from hospital_routes.core.models import OptimizationMetricsDTO

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None  # type: ignore


class RoutePlotter:
    """
    Gera gráficos comparativos de rotas.
    
    Consome apenas DTOs, não entidades de domínio.
    """
    
    @staticmethod
    def plot_fitness_evolution(
        fitness_history: List[float],
        output_path: str = "fitness_evolution.png",
    ) -> None:
        """
        Plota a evolução do fitness ao longo das gerações.
        
        Args:
            fitness_history: Lista de valores de fitness por geração
            output_path: Caminho para salvar o gráfico
        
        Raises:
            ImportError: Se matplotlib não estiver instalado
        """
        if plt is None:
            raise ImportError("matplotlib não está instalado")
        
        plt.figure(figsize=(10, 6))
        plt.plot(fitness_history)
        plt.xlabel("Geração")
        plt.ylabel("Fitness")
        plt.title("Evolução do Fitness")
        plt.grid(True)
        plt.savefig(output_path)
        plt.close()
    
    @staticmethod
    def plot_metrics_comparison(
        metrics: List[OptimizationMetricsDTO],
        output_path: str = "metrics_comparison.png",
    ) -> None:
        """
        Plota comparação de métricas entre diferentes otimizações.
        
        Args:
            metrics: Lista de métricas para comparar
            output_path: Caminho para salvar o gráfico
        """
        # TODO: Implementar gráfico comparativo
        pass

