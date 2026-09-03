# Case 39 Grounding Record — GeckoFTL Power-Failure Metadata Recovery

## Purpose

This record supports [`cases/39-geckoftl-power-failure-metadata-recovery.md`](../cases/39-geckoftl-power-failure-metadata-recovery.md).

The bounded grounding question is:

> Can a later Flash-translation-layer case directly establish that nonvolatile user pages are not sufficient for restart, because volatile mapping/validity state must be reconstructed from persistent metadata, checkpoints, completion witnesses, and still-preserved older structures before normal operation safely resumes?

**Result: yes.** Dayan, Bonnet, and Idreos's peer-reviewed 2016 GeckoFTL paper explicitly makes power-failure recovery time and metadata placement a scalability problem. Bonnet and Dayan's 2016-filed patent application gives the detailed recovery mechanism, including SRAM-state reconstruction, checkpoint-bounded dirty mappings, completed-run qualification, and recovery of volatile invalid-page knowledge.

The case is therefore `grounded` for this **research-system controller-metadata recovery regime**.

It remains explicitly **not grounded** for commercial GeckoFTL deployment, universal SSD recovery semantics, independent named-controller compliance, application/filesystem transaction durability, or invention priority for FTL crash recovery.

---

## Source set and evidence classes

### Source A — Dayan, Bonnet, Idreos, _GeckoFTL_, ACM SIGMOD 2016

**Document:** Niv Dayan, Philippe Bonnet, Stratos Idreos, _GeckoFTL: Scalable Flash Translation Techniques For Very Large Flash Devices_, Proceedings of the 2016 International Conference on Management of Data, pp. 327–342, DOI `10.1145/2882903.2915219`.

**Publication date:** 26 June 2016 in the University of Copenhagen publication record.

**Evidence class:** `H/P/S` — peer-reviewed contemporary research paper; institutional records preserve the paper's abstract, venue, pages, DOI, and explicit evaluation boundary.

**Institutional records:**

- <https://researchprofiles.ku.dk/en/publications/geckoftl-scalable-flash-translation-techniques-for-very-large-fla-2/>
- <https://pure.itu.dk/en/publications/geckoftl-scalable-flash-translation-techniques-for-very-large-fla/>

#### Source A — metadata scale and recovery-time problem

The published abstract directly establishes:

- FTL metadata volume grows with Flash-device capacity;
- integrated RAM is the desirable low-latency location but becomes a scaling constraint;
- power-failure recovery time is proportional to metadata size and is becoming impractical at the scale the paper targets;
- persisting more metadata in Flash increases internal I/O and can harm performance and device lifetime.

**Use in this case:** establishes that controller metadata placement and restart recovery are explicit engineering constraints, rather than modern philosophical reconstruction imposed on an unrelated Flash paper.

#### Source A — PVB as the bottleneck in the evaluated design

The abstract directly establishes:

- `Page Validity Bitmap (PVB)` records which physical pages are invalid for garbage collection;
- PVB constitutes 95% of RAM-resident FTL metadata **in the evaluated setup**;
- recovering PVB after power failure accounts for a significant part of recovery time;
- GeckoFTL replaces PVB with `Logarithmic Gecko`, which logs page-validity updates and later reorganizes them.

**Boundary:** the 95% figure is not promoted to a universal property of FTLs or SSDs.

#### Source A — evaluation class

The institutional abstract explicitly says the paper demonstrates results **analytically and empirically through simulation**. It reports, relative to the stated Flash-PVB baseline:

- 95% lower space requirements;
- at least 51% lower recovery time;
- 98% lower contribution to internal I/O overheads.

**Boundary:** these are research-evaluation results, not field measurements from a commercial SSD fleet and not a product guarantee.

---

### Source B — Bonnet and Dayan, `US20170249257A1`

**Document:** Philippe Bonnet and Niv Dayan, _Solid-state storage device flash translation layer_, U.S. patent application `US20170249257A1` / `US2017249257 (A1)`.

