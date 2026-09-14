# FAST ’11 SSD Sanitization Verification: Hidden Flash Remnants, Command Compliance, and Verifiable Forgetting

## Status

**`grounded`** — bounded to Michael Wei, Laura Grupp, Frederick E. Spada, and Steven Swanson’s FAST ’11 empirical study of SSD sanitization, with the authors’ proposed FTL extensions kept explicitly separate as simulated research mechanisms rather than deployed product behavior.

Grounding record: [`../evidence/47-fast11-2011-ssd-sanitization-grounding.md`](../evidence/47-fast11-2011-ssd-sanitization-grounding.md).

Named-device key-store deepening: [`../evidence/47-samsung-840-850-crypto-blob-remanence-deepening.md`](../evidence/47-samsung-840-850-crypto-blob-remanence-deepening.md).

## Scope

This case asks a question deliberately left open by [`44-nvme13-deallocate-sanitize-forgetting.md`](44-nvme13-deallocate-sanitize-forgetting.md):

> A storage specification can define a stronger forgetting operation, but how do we know that an actual SSD implementation has made prior data unavailable below the ordinary logical interface?

Wei et al. answer that question experimentally for a bounded 2011 sample. Their method writes identifiable fingerprints, performs the sanitization operation under test, dismantles the SSD, and reads raw flash through custom hardware rather than trusting the drive’s normal ATA/SCSI view.

The 2019 named-device deepening asks the same verification question for a different forgetting target: controller **key state**. Meijer and van Gastel show that a Samsung 840 EVO could have one current protection configuration while an older key-bearing `crypto blob` still survived in raw NAND because the internal metadata store was wear-leveled.

The bounded relation is:

```text
host-visible value / file
    -> FTL-managed logical-to-physical mapping
    -> out-of-place updates + garbage collection
    -> stale physical embodiments can survive outside current LBA visibility

sanitization request or overwrite
    -> ordinary interface may report deletion / success
    -> experiment bypasses the controller and reads raw flash
    -> surviving fingerprints qualify or falsify the forgetting claim

current encryption/protection state
    -> current key-bearing metadata
    -> older internal metadata revisions may still survive physically
    -> key-store verification must therefore exceed current-state inspection
```

This case is **not**:

- a claim about every SSD in 2011 or every SSD today;
- a named-product compliance audit of the FAST ’11 sample — that paper deliberately labels tested drives `A` through `L` rather than publishing consumer model identities;
- a claim that ATA `SECURITY ERASE UNIT`, ACS-2 `SANITIZE BLOCK ERASE`, NVMe `Sanitize`, TRIM, filesystem deletion, file overwriting, password changes, and TCG Opal key transitions are the same operation;
- a claim that the 2019 Samsung 840 EVO stale-crypto-blob attack directly demonstrates failure of an ATA/NVMe sanitize command — it demonstrates a stale key-bearing metadata path after a protection-state update;
- an analysis of analog remanence after a correctly executed flash erase — FAST ’11 explicitly does not pursue analog erasure further;
- evidence that FAST ’11’s proposed immediate/background/scan-based FTL scrubbing mechanisms shipped in commercial controllers;
- a replacement for Case 44’s later NVMe 1.3 normative interface semantics.

The contribution is a bounded **implementation-verification and hidden-embodiment case**: logical disappearance, raw-flash digital remnants, controller-command reporting, empirical command compliance, stale key-bearing controller metadata, and the difference between a forgetting contract and evidence that a particular implementation actually fulfilled it.

## Relation to Case 44

Case 44 is specification-level. It shows that NVMe 1.3 deliberately separates Deallocate from Sanitize and separately tracks sanitize-operation completion.

Case 47 is empirical and earlier at its core. FAST ’11 shows why a standards-level contract is not enough by itself: in its sample, some drives reported support for ATA security erase yet did not execute the operation reliably, including one tested drive that reported successful sanitization while all data remained intact. The 2019 deepening adds a later empirical reason to inspect cryptographic erase below the current interface state: obsolete key-bearing metadata can itself have hidden physical history.

The cases therefore separate:

```text
interface semantics
    !=
implementation compliance
    !=
current controller security state
    !=
independent residual-state verification evidence
```

No direct genealogy from the 2011 paper to NVMe 1.3 is asserted, and the Samsung 840 EVO evidence is not treated as an NVMe Sanitize experiment.

## Historical vocabulary

The 2011 paper directly uses:

- `sanitize` / `sanitization`;
- `logical sanitization`;
- `digital sanitization`;
- `analog sanitization`;
- `cryptographically sanitize`;
- `digital remnants`;
- `flash translation layer (FTL)`;
- `logical block address (LBA)`;
- `SECURITY ERASE UNIT`;
- `ERASE UNIT ENH`;
- draft ACS-2 `SANITIZE BLOCK ERASE`;
- `TRIM`;
- `fingerprint` for the experiment’s structured test pattern;
- `scrubbing` for the authors’ proposed page-reprogramming mechanism.

The 2019 deepening directly uses `data encryption key (DEK)`, `crypto blob`, `wear leveling`, ATA Security, and TCG Opal. Those later terms are not projected backward into FAST ’11’s historical vocabulary.

`hidden embodiment`, `verification boundary`, `forgetting contract`, `implementation compliance`, `key closure`, and `forensic witness versus current state` are project engineering terms, not the papers’ historical vocabulary.

## Historical record

### H/P — FTL indirection can leave digitally recoverable old versions outside the current logical mapping

The paper explains that SSDs place an indirection layer between host LBAs and physical flash addresses. Out-of-place update changes the logical map to a newly written page while the previous physical page can remain in digital form until later reclamation.

The authors call these old physical versions **`digital remnants`**. In one experiment they created 1,000 small files, dismantled the SSD, and found that some files had as many as **16 stale copies** in flash. The tested SSDs also contained roughly **6–25% more physical flash capacity than their advertised logical capacity**.

Those are measurements of the tested devices, not universal SSD constants.

**Primary anchor:** Wei et al. 2011, §2.2 and Fig. 1.

### H/P — the experiment verifies forgetting below the normal drive interface

The validation procedure deliberately does not infer sanitization from ordinary reads. The researchers:

1. write structured fingerprint records containing generation/LBA/identifier/checksum information;
2. apply the sanitization technique under test;
3. dismantle the drive;
4. access raw flash chips with a custom FPGA-based tester;
5. reconstruct and count surviving fingerprints.

This is the key evidentiary move. A value can be unavailable through the normal ATA/SCSI interface yet remain digitally recoverable from physical flash.

**Primary anchor:** §3.1 and Figs. 2–3.

### H/P — advertised command support and reported success did not guarantee actual sanitization

The authors tested **12 SSDs** for security/sanitize-command support. None supported the then-draft ACS-2 `SANITIZE BLOCK ERASE`. Eight reported ATA SECURITY support; one encrypted its data and could not be verified by the authors’ raw-data method. Of the remaining seven, only four executed `ERASE UNIT` reliably under the tested conditions.

The strongest counterexample is anonymized **Drive B**: it reported that sanitization succeeded, while the experiment found that **all data remained intact** and the filesystem was still mountable. Two other drives had a firmware-state-dependent bug in which the erase command worked only after a recent firmware reset; otherwise only the first LBA was erased, although those drives did report failure.

The paper therefore concludes that command implementations require individual verification before being trusted.

**Primary anchor:** §3.2.1 and Table 1.

### H/P — repeated whole-drive host overwrites were often effective but not uniformly reliable

For eight non-encrypting drives, the authors tested full-LBA-space overwriting. In most tested cases, two full passes removed their fingerprint evidence. But there were exceptions: roughly **1 GB / 1%** of data remained on Drive A after twenty passes, and a commercial four-pass implementation on Drive C left a fingerprint under one initialization condition.

The bounded historical result is therefore not `overwriting SSDs never works`. It is narrower and stronger:

> **host-visible full-range overwrite was not universally reliable as digital sanitization across the tested SSDs.**

**Primary anchor:** §3.2.2 and Table 2.

### H/P — single-file overwrite protocols consistently failed in the tested SSD experiments

The paper tested thirteen single-file overwrite protocols / software methods. It reports that every one failed to remove all targeted data from the tested SSDs. Depending on experiment and technique, recoverable portions remained in raw flash; repeated free-space overwriting also left substantial old data.

The paper attributes the basic problem to FTL indirection: rewriting the current LBA does not ensure that every older physical page that previously held the file is overwritten or erased.

This is a device/controller-level problem below a filesystem’s current allocation view.

**Primary anchor:** §3.3, Tables 3–4.

### H/P — TRIM/current allocation information was not treated as a sanitization guarantee

In a footnote to the single-file discussion, the paper notes that the then-draft ACS-2 TRIM mechanism informs the drive that LBAs are no longer in use but states that this has no reliable effect on data security.

