# Evidence 124 — FTL Mapping-Recovery Grounding (1995–2014)

## Research question

Can Flash user payload remain nonvolatile across power loss while the volatile logical-to-physical lookup state used during normal operation disappears, forcing a controller to reconstruct the mapping/currentness relation from other retained metadata before ordinary logical service resumes?

This record grounds only that bounded relation. It does not attempt a complete SSD/FTL history.

---

## Source hierarchy and identity

### P0 — inherited primary floor from Case 04: Amir Ban / M-Systems, US 5,404,485

**Title:** `Flash file system`  
**Inventor:** Amir Ban  
**Original assignee:** M-Systems Flash Disk Pioneers Ltd.  
**Filed:** **8 March 1993**  
**Issued:** **4 April 1995**  
**URL:** <https://patents.google.com/patent/US5404485A/en>

Case 04 already inspected the patent-image scan and grounds the following facts:

- the virtual/logical address can remain stable while current data moves to an unwritten physical Flash location;
- the major portion of the virtual map is stored in nonvolatile Flash;
- a smaller secondary map can reside in RAM;
- volatile secondary mapping state can be rebuilt at startup from retained block-usage information.

**What P0 proves for Case 124:** relation reconstruction from Flash-resident metadata predates the later power-failure-specific sources used below.  
**What it does not prove:** modern SSD FTL architecture, the later papers' algorithms, or first invention of crash recovery.

Case 124 therefore reuses P0 rather than duplicating the full 1993–1995 mechanism history.

### P1 — Intel AP-619, August 1995

**Vendor:** Intel Corporation  
**Document:** *FTL Logger: Exchanging Data with FTL Systems*  
**Authors:** Kirk Blum and Peter Lam  
**Document:** AP-619, order no. 292174-001  
**Date:** **August 1995**  
**Preserved scan:** <https://intel-vintage-developer.eu5.org/DESIGN/FLCARD/APPLNOTS/292174_1.PDF>

Case 04 already grounds the source identity and the `Flash Translation Layer (FTL)` terminology floor.

The retention-specific point reused here is that AP-619 describes Block Allocation Maps (BAM), a Virtual Block Map (VBM), erase-unit headers, and free/deleted/bad allocation states, and says VBM state can live on media or be reconstructed in RAM from retained allocation information when media are reinserted.

**What P1 proves:** by August 1995, a vendor FTL document treats RAM lookup state as reconstructible from nonvolatile mapping/allocation information.  
**What it does not prove:** the first FTL, first power-failure recovery algorithm, or the architecture of later SSD controllers.

---

### P2 — Park et al., IEICE Electronics Express, 2009

**Authors:** Jung-Wook Park, Seung-Ho Park, Gi-Ho Park, Shin-Dug Kim  
**Title:** *An integrated mapping table for hybrid FTL with fault-tolerant address cache*  
**Journal:** *IEICE Electronics Express* 6(7), 368–374  
**Received:** **26 December 2008**  
**Accepted:** **3 March 2009**  
**Published:** **10 April 2009**  
**DOI:** 10.1587/elex.6.368  
**Article:** <https://www.jstage.jst.go.jp/article/elex/6/7/6_7_368/_article/-char/en>  
**PDF:** <https://www.jstage.jst.go.jp/article/elex/6/7/6_7_368/_pdf>

#### Abstract and introduction — cached mapping creates a power-failure consistency risk

The paper states that entire FTL mapping tables cannot always fit in fast SRAM. It describes designs that keep physical-page addresses in Flash spare areas and use a page-address cache to reduce search time.

It then makes the failure problem explicit: losing only a few cached addresses during power failure can create substantial inconsistency affecting data information. The introduction likewise says a write-back cache can lose valid data/table information on system failure.

The safe bounded claim is:

> **normal-operation mapping acceleration in volatile memory can create a separate recovery obligation even though the underlying Flash is nonvolatile.**

The paper's generalized statements about "earlier/later FTLs" are not used as proof of every commercial product.

