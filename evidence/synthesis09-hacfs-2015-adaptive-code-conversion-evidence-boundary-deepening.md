# Synthesis 09 deepening — HACFS 2015 adaptive code conversion and the crash-safety evidence boundary

Status: **bounded cross-case deepening complete**

Parent synthesis: [`../docs/SYNTHESIS_09_DISTRIBUTED_CODED_SERVICE_REPAIR_PLACEMENT.md`](../docs/SYNTHESIS_09_DISTRIBUTED_CODED_SERVICE_REPAIR_PLACEMENT.md)

Primary comparison anchor: [`Case 24 — Windows Azure Storage LRC`](../cases/24-windows-azure-lrc-repair-locality-handoff.md)

Roadmap seam advanced: **failed/asynchronous redundancy-mode conversion, stale/incomplete completion metadata, or premature retirement of a source representation**. This packet advances only the **conversion-state / publication-evidence** part of that seam. It does not close the broader adversarial item.

---

## 1. Bounded question

Synthesis 09 already uses Windows Azure Storage (2012) to show that a redundancy-regime transition can have retained progress, validation, completion metadata, and a later retirement step for the old full replicas.

That positive witness leaves a useful adversarial question:

> If another system dynamically changes the code interpreting an otherwise stable data file, what evidence is required before we may call the transition crash-safe, restartable, or complete?

Mingyuan Xia, Mohit Saxena, Mario Blaum, and David A. Pease, **“A Tale of Two Erasure Codes in HDFS,”** FAST ’15, supplies a deliberately different witness. Their HACFS prototype dynamically converts files between a `fast` and a `compact` erasure code. The paper explicitly retains a per-file `coding state`, invokes `upcode` and `downcode` transitions, and runs conversion work as background MapReduce jobs.

That is enough to establish a real representation-transition problem.

It is **not** enough, from the inspected publication alone, to establish a crash-safe handoff protocol between old parity, new parity, and the file’s coding-state interpretation.

The bounded result is therefore a source-discipline result:

```text
dynamic code conversion documented
    !=
crash-safe code-conversion handoff documented
```

and:

```text
coding-state field exists
    !=
transition currentness / atomic publication semantics established
```

This distinction is useful precisely because it prevents a performance/evaluation paper from being silently upgraded into evidence for a stronger persistence contract than it actually describes.

---

## 2. Source custody and scope

### Primary HACFS source

Mingyuan Xia, Mohit Saxena, Mario Blaum, and David A. Pease, “A Tale of Two Erasure Codes in HDFS,” *13th USENIX Conference on File and Storage Technologies (FAST ’15)*, Santa Clara, February 2015, pp. 213–226.

- USENIX landing page: <https://www.usenix.org/conference/fast15/technical-sessions/presentation/xia>
- USENIX paper PDF: <https://www.usenix.org/system/files/conference/fast15/fast15-paper-xia.pdf>

The paper says HACFS is implemented as an extension to HDFS/HDFS-RAID and evaluated with workload distributions obtained from production clusters. The bounded historical object here is therefore the **2015 HACFS research implementation and its published description**, not a claim that HACFS itself was deployed as a production filesystem at Facebook, Cloudera customers, or IBM.

### Positive comparison source already owned by Case 24

Cheng Huang et al., “Erasure Coding in Windows Azure Storage,” *USENIX ATC ’12*, June 2012.

- <https://www.usenix.org/conference/atc12/technical-sessions/presentation/huang>

Case 24 and Synthesis 09 already own the detailed WAS historical record. This packet reuses those grounded facts rather than rebuilding the Azure case.

### Related-repository check

A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `HACFS` found no dedicated packet. Broader histories of HDFS-RAID, adaptive coding, AutoRAID-like tiering, or erasure-code research genealogy should still be routed there if needed. This file keeps only the retention-specific representation-handoff question.

---

## 3. Claim discipline

### Historical record (`H`)

Historical claims below are limited to what Xia et al. describe in the FAST ’15 paper:

- HACFS maintains per-file and global system state;
- the file state includes a `coding state`;
- upcode/downcode convert between fast and compact codes;
- those conversions can modify parity while leaving data blocks unchanged;
- the implementation invokes conversion from an adaptive state machine;
- encoding/conversion run as background MapReduce work;
- the reported fault injector exercises block, disk, and node failure paths for degraded reads/reconstruction.

### Engineering reconstruction (`E`)

The following are project vocabulary, not historical HACFS terms:

- `representation handoff`;
- `transition currentness`;
- `interpretive metadata`;
- `publication gate`;
- `transition-safe ordering`;
- `source/target redundancy representation`.

### Functional analogy (`A`)

HACFS is compared with WAS only because both expose a change in the redundancy representation used to retain an object/file. The comparison does not establish shared code, shared protocol, shared ancestry, or equivalent fault models.

