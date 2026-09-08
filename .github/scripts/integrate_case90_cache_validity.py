from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text()
    if old not in text:
        raise SystemExit(f"anchor missing in {path}: {old[:80]!r}")
    if text.count(old) != 1:
        raise SystemExit(f"anchor not unique in {path}: {old[:80]!r}")
    p.write_text(text.replace(old, new, 1))


def append_once(path: str, marker: str, block: str) -> None:
    p = Path(path)
    text = p.read_text().rstrip() + "\n"
    if marker in text:
        raise SystemExit(f"marker already present in {path}: {marker}")
    p.write_text(text + "\n" + block.strip() + "\n")

case_path = 'cases/90-apache-kafka-leader-epoch-safe-truncation.md'
evidence_path = 'evidence/90-kafka-2016-2017-leader-epoch-truncation-grounding.md'

replace_once(
    case_path,
    "- **Bounded mechanism:** leader-epoch identifiers stamped into the replicated log, per-replica epoch→start-offset recovery metadata, the `OffsetsForLeaderEpoch` exchange, follower truncation before normal fetching, and reconciliation of epoch metadata with the local log.\n",
    "- **Bounded mechanism:** leader-epoch identifiers stamped into the replicated log, per-replica epoch→start-offset recovery metadata, the `OffsetsForLeaderEpoch` exchange, follower truncation before normal fetching, and reconciliation of epoch metadata with the local log.\n- **Post-release validation slice:** Apache Kafka fixes/issues from October 2018 through February 2019 are used only to test the lifetime and admissibility of that retained epoch metadata under successive elections and old/new message-format boundaries. They are not back-projected as Kafka 0.11.0.0 shipped semantics.\n"
)

post_release = r'''## Post-0.11 validation and evolution — 2018–2019

### H/P — KAFKA-7415 made leader-transition completeness an explicit cache obligation

Apache commit [`f2dd6aa2698345fd0b0348f7bc74ce3215adf682`](https://github.com/apache/kafka/commit/f2dd6aa2698345fd0b0348f7bc74ce3215adf682), committed 4 October 2018, is titled `Persist leader epoch and start offset on becoming a leader`. Its commit message gives the failure case: after successive leader elections, a follower can contain records from epochs later than any epoch represented in the new leader's log/cache. The patch therefore records the new leader epoch together with its log-end offset as the epoch start, and tightens the cache so epoch/start-offset entries remain monotonic, deleting conflicting entries when necessary.

This is later corrective/evolution evidence. It shows that **having an epoch checkpoint was not sufficient unless the retained boundary set was complete enough for the recovery question actually asked**.

### H/P — KAFKA-7897 showed that cache presence alone could select an unsafe truncation regime

Apache commit [`d152989f26f51b9004b881397db818ad6eaf0392`](https://github.com/apache/kafka/commit/d152989f26f51b9004b881397db818ad6eaf0392), committed 8 February 2019, is titled `Disable leader epoch cache when older message formats are used`. The commit explains that Kafka had been updating the epoch cache for all message-format versions and then using the presence of *any* cached epoch as the prerequisite for the newer `OffsetsForLeaderEpoch` truncation path. With an older record format that did not actually carry the required epoch history, that test could cause large, unnecessary truncations after leader changes. The fix disables leader-epoch-cache use for those older formats and falls back to high-watermark truncation.

This gives a strong negative boundary:

```text
retained lineage metadata exists
        ≠
retained lineage metadata is admissible for this format/recovery path
```

### H/P — KAFKA-7959 made deliberate cache deletion a compatibility-preserving action

Apache issue [KAFKA-7959](https://issues.apache.org/jira/browse/KAFKA-7959), resolved 22 February 2019 for the 2.0 branch, records a second-order problem. Guarding use of a sparse cache while an old message format remains active is not enough if that same stale cache survives until a later format upgrade, when it can become eligible for use again and cause unexpected truncation/re-replication. The issue therefore requires deleting or clearing the cache while the old message format is in use.

This is an unusually direct retention counterexample: **forgetting a retained recovery structure can be safer than preserving it when the structure has outlived the compatibility conditions that made it truthful.** The deleted object is recovery/currentness metadata, not the partition payload.

### H/P — KAFKA-7984 records rebuildability and its own validity hazard

Apache issue [KAFKA-7984](https://issues.apache.org/jira/browse/KAFKA-7984), opened 22 February 2019, documents existing recovery logic that rebuilds leader-epoch cache files by walking record batches when recovering log segments after an unclean shutdown. It also warns that rebuilding across segments/batches that do not support leader epochs can itself create misleading cache state.

The safe historical claim is narrow: **by this 2019 code/issue context, the checkpoint could be reconstructed from epoch-bearing record batches during log recovery, but reconstruction was format-qualified rather than mechanically valid for every surviving log byte.** The unresolved issue is evidence of a known validity boundary, not proof that every branch/version had one identical rebuild algorithm.

---

'''
replace_once(case_path, "## Functional analogies and limits\n", post_release + "## Functional analogies and limits\n")

