# Case 139 grounding — LPDDR3→LPDDR4 per-bank refresh target authority

## Purpose

This record grounds one bounded comparison for [`../cases/139-lpddr3-lpddr4-per-bank-refresh-target-authority.md`](../cases/139-lpddr3-lpddr4-per-bank-refresh-target-authority.md):

> LPDDR3's inspected `REFpb` regime uses a fixed device-bank-counter sequence while LPDDR4's inspected regime lets the controller transmit the bank address and choose bank order, subject to complete bank coverage before repetition and synchronized controller/device bank-count bookkeeping.

It does not attempt a full LPDDR genealogy or an invention-priority claim.

## Provenance note

The exact historical clause bodies below were recovered from publicly accessible mirrors rather than directly from JEDEC/Micron origin servers. They are therefore labeled `H/P*` rather than silently promoted to origin-hosted primary artifacts.

For the Micron documents, the recovered pages expose manufacturer title, document identifier/revision, copyright line, and detailed command semantics. JEDEC-text mirrors expose the standard number/revision and standard body. The same semantic transition appears in both standards-text copies and Micron product documentation, which makes the bounded mechanism comparison robust while leaving provenance/facsimile cleanup open.

Current AMD and Microchip documentation is first-party implementation evidence for modern controller-facing implications only. It is not used to rewrite the historical standards record.

## Source A — JEDEC JESD209-3B, August 2013

**Artifact:** JEDEC Standard No. 209-3B, *Low Power Double Data Rate 3 (LPDDR3)*, August 2013.

**Access used:** https://studylib.net/doc/28331319/jesd209-3b

**Evidence class:** `H/P*` — standards text through a third-party mirror.

The recovered title page identifies `JESD209-3B`, August 2013, JEDEC Solid State Technology Association. The refresh section states:

- `REFpb` performs per-bank refresh to the bank scheduled by a **bank counter in the memory device**;
- bank sequence is fixed sequential round-robin `0-1-2-3-4-5-6-7-0-1-...`;
- controller and SDRAM synchronize bank count by resetting it to zero;
- synchronization can occur on RESET or every exit from self refresh;
- the controller must track the bank being refreshed;
- target bank must be idle;
- other banks remain available subject to refresh timing;
- a full cycle of eight `REFpb` commands may substitute for one `REFab` for refresh-accounting purposes;
- per-bank refresh has a larger postpone/pull-in command count because one all-bank-equivalent cycle contains eight bank operations.

### Claims supported

- **H/P***: by JESD209-3B, the inspected LPDDR3 per-bank target order is device-counter-scheduled and fixed round robin.
- **H/P***: controller tracking exists despite the fixed device-side bank-selection sequence.
- **H/P***: bank-count synchronization is a named interface relation.
- **H/P***: per-bank target/service geometry differs from all-bank refresh.

### Claims not supported

- first invention of per-bank refresh;
- first LPDDR revision with this behavior;
- internal transistor implementation of the bank counter;
- any claim that controller tracking means controller chooses arbitrary target order.

## Source B — Micron 178-Ball Single-Channel Mobile LPDDR3, Rev. D 9/14

**Artifact:** Micron Technology, *178-Ball, Single-Channel Mobile LPDDR3 SDRAM*, Rev. D 9/14, recovered document identifier/file stem `09005aef858e9dd3 / 178b_8-16gb_2c0f_mobile_lpddr3.pdf`.

**Access used:** https://dtsheet.com/doc/1384705/178-ball--single-channel-mobile-lpddr3-sdram

**Evidence class:** `H/P*` — manufacturer-authored product text through a third-party mirror.

The recovered Micron refresh section repeats the key LPDDR3 relation at product level:

- `REFpb` targets the bank scheduled by the **bank counter in the memory device**;
- the sequence is fixed `0-1-2-3-4-5-6-7...`;
- synchronization resets the bank count to zero on RESET or self-refresh exit;
- controller must track the currently refreshed bank.

It also preserves the timing/accounting context: per-bank commands can be postponed/pulled in in groups scaled by the eight-bank cycle, but temporal flexibility does not change the fixed target sequence.

### Claims supported

- **H/P***: a named Micron 2014 LPDDR3 product family implements/documents the fixed device-bank-counter interface semantics.
- **E**: target tracking and target choice are separate controller responsibilities in this regime.

### Claims not supported

- exact silicon counter topology;
- universal behavior of every vendor's LPDDR3 device;
- standards priority/genealogy.

## Source C — JEDEC JESD209-4B, 2017

**Artifact:** JEDEC Standard No. 209-4B, *Low Power Double Data Rate 4 (LPDDR4)*.

**Access used:** https://studylib.net/doc/27908019/jesd209-4b

**Evidence class:** `H/P*` — standards text through a third-party mirror.

The recovered LPDDR4 refresh section states a different target-selection relation:

- a `REFpb` bank address is transferred on the command/address interface;
- the eight banks may be issued in **any order**;
- the standard gives deliberately nonsequential examples;
- repeating the same bank is illegal until all eight banks have been refreshed;
- the count begins after a synchronization event;
- controller and SDRAM bank counts synchronize to zero on reset/self-refresh exit;
- `REFab` also synchronizes the bank count;
- after synchronization, the controller can issue `REFpb` in any order;
- target bank must be idle and is inaccessible during `tRFCpb`, while other banks can be accessed subject to timing.

### Claims supported

- **H/P***: by JESD209-4B the controller supplies an explicit bank target for `REFpb` and may choose bank ordering.
- **H/P***: this freedom is bounded by a complete-coverage-before-repeat rule.
- **H/P***: synchronized bank-count state remains despite arbitrary controller target order.

### Claims not supported

- that 4B was the first LPDDR4 revision to contain the rule;
- committee rationale or proposal genealogy;
- invention priority.

## Source D — Micron 200b x16/x32 LPDDR4/LPDDR4X, Rev. D 3/20

**Artifact:** Micron Technology, *200b: x16/x32 LPDDR4/LPDDR4X SDRAM*, `CCM005-554574167-10522`, Rev. D 3/20, ©2017 Micron Technology.

**Access used:** https://atta.szlcsc.com/upload/public/pdf/source/20201117/C907715_2114FBF6DFC7A015B06DF2675C9B2C1D.pdf

**Evidence class:** `H/P*` — manufacturer-authored PDF through an electronics-distributor mirror.

### Precise locations inspected

- PDF printed p.122 / parsed lines around 8277–8297: `REFRESH Command`, command encoding, controller-transferred BA, arbitrary order, repeat prohibition, synchronization events.
- printed pp.122–123 / parsed lines around 8295–8340: Table 105, `Bank and Refresh Counter Increment Behavior`.
- printed p.123 / parsed lines around 8342–8368: bank idle requirement, controller tracking, target lockout, other-bank access, timing constraints.
- printed p.125 / parsed lines around 8448–8466: postponement/pull-in accounting, including per-bank scaling.

The browser's page-image screenshot fetch for this mirror was attempted but failed with a cache-miss error; the searchable PDF text and document metadata were still recoverable. No visual-only claim is used.

### Key historical observations

1. **Controller-transferred bank address**

   Micron says `BA0`, `BA1`, and `BA2` are transferred on `CA0`, `CA1`, and `CA2` for `REFpb`.

2. **Arbitrary order with bounded coverage**

   The document gives `1-3-0-2-4-7-5-6` as a legal example and says a bank cannot be repeated until all eight have been refreshed.

3. **Synchronized bank-count phase**

   Reset procedure, self-refresh exit, and `REFab` can synchronize the bank count to zero. `REFab` can interrupt an incomplete per-bank cycle and establishes a new bank-count phase.

4. **Bank counter != row refresh counter**

   Table 105 exposes both a bank-counter field and a refresh/row-counter field. Across eight `REFpb` operations the bank coverage counter cycles while the row-refresh relation advances. A `REFab` resets bank-count phase while operating according to the row counter.

5. **Target-local blocking**

   Target bank is inaccessible during `tRFCpb`; other banks can remain active or receive reads/writes subject to timing.

6. **Temporal accounting remains separate**

   The same section retains `tREFI`-based refresh requirements and bounded postponement/pull-in. Target-order choice therefore does not erase the time-domain maintenance obligation.

### Claims supported

- **H/P***: LPDDR4 product-level controller bank-target selection and arbitrary ordering.
- **H/P***: full-bank-set coverage rule before repetition.
- **H/P***: controller/device bank-count synchronization events.
- **H/P***: target bank lockout and conditional other-bank access.
- **E**: bank-target phase and row-refresh phase are distinct control relations.
- **E**: scheduling freedom and coverage/deadline obligations are distinct.

### Claims not supported

- physical implementation of internal row/bank counters;
- cross-vendor silicon identity;
- error behavior if controller/device bookkeeping becomes desynchronized;
- a guarantee that arbitrary ordering improves application performance.

## Source E — AMD PG313 LPDDR4 Refresh Options, 2026-06-23

**Artifact:** AMD, *Versal Adaptive SoC Programmable Network on Chip and Integrated Memory Controller 1.1 LogiCORE IP Product Guide (PG313)*, `LPDDR4 Refresh Options`, Release Date 2026-06-23.

**Access used:** https://docs.amd.com/r/en-US/pg313-network-on-chip/LPDDR4-Refresh-Options

**Evidence class:** `H/P` for a later named controller implementation; **not** a historical LPDDR4-origin source.

AMD says its DDRMC supports all-bank and per-bank LPDDR4 refresh. During per-bank refresh other banks remain available. It also warns that the performance result depends strongly on traffic pattern/address mapping and can in some cases be worse than all-bank refresh.

### Methodological use

This is valuable primarily as a counterexample to an easy engineering overclaim:

> **per-bank concurrency opportunity != guaranteed performance improvement**.

It does not establish 2013/2017 historical standard wording or first deployment.

## Source F — Microchip UDDRC Refresh Control Register 0

**Artifact:** Microchip current online controller documentation, `UDDRC Refresh Control Register 0`.

