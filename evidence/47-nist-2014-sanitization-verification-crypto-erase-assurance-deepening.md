# Case 47 deepening — NIST SP 800-88 Rev. 1 verification and Cryptographic Erase assurance boundary

**Status:** bounded deepening complete  
**Canonical case:** [`../cases/47-fast11-ssd-sanitization-verification.md`](../cases/47-fast11-ssd-sanitization-verification.md)  
**Primary period studied:** 2014 operational guidance, with the 2011 FAST experiment used only as a controlled comparison  
**Research slice:** what evidence NIST required between a sanitization command/technique and an acceptable forgetting claim, especially for flash and Cryptographic Erase

---

## 1. Why this slice

Case 47 already contains two strong empirical lines:

1. FAST ’11 shows that an SSD can make data disappear from the ordinary host interface, or even report erase success, while old digital embodiments remain in raw flash.
2. The 2019 Samsung 840 EVO deepening shows that current protection state can coexist with an obsolete key-bearing metadata revision in NAND.

What was still missing was a period institutional source that asks a different question:

> after selecting a sanitization mechanism, what evidence is required before an operator should trust the resulting forgetting claim?

NIST Special Publication 800-88 Revision 1 is useful precisely because it does **not** reduce sanitization assurance to a command name. It separately discusses:

- media-specific mechanism selection;
- implementation trust;
- verification of sanitization results;
- special verification problems for Cryptographic Erase;
- device/version/key-lifecycle facts that must be known before CE is relied upon;
- differences hidden behind nominally standardized command sets.

That provides a standards/guidance counterpart to Case 47’s laboratory evidence without treating the two sources as interchangeable.

---

## 2. Source set and evidence roles

### E1 — NIST SP 800-88 Rev. 1

Richard Kissel, Andrew Regenscheid, Matthew Scholl, and Kevin Stine, **Guidelines for Media Sanitization**, NIST Special Publication 800-88 Revision 1, December 2014.

- NIST publication record: <https://csrc.nist.gov/pubs/sp/800/88/r1/final>
- DOI / official PDF: <https://doi.org/10.6028/NIST.SP.800-88r1>

**Role:** primary historical/institutional source for the 2014 sanitization-assurance model used in this slice.

The CSRC publication history records the final as **17 December 2014**, superseding the original 2006 SP 800-88. The same page now marks Rev. 1 as withdrawn on **26 September 2025** and superseded by Rev. 2.

That later withdrawal matters only for source provenance:

> this file uses Rev. 1 as historical evidence for 2014 practice/guidance, not as a claim about current NIST guidance.

### E2 — Wei et al., FAST ’11

Michael Wei, Laura Grupp, Frederick E. Spada, and Steven Swanson, **“Reliably Erasing Data From Flash-Based Solid State Drives,”** FAST ’11, February 2011.

- USENIX record: <https://www.usenix.org/conference/fast11/reliably-erasing-data-flash-based-solid-state-drives>
- Existing repository grounding: [`47-fast11-2011-ssd-sanitization-grounding.md`](47-fast11-2011-ssd-sanitization-grounding.md)

**Role:** controlled empirical comparison only.

NIST Rev. 1 itself lists the FAST ’11 paper in Appendix F’s selected bibliography. That bibliographic inclusion establishes that the paper was among the sources NIST chose to list; it does **not** by itself establish which individual Rev. 1 recommendation was causally derived from Wei et al.

### E3 — named-device key-store deepening

- [`47-samsung-840-850-crypto-blob-remanence-deepening.md`](47-samsung-840-850-crypto-blob-remanence-deepening.md)

**Role:** later empirical comparison showing why key-lifecycle scope can matter below current controller state.

### Evidence labels

- **H/P** — historical / policy record stated by the period source;
- **E** — bounded engineering reconstruction;
- **F** — controlled functional comparison across sources/cases;
- **I** — project-level philosophical interpretation;
- **X** — explicit non-claim.

---

## 3. Historical / policy record

### H/P — NIST separates native-address coverage from broader sanitize coverage

Rev. 1 §2.4 says that a drawback of relying only on the native read/write interface is that areas not currently mapped to active LBAs — including examples such as defect areas and unallocated space — are not addressed by that ordinary overwrite path.

It then says dedicated sanitize commands can address such areas more effectively.

The guide immediately adds a qualification: using those commands requires **trust and assurance from the vendor that the commands were implemented as expected**.

The period relationship is therefore already more complicated than:

```text
standardized command name
    -> sanitization proven
```

The source instead gives something closer to:

```text
selected command / technique
    + device implementation
    + assurance about that implementation
    -> candidate sanitization result
```

**Primary anchor:** E1, §2.4, printed p. 7.

### H/P — Rev. 1 treats flash as a media-specific sanitization problem

Sections 2.3–2.4 describe the rise of flash-based storage as a major sanitization change. The guide explicitly warns against simply carrying over techniques developed for magnetic media.

It notes both that degaussing generally does not apply to flash and that a host interface can remain superficially similar while the underlying media and relevant sanitization mechanisms differ.

The historical claim is therefore:

> same or similar host interface did not imply the same sanitization mechanism.

**Primary anchor:** E1, §§2.3–2.4, printed pp. 6–7.

### H/P — verification is a distinct step, not a synonym for issuing the sanitization operation

Rev. 1 §4.7 calls verification an essential step in the sanitization/disposal process.

It distinguishes two verification modes to consider:

1. verification whenever sanitization is applied, where practical;
2. representative sampling verification over a selected subset of sanitized media.

It additionally discusses equipment calibration/testing and operator competency before reaching the specific verification-of-results subsection.

This means the historical workflow contains separable states:

```text
technique selected
    -> technique executed
    -> result verified
```

rather than treating execution and verification as one event.

**Primary anchor:** E1, §4.7–§4.7.3, printed p. 20.

### H/P — full native-interface reading is high assurance only within an explicit observation boundary

For operational ATA/SCSI/SSD devices, §4.7.3 says the highest level of assurance outside a laboratory is typically a full read of all **accessible** areas, checking that the expected sanitized value appears in all addressable locations, when the technique produces such a value and circumstances permit.

Representative sampling guidance then asks for pseudorandom locations spread across the addressable space rather than repeatedly checking a small convenient region.

This is important, but its scope must be preserved:

```text
full native-interface verification
    = strong evidence over accessible/addressable locations

full native-interface verification
    != proof that no controller-hidden physical embodiment exists
```

NIST does not describe the latter relation in those words; the second line is the repository’s bounded engineering reconstruction when §4.7.3 is compared with FAST ’11’s raw-chip method.

**Primary anchor:** E1, §4.7.3, printed pp. 20–21.

### H/P — Cryptographic Erase has a different verification problem from overwrite/block erase

Rev. 1 §4.7.3 explicitly says Cryptographic Erase has different verification considerations because the physical media contents after CE may not have a known fixed value that can simply be compared with an expected overwrite pattern.

The guide gives candidate checks such as:

- sample locations before CE and compare them after CE;
- search for known strings/files in sampled regions;
- sample broadly across the addressable area.

It then gives a strong fallback rule: if an organization cannot verify that CE effectively sanitized the storage media, it should use an alternative sanitization method that can be verified, either in combination with CE or instead of it.

Therefore the 2014 guidance itself rejects this shortcut:

```text
CE command completed
    -> therefore CE assurance is automatically sufficient
```

**Primary anchor:** E1, §4.7.3, printed p. 21.

### H/P — Rev. 1 treats CE assurance as an implementation-description problem

Appendix D begins by saying that whether CE should be relied on depends on the user’s ability to determine whether the implementation offers sufficient assurance against future recovery.

It then asks users/vendors to identify at least these dimensions:

1. make / model / version / media type;
2. key generation;
3. media encryption algorithm / strength / mode;
4. key level and wrapping — including whether the MEK itself or a wrapping key is sanitized;
5. data areas addressed and any areas not encrypted;
6. key lifecycle management, including previous key instances created by wrapping/rewrapping;
7. key sanitization technique;
8. key escrow or backup;
9. error-condition handling, including what happens if a key-storage location cannot be sanitized;
10. interface clarity, including which commands affect which MEKs.

This is unusually useful for Case 47 because it makes the forgetting target explicit:

> CE assurance is not only about the currently active encryption key.

It depends on the complete enough lifecycle and scope of key-bearing state for the intended purge claim.

**Primary anchor:** E1, Appendix D, printed pp. 49–50.

### H/P — NIST explicitly asks about old key instances and external copies

Appendix D’s key-lifecycle item asks how previous key instances are handled when keys are wrapped, unwrapped, and rewrapped.

Its escrow/backup item asks whether keys at or below the relevant level have ever been escrowed from or injected into the device.

Its data-area item asks which areas are encrypted and how unencrypted areas are sanitized.

