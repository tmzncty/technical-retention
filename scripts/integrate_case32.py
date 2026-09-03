from pathlib import Path


def insert_after_line_containing(text: str, needle: str, new_line: str, *, require_prefix: str | None = None) -> str:
    lines = text.splitlines()
    matches = []
    for i, line in enumerate(lines):
        if needle in line and (require_prefix is None or line.startswith(require_prefix)):
            matches.append(i)
    if len(matches) != 1:
        raise RuntimeError(f"expected exactly one line containing {needle!r} with prefix {require_prefix!r}, got {len(matches)}")
    i = matches[0]
    if new_line in lines:
        raise RuntimeError(f"new line already present for {needle!r}")
    lines.insert(i + 1, new_line)
    return "\n".join(lines) + "\n"


# README navigation
p = Path("README.md")
readme = p.read_text()
case_line = "- [`cases/32-intel-adr-eadr-power-fail-domain.md`](cases/32-intel-adr-eadr-power-fail-domain.md) — grounded platform-persistence bridge: Intel's 2016 ADR model places memory-controller write-pending queues inside a power-fail-protected domain while processor caches remain outside; the 2020–2021 eADR platform description extends protection upstream to processor caches, changes ordinary cache-flush obligations, retains `SFENCE`, and makes OEM stored energy part of the power-fail durability path."
evidence_line = "- [`evidence/32-intel-2016-2021-adr-eadr-grounding.md`](evidence/32-intel-2016-2021-adr-eadr-grounding.md) — Case-32 grounding record: dated Intel first-party sources from 2016–2021 separate processor-cache residency, ADR-protected memory-controller WPQs, optional eADR cache inclusion, PMDK feature-sensitive flush behavior, retained `SFENCE`, and OEM stored-energy requirements without generalizing the sourced power-fail contract into universal crash persistence."
readme = insert_after_line_containing(readme, "cases/31-snia-nvm-persistence-domain-boundary.md", case_line, require_prefix="- [")
readme = insert_after_line_containing(readme, "evidence/31-snia-2013-persistence-domain-grounding.md", evidence_line, require_prefix="- [")
p.write_text(readme)


# ROADMAP bounded bridge status
p = Path("ROADMAP.md")
roadmap = p.read_text()
lines = roadmap.splitlines()
idx = [i for i, line in enumerate(lines) if line.startswith("- [ ] SSD FTL/controller-mediated persistence beyond")]
if len(idx) != 1:
    raise RuntimeError(f"expected one SSD roadmap line, got {len(idx)}")
i = idx[0]
line = lines[i]
old_count = "partially advanced by grounded Cases 15, 20, 30, and 31"
if old_count not in line:
    raise RuntimeError("SSD case-count anchor missing")
line = line.replace(old_count, "partially advanced by grounded Cases 15, 20, 30, 31, and 32", 1)
case32_sentence = " [`cases/32-intel-adr-eadr-power-fail-domain.md`](cases/32-intel-adr-eadr-power-fail-domain.md), grounded by [`evidence/32-intel-2016-2021-adr-eadr-grounding.md`](evidence/32-intel-2016-2021-adr-eadr-grounding.md), maps that abstract durability boundary onto a concrete Intel platform evolution: ADR power-fail-protects the memory-controller WPQ while leaving processor caches outside, whereas optional eADR extends protection into processor caches; PMDK can then omit ordinary cache flushes, but `SFENCE` and OEM stored energy remain separate obligations."
anchor = " The broad item stays unchecked because"
if anchor not in line:
    raise RuntimeError("SSD remaining-work anchor missing")
line = line.replace(anchor, case32_sentence + anchor, 1)
old_open = "platform-specific ADR/eADR or other persistence-domain implementations"
if old_open not in line:
    raise RuntimeError("ADR/eADR open-item anchor missing")
