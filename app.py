import streamlit as st
import pandas as pd
import plotly.express as px


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Custom Index Builder",
    page_icon="📊",
    layout="wide"
)


# ==================================================
# APPLICATION TITLE
# ==================================================

st.title("📊 Custom Index Builder")

st.write(
    "Build and analyse a custom 30-stock Price Return Index."
)


# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data():

    universe = pd.read_csv(
        "data/stock_universe.csv"
    )

    prices = pd.read_csv(
        "data/stock_prices.csv"
    )

    prices["date"] = pd.to_datetime(
        prices["date"]
    )

    return universe, prices


try:

    universe, prices = load_data()

except FileNotFoundError:

    st.error(
        "Data files not found. Please run "
        "data_generator.py first."
    )

    st.stop()


# ==================================================
# SIDEBAR - INDEX SETTINGS
# ==================================================

st.sidebar.header("⚙️ Index Configuration")


# --------------------------------------------------
# STOCK SELECTION
# --------------------------------------------------

selected_stocks = st.sidebar.multiselect(
    "Select Stocks",
    options=universe["ticker"].tolist(),
    default=universe["ticker"].tolist()[:10]
)


# --------------------------------------------------
# WEIGHTING METHOD
# --------------------------------------------------

weight_method = st.sidebar.selectbox(
    "Weighting Method",
    options=[
        "Equal Weight",
        "Market Cap Weight"
    ]
)


# --------------------------------------------------
# DATE RANGE
# --------------------------------------------------

minimum_date = prices["date"].min().date()
maximum_date = prices["date"].max().date()


date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(
        minimum_date,
        maximum_date
    ),
    min_value=minimum_date,
    max_value=maximum_date
)


# --------------------------------------------------
# GENERATE BUTTON
# --------------------------------------------------

generate_index = st.sidebar.button(
    "🚀 Generate Index",
    type="primary"
)


# ==================================================
# DISPLAY STOCK UNIVERSE
# ==================================================

with st.expander("View Complete 30-Stock Universe"):

    st.dataframe(
        universe,
        use_container_width=True
    )


# ==================================================
# MAIN APPLICATION
# ==================================================

