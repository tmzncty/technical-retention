# Intel SSD 320 Power-Loss Protection: Volatile Staging, Flush, and Emergency Retention Work

## Scope

- **Bounded period:** 2007–2013.
- **Primary standards witness:** T13/1699-D Revision 4a, **_AT Attachment 8 - ATA/ATAPI Command Set (ATA8-ACS)_**, working draft dated 21 May 2007, especially §7.14 `FLUSH CACHE` and §7.15 `FLUSH CACHE EXT`.
- **Primary manufacturer witness:** Intel, **_Intel Solid-State Drive 320 Series: Power Loss Data Protection_**, order 325207-001US, March 2011.
- **Named-product interface witnesses:** Intel, **_Intel Solid-State Drive 320 Series Product Specification_**, order 325152-002US, September 2011; and the official Intel **Enterprise Server/Storage Application Product Specification Addendum**, order 325170-002US, April 2011.
- **Independent later boundary:** Mai Zheng, Joseph Tucek, Feng Qin, and Mark Lillibridge, **“Understanding the Robustness of SSDs under Power Fault,”** FAST ’13, pp. 271–284.
- **Research question:** what must remain, and what work must still occur, between a host-side write/flush relation and a recoverable SSD state when the medium is nonvolatile but the controller contains volatile staging and metadata state?

This is **not** a general history of SSDs, NAND, FTL algorithms, SATA, filesystems, `fsync`, NVMe persistence domains, or every form of power-loss protection. Case 04 already grounds mapped-Flash logical/physical relocation; Cases 11–13 ground the device-level floating-gate / erase asymmetry chain. This case begins one layer higher:

> **A nonvolatile medium can sit behind a controller whose currently necessary user or system state is still temporarily volatile.**

The bounded Intel design then adds an event-triggered retention path: detect imminent input-power loss, isolate the drive from the collapsing supply, and spend stored capacitor energy so firmware can move temporary-buffer state to NAND.

---

## Historical vocabulary

The period sources themselves use terms including:

- `volatile write cache`;
- `non-volatile media`;
- `FLUSH CACHE` and `FLUSH CACHE EXT`;
- `write cache` and `write cache reordering`;
- `STANDBY IMMEDIATE`;
- `temporary buffers`;
- `transfer buffer`;
- `system data`;
- `unsafe shutdown`;
- `Power Fail Detect`;
- `Power Good`;
- `power FET`;
- `hold-up circuit`;
- `Power Loss Protection Capacitance`;
- Intel's product phrase `Enhanced power-loss data protection`.

The following are **project engineering terms**, not claims about period vocabulary:

- `controller-mediated durability`;
- `volatile durability window`;
- `retention handoff`;
- `emergency retention work`;
- `energy reserve as retention infrastructure`;
- `payload/currentness-metadata durability split`.

`Commit` is used only where a cited source uses it or where the project explicitly labels it as a later engineering comparison. The ATA working draft itself specifies a narrower observable relation: FLUSH CACHE must not report completion until volatile-cache data have been flushed to nonvolatile media or an error occurs.

---

## Historical record

### H/P — ATA exposes a distinct volatile-cache → nonvolatile-media transition

T13/1699-D Revision 4a, dated 21 May 2007, defines `FLUSH CACHE` in §7.14. The host requests that the device flush its **volatile write cache**; if data are present, they are to be written to **non-volatile media**. The command is not to indicate completion until the data have been flushed to nonvolatile media or an error occurs. `FLUSH CACHE EXT` repeats the same core distinction for the 48-bit addressing feature set.

This is unusually clean period standards-development evidence for two storage conditions inside one device-visible contract:

```text
state present in volatile write cache
        ≠
state flushed to non-volatile media
```

The source is a **working draft**, not the final published ANSI standard. The case therefore cites it as period T13 standards-development text and does not silently upgrade its documentary status.

