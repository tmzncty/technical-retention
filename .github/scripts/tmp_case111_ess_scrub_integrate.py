from pathlib import Path

EVIDENCE_PATH = Path('evidence/111-ibm-ess-post-offline-scrub-completion-deepening.md')
assert not EVIDENCE_PATH.exists(), EVIDENCE_PATH
EVIDENCE = r'''# Evidence 111C — IBM ESS post-offline scrub completion deepening

**Status:** `grounded`

## Scope

This record deepens one bounded part of Case 111: IBM Elastic Storage Server documentation does not stop at a calendar-based instruction to restore power after a long shutdown. It also names a **system-level disk scrubbing run** and gives an operator-visible log marker for completion at the vdisk / declustered-array layer.

The bounded question is:

> when an extended-offline SSD policy calls the system back into powered service, what evidence separates **maintenance opportunity** from an observed **maintenance-completion event**?

This is deliberately narrower than a general history of SSD refresh, IBM Spectrum Scale RAID, or Flash data-retention physics.

---

## Source role and historical context

### Historical / primary vendor record (`H/P`)

IBM's **_IBM Spectrum Scale RAID Frequently Asked Questions and Answers_** describes the Elastic Storage Server (ESS) as an IBM storage system in which Spectrum Scale RAID software actively manages RAID functions. The surviving HTML edition is headed **February 2023**; the corresponding FAQ/PDF records earlier update history as well.

In its SSD extended-shutdown guidance, IBM states that enterprise SSDs are designed and warranted against the JEDEC three-month-at-40 °C retention relation and then gives an earlier operational intervention point.

Two nearby formulations matter:

1. one recommendation says a system and its enclosed drives should be powered up for **at least two weeks after two months of system power-off**;
2. the ESS-specific continuation says that after **two months powered off**, the system should be powered on **to allow the disk scrubbing process to complete a run**.

For the latter path IBM supplies an explicit completion witness: the `mmfs` log (`/var/adm/ras/`) should contain, for each vdisk in each declustered array, a message of the form:

```text
[I] End scrubbing tracks of md_DA1_LG2
```

IBM then says this is how to ensure that all vdisks are scrubbed.

This is unusually useful because the source itself moves from a **calendar schedule** to a **named maintenance process** and then to **operator-visible completion evidence**.

### Historical / primary vendor record (`H/P`) — scrub and sanitize are distinct operations

The same extended-shutdown passage separately advises that a system intended for another activity in the future should have its drives cleared using **Sanitize with Block Erase** before shutdown when the data is no longer needed.

Therefore, within one vendor document:

```text
disk scrubbing for continued retained service
    !=
Sanitize with Block Erase for clearing data
```

The source does not present scrubbing as sanitization and does not present sanitize as the completion marker for the retention-maintenance scrub.

---

## Engineering reconstruction

The terms below are project reconstruction unless explicitly marked as IBM wording.

### E — time-off threshold != data-loss verdict

The two-month point is an operator intervention threshold in this ESS guidance. It does not mean every SSD has become unreadable at two months. IBM itself places the standards-level background at three months / 40 °C and describes data loss after extended shutdown as a potential risk rather than a deterministic clock edge.

Therefore:

```text
two months elapsed
    !=
individual-drive failure established
```

### E — power restored != scrub admitted != scrub complete

The FAQ gives a staged operational relation:

```text
extended powered-off interval
    -> restore powered operation
    -> allow disk scrub to run
    -> observe completion for each vdisk / declustered array
```

Merely applying power creates a maintenance opportunity. The separately named scrub process and completion log stop us from treating `powered on` as equivalent to `maintenance complete`.

### E — prescribed dwell time != observed completion evidence

The same FAQ contains both a **time-based powered interval** (at least two weeks after two months off) and a more specific **scrub-completion witness**. These are related but not identical forms of evidence.

A prescribed dwell time says how long the vendor tells an operator to make maintenance opportunity available. A per-vdisk `End scrubbing tracks ...` message says that a named system-level maintenance pass has reached its documented end condition for that object.

Thus:

```text
maintenance window supplied
    !=
maintenance process observed complete
```

### E — vdisk scrub completion != every NAND cell rewritten

The completion witness is at the Spectrum Scale RAID / vdisk / declustered-array layer. The inspected FAQ does **not** disclose:

- whether every physical NAND page is read;
- whether every corrected read causes a rewrite;
- the SSD firmware's internal read-reclaim threshold;
- whether a drive-local refresh task has independently completed;
- the physical location of all historical Flash embodiments.

Consequently:

```text
all documented vdisks scrubbed
    !=
proof every NAND cell was rewritten
```

and:

```text
system-level scrub completion
    !=
device-internal maintenance implementation identified
```

### E — scrub completion != sanitize completion

The vendor document's separate Sanitize-with-Block-Erase instruction is direct evidence that these operations have different goals and contracts. A successful scrub supports continued service / integrity maintenance at the system layer; it is not evidence that old physical data embodiments are inaccessible.

Therefore:

```text
scrub complete
    !=
data sanitization complete
```

---

## Functional analogy / cross-case comparison

### A — Case 111 Dell read-triggered retention work vs IBM ESS scrub

The canonical Case 111 already records Dell guidance in which reading all used NAND cells can trigger device retention tasks. IBM ESS contributes a different observation layer: a **storage-system scrub** with per-vdisk completion telemetry.

The bounded analogy is:

```text
re-observation of retained data
    can be part of retention maintenance
```

The mechanisms are not collapsed. Dell's support description concerns device retention tasks triggered by a read over used NAND; IBM's ESS FAQ exposes a Spectrum Scale RAID / vdisk scrub workflow. No firmware identity or genealogy is asserted.

### A — time-based policy and state-based completion can coexist

Case 111 previously showed that vendor maintenance cadences are not the same thing as standards qualification. This deepening adds a second distinction inside the operator policy itself:

```text
calendar trigger / dwell recommendation
    !=
state-based evidence that a named maintenance pass ended
```

This is a functional comparison of control semantics, not a claim that every storage product offers equivalent completion telemetry.

---

## Philosophical / project interpretation

### I — retained service can require re-observation plus witnessed recommissioning

A bounded project interpretation is that nonvolatile retention can become an **active recommissioning process**: after a sufficiently long interval in which maintenance machinery could not run, the system is not merely powered; retained state is re-observed through a scrub, and the operator can wait for a documented completion witness.

This is not IBM's philosophical vocabulary. It is an interpretation of the layered operational sequence exposed by the vendor record.

---

## Prior art and related-repository boundary

No invention-priority claim is made for IBM's scrub workflow, RAID scrubbing, Flash refresh, or operator maintenance schedules.

A fresh search of `tmzncty/computing-archaeology` for `ESS background scrub SSD retention` found no dedicated reusable historical module. This evidence therefore stays narrowly in `technical-retention`. A genealogy of storage-system scrubbing, patrol reads, RAID consistency checking, or Flash refresh belongs in `computing-archaeology` if developed later.

---

## Explicit stop conditions / unsupported upgrades

This record does **not** establish:

- that two months is an intrinsic NAND-retention limit;
- that every IBM ESS generation uses exactly the same scrub implementation;
- that applying power immediately certifies retained data;
- that the two-week powered interval and the scrub completion marker are interchangeable guarantees;
- that a vdisk scrub necessarily reads every physical Flash page;
- that every successful scrub causes NAND refresh or rewrite;
- the device firmware's read-reclaim / refresh thresholds;
- that `End scrubbing tracks ...` proves every drive-internal maintenance task complete;
- that scrub completion proves sanitization or forensic irrecoverability;
- invention priority or direct genealogy for data scrubbing;
- universal applicability to non-ESS SSD systems.

---

## Sources

### Primary vendor documentation

IBM, **_IBM Spectrum Scale RAID Frequently Asked Questions and Answers_**, surviving HTML edition headed **February 2023**.

<https://www.ibm.com/docs/en/SSYSP8/gnrfaq.html>

Corresponding IBM-hosted FAQ PDF:

<https://www.ibm.com/support/knowledgecenter/SSYSP8/gnrfaq.pdf>

Inspected anchors:

- ESS / Spectrum Scale RAID system description;
- extended-shutdown note for SSD-based systems;
- enterprise SSD three-month / 40 °C standards background;
- power-on guidance after two months off;
- instruction to allow the disk scrubbing process to complete a run;
- `mmfs` per-vdisk / declustered-array completion message;
- separate Sanitize-with-Block-Erase instruction for clearing drives before future reuse.

---

## Bounded conclusion

IBM ESS documentation supplies a stronger completion boundary than the generic statement “power the SSD back on.” After the documented long-offline interval, the operator is told to make powered operation available **and to allow a named disk-scrubbing run to complete**, with a per-vdisk log marker as completion evidence.

The resulting relation is:

```text
offline-time policy
    -> powered maintenance opportunity
    -> system scrub execution
    -> operator-visible scrub completion
```

while preserving all of the following non-equivalences:

```text
time threshold != failure verdict
power restored != scrub complete
scrub complete != every NAND cell rewritten
scrub complete != sanitize complete
```
'''
EVIDENCE_PATH.write_text(EVIDENCE, encoding='utf-8')

