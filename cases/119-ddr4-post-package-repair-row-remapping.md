# Case 119 — DDR4 Post-Package Repair: Row-Address Continuity Across Spare-Row Substitution

## Status

**`grounded`** — bounded to DDR4-era Post-Package Repair (`PPR`) semantics evidenced by Micron DDR4 product documentation, Samsung's 2014 DDR4 operation document, an SK hynix 2015-priority PPR patent embodiment, Intel platform documentation, Lenovo ThinkSystem service behavior, and an Intel hard-PPR power-failure disclosure. A 1979-filed semiconductor-memory redundancy patent supplies an earlier spare-row/address-substitution prior-art floor. The case does **not** claim a complete JEDEC PPR genealogy, a universal internal implementation for all DDR4 devices, or that patent embodiments automatically describe every shipping product.

Grounding/deepening records: [`../evidence/119-ddr4-1979-2023-post-package-repair-grounding.md`](../evidence/119-ddr4-1979-2023-post-package-repair-grounding.md) + [`../evidence/119-micron-ddr4-ppr-payload-retention-resource-exhaustion-deepening.md`](../evidence/119-micron-ddr4-ppr-payload-retention-resource-exhaustion-deepening.md) + [`../evidence/119-samsung-2014-ddr4-ppr-cross-vendor-resource-transition-deepening.md`](../evidence/119-samsung-2014-ddr4-ppr-cross-vendor-resource-transition-deepening.md) + [`../evidence/119-skhynix-2015-ppr-resource-reconstruction-deepening.md`](../evidence/119-skhynix-2015-ppr-resource-reconstruction-deepening.md).

## Scope

The earlier DRAM cases in this repository ask how a volatile charge state is periodically restored, how refresh responsibility moves between controller and device, how refresh scope changes, and how disturbance-triggered maintenance can be directed. Case 119 asks a different question:

> What happens to the identity of a DRAM row when a platform decides that the originally addressed physical row is defective and causes the device to substitute a spare row for future accesses?

The retention relation here is not ordinary DRAM refresh. It is **retention of address-resolution/repair state across a change of physical row embodiment**.

This case is deliberately narrow. It is **not**:

- a general history of semiconductor-memory redundancy;
- a claim that DDR4 invented spare-row repair;
- a claim that every DDR4 device implements PPR with identical fuse technology, spare counts, timings, or diagnosis policy;
- a claim that PPR preserves the current payload of the defective row while remapping it;
- a claim that PPR is ECC, scrubbing, RowHammer mitigation, or ordinary refresh;
- a claim that a successful `hPPR` makes DRAM payload nonvolatile;
- a proof that a 1979 spare-row design directly evolved into DDR4 PPR.

Broader semiconductor-memory redundancy history belongs primarily in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) if developed there. Current searches found no dedicated PPR case to reuse.

---

## Payload-retention and repair-resource deepening

Micron's DDR4 PPR sequence documentation closes two evidence debts left by the original grounding; see [`../evidence/119-micron-ddr4-ppr-payload-retention-resource-exhaustion-deepening.md`](../evidence/119-micron-ddr4-ppr-payload-retention-resource-exhaustion-deepening.md).

First, **persistent row repair does not by itself define payload preservation across the repair transition**. In Micron's documented `sPPR` path, the bank is expected to retain array data except for the seed row and associated row addresses; if those contents must survive the repair, they are explicitly backed up before sPPR and restored afterwards. Micron's `hPPR` documentation likewise exposes two command-sequence envelopes: one supports data retention under its stated refresh conditions, while the other does not support data retention for the target DRAM.

Second, **repair support does not imply that a repair resource is still available**. Micron states that once the hPPR resource for a bank is used up, the bank should be treated as lacking sPPR resources as well; a repair sequence issued when no repair resource is available is ignored.

The engineering reconstruction can therefore be sharpened to:

```text
logical row-address continuity
!=
repair-mapping persistence
!=
payload preservation across repair

PPR capability
!=
repair resource available now

repair sequence issued
!=
new repair mapping installed
```

