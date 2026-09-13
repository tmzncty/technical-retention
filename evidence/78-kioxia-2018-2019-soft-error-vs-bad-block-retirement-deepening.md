# Case 78 deepening — KIOXIA 2018–2019 soft-error handling versus bad-block retirement

**Status:** `bounded deepening complete`

## Why this slice exists

Case 78 already grounds a strong negative-retention relation from ONFI, Micron, and Linux MTD: a NAND block can remain physically addressable while retained defect evidence says it must no longer count as an admissible storage target. The case also grounds the danger of erasing an original bad-block marker before its exclusion meaning has been captured elsewhere.

What remained too easy to blur was the **classification boundary before retirement**. NAND reliability literature contains many error-producing mechanisms — retention loss, read disturb, random bit errors, program failure, erase failure — but not every observed bit error authorizes the same response. A correctable read error can call for ECC and rewrite while a program/erase status failure can call for block replacement and future exclusion.

KIOXIA's TH58NYG3S0HBAI6 product datasheet is unusually useful because one manufacturer document places all of those paths next to one another:

- initial bad-block detection and a prohibition on erasing detected bad blocks;
- program/erase failure leading to block replacement;
- ordinary read-bit-error handling through ECC and rewrite;
- retention and read-disturb errors that may become usable again after erase/reprogram;
- host-side NAND management that keeps bad-block management, ECC treatment, and wear leveling distinct.

This lets the repository close a narrow but important seam:

> **error evidence is not automatically exclusion authority. The maintenance action depends on the class of evidence and on which future use remains admissible.**

The slice is deliberately product- and revision-bounded. It is not a general NAND reliability history and does not claim that KIOXIA invented any of the mechanisms below.

---

## Source and chronology discipline

### Primary source

KIOXIA Corporation, **TH58NYG3S0HBAI6, 8 Gbit (1G × 8 bit) CMOS NAND E2PROM**, Rev. 2.00, document date `2019-10-01C`:

<https://americas.kioxia.com/content/dam/kioxia/newidr/productinfo/datasheet/201910/DST_TH58NYG3S0HBAI6-TDE_EN_31567.pdf>

Relevant document pages:

- p. 4 — valid-block count and lifetime applicability;
- p. 61 — `(13) Invalid blocks (bad blocks)`;
- p. 62 — `(14) Failure phenomena for Program, Erase and Read operations`;
- p. 63 — `(17) Reliability Guidance`;
- p. 64 — `(18) NAND Management`;
- p. 66 — revision history.

### Revision-history boundary

The document's own revision history says:

- `2013-08-01`, Rev. 0.10 — preliminary version;
- `2013-09-20`, Rev. 1.00;
- `2018-12-14`, Rev. 1.10 — among other changes, **“Renewed Reliability Guidance and added NAND Management”**;
- `2019-10-01`, Rev. 2.00 — **“Rebrand as KIOXIA.”**

Therefore this evidence treats the exact `Reliability Guidance` / `NAND Management` wording inspected here conservatively as a **2018–2019 public-product-document witness**. It does not silently back-project those exact sections to the 2013 preliminary revision.

The product family itself is older than 2018; the bounded historical statement here concerns the surviving revision and its explicit reliability classification.

---

## Historical / primary record

### H/P — the product does not promise a pristine block population

The datasheet specifies `4016` minimum valid blocks and `4096` maximum valid blocks, says the device may contain unusable blocks, guarantees Block 0 valid at shipment, and states that the minimum-valid-block specification applies **over lifetime**.

This is a product-level reminder that a NAND device's usable physical set is not identical to its nominal addressable geometry.

Bounded relation:

```text
nominal block-address range
    !=
all blocks guaranteed admissible for the whole service life
```

The document does not by this statement alone say which individual blocks will later fail or when.

### H/P — detected bad blocks carry an exclusion rule, and erasing them can destroy the evidence

Application Note `(13) Invalid blocks (bad blocks)` instructs the system not to perform erase operations on bad blocks because the bad-block information may become impossible to recover if erased. It tells the host to check for bad blocks after installation and to manage detected bad blocks as unusable.

For this product the bad-block mark is described as existing in whole pages; the prescribed test reads one column from a page in each block and treats `00h` as the bad-block indication. The flow chart repeats that no erase operation is allowed on a detected bad block.

This independently corroborates the core Case-78 relation already grounded from Micron:

```text
bad-block information erased
    !=
underlying block reliability repaired
```

