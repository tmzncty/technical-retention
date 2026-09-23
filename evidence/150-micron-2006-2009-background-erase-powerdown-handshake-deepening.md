# Evidence 150 — Micron 2006–2009 Background-Erase / Power-Down Handshake Deepening

## Status

**`bounded deepening complete`**

This evidence slice deepens [Case 150](../cases/150-crucial-m550-active-garbage-collection.md) without attributing undocumented internals to the Crucial M550.

It adds a pre-M550, first-party Micron design record for a narrower retention question:

> **Can erase/reclamation work be deliberately deferred into a lower-contention interval while retaining an explicit runtime indication that the erase obligation is still pending or executing, and can planned power removal be conditioned on that obligation's completion?**

The primary artifact is Frankie Roohparvar, **“Method and apparatus for improving storage performance using a background erase,”** U.S. Patent **US7564721B2**, filed 25 May 2006, application publication **US20070274134A1** on 29 November 2007, granted 21 July 2009, original assignee **Micron Technology, Inc.**

Primary inspection source:

<https://patents.google.com/patent/US7564721B2/en>

This is **historical / first-party patent prior art**. It is not treated as evidence that Micron shipped this exact design in a particular commercial product, and it is not treated as evidence for the proprietary M550 firmware, Marvell controller microcode, or a direct genealogy into the 2014 M550.

---

## 1. Why this slice matters

Case 150 already separates several relations:

```text
host deletion / overwrite
    != deallocation / invalidity knowledge
    != garbage-collection execution
    != physical erase
    != reusable free capacity
```

Existing evidence also shows that Crucial's maintained support guidance treats **powered idle time** as a useful maintenance opportunity, while IBM 2009-priority controller evidence separates invalidity, live-data movement, mapping update, and later erase.

What was still missing was a period, first-party Micron record that exposes the **control state around deferred erase itself**:

```text
erase obligation exists
    != erase is executing now
    != erase is complete
    != planned power removal is safe now
```

US7564721B2 supplies that bounded control-plane witness.

---

## 2. Source role and claim classes

### Historical record (`H/P`)

The patent directly documents a Micron-assigned proposed design using:

- block erase;
- copying retainable information before erasing a mixed block;
- logical-to-physical address mapping in one illustrated software organization;
- tracking blocks that contain invalid/old locations;
- moving still-good pages before erasing a dirty block;
- a `background-process-busy` indication;
- a `power-down-soon` indication;
- delayed/background erase during idle opportunities;
- a handshake in which power removal waits for pending erases to finish.

### Engineering reconstruction (`E`)

This record reconstructs the relation between:

- **reclamation/erase obligation**;
- **maintenance opportunity**;
- **erase execution**;
- **completion evidence**;
- **power-removal authority**.

These are project terms. They are not claimed as Micron's period vocabulary.

### Functional analogy (`FA`)

The design is compared with later Case-150 Crucial/M550 evidence and with the IBM managed-SSD prior-art slice only at the level of function. No implementation identity or descent is asserted.

### Philosophical interpretation (`A`, bounded)

The only interpretive claim retained here is that an apparently inactive interval can be operationally allocated to finishing a lower-layer obligation, and that the authority to withdraw power can depend on a completion relation rather than merely on elapsed wall-clock time.

---

## 3. Historical record — erase can require preserving live information first

The patent's background begins from block-erase geometry. It states that a block erase can stall reads and writes and that, when some information in a block must be retained while other information is removed, the retainable information may need to be copied to another block before erase.

This supports a bounded sequence already central to Case 150:

```text
mixed block
    -> preserve still-needed information elsewhere
    -> erase old block
```

The source therefore does not describe erase as a free-standing act of destruction. In the relevant mixed-block case, erase presupposes a prior distinction between what remains current and what may be retired.

---

## 4. Historical record — mapping and housekeeping appear in the same design context

One illustrated software organization contains a flash driver with `address mapping` and `flash control`. The patent states that address mapping converts logical-domain addresses from the file system to physical-domain locations in the memory device.

Later, the patent describes data management that can track how “dirty” a block has become, move pages containing good data to another block, optionally pack good data together, and erase the old block only after the good data have been moved.

This is not a complete FTL specification, but it is enough to preserve three historical distinctions:

```text
logical designation
    != current physical location
    != old block's reclamation state
```

and:

```text
dirty / reclaim candidate
    != immediately erasable without preserving good data
```

The source does not specify an M550 mapping format, SSD logical-page table, NAND metadata layout, or power-fail journal.

---

## 5. Historical record — `background-process-busy` can cover pending as well as executing work

