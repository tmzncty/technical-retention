from pathlib import Path

ROOT = Path('.')

synthesis = r'''# Synthesis 26 — Maintenance-Control State: Persistence Horizon, Reconstitution, and Authority

> **Question:** when one retained relation depends on auxiliary state that schedules, qualifies, resumes, authorizes, or audits maintenance, how long must that auxiliary state itself survive?

**Status:** bounded cross-case synthesis over already-grounded evidence. It introduces one project analytical term, `maintenance-control state`, and compares persistence horizons across existing cases. It does **not** claim one historical lineage or one universal metadata architecture across DRAM, NAND, SSD firmware, HDFS, or other distributed systems.

Grounded witnesses used here:

- [`Case 09 — DRAM CBR refresh-address internalization`](../cases/09-dram-cbr-refresh-address-internalization.md), especially [`evidence/09-dram-refresh-counter-initialization-test-deepening.md`](../evidence/09-dram-refresh-counter-initialization-test-deepening.md): a cyclic refresh-counter phase can be stateful and testable yet deliberately reinitialized at power-on;
- [`Case 78 — NAND bad-block management`](../cases/78-micron-nand-bad-block-marker-management.md), especially [`evidence/78-linux-mtd-2004-mirrored-versioned-bbt-deepening.md`](../evidence/78-linux-mtd-2004-mirrored-versioned-bbt-deepening.md): a Flash-resident bad-block table can require restart persistence, mirroring, version currentness, and protected placement;
- [`Case 83 — HDFS BlockScanner`](../cases/83-apache-hdfs-block-scanner-checksum-verification.md), especially [`evidence/83-hdfs-blockscanner-cursor-checkpoint-clock-domain-deepening.md`](../evidence/83-hdfs-blockscanner-cursor-checkpoint-clock-domain-deepening.md): a resumable maintenance cursor can persist across restart, while loss falls back to replay and a clock-domain bug shows configured checkpoint policy need not equal effective checkpointing;
- [`Case 116 — HDFS DataNode maintenance state`](../cases/116-apache-hdfs-datanode-maintenance-state.md), especially [`evidence/116-hadoop-301-maintenance-restart-reconstitution-deepening.md`](../evidence/116-hadoop-301-maintenance-restart-reconstitution-deepening.md): retained administrative intent can survive restart through configuration while runtime replica-location evidence is re-observed;
- [`Case 15 — Intel SSD 320 power-loss durability`](../cases/15-intel-ssd320-power-loss-durability.md), especially [`evidence/15-intel320-2011-unsafe-shutdown-telemetry-deepening.md`](../evidence/15-intel320-2011-unsafe-shutdown-telemetry-deepening.md): a cumulative unsafe-shutdown count can retain event evidence without becoming a payload-durability verdict.

The historical claims remain in those case/evidence records. The categories below are **engineering reconstruction**, not source vocabulary unless a source independently uses the same words.

---

## 1. Verdict

The repository should use `maintenance-control state` as a bounded umbrella for non-payload state whose role is to **schedule, qualify, resume, authorize, or audit work that preserves another retained relation**.

The term is useful only if it does not imply one persistence contract. The five witnesses immediately reject that shortcut:

```text
DRAM refresh counter
    -> regime-local cyclic phase
    -> reinitialize at power-on

HDFS scanner cursor
    -> restart-progress checkpoint
    -> resume if readable, replay if lost

Flash BBT
    -> restart-persistent qualification/currentness state
    -> mirror + version + protected placement

HDFS maintenance configuration
    -> retained policy/expiry
    -> reload policy, re-observe runtime embodiment evidence

SSD unsafe-shutdown counter
    -> cumulative event-history summary
    -> persists as telemetry, not as a durability verdict
```

Therefore the main rule is:

> **maintenance-control state must be classified by role, authority, failure consequence, and required persistence horizon; `metadata` or `checkpoint` alone is too coarse.**

This synthesis does not create an exhaustive taxonomy. It establishes a comparison discipline that survives the current counterexamples.

---

## 2. Claim discipline

Following [`METHOD.md`](METHOD.md) and [`../AGENTS.md`](../AGENTS.md):

- **H/P — historical / primary:** product, patent, project-source, and release-specific facts remain grounded in the individual cases;
- **E — engineering reconstruction:** `maintenance-control state`, persistence-horizon comparison, and the role matrix are project analytical tools;
- **A — functional analogy:** similarity of role does not establish shared mechanism or genealogy;
- **I — philosophical interpretation:** interpretation is limited to differentiated support conditions for technical persistence.

The synthesis specifically rejects the phrase `memory of memory` as a substitute for mechanism. Auxiliary state can be initialized, replayed, mirrored, reloaded, re-observed, or accumulated under sharply different contracts.

---

## 3. Why this is not Synthesis 24 again

[`SYNTHESIS_24_RETENTION_MAINTENANCE_TRIGGER_REGIMES.md`](SYNTHESIS_24_RETENTION_MAINTENANCE_TRIGGER_REGIMES.md) asks **what condition makes preservation work due**: access, elapsed time, capacity pressure, wear, failure, and so on.

This synthesis asks a different question:

> **What state does the preservation machinery itself need in order to know what to do, where to continue, what to trust, or what happened — and across which interruption must that state survive?**

Trigger regime and control-state horizon are therefore orthogonal. A deadline-driven DRAM regime can use volatile cyclic phase; a proactive scanner can use a restart checkpoint; a failure-management path can depend on a durable exclusion map.

> **same maintenance trigger ≠ same maintenance-control-state persistence horizon**

and

> **same persistence horizon ≠ same control authority**.

---

## 4. Comparison axes

For any proposed maintenance-control state, audit at least these axes:

| Axis | Question |
| --- | --- |
| **role** | Does the state carry phase, progress, qualification/currentness, policy/authority, event history, or runtime observation? |
| **target relation** | What retained payload or service relation does it help preserve? |
| **minimum horizon** | Must it survive only the active regime, process restart, device power cycle, media replacement, or the device/system lifetime? |
| **reconstitution path** | Initialize, replay, reload configuration, compare copies, reconstruct from payload, or re-observe participants? |
| **authority** | Advisory only, scheduling input, allocation gate, service-admission gate, or direct currentness selector? |
| **failure consequence** | Repeated work, delayed evidence, unsafe reuse/admission, loss of optimization, loss of diagnosis, or direct loss of recoverability? |
| **history semantics** | Current phase/currentness scalar, compact summary, or event-by-event history? |
| **durability evidence** | Interface/source contract only, or independently tested fault/power-loss behavior? |

A strong case should avoid filling unknown cells by analogy.

---

## 5. Regime-local phase — Case 09

The TI DRAM evidence shows a refresh counter with stateful sequential phase that is forced to zero at power-on and then increments across CAS-before-RAS refresh cycles. Motorola product documentation separately makes counter progression testable.

The key relation is:

```text
powered retention regime active
    -> counter phase matters for next-row coverage

power removed / new regime begins
    -> disclosed counter phase is reinitialized
```

The counter is constitutive maintenance state while refresh is active, yet cross-power durability is not part of the disclosed contract.

Therefore:

> **constitutive maintenance state ≠ durable checkpoint**

and

> **maintenance phase ≠ maintenance history**.

The counter's role is to distribute future work, not to preserve a complete record of prior refreshes.

---

## 6. Restart-progress checkpoint — Case 83

The HDFS scanner cursor has a different contract. It retains traversal position so a restarted scanner can continue rather than repeat the whole scan. If the cursor is absent or unreadable, the implementation creates a fresh iterator.

Thus cursor loss is not payload rollback. It changes the amount and ordering of future maintenance work:

```text
cursor survives
    -> resume later in traversal

cursor lost
    -> replay from fresh iterator
    -> earlier work repeated
    -> later blocks may wait longer for renewed verification evidence
```

This fixes two boundaries:

> **maintenance-progress loss ≠ payload loss**

but also

> **reconstructable/replayable control state ≠ consequence-free control state**.

The clock-domain defect in the intended periodic-save branch adds a second lesson: a documented/configured persistence policy can fail at implementation level.

> **retention policy intent ≠ effective retention behavior**.

---

## 7. Qualification/currentness map — Case 78

The Linux MTD Flash BBT carries a stronger form of authority. It records which blocks are excluded or reserved from ordinary use. The 2004 implementation can retain primary/mirror copies with version numbers, choose the higher readable version, and rewrite a missing or stale peer.

Here loss or stale selection can affect **admission of physical media**, not merely maintenance efficiency. That is why restart continuity and currentness discrimination matter.

But the stronger persistence requirement must not be overread:

> **mirrored/versioned control state ≠ transactional or power-fail-atomic update proof**.

And the version field is a currentness discriminator rather than an event log:

> **qualification currentness ≠ failure history**.

The BBT therefore differs from both the DRAM counter and HDFS cursor even though all three are non-payload state used by maintenance infrastructure.

---

## 8. Retained policy versus re-observed runtime evidence — Case 116

Hadoop 3.0.1 maintenance mode supplies a split persistence contract. Administrative state and expiry can be reloaded from the combined-host configuration after NameNode restart, while knowledge that a currently absent maintenance DataNode actually embodies a replica may require later DataNode return/re-registration.

So one maintenance relation can combine:

```text
retained policy source
    +
reconstituted in-memory policy object
    +
re-observed runtime embodiment evidence
```

This gives a strong boundary:

> **policy persistence ≠ persistence of every runtime fact used under that policy**.

It also blocks a common distributed-systems shortcut:

> **physical embodiment may survive ≠ coordinator presently knows or credits that embodiment**.

Re-observation is therefore a legitimate continuity mechanism alongside storage and replay.

---

## 9. Cumulative event-history summary — Case 15

Intel SSD 320 SMART C0h has yet another role. It is a lifetime cumulative count of unsafe/unclean shutdown events under the documented product semantics. It does not schedule the next NAND address or restore a scan cursor. It records a compact summary of past exposure.

The retained scalar lacks per-event timestamps, affected LBAs, outstanding-command state, PLP completion, and post-restart outcome.

Therefore:

> **cumulative event count ≠ per-event audit history**

and

> **event evidence ≠ preservation outcome**.

This matters because control/telemetry state can survive longer than the event it describes while remaining advisory rather than directly authoritative over payload currentness.

The product documentation also leaves the exact counter-update persistence mechanism open, so:

> **documented cumulative semantics ≠ demonstrated power-fail-atomic telemetry update**.

---

## 10. Persistence horizon ≠ authority

The five cases show that persistence duration and decision authority are independent axes.

- A short-lived DRAM counter phase can be essential to full-array coverage.
- A restart-persistent HDFS cursor can be lost with replay rather than unsafe payload admission.
- A Flash BBT can gate whether a block is eligible for ordinary use.
- An HDFS maintenance config can retain policy while runtime replica evidence is deliberately rebuilt conservatively.
- A lifetime SMART count can persist for diagnosis without selecting payload currentness.

Therefore neither of these shortcuts is safe:

> **long-lived metadata = more authoritative metadata**

> **short-lived/reconstructable metadata = less important metadata**.

Authority must be reconstructed from the bounded mechanism.

---

## 11. Reconstitution is part of retention architecture

A maintenance-control relation need not survive by preserving one unchanged representation. Across the witnesses, continuity can be produced by:

- deterministic initialization;
- replay of maintenance work;
- mirror/version comparison and repair;
- configuration reload;
- participant re-observation;
- cumulative update of compact telemetry.

This gives a useful cross-case rule:

> **persistence can be provided by retained representation, by controlled reconstitution, or by a composition of both.**

That is compatible with [`SYNTHESIS_25_RECURRENCE_REFRESH_TERMINOLOGY.md`](SYNTHESIS_25_RECURRENCE_REFRESH_TERMINOLOGY.md): reconstitution can preserve an operational relation without implying that one physical token or one exact in-memory object survives.

The rule is analytical. It is not a claim that the historical systems shared vocabulary or design lineage.

---

## 12. Checkpoint ≠ certificate

The cases also expose why `checkpoint` is dangerous as a generic word.

- The HDFS scanner cursor says where traversal had reached, not that every earlier block verified successfully.
- The DRAM counter test can expose bounded enumerator progression, not certify all future refresh deadlines.
- The BBT version says which readable table is newer under the implementation rule, not why each block was retired or that the whole update was crash-atomic.

Therefore:

> **retained progress/currentness evidence ≠ complete correctness certificate**.

A maintenance-control record should be read according to the exact proposition it supports.

---

## 13. Failure consequences differ by role

Losing maintenance-control state can have qualitatively different consequences:

| State role | Bounded loss/staleness consequence |
| --- | --- |
| cyclic phase | coverage sequence restarts / must be re-established within the active regime |
| traversal checkpoint | maintenance replay and delayed later coverage |
| qualification/currentness map | risk of using or trusting an inadmissible physical resource if no safe reconstruction path exists |
| retained policy | desired administrative relation may be lost unless reloadable; runtime reliance may still require fresh observation |
| event-history summary | diagnostic/audit information can be incomplete without directly proving payload loss |

This is why `control metadata corrupted` is not a sufficient failure description.

---

## 14. Functional analogies and stop conditions

The cross-case comparison is functional only.

- DRAM counter state is not a filesystem checkpoint.
- A Flash BBT mirror is not consensus replication.
- HDFS configuration reload is not a device firmware journal.
- SMART event telemetry is not repair-history currentness.
- Re-observed replica location is not proof that the bytes became physically rewritten.

No genealogy among these mechanisms is asserted.

A fresh search of `tmzncty/computing-archaeology` for the combined refresh-counter / BBT / scanner-cursor / unsafe-shutdown relation found no dedicated cross-technology study to reuse. Broad histories of DRAM control logic, NAND BBTs, SMART telemetry, or HDFS maintenance mechanisms remain companion-repository work. This document keeps only the retention-specific comparison.

---

## 15. Philosophical interpretation — bounded

The exact technical fact is that preservation can depend on auxiliary state whose required lifetime differs from both the payload and from other control state in the same system.

The narrow conceptual payoff is:

> **technical persistence is often supported by a stratified set of states, some retained, some replayed, some reinitialized, and some re-observed. Continuity of the higher-level relation does not require every supporting representation to persist in the same way.**

This blocks both extremes: persistence is not merely untouched material survival, but neither does every support relation need infinite recursive preservation.

The interpretation stops there. The evidence does not justify `machines remember how to remember`, a universal theory of metadata, or a claim that every maintenance process needs its own durable history.

---

## 16. Rejected strong claims

- **`maintenance-control state is always durable metadata` — rejected.** Case 09 directly supplies a regime-local, power-on-initialized counter phase.
- **`reconstructable state is unimportant` — rejected.** Replay can consume maintenance budget; re-observation can change what embodiments may be credited.
- **`persisted state is automatically authoritative` — rejected.** SMART event history can be persistent yet advisory; HDFS policy can persist while runtime replica evidence is rebuilt.
- **`version/currentness state is history` — rejected.** The BBT version selects the newer representation without preserving a bad-block event ledger.
- **`checkpoint means verified correctness` — rejected.** The HDFS cursor and DRAM counter-test boundaries contradict this.
- **`duplicate control state implies consensus or crash atomicity` — rejected.** The BBT mirror is a local reconciliation mechanism with explicit fault limits.
- **`control-state loss implies payload loss` — rejected as a universal rule.** Cursor loss can cause replay; telemetry loss can lose diagnosis; other control-state failures can be much more severe.
- **`payload survival implies control-state survival` — rejected.** A physical replica can survive while a restarted NameNode has not yet re-observed it.

---

## 17. Research consequences

Future cases that introduce auxiliary preservation state should explicitly answer:

1. What proposition does the state encode?
2. What decision consumes it?
3. What is its minimum required persistence horizon?
4. Can it be reconstructed, replayed, or re-observed?
5. What happens while it is missing or stale?
6. Does it encode phase/currentness, a compact summary, or actual history?
7. What evidence establishes its own durability under the relevant failure model?
8. Does a duplicate copy add redundancy, currentness discrimination, atomicity, or only risk reduction?

This gives future Flash/SSD and distributed-storage cases a common checklist without forcing them into one mechanism.

---

## Sources and evidence custody

This synthesis introduces no new historical floor. Historical claims are inherited from the grounded evidence records listed at the top:

- TI US4653030A and Motorola 1989 *Memory Data* through Case 09 evidence;
- Linux MTD 2004 documentation/CVS source through Case 78 evidence;
- Apache HDFS-7430, HDFS-12209, and Hadoop 2.7.3 source through Case 83 evidence;
- Apache Hadoop 3.0.1 documentation/source/tests through Case 116 evidence;
- Intel SSD 320 September/March 2011 manufacturer documents through Case 15 evidence.

For exact URLs, page anchors, version tags, and evidence grades, use the linked case/evidence records rather than treating this synthesis as a substitute source.
'''

