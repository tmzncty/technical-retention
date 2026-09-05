from pathlib import Path
import re

ROOT = Path('.')
CASE41 = ROOT / 'cases/41-apache-cassandra-tombstone-gc-grace-resurrection.md'
EVID41 = ROOT / 'evidence/41-cassandra-3x-tombstone-repair-grounding.md'
CASE91 = ROOT / 'cases/91-apache-cassandra-tombstone-grace-zombie-prevention.md'
EVID91 = ROOT / 'evidence/91-cassandra-2006-2014-tombstone-grace-grounding.md'

OLD_CASE_PATH = 'cases/91-apache-cassandra-tombstone-grace-zombie-prevention.md'
OLD_EVID_PATH = 'evidence/91-cassandra-2006-2014-tombstone-grace-grounding.md'
NEW_CASE_PATH = 'cases/41-apache-cassandra-tombstone-gc-grace-resurrection.md'
NEW_EVID_PATH = 'evidence/41-cassandra-3x-tombstone-repair-grounding.md'

case_deepening = r'''
## Historical deepening — Cassandra 1.2.19, local purge ordering, and pre-Cassandra prior art

The canonical case is centered on Cassandra 3.x because that release family exposes the later repair-aware purge option especially clearly. A separate later-added Case 91 repeated most of the same tombstone / grace / resurrection mechanism while adding useful older evidence. That older evidence is retained here rather than maintained as a duplicate case.

### H/P — Cassandra 1.2.19 makes the deletion marker an explicit retained object

The `cassandra-1.2.19` source contains `DeletedColumn`, a `Column` subclass whose deletion state is represented explicitly: `isMarkedForDelete()` returns true, `getMarkedForDeleteAt()` returns the column timestamp, `getLocalDeletionTime()` retains the local deletion time, and serialization uses the deletion mask.

**Primary anchor:** Apache Cassandra `DeletedColumn.java`, tag `cassandra-1.2.19`: <https://github.com/apache/cassandra/blob/cassandra-1.2.19/src/java/org/apache/cassandra/db/DeletedColumn.java>.

This is direct implementation evidence for a narrow point already used by the case: deletion is not represented merely by absence; negative/currentness state has an embodiment of its own.

### H/P — the 1.2.19 grace interval is policy state, while overlap still constrains local purge

`CFMetaData.java` in the same tag defines `DEFAULT_GC_GRACE_SECONDS = 864000` for ordinary user tables. More importantly, `CompactionController.shouldPurge(key, maxDeletionTimestamp)` is documented around the condition that all versions of the row be present in the compaction set; it checks overlapping SSTables and refuses purge when an overlapping SSTable can still contain a version at or before the deletion timestamp.

**Primary anchors:**

- <https://github.com/apache/cassandra/blob/cassandra-1.2.19/src/java/org/apache/cassandra/config/CFMetaData.java>
- <https://github.com/apache/cassandra/blob/cassandra-1.2.19/src/java/org/apache/cassandra/db/compaction/CompactionController.java>

The historical/engineering boundary is therefore sharper than `ten days makes deletion safe`:

```text
grace age
    -> purge eligibility input

but

overlapping older representations
    -> can still block local purge
```

`safe-forgetting closure` remains a project reconstruction, not Cassandra vocabulary.

### H/P — CASSANDRA-7810 is a one-node counterexample to “this is only a stale-replica problem”

ASF issue **CASSANDRA-7810**, resolved in August 2014 with fix versions including 1.2.19, 2.0.11, and 2.1.0, reproduces resurrection in a single-node cluster with `gc_grace_seconds = 0`: insert, delete, flush, compact, and the deleted row reappears. The issue diagnosis is that expired tombstones were discarded before their suppressive effect had been correctly applied during compaction. Cassandra 1.2.19 `CHANGES.txt` records `Track expired tombstones (CASSANDRA-7810)`.

**Primary/institutional anchors:**

- <https://issues.apache.org/jira/browse/CASSANDRA-7810>
- <https://github.com/apache/cassandra/blob/cassandra-1.2.19/CHANGES.txt>

This adds a distinct failure boundary to the distributed zombie example: even with no remote stale replica, **retiring negative evidence in the wrong local operation order can restore older positive state**.

### H/P prior art — deletion entries that must survive non-major compaction predate Cassandra

Chang et al.'s **Bigtable** paper (OSDI 2006), §5.4, states that SSTables produced by non-major compactions can contain `special deletion entries` that suppress deleted data in older live SSTables; a major compaction can later produce an SSTable containing neither deletion information nor deleted data.

**Primary anchor:** Fay Chang et al., “Bigtable: A Distributed Storage System for Structured Data,” OSDI 2006, §5.4, HTML proceedings: <https://static.usenix.org/event/osdi06/tech/chang/chang_html/>.

This is earlier primary prior art for the **function** `retain deletion evidence while older immutable representations remain live, then retire both when compaction closes the relation`. It does **not** establish implementation identity, direct Bigtable → Cassandra code descent, or invention priority for the wider tombstone concept.

### Version boundary preserved

Do not project the later Cassandra 3.x `only_purge_repaired_tombstones` option backward into 1.2.19. Conversely, do not use the older `DeletedColumn` embodiment as if it were the exact encoding of every later tombstone type. The canonical case now intentionally uses two bounded historical layers:

- 1.2.19 / 2014 for explicit deletion-marker embodiment, overlap-aware purge, and the CASSANDRA-7810 local sequencing failure;
- 3.x / 3.11 for the later documented hints/repair/grace model and repair-qualified purge option.

---
'''