That period observation is compatible with — but not identical to — Case 44’s later NVMe distinction between Deallocate and Sanitize.

**Primary anchor:** §3.3, note 2.

### H/P — a hard-drive destruction technique can fail because the storage substrate is different

The researchers also exposed seven flash chips to a hard-drive degausser. The data remained intact in all tested chips. The point is not a universal claim about every destructive process; it is that a mechanism effective against magnetic recording does not automatically erase floating-gate flash.

**Primary anchor:** §3.2.3.

### H/P — the proposed file-sanitizing FTL extensions are research mechanisms, not product evidence

The paper proposes immediate, background, and scan-based `scrubbing` extensions to an FTL. They are implemented in a trace-based simulator and evaluated using measured flash characteristics.

The paper itself records important costs and limits: background scrubbing can leave a temporary remnant window; scrubbing competes for flash service; MLC devices can have limited scrub budgets; increased erase activity can increase wear and reduce retention margins.

These mechanisms are useful experiments demonstrating possible implementation tradeoffs. They are **not evidence that the twelve commercial SSDs tested in §3 implemented them**.

**Primary anchors:** §§4.2–4.4.

### H/P — a later named-device study found stale key-bearing metadata below the current protection state

Meijer and van Gastel’s 2019 IEEE Security & Privacy study reverse-engineered named self-encrypting SSDs. For the Samsung 840 EVO they identify a 64 KiB internal NAND `crypto blob` carrying encryption state. In their demonstrated transition, an unprotected blob containing the DEK existed at one physical location; after password protection was configured, an updated protected blob could be written at another location because the internal metadata store was wear-leveled.

The researchers report successfully recovering a previous crypto-blob revision and making it active through a vendor-specific command path. They measured old/new physical locations differing in roughly one out of twenty crypto-state updates in their setup, and observed the stale location eventually being overwritten under later use.

The bounded historical result is:

> **a current protected state did not by itself prove that every older key-bearing NAND representation had already disappeared.**

This is not a direct sanitize-command failure experiment.

**Primary anchor:** Meijer & van Gastel 2019, §VI-E.

### H/P — Samsung 850 EVO provides a bounded negative control for that specific placement mechanism

The same paper reports that Samsung told the researchers that from the 850 EVO onward the crypto blob was no longer wear-leveled and instead occupied a fixed physical NAND address. The authors therefore say the 850 EVO was not vulnerable to the **same wear-leveling crypto-blob recovery attack**.

That narrows the mechanism:

```text
same broad key-management function
    + different metadata-placement policy
    -> different stale-copy exposure for this attack
```

It does not establish that the 850 EVO is secure against every other key-management or erase failure.

**Primary anchor:** Meijer & van Gastel 2019, §VI-F.

## Retained state and forgetting target

The case contains several distinct state classes:

1. **current host-visible LBA value** — what ordinary reads resolve through the controller;
2. **FTL mapping state** — which physical page currently answers for an LBA;
3. **stale physical page embodiments** — old values no longer current through the FTL but still present in digital form;
4. **over-provision / spare-area contents** — physical flash not directly enumerable as host LBAs;
5. **controller command-support/reporting state** — what the device says it supports and whether it reports an erase as successful;
6. **experimental fingerprint evidence** — an external verification witness used after bypassing the controller;
7. **active encryption-key state** — the currently authoritative DEK or equivalent key relationship;
8. **password/key-wrapping metadata** — state governing access to or protection of the DEK;
9. **obsolete key-bearing metadata embodiments** — earlier crypto-blob revisions that can survive outside the controller’s current protection-state view;
10. **internal placement/reclamation state** — wear-leveling and later overwrite history that determines whether a stale key witness still exists.

The forgetting target must therefore be named. `The file disappeared`, `the LBA no longer returns the old value`, `the controller reported erase success`, `the current DEK changed`, and `no usable old payload/key witness remained below the interface` are different claims.

## Access geometry and verification boundary

Normal host access is:

```text
LBA
    -> controller / FTL
    -> current mapped physical page
```

The FAST ’11 experiment intentionally changes the observation path:

```text
raw flash chip pins
    -> custom FPGA tester
    -> scan for fingerprint structure
    -> reconstruct surviving old data
```

The 2019 key-store deepening changes it again:

```text
raw/internal controller state
    -> reverse engineering / low-level access
    -> recover obsolete crypto-blob revision
    -> test whether stale key-bearing state remains actionable
```

