"""
Interface de linha de comando (CLI) do sistema.

Este módulo fornece uma CLI completa para executar otimizações de rotas.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any

from hospital_routes.core.interfaces import (
    Delivery,
    VehicleConstraints,
    OptimizationConfig,
    ReportType,
)
from hospital_routes.optimization.genetic_algorithm import GeneticAlgorithmOptimizer
from hospital_routes.optimization.factory import OptimizerFactory
from hospital_routes.visualization.map_generator import MapGenerator
from hospital_routes.utils.logger import setup_logger, get_logger


def load_input_file(input_path: str) -> Dict[str, Any]:
    """
    Carrega arquivo JSON de entrada.
    
    Args:
        input_path: Caminho do arquivo
    
    Returns:
        dict: Dados carregados
    
    Raises:
        FileNotFoundError: Se arquivo não existir
        json.JSONDecodeError: Se JSON inválido
    """
    input_file = Path(input_path)
    if not input_file.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {input_path}")
    
    with open(input_file, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_deliveries(data: Dict[str, Any]) -> list[Delivery]:
    """Converte dados JSON em lista de Delivery."""
    deliveries = []
    for d in data.get("deliveries", []):
        deliveries.append(
            Delivery(
                id=d["id"],
                location=tuple(d["location"]),
                weight=d["weight"],
                priority=d.get("priority", 2),
                time_window_start=d.get("time_window_start"),
                time_window_end=d.get("time_window_end"),
                estimated_service_time=d.get("estimated_service_time", 0.5),
            )
        )
    return deliveries


def parse_vehicles(data: Dict[str, Any]) -> list[VehicleConstraints]:
    """Converte dados JSON em lista de VehicleConstraints."""
    vehicles = []
    for v in data.get("vehicles", []):
        vehicles.append(
            VehicleConstraints(
                max_capacity=v["max_capacity"],
                max_range=v["max_range"],
                fuel_cost_per_km=v["fuel_cost_per_km"],
                driver_cost_per_hour=v["driver_cost_per_hour"],
            )
        )
    return vehicles


def parse_config(data: Dict[str, Any]) -> OptimizationConfig:
    """Converte dados JSON em OptimizationConfig."""
    config_data = data.get("config", {})
    return OptimizationConfig(
        population_size=config_data.get("population_size", 30),
        generations=config_data.get("generations", 50),
        crossover_rate=config_data.get("crossover_rate", 0.8),
        mutation_rate=config_data.get("mutation_rate", 0.2),
        max_iterations_without_improvement=config_data.get(
            "max_iterations_without_improvement", None
        ),
    )


def save_result(result: Any, output_path: str, format: str = "json") -> None:
    """
    Salva resultado em arquivo.
    
    Args:
        result: Resultado da otimização
        output_path: Caminho do arquivo de saída
        format: Formato de saída (json, csv)
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    if format == "json":
        # Converter para dict serializável
        result_dict = {
            "solution": {
                "routes": result.solution.routes,
                "total_distance": result.solution.total_distance,
                "total_cost": result.solution.total_cost,
                "fitness_score": result.solution.fitness_score,
                "violations": result.solution.violations,
            },
            "execution_time": result.execution_time,
            "generations_evolved": result.generations_evolved,
            "statistics": result.statistics,
        }
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result_dict, f, indent=2, ensure_ascii=False)
    
    elif format == "csv":
        # TODO: Implementar export CSV
        raise NotImplementedError("Export CSV ainda não implementado")


