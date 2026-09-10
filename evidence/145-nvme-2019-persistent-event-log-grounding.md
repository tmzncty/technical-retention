# Evidence 145 — NVMe 1.4 Persistent Event Log grounding

**Case:** [`../cases/145-nvme14-persistent-event-log-retained-history.md`](../cases/145-nvme14-persistent-event-log-retained-history.md)  
**Evidence status:** primary standards/first-party organization evidence (`H/P`) plus bounded engineering reconstruction (`E`) and explicit functional comparison (`A`/`X`)  
**Scope:** NVMe 1.4 Persistent Event Log (PEL), its persistence/completeness boundary, reporting context, and maintenance-operation event evidence

## Source register

### P1 — NVM Express Base Specification Revision 1.4

- **Organization:** NVM Express, Inc.
- **Document:** *NVM Express Base Specification*, Revision 1.4
- **Document date:** 10 June 2019
- **Origin:** NVM Express official site
- **URL:** https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4-2019.06.10-Ratified.pdf
- **Primary locations:**
  - title/front matter: revision/date;
  - §5.14.1.13, Persistent Event Log (Log Identifier `0Dh`): retention across power cycles/resets, power-failure guidance, sanitize interaction, order, bounds, suppression/deletion, reporting context;
  - §5.14.1.13.1 and event-type table: event vocabulary;
  - §5.14.1.13.1.1: SMART / Health Log Snapshot Event;
  - §5.14.1.13.1.7–.10: Format NVM and Sanitize Start/Completion events.
- **Use:** normative mechanism and event-format evidence.

### P2 — NVM Express 1.4 release announcement

- **Organization:** NVM Express, Inc.
- **Title:** “New NVM Express, Inc. Specifications Bolster Cloud and Enterprise Advancements”
- **Date:** 23 July 2019
- **Origin:** NVM Express official site
- **URL:** https://nvmexpress.org/new-nvm-express-inc-specifications-bolster-cloud-and-enterprise-advancements/
- **Use:** first-party public release chronology and contemporary purpose statement: PEL as robust drive history for triage/debug at scale.

## Historical claims supported

### H1 — 10 June 2019 is a document anchor, not a public-release or invention date

P1 identifies itself as Revision 1.4 and is dated 10 June 2019. P2 publicly announces release on 23 July 2019. These are distinct chronology facts. This pass does not infer first proposal, first implementation, first shipment, or invention priority.

### H2 — NVM Express publicly framed PEL as retained drive history

P2 lists Persistent Event Log among NVMe 1.4 features and describes its purpose as robust drive history for issue triage/debug at scale. P1 supplies the normative semantics behind that first-party framing.

## Mechanism claims supported

### E1 — PEL history survives power cycles/resets, but this does not prove user-payload durability

P1 §5.14.1.13 requires PEL information to be retained across power cycles and resets and recommends minimal event-information loss on power failure. The object retained is significant-event log information at NVM-subsystem scope. No clause turns the PEL into a second copy of namespace data.

**Safe relation:** `PEL persistence != namespace-payload persistence`.

### E2 — persistence is explicitly compatible with bounded forgetting

P1 §5.14.1.13 makes event count vendor specific and reports maximum supported PEL size through `PELS`. It allows repeated high-frequency instances to be suppressed and permits vendor-specific event deletion when size/count/category limits are reached; an older important event may outlive a newer event. Sanitize may also remove or alter events.

**Safe relations:**

- `persistent log != exhaustive history`;
- `event occurred != record survives indefinitely`;
- `absence from a later PEL != proof of non-occurrence`;
- `persistent != immutable`.

This is the central counterexample against reading “persistent” as “complete archive.”

### E3 — PEL report order is not a universal total-order clock

P1 says newer events should generally be reported earlier, while the subsystem's method for deciding event order is vendor specific.

**Safe relation:** `reported ordering != universal causal chronology`.

### E4 — reporting context retains one observation membership while the underlying PEL continues changing

P1 defines actions that establish/read/release a PEL reporting context. The implementation may retain page data itself or pointers; that representation is vendor specific. The normative behavioral boundary is that events occurring while the context exists are still logged but are excluded from the already-established context. Context lifetime ends independently through release, reset, or vendor timeout.

