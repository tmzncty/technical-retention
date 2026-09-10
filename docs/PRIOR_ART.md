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

### What the bounded test changes

[`PHILOSOPHICAL_TEST_02_STIEGLER_TERTIARY_RETENTION.md`](PHILOSOPHICAL_TEST_02_STIEGLER_TERTIARY_RETENTION.md) rejects both a durable-human-readable-media-only restriction and the opposite equation `every technically retained state = tertiary retention`.

The useful boundary is relational: technical supports may participate in exteriorization, repetition, learning, and transmission, while controller-internal mappings, refresh states, replica placement, and other infrastructure can be constitutive of a tertiary-retentional system without being philosophically identical to the retained cultural/epistemic trace.

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

### Starting sources

- Bernard Stiegler, *For a New Critique of Political Economy*, trans. Daniel Ross, Polity, 2010, Introduction pp. 8–10.
- Bernard Stiegler, **"Die Aufklärung in the Age of Philosophical Engineering,"** *Computational Culture* 2, 28 September 2012: <https://computationalculture.net/die-aufklarung-in-the-age-of-philosophical-engineering/>.
- Bernard Stiegler, *Technics and Time* series, for the broader development of technical exteriorization and tertiary retention.

---

## 3. Martin Heidegger — technology, ordering, and standing-reserve

### Why he matters

`The Question Concerning Technology` analyzes modern technological revealing in terms of ordering and `Bestand` / standing-reserve: what stands ready to be called upon for further ordering.

This can sharpen questions about addressability, availability, inventory, databases, and storage systems — but only if the engineering and philosophical levels remain distinct.

### Strict boundary

> `Bestand` is **not** an old philosophical word for RAM, disk, cloud storage, or stored data.

The primary text itself blocks that shortcut. In William Lovitt's 1977 translation, printed p. 16, `storing` appears as one operation inside a larger chain of unlocking, transformation, distribution, switching, regulation, and securing. On p. 17 Heidegger names `Bestand` and immediately marks it as something more essential than mere `stock`. On pp. 19–21 `Ge-stell` / Enframing is treated as a mode of revealing/order rather than a technological component or object class.

### What the bounded test changes

[`PHILOSOPHICAL_TEST_03_HEIDEGGER_ORDERABILITY.md`](PHILOSOPHICAL_TEST_03_HEIDEGGER_ORDERABILITY.md) tests the concept against the already grounded addressability decomposition and against mapped Flash/RADOS in particular.

It rejects:

- `stored datum = item of standing-reserve`;
- `addressable = Heideggerianly orderable`;
- `physical presence = technical availability`;
- `replaceable embodiment = immateriality`;
- `any retained state usable later = Bestand`.

The narrower surviving bridge is:

> **designation, resolution, currentness/admissibility, replacement, and recovery can make the engineering conditions of `being on call` precise. Those mechanisms can discipline a Heideggerian interpretation of orderability, but they neither define `Bestand` nor prove that an isolated storage object is standing-reserve.**

Mapped Flash and RADOS are useful not because they are `more Heideggerian storage`, but because they show that callability can persist while physical embodiments are replaced, and that current orderability depends on retained mapping, placement, version, authority, and repair relations.

### Starting sources

- Martin Heidegger, *The Question Concerning Technology and Other Essays*, trans. William Lovitt, Harper & Row, 1977, especially printed pp. 16–23. Page-preserving digital transcription: <https://opensutd.org/qct-sub/>.
- Martin Heidegger, *Die Frage Nach der Technik*, 1954; Bard College Hannah Arendt Personal Library digitization/catalog record: <https://digitalcommons.bard.edu/hapl_marginalia_all/221/>.
- Theodore Kisiel, **"Standing Reserve (Bestand),"** in Mark A. Wrathall (ed.), *The Cambridge Heidegger Lexicon*, Cambridge University Press, 2021, pp. 699–700, DOI 10.1017/9780511843778.192: <https://www.cambridge.org/core/books/abs/cambridge-heidegger-lexicon/standing-reserve-bestand/B1D7C663181755835284E5D6FB591BAD>.
- Stanford Encyclopedia of Philosophy, **"Martin Heidegger,"** §5.2 Technology: <https://plato.stanford.edu/entries/heidegger/>.

---

## 4. Matthew G. Kirschenbaum — forensic and formal materiality beyond disk

### Why he matters

