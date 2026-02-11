import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC_TRANSACTIONS = os.getenv("KAFKA_TOPIC_TRANSACTIONS", "transactions")
PRODUCER_INTERVAL_SECONDS = float(os.getenv("PRODUCER_INTERVAL_SECONDS", "1"))
MODEL_PATH = os.getenv("MODEL_PATH", "model/fraud_model.pkl")
STREAM_RESULTS_PATH = os.getenv("STREAM_RESULTS_PATH", "stream_results.csv")
CONSUMER_GROUP_ID = os.getenv("CONSUMER_GROUP_ID", "fraud-consumer-group")
CONSUMER_AUTO_OFFSET_RESET = os.getenv("CONSUMER_AUTO_OFFSET_RESET", "earliest")
MAX_KAFKA_RETRIES = int(os.getenv("MAX_KAFKA_RETRIES", "10"))
