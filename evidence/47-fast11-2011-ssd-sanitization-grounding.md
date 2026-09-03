# Case 47 grounding record — FAST ’11 SSD sanitization verification, 2011

## Status

**Grounding record for Case 47.**

Case: [`../cases/47-fast11-ssd-sanitization-verification.md`](../cases/47-fast11-ssd-sanitization-verification.md).

This record grounds a narrow empirical forgetting/compliance case in Michael Wei, Laura Grupp, Frederick E. Spada, and Steven Swanson’s FAST ’11 paper. The central evidence is an independent research experiment that bypassed tested SSD controllers and extracted raw digital data directly from flash chips after sanitization attempts.

The record deliberately separates:

1. the paper’s **observations on twelve anonymized commercial SSDs**;
2. the paper’s **experimental validation method**;
3. the authors’ **simulated FTL extensions** for selective sanitization;
4. earlier NIST sanitization policy vocabulary;
5. later NVMe interface semantics already covered in Case 44.

It does not convert an anonymized 2011 test sample into a named-product audit or into evidence about every modern SSD.

## Research question

> When a host-visible file or LBA no longer exposes an old value, or a drive reports that an erase command succeeded, what evidence is required to establish that old digital embodiments are actually gone from controller-hidden flash locations?

The bounded experiment supplies a particularly strong counterexample chain:

```text
host / filesystem / ATA-visible result
    -> may indicate deletion, overwrite, or erase success

raw flash after dismantling drive
    -> may still contain identifiable old fingerprints

therefore
    -> logical disappearance or controller reporting alone is not sufficient evidence of digital sanitization
```

## Evidence set and role separation

### E1 — Wei et al., FAST ’11

**Source:** Michael Wei, Laura Grupp, Frederick E. Spada, Steven Swanson, “Reliably Erasing Data From Flash-Based Solid State Drives,” *9th USENIX Conference on File and Storage Technologies (FAST ’11)*, February 2011.

- USENIX conference record: <https://www.usenix.org/conference/fast11/reliably-erasing-data-flash-based-solid-state-drives>
- Open-access PDF: <https://static.usenix.org/event/fast11/tech/full_papers/Wei.pdf>

**Role:** primary peer-reviewed empirical evidence for FTL-created digital remnants, raw-flash verification methodology, whole-device secure-erase command behavior, overwrite experiments, single-file sanitization failures, degaussing results, and the boundary between empirical commercial-drive observations and simulated FTL proposals.

**Inspection in this slice:**

- the PDF was opened directly and its first page was rendered visually, confirming title/authorship and the abstract’s three principal empirical conclusions;
- page-level text was inspected for §2.1–§2.2, §3.1–§3.4, Tables 1–4, §4.1–§4.4, and the conclusion;
- later table/result pages were not treated as visual-layout evidence where the rendering endpoint was unavailable; claims below use the paper’s parsed printed-page text and explicit table captions/rows.

### E2 — USENIX conference publication record

**Source:** USENIX, “Reliably Erasing Data from Flash-Based Solid State Drives.”

URL: <https://www.usenix.org/conference/fast11/reliably-erasing-data-flash-based-solid-state-drives>

**Role:** institutional bibliographic anchor for authorship, FAST ’11 venue, year, and open-access publication identity. It is not used instead of E1 for mechanism or result claims.

### E3 — NIST SP 800-88, 2006

**Source:** Richard Kissel, Matthew Scholl, Steven Skolochenko, Xing Li, *Guidelines for Media Sanitization*, NIST Special Publication 800-88, September 2006.

- NIST publication record: <https://csrc.nist.gov/pubs/sp/800/88/upd1/final>

**Role:** earlier institutional vocabulary and policy context. NIST’s 2006 guide treats media sanitization as removal such that residual data cannot be easily retrieved/reconstructed and uses the `clear` / `purge` distinction cited by Wei et al.

**Boundary:** E3 does not prove how any SSD controller implemented secure erase. It is used to prevent the paper’s `sanitization` framing from being misread as an invention of the term or objective in 2011.

## E1 exact anchors

