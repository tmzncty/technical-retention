from pathlib import Path

CASE_PATH = Path("cases/134-nand-copyback-relocation-integrity-boundary.md")
EVIDENCE_PATH = Path("evidence/134-2005-2008-nand-copyback-integrity-grounding.md")
ROADMAP = Path("ROADMAP.md")
INDEX = Path("CASE_INDEX.md")

case_text = r'''# NAND Copy-Back: Relocation Without Guaranteed Revalidation

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
'''

evidence_text = r'''# Case 134 evidence — NAND Copy-Back relocation / integrity boundary, 2005–2008

## Purpose

Ground one bounded retention question:

> **Can a NAND page be physically re-instantiated at a new location without that relocation itself re-establishing source-data correctness or full ECC correction margin?**

The answer is grounded here from manufacturer documentation and a public patent record. The evidence is intentionally narrower than a general NAND/SSD history.

## Evidence labels used here

- `H/P` — historical claim grounded in a directly inspectable primary/public technical record;
- `H/P*` — manufacturer-primary document whose current custody is a preserved mirror or official legal-proceeding reproduction rather than the original vendor host;
- `E` — engineering reconstruction from the documented mechanism;
- `A` — bounded functional analogy;
- `X` — rejected/unsupported stronger claim.

## Source set and custody

### S1 — Samsung K9F5608U0D product datasheet (`H/P*`)

Samsung Electronics, `K9F5608R0D / K9F5608U0D / K9F5608D0D`, **32M x 8 Bit NAND Flash Memory**.

- revision history in the preserved document: initial issue 16 May 2005; final revision 30 Oct 2005; revision 1.1 dated 30 Dec 2005;
- preserved full-document mirror: <https://www.100y.com.tw/pdf_file/37-SAMSUNG-K9F5608X0D.pdf>;
- searchable copy-back page: <https://www.alldatasheet.com/html-pdf/129688/SAMSUNG/K9F5608U0D-PCB0/9234/30/K9F5608U0D-PCB0.html>.

Custody qualification: this is a Samsung-authored manufacturer datasheet preserved through third-party mirrors. The historical Samsung technical-information URL is printed in the document, but current first-party hosting was not established in this slice. Product-mechanism claims are therefore retained as `H/P*`, not silently upgraded to current first-party custody.

### S2 — Samsung US7466597B2 / US20060050576A1 (`H/P`)

Hyung-Gon Kim / Samsung Electronics, **“NAND flash memory device and copyback program method for same.”**

- Korean priority: 9 Sep 2004;
- U.S. filing: 22 Dec 2004;
- U.S. publication: 9 Mar 2006;
- grant publication: 16 Dec 2008;
- public record: <https://patents.google.com/patent/US7466597B2/en>.

The priority date is an application-lineage fact, not a public-disclosure date.

### S3 — Micron TN-29-41 (`H/P*`)

Micron Technology, **“Using COPYBACK Operations in NAND Flash Devices,”** Technical Note TN-29-41, dated 1 Oct 2008 in later patent bibliographies.

- the historical `download.micron.com` URL and date are preserved in a later patent bibliography: <https://patents.google.com/patent/US8615700B2/en>;
- an official USPTO proceeding record preserves substantive TN-29-41 text used below: <https://ptacts.uspto.gov/ptacts/public-informations/petitions/1548389/download-documents?artifactId=k_hzx8onBUrJmXs4ydnz0x7FURiK9RcPBIhGTYM1s_H-dcHGTdvdgUo>.

Custody qualification: source authorship/title/date are strongly identified as Micron's manufacturer technical note, but this run did not retrieve the historical note from a live Micron host. Claims from the preserved reproduction are marked `H/P*`.

## Historical record

### S1: internal page movement and destination program status

The Samsung datasheet describes `COPY-BACK PROGRAM` as a way to rewrite a page to another page in the same array without using external memory. The bounded sequence is:

```text
source page
    -> page read
    -> internal buffer
    -> destination address
    -> direct destination program
```

The product uses the feature for block-management work such as moving unchanged pages when a block is replaced/updated, and restricts copy-back to the same memory plane.

The destination programming sequence reports completion/failure through ready/busy and pass/fail status.

### S1: source charge-loss errors can be propagated

The same product text warns that a program failure is reported by status **but** a source-page bit error caused by charge loss can be carried into subsequent copy-back operations, allowing accumulated copy-back operations to accumulate bit errors. It recommends stronger ECC for this path.

This directly grounds:

> `program status` and `source-data integrity` are different evidence relations.

### S2: program verify is not source-read EDC

The Samsung patent record describes copy-back as source-page read -> page buffer -> target-page program -> program verify, and explicitly distinguishes:

- **copyback program verify** — checking whether the buffered pattern has been programmed to the target;
- **EDC scan / parity comparison** — checking whether an error occurred in the source-page copyback read.

Its proposed embodiments can stop the program when source-read EDC fails. The patent motivates this by observing that one error may occur in copyback read and another in program/verify, producing an error burden that a one-bit-ECC regime cannot fully correct.

This is **patent disclosure**, not proof every Samsung NAND product implemented that EDC path.

### S3: external data correction can restore ECC capability

Micron TN-29-41 states that COPYBACK without external data output/input can lead to error counts beyond ECC limits. It then states that outputting/inputting the data during COPYBACK can permit correction and return to the original programmed value, resetting ECC to its maximum error-correction capability.

This directly grounds a positive distinction:

```text
copy only
    !=
copy + validation/correction + rewrite
```

## Engineering reconstruction

### R1 — physical relocation != source revalidation (`E`)

S1 and S2 show that moving data through an internal page buffer and successfully programming the destination does not, by itself, answer whether the source codeword was already wrong.

### R2 — new programming event != maximum ECC margin (`E`)

A newly programmed destination has a new physical embodiment, but S1/S3 show that already accumulated logical errors can be carried forward unless the data are checked/corrected. The new page therefore cannot automatically be described as having maximum codeword correction margin.

### R3 — program verify != end-to-end integrity check (`E`)

S2 directly separates program verify from source-read parity checking. `PASS` at the target-program layer should not be promoted into an end-to-end correctness verdict.

### R4 — relocation can copy a defect (`E`)

The preservation machinery has no semantic filter unless one is separately provided. A source bit error can become part of the target pattern and later combine with additional errors.

### R5 — correction-and-rewrite is a distinct renewal relation (`E`)

S3 says external I/O during COPYBACK can enable correction and restore maximum ECC correction capability. Therefore an integrity-renewing move requires more than physical relocation alone.

### R6 — raw copy-back != FTL currentness transition (`E`, `X`)

A source/destination page movement does not itself establish which host-visible logical designation now resolves to the new page. Currentness/mapping is a higher-layer relation.

## Functional analogies — bounded

### Case 04 mapped Flash (`A`)

Case 04 already grounds identity-preserving relocation before erase. Case 134 adds an orthogonal integrity axis: **the copied representation can be current while still containing a correctable error**. Similar relocation semantics do not establish that Ban's 1993 system used NAND copy-back.

### Case 36 correct-and-refresh (`A`)

Case 36's bounded FCR-style maintenance includes error evidence/correction plus rewrite. Case 134 is a counterexample to the shortcut `rewrite = correction`: a physical rewrite can reproduce an erroneous source codeword if validation/correction is absent.

### Scrub cases (`A`)

Cases 18/83 use verification as part of integrity qualification/maintenance. Copy-back demonstrates that **movement and verification are separable**. No shared genealogy is asserted.

## Philosophical interpretation — bounded

The technical fact supports one narrow conceptual statement:

> A new bearer can inherit an old error because re-instantiation preserves what the operative copying relation treats as the state to be continued.

This clarifies `identity without location` by adding a limit: identity continuity and material renewal do not imply purification or renewed truth of the retained value.

The analogy stops there. Errors are not thereby `memories`; copy-back is not a general theory of copying; and this mechanism cannot be projected onto archival migration or distributed replication without new evidence.

## Rejected claims / stop conditions

- Samsung invented NAND copy-back — **not established**.
- 9 Sep 2004 priority is public disclosure — **rejected**; U.S. publication is 9 Mar 2006.
- Samsung datasheet mirror is current Samsung hosting — **rejected**; custody is qualified.
- every copy-back implementation lacks error detection — **rejected** by S2's separate EDC design.
- copy-back `PASS` proves source payload correctness — **rejected**.
- newly programmed target necessarily restores maximum ECC margin — **rejected** unless correction/re-encoding is established.
- copy-back is equivalent to refresh/scrub/FCR — **rejected**.
- same-plane constraint is universal — **not established**.
- patent disclosure proves named-product deployment — **rejected**.
- Micron note is an independent fault-injection study — **rejected**; it is manufacturer technical guidance.
- raw copy-back proves FTL mapping changed — **rejected**.

## Related-repository check

Fresh default-branch searches of `tmzncty/computing-archaeology` for `copyback` and `internal data move` returned no dedicated technical-history case. Broader command genealogy, page-buffer architecture, controller deployment, ONFI/Toggle evolution, and modern 3-D NAND behavior belong there if developed. This evidence file keeps the retention-specific `relocation != revalidation` boundary.

## Result

This slice grounds a bounded counterexample important to the repository's identity/renewal arguments:

> **A retained NAND value can receive a new physical embodiment without the relocation itself restoring source-data correctness or full ECC correction margin. Program completion, source integrity, logical currentness, and later reclamation are separate relations.**

Still open:

- earliest copy-back terminology and implementation;
- direct first-party Samsung/Micron archival copies with stable page anchors;
- independent fault injection measuring repeated-copyback error accumulation;
- MLC/TLC/QLC and 3-D NAND copyback behavior;
- on-die ECC visibility and controller policy;
- managed-SSD use of internal move primitives;
- standards/revision genealogy;
- higher-layer mapping crash semantics around source retirement.
'''

