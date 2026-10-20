#!/usr/bin/env python3
"""Lab specimen: a CPU spinner.

Burns one CPU core in a busy loop for a stated
number of seconds (default 600), then exits.
It does nothing useful with the cycles; that
is the point. Watching tools should show it
at or near 100% CPU for as long as it runs.

Usage: python3 lab-spinner.py [seconds]
"""
import os
import sys
import time


def main() -> None:
    seconds = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    deadline = time.time() + seconds
    print(f"lab-spinner: pid {os.getpid()}, "
          f"spinning for {seconds}s", flush=True)
    x = 0
    while time.time() < deadline:
        x += 1  # the world's least useful work
    print(f"lab-spinner: pid {os.getpid()} done "
          f"({x} loops)", flush=True)


if __name__ == "__main__":
    main()
