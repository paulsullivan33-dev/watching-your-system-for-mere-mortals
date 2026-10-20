#!/usr/bin/env python3
"""Lab specimen: a sleeper.

Sleeps for a stated number of seconds
(default 600), using no CPU and almost no
memory. It exists so the watching tools have
a process in state S (sleeping) whose name
you know, and so process trees have a quiet
child to point at.

Usage: python3 lab-sleeper.py [seconds]
"""
import os
import sys
import time


def main() -> None:
    seconds = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    print(f"lab-sleeper: pid {os.getpid()}, "
          f"sleeping for {seconds}s", flush=True)
    time.sleep(seconds)
    print(f"lab-sleeper: pid {os.getpid()} woke up",
          flush=True)


if __name__ == "__main__":
    main()
