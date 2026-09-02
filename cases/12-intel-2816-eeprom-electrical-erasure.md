# Intel 2816 EEPROM: Electrical Erasure, Byte Granularity, and Endurance-Bounded Forgetting

## Status

**`grounded`** — bounded to Intel's 1981 2816 E²PROM product documentation and an Intel-assigned 1978-priority floating-gate tunneling patent used to ground the manufacturer-primary electrical program/erase mechanism class without silently identifying the patent embodiment as the exact 2816 production cell.

Grounding record: [`../evidence/12-intel-1978-1981-eeprom-electrical-erasure-grounding.md`](../evidence/12-intel-1978-1981-eeprom-electrical-erasure-grounding.md).

## Scope

This case is not a general history of EEPROM and does not claim one linear invention sequence from EPROM to Flash.

It asks one bounded retention question:

> What changes when deliberate erasure of a nonvolatile floating-gate state becomes an electrically controlled, in-system operation with selectable erase granularity, while still requiring a special high-voltage/timed regime and consuming a finite rewrite budget?

Case 11 established an Intel/Frohman regime in which the floating-gate state is electrically programmed and nondestructively read but deliberately discharged by radiation. Case 12 studies the next change in the control relation: erasure is now electrical as well.

The primary sources are:

1. Intel, **2816 — 16K (2K × 8) Electrically Erasable PROM**, AFN-01635B, 1981, directly inspected as a page-preserving manufacturer scan;
2. Dov Frohman-Bentchkowsky, Jerry Mar, George Perlegos, and William S. Johnson / Intel, US4203158A, **Electrically programmable and erasable MOS floating gate memory device employing tunneling and method of fabricating same**, priority 24 February 1978.

The first source grounds a named commercial product's operating regime. The second grounds a contemporary Intel physical mechanism for moving charge onto and off an insulated floating gate through thin oxide. They are not treated as proof that the patent drawing is the exact transistor-level production implementation of the 2816.

## Why this changes the comparison

Case 11's bounded EPROM relation was:

```text
hold
    trapped charge behind an insulating barrier

program
    addressed electrical stress

read
    lower-stress electrical sensing

erase
    external radiation applied to the device
```

Intel's 2816 changes the erase side:

```text
hold
    nonvolatile floating-gate state

read
    ordinary 5 V service regime

byte erase / byte write
    electrically selected operation
    + 21 V VPP pulse
    + millisecond-scale timing

chip erase
    separate electrical control condition
    + 21 V VPP
```

The result is not `erasure has become ordinary`. It is more precise:

> **the authority and geometry of forgetting move inside the electrical control system, while erase remains a special state-changing mode with its own voltage, timing, sequencing, and lifetime cost.**

That is the retention-specific reason to study EEPROM separately from both UV EPROM and later Flash.

## Historical vocabulary

Intel's 1981 document directly uses:

- `ELECTRICALLY ERASABLE PROM`;
- `E²PROM`;
- `HMOS-E FLOTOX Cell Design`;
- `Reliable Floating Gate Technology`;
- `Single Byte Erase/Write Capability`;
- `Byte Erase`;
- `Byte Write`;
- `Chip Erase`;
- `VPP` / `PROGRAM VOLTAGE`;
- `in-system alteration of non-volatile information`.

US4203158A uses period language including:

- `electrically programmable and electrically erasable MOS memory device`;
- `floating gate`;
- `thin oxide`;
- `tunnel electrons` / tunneling;
- `program` and `erase`.

`erase authority`, `erase geometry`, `service regime`, and `endurance-bounded forgetting` are project comparison terms, not Intel's historical vocabulary.

## Historical record

### H/P — the 2816 brings erasure into an electrical, in-system control path

Intel's 1981 p. 1 calls the 2816 a `16K (2K × 8) ELECTRICALLY ERASABLE PROM` and says it can be erased and reprogrammed on a byte basis. It explicitly contrasts its electrical erase/write capability with earlier optical erasure and presents the device as suitable for `in-system` alteration of nonvolatile information.

This is stronger than the abstract statement `EEPROM can be erased electrically`. The manufacturer is describing a concrete service relation: a selected nonvolatile state can be deliberately reset and rewritten without removing the package for UV exposure.

