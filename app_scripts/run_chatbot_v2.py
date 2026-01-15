"""
Script principal para executar interface refatorada do chatbot.

Versão 2.0 com:
- Layout otimizado (mapa em destaque)
- Chat funcional com Ollama
- Design profissional
- Funcionalidades completas
"""

import sys
from pathlib import Path
import webbrowser
import threading
import time

# Adicionar raiz do projeto ao PYTHONPATH
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from hospital_routes.optimization.genetic_algorithm import GeneticAlgorithmOptimizer
from hospital_routes.visualization.map_generator import MapGenerator
from hospital_routes.visualization.chatbot_interface_v2 import ChatbotInterfaceV2
from hospital_routes.utils.accident_data import create_sample_accident_data
from hospital_routes.llm.ollama_helper import check_ollama_running, get_best_available_model
from seed_real_data import (
    generate_deliveries,
    generate_vehicles,
    get_optimization_config,
    get_depot_location,
)

try:
    from server_chatbot import set_optimization_context, run_server, FLASK_AVAILABLE
    SERVER_AVAILABLE = FLASK_AVAILABLE
except (ImportError, NameError):
    SERVER_AVAILABLE = False
    print("⚠️ Servidor backend não disponível. Interface funcionará em modo standalone.")


def main():
    """Função principal."""
    print("=" * 70)
    print("🤖 Sistema de Chatbot - Interface Refatorada v2.0")
    print("=" * 70)
    print()
    
    # Verificar Ollama
    print("🔍 Verificando Ollama...")
    if not check_ollama_running():
        print("⚠️  Ollama não está rodando.")
        print("   A interface funcionará, mas o chatbot pode não responder corretamente.")
        print()
    else:
        model = get_best_available_model()
        if model:
            print(f"✅ Ollama detectado! Modelo: {model}")
        else:
            print("⚠️  Nenhum modelo Ollama disponível.")
            print("   Execute: ollama pull llama3.2")
        print()
    
    # Carregar dados
    print("📦 Carregando dados...")
    deliveries = generate_deliveries()
    vehicles = generate_vehicles()
    config = get_optimization_config()
    depot = get_depot_location()
    print(f"✅ {len(deliveries)} entregas, {len(vehicles)} veículos")
    print()
    
    # Otimizar
    print("⚙️  Otimizando rotas...")
    optimizer = GeneticAlgorithmOptimizer()
    result = optimizer.optimize(
        deliveries=deliveries,
        vehicles=vehicles,
        config=config,
        depot_location=depot,
    )
    print("✅ Otimização concluída!")
    print(f"   Distância total: {result.solution.total_distance:.2f} km")
    print(f"   Custo total: R$ {result.solution.total_cost:.2f}")
    print(f"   Veículos usados: {len(result.solution.routes)}")
    print()
    
    # Gerar mapa
    print("🗺️  Gerando mapa...")
    accident_provider = create_sample_accident_data()
    
    map_generator = MapGenerator()
    map_file = "route_map.html"
    map_generator.generate_map(
        optimization_result=result,
        deliveries=deliveries,
        depot_location=depot,
        output_path=map_file,
        title="Rotas Otimizadas - Sistema Hospitalar",
        accident_provider=accident_provider,
        show_accidents=True,
    )
    print(f"✅ Mapa gerado: {map_file}")
    print()
    
    # Gerar interface refatorada
    print("🎨 Gerando interface refatorada...")
    interface = ChatbotInterfaceV2(
        optimization_result=result,
        deliveries=deliveries,
        vehicles=vehicles,
        accident_provider=accident_provider,
    )
    
    interface_file = "chatbot_interface_v2.html"
    interface.generate_interface(
        output_path=interface_file,
        map_file=map_file,
        api_url="http://127.0.0.1:5000",
    )
    print(f"✅ Interface gerada: {interface_file}")
    print()
    
    # Iniciar servidor backend (se disponível)
    if SERVER_AVAILABLE:
        print("🚀 Iniciando servidor backend...")
        set_optimization_context(result, deliveries, vehicles)
        
        # Iniciar servidor em thread separada
        server_thread = threading.Thread(
            target=run_server,
            args=('127.0.0.1', 5000, False),
            daemon=True,
        )
        server_thread.start()
        
        # Aguardar servidor iniciar
        time.sleep(2)
        print("✅ Servidor backend rodando em http://127.0.0.1:5000")
        print()
    else:
        print("⚠️  Modo standalone: O chatbot usa respostas simuladas.")
        print("   Para usar chatbot real, instale Flask: pip install flask flask-cors")
        print()
    
    # Abrir no navegador
    print("=" * 70)
    print("🌐 Abrindo interface no navegador...")
    print("=" * 70)
    print()
    
    interface_path = Path(interface_file).absolute()
    webbrowser.open(f"file://{interface_path}")
    
    print("✅ Interface aberta!")
    print()
    print("💡 Funcionalidades:")
    print("   - Mapa em destaque (70% da tela)")
    print("   - Chat funcional com Ollama")
    print("   - Estatísticas compactas")
    print("   - Design profissional")
    print("   - Perguntas rápidas")
    print("   - Histórico de conversa")
    print()
    
    if SERVER_AVAILABLE:
        print("📡 Servidor backend rodando. Pressione Ctrl+C para parar.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Encerrando servidor...")


if __name__ == '__main__':
    main()
