# Case 52 Deepening — SanDisk 2004–2007 Read-Disturb Exposure-Avoidance Prior Art

## Status

**`bounded deepening complete`** for the early SanDisk read-disturb prevention slice described here.

Canonical case: [`../cases/52-nand-flash-read-disturb-access-induced-decay.md`](../cases/52-nand-flash-read-disturb-access-induced-decay.md).

Related Case 52 records:

- [`52-cai-2009-2015-nand-read-disturb-grounding.md`](52-cai-2009-2015-nand-read-disturb-grounding.md)
- [`52-micron-2006-read-disturb-temporary-failure-maintenance-deepening.md`](52-micron-2006-read-disturb-temporary-failure-maintenance-deepening.md)
- [`52-denali-2008-2009-persistent-read-count-checkpoint-deepening.md`](52-denali-2008-2009-persistent-read-count-checkpoint-deepening.md)

## Why this slice exists

Case 52 already grounds NAND read disturb as an access-induced reliability problem and follows later policies that count reads, inspect error margin, relocate data, erase/reprogram a block, or tune read voltage.

That chronology can accidentally make `read disturb management` look as though it naturally means:

```text
allow exposure
    -> count / detect accumulated risk
    -> repair or relocate later
```

Two SanDisk patent families publicly visible by 2005–2007 provide a useful earlier counterexample. They describe designs that try to **avoid creating the dangerous exposure relation in the first place** rather than merely remembering exposure and repairing after a threshold.

The first does so at the allocation/addressability layer: reserve a protected block so that only one word line carries readable/programmed data, leave the other word lines unused, and prevent software or mapping from making those unused physical sectors accessible.

The second does so at the electrical read-path layer: change the NAND read sequence so that channel boosting associated with one form of read disturb is prevented or reduced while read conditions are established.

The bounded result is:

```text
read-disturb mitigation
    !=
necessarily read-count-triggered maintenance

retention margin can be protected by
    reducing / withholding hazardous exposure
as well as by
    detecting exposure and renewing later
```

This record does **not** claim that either patent was the first read-disturb mitigation, nor that a named shipping product used either exact embodiment.

## Source chronology and public-date discipline

### A. `US20050210184A1` — address-space / word-line protection

Jian Chen and Lee M. Gavens, **_Operating non-volatile memory without read disturb limitations_**:

- U.S. application `US10/805,079`;
- filing / priority date: **19 March 2004**;
- assignment record: inventors assigned the application to **SanDisk Corporation on 29 June 2004**;
- U.S. application publication: **US20050210184A1, 22 September 2005**;
- later grant: **US7177977B2, 13 February 2007**.

Primary-family text / metadata:

- <https://patents.google.com/patent/US20050210184A1/en>

The 2004 filing date is used as priority chronology. The public-document floor used here is the **22 September 2005** U.S. publication date. The later assignment metadata supports describing this as a SanDisk-associated manufacturer-primary line by the time of publication; it does not retroactively make every event on filing day public.

### B. `US20070127291A1` — read-path boosting prevention

Yupin Fong, Jun Wan, and Jeffrey Lutze, **_System for reducing read disturb for non-volatile storage_**:

- U.S. application `US11/296,087`;
- filing / priority date: **6 December 2005**;
- U.S. application publication: **US20070127291A1, 7 June 2007**;
- later grant: **US7262994B2, 28 August 2007**.

Primary-family text / metadata:

- <https://patents.google.com/patent/US7262994B2/en>

This second family is used only to establish a different prevention topology already explicit in a manufacturer patent line by 2007. It is not treated as a continuation of the 2004 address-space embodiment unless the family record itself establishes such a relation; the shared company context is not enough to infer a single implementation genealogy.

## Historical record

### H/P — period actors explicitly framed read-mostly code as a disturb problem

`US20050210184A1` does not discuss read disturb only as an abstract device-physics phenomenon. Its background gives workload examples in which code is programmed once and read many times:

- BIOS code read at power-up or reset;
- operating-system code in handheld/mobile devices read repeatedly across device power cycles.

The source says that sufficiently repeated reads can eventually corrupt the code through read disturb.

This matters historically because the problem is stated at the application/workload level by the source itself:

```text
write-once / read-many workload
    -> repeated NAND read exposure
    -> read-disturb risk
```

That is historical actor framing, not a modern reconstruction projected backward.

### H/P — the 2005 publication names several already-recognized mitigation families