replace_once(
    case_path,
    "### E — compatibility fallback ≠ semantic identity\n\nFalling back to the high watermark when leader-epoch data is unavailable preserves compatibility; it does not mean the two mechanisms encode the same information.\n",
    "### E — compatibility fallback ≠ semantic identity\n\nFalling back to the high watermark when leader-epoch data is unavailable preserves compatibility; it does not mean the two mechanisms encode the same information.\n\n### E — metadata presence ≠ metadata admissibility\n\nKAFKA-7897 supplies a concrete failure of the shortcut `checkpoint exists -> checkpoint may safely qualify truncation`. The record/message format must actually support the lineage evidence that the cache claims to summarize.\n\n### E — cache completeness ≠ byte persistence\n\nKAFKA-7415 shows a leader can retain a readable log while its sparse epoch cache is still insufficient to answer a follower's lineage query after successive elections. The missing relation is not missing user payload.\n\n### E — correct forgetting can apply to recovery metadata itself\n\nKAFKA-7959 deliberately clears/deletes a stale epoch cache so that a future upgrade cannot misinterpret it as valid lineage evidence. More retained recovery metadata is therefore not monotonically safer.\n\n### E — rebuildable checkpoint ≠ automatically valid checkpoint\n\nKAFKA-7984 documents cache rebuilding from record batches during unclean-log recovery while simultaneously identifying mixed/unsupported message-format cases in which such rebuilding must be constrained. Reconstruction recovers a derived relation only when its source evidence is semantically eligible.\n"
)

replace_once(
    case_path,
    "6. Apache Kafka `0.11.0.0`, `ReplicaFetcherThread.scala`.\n   - <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/server/ReplicaFetcherThread.scala>\n",
    "6. Apache Kafka `0.11.0.0`, `ReplicaFetcherThread.scala`.\n   - <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/server/ReplicaFetcherThread.scala>\n7. Apache Kafka commit `f2dd6aa2698345fd0b0348f7bc74ce3215adf682`, **KAFKA-7415; Persist leader epoch and start offset on becoming a leader**, 4 October 2018.\n   - <https://github.com/apache/kafka/commit/f2dd6aa2698345fd0b0348f7bc74ce3215adf682>\n8. Apache Kafka commit `d152989f26f51b9004b881397db818ad6eaf0392`, **KAFKA-7897; Disable leader epoch cache when older message formats are used**, 8 February 2019.\n   - <https://github.com/apache/kafka/commit/d152989f26f51b9004b881397db818ad6eaf0392>\n9. Apache Kafka JIRA **KAFKA-7959 — Clear/delete epoch cache if old message format is in use**, resolved 22 February 2019.\n   - <https://issues.apache.org/jira/browse/KAFKA-7959>\n10. Apache Kafka JIRA **KAFKA-7984 — Do not rebuild leader epochs on segments that do not support it**, opened 22 February 2019.\n   - <https://issues.apache.org/jira/browse/KAFKA-7984>\n"
)

replace_once(
    evidence_path,
    "# Case 90 Grounding Record — Kafka 2016–2017 Leader-Epoch Truncation\n",
    "# Case 90 Grounding Record — Kafka 2016–2019 Leader-Epoch Truncation and Cache-Validity Deepening\n"
)
replace_once(
    evidence_path,
    "**Evidence boundary:** accepted Apache design material + exact `0.11.0.0` source are primary. Later Kafka documents are useful only to clarify compatibility/evolution, not to back-project modern semantics into 2017.\n",
    "**Evidence boundary:** accepted Apache design material + exact `0.11.0.0` source are primary for the shipped bounded mechanism. Exact 2018–2019 Apache commits/issues are used as post-release validation of cache completeness, format-qualified admissibility, deliberate cache retirement, and rebuildability; they are not back-projected into 2017.\n"
)

