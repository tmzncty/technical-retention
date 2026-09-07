from pathlib import Path


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    Path(path).write_text(text.rstrip() + "\n", encoding="utf-8")


# 1) Canonical Case 79: absorb the unique chronology and lifecycle evidence.
case79_path = "cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md"
case79 = read(case79_path)
case79 = case79.replace(
    "- **Object / system:** Apache Hadoop HDFS NameNode startup and SafeMode, bounded primarily to the architecture described by Shvachko et al. in 2010 and the Apache Hadoop 2.7.3 documentation/source released in 2016.\n",
    "- **Object / system:** Apache Hadoop HDFS NameNode startup and SafeMode, now bounded by exact released source from Hadoop 0.18.0 (2008), the architecture described by Shvachko et al. in 2010, Apache 1.0.4 documentation, and released 2.7.3/2.8.0 source through 2017.\n",
)
anchor = "## Prior-art boundary\n"
if anchor not in case79:
    raise SystemExit("Case 79 prior-art anchor not found")
insert = r'''## Historical deepening — exact 0.18.0 implementation and later lifecycle continuity

### H/P — Hadoop 0.18.0 already implements the report-rebuilt location relation

Apache records Hadoop 0.18.0 as released on **22 August 2008**. More importantly than the release notice alone, the exact `release-0.18.0` `FSNamesystem.java` source states in its bookkeeping summary that the `block -> machinelist` relation is **kept in memory and rebuilt dynamically from reports**. The same source's DataNode-map documentation says that only the `DatanodeInfo` portion is checkpointed while the list of blocks is restored from DataNode block reports.

This supplies an implementation-level floor for the central Case-79 relation two years before the 2010 MSST paper:

> **by released Hadoop 0.18.0, HDFS already distinguished checkpointed namespace/DataNode descriptive state from a block-location relation reconstructed from reports.**

This is a chronology floor for HDFS only. It is not an invention-priority claim for report-rebuilt inventories, read-only startup modes, or distributed recovery gates.

### H/P — 0.18.0 startup SafeMode already retains typed progress state

The same exact source loads `FSImage`, constructs `SafeModeInfo`, sets the total-block denominator, and starts the relevant monitors. Its startup `SafeModeInfo(Configuration)` retains:

- a safe-block ratio threshold;
- an extension;
- `safeReplication`;
- `blockTotal`;
- `blockSafe`;
- threshold-reached state.

For this release the source defaults are `dfs.safemode.threshold.pct = 0.95`, `dfs.safemode.extension = 0`, and `dfs.replication.min = 1`.

This is useful precisely because later releases differ. Hadoop 1.0.4 documents `0.999f` and a 30-second extension, while later 2.x source retains the same general threshold/extension structure. Therefore:

> **same named SafeMode mechanism across releases ≠ one timeless quantitative admission contract.**

The 0.18.0 values are historical release-specific implementation evidence, not reliability constants.

### H/P — manual SafeMode is already a distinct state machine in 0.18.0

The exact 0.18.0 source has a separate no-argument `SafeModeInfo()` constructor for manual entry. It uses deliberately unreachable automatic-exit parameters, sets `blockTotal` and `blockSafe` to `-1`, and `isManual()` identifies the mode from that state. Hadoop 2.8.0 later makes the same lifecycle distinction explicit in class documentation: startup SafeMode tracks safe blocks for automatic exit, whereas manually entered SafeMode is not intended to leave through that automatic startup condition.

This strengthens the existing boundary:

> **startup SafeMode ≠ manual SafeMode, even when both expose the same service-state name.**

The distinction is historical/implementation evidence, not a modern philosophical analogy.

### Cross-case controls added by consolidation

Case 80 separately shows that replica count does not establish rack/failure-domain placement satisfaction. Case 83 separately shows that a present/reported replica is not thereby checksum-qualified. Case 116 separately models temporary DataNode maintenance with an expiry. Consequently:

- **safe-block admission ≠ rack-placement qualification**;
- **safe/reported replica ≠ integrity-qualified replica**;
- **NameNode-wide startup SafeMode ≠ per-DataNode maintenance mode**.

These are bounded functional comparisons within the repository, not implementation genealogy.

---

'''
if "## Historical deepening — exact 0.18.0 implementation" not in case79:
    case79 = case79.replace(anchor, insert + anchor, 1)

source_anchor = "### Primary / contemporary / institutional\n\n"
if source_anchor not in case79:
    raise SystemExit("Case 79 source anchor not found")