**Primary anchor:** T13/1699-D Revision 4a (21 May 2007), §7.14.2, draft printed p. 108 / PDF p. 147; §7.15.2, printed p. 109 / PDF p. 148.

### H/P — the Intel SSD 320 explicitly implements FLUSH CACHE and a write-cache control surface

Intel's September 2011 SSD 320 product specification states that the Series supports mandatory ATA8-ACS commands and lists `FLUSH CACHE` in the ATA General Feature command set. Its 48-bit Address command set lists `FLUSH CACHE EXT`. The same specification's SCT Feature Control section exposes feature code `0001h` (`write cache`) and `0002h` (`write cache reordering`).

Intel's April 2011 enterprise addendum independently identifies ATA8-ACS compatibility, `Enhanced power-loss data protection`, and measures the reported random-write workload with the **SSD write-cache enabled**.

The full September product specification currently survives in the research path through a non-Intel mirror; its Intel order number, revision/date, and document content are preserved, but the repository does not describe that mirror as current Intel hosting. The April addendum and March power-loss brief are currently available from Intel's own document host.

**Primary anchors:** Intel 325152-002US (September 2011), printed pp. 16, 21–22; Intel 325170-002US (April 2011), printed pp. 1 and 5.

### H/P — Intel explicitly distinguishes NAND-resident data from data temporarily held in buffers

Intel's March 2011 technical brief states that user and system data may be stored in `temporary buffers` for brief periods as well as in the NAND array. For an orderly shutdown, it says a host generally sends `STANDBY IMMEDIATE`, allowing temporary-buffer data to be saved to nonvolatile NAND before shutdown. It contrasts this with an `unsafe shutdown`, where normal saving of temporary-buffer data may be interrupted.

This is manufacturer-primary evidence against a simplistic inference:

> **NAND is nonvolatile, therefore every state currently needed by an SSD is already nonvolatile.**

The product contains nonvolatile NAND **and** controller-managed temporary state whose safe transition into NAND matters at a shutdown boundary.

**Primary anchor:** Intel 325207-001US (March 2011), first page, sections `Power Loss Data Protection` and `Data Protection Mechanisms`.

### H/P — the Intel SSD 320 uses power-fail detection, firmware, and stored capacitance to finish retention work after input power begins to fail

The same Intel brief describes hardware and firmware working together. A power-fail detector signals the ASIC when the input supply is dropping. Intel says firmware then disconnects input power and uses energy stored in onboard power-loss-protection capacitance to move data in the transfer buffer and other temporary buffers to NAND.

The brief's block diagram separately labels:

- `Power Fail Detect`;
- `Power Good` to the controller ASIC;
- a `Power FET` that isolates the drive;
- a `Hold-up Circuit`;
- `Power Loss Protection Capacitance`.

Intel further says the unsafe-shutdown firmware interrupt deprioritizes nonessential controller activity while moving user and system data. The capacitors are therefore not themselves the long-term data medium. They are a **short-lived energy reserve enabling a final transition into the long-lived medium**.

This produces a retention regime not visible at the NAND-cell level:

```text
external power begins to disappear
        ↓
power-fail detection
        ↓
controller enters emergency path / isolates failing input
        ↓
stored capacitor energy sustains controller + NAND activity
        ↓
temporary user/system state transferred to NAND
```

The source is Intel's own design/product claim. This case treats it as strong evidence for what Intel documented about the SSD 320 design, not as an independent proof that every individual drive always survived every possible power transient.

### H/S — independent power-fault experiments show why interface semantics and implementation reliability must remain separate

Zheng et al., FAST ’13, tested fifteen anonymized commodity SSDs under injected power faults. Their methodology used synchronous writes and confirmed cache-flush commands in the I/O path. The paper reports several classes of anomalous behavior across tested devices, including serialization errors despite cache flushing.

The authors also explain a controller-level failure pattern in which NAND programming and mapping/currentness metadata can be interrupted or ordered incorrectly: the new page's payload may be programmed while the validity/mapping relation needed to make it current after restart does not yet consistently reflect that write.

