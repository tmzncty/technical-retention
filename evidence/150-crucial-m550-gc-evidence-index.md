# Case 150 evidence index — Crucial M550 Active Garbage Collection and managed-SSD reclamation

**Case:** [`150 — Crucial M550 Active Garbage Collection`](../cases/150-crucial-m550-active-garbage-collection.md)  
**Current maturity:** `grounded`  
**Purpose:** evidence navigation, claim-layer separation, and bounded-debt tracking

## Why this index exists

Case 150 now has several evidence slices that all concern SSD cleanup, idle time, invalidity, free space, or erase, but they answer different questions.

They should not be collapsed into the statement that “an SSD deletes data in the background.”

The current evidence package separates:

```text
host retirement decision
    != deallocation / invalidity knowledge
    != reclaim eligibility
    != victim selection
    != live-data relocation
    != mapping/currentness publication
    != erase obligation
    != maintenance opportunity
    != erase execution
    != erase-completion evidence
    != reusable-capacity admission
    != sanitization
```

This index keeps those layers navigable and records what remains product-specific and unknown.

---

## Canonical case

### C150 — Crucial M550 Active Garbage Collection

[`../cases/150-crucial-m550-active-garbage-collection.md`](../cases/150-crucial-m550-active-garbage-collection.md)

The canonical case anchors the named product to Crucial's 29-Jan-2014 M550 flyer and Micron's 18-Mar-2014 launch record, while using maintained Crucial support material for the current family-level powered-idle maintenance contract.

Its bounded result is:

```text
logical retirement
    != physical reclamation

forgetting stale embodiments
    can require preserving / relocating still-live data
```

The canonical case deliberately does **not** reconstruct M550 proprietary firmware, Marvell 88SS9189 microcode, exact victim selection, exact OP layout, or the power-fail GC state machine.

---

## Evidence chain 1 — powered idle and maintenance eligibility

### E150-1 — Crucial powered-idle / sleep maintenance-opportunity boundary

[`150-crucial-powered-idle-sleep-maintenance-opportunity-deepening.md`](150-crucial-powered-idle-sleep-maintenance-opportunity-deepening.md)

**Question:** does the absence of foreground I/O itself prove that controller-local cleanup can run?

**Bounded result:** no. Maintained Crucial support guidance deliberately constructs a powered-idle window, while the M550 product flyer separately advertises Device Sleep. The evidence therefore separates:

```text
host idle
    != maintenance-eligible device state
    != maintenance scheduled
    != maintenance completed
```

It does not establish whether M550 GC can run in SATA DevSleep, Partial, or Slumber.

---

## Evidence chain 2 — support provenance and named-device observability

### E150-2 — 2013–2015 AGC provenance / Crucial m4 experiment

[`150-crucial-2013-2015-agc-provenance-experiment-deepening.md`](150-crucial-2013-2015-agc-provenance-experiment-deepening.md)

**Question:** how early can the public Crucial powered-idle wording be conservatively witnessed, and what can stale-data recovery on a named Crucial SSD actually prove?

**Bounded result:** contemporaneous 2013–2014 preservation witnesses move the public-circulation floor earlier, while a SecureComm 2014 m4 experiment shows path-dependent stale-data recovery. The experiment does not by itself distinguish mechanism absence from lack of discard eligibility, lack of scheduling, or incomplete erase.

```text
GC mechanism exists
    != pages eligible for reclamation
    != GC executed on those pages
    != old cells erased before observation
```

### E150-3 — 2013 support-page version provenance

[`150-crucial-2013-support-page-version-provenance-deepening.md`](150-crucial-2013-support-page-version-provenance-deepening.md)

**Question:** can a later support-page body be back-dated to the earliest date associated with the same named resource?

**Bounded result:** no. Page identity, revision metadata, and body-version identity remain separate.

```text
same page/resource identity
    != same body version
    != authenticated origin capture
```

This is historical-source discipline, not an SSD mechanism claim.

---

## Evidence chain 3 — host deallocation / read semantics

### E150-4 — shared T13 TRIM evidence from Case 04

[`04-t13-2007-2010-trim-logical-invalidation-read-semantics-deepening.md`](04-t13-2007-2010-trim-logical-invalidation-read-semantics-deepening.md)

