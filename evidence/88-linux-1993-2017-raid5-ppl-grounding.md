# Grounding Record — Case 88 Linux MD RAID5 Partial Parity Log

## Purpose

Ground [`cases/88-linux-md-raid5-partial-parity-log.md`](../cases/88-linux-md-raid5-partial-parity-log.md) without turning it into a generic RAID history.

The bounded claim is:

> **Linux MD PPL, merged for Linux 4.12 in 2017, persists compact partial-parity plus stripe-identification evidence before ordinary RAID5 member writes are released, so a later dirty-start recovery can restore a trustworthy parity relation in documented cases without retaining/protecting every in-flight user-data write.**

This record separates:

1. directly evidenced 2017 Linux mechanism;
2. earlier prior art that blocks invention claims;
3. engineering reconstruction;
4. functional analogy;
5. claims deliberately left unsupported.

---

## Source 1 — Linux upstream PPL implementation commit

**Type:** primary source, source code + commit message + contemporaneous added documentation.

**Citation:** Artur Paszkiewicz, `raid5-ppl: Partial Parity Log write logging implementation`, Linux commit `3418d036c81dcb604b7c7c71b209d5890a8418aa`, authored 9 March 2017, committed by Shaohua Li 16 March 2017.

**Locator:**
<https://github.com/torvalds/linux/commit/3418d036c81dcb604b7c7c71b209d5890a8418aa>

### Directly established

- The commit implements calculation of partial parity and PPL write logging for RAID5.
- It defines partial parity as the XOR relation over stripe data chunks not modified by the write.
- It distinguishes reconstruct-write and read-modify-write calculation paths.
- It requires partial parity to be computed while the relevant old data are still available.
- Added documentation says the problem addressed is the RAID5 write hole: after a dirty shutdown, parity can be inconsistent with surviving data, and a later degraded state can make ordinary recomputation impossible.
- Added documentation says partial parity is written **before** new data and parity are dispatched to the member disks.
- Added documentation calls PPL a `distributed log` stored in member metadata, on the parity drive for the relevant stripe.
- Added documentation says PPL is **not a true journal** and does not protect against loss of in-flight data; its narrower purpose is protection against silent corruption from the write hole.
- Added documentation says version-1 and external/IMSM metadata arrays can use PPL through `--consistency-policy=ppl`.
- The commit warns that volatile write-back cache on member drives must be disabled at that stage because cache-flush support needed to guarantee power-failure consistency had not yet been implemented.

### Source-code structure directly visible in the commit/current descendant

The implementation maintains:

- PPL header entries that identify affected stripe regions;
- parity-disk identity;
- partial-parity size and data size;
- entry checksums and header checksum;
- generation/sequence state;
- per-member child logs;
- partial-parity pages associated with stripe heads.

The current descendant remains in `drivers/md/raid5-ppl.c`, but current implementation details are not silently projected backward onto the 2017 merge.

### Bounded wording

`just enough data needed for recovering from the write hole` is Linux's documentation claim for partial parity in its stated recovery model. The project may reconstruct this as `recovery-sufficient evidence`, but that phrase is not historical Linux vocabulary.

---

## Source 2 — Linux 4.12 MD pull request

**Type:** primary/contemporary maintainer integration record.

**Citation:** Shaohua Li, `[GIT PULL] MD update for 4.12`, 1 May 2017.

**Locator:**
<https://lkml.iu.edu/hypermail/linux/kernel/1705.0/00532.html>

### Directly established

The pull request says the MD update includes:

- `Partial Parity Log (ppl)`;
- that the feature was `found in Intel IMSM raid array`;
- that it is `another way to close RAID5 writehole`;
- that the Linux implementation can also be used for normal RAID5 arrays when the relevant superblock bit is set.

### Limit

This is sufficient to say that the Linux maintainer described PPL as an existing Intel IMSM feature incorporated into Linux MD.

It is **not** sufficient to establish:

- the first Intel IMSM release containing PPL;
- the complete Intel firmware/on-disk history;
- a direct genealogy from any specific older parity-log paper or patent into Intel's design.

