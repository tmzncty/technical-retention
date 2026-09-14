# Case 47 deepening — Samsung 840/850 EVO crypto-blob remanence and key-store verification

**Status:** bounded deepening complete  
**Canonical case:** [`../cases/47-fast11-ssd-sanitization-verification.md`](../cases/47-fast11-ssd-sanitization-verification.md)  
**Primary period studied:** 2013–2019 product/analysis window  
**Research slice:** named-device evidence for cryptographic forgetting when obsolete key-bearing metadata can survive below the current controller-visible protection state

## Why this slice

Case 47 already has strong 2011 empirical evidence that stale **payload** embodiments can survive below an SSD's current host-visible mapping. Its open evidence debt, however, also asks for:

- named-product / named-controller verification evidence;
- cryptographic-erase verification, especially key-store scope and recoverability.

Meijer and van Gastel's 2019 IEEE Security & Privacy paper provides a bounded named-device witness for a closely related but technically distinct failure surface: the Samsung 840 EVO could retain an older, unprotected revision of key-bearing controller metadata because the internal `crypto blob` itself was wear-leveled.

This does **not** prove that an ATA or NVMe sanitize command on the 840 EVO failed. The demonstrated transition is password/protection-state reconfiguration, not a controlled post-sanitize experiment. The value of the evidence is narrower: it shows why cryptographic forgetting cannot be verified only by checking the controller's current key/protection state.

## Source set and evidence class

Primary technical source:

- Carlo Meijer and Bernard van Gastel, **“Self-Encrypting Deception: Weaknesses in the Encryption of Solid State Drives,”** *2019 IEEE Symposium on Security and Privacy*, pp. 72–87, DOI `10.1109/SP.2019.00088`. Author-hosted paper: <https://www.cs.ru.nl/~cmeijer/publications/Self_Encrypting_Deception_Weaknesses_in_the_Encryption_of_Solid_State_Drives.pdf>

Bibliographic cross-check:

- Open Universiteit research portal record, peer-reviewed conference article, published 19 May 2019: <https://research.ou.nl/en/publications/self-encrypting-deception-weaknesses-in-the-encryption-of-solid-s/>

Evidence labels in this file:

- **H/P** — historical/product record directly reported by the 2019 reverse-engineering study;
- **E** — engineering reconstruction from those observations;
- **F** — bounded functional comparison to another repository case;
- **I** — philosophical/project-level interpretation;
- **X** — explicit non-claim.

The 2019 paper is retrospective relative to the 2013–2014 drives, but it is a peer-reviewed reverse-engineering study of named commercial devices. Product release dates are therefore treated as device chronology, while the attack observations are dated to the later study rather than projected backward as contemporaneous user knowledge.

## Historical / product record

### H/P — self-encrypting SSDs move the sanitization target from payload ciphertext to key state

The paper describes self-encrypting drives as encrypting stored user data with a **data encryption key (DEK)**. For TCG Opal locking ranges, generating a new DEK can make the prior encrypted range inaccessible without rewriting every ciphertext sector.

That creates a distinct sanitization architecture:

```text
physical payload ciphertext may remain
    + old DEK becomes unavailable
    -> old plaintext can become cryptographically inaccessible
```

The engineering promise is therefore conditional. Physical persistence of ciphertext is compatible with successful cryptographic erasure only if the old key relation is genuinely destroyed or made irrecoverable.

**Primary anchor:** Meijer & van Gastel, §II-A–B, especially the DEK discussion and range erase by generating a new DEK.

### H/P — the paper treats key-generation and key-storage behavior as part of erase assurance

The paper's design/implementation checklist does not reduce assurance to `AES is present`. It separately examines:

- whether sanitize creates a fresh randomized DEK with sufficient entropy;
- whether key-bearing internal state has wear-leveling related weaknesses;
- whether power-management paths leave key material behind.

Its summary table makes those separate assessment dimensions for the named devices.

Thus even within the paper's own engineering vocabulary:

```text
cryptographic primitive strength
    != correct key lifecycle
    != correct sanitization behavior
```

**Primary anchors:** §IV; Table I, criteria 7–9.

### H/P — Samsung 840 EVO stored a key-bearing `crypto blob` in NAND internal-data space

For the Samsung 840 EVO, the paper identifies a 64 KiB `crypto blob` containing cryptographic state. It is stored in NAND flash in a region used for the drive's internal data structures.

The paper's example transition is:

1. at `t0`, the drive is unprotected by ATA Security or TCG Opal;
2. the locking range's DEK exists unprotected inside the crypto blob;
3. that blob is physically stored at flash location `s0`;
4. at `t1`, a password/protection state is configured;
5. an updated protected crypto blob is written at location `s1`.

The important fact is that the controller's current protection state changes while an older key-bearing representation can still exist physically.

**Primary anchor:** §VI-E, `Wear leveling` subsection.

### H/P — wear leveling could leave the old unprotected 840 EVO crypto blob recoverable

The 840 EVO's internal crypto-blob storage was itself wear-leveled. Therefore, writing the protected revision did not guarantee in-place replacement of the prior unprotected revision.

The researchers report successfully demonstrating recovery of an earlier crypto-blob revision from NAND. Once recovered, the old revision could be made active through a vendor-specific command path described by the paper.

This gives a named-device witness for:

```text
current protection metadata says "protected"
    != all older key-bearing metadata embodiments are gone
```

It is structurally similar to payload remanence below an FTL, but the retained object here is **controller security metadata / key material**, not a stale user-data page.

**Primary anchor:** §VI-E, `Wear leveling` and attack-strategy discussion.

### H/P — the stale-key window was empirical and bounded, not perpetual

The paper reports that the old and new crypto blobs landed at different physical locations approximately **one in twenty** crypto-state updates in their measurements. It further reports that the stale location was overwritten after roughly **one week of casual office use** in the observed setup.

This matters as counterevidence against an exaggerated claim. The demonstrated problem is not:

> every old Samsung 840 EVO DEK survives indefinitely.

It is:

> a protection-state update did not itself prove immediate destruction of every older key-bearing NAND embodiment.

Survival was contingent on the internal placement/reuse history and elapsed workload.

**Primary anchor:** §VI-E, empirical measurements following the wear-leveling attack.

### H/P — Samsung 850 EVO is a bounded same-vendor negative control for this specific mechanism

For the 850 EVO, the authors report that during responsible disclosure Samsung told them that, from the 850 EVO series onward, crypto-blob storage was no longer wear-leveled and instead used a fixed physical NAND address.

The authors therefore state that the 850 EVO was not vulnerable to the **same crypto-blob recovery attack** caused by wear-leveled placement.

This is a useful negative control because it changes the metadata-placement rule while retaining a broadly similar self-encrypting-drive architecture:

```text
840 EVO: wear-leveled crypto-blob placement
    -> stale prior blob can survive at another physical address

850 EVO: fixed crypto-blob address
    -> that specific stale-placement mechanism is absent
```

This does **not** prove that the 850 EVO's overall encryption implementation, password design, or every erase path is secure. The paper discusses other issues separately.

**Primary anchor:** §VI-F, `Wear leveling` subsection.

### H/P — the study itself separates wear-leveling defects from other cryptographic defects

The paper evaluates several products and shows that eliminating a wear-leveling problem is not equivalent to eliminating every security problem. It independently analyzes password-to-DEK derivation, master-password behavior, entropy, Opal behavior, DEVSLP handling, and other implementation details.

This is important for retention analysis because it prevents one physical-remanence mechanism from swallowing the entire key-management problem.

**Primary anchors:** §IV; device sections in §VI; Table I.

## Retained-state decomposition

The 2019 evidence adds several state classes to Case 47's original payload-centered decomposition:

1. **encrypted user-data ciphertext** — payload embodiments that can remain physically present even after cryptographic erasure;
2. **active DEK** — the currently authoritative key for a locking range;
3. **password / credential state** — state governing whether an actor may obtain or activate access to the DEK;
4. **key-wrapping / crypto-blob metadata** — non-payload structures encoding or protecting key relationships;
5. **current crypto-blob representation** — the blob the controller presently treats as authoritative;
6. **obsolete crypto-blob embodiments** — older physical copies no longer current through the normal control path;
7. **placement / wear-leveling state** — the controller's internal choice of where a new metadata revision is written;
8. **privileged diagnostic / vendor command capability** — a path that can make otherwise non-current internal state operationally relevant in a laboratory attack;
9. **later overwrite/reclamation history** — the process that can eventually destroy the stale physical blob.

The decisive distinction is:

```text
current key-management state
    != complete set of physically retained key-bearing states
```

## Engineering reconstruction

### E — cryptographic erase changes what must be forgotten; it does not eliminate a forgetting obligation

With ordinary media overwrite, the target is every payload embodiment that an attacker can recover.

With cryptographic erase, retained ciphertext can be acceptable if no usable old key survives. The critical forgetting target therefore moves to the **key closure**: every state from which the old DEK can still be obtained, reconstructed, reactivated, or bypassed within the stated threat model.