The 2005 publication says previous attempts included:

- ECC correction;
- periodic refresh by programming;
- periodically rewriting data to another location.

Its own proposed topology is different: for a protected block, use **one word line** to store/read data and prohibit use of the other word lines.

Therefore by September 2005 the public record already contains at least this explicit contrast:

```text
correct / refresh / rewrite after risk exists
    versus
prevent useful data from occupying exposed neighbors
```

This is a prior-art boundary, not proof that every listed mitigation was commercially widespread or implemented identically.

### H/P — protected blocks intentionally sacrifice usable capacity

The source's example block has multiple word lines and logical pages. For a protected block, data are programmed/read only on the selected word line. Other word lines receive pass voltage during reads and may themselves experience disturb, but the design leaves them without useful stored data.

The text explicitly acknowledges the tradeoff: memory space goes unused while the memory space that is used is protected from read disturb.

This supports a historically explicit relation:

```text
nominal physical cell capacity
    !=
capacity admitted for protected logical use
```

and:

```text
reliability protection
    can be purchased with
intentional address-space / capacity sacrifice
```

This is not modern over-provisioning terminology and should not be renamed as such in the historical layer.

### H/P — access prevention can be implemented above raw cell physics

The 2005 disclosure does not require one single enforcement locus. It describes several possibilities, including:

- software / processor-readable code that allows access to the selected word line and prohibits reads/programs to others;
- a list of allowed/prohibited word lines, blocks, addresses, or logical pages;
- physical-address validation before a read/program/erase operation;
- logical-to-physical mapping in which only sectors on the permitted word line receive LBAs;
- internal-controller blocks that are not exposed in the host mapping.

For protected blocks, sectors on prohibited word lines can simply have **no LBA mapped to them**.

Thus a physical cell can exist in the device while being deliberately excluded from the logical access surface:

```text
physical location exists
    !=
location is logically designated / host-addressable
```

The reason here is reliability, not deletion, sanitization, bad-block retirement, or capacity reclamation.

### H/P — protection-policy metadata can itself be represented in multiple ways

The disclosure says the protected-block list may be fixed in software, stored in Flash, or represented by a flag in block-header information. It further notes that such header information should be kept on the same allowed word line as the protected data so that reading the header does not create the very exposure relation the design is trying to avoid.

This gives an unusually concrete policy-metadata relation:

```text
payload-placement rule
    -> protection metadata / mapping state
    -> future access admission
```

and:

```text
metadata read path
    can itself be part of
retention-risk control
```

The source does **not** specify a crash-consistency, journaling, or recovery protocol for changing that protection metadata.

### H/P — the 2007 family attacks a different cause at read-operation level

`US20070127291A1` / `US7262994B2` describes another read-disturb form associated with channel boosting while read conditions are established. Its disclosed method changes select-gate / word-line sequencing so that channel boosting is prevented or reduced before sensing.

The source's stated purpose is preventive: reduce or remove one form of read disturb by changing the read operation itself.

This establishes another topology:

```text
host asks to read the same logical data
    -> controller / state-machine uses a different electrical sequence
    -> hazardous channel condition is reduced
```

The logical request need not expose the electrical mitigation policy.

### H/P — prevention is mechanism-specific, not a universal claim of zero disturb

The 2007 patent repeatedly qualifies its result as preventing/reducing **a form** of read disturb associated with the described boosting mechanism. It also discusses source-side and drain-side variants.

Therefore the historical record does not support:

```text
one read-sequence mitigation
    -> all read-disturb mechanisms eliminated forever
```

The proper scope is one disclosed mechanism family and its associated read conditions.

## Engineering reconstruction

### E — retention work can occur by denying an otherwise possible state transition

Cases 36, 52, and 67 often show maintenance after a risk metric grows: correct, inspect, relocate, erase/reprogram, or reclaim.

The 2005 SanDisk disclosure supplies a different engineering pattern. It protects the retained payload by **not admitting useful payload into physical neighbors that will receive repeated pass-voltage stress**, and by refusing host/controller accesses that would violate the protected geometry.

The project-level reconstruction is:

```text
retention intervention
    can be restorative work after degradation
or
    preventive control over which exposures are allowed
```

This is a functional classification, not vocabulary attributed to Chen or Gavens.

### E — unused capacity can be retention infrastructure

In the protected-block embodiment, physically manufactured cells remain present but are intentionally unavailable for ordinary payload placement.

