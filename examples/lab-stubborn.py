#!/usr/bin/env python3
"""Lab specimen: a stubborn process.

Ignores SIGTERM — the polite "please exit"
signal — and keeps sleeping. It exists so
the signals chapter can show the difference
between asking (TERM, which this specimen
refuses) and insisting (KILL, which no
process can refuse). SIGINT (Ctrl-C) still
works, and KILL always works; nothing here
can trap the machine, only demonstrate.

Usage: python3 lab-stubborn.py [seconds]
"""
import os
import signal
import sys
import time


def main() -> None:
    seconds = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    print(f"lab-stubborn: pid {os.getpid()}, ignoring "
          f"SIGTERM for {seconds}s", flush=True)
    time.sleep(seconds)
    print(f"lab-stubborn: pid {os.getpid()} exiting "
          f"on its own", flush=True)


if __name__ == "__main__":
    main()
