# Synthesis 26 deepening — typed reset events, state-class persistence, and evidence closure

## Status

**`bounded focused synthesis`** — this packet deepens [`Synthesis 26 — Maintenance-Control State: Persistence Horizon, Reconstitution, and Authority`](../docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md) by adding an event-typing boundary that the existing persistence-horizon taxonomy needs explicitly.

The synthesis compares three already-grounded witnesses:

- [`Case 85 — NAND read retry`](../cases/85-toshiba-nand-shift-read-retry-recoverability.md), especially [`85-micron-2015-read-retry-reset-survival-correction-deepening.md`](85-micron-2015-read-retry-reset-survival-correction-deepening.md);
- [`Case 148 — NVMe Device Self-test`](../cases/148-nvme13-device-self-test-reset-surviving-maintenance.md), including the 2017 NVM Express 1.3 contract and the later named-device ULINK / Lexar conformance witness;
- [`Case 38 — Intel DC S3700 power-loss-infrastructure self-test`](../cases/38-intel-s3700-power-loss-imminent-self-test.md), especially [`38-intel-s3700-d000h-policy-persistence-boundary-deepening.md`](38-intel-s3700-d000h-policy-persistence-boundary-deepening.md).

The bounded result is:

```text
"survives reset"
    is not a scalar durability property

it is a claim over at least:
    named state class
    × named event class
    × interface / authority layer
    × survival semantics
    × evidence layer
```

This packet does **not** create a historical lineage among NAND feature registers, NVMe Device Self-test, and ATA/SCT policy controls. Their comparison is engineering reconstruction over independently grounded cases.

---

## 1. Research question

Synthesis 26 already distinguishes maintenance-control states that are reinitialized, persisted and resumed, persisted and rebound, or deliberately discarded and replayed. A remaining shorthand can still hide important differences:

> What exactly does it mean to say that maintenance-control state “survives reset”?

The phrase can collapse several independent questions:

1. **Which reset?** Raw-NAND `FFh`, synchronous `FCh`, LUN reset `FAh`, NVMe Controller Level Reset, ATA hard reset, full power loss, firmware activation, or another event?
2. **Which state?** In-flight operation state, configuration, scheduling policy, diagnostic obligation, progress, result history, payload, or cache/register contents?
3. **What form of survival?** Exact value preservation, logical continuation after reconstitution, replay from stronger retained evidence, restoration to a nonvolatile default, or merely continued authority to perform future work?
4. **What evidence exists?** Generic protocol capability, named-product contract, named-feature support, conformance observation, or implementation/fault trace?

The cross-case answer is that none of these dimensions can safely be omitted.

---

## 2. Evidence ledger and source custody

### 2.1 Case 85 — Micron L83A read-retry feature `89h`

Primary product document:

- Micron Technology, **32Gb, Asynchronous/Synchronous NAND**, L83A family, Rev. A, May 2015 (`L83A_32Gb_Async_Sync_NAND_mlc_plus.pdf`).
- Public copies already inspected in Case 85:
  - <https://www.farnell.com/datasheets/3761294.pdf>
  - <https://www.unikeyic.com/media/datasheet/d9/6b/ded2/d9/8c2c3bd5996175045d2af62c6e827efe.pdf>

Relevant sections are the RESET command descriptions, Configuration Operations, Feature Address `89h: Read Retry`, and Read Retry Operations.

The dedicated Case-85 correction packet records the exact-family result: feature-address values generally survive `RESET (FFh)`, `SYNCHRONOUS RESET (FCh)`, and `RESET LUN (FAh)` unless a feature-specific exception says otherwise; `89h` has no such reset exception in the inspected table. The same product document says selected read-retry settings remain in use until `89h` is rewritten or the device is powered down.

### 2.2 Case 148 — NVM Express Device Self-test

Normative primary document:

- NVM Express, Inc., **NVM Express Revision 1.3**, ratified 26 April 2017, document dated 1 May 2017.
- <https://nvmexpress.org/wp-content/uploads/NVM_Express_Revision_1.3.pdf>

