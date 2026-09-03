# GeckoFTL Power-Failure Recovery: Flash-Resident Validity Metadata, Checkpoints, and Restart Reconstitution

## Scope

- **Bounded system:** Niv Dayan, Philippe Bonnet, and Stratos Idreos, _GeckoFTL: Scalable Flash Translation Techniques For Very Large Flash Devices_, ACM SIGMOD 2016, pp. 327–342, plus Bonnet and Dayan's 29 February 2016-filed U.S. patent application `US20170249257A1`, _Solid-state storage device flash translation layer_.
- **Earlier same-author prior-art boundary:** Dayan and Bonnet, _Garbage Collection Techniques for Flash-Resident Page-Mapping FTLs_, arXiv:1504.01666v1, 7 April 2015, which already introduces `Lazy Gecko` and `Logarithmic Gecko` as garbage-collection metadata techniques for flash-resident page-mapping FTLs.
- **Research question:** if user pages survive in nonvolatile Flash but controller metadata in SRAM disappears at power failure, what additional persistent relations and reconstruction work are required before the FTL can safely resume normal operation?
- **Evidence class:** a peer-reviewed research-system design plus the inventors' patent/application record. This case does **not** claim that GeckoFTL was deployed in a commercial SSD or that its recovery algorithm is a universal FTL implementation.

This case deliberately does not repeat Case 04's 1993 mapped-Flash history. Case 04 already establishes the fundamental relation `logical identity can outlive physical location` and shows that mapping/allocation metadata may itself need to survive or be reconstructible at startup. Case 39 changes the question:

> **What happens when controller metadata becomes large enough that its placement, persistence, checkpointing, and post-failure reconstruction time become first-class retention constraints?**

It also remains separate from Cases 15 and 38. Those cases concern power-loss durability paths and the readiness/validation of stored-energy protection. GeckoFTL instead examines **controller-state reconstruction after power failure**. No claim is made that Intel SSD 320, S3700, or S3500 used GeckoFTL.

---

## Historical vocabulary

The 2015–2017 Gecko sources use terms including:

- `Flash Translation Layer (FTL)`;
- `page-associative FTL`;
- `flash-resident mapping table`;
- `RAM-resident cache` / `SRAM-resident metadata`;
- `Page Validity Bitmap (PVB)`;
- `Lazy Gecko`;
- `Logarithmic Gecko`;
- `LSM tree`;
- `mapping entry`;
- `translation page`;
- `dirty` / `unsynchronized` mapping entry;
- `reverse map`;
- `checkpoint`;
- `run directory`;
- `Global Mapping Directory (GMD)`;
- `preamble` / `postamble`;
- `recovery from power failure`;
- `pinned runs list`.

The following are **project engineering terms**, not period terms attributed to the authors:

- `restart reconstitution`;
- `metadata-retention budget`;
- `recovery-latency obligation`;
- `operational legibility`;
- `controller-state continuity`.

These terms are used only to compare the documented mechanism with other retention cases.

---

## Historical record

### H/P — power-failure recovery becomes a metadata-scaling problem, not merely a NAND-payload problem

The SIGMOD 2016 paper begins from a scaling problem. The amount of FTL metadata grows with device capacity. Keeping all of it in integrated RAM gives fast access, but becomes increasingly expensive as Flash capacities grow. Persisting more metadata in Flash avoids the RAM requirement but creates additional internal I/O, which can harm both performance and device lifetime.

The paper explicitly adds **power-failure recovery time** to this tradeoff: recovery time is proportional to metadata size and, at large scale, becomes impractical. The authors identify the `Page Validity Bitmap (PVB)` as a major component: it records which physical pages are invalid so garbage collection can select and process blocks correctly.

In the evaluated configuration, the authors report that PVB makes up 95% of the FTL's RAM-resident metadata. That percentage is an evaluated-system result, **not a universal property of every FTL**.

**Primary/scholarly anchor:** Dayan, Bonnet, Idreos, _GeckoFTL_, SIGMOD 2016, abstract; University of Copenhagen and IT University of Copenhagen publication records reproduce the peer-reviewed paper metadata and abstract.

### H/P — Logarithmic Gecko moves page-validity metadata into Flash rather than assuming all current controller state stays in SRAM

The 2015 paper introduces `Logarithmic Gecko` for systems where RAM is too scarce to hold the garbage-collection metadata. The 2016 paper develops this into GeckoFTL.

The patent application describes Logarithmic Gecko as storing the PVB in Flash as an LSM tree. Runs map block IDs to bitmaps indicating invalid pages. A Flash-resident reverse map retains which logical pages were most recently written on each physical block.

