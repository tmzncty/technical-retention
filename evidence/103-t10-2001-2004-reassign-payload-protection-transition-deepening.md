# Evidence 103 — T10 REASSIGN BLOCKS Payload-Protection Transition, 2001–2004

## Status

**`bounded deepening complete`**

## Scope

This record tightens one standards-history debt left open by Case 103:

> **When did the public T10/SBC-2 text move from a `REASSIGN BLOCKS` contract in which data in the listed defective blocks could be altered to a contract that explicitly carried recoverable user data and protection information into the reassigned logical block?**

The result is intentionally bounded. It does **not** identify the exact first SBC-2 revision containing the stronger clause. It does, however, shrink the previous 2001→2005 bracket substantially and recover the proposal lineage that made protection information relevant to `REASSIGN BLOCKS`.

The evidence now supports this chronology:

```text
11 Jul 2001 — T10 01-210r0
    listed-block data "may be altered"

25/31 May 2003 — SBC-2 Revision 9 witness
    same older payload wording still present

1 May 2003 — T10 03-176r0 proposal
    REASSIGN BLOCKS explicitly flagged for valid protection information

Nov 2003 — CAP minutes
    proposal lineage renamed 03-176 -> 03-365r0 and still under active revision

18 Apr 2004 — T10 04-114r0
    says 03-365r1 was the final draft of the simplified E2E proposal;
    SBC-2 Revision 13 already contains the associated protection-field infrastructure

13 Nov 2004 — SBC-2 Revision 16 final T10 committee draft
    recoverable user data + protection information SHALL be written to the reassigned block;
    unrecoverable data gets vendor-specific user data and default protection information
```

Thus the directly observed normative-text transition is now bounded by **Revision 9 → Revision 16 (May 2003 → November 2004)** rather than merely by a 2001 proposal and a September 2005 SBC-3 draft.

This file is retention-specific standards archaeology. It is not a general history of SCSI end-to-end data protection, DIF/DIX terminology, disk defect management, or every `REASSIGN BLOCKS` implementation.

---

## Repository context checked

Before this slice, the following repository material was re-read:

- [`../cases/103-scsi-verify-host-driven-medium-qualification.md`](../cases/103-scsi-verify-host-driven-medium-qualification.md)
- [`103-scsi-2001-2022-verification-vs-remediation-authority-deepening.md`](103-scsi-2001-2022-verification-vs-remediation-authority-deepening.md)
- [`../cases/14-scsi-disk-defect-reassignment-logical-identity.md`](../cases/14-scsi-disk-defect-reassignment-logical-identity.md)
- `README.md`, `ROADMAP.md`, `AGENTS.md`, `docs/METHOD.md`, `docs/PRIOR_ART.md`, `docs/TECHNICAL_SPINE.md`, and `RELATED_REPOS.md`.

A fresh search of `tmzncty/computing-archaeology` for `REASSIGN BLOCKS`, `SCSI VERIFY`, and the combined terms found no dedicated overlapping technical-history slice. Broader SCSI/DIF genealogy therefore remains appropriate for that companion repository rather than being reconstructed here.

---

## Sources inspected

### Primary T10 material

1. George Penokie (Tivoli), T10 **01-210r0, _Reassign Blocks 2 TBytes Support_**, 11 July 2001.  
   <https://www.t10.org/ftp/t10/document.01/01-210r0.pdf>

2. T10, **SCSI Block Commands - 2 (SBC-2) project page**, Project 1417-D / INCITS 405.  
   <https://www.t10.org/members/w_sbc2.htm>

3. George Penokie (IBM/Tivoli), T10 **03-176r0, _End-to-End Data Protection_**, 1 May 2003.  
   <https://www.t10.org/ftp/t10/document.03/03-176r0.pdf>

4. Ralph Weber and John Lohmeyer, T10 **03-371r0, _SCSI Commands, Architecture, & Protocol Working Group Meeting -- November 4-5, 2003_**, 6 November 2003.  
   <https://www.t10.org/ftp/t10/document.03/03-371r0.pdf>

5. Keith Holt (LSI Logic), T10 **04-114r0, _SBC-2 Option to Check Only the Logical Block Guard_**, 18 April 2004.  
   <https://www.t10.org/ftp/t10/document.04/04-114r0.pdf>

6. T10 **Working Drafts** publication page for final committee drafts.  
   <https://www.t10.org/drafts.htm>

### Primary-draft text available through indexed mirrors

7. **T10/1417-D Revision 9, _Working Draft SCSI Block Commands - 2 (SBC-2)_**, cover date 25 May 2003; the official T10 project page lists Revision 09 as 31 May 2003. Indexed surviving copy:  
   <https://citeseerx.ist.psu.edu/document?doi=ede8b9b71c690d841a61e5670a48a4e2c82d82f9&repid=rep1&type=pdf>

