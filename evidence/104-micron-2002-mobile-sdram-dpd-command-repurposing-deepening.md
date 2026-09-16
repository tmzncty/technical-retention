# Evidence 104C — Micron 2002 Mobile SDRAM Deep Power-Down, Command Repurposing, and Reinitialization Boundary

## Status

**`bounded deepening complete`** for one narrow pre-2008 question left open by Case 104:

> How early can this repository directly document a named Micron mobile-DRAM product family in which ordinary Power-Down, SELF REFRESH, and Deep Power-Down already have distinct retention contracts, and what does that document reveal about the command/interface boundary of Deep Power-Down?

This record uses an identifiable Micron manufacturer datasheet preserved as an archival HTML transcription:

- Micron Technology, Inc., **_256Mb: x16 Mobile SDRAM_**;
- product family `MT48V16M16LFFG` / `MT48H16M16LFFG`;
- document designation **`ADVANCE`**;
- footer `MobileRamY26L_A.p65 – Pub. 5/02`;
- copyright 2002 Micron Technology, Inc.

The source pushes the bounded **public manufacturer-document floor** for this repository's Deep Power-Down product evidence from 2008 back to **May 2002**. It does **not** establish a first shipment, first silicon, JEDEC introduction date, invention priority, or an unbroken genealogy into later LPDDR generations.

Case: [`../cases/104-micron-lpddr-selective-adaptive-self-refresh.md`](../cases/104-micron-lpddr-selective-adaptive-self-refresh.md)

Later 2008–2009 availability/optionality record: [`104-micron-hynix-2008-2009-dpd-product-availability-deepening.md`](104-micron-hynix-2008-2009-dpd-product-availability-deepening.md)

Related automatic-TCSR cross-vendor record: [`35-samsung-hynix-2005-2008-auto-tcsr-cross-vendor-deepening.md`](35-samsung-hynix-2005-2008-auto-tcsr-cross-vendor-deepening.md)

---

## 1. Source identity and evidence strength

### H/P* — Micron manufacturer document preserved by a third-party mirror

The surviving transcription identifies the part family, Micron copyright, publication footer, command tables, operating sections, and data-sheet designation. The front matter is marked `ADVANCE` and the final designation note defines that status as containing initial descriptions of products still under development.

Archive used for inspection:

- <https://dtsheet.com/doc/503993/micron-mt48v16m16lffg>

The relevant internal anchors are unusually redundant:

- feature list: TCSR, SELF REFRESH, Deep Power Down, PASR;
- printed page 9: Extended Mode Register, TCSR, DPD, PASR;
- printed pp. 23–24: ordinary Power-Down and Deep Power-Down exit sequence;
- printed page 28 / command-table note: command-sequence reassignment from Burst Terminate to Deep Power-Down for the mobile/BAT-RAM part;
- printed page 58: `Advance` designation definition and `Pub. 5/02` footer.

Because the copy is not served from a current Micron origin, claims here are tagged `H/P*`. The manufacturer identity and document-internal publication markers are strong; shipment status is not.

### Development-stage boundary

The document itself defines `Advance` as describing products still under development. Therefore the safe chronology claim is:

```text
May 2002 manufacturer documentation
    establishes a public design/product-document witness
    !=
May 2002 volume shipment
```

The repository must not turn a development-stage data sheet into a commercial-availability date.

---

## 2. Historical record: three low-power contracts already differ in 2002

### H/P* — ordinary Power-Down disables interface activity but does not perform refresh

The operating section states that Power-Down occurs when CKE is registered low with a NOP or COMMAND INHIBIT while no access is in progress. Input/output buffers other than CKE are deactivated for standby power savings.

The crucial retention clause is explicit: the device **may not remain in Power-Down longer than the refresh period, 64 ms, because no refresh operations are performed in this mode**.

This is direct period evidence for a low-power state that is still constrained by the ordinary dynamic-retention deadline:

```text
Power-Down
    -> reduced interface activity
    -> no refresh while resident
    -> residence time bounded by refresh obligation
```

Nothing in this clause licenses calling ordinary Power-Down `powered off` or `nonvolatile`.

### H/P* — SELF REFRESH internalizes recurring maintenance instead of suspending it

