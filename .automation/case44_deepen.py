from pathlib import Path
E=Path("evidence/44-nist-2025-2026-sanitization-assurance-logical-storage-deepening.md")
E.write_text("""# Case 44 deepening — NIST SP 800-88 Rev. 2 assurance and logical storage (2025–2026)

## Scope
Later institutional boundary only; it does not rewrite NVMe 1.3 (2017) or make NIST an NVMe conformance specification.

## Historical record
NIST SP 800-88 Rev. 2 (September 2025) supersedes Rev. 1. Its change log shifts most device-specific technique/tool detail (except CE) toward current standards such as IEEE 2883 and toward an enterprise sanitization program.

Section 3.1 distinguishes logical from physical techniques. Logical techniques may replace data over an interface, issue commands that eliminate data, or eliminate access; Rev. 2 also uses **information storage media (ISM)** to accommodate logical/cloud storage. NIST's July 16, 2026 FAQ explicitly includes cloud and object storage that abstract underlying physical media.

Section 4.5 separates **verification** from **validation**. Verification inspects technique outcome/completion, errors, anomalies, and media health. Validation decides whether target data was effectively sanitized at an acceptable confidentiality-risk level. Therefore:

> **operation completion evidence != validation acceptance**

Rev. 2 gives direct counterexamples: degaussing an SSD may complete successfully while sanitizing no sensitive data; simple write-based clear on overprovisioned storage may leave substantial user data unchanged because target scope was too narrow.

Section 4.5.1 also says elaborate full/representative post-sanitize sampling is not generally necessary unless organizational policy requires it. Thus NIST Rev.-2 assurance is not identical to FAST '11's raw-Flash dismantling experiment.

The July-2026 FAQ says that in virtual/cloud storage the data owner cannot directly execute traditional physical destruction or overwrite against abstracted physical ISM; CE is often the only viable purge method in that bounded setting, with secure key management and traceably validated zeroization required.

## Engineering reconstruction
- `logical sanitization != necessarily host overwrite`;
- `NVMe sanitize-operation completion != NIST validation verdict`;
- `procedure completion != substrate-appropriate sanitization`;
- `user-addressable overwrite coverage != target-data coverage on overprovisioned storage`;
- `data-owner sanitization intent != direct physical-media authority`;
- cloud sanitization evidence can depend on retained provider/key/traceability relations.

These are bounded comparisons, not genealogy and not claims that every cloud service uses CE.

## Cross-case boundary
Case 44 supplies NVMe command/operation semantics. Case 47 supplies direct raw-Flash implementation evidence. Rev. 2 supplies a later institutional assurance layer:

```text
command accepted
 != operation completed
 != verification evidence
 != validation acceptance
```

Case 02's 1991 NCSC `clearing`/`purging` vocabulary remains a separate historical regime; do not back-project 2025/2026 NIST terms.

## Sources
- NIST SP 800-88 Rev. 2, September 2025, §§3.1, 4.5.1–4.5.2, Appendix D: <https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-88r2.pdf>
- NIST CSRC record: <https://csrc.nist.gov/pubs/sp/800/88/r2/final>
- NIST, FAQ for SP 800-88r2, July 16, 2026, Q1/Q3/Q7/Q13: <https://csrc.nist.gov/files/pubs/sp/800/88/r2/final/docs/sp800-88r2-faq.pdf>

## Related-repository check
Fresh searches of `tmzncty/computing-archaeology` for `NIST 800-88 sanitization validation verification` and `media sanitization` found no dedicated overlapping case. Broader standards/device/cloud genealogy belongs there.
""",encoding="utf-8")

p=Path("cases/44-nvme13-deallocate-sanitize-forgetting.md"); s=p.read_text()
sec="""## Later institutional boundary — NIST Rev. 2 assurance and logical storage (2025–2026)

NIST SP 800-88 Rev. 2 (September 2025) adds a later assurance layer to this historical NVMe case. It separates technique-outcome **verification** from effectiveness/risk **validation**; its own examples show that a technically completed SSD degauss or too-narrow overwrite can still fail the target-data objective. The July-2026 NIST FAQ also explicitly includes cloud/object storage as logical ISM whose physical media are abstracted from the data owner. Full review: [`../evidence/44-nist-2025-2026-sanitization-assurance-logical-storage-deepening.md`](../evidence/44-nist-2025-2026-sanitization-assurance-logical-storage-deepening.md).

Bounded comparison:

```text
Sanitize command completion
 != Sanitize operation completion
 != NIST verification evidence
 != NIST validation acceptance
```

Only the first two are NVMe-1.3 interface semantics. The latter two are later NIST vocabulary. Rev. 2 also states that full/representative post-sanitize sampling is not generally required unless policy demands it, so Case 47's FAST-'11 raw-Flash experiment remains a distinct empirical path rather than the definition of NIST verification.

"""
m="## Broader prior art boundary\n"
if "## Later institutional boundary — NIST Rev. 2 assurance" not in s:
    if m not in s: raise SystemExit("case marker")
    s=s.replace(m,sec+m,1)