#### §3 — integrated map block as nonvolatile recovery substrate

The proposed scheme stores metadata tables in a `map block` inside Flash storage. Its map-block entries contain page/block mapping and status information.

The paper says that at startup the map-block area is partially scanned to fetch/generate the block table and available-block bitmap in internal memory, while page-table entries are fetched into the cache on demand.

This directly supports:

> **volatile runtime table ≠ sole authoritative copy of the relation**.

For the proposed system, Flash-resident metadata survives so volatile working tables can be regenerated.

#### Source-status boundary

This is a peer-reviewed academic proposal supported by simulation. It is primary evidence for the authors' proposed mechanism and contemporary scholarly evidence for the stated recovery problem.

It is **not** a named commercial SSD implementation and does not establish universal FTL behavior.

---

### P3 — ITRI, US 9,164,887 B2 / US20130145076A1

**Title:** *Power-failure recovery device and method for flash memory*  
**Inventors:** Tzi-cker Chiueh, Ting-Fang Chien, Shih-Chiang Tsao, Chien-Yung Lee  
**Assignee:** Industrial Technology Research Institute (ITRI)  
**Filed / priority:** **5 December 2011**  
**US application publication:** **6 June 2013**  
**Grant publication:** **20 October 2015**  
**Stable text:** <https://patents.google.com/patent/US9164887B2/en>

#### Disclosure — Flash is nonvolatile, but BMT is temporarily cached

The patent describes Flash as nonvolatile and explains an FTL that manages logical-to-physical translation through a `block map table (BMT)`.

The BMT records logical-block → physical-block mappings and is **temporarily stored in cache**.

Physical pages contain data areas and spare areas; the spare areas can contain metadata such as the logical address associated with the general data.

#### Recovery hierarchy — super map, dedicated map, BMT, update log

The disclosed power-failure recovery path:

1. reads a `super map` from physical blocks;
2. reads a `dedicated map`;
3. loads a Flash-resident BMT into cache;
4. determines whether an abnormal shutdown occurred;
5. if so, reads an `update log`;
6. processes update sections/labels and updates the cached BMT.

The description explicitly says the design can recover a BMT lost due to power failure using information registered in the update log.

This is direct primary support for:

```text
volatile cached BMT
    != nonvolatile recovery records
    != user payload
```

and for:

> **mapping recovery can be replay of relation metadata rather than reconstruction of user payload.**

#### Source-status boundary

A patent is evidence of a disclosed technical design and chronology. It is not evidence that the design shipped in a named ITRI product, nor that it was the first such design.

---

### P4 — Zhang et al., DAC 2014

**Authors:** Chi Zhang, Yi Wang, Tianzheng Wang, Renhai Chen, Duo Liu, Zili Shao  
**Title:** *Deterministic crash recovery for NAND flash based storage systems*  
**Venue:** 51st Design Automation Conference (DAC 2014)  
**Conference:** **2–5 June 2014**, San Francisco  
**DOI:** 10.1145/2593069.2593124  
**Publisher page:** <https://doi.org/10.1145/2593069.2593124>

The paper frames the FTL crash-recovery problem as how to maintain and recover **FTL metadata consistency** after a system crash.

Its DCR design exploits deterministic FTL operation to reproduce events between the last checkpoint and crash point, checking only a limited number of blocks instead of scanning the whole Flash chip. The authors report an implementation for a block-level FTL on an ARM11-based evaluation board.

**What P4 proves:** another independent technical path treats post-crash recovery as consistent reconstruction of FTL metadata relations, and checkpoint/replay structure can reduce recovery work.  
**What it does not prove:** DCR ancestry from the 2009/2011 sources, commercial adoption, or a universal recovery algorithm.

---

## Evidence chain

