import datetime
import logging
from time import sleep

from kafka import KafkaProducer as _KafkaProducer, KafkaConsumer as _KafkaConsumer
from kafka.errors import KafkaError
LOGGER = logging.getLogger(__name__)

class KafkaService():
    LOGGER = logging.getLogger(__name__)

    KAFKA_TOPIC = 'world2kafka'
    BOOTSTRAP_SERVER = 'localhost:9092'

    _producer = _KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER)

    @staticmethod
    def publish(message: str):
        future = KafkaService._producer.send(KafkaService.KAFKA_TOPIC, bytes(message.encode('utf-8')))
        try:
            record_metadata = future.get(timeout=10)
            KafkaService.LOGGER.info("Published to Kafka: {}".format(record_metadata))
            return record_metadata
        except KafkaError as e:
            KafkaService.LOGGER.error("Error attempting to publish message.", e)
            pass

    @staticmethod
    def subscribe_from_start():
        return _KafkaConsumer(KafkaService.KAFKA_TOPIC, bootstrap_servers=[KafkaService.BOOTSTRAP_SERVER], auto_offset_reset='earliest', enable_auto_commit=True)

if __name__ == "__main__":
    while True:
        message = "The Time is: {}".format(datetime.datetime.now())
        pub_meta = KafkaService.publish(message)
        print("Published Record..... {}".format(pub_meta))
        sleep(10)