findings = r'''
## Synthesis 26 — Maintenance-control-state persistence-horizon findings

Evidence: [`docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md`](docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md), drawing only on already-grounded Cases 09, 15, 78, 83, and 116.

- **2665 — `maintenance-control state` is a project analytical role, not a source-era device class.** It names non-payload state used to schedule, qualify, resume, authorize, or audit preservation work; historical actors and vendors retain their own vocabulary. (`E`, `X`)
- **2666 — constitutive maintenance state != durable checkpoint.** TI's disclosed DRAM refresh counter carries sequential phase during the powered regime yet is initialized at power-on rather than preserved as cross-power history. (`H/P` inherited, `E`)
- **2667 — restart-progress checkpoint != payload durability state.** The HDFS BlockScanner cursor can survive process restart to avoid replay while storing traversal position rather than user payload or a complete verification ledger. (`H/P` inherited, `E`)
- **2668 — reconstructable/replayable control state != consequence-free control state.** Losing an HDFS scan cursor can restart traversal, consuming bounded scan bandwidth and delaying renewed verification evidence for later blocks even though payload bytes are not rolled back. (`H/P` inherited, `E`)
- **2669 — qualification/currentness metadata can require a stronger persistence contract than traversal phase.** Linux MTD's Flash BBT persists block-admissibility state with primary/mirror versions and protected placement because safe ordinary allocation depends on that relation after restart. (`H/P` inherited, `E`)
- **2670 — duplicate + versioned control state != transactional or power-fail-atomic update proof.** The bounded BBT implementation can select a newer readable peer and repair a lagging one, but separate erase/write operations do not establish universal crash atomicity. (`H/P` inherited, `E`, `X`)
- **2671 — retained policy != retained runtime observation.** Hadoop 3.0.1 can reload maintenance intent/expiry from host configuration while replica-location evidence for an absent maintenance DataNode may need later re-observation. (`H/P` inherited, `E`)
- **2672 — physical embodiment survival != coordinator knowledge/credit.** A replica may still exist on a DataNode while a restarted NameNode conservatively restores ordinary live replicas because that embodiment has not yet been re-observed. (`H/P` inherited, `E`)
- **2673 — cumulative maintenance-adjacent event history != preservation outcome.** Intel SSD 320 C0h can retain the number of unsafe shutdown events without recording whether PLP succeeded or which payload, if any, was lost. (`H/P` inherited, `E`)
- **2674 — persistence horizon != authority.** A short-lived refresh phase can be operationally essential, a restart-persistent BBT can gate media admission, and a lifetime SMART counter can remain advisory; duration alone does not rank authority. (`E`, `A`)
- **2675 — reconstructable != disposable or unimportant.** Initialization, replay, configuration reload, mirror reconciliation, and participant re-observation are distinct continuity mechanisms whose temporary absence can alter cost, coverage, or admissibility. (`E`, `A`)
- **2676 — checkpoint/currentness evidence != correctness certificate or full history.** HDFS cursor position does not prove all earlier blocks verified successfully, a BBT version is not a bad-block event ledger, and a DRAM counter test does not certify all future refresh deadlines. (`H/P` inherited, `E`, `X`)
- **2677 — documented retention policy != effective retention implementation.** Case 83's monotonic-versus-wall-clock mismatch demonstrates that a configured periodic save interval can fail to produce the intended checkpoint cadence. (`H/P` inherited, `E`)
- **2678 — maintenance-control-state survival and payload survival are not mutually entailed.** Payload/replica bytes can survive while runtime control knowledge must be rebuilt; compact control telemetry can also survive an event without proving payload survival. (`E`, `A`, `X`)
- **2679 — related-repository boundary:** a fresh `tmzncty/computing-archaeology` search found no dedicated cross-technology treatment combining DRAM refresh phase, NAND BBT persistence, HDFS scanner/policy reconstitution, and SSD unsafe-shutdown telemetry; broad mechanism genealogies remain there, while Synthesis 26 keeps the retention-specific role/horizon comparison. (`H/P` project-state record)
'''

