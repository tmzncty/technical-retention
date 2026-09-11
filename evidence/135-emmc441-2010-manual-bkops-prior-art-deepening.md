# Case 135 deepening evidence — e.MMC 4.41 manual BKOPS and the pre-5.1 maintenance-control floor (2010–2011)

## Status

**`grounded`** for a bounded prior-art correction: public e.MMC 4.41 material already exposes generic Background Operations and manual `BKOPS_START` control well before the e.MMC 5.1 witness used in the earlier Case 135 deepening.

This record establishes a **public standardized lower bound**, not an invention date. It does not claim that e.MMC 4.41 invented managed-Flash background maintenance, that every 4.41 device implemented the feature identically, or that generic BKOPS is itself a retention-refresh algorithm.

## Research question

The earlier Case 135 BKOPS pass used JESD84-B51 (February 2015) to separate generic e.MMC maintenance opportunity from Micron/Armadillo vendor self refresh. It deliberately left pre-5.1 genealogy open.

This bounded follow-up asks:

> How far back can the public standardized/manual-BKOPS control surface be moved using inspectable standard metadata and period manufacturer documentation, without converting a lower bound into a first-invention claim?

## Source boundary

### Standards records

- JEDEC Solid State Technology Association, **JESD84-A441:2010**, _Embedded MultiMediaCard(e•MMC) e•MMC/Card Product Standard, High Capacity, including Reliable Write, Boot, Sleep Modes, Dual Data Rate, Multiple Partitions Supports, Security Enhancement, Background Operation and High Priority Interrupt (MMCA, 4.41)_. Intertek Inform's standards record identifies JEDEC as publisher and gives publication date **1 March 2010**: <https://www.intertekinform.com/en-gb/standards/jedec-jesd84-a441-2010-1316222_saig_jedec_jedec_3218476/>.
- JEDEC Solid State Technology Association, **JESD84-A44:2009**, e.MMC 4.4. Intertek Inform's public record gives publication date **1 March 2009** and a title ending with `Security Enhancement (MMCA, 4.4)`, without the later A441 title's `Background Operation and High Priority Interrupt` phrase: <https://www.intertekinform.com/en-gb/standards/jedec-jesd84-a44-2009-1316222_saig_jedec_jedec_3218463/>.

The title difference is used only as a **document/version boundary**. It is not a substitute for a clause-by-clause A44→A441 normative diff and does not prove that no related mechanism existed before A441.

### Period manufacturer witnesses

- **SanDisk iNAND e.MMC 4.41 I/F Data Sheet**, document `80-36-03433`, revision 1.0, dated **25 February 2010**. A USPTO-hosted litigation copy of the manufacturer document exposes `BKOPS_START[164]` as `Manually start background operations` and `BKOPS_EN[163]` as `Enable background operations handshake`: <https://ptacts.uspto.gov/ptacts/public-informations/petitions/1556143/download-documents?artifactId=lQ85v9edb8_QeKi6_NywwOWp0ScgdcM6u8sIx_zzwtaZsLz3HXtCuSKw>.
- Kingston Solutions Inc., **Flash Storage Specification e•MMC 4.41, Embedded MultiMediaCard 4GB, Datasheet Ver. 1.0.1**, **June 2011**. The manufacturer-authored period document states JESD84-A441 compatibility, includes a `Background Operations` section, and exposes `BKOPS_SUPPORT[502]`, `BKOPS_STATUS[246]`, `BKOPS_START[164]`, and `BKOPS_EN[163]`: <https://studylib.net/doc/28562379/ksi-emmc441-4gb-datasheet-v1.0.1>.

These manufacturer documents are period product witnesses. The mirrored copies are not treated as replacements for the full normative A441 text.

### Later control witness already in the repository

- [`135-jedec-emmc51-bkops-maintenance-opportunity-deepening.md`](135-jedec-emmc51-bkops-maintenance-opportunity-deepening.md) directly inspects JESD84-B51 for manual BKOPS, `BKOPS_STATUS`, `MANUAL_EN`, later `AUTO_EN` autonomous idle-time scheduling, and the BKOPS/Sanitize separation.

## Historical record

### H/P — e.MMC 4.41 publicly names Background Operation in 2010

The public standards record for JESD84-A441:2010 includes **Background Operation and High Priority Interrupt** in the standard title and dates publication to **1 March 2010**.

For this repository, that is enough to move the conservative public e.MMC-standard vocabulary floor used by Case 135 from the previously inspected 2015 e.MMC 5.1 text back to **at least e.MMC 4.41 / 2010**.

It does **not** establish first invention, first ballot, first implementation, or first shipment.

### H/P — period 4.41 product documentation exposes manual BKOPS control

The June-2011 Kingston Solutions 4.41 datasheet describes device-internal maintenance better performed while the host is not being serviced. Its `Background Operations` section says the host writes `BKOPS_START` (EXT_CSD byte 164) to **manually start** background operations and that the device remains busy until no more background processing is needed.

The same document exposes:

- `BKOPS_SUPPORT[502]` — background-operations support;
- `BKOPS_STATUS[246]` — background-operations status;
- `BKOPS_START[164]` — manually start background operations;
- `BKOPS_EN[163]` — enable the background-operations handshake.

A SanDisk iNAND e.MMC 4.41 datasheet dated 25 February 2010 independently exposes the same manual-control vocabulary for `BKOPS_START[164]` and `BKOPS_EN[163]`.

Thus the bounded record is stronger than a later retrospective statement: **period e.MMC 4.41 product documentation already presents generic background maintenance as a host/device control relation.**