The device identities were intentionally anonymized. Therefore the paper **cannot** be used to assert that the Intel SSD 320 was one of the failing devices or that Intel's documented power-loss mechanism failed in the experiment.

Its valid use here is narrower:

> **an interface contract or manufacturer feature claim is not the same evidence class as measured compliance under arbitrary fault timing.**

**Scholarly anchor:** Zheng et al., FAST ’13, especially pp. 273, 279, and 281.

---

## Retained state

This case requires several different states/resources to remain distinct.

### 1. User payload in temporary controller buffers

Some host data can exist transiently in controller-managed memory before the documented handoff into NAND.

### 2. Controller / system data

Intel explicitly includes `system data` among the temporary state protected during an unsafe shutdown. The source does not license a complete reverse engineering of every internal data structure, but it does establish that durability is not only about user payload bytes.

### 3. NAND-resident user/system state

NAND is the nonvolatile target into which the emergency path transfers protected temporary state.

### 4. Mapping / currentness relations

Case 04 already establishes mapping as retained state in a mapped-Flash system. FAST ’13 provides a later controller-level warning: programming payload and making the corresponding mapping/validity relation reliably current are separable operations under power failure.

### 5. Stored energy

The charge in the SSD 320's protection capacitors is not the retained user object. It is **retention infrastructure**: a finite physical reserve that buys enough post-failure operating time for another state to become nonvolatile.

---

## Physical / logical substrate

The bounded retention path is layered:

```text
host-visible logical write relation
        ↓
controller / volatile staging state
        ↓
FTL / system metadata and NAND programming machinery
        ↓
nonvolatile NAND state
```

A separate emergency-support path intersects it:

```text
input power
   ↓
power-fail detector → controller emergency path
   ↓
power FET / isolation
   ↓
hold-up capacitance → short post-failure operating interval
```

The distinctive lesson is not that NAND became volatile. Rather, **nonvolatile media are embedded in a device whose path to a recoverable logical state includes volatile control and staging layers**.

---

## Retention mechanism

### Normal explicit flush path

The ATA draft defines a command-level transition from volatile write cache to nonvolatile media and ties command completion to the completion of that flush or an error.

For the SSD 320, Intel documents `FLUSH CACHE` and `FLUSH CACHE EXT` support.

### Clean shutdown path

Intel describes `STANDBY IMMEDIATE` as the usual orderly-shutdown path that allows temporary-buffer data to be saved to NAND.

### Unsafe power-loss path

The SSD 320 adds **failure-triggered retention work**:

1. detect imminent power loss;
2. interrupt/deprioritize ordinary controller work;
3. isolate the failing input path;
4. use stored capacitor energy;
5. transfer user and system data from temporary buffers into NAND.

This is neither periodic refresh nor quiescent passive retention. It is an event-triggered handoff whose work is performed exactly when the external condition that normally powers the device is disappearing.

---

## Addressing and access geometry

The host addresses logical blocks through the ATA interface; the controller resolves those requests through the device's internal mapping and NAND organization.

This case does not attempt to reconstruct the SSD 320's complete FTL algorithm. The retention-specific point is that a host-visible block can be:

- represented in a volatile staging/cache state;
- later represented in nonvolatile NAND;
- dependent on system/mapping state that makes the current NAND embodiment recoverable after restart.

Therefore `where the data are` cannot be answered with one address-space noun. The host designation, controller staging location, current physical NAND embodiment, and retained metadata relation are separate layers.

---

## Read semantics

Ordinary reads are outside the main mechanism question here. The important recovery boundary occurs **after restart following power interruption**: a NAND page physically programmed with bits is useful only insofar as the controller can recover a coherent current logical state from payload plus necessary system/mapping information.

This is why the FAST ’13 mapping-validity discussion is important as a counterexample: raw physical programming and logical post-restart currentness are not automatically the same event.

---

## Write, flush, and shutdown semantics