```text
8 Mar 1993
Ban / M-Systems filing
virtual map + Flash-resident relation state
+ startup rebuild of volatile secondary map
        |
Aug 1995
Intel AP-619
FTL BAM/VBM vocabulary
+ RAM VBM rebuild from retained allocation state
        |
10 Apr 2009
Park et al.
power-failure risk of volatile page-address cache
+ Flash-resident hybrid map block
        |
5 Dec 2011
ITRI filing
cache-resident BMT
+ Flash super/dedicated maps + update log
+ abnormal-shutdown replay
        |
Jun 2014
Zhang et al. DCR
checkpoint / deterministic crash reconstruction
of FTL metadata consistency
```

This is a **documented functional sequence**, not a proven genealogy. Each source independently anchors a bounded mechanism or vocabulary point.

---

## Grounded claims

### H/P — reconstructible mapping state predates the later SSD-era recovery literature

Ban and Intel already make nonvolatile mapping/allocation evidence capable of rebuilding volatile lookup state in the 1993–1995 period.

> **later power-failure paper ≠ invention of rebuildable mapping**.

### H/P/S — power failure can destroy fast mapping state without erasing all Flash payload

Park et al. explicitly identify volatile/cached mapping loss at power failure as a consistency problem and design a Flash-resident map block to regenerate table state.

> **nonvolatile medium ≠ nonvolatile runtime index**.

### H/P — a disclosed controller can keep BMT in cache while retaining recovery logs/maps in Flash

The ITRI filing explicitly separates BMT cache residence from Flash-resident recovery structures and says the update log can recover the BMT after power failure.

> **working translation representation ≠ recovery substrate**.

### H/P/S — crash recovery can target metadata consistency

DCR explicitly defines the problem in terms of FTL metadata consistency and reconstructs post-checkpoint events.

> **recovery of the logical service relation ≠ rewriting every surviving payload page**.

---

## Engineering reconstruction

### E1 — physical payload survival is weaker than logical legibility

Assumptions:

1. the store uses out-of-place mapping;
2. ordinary logical reads need the current mapping relation;
3. power failure removes volatile runtime mapping;
4. the Flash payload itself remains readable.

Then physical NAND survival alone does not tell the restarted controller which physical page should answer a given logical address.

The missing object is a **resolution/currentness relation**, not necessarily the payload.

### E2 — a volatile representation can be disposable

If enough nonvolatile map/log metadata survives, the controller can regenerate a volatile working table.

Therefore:

> **volatile state ≠ unrecoverable state**.

The relevant question is whether the relation has a sufficient retained reconstruction basis.

### E3 — mapping reconstruction and content reconstruction are different

FTL startup scan/log replay regenerates translation/currentness metadata from surviving evidence.

RAID/erasure-code reconstruction regenerates missing content from redundant content.

Both are recovery work, but:

> **relation reconstruction ≠ payload reconstruction**.

### E4 — recovery latency is not media-retention time

The NAND payload can have survived the entire outage while ordinary logical service remains unavailable during map scanning/replay.

Therefore:

> **media state already retained ≠ service already restored**.

### E5 — currentness evidence matters when stale embodiments survive

Out-of-place writes can leave prior physical embodiments until later reclamation. Mapping/allocation metadata determine which one counts as current.

Therefore:

> **many readable physical pages ≠ unambiguous current logical state**.

This is functionally comparable to currentness evidence in distributed systems, but the FTL mechanism is local translation/reclamation state, not replica consensus.

---

## Counterexamples / limits

### C1 — losing a cache entry need not lose the mapping relation permanently

Both the 2009 proposal and 2011 disclosure retain enough metadata in Flash to rebuild runtime table state.

So:

> `RAM table lost` does not imply `mapping relation irrecoverable`.

### C2 — recovering the map cannot recover data that never became durable

If a user page was not successfully programmed before power loss, or is unreadable/corrupt, restoring the L2P/BMT relation cannot recreate those bits.

So:

> `mapping recovered` does not imply `payload recovered`.

### C3 — physically surviving stale pages need not be current

Out-of-place Flash can preserve obsolete physical pages until reclamation.

So:

> `page readable` does not imply `page service-admissible for its former logical address`.

### C4 — one recovery technique does not define FTL history

Map-block scans, spare-area scans, hierarchical map/log replay, and deterministic checkpoint recovery trade runtime overhead, retained metadata, and recovery work differently.

Similarity at the recovery-function level is not proof of historical descent.

---

## Cross-case boundary

### Case 04

Case 04 remains the canonical positive history of mapped Flash identity and reclamation.

Case 124 should not duplicate its broad history. It adds the explicit failure relation:

> **surviving payload + lost volatile map + retained recovery evidence → relation reconstruction before ordinary service**.

### Case 15

Case 15 deals with volatile staged payload/controller state crossing a durability boundary under power loss.

Case 124 instead deals with the resolution relation needed to reach already-surviving nonvolatile payload.

### Synthesis 15

Synthesis 15 separates designation, payload value, resolution relation, and embodiment. Case 124 supplies the missing failure witness in which the resolution relation must be rebuilt even though embodiment/value may physically persist.

### Synthesis 16

Synthesis 16 shows that distributed currentness can depend on retained protocol relations. Case 124 is a useful functional analogy — relation loss can change logical survival without immediate byte destruction — but FTL mapping should not be redescribed as distributed replica currentness.

---

## Claim ledger

| ID | Claim | Evidence | Status |
| --- | --- | --- | --- |
| C124-01 | 1993-filed mapped Flash already supported rebuilding volatile secondary mapping state from Flash-resident allocation information | P0 / Case 04 | `grounded` |
| C124-02 | Intel documented FTL BAM/VBM state and rebuildable RAM lookup by August 1995 | P1 / Case 04 | `grounded` |
| C124-03 | Park et al. explicitly tied volatile mapping-cache loss to power-failure inconsistency and proposed Flash-resident map-block recovery | P2 | `grounded` |
| C124-04 | ITRI disclosed BMT-in-cache plus Flash-resident super/dedicated map and update-log recovery after abnormal shutdown | P3 | `grounded` |
| C124-05 | DCR 2014 framed crash recovery as recovery of FTL metadata consistency | P4 | `grounded` |
| C124-06 | payload persistence does not by itself imply logical legibility in a mapped store | P0–P4 + reconstruction | `grounded` |
| C124-07 | volatile working mapping can be disposable if a sufficient nonvolatile recovery substrate survives | P0–P4 + reconstruction | `grounded` |
| C124-08 | mapping recovery and payload reconstruction are distinct operations | mechanism comparison | `grounded` |
| C124-09 | any retained mapping checkpoint is sufficient for crash-consistent recovery | none | `rejected` |
| C124-10 | all SSDs use the same mapping persistence/replay structure | none | `rejected` |
| C124-11 | the inspected sources prove one Ban→PCMCIA→Park→ITRI→DCR lineage | none | `rejected` |

---

## Related-repository check

Current GitHub searches of `tmzncty/computing-archaeology` for `FTL`, `flash translation layer power loss recovery`, and mapping-table recovery returned no dedicated case.

Repository boundary:

- **technical-retention:** retain the relation-lifetime distinction among payload, volatile working map, nonvolatile recovery metadata, currentness, and reconstruction work;
- **computing-archaeology:** future broad FTL controller history, map-cache evolution, SSD firmware genealogy, and standards/vendor lineage.

---

## Evidence debt

1. Inspect an exact PCMCIA FTL specification facsimile for reinsertion/startup mapping-reconstruction wording rather than relying on Intel AP-619 as the contemporary vendor bridge.
2. Add a named shipping SSD/controller manual or open firmware implementation that exposes its mapping checkpoint/log recovery path.
3. Add independent power-cut/fault-injection evidence measuring mapping corruption/recovery separately from user-payload loss.
4. Trace data-page vs mapping-log ordering rules for one named implementation.
5. Keep forensic recovery after complete mapping-metadata loss separate from ordinary controller recovery.
