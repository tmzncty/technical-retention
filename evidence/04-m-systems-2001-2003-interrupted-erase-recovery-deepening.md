# Evidence 04D — M-Systems 2001–2003 interrupted-erase recovery and retained completion evidence

## Status

**`bounded deepening complete`** — this record deepens Case 04 only at the power-loss boundary around **Flash erase completion and later reuse authority**.

Canonical case: [`../cases/04-flash-virtual-mapping-logical-identity.md`](../cases/04-flash-virtual-mapping-logical-identity.md)

This closes a narrow part of the canonical debt `add power-failure / atomicity evidence before making claims about mapping-update crash consistency`:

- it supplies primary M-Systems evidence that unexpected power loss during a destructive Flash erase can leave a unit in a state that must **not** simply be treated as erased;
- it supplies concrete historical mechanisms that retain `erase pending` / `erase completed` evidence across the power boundary and re-erase uncertain units before normal use;
- it does **not** prove atomic logical-to-physical map updates in the 1993 Ban system;
- it does **not** prove that every TrueFFS release or every M-Systems product used the same marker/register embodiment.

The bounded question is:

> when a maintenance operation is intended to convert a Flash unit into reusable erased space, what must remain knowable after sudden power loss so that a partially completed destructive operation is not mistaken for successful completion?

The inspected M-Systems record gives a clear answer: retain enough completion-history evidence to identify an erase whose success is not proven, then repeat or verify the destructive maintenance operation before granting reuse authority.

---

## Why this slice matters

Case 04 already establishes a central mapped-Flash relation:

```text
stable logical identity
    can survive
changing physical embodiment
```

and it already establishes that reclamation is not merely deletion. Active blocks are first preserved elsewhere; a larger unit is then erased; only afterward can that physical region re-enter the free/reusable pool.

That leaves a failure-window question.

Suppose power disappears **during the erase itself**. The controller may later find a region whose bits look partly erased, whose previous erase operation was initiated, and whose execution microstate no longer exists. The dangerous shortcut is:

```text
erase was requested
    -> unit may now be treated as erased
```

The M-Systems material below explicitly rejects that shortcut.

The historical mechanisms instead preserve evidence about the operation boundary:

```text
erase intended / pending
    -> destructive operation begins
    -> power may fail
    -> restart inspects retained evidence
    -> completion not proven
    -> erase again / verify
    -> only then return to ordinary use
```

This creates a retention seam not centered on preserving the old payload. The retained object is partly **knowledge that destructive maintenance has not yet earned completion authority**.

---

## Evidence classes used here

- `H/P` — primary patent / patent-application record from the historical actor or assignee;
- `E` — engineering reconstruction from relations stated in the source;
- `A` — bounded functional analogy to another repository case;
- `I` — project-level interpretation;
- `X` — rejected shortcut / stop condition.

No project term such as `reuse authority`, `negative completion evidence`, or `maintenance obligation` is attributed to M-Systems historical vocabulary.

---

## Source ledger

### S1 — M-Systems, US 6,977,847 / US 2003/0099134, “Detecting partially erased units in flash devices” (`H/P`)

- Inventors: Menahem Lasser; Meir Avraham.
- Original assignee: M-Systems Flash Disk Pioneers Ltd.
- Provisional priority: **23 November 2001**.
- U.S. application filed: **18 November 2002**.
- U.S. application publication: **29 May 2003**, `US20030099134A1`.
- Patent grant: **20 December 2005**, `US6977847B2`.
- Google Patents record: <https://patents.google.com/patent/US6977847B2/en>
- Application mirror with claims / description: <https://uspto.report/patent/app/20030099134>

Why this is primary evidence:

- the document is an M-Systems patent-family record;
- it explicitly addresses unexpected power loss during Flash erase;
- it explicitly links itself to the earlier M-Systems Flash-management patents `US5404485` and `US5937425`;
- it describes both older TrueFFS erase-mark practice and newer embodiments designed for devices whose partial-page-programming constraints make that older marker strategy unsuitable.

Important custody guardrail:

The patent's statements about earlier TrueFFS practice are **period first-party historical testimony** from M-Systems, not an independently audited release history. This file therefore records them as such and does not invent an exact first-shipping date.

