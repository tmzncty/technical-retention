from pathlib import Path
import textwrap

ROOT = Path('.')
case_path = ROOT / 'cases/149-micron-nand-otp-data-protect-irreversible-authority.md'
roadmap_path = ROOT / 'ROADMAP.md'
index_path = ROOT / 'CASE_INDEX.md'
base_evidence_path = ROOT / 'evidence/149-micron-2004-2006-nand-otp-data-protect-grounding.md'
new_evidence_path = ROOT / 'evidence/149-onfi10-20-vendor-feature-space-otp-interface-deepening.md'
workflow_path = ROOT / '.github/workflows/tmp-case149-onfi-interface-integrate.yml'
script_path = ROOT / '.github/scripts/tmp_case149_onfi_interface_integrate.py'

assert not new_evidence_path.exists(), f'{new_evidence_path} already exists'

new_evidence = textwrap.dedent(r'''
# Evidence 149B — ONFI vendor space and Micron OTP interface migration

## Purpose

Deepen Case 149 at the standards/interface boundary without turning a documented chronology into a genealogy claim.

The bounded question is not whether ONFI standardized an OTP retention policy. It is narrower:

> how did Micron's dedicated `A0h/A5h/AFh` OTP command vocabulary coexist with ONFI command/feature namespaces, and what later Micron evidence shows a move toward `SET FEATURES`-selected OTP modes while retaining the same broad program/protect/read authority relation?

This record separates historical primary claims (`H/P`), mirrored-primary manufacturer evidence (`H/P*`), engineering reconstruction (`E`), functional analogy (`A`), project interpretation (`I`), and rejected upgrades / stop conditions (`X`).

---

## Source ledger

### S1 — ONFI 1.0 final specification, 28-Dec-2006 (`H/P`)

- Organization: Open NAND Flash Interface Workgroup.
- Document: `Open NAND Flash Interface Specification`, Revision 1.0.
- Date: **28-Dec-2006**.
- First-party URL: <https://onfi.org/files/onfi_1_0_gold.pdf>

Relevant records:

- the opcode-reservation table classifies `91h-BFh` as **Vendor Specific**;
- therefore Micron's documented legacy OTP first command bytes `A0h`, `A5h`, and `AFh` all lie inside that vendor-specific opcode range;
- ONFI 1.0 already defines `GET FEATURES (EEh)` / `SET FEATURES (EFh)`;
- the feature-parameter table reserves `80h-FFh` as **Vendor specific**.

Chronology guardrail: Micron's Case-149 product witness is only dated `Rev. D 12/06`, while ONFI 1.0 is dated 28-Dec-2006. The available documents do **not** establish which December document appeared first.

### S2 — ONFI 2.0 final specification, 27-Feb-2008 (`H/P`)

- Organization: Open NAND Flash Interface Workgroup.
- Document: `Open NAND Flash Interface Specification`, Revision 2.0.
- Date: **27-Feb-2008**.
- First-party URL: <https://onfi.org/files/onfi_2_0_gold.pdf>

Relevant records:

- `91h-BFh` remains vendor-specific opcode space;
- `GET FEATURES` / `SET FEATURES` remain the generic feature-access mechanism;
- feature addresses `80h-FFh` remain vendor-specific.

The important standards boundary is therefore negative as well as positive: ONFI provides interoperable command/feature plumbing while leaving a large namespace explicitly vendor-defined.

### S3 — Micron, `ONFI Standards and What They Mean to Designers`, Flash Memory Summit, Aug-2008 (`H/P*`)

- Author: Michael Abraham, Applications Engineering Manager, Micron Technology, Inc.
- Venue/date shown in the deck: Flash Memory Summit, Santa Clara, **August 2008**.
- Original conference-hosted PDF: <https://files.futurememorystorage.com/proceedings/2008/20080813_T1B_Abraham.pdf>
- Searchable preservation mirror: <https://www.yumpu.com/en/document/view/3635151/onfi-standards-and-what-they-mean-to-designers-micron>

The deck's `Get Features (EEh), Set Features (EFh)` slide says these commands were not highly used in ONFI 1.0, were used in ONFI 2.0 for several interface settings, and that vendor-specific feature-address space could handle functions including **OTP**, reducing the need to add more vendor-specific instructions to the command set.

Why `H/P*`: this is manufacturer-authored period presentation material, but the conference PDF is currently served in a way that may reject automated retrieval; the searchable mirror preserves the slide text used here.

### S4 — Micron 2Gb x8/x16 NAND, Rev. A 8/08 (`H/P*`)

- Manufacturer: Micron Technology, Inc.
- Document family: `MT29F2G08AAD`, `MT29F2G16AAD`, `MT29F2G08ABD`, `MT29F2G16ABD`.
- Revision: **Rev. A 8/08 EN**.
- Distributor-hosted manufacturer PDF: <https://media.digikey.com/pdf/Data%20Sheets/Micron%20Technology%20Inc%20PDFs/MT29F2G(08,16)AAD,ABD.pdf>

Relevant records:

- the feature list identifies the part as **ONFI 1.0-compliant**;
- the same product document exposes `GET FEATURES (EEh)` and `SET FEATURES (EFh)`;
- it also still documents the dedicated OTP sequences `A0h-10h`, `A5h-10h`, and `AFh-30h`.

This is a useful coexistence witness: ONFI compliance and vendor-specific OTP command sequences are not mutually exclusive states.

### S5 — Micron 2Gb x8/x16 NAND, Rev. M 4/14 (`H/P*`)

- Manufacturer: Micron Technology, Inc.
- Document: `2Gb: x8, x16 NAND Flash Memory`.
- Revision: **Rev. M 4/14 EN**.
- Preserved manufacturer PDF mirror: <https://www.micros.com.pl/mediaserver/PEF29f2g08abafah4itf_0001.pdf>

Relevant records:

- OTP operation mode is selected by `SET FEATURES (EFh)` at feature address `90h`, writing `01h` to P1;
- while in OTP operation mode, normal `PAGE READ (00h-30h)` and `PROGRAM PAGE (80h-10h)` are redirected to the OTP area;
- OTP protection mode is selected at the same feature address `90h`, writing `03h` to P1, followed by the documented program sequence that establishes protection;
- the document separately includes a **Legacy OTP Commands** note naming `A0h-10h`, `A5h-10h`, and `AFh-30h` and referring readers to an earlier Micron family.

Because ONFI 1.0/2.0 reserve feature addresses `80h-FFh` to vendors, `90h` is inside vendor-specific feature-address space.

---

## Claim-by-claim grounding

### C1 — The legacy Micron OTP opcodes fit ONFI vendor-specific opcode space

**Historical record (`H/P`, `H/P*`):** S1/S2 reserve `91h-BFh` for vendor-specific commands. Case 149's Micron product documents use `A0h`, `A5h`, and `AFh` as the first bytes of dedicated OTP program/protect/read sequences.

**Engineering reconstruction (`E`):** all three bytes fall inside `91h-BFh`.

Therefore:

> **ONFI-compatible command namespace != every operation standardized by ONFI**.

The standards leave room for vendor-defined commands by design.

### C2 — December 2006 ordering remains unresolved

**Historical record (`H/P` / `H/P*`):** S1 has the exact date 28-Dec-2006; the Micron product witness is only `Rev. D 12/06`.

**Stop condition (`X`):** do not write `Micron's 2006 OTP commands predated ONFI 1.0` or the reverse. The current source precision does not support either ordering.

The safe statement is that the records are contemporaneous at month resolution and that ONFI 2.0 is later.

### C3 — ONFI 1.0 already had generic feature access and vendor feature space

**Historical record (`H/P`):** S1 defines `SET FEATURES (EFh)` / `GET FEATURES (EEh)` and makes `80h-FFh` vendor-specific feature-address space.

**Conclusion (`E`):** a standard command transport can carry vendor-defined semantics.

Thus:

> **standardized transport != standardized feature meaning**.

### C4 — Micron's 2008 ONFI presentation names OTP as a vendor-feature use case

**Historical record (`H/P*`):** S3 explicitly lists OTP under uses for vendor-specific feature-address space and says this approach reduces the need for additional vendor-specific command instructions.

This is strong period evidence for an intended interface pattern:

```text
standard SET/GET FEATURES envelope
    + vendor-specific feature address
    -> vendor-defined function without allocating another top-level instruction
```

**Boundary (`X`):** a presentation about an extensibility pattern is not proof that every Micron NAND shipped in August 2008 had already migrated OTP to a feature-address mode.

### C5 — A 2008 Micron ONFI-compliant part still exposes dedicated OTP commands

**Historical record (`H/P*`):** S4 simultaneously says ONFI 1.0-compliant and documents both feature operations and the dedicated `A0h/A5h/AFh` OTP sequences.

Therefore:

> **ONFI compliance != absence of vendor-specific OTP commands**.

This also blocks a simplistic `ONFI arrived -> legacy OTP opcodes disappeared immediately` narrative.

### C6 — By 2014 Micron documents OTP mode selection at vendor feature address 90h

**Historical record (`H/P*`):** S5 uses `SET FEATURES (EFh)` feature address `90h` with P1=`01h` to enter OTP operation mode. Normal page read/program commands are then applied to OTP pages.

**Engineering reconstruction (`E`):** because S1/S2 reserve `80h-FFh` as vendor-specific feature addresses, `90h` is not an ONFI-standard OTP feature assignment in the inspected revisions.

Therefore:

> **ONFI-standard `SET FEATURES` command != ONFI-standard OTP semantics**.

### C7 — Protection keeps the authority transition while command encoding changes

**Historical record (`H/P*`):** S5 uses the same feature address `90h` with P1=`03h` to enter OTP protection mode and then uses the documented program path to establish protection; it continues to describe the protected state as no longer programmable and not unprotectable.

**Engineering reconstruction (`E`):** compared with the older dedicated `A5h-10h` path, the interface encoding changes while the broad authority relation remains recognizable:

```text
program / verify while unprotected
    -> irreversible protection transition
    -> further programming unavailable
    -> read remains available
```

Thus:

> **irreversible OTP authority semantics != command encoding / transport state machine**.

### C8 — `Legacy OTP Commands` is a continuity witness, not full genealogy

**Historical record (`H/P*`):** S5 explicitly labels `A0h-10h`, `A5h-10h`, and `AFh-30h` as `Legacy OTP Commands` and points to an older Micron data-sheet family.

This supports same-vendor vocabulary continuity across documented interfaces.

**Stop condition (`X`):** the label does not prove code reuse, identical internal lock circuitry, identical die lineage, or that the feature-address mode descended directly from the specific 2006 shipped implementation.

### C9 — The standards finding is about namespace allocation, not OTP standardization

The inspected ONFI 1.0/2.0 records standardize:

- command encodings for `SET FEATURES` / `GET FEATURES`;
- the existence of vendor-specific command and feature-address space.

They do **not** assign feature address `90h` the standard meaning `Micron OTP operation/protection`.

Therefore reject:

> `Micron OTP DATA PROTECT became an ONFI-standard command`.

and reject:

> `feature address 90h is an ONFI-standard OTP feature`.

The bounded evidence instead shows vendor semantics carried through an ONFI-defined extension mechanism.

---

## Cross-case controls

### Case 114 — NVMe namespace write protection (`A`)

Both cases show that standardized transport/opcode spaces and a particular mutation-authority policy are separate analytical layers. The protocols, substrates, and authority scopes are otherwise different; no genealogy is implied.

### Case 44 — NVMe sanitize (`A`)

A standards-defined command envelope cannot be treated as evidence for a different semantic contract. Case 44's sanitize semantics aim at forgetting; Case 149's OTP semantics aim at retaining payload while retiring mutation authority.

### Case 78 — NAND bad-block markers (`A`)

Both are raw-NAND examples in which interoperable host/device behavior can coexist with vendor- or device-specific retained control relations. This is a functional comparison only.

---

## Project interpretation

Case 149 now gives a clean example of an interface-level distinction useful across the repository:

> the relation that must persist can remain stable even while the command vocabulary used to reach or establish that relation changes.

For this case, the durable engineering object is the protected/unprotected admissibility relation over OTP payload, not the historical permanence of byte `A5h` as the only way to request it.

This is project interpretation, not Micron or ONFI historical vocabulary.

---

## Counterclaim ledger

| Shortcut | Status | Reason |
| --- | --- | --- |
| “Micron's Dec-2006 OTP commands definitely predate ONFI 1.0” | rejected | Micron source has month precision only; ONFI 1.0 is 28-Dec-2006 |
| “ONFI compliance means no vendor commands” | rejected | ONFI explicitly reserves vendor opcode space; S4 is an ONFI-compliant Micron part with dedicated OTP commands |
| “ONFI standardized OTP DATA PROTECT” | rejected | inspected ONFI revisions classify the relevant legacy opcodes as vendor-specific |
| “ONFI feature address 90h means OTP” | rejected | inspected ONFI revisions reserve 80h-FFh to vendors; 90h meaning comes from Micron product documentation |
| “SET FEATURES is vendor-specific because Micron uses it for OTP” | rejected | EEh/EFh are ONFI-defined feature-access commands; the feature address/meaning can still be vendor-specific |
| “2014 feature-mode sequencing applied to the 2006 part” | rejected | later interface evidence is not back-projected into the earlier product |
| “Legacy label proves identical internal implementation” | rejected | documentary vocabulary continuity is weaker than circuit/code/die genealogy |
| “Command migration changed the physical retention mechanism” | ungrounded | interface documents do not expose enough implementation detail to make that claim |

---

## Related-repository boundary

Fresh searches of `tmzncty/computing-archaeology` for `ONFI`, `OTP DATA PROTECT`, and Micron OTP terms found no dedicated history to reuse.

This bounded record stays here because the central result is retention-specific: **future-mutation authority can remain the same analytical relation while its command encoding changes**.

A broad history of ONFI working-group development, vendor-extension practice, cross-vendor OTP/security-register commands, committee ballot chronology, or controller-driver adaptation belongs primarily in `computing-archaeology`.

---

## What this closes

For Case 149, this record closes the narrow debt `trace when Micron's OTP command vocabulary entered or aligned with ONFI specifications` to the following bounded answer:

- the examined ONFI 1.0/2.0 revisions do **not** standardize Micron's OTP semantics;
- they explicitly provide vendor-specific opcode and feature-address spaces;
- Micron's 2008 standards presentation names OTP as a function suitable for vendor-specific feature-address space;
- a 2008 Micron ONFI-1.0-compliant product still documents the dedicated legacy OTP commands;
- by a 2014 Micron product document, OTP mode/protect selection is encoded through vendor feature address `90h` while `Legacy OTP Commands` remain documented.

This is an interface-alignment chronology, not an invention-priority or internal-implementation genealogy.

---

## Remaining debt

- recover origin-hosted archived copies of the exact 2006 and 2014 Micron product documents where possible;
- identify the earliest Micron shipped family that used feature-address `90h` for OTP, rather than merely the bounded 2014 floor established here;
- trace committee/ballot and cross-vendor history only if needed, preferably in `computing-archaeology`;
- identify exact shipped protection-state circuitry for named parts;
- perform compatible-device tests across protect, reset, power-cycle, and attempted post-protect programming.
''').lstrip()
new_evidence_path.write_text(new_evidence, encoding='utf-8')

