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
from rpi_collector.common import logs
from rpi_collector.common import config
from rpi_collector.temperature import Temperature

LOG = logging.getLogger("collect")


def main():
    sh = logging.StreamHandler()
    sh.setFormatter(logs.color_format())
    sh.setLevel(logging.WARNING)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(sh)
    sh.setLevel(logging.DEBUG)

    conf = config.Configuration(config.FILE_PATH)

    sensor = Temperature(
        sensor_id_path=conf.sensor_path(),
        interval=conf.time_interval(),
        mq_type=conf.message_queue_type(),
        mq_address=conf.message_queue_address(),
        mq_port=conf.message_queue_port(),
        mq_topic=conf.message_queue_topic(),
        mq_qos=conf.message_queue_qos(),
    )

    # if you want to run on thread, you can call "start()" method
    sensor.run()


if __name__ == '__main__':
    main()