Therefore:

> **unused physical capacity != automatically wasted capacity in the engineering sense.**

In this bounded design, withholding capacity is part of the protection mechanism.

This resembles later cases where spare or reserved resources support reliability, but the analogy must remain functional. The 2005 source does not call the unused word lines `over-provisioning`, spare area, or a modern SSD reserve pool.

### E — addressability is part of the reliability boundary

The source makes read-disturb protection depend partly on what addresses software or the mapping layer can resolve into a protected block.

Therefore:

```text
physical ability to address a cell
    !=
policy-authorized addressability of that cell
```

and:

```text
retention safety
    can depend on
retained access-admission / mapping policy
```

This extends Case 52 beyond `how much physical stress has accumulated?` to another question:

> Which future accesses are the controller allowed to create at all?

### E — preventing exposure and remembering exposure are substitute policy dimensions, not equivalents

Denali's later Case 52 embodiment retains a read-count summary across power cycles and moves data when a threshold is reached. SK hynix Case 67 permits a compressed proxy to be reset at power-off if conservative requalification compensates.

The 2005 SanDisk protected-block design can reduce dependence on an accumulated read count by constraining the geometry of useful data/access itself.

The safe comparison is:

```text
exposure avoidance
    !=
exposure counting
    !=
error-margin qualification
    !=
post-exposure renewal
```

Different systems can combine more than one of these.

### E — logical nondestructiveness can be enforced by changing the logical surface, not only the cell

A normal host-level read is expected not to change its requested payload. Read disturb shows that this logical contract does not imply material neutrality in neighboring cells.

The 2005 protected-block design responds by shrinking the set of logically usable physical locations. The 2007 electrical design responds by changing how the read is physically executed.

Thus two different interventions can preserve the same higher-level expectation:

```text
stable logical read service
    <- address-space exclusion
or
    <- altered electrical read sequence
```

They are not technically identical mechanisms.

### E — protection-policy state can become constitutive control state

If a protected block is enforced through an LBA map, block-header flag, or explicit allow/prohibit list, the payload alone is not sufficient to reconstruct the intended safe access regime.

A bounded reconstruction is:

```text
payload physically present
    + protection policy lost / ignored
    -> data may still decode now
    while future access pattern can violate the intended safety regime
```

The source does not present this as a crash-recovery failure mode, so the statement is an engineering implication of the disclosed enforcement topology, not historical evidence of an observed field failure.

## Functional comparisons

### A — Fujitsu 2002-priority / 2003-public read-disturb mitigation

Case 52's Fujitsu witness varies the pass voltage applied to non-selected word lines, balancing disturb suppression against the need to keep cells conductive enough for correct reading.

The SanDisk 2005 protected-block publication instead changes **where useful data are allowed to live and be accessed**.

Functional comparison:

```text
Fujitsu:
    tune electrical read condition for non-selected cells

SanDisk 2005:
    leave exposed neighbor word lines without useful mapped payload
```

This does not prove influence in either direction and does not establish first invention.

### A — Micron 2006 manufacturer design guidance

Micron TN-29-17 later gives several system responses to read-mostly workloads: move execution into volatile memory, keep master/working NAND copies and renew after a system-designated read count, or use ECC margin as an intervention signal.

SanDisk 2005 adds a different public system-policy option before that guidance:

```text
avoid useful-data exposure by protected placement / access exclusion
```

Micron's renewal choices and SanDisk's protected-block topology solve related reliability problems with different capacity, performance, and control-state costs.

No SanDisk→Micron genealogy is claimed.

### A — Denali 2009-public persistent read-count control state

Denali explicitly retains accumulated read exposure in a non-volatile block table and later relocates data.

SanDisk 2005 shows why this generic pattern must not be projected backward as the only controller-level answer:

```text
SanDisk 2005:
    shape the admissible placement/access geometry

Denali 2009 publication:
    remember exposure and trigger relocation
```

The first relies on persistent or otherwise reconstructible **protection policy** in some embodiments; the second relies on retained **exposure summary**. Those are distinct kinds of controller memory.

### A — SK hynix Case 67

Case 67 uses read-count proxies, ECC/bit-error qualification, adaptive thresholds, and conditional reclaim. It therefore belongs to the `measure/qualify/renew` side of the comparison.

The SanDisk evidence adds a prior-art counterweight:

> **A system may preserve margin by preventing a risky relation, not only by measuring how far that relation has progressed.**

