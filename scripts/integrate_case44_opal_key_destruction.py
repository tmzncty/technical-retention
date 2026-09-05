from pathlib import Path


def read(path):
    return Path(path).read_text(encoding="utf-8")


def write(path, text):
    Path(path).write_text(text, encoding="utf-8")


def replace_once(path, old, new):
    text = read(path)
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected one anchor, found {count}: {old[:160]!r}")
    write(path, text.replace(old, new, 1))


case = "cases/44-nvme13-deallocate-sanitize-forgetting.md"
ev = "evidence/44-nvme12-13-deallocate-sanitize-grounding.md"

# 1) Case 44: extend the bounded historical window backward to explicit 2009
# storage-security key-eradication semantics without turning this into a generic SED history.
status_old = """**`grounded`** — bounded to the NVM Express 1.3 interface semantics for Dataset Management `Deallocate` and `Sanitize`, with NVM Express 1.2.1 `Format NVM` secure-erase semantics used as the immediate prior-version boundary. The case asks what the interface means when a host says that a logical range is no longer needed, versus when it requests that prior user data be made unavailable across the NVM subsystem."""
status_new = """**`grounded`** — bounded to the NVM Express 1.3 interface semantics for Dataset Management `Deallocate` and `Sanitize`, with NVM Express 1.2.1 `Format NVM` secure-erase semantics used as the immediate prior-version boundary. TCG Opal 1.0 Revision 1.0 (January 2009) is now used as an earlier storage-security prior-art boundary for media-encryption-key eradication and for the explicit `KeepGlobalRangeKey` counterexample in which a security-provider lifecycle reset occurs without cryptographic erase. The case asks what the interface means when a host says that a logical range is no longer needed, versus when it requests that prior user data be made unavailable across the NVM subsystem."""
replace_once(case, status_old, status_new)

prior_heading = "## Broader prior art boundary\n"
prior_insert = """## Earlier storage-security prior art — TCG Opal 1.0 key eradication (2009)

The **TCG Storage Security Subsystem Class: Opal Specification, Version 1.0, Revision 1.0**, dated **January 27, 2009**, supplies an earlier storage-interface witness for a relation that later appears in NVMe Crypto Erase. The direct TCG PDF is:

<https://trustedcomputinggroup.org/wp-content/uploads/Opal_SSC_1.0_rev1.0-Final.pdf>

Historical vocabulary must remain source-specific. Opal speaks about a `Locking SP`, `Revert`, `RevertSP`, a `media encryption key`, `KeepGlobalRangeKey`, and `cryptographic erase`; this repository should not silently rewrite those 2009 lifecycle/security terms into later NVMe `Sanitize` terminology.

In §5.2.2 (`Revert`, printed p. 76), the specification says that reverting the Locking SP returns it to its original factory state and securely erases personalization. An informative note then states that reverting the Locking SP causes **media encryption keys to be eradicated**, with the side effect of securely erasing data in the User LBA portion. The precise secure-erasure implementation is left implementation-specific.

Section §5.2.3 (`RevertSP`, printed p. 77) provides the more important counterexample. Its optional `KeepGlobalRangeKey` parameter allows the Locking SP to be turned off **without eradicating the media encryption key for the Global locking range** and explicitly describes this as avoiding a **cryptographic erase** of the user data associated with that range. If the parameter is true, the TPer continues using the existing media encryption key after the state transition.

That primary source supports two separate layers.

**Historical record:**

> **security-provider lifecycle reset ≠ cryptographic erase.**

The same family of reset operations can either eradicate a relevant media key or deliberately preserve it.

**Engineering reconstruction:**

> **media-encryption-key eradication ≠ physical ciphertext overwrite.**

In an encrypted-storage regime, recoverability can depend on a retained relation between ciphertext and key material. Destroying that relation can make the old user data unavailable without requiring the same physical transformation as block erase or overwrite. Conversely, preserving the key can preserve that decryptability relation while ownership/security-provider state is reset.

This also blocks a tempting category error:

> **factory-state reset ≠ universal proof of data destruction.**

The effect depends on which retained control and key relations the operation actually retires.

This is a **prior-art boundary**, not an invention claim. The 2009 specification establishes that explicit media-key-eradication / cryptographic-erase semantics predate NIST SP 800-88 Rev. 1 (2014) and NVMe 1.2.1/1.3 (2016–2017), but it does not prove that TCG invented cryptographic erasure, nor does a standards-level contract prove named-product compliance.

## Broader prior art boundary
"""
replace_once(case, prior_heading, prior_insert)