This produces one of the case’s strongest distinctions:

> **ordinary interface inaccessibility ≠ absence of a lower-layer digital witness**.

It also prevents a false conclusion in the other direction. A surviving raw-flash witness is evidence about the stated forgetting target and attacker layer, but it is not automatically the current logical value or an ordinary host-accessible state.

## Failure and forgetting modes

Keep separate:

- **filesystem deletion** — removes or changes software-level reference/currentness;
- **logical overwrite** — writes a new value to a host-visible address;
- **FTL remapping** — changes which physical page answers for that LBA;
- **garbage collection** — may later erase blocks containing stale data, on the controller’s own schedule;
- **ATA command implementation failure** — controller claims or attempts sanitization incorrectly;
- **partial/conditional erase bug** — operation behavior depends on firmware state and may cover only a subset of logical space;
- **whole-drive host overwrite miss** — repeated logical coverage does not guarantee physical coverage of every remnant;
- **single-file overwrite miss** — current file LBAs are overwritten while stale physical copies survive elsewhere;
- **cryptographic sanitization uncertainty** — ciphertext can remain while security depends on the key store actually being sanitized;
- **stale key-metadata remanence** — current protection state changes while an obsolete key-bearing physical representation remains recoverable;
- **analog remanence** — a different attack layer not experimentally resolved by this case.

These are not one generic event called `delete failure`.

## Engineering reconstruction

### E — logical disappearance is weaker than digital sanitization

The paper explicitly distinguishes logical from digital sanitization and empirically recovers old data after ordinary-interface operations have made it noncurrent.

Therefore:

> **logical invisibility ≠ digital sanitization**.

### E — command success reporting is weaker than verified forgetting

Drive B reported successful sanitization while all data remained.

Therefore:

> **reported erase success ≠ verified media sanitization**.

And more generally:

> **interface contract ≠ implementation compliance**.

This is the empirical complement to Case 44.

### E — host address coverage is weaker than physical embodiment coverage

A host can overwrite every visible LBA yet fail to overwrite stale pages in spare or remapped physical regions.

Therefore:

> **complete logical-address overwrite ≠ complete physical-witness overwrite**.

The exact probability depends on controller behavior and workload history; the paper’s measured failures are not universal percentages.

### E — current logical singularity can coexist with physical historical multiplicity

The FTL exposes one current value for an LBA while several old physical versions can survive.

Therefore:

> **one current logical value ≠ one surviving physical embodiment**.

This is not `version history` in the application sense. The old copies are controller by-products, not an intentional archive.

### E — whole-device sanitization and selective-file sanitization are different engineering problems

A controller can erase an entire device more easily than it can destroy every historical embodiment of one selected file while preserving unrelated live data.

Therefore:

> **whole-device forgetting capability ≠ selective forgetting capability**.

### E — verification may require a different observation layer from ordinary use

If the ordinary interface is the mechanism hiding stale locations, asking only that interface whether the stale data exists cannot fully test digital sanitization.

Therefore:

> **service-interface evidence ≠ raw-media verification evidence**.

This does not imply that every verification method must physically dismantle a device. It records the bounded methods used in the cited studies and the epistemic problem they expose.

### E — physical destruction technique is substrate-relative

The degaussing result is a direct counterexample to treating `destroy storage` as a mechanism-independent instruction.

Therefore:

> **sanitization objective continuity ≠ sanitization mechanism portability across media**.

### E — stronger forgetting work can consume retention margin

The proposed scrubbing experiments show that page reprogramming can introduce errors, trigger extra erases, increase wear, and reduce long-term retention margin on some flash devices.

Therefore:

> **forgetting work can compete with future retention work**.

This is grounded only for the measured/reconstructed mechanisms in the paper, not as a universal quantitative law.

### E — cryptographic erase moves the forgetting obligation into the key store

If ciphertext may remain after cryptographic erasure, the old plaintext is forgotten only insofar as the old DEK and every usable route back to it are irrecoverable under the chosen threat model.

Therefore:

```text
ciphertext physically remains
    != cryptographic forgetting failed

current DEK changed
    != cryptographic forgetting verified
```

A stronger bounded assurance chain is:

```text
fresh-key transition
    + sufficient new-key entropy
    + old key no longer authoritative
    + obsolete usable key-bearing copies retired
    + no alternate credential/key path restoring old access
```