This matters for retention because the user payload is no longer the only nonvolatile state that must survive. The controller needs durable or reconstructible **relations about which physical pages remain valid and how logical/physical mappings should be interpreted**.

**Primary anchor:** `US20170249257A1`, paragraphs 0026–0028.

### H/P — the recovery target is explicitly the lost SRAM-resident metadata needed for normal operation

The patent's section `3.4 Recovery from Power Failure` states the goal directly: a fast FTL recovery algorithm restores SRAM-resident metadata so normal operation can resume. The source says recovery should ideally take no more than a few seconds.

Its bounded recovery outline is:

1. scan one out-of-band area for every block to determine block types;
2. reconstruct SRAM structures such as the GMD from that information;
3. recreate cache mapping entries that were dirty at the time of power failure;
4. use periodic checkpoints so a dirty cache mapping does not remain un-synchronized for longer than the bounded update interval.

The important retention distinction is therefore:

```text
NAND pages survive power loss
        ≠
controller has immediately recovered the metadata needed to interpret and manage them
```

**Primary anchor:** `US20170249257A1`, paragraphs 0029–0031.

### H/P — checkpointing limits how much volatile mapping state may need reconstruction

The same recovery description says checkpoints are taken every period of `C` data-page updates, where `C` is tied to the number of mapping entries that fit in SRAM. The checkpoint policy bounds how long a mapping entry may remain dirty in cache before synchronization.

This is not a filesystem or database transaction checkpoint. It is FTL-internal controller metadata maintenance. The word `checkpoint` should therefore remain tied to the mechanism and layer in which the authors use it.

The retention relation is narrower:

> **volatile controller state may be allowed to disappear at failure only because the system preserves enough persistent evidence and periodic closure points to reconstruct the missing relation later.**

### H/P — partially written metadata structures must be distinguishable from valid structures during recovery

The later patent section `5.7 Recovery from Power Failure` adapts the algorithm to the LSM-based FTL. Runs receive IDs and metadata. A run has a preamble, while its last page carries a postamble containing a run-directory copy. During recovery, the algorithm discards a run without a postamble as only partially written, identifies obsolete runs, and recovers run directories for valid runs into SRAM.

This adds a currentness/admissibility relation to metadata recovery:

```text
physically present run bytes
        ≠
recovery-admissible completed run
```

A surviving Flash structure does not automatically count as current controller state merely because its pages are readable after reboot.

**Primary anchor:** `US20170249257A1`, paragraphs 0142–0144.

### H/P — losing one unsynchronized mapping entry can make a live updated data page inaccessible

The patent gives an explicit failure case. A mapping entry can leave the cache, enter the LSM-tree buffer, and then be lost if power fails before that buffered entry reaches Flash. The updated data page itself may exist, yet the mapping entry that provides access to it can disappear.

The patent says this can make the system unable to access the updated data page and adjusts the checkpoint period so entries resident in the LSM-tree buffer at failure are recoverable into cache.

This is an unusually sharp primary-source example of a relation central to this repository:

> **payload embodiment survival ≠ recoverable logical identity.**

The failure is not that the NAND data page necessarily vanished. It is that the controller can lose the retained relation required to designate that page as the current value of a logical address.

**Primary anchor:** `US20170249257A1`, paragraphs 0145–0147.

### H/P — recent invalid-page knowledge is itself volatile state that must be reconstructed

The patent separately warns that power failure loses the contents of Logarithmic Gecko's LSM-tree buffer. That buffer records physical pages that recently became invalid. If the buffer disappears, the FTL can lose track of invalid-page state needed for later garbage collection.

The described solution constrains erasure: a run whose old mapping information may still be needed is kept from being erased until Logarithmic Gecko's buffer has been flushed. A small SRAM `pinned runs list` records this temporary no-erase relation.

This creates a retention dependency that is easy to miss if one looks only at user data:

```text
recent invalidity relation not yet durably closed
        ↓
old metadata embodiment cannot yet be erased safely
        ↓
metadata buffer flush closes the dependency
        ↓
old run may become reclaimable
```

Deletion/reclamation of controller metadata is therefore ordered by the need to preserve enough evidence for future reconstruction.

**Primary anchor:** `US20170249257A1`, paragraphs 0148–0149 and surrounding recovery discussion.

### H/S — the reported improvement is a research evaluation, not a deployment result

The peer-reviewed SIGMOD publication reports analytical and simulation evaluation. Relative to the baseline in which PVB is stored in Flash, the authors report:

- 95% reduction in space requirements;
- at least 51% reduction in recovery time;
- 98% lower contribution to internal I/O overheads.

These figures are useful because they show that **recovery work, metadata footprint, and write/endurance cost were explicit design dimensions**. They are not evidence that a commercial SSD in the field obtained those exact numbers.

**Scholarly anchor:** SIGMOD 2016 publication record and abstract, University of Copenhagen / IT University of Copenhagen.

---

## Retained state

This case requires at least five state classes to stay separate.

### 1. User data pages in Flash

The physical payload is nonvolatile across ordinary loss of controller power within the bounded model.

### 2. Logical-to-physical mapping state

A data page is useful to the host only if the FTL can resolve its logical address to the current physical embodiment.

### 3. Page-validity / invalidity metadata

Garbage collection must know which physical pages in a block remain live and which are obsolete. `PVB` / Logarithmic Gecko is therefore retained controller state with consequences for safe reclamation.

### 4. Volatile working metadata

Caches, LSM-tree buffers, run directories, and other SRAM structures accelerate ordinary operation but disappear on power failure.

### 5. Recovery witnesses and closure metadata

Block-type OOB state, timestamps/spare-area information, run IDs, preambles/postambles, checkpoints, Flash-resident reverse maps, and still-preserved older runs can supply evidence from which volatile state is rebuilt.

A useful bounded description is therefore:

> **nonvolatile payload + persistent/reconstructible identity and validity relations + volatile acceleration state + a recovery procedure.**

---

## Retention mechanism

GeckoFTL combines ordinary operational maintenance with failure-time reconstitution.

### During normal operation

```text
host logical write
    ↓
new physical data page
    ↓
new / dirty logical→physical mapping entry in RAM
    ↓
old physical version becomes an invalidity fact
    ↓
Logarithmic Gecko / mapping structures eventually persist that relation in Flash
    ↓
periodic checkpoint bounds unsynchronized volatile state
```

### After power failure

```text
SRAM state disappears
    ↓
scan persistent OOB / block metadata
    ↓
qualify completed versus partial/obsolete metadata runs
    ↓
reconstruct GMD / run directories / dirty mapping entries
    ↓
recover recently lost invalidity information
    ↓
normal operation resumes
```

Persistence here is not just “Flash remembers.” It includes a protocol for deciding **which surviving metadata is admissible and how enough controller state is recreated after volatile working state disappears**.

---

## Addressing and access geometry

Case 04 established that a logical address may survive physical relocation. GeckoFTL adds a later operational constraint: the address-translation relation itself is split across multiple storage classes.

- logical page addresses designate host-visible identities;
- physical addresses designate NAND pages;
- Flash-resident mapping structures retain a durable part of the relation;
- RAM caches accelerate access to selected mapping entries;
- block IDs and page-validity bitmaps support garbage-collection queries;
- recovery scans OOB/block metadata rather than simply replaying a host-visible address stream.

A logical address can therefore remain conceptually stable while the machinery required to resolve it is temporarily absent during restart.

---

## Read semantics

The bounded case is not about NAND read disturb or read-retry. Its read problem is metadata interpretation.

A user data page can be readable as a physical page while not yet being available through the logical interface if the controller has not reconstructed the current mapping relation. Recovery therefore includes reads whose purpose is not to retrieve host payload but to **rebuild the controller's ability to know what later host reads should mean**.

---

## Write and invalidation semantics

Out-of-place update creates at least two coupled state changes:

1. a new physical page becomes the current embodiment of a logical page;
2. the previous physical page becomes invalid.

The new mapping and the invalidity fact do not have to become durable in one indivisible physical action. The recovery machinery exists because volatile buffers can hold some of this state at interruption.

The case therefore adds a controller-level crash-consistency problem below the filesystem:

> **the system must preserve enough ordering/evidence that it can reconstruct which physical embodiment is current and which older embodiments may safely be reclaimed.**

This is an engineering reconstruction of the documented mechanism, not a claim that GeckoFTL implements database transactions.

---

## Failure and forgetting

### Power loss can destroy volatile controller state without erasing NAND payload

This is the central failure boundary.

### A lost mapping entry can make a surviving current page inaccessible

The patent explicitly describes this failure and changes checkpointing to prevent it.

### A lost invalidity update can make garbage-collection knowledge stale

If the controller forgets that a physical page became invalid, later space-reclamation behavior can no longer rely on the intended validity relation.

### Partial metadata writes can survive physically but be rejected logically

Runs lacking the documented completion witness/postamble are discarded during recovery.

### Reclamation can itself destroy recovery evidence too early