### Philosophical interpretation (`P`)

A final section asks what it means for stable payload blocks to remain while the relation that makes them recoverable is changed. That is an interpretation downstream of the engineering record, not a claim made by Xia et al.

---

## 4. Historical record — HACFS makes coding state explicit

### H — the adaptive module maintains file state and manages transitions

Xia et al. describe HACFS as an HDFS-RAID extension. The adaptive coding module “maintains the system states of erasure-coded data” and manages state transitions.

The per-file state includes:

- file size;
- last modification time;
- read count;
- **coding state**.

The paper then defines the coding state as representing whether a file is three-way replicated or which erasure-coding scheme is used for it.

**Primary anchor:** FAST ’15 PDF p. 216–217, §3.1, especially the `System States` paragraph and Figure 5.

For this repository, the important historical fact is not merely that HACFS has configuration. It is that the system retains a field whose interpretation determines **which redundancy relation is currently supposed to apply to the file**.

This blocks the shortcut:

```text
same data blocks physically present
    -> same retained representation
```

because a file can be associated with different parity/code relations while its payload data blocks remain the same.

---

## 5. Historical record — upcode/downcode can be parity-only representation change

### H — the coding interfaces separate payload data from parity transformation

HACFS exposes four coding interfaces: `encode`, `decode`, `upcode`, and `downcode`.

The paper says `upcode` and `downcode` convert a data-file representation between two coding schemes. Both conversion operations update the associated parity file when the coding scheme changes. For the Product-code upcode path, the paper is especially explicit: the conversion need not read the data file and is a **parity-only transformation**.

The Product-code construction preserves the data and vertical parity blocks while recomputing selected horizontal/global parities. The LRC conversion likewise preserves the global parities in the described collapsing construction while changing local parities.

**Primary anchors:** FAST ’15 PDF p. 217, Table 1 and `Coding Interfaces`; pp. 219–220, Product/LRC `Upcoding and Downcoding`.

This gives a clean retention-specific distinction:

```text
payload embodiment unchanged
    !=
redundancy representation unchanged
```

and:

```text
code conversion
    !=
payload migration
```

The system can change the repair/reconstruction relation around data that itself did not move.

---

## 6. Historical record — conversion is state-machine work, not one instantaneous algebraic operation

### H — state transitions invoke conversion based on retained workload/system state

The HACFS state machine chooses between fast and compact codes according to file read counts and a global storage bound. The implementation section says the extended state machine retrieves file coding state and launches MapReduce jobs to upcode files into the compact code; it can later downcode them into the fast code and update coding state.

The paper also says the upcode/downcode operations change the coding state of the data file. In the HDFS-RAID initial encoding path it reports a separate transition in which a write-cold file is encoded, then its replication level is reduced to one and its coding state changes to Reed–Solomon.

**Primary anchors:** FAST ’15 PDF pp. 217–218, `State Transitions`; pp. 220–221, `HACFS and Two Erasure Codes`.

The HDFS-RAID sentence is evidence **as reported by Xia et al.** It is not treated here as an independent source-level audit of the exact HDFS-RAID implementation ordering.

### H — conversion runs in background MapReduce jobs

The evaluation states that the HDFS-RAID-based systems schedule encoding and conversion operations as background MapReduce jobs to reduce their impact on user jobs. For some workloads, conversion accounts for up to 18% of total encoding time.

**Primary anchor:** FAST ’15 PDF p. 224, §5.5 `Encoding and Conversion Time`.

Thus the transition has nonzero duration and resource cost. It is not merely a mathematical relabeling.

```text
conversion requested
    !=
conversion work finished
```

This is enough to make interruption/currentness questions technically meaningful even though the paper does not answer all of them.

---

## 7. Historical record — the published fault injection targets recovery, not conversion interruption

### H — the fault injector exercises block/disk/node loss paths

The implementation includes a fault injector outside HDFS. The paper describes:

- deleting one local block to trigger a degraded read;
- deleting all data on a disk and restarting a DataNode to simulate disk failure;
- killing a DataNode process to simulate node failure.

The resulting paths exercise missing-block detection and reconstruction jobs.

**Primary anchor:** FAST ’15 PDF p. 221, §4 `Implementation`.

In the inspected publication, this fault-injection description does **not** report an experiment that interrupts `upcode` or `downcode` between parity transformation and coding-state change, then restarts HACFS and verifies the resulting representation.

That negative statement is intentionally narrow:

```text
reconstruction fault injection reported
    !=
conversion-crash fault injection reported
```

It does **not** imply that the implementation lacked internal safeguards.

---

## 8. Source-coverage boundary — what the FAST ’15 paper does not establish

