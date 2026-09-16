# Micron NAND Internal Data Move / COPYBACK: Relocation Without Automatic ECC Requalification

## Scope

- **Bounded historical/technical regime:** Micron raw-NAND documentation from the mid-2000s through the mid-2010s, centered on TN-29-15 (`Internal Data Move`) and TN-29-41 (`COPYBACK`), with a later Micron product datasheet as a named-device continuity witness.
- **Cross-vendor/prior-art deepening:** Samsung named-product evidence from 2004–2005, ONFI 1.0 interface semantics, and a Hynix 2010 automatic-EDC counterexample now bound the earlier/later edges without turning this case into a complete NAND command genealogy.
- **Primary question:** when NAND data is moved internally from one physical page to another without crossing the ordinary external controller path, what exactly is preserved, what integrity work is skipped, and which kinds of error evidence may still be produced?
- **Retention-specific focus:** page-register-mediated relocation, error carry-forward, ECC requalification opportunities, verification, operation-completion evidence, error-detection evidence, and the difference between preserving a logical page image and renewing its error margin.
- **Excluded from this case:** a general history of NAND commands, a full FTL/garbage-collection history, wear-leveling algorithms, read-disturb physics, program-interference physics, invention priority for copyback, or a survey of modern on-die-ECC copyback implementations.

This slice is deliberately adjacent to Cases 04, 36, 52, 59, 67, 78, and 85. Those cases already cover mapped-Flash identity, correct-and-refresh, read disturb, program interference, adaptive reclaim, bad-block retirement, and adaptive read/retry. Case 82 asks a narrower question: **does moving a current NAND page to a new physical embodiment necessarily renew the correctness of the information being moved?** In the bounded evidence, the answer is no.

### Evidence navigation

- original Micron grounding is summarized in this canonical case;
- cross-vendor/prior-art deepening: [`../evidence/82-samsung-onfi-hynix-2004-2010-copyback-integrity-deepening.md`](../evidence/82-samsung-onfi-hynix-2004-2010-copyback-integrity-deepening.md).

---

## Historical vocabulary

The primary sources use terms including:

- `internal data move` / `IDM`;
- `READ FOR INTERNAL DATA MOVE`;
- `PROGRAM FOR INTERNAL DATA MOVE`;
- `COPYBACK` / `Copy-Back` / `COPYBACK READ` / `COPYBACK PROGRAM`;
- `cache register` / `page register`;
- `error correction` / `ECC`;
- `Error Detection Code` / `EDC` in the later Hynix witness;
- `post-READ`;
- `data integrity`;
- `block management`;
- `wear leveling`.

The following are **project engineering terms**, not historical quotations from the manufacturers or ONFI:

- `integrity requalification`;
- `error-debt carry-forward`;
- `relocation-without-renewal`;
- `validation opportunity`;
- `physical re-embodiment`;
- `error-observation state`.

They are used only to compare documented mechanisms.

---

## Historical record

### H/P — traditional external movement and Micron IDM are explicitly different paths

Micron TN-29-15 describes ordinary NAND block-management movement as an external sequence: a page is read from the device, post-processed for error correction, and then programmed into a new erased location. The note introduces `internal data move (IDM)` as a performance alternative that avoids those external data transfers.

The documented IDM path is a two-stage device-internal operation:

```text
source NAND page
    -> READ FOR INTERNAL DATA MOVE (00h–35h)
    -> cache register
    -> PROGRAM FOR INTERNAL DATA MOVE (85h–10h)
    -> destination NAND page
```

The point of the feature is not that the logical value changes. It is that the same page image can be re-embodied elsewhere without sending the data over the external bus and through the controller's ordinary read/correct/write path.

**Primary source:** Micron Technology, *TN-29-15: NAND Flash Performance Improvement Using Internal Data Move* / *NAND Flash Internal Data Move*, historical Micron technical note. A text-preserving mirror of Rev. C is available at <https://doczz.net/doc/7838214/tn-29-15--nand-flash-performance-improvement-using-internal>. Contemporary bibliographic records cite Micron's historical publication path as <http://download.micron.com/pdf/technotes/nand/tn2915.pdf>.

