from pathlib import Path

CASE_APPEND = r'''

---

## 2009–2011 prior-art deepening — cached mapping, Flash-resident recovery state, and replay

This bounded deepening fills the chronology between Case 04's 1993–1995 mapped-Flash/FTL floor and the already-grounded 2014 DCR → 2015–2017 GeckoFTL sequence. It does **not** turn Case 39 into a complete FTL history.

### H/P/S — Park et al. 2009 make volatile address-cache loss a power-failure consistency problem

Jung-Wook Park, Seung-Ho Park, Gi-Ho Park, and Shin-Dug Kim, *An integrated mapping table for hybrid FTL with fault-tolerant address cache*, was received **26 December 2008**, accepted **3 March 2009**, and released by IEICE Electronics Express on **10 April 2009**.

The paper's bounded problem statement is directly relevant here: as Flash capacity grows, an entire mapping table may not fit in fast SRAM, so physical-page address information may remain in Flash while a smaller page-address cache accelerates lookup. The authors explicitly say power failure that loses only a few cached addresses can create substantial inconsistency.

Their proposed design stores integrated metadata in a Flash-resident `hybrid map block`; an initial scan of that map block regenerates working metadata tables.

This gives an earlier explicit witness for:

```text
volatile working address cache
        !=
Flash-resident recovery substrate
        !=
user payload
```

The paper is a peer-reviewed proposed design evaluated by simulation. It is **not** evidence that every 2009 SSD used this architecture, and it is not an invention-date claim.

Primary/institutional anchors:

- IEICE / J-STAGE: <https://doi.org/10.1587/elex.6.368>
- Yonsei institutional record: <https://yonsei.elsevierpure.com/en/publications/an-integrated-mapping-table-for-hybrid-ftl-with-fault-tolerant-ad/>

### H/P — ITRI 2011 separates cached BMT from Flash-resident map/log recovery evidence

US `9,164,887 B2`, *Power-failure recovery device and method for flash memory*, has a **5 December 2011** filing/priority date and names Industrial Technology Research Institute (ITRI) as assignee.

The disclosure describes:

- a `block map table (BMT)` that records logical-block → physical-block mappings;
- that BMT as temporarily stored in cache;
- Flash-resident `super map`, `dedicated map`, and BMT records;
- an `update log` used after abnormal shutdown;
- a recovery procedure that loads the Flash-resident BMT and replays update-log labels to update the cached BMT.

The disclosure explicitly says the mechanism can recover a BMT lost due to power failure using information registered in the update log.

Thus by the 2011 filing, the following separation is explicit in a primary technical source:

> **normal-operation translation state in volatile cache ≠ nonvolatile relation evidence used to reconstitute it after failure.**

The patent is evidence of a disclosed design, not proof of shipping-product adoption or first invention.

Primary anchor: <https://patents.google.com/patent/US9164887B2/en>.

### H/P/S — the chronology narrows GeckoFTL novelty without erasing its distinct problem

The bounded chronology now reads:

```text
1993–1995  Case 04
mapped Flash / FTL relation state can be rebuilt at startup
        ↓ chronology only
2009       Park et al.
power-failure-sensitive address cache + Flash map-block reconstruction
        ↓ chronology only
2011       ITRI filing
cache-resident BMT + Flash maps/log + abnormal-shutdown replay
        ↓ chronology only
2014       DCR
FTL metadata-consistency recovery + checkpoint→crash deterministic replay
        ↓ chronology only
2015–2017  GeckoFTL
metadata scaling + PVB/Logarithmic Gecko + run admissibility + pinned-run dependencies
```

No arrow claims direct descent. The earlier sources block any statement that GeckoFTL originated the broad ideas `volatile mapping can be lost`, `mapping can be reconstructed from Flash-resident evidence`, or `post-failure replay can rebuild FTL metadata`.

GeckoFTL's bounded contribution remains different: it makes **metadata scale, PVB footprint, Flash-resident validity structures, recovery admissibility of partial runs, and safe reclamation dependencies** central in a page-associative/large-device research design.

### Engineering reconstruction — relation recovery is not payload reconstruction

Across the 2009 and 2011 sources, the failure/recovery path can be represented as:

```text
payload pages survive in Flash
        +
volatile lookup/cache state is lost
        +
Flash-resident map/log evidence survives
        ↓
scan / load / replay
        ↓
working logical→physical relation is reconstructed
        ↓
ordinary logical service becomes possible again
```

The operation being reconstructed is the controller's **resolution/currentness relation**. It cannot manufacture a user page that was never durably programmed or repair a physically corrupt page.

Therefore:

- **payload survival ≠ logical legibility**;
- **volatile working map ≠ recovery substrate**;
- **mapping reconstruction ≠ payload reconstruction**;
- **mapping recovered ≠ payload integrity validated**;
- **retained recovery evidence ≠ zero restart work**.
'''