This gives a concrete historical decomposition:

```text
current MEK changed
    !=
all relevant prior key instances sanitized
    !=
all escrow / backup paths excluded
    !=
all target-data areas covered
```

The source does not use the repository term `key closure`; that is project vocabulary for this conjunction of lifecycle/scope conditions.

### H/P — standardized command families can hide device-specific implementations

Appendix E says storage devices from different vendors can share standardized command sets such as ATA, SCSI, and NVM Express while implementing the underlying sanitization action differently.

It says it may be difficult or impossible for users to know exactly how the operation is implemented internally and suggests vendor disclosure of details including:

- media type;
- supported sanitize commands;
- areas not addressed;
- expected completion time;
- validation-test results where applicable.

This institutional source therefore directly supports:

```text
shared command vocabulary
    !=
shared implementation behavior
```

**Primary anchor:** E1, Appendix E, printed p. 52.

### H/P — the guide preserves the FAST ’11 paper as part of its selected bibliography

Appendix F lists Wei, Grupp, Spada, and Swanson’s FAST ’11 SSD sanitization paper.

This establishes a bibliographic connection between the 2011 empirical study and the 2014 NIST revision.

It does **not** prove:

- that one particular NIST sentence came from FAST ’11;
- that NIST reproduced the FAST experiment;
- that NIST endorsed every proposed FTL mechanism in the paper.

**Primary anchor:** E1, Appendix F, printed p. 55.

---

## 4. Engineering reconstruction

### E — sanitization assurance is a chain, not a single status bit

The combined NIST evidence supports a bounded assurance chain:

```text
forgetting requirement
    -> media / device identified
    -> technique selected
    -> implementation applicability established
    -> technique executed
    -> completion / result evidence gathered
    -> verification scope understood
    -> sanitization claim accepted for the intended threat model
```

Breaking any one arrow can invalidate the final claim without implying that every other arrow failed.

### E — command completion evidence and residual-state evidence answer different questions

A command status can answer:

> did the implementation report that the requested operation completed?

A readback/sampling procedure can answer:

> did the observer find target data in the locations that this verification method can inspect?

A raw-chip experiment can ask:

> does an old digital embodiment remain below the controller’s ordinary visibility?

Therefore:

```text
operation-status evidence
    !=
native-interface verification evidence
    !=
raw-media residual-state evidence
```

The evidence classes can reinforce one another, but they are not interchangeable.

### E — verification strength is observation-boundary dependent

The important variable is not just `how much was sampled?` but also:

```text
which state space can the verifier see?
```

A complete scan of one observation layer can still be incomplete relative to a lower layer.

Thus:

```text
100% of accessible LBAs read
    !=
100% of physical NAND embodiments enumerated
```

FAST ’11 demonstrates why this distinction matters for flash; Rev. 1 provides the operational verification vocabulary.

### E — Cryptographic Erase moves, rather than eliminates, the retention target

With CE, ciphertext can remain physically present while future plaintext recovery depends on whether the relevant key relation remains available.

The forgetting target therefore moves from:

```text
remove every payload embodiment
```

toward:

```text
make every key relation required for target-data recovery unavailable
```

But Appendix D shows that this is not simply:

```text
delete one active key
```

because the assurance scope can include prior wrapped instances, key hierarchy, escrow/backup, data-area coverage, error handling, and all relevant MEKs.

### E — `key closure` is a scope proof, not merely a key-generation event

Project shorthand:

```text
CE key closure
    = enough evidence that every key-bearing path
      still capable of recovering the target data
      has been eliminated or rendered unusable
```

This is a reconstruction, not NIST’s phrase.

It follows from the multiple Appendix D conditions and is deliberately stronger than:

```text
new key generated
```

or:

```text
current controller state reports protected
```

### E — successful forgetting can require retained assurance metadata

A sanitization system may need to retain facts such as:

- exact make/model/version;
- command / technique selected;
- result / error status;
- validation evidence;
- key hierarchy and coverage information.

Those retained facts are not the confidential payload being forgotten. They are **evidence about whether forgetting was justified**.

Therefore technical retention can include the apparently paradoxical relation:

```text
forget payload state
    while
retain enough evidence to justify the forgetting claim
```

The exact audit-record schema is an implementation/policy choice; Rev. 1 does not require this repository’s terminology.

---

## 5. Controlled functional comparison with FAST ’11

