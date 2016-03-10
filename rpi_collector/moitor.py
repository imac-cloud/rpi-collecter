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

import time
import datetime
import logging
from threading import Thread
from rpi_collector.common import logs

LOG = logging.getLogger("Monitor")


class Temperature(Thread):
    def __init__(self, sensor_id_path):
        super(Temperature, self).__init__()
        self.sensor_file = open(sensor_id_path)
        self.sensor_content = self.sensor_file.read()
        self.sensor_file.close()

    def parse_data(self):
        data = self.sensor_content.split("\n")[1].split(" ")[9]
        return float(data[2:]) / 1000

    def run(self):
        while True:
            now_time = datetime.datetime.now()
            LOG.info("{time}, {temp}".format(
                time=now_time,
                temp=self.parse_data()
            ))

            time.sleep(1)


def main():
    sh = logging.StreamHandler()
    sh.setFormatter(logs.color_format())
    sh.setLevel(logging.WARNING)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(sh)
    sh.setLevel(logging.DEBUG)

    sensor = Temperature("/sys/bus/w1/devices/28-00000758ff7b/w1_slave")
    sensor.run()


if __name__ == '__main__':
    main()
