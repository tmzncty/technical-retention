# Ceph `osd_auto_mark_unfound_lost`: Configuration Surface vs Implemented Loss Authority

This record deepens [`Case 98`](../cases/98-ceph-unfound-recovery-exhaustion-administrative-loss.md) and its [`2010–2014 grounding record`](98-ceph-2010-2014-unfound-lost-grounding.md).

**Status:** `bounded deepening complete`

## Research question

Case 98 already grounds the 2011 policy change from automatic loss declaration toward explicit administrator authority after all known recovery candidates have been exhausted. This slice asks a narrower question:

> If Ceph exposes a configuration option named `osd_auto_mark_unfound_lost`, does the existence of that option mean that automatic logical forgetting is actually implemented?

The answer in the inspected source is **no**.

This is a useful negative control because configuration vocabulary, default policy, and executable capability can diverge for a long time.

---

## Scope and evidence boundary

The bounded witnesses are:

1. Ceph **v0.80.7 Firefly**, released 16 October 2014;
2. a pinned Ceph `main` snapshot, commit `a2c71ca92826a08801d9e5e7668c5a14e94cce91`, dated 12 September 2026.

This evidence establishes continuity at those two inspected points. It does **not** establish:

- the first commit that introduced `osd_auto_mark_unfound_lost`;
- that every Ceph release between those points had identical code;
- that no branch, downstream distribution, or abandoned patch ever implemented automatic marking;
- that the option has no effect outside the inspected loss-transition path;
- production use or operational frequency;
- the behavior of every modern OSD backend, including Crimson;
- secure physical erasure.

The 2010–2014 origin story for `unfound`, `might_have_unfound`, `revert`, and `delete` remains owned by the parent grounding record rather than being repeated here.

---

## Historical record

### A. Firefly v0.80.7 exposes the option and defaults it to false

Ceph `v0.80.7` contains in `src/common/config_opts.h`:

```text
OPTION(osd_auto_mark_unfound_lost, OPT_BOOL, false)
```

The official Ceph release record dates **v0.80.7 Firefly to 16 October 2014**.

This directly establishes a configuration-visible policy knob by that release. The name alone, however, does not establish an implemented state transition.

Source:

- `https://github.com/ceph/ceph/blob/v0.80.7/src/common/config_opts.h`
- `https://ceph.io/en/news/blog/2014/v0-80-7-firefly-released/`

### B. The same release says automatic marking is not implemented

In `v0.80.7/src/osd/PG.cc`, the peering/recovery path checks whether unfound objects remain and whether all unfound candidates have been queried or declared lost. If `osd_auto_mark_unfound_lost` is true, the code emits an error message saying that it **would** automatically mark the objects lost but that this is **NOT IMPLEMENTED**.

The nearby call that would perform the transition is commented out:

```text
//pg->mark_all_unfound_lost(...)
```

The important historical fact is therefore not merely that the default is `false`. In this inspected release, setting the option true still does not execute the automatic loss transition in that path.

That blocks a tempting but incorrect reading:

```text
configuration option exists
    -> feature is implemented but disabled by default
```

For this release, that implication is false.

Source:

- `https://github.com/ceph/ceph/blob/v0.80.7/src/osd/PG.cc`

### C. The distinction survives into the pinned 2026 main snapshot

At Ceph commit `a2c71ca92826a08801d9e5e7668c5a14e94cce91` (12 September 2026), `src/common/options/global.yaml.in` still defines:

```text
- name: osd_auto_mark_unfound_lost
  type: bool
  level: advanced
  default: false
  with_legacy: true
```

In the same snapshot, `src/osd/PeeringState.cc` still checks the option when all unfound objects have been queried or their candidate sources are lost. When the option is enabled, the code reports that it would automatically mark the objects lost, but explicitly says:

```text
this feature is not yet implemented
```

The continuity claim is deliberately narrow:

> **At the two inspected source points, the configuration name survives while the automatic loss transition remains explicitly unimplemented in the classic peering path.**

This is not a claim about every intermediate release or every backend.

Sources:

- `https://github.com/ceph/ceph/blob/a2c71ca92826a08801d9e5e7668c5a14e94cce91/src/common/options/global.yaml.in`
- `https://github.com/ceph/ceph/blob/a2c71ca92826a08801d9e5e7668c5a14e94cce91/src/osd/PeeringState.cc`
- `https://github.com/ceph/ceph/commit/a2c71ca92826a08801d9e5e7668c5a14e94cce91`

### D. Current operator documentation still presents loss handling as an explicit command

Current Ceph documentation continues to tell an operator who has exhausted all possible recovery locations that they may explicitly invoke:

```text
ceph pg {pg-id} mark_unfound_lost ...
```

The documentation also warns that forced loss handling may confuse applications that expect the object to exist.

This is used only as **contemporary continuity/context**. The current documentation is not projected backward to prove the 2014 implementation, and its current wording around `revert|delete` versus supported options is not resolved in this slice.

Sources:

- `https://docs.ceph.com/en/latest/rados/operations/placement-groups/`
- `https://docs.ceph.com/en/latest/rados/troubleshooting/troubleshooting-pg/`

---

## Engineering reconstruction

The source pair forces three layers apart.

### 1. Configuration vocabulary is retained state, but not executable capability

A configuration schema can preserve a named policy choice even when the code path that would realize that choice is absent or deliberately disabled.

For this case:

```text
retained configuration key
    !=
implemented transition
```

The option's continued presence is evidence about the software's control surface, not evidence that the named behavior can actually occur.

