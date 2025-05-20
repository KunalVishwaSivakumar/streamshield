# 🛡️ StreamShield - Real-Time Fraud Detection & Monitoring Pipeline

StreamShield is a real-time data engineering pipeline that detects potential fraud in live retail transactions using Apache Kafka, MongoDB, and an LLM-based fraud classifier. It also provides a Streamlit dashboard for visual monitoring.

---

## 📌 Features

- 📡 Kafka ingestion for streaming retail transaction data
- 🗃️ MongoDB storage for real-time transactional events
- 🧠 LLM (OpenAI) based fraud classification
- 📊 Streamlit dashboard with auto-refresh, search, filters, and summary analytics

---

## 🧱 Architecture

```
Kafka Producer → Kafka Broker → Python Consumer → MongoDB → Streamlit Dashboard
                                     ↓
                                 LLM (OpenAI)
```

---

## 📂 Project Structure

```
streamshield/
│
├── kafka_producer/
│   └── sample_producer.py          # Sends mock transactions to Kafka
│
├── notebooks/
│   └── kafka_to_mongo.py           # Kafka consumer → MongoDB
│
├── llm_monitoring/
│   └── openai_client.py            # Fraud detection using OpenAI GPT
│
├── dashboard/
│   └── streamlit_app.py            # Real-time dashboard UI
│
└── .env                            # OpenAI API Key
```

---

## 🚀 Getting Started

### 1. Install Requirements

```bash
pip install -r requirements.txt
```

### 2. Set OpenAI Key

Create a `.env` file:

```
OPENAI_API_KEY=your-openai-api-key-here
```

### 3. Start Services

```bash
docker compose up -d --build
```

This launches Kafka, Zookeeper, and MongoDB.

### 4. Produce Sample Data

```bash
python kafka_producer/sample_producer.py
```

### 5. Start the Consumer

```bash
python notebooks/kafka_to_mongo.py
```

This consumes Kafka messages and stores them in MongoDB.

### 6. Enable LLM Classification (Optional)

```bash
python llm_monitoring/openai_client.py
```

This tags records in MongoDB with `"fraud_check": "FRAUD"` or `"LEGIT"`.

### 7. Run Dashboard

```bash
streamlit run dashboard/streamlit_app.py
```

---

## 📊 Dashboard Features

- 🔁 Auto-refresh with “Refresh Now” button
- 🔎 Filter: All / FRAUD / LEGIT
- 🔍 Search: order_id, user_id, product
- 📈 Visuals: Fraud over time, Top products, Total fraud amount
- 🧾 Real-time transactions table

---

## 👤 Author

Kunal Vishwa Sivakumar  
[LinkedIn](https://www.linkedin.com/in/kunalvishwasivakumar/)
