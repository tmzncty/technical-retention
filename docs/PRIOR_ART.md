# Prior Art Map

This repository exists only if it contributes something more precise than `storage technology has a history` or `digital media are forms of memory`.

The following work already occupies major parts of the territory.

## 1. Wolfgang Ernst — closest methodological neighbor

### Why he matters

Wolfgang Ernst's media archaeology is the closest existing work to the interface this project wants to occupy. He insists on reading technical memory at the level of mechanisms, timing, operationality, registers, buffers, access modes, and material processes rather than treating computer memory merely as a metaphor for human or social memory.

In his technical-media notes, Ernst explicitly distinguishes archive, memory, and storage and lists a hierarchy that includes:

- read-only storage;
- registers;
- accumulators;
- buffers;
- direct, sequential, indexed, stack-like, word-organized, and associative storage;
- access time and latency.

His 2013 article **"From Media History to Zeitkritik"** places machine-specific temporality / `Eigenzeit` and time-criticality at the center of technical-media analysis. In a 2013 response to Jussi Parikka on microtemporality, Ernst gives an even stronger operational formulation: technological media are in their `medium-being` only in operation / "under current". These are important primary-author anchors for the repository's operationality test.

A later formulation names **critical storage analysis** as a combination of media archaeology and digital forensics applied to computer memory as hardware and software.

### What is already done

- critique of loose cultural-memory metaphors;
- technical attention to machine memory;
- archive versus operational memory;
- microtemporality and time-criticality;
- machine-specific temporalities / `Eigenzeit`;
- storage / transfer relations;
- registers and buffers as media-theoretical objects.

### What the bounded test changes

[`PHILOSOPHICAL_TEST_01_ERNST_OPERATIONALITY.md`](PHILOSOPHICAL_TEST_01_ERNST_OPERATIONALITY.md) confirms Ernst as a strong methodological prior art but rejects two possible universalizations:

- `retained state = continuous operation`;
- `technically decisive time = microtime only`.

The grounded cases include quiescent positional, magnetic, and Flash states alongside deadline-driven DRAM refresh, access-triggered core restore, deferred Flash reclamation, and failure-triggered RADOS repair. The project therefore treats operationality as a demand to reconstruct **which operation and which timescale matter**, not as one universal retention mechanism.

### What remains open for this repository

A long, source-controlled comparative program following **retention mechanisms** across mechanical, electromechanical, electronic, magnetic, semiconductor, controller-mediated, and distributed systems, while testing philosophical concepts against exact engineering constraints.

The current narrower novelty boundary is:

> Ernst already supplies a powerful operational/time-critical analysis of technical media; this repository can still contribute by comparing retention obligations that are quiescent, continuous, access-triggered, deadline-driven, workload/capacity-triggered, wear-triggered, failure-triggered, or interpretive, without forcing them onto one privileged temporal scale.

### Starting sources

- Wolfgang Ernst, *Digital Memory and the Archive*, University of Minnesota Press, 2012: <https://www.upress.umn.edu/9780816677665/digital-memory-and-the-archive/>
- Wolfgang Ernst, **"From Media History to Zeitkritik"**, *Theory, Culture & Society* 30(6), 2013, pp. 132–146, DOI 10.1177/0263276413496286: <https://journals.sagepub.com/doi/10.1177/0263276413496286>
- Wolfgang Ernst, response in Jussi Parikka, **"Ernst on Time-Critical Media: A mini-interview"**, 18 March 2013: <https://jussiparikka.net/2013/03/18/ernst-on-microtemporality-a-mini-interview/>
- Wolfgang Ernst, *Chronopoetics: The Temporal Being and Operativity of Technological Media*, 2016: <https://www.bloomsbury.com/us/chronopoetics-9781783485703/>
- Wolfgang Ernst, technical storage notes, Humboldt-Universität: <https://www.musikundmedien.hu-berlin.de/de/medienwissenschaft/medientheorien/ernst-in-english/NOTES/PDF/storage-notes.pdf/@@download/file/STORAGE-NOTES.pdf>
- Wolfgang Ernst, **TIME-CRITICALITY**, Humboldt-Universität technical-media script: <https://www.musikundmedien.hu-berlin.de/de/medienwissenschaft/medientheorien/ernst-in-english/pdfs/time-critical-2.pdf/@@download/file/time-critical-2.pdf>

The published article/book records should be preferred where exact bibliographic anchoring matters; the HU scripts are useful authorial working/teaching sources and should not silently substitute for a checked published edition when wording is decisive.

---

## 2. Bernard Stiegler — technics and tertiary retention

### Why he matters

