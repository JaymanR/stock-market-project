import yahoo_fin as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO
from typing import Final
from yahoo_fin import stock_info as si

SP500_URL: Final[str] = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

def fetch_symbols_nasdaq():
    """
    fetches dataframe containing ticker symbols for stocks listed on NASDAQ

    :return: DataFrame with ticker and index values
    """

    df = pd.DataFrame(si.tickers_nasdaq(), columns=["Symbol"])
    df["Index"] = "NASDAQ"
    return df

def fetch_symbols_sp500():
    """
    fetches dataframe containing ticker symbols for stocks listed on S&P 500

    :return: DataFrame with ticker and index values
    """

    response = requests.get(SP500_URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "constituents"})

    df = pd.read_html(StringIO(str(table)))[0]
    print(f"{df.head}")
    df["Index"] = "S&P 500"
    return df

def fetch_tickers():

    try:
        nasdaq = fetch_symbols_nasdaq()
        #sp500 = fetch_tickers_sp500()
        print(f"NASDAQ Stocks: \n{nasdaq.count()}")

        return nasdaq
    except Exception as e:
        print(f"Error fetching tickers: {e}")

def fetch_stock_data(start_date = None, end_date = None,
                     index_as_date = True, interval = "1d"):

    tickers = fetch_tickers()

    data = si.get_data(tickers, start_date, end_date, index_as_date, interval)

    print(f"Data: \n{data}")

if __name__ == "__main__":
    fetch_symbols_sp500()