### S2 — M-Systems, US 6,988,175 / US 2004/0268063, “Flash memory management method that is resistant to data corruption by power loss” (`H/P`)

- Inventor: Menahem Lasser.
- Original assignee: M-Systems Flash Disk Pioneers Ltd.
- Filing / priority: **30 June 2003**.
- U.S. application publication: **30 December 2004**, `US20040268063A1`.
- Patent grant: **17 January 2006**, `US6988175B2`.
- Google Patents record: <https://patents.google.com/patent/US6988175B2/en>

This later same-assignee source is used only as a bounded corroborating witness for the power-loss problem model. It says that conventional prior Flash-management systems, including M-Systems TrueFFS, could focus recovery on the page or block being modified when corruption remained local to the interrupted operation. It lists historical approaches including:

- retaining a pointer to the target page/block plus validity flags;
- constraining candidate write locations and treating those locations as suspect after power-up;
- applying a validity test before trusting possibly interrupted data.

The patent then motivates a different method for MLC devices where corruption from interrupted programming may not remain confined to the page being directly written.

S2 is **not** used to claim that the exact S1 erase-pending mechanism was universal TrueFFS behavior.

### S3 — Amir Ban / M-Systems, US 5,404,485, “Flash file system” (`H/P`, canonical anchor)

- Filed: **8 March 1993**.
- Granted: **4 April 1995**.
- Google Patents: <https://patents.google.com/patent/US5404485A/en>

S3 remains the canonical Case-04 anchor for virtual mapping, out-of-place replacement, transfer-unit reclamation, and reconstruction of volatile mapping support from nonvolatile Flash state.

This evidence packet does not rewrite S3 as if its 1993 disclosure already contained every later S1/S2 power-loss mechanism.

The historically safe relation is:

```text
same assignee / later explicit reference to earlier patents
    !=
proof that the later mechanism existed unchanged in 1993
```

---

## Historical / implementation record

### 1. S1 explicitly frames unexpected power loss as an integrity problem for Flash-management systems

S1 opens by tying the problem to Flash-management systems including the earlier M-Systems patents `US5404485` and `US5937425`.

It says, in substance, that such systems must preserve integrity despite power loss that can occur:

- during a Flash-device operation; or
- during software routines that maintain the data structures needed for coherent interpretation of Flash contents.

This is stronger than a generic modern observation that “Flash needs crash consistency.” It is a period M-Systems record saying that power-loss interruption is part of the engineering problem space around its own Flash-management lineage.

It still does **not** tell us that every update in S3 is atomic.

### 2. Interrupted erase can leave a unit neither safely old nor safely erased

S1 emphasizes erase duration and the possibility that power disappears while an erase is in progress.

The resulting unit can be partially erased:

- some bits may have reached the erased target state;
- others may not;
- the unit therefore cannot safely be assumed ready for programming.

The source additionally warns that a naïve full read is not necessarily sufficient to certify successful erasure because intermediate cell states can be unreliable.

The historical boundary is therefore:

```text
erase command started
    !=
erase operation completed
    !=
unit proven safe for reuse
```

### 3. The older TrueFFS erase-mark method retained a post-erase completion witness

S1 describes a prior-art method it says had been used for years in the TrueFFS family.

The pattern is:

1. after a successful erase, write a special `erase mark` into a predefined location in the erased unit;
2. before a later erase, destroy that mark;
3. when allocating a supposedly free unit, check whether the mark exists;
4. if the mark is absent, treat the earlier erase as potentially interrupted and erase the unit again.

This makes the marker an operation-history witness, not user payload.

The marker's useful meaning is asymmetric:

```text
erase mark present
    -> this mechanism has evidence of a completed erase

erase mark absent
    -> do not infer completion; re-erase before use
```

The second line is especially important. Absence is not interpreted as proof of one exact failure microstate. It is sufficient evidence that **completion is not proven**.

### 4. The older erase-mark method depends on a write-geometry capability

S1 says the erase-mark approach requires multiple writes to some Flash pages between erase cycles.

It names this capability as Partial Page Programming (`PPP`) and explains that some forthcoming devices were expected to allow only one page programming operation before erase (`PPP=1`).

