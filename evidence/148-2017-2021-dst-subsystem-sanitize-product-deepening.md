# Evidence 148 — NVMe Device Self-test: Subsystem Scope, Sanitize-Driven Retirement, and a Named Commercial Witness (2017–2021)

Status: **`bounded deepening complete`**

Canonical case: [`../cases/148-nvme13-device-self-test-reset-surviving-maintenance.md`](../cases/148-nvme13-device-self-test-reset-surviving-maintenance.md)

## Research question

Case 148 already grounds the most striking NVMe 1.3 retention rule: a short Device Self-test is aborted by Controller Level Reset, while an extended Device Self-test must persist across Controller Level Reset and resume after restoration of power.

This slice asks three narrower questions that were still underdeveloped:

1. Was the current self-test relation in NVMe 1.3 necessarily controller-local, or could the specification make **one in-progress operation authoritative for the whole NVM subsystem**?
2. How did NVMe 1.4 change the relation between an unfinished self-test and the subsystem-wide Sanitize operation?
3. Is there a named commercial NVMe 1.3-generation SSD for which the vendor publicly advertised Device Self-test, without pretending that the advertisement is reset/power fault-injection evidence?

The result is useful because it separates three different things that are easy to flatten into “the device is running a test”:

```text
maintenance execution state
    != maintenance concurrency / authority domain
    != later conflicting-operation policy
    != product-level implementation witness
```

---

## Source classes and confidence

### Primary normative sources

1. **NVM Express Revision 1.3**, ratified 26-Apr-2017, document dated 1-May-2017.
   - Device Self-test command processing: §5.8 / Figure 68.
   - Identify Controller Device Self-test Options (`DSTO`): Identify Controller bytes 318 / Figure 109-era table.
   - Device Self-test Log: §5.14.1.6 / Figure 98–99.
   - Device Self-test operation rules: §8.11.
   - Sanitize command / subsystem behavior: §5.24 and §8.15.
   - URL: <https://nvmexpress.org/wp-content/uploads/NVM_Express_Revision_1.3.pdf>

2. **NVM Express Revision 1.4c**, dated 9-Mar-2021, preserving the Revision 1.4 requirements relevant here.
   - Device Self-test command processing: §5.8 / Figure 169.
   - Device Self-test Log and result code `9h`: §5.14.1.6 / Figure 203–204.
   - Sanitize command: §5.24.
   - Device Self-test operations: §8.11.
   - URL: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4c-2021.06.28-Ratified.pdf>

3. **NVM Express, Changes in NVMe Revision 1.4**.
   - Explicitly classifies “Sanitize during Device Self-Test” as a **mandatory / incompatible change**.
   - Attributes that change to Technical Proposal `4022`.
   - URL: <https://nvmexpress.org/changes-in-nvme-revision-1-4/>

### Primary product source

4. **Intel SSD D7-P5510 Product Brief**, document number `345311-001`, marked `1220` (December 2020), now preserved by Solidigm.
   - Names the product as Intel SSD D7-P5510.
   - Lists interface as PCIe 4.0 x4, NVMe 1.3c.
   - Explicitly advertises “Device self-test” and says the host may request the SSD to perform tests including SMART check, volatile-memory backup, NVM integrity, and drive-life checks.
   - URL: <https://www.solidigm.com/content/dam/solidigm/en/site/products/data-center/d7/p5510/documents/d7-p5510-series-product-brief.pdf>

### Provenance limit

The official NVM Express archive exposes a “NVM Express 1.4 Ratified TPs” ZIP, and the official Revision 1.4 changes page attributes the sanitize/self-test change to **TP4022**. In this slice, the TP4022 proposal body itself was **not directly inspected**. Therefore:

> official change-log attribution to TP4022 != direct inspection of TP4022 drafting language

No claim below depends on unseen TP text.

---

## Historical record A — NVMe 1.3 already allowed two different self-test authority domains

NVMe 1.3 did not define “self-test in progress” as necessarily local to one controller.

The Identify Controller data structure includes **Device Self-test Options (`DSTO`)**. Bit 0 distinguishes two models:

- bit 0 cleared: the NVM subsystem supports **one Device Self-test operation per controller** at a time;
- bit 0 set: the NVM subsystem supports **only one Device Self-test operation in progress for the entire NVM subsystem**.

Figure 68 then uses the same bit when deciding what “Self-test in Progress” means for a newly received Device Self-test command. With `DSTO[0]=0`, the conflict is controller-local. With `DSTO[0]=1`, the conflict relation is subsystem-wide.

This yields a state distinction not explicit in the original Case 148 grounding:

```text
current self-test operation state
    != scope in which that state excludes another self-test
```

The same command family can therefore expose different **maintenance-authority domains**.

### Engineering reconstruction

A useful project-level model is:

```text
controller A starts self-test
    + DSTO[0] = 0
        -> controller B may have its own self-test relation

controller A starts self-test
    + DSTO[0] = 1
        -> subsystem already has the one permitted self-test relation
        -> another start sees subsystem-wide “in progress” state
```

`maintenance-authority domain` is engineering language used by this repository. NVMe 1.3 speaks in terms of controller or NVM-subsystem support for simultaneous Device Self-test operations.

### What this does not prove

It does **not** disclose where a subsystem-wide current-operation record is physically stored.

It does **not** require one controller to own all diagnostic execution hardware.

It does **not** prove that every multi-controller NVMe 1.3 subsystem set `DSTO[0]=1`.

It does **not** make the Device Self-test Log a distributed consensus log.

The normative fact is the externally visible concurrency/authority contract.

---

## Historical record B — NVMe 1.3 Sanitize was already subsystem-wide, but did not yet explicitly retire Device Self-test

NVMe 1.3 already described Sanitize as a subsystem-wide operation. When a sanitize operation starts on any controller, the specification says **all controllers in the NVM subsystem** update or restrict several pieces of state and behavior. During sanitize, all controllers and namespaces are subject to command restrictions.

That matters because Device Self-test and Sanitize already inhabited overlapping subsystem control space in 2017.

However, the original Revision 1.3 §8.11 short-test abort list contains Controller Level Reset, certain Format NVM interactions, explicit Device Self-test abort, and optional namespace-removal abort. The inspected Revision 1.3 text does **not** contain the later rule that starting Sanitize must abort in-progress Device Self-test operations.

Likewise, the Revision 1.3 Self-test Result status table has result values `0h` through `8h`, with `9h` through `Eh` reserved. There is no dedicated `9h = aborted due to sanitize operation` result in the inspected 2017 table.

Therefore the safe historical boundary is:

```text
NVMe 1.3:
Sanitize is subsystem-wide
    != explicit normative rule that sanitize start retires all DST work
```

This is stronger than merely noticing different wording in two editions, because the later NVM Express revision-changes page explicitly categorizes the added sanitize/self-test rule as a required incompatible change.

---

## Historical record C — NVMe 1.4 makes sanitize a subsystem-wide retirement event for Device Self-test

The official “Changes in NVMe Revision 1.4” page says:

- **Sanitize during Device Self-Test** is a mandatory behavior change;
- when a sanitize operation starts on any controller, **all controllers in the NVM subsystem shall abort Device Self-test operations in progress**;
- the change is associated with **Technical Proposal 4022**.

Revision 1.4c preserves the normative rule in §5.24. Its Sanitize start behavior now includes aborting Device Self-test operations in progress across the subsystem.

Section 8.11 correspondingly says both short and extended Device Self-test operations **shall be aborted when a sanitize operation is started**.

This creates a particularly useful boundary for the extended test:

```text
extended Device Self-test
    + Controller Level Reset / power restoration
        -> same maintenance obligation survives and resumes

extended Device Self-test
    + Sanitize start
        -> maintenance obligation is terminated
        -> outcome evidence is created as an abort result
```

So:

> **survives a failure boundary != survives every stronger administrative state transition**.

Retention horizon is operation-relative, not an intrinsic “persistent/not persistent” property of one opaque state blob.

---

## Historical record D — NVMe 1.4 adds an explicit historical reason for the sanitize retirement

Revision 1.4c extends the Device Self-test Result status values with:

```text
9h = Operation was aborted due to a sanitize operation
```

This is important because the new policy does not merely make the current operation disappear.

The existing Device Self-test ordering rule requires a result structure to be created before the Current Device Self-test Operation is cleared. Combined with the new `9h` result code, sanitize-driven retirement can be represented as:

```text
current maintenance obligation
    -> conflicting subsystem sanitize begins
    -> self-test is aborted
    -> bounded historical evidence records sanitize as the abort reason
    -> current-operation state is retired
```

This is a clean example of **state-class conversion**:

```text
current obligation
    != retained outcome evidence about the retired obligation
```

The operation stops being current, while selected evidence of why it stopped becomes part of the bounded newest-20 history.

---

## Authority and scope: four relations that must remain separate

This slice supports at least four distinct relations:

1. **execution scope** — which controller / namespaces the test is checking;
2. **concurrency authority scope** — whether another Device Self-test may coexist on another controller (`DSTO[0]`);
3. **interruption-survival scope** — which events preserve the current operation (e.g. reset/power restoration for extended test);
4. **conflict-retirement scope** — which later administrative operations require the current self-test to end (sanitize in NVMe 1.4).

They are not interchangeable:

```text
tests one namespace
    != controller-local concurrency domain

subsystem-wide single-DST policy
    != test necessarily covers every namespace

reset-surviving extended test
    != sanitize-surviving extended test
```

