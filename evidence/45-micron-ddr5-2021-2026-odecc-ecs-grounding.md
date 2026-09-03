# Case 45 grounding record — Micron DDR5 on-die ECC and Error Check Scrub, 2021–2026

## Status

**Grounding record for Case 45.**

Case: [`../cases/45-micron-ddr5-on-die-ecc-ecs.md`](../cases/45-micron-ddr5-on-die-ecc-ecs.md).

This record grounds a deliberately narrow DDR5 integrity-maintenance bridge. It does **not** claim to replace a direct normative audit of JEDEC JESD79-5, and it does not use vendor exposition as proof that every DDR5 device implements every optional/control behavior identically.

## Research question

The case tests one relation that the earlier DRAM cases leave open:

> When a DDR5 device can correct a single-bit error on an ordinary read and can also perform Error Check and Scrub that writes corrected state back into the array, are `successful read`, `stored-state repair`, `ordinary refresh`, and `error reporting` actually the same retention event?

The bounded evidence says **no**.

## Evidence set and role separation

### E1 — Micron 2023 commercial-platform article

**Source:** Micron Technology, “Redefining performance With DDR5 and 4th Gen Intel Xeon scalable processors,” 2023.

URL: <https://www.micron.com/about/blog/company/partners/redefining-performance-with-ddr5-and-4th-gen-intel-xeon-scalable>

**Role:** manufacturer-primary description of commercial Micron DDR5 capability in a named 4th-generation Intel Xeon platform context.

The `Improved reliability` section lists three capabilities separately:

- on-die ECC (`ODECC`);
- Error Check and Scrub (`ECS`);
- Same Bank Refresh.

It then describes the on-die ECC path as generating/storing an ECC code for protected write data and evaluating data plus code during read so a single-bit error can be corrected before the data is sent toward the host.

It describes ECS as an additional feature that can operate manually or automatically within a recommended 24-hour period and can report the number of corrected errors after the scrub completes.

**Claims grounded:**

- commercial manufacturer use of the terms ODECC, ECS, Same Bank Refresh;
- 128-data-bit + 8-code-bit manufacturer explanation;
- single-bit read correction;
- manual/automatic ECS;
- recommended 24-hour ECS period;
- corrected-error count reporting;
- ODECC framed as complementary to wider server RAS rather than a substitute for it.

**Claims not grounded by E1:**

- exact JEDEC mode-register encodings;
- exact automatic-ECS command sequence;
- exact row/segment counter semantics;
- every device/vendor's implementation;
- end-to-end server error coverage;
- invention priority for ECC or scrub.

### E2 — Micron DDR5 product page

**Source:** Micron Technology, DDR5 DRAM product page and DDR4/DDR5 comparison table.

URL: <https://www.micron.com/products/memory/dram-components/ddr5-sdram>

**Role:** independent manufacturer product-family cross-check that on-die ECC/ECS and refresh are separately represented DDR5 features.

The page lists:

- `On-die ECC`: `128b+8b SEC, error check and scrub`;
- `REFRESH commands`: all-bank and same-bank capability, with `REFsb` described separately.

This is especially important for the case's mechanism boundary. It prevents the project from treating ECS as merely a new label for refresh just because both can result in internal rewriting of DRAM state.

**Claims grounded:**

- Micron presents on-die ECC/ECS as a DDR5 RAS capability;
- Micron separately presents refresh geometry/capability;
- ECS and REFsb occupy different feature rows in the manufacturer comparison.

**Claims not grounded by E2:**

- detailed ECS scheduling policy;
- full normative specification language;
- field failure-rate effects.

### E3 — Linux 6.15 EDAC `Scrub Control` documentation

**Source:** Linux Kernel documentation, “Scrub Control,” written for Linux 6.15, copyright 2024–2025 HiSilicon Limited.

URL: <https://docs.kernel.org/6.15/edac/scrub.html>

Current version: <https://docs.kernel.org/edac/scrub.html>

**Role:** later system-software and host-control boundary, not a substitute for Micron product history.

The document defines memory scrubbing generally as an ECC engine reading memory locations, correcting as necessary, and writing corrected data back. Its `Error Check Scrub (ECS)` section identifies ECS as a DDR5 feature defined in JESD79-5 and describes DRAM-internal read, single-bit correction, corrected-data writeback, and error-count transparency.

The current control discussion also shows a later composition in which CXL ECS control can expose selected attributes — including error-count behavior, thresholds, and counter reset — to host/userspace RAS management, and places some responsibility for initiating ECS with the memory controller/platform in response to elevated error rates.

