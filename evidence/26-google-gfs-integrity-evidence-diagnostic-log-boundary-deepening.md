# Case 26 Evidence Deepening — GFS integrity evidence, reconstructible state, and disposable diagnostic history

## Scope

This packet deepens [`cases/26-google-gfs-inactive-chunk-integrity.md`](../cases/26-google-gfs-inactive-chunk-integrity.md) around one bounded question:

> **Within the same early GFS design record, which kinds of “evidence about stored data and system history” are retained because correctness depends on them, which are reconstructed instead of persisted, and which may be discarded because they are only diagnostic?**

The slice is intentionally narrower than a general GFS history. It concentrates on four state classes that appear in the 2003 GFS paper and in Google patent `US7827214B1`:

1. per-block checksum state used to qualify chunk data;
2. the master operation log used to recover authoritative metadata history;
3. chunk-location state reconstructed from chunkservers rather than persistently stored by the master;
4. diagnostic/RPC logs useful for diagnosis but explicitly dispensable for filesystem correctness.

The packet does **not** claim that these four mechanisms share one implementation path, one persistence medium, or one historical genealogy. The point is precisely that the same system gives different state different lifetime rules according to recovery role.

Project labels used below:

- **H/P** — historical / primary-source record;
- **E** — engineering reconstruction;
- **A** — controlled functional analogy;
- **P** — philosophical interpretation.

`correctness-critical evidence`, `diagnostic narrative`, `reconstructible control state`, `retention class`, and `operative evidence` are **project engineering terms**, not vocabulary attributed to the GFS authors.

---

## Source custody and chronology

### Public 2003 system description

Sanjay Ghemawat, Howard Gobioff, and Shun-Tak Leung published **“The Google File System”** in the *Proceedings of the 19th ACM Symposium on Operating Systems Principles* in 2003. The Google Research record identifies the authors, venue, year, and pages 20–43.

The paper remains the repository's public-period terminology anchor for `chunk`, `chunkserver`, `checksum`, `valid replica`, `scan and verify`, `inactive chunks`, operation log, and the other GFS terms used by Case 26.

### Later-published patent record with 2003 priority/filing dates

Google patent **US7827214B1, “Maintaining data in a file system”**, names the same three inventors. The patent record gives:

- priority date: **2003-02-14**;
- U.S. filing date: **2003-06-30**;
- publication date: **2010-11-02**.

The description also states that the application claims priority from U.S. provisional applications filed on 2003-02-14 and 2003-04-03.

Chronology must therefore be stated carefully:

```text
2003 priority / filing lineage
    !=
2003 public publication of the patent text
```

This packet uses the 2010-published patent as a later-public primary legal record preserving a design disclosure whose filing lineage reaches 2003. It does **not** use the patent's priority date as proof that the full patent prose was publicly available before the 2003 SOSP paper.

Likewise, common inventors and strongly overlapping architecture do not by themselves prove a one-way causal relation between paper and patent.

---

## Historical record

### H/P — checksum state is retained because service and repair consult it

The patent's `Data Integrity` discussion says that each chunkserver can independently check the integrity of its own data. A chunk can be divided into 64 KB blocks, each with a corresponding 32-bit checksum, and those checksums may be stored **persistently**, possibly separately from chunk data.

On reads, the chunkserver can verify checksum blocks overlapping the requested range before returning data. A mismatch can be returned as an error and reported to the master. The requester can read another replica while the master can clone from another valid replica and later remove the corrupted one.

This yields a direct historical distinction:

```text
chunk payload
    !=
checksum relation used to qualify that payload
```

Both can be operationally necessary for future correct service, but they are not the same state.

The patent does not say that a checksum is an infallible proof of semantic correctness or authenticity. It is an integrity mechanism in the bounded design.

### H/P — inactive replicas are actively re-qualified

The patent says that during idle periods chunkservers may `scan and verify` inactive chunks. The stated purpose is to detect corruption in rarely read chunks. Once corruption is detected, the master can create a new uncorrupted replica and delete the corrupted one.