That device-geometry change invalidates an otherwise useful recovery representation.

Thus:

```text
recovery invariant
    may remain desirable
while
marker embodiment
    becomes incompatible with a new programming geometry
```

This is a useful Case-04 continuation of the repository's general warning that a retained relation and its physical representation are different things.

### 5. S1 therefore moves completion evidence outside the erase target in several embodiments

The newer embodiments do not rely on repeatedly modifying the target unit's erase-mark page.

S1 describes multiple alternatives, including:

- a separate nonvolatile flag register for `erase pending` plus a nonvolatile register holding the affected unit number;
- separate Flash locations for `erase pending`, unit identity, and `erase completed` information;
- hardware/firmware support that records the unit being erased when a power-loss detector fires.

The common relation is:

```text
uncertain target unit
    +
retained evidence outside or separately represented from that target
    ->
restart can identify what must not yet be trusted
```

### 6. One embodiment records `erase pending` before the destructive operation begins

A central S1 sequence is:

```text
set erase-pending flag
store / associate target unit identity
        |
        v
issue erase
        |
        +---- power failure may occur here
        |
        v
successful completion
        |
        v
clear pending flag or record completion
```

After power-up, a surviving pending indication identifies an erase that cannot be assumed complete.

The recovery action is to erase the named unit again, verify that erase, and only then clear the pending state / proceed with normal operation.

This is effectively a write-ahead maintenance obligation, though **`write-ahead maintenance obligation` is repository vocabulary, not M-Systems terminology**.

### 7. Another embodiment uses paired pending / completed evidence

S1 also describes software-managed locations containing:

- an `erase pending` flag;
- the target unit number;
- a separate `erase completed` flag.

The power-up logic checks whether each pending record has a matching completion record.

If a pending record lacks completion, the target unit is erased and verified again before completion is recorded.

This makes the distinction explicit:

```text
operation intent retained
    !=
operation completion retained
```

and:

```text
pending without completion
    -> recovery obligation survives restart
```

### 8. A further embodiment records the threatened operation at power-loss detection time

S1 also describes a device with:

- a power sensor;
- reserve energy;
- nonvolatile flag registers;
- nonvolatile unit-number registers.

If power loss is detected while erasure is active, the control logic records which units are being erased before remaining energy disappears. On the next power-up those units are erased again.

This embodiment is structurally different from pre-recording every erase.

Therefore S1 should not be reduced to one universal implementation recipe.

The common invariant is narrower:

> enough information survives the boundary to prevent an interrupted destructive operation from being mistaken for proven completion.

### 9. S1's recovery path prefers replay over reconstructing the exact interrupted microstate

None of the inspected S1 recovery paths needs to preserve:

- the exact erase pulse count;
- threshold-voltage trajectories of every cell;
- which individual bits completed first;
- the controller's full pre-failure execution state.

Instead the mechanism retains a much coarser fact:

```text
this unit's erase was pending / completion was not established
```

and converts that fact into a safe restart action:

```text
re-erase + verify
```

This is an engineering reconstruction from the source's control relation, not a claim about the patent's hidden circuitry.

### 10. S2 generalizes the restart problem beyond erase without proving one universal recovery mechanism

The 2003-filed S2 patent says that when power-loss corruption is local to the currently modified page/block, prior Flash-management systems can focus on that last target after reboot.

It lists multiple strategies:

- remember a target pointer and validity flags;
- constrain the set of locations that could have been in flight;
- treat candidate locations as suspect;
- run a validity test before trusting them.

This corroborates the broader principle:

```text
restart recovery does not require preserving all execution state
```

if the system can instead preserve or reconstruct a bounded **suspect set**.

But S2's purpose is to address newer MLC behavior where an interrupted write can disturb a wider risk zone. It therefore also blocks an overgeneralization:

```text
interrupted operation corrupts only the directly targeted page
```

is not a timeless NAND rule.

---

## Engineering reconstruction

### E1 — physical nonvolatility is not completion atomicity

Flash cells can retain state without power.

That does not imply an in-flight erase is all-or-nothing.

S1 exists precisely because power can disappear after an erase has changed some physical state but before the operation has safely completed.

