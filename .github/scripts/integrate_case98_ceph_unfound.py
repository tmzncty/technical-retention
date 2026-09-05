from pathlib import Path

ROOT = Path('.')


def insert_after_unique_line(path: str, needle: str, block: str) -> None:
    p = ROOT / path
    lines = p.read_text(encoding='utf-8').splitlines()
    matches = [i for i, line in enumerate(lines) if needle in line]
    if len(matches) != 1:
        raise SystemExit(f'{path}: expected one line containing {needle!r}, found {len(matches)}')
    i = matches[0]
    addition = block.rstrip('\n').splitlines()
    lines[i + 1:i + 1] = addition
    p.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def replace_unique_line(path: str, needle: str, replacement: str) -> None:
    p = ROOT / path
    lines = p.read_text(encoding='utf-8').splitlines()
    matches = [i for i, line in enumerate(lines) if needle in line]
    if len(matches) != 1:
        raise SystemExit(f'{path}: expected one line containing {needle!r}, found {len(matches)}')
    lines[matches[0]] = replacement
    p.write_text('\n'.join(lines) + '\n', encoding='utf-8')


case = r'''# Ceph Unfound Objects: Retained Version Knowledge, Recovery Exhaustion, and Administrative Loss

**Status:** `grounded`

## Scope

- **Object / system:** Ceph/RADOS placement-group recovery, specifically the `unfound` → explicit `lost` transition.
- **Date range:** 2010–2014 implementation and operator-interface evidence, with the 2006 RADOS design retained as same-system background rather than rewritten here.
- **Institution / project:** Ceph open-source project; New Dream Network / Inktank-era source history.
- **Retention question:** what remains retained when the system still knows that a newer object version should exist, yet cannot locate any recoverable embodiment of that version?

This is not a second generic RADOS replication case. [`Case 05`](05-rados-replicated-object-repair.md) already grounds ordinary 2006 placement, primary-copy versioning, peering, and repair when enough current state survives. Case 98 starts at the failure boundary Case 05 leaves open:

> **the protocol can retain evidence that a required newer version exists after it has lost the payload needed to realize that version.**

The bounded historical path then asks when Ceph is allowed to stop searching, when `unfound` becomes `lost`, and what `revert` or `delete` means for the current logical object.

---

## Historical vocabulary

The source history itself supplies the important terms:

- `unfound`;
- `lost`;
- `might_have_unfound`;
- `Missing`;
- `past_intervals`;
- `last_epoch_clean`;
- `mark_unfound_lost`;
- `revert`;
- later, `delete`;
- placement group / `PG`;
- primary OSD.

These terms are historical Ceph implementation/operator vocabulary. Project terms such as **retained existence claim**, **search-space exhaustion**, **recovery obligation**, and **administrative forgetting authority** are engineering reconstructions used to compare this mechanism with other retention regimes.

Do not retroactively project the 2014 `delete` option onto the 2010–2012 interface. In February 2012, the inspected command path explicitly supported `revert` while saying `mark` and `delete` were not yet implemented.

---

## Retained state

The interesting retained state is not only object bytes.

During the bounded recovery path, Ceph can retain enough control/history state to know that:

1. an object/version is missing from the primary's currently available material;
2. one or more historical OSDs might still contain the needed version;
3. those candidates should be queried before the unresolved version is abandoned;
4. the object remains unresolved even if none of the queried candidates yields the payload.

The 23 November 2010 source change creates a primary-only recovery set named `might_have_unfound`. It derives candidate OSDs from historical acting intervals that might have been read/write since `last_epoch_clean`, and removes candidates as missing-state responses arrive.

That gives a sharp retention distinction:

> **knowledge that a newer/current version should exist ≠ retention of the bytes that instantiate that version.**

A system may retain a *claim about absent state* strongly enough to keep searching for it.

---

## Logical / physical substrate

The unresolved logical object is represented through several different kinds of state:

- surviving object versions on OSDs, if any;
- missing/version information in the PG recovery structures;
- OSD-map membership and loss state;
- historical acting intervals used to identify candidate sources;
- primary authority for deciding recovery progress;
- later operator command state authorizing a transition from unresolved recovery to `lost` handling.

The important point is relational. A candidate OSD is not itself the missing object; a record that an OSD *might* contain the object is a retained recovery relation.

Likewise, exhausting known candidates does not physically erase any unidentified media that might exist elsewhere. It establishes a bounded protocol fact: **the recovery process has no remaining admissible known source in the set it is prepared to search.**

---

## Retention mechanism

### Historical record: building a recovery search set

Commit `846122866db607e5af7409228c0f3d715e781ddc` (23 November 2010), **“Build might_have_unfound set at activation,”** adds `build_might_have_unfound()`.

The code walks `past_intervals` backward, stops once intervals predate `last_epoch_clean`, ignores intervals that did not `maybe_went_rw`, and inserts OSDs from relevant historical acting sets into `might_have_unfound`. The commit message describes the set as tracking OSDs that might contain unfound objects needed by the primary; as `Missing` information arrives, OSDs are removed from that set.

**Engineering reconstruction:** historical placement/authority metadata can preserve a *future recovery search space*. The payload may be unavailable now, yet retained history tells the system where it is still obligated to look.

### Historical record: automatic loss was deliberately replaced by explicit operator authority

The same November 2010 commit describes an intended automatic transition to `LOST` once `might_have_unfound` is empty and the latest version had resided on an OSD already marked lost.

Commit `ce04e3dbaf2383a521b267585a860f772c4cc786` (24 May 2011), **“osd: add ability to explicitly mark unfound as lost,”** changes that policy. Its commit message says Ceph should not automatically mark such objects lost merely after trying every location; instead an administrator must explicitly request the transition. The stated reasons are to avoid incorrectly marking data lost during peering problems and to let the administrator decide whether offline OSDs are worth bringing back.

This is the central bounded finding:

> **repair/search exhaustion ≠ automatic authority to forget.**

The operator can deliberately keep an unresolved recovery obligation alive because a currently offline embodiment may still be worth recovering.

---

## Addressing and recovery geometry

Case 05 shows ordinary object → PG → current OSD placement. Case 98 adds a historical dimension.

For unfound recovery, the relevant question is not only:

```text
where should this object be now?
```

but also:

```text
which OSDs participated in relevant past acting intervals
since the last known-clean boundary and therefore might still
hold the missing version?
```

The 2010 implementation uses `past_intervals` and `last_epoch_clean` to bound that search.

**Engineering reconstruction:** recovery addressing can include *historical candidate location*, not only current placement. Old topology state can remain operationally useful because it tells the future system where a lost current embodiment might still be found.

This must not be expanded into a claim that Ceph retains a complete per-object placement history. The inspected mechanism is PG/recovery scoped and deliberately bounded.

---

## Read / service semantics

Current Ceph documentation still describes `unfound` as a state in which the cluster knows that an object or newer copy should exist but cannot find a copy, and it distinguishes `recovery_unfound` / `backfill_unfound` from clean recovery completion.

For this case, the important retention boundary is:

> **temporary inability to return the required current state ≠ permission to silently substitute any stale state.**

The recovery process can therefore preserve semantic caution by refusing to collapse unresolved currentness into an apparently successful stale answer.

This is an engineering comparison, not a claim that every Ceph release blocks exactly the same I/O classes in exactly the same way. Release-specific service behavior remains separate archaeology.

---

## Write, rollback, and deletion semantics

### 2012: `revert`

Commit `c9416e6184905501159e96115f734bdf65a74d28` (24 February 2012) documents the PG command:

`ceph pg <pgid> mark_unfound_lost revert`

The associated documentation says the operation reverts lost objects to a prior state: a previous version when available, or deletion when the missing value was a newly created object with no prior version. The command path also refuses to proceed if the PG is not primary, if nothing is unfound, or if not all candidate sources have been queried or declared lost.

Thus:

> **revert ≠ reconstruction of the missing newest version.**

It changes which surviving state the system is willing to treat as the admissible continuation after recovery of the newest state has been abandoned.

### 2014: `delete` becomes a distinct option

Commit `245923e704ac3a6262499f26c7a879811edea5b4` (22 April 2014) expands the command to `revert|delete` and explicitly requires `delete` for erasure-coded pools in that implementation because revert was described as difficult for EC pools at the time.

Commit `9fac072380fd357be23e154fc878bbf485af567e` (31 August 2014) updates Ceph documentation to distinguish the two choices: `delete` forgets the lost object, while `revert` returns to a previous version when possible and otherwise forgets a newly created object. The documentation warns that this can confuse applications that expected the object to exist.

This gives three separate transitions:

1. **recover** the missing current version if a candidate source yields it;
2. **revert** authority to an older surviving version when the newest cannot be recovered;
3. **delete** the unresolved object state when the operator elects to abandon it.

None of those is evidence of secure physical erasure.

---

## Time

This case has no single medium-retention deadline comparable to DRAM `tREFI`.

Its relevant timescales are protocol and operational:

- how long historical candidate locations remain useful;
- how long candidate OSDs stay offline before an operator gives up on them;
- how long a PG remains in unresolved recovery;
- when administrator judgment changes from **keep searching** to **declare lost**;
- when a reverted/deleted state becomes the new admitted logical continuation.

The time boundary is therefore partly socio-technical. The 2011 change explicitly moves the final abandonment decision from automatic exhaustion to administrator choice.

---

## Maintenance and labor

The bounded mechanism makes operator labor visible at the exact point automatic self-healing stops being sufficient.

Automatic work includes:

- retaining missing/version information;
- reconstructing candidate OSDs from past intervals;
- probing candidate sources;
- maintaining PG/OSD-map recovery state;
- ordinary peering and recovery when payload is found.

Human/operator work can include:

- deciding whether an offline OSD is worth reviving;
- distinguishing a genuine lost-data condition from a peering/reachability problem;
- choosing whether to abandon the newest version;
- choosing the supported `revert`/`delete` loss policy for the relevant release/pool type;
- accepting application-visible consequences of rollback or deletion.

So `self-healing` does not erase the need for judgment. It can postpone judgment until the protocol no longer has enough material to complete repair automatically.

---

## Failure / forgetting modes

### 1. Payload loss with surviving existence/currentness evidence

The system retains evidence that a required version should exist but lacks a recoverable copy of its bytes.

### 2. Candidate-location loss or exhaustion

Historical placement state can identify candidate OSDs, but candidates may be unavailable, declared lost, or may not contain the needed version.

### 3. Recovery ambiguity

A peering/reachability problem can make automatic declaration of loss unsafe. This is the explicit motivation for the 2011 administrator gate.

### 4. Administrative rollback

The missing newest version is abandoned and an older surviving version becomes the admitted continuation.

### 5. Administrative deletion

The unresolved object is logically retired. This is not a secure-media-erasure claim.

### 6. Application-contract break

The 2014 documentation explicitly warns that forced loss handling can confuse applications that expected the object to exist. Storage-level convergence after forced loss does not imply the application-level state remains semantically valid.

---

## Historical record

The central historical claims are directly grounded by Ceph's own source and documentation history:

- **2010-11-23:** `might_have_unfound` builds a candidate recovery set from past acting intervals and missing-state exchange;
- **2011-05-24:** automatic marking is replaced by explicit administrator action because peering/offline-OSD uncertainty can make automatic loss declaration wrong;
- **2012-02-24:** `mark_unfound_lost revert` is documented and guarded by primary/source-probing checks; later `delete` support must not be backdated;
- **2014-04-22:** `delete` is enabled as a separate loss mode, including the then-specific EC-pool boundary;
- **2014-08-31:** project documentation explicitly distinguishes delete from revert and warns about application expectations.

The full evidence ledger is [`../evidence/98-ceph-2010-2014-unfound-lost-grounding.md`](../evidence/98-ceph-2010-2014-unfound-lost-grounding.md).

---

## Engineering reconstruction

The grounded source history supports these project-level conclusions:

1. **retained currentness evidence can outlive retained payload**;
2. **historical placement metadata can preserve an unresolved recovery obligation**;
3. **all known candidate sources exhausted ≠ logical forgetting**;
4. **unfound ≠ lost**;
5. **lost ≠ physically erased**;
6. **repair exhaustion ≠ automatic authority to forget**;
7. **operator authority can be constitutive of a distributed forgetting transition**;
8. **rollback to an older version ≠ recovery of the missing newest version**;
9. **service refusal/unavailability ≠ forgetting**;
10. **forced storage-level convergence ≠ restored application semantics**.

These are engineering reconstructions. Ceph developers did not formulate them as a general philosophy of technical retention.

---

## Philosophical / media-theoretical interpretation

A useful but bounded conceptual result is that technical systems can retain not only positive payload but also an **obligation toward a missing state**.

The system can continue to say, in effect:

> a newer state counts as the one we owe, even though we cannot currently instantiate it.

That relation matters because forgetting occurs only later, when recovery authority is explicitly changed: either an older state is admitted again or the unresolved object is abandoned.

This sharpens the repository's forgetting thesis:

> **forgetting can be the retirement of a claim about what should count, not merely the destruction of a physical inscription.**

Boundary: this is a philosophical interpretation of the grounded protocol relation. It is not Ceph's historical vocabulary, and it should not be universalized to every missing file or every distributed system.

---

## Functional analogies

- **Case 05 RADOS repair:** same project, earlier ordinary-repair baseline. Case 98 begins where enough current payload no longer survives for ordinary repair.
- **Case 23 Dynamo:** both retain version/currentness relations, but Dynamo's bounded problem is concurrent/admissible versions and reconciliation; Case 98 is a known-needed version with no recoverable embodiment.
- **Case 41 Cassandra tombstones:** both can retain non-payload evidence that controls what state may count, but a tombstone suppresses stale positive state while `unfound` preserves an unresolved recovery claim.
- **Case 90 Kafka leader-epoch truncation:** both can authorize retreat from a physically/symbolically longer apparent history, but Kafka's safe truncation has a different log-lineage mechanism and is not a Ceph genealogy.

These comparisons are functional, not historical lineage claims.

---

## Counterexamples and limits

1. **`unfound = physically absent everywhere` is too strong.** The protocol has exhausted the candidate sources it knows and trusts enough to search; that is not a forensic theorem about every possible medium copy.
2. **`unfound = forgotten` is false.** The very state exists because Ceph still remembers an unresolved object/version claim.
3. **`lost = securely erased` is false.** Revert/delete change logical authority; they do not establish media sanitization.
4. **`revert = recover newest data` is false.** Revert deliberately admits an earlier value or absence after newest-version recovery has failed.
5. **`all Ceph releases have identical loss commands` is false.** 2012 and 2014 source explicitly differ.
6. **`administrator action proves human-only recovery` is false.** Most search/peering/recovery work is automatic; human judgment appears at the abandonment boundary.
7. **`Ceph invented rollback, replication recovery, or operator-directed data loss` is unsupported.** This case establishes a Ceph-specific 2010–2014 implementation history, not invention priority.
8. **current Ceph documentation ≠ contemporaneous proof of 2010 behavior.** Current docs are used only as continuity/context; historical claims are anchored in dated repository artifacts.

---

## Related repositories

A repository search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Ceph` / `Ceph unfound` returned no dedicated matching technical-history module during this research pass. Therefore this file keeps only the retention-specific recovery/forgetting relation.

If a broader Ceph/PG/peering implementation history is built later, it belongs primarily in `computing-archaeology`; this case should link it rather than duplicate it.

---

## Sources

Primary implementation / project history:

- Ceph commit `846122866db607e5af7409228c0f3d715e781ddc`, **“Build might_have_unfound set at activation,”** 23 November 2010: https://github.com/ceph/ceph/commit/846122866db607e5af7409228c0f3d715e781ddc
- Ceph commit `ce04e3dbaf2383a521b267585a860f772c4cc786`, **“osd: add ability to explicitly mark unfound as lost,”** 24 May 2011: https://github.com/ceph/ceph/commit/ce04e3dbaf2383a521b267585a860f772c4cc786
- Ceph commit `c9416e6184905501159e96115f734bdf65a74d28`, **`mark_unfound_lost revert` interface move**, 24 February 2012: https://github.com/ceph/ceph/commit/c9416e6184905501159e96115f734bdf65a74d28
- Ceph commit `245923e704ac3a6262499f26c7a879811edea5b4`, **enable `mark_unfound_lost delete` for EC pools**, 22 April 2014: https://github.com/ceph/ceph/commit/245923e704ac3a6262499f26c7a879811edea5b4
- Ceph commit `95d0278dcfebf77f8548ab7683ce7420302a0443`, local-copy deletion implementation detail, 21 April 2014: https://github.com/ceph/ceph/commit/95d0278dcfebf77f8548ab7683ce7420302a0443
- Ceph commit `9fac072380fd357be23e154fc878bbf485af567e`, **documentation for revert/delete loss handling**, 31 August 2014: https://github.com/ceph/ceph/commit/9fac072380fd357be23e154fc878bbf485af567e

Current official documentation, used only as continuity/context:

- Ceph, “Placement Groups,” section **Reverting Lost RADOS Objects**: https://docs.ceph.com/en/latest/rados/operations/placement-groups/
- Ceph, “Troubleshooting PGs,” including current `unfound` / recovery-state descriptions: https://docs.ceph.com/en/latest/rados/troubleshooting/troubleshooting-pg/

Same-system earlier design background:

- [`Case 05`](05-rados-replicated-object-repair.md) and [`Evidence 05`](../evidence/05-rados-2006-2007-grounding.md), grounded from Weil et al., OSDI 2006 and CRUSH SC 2006.
'''


