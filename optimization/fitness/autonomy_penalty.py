"""
Componente de fitness: Penalidade por violação de autonomia.

Penaliza soluções que excedem a autonomia máxima dos veículos.
"""

from typing import List
from hospital_routes.core.interfaces import Delivery, RouteSolution, VehicleConstraints


class AutonomyPenalty:
    """
    Calcula a penalidade por violação de autonomia.
    
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
        depot_location: tuple[float, float],
        distance_matrix: dict[tuple[str, str], float],
    ) -> float:
        """
        Calcula a penalidade total por violação de autonomia.
        
        Args:
            solution: Solução de rota
            deliveries: Lista de entregas
            vehicles: Lista de veículos com restrições
            depot_location: Localização do depósito
            distance_matrix: Matriz de distâncias entre pontos
        
        Returns:
            float: Penalidade total (já multiplicada pelo peso)
        """
        total_penalty = 0.0
        
        # Verificar cada rota
        for route_idx, route in enumerate(solution.routes):
            if route_idx >= len(vehicles):
                # Mais rotas que veículos disponíveis - penalidade alta
                total_penalty += self.penalty_weight * 1000
                continue
            
            vehicle = vehicles[route_idx]
            
            # Calcular distância total da rota
            route_distance = 0.0
            
            # Distância do depósito até primeira entrega
            if route:
                first_delivery = next(
                    (d for d in deliveries if d.id == route[0]), None
                )
                if first_delivery:
                    route_distance += self._calculate_distance(
                        depot_location, first_delivery.location, distance_matrix
                    )
            
            # Distâncias entre entregas
            for i in range(len(route) - 1):
                delivery1 = next((d for d in deliveries if d.id == route[i]), None)
                delivery2 = next((d for d in deliveries if d.id == route[i + 1]), None)
                if delivery1 and delivery2:
                    route_distance += self._calculate_distance(
                        delivery1.location, delivery2.location, distance_matrix
                    )
            
            # Distância da última entrega até depósito
            if route:
                last_delivery = next(
                    (d for d in deliveries if d.id == route[-1]), None
                )
                if last_delivery:
                    route_distance += self._calculate_distance(
                        last_delivery.location, depot_location, distance_matrix
                    )
            
            # Calcular violação de autonomia
            if route_distance > vehicle.max_range:
                violation = route_distance - vehicle.max_range
                total_penalty += self.penalty_weight * violation
        
        return total_penalty
    
    def _calculate_distance(
        self,
        loc1: tuple[float, float],
        loc2: tuple[float, float],
        distance_matrix: dict[tuple[str, str], float],
    ) -> float:
        """Calcula distância entre dois pontos usando matriz ou cálculo direto."""
        # Se temos matriz de distâncias, usar ela
        key = (f"{loc1[0]},{loc1[1]}", f"{loc2[0]},{loc2[1]}")
        if key in distance_matrix:
            return distance_matrix[key]
        
        # Fallback: cálculo simples (Euclidiano - não ideal para geografia, mas funcional)
        from math import sqrt
        return sqrt((loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1]) ** 2)

