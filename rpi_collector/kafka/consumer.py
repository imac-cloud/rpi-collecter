# coding=utf-8
# Copyright 2016 NUTC i.m.a.c.
# All Rights Reserved

import logging
import datetime
from threading import Thread
from kafka import KafkaConsumer

LOG = logging.getLogger("collect.kafka.consumer")


class Consumer(Thread):

    def __init__(self, host, port, **kwargs):
        super(Consumer, self).__init__()
        self.kwargs = kwargs
        self.topic = self.kwargs['topic'] if 'topic' in self.kwargs else "default"

        self.consumer = KafkaConsumer(
            bootstrap_servers="{host}:{port}".format(host, port),
            auto_offset_reset='earliest'
        )
        self.consumer.subscribe([self.topic])

    def run(self):
        for message in self.consumer:
            LOG.debug("{} , Message is \"{}\"".format(
                datetime.datetime.now(),
                message
            ))