The already-grounded Case-148 reading distinguishes short and extended Device Self-test around Controller Level Reset:

- a **short** Device Self-test is aborted by Controller Level Reset;
- an **extended** Device Self-test persists across Controller Level Reset and resumes after reset / restoration of power;
- the exact segment from which extended testing resumes is vendor specific.

Later bounded conformance witness:

- ULINK Technology, **NVMe-PTC Test Result**, March 2026, Lexar `NM7A1 SSD`, firmware `M7100`.
- <https://ulinktech.com/wp-content/uploads/2026/03/NVMe_Ptc_LexarNM7A1SSD_0C6BEJXU4TBG94UZYY6P_02.pdf>

The public report records controller-reset `PASS` rows for short and extended DST, a power-cycle `PASS` row for short DST, and `N/A` for the extended-DST power-cycle row. That report is later conformance evidence, not evidence of the original 2017 implementation mechanism.

### 2.3 Case 38 — Intel DC S3700 `D000h` maintenance-policy state

Primary named-product document:

- Intel, **Intel Solid-State Drive DC S3700 Product Specification**, October 2012, order `328171-001US`.
- <https://download.intel.com/newsroom/kits/ssd/pdfs/Intel_SSD_DC_S3700_Product_Specification.pdf>

The product exposes SCT Feature Control code `D000h` as the **Power Safe Write Cache capacitor test interval**.

Protocol-level primary / standards-development witness:

- T13/2161-D Revision 1b, **Working Draft ATA/ATAPI Command Set - 3 (ACS-3)**, 17 October 2011, §8.3.4.
- Public copy used in the Case-38 packet: <https://nevar.pl/pliki/ATA8-ACS-3.pdf>

SCT Feature Control distinguishes volatile state from state requested to survive power/reset events and provides a function to return feature option flags. But the inspected S3700 product specification does not disclose the `D000h`-specific option flags or establish whether that named feature accepts the persistent setting.

### 2.4 Companion-repository check

A fresh search of `tmzncty/computing-archaeology` for the combined reset/persistence topics (`NAND`, `NVMe Device Self-test`, `SCT Feature Control`) found no dedicated packet to reuse.

That does **not** mean broad reset-command genealogy belongs in this repository. If a cross-vendor history of reset semantics, command namespaces, or controller-reset architecture is developed later, it belongs primarily in `computing-archaeology`. This packet keeps only the retention-specific relation among event identity, state lifetime, and evidence strength.

---

# 3. Historical / technical record

## H-26R.1 — Micron L83A ordinary reset can abort work while preserving read-retry configuration

The Micron L83A product evidence establishes two simultaneous facts.

First, its reset commands can terminate active protocol/array work. The Case-85 packet records that RESET can abort command sequences, cancel pending array operations, clear the command register, and invalidate data/cache-register contents; an interrupted PROGRAM or ERASE can leave affected data partially programmed/erased and invalid.

Second, the same product's Configuration Operations section gives a default rule that feature-address values do not change under host `FFh`, `FCh`, or `FAh` reset unless otherwise specified. Feature `89h` is the read-retry selector and does not carry a reset-specific exception in the inspected table.

Therefore, on this named family:

```text
FFh / FCh / FAh
    -> active work may be aborted
    -> working register contents may be invalidated
    -> read-retry feature 89h remains selected
```

The historical/product claim is bounded to the documented L83A family and those reset classes.

## H-26R.2 — Micron separately names power-down as the retirement boundary for selected retry state

The same Read Retry Operations section states that after the host selects `89h`, subsequent reads use the chosen internal settings until the feature is rewritten or the device is powered down.

Thus the source itself requires at least two event classes:

```text
ordinary documented NAND reset
    !=
power-down
```

for the lifetime of this state.

The product documentation does not identify the physical carrier of `89h`; this synthesis therefore does not translate reset survival into a claim that the setting is stored in NAND, EEPROM, fuse, SRAM, or any other particular structure.

## H-26R.3 — NVMe 1.3 assigns different reset behavior to short and extended Device Self-test

