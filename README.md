# Custom Index Builder

## Project Overview
A web-based application that allows users to create a custom equity index
using a predefined universe of 30 dummy stocks.

## Features
- View 30 dummy stocks
- Select stocks for the index
- Select a weighting methodology
- Select a date range
- Generate a Price Return Index
- View index levels and cumulative returns
- Download index results as CSV

## Technology Stack
- Python
- Streamlit
- Pandas
- NumPy
- Plotly

## Architecture
### User Interface
Streamlit is used to provide the web-based user interface.

### Backend
Python and Pandas perform data processing and index calculations.

### Data
Dummy stock universe and daily price data are stored in CSV format.

## Weighting Method
Explain the weighting methodology used in your application.

## Index Calculation Methodology

### Stock Return
r(t) = Price(t) / Price(t-1) - 1

### Index Return
r_index(t) = Σ(w_i × r_i(t))

### Index Level
level(t) = level(t-1) × (1 + r_index(t))

The base index level is 100.

## Missing Data Handling
Explain exactly what your code does when price data is missing.

## How to Run

1. Clone the repository
2. Create a virtual environment
3. Install dependencies

pip install -r requirements.txt

4. Run:

python -m streamlit run app.py

## Limitations
- Dummy data instead of live market data
- Simplified corporate actions treatment
- Limited weighting methodologies

## Future Improvements
- Live market data
- Additional weighting methodologies
- Rebalancing functionality
- Corporate actions handling
- Database integration