Full-text inspection of the paper was targeted at the conversion and implementation sections, including searches for restart/transactional vocabulary. The publication clearly describes the *function* and *cost* of conversion, but it does not provide a protocol-level account sufficient to establish the following stronger propositions:

1. a persistent `conversion-in-progress` record exists;
2. interrupted upcode/downcode is resumed rather than restarted or recomputed;
3. parity-file replacement and coding-state publication form one atomic transaction;
4. a crash between target-parity production and coding-state update has a specified recovery rule;
5. a crash after coding-state update but before target parity reaches the required persistence boundary has a specified recovery rule;
6. old parity is preserved until the target representation is validated/admissible;
7. target parity is decoded/checksummed against an independent source before the old code becomes retireable;
8. a completion marker distinct from `coding state` exists;
9. an incomplete conversion is rolled back safely;
10. MapReduce job completion is itself the publication/durability gate;
11. conversion progress survives RaidNode restart;
12. the experiment suite injects a failure into the conversion handoff itself.

The correct historical formulation is:

> **These semantics are not established by the inspected FAST ’15 publication.**

The incorrect formulation would be:

> **HACFS did not implement them.**

The second claim would require source code, design documentation, issue history, or a direct failure experiment that this packet does not possess.

---

## 9. Engineering reconstruction — parity bytes and coding state form one interpreted redundancy relation

The paper supports a minimal project model:

```text
data blocks
    + parity representation
    + coding state
    -> currently interpreted redundancy regime
```

The important word is `interpreted`.

A parity file only has reconstruction meaning relative to the code that tells the system how to combine it with the data blocks. Conversely, a coding-state value naming a target code is not useful if the corresponding target parity representation is not actually present and admissible.

Therefore:

```text
new parity bytes exist
    !=
target coding state is authoritative
```

and:

```text
target coding state published
    !=
target parity is proven complete/durable/valid
```

unless a source establishes the ordering and completion contract connecting them.

This is an engineering reconstruction from the published architecture. The paper does not use the term `interpretive metadata`.

---

## 10. Engineering reconstruction — the missing handoff relation

A safe conversion protocol might, in the abstract, need to order facts resembling:

```text
source representation authoritative
    -> target parity production starts
    -> target parity complete
    -> target parity validated / persisted
    -> target coding state becomes authoritative
    -> source-only parity becomes retireable
    -> cleanup converges
```

But this sequence is **not** attributed to HACFS.

It is a diagnostic checklist used to ask what would have to be evidenced before stronger claims are made.

The FAST ’15 paper directly grounds only part of this picture:

```text
source coding state
    -> background conversion work
    -> parity transformation
    -> coding-state change
```

It does not publish enough ordering/restart detail to place all intermediate persistence and validation gates between those nodes.

Accordingly:

```text
state machine shown
    !=
crash-recovery state machine shown
```

and:

```text
background job completion
    !=
representation-handoff closure
```

without further evidence.

---

## 11. Cross-check — WAS 2012 documents a stronger handoff contract

Case 24 already records a useful positive contrast from Huang et al. 2012.

For sealed extents, the WAS paper describes asynchronous erasure coding in which:

- coding progress is persisted into the new fragments so another Extent Node can resume work after a failure;
- the new coded representation is checked with decoding combinations and CRCs;
- failed validation aborts the conversion while full extent copies remain intact;
- fragment boundaries and completion flags are recorded;
- old full replicas are scheduled for deletion only after the documented completion sequence.

That lets Case 24/Synthesis 09 state a much stronger publication-level relation:

```text
old full replicas
    -> persisted target-conversion progress
    -> validation
    -> completion/admissibility metadata
    -> old replicas become retirement candidates
```

HACFS and WAS therefore differ in **what their inspected publications make available as evidence**.

The safe comparison is:

```text
WAS paper documents explicit restart/validation/retirement gates
    !=
HACFS paper documents no such gates in inspected conversion sections
```

The unsafe comparison would be:

```text
WAS implementation was necessarily safer than HACFS
```

Publication detail is not a direct measurement of implementation quality.

---

## 12. Why this is a useful adversarial control for Synthesis 09

Synthesis 09 already warns:

```text
target fragments present
    !=
representation handoff complete
```

HACFS sharpens the warning in a different direction. Here the data blocks can remain stable while parity changes and a small coding-state field determines how those blocks are to be interpreted for recovery.

This yields three separate relations:

```text
payload continuity
    !=
redundancy-representation continuity
    !=
transition-currentness evidence
```

A file can retain all payload blocks while the system is still changing the parity relation that gives future failures their repair path.

That is exactly why `failed/asynchronous redundancy-mode conversion` deserves its own roadmap adversarial seam rather than being folded into generic `data survived` language.

---

## 13. Functional analogy — bounded and non-genealogical