A bounded reconstruction is:

```text
cryptographic forgetting assurance
    requires, for the targeted old plaintext:

    correct fresh-key transition
    + sufficient new-key entropy
    + old DEK no longer authoritative
    + obsolete key-bearing representations not recoverable/useful
    + no alternate credential/key path that restores old access
```

The paper tests several of these conditions separately. It does not establish a single universal checklist for all SEDs.

### E — state transition success is weaker than representation retirement

On the 840 EVO, configuring password protection could create a new protected crypto blob while an old unprotected copy remained in NAND.

Therefore:

> **successful current-state transition ≠ retirement of every obsolete key-bearing representation**.

This is directly analogous in form to an FTL mapping update leaving stale payload pages, but it occurs in controller-internal metadata.

### E — key remanence and payload remanence are different failure classes

FAST '11 demonstrates old **payload data** surviving below the host-visible FTL mapping. The 2019 Samsung result demonstrates old **key-bearing metadata** surviving below the controller's current protection state.

Either can defeat a particular forgetting claim, but for different reasons:

```text
payload remanence failure:
    old plaintext-bearing physical page survives

key-state remanence failure:
    encrypted payload may remain by design,
    but a stale key-bearing path makes it readable again
```

They should not be collapsed into one generic `flash remanence` label.

### E — logical uniqueness can coexist with physical historical multiplicity in controller metadata

The 840 EVO has one current protection configuration from the ordinary host perspective, yet the study demonstrates that an earlier crypto-blob revision can coexist physically.

Therefore:

> **one current security state ≠ one surviving physical security-state embodiment**.

The consequence is epistemic as well as operational: querying the current state alone cannot prove that no older key-bearing representation remains elsewhere.

### E — metadata-placement policy can determine whether a stale-key window exists

The bounded 840/850 comparison isolates a placement-policy difference. Wear-leveled placement permits old and new revisions to occupy distinct locations; fixed-address replacement removes that particular multiplicity mechanism.

Therefore:

> **same high-level security function ≠ same remanence behavior under a different metadata-placement policy**.

This is not a claim that fixed-address writes are universally atomic, power-fail safe, or securely erased at every storage layer.

### E — time/workload can close a vulnerability window without validating the original transition

The 840 EVO study observed eventual overwrite of stale crypto blobs under casual use. That later destruction can remove the particular recovered witness.

But:

```text
later reclamation destroys stale key state
    != original protection transition itself destroyed stale key state
```

The distinction matters for any sanitization guarantee that is supposed to hold immediately after command completion.

### E — verification must match the stated attack layer

The demonstrated attack requires low-level access, raw NAND recovery, reverse engineering, and a vendor-specific command path. It is not an ordinary host read.

Thus:

> **not visible through normal ATA/Opal state ≠ unavailable to a stronger physical/firmware attacker**.

Conversely, a laboratory path requiring privileged invasive methods does not establish practical exploitability for every attacker model. Assurance statements must name the observation layer.

## Functional comparisons

### F — Case 47 FAST '11: payload remanence vs key-metadata remanence

FAST '11 establishes:

```text
current LBA mapping
    != only surviving payload embodiment
```

The 2019 Samsung evidence adds:

```text
current protection/key state
    != only surviving key-bearing embodiment
```

The comparison is functional. The papers study different devices, dates, mechanisms, and attack paths; no direct technical genealogy is asserted.

### F — Case 44: sanitize contract vs implementation / key-store verification

Case 44 analyzes normative NVMe distinctions among Deallocate, Sanitize, and cryptographic erase semantics. This 2019 slice is empirical SATA/TCG/firmware reverse engineering.

Together they support a bounded verification stack:

```text
specified cryptographic-erase semantics
    != controller's current security state
    != physical key-store history
    != independently demonstrated old-key irrecoverability
```

The 840 EVO experiment is **not** evidence of a failed NVMe Sanitize command and is not imported into Case 44 as if it were.

### F — Case 37: same product family, unrelated maintenance question

Case 37 studies the Samsung 840 EVO old-data **performance/read-recovery** problem and the vendor's restoration/firmware remediation.

This file studies encryption metadata and stale crypto blobs. Sharing a device family does not establish that the 2014 performance issue caused, shared, or was repaired by the same mechanism as the 2019 key-remanence finding.

### F — Synthesis 22: forgetting operation vs proof of forgetting