### Ordinary writes with a write cache present

The Intel documents establish a write-cache facility, but this case does **not** invent a stronger ordinary-write acknowledgement rule than the cited interface documentation establishes.

### FLUSH CACHE

ATA8-ACS draft §7.14 gives an explicit durability-oriented completion boundary: volatile-cache data are to reach nonvolatile media before successful command completion.

### STANDBY IMMEDIATE

Intel describes this as the normal shutdown request that permits temporary-buffer state to be saved to NAND.

### Unsafe power loss

No host shutdown command can be assumed to arrive. The device instead detects the supply failure and performs its own emergency transfer using stored energy.

The three paths must not be collapsed:

```text
explicit host flush
    ≠
orderly shutdown handoff
    ≠
unexpected-power-loss emergency handoff
```

They may all move state toward nonvolatile media, but their trigger, control authority, timing assumptions, and failure surfaces differ.

---

## Time

This case adds several timescales to the comparison:

- ordinary command/cache residence time;
- explicit FLUSH CACHE completion time;
- orderly shutdown time;
- power-fail detection latency;
- the short hold-up interval supplied by the capacitors;
- NAND program / metadata-update sequencing under that interval;
- long-term NAND retention after the transition succeeds.

The Intel brief does not provide a license to invent a universal capacitor hold-up duration. The technically important fact is the **bounded interval**, not an unsupported exact number.

---

## Maintenance and labor

The apparent simplicity of “nonvolatile SSD storage” depends on invisible engineered work:

- controller firmware deciding what must be saved first;
- power-fail detection hardware;
- supply isolation;
- capacitor sizing, qualification, and lifetime margin;
- NAND programming;
- mapping/system metadata maintenance;
- command-set semantics that let a host explicitly request a volatile→nonvolatile transition;
- software issuing the relevant commands at the appropriate persistence boundary.

The Intel design also shows that maintenance can be **deferred until a threat event**. The capacitors are idle from the user's perspective until the external supply fails, at which point their stored energy becomes constitutive of the final retention transition.

---

## Failure / forgetting modes

Distinct failure modes include:

- loss of input power before buffered state reaches NAND;
- insufficient or degraded hold-up capacitance;
- failure of the power-fail detection / isolation path;
- firmware failing to complete the prioritized emergency transfer;
- interruption during NAND programming;
- mapping/validity/system metadata not becoming consistent with newly programmed payload;
- an implementation acknowledging or completing a flush incorrectly;
- the host failing to issue the persistence/shutdown command that its own software semantics require;
- later NAND media failure or ordinary retention loss, which is a different regime from the immediate power-loss window.

The source set does not justify assigning a probability to each failure for the SSD 320, nor does FAST ’13 identify the Intel 320 among its anonymized devices.

---

## Engineering reconstruction

### E — nonvolatile substrate ≠ no volatile durability window

A device may contain nonvolatile NAND while current user or system state is temporarily resident in volatile controller buffers. `Nonvolatile SSD` is therefore a medium/device category, not a proof that every in-flight state is already power-fail durable.

### E — durability can require a final burst of work after external power loss begins

The Intel 320's stored capacitance is valuable because it enables **continued operation during the failure transition**. Persistence is produced by spending a short-lived energy reserve to move state into a longer-lived substrate.

### E — payload residency ≠ recoverable logical currentness

A newly programmed physical page is not necessarily enough after restart. The currentness/mapping relation that makes it the authoritative embodiment may also need to be preserved consistently.

### E — explicit durability contract ≠ empirical implementation compliance

The ATA draft defines what a successful flush is supposed to mean. FAST ’13 demonstrates why a separate evidence layer is needed to establish whether implementations behave correctly under fault injection.

### E — clean-shutdown work ≠ power-fault work

Both can protect the same eventual NAND state, but one begins with a host command under ordinary power and the other is device-triggered while power is collapsing.

---

## Functional analogies

### A — comparison with mapped Flash, Case 04

