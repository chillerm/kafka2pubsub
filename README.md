Kafka2PubSub

Needed to look into Kafka for work.  Firgured it would be fun to build a pipe between Kafka and Pub Sub.  This is meant purely for fun and exploration. 

## Getting Started

To get started, go ahead and clone this repo and move into the newly created directory:
```angular2html
git clone https://github.com/chillerm/kafka2pubsub.git
cd kafka2pubsub
```

Next you're going to want to go pick up kafka and zookeeper.  You can read more about their relationship (and see the inspiration for this app) here: https://kafka.apache.org/quickstart For this tutorial used Kafka version "2.11-0.11.0.0" which you should be able to download here: https://kafka.apache.org/downloads

Alternately you can try download from the commandline and unzip it:
```
wget http://www-us.apache.org/dist/kafka/0.11.0.0/kafka_2.11-0.11.0.0.tgz
tar xzf kafka_2.11-0.11.0.0.tgz
```

At this point I like to rename the directory just to kafka.
```angular2html
mv kafka_2.11-0.11.0.0 kafka
cd kafka
``````

### Installing

There isn't really anything to install since it's just a couple scripts.  If you haven't I would, again, highly recommend checking out some of the examples in the quickstart here: https://kafka.apache.org/quickstart Aside from that, I've written up a few example commands below. 

### Some example shortcuts

Start zookeeper 
```angular2html
bin/zookeeper-server-start.sh config/zookeeper.properties
``` 
Start Kafka
```
bin/kafka-server-start.sh config/server.properties
```

Create Topic
```angular2html
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
```

Start interactive publisher.  Type some text and press `enter` to submit the message. (*cntrl-c* to stop):
```angular2html
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test
```

Start Consumer:
```angular2html
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning
```

Something fun to do is create a producer shell in one terminal and a consumer in another.  Then you can see messages show up in the consumer as you write them to the publisher.


## Running the tests

No tests. I know right... Terrible.

