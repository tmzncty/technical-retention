# Evidence 94B — Linux MD RAID6 scrub mismatch and repair authority

**Status:** `bounded deepening complete`

## Purpose

Deepen Case 94 at one narrow operational boundary that the P+Q algebra by itself does not settle:

> when every RAID6 member is readable but the retained data and P/Q syndromes disagree, what does Linux MD actually know, what does `check` retain as evidence, and what does `repair` choose to rewrite?

This slice is intentionally **not** a new history of RAID6. Case 94 already grounds the 1993–1994 P+Q / RAID Level 6 formulation and the distinction between two known erasures and arbitrary silent corruption. The material below uses current Linux MD implementation and mdadm documentation as a later implementation witness for that distinction.

Labels used below:

- `H/P` — historical/primary record already established by Case 94;
- `P` — present implementation/project documentation;
- `E` — engineering reconstruction;
- `A` — functional analogy;
- `I` — philosophical/project interpretation;
- `X` — explicit non-claim.

---

## Source ledger

### S1 — current Linux RAID5/6 implementation (`P`)

- Project: Linux kernel.
- File: `drivers/md/raid5.c`.
- Inspected commit: `587858367581b9c55c3690f4e63382ad622719d4`.
- Relevant function: `handle_parity_checks6()`.
- URL: <https://github.com/torvalds/linux/blob/587858367581b9c55c3690f4e63382ad622719d4/drivers/md/raid5.c>.

Relevant implementation facts:

- the RAID6 path separately tests P and Q consistency;
- when the check reports no syndrome mismatch, the stripe can be marked in-sync, subject to any actual failed-device writeback still required;
- when a mismatch exists, Linux increments `resync_mismatches`;
- if the operation is `MD_RECOVERY_CHECK`, it explicitly does **not** repair the mismatch;
- if repair is requested, the code schedules recomputation of P and/or Q according to which syndrome checks failed;
- the recomputation targets are the P and Q devices (`pd_idx`, `qd_idx`), not an inferred arbitrary data-device location.

### S2 — current Linux MD sysfs documentation (`P`)

- Project: Linux kernel.
- File: `Documentation/admin-guide/md.rst`.
- Same inspected commit: `587858367581b9c55c3690f4e63382ad622719d4`.
- URL: <https://github.com/torvalds/linux/blob/587858367581b9c55c3690f4e63382ad622719d4/Documentation/admin-guide/md.rst>.

Relevant records:

- `sync_action=check` requests a full redundancy check;
- `sync_action=repair` requests a full check and repair similar to resync;
- `mismatch_count` counts sectors rewritten, or for `check`, sectors that would have been rewritten;
- the count is coarse because MD commonly processes units larger than one sector.

### S3 — mdadm `md(4)` project manual (`P`)

- Project: md-raid-utilities/mdadm.
- File: `md.4`.
- Inspected main-head context: current repository state around commit `3ad8dbf814c2e659450c1e699aa634f2eebff6ce` (10-Sep-2026).
- URL: <https://github.com/md-raid-utilities/mdadm/blob/main/md.4>.

Relevant records:

- scrubbing reads all blocks and checks consistency;
- for RAID4/5/6, consistency checking means checking the parity block or blocks;
- a **read error** invokes normal read-error recovery, which can reconstruct the data from other devices and write it back to the device whose read failed;
- a **mismatch with successful reads** is treated differently: `check` records it without repair, while `repair` follows resync behavior;
- for RAID5/RAID6, that mismatch-repair behavior writes **new parity blocks**;
- `mismatch_cnt` is not a precise count of corrupt sectors because it is incremented at the I/O-unit granularity used by MD.

### S4 — H. Peter Anvin, _The mathematics of RAID-6_ (`H/P`, inherited from Case 94)

- First version: 20-Jan-2004; last updated 20-Dec-2011.
- URL: <https://www.kernel.org/pub/linux/kernel/people/hpa/raid6.pdf>.

Case 94 already uses Anvin's note to ground the historical/mechanistic distinction:

- two known failed positions can be reconstructed from P+Q;
- arbitrary dual corruption is not generally locatable/recoverable merely because P and Q exist.

This deepening does not duplicate the algebra; it asks how a deployed software RAID implementation acts when the location signal differs.

---

## Claim-by-claim grounding

### C1 — Linux MD distinguishes a read failure from a parity mismatch (`P`)

The mdadm manual describes two different scrub situations.

If a device returns a **read error**, the device/request path has supplied fault-location information: MD can reconstruct the desired block from the remaining redundancy, write the recovered value back to the device that failed the read, and then re-read it.

If all member reads succeed but the values do not satisfy the redundancy relation, MD calls the condition a **mismatch**.

That gives a precise operational split:

```text
read failed at a known member/location
    -> failure location supplied by I/O error
    -> reconstruct that member's block
    -> attempt writeback there

all reads succeeded but P/Q relation disagrees
    -> inconsistency detected
    -> corrupt data location not established merely by the mismatch
```

Engineering conclusion (`E`):

> **detecting inconsistency != locating the corrupt embodiment**.

This is exactly the kind of typed information boundary that Case 94's P+Q equations require.

### C2 — `check` preserves evidence of disagreement without choosing a repair authority (`P/E`)

For a scrub requested with `check`, the current RAID6 implementation increments the mismatch counter and explicitly follows the `don't try to repair!!` branch.

The stripe is allowed to move past the check after the mismatch has been recorded; the operation does not attempt to infer a bad data disk merely from the failed P/Q relation.

The retained diagnostic artifact is correspondingly weak but useful:

```text
there was an inconsistency in this checked range
```

It is **not**:

```text
member N definitely contained the wrong data
```

or:

```text
exactly K physical sectors were corrupt
```

The kernel documentation states that `mismatch_count` can overstate the number of actual erroneous sectors because MD accounts in larger units.

Therefore:

> **mismatch evidence != corruption-location evidence**

and:

> **mismatch count != exact corruption cardinality**.

### C3 — `repair` of a readable RAID5/6 mismatch makes parity conform to the read data (`P`)

The mdadm project manual states that for RAID5/RAID6, mismatch repair writes new parity blocks.

The inspected RAID6 kernel source makes that policy concrete. When the P syndrome check fails, `handle_parity_checks6()` schedules recomputation of `pd_idx`; when Q fails, it schedules recomputation of `qd_idx`. If both fail, both parity targets can be scheduled. The code does not use the syndrome mismatch alone to select an arbitrary data member as corrupt and overwrite it.

So, for the bounded **all-reads-successful mismatch** path:

```text
surviving readable data blocks
    -> treated as inputs
    -> recompute failed P and/or Q relation
    -> write parity target(s)
```

This is a repair-authority choice, not an algebraic proof that the readable data were semantically correct.

Engineering conclusion (`E`):

> **repair can restore codeword consistency without proving that the chosen surviving data were the intended payload**.

### C4 — known read failure and silent readable corruption create different recovery authority (`E`)

The same array can therefore react differently to two faults affecting the same physical sector contents:

1. if the device reports the sector unreadable, location evidence allows MD to reconstruct that member's data and try to write it back;
2. if the device returns a plausible but wrong sector, parity/syndrome comparison can reveal disagreement without necessarily establishing which readable input is wrong;
3. `repair` then recomputes parity from the readable data rather than claiming to have diagnosed the data member.

This is a strong operational witness for Case 94's central distinction:

> **erasure-location knowledge is constitutive recovery state**.

The extra state need not be a persistent metadata field. It can be supplied at recovery time by the I/O failure itself.

### C5 — two parity equations increase detectability without automatically creating a trustworthy truth source (`E`)

P and Q give Linux RAID6 two relations to test. The source tracks `SUM_CHECK_P_RESULT` and `SUM_CHECK_Q_RESULT` separately and can recompute either or both parity blocks.

But the existence of two failed checks does not automatically establish that both parity devices are physically wrong. A silent data error can also make the parity relations fail because the current readable data no longer satisfy the retained syndromes.

