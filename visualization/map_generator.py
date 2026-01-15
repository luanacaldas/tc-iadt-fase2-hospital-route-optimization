"""
Geração de mapas interativos usando Folium.

Este módulo consome apenas DTOs e gera visualizações de rotas.
Não participa da lógica de negócio.
"""

from typing import List, Tuple, Optional
from pathlib import Path

import folium
from folium import plugins

from hospital_routes.core.interfaces import (
    OptimizationResult,
    Delivery,
    RouteSolution,
)
from hospital_routes.utils.distance import calculate_distance
from hospital_routes.utils.accident_data import (
    AccidentDataProvider,
    get_risk_color,
    get_risk_icon,
)


class MapGenerator:
    """
    Gera mapas interativos com Folium para visualização de rotas.
    
    Consome apenas DTOs, não entidades de domínio.
    """
    
    # Cores para diferentes veículos - otimizadas para contraste
    # Cores principais com alta visibilidade sobre mapa verde/azul
    ROUTE_COLORS = [
        "#0066FF",  # Azul Royal - destaca bem sobre fundo claro
        "#FF0055",  # Magenta - alta visibilidade
        "#00CC66",  # Verde limão - contrasta com verde do mapa
        "#FF6600",  # Laranja vibrante
        "#9900FF",  # Roxo intenso
        "#FF0066",  # Rosa/Magenta alternativo
        "#00FFFF",  # Ciano
        "#FFCC00",  # Amarelo dourado
        "#FF3300",  # Vermelho intenso
        "#0066CC",  # Azul médio
        "#66FF00",  # Verde neon
        "#FF0099",  # Rosa choque
        "#CC00FF",  # Magenta escuro
        "#00FF99",  # Verde água
        "#FF9900",  # Laranja claro
        "#6600FF",  # Roxo azulado
        "#FF0066",  # Rosa
        "#00FFCC",  # Turquesa
    ]
    
    # Mapeamento de códigos hexadecimais para nomes de cores
    COLOR_NAMES = {
        "#0066FF": "Azul",
        "#FF0055": "Magenta",
        "#00CC66": "Verde",
        "#FF6600": "Laranja",
        "#9900FF": "Roxo",
        "#FF0066": "Rosa",
        "#00FFFF": "Ciano",
        "#FFCC00": "Amarelo",
        "#FF3300": "Vermelho",
        "#0066CC": "Azul Médio",
        "#66FF00": "Verde Neon",
        "#FF0099": "Rosa Choque",
        "#CC00FF": "Magenta Escuro",
        "#00FF99": "Verde Água",
        "#FF9900": "Laranja Claro",
        "#6600FF": "Roxo Azulado",
        "#00FFCC": "Turquesa",
    }
    
    def __init__(self, center_location: Optional[Tuple[float, float]] = None):
        """
        Args:
            center_location: Localização central do mapa (lat, lon).
                           Se None, será calculada automaticamente.
        """
        self.center_location = center_location
    
    def generate_map(
        self,
        optimization_result: OptimizationResult,
        deliveries: List[Delivery],
        depot_location: Tuple[float, float],
        output_path: str = "route_map.html",
        title: str = "Rotas Otimizadas",
        accident_provider: Optional[AccidentDataProvider] = None,
        show_accidents: bool = True,
    ) -> folium.Map:
        """
        Gera mapa interativo com as rotas otimizadas.
        
        Args:
            optimization_result: Resultado da otimização
            deliveries: Lista de entregas (para obter localizações e prioridades)
            depot_location: Localização do depósito (latitude, longitude)
            output_path: Caminho para salvar o mapa HTML
            title: Título do mapa
        
        Returns:
            folium.Map: Mapa gerado
        
        Raises:
            ValueError: Se deliveries estiver vazia ou se houver IDs inválidos
        """
        if not deliveries:
            raise ValueError("Lista de entregas não pode estar vazia")
        
        # Criar dicionário de entregas para acesso rápido
        delivery_dict = {d.id: d for d in deliveries}
        
        # Calcular localização central se não fornecida
        center = self._calculate_center(
            optimization_result.solution, deliveries, depot_location
        )
        
        # Criar mapa
        m = folium.Map(
            location=center,
            zoom_start=12,
            tiles="OpenStreetMap",
        )
        
        # Adicionar CDN do Font Awesome no head do HTML para ícones
        # Isso é necessário para que os ícones Font Awesome funcionem
        font_awesome_cdn = """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" 
              integrity="sha512-9usAa10IRO0HhonpyAIVpjrylPvoDwiPUiKdWk5t3PyolY1cOd4DSE0Ga+ri4AuTroPR5aQvXU9xC6qOPnzFeg==" 
              crossorigin="anonymous" referrerpolicy="no-referrer" />
        """
        m.get_root().html.add_child(folium.Element(font_awesome_cdn))
        
        # Card redundante removido - informações já estão no header da interface
        
        # Adicionar depósito
        self._add_depot_marker(m, depot_location)
        
        # Adicionar camada de acidentes se disponível
        if show_accidents and accident_provider:
            self._add_accident_layer(m, accident_provider)
        
        # Adicionar rotas de cada veículo
        solution = optimization_result.solution
        for route_idx, route in enumerate(solution.routes):
            if not route:
                continue
            
            color = self.ROUTE_COLORS[route_idx % len(self.ROUTE_COLORS)]
            self._add_route_to_map(
                m,
                route,
                delivery_dict,
                depot_location,
                vehicle_id=route_idx + 1,
                color=color,
                accident_provider=accident_provider if show_accidents else None,
            )
        
        # Adicionar legenda
        self._add_legend(m, len(solution.routes), show_accidents=show_accidents and accident_provider is not None)
        
        # Adicionar JavaScript para destacar rotas
        self._add_route_highlight_script(m, solution.routes, delivery_dict, depot_location)
        
        # Salvar mapa
        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)
        m.save(str(output_path_obj))
        
        return m
    
    def _calculate_center(
        self,
        solution: RouteSolution,
        deliveries: List[Delivery],
        depot_location: Tuple[float, float],
    ) -> Tuple[float, float]:
        """
        Calcula localização central do mapa.
        
        Args:
            solution: Solução de rotas
            deliveries: Lista de entregas
            depot_location: Localização do depósito
        
        Returns:
            Tuple[float, float]: Coordenadas (lat, lon) do centro
        """
        if self.center_location:
            return self.center_location
        
        # Coletar todas as localizações
        locations = [depot_location]
        delivery_dict = {d.id: d for d in deliveries}
        
        for route in solution.routes:
            for delivery_id in route:
                if delivery_id in delivery_dict:
                    locations.append(delivery_dict[delivery_id].location)
        
        # Calcular centro (média das coordenadas)
        if locations:
            avg_lat = sum(loc[0] for loc in locations) / len(locations)
            avg_lon = sum(loc[1] for loc in locations) / len(locations)
            return (avg_lat, avg_lon)
        
        return depot_location
    
    def _add_depot_marker(
        self, map_obj: folium.Map, depot_location: Tuple[float, float]
    ) -> None:
        """
        Adiciona marcador do depósito ao mapa.
        
        Args:
            map_obj: Objeto do mapa Folium
            depot_location: Localização do depósito
        """
        # Ícone grande de hospital (40px), verde escuro #10B981, label "DEPÓSITO"
        depot_icon_html = """
        <div style="
            position: relative;
            width: 50px;
            height: 50px;
            filter: drop-shadow(0 3px 10px rgba(0,0,0,0.5));
        ">
            <i class="fas fa-hospital" 
               style="
                   font-size: 40px;
                   color: #10B981;
                   position: absolute;
                   top: 0;
                   left: 0;
                   text-shadow: 0 0 0 white, 0 0 0 white, 0 0 8px white, 0 0 8px white;
                   -webkit-text-stroke: 3px white;
                   paint-order: stroke fill;
               "></i>
            <div style="
                position: absolute;
                bottom: -8px;
                left: 50%;
                transform: translateX(-50%);
                background-color: #10B981;
                color: white;
                padding: 2px 6px;
                border-radius: 4px;
                font-size: 9px;
                font-weight: bold;
                white-space: nowrap;
                box-shadow: 0 2px 6px rgba(0,0,0,0.3);
                border: 2px solid white;
            ">DEPÓSITO</div>
        </div>
        """
        
        folium.Marker(
            location=depot_location,
            popup=folium.Popup(
                "<b>🏥 DEPÓSITO</b><br>Ponto de partida e retorno das rotas",
                max_width=250,
            ),
            tooltip="🏥 DEPÓSITO - Ponto de partida",
            icon=folium.DivIcon(
                html=depot_icon_html,
                icon_size=(50, 60),
                icon_anchor=(25, 50),
            ),
        ).add_to(map_obj)
    
    def _add_route_to_map(
        self,
        map_obj: folium.Map,
        route: List[str],
        delivery_dict: dict,
        depot_location: Tuple[float, float],
        vehicle_id: int,
        color: str,
        accident_provider: Optional[AccidentDataProvider] = None,
    ) -> None:
        """
        Adiciona uma rota completa ao mapa.
        
        Args:
            map_obj: Objeto do mapa Folium
            route: Lista de IDs de entregas na rota
            delivery_dict: Dicionário de entregas (id -> Delivery)
            depot_location: Localização do depósito
            vehicle_id: ID do veículo
            color: Cor da rota
        """
        if not route:
            return
        
        # Coletar coordenadas da rota (depósito → entregas → depósito)
        route_coordinates = [depot_location]
        
        for delivery_id in route:
            if delivery_id in delivery_dict:
                delivery = delivery_dict[delivery_id]
                route_coordinates.append(delivery.location)
        
        # Voltar ao depósito
        route_coordinates.append(depot_location)
        
        # Calcular distância total da rota
        total_route_distance = 0.0
        for i in range(len(route_coordinates) - 1):
            total_route_distance += calculate_distance(
                route_coordinates[i], route_coordinates[i + 1]
            )
        
        # Calcular risco de acidentes se disponível
        route_risk_info = None
        if accident_provider:
            route_risk_info = accident_provider.get_route_risk(route_coordinates)
        
        # Criar popup com informações da rota
        popup_html = f"""
        <div style="font-size: 12px;">
            <b>🚚 Veículo {vehicle_id}</b><br>
            <hr style="margin: 5px 0;">
            <b>📦 Entregas:</b> {len(route)}<br>
            <b>📏 Distância:</b> {total_route_distance:.2f} km<br>
            <b>📍 Paradas:</b> {', '.join(route)}<br>
            <b>🎨 Cor:</b> <span style="color: {color}; font-weight: bold;">{color}</span>
        """
        
        if route_risk_info:
            risk_color = get_risk_color(route_risk_info["overall_risk"])
            popup_html += f"""
            <hr style="margin: 5px 0;">
            <b>⚠️ Análise de Segurança:</b><br>
            <b>Nível de Risco:</b> <span style="color: {risk_color}; font-weight: bold;">{route_risk_info['overall_risk'].upper()}</span><br>
            <b>Acidentes no trajeto:</b> {route_risk_info['total_accidents']}<br>
            <b>Severidade média:</b> {route_risk_info['avg_severity']:.1f}/5.0<br>
            <b>Segmentos de alto risco:</b> {route_risk_info['high_risk_segments']}
            """
        
        popup_html += "</div>"
        
        # Adicionar linha da rota
        # Se houver dados de acidentes, usar cor baseada no risco
        line_color = color
        if route_risk_info and route_risk_info["overall_risk"] in ["high", "critical"]:
            # Misturar cor da rota com cor de risco para alerta visual
            line_color = get_risk_color(route_risk_info["overall_risk"])
        
        # Criar FeatureGroup para a rota (permite mostrar/ocultar facilmente)
        route_group = folium.FeatureGroup(name=f"route_vehicle_{vehicle_id}")
        
        # Hierarquia visual: rotas normais com weight=4, opacity=0.8
        polyline = folium.PolyLine(
            locations=route_coordinates,
            color=line_color,
            weight=4,  # Espessura padrão para rotas normais
            opacity=0.8,  # Opacidade padrão
            popup=folium.Popup(popup_html, max_width=350),
            tooltip=f"🚚 Veículo {vehicle_id} - {len(route)} entregas - Clique para detalhes",
        )
        polyline.add_to(route_group)
        
        # Armazenar coordenadas da rota para zoom e animação
        route_group.route_coordinates = route_coordinates
        route_group.vehicle_id = vehicle_id
        route_group.route = route
        route_group.delivery_dict = {delivery_id: delivery_dict[delivery_id] for delivery_id in route if delivery_id in delivery_dict}
        
        route_group.add_to(map_obj)
        
        # Adicionar marcadores de acidentes ao longo da rota
        if accident_provider:
            self._add_accident_markers_to_route(
                map_obj, route_coordinates, accident_provider
            )
        
        # Adicionar marcadores numerados ao longo da rota para mostrar ordem
        for i in range(len(route_coordinates) - 1):
            start = route_coordinates[i]
            end = route_coordinates[i + 1]
            # Ponto médio do segmento
            mid_lat = start[0] + (end[0] - start[0]) * 0.5
            mid_lon = start[1] + (end[1] - start[1]) * 0.5
            
            # Adicionar pequeno círculo indicando direção com melhor contraste
            folium.CircleMarker(
                location=(mid_lat, mid_lon),
                radius=5,
                color="white",  # Borda branca para contraste
                fill=True,
                fillColor=color,
                fillOpacity=0.9,
                weight=3,  # Borda mais espessa para halo effect
                tooltip=f"Veículo {vehicle_id} - Segmento {i+1}",
            ).add_to(route_group)
        
        # Adicionar marcadores para cada entrega
        for stop_idx, delivery_id in enumerate(route):
            if delivery_id not in delivery_dict:
                continue
            
            delivery = delivery_dict[delivery_id]
            is_critical = delivery.priority == 1
            
            # Configuração baseada no tipo de entrega
            if is_critical:
                # ENTREGAS CRÍTICAS: ⚠️ Ícone de alerta + número (36px), vermelho #EF4444, borda pulsante
                icon_color = "#EF4444"
                icon_name = "exclamation-triangle"
                icon_size = 36
                marker_size = 48
                priority_text = "CRÍTICA (Medicamentos)"
                delivery_type = "Medicamentos"
            else:
                # ENTREGAS NORMAIS: 📦 Ícone de caixa + número (32px), azul #3B82F6
                icon_color = "#3B82F6"
                icon_name = "box"
                icon_size = 32
                marker_size = 44
                priority_text = "Normal"
                delivery_type = "Insumos"
            
            # Criar popup com informações
            popup_html = f"""
            <div style="font-size: 12px">
                <b>Entrega: {delivery_id}</b><br>
                <b>Prioridade: {priority_text}</b><br>
                Tipo: {delivery_type}<br>
                Peso: {delivery.weight} kg<br>
                Parada {stop_idx + 1} na rota do Veículo {vehicle_id}
            </div>
            """
            
            # Animação pulsante para entregas críticas
            pulse_animation = ""
            if is_critical:
                pulse_animation = """
                @keyframes pulse {
                    0%, 100% { transform: scale(1); opacity: 1; }
                    50% { transform: scale(1.1); opacity: 0.9; }
                }
                .pulse-border {
                    animation: pulse 2s ease-in-out infinite;
                }
                """
            
            # Criar ícone customizado com número da parada
            icon_html = f"""
            <style>
                {pulse_animation}
            </style>
            <div class="{'pulse-border' if is_critical else ''}" style="
                position: relative;
                width: {marker_size}px;
                height: {marker_size}px;
                filter: drop-shadow(0 3px 10px rgba(0,0,0,0.5));
            ">
                <i class="fas fa-{icon_name}" 
                   style="
                       font-size: {icon_size}px;
                       color: {icon_color};
                       position: absolute;
                       top: 50%;
                       left: 50%;
                       transform: translate(-50%, -50%);
                       text-shadow: 0 0 0 white, 0 0 0 white, 0 0 8px white, 0 0 8px white;
                       -webkit-text-stroke: 4px white;
                       paint-order: stroke fill;
                   "></i>
                <div style="
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    background-color: {icon_color};
                    color: white;
                    border: 3px solid white;
                    border-radius: 50%;
                    width: 24px;
                    height: 24px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: bold;
                    font-size: 14px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.4);
                    text-shadow: 0 1px 3px rgba(0,0,0,0.5);
                    margin-top: 8px;
                ">{stop_idx + 1}</div>
            </div>
            """
            
            # Tooltip melhorado
            tooltip_text = f"{'⚠️ CRÍTICA' if is_critical else '📦'} {delivery_id} - Parada {stop_idx + 1} ({delivery_type}) - Veículo {vehicle_id}"
            
            folium.Marker(
                location=delivery.location,
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=tooltip_text,
                icon=folium.DivIcon(
                    html=icon_html,
                    icon_size=(marker_size, marker_size),
                    icon_anchor=(marker_size // 2, marker_size // 2),
                ),
            ).add_to(route_group)
    
    def _add_accident_layer(
        self, map_obj: folium.Map, accident_provider: AccidentDataProvider
    ) -> None:
        """
        Adiciona camada de acidentes ao mapa.
        
        Args:
            map_obj: Objeto do mapa Folium
            accident_provider: Provedor de dados de acidentes
        """
        # Criar grupo de acidentes
        accident_group = folium.FeatureGroup(name="⚠️ Pontos de Acidentes", show=False)
        
        # Adicionar marcadores para cada ponto de acidente conhecido
        for location, accident_data in accident_provider._accident_cache.items():
            risk_color = get_risk_color(accident_data.risk_level)
            risk_icon = get_risk_icon(accident_data.risk_level)
            
            # Criar popup com informações
            popup_html = f"""
            <div style="font-size: 12px;">
                <b>⚠️ Ponto de Acidente</b><br>
                <hr style="margin: 5px 0;">
                <b>Via:</b> {accident_data.road_name or 'Não especificada'}<br>
                <b>Acidentes (último ano):</b> {accident_data.accidents_count}<br>
                <b>Severidade:</b> {accident_data.severity:.1f}/5.0<br>
                <b>Nível de Risco:</b> <span style="color: {risk_color}; font-weight: bold;">{accident_data.risk_level.upper()}</span>
            </div>
            """
            
            # Ícone baseado no risco com melhor contraste
            icon_html = f"""
            <div style="
                background-color: {risk_color};
                border: 3px solid white;
                border-radius: 50%;
                width: 22px;
                height: 22px;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.4);
            ">
                <i class="fas fa-{risk_icon}" style="color: white; font-size: 10px;"></i>
            </div>
            """
            
            folium.Marker(
                location=location,
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=f"⚠️ {accident_data.road_name or 'Ponto de acidente'} - Risco: {accident_data.risk_level}",
                icon=folium.DivIcon(
                    html=icon_html,
                    icon_size=(20, 20),
                    icon_anchor=(10, 10),
                ),
            ).add_to(accident_group)
        
        accident_group.add_to(map_obj)
    
    def _add_accident_markers_to_route(
        self,
        map_obj: folium.Map,
        route_coordinates: List[Tuple[float, float]],
        accident_provider: AccidentDataProvider,
    ) -> None:
        """
        Adiciona marcadores de acidentes específicos ao longo de uma rota.
        
        Args:
            map_obj: Objeto do mapa Folium
            route_coordinates: Coordenadas da rota
            accident_provider: Provedor de dados de acidentes
        """
        route_risk = accident_provider.get_route_risk(route_coordinates)
        
        # Adicionar marcadores para segmentos de risco
        for segment in route_risk.get("risk_segments", []):
            location = segment["location"]
            risk_level = segment["risk_level"]
            risk_color = get_risk_color(risk_level)
            
            # Apenas marcar riscos médios, altos ou críticos
            if risk_level in ["medium", "high", "critical"]:
                folium.CircleMarker(
                    location=location,
                    radius=8,
                    color="white",  # Borda branca para contraste
                    fill=True,
                    fillColor=risk_color,
                    fillOpacity=0.7,
                    weight=3,  # Borda mais espessa para halo effect
                    popup=folium.Popup(
                        f"""
                        <div style="font-size: 11px;">
                            <b>⚠️ Ponto de Risco</b><br>
                            <b>Via:</b> {segment.get('road_name', 'Não especificada')}<br>
                            <b>Acidentes:</b> {segment['accidents']}<br>
                            <b>Severidade:</b> {segment['severity']:.1f}/5.0<br>
                            <b>Risco:</b> <span style="color: {risk_color};">{risk_level.upper()}</span>
                        </div>
                        """,
                        max_width=200,
                    ),
                    tooltip=f"⚠️ Risco: {risk_level} - {segment.get('road_name', 'Via')}",
                ).add_to(map_obj)
    
    def _add_legend(self, map_obj: folium.Map, num_vehicles: int, show_accidents: bool = False) -> None:
        """
        Adiciona legenda ao mapa.
        
        Args:
            map_obj: Objeto do mapa Folium
            num_vehicles: Número de veículos
        """
        legend_html = """
        <div id="legend-panel" style="position: fixed; 
                    bottom: 10px; right: 10px; width: 220px; height: auto; 
                    background-color: rgba(255, 255, 255, 0.95); z-index:9999; 
                    border:2px solid #333; border-radius: 5px; padding: 10px;
                    font-size:11px; box-shadow: 0 2px 5px rgba(0,0,0,0.3);
                    max-height: 400px; overflow-y: auto;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <h4 style="margin:0; font-size:13px; color: #333;">🗺️ Legenda</h4>
            <button onclick="toggleLegend()" style="background: #333; color: white; border: none; 
                    border-radius: 3px; padding: 2px 8px; cursor: pointer; font-size: 10px;">−</button>
        </div>
        <div id="legend-content">
        <p style="margin:3px 0; font-weight: bold; color: #555;">🚚 Rotas dos Veículos:</p>
        """
        
        # Adicionar cores dos veículos
        for i in range(min(num_vehicles, len(self.ROUTE_COLORS))):
            color = self.ROUTE_COLORS[i]
            color_name = self.COLOR_NAMES.get(color, "Cor")
            legend_html += f"""
            <p style="margin:3px 0; padding-left: 5px;">
                <span style="color: {color}; font-weight: bold; font-size: 14px;">●</span>
                <b>Veículo {i + 1}</b> <span style="color: {color};">({color_name})</span>
            </p>
            """
        
        legend_html += """
        <hr style="margin: 8px 0; border-color: #ddd;">
        <p style="margin:3px 0; font-weight: bold; color: #555;">📍 Marcadores:</p>
        <p style="margin:3px 0; padding-left: 5px;">
            <i class="fas fa-exclamation-circle" style="color: red;"></i>
            <b>Entrega Crítica</b> (Medicamentos)
        </p>
        <p style="margin:3px 0; padding-left: 5px;">
            <i class="fas fa-map-marker-alt" style="color: blue;"></i>
            <b>Entrega Normal</b> (Insumos)
        </p>
        <p style="margin:3px 0; padding-left: 5px;">
            <i class="fas fa-warehouse" style="color: black;"></i>
            <b>Depósito</b> (Ponto de partida)
        </p>
        """
        
        if show_accidents:
            legend_html += """
        <hr style="margin: 8px 0; border-color: #ddd;">
        <p style="margin:3px 0; font-weight: bold; color: #555;">⚠️ Níveis de Risco:</p>
        <p style="margin:3px 0; padding-left: 5px;">
            <span style="color: #28a745; font-weight: bold;">●</span>
            <b>Baixo</b> (Low)
        </p>
        <p style="margin:3px 0; padding-left: 5px;">
            <span style="color: #ffc107; font-weight: bold;">●</span>
            <b>Médio</b> (Medium)
        </p>
        <p style="margin:3px 0; padding-left: 5px;">
            <span style="color: #fd7e14; font-weight: bold;">●</span>
            <b>Alto</b> (High)
        </p>
        <p style="margin:3px 0; padding-left: 5px;">
            <span style="color: #dc3545; font-weight: bold;">●</span>
            <b>Crítico</b> (Critical)
        </p>
        <p style="margin:3px 0; font-size: 10px; color: #666; padding-left: 5px;">
            <i>Ative a camada "Pontos de Acidentes" para ver todos os pontos</i>
        </p>
        """
        
        legend_html += """
        <hr style="margin: 8px 0; border-color: #ddd;">
        <p style="margin:3px 0; font-size: 10px; color: #666;">
            💡 <i>Clique nas linhas coloridas para ver detalhes das rotas</i>
        </p>
        </div>
        </div>
        <script>
        {% raw %}
        function toggleLegend() {{
            var content = document.getElementById('legend-content');
            var btn = event.target;
            if (content.style.display === 'none') {{
                content.style.display = 'block';
                btn.textContent = '−';
            }} else {{
                content.style.display = 'none';
                btn.textContent = '+';
            }}
        }}
        {% endraw %}
        </script>
        """
        # Escapar chaves duplas para evitar conflito com Jinja2
        map_obj.get_root().html.add_child(folium.Element(legend_html))
    
    def _add_route_highlight_script(
        self,
        map_obj: folium.Map,
        routes: List[List[str]],
        delivery_dict: dict,
        depot_location: Tuple[float, float],
    ) -> None:
        """
        Adiciona JavaScript para destacar rotas específicas via postMessage.
        
        Args:
            map_obj: Objeto do mapa Folium
            routes: Lista de rotas
            delivery_dict: Dicionário de entregas
            depot_location: Localização do depósito
        """
        # Preparar dados das rotas para JavaScript
        routes_data = []
        for route_idx, route in enumerate(routes):
            route_coords = [depot_location]
            for delivery_id in route:
                if delivery_id in delivery_dict:
                    route_coords.append(delivery_dict[delivery_id].location)
            route_coords.append(depot_location)
            
            routes_data.append({
                'vehicle_id': route_idx + 1,
                'coordinates': route_coords,
                'delivery_ids': route,
            })
        
        script_html = f"""
        <script>
        (function() {{
            // Dados das rotas
            const routesData = {routes_data};
            const depotLocation = {list(depot_location)};
            let highlightedVehicleId = null;
            let animationInterval = null;
            
            // Função para destacar uma rota específica
            function highlightRoute(vehicleId) {{
                // Parar animação anterior
                if (animationInterval) {{
                    clearInterval(animationInterval);
                    animationInterval = null;
                }}
                
                highlightedVehicleId = vehicleId;
                
                // Encontrar dados da rota
                const routeData = routesData.find(r => r.vehicle_id === vehicleId);
                if (!routeData) return;
                
                // Ocultar todas as rotas primeiro
                const allGroups = document.querySelectorAll('[class*="leaflet-layer"]');
                allGroups.forEach(group => {{
                    const polylines = group.querySelectorAll('path');
                    const markers = group.querySelectorAll('.leaflet-marker-icon');
                    const circles = group.querySelectorAll('circle');
                    
                    polylines.forEach(el => {{
                        if (el.getAttribute('stroke') && el.getAttribute('stroke') !== 'none') {{
                            el.style.opacity = '0.2';
                            el.style.filter = 'blur(2px)';
                        }}
                    }});
                    markers.forEach(el => {{
                        el.style.opacity = '0.2';
                    }});
                    circles.forEach(el => {{
                        el.style.opacity = '0.2';
                    }});
                }});
                
                // Destacar rota selecionada usando FeatureGroup
                setTimeout(() => {{
                    // Usar Leaflet API para mostrar/ocultar FeatureGroups
                    if (typeof map !== 'undefined') {{
                        // Ocultar todos os grupos de rotas
                        map.eachLayer(function(layer) {{
                            if (layer instanceof L.FeatureGroup) {{
                                const groupName = layer.options.name || '';
                                if (groupName.startsWith('route_vehicle_')) {{
                                    if (groupName === `route_vehicle_${{vehicleId}}`) {{
                                        // Mostrar rota destacada
                                        layer.eachLayer(function(sublayer) {{
                                            if (sublayer instanceof L.Polyline) {{
                                                sublayer.setStyle({{
                                                    opacity: 1,
                                                    weight: 8,
                                                    color: sublayer.options.color
                                                }});
                                            }} else if (sublayer instanceof L.Marker || sublayer instanceof L.CircleMarker) {{
                                                sublayer.setOpacity(1);
                                            }}
                                        }});
                                    }} else {{
                                        // Ocultar outras rotas
                                        layer.eachLayer(function(sublayer) {{
                                            if (sublayer instanceof L.Polyline) {{
                                                sublayer.setStyle({{
                                                    opacity: 0.3,  // Rotas não selecionadas: opacidade baixa
                                                    weight: 2  // Espessura reduzida
                                                }});
                                            }} else if (sublayer instanceof L.Marker || sublayer instanceof L.CircleMarker) {{
                                                sublayer.setOpacity(0.3);
                                            }}
                                        }});
                                    }}
                                }}
                            }}
                        }});
                    }}
                    
                    // Fazer zoom na rota
                    zoomToRoute(routeData.coordinates);
                    
                    // Iniciar animação
                    animateRoute(routeData.coordinates);
                }}, 100);
            }}
            
            // Função para restaurar todas as rotas
            function restoreAllRoutes() {{
                if (animationInterval) {{
                    clearInterval(animationInterval);
                    animationInterval = null;
                }}
                
                highlightedVehicleId = null;
                
                // Restaurar todos os FeatureGroups
                if (typeof map !== 'undefined') {{
                    map.eachLayer(function(layer) {{
                        if (layer instanceof L.FeatureGroup) {{
                            const groupName = layer.options.name || '';
                            if (groupName.startsWith('route_vehicle_')) {{
                                layer.setStyle({{
                                    opacity: 1
                                }});
                                layer.eachLayer(function(sublayer) {{
                                    if (sublayer instanceof L.Polyline) {{
                                        sublayer.setStyle({{
                                            opacity: 1.0,  // Rota destacada: opacidade 100%
                                            weight: 6  // Espessura maior para destaque
                                        }});
                                    }} else if (sublayer instanceof L.Marker || sublayer instanceof L.CircleMarker) {{
                                        sublayer.setOpacity(1);
                                    }}
                                }});
                            }}
                        }}
                    }});
                }}
            }}
            
            // Função para fazer zoom na rota
            function zoomToRoute(coordinates) {{
                if (typeof map === 'undefined') return;
                
                const bounds = L.latLngBounds(coordinates);
                map.fitBounds(bounds, {{ padding: [50, 50] }});
            }}
            
            // Função para animar o percurso
            function animateRoute(coordinates) {{
                if (animationInterval) clearInterval(animationInterval);
                
                // Criar linha animada
                let currentIndex = 0;
                const animatedLine = L.polyline([], {{
                    color: '#FFD700',
                    weight: 4,
                    opacity: 0.8,
                    dashArray: '10, 5'
                }}).addTo(map);
                
                animationInterval = setInterval(() => {{
                    if (currentIndex < coordinates.length) {{
                        animatedLine.addLatLng(coordinates[currentIndex]);
                        currentIndex++;
                    }} else {{
                        clearInterval(animationInterval);
                        animationInterval = null;
                        // Remover linha animada após 2 segundos
                        setTimeout(() => {{
                            map.removeLayer(animatedLine);
                        }}, 2000);
                    }}
                }}, 300);
            }}
            
            // Escutar mensagens do iframe pai
            window.addEventListener('message', function(event) {{
                if (event.data.type === 'highlight_route') {{
                    highlightRoute(event.data.vehicle_id);
                }} else if (event.data.type === 'restore_routes') {{
                    restoreAllRoutes();
                }} else if (event.data.type === 'show_delivery') {{
                    const location = event.data.location;
                    console.log('Recebida mensagem show_delivery:', location);
                    
                    if (!location || !Array.isArray(location) || location.length !== 2) {{
                        console.error('Localização inválida:', location);
                        return;
                    }}
                    
                    // Função para centralizar no mapa
                    function showDelivery() {{
                        // O Folium expõe o mapa como variável global
                        // Tentar diferentes formas de acessar
                        let mapInstance = null;
                        
                        // Método 1: Variável global 'map' (padrão do Folium)
                        if (typeof map !== 'undefined' && map && map.setView) {{
                            mapInstance = map;
                        }}
                        // Método 2: Procurar em window
                        else if (typeof window !== 'undefined') {{
                            // Procurar por variáveis que sejam instâncias de L.Map
                            for (let key in window) {{
                                try {{
                                    const obj = window[key];
                                    if (obj && typeof obj.setView === 'function' && typeof obj.getCenter === 'function') {{
                                        mapInstance = obj;
                                        break;
                                    }}
                                }} catch (e) {{
                                    // Continuar procurando
                                }}
                            }}
                        }}
                        
                        if (!mapInstance) {{
                            console.warn('Mapa não encontrado, tentando novamente em 200ms...');
                            setTimeout(showDelivery, 200);
                            return;
                        }}
                        
                        console.log('Mapa encontrado, centralizando...');
                        
                        // Verificar se Leaflet está disponível
                        if (typeof L === 'undefined') {{
                            console.warn('Leaflet não disponível, apenas centralizando...');
                            mapInstance.setView([location[0], location[1]], 15);
                            return;
                        }}
                        
                        // Remover marcador anterior se existir
                        if (window.deliveryMarker) {{
                            try {{
                                mapInstance.removeLayer(window.deliveryMarker);
                            }} catch (e) {{
                                // Ignorar erro
                            }}
                        }}
                        
                        // Criar marcador destacado
                        try {{
                            window.deliveryMarker = L.marker([location[0], location[1]], {{
                                icon: L.icon({{
                                    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
                                    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                                    iconSize: [25, 41],
                                    iconAnchor: [12, 41],
                                    popupAnchor: [1, -34],
                                    shadowSize: [41, 41]
                                }}),
                                zIndexOffset: 1000
                            }}).addTo(mapInstance);
                            
                            // Centralizar e fazer zoom
                            mapInstance.setView([location[0], location[1]], 15);
                            
                            // Abrir popup
                            window.deliveryMarker.bindPopup('📍 Localização da Entrega').openPopup();
                            
                            console.log('✅ Mapa centralizado com sucesso na localização:', location);
                        }} catch (error) {{
                            console.error('Erro ao criar marcador, apenas centralizando:', error);
                            // Ainda assim, centralizar o mapa
                            mapInstance.setView([location[0], location[1]], 15);
                        }}
                    }}
                    
                    // Aguardar um pouco para garantir que o mapa está carregado
                    if (document.readyState === 'complete') {{
                        showDelivery();
                    }} else {{
                        window.addEventListener('load', showDelivery);
                        // Timeout de segurança
                        setTimeout(showDelivery, 500);
                    }}
                }}
            }});
            
            // Expor funções globalmente para debug
            window.highlightRoute = highlightRoute;
            window.restoreAllRoutes = restoreAllRoutes;
        }})();
        </script>
        """
        map_obj.get_root().html.add_child(folium.Element(script_html))
    
    @staticmethod
    def generate_route_map(
        optimization_result: OptimizationResult,
        deliveries: List[Delivery],
        depot_location: Tuple[float, float],
        output_path: str = "route_map.html",
        title: str = "Rotas Otimizadas",
        center_location: Optional[Tuple[float, float]] = None,
        accident_provider: Optional[AccidentDataProvider] = None,
        show_accidents: bool = True,
    ) -> folium.Map:
        """
        Função estática conveniente para gerar mapa de rotas.
        
        Args:
            optimization_result: Resultado da otimização
            deliveries: Lista de entregas
            depot_location: Localização do depósito
            output_path: Caminho para salvar o mapa HTML
            title: Título do mapa
            center_location: Localização central (opcional)
        
        Returns:
            folium.Map: Mapa gerado
        
        Example:
            >>> from hospital_routes.visualization.map_generator import MapGenerator
            >>> map_obj = MapGenerator.generate_route_map(
            ...     result, deliveries, depot, "mapa.html"
            ... )
        """
        generator = MapGenerator(center_location=center_location)
        return generator.generate_map(
            optimization_result=optimization_result,
            deliveries=deliveries,
            depot_location=depot_location,
            output_path=output_path,
            title=title,
            accident_provider=accident_provider,
            show_accidents=show_accidents,
        )
