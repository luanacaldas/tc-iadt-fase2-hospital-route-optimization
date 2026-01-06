"""
Implementação do Algoritmo Genético para otimização de rotas.

Este módulo implementa o BaseOptimizer usando Algoritmos Genéticos com DEAP.
"""

import time
import random
from typing import List, Dict, Tuple, Any, Optional
from dataclasses import dataclass

from deap import base, creator, tools
import numpy as np

from hospital_routes.core.interfaces import (
    BaseOptimizer,
    Delivery,
    VehicleConstraints,
    OptimizationConfig,
    RouteSolution,
    OptimizationResult,
)
from hospital_routes.core.exceptions import OptimizationError
from hospital_routes.optimization.fitness.composite_fitness import CompositeFitness
from hospital_routes.optimization.initialization_strategy import (
    InitialPopulationStrategy,
    RandomInitializationStrategy,
    NearestNeighborInitializationStrategy,
    PriorityFirstInitializationStrategy,
)
from hospital_routes.utils.config import FitnessWeights, SystemConfig
from hospital_routes.utils.distance import calculate_distance, calculate_distance_matrix
from hospital_routes.utils.validators import validate_deliveries, validate_vehicles


@dataclass
class Location:
    """
    Representa uma localização geográfica.
    
    Wrapper para tupla (latitude, longitude) com métodos auxiliares.
    """
    
    latitude: float
    longitude: float
    
    def to_tuple(self) -> Tuple[float, float]:
        """Retorna como tupla (lat, lon)."""
        return (self.latitude, self.longitude)
    
    @classmethod
    def from_tuple(cls, location: Tuple[float, float]) -> "Location":
        """Cria Location a partir de tupla."""
        return cls(latitude=location[0], longitude=location[1])
    
    def distance_to(self, other: "Location") -> float:
        """Calcula distância até outra localização em km."""
        return calculate_distance(self.to_tuple(), other.to_tuple())


@dataclass
class Route:
    """
    Representa uma rota de um veículo no contexto do algoritmo genético.
    
    Esta é uma classe auxiliar para o GA, diferente da entidade de domínio.
    """
    
    vehicle_id: int
    delivery_ids: List[str]
    
    def __len__(self) -> int:
        """Retorna número de entregas na rota."""
        return len(self.delivery_ids)
    
    def is_empty(self) -> bool:
        """Verifica se a rota está vazia."""
        return len(self.delivery_ids) == 0
    
    def add_delivery(self, delivery_id: str) -> None:
        """Adiciona uma entrega à rota."""
        if delivery_id not in self.delivery_ids:
            self.delivery_ids.append(delivery_id)
    
    def remove_delivery(self, delivery_id: str) -> None:
        """Remove uma entrega da rota."""
        if delivery_id in self.delivery_ids:
            self.delivery_ids.remove(delivery_id)
    
    def to_list(self) -> List[str]:
        """Converte para lista de IDs."""
        return self.delivery_ids.copy()