evidence_deepening = r'''
## Historical deepening — exact 1.2.19 artifacts, CASSANDRA-7810, and Bigtable prior art

This section absorbs the unique evidence from the now-consolidated later Case 91. It does not change the canonical Case 41 thesis; it gives that thesis a deeper historical and implementation floor.

### P7 — Apache Cassandra `DeletedColumn.java`, tag `cassandra-1.2.19`

**URL:** <https://github.com/apache/cassandra/blob/cassandra-1.2.19/src/java/org/apache/cassandra/db/DeletedColumn.java>

Directly inspected implementation facts retained from the older evidence slice:

- `DeletedColumn` extends `Column`;
- `isMarkedForDelete()` returns true;
- `getMarkedForDeleteAt()` returns the column timestamp;
- `getLocalDeletionTime()` decodes retained local deletion time;
- serialization uses `ColumnSerializer.DELETION_MASK`.

**Use:** strong primary implementation evidence that a deletion marker is first-class retained database state, not mere absence.

**Boundary:** this does not describe every later Cassandra tombstone kind or encoding.

### P8 — Apache Cassandra `CFMetaData.java`, tag `cassandra-1.2.19`

**URL:** <https://github.com/apache/cassandra/blob/cassandra-1.2.19/src/java/org/apache/cassandra/config/CFMetaData.java>

`DEFAULT_GC_GRACE_SECONDS = 864000` provides an exact 1.2.19 implementation witness for the ordinary user-table ten-day default.

**Use:** grounds a historical retention-policy timescale distinct from deleted-value lifetime.

**Boundary:** a configured time window is not proof of repair or global convergence.

### P9 — Apache Cassandra `CompactionController.java`, tag `cassandra-1.2.19`

**URL:** <https://github.com/apache/cassandra/blob/cassandra-1.2.19/src/java/org/apache/cassandra/db/compaction/CompactionController.java>

`shouldPurge(key, maxDeletionTimestamp)` checks overlapping SSTables and refuses purge when an overlapping SSTable may still contain an older version at or before the deletion timestamp.

**Use:** direct implementation evidence that elapsed grace is not the complete local purge condition; older shadowed representations outside the compaction set remain relevant.

**Boundary:** this is local compaction admissibility, not proof that every distributed replica has converged.

### P10 — CASSANDRA-7810 and Cassandra 1.2.19 `CHANGES.txt`

**Issue:** <https://issues.apache.org/jira/browse/CASSANDRA-7810>

**Release record:** <https://github.com/apache/cassandra/blob/cassandra-1.2.19/CHANGES.txt>

The ASF defect record reproduces a deleted row reappearing on a **single node** with `gc_grace_seconds = 0` after flush/compaction, and records fix versions 1.2.19, 2.0.11, and 2.1.0. The 1.2.19 change record includes `Track expired tombstones (CASSANDRA-7810)`.

**Use:** strong project/institutional evidence that purge sequencing itself is semantically significant: a tombstone can be old enough to collect yet still be needed to suppress an older local representation during the current compaction operation.

**Boundary:** this one defect does not explain every Cassandra resurrection bug.

### P11 — Chang et al., Bigtable, OSDI 2006, §5.4

**HTML proceedings:** <https://static.usenix.org/event/osdi06/tech/chang/chang_html/>

The paper states that SSTables produced by non-major compactions can contain `special deletion entries` that suppress deleted data in older live SSTables; a major compaction can later produce an SSTable with neither deletion information nor deleted data.

**Use:** earlier primary prior art for temporarily retaining deletion evidence across immutable representations and later retiring it through a stronger compaction closure.

**Boundary:** prior function is not implementation identity and does not prove a direct Bigtable → Cassandra genealogy.

### Cross-version claim controls added by the deepening

| Claim | Type | Grounding | Boundary |
| --- | --- | --- | --- |
| Cassandra 1.2.19 represents column deletion with explicit `DeletedColumn` state | `H/P` | P7 | exact tagged implementation, not every later encoding |
| 1.2.19 ordinary user-table default grace is 864000 seconds | `H/P` | P8 | policy default, not convergence proof |
| older overlapping SSTable state can block local tombstone purge | `H/P` | P9 | local compaction relation only |
| CASSANDRA-7810 resurrected a deleted row on one node when expired tombstones were discarded too early | `H/P` | P10 | one historical defect class |
| deletion-marker retention across immutable SSTables predates Cassandra | `H/P` prior art | P11 | functional prior art, not direct genealogy |
| `only_purge_repaired_tombstones` existed in Cassandra 1.2.19 | `X` | contradicted by version boundary used here | rejected |
| Bigtable deletion entries and Cassandra tombstones are implementation-identical | `X` | none | rejected |

---
'''

