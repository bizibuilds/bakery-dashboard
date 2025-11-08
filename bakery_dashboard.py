# 🎂 Day 20 — Streamlit Dashboard (Optimized for Streamlit Cloud)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- PAGE CONFIG ---
st.set_page_config(page_title="Bakery Sales Dashboard", page_icon="🍞", layout="wide")

st.title("🍰 Bakery Sales Dashboard")
st.markdown("Visualizing daily performance from the bakery sales database or CSV backup.")

# --- LOAD DATA FUNCTION ---
@st.cache_data
def load_data():

    data = pd.DataFrame()
    try:
        data = pd.read_csv("cleaned_bakery_sales.csv")
        st.info("📁 Loaded data from local CSV file (backup mode).")
    except Exception as e:
        st.error(f"❌ Unable to load data: {e}")

    return data


# --- LOAD DATA ---
data = load_data()

if not data.empty:
    # --- CALCULATIONS ---
    data["revenue"] = data["units_sold"] * data["unit_price"]
    data["profit"] = (data["unit_price"] - data["cost_per_unit"]) * data["units_sold"]

    # --- SIDEBAR FILTERS ---
    st.sidebar.header("Filters")
    city = st.sidebar.multiselect("Select City", options=data["city"].unique(), default=data["city"].unique())
    product = st.sidebar.multiselect("Select Product", options=data["product"].unique(), default=data["product"].unique())

    df_filtered = data.query("city in @city and product in @product")

    # --- KPIs ---
    total_revenue = round(df_filtered["revenue"].sum(), 2)
    total_profit = round(df_filtered["profit"].sum(), 2)
    avg_price = round(df_filtered["unit_price"].mean(), 2)

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Revenue", f"${total_revenue}")
    col2.metric("📈 Total Profit", f"${total_profit}")
    col3.metric("🏷️ Avg. Price", f"${avg_price}")

    st.markdown("---")

    # --- CHARTS ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Revenue by City")
        city_rev = df_filtered.groupby("city")["revenue"].sum().reset_index()
        fig, ax = plt.subplots()
        sns.barplot(x="city", y="revenue", data=city_rev, palette="magma", ax=ax)
        ax.set_ylabel("Revenue ($)")
        st.pyplot(fig)

    with col2:
        st.subheader("Profit by Product")
        prod_profit = df_filtered.groupby("product")["profit"].sum().reset_index()
        fig, ax = plt.subplots()
        sns.barplot(x="product", y="profit", data=prod_profit, palette="crest", ax=ax)
        ax.set_ylabel("Profit ($)")
        st.pyplot(fig)

    st.markdown("---")

    # --- DATA TABLE ---
    st.subheader("Detailed Sales Data")
    st.dataframe(df_filtered)

else:
    st.warning("⚠️ No data available. Check database connection or ensure 'cleaned_bakery_sales.csv' exists.")


# --- FOOTER ---
st.markdown("---")
st.caption("👩‍💻 Built by Bizi Builds | Data Analytics Course — Day 20 | Powered by Streamlit 🌐")