### H/P — e.MMC 5.1 remains a later control point, not the origin of generic manual BKOPS

The existing 5.1 evidence remains useful because JESD84-B51 exposes a richer scheduling split, including `AUTO_EN`, under which the device may begin or end background operations during idle time without a manual `BKOPS_START` service window.

The new 4.41 evidence changes the safe chronology to:

```text
by e.MMC 4.41 / 2010:
    public Background Operation vocabulary
    + manual BKOPS control surface

by the inspected e.MMC 5.1 / 2015 text:
    manual control still present
    + autonomous idle-time scheduling exposed through AUTO_EN
```

This is a version-bounded comparison. It does not infer the exact changes made in every intermediate 4.5/4.51/5.0 revision.

## Engineering reconstruction

### E — the standardized maintenance-control relation predates the 5.1 witness

The earlier Case 135 pass used 2015 because that was the normative text directly inspected there. The 4.41 evidence now supplies a prior-art guardrail:

> **e.MMC 5.1 is not the origin point for generic manual BKOPS.**

For this repository, the conservative public standardized floor for the generic manual-BKOPS relation is now **at least e.MMC 4.41 / 2010**.

### E — capability, obligation, and granted execution opportunity remain distinct in the earlier surface

Even with the earlier 4.41 witness:

```text
BKOPS capability
    != current background-work status
    != host-granted manual execution opportunity
    != hidden maintenance algorithm
```

A standard control plane can expose that maintenance exists, whether work is pending, and when the host grants service time without exposing page relocation, erase selection, wear-leveling policy, refresh policy, or another physical mechanism.

### E — scheduling authority can evolve without proving a new hidden maintenance mechanism

The useful cross-version distinction is authority over the service window:

```text
manual BKOPS:
    host explicitly opens the maintenance window

later inspected AUTO_EN:
    device may open/close a maintenance window during idle time
```

Therefore:

> **manual host-granted opportunity != autonomous device scheduling**

while still preserving:

> **scheduling authority != physical-target authority != hidden algorithm identity**.

A change in who schedules maintenance does not by itself prove that the underlying Flash-maintenance mechanism changed.

### E — standardizing a control plane is not standardizing the hidden algorithm

The 4.41 witnesses describe device-internal maintenance and a standard host/device handshake. They do not enumerate one universal internal algorithm.

Therefore:

> **standardized maintenance opportunity/control != standardized hidden Flash maintenance algorithm**.

Any claim that a particular BKOPS run means garbage collection, wear leveling, read reclaim, retention refresh, or block retirement still needs device-specific evidence.

## Prior-art and novelty boundary

The new result is deliberately narrow:

- public e.MMC 4.41 standard metadata names Background Operation in 2010;
- period 4.41 manufacturer documentation exposes manual `BKOPS_START` / `BKOPS_EN` and support/status fields;
- the repository's generic-manual-BKOPS floor therefore moves earlier than the 2015 e.MMC 5.1 witness.

The following remain **unproven**:

- that A441 was the first JEDEC text to define every related background-maintenance mechanism;
- that the public title difference between A44 and A441 proves a clean first-introduction event;
- that SanDisk, Kingston Solutions, JEDEC, or e.MMC invented managed-Flash background maintenance;
- that a direct technical genealogy runs from generic BKOPS to Micron automotive self refresh;
- that one hidden maintenance algorithm remained unchanged across e.MMC revisions or vendors.

A direct normative A44→A441 clause diff and the intermediate 4.5/4.51/5.0 revision sequence remain evidence debt.

## Functional analogy only — generic BKOPS vs Micron/Armadillo self refresh

The functional overlap remains **maintenance opportunity while powered**.

Generic BKOPS exposes a standardized control surface for device-internal work. The Micron/Armadillo path exposes a vendor retention policy involving reset, host-supplied time, elapsed-time eligibility, bus idleness, ECC-conditioned selection, and self-refresh telemetry.

Therefore:

```text
shared powered-idle opportunity != shared mechanism
generic BKOPS status != vendor retention eligibility
generic BKOPS start != demonstrated Micron self-refresh start
```

Nothing in the 4.41 prior-art evidence changes those boundaries.

## Philosophical limit

No philosophy is attributed to JEDEC or the manufacturers. A narrow project-level interpretation is sufficient:

> a maintenance obligation can exist independently of **who is authorized to schedule the next execution window**.

The control plane preserves evidence about capability/status/opportunity while leaving the physical cause and physical work largely hidden.

## Resulting bounded relations

```text
e.MMC 5.1 witness != origin of generic manual BKOPS
public standardized manual-BKOPS floor <= e.MMC 4.41 / 2010
standard-title boundary != invention date
BKOPS capability != current maintenance obligation
current obligation != host-granted execution opportunity
manual host scheduling != autonomous device scheduling
scheduling authority != physical-target authority
standardized control plane != standardized hidden algorithm
shared idle opportunity != shared retention mechanism
```

## Open evidence debt

- obtain and inspect the full normative JESD84-A44 and JESD84-A441 texts side by side before claiming an exact clause-level introduction point;
- trace 4.41→4.5→4.51→5.0→5.1 BKOPS control changes from direct JEDEC texts rather than endpoint summaries;
- locate an official JEDEC drafting/ballot/change-history record if invention/standardization chronology becomes material;
- keep pre-eMMC managed-Flash background-maintenance genealogy primarily in `computing-archaeology` unless a retention-specific bridge is needed;
- do not infer the hidden maintenance algorithm from the standardized control surface alone.