new_sources = (
    "- Apache Hadoop, **release 0.18.0 available**, 22 August 2008: <https://hadoop.apache.org/release/0.18.0.html>.\n"
    "- Apache Hadoop `release-0.18.0`, **`src/hdfs/org/apache/hadoop/dfs/FSNamesystem.java`**, exact released implementation of report-rebuilt block locations and startup/manual `SafeModeInfo`: <https://github.com/apache/hadoop/blob/release-0.18.0/src/hdfs/org/apache/hadoop/dfs/FSNamesystem.java>.\n"
)
if "release-0.18.0`, **`src/hdfs/org/apache/hadoop/dfs/FSNamesystem.java`**" not in case79:
    case79 = case79.replace(source_anchor, source_anchor + new_sources, 1)
source_273 = "- Apache Hadoop `rel/release-2.7.3`, `DFSConfigKeys.java`: <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/DFSConfigKeys.java>.\n"
source_280 = "- Apache Hadoop 2.8.0, **`FSNamesystem.SafeModeInfo` source rendering**, startup versus manually entered SafeMode lifecycle: <https://hadoop.apache.org/docs/r2.8.0/hadoop-project-dist/hadoop-hdfs/api/src-html/org/apache/hadoop/hdfs/server/namenode/FSNamesystem.SafeModeInfo.html>.\n"
if source_273 in case79 and source_280 not in case79:
    case79 = case79.replace(source_273, source_273 + source_280, 1)
case79 = case79.replace(
    "**`grounded`** for the bounded 2010–2016 HDFS startup relation among persistent namespace state, non-checkpointed replica locations, DataNode block-report re-observation, SafeMode admission, and post-exit replication repair.",
    "**`grounded`** for the bounded 2008–2017 HDFS startup relation among persistent namespace state, report-rebuilt replica locations, startup/manual SafeMode control state, admission thresholds, and post-exit replication repair. The accidental later Case 117 duplicate has been consolidated into this canonical case without asserting a broader invention genealogy.",
)
write(case79_path, case79)


# 2) Canonical Evidence 79: add exact 2008 implementation and later continuity.
e79_path = "evidence/79-hadoop-2010-2016-startup-safemode-grounding.md"
e79 = read(e79_path)
e79 = e79.replace(
    "# Case 79 Grounding Record — HDFS Startup SafeMode and Block-Report Re-observation (2010–2016)",
    "# Case 79 Grounding Record — HDFS Startup SafeMode and Block-Report Re-observation (2008–2017)",
)
source1_anchor = "## Source 1 — Shvachko et al., HDFS system paper (2010)\n"
if source1_anchor not in e79:
    raise SystemExit("Evidence 79 Source 1 anchor not found")
source0 = r'''## Source 0 — Apache Hadoop 0.18.0 exact implementation (2008)

**Type:** released primary implementation source (`P/H`).

Official release chronology: Apache Hadoop, **release 0.18.0 available**, **22 August 2008**: <https://hadoop.apache.org/release/0.18.0.html>

Exact released source: <https://github.com/apache/hadoop/blob/release-0.18.0/src/hdfs/org/apache/hadoop/dfs/FSNamesystem.java>

### Directly inspected anchors

The source-level bookkeeping comment states that:

- the valid filesystem name → block list is kept on disk/logged;
- `block -> machinelist` is **kept in memory, rebuilt dynamically from reports**.

The `datanodeMap` documentation further says the descriptor list is checkpointed in the namespace image, but only the `DatanodeInfo` portion is persistent and the list of blocks is restored from DataNode block reports.

During `FSNamesystem` initialization the implementation loads `FSImage`, creates `SafeModeInfo(conf)`, and sets the total-block denominator. The startup `SafeModeInfo(Configuration)` has a threshold, extension, minimum safe replication, `blockTotal`, `blockSafe`, and reached-state accounting. Its release-specific defaults are:

- `dfs.safemode.threshold.pct = 0.95f`;
- `dfs.safemode.extension = 0`;
- `dfs.replication.min = 1`.

The same source has a separate no-argument `SafeModeInfo()` for manual entry, uses sentinel/unreachable automatic-exit values, and exposes `isManual()` via `blockTotal == -1`.

### Supported boundaries

- `checkpointed namespace / DataNode descriptor state ≠ checkpointed block-location inventory`;
- `startup SafeMode ≠ manual SafeMode`;
- `2008 0.95 + no extension ≠ later 0.999 + 30 s defaults`;
- `released HDFS implementation floor ≠ invention priority`.

This exact source is stronger than using a later architecture rendering merely to infer what the 2008 release already did.

---

'''
if "## Source 0 — Apache Hadoop 0.18.0 exact implementation" not in e79:
    e79 = e79.replace(source1_anchor, source0 + source1_anchor, 1)

