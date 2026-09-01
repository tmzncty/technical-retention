# Case 07 source deepening — Intel 5101L battery-backed retention transition

## Purpose

This note deepens [`cases/07-static-mos-ram-powered-quiescence.md`](../cases/07-static-mos-ram-powered-quiescence.md) at one deliberately narrow boundary:

> What has to remain true when a static MOS RAM leaves ordinary +5 V service, keeps its state under a lower-power retention condition, and later returns to active service?

The answer is useful because it prevents `static` from collapsing into `nothing happens`. Intel's 1975 component specification already separates normal operation from a low-voltage data-retention condition. Intel's 1977 *Memory Design Handbook* then shows how a designer can build the board-level transition around the same 5101 family with chip deselection, battery substitution, power-loss detection, and controlled recovery.

This is **not** a new general SRAM history and it does not solve the remaining Intel-1101 transistor-level cell-topology gap. The 1977 handbook is used as a near-period vendor engineering follow-up to the bounded 1968–1975 case, not as evidence that every detail described in 1977 was already documented in 1969.

---

## Source 1 — Intel *Data Catalog* (1975), 5101 / 5101L

### H/P — normal operation and retention are separately specified conditions

Intel's 1975 catalog describes the 5101 family as static CMOS RAM and explicitly frames battery operation or battery backup as useful where system-level non-volatility is required. For the 5101L / 5101L-3 it specifies a separate low-`VCC` data-retention condition:

- ordinary electrical characteristics are specified at `VCC = 5 V ±5%` unless otherwise stated;
- `VCC for Data Retention` is guaranteed down to `2.0 V` for the 5101L family;
- data-retention current at `VDR = 2.0 V` is specified with `CE2 <= 0.2 V`;
- `Chip Deselect to Data Retention Time` is specified separately;
- `Operation Recovery Time` is defined as one read-cycle time;
- the same data sheet gives a `650 ns` read-cycle specification under ordinary operating conditions.

The immediately preceding catalog text also states that the 5101/5101-3 use fully DC-stable static circuitry and that the 5101L variants add guaranteed low-voltage data retention.

**Primary anchor:** Intel Corporation, *Intel Data Catalog* (1975), 5101/5101L section, printed pp. 2-115–2-118: <https://deramp.com/downloads/mfe_archive/050-Component%20Specifications/Intel/Memory%20Components/1975_Intel_Data_Catalog.pdf>.

### Source-inspection boundary

The repository's web path exposed page-preserving extracted text for the relevant 1975 catalog pages, including the printed page labels and table entries. Attempts to render screenshots of those PDF pages returned a cache error in this run. Therefore:

- the numerical/specification claims above are grounded in indexed primary-source text with explicit page locations;
- this note does **not** claim a fresh visual inspection of the 1975 facsimile waveform or typography.

That limitation does not change the distinction the data sheet itself makes among normal operation, chip deselection, low-voltage retention, and operation recovery.

---

## Source 2 — Intel *Memory Design Handbook* (May 1977), 5101 systems considerations

### H/P — Intel treats battery-backed retention as a system-design problem

Intel's 1977 *Memory Design Handbook* says the 5101 requires no refresh timing and then devotes its systems-considerations discussion to battery-supported standby. The indexed primary scan identifies printed pp. 5-7 and 5-8 and describes several elements of that transition path:

- low-power standby design is treated as a `non-volatile semiconductor memory system` problem whose requirements include retention time, standby load current, battery size, and active access/cycle time;
- two basic power-switching arrangements are discussed for transferring the memory between the main supply and a battery;
- in the switch-coupled example, detection of main-power loss opens the main-supply path and the battery then supplies the memory array;
- a `POWER VALID` signal is required early enough that the main DC source has not already fallen below the minimum ordinary operating voltage;
- a dedicated power-loss-detect circuit is described as an advance-warning mechanism for orderly system shutdown;
- elsewhere in the 5101 interface discussion, `CE2` is required high for operation and low for standby/power-down, and the design guidance explicitly focuses on keeping interface circuitry from wasting the standby power source.

**Primary anchor:** Intel Corporation, *Memory Design Handbook*, May 1977, 5101 systems-considerations discussion, especially printed pp. 5-7–5-8. Archival scan: <https://www.bitsavers.org/components/intel/_dataBooks/1977_C-160_memDesignHb_May77.pdf>. A smaller mirror is indexed at <https://deramp.com/downloads/mfe_archive/050-Component%20Specifications/Intel/Memory%20Components/>.