**Claims grounded:**

- read/correct/writeback is an explicit scrub relation, not merely a project inference;
- error-count information can cross the device boundary;
- later software stacks can retain external policy authority around a device-internal scrub mechanism.

**Scope warning:** this source is later than the 2023 Micron article and is a Linux/CXL control composition. It is **not** used to claim that every 2023 Micron DDR5 platform exposed the same sysfs controls or that CXL control semantics are identical to the underlying DDR5 device interface.

### E4 — Nguyen et al. 2021, OBET

**Source:** Duy-Thanh Nguyen et al., “OBET: On-the-Fly Byte-Level Error Tracking for Correcting and Detecting Faults in Unreliable DRAM Systems,” *Sensors* 21(24), 8271, 2021, DOI `10.3390/s21248271`.

URL: <https://pmc.ncbi.nlm.nih.gov/articles/PMC8708231/>

**Role:** independent peer-reviewed technical qualification and terminology cross-check.

Section 2.5, `DDR5 ECC Transparency and Scrubbing`, describes DDR5 ECS as a mechanism intended to prevent error accumulation. In its mechanism account, on-die ECC reads/checks the codeword; a single-bit error is corrected; the corrected codeword is then written back to the DRAM cells. The paper discusses automatic/manual ECS modes and emphasizes the overhead of scanning the full array.

**Claims grounded:**

- scholarly recognition of ECS as a distinct corrective writeback mechanism;
- error-accumulation motivation;
- full-array scanning has performance/power cost;
- automatic/manual mode distinction is not unique to Micron marketing language.

**Scope warning:** OBET is a research paper proposing a different selective-scrubbing design. Its stronger normative statements and detailed command-sequence interpretation are not imported into the case as if directly verified from JESD79-5.

## Directly grounded mechanism decomposition

### A. Ordinary DRAM refresh

Already grounded elsewhere in this repository:

- Case 03 — periodic restoration of decaying dynamic state;
- Case 21 — AUTO REFRESH / SELF REFRESH responsibility handoff;
- Case 33 — DDR5 Same Bank Refresh target/interference geometry;
- Cases 34–35 — temperature-conditioned cadence and commercial automatic TCSR/PASR distinctions.

Case 45 does not re-prove that history. It uses Micron's separate `REFRESH commands` and ECS listings to show that the commercial DDR5 product family composes refresh with an additional ECC-scrub relation.

### B. ODECC read correction

From Micron E1/E2:

```text
stored data + on-die ECC code
    -> READ evaluation
    -> correctable single-bit error repaired for the read result
    -> correct logical value can leave the DRAM
```

This directly supports:

> `raw stored error ≠ immediate logical read failure`.

It does **not** by itself establish that the corrected codeword has been rewritten into the array after every ordinary read. The case intentionally refuses to infer stored-state repair from correct output alone.

### C. ECS stored-state repair

From Linux E3 plus Nguyen et al. E4:

```text
internal read
    -> ECC check
    -> single-bit correction
    -> corrected-data writeback to DRAM array
```

This supports the central distinction:

> `read-path correction ≠ stored-array repair`.

The distinction is evidence-driven rather than linguistic: one path is sufficient to return a correct value; the documented scrub path explicitly includes writeback.

### D. ECS telemetry

From Micron E1 and Linux E3:

- scrub correction counts can be reported;
- later host control can expose/manipulate selected count/threshold/reset policy.

This supports:

> `payload availability ≠ error observability`.

and the project reconstruction:

> correction telemetry can be **second-order retention state** — retained information about the condition/maintenance of first-order payload state.

The phrase `second-order retention state` is not Micron or JEDEC vocabulary.

## Counterexamples established by the evidence

### Counterexample 1 — “If the read is correct, the stored cells are healthy.”

Rejected.

ODECC exists precisely because a correct logical result can be reconstructed from a raw state containing a correctable error. ECS additionally repairs and records correction activity.

### Counterexample 2 — “ECC correction and scrubbing are the same operation.”

Rejected.

The bounded sources permit a successful ordinary read correction while separately defining a scrub operation that reads/checks/corrects and writes back array state.

### Counterexample 3 — “All background DRAM maintenance is refresh.”

Rejected.

Micron lists ODECC/ECS and Same Bank Refresh separately; ECS has an error-correction/writeback objective, while the grounded refresh cases establish charge-restoration deadlines and refresh target geometry.

