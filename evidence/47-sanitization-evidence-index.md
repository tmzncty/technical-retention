# Case 47 evidence index — SSD sanitization verification and verifiable forgetting

**Case:** 47 — FAST ’11 SSD sanitization verification  
**Canonical case:** [`../cases/47-fast11-ssd-sanitization-verification.md`](../cases/47-fast11-ssd-sanitization-verification.md)  
**Current maturity:** `grounded`  
**Purpose:** navigation only; this file does not promote maturity or replace the canonical case.

---

## 1. Scope

Case 47 asks a deliberately evidentiary question:

> after a file disappears, an LBA changes, an erase command reports success, a cryptographic state changes, or a verification interface becomes available, what evidence is sufficient to say that the intended old state can no longer be recovered at the relevant layer?

The case therefore separates at least six claims:

```text
logical disappearance
    !=
command completion
    !=
implementation compliance
    !=
current controller-security state
    !=
controller-mediated post-sanitize verification
    !=
independently verified absence of the targeted old witness
```

The evidence chain currently has four focused files.

---

## 2. Evidence chain A — FAST ’11 raw-flash sanitization verification

### File

- [`47-fast11-2011-ssd-sanitization-grounding.md`](47-fast11-2011-ssd-sanitization-grounding.md)

### Primary source

Michael Wei, Laura Grupp, Frederick E. Spada, and Steven Swanson, **“Reliably Erasing Data From Flash-Based Solid State Drives,”** FAST ’11, February 2011.

### Role

Peer-reviewed empirical grounding for:

- FTL-created `digital remnants`;
- verification below the normal controller interface;
- sanitization-command implementation failures;
- the distinction between whole-device and selective-file forgetting;
- limits of host-visible overwriting on the tested devices;
- the authors’ simulated FTL scrubbing proposals, kept separate from product evidence.

### Strongest bounded result

One anonymized tested SSD reported successful sanitization while all data remained intact and the filesystem remained mountable.

Therefore:

```text
reported erase success
    !=
verified media sanitization
```

### Observation boundary

```text
normal host interface
    -> current controller-visible state

raw NAND extraction
    -> lower-layer digital-remnant witness
```

The FAST ’11 sample is anonymized and does not support named-model conclusions.

---

## 3. Evidence chain B — Samsung 840/850 EVO key-bearing metadata remanence

### File

- [`47-samsung-840-850-crypto-blob-remanence-deepening.md`](47-samsung-840-850-crypto-blob-remanence-deepening.md)

### Primary source

Carlo Meijer and Bernard van Gastel, **“Self-Encrypting Deception: Weaknesses in the Encryption of Solid State Drives,”** IEEE Symposium on Security and Privacy, 2019.

### Role

Named-device deepening for a different forgetting target: **key-bearing controller metadata** rather than stale payload pages.

For the Samsung 840 EVO, the study found that an older unprotected `crypto blob` revision could survive in NAND after the current protection state changed because the internal metadata store was wear-leveled.

The paper reports that the later 850 EVO did not use the same wear-leveled placement mechanism for that blob, providing a bounded negative control for this specific attack path.

### Strongest bounded result

```text
current protection state
    !=
proof that every older key-bearing physical embodiment is gone
```

This was a protection-state / metadata-recovery experiment, **not** a controlled ATA/NVMe sanitize-command failure test.

---

## 4. Evidence chain C — NIST Rev. 1 verification and Cryptographic Erase assurance

### File

- [`47-nist-2014-sanitization-verification-crypto-erase-assurance-deepening.md`](47-nist-2014-sanitization-verification-crypto-erase-assurance-deepening.md)

### Primary source

Richard Kissel, Andrew Regenscheid, Matthew Scholl, and Kevin Stine, **NIST SP 800-88 Rev. 1, Guidelines for Media Sanitization**, December 2014.

### Role

Institutional / operational assurance deepening for:

- implementation trust behind dedicated sanitize commands;
- sanitization-result verification;
- observation-scope limits of native-interface readback;
- Cryptographic Erase verification;
- key hierarchy / lifecycle / escrow / error-handling conditions;
- device/version-specific implementation disclosure.

Rev. 1 is used here historically. NIST withdrew it on 26 September 2025 and superseded it with Rev. 2.

### Strongest bounded result

```text
sanitization command / technique
    !=
implementation assurance
    !=
verification evidence
```

For CE:

```text
current key changed
    !=
complete assurance that every recovery-capable key relation is closed
```

