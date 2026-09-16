# Case 82 Deepening — Samsung / ONFI / Hynix 2004–2010 Copyback Integrity Semantics

## Status

**`bounded deepening complete`** for one narrow question left open by Case 82:

> Did the relocation-without-automatic-ECC-requalification boundary documented by Micron appear only in Micron's mid-2000s notes, or can earlier / independent product and interface evidence show how NAND Copyback separated relocation, program completion, and integrity qualification?

This record adds three bounded layers:

1. a directly inspected Samsung named-product datasheet whose revision line begins in April 2004 and whose Copy-Back section explicitly warns that source-page charge-loss errors can be carried and accumulated;
2. ONFI 1.0 as an interface-standardization boundary for optional Copyback and its single-page-register handoff;
3. a Hynix 2010 product counterexample in which Copyback gains automatic in-device **error detection** without thereby becoming an automatic correction/requalification path.

It does **not** establish:

- invention priority for Samsung, Micron, Hynix, ONFI participants, or any patent family;
- that Samsung's implementation directly caused the ONFI command definition;
- that all pre-ONFI NAND vendors exposed identical command codes, restrictions, or integrity behavior;
- that ONFI 1.0 specifies a universal ECC policy for Copyback;
- that Hynix EDC corrects errors rather than detecting them;
- that later on-die-ECC NAND uses the same semantics;
- a complete Copyback command genealogy.

Case: [`../cases/82-micron-nand-copyback-ecc-requalification.md`](../cases/82-micron-nand-copyback-ecc-requalification.md)

The broader command-set and vendor genealogy still belongs primarily in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology). That repository was searched for a dedicated `copyback` slice before this deepening and none was found.

---

## 1. Why this slice matters

Case 82 already grounds a Micron mechanism:

```text
source NAND page
    -> internal page/cache register
    -> destination NAND page
```

and the corresponding integrity warning:

```text
successful physical relocation
    !=
automatic controller-side ECC correction
```

The historical boundary remained narrower than the mechanism deserved. Micron's TN-29-15 and TN-29-41 showed the issue clearly, but they did not answer whether the distinction was already visible in earlier named-product documentation or how a later interface standard framed Copyback.

The Samsung / ONFI / Hynix evidence changes that boundary without changing the central Case 82 claim.

---

## 2. Historical record — Samsung K9F1208X0B, 2004–2005

### H/P — document identity and revision floor

Samsung's `K9F1208B0B / K9F1208U0B / K9F1208R0B` datasheet is titled **64M x 8 Bit NAND Flash Memory**. The preserved Samsung revision-history page records:

- Rev. 0.0 — initial issue, **24 April 2004**;
- Rev. 0.1 — **11 October 2004**;
- Rev. 0.2 — **22 April 2005**;
- Rev. 0.3 — **6 May 2005**.

The Rev. 0.1 history also records that multi-plane operation and Copy-Back Program were not supported by the 1.8 V member of the family, while the feature list names `Intelligent Copy-Back` for the documented family.

**Evidence boundary:** the currently inspected Rev. 0.3 document directly contains the Copy-Back semantics below. The revision table proves the document family existed from April 2004, and that Copy-Back support was already explicit in the October 2004 revision history. It does not prove that every sentence in the Rev. 0.3 Copy-Back section was present verbatim in Rev. 0.0.

Primary manufacturer document preserved as a page-renderable PDF:

- Samsung Electronics, **K9F1208X0B 64M x 8 Bit NAND Flash Memory**, Rev. 0.3, 6 May 2005: <https://datasheet.octopart.com/K9F1208U0B-JIB0-Samsung-datasheet-11807018.pdf>.

The revision page and Copy-Back page were directly facsimile-inspected in this research pass.

### H/P — Copy-Back is explicitly an internal relocation path

Samsung's `Copy-Back Program` section describes a performance-oriented operation that rewrites one page to another page in the same plane without an external-memory round trip.

The documented sequence is structurally clear:

```text
source page
    -> normal page read
    -> internal page register
    -> destination address / Copy-Back data-input command
    -> program confirm
    -> destination page
```

The product therefore supplies a named pre-ONFI witness for the same basic retention handoff that later Micron notes discuss: a current page image can be re-embodied through device-internal temporary state instead of being emitted to the controller and loaded again.

Samsung also separates destination-program status from source-data integrity. Program failure is reported through the device's pass/fail status path.

### H/P — Samsung explicitly warns that source errors can survive relocation

The same Copy-Back section gives the retention-specific warning that matters here. Samsung distinguishes:

- a programming failure during the Copy-Back operation, which can be reported by status; from
- a source-page bit error caused by charge loss, which can follow repeated Copy-Back operations and accumulate.

Samsung consequently recommends two-bit ECC for the Copy-Back use case.

That product-level warning directly blocks a tempting equation:

```text
Copy-Back program reports success
    !=
source page was error-free
```

and more strongly:

```text
new physical embodiment created successfully
    !=
old correctable error population was removed
```

This is not a later project analogy projected into the device. The manufacturer itself distinguishes program-operation failure reporting from error accumulation in the copied information.

### H/P — Samsung's warning predates the Micron notes used by Case 82

The Samsung document family is earlier than Micron TN-29-15's 2007 bibliographic witness and TN-29-41's October 2008 publication.

The safe historical conclusion is chronological and semantic only:

> By 2004–2005, a Samsung named NAND product already documented internal Copy-Back and explicitly warned that charge-loss bit errors in the source could be propagated across repeated internal copies.

This does **not** establish that Samsung invented Copy-Back, that Micron learned the mechanism from Samsung, or that later ONFI wording descends from this specific Samsung product.

---

## 3. Historical record — ONFI 1.0 interface boundary

### H/P — ONFI 1.0 standardizes Copyback as an optional host-visible capability

The **Open NAND Flash Interface Specification Revision 1.0** defines `Copyback` as a page movement from one location to another location on the same LUN. The specification permits host read-out of the page after Copyback Read and host-side modification before Copyback Program.

It also states that Copyback uses a **single page register** for the read/program operation and allows implementation-specific restrictions such as odd/even-page constraints. The parameter-page feature bits expose whether Copyback is supported.

Primary specification:

- Open NAND Flash Interface Working Group, **Open NAND Flash Interface Specification, Revision 1.0**, §5.15 `Copyback Definition`: <https://onfi.org/files/onfi_1_0_gold.pdf>.

The official ONFI PDF is text-indexed by the public source, although direct rendering from the ONFI server was rejected during this research pass. The claims here are limited to the indexed normative Copyback definition and feature declaration rather than pretending that every section of the standard was facsimile-inspected.

### E — interface standardization does not collapse integrity policy into movement semantics

The inspected ONFI Copyback definition specifies:

- where the data moves;
- the temporary page-register relation;
- host opportunities to read or modify data;
- addressing/restriction behavior;
- capability discovery.

That is enough to standardize a movement interface. It is not, by itself, evidence that every conforming device must automatically correct the page before programming the destination.

A careful formulation is therefore:

```text
standardized Copyback capability
    !=
standardized automatic integrity requalification
```

This is an **engineering reconstruction from the inspected clause scope**, not a claim that the entire ONFI 1.0 specification contains no ECC language anywhere.

### E — an available host-read opportunity is not the same thing as a required correction checkpoint

ONFI explicitly permits the host to read the temporary page data and to modify it before programming. That exposes a place where higher layers *can* inspect or transform the representation.

But the existence of that opportunity does not make the opportunity mandatory in every Copyback execution.

Thus:

```text
host may observe / modify temporary page state
    !=
host necessarily requalifies every Copyback
```

This helps explain why a command can be useful for high-speed relocation while still requiring a separate integrity policy.

---

## 4. Historical record — Hynix H27U2G8F2C, 2010

### H/P — later Copyback can include automatic in-device error detection

Hynix's 2-Gbit NAND documentation for `H27U2G8F2C` describes a Copyback path that uses an internal buffer and does not require normal external data transfer.

The product also adds an **automatic Error Detection Code (EDC) check** during Copyback. The EDC result can be queried through the device's EDC-status path, and the datasheet describes the detection capability in page subdivisions.

Manufacturer document preserved as page-indexed HTML:

- Hynix Semiconductor, **H27U2G8F2C 2 Gbit NAND Flash**, Rev. 0.0, April 2010, Copyback / EDC sections: <https://www.alldatasheet.com/html-pdf/2079229/HYNIX/H27U2G8F2C/3121/17/H27U2G8F2C.html> and <https://www.alldatasheet.com/html-pdf/2079229/HYNIX/H27U2G8F2C/3305/18/H27U2G8F2C.html>.

### H/P/E — detection is not correction

This Hynix witness is valuable precisely because it is a counterexample to an over-broad reading of the original Micron case.

It would be wrong to generalize:

```text
internal Copyback
    -> no integrity machinery inside the NAND device
```

Hynix demonstrates an internal Copyback path with automatic error **detection**.

But the source does not justify silently upgrading detection into correction. An EDC indication can tell the controller that the moved source representation is suspect; it does not by itself prove that the destination receives a corrected logical value.

Therefore the stronger decomposition is:

```text
internal movement
    != error visibility
    != error correction
    != renewed integrity margin
```

### H/P — the Hynix product also exposes a distinct special-read response

The same device family documents a special read-for-copyback path intended for cases in which ordinary read/ECC behavior indicates a problem. This is useful evidence that copyback reliability can be composed from several internal and external response paths rather than one universal primitive.

