#!/usr/bin/env python

from prometheus_client import start_http_server, Metric, REGISTRY
import json
import time
from slugify import slugify

from typing import Dict

import logging
from tellduslive import read_credentials, Session, Device
import sys


class TelldusLiveCollector(object):
    def __init__(self):
        pass

    def collect(self):
        def _new_metric(
                metric_desc: str,
                metric_name: str
                ):
            metric = Metric(
                    'telldus_sensor_data',
                    metric_desc, metric_name)
            return metric

        def _add_metric(
                metric: Metric,
                name: str,
                value: float,
                labels: Dict
                ):
            metric.add_sample(name, value=value, labels=labels)

        """Dump configured devices and sensors."""
        logging.basicConfig(level=logging.WARN)
        credentials = read_credentials()
        session = Session(**credentials)
        session.update()

        device_sensors = dict()
        sensor_metric = _new_metric('Sensor data fromm Telldus Live', 'histogram')

        # Iterate over all the device IDS.
        for device in session.device_ids:
            # Get the raw device info.
            sensor = Device(session, device)

            # Is it a device or a sensor?
            if not sensor.is_sensor:
                continue

            # It's a sensor lets continue
            raw_sensor = sensor.device

            # Grab some values we may want to use later on...
            s_id = raw_sensor.get('id','NO_ID')
            s_name = slugify(raw_sensor.get('name','NO_NAME'), separator='_')
            c_name = slugify(raw_sensor.get('clientName', 'NO_CLIENTNAME'), separator='_')

            # Iterate sensors and create a metric for each.
            if raw_sensor.get('data', False):
                data = raw_sensor.get('data')

                for measurement in data:
                    m_name = measurement['name']
                    metric_name = 'telldus_sensor'
                    _add_metric(sensor_metric, metric_name, float(measurement['value']),
                            labels={'client_name': c_name, 'sensor_name': s_name, 'metric_name': m_name,
                                    'sensor_scale': measurement['scale']}
                        )

        yield sensor_metric

if __name__ == '__main__':
    if len(sys.argv) == 2:
        bind_ip = sys.argv[1]
    else:
        bind_ip = '0.0.0.0'
    tlc = TelldusLiveCollector()
    start_http_server(40001, addr=bind_ip)
    REGISTRY.register(TelldusLiveCollector())

    while True: time.sleep(30)
