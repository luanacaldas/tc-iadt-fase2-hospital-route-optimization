"""
Servidor Flask para interface completa do chatbot.

Serve as interfaces HTML atualizadas:
- chatbot_interface_v2.html (dashboard principal)
- rastreamento_mapbox.html (rastreamento ao vivo)
"""

import sys
from pathlib import Path
import webbrowser
import threading
import time
from datetime import datetime

# Adicionar raiz do projeto ao PYTHONPATH
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Importações Flask
try:
    from flask import Flask, send_from_directory, jsonify, request, send_file
    from flask_cors import CORS
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("❌ Flask não instalado. Execute: pip install flask flask-cors")
    sys.exit(1)

# Importações do projeto
from optimization.genetic_algorithm import GeneticAlgorithmOptimizer
from llm.chatbot import RouteChatbot
from llm.ollama_helper import check_ollama_running, get_best_available_model

# Dados do seed_real_data
try:
    sys.path.insert(0, str(PROJECT_ROOT / 'app_scripts'))
    from seed_real_data import (
        generate_deliveries,
        generate_vehicles,
        get_optimization_config,
        get_depot_location,
    )
except ImportError as e:
    print(f"❌ Erro ao importar seed_real_data: {e}")
    sys.exit(1)

# Estado global
app = Flask(__name__)
CORS(app)
optimization_result = None
deliveries_data = None
chatbot_instance = None


@app.route('/')
def serve_dashboard():
    """Servir dashboard principal."""
    interfaces_dir = str(PROJECT_ROOT / 'interfaces')
    file_path = PROJECT_ROOT / 'interfaces' / 'chatbot_interface_v2.html'
    
    if not file_path.exists():
        return f"Erro: Arquivo não encontrado em {file_path}", 404
    
    return send_from_directory(interfaces_dir, 'chatbot_interface_v2.html')


@app.route('/rastreamento')
def serve_rastreamento():
    """Servir rastreamento ao vivo."""
    interfaces_dir = str(PROJECT_ROOT / 'interfaces')
    file_path = PROJECT_ROOT / 'interfaces' / 'rastreamento_mapbox.html'
    
    if not file_path.exists():
        return f"Erro: Arquivo não encontrado em {file_path}", 404
    
    return send_from_directory(interfaces_dir, 'rastreamento_mapbox.html')


@app.route('/map')
def serve_map():
    """Servir mapa de rotas otimizadas."""
    file_path = PROJECT_ROOT / 'route_map.html'
    
    if not file_path.exists():
        return f"Erro: Mapa não encontrado. Execute a otimização primeiro.", 404
    
    return send_from_directory(str(PROJECT_ROOT), 'route_map.html')


