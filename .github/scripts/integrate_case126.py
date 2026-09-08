from pathlib import Path

CASE_MARKER = "cases/126-nvme11-reservation-ptpl-authority-retention.md"

ROADMAP_BULLET = """- [x] NVMe 1.1 Reservation / Persist Through Power Loss access-authority boundary — [`cases/126-nvme11-reservation-ptpl-authority-retention.md`](cases/126-nvme11-reservation-ptpl-authority-retention.md), grounded by [`evidence/126-nvme-1998-2012-reservation-ptpl-grounding.md`](evidence/126-nvme-1998-2012-reservation-ptpl-grounding.md): the ratified 11 October 2012 NVMe 1.1 shared-namespace reservation contract separates registrant keys, active reservation type/holder, and namespace-specific `PTPL` policy; registrations/reservations survive ordinary controller/subsystem resets while power-loss survival is separately controlled by PTPL. T10/98-203r3 (24 July 1998) supplies an earlier public Persistent Reservations / `APTPL` prior-art floor without proving direct SCSI→NVMe genealogy. This closes only the bounded `namespace payload vs access-authority relation vs reset lifetime vs power-loss lifetime` relation; physical controller implementation, named-device conformance/fault injection, NVMe-oF evolution, cluster-software policy, and broad SCSI/SPC reservation genealogy remain open."""

POWER_LOSS = """- [ ] power loss — **partially advanced at the access-authority layer by grounded Case 126**: NVMe 1.1 makes reservation/registration state survive ordinary controller/subsystem resets while namespace-specific `PTPL` separately decides whether that coordination state survives a reset due to power loss. This grounds `controller-reset persistence ≠ power-loss persistence` and `payload survival ≠ access-authority survival` for one shared-storage protocol; physical-state loss, volatile-payload loss, controller-internal implementation, named-device fault behavior, and broader power-failure mechanisms remain open;"""

CASE_ROW = """| [NVMe 1.1 Reservations: Retained Access Authority Across Reset and Power Loss](cases/126-nvme11-reservation-ptpl-authority-retention.md) | **grounded** | shared-namespace registrant/reservation state + namespace-specific PTPL lifetime policy across controller/subsystem reset and optional power-loss survival | separate namespace payload, namespace identity, registrant population, active reservation, PTPL policy, and live controller/host state; establish reset-survival ≠ power-loss-survival and authority retention ≠ payload durability | [1998–2012 grounding record](evidence/126-nvme-1998-2012-reservation-ptpl-grounding.md); named-controller conformance, implementation storage, NVMe-oF evolution, and broad SCSI/cluster-fencing genealogy remain open |"""

