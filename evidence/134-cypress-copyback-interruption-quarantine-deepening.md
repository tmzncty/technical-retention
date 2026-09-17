# Case 134 deepening — Cypress SLC NAND copy-back interruption, quarantine, and restart evidence

## Status

**`bounded deepening complete`**

This record deepens Case 134 along a boundary that the 2005–2008 copy-back integrity evidence did not settle:

> What should a host conclude if the **destination-program phase of COPYBACK is interrupted by hardware reset, power failure, or another interruption before normal completion?**

The bounded answer is not “retry the read and trust whatever looks right.” A later Cypress SLC NAND product contract explicitly requires the interrupted page to remain unused for reading or programming until an uninterrupted block erase has completed. A first-party Cypress knowledge-base article generalizes the same program/erase recovery rule: an interrupted Flash location is **untrustworthy even if it appears to contain the intended data**, and the system must retain enough evidence to identify interrupted operations and quarantine/recover the affected location.

This closes a retention-specific gap in Case 134:

```text
source-page integrity qualification
    != destination-program completion
    != interruption recovery qualification
    != higher-level currentness publication
```

It does **not** establish that all NAND copy-back implementations have identical reset semantics, that the source page is physically unchanged by every interrupted sequence, or that an interrupted destination is securely erased.

---

## Research slice

### Included

- Cypress `S34ML01G1 / S34ML02G1 / S34ML04G1` SLC NAND family, document number `002-00676 Rev. *V`, specifically the `Copy Back Program` operation and its interruption rule;
- Cypress/Infineon knowledge-base article **“Recover Flash Devices when Power Failure or Reset Happens During a Program or Erase Operation”**, posted 13 March 2017 and currently carrying a 20 April 2025 update stamp;
- the relation between volatile command execution state and externally retained evidence that an operation began but did not safely complete;
- bounded comparison with Case 145 JFFS2 negative/reuse evidence and Case 146 Flash erase suspend/abort.

### Excluded

- invention priority for NAND COPYBACK;
- complete ONFI/Toggle command genealogy;
- managed-SSD FTL mapping-commit behavior;
- empirical power-cut testing on a named S34ML part;
- exact analog threshold-state distribution after an interrupted program pulse sequence;
- secure sanitization;
- a claim that every reset, brownout, supply ramp, and host crash has identical effects;
- a claim that Cypress’s later product-family contract describes Samsung’s 2005 device behavior retroactively.

---

## Source custody and chronology

### Cypress S34ML01G1-family datasheet — manufacturer-authored product contract, mirrored (`H/P*`)

The inspected searchable copy identifies Cypress Semiconductor as the manufacturer and preserves document number `002-00676 Rev. *V`. The historical document is accessed through a third-party datasheet mirror rather than a current Cypress/Infineon first-party download path, so detailed claims from it are marked `H/P*` rather than pretending present-day first-party custody.

The exact public date of Rev. `*V` is **not claimed in this record**. The evidence is used as a later product-family witness, not as a 2005–2008 priority anchor.

Relevant product-contract statements include:

- COPYBACK is a sequential page-read followed by Copy Back Program to a destination page;
- source data are moved into an internal data register;
- Program Confirm `10h` actually begins destination programming;
- for the 2 Gb / 4 Gb devices, an optional EDC path can detect specified source-page errors;
- if a Copy Back Program operation is interrupted by **hardware reset, power failure, or other means**, the host must ensure that the interrupted page is not used for further reading or programming until the next uninterrupted block erase completes;
- the corresponding multiplane rule quarantines the interrupted pages until uninterrupted block erase completes for the applicable blocks.

This is a manufacturer-authored contract preserved through a mirror, not an independent validation experiment.

### Cypress/Infineon KBA — first-party support guidance (`H/P`)

The first-party Infineon-hosted Cypress knowledge-base article was posted **13 March 2017** and currently shows a **20 April 2025** update stamp. Its topic metadata includes both `Memory: NOR Flash` and `Memory: SLC NAND Flash`.

