# S&P 500 Financial Dataset

This python file builds a structured financial dataset for S&P 500 companies using Python. It automatically fetches the current S&P 500 constituents and combines them with three years of company financials into a single, tidy table.

## Project Overview

**Data Sources Scraped:**

- **Wikipedia**: S&P 500 constituents table (`https://en.wikipedia.org/wiki/List_of_S%26P_500_companies`)
- **Yahoo Finance**: Company profiles and annual financial statements via `yfinance`

**Key Steps:**

1. Scrapes S&P 500 list using `requests` + `BeautifulSoup` (avoids 403 errors)
2. Fetches company info and 3 years of financials via `yfinance`
3. Merges into clean DataFrame and exports to CSV

## Final Dataset Columns (14 columns)

| Column             | Source               | Description              | Data Type   |
| ------------------ | -------------------- | ------------------------ | ----------- |
| `ticker`           | Wikipedia + yfinance | Stock ticker             | str         |
| `company_name`     | Wikipedia + yfinance | Full company name        | str         |
| `country`          | yfinance             | Country of incorporation | str         |
| `industry`         | yfinance             | Industry classification  | str         |
| `year`             | yfinance financials  | Fiscal year              | int         |
| `revenue_in$B`     | yfinance financials  | Total revenue            | float (USD) |
| `revenue_currency` | yfinance             | Currency code            | str         |
| `net_income_in_$B` | yfinance financials  | Net income               | float (USD) |
| `gross_profit`     | yfinance financials  | Gross profit             | float (USD) |
| `total_assets`     | yfinance financials  | Total assets             | float (USD) |
| `employees`        | yfinance             | Number of employees      | int         |

**Dataset Size**: ~442 rows × 11 columns (3 years per company)
