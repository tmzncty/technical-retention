# Case 136 Deepening — LSI MegaRAID FlexRAID PowerFail and Cross-Restart Maintenance Continuation (2006)

## Status

**`bounded deepening complete`**.

This addendum closes one narrow evidence gap left by the base Case 136 record: the 2006 LSI manual does more than say that a rebuild starts again after a reboot. It exposes a named, configurable **`FlexRAID PowerFail`** controller feature for carrying selected maintenance work across power failure / reset boundaries.

The bounded question is:

> When a RAID controller is interrupted during maintenance, what did LSI actually promise would continue after restart, and how much retained progress can safely be inferred from that promise?

The answer is deliberately narrower than “MegaRAID has a durable rebuild checkpoint.” The inspected first-party manual establishes **maintenance-task continuation / re-entry**, but it does not disclose the exact persisted progress representation or prove resume from the exact prior stripe offset.

---

## Source set

### Primary source

LSI Logic Corporation, **_MegaRAID Configuration Software User's Guide_**, Version 2.0, document `DB15-000269-01`, Second Edition, March 2006, currently hosted by Broadcom:

- https://docs.broadcom.com/doc/12353347

The title page identifies March 2006 and the document as LSI's official reference for the described MegaRAID software tools. The internal revision-history table labels Version 2.0 as February 2006 while the title/copyright page says March 2006. This addendum therefore cites the document as the **March 2006 Second Edition** and does not turn the revision-history month discrepancy into a publication-priority claim.

Relevant locators:

- §2.4.13, `Disk Rebuilds`, printed p. 2-11 / PDF p. 32;
- BIOS Configuration Utility Adapter submenu, printed p. 3-7 / PDF p. 54;
- WebBIOS Adapter Properties, printed p. 4-7 / PDF p. 90.

A fresh search of `tmzncty/computing-archaeology` for `MegaRAID` returned no dedicated overlapping study in this round.

---

## Historical record

### H/P — ordinary rebuild documentation already promises post-reboot re-entry

In §2.4.13 the manual says that if the system goes down during a rebuild, the RAID controller automatically restarts the rebuild after the system reboots.

This is direct product documentation for continuity of the rebuild obligation / activity across a system interruption.

It supports:

> **an interrupted rebuild can be automatically re-entered after reboot.**

It does not, by itself, support:

> **the controller resumes at the exact previous physical reconstruction offset.**

The verb `restarts` is not a disclosed checkpoint format.

### H/P — BIOS CU exposes `FlexRAID PowerFail` as a configurable feature

The BIOS Configuration Utility Adapter submenu separately lists **`FlexRAID PowerFail`** and describes it as the option that allows drive reconstruction to continue when the system restarts after a power failure.

This is stronger than treating cross-reboot continuation as an invisible universal property of RAID reconstruction. In the inspected management surface, continuation is represented as an explicit controller feature that can be enabled.

Therefore:

> **repair possibility != configured cross-power repair continuation.**

The manual does not disclose the exact storage location of the feature bit or the reconstruction-progress state that makes continuation possible.

### H/P — WebBIOS broadens both the maintenance class and the interruption class

The WebBIOS Adapter Properties table gives a more explicit description. `FlexRAID PowerFail` allows:

- drive reconstruction;
- rebuild;
- check consistency

...to continue when the system restarts after:

- a power failure;
- a reset;
- a hard boot.

The same table says the default is **Enabled**.

This yields two historically grounded boundaries.

First, the feature is not described only as a failed-member rebuild mechanism. It also covers a verification / corrective-maintenance class (`check consistency`).

Second, the feature's documented interruption domain is broader than literal removal of input power; WebBIOS explicitly includes reset and hard boot.

So:

> **`PowerFail` product label != power-removal-only interruption semantics.**

and:

> **cross-restart maintenance continuation != rebuild-only continuation.**

### H/P — `Enabled` by default does not make the policy concept disappear

The WebBIOS table says `FlexRAID PowerFail` defaults to Enabled. A default-on feature is still a separately represented controller policy in the documented management interface.

Therefore the historical record supports:

> **default-enabled continuation != continuation having no independently configurable policy state.**

This addendum does not claim that every controller supported disabling it, every firmware release used the same default, or every later MegaRAID/PERC generation retained this exact option name.

---

## Engineering reconstruction

### E — maintenance obligation, continuation policy, and progress checkpoint are different retained objects

The 2006 manual makes it useful to split an interrupted rebuild into at least three conceptual layers:

```text
failed-member / maintenance condition
        -> repair or verification obligation exists
        -> maintenance task begins
        -> interruption

controller continuation policy
        -> FlexRAID PowerFail enabled?

post-restart maintenance behavior
        -> task is re-entered / allowed to continue
        -> maintenance eventually completes
```

The source does **not** expose a fourth layer in enough detail to characterize it:

```text
exact physical progress checkpoint
        -> stripe / LBA / extent offset?
        -> bitmap?
        -> percentage?
        -> reconstructed work replay window?
```

Accordingly:

> **retained maintenance obligation != retained continuation policy != demonstrated exact progress checkpoint.**

### E — task identity can survive more strongly than exact work position

A controller can know after restart that reconstruction, rebuild, or consistency checking should continue without the source proving that every unit of already completed work is remembered exactly.

The safest project term is **maintenance-task continuity**.

It means only that the controller re-enters the relevant maintenance regime across the documented interruption. It does not mean exactly-once execution.

Thus:

> **maintenance-task continuity != exactly-once maintenance.**

and:

> **resume/restart of an operation class != zero repeated work.**

### E — repair scheduling policy and interruption-continuation policy are orthogonal controls

Case 136 already grounds a separate `Rebuild Rate` setting. The same WebBIOS table presents `Rebuild Rate` and `FlexRAID PowerFail` as different adapter properties.

This directly motivates a two-axis decomposition:

```text
axis A — while the task is running:
    how aggressively does it compete for resources?
    -> Rebuild Rate

axis B — after an interruption:
    should the maintenance regime continue after restart?
    -> FlexRAID PowerFail
```

Therefore:

> **maintenance priority != maintenance restart continuity.**

A controller can retain both kinds of policy without the two properties being the same state.

### E — verification continuation and repair continuation are not the same maintenance semantics

`check consistency` is not identical to reconstructing a missing member. The former verifies/corrects a redundancy relation; the latter recreates a failed member's contribution.

The fact that one controller feature spans both does not erase the distinction among their state machines.

> **shared interruption-continuation policy != identical maintenance task.**

### E — “continue” is not enough to infer a persistence medium

The manual documents behavior, not the implementation substrate. It does not say whether the relevant continuation information lives in:

- controller NVRAM;
- on-disk RAID metadata;
- battery-backed / flash-backed controller state;
- a combination of controller and disk metadata;
- another implementation-specific representation.

Therefore:

> **behavior survives restart != source identifies where its control state is physically retained.**

This addendum deliberately refuses to fill that gap by analogy with other MegaRAID metadata.

---

## Interruption matrix

The WebBIOS wording supports the following bounded matrix.

| Interruption / task | Reconstruction | Rebuild | Check consistency | Exact progress checkpoint proven? |
| --- | --- | --- | --- | --- |
| power failure + restart | documented continuation | documented continuation | documented continuation | **No** |
| reset + restart | documented continuation | documented continuation | documented continuation | **No** |
| hard boot + restart | documented continuation | documented continuation | documented continuation | **No** |
| orderly stop/abort by operator | not established by this slice | not established by this slice | not established by this slice | **No** |
| controller replacement | not established | not established | not established | **No** |
| loss/corruption of controller metadata | not established | not established | not established | **No** |

The table is intentionally conservative. The manual's advertised restart behavior should not be extrapolated into controller replacement, arbitrary metadata corruption, or every operator-initiated stop state.

---

## Functional comparisons — not genealogy

### A — Case 83, HDFS BlockScanner cursor checkpointing

Case 83 exposes a maintenance traversal whose saved cursor can reduce repeated work after restart, while missing/unreadable cursor state falls back to a fresh iterator.

The MegaRAID record is different: the first-party manual exposes a controller policy for continuing maintenance across restart but does not expose the exact progress representation.

The useful comparison is only:

> **both systems distinguish maintenance work from the control state that determines what happens after interruption.**

Do not infer shared implementation, checkpoint format, or lineage.

### A — Case 148, NVMe Device Self-test

NVMe Case 148 separates a background diagnostic operation, reset/power behavior, current progress, and result history at a standardized interface.

MegaRAID's 2006 `FlexRAID PowerFail` predates that interface case and belongs to a RAID-controller-specific management regime. The functional analogy is that maintenance may be explicitly specified to survive selected interruption classes.

This is not a prior-art claim against NVMe Device Self-test and not evidence of genealogy.

### A — Case 17, RAID reconstruction

