# NAND Copy-Back: Relocation Without Guaranteed Revalidation

## Status

**`grounded`** — bounded to a Samsung 2005 NAND product datasheet, Samsung's 2004-priority / 2006-public copyback error-detection patent record, and Micron Technical Note TN-29-41 (2008) as retained through an official USPTO proceeding record and later patent bibliography.

Grounding record: [`../evidence/134-2005-2008-nand-copyback-integrity-grounding.md`](../evidence/134-2005-2008-nand-copyback-integrity-grounding.md).

## Scope

This case asks one narrow question left implicit by mapped-Flash relocation and later Flash-refresh cases:

> When NAND copies a page internally from one physical page to another, does the new physical embodiment automatically mean that the logical data have been revalidated or that ECC margin has been restored?

The bounded answer is **no**. Samsung product documentation describes a fast `COPY-BACK PROGRAM` path that reads a source page into an internal buffer and programs a destination page without the ordinary external read/reload path. The same document warns that a charge-loss bit error in the source can be carried forward and that repeated copy-back can accumulate bit errors. Samsung's later published patent record makes source-read error detection a **separate** operation from destination program verify. Micron TN-29-41 then states the complementary maintenance rule directly: external data output/input during COPYBACK can allow correction and return data to the original programmed value, restoring maximum ECC correction capability.

This is **not**:

- a general history of NAND, FTLs, garbage collection, or wear leveling;
- a claim that Samsung invented copy-back;
- a claim that every NAND copy-back implementation omits error detection;
- a claim that a successful copy-back status proves the source payload was correct;
- a claim that moving a page automatically changes host-visible mapping/currentness;
- a claim that reprogramming fresh cells necessarily restores the logical codeword's ECC margin;
- a claim that copy-back is equivalent to scrub, refresh, read-retry, or FCR-style correction-and-rewrite;
- a claim about modern 3-D NAND, on-die ECC, or managed-SSD controller behavior.

## Historical vocabulary

The bounded sources use terms including:

- `COPY-BACK PROGRAM` / `Copy-Back Program`;
- `copyback read operation`;
- `copyback program operation`;
- `copyback program verify operation`;
- `source page` / `target page` or `destination page`;
- `page buffer` / `internal buffer`;
- `pass/fail status`;
- `error detection code` / `EDC`;
- `ECC`;
- `data integrity`.

`Relocation`, `revalidation`, `currentness`, `embodiment`, and `ECC-margin renewal` are project engineering terms. They should not be attributed to the historical actors unless the source itself uses an equivalent expression.

## Historical record

### 2005 Samsung product documentation: copy-back moves the page internally

Samsung's `K9F5608U0D` family datasheet revision history dates the initial issue to 16 May 2005 and a final revision to 30 October 2005, with revision 1.1 on 30 December 2005.

Its `COPY-BACK PROGRAM` section describes the operation as a fast way to rewrite data from one NAND page to another page in the array **without utilizing an external memory**. The sequence is:

1. a page read moves the source page into the device's internal buffer;
2. the host supplies the destination page address;
3. data already in the internal buffer are programmed directly into destination cells;
4. the destination program operation exposes ordinary ready/busy and pass/fail completion status.

The document presents a concrete block-management use: when part of a block changes, unchanged pages may need to be copied to a newly assigned free block. It also constrains the bounded device's copy-back to the same memory plane.

**Primary-document custody note:** the Samsung datasheet was inspected through preserved third-party mirrors because the historical Samsung semiconductor URL printed in the document is no longer the retrieval path used in this run. The document identifies Samsung Electronics as the author/vendor and preserves its revision history; detailed claims from this mirror are therefore marked `H/P*` in the evidence record rather than pretending current first-party hosting.

### 2005 Samsung product documentation: program success is not source-data correctness

The same copy-back section distinguishes two failure relations:

- a copy-back **program failure** is reported through pass/fail status;
- a **source-page bit error from charge loss** can be copied onward, so accumulated copy-back operations can accumulate bit errors.

Samsung therefore recommends stronger ECC for the bounded copy-back path.

