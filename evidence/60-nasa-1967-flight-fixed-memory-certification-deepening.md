# Case 60 Evidence Deepening — NASA 1967 Flight Fixed-Memory Certification

**Status:** `bounded deepening complete`

## Scope

This evidence slice deepens [`../cases/60-apollo-core-rope-wired-topology.md`](../cases/60-apollo-core-rope-wired-topology.md) at one deliberately narrow boundary:

> once an Apollo fixed-memory program had been approved, how did NASA distinguish the approved software configuration from the manufactured fixed-memory artifact that was actually to fly?

The principal source is the NASA Manned Spacecraft Center **_Apollo Guidance Software Development and Verification Plan_**, dated **October 4, 1967**, prepared by the Guidance Software Validation Committee for the Guidance Software Control Panel. The report is a software-development and verification plan, not a rope-manufacturing specification. It is valuable here because it explicitly connects software approval, hard-memory fabrication, manufactured fixed-memory comparison, acceptance, certification, and configuration control.

A related NASA design-criteria report, **NASA SP-8070, _Spaceborne Digital Computer Systems_ (March 1971)**, is used only as a bounded lifecycle cross-check. It says Apollo core-rope program changes required about a four-week production cycle and notes that verification cycles were at least as long as production cycles. That statement helps bound revision latency; it does not specify the detailed 1967 acceptance procedure.

`tmzncty/computing-archaeology` was searched again for `Apollo core rope verification`; no dedicated reusable treatment was found. This file therefore records only the retention-specific evidence and does not recreate a general Apollo software-engineering history.

---

## Source identity and date boundary

The facsimile title page identifies:

- **NASA Manned Spacecraft Center, Houston, Texas 77058**;
- **October 4, 1967**;
- **_Apollo Guidance Software — Development and Verification Plan_**;
- prepared by **The Guidance Software Validation Committee**;
- for **The Guidance Software Control Panel**.

The report defines `software` as the computer contents normally called the computer program. It separately defines contractor `qualification` and independent `verification` against specifications. That vocabulary matters because the report does not treat a manufactured memory artifact as self-authenticating merely because its bits are physically fixed.

Primary facsimile / transcription:

- https://www.ibiblio.org/apollo/hrst/archive/1695.pdf
- NASA Office of Logic Design index/transcription: https://klabs.org/history/history_docs/mit_docs/sw.htm

---

## Historical record

### 1. Accepted software is released *into* fabrication, not equated with fabrication

The report's summary states that after satisfactory qualification and review at the Customer Acceptance Readiness Review (`CARR`), accepted software is released for:

1. **hard-memory fabrication**;
2. **verification**;
3. **system testing at KSC**.

The sequence matters. Approval of the software configuration precedes and authorizes fabrication; it does not make the resulting physical memory automatically equivalent to the approved program.

The same section says subsequent flights with fixed-memory changes repeat the cycle, with testing reduced according to the magnitude of the change. If a previous flight's fixed memory is approved for reuse at the Critical Design Review, a reduced cycle is possible.

Historical boundary:

```text
software accepted for manufacture
!=
manufactured fixed memory already accepted for flight
```

This is a direct reading of the process distinction in the 1967 plan.

### 2. The manufactured fixed memory is required to match the approved program bit for bit

Section **5.5, `Flight Fixed and Erasable Memory Verification`**, says software verification leads to verification of flight fixed memory so that the fixed memory can be manufactured, and separately includes certification of the manufactured flight fixed memory.

Section **5.5.1, `Flight Fixed Memory Certification`**, is the key passage. Once the flight fixed-memory contents are approved, procedures are to ensure that the approved program delivered by the software contractor is **identical, bit for bit, to the manufactured flight fixed memory**.

The same subsection requires:

- formal **acceptance and certification** of the flight fixed memory by MSC;
- at acceptance test, comparison of the manufactured fixed-memory contents with the **MSC-approved configuration** of the fixed-memory software.

This directly establishes that Apollo's fixed-memory retention chain included an explicit equivalence check between two differently embodied states:

```text
approved software configuration
          ↓
manufacturing process
          ↓
manufactured fixed-memory artifact
          ↓
comparison / acceptance
          ↓
certified flight fixed memory
```

The first and third nodes are not presumed identical merely because the third is physically read-only in normal operation.

### 3. Figure 5-1 exposes two paths into acceptance

The report's Figure **5-1, `Flight Fixed Memory Generation + Verification`**, depicts a production path from the approved program toward the manufacturer, `weavers tape`, rope fabrication, rope check, rope acceptance test, and KSC. It also depicts a `check tape` path feeding the rope acceptance test.

For this repository the safe conclusion is modest:

> the 1967 plan represented fixed-memory production and verification as a chain with an independently represented checking input at acceptance, rather than as one undifferentiated act of manufacture.

The figure does **not** by itself establish the detailed electrical test method, the exact independence of personnel or equipment, or the algorithm by which the comparison was performed.

### 4. Configuration control survives beyond the software source listing

