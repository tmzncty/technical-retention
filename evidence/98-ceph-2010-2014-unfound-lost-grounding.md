# Ceph 2010–2014 unfound / lost grounding record

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
