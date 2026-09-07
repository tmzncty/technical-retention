from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def before(path: str, anchor: str, addition: str, marker: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    if marker in text:
        return
    if anchor not in text:
        raise RuntimeError(f"anchor not found in {path}: {anchor!r}")
    p.write_text(text.replace(anchor, addition + anchor, 1), encoding="utf-8")


def after(path: str, anchor: str, addition: str, marker: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    if marker in text:
        return
    if anchor not in text:
        raise RuntimeError(f"anchor not found in {path}: {anchor!r}")
    p.write_text(text.replace(anchor, anchor + addition, 1), encoding="utf-8")


case_history = r'''
### H/P — generic FTL checkpoint/crash-recovery work predates GeckoFTL

A narrower prior-art check changes the novelty boundary of this case without changing its mechanism. Chi Zhang, Yi Wang, Tianzheng Wang, Renhai Chen, Duo Liu, and Zili Shao's paper _Deterministic Crash Recovery for NAND Flash Based Storage Systems_ was presented at DAC in June 2014, roughly two years before the SIGMOD GeckoFTL publication. The IEEE publication record states the problem in FTL terms: because the FTL manages Flash through metadata, crash recovery must efficiently and effectively maintain and recover **FTL metadata consistency** after a system crash.

The paper's stated `DCR` mechanism already uses a checkpoint boundary. Its basic idea is to reproduce deterministic FTL events that occurred **between the last checkpoint and the crash point**, then inspect only a bounded set of blocks selected from those deterministic operations rather than scan the entire Flash chip. The authors report an implementation for a block-level FTL on an ARM11-based embedded evaluation board and compare it with a version-based recovery scheme.

This supplies a chronological floor for several generic ideas that Case 39 must not attribute to GeckoFTL in 2016:

- FTL crash recovery as a metadata-consistency problem;
- an explicit `last checkpoint → crash point` recovery interval;
- reconstruction/replay of post-checkpoint controller events;
- recovery cost as a separate engineering objective from mere NAND byte survival;
- reducing recovery scope below a whole-device scan.

It does **not** erase GeckoFTL's distinct bounded contribution. DCR is described as a deterministic recovery method for a block-level FTL. GeckoFTL instead makes metadata **scale** central to a page-associative / Flash-resident mapping regime, isolates PVB as a major RAM component in its evaluated design, moves validity state into Logarithmic Gecko's LSM-like Flash structures, and gives run-completion / pinned-run mechanisms for reconstructing volatile mapping and invalidity state. The safe comparison is therefore:

> **2014 DCR proves that FTL checkpoint/reconstruction and recovery-time optimization already existed as explicit research problems; 2016 GeckoFTL supplies a different metadata-scaling and Flash-resident-structure solution.**

No inspected source establishes a direct implementation genealogy from DCR into GeckoFTL, and chronological prior art must not be rewritten as such.

**Primary anchor:** Chi Zhang et al., _Deterministic Crash Recovery for NAND Flash Based Storage Systems_, DAC 2014, DOI `10.1109/DAC.2014.6881475` / ACM proceedings DOI `10.1145/2593069.2593124`; IEEE Xplore publication record and abstract, with the Hong Kong Polytechnic University institutional publication record as bibliographic corroboration.
'''
before(
    "cases/39-geckoftl-power-failure-metadata-recovery.md",
    "\n---\n\n## Retained state\n",
    case_history,
    "generic FTL checkpoint/crash-recovery work predates GeckoFTL",
)

case_engineering = r'''
### `GeckoFTL recovery ≠ invention of generic FTL checkpoint/replay`

The 2014 DCR paper already formulates FTL metadata consistency after crash, a last-checkpoint-to-crash recovery interval, deterministic event reproduction, bounded recovery scanning, and recovery-time evaluation. GeckoFTL's defensible novelty boundary in this repository is therefore narrower: scaling Flash-resident mapping/validity metadata and reconstructing the specific PVB/LSM/run-directory relations described by its sources.

### `earlier DCR mechanism ≠ demonstrated GeckoFTL genealogy`

Chronological and functional prior art blocks an origin claim. It does not prove that GeckoFTL inherited code, data structures, or design decisions from DCR.
'''
before(
    "cases/39-geckoftl-power-failure-metadata-recovery.md",
    "\n---\n\n## Functional analogies\n",
    case_engineering,
    "GeckoFTL recovery ≠ invention of generic FTL checkpoint/replay",
)

case_limits = r'''
## Prior-art limits added in this deepening

- `2016 GeckoFTL = invention of generic FTL crash recovery` is rejected: DCR already makes FTL metadata consistency, checkpoints, reconstruction, and recovery time explicit in 2014.
- `DCR = GeckoFTL mechanism` is rejected: the inspected DCR record describes a block-level deterministic-replay scheme, while GeckoFTL's bounded mechanism is page-associative / Flash-resident and includes PVB, Logarithmic Gecko, LSM-like runs, completion witnesses, and pinned-run dependencies.
- `DCR → GeckoFTL direct genealogy` remains unsupported. Earlier publication establishes a prior-art floor, not a transmission path.
- Neither research-system record proves deployment in a named commercial SSD controller.

'''
before(
    "cases/39-geckoftl-power-failure-metadata-recovery.md",
    "## Related repositories\n",
    case_limits,
    "## Prior-art limits added in this deepening",
)

source_line = "- Chi Zhang, Yi Wang, Tianzheng Wang, Renhai Chen, Duo Liu, and Zili Shao, _Deterministic Crash Recovery for NAND Flash Based Storage Systems_, DAC 2014, 2–5 June 2014, DOI `10.1109/DAC.2014.6881475` / ACM proceedings DOI `10.1145/2593069.2593124`: <https://ieeexplore.ieee.org/document/6881475>; institutional record: <https://research.polyu.edu.hk/en/publications/deterministic-crash-recovery-for-nand-flash-based-storage-systems/>.\n"
after(
    "cases/39-geckoftl-power-failure-metadata-recovery.md",
    "### Primary / period research sources\n\n",
    source_line,
    "https://research.polyu.edu.hk/en/publications/deterministic-crash-recovery-for-nand-flash-based-storage-systems/",
)

evidence_source = r'''
### Source D — Zhang et al., _Deterministic Crash Recovery for NAND Flash Based Storage Systems_, DAC 2014

**Document:** Chi Zhang, Yi Wang, Tianzheng Wang, Renhai Chen, Duo Liu, and Zili Shao, _Deterministic Crash Recovery for NAND Flash Based Storage Systems_, 51st Design Automation Conference, June 2014, DOI `10.1109/DAC.2014.6881475`; ACM proceedings DOI `10.1145/2593069.2593124`.

**Primary publication record:** IEEE Xplore: <https://ieeexplore.ieee.org/document/6881475>.

**Institutional corroboration:** Hong Kong Polytechnic University Scholars Hub: <https://research.polyu.edu.hk/en/publications/deterministic-crash-recovery-for-nand-flash-based-storage-systems/>.

**Evidence class:** `H/P` for the authors' contemporary problem formulation, mechanism summary, implementation class, and evaluation boundary; the institutional record is `H/S` bibliographic corroboration of the same publication.

#### Source D — FTL crash recovery is explicitly a metadata-consistency problem by 2014

The IEEE record states that because an FTL directly manages Flash using metadata, its crash-recovery problem is how to maintain and recover **FTL metadata consistency** after a system crash. This is explicit period vocabulary two years before GeckoFTL's SIGMOD publication.

**Use:** blocks any Case-39 origin claim for the generic proposition that surviving NAND payload needs consistent/recoverable FTL management metadata.

#### Source D — checkpoint-bounded replay/reconstruction predates GeckoFTL

The paper describes DCR's basic idea as exploiting deterministic FTL behavior to reproduce events occurring **between the last checkpoint and the crash point** during recovery. It contrasts this with approaches that scan the whole Flash chip and says DCR can instead check a limited number of blocks selected from deterministic FTL operations.

**Use:** grounds an earlier floor for `checkpoint boundary + reconstruction/replay + bounded recovery scope` as an FTL crash-recovery design family.

**Boundary:** the inspected record does not license importing GeckoFTL's PVB, Logarithmic Gecko, LSM runs, postambles, pinned runs, or page-associative metadata organization into DCR.

#### Source D — implementation/evaluation class remains bounded

The publication record says DCR was implemented for a **block-level FTL** and evaluated against a version-based scheme on an ARM11-based embedded evaluation board. It reports improved recovery time and consistent recovered FTL metadata.

**Use:** separates an evaluated 2014 research implementation from both universal SSD behavior and GeckoFTL's later page-associative / Flash-resident metadata design.

---

## Prior-art consequence for Case 39

The combined chronology now supports:

```text
DCR / DAC 2014
    explicit FTL metadata-consistency crash recovery
    + last-checkpoint → crash-point event reconstruction
    + bounded-block recovery scope
        ↓ chronological floor only
GeckoFTL / SIGMOD 2016
    metadata-scale problem
    + Flash-resident mapping/validity structures
    + PVB / Logarithmic Gecko
    + completion/admissibility witnesses
    + pinned-run recovery dependencies
```

The arrow is **not** a demonstrated genealogy. It means only that Case 39 must describe its novelty more narrowly than `FTL metadata recovery` or `checkpoint-based crash recovery`.

### G-39.11 — `2016 GeckoFTL ≠ origin of generic FTL crash recovery`

**Evidence:** DCR in June 2014 already formulates FTL metadata consistency after crash as the problem and presents a concrete recovery mechanism.

**Status:** grounded prior-art boundary.

### G-39.12 — `checkpoint/reconstruction family predates GeckoFTL`

**Evidence:** DCR explicitly reconstructs deterministic events between the last checkpoint and crash point and reduces the recovery search to a bounded block set.

**Status:** grounded prior-art floor.

### G-39.13 — `DCR ≠ GeckoFTL mechanism identity`

**Evidence:** DCR's inspected record identifies a block-level deterministic-replay design; GeckoFTL's sources identify page-associative Flash-resident mapping/validity structures, PVB, LSM-like runs, and separate completion/reclamation dependencies.

**Status:** grounded mechanism-separation rule.

### G-39.14 — `earlier mechanism floor ≠ direct genealogy`

**Evidence:** chronology establishes that DCR is earlier; no inspected source establishes code, architecture, or design descent from DCR into GeckoFTL.

**Status:** explicit anti-genealogy guardrail.

'''
before(
    "evidence/39-geckoftl-2015-2017-metadata-recovery-grounding.md",
    "## Related-repository duplication check\n",
    evidence_source,
    "### Source D — Zhang et al.",
)

roadmap_bullet = "- [x] GeckoFTL generic FTL crash-recovery / checkpoint prior-art deepening — canonical [`cases/39-geckoftl-power-failure-metadata-recovery.md`](cases/39-geckoftl-power-failure-metadata-recovery.md), with [`evidence/39-geckoftl-2015-2017-metadata-recovery-grounding.md`](evidence/39-geckoftl-2015-2017-metadata-recovery-grounding.md), now adds Zhang et al.'s DAC 2014 DCR as an earlier explicit floor for FTL metadata-consistency recovery, a `last checkpoint → crash point` reconstruction interval, and bounded-block recovery instead of whole-device scanning. This blocks any claim that GeckoFTL invented generic FTL checkpoint/crash recovery while preserving GeckoFTL's narrower metadata-scaling/PVB/LSM-run contribution. DCR is a chronological and functional prior-art floor only; direct DCR→GeckoFTL genealogy, commercial-controller deployment, full pre-2014 PORCE/SPOR history, and fault injection remain open.\n"
after(
    "ROADMAP.md",
    "## Phase 2 — Build missing technical bridges\n\n",
    roadmap_bullet,
    "GeckoFTL generic FTL crash-recovery / checkpoint prior-art deepening",
)

findings = r'''

## Case 39 — DCR prior-art deepening findings

- **1741 — FTL crash recovery as metadata-consistency work predates GeckoFTL:** Zhang et al.'s DAC 2014 DCR publication explicitly formulates recovery after system crash as maintaining and recovering consistency of FTL metadata. (`H/P`)
- **1742 — last checkpoint → crash point is an explicit 2014 recovery interval:** DCR reproduces deterministic FTL events occurring between the last checkpoint and the crash point. (`H/P`)
- **1743 — recovery-scan scope ≠ whole-device scan:** DCR contrasts its bounded set of blocks derived from deterministic FTL operations with approaches that scan the whole Flash chip. (`H/P`, `E`)
- **1744 — GeckoFTL 2016 ≠ invention of generic FTL checkpoint/crash recovery:** the 2014 DCR record supplies a chronological floor for checkpoint-bounded metadata reconstruction and recovery-time optimization. (`H/P`, `X` origin claim rejected)
- **1745 — DCR block-level replay ≠ GeckoFTL page-associative metadata architecture:** DCR's inspected publication record identifies a block-level deterministic recovery design, whereas Case 39's Gecko sources ground PVB, Flash-resident mappings, Logarithmic Gecko, LSM-like runs, completion witnesses, and pinned-run dependencies. (`H/P`, `E`)
- **1746 — metadata recovery objective ≠ NAND-payload retention law:** both research lines operate above raw cell persistence by restoring controller relations needed to interpret/manage surviving Flash; neither source turns recovery latency into a raw-cell retention duration. (`E`)
- **1747 — checkpoint vocabulary ≠ one universal transaction semantics:** DCR and GeckoFTL both use checkpoint-bounded recovery relations, but their controller state, FTL geometry, and reconstruction mechanisms differ; database/filesystem transaction semantics remain a separate layer. (`E`, `A` bounded only)
- **1748 — evaluated research implementation ≠ commercial-controller deployment:** DCR reports a block-level FTL implementation on an ARM11-based evaluation board; GeckoFTL reports research evaluation. Neither record proves use in a named commercial SSD controller. (`H/P`, `X`)
- **1749 — earlier mechanism floor ≠ demonstrated DCR → GeckoFTL genealogy:** chronology blocks an origin claim but does not establish code, architectural, institutional, or citation-line descent from DCR into GeckoFTL. (`H/P`, `X`)
- **1750 — related-repository boundary:** the current `tmzncty/computing-archaeology` search found no dedicated `DCR` / GeckoFTL crash-recovery case to reuse; broader FTL recovery genealogy should live there if developed, while Case 39 keeps the retention-specific novelty boundary. (`H/P` project-state record)
'''
p = ROOT / "CASE_INDEX.md"
text = p.read_text(encoding="utf-8")
if "## Case 39 — DCR prior-art deepening findings" not in text:
    p.write_text(text.rstrip() + findings + "\n", encoding="utf-8")

required = {
    "cases/39-geckoftl-power-failure-metadata-recovery.md": [
        "generic FTL checkpoint/crash-recovery work predates GeckoFTL",
        "GeckoFTL recovery ≠ invention of generic FTL checkpoint/replay",
        "## Prior-art limits added in this deepening",
        "https://research.polyu.edu.hk/en/publications/deterministic-crash-recovery-for-nand-flash-based-storage-systems/",
    ],
    "evidence/39-geckoftl-2015-2017-metadata-recovery-grounding.md": ["### Source D — Zhang et al.", "G-39.14"],
    "ROADMAP.md": ["GeckoFTL generic FTL crash-recovery / checkpoint prior-art deepening"],
    "CASE_INDEX.md": ["**1741 —", "**1750 —"],
}
for path, needles in required.items():
    data = (ROOT / path).read_text(encoding="utf-8")
    for needle in needles:
        if needle not in data:
            raise RuntimeError(f"missing {needle!r} in {path}")

subprocess.run(["git", "diff", "--check"], cwd=ROOT, check=True)
print("Case 39 DCR prior-art integration validated")