Therefore:

```text
nonvolatile medium
    !=
atomic destructive operation
```

### E2 — “looks erased” is weaker than “erase completion is proven”

The recovery design does not grant reuse authority merely because a later read appears compatible with the erased value.

S1's concern about partially erased / intermediate states means the system needs a stronger qualification boundary.

Repository reconstruction:

```text
apparent erased-state read
    !=
qualified reusable unit
```

The source's concrete safe fallback is to repeat and verify the erase when completion evidence is missing.

### E3 — maintenance completion evidence is distinct retained state

Case 04 already separates:

- user payload;
- logical identity;
- virtual/physical mapping;
- block-allocation state.

S1 adds another retained-state class:

- **operation-completion / recovery evidence**.

That evidence can determine whether a unit may safely re-enter the allocator's free pool.

So the state relation becomes:

```text
payload state
    !=
identity / mapping state
    !=
allocation state
    !=
maintenance completion evidence
```

### E4 — reuse authority can depend on remembered negative history

A unit may physically exist and may even be readable.

Nevertheless, if retained evidence says its most recent erase was pending or not proven complete, the allocator should withhold ordinary reuse until recovery completes.

Repository term:

```text
negative operation history
    -> blocks premature reuse authority
```

The useful retained fact is not necessarily “the unit is bad.” It is “the unit has not yet re-earned the status required for ordinary use.”

### E5 — representation placement matters because recovery metadata can share failure exposure with the target

The older erase-mark scheme puts its completion witness in the erased unit itself.

The newer S1 embodiments can place pending/completed evidence in separate Flash locations or nonvolatile registers.

This change is motivated in part by programming-geometry constraints, not by an explicit theorem that “separate metadata is always safer.”

Still, it demonstrates that the same recovery relation can be embodied in materially different places:

```text
completion witness in target unit
    vs
completion witness in separate Flash locations
    vs
completion witness in nonvolatile registers
```

The semantics are not identical to their storage location.

### E6 — safe restart may discard precise progress and replay coarse work

If an interrupted erase is replayed from the beginning, the system is not continuing from the exact physical point of interruption.

It is preserving the **obligation** rather than the micro-progress.

```text
retain obligation identity
    !=
retain exact operation progress
```

This resembles other repository cases where a stronger authoritative fact allows weaker progress state to be forgotten.

### E7 — recovery correctness is scoped by the failure model

S1's mechanism is aimed at interrupted erasure and the ability to record / detect enough information around that interruption.

It does not by itself establish safety under every possible fault, including:

- controller logic corruption;
- loss/corruption of the recovery registers themselves;
- adversarial fault injection;
- multiple correlated storage failures;
- arbitrary torn writes to every metadata location;
- firmware bugs that name the wrong target unit.

The mechanism is meaningful because its failure model is bounded.

---

## Functional comparison inside `technical-retention`

### A1 — Case 04 vs Case 134 (COPYBACK interruption)

Case 134's Cypress COPYBACK deepening records a different failure/recovery rule:

```text
interrupted destination program
    -> affected page cannot simply be trusted
    -> quarantine until a later full block erase
```

S1's interrupted erase rule is instead:

```text
interrupted erase
    -> unit cannot simply be treated as reusable
    -> repeat / verify erase before normal use
```

Shared functional form:

```text
operation was in flight
    + completion not proven
    -> later authority is withheld
```

Different recovery action:

```text
program interruption -> quarantine / erase-before-reuse

erase interruption   -> re-erase / verify
```

This is a functional analogy only. No Cypress-to-M-Systems or M-Systems-to-Cypress lineage is claimed.

### A2 — Case 04 vs Case 152 (SQLite WAL checkpoint progress reset)

SQLite Case 152 shows that physical maintenance work may have happened even though restart conservatively forgets checkpoint progress and replays page-copy work from a stronger WAL authority source.

S1 likewise permits exact erase micro-progress to disappear while retaining a coarse obligation that triggers replay.

Functional comparison:

```text
precise progress may be discardable
if
a stronger retained fact safely determines restart action
```

The systems are historically unrelated for purposes of this repository comparison.

### A3 — Case 04 vs Case 145 / JFFS2 clean-marker style evidence

