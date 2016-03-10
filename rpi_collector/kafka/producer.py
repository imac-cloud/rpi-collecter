# coding=utf-8
# Copyright 2016 NUTC i.m.a.c.
# All Rights Reserved

import logging
from threading import Thread
from kafka import KafkaProducer

LOG = logging.getLogger("Producer")


class Producer(Thread):

    def __init__(self, host, port, **kwargs):
        super(Producer, self).__init__()
        self.kwargs = kwargs
        self.topic = self.kwargs['topic'] if 'topic' in self.kwargs else None
        self.message = None

        self.producer = KafkaProducer(
            bootstrap_servers="{host}:{port}".format(host, port),
            retries=5
        )

    def run(self):
        self.producer.send(self.topic, self.message)