### H/P — the Micron internal path removes the ordinary controller-side ECC opportunity

TN-29-15 makes the integrity consequence explicit. Because the data move remains internal, there is no ordinary external-controller opportunity to correct the moved page. The note warns that excessive internal data moves without periodic checks can allow errors to accumulate and reduce reliability.

Its worked error scenario is important: an already-erroneous bit can follow the page into the cache register and then into the destination page. A later independent error can push the page beyond the correction capability available when it is finally read.

The historical mechanism therefore supports a strict distinction:

> moving the page image successfully is not the same operation as restoring the page image to the intended error-free value.

### H/P — Micron recommends explicit integrity checks around repeated IDM

TN-29-15 recommends system-level techniques that bound the risk, including robust multibit ECC and periodic `post-READ` integrity checks. The checking interval depends on required correction capability and the number of internal moves.

This converts a performance optimization into a retention-policy problem: bus/computation work can be avoided, but doing so changes how long a system may safely defer an integrity-requalification opportunity.

### H/P — TN-29-41 reframes the same issue under `COPYBACK` vocabulary

Micron's October 2008 TN-29-41, *Using COPYBACK Operations to Maintain Data Integrity in NAND Flash Devices*, again warns that COPYBACK without external data output/input can allow error counts to move beyond ECC protection limits.

The note's corrective relation is the opposite path: outputting the data, correcting it, and returning the corrected representation can restore the programmed value and renew usable correction margin. The external path is therefore not merely slower transport; in the bounded design it can be an **integrity-renewal boundary**.

**Primary source:** Micron Technology, *TN-29-41: Using COPYBACK Operations to Maintain Data Integrity in NAND Flash Devices*, October 2008. Historical Micron path: <http://download.micron.com/pdf/technotes/nand/tn2941_idm_copyback.pdf>. A later Micron media path is preserved in USPTO/PTAB filings: <https://media-www.micron.com/-/media/client/global/documents/products/technical-note/nand-flash/tn2941_idm_copyback.pdf?rev=c0a04e8ff8bd4f309bab7ea91ad98035>.

### H/P — later Micron product documentation keeps command success and content qualification separate

A 2015 Micron automotive asynchronous-NAND datasheet documents `COPYBACK READ (00h-35h)` and `COPYBACK PROGRAM (85h-10h)` as page-register-mediated movement. Although ordinary host read-out is not required for the move, the host is advised to read and verify before COPYBACK PROGRAM when it must avoid propagating data errors.

The product also exposes programming status. These answer different questions:

1. did the NAND programming operation complete successfully according to the device status path?
2. was the page content independently requalified/corrected before being propagated?

A command can answer the first without answering the second.

**Primary product witness:** Micron, *8Gb Automotive Async NAND Flash Memory*, Rev. B, March 2015, `Copyback Operations` / `COPYBACK READ`, mirrored at <https://device.report/m/33bc71a4eab1c479cec619ad15d5184198e06218324e8d8d2cb32dd8ab75a8d3>.

### H/P — Samsung 2004–2005 named-product evidence pushes the documented integrity warning earlier

Samsung's `K9F1208B0B / K9F1208U0B / K9F1208R0B` manufacturer datasheet has a revision lineage beginning with an initial issue on **24 April 2004**; Rev. 0.1 is dated 11 October 2004, Rev. 0.2 22 April 2005, and the directly inspected Rev. 0.3 6 May 2005. The feature list names `Intelligent Copy-Back`.

Its `Copy-Back Program` section describes a same-plane internal relocation through page registers, eliminating the ordinary external read/reload round trip. It then makes a stronger integrity distinction: destination program failure can be reported by the pass/fail status mechanism, while a source-page bit error caused by charge loss can be carried across repeated Copy-Back operations and accumulate. Samsung consequently recommends two-bit ECC for the use case.

