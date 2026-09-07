from pathlib import Path

CASE = Path('cases/58-raft-snapshot-log-compaction.md')
EVID = Path('evidence/58-raft-2014-snapshot-log-compaction-grounding.md')
ROAD = Path('ROADMAP.md')
INDEX = Path('CASE_INDEX.md')
MARKER = 'Birrell 1987 checkpoint/log replay + Chubby 2006 WAL/snapshot prior-art floor'


def replace_section(text: str, start: str, end: str, replacement: str) -> str:
    a = text.find(start)
    if a < 0:
        raise SystemExit(f'missing start anchor: {start}')
    b = text.find(end, a + len(start))
    if b < 0:
        raise SystemExit(f'missing end anchor: {end}')
    return text[:a] + replacement.rstrip() + '\n\n' + text[b:]


case = CASE.read_text(encoding='utf-8')
evid = EVID.read_text(encoding='utf-8')
road = ROAD.read_text(encoding='utf-8')
index = INDEX.read_text(encoding='utf-8')

if MARKER in case or MARKER in evid or MARKER in road or MARKER in index:
    raise SystemExit('prior-art slice already integrated')

case_prior = '''## Prior art and novelty boundary

### H/P — 1987 checkpoint + log replay is an earlier mechanism floor

Birrell, Jones, and Wobber's 1987 small-database design records updates incrementally in an on-disk log, occasionally checkpoints the entire database, and recovers after a crash by restoring an older checkpoint and replaying the later log. This predates Raft by decades and is direct evidence that `materialized checkpoint + retained suffix replay` is not a Raft invention.

This floor is intentionally narrow. The 1987 paper is a small-database recovery design, not a replicated-consensus snapshot protocol. It does not establish Raft-style `lastIncludedIndex` / `lastIncludedTerm`, membership continuation metadata, or leader-to-follower `InstallSnapshot` semantics.

### H/P — Chubby 2006 combines WAL/snapshotting with a consensus-distributed database log

Burrows's 2006 Chubby paper states that Chubby rewrote its database using write-ahead logging and snapshotting similar to Birrell et al., while the database log was distributed among replicas using a distributed consensus protocol. It separately describes periodic backup snapshots written to GFS for disaster recovery and initialization of replacement replicas.

This is a stronger pre-Raft distributed-system floor than a generic local checkpoint, but the evidence still does not license semantic collapse. The paper does not specify that Chubby's ordinary database snapshot carries Raft's later index/term boundary contract or that lagging replicas use an `InstallSnapshot`-equivalent RPC under identical rules. Chubby's off-cell backup snapshots are also a distinct operational role from the database's snapshot/log mechanism and must not be silently merged with it.

### H/P — Raft itself acknowledges snapshotting prior art

Section 7 of the 2014 Raft paper explicitly says snapshotting is used in Chubby and ZooKeeper and names log cleaning and log-structured merge trees as other compaction approaches. Raft therefore does not present the generic idea of snapshotting/log compaction as its invention.

### E/A — earlier mechanism floor ≠ proven direct implementation genealogy

The historically safe relation is:

```text
1987 Birrell et al.
    checkpoint whole database + replay later log
        -> earlier checkpoint/replay mechanism floor

2006 Chubby
    WAL + snapshotting similar to Birrell
    + database log distributed by consensus
        -> earlier distributed-service floor

2014 Raft
    snapshot committed/applied state
    + lastIncludedIndex / lastIncludedTerm / configuration
    + explicit InstallSnapshot recovery path
        -> a later, explicitly specified consensus-continuation contract
```

The arrows above mean **chronological/mechanism comparison only**. They do not assert source-code descent, exclusive influence, invention priority, or an uninterrupted Birrell → Chubby → Raft implementation lineage.

The defensible project contribution is therefore:

> **Raft 2014 supplies a particularly explicit primary-source case in which consensus-ordered committed history is replaceable by stable current state plus boundary/membership metadata, and in which that representation change alters the repair path for lagging replicas. Earlier checkpoint/log-replay and Chubby WAL/snapshot evidence constrain novelty claims without erasing Raft's distinct protocol contract.**
'''
case = replace_section(case, '## Prior art and novelty boundary', '## Source ledger', case_prior)