roadmap_line = "- [x] Distinguish maintenance-control-state role, authority, reconstitution path, and persistence horizon — bounded by [`docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md`](docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md): grounded Cases 09, 15, 78, 83, and 116 separate regime-local cyclic phase, restart-progress checkpoint, restart-persistent qualification/currentness state, retained policy, re-observed runtime embodiment evidence, and cumulative event-history summary. This closes only the cross-case decomposition `maintenance-control state != one universal durable-checkpoint contract`; mechanism genealogy, implementation-specific fault atomicity, and broader DRAM/NAND/SMART/HDFS history remain routed to `computing-archaeology`."

readme_s25 = "A bounded recurrence/refresh terminology synthesis is now available in [`docs/SYNTHESIS_25_RECURRENCE_REFRESH_TERMINOLOGY.md`](docs/SYNTHESIS_25_RECURRENCE_REFRESH_TERMINOLOGY.md). It reserves `recurrence` as a project identity-through-re-instantiation descriptor while keeping period/source terms such as recirculation, regeneration, rewrite, and refresh historically distinct; it also rejects the shortcuts `recurrence = refresh`, `continuous recurrence = deadline refresh`, and `state recurrence = history retention`."

readme_s26 = "A bounded maintenance-control-state persistence-horizon synthesis is now available in [`docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md`](docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md). Across grounded DRAM, raw-NAND, SSD telemetry, and HDFS cases it separates regime-local phase, restart-progress checkpoint, qualification/currentness map, retained policy, re-observed runtime evidence, and cumulative event-history summary. It fixes the counterexamples `maintenance-control state != durable checkpoint`, `persistence horizon != authority`, `checkpoint != correctness certificate`, `reconstructable != consequence-free`, and `policy retention != effective implementation behavior`."

