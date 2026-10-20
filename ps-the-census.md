# ps: The Census

`ps aux` is the command this whole guide
hangs on: every process, every user,
with the columns a watcher reaches for
first. Run against the lab machine, its
head looks like this:

```
$ ps aux | head -n 7
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.1  0.0  21524  5560 ?        Ss   10:51   0:02 /usr/lib/systemd/systemd
root          17  0.0  0.0  34032  3272 ?        Ss   10:51   0:00 /usr/lib/systemd/systemd-journald
root         9435 81.3  0.0  15476  6932 ?        Rs   11:08   1:34 python3 lab-spinner.py 900
root        9442  0.0  0.0  15476  6764 ?        Ss   11:08   0:00 python3 lab-sleeper.py 900
```

(the sandbox's own supervisor rows sat
between PID 17 and the lab rows and are
cropped here; nothing else is altered).
Column by column, the ones that earn
their keep:

- **USER** — whose process it is. The
  first triage question for any stranger:
  yours, a service account's, or root's.
- **PID** — the process ID, its name for
  all practical purposes. Chapters 4 and
  9 spend it freely.
- **%CPU** — CPU used *averaged over the
  process's whole life so far*. Read that
  again: lifetime, not current. A spinner
  that has burned a core since it started
  shows a high honest number (81.3 above,
  still climbing toward its steady rate
  as the idle first instants dilute); a
  process that sprinted an hour ago and
  has slept since keeps a fading souvenir
  of the sprint. For *current* appetite,
  top's interval numbers (chapter 5) are
  the truth; ps's %CPU is the biography.
- **%MEM** — the process's share of
  physical memory, by RSS (below).
- **VSZ** — virtual size: how much
  address space the process has
  *reserved*. This is the column that
  lies by telling a useless truth.
  Reserving is cheap and programs reserve
  grandly — one daemon on the build
  machine shows a VSZ of 1,267,260 KB
  (over a gigabyte) while actually
  residing in about 212 MB. **Never
  judge a process's memory by VSZ.**
- **RSS** — resident set size: how much
  physical RAM the process's pages
  actually occupy right now. This is the
  memory column. The lab's eater, which
  allocated a known 200 MB and touched
  every page, reads RSS 215,336 KB —
  its 200 MB plus the Python interpreter
  carrying it. Prediction, meet capture.
- **TTY** — the terminal that owns it, or
  `?` for processes with none: daemons,
  services, and everything the lab
  started detached.
- **STAT** — the state, one letter and
  its modifiers. The next section.
- **START / TIME** — when it started, and
  total CPU time consumed (not wall
  time). TIME is the spinner's confession
  in a single column: 1:34 of CPU in
  under two minutes of life.
- **COMMAND** — what it is, with
  arguments. Bracketed names like
  `[kworker]` are kernel threads, which
  have no program file to name.

## The states: one letter, told straight

The first letter of STAT is the
process's condition *at this instant*:

- **R — running (or runnable).** On a
  core, or queueing for one. The
  spinners live here (`Rs` in the table
  above — R, and `s` for session leader).
- **S — sleeping, interruptibly.**
  Waiting for an event: a timer, input,
  a network packet. Nearly everything
  healthy is here nearly all the time.
  The sleeper's whole biography is S.
- **D — uninterruptible sleep.** Waiting
  on the kernel in a way that can't be
  interrupted, practically always I/O.
  Brief D is normal; *resident* D is a
  disk (or a network filesystem)
  confession. Chapter 5 manufactures six
  of them and shows the machine's `wa`
  number jump to meet them.
- **Z — zombie.** Dead, but its parent
  hasn't collected the exit notice yet.
  Chapter 4 tells this one's story.
- **T — stopped.** Suspended by a signal
  or a debugger; `Ctrl-Z` at a shell puts
  your foreground job here.

Modifiers trail the letter: `s` session
leader, `l` multithreaded, `N` niced
(lower priority — chapter 8 earns this
one), `+` in the foreground of its
terminal. Read `RNs` in chapter 8's
capture as: running, niced, session
leader — a whole sentence in three
letters once the alphabet is yours.

## Sorting by appetite

The census is alphabetical by nothing
useful; sort it by what you fear:

```
$ ps aux --sort=-%cpu | head -n 10
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root        9435 71.9  0.1  15476 10520 ?        Rs   11:08   0:13 python3 lab-spinner.py 900
root        9428 70.3  0.1  15476 10464 ?        Rs   11:08   0:13 python3 lab-spinner.py 900
```

```
$ ps aux --sort=-%mem | head -n 8
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root        9449  0.8  2.6 220240 215336 ?       Ss   11:08   0:00 python3 lab-memory-eater.py 200 900
```

`--sort=-%cpu` puts the spinners on top,
`--sort=-%mem` puts the eater on top,
each by the lifetime measures ps keeps.
(Rows between and below are cropped;
the lab specimens were the leaders of
their sorts by design — that is what a
lab is for. On your machine the leader
will be a stranger, and now you know its
name, owner, age, and biography.)

## Asking for exactly your columns

When the standard set isn't the set you
need, `-o` names your own. One command,
two specimens, every field deliberate:

```
$ ps -o pid,ppid,stat,ni,%cpu,%mem,rss,vsz,etime,args -p 9428
    PID    PPID STAT  NI %CPU %MEM   RSS    VSZ     ELAPSED COMMAND
   9428       1 Rs     0 70.1  0.1 10464  15476       00:18 python3 lab-spinner.py 900

$ ps -o pid,stat,rss,vsz,args -p 9449
    PID STAT   RSS    VSZ COMMAND
   9449 Ss   215336 220240 python3 lab-memory-eater.py 200 900
```

New columns in this capture: **PPID**,
the parent's PID (chapter 4's whole
subject — note the spinner's parent is
PID 1, which is a story in itself), and
**ELAPSED**, wall-clock age. The field
list is yours to compose: `pid,ppid,
user,stat,ni,pri,%cpu,%mem,rss,vsz,
etime,args` covers nearly every question
in this book.

## Finding one process by name

Knowing a name and needing a PID is
half of all watching, and grep-shaped
habits make it fragile (`ps aux | grep`
matches your own grep). The procps
family ships the proper tool:

```
$ pgrep -af lab-
9428 python3 lab-spinner.py 900
9435 python3 lab-spinner.py 900
9442 python3 lab-sleeper.py 900
9449 python3 lab-memory-eater.py 200 900
9456 python3 lab-family.py 900
9463 python3 lab-zombie-parent.py 900
9470 python3 lab-stubborn.py 900
```

`pgrep` matches process *names*; `-f`
widens the match to the full command
line (which is how it finds script names,
since every specimen's name is just
`python3` to the kernel), and `-a` prints
the line beside the PID. `pidof` is the
plainer cousin — PIDs of an exact program
name, nothing else. Two cautions, both
earned in chapter 8: `-f` matches *any*
command line containing the text,
including shells and scripts that merely
mention it; and a pattern is a regular
expression, so names with dots in them
match more than themselves. Look with
`pgrep` first, always. Killing by the
list you just verified is chapter 8;
killing by pattern blindfold is how the
accident in chapter 8 happened.