and:

```text
physical block still selectable
    !=
block authorized for future allocation
```

The KIOXIA marker geometry is product-specific and must not be substituted for Micron's or ONFI's device-specific marker locations.

### H/P — program/erase failure and read-bit error lead to different prescribed response classes

Application Note `(14) Failure phenomena for Program, Erase and Read operations` gives a compact three-way table:

- **Block Erase Failure** — detect by Status Read after erase → **Block Replacement**;
- **Page Programming Failure** — detect by Status Read after program → **Block Replacement**;
- **Read Bit Error** — inspect ECC status at the host controller and take measures such as **rewrite**, considering wear leveling, before an uncorrectable ECC error occurs.

The same page then says that after an erase error the system should prevent future accesses to the bad block, for example by creating a table or using another appropriate scheme. Its replacement diagram shows data from the failing Block A being reprogrammed into another Block B through an external buffer and future accesses to Block A being prevented.

The historical source therefore does **not** collapse every error into one `bad` state. It exposes at least two response classes:

```text
read bit error
    -> ECC observation / correction context
    -> rewrite may be appropriate

program or erase status failure
    -> replacement of the block
    -> future access to failed block prevented
```

The source does not claim those are the only NAND failure classes, and the repository does not turn the table into a universal NAND state machine.

### H/P — random bit error does not necessarily make a block bad

The `Reliability Guidance` section states explicitly that random bit errors can occur during use and that this **does not necessarily mean that a block is bad**. It then says that, generally, a block should be marked bad when a **program status failure or erase status failure** is detected.

This is the central negative control for this slice:

> **observed bit error != automatic bad-block retirement.**

The word `generally` matters. This is product guidance, not a proof that every possible block-retirement decision in every controller is triggered only by those two status bits.

### H/P — retention/read-disturb degradation can be recoverable without turning the block into a permanently retired block

The same `Reliability Guidance` distinguishes two error-producing mechanisms from program/erase-failure retirement.

For **data retention**, the document says stored data may change over time because of charge loss or charge gain, and states that after block erase and reprogramming **the block may become usable again**. It also says retention time depends on P/E cycling and temperature.

For **read disturb**, it explains that repeated reads can cause charge gain and soft-program neighboring cells, and again says that after block erase and reprogramming **the block may become usable again**.

This wording is important precisely because it appears beside the bad-block guidance. It supports:

```text
retention/read-disturb error state
    !=
necessarily permanent block exclusion
```

It does **not** support:

```text
bad block erased and reprogrammed
    -> repaired bad block
```

The latter would directly contradict the separate instruction not to erase detected bad blocks and would erase a distinction that the manufacturer document itself preserves.

### H/P — host-side NAND management keeps ECC treatment, bad-block management, and wear leveling distinct

The following `NAND Management` section says that system design should incorporate, among other things:

- Bad Block Management;
- ECC treatment;
- Wear Leveling.

It separately says ECC treatment is mandatory against random bit errors and that the host should monitor ECC status and take measures such as rewrite before an uncorrectable error occurs.

This is useful as a vocabulary boundary:

```text
ECC treatment != bad-block management != wear leveling
```

The three may interact in one storage stack, but co-presence does not make them one operation or one retained state.

---

## Engineering reconstruction

### E — error observation and allocation authority are different states

A bit error is evidence about the currently read payload/physical state. A bad-block entry is a stronger operational decision about whether that physical block may continue to serve as a target.

The KIOXIA table makes this separation visible because a read-bit error can remain on the **correct / rewrite** path while a program/erase failure moves the block onto a **replace / prevent-future-access** path.

Therefore:

```text
error detected
    !=
block retired
```

and:

```text
correctability evidence
    !=
allocation admissibility evidence
```

A system can know that data need maintenance without yet deciding that the carrier must never be used again.

### E — maintenance and retirement are two different responses to degrading media

The same underlying NAND medium supports at least two broad continuation strategies in the bounded product documentation:

1. **maintain a still-admissible carrier** — use ECC/rewrite to restore margin before errors become uncorrectable;
2. **retire an inadmissible carrier** — move current data elsewhere and retain an exclusion relation so future operations avoid the failed block.

This gives a useful project-level contrast:

```text
repair/refresh current embodiment
    !=
replace embodiment and retain exclusion state
```

Neither response is equivalent to secure deletion.

### E — the same erase/reprogram primitive can have opposite governance depending on classification