readme_nav = "- [`docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md`](docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md) — bounded cross-case synthesis separating maintenance-control-state role, required persistence horizon, reconstitution path, authority, history semantics, and loss consequence across grounded DRAM refresh phase, Linux MTD BBT, HDFS scanner/maintenance state, and Intel SSD unsafe-shutdown telemetry."

glossary = r'''## maintenance-control state

A project analytical descriptor for **non-payload state used to schedule, qualify, resume, authorize, or audit maintenance of another retained relation**.

The term does **not** imply that the state is durable, checkpointed, historical, replicated, or equally authoritative across systems. A maintenance-control state may be:

- a regime-local cyclic phase that is reinitialized;
- a restart-progress checkpoint whose loss causes replay;
- a persistent qualification/currentness map;
- retained policy reloaded after restart;
- runtime embodiment evidence that must be re-observed;
- a cumulative diagnostic/event-history summary.

Always state its role, minimum persistence horizon, reconstitution path, authority, loss consequence, and whether it carries phase/currentness, compact summary, or actual history. Do not call every such state a `checkpoint`.

See [`SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md`](SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md).
'''


def replace_once(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f'{label}: expected exactly one anchor, found {n}')
    return text.replace(old, new, 1)

# Create synthesis document.
synth_path = ROOT / 'docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md'
if synth_path.exists():
    raise RuntimeError('Synthesis 26 already exists; refusing duplicate application')
