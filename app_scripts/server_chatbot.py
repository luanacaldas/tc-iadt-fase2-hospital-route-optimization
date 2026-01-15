"""
Servidor backend para interface do chatbot.

Fornece API REST para comunicação entre interface web e chatbot Python.
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
import json

# Adicionar raiz do projeto ao PYTHONPATH
PROJECT_ROOT = Path(__file__).parent.parent  # Subir um nível (scripts -> hospital_routes)
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from flask import Flask, request, jsonify, send_from_directory
    from flask_cors import CORS
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    Flask = None
    request = None
    jsonify = None
    send_from_directory = None
    CORS = None

from hospital_routes.llm.chatbot import RouteChatbot
from hospital_routes.llm.ollama_helper import check_ollama_running, get_best_available_model
from hospital_routes.core.interfaces import OptimizationResult
from hospital_routes.visualization.report_exporter import ReportExporter


# Criar app apenas se Flask estiver disponível
if FLASK_AVAILABLE:
    app = Flask(__name__)
    CORS(app)
else:
    app = None

# Estado global
chatbot_instance: Optional[RouteChatbot] = None
optimization_result: Optional[OptimizationResult] = None
deliveries_data: list = []
vehicles_data: list = []
report_exporter = ReportExporter() if FLASK_AVAILABLE else None


# Rotas apenas se Flask estiver disponível
if FLASK_AVAILABLE:
    @app.route('/api/chat', methods=['POST'])
    def chat():
        """Endpoint para enviar mensagens ao chatbot."""
        global chatbot_instance
        
        if chatbot_instance is None:
            # Tentar inicializar se não estiver inicializado
            try:
                chatbot_instance = RouteChatbot()
                if optimization_result:
                    chatbot_instance.set_optimization_context(optimization_result, deliveries_data)
            except Exception as e:
                return jsonify({"error": f"Erro ao inicializar chatbot: {str(e)}"}), 500
        
        data = request.json
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({"error": "Mensagem vazia"}), 400
        
        try:
            response = chatbot_instance.chat(message)
            return jsonify({"response": response})
        except Exception as e:
            import traceback
            error_msg = str(e)
            traceback.print_exc()
            return jsonify({"error": error_msg, "response": "Desculpe, ocorreu um erro ao processar sua pergunta."}), 500


    @app.route('/api/init', methods=['POST'])
    def init_chatbot():
        """Inicializa o chatbot com contexto de otimização."""
        global chatbot_instance, optimization_result
        
        if optimization_result is None:
            return jsonify({"error": "Resultado de otimização não fornecido"}), 400
        
        try:
            chatbot_instance = RouteChatbot()
            chatbot_instance.set_optimization_context(optimization_result, deliveries_data)
            return jsonify({"status": "ok", "message": "Chatbot inicializado"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @app.route('/api/health', methods=['GET'])
    def health():
        """Verifica saúde do servidor."""
        ollama_running = check_ollama_running()
        model = get_best_available_model() if ollama_running else None
        
        return jsonify({
            "status": "ok",
            "ollama_running": ollama_running,
            "model": model,
            "chatbot_initialized": chatbot_instance is not None,
        })


    @app.route('/api/export/<export_type>', methods=['GET'])
    def export_report(export_type: str):
        """Exporta relatório no formato solicitado."""
        global optimization_result, deliveries_data, vehicles_data
        
        if optimization_result is None:
            return jsonify({"error": "Nenhum resultado de otimização disponível"}), 400
        
        if not deliveries_data:
            return jsonify({"error": "Dados de entregas não disponíveis"}), 400
        
        if not vehicles_data:
            return jsonify({"error": "Dados de veículos não disponíveis"}), 400
        
        try:
            from pathlib import Path
            import tempfile
            import os
            
            # Criar diretório temporário para os arquivos
            temp_dir = Path(tempfile.gettempdir()) / "hospital_routes_exports"
            temp_dir.mkdir(parents=True, exist_ok=True)
            
            # Gerar nome do arquivo baseado no tipo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_map = {
                'pdf-executive': f'relatorio_executivo_{timestamp}.pdf',
                'pdf-driver': f'instrucoes_motoristas_{timestamp}.pdf',
                'excel': f'rotas_otimizadas_{timestamp}.xlsx',
                'json': f'dados_rotas_{timestamp}.json',
            }
            
            if export_type not in file_map:
                return jsonify({"error": f"Tipo de exportação inválido: {export_type}"}), 400
            
            output_file = temp_dir / file_map[export_type]
            
            # Gerar arquivo baseado no tipo
            if export_type == 'pdf-executive':
                file_path = report_exporter.export_pdf_executive(
                    optimization_result, deliveries_data, vehicles_data, str(output_file)
                )
            elif export_type == 'pdf-driver':
                file_path = report_exporter.export_pdf_driver(
                    optimization_result, deliveries_data, vehicles_data, str(output_file)
                )
            elif export_type == 'excel':
                file_path = report_exporter.export_excel(
                    optimization_result, deliveries_data, vehicles_data, str(output_file)
                )
            elif export_type == 'json':
                file_path = report_exporter.export_json(
                    optimization_result, deliveries_data, vehicles_data, str(output_file)
                )
            
            # Determinar MIME type
            mime_types = {
                'pdf-executive': 'application/pdf',
                'pdf-driver': 'application/pdf',
                'excel': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'json': 'application/json',
            }
            
            # Se o arquivo gerado for HTML (fallback do PDF), ajustar MIME type
            if file_path.endswith('.html'):
                mime_type = 'text/html'
            else:
                mime_type = mime_types.get(export_type, 'application/octet-stream')
            
            # Enviar arquivo para download
            return send_from_directory(
                directory=str(Path(file_path).parent),
                path=Path(file_path).name,
                as_attachment=True,
                mimetype=mime_type
            )
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({"error": f"Erro ao exportar: {str(e)}"}), 500


def set_optimization_context(result: OptimizationResult, deliveries: list, vehicles: list = None):
    """Define o contexto de otimização para o servidor."""
    global optimization_result, deliveries_data, vehicles_data, chatbot_instance
    optimization_result = result
    deliveries_data = deliveries
    vehicles_data = vehicles or []
    
    # Se chatbot já existe, atualizar contexto com entregas
    if chatbot_instance is not None:
        chatbot_instance.set_optimization_context(result, deliveries)


def run_server(host='127.0.0.1', port=5000, debug=True):
    """Executa o servidor Flask."""
    if not FLASK_AVAILABLE:
        print("❌ Flask não está instalado.")
        print("   Instale com: pip install flask flask-cors")
        return
    
    print(f"🚀 Servidor iniciado em http://{host}:{port}")
    print(f"📡 API disponível em http://{host}:{port}/api/")
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_server()