case_path = Path('cases/111-enterprise-ssd-extended-shutdown-maintenance.md')
case = case_path.read_text(encoding='utf-8')
assert '111-ibm-ess-post-offline-scrub-completion-deepening.md' not in case
nav_anchor = 'NetApp rated-life/offline-retention telemetry deepening: [`../evidence/111-netapp-rated-life-offline-retention-telemetry-deepening.md`](../evidence/111-netapp-rated-life-offline-retention-telemetry-deepening.md).'
assert nav_anchor in case
case = case.replace(nav_anchor, nav_anchor + '\n\nIBM ESS post-offline scrub-completion deepening: [`../evidence/111-ibm-ess-post-offline-scrub-completion-deepening.md`](../evidence/111-ibm-ess-post-offline-scrub-completion-deepening.md).', 1)

marker = '## Engineering reconstruction\n'
assert marker in case
follow = r'''## IBM ESS follow-up — post-offline scrub and operator-visible completion

A bounded ESS-specific follow-up is now grounded in [`evidence/111-ibm-ess-post-offline-scrub-completion-deepening.md`](../evidence/111-ibm-ess-post-offline-scrub-completion-deepening.md).

IBM's _Spectrum Scale RAID Frequently Asked Questions and Answers_ goes beyond the generic instruction to restore power after an extended SSD shutdown. For an SSD-based ESS system powered off for two months, it tells the operator to power the system on **to allow the disk scrubbing process to complete a run**, and gives an `mmfs` completion message — `End scrubbing tracks of ...` — to be observed for each vdisk in each declustered array. The same FAQ separately gives a time-based recommendation of at least two weeks powered after two months off.

This sharpens the case's maintenance state machine:

```text
calendar intervention point
    != powered maintenance opportunity
    != named scrub execution
    != observed per-vdisk scrub completion
```

The evidence remains system-layer evidence. A Spectrum Scale RAID scrub completion message does **not** prove that every NAND cell was read or rewritten, does not expose drive-firmware refresh thresholds, and does not establish that every hidden device-local retention task is complete. The same IBM passage separately prescribes **Sanitize with Block Erase** when drives are to be cleared for later reuse, so `scrub complete != sanitize complete` is directly preserved in the vendor record.

'''
case = case.replace(marker, follow + marker, 1)
case_path.write_text(case, encoding='utf-8')