The NVMe 1.3 Device Self-test contract does not assign one universal consequence to Controller Level Reset.

The already-grounded normative distinction is:

```text
short Device Self-test
    + Controller Level Reset
    -> abort

extended Device Self-test
    + Controller Level Reset
    -> persists / resumes
```

The extended operation also has a restoration-of-power continuation contract, while the segment from which it resumes is vendor specific.

This is not an assertion that every internal progress bit survives unchanged. The historical contract is at the operation/obligation level.

## H-26R.4 — later named-device conformance strengthens only the controller-reset observation it actually executes

The 2026 ULINK report for a Lexar NM7A1 / firmware M7100 provides a later named-device test artifact. It records:

```text
Short DST with RESET
    Controller Reset      PASS
    Power Cycle Reset     PASS

Extended DST with RESET
    Controller Reset      PASS
    Power Cycle Reset     N/A
```

This is useful because it separates a named controller-reset conformance observation from a still-unobserved named extended-power-cycle branch.

The report does not disclose the controller's hidden resume checkpoint, the exact before/after percentage complete, or the resume segment. `PASS` is therefore not rewritten here as “exact progress bytes persisted.”

## H-26R.5 — SCT can express persistence even where the named S3700 feature's persistence remains unproved

Intel's S3700 product specification establishes that `D000h` exists as an SCT Feature Control code for the capacitor-test interval.

The contemporaneous ACS-3 working draft establishes a generic SCT Feature Control persistence distinction: a set operation can request state that is preserved during power/reset events, while a volatile setting returns after hard reset to a default or last nonvolatile setting; the interface can also return feature option flags.

But the checked S3700 specification does not close the named-feature link:

```text
SCT has persistence machinery
    +
S3700 exposes D000h through SCT
    !=
S3700 D000h is proved to support persistent setting
```

This is a historical evidence boundary, not a firmware-quality judgment.

## H-26R.6 — Intel Software Settings Preservation is a separate surface

The S3700 also advertises ATA Software Settings Preservation, but the product specification presents it separately from SCT Feature Control. No inspected Intel or standards text used here states that SSP is the persistence mechanism for `D000h`.

Therefore this synthesis preserves:

```text
same product supports SSP
    !=
D000h is governed by SSP
```

The similarity of the word “preservation” does not establish scope identity.

---

# 4. Engineering reconstruction

Everything in this section is project analysis over the historical records above. It is not Micron, NVM Express, Intel, ULINK, or T13 vocabulary unless explicitly quoted in the underlying case.

## E-26R.1 — `reset` must be typed by interface layer and event identity

A raw-NAND reset opcode and an NVMe Controller Level Reset are not interchangeable events merely because both are casually called “reset.” An ATA/SCT hard-reset boundary is another interface-defined event again.

For cross-case analysis, use at least:

```text
reset claim =
    interface layer
    + exact event / command class
    + affected scope
    + named state object
    + documented transition
```

So:

> **same word `reset` != same event boundary.**

This blocks accidental comparisons such as treating NAND `FFh` as if it were the same event as an NVMe controller reset or as if every full system power cycle were simply a “stronger spelling” of a device-local command reset.

## E-26R.2 — the same event can retire one state class and preserve another

Micron L83A is a direct product-level counterexample to a global reset-state model:

```text
same FFh/FCh/FAh event
    -> in-flight operation: aborted
    -> data/cache-register state: invalidated
    -> read-retry feature 89h: preserved
```

Therefore:

> **same event != same state consequence.**

A device can reach a known protocol condition without every state class returning to its power-on default.

## E-26R.3 — survival semantics range from exact configuration preservation to obligation continuation

Case 85 and Case 148 should not be merged into one kind of “persistence.”

Case 85 directly establishes continued selection of a configuration value across named reset events.

Case 148 establishes something different for extended DST: the maintenance operation remains an obligation that must continue after reset/restoration. The standard deliberately leaves the exact resume segment vendor specific.

Thus:

```text
configuration-value survival
    !=
operation-level continuation
    !=
exact microstate survival
```

and:

> **state survives != exact internal representation survives unchanged.**

