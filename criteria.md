# Writing Criteria

Every guide in this repo is written to the same
standard. If you're adding or editing a guide —
human or AI — hold it to these.

1. **Plain words, real ideas.** Simple language,
   never dumbed-down concepts. Explain jargon on
   first use; collect terms in the glossary.
2. **No hype.** No marketing adjectives, no
   "revolutionary," no promises about what
   something will do for the reader.
3. **Honest about limits.** Say what the thing
   *can't* do. State uncertainty instead of
   smoothing it over. Validation notes include
   what remains unverified.
4. **No invented numbers.** Benchmarks, defaults,
   and specs are either measured or qualified with
   "depends on your setup." If it wasn't tested,
   say so.
5. **Checkable.** Commands are meant to be run,
   with "Check:" blocks showing what success looks
   like. Sources are linked, not asserted.
6. **Respect the reader's setup.** Call out
   Windows/Mac/Linux differences. Don't assume a
   GPU, a budget, or prior experience.
7. **Safety isn't skipped.** Real risks get
   stated plainly, not buried.
8. **Scoped.** Each guide says what it covers and
   points elsewhere for the rest. No guide
   pretends to be the whole subject.
9. **Structure over prose.** Tables, before/after
   examples, symptom → fix. Scannable beats essay.

## Verification notes for this guide

