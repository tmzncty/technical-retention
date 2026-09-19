# Case 59 deepening — Invox row-state control embodiments and reconstructible protection state, 2000

## Status

**`bounded deepening complete`** — this note inspects the public 2000 Invox patent record for US6058060A / US 6,058,060 closely enough to establish that one program-disturb protection policy was disclosed with **multiple alternative embodiments for representing the prior programmed/erased state of rows**: volatile flag/latch state, a shift register, a nonvolatile memory cell associated with each row, or no stored flag state at all when sequential programming and the current row address are sufficient to infer which earlier rows contain data.

This closes one retention-specific question left open by the 1998 abstract-level Invox addendum:

> **Does protecting already-written threshold state require one particular persistent metadata embodiment, or can the same write-time protection decision be supported by volatile, nonvolatile, or reconstructible control state?**

The answer in the inspected 2000 public record is: **the patent explicitly discloses several alternatives, so one cannot infer a single persistence horizon from the protection function alone.**

This note does **not** back-project those implementation alternatives into the still-uninspected full 1998 US5818757 specification. The 1998 patent remains directly grounded only at the level already inspected in Case 59: public title/metadata and abstract-level mechanism. The richer control-state alternatives below are attributed to the 2000 US6058060 public record unless a future pass directly verifies them in the earlier full specification.

Canonical case: [`../cases/59-nand-program-interference-write-induced-neighbor-drift.md`](../cases/59-nand-program-interference-write-induced-neighbor-drift.md)

Earlier terminology/mechanism addendum: [`59-program-disturb-1997-1999-terminology-mechanism-boundary.md`](59-program-disturb-1997-1999-terminology-mechanism-boundary.md)

## Bounded question

Case 59 already established an Invox retention relation from the October 1998 public abstract:

```text
row already written
    -> later write can disturb retained threshold state
    -> protection logic chooses a different word-line bias
```

The earlier addendum deliberately stopped before claiming how the row-history indication survived reset, erase, power loss, or later accesses.

The present slice asks only:

1. what the later same-company public technical record says the row-history indicator can be;
2. whether the protection function requires a separately persistent flag;
3. what engineering distinction follows between retained payload, protection-policy knowledge, representation of that knowledge, and reconstructibility;
4. what this does **not** prove about the 1998 patent, commercial products, or modern Flash controllers.

It does not attempt a general Invox/SanDisk product history or a general program-disturb genealogy.

---

## Source custody and chronology

### 1. US5818757A / US 5,818,757 — public 6 October 1998

Hock C. So and Sau C. Wong, Invox Technology, **“Analog and multi-level memory with reduced program disturb.”**

Stable metadata/abstract record:

- <https://idiyas.com/patent/badge/5818757>
- <https://patents.justia.com/inventor/hock-c-so?page=2>

The checked public record gives:

- filing date: **22 July 1996**;
- patent/publication date: **6 October 1998**;
- assignee: **Invox Technology**;
- inventors: **Hock C. So** and **Sau C. Wong**.

Its abstract establishes that a bias voltage on unselected word-lines reduces program disturb of threshold voltages during another write; the bias is applied differently to already-written cells/rows than to erased or virgin cells; sequential recording can fill one row before proceeding to the next; and bias-flag circuitry can indicate which rows are filled.

This remains the **1998 public terminology/mechanism floor** used by the earlier Case 59 addendum.

### 2. US6058060A / US 6,058,060 — public 2 May 2000

Sau C. Wong, Invox Technology, **“Multi-bit-per-cell and analog/multi-level non-volatile memories with improved resolution and signal-to-noise ratio.”**

Full-text patent transcription:

- <https://patents.justia.com/patent/6058060>
- <https://uspto.report/patent/grant/6%2C058%2C060>

The checked record gives:

- filing date: **31 December 1998**;
- patent/publication date: **2 May 2000**;
- assignee: **Invox Technology**;
- inventor: **Sau C. Wong**.

The application date is useful application chronology, but the directly checked public-evidence date for this record is the 2000 patent publication. This note therefore does **not** rewrite `31 December 1998` as a public disclosure date.