EVIDENCE_APPEND = r'''

---

## 2009–2011 intermediate prior-art bridge

This addendum fills the gap between the 1993–1995 mapped-Flash foundation already delegated to Case 04 and the 2014 DCR prior-art floor already present in this evidence record.

### Source E — Park et al., IEICE Electronics Express, 2009

**Document:** Jung-Wook Park, Seung-Ho Park, Gi-Ho Park, Shin-Dug Kim, *An integrated mapping table for hybrid FTL with fault-tolerant address cache*, IEICE Electronics Express 6(7), 368–374.  
**Received:** **26 December 2008**  
**Accepted:** **3 March 2009**  
**Released:** **10 April 2009**  
**DOI:** `10.1587/elex.6.368`  
**Primary record:** <https://www.jstage.jst.go.jp/article/elex/6/7/6_7_368/_article/-char/en>  
**Institutional corroboration:** <https://yonsei.elsevierpure.com/en/publications/an-integrated-mapping-table-for-hybrid-ftl-with-fault-tolerant-ad/>

**Evidence class:** `H/P/S` — peer-reviewed contemporary research paper; the mechanism is the authors' proposed design, with simulation evaluation.

#### Source E — power failure can remove cached address state while Flash retains mapping evidence

The abstract states that entire FTL mapping tables cannot necessarily fit in fast SRAM as capacity grows. It describes physical page addresses retained in Flash/spare areas plus a page-address cache used for lookup speed, and explicitly warns that losing only a few cached addresses during power failure can cause substantial data-information inconsistency.

The proposed scheme integrates metadata into a Flash-resident `hybrid map block` containing the physical page table. An initial scan of that map block generates working metadata tables.

**Use:** establishes an explicit 2009 floor for `volatile address cache loss + Flash-resident reconstruction basis`.

**Boundary:** proposed/simulated design ≠ universal or commercial SSD implementation.

### Source F — ITRI, US 9,164,887 B2 / US20130145076A1

**Document:** *Power-failure recovery device and method for flash memory*  
**Inventors:** Tzi-cker Chiueh, Ting-Fang Chien, Shih-Chiang Tsao, Chien-Yung Lee  
**Assignee:** Industrial Technology Research Institute (ITRI)  
**Filed / priority:** **5 December 2011**  
**Application publication:** **6 June 2013**  
**Grant publication:** **20 October 2015**  
**Primary record:** <https://patents.google.com/patent/US9164887B2/en>

**Evidence class:** `H/P` for the disclosed design and chronology.

#### Source F — cached BMT is not the only retained mapping evidence

The patent says the `block map table (BMT)` records logical-block → physical-block mappings and is temporarily stored in cache. It separately describes Flash-resident physical blocks/spare metadata and a hierarchy of `super map`, `dedicated map`, BMT records, and an `update log`.

For abnormal shutdown the disclosed recovery method reads the super/dedicated maps, loads the Flash-resident BMT into cache, reads the update log, and applies its labels to update the cached BMT. The disclosure explicitly says this can recover a BMT lost due to power failure using information registered in the update log.

**Use:** directly grounds `working translation representation ≠ nonvolatile recovery substrate` and `mapping-log replay ≠ payload reconstruction`.

**Boundary:** patent disclosure ≠ evidence of a named shipping product or priority over all earlier work.

## Claims added by this deepening

### G-39.15 — `2009 power-failure-sensitive address cache ≠ first mapped-Flash recovery`

Case 04 already grounds 1993–1995 startup-rebuildable mapping/allocation state. Park et al. supply a later explicit power-failure/cache-loss witness, not an invention origin.

**Status:** grounded prior-art boundary.

### G-39.16 — `volatile address-cache loss ≠ permanent mapping loss`

Park et al.'s Flash-resident hybrid map block is explicitly designed so an initial scan can regenerate metadata tables after cached state is lost.

**Status:** grounded for the proposed design.

### G-39.17 — `cached BMT ≠ sole mapping authority`

The 2011 ITRI filing temporarily stores BMT in cache while retaining BMT/map/log material in Flash for recovery.

**Status:** grounded for the disclosed design.

### G-39.18 — `update-log replay ≠ payload reconstruction`

The ITRI recovery path updates the mapping relation in cache from surviving map/log evidence. It does not claim to recreate missing user payload bits.

**Status:** grounded engineering distinction.

### G-39.19 — `retained relation evidence ≠ immediate service readiness`

Both the 2009 map-block scan and 2011 map/log load/replay require restart work before a working translation state is reconstituted.

**Status:** grounded engineering reconstruction.

### G-39.20 — `mapping recovered ≠ payload validated`

A reconstructed logical→physical relation says which embodiment to use; it does not prove that page media are intact or that an interrupted write became durable.

**Status:** explicit limit.

### G-39.21 — `intermediate prior art ≠ GeckoFTL mechanism identity`

Park's hybrid map block and ITRI's hierarchical BMT/update-log recovery predate GeckoFTL, but they do not establish GeckoFTL's PVB/Logarithmic-Gecko/run/pinned-run mechanisms or a direct genealogy.

**Status:** grounded mechanism-separation rule.

### G-39.22 — related-repository boundary

A renewed search of `tmzncty/computing-archaeology` for `FTL`, `flash translation layer`, and power-failure mapping recovery still found no dedicated case. Broad FTL/controller genealogy should live there if developed; this record retains only the relation-lifetime and recovery distinctions.

**Status:** project-state record.
'''