### E1-A — FTL indirection and `digital remnants`

**Printed pp. 105–107 in the FAST ’11 proceedings / PDF pp. 1–3, §1 and §2.2.**

The paper explains that SSDs maintain an indirection layer between host-visible LBAs and raw flash addresses. Because a rewritten LBA is normally placed in a new physical page and the mapping is updated, the old physical page can remain in digital form.

The paper calls these leftover old physical versions **`digital remnants`**.

The same section reports two sample-specific observations:

- tested SSDs had roughly **6–25% more physical flash capacity** than advertised logical capacity;
- in an experiment that wrote 1,000 small files, some files had up to **16 stale copies** in raw flash, attributed to out-of-place update and garbage-collection behavior.

**Claims grounded:**

- current logical addressability does not enumerate every surviving physical embodiment;
- one host-visible value can coexist with stale digital copies below the FTL;
- the tested values are sample measurements, not universal constants.

### E1-B — the paper explicitly separates logical and digital sanitization

**PDF p. 2, §2.1.**

Wei et al. define `logical sanitization` as making data unavailable through standard hardware interfaces and `digital sanitization` as making data unrecoverable by digital means including undocumented commands or controller/firmware subversion. They separately discuss analog and cryptographic sanitization.

The paper then states that SSD overwriting can achieve logical sanitization while failing digital sanitization because an old physical page may remain.

**Claims grounded:**

- `logical invisibility ≠ digital sanitization` is not merely our retrospective vocabulary; it is a bounded reconstruction supported by the authors’ own 2011 taxonomy and mechanism description;
- analog sanitization is a separate layer that the paper explicitly declines to investigate further.

### E1-C — verification bypasses the normal controller interface

**PDF p. 4, §3.1.**

The experiment writes structured fingerprints, applies the sanitization method, dismantles the drive, then uses an FPGA/Linux flash tester to access raw chips. Fingerprints include generation/LBA/identifier/checksum structure that helps reconstruct and count remnants even when drives interleave or invert stored data.

**Claims grounded:**

- the evidence is independent of ordinary post-erase ATA/SCSI reads;
- sanitization success is tested against lower-level physical flash contents;
- `service-interface evidence ≠ raw-media verification evidence` is a bounded engineering reconstruction.

### E1-D — built-in command compliance varied, including false success

**PDF pp. 4–5, §3.2.1 and Table 1.**

The paper tested **12 SSDs**, anonymized `A` through `L`.

- none supported the then-draft ACS-2 `SANITIZE BLOCK ERASE`;
- eight reported ATA SECURITY support;
- one encrypted drive could not be verified by the authors’ raw-data technique;
- among the other seven, only four executed `ERASE UNIT` reliably under the tested conditions;
- Drive B reported successful sanitization while all data remained intact and the filesystem was still mountable;
- two other drives had a firmware-state-dependent bug that could reduce the erase to the first LBA, although those drives reported failure.

**Claims grounded:**

- reported feature support is weaker than verified behavior;
- command completion/success reporting can be wrong in an implementation;
- individual implementation testing can reveal failure modes invisible in the normative command name.

**Scope boundary:** the paper does not publish consumer model names for `A`–`L`. This evidence must not be rewritten as a named-controller result.

### E1-E — whole-address-space overwrite was not uniformly reliable

**PDF pp. 5–6, §3.2.2 and Table 2.**

In most tested non-encrypting-drive cases, two full overwrite passes removed the experimental fingerprints. But the paper reports exceptions:

- about **1 GB / 1%** remained on Drive A after twenty passes;
- a commercial four-pass 5220.22-M implementation on Drive C removed all data under sequential initialization but left one fingerprint under random initialization.

The authors characterize the aggregate overwrite result as poor for a sanitization guarantee because success was not universal.

**Claims grounded:**

- `whole visible address-space coverage ≠ guaranteed physical-remnant coverage`;
- the paper does **not** support the opposite universal claim that repeated whole-drive overwriting never works on SSDs.

### E1-F — single-file overwrite methods failed in the tested SSD experiments

