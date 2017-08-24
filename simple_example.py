import json
import logging

from kafka.errors import KafkaError

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

from google.cloud import pubsub
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
from faker import Faker

fake = Faker()


PUBSUB_TOPIC = 'kafka2pubsub'
PUBSUB_SUBSCRIPTION = 'pubsub2world'

__pubsub_client = pubsub.Client()
pubsub_topic = __pubsub_client.topic(name=PUBSUB_TOPIC, timestamp_messages=True)
if not pubsub_topic.exists():
    pubsub_topic.create()
    LOGGER.warning("Created PubSub Topic: " + pubsub_topic.name)

pubsub_subscription = pubsub_topic.subscription(PUBSUB_SUBSCRIPTION)
if not pubsub_subscription.exists():
    pubsub_subscription.create()
    LOGGER.warning("Created Pubsub Subscription: " + pubsub_subscription.name + " on the Topic: " + pubsub_subscription.topic.name)

LOGGER.info("Prepared Subscription: " + pubsub_topic.project + ":" + pubsub_topic.name + "." + pubsub_subscription.name)



KAFKA_TOPIC = 'simpleTopic'
KAFKA_PORT = '9092'
BOOTSTRAP_SERVER='localhost:{}'.format(KAFKA_PORT)

kafka_producer = KafkaProducer(bootstrap_servers=[BOOTSTRAP_SERVER])

for i in range(20):
    address=fake.address()
    future = kafka_producer.send(KAFKA_TOPIC, str(address).encode('utf-8'))
    try:
        record_metadata = future.get(timeout=10)
    except KafkaError as e:
        LOGGER.error("published: {}".format(address), e)
        pass

kafka_producer.close(timeout=120)
# LOGGER.warning("I'm outside the production loop.")

kafka_consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=[BOOTSTRAP_SERVER], auto_offset_reset='earliest', enable_auto_commit=True)
for message in kafka_consumer:
    print ("Pulled Message... {Topic: %s, Partition: %d, Offset: %d, Key: %s, Value: %s}" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))


#################################################
#   YOU NEED TO TERMINATE THIS PROCESS MANUALLY #
#################################################