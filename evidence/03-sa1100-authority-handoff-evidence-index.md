# Case 03 — SA-1100 DRAM Authority-Handoff Evidence Index

## Canonical case and maturity

Canonical case: [`cases/03-dram-refresh-as-scheduled-restoration.md`](../cases/03-dram-refresh-as-scheduled-restoration.md)

Primary Case 03 navigation: [`03-dram-evidence-index.md`](03-dram-evidence-index.md)

Canonical maturity: **`grounded`**.

This scoped index does **not** promote Case 03 and does not replace the broader DRAM evidence index. It exists because the SA-1100 now supplies two distinct named-system authority-transfer mechanisms that should not be collapsed into one generic `handoff` story.

---

# Evidence chain

## 1. Sleep / self-refresh handoff — 1998–1999

**Record:** [`03-intel-sa1100-1998-1999-sleep-self-refresh-control-state-handoff-deepening.md`](03-intel-sa1100-1998-1999-sleep-self-refresh-control-state-handoff-deepening.md)

### Historical mechanism

Intel documents a sleep sequence in which the SA-1100:

1. finishes the currently admitted memory operation;
2. places DRAM into self-refresh;
3. holds RAS / CAS in the self-refresh condition;
4. allows ordinary memory-controller state to reset / lose power;
5. later wakes while DRAM remains in self-refresh;
6. lets software reconstruct the controller configuration;
7. only then releases self-refresh and resumes ordinary access.

### Bounded relation

```text
payload retention continuity
    !=
controller-state continuity
```

and:

```text
SA-1100 ordinary refresh authority
    -> DRAM self-refresh authority
    -> reconstructed SA-1100 ordinary refresh authority
```

### What is retained across the gap

- DRAM payload, under the DRAM's self-refresh regime;
- enough power-manager / interface-hold state to keep that regime active;
- optionally a small scratchpad clue useful for controller reconstruction.

The ordinary DRAM control registers themselves need not survive.

---

## 2. Alternate-master handoff — 1998–1999

**Record:** [`03-intel-sa1100-1998-alternate-master-refresh-authority-handoff-deepening.md`](03-intel-sa1100-1998-alternate-master-refresh-authority-handoff-deepening.md)

### Historical mechanism

Intel §10.8 documents a different path:

1. an external master asserts `MBREQ`;
2. the SA-1100 finishes pending / in-progress memory work and outstanding refresh;
3. the SA-1100 grants the bus and tristates its memory pins;
4. while the alternate master owns the bus, the SA-1100 cannot issue DRAM refresh;
5. Intel assigns DRAM-integrity responsibility to the alternate master;
6. that responsibility can be met either by keeping tenure much shorter than the refresh period or by performing refresh from the alternate master;
7. after bus return, a refresh that became due in the SA-1100 during the tenure is serviced before other stalled transactions.

### Bounded relation

```text
bus ownership
    !=
refresh execution authority
    !=
refresh obligation
```

and:

```text
short authority gap + remaining refresh slack
    OR
replacement refresh executor
    -> bounded continuity path
```

### What can remain in the original controller

The manual says the internal refresh counter may request a refresh while alternate mastership is in progress. Thus a due-state can evolve in the SA-1100 even though it temporarily lacks bus authority to execute the maintenance action.

```text
maintenance due-state
    !=
maintenance execution authority
```

---

# Two handoffs, not one

| Dimension | Sleep / self-refresh | Alternate master |
| --- | --- | --- |
| Why SA-1100 stops ordinary refresh | low-power transition | shared bus granted to external master |
| Replacement preservation regime | DRAM self-refresh | deadline slack or external-master refresh |
| Does ordinary controller configuration survive? | no; documented reconstruction after wake | controller remains powered enough for refresh due-state to evolve |
| Does SA-1100 have DRAM bus execution authority during gap? | no ordinary access while self-refresh hold is active | no; pins are tristated |
| Who is assigned refresh / integrity responsibility? | DRAM self-refresh mechanism | alternate master / system design |
| Closure before handoff | finish admitted memory operation, enter self-refresh | finish admitted memory work and outstanding refresh |
| Closure after handoff | rebuild controller, then release self-refresh | pending refresh first, then stalled ordinary transactions |
| Main retained resource across gap | preservation mode + payload | payload plus bounded time budget, or replacement refresh capability |

The strongest current cross-slice distinction is:

```text
maintenance authority can move
    downward into the memory device
    OR
    sideways to another controller/master
```

That is an engineering reconstruction from the two Intel paths, not Intel's period terminology.

---

# Anti-collapse rules

Do not rewrite the combined SA-1100 evidence as any of the following:

```text
handoff = self-refresh
```

```text
bus master = permanent owner of memory state
```

```text
controller cannot refresh now = payload already lost
```

```text
pending refresh after bus return = proof every deadline was met
```

```text
alternate master refresh = transfer of the SA-1100's exact counter state
```

```text
controller reconstruction after sleep = payload reconstruction
```

The two records instead support a typed authority model:

```text
payload
    !=
maintenance obligation
    !=
maintenance due-state
    !=
current maintenance executor
    !=
physical bus authority
    !=
time budget before another maintenance action is required
```

---

# Historical / reconstruction / analogy boundary

## Historical record

The Intel manuals supply period terms and operations: `MBREQ`, `MBGNT`, alternate memory-bus master, DRAM refresh, self-refresh, refresh counter, DRAM integrity, sleep reset, DRAM control hold, and controller reconfiguration.

## Engineering reconstruction

The project separates bus authority, refresh execution authority, due-state, obligation, deadline slack, preservation-mode state, and payload continuity.

## Functional analogy

Later distributed or storage-maintenance cases may also have replaceable executors and retained repair obligations. Such comparisons are functional only. The SA-1100 is not presented as a historical ancestor of distributed maintenance scheduling.

## Philosophical interpretation

The bounded interpretive point is that persistence can depend on an obligation whose executor changes while the retained object remains continuous. Intel does not use that philosophical vocabulary.

---

# Related repositories

Fresh searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `SA-1100` and `StrongARM` found no dedicated module to reuse.

If a broader StrongARM / PXA / alternate-bus-master history is developed, it belongs there. `technical-retention` should keep only the retention-specific handoff, deadline, and currentness relations.

---

# Remaining debt

The SA-1100 authority-handoff evidence is now conceptually strong but still contract-level rather than experimental. Highest-value remaining work is:

1. named board / external-master implementations using `MBREQ` / `MBGNT`;
2. fault-window tests around alternate tenure and refresh-period violation;
3. attached-DRAM-specific refresh limits and weak-row behavior;
4. exact pending-refresh/coalescing semantics if further Intel implementation material survives;
5. successor comparison only where it materially changes the handoff relation.

---

# Status decision

**No maturity change.** Case 03 remains **`grounded`**.