Section **7.1.1, `Software Approval Procedures`**, says the Software Design Specification and program listing are under configuration control during qualification and verification. It further says that, after the First Article Configuration Inspection (`FACI`), **any change to the configuration-controlled program must be approved by the Guidance Software Control Panel, including changes to any memory cell**.

This is an important authority boundary.

A core-rope bit is physically embodied in manufactured topology, but whether a different bit pattern is the approved flight configuration is governed by configuration-control procedure rather than by physical readability alone.

Thus:

```text
physical ability to manufacture a different topology
!=
authority to alter the approved flight configuration
```

and:

```text
artifact contains a readable program
!=
artifact is the currently authorized flight program
```

### 5. NASA SP-8070 separates production latency from verification latency

NASA SP-8070 (March 1971) describes Apollo core-rope program memory as a fixed-memory example whose program changes required about a **four-week production cycle** for new modules. It adds that **verification cycles were at least as long as production cycles**.

That observation should not be collapsed into one generic `rope manufacturing time`.

For this case it supports:

```text
fabrication latency
!=
verification latency
!=
total revision-to-flight latency
```

The source does not provide one universal elapsed-time formula for every Apollo rope revision or mission.

---

## Engineering reconstruction

The following terms are modern analytical language, not claimed as NASA/MIT period vocabulary.

### Finding 1 — manufactured persistence still needs an identity relation

Case 60 already establishes that program bits can persist in wire/core topology rather than remanent magnetic polarity. The 1967 verification plan adds another retained relation:

> the flight artifact must remain demonstrably the embodiment of the *approved* program configuration.

Physical topology alone answers `what pattern is in this module?` It does not, by itself, answer `is this the pattern that the authorized software configuration says should fly?`

The retention chain therefore includes both:

```text
payload embodiment
+
configuration identity / authority relation
```

### Finding 2 — fabrication is a state transition that requires validation

The mapping from approved program to manufactured topology is not treated as logically transparent.

It crosses representations:

```text
approved program state
→ manufacturing/control media
→ wire-routing work
→ physical rope
```

The NASA requirement for bit-for-bit comparison means the transition itself creates a verification obligation.

So:

```text
representation change
→ possible divergence surface
→ comparison obligation
```

This is not a claim that Apollo engineers used the phrase `representation change`.

### Finding 3 — fixedness moves some retention work outside runtime

The rope's runtime interface prevents ordinary program instructions from rewriting fixed memory. But the 1967 plan shows substantial work is still necessary to preserve *correct program identity* across the lifecycle:

- configuration approval;
- controlled release to manufacture;
- fabrication;
- rope checking;
- acceptance comparison;
- certification;
- later change control.

Thus:

```text
little/no runtime rewrite authority
!=
little/no retention work
```

The work has moved toward production, verification, and configuration governance.

### Finding 4 — read-only and trusted are different predicates

A wrongly manufactured rope could still be read-only during operation. Its inability to be rewritten would not make its contents correct.

Therefore:

```text
runtime read-only
!=
bitwise correspondence to approved software
!=
flight acceptance
```

The first is an interface/property claim. The second is an equivalence claim. The third is an authority/certification claim.

### Finding 5 — supersession can revoke currentness without erasing the old artifact

The configuration-control procedure also sharpens Case 60's existing distinction between physical persistence and current program identity.

A previous rope can retain a complete, readable program while a later approved configuration becomes authoritative for another flight. Reuse is itself an approval decision in the 1967 plan.

Thus:

```text
old artifact still readable
!=
old artifact still current for this mission
```

No physical erase is required for currentness to change.

---

## Functional comparisons — bounded

### Mask ROM / programmed immutable artifacts

There is a limited functional comparison to later manufactured ROM images: a fixed physical payload may still require a release artifact, manufacturing transfer, readback/checking, and configuration identity.

This file does **not** claim Apollo rope directly caused later semiconductor ROM verification practices.

### Firmware image verification

Modern firmware systems often distinguish a build artifact, programmed device contents, cryptographic or bytewise verification, and deployment authorization. The abstract relation is useful:

```text
source/build identity
!=
programmed-device identity
!=
deployment authority
```

But Apollo's 1967 process is not retroactively described as secure boot, code signing, reproducible builds, or a cryptographic supply chain.

### Case 62 — IBM TROS

Case 62 also studies transformer/read-only memory in which the retained control information is embodied in manufactured routing rather than a magnetic bit state. The comparison is functional only: runtime read-only topology still leaves manufacturing and replacement as lifecycle update mechanisms.

This evidence slice does not establish a NASA↔IBM technical genealogy.

---

## Philosophical / media-theoretical interpretation — bounded

One project-level interpretation is justified:

> when information is made physically stable by manufacturing it into an artifact, the problem of retention can shift from `keep this material state from decaying` toward `keep this artifact demonstrably identical to the authorized configuration`.

The 1967 report is evidence for the engineering procedure, not for this philosophical vocabulary.

A fixed artifact therefore does not abolish mediation. It multiplies representations — approved program, manufacturing media, woven topology, acceptance reference, installed flight unit — and the institution must maintain correspondence among them.

That is a useful technical-retention result only so long as it remains subordinate to the documented process.

---