tri_anchor = "## Source triangulation\n\nThe case is `grounded` because the central relation is supported at several levels:\n\n"
if tri_anchor not in e79:
    raise SystemExit("Evidence 79 triangulation anchor not found")
tri_new = (
    "1. **exact released 0.18.0 source (2008)** — explicitly marks block→machine location state as in-memory/report-rebuilt and already distinguishes startup from manual SafeMode;\n"
    "2. **2010 system architecture paper** — location state is not in the persistent checkpoint and is re-learned from DataNodes;\n"
    "3. **versioned Apache documentation** — startup SafeMode waits for reported minimum-replica evidence and postpones block replication;\n"
    "4. **tag-matched 2.7.3 implementation** — the SafeMode counters, threshold/extension checks, mutation gate, and replication-queue gating are inspectable;\n"
    "5. **tag-matched configuration source** — release defaults show why SafeMode `safe` cannot be normalized into `full configured redundancy`;\n"
    "6. **2.8.0 source continuity** — explicitly preserves the lifecycle distinction between automatic startup SafeMode and manual entry.\n"
)
# Replace old numbered block up to negative claims.
start = e79.index(tri_anchor) + len(tri_anchor)
end_marker = "\n---\n\n## Negative claims / evidence limits"
end = e79.index(end_marker, start)
e79 = e79[:start] + tri_new + e79[end:]

prior_old = "Apache HDFS 1.0.4 already documents the mechanism before the 2.7.3 implementation used for source-level inspection."
prior_new = "Exact released Hadoop 0.18.0 source already implements the report-rebuilt location relation and distinct startup/manual SafeMode state before the 2010 paper and later 1.x/2.x documentation used for continuity."
e79 = e79.replace(prior_old, prior_new)
status_old = "Reason: the central claim is triangulated by a contemporary system paper, versioned Apache documentation, and exact tag-matched source/configuration."
status_new = "Reason: the central claim is triangulated by exact released 0.18.0 implementation source, a contemporary 2010 system paper, versioned Apache documentation, and later tag-matched source/configuration through 2.8.0."
e79 = e79.replace(status_old, status_new)

if "## Source 6 — Hadoop 2.8.0 `FSNamesystem.SafeModeInfo` continuity" not in e79:
    source6_anchor = "\n---\n\n## Source triangulation"
    source6 = r'''
---

## Source 6 — Hadoop 2.8.0 `FSNamesystem.SafeModeInfo` continuity

**Type:** released primary implementation source (`P/H`).

<https://hadoop.apache.org/docs/r2.8.0/hadoop-project-dist/hadoop-hdfs/api/src-html/org/apache/hadoop/hdfs/server/namenode/FSNamesystem.SafeModeInfo.html>

The class documentation explicitly says startup SafeMode counts safe blocks and uses threshold/extension progress for automatic exit, while manually entered SafeMode does not track safe blocks for that automatic-exit lifecycle because it is not intended to leave automatically on the startup condition.

This is a later continuity witness, not evidence that the distinction originated in 2.8.0; exact 0.18.0 source already contains a separate manual `SafeModeInfo()` state and `isManual()` discriminator.

### Consolidation note

A later repository slice accidentally created `Case 117` for the same HDFS startup-SafeMode mechanism already grounded here. Its genuinely useful additions — the exact 2008 chronology floor, manual/startup lifecycle emphasis, and cross-controls with Cases 80/83/116 — are now absorbed into canonical Case 79. The old Case-117 paths remain only as link-stability stubs.
'''
    e79 = e79.replace(source6_anchor, source6 + source6_anchor, 1)
write(e79_path, e79)