The explicit failure being prevented is especially important for retention: an inactive but corrupt replica can otherwise cause the master to believe that enough valid replicas remain.

So the period record itself distinguishes:

```text
replica physically present
    !=
replica currently qualified as a valid repair source
```

This is not merely a modern analogy imposed on the design; the source directly explains why inactive-corruption discovery matters to replica accounting.

### H/P — diagnostic logs are useful yet correctness-disposable

Immediately after the integrity discussion, the patent's `Diagnostic Tools` section describes detailed diagnostic logging of significant events and RPC requests/replies.

It then states a sharply different lifetime rule: those diagnostic logs **can be freely deleted without affecting filesystem correctness**. They may be retained while memory space permits. RPC logs can be collated across devices to reconstruct interaction history for diagnosis, load testing, and performance analysis.

This is a particularly useful historical negative case:

```text
a record is useful for reconstructing what happened
    !=
filesystem correctness requires that record to survive
```

The source therefore refuses a broad category such as “history must be retained.” Some history is optional diagnostic evidence.

### H/P — the operation log is a different kind of history

Elsewhere in the same patent description, the master operation log is described as a **persistent historical record of critical metadata changes**. The design can delay making metadata modifications visible until corresponding log records are persistent, replicate the operation log, replay it during recovery, and checkpoint it.

This is deliberately routed to [`cases/46-google-gfs-master-log-checkpoint-recovery.md`](../cases/46-google-gfs-master-log-checkpoint-recovery.md) for full treatment. Case 26 needs only the boundary:

```text
persistent operation history required for authoritative recovery
    !=
diagnostic interaction history useful only for diagnosis
```

The two are both “logs” in ordinary language, but the source gives them different correctness roles and therefore different retention requirements.

### H/P — chunk-location state is reconstructed instead of retained by the master

The patent also says that master chunk-location information is **not persistently stored**. On startup the master can ask chunkservers which chunks they store and then keep the resulting view current through placement decisions, heartbeat exchanges, and later reports.

Again, detailed master-state treatment belongs to Case 46. For this packet the bounded historical point is:

```text
state required at runtime
    !=
state that must be persisted in that runtime representation
```

The design can recover some runtime control state by re-observing surviving authoritative embodiments.

### H/P — one design therefore exposes at least four lifetime rules

The source record supports the following classification without importing a later storage taxonomy:

| State / relation | Period-described lifetime strategy | Bounded role |
| --- | --- | --- |
| chunk checksums | persistent | integrity qualification before service / repair |
| master operation log | persistent, replicated, replayed/checkpointed | authoritative metadata recovery |
| master chunk-location view | not persistently stored by master; rediscovered | runtime routing / replica-location knowledge |
| diagnostic and RPC logs | deletable without affecting correctness | diagnosis / trace reconstruction / analysis |

The table is a project organization of source statements. The historical actors did not present it as a four-class “retention ontology.”

---

## Engineering reconstruction

### E — “metadata” is too broad a retention category

The same system can contain non-payload information with radically different survival requirements. Calling all of it `metadata` hides the engineering distinction.

A safer reconstruction is:

```text
state lifetime
    follows
future recovery / correctness role

not merely

payload vs metadata label
```

A checksum relation must remain available because a future read or repair may consult it. A diagnostic RPC transcript may be extremely useful yet still be unnecessary for correct service. A location view may be necessary at runtime but reconstructible after restart.

### E — correctness evidence and diagnostic evidence are different

The patent gives a unusually clean within-system counterexample to the idea that all observability should be retained equally:

```text
integrity checksum
    -> participates in deciding whether stored data may be trusted

diagnostic log
    -> participates in explaining past behavior
```

Therefore:

```text
useful evidence about the system
    !=
correctness-critical evidence for the system
```

This does not imply diagnostic history is operationally worthless. It means its loss has a different consequence class.

### E — deletion of narrative history need not erase operative correctness state

Because diagnostic logs may be deleted without affecting correctness while checksums and authoritative log relations follow different rules, the design demonstrates a bounded principle:

```text
loss of explanatory history
    !=
loss of all state required for correct future service
```

