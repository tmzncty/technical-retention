# LPDDR3→LPDDR4 Per-Bank Refresh: Moving Bank-Target Scheduling Across the Controller/DRAM Boundary

## Status

**`grounded`** — bounded to the publicly recoverable LPDDR3/LPDDR4 refresh-command semantics in JEDEC standard copies and Micron manufacturer-authored product documentation, with later AMD and Microchip controller documentation used only as implementation/context witnesses.

Grounding record: [`../evidence/139-lpddr3-lpddr4-per-bank-refresh-target-authority-grounding.md`](../evidence/139-lpddr3-lpddr4-per-bank-refresh-target-authority-grounding.md).

The strongest historical bodies used here are mirror-hosted rather than fetched from JEDEC/Micron origin servers. They are therefore marked `H/P*` in the evidence record. Their document identities, revision strings, copyright lines, and technical wording are explicit, and the LPDDR3/LPDDR4 relation is independently consistent across JEDEC-text copies and Micron product documents. This is strong enough for the bounded mechanism claim, but it is not treated as a complete standards-publication provenance chain.

## Scope

This case asks one narrow question left open by Cases 21, 33, 69, and the roadmap's broader LPDDR/per-bank-refresh debt:

> When per-bank refresh remains externally commanded, what changes when the **choice of the next bank target** moves from a fixed device-scheduled round-robin sequence to a controller-specified bank address with a coverage rule and synchronized bookkeeping?

The bounded comparison is:

- LPDDR3 / JESD209-3B and Micron 2014 product documentation: `REFpb` refreshes the bank scheduled by a **bank counter in the memory device**, with a fixed `0-1-2-3-4-5-6-7...` sequence. The controller must nevertheless track which bank is being refreshed.
- LPDDR4 / JESD209-4B and Micron Rev. D 3/20 product documentation: `REFpb` carries a **bank address supplied on the command/address interface**; the controller may choose the eight banks in any order, but may not repeat a bank until all eight have been covered. Controller and DRAM retain synchronized bank-count state, reset at defined synchronization events.

This case is **not**:

- a complete LPDDR2→LPDDR5 standards chronology;
- an invention-priority claim for per-bank refresh;
- proof that the first LPDDR4 revision introduced controller-selected ordering;
- a transistor-level account of the refresh row counter;
- a claim that controller choice removes the DRAM's internal row-refresh machinery;
- a claim that LPDDR4 `REFpb` is the same topology as DDR5 `REFsb`;
- a benchmark claiming per-bank refresh always improves performance.

## Historical vocabulary and record

### LPDDR3: device-scheduled bank order

The recoverable text of **JEDEC JESD209-3B, August 2013**, says a per-bank refresh command performs refresh on the bank scheduled by the **bank counter in the memory device**. The sequence is fixed sequential round robin:

```text
0-1-2-3-4-5-6-7-0-1-...
```

The standard text also says the bank count is synchronized between controller and SDRAM by resetting it to zero on RESET or at every exit from self refresh. The controller must track the bank being refreshed even though it does not choose an arbitrary bank for each `REFpb` command in this bounded regime.

Micron's **178-Ball, Single-Channel Mobile LPDDR3 SDRAM**, Rev. D 9/14, preserves the same wording and is a manufacturer-authored product witness to this fixed device-bank-counter behavior.

The LPDDR3 text also distinguishes all-bank and per-bank service geometry: the bank selected by `REFpb` must be idle and is unavailable for `tRFCpb`, while other banks may remain active or receive reads/writes subject to the documented timing constraints.

### LPDDR4: controller-selected bank address under a coverage rule

The recoverable text of **JEDEC JESD209-4B** changes the bank-target relation. For per-bank refresh, bank address bits are transferred with the command. The controller may issue `REFpb` to the eight banks in any order; the text gives deliberately non-round-robin examples. It is illegal, however, to send `REFpb` to the same bank again until all eight banks have been refreshed.

Micron's **200b: x16/x32 LPDDR4/LPDDR4X SDRAM**, document `CCM005-554574167-10522`, Rev. D 3/20, makes the same relation explicit:

- `BA0`, `BA1`, and `BA2` are transferred on `CA0`, `CA1`, and `CA2` for `REFpb`;
- the eight banks may be refreshed in any order;
- a bank cannot be repeated before all eight are covered;
- the count of eight begins after a synchronization event;
- controller and device bank counts are synchronized to zero on reset procedure, every self-refresh exit, and by `REFab`;
- `REFab` also refreshes all banks according to the row counter and resets the bank counter;
- the row-refresh counter and bank-count bookkeeping therefore remain distinct pieces of maintenance state.

This is not a move from `internal refresh` to `external refresh`. Both regimes still use externally issued refresh commands in normal operation. What changes is a narrower authority: **which bank is selected by the next per-bank maintenance command**.

## Retained state and control state

The payload remains volatile dynamic-cell state whose preservation still depends on timely refresh. The interesting retained/control relations are narrower:

1. **refresh obligation** — restoration work must cover the required array often enough;
2. **row-refresh phase** — internal row enumeration identifies which refresh row is being serviced across cycles;
3. **bank-target phase / coverage state** — which banks in the current per-bank group have already been serviced;
4. **controller scheduling state** — enough state to know which bank can legally receive the next `REFpb` and when;
5. **service-availability state** — whether a given bank is presently eligible for ordinary access while another bank is refreshing.

The repository terms `bank-target scheduling authority`, `coverage state`, and `maintenance target phase` are engineering-reconstruction vocabulary, not historical JEDEC terms.

## Engineering reconstruction

### Refresh obligation != bank-target scheduling authority

LPDDR3 and LPDDR4 both preserve the same broad requirement that refresh work recur. The LPDDR4 change does not remove the physical leakage deadline. It changes who chooses the bank order for per-bank maintenance.

Therefore:

> **refresh obligation != bank-target scheduling authority**.

A retention mechanism can keep its physical obligation while moving one scheduling decision across the device/controller boundary.

### Bank-target selection != row enumeration

LPDDR4's controller supplies the bank address, yet Micron's table still separately exposes a `Ref. Counter (Row Address #)` and shows that a full set of eight per-bank operations advances the row-refresh relation.

Therefore:

> **controller-selected bank != controller-selected refresh row**.

Moving target-bank choice outward is not evidence that every lower-level refresh address becomes externally specified.

This also protects the boundary with Case 09, which studies on-chip refresh-row address generation, not per-bank target-order freedom.

### Arbitrary bank order != arbitrary coverage

LPDDR4 allows any order, but forbids repeating a bank until all eight have been refreshed. `1-3-0-2-4-7-5-6` is legal precisely because it covers the complete bank set once.

Therefore:

> **ordering freedom != coverage freedom**.

A controller can optimize *when* a bank is chosen relative to traffic while remaining constrained by a maintenance-completeness invariant.

### Shared synchronized count != complete refresh history

Both the LPDDR3 and LPDDR4 texts describe synchronization of bank-count state between controller and device. LPDDR4 additionally defines events that reset the bank count to zero and begins a new eight-command counting interval.

That retained phase is not a log of every prior refresh operation. It is enough bookkeeping to keep the current maintenance cycle coherent.

Therefore:

> **maintenance phase state != maintenance history**.

And:

> **synchronization event != recovery of prior bank-order history**.

Reset/SRX/REFab can establish a known current phase without reconstructing the sequence that preceded it.

### Reset of bank-count state != payload erasure

The LPDDR4 text resets bank-count bookkeeping at reset/self-refresh exit/REFab synchronization points. Nothing in that fact means the user payload is thereby cleared. `REFab` is itself a refresh operation; reset and self-refresh exit are control transitions.

Therefore:

> **maintenance-control re-synchronization != payload forgetting**.

This is the same general methodological warning used elsewhere in the repository: a control-state lifetime can differ from the payload relation it helps maintain.

### Controller tracking != controller ownership of every refresh mechanism

LPDDR3 already says the controller must track the bank being refreshed even though the next bank is selected by the DRAM's fixed bank counter. LPDDR4 gives the controller more choice over the bank address, but internal row-refresh state still exists.

Therefore:

> **tracking a maintenance target != owning all maintenance state**,

and:

> **more controller scheduling freedom != complete externalization of refresh**.

### Per-bank service availability != no refresh interference

In both bounded regimes, the target bank is inaccessible during `tRFCpb`, while other banks may be accessed subject to timing constraints.

So:

> **partial concurrency != zero maintenance interference**.

Later AMD controller documentation is useful as an implementation witness because it makes the system-level consequence explicit: LPDDR4 per-bank refresh can reduce refresh interference, but the performance result depends on traffic and address mapping and can even be worse than all-bank refresh in some cases.

Thus:

> **more scheduling freedom != guaranteed performance improvement**.

The physical retention obligation remains; the controller has gained an opportunity for scheduling, not a universal latency theorem.

## Cross-case comparison

### Case 21 — refresh recurrence authority

Case 21 separates externally repeated AUTO REFRESH from SELF REFRESH, where the device generates recurring maintenance internally. Case 139 is narrower: normal `REFpb` remains externally issued, while only **bank-target ordering** changes.

> `recurring refresh authority != per-command bank-target authority`.

### Case 33 — DDR5 Same Bank Refresh

Case 33's DDR5 `REFsb` targets the **same bank position across bank groups**. LPDDR4 `REFpb` in this case targets one explicitly addressed bank in the bounded channel/device organization.

The functional analogy is maintenance localization, but:

> **LPDDR4 per-bank target geometry != DDR5 same-bank-across-bank-groups geometry**.

No genealogy is inferred merely because both allow non-target resources to remain usable.

### Case 69 — temporal scheduling elasticity

Case 69 studies postponement/pull-in and timing debt. LPDDR4's arbitrary bank ordering is another scheduling freedom, but on a different axis.

> **which bank next != how much refresh may be postponed**.

A controller can have target-order freedom while still owing bounded refresh work over time.

