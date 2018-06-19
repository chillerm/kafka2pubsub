import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

from app import kafka_service, pubsub_service


def print_from_start(svc_kafka):
    for message in svc_kafka.subscribe_from_start():
        print("{Topic: %s, Partition: %d, Offset: %d, Key: %s, Value: %s}" % (message.topic, message.partition,
                                                                              message.offset, message.key,
                                                                              message.value))


def pipe_kafka_2_pubsub(svc_kafka, svc_pubsub):
    for message in svc_kafka.subscribe_from_start():
        pub_id = svc_pubsub.publish(message.value)
        LOGGER.info("Published Message ID: {}".format(pub_id))


def main():
    ks = kafka_service.KafkaService()
    ps = pubsub_service.PubSubService()
    # print_from_start(ks)
    pipe_kafka_2_pubsub(ks, ps)


if __name__ == '__main__':
    main()
