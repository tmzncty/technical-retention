# ZFS Dirty Time Log: Retained Failure Intervals and Selective Resilver

**Status:** `grounded`

## Scope

This case asks one bounded retention question:

> How can a storage system retain enough evidence about *when* one redundant device failed to receive state so that later repair can select only blocks exposed during that interval, rather than treating the whole device as equally suspect?

The historical core is bounded to the Sun ZFS dirty-time-log / resilver patent family with a **2005-11-04 priority floor** and **2007-05-10 publication witnesses**. Oracle Solaris operational documentation is used as a product-level witness that ZFS can resilver only the minimum necessary data after a short outage. OpenZFS 2.1.11 source is used only as a later implementation-continuity witness for DTL classes and persistence/derivation boundaries.

This case is not:

- a generic ZFS history;
- a second scrub case (Case 18 already covers proactive verification and checksum-qualified healing);
- a second RAID-Z write-hole case (Case 95);
- a second dRAID sequential-rebuild case (Case 96);
- proof that Sun/ZFS invented dirty logging or selective mirror recovery;
- proof that every ZFS release implements every patent-family embodiment exactly as written;
- a claim that a DTL proves stored payload is corrupt.

A repository search found no dedicated DTL/resilver case in `tmzncty/computing-archaeology`; broader dirty-log, mirror-recovery, and ZFS implementation genealogy belongs there rather than being duplicated here.

## Historical vocabulary

Historical / source vocabulary retained here:

- `dirty region logging` / `DRL`;
- `dirty time log` / `DTL`;
- `birth time`;
- `transaction group`;
- `resilver` / `resilvering`;
- `pruned resilvering`;
- `minimum amount of necessary data`.

Project engineering vocabulary:

- **failure-exposure history** — retained evidence of intervals during which a redundant target had less than the required replication relation;
- **repair-scope witness** — metadata sufficient to decide that a block or subtree can be excluded from a later catch-up pass;
- **repair debt** — a still-retained obligation to restore redundancy after the device becomes available again.

The project terms are analytical reconstructions, not Sun/Oracle historical terminology.

## Historical record

### H/P — dirty-region logging already provided selective recovery before ZFS DTL

Sun Cluster 2.2 documentation describes `Dirty Region Logging (DRL)` as tracking regions changed by writes to a mirrored volume. A status bit represents each logical region; a newly dirty region is synchronously logged before the data write, and after restart only regions marked dirty need recovery.

That is an explicit pre-ZFS functional prior-art floor for **bounded recovery instead of full-copy recovery**.

It does not make DRL and ZFS DTL identical. DRL is region-oriented and incurs logging work when regions transition dirty. The later ZFS DTL family instead exploits block birth time / transaction-group relations to record intervals of unsuccessful storage and decide whether specific blocks need resilvering.

### H/P — the ZFS patent family has a 2005-11-04 priority floor

Sun's later patent-family records claim benefit of provisional application 60/734,023, filed **2005-11-04**, titled `Dirty Time Logging and Resilvering`, naming William H. Moore and Jeffrey S. Bonwick. Related applications published on **2007-05-10** include:

- `Method and system for dirty time logging` (`US20070106869A1`, later `US7925827B2`);
- `Method and system for dirty time log directed resilvering` (`US20070106867A1`, later `US7930495B2`);
- `Method and system for pruned resilvering using a dirty time log` (`US20070106677A1`, later `US8635190B2`);
- `Method and system for metadata-based resilvering` (`US20070106866A1`, later `US8938594B2`).

This is a date-bounded documentary floor, not an invention-priority claim and not by itself proof of the first shipping implementation.

### H/P — DTL records failed-replication time / transaction-group state

The patent-family description associates a DTL with storage devices and says it tracks times during which I/O requests were not successfully completed on a device. It explicitly allows transaction-group numbers to stand for those times, and explains `birth time` as either time or transaction-group number in the described embodiments.

The important historical relation is therefore not simply `block is dirty` but:

```text
block birth txg
    compared with
interval(s) in which one target did not receive required writes
```

### H/P — birth time plus DTL can bound block-level repair

The dirty-time-logging application describes updating the DTL with a block's birth time when a storage attempt is unsuccessful. The directed/pruned resilver family then uses those birth times to decide which blocks require resilvering.