if generate_index:


    # ----------------------------------------------
    # VALIDATION 1
    # ----------------------------------------------

    if len(selected_stocks) == 0:

        st.error(
            "Please select at least one stock."
        )

        st.stop()


    # ----------------------------------------------
    # VALIDATION 2
    # ----------------------------------------------

    if len(date_range) != 2:

        st.error(
            "Please select both a start date and an end date."
        )

        st.stop()


    # ----------------------------------------------
    # CONVERT DATES
    # ----------------------------------------------

    start_date = pd.to_datetime(
        date_range[0]
    )

    end_date = pd.to_datetime(
        date_range[1]
    )


    # ----------------------------------------------
    # VALIDATION 3
    # ----------------------------------------------

    if start_date >= end_date:

        st.error(
            "Start date must be before end date."
        )

        st.stop()


    # ----------------------------------------------
    # FILTER DATA
    # ----------------------------------------------

    filtered_prices = prices[
        (
            prices["ticker"].isin(
                selected_stocks
            )
        )
        &
        (
            prices["date"] >= start_date
        )
        &
        (
            prices["date"] <= end_date
        )
    ].copy()


    # ----------------------------------------------
    # CREATE PRICE MATRIX
    # ----------------------------------------------

    price_matrix = filtered_prices.pivot(
        index="date",
        columns="ticker",
        values="close_price"
    )


    # Sort dates
    price_matrix = price_matrix.sort_index()


    # ----------------------------------------------
    # VALIDATION 4 - MISSING DATA
    # ----------------------------------------------

    missing_values = price_matrix.isna().sum().sum()


    if missing_values > 0:

        st.warning(
            f"Missing data detected: {missing_values} values. "
            "Forward-fill method will be applied."
        )

        price_matrix = price_matrix.ffill()


    # Remove any remaining missing values
    price_matrix = price_matrix.dropna()


    # ----------------------------------------------
    # VALIDATION 5
    # ----------------------------------------------

    if len(price_matrix) < 2:

        st.error(
            "Not enough price observations to calculate returns."
        )

        st.stop()


    # ==================================================
    # STEP 1: CALCULATE STOCK DAILY RETURNS
    # ==================================================

    stock_returns = price_matrix.pct_change()

    # Remove first row because there is no previous price
    stock_returns = stock_returns.dropna()


    # ==================================================
    # STEP 2: CALCULATE INDEX WEIGHTS
    # ==================================================

    if weight_method == "Equal Weight":

        weights = pd.Series(
            1 / len(selected_stocks),
            index=selected_stocks
        )


    elif weight_method == "Market Cap Weight":

        selected_universe = universe[
            universe["ticker"].isin(
                selected_stocks
            )
        ].copy()


        market_caps = selected_universe.set_index(
            "ticker"
        )["market_cap"]


        weights = market_caps / market_caps.sum()


    # Make sure weight order matches return columns
    weights = weights.reindex(
        stock_returns.columns
    )


    # ==================================================
    # STEP 3: CALCULATE DAILY INDEX RETURN
    # ==================================================

    index_returns = (
        stock_returns * weights
    ).sum(
        axis=1
    )


    # ==================================================
    # STEP 4: CALCULATE INDEX LEVEL
    # ==================================================

    BASE_VALUE = 100


    index_levels = (
        BASE_VALUE
        *
        (1 + index_returns).cumprod()
    )


    # ==================================================
    # SUMMARY METRICS
    # ==================================================

    ending_value = index_levels.iloc[-1]


    cumulative_return = (
        (
            ending_value
            /
            BASE_VALUE
        )
        - 1
    ) * 100


    total_stocks = len(selected_stocks)


    # ==================================================
    # DISPLAY RESULTS
    # ==================================================

    st.success(
        "Index generated successfully!"
    )


    # --------------------------------------------------
    # METRICS
    # --------------------------------------------------

    metric1, metric2, metric3, metric4 = st.columns(4)


    metric1.metric(
        "Base Value",
        f"{BASE_VALUE:.2f}"
    )


    metric2.metric(
        "Ending Value",
        f"{ending_value:.2f}"
    )


    metric3.metric(
        "Cumulative Return",
        f"{cumulative_return:.2f}%"
    )


    metric4.metric(
        "Number of Stocks",
        total_stocks
    )


    # --------------------------------------------------
    # INDEX CHART
    # --------------------------------------------------

    st.subheader(
        "📈 Price Return Index Performance"
    )


    chart_data = pd.DataFrame({
        "Date": index_levels.index,
        "Index Level": index_levels.values
    })


    figure = px.line(
        chart_data,
        x="Date",
        y="Index Level",
        title="Custom Price Return Index"
    )


    st.plotly_chart(
        figure,
        use_container_width=True
    )


    # --------------------------------------------------
    # WEIGHTS TABLE
    # --------------------------------------------------

    st.subheader(
        "⚖️ Index Constituent Weights"
    )


    weights_table = weights.reset_index()


    weights_table.columns = [
        "Ticker",
        "Weight"
    ]


    weights_table["Weight (%)"] = (
        weights_table["Weight"] * 100
    )


    weights_table = weights_table.drop(
        columns="Weight"
    )


    weights_table = weights_table.sort_values(
        "Weight (%)",
        ascending=False
    )


    st.dataframe(
        weights_table,
        use_container_width=True
    )


    # --------------------------------------------------
    # INDEX RETURN DATA
    # --------------------------------------------------

    st.subheader(
        "📊 Recent Index Levels"
    )


    display_levels = pd.DataFrame({
        "Date": index_levels.index,
        "Index Level": index_levels.values,
        "Daily Return (%)": index_returns.values * 100
    })


    st.dataframe(
        display_levels.tail(10),
        use_container_width=True
    )
    csv = display_levels.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Index Results as CSV",
        data=csv,
        file_name="custom_index_results.csv",
        mime="text/csv"
    )


    # --------------------------------------------------
    # CALCULATION EXPLANATION
    # --------------------------------------------------

    with st.expander(
        "How is the index calculated?"
    ):

        st.write(
            "1. Calculate daily stock returns."
        )

        st.latex(
            r"r_i(t) = \frac{P_i(t)}{P_i(t-1)} - 1"
        )


        st.write(
            "2. Calculate the weighted index return."
        )

        st.latex(
            r"r_{index}(t) = \sum w_i r_i(t)"
        )


        st.write(
            "3. Build the index from a base value of 100."
        )

        st.latex(
            r"Level(t) = Level(t-1) \times (1 + r_{index}(t))"
        )


# ==================================================
# DEFAULT SCREEN
# ==================================================

else:

    st.info(
        "👈 Select stocks, weighting method and date range "
        "from the sidebar, then click Generate Index."
    )