case_sources = '''## Source ledger

1. Diego Ongaro and John Ousterhout, **“In Search of an Understandable Consensus Algorithm (Extended Version)”**, published May 20, 2014, official author/project PDF: <https://raft.github.io/raft.pdf>.
   - Figure 2: persistent versus volatile Raft state.
   - §§5.3–5.4: commitment/application context.
   - §7 and Figures 12–13: snapshotting, retained metadata, covered-prefix deletion, `InstallSnapshot`, receiver behavior, cadence tradeoffs, and Raft's own prior-art boundary.
2. **The Raft Consensus Algorithm**, official author/project publication index: <https://raft.github.io/>. Used for provenance/publication navigation, not as a substitute for the paper's mechanism details.
3. Andrew D. Birrell, Michael B. Jones, and Edward P. Wobber, **“A Simple and Efficient Implementation for Small Databases”**, SOSP 1987 / DEC SRC Research Report 24. Author-hosted report: <https://birrell.org/andrew/papers/024-DatabasesPaper.pdf>; institutional publication record: <https://www.microsoft.com/en-us/research/publication/a-simple-and-efficient-implementation-for-small-databases/>.
   - Direct prior-art floor for incremental on-disk logging, occasional whole-database checkpointing, and crash recovery by checkpoint restore plus log replay.
   - Not evidence for Raft consensus metadata or `InstallSnapshot` semantics.
4. Mike Burrows, **“The Chubby lock service for loosely-coupled distributed systems”**, OSDI 2006, USENIX: <https://static.usenix.org/events/osdi06/tech/full_papers/burrows/burrows_html/>.
   - §2.10: Chubby database rewrite using write-ahead logging and snapshotting similar to Birrell et al.; database log distributed among replicas using consensus.
   - §2.11: periodic backup snapshots to GFS for disaster recovery/replacement-replica initialization, kept separate here from the ordinary database snapshot/log mechanism.

A search of `tmzncty/computing-archaeology` for Raft/snapshot/InstallSnapshot and, in this deepening pass, Birrell/Chubby checkpoint terms found no dedicated case to reuse. Broader consensus/checkpoint genealogy should still be routed there if later needed; this repository keeps only the retention-specific mechanism and novelty boundary.
'''
case = replace_section(case, '## Source ledger', '## Claim ledger', case_sources)

findings_anchor = '16. **Raft 2014 snapshotting ≠ invention of snapshotting/log compaction.**'
if findings_anchor not in case:
    raise SystemExit('missing Case 58 findings anchor')
case = case.replace(findings_anchor, findings_anchor + '''\n17. **1987 checkpoint + log replay ≠ replicated-consensus snapshot protocol.**\n18. **Checkpoint/replay materialization predates Raft 2014.**\n19. **Chubby 2006 WAL + snapshotting + consensus-distributed log ≠ Raft `InstallSnapshot` contract.**\n20. **Chubby database snapshotting ≠ Chubby off-cell backup snapshot role.**\n21. **Earlier mechanism floor ≠ proven direct Birrell → Chubby → Raft implementation genealogy.**''', 1)

# Evidence: replace the thin prior-art note with direct earlier sources and explicit boundaries.
evid_prior = '''### §7 — Raft's own prior-art statement

The paper states that snapshotting is used in Chubby and ZooKeeper and names log cleaning and log-structured merge trees as incremental alternatives.

**Rejected claim:** `Raft 2014 invented snapshotting/log compaction`.

### Earlier mechanism floor — Birrell, Jones, and Wobber 1987

The 1987 paper's publication record and report describe a small database that records updates incrementally on disk in a log, occasionally makes a checkpoint of the entire database, and recovers by restoring an older checkpoint and replaying the later log.

**Grounded boundary:** `checkpoint + suffix replay predates Raft`; `generic database checkpoint/replay ≠ Raft consensus snapshot semantics`.

### Earlier distributed-service floor — Chubby 2006

Chubby §2.10 states that its rewritten database uses write-ahead logging and snapshotting similar to Birrell et al., while its database log is distributed among replicas using a distributed consensus protocol. §2.11 separately describes periodic GFS backup snapshots for disaster recovery and replacement-replica initialization.

**Grounded boundaries:** `pre-Raft consensus-distributed log + snapshotting exists`; `Chubby WAL/snapshot design ≠ demonstrated Raft InstallSnapshot contract`; `database snapshotting ≠ off-cell backup role`.

### Novelty/genealogy guardrail

The direct evidence supports chronological and functional prior-art floors. It does **not** by itself prove source-code descent, exclusive intellectual influence, or an uninterrupted Birrell → Chubby → Raft implementation genealogy.

**Grounded boundary:** `earlier analogous mechanism ≠ proven direct genealogy`.
'''
evid = replace_section(evid, '### §7 — prior art', '## Source 2 — official Raft publication index', evid_prior)

