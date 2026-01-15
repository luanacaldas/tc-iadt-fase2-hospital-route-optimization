"""
Busca local para melhorar soluções do algoritmo genético.

Aplica operadores de busca local para refinar soluções:
- 2-opt para otimizar rotas individuais
- Swap entre rotas para balancear carga
- Reinserção de entregas
"""

import random
from typing import List, Tuple, Dict, Any
from hospital_routes.core.interfaces import (
    Delivery,
    RouteSolution,
    VehicleConstraints,
)
from hospital_routes.utils.distance import calculate_distance_matrix


class LocalSearch:
    """
    Aplica busca local para melhorar soluções.
    
    Operadores:
    1. 2-opt: Otimiza ordem dentro de uma rota
    2. Inter-route swap: Move entregas entre rotas para balancear
    3. Reinsertion: Reinsere entregas em posições melhores
    """
    
    def __init__(
        self,
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
        depot_location: Tuple[float, float],
        distance_matrix: Dict[Tuple[str, str], float],
    ):
        """
        Args:
            deliveries: Lista de entregas
            vehicles: Lista de veículos
            depot_location: Localização do depósito
            distance_matrix: Matriz de distâncias
        """
        self.deliveries = deliveries
        self.vehicles = vehicles
        self.depot_location = depot_location
        self.distance_matrix = distance_matrix
        self.delivery_dict = {d.id: d for d in deliveries}
    
    def improve_solution(
        self,
        solution: RouteSolution,
        max_iterations: int = 50,
        fitness_calculator: Any = None,
    ) -> RouteSolution:
        """
        Melhora uma solução aplicando busca local.
        
        Args:
            solution: Solução a melhorar
            max_iterations: Número máximo de iterações
            fitness_calculator: Função para calcular fitness
        
        Returns:
            RouteSolution: Solução melhorada
        """
        current_solution = solution
        current_fitness = fitness_calculator.calculate(
            current_solution, self.deliveries, self.vehicles,
            self.depot_location, self.distance_matrix
        ) if fitness_calculator else float('inf')
        
        improved = True
        iterations = 0
        
        while improved and iterations < max_iterations:
            improved = False
            iterations += 1
            
            # Tentar 2-opt em cada rota
            new_routes = []
            for route in current_solution.routes:
                improved_route = self._two_opt(route)
                new_routes.append(improved_route)
            
            # Tentar balanceamento de carga
            balanced_routes = self._balance_loads(new_routes)
            
            # Criar nova solução
            from hospital_routes.core.interfaces import RouteSolution
            new_solution = RouteSolution(
                routes=balanced_routes,
                total_distance=self._calculate_total_distance(balanced_routes),
                total_cost=self._calculate_total_cost(balanced_routes),
                fitness_score=0.0,  # Será recalculado
                violations=[],
            )
            
            # Recalcular fitness
            if fitness_calculator:
                new_fitness = fitness_calculator.calculate(
                    new_solution, self.deliveries, self.vehicles,
                    self.depot_location, self.distance_matrix
                )
                
                if new_fitness < current_fitness:
                    current_solution = new_solution
                    current_fitness = new_fitness
                    improved = True
        
        return current_solution
    
    def _two_opt(self, route: List[str]) -> List[str]:
        """
        Aplica 2-opt para melhorar uma rota.
        
        Tenta todas as inversões de segmentos e mantém a melhor.
        """
        if len(route) < 4:
            return route
        
        best_route = route[:]
        best_distance = self._calculate_route_distance(route)
        improved = True
        
        while improved:
            improved = False
            for i in range(1, len(best_route) - 2):
                for j in range(i + 1, len(best_route)):
                    if j - i == 1:
                        continue
                    
                    # Inverter segmento
                    new_route = best_route[:i] + best_route[i:j][::-1] + best_route[j:]
                    new_distance = self._calculate_route_distance(new_route)
                    
                    if new_distance < best_distance:
                        best_route = new_route
                        best_distance = new_distance
                        improved = True
                        break
                if improved:
                    break
        
        return best_route
    
    def _balance_loads(self, routes: List[List[str]]) -> List[List[str]]:
        """
        Tenta balancear cargas entre rotas movendo entregas.
        
        Move entregas de rotas sobrecarregadas para subutilizadas.
        """
        if len(routes) < 2:
            return routes
        
        # Calcular cargas
        route_loads = []
        for route in routes:
            load = sum(
                self.delivery_dict[d_id].weight
                for d_id in route
                if d_id in self.delivery_dict
            )
            route_loads.append(load)
        
        if not route_loads:
            return routes
        
        mean_load = sum(route_loads) / len(route_loads)
        new_routes = [route[:] for route in routes]
        
        # Tentar mover entregas
        for _ in range(10):  # Máximo de tentativas
            # Encontrar rota mais sobrecarregada e mais subutilizada
            max_idx = max(range(len(route_loads)), key=lambda i: route_loads[i])
            min_idx = min(range(len(route_loads)), key=lambda i: route_loads[i])
            
            if route_loads[max_idx] <= mean_load * 1.1:
                break  # Já está balanceado
            
            if not new_routes[max_idx]:
                break
            
            # Tentar mover uma entrega
            delivery_to_move = random.choice(new_routes[max_idx])
            delivery_weight = self.delivery_dict.get(delivery_to_move, None)
            
            if delivery_weight:
                # Verificar se pode mover sem violar capacidade
                if min_idx < len(self.vehicles):
                    vehicle = self.vehicles[min_idx]
                    if route_loads[min_idx] + delivery_weight.weight <= vehicle.max_capacity:
                        new_routes[max_idx].remove(delivery_to_move)
                        new_routes[min_idx].append(delivery_to_move)
                        route_loads[max_idx] -= delivery_weight.weight
                        route_loads[min_idx] += delivery_weight.weight
        
        return new_routes
    
    def _calculate_route_distance(self, route: List[str]) -> float:
        """Calcula distância de uma rota."""
        if not route:
            return 0.0
        
        distance = 0.0
        depot_key = "depot"
        
        # Depósito → primeira entrega
        distance += self.distance_matrix.get((depot_key, route[0]), 0.0)
        
        # Entre entregas
        for i in range(len(route) - 1):
            distance += self.distance_matrix.get((route[i], route[i + 1]), 0.0)
        
        # Última entrega → depósito
        distance += self.distance_matrix.get((route[-1], depot_key), 0.0)
        
        return distance
    
    def _calculate_total_distance(self, routes: List[List[str]]) -> float:
        """Calcula distância total de todas as rotas."""
        return sum(self._calculate_route_distance(route) for route in routes)
    
    def _calculate_total_cost(self, routes: List[List[str]]) -> float:
        """Calcula custo total (simplificado: distância * custo por km)."""
        total_distance = self._calculate_total_distance(routes)
        cost_per_km = 2.5  # R$ por km
        return total_distance * cost_per_km