# 1. Deepen canonical Case 41.
case41 = CASE41.read_text()
if '## Historical deepening — Cassandra 1.2.19, local purge ordering, and pre-Cassandra prior art' not in case41:
    marker = '\n## Retained state\n'
    assert marker in case41, 'Case 41 insertion marker missing'
    case41 = case41.replace(marker, '\n' + case_deepening + marker, 1)
CASE41.write_text(case41)

# 2. Deepen canonical evidence record.
evid41 = EVID41.read_text()
if '## Historical deepening — exact 1.2.19 artifacts, CASSANDRA-7810, and Bigtable prior art' not in evid41:
    marker = '\n## Claim ledger\n'
    assert marker in evid41, 'Evidence 41 insertion marker missing'
    evid41 = evid41.replace(marker, '\n' + evidence_deepening + marker, 1)
EVID41.write_text(evid41)

# 3. Remove duplicate case/evidence files after their unique material has been absorbed.
assert CASE91.exists(), 'duplicate Case 91 file unexpectedly absent before consolidation'
assert EVID91.exists(), 'duplicate Case 91 evidence unexpectedly absent before consolidation'
CASE91.unlink()
EVID91.unlink()

# 4. Update CASE_INDEX canonically: remove duplicate row, deepen Case 41 row, retain finding IDs but rewrite duplicate findings as historical deepening.
idx_path = ROOT / 'CASE_INDEX.md'
idx = idx_path.read_text()
idx = ''.join(line for line in idx.splitlines(keepends=True) if OLD_CASE_PATH not in line and OLD_EVID_PATH not in line)

