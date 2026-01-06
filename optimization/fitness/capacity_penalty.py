"""
Componente de fitness: Penalidade por violação de capacidade.

Penaliza soluções que excedem a capacidade máxima dos veículos.
"""

from typing import List
from hospital_routes.core.interfaces import Delivery, RouteSolution, VehicleConstraints


class CapacityPenalty:
    """
    Calcula a penalidade por violação de capacidade.
    
    Quanto maior a violação, maior a penalidade.
    """
    
    def __init__(self, penalty_weight: float = 1000.0):
        """
        Args:
            penalty_weight: Peso da penalidade (deve ser alto para desencorajar violações)
        """
        self.penalty_weight = penalty_weight
    
    def calculate(
        self,
        solution: RouteSolution,
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
    ) -> float:
        """
        Calcula a penalidade total por violação de capacidade.
        
        Args:
            solution: Solução de rota
            deliveries: Lista de entregas
            vehicles: Lista de veículos com restrições
        
        Returns:
            float: Penalidade total (já multiplicada pelo peso)
        """
        total_penalty = 0.0
        
        # Criar dicionário de entregas para acesso rápido
        delivery_dict = {d.id: d for d in deliveries}
        
        # Verificar cada rota
        for route_idx, route in enumerate(solution.routes):
            if route_idx >= len(vehicles):
                # Mais rotas que veículos disponíveis - penalidade alta
                total_penalty += self.penalty_weight * 1000
                continue
            
            vehicle = vehicles[route_idx]
            route_weight = sum(
                delivery_dict[delivery_id].weight
                for delivery_id in route
                if delivery_id in delivery_dict
            )
            
            # Calcular violação de capacidade
            if route_weight > vehicle.max_capacity:
                violation = route_weight - vehicle.max_capacity
                total_penalty += self.penalty_weight * violation
        
        return total_penalty

