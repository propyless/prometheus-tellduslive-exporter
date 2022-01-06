FROM python:3.8-alpine

COPY requirements.txt /exporter/

WORKDIR /exporter/
RUN apk add --no-cache git curl && \
	pip install -r requirements.txt

COPY prometheus_exporter.py /exporter/

USER 1000:1000
ENTRYPOINT ["python3", "prometheus_exporter.py"]