This gives Case 82 an earlier named-product witness for:

```text
program-operation success
    !=
source-content correctness
```

and:

```text
physical relocation
    !=
automatic removal of inherited correctable errors
```

**Evidence boundary:** the inspected Rev. 0.3 contains the full warning. The revision table shows that the product-document family existed from April 2004 and that Copy-Back support was already part of the October 2004 revision history, but it does not prove that every sentence in Rev. 0.3 was already present in Rev. 0.0.

**Primary source:** Samsung Electronics, *K9F1208X0B 64M x 8 Bit NAND Flash Memory*, Rev. 0.3, 6 May 2005: <https://datasheet.octopart.com/K9F1208U0B-JIB0-Samsung-datasheet-11807018.pdf>.

### H/P — ONFI 1.0 standardizes the Copyback handoff without thereby standardizing one integrity policy

The *Open NAND Flash Interface Specification Revision 1.0* defines Copyback as moving a page from one location to another on the same LUN. Its Copyback definition uses a **single page register** for the read/program operation, permits the host to read the temporary data and modify it before Copyback Program, and allows device restrictions such as odd/even-page constraints. Capability information indicates whether Copyback is supported.

This is an interface-standardization boundary: the movement primitive and temporary-state handoff become standardized vocabulary. The inspected Copyback clause does not itself justify the stronger claim that every conforming Copyback automatically corrects page errors before programming the destination.

Thus the safe reconstruction is:

```text
standardized Copyback movement semantics
    !=
standardized automatic integrity-requalification policy
```

**Primary standard:** Open NAND Flash Interface Working Group, *Open NAND Flash Interface Specification, Revision 1.0*, §5.15 `Copyback Definition`: <https://onfi.org/files/onfi_1_0_gold.pdf>.

The official ONFI source was text-indexed but not directly renderable in the current research environment; claims here are limited to the indexed normative Copyback clause rather than pretending that the whole standard was facsimile-inspected.

### H/P — Hynix 2010 supplies an automatic-error-detection counterexample

Hynix's `H27U2G8F2C` 2-Gbit NAND documentation describes Copyback through an internal buffer and adds an automatic **Error Detection Code (EDC)** check. The EDC result can be queried through a device status path.

This is important because it blocks an over-broad interpretation of Micron:

```text
internal Copyback
    -> no integrity machinery inside the NAND device
```

is false as a universal statement.

But Hynix's documented EDC is error **detection**. The source does not justify silently promoting detection into correction or into renewed ECC margin. The stronger decomposition is:

```text
internal movement
    != error visibility
    != error correction
    != renewed integrity margin
```

The product family also documents a special read-for-copyback response path. That later read-recovery machinery is not reconstructed here; Case 85 remains the better home for adaptive-read/retry genealogy.

**Primary manufacturer document preserved in page-indexed form:** Hynix Semiconductor, *H27U2G8F2C 2 Gbit NAND Flash*, Rev. 0.0, April 2010: <https://www.alldatasheet.com/html-pdf/2079229/HYNIX/H27U2G8F2C/3121/17/H27U2G8F2C.html> and <https://www.alldatasheet.com/html-pdf/2079229/HYNIX/H27U2G8F2C/3305/18/H27U2G8F2C.html>.

---

## Retained state

At least seven distinct states or relations matter in this bounded case.

### 1. Logical payload

The value the storage system intends to preserve across physical relocation.

### 2. Raw physical page image

The bits recovered from the source NAND page before higher-level correction. In the bounded internal-move paths, already-present errors can travel with this image.

### 3. Temporary page/cache-register state

The source page is temporarily embodied in an internal register between read-for-move and program-for-move phases. This state is neither the long-term source embodiment nor yet the durable destination embodiment.

### 4. Program-completion state

The device can report whether the destination programming operation completed successfully according to its program/status machinery. Samsung's warning is especially useful because it shows this predicate can be true while inherited source errors remain a distinct concern.