This is a concrete reason not to model “maintenance persistence” with a single boolean.

---

## Named commercial witness — Intel SSD D7-P5510

The December-2020 Intel D7-P5510 product brief provides a bounded commercial implementation witness.

It identifies the D7-P5510 as a PCIe 4.0 x4 SSD using **NVMe 1.3c** and explicitly lists **Device self-test** among firmware/manageability capabilities. The brief says the host may request the SSD to perform tests intended to ensure correct operation, naming examples such as SMART check, volatile-memory backup, NVM integrity, and drive life.

This closes one narrow part of the Case 148 product-evidence debt:

> **Device Self-test was not only paper-standard functionality; a named shipping enterprise SSD family publicly advertised it.**

But the source class matters.

The product brief does **not** report:

- a Controller Level Reset injected during an extended self-test;
- a full power cut and observed resumed segment;
- how current progress was persisted internally;
- whether the newest-20 result population survives every reset or firmware-update boundary;
- which exact D7-P5510 firmware revisions implemented which Device Self-test behavior;
- raw `Identify Controller`, `DSTO`, or Device Self-test Log captures from the product.

Therefore:

```text
named product advertises Device Self-test
    != reset/power continuation empirically verified on that product
```

The stronger named-controller fault-injection debt remains open.

### Informative segment resemblance is not implementation proof

The D7-P5510 brief names SMART check, volatile-memory backup, NVM integrity, and drive-life checks. Those closely resemble items in the NVMe Device Self-test informative example.

The safe statement is that the vendor advertises a set of diagnostic functions aligned with the standard feature.

Do **not** infer that the firmware executes the informative Figure 280/analogous sequence exactly, in that order, or with the same segment numbering.

```text
vendor feature summary resembles informative standard example
    != disclosed internal test program
```

---

## Cross-case functional comparisons

### Case 18 — OpenZFS scrub progress and completion

Case 18 deepens a long-running maintenance process whose progress can be checkpointed and resumed, and separates “work performed” from “work durably checkpointed.” Case 148 instead specifies an external contract that an extended self-test survives reset/power restoration while leaving exact resume segment implementation vendor specific.

Functional similarity:

```text
maintenance identity may survive interruption
```

Important difference:

```text
OpenZFS implementation exposes checkpoint machinery
    != NVMe standard discloses SSD-internal checkpoint embodiment
```

No genealogy is claimed.

### Case 56 — Kafka high-watermark checkpoint loss

Case 56 shows omission of one control-state key can later change recovery behavior even when payload log bytes survive. Case 148 shows a different pattern: the standard requires preservation/reconstitution of an unfinished maintenance relation across selected failure boundaries, but may deliberately retire it at a stronger conflicting operation.

Shared project lesson only:

```text
payload survival
    != sufficient description of recovery / maintenance state
```

No mechanism or historical lineage is shared.

### Case 66 — Persistent Event Log

The Device Self-test newest-20 history remains distinct from NVMe 1.4 Persistent Event Log.

The new sanitize abort result (`9h`) is a self-test result-state transition. It does not convert the Device Self-test Log into PEL, nor prove identical retention/deletion semantics.

---

## Philosophical boundary

A narrow interpretation is justified:

> A technical system may preserve an unfinished obligation through one class of interruption yet intentionally terminate that same obligation when a later operation changes the authority conditions under which the work remains meaningful.

The historical mechanism is not “memory deciding to forget.” It is a standards-defined state transition between:

- current diagnostic work;
- subsystem-wide conflicting maintenance;
- and bounded outcome evidence.

Do not promote this into a universal theory of memory, institutional authority, or distributed consensus.

---

## Explicit non-claims

This evidence does **not** claim that:

1. NVMe invented storage-device self-test.
2. `DSTO[0]=1` is mandatory on all NVMe 1.3 devices.
3. `DSTO[0]=1` means every self-test tests the whole subsystem.
4. a subsystem-wide current self-test is stored in one particular flash page or controller NVRAM object.
5. Device Self-test is equivalent to SMART, SCSI SEND DIAGNOSTIC, ATA SMART self-test, scrub, or patrol read.
6. NVMe 1.3 required sanitize to abort an in-progress Device Self-test.
7. the absence of a 1.3 `9h` result code proves implementations could not choose to stop a self-test during sanitize for vendor-specific reasons.
8. the 1.4 sanitize rule was inferred only from later text; NVM Express itself labels it a required change and links it to TP4022.
9. TP4022’s proposal body was directly inspected in this slice.
10. an extended self-test that survives reset retains every internal instruction pointer or physical-block frontier.
11. the newest-20 Device Self-test result population necessarily has the same persistence horizon as the active extended test.
12. a sanitize-driven DST abort means sanitize itself completed successfully.
13. a `9h` self-test result is proof that user data was successfully sanitized.
14. D7-P5510 advertising Device Self-test proves its reset/power-resume path was fault-tested here.
15. D7-P5510’s listed diagnostic functions reveal its exact internal self-test segment sequence.
16. a successful Device Self-test proves archival fitness, secure erasure, or complete media correctness.

