# Case 146 Evidence Index — Flash Erase Suspend / Pending-Operation State

## Status

**Case status:** `grounded`

**Canonical case:** [`../cases/146-flash-erase-suspend-pending-operation-state.md`](../cases/146-flash-erase-suspend-pending-operation-state.md)

This index is the navigation layer for the current Case 146 evidence packet. It keeps chronology, named-product behavior, engineering reconstruction, and later comparison layers separate. It does not promote the case beyond `grounded`.

---

## Research question

Case 146 asks:

> When a long Flash erase is suspended so another access can proceed, what relation must remain live for a later Resume to continue the same pending erase, and what happens when reset/power/power-control events retire that relation?

The mature bounded model is now:

```text
array / cell state
    !=
pending-operation control state
    !=
host-visible admission/status state
    !=
integrity authority over the target
```

A Flash array can be nonvolatile while the continuation relation of an in-progress erase is only powered state. The latest Micron deepening further shows that loss of that continuation relation can also invalidate the manufacturer's integrity guarantee for the target block.

---

## Evidence chain

### 146A — Intel / AMD 1991–1998 erase-suspend grounding

[`146-intel-amd-1991-1998-flash-erase-suspend-grounding.md`](146-intel-amd-1991-1998-flash-erase-suspend-grounding.md)

**Role:** foundational historical/product grounding.

**What it establishes:**

- Intel's public patent line supplies an early documented erase-suspend problem/solution family, with 1991 priority kept distinct from 1994 public publication/grant;
- AMD's 1996 Am29F040 provides a named-product erase-suspend/read/resume contract;
- later Am29F040B and Macronix material expose capability changes and checkpoint-style suspension boundaries;
- suspend is a retained pending-operation relation, not rollback or erase completion.

**What it does not establish:**

- exact cross-vendor circuitry;
- power-cycle-persistent erase checkpoints;
- exact cell state after interrupted erase;
- first invention or universal genealogy.

### 146B — TI TMS29F040 microstate / power-transition deepening

[`146-ti-tms29f040-erase-suspend-microstate-power-deepening.md`](146-ti-tms29f040-erase-suspend-microstate-power-deepening.md)

**Role:** named-product counterexample to exact-microstate preservation.

**What it establishes:**

- TI suspends erase at predetermined breakpoints;
- Resume continues the same pending erase workflow;
- the internal pulse counter can nevertheless reset to zero across suspend/resume;
- low-VCC/power-up transitions return command/control behavior to read mode rather than documenting persistence of the suspended operation.

**Key relation:**

```text
same pending erase obligation
    !=
bit-for-bit preservation of every controller progress variable
```

### 146C — Intel 28F008SA suspend / abort / power-control boundary

[`146-intel-28f008sa-suspend-abort-power-boundary-deepening.md`](146-intel-28f008sa-suspend-abort-power-boundary-deepening.md)

**Role:** named Intel product witness for powered continuation versus abort.

**What it establishes:**

- the 28F008SA WSM can suspend a block erase and later resume it with `D0H`;
- the target block is not thereby restored to authoritative old data;
- maintained electrical/control conditions, including `VPP`, are part of the continuation contract;
- reset/power-control abort is followed by a fresh erase setup/confirm path rather than ordinary Resume.

**Key relation:**

```text
powered suspend -> Resume continues pending WSM erase

reset/power-control abort -> fresh erase sequence required
```

### 146D — Micron 2015–2018 reset/power-down integrity boundary

[`146-micron-2015-2018-erase-suspend-reset-integrity-boundary-deepening.md`](146-micron-2015-2018-erase-suspend-reset-integrity-boundary-deepening.md)

**Role:** closes the later named-product target-integrity consequence after loss of suspend continuity.

**What it establishes:**

- Micron M29W512GH explicitly says reset or power-down can abort an `ERASE SUSPEND` episode;
- after that boundary, data integrity cannot be ensured and the suspended blocks should be erased again;
- Micron P30-65nm separately documents the same integrity warning for interrupted block erase;
- P30 `BLANK CHECK` is specifically useful after power-loss-interrupted erase and can re-establish evidence that the block is completely erased.

