# Recipes

Five investigations, each assembled
from chapters already proven, each run
against the lab so the answer was known
before the question was asked. On your
machine the names will be strangers;
the shapes of the answers won't be.

## 1. Find the CPU eater, now

```
$ ps aux --sort=-%cpu | head -n 10
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root        9435 71.9  0.1  15476 10520 ?        Rs   11:08   0:13 python3 lab-spinner.py 900
root        9428 70.3  0.1  15476 10464 ?        Rs   11:08   0:13 python3 lab-spinner.py 900
```

Two spinners, unmistakable: R state,
TIME already at 0:13 in the first
moments, nothing else on the machine in
their league. Remember the columns'
honesty: %CPU here is the lifetime
average (chapter 3), so a suspect that
sprints in bursts may rank below a
steady plodder. Cross-check the leader
in top's interval view before ending
anything (chapter 8's protocol: ask,
verify, insist).

## 2. Find the memory hog

```
$ ps aux --sort=-%mem | head -n 8
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root        9449  0.8  2.6 220240 215336 ?       Ss   11:08   0:00 python3 lab-memory-eater.py 200 900
```

The eater, by RSS — 215,336 KB against
its stated 200 MB plus its interpreter.
Read RSS, never VSZ (chapter 3's
standing warning, and note the eater's
own two numbers are close only because
it *touched* everything it reserved;
most processes' VSZ is a fantasy next
to their RSS). Then judge the finding
against chapter 7: a hog matters when
`available` is what it's eating into.

## 3. CPU-bound or I/O-bound?

The verdict in two looks. First top's
header, during the build's staged disk
jam:

```
%Cpu(s): 53.0 us,  4.8 sy,  0.0 ni,  0.0 id, 41.1 wa,  0.0 hi,  1.0 si,  0.2 st
```

then the corroboration:

```
$ ps -eo stat | grep -c ^D
6
```

`wa` at 41.1 with six threads resident
in D is an I/O verdict beyond argument:
the cores are idle *on behalf of* the
disk. The mirror image — `us` in the
nineties, `wa` at zero, D count zero —
is a CPU verdict, and recipe 1 names
the culprit. When both are low and the
machine still feels slow, the problem
isn't this machine's processes at all;
look at the load's neighbours (chapter
2) or the network (another shelf).

## 4. One service's whole family

Pick the parent; take the tree:

```
$ pstree -p 9456
python3(9456)-+-python3(9476)
              `-python3(9477)---sleep(9513)
```

or the census with branches:

```
$ ps --forest -o pid,ppid,stat,args -g 9456
   9456       1 Ss   python3 lab-family.py 900
   9476    9456 S     \_ .../lab-sleeper.py 900
   9477    9456 S     \_ .../lab-churner.py 900
   9513    9477 S         \_ sleep 1
```

(paths trimmed in the forest's deeper
rows). Do this *before* ending anything
in the household (chapter 8): the tree
tells you what a kill would orphan,
what would be restarted by whom, and
which quiet child is actually the
service you meant to keep.

## 5. Is this machine actually overloaded?

Assemble the verdict from three
readings, all demonstrated in this
guide:

1. **Load against cores.** 2 cores here.
   Readings across the build sat between
   1.1 and 3.7 — sometimes queued,
   sometimes not, on a *shared* machine
   where part of the load was never
   ours. Persistently above the core
   count, on the 15-minute figure, is
   the overload signature; a 1-minute
   spike is weather.
2. **top's `id` and `wa`.** With both
   spinners running, the %Cpu(s) line
   read `0.0 id` — no headroom at all,
   CPU the binding constraint. With one,
   `id` sat at 44.7 — half the machine
   still free, whatever the load number
   said.
3. **Who, specifically.** Recipes 1 and
   2. A machine is not "overloaded" in
   the abstract; it is overloaded *by*
   something, and ps sorts by its name.

All three agreeing is a verdict. Any
one alone is a hunch — and hunches are
what this guide exists to retire.