The minimum retained information for restart can be less than a byte-for-byte image of the pre-reset execution state if the operation can be safely reconstituted or replayed from a coarser checkpoint.

## E-26R.4 — operation abort and configuration retirement are orthogonal predicates

Combining Case 85's two results gives a useful two-axis model:

```text
                 configuration survives?    configuration retired?
operation aborts       L83A witness                 possible elsewhere
operation resumes      possible                    possible after reinit
```

The point is not to populate every quadrant historically. It is to forbid this shortcut:

```text
operation aborted
    therefore
all related configuration reset
```

No such implication exists in the L83A record.

## E-26R.5 — protocol expressiveness is not named-feature evidence

Case 38 exposes another kind of overclaim. A protocol can define a persistence selector before a product-specific manual states whether a particular vendor feature supports it.

The evidence ladder is:

```text
protocol can express persistent state
    ↓ not automatic
named product implements the protocol family
    ↓ not automatic
named feature accepts / reports persistence option
    ↓ not automatic
controlled reset/power experiment confirms behavior
```

Therefore:

> **protocol can express persistence != named feature supports persistence.**

This is an evidence-transition rule as much as a state-transition rule.

## E-26R.6 — a product feature witness, normative contract, and conformance test answer different questions

Case 148 makes the distinction especially visible:

```text
normative specification
    -> what compliant behavior is required

product feature declaration
    -> named product claims/exposes the feature

third-party conformance result
    -> bounded tested scenario passed or was not run

implementation / fault trace
    -> how the state was actually retained/reconstituted
```

A stronger layer cannot be silently synthesized when the artifact only supports a weaker one.

For example:

```text
Extended DST + Controller Reset PASS
    !=
public proof of exact resume checkpoint format
```

and:

```text
Extended DST normative power-restoration rule
    !=
Lexar NM7A1 extended power-cycle test PASS
```

because the inspected ULINK row is `N/A`.

## E-26R.7 — persistence horizon is not always a single ordered ladder of event strength

It is tempting to model events as one scale:

```text
command reset < controller reset < power cycle
```

The cross-case evidence does not justify that universal ordering.

Different interfaces define different scopes and retained domains. A controller-level reset can preserve some subsystem state while reinitializing controller-local state; a raw NAND command reset addresses a target/LUN protocol state; an ATA hard reset and full removal/restoration of power have other semantics.

Accordingly, Synthesis 26 should treat the “minimum persistence horizon” as a named boundary, not merely an ordinal score.

Better:

```text
survives {FFh,FCh,FAh}
loses on power-down
```

or:

```text
extended operation continues across NVMe Controller Level Reset;
named-device power-cycle conformance remains unobserved
```

rather than:

```text
persistence level = 2
```

## E-26R.8 — reset-safe maintenance may preserve a relation rather than a representation

Case 148 sharpens a principle already present elsewhere in the repository:

```text
retained relation:
    "this extended diagnostic remains due and must continue"

possible implementation:
    exact checkpoint
    coarse segment checkpoint
    restart of a bounded segment
    another vendor-specific reconstitution path
```

The normative contract constrains the relation while leaving some representation details open.

Therefore:

> **semantic continuation obligation != specified persistence embodiment.**

This is precisely why conformance and implementation evidence must remain separate.

## E-26R.9 — power-down can be a stronger boundary for one state without being global forgetting

Micron's read-retry setting ends at power-down, yet the NAND payload is not thereby erased. Conversely, NVMe extended DST has a normative restoration-of-power continuation relation even though active execution necessarily stops while power is absent.

So:

```text
power absent
    !=
all retained state absent
```

and:

```text
state unavailable during outage
    !=
continuation obligation forgotten
```

Again, the state class matters.

---

# 5. Event/state/evidence matrix

The matrix below is engineering synthesis over grounded records; it is not a historical table used by the original designers.