The article states that a Flash location can be trusted only if every Flash operation affecting that location since the most recent block/sector erase is known to have started and run to completion under continuous power. If a program/erase operation is interrupted, the location is indeterminate and untrustworthy for further read/program use—even if it appears to contain the intended image.

For interrupted program, the article recommends:

1. if source data still exist, program them again **in a new location**;
2. mark the location subjected to interrupted programming as untrustworthy;
3. do not use it for reading or programming until the containing block/sector can be erased again.

It also gives a host-side detection pattern:

```text
persist start marker
    -> perform Flash operation under continuous power
    -> persist completion marker

on restart:
    start marker without completion marker
    -> interrupted-operation evidence
    -> quarantine/recovery action
```

The KBA is broader than COPYBACK. Its value here is as a first-party statement of the **interrupted-program trust rule** and of the need for retained negative-state evidence across restart.

---

## Historical / implementation record

### 1. Copy-back contains a destination-program phase with its own completion boundary

The Cypress SLC NAND family describes COPYBACK as a composition rather than one indivisible semantic event:

```text
source page
    -> Copy Back Read
    -> internal data register
    -> destination address
    -> Program Confirm (10h)
    -> destination programming
    -> completion / status
```

The existing Case 134 grounding already established a different boundary: the source value may itself need integrity checking/correction before relocation. The Cypress record adds a second boundary after the source value has reached the internal register:

> **having a candidate source value in the internal register != having a qualified destination embodiment.**

The destination is not authoritative merely because a COPYBACK sequence was initiated.

### 2. Reset or power failure can turn the destination page into a quarantined location

The product contract is unusually explicit. If Copy Back Program is interrupted by hardware reset, power failure, or another means, the host is instructed not to use the interrupted page for further reading **or programming** until the next uninterrupted block erase completes.

That yields:

```text
program operation started
    + normal completion not established
        -> page cannot be admitted as trustworthy
        -> page cannot be repaired in place merely by another program
        -> block erase is the requalification frontier
```

The vendor rule is stronger than “check whether the bytes look correct.” It is a **trust/admission rule** about the history of the location.

### 3. Apparently correct contents do not cancel interruption history

The 2017 Cypress KBA states the more general rule directly: after an interrupted Flash operation, any stable or unstable data state is possible, including an **apparently correct** image of the intended data.

Therefore:

> **readback resemblance != trustworthy completion evidence.**

and:

> **stable-looking bits != qualified reusable program state.**

The physical observation after restart does not, by itself, reconstruct whether the internal program algorithm crossed its safe completion boundary.

### 4. “No completion record” can itself be retained evidence

Power failure destroys the running command context that would otherwise distinguish `program in progress` from `program completed`. Cypress therefore recommends a higher-level nonvolatile start/finish marking scheme.

This creates a retention relation in which a small negative-state record can govern a much larger physical object:

```text
operation-start evidence
    + absence of matching completion evidence
        -> location is treated as interrupted
        -> location is excluded from read/program admission
        -> later erase can restore reuse eligibility
```

The significance is not that every NAND controller literally implements Cypress’s marker example. It is that **recovery authority may depend on retaining evidence about an unfinished operation after the operation’s volatile execution state has vanished**.

### 5. Quarantine is not sanitization

The rule “do not use until erase” describes **trustworthiness and reuse admission**. It does not prove that the interrupted destination contains no residual charge pattern, that the old value cannot be physically recovered, or that the later block erase meets a secure-sanitization standard.

Thus:

> **quarantined != physically blank**

and:

> **erase required before reuse != secure erase guarantee.**

---

## Engineering reconstruction

### A. Copy-back has at least three independent qualification questions

Case 134 can now be decomposed into three separate checks:

```text
Q1 — source integrity
    Is the value obtained from the source page still the intended protected codeword?

Q2 — destination program completion
    Did the destination program operation reach its documented completion boundary?

Q3 — higher-level currentness
    Did the controller/filesystem publish the destination as the current logical embodiment?
```

A positive answer to any one does not imply the others.

