# Micron NAND Internal Data Move / COPYBACK: Relocation Without Automatic ECC Requalification

## Scope

- **Bounded historical/technical regime:** Micron raw-NAND documentation from the mid-2000s through the mid-2010s, centered on TN-29-15 (`Internal Data Move`) and TN-29-41 (`COPYBACK`), with a later Micron product datasheet as a named-device continuity witness.
- **Primary question:** when NAND data is moved internally from one physical page to another without crossing the external I/O path, what exactly is preserved, and what integrity work is skipped?
- **Retention-specific focus:** page-register-mediated relocation, error carry-forward, ECC requalification opportunities, verification, and the difference between preserving a logical page image and renewing its error margin.
- **Excluded from this case:** a general history of NAND commands, a full FTL/garbage-collection history, wear-leveling algorithms, read-disturb physics, program-interference physics, invention priority for copyback, or modern on-die-ECC copyback implementations.

This slice is deliberately adjacent to Cases 04, 36, 52, 59, 67, and 78. Those cases already cover mapped-Flash identity, correct-and-refresh, read disturb, program interference, adaptive reclaim, and bad-block retirement. Case 82 asks a narrower question that those cases leave open: **does moving a current NAND page to a new physical embodiment necessarily renew the correctness of the information being moved?** In the bounded Micron regime, the answer is no.

---

## Historical vocabulary

The primary sources use terms including:

- `internal data move` / `IDM`;
- `READ FOR INTERNAL DATA MOVE`;
- `PROGRAM FOR INTERNAL DATA MOVE`;
- `COPYBACK` / `COPYBACK READ` / `COPYBACK PROGRAM`;
- `cache register` / `page register`;
- `error correction` / `ECC`;
- `post-READ`;
- `data integrity`;
- `block management`;
- `wear leveling`.

The following are **project engineering terms**, not historical quotations from Micron:

- `integrity requalification`;
- `error-debt carry-forward`;
- `relocation-without-renewal`;
- `validation opportunity`;
- `physical re-embodiment`.

They are used only to compare the documented mechanism with other retention regimes.

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

### H/P — the internal path deliberately removes the ordinary ECC opportunity

TN-29-15 makes the integrity consequence explicit. Because the data move remains internal, there is **no opportunity to perform error correction** on the moved page through the ordinary external controller path. The note warns that excessive internal data moves without periodic checks can allow errors to accumulate and reduce system reliability.

Its worked error scenario is especially important. A page already containing a possible bit error is moved from the array into the cache register; the error follows the move. The page is then programmed to the new physical location; because no external correction occurred, the error follows again. A later independent error can leave the page beyond the correction capability available when it is finally read.

The historical mechanism therefore supports a strict distinction:

> moving the page image successfully is not the same operation as restoring the page image to the intended error-free value.

### H/P — Micron recommends explicit integrity checks around repeated IDM

TN-29-15 does not treat the limitation as a reason to abandon internal relocation. It recommends system-level techniques that bound the risk, including robust multibit ECC and periodic `post-READ` integrity checks. The optimum checking frequency is explicitly made dependent on the required correction level and the number of internal moves.

This matters because it converts a performance optimization into a retention-policy problem. The controller can trade some bus/computation work away, but doing so changes how long it may safely defer an integrity-requalification opportunity.

### H/P — TN-29-41 reframes the same issue under `COPYBACK` vocabulary

Micron's October 2008 TN-29-41, *Using COPYBACK Operations to Maintain Data Integrity in NAND Flash Devices*, states that NAND systems require ECC for normal program/read error protection and warns that using COPYBACK without external data output/input can let error counts move beyond ECC protection limits.

The note's key corrective relation is the opposite path: outputting the data, correcting it, and returning the corrected representation can restore the programmed value and return the ECC budget toward its maximum correction capability. In other words, the external path is not merely slower transport. It can be an **integrity-renewal boundary**.