For the bounded sPPR path, data-preserving maintenance is a compound workflow:

```text
back up affected seed / associated rows
    -> perform repair/remap transition
    -> restore payload
```

That is not evidence for a universal DDR4 migration algorithm. It is evidence that **mapping continuity and payload continuity are distinct obligations even inside one vendor's documented PPR procedure**.

Repair-resource exhaustion also makes future maintainability stateful: consuming a finite repair resource changes which later defect-repair transitions remain admissible. This is a repository-level engineering reconstruction, not Micron's historical terminology and not a claim that every DDR4 vendor exposes the same spare topology or count.

Finally, none of these transitions establishes sanitization. Backing up/restoring data, redirecting a row address, retiring a defective row, or consuming a spare does not prove that data remaining in the old physical embodiment has been securely erased or made forensically inaccessible.

---

## Cross-vendor resource and transition deepening

Samsung and SK hynix add two different kinds of manufacturer-primary evidence around the same resource question.

Samsung's September/October 2014 DDR4 operation document exposes a one-repair-element-per-bank-group operation contract, distinguishes volatile `sPPR` from permanent `hPPR`, requires outstanding soft repair to be cleared before the documented hard-repair path, and says exhausted resource causes a repair programming sequence to be ignored. See [`../evidence/119-samsung-2014-ddr4-ppr-cross-vendor-resource-transition-deepening.md`](../evidence/119-samsung-2014-ddr4-ppr-cross-vendor-resource-transition-deepening.md).

The SK hynix 2015-priority patent embodiment exposes a different layer: persistent failed-address information in an Array Rupture Electrical-fuse (`ARE`) array is scanned after power-up to derive repair-resource information; fuse lines can be shared across a bank grouping while resource status is checked per bank/region; and a masking controller prevents another irreversible rupture when no unused repair fuse remains. See [`../evidence/119-skhynix-2015-ppr-resource-reconstruction-deepening.md`](../evidence/119-skhynix-2015-ppr-resource-reconstruction-deepening.md).

Together with the bounded Micron product evidence, these records justify several negative controls:

```text
shared PPR vocabulary
    != identical exposed repair capacity

shared PPR vocabulary
    != identical physical/shared resource topology

same sPPR/hPPR lifetime labels
    != identical transition preconditions

persistent repair state
    != runtime resource-availability state

remaining repair capacity
    can be reconstructed from retained allocation history
    in at least one manufacturer patent embodiment
```

The evidence layers remain deliberately unequal: Samsung is a vendor operation document, Micron is bounded product documentation, and the SK hynix source is a patent embodiment. The SK hynix patent is therefore **not** promoted into a named shipping-product contract merely to force a symmetrical comparison.

---

## Historical record

### A much earlier spare-row/address-substitution floor: 1979 filing

F. Procyk and R. Cenker's **“Memory with redundant rows and columns”** family has a 9 February 1979 priority/filing date. The public patent record describes a semiconductor memory with spare rows and columns, individual standard and spare decoders, and a repair procedure in which the decoder for a defective standard row or column is disabled while a spare decoder is modified so that the spare responds to the address formerly associated with the defective element.

The disclosed implementation uses fusible links opened by laser during manufacturing/test. The important retention relation is already visible:

```text
external address relation
    remains usable
while
physical row/column embodiment changes
```

This is an earlier **mechanism/prior-art floor for redundant-row address takeover**. It is not Post-Package Repair and it does not establish a direct genealogy into DDR4 PPR.

### Micron DDR4 product PPR

Micron's 16Gb DDR4 SDRAM documentation (Rev. G, August 2020, publicly inspectable through a datasheet mirror) exposes both **soft Post-Package Repair (`sPPR`)** and **hard Post-Package Repair (`hPPR`)** as product modes. It states that hard repair is irreversible, describes one row per bank as repairable for the bounded product, and exposes mode-register/MPR capability bits for PPR support.

A later Micron 16Gb DDR4 product-document extraction states the distinction directly:

- `sPPR` is **non-persistent** and can be reversed/reassigned or later made permanent;
- `hPPR` is **persistent/permanent** and cannot be reversed;
- the controller supplies the failing row address in the PPR sequence;
- repeated repair activity in one bank does not silently overwrite an already established hard-PPR address.

The Micron text is manufacturer-authored but, in this research slice, accessed through public datasheet mirrors rather than a stable current Micron-hosted archive. That provenance is preserved explicitly in the evidence record.

### Samsung 2014 DDR4 operation contract

Samsung's **DDR4 SDRAM Specification — Device Operation & Timing Diagram**, Rev. 1.1, October 2014, exposes hard PPR and soft PPR as separate operation modes. The bounded public extraction states one repair element per bank group in the exposed operation contract, describes hard repair as permanent electrical-fuse repair, makes soft repair volatile across loss of operating power/reset, requires outstanding soft repairs to be cleared before the documented hard-repair path, and makes repair-resource exhaustion visible to the operation semantics.

This is a vendor operation-document witness. It does not prove that every Samsung DDR4 SKU contains exactly one physical spare wordline per bank group or that Samsung's fuse implementation is shared by other vendors.

### SK hynix 2015-priority PPR patent embodiment

SK hynix's **“Post package repair device”** family has Korean priority on 26 January 2015. The US application was filed 28 April 2015, published as US20160217873A1 on 28 July 2016, and granted as US9666308B2 on 30 May 2017.

The disclosure describes an Array Rupture Electrical-fuse (`ARE`) array that permanently stores failed-address information. After power-up, a boot-up controller scans fuse data used for PPR and provides resource information to a resource-detection unit. The resource state is qualified by channel/bank-group/bank/mat/fuse-address selection, and a masking controller prevents an irreversible rupture operation when no unused fuse remains. The disclosure also describes two banks sharing fuse lines in one grouping while fuse use remains controllable per bank.

This supplies manufacturer-primary implementation evidence for:

```text
persistent repair-fuse state
    -> boot-time resource scan
    -> derived target-qualified availability
    -> irreversible repair allowed or masked
```

It is not a named-product capability sheet and is not projected onto every shipping SK hynix DDR4 part.

### Intel platform authority: BIOS participates in row repair

Intel's **12th Generation Intel Core Processors Datasheet, Volume 1 of 2**, public revision dated 15 June 2023, states that PPR is supported according to JEDEC specification and that BIOS can identify a single row failure per bank and perform PPR to exchange the failing row with a spare row. It lists DDR4 among the supported memory technologies.

This provides a useful system boundary:

> **repair capability inside DRAM ≠ autonomous repair decision inside DRAM.**

At least in this documented platform path, BIOS/controller-side diagnosis and command authority participate in deciding which row address is repaired.

### Lenovo deployment witness: repair can be a boot-time service action

Lenovo ThinkSystem support documentation describes PPR as DIMM self-healing that substitutes access to a bad cell/address row with a spare row inside the DRAM device. Its service guidance distinguishes:

- `sPPR`: repair for the current boot cycle, lost when system power is removed or the system is reset/rebooted;
- `hPPR`: permanent row repair.

A ThinkSystem SR860 V2 support workflow further instructs the operator to restart the system so DIMM self-healing can attempt hard PPR and then check for the successful-repair event.

This is a deployment witness, not a universal PPR scheduling law. It shows that a real server platform can make **reboot/firmware service time** part of the repair lifecycle.

### Intel hard-PPR power-failure disclosure

Intel's patent family **“Dynamic random access memory built-in self-test power fail mitigation”** has a 4 February 2020 priority date. Its background describes PPR as remapping a defective row address to a spare row, distinguishes quick/temporary `sPPR` from slower/permanent `hPPR`, and states that hard PPR can program electrical fuses to disconnect faulty rows/columns and replace them with redundant ones.

Crucially, the disclosure identifies a failure window: in the described implementation context, unexpected power failure during hard PPR may leave electrical fuses partially blown and can make the SDRAM unusable. The proposed mitigation separates test from hard-repair work and starts repair only when the remaining stable-power interval is sufficient.