This is unusually direct product-level evidence that the status proving the destination programming sequence completed is not, by itself, a certificate that the source logical codeword was error-free.

### 2004-priority / 2006-public Samsung patent: source-read error checking is a separate mechanism

Samsung's `NAND flash memory device and copyback program method for same` has Korean priority dated 9 September 2004, a U.S. filing date of 22 December 2004, and U.S. publication `US20060050576A1` on 9 March 2006. Priority is not treated here as public disclosure.

The published record describes conventional copy-back as:

```text
source-page read -> page buffer -> target-page program -> program verify
```

without reading the page-buffer data out through the normal external path.

Crucially, the patent distinguishes **copyback program verify** from **source-read error detection**. Program verify checks whether the data held in the page buffer were successfully programmed to the target page. The proposed EDC path separately compares parity so that an error occurring during the source-page copyback read can stop the target program.

The patent's stated problem is that one error may arise during copyback read and another during copyback program/verify, exceeding the correction capability of a one-bit-ECC regime. Whether every real product implemented the disclosed EDC is not established by the patent.

### 2008 Micron TN-29-41: external correction can restore ECC correction capability

Micron Technical Note `TN-29-41`, **“Using COPYBACK Operations in NAND Flash Devices,”** is dated 1 October 2008 in later patent bibliographies. An official USPTO proceeding record preserves the note's substantive text.

Micron states that COPYBACK without external data output/input can allow errors to grow beyond ECC protection limits. It then gives the complementary path: when the data are output and, if required, input again during COPYBACK, the controller can correct the data, return it to the original programmed value, and restore maximum ECC error-correction capability.

The bounded distinction is therefore explicit in manufacturer vocabulary:

```text
internal page relocation
    !=
checked/corrected relocation
```

**Custody note:** the original historical `download.micron.com` URL is recorded in later patent bibliographies, while the directly inspected text in this run is preserved by the USPTO proceeding record. The source is treated as a Micron primary technical note with custody qualification (`H/P*`), not as an independently replicated experiment.

## Retained state and substrate

At least four relations matter in this case:

1. **source-page physical state** — threshold/charge state read from the existing NAND page;
2. **internal page-buffer state** — the transient representation from which the destination is programmed;
3. **destination-page physical state** — a newly programmed physical embodiment;
4. **ECC relation** — parity/check information that determines how much error can still be corrected when the data are later checked.

A higher-level mapping relation may decide whether the destination page becomes the current logical embodiment, but the raw copy-back command itself does not establish an FTL's host-visible currentness transition.

## Retention mechanism

Copy-back is a **relocation/re-instantiation mechanism**: a retained value is read from one NAND page into an internal buffer and reprogrammed into another page.

That makes it superficially resemble renewal, but the bounded sources add an important qualifier. If the source representation already contains an error and the path does not check/correct it, a newly programmed destination can preserve the **erroneous reconstructed bit pattern** rather than restore the intended codeword.

Thus two kinds of continuation must be separated:

```text
physical re-instantiation
    destination cells receive a newly programmed pattern

logical/integrity revalidation
    the transferred codeword is checked and, where possible, corrected
```

They can occur together, but neither implies the other by definition.

## Addressing and access geometry

The Samsung product path uses a source-page read followed by a destination-page program and restricts copy-back to the same plane on the bounded device.

The operation therefore has two addresses with different roles:

- **source address** — which existing physical page supplies the buffered pattern;
- **destination address** — which page receives the new physical embodiment.

This is not enough to infer a logical-address mapping update. A controller may use copy-back as part of block replacement, garbage collection, or wear management, but those higher-level currentness decisions require their own source evidence.

## Read semantics

The source page is read into an internal page buffer. In the fast bounded path, the data need not traverse the ordinary external data path before destination programming.

The historical significance is not that internal reads are inherently unsafe. It is that bypassing the external check/correction round trip can also bypass an opportunity to normalize a correctable codeword before it is reprogrammed.

## Write / program semantics

Destination programming has its own verify/completion relation.

Samsung's patent makes the separation unusually clear:

- **program verify** asks whether page-buffer data were successfully programmed to the target;
- **EDC/source-read check** asks whether an error occurred in the data read from the source before that target program should be trusted.

