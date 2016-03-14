# coding=utf-8
# Copyright 2016 NUTC i.m.a.c.
# All Rights Reserved

from kafka import KafkaProducer
from kafka.common import KafkaError


class Producer(KafkaProducer):
    def __init__(self, host, port, topic):
        super(Producer, self).__init__(
            client_id="",
            bootstrap_servers=['{host}:{port}'.format(host=host, port=port)],
        )
        self.topic = topic
        self.message = None

    def push(self):
        future = self.send(self.topic, self.message)
        try:
            record_metadata = future.get(timeout=10)
        except KafkaError:
            pass