roadmap_path = Path('ROADMAP.md')
roadmap = roadmap_path.read_text(encoding='utf-8')
assert 'Case 111 IBM ESS post-offline scrub completion' not in roadmap
phase = '## Phase 2 — Build missing technical bridges\n\n'
assert phase in roadmap
bullet = "- [x] **Case 111 IBM ESS post-offline scrub completion:** [`cases/111-enterprise-ssd-extended-shutdown-maintenance.md`](cases/111-enterprise-ssd-extended-shutdown-maintenance.md) + [`evidence/111-ibm-ess-post-offline-scrub-completion-deepening.md`](evidence/111-ibm-ess-post-offline-scrub-completion-deepening.md) ground an ESS-specific transition from two-month offline policy to powered disk-scrub execution and per-vdisk `mmfs` completion evidence, while keeping `power restored != scrub complete != every NAND cell rewritten != sanitize complete`.\n"
roadmap = roadmap.replace(phase, phase + bullet, 1)
roadmap_path.write_text(roadmap, encoding='utf-8')

index_path = Path('CASE_INDEX.md')
idx = index_path.read_text(encoding='utf-8')
assert '- **3541 —' in idx
assert '- **3542 —' not in idx
add = r'''

## Case 111 — IBM ESS post-offline scrub-completion deepening findings

Deepening record: [`evidence/111-ibm-ess-post-offline-scrub-completion-deepening.md`](evidence/111-ibm-ess-post-offline-scrub-completion-deepening.md).

- **3542 — ESS long-offline maintenance names a scrub process:** IBM's Spectrum Scale RAID FAQ says that after an SSD-based system and its enclosed drives have been powered off for two months, the system should be powered on to allow the disk scrubbing process to complete a run. (`H/P`)
- **3543 — time-based and process-based guidance coexist:** the same FAQ also says a system and its enclosed drives should be powered up for at least two weeks after two months off, so a prescribed powered dwell window and a named scrub completion condition are both present in the vendor record. (`H/P`)
- **3544 — per-vdisk completion telemetry:** IBM says scrub completion is indicated in the `mmfs` log by `End scrubbing tracks of ...` for each vdisk in each declustered array, providing operator-visible completion evidence at the storage-system layer. (`H/P`)
- **3545 — two-month intervention point != individual-drive failure verdict:** the two-month point is an operational policy threshold preceding the three-month / 40 °C standards background cited by IBM; it is not evidence that every drive has already lost data. (`E`)
- **3546 — power restored != scrub complete:** powering the system creates the opportunity for maintenance, while IBM separately names the scrub run and its completion message. (`E`)
- **3547 — dwell time != completion evidence:** an elapsed powered interval and an observed end-of-scrub marker are different evidence types even when both appear in one runbook. (`E`)
- **3548 — system scrub completion is object-scoped:** the documented completion witness is attached to vdisks / declustered arrays, not directly to individual NAND cells or hidden FTL structures. (`H/P, E`)
- **3549 — all vdisks scrubbed != every NAND cell rewritten:** the inspected FAQ does not disclose physical-page coverage, conditional rewrite policy, read-reclaim thresholds, or device-local refresh completion. (`E`)
- **3550 — scrub and sanitize are distinct vendor operations:** the same extended-shutdown passage separately prescribes Sanitize with Block Erase when drives are to be cleared for future reuse, so scrub completion is not the documented erase/sanitize contract. (`H/P, E`)
- **3551 — functional analogy to Dell is re-observation only:** Dell's used-NAND read can trigger device retention tasks, while IBM ESS exposes a Spectrum Scale RAID scrub with per-vdisk completion telemetry; both involve re-observation, but mechanism identity and genealogy are not established. (`A`)
- **3552 — calendar trigger != state-based completion:** Case 111 now contains direct evidence that an operator policy can combine a time trigger with an observable state transition marking a maintenance pass complete. (`E/A`)
- **3553 — retained service can require witnessed recommissioning:** project interpretation treats the sequence from offline interval through scrub completion as active recommissioning rather than mere restoration of electrical power; this is not IBM historical vocabulary. (`I`)
- **3554 — no device-internal completion claim:** `End scrubbing tracks ...` does not prove every drive-internal retention task, controller metadata pass, or NAND refresh operation has completed. (`X`, rejected upgrade)
- **3555 — no invention or universal-policy claim:** the evidence does not establish first invention of scrubbing, a universal SSD cadence, or applicability beyond the documented ESS/Spectrum Scale RAID context. (`X`, rejected upgrade)
'''
idx = idx.rstrip() + add + '\n'
index_path.write_text(idx, encoding='utf-8')

# Remove one-shot integration scaffolding from the final tree.
Path('.github/scripts/tmp_case111_ess_scrub_integrate.py').unlink()
Path('.github/workflows/tmp-case111-ess-scrub-integrate.yml').unlink()