evidence = r'''# Ceph 2010–2014 unfound / lost grounding record

This record grounds [`Case 98`](../cases/98-ceph-unfound-recovery-exhaustion-administrative-loss.md).

**Status:** `grounded evidence record`

## Grounding question

Case 05 already establishes the normal 2006 RADOS relation among placement, versions, primary authority, peering, and replica repair. This evidence package asks a narrower later question:

> What does Ceph retain when it knows a required newer object/version is missing, can identify historical candidate sources, but cannot recover the payload from any of them — and how does that unresolved state become `lost`?

The answer must distinguish:

- knowledge that a version should exist;
- candidate-location/search state;
- actual payload recovery;
- exhaustion of known candidates;
- operator authority to abandon recovery;
- rollback to a prior version;
- logical deletion;
- physical media erasure.

No source here is used to claim that Ceph invented replicated recovery, rollback, data-loss administration, or version metadata.

---

## Source A — 23 November 2010: `might_have_unfound`

Ceph commit:

`846122866db607e5af7409228c0f3d715e781ddc`

**Title:** `Build might_have_unfound set at activation`

https://github.com/ceph/ceph/commit/846122866db607e5af7409228c0f3d715e781ddc

### A1. Historical vocabulary

The commit message explicitly names:

- `might_have_unfound`;
- primary OSD recovery;
- OSDs that might contain unfound objects;
- `Missing` state returned from candidate OSDs;
- objects becoming `LOST` if the latest version resided on an OSD marked lost.

This is direct project vocabulary, not a later reconstruction.

### A2. Candidate recovery set

The patch adds `PG::build_might_have_unfound()` as primary-only recovery state.

The function:

1. ensures historical `past_intervals` are available;
2. walks intervals backward;
3. stops once it crosses `info.history.last_epoch_clean`;
4. skips intervals that did not `maybe_went_rw`;
5. inserts OSDs from relevant acting sets into `might_have_unfound`;
6. removes the primary itself from the candidate set.

The commit message says candidates are removed as `Missing` information is received.

**Grounded use:** historical PG membership/acting information can determine where the future recovery process must still search for a missing current version.

**Do not overclaim:** this does not establish a permanent full per-object location history or a forensic scan of every physical medium.

### A3. Initial automatic-loss direction

The same commit message says that when `might_have_unfound` is empty, objects would be marked `LOST` when the latest version resided on an OSD already marked lost.

This is important because Source B deliberately changes that policy.

---

## Source B — 24 May 2011: administrator-gated loss declaration

Ceph commit:

`ce04e3dbaf2383a521b267585a860f772c4cc786`

**Title:** `osd: add ability to explicitly mark unfound as lost`

https://github.com/ceph/ceph/commit/ce04e3dbaf2383a521b267585a860f772c4cc786

### B1. Policy change is explicit

The commit message says the system should stop automatically marking unfound objects lost merely after all known locations have been tried. Instead, an administrator must explicitly request the transition.

The author gives two reasons:

- peering issues can make an automatic loss declaration wrong;
- the administrator may decide that offline OSDs are worth bringing online to continue the search.

This is direct historical evidence for:

> **search exhaustion ≠ authority to forget.**

### B2. Command guards

The inspected patch only accepts the action on the primary PG and checks that unfound objects exist. It also refuses to mark the state lost when not all potential sources have been probed / qualified as lost.

**Grounded use:** the operator command does not bypass the recovery-search obligation arbitrarily; it is gated on the protocol's candidate-source accounting.

**Limit:** exact guard names and implementation details evolve later; do not treat this one patch as current Ceph behavior.

---

## Source C — 24 February 2012: `revert` semantics and release boundary

Ceph commit:

`c9416e6184905501159e96115f734bdf65a74d28`

**Title:** `osd: 'tell osd.N mark_unfound_lost revert' -> 'pg <pgid> mark_unfound_lost revert'`

https://github.com/ceph/ceph/commit/c9416e6184905501159e96115f734bdf65a74d28

### C1. Operator interface

The documentation added by this commit gives:

`ceph pg <pgid> mark_unfound_lost revert`

and explains that lost objects are reverted to a prior state: a prior version when one exists, or deletion if the missing value was a newly created object.

### C2. `revert` is not newest-version recovery

The command does not reconstruct the missing newest payload. It changes the admitted current state after the newest version has been abandoned.

That supports the engineering distinction:

> **rollback continuity ≠ recovery continuity.**

### C3. Do not backdate `delete`

The patch's command parser explicitly accepts `revert` while reporting that `mark` and `delete` are not yet implemented.

This is a strong anti-anachronism anchor. Later `delete` support belongs to Source D, not to the 2012 interface.

---

## Source D — April 2014: `delete` as a distinct loss mode

Ceph commit:

`245923e704ac3a6262499f26c7a879811edea5b4`

**Title:** `ReplicatedPG: enable mark_unfound_lost delete for ec pools`

https://github.com/ceph/ceph/commit/245923e704ac3a6262499f26c7a879811edea5b4

### D1. `revert|delete`

The command choices are expanded from `revert` to `revert|delete`.

The command description says unfound objects can be marked lost either by removing them or by reverting to a prior version when one is available.

### D2. Erasure-coded boundary

The implementation rejects `revert` for an EC pool and requires `delete` in that bounded release path; the commit message says revert was difficult to implement for EC pools at that time.

**Grounded use:** loss semantics can depend on the retained representation/redundancy regime. Replicated-object rollback support must not be silently projected onto erasure-coded objects.

**Limit:** this is a 2014 implementation boundary, not a timeless property of Ceph EC.

### D3. Local deletion implementation detail

The immediately preceding commit `95d0278dcfebf77f8548ab7683ce7420302a0443` removes a local object copy in the delete path where needed for an EC pool.

https://github.com/ceph/ceph/commit/95d0278dcfebf77f8548ab7683ce7420302a0443

This supports the fact that `delete` is not merely a label change inside one abstract state machine. It can drive physical-object-store removal operations. It still does **not** establish secure media sanitization.

---

## Source E — 31 August 2014: project documentation names the semantic consequence

Ceph commit:

`9fac072380fd357be23e154fc878bbf485af567e`

**Title:** `documentation: add the mark_unfound_lost delete option`

https://github.com/ceph/ceph/commit/9fac072380fd357be23e154fc878bbf485af567e

The documentation update distinguishes:

- `delete`: forget the lost object;
- `revert`: roll back to a prior version where possible, otherwise forget a new object for which no prior version exists.

It also warns that the operation can confuse applications that expected the object to exist.

**Grounded use:** a storage system can force itself into a converged state after irrecoverable loss while still violating a higher-level application expectation. `storage convergence ≠ application semantic repair`.

**Forgetting boundary:** the historical docs themselves use `forget` language. The project nevertheless keeps this separate from secure physical erasure.

---

## Source F — current official documentation: continuity/context only

Current Ceph documentation continues to maintain an operator-facing distinction between `unfound` objects and explicitly marking them `lost` after giving up the search.

- Placement Groups — “Reverting Lost RADOS Objects”:
  https://docs.ceph.com/en/latest/rados/operations/placement-groups/
- Troubleshooting PGs — `unfound` / recovery states:
  https://docs.ceph.com/en/latest/rados/troubleshooting/troubleshooting-pg/

The current documentation is useful for explaining the contemporary operational concept. It is **not** used to backfill exact 2010–2014 command support or source behavior; Sources A–E carry the historical claims.

---

## Same-system background — Case 05, not duplicated here

[`Case 05`](../cases/05-rados-replicated-object-repair.md) and its [`2006–2007 grounding record`](05-rados-2006-2007-grounding.md) already establish:

- object → PG → ordered OSD placement;
- primary-copy replication and version assignment;
- PG log/version exchange;
- peering before ordinary I/O;
- missing/stale-object repair when enough current state survives;
- failure-triggered membership replacement.

Case 98 therefore does not repeat CRUSH or the general RADOS architecture. It extends the evidence chain only where ordinary repair fails because the latest needed version is known but unfound.

---

## Related-repository duplication check

A GitHub repository search during this research pass found no dedicated `Ceph` or `Ceph unfound` technical-history match in `tmzncty/computing-archaeology`.

Use this result narrowly: no matching module was found by those searches. It is not a proof that no related distributed-storage material exists anywhere in that repository.

The division of labor remains:

- broad Ceph/PG/peering implementation history → `computing-archaeology` if developed;
- retention-specific distinction among unresolved currentness, recoverability, loss authority, rollback, and deletion → this case.

---

## Claim ledger

| Claim | Type | Evidence | Status / limit |
| --- | --- | --- | --- |
| primary recovery tracks OSDs that might contain unfound objects | H/P | Source A | grounded to 2010 source |
| historical acting intervals since a clean boundary help build the candidate set | H/P | Source A patch | grounded; PG/recovery scoped |
| the system can remember that required state is missing without possessing its payload | E | Sources A–B | reconstruction from grounded mechanism |
| automatic loss declaration was replaced by administrator-gated action | H/P | Source B | grounded to 2011 source |
| peering uncertainty / offline OSD recovery motivated the operator gate | H/P | Source B commit message | grounded |
| all candidates queried ≠ automatic logical forgetting | E | Sources A–B | grounded engineering reconstruction |
| 2012 `revert` can select a previous version or absence for a newly created object | H/P | Source C | grounded |
| 2012 `delete` support | X | Source C | explicitly not yet implemented in inspected path |
| 2014 `delete` is a separate loss mode | H/P | Sources D–E | grounded |
| 2014 EC pools share identical revert semantics with replicated pools | X | Source D | explicitly rejected in bounded implementation |
| logical lost/delete means secure physical erasure | X | Sources D–E | unsupported; separate sanitization problem |
| Ceph invented operator-directed rollback/loss recovery | X | none | not claimed |
| forced storage convergence automatically repairs application semantics | X | Source E warning | explicitly rejected |

---

## Controlled cross-case conclusions

1. **currentness knowledge can outlive payload recoverability**;
2. **historical candidate-location state can itself be retention infrastructure**;
3. **unfound ≠ lost**;
4. **loss declaration ≠ media sanitization**;
5. **revert ≠ newest-version reconstruction**;
6. **repair exhaustion can create a human authorization boundary rather than an automatic state transition**;
7. **retaining an unresolved recovery obligation is different from retaining complete operation history**;
8. **representation regime can constrain available forgetting/recovery transitions**;
9. **storage-level resolution can still violate application expectations**.

These are project-level engineering conclusions, not quotations or universal distributed-systems laws.
'''