**Question:** what changes at the host/device interface when a logical range becomes discardable, and does that prove physical erase?

**Bounded result:** the T13 proposal chain separates discardability notification and post-TRIM read semantics from later physical reclamation.

For Case 150 the reused result is:

```text
TRIM / deallocation delivered
    != GC execution
    != old NAND embodiment erased
    != sanitize completion
```

The standards chronology stays authoritative in the Case-04 evidence file rather than being duplicated here.

---

## Evidence chain 4 — controller validity, map publication, and later erase

### E150-5 — IBM 2009–2012 SSD GC validity / mapping / erase prior art

[`150-ibm-2009-2012-ssd-gc-validity-map-erase-prior-art-deepening.md`](150-ibm-2009-2012-ssd-gc-validity-map-erase-prior-art-deepening.md)

**Question:** can a manufacturer-authored managed-SSD design separate invalidity evidence, victim choice, live-data preservation, map/currentness publication, erase eligibility, and actual erase?

**Bounded result:** yes, for the IBM-described controller design.

The source exposes a sequence of the form:

```text
PI invalidity evidence
    -> select recycle target
    -> recover / re-store still-valid data
    -> update LBA/PBA map
    -> old block becomes erasable
    -> erase now or later
```

This is manufacturer prior art / control-architecture evidence. It is not an M550 implementation claim and not an IBM→Micron genealogy claim.

---

## Evidence chain 5 — reserved capacity / over-provisioning as maintenance headroom

### E150-6 — 2009–2012 over-provisioning / reserved-capacity deepening

[`150-2009-2012-overprovisioning-reserved-capacity-deepening.md`](150-2009-2012-overprovisioning-reserved-capacity-deepening.md)

**Question:** is controller-reserved capacity equivalent to immediately erased NAND capacity?

**Bounded result:** no. The evidence separates physical NAND capacity, host-visible namespace capacity, controller-reserved maintenance headroom, and actual erased/free-block readiness.

```text
reserved / OP capacity
    != erased block
    != GC already completed
```

The slice treats over-provisioning as transformation headroom, not as a certificate that reclamation has already occurred.

---

## Evidence chain 6 — Micron background erase, runtime completion, and planned power removal

### E150-7 — Micron 2006–2009 background-erase / power-down handshake

[`150-micron-2006-2009-background-erase-powerdown-handshake-deepening.md`](150-micron-2006-2009-background-erase-powerdown-handshake-deepening.md)

**Question:** before the M550, did Micron publicly document a flash design in which erase could be deferred toward idle time while another actor retained an explicit indication that erase remained pending/running, and in which planned power removal waited for completion?

**Bounded result:** yes, as patent/design prior art.

US7564721B2, filed in 2006 with Micron Technology as original assignee, describes:

- delayed/background erase;
- idle cycles as one possible delay/opportunity condition;
- a `background-process-busy` indication that can cover pending or executing erase;
- negation of that indication after erase completion;
- a `power-down-soon` path where pending erase is drained before planned power removal;
- and, importantly, an explicit warning that unpredictable power removal during erase may leave a block incompletely erased while system belief diverges from physical state.

The new state separation is:

```text
erase obligation
    != maintenance opportunity
    != erase execution
    != runtime completion evidence
    != planned power-removal authority
```

and the negative boundary is:

```text
planned-power-down handshake
    != arbitrary sudden-power-loss recovery
```

This is **not** evidence that M550 implemented the patent, exposed these flags, or retained a durable GC checkpoint across reset/power loss.

---

## Combined technical picture

The evidence chain now supports the following bounded model without pretending every source describes one implementation:

```text
host / filesystem retires a logical value
        |
        v
possible deallocation / invalidity knowledge
        |
        v
old physical embodiment no longer required as current
        |
        v
reclaim pressure / candidate selection
        |
        +------------------------------+
        |                              |
        v                              v
still-live payload in block       stale payload in block
        |                              |
        v                              |
preserve / relocate current data      |
        |                              |
        +--------------+---------------+
                       v
            publish / retain current resolution
                       |
                       v
              old block erase-eligible
                       |
              +--------+---------+
              |                  |
              v                  v
      erase now / under load   defer toward later opportunity
                                 |
                                 v
                        pending erase obligation
                                 |
                    idle / planned-powerdown trigger
                                 |
                                 v
                           erase execution
                                 |
                                 v
                       completion evidence
                                 |
                                 v
                        reusable capacity
```

