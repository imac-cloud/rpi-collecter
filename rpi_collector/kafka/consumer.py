# coding=utf-8

import logging
import time
import threading
from kafka import KafkaConsumer


class Consumer(threading.Thread):
    daemon = True

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                                 auto_offset_reset='earliest')
        consumer.subscribe(['my-topic'])

        for message in consumer:
            print (message)


def main():
    threads = [
        Consumer(),
    ]

    for t in threads:
        t.start()

    time.sleep(10)


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
    )
    main()