case_path = ROOT / 'cases/98-ceph-unfound-recovery-exhaustion-administrative-loss.md'
evidence_path = ROOT / 'evidence/98-ceph-2010-2014-unfound-lost-grounding.md'
if case_path.exists() or evidence_path.exists():
    raise SystemExit('Case 98 target path already exists; refusing to overwrite')
case_path.write_text(case, encoding='utf-8')
evidence_path.write_text(evidence, encoding='utf-8')

# README: put the new canonical case immediately after the current highest active case.
insert_after_unique_line(
    'README.md',
    'cases/96-openzfs-draid-distributed-spare-sequential-resilver.md',
    '- [`cases/98-ceph-unfound-recovery-exhaustion-administrative-loss.md`](cases/98-ceph-unfound-recovery-exhaustion-administrative-loss.md) — grounded distributed-recovery failure boundary: Ceph 2010–2014 source history shows that PG recovery can retain evidence that a newer object version should exist and historical candidate OSDs that might contain it even when the payload is not recoverable; `unfound`, administrator-gated `lost`, `revert`, and later `delete` are kept distinct, so search exhaustion, rollback, logical forgetting, and physical erasure are not collapsed; see [`evidence/98-ceph-2010-2014-unfound-lost-grounding.md`](evidence/98-ceph-2010-2014-unfound-lost-grounding.md).'
)