The same 2002 document describes SELF REFRESH separately. Once self refresh is engaged, the SDRAM provides its own internal clocking and performs its own refresh cycles while CKE remains low.

The document also gives TCSR and PASR controls in the Extended Mode Register. In this early part, TCSR is controller-programmed according to case temperature; PASR selects how much of the array is maintained during SELF REFRESH.

Thus the source already exposes three separable questions:

```text
who generates recurring refresh?
how often should it run?
which array regions receive it?
```

This evidence predates the later automatic-TCSR product semantics analyzed in Case 35. It must not be rewritten as though the 2002 device already used the later on-die automatic temperature-authority model.

### H/P* — Deep Power-Down explicitly withdraws the payload-retention contract

The DPD section describes Deep Power-Down as a maximum-power-saving mode achieved by shutting off power to the whole memory array and states that **data will not be retained once the device enters Deep Power-Down**.

The safe historical relation is therefore:

```text
ordinary Power-Down
    -> refresh paused; retention deadline still binding

SELF REFRESH
    -> refresh continues internally

Deep Power-Down
    -> array-power support withdrawn; data not retained
```

These are not three intensity levels of one identical retention mechanism. They change different support relations.

---

## 3. Historical record: exiting DPD is not retained-state resume

### H/P* — service restoration requires a multi-step reinitialization sequence

The May-2002 operating section says that after asserting CKE high to leave Deep Power-Down, a new command is not immediately admissible. The documented sequence is:

1. maintain NOP input conditions for a minimum of **200 microseconds**;
2. issue PRECHARGE commands for all banks;
3. issue **eight or more AUTO REFRESH** commands;
4. issue a MODE REGISTER set command to initialize the mode register;
5. issue an EXTENDED MODE REGISTER set command to initialize the extended mode register.

This provides a particularly clear transition boundary:

```text
DPD exited electrically
    !=
normal command service restored
    !=
old payload restored
```

The initialization sequence re-establishes an operationally usable DRAM regime. It is not a recovery procedure for the pre-DPD user data, which the same source places outside the retention contract.

### H/P* — the Extended Mode Register is itself retained control state under ordinary powered conditions

Earlier in the document, Micron says the Extended Mode Register retains its stored information until it is programmed again **or the device loses power**. TCSR and PASR are among the functions controlled there.

The DPD exit procedure then requires both the Mode Register and Extended Mode Register to be initialized before normal command service resumes.

This supports a bounded state decomposition:

```text
array payload state
    !=
refresh-scope/rate configuration state
    !=
mode / command-admission state
```

The source does not expose the physical storage cell used for every configuration bit, nor does it explicitly enumerate every register bit's analog fate during DPD. The safe claim is about the documented retention and reinitialization contract, not undocumented internal circuitry.

---

## 4. Historical record: one command encoding can change meaning across device families

### H/P* — Micron explicitly says the DPD command sequence corresponds to Burst Terminate on traditional SDRAM

The command-table notes contain an unusually useful interface-history sentence. Micron states that Deep Power-Down is a power-saving feature of this Mobile SDRAM / BAT-RAM device and that the same command is **Burst Terminate on traditional SDRAM components**; for the mobile/BAT-RAM device, that command sequence is assigned to Deep Power-Down.

This matters because it blocks a common retrospective shortcut:

```text
same pin pattern / command encoding
    !=
same functional operation across product families
```

A command code has meaning only within the applicable device contract and state machine.

The repository should therefore not infer historical semantic continuity solely from electrical command shape.

### Engineering reconstruction — command identity is contract-relative

The physical pins and truth-table pattern are insufficient by themselves to identify the operation. The same encoded stimulus can denote:

- burst termination on a traditional SDRAM contract;
- entry into a non-retentive deep-power state on the documented mobile/BAT-RAM contract.

This is a useful retention-specific reminder that **interface interpretation is retained context**. A future reader/controller needs the applicable device family/specification, not merely a captured waveform, to recover the operation's meaning.

This is an engineering reconstruction from Micron's explicit contrast, not evidence that historical engineers used the phrase `contract-relative command identity`.

---

## 5. Chronology boundary

### What May 2002 now establishes

For this repository, an identifiable Micron document dated by its own footer to May 2002 already combines:

