#!/bin/sh
# Start the whole lab: one spinner, one memory
# eater, one family, one zombie parent. Each
# specimen is recorded in .lab-pids next to this
# script as "pid start-time name", so stop-lab.sh
# can verify it is ending exactly what this
# started -- a bare PID is not an identity: if a
# specimen exits and its PID is recycled, the
# number alone would point at a stranger.
# Specimens run for 600 seconds by default and
# then exit on their own even if never stopped.
set -eu
cd "$(dirname "$0")"
SECONDS_TO_RUN="${1:-600}"

# A process's start time (clock ticks since boot)
# from /proc/<pid>/stat, field 22. The name in
# field 2 is parenthesised and may itself contain
# spaces, so strip through the last ')' first;
# the start time is then the 20th field left.
# Prints nothing when it cannot be read.
start_time_of() {
    sed 's/^.*) //' "/proc/$1/stat" 2>/dev/null | cut -d' ' -f20
}

: > .lab-pids
for spec in "lab-spinner.py $SECONDS_TO_RUN" \
            "lab-memory-eater.py 200 $SECONDS_TO_RUN" \
            "lab-family.py $SECONDS_TO_RUN" \
            "lab-zombie-parent.py $SECONDS_TO_RUN"; do
    # Deliberate word splitting: each entry is
    # "script args...".
    # shellcheck disable=SC2086
    nohup python3 $spec > "/tmp/$(echo "$spec" | cut -d' ' -f1).out" 2>&1 &
    pid=$!
    name=$(echo "$spec" | cut -d' ' -f1)
    started=$(start_time_of "$pid")
    [ -n "$started" ] || started="?"
    echo "$pid $started $name" >> .lab-pids
done
echo "Lab started; PIDs in examples/.lab-pids"
echo "Stop it any time with: sh stop-lab.sh"