# ROADMAP: record the bounded bridge and advance, but do not close, the broad failed-repair item.
insert_after_unique_line(
    'ROADMAP.md',
    '- [x] OpenZFS dRAID distributed-spare / sequential-resilver recovery window',
    '- [x] Ceph `unfound` / administrator-gated `lost` recovery-exhaustion boundary — [`cases/98-ceph-unfound-recovery-exhaustion-administrative-loss.md`](cases/98-ceph-unfound-recovery-exhaustion-administrative-loss.md), grounded by [`evidence/98-ceph-2010-2014-unfound-lost-grounding.md`](evidence/98-ceph-2010-2014-unfound-lost-grounding.md), adds a 2010–2014 RADOS failure regime beyond Case 05 ordinary repair: retained PG history can identify OSDs that might still contain a known-needed newer version after the payload is unavailable; a 2011 policy change deliberately moves final abandonment from automatic search exhaustion to explicit administrator authority; 2012 `revert` and later 2014 `delete` remain separate release-bounded transitions. This establishes `unfound ≠ lost`, `rollback ≠ recovery`, `logical loss ≠ secure erasure`, and `repair exhaustion ≠ automatic forgetting authority`. Broader Ceph peering genealogy, modern release behavior, Byzantine/partition models, field incident evidence, and cross-system failed-repair history remain open.'
)
replace_unique_line(
    'ROADMAP.md',
    '- [ ] replica divergence and failed repair;',
    '- [ ] replica divergence and failed repair — **partially advanced by grounded Case 98**: Ceph can retain evidence that a newer object/version is owed plus historical candidate locations after no recoverable payload is currently found; candidate-source exhaustion still does not itself authorize forgetting, because 2011 source makes the final `unfound`→`lost` transition administrator-gated. Revert/delete then change admissible logical state without establishing physical sanitization. Byzantine divergence, correlated-loss incidents, modern Ceph behavior, quorum-store unrecoverability, and independent fault injection remain open;'
)

