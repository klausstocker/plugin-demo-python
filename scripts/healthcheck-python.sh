#!/bin/bash
hc=/healthcounter
logfile=/log/start.log

result=$(curl --fail http://localhost:"${PORT:-8080}"/ping 2>/dev/null)

if [ "$result" = "pong" ]; then
    rm -f "$hc"
    exit 0
fi

# Increment unhealthy counter
count=0
if [ -f "$hc" ]; then
    count=$(cat "$hc")
fi
count=$((count + 1))
echo "$count" > "$hc"

max_retries="${UNHEALTHY_RETRIES:-100}"
if [ "$count" -ge "$max_retries" ]; then
    echo "$(date) : Health check failed $count times – terminating." >> "$logfile"
    kill 1
fi

exit 1