This is functional comparison only; it is not a continuous product or algorithm genealogy.

## Philosophical interpretation — bounded

The narrow conceptual result is not that `forbidden addresses are memory` or that unused cells philosophically `remember absence`.

The engineering result is more precise:

> A retained object's future reliability can depend on preserving a rule about what the system must **not** make addressable or executable.

That means technical retention may depend not only on keeping payload and repair history, but also on retaining **negative operational constraints**: locations, operations, or transitions that are intentionally excluded because admitting them would spend reliability margin.

A second bounded interpretation is:

> Availability and preservation can conflict. Making every manufactured location immediately usable can reduce the safety margin of the locations chosen to carry important data.

This is project interpretation. The patent sources are engineering disclosures about NAND operation, not philosophical texts about availability, absence, sacrifice, or memory.

## Historical record / engineering reconstruction / analogy ledger

| Claim | Layer | Evidence boundary |
| --- | --- | --- |
| `US20050210184A1` was publicly published on 22 Sep 2005 | `H/P` | patent-family publication metadata |
| inventors assigned the 2004 application to SanDisk before publication | `H/P` | patent assignment metadata |
| the 2005 publication treats BIOS / operating-system read-mostly workloads as read-disturb risks | `H/P` | explicit background examples |
| the disclosed protected-block embodiment stores/reads useful data on one word line and prohibits use of others | `H/P` | abstract, description, claims |
| unused protected-block sectors can be left without LBA mappings | `H/P` | explicit logical-to-physical mapping embodiment |
| protected-block policy can be represented in software, a Flash list, or block-header flag | `H/P` | explicit alternatives in description |
| the design intentionally trades usable memory space for protection | `H/P` | explicit discussion of unused space vs protection |
| `US20070127291A1` was publicly published on 7 Jun 2007 | `H/P` | patent-family publication metadata |
| the 2007 family changes read sequencing to prevent/reduce channel boosting associated with one disturb form | `H/P` | abstract, description, claims |
| unused word lines are equivalent to modern SSD over-provisioning | `X` | later vocabulary/mechanism would be anachronistic |
| either patent proves a named shipping product used the exact embodiment | `X` | patent disclosure is not deployment evidence |
| the 2005 design requires no retained policy metadata in every embodiment | `H/P` | some enforcement can be compiled/fixed in software; others use Flash/header state |
| losing/ignoring protection policy could re-admit unsafe accesses | `E` | follows from disclosed access-control/mapping role, not field-failure evidence |
| exposure avoidance, exposure counting, ECC qualification, and renewal are functionally different policy dimensions | `A/E` | cross-case comparison; not historical vocabulary |
| reliability can be bought by deliberate reduction of usable address space | `H/P + E` | explicit capacity tradeoff + project reconstruction |

## Explicit non-claims

This record does **not** claim that:

1. SanDisk discovered NAND read disturb;
2. the 19 March 2004 filing date of `US10/805,079` is its public-document date;
3. the 6 December 2005 filing date of `US11/296,087` is its public-document date;
4. `US20050210184A1` is earlier than every Fujitsu, Toshiba, Samsung, SanDisk, or other read-disturb disclosure;
5. a patent assignment record proves commercial deployment;
6. a protected block with intentionally unused word lines is identical to modern SSD over-provisioning;
7. unused word lines are physically unstressed during reads of the allowed word line;
8. the unused cells are erased, sanitized, permanently bad, or incapable of later reuse;
9. the one-word-line policy eliminates every physical read-disturb mechanism;
10. every protected-block embodiment requires mutable non-volatile policy metadata;
11. every header/list update is crash-atomic or journaled;
12. the logical-to-physical mapping described here is a complete modern SSD FTL;
13. restricting addressability and lowering `Vpass` are the same mitigation mechanism;
14. the 2007 anti-boosting read sequence eliminates all forms of read disturb;
15. the 2007 patent proves use of the same implementation in the 2005 protected-block design;
16. the patents establish a direct genealogy into Micron TN-29-17, Denali, Texas Memory Systems, Samsung, SK hynix, or Cai et al.;
17. a read-disturb prevention policy guarantees indefinite retention against leakage, wear, program interference, or other error sources;
18. physical presence of a cell implies it should be host-addressable;
19. physical unaddressability proves physical absence;
20. capacity sacrifice alone is a sufficient universal retention strategy.

## Evidence strength