# CASE_INDEX canonical row.
insert_after_unique_line(
    'CASE_INDEX.md',
    'cases/96-openzfs-draid-distributed-spare-sequential-resilver.md',
    '| [Ceph Unfound Objects: Retained Version Knowledge, Recovery Exhaustion, and Administrative Loss](cases/98-ceph-unfound-recovery-exhaustion-administrative-loss.md) | **grounded** | missing/current-version evidence + historical PG acting intervals + `might_have_unfound` candidate set + explicit administrator loss authority + rollback/delete transitions | separate knowledge that a newer version should exist from retention of its payload; candidate-source exhaustion from logical forgetting; `unfound` from `lost`; rollback from reconstruction; logical loss from secure erasure | [2010–2014 Ceph unfound/lost grounding](evidence/98-ceph-2010-2014-unfound-lost-grounding.md); broader peering/loss genealogy, modern-release semantics, distributed-system prior art, production incident evidence, and independent fault injection remain separate work |'
)

# CASE_INDEX comparison matrix: add a failure-boundary row next to the ordinary RADOS row.
insert_after_unique_line(
    'CASE_INDEX.md',
    '| RADOS | multiple object replicas + cluster map + PG/version/recovery state |',
    '| Ceph unfound/lost / 2010–2014 bounded regime | retained missing/current-version relation + historical acting intervals + candidate OSD search set + surviving older versions/absence + administrator loss decision | automatic recovery keeps probing historically plausible sources; when newest payload remains unfound, final abandonment is explicitly operator-gated; `revert` or later `delete` resolves the blocked obligation | ordinary current-version recovery is unavailable at the failure boundary; forced `revert` admits an older value or absence rather than reconstructing the missing newest payload | current placement is insufficient; recovery uses historical PG acting intervals to enumerate OSDs that might still hold the required version | no recoverable newest embodiment may remain even though the logical system still retains an existence/currentness claim; later rollback/delete changes admissible continuation without proving media erasure | no complete operation history; bounded placement/version evidence and candidate-source accounting are retained long enough to decide whether recovery is still owed |'
)

