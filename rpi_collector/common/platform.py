# coding=utf-8
# Copyright 2016 NUTC i.m.a.c.
# All Rights Reserved


import re

UNKNOWN = 0
RASPBERRY_PI = 1


class Platform(object):

    def __init__(self):
        super(Platform, self).__init__()
        self.version = None

    def detect(self):
        pi = self._pi_version()
        if pi is not None:
            self.version = pi
            return RASPBERRY_PI

        return UNKNOWN

    def _pi_revision(self):
        """
        Detect the revision number of a Raspberry Pi, useful for changing
        functionality like default I2C bus based on revision.
        """
        with open('/proc/cpuinfo', 'r') as infile:
            for line in infile:
                match = re.match('Revision\s+:\s+.*(\w{4})$', line, flags=re.IGNORECASE)
                if match and match.group(1) in ['0000', '0002', '0003']:
                    return 1
                elif match:
                    return 2
            raise RuntimeError('Could not determine Raspberry Pi revision.')

    def _pi_version(self):
        """
        Detect the version of the Raspberry Pi.
        """
        with open('/proc/cpuinfo', 'r') as infile:
            cpuinfo = infile.read()

        match = re.search('^Hardware\s+:\s+(\w+)$', cpuinfo,
                          flags=re.MULTILINE | re.IGNORECASE)

        if not match:
            # Couldn't find the hardware, assume it isn't a pi.
            return None
        if match.group(1) == 'BCM2708':
            # Pi 1
            return 1
        elif match.group(1) == 'BCM2709':
            # Pi 2
            return 2
        elif match.group(1) == 'BCM2710':
            # Pi 3
            return 3
        else:
            # Something else, not a pi.
            return None
