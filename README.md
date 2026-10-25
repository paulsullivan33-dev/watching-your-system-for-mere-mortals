# Watching Your System for Mere Mortals

A Linux machine under strain announces
itself the way a house does: a fan that
won't quit, a command that takes a breath
before it answers, a web page a second
slower than yesterday. Feelings like that
are real evidence, but they are not a
diagnosis. This guide is about the three
small tools that turn "the machine feels
slow" into an answer with a process name
on it: **ps**, which takes a census of
everything running; **top**, which shows
the same census live, sorted by appetite;
and **htop**, the friendlier face on the
same numbers. Between them they answer
the questions every mortal with a server
asks sooner or later: what is eating the
CPU, what is eating the memory, and what
is even running here?

Almost everything happens in a small lab
built for the purpose: specimen processes
in `examples/` whose behaviour you know
*before* you look — a spinner that burns
one core doing nothing, a memory eater
that holds a stated 200 megabytes, a
sleeper, a little family with children of
its own, a zombie, and a stubborn process
that ignores polite requests to die.
Watching tools pointed at strangers teach
you to read other people's mysteries.
Pointed at specimens, they teach you to
read — every number in these chapters has
an answer you can predict, and the text
says what the answer should be before it
shows you the capture.

A note on how this guide was verified.
The build machine ran Ubuntu 24.04 as
root, with two cores and 7.7 GiB of
memory and no swap. ps, top, and free are
**procps-ng 4.0.4**; pstree is PSmisc
23.7. **htop 3.3.0** was not installed
when the build began and was added fresh
(`apt-get install htop`) so its version
could be recorded and its screens
captured. Every quoted output is a real
capture from that machine with the lab
running — the load averages, the zombie,
the signal that was refused, even the
`pkill` that shot the capture harness
itself, which chapter 9 keeps as the
lesson it is. Two things could not be
produced on this machine and are labelled
where they stand: the sandbox refuses to
read the kernel log, so the OOM killer's
visits are described rather than shown;
and with no swap configured, swap
behaviour is described, not captured.
The build machine is also a shared one —
other tenants' work comes and goes in
several captures, and the chapters point
at it when it matters, because your
machines will have neighbours too.
`criteria.md` keeps the full ledger.

## What this guide covers

- [**What watching is**](what-watching-is.md) —
  feelings versus diagnoses, the three
  tools and their three tempers, checking
  your versions, and the lab
- [**Load average first**](load-average-first.md) —
  the three most misread numbers in
  Linux, what they count, and the only
  honest way to read them — against your
  core count
- [**ps: the census**](ps-the-census.md) —
  `ps aux` column by column, the states,
  sorting by appetite, asking for exactly
  the columns you want, and finding one
  process by name
- [**Families**](families.md) — parents,
  children, trees, orphans, and who adopts
  them; the short-lived process you cannot
  catch by looking twice
- [**top: the live screen**](top-live.md) —
  the header decoded line by line, the
  CPU fields including `wa` the I/O tell,
  batch mode as the capturable truth, and
  the 100%-is-one-core arithmetic
- [**htop: the friendlier face**](htop.md) —
  meters and what their segments mean,
  tree view, search and filter, and where
  its settings live
- [**Memory, honestly**](memory-honestly.md) —
  `free -h`, why "free" is the wrong
  number to fear, page cache as a feature,
  swap, and the OOM killer named
- [**Ending things kindly**](ending-things-kindly.md) —
  signals in order of politeness, TERM
  before KILL and why, killing by name and
  aiming it, and `renice` as the gentler
  lever
- [**Watching over time**](watching-over-time.md) —
  `watch`, snapshots to a file, and asking
  "when did it spike" with the
  text-processing trio's help
- [**Recipes**](recipes.md) — the CPU
  eater now, the memory hog, CPU-bound or
  I/O-bound, one service's whole family,
  and whether the machine is actually
  overloaded
- [**Troubleshooting**](troubleshooting.md) —
  load high but CPU idle, the zombie you
  cannot kill, the 100% that is fine, the
  process that vanished, and swap thrash
- [**Glossary**](glossary.md) — the terms,
  collected in one place

## What it doesn't cover

Systemd's own watching — `systemctl
status` trees, `journalctl`, cgroup
accounting — which the sibling guide
*systemd for Mere Mortals* owns; this
guide watches processes, and names the
border where it stops. Performance
archaeology (`perf`, tracers, eBPF)
belongs to another shelf entirely.
Monitoring *systems* — Prometheus,
Grafana, alerting — are covered by their
own sibling guide; nothing here phones
home or keeps history beyond what you
deliberately save to a file. And other
platforms: macOS and the BSDs ship a
`ps` and a `top` with different flags
and different columns, and Windows is a
different world — where a difference
bites, the chapters say so once, plainly.

## How to use this guide

Read chapter 1, start the lab
(`sh examples/start-lab.sh`), and keep a
terminal open from chapter 2 on — every
tool in the guide gets pointed at the
specimens first, so you can check its
report against what you know is true.
Stop the lab with
`sh examples/stop-lab.sh` when you're
done; the specimens also retire on their
own after ten minutes. Keep the lab
afterwards: a spinner whose appetite you
know exactly is a standing rehearsal for
the day a stranger's process has one you
don't.

---

## Part of the series

This guide is one of the [For Mere Mortals](https://paulsullivan33-dev.github.io/mere-mortals/) guides: plain-language guides to the tools programmers and makers use.

Related guides:

- [lsof for Mere Mortals](https://paulsullivan33-dev.github.io/lsof-for-mere-mortals/)
- [systemd for Mere Mortals](https://paulsullivan33-dev.github.io/systemd-for-mere-mortals/)
- [Prometheus and Grafana for Mere Mortals](https://paulsullivan33-dev.github.io/prometheus-and-grafana-for-mere-mortals/)

## License

The writing in this guide is licensed under [CC BY 4.0](https://github.com/paulsullivan33-dev/watching-your-system-for-mere-mortals/blob/main/LICENSE). Code examples and lab scripts are licensed under the [MIT License](https://github.com/paulsullivan33-dev/watching-your-system-for-mere-mortals/blob/main/LICENSE-CODE).