### H/P — electrical control does not collapse read, erase, and write into one regime

The 2816 is not simply `5 V RAM that happens to remember power loss`.

Intel's mode table separates:

- READ;
- STANDBY;
- BYTE ERASE;
- BYTE WRITE;
- CHIP ERASE;
- E/W INHIBIT.

Ordinary read operates with VPP at 4–6 V. Erase/write pulses VPP to 21 V. Chip erase also uses the elevated VPP and an additional output-enable condition.

Therefore:

> **electrical erasability ≠ ordinary read-service equivalence.**

The erase path is electrically controllable, but it remains a privileged operating condition.

### H/P — erase geometry is plural inside one device

The 2816 supports at least two deliberate erase scopes:

1. **byte erase** — one selected location is erased without affecting other bytes;
2. **chip erase** — all 2K bytes are returned to the erased `FF` state in one operation.

Electrical erasability therefore does not define one natural erase granularity. Even one product can expose both fine-grained and whole-array forgetting operations.

This is a useful control for later Flash history: `electrical erase` by itself does not explain why a later design adopts page/block-scale programming/erase geometry.

### H/P — byte rewriting remains erase-before-write

Intel's p. 4 says that to write a particular location, that byte must first be erased. The erase operation uses logic-high data inputs, CE selection, and a 21 V programming signal; once erased, the operation is repeated with the intended data for the write.

The device is therefore electrically alterable in-system, but not an unconstrained in-place overwrite medium.

At the bounded product level:

```text
new byte value
    requires
selected erase
    then
selected data write
```

This makes forgetting operationally constitutive of rewriting rather than merely an optional end-of-life action.

### H/P — the physical state can be electrically discharged by tunneling

US4203158A discloses a floating polysilicon gate completely surrounded by oxide. A local thin-oxide region supplies the carrier-transfer path.

The preferred mechanism uses a high electric field to tunnel electrons onto the floating gate for programming and reverses the transfer direction to tunnel electrons off the gate for erasure. A lower approximately +5 V condition is used to sense the resulting transistor state.

The important mechanism distinction is:

```text
insulation creates quiescent retention
    while
an intentionally applied field creates a controlled path across that retention barrier
```

Erasure is therefore not `retention switched off` in an abstract sense. It is an active physical operation that changes the conditions under which charge crosses the barrier that normally keeps the state.

### H/P — electrical alterability has a finite cycling budget

Intel's 2816 document says the device is designed for applications requiring up to `1 × 10^4` erase/write cycles per byte and emphasizes that cycling is byte independent.

This adds a new retention axis not needed by the bounded EPROM case:

> **nonvolatility can coexist with a finite budget for deliberate forgetting and rewriting.**

The product can retain a state without periodic refresh, yet repeated intentional state changes consume device lifetime.

The patent independently discusses finite thin-oxide program/erase cycling, but its preferred-embodiment range is not substituted for the 2816 product specification.

### H/P — the patent itself blocks a universal EEPROM-invention claim

US4203158A's prior-art section discusses electrically erasable integrated-circuit PROMs already in use, including silicon-nitride storage devices, as well as earlier tunneling and avalanche-erasure structures.

This case therefore does not claim `Intel invented EEPROM` or `FLOTOX was the first electrically erasable memory`. The claim is mechanism- and source-specific: Intel primary sources document one floating-gate electrical program/erase path and a named commercial device exposing byte/chip electrical erasure.

## Retained state and substrate

At the comparison level, the retained state is a nonvolatile floating-gate charge condition that changes the cell's electrical behavior sufficiently to distinguish stored values on later read.

The bounded retention relation is:

```text
stored charge
    +
insulating barrier
    ->
quiescent persistence without DRAM-style refresh
```

Case 12 adds the controlled exception:

```text
selected high-field electrical condition
    ->
carrier transport across the barrier
    ->
erased or newly programmed state
```

The same physical barrier participates in both durability and deliberately induced forgetting.

## Read / erase / write semantics

### Read

Read is the normal fast service path and uses the lower-voltage operating condition. The product's access time is hundreds of nanoseconds, far shorter than its erase/write interval.

