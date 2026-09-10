# Evidence 140 — IBM 1991–1994 double-disk-failure array codes

## Scope

This record grounds a bounded extension of the repository's RAID/rebuild line: early-1990s IBM work that explicitly protected a disk/DASD array against **up to two unavailable members**, followed by the 1994 EVENODD paper framed for "RAID architectures".

It does **not** establish a complete RAID-6 genealogy, a first-use date for the term `RAID-6`, commercial deployment in a named controller, or equivalence between every two-redundancy array code. The historical sources use their own vocabulary — `double disk failures`, `up to two unavailable DASDs`, and later `RAID architectures`. `RAID-6` is used here only as a later functional comparison where explicitly identified as such.

## Claim-layer labels

- `H/P` — historical record from an original publisher/institutional page or public patent record.
- `H/P*` — historical primary patent text inspected through a public patent mirror rather than an origin-host facsimile.
- `E` — engineering reconstruction made explicit from the cited mechanism.
- `A` — bounded functional analogy to another repository case or later terminology.
- `X` — counterexample or stop condition preventing an overclaim.

## Source ladder

| Source | Date represented | Strength | What it can establish | What it cannot establish |
|---|---:|---|---|---|
| IBM Research, Mario Blaum, *A coding technique for recovery against double disk failures in disk arrays*, IEEE ICC 1992 | 1992-06-14 | `H/P` | an IBM-affiliated conference disclosure explicitly protecting against two disk failures with two redundant disks and XOR-only encoding/decoding | commercial deployment; term `RAID-6`; absolute invention priority |
| EP0499365A2 / US07/653,596 family, *Data processing system and method for encoding and rebuilding data contents of unavailable DASDS* | priority 1991-02-11; EP publication 1992-08-19 | `H/P*` | a patent-family record for coding/rebuilding up to two unavailable DASDs; row/diagonal parity; spare rebuild; explicit distinction among errors, erasures, failed members, degraded mode, and return toward fault tolerance | that the 1991 priority filing was publicly available in 1991; product shipment; later `RAID-6` nomenclature |
| IBM Research, Blaum, Brady, Bruck, Menon, *EVENODD: An optimal scheme for tolerating double disk failures in RAID architectures*, ISCA 1994 | 1994-04-18 | `H/P` | the named EVENODD scheme; up to two disk failures; two redundant disks; XOR-only operations; authors' scoped optimality and parity-hardware claims | universal priority over all double-failure codes; named controller support; measured production behavior |
| Plank, *The RAID-6 Liberation Codes*, FAST 2008 / USENIX | 2008 | scholarly later context | a later explicit `RAID-6` usage for a k+2 arrangement designed to survive any two device failures; P/Q terminology in a modern coding discussion | retroactive proof that 1991–1994 sources themselves used `RAID-6`; direct genealogy from IBM work |

## Source 1 — 1991 priority / 1992 publication patent-family floor

Public patent record:

- EP0499365A2, *Data processing system and method for encoding and rebuilding data contents of unavailable DASDS*
- Google Patents mirror: <https://patents.google.com/patent/EP0499365A2/en>
- listed priority date: **1991-02-11**
- EP filing date: **1992-01-23**
- EP publication date: **1992-08-19**
- listed inventors: Miguel Mario Blaum, Hsieh Tung Hao, Richard Lewis Mattson, Jaishankar Moothedath Menon
- assignee: International Business Machines Corporation
- family record points to U.S. application 07/653,596 and later US5271012A.

The abstract directly describes encoding an array of `M` synchronous DASDs so that data can be rebuilt onto spare DASD capacity when **up to two DASDs fail**. The mechanism uses an `(M-1) × M` logical data array, pairs of simple parities along diagonal and intersecting row directions, and reconstruction followed by writing rebuilt material back across `M` DASDs including spare capacity.

The description is especially useful because it distinguishes several relations that later summaries often collapse:

1. **availability / failed-member identity** — DASDs can become unavailable;
2. **data error** — a stored value can change because of noise/burst processes;
3. **erasure** — a storage location's data value can be absent;
4. **coding redundancy** — parity relations make missing content reconstructable;
5. **spare substitution and rebuild** — a replacement path is selected and reconstructed data can be written onto it;
6. **degraded mode** — the period after failure and before restoration of the former information state.

