Telldus Live Prometheus Exporter
================================

This is an exporter for telldus live sensor data.

It will retrieve a list of your devices from telldus live api
iterate each sensor, and report back the data to prometheus.

I only have one sensor at the time of development so I've not had
the chance to test with multiple sensors. But it should work (TM).


It uses the python tellduslive bindings from: https://github.com/molobrakos/tellduslive/

Follow the guide there for creating the credentials file..


=== Example metric data
The metrics exported are formatted like so..:

```
# HELP telldus_sensor_data Sensor data located at Växthus
# TYPE telldus_sensor_data histogram
telldus_<client_name>_<sensor_name>_<name_of_the_sensor_metric> 20.3
telldus_<client_name>_<sensor_name>_<name_of_the_sensor_metric> 69.0

# HELP telldus_sensor_data Sensor data located at Växthus
# TYPE telldus_sensor_data histogram
telldus_engelbrekts_greenhouse_temp 20.3
telldus_engelbrekts_greenhouse_humidity 69.0
```