Case 04 asks how logical identity survives out-of-place Flash relocation and reclamation. Case 15 assumes such controller mediation and asks a different question: **when is the controller's current state safely handed into a nonvolatile recovery domain?**

Similarity does not make power-loss protection an FTL algorithm.

### A — comparison with HDD defect reassignment, Case 14

Both cases show metadata/control state becoming constitutive of the service presented above the medium. But Case 14 is failure-triggered replacement of a physical sector behind a stable LBA; Case 15 is a power-failure boundary between volatile staging/control state and a recoverable nonvolatile SSD state.

### A — comparison with RADOS, Case 05

RADOS already forced the project to distinguish acknowledgement, replication, and later durable commit in a distributed protocol. The useful analogy here is only that **a system-visible success relation must be specified separately from physical durability**. ATA FLUSH gives one device-level contract; Ceph/RADOS has different protocol roles, copies, and authorities.

---

## Philosophical / media-theoretical interpretation

### I — nonvolatility does not eliminate temporality from persistence

A tempting picture treats nonvolatile memory as state that simply remains once written. The SSD 320 power-loss path complicates that picture without denying NAND nonvolatility.

At the device boundary, there is a short crisis interval in which the future availability of data depends on:

- recognizing that ordinary power is ending;
- retaining enough energy to continue acting;
- prioritizing which controller states matter;
- completing a transition into NAND before the reserve is exhausted.

A cautious conceptual formulation is:

> **technical retention can depend on preserving the capacity to complete a final act, not only on the passive persistence of the substrate that will hold the result.**

This is an interpretation disciplined by the Intel mechanism. It is not a claim that every nonvolatile technology has the same temporal structure.

---

## Rejected / unsupported claims

### X — “because NAND is nonvolatile, SSD power loss cannot lose in-flight state”

Rejected. Intel explicitly documents temporary buffers and a protection mechanism intended to move their state to NAND during power loss.

### X — “the SSD 320 has no volatile state because it has power-loss protection”

Rejected. The protection mechanism exists precisely because temporary user/system state and controller work can precede NAND residency.

### X — “support for FLUSH CACHE proves every implementation obeys the contract under every power fault”

Rejected. Standards/interface semantics and empirical fault behavior are different evidence layers.

### X — “FAST ’13 proves the Intel SSD 320 loses data under power faults”

Rejected. The tested devices are anonymized; the paper cannot be mapped to the Intel product without additional evidence.

### X — “capacitors make the SSD a battery-backed RAM”

Rejected. In the bounded Intel description, the capacitors provide short hold-up energy so firmware can move state to NAND. They are retention infrastructure, not the long-term payload substrate.

### X — “this case establishes filesystem `fsync` or NVMe persistence semantics”

Rejected. The case stops at the ATA/SSD device boundary. Filesystem ordering, block-layer barriers, NVMe volatile-write-cache rules, and later persistence-domain terminology require separate sources and cases.

---

## Claim ledger

| Claim | Type | Evidence status |
| --- | --- | --- |
| ATA8-ACS draft distinguishes volatile write-cache state from data flushed to nonvolatile media | H/P | strong: T13/1699-D Rev. 4a §7.14–7.15 |
| successful FLUSH CACHE completion is specified only after cache data reach nonvolatile media or an error occurs | H/P | strong for the cited working draft |
| Intel SSD 320 supports FLUSH CACHE / FLUSH CACHE EXT and exposes write-cache control | H/P | strong: Intel 325152-002US; surviving mirror inspected |
| Intel SSD 320 product literature advertises enhanced power-loss data protection and write-cache-enabled workloads | H/P | strong: Intel 325170-002US |
| Intel documents temporary user/system data buffers and an unsafe-shutdown protection path | H/P | strong: Intel 325207-001US |
| Intel documents power-fail detect + controller firmware + isolation + hold-up capacitance + NAND transfer | H/P | strong manufacturer-primary design description |
| nonvolatile substrate does not imply every currently necessary device state is already nonvolatile | E | strongly supported by bounded Intel design |
| stored capacitor energy can be retention infrastructure without being the retained payload | E | strongly supported by bounded Intel design |
| programmed payload and mapping/currentness metadata can fail as separate relations under power fault | H/S + E | high-quality FAST ’13 boundary; not Intel-product-specific |
| interface flush contract proves empirical correctness of every SSD | X | explicitly rejected |
| FAST ’13 identifies Intel SSD 320 as a failing device | X | explicitly rejected |

