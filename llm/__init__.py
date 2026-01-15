"""LLM-based report generation module."""

from hospital_routes.llm.base_reporter import BaseReporter

# Importações opcionais - apenas se as dependências estiverem disponíveis
__all__ = ["BaseReporter"]

try:
    from hospital_routes.llm.openai_reporter import OpenAIReporter
    __all__.append("OpenAIReporter")
except ImportError:
    # OpenAI/LangChain não está disponível
    pass

try:
    from hospital_routes.llm.ollama_reporter import OllamaReporter
    __all__.append("OllamaReporter")
except ImportError:
    # Ollama não está disponível
    pass

try:
    from hospital_routes.llm.chatbot import RouteChatbot, RouteAnalyzer
    __all__.extend(["RouteChatbot", "RouteAnalyzer"])
except ImportError:
    # Ollama não está disponível
    pass

try:
    from hospital_routes.llm.ollama_helper import (
        list_available_models,
        get_best_available_model,
        check_ollama_running,
    )
    __all__.extend(["list_available_models", "get_best_available_model", "check_ollama_running"])
except ImportError:
    pass