Case 17 establishes the underlying `degraded -> reconstruct -> restored redundancy` relation. This addendum inserts an interruption boundary inside that repair process:

```text
degraded array
    -> rebuild in progress
    -> power failure / reset / hard boot
    -> controller restart
    -> maintenance task continues
    -> redundancy restoration can proceed
```

It does not strengthen the claim about exact progress persistence.

---

## Philosophical interpretation — bounded

The modest retention result is that a maintenance process can possess **continuity as an obligation or task identity** even when its exact micro-progress is not historically visible to us.

That permits a narrow statement:

> technical continuation can depend on retaining enough control relation to say “this unfinished work still belongs to the restarted system.”

This is project interpretation, not LSI vocabulary. It does not imply that a controller has autobiographical memory, and it does not turn every restartable operation into the same philosophical object.

---

## Explicit non-claims

This slice does **not** claim that:

1. LSI invented cross-reboot rebuild continuation;
2. March 2006 is the first implementation or first public use of `FlexRAID PowerFail`;
3. the February/March date discrepancy in the manual proves two separate public editions;
4. `FlexRAID PowerFail` is present under the same name on every MegaRAID/PERC generation;
5. `Enabled` by default means the setting cannot be disabled;
6. `continue` proves exact resume from the previous stripe/LBA;
7. no rebuild work is repeated after interruption;
8. the progress checkpoint is stored in NVRAM;
9. the progress checkpoint is stored on member disks;
10. controller configuration and progress state have the same persistence horizon;
11. `Rebuild Rate` controls whether cross-restart continuation occurs;
12. `FlexRAID PowerFail` determines rebuild bandwidth or priority;
13. reconstruction, rebuild, and consistency check are identical operations;
14. automatic task continuation proves successful maintenance completion;
15. restart continuity proves every source sector remains readable;
16. restart continuity proves payload integrity;
17. a reboot is equivalent to controller replacement;
18. a hard boot is equivalent to arbitrary sudden hardware destruction;
19. the controller survives every metadata-corruption scenario;
20. the source is a controlled power-cut fault-injection test.

---

## Prior-art boundary

The defensible historical floor is narrow:

> By the March 2006 LSI MegaRAID Configuration Software manual, a named `FlexRAID PowerFail` management property explicitly governed continuation of reconstruction/rebuild/check-consistency work across documented restart classes, and WebBIOS documented the property as enabled by default.

This establishes a public vendor implementation/management concept by that date. It does **not** establish invention priority for persistent maintenance tasks, RAID rebuild checkpoints, power-fail recovery, or consistency-check continuation.

Broader pre-2006 RAID-controller genealogy belongs in `tmzncty/computing-archaeology` if developed.

---

## Claim ledger

| Claim | Type | Evidence status |
| --- | --- | --- |
| LSI 2006 says an interrupted rebuild is automatically restarted after system reboot | H/P | direct manufacturer manual |
| LSI 2006 exposes a named configurable `FlexRAID PowerFail` property | H/P | direct BIOS CU / WebBIOS tables |
| WebBIOS says the property covers reconstruction, rebuild, and check consistency | H/P | direct manufacturer manual |
| WebBIOS says the covered restart classes include power failure, reset, and hard boot | H/P | direct manufacturer manual |
| WebBIOS says the property defaults to Enabled | H/P | direct manufacturer manual |
| maintenance priority (`Rebuild Rate`) and restart continuity (`FlexRAID PowerFail`) are separate properties | E grounded in H/P layout | strong bounded reconstruction |
| task continuity != exact progress checkpoint persistence | E/X | explicit source limit |
| restart behavior proves a specific NVRAM/on-disk persistence representation | X | unsupported |
| all three maintenance tasks share the same internal state machine | X | unsupported |
| March 2006 is invention priority | X | unsupported |

---

## Remaining evidence debt

This slice closes the **named cross-restart continuation-policy** gap for the bounded 2006 MegaRAID management regime. It leaves open:

- exact progress representation and persistence location;
- whether rebuild restarts at an exact prior stripe/extent or replays a bounded region;
- behavior if progress metadata itself is corrupt;
- persistence/reset semantics when `FlexRAID PowerFail` is disabled and later re-enabled;
- controller-replacement behavior;
- exact feature genealogy before 2006;
- later MegaRAID/PERC evolution and removal/renaming of the feature;
- controlled power-cut fault injection proving progress continuity rather than only task re-entry.

Those remain separate research slices rather than assumptions hidden inside the word `continue`.