This record does not attempt to reconstruct that later vendor-specific read-threshold mechanism in detail; adaptive-read / retry-read behavior is already treated separately in Case 85.

---

## 5. Revised historical boundary for Case 82

The cross-vendor sequence can now be stated conservatively as:

```text
Samsung named product, 2004–2005
    internal Copy-Back already documented
    source charge-loss errors can be propagated
    program pass/fail does not remove that problem

ONFI 1.0, 2006–2007 publication boundary
    Copyback becomes an optional standardized interface capability
    one page-register handoff is defined
    host read/modify opportunity is exposed

Micron, 2007–2008 and later
    integrity consequence is explicitly framed around skipped external ECC
    periodic / explicit requalification is recommended

Hynix, 2010
    internal Copyback may add automatic EDC
    detection still does not equal correction
```

The exact standards-publication date and committee genealogy are not needed for the retention argument. The important historical change is from vendor-specific named-product behavior to an interoperable command/interface vocabulary, followed by vendor-specific integrity machinery layered around that interface.

---

## 6. Retained-state decomposition

This deepening adds three distinctions to the original Case 82 state model.

### 6.1 Program-completion state

The device can retain/report whether the destination program operation completed successfully according to its status machinery.

This is not the same relation as source-content correctness.

### 6.2 Error-observation state

A later device may expose evidence that an error was detected during the internal move.

That evidence is itself useful control state, but it is not the intended payload and not automatically a corrected payload.

### 6.3 Interface-capability state

ONFI parameter information can state that a device supports Copyback and related restrictions/capabilities.

This is retained descriptive/control state about what operations are admissible. It does not certify the integrity of the particular page currently being moved.

The resulting model is:

```text
logical payload
    != raw source-page image
    != temporary page-register image
    != destination program-completion status
    != error-detection evidence
    != ECC correction / remaining margin
    != higher-level current-location mapping
```

---

## 7. Engineering reconstruction

### E — relocation success and information correctness are different predicates

Samsung's own separation of program failure from accumulated source bit errors makes this especially strong. The destination cell programming can satisfy its operation-status contract while the representation being programmed already includes a correctable error inherited from the source.

### E — the same command family can support different integrity envelopes

Samsung, Micron, ONFI, and Hynix do not justify one timeless universal implementation of Copyback.

A more defensible abstraction is:

```text
Copyback movement contract
    + vendor/device-specific integrity machinery
    + controller policy
    -> actual preservation behavior
```

The command name therefore does not uniquely determine the integrity semantics.

### E — detection can preserve future repair opportunity without performing repair

If the internal path detects an error and reports that fact, the system may still have time to choose a safer external read/correct/program path, retire a page, or invoke another recovery action.

That is preservation-relevant because retained **evidence of suspect state** can alter future admissibility. It remains distinct from having already repaired the payload.

### E — standardization can stabilize a handoff boundary while leaving policy open

ONFI's page-register and Copyback command semantics make the handoff interoperable at the interface level. Yet the standardization of an operation does not mean every controller uses it with the same checking interval, ECC strength, retry policy, or retirement threshold.

This reinforces a repository-wide rule:

> interface semantics and maintenance policy are different retained relations.

---

## 8. Functional comparisons — not genealogy

### A — Case 36, NAND Correct-and-Refresh

Case 36 uses a read / correction / rewrite path to renew recoverability before the error population exceeds the available ECC budget.

Case 82 now has an even stronger counterexample family:

```text
Copyback relocation
    may preserve the page image
    may expose error status
    yet still need a separate correction/rewrite boundary
```

So `copyback != correct-and-refresh` remains valid even when the copyback implementation contains some integrity checking.

### A — Case 59, NAND program interference

Samsung's copyback warning concerns already-present charge-loss errors being carried through relocation. Case 59 concerns write-induced disturbance/interference around programming.

The two can coexist, but they are not the same mechanism.

### A — Case 85, adaptive read / retry

Hynix's special read-for-copyback path shows why reader-side recovery behavior and movement policy can become coupled. Case 85 remains the better home for read-threshold/retry genealogy; Case 82 uses the Hynix witness only to show that relocation may call on additional error-observation/recovery machinery.

### A — Case 04, mapped Flash

Case 04 asks which physical embodiment currently counts for a logical address. Case 82 continues to show that **location currentness and integrity qualification can diverge**: a higher layer can correctly point to the new page while the page still carries inherited error debt or unresolved detection state.

---

## 9. Prior-art and genealogy boundary

This deepening changes the novelty boundary of the case but does not create an invention claim.

The defensible statement is now:

> Samsung named-product documentation from the 2004–2005 period already shows internal Copy-Back plus an explicit warning that source-page charge-loss errors can accumulate across repeated moves. ONFI 1.0 later standardizes optional Copyback as an interface-level page-register handoff. Micron's later notes make the skipped-controller-ECC consequence and requalification policy unusually explicit, while Hynix 2010 demonstrates that an internal copyback path can add automatic error detection without thereby collapsing detection into correction.

