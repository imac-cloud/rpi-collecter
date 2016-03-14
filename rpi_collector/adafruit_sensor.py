# coding=utf-8
# Copyright 2016 NUTC i.m.a.c.
# All Rights Reserved


import time
import datetime
import logging
import Adafruit_DHT

from rpi_collector.base_sensor import BaseSensor


LOG = logging.getLogger("collect.AdafruitSensor")


class AdafruitSensor(BaseSensor):

    SENSOR_TYPE = {
        'DHT11': 11, 'DHT22': 2, 'AM2302': 22,
    }

    def __init__(self, sensor_gpio, sensor_type, **kwargs):
        super(AdafruitSensor, self).__init__(**kwargs)
        self.kwargs = kwargs

        self.sensor_gpio = sensor_gpio
        self.sensor_type = self.SENSOR_TYPE[sensor_type]

        if self.sensor_type is None:
            LOG.error("Sensor Type Error ...")

    def get_data(self):
        return Adafruit_DHT.read_retry(self.sensor_type, self.sensor_gpio)

    # if you want to run on thread, you can call "start()" method
    def run(self):
        while True:
            humidity, temperature = self.get_data()
            message = "{0}, {1:0.1f}%, {1:0.1f}%".format(
                datetime.datetime.now(),
                temperature,
                humidity
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


