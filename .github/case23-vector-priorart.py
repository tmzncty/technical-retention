from pathlib import Path
import re

def read(path):
    return Path(path).read_text(encoding="utf-8")

def write(path, text):
    Path(path).write_text(text, encoding="utf-8")

def replace_once(path, old, new):
    text = read(path)
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected one anchor, found {count}: {old[:120]!r}")
    write(path, text.replace(old, new, 1))

case = "cases/23-amazon-dynamo-divergent-version-anti-entropy.md"
ev = "evidence/23-amazon-dynamo-2007-version-handoff-antientropy-grounding.md"

# 1) Deepen the retention argument with Dynamo's own bounded clock-truncation caveat.
case_anchor = """The paper's Figure 3 example makes the boundary concrete: versions D1 and D2 can be garbage-collected after a descendant is known, while two causally unrelated descendants such as D3 and D4 must both remain until reconciliation establishes a later successor.

### Engineering reconstruction"""
case_insert = """The paper's Figure 3 example makes the boundary concrete: versions D1 and D2 can be garbage-collected after a descendant is known, while two causally unrelated descendants such as D3 and D4 must both remain until reconciliation establishes a later successor.

The same section also makes the causal metadata itself a bounded retention object. Dynamo notes that a clock can grow when many different servers coordinate writes. To cap that growth, it stores a timestamp with each `(node, counter)` pair and removes the oldest pair after a configured threshold is reached (the paper gives 10 as an example). The authors explicitly warn that, after truncation, descendant relationships may no longer be derived accurately, which can make reconciliation less efficient; they also say the issue had not surfaced in production and was not thoroughly investigated.

This adds a second forgetting boundary:

> **payload-version retention and causal-metadata retention are coupled but not identical.**

Dynamo can deliberately forget part of the causal summary without deleting the object version itself, accepting reduced precision in later ancestry/reconciliation reasoning.

### Engineering reconstruction"""
replace_once(case, case_anchor, case_insert)

case_bullets_old = """- `causal ancestry can authorize forgetting`;
- `causal incomparability can create a positive retention obligation`.

The repository should therefore not define distributed `currentness` as necessarily singular."""
case_bullets_new = """- `causal ancestry can authorize forgetting`;
- `causal incomparability can create a positive retention obligation`;
- `causal summary ≠ full update history`;
- `clock truncation ≠ object-version deletion`;
- `metadata-size control can trade retained causal precision for bounded state`.

The repository should therefore not define distributed `currentness` as necessarily singular."""
replace_once(case, case_bullets_old, case_bullets_new)