**Filing date:** 29 February 2016.

**Publication date:** 31 August 2017.

**Institutional patent record:** IT University of Copenhagen: <https://pure.itu.dk/en/publications/solid-state-storage-device-flash-translation-layer/>.

**Paragraph-level public transcription:** <https://uspto.report/patent/app/20170249257>.

**Evidence class:** `H/P` for the published patent/application mechanism; the institutional record anchors authorship, dates, application identity, and the RAM/Flash LSM mapping-table architecture. Paragraph locators below use the public transcription of that application.

#### Source B, ¶¶0026–0028 — Flash-resident page-validity metadata and reverse mapping

Directly establishes:

- the application incorporates the authors' 2015 Logarithmic Gecko paper by reference;
- Logarithmic Gecko stores PVB in Flash as an LSM tree;
- its runs map block IDs to invalid-page bitmaps;
- the FTL informs Logarithmic Gecko of the physical address of an older page version when a dirty mapping is evicted;
- a Flash-resident reverse map tracks logical pages last written on each physical block.

**Use:** grounds the split between nonvolatile payload and nonvolatile/reconstructible controller relations used for validity and garbage collection.

#### Source B, ¶¶0029–0031 — recovery target and bounded dirty state

The section `3.4 Recovery from Power Failure` directly establishes:

- fast recovery is stated as an FTL requirement;
- the recovery goal is to restore `SRAM-resident metadata` so normal operation can resume;
- one OOB area per block is scanned to determine Flash-block types;
- SRAM structures such as GMD are reconstructed;
- mappings that were dirty at power failure are recreated in cache;
- checkpoints are taken every `C` data-page updates so a mapping cannot remain dirty beyond the bounded interval;
- the source gives an asymptotic recovery-I/O model in terms of block count `K`, cache capacity `C`, and Logarithmic Gecko reporting cost.

**Use:** directly supports `payload survival ≠ immediate restart availability`, because the source itself defines normal-operation resumption as following SRAM metadata restoration.

**Boundary:** “ideally no longer than a few seconds” is the authors' stated design target, not a universal SSD standard.

#### Source B, ¶¶0142–0144 — completed-run qualification during recovery

The section `5.7 Recovery from Power Failure` directly establishes:

- LSM-FTL adapts the earlier recovery algorithm;
- runs receive unique IDs and completion/reconstruction metadata;
- the first page includes a preamble;
- the last page includes a postamble and run-directory copy;
- recovery discards a run without a postamble because it is only partially written;
- obsolete runs are also identified/discarded;
- run directories for valid runs are recovered into SRAM.

**Use:** grounds the distinction `physical survival ≠ recovery admissibility` for controller metadata.

#### Source B, ¶¶0145–0147 — live data can become inaccessible if a volatile mapping relation disappears

The application describes a concrete interruption sequence:

- a mapping entry for an updated logical page exists in cache;
- after enough activity, it is evicted and enters the LSM-tree buffer;
- power fails before that mapping entry is written to Flash;
- the data page may exist, but the mapping entry can be lost;
- the source explicitly says the updated data page can become inaccessible;
- the checkpoint period is reduced so an entry present in the LSM-tree buffer at failure can be recovered to cache.

**Use:** this is the central grounding for `payload embodiment survival ≠ recoverable logical identity`.

#### Source B, ¶¶0148–0149 and surrounding text — volatile invalid-page knowledge and delayed erase

Directly establishes:

- power failure loses Logarithmic Gecko's LSM-tree buffer;
- that buffer includes information about physical pages that recently became invalid;
- the information must be recovered so Logarithmic Gecko can continue to track invalid pages;
- the described solution prevents an older run from being erased until the relevant Logarithmic Gecko buffer is flushed;
- an SRAM `pinned runs list` records the temporary no-erase relation.

