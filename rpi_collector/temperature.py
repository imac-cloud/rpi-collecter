# coding=utf-8
# Copyright 2016 NUTC i.m.a.c.
# All Rights Reserved

import time
import datetime
import logging
from threading import Thread

from rpi_collector.mqtt.publish import Publish
from rpi_collector.kafka.producer import Producer

LOG = logging.getLogger("Temperature")


class Temperature(Thread):
    def __init__(self, sensor_id_path, interval, **kwargs):
        super(Temperature, self).__init__()
        self.kwargs = kwargs

        self.mq_type = self.kwargs["mq_type"] if self.kwargs["mq_type"] != "None" else None

        self.interval = interval
        self.sensor_path = sensor_id_path

    def parse_data(self, content):
        data = content.split("\n")[1].split(" ")[9]
        return float(data[2:]) / 1000

    def _publish_message(self, message):
        try:
            publish_client = Publish(
                self.kwargs["mq_address"],
                self.kwargs["mq_port"],
                topic=self.kwargs["mq_topic"],
                qos=self.kwargs["mq_qos"],
            )
            publish_client.message = message
            publish_client.start()
        except Exception as e:
            LOG.error("%s" % (e.__str__()))

    def _producer_message(self, message):
        try:
            producer_client = Producer(
                self.kwargs["mq_address"],
                self.kwargs["mq_port"],
                topic=self.kwargs["mq_topic"],
            )
            producer_client.message = message
            producer_client.start()
        except Exception as e:
            LOG.error("%s" % (e.__str__()))

    # if you want to run on thread, you can call "start()" method
    def run(self):
        while True:
            sensor_file = open(self.sensor_path)
            sensor_content = sensor_file.read()
            sensor_file.close()
            message = "{time}, {temp}".format(
                time=datetime.datetime.now(),
                temp=self.parse_data(sensor_content)
            )
            if self.mq_type == "mqtt":
                self._publish_message(message)
            elif self.mq_type == "kafka":
                self._producer_message(message)

            LOG.info(message)
            time.sleep(self.interval)
