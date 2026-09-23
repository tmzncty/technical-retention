# Evidence 146D — Micron Erase-Suspend Reset / Power-Down Integrity Boundary

## Scope

This note deepens Case 146 with a later named-product contract that makes an application-visible consequence of losing erase-suspend control state explicit.

The narrow question is:

> If a NOR Flash block erase has been suspended, what does a device reset or power-down mean for the suspended block's *data-integrity authority*?

The bounded answer in Micron's `M29W512GH` product documentation is unusually direct: a reset or power-down can abort an `ERASE SUSPEND` episode; after that boundary, **data integrity is not guaranteed and the suspended blocks should be erased again**. A related Micron P30-65nm product family separately documents that reset/power-down aborts block erase, that integrity cannot then be ensured, and that `BLANK CHECK` is specifically useful after power-loss-interrupted erase to determine whether a block is completely erased.

This closes a product-level consequence that the earlier Intel/TI evidence in Case 146 left deliberately open. It does **not** establish the exact cell-threshold distribution after interruption, and it must not be projected backward onto every 1990s device.

---

## Source identity and provenance

### P1 — Micron M29W512GH, Rev. E 9/15 / later Rev. F 5/18 — `H/P*`

- **Document:** *512Mb: 3V Embedded Parallel NOR Flash*
- **Manufacturer:** Micron Technology, Inc.
- **Product:** `M29W512GH70N3E`, `M29W512GH7AN6E`
- **Document identifier:** `m29w_512mb.pdf`; public copies expose Micron document identifier `09005aef85007385` for Rev. E and later Micron-controlled revision metadata in Rev. F.
- **Relevant revisions:** Rev. E, September 2015; Rev. F, May 2018.
- **Accessible manufacturer-document mirror:** https://www.mouser.com/datasheet/2/671/m29w_512mb-1283467.pdf
- **Evidence class:** `H/P*` — Micron-authored product documentation preserved by a distributor/archive rather than currently served from Micron's own origin.

The later Rev. F copy preserves a revision history listing Rev. E `9/15` and retains the same erase-suspend reset/power-down rule. This note therefore uses the named product contract, not the mirror crawl date, as the historical anchor.

### P2 — Micron P30-65nm MLC, Rev. C 2/15 — `H/P*`

- **Document:** *512Mb, 1Gb, 2Gb: P30-65nm*
- **Manufacturer:** Micron Technology, Inc.
- **Revision:** Rev. C, February 2015
- **PDF identifier:** `09005aef845667b3`
- **Accessible archival copy:** https://www.micron-electronic.com/pdf-c9/pc28f512p30efb.pdf
- **Evidence class:** `H/P*` — Micron-authored product documentation preserved by a third-party archive.

This second family is not used to claim implementation identity with M29W. It is used as an independent Micron named-product witness for the distinction between interrupted erase, integrity uncertainty, and post-interruption qualification by `BLANK CHECK`.

---

## Historical record

### H/P* — M29W512GH explicitly separates suspend from reset/power-down abort

The M29W512GH product advertises program/erase suspend and resume. During an `ERASE SUSPEND` episode, the controller suspends block erase, permits read/program activity in blocks that are not suspended, and later accepts `ERASE RESUME (30h)` after the device is returned to read-array mode.

The same command section then gives a different transition for reset or power-down:

```text
active block erase
    -> ERASE SUSPEND (B0h)
    -> powered suspended erase
    -> ERASE RESUME (30h)
    -> controller continues erase
```

but:

```text
powered suspended erase
    -> device reset OR power-down
    -> suspend episode aborted
    -> data integrity not guaranteed
    -> suspended blocks should be erased again
```

That is direct product documentation, not an inference from generic Flash physics.

### H/P* — ordinary block erase has the same integrity-warning shape

The same M29W documentation separately says a block erase aborted by reset or power-down does not carry a data-integrity guarantee and that the aborted blocks should be erased again.

This matters because it prevents a misleading reading in which only the *software-visible suspend mode* is lost while the target block is somehow known-good. The manufacturer treats interruption of the erase episode as an integrity boundary for the affected block.

### H/P* — program suspend shows that the rule is operation-scoped, not merely a block-erasure vocabulary accident

The M29W product also says a reset or power-down can abort a `PROGRAM SUSPEND` episode; in that case data integrity cannot be ensured and the affected words/bytes should be reprogrammed.

This note does not merge program and erase into one physical mechanism. The narrower lesson is that Micron's command contract consistently distinguishes:

```text
powered suspend/resume continuity
    !=
reset/power-down interruption
```

and associates the latter with loss of integrity assurance over the operation's target region.

### H/P* — P30-65nm makes post-power-loss qualification explicit

Micron's 2015 P30-65nm MLC documentation says a block erase aborted by reset or power-down does not carry an integrity guarantee and recommends erasing the aborted block again.

Immediately afterward, the datasheet defines `BLANK CHECK` as a separate operation that determines whether a block is completely erased. It specifically identifies power-loss-interrupted block erase as a use case for `BLANK CHECK`.

