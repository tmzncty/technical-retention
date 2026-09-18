# Case 136 evidence — 2000–2002 MegaRAID rebuild-policy prior art

## Status

**`bounded deepening complete`** — this record moves the directly checked public-documentation floor for MegaRAID rebuild scheduling and restart-continuation policy earlier than the March 2006 manual used by the canonical case.

The bounded claim is:

> By July 2000, a MegaRAID configuration-software guide documented rebuild rate as an adapter-level resource-allocation control, exposed `FlexRAID PowerFail` as a separate restart-continuation option, and stated that clearing configuration did not affect rebuild rate. An April 2000 MegaRAID Express 500 hardware-guide draft already described user-definable rebuild rates; an August 2002 LSI Logic hardware guide independently preserved the same 0–100% compute-cycle / priority semantics.

This is an **earliest directly checked documentation floor in the current evidence set**, not an invention-priority claim for RAID repair throttling.

## Why this slice was selected

The canonical Case 136 was grounded mainly from a March 2006 LSI MegaRAID software guide and later Dell PERC documentation. That was enough to establish the retention model, but it left a historical uncertainty:

> Was the exposed rebuild-priority / continuation-policy structure already present in earlier MegaRAID generations, or was 2006 simply the first checked witness?

This slice answers only that bounded question. It does not attempt a general history of RAID rebuild scheduling.

## Sources

### Source A — MegaRAID Configuration Software Guide, MAN-MR-GENSW, 7/20/00

Vendor-authored manual:

- title: *MegaRAID RAID Controller Configuration Software Guide*;
- document number: `MAN-MR-GENSW`;
- document date printed on the title page: `7/20/00`;
- the surviving mirrored copy carries LSI Logic copyright text and a revision history extending from 1997 through the 7/20/00 revision;
- inspected through public manual mirrors preserving the vendor text.

Useful public transcriptions/facsimile access:

- https://www.manualshelf.com/manual/american-megatrends/megaraid-express-500/technical-information-english.html
- https://manualzilla.com/doc/7439827/american-megatrends-megaraid-express-500-technical-inform...

Relevant passages in the surviving guide:

- Adapter / Objects exposes `Rebuild Rate` as a setting that displays and changes the rebuild rate for drives on the selected adapter.
- The same adapter-property area separately exposes `FlexRAID PowerFail`, described as allowing drive reconstruction to continue when the system restarts after a power failure.
- Power Console Plus describes `Rebuild Rate` as the amount of system resources devoted to rebuilding failed disks; increasing it leaves fewer resources for ordinary RAID operations.
- Operational guidance later says to check the rebuild rate per adapter and explicitly states that the rebuild rate **is not affected when configuration is cleared**.

The document date is used as the documentation floor. The revision-history entries before 2000 do **not** establish that all of these particular features existed in the 1997 initial release.

### Source B — MegaRAID Express 500 Hardware Guide, preliminary draft MAN-475, 4/14/2000

Vendor-authored preliminary hardware guide:

- title: *MegaRAID Express 500 Hardware Guide*;
- document number: `MAN-475`;
- marked `Preliminary Draft`;
- date: `4/14/2000`;
- American Megatrends copyright 2000.

Public facsimile/transcription access:

- https://www.manualshelf.com/manual/american-megatrends/megaraid-express-500/american-megatrends-inc-megaraid-express-500-hardware-guide.html
- https://www.manualsdir.com/manuals/44046/american-megatrends-megaraid-express-500.html?page=28

The Disk Rebuild section says the controller automatically and transparently rebuilds failed drives with **user-definable rebuild rates**. It defines rebuild rate as the fraction of compute cycles dedicated to rebuilding failed drives and gives the same endpoints later seen in LSI documentation:

- `0%`: rebuild occurs only when the system is otherwise idle;
- `100%`: rebuild has higher priority than any other system activity.

The same section says the controller restarts the rebuild if the system goes down during a rebuild.