| Question | Strength | Reason |
| --- | --- | --- |
| Was the protected-block application publicly available by 22 Sep 2005? | **strong** | U.S. publication metadata |
| Did it explicitly discuss NAND read disturb in read-mostly BIOS / OS workloads? | **strong** | explicit description |
| Did it intentionally restrict useful data to one word line in protected blocks? | **strong** | abstract + description + claims |
| Could LBA mapping make prohibited sectors inaccessible? | **strong** | explicit mapping embodiment |
| Could protection state be represented in Flash/header metadata? | **strong** | explicit alternatives in description |
| Did the source acknowledge a capacity cost? | **strong** | explicit `memory space is going unused` tradeoff |
| Was the anti-boosting family publicly available by 7 Jun 2007? | **strong** | U.S. publication metadata |
| Did it change read sequencing to prevent/reduce one channel-boosting disturb mechanism? | **strong** | abstract + detailed read sequence + claims |
| Did either exact design ship in a named product? | **not established** | no named-product deployment evidence inspected |
| How was mutable protection metadata recovered after abrupt power loss? | **open** | no bounded crash/recovery protocol inspected |
| Which policy was more effective in a real workload? | **open** | no controlled comparative product benchmark in this slice |

## Source-lineage and related-repository boundary

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for the exact `US20050210184A1` publication number returned no dedicated reusable packet.

Broader SanDisk NAND-controller history belongs there if developed later, including:

- SanDisk product-line / controller genealogy;
- the 2000–2007 patent-family network for NAND disturb mitigation;
- exact commercial deployment of protected-block or anti-boosting techniques;
- Flash-array architecture and process-node evolution;
- historical relationships among SanDisk, Toshiba, and later joint-venture NAND development;
- performance/capacity economics of reserving word lines in real products.

This record keeps only the retention-specific seam:

```text
read-mostly workload
    -> hazardous physical exposure relation
    -> preventive electrical or addressability control
    -> reduced exposure of the retained payload
    -> capacity / policy-state tradeoff
```

## Remaining evidence debt

1. Find **named shipping product** documentation, firmware, service material, or independent teardown evidence for a controller that used the one-word-line protected-block policy or an equivalent explicit access-quarantine scheme.
2. Determine whether a period public source documents how mutable protected-block metadata was made crash-consistent or reconstructed after power failure.
3. Trace the 2002–2007 SanDisk patent-family network in `computing-archaeology` if actor-to-actor or circuit-genealogy claims become important; do not grow that broad genealogy here.
4. Keep Case 52's separate Denali debt open: this source does **not** establish shipping retention of a per-block read-exposure counter across reset/power loss.
5. If comparing later 3-D NAND read-reclaim, keep detailed controller genealogy in Case 67 unless it changes this prevention-versus-renewal distinction.

## Sources

1. Jian Chen and Lee M. Gavens, **_Operating non-volatile memory without read disturb limitations_**, U.S. application publication **US20050210184A1** (22 September 2005), later grant US7177977B2; filing / priority 19 March 2004; assignment to SanDisk Corporation recorded 29 June 2004: <https://patents.google.com/patent/US20050210184A1/en>.
2. Yupin Fong, Jun Wan, and Jeffrey Lutze, **_System for reducing read disturb for non-volatile storage_**, U.S. application publication **US20070127291A1** (7 June 2007), later grant **US7262994B2** (28 August 2007), priority 6 December 2005: <https://patents.google.com/patent/US7262994B2/en>.
3. Canonical Case 52's earlier Fujitsu 2002-priority / 2003-public witness remains the comparison point for pass-voltage mitigation; Micron TN-29-17 (2006) remains the manufacturer design-guidance comparison for renewal / ECC intervention; Denali US20090193174A1 remains the explicit persistent read-count control-state witness.

## Bounded result

The new prior-art boundary is:

```text
by September 2005 public manufacturer-associated evidence already showed
    NAND read disturb
    + read-mostly workload framing
    + controller/mapping-level access exclusion
    + deliberate capacity sacrifice for protection

by June 2007 another SanDisk line publicly showed
    read-sequence / channel-condition prevention

therefore
    read-disturb management history
    != one inevitable path toward read counters and relocation
```

For `technical-retention`, the important consequence is narrower:

> **Retention policy can preserve future margin either by remembering accumulated hazard and renewing after it grows, or by retaining/enforcing rules that prevent useful state from entering a hazardous access relation in the first place.**
