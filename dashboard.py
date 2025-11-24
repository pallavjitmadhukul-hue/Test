import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Enterprise Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.title("⚙️ Controls & Filters")

selected_year = st.sidebar.selectbox("Select Year", [2023, 2024, 2025])
selected_region = st.sidebar.multiselect(
    "Select Regions", ["North America", "Europe", "Asia", "LATAM"], default=["North America", "Europe"]
)

metric_option = st.sidebar.radio(
    "Metric to Analyze",
    ["Revenue", "Cost", "Profit"],
    index=0
)

show_advanced = st.sidebar.checkbox("Show Advanced Analytics", value=True)

# ---------------------------
# DATA GENERATION
# ---------------------------
np.random.seed(42)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Sample data
regions = ["North America", "Europe", "Asia", "LATAM"]
df = pd.DataFrame({
    "Month": np.tile(months, 4),
    "Region": np.repeat(regions, 12),
    "Revenue": np.random.randint(20000, 150000, 48),
    "Cost": np.random.randint(10000, 90000, 48)
})
df["Profit"] = df["Revenue"] - df["Cost"]

# Filter based on sidebar
filtered_df = df[df["Region"].isin(selected_region)]

# ---------------------------
# HEADER KPIs
# ---------------------------
st.title("📊 Enterprise Analytics Dashboard")
st.caption(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${filtered_df['Revenue'].sum():,}")
col2.metric("Total Cost", f"${filtered_df['Cost'].sum():,}")
col3.metric("Profit", f"${filtered_df['Profit'].sum():,}")
col4.metric("Avg Monthly Profit", f"${filtered_df['Profit'].mean():,.0f}")

# ---------------------------
# CHART: MONTHLY METRIC TREND
# ---------------------------
st.subheader(f"📈 Monthly {metric_option} Trend")

trend_df = (
    filtered_df.groupby("Month")[[metric_option]].sum().reindex(months)
)

fig_trend = px.line(
    trend_df,
    x=trend_df.index,
    y=metric_option,
    markers=True,
    title=f"{metric_option} Over Time"
)
st.plotly_chart(fig_trend, use_container_width=True)

# ---------------------------
# BAR CHART: REGION COMPARISON
# ---------------------------
st.subheader(f"📊 {metric_option} by Region")
fig_bar = px.bar(
    filtered_df.groupby("Region")[[metric_option]].sum().reset_index(),
    x="Region",
    y=metric_option,
    color="Region",
    title=f"Regional Comparison of {metric_option}"
)
st.plotly_chart(fig_bar, use_container_width=True)

# ---------------------------
# ADVANCED ANALYTICS
# ---------------------------
if show_advanced:
    st.subheader("🧠 Advanced Analytics")

    # Correlation heatmap
    st.markdown("### 🔍 Correlation Matrix")
    corr_df = filtered_df[["Revenue", "Cost", "Profit"]].corr()
    st.dataframe(corr_df.style.background_gradient(cmap="coolwarm"))

    # Region vs Month pivot table
    st.markdown("### 📌 Region-Month Pivot Table")
    pivot = filtered_df.pivot_table(index="Region", columns="Month", values=metric_option, aggfunc="sum")
    st.dataframe(pivot)

# ---------------------------
# RAW DATA TABLE
# ---------------------------
st.subheader("📋 Raw Data")
st.dataframe(filtered_df, use_container_width=True)