Those require separate history work, preferably in `tmzncty/computing-archaeology`.

---

## Source 3 — PPL patch-series cover letter

**Type:** primary/contemporary engineering discussion.

**Citation:** Artur Paszkiewicz, `[PATCH v4 0/7] Partial Parity Log for MD RAID 5`, 21 February 2017.

**Locator:**
<https://lwn.net/Articles/715280/>

### Directly established

The patch author describes PPL as:

- a RAID5 write-hole solution;
- an alternative to the existing `raid5-cache` mechanism;
- a distributed log stored on array-member metadata rather than a dedicated journal drive;
- a mechanism whose logging workflow/implementation reuses ideas from `raid5-cache` while retaining different stored evidence.

### Use in Case 88

This source supports the historical distinction:

`PPL ≠ raid5-cache journal`.

It also prevents the case from describing PPL as though Linux MD had only one write-hole closure technique in 2017.

---

## Source 4 — current Linux kernel PPL documentation

**Type:** first-party institutional documentation, later continuity witness.

**Locator:**
<https://docs.kernel.org/driver-api/md/raid5-ppl.html>

### Directly established

The maintained documentation still explains:

- parity inconsistency after dirty shutdown;
- degraded-state risk and silent corruption;
- partial parity as XOR of unmodified chunks;
- PPL recovery;
- member-local distributed-log placement;
- distinction from `raid5-cache` / a true journal;
- performance and metadata/version constraints.

### Limit

Current documentation/source may include behavior added after Linux 4.12. Historical claims about the initial implementation therefore use the 2017 commit as the decisive anchor.

---

## Source 5 — 1993 parity-logging research

**Type:** original academic technical paper / institutional archive.

**Citation:** Daniel Stodolsky, Mark Holland, Garth A. Gibson, `Parity Logging: Overcoming the Small Write Problem in Redundant Disk Arrays`, ISCA 1993, pp. 64–75.

**Institutional locator:**
<https://www.cs.cmu.edu/afs/cs/project/nectar-io/ftp/ParityLogging/ISCA93.abstract>

### Directly established

The 1993 work explicitly uses the term `parity logging` and applies journaling techniques to parity-encoded redundant disk arrays, especially to reduce the cost of small writes.

### Prior-art effect

This blocks any claim that Linux 4.12 introduced the general idea of `parity logging`.

### Limit

The paper's stated problem and mechanism are not automatically identical to Linux MD PPL. In particular, its historical focus is efficient small writes, whereas Case 88 is bounded to PPL's write-hole recovery semantics. The shared phrase/logging function is prior art, not proof of direct design lineage.

---

## Source 6 — Digital Equipment Corporation write-hole recovery patent

**Type:** primary patent prior art.

**Citation:** Clark E. Lubbers, Susan G. Elkington, Ronald H. McLean, `Enhanced raid write hole protection and recovery`, US5774643A, filed 13 October 1995, issued 30 June 1998; assignee Digital Equipment Corporation.

**Public metadata/abstract witness:**
<https://patents.google.com/patent/US20050066124A1/en> (later patent's background discussion identifies US5774643A and summarizes its non-volatile write-back-cache/metadata method).

### Directly established at bounded level

The earlier DEC patent describes RAID5 write-hole protection using non-volatile write-back cache plus metadata identifying outstanding writes/targets, so interrupted operations can be identified and parity consistency reconstructed after crash.

### Prior-art effect

This blocks any claim that Linux PPL invented RAID5 write-hole recovery or the use of retained auxiliary state to close the crash window.

### Limit

DEC's retained NVRAM payload/metadata and Linux PPL's distributed partial-parity record are not the same mechanism. No direct DEC → Intel IMSM → Linux genealogy is claimed.

---

## Source 7 — Case 17 / Chen et al. 1993–1994 parity-currentness boundary

**Type:** repository-internal reuse of already grounded original RAID literature.

**Locator:**
[`cases/17-raid-parity-reconstruction-degraded-repair.md`](../cases/17-raid-parity-reconstruction-degraded-repair.md)

### Already established there

Chen et al. describe crash-interrupted writes as capable of leaving parity inconsistent, and they make parity consistency plus reconstruction progress part of array `meta state`.

