from kafka import KafkaConsumer
import json
import joblib
import pandas as pd

model = joblib.load("fraud_model.pkl")

consumer = KafkaConsumer(
    "transactions",
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    data = message.value
    df = pd.DataFrame([data])

    prediction = model.predict(df[["amount"]])[0]

    data["fraud_prediction"] = int(prediction)

    print("Processado:", data)
