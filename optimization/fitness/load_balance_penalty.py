"""
Componente de fitness: Penalidade por desbalanceamento de carga.

Penaliza soluções onde a carga está desbalanceada entre veículos.
"""

from typing import List
from hospital_routes.core.interfaces import (
    Delivery,
    RouteSolution,
    VehicleConstraints,
)


class LoadBalancePenalty:
    """
    Calcula penalidade por desbalanceamento de carga entre veículos.
    
    Quanto mais balanceada a carga, menor a penalidade.
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
        vehicles: List[VehicleConstraints],
    ) -> float:
        """
        Calcula penalidade por desbalanceamento.
        
        Usa desvio padrão das cargas para medir desbalanceamento.
        
        Args:
            solution: Solução de rota
            deliveries: Lista de entregas
            vehicles: Lista de veículos
        
        Returns:
            float: Penalidade por desbalanceamento (já multiplicada pelo peso)
        """
        if not solution.routes:
            return 0.0
        
        delivery_dict = {d.id: d for d in deliveries}
        
        # Calcular carga de cada rota
        route_loads = []
        for route in solution.routes:
            route_weight = sum(
                delivery_dict[d_id].weight
                for d_id in route
                if d_id in delivery_dict
            )
            route_loads.append(route_weight)
        
        if not route_loads:
            return 0.0
        
        # Calcular desvio padrão das cargas
        mean_load = sum(route_loads) / len(route_loads)
        variance = sum((load - mean_load) ** 2 for load in route_loads) / len(route_loads)
        std_dev = variance ** 0.5
        
        # Normalizar pelo número de veículos e peso médio
        if mean_load > 0:
            coefficient_of_variation = std_dev / mean_load
        else:
            coefficient_of_variation = 0.0
        
        # Penalidade proporcional ao coeficiente de variação
        penalty = coefficient_of_variation * mean_load
        
        return self.weight * penalty