**Primary source:** Micron Technology, *TN-29-41: Using COPYBACK Operations to Maintain Data Integrity in NAND Flash Devices*, October 2008. Historical Micron path cited in contemporary literature: <http://download.micron.com/pdf/technotes/nand/tn2941_idm_copyback.pdf>. A later Micron media path is preserved in a USPTO-filed exhibit citation: <https://media-www.micron.com/-/media/client/global/documents/products/technical-note/nand-flash/tn2941_idm_copyback.pdf?rev=c0a04e8ff8bd4f309bab7ea91ad98035>. A text-indexed USPTO PTAB exhibit reproducing the note is available through the PTAB public-document system.

### H/P — later Micron product documentation keeps the command/integrity split visible

A 2015 Micron automotive asynchronous-NAND datasheet documents `COPYBACK READ (00h-35h)` and `COPYBACK PROGRAM (85h-10h)` as page-register-mediated movement within the supported physical scope. It then gives a revealing recommendation: although host read-out is not required to execute COPYBACK, the host is advised to read and verify the data before COPYBACK PROGRAM to prevent propagation of data errors.

The same product documentation also has the host check operation status after programming. These are two different questions:

1. did the NAND programming operation complete successfully according to the device status path?
2. was the page content independently requalified/corrected before being propagated?

A command can answer the first without automatically answering the second.

**Primary product witness:** Micron, *8Gb Automotive Async NAND Flash Memory*, Rev. B, March 2015, `Copyback Operations` / `COPYBACK READ`, mirrored at <https://device.report/m/33bc71a4eab1c479cec619ad15d5184198e06218324e8d8d2cb32dd8ab75a8d3>.

---

## Retained state

At least five distinct states or relations matter in this bounded case.

### 1. Logical payload

The value the storage system intends to preserve across physical relocation.

### 2. Raw physical page image

The bits recovered from the source NAND page before higher-level ECC correction. In the bounded internal-move path, already-present errors can travel with this image.

### 3. Temporary page/cache-register state

The source page is temporarily embodied in an internal register between the read-for-move and program-for-move phases. This state is neither the long-term source embodiment nor yet the durable destination embodiment.

### 4. ECC / integrity relation

The ability of the system's error-correction path to identify and correct a bounded error population. The ECC budget is not the payload itself, yet how much of that budget has already been consumed affects future recoverability.

### 5. Relocation / mapping state

At a higher layer, the system must know which physical page now embodies the current logical data after block management, wear leveling, reclamation, or replacement. Case 82 does not reconstruct a full FTL; it only notes that physical movement becomes useful to a logical store because some higher-level relation later resolves to the destination.

---

## Read, move, verify, and rewrite semantics

### Ordinary external read/correct/reprogram path

The controller obtains the page through the external interface, applies its ECC/error-processing path, and can program a corrected representation into the destination.

This path couples **movement** with an opportunity for **requalification and correction**.

### Internal data move / COPYBACK path

The NAND device reads the source page into an internal register and programs that register into a destination page without requiring ordinary external data transfer.

This path couples **movement** with **bus avoidance**, but in the bounded Micron documentation it does not automatically couple movement with controller-side ECC correction.

### Post-READ / explicit output path

Micron recommends periodic or pre-program read-out/checking when integrity risk requires it. This introduces a separate maintenance operation whose schedule can depend on accumulated internal moves and the error-correction budget.

### Program status / completion

The destination programming path exposes operation status. That status is evidence about the programming operation's completion/pass-fail condition, not a substitute for an end-to-end proof that the page was first restored to its intended error-free logical value.

---

## Engineering reconstruction

### E — relocation and renewal are separate retention operations

A page can move from one physical NAND location to another while preserving its current raw image, including already-present correctable errors. Physical re-embodiment therefore does not entail integrity renewal.

### E — a performance optimization can remove a preservation opportunity

The speed/power advantage of IDM comes partly from avoiding the external path. But that same external path is where the bounded system performs ordinary ECC correction. Removing transport work can therefore also remove a corrective checkpoint.

### E — error margin can be a consumable continuation resource

A page can remain logically recoverable while already containing errors inside ECC capability. Carrying those errors forward does not necessarily cause immediate data loss, but it leaves less correction margin for later retention errors, read disturb, program interference, or other faults.