class GeneticAlgorithmOptimizer(BaseOptimizer):
    """
    Otimizador de rotas usando Algoritmo Genético.
    
    Implementa o BaseOptimizer usando DEAP para evolução genética.
    """
    
    def __init__(
        self,
        fitness_weights: Optional[FitnessWeights] = None,
        initialization_strategy: Optional[InitialPopulationStrategy] = None,
    ):
        """
        Args:
            fitness_weights: Pesos da função de fitness (usa padrão se None)
            initialization_strategy: Estratégia de inicialização (usa Random se None)
        """
        self.fitness_weights = fitness_weights or FitnessWeights()
        self.initialization_strategy = (
            initialization_strategy or RandomInitializationStrategy()
        )
        self.composite_fitness = CompositeFitness(self.fitness_weights)
        
        # Cache de dados
        self._deliveries: List[Delivery] = []
        self._vehicles: List[VehicleConstraints] = []
        self._depot_location: Tuple[float, float] = (0.0, 0.0)
        self._distance_matrix: Dict[Tuple[str, str], float] = {}
        self._delivery_dict: Dict[str, Delivery] = {}
    
    def optimize(
        self,
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
        config: OptimizationConfig,
        depot_location: Tuple[float, float],
    ) -> OptimizationResult:
        """
        Otimiza as rotas usando algoritmo genético.
        
        Args:
            deliveries: Lista de entregas
            vehicles: Lista de veículos disponíveis
            config: Configuração do algoritmo
            depot_location: Localização do depósito
        
        Returns:
            OptimizationResult: Resultado da otimização
        
        Raises:
            OptimizationError: Se houver erro na otimização
        """
        start_time = time.time()
        
        try:
            # Validar inputs
            validate_deliveries(deliveries)
            validate_vehicles(vehicles)
            
            # Armazenar dados para uso nos operadores
            self._deliveries = deliveries
            self._vehicles = vehicles
            self._depot_location = depot_location
            self._delivery_dict = {d.id: d for d in deliveries}
            
            # Calcular matriz de distâncias
            self._distance_matrix = self._build_distance_matrix(
                deliveries, depot_location
            )
            
            # Configurar DEAP
            self._setup_deap()
            
            # Criar população inicial
            population = self._create_initial_population(
                deliveries, vehicles, depot_location, config
            )
            
            # Avaliar população inicial
            fitnesses = list(map(self._evaluate_individual, population))
            for ind, fit in zip(population, fitnesses):
                ind.fitness.values = (fit,)
            
            # Histórico de fitness
            best_fitness_history = []
            best_fitness = float('inf')
            generations_without_improvement = 0
            
            # Evolução
            for generation in range(config.generations):
                # Seleção
                offspring = self._select(population, config)
                
                # Crossover
                offspring = self._crossover(offspring, config)
                
                # Mutação
                offspring = self._mutate(offspring, config)
                
                # Avaliar novos indivíduos
                invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
                fitnesses = list(map(self._evaluate_individual, invalid_ind))
                for ind, fit in zip(invalid_ind, fitnesses):
                    ind.fitness.values = (fit,)
                
                # Substituir população (elitismo)
                population = self._replace_with_elitism(
                    population, offspring, config
                )
                
                # Estatísticas
                fits = [ind.fitness.values[0] for ind in population]
                current_best = min(fits)
                best_fitness_history.append(current_best)
                
                # Early stopping
                if current_best < best_fitness:
                    best_fitness = current_best
                    generations_without_improvement = 0
                else:
                    generations_without_improvement += 1
                
                if (
                    config.max_iterations_without_improvement
                    and generations_without_improvement
                    >= config.max_iterations_without_improvement
                ):
                    break
            
            # Melhor solução
            best_individual = tools.selBest(population, 1)[0]
            solution = self._individual_to_route_solution(
                best_individual, deliveries, vehicles, depot_location
            )
            
            execution_time = time.time() - start_time
            
            return OptimizationResult(
                solution=solution,
                execution_time=execution_time,
                generations_evolved=generation + 1,
                best_fitness_history=best_fitness_history,
                config=config,
                statistics={
                    "final_best_fitness": best_fitness,
                    "final_avg_fitness": np.mean(fits),
                    "final_worst_fitness": max(fits),
                    "generations_without_improvement": generations_without_improvement,
                },
            )
        
        except Exception as e:
            raise OptimizationError(f"Erro durante otimização: {str(e)}") from e
    
    def validate_solution(
        self,
        solution: RouteSolution,
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
    ) -> bool:
        """
        Valida se uma solução atende todas as restrições.
        
        Args:
            solution: Solução a validar
            deliveries: Lista de entregas
            vehicles: Lista de veículos
        
        Returns:
            bool: True se válida, False caso contrário
        """
        delivery_dict = {d.id: d for d in deliveries}
        
        # Verificar se todas as entregas estão nas rotas
        all_delivery_ids = set(d.id for d in deliveries)
        solution_delivery_ids = set()
        for route in solution.routes:
            solution_delivery_ids.update(route)
        
        if all_delivery_ids != solution_delivery_ids:
            return False
        
        # Verificar restrições de capacidade e autonomia
        for route_idx, route in enumerate(solution.routes):
            if route_idx >= len(vehicles):
                return False
            
            vehicle = vehicles[route_idx]
            
            # Verificar capacidade
            route_weight = sum(
                delivery_dict[d_id].weight
                for d_id in route
                if d_id in delivery_dict
            )
            if route_weight > vehicle.max_capacity:
                return False
        
        return True
    
    def _setup_deap(self) -> None:
        """Configura DEAP (creator e toolbox)."""
        # Criar tipos se ainda não existirem
        if not hasattr(creator, "FitnessMin"):
            creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        
        if not hasattr(creator, "Individual"):
            creator.create(
                "Individual",
                list,
                fitness=creator.FitnessMin,
            )
        
        # Toolbox
        self.toolbox = base.Toolbox()
        
        # Registros de operadores serão feitos dinamicamente
        # pois dependem dos dados do problema
    
    def _build_distance_matrix(
        self,
        deliveries: List[Delivery],
        depot_location: Tuple[float, float],
    ) -> Dict[Tuple[str, str], float]:
        """
        Constrói matriz de distâncias entre todos os pontos.
        
        Args:
            deliveries: Lista de entregas
            depot_location: Localização do depósito
        
        Returns:
            dict: Matriz de distâncias (chave: (from_id, to_id))
        """
        matrix = {}
        
        # Distâncias entre entregas
        for d1 in deliveries:
            for d2 in deliveries:
                if d1.id != d2.id:
                    key = (d1.id, d2.id)
                    matrix[key] = calculate_distance(d1.location, d2.location)
        
        # Distâncias do depósito para entregas e vice-versa
        depot_key = "depot"
        for d in deliveries:
            # Depósito → Entrega
            matrix[(depot_key, d.id)] = calculate_distance(
                depot_location, d.location
            )
            # Entrega → Depósito
            matrix[(d.id, depot_key)] = calculate_distance(
                d.location, depot_location
            )
        
        return matrix
    
    def _create_initial_population(
        self,
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
        depot_location: Tuple[float, float],
        config: OptimizationConfig,
    ) -> List:
        """
        Cria população inicial usando estratégia configurada.
        
        Args:
            deliveries: Lista de entregas
            vehicles: Lista de veículos
            depot_location: Localização do depósito
            config: Configuração
        
        Returns:
            List: População inicial
        """
        population = []
        
        for _ in range(config.population_size):
            routes_list = self.initialization_strategy.generate_individual(
                deliveries, vehicles, depot_location
            )
            individual = creator.Individual(routes_list)
            population.append(individual)
        
        return population
    
    def _evaluate_individual(self, individual: List[List[str]]) -> float:
        """
        Avalia um indivíduo (solução) calculando seu fitness.
        
        Args:
            individual: Indivíduo (lista de rotas)
        
        Returns:
            float: Fitness (quanto menor, melhor)
        """
        # Converter para RouteSolution
        solution = self._routes_list_to_solution(individual)
        
        # Calcular fitness usando CompositeFitness
        fitness = self.composite_fitness.calculate(
            solution,
            self._deliveries,
            self._vehicles,
            self._depot_location,
            self._distance_matrix,
        )
        
        return fitness
    
    def _routes_list_to_solution(
        self, routes_list: List[List[str]]
    ) -> RouteSolution:
        """
        Converte lista de rotas em RouteSolution.
        
        Args:
            routes_list: Lista de rotas (cada rota é lista de IDs)
        
        Returns:
            RouteSolution: Solução de rota
        """
        # Calcular distância total
        total_distance = self._calculate_total_distance(routes_list)
        
        # Calcular custo total
        total_cost = self._calculate_total_cost(routes_list, total_distance)
        
        # Calcular violações
        violations = self._calculate_violations(routes_list)
        
        # Criar solução
        solution = RouteSolution(
            routes=routes_list,
            total_distance=total_distance,
            total_cost=total_cost,
            fitness_score=0.0,  # Será calculado depois
            violations=violations,
            metadata={},
        )
        
        # Calcular fitness
        fitness = self.composite_fitness.calculate(
            solution,
            self._deliveries,
            self._vehicles,
            self._depot_location,
            self._distance_matrix,
        )
        solution.fitness_score = fitness
        
        return solution
    
    def _calculate_total_distance(
        self, routes_list: List[List[str]]
    ) -> float:
        """Calcula distância total de todas as rotas."""
        total = 0.0
        depot_key = "depot"
        
        for route in routes_list:
            if not route:
                continue
            
            # Depósito → primeira entrega
            total += self._distance_matrix.get(
                (depot_key, route[0]), 0.0
            )
            
            # Entre entregas
            for i in range(len(route) - 1):
                total += self._distance_matrix.get(
                    (route[i], route[i + 1]), 0.0
                )
            
            # Última entrega → depósito
            total += self._distance_matrix.get(
                (route[-1], depot_key), 0.0
            )
        
        return total
    
    def _calculate_total_cost(
        self, routes_list: List[List[str]], total_distance: float
    ) -> float:
        """Calcula custo total."""
        cost = 0.0
        
        # Custo de combustível
        for route_idx, route in enumerate(routes_list):
            if route_idx < len(self._vehicles):
                vehicle = self._vehicles[route_idx]
                route_distance = self._calculate_route_distance(route)
                cost += route_distance * vehicle.fuel_cost_per_km
                
                # Custo do motorista (estimado)
                route_time = route_distance / 50.0  # 50 km/h média
                cost += route_time * vehicle.driver_cost_per_hour
        
        return cost
    
    def _calculate_route_distance(self, route: List[str]) -> float:
        """Calcula distância de uma rota específica."""
        if not route:
            return 0.0
        
        distance = 0.0
        depot_key = "depot"
        
        # Depósito → primeira entrega
        distance += self._distance_matrix.get((depot_key, route[0]), 0.0)
        
        # Entre entregas
        for i in range(len(route) - 1):
            distance += self._distance_matrix.get(
                (route[i], route[i + 1]), 0.0
            )
        
        # Última entrega → depósito
        distance += self._distance_matrix.get((route[-1], depot_key), 0.0)
        
        return distance
    
    def _calculate_violations(
        self, routes_list: List[List[str]]
    ) -> Dict[str, float]:
        """Calcula violações de restrições."""
        violations = {
            "capacity": 0.0,
            "autonomy": 0.0,
        }
        
        for route_idx, route in enumerate(routes_list):
            if route_idx >= len(self._vehicles):
                continue
            
            vehicle = self._vehicles[route_idx]
            
            # Violação de capacidade
            route_weight = sum(
                self._delivery_dict[d_id].weight
                for d_id in route
                if d_id in self._delivery_dict
            )
            if route_weight > vehicle.max_capacity:
                violations["capacity"] += route_weight - vehicle.max_capacity
            
            # Violação de autonomia
            route_distance = self._calculate_route_distance(route)
            if route_distance > vehicle.max_range:
                violations["autonomy"] += route_distance - vehicle.max_range
        
        return violations
    
    def _select(
        self, population: List, config: OptimizationConfig
    ) -> List:
        """Seleção de indivíduos para reprodução."""
        # Seleção por torneio
        selected = tools.selTournament(
            population, len(population), tournsize=3
        )
        return selected
    
    def _crossover(
        self, offspring: List, config: OptimizationConfig
    ) -> List:
        """Operador de crossover."""
        for i in range(0, len(offspring) - 1, 2):
            if random.random() < config.crossover_rate:
                offspring[i], offspring[i + 1] = self._route_crossover(
                    offspring[i], offspring[i + 1]
                )
                del offspring[i].fitness.values
                del offspring[i + 1].fitness.values
        
        return offspring
    
    def _route_crossover(
        self, ind1: List[List[str]], ind2: List[List[str]]
    ) -> Tuple[List[List[str]], List[List[str]]]:
        """
        Crossover específico para rotas VRP.
        
        Usa Order Crossover (OX) adaptado para múltiplas rotas.
        """
        # Flatten rotas
        flat1 = [d_id for route in ind1 for d_id in route]
        flat2 = [d_id for route in ind2 for d_id in route]
        
        # Crossover OX
        if len(flat1) < 2 or len(flat2) < 2:
            return ind1, ind2
        
        # Selecionar segmento
        start = random.randint(0, len(flat1) - 1)
        end = random.randint(start + 1, len(flat1))
        
        # Filho 1
        segment1 = flat1[start:end]
        child1_flat = segment1 + [d for d in flat2 if d not in segment1]
        
        # Filho 2
        segment2 = flat2[start:min(end, len(flat2))]
        child2_flat = segment2 + [d for d in flat1 if d not in segment2]
        
        # Reconstruir rotas (distribuir entre veículos)
        child1 = self._redistribute_to_routes(
            child1_flat, len(ind1), self._vehicles
        )
        child2 = self._redistribute_to_routes(
            child2_flat, len(ind2), self._vehicles
        )
        
        return child1, child2
    
    def _redistribute_to_routes(
        self,
        delivery_ids: List[str],
        num_routes: int,
        vehicles: List[VehicleConstraints],
    ) -> List[List[str]]:
        """
        Redistribui entregas entre rotas respeitando capacidade.
        
        Args:
            delivery_ids: Lista de IDs de entregas
            num_routes: Número de rotas
            vehicles: Lista de veículos
        
        Returns:
            List[List[str]]: Rotas redistribuídas
        """
        routes = [[] for _ in range(min(num_routes, len(vehicles)))]
        current_route = 0
        current_weight = 0.0
        
        for d_id in delivery_ids:
            if d_id not in self._delivery_dict:
                continue
            
            delivery = self._delivery_dict[d_id]
            
            # Tentar adicionar à rota atual
            if (
                current_route < len(vehicles)
                and current_weight + delivery.weight
                <= vehicles[current_route].max_capacity
            ):
                routes[current_route].append(d_id)
                current_weight += delivery.weight
            else:
                # Próxima rota
                current_route += 1
                if current_route >= len(routes):
                    # Criar nova rota se necessário
                    if current_route < len(vehicles):
                        routes.append([])
                    else:
                        # Forçar na última rota (violação será penalizada)
                        current_route = len(routes) - 1
                
                routes[current_route].append(d_id)
                current_weight = delivery.weight
        
        # Remover rotas vazias
        routes = [r for r in routes if r]
        return routes
    
    def _mutate(
        self, offspring: List, config: OptimizationConfig
    ) -> List:
        """Operador de mutação."""
        for ind in offspring:
            if random.random() < config.mutation_rate:
                self._route_mutate(ind)
                del ind.fitness.values
        
        return offspring
    
    def _route_mutate(self, individual: List[List[str]]) -> None:
        """
        Mutação específica para rotas VRP.
        
        Operadores de mutação:
        - Swap: Troca duas entregas
        - Move: Move entrega de uma rota para outra
        - Reverse: Inverte ordem de uma rota
        """
        if not individual:
            return
        
        mutation_type = random.choice(["swap", "move", "reverse"])
        
        if mutation_type == "swap":
            # Trocar duas entregas aleatórias
            all_deliveries = [
                (r_idx, d_idx, d_id)
                for r_idx, route in enumerate(individual)
                for d_idx, d_id in enumerate(route)
            ]
            if len(all_deliveries) >= 2:
                (r1, d1_idx, d1), (r2, d2_idx, d2) = random.sample(
                    all_deliveries, 2
                )
                individual[r1][d1_idx] = d2
                individual[r2][d2_idx] = d1
        
        elif mutation_type == "move":
            # Mover entrega de uma rota para outra
            all_deliveries = [
                (r_idx, d_idx, d_id)
                for r_idx, route in enumerate(individual)
                for d_idx, d_id in enumerate(route)
            ]
            if all_deliveries:
                r1, d1_idx, d1 = random.choice(all_deliveries)
                r2 = random.randint(0, len(individual) - 1)
                
                individual[r1].pop(d1_idx)
                if not individual[r1]:
                    individual.pop(r1)
                
                if r2 < len(individual):
                    insert_pos = random.randint(0, len(individual[r2]))
                    individual[r2].insert(insert_pos, d1)
        
        elif mutation_type == "reverse":
            # Inverter ordem de uma rota aleatória
            if individual:
                route_idx = random.randint(0, len(individual) - 1)
                individual[route_idx].reverse()
    
    def _replace_with_elitism(
        self,
        population: List,
        offspring: List,
        config: OptimizationConfig,
    ) -> List:
        """
        Substitui população mantendo elite.
        
        Args:
            population: População atual
            offspring: Novos indivíduos
            config: Configuração
        
        Returns:
            List: Nova população
        """
        # Combinar população e offspring
        combined = population + offspring
        
        # Selecionar melhores
        new_population = tools.selBest(combined, config.population_size)
        
        return new_population
    
    def _individual_to_route_solution(
        self,
        individual: List[List[str]],
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
        depot_location: Tuple[float, float],
    ) -> RouteSolution:
        """
        Converte indivíduo do DEAP em RouteSolution.
        
        Args:
            individual: Indivíduo do DEAP
            deliveries: Lista de entregas
            vehicles: Lista de veículos
            depot_location: Localização do depósito
        
        Returns:
            RouteSolution: Solução de rota
        """
        return self._routes_list_to_solution(individual)