The pruned-resilver application states that a child block is resilvered when its birth time is in the DTL and that a branch need not be traversed when parent/descendant birth-time ordering makes intersection with the DTL impossible. Its worked example uses DTL birth times / transaction groups 32–37 for an offline disk and treats blocks outside that interval as not requiring resilvering under the described conditions.

Thus retained time/txg metadata can reduce future traversal as well as future write work.

### H/P — product documentation exposes the selective-repair outcome

Oracle's Solaris ZFS administration documentation states that ZFS resilvers only the minimum amount of necessary data. It contrasts a short outage, where catch-up can finish quickly, with full device replacement, where work is proportional to used data.

This operational documentation is useful because the patent family alone would only establish a described design. It still does not prove a universal performance ratio, exact internal algorithm for every release, or that every short outage produces little work.

### H/P — later OpenZFS source retains DTL as replication-history state

OpenZFS 2.1.11 `module/zfs/vdev.c` describes a vdev DTL as the set of transaction groups for which the vdev has `less than perfect replication`. It distinguishes `DTL_MISSING`, `DTL_PARTIAL`, `DTL_SCRUB`, and on-demand `DTL_OUTAGE`.

The same source says that leaf `DTL_MISSING` maps are sufficient to derive the aggregate DTL/outage state and therefore are what the implementation keeps on disk; other DTL forms are regenerated after pool load/configuration changes.

This is **later source-level continuity only**. It must not be projected backward as proof that every 2005–2007 Solaris/ZFS implementation had precisely these four classes or identical persistence rules.

## Retained state

In the bounded DTL-directed repair model, later selective catch-up requires at least:

1. payload / metadata blocks that remain valid on surviving redundant members;
2. block pointers carrying birth-time / transaction-group information in the described ZFS tree;
3. retained DTL interval information identifying when a target did not receive required state;
4. current vdev/topology information identifying which redundancy relation must be restored;
5. traversal/recovery logic that compares block birth state with the retained DTL;
6. enough surviving redundancy to source the missing contribution.

The DTL is not user payload. It is also not a complete write history. It is a compressed witness to a **repair-relevant interval**.

## Retention mechanism

### A failure event can end while its repair obligation remains

A device may return online, but blocks born while it was unavailable can still be missing there. If the system forgot the relevant exposure interval immediately when the device returned, it would lose information useful for bounded repair.

Engineering reconstruction:

```text
device unavailable during txg interval
    ->
retain interval / missing-replication evidence
    ->
device returns
    ->
compare block birth txgs with retained interval
    ->
repair only potentially affected blocks
    ->
retire repair evidence when the required relation is restored
```

Therefore:

> **failure over ≠ repair debt over.**

### DTL is failure-exposure history, not mutation history

A DTL does not need to enumerate every application write, file operation, or historical block value. It preserves the subset of temporal information needed to decide whether a block could have missed required replication on a particular target.

Thus:

> **repair-scope history ≠ complete mutation history.**

### Time/txg selection is different from a dirty-region bitmap

DRL marks spatial regions that need recovery. The described DTL method can instead log transaction-group/birth-time intervals and ask each block whether its birth belongs to those intervals.

Both can reduce full-copy work, but their retained evidence has different geometry:

```text
DRL: spatial region -> dirty/clean recovery status
DTL: transaction-time interval + block birth -> possible repair membership
```

No direct genealogy beyond documented chronology/function is asserted.

## Addressing and access geometry

DTL-directed resilver combines two coordinate systems:

- **tree/location reachability** — block pointers identify and reach current blocks;
- **transaction-time membership** — birth time / txg is compared with DTL intervals.

Pruned resilver can avoid descending a subtree when its birth-time relation shows that no descendant could fall into the relevant dirty interval under the described tree ordering.

So future repair work is shaped not only by where blocks are but by **when their current embodiments entered the tree**.

## Read and verification semantics

A DTL entry does not say that a surviving source block has failed a checksum. It says that the required replication relation was incomplete during specified transaction groups / conditions.

Case 18 remains the checksum/scrub comparison. In modern OpenZFS source, `DTL_SCRUB` also shows that scrub outcome and replication-missing state can interact, but this does not collapse them into one state.

Therefore:

