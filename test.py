import streamlit as st
import pandas as pd
import plotly as pt
import plotly.express as px
from datetime import date

st.set_page_config(
    page_title="Test Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data(path):
    df = pd.read_csv(path, parse_dates=["Order Date", "Ship Date"])
    return df

df = load_data("Superstore.csv")
#st.success("CSV Loaded Successfully")

col1, col2 = st.columns([6, 1])

with col2:
    st.image("logo.png", width=60)
col1, col2 = st.columns([6, 1])

with col1:
    st.title("📊 Test Dashboard")
    st.markdown("This dashboard is built using Python + Streamlit")
col1, col2 = st.columns([6, 1])

st.sidebar.header("Filters")

min_date = df["Order Date"].min()
max_date = df["Order Date"].max()

date_range = st.sidebar.date_input(
    "Select Order Date Range",
    [min_date.date(), max_date.date()]
)
start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

st.sidebar.markdown("Select Region, Category, Sub-Category")
regions = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

categories = st.sidebar.multiselect(
    "Category",
    sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

subcategories = st.sidebar.multiselect(
    "Sub-Category",
    sorted(df["Sub-Category"].unique()),
    default=sorted(df["Sub-Category"].unique())
)

filtered = df[
    (df["Order Date"] >= start_date) &
    (df["Order Date"] <= end_date) &
    (df["Category"].isin(categories)) &
    (df["Sub-Category"].isin(subcategories))
]

st.markdown("KPIS")

col1,col2,col3,col4 = st.columns(4)

col1.metric("Total Sales", f"${filtered['Sales'].sum():,.2f}")
col2.metric("Total Profit", f"${filtered['Profit'].sum():,.2f}")
col3.metric("Total Quantity",f"${int(filtered['Quantity'].sum()):,.2f}")
col4.metric("Avg Discount", f"{filtered['Discount'].mean():.2%}")

st.markdown("Sales and Profit Trends")

left, right = st.columns([2,1])

# with left:
#     monthly = filtered.resample("M", on="Order Date").sum().reset_index()
#     if not monthly.empty:
#         fig = px.line(
#             monthly,
#             x="Order Date",
#             Y=["Sales","Profit"],
#             title="Monthly Sales and Profit"
#         )
#         st.plotly_chart(fig, use_container_width=True)
#     else:
#         st.info("No Data Available")

with left:
    monthly = (
        filtered
        .resample("M", on="Order Date")[["Sales", "Profit"]]
        .sum()
        .reset_index()
    )

    if not monthly.empty:
        fig = px.line(
            monthly,
            x="Order Date",
            y=["Sales", "Profit"],
            title="Monthly Sales and Profit"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No Data Available")

with right:
    if not filtered.empty:
        cat_sales = filtered.groupby("Category", as_index=False)["Sales"].sum()
        fig2 = px.bar(cat_sales, x="Category", y="Sales", title="Sales by Category")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Data Not Available")

st.markdown("Top Selling Products")

top_n = st.slider("Select number of products", 5, 25, 10)

top_products = (
    filtered.groupby("Product Name", as_index=False)
    .agg({"Sales": "sum", "Profit": "sum", "Quantity": "sum"})
    .sort_values("Sales",ascending=False)
    .head(top_n)
)

st.dataframe(top_products)