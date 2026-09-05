# Ceph Unfound Objects: Retained Version Knowledge, Recovery Exhaustion, and Administrative Loss

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