### 2. Default policy and capability are different questions

A reader could see `default: false` and infer that the feature exists but merely requires opt-in. The inspected source rejects that inference.

The stronger decomposition is:

```text
option exists
    != capability implemented

default false
    != implemented-but-disabled

operator can name a policy
    != system can execute that policy
```

Whether a capability exists must be checked in the implementation path, not inferred from the schema alone.

### 3. Recovery exhaustion remains distinct from forgetting authority

The peering code reaches the auto-mark branch only after there are unfound objects and the system believes all candidate locations have been queried or lost. Yet even then, the automatic transition is absent in the inspected path.

Thus the parent Case 98 distinction becomes more precise:

```text
candidate search exhausted
    -> apparently lost / unresolved state
    -> warning or operator decision boundary
    != automatic logical forgetting
```

The configuration key does not collapse that boundary.

---

## Retention-specific interpretation

This slice exposes a less obvious kind of retained state: **a durable control-surface name can outlive the executable mechanism it appears to name**.

That matters methodologically because repositories contain many artifacts that look authoritative when inspected in isolation:

- configuration keys;
- command names;
- enums;
- comments;
- documentation syntax;
- telemetry fields.

Their survival proves that some vocabulary or interface surface persists. It does not prove that the corresponding behavior is live, complete, reachable, or authoritative.

For technical-retention, the bounded lesson is:

> **retention of an interface sign is not retention of the capability it denotes.**

This is an engineering/philosophical interpretation of the code history, not Ceph's own historical vocabulary.

---

## Functional comparison

The finding is comparable, at a purely functional level, to other repository cases where an interface-visible state must not be equated with a lower-layer physical or operational fact:

- SMART / health telemetry can expose a service threshold without being a literal physical-resource counter;
- a persistent repair mapping can survive while payload continuity remains a separate question;
- an operation name can survive across implementation changes while the underlying retained representation changes.

The comparison is heuristic only. No genealogy is claimed between these mechanisms and Ceph's loss configuration.

---

## Counterexamples and explicit non-claims

1. **`osd_auto_mark_unfound_lost` exists → automatic marking works** is false at the inspected Firefly and 2026 source points.
2. **`default false` → implemented but opt-in** is unsupported and contradicted by the inspected implementation path.
3. **unimplemented auto-mark → Ceph has no loss transition** is false. Case 98 already grounds explicit administrator-driven `revert` / `delete` paths in the relevant historical releases.
4. **all candidates queried/lost → payload is physically absent everywhere** is false. Candidate exhaustion is protocol-scoped, not a forensic theorem.
5. **manual lost/delete → secure erasure** is false.
6. **the option survived → developers continuously intended to implement it** is unsupported. A surviving symbol does not prove continuous roadmap intent.
7. **two inspected snapshots → every intermediate release behaved identically** is unsupported.
8. **classic `PeeringState` behavior → Crimson parity** is unsupported. Modern backend-specific completion remains separate work.
9. **current documentation wording → exact historical command support** is unsupported.
10. **configuration schema is irrelevant** is also too strong. Its survival is real historical evidence for a retained control-surface concept; it simply must not be mistaken for implemented capability.

---

## Related-repository check

A repository search of `tmzncty/computing-archaeology` for `Ceph unfound` found no dedicated matching technical-history module during this pass.

Therefore this file keeps only the retention-specific configuration/capability boundary. A broader genealogy of Ceph option plumbing, peering state-machine refactors, or backend parity belongs primarily in `computing-archaeology` if developed later.

---

## Claim ledger

| Claim | Type | Evidence | Status / limit |
| --- | --- | --- | --- |
| Firefly v0.80.7 exposes `osd_auto_mark_unfound_lost` with default `false` | Historical record | `config_opts.h` v0.80.7 | grounded to inspected tag |
| Firefly v0.80.7 auto-mark branch says `NOT IMPLEMENTED` and does not invoke the commented transition | Historical record | `PG.cc` v0.80.7 | grounded to inspected path |
| pinned 2026 main still defines the option with default `false` | Historical record | `global.yaml.in` @ `a2c71ca...` | grounded to inspected snapshot |
| pinned 2026 classic peering path still says auto-mark is not yet implemented | Historical record | `PeeringState.cc` @ `a2c71ca...` | grounded to inspected path |
| configuration key existence does not prove executable capability | Engineering reconstruction | paired schema + implementation witnesses | bounded conclusion |
| `default false` does not by itself mean implemented-but-disabled | Engineering reconstruction | paired witnesses | bounded conclusion |
| candidate exhaustion does not itself execute logical forgetting in the inspected auto path | Engineering reconstruction | `PG.cc` / `PeeringState.cc` | bounded to inspected paths |
| the option's first introduction date | Historical record | not established here | open |
| no release or downstream ever implemented auto-mark | Historical record | not established | explicitly not claimed |
| Crimson has identical behavior | Historical record | not established | open |

---

## Follow-up work

The useful remaining questions are now narrower:

- locate the exact introduction commit and original rationale for `osd_auto_mark_unfound_lost`;
- determine whether any historical release branch ever wired the option to a real automatic transition;
- trace the option through the PG → `PeeringState` refactor without assuming uninterrupted semantics;
- audit Crimson's current `mark_unfound_lost` support separately;
- resolve the current documentation wording around supported `revert|delete` forms;
- find field incidents where operators deliberately kept `unfound` obligations alive rather than declaring loss.

None of those is required for the bounded conclusion of this slice.
