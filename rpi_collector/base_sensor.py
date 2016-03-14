# coding=utf-8
# Copyright 2016 NUTC i.m.a.c.
# All Rights Reserved

import logging
import datetime
from threading import Thread

from rpi_collector.mqtt.publish import Publish
from rpi_collector.kafka.producer import Producer

LOG = logging.getLogger("collect.BaseSensor")


class BaseSensor(Thread):
    def __init__(self, **kwargs):
        super(BaseSensor, self).__init__()
        self.kwargs = kwargs

        self.mq_type = self.kwargs["mq_type"] if self.kwargs["mq_type"] != "None" else None
        self.interval = float(self.kwargs["interval"])

        if self.mq_type == "kafka":
            self.producer_client = Producer(
                self.kwargs["mq_address"],
                self.kwargs["mq_port"],
            )

    def _publish_message(self, message):
        publish_client = Publish(
            self.kwargs["mq_address"],
            self.kwargs["mq_port"],
            topic=self.kwargs["mq_topic"],
            qos=self.kwargs["mq_qos"],
        )
        publish_client.message = message
        publish_client.start()

    def _producer_message(self, message):
        self.producer_client.message = message

        # if you want to run on thread, you can call "start()" method
        self.producer_client.run()

    def run_once(self, message):
        message = "{time}, {message}".format(
            time=datetime.datetime.now(),
            message=message,
        )
        try:
            if self.mq_type == "mqtt":
                self._publish_message(message)
            elif self.mq_type == "kafka":
                self._producer_message(message)
        except Exception as e:
            LOG.error("%s" % (e.__str__()))

        LOG.info(message)