This is **bounded patent evidence about one hard-repair implementation/problem formulation**, not proof that every DDR4 PPR device has the same fuse technology or failure behavior.

---

## Retained states and relations

Case 119 contains several different states that must not be collapsed into one word such as `memory` or `repair`:

1. **application payload charge** — ordinary volatile DRAM cell state;
2. **logical/platform-visible row address** — the address used to select the row;
3. **original physical row embodiment** — the row that has become defective;
4. **spare physical row embodiment** — the replacement row available inside the DRAM;
5. **repair mapping / decoder state** — the relation that causes the old address to select the spare embodiment;
6. **repair lifetime class** — soft/non-persistent versus hard/persistent;
7. **defect evidence** — platform/device evidence that a row should be retired;
8. **repair authority and sequencing state** — BIOS/controller/mode-register state required to request and complete PPR;
9. **remaining spare/repair resource** — finite replacement capacity available to the bounded device;
10. **derived resource-availability state** — runtime knowledge that a target region can still accept another repair, which the SK hynix patent embodiment reconstructs from persistent fuse state during boot-up.

Only item 1 is the ordinary user payload. Items 5–10 are **second-order retention infrastructure** that determine whether future reads/writes to the same row address reach a usable physical embodiment and whether another repair transition remains possible.

---

## Engineering reconstruction

### Logical row identity can outlive one physical row

The Intel and Micron records describe a failing row address being repaired by substituting a spare row. Therefore the stable object at the interface is not necessarily one permanent physical wordline.

```text
row address A
    -> original physical row
    -> defect discovered
    -> PPR establishes replacement relation
    -> row address A
    -> spare physical row
```

So:

> **logical row-address continuity ≠ physical-row continuity.**

This is a DRAM-scale example of identity surviving replacement of embodiment.

### Repair mapping persistence and payload persistence have different lifetimes

The most important counterexample in this case is that the **repair relation can be more persistent than the data it governs**.

Ordinary DDR4 payload is volatile and requires power plus refresh. Yet hard PPR is documented as permanent/persistent. After a power cycle, the user data from the previous powered session is not thereby preserved, while the hard repair can continue to determine which physical row future accesses use.

Therefore:

> **persistent hPPR mapping ≠ nonvolatile DRAM payload.**

and:

> **retention infrastructure can outlive the payload states whose future embodiments it governs.**

This is a useful inversion of the usual question `does the data survive power loss?` The mapping that decides where later data will live may survive even when the later data itself does not.

### Soft PPR makes repair lifetime an explicit policy dimension

Lenovo's platform documentation states that soft PPR survives only for the current boot cycle and disappears on reset/reboot/power removal, whereas hard PPR is permanent.

Thus one physical spare-row mechanism can support at least two authority lifetimes:

```text
sPPR:
repair relation valid within bounded powered/boot lifetime

hPPR:
repair relation retained across later boots/power cycles
```

Therefore:

> **same repaired address ≠ same repair-state lifetime.**

and:

> **temporary repair mapping ≠ failed repair.**

A soft repair can be intentionally useful precisely because it is reversible/reassignable.

### Remapping a row does not prove preservation of the old row's payload

The inspected sources establish **future address redirection**. They do not establish a universal operation that copies every current bit from the defective row into the spare row before the mapping changes.

Therefore:

> **row-address continuity ≠ payload continuity across the PPR transition.**

That distinction matters especially because documented server hard-PPR workflows may run at reboot, when ordinary volatile session contents are already outside the preservation contract.

Case 14 supplies a useful lower-layer counterexample: SCSI defect reassignment can preserve the same LBA designation while the affected payload still requires separate recovery. The same methodological warning applies here even though the physical mechanisms are different.

### PPR is repair by substitution, not correction of the currently read word

ECC can reconstruct a currently requested value from redundant code information without permanently changing which physical row the address selects. PPR instead changes the future row-resolution relation by substituting a spare physical row.

Therefore:

> **ECC correction ≠ PPR row retirement/substitution.**