The patent text explicitly seeks degraded operation in the presence of a second DASD failure and a return toward fault tolerance by rebuilding onto spare capacity. It also states that reconstruction can be scheduled or opportunistic and that the subsystem's risk during redo/rebuild must be traded against throughput.

### Historical boundary

The **1991-02-11 date is a priority date**, not evidence that the patent text was publicly disseminated on that date. The inspected EP publication is dated **1992-08-19**. The ICC paper below gives an independently citable public conference disclosure dated 1992-06-14.

### Engineering reconstruction

For Case 17's single-parity regime, a stripe with one unavailable member has one unknown value and one independent parity relation capable of reconstructing it. Two arbitrary unavailable members introduce two unknown members; one ordinary parity relation does not uniquely determine both. A two-failure code therefore requires additional independent redundancy structure. (`E`)

This is a relation among coded symbols, not two full payload copies. Two redundant DASDs are **not** equivalent to mirroring the whole array. (`E`, `X`)

If the code's stated failure model allows up to two located unavailable members, then after the first member becomes unavailable the encoded object still has one additional member-failure margin within that model. That is a larger residual margin than the single-parity Case 17 regime after its first failure. It still does **not** mean repair is unnecessary: rebuilding onto a spare restores the designed physical redundancy embodiment and removes the system from the reduced-margin state. (`E`, `A`)

## Source 2 — ICC 1992 conference disclosure

IBM Research publication page:

<https://research.ibm.com/publications/a-coding-technique-for-recovery-against-double-disk-failures-in-disk-arrays>

IBM Research dates Mario Blaum's IEEE ICC 1992 paper to **1992-06-14**. Its abstract states that the disk array is encoded so information is protected against **two disk failures**, requiring **two redundant disks**. It further says the encoding and decoding circuits use only exclusive-OR operations, contrasted with schemes requiring finite-field operations such as Reed–Solomon.

This is enough to ground all of the following, but no more:

- a 1992 IBM-affiliated published disk-array technique explicitly targeted two disk failures; (`H/P`)
- it used two redundant disks; (`H/P`)
- it was presented as XOR-only in encoding/decoding circuitry; (`H/P`)
- its paper wording does not, in the inspected abstract, call the arrangement `RAID-6`; (`H/P`, `X`)
- `two redundant disks` describes redundancy quantity, not two replicas of every data disk. (`E`)

The abstract calls this redundancy quantity/performance `optimal`. That historical wording should not be silently expanded into optimal rebuild time, IOPS, latency, controller scheduling, failure probability, or operational recovery. (`H/P`, `X`)

## Source 3 — EVENODD at ISCA 1994

IBM Research publication page:

<https://research.ibm.com/publications/evenodd-an-optimal-scheme-for-tolerating-double-disk-failures-in-raid-architectures>

IBM Research dates the ISCA paper to **1994-04-18**. The abstract introduces a named method, **EVENODD**, for tolerating up to two disk failures in **RAID architectures**. It says EVENODD:

- adds only two redundant disks;
- consists of simple XOR computations;
- is, in the authors' wording, the first known double-disk-failure scheme optimal with regard to both storage and performance;
- requires parity hardware of the sort typically present in then-standard RAID-5 controllers and therefore, according to the paper, can be implemented without hardware changes;
- contrasts this with a previously known two-extra-disk Reed–Solomon approach requiring finite-field computation.

### Priority and implementation stop conditions

The authors' `first known` claim is preserved **as their scoped 1994 claim**, not upgraded into an independently established universal invention priority. The same abstract explicitly acknowledges prior Reed–Solomon-based optimal-storage approaches. (`H/P`, `X`)

Similarly, "can be implemented" on standard RAID-5 parity hardware is an implementation-primitive claim. It is **not** evidence that a named shipping RAID-5 controller actually supported EVENODD in firmware, exposed two-failure semantics, or was validated under production fault injection. (`H/P`, `X`)

`XOR-only` also does not make EVENODD functionally identical to ordinary single-parity RAID-5. Reusing XOR/parity hardware says something about computational primitives; the second independent redundancy relation changes the reconstructability relation. (`E`, `X`)

## Source 4 — later `RAID-6` terminology, used only as a functional comparison

USENIX FAST 2008, James S. Plank, *The RAID-6 Liberation Codes*:

<https://www.usenix.org/conference/fast-08/raid-6-liberation-codes>

The paper explicitly describes RAID-6 as a storage arrangement with `k+2` devices/nodes intended to tolerate any two device failures, with two coding devices often denoted `P` and `Q` in the detailed exposition.

