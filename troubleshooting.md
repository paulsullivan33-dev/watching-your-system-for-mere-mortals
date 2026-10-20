# Troubleshooting

Five symptoms, each either reproduced
on the build machine while this guide
was being written or labelled as the
description it honestly is.

## Load is high, but the CPU is idle

The signature from chapter 5, staged on
purpose: six writers doing synchronous
disk I/O, and —

```
%Cpu(s): 53.0 us,  4.8 sy,  0.0 ni,  0.0 id, 41.1 wa,  0.0 hi,  1.0 si,  0.2 st
$ ps -eo stat | grep -c ^D
6
```

The load average counts state-D threads
(chapter 2); they use no CPU while they
wait, and `wa` is the waiting made
visible. So the machine reports a queue
(load above the core count) while its
cores stand idle with nothing to run.
The diagnosis order: `wa` first, then
the D count, then `ps -eo pid,stat,args`
to name the waiters — on the build
machine they were the specimen writers,
asleep inside the kernel at
`wait_log_commit`, which is the journal
of a filesystem doing exactly what
synchronous writes ask of it. On your
machine the names will be a database, a
backup, an NFS mount that stopped
answering. The fix belongs to the I/O,
never to the messenger: renicing,
killing, and adding CPU all leave the
disk exactly as slow as it was.

## The zombie you cannot kill

You can't, and the attempt is captured
to prove it isn't stubbornness:

```
$ kill -KILL 9475   # aiming at the zombie itself
$ ps -o pid,ppid,stat,args -p 9475
    PID    PPID STAT COMMAND
   9475    9463 Z    [python3] <defunct>
```

KILL is the signal nothing can ignore,
and the zombie is unmoved — because
there is no process left to receive a
signal. 9475 is an exit notice in a
table (chapter 4), and signals aren't
delivered to mail. The address for a
zombie is always the **parent** in its
PPID column: a healthy parent reaps
promptly, a stuck one must be prodded
or restarted, and a dead one's children
pass to PID 1, which reaps as a matter
of constitution. If zombies are
*multiplying*, the parent is the
disease; count them with
`ps -eo stat | grep -c ^Z` and fix
upward.

## The 100% process that is fine

A user reports a process "at 100%" as
if the machine were melting. top's
arithmetic (chapter 5): 100% is one
core. The lab spinner at 99.0 on a
2-core machine had the %Cpu(s) line
reporting 44.7% idle beside it — half
the machine free, one process
legitimately busy. A single-threaded
program *cannot* use more than one
core; its ceiling and its crime are the
same number. The readings that would
make it a problem are the machine-level
ones: `id` pinned at 0, load standing
above the core count, and other work
queueing. Absent those, a process at
100% is a process at work — and if a
colleague's top says 50 for the same
load, one of you has Solaris mode on
(chapter 5 again); compare modes before
comparing numbers.

## The process that vanished

You saw it once; a second look finds
nothing, and grep of the next census is
empty. Before concluding anything
sinister, meet the churner's children
(chapter 4): a one-second `sleep`,
present in one `pstree` (PID 9513),
replaced minutes later (10143), absent
entirely in a snapshot that fell between
children. Processes that live for a
second or less — cron's grandchildren,
health checks, build steps, connection
handlers — routinely begin and end
between snapshot tools' looks. The
working response is to watch the
*parent* (long-lived, attributable) or
to watch faster and into a file
(chapter 9). A vanishing process with
a living parent is usually a rhythm,
not an intruder. A vanishing *parent*,
with no exit you scheduled, earns the
OOM killer's records a look (chapter
7) — on a machine where you're
permitted to read them.

## Swap thrash (described, not captured)

This symptom could not be staged: the
build machine has no swap at all
(chapter 7), and the guide doesn't
pretend otherwise. Described, then, in
the terms the other chapters built.
The working set of everything running
exceeds RAM; the kernel evicts pages to
swap to make room; the evicted pages
are wanted again almost immediately and
are swapped back in; the disk becomes
the memory's bottleneck. The watching
signature: load high (the waiting
counts), `wa` high, %CPU low, the
machine audibly and measurably crawling
— and, decisive, *sustained swap
movement*, `vmstat`'s `si`/`so` columns
refusing to return to zero. Swap
*occupancy* alone proves nothing; cold
pages can sit out there for weeks.
Movement is the symptom. The remedies
belong to other shelves — more RAM,
less appetite, a hog from recipe 2
ended kindly — but the diagnosis is
this guide's whole job, and it is made
from the same five numbers as
everything else here.