The product document produces an especially sharp control boundary:

- in the retention/read-disturb discussion, erase plus reprogram can make the block usable again;
- in the detected-bad-block discussion, erase is prohibited because it can destroy the bad-block information needed to preserve exclusion.

Thus the operation cannot be interpreted independently of its control state:

```text
erase + reprogram on maintenance-eligible block
    -> may restore usable margin

erase on detected bad block
    -> may destroy exclusion evidence
```

This is not a contradiction. The two actions apply to differently classified carriers.

It also means that `erase` is not semantically identical across the repository:

- Case 04 uses erase as part of Flash reclamation;
- Case 36 can use remap/reprogram as retention maintenance;
- Case 52 uses relocation/erase to reset accumulated read-disturb exposure;
- Case 78 warns that erasing the **evidence-bearing bad block** can be precisely the wrong action.

### E — block retirement is a retained future-use rule, not a description of every bit

Once program/erase failure triggers block replacement and future access prevention, the important retained state is not simply “an error happened.” The system needs a future-use relation equivalent to:

```text
Block A -> do not allocate/use as ordinary storage target
```

That relation can remain necessary even if some pages in Block A are readable or some current payload was successfully copied away.

Therefore:

```text
some data recoverable from carrier
    !=
carrier remains admissible for future allocation
```

and the converse:

```text
read bit error observed
    !=
carrier already proved permanently inadmissible
```

---

## Functional comparisons — not genealogy

### A — Case 36, NAND Flash Correct-and-Refresh

Case 36 studies a 2012 research regime in which accumulated retention errors are periodically read, ECC-corrected, and refreshed/remapped before correction margin is exhausted. The KIOXIA product documentation supplies a later manufacturer-side control: random/read errors can call for ECC and rewrite without automatically becoming `bad block` retirement.

The useful functional relation is:

```text
error-margin maintenance
    !=
block-exclusion authority
```

No KIOXIA implementation of Cai et al.'s FCR algorithm is claimed.

### A — Case 52, NAND read disturb

Case 52 grounds that repeated reads can alter neighboring NAND state and that read-count/error evidence can motivate relocation or mitigation. KIOXIA's product guidance independently says read disturb may produce bit errors and that erase/reprogram can make the block usable again.

The comparison closes a semantic trap:

```text
read-disturb damage
    !=
automatically a lifetime-developed bad block
```

Again, no direct Fujitsu/TMS/Cai → KIOXIA genealogy is asserted.

### A — Case 78's Micron witness

Micron's Case-78 evidence emphasizes preservation of an erasable manufacturer defect mark, construction of a BBT, and replacement of lifetime bad blocks. KIOXIA adds a different slice: how the manufacturer distinguishes **soft/read error handling** from **block-retirement evidence**.

The two sources agree at the functional level that program/erase failure can produce replacement/exclusion work, but they are not used to infer identical marker geometry, ECC policy, reserve topology, or firmware/software implementation.

### A — Case 14, SCSI grown-defect reassignment

Case 14 likewise separates a still-addressable logical designation from the physical sector that is retired after a grown defect. The analogy is only the future-use rule plus replacement relation. NAND's ECC/rewrite/bad-block-marker regime has different media physics and control state.

---

## Historical versus engineering versus interpretation boundary

### Historical record

The manufacturer directly states the bad-block erase prohibition, the program/erase-failure replacement response, the read-bit-error ECC/rewrite response, the `random bit error != necessarily bad block` distinction, and the retention/read-disturb erase/reprogram recovery possibility.

### Engineering reconstruction

The repository describes these statements as a separation among:

- **error observation**;
- **maintenance eligibility**;
- **allocation admissibility**;
- **retirement / exclusion authority**.

Those four labels are project analytical terms, not claimed as KIOXIA's formal state-machine vocabulary.

### Functional analogy

Comparisons to Cases 14, 36, and 52 are mechanism-level comparisons only. No historical descent is inferred from shared operations such as rewrite, remap, or block replacement.

### Philosophical interpretation

A bounded observation follows: **preserving a storage service sometimes requires preserving not merely data and mappings, but the classification rules that decide whether an error should be corrected in place or whether a carrier should cease to count as usable.**

This is a project interpretation. It does not turn `bad`, `error`, or `usable` into philosophical categories, and it does not claim that the manufacturer intended such an interpretation.

---

## Explicit non-claims

This evidence does **not** establish that:

1. KIOXIA/Toshiba invented NAND bad-block management, read-disturb recovery, ECC rewrite, or wear leveling;
2. the exact 2018–2019 reliability text was present in the 2013 preliminary datasheet;
3. every random bit error should always be handled without block retirement;
4. program/erase status failure is the only possible reason any controller may ever retire a block;
5. every retention or read-disturb error can be repaired successfully by erase/reprogram;
6. a block already classified as bad becomes good if its bad-block marker is erased;
7. the KIOXIA marker location/geometry is universal across NAND vendors or generations;
8. ECC correction, rewrite, wear leveling, garbage collection, and bad-block management are one algorithm;
9. KIOXIA implements the 2012 FCR or 2015 RDR research algorithms;
10. the datasheet exposes the complete factory qualification procedure or the hidden reason each shipped block was marked bad;
11. block replacement implies secure sanitization of the retired block;
12. data copied out of a failing block prove that the block is safe for future writes;
13. the `4016`-block minimum is a universal NAND reserve ratio;
14. the host-visible table described as an example is the only possible implementation of future-access prevention.

---

## Claim ledger

| Claim | Type | Status |
| --- | --- | --- |
| TH58NYG3S0HBAI6 guarantees 4016–4096 valid blocks, with the minimum applicable over lifetime | H/P | grounded in 2019 Rev. 2.00 datasheet |
| detected bad blocks must be managed unusable and must not be erased because bad-block information may become unrecoverable | H/P | grounded |
| program/erase status failure leads to block replacement in the product guidance | H/P | grounded |
| read-bit error leads to ECC-status handling / possible rewrite rather than automatic block replacement | H/P | grounded |
| random bit error does not necessarily mean the block is bad | H/P | explicit manufacturer statement |
| retention/read-disturb degradation may become usable again after erase/reprogram | H/P | explicit manufacturer statement, bounded to those sections |
| exact Reliability Guidance / NAND Management wording is safely dated to 2018–2019 rather than silently to 2013 | H/P/E | grounded by document revision history + conservative chronology |
| error observation != block retirement authority | E | reconstruction from distinct manufacturer response paths |
| erase/reprogram can be maintenance for one classified block while erase is prohibited for an already-detected bad block | E | bounded reconstruction from adjacent application notes |
| correctable error == permanent physical defect | X | rejected |
| erased bad-block marker == repaired block | X | rejected |
| KIOXIA uses FCR/RDR exactly | X | unsupported |

---

## What this closes in Case 78

This deepening closes a bounded classification debt:

- a second manufacturer product document independently corroborates that bad-block information is exclusion-critical and should not be erased;
- the same document shows that **read-bit errors and program/erase failures do not automatically carry the same future-use authority**;
- it provides a direct product-level negative control against treating retention/read-disturb bit errors as synonymous with bad-block retirement;
- it shows that erase/reprogram can be restorative in one degradation class while erase can be evidence-destroying in the retired-block class.

It does **not** close broader cross-vendor statistics or controller behavior.

---

## Remaining evidence debt

Useful next steps are narrower than another general NAND reliability survey:

1. recover a directly inspectable Toshiba-branded Rev. 1.10 (14 December 2018) or earlier revision of this product datasheet to pin the exact text transition before the KIOXIA rebrand;
2. add a contemporaneous second-vendor raw-NAND product witness that explicitly distinguishes ECC-correctable/read-disturb handling from block retirement, rather than merely repeating a generic bad-block rule;
3. obtain fault-injection or controller traces showing the actual transition from repeated read/ECC evidence to rewrite versus permanent BBT insertion;
4. distinguish any vendor-specific thresholds for proactive retirement from the datasheet's general `program/erase status failure` rule;
5. keep managed-SSD hidden-media retirement separate unless a controller interface exposes equivalent evidence.

Broader NAND reliability and controller genealogy belongs primarily in `tmzncty/computing-archaeology`; a fresh repository search found no existing TH58NYG3S0HBAI6 / KIOXIA reliability-guidance slice to reuse.

---

## Source

KIOXIA Corporation, **TH58NYG3S0HBAI6, 8 Gbit (1G × 8 bit) CMOS NAND E2PROM**, Rev. 2.00, `2019-10-01C`, especially pp. 4, 61–64, and revision history p. 66:

<https://americas.kioxia.com/content/dam/kioxia/newidr/productinfo/datasheet/201910/DST_TH58NYG3S0HBAI6-TDE_EN_31567.pdf>