line = line.replace(old_open, "other platform-specific persistence-domain implementations", 1)
lines[i] = line
roadmap = "\n".join(lines) + "\n"
p.write_text(roadmap)


# CASE_INDEX: case table
p = Path("CASE_INDEX.md")
ci = p.read_text()
case_row = "| [Intel ADR/eADR: Moving the Power-Fail Protected Domain Upstream](cases/32-intel-adr-eadr-power-fail-domain.md) | **grounded** | direct-load/store persistent-memory state + processor caches + memory-controller WPQ + ADR/eADR failure-triggered drain + OEM stored-energy support + software flush/fence obligations | show that persistence can include volatile in-flight state when the platform guarantees failure-triggered transfer; separate ADR WPQ protection, eADR cache inclusion, software cache flush, `SFENCE`, platform capability, and final-media residence | [2016–2021 Intel ADR/eADR grounding](evidence/32-intel-2016-2021-adr-eadr-grounding.md); generic NVDIMM history, non-Intel platform domains, failure classes beyond sourced power-fail/shutdown behavior, and empirical fault qualification remain separate work |"
ci = insert_after_line_containing(ci, "cases/31-snia-nvm-persistence-domain-boundary.md", case_row, require_prefix="| [")

# CASE_INDEX: comparison matrix row immediately before its closing delimiter
matrix_row = "| Intel ADR/eADR / 2016–2021 bounded power-fail domain | intended persistent payload + modified processor-cache lines + memory-controller WPQ entries + persistent-memory media + platform capability/ordering relation + stored-energy reserve | ADR: software cache writeback plus failure-triggered WPQ drain; eADR: failure-triggered processor-cache drain followed by ADR, with PMDK feature detection and retained `SFENCE` | ordinary reads are outside the bounded mechanism question; post-power-fail correctness depends on the intended write surviving the protected path | cache-coherent application address resolves through processor/memory-controller path to persistent memory; durability additionally depends on which path stages are inside ADR/eADR protection | intermediate physical residence can remain volatile while the platform classifies it as power-fail protected; eADR moves the protected boundary upstream without changing the logical persistent address | no complete history; current payload plus capability, ordering, protected-path, and energy assumptions are retained |"
marker = "\n---\n\n## Cross-case findings already supported"
pos = ci.find(marker)
if pos == -1:
    raise RuntimeError("comparison-matrix closing marker missing")
if matrix_row in ci:
    raise RuntimeError("Case 32 matrix row already present")
ci = ci[:pos].rstrip("\n") + "\n" + matrix_row + "\n" + ci[pos:]

# CASE_INDEX: current count
old_intro = "After thirty-two bounded cases, **all thirty-two cases are now `grounded`.**"
new_intro = "After thirty-three bounded cases, **all thirty-three cases are now `grounded`.**"
if ci.count(old_intro) != 1:
    raise RuntimeError(f"current-count intro anchor count={ci.count(old_intro)}")
ci = ci.replace(old_intro, new_intro, 1)