Standard 3 and 4 applied to this guide,
specifically. The build machine ran Ubuntu
24.04 as root: **2 cores, 7.7 GiB of RAM
(8,125,588 kB), and no swap at all**.
ps, top, free, and watch are **procps-ng
4.0.4**; pstree is **PSmisc 23.7**.
**htop 3.3.0** was absent when the build
began and was installed fresh for it
(`apt-get install -y htop`, after an
initial wait for the dpkg lock, held by
the sandbox's own package maintenance);
its version was recorded from the
installed binary. Every quoted output in
the chapters is a capture from that
machine with the shipped lab running.
Working transcripts are kept with the
build (`system-watch-lab/transcripts/`).

**The lab.** Six specimens in
`examples/`, each with its behaviour
stated in advance: a spinner (one busy
core), a memory eater (200 MB requested,
every page touched, hard-capped at
300 MB inside the script so the lab can
never summon the OOM killer on its own
machine), a sleeper, a churner spawning
one-second children, a family (parent +
sleeper + churner), a zombie parent
(forks a child that exits, declines to
reap it for the specimen's lifetime,
reaps on exit), and a stubborn process
that ignores SIGTERM. A seventh
throwaway program, six synchronous disk
writers, exists only in the transcripts:
it staged chapter 5's I/O wait and was
never shipped, because a guide's lab
should not include a disk jammer.

**The shared machine, stated once.** The
build sandbox runs other tenants'
work beside the lab, and its CPU is
metered. Both facts are inside the
captures and are named where they bite:
the baseline load average was 2.73
before the lab started; killing the
last spinner was followed, 75 seconds
later, by a *higher* load (3.66) as
another tenant's work arrived — that
capture is quoted in chapter 2 as the
lesson it is, not hidden. Likewise the
spinners' percentages: two spinners on
the metered box read 63–76% each in
top, and a lone spinner read 98–99%
there and 98.3 in htop. The chapters
predict ~100% for a lone spinner on an
unmetered machine as the arithmetic of
one full core, labelled as arithmetic,
not as a capture.

**Verified by running, per chapter:**

- *Ch. 1:* `ps/top/pstree --version`,
  `nproc` (2), as printed. htop's
  absence at first check and its
  install are build facts recorded
  above.
- *Ch. 2:* `uptime` and
  `/proc/loadavg` before the lab
  (2.73 1.95 1.10, running/total
  3/405); the spinner-kill sequence in
  full, including the inconvenient
  result.
- *Ch. 3:* `ps aux` head with the lab
  rows; `--sort=-%cpu` and
  `--sort=-%mem` with the specimens
  leading their sorts; the custom `-o`
  formats on the spinner (PPID 1,
  ELAPSED 00:18) and the eater (RSS
  215,336 KB against VSZ 220,240 —
  the stated 200 MB plus its
  interpreter); the supervisor daemon's
  VSZ 1,267,260 KB vs its ~212 MB RSS,
  quoted as the VSZ warning's evidence;
  `pgrep -af lab-` naming all seven
  specimens; `pidof python3`.
- *Ch. 4:* `pstree -p` and
  `ps --forest` of the family,
  including the churner's `sleep 1`
  grandchild (PID 9513); the same tree
  re-captured minutes later with the
  grandchild replaced (10143) and once
  more in the gap between children;
  the zombie row (9475, Z,
  `[python3] <defunct>`, PPID 9463);
  the machine-wide zombie count (1).
  The family's PPID of 1 — adoption
  after its starting shell exited — is
  in the forest capture, not asserted.
- *Ch. 5:* `top -b -n 2` both screens
  (first-screen spinner values 63.6,
  second-screen 76.1/71.6 — the
  since-start vs interval difference
  is the chapter's own warning, shown
  rather than claimed); the Tasks line
  (17 total, 3 running, 1 zombie);
  `top -b -o %MEM` second screen
  (eater RES 211,664 KB, spinner at
  99.0 in that interval); the staged
  I/O capture: six writers in state D
  with `wchan` shown (`wait_log_commit`,
  `folio_wait_bit_common`), and top's
  header at the same moment —
  `id` 0.0, `wa` 41.1.
- *Ch. 6:* `htop --version` (3.3.0);
  two full screens captured by running
  htop in a pseudo-terminal of a
  stated size (108×30) and rendering
  the final screen through a terminal
  emulator: the meters screen (core 1
  at 99.3%, Mem 7.18G/7.75G, Swp 0K/0K,
  spinner at CPU% 98.3, eater RES
  206M) and the tree view (specimens
  hanging from PID 1 by `├─`
  branches). Colours do not survive
  text rendering, so the colour
  meanings of the meter segments are
  described from htop's documentation
  and labelled as description; the
  setup screens, search, and filter
  are likewise described, not
  captured — a batch document has no
  keystrokes, and the chapter says so.
  The `~/.config/htop/htoprc` head,
  including its own warning comment
  and the `fields=` line, is a real
  file capture after htop wrote it.
- *Ch. 7:* `free -h` before the lab
  (available 607 MiB) and with the
  eater holding (available 383 MiB,
  free 190 MiB, buff/cache 557 MiB),
  plus the matching `/proc/meminfo`
  lines. The eater's 200 MB leaving
  `available`, specifically, is the
  chapter's checkable claim.
- *Ch. 8:* the full signal protocol on
  camera: `kill -TERM` on a spinner,
  ps verifying absence; `kill -TERM`
  on the stubborn specimen, ps
  verifying survival (still `Ss`);
  `kill -KILL`, ps verifying absence;
  `renice -n 10` (old priority 0, new
  priority 10) with the spinner's NI
  and the `N` in its STAT (`RNs`)
  confirmed by ps. The `pkill`
  accident is a real transcript: the
  capture harness's own shells matched
  `pgrep -af lab-spinner` (their
  command lines contained the pattern)
  alongside the spinner (PID 10156);
  `pkill -f lab-spinner` then
  terminated the harness shell
  mid-capture, which is why the
  quoted transcript ends at the pkill
  line. A census immediately after
  confirmed the spinner was gone too.
  The shell rows are quoted trimmed,
  with the trim marked in the chapter.
- *Ch. 9:* `watch -n 1 'cat
  /proc/loadavg'` rendered from a
  terminal capture (header's hostname
  and date trimmed, marked in the
  chapter); the three-snapshot loop
  (`us` 52.6 / 47.6 / 47.6 with one
  spinner on two cores); the awk
  extraction of the `us` column run
  against that very snapshot file.
- *Ch. 10:* every recipe is a
  re-presentation of its chapter's
  capture — no new numbers were
  produced for the recipes chapter.
- *Ch. 11:* `kill -KILL` aimed at the
  zombie (9475), which remained Z
  under the same parent — captured,
  not reasoned. The D-state symptom
  reuses ch. 5's staged capture.

**Capture hygiene (declared trims):**
rows belonging to the sandbox's own
supervisor processes are cropped from
some census quotes, and the chapters
say so where it happens; the htop
screen renders are cropped to the
meters and the rows under discussion;
the pkill transcript's harness-shell
lines are trimmed to their first words
with the trim marked; the
`ps --forest` quote trims the specimens'
long absolute paths in deeper rows.
No output was completed, corrected, or
invented: where a capture surprised the
draft (the load rising after the
spinner died; pgrep matching the
harness itself), the chapter was
rewritten to the capture.

**Documented-only (not run), and why:**

- *The OOM killer's behaviour and
  records.* The lab was capped
  specifically so it could never be
  summoned for a demonstration, and
  the sandbox refuses to show the
  kernel log at all — the refusal
  itself is captured in ch. 7
  (`dmesg: read kernel buffer failed:
  Operation not permitted`). Described
  from the kernel's documented
  behaviour; on the reader's machine
  the log is the first place to check.
- *Swap in all its behaviour.* The
  build machine has no swap (SwapTotal
  0 in every capture). Swapping,
  thrashing, and `vmstat`'s `si`/`so`
  signature are described, and ch. 7
  and ch. 11 label them as described
  each time.
- *Huge-machine readings* (a load of 20
  on 64 cores): arithmetic from
  ch. 2's definition, presented as
  translation examples, not captures.
- *htop's colours, setup screens,
  search, and filter:* described from
  htop's documentation, as detailed
  above. What the text render *did*
  preserve — meters, values, tree
  branches — is quoted as capture.
- *top's interactive keystrokes*
  (sorting with P/M, the `1` per-core
  split, the Irix/Solaris `I` toggle):
  described; batch mode has no keys.
  The batch equivalents (`-o %MEM`)
  are captured.
- *systemd's watching tools*
  (`systemctl status`, `journalctl -u`,
  cgroup accounting): named as the
  neighbouring guide's territory
  wherever process ownership by a
  service manager matters, never
  silently assumed.
- *macOS and BSD ps/top:* named once,
  plainly — different flags, different
  columns, no load-average twin in the
  same form. No non-Linux machine was
  available to the build.

Specimen discipline, for the record:
every process signalled, reniced, or
killed by name or PID in this guide was
a lab specimen started for that purpose,
with one honourable exception — the
capture harness's own shells, ended by
the pkill accident of ch. 8, which is
kept in the guide *because* it happened.
The memory eater's cap, the spinners'
self-expiry, and a final census after
teardown (no specimen processes
remaining, zombie count back to 0) are
the lab's closing state, verified
before this file was written.