FINDINGS = r'''### Case 39 deepening — 2009–2011 FTL mapping-recovery prior-art bridge

- **2029 — 2009 power-failure address-cache witness ≠ invention of rebuildable mapped Flash:** Case 04 already grounds 1993–1995 startup-reconstructible mapping/allocation state; Park et al. make the power-failure/cache-loss problem explicit later. (`H/P/S`, `X`)
- **2030 — nonvolatile Flash ≠ nonvolatile runtime mapping:** a Flash payload can survive while SRAM/cache-resident lookup state disappears. (`H/P/S`, `E`)
- **2031 — volatile working-map loss ≠ permanent relation loss:** Park et al.'s Flash-resident hybrid map block provides a reconstruction basis for lost cached mapping metadata. (`H/P/S`, `E`)
- **2032 — proposed map-block recovery ≠ commercial deployment:** the 2009 paper is a peer-reviewed proposed design evaluated by simulation, not a named shipping-SSD witness. (`H/P/S`, `X`)
- **2033 — cached BMT ≠ sole mapping authority:** the 2011 ITRI disclosure temporarily stores BMT in cache while retaining Flash-resident map/BMT/log evidence for abnormal-shutdown recovery. (`H/P`, `E`)
- **2034 — update-log replay ≠ payload reconstruction:** applying retained update-log information to rebuild a BMT reconstructs a logical→physical relation; it does not regenerate missing user bytes. (`H/P`, `E`)
- **2035 — patent disclosure ≠ shipping-product behavior:** US9164887B2 establishes a disclosed 2011-priority design, not universal implementation, deployment, or first invention. (`H/P`, `X`)
- **2036 — payload survival ≠ logical legibility:** readable NAND pages do not by themselves identify which physical embodiment should answer a logical address after working mapping state is lost. (`E`)
- **2037 — retained recovery substrate ≠ zero recovery work:** map-block scanning or map/log loading and replay can remain necessary before normal logical service resumes. (`H/P/S`, `H/P`, `E`)
- **2038 — mapping recovered ≠ payload validated:** a correct relation does not prove media integrity or that an interrupted write had already become durable. (`E`, `X`)
- **2039 — readable stale page ≠ current logical page:** out-of-place Flash can preserve obsolete embodiments until reclamation, so byte presence is weaker than mapping/currentness qualification. (`H/P`, `E`)
- **2040 — retained mapping summary ≠ complete operation history:** map blocks, BMT snapshots, and update logs can preserve enough recovery evidence without recording every host operation. (`H/P/S`, `H/P`, `E`)
- **2041 — 2014 DCR checkpoint/replay floor ≠ GeckoFTL origin claim:** DCR already frames FTL crash recovery as metadata-consistency recovery between checkpoint and crash; GeckoFTL's later claim must remain narrower. (`H/P/S`, `X`)
- **2042 — earlier recovery function ≠ GeckoFTL mechanism identity:** GeckoFTL remains distinct in its metadata-scaling problem, PVB/Logarithmic-Gecko structures, run-completion admissibility, and pinned-run reclamation dependencies. (`H/P/S`, `A`, `X`)
- **2043 — chronology ≠ genealogy:** 1993/1995 mapped Flash, 2009 hybrid map block, 2011 BMT/update-log recovery, 2014 DCR, and 2015–2017 GeckoFTL form a chronological evidence sequence only; direct descent is not established. (`H/P`, `H/P/S`, `A`, `X`)
- **2044 — Case 04 constitutive mapping ≠ Case 39 failure-time reconstitution:** Case 04 grounds identity across relocation; Case 39 uses later sources to ground loss/reconstruction of the controller relation after power failure. (`A`)
- **2045 — Case 15 payload durability handoff ≠ Case 39 mapping recovery:** losing volatile staged user data before nonvolatile commit differs from rebuilding lookup/currentness state for payload that survived in Flash. (`A`)
- **2046 — related-repository boundary:** current `tmzncty/computing-archaeology` searches still found no dedicated FTL power-loss metadata-recovery case; broad controller genealogy belongs there if developed. (`H/P` project-state record)'''