A filesystem can also attach a marker to an erase region so later software can distinguish regions considered clean from those needing recovery.

The similarity is useful only at the level of:

```text
destructive maintenance
    -> later reuse depends on retained completion evidence
```

This packet does not claim the M-Systems erase mark caused JFFS2 CLEANMARKER design, or vice versa.

---

## Philosophical interpretation

### I1 — preservation can require remembering an unfinished act of destruction

The obvious object of “retention” in Flash is the data that should remain available.

S1 exposes a less obvious retained relation: the system may need to remember that a destructive maintenance act **was not proven to have finished**.

That memory is productive because it prevents a later process from treating an uncertain physical region as ordinary free space.

A bounded project-level formulation is:

> continuity can depend on retaining not only what exists, but which destructive transitions have not yet earned completion authority.

This is interpretation, not historical M-Systems vocabulary.

### I2 — forgetting physical progress can coexist with preserving operational responsibility

After power loss, the controller need not know exactly how far the erase progressed.

It does need enough retained evidence to know what obligation remains.

Thus:

```text
forget exact physical progress
    while
preserve responsibility to re-establish a safe state
```

The retained relation is procedural rather than a frozen snapshot of the interrupted device.

### I3 — a free block is not merely a physical block with many `1` bits

Within this bounded failure model, “free/reusable” is partly an **authorized status** produced by successful maintenance qualification.

That status depends on relations among:

- physical cell condition;
- erase operation history;
- retained pending/completed evidence;
- restart recovery action;
- allocator decision.

Therefore a storage system can preserve logical continuity by being conservative about when physical space is allowed to become “free” again.

---

## Explicit non-claims

This evidence packet does **not** claim:

1. that `US6977847` proves the 1993 `US5404485` implementation had this exact erase-marker or register design;
2. that all TrueFFS versions used one identical power-loss-recovery mechanism;
3. that the TrueFFS erase-mark technique originated with M-Systems;
4. that the patent supplies an independently verified first-use date for the TrueFFS erase mark;
5. that every Flash erase interrupted by power loss produces the same physical bit pattern;
6. that reading an interrupted unit can never provide useful diagnostic evidence;
7. that a whole Flash translation layer is transactionally atomic merely because interrupted erase can be detected;
8. that logical-to-physical mapping updates in Case 04 are proven crash-atomic;
9. that user payload survives an erase operation targeting the unit that contains it;
10. that the recovery flags themselves are immune to corruption or implementation bugs;
11. that all embodiments require a capacitor or reserve-energy circuit;
12. that all embodiments write a pending flag before erase rather than at power-fail detection time;
13. that pending/completed flags are the only valid way to recover from interrupted erase;
14. that modern SSD firmware uses the same mechanism;
15. that NAND, NOR, MLC, SLC, TLC, QLC, or later managed Flash all share one identical interruption model;
16. that `PPP=1` describes all devices contemporary with the patent;
17. that the patent's proposed embodiments were all shipped in named commercial products;
18. that repeated erase after interruption has no endurance cost;
19. that erasing again is equivalent to secure sanitization;
20. that an erase-completion marker proves the old data is forensically unrecoverable;
21. that the patent solves host-level filesystem crash consistency;
22. that recording a target pointer proves the mapped logical object associated with that target is current;
23. that recovery metadata automatically remains semantically current after arbitrary remapping bugs;
24. that the source establishes a historical lineage to SQLite, Kafka, JFFS2, Cypress COPYBACK recovery, or any other repository comparison case.

---

## Claim ledger

