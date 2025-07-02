#!/bin/bash
set -e
set -x

echo ">>> Waiting for Kafka to be ready…"
cub kafka-ready -b localhost:9092 1 20

echo ">>> Creating topic profile_registration…"
kafka-topics --bootstrap-server localhost:9092 \
             --create --if-not-exists \
             --topic profile_registration \
             --partitions 1 \
             --replication-factor 1
echo ">>> Topic created!"