### 5. Error-observation state

A device may expose evidence that an error was detected during the move, as in the Hynix EDC path. This is useful retained control evidence, but it is not the payload and is not automatically a corrected payload.

### 6. ECC / integrity relation

The system's ability to identify and correct a bounded error population. The project term `error budget` means remaining correctable margin under a bounded code/error model; it does not mean that an ECC code is physically consumed like a battery.

### 7. Relocation / mapping state

At a higher layer, the system must know which physical page now embodies the current logical data after block management, wear leveling, reclamation, or replacement. Case 82 does not reconstruct a full FTL; it only notes that physical movement is useful to a logical store because some higher-level relation later resolves to the destination.

---

## Read, move, verify, detect, and rewrite semantics

### Ordinary external read/correct/reprogram path

The controller obtains the page through the external interface, applies its ECC/error-processing path, and can program a corrected representation into the destination.

This path couples **movement** with an opportunity for **requalification and correction**.

### Internal data move / COPYBACK path

The NAND device reads the source page into an internal register and programs that register into a destination page without requiring the ordinary external data round trip.

This couples **movement** with **bus avoidance**, but does not by itself prove that inherited page errors have been corrected.

### Optional host read/modify path

ONFI 1.0 allows the host to read the temporary Copyback data and to modify data before Copyback Program. That is an available observation/transformation point, not proof that every Copyback execution uses it as an integrity checkpoint.

### Error-detection path

A later device may attach error-detection machinery to the internal movement path. Hynix shows that the internal path need not be integrity-blind; yet detection remains distinct from payload correction.

### Post-READ / explicit output path

Micron recommends periodic or pre-program read-out/checking when integrity risk requires it. This introduces a separate maintenance operation whose schedule can depend on accumulated internal moves and the correction budget.

### Program status / completion

Destination program status is evidence about the programming operation's completion/pass-fail condition. It is not a substitute for end-to-end proof that the page was first restored to its intended error-free logical value.

---

## Engineering reconstruction

### E — relocation and renewal are separate retention operations

A page can move from one physical NAND location to another while preserving its current raw image, including already-present correctable errors. Physical re-embodiment therefore does not entail integrity renewal.

### E — operation success and information correctness are different predicates

Samsung's product documentation makes this unusually concrete: Copy-Back program failure is visible through status, while source charge-loss errors may still be propagated across successful copies.

Therefore:

```text
operation completed successfully
    !=
representation was requalified as error-free
```

### E — a performance optimization can remove a preservation opportunity

The speed/power advantage of IDM/COPYBACK partly comes from avoiding an external data path. Where controller-side ECC correction lives on that path, removing transport work can also remove a corrective checkpoint.

### E — error visibility and error correction must remain separate

Hynix adds automatic EDC to a Copyback path. That can preserve evidence that a page is suspect and allow future policy to choose another recovery action. It does not, without further evidence, prove that the page was corrected.

So:

```text
error detected
    !=
error repaired
```

### E — the same command family can have different integrity envelopes

The cross-vendor evidence supports this bounded model:

```text
Copyback movement contract
    + vendor/device-specific integrity machinery
    + controller policy
    -> actual preservation behavior
```

The command name alone does not uniquely determine the integrity semantics.

### E — error margin can be a consumable continuation resource

A page can remain logically recoverable while already containing errors within ECC capability. Carrying those errors forward need not cause immediate data loss, but it leaves less correction margin for later retention errors, read disturb, program interference, or other faults.

### E — temporary internal state is part of a retention handoff

During COPYBACK/IDM, a page register holds the representation between old and new NAND embodiments. Successful persistence across the move requires the handoff to progress from source array state, through temporary register state, to a programmed destination. The register is retention infrastructure even though it is not the intended long-term home.

### E — correctness authority and location authority can diverge

A higher-level mapping layer may correctly designate the newly programmed page as current while the page image still carries correctable errors or unresolved error-detection evidence. `where the current page is` and `how much integrity confidence/margin the current page has` are separate relations.

