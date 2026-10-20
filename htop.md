# htop: The Friendlier Face

```
$ htop --version
htop 3.3.0
```

htop reads the same `/proc` filesystem
as ps and top and computes the same
numbers; nothing in this chapter is new
*information*. What htop adds is
arrangement: the machine's state drawn
as meters at the top, the process table
below, and keys that let you poke at
what you're seeing without leaving the
screen. Its captures here were taken by
running htop in a real terminal session
of a stated size and rendering the final
screen to text — the colours don't
survive that rendering, so colour is
described (from htop's own
documentation) where it matters, and the
numbers are quoted as captured.

## The meters

With the lab running — by then only
one spinner remained of the original
two — htop's screen
opened like this (top rows, and the
rows this section talks about; the
sandbox's own processes filled the rest
and are cropped):

```
    0[||||||||||                               17.2%] Tasks: 17, 11 thr, 0 kthr; 2 running
    1[|||||||||||||||||||||||||||||||||||||||||99.3%] Load average: 1.35 1.67 1.08
  Mem[|||||||||||||||||||||||||||||||||||7.18G/7.75G] Uptime: 00:19:10
  Swp[                                         0K/0K]

    PID USER       PRI  NI  VIRT   RES   SHR S  CPU%  MEM%   TIME+  Command
   9435 root        20   0 15476  6868  3008 R  98.3  0.1  1:06.07 python3 lab-spinner.py 900
   9449 root        20   0  215M  206M  2960 S   0.0  2.6  0:00.16 python3 lab-memory-eater.py 200 900
```

Read it against the chapters you have:

- **One meter per core.** Two cores, two
  bars — and the story of the moment is
  visible at a glance: core 1 at 99.3%
  is the spinner's home; core 0 at 17.2%
  is doing the machine's other errands.
  Compare top's single %Cpu(s) line,
  which averages them into one number
  unless you press `1`. Neither is
  truer; htop's default is harder to
  misread.
- **The segments inside a CPU bar** are
  coloured by kind of work — user,
  kernel, and low-priority (nice) time
  each get their own colour in the
  default theme, so a bar's *makeup*,
  not just its length, is readable.
- **Mem and Swp meters** summarise
  chapter 7: the memory bar's segments
  split used, buffers, and cache into
  colours (the split `free` makes you
  read columns for), here 7.18G of
  7.75G in use on this tight machine;
  swap sits at 0K of 0K because this
  machine has none.
- **The right-hand readouts** — Tasks,
  Load average, Uptime — are the same
  numbers from chapters 2 and 5, kept in
  view while you work.

And the table is top's table with the
names slightly rearranged (PRI for PR,
CPU% for %CPU — same quantities), the
spinner wearing an honest 98.3 in
htop's own interval, and the eater's
206M of RES agreeing with ps to
rounding. Three tools, one truth: that
agreement *is* the verification.

## Trees without asking

Chapter 4 built a process tree with two
commands. htop's tree view (the `t` key,
or F5) is the same drawing, live:

```
      1 root        20   0 21524  5812  2512 S   0.0  0.1  0:02.16 /usr/lib/systemd/systemd
     17 root        20   0 34032  2488  1540 S   0.0  0.0  0:00.10 ├─ /usr/lib/systemd/systemd-journald
   9435 root        20   0 15476  6868  3008 R  93.0  0.1  1:09.00 ├─ python3 lab-spinner.py 900
   9449 root        20   0 15476  6868  3008 S   0.0  2.6  0:00.16 ├─ python3 lab-memory-eater.py 200 900
```

(second capture, moments later; rows for
the sandbox's processes and the deeper
branches are cropped). The lab specimens
hang from PID 1 by `├─` branches —
adopted orphans, as chapter 4 found —
and on your machine the family specimen
would show its sleeper and churner
children nested under it the same way,
updating as the churner's own children
come and go.

## Finding and filtering, in place

Three keys cover most interactive
hunting, described here because a batch
capture has no keys to press:

- **`/` search** — type a name, land on
  the process. The interactive answer to
  pgrep.
- **`\` filter** — narrow the table to
  matching rows only: the lab's six
  specimens out of a crowded table in
  four keystrokes (`lab-`).
- **`t` / F5 tree, F6 sort** — the tree
  above, and re-sorting by the column
  you meant this time.

And the function-key bar along the
bottom (F1 help through F10 quit) is
htop's own cheat sheet, always on
screen — the mortal-friendly design
decision the whole tool is named for.

## Where its settings live

htop remembers — in a file with the most
honest header comment in this guide:

```
$ head -n 12 ~/.config/htop/htoprc
# Beware! This file is rewritten by htop when settings are changed in the interface.
# The parser is also very primitive, and not human-friendly.
htop_version=3.3.0
config_reader_min_version=3
fields=0 48 17 18 38 39 40 2 46 47 49 1
```

`~/.config/htop/htoprc` is written when
you change settings in the F2 setup
screens (described here, not captured —
setup is a conversation with menus, and
its *result* is this file). The header
tells you the working arrangement: tune
in the interface, treat the file as
htop's property, and read the `fields=`
line as what it is — the column order of
your table, in numbers htop explains in
its help. Deleting the file resets htop
to defaults; copying it carries your
setup to another machine. Settings that
live in a plain file you can inspect
beat settings that live nowhere you can
see — a preference this whole series
shares.