Thus:

> **more independent redundancy relations != automatic source-of-truth identification**.

This does not reduce the value of P+Q. It specifies the fault model in which that redundancy safely supports reconstruction.

### C6 — `mismatch_cnt` is retained maintenance evidence, not payload and not a forensic map (`P/E`)

The sysfs counter reports the amount of address space associated with detected/repaired mismatches at MD's processing granularity. It is useful operational evidence that a consistency pass found trouble.

It does not retain:

- the old payload bytes;
- a cryptographic checksum per data block;
- which readable member was wrong;
- a precise list of every corrupt sector;
- a proof that the post-repair payload matches application intent.

Therefore it belongs in the repository's control/evidence layer:

```text
payload state
    != parity relation
    != mismatch-detection evidence
    != fault-location evidence
    != repair authority
```

### C7 — current Linux `check` can still write when an actual read error occurs (`P`)

A potentially misleading shortcut is that `check` is always read-only.

The mdadm manual explicitly says a scrub-time read error invokes normal read-error recovery, which may reconstruct and write the recovered block back to the device. The no-repair rule applies to the **successful-read parity mismatch** branch, not to all possible events encountered during the traversal.

Therefore:

> **`sync_action=check` != universal no-write guarantee**.

This matters because a maintenance label is not enough to infer every side effect; the triggering evidence class changes what recovery is authorized to do.

### C8 — restoring P/Q consistency is a scoped completion condition (`E`)

After `repair`, the RAID stripe may again satisfy its P/Q equations. That proves a narrower relation than end-to-end data correctness.

Safe statement:

```text
post-repair stripe satisfies MD's redundancy relation
```

Unsafe upgrade:

```text
post-repair application payload is proven historically correct
```

Without an independent checksum, higher-layer semantic witness, or known failed position, the parity equations alone do not supply that proof.

This is why checksummed storage systems belong in a separate comparison rather than being silently imported into Linux MD RAID6.

---

## Retained-state decomposition

This slice sharpens Case 94 into at least seven distinct state/evidence classes:

1. **user data blocks** — application payload embodiments;
2. **P syndrome** — first redundancy relation;
3. **Q syndrome** — second redundancy relation;
4. **member/stripe position relation** — tells the Q algebra which coefficient belongs to which contribution;
5. **fault-location evidence** — for example, the fact that a read failed on a particular member/address;
6. **consistency-test evidence** — P/Q mismatch observations and `mismatch_cnt` accounting;
7. **repair-policy authority** — the rule deciding whether to leave a mismatch recorded, reconstruct a known failed member, or regenerate parity.

The important new distinction is between items 5 and 6.

```text
syndrome disagreement says "these retained relations cannot all be true together"

fault-location evidence says "this particular embodiment is the one recovery may replace"
```

Those are not the same fact.

---

## Failure / forgetting boundaries

### 1. Silent data corruption with readable media

All drives answer reads, but a data block differs from the state against which P/Q were generated. Scrub can detect a mismatch, yet the bounded MD path does not thereby know which readable data member is wrong.

### 2. Parity corruption

Readable data may still be right while P and/or Q are wrong. In this case parity regeneration from data is the intended corrective direction.

### 3. Ambiguous readable mismatch

The observable syndrome failure is compatible with more than one physical cause. Running `repair` makes a policy choice about authority; it does not manufacture historical evidence that was absent.

### 4. Known read failure

The I/O subsystem supplies a failed member/address relation. MD can use the remaining redundancy to reconstruct that known erasure and write the result back.

### 5. Coarse diagnostic accounting

`mismatch_cnt` records that a region required or would require rewrite at MD's work-unit granularity. It must not be interpreted as an exact forensic inventory.

### 6. Consistent but wrong state

If data and parity are changed coherently, ordinary parity checking can report a valid codeword even though the logical payload is not what an application intended. Algebraic consistency is not semantic authenticity.

---

## Historical record vs present implementation

This deepening deliberately keeps two time layers separate.

### Historical record already grounded by Case 94 (`H/P`)