p_sources = r'''### P7 — Apache Kafka commit `f2dd6aa...` / KAFKA-7415, 4 October 2018

**Artifact:** `KAFKA-7415; Persist leader epoch and start offset on becoming a leader (#5678)`.

**URL:** <https://github.com/apache/kafka/commit/f2dd6aa2698345fd0b0348f7bc74ce3215adf682>

**Type:** primary implementation/commit record.

**Supports:**

- successive leader elections can leave followers with epochs later than any epoch represented by the new leader;
- the new leader must persist its epoch/start offset so followers can obtain a safe truncation point;
- the cache enforces monotonically increasing epoch/start-offset entries and removes conflicts.

**Boundary:** later corrective/evolution evidence; not Kafka 0.11.0.0 shipped behavior.

### P8 — Apache Kafka commit `d152989...` / KAFKA-7897, 8 February 2019

**Artifact:** `KAFKA-7897; Disable leader epoch cache when older message formats are used (#6232)`.

**URL:** <https://github.com/apache/kafka/commit/d152989f26f51b9004b881397db818ad6eaf0392>

**Type:** primary implementation/commit record.

**Supports:**

- older message formats should disable leader-epoch-cache use and fall back to high-watermark truncation;
- merely detecting the presence of any cached epoch had been sufficient to select the newer truncation path;
- sparse/ineligible cache state could cause large unnecessary truncations after leader changes.

### P9 — Apache Kafka JIRA KAFKA-7959, resolved 22 February 2019

**Artifact:** `Clear/delete epoch cache if old message format is in use`.

**URL:** <https://issues.apache.org/jira/browse/KAFKA-7959>

**Type:** primary project issue record.

**Supports:**

- a sparse cache guarded while an old format is active can remain hazardous if retained until a later upgrade;
- clearing/deleting the cache is used to prevent future misuse and unexpected truncation/re-replication.

**Boundary:** branch/version-specific corrective history; not a universal Kafka rule for all epochs.

### P10 — Apache Kafka JIRA KAFKA-7984, opened 22 February 2019

**Artifact:** `Do not rebuild leader epochs on segments that do not support it`.

**URL:** <https://issues.apache.org/jira/browse/KAFKA-7984>

**Type:** primary project issue record.

**Supports:**

- log recovery code rebuilt leader-epoch cache state by iterating record batches on segments recovered after an unclean shutdown;
- record/message-format eligibility matters to whether reconstructed epoch state is truthful;
- mixed/unsupported-format content can make naive reconstruction unsafe.

**Boundary:** the issue was opened as a bug report; use it to establish the documented implementation hazard/rebuild path, not to claim one final fixed behavior across all branches.

'''
replace_once(evidence_path, "## Claim ledger\n", p_sources + "## Claim ledger\n")

replace_once(
    evidence_path,
    "| truncation ≠ secure sanitization | negative boundary | no physical erase claim in P1–P6 | strong as claim-control boundary |\n",
    "| truncation ≠ secure sanitization | negative boundary | no physical erase claim in P1–P6 | strong as claim-control boundary |\n| a leader-epoch cache can be present yet incomplete for successive-election truncation | post-release historical/implementation record | P7 | strong |\n| cache presence alone is not sufficient evidence that the record format supports safe epoch-based truncation | post-release historical/implementation record | P8 | strong |\n| clearing/deleting stale recovery metadata can prevent later unsafe reuse after a format transition | post-release historical/implementation record | P9 | strong |\n| leader-epoch checkpoint state can be rebuilt from eligible record batches during unclean-log recovery | post-release implementation record | P10 | moderate/strong, bounded to documented code path |\n| retained metadata presence ≠ metadata admissibility | engineering reconstruction | P8, P9 | strong |\n| rebuildability ≠ unconditional semantic validity | engineering reconstruction | P10 | strong as bounded negative rule |\n"
)

roadmap_old = "- [ ] loss of currentness/version metadata;"
roadmap_new = "- [ ] loss of currentness/version metadata — **substantially advanced by grounded Case 90 plus its 2018–2019 cache-validity deepening**: Kafka's leader-epoch lineage can survive as a checkpoint while still being incomplete or format-inadmissible; KAFKA-7415 requires a new-leader epoch boundary after successive elections, KAFKA-7897 disables epoch-cache use for old message formats, and KAFKA-7959 deliberately clears/deletes sparse cache state before a later upgrade can misuse it. KAFKA-7984 further records reconstruction from epoch-bearing record batches after unclean recovery, while warning that unsupported/mixed formats constrain that rebuild. This grounds `metadata presence ≠ metadata admissibility`, `correct metadata forgetting can preserve higher-level continuity`, and `rebuildable checkpoint ≠ automatically valid checkpoint`; total lineage-evidence loss, checkpoint corruption, other replicated-log/version systems, and empirical fault injection remain open;"
replace_once('ROADMAP.md', roadmap_old, roadmap_new)

