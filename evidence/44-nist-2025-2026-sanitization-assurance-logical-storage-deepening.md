# Case 44 deepening — NIST SP 800-88 Rev. 2 assurance and logical storage (2025–2026)

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