### F — FAST ’11 is a laboratory falsification path; Rev. 1 is an operational assurance framework

FAST ’11:

```text
sanitize / overwrite attempt
    -> dismantle SSD
    -> bypass controller
    -> raw NAND fingerprint search
    -> old embodiments can falsify the sanitization claim
```

NIST Rev. 1:

```text
sanitization requirement
    -> select media-appropriate technique
    -> understand implementation / device scope
    -> execute
    -> verify using an appropriate method
    -> accept or reject result
```

These are complementary, not equivalent.

FAST ’11 provides unusually strong lower-layer empirical evidence for a bounded device sample. NIST provides a broadly applicable operational process and explicitly recognizes implementation trust, verification, and CE-specific assurance conditions.

### F — NIST’s native-interface verification is not FAST ’11’s raw-media verification

This distinction must stay explicit:

```text
NIST full read of accessible/addressable areas
    !=
FAST raw-chip scan below the FTL
```

It would be incorrect to cite §4.7.3 as though NIST required dismantling every SSD and reading raw NAND.

Conversely, it would be incorrect to use FAST ’11 to claim that native-interface verification has no value. It can detect broad failures and provides operational evidence over the interface it can inspect.

### F — Drive B is a concrete example of why status-only assurance is weak

FAST ’11’s anonymized Drive B reported successful sanitization while its data remained intact and its filesystem remained mountable.

NIST Rev. 1 later says dedicated sanitize commands require implementation trust/assurance and separately requires verification.

The functional comparison is strong:

```text
reported success
    !=
verified outcome
```

But no claim is made that NIST wrote those passages specifically because of Drive B.

### F — Samsung 840 EVO illustrates one Appendix-D-style lifecycle concern

The 2019 Samsung deepening shows an obsolete key-bearing metadata revision surviving because the internal crypto blob was wear-leveled.

Appendix D had already required users to reason about:

- key lifecycle;
- which key level is sanitized;
- prior key instances;
- storage/media scope;
- error handling.

The later named-device study is therefore a useful functional witness for why those categories matter.

It is **not** evidence that the Samsung 840 EVO failed a NIST-defined CE procedure, because the demonstrated transition was protection/password-state reconfiguration rather than a controlled named CE command experiment.

---

## 6. Cross-case hooks

### Case 44 — NVMe Deallocate / Sanitize

Case 44 provides later normative command semantics:

```text
Deallocate
    !=
Sanitize
```

This Case-47 deepening adds:

```text
Sanitize semantics / command availability
    !=
implementation assurance
    !=
verification evidence
```

### Case 150 — SSD compatibility / command-path admission

Case 150 shows that even when a host retains a correct safety rule, model/firmware identity and applicability can determine whether that rule is actually selected.

The functional comparison here is only:

```text
nominal interface category
    !=
complete device-specific applicability knowledge
```

No design genealogy between Linux libata workarounds and NIST sanitization guidance is asserted.

---

## 7. Philosophical interpretation

### I — a forgetting claim is relative to an evidence boundary

The strongest bounded interpretation is:

> `nothing was found` is meaningful only together with `where, how, and against what recovery capability did we look?`

This does not make sanitization unknowable. It says that assurance claims have an observation scope.

### I — successful forgetting and knowledge of forgetting are different states

A device might actually have destroyed every relevant old embodiment even if the operator cannot prove that fact.

Conversely, an operator can possess a success status while target state remains.

Therefore:

```text
forgetting actually occurred
    !=
operator has sufficient evidence that forgetting occurred
```

Case 47 is valuable because it contains direct examples of the second mismatch.

### I — cryptographic forgetting is relational rather than purely material

CE can leave ciphertext physically intact while destroying the relation needed to recover plaintext.

So for this bounded mechanism:

```text
physical persistence
    can coexist with
semantic / cryptographic inaccessibility
```

But only if the relevant key relation is genuinely closed. The project should not convert that conditional statement into a universal claim that encrypted remnants are harmless.

---

## 8. Explicit non-claims

This evidence file does **not** claim that:

