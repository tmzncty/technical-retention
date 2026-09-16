# Case 52 Deepening — Denali 2008–2009 Persistent Read-Count Checkpoint Semantics

## Status

**`bounded deepening complete`** for the Denali read-disturb-control-state slice described here.

Canonical case: [`../cases/52-nand-flash-read-disturb-access-induced-decay.md`](../cases/52-nand-flash-read-disturb-access-induced-decay.md).

Parent grounding record: [`52-cai-2009-2015-nand-read-disturb-grounding.md`](52-cai-2009-2015-nand-read-disturb-grounding.md).

Micron 2006 manufacturer-policy deepening: [`52-micron-2006-read-disturb-temporary-failure-maintenance-deepening.md`](52-micron-2006-read-disturb-temporary-failure-maintenance-deepening.md).

## Why this slice exists

Case 52 already established that NAND reads can cumulatively consume future error margin, that a read count can become a maintenance trigger, and that relocation can preserve logical data by replacing its physical embodiment. What remained underdeveloped was a different retention question:

> If a controller uses accumulated read exposure as the reason for future maintenance, what state must survive a reboot for that maintenance policy to retain its memory of the past?

The Denali Software filing later published as **US20090193174A1, _Read disturbance management in a non-volatile memory system_**, supplies an unusually explicit early answer. Its disclosed embodiment stores per-location read-count state in a block table in non-volatile memory, loads that table into system memory at power-up, updates the live copy during operation, and writes the table back to non-volatile memory periodically and at shutdown.

This is useful for `technical-retention` because the read counter is neither user payload nor a mere instantaneous sensor value. It is a retained summary of earlier accesses whose purpose is to govern future maintenance.

The bounded result is:

```text
payload survives power-off
    !=
maintenance history automatically survives power-off

retaining access-induced maintenance policy
    can require
retaining a summary of prior access exposure
```

The same source also exposes an important persistence horizon:

```text
live read-count state
    !=
latest non-volatile checkpoint of that state
```

The source does **not** specify a crash-consistency protocol that makes every individual read-count increment durable.

## Source and chronology

### Patent family

Robert Alan Reid, **_Read disturbance management in a non-volatile memory system_**:

- U.S. application `US12/022,146`;
- filed / priority date: **29 January 2008**;
- U.S. application publication: **US20090193174A1, 30 July 2009**;
- later grant: **US7937521B2, 3 May 2011**.

Primary-family text / metadata:

- <https://patents.google.com/patent/US7937521B2/en>
- publication record for `US20090193174A1` is preserved in that family page.

The Google Patents family record also preserves a 29 January 2008 assignment to **Denali Software, Inc.** and later assignment history to Cadence. The historical engineering discussion below is about the disclosed mechanism, not about present legal ownership.

### Public-date discipline

The filing date and public-document date are not collapsed.

The application was filed in January 2008, but the inspected family record identifies **30 July 2009** as publication of `US20090193174A1`. Therefore this evidence uses:

```text
2008-01-29
    = filing / priority chronology

2009-07-30
    = public-document floor used here
```

The filing date is relevant to priority chronology. It is **not** presented as proof that the full application text was publicly available on that date.

## Historical record

### H/P — read count is stored as explicit control state

The disclosed block table contains, among other fields:

- logical block addresses;
- block-status flags;
- physical block addresses;
- wear-level indicators;
- **read-count data**.

The text says embodiments record the number of reads for blocks and use that read count to decide when data should move to avoid read-disturb effects.

This establishes period control vocabulary stronger than a generic statement that firmware “knows” a block is hot:

```text
past READ operations
    -> explicit read-count state
    -> future relocation decision
```

The counter is a compact record of an access history, not the access history itself.

### H/P — the block table is retained in non-volatile memory

The disclosed embodiment stores the block table in a memory block of the non-volatile memory. At power-up, that table is loaded into system memory and used by the non-volatile-memory file system.

The source expressly contrasts this with reconstructing the table anew at each boot.

Therefore the historical mechanism includes an intentional cross-power boundary:

```text
non-volatile block-table image
    -> power-up load
    -> live system-memory control state
```

The read count is thus part of the information that can be reconstituted after a power cycle.

### H/P — the live copy and persistent copy have different update horizons

The patent says that while data are accessed and moved, the block table copy in system memory is updated. It then says the table is written to non-volatile memory **periodically, and at system shutdown**.

That wording is important. The disclosed control path is not simply:

```text
every read
    -> immediately durable read-count increment
```

Instead, the described path is:

```text
READ activity
    -> live block-table update in system memory
    -> periodic / shutdown writeback
    -> non-volatile checkpoint
```

The source does not quantify the checkpoint interval.

### H/P — power-up restores the table rather than replaying every read

At power-up, the saved block table is loaded as a unit from non-volatile memory into system memory. The patent presents this as an advantage over designs that reconstruct needed information each boot.

That makes the retained table a **summary sufficient for policy continuation in the disclosed embodiment**, not a replay log of every historical operation.

This distinction is central:

```text
retained maintenance summary
    !=
complete retained event history
```