# 2) Replace the generic vector-clock priority disclaimer with a bounded terminology/prior-art map.
prior_old = """## Prior-art boundary

Dynamo's own paper says it synthesizes `well known techniques`; the novelty of this case is therefore **not** an invention-priority claim for its ingredients.

Two earlier lines are especially relevant:

- Alan Demers et al., **“Epidemic Algorithms for Replicated Database Maintenance,”** PODC 1987, pp. 1–12, DOI <https://doi.org/10.1145/41840.41841>. This is direct prior art for randomized propagation / replica convergence well before Dynamo's anti-entropy deployment.
- Douglas B. Terry et al., **“Managing Update Conflicts in Bayou, a Weakly Connected Replicated Storage System,”** SOSP 1995, pp. 172–182, DOI <https://doi.org/10.1145/224057.224070>. This is earlier primary literature for weakly connected replicated storage with application-specific conflict handling.

The present case therefore makes **no** claim that Dynamo invented eventual consistency, divergent-version reconciliation, anti-entropy, vector clocks, or Merkle trees.

A full genealogy of vector clocks, epidemic replication, consistent hashing, quorums, Merkle trees, and weak consistency belongs in distributed-systems history, not in this bounded retention slice.

---"""
prior_new = """## Prior-art boundary

Dynamo's own paper says it synthesizes `well known techniques`; the novelty of this case is therefore **not** an invention-priority claim for its ingredients.

The causal-metadata boundary can now be stated more precisely.

- Leslie Lamport's 1978 **“Time, Clocks, and the Ordering of Events in a Distributed System”** establishes `happened before` as a partial order and gives synchronized **logical clocks** whose scalar values can support a total order consistent with that relation. Dynamo cites this paper as reference [12]. That citation is foundational causal-order prior art; it is **not evidence that Lamport 1978 already used Dynamo's per-object `(node, counter)` vector representation**. Microsoft Research publication record: <https://www.microsoft.com/en-us/research/publication/time-clocks-ordering-events-distributed-system/>; DOI <https://doi.org/10.1145/359545.359563>.
- D. Stott Parker Jr. et al., **“Detection of Mutual Inconsistency in Distributed Systems,”** *IEEE Transactions on Software Engineering* 9(3), 1983, pp. 240–247, directly use the historical term **`version vector`** for replicated files under network partition. Each component counts updates at one site; componentwise dominance/compatibility is used to detect independently modified versions. Crucially for this repository, the authors motivate the vector as a way to encode the necessary characteristics of the history graph without retaining the entire arbitrarily growing graph. DOI <https://doi.org/10.1109/TSE.1983.236733>.
- Friedemann Mattern's **“Virtual Time and Global States of Distributed Systems,”** 1989, develops `vector time` from vectors of logical clocks and componentwise maximum. Mattern explicitly says Fidge independently proposed vectors of logical clocks for distributed debugging, and then identifies Parker et al.'s earlier replicated-file `version vector` as a very similar scheme for detecting independent modifications under partition. Official ETH facsimile and bibliographic record: <https://vs.inf.ethz.ch/publ/papers/VirtTimeGlobStates.pdf> and <https://vs.inf.ethz.ch/publ/bibtex.html?file=papers%2FVirtTimeGlobStates>.
- Alan Demers et al., **“Epidemic Algorithms for Replicated Database Maintenance,”** PODC 1987, pp. 1–12, DOI <https://doi.org/10.1145/41840.41841>, remains prior art for randomized propagation / replica convergence before Dynamo's anti-entropy deployment.
- Douglas B. Terry et al., **“Managing Update Conflicts in Bayou, a Weakly Connected Replicated Storage System,”** SOSP 1995, pp. 172–182, DOI <https://doi.org/10.1145/224057.224070>, remains earlier primary literature for weakly connected replicated storage with application-specific conflict handling.

Terminology must remain source-specific:

```text
Lamport 1978 logical clock / happened-before
        !=
Parker et al. 1983 replicated-file version vector
        !=
Mattern/Fidge late-1980s vector time / vectors of logical clocks
        !=
Dynamo 2007 per-object "vector clock"
```

The mechanisms are historically related enough to establish prior art and a comparison boundary, but this repository does **not** silently rename Parker's `version vector` as a Dynamo `vector clock`, or vice versa. Nor does Mattern's statement that Fidge worked independently settle a universal first-invention priority.

Parker also supplies two useful limits against overgeneralization: equal bytes produced independently can still carry conflicting version vectors, and the paper's bounded scheme is explicitly a **single-file** conflict detector that does not by itself detect every cross-file transaction serialization error. Therefore:

> **vector dominance ≠ semantic equivalence ≠ complete transaction-consistency proof.**

The present case makes no claim that Dynamo invented eventual consistency, divergent-version reconciliation, anti-entropy, vector clocks, version vectors, or Merkle trees. A full priority genealogy of logical clocks, vector timestamps, version vectors, epidemic replication, quorums, consistent hashing, and later descendants belongs in distributed-systems history—preferably `computing-archaeology` if that history is later built—rather than being duplicated here.

---"""
replace_once(case, prior_old, prior_new)

# 3) Evidence record: strengthen status, add primary-source prior-art records, and close the old genealogy gap.
replace_once(
    ev,
    "- prior-art controls are supplied by Dynamo's own `well known techniques` statement plus earlier ACM records for epidemic replica maintenance and Bayou conflict handling;",
    "- prior-art controls are supplied by Dynamo's own `well known techniques` statement, Lamport 1978, Parker et al. 1983, Mattern 1989, and earlier ACM records for epidemic replica maintenance and Bayou conflict handling;"
)

