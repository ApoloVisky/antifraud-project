from kafka import KafkaConsumer
import json
import joblib
import pandas as pd

model = joblib.load("model/fraud_model.pkl")

consumer = KafkaConsumer(
    "transactions",
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

results = []

for message in consumer:
    data = message.value
    df = pd.DataFrame([data])
    prediction = model.predict(df[["amount"]])[0]

    data["fraud_prediction"] = int(prediction)
    results.append(data)

    df_results = pd.DataFrame(results)
    df_results.to_csv("stream_results.csv", index=False)

    print("Salvo:", data)
