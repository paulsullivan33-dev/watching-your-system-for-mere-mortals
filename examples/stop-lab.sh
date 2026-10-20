#!/bin/sh
# Stop exactly the lab processes start-lab.sh
# started, politely first (TERM), then firmly
# (KILL) for anything still standing.
set -eu
cd "$(dirname "$0")"
if [ ! -f .lab-pids ]; then
    echo "No .lab-pids file: the lab is not running (or was already stopped)."
    exit 0
fi
# TERM first, to parents and children alike.
while read -r pid; do
    pkill -TERM -P "$pid" 2>/dev/null || true
    kill -TERM "$pid" 2>/dev/null || true
done < .lab-pids
sleep 2
# Anything left gets KILL.
while read -r pid; do
    pkill -KILL -P "$pid" 2>/dev/null || true
    kill -KILL "$pid" 2>/dev/null || true
done < .lab-pids
rm -f .lab-pids
echo "Lab stopped."