**Use:** grounds `metadata obsolescence ≠ immediately safe physical erasure` and shows that retaining old controller structures can be a temporary prerequisite for reconstructing newer state.

---

### Source C — Dayan and Bonnet, April 2015 Logarithmic Gecko prior work

**Document:** Niv Dayan and Philippe Bonnet, _Garbage Collection Techniques for Flash-Resident Page-Mapping FTLs_, arXiv:1504.01666v1, submitted 7 April 2015.

**Direct record:** <https://arxiv.org/abs/1504.01666>.

**Institutional record:** <https://pure.itu.dk/en/publications/garbage-collection-techniques-for-flash-resident-page-mapping-ftl/>.

**Evidence class:** `H/P` for chronology and terminology; `S` only insofar as the institutional metadata mirrors the paper record.

Directly establishes:

- page-associative Flash-resident FTLs already used a Flash-resident logical→physical mapping table with a smaller RAM cache;
- the authors frame garbage-collection metadata size as a RAM pressure;
- `Lazy Gecko` and `Logarithmic Gecko` are proposed as two distinct solutions, with Logarithmic Gecko intended for lower-RAM settings and storing GC metadata in Flash.

**Prior-art use:** this source blocks any false claim that the SIGMOD 2016 paper suddenly invented the underlying Logarithmic Gecko concept. It also does not establish broader invention priority for FTL metadata recovery; the authors build on pre-existing page-associative FTL work.

---

## Related-repository duplication check

At the start of this slice, code/content searches in `tmzncty/computing-archaeology` for:

- `GeckoFTL Logarithmic Gecko`;
- `FTL metadata power failure recovery`;

returned no dedicated treatment.

**Routing consequence:** the retention-specific case remains here. A later broad history of FTL controller metadata architectures belongs primarily in `computing-archaeology`; this case should then link rather than duplicate it.

---

## Grounded mechanism

The combined evidence supports this bounded model:

```text
normal operation
    ↓
new physical user page
    +
RAM-resident mapping update
    +
recent invalid-page relation
    ↓
periodic mapping/checkpoint closure
    +
Flash-resident mapping / validity / reverse-map structures

power failure
    ↓
RAM caches and metadata buffers disappear
    ↓
persistent OOB/block/run metadata survive
    ↓
scan + classify block/run state
    ↓
reject partial / obsolete metadata runs
    ↓
rebuild GMD, run directories, dirty mappings, invalid-page knowledge
    ↓
normal FTL operation resumes
```

The system therefore does not reduce to `NAND is nonvolatile`. It requires enough persistent evidence to recreate the volatile relations through which the controller knows what the surviving NAND pages mean operationally.

---

## Claims strengthened by this slice

### G-39.1 — `nonvolatile payload ≠ nonvolatile controller state`

**Evidence:** the patent explicitly loses SRAM-resident metadata at power failure while reconstructing it from Flash/OOB state.

**Status:** grounded.

### G-39.2 — `payload survival ≠ immediate restart availability`

**Evidence:** the source defines the recovery objective as restoring SRAM-resident metadata so normal operation can resume.

**Status:** grounded historical/engineering relation.

### G-39.3 — `metadata persistence ≠ zero recovery work`

**Evidence:** even with Flash-resident structures, the controller scans block metadata, reconstructs directories/GMD, recreates dirty mappings, and recovers recent invalidity information.

**Status:** grounded engineering reconstruction.

### G-39.4 — `recovery correctness ≠ recovery latency`

**Evidence:** the SIGMOD paper explicitly treats recovery time as a scaling problem and measures it separately from metadata correctness.

**Status:** grounded.

### G-39.5 — `more persistent metadata ≠ free durability`

**Evidence:** the peer-reviewed abstract states that writing more metadata to Flash increases internal I/O and harms performance and device lifetime.

**Status:** grounded.

### G-39.6 — `physically present metadata ≠ recovery-admissible metadata`