Because this document is explicitly a preliminary draft, it is useful evidence of published design/documentation state, not by itself proof of a particular shipping-firmware behavior on 4/14/2000.

### Source C — LSI Logic MegaRAID SCSI 320-1 Hardware Guide, MAN-520, 8/16/2002

Vendor-authored LSI Logic manual:

- title: *MegaRAID SCSI 320-1 Hardware Guide*;
- document number: `MAN-520`;
- date: `8/16/2002`;
- revision history: `8/16/02 Initial release`;
- LSI Logic copyright 2002.

Public PDF facsimile mirror:

- https://dlcdnets.asus.com/pub/ASUS/scsi/LSI%20MegaRAID/SCSI%20320-1%20%26%20320-2/320-1hguide.pdf

The Disk Rebuild section says the SCSI 320-1 automatically and transparently rebuilds failed drives with user-definable rebuild rates. It defines rebuild rate as the fraction of compute cycles dedicated to rebuilding failed drives and documents:

- configurable range `0%`–`100%`;
- `0%`: rebuild only when the system is otherwise idle;
- `100%`: rebuild higher priority than any other system activity.

The guide also lists `User-specified rebuild rate: Yes` among controller features and defines `Rebuild Rate` in the glossary as the percentage of CPU resources devoted to rebuilding.

This is useful as a post-2000, non-preliminary LSI-branded witness for the same broad control semantics.

## Historical record

### April 2000 — user-definable rebuild scheduling is already explicit in MegaRAID documentation

The preliminary MegaRAID Express 500 hardware guide does not present rebuild as an all-or-nothing background action. It exposes a quantitative operator policy spanning idle-only rebuild at one end and repair-prioritized operation at the other.

Historical claim supported:

> By 14 April 2000, MegaRAID documentation publicly represented degraded-array repair as work whose competition with ordinary service could be changed by a user-defined rebuild-rate control.

Historical claim **not** supported:

> MegaRAID invented rebuild throttling in 2000.

No invention-priority search is performed here.

### July 2000 — resource competition, restart continuation, and configuration lifetime are separate controls

The 7/20/00 configuration-software guide is more useful for Case 136 than the hardware overview because it exposes the management surface directly.

Three relations appear separately:

1. `Rebuild Rate` controls resources devoted to failed-drive rebuild.
2. `FlexRAID PowerFail` controls whether reconstruction continues after the documented restart condition.
3. Clearing RAID configuration does not reset the rebuild-rate setting.

That is already enough to reject a monolithic model in which “rebuild state” is one indivisible object.

### August 2002 — LSI hardware documentation preserves the same rebuild-rate semantics

The 2002 SCSI 320-1 guide repeats the compute-cycle definition and the 0% / 100% priority endpoints in an LSI Logic initial-release manual.

This strengthens the historical claim from “one preliminary 2000 manual used this wording” to:

> the operator-visible rebuild-priority concept is directly documented across multiple MegaRAID manuals before the 2006 witness previously used as the case floor.

This does **not** prove byte-for-byte firmware continuity, a single internal field, or uninterrupted product-line genealogy.

## Engineering reconstruction

### Repair obligation != repair scheduling policy

The failed-member condition creates a reconstruction obligation. The rebuild-rate property controls how aggressively controller resources are assigned while that obligation exists.

```text
member failure
    -> repair obligation
    -> rebuild work exists

stored rebuild-rate policy
    -> scheduling / resource-priority relation
    -> how strongly rebuild competes with foreground RAID service
```

Therefore:

> **repair owed != repair priority != repair completed.**

### 0% != disabled

The 2000 and 2002 hardware-guide wording makes the low endpoint especially useful:

```text
rebuild rate = 0%
    -> rebuild still eligible
    -> execute when system otherwise idle
```

So:

> **lowest scheduling priority != maintenance cancellation.**

This is stronger than inferring behavior from the numeric label alone.

### 100% != a measured throughput guarantee

