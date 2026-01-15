"""Visualization module for route mapping and plotting."""

from hospital_routes.visualization.map_generator import (
    MapGenerator,
    MapGenerator as RouteMapGenerator,
)

try:
    from hospital_routes.visualization.timeline_generator import (
        TimelineGenerator,
        TimelineEvent,
    )
except ImportError:
    TimelineGenerator = None
    TimelineEvent = None

try:
    from hospital_routes.visualization.scenario_comparator import (
        ScenarioComparator,
        ScenarioComparison,
    )
except ImportError:
    ScenarioComparator = None
    ScenarioComparison = None

try:
    from hospital_routes.visualization.vehicle_tracker import (
        VehicleTracker,
        VehicleTracking,
        VehicleStatus,
    )
except ImportError:
    VehicleTracker = None
    VehicleTracking = None
    VehicleStatus = None

try:
    from hospital_routes.visualization.report_exporter import ReportExporter
except ImportError:
    ReportExporter = None

try:
    from hospital_routes.visualization.chatbot_interface import ChatbotWebInterface
    __all__ = ["MapGenerator", "RouteMapGenerator", "ChatbotWebInterface"]
except ImportError:
    __all__ = ["MapGenerator", "RouteMapGenerator"]

