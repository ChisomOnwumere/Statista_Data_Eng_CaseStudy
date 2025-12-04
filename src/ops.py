import pandas as pd
import requests
from bs4 import BeautifulSoup
import yfinance as yf

# Load S&P 500 table

def load_sp500_companies(max_companies=500):
    """Load the S&P 500 constituent table from Wikipedia.

    Parameters:
    ----------
    max_companies : int
        Maximum number of companies to keep.

    Returns
    -------
    DataFrame
        Subset of S&P 500 companies.
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "constituents"})
    df = pd.read_html(str(table))[0]

    return df.head(max_companies)

# Safe getter for statements

def safe_get_item(df, row_label, date):
    """Safely get a single numeric value from a financial statement.

    Parameters
    ----------
    df : DataFrame
        Financial statement.
    row_label : str
        Line item name ('Total Revenue', 'Net Income', etc).
    date : str or Timestamp
        Column label for the year.
    """
    try:
        value = df.loc[row_label, date]
        if pd.isna(value):
            return None
        return float(value)
    except Exception:
        return None

# Extract financials for a given ticker

def get_company_metadata(ticker_obj):
    """ Function to retrieve basic company metadata from a Yahoo Finance ticker object.

     This function safely queries Yahoo Finance for information about a given company.
    If the data request fails (e.g due to missing fields, connection issues, or API
    inconsistencies), the function returns an empty dictionary instead of raising an error,
    ensuring that failures for individual companies do not interrupt larger batch processes.
    """
    try:
        info = ticker_obj.get_info()
    except Exception:
        return {}

    return {
        "company_name": info.get("longName") or info.get("shortName") or ticker_obj.ticker,
        "country": info.get("country"),
        "industry": info.get("industry"),
        "sector": info.get("sector"),
        "currency": info.get("financialCurrency") or info.get("currency"),
        "employees": info.get("fullTimeEmployees"),
        "market_cap": info.get("marketCap"),
    }

def extract_company_financials(ticker, max_years=3):
    """
    Extract key financial metrics from the income statement and balance sheet
    for a given ticker.

    Parameters
    ----------
    ticker : str
        Stock ticker symbol.
    max_years : int, optional
        Number of most recent years to extract (default is 3).

    Returns
    -------
    list of dict
        Each dictionary contains:
        'ticker', 'company_name', 'country', 'industry', 'year',
        'revenue', 'revenue_currency', 'net_income', 'gross_profit',
        'total_assets', and 'employees'.
    """
    stock = yf.Ticker(ticker)
    meta = get_company_metadata(stock)

    income = stock.income_stmt
    balance = stock.balance_sheet

    years = list(income.columns)[:max_years]

    data_rows = []
    for year in years:

        row = {
            "ticker": ticker,
            "company_name": meta.get("company_name"),
            "country": meta.get("country"),
            "industry": meta.get("industry"),
            "year": year.strftime("%Y"),

            # Revenue and its currency
            "revenue": safe_get_item(income, "Total Revenue", year),
            "revenue_currency": meta.get("currency"),

            # Additional KPIs
            "net_income": safe_get_item(income, "Net Income", year),
            "gross_profit": safe_get_item(income, "Gross Profit", year),
            "total_assets": safe_get_item(balance, "Total Assets", year),

            # Snapshot KPI
            "employees": meta.get("employees"),
        }

        data_rows.append(row)

    return data_rows
