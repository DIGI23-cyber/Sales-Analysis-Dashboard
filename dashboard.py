import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import textwrap
import numpy as np


st.set_page_config(page_title="SUPERSTORE DASHBOARD",page_icon="📊",layout="wide")
# STEP 52 - PREMIUM DASHBOARD THEME

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a,
        #172554,
        #1e1b4b
    );
}

[data-testid="stMetric"] {
    background: linear-gradient(
        135deg,
        #1e3a8a,
        #312e81
    );
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #475569;
    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
}

[data-testid="stMetricLabel"] {
    color: #bfdbfe;
    font-size: 15px;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #ffffff;
    font-size: 30px;
    font-weight: 800;
}

h1, h2, h3 {
    color: #93c5fd !important;
    font-weight: 800 !important;
}

[data-testid="stPlotlyChart"] {
    background: rgba(30, 41, 59, 0.65);
    padding: 12px;
    border-radius: 18px;
    border: 1px solid #334155;
}

[data-testid="stSidebar"] {
    background: #111827;
}

</style>
""", unsafe_allow_html=True)
st.title("📊Superstore sales Analytics Dashboard")
st.markdown("### Bussiness performence & Insights") 
st.write("welcome to the superstore sales analysis dashboard")

df=pd.read_excel("sample_-_superstore.xls")

st.sidebar.markdown("## Date Filter")
start_date = st.sidebar.date_input("start Date",df["Order Date"].min())
end_date = st.sidebar.date_input("End Date",df["Order Date"].max())
filtered_df=df[(df["Order Date"].dt.date >= start_date)&(df["Order Date"].dt.date <= end_date)]


st.sidebar.markdown("## Data filters")
selected_category = st.sidebar.multiselect("Select Category",options=sorted(filtered_df["Category"].dropna().unique()),
default=sorted(filtered_df["Category"].dropna().unique()),key="category_filter")
filtered_df = filtered_df[filtered_df["Category"].isin(selected_category)]

total_sales = filtered_df["Sales"].sum()
total_profit =filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
avg_discount=filtered_df["Discount"].mean()
st.markdown("## 📌 Bussiness overview")
col1,col2,col3,col4=st.columns(4)
with col1:
    st.metric( label="💰Total sales", value=f"${total_sales:,.2f}")
with col2:
    st.metric(label="📈 Total Profit",value=f"${total_profit:,.2f}")
with col3:
    st.metric(label=" 🛒Total Orders",value=f"{total_orders:,}")
with col4:
    st.metric(label="🏷️ Average Discount",value=f"{avg_discount:.1%}")

# Step 47 - Discount Analysis

st.subheader("🏷️ Discount Analysis")

# Average Discount by Category

discount_data = (
    filtered_df.groupby("Category")["Discount"]
    .mean()
    .reset_index()
)

fig1 = px.bar(
    discount_data,
    x="Category",
    y="Discount",
    color="Discount",
    text_auto=".2f",
    title="Average Discount by Category",
    color_continuous_scale="Viridis",
    template="plotly_dark"
)

st.plotly_chart(fig1, use_container_width=True)
# PREMIUM CATEGORY WISE SALES

st.markdown("---")
st.subheader("🛍️ Category Wise Sales Performance")

category_sales = (
    filtered_df.groupby("Category")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum")
    )
    .reset_index()
)

fig = px.bar(
    category_sales,
    x="Category",
    y="Total_Sales",
    color="Category",
    text_auto=".2s",
    hover_data=["Total_Profit"],
    title="Sales Performance by Category",
    template="plotly_dark",
    color_discrete_sequence=px.colors.qualitative.Bold
)

fig.update_layout(
    height=450,
    title_x=0.5,
    xaxis_title="Product Category",
    yaxis_title="Total Sales",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(
    category_sales,
    use_container_width=True,
    hide_index=True
)

df["Order Date"]=pd.to_datetime(df["Order Date"])
monthly_sales = filtered_df.groupby(filtered_df["Order Date"].dt.to_period("M"))["Sales"].sum()
monthly_sales.index=monthly_sales.index.astype(str)
st.markdown("##📈 monthly sales trend")
st.line_chart(monthly_sales)
st.markdown("## 📈category wise profit")
category_profit=filtered_df.groupby("Category")["Profit"].sum()
st.bar_chart(category_profit)
st.markdown("##🛍️Sub-Category wise sales")
sub_category_sales=filtered_df.groupby("Sub-Category")["Sales"].sum()
st.bar_chart(sub_category_sales)

# =====================================
# TOP 10 PRODUCTS BY SALES AND PROFIT
# =====================================

st.markdown("---")
st.header("🏆 Top 10 Product Performance")

# 1. TOP 10 PRODUCTS BY SALES

st.subheader("💰 Top 10 Products by Sales")

top_sales_products = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .nlargest(10)
    .sort_values()
    .reset_index()
)

fig1 = px.bar(
    top_sales_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    color="Sales",
    text_auto=".2s",
    title="Top 10 Products by Total Sales",
    template="plotly_dark",
    color_continuous_scale="Blues"
)

fig1.update_layout(
    height=550,
    title_x=0.5,
    xaxis_title="Total Sales",
    yaxis_title="Product Name"
)

st.plotly_chart(fig1, use_container_width=True)


# 2. TOP 10 PRODUCTS BY PROFIT

st.subheader("📈 Top 10 Products by Profit")

top_profit_products = (
    filtered_df.groupby("Product Name")["Profit"]
    .sum()
    .nlargest(10)
    .sort_values()
    .reset_index()
)

fig2 = px.bar(
    top_profit_products,
    x="Profit",
    y="Product Name",
    orientation="h",
    color="Profit",
    text_auto=".2s",
    title="Top 10 Products by Total Profit",
    template="plotly_dark",
    color_continuous_scale="Viridis"
)

fig2.update_layout(
    height=550,
    title_x=0.5,
    xaxis_title="Total Profit",
    yaxis_title="Product Name"
)

st.plotly_chart(fig2, use_container_width=True)
st.markdown("## sales by ship mode")
ship_mode_sales = (filtered_df.groupby("Ship Mode")["Sales"].sum().sort_values(ascending=False))
st.bar_chart(ship_mode_sales)

st.subheader("🔥 Region vs Category Sales Heatmap")

heatmap_data = filtered_df.pivot_table(
    index="Region",
    columns="Category",
    values="Sales",
    aggfunc="sum",
    fill_value=0
)

fig = px.imshow(
    heatmap_data,
    text_auto=".0f",
    color_continuous_scale="Blues",
    labels=dict(
        x="Category",
        y="Region",
        color="Sales"
    ),
    aspect="auto"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📈 Monthly Sales Trend")

monthly_sales = filtered_df.groupby(
    filtered_df["Order Date"].dt.to_period("M")
)["Sales"].sum().reset_index()

monthly_sales["Order Date"] = (
    monthly_sales["Order Date"].astype(str)
)

fig = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    markers=True,
    title="Monthly Sales Performance",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)
st.write("heatmap data preview")
st.write(filtered_df[["Sales","Profit","Discount","Quantity"]].head())
st.markdown("## sales & profit correlation heatmap")
correlation=filtered_df[["Sales","Profit","Discount","Quantity"]].corr()
fig,ax=plt.subplots(figsize=(8,6))
sns.heatmap(correlation,annot=True,cmap="coolwarm",fmt=".2f",ax=ax)
st.pyplot(fig)
st.markdown("##🏆 Top 10 Best Selling products")

top_products = (df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head().reset_index())
fig=px.bar(top_products,x="Sales",y="Product Name",orientation="h",text="Sales",color="Sales",color_continuous_scale="Turbo",title="Top 10 Products by Sales")
fig.update_layout(template="plotly_dark",height=550,yaxis={"categoryorder":"total ascending"},showlegend=False)
st.plotly_chart(fig,use_container_width=True)
st.markdown("##📊 Sub-Category sales Analysis")
sub_category_sales = (df.groupby("Sub-Category")["Sales"].sum().sort_values(ascending=False).reset_index())
fig=px.bar(sub_category_sales,x="Sub-Category",y="Sales",text_auto=".2s",color_continuous_scale="Plasma",title="Sales performance by Sub-Category")
fig.update_layout(template="plotly_dark",height=500,xaxis_tickangle=-35,showlegend=False)
st.plotly_chart(fig,use_container_width=True)

st.markdown("##🏆 Top 10 Customers")

top_Customers = (df.groupby("Customer Name")["Sales"].sum().sort_values(ascending=False).head().reset_index())
fig=px.bar(top_Customers,x="Sales",y="Customer Name",orientation="h",text_auto=".2s",color="Sales",color_continuous_scale="Turbo",title="Top 10 Customers by Sales")
fig.update_layout(template="plotly_dark",height=500,yaxis={"categoryorder":"total ascending"},showlegend=False)
st.plotly_chart(fig,use_container_width=True)
st.markdown("##💰Profit by sub-category")
subcategory_profit = (df.groupby("Sub-Category")["Profit"].sum().sort_values(ascending=False).reset_index())
fig=px.bar(subcategory_profit,x="Sub-Category",y="Profit",color="Profit",text_auto=".2s",color_continuous_scale="RdYlGn",title="Profit Analysis by Sub-Category")
fig.update_layout(template="plotly_dark",height=500,xaxis_tickangle=-35,showlegend=False)
st.plotly_chart(fig,use_container_width=True)
# STEP 48 - SALES VS PROFIT ANALYSIS

st.markdown("---")
st.subheader("💹 Sales vs Profit Relationship")

fig = px.scatter(
    filtered_df,
    x="Sales",
    y="Profit",
    color="Category",
    size="Quantity",
    hover_name="Product Name",
    title="Sales vs Profit Analysis",
    template="plotly_dark",
    color_discrete_sequence=px.colors.qualitative.Bold
)

fig.update_layout(
    height=500,
    title_x=0.5,
    xaxis_title="Total Sales",
    yaxis_title="Total Profit"
)

st.plotly_chart(fig, use_container_width=True)

# STEP 50 - SALES FORECASTING

st.markdown("---")
st.subheader("🔮 Sales Forecasting")

# Monthly Sales Data

forecast_data = (
    filtered_df.set_index("Order Date")
    .resample("MS")["Sales"]
    .sum()
    .reset_index()
)

forecast_data.columns = ["Date", "Sales"]

if len(forecast_data) >= 3:

    forecast_data["Month"] = range(len(forecast_data))

    slope, intercept = np.polyfit(
        forecast_data["Month"],
        forecast_data["Sales"],
        1
    )

    future_months = np.arange(
        len(forecast_data),
        len(forecast_data) + 3
    )

    future_sales = slope * future_months + intercept

    future_dates = pd.date_range(
        start=forecast_data["Date"].max() +
        pd.offsets.MonthBegin(1),
        periods=3,
        freq="MS"
    )

    future_df = pd.DataFrame({
        "Date": future_dates,
        "Sales": future_sales,
        "Type": "Predicted"
    })

    forecast_data["Type"] = "Actual"

    combined_data = pd.concat(
        [forecast_data, future_df],
        ignore_index=True
    )

    fig = px.line(
        combined_data,
        x="Date",
        y="Sales",
        color="Type",
        markers=True,
        title="Actual vs Predicted Sales",
        template="plotly_dark",
        color_discrete_map={
            "Actual": "#00CC96",
            "Predicted": "#FFA15A"
        }
    )

    fig.update_layout(
        height=500,
        title_x=0.5
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:
    st.warning(
        "At least 3 months of sales data is required."
    )

# STEP 51 - ADVANCED DATA EXPORT

st.markdown("---")
st.subheader("📥 Download Business Reports")

col1, col2 = st.columns(2)

with col1:
    csv_file = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📄 Download CSV Report",
        data=csv_file,
        file_name="Business_Report.csv",
        mime="text/csv",
        use_container_width=True
    )

with col2:
    import io

    excel_buffer = io.BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:

        filtered_df.to_excel(
            writer,
            index=False,
            sheet_name="Sales Data"
        )

    st.download_button(
        label="📊 Download Excel Report",
        data=excel_buffer.getvalue(),
        file_name="Business_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

st.success("Your Business Reports Are Ready!")

# STEP 51 - BUSINESS RECOMMENDATIONS

st.markdown("---")
st.subheader("🧠 Key Business Recommendations")

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
avg_discount = filtered_df["Discount"].mean()

recommendations = []

if total_profit < 0:
    recommendations.append(
        "⚠️ Overall Profit is negative. "
        "Review pricing and operational costs."
    )
else:
    recommendations.append(
        "✅ Overall business is generating positive profit."
    )

if avg_discount > 0.20:
    recommendations.append(
        "⚠️ Average discount is high. "
        "Review discount strategies."
    )
else:
    recommendations.append(
        "✅ Average discount level is relatively controlled."
    )

category_profit = (
    filtered_df.groupby("Category")["Profit"].sum()
)

if not category_profit.empty:
    best_category = category_profit.idxmax()

    recommendations.append(
        f"🏆 Most profitable category: {best_category}"
    )

category_sales = (
    filtered_df.groupby("Category")["Sales"].sum()
)

if not category_sales.empty:
    best_sales_category = category_sales.idxmax()

    recommendations.append(
        f"📈 Highest sales category: {best_sales_category}"
    )

for recommendation in recommendations:
    st.info(recommendation)


st.markdown("## 🧠 Automatic Business Insights")

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()

best_category = (
    df.groupby("Category")["Sales"]
    .sum()
    .idxmax()
)

best_profit_category = (
    df.groupby("Category")["Profit"]
    .sum()
    .idxmax()
)

best_product = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .idxmax()
)

col1, col2 = st.columns(2)

with col1:
    st.success(f"🏆 Highest Sales Category: {best_category}")
    st.info(f"💰 Highest Profit Category: {best_profit_category}")

with col2:
    st.warning(f"📦 Best Selling Product: {best_product}")
    st.metric("Total Business Sales", f"${total_sales:,.2f}")

st.metric("Total Business Profit", f"${total_profit:,.2f}")

st.markdown("""
<style>

