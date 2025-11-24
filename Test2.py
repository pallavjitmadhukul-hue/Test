import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Test Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data(path):
    df = pd.read_csv(path, parse_dates=["Order Date", "Ship Date"])
    return df

df = load_data("Superstore.csv")

# -----------------------------
# HEADER WITH LOGO + TITLE
# -----------------------------
# -----------------------------
# HEADER WITH LOGO LEFT + TITLE RIGHT
# -----------------------------
header = st.container()
with header:
    col1, col2 = st.columns([2, 8])

    with col1:
        st.image("logo2.png", width=250)

    with col2:
        st.markdown(
            """
            <div style='text-align:center;'>
                <h1 style='margin-bottom:0px;'>Test Dashboard</h1>
                <p style='color:#666;margin-top:0px;'>Test dashboard built using Python + Streamlit</p>
            </div>
            """,
            unsafe_allow_html=True
        )


# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("Filters")

min_date = df["Order Date"].min()
max_date = df["Order Date"].max()

date_range = st.sidebar.date_input(
    "Select Order Date Range",
    [min_date.date(), max_date.date()]
)

start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

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

# -----------------------------
# FILTER DATA
# -----------------------------
filtered = df[
    (df["Order Date"] >= start_date) &
    (df["Order Date"] <= end_date) &
    (df["Category"].isin(categories)) &
    (df["Sub-Category"].isin(subcategories))
]

# -----------------------------
# KPIs SECTION
# -----------------------------
st.markdown("#### Key Performance Indicators")
st.write("")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("Total Sales", f"${filtered['Sales'].sum():,.2f}")
kpi2.metric("Total Profit", f"${filtered['Profit'].sum():,.2f}")
kpi3.metric("Total Quantity", f"{int(filtered['Quantity'].sum()):,}")
kpi4.metric("Avg Discount", f"{filtered['Discount'].mean():.2%}")

st.markdown("---")

# -----------------------------
# TREND CHARTS
# -----------------------------
#st.markdown("<b>Sales & Profit Trends<b>", unsafe_allow_html=True)

# st.markdown("#### Sales & Profit Trends")

# left, right = st.columns([2, 1])

# with left:
#     monthly = (
#         filtered
#         .resample("M", on="Order Date")[["Sales", "Profit"]]
#         .sum()
#         .reset_index()
#     )

#     if not monthly.empty:
#         fig = px.line(
#             monthly,
#             x="Order Date",
#             y=["Sales", "Profit"],
#             markers=True,
#             title="Monthly Sales vs Profit Trend",
#             labels={"value": "$ Amount"}
#         )
#         fig.update_layout(height=450)
#         st.plotly_chart(fig, use_container_width=True)
#     else:
#         st.info("No Data Available")

st.markdown("#### Sales & Profit Trends")

left, right = st.columns([2, 1])

with left:
    monthly = (
        filtered
        .resample("M", on="Order Date")[["Sales", "Profit"]]
        .sum()
        .reset_index()
    )

    if not monthly.empty:

        import plotly.graph_objects as go

        fig = go.Figure()

        # --- Sales as Area ---
        fig.add_trace(go.Scatter(
            x=monthly["Order Date"],
            y=monthly["Sales"],
            mode="lines",
            fill="tozeroy",
            name="Sales",
            line=dict(width=2, color="#6EC2F7"),    
            fillcolor="rgba(110,194,247,0.4)"
        ))

        # --- Profit as Line ---
        fig.add_trace(go.Scatter(
            x=monthly["Order Date"],
            y=monthly["Profit"],
            mode="lines+markers",
            name="Profit",
            line=dict(width=3, color="#003049")
        ))

        fig.update_layout(
            title="Monthly Sales vs Profit Trend",
            yaxis_title="$ Amount",
            height=450
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No Data Available")


with right:
    if not filtered.empty:
        cat_sales = filtered.groupby("Category", as_index=False)["Sales"].sum()
        fig2 = px.bar(
            cat_sales,
            x="Category",
            y="Sales",
            color="Category",
            color_discrete_sequence=["#FDC400", "#006EFF", "#00D819"],
            title="Sales by Category",
            text_auto=".2s"
        )
        fig2.update_layout(height=450)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Data Not Available")

st.markdown("---")

# -----------------------------
# TOP PRODUCTS
# -----------------------------
st.markdown("#### Top Selling Products")

top_n = st.slider("Select number of products", 5, 25, 10)

top_products = (
    filtered.groupby("Product Name", as_index=False)
    .agg({"Sales": "sum", "Profit": "sum", "Quantity": "sum"})
    .sort_values("Sales", ascending=False)
    .head(top_n)
)

st.dataframe(top_products, use_container_width=True)