The pinned-run mechanism delays erasure until buffered invalidity information reaches a recoverable state.

Thus `forgetting` is not one thing. It can be:

- intentional invalidation of an obsolete physical page;
- physical erase of a reclaimable Flash block;
- accidental disappearance of volatile metadata;
- loss of a logical→physical relation;
- rejection of a partial metadata run;
- or loss of enough validity history to reclaim safely.

---

## Time

GeckoFTL exposes at least four relevant timescales.

### Host-write time

Logical and physical currentness change as updates arrive.

### Metadata synchronization/checkpoint time

Dirty/unsynchronized controller state is periodically closed into recoverable form.

### Power-failure recovery time

The authors treat time-to-resume as a design objective distinct from the survival of individual NAND pages.

### Device-lifetime / internal-I/O time

Persisting metadata more aggressively costs Flash writes and therefore can affect performance and lifetime.

This creates a useful tension:

> **making controller state easier to recover can itself consume the medium whose long-term reliability the controller is managing.**

---

## Maintenance and labor

The maintenance work in this case is largely firmware/controller work:

- updating mapping-cache entries;
- recording invalid-page relations;
- maintaining reverse maps;
- building/merging Flash-resident metadata runs;
- taking checkpoints;
- delaying erasure while recovery evidence is still needed;
- scanning metadata after failure;
- reconstructing SRAM structures before normal service resumes.

No human operator is shown performing this routine recovery. That is still labor in the repository's broader infrastructural sense: the apparent stability of the logical block interface depends on hidden controller work and on design choices about how much recovery latency, RAM, Flash I/O, and endurance cost are acceptable.

---

## Engineering reconstruction

The grounded evidence supports the following bounded relations.

### `nonvolatile payload ≠ nonvolatile controller state`

Power failure can leave NAND data pages present while destroying SRAM-resident mappings, caches, and validity buffers.

### `payload survival ≠ immediate restart availability`

Normal operation resumes only after enough controller metadata has been restored.

### `metadata persistence ≠ zero recovery work`

Persisting structures in Flash does not eliminate scanning, qualification of completed runs, directory reconstruction, or recreation of dirty entries.

### `recovery correctness ≠ recovery latency`

A system might in principle reconstruct the right state eventually while still violating a practical restart-time objective. GeckoFTL makes recovery time an explicit scaling axis.

### `more persistent metadata ≠ free durability`

Moving more metadata to Flash increases internal I/O and can consume performance/lifetime budget; the design problem is a tradeoff rather than “persist everything.”

### `surviving bytes ≠ admissible metadata state`

Partially written or obsolete runs can remain physically present but be rejected during recovery.

### `safe metadata erasure ≠ immediate obsolescence`

An obsolete run may still need to remain physically available until volatile invalidity information is durably closed.

---

## Functional analogies

### A — Case 04 mapped Flash

Case 04 already shows that retained mapping state can preserve logical identity across physical relocation. GeckoFTL is not the same historical system. The functional bridge is narrower:

> both demonstrate that user payload alone is insufficient; a later controller must recover a relation that says which embodiment counts.

Case 39 adds recovery-scale, checkpoint, partial-metadata-admissibility, and recovery-latency constraints absent from the bounded 1993 argument.

### A — filesystem/database crash recovery

Both an FTL and a filesystem/database may reconstruct volatile operational state after interruption. This is only a functional analogy. GeckoFTL's mapping/checkpoint mechanism is **not** a filesystem journal, WAL, or transaction protocol, and its correctness target is controller mapping/validity state rather than application-level atomicity.

### A — distributed currentness

The distinction `physical survivor ≠ current/admissible state` resembles later distributed cases in which stale replicas or fragments remain present but do not count as current. There is no historical genealogy implied: GeckoFTL's run completion/currentness is a local controller problem.

---

## Philosophical interpretation

The exact technical fact that creates the conceptual problem is simple:

> a physical data page may survive, while the operational relation that makes it available as **this logical page now** must be reconstructed.

This puts pressure on any philosophy that identifies persistence solely with material survival. The retained object presented to the host is relational: payload, mapping, validity, and an admissibility/recovery procedure jointly sustain its later availability.

A bounded project interpretation is therefore:

> **technical retention can require preserving enough traces to reconstitute the conditions of intelligibility and currentness after the volatile machinery that previously held those relations has disappeared.**

This is not a claim that FTL metadata is automatically Stieglerian `tertiary retention`, that the SSD is a Heideggerian `Bestand`, or that controller recovery supplies a general philosophy of memory. The mechanism constrains the interpretation; it does not prove a philosophical doctrine.