nvm_prior_old = """Media-sanitization vocabulary and cryptographic erasure also predate NVMe 1.3. NIST SP 800-88 Rev. 1 was finalized in December 2014 and defines media sanitization as rendering access to target data infeasible for a stated level of effort; its keyword set includes `crypto erase` and `secure erase`.

This source is used only to block an invention-priority shortcut. It does **not** imply that NVMe 1.3 simply copied NIST's taxonomy or that the interface semantics are reducible to the policy document."""
nvm_prior_new = """Media-sanitization vocabulary and cryptographic erasure also predate NVMe 1.3. The TCG Opal 1.0 witness above pushes explicit storage-interface key-eradication / cryptographic-erase semantics back to 2009. NIST SP 800-88 Rev. 1 was finalized in December 2014 and defines media sanitization as rendering access to target data infeasible for a stated level of effort; its keyword set includes `crypto erase` and `secure erase`.

These sources are used to block invention-priority shortcuts and to separate engineering layers. They do **not** imply that NVMe 1.3 simply copied TCG or NIST taxonomy, that TCG originated cryptographic erasure, or that later NVMe interface semantics are reducible to either earlier document."""
replace_once(case, nvm_prior_old, nvm_prior_new)

claim_anchor = """| NVMe 1.2.1 already provided User Data Erase / Cryptographic Erase through Format NVM | H/P | Revision 1.2.1 §5.16 |
| `logical deallocation != physical/media erasure` | E | reconstruction from permitted deallocated-read semantics and sanitize scope |"""
claim_new = """| NVMe 1.2.1 already provided User Data Erase / Cryptographic Erase through Format NVM | H/P | Revision 1.2.1 §5.16 |
| TCG Opal 1.0 Rev. 1.0 (Jan. 27, 2009) states that Locking-SP Revert eradicates media encryption keys, with secure erasure of User-LBA data as the described side effect | H/P | Opal 1.0 Rev. 1.0 §5.2.2, printed p. 76; secure-erasure note is informative |
| Opal `RevertSP` with `KeepGlobalRangeKey=true` can reset/turn off the Locking SP while preserving the Global-range media key and avoiding cryptographic erase for that range | H/P | Opal 1.0 Rev. 1.0 §5.2.3, printed p. 77 |
| `security-provider lifecycle reset != cryptographic erase` | E | reconstruction from the `KeepGlobalRangeKey` counterexample |
| `media-encryption-key eradication != physical ciphertext overwrite` | E | bounded reconstruction from encrypted-storage key dependence; not a forensic-unrecoverability claim |
| `logical deallocation != physical/media erasure` | E | reconstruction from permitted deallocated-read semantics and sanitize scope |"""
replace_once(case, claim_anchor, claim_new)

# 2) Grounding record: add the exact primary source, exact sections, and evidence boundary.
ev_source_anchor = """## Directly grounded historical claims
"""
ev_source_insert = """### TCG Storage Security Subsystem Class: Opal 1.0 Revision 1.0

Trusted Computing Group, **Storage Security Subsystem Class: Opal, Version 1.0, Revision 1.0**, January 27, 2009.

Direct TCG primary PDF:

- <https://trustedcomputinggroup.org/wp-content/uploads/Opal_SSC_1.0_rev1.0-Final.pdf>

Sections inspected:

- §5.2.2, `Revert` — printed p. 76;
- §5.2.3, `RevertSP` and `KeepGlobalRangeKey` — printed pp. 77–78.

Inspection level: **direct primary standards PDF text with exact section/page anchoring**. The source is used for its own 2009 vocabulary and operation semantics, not as evidence for every later self-encrypting-drive implementation.

## Directly grounded historical claims
"""
replace_once(ev, ev_source_anchor, ev_source_insert)

