Telldus Live Prometheus Exporter
================================

This is an exporter for telldus live sensor data.

It will retrieve a list of your devices from telldus live api
iterate each sensor, and report back the data to prometheus.

I only have one sensor at the time of development so I've not had
the chance to test with multiple sensors. But it should work (TM).


It uses the python tellduslive bindings from: https://github.com/molobrakos/tellduslive/

Follow the guide there for creating the credentials file..
