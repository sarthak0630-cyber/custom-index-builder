import pandas as pd
import numpy as np
import os

# --------------------------------------------------
# PROJECT SETTINGS
# --------------------------------------------------

np.random.seed(42)

# Create data folder if it does not exist
os.makedirs("data", exist_ok=True)


# --------------------------------------------------
# CREATE 30-STOCK UNIVERSE
# --------------------------------------------------

stocks = [
    ["ALPH", "Alpha Technologies", "Technology", 85000],
    ["NOVA", "Nova Systems", "Technology", 72000],
    ["CYBR", "CyberNet Solutions", "Technology", 68000],
    ["CLOUD", "CloudCore Technologies", "Technology", 61000],
    ["INFX", "Infinix Software", "Technology", 54000],

    ["FINX", "FinX Financial Services", "Financials", 90000],
    ["PRIM", "Prime Capital", "Financials", 78000],
    ["INVB", "InvestBank Holdings", "Financials", 65000],
    ["PAYM", "PayMax Services", "Financials", 48000],
    ["SAFE", "SafeGuard Insurance", "Financials", 42000],

    ["HLTH", "HealthFirst Pharma", "Healthcare", 75000],
    ["MEDI", "Medicare Solutions", "Healthcare", 58000],
    ["BIOT", "BioTech Innovations", "Healthcare", 46000],
    ["LIFE", "LifeCare Hospitals", "Healthcare", 39000],
    ["CURE", "CureWell Laboratories", "Healthcare", 35000],

    ["ENRG", "EnergyCore Limited", "Energy", 82000],
    ["SOLR", "SolarEdge Energy", "Energy", 53000],
    ["WIND", "WindPower Corporation", "Energy", 44000],
    ["OILX", "OilMax Industries", "Energy", 70000],
    ["POWR", "PowerGrid Solutions", "Energy", 60000],

    ["RETL", "RetailMart Limited", "Consumer", 55000],
    ["FOOD", "FoodWorld Brands", "Consumer", 47000],
    ["LUXE", "Luxe Lifestyle", "Consumer", 38000],
    ["AUTO", "AutoDrive Motors", "Consumer", 63000],
    ["HOME", "HomeComfort Products", "Consumer", 41000],

    ["INDU", "IndustrialWorks", "Industrials", 67000],
    ["MACH", "MachTech Manufacturing", "Industrials", 52000],
    ["LOGI", "LogisticsPro", "Industrials", 45000],
    ["CHEM", "ChemCore Industries", "Materials", 59000],
    ["MINE", "MineWorks Resources", "Materials", 43000]
]


# Create DataFrame
universe = pd.DataFrame(
    stocks,
    columns=[
        "ticker",
        "company_name",
        "sector",
        "market_cap"
    ]
)


# Save stock universe
universe.to_csv(
    "data/stock_universe.csv",
    index=False
)


# --------------------------------------------------
# GENERATE DAILY PRICES
# --------------------------------------------------

# Business days only
dates = pd.date_range(
    start="2024-01-01",
    end="2025-12-31",
    freq="B"
)

all_prices = []


for _, stock in universe.iterrows():

    ticker = stock["ticker"]

    # Random starting price
    starting_price = np.random.uniform(
        50,
        500
    )

    # Sector-specific characteristics
    daily_drift = np.random.uniform(
        0.0001,
        0.0008
    )

    daily_volatility = np.random.uniform(
        0.01,
        0.025
    )

    # Generate daily returns
    daily_returns = np.random.normal(
        loc=daily_drift,
        scale=daily_volatility,
        size=len(dates)
    )

    # Generate price series
    prices = starting_price * np.cumprod(
        1 + daily_returns
    )

    # Add each daily price
    for date, price in zip(dates, prices):

        all_prices.append({
            "date": date,
            "ticker": ticker,
            "close_price": round(
                max(price, 1),
                2
            )
        })


# Create price DataFrame
price_data = pd.DataFrame(all_prices)


# Save price data
price_data.to_csv(
    "data/stock_prices.csv",
    index=False
)


# --------------------------------------------------
# SUCCESS MESSAGE
# --------------------------------------------------

print("\nSUCCESS!")
print("30-stock universe created.")
print(f"Number of stocks: {len(universe)}")
print(f"Number of price records: {len(price_data)}")

print("\nFiles created:")
print("data/stock_universe.csv")
print("data/stock_prices.csv")