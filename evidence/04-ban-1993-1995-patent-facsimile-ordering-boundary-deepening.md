# Case 04 Deepening — Ban 1993–1995 Patent Facsimile and Relocation-Ordering Boundary

**Status:** `bounded deepening complete`

**Canonical case:** [`../cases/04-flash-virtual-mapping-logical-identity.md`](../cases/04-flash-virtual-mapping-logical-identity.md)

**Navigation:** [`04-flash-mapping-evidence-index.md`](04-flash-mapping-evidence-index.md)

## Question

Case 04 already uses Amir Ban / M-Systems U.S. Patent 5,404,485 to ground virtual-to-physical mapping, out-of-place replacement, logical-unit identity across physical relocation, delayed erase, and reconstruction of a volatile secondary map.

This slice asks a narrower question left open by the case:

> What does direct inspection of the issued-patent facsimile establish about the **ordering** of replacement-data write, allocation-state change, mapping publication, transfer, and erase — and can this patent by itself be used as evidence for a crash-atomic update protocol?

The result is deliberately conservative:

```text
functional relocation procedure
    !=
fully specified power-fail ordering contract
    !=
proven crash-atomic publication protocol
```

The facsimile strengthens page/column anchoring for the existing Case 04 claims, but it also exposes an internal ordering ambiguity that makes the patent a poor source for stronger crash-consistency claims.

---

## Related-repository check

A fresh search of `tmzncty/computing-archaeology` for `US5404485`, `Flash file system`, and `Amir Ban` exposed no dedicated reusable packet. Broad M-Systems / PCMCIA / FTL genealogy still belongs there; this file retains only the retention-specific ordering boundary.

---

## Source custody

### Directly inspected issued-patent facsimile

Amir Ban, **“Flash file system,”** U.S. Patent 5,404,485, filed 8 March 1993, issued 4 April 1995.

Directly inspected facsimile served through Google Patents / Google Patent Images:

- <https://patentimages.storage.googleapis.com/dc/11/69/e5e495348e8726/US5404485.pdf>
- bibliographic / HTML record: <https://patents.google.com/patent/US5404485A/en>

### Custody qualification

The PDF is a facsimile of the issued U.S. patent and visibly carries patent number `5,404,485`, issue date `Apr. 4, 1995`, inventor Amir Ban, assignee M-Systems Flash Disk Pioneers Ltd., five drawing sheets, and printed patent pages 1–8.

It is served by Google rather than an inspected USPTO-hosted PDF endpoint. Therefore this slice closes the **direct facsimile / printed-page anchoring** gap, but it does **not** claim to close the narrower archival-custody wish for an independently inspected USPTO-hosted PDF.

---

# Historical record

## H1 — Printed pp. 1–2 anchor erase-before-rewrite and the virtual-map substitution mechanism

The issued patent begins from a physical constraint: a previously written area is not practically rewritten without first erasing a larger area. It then defines a virtual map that converts virtual addresses to physical addresses.

On printed p. 2, when the mapped physical block is already written, the description says an unwritten block is located and written, the map is changed so that this new physical block corresponds to the original virtual address, and the old physical address is marked unusable until a later zone erase.

**Direct anchor:** printed pp. 1–2, especially p. 2 col. 1–2; PDF image page 7 of 12 in the Google-hosted facsimile.

The retention boundary is:

```text
old physical embodiment ceases to count
    !=
old erase unit has already been physically erased
```

## H2 — The same summary gives stable logical-unit identity across physical movement

Printed p. 2 says that, in the preferred embodiment, each unit has a logical unit address that remains unchanged as the unit is rewritten into a new physical address location. It further states that the virtual map refers to logical rather than physical unit addresses so that movement during unit transfer need not change the virtual map.

This is direct primary evidence for:

```text
logical-unit continuity
    !=
physical-unit-location continuity
```

## H3 — Reclamation explicitly copies usable/current blocks before destructive erase

The p. 2 summary says unusable blocks are reclaimed by transferring units to reserved unwritten space, copying only the usable blocks, and then flash-erasing the original memory-unit space.

Printed p. 6 gives the operational form: select an active unit, read its currently mapped active blocks, write them to the transfer unit, erase the selected unit, then change the logical-to-physical unit relation so the role of the transfer unit and selected unit is exchanged.

**Direct anchors:** printed p. 2 col. 2; printed p. 6 col. 2; Figures 7–8.

This supports:

```text
select current state
    -> copy current state elsewhere
    -> erase old mixed region
    -> reuse physical space
```

It does not by itself specify power-fail atomicity across those stages.

## H4 — Printed pp. 3–4 anchor the transfer unit and currentness metadata

The preferred embodiment keeps at least one unit entirely unwritten as a `TRANSFER UNIT`, explicitly so active blocks from a unit to be erased can first be written there.

The unit header includes the logical unit number. The block-allocation map distinguishes states including:

- `block free and writable`;
- `block deleted and not writable`;
- `block allocated and contains user data`;
- a virtual-address / back-pointer field.

The text again says the logical unit number does not change even though physical location changes.

**Direct anchor:** printed p. 4, especially col. 2.

Thus free capacity and metadata are part of the maintenance mechanism rather than incidental unused space.

## H5 — Printed p. 5 gives one high-level narrative ordering for a replacement write

One paragraph on printed p. 5 describes the replacement path in this order:

1. find a free block;
2. change the original block's status to deleted;
3. change the free block's status to written;
4. update the virtual map so the original virtual address points to the new logical address;
5. map that logical address to a physical address;
6. write the block there.

The paragraph therefore reads as though **metadata/currentness changes precede the new data write**.

**Direct anchor:** printed p. 5, col. 1; the paragraph beginning `In a write operation...` immediately before the FIG. 6 discussion.

This ordering must not be silently promoted into the patent's unique normative update protocol, because the next description differs.

## H6 — The FIG. 6 detailed flow on the same printed page gives a different ordering

The immediately following FIG. 6 explanation describes the non-free-address branch in this order:

1. locate a free logical address (`block 50`);
2. map it to a physical address (`block 51`);
3. **write the data** to that physical address (`block 52`);
4. update the unit-allocation tables (`block 53`) so the original block is deleted/not writable and the replacement is allocated/user-data;
5. update the virtual/logical mapping (`blocks 54 and 55`) so the original virtual address points to the replacement.

That is materially different from H5:

```text
H5 prose:
allocation/currentness changes
    -> map update
    -> new data write

FIG. 6 explanation:
new data write
    -> allocation changes
    -> map update
```

**Direct anchor:** printed pp. 5–6, FIG. 6 explanation.

The contradiction/ambiguity is present in the primary source itself; this record does not choose one ordering and pretend the other does not exist.

## H7 — Claim 1 aligns more closely with the write-first FIG. 6 sequence

Claim 1 on printed p. 8 says that, when the currently mapped block is written or deleted, the method identifies an unwritten block, **writes the data into that unwritten block**, changes the allocation map to mark the formerly unwritten block as written, and then changes the virtual map so the virtual address maps to that physical address.

So the claim text supplies another ordering witness:

```text
write replacement payload
    -> allocation-state update
    -> virtual-map update
```

It then separately claims transfer-unit establishment, periodic unit selection, reading/writing written blocks into the transfer unit, erasing the selected unit, and updating the virtual map to reflect movement.

**Direct anchor:** printed p. 8, claim 1.

## H8 — Map metadata is itself updated out-of-place and volatile map state is reconstructed at startup

Printed pp. 6–7 describe storing most of the virtual map in Flash and a small secondary map in RAM. A modified map block is written to an unwritten Flash block, the old map block is marked deleted, and the RAM secondary map is updated to point to the replacement map block.

The patent then explicitly says the volatile secondary map can be reconstructed on startup by scanning block-usage maps retained in each unit.

**Direct anchor:** printed pp. 6–7, FIG. 9 discussion.

This directly separates:

```text
nonvolatile map representation
    !=
volatile lookup/locator representation
    !=
startup reconstruction of operational mapping state
```

---

# Engineering reconstruction

## E1 — The patent strongly grounds the functional dependency graph, not a crash-consistency protocol

Across the summary, figures, detailed description, and claims, the patent clearly grounds these dependencies:

```text
rewrite requires another writable embodiment
logical currentness must move to that embodiment
old embodiment becomes non-current / unusable
reclamation preserves current blocks before erase
mapping metadata is itself maintained and partly reconstructed
```

But H5–H7 show that it does **not** provide one unambiguous, globally consistent sequence for the individual write-path state transitions.

Therefore:

```text
patent describes all required state transitions
    !=
patent proves one crash-safe ordering among them
```

## E2 — Publication order matters because the states have different failure consequences

If a system publishes mapping/currentness before replacement payload is safely established, a crash can leave the logical address naming incomplete state. If it establishes the new payload first but crashes before publication, the system instead risks an orphan/unreferenced new copy while the old mapping remains current.

Those are engineering consequences of the state classes, not failure behaviors demonstrated by this 1995 patent.

The facsimile therefore sharpens the open question to:

> Which later named implementation records a durable ordering relation among replacement completion, allocation-state publication, mapping publication, and old-embodiment retirement?

## E3 — Functional order is not durability order

Even the write-first FIG. 6 / claim sequence does not tell us:

- when a Flash program operation is considered power-fail-safe;
- whether map/allocation writes are individually atomic;
- whether metadata updates are journaled, versioned, checksummed, or replayable;
- whether a controller waits for Flash-ready completion before publishing the map;
- how interrupted map-block replacement is resolved;
- how an interrupted transfer-unit erase or unit-role exchange is recovered.

Thus:

```text
textual step A appears before textual step B
    !=
A is durably committed before B becomes authoritative
```

## E4 — Map self-hosting creates a second out-of-place-update problem

The patent applies essentially the same Flash replacement rule to map blocks themselves: write a modified map block into an unwritten block, mark the old map block deleted, and update the RAM locator.

This means the system is not only maintaining:

```text
virtual address -> current user-data embodiment
```

but also:

```text
secondary map -> current primary-map-block embodiment
```

That recursive relation makes startup reconstruction important. It also means payload relocation and mapping-metadata relocation are distinct retention obligations even though both use out-of-place Flash updates.

---

# Functional analogy

A bounded comparison to copy-on-write, WAL/journal publication, or distributed configuration commits is useful only at the question level:

```text
new candidate state exists
    !=
new candidate state is authoritative
```

The Ban patent is not evidence that it implements filesystem COW atomicity, database commit, consensus, or later SSD firmware transaction machinery.

Likewise, the FIG. 6 / claim ordering can be called **write-before-map-update** as a description of those specific passages, but it must not be generalized into a universal FTL crash-consistency rule.

---

# Philosophical interpretation

This facsimile adds a modest conceptual result to Case 04:

> continuity of a logical object depends not only on preserving enough physical copies, but on controlling when a new embodiment acquires authority.

The source itself does not use `authority`, `publication`, or `commit` in this sense. Those are project-level analytical terms for distinguishing payload existence from the mapping relation that makes one payload current.

The internal ordering ambiguity is philosophically useful precisely because it disciplines interpretation: a diagram of state replacement is not automatically a theory of temporal commitment.

---

# Explicit non-claims

This deepening does **not** claim:

- that Google Patent Images provides official USPTO archival custody;
- that the patent's high-level prose is wrong and FIG. 6 is necessarily the implemented code path;
- that FIG. 6 is wrong because the preceding paragraph differs;
- that claim ordering automatically defines hardware durability barriers;
- that M-Systems shipping firmware necessarily executed the steps in claim order;
- that a new Flash block was always durable before the map changed;
- that the patent guarantees atomic recovery from arbitrary power loss;
- that block-allocation words or map entries were atomically programmable;
- that startup scanning resolves every possible torn metadata update;
- that `deleted` means physically erased or forensically unrecoverable;
- that this patent is identical to later PCMCIA FTL, TrueFFS, NAND SSD FTLs, or modern copy-on-write systems.

---

# Resulting bounded distinctions

```text
logical identity continuity
    !=
physical-location continuity

replacement payload written
    !=
replacement payload published as current

mapping publication
    !=
old physical erase

functional step ordering
    !=
durable / crash-atomic ordering

one preferred-embodiment paragraph
    !=
one uniquely specified update protocol

nonvolatile primary map
    !=
volatile secondary lookup state
    !=
reconstructed startup lookup state

issued-patent facsimile page anchor
    !=
official archival custody claim
```

---

# What this closes and what remains open

This slice closes a narrower Case 04 source-quality gap:

- the main Ban-patent claims now have directly inspected **printed page / figure / claim anchors** rather than relying only on Google Patents HTML transcription;
- the patent can no longer be casually cited as though it established a single crash-safe replacement ordering;
- the existing `power-fail ordering around relocation` debt is **narrowed**, not closed.

The next highest-value source would be a named implementation, firmware/patent revision, or fault-injection study that explicitly orders and survives interruption across:

```text
destination payload validation
    -> durable mapping/currentness publication
    -> old embodiment retirement
    -> later erase/reuse
```

A separately inspected USPTO-hosted facsimile would improve custody, but would not by itself resolve the engineering ordering ambiguity already visible in the issued patent.

---

# Sources

## Primary

1. Amir Ban, **“Flash file system,”** U.S. Patent 5,404,485, filed 8 March 1993, issued 4 April 1995. Directly inspected issued-patent facsimile: <https://patentimages.storage.googleapis.com/dc/11/69/e5e495348e8726/US5404485.pdf>.
   - printed pp. 1–2: erase-before-rewrite, virtual map, replacement into unwritten physical space, stable logical-unit identity, transfer/reclamation summary;
   - printed pp. 3–4: transfer-unit reserve, unit header, allocation-map states, logical/physical separation;
   - printed pp. 5–6: read/write paths, FIG. 6 replacement sequence, transfer and reclaim, Flash-resident primary map;
   - printed p. 7: map-block out-of-place update and startup reconstruction;
   - printed p. 8: claim 1 write/allocation/map order and transfer-unit sequence.
2. Google Patents HTML record for bibliographic cross-check and machine-searchable transcription: <https://patents.google.com/patent/US5404485A/en>.

## Companion repository check

3. `tmzncty/computing-archaeology` search for `US5404485`, `Flash file system`, and `Amir Ban`: no dedicated reusable packet found in this pass.
