import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO
from typing import Final

SP500_URL: Final[str] = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
NASDAQ_LISTED_URL: Final[str] = "https://www.nasdaqtrader.com/dynamic/symdir/nasdaqlisted.txt"
SYMBOLS_PATH: Final[str] = "./data/symbols.csv"


def fetch_symbols_nasdaq():
    """
    creates and returns a dataframe containing ticker symbols for stocks listed on NASDAQ

    :return: DataFrame
    """

    df = pd.read_csv(NASDAQ_LISTED_URL, sep='|')[:-1]  # removes the footer
    df_symbols = df[["Symbol"]]
    return df_symbols


def fetch_symbols_sp500():
    """
    creates and returns a dataframe containing ticker symbols for stocks listed on S&P 500

    :return: DataFrame
    """

    response = requests.get(SP500_URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "constituents"})

    df = pd.read_html(StringIO(str(table)))[0]
    df_symbols = df[["Symbol"]]
    return df_symbols


def fetch_symbols():
    """
    combines symbols from different sources into a single dataframe, dropping any duplicates.
    :return: Dataframe
    """

    try:
        nasdaq = fetch_symbols_nasdaq()
        sp500 = fetch_symbols_sp500()

        df = pd.concat([nasdaq, sp500]).drop_duplicates().reset_index(drop=True)

        return df
    except Exception as e:
        print(f"Error fetching symbols: {e}")


def download_symbols(path=SYMBOLS_PATH):
    """
    Downloads and saves stock symbols to a csv file.
    """

    df = fetch_symbols()
    try:
        df.to_csv(path, index=False)
    except Exception as e:
        print(f"Error downloading symbols: {e}")


if __name__ == "__main__":
    print()
    download_symbols()
