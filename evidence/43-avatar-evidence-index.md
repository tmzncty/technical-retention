# Case 43 Evidence Index — AVATAR VRT-Aware DRAM Refresh

Canonical case: [`../cases/43-avatar-vrt-aware-dram-refresh-feedback.md`](../cases/43-avatar-vrt-aware-dram-refresh-feedback.md)

Current status: **`grounded`**.

This index keeps the evidence layers for Case 43 separated so that AVATAR's runtime feedback mechanism, its modeled reliability claims, and the protection/lifetime of its own refresh-policy metadata are not collapsed into one statement.

---

## Evidence chain 1 — Original AVATAR mechanism and evaluation boundary

**Record:** [`43-avatar-2015-vrt-aware-refresh-grounding.md`](43-avatar-2015-vrt-aware-refresh-grounding.md)

**Primary source:** Qureshi et al., *AVATAR: A Variable-Retention-Time (VRT) Aware Refresh for DRAM Systems*, DSN 2015.

**Grounds:**

```text
initial retention testing
    -> RRT Slow/Fast classification
    -> runtime ECC observation
    -> correct current error
    -> upgrade affected row to Fast Refresh
    -> proactive scrub for cold memory
    -> later retention retest / possible downgrade
```

**Important boundaries:**

- VRT characterization on 24 chips is experimental evidence;
- multi-decade reliability numbers are model/evaluation results, not field lifetimes;
- scrub is distinct from refresh;
- ECC correction is distinct from future refresh-policy repair;
- a surviving profile is not automatically a still-valid profile;
- AVATAR is a research architecture, not evidence of commercial deployment.

---

## Evidence chain 2 — RRT placement, representation, and self-protection

**Record:** [`43-avatar-2015-rrt-self-protection-deepening.md`](43-avatar-2015-rrt-self-protection-deepening.md)

**Primary sources:** AVATAR (DSN 2015) plus RAIDR (ISCA 2012) as explicit prior art / controlled comparison.

**Grounds:**

```text
refresh policy
    -> represented by RRT bits
    -> consumed at memory controller
    -> can optionally be backed by reserved DRAM
    -> DRAM-resident RRT can itself suffer VRT errors
    -> paper proposes three replicas for that RRT
```

The deepening also records the source's proposed current-line / next-line RRT prefetch arrangement and the one-bit-per-row representation used when the expected FastRefresh population is too large for the sparse Bloom-filter approach to remain attractive.

**New retention boundary:**

```text
payload retention
    !=
retention of the policy that schedules payload retention
```

and:

```text
policy meaning becomes stale
    !=
policy representation becomes corrupted
```

AVATAR addresses the first through runtime ECC/scrub feedback and retesting; for the optional DRAM-resident RRT it acknowledges the second by proposing replication.

**Important boundaries:**

- triplication is documented, but a complete read/vote/repair/update protocol is not;
- controller decision locus is not the same thing as full-table physical storage locus;
- prefetched metadata availability is not identical to retained backing state;
- AVATAR does not establish cross-reboot persistence semantics for runtime FastRefresh upgrades;
- the paper does not specify bootstrap refresh/classification of the DRAM rows that hold the RRT;
- RAIDR's Bloom-filter no-false-negative property is an abstract data-structure property, not immunity to physical bit corruption.

---

# Historical / engineering separation

## Historical record

Directly supported by the sources:

- AVATAR uses initial retention testing, an RRT, ECC, scrub, runtime upgrades, and infrequent retesting;
- the studied RRT uses one bit per row and is 128 KB for the paper's 8 GB / 8 KB-row example;
- RRT information is assumed available at the memory controller;
- the paper proposes reserved-DRAM backing as an alternative to storing the whole RRT in SRAM;
- while the current 512-row RRT line is used, the next line can be prefetched;
- a DRAM-resident RRT can be replicated three times to tolerate VRT-related errors in the RRT;
- RAIDR stores sparse retention bins in the controller using Bloom filters and discusses saving profiling results for future boots.

## Engineering reconstruction

Project-level deductions kept explicitly separate from the historical record:

- maintenance-policy metadata can itself become retention payload when placed in DRAM;
- decision locus, backing-store locus, and protection locus are distinct;
- self-hosted policy metadata creates a recursive service dependency;
- retained state and timely state availability are distinct requirements;
- with `0 = SlowRefresh`, `1 = FastRefresh`, policy-bit corruption has asymmetric consequences;
- redundant copies do not by themselves establish a consistent mutable replicated state machine.

## Functional analogy

The RRT can be compared at the relation level with storage/distributed systems where payload maintenance depends on protected control metadata. No historical genealogy is inferred from that analogy.

RAIDR is a stronger historical comparison because AVATAR explicitly cites it and directly discusses the difference in metadata representation.

## Philosophical interpretation

A narrowly supported interpretation is:

> the state that specifies **how to preserve other state** can itself require preservation and revalidation.

This remains a repository interpretation, not a philosophical claim attributed to the AVATAR authors.

---

# Cross-case hooks

Useful comparisons for later synthesis:

- **Case 03 — DRAM refresh control:** physical retention service depends on coverage/cadence state; Case 43 adds adaptive per-row policy metadata and shows that this metadata can itself live in DRAM.
- **Case 40 — retention profiling / DPD / VRT:** Case 40 establishes why a retained profile may become stale; Case 43 adds runtime repair of that policy and now a separate protection question for the policy representation.
- **Case 52 — NAND read-disturb maintenance:** useful functional comparison between retained maintenance policy and retained pending maintenance work; do not infer genealogy.
- **Case 153 — Ceph snap-trim:** useful functional comparison between reconstructable work state and retained completion evidence; again, only a relation-level analogy.

---

# Remaining evidence debt

Highest-value next slices, in priority order:

1. **Replicated-RRT semantics:** locate any simulator code, dissertation, technical report, or follow-on artifact that specifies voting, repair, and update semantics for the three RRT copies.
2. **RRT bootstrap:** determine whether RRT-hosting rows receive a conservative baseline refresh treatment before metadata becomes available.
3. **Epoch / reboot lifetime:** establish whether runtime FastRefresh upgrades are intended to survive reset/reboot or be reconstructed/retested.
4. **Fault injection:** model `Fast -> Slow`, `Slow -> Fast`, replica disagreement, and metadata-unavailable cases separately.
5. **Commercial boundary:** only if strong primary evidence appears, test whether any shipped controller implemented an AVATAR-like dynamic policy; do not infer deployment from the paper.
6. **Representation comparison:** quantify exact-table vs Bloom-filter policy errors while keeping algorithmic false positives separate from physical bit faults.

---

# Maturity decision

**No promotion. Case 43 remains `grounded`.**

The new evidence substantially strengthens the second-order metadata boundary, but open questions remain around replicated-RRT protocol details, bootstrap protection, cross-reboot lifetime, and real implementation evidence. Those gaps are material enough that this slice should deepen the case rather than change its maturity state.

---

# Related repository boundary

`tmzncty/computing-archaeology` was searched for AVATAR / VRT / RRT material before this deepening. No dedicated reusable packet was found.

`technical-retention` therefore retains only the state-lifetime and maintenance-metadata relation. A broader history of DRAM refresh research, commercial memory-controller implementation, or full RAIDR→AVATAR research genealogy belongs in the companion repository if later pursued.