*Mechanisms* pushes new-media and textual studies below the visible interface into actual storage mechanisms and physical records. Kirschenbaum's Introduction defines **forensic materiality** through material particularity / individualization and **formal materiality** through relational computational states, while warning that the pair cannot simply be mapped to `hardware` and `software`.

The book's central storage mechanism is nevertheless the magnetic hard drive. MIT Press describes *Mechanisms* as the first book in its field to devote significant attention to storage, particularly the hard drive, and the Introduction describes the hard drive as the central example of storage as a writing machine.

### What the bounded test changes

[`PHILOSOPHICAL_TEST_04_KIRSCHENBAUM_FORENSIC_MATERIALITY.md`](PHILOSOPHICAL_TEST_04_KIRSCHENBAUM_FORENSIC_MATERIALITY.md) tests the portable part of Kirschenbaum's method against grounded mapped Flash and RADOS, with Wei et al. FAST 2011 as a deliberately later SSD-forensics boundary.

The test retains the methodological demand to investigate material embodiments and trace histories below the interface, but rejects the stronger shortcuts:

- `forensic materiality = hard-drive remanence`;
- `every deleted/obsolete digital state remains forensically recoverable`;
- `host-interface invisibility = raw-media absence`;
- `physical survival = current logical state`;
- `physical survival = forensic accessibility`;
- `one logical object = one material witness`.

Mapped Flash and the FAST 2011 SSD experiments show why the distinction matters: controller indirection can make a logical value disappear through the normal interface while stale raw-Flash embodiments remain, yet reclamation, sanitization, and key-mediated unreadability can later change recoverability. RADOS adds a distributed boundary in which several individualized physical replicas may survive while version, epoch, peering, and authority determine which state currently counts.

The bounded test therefore adds two project comparison rules:

> **forensic witness ≠ authoritative current state**

and

> **logical-object survivability ≠ current-embodiment survivability ≠ forensic-trace survivability**.

These are project terms, not Kirschenbaum's vocabulary.

### Revised contribution opportunity

The novelty claim here is no longer the generic statement that digital media are material or that deletion may leave traces. Kirschenbaum and digital forensics already establish that territory.

The narrower contribution opportunity is:

> **re-ground forensic persistence mechanism by mechanism when logical identity is remapped, obsolete embodiments are reclaimed, recoverability depends on keys or controller state, replicas multiply or disappear, and protocol currentness diverges from physical survival.**

This also gives the broader project another invariant to test before any grand synthesis: `trace survivability` should not be silently folded into `logical persistence`.

### Starting sources

- Matthew G. Kirschenbaum, *Mechanisms: New Media and the Forensic Imagination*, MIT Press, 2008: <https://mitpress.mit.edu/9780262113113/mechanisms/>.
- Kirschenbaum, *Mechanisms*, Introduction, page-preserving excerpt used for the forensic/formal definitions and hard-drive scope boundary: <https://raley.english.ucsb.edu/wp-content/Engl800/Kirschenbaum-intro.pdf>.
- Michael Wei, Laura M. Grupp, Frederick E. Spada, Steven Swanson, **"Reliably Erasing Data From Flash-Based Solid State Drives,"** FAST '11, USENIX Association, February 2011: <https://www.usenix.org/conference/fast11/reliably-erasing-data-flash-based-solid-state-drives>.

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

## 7. OAIS and PREMIS — digital preservation beyond simple bit survival

### Why they matter

The digital-preservation community already occupies an important part of this repository's conceptual territory. In particular, the **Open Archival Information System (OAIS)** reference model and **PREMIS** preservation-metadata work make it impossible to treat the following as novel claims here:

- preserving bits is sufficient for long-term preservation;
- a bitstream remains useful without retained representation/interpretation information;
- software, hardware, and runtime environment can be ignored once content files survive;
- fixity checking is the same thing as preserving meaning or authenticity;
- preservation actions and their outcomes need not themselves become records.

The source-controlled review is in [`../evidence/prior-art-oais-premis-2002-2024-grounding.md`](../evidence/prior-art-oais-premis-2002-2024-grounding.md).

### Historical boundary

The original OAIS issue, **CCSDS 650.0-B-1 (January 2002)**, explicitly says its long-term information-preservation/access function is being distinguished from simple `bit storage`. It already uses **Designated Community** and **Representation Information**, and its migration model permits controlled representation changes while attempting to preserve information content.

The current **CCSDS 650.0-M-3 (December 2024)** preserves that broad architecture but its own document-control note says **Preservation Objectives** were introduced in Issue 3 to make `Independently Understandable` more consistently testable. Do not back-project that 2024 addition into the 2002 vocabulary.

