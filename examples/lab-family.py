#!/usr/bin/env python3
"""Lab specimen: a family.

A parent process that starts two children
from this same lab — a lab-sleeper and a
lab-churner — and then waits for them. It
exists so pstree and ps --forest have a
household whose members you know by name:
one quiet child, one child with children of
its own.

Usage: python3 lab-family.py [seconds]
"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> None:
    seconds = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    print(f"lab-family: parent pid {os.getpid()}, "
          f"starting children for {seconds}s",
          flush=True)
    children = [
        subprocess.Popen(
            [sys.executable,
             os.path.join(HERE, "lab-sleeper.py"),
             str(seconds)]),
        subprocess.Popen(
            [sys.executable,
             os.path.join(HERE, "lab-churner.py"),
             str(seconds)]),
    ]
    for child in children:
        child.wait()
    print(f"lab-family: parent pid {os.getpid()} "
          f"done", flush=True)


if __name__ == "__main__":
    main()
