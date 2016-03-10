# coding=utf-8
# Copyright 2016 NUTC i.m.a.c.
# All Rights Reserved

from ConfigParser import SafeConfigParser

FILE_PATH = "/etc/rpi-collector/rpi-collector.conf"


class Configuration:
    def __init__(self, conf_path):
        self.conf_path = conf_path
        self.parser = SafeConfigParser()
        self.parser.read(self.conf_path)

    def sensor_path(self):
        return self.parser.get("default", "sensor_id_path")

    def time_interval(self):
        return self.parser.getint("default", "time_interval")

    def message_queue_type(self):
        return self.parser.get("message_queue", "type")

    def message_queue_address(self):
        return self.parser.get("message_queue", "address")

    def message_queue_port(self):
        return self.parser.get("message_queue", "port")

    def message_queue_topic(self):
        return self.parser.get("message_queue", "topic_name")

    def message_queue_qos(self):
        return self.parser.get("message_queue", "qos_level")