**PDF pp. 6–7, §3.3 and Tables 3–4.**

The authors tested thirteen single-file overwrite protocols/software methods. Their text states that all of them failed; recoverable data remained on the SATA SSD experiments. Repeated free-space overwrite also left most target data on the tested Drive C under the reported setups.

A footnote notes that draft ACS-2 `TRIM` informs the drive that LBA ranges are no longer in use but does not provide a reliable data-security effect in the paper’s bounded discussion.

**Claims grounded:**

- file-level logical overwrite does not reliably reach every stale physical page that previously embodied that file;
- allocation/deallocation information is not itself evidence of digital sanitization;
- whole-device and selective-file sanitization are different engineering problems.

### E1-G — degaussing did not erase the tested flash chips

**PDF p. 6, §3.2.3.**

Seven flash chips spanning SLC/MLC/TLC types were exposed to the described hard-drive degausser fields. In all tested chips the data remained intact.

**Claim grounded:**

- a sanitization technique effective against magnetic-media state does not automatically transfer to floating-gate flash.

**Boundary:** this is not a claim that no sufficiently destructive electromagnetic process could ever damage flash electronics; it is the reported result of the specified test.

### E1-H — encryption offers a different forgetting relation but was not independently verified for the encrypted drive

**PDF p. 6, §3.2.4.**

The paper describes cryptographic sanitization as deleting the key needed to make ciphertext accessible. For encrypted Drive E, the authors could not verify whether key material had actually been erased. They explicitly identify key-store sanitization as an implementation trust problem.

**Claims grounded:**

- cryptographic forgetting may preserve ciphertext while changing the interpretation/access key relation;
- a fast apparent erase path is not, by itself, evidence that key-store sanitization succeeded.

### E1-I — proposed FTL `scrubbing` is simulation-backed research, not deployed commercial behavior

**PDF pp. 8–12, §§4.2–4.4.**

The paper proposes reprogramming stale pages toward zero (`scrubbing`) and evaluates immediate, background, and scan-based variants in a trace-based FTL simulator using measured flash characteristics.

The paper itself records several limits:

- some MLC chips exhibit disturb/error behavior after small numbers of scrubs;
- paired-page effects can require relocating otherwise valid data;
- immediate scrubbing can increase write latency;
- background scrubbing can leave a temporary remnant window and compete with foreground requests;
- extra erases increase wear and can reduce future data-retention margin.

**Claims grounded:**

- selective sanitization can impose latency, bandwidth, wear, and future-retention costs;
- `forgetting work can compete with retention work` is a bounded engineering relation;
- these designs are research proposals evaluated in simulation, not evidence of deployment in Drives A–L.

## Evidence ledger

| Claim | Type | Evidence | Status |
| --- | --- | --- | --- |
| FTL out-of-place updates can leave old physical versions after current mapping moves | `H/P` | E1 §2.2 | strong |
| the authors found up to 16 stale copies of some files in one tested SSD experiment | `H/P` | E1 Fig. 1 / §2.2 | strong, sample-specific |
| raw-flash fingerprint extraction was used to verify digital sanitization | `H/P` | E1 §3.1 | strong |
| Drive B reported sanitize success while all data remained and filesystem was mountable | `H/P` | E1 §3.2.1 / Table 1 | strong, anonymized device |
| only four of seven verifiable ATA-SECURITY-supporting drives executed ERASE UNIT reliably in the tested conditions | `H/P` | E1 §3.2.1 | strong, sample-specific |
| full-drive overwrite was usually but not universally effective in the tested devices | `H/P` | E1 §3.2.2 | strong, sample-specific |
| every tested single-file overwrite protocol failed to remove all target data in at least some SSD experiment | `H/P` | E1 §3.3 | strong |
| degaussing the seven tested flash chips left data intact | `H/P` | E1 §3.2.3 | strong, bounded test |
| `logical invisibility ≠ digital sanitization` | `E` | E1 taxonomy + raw-flash evidence | strong bounded reconstruction |
| `reported erase success ≠ verified media sanitization` | `E` | Drive B | strong bounded reconstruction |
| `interface contract ≠ implementation compliance` | `E` | E1 + Case 44 comparison | strong bounded reconstruction |
| the proposed FTL scrub mechanisms shipped in commercial SSDs | `X` | E1 says simulator / proposed extensions | rejected |
| the tested drives are named models/controllers | `X` | E1 anonymizes A–L | rejected |
| FAST ’11 proves current NVMe sanitize behavior | `X` | outside date/interface/sample | rejected |