evidence_anchor = """---

## Prior-art controls"""
evidence_insert = """---

## Source F — Lamport, logical clocks and event ordering, 1978

### Bibliographic record

Leslie Lamport, **“Time, Clocks, and the Ordering of Events in a Distributed System,”** *Communications of the ACM* 21(7), July 1978, pp. 558–565.

Microsoft Research author/publication record:

<https://www.microsoft.com/en-us/research/publication/time-clocks-ordering-events-distributed-system/>

DOI:

<https://doi.org/10.1145/359545.359563>

### Inspection level

**Primary-paper institutional publication record + abstract/author context; Dynamo reference list directly inspected.**

### Use

Lamport's paper establishes the `happened before` partial order and a synchronized logical-clock mechanism that can totally order events consistently with that causal relation. Dynamo's 2007 reference [12] points directly to Lamport 1978.

**Established:** Lamport is direct causal-order/logical-clock prior art for the problem Dynamo cites.

**Not established:** that Lamport 1978 used a per-object vector of site counters, the term `version vector`, or the exact Dynamo clock representation. The historical distinction matters because `logical clock` is not one fixed data structure across all later literature.

---

## Source G — Parker et al., replicated-file version vectors, 1983

### Bibliographic record

D. Stott Parker Jr., Gerald J. Popek, Gerard Rudisin, Allen Stoughton, Bruce J. Walker, Evelyn Walton, Johanna M. Chow, David Edwards, Stephen Kiser, and Charles Kline, **“Detection of Mutual Inconsistency in Distributed Systems,”** *IEEE Transactions on Software Engineering* 9(3), May 1983, pp. 240–247.

DOI:

<https://doi.org/10.1109/TSE.1983.236733>

Direct facsimile mirror inspected for text:

<https://pages.cs.wisc.edu/~remzi/Classes/739/Fall2018/Papers/parker83detection.pdf>

### Inspection level

**Primary-paper direct PDF text, especially printed pp. 242–244 (§III.C–D).**

### Use

The paper explicitly uses the term `version vector`. It proposes keeping a vector with each copy of each replicated file; each component counts updates made at one site. The authors define componentwise compatibility/dominance, increment the originating site's component on update, combine predecessor maxima during reconciliation, and state that the vector is committed with the updated file.

The retention-specific motivation is especially important: the paper rejects retaining an entire potentially unbounded partition/history graph and instead proposes a version-numbering scheme encoding only the necessary characteristics of that history graph.

This grounds:

- `version vector` terminology no later than 1983 in a replicated-file partition context;
- `causal/history summary ≠ full history archive`;
- a small retained relation can authorize conflict detection without retaining every historical event.

### Counterexamples / limits

The authors also state two limits that must survive comparison with Dynamo:

1. identical independent updates in separate partitions can still be reported as a version conflict;
2. the bounded scheme applies to single files and can miss a cross-file transaction serialization conflict.

Therefore `vector compatibility` is not a universal test for semantic equality or arbitrary transactional consistency.

**Not used to claim:** code lineage from this paper to Dynamo, or that Parker's exact file-copy semantics are identical to Dynamo's object clocks.

---

## Source H — Mattern, vector time and explicit relation to Fidge/Parker, 1989

### Bibliographic record

Friedemann Mattern, **“Virtual Time and Global States of Distributed Systems,”** in M. Cosnard et al. (eds.), *Proceedings of the Workshop on Parallel and Distributed Algorithms*, North-Holland / Elsevier, 1989, pp. 215–226.

Official ETH publication/facsimile:

<https://vs.inf.ethz.ch/publ/papers/VirtTimeGlobStates.pdf>

Official ETH bibliographic record:

<https://vs.inf.ethz.ch/publ/bibtex.html?file=papers%2FVirtTimeGlobStates>

### Inspection level

**Primary paper, direct text + page-image inspection.** The vector-time construction was checked around reprint printed p. 126, and the Fidge/Parker comparison around printed p. 129.

### Use

Mattern builds `vector time` from one logical-clock component per process, increments the local component, piggybacks the vector, and merges received knowledge with componentwise maximum. In the applications discussion he says that Fidge independently suggested vectors of logical clocks for distributed debugging. He then explicitly describes Parker et al.'s older replicated-file `version vector`, including per-site update counts and conflict detection for independent modifications under partition.

This is a particularly strong terminology bridge because it is a late-1980s primary author explicitly relating:

```text
vectors of logical clocks / vector time
        to
an earlier replicated-file version-vector scheme
```

**Boundary:** Mattern's wording establishes a contemporaneous relationship and an independent-work statement about Fidge; it does not settle a universal priority dispute for every vector-clock/version-vector concept.

---

## Source A addendum — Dynamo clock truncation is deliberate causal-metadata forgetting

### Anchor

DeCandia et al. §4.4 / author-hosted online text corresponding to printed pp. 210–211.

### Inspection level

**Primary paper / author-hosted text.**

### Use

Dynamo states that vector-clock size can grow when many servers coordinate writes. Its bounded scheme stores a timestamp with each `(node, counter)` pair and removes the oldest pair after a threshold (the paper gives 10 as an example). The authors explicitly say this can make descendant relationships impossible to derive accurately and therefore create reconciliation inefficiency; they also report that this had not surfaced in production and was not thoroughly investigated.

This directly grounds:

- `causal metadata is itself retained state`;
- `bounded metadata growth can require deliberate metadata forgetting`;
- `metadata forgetting ≠ payload-version deletion`;
- `smaller retained causal summary can reduce future reconciliation precision`.

It does **not** establish a quantified probability of false conflict/loss, nor a general claim that truncation is unsafe in every workload.

---

## Prior-art controls"""
replace_once(ev, evidence_anchor, evidence_insert)

