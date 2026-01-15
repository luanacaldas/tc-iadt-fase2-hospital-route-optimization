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
        """Gera HTML do relatório executivo."""
        solution = optimization_result.solution
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Relatório Executivo - Otimização de Rotas</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #2563eb; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #2563eb; color: white; }}
            </style>
        </head>
        <body>
            <h1>Relatório Executivo - Otimização de Rotas</h1>
            <p><strong>Data:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            
            <h2>Resumo Executivo</h2>
            <table>
                <tr>
                    <th>Métrica</th>
                    <th>Valor</th>
                </tr>
                <tr>
                    <td>Distância Total</td>
                    <td>{solution.total_distance:.2f} km</td>
                </tr>
                <tr>
                    <td>Custo Total</td>
                    <td>R$ {solution.total_cost:.2f}</td>
                </tr>
                <tr>
                    <td>Veículos Utilizados</td>
                    <td>{len([r for r in solution.routes if r])}</td>
                </tr>
                <tr>
                    <td>Entregas</td>
                    <td>{len(deliveries)}</td>
                </tr>
            </table>
            
            <h2>Rotas Otimizadas</h2>
            <table>
                <tr>
                    <th>Veículo</th>
                    <th>Entregas</th>
                    <th>Rota</th>
                </tr>
        """
        
        for vehicle_idx, route in enumerate(solution.routes):
            if route:
                html += f"""
                <tr>
                    <td>Veículo {vehicle_idx + 1}</td>
                    <td>{len(route)}</td>
                    <td>{' → '.join(route)}</td>
                </tr>
                """
        
        html += """
            </table>
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
        """Gera HTML das instruções para motoristas."""
        solution = optimization_result.solution
        delivery_dict = {d.id: d for d in deliveries}
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Instruções para Motoristas</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #2563eb; }}
                .route {{ margin: 20px 0; padding: 15px; border: 2px solid #2563eb; border-radius: 5px; }}
                .stop {{ margin: 10px 0; padding: 10px; background: #f0f0f0; border-radius: 3px; }}
                .critical {{ background: #fee2e2; border-left: 4px solid #dc2626; }}
            </style>
        </head>
        <body>
            <h1>Instruções de Rota para Motoristas</h1>
            <p><strong>Data:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        """
        
        for vehicle_idx, route in enumerate(solution.routes):
            if route:
                html += f"""
                <div class="route">
                    <h2>🚚 Veículo {vehicle_idx + 1}</h2>
                    <p><strong>Total de Paradas:</strong> {len(route)}</p>
                    <ol>
                """
                
                for stop_idx, delivery_id in enumerate(route):
                    delivery = delivery_dict.get(delivery_id)
                    is_critical = delivery.priority == 1 if delivery else False
                    critical_class = 'critical' if is_critical else ''
                    
                    html += f"""
                        <li class="stop {critical_class}">
                            <strong>Parada {stop_idx + 1}:</strong> {delivery_id}
                            {f'<br><span style="color: red;">⚠️ ENTREGA CRÍTICA</span>' if is_critical else ''}
                            {f'<br><strong>Peso:</strong> {delivery.weight} kg' if delivery else ''}
                            {f'<br><strong>Localização:</strong> ({delivery.location[0]:.4f}, {delivery.location[1]:.4f})' if delivery else ''}
                        </li>
                    """
                
                html += """
                    </ol>
                </div>
                """
        
        html += """
        </body>
        </html>
        """
        
        return html