PREMIS Version 1.0's final report appeared in **May 2005**. It provides a practical data dictionary for preservation metadata but explicitly leaves detailed format-specific technical metadata and detailed media/hardware description to specialists. PREMIS 3.0 (2015) models fixity references, preservation Events and outcomes, and gives a richer environment/dependency model; the 3.0 text explicitly says its environment modeling changed from earlier versions.

### What this changes for the repository

OAIS/PREMIS are strong prior art for the general proposition:

> **material or bit-level survival is not sufficient for long-term information preservation when representation knowledge, environmental dependencies, provenance/fixity evidence, and a future community's ability to interpret the object may change.**

That is no longer a contribution opportunity for `technical-retention` by itself.

The narrower opportunity is mechanism-level and comparative: trace those archival requirements downward into exact physical, controller, filesystem, protocol, and distributed relations. For example, OAIS Representation Information and PREMIS environment dependencies overlap functionally with [`SYNTHESIS_23_RETENTION_INTERPRETER_ACCESS_APPARATUS.md`](SYNTHESIS_23_RETENTION_INTERPRETER_ACCESS_APPARATUS.md), but they are not identical to its distinctions among material embodiment, restart legibility, software-format interpretation, physical reader capability, controller admission, and operation-specific service.

Likewise PREMIS fixity/Event semantics are prior art for retaining integrity references and preservation-action outcomes, but they do not by themselves answer which replica is current, whether a NAND mapping is recoverable, whether a device admits a medium, or whether a successful repair restored redundancy and was later revalidated.

The project should therefore preserve these stop conditions:

- `bit survival != intelligibility`;
- `fixity evidence != intelligibility`;
- `fixity evidence != complete authenticity proof`;
- `preservation metadata != preservation mechanism`;
- `documented dependency != available dependency`;
- `Representation Information != one concrete reader apparatus`;
- `environment description != executable environment`;
- `Designated Community relative understandability != timeless universal meaning`.

### Sources

- CCSDS, *Reference Model for an Open Archival Information System (OAIS)*, CCSDS 650.0-B-1, January 2002, preserved by UNT Libraries: <https://digital.library.unt.edu/ark:/67531/metadc123533/>.
- CCSDS, *Reference Model for an Open Archival Information System (OAIS)*, CCSDS 650.0-M-3, Issue 3, December 2024: <https://ccsds.org/publications/allpubs/entry/3054/>.
- PREMIS Working Group, *Data Dictionary for Preservation Metadata*, Version 1.0, May 2005: <https://www.loc.gov/standards/premis/v1/>.
- PREMIS Editorial Committee, *PREMIS Data Dictionary for Preservation Metadata*, Version 3.0, 2015: <https://www.loc.gov/standards/premis/v3/index.html>.

---

## 8. Adjacent traditions to map later

The first scaffold is incomplete. Later prior-art work should explicitly map:

- Friedrich Kittler and German media theory;
- Jussi Parikka and media archaeology;
- Gilbert Simondon on technical objects and individuation;
- Jacques Derrida on archive / trace where technically relevant;
- philosophy of information;
- history of writing, notation, accounting, and administrative records;
- archival science and preservation beyond the bounded OAIS/PREMIS slice;
- database history;
- digital preservation and emulation beyond the OAIS/PREMIS information-model and metadata boundary;
- forensic computing;
- infrastructure studies and maintenance studies;
- histories of bookkeeping, indexing, cataloging, and filing.

The test for inclusion is not `does this scholar mention memory?` but `does this work change how we can analyze technical retention?`

---

## Current novelty claim — deliberately modest

The working novelty claim is **not** that nobody has connected technology and memory.

That claim would be false.

It is also not that digital preservation first learns here that bits, formats, software/hardware environments, and interpretive context can diverge. OAIS and PREMIS already occupy that archival-level territory.

The narrower claim to test is:

> There is room for a source-controlled research program that follows retained state from mechanical and pre-electronic configurations through computer memory and modern distributed storage, compares the mechanisms along shared dimensions such as refresh, addressability, erasure, failure, maintenance, identity, currentness, integrity evidence, interpretation, and recovery apparatus, and uses those mechanisms to discipline philosophical interpretation while explicitly reusing rather than rediscovering archival digital-preservation prior art.

If later literature proves that this program has already been done substantially better, this repository should become an annotated map to that work rather than duplicate it.