NIST Rev. 1 lists FAST ’11 in Appendix F, establishing a bibliographic connection but not proving a sentence-by-sentence causal lineage.

---

## 5. Evidence chain D — NVMe 2024 Post-Sanitize Media Verification

### File

- [`47-nvme-2024-post-sanitize-media-verification-boundary-deepening.md`](47-nvme-2024-post-sanitize-media-verification-boundary-deepening.md)

### Primary / institutional sources

- NVM Express, **NVM Express NVM Command Set Specification Revision 1.1**, 5 August 2024, incorporating TP4152;
- NVM Express, **Changes in NVM Express Specifications**, August 2024, TP4152 summary;
- UNH-IOL, **Test Plan for NVM Command Set Conformance Version 22.0**, 15 August 2024;
- Open Compute Project, **Datacenter NVMe SSD Specification v2.6**, 2024.

### Role

Standards/conformance deepening for the previously open **verifier-visibility** question.

TP4152 adds a temporary `Media Verification state` after successful sanitize processing. Under the NVM Command Set, special Read semantics expose media-derived post-sanitize data that ordinary integrity behavior might otherwise hide. The controller may return different values on successive reads of the same LBA, explicitly preventing the interface from being treated as a stable raw-media imaging path.

UNH-IOL provides an external protocol-level conformance procedure: write a known pattern, enter Media Verification after Block Erase or Crypto Erase, read the target blocks, and require that the returned pattern not match the pre-sanitize pattern.

OCP v2.6 separately requires TP4152 support for its datacenter profile and reports Sanitize support/conformance information through its Device Capabilities log.

### Strongest bounded result

```text
standardized post-sanitize verification access
    !=
controller-bypassing raw-NAND acquisition
```

and:

```text
feature support
    !=
profile conformance claim
    !=
independent residual-state evidence at every lower layer
```

### Observation boundary

```text
TP4152 Media Verification Read
    -> special controller-mediated media-derived observation
    -> integrity failures may be bypassed for verification
    -> repeated returned values may differ

FAST ’11 raw NAND
    -> controller-bypassing extracted flash observation
```

This closes the standardized-interface portion of verifier-visibility mapping but leaves named-device implementation and same-device raw-NAND comparison open.

---

## 6. Evidence-layer separation

### Historical / product / policy record

The sources directly establish different things:

- **FAST ’11:** empirical raw-flash remnants and anonymized command-compliance failures;
- **Meijer & van Gastel 2019:** named-device stale key-bearing NAND metadata;
- **NIST Rev. 1:** operational guidance on technique selection, implementation assurance, verification, and CE implementation attributes;
- **NVM Express / UNH-IOL / OCP 2024:** a standardized controller-mediated post-sanitize verification state, protocol-level conformance procedures, and datacenter-profile support requirements.

These records should not be collapsed into one chronology of a single mechanism.

### Engineering reconstruction

Repository-level distinctions now include:

```text
current logical value
    !=
stale physical payload embodiment
```

```text
current key/protection state
    !=
stale key-bearing metadata embodiment
```

```text
command status
    !=
native-interface readback evidence
    !=
TP4152 media-verification read evidence
    !=
raw-media residual-state evidence
```

```text
full coverage at one observation layer
    !=
exhaustive coverage of every lower hidden layer
```

```text
verification opportunity available
    !=
verification evidence already collected
```

### Functional comparison

FAST ’11, NIST Rev. 1, and TP4152 are complementary:

```text
FAST ’11
    -> laboratory falsification below ordinary interface

NIST Rev. 1
    -> operational assurance / verification workflow

NVMe TP4152
    -> standardized controller-mediated post-sanitize evidence-access state
```

The comparison is functional. The repository does not infer direct genealogy merely because later standards and guidance address related assurance problems.

### Philosophical interpretation

The bounded project-level statement is:

> a forgetting claim has an observation boundary, an attacker/recovery-effort boundary, and an evidence-access horizon.

That does not imply that sanitization is unknowable. It requires naming what was made unrecoverable, from which layer, and with what evidence.

---

## 7. Cross-case hooks

### Case 44 — NVMe 1.3 Deallocate / Sanitize

```text
Case 44:
Deallocate != Sanitize
Sanitize command completion != sanitize-operation completion

Case 47:
Sanitize semantics
    != implementation compliance
    != post-sanitize verification access
    != independently collected lower-layer residual-state evidence
```

TP4152 is a later development and must not be backdated into NVMe 1.3.

