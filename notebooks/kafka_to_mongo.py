import os
import json
from kafka import KafkaConsumer
from pymongo import MongoClient
from openai import OpenAI
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# ✅ Kafka Consumer Setup
consumer = KafkaConsumer(
    "retail-transactions",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    enable_auto_commit=True,
    group_id="streamshield-consumer-group",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

# ✅ MongoDB Setup
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["streamshield"]
collection = db["kafka_messages"]

# ✅ LLM Fraud Detection Function
def ask_gpt_fraud(transaction: dict) -> str:
    prompt = f"""Analyze the following transaction and determine if it is FRAUD or LEGIT:
    
Transaction:
- Order ID: {transaction['order_id']}
- User ID: {transaction['user_id']}
- Product: {transaction['product']}
- Amount: ${transaction['amount']}
- Timestamp: {transaction['timestamp']}

Respond with only one word: FRAUD or LEGIT."""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip().upper()

# ✅ Start pipeline
print("✅ Started Kafka → MongoDB pipeline with LLM-based fraud detection...")

for message in consumer:
    data = message.value
    print(f"📥 Message from Kafka: {data}")

    try:
        # 🧠 Classify using GPT
        fraud_result = ask_gpt_fraud(data)
        data["fraud_check"] = fraud_result

        # 💾 Store in MongoDB
        collection.insert_one(data)
        print(f"✅ Inserted into MongoDB with fraud_check = {fraud_result}")
    except Exception as e:
        print(f"❌ Error processing message: {e}")