A later investigator may lose the ability to reconstruct an incident while the filesystem remains able to qualify data and recover its authoritative state.

The inverse is also possible in principle: retaining rich diagnostics does not substitute for preserving the checksum or authoritative metadata relations that correctness actually consumes.

### E — reconstruction can substitute for persistence only under a defined source relation

The non-persistent master location view should not be generalized into “state need not be saved because it can always be recomputed.” Here reconstruction has an identified source: chunkservers report the chunks they store at startup, and the master subsequently maintains the view from its placement authority and heartbeat/report traffic.

Thus:

```text
reconstructible
    requires
surviving authoritative embodiments
+ discovery protocol
+ enough identity/currentness information
```

If those premises are unavailable, the source does not establish that reconstruction remains possible.

### E — maintenance need not preserve a full transcript of itself

Inactive-chunk scanning changes what the system knows about repair margin, but the cited record does not require retaining a permanent, exact transcript of every scan step. What the design demonstrably needs is enough retained/reconstructed state to keep serving, detecting corruption, reporting it, and restoring valid replicas.

So the safe claim is:

```text
maintenance occurred / can recur
    !=
a complete maintenance narrative must be retained forever
```

This is **not** a claim that GFS scan cursors or progress state were definitely volatile; the source inspected here does not specify their full persistence semantics.

### E — redundancy count is only as good as its qualification relation

The integrity path also sharpens the familiar replica-count problem:

```text
N physical replicas
    !=
N known-valid repair sources
```

A latent-corrupt inactive copy can temporarily inflate apparent redundancy until a read or background verification exercises the checksum relation. The repair margin is therefore partly epistemic in the narrow engineering sense: the system needs evidence that a replica still satisfies the validity conditions under which it may be counted.

This does not make the underlying corruption “merely informational”; physical media faults remain physical faults.

---

## Controlled functional comparisons

### A — Case 46: persistent authoritative history vs reconstructible runtime view

[`cases/46-google-gfs-master-log-checkpoint-recovery.md`](../cases/46-google-gfs-master-log-checkpoint-recovery.md) treats the master operation log and checkpoint as its main subject. Case 26 should not duplicate that history.

The useful cross-case boundary is:

```text
operation log
    = retained authoritative transition history

chunk-location view
    = runtime state reconstructed from chunkservers

diagnostic logs
    = optional explanatory history
```

These are three distinct strategies inside one documented architecture, not three names for the same persistence mechanism.

### A — Synthesis 29: observability is not closure

[`docs/SYNTHESIS_29_MAINTENANCE_OBSERVABILITY_COVERAGE_ACCOUNTING.md`](../docs/SYNTHESIS_29_MAINTENANCE_OBSERVABILITY_COVERAGE_ACCOUNTING.md) separates maintenance execution, coverage, accounting, and closure.

Case 26 contributes a complementary boundary: retaining a diagnostic trace that says something happened is not itself the same as retaining the integrity relation that qualifies a replica or completing the repair that restores redundancy.

```text
diagnostic trace
    !=
integrity qualification
    !=
repair completion
```

This is a functional synthesis, not historical terminology.

### A — Case 38: observability can be lossy without defining mechanism correctness

Case 38's S3700 evidence separates PLI mechanism state from bounded SMART observability. GFS gives a different mechanism but a compatible caution: diagnostic history can be lossy/disposable while correctness-critical state follows other lifetime rules.

No lineage between SMART telemetry and GFS diagnostic logs is implied.

### A — Case 153: exact worker state need not be the recoverable obligation

Case 153 shows a Ceph cleanup obligation that can be reconstructed from retained relations rather than preserving exact worker-queue state. GFS master location rediscovery is functionally comparable at a very high level:

```text
exact previous runtime representation
    !=
minimum authority needed to reconstruct a usable runtime state
```

The underlying protocols, eras, and data structures are different. This is not a genealogy claim.

---

## Prior-art and terminology boundary

This packet does not move the repository's public terminology floor for `scan and verify` earlier than the 2003 GFS paper. The patent's priority and filing chronology is useful for design-lineage context, but the inspected patent publication itself is dated 2010-11-02.

