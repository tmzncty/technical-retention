from pathlib import Path


def insert_after(lines, prefix, new_line):
    if new_line in lines:
        return
    idx = next(i for i, line in enumerate(lines) if line.startswith(prefix))
    lines.insert(idx + 1, new_line)


# README
p = Path("README.md")
original = p.read_text()
lines = original.splitlines()
insert_after(
    lines,
    "- [`cases/30-nvme14-pmr-persistence-barriers.md`](cases/30-nvme14-pmr-persistence-barriers.md)",
    "- [`cases/31-snia-nvm-persistence-domain-boundary.md`](cases/31-snia-nvm-persistence-domain-boundary.md) — grounded terminology/programming-model bridge: SNIA's 2013 NVM model defines `durable` through a `persistence domain`, separates store execution and cache/buffer residency from domain arrival, conditions recovery on tolerated failure patterns, and keeps synchronization distinct from atomicity/order; the exact term is not silently reassigned to NVMe PMR.",
)
insert_after(
    lines,
    "- [`evidence/30-nvme14-2019-pmr-grounding.md`](evidence/30-nvme14-2019-pmr-grounding.md)",
    "- [`evidence/31-snia-2013-persistence-domain-grounding.md`](evidence/31-snia-2013-persistence-domain-grounding.md) — Case-31 grounding record: official SNIA Version 1 text anchors the 2013 `persistence domain`, multiple-domain/configuration semantics, PM sync/flush closure, failure-qualified recoverability, and atomicity/order limits; official ratified NVMe 1.4 and 2.0 provide a bounded negative terminology check without claiming universal absence or first use.",
)
p.write_text("\n".join(lines) + ("\n" if original.endswith("\n") else ""))


# ROADMAP
p = Path("ROADMAP.md")
original = p.read_text()
lines = original.splitlines()
ssd_line = "- [ ] SSD FTL/controller-mediated persistence beyond the bounded Ban/1990s case — **partially advanced by grounded Cases 15, 20, 30, and 31**. [`cases/15-intel-ssd320-power-loss-durability.md`](cases/15-intel-ssd320-power-loss-durability.md) uses 2007 ATA8-ACS standards-development text plus Intel's 2011 SSD 320 product/design material to separate volatile write-cache/temporary-buffer state, nonvolatile NAND, explicit `FLUSH CACHE` completion, orderly `STANDBY IMMEDIATE` handoff, and a power-failure-triggered capacitor-backed emergency transfer. [`cases/20-nvme10-fua-flush-persistence-ordering.md`](cases/20-nvme10-fua-flush-persistence-ordering.md), grounded by [`evidence/20-nvme10-2011-flush-fua-grounding.md`](evidence/20-nvme10-2011-flush-fua-grounding.md), separately uses the official ratified NVMe 1.0 specification to distinguish VWC classification, volatile→nonvolatile Flush, per-write FUA media commitment, cross-command ordering, and normal-versus-power-fail atomicity. [`cases/30-nvme14-pmr-persistence-barriers.md`](cases/30-nvme14-pmr-persistence-barriers.md), grounded by [`evidence/30-nvme14-2019-pmr-grounding.md`](evidence/30-nvme14-2019-pmr-grounding.md), adds a later NVMe interface regime in which a PCIe Persistent Memory Region persists across specified power/reset/disable transitions while Posted-write completion, read-based persistence barriers, readiness/restore health, and implementation-specific nonvolatile staging remain separate relations. [`cases/31-snia-nvm-persistence-domain-boundary.md`](cases/31-snia-nvm-persistence-domain-boundary.md), grounded by [`evidence/31-snia-2013-persistence-domain-grounding.md`](evidence/31-snia-2013-persistence-domain-grounding.md), corrects the terminology boundary: SNIA's approved 2013 programming model already defines `durable` through a `persistence domain`, conditions recovery on the failure pattern tolerated by that domain, allows multiple administratively aligned domains, and keeps domain arrival separate from atomicity/order. Exact-text checks found no `persistence domain` match in the inspected ratified NVMe 1.4/2.0 PDFs, so future work should ask whether/where NVMe later adopts the phrase rather than presuppose an NVMe origin. The broad item stays unchecked because controller-metadata recovery, enterprise PLP qualification, named-controller fault compliance, platform-specific ADR/eADR or other persistence-domain implementations, exact later NVMe 2.1+ terminology if evidence warrants it, and filesystem/database composition remain distinct regimes; the independent FAST '13 fault-injection evidence in Case 15 remains a contract-versus-compliance boundary rather than silently assigned to a named product."
for i, line in enumerate(lines):
    if line.startswith("- [ ] SSD FTL/controller-mediated persistence beyond the bounded Ban/1990s case"):
        lines[i] = ssd_line
        break
