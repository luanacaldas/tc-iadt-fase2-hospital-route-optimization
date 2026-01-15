"""
Exemplo de uso do OllamaReporter para gerar relatórios usando Ollama local.

Pré-requisitos:
1. Instalar Ollama: https://ollama.ai/
2. Baixar um modelo: ollama pull llama3.2 (ou outro modelo)
3. Instalar dependências Python:
   - pip install ollama
   OU
   - pip install langchain-ollama

Certifique-se de que o Ollama está rodando antes de executar este script.
"""

import sys
from pathlib import Path

# Adicionar raiz do projeto ao PYTHONPATH
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from hospital_routes.llm.ollama_reporter import OllamaReporter
from hospital_routes.core.interfaces import (
    OptimizationResult,
    RouteSolution,
    OptimizationConfig,
    ReportRequest,
    ReportType,
)
from seed_real_data import generate_deliveries, get_depot_location


def create_sample_optimization_result():
    """Cria um resultado de otimização de exemplo."""
    # Criar solução de exemplo
    solution = RouteSolution(
        routes=[
            ["HOSP_001", "HOSP_002", "HOSP_003"],
            ["HOSP_004", "HOSP_005"],
        ],
        total_distance=45.5,
        total_cost=125.30,
        fitness_score=850.25,
        violations={"capacity": 0.0, "autonomy": 0.0},
        metadata={},
    )
    
    # Adicionar entregas aos metadados
    deliveries = generate_deliveries()
    solution.metadata["deliveries"] = deliveries
    
    # Criar resultado
    result = OptimizationResult(
        solution=solution,
        execution_time=2.5,
        generations_evolved=50,
        best_fitness_history=[1000, 950, 900, 850],
        config=OptimizationConfig(
            population_size=30,
            generations=50,
            crossover_rate=0.8,
            mutation_rate=0.2,
        ),
        statistics={},
    )
    
    return result


def main():
    """Função principal de teste."""
    print("🤖 Teste do OllamaReporter")
    print("=" * 60)
    print()
    
    # Verificar se Ollama está disponível
    try:
        reporter = OllamaReporter(
            model_name="llama3.2",  # Altere para o modelo que você tem instalado
            temperature=0.7,
            num_predict=2000,
        )
        print(f"✅ OllamaReporter inicializado com sucesso!")
        print(f"   Modelo: {reporter.model_name}")
        print(f"   Usando API direta: {reporter.use_direct_api}")
        print()
    except ImportError as e:
        print(f"❌ Erro: {e}")
        print()
        print("💡 Para instalar as dependências:")
        print("   pip install ollama")
        print("   OU")
        print("   pip install langchain-ollama")
        return 1
    except Exception as e:
        print(f"❌ Erro ao inicializar OllamaReporter: {e}")
        print()
        print("💡 Certifique-se de que:")
        print("   1. Ollama está instalado e rodando")
        print("   2. Um modelo está instalado (ex: ollama pull llama3.2)")
        print("   3. O modelo especificado existe localmente")
        return 1
    
    # Criar resultado de otimização de exemplo
    print("📊 Criando resultado de otimização de exemplo...")
    optimization_result = create_sample_optimization_result()
    print(f"   ✅ Resultado criado com {len(optimization_result.solution.routes)} rotas")
    print()
    
    # Gerar relatório
    print("📝 Gerando instruções para o motorista...")
    print("   (Isso pode levar alguns segundos)")
    print()
    
    try:
        request = ReportRequest(
            optimization_result=optimization_result,
            report_type=ReportType.DRIVER_INSTRUCTIONS,
            language="pt-BR",
        )
        
        report = reporter.generate_report(request)
        
        print("=" * 60)
        print("✅ RELATÓRIO GERADO COM SUCESSO!")
        print("=" * 60)
        print()
        print("📄 Conteúdo do relatório:")
        print("-" * 60)
        print(report.content)
        print("-" * 60)
        print()
        print("📊 Metadados:")
        for key, value in report.metadata.items():
            print(f"   {key}: {value}")
        print()
        
        return 0
    
    except Exception as e:
        print(f"❌ Erro ao gerar relatório: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

