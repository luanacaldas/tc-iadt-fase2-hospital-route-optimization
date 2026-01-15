"""
Sistema de cache para distâncias e outros cálculos custosos.

Implementa cache LRU em memória com opção de persistência.
"""

from functools import lru_cache, wraps
from typing import Callable, Dict, Tuple, Any, Optional
import json
from pathlib import Path
import hashlib


class DistanceCache:
    """
    Cache para cálculos de distância.
    
    Usa LRU cache em memória com opção de persistência em arquivo.
    """
    
    def __init__(self, maxsize: int = 1000, persist_file: Optional[str] = None):
        """
        Args:
            maxsize: Tamanho máximo do cache em memória
            persist_file: Arquivo para persistir cache (None = não persiste)
        """
        self.maxsize = maxsize
        self.persist_file = persist_file
        self._cache: Dict[str, float] = {}
        self._load_cache()
    
    def _cache_key(self, loc1: Tuple[float, float], loc2: Tuple[float, float]) -> str:
        """Gera chave de cache para duas localizações."""
        # Normalizar coordenadas (sempre menor -> maior)
        coords = tuple(sorted([loc1, loc2]))
        return f"{coords[0][0]:.6f},{coords[0][1]:.6f}|{coords[1][0]:.6f},{coords[1][1]:.6f}"
    
    def get(self, loc1: Tuple[float, float], loc2: Tuple[float, float]) -> Optional[float]:
        """
        Obtém distância do cache.
        
        Args:
            loc1: Primeira localização (lat, lon)
            loc2: Segunda localização (lat, lon)
        
        Returns:
            Distância em km ou None se não estiver no cache
        """
        key = self._cache_key(loc1, loc2)
        return self._cache.get(key)
    
    def set(self, loc1: Tuple[float, float], loc2: Tuple[float, float], distance: float) -> None:
        """
        Armazena distância no cache.
        
        Args:
            loc1: Primeira localização
            loc2: Segunda localização
            distance: Distância em km
        """
        key = self._cache_key(loc1, loc2)
        
        # Se cache está cheio, remover item mais antigo (FIFO simples)
        if len(self._cache) >= self.maxsize and key not in self._cache:
            # Remover primeiro item
            first_key = next(iter(self._cache))
            del self._cache[first_key]
        
        self._cache[key] = distance
        self._save_cache()
    
    def clear(self) -> None:
        """Limpa o cache."""
        self._cache.clear()
        if self.persist_file and Path(self.persist_file).exists():
            Path(self.persist_file).unlink()
    
    def _load_cache(self) -> None:
        """Carrega cache do arquivo se existir."""
        if not self.persist_file:
            return
        
        cache_file = Path(self.persist_file)
        if cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    self._cache = json.load(f)
            except Exception:
                # Se houver erro, começar com cache vazio
                self._cache = {}
    
    def _save_cache(self) -> None:
        """Salva cache no arquivo."""
        if not self.persist_file:
            return
        
        try:
            cache_file = Path(self.persist_file)
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(self._cache, f)
        except Exception:
            # Falha silenciosa - cache em memória continua funcionando
            pass
    
    def stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do cache."""
        return {
            "size": len(self._cache),
            "maxsize": self.maxsize,
            "persist_file": self.persist_file,
        }


# Instância global do cache
_global_cache: Optional[DistanceCache] = None


def get_distance_cache(maxsize: int = 1000, persist_file: Optional[str] = None) -> DistanceCache:
    """
    Obtém instância global do cache de distâncias.
    
    Args:
        maxsize: Tamanho máximo (usado apenas na primeira chamada)
        persist_file: Arquivo de persistência (usado apenas na primeira chamada)
    
    Returns:
        DistanceCache: Instância do cache
    """
    global _global_cache
    if _global_cache is None:
        _global_cache = DistanceCache(maxsize=maxsize, persist_file=persist_file)
    return _global_cache


def cached_distance(func: Callable) -> Callable:
    """
    Decorator para cachear resultados de funções de distância.
    
    Usage:
        @cached_distance
        def calculate_distance(loc1, loc2):
            ...
    """
    cache = get_distance_cache()
    
    @wraps(func)
    def wrapper(loc1: Tuple[float, float], loc2: Tuple[float, float]) -> float:
        # Verificar cache
        cached = cache.get(loc1, loc2)
        if cached is not None:
            return cached
        
        # Calcular e cachear
        distance = func(loc1, loc2)
        cache.set(loc1, loc2, distance)
        return distance
    
    return wrapper
