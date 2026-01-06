"""
Interface de linha de comando (CLI) do sistema.

Este módulo fornece uma CLI para executar otimizações de rotas.
"""

import argparse
import json
from pathlib import Path
from typing import Optional


def main() -> None:
    """
    Função principal da CLI.
    
    Exemplo de uso:
        python -m hospital_routes.cli --input deliveries.json
    """
    parser = argparse.ArgumentParser(
        description="Sistema de Otimização de Rotas Hospitalares"
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
    
    args = parser.parse_args()
    
    # TODO: Implementar lógica completa da CLI
    print(f"Processando arquivo: {args.input}")
    print(f"Saída: {args.output}")
    
    if args.generate_report:
        print(f"Gerando relatório: {args.report_type}")


if __name__ == "__main__":
    main()

