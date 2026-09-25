# Case 111 — NVMe 2.1 Host-Initiated Refresh observability boundary

**Status:** Case 111 remains `grounded`.

## Scope

NVM Express Base Specification Revision 2.1, ratified 5 August 2024, introduced the optional **Host-Initiated Refresh (HIR)** capability through TP4058, *Environmental Extremes Management*. The bounded question here is whether a public storage interface can expose refresh-specific timing and progress rather than only generic background-maintenance status.

## Historical record

The official Revision-2.1 change summary says TP4058 adds Host-Initiated Refresh as part of Device Self-test and updates the Device Self-test Log page.

Revision 2.1 section 8.1.11 describes HIR as implementation-specific media-refresh work intended to verify media integrity and ensure media access, including after long periods without operation or extreme environmental exposure. The examples include read verification, selective rewriting of media with high correctable-error rates, and other maintenance activities. Stored user data is not changed by the operation.

The same section gives HIR an **all-media NVM-subsystem scope** and states that the Device Self-test log reports **Current Percentage Complete** for HIR.

Identify Controller also exposes two HIR-specific timing fields:

- **RHIRI** — Recommended Host-Initiated Refresh Interval, expressed in days from the last power down to the recommended intervention point;
- **HIRT** — Host-Initiated Refresh Time, the nominal number of minutes the device reports for completing HIR.

The Device Self-test processing description separates acceptance/start of HIR from the later end of the refresh operation. A 2025 UNH-IOL conformance test independently reflects the same distinction by observing the Device Self-test log while HIR remains in progress and waiting until the log reports that the operation has finished.

## Engineering reconstruction

The public interface now supports this bounded decomposition:

```text
HIR capability
    -> recommended intervention interval
    -> refresh operation admitted
    -> refresh work in progress
    -> percentage-complete evidence
    -> refresh operation finished
```

The following distinctions are project engineering language, not NVM Express historical terminology:

```text
refresh admission
    != refresh execution
    != refresh progress evidence
    != refresh-operation completion
```

A second useful separation is:

```text
RHIRI = recommended scheduling horizon
HIRT  = nominal run duration
log   = observed current progress
scope = all media in the NVM subsystem
```

## What this changes in Case 111

Earlier eMMC evidence showed that a named product may expose refresh capability next to generic BKOPS without publicly binding generic BKOPS completion to refresh completion.

NVMe 2.1 supplies a different standards design:

```text
named refresh-class operation
    + refresh-specific support
    + refresh-specific scheduling hint
    + refresh-specific nominal duration
    + refresh-operation percentage complete
    + all-media operation scope
```

Thus the standards-level question “can a public storage interface make retention-oriented refresh progress separately observable?” is boundedly closed.

The stronger product-level question remains open: identify a named shipping SSD/NVMe product and firmware that actually advertises and exercises HIR.

## Anti-collapse rules

```text
HIR accepted / started
    != HIR operation finished

HIR percentage complete
    != future offline-retention guarantee

HIR all-media scope
    != every physical page necessarily rewritten

HIRT nominal duration
    != measured completion time

RHIRI recommended interval
    != deterministic retention-failure deadline

NVMe 2.1 capability definition
    != named-product adoption

standardized interface
    != disclosed media-refresh algorithm
```

The specification also defines events that end an in-progress HIR rather than preserving it as a restart checkpoint. Therefore current refresh progress should not be treated as evidence of a restart-persistent maintenance checkpoint.

## Functional comparison

The comparison with eMMC BKOPS is functional only. eMMC BKOPS supplies a generic maintenance-debt/execution surface; NVMe 2.1 HIR supplies an explicitly named refresh-class operation with refresh-specific timing and progress. No JEDEC-to-NVMe genealogy, shared implementation, or common firmware architecture is claimed.

## Philosophical interpretation

A narrow interpretation survives the mechanism: controller-internal maintenance can remain physically opaque while the public interface still exposes bounded evidence about when work is due, whether it is running, how far it has progressed, and when the defined operation has ended. Operation completion still does not reveal every lower-layer physical event.

## Related-repository boundary

Fresh searches of `tmzncty/computing-archaeology` for `Host-Initiated Refresh`, `TP4058`, `NVMe 2.1 refresh`, and `Environmental Extremes Management` found no dedicated packet to reuse. Broad NVMe feature genealogy and product-adoption archaeology belong there if pursued.

## Remaining debt

1. Find a first-party named SSD/NVMe implementation that reports HIR support and preferably RHIRI/HIRT plus observed progress/completion behavior.
2. Deepen the exact result semantics for successful, interrupted, and error-ending HIR operations.
3. Keep implementation-specific read verification and rewrite policy separate from the standardized interface.

## Primary / institutional sources

- NVM Express, *NVM Express Base Specification, Revision 2.1*, ratified 5 August 2024.
- NVM Express, *NVM Express Revision 2.1 Changes*, TP4058 / Environmental Extremes Management.
- University of New Hampshire InterOperability Laboratory, *NVM Command Set Conformance Test Suite*, Host-Initiated Refresh test, 2025.

