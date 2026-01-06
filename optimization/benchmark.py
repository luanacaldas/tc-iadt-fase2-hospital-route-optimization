"""
Módulo de benchmark e comparação de algoritmos de otimização.

Compara desempenho de diferentes algoritmos (Genetic Algorithm, Greedy, Simulated Annealing).
"""

import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

from hospital_routes.core.interfaces import (
    Delivery,
    VehicleConstraints,
    OptimizationConfig,
    OptimizationResult,
)
from hospital_routes.optimization.genetic_algorithm import GeneticAlgorithmOptimizer
from hospital_routes.optimization.greedy_optimizer import GreedyOptimizer
from hospital_routes.optimization.simulated_annealing_optimizer import SimulatedAnnealingOptimizer


@dataclass
class AlgorithmResult:
    """Resultado de um algoritmo específico."""
    
    algorithm_name: str
    result: OptimizationResult
    execution_time: float
    fitness_score: float
    total_distance: float
    total_cost: float
    num_vehicles: int
    violations: Dict[str, float]
    is_valid: bool


@dataclass
class BenchmarkResult:
    """Resultado completo do benchmark."""
    
    algorithm_results: List[AlgorithmResult] = field(default_factory=list)
    best_algorithm: Optional[str] = None
    fastest_algorithm: Optional[str] = None
    most_efficient_algorithm: Optional[str] = None
    summary: Dict[str, Any] = field(default_factory=dict)