> **repair membership ≠ corruption diagnosis.**

## Repair semantics

### Short-outage catch-up is not full-device replacement

Oracle documentation distinguishes short-outage resilvering from replacement. A returned device may need only the state it missed; a replacement has no trusted prior contents and therefore presents a much larger repair scope, bounded by allocated/used state and implementation details.

### DTL-directed resilver is not dRAID sequential reconstruction

Case 96's dRAID reconstruction uses fixed-width redundancy geometry and device/space-map order to restore redundancy quickly across distributed spare capacity. Case 100 instead focuses on **temporal pruning of repair scope** using DTL/birth relations.

One can optimize *which blocks need repair* and *how repair I/O is laid out* independently.

### DTL-directed resilver is not RAID-Z write-hole avoidance

Case 95 addresses how a new coded block is committed without leaving a fixed partial-stripe update as the standing authoritative state. Case 100 starts after a redundancy gap exists and asks how much state must later be repaired.

## Persistence and derivation boundary

The OpenZFS 2.1.11 comment gives a useful later counterexample to the assumption that every useful maintenance classification must itself be independently durable. Leaf `DTL_MISSING` state is retained on disk, while aggregate/other DTL state can be derived after load or topology change.

Engineering reconstruction:

> **retention infrastructure can preserve a minimal sufficient basis and regenerate higher-level maintenance state.**

This is implementation-specific, not a universal ZFS law.

## Failure boundaries

### Losing DTL / repair-scope evidence

If repair-relevant interval state is unavailable or invalid, selective catch-up may no longer be justified even if payload remains on surviving members. A conservative system may have to enlarge repair/verification scope.

> **payload survival ≠ preservation of the evidence needed for efficient repair.**

### DTL presence mistaken for corruption

A transaction group can be in a missing/partial replication interval without proving that every corresponding source block is corrupt. The DTL bounds where a replica may be incomplete; checksum/integrity evidence answers another question.

### DTL absence mistaken for universal integrity

Conversely, absence from this repair log is not a proof against latent media corruption, controller bugs, or every other failure class. Scrub/checksum verification remains a separate relation.

### Patent embodiment mistaken for release guarantee

The patent family establishes described methods and chronology. Oracle operational docs establish user-visible selective-resilver behavior. Neither source alone licenses projection of every algorithmic detail onto every Solaris/OpenZFS release.

## Prior art and genealogy boundary

### Dirty-region logging is an explicit earlier functional floor

Sun Cluster 2.2 documentation already describes DRL-driven partial recovery of mirrored volumes. The 2007 DTL patent description itself also discusses conventional DRL as an existing recovery scheme.

Therefore this case explicitly rejects:

> `ZFS DTL invented selective mirror resynchronization`.

### Difference retained instead of erased

The prior art matters precisely because the mechanisms are not identical. DRL pays for a spatial dirty map around writes; the ZFS DTL family exploits temporal/transaction-group exposure plus block birth metadata already carried in the tree.

Chronology and functional resemblance do not establish direct descent, and this case makes no universal `first` claim for either technique.

## Cross-case comparison

### Case 18 — ZFS scrub

- Case 18: proactively read/verify current storage and use checksum-qualified redundancy for healing.
- Case 100: retain exposure history so a later resilver can avoid treating unaffected state as repair work.

`verification scope ≠ catch-up scope`.

### Case 48 — Cassandra incremental repair state

Both cases retain maintenance history that can reduce future repair work. Cassandra retains repaired/unrepaired classification over SSTable populations; ZFS DTL retains txg exposure intervals for a redundancy target. This is a functional comparison only, not genealogy.

### Case 95 — RAID-Z write-hole avoidance

Write-hole avoidance governs admissible update construction. DTL governs later repair after incomplete replication. `update consistency ≠ recovery-scope selection`.

### Case 96 — dRAID

DTL/pruned resilver reduces the **set** of blocks that require catch-up. dRAID sequential reconstruction changes **reconstruction geometry/bandwidth** and restores coded redundancy before later checksum scrub. `less work selected ≠ same work scheduled faster`.

## Functional analogy

A bounded analogy is a maintenance exception journal: instead of remembering all successful events, the system retains only intervals where a required relation was not satisfied and later uses that summary to focus repair.

