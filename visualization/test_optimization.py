"""
Teste de otimização de rotas hospitalares. 

Este script valida o funcionamento do sistema de otimização
usando dados de exemplo de entregas em São Paulo.
"""

import sys
from pathlib import Path

# Adicionar raiz do projeto ao PYTHONPATH
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))


def main():
    """Função principal do teste."""
    print("🚀 Iniciando teste de otimização de rotas\n")
    print("=" * 60)
    
    try:
        # Validar imports
        print("📦 Importando módulos...")
        from hospital_routes.core.interfaces import (
            Delivery,
            VehicleConstraints,
            OptimizationConfig,
        )
        from hospital_routes.optimization.genetic_algorithm import (
            GeneticAlgorithmOptimizer,
        )
        print("✅ Módulos importados com sucesso!\n")
        
    except ImportError as e:
        print(f"❌ Erro ao importar módulos: {e}")
        print("\nVerifique se o projeto está instalado corretamente.")
        return 1
    
    # Configuração de dados de teste
    print("📍 Configurando dados de teste...")
    
    deliveries = [
        Delivery(id="D001", location=(-23.5489, -46.6388), weight=10.0, priority=1),
        Delivery(id="D002", location=(-23.5578, -46.6593), weight=5.0, priority=2),
        Delivery(id="D003", location=(-23.5629, -46.6544), weight=15.0, priority=1),
        Delivery(id="D004", location=(-23.5505, -46.6125), weight=8.0, priority=2),
        Delivery(id="D005", location=(-23.5431, -46.6367), weight=12.0, priority=1),
    ]
    
    vehicles = [
        VehicleConstraints(
            max_capacity=50.0,
            max_range=100.0,
            fuel_cost_per_km=2.5,
            driver_cost_per_hour=20.0,
        ),
        VehicleConstraints(
            max_capacity=50.0,
            max_range=100.0,
            fuel_cost_per_km=2.5,
            driver_cost_per_hour=20.0,
        ),
    ]
    
    config = OptimizationConfig(
        population_size=30,
        generations=50,
        crossover_rate=0.8,
        mutation_rate=0.2,
    )
    
    depot_location = (-23.5505, -46.6333)  # Hospital Central - São Paulo
    
    print(f"   📦 Entregas:  {len(deliveries)}")
    print(f"   🚚 Veículos: {len(vehicles)}")
    print(f"   🧬 Gerações: {config.generations}")
    print(f"   👥 População: {config.population_size}")
    print("=" * 60)
    print()
    
    # Executar otimização
    try:
        print("⏳ Executando algoritmo genético...")
        print("   (Isso pode levar alguns segundos)\n")
        
        optimizer = GeneticAlgorithmOptimizer()
        result = optimizer.optimize(
            deliveries=deliveries,
            vehicles=vehicles,
            config=config,
            depot_location=depot_location,
        )
        
    except Exception as e:
        print(f"❌ Erro durante otimização: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Exibir resultados
    print("=" * 60)
    print("✅ OTIMIZAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 60)
    print()
    print("📊 RESULTADOS:")
    print(f"   📏 Distância total: {result.solution.total_distance:.2f} km")
    print(f"   💰 Custo total: R$ {result.solution.total_cost:.2f}")
    print(f"   ⏱️  Tempo de execução: {result.execution_time:.2f}s")
    print(f"   🧬 Gerações: {result.generations_evolved}")
    print(f"   🎯 Fitness: {result.solution.fitness_score:.2f}")
    print(f"   🚚 Veículos usados: {len(result.solution.routes)}")
    print()
    
    # Mostrar rotas detalhadas
    print("=" * 60)
    print("📍 ROTAS OTIMIZADAS")
    print("=" * 60)
    
    for vehicle_idx, route in enumerate(result.solution.routes, start=1):
        if not route:
            continue
            
        print(f"\n🚚 Veículo {vehicle_idx}:")
        print(f"   Entregas: {' → '.join(route)}")
        print(f"   Total de paradas: {len(route)}")
        
        # Calcular peso total desta rota
        total_weight = sum(
            d.weight for d in deliveries if d.id in route
        )
        print(f"   Peso total: {total_weight:.1f} kg")
        
        # Identificar entregas críticas
        critical = [d.id for d in deliveries if d.id in route and d.priority == 1]
        if critical:
            print(f"   ⚠️  Entregas críticas: {', '.join(critical)}")
    
    print()
    print("=" * 60)
    print("🎉 Teste concluído com sucesso!")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)