A platform may use ECC/error telemetry to discover a candidate row for later PPR, but diagnostic evidence, current-value correction, and physical-row retirement remain separate stages.

### Persistent repair state can itself require a safe transition

The Intel hard-PPR power-failure disclosure is valuable because it prevents `permanent` from being read as `instantaneously and unconditionally safe`. In that disclosed implementation context, establishing persistent repair state involves fuse-programming work that can be interrupted by power loss.

Therefore:

> **persistent repair result ≠ failure-proof repair transition.**

and:

> **retained configuration can have its own durability handoff.**

This is not a universal DDR4 atomicity claim. It is a bounded example showing that the operation which creates long-lived infrastructure state can itself need a protected power/time window.

### Spare capacity is retention infrastructure, not unlimited healing

The bounded Micron product documentation exposes a finite repair-row budget. Once a hard repair occupies a persistent repair address/resource, later repair commands do not simply overwrite it as though the spare relation were cost-free and unbounded.

The SK hynix patent adds another implementation-level boundary: the state that says `repair resource still available` can be reconstructed after power-up by scanning persistent fuse allocation and then used to mask a later rupture when the pool is exhausted.

Therefore:

> **spare-row availability ≠ unlimited future repair capacity.**

and, in the bounded SK hynix embodiment:

> **persistent repair history ≠ runtime capacity state, but runtime capacity can be reconstructed from persistent repair history.**

Reserved silicon and its allocation history can therefore be constitutive retention infrastructure even when they are not carrying ordinary current payload.

---

## Historical record vs engineering reconstruction vs analogy

### Historical record

- a 1979-filed semiconductor-memory patent already describes spare rows/columns taking over addresses of defective standard elements through programmable decoder changes;
- Samsung's 2014 DDR4 operation document exposes bank-group-scoped repair capacity, volatile sPPR versus permanent hPPR, and a clear-before-hard transition rule in its documented path;
- Micron DDR4 product documentation distinguishes non-persistent `sPPR` and persistent/irreversible `hPPR`, exposes finite row-repair resources, and documents a different vendor resource/transition envelope;
- an SK hynix 2015-priority patent embodiment stores failed-address information in electrical fuses, reconstructs resource availability through boot-time scanning, and masks rupture when no unused fuse remains;
- Intel platform documentation makes BIOS a participant in identifying a failing row and exchanging it with a spare row;
- Lenovo server guidance documents reboot-time hard-PPR service and boot-lifetime soft PPR;
- Intel's 2020-priority patent disclosure identifies a hard-PPR fuse-programming power-failure hazard in its bounded implementation context.

### Engineering reconstruction

From those records this repository can safely distinguish:

```text
defect evidence
    != current-value correction
    != repair authorization
    != logical row address
    != original physical row
    != spare physical row
    != repair mapping
    != repair-mapping lifetime
    != payload lifetime
    != repair-transition durability
    != persistent repair-allocation history
    != runtime derived resource availability
    != remaining spare capacity
```

### Functional analogy only

Case 119 is functionally comparable to:

- **Case 14, SCSI defect reassignment** — stable logical designation can survive substitution of a defective physical embodiment;
- **Case 04, mapped Flash** — logical identity can survive changes in physical location/embodiment;
- **distributed repair cases** — a logical object can outlive particular physical holders through replacement.

These are **not** claims of shared mechanism or direct genealogy. DDR4 PPR works inside a volatile semiconductor array with spare-row/decoder state; SCSI disk reassignment works through drive-level logical-block/defect mapping; FTL relocation works under erase/program/reclamation constraints; distributed repair works across machines and protocol authority.

---

## Philosophical / media-theoretical interpretation

Case 119 sharpens one bounded conceptual problem:

> **Which part of a technical memory must remain the same for the system to treat it as the same addressable place?**

The engineering evidence says that material identity of one physical row is not required. A retained repair relation can preserve the **callability** of row address A while replacing the material row that answers to A.