This does **not** mean the ECC code itself is consumed like a battery. The project term `error budget` refers to remaining correctable margin under the bounded code/error model.

### E — temporary internal state is part of a retention handoff

During COPYBACK/IDM, the page register holds the page between old and new NAND embodiments. Successful persistence across the move requires the handoff to progress from source array state, through temporary register state, to a programmed destination. The register is therefore retention infrastructure even though it is not the intended long-term home.

### E — correctness authority and location authority can diverge

A higher-level mapping layer may correctly designate the newly programmed page as the current physical location while the page image still carries correctable errors from the prior embodiment. `where the current page is` and `how much integrity margin the current page has` are separate state relations.

---

## Functional comparisons — not genealogy

### A — Case 04, mapped Flash

Case 04 grounds stable logical identity across out-of-place Flash relocation and reclamation. Case 82 adds a lower-level warning: **a successful location transition does not by itself requalify the information moved**. Mapping currentness and payload-integrity currentness are different relations.

### A — Case 36, NAND Flash Correct-and-Refresh

Case 36 explicitly uses read + ECC correction + rewrite/remap to renew aging NAND before errors exceed correction capacity. Case 82 provides the counterexample path: internal movement can relocate the page while skipping the correction step. Therefore:

> `relocation ≠ refresh` and `copyback ≠ correct-and-refresh`.

### A — Cases 52, 59, and 67

Read disturb and program interference can create or enlarge physical error populations; adaptive reclaim can move data after reliability evidence crosses a policy threshold. Case 82 does not claim COPYBACK causes those mechanisms. It shows instead that **whatever correctable error population already exists can be propagated if movement bypasses correction**.

### A — Case 78, bad-block replacement

Case 78 shows that failure-triggered retirement can require moving current payload to a reserve block while retaining the exclusion/replacement relation. Case 82 adds an orthogonal audit question for any such movement: was the page merely copied, or was it externally checked/corrected before the destination became current?

---

## Philosophical interpretation — bounded

### I — migration can preserve error debt as well as value

A common abstract description of technical preservation says that a value survives because it is repeatedly moved to new carriers. Case 82 makes that statement more exact and less comforting. **Migration can preserve the intended logical value while also carrying forward imperfections that reduce future recoverability.** Re-embodiment is not automatically rejuvenation.

This is a retention-specific philosophical observation, not a historical claim that Micron engineers formulated `error debt` as a philosophical concept.

---

## Counterexamples and limits

- The case does not establish who invented NAND copyback/internal data move.
- `IDM` and `COPYBACK` are treated as documented Micron command/feature vocabulary in the bounded sources, not as proof that every vendor or standards revision used identical wording or restrictions.
- The exact source/destination plane, odd/even, die, or LUN restrictions vary by device generation; they are not generalized into one universal NAND geometry.
- The case does not claim every later NAND lacks internal ECC. Modern managed or on-die-ECC devices may compose copyback with different integrity machinery.
- An internal move carrying a correctable source error does not imply immediate user-visible corruption. Failure occurs when the relevant error population exceeds the available correction/recovery path.
- Program-status success is not described as worthless; it answers a different operational question from end-to-end content requalification.
- The case does not prove that every garbage-collection or wear-leveling implementation uses NAND-native COPYBACK. Controllers can use external read/correct/program paths or other internal primitives.
- A later physical rewrite can change charge distributions and therefore physical condition, but that does not erase the distinction between copying an already-wrong logical bit pattern and correcting it before rewrite.
- Secure sanitization is outside scope. Moving or rewriting a current page says nothing by itself about physical erasure of the obsolete source embodiment.

---

## Prior-art boundary

This case makes **no invention-priority claim** for internal NAND page movement, copyback commands, page registers, or ECC-aware relocation.

The defensible historical statement is narrower:

> By Micron's mid-2000s technical documentation, NAND internal data move was explicitly presented as a faster alternative to an external read/correct/reprogram path, and Micron explicitly warned that bypassing that external path also bypassed an ECC opportunity so existing errors could follow the page into its new physical location. By the 2008 COPYBACK note and later product documentation, the integrity consequence remained explicit enough that external read/check/correction was recommended when reliability required renewed confidence.

