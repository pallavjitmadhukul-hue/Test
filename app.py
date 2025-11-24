import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import df, date, datetime

st.set_page_config(
    page_title="Enterprise Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)
logo = st.sidebar.image ("data:image/png;base64,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")

st.sidebar.title("⚙️ Controls & Filters")

selected_year = st.sidebar.selectbox("Select Year", [2023, 2024, 2025])

start_date, end_date = st.sidebar.date_input(
        "Select Date Range",
        value=(date(2025, 1, 1), date(2025, 11, 1))
)
#
#TEST
#
# ----- SIDEBAR -----
frequency = st.sidebar.radio(
    "Select Frequency",
    ["Daily", "Weekly", "Monthly"],
    index=2
)

# ----- GROUP DATA -----
df["DATE"] = pd.to_datetime(df["DATE"])

if frequency == "Daily":
    df_grouped = df.groupby("DATE")[["ACTUAL_REV", "ACTUAL_COST"]].sum()

elif frequency == "Weekly":
    df_grouped = df.groupby(pd.Grouper(key="DATE", freq="W"))[["ACTUAL_REV", "ACTUAL_COST"]].sum()

elif frequency == "Monthly":
    df_grouped = df.groupby(pd.Grouper(key="DATE", freq="M"))[["ACTUAL_REV", "ACTUAL_COST"]].sum()

# ----- VISUALIZE -----
st.subheader(f"{frequency} Revenue vs Cost")

fig = px.line(
    df_grouped.reset_index(),
    x="DATE",
    y=["ACTUAL_REV", "ACTUAL_COST"],
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

######################
selected_region = st.sidebar.multiselect(
    "Select Regions", ["North America", "Europe", "Asia", "LATAM"] #, default=["North America", "Europe"]
)

metric_option = st.sidebar.selectbox(
    "Metric to Analyze",
    ["Revenue", "Cost", "Profit", "Discount"],
    index=0
)