hist_anchor = """## Visual inspection note
"""
hist_insert = """### TCG Opal 1.0 §5.2.2–§5.2.3 — key eradication and an explicit non-erasure counterexample

The January 2009 Opal specification gives two neighboring operation paths whose difference is retention-critical.

In §5.2.2, `Revert` returns the Locking SP to its original factory state and securely erases personalization. The specification's informative note says that this operation causes **media encryption keys to be eradicated**, with the side effect of securely erasing data in the User LBA portion. The secure-erasure mechanism itself is implementation-specific.

In §5.2.3, `RevertSP` accepts an optional `KeepGlobalRangeKey` parameter. The specification says this option allows the Locking SP to be turned off **without eradicating the media encryption key for the Global locking range**, explicitly so that the transition occurs **without causing a cryptographic erase** of the user data associated with that range. When the parameter is true, the TPer continues to use the existing media encryption key after the Locking-SP state change.

This directly grounds:

- explicit storage-security `media encryption key` / `cryptographic erase` semantics by January 27, 2009;
- key eradication as a relation distinct from physical block erase or overwrite;
- an explicit counterexample in which a broad security-provider lifecycle reset does **not** erase the relevant key;
- `security-provider lifecycle reset != cryptographic erase`;
- `key-state transition != authentication/locking-state transition`.

The evidence does **not** establish:

- that TCG invented cryptographic erase or media-key destruction;
- that every Opal product implements Revert/RevertSP correctly;
- that eradicating one key destroys every possible backup, wrapped copy, escrow copy, host copy, or forensic avenue outside the specified TPer state;
- that ciphertext bits are physically overwritten when the key is eradicated.

## Visual inspection note
"""
replace_once(ev, hist_anchor, hist_insert)

broad_old = """NIST **SP 800-88 Rev. 1**, finalized December 17, 2014, defines media sanitization as rendering access to target data infeasible for a given level of effort and includes `crypto erase` and `secure erase` in its keyword vocabulary.

This establishes that media-sanitization / crypto-erase terminology predates NVMe Revision 1.3. It does **not** establish direct standards genealogy from NIST into NVMe and is not used to reinterpret normative NVMe fields."""
broad_new = """TCG **Opal 1.0 Revision 1.0**, dated January 27, 2009, now provides the earlier storage-interface witness for media-key eradication and explicit `cryptographic erase` semantics. This moves the repository's bounded prior-art line earlier than both NIST SP 800-88 Rev. 1 and NVMe secure-erase/sanitize revisions without making an invention-priority claim.

NIST **SP 800-88 Rev. 1**, finalized December 17, 2014, defines media sanitization as rendering access to target data infeasible for a given level of effort and includes `crypto erase` and `secure erase` in its keyword vocabulary.

Together these establish that cryptographic-erasure vocabulary and mechanism classes predate NVMe Revision 1.3. They do **not** establish direct standards genealogy from TCG or NIST into NVMe and are not used to reinterpret normative NVMe fields."""
replace_once(ev, broad_old, broad_new)

eng_old = """- `forgetting payload can depend on retaining erasure-progress/result state`;
- `stronger forgetting work != zero medium/endurance cost`."""
eng_new = """- `forgetting payload can depend on retaining erasure-progress/result state`;
- `stronger forgetting work != zero medium/endurance cost`;
- `security-provider lifecycle reset != cryptographic erase`;
- `media-encryption-key eradication != physical ciphertext overwrite`;
- `key survival can preserve decryptability across a broader control-state reset`;
- `factory-state reset is not, by category alone, proof of data destruction`."""
replace_once(ev, eng_old, eng_new)

unsupported_old = """- that NVMe 1.3 invented secure erase, crypto erase, sanitization, TRIM-like deallocation, or media sanitization;
- that crypto erase, block erase, and overwrite are physically equivalent;
- that sanitizing an NVMe device establishes application/filesystem/database deletion semantics above the device."""
unsupported_new = """- that NVMe 1.3 invented secure erase, crypto erase, sanitization, TRIM-like deallocation, or media sanitization;
- that TCG Opal 1.0 invented cryptographic erasure or that its standards text proves every named implementation compliant;
- that eradicating one media key proves destruction of every possible external/wrapped/escrowed copy of key material;
- that crypto erase, block erase, and overwrite are physically equivalent;
- that sanitizing an NVMe device establishes application/filesystem/database deletion semantics above the device."""
replace_once(ev, unsupported_old, unsupported_new)

