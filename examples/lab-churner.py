#!/usr/bin/env python3
"""Lab specimen: a short-lived process spawner.

Starts a `sleep 1` child, waits for it, waits
a moment, and repeats for a stated number of
seconds (default 600). At any instant there
is usually one very young child alive under
it. It exists so process trees and repeated
snapshots have something that changes.

Usage: python3 lab-churner.py [seconds]
"""
import os
import subprocess
import sys
import time


def main() -> None:
    seconds = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    deadline = time.time() + seconds
    print(f"lab-churner: pid {os.getpid()}, spawning "
          f"short-lived children for {seconds}s",
          flush=True)
    while time.time() < deadline:
        subprocess.run(["sleep", "1"], check=False)
        time.sleep(1)
    print(f"lab-churner: pid {os.getpid()} done",
          flush=True)


if __name__ == "__main__":
    main()