### E — interface standardization and maintenance policy are different layers

ONFI can standardize Copyback command/interface semantics without forcing every controller to use the same checking interval, ECC strength, retry policy, retirement threshold, or physical implementation.

---

## Functional comparisons — not genealogy

### A — Case 04, mapped Flash

Case 04 grounds stable logical identity across out-of-place Flash relocation and reclamation. Case 82 adds a lower-level warning: **a successful location transition does not by itself requalify the information moved**. Mapping currentness and payload-integrity currentness are different relations.

### A — Case 36, NAND Flash Correct-and-Refresh

Case 36 explicitly uses read + ECC correction + rewrite/remap to renew aging NAND before errors exceed correction capacity. Case 82 provides the counterexample path: internal movement can relocate the page while skipping correction, or can add detection without proving correction.

Therefore:

> `relocation ≠ refresh`, `detection ≠ correction`, and `copyback ≠ correct-and-refresh`.

### A — Cases 52, 59, and 67

Read disturb and program interference can create or enlarge physical error populations; adaptive reclaim can move data after reliability evidence crosses a policy threshold. Case 82 does not claim COPYBACK causes those mechanisms. It shows instead that whatever correctable error population already exists can be propagated if movement does not correct it first.

### A — Case 78, bad-block replacement

Case 78 shows that failure-triggered retirement can require moving current payload to a reserve block while retaining the exclusion/replacement relation. Case 82 adds an orthogonal audit question: was the page merely copied, merely checked, or actually corrected before the destination became current?

### A — Case 85, adaptive read / retry

Hynix's special read-for-copyback behavior shows that movement can be coupled to reader-side recovery. Case 85 remains the proper home for read-threshold/retry history; the comparison here is functional only.

---

## Philosophical interpretation — bounded

### I — migration can preserve error debt as well as value

A common abstract description of technical preservation says that a value survives because it is repeatedly moved to new carriers. Case 82 makes that statement more exact: **migration can preserve the intended logical value while also carrying forward imperfections that reduce future recoverability.** Re-embodiment is not automatically rejuvenation.

The cross-vendor deepening adds a second qualification: a system may preserve **evidence that the migrated state is suspect** without yet repairing it. Retaining diagnostic evidence can preserve a future repair opportunity, but diagnosis is not identical to recovery.

These are project interpretations, not historical claims that Samsung, Micron, ONFI, or Hynix used the philosophical vocabulary of `error debt`, `rejuvenation`, or `repair opportunity`.

---

## Counterexamples and limits

- The case does not establish who invented NAND copyback/internal data move.
- Samsung's 2004–2005 chronology is a named-product/document witness, not an invention-priority proof.
- Chronological ordering Samsung → ONFI → Micron → Hynix is not evidence of direct technical descent or technology transfer.
- `IDM`, `Copy-Back`, and `COPYBACK` are historical product/interface terms with overlapping bounded functions; the case does not claim that every vendor used identical command codes, restrictions, or internal circuitry.
- ONFI's inspected Copyback clause establishes movement/interface semantics. It does not justify a universal claim about every ECC mechanism elsewhere in the specification or in every conforming device.
- The exact source/destination plane, odd/even, die, or LUN restrictions vary by device generation; they are not generalized into one universal NAND geometry.
- Hynix automatic EDC is evidence of detection, not proof of automatic correction.
- The case does not claim every later NAND lacks internal ECC. Modern managed or on-die-ECC devices may compose copyback with different integrity machinery.
- An internal move carrying a correctable source error does not imply immediate user-visible corruption. Failure occurs when the relevant error population exceeds the available correction/recovery path.
- Program-status success is not described as worthless; it answers a different operational question from end-to-end content requalification.
- The case does not prove that every garbage-collection or wear-leveling implementation uses NAND-native COPYBACK. Controllers can use external read/correct/program paths or other internal primitives.
- A later physical rewrite can change charge distributions and therefore physical condition, but that does not erase the distinction between copying an already-wrong logical bit pattern and correcting it before rewrite.
- Secure sanitization is outside scope. Moving or rewriting a current page says nothing by itself about physical erasure of the obsolete source embodiment.