# 3) Replace accidental duplicate paths with link-stability stubs.
case117_path = "cases/117-apache-hdfs-startup-safemode-reobservation.md"
case117_stub = r'''# Consolidated into Case 79 — HDFS Startup SafeMode

**Status:** `retired duplicate / link-stability stub`.

This path is intentionally retained so existing repository and external links do not break.

The research slice previously stored here duplicated the already-grounded HDFS startup-SafeMode mechanism in:

- [`79-apache-hdfs-startup-safemode-block-report-reobservation.md`](79-apache-hdfs-startup-safemode-block-report-reobservation.md)
- [`../evidence/79-hadoop-2010-2016-startup-safemode-grounding.md`](../evidence/79-hadoop-2010-2016-startup-safemode-grounding.md)

Its unique useful evidence has been folded into Case 79, including:

- the exact released Hadoop 0.18.0 `FSNamesystem.java` implementation floor;
- the startup-versus-manual SafeMode lifecycle distinction;
- release-specific threshold/extension evolution;
- cross-case controls with HDFS placement, integrity scanning, and DataNode maintenance.

No independent Case 117 claim remains. Use **Case 79** as the canonical citation and comparison target.
'''
write(case117_path, case117_stub)

e117_path = "evidence/117-hadoop-2008-2017-startup-safemode-grounding.md"
e117_stub = r'''# Consolidated into Evidence 79 — HDFS Startup SafeMode

**Status:** `retired duplicate / link-stability stub`.

This evidence path remains only to preserve old links. Its non-duplicative material has been merged into:

[`79-hadoop-2010-2016-startup-safemode-grounding.md`](79-hadoop-2010-2016-startup-safemode-grounding.md)

The canonical record now includes exact released Hadoop 0.18.0 source evidence, the later startup/manual SafeMode continuity witness, and the relevant cross-case guardrails. Do not cite this stub as a separate evidence package.
'''
write(e117_path, e117_stub)


# 4) ROADMAP: remove duplicate Case 117 line and deepen the existing Case 79 line.
roadmap_path = "ROADMAP.md"
roadmap = read(roadmap_path)
road_lines = roadmap.splitlines()
filtered = []
removed_117 = 0
for line in road_lines:
    if "cases/117-apache-hdfs-startup-safemode-reobservation.md" in line:
        removed_117 += 1
        continue
    if "cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md" in line:
        line = "- [x] HDFS startup SafeMode / block-report re-observation — canonical [`cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md`](cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md), grounded by expanded [`evidence/79-hadoop-2010-2016-startup-safemode-grounding.md`](evidence/79-hadoop-2010-2016-startup-safemode-grounding.md), now spans exact released Hadoop 0.18.0 implementation evidence through 2.8.0 continuity. The 0.18.0 source directly marks block→machine location state as in-memory/report-rebuilt, already distinguishes startup and manual SafeMode, and exposes release-specific 0.95/no-extension defaults; later 1.x/2.x evidence shows quantitative policy evolution without changing the core replay/re-observation distinction. The accidental duplicate Case 117 has been consolidated here with link-stability stubs. This remains separate from placement qualification (Case 80), checksum integrity (Case 83), DataNode maintenance (Case 116), HA command fencing (Case 51), and Observer freshness (Case 61); broader recovery genealogy belongs in `computing-archaeology`."
    filtered.append(line)
if removed_117 != 1:
    raise SystemExit(f"Expected exactly one duplicate Case 117 roadmap line, removed {removed_117}")
roadmap = "\n".join(filtered)
write(roadmap_path, roadmap)


# 5) CASE_INDEX: remove duplicate row, deepen canonical row, preserve finding IDs.
index_path = "CASE_INDEX.md"
index = read(index_path)
lines = index.splitlines()
out = []
removed_row = 0
for line in lines:
    if "| [Apache HDFS Startup Safemode: Namespace Recovery, Block Re-observation, and Withheld Mutation Authority](cases/117-apache-hdfs-startup-safemode-reobservation.md)" in line:
        removed_row += 1
        continue
    if "| [Apache HDFS Startup SafeMode: Reconstructed Block Locations, Re-observed Replicas, and Delayed Repair Authority](cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md)" in line:
        line = "| [Apache HDFS Startup SafeMode: Reconstructed Block Locations, Re-observed Replicas, and Delayed Repair Authority](cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md) | **grounded** | persistent NameNode namespace + DataNode-resident block replicas + report-rebuilt location state + SafeMode safe-block/threshold/extension state + distinct startup/manual lifecycle + post-exit replication queues | separate durable namespace from current replica-location knowledge; physical replica survival from re-observed availability; Blockreport from repair; startup admission from full redundancy/integrity/placement; and one named SafeMode from one timeless quantitative contract | [expanded 2008–2017 HDFS startup/SafeMode grounding](evidence/79-hadoop-2010-2016-startup-safemode-grounding.md), now including exact released 0.18.0 implementation and later 2.8.0 lifecycle continuity; old Case-117 paths are retired link-stability stubs; broader recovery genealogy, HA/resource-low/EC startup, production incidents, and fault injection remain separate work |"
    out.append(line)
