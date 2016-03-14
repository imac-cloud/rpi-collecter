# coding=utf-8
# Copyright 2016 NUTC i.m.a.c.
# All Rights Reserved
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

import logging
import time

from rpi_collector.common import logs
from rpi_collector.common import config

from rpi_collector import w1therm_sensor
from rpi_collector import adafruit_sensor
from rpi_collector import base_sensor

LOG = logging.getLogger("collect")


def check_sensors(ids, types):
    if len(ids) != len(types):
        LOG.error("Configuration Error ...")
        exit(1)

    return ids, types


def main():
    conf = config.Configuration(config.FILE_PATH)

    if conf.debug():
        sh = logging.StreamHandler()
        sh.setFormatter(logs.color_format())
        sh.setLevel(logging.WARNING)

        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        root_logger.addHandler(sh)
        sh.setLevel(logging.DEBUG)

    multi_mq = conf.multi_message_queue()
    sensors = []

    w1therm_ids, w1therm_types = check_sensors(
        conf.w1therm_sensors_id(),
        conf.w1therm_sensors_type()
    )

    mq_dict = {
        'interval': conf.time_interval(),
        'mq_type': conf.message_queue_type(),
        'mq_address': conf.message_queue_address(),
        'mq_port': conf.message_queue_port(),
        'mq_topic': conf.message_queue_topic(),
        'mq_qos': conf.message_queue_qos(),
    }

    for (sensor_id, sensor_type) in zip(w1therm_ids, w1therm_types):
        if sensor_id != "None" and sensor_type != "None":
            sensor = w1therm_sensor.Temperature(
                sensor_id=sensor_id,
                sensor_type=sensor_type,
                **mq_dict
            )
            # if you want to run on thread, you can call "start()" method
            if not multi_mq:
                sensors.append(sensor)
            else:
                sensor.start()

    adafruit_gpios, adafruit_types = check_sensors(
        conf.adafruit_sensors_gpio(),
        conf.adafruit_sensors_type(),
    )

    for (sensor_gpio, sensor_type) in zip(adafruit_gpios, adafruit_types):
        if sensor_gpio != "None" and sensor_type != "None":
            sensor = adafruit_sensor.AdafruitSensor(
                sensor_gpio=sensor_gpio,
                sensor_type=sensor_type,
                **mq_dict
            )
            # if you want to run on thread, you can call "start()" method
            if not multi_mq:
                sensors.append(sensor)
            else:
                sensor.start()

    if not multi_mq and len(sensors) > 0:
        push_client = base_sensor.BaseSensor(**mq_dict)
        while True:
            message = ""
            for sensor in sensors:
                data = sensor.get_data()
                if type(data) == tuple:
                    message += "{0:0.2f} ".format(data[0])
                else:
                    message += "{0} ".format(data)

            push_client.run_once(message)
            time.sleep(push_client.interval)
    else:
        LOG.error("No any sensors ...")


if __name__ == '__main__':
    main()