case_index_block = r'''### Case 90 deepening — Kafka 2018–2019 leader-epoch cache validity findings

- **2063 — checkpoint presence ≠ checkpoint completeness:** KAFKA-7415 shows that after successive elections a leader can retain a log and an epoch cache while still lacking the boundary needed to answer a follower carrying later-epoch data. (`H/P`, `E`)
- **2064 — becoming leader can create a new retention obligation for lineage metadata:** the 4 October 2018 fix persists the new leader epoch and its start offset even when no ordinary produce append first supplies that boundary. (`H/P`)
- **2065 — more cached epochs ≠ monotonically safer recovery:** KAFKA-7415 removes conflicting epoch/start-offset entries to preserve a monotonic usable sequence; obsolete/conflicting lineage metadata can be less useful than a smaller consistent cache. (`H/P`, `E`)
- **2066 — epoch-cache existence ≠ epoch-cache admissibility:** KAFKA-7897 documents that using the presence of any cached epoch as the switch into `OffsetsForLeaderEpoch` truncation was unsafe when the active record format did not support the needed epoch history. (`H/P`, `E`)
- **2067 — record-format compatibility is part of currentness-evidence validity:** the same on-disk checkpoint bytes can be unusable for one format regime and eligible in another; metadata meaning depends on the encoding/protocol evidence it summarizes. (`H/P`, `E`)
- **2068 — fallback to high watermark ≠ equivalence of recovery evidence:** the 2019 fix deliberately falls back when epoch metadata is ineligible; this compatibility path does not make high watermark and leader-epoch lineage the same retained relation. (`H/P`, `E`, `X`)
- **2069 — sparse retained lineage can cause destructive over-truncation:** KAFKA-7897 records large unnecessary truncations after leader changes when incomplete/ineligible epoch-cache state selected the wrong recovery path. (`H/P`)
- **2070 — retaining stale recovery metadata across an upgrade can be a future hazard:** KAFKA-7959 warns that a cache safely ignored under an old message format may later become eligible after upgrade and then be misused. (`H/P`, `E`)
- **2071 — deliberate metadata deletion can preserve logical continuity:** clearing/deleting the sparse epoch cache prevents later unsafe truncation/re-replication; forgetting recovery metadata can therefore be the correct retention action for the higher-level log. (`H/P`, `E`)
- **2072 — forgetting lineage metadata ≠ deleting partition payload:** KAFKA-7959 clears a derived recovery structure, not the user records whose lineage will later be re-established through supported recovery paths. (`H/P`, `E`)
- **2073 — checkpoint loss/rebuildability ≠ payload reconstruction:** KAFKA-7984 records leader-epoch cache rebuilding by scanning surviving record batches during unclean-log recovery; rebuilding the lineage index does not regenerate missing user records. (`H/P`, `E`)
- **2074 — rebuildable metadata ≠ unconditionally rebuildable metadata:** KAFKA-7984 exists because record batches lacking leader-epoch support can make naive reconstruction misleading; surviving bytes must be semantically eligible evidence. (`H/P`, `E`, `X`)
- **2075 — later corrective history ≠ Kafka 0.11 shipped semantics:** the 2018–2019 commits/issues validate and narrow Case 90's retention model but must not be projected backward into the exact 28 June 2017 release behavior. (`H/P`, `X`)
- **2076 — related-repository boundary:** current `tmzncty/computing-archaeology` search still found no dedicated Kafka leader-epoch/cache-validity case; broad replicated-log epoch genealogy belongs there if developed, while Case 90 keeps the retention-specific currentness-evidence lifetime. (`H/P` project-state record)
'''
append_once('CASE_INDEX.md', '2063 — checkpoint presence', case_index_block)

for path in [case_path, evidence_path, 'ROADMAP.md', 'CASE_INDEX.md']:
    p = Path(path)
    p.write_text(p.read_text().rstrip() + "\n")