related_old = """`tmzncty/computing-archaeology` was searched before writing for `NVMe sanitize`, `secure erase`, `deallocate`, `TRIM`, and SSD sanitization. No dedicated case was found. Generic Flash/SSD implementation history remains routed there; this record exists because the **retention/forgetting-layer distinction** changes the cross-case argument in `technical-retention`."""
related_new = """`tmzncty/computing-archaeology` was searched before writing for `NVMe sanitize`, `secure erase`, `deallocate`, `TRIM`, SSD sanitization, and again during this deepening for `Opal`, `RevertSP`, and media-encryption-key destruction. No dedicated case was found. Generic Flash/SSD/SED implementation history remains routed there; this record exists because the **retention/forgetting-layer distinction** changes the cross-case argument in `technical-retention`."""
replace_once(ev, related_old, related_new)

# 3) README: keep navigation current without adding a duplicate case.
readme = "README.md"
readme_old = """- [`cases/44-nvme13-deallocate-sanitize-forgetting.md`](cases/44-nvme13-deallocate-sanitize-forgetting.md) — grounded technical-forgetting interface bridge: NVMe 1.3 keeps advisory Dataset-Management deallocation, post-deallocate read semantics, subsystem-wide Sanitize scope, Block/Crypto/Overwrite mechanisms, and background sanitize completion/status separate; NVMe 1.2.1 bounds the earlier Format secure-erase path."""
readme_new = """- [`cases/44-nvme13-deallocate-sanitize-forgetting.md`](cases/44-nvme13-deallocate-sanitize-forgetting.md) — grounded technical-forgetting interface bridge: NVMe 1.3 keeps advisory Dataset-Management deallocation, post-deallocate read semantics, subsystem-wide Sanitize scope, Block/Crypto/Overwrite mechanisms, and background sanitize completion/status separate; NVMe 1.2.1 bounds the earlier Format secure-erase path, while TCG Opal 1.0 (2009) now supplies explicit media-key-eradication prior art and a `KeepGlobalRangeKey` counterexample showing that security-provider reset need not cause cryptographic erase."""
replace_once(readme, readme_old, readme_new)

# 4) ROADMAP: partially advance the previously untouched key-destruction item.
roadmap = "ROADMAP.md"
roadmap_old = "- [ ] key destruction;"
roadmap_new = "- [ ] key destruction — **partially advanced by grounded Case 44 historical deepening**: TCG Opal 1.0 (January 2009) explicitly links media-encryption-key eradication to cryptographic erasure and, through `KeepGlobalRangeKey`, supplies the counterexample that a Locking-SP/factory-state transition can preserve the relevant key and avoid cryptographic erase. Application/file-level key hierarchies, wrapped/escrowed/backup keys, HSM/KMS failure, selective multi-key erasure, key-recovery policy, named-product compliance, and forensic validation remain open;"
replace_once(roadmap, roadmap_old, roadmap_new)

# 5) CASE_INDEX: deepen the canonical row and append bounded cross-case findings.
index = "CASE_INDEX.md"
index_old = """| [NVM Express 1.3 Deallocate and Sanitize: Logical Forgetting, Media Sanitization, and Completion State](cases/44-nvme13-deallocate-sanitize-forgetting.md) | **grounded** | advisory logical-range deallocation + controller allocation/currentness state + subsystem-wide sanitize operation + Block/Crypto/Overwrite mechanisms + retained progress/result status | separate logical deallocation from media erasure; sanitize scope from allocated-LBA scope; request completion from operation completion; and forgotten payload from retained forgetting-status evidence | [2016–2017 NVMe grounding](evidence/44-nvme12-13-deallocate-sanitize-grounding.md); anonymized 2011 raw-flash compliance/forensic validation is now handled separately in Case 47, while ATA/SCSI genealogy, named-controller/device sanitize compliance, later ATA/NVMe implementation validation, and filesystem/database deletion composition remain separate work |"""
index_new = """| [NVM Express 1.3 Deallocate and Sanitize: Logical Forgetting, Media Sanitization, and Completion State](cases/44-nvme13-deallocate-sanitize-forgetting.md) | **grounded** | advisory logical-range deallocation + controller allocation/currentness state + subsystem-wide sanitize operation + Block/Crypto/Overwrite mechanisms + retained progress/result status + earlier media-key-eradication control state | separate logical deallocation from media erasure; sanitize scope from allocated-LBA scope; request completion from operation completion; forgotten payload from retained forgetting-status evidence; and security-provider reset from key destruction | [2009–2017 Opal/NVMe grounding](evidence/44-nvme12-13-deallocate-sanitize-grounding.md); TCG Opal 1.0 now supplies explicit media-key-eradication prior art plus the `KeepGlobalRangeKey` non-erasure counterexample; anonymized 2011 raw-flash compliance/forensic validation remains Case 47, while earlier crypto-erase genealogy, named-product/SED compliance, key hierarchy/escrow, ATA/SCSI genealogy, and application deletion composition remain separate work |"""
replace_once(index, index_old, index_new)

