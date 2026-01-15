"""
Sistema de logging estruturado para o projeto.

Fornece logging configurável com níveis, formatação e rotação de arquivos.
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional


def setup_logger(
    name: str = "hospital_routes",
    level: str = "INFO",
    log_file: Optional[str] = None,
    log_dir: str = "logs",
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
) -> logging.Logger:
    """
    Configura e retorna um logger estruturado.
    
    Args:
        name: Nome do logger
        level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Nome do arquivo de log (None = não salva em arquivo)
        log_dir: Diretório para salvar logs
        max_bytes: Tamanho máximo do arquivo antes de rotacionar
        backup_count: Número de arquivos de backup a manter
    
    Returns:
        logging.Logger: Logger configurado
    """
    logger = logging.getLogger(name)
    
    # Converter string de nível para constante
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Evitar duplicação de handlers
    if logger.handlers:
        return logger
    
    # Formato estruturado
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    # Handler para console (stderr)
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para arquivo (se especificado)
    if log_file:
        log_dir_path = Path(log_dir)
        log_dir_path.mkdir(parents=True, exist_ok=True)
        
        log_file_path = log_dir_path / log_file
        
        file_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Retorna um logger configurado.
    
    Se o logger não existir, cria um novo com configuração padrão.
    
    Args:
        name: Nome do logger (None = usa nome do módulo chamador)
    
    Returns:
        logging.Logger: Logger configurado
    """
    if name is None:
        # Tentar obter nome do módulo chamador
        import inspect
        frame = inspect.currentframe().f_back
        name = frame.f_globals.get("__name__", "hospital_routes")
    
    logger = logging.getLogger(name)
    
    # Se não tem handlers, configurar
    if not logger.handlers:
        setup_logger(name)
    
    return logger
