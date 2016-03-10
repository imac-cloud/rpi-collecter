#!/usr/bin/env python
import sys
from rpi_collector.collector import main

"""
Collect temperature data using Raspberry Pi,
and publish to server using MQTT, Kafka
"""

if __name__ == "__main__":
    sys.exit(main())