**Key relations:**

```text
operation-control relation retired
    !=
erase completed successfully
```

```text
nonvolatile physical state
    !=
trusted logical / integrity state
```

```text
re-erase
    = re-establish a known erased state
    != restore pre-erase payload
```

---

## Chronology discipline

The current evidence chain should be read in layers rather than as one continuous genealogy.

```text
1991  Intel patent priority
1994  Intel patent public publication/grant
1995  Intel 28F008SA named-product datasheet
1996  Intel AP-364 named-product WSM detail
1996  AMD Am29F040 named-product suspend/read/resume contract
1996/1998  TI TMS29F040 named-product microstate/power contract
1996-priority/1998-public  Macronix multiple-checkpoint refinement
2015  Micron P30-65nm named-product interrupted-erase / Blank Check contract
2015  Micron M29W512GH Rev. E named-product suspend-abort integrity contract
2018  Micron M29W512GH Rev. F retains the same rule and revision history
```

This sequence **must not** be read as proof that later Micron devices descend from the exact Intel patent implementation or that the 1990s products shared one state machine.

The chronology is used to show how public product contracts make different boundaries explicit over time.

---

## Current engineering model

### State classes

Case 146 now distinguishes at least four state classes:

1. **array/cell state** — physical floating-gate / threshold state in the target and unaffected blocks;
2. **pending-operation control state** — whether erase is active, suspended, resumable, complete, or aborted;
3. **host-visible status/admission state** — which commands/reads are legal and what status means;
4. **integrity authority** — whether the target can be treated as satisfying a known completed-state predicate.

The critical rule is:

```text
physical persistence
    !=
control-state persistence
    !=
integrity qualification
```

### Event classes

The evidence also requires typed events:

- ordinary powered erase progression;
- suspend request;
- admitted suspended state;
- resume;
- reset/read-reset where product-defined;
- hardware reset / reset-powerdown pin where product-defined;
- VPP loss where product-defined;
- VCC loss / power-down;
- power-up / return to normal command mode.

Do not collapse these into a single scalar `reset` or `power event`.

### Transition model

```text
known pre-operation block state
    ↓
ERASE admitted
    ↓
internal destructive update / verify sequence
    ↓
SUSPEND request
    ↓
safe suspended checkpoint reached
    ↓
pending erase relation retained
    + other-operation admission changes
    ↓
RESUME
    ↓
normal completion
    ↓
known erased-state contract
```

A different path is:

```text
safe suspended checkpoint
    ↓
reset / power-down / product-specific abort boundary
    ↓
continuation relation no longer authorized
    ↓
target integrity may be unqualified
    ↓
re-erase OR product-specific verification/requalification
```

The second path is now product-level grounded for the later Micron witness. It is **not** retroactively assigned to every earlier device.

---

## Evidence-strength matrix

| Question | Current answer | Strongest evidence | Confidence boundary |
|---|---|---|---|
| Can a sector/block erase be suspended and later resumed? | Yes, in multiple named products | Intel/AMD/TI/Micron product docs | product-specific |
| Is suspend the same as erase completion? | No | named command/state behavior | strong |
| Is suspend rollback to pre-erase payload? | No evidence for rollback; target may be unknown/non-authoritative | Intel/TI/Micron product docs | strong negative boundary |
| Must every internal progress variable survive suspend? | No | TI pulse-counter reset | named-product direct evidence |
| Does powered suspend necessarily survive power loss? | No such general contract; several products expose an abort/power boundary | Intel/TI/Micron product docs | strong product-specific boundary |
| Can reset/power-down of a suspended erase leave target integrity unguaranteed? | Yes for Micron M29W512GH | Micron M29W datasheet | direct named-product evidence |
| Does an interrupted block necessarily contain corrupt bits? | Not proven | manufacturer says integrity cannot be ensured | intentionally weaker claim |
| Can erased-state confidence be re-established by observation rather than immediately re-erasing? | P30 `BLANK CHECK` can establish whether a block is completely erased | Micron P30 datasheet | product-specific |
| Is exact cell-level interruption state known? | No | not exposed by current product docs | open research debt |
| Is there a universal cross-vendor suspend checkpoint representation? | No evidence | TI counter behavior already warns against this | explicit non-claim |

