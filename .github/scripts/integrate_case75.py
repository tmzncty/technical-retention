from pathlib import Path

CASE_PATH = "cases/75-nvme13-reservation-persistence-ptpl.md"
EVIDENCE_PATH = "evidence/75-nvme-2001-2019-reservation-persistence-grounding.md"


def update_readme() -> None:
    p = Path("README.md")
    text = p.read_text()
    if CASE_PATH not in text:
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if "cases/74-linux-jbd-revoke-stale-replay-suppression.md" in line:
                lines.insert(
                    i + 1,
                    "- [`Case 75 — NVM Express 1.3d Reservations: Retained Access Authority, PTPL, and Preemption`](cases/75-nvme13-reservation-persistence-ptpl.md) — `grounded`; registration/reservation state survives ordinary controller/subsystem reset, while namespace PTPL separately decides whether that access-authority relation crosses power loss. Preemption changes authority without relocating payload, and Reservation Report `GEN` is bounded change evidence rather than a complete history. Grounding: [`evidence/75-nvme-2001-2019-reservation-persistence-grounding.md`](evidence/75-nvme-2001-2019-reservation-persistence-grounding.md).",
                )
                break
        else:
            raise RuntimeError("README Case 74 anchor not found")
        text = "\n".join(lines) + "\n"

    text = text.replace("After seventy-five bounded cases", "After seventy-six bounded cases")
    text = text.replace("all seventy-five cases are now `grounded`", "all seventy-six cases are now `grounded`")
    p.write_text(text)


def update_roadmap() -> None:
    p = Path("ROADMAP.md")
    text = p.read_text()
    marker = "- [x] In reservation-capable NVMe namespaces, separate `namespace payload`, `registration/key state`, `reservation-holder/type state`, ordinary reset persistence, `PTPL` power-loss policy, current-state reporting, and preemption/clear/release authority"
    if marker not in text:
        anchor = "- [ ] How should `command completion`, `volatile-cache residence`, `nonvolatile-media commitment`, `cross-command ordering`, and `power-fail atomicity` be separated at storage interfaces?"
        addition = (
            marker
            + " — grounded in [`cases/75-nvme13-reservation-persistence-ptpl.md`](cases/75-nvme13-reservation-persistence-ptpl.md), with [`evidence/75-nvme-2001-2019-reservation-persistence-grounding.md`](evidence/75-nvme-2001-2019-reservation-persistence-grounding.md); named-controller implementation/fault validation and a full SCSI→NVMe reservation genealogy remain separate work."
        )
        if anchor not in text:
            raise RuntimeError("ROADMAP storage-interface anchor not found")
        text = text.replace(anchor, anchor + "\n" + addition, 1)
    p.write_text(text)