### Case 04 — mapped flash

Case 04 grounds an earlier architecture in which logical currentness can move before old physical embodiment is erased.

Case 47 later shows empirical consequences in SSDs and, with TP4152, a standardized attempt to expose a bounded post-sanitize media-observation path.

This is a functional bridge, not proof that the tested FAST ’11 devices implement the Case-04 historical architecture or TP4152.

### Case 150 — SSD compatibility / command-path admission

Case 150 adds another control boundary:

```text
known safety policy
    !=
correct applicability to this model / firmware / command path
```

Case 47 instead asks whether the selected forgetting path actually produced the intended result and what the verifier could observe.

---

## 8. Current compact model

```text
forgetting requirement
    |
    v
select media-appropriate mechanism
    |
    v
bind mechanism to actual model / version / state
    |
    v
execute
    |
    v
collect completion / error evidence
    |
    v
select observation boundary
    |
    v
verify within that boundary
    |
    v
accept only the forgetting claim supported by that evidence
```

For ordinary overwrite / erase:

```text
accessible-LBA absence
    !=
TP4152 verification-read result
    !=
raw-NAND absence
```

For Cryptographic Erase:

```text
ciphertext may remain
    + recovery-capable key relation becomes unavailable
    -> cryptographic forgetting can succeed
```

but:

```text
new key / current protected state
    !=
proof that all old key paths disappeared
```

For TP4152:

```text
sanitize processing success
    -> temporary verification-readable state
    -> evidence may be collected
    -> exit / post-verification deallocation
```

so:

```text
completed sanitize
    !=
evidence channel
    !=
evidence already collected
```

---

## 9. What this navigation does not claim

- It does not make Case 47 `mature`; status remains `grounded`.
- It does not identify FAST ’11 Drives A–L by consumer model.
- It does not treat all SSD erase failures as one mechanism.
- It does not treat filesystem deletion, TRIM, overwrite, ATA Security Erase, ATA/SCSI/NVMe Sanitize, and Cryptographic Erase as synonyms.
- It does not say native-interface verification is useless.
- It does not say native-interface verification is equivalent to raw-chip analysis.
- It does not claim that NIST Rev. 1 is current guidance.
- It does not claim NIST requires destructive teardown of every SSD.
- It does not turn Appendix D’s CE checklist into a formal proof of key absence.
- It does not claim the Samsung 840 EVO stale-blob experiment was a sanitize-command experiment.
- It does not claim the Samsung 850 EVO is secure against every erase/key-management failure.
- It does not backdate TP4152 into NVMe 1.3.
- It does not claim TP4152 bypasses the controller or exposes raw NAND/OOB data.
- It does not treat an OCP device-reported conformance bit as the underlying independent test record.
- It does not treat the UNH-IOL conformance plan as a published named-device pass result.
- It does not infer implementation genealogy merely from similar assurance problems.

---

## 10. Remaining evidence debt

The most valuable next slices are now concrete:

1. controlled **named-model + firmware** ATA/SCSI/NVMe sanitize experiments with independent residual-state verification;
2. controlled **named Cryptographic Erase** execution followed by search for old keys / key-bearing metadata;
3. firmware-revision comparisons where sanitize behavior changes on the same product family;
4. power-loss / interruption behavior during sanitize and CE on named devices;
5. **same-device verifier-visibility bridge:** ordinary LBA vs TP4152 Media Verification vs reserved/service area vs controller metadata vs raw NAND page/OOB;
6. modern hidden-capacity / remap / over-provisioning experiments after standardized sanitize;
7. named SSD + firmware TP4152 test reports rather than capability-only documentation;
8. a separate Rev. 1 → Rev. 2 policy-history slice only if useful, without retroactively rewriting the 2014 evidence.

The previous generic “map verifier visibility” debt is therefore **partially closed at the standardized-interface / conformance-test level** by Evidence chain D. Lower-layer same-device comparison remains open.

---

## 11. Related-repository boundary

`tmzncty/computing-archaeology` has been searched for `SP 800-88`, `cryptographic erase`, and now `Post Sanitize Media Verification`; no dedicated packet was returned in these rounds.

Broad histories of secure-erase standards, command-set evolution, SSD security marketing, NVMe/OCP qualification, or storage-controller genealogy belong there if developed later.

Case 47 should remain focused on the technical-retention relation:

```text
requested forgetting
    !=
implemented forgetting
    !=
verified forgetting
    !=
which layer the verifier was allowed to observe
```