### Source-inspection boundary

The Bitsavers PDF endpoint returned HTTP 403 when opened directly in this run, while the Deramp PDF could be opened but its screenshot fetch returned a cache error. Search indexing nevertheless exposes the relevant primary-source text, printed page number, and figure descriptions.

Accordingly:

- `indexed primary handbook text` **≠** `fresh direct facsimile inspection`;
- this note records the 1977 handbook as a period-vendor engineering source with precise printed-page locators;
- no component value, waveform geometry, or drawing-specific detail is inferred beyond what the indexed source text states.

Direct facsimile inspection remains worthwhile archival cleanup, but the system-transition claim does not depend on reproducing a diagram from memory.

---

## Engineering reconstruction

### E — retention is a transition protocol, not only a cell voltage

Taken together, the 1975 data sheet and the 1977 systems guidance support a bounded reconstruction:

```text
ordinary +5 V service
        ↓
deselect / place interface in standby condition
        ↓
preserve a valid supply path while main power fails
        ↓
substitute battery / retention-supporting supply
        ↓
state remains under the specified retention condition
        ↓
restore ordinary supply
        ↓
observe the specified recovery interval
        ↓
resume normal read/write service
```

The retained binary relation may be quiescent at the cell level, but the **continuity of the condition that allows it to remain** can depend on board-level switching and control.

This gives a sharper formulation than `SRAM needs power`:

> **a static cell can require no scheduled state refresh while a system still performs event-triggered retention work at the power boundary.**

That work is different from DRAM refresh. The bit is not periodically rewritten because time passed. Instead, the system must preserve the electrical preconditions under which the static relation remains valid when the ordinary supply disappears.

---

## Three distinctions added by the 5101 transition path

### E — `retention-supporting supply` is a relation, not merely a voltage number

The 1975 `2.0 V` figure is not a self-sufficient statement that `2 V means data survives` under arbitrary pin conditions. Intel specifies retention current with `CE2` in the deselected low condition and separately specifies recovery into operation.

For this bounded device family, the retention condition therefore includes at least:

```text
supply condition
+ deselection / interface condition
+ bounded environmental/specification conditions
+ later recovery before normal service
```

This does not imply that every SRAM has the same standby protocol.

### E — `retained` is not identical to `immediately serviceable`

The data sheet explicitly inserts an operation-recovery interval between low-voltage retention and normal service. The 1977 handbook similarly requires a controlled return from the retention path before treating the memory as ordinarily usable.

So the project can now sharpen a previous Case-07 result:

> **state continuity can survive across a period in which ordinary service is intentionally suspended.**

This is an engineering availability distinction, not a Heideggerian claim.

### E — no-refresh operation can still have event-triggered infrastructure

The 5101 is static precisely in the bounded sense that Intel does not require periodic refresh timing merely to preserve the state. Yet battery-backed continuity recruits:

- supply switching;
- power-loss detection;
- a `POWER VALID` control relation;
- chip deselection / standby interface discipline;
- a battery sized for the required retention interval and load;
- a defined recovery path.

Thus:

> **`no periodic refresh` ≠ `no retention infrastructure`.**

This is a distinct maintenance trigger from the deadline-driven refresh obligation in grounded DRAM.

---

## Failure / forgetting boundary

### H/P

Intel specifies the conditions under which retention is guaranteed and describes system circuitry intended to move the memory into those conditions before ordinary power becomes invalid.

### E

The safe claim is therefore about **loss of guarantee / loss of the supported retention path**, not an invented transistor-level failure threshold.

Potential system-level failure classes include:

1. **late power-loss detection** — the system fails to enter its protected transition before ordinary operating voltage is no longer guaranteed;
2. **failed supply substitution** — the battery/switching path does not maintain a valid retention-supporting supply;
3. **interface-state failure** — the chip is not held in the documented standby/deselected condition;
4. **premature re-entry** — ordinary service resumes without satisfying the documented operation-recovery relation;
5. **battery exhaustion / undersizing** — the external energy source no longer satisfies the retention interval/load requirement.

The primary sources do **not** justify claiming exactly which internal transistor flips first, an exact data-loss voltage below the guaranteed floor, or a universal SRAM brownout mechanism.