8. **T10/1417-D Revision 16, _Working Draft SCSI Block Commands - 2 (SBC-2)_**, 13 November 2004. Indexed surviving copy:  
   <https://citeseerx.ist.psu.edu/document?doi=ee9633c63189099a796a09ae69824ca39b0f4fc3&repid=rep1&type=pdf>

The T10 project and Working Drafts pages independently establish Revision 16 as the **13 November 2004 final T10 committee working draft** and map it to **INCITS 405-2005**. The indexed mirror is used for the directly inspectable command text because the public T10 final-draft endpoint is membership-restricted.

---

## Historical record

### H/P — 01-210r0 still gives listed-block payload only a weak preservation contract

T10 `01-210r0`, dated **11 July 2001**, proposes the corrected large-LBA `REASSIGN BLOCKS` parameter handling for SBC-2. Its command text says that the application client supplies logical block addresses and that the device server reassigns the physical medium used for each listed LBA.

The retention-critical sentence is explicit: **data in the logical blocks named in the defect list may be altered**, while data in all other logical blocks shall be preserved.

That yields three distinct relations even before later data-protection work:

```text
logical designation survives reassignment
    !=
physical embodiment survives reassignment
    !=
old payload is guaranteed to survive reassignment
```

This proposal also notes that one LBA may be reassigned repeatedly over the life of the medium until spare locations are exhausted.

The document is a T10 proposal, not proof that every shipping drive implemented this exact text.

### H/P* — SBC-2 Revision 9 still carries the older wording in May 2003

The directly indexed copy of **T10/1417-D Revision 9** has cover date **25 May 2003**. T10's own project page lists Revision 09 with date **31 May 2003**. The discrepancy is retained rather than silently normalized: the former is the draft-cover date visible in the surviving text, while the latter is the project's revision-list date.

The `REASSIGN BLOCKS` clause in Revision 9 still states that data in the logical blocks specified by the defect list **may be altered**, while all other logical blocks shall be preserved.

Therefore the older payload contract is not merely a 2001 proposal artifact. It remains directly visible in an SBC-2 working draft in late May 2003.

> **Direct old-wording floor: SBC-2 Revision 9, May 2003.**

`H/P*` is used here because the text is an indexed copy of the T10 draft rather than a directly renderable public T10-hosted facsimile; official T10 metadata independently verifies the revision sequence/date.

### H/P — 03-176r0 makes REASSIGN a target of the new protection-information work

T10 `03-176r0`, **1 May 2003**, is explicitly a proposal for standardized end-to-end data protection. Its overview proposes per-block protection information and states that protection information received by a device server is to be retained until overwritten.

Most important for this slice, its `Protected data commands` list includes `REASSIGN BLOCKS` with an editing note saying the command description needs to state that the **reassigned block needs valid protection information written with it**.

This is proposal-stage evidence. It proves that the standards-development work had identified reassignment as a place where protection information could not simply be ignored.

It does **not** by itself prove:

- that the final wording already existed on 1 May 2003;
- that the proposal was accepted unchanged;
- that every device stored protection information physically adjacent to user data;
- that a recoverability obligation for the old user payload had already been standardized.

The editing note is therefore treated as a historical development marker, not as final normative semantics.

### H/P — the November 2003 CAP minutes preserve the proposal lineage and its still-changing state

T10 `03-371r0`, minutes for the **4–5 November 2003** SCSI Commands, Architecture, & Protocol working-group meeting, says the group reviewed the latest simplified end-to-end data protection proposal, **formerly `03-176`, now `03-365r0`**.

The same minutes record discussion and agreement on several specific changes, including increasing the protection-control fields from two bits to three, and say Penokie would revise the proposal.

This matters because it prevents a false clean chronology:

```text
03-176r0 exists
    !=
proposal already frozen
    !=
final SBC-2 wording already established
```

The proposal family was still under active revision in November 2003.

### H/P — by April 2004 the protection proposal had a "final draft" and Revision 13 already exposed its infrastructure

T10 `04-114r0`, dated **18 April 2004**, looks back on the data-protection work. It says the `RDPROTECT` and `WRPROTECT` fields were introduced in `03-176r2` on **31 July 2003**, that the fields were later expanded, and that the change was made in the **final draft of the proposal, `03-365r1`**.

The same document says **SBC-2 Revision 13** requires the reference tag to equal the lower four bytes of the LBA, demonstrating that substantial protection-information machinery had already entered the working draft by that revision.

