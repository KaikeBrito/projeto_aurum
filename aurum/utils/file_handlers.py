"""
Utilitários para manipulação de arquivos
========================================

Funções para salvar/carregar DataFrames em parquet e CSV,
com normalização de datas e validações.
"""

import logging
import os
from pathlib import Path
from typing import Optional, List, Union
from datetime import datetime

import pandas as pd

from aurum.config.settings import PATHS

logger = logging.getLogger(__name__)


def save_dataframe(
    df: pd.DataFrame,
    ticker: str,
    directory: Union[str, Path],
    save_csv: bool = True,
    date_column: str = "date"
) -> tuple[Path, Optional[Path]]:
    """
    Salva DataFrame em parquet e opcionalmente em CSV

    Args:
        df: DataFrame a ser salvo
        ticker: Nome do ticker (usado no nome do arquivo)
        directory: Diretório de destino
        save_csv: Se True, salva também em CSV
        date_column: Nome da coluna de data para normalização

    Returns:
        tuple: (caminho_parquet, caminho_csv ou None)

    Raises:
        ValueError: Se DataFrame for None ou vazio

    Example:
        >>> df = pd.DataFrame({'date': [...], 'Close': [...]})
        >>> parquet_path, csv_path = save_dataframe(df, "PETR4.SA", "data/historical")
    """
    if df is None or df.empty:
        raise ValueError(f"DataFrame vazio para ticker {ticker}")

    df = df.copy()
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)

    # Normalizar índice de data se necessário
    if isinstance(df.index, pd.DatetimeIndex):
        df.index.name = date_column
        df = df.reset_index()

    # Salvar parquet
    parquet_path = directory / f"{ticker}.parquet"
    try:
        df.to_parquet(parquet_path, index=False, compression='snappy')
        logger.info(f"Saved {len(df)} rows for {ticker} -> {parquet_path}")
    except Exception as e:
        logger.exception(f"Erro salvando parquet para {ticker}: {e}")
        raise

    # Salvar CSV (opcional)
    csv_path = None
    if save_csv:
        csv_path = directory / f"{ticker}.csv"
        try:
            df_csv = df.copy()
            # Normalizar datas para formato ISO
            if date_column in df_csv.columns:
                df_csv[date_column] = pd.to_datetime(
                    df_csv[date_column], errors='coerce'
                ).dt.strftime('%Y-%m-%d')
            df_csv.to_csv(csv_path, index=False)
            logger.debug(f"Saved CSV for {ticker} -> {csv_path}")
        except Exception as e:
            logger.warning(f"Erro salvando CSV para {ticker}: {e}")
            # Não propagar erro - parquet já foi salvo

    return parquet_path, csv_path


def load_dataframe(
    ticker: str,
    directory: Union[str, Path],
    parse_dates: Optional[List[str]] = None
) -> Optional[pd.DataFrame]:
    """
    Carrega DataFrame de arquivo parquet

    Args:
        ticker: Nome do ticker
        directory: Diretório onde está o arquivo
        parse_dates: Lista de colunas para converter em datetime

    Returns:
        DataFrame carregado ou None se não existir

    Example:
        >>> df = load_dataframe("PETR4.SA", "data/historical", parse_dates=['date'])
    """
    path = Path(directory) / f"{ticker}.parquet"

    if not path.exists():
        logger.debug(f"Arquivo não encontrado: {path}")
        return None

    try:
        df = pd.read_parquet(path)

        # Converter colunas de data
        if parse_dates:
            for col in parse_dates:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce')

        logger.debug(f"Loaded {len(df)} rows from {path}")
        return df

    except Exception as e:
        logger.error(f"Erro carregando {path}: {e}")
        return None


def ticker_exists(ticker: str, directory: Union[str, Path]) -> bool:
    """
    Verifica se arquivo parquet existe para o ticker

    Args:
        ticker: Nome do ticker
        directory: Diretório para verificar

    Returns:
        True se arquivo existe, False caso contrário

    Example:
        >>> if ticker_exists("PETR4.SA", "data/historical"):
        ...     print("Já foi baixado")
    """
    path = Path(directory) / f"{ticker}.parquet"
    return path.exists()