Accordingly, the safe chronology is:

```text
2003 GFS paper
    -> public period record of checksum verification and inactive scan-and-verify

US7827214B1
    -> 2003 priority / filing lineage
    -> patent text published in 2010
    -> later-public primary record that independently preserves the same bounded design family
```

Do **not** rewrite this as:

```text
patent published in February 2003
```

or:

```text
patent proves GFS invented proactive integrity verification
```

or:

```text
patent proves later scrub systems descend from GFS
```

The patent is especially valuable here because it places persistent checksum state, reconstructible location state, persistent operation history, and disposable diagnostic history into one source family.

---

## Philosophical interpretation

The bounded philosophical result is selective rather than totalizing.

A technical system can preserve several different relations to its own past:

- some past transitions are retained because future authoritative state depends on replaying or checkpointing them;
- some current relations are retained because future service must test against them;
- some runtime views are rebuilt from surviving sources rather than preserved in their old representation;
- some narratives of what happened may be discarded even though they would make the system easier to understand later.

This supports a project-level distinction:

```text
operative memory
    !=
explanatory history
```

A system can remain technically capable of correct continuation while becoming harder for an observer to narrate or diagnose. Conversely, a rich narrative log does not by itself preserve the operative relations needed for correct continuation.

This vocabulary is philosophical interpretation by this repository. It is **not** attributed to Ghemawat, Gobioff, Leung, Google, or the patent.

---

## Explicit non-claims

This evidence packet does **not** establish any of the following:

1. Google or GFS invented checksums.
2. Google or GFS invented replicated storage.
3. Google or GFS invented background integrity verification.
4. The 2010 patent publication was publicly available in 2003.
5. A patent priority date is the same as a publication date.
6. The patent text is word-for-word identical to the 2003 SOSP paper.
7. Common inventors prove the paper caused the patent or the patent caused the paper.
8. Every GFS implementation exactly matched every optional `may` statement in the patent.
9. A 32-bit checksum detects every possible corruption.
10. A matching checksum proves semantic correctness, authenticity, freshness, or current chunk version.
11. A checksum is equivalent to a cryptographic authentication tag.
12. Three physical replicas imply three currently valid repair sources.
13. A successful alternate read means the configured replication goal has already been restored.
14. Detection of corruption is the same event as completed re-replication.
15. Inactive chunks were scanned on one fixed universal period.
16. The source specifies persistence semantics for every scan cursor or scan-progress field.
17. Diagnostic logs were never written to persistent storage.
18. Diagnostic logs were useless because correctness did not depend on them.
19. Deleting diagnostic logs preserves the ability to diagnose every past incident.
20. Retaining diagnostic logs could substitute for checksum integrity state.
21. Master location data was unnecessary because it was not persisted.
22. Any arbitrary runtime state can be reconstructed after a crash.
23. Reconstruction is possible after loss of the authoritative sources from which the state is rebuilt.
24. The operation log is merely diagnostic history.
25. The operation log can be freely deleted under the same rule as diagnostic RPC logs.
26. GFS's `scan and verify` should be historically renamed `scrub`.
27. The patent establishes a historical lineage from GFS to ZFS scrub, Dynamo anti-entropy, Ceph scrub, SMART telemetry, or later distributed-storage maintenance.
28. The distinction between `operative memory` and `explanatory history` is historical GFS vocabulary.
29. The patent's legal claims are being evaluated here for validity, enforceability, or priority over other systems.
30. This packet closes the broader history of distributed-filesystem integrity maintenance.

---

## Claim ledger