CASE_PATH.write_text(case_text, encoding="utf-8")
EVIDENCE_PATH.write_text(evidence_text, encoding="utf-8")

roadmap = ROADMAP.read_text(encoding="utf-8")
roadmap_title = "Case 134 NAND Copy-Back relocation / integrity-validation boundary"
if roadmap_title in roadmap:
    raise SystemExit("ROADMAP already contains Case 134 marker")
roadmap_marker = "- [ ] DRAM evolution and refresh machinery beyond the bounded case —"
if roadmap.count(roadmap_marker) != 1:
    raise SystemExit(f"ROADMAP insertion marker count={roadmap.count(roadmap_marker)}")
roadmap_bullet = "- [x] Case 134 NAND Copy-Back relocation / integrity-validation boundary — [`cases/134-nand-copyback-relocation-integrity-boundary.md`](cases/134-nand-copyback-relocation-integrity-boundary.md), grounded by [`evidence/134-2005-2008-nand-copyback-integrity-grounding.md`](evidence/134-2005-2008-nand-copyback-integrity-grounding.md): Samsung's 2005 K9F5608U0D product documentation grounds an internal source-page→buffer→destination-page COPY-BACK path and explicitly warns that source charge-loss errors can be carried/accumulated even when destination program status reports the programming outcome. Samsung's 2004-priority / 2006-public patent record then separates source-read EDC from target program verify, while Micron TN-29-41 (2008) states that external output/input can permit correction and restore maximum ECC correction capability. This closes the bounded `physical relocation != source-data revalidation`, `program completion != end-to-end integrity`, and `new embodiment != renewed ECC margin` seam without claiming copy-back invention priority, universal unchecked behavior, FTL-currentness semantics, modern 3-D/on-die-ECC behavior, or named-SSD deployment. Broader NAND copy-back/page-buffer/controller genealogy belongs primarily in `computing-archaeology`."
roadmap = roadmap.replace(roadmap_marker, roadmap_bullet + "\n\n" + roadmap_marker, 1)
ROADMAP.write_text(roadmap, encoding="utf-8")

