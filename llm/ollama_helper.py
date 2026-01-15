"""
Helper para gerenciar modelos Ollama e detectar modelos disponíveis.
"""

from typing import List, Optional, Dict
import subprocess
import sys


def list_available_models() -> List[str]:
    """
    Lista modelos Ollama disponíveis localmente.
    
    Returns:
        List[str]: Lista de nomes de modelos disponíveis (sem tags)
    """
    try:
        import ollama
        response = ollama.list()
        
        # Converter para dict se necessário
        if hasattr(response, 'model_dump'):
            data = response.model_dump()
        elif hasattr(response, 'dict'):
            data = response.dict()
        else:
            data = dict(response) if hasattr(response, '__dict__') else {}
        
        model_names = []
        models_list = data.get('models', [])
        
        for m in models_list:
            # O campo pode ser 'model' ou 'name'
            name = m.get('model') or m.get('name', '')
            if not name:
                continue
            
            # Remover tag :latest ou outras tags
            if ':' in name:
                name = name.split(':')[0]
            model_names.append(name)
        
        # Remover duplicatas mantendo ordem
        seen = set()
        unique_models = []
        for name in model_names:
            if name and name not in seen:
                seen.add(name)
                unique_models.append(name)
        
        return unique_models
    except Exception as e:
        # Em caso de erro, retornar lista vazia
        return []


def get_best_available_model(preferred: Optional[List[str]] = None) -> Optional[str]:
    """
    Retorna o melhor modelo disponível, tentando os preferidos primeiro.
    
    Args:
        preferred: Lista de modelos preferidos em ordem de prioridade
    
    Returns:
        str: Nome do modelo disponível (sem tags) ou None
    """
    if preferred is None:
        preferred = ["llama3.2", "llama3.1", "llama3", "mistral", "phi3", "gemma2"]
    
    available = list_available_models()
    
    # Tentar modelos preferidos primeiro
    for model in preferred:
        if model in available:
            return model
    
    # Se nenhum preferido disponível, retornar o primeiro disponível
    if available:
        return available[0]
    
    return None


def suggest_model_installation() -> str:
    """
    Retorna sugestão de comando para instalar modelo.
    
    Returns:
        str: Comando sugerido
    """
    return "ollama pull llama3.2"


def check_ollama_running() -> bool:
    """
    Verifica se o Ollama está rodando.
    
    Returns:
        bool: True se Ollama está rodando
    """
    try:
        import ollama
        ollama.list()  # Tentar listar modelos
        return True
    except Exception:
        return False


def get_model_full_name(model_name: str) -> Optional[str]:
    """
    Retorna o nome completo do modelo (com tag) para uso em chamadas.
    
    Args:
        model_name: Nome do modelo sem tag (ex: "llama3.2")
    
    Returns:
        str: Nome completo do modelo (ex: "llama3.2:latest") ou None
    """
    try:
        import ollama
        response = ollama.list()
        
        # Converter para dict se necessário
        if hasattr(response, 'model_dump'):
            data = response.model_dump()
        elif hasattr(response, 'dict'):
            data = response.dict()
        else:
            data = dict(response) if hasattr(response, '__dict__') else {}
        
        for model in data.get('models', []):
            model_full_name = model.get('model') or model.get('name', '')
            # Comparar base (sem tag)
            model_base_name = model_full_name.split(':')[0] if ':' in model_full_name else model_full_name
            if model_base_name == model_name:
                return model_full_name  # Retornar nome completo com tag
        return None
    except Exception:
        return None


def get_model_info(model_name: str) -> Optional[Dict]:
    """
    Obtém informações sobre um modelo específico.
    
    Args:
        model_name: Nome do modelo (com ou sem tag)
    
    Returns:
        dict: Informações do modelo ou None
    """
    try:
        import ollama
        response = ollama.list()
        
        # Converter para dict se necessário
        if hasattr(response, 'model_dump'):
            data = response.model_dump()
        elif hasattr(response, 'dict'):
            data = response.dict()
        else:
            data = dict(response) if hasattr(response, '__dict__') else {}
        
        for model in data.get('models', []):
            model_full_name = model.get('model') or model.get('name', '')
            # Comparar com ou sem tag
            model_base_name = model_full_name.split(':')[0] if ':' in model_full_name else model_full_name
            if model_base_name == model_name or model_full_name == model_name:
                return model
        return None
    except Exception:
        return None
