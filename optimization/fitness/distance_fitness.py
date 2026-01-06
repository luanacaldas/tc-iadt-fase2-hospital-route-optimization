"""
Componente de fitness: Distância total.

Calcula a distância total percorrida por todos os veículos.
"""

from typing import List
from hospital_routes.core.interfaces import Delivery, RouteSolution


class DistanceFitness:
    """
    Calcula o componente de distância da função de fitness.
    
    Quanto menor a distância, melhor o fitness.
    """
    
    def __init__(self, weight: float = 1.0):
        """
        Args:
            weight: Peso deste componente na função de fitness
        """
        self.weight = weight
    
    def calculate(
        self,
        solution: RouteSolution,
        deliveries: List[Delivery],
        depot_location: tuple[float, float],
    ) -> float:
        """
        Calcula o componente de distância.
        
        Args:
            solution: Solução de rota
            deliveries: Lista de entregas
            depot_location: Localização do depósito
        
        Returns:
            float: Componente de distância (já multiplicado pelo peso)
        """
        # A distância total já está calculada em solution.total_distance
        return self.weight * solution.total_distance

