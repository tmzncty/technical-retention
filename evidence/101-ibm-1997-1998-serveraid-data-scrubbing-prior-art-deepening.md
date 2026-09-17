# Case 101 deepening — IBM ServeRAID data scrubbing before T10 BMS / Dell-LSI Patrol Read

Status: `bounded deepening complete`

## Scope

This evidence packet deepens [`../cases/101-scsi-background-medium-scan-proactive-defect-discovery.md`](../cases/101-scsi-background-medium-scan-proactive-defect-discovery.md) along one narrow historical and engineering seam:

> **Was controller-orchestrated proactive media coverage with redundancy-assisted repair already documented before the 2005 T10 Background Medium Scan work and the 2005 Dell/LSI `Patrol Read` witnesses?**

The answer is yes for a bounded IBM ServeRAID lineage.

The strongest inspected IBM records establish that by **December 1997** IBM was explicitly recommending `Data Scrubbing` to expose latent media defects before a later drive failure made RAID reconstruction impossible, and by **1998** IBM product documentation described controller-level data scrubbing that periodically or continuously reads RAID-1/RAID-5 logical-drive sectors in the background and automatically repairs defective sectors.

The retained-state significance is not merely that an older vendor used another name for `patrol read`. The more important boundary is that IBM's own documentation makes **repair authority depend on the current validity of RAID redundancy**:

```text
sector defect detected
    !=
redundancy known valid
    !=
reconstruction safe
    !=
repair completed
```

IBM warns that if RAID-5 parity has never been synchronized, then scrub-time reconstruction may use incorrect parity and itself produce data loss. Thus proactive discovery does not, by itself, authorize a trustworthy repair.

This packet does **not** claim that IBM invented disk scrubbing, that IBM ServeRAID is the ancestor of T10 BMS or Dell/LSI Patrol Read, or that every later vendor implementation descends from this family.

---

## Source set and custody

### P1 — IBM Server White Paper: hard-drive media defects, December 1997

Current IBM support record:

- `Understanding hard drive media defects white paper - Servers`
- IBM Support UID `ibm1MIGR-50341` / current page title as indexed by IBM Support
- page explicitly identifies the underlying document as **IBM Server White Paper, Date: December 1997**
- current URL: <https://www.ibm.com/support/pages/node/796648>

The retained IBM page states that latent media errors may remain undetected in seldom-used files or unused sectors until those sectors are accessed, and that `Data Scrubbing` performs the needed background access while concurrent user disk activity continues. It points readers to the companion IBM white paper `Using IBM RAID Adapters to Avoid Data Loss` for the recommended procedure.

**Custody note:** the HTML is a later IBM Support presentation of an older IBM white paper. The December 1997 date is printed in the reproduced content itself; the support-page modification/crawl date is not used as the historical date.

### P2 — IBM RAID configuration / data scrubbing support record

Current IBM support record:

- `RAID configuration and data scrubbing to prevent RAID rebuild failure - Servers`
- current URL: <https://www.ibm.com/support/pages/raid-configuration-and-data-scrubbing-prevent-raid-rebuild-failure-servers>

The surviving IBM text ties data scrubbing to specific early IBM RAID adapters and firmware. It states, among other things:

- RAID-5 logical drives should be synchronized before data is stored;
- RAID-5 logical drives should be scrubbed regularly to reduce rebuild/data-loss risk;
- Netfinity Manager 5.0 could run the synchronization-based scrub in the background;
- `Data Scrubbing` runs automatically in the background on the **ServeRAID II Adapter** with firmware **2.30.04 or higher**;
- grown defects in regions not otherwise accessed may remain latent;
- scrub-forced access can expose those defects while redundancy is still available;
- if parity was never correctly synchronized, scrub-time reconstruction may use incorrect parity and produce data loss.

**Custody note:** the current page does not expose a clean original publication date in its header. This packet therefore does not date every sentence on the page to December 1997. It is used together with the dated December 1997 white-paper witness and dated product records below.

### P3 — IBM ServeRAID-3H technical specification, announced 22 September 1998

Current IBM product record:

- `Technical specifications - ServeRAID 3H`
- announce date: **22 September 1998**
- current URL: <https://www.ibm.com/support/pages/technical-specifications-serveraid-3h>

The IBM specification lists as a controller characteristic:

> `Data scrubbing periodically scans disk services and automatically repairs bad sectors on the disk array to enhance data integrity.`

The same product record separately lists hot-swap rebuild, auto-synchronization, and other controller functions.

This is a dated named-product witness that controller-level proactive scanning plus automatic repair was commercially documented in IBM's ServeRAID family before 2005.

### P4 — IBM Netfinity 5500 ServeRAID administration documentation

Current IBM support page:

- `Using the ServeRAID administration functions - Netfinity 5500`
- current URL: <https://www.ibm.com/support/pages/using-serveraid-administration-functions-netfinity-5500>

The reproduced IBM documentation says the ServeRAID controller's data-scrubbing function continuously reads all sections of RAID-1 and RAID-5 logical drives in the background while the system is running; if a defective sector is found, it is automatically repaired. It explicitly contrasts this with manually synchronizing those logical drives on a weekly basis.

IBM's Netfinity 5500 product records identify configurations using the ServeRAID II controller in 1998–1999. For example:

- model 8660-5SU, announced **24 August 1998**, general availability **15 September 1998**: <https://www.ibm.com/support/pages/technical-specifications-8660-5su-netfinity-5500>
- later Netfinity 5500 model records likewise identify `IBM ServeRAID II on planar`.

**Boundary:** the support-page transcription is useful for operational semantics, while the dated model records and P3 provide the stronger chronology anchors. This packet does not infer that every Netfinity 5500 firmware revision behaved identically.

### P5 — IBM SSA RAID Cluster Adapter, December 1997 availability

IBM's December 1997 SSA RAID Cluster Adapter product record lists `Data scrubbing available on arrays` under reliability features:

- planned / available date: **19 December 1997**
- current URL: <https://www.ibm.com/support/pages/overview-ibm-ssa-raid-cluster-adapter>

This is a useful independent IBM product-family corroboration that the phrase and maintenance function were not confined to one later ServeRAID-3H document.

It is not used to claim identical firmware or the same exact algorithm as ServeRAID II/3H.

---

## Historical record

### H/P — December 1997 IBM documentation already frames latent sectors as a proactive-maintenance problem

The December 1997 IBM hard-drive media-defects white paper makes the historical problem explicit.

It distinguishes sectors whose defects are discovered by ordinary access from sectors that remain untouched because the file is seldom used, the region is free, or access may be satisfied elsewhere. The latter can retain a latent failure condition until some later event finally demands the sector.

IBM's proposed operational response is `Data Scrubbing`: deliberately access the medium in the background while normal user activity continues so that defects can be exposed earlier.

This directly grounds:

```text
physical sector still present
    !=
recently qualified as readable
```

and:

```text
absence of demand-time error
    !=
positive evidence that all array sectors remain readable
```

These are engineering restatements of the documented behavior, not IBM's own formal ontology.

### H/P — IBM documents regular scrubbing before a second failure consumes the redundancy margin

The surviving IBM RAID-scrubbing support record explains why proactive reads matter specifically for RAID reconstruction.

If one member drive later fails completely while another surviving drive contains an unreadable sector, reconstruction can become impossible at the exact moment the system needs the remaining members most. The recommended scrub attempts to expose and repair the latent sector earlier, while the array still has enough redundant information to reconstruct it.

The historical function is therefore not simply `find bad sectors`.

It is:

```text
find latent unreadability
    while
redundant reconstruction sources still exist
```

That is a retention-maintenance relation: maintenance timing affects whether a later embodiment loss remains recoverable.

### H/P — ServeRAID II moves the work into an automatic background controller task

The IBM support record states that `Data Scrubbing` runs automatically in the background on the ServeRAID II Adapter when firmware 2.30.04 or later provides the feature.

The Netfinity administration documentation likewise describes continuous background reading of RAID-1 and RAID-5 logical-drive sections while the system remains in operation, with defective sectors automatically repaired.

This is stronger than a host operator being told to run an occasional offline verify.