The 2019 Samsung study directly demonstrates why the obsolete-copy term matters; it does not prove that this list is a universal formal specification.

### E — current security state can coexist with obsolete physical key state

The 840 EVO attack shows the controller can have one current protection configuration while an older crypto-blob revision still exists below that logical state.

Therefore:

> **one current key/protection state ≠ one surviving physical key-state embodiment**.

This is a key-metadata analogue of the stale-payload multiplicity already documented by FAST ’11, but the retained object and recovery mechanism are different.

### E — later overwrite can close a stale-key window without validating the original transition

The 2019 study observed eventual overwriting of stale 840 EVO crypto blobs during subsequent use.

Therefore:

```text
later reclamation destroys stale key state
    != original protection transition destroyed it immediately
```

That distinction matters whenever an erase/sanitize guarantee is supposed to hold at command completion rather than after an unspecified later workload.

## Cross-case comparison

### Case 04 — mapped Flash

Case 04 establishes that logical currentness can move to a new physical block before the old embodiment is erased. Case 47 supplies direct empirical evidence that later SSD FTL behavior can leave many digitally recoverable stale embodiments below the host map.

Therefore:

> `logical remapping` and `forensic/raw-media survivability` are related but distinct retention relations.

No claim is made that the 1993 patent architecture is identical to the 2011 test drives.

### Case 44 — NVMe Deallocate / Sanitize

Case 44 is a normative 2017 interface case. Case 47 is an empirical verification case spanning FAST ’11 and the later 2019 named-device deepening.

Together they justify a four-layer comparison:

```text
specified forgetting semantics
    !=
controller-reported operation result
    !=
current key/protection state
    !=
independently observed residual state
```

The Samsung 840 EVO stale-blob attack is not evidence that an NVMe Sanitize command failed.

### Case 37 — Samsung 840 EVO old-data performance refresh

Case 37 concerns old-data read performance / recovery behavior in the Samsung 840 EVO family. The 2019 evidence here concerns encryption metadata and a stale crypto blob.

Sharing the model family does not establish mechanism identity, causal connection, or common remediation.

### Synthesis 22 — erase / invalidation / sanitization / verification

[`../docs/SYNTHESIS_22_ERASE_INVALIDATION_SANITIZATION_VERIFICATION.md`](../docs/SYNTHESIS_22_ERASE_INVALIDATION_SANITIZATION_VERIFICATION.md) distinguishes forgetting operation semantics from evidence that residual state is actually gone.

The 2019 key-store result sharpens that verification layer:

> **proof that the active key changed ≠ proof that every usable old-key witness disappeared**.

### Kirschenbaum / forensic-materiality test

The existing philosophical test already warns that a physical witness is not necessarily authoritative current state. Case 47 strengthens the technical side of that warning: raw-flash remnants can be recoverable after the FTL or key-management layer has ceased to expose them as current logical state.

The case does **not** conclude that all deleted SSD data or old key material remains recoverable indefinitely. Garbage collection, block erase, sanitization, encryption, wear, later controller behavior, and metadata-placement policy can eliminate or transform those witnesses.

## Functional analogy and philosophical limit

A bounded functional analogy describes sanitization as **technical forgetting**, but only after the target and attack/observation layer are specified.

The engineering evidence supports this narrow statement:

> A system can have stopped presenting a value or key relation as current while still retaining lower-layer material conditions from which that earlier state can be reconstructed.

Cryptographic erasure adds a second project-level interpretation: forgetting can act on the **decoding relation** rather than every payload-bearing physical bit. If ciphertext is intentionally retained, then the key relation becomes a privileged retention object whose old embodiments matter to the forgetting claim.