---

## Cross-case routing

### Case 13 — early Flash erase geometry

Case 13 supplies coarse-erase physical/architectural background. Case 146 should not duplicate that history. Its object is the **retained operation relation above erase geometry**.

### Case 04 / Case 134 — mapping / Copy-Back integrity

Use only for a relation-level comparison:

```text
an operation primitive executed
    !=
payload/integrity predicate independently established
```

Do not infer common protocol or genealogy.

### Case 15 / SSD power-loss protection

Case 15 studies a device/controller durability contract with explicit failure handling. Case 146's earlier NOR products instead expose a pending operation whose immediate continuation can depend on powered control state. The comparison is useful only for differentiating payload nonvolatility from operation-control durability.

### Case 85 — read-retry reset survival

Case 85 is a useful opposite-direction state-class example: a documented feature setting can survive resets that abort other operation state. This reinforces typed event/state reasoning and should not be interpreted as a Micron-wide rule.

### Synthesis 26 — maintenance-control persistence horizons

Case 146D is now another named-product witness for:

```text
state class × event class × interface layer
```

rather than a one-dimensional `survives reset` ladder.

### `computing-archaeology`

A fresh repository search found no existing dedicated `M29W` / Micron erase-suspend packet in `tmzncty/computing-archaeology`. Broad parallel-NOR history should still route there if developed later; this Case 146 index keeps only retention-specific operation-state and integrity boundaries.

---

## Historical record / reconstruction / analogy / interpretation guardrail

### Historical record

Safe historical statements are limited to what the cited patent/product documents actually establish: commands, modes, status, timing, reset/power behavior, and manufacturer recovery guidance.

### Engineering reconstruction

Project terms such as `pending-operation identity`, `continuation authority`, `integrity authority`, and `operation-state retention` are analytical vocabulary. They are useful because they separate relations that the product behavior demonstrates, but they are not attributed to historical engineers unless a source uses them.

### Functional analogy

Comparisons to journaling, checkpoint/restart, array rebuild progress, read-retry feature state, or Copy-Back are structural comparisons only. They do not establish implementation descent.

### Philosophical interpretation

The broad interpretation — that a physically persistent object can lose the evidence that makes one reading of it authoritative — belongs to the project synthesis layer. It is not a historical claim about vendor intent.

---

## Current non-claims

Case 146 currently does **not** claim:

- first invention of erase suspend;
- one continuous Intel→AMD→TI→Micron genealogy;
- one universal internal checkpoint representation;
- crash-persistent suspend across power cycles;
- exact analog/threshold state after interruption;
- corruption of every bit after reset/power-down;
- re-erase as restoration of old payload;
- blank check as a repair operation;
- identical semantics for reset, read-reset, RST#, VPP loss, VCC loss, and power-down;
- identical semantics across NOR and NAND.

---

## Remaining research debt

Highest-value remaining slices are:

1. **phase-controlled fault injection:** production/app-note evidence for cutting VCC/VPP at known erase/suspend phases and reading back the target;
2. **1990s target-integrity wording:** find an earlier named product that states target-data consequences after reset/power loss during suspend as explicitly as later Micron documentation;
3. **event decomposition:** separate software reset/read-reset, hardware reset pin, VPP loss, brownout, and full power loss wherever product documentation permits;
4. **physical-state evidence:** threshold-distribution or erase-verify behavior after interruption, without importing NAND assumptions;
5. **persistent maintenance checkpoints:** look for later NOR/NVM designs that intentionally persist an in-progress operation across power loss rather than merely allowing powered suspend/resume;
6. **verification/reinitialization comparison:** compare blank-check, re-erase, verify, and bad-block/error-handling guidance as distinct ways of re-establishing authority.

Until those are closed, the preferred compact model is:

```text
powered suspend
    = retained pending-operation relation

resume
    = continuation under that retained relation

reset / power-down
    may retire continuation state
    and may invalidate target integrity authority

nonvolatile medium
    !=
atomic in-progress update
    !=
persistent operation checkpoint
```
