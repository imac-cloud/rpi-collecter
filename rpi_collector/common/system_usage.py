# coding=utf-8
# Copyright 2016 NUTC i.m.a.c.
# All Rights Reserved


import psutil


def convert_unit_size(size, unit='MB'):
    if unit == 'KB':
        size /= 1024
    elif unit == 'MB':
        size /= 1024 * 1024
    elif unit == 'GB':
        size /= 1024 * 1024 * 1024
    return float(size)


def get_cpu_percent(interval=None):
    return psutil.cpu_percent(interval=None) if interval is None \
        else psutil.cpu_percent(interval=interval)


def get_cpu_count(logical=False):
    return psutil.cpu_count() if logical else psutil.cpu_count(logical=False)


def get_virtual_memory():
    mem = psutil.virtual_memory()
    return mem.used, mem.available, mem.total


def get_virtual_memory_percent():
    return psutil.virtual_memory().percent


def get_swap_memory():
    mem = psutil.swap_memory()
    return mem.used, mem.free, mem.total


def get_swap_memory_percent():
    return psutil.swap_memory().percent


def get_disk_usage():
    disk = psutil.disk_usage('/')
    return disk.used, disk.free, disk.total


def get_disk_usage_percen():
    return psutil.disk_usage('/').percent

