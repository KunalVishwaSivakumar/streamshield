import json, time, random
from faker import Faker
from kafka import KafkaProducer

fake = Faker()

KAFKA_TOPIC = "retail-transactions"
KAFKA_BROKER = "localhost:9092"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

print("🚀 Starting live Kafka producer...")

while True:
    event = {
        "order_id": fake.uuid4(),
        "user_id": fake.uuid4(),
        "product": random.choice(["Mouse", "Keyboard", "Monitor", "Speaker"]),
        "amount": round(random.uniform(25.0, 500.0), 2),
        "timestamp": fake.iso8601()
    }
    producer.send(KAFKA_TOPIC, value=event)
    print(f"✅ Sent: {event}")
    time.sleep(2)