Not established:

- the first NAND product ever to implement Copyback;
- the first use of the word `Copyback`;
- direct Samsung → ONFI → Micron → Hynix technical descent;
- identical internal buffer architecture across products;
- identical ECC/EDC algorithms;
- the complete ONFI ballot / vendor-contribution history.

Those are broader technical-history questions and should be routed to `computing-archaeology` if pursued.

---

## 10. Claim ledger

| Claim | Type | Evidence status |
| --- | --- | --- |
| Samsung K9F1208X0B documentation has a revision lineage beginning 24 Apr 2004 | H/P | strong manufacturer-primary revision table, directly inspected |
| the Samsung family documents internal same-plane Copy-Back through page registers | H/P | strong manufacturer-primary, directly inspected |
| Samsung separates program pass/fail from source charge-loss bit-error accumulation | H/P | strong manufacturer-primary, directly inspected |
| Samsung recommends stronger ECC for Copy-Back use | H/P | strong manufacturer-primary, directly inspected |
| Samsung is proven to have invented NAND Copyback | X | not established |
| ONFI 1.0 defines optional Copyback using one page register and permits host read/modify participation | H/P | primary standard text, indexed from official ONFI source |
| ONFI Copyback support implies automatic ECC correction | X | not established by inspected clause |
| interface standardization != integrity-policy standardization | E | bounded reconstruction |
| Hynix 2010 Copyback includes automatic EDC/error detection | H/P | manufacturer document preserved in page-indexed archive |
| Hynix EDC proves automatic correction | X | explicitly not claimed |
| internal movement != error visibility != correction != renewed error margin | E | bounded reconstruction from the cross-vendor evidence |
| Copyback movement semantics can remain stable while integrity machinery varies | E/A | bounded functional comparison, not genealogy |
| program completion != content requalification | E | direct reconstruction, especially strong in Samsung witness |

---

## 11. Source notes

### Primary — Samsung

- Samsung Electronics, **K9F1208B0B / K9F1208U0B / K9F1208R0B, 64M x 8 Bit NAND Flash Memory**, Rev. 0.3, 6 May 2005. Preserved PDF: <https://datasheet.octopart.com/K9F1208U0B-JIB0-Samsung-datasheet-11807018.pdf>.
  - revision history: document p. 1 / PDF page 1;
  - `Intelligent Copy-Back` feature: document p. 2;
  - `Copy-Back Program`: document p. 37 / PDF page index 36;
  - source-error accumulation and two-bit-ECC recommendation are on that Copy-Back page.

### Primary — ONFI

- Open NAND Flash Interface Working Group, **Open NAND Flash Interface Specification, Revision 1.0**, §5.15 `Copyback Definition`: <https://onfi.org/files/onfi_1_0_gold.pdf>.
  - direct server rendering was unavailable in this pass;
  - the official document remains text-indexed and exposes the Copyback clause used here.

### Primary — Hynix

- Hynix Semiconductor, **H27U2G8F2C 2 Gbit NAND Flash**, Rev. 0.0, April 2010.
  - Copyback / automatic EDC page: <https://www.alldatasheet.com/html-pdf/2079229/HYNIX/H27U2G8F2C/3121/17/H27U2G8F2C.html>;
  - EDC behavior page: <https://www.alldatasheet.com/html-pdf/2079229/HYNIX/H27U2G8F2C/3305/18/H27U2G8F2C.html>.

### Source-strength caution

Samsung is the strongest source in this slice because the complete manufacturer PDF was directly rendered and the relevant page was facsimile-inspected. ONFI is a primary normative source but only the indexed official text was recoverable from the current environment. Hynix is manufacturer-primary text preserved by a datasheet archive rather than a current SK hynix-hosted download.

The evidence labels above preserve those differences instead of treating every web copy as equally strong.

---

## 12. Bounded conclusion

The cross-vendor record sharpens Case 82 in two directions at once.

First, it pushes the documented integrity problem earlier than the Micron notes: a Samsung product family in the 2004–2005 record already distinguishes successful internal Copy-Back programming from charge-loss errors that can ride along with the copied page.

Second, it prevents the opposite over-generalization. Later Copyback need not be an integrity-blind internal path: Hynix shows that in-device error detection can be added. Yet **detection, correction, and renewed integrity margin remain separate states**.

The most defensible retention relation is therefore:

```text
physical relocation
    != operation success
    != error observation
    != correction
    != renewed recoverability margin
```

and, historically:

```text
vendor Copy-Back behavior
    -> standardized movement interface
    -> vendor-specific integrity machinery
```

is a useful chronology, **not** a demonstrated genealogy.