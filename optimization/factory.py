"""
Factory para criar instâncias de otimizadores.

Permite criar diferentes tipos de otimizadores baseado em configuração,
seguindo o padrão Factory.
"""

from typing import Optional
from hospital_routes.core.interfaces import BaseOptimizer
from hospital_routes.core.exceptions import InvalidConfigurationError
from hospital_routes.optimization.genetic_algorithm import GeneticAlgorithmOptimizer
from hospital_routes.optimization.greedy_optimizer import GreedyOptimizer
from hospital_routes.optimization.simulated_annealing_optimizer import SimulatedAnnealingOptimizer
from hospital_routes.optimization.initialization_strategy import (
    InitialPopulationStrategy,
    RandomInitializationStrategy,
    NearestNeighborInitializationStrategy,
    PriorityFirstInitializationStrategy,
)
from hospital_routes.utils.config import FitnessWeights


class OptimizerFactory:
    """
    Factory para criar otimizadores.
    
    Exemplo:
        factory = OptimizerFactory()
        optimizer = factory.create("genetic_algorithm", config)
    """
    
    @staticmethod
    def create(
        optimizer_type: str,
        config: Optional[dict] = None,
    ) -> BaseOptimizer:
        """
        Cria uma instância de otimizador.
        
        Args:
            optimizer_type: Tipo de otimizador ("genetic_algorithm", etc.)
            config: Configuração opcional para o otimizador
                - fitness_weights: FitnessWeights (opcional)
                - initialization_strategy: str ("random", "nearest_neighbor", "priority_first")
        
        Returns:
            BaseOptimizer: Instância do otimizador
        
        Raises:
            InvalidConfigurationError: Se o tipo de otimizador não for suportado
        """
        config = config or {}
        
        # Fitness weights (compartilhado entre algoritmos)
        fitness_weights = config.get("fitness_weights")
        if fitness_weights is None:
            fitness_weights = FitnessWeights()
        
        if optimizer_type == "genetic_algorithm":
            # Initialization strategy
            strategy_name = config.get("initialization_strategy", "random")
            if strategy_name == "nearest_neighbor":
                initialization_strategy = NearestNeighborInitializationStrategy()
            elif strategy_name == "priority_first":
                initialization_strategy = PriorityFirstInitializationStrategy()
            else:
                initialization_strategy = RandomInitializationStrategy()
            
            return GeneticAlgorithmOptimizer(
                fitness_weights=fitness_weights,
                initialization_strategy=initialization_strategy,
            )
        elif optimizer_type == "greedy":
            return GreedyOptimizer(fitness_weights=fitness_weights)
        elif optimizer_type == "simulated_annealing":
            sa_config = config.get("sa_config", {})
            return SimulatedAnnealingOptimizer(
                fitness_weights=fitness_weights,
                initial_temperature=sa_config.get("initial_temperature", 1000.0),
                cooling_rate=sa_config.get("cooling_rate", 0.95),
                min_temperature=sa_config.get("min_temperature", 0.1),
            )
        else:
            raise InvalidConfigurationError(
                f"Tipo de otimizador não suportado: {optimizer_type}. "
                f"Opções: genetic_algorithm, greedy, simulated_annealing"
            )