Therefore:

> **destination program success != source logical correctness**.

## Erase and reclamation semantics

Copy-back does not itself erase the source block. In block-management use, copied current pages can be re-instantiated elsewhere so that an old erase block may later be reclaimed.

That is compatible with Case 04's broader `copy current -> erase old -> remap` pattern, but Case 134 adds a new integrity question:

> **Was the state copied merely transferred, or also checked/corrected before the old embodiment was retired?**

The sources do not justify calling every copy-back a scrub or refresh.

## Engineering reconstruction

### New embodiment does not guarantee renewed logical correctness

A destination page programmed moments ago has a new physical programming event. But if the internal buffer contains a source error and the error is copied along with stale/unchanged check information, the logical codeword can arrive at the new page with correction margin already consumed.

Therefore:

> **new physical embodiment != fresh logical integrity margin**.

This is the central engineering result of the case.

### Program verify and integrity revalidation answer different questions

The patent explicitly separates target program verify from source-read error detection. The two checks answer different questions:

```text
program verify:
    did target cells accept the page-buffer pattern?

integrity check/correction:
    does that pattern still represent the intended protected codeword?
```

Therefore:

> **copy-back completion != end-to-end revalidation**.

### Relocation can preserve an error as faithfully as a value

If a correctable source error is not corrected before transfer, copy-back can reproduce that erroneous bit pattern at a new physical location. Subsequent physical errors can then consume additional ECC margin.

This does not make error accumulation inevitable. It means that **relocation alone does not remove already accumulated logical error state**.

### Checked/corrected relocation is a distinct maintenance regime

Micron's 2008 note makes the positive path explicit: output/input permits correction and return to the original programmed value, restoring maximum ECC correction capability.

Therefore:

> **relocation + validation/correction + rewrite**

is analytically stronger than

> **relocation + program verify**.

That stronger path is closer to a scrub/renewal operation, but terminology should follow the actual product/controller source rather than being projected backward.

### Copy-back is not automatically a mapping transition

A physical source->destination copy does not identify which logical page, LBA, file block, or FTL mapping should now count as current. The management layer must separately establish currentness and later retire/reclaim the old embodiment.

Therefore:

> **physical copy != logical-currentness update**.

## Failure and forgetting boundaries

The bounded sources expose several distinct failure classes:

- **source retention/read error** — a bit presented from the source page is already wrong or is read wrongly;
- **copyback-read error** — the source->buffer read path produces an error;
- **destination program failure** — target cells fail to accept the buffered pattern;
- **accumulated ECC-margin loss** — copied errors plus later errors exceed correction capability;
- **mapping/currentness error** — a higher layer identifies the wrong physical embodiment as current;
- **reclamation failure** — later erase/space recovery is a separate operation.

These must not be collapsed into one generic `copy-back failed` state.

## Prior art and novelty boundary

This case does **not** establish the invention date of NAND copy-back. Samsung's patent claims 2004 Korean priority, but its own discussion treats copy-back and error checking as already-known design context. The 2005 product datasheet is a named-product witness, not a first-commercialization proof.

The contribution to this repository is narrower:

> Product and manufacturer-primary evidence show that **physical NAND relocation and integrity revalidation are separable retention operations**.

Earliest copy-back terminology, first implementation, cross-vendor controller genealogy, and later ONFI/Toggle/managed-NAND evolution belong primarily in `computing-archaeology` if pursued.

## Functional analogy — bounded

### Case 04 — mapped Flash reclamation

Case 04 establishes that current data can be copied before an old erase unit is destroyed and that logical identity can survive physical relocation. Case 134 adds a different axis: **copying the current embodiment does not by itself establish that the copied codeword was revalidated before relocation**.

This is a functional decomposition, not evidence that Ban's 1993 transfer-unit mechanism used NAND copy-back.

### Case 36 — NAND correct-and-refresh

Case 36's correction-and-refresh regime uses error evidence/correction plus rewrite to renew a weakening representation. Copy-back can instead move page-buffer contents directly. Therefore:

> **rewrite occurred != correction occurred**.