- ordinary Power-Down with no refresh and a 64 ms residence bound;
- SELF REFRESH with internally generated refresh;
- controller-programmed TCSR;
- PASR with selectively maintained array regions;
- Deep Power-Down with array power removed and payload not retained;
- a substantial DPD-exit reinitialization sequence;
- explicit command-sequence repurposing relative to traditional SDRAM.

The previous 2008 Micron / 2009 Hynix evidence remains useful for **later product continuity and optionality**, but it is no longer the earliest named-product public-document witness currently held by Case 104.

### What May 2002 does not establish

The source does not establish:

- that DPD was invented by Micron;
- that May 2002 was the first publication anywhere;
- that the ADVANCE part was shipping in volume in May 2002;
- the first JEDEC Mobile SDRAM / Mobile DDR / LPDDR revision containing DPD;
- direct lineage from this 2002 Micron command assignment to Samsung, Hynix, later Micron LPDDR, or JEDEC;
- the internal switch/transistor topology used to remove array power;
- exact cell-charge decay after entry;
- forensic unrecoverability or sanitization;
- exact availability across every part-number suffix or later production revision.

---

## 6. Engineering reconstruction

### E — low power is not one retention category

The source directly defeats the idea that lower power has a monotonic relation to `more or less retention`.

```text
Power-Down
    lower activity, but refresh debt keeps aging

SELF REFRESH
    lower external activity, but internal maintenance continues

Deep Power-Down
    deeper power reduction by withdrawing the array-retention condition
```

A low-power-mode name therefore cannot substitute for the mechanism-level question: **what support remains active, and what state is still promised to survive?**

### E — transition completion and service readiness are distinct

Exiting the electrical DPD condition is only the start of a restoration path. The 200 microsecond wait, bank precharge, multiple refreshes, and register initialization show that the device must reconstruct an admissible operating regime before ordinary commands resume.

This supports:

```text
power-domain transition complete
    !=
interface ready
    !=
payload recovered
```

### E — configuration state can be retention infrastructure

TCSR/PASR mode-register state is not user payload. Yet it determines the cadence and coverage of self-refresh maintenance. The 2002 document therefore supplies another example of small control state governing the future survivability of a much larger array.

### E — non-retention is weaker than secure erasure

Micron's statement that data will not be retained is an operational product contract. It does not specify an erase-verification method, a maximum remanence interval, forensic recovery resistance, or a sanitization assurance level.

Therefore:

```text
outside documented retention contract
    !=
verified sanitization
```

---

## 7. Functional comparison — explicitly non-genealogical

### Case 21 / Case 35 / Case 104

The useful DRAM-family comparison is relational:

- Case 21: recurring refresh responsibility can move from controller-issued AUTO REFRESH to device-internal SELF REFRESH;
- this 2002 Case-104 witness: ordinary Power-Down pauses refresh, SELF REFRESH continues it internally, and DPD withdraws the array-retention condition;
- Case 35: later 2005–2008 Mobile-DDR products can automate temperature-conditioned cadence internally while PASR remains a separate coverage control.

This does not prove a linear invention genealogy or unchanged implementation.

### Case 02 magnetic core

Magnetic core provides the opposite power-boundary counterexample: quiescent magnetic payload can survive loss of ordinary power even though control state and safe transition procedures remain separate. The 2002 mobile SDRAM DPD contract instead explicitly withdraws payload retention.

The comparison is functional only.

### Case 146 Flash erase suspend / abort

Both cases distinguish a powered suspended/low-activity state from a deeper transition that does not preserve the same operational continuation contract. The underlying physical mechanisms are unrelated; the comparison concerns only **state-transition semantics**.

---

## 8. Philosophical limit

The engineering record supports a narrow conceptual observation:

> `remaining available` depends not only on whether a substrate still physically contains a distinction, but on which maintenance and interpretation regime remains in force across a state transition.

That does not make DPD a philosophical theory of forgetting. Nor does it imply that intentional withdrawal of a retention guarantee is equivalent to archival erasure, human forgetting, or Stieglerian tertiary retention.

The strongest allowed conclusion is technical: **the future of the payload is governed by a mode-specific support contract, and the same interface encoding can participate in different contracts on different devices.**