The maintenance locus can be represented as:

```text
host application demand
        |
        | normal I/O
        v
ServeRAID logical drive
        |
        +---- background controller scrub ---->
              drive read / verify activity
              defect detection
              redundancy-assisted recovery where possible
              sector repair/reallocation path
```

This diagram is an engineering reconstruction. The IBM sources do not provide enough internal firmware detail to turn it into a precise command-by-command state machine for every controller generation.

### H/P — the 1998 ServeRAID-3H product contract separately names periodic scan and automatic repair

The ServeRAID-3H product specification, with an announce date of 22 September 1998, says data scrubbing periodically scans disk services and automatically repairs bad sectors on the disk array.

That gives a dated named-controller witness for both:

1. proactive / periodic scan;
2. repair rather than logging-only behavior.

It also prevents a chronology error in Case 101:

```text
2005 Dell/LSI `Patrol Read` documentation
    !=
first public controller-level proactive RAID media scan
```

and:

```text
2005 T10 Background Medium Scan standardization
    !=
first public proactive disk/array scan mechanism
```

### H/P — IBM's own terminology distinguishes scrubbing from synchronization even though one utility path could be used to perform a scrub

The surviving IBM material uses both `Synchronization` and `Data Scrubbing`.

Synchronization establishes or checks the RAID redundancy relation, especially parity for RAID-5. Older operational guidance could use a synchronization utility periodically as a scrub-like procedure. Later ServeRAID II documentation says automatic background data scrubbing means the administrator no longer needs the same weekly manual synchronization practice for that maintenance purpose.

The terms therefore should not be flattened into one timeless operation.

A bounded historical reconstruction is:

```text
initial / explicit synchronization
    -> establish or verify redundancy relation

periodic / automatic data scrubbing
    -> exercise sectors proactively
    -> expose latent defects
    -> use valid redundancy to repair where possible
```

The fact that a synchronization utility could also be used as a manual scrub path does not make every synchronization operation identical to the later background scrub task.

### H/P — IBM explicitly separates PFA-style prediction from forced coverage

The RAID-scrubbing support record also discusses Predictive Failure Analysis (`PFA`). It says periodic internal measurements are collected when sectors are actually accessed, while data scrubbing forces sectors to be read and thereby supplies more observations.

This is an early vendor-side version of a distinction already important elsewhere in the repository:

```text
health prediction / telemetry
    !=
proactive coverage
```

Case 101 later makes the same distinction between SMART alerts and active Patrol Read. The 1997-era IBM record therefore provides earlier prior art for the functional separation without proving direct vocabulary or engineering descent.

---

## Engineering reconstruction

### E — proactive maintenance preserves a future reconstruction option, not merely present readability

A scrub pass has at least two possible retention effects:

1. it can establish new evidence that a currently accessible sector is readable now;
2. if a latent defect is found early enough, it can consume available redundancy to repair or relocate the bad embodiment before another failure removes the remaining reconstruction source.

The maintenance target is therefore not only the sector's present bit pattern. It is also the array's **future ability to reconstruct the logical stripe**.

A useful decomposition is:

```text
payload presence
    !=
sector readability
    !=
redundancy correctness
    !=
reconstruction admissibility
    !=
repair completion
    !=
future redundancy margin
```

### E — parity/currentness is a precondition for safe repair authority

The strongest engineering boundary in this slice comes from IBM's warning that an unsynchronized RAID-5 array can contain parity that does not accurately reflect the data.

If scrub-time recovery then treats that parity as authoritative, the controller may reconstruct the wrong value.

Therefore:

```text
defect detected
    + redundant-looking members present
    !=
safe repair source qualified
```

A more exact relation is:

```text
repair authority
    requires
current / valid redundancy relation
```

This is not just a capacity issue. An array may physically contain all expected disks and still lack trustworthy reconstruction authority if parity/currentness has not been established.

### E — proactive verification cannot be modeled as a single `good/bad` bit

The IBM sources imply several distinct states:

- sector has not been recently exercised;
- sector read succeeds;
- sector read requires recovery;
- sector is unreadable;
- array redundancy is valid enough for reconstruction;
- array redundancy is not known valid;
- reconstructed data is written back successfully;
- a sector has been reallocated;
- the array is again in a stronger redundancy state.

Conflating them into one health flag would lose the exact maintenance obligation.

### E — maintenance frequency trades work against latent-defect exposure time

IBM recommended weekly scrubbing in the older operator-driven guidance and later documented automatic/continuous or periodic controller scrubbing.

The bounded engineering point is not that weekly is a universal optimal interval.

It is that there is an exposure window:

```text
defect appears
    -> remains latent while unaccessed
    -> proactive or demand read discovers it
```

Shorter coverage intervals can reduce the time during which a latent unreadable sector coexists with apparently healthy redundancy, at the cost of more background I/O and maintenance work.

No failure-probability model is inferred here from the vendor recommendation alone.

---

## Prior-art boundary relative to Case 101's 2005 evidence

### 1. IBM 1997–1998 is an earlier controller-level proactive-scan witness

The current Case 101 chronology already establishes:

- T10 `04-198r5` / 2005 BMS standardization;
- Dell PERC Patrol Read documentation by April 2005;
- Dell MegaPR utility in June 2005;
- generic LSI MegaRAID Patrol Read documentation by February/March 2006;
- Seagate named-drive BMS implementation by 2007.

The IBM evidence pushes the controller-level public documentation floor substantially earlier:

```text
December 1997 IBM white-paper problem statement + Data Scrubbing guidance
    -> 1997/1998 IBM product-family data-scrubbing witnesses
    -> September 1998 ServeRAID-3H named-controller product specification
    -> 2005 Dell PERC Patrol Read documentation
    -> 2005 T10 standardized BMS control/status work
```

This chronology is evidence of earlier public documentation, not proof of invention priority or a direct lineage.

### 2. IBM `Data Scrubbing` must not be silently renamed `Patrol Read` or `BMS`

The functional overlap is strong:

- background access before ordinary demand;
- defect discovery;
- controller/device maintenance locus;
- optional or automatic corrective action.

But the historical terms, layer boundaries, and exact control interfaces differ.

Therefore:

```text
functional similarity
    !=
terminological identity
    !=
implementation identity
    !=
genealogical descent
```

### 3. IBM adds a repair-authority precondition not visible in the phrase `automatic repair`

The 1998 product summary can sound like:

```text
find bad sector -> automatically repair
```

The broader IBM operational documentation shows that the actual safety relation is narrower:

```text
find bad sector
    -> require usable/current redundant information
    -> reconstruct
    -> rewrite / reallocate
```

If parity has not been correctly synchronized, the reconstruction source can be wrong.

Thus:

> **automatic repair capability != unconditional repair authority.**

This is the main retention-specific reason to keep the 1997–1998 IBM slice in `technical-retention` instead of treating it only as a controller-feature chronology.

---

## Functional comparisons

### Case 14 — SCSI defect reassignment

Case 14 owns the narrower relation between one logical block and replacement physical sectors.

IBM ServeRAID scrubbing sits upstream:

```text
proactive read
    -> latent defect discovery
    -> redundancy qualification/reconstruction
    -> drive repair or reassignment path
```

This is a functional sequence, not a claim that every ServeRAID generation issued one specific SCSI reassignment command.

### Case 18 / Synthesis 08 — ZFS and proactive integrity maintenance

Both IBM RAID data scrubbing and ZFS scrub can discover faults before foreground demand.

But the qualification relation differs:

- IBM ServeRAID scrub is controller/array-centric and primarily tied to sector readability plus RAID redundancy;
- ZFS scrub uses filesystem-level block identity and checksums to qualify content integrity and repair sources.

Therefore:

```text
medium/stripe readability maintenance
    !=
end-to-end checksum integrity maintenance
```

### Case 55 — health telemetry

The 1997 IBM discussion of PFA versus forced scrub coverage is functionally analogous to Case 55's distinction between health telemetry and active verification.

It does not establish a PFA→SMART→NVMe genealogy.

### Case 94 — RAID code strength versus repair-source validity

Case 94 shows that additional parity does not automatically provide arbitrary corruption diagnosis.