def main() -> int:
    """
    Função principal da CLI.
    
    Returns:
        int: Código de saída (0 = sucesso, 1 = erro)
    """
    parser = argparse.ArgumentParser(
        description="Sistema de Otimização de Rotas Hospitalares",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Otimização básica
  python -m hospital_routes.cli --input data.json --output routes.json
  
  # Com algoritmo específico
  python -m hospital_routes.cli --input data.json --algorithm greedy
  
  # Com mapa e relatório
  python -m hospital_routes.cli --input data.json --map mapa.html --report
        """,
    )
    
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Arquivo JSON com entregas e veículos",
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="optimized_routes.json",
        help="Arquivo de saída para rotas otimizadas",
    )
    
    parser.add_argument(
        "--algorithm",
        type=str,
        choices=["genetic", "greedy", "simulated_annealing"],
        default="genetic",
        help="Algoritmo de otimização a usar",
    )
    
    parser.add_argument(
        "--map",
        type=str,
        help="Gerar mapa HTML (especifique caminho do arquivo)",
    )
    
    parser.add_argument(
        "--generate-report",
        action="store_true",
        help="Gerar relatório LLM após otimização",
    )
    
    parser.add_argument(
        "--report-type",
        type=str,
        choices=["driver_instructions", "managerial_report", "daily_summary"],
        default="driver_instructions",
        help="Tipo de relatório a gerar",
    )
    
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Nível de logging",
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Modo verboso (equivalente a --log-level DEBUG)",
    )
    
    args = parser.parse_args()
    
    # Configurar logging
    log_level = "DEBUG" if args.verbose else args.log_level
    logger = setup_logger(level=log_level, log_file="cli.log")
    
    try:
        logger.info("Iniciando otimização de rotas")
        logger.debug(f"Argumentos: {args}")
        
        # Carregar dados
        logger.info(f"Carregando arquivo: {args.input}")
        data = load_input_file(args.input)
        
        deliveries = parse_deliveries(data)
        vehicles = parse_vehicles(data)
        config = parse_config(data)
        depot_location = tuple(data.get("depot_location", [-23.5505, -46.6333]))
        
        logger.info(f"Carregados: {len(deliveries)} entregas, {len(vehicles)} veículos")
        
        # Executar otimização
        logger.info(f"Executando algoritmo: {args.algorithm}")
        optimizer = OptimizerFactory.create(args.algorithm)
        
        result = optimizer.optimize(
            deliveries=deliveries,
            vehicles=vehicles,
            config=config,
            depot_location=depot_location,
        )
        
        logger.info(
            f"Otimização concluída: {result.solution.total_distance:.2f} km, "
            f"R$ {result.solution.total_cost:.2f}, {result.execution_time:.2f}s"
        )
        
        # Salvar resultado
        logger.info(f"Salvando resultado em: {args.output}")
        save_result(result, args.output)
        
        # Gerar mapa se solicitado
        if args.map:
            logger.info(f"Gerando mapa: {args.map}")
            result.solution.metadata["deliveries"] = deliveries
            MapGenerator.generate_route_map(
                result, deliveries, depot_location, args.map
            )
            logger.info(f"Mapa salvo em: {args.map}")
        
        # Gerar relatório se solicitado
        if args.generate_report:
            logger.info(f"Gerando relatório: {args.report_type}")
            try:
                from hospital_routes.llm.ollama_reporter import OllamaReporter
                from hospital_routes.core.interfaces import ReportRequest
                
                reporter = OllamaReporter()
                result.solution.metadata["deliveries"] = deliveries
                
                request = ReportRequest(
                    optimization_result=result,
                    report_type=ReportType(args.report_type),
                    language="pt-BR",
                )
                
                report = reporter.generate_report(request)
                
                report_file = Path(args.output).with_suffix(".txt")
                with open(report_file, "w", encoding="utf-8") as f:
                    f.write(report.content)
                
                logger.info(f"Relatório salvo em: {report_file}")
            except ImportError:
                logger.warning("Ollama não disponível. Instale com: pip install ollama")
            except Exception as e:
                logger.error(f"Erro ao gerar relatório: {e}")
        
        logger.info("Processo concluído com sucesso!")
        return 0
    
    except FileNotFoundError as e:
        logger.error(f"Arquivo não encontrado: {e}")
        return 1
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao ler JSON: {e}")
        return 1
    except Exception as e:
        logger.exception(f"Erro inesperado: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