---

## 9. Claim ledger

| Claim | Type | Evidence status |
| --- | --- | --- |
| Micron's `MT48V16M16LFFG` / `MT48H16M16LFFG` ADVANCE datasheet carries `Pub. 5/02` and ©2002 Micron markers | H/P* | strong manufacturer-document identity on archival mirror |
| `ADVANCE` means the document describes products still under development | H/P* | explicit data-sheet designation note |
| the May-2002 feature set includes TCSR, SELF REFRESH, DPD, and PASR | H/P* | explicit feature list / operation sections |
| ordinary Power-Down performs no refresh and is bounded by the 64 ms refresh period | H/P* | explicit operation text, printed p. 23 |
| SELF REFRESH provides internal clocking and refresh cycles | H/P* | explicit self-refresh text |
| DPD shuts off array power and places payload outside the retention contract | H/P* | explicit DPD text, printed pp. 9 and 24 |
| DPD exit requires 200 µs NOP, all-bank precharge, eight or more AUTO REFRESH commands, and MR/EMR initialization | H/P* | explicit exit sequence, printed p. 24 |
| Micron states the corresponding command is Burst Terminate on traditional SDRAM but assigned to DPD on the mobile/BAT-RAM part | H/P* | command-table note |
| same electrical command encoding guarantees the same semantic operation across SDRAM families | X | explicitly contradicted by Micron's command note |
| May-2002 ADVANCE documentation proves volume shipment in May 2002 | X | explicitly contradicted by development-stage designation |
| May-2002 documentation proves invention priority or JEDEC introduction | X | outside evidence scope |
| `data will not be retained` proves sanitization / forensic unrecoverability | X | no erase-assurance or remanence evidence |
| electrical exit from DPD equals immediate service readiness | X | contradicted by mandatory exit/reinitialization sequence |
| reinitialization restores the pre-DPD user payload | X | contradicted by non-retention contract |
| interface operation identity is contract-relative rather than derivable from a pin pattern alone | E | strongly bounded reconstruction from explicit Burst-Terminate/DPD reassignment |

---

## 10. What this closes and what remains open

This slice closes one previously explicit Case-104 debt:

```text
pre-2008 named-product DPD documentation
```

is no longer wholly open. The repository now has a May-2002 manufacturer-document witness, albeit at `ADVANCE` development-document status.

Still open:

- pre-2002 product and patent genealogy;
- first shipping/commercial availability of this Micron family;
- JEDEC normative introduction and revision history for DPD / PASR / TCSR;
- exact relationship between `BATRAM`, `Mobile SDRAM`, `Mobile DDR`, and later LPDDR nomenclature in standards and vendor product lines;
- command-assignment genealogy across standards revisions and vendors;
- physical power-domain implementation and analog remanence after DPD;
- controller policy deciding when to enter DPD;
- direct experimental validation on surviving hardware.

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for the exact part number and for `Deep Power Down` found no dedicated module to reuse. Broader semiconductor-memory product/standard genealogy should be developed there if pursued; this record keeps only the retention-specific state-transition and interface-semantic boundary.

---

## Sources

1. Micron Technology, Inc., **_256Mb: x16 Mobile SDRAM_**, `MT48V16M16LFFG` / `MT48H16M16LFFG`, `ADVANCE`, document footer `MobileRamY26L_A.p65 – Pub. 5/02`, ©2002 Micron Technology, Inc. Manufacturer document preserved as archival HTML transcription: <https://dtsheet.com/doc/503993/micron-mt48v16m16lffg>. Inspected anchors include printed pp. 9, 23–24, 28, and 58.
2. [`104-micron-hynix-2008-2009-dpd-product-availability-deepening.md`](104-micron-hynix-2008-2009-dpd-product-availability-deepening.md) for later Micron/Hynix DPD continuity and Hynix optionality/configuration-loss evidence.
3. [`35-samsung-hynix-2005-2008-auto-tcsr-cross-vendor-deepening.md`](35-samsung-hynix-2005-2008-auto-tcsr-cross-vendor-deepening.md) for the later cross-vendor automatic-TCSR/PASR product-semantic comparison. Its DPD mentions are not reused here as invention evidence.