The ServeRAID slice supplies a simpler precondition:

> even nominal RAID redundancy is not a trustworthy repair source if its parity relation was never made current.

The shared functional lesson is:

```text
redundant bytes present
    !=
repair source qualified
```

No common historical lineage is asserted.

---

## Philosophical interpretation — bounded

The IBM ServeRAID case adds a useful limit to the idea that retention is simply the survival of a payload.

A RAID stripe can remain physically present while the system's future ability to recover one member depends on a relation that must also remain valid: parity/currentness across the members. Proactive maintenance is partly an attempt to keep latent physical deterioration from silently consuming the margin before that relation is needed.

The technically exact conceptual problem is therefore:

> **retention may depend on preserving not only an object, but the trustworthiness of the relation that authorizes reconstruction of the object.**

This is a philosophical interpretation of the engineering evidence, not IBM's historical vocabulary.

The limit is equally important. `Trust`, `authority`, and `currentness` here are project analytical terms. They should not be projected back as concepts used by IBM engineers unless a primary source actually uses equivalent language.

---

## Explicit non-claims

This packet does **not** claim:

1. IBM invented disk scrubbing.
2. December 1997 is the first historical use of the phrase `Data Scrubbing`.
3. IBM invented latent-sector-error management.
4. IBM ServeRAID is the ancestor of T10 BMS.
5. IBM ServeRAID is the ancestor of Dell/LSI Patrol Read.
6. Dell/LSI copied the IBM design.
7. T10 BMS copied IBM terminology or firmware behavior.
8. `Data Scrubbing`, `Patrol Read`, `Background Medium Scan`, and `Consistency Check` are interchangeable historical terms.
9. Every ServeRAID generation used the same internal algorithm.
10. Every IBM RAID controller automatically repaired every detected sector error.
11. Automatic repair guarantees payload preservation if redundancy is already invalid.
12. Physical presence of all RAID members proves parity correctness.
13. Synchronization and data scrubbing are the same operation in every IBM document or generation.
14. A weekly recommendation is a universal optimal scan interval.
15. Background scrubbing proves that every sector has a permanent verification certificate.
16. Completing one scrub proves future readability indefinitely.
17. Scrubbing is a secure-erasure mechanism.
18. Sector reassignment necessarily destroys the old physical embodiment.
19. PFA prediction and proactive media coverage are the same maintenance function.
20. The current IBM support-page modification date is the historical date of the underlying 1997/1998 material.
21. The ServeRAID-3H product record proves first firmware implementation in September 1998.
22. The Netfinity support transcription proves identical semantics across every Netfinity 5500 controller/firmware combination.
23. The SSA RAID Cluster Adapter and ServeRAID II/3H shared identical scrub firmware.
24. The surviving sources expose exact persistent scan checkpoints, restart semantics, or power-loss behavior.
25. The sources prove the exact SCSI command sequence used internally for each repaired defect.
26. The sources prove that repair always resulted in drive-level physical-sector reallocation rather than another successful rewrite path.

---

## Claim ledger

| Claim | Type | Evidence | Strength |
|---|---|---|---|
| IBM documented Data Scrubbing as a response to latent media defects by December 1997 | historical record | P1 | strong |
| IBM documentation recommended regular scrub to reduce rebuild/data-loss risk | historical record | P2 | strong |
| ServeRAID II firmware 2.30.04+ is described as running Data Scrubbing automatically in the background | historical record | P2 | strong, later support presentation of older material |
| ServeRAID-3H public product specification documented periodic scrub + automatic bad-sector repair by 22 Sep 1998 | historical record | P3 | strong |
| Netfinity ServeRAID administration documentation describes continuous background reads of RAID-1/5 and automatic repair | historical record | P4 | strong for semantics; chronology bounded by product records |
| IBM product material in December 1997 also exposed data scrubbing on SSA RAID arrays | historical record | P5 | strong product-family corroboration |
| controller-level proactive array scanning predates 2005 Dell/LSI Patrol Read documentation | historical reconstruction from dated records | P1/P3/P5 + Case 101 existing sources | strong |
| controller-level proactive array scanning predates T10's 2005 BMS standardization | historical reconstruction from dated records | P1/P3/P5 + Case 101 existing sources | strong |
| safe scrub-time repair depends on valid/current redundancy, not only defect detection | engineering reconstruction | P2 parity warning | strong |
| redundancy presence is not equivalent to repair-source qualification | engineering reconstruction | P2 | strong |
| IBM ServeRAID caused or directly influenced T10 BMS / Dell-LSI Patrol Read | historical genealogy | none | unsupported / explicitly rejected |
| exact restart/power-loss persistence of IBM scrub progress | implementation claim | none in inspected sources | open |