| Witness | Named state / relation | Named event | Documented result | Survival semantics | Evidence closure |
| --- | --- | --- | --- | --- | --- |
| Micron L83A, Case 85 | read-retry feature `89h` | NAND `FFh` / `FCh` / `FAh` | feature value generally unchanged absent exception | configuration-value survival | named-product direct contract |
| Micron L83A, Case 85 | in-flight command / array operation | NAND reset | command sequence / pending work aborted; working registers invalidated as documented | operation retirement | named-product direct contract |
| Micron L83A, Case 85 | read-retry feature `89h` | power-down | selected setting ends | configuration retirement | named-product direct contract |
| NVMe 1.3, Case 148 | short Device Self-test | Controller Level Reset | abort | maintenance obligation retired/aborted | normative contract; later named controller-reset test witness |
| NVMe 1.3, Case 148 | extended Device Self-test | Controller Level Reset | persists and resumes | operation-level continuation; exact resume segment vendor-specific | normative contract + later named controller-reset conformance |
| NVMe 1.3, Case 148 | extended Device Self-test | restoration of power | continuation required | operation-level continuation | normative contract; named Lexar extended power-cycle row remains `N/A` |
| Intel S3700 / SCT, Case 38 | `D000h` capacitor-test interval | SCT power/reset persistence option | protocol can request persistent or volatile state | selectable policy-state horizon at protocol level | protocol rule + named-product feature exposure; named-feature support still open |

The table fixes four independent dimensions:

```text
state identity
    != event identity
    != survival semantics
    != evidence closure
```

A cross-case statement that omits one of them is at high risk of overclaiming.

---

# 6. Addition to the Synthesis-26 comparison discipline

Synthesis 26 already asks about role, target relation, minimum horizon, referent/currentness, reconstitution, fallback, authority, consequence, history semantics, and durability evidence.

This deepening adds four questions that should be made explicit whenever `reset` or `restart` appears:

| Added axis | Question |
| --- | --- |
| **event namespace / layer** | Which interface defines this reset/restart event — media command, controller, subsystem, host process, power domain, or system? |
| **state-specific transition** | Which named state class is preserved, aborted, invalidated, reinitialized, replayed, or restored? |
| **survival semantics** | Is the same value preserved, is an obligation reconstituted, is work replayed, or is only a default/nonvolatile policy restored? |
| **evidence closure** | Is the claim protocol-generic, named-product, named-feature, conformance-tested, or implementation/fault-traced? |

The revised shorthand should therefore be:

```text
maintenance-control persistence claim
    = role
    + referent
    + named event
    + state-specific transition
    + reconstitution/fallback
    + evidence layer
```

rather than merely:

```text
this metadata survives reset
```

---

# 7. Why this matters for the repository's main bridge

The repository's bridge thesis separates state transitions from evidence transitions. These witnesses show both at once.

### State transition side

```text
reset event
    -> one operation can end
    -> another configuration can remain
    -> another obligation can survive only as a requirement to resume
```

### Evidence transition side

```text
protocol defines persistence machinery
    !=
named feature proven to use it

normative continuation requirement
    !=
named-device conformance observation

conformance PASS
    !=
implementation checkpoint disclosed
```

So the same analytical discipline prevents two different mistakes:

1. collapsing different internal state classes into one reset outcome;
2. collapsing different evidence classes into one confidence level.

---

# 8. Functional analogy — bounded only

A measuring instrument provides a useful functional analogy.

An acquisition may be aborted while the selected calibration preset remains active. A long diagnostic may be required to resume after a controller restart even if it restarts from the beginning of the current phase. A separate maintenance interval may have an interface that supports persistent configuration even if the particular model's support for that option has not been observed.

The analogy helps separate:

```text
work execution
configuration
continuation obligation
policy persistence
```

It is **not** evidence that NAND, NVMe controllers, ATA/SCT drives, and laboratory instruments share an implementation, history, or design genealogy.

---

# 9. Philosophical interpretation — downstream only

One restrained interpretation follows from the engineering record:

> `reset` is not technical annihilation in the abstract. It is a named event whose significance is defined only in relation to a named state or obligation.

A reset can be discontinuity for an operation and continuity for a configuration at the same time. A continuation requirement can survive even when the exact pre-interruption microstate is not specified as the thing that persists. A protocol may make persistence expressible before available evidence proves a particular product feature actually uses that affordance.

