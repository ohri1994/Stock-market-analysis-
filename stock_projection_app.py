import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Stock Projection Tool", layout="centered")

st.title("📈 Simple Stock Projection Tool")

# Inputs
st.header("Input Assumptions")
current_price = st.number_input("Current Price", min_value=0.0, value=100.0, step=0.1)
starting_eps = st.number_input("Starting EPS (TTM)", min_value=0.0, value=5.0, step=0.01)
years = st.number_input("Years to Project", min_value=1, value=5, step=1)

st.subheader("Bear Case")
bear_growth = st.number_input("Bear EPS Growth (%)", value=3.0, step=0.1)
bear_exit_pe = st.number_input("Bear Exit P/E", value=15.0, step=0.1)

st.subheader("Base Case")
base_growth = st.number_input("Base EPS Growth (%)", value=8.0, step=0.1)
base_exit_pe = st.number_input("Base Exit P/E", value=20.0, step=0.1)

st.subheader("Bull Case")
bull_growth = st.number_input("Bull EPS Growth (%)", value=12.0, step=0.1)
bull_exit_pe = st.number_input("Bull Exit P/E", value=25.0, step=0.1)

# Computation
def project_eps(eps0, growth_rate, years):
    g = growth_rate / 100.0
    return [eps0 * ((1 + g) ** t) for t in range(1, years + 1)]

bear_eps = project_eps(starting_eps, bear_growth, years)
base_eps = project_eps(starting_eps, base_growth, years)
bull_eps = project_eps(starting_eps, bull_growth, years)

bear_price_final = bear_eps[-1] * bear_exit_pe
base_price_final = base_eps[-1] * base_exit_pe
bull_price_final = bull_eps[-1] * bull_exit_pe

bear_return_pct = ((bear_price_final / current_price) - 1) * 100
base_return_pct = ((base_price_final / current_price) - 1) * 100
bull_return_pct = ((bull_price_final / current_price) - 1) * 100

# Table
df = pd.DataFrame({
    "Year": list(range(1, years + 1)),
    "Bear EPS": bear_eps,
    "Base EPS": base_eps,
    "Bull EPS": bull_eps
})

# Append final prices and returns to display
summary_df = pd.DataFrame({
    "Scenario": ["Bear", "Base", "Bull"],
    "Final EPS": [bear_eps[-1], base_eps[-1], bull_eps[-1]],
    "Exit P/E": [bear_exit_pe, base_exit_pe, bull_exit_pe],
    "Final Price": [bear_price_final, base_price_final, bull_price_final],
    "Total Return %": [bear_return_pct, base_return_pct, bull_return_pct]
})

st.header("Projected EPS (per year)")
st.dataframe(df.style.format("{:.2f}"), use_container_width=True)

st.header("Final Year Summary")
st.dataframe(summary_df.style.format({"Final EPS": "{:.2f}", "Exit P/E": "{:.1f}", "Final Price": "{:.2f}", "Total Return %": "{:.1f}%"}), use_container_width=True)

# Chart
st.header("EPS Projection Chart")
chart_df = df.set_index("Year")
st.line_chart(chart_df)

# Download CSV
output = io.StringIO()
df.to_csv(output, index=False)
csv_data = output.getvalue()

st.download_button(
    label="📥 Download EPS Table as CSV",
    data=csv_data,
    file_name="stock_projection.csv",
    mime="text/csv"
)
