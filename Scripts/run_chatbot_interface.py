"""
Script principal para executar interface completa do chatbot.

Gera interface web moderna com:
- Chatbot interativo
- Informações de motoristas
- Informações de hospitais
- Informações de medicamentos
- Integração com mapa (opcional)
"""

import sys
from pathlib import Path
import webbrowser
import threading
import time

# Adicionar raiz do projeto ao PYTHONPATH
PROJECT_ROOT = Path(__file__).parent.parent  # Subir um nível (scripts -> hospital_routes)
sys.path.insert(0, str(PROJECT_ROOT))

from hospital_routes.optimization.genetic_algorithm import GeneticAlgorithmOptimizer
from hospital_routes.visualization.map_generator import MapGenerator
from hospital_routes.visualization.chatbot_interface import ChatbotWebInterface
from hospital_routes.utils.accident_data import AccidentDataProvider, create_sample_accident_data
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
    print("🤖 Sistema de Chatbot - Interface Completa")
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
    
    # Gerar interface
    print("🎨 Gerando interface web...")
    interface = ChatbotWebInterface(
        optimization_result=result,
        deliveries=deliveries,
        accident_provider=accident_provider,
    )
    
    interface_file = "chatbot_interface.html"
    interface.generate_interface(
        output_path=interface_file,
        include_map=True,
        map_file=map_file,
    )
    print(f"✅ Interface gerada: {interface_file}")
    print()
    
    # Iniciar servidor backend (se disponível)
    if SERVER_AVAILABLE:
        print("🚀 Iniciando servidor backend...")
        set_optimization_context(result, deliveries)
        
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
        
        # Atualizar interface para usar API
        _update_interface_for_api(interface_file)
    
    # Abrir no navegador
    print("=" * 70)
    print("🌐 Abrindo interface no navegador...")
    print("=" * 70)
    print()
    
    interface_path = Path(interface_file).absolute()
    webbrowser.open(f"file://{interface_path}")
    
    print("✅ Interface aberta!")
    print()
    print("💡 Dicas:")
    print("   - Faça perguntas no chat sobre rotas, veículos, entregas")
    print("   - Use os botões de perguntas rápidas")
    print("   - Visualize informações de motoristas e hospitais nos painéis")
    print("   - O mapa está integrado na interface")
    print()
    
    if SERVER_AVAILABLE:
        print("📡 Servidor backend rodando. Pressione Ctrl+C para parar.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Encerrando servidor...")
    else:
        print("⚠️  Modo standalone: O chatbot usa respostas simuladas.")
        print("   Para usar chatbot real, instale Flask: pip install flask flask-cors")


def _update_interface_for_api(interface_file: str):
    """Atualiza interface para usar API do servidor."""
    try:
        with open(interface_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Substituir função callChatbotAPI para usar servidor real
        new_api_code = """
        // Chamar API do chatbot
        async function callChatbotAPI(message) {
            try {
                const response = await fetch('http://127.0.0.1:5000/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });
                
                if (!response.ok) {
                    throw new Error('Erro na API');
                }
                
                const data = await response.json();
                return data.response || 'Desculpe, não consegui processar sua pergunta.';
            } catch (error) {
                console.error('Erro ao chamar API:', error);
                // Fallback para respostas simuladas
                return getFallbackResponse(message);
            }
        }
        
        // Resposta de fallback
        function getFallbackResponse(message) {
            const msg = message.toLowerCase();
            if (msg.includes('veículo') || msg.includes('motorista')) {
                return `Foram utilizados ${statsData.num_vehicles} veículos na otimização. Cada veículo foi responsável por distribuir as entregas de forma eficiente.`;
            } else if (msg.includes('crítica') || msg.includes('medicamento')) {
                return `Há ${statsData.critical_deliveries} entregas críticas (medicamentos) que precisam de atenção especial. Estas entregas foram priorizadas nas rotas.`;
            } else if (msg.includes('distância')) {
                return `A distância total percorrida é de ${statsData.total_distance.toFixed(2)} km, distribuída de forma otimizada entre os veículos.`;
            } else if (msg.includes('custo')) {
                return `O custo total estimado é de R$ ${statsData.total_cost.toFixed(2)}, incluindo combustível e custos de motorista.`;
            } else {
                return `Com base nos dados da otimização: ${statsData.num_vehicles} veículos, ${statsData.num_deliveries} entregas, distância total de ${statsData.total_distance.toFixed(2)} km. Como posso ajudar mais?`;
            }
        }
        """
        
        # Substituir função antiga
        old_pattern = r'async function callChatbotAPI\(message\) \{[\s\S]*?\}'
        import re
        content = re.sub(old_pattern, new_api_code, content)
        
        # Adicionar inicialização do chatbot via API
        init_code = """
        // Inicializar chatbot ao carregar
        document.addEventListener('DOMContentLoaded', async function() {
            try {
                const response = await fetch('http://127.0.0.1:5000/api/init', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
                if (response.ok) {
                    console.log('Chatbot inicializado via API');
                }
            } catch (error) {
                console.warn('Não foi possível inicializar chatbot via API:', error);
            }
        });
        """
        
        # Adicionar antes do fechamento do script
        content = content.replace('</script>', init_code + '\n</script>')
        
        with open(interface_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
    except Exception as e:
        print(f"⚠️  Não foi possível atualizar interface para API: {e}")


if __name__ == '__main__':
    main()
