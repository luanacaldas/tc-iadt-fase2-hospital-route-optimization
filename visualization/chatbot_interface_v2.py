"""
Interface web refatorada para chatbot - Versão 2.0

Layout otimizado com:
- Mapa em destaque (70% da tela)
- Chat colapsável e funcional
- Estatísticas compactas
- Design profissional
- Integração completa com Ollama
"""

from typing import Optional, List, Dict, Any
from pathlib import Path
import json
from datetime import datetime

from hospital_routes.core.interfaces import (
    OptimizationResult,
    Delivery,
    RouteSolution,
    VehicleConstraints,
)


class ChatbotInterfaceV2:
    """
    Interface web refatorada com layout otimizado e funcionalidades completas.
    
    Prioridades:
    1. Mapa em destaque (elemento principal)
    2. Chat funcional com Ollama
    3. Estatísticas compactas
    4. Design profissional e acessível
    """
    
    def __init__(
        self,
        optimization_result: OptimizationResult,
        deliveries: List[Delivery],
        vehicles: Optional[List[VehicleConstraints]] = None,
        accident_provider: Optional[Any] = None,
    ):
        """
        Args:
            optimization_result: Resultado da otimização
            deliveries: Lista de entregas
            vehicles: Lista de veículos com restrições (opcional)
            accident_provider: Provedor de dados de acidentes (opcional)
        """
        self.optimization_result = optimization_result
        self.deliveries = deliveries
        self.vehicles = vehicles or []
        self.accident_provider = accident_provider
        self.solution = optimization_result.solution
        
        # Cores dos veículos (mesmas do MapGenerator)
        self.vehicle_colors = [
            "blue", "red", "green", "purple", "orange", "darkred",
            "lightred", "beige", "darkblue", "darkgreen", "cadetblue",
            "darkpurple", "white", "pink", "lightblue", "lightgreen",
            "gray", "black", "lightgray",
        ]
        
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
            route_distance = self._calculate_route_distance(route)
            
            # Obter restrições do veículo se disponível
            vehicle = self.vehicles[idx] if idx < len(self.vehicles) else None
            max_capacity = vehicle.max_capacity if vehicle else 100.0
            max_range = vehicle.max_range if vehicle else 200.0
            
            # Calcular percentuais
            capacity_percent = (total_weight / max_capacity * 100) if max_capacity > 0 else 0
            range_percent = (route_distance / max_range * 100) if max_range > 0 else 0
            
            # Status de capacidade
            if capacity_percent < 70:
                capacity_status = "ok"
            elif capacity_percent < 90:
                capacity_status = "warning"
            else:
                capacity_status = "critical"
            
            # Status de autonomia
            if range_percent < 70:
                range_status = "ok"
            elif range_percent < 90:
                range_status = "warning"
            else:
                range_status = "critical"
            
            # Custo estimado (simplificado)
            cost_per_km = vehicle.fuel_cost_per_km if vehicle else 2.5
            route_cost = route_distance * cost_per_km
            
            self.drivers_data.append({
                "driver_id": idx + 1,
                "route": route,
                "num_deliveries": len(route),
                "critical_deliveries": critical_count,
                "total_weight": total_weight,
                "max_capacity": max_capacity,
                "capacity_percent": capacity_percent,
                "capacity_status": capacity_status,
                "distance": route_distance,
                "max_range": max_range,
                "range_percent": range_percent,
                "range_status": range_status,
                "cost": route_cost,
                "color": self.vehicle_colors[idx % len(self.vehicle_colors)],
            })
        
        # Dados de entregas críticas
        self.critical_deliveries_data = []
        for delivery in self.deliveries:
            if delivery.priority == 1:
                # Encontrar em qual rota está
                route_idx = None
                for idx, route in enumerate(self.solution.routes):
                    if delivery.id in route:
                        route_idx = idx
                        break
                
                self.critical_deliveries_data.append({
                    "id": delivery.id,
                    "location": delivery.location,
                    "weight": delivery.weight,
                    "vehicle_id": route_idx + 1 if route_idx is not None else None,
                    "vehicle_color": self.vehicle_colors[route_idx % len(self.vehicle_colors)] if route_idx is not None else "gray",
                })
        
        # Estatísticas gerais
        self.stats = {
            "total_distance": self.solution.total_distance,
            "total_cost": self.solution.total_cost,
            "num_vehicles": len(self.solution.routes),
            "num_deliveries": len(self.deliveries),
            "critical_deliveries": sum(1 for d in self.deliveries if d.priority == 1),
            "execution_time": self.optimization_result.execution_time,
            "fitness_score": self.solution.fitness_score,
        }
    
    def _calculate_route_distance(self, route: List[str]) -> float:
        """Calcula distância de uma rota."""
        from hospital_routes.utils.distance import calculate_distance
        
        if not route:
            return 0.0
        
        total = 0.0
        delivery_dict = {d.id: d for d in self.deliveries}
        
        for i in range(len(route) - 1):
            if route[i] in delivery_dict and route[i + 1] in delivery_dict:
                total += calculate_distance(
                    delivery_dict[route[i]].location,
                    delivery_dict[route[i + 1]].location,
                )
        
        return total
    
    def generate_interface(
        self,
        output_path: str = "chatbot_interface_v2.html",
        map_file: Optional[str] = None,
        api_url: str = "http://127.0.0.1:5000",
    ) -> str:
        """
        Gera interface web refatorada.
        
        Args:
            output_path: Caminho do arquivo HTML
            map_file: Caminho do arquivo do mapa
            api_url: URL da API backend
        
        Returns:
            str: Caminho do arquivo gerado
        """
        html_content = self._generate_html(map_file, api_url)
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        return str(output_file.absolute())
    
    def _generate_html(self, map_file: Optional[str], api_url: str) -> str:
        """Gera HTML completo da interface refatorada."""
        
        # Preparar dados JSON para JavaScript
        drivers_json = json.dumps(self.drivers_data, ensure_ascii=False, indent=2)
        critical_json = json.dumps(self.critical_deliveries_data, ensure_ascii=False, indent=2)
        stats_json = json.dumps(self.stats, ensure_ascii=False, indent=2)
        
        # Preparar dados de todas as entregas para dropdown
        all_deliveries_json = json.dumps([
            {
                "id": d.id,
                "location": d.location,
                "priority": d.priority,
                "weight": d.weight,
                "is_critical": d.priority == 1,
            }
            for d in self.deliveries
        ], ensure_ascii=False, indent=2)
        
        map_path = f"file://{Path(map_file).absolute()}" if map_file else ""
        
        html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Rotas Hospitalares - Chatbot Inteligente</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --primary: #2563eb;
            --primary-dark: #1e40af;
            --secondary: #64748b;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --bg: #f8fafc;
            --surface: #ffffff;
            --text: #1e293b;
            --text-light: #64748b;
            --border: #e2e8f0;
            --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            overflow: hidden;
        }}
        
        .app-container {{
            display: flex;
            flex-direction: column;
            height: 100vh;
        }}
        
        /* Header */
        .header {{
            background: var(--surface);
            border-bottom: 1px solid var(--border);
            padding: 1rem 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: var(--shadow);
            z-index: 100;
            flex-wrap: wrap;
            gap: 1rem;
        }}
        
        .header-left {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        
        .header-title {{
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--text);
        }}
        
        .header-stats {{
            display: flex;
            gap: 1.5rem;
            flex-wrap: wrap;
        }}
        
        /* ============================================
           DESIGN MINIMALISTA: BOTÕES DO HEADER
           Estilo unificado e coeso
           ============================================ */
        
        .header-actions {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 16px 0;
            margin-left: auto;
            flex-wrap: wrap;
        }}
        
        /* Estilo base de TODOS os botões */
        .action-header-btn {{
            /* Layout */
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 20px;
            
            /* Visual */
            background: white;
            border: 1.5px solid #E5E7EB;
            border-radius: 8px;
            
            /* Texto */
            font-size: 14px;
            font-weight: 500;
            color: #374151;
            text-decoration: none;
            
            /* Transição */
            transition: all 0.15s ease;
            cursor: pointer;
            
            /* Remove estilos padrão */
            outline: none;
        }}
        
        /* Ícone dentro do botão */
        .action-header-btn .icon {{
            font-size: 16px;
            opacity: 0.8;
        }}
        
        /* Hover - TODOS os botões */
        .action-header-btn:hover {{
            background: #F9FAFB;
            border-color: #4F46E5;
            color: #4F46E5;
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }}
        
        .action-header-btn:hover .icon {{
            opacity: 1;
        }}
        
        /* Active - TODOS os botões */
        .action-header-btn:active {{
            transform: translateY(0);
            box-shadow: none;
        }}
        
        /* Focus - TODOS os botões */
        .action-header-btn:focus-visible {{
            border-color: #4F46E5;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
        }}
        
        /* Diferenciação sutil por peso visual (opcional) */
        .action-header-btn.primary {{
            font-weight: 600;
        }}
        
        /* Responsividade */
        @media (max-width: 768px) {{
            .header-actions {{
                gap: 8px;
                padding: 12px 0;
            }}
            
            .action-header-btn {{
                padding: 8px 16px;
                font-size: 13px;
            }}
        }}
        
        @media (max-width: 480px) {{
            /* Em mobile, mostrar apenas ícones */
            .action-header-btn .text {{
                display: none;
            }}
            
            .action-header-btn .icon {{
                margin-right: 0;
                font-size: 18px;
            }}
            
            .action-header-btn {{
                padding: 10px;
                width: 44px;
                height: 44px;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
        }}
        
        .modal-large {{
            max-width: 1000px;
        }}
        
        .export-options {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
            padding: 1rem 0;
        }}
        
        .export-btn {{
            padding: 1.5rem;
            background: var(--surface);
            border: 2px solid var(--border);
            border-radius: 0.5rem;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.5rem;
            font-size: 1rem;
            color: var(--text);
        }}
        
        .export-btn:hover {{
            background: var(--primary);
            color: white;
            border-color: var(--primary);
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .export-btn i {{
            font-size: 2rem;
        }}
        
        /* Timeline Styles */
        .timeline-container {{
            padding: 1.5rem;
        }}
        
        .timeline-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid var(--border);
        }}
        
        .timeline-stats {{
            display: flex;
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }}
        
        .timeline-stat-item {{
            padding: 0.75rem 1rem;
            background: var(--bg);
            border-radius: 0.5rem;
            border-left: 4px solid var(--primary);
        }}
        
        .timeline-events {{
            max-height: 500px;
            overflow-y: auto;
        }}
        
        .timeline-event {{
            padding: 1rem;
            margin-bottom: 0.75rem;
            background: var(--bg);
            border-radius: 0.5rem;
            border-left: 4px solid var(--primary);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .timeline-event.critical {{
            border-left-color: var(--danger);
            background: #fee2e2;
        }}
        
        .timeline-time {{
            font-weight: 600;
            font-size: 1.125rem;
            color: var(--primary);
        }}
        
        .timeline-event-info {{
            flex: 1;
            margin-left: 1rem;
        }}
        
        /* Comparison Styles */
        .comparison-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }}
        
        .comparison-table th,
        .comparison-table td {{
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}
        
        .comparison-table th {{
            background: var(--primary);
            color: white;
            font-weight: 600;
        }}
        
        .comparison-table tr:hover {{
            background: var(--bg);
        }}
        
        .savings-section {{
            margin-top: 1.5rem;
            padding: 1rem;
            background: var(--bg);
            border-radius: 0.5rem;
        }}
        
        /* Tracking Styles */
        .tracking-vehicle {{
            padding: 1rem;
            margin-bottom: 1rem;
            background: var(--bg);
            border-radius: 0.5rem;
            border-left: 4px solid var(--primary);
        }}
        
        .tracking-status {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
        }}
        
        .progress-bar-tracking {{
            width: 100%;
            height: 20px;
            background: var(--border);
            border-radius: 10px;
            overflow: hidden;
            margin: 0.5rem 0;
        }}
        
        .progress-fill-tracking {{
            height: 100%;
            background: var(--primary);
            transition: width 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        
        .stat-badge {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.875rem;
            color: var(--text-light);
            position: relative;
            cursor: pointer;
            user-select: none;
            padding: 0.5rem 0.75rem;
            border-radius: 0.5rem;
            transition: all 0.2s ease;
        }}
        
        /* Hover state com feedback visual claro */
        .stat-badge:hover {{
            color: var(--primary);
            background: #EEF2FF;
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        /* Active state */
        .stat-badge:active {{
            transform: translateY(0);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
        }}
        
        /* Badge ativo (com dropdown aberto) */
        .stat-badge.active {{
            color: var(--primary);
            background: #EEF2FF;
        }}
        
        .stat-badge i {{
            color: var(--primary);
            transition: transform 0.2s;
        }}
        
        .stat-badge.active i {{
            transform: rotate(180deg);
        }}
        
        /* Indicador de dropdown (▼) */
        .stat-badge .dropdown-indicator {{
            font-size: 0.75rem;
            color: var(--text-light);
            margin-left: 0.25rem;
            transition: all 0.2s;
            opacity: 0.6;
        }}
        
        .stat-badge:hover .dropdown-indicator {{
            color: var(--primary);
            opacity: 1;
        }}
        
        .stat-badge.active .dropdown-indicator {{
            color: var(--primary);
            opacity: 1;
            transform: rotate(180deg);
        }}
        
        .stat-badge strong {{
            color: var(--text);
            margin-left: 0.25rem;
        }}
        
        /* Dropdowns Interativos */
        .dropdown {{
            display: none;
            position: absolute;
            top: calc(100% + 0.5rem);
            left: 50%;
            transform: translateX(-50%);
            background: var(--surface);
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1), 0 10px 15px -3px rgba(0,0,0,0.1);
            padding: 1.5rem;
            min-width: 400px;
            max-width: 600px;
            max-height: 500px;
            overflow-y: auto;
            z-index: 1000;
            animation: slideDown 0.3s;
        }}
        
        /* Ajuste para dropdowns próximos às bordas */
        .dropdown.dropdown-left {{
            left: 0;
            transform: translateX(0);
        }}
        
        .dropdown.dropdown-right {{
            left: auto;
            right: 0;
            transform: translateX(0);
        }}
        
        @keyframes slideDown {{
            from {{
                opacity: 0;
                transform: translateY(-10px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .dropdown.active {{
            display: block;
        }}
        
        .dropdown-header {{
            font-size: 1.125rem;
            font-weight: 600;
            margin-bottom: 1rem;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid var(--border);
        }}
        
        .vehicle-item, .delivery-item, .critical-item {{
            padding: 1rem;
            margin-bottom: 0.75rem;
            background: var(--bg);
            border-radius: 8px;
            border-left: 4px solid var(--primary);
        }}
        
        .vehicle-item-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.75rem;
        }}
        
        .vehicle-id {{
            font-weight: 600;
            font-size: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .vehicle-color-badge {{
            display: inline-block;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            border: 2px solid var(--border);
        }}
        
        .progress-bar-container {{
            margin: 0.5rem 0;
        }}
        
        .progress-label {{
            display: flex;
            justify-content: space-between;
            font-size: 0.75rem;
            color: var(--text-light);
            margin-bottom: 0.25rem;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 8px;
            background: var(--border);
            border-radius: 4px;
            overflow: hidden;
        }}
        
        .progress-fill {{
            height: 100%;
            transition: width 0.3s;
            border-radius: 4px;
        }}
        
        .progress-fill.ok {{
            background: var(--success);
        }}
        
        .progress-fill.warning {{
            background: var(--warning);
        }}
        
        .progress-fill.critical {{
            background: var(--danger);
        }}
        
        .status-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            padding: 0.25rem 0.5rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 500;
        }}
        
        .status-badge.ok {{
            background: #d1fae5;
            color: #065f46;
        }}
        
        .status-badge.warning {{
            background: #fef3c7;
            color: #92400e;
        }}
        
        .status-badge.critical {{
            background: #fee2e2;
            color: #991b1b;
        }}
        
        .delivery-list {{
            margin-top: 0.5rem;
            font-size: 0.875rem;
            color: var(--text-light);
        }}
        
        .delivery-list-item {{
            padding: 0.25rem 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .action-buttons {{
            display: flex;
            gap: 0.5rem;
            margin-top: 0.75rem;
            flex-wrap: wrap;
        }}
        
        .action-btn {{
            padding: 0.5rem 1rem;
            background: var(--primary);
            color: white;
            border: none;
            border-radius: 0.375rem;
            font-size: 0.75rem;
            cursor: pointer;
            transition: background 0.2s;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .action-btn:hover {{
            background: var(--primary-dark);
        }}
        
        .action-btn.secondary {{
            background: var(--surface);
            color: var(--text);
            border: 1px solid var(--border);
        }}
        
        .action-btn.secondary:hover {{
            background: var(--bg);
        }}
        
        .insights-section {{
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 2px solid var(--border);
        }}
        
        .insight-item {{
            padding: 0.75rem;
            margin-bottom: 0.5rem;
            background: var(--bg);
            border-radius: 6px;
            font-size: 0.875rem;
        }}
        
        .insight-item.warning {{
            border-left: 4px solid var(--warning);
        }}
        
        .insight-item.info {{
            border-left: 4px solid var(--primary);
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        /* Modal */
        .modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 2000;
            align-items: center;
            justify-content: center;
        }}
        
        .modal.active {{
            display: flex;
        }}
        
        .modal-content {{
            background: var(--surface);
            border-radius: 12px;
            padding: 2rem;
            max-width: 800px;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: var(--shadow-lg);
        }}
        
        .modal-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }}
        
        .modal-close {{
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: var(--text-light);
        }}
        
        .modal-close:hover {{
            color: var(--text);
        }}
        
        /* Responsivo */
        @media (max-width: 768px) {{
            .dropdown {{
                min-width: calc(100vw - 2rem);
                left: 50% !important;
                transform: translateX(-50%) !important;
                max-width: calc(100vw - 2rem);
            }}
        }}
        
        /* Click outside para fechar */
        .dropdown-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 999;
            display: none;
        }}
        
        .dropdown-overlay.active {{
            display: block;
        }}
        
        /* Main Layout */
        .main-layout {{
            display: flex;
            flex: 1;
            overflow: hidden;
        }}
        
        /* Mapa - 70% da tela */
        .map-section {{
            flex: 0 0 70%;
            display: flex;
            flex-direction: column;
            background: var(--surface);
            position: relative;
        }}
        
        .map-header {{
            padding: 0.75rem 1rem;
            background: var(--surface);
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .map-header h2 {{
            font-size: 1rem;
            font-weight: 600;
        }}
        
        .map-fullscreen-btn {{
            background: var(--primary);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 0.375rem;
            cursor: pointer;
            font-size: 0.875rem;
            transition: background 0.2s;
        }}
        
        .map-fullscreen-btn:hover {{
            background: var(--primary-dark);
        }}
        
        .map-container {{
            flex: 1;
            position: relative;
            overflow: hidden;
        }}
        
        .map-container iframe {{
            width: 100%;
            height: 100%;
            border: none;
        }}
        
        /* Sidebar - 30% da tela */
        .sidebar {{
            flex: 0 0 30%;
            display: flex;
            flex-direction: column;
            background: var(--surface);
            border-left: 1px solid var(--border);
            overflow: hidden;
        }}
        
        /* Chat Section */
        .chat-section {{
            flex: 1;
            display: flex;
            flex-direction: column;
            min-height: 0;
        }}
        
        .chat-header {{
            padding: 1rem;
            background: var(--surface);
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .chat-header h3 {{
            font-size: 1rem;
            font-weight: 600;
        }}
        
        .chat-toggle {{
            background: none;
            border: none;
            color: var(--text-light);
            cursor: pointer;
            padding: 0.25rem;
            font-size: 1.25rem;
        }}
        
        .chat-messages {{
            flex: 1;
            overflow-y: auto;
            padding: 1rem;
            background: var(--bg);
        }}
        
        .message {{
            margin-bottom: 1rem;
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
            max-width: 85%;
            padding: 0.75rem 1rem;
            border-radius: 1rem;
            word-wrap: break-word;
            line-height: 1.5;
        }}
        
        .message.user .message-bubble {{
            background: var(--primary);
            color: white;
            border-bottom-right-radius: 0.25rem;
        }}
        
        .message.assistant .message-bubble {{
            background: var(--surface);
            color: var(--text);
            border: 1px solid var(--border);
            border-bottom-left-radius: 0.25rem;
        }}
        
        .typing-indicator {{
            display: none;
            padding: 0.75rem 1rem;
            color: var(--text-light);
            font-size: 0.875rem;
            font-style: italic;
        }}
        
        .typing-indicator.active {{
            display: block;
        }}
        
        .typing-dots {{
            display: inline-block;
        }}
        
        .typing-dots span {{
            animation: typing 1.4s infinite;
            display: inline-block;
        }}
        
        .typing-dots span:nth-child(2) {{
            animation-delay: 0.2s;
        }}
        
        .typing-dots span:nth-child(3) {{
            animation-delay: 0.4s;
        }}
        
        @keyframes typing {{
            0%, 60%, 100% {{ transform: translateY(0); }}
            30% {{ transform: translateY(-10px); }}
        }}
        
        .chat-input-container {{
            padding: 1rem;
            background: var(--surface);
            border-top: 1px solid var(--border);
        }}
        
        .chat-input-wrapper {{
            display: flex;
            gap: 0.5rem;
            align-items: flex-end;
        }}
        
        .chat-input {{
            flex: 1;
            padding: 0.75rem;
            border: 1px solid var(--border);
            border-radius: 0.5rem;
            font-size: 0.875rem;
            resize: none;
            outline: none;
            transition: border-color 0.2s;
            font-family: inherit;
            max-height: 120px;
            overflow-y: auto;
        }}
        
        .chat-input:focus {{
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        }}
        
        .send-button {{
            background: var(--primary);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 0.5rem;
            cursor: pointer;
            font-weight: 500;
            transition: background 0.2s;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .send-button:hover:not(:disabled) {{
            background: var(--primary-dark);
        }}
        
        .send-button:disabled {{
            background: var(--secondary);
            cursor: not-allowed;
            opacity: 0.6;
        }}
        
        .quick-actions {{
            padding: 0.75rem 1rem;
            background: var(--bg);
            border-top: 1px solid var(--border);
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }}
        
        .quick-btn {{
            padding: 0.5rem 0.75rem;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 0.375rem;
            font-size: 0.75rem;
            cursor: pointer;
            transition: all 0.2s;
            color: var(--text);
        }}
        
        .quick-btn:hover {{
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }}
        
        /* Stats Section */
        .stats-section {{
            padding: 1rem;
            background: var(--bg);
            border-top: 1px solid var(--border);
            max-height: 200px;
            overflow-y: auto;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 0.75rem;
        }}
        
        .stat-card {{
            background: var(--surface);
            padding: 0.75rem;
            border-radius: 0.5rem;
            border: 1px solid var(--border);
        }}
        
        .stat-card-label {{
            font-size: 0.75rem;
            color: var(--text-light);
            margin-bottom: 0.25rem;
        }}
        
        .stat-card-value {{
            font-size: 1.125rem;
            font-weight: 600;
            color: var(--text);
        }}
        
        /* Scrollbar */
        .chat-messages::-webkit-scrollbar,
        .stats-section::-webkit-scrollbar {{
            width: 6px;
        }}
        
        .chat-messages::-webkit-scrollbar-track,
        .stats-section::-webkit-scrollbar-track {{
            background: transparent;
        }}
        
        .chat-messages::-webkit-scrollbar-thumb,
        .stats-section::-webkit-scrollbar-thumb {{
            background: var(--border);
            border-radius: 3px;
        }}
        
        .chat-messages::-webkit-scrollbar-thumb:hover,
        .stats-section::-webkit-scrollbar-thumb:hover {{
            background: var(--secondary);
        }}
        
        /* Responsive */
        @media (max-width: 1024px) {{
            .main-layout {{
                flex-direction: column;
            }}
            
            .map-section {{
                flex: 0 0 60%;
            }}
            
            .sidebar {{
                flex: 0 0 40%;
            }}
        }}
        
        /* Fullscreen map */
        .map-fullscreen {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 1000;
            background: var(--surface);
        }}
        
        .map-fullscreen .map-header {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1001;
        }}
        
        .map-fullscreen .map-container {{
            height: 100vh;
        }}
    </style>
</head>
<body>
    <div class="app-container">
        <!-- Header -->
        <div class="header">
            <div class="header-left">
                <h1 class="header-title">
                    <i class="fas fa-route"></i> Sistema de Rotas Hospitalares
                </h1>
            </div>
            <div class="header-stats">
                <!-- Badge Veículos com Dropdown -->
                <div class="stat-badge" onclick="toggleDropdown('vehicles')" id="badge-vehicles">
                    <i class="fas fa-truck"></i>
                    <span>{self.stats['num_vehicles']} Veículos</span>
                    <span class="dropdown-indicator">▼</span>
                    <div class="dropdown" id="dropdown-vehicles">
                        <div class="dropdown-header">🚚 Veículos ({self.stats['num_vehicles']})</div>
                        <div id="vehicles-list">
                            <!-- Preenchido via JavaScript -->
                        </div>
                        <div class="insights-section" id="vehicles-insights">
                            <!-- Insights preenchidos via JavaScript -->
                        </div>
                    </div>
                </div>
                
                <!-- Badge Entregas com Dropdown -->
                <div class="stat-badge" onclick="toggleDropdown('deliveries')" id="badge-deliveries">
                    <i class="fas fa-box"></i>
                    <span>{self.stats['num_deliveries']} Entregas</span>
                    <span class="dropdown-indicator">▼</span>
                    <div class="dropdown" id="dropdown-deliveries">
                        <div class="dropdown-header">📦 Entregas ({self.stats['num_deliveries']})</div>
                        <div id="deliveries-list">
                            <!-- Preenchido via JavaScript -->
                        </div>
                    </div>
                </div>
                
                <!-- Badge Críticas com Dropdown -->
                <div class="stat-badge" onclick="toggleDropdown('critical')" id="badge-critical">
                    <i class="fas fa-exclamation-triangle"></i>
                    <span>{self.stats['critical_deliveries']} Críticas</span>
                    <span class="dropdown-indicator">▼</span>
                    <div class="dropdown" id="dropdown-critical">
                        <div class="dropdown-header">⚠️ Entregas Críticas ({self.stats['critical_deliveries']})</div>
                        <div id="critical-list">
                            <!-- Preenchido via JavaScript -->
                        </div>
                    </div>
                </div>
                
                <!-- Badges informativos (sem dropdown) -->
                <div class="stat-badge">
                    <i class="fas fa-route"></i>
                    <span><strong>{self.stats['total_distance']:.1f} km</strong></span>
                </div>
                <div class="stat-badge">
                    <i class="fas fa-dollar-sign"></i>
                    <span><strong>R$ {self.stats['total_cost']:.2f}</strong></span>
                </div>
            </div>
            
            <!-- Botões de Ação - Design Minimalista e Coeso -->
            <div class="header-actions">
                <button 
                    class="action-header-btn primary" 
                    onclick="showTimeline()" 
                    aria-label="Ver timeline de entregas"
                    title="Visualizar linha do tempo das entregas"
                >
                    <span class="icon"><i class="fas fa-calendar-alt"></i></span>
                    <span class="text">Timeline</span>
                </button>
                
                <button 
                    class="action-header-btn" 
                    onclick="showComparison()" 
                    aria-label="Comparar cenários de otimização"
                    title="Comparar diferentes cenários de otimização"
                >
                    <span class="icon"><i class="fas fa-balance-scale"></i></span>
                    <span class="text">Comparar</span>
                </button>
                
                <button 
                    class="action-header-btn" 
                    onclick="showTracking()" 
                    aria-label="Rastrear veículos em tempo real"
                    title="Rastrear veículos em tempo real"
                >
                    <span class="icon"><i class="fas fa-map-marker-alt"></i></span>
                    <span class="text">Rastrear</span>
                </button>
                
                <button 
                    class="action-header-btn" 
                    onclick="showExportMenu()" 
                    aria-label="Exportar relatórios"
                    title="Exportar relatórios em diferentes formatos"
                >
                    <span class="icon"><i class="fas fa-download"></i></span>
                    <span class="text">Exportar</span>
                </button>
            </div>
            
            <!-- Overlay para fechar dropdowns ao clicar fora -->
            <div class="dropdown-overlay" id="dropdown-overlay" onclick="closeAllDropdowns()"></div>
            
            <!-- Modal para detalhes completos -->
            <div class="modal" id="details-modal">
                <div class="modal-content">
                    <div class="modal-header">
                        <h2 id="modal-title">Detalhes</h2>
                        <button class="modal-close" onclick="closeModal()">&times;</button>
                    </div>
                    <div id="modal-body">
                        <!-- Conteúdo preenchido via JavaScript -->
                    </div>
                </div>
            </div>
            
            <!-- Modal Timeline -->
            <div class="modal modal-large" id="timeline-modal">
                <div class="modal-content">
                    <div class="modal-header">
                        <h2>📅 Timeline de Entregas</h2>
                        <button class="modal-close" onclick="closeModal('timeline-modal')">&times;</button>
                    </div>
                    <div id="timeline-body">
                        <!-- Conteúdo preenchido via JavaScript -->
                    </div>
                </div>
            </div>
            
            <!-- Modal Comparação -->
            <div class="modal modal-large" id="comparison-modal">
                <div class="modal-content">
                    <div class="modal-header">
                        <h2>⚖️ Comparação de Cenários</h2>
                        <button class="modal-close" onclick="closeModal('comparison-modal')">&times;</button>
                    </div>
                    <div id="comparison-body">
                        <!-- Conteúdo preenchido via JavaScript -->
                    </div>
                </div>
            </div>
            
            <!-- Modal Rastreamento -->
            <div class="modal modal-large" id="tracking-modal">
                <div class="modal-content">
                    <div class="modal-header">
                        <h2>📍 Rastreamento em Tempo Real</h2>
                        <button class="modal-close" onclick="closeModal('tracking-modal')">&times;</button>
                    </div>
                    <div id="tracking-body">
                        <!-- Conteúdo preenchido via JavaScript -->
                    </div>
                </div>
            </div>
            
            <!-- Modal Exportação -->
            <div class="modal" id="export-modal">
                <div class="modal-content">
                    <div class="modal-header">
                        <h2>📥 Exportar Relatórios</h2>
                        <button class="modal-close" onclick="closeModal('export-modal')">&times;</button>
                    </div>
                    <div id="export-body">
                        <!-- Conteúdo preenchido via JavaScript -->
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Main Layout -->
        <div class="main-layout">
            <!-- Mapa (70%) -->
            <div class="map-section" id="map-section">
                <div class="map-header">
                    <h2><i class="fas fa-map"></i> Mapa das Rotas Otimizadas</h2>
                    <button class="map-fullscreen-btn" onclick="toggleFullscreen()">
                        <i class="fas fa-expand"></i> Tela Cheia
                    </button>
                </div>
                <div class="map-container">
                    <iframe src="{map_path}" title="Mapa de Rotas" id="map-iframe"></iframe>
                </div>
            </div>
            
            <!-- Sidebar (30%) -->
            <div class="sidebar">
                <!-- Chat Section -->
                <div class="chat-section">
                    <div class="chat-header">
                        <h3><i class="fas fa-robot"></i> Assistente Inteligente</h3>
                        <button class="chat-toggle" onclick="clearChat()" title="Limpar chat">
                            <i class="fas fa-trash-alt"></i>
                        </button>
                    </div>
                    <div class="chat-messages" id="chat-messages">
                        <div class="message assistant">
                            <div class="message-bubble">
                                <strong>🤖 Assistente:</strong> Olá! Sou seu assistente para otimização de rotas hospitalares. 
                                Posso ajudar com informações sobre rotas, entregas, veículos, análises e muito mais. 
                                Faça sua pergunta!
                            </div>
                        </div>
                    </div>
                    <div class="typing-indicator" id="typing-indicator">
                        <div class="message assistant">
                            <div class="message-bubble">
                                Assistente está digitando<span class="typing-dots"><span>.</span><span>.</span><span>.</span></span>
                            </div>
                        </div>
                    </div>
                    <div class="chat-input-container">
                        <div class="chat-input-wrapper">
                            <textarea 
                                class="chat-input" 
                                id="chat-input" 
                                placeholder="Digite sua pergunta..."
                                rows="1"
                                onkeydown="handleKeyDown(event)"
                            ></textarea>
                            <button class="send-button" onclick="sendMessage()" id="send-btn">
                                <i class="fas fa-paper-plane"></i> Enviar
                            </button>
                        </div>
                        <div class="quick-actions">
                            <button class="quick-btn" onclick="askQuick('Quantos veículos foram usados?')">
                                Veículos
                            </button>
                            <button class="quick-btn" onclick="askQuick('Há entregas críticas?')">
                                Críticas
                            </button>
                            <button class="quick-btn" onclick="askQuick('Qual a distância total?')">
                                Distância
                            </button>
                            <button class="quick-btn" onclick="askQuick('Analise a eficiência das rotas')">
                                Análise
                            </button>
                        </div>
                    </div>
                </div>
                
                <!-- Stats Section -->
                <div class="stats-section">
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-card-label">Distância Total</div>
                            <div class="stat-card-value">{self.stats['total_distance']:.2f} km</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-card-label">Custo Total</div>
                            <div class="stat-card-value">R$ {self.stats['total_cost']:.2f}</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-card-label">Tempo Execução</div>
                            <div class="stat-card-value">{self.stats['execution_time']:.2f}s</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-card-label">Fitness Score</div>
                            <div class="stat-card-value">{self.stats['fitness_score']:.2f}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Configuração
        const API_URL = '{api_url}';
        const driversData = {drivers_json};
        const criticalData = {critical_json};
        const allDeliveriesData = {all_deliveries_json};
        const statsData = {stats_json};
        
        // Estado
        let conversationHistory = [];
        let isProcessing = false;
        let chatInitialized = false;
        let openDropdown = null;
        
        // Inicializar
        document.addEventListener('DOMContentLoaded', function() {{
            initializeChat();
            autoResizeTextarea();
            renderDropdowns();
        }});
        
        // Renderizar dropdowns
        function renderDropdowns() {{
            renderVehiclesDropdown();
            renderDeliveriesDropdown();
            renderCriticalDropdown();
        }}
        
        // Toggle dropdown
        function toggleDropdown(type) {{
            const badge = document.getElementById(`badge-${{type}}`);
            const dropdown = document.getElementById(`dropdown-${{type}}`);
            const overlay = document.getElementById('dropdown-overlay');
            
            if (openDropdown === type) {{
                // Fechar
                badge.classList.remove('active');
                dropdown.classList.remove('active');
                overlay.classList.remove('active');
                openDropdown = null;
            }} else {{
                // Fechar anterior e abrir novo
                closeAllDropdowns();
                
                badge.classList.add('active');
                dropdown.classList.add('active');
                overlay.classList.add('active');
                openDropdown = type;
                
                // Ajustar posicionamento do dropdown
                adjustDropdownPosition(dropdown, badge);
            }}
        }}
        
        // Ajustar posicionamento do dropdown para não ultrapassar limites da tela
        function adjustDropdownPosition(dropdown, badge) {{
            // Remover classes de posicionamento anteriores
            dropdown.classList.remove('dropdown-left', 'dropdown-right');
            
            // Resetar estilos inline
            dropdown.style.top = '';
            dropdown.style.bottom = '';
            
            // Aguardar renderização
            setTimeout(() => {{
                const badgeRect = badge.getBoundingClientRect();
                const dropdownRect = dropdown.getBoundingClientRect();
                const viewportWidth = window.innerWidth;
                const viewportHeight = window.innerHeight;
                
                // Calcular posição central do badge
                const badgeCenterX = badgeRect.left + (badgeRect.width / 2);
                const dropdownHalfWidth = dropdownRect.width / 2;
                
                // Verificar se ultrapassa à esquerda
                if (badgeCenterX - dropdownHalfWidth < 10) {{
                    dropdown.classList.add('dropdown-left');
                }}
                // Verificar se ultrapassa à direita
                else if (badgeCenterX + dropdownHalfWidth > viewportWidth - 10) {{
                    dropdown.classList.add('dropdown-right');
                }}
                
                // Verificar se ultrapassa na parte inferior
                if (dropdownRect.bottom > viewportHeight - 10) {{
                    // Ajustar para aparecer acima do badge
                    dropdown.style.top = 'auto';
                    dropdown.style.bottom = 'calc(100% + 0.5rem)';
                }} else {{
                    dropdown.style.top = 'calc(100% + 0.5rem)';
                    dropdown.style.bottom = 'auto';
                }}
            }}, 10);
        }}
        
        // Ajustar posição ao redimensionar janela
        window.addEventListener('resize', function() {{
            if (openDropdown) {{
                const badge = document.getElementById(`badge-${{openDropdown}}`);
                const dropdown = document.getElementById(`dropdown-${{openDropdown}}`);
                if (badge && dropdown && dropdown.classList.contains('active')) {{
                    adjustDropdownPosition(dropdown, badge);
                }}
            }}
        }});
        
        // Fechar todos os dropdowns
        function closeAllDropdowns() {{
            document.querySelectorAll('.stat-badge').forEach(badge => {{
                badge.classList.remove('active');
            }});
            document.querySelectorAll('.dropdown').forEach(dropdown => {{
                dropdown.classList.remove('active');
            }});
            document.getElementById('dropdown-overlay').classList.remove('active');
            openDropdown = null;
        }}
        
        // Renderizar dropdown de veículos
        function renderVehiclesDropdown() {{
            const container = document.getElementById('vehicles-list');
            if (!container) return;
            container.innerHTML = '';
            
            driversData.forEach(vehicle => {{
                const item = document.createElement('div');
                item.className = 'vehicle-item';
                item.style.borderLeftColor = getColorCode(vehicle.color);
                
                const statusIcon = vehicle.range_status === 'ok' ? '✅' : 
                                  vehicle.range_status === 'warning' ? '⚠️' : '🚨';
                
                item.innerHTML = `
                    <div class="vehicle-item-header">
                        <div class="vehicle-id">
                            Veículo ${{vehicle.driver_id}}
                            <span class="vehicle-color-badge" style="background-color: ${{getColorCode(vehicle.color)}}"></span>
                        </div>
                        <span class="status-badge ${{vehicle.range_status}}">
                            ${{statusIcon}} ${{vehicle.range_status === 'ok' ? 'OK' : vehicle.range_status === 'warning' ? 'Atenção' : 'Crítico'}}
                        </span>
                    </div>
                    
                    <div class="progress-bar-container">
                        <div class="progress-label">
                            <span>Capacidade</span>
                            <span>${{vehicle.total_weight.toFixed(1)}} / ${{vehicle.max_capacity.toFixed(1)}} kg (${{vehicle.capacity_percent.toFixed(1)}}%)</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill ${{vehicle.capacity_status}}" style="width: ${{Math.min(vehicle.capacity_percent, 100)}}%"></div>
                        </div>
                    </div>
                    
                    <div class="progress-bar-container">
                        <div class="progress-label">
                            <span>Autonomia</span>
                            <span>${{vehicle.distance.toFixed(2)}} / ${{vehicle.max_range.toFixed(1)}} km (${{vehicle.range_percent.toFixed(1)}}%)</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill ${{vehicle.range_status}}" style="width: ${{Math.min(vehicle.range_percent, 100)}}%"></div>
                        </div>
                    </div>
                    
                    <div style="margin-top: 0.5rem; font-size: 0.875rem; color: var(--text-light);">
                        <div>📦 ${{vehicle.num_deliveries}} entregas (${{vehicle.critical_deliveries}} críticas)</div>
                        <div>💰 Custo: R$ ${{vehicle.cost.toFixed(2)}}</div>
                    </div>
                    
                    <div class="delivery-list">
                        <strong>Entregas:</strong>
                        <div style="margin-top: 0.25rem;">
                            ${{vehicle.route.map(id => `<div class="delivery-list-item"><i class="fas fa-map-marker-alt"></i> ${{id}}</div>`).join('')}}
                        </div>
                    </div>
                    
                    <div class="action-buttons">
                        <button class="action-btn" onclick="highlightRoute(${{vehicle.driver_id}})">
                            <i class="fas fa-eye"></i> Ver Rota no Mapa
                        </button>
                        <button class="action-btn secondary" onclick="showVehicleDetails(${{vehicle.driver_id}})">
                            <i class="fas fa-chart-bar"></i> Detalhes Completos
                        </button>
                    </div>
                `;
                
                container.appendChild(item);
            }});
            
            // Renderizar insights
            renderVehicleInsights();
        }}
        
        // Renderizar insights de veículos
        function renderVehicleInsights() {{
            const container = document.getElementById('vehicles-insights');
            if (!container) return;
            container.innerHTML = '<div class="dropdown-header" style="margin-top: 0;">💡 Insights</div>';
            
            const insights = [];
            
            // Veículos próximos do limite de autonomia
            const highRange = driversData.filter(v => v.range_percent > 90);
            if (highRange.length > 0) {{
                insights.push({{
                    type: 'warning',
                    message: `⚠️ ${{highRange.length}} veículo(s) próximo(s) do limite de autonomia (>90%): ${{highRange.map(v => `Veículo ${{v.driver_id}}`).join(', ')}}`
                }});
            }}
            
            // Veículos subutilizados
            const underutilized = driversData.filter(v => v.capacity_percent < 70);
            if (underutilized.length > 0) {{
                insights.push({{
                    type: 'info',
                    message: `ℹ️ ${{underutilized.length}} veículo(s) subutilizado(s) (<70% capacidade): ${{underutilized.map(v => `Veículo ${{v.driver_id}}`).join(', ')}}`
                }});
            }}
            
            // Sugestões de rebalanceamento
            if (driversData.length > 1) {{
                const avgCapacity = driversData.reduce((sum, v) => sum + v.capacity_percent, 0) / driversData.length;
                const unbalanced = driversData.filter(v => Math.abs(v.capacity_percent - avgCapacity) > 15);
                if (unbalanced.length > 0) {{
                    insights.push({{
                        type: 'info',
                        message: `💡 Considere rebalancear carga entre veículos para melhor distribuição`
                    }});
                }}
            }}
            
            if (insights.length === 0) {{
                insights.push({{
                    type: 'info',
                    message: '✅ Todos os veículos estão bem balanceados!'
                }});
            }}
            
            insights.forEach(insight => {{
                const item = document.createElement('div');
                item.className = `insight-item ${{insight.type}}`;
                item.textContent = insight.message;
                container.appendChild(item);
            }});
        }}
        
        // Renderizar dropdown de entregas
        function renderDeliveriesDropdown() {{
            const container = document.getElementById('deliveries-list');
            if (!container) return;
            container.innerHTML = '';
            
            allDeliveriesData.forEach(delivery => {{
                const item = document.createElement('div');
                item.className = 'delivery-item';
                
                const badge = delivery.is_critical 
                    ? '<span class="status-badge critical">⚠️ CRÍTICA</span>'
                    : '<span class="status-badge ok">✓ Normal</span>';
                
                item.innerHTML = `
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <div style="font-weight: 600;">${{delivery.id}}</div>
                        ${{badge}}
                    </div>
                    <div style="font-size: 0.875rem; color: var(--text-light);">
                        <div>📍 Localização: (${{delivery.location[0].toFixed(4)}}, ${{delivery.location[1].toFixed(4)}})</div>
                        <div>⚖️ Peso: ${{delivery.weight}} kg</div>
                        <div>🔢 Prioridade: ${{delivery.priority}}</div>
                    </div>
                    <div class="action-buttons">
                        <button class="action-btn secondary" onclick="showDeliveryOnMap([${{delivery.location[0]}}, ${{delivery.location[1]}}])">
                            <i class="fas fa-map-marker-alt"></i> Ver no Mapa
                        </button>
                    </div>
                `;
                
                container.appendChild(item);
            }});
        }}
        
        // Renderizar dropdown de críticas
        function renderCriticalDropdown() {{
            const container = document.getElementById('critical-list');
            if (!container) return;
            container.innerHTML = '';
            
            if (criticalData.length === 0) {{
                container.innerHTML = '<div style="text-align: center; padding: 2rem; color: var(--text-light);">Nenhuma entrega crítica</div>';
                return;
            }}
            
            criticalData.forEach(delivery => {{
                const item = document.createElement('div');
                item.className = 'critical-item';
                item.style.borderLeftColor = getColorCode(delivery.vehicle_color);
                
                item.innerHTML = `
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <div style="font-weight: 600; font-size: 1rem;">${{delivery.id}}</div>
                        <span class="status-badge critical">⚠️ CRÍTICA</span>
                    </div>
                    <div style="font-size: 0.875rem; color: var(--text-light); margin-bottom: 0.5rem;">
                        <div>📍 Localização: (${{delivery.location[0].toFixed(4)}}, ${{delivery.location[1].toFixed(4)}})</div>
                        <div>⚖️ Peso: ${{delivery.weight}} kg</div>
                        ${{delivery.vehicle_id ? `<div>🚚 Veículo: <span style="color: ${{getColorCode(delivery.vehicle_color)}}; font-weight: 600;">Veículo ${{delivery.vehicle_id}}</span></div>` : '<div>⚠️ Não atribuída a nenhum veículo</div>'}}
                    </div>
                    <div class="action-buttons">
                        <button class="action-btn" onclick="showDeliveryOnMap([${{delivery.location[0]}}, ${{delivery.location[1]}}])">
                            <i class="fas fa-map-marker-alt"></i> Ver no Mapa
                        </button>
                        ${{delivery.vehicle_id ? `<button class="action-btn secondary" onclick="highlightRoute(${{delivery.vehicle_id}})"><i class="fas fa-route"></i> Ver Rota do Veículo</button>` : ''}}
                    </div>
                `;
                
                container.appendChild(item);
            }});
        }}
        
        // Funções auxiliares
        function getColorCode(colorName) {{
            const colors = {{
                'blue': '#3b82f6',
                'red': '#ef4444',
                'green': '#10b981',
                'purple': '#a855f7',
                'orange': '#f59e0b',
                'darkred': '#dc2626',
                'lightred': '#f87171',
                'beige': '#f5f5dc',
                'darkblue': '#1e40af',
                'darkgreen': '#059669',
                'cadetblue': '#5f9ea0',
                'darkpurple': '#7c3aed',
                'white': '#ffffff',
                'pink': '#ec4899',
                'lightblue': '#60a5fa',
                'lightgreen': '#34d399',
                'gray': '#6b7280',
                'black': '#000000',
                'lightgray': '#d1d5db',
            }};
            return colors[colorName] || '#6b7280';
        }}
        
        // Destacar rota no mapa
        function highlightRoute(vehicleId) {{
            const mapIframe = document.getElementById('map-iframe');
            if (!mapIframe) {{
                console.warn('Mapa não encontrado');
                return;
            }}
            
            // Enviar mensagem para o iframe do mapa
            mapIframe.contentWindow.postMessage({{
                type: 'highlight_route',
                vehicle_id: vehicleId
            }}, '*');
            
            closeAllDropdowns();
        }}
        
        // Restaurar todas as rotas no mapa
        function restoreAllRoutes() {{
            const mapIframe = document.getElementById('map-iframe');
            if (!mapIframe) return;
            
            mapIframe.contentWindow.postMessage({{
                type: 'restore_routes'
            }}, '*');
        }}
        
        // Mostrar detalhes do veículo
        function showVehicleDetails(vehicleId) {{
            const vehicle = driversData.find(v => v.driver_id === vehicleId);
            if (!vehicle) return;
            
            const modal = document.getElementById('details-modal');
            const title = document.getElementById('modal-title');
            const body = document.getElementById('modal-body');
            
            title.textContent = `Veículo ${{vehicleId}} - Detalhes Completos`;
            
            body.innerHTML = `
                <div style="display: grid; gap: 1rem;">
                    <div>
                        <h3 style="margin-bottom: 0.5rem;">Informações Gerais</h3>
                        <div style="background: var(--bg); padding: 1rem; border-radius: 8px;">
                            <div><strong>ID:</strong> Veículo ${{vehicleId}}</div>
                            <div><strong>Cor:</strong> <span style="display: inline-block; width: 20px; height: 20px; background: ${{getColorCode(vehicle.color)}}; border-radius: 50%; border: 2px solid var(--border);"></span> ${{vehicle.color}}</div>
                            <div><strong>Número de Entregas:</strong> ${{vehicle.num_deliveries}}</div>
                            <div><strong>Entregas Críticas:</strong> ${{vehicle.critical_deliveries}}</div>
                        </div>
                    </div>
                    
                    <div>
                        <h3 style="margin-bottom: 0.5rem;">Capacidade</h3>
                        <div style="background: var(--bg); padding: 1rem; border-radius: 8px;">
                            <div><strong>Peso Total:</strong> ${{vehicle.total_weight.toFixed(2)}} kg</div>
                            <div><strong>Capacidade Máxima:</strong> ${{vehicle.max_capacity.toFixed(2)}} kg</div>
                            <div><strong>Utilização:</strong> ${{vehicle.capacity_percent.toFixed(1)}}%</div>
                            <div><strong>Status:</strong> <span class="status-badge ${{vehicle.capacity_status}}">${{vehicle.capacity_status === 'ok' ? 'OK' : vehicle.capacity_status === 'warning' ? 'Atenção' : 'Crítico'}}</span></div>
                        </div>
                    </div>
                    
                    <div>
                        <h3 style="margin-bottom: 0.5rem;">Autonomia</h3>
                        <div style="background: var(--bg); padding: 1rem; border-radius: 8px;">
                            <div><strong>Distância Percorrida:</strong> ${{vehicle.distance.toFixed(2)}} km</div>
                            <div><strong>Autonomia Máxima:</strong> ${{vehicle.max_range.toFixed(2)}} km</div>
                            <div><strong>Utilização:</strong> ${{vehicle.range_percent.toFixed(1)}}%</div>
                            <div><strong>Status:</strong> <span class="status-badge ${{vehicle.range_status}}">${{vehicle.range_status === 'ok' ? 'OK' : vehicle.range_status === 'warning' ? 'Atenção' : 'Crítico'}}</span></div>
                        </div>
                    </div>
                    
                    <div>
                        <h3 style="margin-bottom: 0.5rem;">Custo</h3>
                        <div style="background: var(--bg); padding: 1rem; border-radius: 8px;">
                            <div><strong>Custo Estimado:</strong> R$ ${{vehicle.cost.toFixed(2)}}</div>
                        </div>
                    </div>
                    
                    <div>
                        <h3 style="margin-bottom: 0.5rem;">Rota Completa</h3>
                        <div style="background: var(--bg); padding: 1rem; border-radius: 8px;">
                            <div style="font-family: monospace; font-size: 0.875rem;">
                                Depósito → ${{vehicle.route.join(' → ')}} → Depósito
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            modal.classList.add('active');
            closeAllDropdowns();
        }}
        
        // Mostrar entrega no mapa
        function showDeliveryOnMap(location) {{
            const mapIframe = document.getElementById('map-iframe');
            if (!mapIframe) {{
                console.warn('Mapa não encontrado');
                alert(`Centralizando mapa na localização: (${{location[0].toFixed(4)}}, ${{location[1].toFixed(4)}})\\n\\nErro: Mapa não encontrado.`);
                return;
            }}
            
            // Garantir que o iframe está carregado
            if (!mapIframe.contentWindow) {{
                console.warn('Iframe ainda não carregado, aguardando...');
                setTimeout(() => showDeliveryOnMap(location), 500);
                return;
            }}
            
            // Validar formato da localização [latitude, longitude]
            if (!Array.isArray(location) || location.length !== 2) {{
                console.error('Formato de localização inválido:', location);
                alert('Erro: Formato de localização inválido.');
                return;
            }}
            
            console.log('Enviando localização para o mapa:', location);
            
            // Enviar mensagem para o iframe do mapa
            try {{
                mapIframe.contentWindow.postMessage({{
                    type: 'show_delivery',
                    location: [parseFloat(location[0]), parseFloat(location[1])]
                }}, '*');
                
                console.log('Mensagem enviada com sucesso');
            }} catch (error) {{
                console.error('Erro ao enviar mensagem para o mapa:', error);
                alert('Erro ao comunicar com o mapa. Tente recarregar a página.');
            }}
            
            closeAllDropdowns();
        }}
        
        // Fechar modal
        function closeModal(modalId = 'details-modal') {{
            document.getElementById(modalId).classList.remove('active');
            if (window.trackingInterval) {{
                clearInterval(window.trackingInterval);
                window.trackingInterval = null;
            }}
        }}
        
        // Mostrar Timeline
        function showTimeline() {{
            const modal = document.getElementById('timeline-modal');
            const body = document.getElementById('timeline-body');
            
            // Simular dados da timeline (em produção, viria do backend)
            const timelineData = generateTimelineData();
            
            body.innerHTML = `
                <div class="timeline-container">
                    <div class="timeline-header">
                        <h3>📅 Timeline de Entregas - ${{new Date().toLocaleDateString('pt-BR')}}</h3>
                        <div>
                            <button class="action-btn secondary" onclick="exportTimeline()">
                                <i class="fas fa-download"></i> Exportar
                            </button>
                        </div>
                    </div>
                    
                    <div class="timeline-stats">
                        <div class="timeline-stat-item">
                            <strong>✅ ${{timelineData.onTime}}</strong> dentro do prazo
                        </div>
                        <div class="timeline-stat-item">
                            <strong>⚠️ ${{timelineData.nearLimit}}</strong> próximas ao limite
                        </div>
                        <div class="timeline-stat-item">
                            <strong>🚨 ${{timelineData.late}}</strong> atrasadas
                        </div>
                    </div>
                    
                    <div class="timeline-events">
                        ${{timelineData.events.map(event => `
                            <div class="timeline-event ${{event.isCritical ? 'critical' : ''}}">
                                <div class="timeline-time">${{event.time}}</div>
                                <div class="timeline-event-info">
                                    <div><strong>${{event.vehicle}}</strong> → ${{event.deliveryId}} ${{event.isCritical ? '⚠️ CRÍTICA' : ''}}</div>
                                    <div style="font-size: 0.875rem; color: var(--text-light);">${{event.location}}</div>
                                </div>
                            </div>
                        `).join('')}}
                    </div>
                </div>
            `;
            
            modal.classList.add('active');
        }}
        
        // Gerar dados da timeline (simulado)
        function generateTimelineData() {{
            const events = [];
            const vehicles = ['🔵 V1', '🔴 V2', '🟢 V3'];
            const deliveries = ['D001', 'D002', 'D003', 'D004', 'D005', 'D006'];
            const locations = ['Hospital das Clínicas', 'Hospital Sírio-Libanês', 'Santa Casa', 'Hospital Einstein', 'Hospital Israelita', 'Hospital Alemão'];
            
            let currentTime = new Date();
            currentTime.setHours(9, 0, 0, 0);
            
            for (let i = 0; i < 12; i++) {{
                const vehicleIdx = i % 3;
                const deliveryIdx = i % 6;
                const isCritical = i % 3 === 0;
                
                events.push({{
                    time: currentTime.toLocaleTimeString('pt-BR', {{hour: '2-digit', minute: '2-digit'}}),
                    vehicle: vehicles[vehicleIdx],
                    deliveryId: deliveries[deliveryIdx],
                    location: locations[deliveryIdx],
                    isCritical: isCritical,
                }});
                
                currentTime.setMinutes(currentTime.getMinutes() + 15);
            }}
            
            return {{
                events: events,
                onTime: 10,
                nearLimit: 2,
                late: 0,
            }};
        }}
        
        // Mostrar Comparação
        function showComparison() {{
            const modal = document.getElementById('comparison-modal');
            const body = document.getElementById('comparison-body');
            
            // Simular dados de comparação (em produção, viria do backend)
            const comparisonData = {{
                distance: {{current: 81.7, greedy: 95.3, baseline: 120.5}},
                cost: {{current: 299, greedy: 340, baseline: 450}},
                vehicles: {{current: 3, greedy: 3, baseline: 4}},
                time: {{current: 3.2, greedy: 3.8, baseline: 5.1}},
                violations: {{current: 0, greedy: 1, baseline: 3}},
            }};
            
            const savings = {{
                vsGreedy: {{cost: 41, percent: 12.1, distance: 13.6}},
                vsBaseline: {{cost: 151, percent: 33.6, distance: 38.8, co2: 9.2}},
            }};
            
            body.innerHTML = `
                <div style="padding: 1.5rem;">
                    <table class="comparison-table">
                        <thead>
                            <tr>
                                <th>Métrica</th>
                                <th>Atual</th>
                                <th>Greedy</th>
                                <th>Baseline</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>📏 Distância Total</td>
                                <td><strong>${{comparisonData.distance.current}} km</strong></td>
                                <td>${{comparisonData.distance.greedy}} km</td>
                                <td>${{comparisonData.distance.baseline}} km</td>
                            </tr>
                            <tr>
                                <td>💰 Custo Total</td>
                                <td><strong>R$ ${{comparisonData.cost.current}}</strong></td>
                                <td>R$ ${{comparisonData.cost.greedy}}</td>
                                <td>R$ ${{comparisonData.cost.baseline}}</td>
                            </tr>
                            <tr>
                                <td>🚚 Veículos Usados</td>
                                <td><strong>${{comparisonData.vehicles.current}}</strong></td>
                                <td>${{comparisonData.vehicles.greedy}}</td>
                                <td>${{comparisonData.vehicles.baseline}}</td>
                            </tr>
                            <tr>
                                <td>⏱️ Tempo Entrega</td>
                                <td><strong>${{comparisonData.time.current}}h</strong></td>
                                <td>${{comparisonData.time.greedy}}h</td>
                                <td>${{comparisonData.time.baseline}}h</td>
                            </tr>
                            <tr>
                                <td>⚠️ Violações</td>
                                <td><strong>${{comparisonData.violations.current}}</strong></td>
                                <td>${{comparisonData.violations.greedy}}</td>
                                <td>${{comparisonData.violations.baseline}}</td>
                            </tr>
                        </tbody>
                    </table>
                    
                    <div class="savings-section">
                        <h3>📊 ECONOMIA GERADA:</h3>
                        <ul style="list-style: none; padding: 0;">
                            <li style="margin: 0.5rem 0;">• vs. Greedy: R$ ${{savings.vsGreedy.cost}} (${{savings.vsGreedy.percent}}% melhor) ✅</li>
                            <li style="margin: 0.5rem 0;">• vs. Baseline: R$ ${{savings.vsBaseline.cost}} (${{savings.vsBaseline.percent}}% melhor) ✅</li>
                            <li style="margin: 0.5rem 0;">• Distância economizada: ${{savings.vsBaseline.distance}} km</li>
                            <li style="margin: 0.5rem 0;">• CO₂ evitado: ~${{savings.vsBaseline.co2}} kg 🌱</li>
                        </ul>
                    </div>
                    
                    <div style="margin-top: 1.5rem; display: flex; gap: 1rem;">
                        <button class="action-btn" onclick="alert('Funcionalidade de gráfico em desenvolvimento')">
                            <i class="fas fa-chart-bar"></i> Visualizar Gráfico
                        </button>
                        <button class="action-btn secondary" onclick="exportReport('comparison')">
                            <i class="fas fa-download"></i> Exportar Relatório
                        </button>
                    </div>
                </div>
            `;
            
            modal.classList.add('active');
        }}
        
        // Mostrar Rastreamento
        function showTracking() {{
            const modal = document.getElementById('tracking-modal');
            const body = document.getElementById('tracking-body');
            
            // Simular dados de rastreamento (em produção, viria do backend)
            const trackingData = [
                {{
                    vehicleId: 1,
                    color: 'blue',
                    status: 'Em trânsito 🚚',
                    nextStop: 'D004 (Hospital Einstein)',
                    distance: 3.2,
                    eta: '09:45 (em 8 minutos)',
                    speed: 45,
                    progress: 35,
                }},
                {{
                    vehicleId: 2,
                    color: 'red',
                    status: 'Entregando 📦',
                    nextStop: 'D002 (Sírio-Libanês)',
                    distance: 0,
                    eta: 'Agora',
                    speed: 0,
                    progress: 15,
                }},
                {{
                    vehicleId: 3,
                    color: 'green',
                    status: 'Aguardando início 🕐',
                    nextStop: 'D003 (Santa Casa)',
                    distance: 0,
                    eta: '09:30',
                    speed: 0,
                    progress: 0,
                }},
            ];
            
            body.innerHTML = `
                <div style="padding: 1.5rem;">
                    ${{trackingData.map(vehicle => `
                        <div class="tracking-vehicle" style="border-left-color: ${{getColorCode(vehicle.color)}};">
                            <div class="tracking-status">
                                <span style="font-size: 1.5rem;">${{vehicle.color === 'blue' ? '🔵' : vehicle.color === 'red' ? '🔴' : '🟢'}}</span>
                                <h3>VEÍCULO ${{vehicle.vehicleId}} (${{vehicle.color === 'blue' ? 'Azul' : vehicle.color === 'red' ? 'Vermelho' : 'Verde'}})</h3>
                            </div>
                            <div style="margin: 0.5rem 0;">
                                <div><strong>Status:</strong> ${{vehicle.status}}</div>
                                <div><strong>Próxima parada:</strong> ${{vehicle.nextStop}}</div>
                                ${{vehicle.distance > 0 ? `<div><strong>Distância:</strong> ${{vehicle.distance}} km</div>` : ''}}
                                <div><strong>ETA:</strong> ${{vehicle.eta}}</div>
                                ${{vehicle.speed > 0 ? `<div><strong>Velocidade:</strong> ${{vehicle.speed}} km/h</div>` : ''}}
                            </div>
                            <div class="progress-bar-tracking">
                                <div class="progress-fill-tracking" style="width: ${{vehicle.progress}}%;">
                                    ${{vehicle.progress}}% concluído
                                </div>
                            </div>
                            <div style="margin-top: 0.75rem; display: flex; gap: 0.5rem; flex-wrap: wrap;">
                                <button class="action-btn secondary" style="font-size: 0.75rem;">
                                    <i class="fas fa-phone"></i> Contatar Motorista
                                </button>
                                <button class="action-btn secondary" style="font-size: 0.75rem;">
                                    <i class="fas fa-sync-alt"></i> Atualizar
                                </button>
                            </div>
                        </div>
                    `).join('')}}
                    
                    <div style="margin-top: 1.5rem; display: flex; gap: 1rem;">
                        <button class="action-btn" onclick="alert('Funcionalidade de mapa em desenvolvimento')">
                            <i class="fas fa-map"></i> Ver Todos no Mapa
                        </button>
                        <button class="action-btn secondary">
                            <i class="fas fa-chart-line"></i> Dashboard Completo
                        </button>
                    </div>
                </div>
            `;
            
            modal.classList.add('active');
            
            // Atualizar rastreamento a cada 5 segundos
            if (window.trackingInterval) {{
                clearInterval(window.trackingInterval);
            }}
            window.trackingInterval = setInterval(() => {{
                showTracking(); // Recarregar dados
            }}, 5000);
        }}
        
        // Mostrar Menu de Exportação
        function showExportMenu() {{
            const modal = document.getElementById('export-modal');
            const body = document.getElementById('export-body');
            
            body.innerHTML = `
                <div style="padding: 1.5rem;">
                    <h3 style="margin-bottom: 1rem;">Escolha o formato de exportação:</h3>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                        <button class="action-btn" onclick="exportReport('pdf-executive')" style="flex-direction: column; padding: 1.5rem;">
                            <i class="fas fa-file-pdf" style="font-size: 2rem; margin-bottom: 0.5rem;"></i>
                            <strong>PDF Executivo</strong>
                            <small style="font-size: 0.75rem; opacity: 0.8;">Relatório resumido para gestão</small>
                        </button>
                        <button class="action-btn" onclick="exportReport('pdf-driver')" style="flex-direction: column; padding: 1.5rem;">
                            <i class="fas fa-file-pdf" style="font-size: 2rem; margin-bottom: 0.5rem;"></i>
                            <strong>PDF Motoristas</strong>
                            <small style="font-size: 0.75rem; opacity: 0.8;">Instruções detalhadas por veículo</small>
                        </button>
                        <button class="action-btn" onclick="exportReport('excel')" style="flex-direction: column; padding: 1.5rem;">
                            <i class="fas fa-file-excel" style="font-size: 2rem; margin-bottom: 0.5rem;"></i>
                            <strong>Excel</strong>
                            <small style="font-size: 0.75rem; opacity: 0.8;">Planilha completa com dados</small>
                        </button>
                        <button class="action-btn" onclick="exportReport('json')" style="flex-direction: column; padding: 1.5rem;">
                            <i class="fas fa-code" style="font-size: 2rem; margin-bottom: 0.5rem;"></i>
                            <strong>JSON/API</strong>
                            <small style="font-size: 0.75rem; opacity: 0.8;">Dados estruturados para integração</small>
                        </button>
                    </div>
                </div>
            `;
            
            modal.classList.add('active');
        }}
        
        // Exportar Relatório
        async function exportReport(type) {{
            try {{
                // Mostrar indicador de carregamento
                const loadingMsg = document.createElement('div');
                loadingMsg.id = 'export-loading';
                loadingMsg.style.cssText = 'position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); z-index: 10000;';
                loadingMsg.innerHTML = '<div style="text-align: center;"><div class="spinner" style="border: 4px solid #f3f3f3; border-top: 4px solid var(--primary); border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 0 auto 1rem;"></div><p>Gerando relatório...</p></div>';
                document.body.appendChild(loadingMsg);
                
                // Fazer requisição ao backend
                const response = await fetch(`${{API_URL}}/api/export/${{type}}`, {{
                    method: 'GET',
                }});
                
                if (!response.ok) {{
                    const error = await response.json();
                    throw new Error(error.error || 'Erro ao exportar relatório');
                }}
                
                // Obter blob do arquivo
                const blob = await response.blob();
                
                // Criar link de download
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                
                // Determinar nome do arquivo baseado no tipo
                const fileNames = {{
                    'pdf-executive': 'relatorio_executivo.pdf',
                    'pdf-driver': 'instrucoes_motoristas.pdf',
                    'excel': 'rotas_otimizadas.xlsx',
                    'json': 'dados_rotas.json',
                }};
                
                // Se for HTML (fallback do PDF), ajustar extensão
                const contentType = response.headers.get('content-type');
                if (contentType && contentType.includes('text/html')) {{
                    a.download = fileNames[type]?.replace('.pdf', '.html') || 'relatorio.html';
                }} else {{
                    a.download = fileNames[type] || 'relatorio';
                }}
                
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
                
                // Remover indicador de carregamento
                document.body.removeChild(loadingMsg);
                
                // Mostrar mensagem de sucesso
                alert('✅ Relatório exportado com sucesso!');
                closeModal('export-modal');
                
            }} catch (error) {{
                // Remover indicador de carregamento se existir
                const loadingMsg = document.getElementById('export-loading');
                if (loadingMsg) {{
                    document.body.removeChild(loadingMsg);
                }}
                
                console.error('Erro ao exportar:', error);
                alert(`❌ Erro ao exportar relatório: ${{error.message}}\\n\\nVerifique o console para mais detalhes.`);
            }}
        }}
        
        // Exportar Timeline
        function exportTimeline() {{
            alert('Exportando timeline...\\n\\nEm produção, isso baixaria um arquivo PDF ou Excel.');
        }}
        
        // Fechar modal ao clicar fora
        document.addEventListener('DOMContentLoaded', function() {{
            ['details-modal', 'timeline-modal', 'comparison-modal', 'tracking-modal', 'export-modal'].forEach(modalId => {{
                const modal = document.getElementById(modalId);
                if (modal) {{
                    modal.addEventListener('click', function(e) {{
                        if (e.target === this) {{
                            closeModal(modalId);
                        }}
                    }});
                }}
            }});
        }});
        
        // Auto-resize textarea
        function autoResizeTextarea() {{
            const textarea = document.getElementById('chat-input');
            textarea.addEventListener('input', function() {{
                this.style.height = 'auto';
                this.style.height = Math.min(this.scrollHeight, 120) + 'px';
            }});
        }}
        
        // Inicializar chatbot
        async function initializeChat() {{
            try {{
                const response = await fetch(`${{API_URL}}/api/init`, {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }}
                }});
                
                if (response.ok) {{
                    chatInitialized = true;
                    console.log('Chatbot inicializado');
                }}
            }} catch (error) {{
                console.warn('Não foi possível inicializar chatbot via API:', error);
                // Continuar mesmo sem API
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
            input.style.height = 'auto';
            
            // Mostrar typing indicator
            showTyping();
            
            // Processar
            isProcessing = true;
            const sendBtn = document.getElementById('send-btn');
            sendBtn.disabled = true;
            
            try {{
                const response = await callChatbotAPI(message);
                hideTyping();
                addMessage('assistant', response);
            }} catch (error) {{
                hideTyping();
                addMessage('assistant', 'Desculpe, ocorreu um erro ao processar sua pergunta. Tente novamente ou verifique se o servidor está rodando.');
                console.error('Erro:', error);
            }} finally {{
                isProcessing = false;
                sendBtn.disabled = false;
            }}
        }}
        
        // Chamar API do chatbot
        async function callChatbotAPI(message) {{
            try {{
                const response = await fetch(`${{API_URL}}/api/chat`, {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                    }},
                    body: JSON.stringify({{ message: message }})
                }});
                
                if (!response.ok) {{
                    throw new Error(`HTTP ${{response.status}}`);
                }}
                
                const data = await response.json();
                return data.response || 'Desculpe, não consegui processar sua pergunta.';
            }} catch (error) {{
                // Fallback para respostas simuladas se API não disponível
                return getFallbackResponse(message);
            }}
        }}
        
        // Resposta de fallback
        function getFallbackResponse(message) {{
            const msg = message.toLowerCase();
            if (msg.includes('veículo') || msg.includes('motorista')) {{
                return `Foram utilizados ${{statsData.num_vehicles}} veículos na otimização. Cada veículo foi responsável por distribuir as entregas de forma eficiente.`;
            }} else if (msg.includes('crítica') || msg.includes('medicamento')) {{
                return `Há ${{statsData.critical_deliveries}} entregas críticas que precisam de atenção especial. Estas entregas foram priorizadas nas rotas.`;
            }} else if (msg.includes('distância')) {{
                return `A distância total percorrida é de ${{statsData.total_distance.toFixed(2)}} km, distribuída de forma otimizada entre os veículos.`;
            }} else if (msg.includes('custo')) {{
                return `O custo total estimado é de R$ ${{statsData.total_cost.toFixed(2)}}, incluindo combustível e custos operacionais.`;
            }} else {{
                return `Com base nos dados da otimização: ${{statsData.num_vehicles}} veículos, ${{statsData.num_deliveries}} entregas, distância total de ${{statsData.total_distance.toFixed(2)}} km. Como posso ajudar mais?`;
            }}
        }}
        
        // Adicionar mensagem
        function addMessage(role, content) {{
            const container = document.getElementById('chat-messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${{role}}`;
            
            const roleLabel = role === 'user' ? 'Você' : '🤖 Assistente';
            const formattedContent = formatMessage(content);
            
            messageDiv.innerHTML = `
                <div class="message-bubble">
                    <strong>${{roleLabel}}:</strong> ${{formattedContent}}
                </div>
            `;
            
            container.appendChild(messageDiv);
            scrollToBottom();
            
            // Salvar no histórico
            conversationHistory.push({{role, content, timestamp: new Date()}});
        }}
        
        // Formatar mensagem (markdown básico)
        function formatMessage(text) {{
            return text
                .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
                .replace(/\\*(.*?)\\*/g, '<em>$1</em>')
                .replace(/\\n/g, '<br>');
        }}
        
        // Mostrar typing indicator
        function showTyping() {{
            document.getElementById('typing-indicator').classList.add('active');
            scrollToBottom();
        }}
        
        // Esconder typing indicator
        function hideTyping() {{
            document.getElementById('typing-indicator').classList.remove('active');
        }}
        
        // Scroll para baixo
        function scrollToBottom() {{
            const container = document.getElementById('chat-messages');
            container.scrollTop = container.scrollHeight;
        }}
        
        // Pergunta rápida
        function askQuick(question) {{
            document.getElementById('chat-input').value = question;
            sendMessage();
        }}
        
        // Limpar chat
        function clearChat() {{
            if (confirm('Deseja limpar o histórico de conversa?')) {{
                const container = document.getElementById('chat-messages');
                container.innerHTML = `
                    <div class="message assistant">
                        <div class="message-bubble">
                            <strong>🤖 Assistente:</strong> Histórico limpo! Como posso ajudar?
                        </div>
                    </div>
                `;
                conversationHistory = [];
            }}
        }}
        
        // Toggle fullscreen
        function toggleFullscreen() {{
            const mapSection = document.getElementById('map-section');
            if (mapSection.classList.contains('map-fullscreen')) {{
                mapSection.classList.remove('map-fullscreen');
            }} else {{
                mapSection.classList.add('map-fullscreen');
            }}
        }}
        
        // Handle Enter key
        function handleKeyDown(event) {{
            if (event.key === 'Enter' && !event.shiftKey) {{
                event.preventDefault();
                sendMessage();
            }}
        }}
    </script>
</body>
</html>
"""
        return html
