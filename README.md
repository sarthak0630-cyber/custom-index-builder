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