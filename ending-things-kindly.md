# Ending Things Kindly

Watching ends, sooner or later, in a
decision: that process has to stop.
Linux gives you a vocabulary for asking,
in escalating order of insistence, and
the order matters — because the polite
request and the rude one do different
things to the process's work, its files,
and its children.

## The signals, in the order you'll use them

A **signal** is a one-word message the
kernel delivers to a process. Programs
can catch most of them, tidy up, and
exit on their own terms. The working
set:

- **TERM (15)** — "please exit." The
  default of `kill`, catchable, and the
  one to reach for first: a well-written
  program finishes its current write,
  closes its files, removes its locks,
  and dies cleanly. Give it a moment to
  work.
- **INT (2)** — the signal `Ctrl-C`
  sends. Same spirit as TERM, addressed
  to foreground terminal work.
- **HUP (1)** — "the terminal hung up."
  Historically fatal; many daemons read
  it instead as "reload your config," a
  second career the name doesn't hint at.
- **KILL (9)** — not a message but an
  execution: uncatchable, unignorable,
  delivered by the kernel itself. The
  process gets no chance to tidy — files
  can be left mid-write, locks unremoved,
  children unreaped-by-it. That is
  sometimes exactly what's needed, and
  it's why KILL is the *last* resort,
  not the spelling of seriousness.
- **STOP / CONT** — freeze and resume,
  without killing: state T from chapter
  3. The pause button almost nobody
  knows they have.

## The lab, asked politely and then not

The ordinary case first — a spinner,
sent TERM:

```
$ kill -TERM 9428   # an ordinary spinner takes the hint
$ ps -o pid,stat,args -p 9428
    PID STAT COMMAND
(no such process — gone)
```

(`kill` with no signal named sends TERM;
`ps` finding nothing prints its header
and the shell of this capture added the
verdict in parentheses.) The spinner had
no cleanup to do and did none; it
simply stopped being.

The stubborn specimen exists for the
other case. It catches SIGTERM and
ignores it — as a stuck or badly-written
program does — so:

```
$ kill -TERM 9470   # the stubborn specimen, which ignores TERM
$ ps -o pid,stat,args -p 9470
    PID STAT COMMAND
   9470 Ss   python3 lab-stubborn.py 900

$ kill -KILL 9470
$ ps -o pid,stat,args -p 9470
    PID STAT COMMAND
(no such process — gone)
```

Still there after TERM, gone after
KILL, both verdicts captured from ps,
not assumed. That pair of outputs is
the whole protocol: ask, **verify**,
then insist. The verification step is
the part people skip — `kill` reports
that a signal was *sent*, never that it
*worked* — and the skip is how processes
believed dead are found running next
week.

## Killing by name: pkill, and aiming it

`kill` wants a PID. `pkill` wants the
pattern from chapter 3: `pkill -f
lab-spinner` signals every process whose
command line matches. The `-f` is the
same widened match pgrep uses — and
chapter 3's caution, that it matches
*any* line merely containing the text,
turned from warning into accident
during this guide's own build, captured
in the harness's transcript:

```
$ pgrep -af lab-spinner
10146 /bin/bash --norc ... lab-spinner ... (harness shell, trimmed)
10154 /bin/bash --norc ... lab-spinner ... (harness shell, trimmed)
10156 python3 lab-spinner.py 300
$ pkill -f lab-spinner
```

The transcript ends there. `pgrep` had
listed *three* matches — the spinner,
and the two shells whose own command
lines contained the pattern because they
were running the capture — and `pkill`
signalled all three. The shell running
the capture died of the pattern it was
carrying; a later census confirmed the
spinner died too, but the lesson is the
order of those deaths. `pkill` is only
as aimed as its match, and its match is
a regular expression searched against
every command line on the machine,
including the ones belonging to the
person aiming it.

The disciplines that follow, all cheap:

- **pgrep first, read the list.** If the
  list contains anything you didn't
  mean — a shell, an editor with the
  name in a filename, a colleague's
  job — narrow the pattern before
  signalling it.
- **Anchor and specify.** Longer, more
  exact patterns (`lab-spinner.py`
  rather than `spin`) match fewer
  bystanders.
- **killall is blunter still.** It
  matches process *names* — and every
  specimen in this lab has the same
  name, `python3`. `killall python3`
  would have ended all six specimens
  and every other Python on the machine
  in one word. Name-based killing is
  for names that are unique.

## renice: the lever that isn't an ending

Sometimes the process is legitimate and
merely rude — a backup, a build, a batch
job that can have the machine's spare
cycles but not its front seat. **Nice
values** run from −20 (most favoured) to
19 (most deferential); ordinary users
can raise a process's nice value (lower
its priority) but not lower it back —
that takes root — which makes renicing a
one-way kindness the system lets anyone
perform:

```
$ renice -n 10 -p 9428
9428 (process ID) old priority 0, new priority 10

$ ps -o pid,ni,pri,stat,args -p 9428
    PID  NI PRI STAT COMMAND
   9428  10   9 RNs  python3 lab-spinner.py 900
```

The spinner kept spinning — renice is
not a punishment and not a pause — but
its STAT gained the `N` modifier and,
had anything else wanted the core, it
would have yielded first. On a loaded
machine, renicing the batch job is
often the whole fix for "the machine
feels slow," no ending required.

## When killing is the wrong fix

- **The process is in state D.** Signals
  — KILL included — are delivered when
  the process next surfaces from its
  uninterruptible wait, which is to say
  when the I/O finishes or the disk
  confesses. A D-state process that
  "won't die" isn't ignoring you; it
  literally hasn't heard you yet. Fix
  the I/O, or wait it out.
- **It's a zombie.** Already dead
  (chapter 4). Nothing to kill; the
  parent is the address for complaints.
- **A service manager owns it.** Kill a
  supervised service and its manager
  restarts it — correctly, by its
  lights — and you've changed nothing
  but the PID. Stop the *service*; which
  manager owns it is the systemd
  sibling's subject.
- **It's a parent.** Killing the family
  specimen orphans the sleeper and the
  churner into PID 1's care — alive,
  adopted, and now harder to attribute.
  End households child-first, or on
  purpose, knowing the adoption rule
  from chapter 4.
