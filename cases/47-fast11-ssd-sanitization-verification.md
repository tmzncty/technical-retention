# FAST ’11 SSD Sanitization Verification: Hidden Flash Remnants, Command Compliance, and Verifiable Forgetting

## Status

**`grounded`** — bounded to Michael Wei, Laura Grupp, Frederick E. Spada, and Steven Swanson’s FAST ’11 empirical study of SSD sanitization, with the authors’ proposed FTL extensions kept explicitly separate as simulated research mechanisms rather than deployed product behavior.

Grounding record: [`../evidence/47-fast11-2011-ssd-sanitization-grounding.md`](../evidence/47-fast11-2011-ssd-sanitization-grounding.md).

## Scope

This case asks a question deliberately left open by [`44-nvme13-deallocate-sanitize-forgetting.md`](44-nvme13-deallocate-sanitize-forgetting.md):

> A storage specification can define a stronger forgetting operation, but how do we know that an actual SSD implementation has made prior data unavailable below the ordinary logical interface?

Wei et al. answer that question experimentally for a bounded 2011 sample. Their method writes identifiable fingerprints, performs the sanitization operation under test, dismantles the SSD, and reads raw flash through custom hardware rather than trusting the drive’s normal ATA/SCSI view.

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
```

This case is **not**:

- a claim about every SSD in 2011 or every SSD today;
- a named-product compliance audit — the paper deliberately labels tested drives `A` through `L` rather than publishing consumer model identities;
- a claim that ATA `SECURITY ERASE UNIT`, ACS-2 `SANITIZE BLOCK ERASE`, NVMe `Sanitize`, TRIM, filesystem deletion, and file overwriting are the same operation;
- an analysis of analog remanence after a correctly executed flash erase — the paper explicitly does not pursue analog erasure further;
- evidence that the paper’s proposed immediate/background/scan-based FTL scrubbing mechanisms shipped in commercial controllers;
- a replacement for Case 44’s later NVMe 1.3 normative interface semantics.

The contribution is a bounded **implementation-verification and hidden-embodiment case**: logical disappearance, raw-flash digital remnants, controller-command reporting, empirical command compliance, and the difference between a forgetting contract and evidence that a particular implementation actually fulfilled it.

## Relation to Case 44

Case 44 is specification-level. It shows that NVMe 1.3 deliberately separates Deallocate from Sanitize and separately tracks sanitize-operation completion.

Case 47 is empirical and earlier. It shows why a standards-level contract is not enough by itself: in the FAST ’11 sample, some drives reported support for ATA security erase yet did not execute the operation reliably, including one tested drive that reported successful sanitization while all data remained intact.

The cases therefore separate:

```text
interface semantics
    !=
implementation compliance
    !=
independent verification evidence
```

No direct genealogy from the 2011 paper to NVMe 1.3 is asserted.

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

`hidden embodiment`, `verification boundary`, `forgetting contract`, `implementation compliance`, and `forensic witness versus current state` are project engineering terms, not the paper’s historical vocabulary.

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

## Retained state and forgetting target

The case contains several distinct state classes:

1. **current host-visible LBA value** — what ordinary reads resolve through the controller;
2. **FTL mapping state** — which physical page currently answers for an LBA;
3. **stale physical page embodiments** — old values no longer current through the FTL but still present in digital form;
4. **over-provision / spare-area contents** — physical flash not directly enumerable as host LBAs;
5. **controller command-support/reporting state** — what the device says it supports and whether it reports an erase as successful;
6. **experimental fingerprint evidence** — an external verification witness used after bypassing the controller;
7. **encryption-key state** — relevant to cryptographic sanitization, but not directly verifiable by the authors for the encrypted test drive.

The forgetting target must therefore be named. `The file disappeared`, `the LBA no longer returns the old value`, `the controller reported erase success`, and `no old fingerprint remained in raw flash` are four different claims.

## Access geometry and verification boundary

Normal host access is:

```text
LBA
    -> controller / FTL
    -> current mapped physical page
```

The experiment intentionally changes the observation path:

```text
raw flash chip pins
    -> custom FPGA tester
    -> scan for fingerprint structure
    -> reconstruct surviving old data