Thus technical continuity is plural and typed. This is project interpretation, not historical actor vocabulary.

---

# 10. Explicit non-claims

This packet does **not** claim that:

1. raw-NAND `FFh`, `FCh`, or `FAh` is the same event as an NVMe Controller Level Reset;
2. NVMe Controller Level Reset is the same event as ATA hard reset, host reboot, firmware activation, or complete device power removal;
3. all reset events can be placed on one universal weakest-to-strongest ladder;
4. every Micron NAND family preserves every feature address across `FFh/FCh/FAh`;
5. Micron L83A `89h` survives power-down — the inspected source gives the opposite boundary;
6. the physical carrier of L83A `89h` is known from the product document;
7. an NVMe extended Device Self-test preserves every exact progress bit across reset;
8. the NVMe 1.3 wording specifies one universal checkpoint representation or resume segment;
9. the 2026 Lexar/ULINK test reveals the firmware's internal restart implementation;
10. the Lexar report demonstrates extended-DST power-cycle continuation — that row is `N/A` in the inspected report;
11. a 2026 conformance witness proves how first-generation 2017 NVMe 1.3 products implemented Device Self-test;
12. Intel S3700 `D000h` is persistent by default;
13. Intel S3700 `D000h` is proven to accept SCT's persistent option bit;
14. S3700 Software Settings Preservation governs `D000h`;
15. generic protocol capability is equivalent to named-feature support;
16. controller reset survival implies power-cycle survival for every state class;
17. operation abort implies configuration reset;
18. configuration survival implies payload correctness, currentness, or maintenance completion;
19. these three cases share a historical genealogy merely because they expose typed persistence boundaries;
20. this packet establishes invention priority for reset-surviving configuration or resumable maintenance.

---

# 11. What this slice closes

Closed for Synthesis 26:

- `reset` is now explicitly modeled as an event-class/interface-layer dimension rather than an untyped persistence horizon;
- a direct same-product counterexample fixes `operation aborted != configuration retired`;
- configuration-value survival is separated from operation-level continuation and exact microstate preservation;
- protocol expressiveness is separated from named-feature persistence evidence;
- normative contract, named-product conformance, and implementation evidence are explicitly separated;
- persistence horizons are no longer assumed to form one universal scalar ladder across interfaces.

This does **not** change the maturity/status of Cases 38, 85, or 148. It deepens the cross-case analytical discipline only.

---

# 12. Still open

The most valuable next evidence is now narrower:

- a real Micron L83A command transcript reading `89h` before/after `FFh`, `FCh`, `FAh`, and controlled power cycle;
- a named NVMe device trace for **extended** DST across an actual power cycle/restoration, including before/after current-operation and progress fields;
- a firmware/source/fault trace showing whether extended DST resumes from a durable segment checkpoint, reconstructs state, or safely repeats work;
- an Intel S3700 SCT transcript returning `D000h` feature option flags and exercising volatile versus persistent set behavior across hard reset and power cycle;
- evidence around brownout or partial power-domain collapse, which should not be silently equated with clean reset or clean power-down;
- firmware-update / controller-replacement transitions, which may have persistence rules different from ordinary reset;
- broader historical genealogy of reset semantics across storage interfaces, preferably in `tmzncty/computing-archaeology` rather than duplicated here.

---

# 13. Bounded conclusion

The three grounded witnesses reject a generic sentence such as “maintenance metadata survives reset.”

A safer form is always typed:

```text
Micron L83A read-retry 89h
    survives named NAND reset commands
    while in-flight work can be aborted
    and power-down retires the selection

NVMe extended Device Self-test
    survives as a continuation obligation across Controller Level Reset
    without the standard specifying exact resume microstate

S3700 D000h
    lives in a protocol family that can express persistent policy state
    while the named feature's product-specific persistence remains unproved
```

Therefore Synthesis 26 should treat **state class × event class × interface layer × survival semantics × evidence layer** as the minimum form of any reset-persistence claim.