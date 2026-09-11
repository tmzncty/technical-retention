# Case 135 Deepening Evidence — e.MMC 5.1 BKOPS Maintenance Opportunity vs Vendor Self-Refresh

## Status

**`grounded`** for the bounded distinction between JEDEC e.MMC 5.1 background-operation control and the Micron/Armadillo vendor self-refresh path already documented in Case 135.

This record does **not** claim that BKOPS is a retention-refresh command, that every background operation is Flash refresh, or that e.MMC 5.1 invented internal Flash maintenance.

## Research question

Case 135 already shows a vendor-specific Micron e.MMC path in which reset, host-supplied time, bus idleness, an ECC-related threshold, and retained maintenance statistics participate in data-retention work. This deepening asks a different question:

> What does the standard e.MMC 5.1 BKOPS interface actually expose about internal maintenance, and which parts of that interface must remain separate from Micron's documented self-refresh semantics?

## Source boundary

### Primary technical source

- JEDEC Solid State Technology Association, **JESD84-B51, Embedded Multi-Media Card (e.MMC) Electrical Standard (5.1)**, February 2015, especially §6.6.25 and EXT_CSD fields `BKOPS_STATUS[246]`, `BKOPS_START[164]`, and `BKOPS_EN[163]`. Official historical URL: <https://www.jedec.org/system/files/docs/JESD84-B51.pdf>. The official endpoint was not directly retrievable in this research environment; the standard text was inspected through a text mirror preserving JEDEC pagination and field numbering: <https://studylib.net/doc/27873175/emmc5.1%E5%AE%98%E6%96%B9%E6%A0%87%E5%87%86%E5%8D%8F%E8%AE%AE>.

### Publication/date corroboration

- The 24 February 2015 JEDEC e.MMC 5.1 announcement, reproduced by Design & Reuse, identifies JESD84-B51 and lists **Background Operation Control** among the revision's added features: <https://www.design-reuse.com/news/202526512-jedec-announces-publication-of-e-mmc-standard-update-v5-1/>.

### Existing Case 135 witnesses

- Atmark Techno, **Armadillo-IoT Gateway G4 Product Manual v1.0.0**, 9 December 2021: <https://manual.atmark-techno.com/armadillo-iot-g4/armadillo-iotg-g4_product_manual_ja-1.0.0/ch09.html>.
- Micron catalog entry for **TN-FC-60, Refresh Features for Micron e.MMC Automotive 5.1 Devices**, 11 April 2023: <https://www.micron.com/products/storage/emmc/software-downloads>.

## Historical record

### H/P — background operations expose a maintenance-control relation

JESD84-B51 §6.6.25 says e.MMC devices have internal maintenance operations and separates host-serviced foreground work from background work executed while the host is not being serviced. The standard does not identify every background operation as garbage collection, wear leveling, read reclaim, data refresh, or block retirement.

### H/P — manual BKOPS grants a service window

Writing `BKOPS_START[164]` manually starts background operations and the device remains busy until no more background processing is needed. `MANUAL_EN` in `BKOPS_EN[163]` tells the device that the host expects to start background operations periodically; the device may then delay some maintenance until such a host-granted window.

```text
host advertises future maintenance opportunities
    -> device may defer some internal maintenance
    -> host opens a BKOPS service window
    -> device performs currently needed background processing
```

The physical target set and rewrite geometry remain hidden.

### H/P — BKOPS_STATUS is urgency, not a maintenance transcript

`BKOPS_STATUS[246]` reports four levels: no operations required, non-critical outstanding work, performance-impacting outstanding work, and critical outstanding work. Levels 2 and 3 can surface `URGENT_BKOPS`; at level 3 foreground operations may exceed their original timeouts because maintenance can no longer be delayed.

This is an urgency/control summary, not a page-movement, erase, ECC-event, or refresh-completion log.

### H/P — e.MMC 5.1 permits autonomous idle-time BKOPS

With `AUTO_EN` set, the device may start or stop background operations during idle time without notifying the host. The standard advises the host to keep device power active while autonomous BKOPS is permitted, while allowing the host to set or clear the bit according to power constraints.

The same section says Background Operations support is mandatory for this specification and requires the support indication in `BKOPS_SUPPORT[502]`.

### H/P — BKOPS and Sanitize are separate controls