---

## Prior-art boundary

This case makes **no invention-priority claim** for internal NAND page movement, copyback commands, page registers, or ECC-aware relocation.

The defensible historical statement is now narrower and stronger:

> Samsung named-product documentation in the 2004–2005 record already documents internal Copy-Back and explicitly warns that charge-loss errors in a source page can propagate and accumulate across repeated copies even when destination-program status is separately available. ONFI 1.0 later standardizes Copyback as an optional interface-level page-register handoff. Micron's 2007–2008 documentation makes the skipped-controller-ECC consequence and explicit requalification policy especially clear, while Hynix 2010 shows that an internal Copyback path can add automatic error detection without thereby collapsing detection into correction.

This changes the Case 82 novelty boundary in two ways:

1. the integrity problem is no longer presented as a Micron-local discovery from the late 2000s;
2. the Micron path is not generalized into a timeless claim that all internal Copyback lacks device-side integrity machinery.

The companion `tmzncty/computing-archaeology` repository was searched again for a dedicated NAND copyback/internal-data-move slice and none was found. A complete vendor / patent / ONFI-ballot genealogy belongs there rather than being recreated here.

---

## Claim ledger

| Claim | Type | Evidence status |
| --- | --- | --- |
| Micron documents an internal page-move path through an internal register | H/P | grounded in TN-29-15 and later product documentation |
| the documented Micron internal path avoids ordinary external data transfer | H/P | grounded |
| the ordinary external movement path can include error correction before reprogramming | H/P | grounded in TN-29-15 |
| Micron warns that IDM/COPYBACK without external checking can propagate/accumulate errors | H/P | grounded in TN-29-15, TN-29-41, and later product documentation |
| Micron recommends ECC plus periodic/post-read or pre-copyback verification according to integrity needs | H/P | grounded |
| Samsung K9F1208X0B documentation has a revision lineage beginning 24 Apr 2004 | H/P | manufacturer-primary revision table, directly inspected |
| Samsung documents same-plane internal Copy-Back through page registers | H/P | manufacturer-primary, directly inspected |
| Samsung separates program pass/fail from source charge-loss error accumulation | H/P | manufacturer-primary, directly inspected |
| Samsung recommends stronger ECC for the bounded Copy-Back use | H/P | manufacturer-primary, directly inspected |
| Samsung invented NAND Copyback | X | not established |
| ONFI 1.0 defines Copyback with one page register and host read/modify opportunities | H/P | primary standard text, indexed from official source |
| ONFI Copyback support implies automatic ECC correction | X | not established by the inspected clause |
| Hynix 2010 Copyback exposes automatic EDC/error detection | H/P | manufacturer document preserved in page-indexed archive |
| Hynix EDC proves automatic correction | X | explicitly not claimed |
| physical relocation ≠ integrity requalification | E | direct reconstruction from the documented paths |
| operation completion ≠ source-content correctness | E | especially strong in Samsung witness |
| error visibility ≠ error correction | E | bounded Hynix reconstruction |
| interface standardization ≠ integrity-policy standardization | E | bounded ONFI reconstruction |
| mapping/location currentness ≠ integrity margin | E | bounded cross-layer reconstruction |
| correctable error presence ≠ immediate logical failure | E | bounded by the ECC model described in the sources |
| COPYBACK ≠ Correct-and-Refresh | E/A | functional comparison with Case 36; no genealogy claim |
| COPYBACK ≠ read-disturb/program-interference mechanism | E/A | functional boundary with Cases 52/59 |
| internal relocation can participate in block management/wear leveling without being identical to either policy | H/E | bounded by manufacturer use framing |
| migration can carry forward reduced recovery margin as well as logical value | I/E | bounded interpretation |
| retaining error evidence can preserve a later repair opportunity without performing repair | I/E | bounded interpretation from Hynix counterexample |