### Counterexample 4 — “Device-internal automation eliminates external maintenance policy.”

Rejected.

Micron preserves manual and automatic ECS. Linux's later control model exposes count/threshold/reset policy and permits controller/platform participation in initiation. Authority can migrate across layers without the maintenance obligation disappearing.

### Counterexample 5 — “On-die ECC means the whole memory system is ECC-protected end to end.”

Rejected.

Micron calls ODECC complementary to wider server RAS. Its product material also lists other mechanisms such as read/write CRC separately. The device-local code is one protection domain, not proof about all paths above or outside it.

### Counterexample 6 — “DDR5 ECS is AVATAR made commercial.”

Rejected.

AVATAR's bounded mechanism changes a row's future refresh class after ECC/scrub observations. The inspected DDR5 ECS evidence establishes correction, writeback, and reporting; it does not establish AVATAR-style row refresh reclassification. Functional similarity in `observe errors and perform maintenance` is not historical identity or implementation genealogy.

## Historical record / reconstruction / analogy / interpretation boundary

### Historical record

Supported terms and facts include:

- Micron DDR5 `ODECC`, `ECS`, and `Same Bank Refresh`;
- Micron's 128b+8b SEC description;
- read-time single-bit correction;
- manual/automatic ECS and recommended 24-hour scrub period in Micron's public exposition;
- corrected-error count reporting;
- Linux's later DDR5 ECS read/correct/writeback and host-control documentation.

### Engineering reconstruction

Project-level relations include:

- `read-path correction ≠ stored-array repair`;
- `ECS scrub ≠ DRAM refresh`;
- `refresh deadline ≠ scrub coverage interval`;
- `payload availability ≠ error observability`;
- correction telemetry as second-order retention state;
- automatic maintenance does not erase external policy authority.

### Functional analogy

ECS can be compared to preventive maintenance that repairs a correctable defect before another fault exhausts the correction margin. This is a relation-level analogy only.

### Philosophical interpretation

The mechanism supports a narrow conceptual result:

> apparent continuity of a logical value can conceal multiple physically and operationally different states — uncorrected, corrected for access, repaired in storage, and accompanied by retained evidence of repair.

It does not establish human memory, diagnosis, archive, or self-knowledge inside the DRAM.

## Prior-art boundary

No priority claim is made for:

- error-correcting codes;
- memory scrubbing;
- DRAM refresh;
- server RAS;
- maintenance telemetry.

The bounded novelty for this repository is not historical invention. It is the comparative relation supplied by a commercial DDR5 device generation:

```text
short-timescale charge refresh
    + read-path ODECC
    + longer-coverage ECS corrective writeback
    + correction telemetry
    + separately movable host/device policy authority
```

The relevant broader history should be developed in `tmzncty/computing-archaeology` if needed.

## Related-repository duplication check

Before writing the case, `tmzncty/computing-archaeology` was searched for:

- `DDR5`;
- `ECS`;
- `DDR5 ECS Error Check Scrub on-die ECC`.

No dedicated match was found. The present case therefore does not duplicate an existing technical-history case. If later work reconstructs the detailed ECC genealogy, DDR5 mode-register chronology, or semiconductor scaling rationale, that engineering history should be routed to the companion repository and linked back here.

## Evidence maturity assessment

**Why `grounded` is justified:**

1. two Micron manufacturer pages independently establish the commercial feature composition;
2. the Linux kernel documentation independently specifies the read/correct/writeback relation and later control surface;
3. a peer-reviewed 2021 paper independently describes DDR5 ECS and its corrective writeback / scan-overhead role;
4. the case avoids claims that require uninspected normative mode-register text;
5. the central comparison relies on distinctions directly visible in the sources, not on speculative circuit details;
6. related-repository duplication was checked;
7. invention-priority and commercial-universality claims are explicitly rejected.

**What remains open:**

- direct, revision-by-revision JESD79-5 normative ECS audit;
- exact manual/automatic ECS mode-register, segment, threshold, and counter semantics from directly inspected standard text;
- product-to-product differences across Micron and other vendors;
- independent fault-injection/field validation of ECS behavior;
- system-level composition of on-die ECC with ECC DIMMs, memory-controller ECC, CXL RAS, PPR, sparing, and OS page retirement;
- whether and how later production systems use ECS telemetry to change refresh, repair, retirement, or sparing policy;
- RowHammer-oriented refresh/repair interaction.

These are later cases, not hidden promotion blockers for this bounded commercial-device integrity-maintenance bridge.