## Cross-case boundaries

### Case 44 — NVM Express 1.3 Deallocate / Sanitize

Case 44 establishes a later normative interface distinction:

```text
Deallocate
    !=
Sanitize
```

Case 47 establishes an empirical evidence distinction:

```text
specified / reported erase
    !=
verified absence of old raw-flash data
```

The two cases are complementary. FAST ’11 does not test NVMe 1.3, and NVMe 1.3’s standard text does not prove any particular controller’s physical compliance.

### Case 04 — mapped Flash

Case 04’s 1993 primary evidence establishes that logical currentness can move before old physical embodiment is erased. Case 47 shows an independently observed consequence in later SSDs: stale digital embodiments can accumulate outside the current host mapping.

This is a functional bridge, not an assertion that the tested SSD FTLs implement the 1993 patent architecture.

### Kirschenbaum forensic-materiality test

The empirical remnants strengthen a distinction already used by the project:

> `forensic witness ≠ authoritative current state`.

A stale raw-flash copy can be real and recoverable without being the LBA value the controller currently exposes.

The reverse distinction matters equally:

> `logical absence ≠ forensic/material absence`.

Neither statement licenses the claim that old Flash traces survive indefinitely.

## Terminology and prior-art boundary

Historical 2011 vocabulary kept in the case:

- `sanitize` / `sanitization`;
- `logical sanitization`;
- `digital sanitization`;
- `analog sanitization`;
- `cryptographically sanitize`;
- `digital remnants`;
- `FTL`;
- `LBA`;
- `SECURITY ERASE UNIT`;
- `SANITIZE BLOCK ERASE`;
- `TRIM`;
- `scrubbing`.

Project vocabulary:

- `hidden embodiment`;
- `verification boundary`;
- `implementation compliance`;
- `forgetting contract`;
- `raw-media verification evidence`.

NIST SP 800-88 (2006) and the older ATA/security material cited by the paper prevent a false `Wei et al. invented sanitization/secure erase` narrative. The contribution of E1 is empirical SSD-specific validation and the resulting design argument for **verifiable** sanitization, not invention priority for deletion or media sanitization.

## Related-repository duplication check

`tmzncty/computing-archaeology` was searched in this slice for:

- `Reliably Erasing Data`;
- `FAST 2011 SSD sanitization`;
- `Wei Grupp Spada Swanson`;
- `digital remnants`.

No dedicated matching case was found. A broader history of SSD security, FTL design, or flash-controller evolution should still be routed there; `technical-retention` keeps the narrow relation between logical forgetting, hidden embodiments, and verification evidence.

## Evidence maturity and remaining limits

Case 47 is `grounded` because the central claims come from a peer-reviewed empirical study with explicit experimental procedure, per-device result tables, raw-flash extraction, and negative counterexamples. The strongest result — false success reporting with all data still present — does not depend on a speculative controller reconstruction.

The evidence is still bounded in important ways:

- drive identities are anonymized;
- firmware revisions and exact commercial model names are not recoverable from the paper;
- raw-flash extraction verifies digital remnants, not every possible analog remanence channel;
- encrypted-drive key destruction could not be independently verified;
- the proposed FTL scrub mechanisms were evaluated in simulation rather than shown as commercial deployments;
- the work predates NVMe 1.3 and therefore cannot establish modern NVMe Sanitize implementation quality;
- later NAND generations, controller encryption defaults, secure elements, and sanitize-status mechanisms require separate evidence.

Those limits are why the next roadmap step remains **named-product / named-controller sanitization compliance and later NVMe/ATA implementation validation**, not a universal conclusion from FAST ’11.