This is important for the repository's forgetting vocabulary:

> **failure of retention infrastructure can make state continuity unsupported even when the storage cell is not being periodically refreshed and no explicit erase operation occurred.**

---

## Historical / conceptual boundary

### H/P

Intel itself uses terms such as `static`, `data retention`, `standby`, `battery backup`, `power switching`, and `power loss detect` in the bounded sources.

### E

The project term **event-triggered retention infrastructure** is an engineering comparison: the event is loss/restoration of ordinary power, and the work is to preserve or re-establish the conditions for state continuity.

### A

It is useful to compare this with:

- DRAM's deadline-driven refresh;
- RADOS's failure-triggered repair;
- mapped Flash's capacity/reclamation-triggered maintenance.

The trigger families are functionally comparable. They are not one historical mechanism and should not be presented as a genealogy.

### I

The case reinforces the repository's broader distinction between **retention** and **availability**: a state can remain technically retained while the device is intentionally outside normal active service. No philosophical vocabulary is attributed to Intel.

---

## Promotion consequence for Case 07

This run materially deepens the Intel-device-specific failure/hold side of Case 07, but it does **not** promote the case to `grounded`.

What is now stronger:

- a device-specific low-voltage retention boundary is tied to explicit standby/control conditions;
- operation recovery is part of the documented state-continuity path;
- a near-period Intel design handbook shows the board-level battery/power-loss infrastructure that sustains the 5101 family across ordinary power failure;
- failure analysis can now distinguish loss of the supported retention transition from transistor-level decay or noise-margin failure.

What remains open:

1. direct facsimile inspection of Vadasz–Chua–Grove 1971 pp. 43 and 47;
2. a primary Intel 1101/1101A/2102 cell schematic/design disclosure, or directly interpretable Intel artifact evidence sufficient to ground the exact static-cell mechanism;
3. a **cell-level** Intel-specific electrical margin account if the case is to make transistor/noise-margin claims rather than only package/system retention-condition claims;
4. cache policy/interface semantics remain deferred.

The Case-07 status therefore remains `first-pass`. The correct next move is still cell-level Intel primary evidence, not a generic cache survey.

---

## Claim ledger

| Claim | Type | Status |
| --- | --- | --- |
| Intel 1975 specifies ordinary 5101-family operation at 5 V ±5% and a separate 5101L low-voltage retention condition down to 2.0 V | H/P | supported |
| the 5101L retention-current specification is conditioned on `CE2 <= 0.2 V` | H/P | supported |
| Intel specifies a separate operation-recovery time after data retention | H/P | supported |
| Intel's 1977 handbook treats 5101 battery-backed standby through power switching, power-loss detection, standby interface conditions, and battery sizing | H/P | supported by indexed primary handbook text with printed-page locators; direct facsimile inspection remains cleanup |
| the 5101L is intrinsically nonvolatile with zero external energy | X | contradicted by the battery/retention-supply model |
| `2.0 V` alone guarantees retention regardless of control pins or transition sequencing | X | unsupported |
| no-refresh static operation implies no retention maintenance infrastructure | X | contradicted at system level |
| loss of the documented transition path proves a particular transistor-level data-loss mechanism | X | unsupported |
| Case 07 can now be promoted without Intel-specific cell-mechanism evidence | X | not established |

---

## Related-repository check

A fresh search in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `5101`, `SRAM`, `static RAM`, and Intel data-retention terms still found no dedicated static-semiconductor case to reuse. Broad semiconductor-memory engineering history remains routed there; this note contributes only the retention-specific power-transition comparison needed by Case 07.

---

## Sources

1. Intel Corporation, *Intel Data Catalog*, 1975, 5101 / 5101L section, printed pp. 2-115–2-118. <https://deramp.com/downloads/mfe_archive/050-Component%20Specifications/Intel/Memory%20Components/1975_Intel_Data_Catalog.pdf>
2. Intel Corporation, *Memory Design Handbook*, May 1977, 5101 systems-considerations discussion, especially printed pp. 5-7–5-8. <https://www.bitsavers.org/components/intel/_dataBooks/1977_C-160_memDesignHb_May77.pdf>
3. Deramp Intel memory-component archive index, hosting a smaller scan of the 1977 handbook. <https://deramp.com/downloads/mfe_archive/050-Component%20Specifications/Intel/Memory%20Components/>