# Update the case with navigation, bounded standards chronology, and narrowed debt.
case = case_path.read_text(encoding='utf-8')
assert '149-onfi10-20-vendor-feature-space-otp-interface-deepening.md' not in case
nav_anchor = "Grounding record: [`../evidence/149-micron-2004-2006-nand-otp-data-protect-grounding.md`](../evidence/149-micron-2004-2006-nand-otp-data-protect-grounding.md).\n"
assert nav_anchor in case
case = case.replace(
    nav_anchor,
    nav_anchor + "\nInterface/standards deepening: [`../evidence/149-onfi10-20-vendor-feature-space-otp-interface-deepening.md`](../evidence/149-onfi10-20-vendor-feature-space-otp-interface-deepening.md).\n",
    1,
)
section_anchor = '## Retained state\n'
assert section_anchor in case
section = textwrap.dedent(r'''
## ONFI command-space boundary and later Micron interface migration

The bounded standards history now separates **OTP semantics** from **the command namespace used to reach them**.

ONFI 1.0 (28-Dec-2006) already defines `GET FEATURES (EEh)` / `SET FEATURES (EFh)`, reserves feature addresses `80h-FFh` to vendors, and classifies opcode range `91h-BFh` as vendor-specific. Micron's historical `A0h`, `A5h`, and `AFh` OTP command bytes all fall inside that vendor-specific opcode range. Because the Micron Rev. D product witness is dated only `12/06`, this case does not claim whether it appeared before or after the precisely dated ONFI 1.0 final specification.

ONFI 2.0 (27-Feb-2008) preserves the same important separation: standardized feature-access machinery coexists with vendor-defined command and feature-address space. A Micron Flash Memory Summit presentation from August 2008 then makes the intended use explicit: vendor-specific feature-address space can carry functions such as OTP and thereby reduce the need for additional vendor-specific top-level instructions.

Micron product records show both sides of the transition. A Rev. A 8/08 2Gb part identifies itself as ONFI 1.0-compliant while still documenting the dedicated `A0h/A5h/AFh` OTP sequences. By Rev. M 4/14, a Micron 2Gb data sheet selects OTP operation through `SET FEATURES (EFh)` at vendor feature address `90h` with P1=`01h`, and OTP protection mode at the same feature address with P1=`03h`; ordinary page read/program commands are then used inside that mode. The later document still carries a `Legacy OTP Commands` note naming the earlier `A0h/A5h/AFh` vocabulary.

The safe engineering conclusions are:

> **ONFI-standard command transport != ONFI-standard OTP semantics**

> **irreversible OTP authority semantics != command encoding / transport state machine**

> **ONFI compliance != absence of vendor-specific commands or features**

and

> **later feature-address mode != evidence that the 2006 product used the same mode internally**.

The later `Legacy OTP Commands` label is useful same-vendor documentary continuity, but it does not prove identical firmware, die lineage, lock circuitry, or direct implementation genealogy.

---

''')
case = case.replace(section_anchor, section + section_anchor, 1)
case = case.replace(
    '- the precise standards history by which OTP commands entered later ONFI-era devices;\n',
    '- a full cross-vendor or ballot-level genealogy of ONFI/vendor OTP extension practice beyond the bounded ONFI 1.0/2.0 alignment established here;\n',
    1,
)
case = case.replace(
    '- ONFI OTP command standardization;\n',
    '- broader ONFI/vendor-feature OTP genealogy beyond the bounded 1.0/2.0 interface alignment established here;\n',
    1,
)
old_debt = "- trace when Micron's OTP command vocabulary entered or aligned with ONFI specifications;\n- compare later Micron NAND OTP command revisions without back-projecting them into 2006;\n"
assert old_debt in case
new_debt = "- deepen cross-vendor ONFI/vendor-feature OTP genealogy only if required; the bounded record now establishes that the examined ONFI 1.0/2.0 revisions leave OTP semantics vendor-scoped;\n- identify the earliest Micron shipped family using feature-address `90h` OTP mode and compare additional later families without back-projecting them into 2006;\n"
case = case.replace(old_debt, new_debt, 1)
case_path.write_text(case.rstrip() + '\n', encoding='utf-8')