T10's SBC-2 project page dates Revision 13 to **20 March 2004**.

This does not directly prove that Revision 13 already contained the final `REASSIGN BLOCKS` payload-recovery sentence. The present slice therefore refuses to collapse:

```text
protection-information infrastructure incorporated
    !=
specific REASSIGN payload clause verified in that revision
```

### H/P* — Revision 16 has the stronger recover-if-possible reassignment contract

The indexed text of **T10/1417-D Revision 16, 13 November 2004** changes the retention contract materially.

For each LBA in the defective-LBA list, the device server still reassigns the medium. But the command overview now says:

- if the device server can recover user data and protection information, it **shall write the recovered user data and protection information to the reassigned logical block**;
- if it cannot recover them, it shall write vendor-specific user data and a defined default protection-information value when protection is enabled;
- all other logical blocks remain preserved.

T10's Working Drafts page identifies this Revision 16 as the **final T10 committee working draft** for SBC-2, later published as **INCITS 405-2005**.

The important change is therefore not merely that protection metadata was added somewhere in the standard. The `REASSIGN BLOCKS` operation itself now carries an explicit conditional payload-transfer obligation.

```text
old contract:
    listed-block payload may be altered

Revision 16 contract:
    if old user data + PI are recoverable,
    carry them into the reassigned logical block
```

### H/P — the observable transition window is now Revision 9 → Revision 16

Because Revision 9 still has the old wording and Revision 16 has the stronger wording, the exact direct-text bracket becomes:

```text
SBC-2 Revision 09
    cover: 25 May 2003
    T10 project list: 31 May 2003
    old "may be altered" contract

        [uninspected exact first-change revision]

SBC-2 Revision 16
    13 Nov 2004
    recover-if-possible user-data + PI contract
```

This is a substantial tightening from the repository's previous `2001 proposal → September 2005 SBC-3` bracket.

The exact first revision between 10 and 16 containing the final clause remains open. Revision 13 is known to have protection-information infrastructure, but this pass does not pretend that infrastructure proves the exact `REASSIGN` wording.

---

## Engineering reconstruction

The statements in this section are project analytical terms, not T10 historical vocabulary.

### E — reassignment can preserve a service designation under two different payload contracts

Both the older and newer clauses preserve the idea that a named LBA is reassigned to different medium. What changes is the command's obligation toward the old value.

Thus:

```text
same logical designation after repair
    !=
unchanged payload-preservation contract across revisions
```

This is why command-name continuity cannot stand in for semantic continuity.

### E — the stronger contract is conditional, not magical recovery

Revision 16 does not promise that every defective block's old payload will survive. The obligation is conditional on successful recovery.

So:

```text
reassignment completed
    !=
old user payload recovered
```

and:

```text
payload unrecoverable
    -> logical service slot may still be reassigned
    -> replacement block receives defined fallback content
```

Logical-address continuity and value continuity remain separate even after the standard strengthens the repair contract.

### E — protection information becomes part of what must accompany a valid recoverable block

The 2003 proposal explicitly brings `REASSIGN BLOCKS` into the end-to-end protection-information problem. By Revision 16, the command requires recoverable protection information to travel with recoverable user data.

Retention therefore includes more than the user-data bytes when the protection regime is enabled:

```text
current recoverable block state
    = user data relation
    + protection-information relation
    + logical designation
    + current physical embodiment
```

This is a functional decomposition, not a claim that T10 defined a philosophical ontology of retained state.

### E — standards-development intent, draft incorporation, and final committee text are separate evidence layers

This slice exposes four evidence stages:

```text
editing note / proposal target
    -> working-group revision process
    -> feature infrastructure in a working draft
    -> directly observed command text in final committee draft
```

Those stages should not be collapsed into one date of "introduction".

### E — date labels themselves have provenance

Revision 9 illustrates a smaller but important source-control rule: a surviving draft cover says **25 May 2003**, while the official T10 project revision list says **31 May 2003**.

The correct response is not to choose one silently. They refer to different documentary surfaces and should be preserved as such unless an archival record explains the discrepancy.

---

## Cross-case comparison

### Case 103 — VERIFY remains a qualification primitive, not a repair command

The present slice deepens the downstream repair side of Case 103.

Case 103 already establishes:

```text
VERIFY
    -> qualification / error evidence

REASSIGN BLOCKS
    -> embodiment-replacement authority
```

This new chronology adds that the *repair command itself* changed its payload-preservation contract across SBC-2 development.

Therefore:

```text
verification evidence
    !=
repair authority
    !=
payload-preservation guarantee attached to repair
```

### Case 14 — logical identity across physical replacement

