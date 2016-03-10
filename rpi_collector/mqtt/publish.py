# coding=utf-8

import logging
from threading import Thread
import paho.mqtt.client as mqtt


LOG = logging.getLogger("collect.mqtt.publish")


class Publish(Thread):

    def __init__(self, host, port, **kwargs):
        super(Publish, self).__init__()

        self.kwargs = kwargs
        self.topic = self.kwargs['topic'] if 'topic' in self.kwargs else None
        self.qos = self.kwargs['qos'] if 'qos' in self.kwargs else 0
        self.publish_num = self.kwargs['publish_num'] if 'publish_num' in self.kwargs else 1
        self.message = None

        self.push_client = mqtt.Client(
            client_id="",
            clean_session=True,
            userdata=None,
        )
        self.push_client.connect(host, port, keepalive=60)

    def run(self):
        self.push_client.loop_start()
        self.push_client.publish(self.topic, self.message, qos=int(self.qos))
        self.push_client.loop_stop()
        self.push_client.disconnect()