---

## Claim ledger

| Claim | Type | Strength | Evidence |
| --- | --- | --- | --- |
| NVMe 1.3 supports either one DST per controller or one DST per subsystem according to `DSTO[0]` | historical / normative | strong | NVMe 1.3 Identify Controller + Figure 68 |
| NVMe 1.3 Sanitize already has subsystem-wide behavior | historical / normative | strong | NVMe 1.3 §5.24 / §8.15 |
| Inspected NVMe 1.3 DST abort lists do not include sanitize and result `9h` is reserved | historical / normative | strong | NVMe 1.3 §8.11 + Figure 99 |
| NVMe 1.4 makes sanitize-start abort all in-progress DST operations across the subsystem | historical / normative | strong | official Revision 1.4 changes page + 1.4c §5.24 / §8.11 |
| NVM Express classifies sanitize-vs-DST behavior as a mandatory / incompatible change linked to TP4022 | historical / provenance | strong | official Revision 1.4 changes page |
| NVMe 1.4c uses DST result code `9h` for abort due to sanitize | historical / normative | strong | 1.4c Device Self-test Result table |
| Current maintenance obligation and historical abort evidence are different state classes | engineering reconstruction | strong, bounded | result-creation-before-clear rule + `9h` |
| Reset/power-surviving extended test need not survive sanitize | engineering reconstruction | strong, bounded | 1.4c §8.11.2 |
| Intel D7-P5510 is a named NVMe 1.3c product publicly advertising Device Self-test | historical / product | strong | Intel/Solidigm D7-P5510 product brief |
| D7-P5510 product brief proves exact resume checkpoint behavior after injected reset/power loss | rejected | unsupported | no fault-injection evidence in source |
| TP4022 proposal body was inspected | rejected | not done | official attribution only |

---

## Remaining evidence debt

This slice narrows rather than closes Case 148’s remaining work:

1. **TP001a genealogy:** obtain and directly inspect the proposal that introduced Device Self-test into NVMe 1.3.
2. **TP4022 drafting history:** directly inspect the ratified proposal body, not only the official change-log attribution and resulting normative text.
3. **Named-device fault injection:** on a specific firmware revision, start extended DST, capture log/progress, inject Controller Level Reset and full power loss separately, then verify resumed operation and result ordering.
4. **Subsystem / multi-controller conformance:** capture `DSTO`, start DST through controller A, then test start/abort visibility through controller B on a real multi-controller subsystem.
5. **Sanitize conflict test:** on hardware where safe and disposable, start DST, begin sanitize from the same or another controller, and verify current-state retirement plus result code `9h` without confusing “DST aborted” with “sanitize completed.”
6. **Result-history lifetime:** test newest-20 persistence across controller reset, subsystem reset, power cycle, firmware activation, format, and sanitize as distinct boundaries.
7. **Implementation embodiment:** look for controller/vendor technical material that reveals how extended-test resume state is persisted or reconstructed.

---

## Navigation outcome

Recommended canonical addition:

```text
NVMe 1.3 DSTO
    -> current self-test exclusion domain may be controller-local or subsystem-wide

NVMe 1.4 sanitize interaction
    -> sanitize start on any controller terminates in-progress DST across subsystem
    -> abort becomes bounded historical result code 9h

named commercial witness
    -> Intel D7-P5510 (NVMe 1.3c) publicly advertises Device Self-test
    != reset/power fault-injection proof
```

This evidence strengthens Case 148 without changing its maturity beyond `grounded`.

---

## Sources

1. NVM Express, **NVM Express Revision 1.3**, ratified 26-Apr-2017, dated 1-May-2017: <https://nvmexpress.org/wp-content/uploads/NVM_Express_Revision_1.3.pdf>.
2. NVM Express, **NVM Express Base Specification Revision 1.4c**, 9-Mar-2021: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4c-2021.06.28-Ratified.pdf>.
3. NVM Express, **Changes in NVMe Revision 1.4**, especially “Sanitize during Device Self-Test (mandatory)” and the TP4022 attribution: <https://nvmexpress.org/changes-in-nvme-revision-1-4/>.
4. NVM Express, **Specification Archives**, preserving Revision 1.4 and its ratified-TP archive: <https://nvmexpress.org/nvm-express-specification-archives/>.
5. Intel / Solidigm, **Intel SSD D7-P5510 Product Brief**, document 345311-001, `1220`: <https://www.solidigm.com/content/dam/solidigm/en/site/products/data-center/d7/p5510/documents/d7-p5510-series-product-brief.pdf>.

Retrieved / checked: 2026-09-15.
