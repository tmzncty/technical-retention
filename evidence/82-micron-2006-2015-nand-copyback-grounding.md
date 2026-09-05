# Evidence 82 — Micron NAND Internal Data Move / COPYBACK Integrity Grounding

## Purpose

Ground Case 82's narrow claim that a NAND page can be relocated internally while already-present errors are carried forward because the ordinary external controller/ECC path is bypassed. This record does **not** attempt a complete NAND COPYBACK genealogy or a general garbage-collection/wear-leveling history.

## Evidence classification

- **Historical record (H/P):** Micron technical notes and product documentation describing commands, data paths, intended use, limitations, and recommended integrity checks.
- **Engineering reconstruction (E):** separation of location change from integrity requalification, temporary register embodiment from durable destination state, and remaining ECC margin from payload identity.
- **Functional analogy (A):** controlled comparisons with mapped Flash, Correct-and-Refresh, disturbance/reclaim, and bad-block replacement already grounded elsewhere in this repository.
- **Philosophical interpretation (I):** the limited observation that migration can preserve both value and accumulated imperfection; not historical actor vocabulary.

---

## Source 1 — Micron TN-29-15, `NAND Flash Internal Data Move`

### Source identity

Micron Technology, technical note **TN-29-15**, title rendered in surviving copies as *NAND Flash Performance Improvement Using Internal Data Move* / *NAND Flash Internal Data Move*. The inspected text mirror identifies Rev. C 3/10 and Micron copyright beginning in 2006. A later patent bibliography dates the Micron note to June 2007.

- text-preserving mirror: <https://doczz.net/doc/7838214/tn-29-15--nand-flash-performance-improvement-using-internal>
- historical Micron path preserved in contemporary citations: <http://download.micron.com/pdf/technotes/nand/tn2915.pdf>
- bibliographic witness: <https://patents.google.com/patent/US8615700B2>

### Directly supported points

1. Micron names the feature `internal data move (IDM)`.
2. Traditional movement is described as external page read, error-correction post-processing, then programming to the new location.
3. IDM eliminates the extra external movement steps.
4. IDM consists of an internal read followed by internal program.
5. `READ FOR INTERNAL DATA MOVE (00h–35h)` moves the addressed source page into the cache register.
6. `PROGRAM FOR INTERNAL DATA MOVE (85h–10h)` programs the register contents to the destination.
7. The note states that when data is moved internally there is no opportunity to perform error correction through the ordinary path.
8. It warns that excessive IDM operations without periodic checks may let errors accumulate and decrease reliability.
9. It recommends robust multibit error correction and periodic `post-READ` integrity checks, with checking frequency dependent on required integrity and how many IDM operations occur between checks.
10. Its worked data-error scenario shows an already-present bit error following the data into the internal register and then following the programmed page to the new NAND location because correction was not performed.

### Retention consequence

This source directly blocks the inference:

> new physical embodiment = renewed error-free representation.

The move preserves the page image strongly enough to relocate it, but the page image may already include a correctable error. Relocation and correction are therefore separate operations in this bounded design.

### Evidence caution

The note's performance examples and command restrictions are product-generation dependent. They should not be generalized into a timeless NAND geometry. The central claim needs only the documented path and ECC omission.

---

## Source 2 — Micron TN-29-41, `Using COPYBACK Operations to Maintain Data Integrity in NAND Flash Devices`

### Source identity

Micron Technology, **TN-29-41**, October 2008.

Historical and later-preserved Micron URLs:

- <http://download.micron.com/pdf/technotes/nand/tn2941_idm_copyback.pdf>
- <https://media-www.micron.com/-/media/client/global/documents/products/technical-note/nand-flash/tn2941_idm_copyback.pdf?rev=c0a04e8ff8bd4f309bab7ea91ad98035>

An indexed copy was preserved as a USPTO/PTAB exhibit:

- <https://ptacts.uspto.gov/ptacts/public-informations/petitions/1548389/download-documents?artifactId=k_hzx8onBUrJmXs4ydnz0x7FURiK9RcPBIhGTYM1s_H-dcHGTdvdgUo>

A U.S. patent bibliography independently records the October 2008 Micron note:

- <https://patents.google.com/patent/US8615700B2>

### Directly supported points from the indexed note

1. Micron frames COPYBACK as an internal movement mechanism and discusses it specifically as a data-integrity problem.
2. The note states that NAND requires ECC to protect against program/read errors in the bounded product context.
3. It warns that COPYBACK without external data output/input can allow errors to move beyond the protection limits of ECC.
4. It explains that inputting/outputting data around COPYBACK gives the system an opportunity to correct data and return it to the intended programmed value.
5. This corrective path can restore the available correction margin rather than merely transport the same raw error population to another location.

### Retention consequence

TN-29-41 strengthens TN-29-15's boundary. The missing external transfer is not only a bandwidth optimization. It can also be the missing **qualification/correction stage**. The system therefore has two distinguishable continuation goals:

```text
preserve page identity across relocation
preserve enough correctness margin for future reads
```

They can be served by different work.

### Evidence caution

The phrase `restore the ECC budget` in Case 82 is an engineering shorthand for recovering correction margin after correcting/reprogramming data. The ECC code is not literally a consumable material reservoir.

---

## Source 3 — Micron 8Gb Automotive Async NAND, Rev. B, March 2015

### Source identity

Micron Technology, *8Gb Automotive Async NAND Flash Memory*, Rev. B 03/15. Inspected mirror:

<https://device.report/m/33bc71a4eab1c479cec619ad15d5184198e06218324e8d8d2cb32dd8ab75a8d3>

### Directly supported points