JESD84-B51 defines `SANITIZE_START[165]` separately from `BKOPS_START[164]`. The first starts sanitize; the second starts background operations. Generic internal maintenance therefore must not be silently promoted into a sanitization claim.

## Engineering reconstruction

### E — capability, obligation, urgency, opportunity, execution, and completion differ

```text
BKOPS supported
    != background work outstanding
    != background work urgent
    != maintenance opportunity granted
    != background processing executing
    != no more BKOPS work currently needed
```

### E — maintenance opportunity is not mechanism identity

BKOPS gives a device time and authority to perform internal maintenance, but does not disclose which hidden algorithm consumes that opportunity.

> **BKOPS execution != demonstrated garbage collection**
>
> **BKOPS execution != demonstrated wear leveling**
>
> **BKOPS execution != demonstrated retention refresh**

Specific implementation evidence is required for any such claim.

### E — urgency zero is narrower than a universal media-health guarantee

`BKOPS_STATUS = 0` means the device currently reports no background operations required under this interface. It does not prove every NAND cell has freshly renewed charge margin, that no latent media error exists, that no future maintenance will become due, or that physical media has been sanitized.

### E — Micron self-refresh eligibility is not BKOPS urgency

Case 135's Armadillo/Micron path uses reset, `SET_TIME (CMD49)`, elapsed-time qualification, bus idleness, Delay 2, and an ECC-related threshold. JESD84-B51 BKOPS exposes generic maintenance support, urgency, and scheduling controls.

The inspected sources do not establish that `SET_TIME` updates BKOPS urgency, that BKOPS status is the self-refresh queue, that starting BKOPS starts Micron self refresh, or that completing BKOPS means Micron self refresh completed.

> **vendor self-refresh due != generic BKOPS urgency**
>
> **shared idle opportunity != shared mechanism**

### E — scheduling authority and physical-target authority are separate

Manual versus autonomous BKOPS changes who opens the service window without requiring the standard to disclose physical target selection. Case 135's self-refresh path similarly gives the host time/reset inputs while the controller retains local ECC-conditioned selection.

## Functional comparison only

The useful comparison between generic BKOPS and Case 135 vendor self refresh is **powered maintenance opportunity**. Their exposed policy evidence is different. This is a functional analogy, not evidence of state-machine identity or genealogy.

Cases 36 and 37 provide stronger evidence about refresh-like behavior than generic BKOPS does; Case 150 grounds a more specific reclamation relation. None should be used to fill in BKOPS's intentionally hidden mechanism.

## Prior-art and chronology boundary

The safe chronology in this slice is limited:

- JESD84-B51 is dated **February 2015**;
- the February 2015 publication announcement lists **Background Operation Control** among e.MMC 5.1 changes;
- JESD84-B51 defines the manual and autonomous controls described above.

This pass does **not** establish when manual BKOPS first appeared, when a vendor first shipped comparable background maintenance, or who invented autonomous managed-Flash maintenance. Those broader genealogies belong in `computing-archaeology` if pursued. A fresh search there for `BKOPS` found no dedicated module to reuse.

## Sanitization boundary

> **BKOPS complete / BKOPS_STATUS=0 != sanitize complete != verified physical erasure**

Nothing in the generic BKOPS interface proves stale physical embodiments of user data are unrecoverable.

## Philosophical limit

No historical philosophy is attributed to JEDEC, Micron, or Atmark. A narrow project-level interpretation is sufficient: a managed storage system can expose a compact **maintenance obligation signal** and a **maintenance opportunity protocol** without exposing the physical work that makes the obligation disappear.

## Resulting bounded relations

```text
maintenance capability != current maintenance obligation
current obligation != urgency
urgency != execution
execution != disclosed physical mechanism
no current BKOPS work != all future retention risk eliminated
vendor self-refresh due != generic BKOPS urgency
shared idle opportunity != mechanism identity
BKOPS completion != sanitization
```

## Remaining evidence debt

- inspect pre-5.1 JEDEC revisions directly to establish the chronology of manual BKOPS versus later background-operation control;
- obtain the full Micron TN-FC-60 body and test whether it explicitly relates self refresh to standard BKOPS controls;
- obtain a named Micron part/firmware record exposing both BKOPS fields and the vendor self-refresh feature;
- gather fault-injection or telemetry evidence for interrupted vendor self-refresh/BKOPS interaction;
- keep host-tooling one-time-programmable warnings separate unless the exact field semantics are directly verified for the target revision/device.
