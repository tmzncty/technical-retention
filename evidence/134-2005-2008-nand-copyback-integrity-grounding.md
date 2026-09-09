# Case 134 evidence — NAND Copy-Back relocation / integrity boundary, 2005–2008

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
