import json
import logging
import os
import time
from typing import Any

import joblib
import pandas as pd
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

from common.config import (
    CONSUMER_AUTO_OFFSET_RESET,
    CONSUMER_GROUP_ID,
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_TOPIC_TRANSACTIONS,
    MAX_KAFKA_RETRIES,
    MODEL_PATH,
    STREAM_RESULTS_PATH,
)
from common.logging_utils import setup_logging

logger = logging.getLogger("consumer")


def create_consumer_with_retry() -> KafkaConsumer:
    for attempt in range(1, MAX_KAFKA_RETRIES + 1):
        try:
            consumer = KafkaConsumer(
                KAFKA_TOPIC_TRANSACTIONS,
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                group_id=CONSUMER_GROUP_ID,
                enable_auto_commit=False,
                auto_offset_reset=CONSUMER_AUTO_OFFSET_RESET,
            )
            logger.info("Consumer conectado ao Kafka em %s", KAFKA_BOOTSTRAP_SERVERS)
            return consumer
        except NoBrokersAvailable:
            sleep_time = min(2**attempt, 30)
            logger.warning(
                "Kafka indisponível (tentativa %s/%s). Tentando novamente em %ss...",
                attempt,
                MAX_KAFKA_RETRIES,
                sleep_time,
            )
            time.sleep(sleep_time)

    raise RuntimeError("Não foi possível conectar ao Kafka após múltiplas tentativas")


def is_valid_transaction(payload: dict[str, Any]) -> bool:
    return isinstance(payload.get("transaction_id"), int) and isinstance(payload.get("amount"), (int, float))


def save_result(data: dict[str, Any]) -> None:
    df_results = pd.DataFrame([data])
    file_exists = os.path.exists(STREAM_RESULTS_PATH)
    df_results.to_csv(
        STREAM_RESULTS_PATH,
        mode="a",
        header=not file_exists,
        index=False,
    )


def main() -> None:
    setup_logging()
    model = joblib.load(MODEL_PATH)
    logger.info("Modelo carregado de %s", MODEL_PATH)

    consumer = create_consumer_with_retry()

    for message in consumer:
        data = message.value

        if not is_valid_transaction(data):
            logger.warning("Mensagem inválida recebida: %s", data)
            consumer.commit()
            continue

        df = pd.DataFrame([data])
        prediction = model.predict(df[["amount"]])[0]

        data["fraud_prediction"] = int(prediction)
        save_result(data)
        consumer.commit()

        logger.info(
            "Processado transaction_id=%s prediction=%s",
            data.get("transaction_id"),
            data["fraud_prediction"],
        )


if __name__ == "__main__":
    main()