def combine_parquets(
    directory: Union[str, Path],
    output_path: Union[str, Path],
    tickers: Optional[List[str]] = None,
    add_ticker_column: bool = True,
    save_csv: bool = True
) -> pd.DataFrame:
    """
    Combina múltiplos arquivos parquet em um único arquivo

    Args:
        directory: Diretório contendo os parquets
        output_path: Caminho do arquivo de saída
        tickers: Lista de tickers específicos (None = todos)
        add_ticker_column: Se True, adiciona coluna 'ticker'
        save_csv: Se True, salva também em CSV

    Returns:
        DataFrame combinado

    Raises:
        RuntimeError: Se nenhum parquet for encontrado

    Example:
        >>> combined = combine_parquets(
        ...     "data/historical",
        ...     "data/all_histories.parquet",
        ...     tickers=["PETR4.SA", "VALE3.SA"]
        ... )
    """
    directory = Path(directory)
    output_path = Path(output_path)

    # Descobrir arquivos
    if tickers:
        files = [
            directory / f"{ticker}.parquet"
            for ticker in tickers
            if (directory / f"{ticker}.parquet").exists()
        ]
    else:
        files = list(directory.glob("*.parquet"))
        # Excluir arquivo de saída se estiver no mesmo diretório
        files = [f for f in files if f != output_path]

    if not files:
        raise RuntimeError(f"Nenhum parquet encontrado em {directory}")

    logger.info(f"Combinando {len(files)} arquivos parquet...")

    # Ler e combinar
    dfs = []
    for file_path in files:
        try:
            df = pd.read_parquet(file_path)

            # Adicionar coluna ticker se necessário
            if add_ticker_column and 'ticker' not in df.columns:
                ticker_name = file_path.stem  # nome sem extensão
                df.insert(0, 'ticker', ticker_name)

            # Normalizar coluna de data
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'], errors='coerce')

            dfs.append(df)

        except Exception as e:
            logger.warning(f"Erro lendo {file_path}: {e}")
            continue

    if not dfs:
        raise RuntimeError("Nenhum DataFrame válido foi carregado")

    # Concatenar
    combined = pd.concat(dfs, ignore_index=True, sort=False)

    # Salvar parquet
    output_path.parent.mkdir(parents=True, exist_ok=True)
    combined.to_parquet(output_path, index=False, compression='snappy')
    logger.info(f"Combined parquet saved: {output_path} ({len(combined)} rows)")

    # Salvar CSV
    if save_csv:
        csv_path = output_path.with_suffix('.csv')
        df_csv = combined.copy()
        if 'date' in df_csv.columns:
            df_csv['date'] = pd.to_datetime(
                df_csv['date'], errors='coerce'
            ).dt.strftime('%Y-%m-%d')
        df_csv.to_csv(csv_path, index=False)
        logger.info(f"Combined CSV saved: {csv_path}")

    return combined


def save_summary(
    summary_df: pd.DataFrame,
    directory: Union[str, Path],
    filename: Optional[str] = None
) -> Path:
    """
    Salva DataFrame de resumo com timestamp

    Args:
        summary_df: DataFrame com resumo
        directory: Diretório de destino
        filename: Nome do arquivo (None = gera com timestamp)

    Returns:
        Caminho do arquivo salvo

    Example:
        >>> summary = pd.DataFrame({'ticker': [...], 'status': [...]})
        >>> path = save_summary(summary, "data/historical")
    """
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)

    if filename is None:
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        filename = f"download_summary_{timestamp}.csv"

    output_path = directory / filename
    summary_df.to_csv(output_path, index=False)
    logger.info(f"Summary saved: {output_path}")

    return output_path


def get_latest_summary(directory: Union[str, Path]) -> Optional[pd.DataFrame]:
    """
    Carrega o resumo mais recente de download

    Args:
        directory: Diretório onde estão os resumos

    Returns:
        DataFrame do resumo mais recente ou None
    """
    directory = Path(directory)
    summaries = sorted(directory.glob("download_summary_*.csv"), reverse=True)

    if not summaries:
        return None

    return pd.read_csv(summaries[0])