FINDINGS = """## Case 126 — NVMe reservation / PTPL findings

- **2179 — NVMe 1.1 reservation date ≠ invention date:** NVM Express Revision 1.1 is dated 11 October 2012 and official NVM Express material identifies Reservations as a 1.1 addition, establishing a public NVMe floor without supporting an invention-priority claim. (`H/P`)
- **2180 — 1998 T10 APTPL ≠ NVMe-origin claim:** T10/98-203r3 already describes Persistent Reservations that survive reset/recovery actions and may be retained across power loss through APTPL; this is earlier functional/standards prior art, not proof of direct implementation genealogy. (`H/P`, `X`)
- **2181 — shared namespace lifetime ≠ one controller lifetime:** NVMe 1.1's multipath example allows one port/controller to reset without removing the other controller's access or the shared namespace itself. (`H/P`, `E`)
- **2182 — reservation capability ≠ active reservation:** a namespace may advertise reservation/PTPL support while having no current reservation holder or registrant population. (`H/P`, `E`)
- **2183 — registration key ≠ reservation authority:** registration qualifies a participant and supplies a protocol key; an active reservation separately determines current access rights. (`H/P`, `E`)
- **2184 — reset survival ≠ power-loss survival:** NVMe 1.1 preserves registrations/reservations across controller and NVM-subsystem resets except power-loss reset, whose survival is separately controlled by PTPL. (`H/P`, `E`)
- **2185 — PTPL policy state ≠ reservation state:** PTPL is a namespace-specific retained rule governing what happens to registrants/reservations at a future power-loss event; it is not itself the holder, key population, or reservation type. (`H/P`, `E`)
- **2186 — payload durability ≠ access-authority durability:** preserving reservation/registration state says nothing by itself about whether newest user writes reached their required persistence boundary, and clearing reservation state need not disturb namespace payload. (`E`)
- **2187 — authority survival ≠ actor survival:** controller queues, paths, or host processes may disappear while a retained reservation relation survives, so recovery may need explicit preempt/release/clear work. (`E`)
- **2188 — more persistent authority ≠ monotonically safer retention:** PTPL can protect multi-host coordination across power failure but can also preserve stale authority after the originating execution context is gone. (`E`)
- **2189 — namespace-specific PTPL ≠ controller-global persistence:** the lifetime policy is associated with reservation-supporting namespaces even though a controller may issue a Set Features operation across accessible namespaces. (`H/P`, `E`)
- **2190 — Reservation Report current state ≠ historical log:** PTPLS and registered-controller data expose current reservation state; they do not preserve the complete sequence of past holders, registrations, or preemptions. (`H/P`, `E`)
- **2191 — preempt/clear ≠ payload erasure:** reservation operations alter access qualification and holder/registrant state, not secure media sanitization or proof of user-data destruction. (`H/P`, `E`, `X`)
- **2192 — NVMe reservation ≠ NVMe namespace write protection:** Case 114 retains a mutation-authority policy on a namespace, while Case 126 retains relative multi-host participation/holder state; overlapping write-admission effects do not make the mechanisms identical. (`A`, `X`)
- **2193 — NVMe reservation fencing ≠ HDFS QJM epoch fencing:** both can retain authority state beyond one actor lifetime, but namespace reservation keys/types and quorum-persisted writer epochs have different mechanisms, scopes, and histories. (`A`, `X`)
- **2194 — related-repository boundary:** a fresh `tmzncty/computing-archaeology` search found no dedicated Persistent Reservation/APTPL/PTPL case to reuse; broad SCSI/SPC reservation genealogy, cluster fencing, and multipath adoption belong there if developed, while Case 126 remains retention-specific. (`H/P` project-state record)"""


def update_roadmap():
    p = Path("ROADMAP.md")
    text = p.read_text(encoding="utf-8")
    if CASE_MARKER not in text:
        anchor = "## Phase 2 — Build missing technical bridges\n\n"
        if anchor not in text:
            raise RuntimeError("ROADMAP Phase 2 anchor missing")
        text = text.replace(anchor, anchor + ROADMAP_BULLET + "\n", 1)
    if "- [ ] power loss;" in text:
        text = text.replace("- [ ] power loss;", POWER_LOSS, 1)
    elif "partially advanced at the access-authority layer by grounded Case 126" not in text:
        raise RuntimeError("ROADMAP power-loss anchor changed")
    p.write_text(text.rstrip() + "\n", encoding="utf-8")


def update_index():
    p = Path("CASE_INDEX.md")
    text = p.read_text(encoding="utf-8")
    if CASE_MARKER not in text:
        lines = text.splitlines()
        start = lines.index("## Cases")
        last = None
        for i in range(start + 1, len(lines)):
            if lines[i].startswith("## ") and i > start + 1:
                break
            if lines[i].startswith("| ["):
                last = i
        if last is None:
            raise RuntimeError("CASE_INDEX case table rows missing")
        lines.insert(last + 1, CASE_ROW)
        text = "\n".join(lines)
    if "## Case 126 — NVMe reservation / PTPL findings" not in text:
        if "**2178" not in text:
            raise RuntimeError("CASE_INDEX expected tail 2178 missing")
        text = text.rstrip() + "\n\n" + FINDINGS.rstrip() + "\n"
    p.write_text(text.rstrip() + "\n", encoding="utf-8")


update_roadmap()
update_index()