The sequence therefore exposes two distinct post-interruption strategies:

```text
power-loss-interrupted erase
    -> integrity of target not assumed
    -> either re-establish erased state by BLOCK ERASE
       or test the relevant postcondition with BLANK CHECK
```

A successful `BLANK CHECK` is evidence for the *erased-state predicate*. It is not restoration of the pre-erase payload.

### H/P* — suspend itself remains a checkpointed powered operation

The P30 documentation says `ERASE SUSPEND` asks the device to suspend the erase algorithm at predetermined points and reports completion through status-register bits. That remains consistent with the older Case 146 sources:

```text
suspend request
    !=
safe suspended state at the same instant
```

The later Micron evidence adds the stronger post-interruption consequence; it does not erase the earlier distinction between request, admitted suspended state, and eventual resume.

---

## Engineering reconstruction

### 1. Operation-control state and payload-integrity authority are distinct state classes

Case 146 already distinguishes array/cell state from operation-control state. The Micron evidence now adds a third relation that should not be collapsed into either one:

```text
C = physical cell / payload state
O = operation-control state
A = integrity authority: whether software is entitled to treat the target as satisfying a known postcondition
```

During a normal powered suspend:

```text
O = suspended/resumable
A = target erase not yet complete
```

After reset/power-down abort:

```text
O = suspended/resumable relation retired
A = target integrity not guaranteed
```

The cells remain physically present, but their mere nonvolatility does not recreate the lost operation relation or establish a trusted logical state.

### 2. `operation no longer pending != operation completed successfully`

A reset may return a device to an ordinary command/read mode while simultaneously destroying the continuation contract for the suspended erase.

Therefore:

```text
controller ready for new commands
    !=
interrupted target is known-good
```

and:

```text
pending-operation relation retired
    !=
erase postcondition satisfied
```

This is a stronger product-level boundary than the generic statement that Flash control state can be volatile.

### 3. `nonvolatile cells != erase atomicity`

NOR Flash is nonvolatile at rest, but an erase is a multi-step internally timed operation. Power loss does not need to make the medium volatile in order to leave the target without a trustworthy completed-state predicate.

The safe relation is:

```text
nonvolatile substrate
    + multi-step destructive update
    + interruption
    -> physical state may persist
       while logical/integrity qualification is lost
```

This is not a claim that every interrupted cell is corrupt. The manufacturer's wording is weaker and more precise: integrity **cannot be ensured**.

### 4. Re-erasing is re-establishment, not rollback

Micron's recommendation to erase the suspended/aborted block again should not be described as recovering the old data.

It establishes a new known erased state:

```text
unknown / unqualified post-interruption target
    -- successful erase -->
known erased target
```

not:

```text
unknown target
    -> restore pre-erase payload
```

The old payload may already have been partially destroyed by the original erase episode.

### 5. Blank Check is evidence, not mutation equivalence

P30's `BLANK CHECK` provides a useful separation between **qualification** and **repair/reinitialization**:

```text
BLOCK ERASE
    = state-changing maintenance operation

BLANK CHECK
    = observation/qualification of whether erased-state predicate already holds
```

Thus:

```text
verified blank
    !=
blank because a new erase was necessarily performed
```

and:

```text
operation completion status lost
    !=
impossible to re-establish confidence by later observation
```

### 6. Reset semantics must be typed by state class

This slice is a concrete Case 146 counterpart to the repository's broader reset-state discipline.

For this named product:

```text
reset
    -> can retire erase-suspend continuation state
    -> can leave target integrity unqualified
```

That does not imply all device state is cleared by reset. Other cases in the repository show state classes that survive documented resets. The correct unit of comparison is:

```text
state class × event class × interface contract
```

not the bare word `reset`.

---

## Transition table

| Event / state | Pending erase relation | Ordinary target-payload authority | Integrity consequence | Documented next step |
|---|---|---|---|---|
| Active erase | live | not ordinary completed-state data | erase incomplete | wait, suspend, or complete |
| Successful Erase Suspend | live and resumable | target remains outside ordinary completed-state contract | pending state retained | Resume may continue erase |
| Erase Resume | live and executing again | still incomplete until normal completion | normal erase contract resumes | wait for completion/status |
| Reset while suspended | resumable suspend relation no longer relied upon | not guaranteed | integrity cannot be ensured | erase suspended blocks again |
| Power-down while suspended | resumable suspend relation no longer relied upon | not guaranteed | integrity cannot be ensured | erase suspended blocks again |
| Power-loss-interrupted erase, P30 | operation interrupted | not assumed complete | integrity cannot be ensured | re-erase or use Blank Check to test erased-state predicate |
| Successful Blank Check, P30 | no suspended continuation implied | block qualifies as completely erased | erased-state predicate re-established by observation | proceed under blank-block contract |

The table is an engineering reconstruction of manufacturer contracts, not a claim that all listed devices share one internal state machine.

---

## Cross-case comparison — functional only

