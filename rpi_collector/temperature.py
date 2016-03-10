# coding=utf-8
# Copyright 2016 NUTC i.m.a.c.
# All Rights Reserved
# Supporting DS18B20

import time
import datetime
import logging
from threading import Thread

from rpi_collector.mqtt.publish import Publish
from rpi_collector.kafka.producer import Producer

LOG = logging.getLogger("collect.temperature")


class Temperature(Thread):
    def __init__(self, sensor_id_path, interval, **kwargs):
        super(Temperature, self).__init__()
        self.kwargs = kwargs

        self.mq_type = self.kwargs["mq_type"] if self.kwargs["mq_type"] != "None" else None

        self.interval = interval
        self.sensor_path = sensor_id_path

        if self.mq_type == "kafka":
            self.producer_client = Producer(
                self.kwargs["mq_address"],
                self.kwargs["mq_port"],
                topic=self.kwargs["mq_topic"],
            )

    def parse_data(self, content):
        data = content.split("\n")[1].split(" ")[9]
        return float(data[2:]) / 1000

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
            try:
                if self.mq_type == "mqtt":
                    self._publish_message(message)
                elif self.mq_type == "kafka":
                    self._producer_message(message)
            except Exception as e:
                LOG.error("%s" % (e.__str__()))

            LOG.info(message)
            time.sleep(self.interval)