source2_start = '## Source 2 — official Raft publication index'
related_start = '## Related-repository duplication check'
a = evid.find(source2_start)
b = evid.find(related_start, a)
if a < 0 or b < 0:
    raise SystemExit('missing Evidence 58 source anchors')
source_block = evid[a:b].rstrip() + '''\n\n## Source 3 — Birrell/Jones/Wobber 1987 checkpoint + log replay\n\nAndrew D. Birrell, Michael B. Jones, and Edward P. Wobber, **“A Simple and Efficient Implementation for Small Databases”**, SOSP 1987 / DEC SRC Research Report 24. Author-hosted report: <https://birrell.org/andrew/papers/024-DatabasesPaper.pdf>. Institutional publication record: <https://www.microsoft.com/en-us/research/publication/a-simple-and-efficient-implementation-for-small-databases/>.\n\nUsed only for the earlier mechanism floor: incremental disk log, occasional whole-database checkpoint, and crash recovery by restoring a checkpoint then replaying the log. No Raft-style consensus metadata is inferred.\n\n## Source 4 — Chubby 2006 WAL/snapshot + consensus-distributed log\n\nMike Burrows, **“The Chubby lock service for loosely-coupled distributed systems”**, OSDI 2006, USENIX HTML: <https://static.usenix.org/events/osdi06/tech/full_papers/burrows/burrows_html/>.\n\n- §2.10 grounds the rewritten Chubby database's write-ahead logging and snapshotting, its explicit similarity to Birrell et al., and consensus distribution of the database log.\n- §2.11 grounds the separate GFS backup-snapshot role.\n\nUsed as a pre-Raft distributed-service floor, not as evidence that Chubby implemented Raft's later boundary metadata or `InstallSnapshot` receiver rules.\n\n'''
evid = evid[:a] + source_block + evid[b:]

# Roadmap: mark the bounded prior-art deepening as complete without closing broader genealogy.
road_anchor = '## Phase 2 — Build missing technical bridges\n\n'
if road_anchor not in road:
    raise SystemExit('missing ROADMAP Phase 2 anchor')
road_bullet = '- [x] Raft snapshot/log-compaction prior-art floor deepening — Case 58 now directly grounds the ' + MARKER + ', separating generic checkpoint/replay, Chubby database snapshotting with a consensus-distributed log, Chubby off-cell backup snapshots, and Raft\'s 2014 `lastIncludedIndex` / `lastIncludedTerm` / configuration + `InstallSnapshot` contract. This closes only the bounded novelty guardrail; broader checkpoint/consensus genealogy, implementation crash windows, production snapshot formats, and fault injection remain open.\n'
road = road.replace(road_anchor, road_anchor + road_bullet, 1)

# Case-index navigation/status: annotate the existing Case 58 row without assuming table-column wording.
idx_lines = index.splitlines()
found = False
for i, line in enumerate(idx_lines):
    if '(cases/58-raft-snapshot-log-compaction.md)' in line:
        if MARKER in line:
            raise SystemExit('CASE_INDEX already updated')
        stripped = line.rstrip()
        if not stripped.endswith('|'):
            raise SystemExit('unexpected Case 58 row shape')
        idx_lines[i] = stripped[:-1].rstrip() + '; ' + MARKER + ' now directly grounded; direct genealogy remains unclaimed |'
        found = True
        break
if not found:
    raise SystemExit('missing Case 58 CASE_INDEX row')
index = '\n'.join(idx_lines) + '\n'

# Normalize EOF and validate intended boundaries.
for path, text in [(CASE, case), (EVID, evid), (ROAD, road), (INDEX, index)]:
    text = text.rstrip() + '\n'
    if '\t' in text:
        raise SystemExit(f'tab introduced in {path}')
    path.write_text(text, encoding='utf-8')

checks = {
    CASE: [MARKER.split(' + ')[0], 'Birrell → Chubby → Raft', 'Chubby database snapshotting ≠ Chubby off-cell backup snapshot role'],
    EVID: ['Source 3 — Birrell/Jones/Wobber 1987', 'Source 4 — Chubby 2006', 'earlier analogous mechanism ≠ proven direct genealogy'],
    ROAD: [MARKER, 'broader checkpoint/consensus genealogy'],
    INDEX: [MARKER],
}
for path, needles in checks.items():
    text = path.read_text(encoding='utf-8')
    for needle in needles:
        if needle not in text:
            raise SystemExit(f'missing {needle!r} in {path}')

print('Case 58 prior-art deepening integrated')