else:
    raise RuntimeError("ROADMAP SSD priority line missing")

question_anchor = "- [ ] How should `command completion`, `volatile-cache residence`, `nonvolatile-media commitment`, `cross-command ordering`, and `power-fail atomicity` be separated at storage interfaces?"
question_new = "- [ ] How should `store execution`, processor/controller-buffer residence, persistence-domain arrival, synchronization completion, failure-qualified recoverability, atomicity, and ordering be separated in persistent-memory programming models?"
insert_after(lines, question_anchor, question_new)

old_sentence = "Later `persistence domain` terminology should be sourced in its own revision-specific case rather than projected back onto 2011."
new_sentence = "Case 31 now grounds `persistence domain` as SNIA Version-1 vocabulary by December 2013 and therefore blocks projection onto 2011 NVMe; future NVMe terminology work should establish an exact revision/TP adoption before assigning the phrase to NVMe itself."
for i, line in enumerate(lines):
    if line.startswith("The grounded NVMe 1.0 interface bridge sharpens"):
        if old_sentence not in line and new_sentence not in line:
            raise RuntimeError("ROADMAP NVMe terminology sentence changed")
        lines[i] = line.replace(old_sentence, new_sentence)
        nvme_idx = i
        break
else:
    raise RuntimeError("ROADMAP NVMe paragraph missing")

snia_para = "The grounded SNIA persistence-domain bridge adds a cross-layer durability boundary that Cases 15, 20, and 30 did not themselves name. SNIA Version 1 defines `durable` as committed to a `persistence domain`, allows mapped stores to remain in processor caches or memory-controller buffers before crossing that boundary, permits multiple persistence domains whose volume/filesystem alignment is administrative, and states that post-restart recoverability still depends on whether the actual failure pattern is tolerated by the domain's design/configuration. `NVM.PM.FILE.SYNC` can force a requested range to the domain, but the same source withholds write atomicity and permits bytes to have arrived before the call; optimized flush additionally withholds ordering and can leave indeterminate partial progress under failure. Future persistence comparisons should therefore separate **store execution**, **buffer/cache residency**, **domain arrival**, **sync closure**, **failure envelope**, **atomicity**, **ordering**, and **administrative alignment**. The exact term is historical SNIA vocabulary no later than 2013; ratified NVMe 1.4/2.0 retain PMR-specific wording in the inspected texts, so `persistence domain` and `Persistent Memory Region` must remain distinct unless a source establishes an explicit mapping."
if snia_para not in lines:
    lines.insert(nvme_idx + 1, "")
    lines.insert(nvme_idx + 2, snia_para)

forget_anchor = "- [ ] FUA/Flush misuse, missing host-enforced ordering, or power-fail atomicity assumptions that exceed the interface contract;"
forget_new = "- [ ] treating a mapped store or cache/controller-buffer residence as persistence-domain arrival; assuming sync supplies atomicity/order; failure patterns outside the configured domain; or domain/volume/filesystem misalignment;"
insert_after(lines, forget_anchor, forget_new)

p.write_text("\n".join(lines) + ("\n" if original.endswith("\n") else ""))


# CASE_INDEX
p = Path("CASE_INDEX.md")
original = p.read_text()
lines = original.splitlines()
case_row = "| [SNIA NVM Programming Model v1: Persistence Domain as a Durability Boundary](cases/31-snia-nvm-persistence-domain-boundary.md) | **grounded** | mapped persistent-memory bytes + processor/controller pre-domain state + synchronization-to-domain relation + failure-model/configuration relation + multiple domain/volume/filesystem alignment | separate store execution, buffering, persistence-domain arrival, sync closure, recoverability, atomicity, and ordering; anchor `persistence domain` as 2013 SNIA vocabulary without renaming NVMe PMR | [2013 SNIA persistence-domain grounding](evidence/31-snia-2013-persistence-domain-grounding.md); pre-2013 term genealogy, SNIA v1.1+, platform ADR/eADR mappings, exact later NVMe 2.1+ adoption, OS/PMDK composition, and named-hardware compliance remain separate work |"
insert_after(lines, "| [NVM Express 1.4 Persistent Memory Region: Posted Writes, Persistence Barriers, and Restore Health](cases/30-nvme14-pmr-persistence-barriers.md)", case_row)

