import streamlit as st
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import plotly.express as px

# 🔌 MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["streamshield"]
collection = db["kafka_messages"]

st.set_page_config(page_title="StreamShield Dashboard", layout="wide")
st.title("🛡️ StreamShield Transaction Monitor")

# 📥 Load Data from MongoDB
def load_data():
    data = list(collection.find({}, {"_id": 0}))
    return pd.DataFrame(data)

# 🔁 Manual Refresh
if st.button("🔄 Refresh Now"):
    st.rerun()

# 🚀 Main
try:
    df = load_data()
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # 🧠 Sanitize 'fraud_check' and compute fraud boolean
    if "fraud_check" in df.columns:
        df["fraud_check"] = df["fraud_check"].astype(str).str.strip().str.upper()
        df["fraud"] = df["fraud_check"] == "FRAUD"
    else:
        df["fraud"] = df["amount"] > 300  # Fallback rule

    # 🔍 Filters
    st.sidebar.header("🔎 Filters")
    fraud_filter = st.sidebar.selectbox("Transaction Type", ["All", "FRAUD", "LEGIT"])
    search_text = st.sidebar.text_input("Search (Order ID, User ID, Product)")

    # 💡 Apply filters
    if fraud_filter != "All":
        df = df[df["fraud_check"] == fraud_filter]
    if search_text:
        df = df[df.apply(lambda row: search_text.lower() in str(row.values).lower(), axis=1)]

    # 📊 Summary Stats
    st.subheader("📈 Summary Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transactions", len(df))
    col2.metric("Total Frauds", df["fraud"].sum())
    col3.metric("Avg Fraud Amount", round(df[df["fraud"]]["amount"].mean() or 0, 2))

    # 📄 Show Data Table
    st.subheader("🧾 Recent Transactions")
    st.dataframe(df.sort_values(by="timestamp", ascending=False), use_container_width=True)

    # 📉 Time-series of Fraud Volume
    st.subheader("📉 Fraud Over Time")
    df_group = df[df["fraud"]].groupby(df["timestamp"].dt.date).size().reset_index(name="Fraud Count")
    fig1 = px.line(df_group, x="timestamp", y="Fraud Count", title="Fraud Trend")
    st.plotly_chart(fig1, use_container_width=True)

    # 📦 Top Products with Most Frauds
    st.subheader("📦 Top Fraudulent Products")
    top_products = df[df["fraud"]]["product"].value_counts().nlargest(5).reset_index()
    top_products.columns = ["Product", "Count"]
    fig2 = px.bar(top_products, x="Product", y="Count", title="Top Products with Fraud")
    st.plotly_chart(fig2, use_container_width=True)

    # 💰 Total Fraud Amount by Product
    st.subheader("💰 Total Fraud Amount by Product")
    fraud_amount = df[df["fraud"]].groupby("product")["amount"].sum().reset_index()
    fig3 = px.bar(fraud_amount, x="product", y="amount", title="Fraud Amount by Product")
    st.plotly_chart(fig3, use_container_width=True)

except Exception as e:
    st.error(f"❌ Error loading data: {e}")