/* Premium KPI Cards */

[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        #1e293b,
        #312e81,
        #4338ca
    );

    padding: 25px;
    border-radius: 18px;
    border: 1px solid #818cf8;

    box-shadow:
        0 8px 25px rgba(79, 70, 229, 0.25);

    transition: all 0.3s ease;
}

/* Hover Animation */

[data-testid="stMetric"]:hover {
    transform: translateY(-6px);

    box-shadow:
        0 12px 30px rgba(99, 102, 241, 0.45);

    border: 1px solid #c4b5fd;
}

/* KPI Labels */

[data-testid="stMetricLabel"] {
    color: #c4b5fd !important;
    font-size: 15px;
    font-weight: 600;
}

/* KPI Values */

[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 30px;
    font-weight: 800;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a,
        #172554,
        #1e1b4b
    );
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

h1, h2, h3 {
    color: #ffffff !important;
    font-weight: 800 !important;
}

p, label, span {
    color: #e2e8f0;
}

[data-testid="stMetric"] {
    background: linear-gradient(
        135deg,
        #1e293b,
        #312e81
    );
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #6366f1;
    box-shadow: 0 5px 20px rgba(0,0,0,0.3);
}

[data-testid="stMetricLabel"] {
    color: #93c5fd !important;
}

[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 28px;
    font-weight: bold;
}