### H/P — threshold crossing leads to movement and counter reset

The patent states that when the read count reaches a predetermined threshold, data are moved to a new physical memory block. It then resets read-count state associated with the old and new block locations.

The disclosed embodiment therefore ties a maintenance event to a change in embodiment and to a reset of the exposure summary:

```text
accumulated read exposure
    -> threshold
    -> relocate payload
    -> reset read-count state
```

This is a different controller-policy topology from the later Texas Memory Systems page-by-page proposal used elsewhere in Case 52. It is also distinct from Micron's 2006 design-guide choices.

### H/P — the threshold is preventive, not an observation that corruption already occurred

The source describes the threshold as a value chosen below the point at which read disturbance is expected to change data, so movement can occur before accumulated disturbance reaches an unsafe level.

Thus the counter is used as a **preventive maintenance trigger**:

```text
maintenance threshold reached
    !=
payload already proved uncorrectable
```

This remains a disclosed design, not proof that every commercial controller of the period used this exact threshold or table layout.

## Engineering reconstruction

### E — retained read count is a memory of maintenance debt

The patent itself speaks in terms of read counts and movement, not “maintenance debt.” In project vocabulary, the persisted counter can be read as a compact witness that prior accesses have consumed part of a block's allowed read-disturb budget.

That gives a useful decomposition:

```text
user payload state
    !=
logical-to-physical mapping state
    !=
read-exposure summary
    !=
wear summary
```

All can affect whether future access remains safe, but they are not the same state.

### E — power-cycle continuity of payload does not imply power-cycle continuity of exposure knowledge

NAND payload is non-volatile by construction, but the controller's live read-count copy resides in system memory in the disclosed embodiment. The design therefore deliberately checkpoints the block table to non-volatile memory so the exposure summary can be recovered later.

The bounded reconstruction is:

> **non-volatile payload ≠ automatically non-volatile knowledge about how that payload has been stressed**.

This is one of the clearest early controller-level examples in the repository of retention requiring preservation of **control state about the payload**, not only the payload itself.

### E — periodic checkpointing does not establish per-read crash durability

Because the source distinguishes live system-memory updates from periodic / shutdown non-volatile writeback, it does not establish that the latest read-count value is durable after an unexpected power loss between checkpoints.

The careful inference is only:

```text
latest live counter
    may be newer than
latest persisted counter
```

and therefore:

```text
cross-power continuity of the counter scheme
    !=
zero rollback of read-count history after abrupt power loss
```

The patent does not specify the maximum rollback, atomicity of the table update, power-loss protection, journal format, or recovery rule for an interrupted table write. Those questions remain open.

This is an **engineering reconstruction from the stated update horizons**, not a historical claim that Denali described the problem as “crash consistency.”

### E — maintenance completion can reset the trigger summary without erasing logical identity

When a hot block is relocated, its logical payload continues at a new physical embodiment while the read-count summary is reset.

Therefore:

```text
logical data continuity
    !=
continuity of the old embodiment's exposure counter
```

and:

```text
counter reset
    can mean
new maintenance epoch

counter reset
    !=
logical object recreated from nothing
```

This is a bounded example of **epochal control state**: the counter describes stress accumulated since a maintenance-changing event, not the full lifetime history of the logical object.

### E — a compact summary can forget detail intentionally

One counter can stand in for many individual reads. That compression is not necessarily a defect; it is the policy's chosen sufficient statistic.

But the compression boundary matters:

```text
read count N
    does not preserve
which exact pages were read in which order
```

The controller can retain enough history to trigger maintenance while forgetting most of the event sequence.

This is a technical distinction between **retaining a decision-relevant summary** and **retaining provenance of every event**.

## Functional comparisons

### A — Micron 2006 manufacturer guidance

Micron TN-29-17 already says a system can designate a read count at which repeatedly read NAND data should be renewed. Denali adds a more explicit controller-state embodiment: a read count field in a block table, non-volatile storage of the table, power-up load, and threshold-triggered relocation.

The safe relation is:

```text
Micron 2006:
    manufacturer guidance for read-count-triggered renewal

Denali 2009 publication:
    explicit retained controller summary + relocation logic
```

This is **not** a claim that Denali implemented Micron's guidance or that one source derived from the other.

### A — Texas Memory Systems 2009-priority / 2010 publication

The later Texas Memory Systems patent `US7818525B1` cites `US20090193174A1` in its patent record and proposes its own read-disturb handling, including page-level movement after block-read thresholds.

The bounded comparison is:

```text
Denali:
    move an entire block in the principal described threshold path

Texas Memory Systems:
    later disclosure includes more incremental page movement
```

A patent citation establishes a formal prior-art relation in the document record. It does **not** by itself prove direct engineering influence, code reuse, product genealogy, or commercial deployment.

### A — later read-reclaim / read-scrub schemes

Later controller policies in Case 67 use richer signals and different controller geometry. Denali's table therefore supplies prior art for one generic pattern:

```text
retain access-exposure state
    -> compare to threshold
    -> replace / relocate embodiment
```

