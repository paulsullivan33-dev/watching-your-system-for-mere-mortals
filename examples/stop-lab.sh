#!/bin/sh
# Stop exactly the lab processes start-lab.sh
# started, politely first (TERM), then firmly
# (KILL) for anything still standing.
#
# A recorded PID is never signalled on its own:
# PIDs get recycled, so a stale .lab-pids could
# otherwise name a stranger's process. Before
# signalling, the process now at a recorded PID
# must prove it is the one that was written down
# -- same start time as recorded at launch, and
# the specimen's name in its command line -- and
# the KILL pass checks again before it fires.
# Records that cannot prove their identity,
# including bare-PID records from older versions
# of start-lab.sh, are reported and skipped,
# never signalled.
set -eu
cd "$(dirname "$0")"
if [ ! -f .lab-pids ]; then
    echo "No .lab-pids file: the lab is not running (or was already stopped)."
    exit 0
fi

# Same /proc start-time reader as start-lab.sh.
start_time_of() {
    sed 's/^.*) //' "/proc/$1/stat" 2>/dev/null | cut -d' ' -f20
}

# is_recorded_process PID START-TIME NAME: true
# only when the process currently at PID is
# verifiably the recorded specimen.
is_recorded_process() {
    [ -d "/proc/$1" ] || return 1
    [ "$2" != "?" ] || return 1
    [ "$(start_time_of "$1")" = "$2" ] || return 1
    tr '\0' ' ' < "/proc/$1/cmdline" 2>/dev/null | grep -q "$3"
}

# First pass: verify every record, remember the
# ones that prove their identity.
verified=""
while read -r pid started name extra; do
    case $pid in ''|\#*) continue ;; esac
    if [ -z "${started:-}" ] || [ -z "${name:-}" ]; then
        echo "Skipping PID $pid: old-format record, its identity cannot be verified."
        continue
    fi
    [ -d "/proc/$pid" ] || continue
    if is_recorded_process "$pid" "$started" "$name"; then
        verified="$verified $pid:$started:$name"
    else
        echo "Skipping PID $pid: not the recorded $name (the PID may have been reused)."
    fi
done < .lab-pids

# Deliberate word splitting: $verified holds
# spaceless pid:start-time:name tokens.
# shellcheck disable=SC2086
for rec in $verified; do
    pid=${rec%%:*}
    pkill -TERM -P "$pid" 2>/dev/null || true
    kill -TERM "$pid" 2>/dev/null || true
done
sleep 2
# Anything left gets KILL -- after proving its
# identity again, in case it exited and its PID
# was recycled during the wait.
# shellcheck disable=SC2086
for rec in $verified; do
    pid=${rec%%:*}
    rest=${rec#*:}
    started=${rest%%:*}
    name=${rest#*:}
    if is_recorded_process "$pid" "$started" "$name"; then
        pkill -KILL -P "$pid" 2>/dev/null || true
        kill -KILL "$pid" 2>/dev/null || true
    fi
done
rm -f .lab-pids
echo "Lab stopped."
