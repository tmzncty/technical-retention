# Case 47 evidence index — SSD sanitization verification and verifiable forgetting

**Case:** 47 — FAST ’11 SSD sanitization verification  
**Canonical case:** [`../cases/47-fast11-ssd-sanitization-verification.md`](../cases/47-fast11-ssd-sanitization-verification.md)  
**Current maturity:** `grounded`  
**Purpose:** navigation only; this file does not promote maturity or replace the canonical case.

---

## 1. Scope

Case 47 asks a deliberately evidentiary question:

> after a file disappears, an LBA changes, an erase command reports success, or a cryptographic state changes, what evidence is sufficient to say that the intended old state can no longer be recovered at the relevant layer?

The case therefore separates at least five claims:

```text
logical disappearance
    !=
command completion
    !=
implementation compliance
    !=
current controller-security state
    !=
independently verified absence of the targeted old witness
```

The evidence chain currently has three focused files.

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

## 5. Evidence-layer separation

### Historical / product / policy record

The sources directly establish different things:

- **FAST ’11:** empirical raw-flash remnants and anonymized command-compliance failures;
- **Meijer & van Gastel 2019:** named-device stale key-bearing NAND metadata;
- **NIST Rev. 1:** operational guidance on technique selection, implementation assurance, verification, and CE implementation attributes.

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
raw-media residual-state evidence
```

```text
full coverage at one observation layer
    !=
exhaustive coverage of every lower hidden layer
```

### Functional comparison

FAST ’11 and NIST Rev. 1 are complementary:

```text
FAST ’11
    -> laboratory falsification below ordinary interface

NIST Rev. 1
    -> operational assurance / verification workflow
```

The comparison is functional even though Rev. 1 cites FAST ’11 in its bibliography. The repository does not infer that each NIST recommendation was directly derived from that paper.

### Philosophical interpretation

The bounded project-level statement is:

> a forgetting claim has an observation boundary and an attacker/recovery-effort boundary.

That does not imply that sanitization is unknowable. It requires naming what was made unrecoverable, from which layer, and with what evidence.

---

## 6. Cross-case hooks

### Case 44 — NVMe 1.3 Deallocate / Sanitize

```text
Case 44:
Deallocate != Sanitize

Case 47:
Sanitize semantics != implementation compliance != verification evidence
```

### Case 04 — mapped flash

Case 04 grounds an earlier architecture in which logical currentness can move before old physical embodiment is erased.

Case 47 later shows empirical consequences in SSDs.

This is a functional bridge, not proof that the tested FAST ’11 devices implement the Case-04 historical architecture.

### Case 150 — SSD compatibility / command-path admission

Case 150 adds another control boundary:

```text
known safety policy
    !=
correct applicability to this model / firmware / command path
```

Case 47 instead asks whether the selected forgetting path actually produced the intended result.

---

## 7. Current compact model

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
verify within a named observation boundary
    |
    v
accept only the forgetting claim supported by that evidence
```

For ordinary overwrite / erase:

```text
accessible-LBA absence
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

---

## 8. What this navigation does not claim

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
- It does not infer implementation genealogy merely from similar assurance problems.

---

## 9. Remaining evidence debt

The most valuable next slices are now concrete:

1. controlled **named-model + firmware** ATA/SCSI/NVMe sanitize experiments with independent residual-state verification;
2. controlled **named Cryptographic Erase** execution followed by search for old keys / key-bearing metadata;
3. firmware-revision comparisons where sanitize behavior changes on the same product family;
4. power-loss / interruption behavior during sanitize and CE;
5. explicit mapping of verifier visibility: host LBA vs reserved/service area vs controller metadata vs raw NAND page/OOB;
6. modern hidden-capacity / remap / over-provisioning experiments after standardized sanitize;
7. a separate Rev. 1 → Rev. 2 policy-history slice only if useful, without retroactively rewriting this 2014 evidence.

---

## 10. Related-repository boundary

`tmzncty/computing-archaeology` was searched for `SP 800-88` and `cryptographic erase`; no dedicated packet was found in this round.

Broad histories of secure-erase standards, command-set evolution, SSD security marketing, or storage-controller genealogy belong there if developed later.

Case 47 should remain focused on the technical-retention relation:

```text
requested forgetting
    !=
implemented forgetting
    !=
verified forgetting
```
