import main 
df, faulty_companies = main.build_financial_dataset_from_sp500(max_companies=150, max_years_per_company=3, sleep_seconds=0.5)

df.to_csv("Companies.csv", index=False)

