# Glossary

**available (memory)** — `free`'s honest
headline: how much RAM a new workload
could get without swapping, counting
reclaimable cache. The memory number to
watch.

**batch mode** — `top -b`: screens
printed as plain text instead of drawn
for a terminal. The capturable,
saveable, greppable form of top.

**buff/cache** — RAM lent to copies of
disk data and filesystem metadata.
Reclaimable on demand; its size is a
sign of health, not hunger.

**core** — one independent CPU
processor. The yardstick every load
average must be read against
(`nproc` counts them).

**D state** — uninterruptible sleep: a
process waiting in the kernel, usually
on I/O, that cannot yet receive signals.
Counts toward load average; uses no
CPU.

**defunct** — the label ps gives a
zombie's row, where its command line
used to be.

**elapsed** — a process's wall-clock
age, as opposed to **TIME**, its total
CPU consumed.

**Irix mode** — top's default %CPU
accounting: per core, so 100% is one
full core and totals can reach
cores × 100. Solaris mode divides by
the core count instead.

**load average** — the damped 1-, 5-,
and 15-minute averages of threads
running, queueing for CPU, or waiting
in state D. A count, never a percentage.

**nice / NI** — a process's politeness
value, −20 (favoured) to 19
(deferential). Raised with `renice`;
shows as STAT's `N` modifier.

**OOM killer** — the kernel's last
resort: when memory is exhausted, it
scores processes and kills the worst
with SIGKILL so the machine survives.
Its visits are recorded in the kernel
log.

**orphan** — a process whose parent
died first. Adopted by PID 1, which
becomes responsible for collecting it.

**page cache** — the kernel's use of
spare RAM to remember disk contents.
Why `free` sits near zero on a healthy
machine.

**parent / PPID** — the process that
started a process, and its PID. Every
process carries its PPID in the census.

**pgrep / pkill** — find processes by
name or pattern / signal them by the
same match. `-f` widens the match to the
full command line — aim carefully.

**process** — a running program
instance: code, memory, open files, and
a row in the kernel's table, named by
its PID.

**R state** — running or runnable: on a
core or queueing for one.

**RSS (resident set size)** — the RAM a
process's pages actually occupy now.
The memory column to judge by — never
VSZ.

**S state** — interruptible sleep:
waiting for an event. Where nearly
every healthy process spends nearly all
its life.

**signal** — a one-word kernel message
to a process: TERM (please exit), KILL
(die now, uncatchable), INT, HUP, STOP,
CONT, and others. `kill` sends them;
sending is not the same as success —
verify.

**steal (st)** — CPU time a virtual
machine wanted and the hypervisor gave
to a neighbour. A measurable tenant tax
on rented machines.

**swap** — disk space used to hold
memory pages under pressure. Occupancy
is harmless; sustained movement in and
out (thrashing) is the disease.

**T state** — stopped: frozen by a
signal or debugger, resumable with
CONT. `Ctrl-Z` puts shell jobs here.

**VSZ (virtual size)** — address space
a process has *reserved*. Large,
cheap, and useless for judging memory
appetite.

**wa (I/O wait)** — top's %Cpu(s) field:
cores idle because the work is waiting
on I/O. The tell that separates
disk-bound from CPU-bound.

**watch** — the tool that re-runs a
command on a screen every few seconds.
One fact, kept current.

**wchan** — the kernel function a
sleeping process is asleep inside, as
ps can report it. Diagnostic depth
beyond this guide's scope.

**zombie (Z state)** — a process that
has exited whose parent hasn't yet
collected its exit notice. Holds a
table entry and nothing else; the fix
is always at the parent.