1. NIST SP 800-88 Rev. 1 is current guidance; it was superseded by Rev. 2 in September 2025.
2. NIST requires raw-NAND teardown verification for every SSD.
3. a full native-interface read can enumerate controller-hidden over-provisioned NAND.
4. representative sampling proves mathematical absence of every remnant.
5. verification failure means sanitization definitely failed physically.
6. successful command status proves sanitization.
7. all ATA/SCSI/NVMe sanitize implementations differ.
8. standardized interfaces are unreliable by definition.
9. FAST ’11 tested NVMe Sanitize.
10. the anonymized FAST ’11 drives can be mapped safely to named consumer models.
11. NIST reproduced Wei et al.’s raw-flash experiment.
12. every NIST Rev. 1 recommendation was caused by FAST ’11 merely because the paper appears in Appendix F.
13. every Cryptographic Erase implementation is suitable for Purge.
14. changing one active key establishes key closure.
15. changing a KEK and changing a MEK are always equivalent.
16. escrow, backup, wrapping, and stale on-device key copies are the same mechanism.
17. every encrypted byte on a device is necessarily covered by the same key.
18. ciphertext persistence after valid CE is itself proof of CE failure.
19. inability to recover sampled plaintext proves that no alternate key path exists.
20. the Samsung 840 EVO study executed and falsified a named NIST CE procedure.
21. the Samsung 850 EVO negative control proves universal sanitize correctness.
22. `key closure` is NIST historical terminology; it is repository shorthand.
23. `observation boundary` is NIST historical terminology; it is repository shorthand.
24. a sanitization certificate or retained audit record is equivalent to residual-state verification.
25. device/version disclosure by a vendor independently proves implementation correctness.
26. Appendix D is a formal cryptographic proof system.
27. Rev. 1’s 2014 guidance should be retroactively projected into 2011 developer intent.
28. the 2014 guide settles analog remanence for all modern flash technologies.
29. all hidden areas are reachable through the same verification interface.
30. stronger verification is free of time, tooling, or operational cost.

---

## 9. Evidence maturity

This slice strengthens Case 47 without changing its maturity beyond `grounded`.

What is now strongly supported:

```text
command / technique selection
    !=
implementation assurance
    !=
result verification
```

and:

```text
current-key transition
    !=
complete CE assurance scope
```

and:

```text
full verification at one observation layer
    !=
exhaustive verification of lower hidden layers
```

The evidence is strong because the main claims come from a first-party institutional publication, while FAST ’11 supplies a peer-reviewed empirical counterexample set and the Samsung deepening supplies later named-device key-state evidence.

---

## 10. Remaining evidence debt after this slice

The most useful next Case-47 work is now narrower:

1. **Named sanitize-command execution:** find controlled experiments on named SSD/controller + firmware revisions that actually execute ATA SANITIZE / SCSI SANITIZE / NVMe Sanitize and independently test residual state.
2. **Named CE execution:** execute or find studies of a named Cryptographic Erase/key-regeneration command followed by independent old-key/key-bearing-state search.
3. **Verification-layer comparison:** map what each real tool can observe — LBA, service area, controller metadata, NAND page, spare/OOB — without collapsing them into one `media scan` category.
4. **Firmware/version boundary:** identify cases where sanitize behavior changes across firmware versions of one named model.
5. **Power interruption:** test or source behavior when sanitize/CE is interrupted and later resumed/reported.
6. **Hidden-capacity scope:** newer empirical work on remapped/over-provisioned NAND after standardized sanitize operations.
7. **Rev. 2 comparison:** only if needed, create a separate historical-policy slice comparing the 2014 Rev. 1 assurance model with the 2025 Rev. 2 model; do not silently overwrite this historical evidence with current guidance.

---

## 11. Related-repository duplication check

`tmzncty/computing-archaeology` was searched in this slice for:

- `SP 800-88`;
- `cryptographic erase`.

No dedicated matching packet was found.

A broad history of storage-security standards, ATA/SCSI/NVMe command-set development, or secure-erase industry adoption should still be developed in the companion repository if needed. This file keeps only the technical-retention question:

> what state, scope, and evidence must survive long enough for a forgetting claim to be justified?

---

## 12. Compact result

```text
sanitization intent
    !=
sanitization command / technique
    !=
device-specific implementation
    !=
reported completion
    !=
verification result
    !=
exhaustive lower-layer absence proof
```

For Cryptographic Erase:

```text
new / changed key state
    !=
all relevant prior key relations closed

CE assurance
    requires reasoning about
    model/version
    + encryption scope
    + key hierarchy
    + lifecycle
    + escrow/backup
    + key-sanitization method
    + error handling
    + interface semantics
```

The retained object in this slice is therefore partly **assurance knowledge** itself: enough device-, method-, and verification-state to distinguish `we requested forgetting` from `we have justified evidence that the intended forgetting contract was fulfilled`.