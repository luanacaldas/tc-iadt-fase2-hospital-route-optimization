"""
Script completo para executar e visualizar o projeto.

Este script:
1. Executa otimização de rotas com dados reais de hospitais de SP
2. Gera um mapa interativo HTML
3. Opcionalmente gera relatório com Ollama
4. Abre o mapa no navegador automaticamente
"""

import sys
import webbrowser
from pathlib import Path

# Adicionar raiz do projeto ao PYTHONPATH
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))


def main():
    """Função principal."""
    print("🏥 Sistema de Otimização de Rotas Hospitalares")
    print("=" * 70)
    print()
    
    try:
        # Importar módulos
        print("📦 Importando módulos...")
        from hospital_routes.optimization.genetic_algorithm import (
            GeneticAlgorithmOptimizer,
        )
        from hospital_routes.visualization.map_generator import MapGenerator
        from hospital_routes.utils.accident_data import (
            AccidentDataProvider,
            create_sample_accident_data,
        )
        from seed_real_data import (
            generate_deliveries,
            generate_vehicles,
            get_optimization_config,
            get_depot_location,
            get_hospital_info,
        )
        print("✅ Módulos importados com sucesso!")
        print()
        
    except ImportError as e:
        print(f"❌ Erro ao importar módulos: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Carregar dados reais
    print("📍 Carregando dados de hospitais reais de São Paulo...")
    deliveries = generate_deliveries()
    vehicles = generate_vehicles()
    config = get_optimization_config()
    depot_location = get_depot_location()
    
    print(f"   📦 Entregas: {len(deliveries)}")
    print(f"   🚚 Veículos: {len(vehicles)}")
    print(f"   🧬 Gerações: {config.generations}")
    print(f"   👥 População: {config.population_size}")
    print()
    
    # Executar otimização
    print("⏳ Executando otimização de rotas...")
    print("   (Isso pode levar alguns segundos)")
    print()
    
    try:
        optimizer = GeneticAlgorithmOptimizer()
        result = optimizer.optimize(
            deliveries=deliveries,
            vehicles=vehicles,
            config=config,
            depot_location=depot_location,
        )
        
        # Adicionar entregas aos metadados (para o mapa e relatório)
        result.solution.metadata["deliveries"] = deliveries
        
    except Exception as e:
        print(f"❌ Erro durante otimização: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Exibir resultados
    print("=" * 70)
    print("✅ OTIMIZAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 70)
    print()
    print("📊 RESULTADOS:")
    print(f"   📏 Distância total: {result.solution.total_distance:.2f} km")
    print(f"   💰 Custo total: R$ {result.solution.total_cost:.2f}")
    print(f"   ⏱️  Tempo de execução: {result.execution_time:.2f}s")
    print(f"   🧬 Gerações: {result.generations_evolved}")
    print(f"   🎯 Fitness: {result.solution.fitness_score:.2f}")
    print(f"   🚚 Veículos usados: {len(result.solution.routes)}")
    print()
    
    # Carregar dados de acidentes (antes de mostrar rotas para poder usar na análise)
    print("=" * 70)
    print("⚠️  Carregando dados de acidentes de trânsito...")
    print("=" * 70)
    print()
    
    accident_provider = None
    try:
        accident_provider = create_sample_accident_data()
        print(f"✅ Dados de acidentes carregados!")
        print(f"   Pontos de risco: {len(accident_provider._accident_cache)}")
        print()
    except Exception as e:
        print(f"⚠️  Aviso: Não foi possível carregar dados de acidentes: {e}")
        print("   Continuando sem dados de acidentes...")
        print()
        accident_provider = None
    
    # Mostrar rotas detalhadas
    print("=" * 70)
    print("📍 ROTAS OTIMIZADAS")
    print("=" * 70)
    
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
        
        # Mostrar nomes dos hospitais
        hospital_names = []
        for delivery_id in route:
            info = get_hospital_info(delivery_id)
            if info:
                hospital_names.append(info["nome"])
        if hospital_names:
            print(f"   🏥 Hospitais: {' → '.join(hospital_names)}")
        
        # Mostrar análise de segurança se disponível
        if accident_provider:
            from hospital_routes.utils.distance import calculate_distance
            route_coords = [depot_location]
            for delivery_id in route:
                delivery = next((d for d in deliveries if d.id == delivery_id), None)
                if delivery:
                    route_coords.append(delivery.location)
            route_coords.append(depot_location)
            
            route_risk = accident_provider.get_route_risk(route_coords)
            risk_emoji = {
                "low": "✅",
                "medium": "⚠️",
                "high": "🔴",
                "critical": "🚨"
            }
            print(f"   {risk_emoji.get(route_risk['overall_risk'], '⚠️')} Segurança: {route_risk['overall_risk'].upper()}")
            print(f"      Acidentes no trajeto: {route_risk['total_accidents']}")
            print(f"      Segmentos de alto risco: {route_risk['high_risk_segments']}")
    
    print()
    
    # Gerar mapa interativo
    print("=" * 70)
    print("🗺️  Gerando mapa interativo com análise de segurança...")
    print("=" * 70)
    print()
    
    try:
        map_output = "route_map.html"
        map_generator = MapGenerator(center_location=depot_location)
        map_obj = map_generator.generate_map(
            optimization_result=result,
            deliveries=deliveries,
            depot_location=depot_location,
            output_path=map_output,
            title="Rotas Otimizadas - Hospitais de São Paulo",
            accident_provider=accident_provider,
            show_accidents=True,
        )
        
        map_path = Path(map_output).absolute()
        print(f"✅ Mapa gerado com sucesso!")
        print(f"   📁 Arquivo: {map_path}")
        print()
        
        # Abrir mapa no navegador
        print("🌐 Abrindo mapa no navegador...")
        webbrowser.open(f"file://{map_path}")
        print("   ✅ Mapa aberto!")
        print()
        
    except Exception as e:
        print(f"❌ Erro ao gerar mapa: {e}")
        import traceback
        traceback.print_exc()
        print()
        print("💡 Certifique-se de que o folium está instalado:")
        print("   pip install folium")
        print()
    
    # Opcional: Gerar relatório com Ollama
    print("=" * 70)
    print("📝 Gerar relatório com Ollama? (opcional)")
    print("=" * 70)
    print()
    
    try:
        from hospital_routes.llm.ollama_reporter import OllamaReporter
        from hospital_routes.core.interfaces import ReportRequest, ReportType
        
        # Tentar inicializar Ollama com auto-detecção
        try:
            from hospital_routes.llm.ollama_helper import get_best_available_model, list_available_models
            
            available_models = list_available_models()
            if available_models:
                print(f"✅ Ollama detectado! Modelos disponíveis: {', '.join(available_models)}")
                best_model = get_best_available_model()
                print(f"   Usando modelo: {best_model}")
            else:
                print("⚠️  Ollama detectado mas nenhum modelo instalado.")
                print("   Execute: ollama pull llama3.2")
                raise Exception("Nenhum modelo disponível")
            
            reporter = OllamaReporter(model_name=None)  # Auto-detect
            print("✅ Gerando relatório...")
            print("   (Isso pode levar alguns segundos)")
            print()
            
            request = ReportRequest(
                optimization_result=result,
                report_type=ReportType.DRIVER_INSTRUCTIONS,
                language="pt-BR",
            )
            
            report = reporter.generate_report(request)
            
            # Salvar relatório
            report_output = "driver_instructions.txt"
            with open(report_output, "w", encoding="utf-8") as f:
                f.write(report.content)
            
            print("=" * 70)
            print("✅ RELATÓRIO GERADO COM SUCESSO!")
            print("=" * 70)
            print()
            print("📄 Conteúdo do relatório:")
            print("-" * 70)
            print(report.content)
            print("-" * 70)
            print()
            print(f"📁 Relatório salvo em: {Path(report_output).absolute()}")
            print()
            
        except ImportError:
            print("ℹ️  Ollama não está disponível.")
            print("   Para usar relatórios, instale: pip install ollama")
            print()
        except Exception as e:
            print(f"⚠️  Erro ao gerar relatório: {e}")
            print("   Continuando sem relatório...")
            print()
    
    except ImportError:
        print("ℹ️  Ollama não está disponível.")
        print("   Para usar relatórios, instale: pip install ollama")
        print()
    
    # Opcional: Chatbot e Análise Inteligente
    print("=" * 70)
    print("🤖 Chatbot e Análise Inteligente (opcional)")
    print("=" * 70)
    print()
    
    try:
        from hospital_routes.llm.chatbot import RouteChatbot, RouteAnalyzer
        from hospital_routes.llm.ollama_helper import check_ollama_running, get_best_available_model
        
        if check_ollama_running() and get_best_available_model():
            print("✅ Ollama disponível para chatbot e análise!")
            print()
            
            # Análise Inteligente de Rotas
            print("📊 Gerando análise inteligente das rotas...")
            print("   (Isso pode levar alguns segundos)")
            print()
            
            try:
                analyzer = RouteAnalyzer()
                analysis = analyzer.analyze_route(
                    result,
                    deliveries,
                    accident_provider=accident_provider,
                )
                
                print("=" * 70)
                print("✅ ANÁLISE INTELIGENTE GERADA!")
                print("=" * 70)
                print()
                print("📄 Análise:")
                print("-" * 70)
                print(analysis["summary"])
                print("-" * 70)
                print()
                
                if analysis.get("recommendations"):
                    print("💡 Recomendações:")
                    for i, rec in enumerate(analysis["recommendations"], 1):
                        print(f"   {i}. {rec}")
                    print()
                
                # Salvar análise
                analysis_output = "route_analysis.txt"
                with open(analysis_output, "w", encoding="utf-8") as f:
                    f.write("ANÁLISE INTELIGENTE DE ROTAS\n")
                    f.write("=" * 70 + "\n\n")
                    f.write(analysis["summary"])
                    f.write("\n\n" + "=" * 70 + "\n")
                    f.write("RECOMENDAÇÕES\n")
                    f.write("=" * 70 + "\n\n")
                    for i, rec in enumerate(analysis.get("recommendations", []), 1):
                        f.write(f"{i}. {rec}\n")
                
                print(f"📁 Análise salva em: {Path(analysis_output).absolute()}")
                print()
                
            except Exception as e:
                print(f"⚠️  Erro ao gerar análise: {e}")
                print("   Continuando...")
                print()
            
            # Exemplo de uso do Chatbot
            print("💬 Exemplo de Chatbot para Operadores:")
            print("   (Você pode usar o chatbot interativamente)")
            print()
            
            try:
                chatbot = RouteChatbot()
                chatbot.set_optimization_context(result)
                
                # Exemplo de perguntas
                example_questions = [
                    "Quantos veículos foram usados?",
                    "Qual a distância total percorrida?",
                    "Há entregas críticas nas rotas?",
                ]
                
                print("   Exemplos de perguntas que você pode fazer:")
                for q in example_questions:
                    print(f"   • {q}")
                print()
                
                # Responder uma pergunta de exemplo
                print("   Testando pergunta de exemplo...")
                response = chatbot.chat("Resuma as rotas otimizadas de forma clara.")
                print(f"   Resposta: {response[:200]}...")
                print()
                
            except Exception as e:
                print(f"⚠️  Erro ao testar chatbot: {e}")
                print()
        else:
            print("ℹ️  Ollama não disponível para chatbot.")
            print("   Instale modelos: ollama pull llama3.2")
            print()
    
    except ImportError:
        print("ℹ️  Funcionalidades de chatbot não disponíveis.")
        print("   Instale: pip install ollama")
        print()
    except Exception as e:
        print(f"⚠️  Erro: {e}")
        print()
    
    # Resumo final
    print("=" * 70)
    print("🎉 DEMONSTRAÇÃO CONCLUÍDA!")
    print("=" * 70)
    print()
    print("📋 Arquivos gerados:")
    print(f"   🗺️  Mapa: {map_output}")
    if Path("driver_instructions.txt").exists():
        print(f"   📄 Relatório: driver_instructions.txt")
    print()
    print("💡 Dicas:")
    print("   - O mapa HTML é interativo: você pode zoom, clicar nos marcadores, etc.")
    print("   - Cada cor representa um veículo diferente")
    print("   - Marcadores vermelhos = entregas críticas (medicamentos)")
    print("   - Marcadores azuis = entregas normais (insumos)")
    print("   - Estrela azul = depósito central")
    print()
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

