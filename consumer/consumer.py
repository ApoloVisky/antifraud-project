import json
import logging

from kafka import KafkaConsumer

from common.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC_TRANSACTIONS
from common.logging_utils import setup_logging

logger = logging.getLogger("consumer_raw")


def main() -> None:
    setup_logging()

    consumer = KafkaConsumer(
        KAFKA_TOPIC_TRANSACTIONS,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )

    for message in consumer:
        logger.info("Recebido: %s", message.value)


if __name__ == "__main__":
    main()