synth_path.write_text(synthesis.rstrip() + '\n', encoding='utf-8')

# README: add missing chain entries for Synthesis 25 and new 26, then navigation.
readme_path = ROOT / 'README.md'
readme = readme_path.read_text(encoding='utf-8')
chain_anchor = '\n\nThis chain is a **research heuristic**, not a claim that all of these mechanisms are historically or philosophically identical.'
if 'A bounded recurrence/refresh terminology synthesis is now available' not in readme:
    readme = replace_once(readme, chain_anchor, '\n\n' + readme_s25 + '\n\n' + readme_s26 + chain_anchor, 'README synthesis chain')
elif 'A bounded maintenance-control-state persistence-horizon synthesis is now available' not in readme:
    readme = replace_once(readme, chain_anchor, '\n\n' + readme_s26 + chain_anchor, 'README synthesis chain 26')
nav_anchor = "- [`docs/SYNTHESIS_25_RECURRENCE_REFRESH_TERMINOLOGY.md`](docs/SYNTHESIS_25_RECURRENCE_REFRESH_TERMINOLOGY.md) — bounded terminology synthesis separating identity-through-re-instantiation (`recurrence`) from source-sensitive maintenance operations (`refresh`), grounded by 1947–1976 delay-line/DRAM primary vocabulary and explicitly rejecting a shared-mechanism or genealogy claim."
if 'SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md`](docs/' not in readme:
    readme = replace_once(readme, nav_anchor, nav_anchor + '\n' + readme_nav, 'README nav')
