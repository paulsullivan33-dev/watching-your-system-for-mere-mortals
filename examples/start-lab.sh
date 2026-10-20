#!/bin/sh
# Start the whole lab: one spinner, one memory
# eater, one family, one zombie parent. PIDs are
# recorded in .lab-pids next to this script so
# stop-lab.sh can end exactly what this started.
# Specimens run for 600 seconds by default and
# then exit on their own even if never stopped.
set -eu
cd "$(dirname "$0")"
SECONDS_TO_RUN="${1:-600}"
: > .lab-pids
for spec in "lab-spinner.py $SECONDS_TO_RUN" \
            "lab-memory-eater.py 200 $SECONDS_TO_RUN" \
            "lab-family.py $SECONDS_TO_RUN" \
            "lab-zombie-parent.py $SECONDS_TO_RUN"; do
    # Deliberate word splitting: each entry is
    # "script args...".
    # shellcheck disable=SC2086
    nohup python3 $spec > "/tmp/$(echo "$spec" | cut -d' ' -f1).out" 2>&1 &
    echo "$!" >> .lab-pids
done
echo "Lab started; PIDs in examples/.lab-pids"
echo "Stop it any time with: sh stop-lab.sh"