def update_case_index() -> None:
    p = Path("CASE_INDEX.md")
    text = p.read_text()

    main_row = "| [NVM Express 1.3d Reservations: Retained Access Authority, PTPL, and Preemption](cases/75-nvme13-reservation-persistence-ptpl.md) | **grounded** | namespace registration keys + registrant/holder/type authority state + reset persistence + namespace PTPL policy + current Reservation Report/GEN + release/clear/preemption transitions | separate payload durability from authority durability; ordinary reset from power-loss reset; reservation support from PTPL enablement; current authority state from complete history; and preemption from payload relocation or sanitization | [2001–2019 SCSI/NVMe reservation-persistence grounding](evidence/75-nvme-2001-2019-reservation-persistence-grounding.md); named-controller PTPL implementation/fault validation, NVMe-oF deployment behavior, exact NVMe introduction revision, and full SCSI→NVMe genealogy remain separate work |"
    if main_row not in text:
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if line.startswith("| [") and "cases/74-linux-jbd-revoke-stale-replay-suppression.md" in line:
                lines.insert(i + 1, main_row)
                break
        else:
            raise RuntimeError("CASE_INDEX Case 74 ledger row not found")
        text = "\n".join(lines) + "\n"

    matrix_row = "| NVMe 1.3d reservations / 2019 bounded regime | namespace user payload + registration keys + registrant/holder/type authority state + namespace PTPL state + wrapping GEN/current report | no payload rewrite merely to retain authority; Register/Acquire/Release/Clear/Preempt revise control state; ordinary reset preserves it while PTPL separately governs power-loss retention | reads/writes may be allowed or rejected with Reservation Conflict according to holder/registrant/type state; Reservation Report reads current authority state | namespace/Host Identifier/reservation-key relations identify who is registered and who may act; physical metadata placement is unspecified | payload location need not change when authority changes; reservation relations can survive reset or be forgotten at power loss independently of payload | no complete authority history by default; current status plus wrapping GEN and optional notifications are not an append-only audit log |"
    if matrix_row not in text:
        lines = text.splitlines()
        inserted = False
        for i, line in enumerate(lines):
            if line.startswith("| Linux JBD") and "revoke" in line.lower():
                lines.insert(i + 1, matrix_row)
                inserted = True
                break
        if not inserted:
            try:
                end = lines.index("## Cross-case findings")
            except ValueError:
                # The next case-findings heading is also a safe matrix terminator.
                start = next(i for i, line in enumerate(lines) if line.startswith("## Comparison matrix"))
                end = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("## Case "))
            lines.insert(end, matrix_row)
        text = "\n".join(lines) + "\n"

    text = text.replace("After seventy-five bounded cases", "After seventy-six bounded cases")
    text = text.replace("all seventy-five cases are now `grounded`", "all seventy-six cases are now `grounded`")

    if "## Case 75 — NVMe reservation-persistence findings" not in text:
        findings = """
## Case 75 — NVMe reservation-persistence findings

877. **payload durability ≠ access-authority durability** — namespace data can survive while reservation registrations/holder state are deliberately cleared at a power-loss boundary, or both state classes can survive;
878. **Controller Level Reset / NVM Subsystem Reset ≠ power-loss reset** — Revision 1.3d preserves registrations and reservations across the former while making the latter separately conditional on PTPL;
879. **reset-persistent authority ≠ power-loss-persistent authority** — the word `persistent` is incomplete unless the failure boundary is named;
880. **PTPL capability/state support ≠ PTPL currently enabled** — a reservation-capable namespace exposes PTPL state, but the current value determines whether reservation/registrant relations cross power loss;
881. **PTPL state ≠ reservation/registrant state** — PTPL is second-order control state that decides the failure-boundary retention policy of the access-authority relation itself;
882. **specified persistence semantics ≠ specified physical persistence implementation** — NVMe defines externally visible reservation survival/clearing behavior without prescribing the medium that stores reservation metadata;
883. **registration/key state ≠ reservation-holder state ≠ reservation type** — becoming a registrant, holding a reservation, and determining the exclusion rule are separate relations in the normative model;
884. **payload presence ≠ command admissibility** — intact namespace bytes can coexist with `Reservation Conflict` because retained authority state qualifies who may read/write;
885. **authority transfer ≠ payload relocation** — preemption can replace registrations/holder state atomically while leaving the namespace payload in place;
886. **Preempt and Abort ≠ guaranteed instantaneous cancellation** — the standard explicitly treats abort of affected in-flight commands as best effort and waits for abort or ordinary completion;
887. **explicit Release ≠ Clear ≠ power-loss-triggered authority forgetting** — orderly holder release, administrative clearing, and PTPL=0 failure-boundary clearing have different triggers and semantics;
888. **authority forgetting ≠ media sanitization** — clearing reservation relations does not establish erase, overwrite, cryptographic severance, or forensic absence of namespace payload;
889. **Reservation Report current state ≠ complete authority history** — the report exposes current registration/reservation state plus a 32-bit wrapping GEN counter rather than an append-only transition record;
890. **GEN change evidence ≠ event chronology** — selected successful reservation operations increment GEN, but the counter does not preserve actors, a full ordered transition record, or old values after wrap;
891. **NVMe reservation persistence ≠ NVMe Persistent Event Log** — Case 75 retains current exclusion authority across chosen failure boundaries, whereas Case 66 retains a bounded device-event history with different lifecycle/retrieval rules;
892. **NVMe 1.3d reservation/PTPL semantics ≠ invention of persistent reservations** — SPC-2/SPC-3-era T10 material already documents reservation keys, preemption, and optional persist-through-power-loss behavior; the grounded claim is the NVMe-specific normative composition, not first invention.
"""
        text = text.rstrip() + "\n\n" + findings.strip() + "\n"

    p.write_text(text)


def validate() -> None:
    for path in ["README.md", "ROADMAP.md", "CASE_INDEX.md", CASE_PATH, EVIDENCE_PATH]:
        if not Path(path).exists():
            raise RuntimeError(f"missing expected file: {path}")
    assert CASE_PATH in Path("README.md").read_text()
    assert CASE_PATH in Path("ROADMAP.md").read_text()
    idx = Path("CASE_INDEX.md").read_text()
    assert CASE_PATH in idx
    assert EVIDENCE_PATH in idx
    assert "877. **payload durability ≠ access-authority durability**" in idx
    assert "892. **NVMe 1.3d reservation/PTPL semantics ≠ invention of persistent reservations**" in idx


update_readme()
update_roadmap()
update_case_index()
validate()
print("Case 75 navigation/status integration staged successfully")