The 2000 specification cites the earlier US5818757 work in its program-disturb discussion, but it is a later patent with its own claims and embodiments. The present note uses it as a **later same-company continuity/deepening witness**, not as a facsimile substitute for the earlier patent.

### 3. US6285593B1 / US 6,285,593 — public 4 September 2001

Sau C. Wong, SanDisk Corporation, **“Word-line decoder for multi-bit-per-cell and analog/multi-level memories with improved resolution and signal-to-noise ratio.”**

Record:

- <https://patents.justia.com/patent/6285593>

This later divisional/continuity record repeats the same family of row-state / word-line-decoder implementation alternatives and explicitly cites US5818757. It is used only as a **cross-check that the disclosure persisted into the later public lineage**. It does not move the public floor earlier than the directly checked 2000 record.

---

## Historical record

### H1. Write-time bias depends on prior row state

In the 2000 Invox record, the word-line decoder distinguishes at least three relevant conditions for a row during programming:

1. the selected row being programmed;
2. an unselected row that already contains programmed data;
3. an unselected row that remains erased.

The described word-line driver can therefore choose different voltages for unselected rows according to their prior programmed/erased state.

Retention-specific result:

> **already-retained payload state participates in the control condition for a later write.**

This is not a modern controller abstraction imposed on the patent. It follows from the patent's concrete distinction between already-programmed and erased rows when choosing word-line treatment.

### H2. One disclosed embodiment uses volatile flag/latch state

The specification describes bias-flag circuits associated with rows. After an erase, the flags indicate that rows are not programmed; when a row is selected for programming, its associated flag is set so the decoder can treat that row differently during a later write.

One disclosed implementation makes each bias flag a **volatile memory cell or latch**.

This is historically significant for retention analysis because it blocks a tempting inference:

> protection-policy knowledge is used later
> therefore the knowledge must itself be stored nonvolatily.

The record explicitly supplies a counterexample embodiment in which the immediate control representation is volatile.

### H3. A shift register is another disclosed representation

The specification says the per-row bias flags may instead be replaced with a **shift register** that shifts when the row-address signal changes.

This matters because the state is no longer naturally described as an independent durable bit permanently paired with every row. It can instead be represented as **progress/order state** that advances along with sequential access/programming.

No claim is made here about power-loss persistence of that shift register. The public record establishes the alternative representation, not a reset-recovery contract.

### H4. A nonvolatile row-associated cell is also disclosed

The same specification separately describes an alternative in which a **nonvolatile memory cell associated with each row** can indicate whether the rest of that row remains erased.

Thus the same broad protection decision can be supported by an embodiment with a longer persistence horizon than the volatile-latch embodiment.

The important historical result is plural rather than singular:

> **the patent family did not bind the protection function to one control-state persistence class.**

### H5. The patent also discloses a no-memory / address-derived alternative

Most important for this slice, the specification gives another embodiment in which the bias-flag circuits **do not themselves have memory capability**. Instead, row-address information is used to determine which rows contain data under the stated sequential-programming regime: if rows are programmed in sequence, rows below the current row address can be treated as already containing data.

That makes the relation materially different from both the volatile and nonvolatile flag versions:

```text
sequential-programming invariant
    + current row address
    -> infer which prior rows contain data
    -> choose protective word-line bias
```

The protection-relevant knowledge can therefore be **derived from an ordering invariant plus current position**, rather than retrieved from a separately retained per-row history bit.

### H6. A sequential selector implementation resets working state before operations

The 2000 record also describes a sequential word-line-selector implementation based on a series of flip-flops. In that embodiment the flip-flops are reset before operations and clocked so selection/bias signals advance through rows.

For this repository the safe historical use is narrow:

> the public record contains an implementation in which relevant working control state is intentionally regenerated for an operation rather than treated as a durable historical ledger.

This is not evidence that every disclosed embodiment behaves identically across reset or power loss.

---

## Engineering reconstruction

### E1. Payload persistence != control-state persistence

