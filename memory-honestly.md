# Memory, Honestly

Memory is where watching goes wrong most
often, because the scariest number on
the screen is usually the least
important one. The build machine, lab
running, eater holding its known 200 MB:

```
$ free -h   (memory eater holding 200 MB)
               total        used        free      shared  buff/cache   available
Mem:           7.7Gi       7.4Gi       190Mi       116Mi       557Mi       383Mi
Swap:             0B          0B          0B

$ grep -E "MemTotal|MemFree|MemAvailable|Buffers|^Cached|SwapTotal|SwapFree" /proc/meminfo
MemTotal:        8125588 kB
MemFree:          195116 kB
MemAvailable:     392756 kB
Buffers:               8 kB
Cached:           504344 kB
SwapTotal:             0 kB
SwapFree:              0 kB
```

(`free` reads `/proc/meminfo`; the second
command is the same facts at the source,
in kilobytes, where `free -h`'s rounded
gigabytes come from.)

## The columns, in order of honesty

- **total** — the RAM there is. Fixed by
  hardware (and on this virtual machine,
  by the sandbox's grant).
- **free** — RAM doing *nothing at all*:
  190 MiB here, and the number that
  panics people. It should be small. RAM
  sitting empty is RAM wasted, and the
  kernel knows it, so the kernel spends
  spare RAM on cache (below) and gives
  it back the instant a program asks.
  A healthy Linux machine trends toward
  *little* free memory the longer it
  runs. "Free is nearly zero" is not a
  symptom; it's a description of Linux
  working.
- **buff/cache** — RAM holding copies of
  disk data (the page cache) and
  filesystem metadata. 557 MiB here.
  This is the "Linux ate my RAM" column:
  the memory is *lent*, not taken, and
  is reclaimable on demand, in
  microseconds, without asking anyone.
- **available** — the honest headline:
  how much memory a new workload could
  get *without swapping*, counting the
  reclaimable cache. 383 MiB here. This
  is the number to watch, fear, and
  quote. `used` is only `total − free −
  buff/cache` — arithmetic, not appetite.

Against the known answer: before the
lab started, `available` read 607 MiB
and `free` read 265 MiB. The eater then
took its 200 MB out of the machine —
and it came out of *available* (607 →
383), not out of the page cache's hide
or anyone else's allocation. A specimen
with a stated appetite, subtracted from
exactly the column that should move:
that is what a verified reading looks
like, and it's the reading to reproduce
on your own machine before trusting
yourself to judge a stranger's.

At the process level the eater's row
agrees (chapter 3): RSS 215,336 KB —
200 MB held, plus the interpreter
holding it. When a machine is genuinely
short, `ps aux --sort=-%mem` (chapter
3) names the holders in order, and the
question stops being "why is memory
full" and becomes "should *that* process
have that much" — a question with an
owner and, usually, an answer.

## Swap: this machine has none, and that is stated on the label

The Swap line reads `0B` in both total
and free, in every capture in this
guide — the build machine was given no
swap at all, so **everything in this
section is described, not captured**,
and is labelled accordingly.

Swap is disk space the kernel can move
idle memory pages into when RAM is
wanted for better things. Used gently,
it's a pressure valve: cold pages sit
on disk, hot pages stay resident, and
nobody notices. Used desperately —
pages being swapped *in* constantly
because the working set doesn't fit —
the machine **thrashes**: the disk
becomes the bottleneck for memory
itself, load climbs (the waiting counts,
chapter 2), `wa` climbs (chapter 5), and
everything slows to the disk's pace.
The watching signature is not "swap
used is high" — a machine can park
pages in swap for weeks, harmlessly —
but *movement*: swap-in and swap-out
rates that won't settle. `vmstat`'s
`si`/`so` columns are the classic gauge
(procps again); a quiet machine shows
zeros there even with swap occupied.

## The OOM killer: the last resort, named

When RAM *and* swap are exhausted and a
program still asks for memory, the
kernel doesn't return an error and hope.
It chooses a process and kills it —
the **OOM killer** — scoring every
process for badness (mostly appetite,
adjusted by settings) and ending the
worst, instantly, with SIGKILL, so the
machine survives. It is not a bug or a
crash; it is triage, and it leaves a
record: the kernel log notes the event,
the victim, and the memory census that
condemned it.

Here the honesty ledger bites in the
other direction: on the build machine
the record exists in principle but the
sandbox won't show it —

```
$ dmesg | tail -n 2
dmesg: read kernel buffer failed: Operation not permitted
```

— so the OOM killer is **described in
this guide, not captured**, and the lab
was deliberately capped (the eater's
300 MB hard limit) so it could never
summon one for a demonstration. On
your machine, `dmesg | grep -i "out of
memory"` — or the system journal, the
systemd sibling's territory — is where
its visits are written, and "killed
process" lines there are the first
place to look when a service has
*vanished* rather than crashed. Absent
that record, a missing process died of
something else, and chapter 11 has the
other suspects.