```

This produces one of the case’s strongest distinctions:

> **ordinary interface inaccessibility ≠ absence of a lower-layer digital witness**.

It also prevents a false conclusion in the other direction. A surviving raw-flash witness is evidence that digital sanitization failed under the paper’s definition, but it is not automatically the current logical value of the SSD.

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

This does not imply that every verification method must physically dismantle a device. It records the bounded method used in 2011 and the epistemic problem it exposes.

### E — physical destruction technique is substrate-relative

The degaussing result is a direct counterexample to treating `destroy storage` as a mechanism-independent instruction.

Therefore:

> **sanitization objective continuity ≠ sanitization mechanism portability across media**.

### E — stronger forgetting work can consume retention margin

The proposed scrubbing experiments show that page reprogramming can introduce errors, trigger extra erases, increase wear, and reduce long-term retention margin on some flash devices.

Therefore:

> **forgetting work can compete with future retention work**.

This is grounded only for the measured/reconstructed mechanisms in the paper, not as a universal quantitative law.

## Cross-case comparison

### Case 04 — mapped Flash

Case 04 establishes that logical currentness can move to a new physical block before the old embodiment is erased. Case 47 supplies direct empirical evidence that later SSD FTL behavior can leave many digitally recoverable stale embodiments below the host map.

Therefore:

> `logical remapping` and `forensic/raw-media survivability` are related but distinct retention relations.

No claim is made that the 1993 patent architecture is identical to the 2011 test drives.

### Case 44 — NVMe Deallocate / Sanitize

Case 44 is a normative 2017 interface case. Case 47 is an empirical 2011 ATA-era compliance/verification case.

Together they justify a three-layer comparison:

```text
specified forgetting semantics
    !=
controller-reported operation result
    !=
independently observed residual state
```

### Kirschenbaum / forensic-materiality test

The existing philosophical test already warns that a physical witness is not necessarily authoritative current state. Case 47 strengthens the technical side of that warning: raw-flash remnants can be recoverable after the FTL has ceased to expose them as current logical data.

The case does **not** conclude that all deleted SSD data remains recoverable indefinitely. Garbage collection, block erase, sanitization, encryption, wear, and later controller behavior can eliminate or transform those witnesses.

## Functional analogy and philosophical limit

A bounded functional analogy describes sanitization as **technical forgetting**, but only after the target and attack/observation layer are specified.

The engineering evidence supports this narrow statement:

> A system can have stopped presenting a value as current while still retaining lower-layer material conditions from which that value can be reconstructed.

It does not establish claims about human forgetting, repression, institutional oblivion, or cultural memory. Nor does it prove that every physical trace should count as the same object for every purpose.

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
| the paper’s proposed scrub-enabled FTL shipped commercially | X | not established; evaluated in a simulator |
| the twelve SSD labels identify named commercial models | X | identities are anonymized A–L |
| the paper proves universal modern NVMe sanitize failure | X | outside date, interface, and sample scope |

## Sources

### Primary / contemporaneous

- Michael Wei, Laura Grupp, Frederick E. Spada, Steven Swanson, **“Reliably Erasing Data From Flash-Based Solid State Drives,”** *FAST ’11: 9th USENIX Conference on File and Storage Technologies*, February 2011: <https://www.usenix.org/conference/fast11/reliably-erasing-data-flash-based-solid-state-drives>
- Open-access conference PDF: <https://static.usenix.org/event/fast11/tech/full_papers/Wei.pdf>
- Richard Kissel, Matthew Scholl, Steven Skolochenko, Xing Li, **NIST SP 800-88, Guidelines for Media Sanitization**, September 2006: <https://csrc.nist.gov/pubs/sp/800/88/upd1/final>

### Related internal cases

- [`04-flash-virtual-mapping-logical-identity.md`](04-flash-virtual-mapping-logical-identity.md)
- [`44-nvme13-deallocate-sanitize-forgetting.md`](44-nvme13-deallocate-sanitize-forgetting.md)
- [`../docs/PHILOSOPHICAL_TEST_04_KIRSCHENBAUM_FORENSIC_MATERIALITY.md`](../docs/PHILOSOPHICAL_TEST_04_KIRSCHENBAUM_FORENSIC_MATERIALITY.md)

## Next work

- named-product / named-controller sanitization-compliance evidence, especially where firmware versions and exact command paths are recoverable;
- later ATA SANITIZE and NVMe Sanitize implementation studies;
- cryptographic-erase verification, including key-store scope and recoverability;
- controller-hidden-area and over-provisioning forensics across newer NAND generations;
- secure-delete composition with filesystems, databases, encryption layers, and cloud lifecycle policy;
- analog-remanence work kept separate from this paper’s digital-remnant experiments.