## Prior art and anti-anachronism

This case deliberately makes no claim that LPDDR4 invented per-bank refresh. LPDDR3 — and earlier LPDDR2 material — already documents per-bank refresh with concurrent access to other banks.

The bounded historical change is narrower:

> **by the LPDDR3 2013/2014 record examined here, the device's bank counter fixes the per-bank sequence; by the LPDDR4B / Micron LPDDR4 record examined here, the controller transmits a bank address and may choose the eight-bank order under a complete-coverage-before-repeat rule.**

That is a standards/product semantic comparison, not a priority claim. Establishing the first ballot, proposal, patent, implementation, or committee rationale that moved bank-order choice outward belongs in `computing-archaeology` if pursued.

A fresh search of `tmzncty/computing-archaeology` found no dedicated LPDDR per-bank-refresh study to reuse, so the broader DRAM/JEDEC genealogy remains routed there rather than duplicated here.

## Functional analogy and philosophical limit

A bounded conceptual result follows:

> A retention obligation can remain physically unchanged while the **freedom to choose the next maintenance target** migrates across an interface.

That matters because `where maintenance happens` and `who chooses its next target` are not the same question. The same volatile substrate can be presented through different control partitions.

The analogy stops there. This does not imply that a DRAM `remembers its own maintenance`, that controller scheduling is a form of cultural memory, or that all technical retention evolves by steadily externalizing control.

## Failure / misuse boundaries

The sources justify several concrete risks without supplying a production fault-injection study:

- losing controller/device agreement about bank-count phase can invalidate assumptions about which bank is legal or due next;
- arbitrary ordering can still violate the complete-coverage-before-repeat rule;
- a legal target order can still violate temporal refresh requirements if commands are too late;
- serving a non-target bank during `tRFCpb` does not prove the overall refresh schedule is retention-safe;
- a synchronized bank counter does not prove payload correctness;
- current AMD/Microchip controller documentation demonstrates implementer-visible policy choices, not the exact behavior of every historical LPDDR controller.

## Findings

1. LPDDR3 `REFpb` can be externally commanded while bank target selection remains device-scheduled.
2. LPDDR4 `REFpb` can move per-command bank selection to controller-supplied bank address without moving the internal row-refresh phase out of the DRAM.
3. Ordering freedom and coverage obligation are distinct.
4. Controller/device bank-count synchronization is current maintenance-phase state, not a complete history.
5. Control-phase re-synchronization does not imply payload reset.
6. Partial bank availability during refresh does not remove timing/interference constraints.
7. LPDDR4 `REFpb` and DDR5 `REFsb` share a localization theme but have different target geometries.

## Open work

- direct official-host provenance/facsimiles for the exact JESD209-3B / JESD209-4B clauses;
- original JESD209-4 / earlier LPDDR4 revision comparison to determine whether the ordering change already appears there;
- LPDDR2 product/standard archaeology and first per-bank-refresh genealogy;
- committee ballot / proposal / patent history for bank-target scheduling;
- LPDDR5 evolution;
- named controller traces or fault injection for lost bank-phase synchronization;
- quantitative scheduling studies separated from normative command semantics.

## Sources

### Historical / manufacturer / standards bodies

- JEDEC, **JESD209-3B, Low Power Double Data Rate 3 (LPDDR3)**, August 2013; publicly recoverable mirror used for clause text: https://studylib.net/doc/28331319/jesd209-3b
- Micron, **178-Ball, Single-Channel Mobile LPDDR3 SDRAM**, Rev. D 9/14, document `09005aef858e9dd3`; publicly recoverable mirror: https://dtsheet.com/doc/1384705/178-ball--single-channel-mobile-lpddr3-sdram
- JEDEC, **JESD209-4B, Low Power Double Data Rate 4 (LPDDR4)**, 2017; publicly recoverable mirror used for clause text: https://studylib.net/doc/27908019/jesd209-4b
- Micron, **200b: x16/x32 LPDDR4/LPDDR4X SDRAM**, `CCM005-554574167-10522`, Rev. D 3/20; publicly recoverable PDF mirror: https://atta.szlcsc.com/upload/public/pdf/source/20201117/C907715_2114FBF6DFC7A015B06DF2675C9B2C1D.pdf
- Micron, current LPDDR4/4X product family page (current product-family metadata, not historical clause text): https://www.micron.com/products/memory/lpddr-components/lpddr4

### Later implementation/context witnesses

- AMD, **Versal Adaptive SoC Programmable Network on Chip and Integrated Memory Controller 1.1, PG313, LPDDR4 Refresh Options**, release 2026-06-23: https://docs.amd.com/r/en-US/pg313-network-on-chip/LPDDR4-Refresh-Options
- Microchip, **UDDRC Refresh Control Register 0**, current controller documentation: https://onlinedocs.microchip.com/oxy/GUID-999BFD8D-CFE5-4F54-AF70-76475125B7FB-en-US-2/GUID-BE25A87E-A9A0-465E-8403-4C64CED59221.html