The patent describes a `background-process-busy` flag whose meaning can include background erase **in progress or waiting to execute**.

In process 600, an erase command may be accepted while background erase is enabled, after which the implementation can wait for a time-delay event. The listed delay events include:

- a predetermined delay;
- a subsequent command;
- a predetermined number of idle bus cycles;
- or, in another embodiment, receipt of `power-down-soon`.

The patent explicitly says the delay can be selected to wait until the memory device is idle so that erase does not unnecessarily contend with other operations.

Therefore the historical state machine contains a real intermediate state:

```text
erase command / obligation accepted
    -> pending background work
    -> delay / idle opportunity
    -> erase execution
    -> completion indication
```

That intermediate state blocks a common simplification:

```text
erase requested
    != erase already performed
```

It also means the word `background` should not be read as `costless`. The operation is still performed; its timing is moved relative to other work.

---

## 6. Historical record — completion is represented separately from admission

After the delay event, process 600 asserts the busy indication if needed, performs pending erase cycles, and then negates the busy indication after those erase cycles finish.

The patent makes the intended handshake explicit: an agent that issued the erase command can wait for the busy indication to become negated in order to determine that the erase commands have actually been executed.

For this described protocol:

```text
erase command accepted
    != erase completion

busy / pending-or-running
    != done

busy negated after erase
    -> runtime completion witness for this handshake
```

The phrase **runtime completion witness** is a project reconstruction. The source itself speaks in terms of the flag and the agent determining that erase commands have been executed.

This evidence does **not** establish that the flag is persisted in nonvolatile metadata or that it survives a controller reset.

---

## 7. Historical record — planned power removal is gated by pending erase

Process 700 is specifically described for memory systems that cycle power frequently.

The requester asserts `power-down-soon`. The executor then checks whether background erase is enabled and whether erase commands are pending. If work is pending, the executor asserts `background-process-busy`; the patent describes that state as indicating that it is **not yet safe to remove power**.

The pending erase operations are then performed. Afterward the busy indication is negated, and the patent states that power may then be removed safely in the sense relevant to the described erase commands.

The claims preserve the same relation. Claim 32 specifies removing power after negating the busy indication, while claim 34 describes the `power-down-soon -> pending? -> busy -> erase -> busy negated` sequence and claim 38 again conditions power removal on detecting the negated state.

The bounded historical relation is therefore:

```text
planned power removal requested
    + pending erase work
        -> power removal temporarily withheld
        -> erase performed
        -> busy negated
        -> planned power removal may proceed
```

This is stronger than merely saying that idle time is useful. It exposes a control relation in which a lower-layer maintenance obligation can temporarily withhold power-removal authority.

---

## 8. Historical record — sudden power removal remains a different failure class

The patent's own problem statement warns that, in transient-power systems, the exact time of power removal may be unpredictable. It states that removing power while a block is being erased can leave that block not fully erased even though the system believes it has been erased; a later program operation may then fail to write data correctly.

This warning is essential because it prevents the handshake from being over-generalized.

The source distinguishes at least two situations:

```text
coordinated / announced power-down
    -> pending erase can be drained before power removal

unpredictable power removal during erase
    -> block may be incompletely erased
    -> system belief can diverge from physical state
```

Accordingly:

```text
planned-power-down completion protocol
    != arbitrary sudden-power-loss recovery protocol
```

The latter remains an open Case-150 debt for the named M550.

---

## 9. Engineering reconstruction — five distinct authority states

The Micron design is useful because it makes five states analytically separable.

### 9.1 Erase/reclamation obligation

An erase command has been accepted, or a block has reached a state in which erase should eventually occur.

This does not imply execution.

### 9.2 Maintenance opportunity

A delay event, idle interval, or announced future power-down creates an interval in which deferred erase may be scheduled.

This does not imply that erase has completed.

### 9.3 Execution state

The erase cycle is actually in progress.

This matters because interruption during this state is explicitly hazardous in the patent's problem statement.

### 9.4 Completion evidence

The busy indication is negated after erase completion in the described handshake.

This allows another actor to distinguish unfinished from finished work without directly measuring cell thresholds.

### 9.5 Power-removal authority

In the planned-power-down path, the requester is allowed to proceed only after the completion relation is satisfied.

The resulting chain is:

```text
erase obligation
    -> wait for usable maintenance opportunity
    -> execute erase
    -> publish completion in the handshake
    -> permit planned power withdrawal
```

This is an engineering decomposition of the documented behavior, not Micron's conceptual terminology.

---

## 10. Engineering reconstruction — “idle” is a scheduling condition, not a persistence property

