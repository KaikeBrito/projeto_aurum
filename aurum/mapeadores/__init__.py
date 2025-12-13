"""
Sistema de Mapeamento Ticker ↔ CNPJ
Versão: 1.0.0
Author: Aurum Team
"""

from .config import MappingConfig
from .create_map import TickerCNPJMapper

__version__ = "1.0.0"
__all__ = ["MappingConfig", "TickerCNPJMapper"]
