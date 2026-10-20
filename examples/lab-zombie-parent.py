#!/usr/bin/env python3
"""Lab specimen: a zombie maker.

Forks a child that exits immediately, then
sleeps WITHOUT reaping it, for a stated
number of seconds (default 600). The dead
child stays in the process table as a
zombie (state Z, <defunct>) because its
exit notice has nowhere to go until the
parent collects it or dies. Harmless: a
zombie holds a table entry and nothing
else — no CPU, no memory to speak of.

Usage: python3 lab-zombie-parent.py [seconds]
"""
import os
import sys
import time


def main() -> None:
    seconds = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    print(f"lab-zombie-parent: pid {os.getpid()}",
          flush=True)
    child = os.fork()
    if child == 0:
        # The child: exits at once, on purpose.
        os._exit(0)
    print(f"lab-zombie-parent: child {child} has "
          f"exited and will not be reaped for "
          f"{seconds}s", flush=True)
    time.sleep(seconds)
    # On the way out, reap properly.
    os.waitpid(child, 0)
    print("lab-zombie-parent: reaped and exiting",
          flush=True)


if __name__ == "__main__":
    main()