### Byte erase

One selected byte is deliberately returned toward the erased all-ones condition through a millisecond-scale high-voltage operation. Other bytes remain unaffected under the specified regime.

### Byte write

The byte is first erased, then another high-voltage/timed operation establishes the intended data.

### Chip erase

A distinct control condition erases the entire 2K-byte array in approximately the same nominal 10 ms order as the byte operation.

This is not evidence that `larger erase is always as cheap as smaller erase` across technologies. It is a bounded product-specific operating fact.

## Addressability and forgetting geometry

The major transition from Case 11 is that erasure can now participate in electrical selection/control instead of requiring device-level radiation exposure.

But the result is not one-to-one identity between ordinary memory addressing and forgetting:

- byte erase is fine-grained and address-sensitive;
- chip erase deliberately ignores that fine granularity and resets the array together;
- erase/write additionally depends on VPP and mode/control sequencing absent from ordinary read.

Therefore:

```text
ordinary read addressability
    overlaps with
byte erase selection
    but does not exhaust
all erase authority / erase geometry
```

This is a stronger and more useful statement than `EEPROM has byte erase`.

## Engineering reconstruction

### Electrical control internalizes forgetting without making it ordinary

External UV exposure in the EPROM case placed erase authority partly outside the normal electrical interface. The 2816 moves deliberate erase into the system's electronics, but still requires a special voltage source, controller/timer behavior, mode selection, and a long operation relative to read.

Project comparison:

```text
external physical intervention
    ->
internal electrically orchestrated intervention
```

This is a migration of control locus, not disappearance of erase work.

### Fine-grained erase reduces one kind of collateral forgetting

A byte can be erased without changing adjacent bytes. Relative to device-wide optical erasure, this reduces the amount of otherwise-current state that must be disturbed when one location changes.

That is an engineering consequence, not a claim that Intel engineers used the phrase `collateral forgetting`.

### Erase-before-write makes forgetting part of update

For the bounded 2816, changing one byte is not just `write a new value`. The update path includes a reset operation before the new value is programmed.

This creates a bridge to later Flash Case 04, where erase geometry and out-of-place update force copying, invalidation, reclamation, and mapping work. The mechanisms are not yet the same: the 2816 can erase a byte directly, whereas later Flash deliberately changes the granularity/economics of erase.

### Endurance makes update history materially relevant even when value history is not retained

The device does not preserve a log of prior values, but repeated erase/write events affect the future reliability budget of the cell/byte.

This yields a useful distinction:

```text
application value history
    may be forgotten
while
physical stress history
    continues to matter to future retention/write capability
```

No claim is made that the 2816 exposes a readable per-byte wear counter. The point is an engineering consequence of finite cycling, not retained digital metadata.

## Failure and forgetting

Relevant failure classes include:

- **retention loss** — trapped charge no longer supports the intended state;
- **erase failure** — an intended reset operation does not sufficiently erase the target;
- **write/program failure** — the new state is not established after erase;
- **wrong-scope erasure** — control error causes a broader erase mode than intended;
- **high-voltage/timing failure** — the exceptional operation is not delivered within specification;
- **cycling wear** — repeated erase/write stress consumes a finite endurance budget;
- **read-path failure** — the state may remain physically present while selection/output circuitry fails to recover it, a boundary already established in the SRAM case.

These should not be collapsed into one generic `data loss` category.

## Functional analogy and anti-anachronism

Useful modern comparisons:

- `erase authority moves on-interface`;
- `erase geometry becomes address-sensitive`;
- `endurance-bounded forgetting`;
- `physical stress history outlives value history`.

These are analytical phrases, not historical Intel terms.

The case must not be rewritten in later Flash vocabulary. The 2816's `byte erase` is not `Flash sector erase`, and `E²PROM` is not evidence that FTL, garbage collection, wear leveling, or SSD-style controller semantics already existed in this device.

## Philosophical limit

Case 12 makes one conceptual point available for later synthesis: technical forgetting can become a deliberately callable operation without becoming frictionless or semantically equivalent to absence.