matrix_row = "| SNIA NVM Programming Model / 2013 bounded regime | mapped PM-file bytes + processor/cache/controller pre-domain state + abstract persistence-domain/failure relation + domain-to-volume/filesystem alignment | direct stores; implementation-specific cache/buffer draining; `NVM.PM.FILE.SYNC` / optimized flush; administrative domain alignment; restart recovery | mapped loads/stores are ordinary memory accesses; successful sync guarantees the named range has reached the domain by completion but supplies neither write atomicity nor a timestamp for earlier arrival | PM file/range → mapped address → PM implementation → one applicable persistence domain; multiple domains may coexist and be aligned with volumes/filesystems | physical embodiment is intentionally unspecified; bytes may move through caches/buffers before crossing the software durability boundary | no complete history; current bytes plus mapping, persistence qualification, failure-envelope, and configuration relations are retained |"
insert_after(lines, "| NVM Express PMR / 2019 bounded regime |", matrix_row)

text = "\n".join(lines)
text = text.replace(
    "After thirty-one bounded cases, **all thirty-one cases are now `grounded`.**",
    "After thirty-two bounded cases, **all thirty-two cases are now `grounded`.**",
    1,
)
text = text.replace(
    "exact later `persistence domain` terminology/revisions, named-controller implementation/compliance",
    "SNIA 2013 `persistence domain` terminology is now grounded in Case 31; exact later NVMe adoption, named-controller implementation/compliance",
    1,
)
text = text.replace(
    "exact later `persistence domain` terminology, named-controller implementations, host PMEM programming models",
    "SNIA 2013 persistence-domain semantics are now handled in Case 31; exact later NVMe adoption, named-controller implementations, broader host PMEM programming models",
    1,
)

findings = """280. **persistence domain ≠ persistent medium** — SNIA Version 1 defines a software-visible location/boundary for durability across restart while deliberately spanning multiple NVM device models; the term does not name one universal chip, controller, or media technology.
281. **persistence-domain arrival ≠ unconditional recoverability** — §6.9 says data that reached the domain may be recoverable and conditions recovery on whether the actual failure pattern is tolerated by the domain's design/configuration; survival is qualified by a failure envelope.
282. **store execution ≠ persistence qualification** — mapped PM writes may remain in processor-resident caches or memory-controller buffers before reaching a persistence domain, so direct load/store access does not eliminate a durability boundary.
283. **successful synchronization ≠ write atomicity** — `NVM.PM.FILE.SYNC` guarantees the requested range reaches the persistence domain by successful completion while explicitly withholding write atomicity; durable arrival and failure-consistent update are separate properties.
284. **persistence synchronization ≠ ordering guarantee** — `NVM.PM.FILE.OPTIMIZED_FLUSH` explicitly supplies neither atomicity nor ordering for synchronized byte ranges; a higher-level consistency protocol cannot be inferred from the durability primitive.
285. **sync completion ≠ exact persistence timestamp** — SNIA allows a range to reach the persistence domain before the sync action, so successful completion closes an obligation by a deadline rather than proving when every byte crossed the boundary.
286. **multiple persistence domains ≠ one global machine durability boundary** — SNIA allows several domains in one system and makes their alignment with volumes/filesystems an administrative act, so durability configuration can participate in the retained recovery relation.
287. **interrupted flush progress ≠ retained completion map** — failure during optimized flush can leave some ranges persistent and others not, with no indication of which ranges completed; physical progress and knowledge of that progress are distinct states.
288. **historical term ownership ≠ functional similarity** — `persistence domain` is directly documented in SNIA's approved 2013 programming model, which separately cites NVMe 1.1; inspected ratified NVMe 1.4 and 2.0 use `Persistent Memory Region`/PMR barrier vocabulary and contain no exact-text match for the phrase. This supports a bounded vocabulary distinction, not a universal absence or invention claim.
289. **SNIA persistence domain ≠ NVMe PMR** — both can participate in software claims that earlier writes are persistent, but SNIA's term denotes a cross-layer durability location/failure boundary while PMR is a named NVMe PCIe memory region with its own barrier/readiness/health semantics; the comparison is functional, not synonymy or proven genealogy."""
marker = "These are provisional cross-case findings, not final philosophical conclusions."
if "280. **persistence domain ≠ persistent medium**" not in text:
    if marker not in text:
        raise RuntimeError("CASE_INDEX findings marker missing")
    text = text.replace(marker, findings + "\n\n" + marker, 1)

p.write_text(text + ("\n" if original.endswith("\n") else ""))