The SK hynix resource-reconstruction witness adds a second, narrower point: even the maintenance possibility itself need not persist as one byte-identical runtime object if durable repair-allocation traces allow the device to reconstruct which future substitutions remain possible after power-up.

The stronger philosophical claim should stop there. This case does not prove that logical identity is immaterial, nor that a DRAM row is `tertiary retention`, nor that addressability by itself constitutes Heideggerian `Bestand`. The retained mapping and repair-resource traces are themselves material/technical state, require spare silicon and repair machinery, and can fail during establishment.

The useful conclusion is narrower:

> technical persistence can reside partly in a **retained rule of substitution** and in durable traces from which future substitution capacity can be reconstructed, rather than in persistence of one physical bearer or one runtime control object.

---

## Counterexamples and limits

1. **PPR is not the origin of semiconductor spare-row repair.** The 1979 filing already establishes address takeover by redundant rows/columns.
2. **The 1979 patent is not PPR.** Its laser-fuse manufacturing/test procedure is historically and operationally different from a post-package platform command path.
3. **`hPPR` persistence does not make DRAM data persistent.** Repair metadata and payload have different volatility classes.
4. **`sPPR` non-persistence does not make the repair useless.** Its reversibility is a deliberate lifetime property.
5. **A row replacement does not prove data migration.** No universal payload-copy claim is made.
6. **PPR does not prove ECC is unnecessary.** Correction/detection and permanent row substitution solve different parts of the failure lifecycle.
7. **Intel's fuse-power-failure disclosure is implementation-bounded.** It is not projected onto every vendor's internal hard-PPR technology.
8. **Samsung, Micron, and SK hynix evidence layers are not symmetrical.** A Samsung operation document, Micron product documentation, and an SK hynix patent embodiment cannot be silently treated as three equivalent shipping-product contracts.
9. **One vendor's repair-resource geometry is not a universal DDR4 capacity law.** Cross-vendor counts, sharing, and transition rules differ or remain unproven.
10. **A patent embodiment is not proof of a named shipping SKU.** SK hynix product-level confirmation remains open.
11. **A successful platform PPR event is not a forensic proof of every internal mapping bit.** Independent fault injection and post-repair characterization remain separate evidence.
12. **Permanent repair ≠ secure erasure of the retired row.** The inspected evidence does not establish sanitization, overwrite, or forensic inaccessibility of the defective physical row.

---

## Related repositories

- [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) — broader semiconductor-memory redundancy, decoder/fuse history, DIMM/controller/platform history, and JEDEC chronology belong there if developed; searches in this round found no dedicated `PPR` / `Post Package Repair` case to reuse.
- [`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) — use its anti-anachronism discipline: `logical identity survives physical replacement` and `runtime repair capacity is reconstructed from retained allocation history` are this repository's engineering reconstructions, not language attributed to 1979 or DDR4 actors unless a source says so.

---

## Evidence debt / future work

- establish the exact JEDEC revision/ballot chronology by which `hPPR` and `sPPR` entered DDR4 rather than assuming initial JESD79-4 already contained both;
- obtain a stable official Micron-hosted archive or page-preserving facsimile for the bounded 2020 DDR4 product documentation;
- obtain a **named SK hynix DDR4 product** operation/datasheet witness before turning the 2015 patent embodiment into a product-level capacity or transition claim;
- extend the now-grounded Micron target-row/associated-row preservation semantics to JEDEC text and named Samsung/SK hynix products before making any cross-vendor payload-retention rule;
- inspect how ECC/patrol scrub/error thresholds hand off row-defect evidence to firmware repair decisions on named platforms;
- test hard-PPR power-failure behavior and recovery on sacrificial hardware where safe and practical;
- characterize physical repair-resource topology/counts, exhaustion telemetry, and success/failure reporting on named DIMMs without projecting any one vendor's bounded behavior across others;
- investigate interactions among manufacturing-time redundancy, post-package repair, internal address scrambling/remapping, RowHammer mitigation, and later DDR5 repair features.

These are future bounded slices. They are not blockers for the present `logical address vs physical row vs repair-state lifetime vs reconstructed repair-capacity state` result.