Case 14 uses 1990–1997 evidence to show that the same host-visible LBA can survive physical replacement even when `REASSIGN BLOCKS` itself does not preserve the old payload.

Revision 16 does not invalidate that older case. It supplies a later standards-development change:

- **1997 Seagate / May-2003 Rev9 family:** designation can survive even though affected-block payload preservation is not guaranteed by reassignment;
- **Nov-2004 Rev16:** if the payload and protection information are recoverable, the command now requires them to be carried forward.

The cross-case rule becomes stronger:

> **designation continuity is stable enough to survive a change in physical embodiment, while the payload-preservation obligations attached to the repair operation can themselves evolve historically.**

### Case 101 — discovery and remediation remain distinct

Background Medium Scan work can expose a defect before remediation is complete. The present slice adds another axis: even after remediation is selected, the exact preservation contract of that remediation is revision-dependent.

```text
defect discovered
    !=
repair selected
    !=
replacement completed
    !=
old payload successfully recovered
```

### Functional analogy boundary

It is acceptable to compare this with mapped-Flash or distributed repair at the level of **logical designation surviving embodiment replacement**.

It is not acceptable to infer:

- shared algorithms;
- direct genealogy;
- equivalent failure domains;
- equivalent metadata structures;
- identical atomicity guarantees.

---

## Prior-art / genealogy boundary

This evidence does **not** establish:

- who invented SCSI defect reassignment;
- when the first disk firmware preserved data during reallocation;
- when vendors first implemented end-to-end protection information;
- that `03-176r0` was adopted unchanged;
- that Revision 13 already had the final `REASSIGN BLOCKS` clause;
- the exact revision among 10–16 where the stronger wording first appeared;
- a direct product lineage from the committee drafts to any named drive;
- that every drive conforming to SBC-2 performed reassignment identically internally;
- that successful reassignment is crash-atomic;
- that fallback vendor-specific data preserves the old user value;
- that default protection information proves semantic validity of unrecoverable user data.

The safe historical result is narrower:

> **The older `listed data may be altered` rule is directly visible through SBC-2 Revision 9 in May 2003. A May 2003 T10 end-to-end protection proposal explicitly targets `REASSIGN BLOCKS` for valid protection information; that proposal remains under active revision in November 2003 and is described as finalized as `03-365r1` by April 2004. The final T10 SBC-2 Revision 16 of 13 November 2004 directly contains the stronger conditional recover-and-carry-forward rule.**

---

## Philosophical interpretation — bounded

The useful conceptual point is not that standards "remember" old data. It is that persistence of one technical identity can depend on a historically changing contract about what relations must survive a repair transition.

An LBA can remain callable after a defective sector is replaced. But what it means for the **same retained block** to have survived is not exhausted by the address alone:

- the designation may continue;
- the physical embodiment may change;
- the old user value may or may not be recoverable;
- protection information may become part of the required carried-forward state.

That does not make the standard a philosophical theory of identity. It supplies an engineering counterexample to any claim that stable naming alone guarantees stable retained content.

---

## Remaining evidence debt

The bounded slice is complete, but several narrower questions remain open:

1. inspect SBC-2 Revisions 10, 11, 12, 13, 14, 15, 15a, and 15b directly to identify the **first exact revision** carrying the stronger `REASSIGN BLOCKS` wording;
2. identify the T10 motion / incorporated proposal that changed the exact command text, rather than inferring it from the broader end-to-end protection proposal family;
3. determine whether any named 2003–2004 product manual adopted the stronger recover-if-possible rule before INCITS 405-2005 publication;
4. route a broader SCSI end-to-end-protection / DIF genealogy to `computing-archaeology` if that repository develops the topic;
5. keep product implementation traces separate from normative interface text.

These debts do not block the present conclusion because the slice's explicit goal is to **tighten the direct-text transition window and recover the proposal lineage**, not to claim the exact first incorporated revision.

---

## Result

**Bounded deepening complete.**

The repository can now replace the coarse `2001 → 2005` semantic bracket with a more defensible standards-development sequence:

```text
SBC-2 Rev09 (May 2003)
    older affected-block-data-may-be-altered contract

03-176 / 03-365 proposal work (May–Nov 2003)
    protection information explicitly brought into REASSIGN semantics

SBC-2 Rev13 (Mar 2004)
    associated protection infrastructure known to be present,
    but exact REASSIGN clause not yet directly verified in this pass

SBC-2 Rev16 (13 Nov 2004)
    recoverable user data + protection information must be carried forward
```

The historical distinction to retain is:

> **stable command name ≠ stable repair contract; proposal intent ≠ incorporated normative text; logical-address continuity ≠ guaranteed old-value recovery.**