---

## What this changes in Case 101

Case 101's earlier prior-art boundary said a full controller patrol-read history still needed genuinely earlier or independent vendors beyond the 2005 Dell/LSI ecosystem.

This packet closes one bounded part of that debt:

- IBM has a **December 1997** dated proactive `Data Scrubbing` problem/maintenance record;
- IBM product documentation in **1997–1998** exposes controller/array data scrubbing before the Dell/LSI 2005 `Patrol Read` public floor;
- the ServeRAID evidence adds a particularly useful negative condition: repair is only safe when the redundant relation used for reconstruction is itself valid/current.

It does **not** close the entire controller-scrubbing genealogy. Earlier RAID-controller maintenance, independent non-IBM vendors, exact firmware ancestry, command-level implementation, and field traces remain open.

Case 101 remains `grounded`; this packet deepens evidence and prior-art boundaries without changing maturity.

---

## Remaining evidence debt

1. Find a directly preserved period copy of IBM's `Using IBM RAID Adapters to Avoid Data Loss` white paper with original publication metadata and page anchors.
2. Recover the original ServeRAID II firmware 2.30.04 release notes and exact release date.
3. Inspect period ServeRAID II / 3H firmware manuals for scrub scheduling, progress state, restart semantics, and error-state transitions.
4. Determine whether the automatic scrub internally used READ VERIFY, ordinary reads, vendor-specific drive commands, or a generation-dependent mixture.
5. Find non-IBM, non-LSI controller evidence from the 1990s to test whether similar proactive array scrubbing was already widespread.
6. Recover earlier uses of `scrub` / `scrubbing` in storage-controller literature without inferring one genealogy from vocabulary alone.
7. Find fault-injection or field-service evidence showing the actual repair/reallocation path after a detected latent sector error.
8. Test whether scrub progress or schedule state survived controller reset/power loss in any named ServeRAID generation.
9. Separate firmware-level automatic scanning from host-scheduled `Synchronize` jobs across exact ServeRAID releases.
10. Route the broad controller-history/genealogy work to `tmzncty/computing-archaeology` if a full chronology is built.

---

## Related-repository routing

A fresh search of `tmzncty/computing-archaeology` for `ServeRAID data scrubbing` returned no dedicated packet to reuse.

The division of labor should therefore be:

```text
technical-retention
    -> latent unreadability
    -> proactive coverage
    -> redundancy/currentness qualification
    -> repair authority
    -> restored margin

computing-archaeology
    -> IBM RAID controller genealogy
    -> ServeRAID hardware/firmware evolution
    -> command implementation
    -> vendor competition and terminology diffusion
    -> broader patrol-read / scrub chronology
```

The historical engineering history should not be duplicated here once the companion repository contains it.

---

## Compact conclusion

The bounded result is:

```text
December 1997 IBM documentation
    -> latent sectors can remain undiscovered without proactive access
    -> Data Scrubbing is recommended while the array still has recovery margin

1997-1998 IBM product/controller records
    -> background / periodic controller-level scrubbing
    -> automatic defect repair where reconstruction is possible

but

defect detection
    != valid parity
    != qualified repair source
    != completed repair
```

This moves Case 101's controller prior-art floor materially earlier than its 2005 Dell/LSI witness while preserving the anti-anachronism boundary: IBM `Data Scrubbing`, Dell/LSI `Patrol Read`, and T10 `Background Medium Scan` can be compared functionally without being collapsed into one name, one implementation, or one historical lineage.