prior_table_old = """| `Dynamo invented vector clocks` | **rejected / not investigated as a priority question** | the case only grounds Dynamo's use of vector clocks; a correct clock-history genealogy requires a separate literature slice |"""
prior_table_new = """| `Dynamo invented vector clocks` | **rejected** | Lamport 1978 is causal/logical-clock prior art; Parker et al. 1983 directly use `version vector` for replicated files; Mattern 1989 relates vector time, Fidge's independent vectors of logical clocks, and Parker's earlier version vectors |
| `Lamport 1978 already contains the Dynamo/Parker vector data structure` | **rejected / unsupported** | Lamport's bounded inspected result is happened-before + logical clocks/total ordering; do not infer the later per-site vector representation from Dynamo's citation alone |
| `Parker version vector = Dynamo vector clock in every semantic detail` | **rejected** | useful functional/prior-art relation, but different systems, vocabulary, object models, and stated limits |"""
replace_once(ev, prior_table_old, prior_table_new)

hist_old = """- multiple object versions;
- vector-clock causality;
- ancestor version `can be forgotten`;"""
hist_new = """- multiple object versions;
- Dynamo's historical term `vector clock` and per-object `(node, counter)` representation;
- clock-component timestamping/truncation as an explicit bounded-metadata mechanism;
- vector-clock causality;
- ancestor version `can be forgotten`;"""
replace_once(ev, hist_old, hist_new)

eng_old = """- `causal ancestry can authorize forgetting`;
- `background maintenance has a resource budget`."""
eng_new = """- `causal ancestry can authorize forgetting`;
- `causal summary ≠ full history archive`;
- `clock truncation ≠ object-version deletion`;
- `metadata-size control can trade causal precision for bounded retained state`;
- `vector dominance ≠ semantic equality or arbitrary transaction-consistency proof`;
- `background maintenance has a resource budget`."""
replace_once(ev, eng_old, eng_new)

dup_old = """Before writing, the indexed `tmzncty/computing-archaeology` repository was searched for:

- `Dynamo`;
- `Merkle tree anti entropy replication`.

No dedicated matching treatment was returned."""
dup_new = """Before writing and again during the vector/version-vector deepening, the indexed `tmzncty/computing-archaeology` repository was checked for a dedicated treatment of:

- `Dynamo`;
- `Merkle tree anti entropy replication`;
- vector clocks / version vectors.

No dedicated matching treatment was returned in the inspected index/search state."""
replace_once(ev, dup_old, dup_new)