---

## Related repositories

A pre-write search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for SSD power loss, flush, controller cache, FTL durability, capacitor / power-loss-protection vocabulary did **not** locate a dedicated existing case covering this bounded mechanism. This file therefore keeps only the retention-specific argument rather than constructing a generic SSD technical history.

Case 04 remains the main internal technical bridge for 1990s mapped Flash. Cases 11–13 remain the device-level floating-gate / erase-history bridge. The present case should be linked rather than used to rewrite those histories.

---

## Sources and inspection notes

### Primary / contemporary sources

1. T13, **_AT Attachment 8 - ATA/ATAPI Command Set (ATA8-ACS)_**, T13/1699-D Revision 4a, 21 May 2007. This is explicitly a **working draft**, not a completed standard. Directly inspected §7.14 `FLUSH CACHE`, printed p. 108 / PDF p. 147, and adjacent §7.15.  
   Surviving copy used for inspection: <https://tc.gts3.org/cs3210/2016/spring/r/hardware/ATA8-ACS.pdf>

2. Intel Corporation, **_Intel Solid-State Drive 320 Series: Power Loss Data Protection_**, order 325207-001US, March 2011. Directly inspected both pages, including the power-path block diagram.  
   <https://www.intel.com/content/dam/www/public/us/en/documents/technology-briefs/ssd-320-series-power-loss-data-protection-brief.pdf>

3. Intel Corporation, **_Intel Solid-State Drive 320 Series Enterprise Server/Storage Application Product Specification Addendum_**, order 325170-002US, April 2011. Directly inspected the first page and performance section; the document identifies ATA8-ACS, enhanced power-loss protection, and write-cache-enabled random-write measurement.  
   <https://www.intel.com/content/dam/www/public/us/en/documents/product-specifications/ssd-320-enterprise-server-storage-application-specification-addendum.pdf>

4. Intel Corporation, **_Intel Solid-State Drive 320 Series Product Specification_**, order 325152-002US, September 2011. Directly inspected the surviving mirrored PDF at printed pp. 16, 21–22 for command support and cache-control surfaces. The current research path is a third-party mirror; this source is not represented as presently Intel-hosted.  
   <https://www.ssdwiki.com/media/ssd-320-specification.pdf>

### High-quality independent research

5. Mai Zheng, Joseph Tucek, Feng Qin, and Mark Lillibridge, **“Understanding the Robustness of SSDs under Power Fault,”** _Proceedings of the 11th USENIX Conference on File and Storage Technologies (FAST ’13)_, 2013, pp. 271–284. Directly inspected the USENIX paper, especially printed pp. 273, 279, and 281.  
   <https://www.usenix.org/conference/fast13/technical-sessions/presentation/zheng>

### Evidence boundary

- Intel's 2011 power-loss brief is a **manufacturer-primary disclosure / claim**, not independent fault-injection validation.
- T13/1699-D Rev. 4a is **standards-development primary evidence**, explicitly a working draft rather than the final standard.
- The September Intel SSD 320 product specification was inspected through a surviving third-party mirror; claims drawn from it are limited to the identifiable Intel document and cited pages.
- FAST ’13 supplies an independent **counterexample class** for SSD power-fault robustness, but its anonymized devices cannot be identified as the Intel SSD 320.
- No claim is made that all SSD controllers, all SATA devices, NVMe devices, or filesystems implement this exact retention path.