1. The product documents `COPYBACK` as a two-step read/program operation using the device's internal register path.
2. The command is constrained by the device's supported physical movement geometry.
3. For `COPYBACK READ (00h–35h)`, Micron says host data read-out is not required for command execution but recommends reading/verifying the data before `COPYBACK PROGRAM` to prevent propagation of data errors.
4. The copyback-program flow also exposes status checking for operation completion/pass-fail.

### Retention consequence

This product witness keeps two proof obligations separate:

- did the target programming operation complete successfully?
- was the source content independently checked/corrected so latent source errors were not simply propagated?

Case 82 therefore uses **operation success ≠ integrity requalification** as a bounded engineering distinction, not as a claim that status checking is unimportant.

---

## Source 4 — bibliographic continuity witness

US8615700B2, *Forward error correction with parallel error detection for flash memories*, includes in its cited literature:

- Micron, `NAND Flash Design and Use Considerations`, August 2006;
- Micron, `NAND Flash Internal Data Move`, June 2007;
- Micron, `Using COPYBACK Operations in NAND Flash Devices`, October 2008;
- Micron, `Wear-Leveling Techniques in NAND Flash Devices`, October 2008.

Source: <https://patents.google.com/patent/US8615700B2>.

This is used only as a bibliographic/date witness and not as a substitute for Micron's mechanism claims.

---

## Claim matrix

| Claim | Source 1 TN-29-15 | Source 2 TN-29-41 | Source 3 2015 datasheet | Status |
| --- | --- | --- | --- | --- |
| internal page movement exists without ordinary external data transfer | yes | yes | yes | grounded |
| page moves through an internal register/path | yes | compatible | yes | grounded |
| external movement can include ECC correction before reprogramming | yes | yes | recommended integrity path | grounded |
| blind/internal movement can propagate existing errors | explicit worked scenario | explicit warning | explicit propagation warning | grounded |
| repeated unchecked movement can reduce future recoverability | explicit | explicit | compatible | grounded |
| periodic/pre-move integrity checking is recommended | explicit post-READ policy | explicit input/output correction | explicit read/verify recommendation | grounded |
| every later NAND copyback lacks on-die ECC | no | no | no | rejected |
| Micron invented copyback | no | no | no | unsupported |

---

## Cross-case controls

### Case 04 — mapped Flash

Use only for the distinction `logical identity can survive physical relocation`. Case 82 adds `relocation does not automatically renew integrity`. Do not retrofit Micron COPYBACK into the 1993 Ban patent as if they were one historical mechanism.

### Case 36 — NAND Flash Correct-and-Refresh

FCR deliberately uses error correction followed by reprogram/remap to recover retention margin. It is therefore a controlled counterexample to blind internal movement. `COPYBACK` and `FCR` can both move/write data but do not have the same preservation semantics.

### Cases 52 and 59 — read disturb and program interference

Those cases explain mechanisms that can create additional physical error population. Case 82 only needs the weaker relation that **existing errors can be carried forward** when correction is skipped. It does not rename copyback as read disturb or program interference.

### Case 67 — adaptive read-disturb reclaim

A reliability-triggered reclaim policy can choose when relocation is required. Case 82 isolates one possible relocation primitive and its integrity boundary; trigger policy and movement mechanism remain different layers.

### Case 78 — NAND bad-block management

Bad-block replacement decides that one physical block must no longer receive current payload and may require data movement to a reserve. Case 82 asks whether that movement includes correction/requalification. Exclusion authority and payload-integrity renewal are orthogonal.

---

## Findings admitted by this grounding

The evidence is strong enough to support the following bounded findings:

- **internal relocation ≠ external ECC requalification**;
- **new physical location ≠ renewed error-free representation**;
- **source-page error can survive a location change**;
- **correctable error presence ≠ immediate logical failure**;
- **remaining ECC margin can shrink while the logical page remains readable**;
- **page-register transit ≠ final durable destination state**;
- **program-operation success ≠ proof that inherited source errors were corrected**;
- **bus/computation avoidance can also avoid a validation opportunity**;
- **migration policy ≠ migration primitive**;
- **copyback ≠ correct-and-refresh**;
- **copyback ≠ garbage collection or wear leveling, although those policies may use internal movement**;
- **relocation ≠ secure sanitization of the obsolete source**.

---

## Prior-art and terminology boundary

No first-invention claim is made. The case uses Micron's own chronological vocabulary (`IDM`, later `COPYBACK`) because that vocabulary is sufficient to ground the retention distinction. A full copyback genealogy across Toshiba/Samsung/Hynix/Micron and ONFI revisions would be a technical-history task better placed in `computing-archaeology`.

The repository search performed before this slice found no dedicated `copyback` / `internal data move` history in `tmzncty/computing-archaeology`, so no existing companion chapter is duplicated here.

---

## Remaining gaps

- recover a stable official Micron-hosted facsimile of TN-29-41 if one becomes directly accessible;
- compare early vendor-specific copyback restrictions with exact ONFI revision-by-revision optional-command semantics;
- separately study later NAND with on-die ECC or controller-assisted copyback, where the `blind move` boundary may change;
- obtain independent hardware/fault-injection evidence before claiming compliance or failure behavior for named SSDs/controllers;
- keep controller garbage collection and wear-leveling policy histories separate unless a later case specifically needs their scheduling relation.

## Promotion decision

**Case 82 may be marked `grounded`.**

Reason: the central claim does not depend on a speculative controller reconstruction. Micron's own technical note supplies the internal read/register/program path, explicitly states that correction is skipped, illustrates an error following the move, and recommends periodic external checking; the later COPYBACK note and named product documentation independently preserve the same integrity boundary. The remaining gaps concern genealogy, modern variants, and empirical compliance rather than the bounded mechanism.