- 1993/1994: Chen et al. describe P+Q / RAID Level 6 and protection from two disk failures;
- 2004/2011: Anvin gives the P/Q recovery mathematics and explicitly discusses the limit of arbitrary corruption diagnosis.

### Present implementation witness added here (`P`)

- current Linux MD exposes `check` and `repair` maintenance actions;
- current RAID6 code tests P and Q separately;
- current mismatch repair recomputes parity targets rather than inferring an arbitrary bad data member;
- current mdadm documentation distinguishes read-error recovery from all-readable mismatch handling.

No claim is made that the exact 2026 `raid5.c` state machine or sysfs vocabulary existed in 1993, 2004, or every intervening Linux release.

---

## Engineering reconstruction

The bounded operational logic can be expressed as:

```text
P/Q consistency test
    -> if consistent: no parity mismatch evidence
    -> if inconsistent:
         retain mismatch evidence
         + ask whether there is independent fault-location evidence

known failed position
    -> reconstruct that known erasure

no known failed position; all reads successful
    -> `check`: record disagreement, do not choose data victim
    -> `repair`: regenerate failed parity relation(s) from readable data
```

This yields a general but still engineering-level conclusion:

> **redundancy can preserve enough information to detect that retained embodiments disagree without preserving enough information to identify which one deserves authority.**

That is a stronger and more precise statement than saying merely that RAID6 can survive two drive failures.

---

## Functional comparison

### Case 18 — ZFS scrub (`A`)

Both cases concern proactive integrity traversal, but the authority basis differs. ZFS combines redundancy with end-to-end checksums and therefore can sometimes use checksum validity to identify a bad replica/block. Linux MD P+Q parity alone does not receive that independent per-block truth signal in the bounded path.

Safe comparison:

> **scrub traversal != identical fault-localization authority**.

No implementation genealogy is implied.

### Case 27 — Ceph EC scrub (`A`)

Both coded systems can discover inconsistency among redundant representations. Ceph's object/checksum/PG authority relations are different from MD's local stripe parity relation. The similarity is only that repair needs more than the abstract fact that redundancy exists.

### Case 88 — Linux MD PPL (`A`)

PPL concerns write-hole/currentness evidence. This slice assumes the stripe is being checked and asks which currently readable contribution should be trusted after an inconsistency is found.

Therefore:

> **parity currentness evidence != corruption-location evidence**.

### Case 17 — single-parity RAID (`A/E`)

The same mismatch-versus-location distinction exists with one parity syndrome. RAID6 adds another independent relation and more known-erasure capacity, but it does not automatically turn parity into end-to-end provenance.

---

## Philosophical / media-theoretical interpretation

A bounded project-level interpretation follows:

> A technical system may retain evidence of contradiction without retaining enough evidence to resolve the contradiction.

In Case 94, P and Q can jointly say that the present stripe embodiments do not belong to one valid coded state. That retained contradiction is operationally meaningful: it can trigger counters, warnings, or maintenance.

But contradiction alone does not necessarily identify the historically correct payload. Repair therefore contains an **authority rule** in addition to an algebraic operation.

Boundary: Linux developers do not present this as a philosophy of memory, testimony, or truth. The interpretation is downstream of the implementation evidence.

---

## Explicit non-claims