**Evidence:** runs without a postamble are rejected as partially written; obsolete runs are also discarded during recovery.

**Status:** grounded.

### G-39.7 — `surviving data page ≠ recoverable logical identity`

**Evidence:** ¶¶0145–0147 explicitly describe loss of a mapping entry making an updated data page inaccessible and adapt checkpointing to prevent it.

**Status:** grounded.

### G-39.8 — `metadata obsolescence ≠ immediately safe erasure`

**Evidence:** the pinned-run mechanism retains an older run until volatile invalidity information is durably flushed/recoverable.

**Status:** grounded.

### G-39.9 — `controller checkpoint ≠ application transaction checkpoint`

**Evidence:** source semantics concern FTL mapping-cache synchronization and recovery, not filesystem/database transaction atomicity.

**Status:** grounded terminology boundary / functional-analogy guardrail.

### G-39.10 — `research evaluation ≠ commercial deployment`

**Evidence:** the SIGMOD source is a peer-reviewed research design evaluated analytically and through simulation; no inspected source identifies GeckoFTL as a shipped commercial-controller implementation.

**Status:** grounded evidence boundary.

---

## Claims still rejected or open

- **`GeckoFTL was deployed in a commercial SSD`** — unsupported by inspected sources.
- **`95% of all FTL metadata is PVB`** — false generalization; 95% is the paper's evaluated configuration.
- **`51% is a universal power-failure recovery improvement`** — false generalization; baseline/evaluation-specific.
- **`a power-loss-protected NAND payload is automatically host-readable after reboot`** — contradicted as a general inference by the documented need to restore controller metadata.
- **`FTL checkpoint = filesystem journal/WAL`** — rejected genealogy; only a bounded functional analogy is permitted.
- **`GeckoFTL solves all controller-metadata recovery`** — unsupported; it solves the research problem in the described design.
- **`Case 39 proves Intel/Samsung/SanDisk controller recovery behavior`** — unsupported product attribution.
- **invention priority for mapping recovery, checkpoints, LSM trees, or FTLs** — not claimed.

---

## Cross-case boundary

### Case 04 — mapped Flash

Case 04 establishes the early relation:

```text
logical identity
    can survive
physical relocation
```

and already shows that mapping metadata can be retained/reconstructed. Case 39 does not rediscover that. It adds:

```text
metadata scale
    +
volatile working metadata
    +
checkpoint closure
    +
partial-write qualification
    +
recovery latency
    +
reconstruction work after failure
```

### Cases 15 and 38 — SSD power-loss protection

Case 15 studies how stored energy can move temporary committed state to NAND when external power disappears. Case 38 studies whether that protection path remains ready and how a manufacturer validates it.

Case 39 asks a different question:

> after volatile controller metadata disappears, what must be reconstructed for normal logical service to resume?

These mechanisms can coexist in real systems, but the inspected evidence does not establish any implementation genealogy between Intel products and GeckoFTL.

### Case 36 — Flash Correct-and-Refresh

Case 36 renews NAND error-correction margin across retention age/wear. Case 39 reconstructs controller identity/validity metadata after interruption. `refreshing physical reliability margin` and `recovering logical-management state` are different retention work.

---

## Promotion decision

**Case 39 status: `grounded`.**

Promotion is justified because the bounded claim has:

- a named, peer-reviewed SIGMOD paper;
- an institutional publication record with exact date/pages/DOI and evaluation class;
- a same-inventor patent/application record with detailed recovery semantics;
- explicit historical vocabulary;
- direct failure examples;
- explicit source boundaries against commercial deployment and universalization;
- an earlier 2015 same-author chronology anchor;
- a completed related-repository duplication check;
- cross-case separation from mapped Flash, PLP, and NAND retention refresh.

Remaining work should not expand this case into a generic SSD-controller history. Higher-value follow-ups are commercial/named-controller metadata recovery, independent fault compliance, or higher-layer composition with filesystem/database durability.