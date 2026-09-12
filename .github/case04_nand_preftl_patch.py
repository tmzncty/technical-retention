from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"anchor missing in {path}: {old[:180]!r}")
    if text.count(old) != 1:
        raise SystemExit(f"anchor not unique in {path}: {old[:180]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


def append_once(path: str, required_marker: str, forbidden_marker: str, addition: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if required_marker not in text:
        raise SystemExit(f"required marker missing in {path}: {required_marker!r}")
    if forbidden_marker in text:
        raise SystemExit(f"addition already appears in {path}: {forbidden_marker!r}")
    p.write_text(text.rstrip() + "\n\n" + addition.strip() + "\n", encoding="utf-8")


evidence_path = Path("evidence/04-1987-1989-nand-device-geometry-before-ftl-deepening.md")
case_path = "cases/04-flash-virtual-mapping-logical-identity.md"
grounding_path = "evidence/04-flash-1992-1998-grounding.md"
roadmap_path = "ROADMAP.md"
index_path = "CASE_INDEX.md"

if evidence_path.exists():
    raise SystemExit(f"evidence already exists: {evidence_path}")

EVIDENCE = r'''# Case 04 Deepening — NAND Device Geometry Before FTL Semantics (1987–1989)

## Purpose

This record deepens [`../cases/04-flash-virtual-mapping-logical-identity.md`](../cases/04-flash-virtual-mapping-logical-identity.md) around one bounded historical boundary:

> what did the late-1980s NAND-structure device literature actually establish before the 1992–1995 mapping / FTL evidence used by Case 04?

The answer matters because a later vocabulary such as `Flash Translation Layer`, `garbage collection`, or `logical-to-physical remapping` can easily be projected backward onto early NAND papers merely because later NAND storage systems require those mechanisms.

This slice therefore separates:

```text
NAND cell / string geometry
    !=
device program / erase / read operation geometry
    !=
controller mapping and logical-identity continuity
```

The source situation is itself part of the evidence boundary. A directly inspectable full copy of the 1987 IEDM paper was not obtained in this pass. The 1987 claims below are therefore limited to its bibliographic record and reproduced abstract. The 1988–1989 continuity is supported by later peer-reviewed Toshiba-authored paper records and abstracts. No page-level quotation from an unavailable full text is invented.

## Related-repository check

`tmzncty/computing-archaeology` was searched for `NAND EEPROM Masuoka` and did not expose a dedicated reusable module for this exact 1987–1989 device-history slice. Broader semiconductor-memory and Flash engineering history still belongs primarily there; this record retains only the boundary needed by `technical-retention`.

## Sources inspected

### A. Masuoka, Momodomi, Iwata, Shirota — IEDM 1987

**Type:** H/P, abstract-level record of a primary peer-reviewed paper; no page-level full-text inspection in this pass.

**Title:** `New ultra high density EPROM and Flash EEPROM with NAND structure cell`

**Venue:** International Electron Devices Meeting Technical Digest, 1987, pp. 552–555.

**DOI:** `10.1109/IEDM.1987.191485`

**Institutional bibliographic / abstract records:**

- https://scholar.nycu.edu.tw/en/publications/new-ultra-high-density-eprom-and-flash-eeprom-with-nand-structure/
- https://ndlsearch.ndl.go.jp/books/R100000136-I1574231875756379520

The reproduced abstract says the proposed NAND structure reduces cell size without scaling device dimensions, gives a 6.43 µm² cell under a 1.0-µm design rule, reports roughly 30% lower area per bit than the compared conventional 4-Mbit EPROM structure, and says individual bits in a NAND cell can be programmed selectively. It presents the structure as applicable to high-density nonvolatile memories up to 8 Mbit in the paper's contemporary frame.

**Boundary:** this establishes a 1987 published NAND-structure density / selective-programming proposal. The abstract does not establish a logical sector mapping layer, a garbage collector, an SSD, or later FTL terminology.

### B. Momodomi et al. — IEDM 1988

**Type:** H/P, abstract-level record of a primary peer-reviewed paper.

**Title:** `New device technologies for 5 V-only 4 Mb EEPROM with NAND structure cell`

**Venue:** IEDM Technical Digest, 1988, pp. 412–415.

**Institutional record:**

- https://tohoku.elsevierpure.com/en/publications/new-device-technologies-for-5-v-only-4-mb-eeprom-with-nand-struct/

The abstract describes a 5-V-only NAND-structure EEPROM and names two program-path details: half the programming voltage is applied to unselected bit lines and a successive programming sequence is used to preserve a wide threshold margin. It also reports experimental confirmation of cell reliability and a 12.9 µm² unit-cell area under 1.0-µm rules.

This is useful because it moves the chain from the 1987 density proposal toward an experimentally characterized device program regime without invoking controller mapping semantics.

### C. Itoh et al. — ISSCC 1989

**Type:** H/P, abstract-level record of a primary peer-reviewed paper.

**Title:** `Experimental 4 Mb CMOS EEPROM with a NAND structured cell`

**Venue:** IEEE ISSCC Digest, 1989, pp. 134–135, 314.

**DOI:** `10.1109/ISSCC.1989.48209`

**Institutional record:**

- https://scholar.nycu.edu.tw/en/publications/experimental-4-mb-cmos-eeprom-with-a-nand-structured-cell/

The abstract gives a concrete topology: eight bits are arranged in series between two select transistors. It explains the density advantage in terms of reduced select-transistor and contact-hole overhead per bit, reports a 10^4-cycle endurance figure for the experimental 512K×8 EEPROM, and says page mode is adopted for high-speed programming.

The device-level retained state is therefore already embedded in a shared-string access/program structure. That is a different layer from the later question `which physical embodiment currently counts for a stable logical address?`

### D. Momodomi et al. — IEEE JSSC 1989

**Type:** H/P, abstract-level record of a primary peer-reviewed journal article.

**Title:** `An Experimental 4-Mbit CMOS EEPROM with a NAND-Structured Cell`

**Venue:** IEEE Journal of Solid-State Circuits 24(5), 1989, pp. 1238–1243.

**DOI:** `10.1109/JSSC.1989.572587`

**Institutional records:**

- https://scholar.nycu.edu.tw/en/publications/an-experimental-4-mbit-cmos-eeprom-with-a-nand-structured-cell/
- https://scholars.nthu.edu.tw/esploro/outputs/journalArticle/An-Experimental-4-Mbit-CMOS-EEPROM-with/9957776404306774

The reproduced abstract is especially important for the retention boundary because it explicitly lists **block erasing, successive programming, and random reading** as operations achieved by the NAND-cell control circuit. The same article remains a device/circuit paper; its abstract does not describe a virtual sector map that preserves one external identity while data are relocated.

### E. Momodomi et al. — CICC 1989

**Type:** H/P, abstract-level record of a primary peer-reviewed conference paper.

**Title:** `A high density NAND EEPROM with block-page programming for microcomputer applications`

**DOI:** `10.1109/CICC.1989.56726`

**Institutional record:**

- https://scholar.nycu.edu.tw/en/publications/a-high-density-nand-eeprom-with-block-page-programming-for-microc/

The abstract describes a 5-V-only 4-Mbit NAND EEPROM with high-speed **block-page programming** circuits and on-chip test circuits, framed as applicable to microcomputer systems needing large nonvolatile memory with low power consumption.

This further confirms that late-1980s NAND publications already exposed nontrivial internal operation granularity before the controller-mapping evidence that grounds the main Case 04.

## Historical record — a device-history layer precedes the mapped-storage layer

Taken conservatively, the inspected publication records establish the following chronology:

```text
1987
NAND-structure density proposal + selective bit programming

1988
5-V-only device programming / threshold-margin techniques

1989
experimental 4-Mbit NAND EEPROM
8-bit serial string topology
page / successive programming
block erase + random read
block-page programming for microcomputer applications

1992–1995 Case 04 mapping evidence
logical/virtual identity can be rebound to another physical location
old physical embodiments become dirty/deleted
later clean-up / transfer recovers erase-unit capacity
```

The chronology is important precisely because the layers are not interchangeable. The late-1980s papers show a NAND device and its access/program/erase geometry; Ban, Wells, and later FTL documentation add retained mapping and allocation relations that decide **which embodiment counts as current**.

## Engineering reconstruction — device operation geometry is a constraint, not already a translation layer

The 1989 ISSCC abstract describes eight memory bits sharing a series NAND string between two select transistors. The 1989 JSSC abstract separately names block erasing, successive programming, and random reading.

A safe engineering reconstruction is therefore:

```text
cell/string organization
    -> shared access/program circuitry and operation granularity
    -> physical constraints on how a rewritable nonvolatile array is used
```

But the following additional relation is not supplied by those device papers:

```text
stable host/logical identity
    -> current physical embodiment selected by mapping metadata
    -> obsolete embodiment retired
    -> later reclamation copies current data and erases old capacity
```

That second chain is the distinct mapped-storage problem grounded by the 1992–1995 sources in Case 04.

This yields several bounded distinctions:

> **NAND string geometry != Flash Translation Layer.**

> **block erase != garbage collection.**

> **page / successive programming != logical remapping.**

> **random reading != random in-place overwrite.**

> **device-level nonvolatility != logical-identity continuity across relocation.**

The physical operations help create the constraints that later mapping systems must accommodate, but `constraint exists` is not the same historical claim as `this later abstraction already existed`.

## Functional analogy — the later mapping layer answers a different retention question

At a functional level, Case 04's later mapping system can be read as an answer to a mismatch exposed by Flash operation geometry:

```text
physical medium
has erase/program constraints and shared granularities

logical storage service
wants a stable-looking rewritable address

mapping + allocation + reclamation
mediate between them
```

This is a **functional relation**, not a demonstrated genealogy from the 1987–1989 Toshiba papers to Amir Ban, Intel, PCMCIA, or any particular FTL implementation. No influence claim is made without a source that actually connects the actors or documents.

## Philosophical interpretation — persistence at one layer does not settle identity at another

The technical fact is narrow: a NAND cell can be designed as nonvolatile and densely organized while a later storage service still requires additional state to decide which physical instance is the current bearer of one logical identity.

A bounded interpretation is therefore:

> material persistence of a device state is not yet an account of the continuity of an addressable object when rewriting changes embodiment.

This is the repository's interpretation, not vocabulary attributed to Masuoka, Momodomi, Ban, or their contemporaries.

## Prior-art and anti-anachronism boundaries

This deepening does **not** claim:

- that the 1987 IEDM paper has been page-by-page inspected here;
- that abstract-level records prove every circuit detail in the full papers;
- that Masuoka or Toshiba invented every form of NAND memory, Flash memory, page programming, block erase, or high-density nonvolatile memory;
- that 1987 is the first commercial shipment date of NAND Flash;
- that the 1987–1989 papers used `FTL`, `garbage collection`, `TRIM`, `wear leveling`, `SSD`, or modern host-block vocabulary;
- that the Toshiba device papers directly caused or were cited by the 1992–1995 mapping / FTL line used in Case 04;
- that block erase proves immediate logical deletion, reclamation, secure sanitization, or forensic non-recoverability;
- that a later controller can be reconstructed from device-paper abstracts alone.

## Resulting bounded distinctions

```text
1987–1989 NAND device publication record
    !=
1992–1995 mapped-Flash / FTL publication record

NAND string density optimization
    !=
logical-address continuity

block erase
    !=
logical invalidation
    !=
reclamation
    !=
sanitation

page / successive programming
    !=
out-of-place update policy

physical nonvolatility
    !=
currentness / authority of one logical embodiment

historical ordering
    !=
demonstrated actor-to-actor genealogy
```

## Open work deliberately left outside this slice

- obtain and directly inspect the full 1987 IEDM paper if a renderable copy becomes available;
- page-level inspection of the 1988–1989 papers where exact circuit wording matters;
- earlier NAND-string patent / device genealogy and commercial-shipment chronology;
- direct citation / influence genealogy between early Toshiba NAND work and later mapping / FTL actors;
- later controller policies such as garbage collection, wear leveling, read-retry, refresh, and bad-block management except where separately grounded in other cases;
- device-level experiments or electrical characterization.

Broader semiconductor-memory history belongs primarily in `computing-archaeology`; this record exists to prevent Case 04 from collapsing device geometry into later logical-retention machinery.
'''

evidence_path.write_text(EVIDENCE, encoding="utf-8")

case_anchor = """**Primary bibliographic anchor:** F. Masuoka, M. Momodomi, Y. Iwata, R. Shirota, IEDM Technical Digest 1987, pp. 552–555, DOI `10.1109/IEDM.1987.191485`.\n\n### H/S + H/P — FTL terminology is public by February 1995, while approval and release remain separate milestones"""
case_replacement = """**Primary bibliographic anchor:** F. Masuoka, M. Momodomi, Y. Iwata, R. Shirota, IEDM Technical Digest 1987, pp. 552–555, DOI `10.1109/IEDM.1987.191485`.\n\n**Early NAND device-geometry deepening:** [`evidence/04-1987-1989-nand-device-geometry-before-ftl-deepening.md`](../evidence/04-1987-1989-nand-device-geometry-before-ftl-deepening.md) follows the 1987 proposal into 1988–1989 peer-reviewed Toshiba device papers. Their public abstracts expose selective/successive programming, an eight-bit serial NAND string with reduced select/contact overhead, page programming, block erasing, and random reading before the later mapped-storage line. The boundary is explicit: `NAND string / block-page operation geometry != FTL / logical-to-physical remapping`; the historical ordering is not promoted into an actor-to-actor genealogy.\n\n### H/P + E — late-1980s NAND operation geometry predates this case's mapping semantics\n\nThe 1989 ISSCC record describes eight bits arranged in series between two select transistors and page-mode programming; the 1989 JSSC record explicitly names block erasing, successive programming, and random reading. These are device/circuit facts. They establish a nonvolatile array with shared operation geometry, not a virtual sector namespace.\n\nFor this case the distinction is now source-controlled:\n\n```text\nNAND cell/string organization\n    + block/page program/read/erase operations\n        !=\nlogical identity retained while physical embodiment changes\n```\n\nThe latter relation still enters with the 1992–1995 mapping evidence below. A later FTL can functionally mediate constraints created by Flash geometry, but no direct influence from the 1987–1989 Toshiba papers to Ban/Intel/PCMCIA is asserted. Direct full-text inspection of the 1987 paper remains open.\n\n### H/S + H/P — FTL terminology is public by February 1995, while approval and release remain separate milestones"""
replace_once(case_path, case_anchor, case_replacement)

ground_anchor = """## Masuoka 1987 status — deliberately not overclaimed\n\nFujio Masuoka, Momodomi, Iwata, and Shirota's IEDM 1987 paper, `New ultra high density EPROM and Flash EEPROM with NAND structure cell`, remains an important earlier device-history boundary (IEDM Technical Digest 1987, pp. 552–555, DOI `10.1109/IEDM.1987.191485`).\n\nDuring this grounding pass, bibliographic metadata and abstract-level records were recoverable, but a directly inspectable full text was not obtained. Therefore:"""
ground_replacement = """## Masuoka 1987 status — deliberately not overclaimed\n\nFujio Masuoka, Momodomi, Iwata, and Shirota's IEDM 1987 paper, `New ultra high density EPROM and Flash EEPROM with NAND structure cell`, remains an important earlier device-history boundary (IEDM Technical Digest 1987, pp. 552–555, DOI `10.1109/IEDM.1987.191485`).\n\nA directly inspectable full 1987 text still was not obtained. A companion deepening now follows the bounded abstract-level 1987 record into 1988–1989 peer-reviewed Toshiba device publications that explicitly expose selective/successive programming, serial NAND-string topology, page programming, block erase, and random read: [`04-1987-1989-nand-device-geometry-before-ftl-deepening.md`](04-1987-1989-nand-device-geometry-before-ftl-deepening.md). That new chain strengthens the pre-FTL **device-operation** boundary without treating it as mapping history.\n\nTherefore:"""
replace_once(grounding_path, ground_anchor, ground_replacement)

road_anchor = """## Phase 2 — Build missing technical bridges\n\n- [x] **Case 115 HDFS snapshot normal edit-log replay deepening:**"""
road_replacement = """## Phase 2 — Build missing technical bridges\n\n- [x] **Case 04 1987–1989 NAND device-geometry / pre-FTL deepening:** [`cases/04-flash-virtual-mapping-logical-identity.md`](cases/04-flash-virtual-mapping-logical-identity.md) + [`evidence/04-1987-1989-nand-device-geometry-before-ftl-deepening.md`](evidence/04-1987-1989-nand-device-geometry-before-ftl-deepening.md) separate the late-1980s Toshiba NAND device publication chain from the 1992–1995 mapping/FTL layer. The 1987 abstract establishes a dense NAND-structure proposal with selective bit programming; 1988–1989 peer-reviewed records add successive programming, an eight-bit serial string with reduced select/contact overhead, page programming, block erasing, random reading, and block-page programming. This closes the bounded `early NAND device geometry != later FTL semantics` seam and fixes `block erase != garbage collection`, `page programming != remapping`, and `historical ordering != demonstrated genealogy`. Direct page-level inspection of the 1987 IEDM paper, earlier patent/shipment chronology, and actor-to-actor influence genealogy remain open; broader semiconductor-memory history belongs primarily in `computing-archaeology`.\n\n- [x] **Case 115 HDFS snapshot normal edit-log replay deepening:**"""
replace_once(roadmap_path, road_anchor, road_replacement)

FINDINGS = r'''### Findings 3828–3843 — Case 04 late-1980s NAND device geometry before FTL semantics

- **3828 — H/P** — The abstract-level record for Masuoka et al., IEDM 1987, presents a NAND-structure cell as a density technique, reports 6.43 µm² under a 1.0-µm rule and about 30% lower area per bit than the compared conventional 4-Mbit EPROM structure, and says individual NAND-cell bits can be selectively programmed.
- **3829 — H/P** — Momodomi et al., IEDM 1988, describe a 5-V-only NAND EEPROM program regime using half programming voltage on unselected bit lines plus successive programming to retain threshold margin, with experimentally confirmed cell reliability in the abstract-level record.
- **3830 — H/P** — Itoh et al., ISSCC 1989, describe an experimental 512K×8 EEPROM whose NAND structured cell places eight bits in series between two select transistors, reducing select-transistor and contact-hole overhead per bit.
- **3831 — H/P** — The same ISSCC record reports 10^4-cycle endurance for the experimental device and page mode for high-speed programming; these are device/circuit characteristics rather than evidence of a logical block map.
- **3832 — H/P** — Momodomi et al., IEEE JSSC 1989, explicitly list block erasing, successive programming, and random reading as operations implemented by the NAND-cell control circuit.
- **3833 — H/P** — A 1989 Toshiba-authored CICC paper separately describes a 4-Mbit NAND EEPROM with high-speed block-page programming circuits for microcomputer applications, corroborating that nontrivial program granularity predates the Case-04 mapping line.
- **3834 — E** — `NAND serial-string density optimization != logical-to-physical translation`: sharing select devices / contacts explains a device-layout advantage but does not determine which physical embodiment is current for a stable host-visible identity.
- **3835 — E** — `block erase != garbage collection`: a physical erase operation can exist without the copy-current / retire-old / remap policy relation grounded later by Ban/Wells/FTL sources.
- **3836 — E** — `page or successive programming != logical remapping`; a device programming mode does not by itself preserve one external logical address while relocating data.
- **3837 — E** — `random reading != random in-place overwrite`; the ability to select/read data does not erase the physical program/erase asymmetry later mapping layers must mediate.
- **3838 — E** — `device-level nonvolatility != logical-identity continuity across relocation`; the former concerns persistence of cell state, while the latter additionally requires retained currentness / mapping relations.
- **3839 — FA** — The later Case-04 mapping layer can be compared functionally as machinery that mediates Flash operation constraints and a stable-looking rewritable namespace, but the comparison does not establish direct descent from the Toshiba device papers.
- **3840 — X** — Publication order `1987–1989 NAND device papers -> 1992–1995 mapping/FTL evidence` is not evidence of an actor-to-actor citation, influence, standards, or implementation genealogy.
- **3841 — X** — The inspected records do not establish that 1987 is the first NAND invention, first commercial NAND shipment, or first use of every listed program/erase technique.
- **3842 — X** — Because the 1987 paper was not page-by-page inspected in this pass, abstract-level evidence is not promoted into unsupported circuit details or exact full-paper wording; direct full-text inspection remains open.
- **3843 — X** — `block erase` in these device records is not evidence of host-level deletion, reclamation completion, secure sanitization, or forensic non-recoverability.
'''
append_once(index_path, "### Findings 3812–3827", "### Findings 3828–3843", FINDINGS)