Stiegler makes technical exteriorization central to the constitution of human temporality and memory. `Tertiary retention` provides a powerful way to ask how technical traces can outlive individual experience and condition later recollection, repetition, expectation, and inheritance.

### Risk

Do not use `tertiary retention` as a loose synonym for every bit-holding mechanism.

A DRAM cell, magnetic core, archive, notebook, phonograph, and database do not become conceptually identical merely because they can all be described using the word `retention`.

### Contribution opportunity

Use exact technical cases to distinguish:

- external trace;
- machine-operational state;
- cultural record;
- addressable data;
- executable state;
- durable archive;
- temporary buffer;
- replicated logical object.

Then ask which kinds of technical retention actually bear on Stiegler's argument and how.

### Starting source

- Bernard Stiegler, *Technics and Time* (especially the development of technical exteriorization and tertiary retention across the series).

---

## 3. Martin Heidegger — technology, ordering, and standing-reserve

### Why he matters

`The Question Concerning Technology` analyzes modern technological revealing in terms of ordering and `Bestand` / standing-reserve: what stands ready to be called upon for further ordering.

This can sharpen questions about addressability, availability, inventory, databases, and storage systems.

### Strict boundary

> `Bestand` is **not** an old philosophical word for RAM, disk, or cloud storage.

The project must not derive a technical thesis from an English-language pun on `storage`, `stock`, `reserve`, or `standing`.

### Starting source

- Martin Heidegger, "The Question Concerning Technology," in *The Question Concerning Technology and Other Essays*.

---

## 4. Matthew G. Kirschenbaum — forensic materiality of digital storage

### Why he matters

*Mechanisms* pushes new-media and textual studies below the visible interface into actual storage mechanisms, especially the hard drive. Its key analytical vocabulary includes erasure, variability, repeatability, and survivability.

MIT Press describes it as the first book in its field to devote significant attention to storage, particularly the hard drive.

### Contribution opportunity

Extend mechanism-specific analysis across a much broader technical lineage and connect forensic persistence to refresh, remapping, wear, redundancy, distributed identity, and maintenance.

### Source

- Matthew G. Kirschenbaum, *Mechanisms: New Media and the Forensic Imagination*, MIT Press: <https://mitpress.mit.edu/9780262517409/mechanisms/>

---

## 5. Computer History Museum — *The Storage Engine*

### Why it matters

The Computer History Museum already provides a substantial milestone history of information storage, ranging from very early inscription through punched media, magnetic storage, optical storage, semiconductor RAM and Flash, networked storage, and cloud storage.

This is extremely useful as a timeline and source-discovery map.

### What it means for this repository

Do **not** build another generic `year → invention → capacity` timeline unless needed as an index.

The value here must come from mechanism comparison and the conceptual problem of retention.

### Sources

- *The Storage Engine*: <https://www.computerhistory.org/storageengine/>
- CHM Memory & Storage timeline: <https://www.computerhistory.org/timeline/memory-storage/>

---

## 6. Conventional computer architecture and memory-system literature

There is already a vast technical literature on:

- registers and latches;
- cache hierarchies;
- SRAM and DRAM;
- virtual memory;
- magnetic disks;
- Flash;
- SSD controllers and FTLs;
- RAID;
- distributed storage;
- consistency and replication.

These sources should supply mechanism, terminology, performance models, and engineering constraints. `technical-retention` should not pretend to replace them.

A useful integrated technical reference is:

- Bruce Jacob, Spencer Ng, David Wang, *Memory Systems: Cache, DRAM, Disk*.

---

## 7. Adjacent traditions to map later

The first scaffold is incomplete. Later prior-art work should explicitly map:

- Friedrich Kittler and German media theory;
- Jussi Parikka and media archaeology;
- Gilbert Simondon on technical objects and individuation;
- Jacques Derrida on archive / trace where technically relevant;
- philosophy of information;
- history of writing, notation, accounting, and administrative records;
- archival science and preservation;
- database history;
- digital preservation and emulation;
- forensic computing;
- infrastructure studies and maintenance studies;
- histories of bookkeeping, indexing, cataloging, and filing.

The test for inclusion is not `does this scholar mention memory?` but `does this work change how we can analyze technical retention?`

---

## Current novelty claim — deliberately modest

The working novelty claim is **not** that nobody has connected technology and memory.

That claim would be false.

The narrower claim to test is:

> There is room for a source-controlled research program that follows retained state from mechanical and pre-electronic configurations through computer memory and modern distributed storage, compares the mechanisms along shared dimensions such as refresh, addressability, erasure, failure, maintenance, and identity, and uses those mechanisms to discipline philosophical interpretation.

If later literature proves that this program has already been done substantially better, this repository should become an annotated map to that work rather than duplicate it.