### Case 146 earlier Intel/TI witnesses

Earlier Case 146 evidence already established:

- powered suspend/resume is distinct from abort/reset/power-control transitions;
- a resume relation can preserve the pending operation without preserving every internal microstate;
- the exact cell-level result of an interrupted erase remained unproven in those named sources.

The Micron evidence closes only the later product-level consequence:

```text
after reset/power-down interruption
    -> manufacturer does not authorize assuming target integrity
```

It does **not** retroactively prove how the Intel 28F008SA, AMD Am29F040, or TI TMS29F040 physically behaved under every interruption.

### Case 04 / Case 134 — relocation and payload qualification

Flash copy/migration cases distinguish a successfully executed placement/update primitive from independent payload-integrity qualification.

Case 146 now supplies a related but different relation:

```text
control episode ended
    !=
target state qualified
```

This is a functional analogy only. Copy-back and erase suspend are not the same protocol or lineage.

### Case 85 — Micron read-retry reset survival

Case 85 shows a Micron NAND feature-state class that survives specified reset commands while active operations can be aborted. Case 146 shows a different product/interface where erase-suspend continuation is not granted across reset/power-down.

Together they support a methodological rule, not a product genealogy:

```text
same event word: reset
    !=
same consequence for every retained state class
```

### Synthesis 26 — typed reset persistence boundaries

This slice is another concrete witness for the synthesis rule that `survives reset` is not a scalar durability grade. Here the relevant state is an erase-suspend continuation relation plus the target's integrity authority. The correct statement is event- and state-specific.

---

## Historical record vs reconstruction vs analogy vs interpretation

### Historical record

The manufacturer documents directly establish that:

- M29W supports erase suspend/resume;
- reset or power-down can abort a suspended erase;
- after that abort, target-block data integrity is not guaranteed and Micron recommends erasing the suspended blocks again;
- P30 block erase interrupted by reset/power-down likewise loses an integrity guarantee;
- P30 `BLANK CHECK` can determine whether a block is completely erased and is specifically useful after power-loss-interrupted erase.

### Engineering reconstruction

The project reconstructs from those facts that:

- payload/cell state, pending-operation control state, and integrity authority are distinct;
- losing the resumable operation relation can force requalification even though the medium is physically nonvolatile;
- re-erase and blank-check are different ways of re-establishing a trustworthy postcondition.

### Functional analogy

Comparisons to copy-back integrity, read-retry reset survival, persistent transaction records, or distributed-maintenance checkpoints are relation-level analogies only.

### Philosophical interpretation

The broader interpretation is that material persistence alone does not confer current authoritative status. A technical object can remain physically present while the evidence that authorized a particular reading of that object has expired.

That interpretation is **not** Micron's historical vocabulary and is not evidence about designer intent.

---

## Explicit non-claims

This note does **not** claim:

1. every reset or power-down actually corrupts every bit in a suspended block;
2. Micron specifies the exact threshold-voltage distribution or fraction of changed cells after interruption;
3. all NOR Flash families have the same reset/power-down behavior;
4. the 2015/2018 Micron contract can be projected backward onto 1990s Intel, AMD, TI, or Macronix devices;
5. `ERASE SUSPEND` is a crash-consistent transaction mechanism;
6. re-erasing an affected block restores the pre-erase payload;
7. `BLANK CHECK` repairs anything by itself;
8. a successful blank check proves anything beyond the documented erased-state predicate;
9. Micron M29W and P30 share identical internal controllers because their external contracts resemble one another;
10. a distributor/archive host is the historical origin of the Micron-authored datasheet.

---

## Impact on Case 146

This slice closes one previously open product-level boundary:

```text
old bounded statement:
    power/reset can destroy suspended-operation continuation,
    but exact target consequence may remain unspecified

new later named-product statement:
    Micron explicitly says reset/power-down-aborted suspend
    leaves target integrity unguaranteed and calls for re-erase
```

Case 146 should remain **`grounded`**. The new evidence deepens the reset/power boundary but does not justify a maturity promotion because the implementation-level physical trajectory and cross-vendor chronology remain intentionally bounded.

---

## Remaining research debt

High-value next steps are now narrower:

1. find a 1990s or early-2000s named product that explicitly states the target-data consequence of power loss *while already in erase-suspend mode*;
2. find production test/application material that power-cuts at controlled erase/suspend phases and reports block/readback behavior;
3. separate hardware reset, software reset/read-reset, VCC collapse, and VPP loss where a product documents them independently;
4. locate threshold-distribution or disturb data for interrupted NOR erase without importing NAND assumptions;
5. trace whether any family introduced persistent/restartable nonvolatile operation checkpoints rather than powered-only suspend state;
6. compare blank-check/re-erase recovery guidance across vendor generations without treating similar commands as shared genealogy.

Until those are found, the safe relation is:

```text
powered suspend/resume continuity
    !=
reset/power-down survival

nonvolatile cell state
    !=
trusted completed-operation state

operation-control loss
    -> may require requalification or re-establishment
```
