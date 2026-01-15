"""
Interface web completa para o chatbot com painéis informativos.

Cria uma interface moderna e fluida com:
- Chatbot interativo
- Informações de motoristas
- Informações de hospitais
- Informações de medicamentos
- Integração com mapa (opcional)
"""

from typing import Optional, List, Dict, Any
from pathlib import Path
import json
from datetime import datetime

from hospital_routes.core.interfaces import (
    OptimizationResult,
    Delivery,
    RouteSolution,
)


class ChatbotWebInterface:
    """
    Gera interface web completa para chatbot com painéis informativos.
    
    Cria uma interface moderna, responsiva e fluida.
    """
    
    def __init__(
        self,
        optimization_result: OptimizationResult,
        deliveries: List[Delivery],
        accident_provider: Optional[Any] = None,
    ):
        """
        Args:
            optimization_result: Resultado da otimização
            deliveries: Lista de entregas
            accident_provider: Provedor de dados de acidentes (opcional)
        """
        self.optimization_result = optimization_result
        self.deliveries = deliveries
        self.accident_provider = accident_provider
        self.solution = optimization_result.solution
        
        # Preparar dados
        self._prepare_data()
    
    def _prepare_data(self) -> None:
        """Prepara dados para a interface."""
        # Dados de motoristas/veículos
        self.drivers_data = []
        for idx, route in enumerate(self.solution.routes):
            route_deliveries = [d for d in self.deliveries if d.id in route]
            critical_count = sum(1 for d in route_deliveries if d.priority == 1)
            total_weight = sum(d.weight for d in route_deliveries)
            
            self.drivers_data.append({
                "driver_id": idx + 1,
                "route": route,
                "num_deliveries": len(route),
                "critical_deliveries": critical_count,
                "total_weight": total_weight,
                "distance": self._calculate_route_distance(route),
            })
        
        # Dados de hospitais
        self.hospitals_data = []
        for delivery in self.deliveries:
            self.hospitals_data.append({
                "id": delivery.id,
                "location": delivery.location,
                "priority": delivery.priority,
                "weight": delivery.weight,
                "is_critical": delivery.priority == 1,
            })
        
        # Estatísticas gerais
        self.stats = {
            "total_distance": self.solution.total_distance,
            "total_cost": self.solution.total_cost,
            "num_vehicles": len(self.solution.routes),
            "num_deliveries": len(self.deliveries),
            "critical_deliveries": sum(1 for d in self.deliveries if d.priority == 1),
            "execution_time": self.optimization_result.execution_time,
        }
    
    def _calculate_route_distance(self, route: List[str]) -> float:
        """Calcula distância de uma rota."""
        from hospital_routes.utils.distance import calculate_distance
        
        if not route:
            return 0.0
        
        total = 0.0
        delivery_dict = {d.id: d for d in self.deliveries}
        
        # Distância entre entregas
        for i in range(len(route) - 1):
            if route[i] in delivery_dict and route[i + 1] in delivery_dict:
                total += calculate_distance(
                    delivery_dict[route[i]].location,
                    delivery_dict[route[i + 1]].location,
                )
        
        return total
    
    def generate_interface(
        self,
        output_path: str = "chatbot_interface.html",
        include_map: bool = False,
        map_file: Optional[str] = None,
    ) -> str:
        """
        Gera interface web completa.
        
        Args:
            output_path: Caminho do arquivo HTML
            include_map: Se True, integra mapa no iframe
            map_file: Caminho do arquivo do mapa (se include_map=True)
        
        Returns:
            str: Caminho do arquivo gerado
        """
        html_content = self._generate_html(include_map, map_file)
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        return str(output_file.absolute())
    
    def _generate_html(self, include_map: bool, map_file: Optional[str]) -> str:
        """Gera HTML completo da interface."""
        
        # Preparar dados JSON para JavaScript
        drivers_json = json.dumps(self.drivers_data, ensure_ascii=False, indent=2)
        hospitals_json = json.dumps(self.hospitals_data, ensure_ascii=False, indent=2)
        stats_json = json.dumps(self.stats, ensure_ascii=False, indent=2)
        
        html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot - Sistema de Rotas Hospitalares</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }}
        
        .header {{
            background: rgba(255, 255, 255, 0.95);
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            z-index: 1000;
        }}
        
        .header h1 {{
            color: #333;
            font-size: 24px;
            margin-bottom: 10px;
        }}
        
        .header .stats {{
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }}
        
        .stat-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            color: #666;
            font-size: 14px;
        }}
        
        .stat-item i {{
            color: #667eea;
        }}
        
        .container {{
            display: flex;
            flex: 1;
            gap: 20px;
            padding: 20px;
            overflow: hidden;
        }}
        
        .left-panel {{
            width: 350px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            overflow-y: auto;
        }}
        
        .main-content {{
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 20px;
            min-width: 0;
        }}
        
        .right-panel {{
            width: 350px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            overflow-y: auto;
        }}
        
        .panel {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .panel-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #f0f0f0;
        }}
        
        .panel-header h2 {{
            color: #333;
            font-size: 18px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .panel-header i {{
            color: #667eea;
        }}
        
        .chat-container {{
            display: flex;
            flex-direction: column;
            height: 600px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .chat-messages {{
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            background: #f8f9fa;
        }}
        
        .message {{
            margin-bottom: 15px;
            animation: fadeIn 0.3s;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .message.user {{
            text-align: right;
        }}
        
        .message.assistant {{
            text-align: left;
        }}
        
        .message-bubble {{
            display: inline-block;
            max-width: 70%;
            padding: 12px 16px;
            border-radius: 18px;
            word-wrap: break-word;
        }}
        
        .message.user .message-bubble {{
            background: #667eea;
            color: white;
        }}
        
        .message.assistant .message-bubble {{
            background: white;
            color: #333;
            border: 1px solid #e0e0e0;
        }}
        
        .chat-input-container {{
            padding: 15px;
            background: white;
            border-top: 1px solid #e0e0e0;
            display: flex;
            gap: 10px;
        }}
        
        .chat-input {{
            flex: 1;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            font-size: 14px;
            outline: none;
            transition: border-color 0.3s;
        }}
        
        .chat-input:focus {{
            border-color: #667eea;
        }}
        
        .send-button {{
            padding: 12px 24px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
            transition: background 0.3s;
        }}
        
        .send-button:hover {{
            background: #5568d3;
        }}
        
        .send-button:disabled {{
            background: #ccc;
            cursor: not-allowed;
        }}
        
        .driver-card, .hospital-card {{
            padding: 15px;
            margin-bottom: 10px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .driver-card:hover, .hospital-card:hover {{
            transform: translateX(5px);
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .driver-card h3, .hospital-card h3 {{
            color: #333;
            font-size: 16px;
            margin-bottom: 8px;
        }}
        
        .driver-card .info, .hospital-card .info {{
            display: flex;
            flex-direction: column;
            gap: 5px;
            font-size: 13px;
            color: #666;
        }}
        
        .badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: bold;
            margin-top: 5px;
        }}
        
        .badge-critical {{
            background: #fee;
            color: #c33;
        }}
        
        .badge-normal {{
            background: #eef;
            color: #336;
        }}
        
        .badge-success {{
            background: #efe;
            color: #363;
        }}
        
        .map-container {{
            height: 400px;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .map-container iframe {{
            width: 100%;
            height: 100%;
            border: none;
        }}
        
        .loading {{
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        .quick-actions {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }}
        
        .quick-action-btn {{
            padding: 6px 12px;
            background: #f0f0f0;
            border: 1px solid #ddd;
            border-radius: 15px;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        
        .quick-action-btn:hover {{
            background: #667eea;
            color: white;
            border-color: #667eea;
        }}
        
        .scrollbar-custom::-webkit-scrollbar {{
            width: 8px;
        }}
        
        .scrollbar-custom::-webkit-scrollbar-track {{
            background: #f1f1f1;
            border-radius: 10px;
        }}
        
        .scrollbar-custom::-webkit-scrollbar-thumb {{
            background: #888;
            border-radius: 10px;
        }}
        
        .scrollbar-custom::-webkit-scrollbar-thumb:hover {{
            background: #555;
        }}
        
        @media (max-width: 1200px) {{
            .container {{
                flex-direction: column;
            }}
            
            .left-panel, .right-panel {{
                width: 100%;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1><i class="fas fa-robot"></i> Chatbot - Sistema de Rotas Hospitalares</h1>
        <div class="stats">
            <div class="stat-item">
                <i class="fas fa-truck"></i>
                <span>{self.stats['num_vehicles']} Veículos</span>
            </div>
            <div class="stat-item">
                <i class="fas fa-box"></i>
                <span>{self.stats['num_deliveries']} Entregas</span>
            </div>
            <div class="stat-item">
                <i class="fas fa-exclamation-triangle"></i>
                <span>{self.stats['critical_deliveries']} Críticas</span>
            </div>
            <div class="stat-item">
                <i class="fas fa-route"></i>
                <span>{self.stats['total_distance']:.1f} km</span>
            </div>
            <div class="stat-item">
                <i class="fas fa-dollar-sign"></i>
                <span>R$ {self.stats['total_cost']:.2f}</span>
            </div>
        </div>
    </div>
    
    <div class="container">
        <!-- Painel Esquerdo: Motoristas -->
        <div class="left-panel scrollbar-custom">
            <div class="panel">
                <div class="panel-header">
                    <h2><i class="fas fa-users"></i> Motoristas</h2>
                </div>
                <div id="drivers-list">
                    <!-- Preenchido via JavaScript -->
                </div>
            </div>
            
            <div class="panel">
                <div class="panel-header">
                    <h2><i class="fas fa-hospital"></i> Hospitais</h2>
                </div>
                <div id="hospitals-list">
                    <!-- Preenchido via JavaScript -->
                </div>
            </div>
        </div>
        
        <!-- Conteúdo Principal: Chatbot -->
        <div class="main-content">
            <div class="chat-container">
                <div class="chat-messages scrollbar-custom" id="chat-messages">
                    <div class="message assistant">
                        <div class="message-bubble">
                            <strong>🤖 Assistente:</strong> Olá! Sou o assistente do sistema de rotas hospitalares. 
                            Posso ajudar você com informações sobre rotas, entregas, veículos e muito mais. 
                            Faça sua pergunta!
                        </div>
                    </div>
                </div>
                <div class="chat-input-container">
                    <input 
                        type="text" 
                        class="chat-input" 
                        id="chat-input" 
                        placeholder="Digite sua pergunta..."
                        onkeypress="if(event.key === 'Enter') sendMessage()"
                    >
                    <button class="send-button" onclick="sendMessage()" id="send-btn">
                        <i class="fas fa-paper-plane"></i> Enviar
                    </button>
                </div>
            </div>
            
            <!-- Ações Rápidas -->
            <div class="panel">
                <div class="panel-header">
                    <h2><i class="fas fa-bolt"></i> Perguntas Rápidas</h2>
                </div>
                <div class="quick-actions">
                    <button class="quick-action-btn" onclick="askQuick('Quantos veículos foram usados?')">
                        Quantos veículos?
                    </button>
                    <button class="quick-action-btn" onclick="askQuick('Há entregas críticas?')">
                        Entregas críticas?
                    </button>
                    <button class="quick-action-btn" onclick="askQuick('Qual a distância total?')">
                        Distância total?
                    </button>
                    <button class="quick-action-btn" onclick="askQuick('Analise a eficiência das rotas')">
                        Análise de eficiência
                    </button>
                    <button class="quick-action-btn" onclick="askQuick('Quais hospitais serão visitados?')">
                        Hospitais visitados?
                    </button>
                    <button class="quick-action-btn" onclick="askQuick('Há melhorias possíveis?')">
                        Sugestões de melhoria
                    </button>
                </div>
            </div>
            
            <!-- Mapa (se incluído) -->
            {self._generate_map_section(include_map, map_file)}
        </div>
        
        <!-- Painel Direito: Estatísticas e Informações -->
        <div class="right-panel scrollbar-custom">
            <div class="panel">
                <div class="panel-header">
                    <h2><i class="fas fa-chart-bar"></i> Estatísticas</h2>
                </div>
                <div class="info">
                    <div style="margin-bottom: 15px;">
                        <strong>Distância Total:</strong><br>
                        <span style="color: #667eea; font-size: 20px; font-weight: bold;">
                            {self.stats['total_distance']:.2f} km
                        </span>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <strong>Custo Total:</strong><br>
                        <span style="color: #667eea; font-size: 20px; font-weight: bold;">
                            R$ {self.stats['total_cost']:.2f}
                        </span>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <strong>Tempo de Execução:</strong><br>
                        <span style="color: #667eea; font-size: 20px; font-weight: bold;">
                            {self.stats['execution_time']:.2f}s
                        </span>
                    </div>
                    <div>
                        <strong>Fitness Score:</strong><br>
                        <span style="color: #667eea; font-size: 20px; font-weight: bold;">
                            {self.solution.fitness_score:.2f}
                        </span>
                    </div>
                </div>
            </div>
            
            <div class="panel">
                <div class="panel-header">
                    <h2><i class="fas fa-pills"></i> Medicamentos</h2>
                </div>
                <div id="medications-list">
                    <!-- Preenchido via JavaScript -->
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Dados
        const driversData = {drivers_json};
        const hospitalsData = {hospitals_json};
        const statsData = {stats_json};
        
        // Estado do chatbot
        let conversationHistory = [];
        let isProcessing = false;
        
        // Inicializar interface
        document.addEventListener('DOMContentLoaded', function() {{
            renderDrivers();
            renderHospitals();
            renderMedications();
        }});
        
        // Renderizar motoristas
        function renderDrivers() {{
            const container = document.getElementById('drivers-list');
            container.innerHTML = '';
            
            driversData.forEach(driver => {{
                const card = document.createElement('div');
                card.className = 'driver-card';
                card.innerHTML = `
                    <h3><i class="fas fa-user"></i> Motorista ${{driver.driver_id}}</h3>
                    <div class="info">
                        <div><i class="fas fa-box"></i> ${{driver.num_deliveries}} entregas</div>
                        <div><i class="fas fa-exclamation-triangle"></i> ${{driver.critical_deliveries}} críticas</div>
                        <div><i class="fas fa-weight"></i> ${{driver.total_weight.toFixed(1)}} kg</div>
                        <div><i class="fas fa-route"></i> ${{driver.distance.toFixed(2)}} km</div>
                    </div>
                `;
                container.appendChild(card);
            }});
        }}
        
        // Renderizar hospitais
        function renderHospitals() {{
            const container = document.getElementById('hospitals-list');
            container.innerHTML = '';
            
            hospitalsData.forEach(hospital => {{
                const card = document.createElement('div');
                card.className = 'hospital-card';
                const badge = hospital.is_critical 
                    ? '<span class="badge badge-critical">CRÍTICA</span>'
                    : '<span class="badge badge-normal">Normal</span>';
                card.innerHTML = `
                    <h3><i class="fas fa-hospital"></i> ${{hospital.id}}</h3>
                    <div class="info">
                        <div>Prioridade: ${{hospital.priority}}</div>
                        <div>Peso: ${{hospital.weight}} kg</div>
                        <div>Localização: (${{hospital.location[0].toFixed(4)}}, ${{hospital.location[1].toFixed(4)}})</div>
                        ${{badge}}
                    </div>
                `;
                container.appendChild(card);
            }});
        }}
        
        // Renderizar medicamentos
        function renderMedications() {{
            const container = document.getElementById('medications-list');
            container.innerHTML = '';
            
            const critical = hospitalsData.filter(h => h.is_critical);
            const normal = hospitalsData.filter(h => !h.is_critical);
            
            if (critical.length > 0) {{
                const section = document.createElement('div');
                section.innerHTML = '<strong style="color: #c33;">Medicamentos Críticos:</strong>';
                container.appendChild(section);
                
                critical.forEach(h => {{
                    const item = document.createElement('div');
                    item.style.cssText = 'padding: 8px; margin: 5px 0; background: #fee; border-radius: 5px;';
                    item.innerHTML = `<i class="fas fa-exclamation-circle" style="color: #c33;"></i> ${{h.id}} - ${{h.weight}}kg`;
                    container.appendChild(item);
                }});
            }}
            
            if (normal.length > 0) {{
                const section = document.createElement('div');
                section.style.marginTop = '15px';
                section.innerHTML = '<strong>Insumos Normais:</strong>';
                container.appendChild(section);
                
                normal.forEach(h => {{
                    const item = document.createElement('div');
                    item.style.cssText = 'padding: 8px; margin: 5px 0; background: #eef; border-radius: 5px;';
                    item.innerHTML = `<i class="fas fa-box"></i> ${{h.id}} - ${{h.weight}}kg`;
                    container.appendChild(item);
                }});
            }}
        }}
        
        // Enviar mensagem
        async function sendMessage() {{
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            
            if (!message || isProcessing) return;
            
            // Adicionar mensagem do usuário
            addMessage('user', message);
            input.value = '';
            
            // Mostrar loading
            isProcessing = true;
            const sendBtn = document.getElementById('send-btn');
            sendBtn.disabled = true;
            sendBtn.innerHTML = '<div class="loading"></div>';
            
            // Chamar API do chatbot (via backend ou direto)
            try {{
                const response = await callChatbotAPI(message);
                addMessage('assistant', response);
            }} catch (error) {{
                addMessage('assistant', 'Desculpe, ocorreu um erro. Tente novamente.');
                console.error('Erro:', error);
            }} finally {{
                isProcessing = false;
                sendBtn.disabled = false;
                sendBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Enviar';
            }}
        }}
        
        // Chamar API do chatbot
        async function callChatbotAPI(message) {{
            // Nota: Em produção, isso chamaria um backend
            // Por enquanto, retornamos uma resposta simulada
            // Você pode integrar com um servidor Flask/FastAPI
            
            // Simulação de resposta (substitua por chamada real)
            return new Promise((resolve) => {{
                setTimeout(() => {{
                    // Respostas baseadas em palavras-chave
                    const msg = message.toLowerCase();
                    if (msg.includes('veículo') || msg.includes('motorista')) {{
                        resolve(`Foram utilizados ${{statsData.num_vehicles}} veículos na otimização. Cada veículo foi responsável por distribuir as entregas de forma eficiente.`);
                    }} else if (msg.includes('crítica') || msg.includes('medicamento')) {{
                        resolve(`Há ${{statsData.critical_deliveries}} entregas críticas (medicamentos) que precisam de atenção especial. Estas entregas foram priorizadas nas rotas.`);
                    }} else if (msg.includes('distância')) {{
                        resolve(`A distância total percorrida é de ${{statsData.total_distance.toFixed(2)}} km, distribuída de forma otimizada entre os veículos.`);
                    }} else if (msg.includes('custo')) {{
                        resolve(`O custo total estimado é de R$ ${{statsData.total_cost.toFixed(2)}}, incluindo combustível e custos de motorista.`);
                    }} else {{
                        resolve(`Com base nos dados da otimização: ${{statsData.num_vehicles}} veículos, ${{statsData.num_deliveries}} entregas, distância total de ${{statsData.total_distance.toFixed(2)}} km. Como posso ajudar mais?`);
                    }}
                }}, 1000);
            }});
        }}
        
        // Adicionar mensagem ao chat
        function addMessage(role, content) {{
            const container = document.getElementById('chat-messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${{role}}`;
            
            const roleLabel = role === 'user' ? 'Você' : '🤖 Assistente';
            messageDiv.innerHTML = `
                <div class="message-bubble">
                    <strong>${{roleLabel}}:</strong> ${{content}}
                </div>
            `;
            
            container.appendChild(messageDiv);
            container.scrollTop = container.scrollHeight;
            
            // Salvar no histórico
            conversationHistory.push({{role, content, timestamp: new Date()}});
        }}
        
        // Pergunta rápida
        function askQuick(question) {{
            document.getElementById('chat-input').value = question;
            sendMessage();
        }}
    </script>
</body>
</html>
"""
        return html
    
    def _generate_map_section(self, include_map: bool, map_file: Optional[str]) -> str:
        """Gera seção do mapa se solicitado."""
        if not include_map or not map_file:
            return ""
        
        map_path = Path(map_file).absolute()
        return f"""
            <div class="panel">
                <div class="panel-header">
                    <h2><i class="fas fa-map"></i> Mapa das Rotas</h2>
                </div>
                <div class="map-container">
                    <iframe src="file://{map_path}" title="Mapa de Rotas"></iframe>
                </div>
            </div>
        """
