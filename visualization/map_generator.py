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


class MapGenerator:
    """
    Gera mapas interativos com Folium para visualização de rotas.
    
    Consome apenas DTOs, não entidades de domínio.
    """
    
    # Cores para diferentes veículos
    ROUTE_COLORS = [
        "blue",
        "red",
        "green",
        "purple",
        "orange",
        "darkred",
        "lightred",
        "beige",
        "darkblue",
        "darkgreen",
        "cadetblue",
        "darkpurple",
        "white",
        "pink",
        "lightblue",
        "lightgreen",
        "gray",
        "black",
        "lightgray",
    ]
    
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
        
        # Adicionar título
        title_html = f"""
        <div style="position: fixed; 
                    top: 10px; left: 50px; width: 300px; height: 90px; 
                    background-color: white; z-index:9999; 
                    border:2px solid grey; padding: 10px;
                    font-size:14px">
        <h4 style="margin-top:0">{title}</h4>
        <p style="margin:5px 0">
        <b>Distância Total:</b> {optimization_result.solution.total_distance:.2f} km<br>
        <b>Custo Total:</b> R$ {optimization_result.solution.total_cost:.2f}
        </p>
        </div>
        """
        m.get_root().html.add_child(folium.Element(title_html))
        
        # Adicionar depósito
        self._add_depot_marker(m, depot_location)
        
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
            )
        
        # Adicionar legenda
        self._add_legend(m, len(solution.routes))
        
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
        folium.Marker(
            location=depot_location,
            popup=folium.Popup(
                "<b>Depósito</b><br>Ponto de partida e retorno",
                max_width=200,
            ),
            tooltip="Depósito",
            icon=folium.Icon(
                color="black",
                icon="warehouse",
                prefix="fa",
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
        
        # Adicionar linha da rota
        folium.PolyLine(
            locations=route_coordinates,
            color=color,
            weight=4,
            opacity=0.7,
            popup=folium.Popup(
                f"<b>Veículo {vehicle_id}</b><br>"
                f"Entregas: {len(route)}<br>"
                f"Paradas: {', '.join(route)}",
                max_width=300,
            ),
            tooltip=f"Rota do Veículo {vehicle_id}",
        ).add_to(map_obj)
        
        # Adicionar marcadores para cada entrega
        for stop_idx, delivery_id in enumerate(route):
            if delivery_id not in delivery_dict:
                continue
            
            delivery = delivery_dict[delivery_id]
            is_critical = delivery.priority == 1
            
            # Ícone vermelho para entregas críticas
            if is_critical:
                icon_color = "red"
                icon_name = "exclamation-circle"
                priority_text = "CRÍTICA (Medicamentos)"
            else:
                icon_color = "blue"
                icon_name = "map-marker-alt"
                priority_text = "Normal"
            
            # Criar popup com informações
            popup_html = f"""
            <div style="font-size: 12px">
                <b>Entrega: {delivery_id}</b><br>
                <b>Prioridade: {priority_text}</b><br>
                Peso: {delivery.weight} kg<br>
                Parada {stop_idx + 1} na rota do Veículo {vehicle_id}
            </div>
            """
            
            # Criar ícone customizado com número da parada
            icon_html = f"""
            <div style="
                position: relative;
                width: 30px;
                height: 30px;
            ">
                <i class="fas fa-{icon_name}" 
                   style="
                       font-size: 24px;
                       color: {icon_color};
                       position: absolute;
                       top: 0;
                       left: 0;
                   "></i>
                <div style="
                    position: absolute;
                    top: 8px;
                    left: 8px;
                    background-color: white;
                    border: 1px solid {icon_color};
                    border-radius: 50%;
                    width: 14px;
                    height: 14px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: bold;
                    font-size: 9px;
                    color: {icon_color};
                ">{stop_idx + 1}</div>
            </div>
            """
            
            folium.Marker(
                location=delivery.location,
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=f"{delivery_id} - Parada {stop_idx + 1} ({priority_text})",
                icon=folium.DivIcon(
                    html=icon_html,
                    icon_size=(30, 30),
                    icon_anchor=(15, 15),
                ),
            ).add_to(map_obj)
    
    def _add_legend(self, map_obj: folium.Map, num_vehicles: int) -> None:
        """
        Adiciona legenda ao mapa.
        
        Args:
            map_obj: Objeto do mapa Folium
            num_vehicles: Número de veículos
        """
        legend_html = """
        <div style="position: fixed; 
                    bottom: 50px; right: 50px; width: 200px; height: auto; 
                    background-color: white; z-index:9999; 
                    border:2px solid grey; padding: 10px;
                    font-size:12px">
        <h4 style="margin-top:0">Legenda</h4>
        """
        
        # Adicionar cores dos veículos
        for i in range(min(num_vehicles, len(self.ROUTE_COLORS))):
            color = self.ROUTE_COLORS[i]
            legend_html += f"""
            <p style="margin:5px 0">
                <span style="color: {color}; font-weight: bold;">●</span>
                Veículo {i + 1}
            </p>
            """
        
        legend_html += """
        <hr style="margin: 10px 0">
        <p style="margin:5px 0">
            <i class="fas fa-exclamation-circle" style="color: red;"></i>
            Entrega Crítica
        </p>
        <p style="margin:5px 0">
            <i class="fas fa-map-marker-alt"></i>
            Entrega Normal
        </p>
        <p style="margin:5px 0">
            <i class="fas fa-warehouse"></i>
            Depósito
        </p>
        </div>
        """
        
        map_obj.get_root().html.add_child(folium.Element(legend_html))
    
    @staticmethod
    def generate_route_map(
        optimization_result: OptimizationResult,
        deliveries: List[Delivery],
        depot_location: Tuple[float, float],
        output_path: str = "route_map.html",
        title: str = "Rotas Otimizadas",
        center_location: Optional[Tuple[float, float]] = None,
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
        )