1. `X` — Linux MD RAID6 cannot detect any silent corruption. False; P/Q checks can detect inconsistency.
2. `X` — any nonzero `mismatch_cnt` tells exactly which disk is corrupt. Not established.
3. `X` — `mismatch_cnt` is an exact count of bad physical sectors. Contradicted by MD's coarse accounting description.
4. `X` — `repair` proves the data blocks were correct. It restores the parity relation chosen by the implementation.
5. `X` — every parity mismatch means the parity devices were physically faulty. A bad data contribution can also break the relation.
6. `X` — `check` is guaranteed never to write. Read-error recovery can write back reconstructed data.
7. `X` — two P/Q syndrome failures identify two corrupt data disks. The bounded sources do not establish that inference.
8. `X` — Linux MD's present repair policy is required by RAID6 mathematics. It is an implementation/policy choice consistent with the documented fault model.
9. `X` — end-to-end checksums are unnecessary because RAID6 has Q. Not supported.
10. `X` — ZFS scrub and Linux MD scrub are the same mechanism. They have different integrity metadata and repair authority.
11. `X` — a post-repair codeword is guaranteed to equal the application-intended historical state. Not established by parity consistency alone.
12. `X` — current `raid5.c` is direct evidence for 1993 Berkeley implementation behavior. It is explicitly a later implementation witness.
13. `X` — two-known-erasure recovery and two-unknown-corruption repair are equivalent problems. Case 94 and this deepening show the opposite.
14. `X` — a readable device is necessarily correct. Readability is weaker than integrity.
15. `X` — parity regeneration physically erases every stale/corrupt embodiment elsewhere. It only updates the targeted array blocks.

---

## Claim ledger

| Claim | Label | Support | Boundary |
| --- | --- | --- | --- |
| Linux MD distinguishes scrub-time read errors from all-readable parity mismatches | `P` | mdadm `md(4)` | present project behavior, not universal RAID semantics |
| `check` records RAID6 syndrome mismatch without repairing that mismatch | `P` | `raid5.c` `MD_RECOVERY_CHECK` branch | actual read errors can still trigger writeback recovery |
| `repair` recomputes mismatched P and/or Q blocks | `P` | mdadm manual + `handle_parity_checks6()` targets `pd_idx`/`qd_idx` | not proof that data inputs are historically correct |
| P and Q are checked independently in the current RAID6 path | `P` | `SUM_CHECK_P_RESULT`, `SUM_CHECK_Q_RESULT` | implementation detail may change |
| `mismatch_cnt` can exceed the exact number of bad sectors | `P` | Linux MD documentation / mdadm manual | counter remains useful maintenance evidence |
| known failed location changes what recovery is authorized to overwrite | `E` | read-error path versus mismatch path | project reconstruction |
| syndrome disagreement is weaker than corruption-location evidence | `E` | source behavior + Case 94 algebra | project vocabulary |
| restored parity consistency proves application-level correctness | `X` | not established | needs independent integrity/provenance evidence |
| current Linux MD scrub is historical evidence for 1993 RAID6 | `X` | time-layer mismatch | present implementation witness only |

---

## What this closes

For Case 94, this slice closes the narrow open item **`checksummed RAID-6 fault-location/repair protocols` only at its Linux-MD negative-control edge**:

- Linux MD provides a concrete non-checksummed P+Q operational witness;
- a known read failure provides location evidence and permits data reconstruction/writeback;
- an all-readable syndrome mismatch provides inconsistency evidence but not automatic data-victim identification;
- `check` preserves the mismatch as maintenance evidence;
- `repair` restores the P/Q relation by rewriting parity, which is not the same as proving payload truth.

It does **not** yet close the positive checksummed-RAID side of that open item. A future bounded slice may compare a named checksummed RAID implementation where an independent checksum supplies the missing fault-location/admissibility evidence.

---

## Remaining debt

- add a positive checksummed RAID6/RAIDZ-style source-level contrast only if it can be kept separate from existing ZFS scrub cases;
- trace the historical introduction of MD `check`/`repair` and mismatch accounting only if chronology is needed; current source is intentionally not backdated;
- perform fault-injection experiments that distinguish unreadable sectors, parity-only corruption, one readable data corruption, and multiple readable corruptions;
- record exact post-repair payload outcomes under those experiments rather than inferring them from `mismatch_cnt` alone;
- keep full RAID6/EVENODD/Reed–Solomon genealogy in `computing-archaeology` if developed.

---

## Related-repository boundary

A fresh search of `tmzncty/computing-archaeology` for `mismatch_cnt` / RAID6 scrub found no dedicated module to reuse. This file therefore retains only the retention-specific evidence/authority distinction.

A broad history of Linux MD scrubbing, RAID administration, parity repair policy, or checksum-enabled array designs belongs in `computing-archaeology` rather than being duplicated here.