| Claim | Class | Support | Confidence |
|---|---|---|---|
| M-Systems filed a patent family specifically addressing partial Flash erasure after power loss with 2001 provisional priority | H/P | S1 bibliographic record | high |
| S1 explicitly references the earlier M-Systems `US5404485` and `US5937425` Flash-management patents | H/P | S1 background | high |
| An interrupted erase can leave a unit in a state that must not simply be assumed reusable | H/P | S1 background and recovery procedures | high |
| S1 reports an older TrueFFS erase-mark practice used to detect incomplete erasure | H/P | S1 prior-art discussion | high for the first-party historical statement; medium for exact product breadth/date |
| S1 describes separate pending/completed evidence and nonvolatile unit-identity registers | H/P | S1 summary, claims, embodiments | high |
| Restart can re-erase and verify a unit whose completion was not established | H/P | S1 power-up procedures | high |
| The mechanism retains a recovery obligation rather than exact erase micro-progress | E | S1 state/control relation | high |
| Physical nonvolatility does not imply atomic erase completion | E | S1 failure model | high |
| Reuse authority depends on more than an apparently erased read value in this bounded design | E | S1 warning + recovery rule | high |
| S2 records multiple broader prior approaches to bounding suspect locations after power loss | H/P | S2 background | high |
| S1/S2 do not establish mapping-update crash atomicity for the 1993 Ban FTL | X | absence of such proof; scope distinction | high |
| Comparison to Cases 134/145/152 is functional, not genealogical | A | repository synthesis | high |

---

## What this changes in Case 04

Before this deepening, Case 04 had strong evidence for:

```text
logical identity
    -> movable physical embodiment
    -> reclamation by copy + erase
```

but intentionally stopped before crash-consistency claims.

This packet adds a bounded power-loss relation:

```text
reclamation / erase intent
    -> destructive operation in flight
    -> power loss may destroy execution context
    -> retained pending/completion evidence survives
    -> uncertain unit is denied ordinary reuse
    -> erase is replayed / verified
    -> reusable status can be re-established
```

The safe revised synthesis is:

> **Mapped-Flash continuity may require retained evidence not only of where current data lives, but also of whether destructive maintenance on candidate free space completed strongly enough for that space to be trusted again.**

The unsafe stronger synthesis remains rejected:

> **The 1993 Ban virtual map was already a fully crash-atomic FTL.**

That claim still lacks direct evidence.

---

## Related-repository boundary

A fresh search of `tmzncty/computing-archaeology` found no dedicated packet for M-Systems `US6977847`, TrueFFS erase marks, or the specific pending/completed-erase recovery seam.

`technical-retention` should retain only the cross-mechanism relation developed here:

```text
interrupted destructive maintenance
    -> retained completion evidence
    -> conservative restart action
    -> restored reuse authority
```

Broader work belongs in `computing-archaeology`, including:

- detailed TrueFFS / DiskOnChip product chronology;
- NAND/NOR erase-circuit history;
- Partial Page Programming evolution across device generations;
- M-Systems patent-family genealogy;
- exact controller/firmware implementations in shipped products;
- vendor-to-vendor adoption history.

---

## Remaining evidence debt

This slice is complete, but Case 04 still has important open work.

### 1. Mapping-update power-failure ordering remains open

The strongest remaining debt is still to find a primary early FTL source that explicitly shows how old/new mapping records are ordered, versioned, committed, or reconstructed when power disappears during a logical-sector replacement.

This packet must not be used as a substitute for that evidence.

### 2. A named shipping-product witness would strengthen implementation confidence

Useful future evidence would include a period M-Systems / DiskOnChip manual that explicitly documents:

- power-fail recovery;
- erase-mark behavior;
- startup scan/recovery;
- or a named firmware/TrueFFS version whose behavior can be tied to the patent relation.

### 3. The older TrueFFS “used for years” claim should be independently dated

S1 is a good first-party historical statement, but independent period manuals/releases would let the repository separate:

```text
patent author's recollection of prior deployment
    from
independently dated product evidence
```

### 4. Device-specific interruption behavior remains a separate empirical question

A hardware experiment could characterize one historical or representative Flash device under deliberately interrupted erase, but such an experiment would be a new implementation witness, not proof of every device covered by the patent's generalized discussion.

---

## Bottom line

The M-Systems 2001–2003 record supplies a concrete power-loss boundary that Case 04 previously lacked:

```text
nonvolatile cells
    do not make
in-flight erase atomic

and

erase intent
    does not create
reuse authority

therefore

retained pending / completion evidence
    + conservative replay / verification
    can preserve
safe future allocation after restart
```

The key technical-retention lesson is deliberately narrow:

> **when destructive maintenance is interruptible, continuity can depend on preserving evidence that completion is unproven, even if the exact physical progress of the interrupted operation is allowed to disappear.**
