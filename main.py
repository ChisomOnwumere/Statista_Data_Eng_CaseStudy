#import libraries
import time
import pandas as pd
from src.ops import load_sp500_companies, extract_company_financials 

#

def build_financial_dataset_from_sp500(
    max_companies:int=150,
    max_years_per_company:int=3,
    sleep_seconds:float=2.0
):
    """Create the full multi-year dataset for a subset of S&P 500.
    Args:
        max_companies: number of companies fetched. 
        max_years_per_company: number of years we are looking at.
        sleep_seconds: how many seconds the crawler will sleep
    Ouput:
        Returns a pandas DataFrame with one row per company–year and the following columns 
        ['ticker', 'company_name', 'year',
         'total_revenue', 'cost_of_revenue', 'gross_profit',
         'operating_income', 'net_income',
         'total_assets', 'total_liabilities', 'total_equity',
         'operating_cashflow', 'capital_expenditure', 'free_cashflow'].
    """
    faulty_companies = []
    #load s&p companies
    sp500 = load_sp500_companies(max_companies=max_companies)

    all_rows = []

    #get the revenue and other financial data for each company
    for i, row in sp500.iterrows():
        ticker_symbol = row["Symbol"]  # uses the renamed column
        print(f"[{i+1}/{len(sp500)}] Processing {ticker_symbol}...")

        try:
            company_rows = extract_company_financials (
                ticker=ticker_symbol,
                max_years=max_years_per_company,
            )
            all_rows.extend(company_rows)
        #if there is an exception, skip and collect details in faulty companies list
        except Exception as e:
            print(f"  -> Skipping {ticker_symbol} due to error: {e}")
            faulty_companies.append(ticker_symbol)
        time.sleep(sleep_seconds)

    dataset = pd.DataFrame(all_rows)

    # Optional cleaning step: keep only rows where revenue is present
    if "revenue" in dataset.columns:
        dataset = dataset[dataset["revenue"].notna()]
        
    money_cols = ["revenue", "net_income", "gross_profit", "total_assets"]
    # 2) Convert from units (usually dollars) to billions
    #    e.g. 10000000000 → 10.0
    dataset[money_cols] = dataset[money_cols] / 1e9

    # 3) Rename the columns to make it clear they are in billions of dollars
    dataset = dataset.rename(columns={
        "revenue": "revenue_in_$B",
        "net_income": "net_income_in_$B",
        "gross_profit": "gross_profit_in_$B",
        "total_assets": "total_assets_in_$B",
        }
    )

    dataset["employees"] = (
        pd.to_numeric(dataset["employees"], errors="coerce")
        .round(0)
        .astype("Int64")
    )
    return dataset, faulty_companies

