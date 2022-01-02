Telldus Live Prometheus Exporter
================================

This is an exporter for telldus live sensor data.

It will retrieve a list of your devices from telldus live api
iterate each sensor, and report back the data to prometheus.

It uses the python tellduslive bindings from: https://github.com/molobrakos/tellduslive/

Follow the guide there for creating the credentials file..


=== Example metric data
The metrics exported are formatted like so..:

```
# HELP telldus_sensor_data Sensor data fromm Telldus Live
# TYPE telldus_sensor_data histogram
telldus_sensor{client_name="engelbrekts",metric_name="temp",sensor_name="vaxthus"} 22.3
telldus_sensor{client_name="engelbrekts",metric_name="humidity",sensor_name="vaxthus"} 53.0
```