case41_row_re = re.compile(r'^\| \[Apache Cassandra GC Grace: Tombstone Retention, Repair Windows, and Data Resurrection\]\(cases/41-apache-cassandra-tombstone-gc-grace-resurrection\.md\).*?\|\n', re.M)
case41_row = '| [Apache Cassandra GC Grace: Tombstone Retention, Repair Windows, and Data Resurrection](cases/41-apache-cassandra-tombstone-gc-grace-resurrection.md) | **grounded** | replicated positive values + timestamped tombstone negative state + hints/repair + SSTable repaired/unrepaired state + overlap-aware compaction + version-bounded purge controls | show deletion can depend on retained negative evidence; separate marker age, local shadow closure, replica convergence, repair evidence, and physical reclamation; use CASSANDRA-7810 to show purge ordering itself can resurrect older state | [1.2.19 + 3.x Cassandra tombstone/repair grounding](evidence/41-cassandra-3x-tombstone-repair-grounding.md); historical deepening now includes exact `DeletedColumn`/`CompactionController` source, CASSANDRA-7810, and Bigtable 2006 prior art; pre-1.2 genealogy, range/TTL tombstones, post-4.0 evolution, production fault injection, and secure erasure remain separate work |\n'
idx, n = case41_row_re.subn(case41_row, idx, count=1)
assert n == 1, f'expected one Case 41 table row, replaced {n}'

findings_re = re.compile(r'### Case 91 — Cassandra tombstone-grace findings\n.*?(?=### Case 53 deepening — DRAM RowHammer)', re.S)
findings = '''### Case 41 deepening — Cassandra 1.2.19 / CASSANDRA-7810 / Bigtable prior art\n\n1133. **deletion marker ≠ mere absence in the exact 1.2.19 implementation** — `DeletedColumn` is retained typed state with deletion timestamp/local-deletion-time semantics and a deletion serialization flag.\n1134. **documented default grace ≠ universal safe-forgetting proof** — `DEFAULT_GC_GRACE_SECONDS = 864000` is an exact 1.2.19 policy default, not proof that every old replica or representation has converged after ten days.\n1135. **grace eligibility ≠ local purge authority** — 1.2.19 `CompactionController.shouldPurge` still examines overlapping SSTables and refuses purge when an older version may remain outside the compaction set.\n1136. **local shadow closure ≠ distributed convergence** — knowing that relevant SSTable versions participate in one compaction does not prove that every remote replica has learned the deletion.\n1137. **stale-replica resurrection ≠ the only resurrection mechanism** — CASSANDRA-7810 reproduces a deleted row reappearing in a one-node cluster, so distributed outage is not required for every premature-forgetting failure.\n1138. **expired tombstone ≠ dispensable tombstone during the current operation** — CASSANDRA-7810 shows that an age-eligible marker can still be semantically required until its suppressive work against older local data is complete.\n1139. **purge ordering is retention semantics** — discarding negative evidence before applying it can restore older positive state even when the bytes of the old value were never lost.\n1140. **bug-fix record ≠ mechanism invention date** — the 1.2.19 / 2.0.11 / 2.1.0 CASSANDRA-7810 fixes date one failure correction, not the origin of Cassandra tombstones or grace-based reclamation.\n1141. **deletion-entry compaction predates Cassandra** — Bigtable 2006 already documents `special deletion entries` that suppress deleted data in older live SSTables until major compaction can remove both.\n1142. **Bigtable prior function ≠ Cassandra implementation identity** — similar negative-state retention across immutable files blocks an origin myth but does not establish direct code descent or identical currentness rules.\n1143. **older immutable representation can create a retention obligation without replica failure** — both Bigtable's compaction description and CASSANDRA-7810 show that local historical embodiments can keep deletion evidence necessary even in the absence of a disconnected node.\n1144. **later `zombie` vocabulary ≠ proven 1.2 historical vocabulary** — modern Apache documentation is a useful institutional explanation of the stale-replica failure, while the exact older source remains described in its period implementation terms.\n1145. **later repair-qualified purge ≠ Cassandra 1.2.19 behavior** — Case 41's 3.x `only_purge_repaired_tombstones` evidence must not be projected backward into the older `DeletedColumn`/`shouldPurge` implementation.\n1146. **one canonical case can contain version-bounded mechanism layers without flattening them** — Case 41 now treats 1.2.19 local purge/defect evidence and 3.x repair-aware purge as related but historically distinct witnesses.\n1147. **tombstone retirement ≠ secure sanitization** — closing database currentness/shadowing relations still says nothing by itself about physical-media, snapshot, backup, or controller-level forensic erasure.\n1148. **negative evidence has a retirement condition, not a metaphysical requirement to persist forever** — once the bounded older-state paths can no longer reassert themselves, deletion evidence can become reclaimable without turning tombstones into an indefinite archive.\n\n'''
idx, n = findings_re.subn(findings, idx, count=1)
assert n == 1, f'expected one Case 91 findings block, replaced {n}'
idx_path.write_text(idx)