The patent can defer erase until a number of idle bus cycles have occurred. Therefore:

```text
host / bus idle
    != block erased
    != reclaim obligation discharged
```

Idle time is one possible **opportunity condition**. Whether work is pending, enabled, and ultimately completed are separate facts.

This directly complements the later Crucial support evidence in Case 150, which also treats powered idle as maintenance opportunity rather than as proof of maintenance completion.

But chronology does not establish a direct design lineage from the 2006 patent into the 2014 support behavior.

---

## 11. Engineering reconstruction — a runtime flag is not a crash-persistent checkpoint

The patent's busy/done relation is strong evidence for an online completion protocol. It does not establish a durable checkpoint that survives loss of the executor itself.

The source inspected here does not show:

- nonvolatile storage of the busy flag;
- a journal for partially completed erase work;
- a reset-time scan that rediscovers an interrupted erase;
- a generation counter or transaction record pairing mapping state with erase completion;
- a restart rule for distinguishing a never-started erase from a torn erase;
- an M550-specific recovery path.

Therefore:

```text
runtime completion evidence
    != restart-persistent completion evidence
```

and:

```text
graceful drain before power-off
    != crash recovery after unannounced power loss
```

This distinction is the central negative result of the slice.

---

## 12. Functional comparison — later Crucial powered-idle support

Case 150's Crucial support evidence says that Active Garbage Collection benefits from a long period in which the SSD is powered but not actively serving ordinary reads/writes.

The Micron patent is a useful earlier functional comparator because it also makes idle time a possible background-erase scheduling condition.

What can safely be compared:

```text
foreground inactivity
    can create lower-layer maintenance opportunity
```

What cannot safely be inferred:

- the 2014 M550 implements US7564721B2;
- M550 exposes the patent's flags;
- M550 waits for the same number of idle cycles;
- the modern Crucial 6–8-hour runbook descends from this patent;
- the M550 uses the same power-down handshake.

Thus this is **functional analogy plus same-company prior art**, not established genealogy.

---

## 13. Functional comparison — IBM 2009-priority validity/map/erase witness

The existing Case-150 IBM evidence answers a different question. It exposes a managed-SSD sequence in which invalidity metadata drives victim choice, valid data are recovered/re-stored, the LBA/PBA map is updated, and old blocks become erasable, with erase allowed immediately or later.

The Micron record adds a complementary control question:

```text
IBM witness:
    when does an old block become logically/operationally eligible for later erase?

Micron witness:
    once erase is pending, how can execution be deferred and completion coordinated with planned power removal?
```

Combining them functionally yields a richer decomposition:

```text
reclaim eligibility
    != scheduled erase obligation
    != maintenance opportunity
    != erase execution
    != completion evidence
    != safe planned power withdrawal
```

No IBM→Micron or Micron→IBM genealogy is claimed.

---

## 14. Functional comparison — mapped Flash / Case 04

Case 04 grounds the broader separation between logical identity/currentness, physical embodiment, and later erase/reclamation.

The Micron patent likewise contains logical-to-physical mapping in one illustrated software organization and describes copying retainable/good information before erasing a block.

The safe comparison is structural:

```text
logical/current data continuity
    can require new physical embodiment
    before old erase-container retirement
```

The source does not show that the Case-04 1990s systems evolved directly into this Micron design, and this slice does not reopen the broader FTL genealogy.

---

## 15. Philosophical interpretation — bounded

The technically interesting point is not that “background” work is invisible.

It is that **apparent inactivity at one interface can be allocated as completion time for a lower-layer obligation**, and that another action — here planned power removal — may remain unavailable until that obligation has been discharged.

The system therefore retains not only payload state but also a temporary relation of unfinished work:

```text
this block still requires erase before the planned transition may safely finish
```

That relation is operational rather than archival. It can disappear once the erase completes.

Nothing here licenses a general equation between technical garbage collection and human forgetting, nor between power withdrawal and philosophical absence.

---

## 16. Explicit non-claims

This evidence does **not** establish that:

