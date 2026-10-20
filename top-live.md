# top: The Live Screen

`top` is ps with a pulse. It repeats the
census every few seconds, sorts it by
appetite, and puts a five-line summary of
the whole machine on top. Everything in
this chapter is captured in **batch
mode** — `top -b` — which prints screens
as plain text instead of drawing them
for a terminal. Batch mode is the
capturable truth: what interactively is
a flickering display becomes, in batch,
a document you can save, diff, and quote
(chapter 9 builds on exactly that). One
batch-mode trap first, because it bites
everyone once: **the first screen's
percentages are averages since the
processes started**, not measurements of
the moment. Ask for two screens and read
the second:

```
$ top -b -n 2 -d 2        (first screen, header)
top - 11:09:08 up 18 min,  0 user,  load average: 2.19, 1.86, 1.11
Tasks:  17 total,   3 running,  13 sleeping,   0 stopped,   1 zombie
%Cpu(s): 90.5 us,  9.5 sy,  0.0 ni,  0.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
```

## The header, line by line

**Line 1** is `uptime` wearing a watch:
current time, how long the machine has
been up, and the load averages of
chapter 2.

**Line 2 — Tasks:** the census in one
breath. `17 total, 3 running, 13
sleeping, 0 stopped, 1 zombie` is the
state alphabet of chapter 3, counted.
On the lab machine: the two spinners
and one more were running; the zombie
is the specimen from chapter 4.

**Line 3 — %Cpu(s):** where the machine's
CPU went during the interval, in
percents of *all cores combined*:

- **us** — user: programs doing their own
  work. The spinners live here.
- **sy** — system: the kernel working on
  programs' behalf.
- **ni** — nice: user work running at
  lowered priority (chapter 8's lever,
  made visible).
- **id** — idle. The money column for
  "is the CPU the problem": 0.0 id with
  a queue means yes.
- **wa** — I/O wait: cores idle *because*
  the runnable work is waiting on I/O.
  The tell that separates "CPU-bound"
  from "disk-bound," and the subject of
  the capture below.
- **hi / si** — hardware and software
  interrupt time; usually small, named
  for completeness.
- **st** — steal: time this virtual
  machine wanted a core and the
  hypervisor gave it to a neighbour.
  The build machine, a sandbox, shows
  small nonzero `st` (0.2–0.9 in these
  captures) — a tenant's tax you can
  measure but not appeal.

**Lines 4–5 — Mem and Swap:** the memory
headline, decoded properly in chapter 7.
For now: `avail Mem` is the column to
trust, and this machine's Swap line is
all zeros because it has no swap at all.

## The table below the header

Same columns as ps, interval-flavoured:
%CPU here is *current* appetite. Second
screen of the same run, both spinners
at work:

```
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   9428 root      20   0   15476  10464   6604 R  76.1   0.1   0:24.35 python3
   9435 root      20   0   15476  10520   6660 R  71.6   0.1   0:24.13 python3
```

Two specimens, each alone on top, TIME+
accumulating about three-quarters of a
second per second on this metered
sandbox. Later, with one spinner killed
and the other alone on the machine, the
same column read **99.0** — effectively
a whole core. Which brings up the
arithmetic that confuses every top
reader once:

**100% in top means one full core.** The
default (Irix) mode counts per core, so
a single-threaded process maxes at 100,
a busy multithreaded one can pass it —
up to cores × 100 (200 on this machine,
which is also the %Cpu(s) line's whole
budget). The spinner at 99% is not "the
machine at 99%"; it is *one of two
cores* spoken for, and the %Cpu(s)
line's `id` said so in the same breath:
44.7% idle. (Pressing `I` interactively
switches to Solaris mode, which divides
by the core count and makes 100% mean
the whole machine; the two modes cause
more cross-talk between colleagues than
any other top setting. Batch captures in
this guide are all Irix, the default.)

Sorting in batch is a flag, not a
keystroke: `top -b -o %MEM` re-sorts by
memory, and its second screen put the
known quantities in their known order —
a supervisor daemon and then the eater,
RES 211,664 KB, at the top. Interactively,
the keys `P` (CPU) and `M` (memory)
re-sort in place, `x` highlights the
sort column, and `1` splits the %Cpu(s)
line into one line per core — worth
pressing once on your own machine to see
your two (or sixty-four) cores as
separate citizens. Those keystrokes are
described here rather than captured;
batch mode has no keys to press, and
this guide doesn't dress descriptions up
as captures.

## wa: the I/O tell, on camera

The single most useful diagnostic in
the header is the one that answers
"CPU-bound or disk-bound" without
guessing. The build machine staged the
answer: six small writers, each writing
to disk *synchronously* — every write
waited out by the kernel before the
next could start — put six threads in
state D:

```
$ ps -eo pid,stat,wchan:24,args | grep io_waiters
   9927 Ds   wait_log_commit          python3 io_waiters.py
   9928 Ds   folio_wait_bit_common    python3 io_waiters.py
   9929 Ds   wait_log_commit          python3 io_waiters.py
```

(`wchan` names the kernel function each
is asleep inside — shown because ps can;
reading those names is beyond this
guide's scope, but their sameness is
the story.) And top, at the same
moment:

```
%Cpu(s): 53.0 us,  4.8 sy,  0.0 ni,  0.0 id, 41.1 wa,  0.0 hi,  1.0 si,  0.2 st
```

Read it as a sentence: no idle CPU at
all (`id` 0.0), only about half the
machine doing program work (`us` 53),
and **41.1% of all CPU capacity standing
idle with its hands in its pockets
waiting for the disk** (`wa`). Those
waiting threads still count in the load
average (chapter 2's definition, kept),
which is why this machine's load can
say "busy" while its cores say
"waiting." When the verdict matters:
high `us` is a CPU story; high `wa` with
resident D states is an I/O story; the
remedies share almost nothing.