p.write_text(s)

p=Path("ROADMAP.md"); s=p.read_text()
item="""- [x] Case 44 NIST Rev.-2 sanitization-assurance / logical-storage deepening — [`evidence/44-nist-2025-2026-sanitization-assurance-logical-storage-deepening.md`](evidence/44-nist-2025-2026-sanitization-assurance-logical-storage-deepening.md): September-2025 Rev. 2 + July-2026 FAQ close the bounded `operation completion != validation acceptance` and `data-owner sanitization intent != direct physical-media authority` seams, without back-projecting current terminology into NVMe 1.3 or equating NIST assurance with FAST-'11 raw-media forensics. IEEE-2883 genealogy, named-device compliance, cloud-provider internals, and independent fault validation remain open.

"""
m="## Phase 2 — Build missing technical bridges\n\n"
if item not in s:
    if m not in s: raise SystemExit("roadmap marker")
    s=s.replace(m,m+item,1)
p.write_text(s)

p=Path("CASE_INDEX.md"); s=p.read_text()
f="""

## Case 44 deepening — NIST Rev.-2 sanitization-assurance / logical-storage findings

Evidence: [`evidence/44-nist-2025-2026-sanitization-assurance-logical-storage-deepening.md`](evidence/44-nist-2025-2026-sanitization-assurance-logical-storage-deepening.md)

- **2879 — Rev.-1 historical guidance != current NIST guidance:** SP 800-88 Rev. 2 supersedes Rev. 1. (`H/P`)
- **2880 — current NIST program guidance != device-command specification:** Rev. 2 shifts most technique detail to evolving standards and an enterprise program. (`H/P`, `E`, `X`)
- **2881 — ISM != only a physical device:** the 2026 FAQ explicitly includes cloud/object-storage abstractions. (`H/P`)
- **2882 — logical sanitization != necessarily host overwrite:** Rev. 2 permits commands/access elimination as logical techniques. (`H/P`)
- **2883 — verification != validation:** outcome/completion inspection is separate from effectiveness/risk acceptance. (`H/P`)
- **2884 — operation completion evidence != validation acceptance:** completion is an assurance input, not the final effectiveness decision. (`H/P`, `E`)
- **2885 — completed procedure != substrate-appropriate sanitization:** NIST's SSD-degauss counterexample completes yet sanitizes no sensitive data. (`H/P`, `E`)
- **2886 — user-addressable overwrite != full target coverage:** Rev. 2 warns about overprovisioned storage. (`H/P`, `E`)
- **2887 — NIST verification != mandatory raw-media sampling:** elaborate sampling is not generally required absent policy. (`H/P`, `X`)
- **2888 — FAST-'11 raw-Flash evidence != Rev.-2 assurance by definition:** these are distinct observation/decision practices. (`H/P`, `A`, `X`)
- **2889 — interface status != independent implementation proof:** NVMe status, NIST assurance, and Case-47 empirical evidence answer different questions. (`E`, `A`)
- **2890 — data-owner sanitization intent != direct physical-media authority:** cloud physical ISM is abstracted from the owner. (`H/P`, `E`)
- **2891 — cloud purge can depend on retained key/traceability relations:** FAQ Q13 requires secure key management and traceably validated zeroization for its bounded CE path. (`H/P`, `E`)
- **2892 — provider agreement != sanitization proof by itself:** contract review is an assurance input, not the physical result. (`H/P`, `E`, `X`)
- **2893 — 2025/2026 vocabulary != NVMe-1.3 historical vocabulary:** later terms are not evidence of 2017 authorial intent. (`H/P`, `X`)
- **2894 — related-repository boundary:** fresh `computing-archaeology` searches found no dedicated NIST sanitization-assurance case; broader genealogy belongs there. (`H/P` project-state record)
"""
if "## Case 44 deepening — NIST Rev.-2 sanitization-assurance / logical-storage findings" not in s:
    if "**2878 — related-repository boundary:**" not in s: raise SystemExit("index marker")
    s=s.rstrip()+f+"\n"
p.write_text(s)
