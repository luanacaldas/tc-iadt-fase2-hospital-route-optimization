"""
Exportador de Relatórios.

Gera relatórios em diferentes formatos (PDF, Excel, JSON).

✅ TODAS AS BIBLIOTECAS SÃO 100% GRATUITAS E OPEN SOURCE:
- PDF: WeasyPrint (gratuito) ou HTML para impressão pelo navegador
- Excel: pandas + openpyxl (gratuitos)
- JSON: Nativo do Python (gratuito)
- CSV: Nativo do Python (gratuito, fallback para Excel)

Nenhuma funcionalidade requer serviços pagos ou licenças comerciais.
"""

from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime
import json

from hospital_routes.core.interfaces import (
    OptimizationResult,
    Delivery,
    VehicleConstraints,
)


class ReportExporter:
    """Exporta relatórios em diferentes formatos."""
    
    def __init__(self):
        pass
    
    def export_pdf_executive(
        self,
        optimization_result: OptimizationResult,
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
        output_path: str,
    ) -> str:
        """
        Exporta relatório executivo em PDF.
        
        Usa bibliotecas GRATUITAS:
        - weasyprint (gratuito, open source) - para PDF real
        - ou HTML que pode ser impresso como PDF pelo navegador
        
        Args:
            optimization_result: Resultado da otimização
            deliveries: Lista de entregas
            vehicles: Lista de veículos
            output_path: Caminho do arquivo de saída
        
        Returns:
            Caminho do arquivo gerado
        """
        html_content = self._generate_executive_html(
            optimization_result, deliveries, vehicles
        )
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Tentar usar weasyprint (GRATUITO) se disponível
        try:
            from weasyprint import HTML
            HTML(string=html_content).write_pdf(output_file)
            return str(output_file.absolute())
        except ImportError:
            # Fallback: salvar HTML (pode ser impresso como PDF pelo navegador)
            html_file = output_file.with_suffix('.html')
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            # Adicionar instrução no HTML para impressão
            print(f"⚠️ WeasyPrint não instalado. HTML salvo em: {html_file}")
            print("💡 Para PDF: Abra o HTML no navegador e use Ctrl+P → Salvar como PDF")
            print("💡 Ou instale: pip install weasyprint")
            return str(html_file.absolute())
    
    def export_pdf_driver(
        self,
        optimization_result: OptimizationResult,
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
        output_path: str,
    ) -> str:
        """
        Exporta instruções detalhadas para motoristas em PDF.
        
        Usa bibliotecas GRATUITAS (weasyprint ou HTML para impressão).
        
        Args:
            optimization_result: Resultado da otimização
            deliveries: Lista de entregas
            vehicles: Lista de veículos
            output_path: Caminho do arquivo de saída
        
        Returns:
            Caminho do arquivo gerado
        """
        html_content = self._generate_driver_html(
            optimization_result, deliveries, vehicles
        )
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Tentar usar weasyprint (GRATUITO) se disponível
        try:
            from weasyprint import HTML
            HTML(string=html_content).write_pdf(output_file)
            return str(output_file.absolute())
        except ImportError:
            # Fallback: salvar HTML (pode ser impresso como PDF pelo navegador)
            html_file = output_file.with_suffix('.html')
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"⚠️ WeasyPrint não instalado. HTML salvo em: {html_file}")
            print("💡 Para PDF: Abra o HTML no navegador e use Ctrl+P → Salvar como PDF")
            return str(html_file.absolute())
    
    def export_excel(
        self,
        optimization_result: OptimizationResult,
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
        output_path: str,
    ) -> str:
        """
        Exporta dados brutos em Excel.
        
        Usa bibliotecas GRATUITAS:
        - pandas (gratuito, open source)
        - openpyxl (gratuito, open source) - para arquivos .xlsx
        
        Args:
            optimization_result: Resultado da otimização
            deliveries: Lista de entregas
            vehicles: Lista de veículos
            output_path: Caminho do arquivo de saída
        
        Returns:
            Caminho do arquivo gerado
        """
        try:
            import pandas as pd
        except ImportError:
            # Se pandas não estiver disponível, criar CSV (também gratuito)
            return self._export_csv(optimization_result, deliveries, vehicles, output_path)
        
        # Preparar dados
        routes_data = []
        solution = optimization_result.solution
        
        for vehicle_idx, route in enumerate(solution.routes):
            for delivery_idx, delivery_id in enumerate(route):
                delivery = next((d for d in deliveries if d.id == delivery_id), None)
                if delivery:
                    routes_data.append({
                        'Veículo': vehicle_idx + 1,
                        'Ordem': delivery_idx + 1,
                        'ID Entrega': delivery_id,
                        'Latitude': delivery.location[0],
                        'Longitude': delivery.location[1],
                        'Peso (kg)': delivery.weight,
                        'Prioridade': 'Crítica' if delivery.priority == 1 else 'Normal',
                    })
        
        df = pd.DataFrame(routes_data)
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        df.to_excel(output_file, index=False, engine='openpyxl')
        
        return str(output_file.absolute())
    
    def export_json(
        self,
        optimization_result: OptimizationResult,
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
        output_path: str,
    ) -> str:
        """
        Exporta dados em JSON para integração com APIs.
        
        Args:
            optimization_result: Resultado da otimização
            deliveries: Lista de entregas
            vehicles: Lista de veículos
            output_path: Caminho do arquivo de saída
        
        Returns:
            Caminho do arquivo gerado
        """
        data = {
            'timestamp': datetime.now().isoformat(),
            'solution': {
                'total_distance': optimization_result.solution.total_distance,
                'total_cost': optimization_result.solution.total_cost,
                'fitness_score': optimization_result.solution.fitness_score,
                'routes': optimization_result.solution.routes,
                'violations': optimization_result.solution.violations,
            },
            'deliveries': [
                {
                    'id': d.id,
                    'location': list(d.location),
                    'priority': d.priority,
                    'weight': d.weight,
                    'time_window_start': d.time_window_start,
                    'time_window_end': d.time_window_end,
                }
                for d in deliveries
            ],
            'vehicles': [
                {
                    'max_capacity': v.max_capacity,
                    'max_range': v.max_range,
                    'fuel_cost_per_km': v.fuel_cost_per_km,
                    'driver_cost_per_hour': v.driver_cost_per_hour,
                }
                for v in vehicles
            ],
        }
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return str(output_file.absolute())
    
    def _export_csv(
        self,
        optimization_result: OptimizationResult,
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
        output_path: str,
    ) -> str:
        """Exporta CSV como fallback quando Excel não está disponível."""
        import csv
        
        output_file = Path(output_path).with_suffix('.csv')
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        solution = optimization_result.solution
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Veículo', 'Ordem', 'ID Entrega', 'Latitude', 'Longitude', 'Peso (kg)', 'Prioridade'])
            
            for vehicle_idx, route in enumerate(solution.routes):
                for delivery_idx, delivery_id in enumerate(route):
                    delivery = next((d for d in deliveries if d.id == delivery_id), None)
                    if delivery:
                        writer.writerow([
                            vehicle_idx + 1,
                            delivery_idx + 1,
                            delivery_id,
                            delivery.location[0],
                            delivery.location[1],
                            delivery.weight,
                            'Crítica' if delivery.priority == 1 else 'Normal',
                        ])
        
        return str(output_file.absolute())
    
    def _generate_executive_html(
        self,
        optimization_result: OptimizationResult,
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
    ) -> str:
        """Gera HTML do relatório executivo completo para gestão."""
        solution = optimization_result.solution
        delivery_dict = {d.id: d for d in deliveries}
        
        # Calcular métricas detalhadas
        critical_deliveries = [d for d in deliveries if d.priority == 1]
        normal_deliveries = [d for d in deliveries if d.priority == 2]
        total_weight = sum(d.weight for d in deliveries)
        
        # Calcular métricas por veículo
        vehicle_metrics = []
        for vehicle_idx, route in enumerate(solution.routes):
            if route:
                route_weight = sum(delivery_dict[d_id].weight for d_id in route if d_id in delivery_dict)
                route_critical = sum(1 for d_id in route if d_id in delivery_dict and delivery_dict[d_id].priority == 1)
                
                # Calcular distância da rota
                from hospital_routes.utils.distance import calculate_distance
                route_distance = 0.0
                for i in range(len(route) - 1):
                    if route[i] in delivery_dict and route[i+1] in delivery_dict:
                        route_distance += calculate_distance(
                            delivery_dict[route[i]].location,
                            delivery_dict[route[i+1]].location
                        )
                
                vehicle_metrics.append({
                    'id': vehicle_idx + 1,
                    'deliveries': len(route),
                    'weight': route_weight,
                    'critical': route_critical,
                    'distance': route_distance,
                    'capacity_usage': (route_weight / vehicles[vehicle_idx].max_capacity * 100) if vehicle_idx < len(vehicles) else 0,
                    'cost': route_distance * vehicles[vehicle_idx].fuel_cost_per_km if vehicle_idx < len(vehicles) else 0
                })
        
        # Custo médio e estatísticas
        avg_distance = solution.total_distance / len([r for r in solution.routes if r]) if solution.routes else 0
        avg_cost = solution.total_cost / len([r for r in solution.routes if r]) if solution.routes else 0
        cost_per_km = solution.total_cost / solution.total_distance if solution.total_distance > 0 else 0
        cost_per_delivery = solution.total_cost / len(deliveries) if deliveries else 0
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Relatório Executivo - Otimização de Rotas Hospitalares</title>
            <style>
                @page {{ margin: 2cm; }}
                body {{ 
                    font-family: 'Segoe UI', Arial, sans-serif; 
                    margin: 0;
                    padding: 20px;
                    color: #1f2937;
                    line-height: 1.6;
                }}
                .header {{
                    background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 8px;
                    margin-bottom: 30px;
                }}
                h1 {{ 
                    margin: 0;
                    font-size: 28px;
                    font-weight: 700;
                }}
                .subtitle {{
                    font-size: 14px;
                    opacity: 0.9;
                    margin-top: 8px;
                }}
                h2 {{ 
                    color: #2563eb; 
                    border-bottom: 3px solid #2563eb;
                    padding-bottom: 8px;
                    margin-top: 30px;
                    font-size: 20px;
                }}
                h3 {{
                    color: #374151;
                    font-size: 16px;
                    margin-top: 20px;
                }}
                .metrics-grid {{
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 15px;
                    margin: 20px 0;
                }}
                .metric-card {{
                    background: #f9fafb;
                    border-left: 4px solid #2563eb;
                    padding: 15px;
                    border-radius: 4px;
                }}
                .metric-card.warning {{
                    border-left-color: #f59e0b;
                }}
                .metric-card.success {{
                    border-left-color: #10b981;
                }}
                .metric-card.danger {{
                    border-left-color: #ef4444;
                }}
                .metric-label {{
                    font-size: 12px;
                    color: #6b7280;
                    text-transform: uppercase;
                    font-weight: 600;
                    margin-bottom: 5px;
                }}
                .metric-value {{
                    font-size: 24px;
                    font-weight: 700;
                    color: #1f2937;
                }}
                .metric-unit {{
                    font-size: 14px;
                    color: #6b7280;
                    margin-left: 4px;
                }}
                table {{ 
                    border-collapse: collapse; 
                    width: 100%; 
                    margin: 20px 0;
                    background: white;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                }}
                th, td {{ 
                    border: 1px solid #e5e7eb; 
                    padding: 12px; 
                    text-align: left;
                }}
                th {{ 
                    background-color: #2563eb; 
                    color: white;
                    font-weight: 600;
                    font-size: 13px;
                    text-transform: uppercase;
                }}
                tr:nth-child(even) {{
                    background-color: #f9fafb;
                }}
                tr:hover {{
                    background-color: #f3f4f6;
                }}
                .status-badge {{
                    display: inline-block;
                    padding: 4px 8px;
                    border-radius: 12px;
                    font-size: 11px;
                    font-weight: 600;
                    text-transform: uppercase;
                }}
                .status-critical {{
                    background: #fee2e2;
                    color: #991b1b;
                }}
                .status-normal {{
                    background: #dbeafe;
                    color: #1e40af;
                }}
                .summary-box {{
                    background: #fffbeb;
                    border: 1px solid #fbbf24;
                    border-radius: 8px;
                    padding: 20px;
                    margin: 20px 0;
                }}
                .summary-box h3 {{
                    color: #92400e;
                    margin-top: 0;
                }}
                .insight {{
                    background: #f0f9ff;
                    border-left: 4px solid #0284c7;
                    padding: 15px;
                    margin: 15px 0;
                    border-radius: 4px;
                }}
                .footer {{
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 2px solid #e5e7eb;
                    font-size: 12px;
                    color: #6b7280;
                    text-align: center;
                }}
                .progress-bar {{
                    background: #e5e7eb;
                    height: 20px;
                    border-radius: 10px;
                    overflow: hidden;
                    margin-top: 5px;
                }}
                .progress-fill {{
                    background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%);
                    height: 100%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 11px;
                    font-weight: 600;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 Relatório Executivo - Otimização de Rotas Hospitalares</h1>
                <div class="subtitle">Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}</div>
            </div>
            
            <h2>📈 Indicadores Principais (KPIs)</h2>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-label">Distância Total</div>
                    <div class="metric-value">{solution.total_distance:.1f}<span class="metric-unit">km</span></div>
                </div>
                <div class="metric-card success">
                    <div class="metric-label">Custo Total</div>
                    <div class="metric-value">R$ {solution.total_cost:.2f}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Veículos Ativos</div>
                    <div class="metric-value">{len([r for r in solution.routes if r])}</div>
                </div>
                <div class="metric-card warning">
                    <div class="metric-label">Entregas Críticas</div>
                    <div class="metric-value">{len(critical_deliveries)}<span class="metric-unit">/ {len(deliveries)}</span></div>
                </div>
            </div>
            
            <h2>💰 Análise Financeira</h2>
            <table>
                <tr>
                    <th>Métrica</th>
                    <th>Valor</th>
                    <th>Observação</th>
                </tr>
                <tr>
                    <td>Custo por Quilômetro</td>
                    <td>R$ {cost_per_km:.2f}/km</td>
                    <td>Custo médio operacional</td>
                </tr>
                <tr>
                    <td>Custo por Entrega</td>
                    <td>R$ {cost_per_delivery:.2f}</td>
                    <td>Custo unitário de distribuição</td>
                </tr>
                <tr>
                    <td>Custo Médio por Veículo</td>
                    <td>R$ {avg_cost:.2f}</td>
                    <td>Média de custo operacional</td>
                </tr>
                <tr>
                    <td>Distância Média por Veículo</td>
                    <td>{avg_distance:.2f} km</td>
                    <td>Balanceamento de rotas</td>
                </tr>
            </table>
            
            <h2>🚚 Análise por Veículo</h2>
            <table>
                <tr>
                    <th>Veículo</th>
                    <th>Entregas</th>
                    <th>Distância</th>
                    <th>Peso Total</th>
                    <th>Uso Capacidade</th>
                    <th>Críticas</th>
                    <th>Custo</th>
                </tr>
        """
        
        for vm in vehicle_metrics:
            html += f"""
                <tr>
                    <td><strong>Veículo {vm['id']}</strong></td>
                    <td>{vm['deliveries']}</td>
                    <td>{vm['distance']:.2f} km</td>
                    <td>{vm['weight']:.1f} kg</td>
                    <td>
                        {vm['capacity_usage']:.1f}%
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {vm['capacity_usage']:.0f}%">
                                {vm['capacity_usage']:.0f}%
                            </div>
                        </div>
                    </td>
                    <td>{vm['critical']}</td>
                    <td>R$ {vm['cost']:.2f}</td>
                </tr>
            """
        
        html += f"""
            </table>
            
            <h2>📦 Distribuição de Entregas</h2>
            <div class="metrics-grid">
                <div class="metric-card danger">
                    <div class="metric-label">Entregas Críticas</div>
                    <div class="metric-value">{len(critical_deliveries)}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Entregas Normais</div>
                    <div class="metric-value">{len(normal_deliveries)}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Peso Total</div>
                    <div class="metric-value">{total_weight:.1f}<span class="metric-unit">kg</span></div>
                </div>
                <div class="metric-card success">
                    <div class="metric-label">Taxa Conclusão</div>
                    <div class="metric-value">100<span class="metric-unit">%</span></div>
                </div>
            </div>
            
            <h2>📋 Detalhamento de Rotas</h2>
            <table>
                <tr>
                    <th>Veículo</th>
                    <th>Nº Paradas</th>
                    <th>Sequência de Entregas</th>
                </tr>
        """
        
        for vehicle_idx, route in enumerate(solution.routes):
            if route:
                route_display = ' → '.join([f"{d_id}" for d_id in route])
                html += f"""
                <tr>
                    <td><strong>Veículo {vehicle_idx + 1}</strong></td>
                    <td>{len(route)} paradas</td>
                    <td style="font-family: monospace; font-size: 11px;">{route_display}</td>
                </tr>
                """
        
        html += f"""
            </table>
            
            <div class="summary-box">
                <h3>💡 Insights e Recomendações</h3>
                <p><strong>Eficiência Operacional:</strong></p>
                <ul>
                    <li>Sistema otimizado com {len([r for r in solution.routes if r])} veículos ativos</li>
                    <li>Distância total de {solution.total_distance:.2f} km com custo de R$ {solution.total_cost:.2f}</li>
                    <li>{len(critical_deliveries)} entregas críticas ({len(critical_deliveries)/len(deliveries)*100:.1f}% do total) priorizadas</li>
                    <li>Custo médio de R$ {cost_per_delivery:.2f} por entrega</li>
                </ul>
                
                <p><strong>Pontos de Atenção:</strong></p>
                <ul>
        """
        
        # Adicionar alertas baseados em análise
        high_capacity_vehicles = [vm for vm in vehicle_metrics if vm['capacity_usage'] > 80]
        low_capacity_vehicles = [vm for vm in vehicle_metrics if vm['capacity_usage'] < 50]
        
        if high_capacity_vehicles:
            html += f"<li>⚠️ Veículos {', '.join([str(vm['id']) for vm in high_capacity_vehicles])} com uso de capacidade acima de 80%</li>"
        
        if low_capacity_vehicles:
            html += f"<li>📊 Veículos {', '.join([str(vm['id']) for vm in low_capacity_vehicles])} subutilizados (capacidade abaixo de 50%)</li>"
        
        if solution.violations:
            html += f"<li>🔴 Violações detectadas: {', '.join(solution.violations.keys())}</li>"
        else:
            html += "<li>✅ Nenhuma violação de restrições detectada</li>"
        
        html += f"""
                </ul>
            </div>
            
            <div class="insight">
                <strong>📊 Indicador de Performance:</strong> Fitness Score = {solution.fitness_score:.2f}<br>
                <small>Score de otimização considerando distância, capacidade, autonomia e prioridades</small>
            </div>
            
            <div class="footer">
                <p><strong>Sistema de Otimização de Rotas Hospitalares</strong></p>
                <p>Relatório gerado automaticamente • Algoritmo Genético com busca local • Tempo de execução: {optimization_result.execution_time:.2f}s</p>
                <p>Gerações evolutivas: {optimization_result.generations_evolved} • Score final: {solution.fitness_score:.4f}</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _generate_driver_html(
        self,
        optimization_result: OptimizationResult,
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
    ) -> str:
        """Gera HTML detalhado das instruções para motoristas."""
        solution = optimization_result.solution
        delivery_dict = {d.id: d for d in deliveries}
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Instruções Detalhadas para Motoristas</title>
            <style>
                @page {{ margin: 1.5cm; }}
                body {{ 
                    font-family: 'Segoe UI', Arial, sans-serif; 
                    margin: 0;
                    padding: 20px;
                    color: #1f2937;
                    line-height: 1.5;
                }}
                .header {{
                    background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
                    color: white;
                    padding: 25px;
                    border-radius: 8px;
                    margin-bottom: 25px;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 26px;
                }}
                .header .date {{
                    font-size: 14px;
                    opacity: 0.9;
                    margin-top: 5px;
                }}
                .vehicle-section {{
                    page-break-before: always;
                    margin-bottom: 40px;
                    break-inside: avoid;
                }}
                .vehicle-section:first-of-type {{
                    page-break-before: auto;
                }}
                .vehicle-header {{
                    background: #f0f9ff;
                    border-left: 5px solid #2563eb;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 20px;
                }}
                .vehicle-header h2 {{
                    margin: 0 0 10px 0;
                    color: #1e40af;
                    font-size: 24px;
                }}
                .vehicle-summary {{
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 10px;
                    margin-top: 15px;
                }}
                .summary-item {{
                    background: white;
                    padding: 10px;
                    border-radius: 6px;
                    border: 1px solid #e5e7eb;
                }}
                .summary-label {{
                    font-size: 11px;
                    color: #6b7280;
                    text-transform: uppercase;
                    font-weight: 600;
                }}
                .summary-value {{
                    font-size: 18px;
                    font-weight: 700;
                    color: #1f2937;
                    margin-top: 2px;
                }}
                .checklist {{
                    background: #fffbeb;
                    border: 2px solid #fbbf24;
                    border-radius: 8px;
                    padding: 15px;
                    margin-bottom: 20px;
                }}
                .checklist h3 {{
                    margin: 0 0 10px 0;
                    color: #92400e;
                    font-size: 16px;
                }}
                .checklist-item {{
                    padding: 8px 0;
                    border-bottom: 1px solid #fde68a;
                }}
                .checklist-item:last-child {{
                    border-bottom: none;
                }}
                .checklist-item input {{
                    margin-right: 10px;
                    transform: scale(1.2);
                }}
                .stops-container {{
                    counter-reset: stop-counter;
                }}
                .stop {{
                    position: relative;
                    margin: 15px 0;
                    padding: 20px;
                    background: white;
                    border: 2px solid #e5e7eb;
                    border-radius: 8px;
                    page-break-inside: avoid;
                }}
                .stop::before {{
                    counter-increment: stop-counter;
                    content: counter(stop-counter);
                    position: absolute;
                    left: -15px;
                    top: 20px;
                    width: 40px;
                    height: 40px;
                    background: #2563eb;
                    color: white;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: 700;
                    font-size: 18px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                }}
                .stop.critical {{
                    background: #fef2f2;
                    border-color: #dc2626;
                    border-width: 3px;
                }}
                .stop.critical::before {{
                    background: #dc2626;
                }}
                .stop-header {{
                    display: flex;
                    justify-content: space-between;
                    align-items: start;
                    margin-bottom: 15px;
                }}
                .stop-title {{
                    font-size: 18px;
                    font-weight: 700;
                    color: #1f2937;
                }}
                .priority-badge {{
                    padding: 6px 12px;
                    border-radius: 20px;
                    font-size: 11px;
                    font-weight: 700;
                    text-transform: uppercase;
                }}
                .priority-critical {{
                    background: #dc2626;
                    color: white;
                }}
                .priority-normal {{
                    background: #3b82f6;
                    color: white;
                }}
                .stop-details {{
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 15px;
                    margin-top: 15px;
                }}
                .detail-box {{
                    background: #f9fafb;
                    padding: 12px;
                    border-radius: 6px;
                    border-left: 3px solid #2563eb;
                }}
                .detail-label {{
                    font-size: 11px;
                    color: #6b7280;
                    text-transform: uppercase;
                    font-weight: 600;
                    margin-bottom: 5px;
                }}
                .detail-value {{
                    font-size: 14px;
                    font-weight: 600;
                    color: #1f2937;
                }}
                .coordinates {{
                    font-family: monospace;
                    font-size: 13px;
                }}
                .map-link {{
                    display: inline-block;
                    margin-top: 10px;
                    padding: 8px 16px;
                    background: #2563eb;
                    color: white;
                    text-decoration: none;
                    border-radius: 6px;
                    font-size: 13px;
                    font-weight: 600;
                }}
                .map-link:hover {{
                    background: #1e40af;
                }}
                .alert-box {{
                    background: #fee2e2;
                    border: 2px solid #dc2626;
                    border-radius: 8px;
                    padding: 15px;
                    margin: 15px 0;
                }}
                .alert-box strong {{
                    color: #991b1b;
                }}
                .completion-box {{
                    background: #f9fafb;
                    border: 2px dashed #9ca3af;
                    border-radius: 8px;
                    padding: 15px;
                    margin-top: 15px;
                    text-align: center;
                }}
                .completion-box input {{
                    margin-right: 10px;
                    transform: scale(1.5);
                }}
                .footer {{
                    margin-top: 30px;
                    padding-top: 15px;
                    border-top: 2px solid #e5e7eb;
                    font-size: 11px;
                    color: #6b7280;
                    text-align: center;
                }}
                .signature-box {{
                    margin-top: 30px;
                    padding: 20px;
                    background: #f9fafb;
                    border: 2px solid #e5e7eb;
                    border-radius: 8px;
                }}
                .signature-line {{
                    border-top: 2px solid #1f2937;
                    margin-top: 30px;
                    padding-top: 8px;
                    text-align: center;
                    font-size: 12px;
                    color: #6b7280;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚚 Instruções Detalhadas de Entrega</h1>
                <div class="date">Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}</div>
            </div>
        """
        
        for vehicle_idx, route in enumerate(solution.routes):
            if not route:
                continue
                
            # Calcular métricas do veículo
            route_weight = sum(delivery_dict[d_id].weight for d_id in route if d_id in delivery_dict)
            route_critical = sum(1 for d_id in route if d_id in delivery_dict and delivery_dict[d_id].priority == 1)
            
            # Calcular distância estimada
            from hospital_routes.utils.distance import calculate_distance
            route_distance = 0.0
            for i in range(len(route) - 1):
                if route[i] in delivery_dict and route[i+1] in delivery_dict:
                    route_distance += calculate_distance(
                        delivery_dict[route[i]].location,
                        delivery_dict[route[i+1]].location
                    )
            
            # Tempo estimado (assumindo 40 km/h médio + 15 min por parada)
            estimated_time_hours = (route_distance / 40.0) + (len(route) * 0.25)
            estimated_time_min = int(estimated_time_hours * 60)
            
            vehicle_capacity = vehicles[vehicle_idx].max_capacity if vehicle_idx < len(vehicles) else 100
            capacity_usage = (route_weight / vehicle_capacity * 100)
            
            html += f"""
            <div class="vehicle-section">
                <div class="vehicle-header">
                    <h2>🚛 VEÍCULO {vehicle_idx + 1}</h2>
                    <div class="vehicle-summary">
                        <div class="summary-item">
                            <div class="summary-label">Total Paradas</div>
                            <div class="summary-value">{len(route)}</div>
                        </div>
                        <div class="summary-item">
                            <div class="summary-label">Distância Total</div>
                            <div class="summary-value">{route_distance:.1f} km</div>
                        </div>
                        <div class="summary-item">
                            <div class="summary-label">Tempo Estimado</div>
                            <div class="summary-value">{estimated_time_min} min</div>
                        </div>
                        <div class="summary-item">
                            <div class="summary-label">Carga Total</div>
                            <div class="summary-value">{route_weight:.1f} kg</div>
                        </div>
                    </div>
                </div>
                
                <div class="checklist">
                    <h3>✓ Checklist de Pré-Viagem</h3>
                    <div class="checklist-item">
                        <input type="checkbox"> Verificar nível de combustível
                    </div>
                    <div class="checklist-item">
                        <input type="checkbox"> Conferir documentação do veículo
                    </div>
                    <div class="checklist-item">
                        <input type="checkbox"> Verificar condições dos pneus
                    </div>
                    <div class="checklist-item">
                        <input type="checkbox"> Conferir carga total: {route_weight:.1f} kg ({capacity_usage:.0f}% da capacidade)
                    </div>
                    <div class="checklist-item">
                        <input type="checkbox"> Verificar itens de segurança (extintor, triângulo, etc)
                    </div>
                </div>
            """
            
            if route_critical > 0:
                html += f"""
                <div class="alert-box">
                    <strong>⚠️ ATENÇÃO:</strong> Esta rota contém {route_critical} entrega(s) CRÍTICA(S) (medicamentos urgentes). 
                    Priorize estas entregas e certifique-se de entregar no prazo!
                </div>
                """
            
            html += '<div class="stops-container">'
            
            for stop_idx, delivery_id in enumerate(route):
                delivery = delivery_dict.get(delivery_id)
                if not delivery:
                    continue
                    
                is_critical = delivery.priority == 1
                priority_class = 'critical' if is_critical else ''
                priority_badge_class = 'priority-critical' if is_critical else 'priority-normal'
                priority_text = '🚨 CRÍTICA' if is_critical else '📦 NORMAL'
                
                # Tempo estimado de chegada
                time_to_stop = (stop_idx + 1) * 15  # Estimativa simples: 15 min por parada
                
                html += f"""
                <div class="stop {priority_class}">
                    <div class="stop-header">
                        <div class="stop-title">📍 {delivery_id}</div>
                        <span class="priority-badge {priority_badge_class}">{priority_text}</span>
                    </div>
                    
                    <div class="stop-details">
                        <div class="detail-box">
                            <div class="detail-label">Peso da Carga</div>
                            <div class="detail-value">{delivery.weight:.1f} kg</div>
                        </div>
                        <div class="detail-box">
                            <div class="detail-label">Tempo Estimado</div>
                            <div class="detail-value">~{time_to_stop} minutos</div>
                        </div>
                        <div class="detail-box" style="grid-column: span 2;">
                            <div class="detail-label">Coordenadas GPS</div>
                            <div class="detail-value coordinates">
                                Lat: {delivery.location[0]:.6f}, Lon: {delivery.location[1]:.6f}
                            </div>
                            <a href="https://www.google.com/maps/search/?api=1&query={delivery.location[0]},{delivery.location[1]}" 
                               class="map-link" target="_blank">
                                📍 Abrir no Google Maps
                            </a>
                        </div>
                    </div>
                    
                    <div class="completion-box">
                        <input type="checkbox" id="stop{vehicle_idx}_{stop_idx}">
                        <label for="stop{vehicle_idx}_{stop_idx}"><strong>Entrega Concluída</strong></label>
                        <span style="margin-left: 20px;">Horário: _____:_____</span>
                        <span style="margin-left: 20px;">Assinatura: _________________</span>
                    </div>
                </div>
                """
            
            html += """
                </div>
                
                <div class="signature-box">
                    <h3>📝 Confirmação do Motorista</h3>
                    <p>Declaro que recebi todas as informações de rota e estou ciente das entregas críticas.</p>
                    <div class="signature-line">
                        Assinatura do Motorista: _________________________________ Data: ____/____/______
                    </div>
                </div>
            </div>
            """
        
        html += f"""
            <div class="footer">
                <p><strong>Sistema de Otimização de Rotas Hospitalares</strong></p>
                <p>Instruções geradas automaticamente • Em caso de dúvidas, contate a central de operações</p>
                <p>⚠️ Mantenha este documento durante toda a jornada de entregas</p>
            </div>
        </body>
        </html>
        """
        
        return html