The stored analog/multilevel threshold state is nonvolatile payload. The protection decision used during a later write depends on whether a row is already programmed. But the patent discloses several ways to supply that knowledge.

Therefore:

```text
payload survives
    !=
particular bias-flag representation survives
```

The payload and the current representation of protection knowledge have different possible persistence horizons.

### E2. Protection function != representation choice

The same broad control function can be implemented by:

```text
A. volatile per-row latch/flag
B. shift-register progress state
C. nonvolatile per-row indication
D. no stored per-row flag, infer from sequential address/order
```

Therefore:

> **same protection function != same state embodiment.**

This is a stronger retention distinction than the earlier abstract alone permitted.

### E3. Required knowledge != separately retained metadata

The decoder needs an answer to a functional question:

> Is this unselected row already programmed or still erased, such that a different bias should be chosen?

But the answer need not always exist as a separately retained bit.

Under the sequential-programming assumption it can be reconstructed from current position and the invariant that earlier rows have already been filled.

Thus:

> **control knowledge required for safe operation != separately persisted control metadata.**

This is not a claim that reconstruction is free or universally safe. It depends on the validity of the ordering assumption.

### E4. Reconstructibility is conditional authority

The no-memory embodiment is only justified while its premise remains true:

```text
rows are programmed sequentially
    -> row-address ordering encodes prior fill state
```

If the history does not obey that relation, row address alone is not sufficient evidence of prior row state.

Therefore:

> **derivability from current position is an authority only under a preserved history invariant.**

This is an engineering reconstruction from the disclosed embodiment, not language used by the patent.

### E5. Losing a volatile representation is not automatically equivalent to losing the underlying fact

A volatile flag may disappear even though the nonvolatile row payload still physically embodies whether the row has been programmed. The patent's alternative embodiments show that the protection-relevant fact and one particular representation of that fact can be separated.

Accordingly:

```text
loss of working flag state
    !=
necessary loss of payload state
    !=
necessary loss of all possible evidence about prior programming
```

Whether a concrete implementation can safely reconstruct the needed relation after a particular reset or power event remains unestablished here.

### E6. Conversely, nonvolatile control state is not automatically authoritative forever

A nonvolatile row-associated indicator persists longer, but persistence alone does not prove correctness after an erase, interrupted operation, defective cell, or an implementation-specific update failure.

The patent describes clearing/setting relations around erase and program activity; it does not provide a crash-consistency proof for the nonvolatile-indicator alternative.

Therefore:

> **nonvolatile != automatically current/authoritative under every interruption.**

This is a general engineering caution applied only to the absence of a verified interruption protocol in the inspected source.

---

## Functional comparisons — bounded

### A1. Case 43 / Case 93 — control knowledge protects payload

A narrow functional analogy remains valid:

- AVATAR/related DRAM cases use retained classification/policy state to decide refresh treatment;
- the Invox disclosure uses row programmed/erased knowledge to decide write-time bias treatment.

Shared function:

> **payload preservation depends on non-payload control knowledge.**

Stop condition:

- DRAM refresh classification is not Flash program-disturb bias selection;
- AVATAR's profile revalidation problem is not an Invox row-order problem;
- no genealogy or shared metadata format is claimed.

### A2. Case 145 — reconstruction from retained evidence

A second narrow analogy is possible with JFFS2's restart-time reconstruction:

> a volatile working classification can be regenerated from more persistent evidence or invariants rather than itself surviving indefinitely.

Stop condition:

- JFFS2 scans a flash filesystem and reconstructs allocator/erase-block state after mount;
- the Invox no-memory embodiment infers programmed-row status from sequential addressing/order during memory operation;
- there is no filesystem scan, crash protocol, or equivalent recovery algorithm here.

### A3. Case 137 — control root versus underlying durable content

Another functional comparison is possible with LevelDB's separation of durable content from metadata that selects/interprets it:

> retained payload and retained/reconstructed control state can have different durability roles.

Stop condition:

- LevelDB's `CURRENT`/MANIFEST relation is a filesystem metadata publication problem;
- Invox's relation is an on-chip bias-selection problem;
- no historical or technical genealogy is claimed.

---

## Philosophical interpretation — bounded

The case supports one modest project-level pressure:

> **the persistence of a technical capacity does not require the persistence of one identical auxiliary representation.**

A system may continue to know enough to protect already-written state because the necessary relation is:

- currently held in volatile working state;
- encoded in a more persistent control cell;
- represented by progress state;
- or recoverable from a preserved ordering relation.

This does not imply that storage is immaterial or that metadata is dispensable. The alternatives are all materially implemented and each imposes different assumptions and failure boundaries.

A sharper formulation is:

> **what must persist is not always a particular bit-pattern named `metadata`; what must remain available is sufficient evidence or structure to re-establish the control relation required by the next operation.**

That sentence is a repository interpretation, not Invox's vocabulary.

---

## Explicit non-claims

This deepening does **not** claim that:

1. US6058060 invented program disturb;
2. US6058060 invented multilevel Flash;
3. the 31 December 1998 filing date is a public-disclosure date;
4. the richer 2000 implementation alternatives were necessarily present in the full 1998 US5818757 specification;
5. US5818757 has now been fully facsimile-inspected;
6. the Invox design is NAND Flash;
7. the 1998/2000 Invox disturb mechanism is the same as the 2002+ NAND cell-to-cell capacitive program-interference mechanism;
8. the 2000 patent proves commercial deployment of any one embodiment;
9. an Invox or SanDisk shipping product used volatile bias flags;
10. a shipping product used nonvolatile per-row flags;
11. a shipping product used the no-memory/address-derived embodiment;
12. the disclosed volatile flag state survives power loss;
13. the shift register survives reset or power loss;
14. the nonvolatile row-associated indicator is crash-consistent under interrupted program/erase;
15. the no-memory embodiment can tolerate arbitrary out-of-order programming;
16. modern FTL metadata descends from these circuits;
17. the patent discloses a modern checkpoint, log, journal, or recovery transaction;
18. the later SanDisk patent lineage proves direct adoption into modern NAND controllers;
19. similar control-state reconstruction in other cases proves shared genealogy;
20. one persistence horizon is intrinsically superior to the others without a concrete workload/failure model.

---

## Claim ledger

| ID | Claim | Layer | Evidence strength | Boundary |
| --- | --- | --- | --- | --- |
| H-59.51 | US5818757 is publicly dated 6 Oct 1998 and its abstract distinguishes already-written from erased/virgin rows for word-line-bias treatment | Historical record | strong, public patent metadata/abstract | full 1998 specification still not directly inspected here |
| H-59.52 | US6058060 is filed 31 Dec 1998 and publicly patented 2 May 2000 by Invox | Historical record | strong, patent record | filing date != public date |
| H-59.53 | the 2000 specification discloses volatile per-row bias flags/latches | Historical record | strong, full-text transcription | deployment not established |
| H-59.54 | the 2000 specification discloses shift-register replacement for per-row bias flags | Historical record | strong | persistence across reset/power not established |
| H-59.55 | the 2000 specification discloses a nonvolatile row-associated cell as an alternative programmed/erased indication | Historical record | strong | update atomicity/currentness not established |
| H-59.56 | the 2000 specification discloses a no-memory alternative using row address plus sequential programming | Historical record | strong | only under stated sequencing relation |
| H-59.57 | the 2000 sequential selector can reset working flip-flops before operations and regenerate selection progression | Historical record | strong | not a power-fail recovery protocol |
| E-59.58 | payload persistence and protection-control representation can have different horizons | Engineering reconstruction | strong from alternative embodiments | bounded to disclosed architecture |
| E-59.59 | required safe-operation knowledge need not be separately persisted when inferable from a valid ordering invariant | Engineering reconstruction | strong | invariant must remain true |
| E-59.60 | loss of one volatile representation does not logically prove loss of every possible evidence source for prior programming | Engineering reconstruction | moderate/strong | concrete restart behavior not tested |
| A-59.61 | Case 43/93 provide a functional analogy in which non-payload control knowledge protects payload | Functional analogy | bounded | mechanisms and genealogy differ |
| A-59.62 | Case 145 provides a functional analogy for regeneration of volatile classification from retained evidence/invariants | Functional analogy | bounded | no filesystem/restart equivalence |
| I-59.63 | persistence of technical capacity need not mean persistence of one identical auxiliary representation | Philosophical interpretation | bounded | repository formulation, not actor vocabulary |

