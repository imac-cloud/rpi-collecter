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

    def w1therm_sensors_id(self):
        ids = self.parser.get("default", "w1therm_sensors_id").split(",")
        return ids

    def w1therm_sensors_type(self):
        types = self.parser.get("default", "w1therm_sensors_type").split(",")
        return types

    def time_interval(self):
        return self.parser.getfloat("default", "time_interval")

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
