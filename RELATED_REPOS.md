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

## 4. old-web-archaeology

<https://github.com/tmzncty/old-web-archaeology>

### Role

Concrete historical web-preservation and reconstruction companion.

Its scope is roughly:

> What did the Chinese web of roughly 1995–2015 actually leave behind, why did parts disappear, and what can surviving captures, software, browser assumptions, screenshots, link structures, and other evidence justify reconstructing?

This makes it especially relevant when `technical-retention` reaches long-term access problems involving file formats, character encodings, browser engines, plug-ins, scripts, network dependencies, missing resources, or reconstruction from incomplete captures.

### Reuse rule

If the research problem is primarily about a particular historical website, archived capture, browser/runtime environment, or reconstruction of missing web evidence, develop it in `old-web-archaeology` and cite it here.

`technical-retention` should keep the cross-mechanism analytical question: which retained relations must survive or be reconstituted for a future operation to recover an object as usable/current/meaningful? The bounded OAIS/PREMIS prior-art review in [`docs/PRIOR_ART.md`](docs/PRIOR_ART.md) and [`evidence/prior-art-oais-premis-2002-2024-grounding.md`](evidence/prior-art-oais-premis-2002-2024-grounding.md) supplies the archival-information-model boundary; `old-web-archaeology` supplies concrete historical web cases when needed.

Do not duplicate a capture history here merely to illustrate that old software becomes incompatible.

---

## 5. Future links

Other repositories may become relevant when retention is studied as:

- interface compatibility;
- file-format survivability;
- network state;
- archival practice;
- encoding failure;
- scholarly research protocol.

Old-web preservation is no longer merely a future-link category: `old-web-archaeology` now has an explicit division of labor above.

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
       ┌────────┼──────────────────────────┐
       ▼        ▼                          ▼
problem-history mechanical-computing-     old-web-archaeology
anti-anachronism playground               historical captures /
                 reconstruction /         browser-runtime /
                 experiment               reconstruction cases
```
