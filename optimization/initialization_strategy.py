"""
Estratégias de inicialização da população do algoritmo genético.

Permite diferentes abordagens para gerar a população inicial,
melhorando a convergência do algoritmo.
"""

from abc import ABC, abstractmethod
from typing import List
from hospital_routes.core.interfaces import Delivery, VehicleConstraints


class InitialPopulationStrategy(ABC):
    """
    Interface abstrata para estratégias de inicialização.
    
    Diferentes estratégias podem ser usadas:
    - Random: População completamente aleatória
    - NearestNeighbor: Usa heurística do vizinho mais próximo
    - PriorityFirst: Prioriza entregas críticas
    - Hybrid: Combina múltiplas estratégias
    """
    
    @abstractmethod
    def generate_individual(
        self,
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
        depot_location: tuple[float, float],
    ) -> List[List[str]]:
        """
        Gera um indivíduo (solução) para a população inicial.
        
        Args:
            deliveries: Lista de entregas
            vehicles: Lista de veículos disponíveis
            depot_location: Localização do depósito
        
        Returns:
            List[List[str]]: Lista de rotas, cada rota é lista de IDs de entregas
        """
        pass


class RandomInitializationStrategy(InitialPopulationStrategy):
    """
    Estratégia de inicialização aleatória.
    
    Gera soluções completamente aleatórias.
    Útil para manter diversidade genética.
    """
    
    def generate_individual(
        self,
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
        depot_location: tuple[float, float],
    ) -> List[List[str]]:
        """Gera solução aleatória."""
        import random
        
        # Embaralhar entregas
        delivery_ids = [d.id for d in deliveries]
        random.shuffle(delivery_ids)
        
        # Distribuir aleatoriamente entre veículos
        num_vehicles = min(len(vehicles), len(delivery_ids))
        routes = []
        
        for i in range(num_vehicles):
            # Calcular quantas entregas para este veículo
            start_idx = i * len(delivery_ids) // num_vehicles
            end_idx = (i + 1) * len(delivery_ids) // num_vehicles
            route = delivery_ids[start_idx:end_idx]
            if route:
                routes.append(route)
        
        return routes


class NearestNeighborInitializationStrategy(InitialPopulationStrategy):
    """
    Estratégia de inicialização usando heurística do vizinho mais próximo.
    
    Gera soluções de melhor qualidade inicial, acelerando convergência.
    """
    
    def generate_individual(
        self,
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
        depot_location: tuple[float, float],
    ) -> List[List[str]]:
        """Gera solução usando nearest neighbor."""
        from hospital_routes.utils.distance import calculate_distance
        
        routes = []
        remaining_deliveries = deliveries.copy()
        current_location = depot_location
        
        # Distribuir entregas entre veículos usando nearest neighbor
        for vehicle_idx, vehicle in enumerate(vehicles):
            if not remaining_deliveries:
                break
            
            route = []
            current_weight = 0.0
            current_range = 0.0
            
            while remaining_deliveries:
                # Encontrar entrega mais próxima que cabe no veículo
                nearest = None
                nearest_distance = float('inf')
                
                for delivery in remaining_deliveries:
                    distance = calculate_distance(current_location, delivery.location)
                    
                    # Verificar se cabe no veículo
                    if (current_weight + delivery.weight <= vehicle.max_capacity and
                        current_range + distance <= vehicle.max_range):
                        
                        if distance < nearest_distance:
                            nearest = delivery
                            nearest_distance = distance
                
                if nearest:
                    route.append(nearest.id)
                    current_location = nearest.location
                    current_weight += nearest.weight
                    current_range += nearest_distance
                    remaining_deliveries.remove(nearest)
                else:
                    # Nenhuma entrega cabe, terminar rota deste veículo
                    break
            
            if route:
                routes.append(route)
                current_location = depot_location  # Voltar ao depósito
        
        return routes


class PriorityFirstInitializationStrategy(InitialPopulationStrategy):
    """
    Estratégia que prioriza entregas críticas (priority=1).
    
    Garante que medicamentos sejam atendidos primeiro.
    """
    
    def generate_individual(
        self,
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
        depot_location: tuple[float, float],
    ) -> List[List[str]]:
        """Gera solução priorizando entregas críticas."""
        # Separar entregas por prioridade
        critical_deliveries = [d for d in deliveries if d.priority == 1]
        normal_deliveries = [d for d in deliveries if d.priority != 1]
        
        # Primeiro, distribuir entregas críticas
        routes = []
        for vehicle_idx, vehicle in enumerate(vehicles):
            if not critical_deliveries:
                break
            
            route = []
            current_weight = 0.0
            
            while critical_deliveries:
                delivery = critical_deliveries.pop(0)
                if current_weight + delivery.weight <= vehicle.max_capacity:
                    route.append(delivery.id)
                    current_weight += delivery.weight
                else:
                    critical_deliveries.insert(0, delivery)
                    break
            
            if route:
                routes.append(route)
        
        # Depois, distribuir entregas normais
        # (implementação simplificada - pode ser melhorada)
        for vehicle_idx, vehicle in enumerate(vehicles):
            if vehicle_idx >= len(routes):
                routes.append([])
            
            current_weight = sum(
                d.weight for d in deliveries
                if d.id in routes[vehicle_idx]
            )
            
            for delivery in normal_deliveries[:]:
                if current_weight + delivery.weight <= vehicle.max_capacity:
                    routes[vehicle_idx].append(delivery.id)
                    current_weight += delivery.weight
                    normal_deliveries.remove(delivery)
        
        return routes

