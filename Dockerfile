FROM python:3

COPY requirements.txt /exporter/

WORKDIR /exporter/
RUN pip install -r requirements.txt

COPY prometheus_exporter.py /exporter/

USER 1000:1000
ENTRYPOINT ["python3", "prometheus_exporter.py"]