# 5. Navigation/status cleanup across Markdown. Remove explicit duplicate navigation lines, redirect residual prose links, and fix aggregate counts if present.
for p in ROOT.rglob('*.md'):
    if '.git' in p.parts:
        continue
    text = p.read_text()
    if p.name in {'README.md', 'ROADMAP.md', 'CASE_INDEX.md'}:
        text = ''.join(line for line in text.splitlines(keepends=True) if OLD_CASE_PATH not in line and OLD_EVID_PATH not in line)
    text = text.replace('../' + OLD_CASE_PATH, '../' + NEW_CASE_PATH)
    text = text.replace('../' + OLD_EVID_PATH, '../' + NEW_EVID_PATH)
    text = text.replace(OLD_CASE_PATH, NEW_CASE_PATH)
    text = text.replace(OLD_EVID_PATH, NEW_EVID_PATH)
    text = text.replace('Case 91', 'Case 41')
    text = text.replace('Cases 41 and 41', 'Case 41').replace('Cases 41 + 41', 'Case 41')
    text = re.sub(r'\b93 bounded cases\b', '92 bounded cases', text)
    text = re.sub(r'\b93 grounded cases\b', '92 grounded cases', text)
    text = re.sub(r'\b93 cases, 93 grounded\b', '92 cases, 92 grounded', text)
    p.write_text(text)

# Enrich the README evidence navigation line for the canonical evidence record.
readme = ROOT / 'README.md'
rt = readme.read_text()
pattern = re.compile(r'^- \[`evidence/41-cassandra-3x-tombstone-repair-grounding\.md`\]\(evidence/41-cassandra-3x-tombstone-repair-grounding\.md\).*?$', re.M)
replacement = '- [`evidence/41-cassandra-3x-tombstone-repair-grounding.md`](evidence/41-cassandra-3x-tombstone-repair-grounding.md) — Case-41 canonical grounding now spans exact Cassandra 1.2.19 deletion-marker/overlap-purge source, CASSANDRA-7810 local resurrection, Cassandra 3.x hints/repair and repair-qualified purge, plus Bigtable 2006 deletion-entry prior art while keeping the release boundaries explicit.'
rt, n = pattern.subn(replacement, rt, count=1)
assert n == 1, f'expected one README Case 41 evidence line, replaced {n}'
readme.write_text(rt)

# 6. Validation: no live duplicate references; canonical files contain the unique evidence; active case ledger count is correct.
for p in ROOT.rglob('*.md'):
    text = p.read_text()
    assert OLD_CASE_PATH not in text, f'stale duplicate case path in {p}'
    assert OLD_EVID_PATH not in text, f'stale duplicate evidence path in {p}'
    assert 'Case 91' not in text, f'stale Case 91 prose reference in {p}'

assert not CASE91.exists() and not EVID91.exists()
assert 'CASSANDRA-7810' in CASE41.read_text()
assert 'Bigtable' in CASE41.read_text()
assert 'DeletedColumn.java' in EVID41.read_text()
assert 'special deletion entries' in EVID41.read_text()

idx = idx_path.read_text()
cases_block = idx.split('## Cases', 1)[1].split('## Comparison matrix', 1)[0]
case_rows = [line for line in cases_block.splitlines() if line.startswith('| [')]
grounded_rows = [line for line in case_rows if '**grounded**' in line]
assert len(case_rows) == 92, f'expected 92 canonical case rows, found {len(case_rows)}'
assert len(grounded_rows) == 92, f'expected 92 grounded case rows, found {len(grounded_rows)}'

print('Consolidated duplicate Cassandra Case 91 into canonical Case 41.')
print(f'Canonical case rows: {len(case_rows)}; grounded: {len(grounded_rows)}')
