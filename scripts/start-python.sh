#!/bin/bash
logfile=/log/start.log
date=$(date)

mkdir -p /log

echo "$date : Plugin-Service (Python) starting" >> "$logfile"
echo "Starting plugin-demo-python with uvicorn..."

exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port "${PORT:-8080}" \
    --log-level "${LOG_LEVEL:-info}"
