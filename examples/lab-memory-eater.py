#!/usr/bin/env python3
"""Lab specimen: a memory eater.

Allocates a stated number of megabytes
(default 200), touches every page so the
memory is really resident (RSS, not just
reserved), then holds it while sleeping for
a stated number of seconds (default 600).

SAFETY: the request is hard-capped at
300 MB inside this script. The lab must
never be able to push its own machine into
the OOM killer's arms; if you ask for more,
you get 300 and a note saying so.

Usage: python3 lab-memory-eater.py [megabytes] [seconds]
"""
import os
import sys
import time

HARD_CAP_MB = 300


def main() -> None:
    mb = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    seconds = int(sys.argv[2]) if len(sys.argv) > 2 else 600
    if mb > HARD_CAP_MB:
        print(f"lab-memory-eater: {mb} MB requested, "
              f"capped at {HARD_CAP_MB} MB by the "
              f"script's own safety limit", flush=True)
        mb = HARD_CAP_MB
    print(f"lab-memory-eater: pid {os.getpid()}, "
          f"allocating {mb} MB", flush=True)
    block = bytearray(mb * 1024 * 1024)
    # Touch one byte per page so the allocation
    # is resident, not merely reserved.
    for offset in range(0, len(block), 4096):
        block[offset] = 1
    print(f"lab-memory-eater: holding {mb} MB for "
          f"{seconds}s", flush=True)
    time.sleep(seconds)
    print(f"lab-memory-eater: pid {os.getpid()} "
          f"releasing and exiting", flush=True)


if __name__ == "__main__":
    main()