A byte can be made erasable `on demand`, but the demand is mediated by physical thresholds, voltage, time, selection, and finite endurance. What looks like greater command over forgetting is therefore simultaneously a new dependence on control infrastructure and medium lifetime.

This is a philosophical interpretation grounded by the engineering facts; Intel's datasheet and patent are not evidence that the designers formulated a theory of forgetting.

## Cross-case result

Case 11 established:

```text
electrical programmability != electrical erasability
```

Case 12 revises the relation rather than merely reversing it:

```text
electrical erasability
    !=
ordinary read equivalence
    !=
unlimited mutability
    !=
one fixed erase granularity
```

It also adds:

```text
erase can be part of the update path
    while
quiescent retention remains refresh-free
```

and:

```text
value-history forgetting
    !=
erasure of physical stress history
```

The last statement is an engineering reconstruction from finite cycling, not a claim that past values remain forensically recoverable.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Intel's 2816 is a 2K×8 E²PROM with HMOS-E FLOTOX cell design | H/P | Intel 2816 p. 1 |
| the product supports single-byte electrical erase/write and whole-chip erase | H/P | Intel 2816 pp. 1, 4–5 |
| erase/write uses a special 21 V VPP regime distinct from ordinary read | H/P | Intel 2816 pp. 1–2, 4–5 |
| a selected byte is erased before being rewritten in the bounded 2816 procedure | H/P | Intel 2816 p. 4 |
| erase/write is intended for in-system alteration of nonvolatile information | H/P | Intel 2816 pp. 1, 4 |
| product erase/write endurance is finite and specified up to `1 × 10^4` cycles per byte for the cited applications | H/P | Intel 2816 p. 4 |
| an Intel floating-gate design can program and erase by charge tunneling through thin oxide | H/P | US4203158A |
| byte erase and chip erase demonstrate more than one erase geometry in the same device | E, grounded in H/P | Intel 2816 pp. 1, 4–5 |
| electrically erasable means ordinary read, erase, and write are the same operation | X | contradicted by mode / voltage / timing separation |
| electrically erasable means unlimited rewriting | X | contradicted by finite cycling specification |
| byte erasability means no erase-before-write obligation | X | contradicted by Intel p. 4 procedure |
| US4203158A is proven to be the exact 2816 production transistor topology | X | source boundary not established |
| Intel/FLOTOX invented EEPROM generally | X | blocked by the patent's own prior-art discussion |
| the 2816 should be described with later Flash/FTL terminology | X | anachronistic and technically unsupported |

## Related repositories

Searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `EEPROM`, `FLOTOX`, `2816`, and floating-gate/Flash terms found no dedicated EEPROM case to reuse. Broader process/vendor history belongs there if developed later.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) supplies the anti-teleology guardrail: the present research sequence `EPROM → EEPROM → Flash` is an analytical lineage. It must not be presented as though engineers in 1981 were necessarily solving a pre-given historical problem called `how to become Flash`.

## Sources

1. Intel Corporation, _2816 — 16K (2K × 8) Electrically Erasable PROM_, AFN-01635B, 1981, surviving page-preserving scan: <https://ethw-images.s3.us-east-va.perf.cloud.ovh.us/ethw/e/ea/MEMO-data_2816.pdf>.
2. ETHW archival file record for the scan: <https://ethw.org/File:MEMO-data_2816.pdf>.
3. Dov Frohman-Bentchkowsky, Jerry Mar, George Perlegos, William S. Johnson, Intel Corp., US4203158A, _Electrically programmable and erasable MOS floating gate memory device employing tunneling and method of fabricating same_: <https://patents.google.com/patent/US4203158A/en>.

## Next bounded bridge

Do **not** generalize directly from byte-erasable EEPROM to all Flash. The next useful source slice is a period-primary early Flash design in which a coarser electrically erased unit is deliberate and consequential. It should ask:

- what erase unit is physically/control-wise selected;
- why coarse erase changes density/speed/circuit economy;
- whether rewrite becomes copy/reorganize/reclaim work rather than a local byte operation;
- how erase/program endurance enters management;
- which terminology the period source actually uses.

Only after that mechanism bridge should Case 04's already-grounded logical mapping / reclamation layer be used to connect device erase geometry to controller-mediated logical identity.