class AlgorithmBenchmark:
    """
    Classe para comparar desempenho de diferentes algoritmos de otimização.
    
    Executa múltiplos algoritmos no mesmo problema e compara resultados.
    """
    
    def __init__(self):
        """Inicializa o benchmark."""
        self.algorithms = {
            "genetic_algorithm": GeneticAlgorithmOptimizer(),
            "greedy": GreedyOptimizer(),
            "simulated_annealing": SimulatedAnnealingOptimizer(
                initial_temperature=1000.0,
                cooling_rate=0.95,
            ),
        }
    
    def run_benchmark(
        self,
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
        config: OptimizationConfig,
        depot_location: tuple[float, float],
        algorithms: Optional[List[str]] = None,
    ) -> BenchmarkResult:
        """
        Executa benchmark comparando diferentes algoritmos.
        
        Args:
            deliveries: Lista de entregas
            vehicles: Lista de veículos
            config: Configuração (usada para GA e SA)
            depot_location: Localização do depósito
            algorithms: Lista de algoritmos para testar (None = todos)
        
        Returns:
            BenchmarkResult: Resultado completo do benchmark
        """
        if algorithms is None:
            algorithms = list(self.algorithms.keys())
        
        algorithm_results = []
        
        print(f"🔬 Executando benchmark com {len(algorithms)} algoritmo(s)...")
        print()
        
        for algo_name in algorithms:
            if algo_name not in self.algorithms:
                print(f"⚠️  Algoritmo '{algo_name}' não encontrado, pulando...")
                continue
            
            print(f"📊 Executando: {algo_name}")
            optimizer = self.algorithms[algo_name]
            
            try:
                start_time = time.time()
                result = optimizer.optimize(
                    deliveries, vehicles, config, depot_location
                )
                execution_time = time.time() - start_time
                
                # Validar solução
                is_valid = optimizer.validate_solution(
                    result.solution, deliveries, vehicles
                )
                
                algo_result = AlgorithmResult(
                    algorithm_name=algo_name,
                    result=result,
                    execution_time=execution_time,
                    fitness_score=result.solution.fitness_score,
                    total_distance=result.solution.total_distance,
                    total_cost=result.solution.total_cost,
                    num_vehicles=len(result.solution.routes),
                    violations=result.solution.violations,
                    is_valid=is_valid,
                )
                
                algorithm_results.append(algo_result)
                
                print(f"   ✅ Concluído em {execution_time:.2f}s")
                print(f"      Fitness: {result.solution.fitness_score:.2f}")
                print(f"      Distância: {result.solution.total_distance:.2f} km")
                print(f"      Válido: {'Sim' if is_valid else 'Não'}")
                print()
            
            except Exception as e:
                print(f"   ❌ Erro: {str(e)}")
                print()
        
        # Análise comparativa
        benchmark_result = self._analyze_results(algorithm_results)
        
        return benchmark_result
    
    def _analyze_results(
        self, algorithm_results: List[AlgorithmResult]
    ) -> BenchmarkResult:
        """
        Analisa resultados e identifica melhores algoritmos.
        
        Args:
            algorithm_results: Lista de resultados
        
        Returns:
            BenchmarkResult: Resultado com análise
        """
        if not algorithm_results:
            return BenchmarkResult()
        
        # Melhor fitness (menor é melhor)
        best_algo = min(
            algorithm_results, key=lambda x: x.fitness_score
        ).algorithm_name
        
        # Mais rápido
        fastest_algo = min(
            algorithm_results, key=lambda x: x.execution_time
        ).algorithm_name
        
        # Mais eficiente (fitness / tempo)
        most_efficient_algo = min(
            algorithm_results,
            key=lambda x: x.fitness_score / max(x.execution_time, 0.001),
        ).algorithm_name
        
        # Resumo estatístico
        summary = {
            "total_algorithms": len(algorithm_results),
            "best_fitness": min(r.fitness_score for r in algorithm_results),
            "worst_fitness": max(r.fitness_score for r in algorithm_results),
            "avg_fitness": sum(r.fitness_score for r in algorithm_results) / len(algorithm_results),
            "fastest_time": min(r.execution_time for r in algorithm_results),
            "slowest_time": max(r.execution_time for r in algorithm_results),
            "avg_time": sum(r.execution_time for r in algorithm_results) / len(algorithm_results),
        }
        
        return BenchmarkResult(
            algorithm_results=algorithm_results,
            best_algorithm=best_algo,
            fastest_algorithm=fastest_algo,
            most_efficient_algorithm=most_efficient_algo,
            summary=summary,
        )
    
    def print_comparison(self, benchmark_result: BenchmarkResult) -> None:
        """
        Imprime tabela comparativa dos resultados.
        
        Args:
            benchmark_result: Resultado do benchmark
        """
        print("=" * 100)
        print("COMPARATIVO DE DESEMPENHO")
        print("=" * 100)
        print()
        
        # Cabeçalho
        print(f"{'Algoritmo':<25} {'Fitness':<12} {'Distância':<12} {'Custo':<12} {'Tempo':<12} {'Válido':<8}")
        print("-" * 100)
        
        # Dados
        for algo_result in benchmark_result.algorithm_results:
            print(
                f"{algo_result.algorithm_name:<25} "
                f"{algo_result.fitness_score:<12.2f} "
                f"{algo_result.total_distance:<12.2f} "
                f"{algo_result.total_cost:<12.2f} "
                f"{algo_result.execution_time:<12.2f} "
                f"{'Sim' if algo_result.is_valid else 'Não':<8}"
            )
        
        print()
        print("=" * 100)
        print("ANÁLISE")
        print("=" * 100)
        print(f"🏆 Melhor Fitness: {benchmark_result.best_algorithm}")
        print(f"⚡ Mais Rápido: {benchmark_result.fastest_algorithm}")
        print(f"💡 Mais Eficiente: {benchmark_result.most_efficient_algorithm}")
        print()
        
        # Estatísticas
        if benchmark_result.summary:
            print("📊 Estatísticas:")
            print(f"   Fitness médio: {benchmark_result.summary['avg_fitness']:.2f}")
            print(f"   Tempo médio: {benchmark_result.summary['avg_time']:.2f}s")
            print(f"   Melhor fitness: {benchmark_result.summary['best_fitness']:.2f}")
            print(f"   Pior fitness: {benchmark_result.summary['worst_fitness']:.2f}")
        
        print()
    
    def export_comparison(
        self, benchmark_result: BenchmarkResult, output_file: str = "benchmark_results.json"
    ) -> None:
        """
        Exporta resultados do benchmark para JSON.
        
        Args:
            benchmark_result: Resultado do benchmark
            output_file: Arquivo de saída
        """
        import json
        
        data = {
            "best_algorithm": benchmark_result.best_algorithm,
            "fastest_algorithm": benchmark_result.fastest_algorithm,
            "most_efficient_algorithm": benchmark_result.most_efficient_algorithm,
            "summary": benchmark_result.summary,
            "algorithm_results": [
                {
                    "algorithm_name": r.algorithm_name,
                    "fitness_score": r.fitness_score,
                    "total_distance": r.total_distance,
                    "total_cost": r.total_cost,
                    "execution_time": r.execution_time,
                    "num_vehicles": r.num_vehicles,
                    "violations": r.violations,
                    "is_valid": r.is_valid,
                }
                for r in benchmark_result.algorithm_results
            ],
        }
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Resultados exportados para: {output_file}")