OLD_ROW = "| [GeckoFTL Power-Failure Recovery: Flash-Resident Validity Metadata, Checkpoints, and Restart Reconstitution](cases/39-geckoftl-power-failure-metadata-recovery.md) | **grounded** | research FTL + nonvolatile NAND payload + Flash-resident mapping/validity metadata + volatile SRAM caches/buffers + checkpoint/recovery witnesses | separate payload survival from controller-state survival and immediate restart availability; show partial metadata can survive physically yet be inadmissible, while safe reclamation may depend on retaining old metadata until newer invalidity state is durably closed | [2015–2017 GeckoFTL grounding](evidence/39-geckoftl-2015-2017-metadata-recovery-grounding.md); commercial/named-controller metadata recovery, independent fault compliance, and filesystem/database composition remain separate work |"
NEW_ROW = "| [GeckoFTL Power-Failure Recovery: Flash-Resident Validity Metadata, Checkpoints, and Restart Reconstitution](cases/39-geckoftl-power-failure-metadata-recovery.md) | **grounded** | research FTL + nonvolatile NAND payload + Flash-resident mapping/validity metadata + volatile SRAM caches/buffers + checkpoint/recovery witnesses | separate payload survival from controller-state survival and immediate restart availability; show partial metadata can survive physically yet be inadmissible, while safe reclamation may depend on retaining old metadata until newer invalidity state is durably closed | [2009–2017 FTL/GeckoFTL grounding](evidence/39-geckoftl-2015-2017-metadata-recovery-grounding.md); Park 2009 and ITRI 2011 now supply intermediate power-failure mapping-recovery prior art before DCR 2014 / GeckoFTL; commercial named-controller recovery, independent fault compliance, and filesystem/database composition remain separate work |"

