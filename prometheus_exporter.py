#!/usr/bin/env python

from prometheus_client import start_http_server, Metric, REGISTRY
import json
import time
from slugify import slugify

from typing import Dict

import logging
from tellduslive import read_credentials, Session, Device


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
                value: float
                # Add support for labeling later..
                #labels, Dict
                ):
            metric.add_sample(name, value=value, labels={})

        """Dump configured devices and sensors."""
        logging.basicConfig(level=logging.WARN)
        credentials = read_credentials()
        session = Session(**credentials)
        session.update()

        device_sensors = dict()
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
            s_name = raw_sensor.get('name','NO_NAME')
            c_name = raw_sensor.get('clientName', 'NO_CLIENTNAME')

            # Create a metric for this sensor
            sensor_metric = _new_metric('Sensor data located at {}'.format(s_name, c_name), 'histogram')

            # Iterate sensors and create a metric for each.
            if raw_sensor.get('data', False):
                data = raw_sensor.get('data')
                for measurement in data:
                    m_name = measurement['name']
                    metric_name = 'telldus_{}_{}_{}'.format(
                            slugify(c_name, separator='_'),
                            slugify(s_name, separator='_'),
                            m_name)

                    _add_metric(sensor_metric, metric_name, float(measurement['value']))

            yield sensor_metric

if __name__ == '__main__':
    tlc = TelldusLiveCollector()
    start_http_server(40001, addr='192.168.1.1')
    REGISTRY.register(TelldusLiveCollector())

    while True: time.sleep(30)