remain_old = """- the exact historical genealogy of vector clocks (including the distinction from Lamport logical clocks);
- detailed Bayou→Dynamo comparison;"""
remain_new = """- the **full** priority genealogy beyond the bounded Lamport 1978 → Parker 1983 → Fidge/Mattern late-1980s anchors established here, including terminology drift and later database/filesystem descendants;
- detailed Bayou→Dynamo comparison;"""
replace_once(ev, remain_old, remain_new)

# 4) README navigation: retain the case but expose the newly bounded prior-art/metadata-retention result.
readme_old = "- [`cases/23-amazon-dynamo-divergent-version-anti-entropy.md`](cases/23-amazon-dynamo-divergent-version-anti-entropy.md) — grounded distributed-currentness bridge: Dynamo can deliberately retain several causally unrelated versions of one key, use vector-clock ancestry to authorize forgetting, separate sloppy-quorum availability from intended-placement convergence through hinted handoff, and repair replica divergence through read repair plus Merkle-tree anti-entropy."
readme_new = "- [`cases/23-amazon-dynamo-divergent-version-anti-entropy.md`](cases/23-amazon-dynamo-divergent-version-anti-entropy.md) — grounded distributed-currentness bridge: Dynamo can deliberately retain several causally unrelated versions of one key, use vector-clock ancestry to authorize forgetting, separate sloppy-quorum availability from intended-placement convergence, and repair divergence through read repair plus Merkle-tree anti-entropy. Prior-art deepening now distinguishes Lamport 1978 logical clocks, Parker et al. 1983 replicated-file `version vector`, and Mattern/Fidge late-1980s vector-time work from Dynamo's 2007 historical `vector clock` vocabulary; Dynamo's own clock truncation also shows that causal metadata can be deliberately forgotten while payload versions survive."
replace_once("README.md", readme_old, readme_new)

# 5) ROADMAP: close the already-grounded divergent-version synthesis item rather than inventing a duplicate case.
road_old = "- [ ] In divergent-version replication, how should `causally superseded`, `concurrent/admissible`, `returned`, `read-repaired`, `anti-entropy synchronized`, and `placement-converged` states be separated?"
road_new = "- [x] In divergent-version replication, separate `causally superseded`, `concurrent/admissible`, `returned`, `read-repaired`, `anti-entropy synchronized`, and `placement-converged` states — grounded in [`cases/23-amazon-dynamo-divergent-version-anti-entropy.md`](cases/23-amazon-dynamo-divergent-version-anti-entropy.md), with [`evidence/23-amazon-dynamo-2007-version-handoff-antientropy-grounding.md`](evidence/23-amazon-dynamo-2007-version-handoff-antientropy-grounding.md). Prior-art deepening now adds Lamport 1978 logical-clock foundations, Parker et al. 1983 replicated-file `version vector` terminology/history summarization, Mattern/Fidge late-1980s vector-time boundaries, and Dynamo's explicit clock-truncation precision tradeoff. Full priority genealogy and later descendants remain separate distributed-systems history work, preferably coordinated with `computing-archaeology`."
replace_once("ROADMAP.md", road_old, road_new)