The original Samsung/Micron evidence primarily grounded Q1. This deepening adds a product contract for Q2 and leaves Q3 outside the raw NAND command.

### B. Operation-state persistence can be weaker than recovery-policy persistence

During normal execution, the NAND device has transient state such as internal data-register contents, busy state, and embedded program-control state. A reset/power loss can destroy that transient state.

But safe recovery may require a different piece of state to survive:

```text
volatile execution state disappears
        !=
recovery obligation disappears
```

The host may need to retain the weaker fact:

```text
“this destination was subjected to a program that was not proven complete”
```

That fact is enough to prohibit later use until erase, even though it does not reconstruct the exact analog program progress.

### C. Recovery does not require reconstructing the interrupted analog microstate

The Cypress rule deliberately avoids asking the host to infer where the interrupted programming waveform stopped. The host instead applies a coarse policy:

```text
completion not proven
    -> distrust location
    -> relocate from surviving source if available
    -> erase before location reuse
```

Therefore:

> **exact interrupted-program microstate != required recovery state.**

A system can recover safely by retaining a conservative classification rather than the physical process history in full detail.

### D. “Retry in place” and “retry elsewhere” are different authority decisions

The KBA explicitly rejects relying on same-location reprogramming as the generally provable safe recovery. Its preferred interrupted-program recovery uses a **new location** when source data remain available and quarantines the interrupted location until erase.

Thus:

> **logical payload still recoverable != interrupted physical location reusable.**

This is a direct retention/currentness distinction: the value may survive through another embodiment while the failed candidate embodiment is denied authority.

### E. Destination failure and source failure must remain separate

COPYBACK has a source read and a destination program. The interruption rule is about the page whose program was interrupted. It does **not** justify the stronger claim that the source page is guaranteed electrically untouched by the entire sequence.

The safe bounded statement is:

- destination program completion was not established;
- the destination is quarantined by the vendor contract;
- a still-valid source may permit recovery to a new location;
- source integrity and future source margin still require their own evidence.

---

## Functional comparison — bounded

### Versus Case 145 — JFFS2 CLEANMARKER / negative reuse evidence

Case 145 shows that an erase block that *looks* erased is not necessarily admitted for reuse after an interrupted erase; JFFS2 retains a `CLEANMARKER` relation to qualify reuse.

The Cypress interrupted-program rule has a related but lower-level shape:

```text
apparently readable/programmed physical state
    != trustworthy reusable state
```

In both cases, admission depends on retained evidence about whether a destructive/programming transition completed safely.

This is **functional comparison only**. JFFS2 `CLEANMARKER` is filesystem metadata; Cypress’s product rule concerns Flash-operation history. No implementation genealogy is asserted.

### Versus Case 146 — Flash erase suspend / abort

Case 146 distinguishes a **documented suspended state** that remains resumable while powered from an **aborted/interrupted operation** whose continuation semantics are not preserved across reset/power loss.

Case 134 now adds the NAND copy-back counterpart:

> **interrupted Copy Back Program != suspended Copy Back Program.**

The Cypress rule does not authorize “resume from the interrupted internal pulse position.” It quarantines the destination until erase.

Again, this is a functional boundary, not a claim that the command families share circuitry or history.

### Versus Case 20 — atomicity and durability

An interrupted Flash page being quarantined is not evidence that an NVMe write meets AWUPF all-old/all-new semantics. Raw-NAND program trust, controller mapping publication, and host-interface atomicity are different layers.

The useful comparison is only:

> **lower-layer interruption semantics must not be silently promoted into a stronger upper-layer commit/atomicity guarantee.**

---

## Philosophical interpretation — bounded

The narrow engineering fact is that **material appearance is not always sufficient evidence of technical authority**. A page may read as if it contains the desired value and still be excluded from trusted use because the system lacks evidence that the programming transition completed under the required conditions.

A bounded conceptual formulation is:

> **Retention can depend on preserving the history needed to authorize a state, not only the state’s presently observable bits.**

This is not a claim that physical data require social “belief,” that Flash devices possess memory in a psychological sense, or that every technical state needs a journal. It is simply the engineering distinction between **what is physically observable** and **what the protocol/product contract permits the system to treat as valid/current/reusable**.

