"""
Configurações centralizadas do projeto Aurum
============================================

Todos os paths, constantes e parâmetros configuráveis ficam aqui.
"""

import os
from pathlib import Path
from dataclasses import dataclass
from typing import List


# ============================================
# PATHS - Estrutura de diretórios
# ============================================

class PATHS:
    """Centraliza todos os caminhos de arquivos e diretórios"""

    # Diretório raiz do projeto
    BASE_DIR = Path(__file__).parent.parent.parent

    # Diretórios de dados
    DATA_DIR = BASE_DIR / "data"
    HIST_DIR = DATA_DIR / "historical"
    NEWS_DIR = DATA_DIR / "news"
    CVM_DIR = DATA_DIR / "cvm"
    FUNDAMENTALS_DIR = DATA_DIR / "fundamentals"

    # Diretórios de trabalho
    CACHE_DIR = DATA_DIR / ".cache"
    LOGS_DIR = BASE_DIR / "logs"

    # Criar diretórios automaticamente
    @classmethod
    def create_all(cls):
        """Cria todos os diretórios necessários"""
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if isinstance(attr, Path) and attr_name.endswith('_DIR'):
                attr.mkdir(parents=True, exist_ok=True)


# ============================================
# DOWNLOAD CONFIG - Parâmetros de download
# ============================================

@dataclass
class DownloadConfig:
    """Configurações para download de dados históricos"""

    # Data inicial padrão para históricos
    DEFAULT_START: str = "2011-01-01"

    # Tamanho do batch para download paralelo
    BATCH_SIZE: int = 15

    # Número de tentativas em caso de falha
    MAX_ATTEMPTS: int = 4

    # Tempo de espera entre batches (segundos)
    SLEEP_BETWEEN_BATCHES: float = 1.0

    # Tempo de espera entre tickers (segundos)
    SLEEP_BETWEEN_TICKERS: float = 0.2

    # Salvar também em CSV (além de parquet)
    SAVE_CSV: bool = True

    # Forçar re-download de dados existentes
    FORCE_REDOWNLOAD: bool = False


# ============================================
# SENTIMENT CONFIG - Análise de sentimento
# ============================================

@dataclass
class SentimentConfig:
    """Configurações para análise de sentimento"""

    # Modelos candidatos (ordem de preferência)
    MODEL_CANDIDATES: List[str] = None

    # Tamanho do batch para inferência
    BATCH_SIZE: int = 64

    # Limite de caracteres por texto
    MAX_CHARS: int = 2000

    # Limite de tokens (se usar tokenizer)
    TRUNCATE_TOKENS: int = 512

    # Palavras positivas para fallback lexicon
    POS_WORDS: set = None

    # Palavras negativas para fallback lexicon
    NEG_WORDS: set = None

    def __post_init__(self):
        if self.MODEL_CANDIDATES is None:
            self.MODEL_CANDIDATES = [
                "cardiffnlp/twitter-xlm-roberta-base-sentiment",
                "lipaoMai/BERT-sentiment-analysis-portuguese-with-undersampling-v2",
                "pysentimiento/bertweet-pt-sentiment",
                "nlptown/bert-base-multilingual-uncased-sentiment",
            ]

        if self.POS_WORDS is None:
            self.POS_WORDS = {
                "bom", "ótimo", "excelente", "positivo", "cresceu",
                "alta", "superior", "melhor", "lucro", "recupera"
            }

        if self.NEG_WORDS is None:
            self.NEG_WORDS = {
                "ruim", "queda", "prejuízo", "redução", "negativo",
                "menor", "rebaixamento", "perda", "crise", "dívida"
            }


# ============================================
# URLs - Endpoints e fontes de dados
# ============================================

class URLs:
    """URLs das fontes de dados"""

    # B3 - Composição de índices
    B3_INDEX_BASE = "https://sistemaswebb3-listados.b3.com.br/indexPage/day/{index}?language=en-us"

    # Placeholders de índices
    IBRX100 = "IBRX100"
    IBOV = "IBOV"

    @classmethod
    def get_index_url(cls, index_code: str) -> str:
        """Retorna URL formatada para um índice específico"""
        return cls.B3_INDEX_BASE.format(index=index_code)


# ============================================
# TICKER CONFIG - Normalização de tickers
# ============================================

class TickerConfig:
    """Configurações para tickers"""

    # Sufixo padrão para ações brasileiras
    DEFAULT_SUFFIX = ".SA"

    # Regex para validação de tickers
    TICKER_PATTERN = r'^[A-Z]{2,6}\d{1,2}$'

    # Keywords para identificar colunas de ticker
    HEADER_KEYWORDS = {
        "code", "stock", "ativo", "código", "codigo",
        "symbol", "ticker"
    }


# ============================================
# LOGGING CONFIG - Configuração de logs
# ============================================

@dataclass
class LoggingConfig:
    """Configurações de logging"""

    # Nível de log padrão
    LEVEL: str = "INFO"

    # Formato de log
    FORMAT: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"

    # Formato de data
    DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    # Salvar logs em arquivo
    SAVE_TO_FILE: bool = True

    # Nome do arquivo de log
    LOG_FILENAME: str = "aurum.log"

    # Rotação de logs (tamanho máximo em bytes)
    MAX_BYTES: int = 10 * 1024 * 1024  # 10 MB

    # Número de backups de log
    BACKUP_COUNT: int = 5


# ============================================
# INICIALIZAÇÃO
# ============================================

# Criar diretórios ao importar
PATHS.create_all()

# Instâncias padrão
download_config = DownloadConfig()
sentiment_config = SentimentConfig()
logging_config = LoggingConfig()