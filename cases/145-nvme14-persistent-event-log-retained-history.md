# Case 145 — NVMe 1.4 Persistent Event Log: retained device event history, bounded eviction, and reporting-context snapshot

**Status:** `grounded`  
**Historical anchor:** NVM Express Base Specification Revision 1.4, dated 10 June 2019; first-party public release announcement dated 23 July 2019  
**Layer:** NVMe controller / NVM-subsystem diagnostic and maintenance history  
**Grounding record:** [`../evidence/145-nvme-2019-persistent-event-log-grounding.md`](../evidence/145-nvme-2019-persistent-event-log-grounding.md)

## Research question

What exactly is retained when NVMe 1.4 defines a **Persistent Event Log** (PEL) that survives resets and power cycles? Does “persistent” mean complete, immutable, or archival history? How does a host obtain a stable view of a log that can continue to change, and what can a recorded maintenance event prove about the underlying operation?

This case is deliberately narrower than a history of NVMe management or SSD telemetry. It studies one retention relation: a controller/NVM subsystem can preserve selected evidence of its own past across execution-boundary loss while also bounding, suppressing, reordering, or later removing portions of that evidence.

## Historical record

NVM Express Revision 1.4 is dated **10 June 2019**. Section 5.14.1.13 defines Log Identifier `0Dh`, Persistent Event Log. NVM Express, Inc. publicly announced the NVMe 1.4 Base Specification on **23 July 2019** and described the PEL as enabling “robust drive history for issue triage and debug at scale.”

Those two dates are different claims: the document date is a specification anchor and 23 July is a first-party public-release announcement. Neither establishes invention priority, the first implementation, or the first product shipment.

The 1.4 PEL event vocabulary includes SMART/Health Log Snapshot, Firmware Commit, Timestamp Change, Power-on or Reset, NVM Subsystem Hardware Error, Change Namespace, Format NVM Start/Completion, Sanitize Start/Completion, Set Feature, Telemetry Log Created, Thermal Excursion, and vendor-defined classes. The breadth matters: the PEL is not merely a self-test result ring or a user-data journal.

## Engineering reconstruction

### 1. Persistence retains diagnostic history, not namespace payload

Section 5.14.1.13 says the PEL contains information about significant events not specific to a particular command and that its information is retained across power cycles and resets. It also recommends design for minimal event-information loss on power failure.

That creates a controller/subsystem historical relation which can outlive one powered execution interval. It does **not** establish that user namespace writes survived the same event, nor is the PEL a second copy of namespace data.

`PEL retention across reset/power cycle != user-payload durability`

### 2. “Persistent” is not “complete”

The same section sharply limits any archival reading of the word *persistent*.

- the number of supported events is vendor specific;
- maximum log size is bounded through the controller capability (`PELS`);
- repeated events above a vendor-specific frequency threshold may be suppressed;
- if size/count/category limits are reached, event deletion policy is vendor specific;
- important older events may be retained while newer, less-important events are deleted;
- sanitize is permitted to alter the PEL, with the set of removed events unspecified.

Consequently a device may retain a useful cross-reset history without retaining an exhaustive history of everything that happened. Absence of an event from a later PEL cannot, by itself, prove that the event never occurred.

`persistent event log != exhaustive event history`

`event occurrence != indefinite event-record survival`

`event suppression/eviction != proof of non-occurrence`

`log persistence != immutability`

### 3. Report ordering is not a universal causal chronology

NVMe 1.4 says recent events should generally be reported before older ones, but the method by which the subsystem determines event order is vendor specific. A consumer can therefore use the PEL as a standardized event-history interface without upgrading report order into a universal causal clock or total-order theorem.

`reported order != universal causal chronology`

### 4. Stable reporting context and evolving underlying history are distinct states

PEL retrieval has explicit actions to establish a reporting context, read from an existing context, and release it. The reporting context may be a copy of the page data or a set of pointers; its representation is vendor specific.

The important semantic boundary is independent of representation. Events that occur while a reporting context exists are still logged, but they are not reported through that already-established context. The context can end on explicit release, reset, or a vendor-specific timeout. Thus the controller can continue to accumulate history while exposing one stable query view.

`reporting-context snapshot != underlying Persistent Event Log`

`reporting-context lifetime != PEL lifetime`

`stable retrieval view != frozen device history`

This is a useful retained-state layering example: a transient query context can preserve the membership of one observation while the longer-lived historical object keeps changing.

### 5. SMART snapshot event is historical evidence, not the current SMART page

A PEL SMART / Health Log Snapshot Event contains a snapshot of SMART/Health Information Log data. That retained copy is historical evidence about one observation point; it is not identical to the current SMART/Health page read later, nor does it replace cumulative counters that have their own semantics.