# Findings continue the existing numbered ledger without renumbering historical gaps.
insert_after_unique_line(
    'CASE_INDEX.md',
    '1290. **controller-managed Flash retention is a staged relation rather than one `nonvolatile` Boolean**',
    r'''

### Case 98 — Ceph unfound / recovery-exhaustion findings

1291. **knowledge that a newer version should exist ≠ retention of that version's payload** — Ceph can retain missing/currentness evidence after no recoverable embodiment of the newest object version is available.
1292. **historical candidate-location metadata ≠ recovered content** — `past_intervals` and `might_have_unfound` preserve where recovery should still look, not the bytes being sought.
1293. **current placement ≠ complete recovery search geometry** — the 2010 code consults historically relevant acting intervals since a clean boundary because a former participant may still hold the needed version.
1294. **all known candidate sources queried ≠ physical proof of universal absence** — search-space exhaustion is a bounded protocol conclusion, not a forensic theorem about every possible copy on every medium.
1295. **`unfound` ≠ `lost`** — an unresolved object can remain represented as a recovery obligation until a separate transition declares the newest state abandoned.
1296. **repair exhaustion ≠ automatic authority to forget** — the 2011 policy change deliberately requires administrator action because peering faults or worth-reviving offline OSDs can make automatic loss declaration premature.
1297. **operator authority can become retention/forgetting state** — at the automatic-repair boundary, human judgment can determine whether the system continues preserving a search obligation or retires it.
1298. **`revert` ≠ recovery of the missing newest version** — the 2012 path selects a prior version, or absence for a newly created object, after newest-version recovery has failed.
1299. **rollback continuity ≠ history fidelity** — service may resume under an older admissible state while the latest acknowledged/known version remains irrecoverable.
1300. **2012 `revert` semantics ≠ later `delete` semantics** — the inspected 2012 parser explicitly lacked delete support; 2014 source adds a separate delete mode and an EC-specific boundary.
1301. **logical `lost` / delete ≠ secure physical erasure** — changing currentness authority or removing object-store state does not establish sanitization of every lower-layer embodiment.
1302. **representation regime can constrain failure-resolution options** — the 2014 EC path required `delete` rather than the replicated-pool `revert` behavior in that implementation, so one logical forgetting interface cannot be projected uniformly across redundancy formats.
1303. **storage-level convergence ≠ application semantic repair** — Ceph's 2014 documentation warns that forced loss handling can confuse applications that expected the object to exist.
1304. **retention can preserve an obligation toward absent state** — Case 98 supplies a bounded distributed counterexample in which the surviving technical state is partly the rule that a missing newer version still counts as owed until recovery or explicit abandonment resolves that claim.
'''
)