readme_path.write_text(readme.rstrip() + '\n', encoding='utf-8')

# ROADMAP: insert the completed bounded synthesis after the existing maintenance-trigger taxonomy item.
roadmap_path = ROOT / 'ROADMAP.md'
roadmap = roadmap_path.read_text(encoding='utf-8')
if 'SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md' not in roadmap:
    lines = roadmap.splitlines()
    candidates = [i for i, line in enumerate(lines) if line.startswith('- [x] Formally distinguish quiescent retention') and 'SYNTHESIS_24_RETENTION_MAINTENANCE_TRIGGER_REGIMES.md' in line]
    if len(candidates) != 1:
        raise RuntimeError(f'ROADMAP synthesis24 anchor count: {len(candidates)}')
    lines.insert(candidates[0] + 1, roadmap_line)
    roadmap = '\n'.join(lines) + '\n'
roadmap_path.write_text(roadmap, encoding='utf-8')

# Glossary: define the cross-case term immediately after the regime taxonomy.
gloss_path = ROOT / 'docs/GLOSSARY.md'
gloss = gloss_path.read_text(encoding='utf-8')
if '## maintenance-control state' not in gloss:
    anchor = 'See [`SYNTHESIS_24_RETENTION_MAINTENANCE_TRIGGER_REGIMES.md`](SYNTHESIS_24_RETENTION_MAINTENANCE_TRIGGER_REGIMES.md).\n\n## remanence'
    replacement = 'See [`SYNTHESIS_24_RETENTION_MAINTENANCE_TRIGGER_REGIMES.md`](SYNTHESIS_24_RETENTION_MAINTENANCE_TRIGGER_REGIMES.md).\n\n' + glossary.rstrip() + '\n\n## remanence'
    gloss = replace_once(gloss, anchor, replacement, 'GLOSSARY anchor')
gloss_path.write_text(gloss.rstrip() + '\n', encoding='utf-8')

# CASE_INDEX: append controlled findings after the current final finding.
idx_path = ROOT / 'CASE_INDEX.md'
idx = idx_path.read_text(encoding='utf-8')
if '**2665 —' in idx:
    raise RuntimeError('CASE_INDEX already contains Synthesis 26 findings')
if idx.count('**2664 —') != 1:
    raise RuntimeError('CASE_INDEX expected one current terminal finding 2664')
idx = idx.rstrip() + '\n\n' + findings.strip() + '\n'
idx_path.write_text(idx, encoding='utf-8')

# Normalize trailing whitespace in touched text files.
for path in [synth_path, readme_path, roadmap_path, gloss_path, idx_path]:
    text = path.read_text(encoding='utf-8')
    text = '\n'.join(line.rstrip() for line in text.splitlines()) + '\n'
    path.write_text(text, encoding='utf-8')