---

## Related-repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `5818757`, `Invox program disturb`, and related vocabulary found no dedicated packet to reuse.

Accordingly this file keeps only the retention-specific seam:

```text
prior programmed/erased payload state
    -> protection-relevant control knowledge
    -> multiple possible control-state embodiments
       (volatile / progress / nonvolatile / derived)
    -> write-time bias authority
```

A broad history of Invox's analog-Flash products, exact circuit genealogy, SanDisk acquisition/adoption, commercial device deployment, NOR/NAND architectural transitions, and subsequent program-disturb mitigation belongs primarily in `computing-archaeology` if developed later.

---

## Remaining evidence debt

This pass intentionally leaves several bounded questions open:

1. **Direct full 1998 US5818757 specification/facsimile inspection.** The original abstract is directly checked, but the richer embodiment alternatives are not projected backward from the 2000/2001 records.
2. **Reset/power-loss semantics.** The inspected 2000 record gives alternative state embodiments but does not provide a complete power-interruption protocol for each one.
3. **Commercial deployment.** No named shipping Invox/SanDisk part is tied to any specific bias-flag implementation here.
4. **Exact patent genealogy.** The 1998, 2000, and 2001 records are technically related/citing records, but this note does not claim one simple continuation chain where the patent record does not establish it.
5. **Fault experiment.** No electrical simulation or interrupted-program experiment is performed in this repository.

These are future deepening targets, not blockers for the bounded relation established here.

---

## Result

The central retention result is now:

```text
nonvolatile payload state
    -> later write needs programmed/erased-row knowledge

that knowledge may be represented as:
    volatile per-row flag/latch
    OR shift/progress state
    OR nonvolatile row-associated state
    OR no separately retained state,
       when current address + sequential-order invariant is sufficient

therefore:
    protection function
        != particular metadata embodiment
        != particular persistence horizon
        != proof of commercial implementation
```

And the anti-anachronism boundary remains:

> **a later same-company disclosure can deepen the space of historically documented implementations without being silently back-projected into an earlier patent whose full specification has not yet been directly inspected.**

## Sources

1. Hock C. So and Sau C. Wong, Invox Technology, US5818757A / US 5,818,757, **“Analog and multi-level memory with reduced program disturb,”** filed 22 July 1996, patented/published 6 October 1998. Metadata/abstract: <https://idiyas.com/patent/badge/5818757> and inventor record at <https://patents.justia.com/inventor/hock-c-so?page=2>.
2. Sau C. Wong, Invox Technology, US6058060A / US 6,058,060, **“Multi-bit-per-cell and analog/multi-level non-volatile memories with improved resolution and signal-to-noise ratio,”** filed 31 December 1998, patented/published 2 May 2000. Full-text transcription: <https://patents.justia.com/patent/6058060>; secondary mirror of patent text: <https://uspto.report/patent/grant/6%2C058%2C060>.
3. Sau C. Wong, SanDisk Corporation, US6285593B1 / US 6,285,593, **“Word-line decoder for multi-bit-per-cell and analog/multi-level memories with improved resolution and signal-to-noise ratio,”** patented 4 September 2001. <https://patents.justia.com/patent/6285593>.
4. Sau C. Wong and Hock C. So, Invox Technology, US5923585A / US 5,923,585, **“Source biasing in non-volatile memory having row-based sectors,”** patented 13 July 1999. <https://www.sauwong.com/patents/5923585>. Used only as adjacent Invox program-disturb context, not as evidence for the row-flag embodiment claims above.