---

## Claim ledger

| Claim | Layer | Evidence boundary |
| --- | --- | --- |
| S34ML01G1-family COPYBACK reads a source page into an internal data register and then programs a destination after Program Confirm | `H/P*` | Cypress manufacturer datasheet preserved through mirror |
| the product contract quarantines an interrupted Copy Back Program page until uninterrupted block erase | `H/P*` | exact Cypress datasheet language |
| the corresponding multiplane operation quarantines interrupted pages until applicable blocks are erased | `H/P*` | exact Cypress datasheet language |
| Cypress first-party guidance says interrupted program/erase locations are untrustworthy even when an apparently correct image is observed | `H/P` | 2017 KBA, updated 2025 |
| Cypress recommends a nonvolatile start/finish marking pattern to identify interrupted operations on restart | `H/P` | 2017 KBA |
| the exact analog state of an interrupted NAND page can be reconstructed from those markers | `X` | not claimed; markers classify the operation history |
| an interrupted destination is necessarily all-0, all-1, or visibly corrupt | `X` | explicitly contradicted by KBA’s “apparently correct” possibility |
| Copy Back interruption proves source page corruption | `X` | source integrity requires separate evidence |
| quarantine until erase is a secure-sanitization guarantee | `X` | reuse/trust rule only |
| later Cypress semantics apply retroactively to Samsung’s 2005 device | `X` | cross-product chronology not established |
| safe recovery can retain a coarse interrupted/not-completed classification instead of exact internal program progress | `E` | engineering reconstruction of vendor-prescribed quarantine/recovery |
| negative operation-history evidence can remain authoritative after volatile command state disappears | `E` | bounded reconstruction of start/finish marker guidance |

---

## Explicit non-claims / stop conditions

1. No claim that Cypress invented COPYBACK.
2. No claim that Rev. `*V` is the earliest public statement of the interruption rule.
3. No claim that the mirrored datasheet has current first-party web custody.
4. No claim that every SLC/MLC/TLC/3-D NAND family shares this exact rule.
5. No claim that every hardware reset and every power-failure waveform produces identical cell states.
6. No claim that the source page is perfectly unchanged by COPYBACK or by the read used to seed it.
7. No claim that an interrupted destination is definitely corrupt when read.
8. No claim that apparently correct readback establishes safe completion.
9. No claim that the interrupted page can be safely reprogrammed in place.
10. No claim that block erase securely sanitizes prior data.
11. No claim that raw NAND COPYBACK commits an FTL mapping update.
12. No claim that the KBA’s marker recipe is implemented inside the S34ML device.
13. No claim that every flash filesystem uses the exact marker scheme described by Cypress.
14. No claim that JFFS2 CLEANMARKER and Cypress operation markers are the same data structure.
15. No claim that an interrupted COPYBACK provides NVMe-style atomic-write semantics.
16. No claim that product pass/fail status is itself power-fail-persistent.
17. No claim that host restart alone, without NAND reset/power interruption, necessarily invalidates the same state.
18. No claim that exact internal programming progress must be persisted for safe recovery.
19. No claim that quarantine proves physical unreadability.
20. No claim that this slice closes the broad ONFI/Toggle/managed-NAND genealogy.

---

## Relation to existing Case 134 evidence

The original grounding established:

```text
physical relocation
    != source integrity revalidation
    != restored ECC margin
```

This deepening adds:

```text
COPYBACK initiated
    != destination program proven complete

apparently correct destination bits
    != trustworthy destination

volatile command state lost
    != recovery obligation lost

interrupted destination quarantined
    != logical payload unrecoverable elsewhere
```

Together, the case now has two independent ways for “a copied page exists” to fail as a sufficient retention claim:

1. **content problem:** the source codeword can be copied with pre-existing error unless checked/corrected;
2. **transition problem:** the destination programming transition can be interrupted and leave a page that must not be trusted even if it appears correct.

The higher-level mapping/currentness publication boundary remains open.