# 6) CASE_INDEX ledger row.
idx_old = "| [Amazon Dynamo: Divergent Version Retention, Hinted Handoff, and Anti-Entropy](cases/23-amazon-dynamo-divergent-version-anti-entropy.md) | **grounded** | replicated key/value versions + per-version vector clocks/context + sloppy-quorum temporary placement + intended-recipient hints + read repair + Merkle-tree anti-entropy | show currentness can remain plural until causal/semantic reconciliation; separate write/read availability from intended placement and replica convergence; separate divergence detection from repair | [2007 Dynamo grounding](evidence/23-amazon-dynamo-2007-version-handoff-antientropy-grounding.md); vector-clock genealogy, later Dynamo/DynamoDB semantics, modern LRC/EC currentness, and broader consistency theory remain separate work |"
idx_new = "| [Amazon Dynamo: Divergent Version Retention, Hinted Handoff, and Anti-Entropy](cases/23-amazon-dynamo-divergent-version-anti-entropy.md) | **grounded** | replicated key/value versions + per-version vector clocks/context + bounded clock-component retention/truncation + sloppy-quorum temporary placement + intended-recipient hints + read repair + Merkle-tree anti-entropy | show currentness can remain plural until causal/semantic reconciliation; separate payload-version survival from retained causal-summary precision; separate write/read availability from intended placement and replica convergence; separate divergence detection from repair | [2007 Dynamo grounding + 1978–1989 causal/version-vector prior-art deepening](evidence/23-amazon-dynamo-2007-version-handoff-antientropy-grounding.md); full priority genealogy, later Dynamo/DynamoDB semantics, modern LRC/EC currentness, and broader consistency theory remain separate work |"
replace_once("CASE_INDEX.md", idx_old, idx_new)

# Append findings with dynamic numbering to avoid collisions if another bounded slice landed immediately before this workflow ran.
idx = read("CASE_INDEX.md")
marker = "### Case 23 deepening — logical clocks, version vectors, and bounded causal metadata"
if marker in idx:
    raise SystemExit("Case 23 vector/version-vector deepening already present")
nums = [int(m.group(1)) for m in re.finditer(r"(?m)^(\d+)\.\s+\*\*", idx)]
start = (max(nums) + 1) if nums else 1
findings_texts = [
    "**Lamport logical clock ≠ later per-site vector representation** — Dynamo cites Lamport 1978 for causal/logical-clock foundations, but that citation alone does not establish the later version-vector/vector-time data structure.",
    "**replicated-file `version vector` is period vocabulary by 1983** — Parker et al. directly retain per-site update counts with each file copy and compare them after network partition; Dynamo therefore cannot be assigned invention priority for the general storage-specific vector-version idea.",
    "**history summary ≠ history archive** — Parker explicitly motivates version vectors as encoding necessary characteristics of an otherwise potentially unbounded partition/history graph rather than retaining the entire graph.",
    "**vector dominance ≠ byte-semantic equivalence** — Parker notes that two independently produced but byte-identical updates can still signal a version conflict because the retained relation records independent modification history.",
    "**single-object causal summary ≠ transaction serialization proof** — Parker's own cross-file example shows a serialization conflict that file-local version vectors do not detect.",
    "**historical vocabulary must remain local to sources** — Parker's `version vector`, Mattern's `vector time` / vectors of logical clocks, and Dynamo's `vector clock` can be compared without normalizing all three into one retroactive term.",
    "**bounded causal metadata can itself be deliberately forgotten** — Dynamo removes old `(node, counter)` pairs when its vector clock reaches a configured size threshold; the authors acknowledge that ancestry may then be derived less accurately.",
    "**metadata forgetting ≠ payload forgetting** — removing a clock component does not itself delete the object version; it changes the evidence available for later ancestry/reconciliation decisions.",
    "**bounded metadata size can trade future decision precision for present state cost** — Dynamo's truncation caveat makes causal-metadata retention a resource policy, not a free logical abstraction.",
    "**distributed currentness is a staged relation, not one Boolean** — `causally superseded`, `concurrent/admissible`, `returned`, `read-repaired`, `anti-entropy synchronized`, and `placement-converged` describe distinct states/times in the bounded Dynamo regime."
]
lines = ["", marker, ""]
for i, text in enumerate(findings_texts, start=start):
    lines.append(f"{i}. {text}")
    lines.append("")
write("CASE_INDEX.md", idx.rstrip() + "\n" + "\n".join(lines).rstrip() + "\n")

# Final structural checks.
case_text = read(case)
ev_text = read(ev)
road = read("ROADMAP.md")
readme = read("README.md")
idx = read("CASE_INDEX.md")
assert "Parker et al. 1983" in readme
assert "clock truncation" in case_text
assert "Source G — Parker et al." in ev_text
assert "Lamport 1978" in road
assert marker in idx
assert len([n for n in findings_texts if n in idx]) == len(findings_texts)
