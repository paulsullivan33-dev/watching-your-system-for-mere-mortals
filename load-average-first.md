# Load Average First

Every watching session in this guide
starts with three numbers, because they
are the cheapest health check the machine
offers and the most reliably misread.
Here they are on the build machine,
before the lab started:

```
$ uptime
 11:08:21 up 17 min,  0 user, load average: 2.73, 1.95, 1.10

$ cat /proc/loadavg
2.73 1.95 1.10 3/405 9397
```

`uptime` prints them as a courtesy;
`/proc/loadavg` is where they live (and
where top and htop read them, which is
why all three tools always agree). The
same file carries two more fields worth
knowing: `3/405` means 3 threads were
runnable at that instant out of 405 in
existence, and `9397` is simply the
highest PID handed out so far.

## What the three numbers count

The load average is a damped average,
over the last **1, 5, and 15 minutes**,
of how many threads were *wanting to
run or running* — plus, and this is the
part that surprises everyone once, how
many were **stuck in uninterruptible
sleep**, state D, almost always waiting
on I/O. Chapter 3 gives the states their
letters; for now hold the definition
whole:

> load ≈ (threads running or queueing for
> CPU) + (threads waiting uninterruptibly,
> usually on disk)

Two consequences follow, and between
them they explain most load confusion on
earth:

- **Load is not a percentage.** It is a
  count, of queueing things. A load of
  2.73 does not mean "273% busy" or
  "2.73% busy"; it means that over the
  last minute, on average, between two
  and three threads wanted a core or
  were stuck waiting.
- **Load can be high with the CPU idle.**
  Threads in state D count fully and use
  no CPU at all. Chapter 11 opens with
  exactly that symptom; chapter 5 shows
  the build machine manufacturing it on
  purpose.

## The only honest yardstick: your core count

A count of queueing threads means
nothing until it's compared with how
many can run at once — your core count
from chapter 1. The build machine has
**2 cores**, so its readings translate
like this:

- **Load below 2:** fewer threads want
  cores than there are cores, averaged.
  Nobody is really queueing; the machine
  has headroom.
- **Load around 2:** the machine is
  fully subscribed. Work runs, but new
  work waits its turn in short lines.
- **Load persistently above 2:** a queue
  is standing. Every thread waits, on
  average, behind others — this is the
  reading that deserves investigation,
  *if it persists*. The 15-minute number
  is the one that tells you whether it
  persists; the 1-minute number is
  weather, the 15 is climate.

Translate, don't transplant: on a
64-core machine a load of 20 is a
lightly loaded box with 44 cores idle,
and on a 1-core box a load of 3 is a
traffic jam. The same three numbers,
opposite verdicts — which is why guides
that say "load should stay under X"
without asking your core count are
selling you someone else's machine.
(Huge-machine readings are described
here, not captured; the build machine
has the two honest cores it has.)

## Why the numbers trail the truth

The averages are *damped*: each is an
exponentially-decaying average, not a
count of the last 60 seconds exactly.
Start a heavy process and the 1-minute
figure climbs toward the new reality
over tens of seconds; stop it, and the
figure subsides the same way. The build
machine demonstrated the neighbour half
of that lesson while this chapter was
being captured. With one lab spinner
running — a known, steady one-core load
that this guide started itself — the
reading was:

```
$ uptime   (one spinner still running)
 11:11:43 up 20 min,  0 user, load average: 2.94, 2.00, 1.26
$ kill -TERM 9435   # the last spinner
$ uptime   (75 seconds after the spinner stopped)
 11:12:58 up 22 min,  0 user, load average: 3.66, 2.38, 1.45
```

The spinner died and the load *rose* —
because this machine is shared, and
another tenant's work arrived in the
same minute. Both halves of that are the
lesson. First, your load average is a
sum over *everything* on the machine,
including work you didn't start and
can't see the purpose of; on a shared
box, a quiet VM, or a CI runner, the
baseline is not yours to command.
Second, watch the *shape* across the
three figures, not one figure: here the
1-minute number jumps around (2.73,
2.94, 3.66 across five minutes) while
the 15-minute number moves like a tide
(1.10, 1.26, 1.45). Weather and climate.

When the lab runs alone — one spinner on
this 2-core machine — the shape to
expect is a 1-minute average climbing
toward roughly 1 plus whatever your own
baseline is, and a CPU about half busy
in top (one of two cores). Chapter 9
captures exactly that half-busy reading,
three times in a row.
