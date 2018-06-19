import logging

from google.cloud import pubsub
from kafka.errors import KafkaError

TOPIC_NAME = 'kafka2pubsub'
PUBSUB_SUBSCRIPTION = 'pubsub2world'


class PubSubService:
    def __init__(self):
        pass

    LOGGER = logging.getLogger(__name__)

    _client = pubsub.Client()
    _topic = _client.topic(name=TOPIC_NAME, timestamp_messages=True)
    if not _topic.exists():
        _topic.create()
        LOGGER.warning("Created PubSub Topic: " + _topic.name)

    _sub = _topic.subscription(PUBSUB_SUBSCRIPTION)
    if not _sub.exists():
        _sub.create()
        LOGGER.warning("Created Pubsub Subscription: " + _sub.name + " on the Topic: " + _sub.topic.name)

    LOGGER.info("Prepared Subscription: " + _topic.project + ":" + _topic.name + "." + _sub.name)

    @staticmethod
    def publish(message):
        message_id = PubSubService._topic.publish(message)
        PubSubService.LOGGER.debug("PubSub Publish ID: {}".format(message_id))
        return message_id

    @staticmethod
    def subscribe():
        return PubSubService._sub


if __name__ == '__main__':
    subscription = PubSubService.subscribe()
    while True:
        pubsubTuples = subscription.pull(max_messages=500)
        for pubsubTuple in pubsubTuples:
            message = pubsubTuple[1]
            print(
            "Pulled Message from PubSub Timestampped: {} ::::::: Data: {}".format(message.timestamp, message.data))