That is project interpretation, not historical vocabulary from the cited authors. It does not establish claims about human forgetting, repression, institutional oblivion, or cultural memory. Nor does it prove that every physical trace should count as the same object for every purpose.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| 2011 tested SSDs used FTL indirection that could leave old physical data outside current LBA visibility | H/P | Wei et al. §§1–2.2 |
| the experiment verified sanitization by direct raw-flash extraction after dismantling drives | H/P | §3.1 |
| one tested drive reported successful sanitization while all data remained and the filesystem remained mountable | H/P | §3.2.1 / Table 1 |
| whole-LBA-space overwrite was often but not universally successful in the tested drives | H/P | §3.2.2 / Table 2 |
| every tested single-file overwrite protocol left recoverable data in at least some tested SSD experiments | H/P | §3.3 / Tables 3–4 |
| `logical invisibility != digital sanitization` | E | paper’s explicit taxonomy + raw-flash experiments |
| `reported erase success != verified media sanitization` | E | Drive B counterexample |
| `one current logical value != one surviving physical embodiment` | E | FTL mechanism + stale-copy measurement |
| Samsung 840 EVO could retain an older unprotected crypto-blob revision after current protection metadata was updated | H/P | Meijer & van Gastel 2019 §VI-E |
| the 840 EVO stale-blob attack was demonstrated with low-level recovery and a vendor-specific reactivation path | H/P | Meijer & van Gastel 2019 §VI-E |
| Samsung reported 850 EVO and later used fixed-address rather than wear-leveled crypto-blob storage, removing that specific stale-placement attack | H/P | Meijer & van Gastel 2019 §VI-F; bounded vendor statement through paper |
| `current key/protection state != complete set of physically retained key-bearing states` | E | 840 EVO stale-blob demonstration |
| the paper’s proposed scrub-enabled FTL shipped commercially | X | not established; evaluated in a simulator |
| the twelve FAST ’11 SSD labels identify named commercial models | X | identities are anonymized A–L |
| the papers prove universal modern NVMe sanitize failure | X | outside date, interface, sample, and command-path scope |
| Samsung 840 EVO sanitize was directly shown to fail by the 2019 stale-blob experiment | X | not established; protection-state transition is not a sanitize-command trace |
| fixed-address 850 EVO metadata proves complete sanitization security | X | not established |

## Sources

### Primary / contemporaneous

- Michael Wei, Laura Grupp, Frederick E. Spada, Steven Swanson, **“Reliably Erasing Data From Flash-Based Solid State Drives,”** *FAST ’11: 9th USENIX Conference on File and Storage Technologies*, February 2011: <https://www.usenix.org/conference/fast11/reliably-erasing-data-flash-based-solid-state-drives>
- Open-access conference PDF: <https://static.usenix.org/event/fast11/tech/full_papers/Wei.pdf>
- Richard Kissel, Matthew Scholl, Steven Skolochenko, Xing Li, **NIST SP 800-88, Guidelines for Media Sanitization**, September 2006: <https://csrc.nist.gov/pubs/sp/800/88/upd1/final>

### Later named-device deepening

- Carlo Meijer and Bernard van Gastel, **“Self-Encrypting Deception: Weaknesses in the Encryption of Solid State Drives,”** *2019 IEEE Symposium on Security and Privacy*, pp. 72–87, DOI `10.1109/SP.2019.00088`: <https://www.cs.ru.nl/~cmeijer/publications/Self_Encrypting_Deception_Weaknesses_in_the_Encryption_of_Solid_State_Drives.pdf>
- Open Universiteit research portal bibliographic record: <https://research.ou.nl/en/publications/self-encrypting-deception-weaknesses-in-the-encryption-of-solid-s/>

### Related internal cases

- [`04-flash-virtual-mapping-logical-identity.md`](04-flash-virtual-mapping-logical-identity.md)
- [`37-samsung-840-evo-old-data-performance-refresh.md`](37-samsung-840-evo-old-data-performance-refresh.md)
- [`44-nvme13-deallocate-sanitize-forgetting.md`](44-nvme13-deallocate-sanitize-forgetting.md)
- [`../docs/SYNTHESIS_22_ERASE_INVALIDATION_SANITIZATION_VERIFICATION.md`](../docs/SYNTHESIS_22_ERASE_INVALIDATION_SANITIZATION_VERIFICATION.md)
- [`../docs/PHILOSOPHICAL_TEST_04_KIRSCHENBAUM_FORENSIC_MATERIALITY.md`](../docs/PHILOSOPHICAL_TEST_04_KIRSCHENBAUM_FORENSIC_MATERIALITY.md)

## Next work

- extend named-product / named-controller sanitization-compliance evidence beyond the 840/850 key-store deepening, especially where firmware revisions and exact erase/sanitize command paths are recoverable;
- later ATA SANITIZE and NVMe Sanitize implementation studies;
- direct cryptographic-erase experiments that execute a named sanitize/key-regeneration path and then independently search every relevant key store for usable old key material;
- controller-hidden-area and over-provisioning forensics across newer NAND generations;
- secure-delete composition with filesystems, databases, encryption layers, and cloud lifecycle policy;
- analog-remanence work kept separate from FAST ’11’s digital-remnant experiments.