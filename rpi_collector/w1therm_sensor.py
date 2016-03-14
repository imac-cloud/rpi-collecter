# coding=utf-8
# Copyright 2016 NUTC i.m.a.c.
# All Rights Reserved

import time
import datetime
import logging
from w1thermsensor import W1ThermSensor

from rpi_collector.base_sensor import BaseSensor


LOG = logging.getLogger("collect.W1ThermSensor")


class Temperature(BaseSensor):

    SENSOR_TYPE = {
        'DS18S20': W1ThermSensor.THERM_SENSOR_DS18S20, 'DS1822': W1ThermSensor.THERM_SENSOR_DS1822,
        'DS18B20': W1ThermSensor.THERM_SENSOR_DS18B20, 'DS1825': W1ThermSensor.THERM_SENSOR_DS1825,
        'DS28EA00': W1ThermSensor.THERM_SENSOR_DS28EA00, 'MAX31850K': W1ThermSensor.THERM_SENSOR_MAX31850K
    }

    def __init__(self, sensor_id, sensor_type, **kwargs):
        super(Temperature, self).__init__(**kwargs)
        self.kwargs = kwargs

        sensor_type = self.SENSOR_TYPE[sensor_type]
        if sensor_type is None:
            LOG.error("Sensor Type Error ...")

        self.sensor = W1ThermSensor(
            sensor_type,
            sensor_id
        )

    def get_data(self):
        return self.sensor.get_temperature()

    # if you want to run on thread, you can call "start()" method
    def run(self):
        while True:
            message = "{time}, {temp}".format(
                time=datetime.datetime.now(),
                temp=self.get_data(),
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
