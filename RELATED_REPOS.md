# Related Repositories

`technical-retention` is designed as a conceptual bridge across existing projects, not a replacement for them.

## 1. computing-archaeology

<https://github.com/tmzncty/computing-archaeology>

### Role

Primary companion for technical history and engineering reconstruction.

Its question is roughly:

> Why did a historical computing design make sense under its period material, manufacturing, cost, speed, interface, and operational constraints?

It already contains a substantial `docs/memory/` track covering delay lines, Williams tubes, drums, magnetic core, tape, disk, HBM, and related topics, while its audit identifies semiconductor memory and later storage geometry as important work still to deepen.

### Reuse rule

If the historical mechanism is already explained there, `technical-retention` should **link and analyze**, not copy and paraphrase the same technical history.

If new research mainly improves the historical engineering account, contribute it there first.

---

## 2. problem-history

<https://github.com/tmzncty/problem-history>

### Role

Methodological companion.

Its strongest transferable rule is:

> Prove that historical actors had a problem before attributing our modern formulation of that problem to them.

This protects `technical-retention` from claims such as:

- `the abacus was already a register`;
- `ancient record keeping was already database storage`;
- `Babbage anticipated every modern memory abstraction`.

Such comparisons may be useful functional analogies, but they are not automatically historical continuities.

---

## 3. mechanical-computing-playground

<https://github.com/tmzncty/mechanical-computing-playground>

### Role

Hands-on reconstruction, simulation, and mechanism demonstration.

Examples of work that might belong there:

- a mechanical retained-state demonstrator;
- a simple counter or carry mechanism;
- a physical or executable comparison of destructive versus nondestructive read;
- a small model showing recirculating memory.

`technical-retention` can then cite the experiment when making the conceptual comparison.

---

## 4. Future links

Other repositories may become relevant when retention is studied as:

- interface compatibility;
- file-format survivability;
- network state;
- archival practice;
- encoding failure;
- old-web preservation;
- scholarly research protocol.

Add a cross-link only when there is an actual division of labor. Avoid building a decorative graph of every repository.

---

## Boundary summary

```text
computing-archaeology
    historical mechanism + engineering constraint
                │
                ▼
technical-retention
    cross-mechanism comparison + philosophy of retention
                │
       ┌────────┴─────────┐
       ▼                  ▼
problem-history       mechanical-computing-playground
anti-anachronism      reconstruction / experiment
```