**Access used:** https://onlinedocs.microchip.com/oxy/GUID-999BFD8D-CFE5-4F54-AF70-76475125B7FB-en-US-2/GUID-BE25A87E-A9A0-465E-8403-4C64CED59221.html

**Evidence class:** `H/P` for a current controller interface; not historical origin evidence.

The controller exposes a static `PER_BANK_REFRESH` configuration for LPDDR2/LPDDR3-capable designs, notes that per-bank refresh allows traffic to other banks, and separately encodes postponed-refresh behavior.

### Methodological use

- later implementation evidence that mode choice and scheduling/accounting are controller-visible policies;
- corroborates that target-local concurrency does not mean ordinary DDR2/DDR3 rank refresh had the same geometry;
- must not be back-projected as the exact implementation of the 2013/2014 LPDDR3 products.

## Relation decomposition

The evidence supports the following bounded chain:

```text
physical dynamic-cell retention obligation
    !=
recurring REFRESH command generation
    !=
per-command bank-target selection
    !=
controller/device bank-coverage phase
    !=
internal row-refresh phase
    !=
command timing / postpone-pull-in debt
    !=
target/non-target service availability
```

### LPDDR3 inspected regime

```text
controller issues REFpb
    -> device bank counter chooses next fixed-round-robin bank
    -> controller tracks that implied target
    -> DRAM performs internal row-refresh work
    -> shared phase advances
```

### LPDDR4 inspected regime

```text
controller chooses/transmits bank address
    -> legality depends on current eight-bank coverage phase
    -> target bank is refreshed / temporarily blocked
    -> internal row-refresh relation remains distinct
    -> after all banks covered, next target-order set may differ
```

The transition is therefore not `device refresh -> controller refresh`. It is a narrower repartitioning of **bank-target scheduling authority**.

## Claim ledger

| Claim | Class | Strength | Evidence |
| --- | --- | --- | --- |
| JESD209-3B / Micron LPDDR3 use device bank counter for fixed `REFpb` order | `H/P*` | strong bounded | A, B |
| LPDDR3 controller must still track current refreshed bank | `H/P*` | strong bounded | A, B |
| JESD209-4B / Micron LPDDR4 accept controller-transferred bank address and arbitrary eight-bank order | `H/P*` | strong bounded | C, D |
| LPDDR4 arbitrary order remains constrained by all-eight-before-repeat rule | `H/P*` | strong bounded | C, D |
| bank-count synchronization and row-refresh enumeration are distinct | `H/P*`, `E` | strong bounded | D |
| target-order freedom does not remove tREFI/deadline accounting | `H/P*`, `E` | strong bounded | C, D |
| other-bank accessibility does not mean zero timing interference | `H/P*`, `E` | strong bounded | A–D |
| per-bank scheduling does not guarantee better workload performance | `H/P`, `E` | named later implementation | E |
| LPDDR4 `REFpb` == DDR5 `REFsb` | `X` | rejected | Case 33 + D |
| LPDDR4 is first per-bank-refresh technology | `X` | rejected | A, B and earlier LPDDR2 evidence |
| exact controller/device desynchronization failure behavior | `X` | ungrounded | requires empirical/controller evidence |
| LPDDR3→LPDDR4 semantics proves direct invention genealogy | `X` | rejected | chronology/interface comparison only |

## Prior-art / genealogy boundary

Earlier LPDDR2 sources also expose per-bank refresh and fixed device-bank-counter sequencing; therefore the LPDDR3 evidence cannot be treated as origin priority. The immediate purpose of LPDDR3 is to establish a clean pre-LPDDR4 control partition with manufacturer/standard wording.

Likewise, the LPDDR4 record establishes a later interface relation, not who proposed or invented it. The missing historical work is proposal/ballot/patent genealogy and comparison of the initial JESD209-4 revision with 4B.

`tmzncty/computing-archaeology` was searched for `per bank refresh LPDDR4` and no dedicated overlapping study was found. Broad LPDDR standards/controller history should be developed there if needed; this repository keeps the retention-specific maintenance-authority comparison.

## Cross-case boundaries

- **Case 09:** refresh-row enumeration/internalization, not bank-target scheduling freedom.
- **Case 21:** external recurring AUTO REFRESH versus internal SELF REFRESH authority, not per-command target-order choice.
- **Case 33:** DDR5 `REFsb` same-bank-position-across-bank-groups geometry, not LPDDR4 single-bank `REFpb` identity.
- **Case 69:** temporal postpone/pull-in elasticity, not spatial target selection.
- **Synthesis 24:** maintenance trigger regime remains separate from target-order policy.
- **Synthesis 26/27:** control-state lifetime/evidence validity can be compared functionally, but no genealogy follows.

## Open evidence debt

- origin-hosted JEDEC/Micron facsimiles for exact historical clauses;
- initial JESD209-4 versus later 4A/4B wording;
- LPDDR2 first-standard/product chronology;
- committee proposals/ballots and relevant patents;
- LPDDR5 target-geometry evolution;
- named-controller traces of bank-target phase;
- deliberate controller/device phase-desynchronization fault injection;
- workload measurements separated from normative command semantics.