## Explicit non-claims

This slice does **not** claim that:

1. the 1967 verification plan is a detailed Raytheon rope-manufacturing specification;
2. every Apollo mission followed every diagrammed step without exception or local procedural change;
3. `bit for bit` comparison specifies the exact electrical reader, test fixture, algorithm, or staffing arrangement used at every acceptance test;
4. the `check tape` shown in Figure 5-1 proves organizational independence, cryptographic independence, or a modern two-person control scheme;
5. acceptance testing proved the absence of all latent hardware faults;
6. bitwise equality to the approved program proved that the program's requirements or algorithms were themselves correct;
7. configuration-control approval physically prevented an unauthorized person from manufacturing a different rope;
8. reuse approval meant the old physical module had been electrically or mechanically modified;
9. a superseded rope ceased to retain its old program;
10. the four-week production figure in NASA SP-8070 was a universal Raytheon manufacturing constant;
11. `verification cycles were at least as long as production cycles` means both cycles always had exactly the same duration;
12. the 1967 report settles the invention priority of core-rope or wired-in memory;
13. the Apollo process is historically identical to modern firmware signing, reproducible builds, ROM checksums, or secure boot;
14. this evidence proves a direct technical genealogy from Apollo configuration control to later software/firmware configuration-management practice.

---

## Claim ledger

| Claim | Type | Evidence status |
| --- | --- | --- |
| NASA's October 4, 1967 plan separately treats software approval, hard-memory fabrication, verification, and KSC system testing | H/P | direct in NASA plan summary |
| The manufactured flight fixed memory was required to be identical bit for bit to the approved program | H/P | direct in §5.5.1 |
| MSC was to formally accept/certify the flight fixed memory and compare its contents with the MSC-approved software configuration | H/P | direct in §5.5.1 |
| Figure 5-1 represents rope fabrication/checking and a separately drawn check-tape path into acceptance testing | H/P | direct in NASA figure; bounded to represented process |
| After FACI, configuration-controlled program changes, including any memory-cell change, required GSCP approval | H/P | direct in §7.1.1 |
| A prior flight's fixed memory could be approved for a subsequent flight under a reduced process | H/P | direct in plan summary |
| NASA SP-8070 says Apollo rope program changes involved about a four-week production cycle and verification cycles at least as long | H/P | direct in NASA SP-8070 §2.2.2 |
| Manufactured topology is not self-authenticating as the approved flight configuration | E | reconstruction from mandatory comparison/certification |
| Runtime read-only status, bitwise correspondence, and flight acceptance are distinct predicates | E | reconstruction from fixed-memory semantics + 1967 acceptance process |
| Fixedness moves part of retention labor into fabrication/verification/configuration control | E | reconstruction from cross-lifecycle evidence |
| A readable old rope may persist after losing mission currentness | E | reconstruction from reuse/change-control structure; no erase implied |
| Apollo rope certification was equivalent to modern secure boot or cryptographic code signing | X | unsupported and rejected |
| The 1967 plan proves every manufactured rope was fault-free | X | unsupported and rejected |

---

## Navigation consequence

This slice closes one of Case 60's previously open directions: **mission-specific rope production/configuration records** now have a direct 1967 NASA process witness at the plan/certification level.

Remaining work is narrower:

- a directly renderable facsimile of Hayden A. Nelson's December 1964 `A Wired Core Memory for Airborne Computers` article;
- pre-Apollo wired-in / Dimond-ring / transformer-ROM genealogy if a future priority argument needs it;
- mission- or program-specific rope anomaly, acceptance-test, rework, and configuration-change records that show the general 1967 procedure in concrete incidents;
- physical or simulated rope-reader experiments if they clarify topology-versus-magnetization semantics.

---

## Sources

1. **NASA Manned Spacecraft Center, Guidance Software Validation Committee, _Apollo Guidance Software — Development and Verification Plan_, October 4, 1967.** Especially summary pp. 2-1–2-2, §5.5 / §5.5.1 `Flight Fixed Memory Certification`, Fig. 5-1 `Flight Fixed Memory Generation + Verification`, and §7.1.1 `Software Approval Procedures`. Facsimile: https://www.ibiblio.org/apollo/hrst/archive/1695.pdf . NASA Office of Logic Design document index/transcription: https://klabs.org/history/history_docs/mit_docs/sw.htm
2. **NASA, _Spaceborne Digital Computer Systems — Space Vehicle Design Criteria_, NASA SP-8070, March 1971, §2.2.2 `Memory`.** NTRS PDF: https://ntrs.nasa.gov/api/citations/19710024203/downloads/19710024203.pdf
3. **Case 60 canonical record and its existing MIT/NASA sources.** [`../cases/60-apollo-core-rope-wired-topology.md`](../cases/60-apollo-core-rope-wired-topology.md)

---

## Evidence status

**`bounded deepening complete`.**

The 1967 NASA source directly establishes an approval→fabrication→comparison→acceptance/certification chain for flight fixed memory and configuration-control authority over later memory-cell changes. It does not supply detailed factory process parameters or a mission-specific anomaly history, so those remain explicitly outside this slice.