The companion `tmzncty/computing-archaeology` repository was searched for a dedicated NAND copyback/internal-data-move slice before writing this case; none was found. A broader NAND command-set genealogy or vendor-comparison history belongs there rather than being recreated here.

---

## Claim ledger

| Claim | Type | Evidence status |
| --- | --- | --- |
| Micron documents an internal page-move path through an internal register | H/P | grounded in TN-29-15 and later product documentation |
| the documented internal path avoids ordinary external data transfer | H/P | grounded |
| the ordinary external movement path can include error correction before reprogramming | H/P | grounded in TN-29-15 |
| Micron warns that IDM/COPYBACK without external checking can propagate/accumulate errors | H/P | grounded in TN-29-15, TN-29-41, and later product documentation |
| Micron recommends ECC plus periodic/post-read or pre-copyback verification according to integrity needs | H/P | grounded in the bounded notes/product witness |
| physical relocation ≠ integrity requalification | E | direct reconstruction from the two documented paths |
| mapping/location currentness ≠ integrity margin | E | bounded cross-layer reconstruction |
| correctable error presence ≠ immediate logical failure | E | bounded by the ECC model described in the sources |
| COPYBACK operation completion ≠ proof that source errors were corrected before propagation | E | grounded reconstruction from status versus verification paths |
| COPYBACK ≠ Correct-and-Refresh | E/A | functional comparison with Case 36; no genealogy claim |
| COPYBACK ≠ read-disturb/program-interference mechanism | E/A | functional boundary with Cases 52/59 |
| internal relocation can participate in block management/wear leveling without being identical to either policy | H/E | grounded by Micron's documented use framing; policy distinction retained |
| migration can carry forward reduced recovery margin as well as logical value | I/E | bounded interpretation |
| Micron invented NAND copyback | X | not established |
| every later NAND copyback bypasses all internal ECC | X | explicitly not claimed |

---

## Sources

### Primary / manufacturer

- Micron Technology, **TN-29-15: NAND Flash Performance Improvement Using Internal Data Move / NAND Flash Internal Data Move**, historical note, Rev. C text mirror: <https://doczz.net/doc/7838214/tn-29-15--nand-flash-performance-improvement-using-internal>.
- Micron Technology, **TN-29-41: Using COPYBACK Operations to Maintain Data Integrity in NAND Flash Devices**, October 2008. Historical publication URL: <http://download.micron.com/pdf/technotes/nand/tn2941_idm_copyback.pdf>; later Micron media URL preserved in PTAB filings: <https://media-www.micron.com/-/media/client/global/documents/products/technical-note/nand-flash/tn2941_idm_copyback.pdf?rev=c0a04e8ff8bd4f309bab7ea91ad98035>.
- Micron Technology, **8Gb Automotive Async NAND Flash Memory**, Rev. B, March 2015, `Copyback Operations`: <https://device.report/m/33bc71a4eab1c479cec619ad15d5184198e06218324e8d8d2cb32dd8ab75a8d3>.

### Archival / bibliographic witnesses

- USPTO/PTAB-filed exhibit text indexing TN-29-41 and its Micron URL: <https://ptacts.uspto.gov/ptacts/public-informations/petitions/1548389/download-documents?artifactId=k_hzx8onBUrJmXs4ydnz0x7FURiK9RcPBIhGTYM1s_H-dcHGTdvdgUo>.
- US8615700B2 bibliography records Micron TN-29-15 (June 2007), TN-29-41 (October 2008), and TN-29-42 as contemporaneous NAND technical notes: <https://patents.google.com/patent/US8615700B2>.

---

## Status

**`grounded`** — the central mechanism and error-propagation boundary are supported by manufacturer-primary technical documentation plus a later named-product witness. Open work is deliberately narrower: recover an official directly downloadable archival copy of TN-29-41 if convenient; build a broader cross-vendor/ONFI copyback genealogy in `computing-archaeology`; inspect modern on-die-ECC copyback variants separately; and seek independent fault-injection measurements before making product-compliance claims.