No genealogy between one vendor copy-back command and the research FCR policy is asserted.

### Cases 18 / 83 — scrub and verification

ZFS/HDFS verification cases deliberately acquire integrity evidence before repair or qualification. Copy-back demonstrates the counterexample: **movement can happen without the same verification semantics**. Distributed checksum/scrub mechanisms are not NAND copy-back mechanisms.

## Philosophical interpretation — bounded

The exact technical fact is narrow: a system can create a **new material embodiment** while carrying forward an error already present in the source representation.

That complicates any simple equation of technical renewal with restoration of an ideal original. Re-instantiation preserves whatever state the copying path treats as authoritative enough to reproduce; without a separate validation relation, that can include a defect.

A bounded conceptual formulation is:

> **material succession can preserve logical identity without guaranteeing semantic purification.**

This does **not** mean errors are `memories`, that every migration reproduces corruption, or that physical replacement is philosophically equivalent across Flash, filesystems, and distributed replicas.

## Rejected claims / stop conditions

- **Samsung invented NAND copy-back** — not established.
- **2004 priority date = public disclosure date** — rejected; U.S. publication is March 2006.
- **every copy-back is unchecked** — rejected; the Samsung patent itself discloses integrated source-read error detection.
- **pass/fail program status = source codeword verified** — rejected by the product warning and patent decomposition.
- **new destination page = maximum ECC margin restored** — rejected unless a correction/re-encoding path is separately established.
- **copy-back = scrub / FCR / refresh** — rejected; those terms carry additional trigger/validation/correction semantics.
- **copy-back = FTL remap** — rejected; physical copying and logical-currentness update are separate relations.
- **same-plane restriction is universal NAND law** — rejected; it is a bounded product/interface constraint.
- **manufacturer mirror = current official hosting** — rejected; source custody is explicitly qualified.
- **patent disclosure = shipped implementation** — rejected.
- **copy-back accumulated-error warning = measured field failure rate** — rejected; the datasheet warning is an engineering/product contract, not an independent failure-rate experiment.

## Related-repository check

Fresh searches of `tmzncty/computing-archaeology` for `copyback` and `internal data move` returned no dedicated case to reuse. If the wider history of NAND copy-back commands, page-buffer architectures, controller adoption, or standards genealogy is developed, it belongs primarily there. `technical-retention` keeps only the bounded **relocation vs revalidation** relation.

## Sources

### Samsung product documentation — manufacturer primary, mirrored (`H/P*`)

- Samsung Electronics, `K9F5608R0D / K9F5608U0D / K9F5608D0D`, **32M x 8 Bit NAND Flash Memory**, revision history beginning 16 May 2005; preserved PDF mirror: <https://www.100y.com.tw/pdf_file/37-SAMSUNG-K9F5608X0D.pdf>.
- Samsung Electronics, `K9F5608U0D-PCB0`, copy-back section preserved as searchable HTML: <https://www.alldatasheet.com/html-pdf/129688/SAMSUNG/K9F5608U0D-PCB0/9234/30/K9F5608U0D-PCB0.html>.

### Samsung patent — public patent record (`H/P`)

- Hyung-Gon Kim / Samsung Electronics, **“NAND flash memory device and copyback program method for same,”** US7466597B2 / US20060050576A1; Korean priority 9 Sep 2004, U.S. filing 22 Dec 2004, U.S. publication 9 Mar 2006: <https://patents.google.com/patent/US7466597B2/en>.

### Micron manufacturer note — primary with custody qualification (`H/P*`)

- Micron Technology, **“Using COPYBACK Operations in NAND Flash Devices,”** Technical Note TN-29-41, 1 Oct 2008. Historical manufacturer URL is recorded in later patent bibliographies; directly inspected substantive text in this run is preserved in a USPTO proceeding record: <https://ptacts.uspto.gov/ptacts/public-informations/petitions/1548389/download-documents?artifactId=k_hzx8onBUrJmXs4ydnz0x7FURiK9RcPBIhGTYM1s_H-dcHGTdvdgUo>.
- Later patent bibliography preserving the title/date/historical Micron URL: <https://patents.google.com/patent/US8615700B2/en>.