### Reuse rule

Case 88 does not repeat the broad RAID history. It narrows the later 2017 question to **how Linux PPL retains enough before-update evidence to make parity trustworthy after the non-atomic interval**.

---

## Claim audit

| Claim | Evidence class | Result |
| --- | --- | --- |
| Linux MD PPL was merged for the Linux 4.12 development cycle in 2017 | H/P | grounded by upstream commit + maintainer pull request |
| PPL logs partial parity before ordinary data/parity writes are dispatched | H/P | grounded by 2017 added documentation |
| partial parity is the XOR of data chunks not modified by the write | H/P | grounded by commit message/source/docs |
| PPL is distributed across member metadata, associated with the parity disk of the stripe | H/P | grounded |
| PPL protects write-hole parity consistency without protecting all in-flight user data | H/P | explicitly grounded by documentation |
| PPL is a true/full user-data write journal | X | explicitly rejected |
| PPL guarantees application-level atomic durability | X | rejected by documented limitation |
| physically present parity is always reconstructively trustworthy | X | rejected by write-hole definition |
| software ordering alone survives power loss through volatile member caches | X | rejected by initial cache warning |
| Linux invented parity logging | X | rejected by 1993 prior art |
| Linux invented RAID5 write-hole recovery | X | rejected by 1995-filed DEC prior art and earlier Case-17 consistency work |
| PPL directly descends from Stodolsky parity logging or DEC's patent | X | not established |
| Intel IMSM's exact PPL origin/version is known from these sources | X | not established |
| compact auxiliary state can be sufficient for a specific future recovery without duplicating complete payload | E | supported engineering reconstruction |
| temporary recovery evidence can become disposable once recovery closure is achieved | E/I | supported project interpretation, not Linux historical vocabulary |

---

## Cross-case boundary audit

### Case 17 — RAID parity reconstruction

Reuse, do not duplicate:

- parity/checksum reconstructability;
- degraded service;
- repair margin;
- parity/currentness meta state.

New in Case 88:

- a concrete 2017 pre-update PPL record;
- deliberate retention of **partial**, recovery-sufficient relation data;
- explicit distinction between closing parity corruption and protecting in-flight payload;
- explicit lower-layer volatile-cache caveat.

### Case 87 — SCSI cache completion / medium commitment

Functional comparison only. Case 87 gives earlier interface evidence that completion/cache residence/medium commitment differ. Case 88's 2017 cache warning shows why a higher-level logging order must cross a lower persistence boundary to survive power loss.

No direct SCSI → Linux PPL design genealogy is established.

### Case 74 — JBD revoke

Functional analogy only. Both preserve compact recovery-control evidence, but:

- JBD revoke suppresses replay of stale block images after reuse;
- PPL reconstructs/qualifies a parity relation after an interrupted multi-device update.

### Case 71 — ZooKeeper fuzzy snapshot

Functional analogy only. Both demonstrate that the recovery artifact need not itself be a complete instantaneous copy of desired final state. Their data models, ordering rules, and historical lineages differ.

---

## Related-repository audit

A pre-write search of `tmzncty/computing-archaeology` for `RAID`, `RAID parity write hole`, and PPL-specific terms returned no dedicated treatment.

Therefore:

- Case 88 keeps only the retention-specific mechanism/comparison here;
- a full RAID small-write / parity-logging / hardware-controller / Intel IMSM / Linux-MD genealogy should be added to `computing-archaeology` rather than expanded inside this case;
- any later discovery of prior art should update the genealogy claim here rather than destabilize the directly sourced 2017 Linux mechanism.

---

## Grounding decision

**Status: `grounded`.**

The bounded mechanism rests on first-party Linux source, original commit history, contemporaneous maintainer/patch discussion, and older primary/scholarly prior-art witnesses. The case's strongest synthesis claim remains deliberately narrow:

> **retention can consist of preserving a compact relation that is sufficient to keep later reconstruction trustworthy, even when the mechanism neither retains a full duplicate of the in-flight payload nor guarantees that payload's atomic survival.**