if removed_row != 1:
    raise SystemExit(f"Expected exactly one duplicate Case 117 index row, removed {removed_row}")
index = "\n".join(out)
index = index.replace(
    "## Case 117 — HDFS startup Safemode findings",
    "## Case 79 deepening — HDFS startup SafeMode consolidation findings",
)
index = index.replace(
    "- **1830 — 2008 released HDFS Safemode record != invention priority:** Apache's 22 August 2008 Hadoop 0.18.0 release and early HDFS architecture documentation provide a public HDFS chronology floor, not proof of the first recovery gate, read-only startup mode, or distributed-storage Safemode concept. (`H/P`, `X`)",
    "- **1830 — exact 2008 released HDFS SafeMode implementation != invention priority:** Apache's 22 August 2008 Hadoop 0.18.0 release plus exact `release-0.18.0` `FSNamesystem.java` directly show report-rebuilt block-location state and startup/manual SafeMode control; this is a public HDFS implementation floor, not proof of the first recovery gate, read-only startup mode, or distributed-storage SafeMode concept. (`H/P`, `X`)",
)
index = index.replace(
    "- **1837 — startup Safemode != manual Safemode:** Hadoop 2.8.0 source tracks safe blocks for automatic startup exit but explicitly does not use that automatic-exit lifecycle for manually entered Safemode. (`H/P`)",
    "- **1837 — startup SafeMode != manual SafeMode:** exact 0.18.0 source already uses separate startup/manual `SafeModeInfo` state, and Hadoop 2.8.0 source explicitly preserves the lifecycle distinction by tracking safe blocks for automatic startup exit but not for manually entered SafeMode. (`H/P`)",
)
index = index.replace(
    "- **1845 — Case 117 startup Safemode != Case 116 DataNode maintenance mode:** the former is a NameNode-wide startup admission gate while replica-location evidence is rebuilt; the latter is a per-DataNode temporary-withdrawal/expiry regime. The comparison is functional only and establishes no genealogy. (`A`, `X`)",
    "- **1845 — Case 79 startup SafeMode != Case 116 DataNode maintenance mode:** the former is a NameNode-wide startup admission gate while replica-location evidence is rebuilt; the latter is a per-DataNode temporary-withdrawal/expiry regime. The comparison is functional only and establishes no genealogy. (`A`, `X`)",
)
index = index.replace(
    "- **1846 — related-repository boundary:** current `tmzncty/computing-archaeology` search found no dedicated HDFS Safemode case; broader HDFS/GFS recovery genealogy and Blockreport history belong there if developed, while Case 117 keeps only the retention-specific replay/re-observation/admission relation. (`H/P` project-state record)",
    "- **1846 — related-repository and duplicate-consolidation boundary:** current `tmzncty/computing-archaeology` search found no dedicated HDFS SafeMode case; broader HDFS/GFS recovery genealogy and Blockreport history belong there if developed. The accidental Case 117 duplicate has been retired into link-stability stubs, while canonical Case 79 keeps the retention-specific replay/re-observation/admission relation. (`H/P` project-state record)",
)
write(index_path, index)


# 6) Bounded validation.
checks = {
    case79_path: ["exact released source from Hadoop 0.18.0", "startup SafeMode ≠ manual SafeMode"],
    e79_path: ["Source 0 — Apache Hadoop 0.18.0 exact implementation", "Source 6 — Hadoop 2.8.0"],
    case117_path: ["retired duplicate / link-stability stub", "Use **Case 79**"],
    e117_path: ["retired duplicate / link-stability stub", "Do not cite this stub"],
    roadmap_path: ["canonical [`cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md`]"],
    index_path: ["Case 79 deepening — HDFS startup SafeMode consolidation findings", "exact 2008 released HDFS SafeMode implementation"],
}
for path, needles in checks.items():
    text = read(path)
    for needle in needles:
        if needle not in text:
            raise SystemExit(f"Missing expected text in {path}: {needle}")

if "cases/117-apache-hdfs-startup-safemode-reobservation.md" in read(roadmap_path):
    raise SystemExit("Duplicate Case 117 still present in ROADMAP")
if "cases/117-apache-hdfs-startup-safemode-reobservation.md) | **grounded**" in read(index_path):
    raise SystemExit("Duplicate Case 117 row still present in CASE_INDEX")

print("Case 117 duplicate consolidated into canonical Case 79")