# Add forward navigation and narrow the stale ONFI debt in the original evidence file.
base = base_evidence_path.read_text(encoding='utf-8')
assert '149-onfi10-20-vendor-feature-space-otp-interface-deepening.md' not in base
purpose_anchor = 'This record separates historical primary claims (`H/P`), mirrored-primary product evidence (`H/P*`), engineering reconstruction (`E`), functional analogy (`A`), and stop conditions/counterclaims (`X`).\n'
assert purpose_anchor in base
base = base.replace(
    purpose_anchor,
    purpose_anchor + "\nFollow-up standards/interface record: [`149-onfi10-20-vendor-feature-space-otp-interface-deepening.md`](149-onfi10-20-vendor-feature-space-otp-interface-deepening.md).\n",
    1,
)
base = base.replace(
    '- trace ONFI OTP command standardization and later Micron command migrations;\n',
    '- use the follow-up standards/interface record for the bounded ONFI 1.0/2.0 vendor-space alignment; broader cross-vendor and earliest-feature-mode genealogy remains open;\n',
    1,
)
base_evidence_path.write_text(base.rstrip() + '\n', encoding='utf-8')

# Update the roadmap's Case 149 line in place.
roadmap = roadmap_path.read_text(encoding='utf-8')
lines = roadmap.splitlines()
matches = [i for i, line in enumerate(lines) if line.startswith('- [x] **Case 149 Micron NAND OTP Data Protect irreversible-authority slice**')]
assert len(matches) == 1, matches
lines[matches[0]] = (
    '- [x] **Case 149 Micron NAND OTP Data Protect irreversible-authority slice + ONFI interface deepening** — '
    '[`cases/149-micron-nand-otp-data-protect-irreversible-authority.md`](cases/149-micron-nand-otp-data-protect-irreversible-authority.md), '
    '[`evidence/149-micron-2004-2006-nand-otp-data-protect-grounding.md`](evidence/149-micron-2004-2006-nand-otp-data-protect-grounding.md), and '
    '[`evidence/149-onfi10-20-vendor-feature-space-otp-interface-deepening.md`](evidence/149-onfi10-20-vendor-feature-space-otp-interface-deepening.md): '
    'the 2006 Micron witness still fixes `unprotected != erasable`, `programmed != protected`, and payload vs future-mutation authority, while ONFI 1.0/2.0 establish that the legacy `A0h/A5h/AFh` bytes occupy vendor-specific opcode space and that `80h-FFh` feature addresses are vendor-specific. Micron\'s Aug-2008 ONFI presentation explicitly names OTP as a vendor-feature-space use, a Rev. A 8/08 ONFI-1.0-compliant product still retains dedicated OTP commands, and a Rev. M 4/14 product uses `SET FEATURES` address `90h` for OTP/protect modes while documenting the old path as `Legacy OTP Commands`. This closes the bounded alignment debt as `standard transport != standardized OTP semantics` and `authority relation != command encoding`; origin-hosted product archives, earliest shipped 90h-mode family, exact circuitry, broad cross-vendor genealogy, and hardware validation remain open.'
)
roadmap_path.write_text('\n'.join(lines).rstrip() + '\n', encoding='utf-8')