---

## Counterexamples and limits

- GeckoFTL is a **research design**, not evidence of commercial deployment.
- The 95% PVB share and 95%/51%/98% evaluation results belong to the paper's evaluated configuration/baseline; they are not universal FTL constants.
- The case does not prove that all user data survive every power failure. It studies metadata recovery under the authors' FTL model.
- `checkpoint` here is FTL-internal vocabulary and should not be silently normalized into database/filesystem transaction semantics.
- The patent/application describes one LSM-based design and its adaptations; it is not a normative SSD standard.
- This case does not establish invention priority for Flash metadata recovery, mapping-table persistence, checkpointing, LSM trees, or FTLs. The authors explicitly build on earlier page-associative FTL work and their own April 2015 Logarithmic Gecko paper.
- Exact implementation behavior of Intel, Samsung, SanDisk/Western Digital, or other commercial controllers cannot be inferred from GeckoFTL.

---

## Related repositories

### `tmzncty/computing-archaeology`

Repository searches for `GeckoFTL`, `Logarithmic Gecko`, and `FTL metadata power failure recovery` found no dedicated existing treatment at this slice's start. If a broader history of commercial FTL metadata architectures is later built there, this case should link to it rather than grow into that history.

### `tmzncty/problem-history`

Useful anti-anachronism warning: the authors explicitly formulate `recovery from power failure`, `PVB`, checkpoints, and SRAM/Flash metadata placement. Project terms such as `restart reconstitution` are later reconstruction and must not be substituted for their vocabulary.

---

## Claim ledger

| Claim | Type | Status |
| --- | --- | --- |
| GeckoFTL treats FTL metadata size and power-failure recovery time as scaling constraints | H/P | grounded |
| PVB records invalid physical pages for garbage collection and is a major RAM metadata component in the evaluated design | H/P | grounded, configuration-bounded |
| Logarithmic Gecko stores page-validity information in Flash as LSM-tree-like runs | H/P | grounded |
| recovery explicitly restores SRAM-resident metadata before normal operation resumes | H/P | grounded |
| checkpoints bound unsynchronized mapping state in the described recovery algorithm | H/P | grounded |
| run postambles help distinguish completed/admissible metadata from partial writes | H/P/E | grounded |
| losing an unsynchronized mapping entry can make a surviving updated data page inaccessible | H/P | grounded |
| recent invalidity metadata can be lost with the volatile Logarithmic Gecko buffer and must be reconstructed | H/P | grounded |
| payload survival does not imply immediate logical availability after failure | E | grounded reconstruction |
| GeckoFTL was deployed in commercial SSDs | X | unsupported |
| the paper's 95%/51%/98% results are universal SSD properties | X | unsupported |
| FTL checkpoints are historically identical to filesystem/database checkpoints | X/A | rejected as genealogy; bounded functional analogy only |

---

## Sources

### Primary / period research sources

- Niv Dayan and Philippe Bonnet, _Garbage Collection Techniques for Flash-Resident Page-Mapping FTLs_, arXiv:1504.01666v1, submitted 7 April 2015: <https://arxiv.org/abs/1504.01666>.
- Niv Dayan, Philippe Bonnet, and Stratos Idreos, _GeckoFTL: Scalable Flash Translation Techniques For Very Large Flash Devices_, Proceedings of ACM SIGMOD 2016, pp. 327–342, DOI `10.1145/2882903.2915219`.
- Philippe Bonnet and Niv Dayan, _Solid-state storage device flash translation layer_, U.S. patent application `US20170249257A1`, filed 29 February 2016, published 31 August 2017. IT University of Copenhagen institutional patent record: <https://pure.itu.dk/en/publications/solid-state-storage-device-flash-translation-layer/>.

### Institutional bibliographic / abstract records

- University of Copenhagen Research Portal, GeckoFTL publication record: <https://researchprofiles.ku.dk/en/publications/geckoftl-scalable-flash-translation-techniques-for-very-large-fla-2/>.
- IT University of Copenhagen, GeckoFTL publication record: <https://pure.itu.dk/en/publications/geckoftl-scalable-flash-translation-techniques-for-very-large-fla/>.

### Public patent transcription used for paragraph-level location

- `US20170249257A1` transcription: <https://uspto.report/patent/app/20170249257>.

The institutional patent record establishes inventors, filing/publication metadata, and the patent's LSM mapping-table abstract. The public transcription is used for paragraph-level recovery locations; claims depending on those locations remain bounded to the published patent application rather than generalized to commercial products.