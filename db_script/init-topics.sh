#!/bin/bash
set -e
# Ждём, пока Kafka станет доступен
cub kafka-ready -b localhost:9092 1 20

kafka-topics \
  --bootstrap-server localhost:9092 \
  --create --if-not-exists \
  --topic profile_registration \
  --partitions 1 \
  --replication-factor 1 # в продакшене ставить >= 3