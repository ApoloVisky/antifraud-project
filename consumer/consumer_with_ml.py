import json
import logging

import joblib
import pandas as pd
from kafka import KafkaConsumer

from common.config import (
    CONSUMER_AUTO_OFFSET_RESET,
    CONSUMER_GROUP_ID,
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_TOPIC_TRANSACTIONS,
    MODEL_PATH,
)
from common.logging_utils import setup_logging

logger = logging.getLogger("consumer_with_ml")


def main() -> None:
    setup_logging()
    model = joblib.load(MODEL_PATH)

    consumer = KafkaConsumer(
        KAFKA_TOPIC_TRANSACTIONS,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id=CONSUMER_GROUP_ID,
        auto_offset_reset=CONSUMER_AUTO_OFFSET_RESET,
    )

    for message in consumer:
        data = message.value
        df = pd.DataFrame([data])
        prediction = model.predict(df[["amount"]])[0]

        data["fraud_prediction"] = int(prediction)
        logger.info("Processado: %s", data)


if __name__ == "__main__":
    main()