1. Crucial or Micron invented background erase or SSD garbage collection.
2. US7564721B2 was commercially deployed as described.
3. The Crucial M550 implemented this patent.
4. The M550 used the patent's `background-process-busy` or `power-down-soon` flags.
5. The M550's Marvell controller executed the illustrated state machine.
6. A direct genealogy from this patent to the M550 has been established.
7. `background-process-busy` is a nonvolatile or reset-surviving checkpoint.
8. Busy negation proves arbitrary crash consistency.
9. Busy negation proves sanitization or forensic erasure of every stale embodiment.
10. The power-down handshake protects against unannounced power loss.
11. An incompletely erased block is automatically detected after restart.
12. The patent specifies a journal or transaction protocol for mapping updates plus erase.
13. Idle time alone guarantees erase execution.
14. Background erase can run in every low-power state.
15. SATA DevSleep semantics are described by this 2006 filing.
16. The patent's memory-card examples are equivalent to a later SATA SSD.
17. The `dirty` terminology maps one-to-one onto a modern SSD's proprietary validity metadata.
18. The described house-cleaning sequence gives the exact M550 victim-selection policy.
19. Erasing one reclaimed block is equivalent to whole-device sanitize.
20. The 2006 filing date is an invention-priority claim for the general idea of flash reclamation.

---

## 17. Claim ledger

| Claim | Type | Strength | Boundary |
| --- | --- | --- | --- |
| Micron was original assignee of the 2006-filed US7564721 family | historical record | strong | patent metadata; not commercial-deployment proof |
| Patent describes copying retainable information before block erase | historical record | strong | mixed-block background/problem statement |
| Patent includes logical-to-physical address mapping in an illustrated software organization | historical record | strong | does not establish an M550 FTL |
| Patent describes moving good pages before erasing a dirty block | historical record | strong | proposed design, not product proof |
| Background erase can be delayed toward idle time | historical record | strong | explicit process-600 description |
| Busy may denote pending or executing erase | historical record | strong | explicit controller description |
| Busy negation follows erase completion in the handshake | historical record | strong | explicit process + claims |
| Planned power removal can wait on pending erase completion | historical record | strong | process 700 + claims 32/34/38 |
| Sudden power loss during erase may leave a block incompletely erased | historical record | strong | explicit problem statement |
| Runtime completion evidence and crash-persistent recovery evidence are distinct | engineering reconstruction | strong | source exposes former, not latter |
| M550 implemented this handshake | rejected | unsupported | no direct product/firmware source |
| This patent proves the M550 GC crash protocol | rejected | unsupported | named-product crash seam remains open |

---

## 18. Source ledger

### P1 — US7564721B2 / US20070274134A1 — primary manufacturer patent

Frankie Roohparvar, **“Method and apparatus for improving storage performance using a background erase.”**

- original assignee: Micron Technology, Inc.;
- U.S. filing / priority: 25 May 2006;
- application publication: 29 November 2007;
- patent grant publication: 21 July 2009.

Google Patents HTML inspected:

<https://patents.google.com/patent/US7564721B2/en>

Relevant anchors in the rendered text include:

- background/problem discussion of block erase, live-information copying, and interruption during erase;
- FIG. 3A / FIG. 5 discussion of background flags and address mapping;
- housekeeping discussion of dirty blocks and moving good pages before erase;
- FIG. 6 process 600 for idle/delayed erase and busy completion;
- FIG. 7 process 700 for planned power-down coordination;
- claims 1, 6, 24, 30, 32, 34, and 38.

The Google Patents page is used as a convenient page-preserving/rendered legal-document host. This slice does not claim independent USPTO archival-PDF inspection.

---

## 19. Related-repository check

A fresh code search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `background erase` and for `Micron` returned no reusable dedicated packet in this run. The search endpoint reported incomplete indexing, so this is a conservative **no reusable match found**, not proof that the repository contains no related sentence anywhere.

Accordingly, this file keeps only the retention-specific control boundary. Broad flash-controller genealogy, commercial memory-card adoption, Micron product history, SSD firmware lineage, and background-operation standards evolution remain better suited to `computing-archaeology` if pursued.

---

## 20. Debt closed and debt retained

### Closed by this slice

A conservative first-party Micron public floor now exists for all of the following in one 2006-filed design record:

```text
background erase can be deferred
    + idle time can be a scheduling opportunity
    + pending/executing erase can be exposed through a runtime busy relation
    + completion can be distinguished from admission
    + planned power withdrawal can wait for erase completion
```

This closes the narrow prior-art/control-state question.

### Still open

For **Case 150 / M550 specifically**, the important debts remain:

1. exact M550 victim-selection and mapping-publication protocol;
2. exact M550 behavior on sudden power loss during GC;
3. whether M550 retains a durable interrupted-GC checkpoint, reconstructs by scan, or uses another protocol;
4. named-device fault/power-cut traces around live-page relocation and erase;
5. exact M550 interaction between AGC and DevSleep/Partial/Slumber;
6. product-revision-specific scheduling behavior;
7. stronger 2010–2014 origin-hosted support-page provenance where available.

The case therefore remains **`grounded`**. This evidence does not justify a maturity promotion.