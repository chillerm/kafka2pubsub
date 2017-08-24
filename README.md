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

You can see the file related to data partitioning and logs for the topic here `/tmp/kafka-logs/`


#### Clustered

Next we'll create a kafka cluster with 3 nodes.  I'm going to assume you still have the previous instance running.  Copy 2 more server property files that will represent the 2 new nodes.

```apple js
cp config/server.properties config/server-1.properties
cp config/server.properties config/server-2.properties
```

Once copied, open up these files and make the below modifications:
```apple js
config/server-1.properties:
    broker.id=1
    listeners=PLAINTEXT://:9093
    log.dir=/tmp/kafka-logs-1
 
config/server-2.properties:
    broker.id=2
    listeners=PLAINTEXT://:9094
    log.dir=/tmp/kafka-logs-2
```

Now go ahead and start these 2 brokers and run them in the background.  If you prefer to run them in seperate terminsals just omit the `&`
```apple js
bin/kafka-server-start.sh config/server-1.properties &
bin/kafka-server-start.sh config/server-2.properties &
```

Now we'll create a new topic with a replication factor of 3.  This will take advantage of the extra nodes we just stood up:
```apple js
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 1 --topic my-replicated-topic
```

Let's start up a producer and consumer again to push messages to this new topic:
```apple js
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic my-replicated-topic
```
In a separate Terminal
```apple js
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --from-beginning --topic my-replicated-topic
```

Go ahead and write some messages again.  Once you have a few messages published, lets simulate a  node failing by killing it's parent process.
```apple js
ps aux | grep server-1.properties
# Find the PID
#kill -9 <your-PID>
kill -9 kill -9 81432
```

Now lets take a look at the state of the topics we've created:
```apple js
bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic my-replicated-topic
#Topic:my-replicated-topic	PartitionCount:1	ReplicationFactor:3	Configs:
#	Topic: my-replicated-topic	Partition: 0	Leader: 0	Replicas: 0,1,2	Isr: 0
bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic test
#Topic:test	PartitionCount:1	ReplicationFactor:1	Configs:
#	Topic: test	Partition: 0	Leader: 0	Replicas: 0	Isr: 0
```

If you look at your producer / consumer consoles now, you should not notice any difference either.  You should also still be able to send messages without issue.



Go ahead and create a file with a couple lines of text that we will read:
```apple js
echo -e "Heyo I'm a message\nI'm a new message.  See how I'm on my own line?" > test.txt
```

Now lets see if we can make it kafkaesque.  First lets start a single standalone cluster (This is ideal for dev environments) and give it a source (File) and sink (Another File).
```apple js
bin/connect-standalone.sh config/connect-standalone.properties config/connect-file-source.properties config/connect-file-sink.properties
```

Now, let's see what our new file contains:
```apple js
cat test.sink.txt
```

Nice!  Now, let's take a look at the topic itself.  Also, note we're this one will read the entire history of the topic (Go ahead and run this on previous topics too to see ALL messages you have history for)
```
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic connect-test --from-beginning```
```

Very cool.  Now note we did not kill our standalone process.  Let's see what happens if we add a line of text to our source file.
```apple js
echo "Another line" >> test.txt
```

Now check the file and topic again.
```apple js
cat test.sink.txt
echo "Another line" >> test.txt
```


That's awesome.  I'll leave the clean up to you for now :)


## Running the tests

No tests. I know right... Terrible.