---

## Sources

### Primary / manufacturer — Micron

- Micron Technology, **TN-29-15: NAND Flash Performance Improvement Using Internal Data Move / NAND Flash Internal Data Move**, historical note, Rev. C text mirror: <https://doczz.net/doc/7838214/tn-29-15--nand-flash-performance-improvement-using-internal>.
- Micron Technology, **TN-29-41: Using COPYBACK Operations to Maintain Data Integrity in NAND Flash Devices**, October 2008. Historical publication URL: <http://download.micron.com/pdf/technotes/nand/tn2941_idm_copyback.pdf>; later Micron media URL preserved in PTAB filings: <https://media-www.micron.com/-/media/client/global/documents/products/technical-note/nand-flash/tn2941_idm_copyback.pdf?rev=c0a04e8ff8bd4f309bab7ea91ad98035>.
- Micron Technology, **8Gb Automotive Async NAND Flash Memory**, Rev. B, March 2015, `Copyback Operations`: <https://device.report/m/33bc71a4eab1c479cec619ad15d5184198e06218324e8d8d2cb32dd8ab75a8d3>.

### Primary / manufacturer — Samsung

- Samsung Electronics, **K9F1208B0B / K9F1208U0B / K9F1208R0B, 64M x 8 Bit NAND Flash Memory**, Rev. 0.3, 6 May 2005: <https://datasheet.octopart.com/K9F1208U0B-JIB0-Samsung-datasheet-11807018.pdf>.
  - revision history: document p. 1;
  - `Intelligent Copy-Back` feature: document p. 2;
  - `Copy-Back Program` and accumulated-source-error warning: document p. 37.

### Primary / standard — ONFI

- Open NAND Flash Interface Working Group, **Open NAND Flash Interface Specification, Revision 1.0**, §5.15 `Copyback Definition`: <https://onfi.org/files/onfi_1_0_gold.pdf>.

### Primary / manufacturer — Hynix

- Hynix Semiconductor, **H27U2G8F2C 2 Gbit NAND Flash**, Rev. 0.0, April 2010, Copyback / EDC sections: <https://www.alldatasheet.com/html-pdf/2079229/HYNIX/H27U2G8F2C/3121/17/H27U2G8F2C.html> and <https://www.alldatasheet.com/html-pdf/2079229/HYNIX/H27U2G8F2C/3305/18/H27U2G8F2C.html>.

### Archival / bibliographic witnesses

- USPTO/PTAB-filed exhibit text indexing TN-29-41 and its Micron URL: <https://ptacts.uspto.gov/ptacts/public-informations/petitions/1548389/download-documents?artifactId=k_hzx8onBUrJmXs4ydnz0x7FURiK9RcPBIhGTYM1s_H-dcHGTdvdgUo>.
- US8615700B2 bibliography records Micron TN-29-15 (June 2007), TN-29-41 (October 2008), and TN-29-42 as contemporaneous NAND technical notes: <https://patents.google.com/patent/US8615700B2>.

---

## Status

**`grounded`** — the central mechanism and error-propagation boundary remain grounded in manufacturer-primary Micron documentation, now bounded by earlier Samsung named-product evidence, ONFI 1.0 interface semantics, and a later Hynix automatic-error-detection counterexample. The new deepening closes the narrow `Micron-only integrity warning` gap without claiming invention priority or a demonstrated vendor-to-standard genealogy.

Open work is now narrower: recover an official directly downloadable archival copy of TN-29-41 if convenient; recover a directly renderable archival ONFI 1.0 copy if a page-level standards argument needs it; build a complete cross-vendor / patent / ONFI-ballot Copyback genealogy in `computing-archaeology`; inspect modern on-die-ECC Copyback variants separately; and seek independent fault-injection measurements before making product-compliance claims.