| Claim | Label | Evidence / status |
| --- | --- | --- |
| GFS paper publicly documents the system in SOSP 2003 | H/P | Google Research publication record |
| US7827214B1 names Ghemawat, Gobioff, Leung and Google | H/P | patent bibliographic record |
| patent priority is 2003-02-14 and filing is 2003-06-30 | H/P | patent bibliographic / priority table |
| inspected patent publication is dated 2010-11-02 | H/P | patent publication record |
| per-64 KB checksums may be stored persistently | H/P | patent `Data Integrity` description |
| reads can verify overlapping checksum blocks before return | H/P | patent `Data Integrity` description |
| inactive chunks may be scanned and verified during idle periods | H/P | patent `Data Integrity` description |
| corruption can trigger repair from another valid replica | H/P | patent `Data Integrity` description |
| diagnostic logs may be deleted without affecting filesystem correctness | H/P | patent `Diagnostic Tools` description |
| RPC logs can reconstruct interaction history for diagnosis | H/P | patent `Diagnostic Tools` description |
| master operation log is a persistent historical record of critical metadata changes | H/P | patent master-metadata description; routed to Case 46 |
| master chunk-location state is not persistently stored and is rediscovered from chunkservers | H/P | patent master-metadata description; routed to Case 46 |
| useful evidence ≠ correctness-critical evidence | E | reconstruction from checksum / diagnostic-log contrast |
| runtime-needed state ≠ state that must persist in the same representation | E | reconstruction from location rediscovery |
| explanatory history loss ≠ automatic correctness loss | E | bounded reconstruction from diagnostic-log deletion rule |
| rich diagnostic history ≠ substitute for integrity / authoritative recovery state | E | bounded reconstruction from source role separation |
| GFS gives multiple retention strategies inside one architecture | E | synthesis of primary-source state classes |

---

## Sources

### Primary system publication

Sanjay Ghemawat, Howard Gobioff, Shun-Tak Leung, **“The Google File System,”** *Proceedings of the 19th ACM Symposium on Operating Systems Principles (SOSP)*, 2003, pp. 20–43.

- Google Research: <https://research.google/pubs/the-google-file-system/>
- repository canonical anchors: §§4.3, 4.5, 5.2.

### Primary legal/design record

Sanjay Ghemawat, Howard Gobioff, Shun-Tak Leung, **US7827214B1, “Maintaining data in a file system,”** Google LLC.

- priority date: 2003-02-14;
- filing date: 2003-06-30;
- publication date: 2010-11-02;
- Google Patents text: <https://patents.google.com/patent/US7827214B1/en>
- bounded inspected sections: master metadata / location / operation log; `Data Integrity`; `Diagnostic Tools`; bibliographic/priority/publication tables.

### Repository controls

- [`cases/26-google-gfs-inactive-chunk-integrity.md`](../cases/26-google-gfs-inactive-chunk-integrity.md) — canonical Case 26.
- [`cases/46-google-gfs-master-log-checkpoint-recovery.md`](../cases/46-google-gfs-master-log-checkpoint-recovery.md) — operation-log/checkpoint and master-state recovery; do not duplicate its technical history here.
- [`docs/SYNTHESIS_29_MAINTENANCE_OBSERVABILITY_COVERAGE_ACCOUNTING.md`](../docs/SYNTHESIS_29_MAINTENANCE_OBSERVABILITY_COVERAGE_ACCOUNTING.md) — observability / closure distinction.
- Case 38 PLI observability evidence — telemetry-lifetime functional comparison only.
- Case 153 snap-trim evidence — reconstructible-obligation functional comparison only.

### Related-repository duplication check

`tmzncty/computing-archaeology` was searched again for GFS / Google File System / checksum / inactive-chunk integrity / diagnostic logs. No dedicated reusable technical-history packet was found for this bounded slice. A broader history of GFS, Google storage architecture, or checksum practice should still be routed there rather than duplicated here.

---

## Status

**Bounded deepening complete; canonical Case 26 remains `grounded`.**

This packet closes one narrow debt: it gives Case 26 a source-grounded within-system distinction among **persistent integrity evidence**, **persistent authoritative operation history**, **reconstructed runtime location state**, and **disposable diagnostic history**.

It does **not** close:

- exact persistence/restart semantics for inactive-scan progress;
- an empirical fault-injection trace showing latent corruption discovery and replica replacement;
- checksum corruption / metadata-loss combinations;
- later GFS / Colossus integrity-maintenance evolution;
- broader distributed-filesystem scrub genealogy;
- legal patent-priority analysis beyond the bibliographic chronology recorded above.