# CASE_INDEX: findings 290–299
findings = """290. **persistence-domain membership ≠ physical nonvolatile-media residency** — Intel ADR places memory-controller WPQ state inside a power-fail-safe persistence domain because the platform guarantees a failure-triggered drain, even though the bytes may not yet reside in the persistent-memory DIMM.
291. **ADR-protected WPQ ≠ processor-cache persistence** — Intel explicitly keeps processor caches outside the ADR-only protected path; software must still move relevant modified cache lines toward the memory subsystem before relying on ADR.
292. **eADR domain expansion ≠ elimination of ordering/fencing** — eADR extends power-fail protection into processor caches and can remove ordinary PMDK cache-flush operations, while Intel still requires `SFENCE`; enlarging the protected physical path does not create every persistence ordering relation.
293. **same persistent-memory medium ≠ same software persistence obligation** — ADR and eADR can terminate in the same broad class of persistent memory while the required cache-flush work differs according to the platform capability exposed to software.
294. **power-fail protection ≠ universal crash/reset/failure survivability** — the Intel sources ground power-failure behavior and, for ADR, shutdown draining; they do not establish arbitrary reset, firmware-fault, media-corruption, transaction, or software-crash semantics.
295. **persistent qualification can depend on guaranteed future transfer work** — ADR/eADR can classify volatile intermediate state as protected because power-fail signaling, drain logic, and available energy promise a later transfer into persistent memory before the failure completes.
296. **stored energy ≠ payload, while stored energy can be retention infrastructure** — Intel requires additional OEM stored energy for eADR; the reserve carries no user bytes but is part of the mechanism that makes failure-triggered cache draining credible.
297. **platform capability detection can change which retention work software performs** — Intel states that PMDK detects eADR and can omit explicit flush operations when it is present, making the persistence algorithm conditional on discoverable platform state rather than only on the memory module.
298. **ADR/eADR ≠ NVMe Flush/FUA/PMR or SSD-controller PLP** — the bounded similarity is power-fail persistence work; the historical interfaces, protected state, authority, and transfer paths differ across Cases 15, 20, 30, and 32.
299. **ADR `Asynchronous DRAM Refresh` ≠ SDRAM `SELF REFRESH`** — Intel's ADR source describes imminent-power-fail signaling and WPQ draining, while Case 21 grounds recurring in-device DRAM refresh under a retention mode; shared `refresh` vocabulary does not establish mechanism identity."""
anchor = "\nThese are provisional cross-case findings, not final philosophical conclusions."
if anchor not in ci:
    raise RuntimeError("findings closing anchor missing")
if "290. **persistence-domain membership" in ci:
    raise RuntimeError("Case 32 findings already present")
ci = ci.replace(anchor, "\n" + findings + "\n" + anchor, 1)

# CASE_INDEX: add Case 32 to the case-by-case synthesis narrative
narrative = "\nCase 32 is the grounded Intel platform-persistence continuation; [`evidence/32-intel-2016-2021-adr-eadr-grounding.md`](evidence/32-intel-2016-2021-adr-eadr-grounding.md) uses dated Intel first-party sources to place memory-controller WPQs inside the ADR power-fail protected domain, keep processor caches outside that boundary under ADR, then extend protection upstream with optional eADR while preserving `SFENCE` and an explicit OEM stored-energy requirement. This concretizes Case 31's abstract persistence-domain relation without treating ADR/eADR as a universal platform model, an NVMe mechanism, or ordinary SDRAM self refresh.\n"
gate_marker = "\n---\n\n## Current synthesis gate"
pos = ci.find(gate_marker)
if pos == -1:
    raise RuntimeError("synthesis-gate marker missing")
if "Case 32 is the grounded Intel platform-persistence continuation" in ci:
    raise RuntimeError("Case 32 synthesis narrative already present")
ci = ci[:pos].rstrip("\n") + narrative + ci[pos:]

# CASE_INDEX: gate count + explicit new gate witness
old_gate_count = "currently thirty-two;"
if ci.count(old_gate_count) != 1:
    raise RuntimeError(f"gate count anchor count={ci.count(old_gate_count)}")
ci = ci.replace(old_gate_count, "currently thirty-three;", 1)
gate_anchor = "- [x] at least one host/controller persistence-interface case where per-command media commitment, cross-command ordering, and power-fail atomicity are separately grounded — NVMe 1.0 Case 20;"
new_gate = "- [x] at least one platform persistence-domain case where power-fail protection includes volatile intermediate state and moving the boundary changes software flush obligations without eliminating ordering — Intel ADR/eADR Case 32;"
if ci.count(gate_anchor) != 1:
    raise RuntimeError(f"gate witness anchor count={ci.count(gate_anchor)}")
ci = ci.replace(gate_anchor, gate_anchor + "\n" + new_gate, 1)

p.write_text(ci)

print("integrated Case 32 navigation/status")