The manuals describe compute cycles, system resources, and priority. They do not promise that a setting of `100%` maps to a fixed media bandwidth or wall-clock completion time.

Thus:

> **configured percentage != guaranteed percentage of disk bandwidth, IOPS, or elapsed-time share.**

### Rebuild priority != restart continuation

The 7/20/00 configuration guide exposes `Rebuild Rate` and `FlexRAID PowerFail` as separate adapter properties.

```text
Rebuild Rate
    -> competition while maintenance runs

FlexRAID PowerFail
    -> whether documented reconstruction continues after restart
```

Therefore:

> **maintenance aggressiveness != maintenance lifetime across interruption.**

### Restart continuation != demonstrated exact progress checkpoint

The manuals say reconstruction/rebuild continues or restarts after the documented outage/restart condition. They do not reveal whether firmware retains:

- an exact stripe/LBA cursor;
- a bitmap;
- a coarse frontier;
- a task descriptor only;
- or no precise cursor and simply redoes part of the work.

Hence:

> **task continuity != exact-progress persistence.**

and:

> **restart continuation != exactly-once maintenance execution.**

### Configuration clear != controller-policy clear

The 7/20/00 software guide explicitly says rebuild rate is not affected when configuration is cleared.

That yields a direct lifetime boundary:

```text
clear array configuration
    -> topology/configuration relation retired
    -/-> rebuild-rate policy necessarily retired
```

Therefore:

> **array-configuration lifetime != rebuild-policy lifetime.**

The source does not disclose the physical storage location of the policy, so no NVRAM-field claim is made.

### Same label across manuals != proven same implementation

The 2000 preliminary Express 500 guide and 2002 SCSI 320-1 guide use highly similar rebuild-rate semantics. That supports continuity of an exposed operator concept.

It does not prove:

- the same scheduler;
- the same firmware code;
- the same persistence representation;
- the same controller CPU accounting;
- or a direct code lineage.

The safe level is interface/behavioral documentation, not hidden implementation identity.

## Functional comparison

### Case 17 — RAID reconstruction

Case 17 provides the reconstruction obligation and redundancy-restoration mechanism. This evidence inserts an explicitly configurable scheduler between obligation and completion:

```text
degraded array
    -> reconstruction possible
    -> rebuild admitted
    -> retained priority policy
    -> foreground/repair competition
    -> eventual redundancy restoration
```

This is an intra-RAID functional relation, not a new RAID taxonomy.

### Case 83 — maintenance cursor checkpointing

HDFS BlockScanner exposes a concrete cursor/checkpoint relation. Early MegaRAID documentation exposes continuation behavior but not its progress representation.

> **documented continuation != documented cursor checkpoint.**

### Case 148 — NVMe Device Self-test

Both expose maintenance-lifecycle policy around background work, but the standardized NVMe operation model and vendor-specific MegaRAID reconstruction controls are not historically or mechanically identical.

The comparison is functional only.

## Philosophical interpretation

This evidence strengthens a recurring project distinction:

> A system can retain not only payload or topology, but also a **policy about how urgently an already-owed repair should consume future resources**.

That policy can have a different lifetime from the array configuration itself. It is therefore misleading to treat “what the controller remembers” as only data blocks plus RAID membership.

This interpretation remains downstream of the historical source. The manuals themselves do not use the project's philosophical vocabulary.

## Explicit non-claims

This record does **not** claim that:

1. RAID rebuild throttling was invented by American Megatrends, LSI, or MegaRAID.
2. April 2000 is the first appearance of rebuild-rate control anywhere.
3. The pre-2000 revision-history entries prove rebuild-rate behavior existed in 1997.
4. A preliminary hardware guide proves every shipping controller behaved exactly as described.
5. The 2000, 2002, and 2006 implementations used identical firmware.
6. The numeric percentage is a literal disk-bandwidth reservation.
7. `0%` disables rebuilding.
8. `100%` guarantees a particular rebuild duration.
9. Rebuild rate determines reconstructed-byte correctness.
10. Rebuild rate and rebuild progress are the same state.
11. `FlexRAID PowerFail` proves an exact persisted stripe cursor.
12. A continued task performs exactly-once work across restart.
13. Restart continuation proves all intermediate controller state survives power loss.
14. The rebuild-rate setting is stored in a particular NVRAM field.
15. Every MegaRAID property has the same persistence horizon.
16. Clearing configuration erases every controller-level policy.
17. Similar wording proves uninterrupted corporate/product genealogy.
18. The same term implies the same scheduler across controller generations.
19. This evidence says anything about secure deletion or media remanence.
20. A maintenance-priority policy by itself reduces unrecoverable-read risk on surviving disks.

## Evidence-strength ledger

| Claim | Strength | Basis |
|---|---|---|
| 4/14/2000 MegaRAID Express 500 draft documents user-definable rebuild rates | high | dated vendor-authored hardware guide transcript/facsimile |
| 0% means idle-only and 100% gives rebuild higher priority | high | explicit 2000 and 2002 manual text |
| 7/20/00 guide exposes rebuild rate as adapter property | high | dated vendor-authored configuration guide |
| 7/20/00 guide separately exposes FlexRAID PowerFail | high | explicit adapter-property description |
| 7/20/00 guide says rebuild rate survives configuration clear | high | explicit operational instruction |
| 8/16/2002 LSI SCSI 320-1 guide preserves same broad rate semantics | high | dated initial-release LSI hardware guide |
| early MegaRAID therefore had a retained repair-policy concept distinct from array topology | medium-high | engineering reconstruction from explicit lifetime/management distinctions |
| exact physical storage of the property | unsupported | not disclosed by inspected manuals |
| exact progress checkpoint used across restart | unsupported | not disclosed by inspected manuals |
| invention priority for RAID rebuild throttling | unsupported | no exhaustive prior-art search |

## What this closes

This closes the narrow Case 136 evidence debt:

> **Was March 2006 merely the first checked rebuild-rate witness?**

Yes. The checked documentation floor can now be moved earlier:

- April 2000: preliminary MegaRAID Express 500 hardware documentation already states user-definable rebuild-rate semantics;
- July 2000: MegaRAID configuration software documentation exposes rebuild priority, restart-continuation policy, and a rebuild-rate lifetime distinct from configuration clear;
- August 2002: an LSI initial-release SCSI 320-1 hardware guide independently preserves the same 0–100% priority semantics.

The result is a **documentation-floor deepening**, not a first-invention finding.

## Remaining evidence debt

Still open:

- pre-2000 direct product/manual evidence for rebuild-rate or rebuild-priority controls;
- non-MegaRAID / cross-vendor rebuild-priority evidence before 2000;
- exact introduction commit/firmware release for the MegaRAID setting;
- controller-internal scheduler algorithm behind the percentage;
- physical persistence location and reset/default lifetime of each policy property;
- exact cross-restart rebuild-progress representation;
- power-cut experiments on period hardware/firmware;
- quantitative foreground-I/O versus rebuild-completion curves;
- broader RAID rebuild-throttling genealogy, which belongs primarily in `tmzncty/computing-archaeology`.

## Related-repository routing

A search of `tmzncty/computing-archaeology` for the exact `MegaRAID SCSI 320-1` and `MAN-MR-GENSW FlexRAID PowerFail` terms did not return a dedicated existing packet in this run.

`technical-retention` therefore keeps only the retention-specific seam:

```text
repair obligation
    -> retained repair-priority policy
    -> service/maintenance competition
    -> interruption
    -> separately represented continuation policy
    -> eventual repair completion
```

The broader history of MegaRAID ownership/product evolution, RAID-controller firmware lineage, and cross-vendor rebuild scheduling should be developed in `computing-archaeology` rather than duplicated here.