[data-testid="stSidebar"] {
    background: #111827;
}

[data-testid="stPlotlyChart"] {
    background: #1e293b;
    padding: 12px;
    border-radius: 16px;
    border: 1px solid #334155;
}

.stButton > button {
    background: linear-gradient(
        90deg,
        #6366f1,
        #a855f7
    );
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background: linear-gradient(120deg, #312e81, #1d4ed8, #2563eb); padding: 30px; border-radius: 20px; margin-bottom: 25px; box-shadow: 0 8px 25px rgba(0,0,0,0.3);">
<h1 style="color: white; font-size: 36px; margin-bottom: 8px;">📊 SALES ANALYTICS DASHBOARD</h1>
<p style="color: #dbeafe; font-size: 16px; margin-bottom: 15px;">Smart Business Intelligence | Performance Monitoring</p>
<span style="background: #ffffff30; padding: 8px 15px; border-radius: 20px; color: white; font-size: 13px;">✨ PREMIUM ANALYTICS</span>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style="text-align:center; padding:20px 5px;"><h1 style="color:#818cf8; font-size:28px;">📊 SALES PRO</h1><p style="color:#94a3b8; font-size:12px;"> BUSINESS INTELLIGENCE</p>
</div>
<hr style="border:1px solid #334155;">
""", unsafe_allow_html=True)

st.sidebar.markdown("""
### 🏠 Dashboard Overview

Your business performance at a glance.

---

### 📈 Analytics

- Sales Performance
- Profit Analysis
- Product Insights
- Customer Insights

---

### ⚙️ Dashboard

- Interactive Reports
- Business Insights
- Performance Tracking

---

""")

st.sidebar.info("✨ Premium Analytics Dashboard")

st.markdown("""
<style>

/* Premium Chart Containers */

[data-testid="stPlotlyChart"] {
    background: linear-gradient(
        145deg,
        #172554,
        #1e1b4b,
        #312e81
    );

    padding: 20px;
    border-radius: 20px;

    border: 1px solid #6366f1;

    box-shadow:
        0 8px 25px rgba(79, 70, 229, 0.20);

    transition: all 0.3s ease;
}

/* Chart Hover Effect */

[data-testid="stPlotlyChart"]:hover {
    transform: translateY(-4px);

    box-shadow:
        0 12px 30px rgba(99, 102, 241, 0.35);

    border-color: #a78bfa;
}

/* Section Headings */

h2 {
    border-left: 5px solid #818cf8;
    padding-left: 12px;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)

# STEP 53 - FINAL DASHBOARD STATUS

st.markdown("---")

st.subheader("✅ Dashboard System Status")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("Data Loaded")

with col2:
    st.success("Analytics Active")

with col3:
    st.success("Dashboard Ready")

st.markdown("---")

st.markdown("""
### 🚀 Business Analytics Dashboard

**All Analytics Features Are Ready!**

- Sales Analysis
- Profit Analysis
- Customer Insights
- Product Performance
- Sales Forecasting
- Interactive Data Filters
- Report Downloads

""")

st.caption("Professional Business Intelligence Dashboard")