idx = INDEX.read_text(encoding="utf-8")
case_link = "134-nand-copyback-relocation-integrity-boundary.md"
if case_link in idx:
    raise SystemExit("CASE_INDEX already contains Case 134")
lines = idx.splitlines()
row = "| [NAND Copy-Back: Relocation Without Guaranteed Revalidation](cases/134-nand-copyback-relocation-integrity-boundary.md) | **grounded** | NAND source-page read -> internal page buffer -> destination-page program + optional/separate source-read error validation | separate physical re-instantiation, destination program success, source codeword correctness/ECC margin, logical currentness, and later reclamation; show a new bearer can reproduce an old correctable error | [2005–2008 copy-back integrity grounding](evidence/134-2005-2008-nand-copyback-integrity-grounding.md); earliest genealogy, first-party archival page anchors, MLC/3-D/on-die-ECC evolution, named-controller deployment, and fault injection remain open |"
row_pos = None
for i, line in enumerate(lines):
    if line.startswith("| [Micron LPDDR4 MR4 Thermal Offset:"):
        row_pos = i + 1
        break
if row_pos is None:
    raise SystemExit("Case 133 table row not found")
lines.insert(row_pos, row)
idx = "\n".join(lines) + "\n"

findings_marker = "## Case 02 deepening — TCM-32 clear/write and whole-stack memory-clear findings"
if idx.count(findings_marker) != 1:
    raise SystemExit(f"CASE_INDEX findings marker count={idx.count(findings_marker)}")
