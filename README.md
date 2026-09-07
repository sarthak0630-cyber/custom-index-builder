# Custom Index Builder

## Project Overview

Custom Index Builder is a web-based application that allows users to create and analyse a custom Price Return Equity Index using a predefined universe of 30 dummy stocks.

Users can select one or more stocks, choose a weighting methodology, select a date range, and generate a custom index starting with a base value of 100.

---

## Features

- Universe of 30 dummy stocks
- Stock selection functionality
- Equal Weight methodology
- Market Capitalisation Weight methodology
- Date range selection
- Price Return Index calculation
- Index performance chart
- Index constituent weights table
- Summary performance metrics
- Input validation
- Missing data handling
- CSV download of index results

---

## Technology Stack

- Python
- Streamlit
- Pandas
- Plotly

---

## Project Architecture

### User Interface

Streamlit is used to build the interactive web application. Users can select stocks, choose a weighting method, select a date range and generate the custom index.

### Backend

Python performs the index calculations. Pandas is used for data manipulation, price calculations and return calculations.

### Data Layer

The project uses CSV files containing:

- A dummy stock universe
- Historical daily closing prices

---

## Stock Universe

The application uses a predefined universe of 30 dummy stocks.

The stock data includes:

- Ticker
- Company information
- Sector information
- Market capitalisation

Users can select one or more stocks from the available universe.

---

# Index Methodology

## 1. Stock Daily Return

The daily return for each stock is calculated using:

r(t) = Price(t) / Price(t-1) - 1

The application uses Pandas `pct_change()` to calculate daily percentage returns.

---

## 2. Weighting Methodology

### Equal Weight

Under the Equal Weight methodology, every selected stock receives the same weight.

Weight = 1 / Number of Selected Stocks

For example, if 10 stocks are selected, each stock receives a weight of 10%.

### Market Capitalisation Weight

Under the Market Cap Weight methodology, each stock receives a weight based on its market capitalisation.

Weight of Stock = Stock Market Cap / Total Market Cap of Selected Stocks

Stocks with larger market capitalisations receive higher weights.

---

## 3. Index Daily Return

The daily index return is calculated by multiplying each stock return by its respective weight and summing the results:

Index Return = Σ(Weight × Stock Return)

---

## 4. Index Level Calculation

The index begins with a base value of 100.

The index level is calculated using:

Level(t) = Level(t-1) × (1 + Index Return)

The application calculates the cumulative index performance over the selected date range.

---

## Missing Data Handling

The application checks the price matrix for missing values.

If missing values are detected:

1. A warning is displayed to the user.
2. The forward-fill method is applied using `ffill()`.
3. Any remaining missing observations are removed using `dropna()`.

The application also validates that at least two price observations are available before calculating returns.

---

## Input Validation

The application validates:

- At least one stock must be selected.
- Both a start date and end date must be selected.
- The start date must be before the end date.
- There must be sufficient price observations.
- Missing data is identified and handled before return calculations.

---

## Results

After generating the index, the application displays:

- Base Value
- Ending Value
- Cumulative Return
- Number of Selected Stocks
- Price Return Index Performance Chart
- Index Constituent Weights
- Recent Index Levels
- Daily Index Returns

Users can also download the index results as a CSV file.

---

## How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/sarthak0630-cyber/custom-index-builder.git
cd custom-index-builder
```

### 2. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Generate Dummy Data (Optional)

The repository already includes generated CSV files. To regenerate them:

```bash
python data_generator.py
```

This creates or replaces `data/stock_universe.csv` and `data/stock_prices.csv`.

### 4. Start the Application

```bash
streamlit run app.py
```

Streamlit will provide a local URL that can be opened in a web browser.

## Data Format

### `data/stock_universe.csv`

Contains 30 rows, one for each dummy stock:

| Column | Description |
| --- | --- |
| `ticker` | Unique stock identifier |
| `company_name` | Dummy company name |
| `sector` | Sector or industry label |
| `market_cap` | Numeric value used for market-cap weighting |

### `data/stock_prices.csv`

Contains one row per stock per business date:

| Column | Description |
| --- | --- |
| `date` | Trading date |
| `ticker` | Stock identifier matching the universe file |
| `close_price` | Dummy daily closing price |

The included data covers business days from January 1, 2024 through December 31, 2025. Prices are simulated and are reproducible because the generator uses a fixed random seed.

## Assumptions

- Only available business dates are used; weekends and public holidays are not modelled separately.
- The selected stocks are held with static weights for the full calculation period.
- The index is a price return index, so dividends and other distributions are excluded.
- If a price is missing, the app forward-fills from the most recent available observation and removes any rows that still contain missing values.
- The first return observation is excluded because it has no prior closing price.

## Limitations and Future Improvements

- The stock universe and prices are dummy data and are not suitable for investment decisions.
- The app currently supports equal weighting and market-cap weighting only.
- Market-cap weights do not rebalance during the selected date range.
- The calculation does not include dividends, transaction costs, taxes, corporate actions, or index rebalancing rules.
- Future improvements could include custom user-defined weights, configurable rebalancing dates, dividend-adjusted total returns, stronger data-quality checks, and automated tests for the calculation logic.

## Git Workflow

The project was developed through multiple commits, including an initial implementation, documentation updates, and an index enhancement branch. The repository is available on GitHub at:

https://github.com/sarthak0630-cyber/custom-index-builder