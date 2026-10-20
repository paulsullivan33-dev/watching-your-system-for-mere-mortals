# Watching Over Time

Every tool so far answers *now*. The
next question is always *since when* —
and a machine that spikes at 3 a.m.
won't repeat the performance while you
watch it at noon. Watching over time is
two habits: a screen that refreshes a
single fact, and snapshots saved to a
file so the past can be interrogated
later with the text tools.

## watch: one fact, refreshed

`watch` runs a command every two
seconds (or `-n` seconds of your
choosing) and shows the newest output
full-screen, with a header naming the
command and the time:

```
Every 1.0s: cat /proc/loadavg

1.25 1.61 1.09 3/419 9854
```

(rendered from a terminal capture of
`watch -n 1 'cat /proc/loadavg'`, the
header's right-hand side — this
machine's name and the date — trimmed).
That's chapter 2's load file, breathing:
the three averages, then the runnable
count `3/419`, updating once a second.
Point `watch` at any command from this
guide whose answer you'd rather see
move than freeze — a `ps -o` for one
suspect, `free -h`, `df -h` on a filling
disk. `watch -d` highlights what changed
between refreshes, which turns a wall of
numbers into a single flickering field.
It is a live screen, so its capture here
is a rendered frame of it; the mechanism
is simple enough that the description
and the frame together are the whole
truth.

## Snapshots: top as a recording instrument

For the past, save it. Batch mode
(chapter 5) turns top into a witness
that writes things down:

```
$ for i in 1 2 3; do top -b -n 1 | head -n 3 | tail -n 1; sleep 5; done
%Cpu(s): 52.6 us,  0.0 sy,  0.0 ni, 47.4 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
%Cpu(s): 47.6 us,  4.8 sy,  0.0 ni, 47.6 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
%Cpu(s): 47.6 us,  4.8 sy,  0.0 ni, 47.6 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
```

This loop kept only the %Cpu(s) line of
each snapshot — the machine's vital sign
at five-second intervals — and the known
answer shows through: with exactly one
lab spinner alive on a 2-core machine,
user time hovers at half (52.6, 47.6,
47.6) and idle matches it. One core
busy, one core free, three times in a
row: a rhythm, not an event. Left
running with output appended to a file,
the same loop is a poor mortal's
monitoring system — honest about its
limits (it samples; the churner's
grandchildren live and die between
samples, chapter 4) and genuinely
sufficient for "when did it start" and
"is it still happening."

Two working rules for snapshot files:
**append, don't overwrite** (`>>`), and
**stamp the time** — a snapshot without
a timestamp is a riddle. `date` in the
loop, or top's own first line, both
serve.

## Asking the file questions

A saved series is text, and text is the
sibling guide *Text Processing for Mere
Mortals'* home ground; this chapter
borrows two of its moves and points at
the rest. The %Cpu(s) lines above, kept
in a file, surrender their `us` column
to awk:

```
$ awk "/%Cpu/ {print \$2}" snapshots.txt
52.6
47.6
47.6
```

(run against the capture file from the
loop above; the values are its second
field, the user-time percent, in order).
From there the questions compound the
way they do in that guide: `grep` the
snapshots for the hour you suspect,
`awk` for the maximum `wa` anyone
recorded, `sort` the suspects' TIME+
columns across an hour of process
snapshots and watch the climber reveal
itself. The pattern matters more than
the particulars: **capture in a form
your future self can grep.** Plain text,
one fact per line where you can manage
it, timestamps attached — the same
discipline chapter 9 of the nmap guide
asked of scan output, for the same
reason. Your 3 a.m. self, reading the
file at noon, is a stranger; write for
them.
