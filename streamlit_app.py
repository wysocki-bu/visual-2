import numpy as np
import pandas as pd
import streamlit as st
 
 
@st.cache_data
def load_orders():
    rng = np.random.default_rng(1)
    n = 2_000
    return pd.DataFrame({
        "date": pd.Timestamp("2026-01-01") + pd.to_timedelta(rng.integers(0, 280, n), unit="D"),
        "sector": rng.choice(["Retail", "Energy", "Autos", "Food"], n),
        "product": rng.choice(["Americas", "Europe", "Asia"], n, p=[0.5, 0.35, 0.15]),
        "amount": rng.gamma(2.0, 60.0, n).round(2),
    })
 
 
orders = load_orders()
all_sectors = sorted(orders.sector.unique())
 
with st.sidebar:
    st.header("Filters")
    sectors = st.multiselect("Sector", all_sectors, default=all_sectors)
    dates = st.date_input("Dates", (orders.date.min().date(), orders.date.max().date()))
 
if len(dates) != 2:
    st.stop()  # the user has picked a start date but not yet an end date
 
start, end = dates
picked = orders[orders.sector.isin(sectors) & orders.date.dt.date.between(start, end)]
 
st.title("Corporate Earnings by Industry & Region ($millions)")
st.metric("Earnings in range", f"${picked.amount.sum():,.0f}", f"{len(picked):,} orders", delta_color="off")
weekly = picked.groupby([pd.Grouper(key="date", freq="W"), "sector"]).amount.sum().unstack()
st.bar_chart(weekly)
st.dataframe(picked.sort_values("date", ascending=False), hide_index=True)
