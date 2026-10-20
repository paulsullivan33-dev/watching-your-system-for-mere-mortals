# What Watching Is

"The machine feels slow" is where every
investigation starts and where too many
end — with a reboot, a shrug, or a bigger
server bought on a feeling. The feeling
is real. Something *is* different. But a
feeling doesn't say whether the machine
is short of CPU, short of memory, waiting
on a disk, or perfectly healthy and
merely sharing itself with a neighbour.
Those four conditions feel identical from
the outside and have nothing in common as
fixes. Watching is the discipline of
replacing the feeling with a measurement
before reaching for a remedy.

Three questions cover most of mortal
system-watching:

1. **What is eating the CPU?** Some
   process is doing arithmetic as fast as
   it can, and everything else queues
   behind it.
2. **What is eating the memory?** Some
   process is holding RAM, and the kernel
   is making room for it — gracefully, up
   to a point.
3. **What is even running here?** The
   census question, and the embarrassing
   one: half of "the machine is slow" is
   a process nobody remembers starting.

## The three tools, and their tempers

**ps** is a census: a still photograph
of every process at the instant you ask,
with columns of facts about each. It
answers and exits. Everything you learn
from ps is exactly true and exactly one
moment old.

**top** is the same census as a live
feed: it re-asks every few seconds,
sorts by appetite, and stays on screen
until dismissed. Its header summarises
the whole machine — how busy, how full,
how queued — above the hungriest
processes. What ps freezes, top animates.

**htop** is top's friendlier relative:
the same underlying numbers (both read
the kernel's `/proc` filesystem), drawn
as coloured meters, navigable with arrow
keys, searchable, and honest about
process family trees by default. Nothing
htop shows is secret from ps and top; it
is arranged so a human notices it faster.

Underneath all three, and underneath this
whole guide, is one fact worth keeping:
these tools *read* the system, they don't
ask its permission or change its state.
You can run them as an ordinary user, as
often as you like, against a machine in
distress. Watching is the safest verb in
this book.

## Checking your versions

The build machine's set, captured before
anything else was:

```
$ ps --version
ps from procps-ng 4.0.4
$ top --version
top from procps-ng 4.0.4
$ pstree --version
pstree (PSmisc) 23.7
$ nproc
2
```

ps, top, free, and watch are all one
family — procps-ng — so they agree about
definitions, which is why this guide can
move between them without re-teaching
terms. htop is a separate project; the
build machine didn't have it at first,
and installing it was one command
(`apt-get install htop` on Debian and
Ubuntu; your package manager's spelling
elsewhere). Its version is recorded in
chapter 6, where it belongs.

The `nproc` answer — **2** — matters more
than any version number in this guide.
Two cores is the size of this machine,
and every load average and percentage in
the chapters is read against it. Run it
on your machine and remember your number;
chapter 2 explains why it's the key to
the most misread numbers in Linux.

## The lab

Six specimens live in `examples/`, each
with behaviour stated in advance:

- **lab-spinner.py** — burns one CPU core
  in a busy loop, doing arithmetic nobody
  wants. The known answer to "what is
  eating the CPU."
- **lab-memory-eater.py** — allocates a
  stated number of megabytes (200 in the
  guide's runs), touches every page so
  the memory is genuinely resident, and
  holds it. Hard-capped at 300 MB inside
  the script itself: the lab must never
  be able to push its own machine into
  real memory trouble.
- **lab-sleeper.py** — sleeps. No CPU,
  almost no memory: the specimen for
  "running but idle."
- **lab-family.py** — a parent with two
  children: the sleeper above, and
  **lab-churner.py**, which spawns a
  one-second `sleep` child over and over.
  The known answer to "who started whom,"
  and to "where did that process go."
- **lab-zombie-parent.py** — starts a
  child that exits immediately, then
  deliberately doesn't collect it. The
  known answer to "what is that defunct
  thing."
- **lab-stubborn.py** — ignores SIGTERM,
  the polite exit signal. The known
  answer to "why won't it die."

Start them all with
`sh examples/start-lab.sh`, stop them
with `sh examples/stop-lab.sh`; left
alone, each retires on its own after ten
minutes. `examples/lab-notes.txt`
describes each specimen, and
`examples/commands.txt` lists the guide's
commands in order.

One honesty note before the numbers
start. The build machine is a *shared*
one — a sandbox running other work
beside the lab — and its process list
includes the sandbox's own machinery,
which appears in captures under its own
names. That is not contamination; it is
the normal condition of real machines,
and the chapters point at it where it
changes a reading. Your machine's
neighbours will have different names.
The specimens are how you tell them
apart from the story.
