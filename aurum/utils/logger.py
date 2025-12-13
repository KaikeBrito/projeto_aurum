"""
Sistema de logging configuravel para o projeto
==============================================

Configura logging com suporte a console e arquivo, com rotacao automatica.
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional

from aurum.config.settings import LoggingConfig, PATHS


_logger_initialized = False


def setup_logger(
    name: Optional[str] = None,
    level: Optional[str] = None,
    log_to_file: bool = True,
    log_to_console: bool = True
) -> logging.Logger:
    """
    Configura o sistema de logging

    Args:
        name: Nome do logger (None = root logger)
        level: Nivel de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Se True, salva logs em arquivo
        log_to_console: Se True, exibe logs no console

    Returns:
        Logger configurado

    Example:
        >>> logger = setup_logger('aurum', level='DEBUG')
        >>> logger.info("Sistema iniciado")
    """
    global _logger_initialized

    config = LoggingConfig()
    log_level = level or config.LEVEL

    # Obter logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))

    # Evitar duplicacao de handlers
    if _logger_initialized and name is None:
        return logger

    # Limpar handlers existentes
    logger.handlers.clear()

    # Formatter
    formatter = logging.Formatter(
        fmt=config.FORMAT,
        datefmt=config.DATE_FORMAT
    )

    # Console handler
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handler (com rotacao)
    if log_to_file and config.SAVE_TO_FILE:
        PATHS.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        log_file = PATHS.LOGS_DIR / config.LOG_FILENAME

        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=config.MAX_BYTES,
            backupCount=config.BACKUP_COUNT,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Evitar propagacao para root logger
    logger.propagate = False

    if name is None:
        _logger_initialized = True

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Retorna logger com nome especifico

    Args:
        name: Nome do modulo (use __name__)

    Returns:
        Logger configurado

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Processando dados")
    """
    return logging.getLogger(name)


def set_level(level: str, name: Optional[str] = None):
    """
    Altera nivel de log dinamicamente

    Args:
        level: Novo nivel (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        name: Nome do logger (None = root logger)

    Example:
        >>> set_level('DEBUG')  # Ativa modo debug
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    for handler in logger.handlers:
        handler.setLevel(getattr(logging, level.upper()))