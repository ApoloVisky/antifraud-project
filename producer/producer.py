import json
import logging
import random
import time

from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

from common.config import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_TOPIC_TRANSACTIONS,
    MAX_KAFKA_RETRIES,
    PRODUCER_INTERVAL_SECONDS,
)
from common.logging_utils import setup_logging

logger = logging.getLogger("producer")


def create_producer_with_retry() -> KafkaProducer:
    for attempt in range(1, MAX_KAFKA_RETRIES + 1):
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
            logger.info("Producer conectado ao Kafka em %s", KAFKA_BOOTSTRAP_SERVERS)
            return producer
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


def generate_transaction() -> dict:
    return {
        "transaction_id": random.randint(1, 100000),
        "amount": random.randint(1, 5000),
        "event_time": int(time.time()),
    }


def main() -> None:
    setup_logging()
    producer = create_producer_with_retry()

    while True:
        transaction = generate_transaction()
        producer.send(KAFKA_TOPIC_TRANSACTIONS, transaction)
        producer.flush()
        logger.info("Enviado: %s", transaction)
        time.sleep(PRODUCER_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