[`../docs/SYNTHESIS_22_ERASE_INVALIDATION_SANITIZATION_VERIFICATION.md`](../docs/SYNTHESIS_22_ERASE_INVALIDATION_SANITIZATION_VERIFICATION.md) distinguishes interface-level forgetting claims from independent residual-state verification.

This case deepens that distinction for cryptographic erase:

```text
proof that the active key changed
    != proof that every usable old-key witness disappeared
```

## Philosophical / project interpretation

### I — cryptographic forgetting can act on a relation rather than the payload embodiment

For project purposes, cryptographic erasure is a useful example where `forgetting` need not mean destruction of every payload-bearing physical bit.

The retained ciphertext can remain materially present while the system destroys the **decoding relation** that made it recoverable as the old plaintext. In that regime, the key becomes a privileged retention object: forgetting the payload depends on forgetting the key relation strongly enough for the chosen threat model.

This is an interpretive vocabulary of `technical-retention`; the 2019 authors analyze security, key management, and implementation flaws, not a philosophy of memory.

The interpretation must also retain the negative boundary exposed by the 840 EVO:

> changing the authoritative relation does not prove that every prior material witness of that relation has disappeared.

## Explicit non-claims

1. **X — This file does not claim that the Samsung 840 EVO ATA SECURITY ERASE UNIT command was experimentally shown to fail.** The demonstrated stale-blob transition concerns protection-state/key-metadata updates.
2. **X — It does not claim that NVMe Sanitize failed on the Samsung 840 EVO.** The 840 EVO is the SATA product analyzed here, and the evidence is not an NVMe sanitize experiment.
3. **X — It does not claim that every old DEK survives indefinitely.** The study observed later overwrite of stale blobs under use.
4. **X — It does not claim that the approximately one-in-twenty placement observation is a universal firmware probability.** It is an empirical measurement in the study's tested setup.
5. **X — It does not claim that roughly one week is a retention guarantee or maximum.** That duration depended on the tested workload/history.
6. **X — It does not claim that ordinary host software can enumerate stale crypto blobs.** The attack relied on low-level reverse-engineering and physical/firmware techniques.
7. **X — It does not claim that physical ciphertext persistence is itself a cryptographic-erase failure.** Ciphertext may remain safely if all usable old keys are irrecoverable.
8. **X — It does not claim that fixed-address crypto-blob storage makes the 850 EVO wholly secure.** It removes the specific wear-leveling attack described here; other findings remain separate.
9. **X — It does not claim that FAST '11 and the 2019 Samsung mechanism share controller code, firmware lineage, or causal ancestry.** The comparison is functional.
10. **X — It does not claim that Case 37's old-data performance problem is caused by encryption metadata.** Same model family is not mechanism identity.
11. **X — It does not claim that changing a password is the same operation as cryptographic sanitize.** The password transition is evidence about stale key-bearing state, not a sanitize-command trace.
12. **X — It does not claim that a successful cryptographic erase must erase ciphertext.** The relevant target may be key material rather than payload pages.
13. **X — It does not claim that controller self-reporting can never verify sanitization.** It shows why current-state reporting alone may be insufficient against stronger attack models.
14. **X — It does not universalize the Samsung result to all self-encrypting drives.** The paper itself finds different mechanisms across vendors and models.
15. **X — It does not infer that wear leveling is inherently insecure.** The risk arises when wear leveling is applied to sensitive key-bearing state without a mechanism that prevents stale usable copies.

## Claim ledger

| Claim | Label | Evidence / boundary |
| --- | --- | --- |
| self-encrypting drives can cryptographically erase a locking range by generating a new DEK while ciphertext remains | H/P | Meijer & van Gastel §II-A–B |
| the 840 EVO stored a key-bearing crypto blob in internal NAND and wear-leveled that storage | H/P | §VI-E |
| after a password/protection-state update, an older unprotected crypto blob could survive at a different NAND location | H/P | §VI-E |
| researchers demonstrated recovery of a previous crypto-blob revision and could make it active through a vendor-specific command | H/P | §VI-E |
| different old/new blob locations occurred about one in twenty updates in the experiment | H/P | §VI-E empirical measurement; not universalized |
| the stale blob was overwritten after roughly one week of casual office use in the observed setup | H/P | §VI-E empirical observation; not a guarantee |
| authors report Samsung said 850 EVO and later used fixed-address crypto-blob storage and was not vulnerable to that specific wear-leveling attack | H/P | §VI-F; vendor statement transmitted through paper |
| `current key state != complete set of physically retained key-bearing states` | E | 840 EVO stale-blob demonstration |
| cryptographic erase assurance requires reasoning about old-key irrecoverability, not only ciphertext presence | E | DEK model + key-lifecycle findings |
| changing password/protection state is equivalent to issuing a sanitize command | X | not established |
| Samsung 840 EVO sanitize was directly shown to fail | X | not established by this source |
| fixed-address 850 EVO metadata proves complete sanitization security | X | not established |