**Safe relations:**

- `reporting context != underlying PEL`;
- `context lifetime != PEL lifetime`;
- `stable read membership != frozen device history`.

### E5 — a SMART snapshot event is historical evidence distinct from current SMART state

P1 §5.14.1.13.1.1 defines event data as a snapshot of SMART/Health Information Log data. A later current SMART page and cumulative counters therefore answer different temporal questions.

**Safe relation:** `SMART snapshot event != current SMART state != cumulative-counter semantics`.

### E6 — operation-start evidence is weaker than completion evidence

P1 defines separate Format NVM Start/Completion and Sanitize Start/Completion events. §5.14.1.13.1.9 records Sanitize Start at operation start; §5.14.1.13.1.10 records Sanitize Completion at operation completion and includes sanitize status/progress information. A start entry therefore cannot demonstrate completion. A completion entry still records controller-reported operation status rather than independently proving lower-media forensic erasure.

**Safe relations:**

- `operation-start record != operation-completion record`;
- `PEL record about sanitize != sanitize implementation/effect`.

## Event-vocabulary significance

P1's event-type table includes, among other classes:

- SMART / Health Log Snapshot;
- Firmware Commit;
- Timestamp Change;
- Power-on or Reset;
- NVM Subsystem Hardware Error;
- Change Namespace;
- Format NVM Start and Completion;
- Sanitize Start and Completion;
- Set Feature;
- Telemetry Log Created;
- Thermal Excursion;
- vendor-specific / TCG-defined entries.

This supports treating PEL as broader significant-device-event history rather than normalizing it to one self-test or one command journal.

## Prior art and cross-case check

### Case 55 — ATA/ATAPI self-test history

`cases/55-nvme-smart-health-endurance-telemetry.md` already grounds ATA/ATAPI-5-era self-test logging by 1999. That is earlier functional prior art for bounded retained storage-device diagnostic history. It prevents an NVMe-origin claim for the general idea.

The mechanisms remain distinct: the ATA self-test log is centered on self-test history/results, while NVMe 1.4 PEL standardizes broader event classes, reset/power-cycle persistence, suppression/eviction, and reporting context.

**Classification:** functional prior art (`A`/`X`), not demonstrated genealogy.

### Case 44 — sanitize effect

Case 44 studies command/interface semantics for deallocation versus sanitize/erasure. PEL's Sanitize Start/Completion entries are retained evidence *about* such an operation, not the destructive mechanism itself.

**Classification:** bounded functional comparison (`A`/`X`).

### `computing-archaeology`

A fresh repository search for `Persistent Event Log` / `NVMe` found no dedicated PEL case to reuse. Broader NVMe log-page history, standards-proposal genealogy, controller firmware evolution, and shipping-product adoption should be routed there if developed.

## Counterclaims explicitly rejected

This evidence does not support:

1. “PEL stores every significant event forever.”
2. “If no PEL entry is present, the event did not occur.”
3. “Persistence across reset proves namespace payload durability.”
4. “The PEL is append-only, immutable, authenticated, tamper evident, or compliance WORM.”
5. “Report order is a universal causal ordering.”
6. “A reporting context freezes the underlying device log.”
7. “A Sanitize Start event proves sanitization completed.”
8. “A Sanitize Completion record independently proves physical forensic erasure.”
9. “NVMe 1.4 invented persistent device diagnostic logs.”
10. “Earlier ATA diagnostic history demonstrates direct ATA -> NVMe genealogy.”

## Follow-up evidence debt

- recover and compare the exact NVMe technical proposal / ratification chain that introduced PEL;
- trace changes from 1.4 through later Base Specification revisions;
- add a named shipping SSD with documented `PELS`, event capacity, and support behavior;
- test real eviction/suppression behavior where a safe repeatable setup exists;
- test reporting-context behavior under concurrent events and resets;
- test power-failure retention rather than inferring product compliance from the standard;
- compare PEL with authenticated/tamper-evident audit logging without normalizing the categories;
- characterize sanitize-induced event removal on named implementations.