findings = r'''## Case 134 — NAND Copy-Back relocation / integrity findings

Evidence: [`evidence/134-2005-2008-nand-copyback-integrity-grounding.md`](evidence/134-2005-2008-nand-copyback-integrity-grounding.md).

- **2725 — copy-back relocation != external data round trip.** Samsung's bounded product moves the source page into an internal buffer and programs a destination page without ordinary external-memory read/reload, which is the performance purpose of the command. (`H/P*`, `E`)
- **2726 — destination program status != source-data correctness.** The same datasheet reports copy-back program failure through pass/fail status but separately warns that a source charge-loss bit error can be carried and accumulated. (`H/P*`, `E`)
- **2727 — program verify != source-read error detection.** Samsung's public patent record treats target program verify and source-page EDC/parity checking as distinct operations answering different questions. (`H/P`, `E`)
- **2728 — one successful physical re-instantiation != maximum ECC margin.** A new destination page can inherit an already-wrong source bit pattern; the physical programming event is new while the protected codeword may already have consumed correction capability. (`H/P*`, `E`)
- **2729 — relocation can preserve an error as well as a value.** Copying is faithful to the page-buffer representation unless a separate validation/correction path changes that representation. (`E`)
- **2730 — accumulated copy-back errors != inevitable copy-back failure.** Samsung documents a risk/engineering constraint, not a deterministic statement that every repeated copy loses data. (`H/P*`, `X`)
- **2731 — source-read validation != destination program verification.** Samsung's EDC embodiment can reject a source-read error before/alongside programming while program verify remains concerned with whether target cells accepted the buffered pattern. (`H/P`, `E`)
- **2732 — patent EDC disclosure != universal shipped-product behavior.** The patent proves a disclosed mechanism and prior problem formulation, not that every Samsung or other vendor NAND implemented it. (`H/P`, `X`)
- **2733 — external COPYBACK data I/O can be retention maintenance rather than mere transfer overhead.** Micron TN-29-41 says output/input can allow correction, return data to the original programmed value, and restore maximum ECC correction capability. (`H/P*`, `E`)
- **2734 — rewrite occurred != correction occurred.** A physical destination program can reproduce buffered state without correcting the source codeword; correction-and-rewrite is a stronger maintenance relation. (`E`, `X`)
- **2735 — copy-back != FTL currentness update.** Source/destination physical pages are insufficient to establish which logical designation now counts as current; mapping/authority is a separate higher-layer relation. (`E`, `X`)
- **2736 — copy-back != scrub / refresh / FCR.** Similar movement/rewrite can participate in maintenance, but those regimes add distinct trigger, validation, correction, or policy semantics. (`A`, `X`)
- **2737 — Case 04 relocation and Case 134 integrity are orthogonal axes.** Case 04 grounds logical identity across location change; Case 134 shows that such re-instantiation does not automatically revalidate the copied codeword. (`A`, `E`)
- **2738 — new bearer != semantic purification.** The bounded philosophical result is only that material succession can carry forward a defect when the copying relation treats the defective representation as authoritative enough to reproduce. (`I`, `E`)
- **2739 — related-repository boundary:** fresh `tmzncty/computing-archaeology` searches for `copyback` and `internal data move` found no dedicated case; broad NAND command/page-buffer/controller/standards genealogy belongs there if developed, while Case 134 keeps the retention-specific relocation/revalidation boundary. (`H/P` project-state record)

'''
idx = idx.replace(findings_marker, findings + findings_marker, 1)
INDEX.write_text(idx, encoding="utf-8")

assert CASE_PATH.read_text(encoding="utf-8").count("## Historical record") == 1
assert CASE_PATH.read_text(encoding="utf-8").count("## Engineering reconstruction") == 1
assert CASE_PATH.read_text(encoding="utf-8").count("## Functional analogy — bounded") == 1
assert CASE_PATH.read_text(encoding="utf-8").count("## Philosophical interpretation — bounded") == 1
assert EVIDENCE_PATH.read_text(encoding="utf-8").count("## Historical record") == 1
assert ROADMAP.read_text(encoding="utf-8").count(roadmap_title) == 1
idx_check = INDEX.read_text(encoding="utf-8")
assert idx_check.count("## Case 134 — NAND Copy-Back relocation / integrity findings") == 1
assert idx_check.count(case_link) >= 1
for n in range(2725, 2740):
    marker = f"**{n} —"
    assert idx_check.count(marker) == 1, (n, idx_check.count(marker))
print("Case 134 research slice applied successfully")