`SMART snapshot event != current SMART/Health state != cumulative counter semantics`

Case 55 supplies the older ATA/ATAPI self-test / health-history comparison and should remain a separate mechanism.

### 6. Operation evidence is not operation effect

NVMe 1.4 defines paired Format NVM Start/Completion and Sanitize Start/Completion event types. A Sanitize Start entry is recorded at operation start, while a Sanitize Completion entry records state at operation completion and carries sanitize status/progress information. The same start/completion separation appears for Format NVM.

Therefore a retained event saying that an operation started is evidence that the command passed far enough to enter that operation; it is not evidence that the destructive or formatting effect completed successfully. Even a completion record reports the controller’s completion/status relation; it is not an independent forensic proof of lower-layer physical erasure.

`maintenance-operation start evidence != completion evidence`

`PEL evidence about sanitize != sanitize mechanism/effect`

Case 44 remains the repository’s separate sanitization boundary.

## Prior art and bounded comparison

### ATA self-test logs — earlier bounded diagnostic-history prior art, not genealogy

Case 55 already grounds ATA/ATAPI-5-era self-test logging by 1999. That is earlier functional prior art for retaining bounded device diagnostic history. It blocks any claim that NVMe 1.4 invented the general idea of a storage device preserving diagnostic evidence across time.

The mechanisms and scopes are not identical. The ATA self-test log is centered on self-test execution/results, while NVMe 1.4 PEL defines a broader significant-event history, explicit cross-reset/power-cycle retention, suppression/eviction semantics, and a stable reporting-context interface. This case does not establish an ATA -> NVMe design genealogy.

### Sanitize — history about an operation is not the operation

Case 44 studies erase/sanitize authority and effect. Case 145 studies retained controller evidence that a sanitize operation started or completed. The same word appearing in both cases does not collapse the two retention relations.

## Failure modes and limits

The PEL relation can fail or become incomplete without user payload loss:

- a power failure may still cause some event-information loss despite the design recommendation to minimize it;
- high-frequency repeated events may be suppressed;
- bounded capacity can trigger vendor-specific deletion;
- sanitize may alter/remove events;
- ordering is vendor specific;
- reporting context can expire or be destroyed by reset;
- a logged start event can survive even when the corresponding maintenance operation does not complete successfully.

Conversely, losing or pruning a PEL entry does not prove that the underlying user payload was altered.

## Philosophical interpretation — downstream only

A narrow inference is justified after the mechanism is established: a technical system can retain **selected evidence of its own prior events** while also implementing rules that intentionally suppress, evict, or rewrite portions of that evidence. Persistence can therefore name a bounded relation to the past without naming total historical conservation.

Do not inflate that observation into a claim that the PEL is human memory, an archive in the institutional sense, or Stieglerian tertiary retention. Those are optional interpretive comparisons, not engineering identities.

## Stop conditions

This case does **not** establish:

- that NVMe 1.4 or NVM Express invented persistent device diagnostic logging;
- the first proposal, ballot, implementation, or shipping SSD supporting PEL;
- one universal vendor eviction algorithm or exact PEL capacity;
- tamper evidence, authenticated logging, legal/compliance WORM behavior, or forensic completeness;
- that a Sanitize Start/Completion event independently proves physical media erasure;
- product-specific power-fail correctness or fault-injection behavior;
- a direct ATA/SCSI -> NVMe genealogy.

Those are follow-up work, not implicit conclusions.

## Related-repository boundary

A fresh search of `tmzncty/computing-archaeology` found no dedicated NVMe Persistent Event Log study to reuse. Broader NVMe log-page genealogy, controller-management history, standards-proposal archaeology, and product adoption belong there if developed. `technical-retention` keeps the narrower cross-reset history, bounded forgetting, reporting-context, and operation-evidence relations.

## Sources

- NVM Express, Inc., *NVM Express Base Specification*, Revision 1.4, 10 June 2019, especially §5.14.1.13 and §5.14.1.13.1: https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4-2019.06.10-Ratified.pdf
- NVM Express, Inc., “New NVM Express, Inc. Specifications Bolster Cloud and Enterprise Advancements,” 23 July 2019: https://nvmexpress.org/new-nvm-express-inc-specifications-bolster-cloud-and-enterprise-advancements/
- Cross-case prior art: [`55-nvme-smart-health-endurance-telemetry.md`](55-nvme-smart-health-endurance-telemetry.md)
- Sanitization boundary: [`44-storage-sanitize-deallocation-vs-erasure.md`](44-storage-sanitize-deallocation-vs-erasure.md)