It does not prove that later 3-D NAND policies inherited Denali's table layout or persistence strategy.

## Philosophical interpretation — bounded

The narrow conceptual contribution is that a storage system may need to remember **what has been done to a stored state** in order to preserve that state later.

The payload can survive power-off while the system also needs a separate retained summary of prior reads. In that sense, retention can depend on a second-order memory:

```text
memory of payload
    +
memory of maintenance-relevant history
```

But this is project interpretation. The patent is an engineering disclosure about read-disturb management, not a philosophical claim about memory, history, or identity.

## Explicit non-claims

This record does **not** claim that:

1. Denali discovered NAND read disturb;
2. the 29 January 2008 filing date is the public-document date;
3. Denali was the first company to store read counts persistently;
4. the patent proves a named shipping product used this exact block-table design;
5. every individual read-count increment was synchronously persisted;
6. abrupt power loss necessarily loses a specific number of count increments;
7. the patent specifies an atomic or journaled block-table update protocol;
8. resetting the read count means the logical data ceased to exist;
9. a read-count threshold is a universal physical NAND limit;
10. a patent citation proves direct product or implementation genealogy;
11. Denali's whole-block movement and Texas Memory Systems' later page movement are the same algorithm;
12. the retained counter records a complete access history;
13. read-count persistence is equivalent to ECC metadata or bad-block-retirement authority;
14. this source closes the later 3-D NAND read-reclaim history;
15. current legal assignee metadata is identical to the historical engineering organization at filing.

## Source-lineage and repository boundary

A current repository search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `read disturbance`, `NAND`, and `Denali` found no dedicated module to reuse.

A broader genealogy of Denali Software, controller software, NAND FTL products, Cadence acquisition history, and the Texas Memory Systems / IBM line belongs in `computing-archaeology` if developed later. This record keeps only the retention-specific relation among:

- accumulated access exposure;
- explicit read-count control state;
- non-volatile checkpointing;
- power-up reconstitution;
- threshold-triggered relocation;
- and maintenance-epoch reset.

## Evidence strength

| Question | Strength | Reason |
| --- | --- | --- |
| Was `US20090193174A1` publicly published by 30 July 2009? | **strong** | patent-family publication metadata |
| Did the disclosed design store read-count state in a block table? | **strong** | description + claims |
| Could that table be stored in non-volatile memory and loaded at power-up? | **strong** | explicit description + claim 18 |
| Was the live table updated in system memory and written back periodically / at shutdown? | **strong** | explicit description |
| Did threshold crossing trigger relocation and counter reset in the disclosed embodiment? | **strong** | explicit description / claims |
| Was every increment crash-durable? | **not established** | source says periodic / shutdown writeback, not synchronous per-read persistence |
| How many increments could be lost on abrupt power failure? | **open** | checkpoint interval and recovery protocol not specified |
| Was this exact design deployed in a named Denali product? | **not established** | patent disclosure is not deployment evidence |
| Does the later TMS citation prove direct engineering lineage? | **no** | citation is documentary prior art, not implementation genealogy |

## Remaining evidence debt

1. Find period product or firmware documentation that demonstrates a **shipping** controller retaining read-exposure state across reset / power loss.
2. Find a source that specifies the **checkpoint granularity or crash-recovery rule** for read-count metadata, rather than only saying it is periodically persisted.
3. Determine whether any 2007-or-earlier public controller disclosure used persistent read-count maintenance state, without treating filing dates as publication dates.
4. Keep later 3-D NAND read-reclaim history in Case 67 unless a source materially changes Case 52's access-induced-retention argument.
5. If Denali / Cadence / Texas Memory Systems product genealogy is pursued, move the broad historical reconstruction to `computing-archaeology` and cite it back here.

## Sources

1. Robert Alan Reid, **_Read disturbance management in a non-volatile memory system_**, U.S. application `US12/022,146`, application publication **US20090193174A1** (30 July 2009), later grant **US7937521B2** (3 May 2011): <https://patents.google.com/patent/US7937521B2/en>.
2. Patent-family metadata on the same page records the 29 January 2008 filing / priority date, 30 July 2009 application publication, and historical assignment to Denali Software, Inc.
3. Holloway H. Frost et al., **_Efficient reduction of read disturb errors in NAND FLASH memory_**, `US7818525B1`, priority 12 August 2009, publication 19 October 2010; its patent record cites `US20090193174A1`: <https://patents.google.com/patent/US7818525B1/en>.
4. Micron Technology, Inc., **TN-29-17: _NAND Flash Design and Use Considerations_**, Rev. A 8/06; bounded evidence record: [`52-micron-2006-read-disturb-temporary-failure-maintenance-deepening.md`](52-micron-2006-read-disturb-temporary-failure-maintenance-deepening.md).

## Completion note

This slice is complete at the level justified by the inspected sources: it adds a **2009 public controller disclosure of persistent read-exposure control state**, separates live state from periodic non-volatile checkpoints, and makes the abrupt-power-loss persistence limit explicit without inventing a crash-consistency mechanism the source does not specify.