This later source is useful for **terminological comparison only**. It does not prove that the 1991 patent family, the 1992 ICC paper, or EVENODD's authors used `RAID-6` as their contemporary label, nor does it establish a direct genealogy. (`A`, `X`)

## Cross-case comparison

### Case 17 — single-parity RAID reconstruction

Case 17's bounded regime is one unavailable member protected by single parity. After that first failure, the array may still serve reconstructable data, but another independent member failure in the same single-parity protection domain can exceed the code's reconstructability.

Case 140 changes one variable: the coding relation is explicitly designed for up to two unavailable disks/DASDs. Within that stated model:

`healthy two-failure code → first member unavailable → data still reconstructable + one member-failure margin remains → rebuild onto spare → full designed physical redundancy restored`

This is a **functional contrast**, not a claim that Case 140 is simply "Case 17 plus one parity disk" in every implementation detail. (`A`, `X`)

### Case 136 — rebuild scheduling policy

Case 136 studies how a controller allocates foreground/service resources to rebuild and what policy survives reboot/configuration events. Case 140 studies the earlier coding/reconstructability boundary that determines **whether** two unavailable members remain mathematically recoverable. Coding capability does not determine rebuild rate, wall-clock exposure, IOPS interference, or scheduler policy. (`A`, `X`)

### Later erasure-coded distributed systems

Later distributed erasure-coded systems share the broad relation `redundancy relation → reconstruct missing fragments`, but add placement, failure-domain, membership, currentness, repair-traffic, and protocol concerns. No genealogy is inferred from this functional similarity. (`A`, `X`)

## Retention relevance

This slice contributes one narrow retention claim:

> **Future failure margin can be retained as a distributed coding relation rather than as an extra complete copy.**

After one member disappears, the remaining members can retain not only enough information to reconstruct the current logical payload but, in a two-failure code, enough independent redundancy relation to survive one additional located member loss within the code's model. That remaining margin is a state of the **relation among fragments**, not a property of any single surviving disk.

Repair remains a separate temporal process because the system can be reconstructable while operating with less than its designed maximum margin. `Recoverable now != fully repaired != full future-failure margin restored.` (`E`)

## Counterexamples and stop conditions

- **Two-disk-failure tolerance != two replicas.** Redundant coding disks do not each contain complete payload copies. (`E`, `X`)
- **Known/unavailable member recovery != arbitrary silent-corruption correction.** The sources discuss failed/unavailable disks and distinguish error/erasure concepts; do not claim the code automatically locates every silent error. (`H/P*`, `E`, `X`)
- **Two redundant disks != all two-parity schemes are identical.** The 1991-family row/diagonal scheme, Reed–Solomon alternatives, and 1994 EVENODD have different coding structures. (`H/P`, `X`)
- **1991 priority != 1991 public disclosure.** Public chronology must distinguish filing/priority from publication. (`H/P*`, `X`)
- **Double-disk-failure scheme != source-era use of the label RAID-6.** Later RAID-6 terminology is a functional comparison only. (`A`, `X`)
- **Authors' optimality claim != universal systems optimality.** Do not infer shortest rebuild time, lowest latency, safest operations, or lowest real-world failure risk. (`H/P`, `X`)
- **Parity-hardware compatibility != named product deployment.** A paper's implementability statement is not a shipment record. (`H/P`, `X`)
- **Rebuild != sanitization.** Writing reconstructed data to a spare restores redundancy but says nothing about secure erasure of the failed/removed member. (`E`, `X`)

## Open debt

This bounded slice intentionally leaves open:

1. the full Reed–Solomon → array-code → EVENODD / RDP / later RAID-6 genealogy;
2. exact proposal/publication chronology before the 1991 IBM patent-family priority;
3. named production-controller or product deployments of the inspected IBM schemes;
4. controller behavior under a second failure during an active rebuild;
5. silent-sector-error / URE detection and location semantics versus known failed-member reconstruction;
6. rebuild bandwidth, degraded-read cost, and fault-injection measurements;
7. the broader history of the `RAID-6` name and standards usage.

Those mechanism/history questions are appropriate for `tmzncty/computing-archaeology` if developed. A fresh repository search during this slice found no dedicated `EVENODD`, `double disk`, or RAID double-parity study there, so this repository keeps only the retention-specific reconstructability / residual-margin boundary.
