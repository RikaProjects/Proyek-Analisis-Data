import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

st.set_page_config(
    page_title="E-Commerce Dashboard",
    layout="wide"
)

sns.set(style="whitegrid")

@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/all_data.csv")
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    return df

df = load_data()

min_date = df["order_purchase_timestamp"].min().date()
max_date = df["order_purchase_timestamp"].max().date()

with st.sidebar:

    st.title("E-Commerce Dashboard")

    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

df_filtered = df[
    (df["order_purchase_timestamp"].dt.date >= start_date) &
    (df["order_purchase_timestamp"].dt.date <= end_date)
]

def top_revenue_categories(data):

    result = (
        data.groupby("product_category_name")["price"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    result["formatted_price"] = result["price"].apply(
        lambda x: format_currency(x, "IDR", locale="id_ID")
    )

    return result

def top_review_categories(data):

    result = (
        data.groupby("product_category_name")["review_score"]
        .mean()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    return result

def order_trend(data):

    trend = data.copy()

    trend["month"] = trend["order_purchase_timestamp"].dt.to_period("M")

    trend = (
        trend.groupby("month")
        .size()
        .reset_index(name="order_count")
    )

    trend["month"] = trend["month"].astype(str)

    return trend

total_orders = len(df_filtered)

total_revenue = df_filtered["price"].sum()

avg_review = df_filtered["review_score"].mean()

formatted_revenue = format_currency(
    total_revenue,
    "IDR",
    locale="id_ID"
)

st.header("Dashboard E-Commerce")

col1, col2, col3 = st.columns(3)

col1.metric("Total Pesanan", f"{total_orders:,}")

col2.metric("Total Pendapatan", formatted_revenue)

col3.metric("Rata-rata Review", f"{avg_review:.2f}")

st.subheader("Top 5 Kategori dengan Pendapatan Tertinggi")

revenue_data = top_revenue_categories(df_filtered)

fig, ax = plt.subplots()

sns.barplot(
    data=revenue_data,
    x="price",
    y="product_category_name",
    ax=ax
)

st.pyplot(fig)

st.subheader("Top 5 Kategori dengan Review Tertinggi")

review_data = top_review_categories(df_filtered)

fig, ax = plt.subplots()

sns.barplot(
    data=review_data,
    x="review_score",
    y="product_category_name",
    ax=ax
)

st.pyplot(fig)

st.subheader("Trend Pesanan per Bulan")

trend_data = order_trend(df_filtered)

fig, ax = plt.subplots()

sns.lineplot(
    data=trend_data,
    x="month",
    y="order_count",
    marker="o",
    ax=ax
)

plt.xticks(rotation=45)

st.pyplot(fig)

st.caption("Copyright © Rika Rostika Afipah")