@app.route('/api/init', methods=['POST'])
def init():
    """Endpoint para inicializar/verificar se sistema está pronto."""
    global optimization_result, chatbot_instance
    
    return jsonify({
        "status": "ready" if optimization_result else "loading",
        "optimization_ready": optimization_result is not None,
        "chatbot_ready": chatbot_instance is not None
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint para chat com o bot."""
    global chatbot_instance, optimization_result, deliveries_data
    
    if not request.json or 'message' not in request.json:
        return jsonify({"error": "Mensagem não fornecida"}), 400
    
    message = request.json['message']
    
    if not message or not message.strip():
        return jsonify({"error": "Mensagem vazia"}), 400
    
    try:
        # Inicializar chatbot se necessário
        if chatbot_instance is None and optimization_result is not None:
            chatbot_instance = RouteChatbot()
            chatbot_instance.set_optimization_context(optimization_result, deliveries_data)
        
        if chatbot_instance:
            response = chatbot_instance.chat(message)
        else:
            response = "Sistema ainda inicializando. Tente novamente em alguns segundos."
        
        return jsonify({"response": response})
    except Exception as e:
        import traceback
        error_msg = str(e)
        traceback.print_exc()
        return jsonify({
            "error": error_msg, 
            "response": "Desculpe, ocorreu um erro ao processar sua pergunta."
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Verificar saúde do servidor."""
    return jsonify({
        "status": "ok",
        "optimization_loaded": optimization_result is not None,
        "chatbot_ready": chatbot_instance is not None
    })


@app.route('/api/debug', methods=['GET'])
def debug():
    """Debug - verificar caminhos."""
    interfaces_dir = PROJECT_ROOT / 'interfaces'
    dashboard_exists = (interfaces_dir / 'chatbot_interface_v2.html').exists()
    rastreamento_exists = (interfaces_dir / 'rastreamento_mapbox.html').exists()
    
    return jsonify({
        "PROJECT_ROOT": str(PROJECT_ROOT),
        "interfaces_dir": str(interfaces_dir),
        "dashboard_exists": dashboard_exists,
        "rastreamento_exists": rastreamento_exists,
        "dashboard_path": str(interfaces_dir / 'chatbot_interface_v2.html'),
        "rastreamento_path": str(interfaces_dir / 'rastreamento_mapbox.html')
    })


@app.route('/api/stats', methods=['GET'])
def stats():
    """Retornar estatísticas da otimização."""
    global optimization_result, deliveries_data
    
    if optimization_result is None:
        return jsonify({"error": "Otimização não carregada"}), 404
    
    critical_count = sum(1 for d in deliveries_data if d.priority == 1)
    
    return jsonify({
        "total_distance": round(optimization_result.solution.total_distance, 2),
        "total_cost": round(optimization_result.solution.total_cost, 2),
        "num_vehicles": len(optimization_result.solution.routes),
        "num_deliveries": len(deliveries_data),
        "critical_deliveries": critical_count,
        "execution_time": round(optimization_result.execution_time, 2)
    })


@app.route('/api/export/<export_type>', methods=['GET'])
def export_report(export_type):
    """Exportar relatórios em diferentes formatos."""
    global optimization_result, deliveries_data
    
    if optimization_result is None:
        return jsonify({"error": "Otimização não carregada"}), 404
    
    try:
        from visualization.report_exporter import ReportExporter
        
        exporter = ReportExporter()
        vehicles = generate_vehicles()
        
        # Criar diretório de saída
        output_dir = PROJECT_ROOT / 'output'
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if export_type == 'pdf-executive':
            filename = f'relatorio_executivo_{timestamp}.pdf'
            output_path = output_dir / filename
            file_path = exporter.export_pdf_executive(
                optimization_result, deliveries_data, vehicles, str(output_path)
            )
            mimetype = 'application/pdf' if file_path.endswith('.pdf') else 'text/html'
            
        elif export_type == 'pdf-driver':
            filename = f'instrucoes_motorista_{timestamp}.pdf'
            output_path = output_dir / filename
            file_path = exporter.export_pdf_driver(
                optimization_result, deliveries_data, vehicles, str(output_path)
            )
            mimetype = 'application/pdf' if file_path.endswith('.pdf') else 'text/html'
            
        elif export_type == 'excel':
            filename = f'dados_rotas_{timestamp}.xlsx'
            output_path = output_dir / filename
            file_path = exporter.export_excel(
                optimization_result, deliveries_data, vehicles, str(output_path)
            )
            mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            
        else:
            return jsonify({"error": "Tipo de exportação inválido"}), 400
        
        # Enviar arquivo
        return send_file(
            file_path,
            mimetype=mimetype,
            as_attachment=True,
            download_name=Path(file_path).name
        )
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Erro ao exportar: {str(e)}"}), 500


def initialize_optimization():
    """Inicializar otimização em background."""
    global optimization_result, deliveries_data, chatbot_instance
    
    print("\n" + "=" * 70)
    print("⚙️  INICIALIZANDO SISTEMA")
    print("=" * 70)
    
    # Verificar Ollama
    print("\n🔍 Verificando Ollama...")
    if not check_ollama_running():
        print("⚠️  Ollama não está rodando.")
        print("   O chatbot pode não funcionar corretamente.")
    else:
        model = get_best_available_model()
        if model:
            print(f"✅ Ollama detectado! Modelo: {model}")
        else:
            print("⚠️  Nenhum modelo disponível. Execute: ollama pull llama3.2")
    
    # Carregar dados
    print("\n📦 Carregando dados...")
    deliveries_data = generate_deliveries()
    vehicles = generate_vehicles()
    config = get_optimization_config()
    depot = get_depot_location()
    print(f"✅ {len(deliveries_data)} entregas, {len(vehicles)} veículos")
    
    # Otimizar
    print("\n🧬 Executando otimização genética...")
    optimizer = GeneticAlgorithmOptimizer()
    optimization_result = optimizer.optimize(
        deliveries=deliveries_data,
        vehicles=vehicles,
        config=config,
        depot_location=depot,
    )
    
    print("\n✅ OTIMIZAÇÃO CONCLUÍDA!")
    print(f"   📏 Distância total: {optimization_result.solution.total_distance:.2f} km")
    print(f"   💰 Custo total: R$ {optimization_result.solution.total_cost:.2f}")
    print(f"   🚗 Veículos usados: {len(optimization_result.solution.routes)}")
    print(f"   ⏱️  Tempo execução: {optimization_result.execution_time:.2f}s")
    
    # Gerar mapa
    print("\n🗺️  Gerando mapa de rotas...")
    try:
        from visualization.map_generator import MapGenerator
        map_gen = MapGenerator()
        map_gen.generate_map(
            optimization_result=optimization_result,
            deliveries=deliveries_data,
            depot_location=depot,
            output_path=str(PROJECT_ROOT / 'route_map.html'),
            title="Rotas Otimizadas - Hospital Routes",
            show_accidents=False
        )
        print("✅ Mapa gerado!")
    except Exception as e:
        print(f"⚠️  Erro ao gerar mapa: {e}")
    
    # Inicializar chatbot
    print("\n🤖 Inicializando chatbot...")
    try:
        chatbot_instance = RouteChatbot()
        chatbot_instance.set_optimization_context(optimization_result, deliveries_data)
        print("✅ Chatbot pronto!")
    except Exception as e:
        print(f"⚠️  Erro ao inicializar chatbot: {e}")
    
    print("\n" + "=" * 70)


def main():
    """Função principal."""
    print("\n" + "=" * 70)
    print("🏥 SISTEMA DE ROTAS HOSPITALARES")
    print("=" * 70)
    print("\n🚀 Iniciando servidor Flask...")
    
    # Inicializar otimização em thread separada
    init_thread = threading.Thread(target=initialize_optimization, daemon=True)
    init_thread.start()
    
    # Aguardar um pouco para thread iniciar
    time.sleep(1)
    
    # Abrir navegador
    url = "http://127.0.0.1:5000"
    print(f"\n🌐 Abrindo navegador: {url}")
    
    def open_browser():
        time.sleep(2)  # Aguardar servidor iniciar
        try:
            webbrowser.open(url)
            print(f"✅ Navegador aberto com URL: {url}")
        except Exception as e:
            print(f"⚠️  Erro ao abrir navegador: {e}")
            print(f"   Acesse manualmente: {url}")
    
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Iniciar servidor
    print("\n" + "=" * 70)
    print("📡 SERVIDOR RODANDO")
    print("=" * 70)
    print(f"\n✅ Dashboard: {url}")
    print(f"✅ Rastreamento: {url}/rastreamento")
    print(f"✅ API Chat: {url}/api/chat")
    print(f"✅ Stats: {url}/api/stats")
    print(f"✅ Debug: {url}/api/debug")
    print("\n💡 Pressione Ctrl+C para parar o servidor\n")
    
    try:
        app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n👋 Encerrando servidor...")


if __name__ == '__main__':
    main()
