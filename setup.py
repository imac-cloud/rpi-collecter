from setuptools import setup, find_packages
import sys

if sys.version_info <= (2, 5):
    error = "ERROR: rpi-collector requires Python Version 2.6 or above...exiting."
    print(error)
    sys.exit(1)

requirements = [
    'paho-mqtt>=1.1',
    'kafka-python>=1.0.1',
    'w1thermsensor>=0.3.0',
]

setup(
    name='rpi-collector',
    version='0.1.0',
    packages=find_packages(),
    description='Collect temperature data using Raspberry Pi',
    author='Kyle Bai',
    author_email='kyle.b@inwinstack.com',
    url='http://www.inwinstack.com/',
    install_requires=requirements,
    license="MIT",
    entry_points={
        'console_scripts': [
            'rpi-collector = rpi_collector.collector:main',
        ],
    },
)