# coding=utf-8
# Copyright 2016 NUTC i.m.a.c.
# All Rights Reserved
# Supporting DS18B20

import time
import datetime
import logging
from threading import Thread
from w1thermsensor import W1ThermSensor

from rpi_collector.mqtt.publish import Publish
from rpi_collector.kafka.producer import Producer

LOG = logging.getLogger("collect.temperature")


class Temperature(Thread):

    SENSOR_TYPE = {
        'DS18S20': W1ThermSensor.THERM_SENSOR_DS18S20, 'DS1822': W1ThermSensor.THERM_SENSOR_DS1822,
        'DS18B20': W1ThermSensor.THERM_SENSOR_DS18B20, 'DS1825': W1ThermSensor.THERM_SENSOR_DS1825,
        'DS28EA00': W1ThermSensor.THERM_SENSOR_DS28EA00, 'MAX31850K': W1ThermSensor.THERM_SENSOR_MAX31850K
    }

    def __init__(self, sensor_id, interval, **kwargs):
        super(Temperature, self).__init__()
        self.kwargs = kwargs

        self.mq_type = self.kwargs["mq_type"] if self.kwargs["mq_type"] != "None" else None
        self.interval = interval

        sensor_type = self.SENSOR_TYPE[self.kwargs['sensor_type']]
        if sensor_type is None:
            LOG.error("Sensor Type Error ...")

        self.sensor = W1ThermSensor(
            sensor_type,
            sensor_id
        )

        if self.mq_type == "kafka":
            self.producer_client = Producer(
                self.kwargs["mq_address"],
                self.kwargs["mq_port"],
                topic=self.kwargs["mq_topic"],
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

    # if you want to run on thread, you can call "start()" method
    def run(self):
        while True:
            message = "{time}, {temp}".format(
                time=datetime.datetime.now(),
                temp=self.sensor.get_temperature()
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