The analogy is functional. It must not replace the historical terms `DTL`, `birth time`, `transaction group`, and `resilver`.

## Philosophical / media-theoretical interpretation

`I` — Case 100 shows that technical retention can preserve not only a payload or an old version but a **debt toward a relation**: the system remembers that one embodiment missed part of the current state and therefore still requires repair.

`I` — It also shows a form of selective forgetting. Complete write history can disappear while a small temporal summary survives because that summary is sufficient for a future maintenance decision.

`I` — The past matters operationally only to the degree that it can still constrain present repair. Once redundancy is restored and the relevant evidence can safely be retired, the system need not become a permanent archive of the outage.

These are project interpretations, not claims that Sun/Oracle/OpenZFS authors formulated a philosophy of memory.

## Counterexamples and limits

This case does not establish:

- that DTL is the first dirty-log technique;
- that DRL and DTL are the same mechanism;
- that the 2005 provisional date equals first deployment;
- that every patent claim shipped unchanged;
- that DTL membership proves checksum failure or user-visible corruption;
- that selective resilver is always fast;
- that every short outage has a small repair set;
- that pruned tree traversal and modern dRAID sequential rebuild are interchangeable;
- that modern OpenZFS DTL class/persistence semantics can be backdated unchanged to 2005;
- that clearing repair-state metadata securely erases payload.

## Related repositories

- [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) — search found no dedicated DTL/resilver case in this slice. Broad dirty-log, mirror-recovery, ZFS source-history, and controller genealogy should live there if developed.
- [`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) — useful for a future question about when `dirty`, `resync`, `resilver`, and transaction-time repair became actors' own problem vocabulary.

## Claim ledger

| Claim | Label | Evidence | Limit |
| --- | --- | --- | --- |
| Sun Cluster 2.2 DRL tracks changed mirror regions and recovers only dirty regions | `H/P` | Sun Cluster 2.2 Cluster Volume Manager Guide | prior-art floor; not DTL identity |
| Sun DTL/resilver family claims 2005-11-04 provisional priority | `H/P` | US patent family | documentary chronology, not first deployment |
| DTL can store failed-write/offline time as transaction-group / birth-time evidence | `H/P` | US7925827 / related family description | bounded to described embodiments |
| pruned resilver can use parent/child birth-time relations to skip unaffected tree branches | `H/P` | US8635190 / US20070106677 | patent/design witness; not universal release guarantee |
| ZFS product docs say short-outage repair can resilver only minimum necessary data | `H/P` | Oracle Solaris ZFS Administration Guide | qualitative product behavior; no universal performance factor |
| later OpenZFS source defines DTL as txgs with less-than-perfect replication | `H/P` | OpenZFS 2.1.11 `vdev.c` | later continuity only |
| later OpenZFS persists a sufficient leaf missing-state basis and derives other DTL state | `H/P/E` | OpenZFS 2.1.11 `vdev.c` | implementation/version-specific |
| DTL is a complete write-history archive | `X` | mechanism/source comparison | rejected |
| DTL membership proves payload corruption | `X` | mechanism/source comparison | rejected |
| ZFS invented selective mirror recovery | `X` | earlier DRL + patent's own prior-art discussion | rejected |
| DRL chronology proves direct genealogy into DTL | `X` | none | unsupported |

## Sources

- Sun Cluster 2.2, `Dirty Region Logging and CVM`: <https://docs.oracle.com/cd/E19957-01/806-2329/ch2admin-39382/index.html>
- Sun/Oracle patent family overview, `Method and system for metadata-based resilvering`: <https://patents.google.com/patent/US8938594B2/en>
- `Method and system for dirty time logging`: <https://patents.google.com/patent/US7925827B2/en>
- `Method and system for dirty time log directed resilvering`: <https://patents.google.com/patent/US7930495B2/en>
- `Method and system for pruned resilvering using a dirty time log`: <https://patents.google.com/patent/US8635190B2/en>
- Oracle Solaris ZFS resilvering status: <https://docs.oracle.com/cd/E26505_01/html/E37384/gbbba.html>
- OpenZFS 2.1.11 source as packaged by Debian, `module/zfs/vdev.c`: <https://sources.debian.org/src/zfs-linux/2.1.11-1%2Bdeb12u1/module/zfs/vdev.c>