## Evidence strength and limitations

**Strong for this bounded claim:** a named-device, peer-reviewed reverse-engineering study reports a demonstrated stale key-bearing metadata attack on the Samsung 840 EVO and gives a same-vendor placement-policy contrast for the 850 EVO.

**Moderate for exact physical chronology:** the study was performed after product release, so it is evidence about the analyzed devices/firmware, not contemporaneous 2013 public documentation of the flaw.

**Not closed:** exact firmware revisions for every demonstrated 840/850 behavior are not pinned in this file, and the paper does not supply a controlled `sanitize command -> power cycle -> raw-key recovery` experiment for the 840 EVO.

## Remaining evidence debt

1. Pin exact Samsung 840 EVO and 850 EVO firmware revisions for the crypto-blob experiments where recoverable.
2. Find a named-device experiment that directly executes ATA SANITIZE / SECURITY ERASE or NVMe Crypto Erase and then independently searches for old key material.
3. Separate ATA SECURITY ERASE, TCG Opal revert/range-key regeneration, PSID workflows, and NVMe Sanitize command paths instead of treating them as one `crypto erase` operation.
4. Add a power-loss/interruption experiment around key replacement: old-key retirement, new-key publication, and crash recovery are separate transition questions.
5. Find vendor/security-evaluation material that documents which nonvolatile key stores, copies, wrapped forms, and recovery paths are included in a crypto-erase assurance boundary.
6. Keep privileged JTAG/vendor-command evidence distinct from ordinary host-interface exploitability.
7. If a later NVMe implementation study is added, compare it to Case 44's normative contract without projecting NVMe semantics backward onto the SATA 840 EVO.

## Repository routing

- Canonical case: [`../cases/47-fast11-ssd-sanitization-verification.md`](../cases/47-fast11-ssd-sanitization-verification.md)
- Original FAST '11 grounding: [`47-fast11-2011-ssd-sanitization-grounding.md`](47-fast11-2011-ssd-sanitization-grounding.md)
- NVMe forgetting semantics: [`../cases/44-nvme13-deallocate-sanitize-forgetting.md`](../cases/44-nvme13-deallocate-sanitize-forgetting.md)
- Samsung 840 EVO performance-refresh case: [`../cases/37-samsung-840-evo-old-data-performance-refresh.md`](../cases/37-samsung-840-evo-old-data-performance-refresh.md)
- Erase/invalidation/sanitization synthesis: [`../docs/SYNTHESIS_22_ERASE_INVALIDATION_SANITIZATION_VERIFICATION.md`](../docs/SYNTHESIS_22_ERASE_INVALIDATION_SANITIZATION_VERIFICATION.md)

## Sources

### Primary / high-quality technical

- Carlo Meijer and Bernard van Gastel, **“Self-Encrypting Deception: Weaknesses in the Encryption of Solid State Drives,”** *2019 IEEE Symposium on Security and Privacy*, 2019, pp. 72–87, DOI `10.1109/SP.2019.00088`: <https://www.cs.ru.nl/~cmeijer/publications/Self_Encrypting_Deception_Weaknesses_in_the_Encryption_of_Solid_State_Drives.pdf>
- Open Universiteit research portal bibliographic record: <https://research.ou.nl/en/publications/self-encrypting-deception-weaknesses-in-the-encryption-of-solid-s/>

### Existing repository evidence used only for bounded comparison

- Michael Wei et al., FAST '11 grounding: [`47-fast11-2011-ssd-sanitization-grounding.md`](47-fast11-2011-ssd-sanitization-grounding.md)
- NVMe normative sanitization semantics: [`44-nvme12-13-deallocate-sanitize-grounding.md`](44-nvme12-13-deallocate-sanitize-grounding.md)
- Samsung 840 EVO old-data performance remediation: [`37-samsung-840-evo-2014-2015-performance-refresh-grounding.md`](37-samsung-840-evo-2014-2015-performance-refresh-grounding.md)

## Completion note

This slice closes a bounded part of Case 47's `cryptographic-erase verification / key-store scope` debt by adding named-device evidence that **obsolete key-bearing controller metadata can outlive a current protection-state transition**. It deliberately leaves direct post-sanitize key recovery, firmware-exact command tracing, and later NVMe implementation verification open.