---

## Related-repository check

A fresh search of `tmzncty/computing-archaeology` for `copyback NAND` returned no dedicated packet to reuse. The broader history of NAND COPYBACK commands, manufacturer adoption, ONFI/Toggle standardization, and controller architectures therefore remains outside this file. If developed, that history should live primarily in `computing-archaeology`; `technical-retention` keeps the narrower **interruption -> trust/quarantine -> recovery evidence** seam.

---

## Remaining evidence debt

- locate an earlier, directly first-party-hosted Cypress/Spansion revision that preserves the exact COPYBACK interruption wording and pins its public date;
- determine whether the interruption/quarantine language can be traced into an ONFI normative requirement or is vendor-specific product policy;
- inspect any available S34ML application note or controller integration guide showing how host software records/quarantines an interrupted destination;
- find independent power-cut/fault-injection validation for a named raw-NAND device rather than treating the datasheet contract as measured behavior;
- study managed-NAND/SSD currentness publication separately: when does a copied destination become the authoritative logical page, and what evidence survives controller restart?;
- keep source-page read-disturb/error qualification separate from destination-program interruption.

None of these debts blocks the bounded conclusion of this record.

---

## Sources

### Cypress SLC NAND product documentation — manufacturer primary, mirrored (`H/P*`)

- Cypress Semiconductor, `S34ML01G1 / S34ML02G1 / S34ML04G1`, **1 Gb/2 Gb/4 Gb, 3 V, SLC NAND Flash for Embedded**, Document Number `002-00676 Rev. *V`; searchable mirror page showing the COPYBACK sequence: <https://www.alldatasheet.com/html-pdf/1044507/CYPRESS/S34ML01G1/6311/18/S34ML01G1.html>.
- Mirror/search extract preserving the next-page interruption and EDC text for Rev. `*V`: <https://www.ic-components.it/files/15/S34ML02G100BHI000.pdf>.

### Cypress/Infineon first-party support guidance (`H/P`)

- Cypress Semiconductor / Infineon Developer Community, **“Recover Flash Devices when Power Failure or Reset Happens During a Program or Erase Operation,”** posted 13 Mar 2017; current page updated 20 Apr 2025: <https://community.infineon.com/t5/Knowledge-Base-Articles/Recover-Flash-Devices-when-Power-Failure-or-Reset-Happens-During-a-Program-or/ta-p/248567>.

### Existing Case 134 grounding

- [`134-2005-2008-nand-copyback-integrity-grounding.md`](134-2005-2008-nand-copyback-integrity-grounding.md) — Samsung 2005 product warning, 2006 published EDC patent record, and Micron 2008 correction/requalification note.

### Cross-case comparison anchors

- [`../cases/145-jffs2-garbage-collection-negative-state-evidence.md`](../cases/145-jffs2-garbage-collection-negative-state-evidence.md) — negative/reuse evidence after destructive Flash transitions.
- [`../cases/146-flash-erase-suspend-pending-operation-state.md`](../cases/146-flash-erase-suspend-pending-operation-state.md) — powered suspend/resume versus reset/power-loss abort.
- [`../cases/20-nvme-atomicity-versus-durability.md`](../cases/20-nvme-atomicity-versus-durability.md) — upper-layer atomicity/durability contract kept separate from raw-media interruption behavior.

---

## Bounded result

The strongest safe result is:

> **NAND COPYBACK can fail retention qualification in two independent ways: the source value may be copied without sufficient integrity revalidation, and the destination programming transition may be interrupted without reaching a trustworthy completion boundary. A later Cypress SLC NAND product contract requires an interrupted COPYBACK destination to remain quarantined until uninterrupted block erase, while Cypress first-party recovery guidance explicitly warns that even apparently correct post-interruption bits are not sufficient evidence of trustworthiness. Safe restart therefore may depend on retained evidence that a destructive/programming operation began but was not proven complete, rather than on preserving the exact internal operation state.**

That result is intentionally narrower than a general claim about all NAND, SSD FTLs, or power-fail atomicity.