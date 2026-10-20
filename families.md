# Families: Who Started Whom

No process on a Linux machine is an
orphan by accident of birth: every one
was started by another process, its
**parent**, and carries the parent's PID
in its **PPID** column forever. The
family structure answers questions the
flat census can't: if I kill this, what
else dies? Where did that come from?
And why is that dead thing still in the
table?

The lab's family is small and known:
`lab-family.py` starts a sleeper and a
churner, and the churner starts a
one-second `sleep` over and over. Drawn
as a tree:

```
$ pstree -p 9456
python3(9456)-+-python3(9476)
              `-python3(9477)---sleep(9513)
```

`pstree` shows the household hanging
from the parent's PID (9456): child
9476 the sleeper, child 9477 the
churner, and — at the moment of the
capture — grandchild 9513, a `sleep 1`
with most of its second already spent.
The same family through ps's own lens:

```
$ ps --forest -o pid,ppid,stat,args -g 9456
    PID    PPID STAT COMMAND
   9456       1 Ss   python3 lab-family.py 900
   9476    9456 S     \_ /usr/bin/python3 .../lab-sleeper.py 900
   9477    9456 S     \_ /usr/bin/python3 .../lab-churner.py 900
   9513    9477 S         \_ sleep 1
```

(the long paths are trimmed where the
tree indents; the `\_` branches are
ps's own drawing). Everything the census
knows is here — PID, PPID, state — and
the tree is just those PPIDs, followed
to their conclusions.

## The grandchild who won't sit still

Look for the churner's child twice:

```
$ pstree -p 9456        (a minute later)
python3(9456)-+-python3(9476)
              `-python3(9477)---sleep(10143)

$ pstree -p 9456        (three seconds after that)
python3(9456)-+-python3(9476)
              `-python3(9477)
```

Same family, three portraits: the
grandchild's PID changed (9513 →
10143), then a snapshot caught the gap
between one `sleep` ending and the next
starting, and the branch was bare.
Short-lived processes are the blind spot
of every snapshot tool in this guide: a
process that lives for a second can do
its work — good or ill — entirely
between two of your looks. Chapter 11
returns to this as a troubleshooting
symptom. The honest mitigations are
faster looks (`top` refreshes; `watch`
polls) and the knowledge that the
*parent* — the churner, long-lived and
catchable — is where responsibility
lives. Investigate parents; children are
weather.

## Orphans and the universal adopter

Look again at the family's own PPID in
the forest capture: **1**. The lab's
parent was started by a shell, the shell
exited, and the family didn't die with
it — because when a parent dies first,
its children are **adopted by PID 1**
(on modern systems, the init system —
systemd here; in containers, whatever
process holds PID 1 in the namespace).
Adoption is not a courtesy; it's the
rule that keeps the tree connected and
ensures every process always has a
parent responsible for collecting it
when it dies. Every detached daemon and
double-forked service on your machine
arrived at PPID 1 by exactly this road.

The practical consequences are two.
First, a PPID of 1 tells you the starter
is gone — the trail of "who launched
this" ends at a shell history, a service
manager, or a cron line, not at a
living parent. (Which manager owns which
services is the systemd sibling guide's
territory; this guide watches the
processes themselves.) Second, adoption
is the backstop in the zombie story,
next.

## The zombie, collected at last

The lab's zombie parent forks a child
that exits immediately, then waits
without collecting it. The census shows
the result:

```
$ ps -eo pid,ppid,stat,args | grep defunct
   9475    9463 Z    [python3] <defunct>
```

A **zombie** is a process that has
finished — exited, released its memory,
its files, everything — except its exit
notice, which sits in the process table
until the parent calls `wait()` and
reads it. What remains is a table entry
and a line in ps: no CPU, no RAM worth
naming, just the name in brackets and
`<defunct>` where its command line used
to be. Zombies are not a leak and not a
haunting; they are uncollected mail.
One or two, from a parent written
carelessly, are untidy. Thousands mean
a parent is stuck and not reaping — and
the fix is never aimed at the zombies,
who are already dead and cannot be
killed (chapter 11). The parent must
reap, or die and let PID 1 adopt the
zombies and reap them itself — which is
exactly what the lab specimen does in
reverse: it collects its child on the
way out and leaves no zombie behind.

On the build machine, at the moment of
capture, the whole population of the
undead was:

```
$ ps -eo stat | grep -c ^Z
1
```

One zombie, ours, accounted for. When
your machine's count surprises you,
`ps` sorted by state will name the
parent in the PPID column — and the
parent is the process to fix, restart,
or forgive.
