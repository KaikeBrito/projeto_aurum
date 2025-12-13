import os
from pathlib import Path

# Diretórios base
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
HIST_DIR = DATA_DIR / "historical"
NEWS_DIR = DATA_DIR / "news"

# Criar diretórios automaticamente
for directory in [HIST_DIR, NEWS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Parâmetros de download
class DownloadConfig:
    DEFAULT_START = "2011-01-01"
    BATCH_SIZE = 15
    MAX_ATTEMPTS = 4
    SLEEP_BETWEEN_BATCHES = 1
    SLEEP_BETWEEN_TICKERS = 0.2

# URLs
class URLs:
    B3_IFRAME = "https://sistemaswebb3-listados.b3.com.br/indexPage/day/{index}?language=en-us"
    
# Modelos de sentimento
SENTIMENT_MODELS = [
    "cardiffnlp/twitter-xlm-roberta-base-sentiment",
    "pysentimiento/bertweet-pt-sentiment",
]