# Append findings after verifying the current index tail has not advanced concurrently.
idx = index_path.read_text(encoding='utf-8')
assert '- **3555 — no invention or universal-policy claim:**' in idx
assert '- **3556 —' not in idx
index_section = textwrap.dedent(r'''

## Case 149 — ONFI vendor-space / Micron OTP interface-migration deepening findings

Deepening record: [`evidence/149-onfi10-20-vendor-feature-space-otp-interface-deepening.md`](evidence/149-onfi10-20-vendor-feature-space-otp-interface-deepening.md).

- **3556 — ONFI 1.0 supplies a vendor-opcode boundary:** the 28-Dec-2006 ONFI 1.0 final specification classifies opcode range `91h-BFh` as vendor-specific; Micron's documented legacy OTP bytes `A0h`, `A5h`, and `AFh` all lie inside that range. (`H/P, E`)
- **3557 — December-2006 document ordering remains unresolved:** the Micron product witness is dated only `Rev. D 12/06`, whereas ONFI 1.0 is exactly 28-Dec-2006, so current evidence does not establish which appeared first. (`H/P, X`)
- **3558 — ONFI 1.0 already defines generic feature access:** `GET FEATURES (EEh)` and `SET FEATURES (EFh)` are part of the ONFI 1.0 record, independent of Micron's later OTP use of that mechanism. (`H/P`)
- **3559 — ONFI 1.0 reserves feature addresses `80h-FFh` to vendors:** a standardized feature-access command can therefore carry a vendor-defined feature meaning. (`H/P, E`)
- **3560 — ONFI 2.0 preserves the vendor-space separation:** Revision 2.0 (27-Feb-2008) retains vendor-specific opcode range `91h-BFh` and vendor-specific feature-address range `80h-FFh`. (`H/P`)
- **3561 — Micron's Aug-2008 ONFI presentation explicitly names OTP as a vendor-feature use case:** the deck says vendor-specific feature-address space can handle OTP and reduce the need for additional vendor-specific command instructions. (`H/P*`)
- **3562 — an ONFI-1.0-compliant Micron 2008 part still documents dedicated OTP commands:** the Rev. A 8/08 product record combines ONFI compliance, `GET/SET FEATURES`, and `A0h/A5h/AFh` OTP sequences. (`H/P*`)
- **3563 — ONFI compliance != absence of vendor extensions:** the coexistence record blocks the inference that standards compliance requires every product function to use only ONFI-assigned standard semantics. (`E`)
- **3564 — by Rev. M 4/14 Micron selects OTP operation through feature address `90h`:** `SET FEATURES (EFh)` with P1=`01h` enters OTP operation mode, after which normal page read/program commands act on the OTP area. (`H/P*`)
- **3565 — 2014 Micron protection mode also uses feature address `90h`:** P1=`03h` selects OTP protection mode before the documented program path establishes the irreversible protected relation. (`H/P*`)
- **3566 — `90h` OTP meaning remains vendor-scoped in the inspected ONFI revisions:** because ONFI 1.0/2.0 reserve `80h-FFh` feature addresses to vendors, Micron's use of `90h` is not evidence for an ONFI-standard OTP feature assignment. (`H/P, E, X`)
- **3567 — `Legacy OTP Commands` records same-vendor vocabulary continuity:** the 2014 Micron document explicitly names `A0h-10h`, `A5h-10h`, and `AFh-30h` as legacy OTP commands while documenting the feature-address mode. (`H/P*`)
- **3568 — irreversible authority semantics != command encoding:** Case 149 can retain the distinction `program/verify -> protect -> no further programming while read survives` even when the interface migrates from dedicated OTP opcodes to a mode selected through `SET FEATURES`. (`E`)
- **3569 — standard transport != standardized OTP semantics:** ONFI-standard `SET/GET FEATURES` plumbing does not by itself standardize the vendor meaning attached to feature address `90h`. (`E`)
- **3570 — later mode-gated sequencing is not back-projected into 2006:** the 2014 feature-address state machine does not prove the Rev. D 12/06 device used identical mode selection, control state, firmware, or circuitry. (`X`, rejected upgrade)
- **3571 — interface chronology != invention or implementation genealogy:** `Legacy OTP Commands`, standards namespace alignment, and same-vendor documentation do not prove direct code/die lineage, first invention, or cross-vendor derivation. (`A, X`)
''')
index_path.write_text(idx.rstrip() + index_section + '\n', encoding='utf-8')

# Final local assertions before the workflow's git-level checks.
assert new_evidence_path.exists()
assert '## ONFI command-space boundary and later Micron interface migration' in case_path.read_text(encoding='utf-8')
assert '- **3571 — interface chronology != invention or implementation genealogy:**' in index_path.read_text(encoding='utf-8')
assert 'Case 149 Micron NAND OTP Data Protect irreversible-authority slice + ONFI interface deepening' in roadmap_path.read_text(encoding='utf-8')

# Remove one-shot integration scaffolding from the canonical tree.
script_path.unlink()
workflow_path.unlink()