HACFS can be compared functionally with other repository cases where an identity survives a representation change:

- mapped Flash changes physical embodiment behind a logical address;
- WAS changes a sealed extent from full replication to LRC;
- Swift changes admissible EC object-version state through durability/currentness metadata;
- filesystems can replace one metadata/body representation while preserving a stable namespace identity.

The comparison is only:

```text
stable logical object
    can depend on
changing auxiliary representation + retained interpretation state
```

It does **not** establish that HACFS inherited an FTL-style commit protocol, that WAS influenced HACFS handoff semantics, or that these systems share one implementation pattern.

---

## 14. Philosophical interpretation — persistence can include persistence of the rule of reconstruction

The HACFS case makes one interpretive point unusually visible.

If payload data blocks stay fixed while parity changes from one code to another, what persists is not only matter or bytes. The usable future of those bytes also depends on retaining the correct rule under which missing pieces will later be reconstructed.

In project vocabulary:

> Technical persistence can require persistence not only of a payload, but of the **current relation that makes the payload repairable**.

That relation can change without changing the payload itself.

This should not be inflated into a claim that `coding state` is human meaning, memory, or interpretation in a hermeneutic sense. It is a bounded technical dependency: the system must know which coding relation currently qualifies its parity and data.

---

## 15. Explicit non-claims

This packet does **not** claim that:

1. HACFS loses data during upcode or downcode;
2. HACFS lacks a crash-safe implementation;
3. parity replacement in HACFS is non-atomic;
4. the `coding state` field is volatile;
5. the `coding state` field is definitely persisted in one particular HDFS metadata object;
6. a MapReduce job success response is definitely the durable publication boundary;
7. old parity is deleted before new parity is safe;
8. target parity can be observed under the wrong coding state in the actual implementation;
9. an interrupted conversion necessarily leaves a mixed-code file;
10. the absence of `crash`, `atomic`, `transaction`, or `resume` protocol prose in the paper proves the absence of such code;
11. HACFS was deployed in the production clusters whose workload distributions were used for evaluation;
12. workload traces from production make HACFS itself a production system;
13. the 11-node evaluation cluster proves exabyte-scale transition safety;
14. the paper’s block/disk/node fault injector tests conversion interruption;
15. Product-code and LRC conversion have identical intermediate states;
16. parity-only conversion means the operation is risk-free;
17. unchanged data blocks imply unchanged recoverability;
18. HDFS-RAID’s reported `encode -> reduce replication -> change coding state` sentence is a complete source-level transaction audit;
19. HACFS and WAS share a direct implementation lineage;
20. the stronger handoff detail published for WAS proves a stronger implementation than HACFS;
21. all adaptive erasure-code systems require one universal transaction protocol;
22. coding-state persistence is sufficient without payload/parity integrity;
23. target parity integrity is sufficient without currentness/interpretation metadata;
24. this packet closes the roadmap’s entire failed/asynchronous conversion adversarial branch.

---

## 16. Roadmap status after this slice

This packet **partially advances but does not close** the roadmap item concerning failed/asynchronous redundancy-mode conversion, stale/incomplete completion metadata, or premature source retirement.

What is now grounded from the FAST ’15 publication:

```text
real adaptive code conversion exists
    +
per-file coding state exists
    +
conversion has nonzero/background execution duration
    +
payload can remain unchanged while parity representation changes
    +
reported recovery fault injection is not conversion-crash injection
```

What remains open for HACFS specifically:

- source/design evidence for where `coding state` is stored and how it survives RaidNode/process restart;
- exact ordering between target parity creation/replacement and coding-state update;
- whether an intermediate `conversion in progress` state exists;
- rollback, retry, idempotence, or resume semantics after interrupted up/downcode;
- whether old parity is retained until target-code admissibility is established;
- exact persistence/fsync/rename semantics of parity-file replacement;
- a mid-conversion fault-injection test followed by restart and recovery;
- source-level verification of the HDFS-RAID initial `encoding -> replication reduction -> coding-state change` handoff rather than relying on the FAST ’15 summary.

These are narrow, testable debts. They are preferable to another generic survey of erasure coding.

---

## 17. Result

The useful result of this slice is not a newly alleged HACFS bug. It is a sharper evidentiary threshold for talking about redundancy-mode transitions.

The FAST ’15 paper directly supports:

```text
retained coding state
    +
background parity transformation
    +
dynamic code transitions
```

It does not, by itself, support:

```text
crash-safe / restartable / atomic representation handoff
```

Case 24 shows what stronger evidence looks like when a source actually documents progress persistence, validation, completion metadata, and old-representation retirement ordering.

Therefore the repository should preserve this boundary:

> **A paper that proves a conversion algorithm and evaluates its cost is not automatically evidence for the crash semantics of the conversion’s representation handoff.**
