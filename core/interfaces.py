"""
Interfaces Abstratas (ABC) para o sistema de otimização de rotas.

Este módulo define os contratos que devem ser implementados por:
- Otimizadores (Algoritmos Genéticos, etc.)
- Geradores de Relatórios (LLM-based)
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


@dataclass
class OptimizationConfig:
    """Configuração para o processo de otimização."""
    
    population_size: int = 100
    generations: int = 200
    crossover_rate: float = 0.8
    mutation_rate: float = 0.2
    elite_size: int = 10
    max_vehicles: int = 5
    max_iterations_without_improvement: Optional[int] = None


@dataclass
class VehicleConstraints:
    """Restrições de um veículo."""
    
    max_capacity: float  # Capacidade máxima de carga (kg)
    max_range: float  # Autonomia máxima (km)
    fuel_cost_per_km: float  # Custo de combustível por km
    driver_cost_per_hour: float  # Custo do motorista por hora


@dataclass
class Delivery:
    """Representa uma entrega a ser realizada."""
    
    id: str
    location: tuple[float, float]  # (latitude, longitude)
    priority: int  # 1 = crítico (medicamentos), 2 = normal (insumos)
    weight: float  # Peso da entrega (kg)
    time_window_start: Optional[float] = None  # Janela de tempo início (horas)
    time_window_end: Optional[float] = None  # Janela de tempo fim (horas)
    estimated_service_time: float = 0.5  # Tempo de serviço em horas


@dataclass
class RouteSolution:
    """Solução de rota otimizada."""
    
    routes: List[List[str]]  # Lista de rotas, cada rota é lista de IDs de entregas
    total_distance: float  # Distância total percorrida (km)
    total_cost: float  # Custo total
    fitness_score: float  # Score de fitness
    violations: Dict[str, float]  # Violações de restrições
    metadata: Dict[str, Any]  # Metadados adicionais


@dataclass
class OptimizationResult:
    """Resultado completo do processo de otimização."""
    
    solution: RouteSolution
    execution_time: float  # Tempo de execução em segundos
    generations_evolved: int
    best_fitness_history: List[float]
    config: OptimizationConfig
    statistics: Dict[str, Any]


class BaseOptimizer(ABC):
    """
    Interface abstrata para otimizadores de rotas.
    
    Define o contrato que todos os otimizadores devem seguir,
    permitindo trocar algoritmos sem modificar o código cliente.
    """
    
    @abstractmethod
    def optimize(
        self,
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
        config: OptimizationConfig,
        depot_location: tuple[float, float],
    ) -> OptimizationResult:
        """
        Otimiza as rotas para as entregas fornecidas.
        
        Args:
            deliveries: Lista de entregas a serem realizadas
            vehicles: Lista de veículos disponíveis com suas restrições
            config: Configuração do processo de otimização
            depot_location: Localização do depósito (latitude, longitude)
        
        Returns:
            OptimizationResult: Resultado completo da otimização
        
        Raises:
            OptimizationError: Se houver erro no processo de otimização
        """
        pass
    
    @abstractmethod
    def validate_solution(
        self,
        solution: RouteSolution,
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
    ) -> bool:
        """
        Valida se uma solução atende todas as restrições.
        
        Args:
            solution: Solução a ser validada
            deliveries: Lista de entregas
            vehicles: Lista de veículos
        
        Returns:
            bool: True se a solução é válida, False caso contrário
        """
        pass


class ReportType(Enum):
    """Tipos de relatório disponíveis."""
    
    DRIVER_INSTRUCTIONS = "driver_instructions"
    DAILY_SUMMARY = "daily_summary"
    WEEKLY_ANALYSIS = "weekly_analysis"
    MANAGERIAL_REPORT = "managerial_report"


@dataclass
class ReportRequest:
    """
    Request para geração de relatório.
    
    Usa ReportType enum para garantir tipos explícitos e evitar strings mágicas.
    """
    
    optimization_result: OptimizationResult
    report_type: ReportType  # Tipo explícito via enum
    language: str = "pt-BR"
    additional_context: Optional[Dict[str, Any]] = None


@dataclass
class ReportResult:
    """Resultado da geração de relatório."""
    
    content: str  # Conteúdo do relatório gerado
    report_type: str
    metadata: Dict[str, Any]  # Metadados (tokens usados, custo, etc.)


class BaseReporter(ABC):
    """
    Interface abstrata para geradores de relatórios baseados em LLM.
    
    Define o contrato que todos os geradores de relatório devem seguir,
    permitindo trocar modelos/provedores de LLM sem modificar o código cliente.
    """
    
    @abstractmethod
    def generate_report(self, request: ReportRequest) -> ReportResult:
        """
        Gera um relatório baseado no resultado da otimização.
        
        Args:
            request: Request contendo o resultado da otimização e tipo de relatório
        
        Returns:
            ReportResult: Relatório gerado
        
        Raises:
            ReportGenerationError: Se houver erro na geração do relatório
        """
        pass
    
    @abstractmethod
    def generate_driver_instructions(
        self,
        optimization_result: OptimizationResult,
        language: str = "pt-BR",
    ) -> ReportResult:
        """
        Gera instruções passo-a-passo para o motorista.
        
        Args:
            optimization_result: Resultado da otimização
            language: Idioma do relatório
        
        Returns:
            ReportResult: Instruções para o motorista
        """
        pass
    
    @abstractmethod
    def generate_managerial_report(
        self,
        optimization_result: OptimizationResult,
        language: str = "pt-BR",
        additional_context: Optional[Dict[str, Any]] = None,
    ) -> ReportResult:
        """
        Gera relatório gerencial de economia e eficiência.
        
        Args:
            optimization_result: Resultado da otimização
            language: Idioma do relatório
            additional_context: Contexto adicional (ex: custos anteriores)
        
        Returns:
            ReportResult: Relatório gerencial
        """
        pass
    
    @abstractmethod
    def generate_daily_summary(
        self,
        optimization_result: OptimizationResult,
        language: str = "pt-BR",
    ) -> ReportResult:
        """
        Gera resumo diário de operações.
        
        Args:
            optimization_result: Resultado da otimização
            language: Idioma do relatório
        
        Returns:
            ReportResult: Resumo diário
        """
        pass
    
    @abstractmethod
    def generate_weekly_analysis(
        self,
        optimization_results: List[OptimizationResult],
        language: str = "pt-BR",
    ) -> ReportResult:
        """
        Gera análise semanal de performance.
        
        Args:
            optimization_results: Lista de resultados da semana
            language: Idioma do relatório
        
        Returns:
            ReportResult: Análise semanal
        """
        pass