ROADMAP_NEW = "- [ ] loss of index or mapping metadata — **substantially advanced by grounded Case 39**: nonvolatile Flash payload can outlive volatile lookup state, while Park 2009, an ITRI 2011-priority disclosure, DCR 2014, and GeckoFTL 2015–2017 show several bounded ways to retain/reconstruct mapping, validity, checkpoint, and log evidence before ordinary logical service resumes. This closes the mapped-Flash/FTL `payload survival ≠ logical legibility`, `volatile working map ≠ recovery substrate`, and `mapping reconstruction ≠ payload reconstruction` relation; complete metadata loss beyond the reconstruction substrate, named commercial-controller power-cut behavior, filesystem/database index loss, and forensic recovery remain open;"

# Append bounded deepening to Case 39 and Evidence 39.
case_path = Path("cases/39-geckoftl-power-failure-metadata-recovery.md")
case = case_path.read_text(encoding="utf-8")
if "## 2009–2011 prior-art deepening" not in case:
    case_path.write_text(case.rstrip() + CASE_APPEND + "\n", encoding="utf-8")

evidence_path = Path("evidence/39-geckoftl-2015-2017-metadata-recovery-grounding.md")
evidence = evidence_path.read_text(encoding="utf-8")
if "## 2009–2011 intermediate prior-art bridge" not in evidence:
    evidence_path.write_text(evidence.rstrip() + EVIDENCE_APPEND + "\n", encoding="utf-8")

# Correct ROADMAP: this broad family remains open outside the bounded FTL layer.
roadmap_path = Path("ROADMAP.md")
lines = roadmap_path.read_text(encoding="utf-8").splitlines()
found = False
for i, line in enumerate(lines):
    if "loss of index or mapping metadata" in line:
        lines[i] = ROADMAP_NEW
        found = True
        break
if not found:
    raise SystemExit("ROADMAP mapping-loss marker not found")
roadmap_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

# Remove the accidental duplicate Case 124 navigation/findings and deepen canonical Case 39 instead.
index_path = Path("CASE_INDEX.md")
index = index_path.read_text(encoding="utf-8")
index = "\n".join(line for line in index.splitlines() if "cases/124-ftl-power-loss-mapping-recovery.md" not in line)
marker = "## Case 124 — FTL power-loss mapping-recovery findings"
if marker in index:
    index = index.split(marker, 1)[0].rstrip()
if OLD_ROW in index:
    index = index.replace(OLD_ROW, NEW_ROW)
elif NEW_ROW not in index:
    raise SystemExit("Case 39 row not found for update")
if "### Case 39 deepening — 2009–2011 FTL mapping-recovery prior-art bridge" not in index:
    index = index.rstrip() + "\n\n" + FINDINGS + "\n"
else:
    index = index.rstrip() + "\n"
index_path.write_text(index, encoding="utf-8")

# Remove duplicate research artifacts and one-time integration machinery.
for p in [
    Path("cases/124-ftl-power-loss-mapping-recovery.md"),
    Path("evidence/124-ftl-1995-2014-mapping-recovery-grounding.md"),
    Path("scripts/deepen_case39_ftl_prior_art.py"),
    Path(".github/workflows/deepen-case39-ftl-prior-art.yml"),
]:
    if p.exists():
        p.unlink()
