"""
Configurações do sistema, incluindo pesos da função de fitness.

Este módulo centraliza todas as configurações, permitindo ajuste fino
dos parâmetros do algoritmo genético e da função de fitness.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class FitnessWeights:
    """
    Pesos da função de fitness multi-objetivo.
    
    A função de fitness é calculada como:
    
    fitness = α * total_distance
           + β * capacity_violation
           + γ * autonomy_violation
           + δ * priority_delay
           + ε * vehicle_count
    
    Onde:
    - α (distance_weight): Peso da distância total
    - β (capacity_penalty): Penalidade por violação de capacidade
    - γ (autonomy_penalty): Penalidade por violação de autonomia
    - δ (priority_penalty): Penalidade por atraso em entregas prioritárias
    - ε (vehicle_penalty): Penalidade por uso de veículos adicionais
    """
    
    distance_weight: float = 1.0  # α
    capacity_penalty: float = 1000.0  # β - alto para desencorajar violações
    autonomy_penalty: float = 1000.0  # γ - alto para desencorajar violações
    priority_penalty: float = 500.0  # δ - penaliza atraso em entregas críticas
    vehicle_penalty: float = 100.0  # ε - penaliza uso de mais veículos
    
    def __post_init__(self):
        """Valida que todos os pesos são não-negativos."""
        if any(w < 0 for w in [
            self.distance_weight,
            self.capacity_penalty,
            self.autonomy_penalty,
            self.priority_penalty,
            self.vehicle_penalty,
        ]):
            raise ValueError("Todos os pesos devem ser não-negativos")


@dataclass
class GeneticAlgorithmConfig:
    """
    Configuração do algoritmo genético.
    
    Parâmetros que controlam o comportamento do GA:
    - Tamanho da população
    - Número de gerações
    - Taxas de crossover e mutação
    - Estratégias de inicialização e seleção
    """
    
    population_size: int = 100
    generations: int = 200
    crossover_rate: float = 0.8
    mutation_rate: float = 0.2
    elite_size: int = 10
    max_vehicles: int = 5
    max_iterations_without_improvement: Optional[int] = 50
    
    # Estratégia de inicialização
    use_heuristic_initialization: bool = True  # Nearest neighbor para melhorar população inicial
    
    # Early stopping
    early_stopping_patience: Optional[int] = 30  # Gerações sem melhoria antes de parar
    
    def __post_init__(self):
        """Valida configurações."""
        if self.population_size < 2:
            raise ValueError("population_size deve ser >= 2")
        if self.generations < 1:
            raise ValueError("generations deve ser >= 1")
        if not 0 <= self.crossover_rate <= 1:
            raise ValueError("crossover_rate deve estar entre 0 e 1")
        if not 0 <= self.mutation_rate <= 1:
            raise ValueError("mutation_rate deve estar entre 0 e 1")
        if self.elite_size >= self.population_size:
            raise ValueError("elite_size deve ser menor que population_size")


@dataclass
class SystemConfig:
    """
    Configuração geral do sistema.
    
    Centraliza todas as configurações em um único lugar.
    """
    
    fitness_weights: FitnessWeights
    ga_config: GeneticAlgorithmConfig
    
    # Configurações de LLM
    llm_provider: str = "openai"  # "openai" ou "ollama"
    llm_model: str = "gpt-4"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 2000
    
    # Configurações de validação
    validate_llm_output: bool = True  # Validar saída do LLM (evitar alucinações)
    strict_mode: bool = False  # Modo estrito (rejeita soluções com violações)
    
    @classmethod
    def default(cls) -> "SystemConfig":
        """Retorna configuração padrão do sistema."""
        return cls(
            fitness_weights=FitnessWeights(),
            ga_config=GeneticAlgorithmConfig(),
        )