index_text = read(index)
if "1265. **key destruction ≠ ciphertext destruction**" in index_text:
    raise SystemExit("CASE_INDEX already contains Case 44 key-destruction findings")
if "1264. **distributed currentness is a staged relation, not one Boolean**" not in index_text:
    raise SystemExit("CASE_INDEX expected latest finding 1264 was not found")
findings = """

1265. **key destruction ≠ ciphertext destruction** — the bounded Opal/NVMe crypto-erase relation can retire the media key that makes encrypted user data recoverable without requiring the same physical transformation as block erase or overwrite.
1266. **security-provider lifecycle reset ≠ cryptographic erase** — Opal `RevertSP` with `KeepGlobalRangeKey=true` explicitly permits a Locking-SP state transition while preserving the Global-range media key and avoiding cryptographic erase for that range.
1267. **key survival ≠ unchanged security-control state** — the same media key may continue after ownership/Locking-SP state changes, so key continuity and lifecycle/control-state continuity are separate retention relations.
1268. **authentication/locking state ≠ media-encryption-key state** — losing or resetting one control relation does not by itself establish destruction of the other; both must be identified before calling data retained or forgotten.
1269. **cryptographic erasure targets a decryptability relation, not every physical embodiment** — in the bounded encrypted-storage case, removing the relevant key relation can make retained ciphertext unusable without asserting that every media bit was overwritten.
1270. **erase-mechanism identity matters even under one higher-level forgetting objective** — key eradication, block erase, and overwrite can all support sanitization while performing different state transformations and carrying different evidentiary limits.
1271. **retained ciphertext can cease to be admissibly recoverable without physical overwrite** — this is an engineering relation about encrypted storage, not a universal forensic-unrecoverability theorem.
1272. **keeping a key can be an explicit anti-erasure operation** — Opal's `KeepGlobalRangeKey` parameter exists precisely to preserve the relevant media-key relation across a broader Locking-SP transition.
1273. **explicit storage cryptographic-erase prior art is established by January 2009** — TCG Opal 1.0 predates the repository's 2014 NIST and 2016–2017 NVMe witnesses; this is a dated prior-art floor, not an invention-priority claim.
1274. **key state is retention state when payload intelligibility depends on it** — for encrypted storage, whether a ciphertext remains usable depends not only on the surviving media pattern but also on retained key material and the relations that authorize its use.
"""
write(index, index_text.rstrip() + findings + "\n")

# Sanity checks before the workflow commits anything.
checks = {
    case: ["TCG Opal 1.0", "KeepGlobalRangeKey", "security-provider lifecycle reset ≠ cryptographic erase"],
    ev: ["January 27, 2009", "KeepGlobalRangeKey", "direct primary standards PDF text"],
    readme: ["TCG Opal 1.0 (2009)", "KeepGlobalRangeKey"],
    roadmap: ["partially advanced by grounded Case 44 historical deepening", "HSM/KMS"],
    index: ["[2009–2017 Opal/NVMe grounding]", "1265. **key destruction ≠ ciphertext destruction**", "1274. **key state is retention state when payload intelligibility depends on it**"],
}
for path, needles in checks.items():
    text = read(path)
    for needle in needles:
        if needle not in text:
            raise SystemExit(f"{path}: missing expected text {needle!r}")

print("Case 44 TCG Opal key-destruction deepening staged successfully")