No one source is claimed to implement every box. The diagram is an **engineering synthesis of bounded evidence**.

---

## Historical record versus engineering reconstruction

### Historical / source-level claims

The source packet establishes, in their respective artifacts:

- M550 publicly listed Active Garbage Collection and TRIM separately;
- maintained Crucial guidance treats powered idle as useful cleanup opportunity;
- T13 deallocation/read semantics do not prove physical erase;
- IBM's described controller separates invalidity, live-data relocation, mapping update, and later erase;
- pre-M550 Micron patent/design prior art separates delayed background erase, busy/completion indication, and planned power-down coordination;
- reserved capacity can support maintenance without being identical to an erased-free-block state.

### Engineering reconstruction

Project terms include:

- `reclaim eligibility`;
- `reclamation debt`;
- `maintenance opportunity`;
- `currentness publication`;
- `runtime completion evidence`;
- `power-removal authority`;
- `free-space authority`.

They organize the evidence but are not silently attributed to the historical actors.

---

## Functional comparisons and limits

### Case 04 — mapped Flash

Shared function:

```text
logical/current identity can survive physical relocation
before old embodiment reclamation
```

Not claimed: direct lineage from Ban/TrueFFS/T13 evidence to M550 or to the Micron patent.

### Case 145 — JFFS2

Shared function: live data may be preserved while stale flash state is reclaimed.

Important difference: JFFS2 exposes filesystem-level GC state and source code; managed SSD firmware hides corresponding control state behind a block interface.

### Cases 44 / 47 — sanitization and remanence

Shared physical primitive may include erase, but authority and completeness differ:

```text
capacity reclamation
    != sanitize objective
    != verified forensic forgetting
```

### Case 39 — FTL restart recovery

Case 39 remains the stronger case for explicit restart/reconstitution after volatile mapping state disappears.

The Micron background-erase handshake does not substitute for a crash-recovery protocol.

---

## What this round closes

The current round closes one bounded prior-art/control-state debt:

> **By a 2006-filed Micron design record, background flash erase could be deferred toward idle or planned-powerdown opportunity while a runtime busy/completion relation distinguished unfinished work from completed erase and gated planned power removal.**

This matters because it gives Case 150 an earlier first-party Micron witness for the separation:

```text
powered / idle opportunity
    != erase admission
    != erase completion
```

and additionally:

```text
planned shutdown coordination
    != sudden-power-loss recovery
```

The close is deliberately source-scoped. It is not a product-lineage claim.

---

## Open debts after this round

Case 150 remains **`grounded`**. No maturity promotion is justified.

Highest-value remaining work is now more product-specific:

1. **M550 sudden-power-loss GC path** — determine whether interrupted relocation/erase is journaled, scanned, replayed, quarantined, or otherwise reconstructed.
2. **M550 mapping-publication order** — identify exactly when a relocated page becomes authoritative and when the old embodiment becomes safely erasable.
3. **Named-device power-cut trace** — interrupt around live-page move, map publication, erase start, erase completion, and reboot; inspect host-visible correctness and internal telemetry where possible.
4. **M550 power-state arbitration** — establish whether AGC is eligible in Partial, Slumber, DevSleep, or only fuller-power idle states for a specified firmware revision.
5. **Period Crucial support provenance** — obtain stronger origin-hosted/captured 2010–2014 versions of the AGC support text if available.
6. **Commercial genealogy** — if pursued, route broader Micron controller/product lineage to `computing-archaeology` and link it here rather than duplicating it.

---

## Related-repository routing

A fresh `tmzncty/computing-archaeology` code search for `background erase` and `Micron` found no reusable dedicated packet during this run; the search response reported incomplete indexing, so the conclusion is only **no reusable dedicated match found**, not an exhaustive negative proof.

Broad flash-controller history, commercial SSD evolution, memory-card product history, standards adoption, and patent-family genealogy belong primarily there.

Case 150 should continue to keep the retention-specific question here:

> what state/evidence allows stale physical capacity to be retired while current logical state remains available, and what maintenance/control obligations survive until that transition is complete?
