# Case 02 deepening — NCSC magnetic-core clearing, purging, and degaussing boundary, 1991

This evidence addendum deepens [`../cases/02-magnetic-core-destructive-read.md`](../cases/02-magnetic-core-destructive-read.md) without reopening the general history of magnetic-core memory.

**Bounded question:** the 1964 TCM-32 manual already shows a production core-memory `Memory Clear` operation that resets the whole stack to a defined `ZERO` state. Does that machine operation by itself establish security-grade forgetting, and how did a later period security source distinguish clearing, purging, overwriting, and degaussing for magnetic core memory?

The shared word `clear` is hazardous here. A product manual can use it for a concrete state-setting operation, while a security guideline can use `clearing` for an assurance category defined by what reconstruction capability must be defeated.

---

## Source A — NCSC-TG-025 Version 2, September 1991

**Document:** National Computer Security Center, *A Guide to Understanding Data Remanence in Automated Information Systems*, NCSC-TG-025, Library No. 5-236,082, Version 2, September 1991.

**Preserved transcription:** <https://irp.fas.org/nsa/rainbow/tg025-2.htm>

**Evidence class:** `H/P*` — a period U.S. National Computer Security Center technical guideline accessed through a later preservation/transcription host. FAS is not the historical author. The guide explicitly says it is guidance and should not replace policy.

Its foreword says Version 2 supersedes **CSC-STD-005-85, Department of Defense Magnetic Remanence Security Guideline, dated 15 November 1985**. That establishes a documentary predecessor floor, not invention priority. The guide retrospectively says storage-remanence risk had been recognized as early as 1960; because no direct 1960 source was inspected here, that date remains a retrospective claim rather than a new origin anchor.

---

## Historical record

### H1. Data remanence is residual physical representation after erasure

NCSC-TG-025 defines data remanence as residual physical representation after storage media has been erased, where surviving physical characteristics may permit reconstruction. This blocks `not current through the ordinary machine interface = no residual physical representation remains`.

### H2. `Clearing` and `purging` are different assurance categories

Section 2.2 defines **clearing** as removing sensitive data with assurance that it cannot be reconstructed through normal system capabilities — the guide frames this as the `keyboard` threat — while the secured physical environment remains controlled.

It defines **purging** as removing sensitive data with assurance that it cannot be reconstructed through open-ended laboratory techniques, and associates purging with release to a less secure environment.

Therefore:

```text
TCM-32 `Memory Clear`
    != automatically
NCSC security `clearing`
    != automatically
NCSC security `purging`
```

The first phrase names a documented 1964 product operation. The latter two name 1991 security-assurance categories.

### H3. Overwriting and degaussing are distinct procedures

Section 5.1.1 describes overwriting as writing unclassified data to locations that previously contained sensitive data. The generic guidance permits a single overwrite pattern for clearing and describes stronger patterned overwrite procedures for purging where applicable.

The degaussing primer instead describes erasure through an applied magnetic field. It distinguishes AC erasure, using an alternating field reduced from an initially high value, from DC erasure/saturation using a unidirectional field or permanent magnet. These are physically different from a machine-level clear/write sequence.

### H4. Magnetic core memory is named explicitly

Section 5.2.5 states that the DoD had approved both **overwriting** and **degaussing** as methods to clear or purge **magnetic core memory**, and says Type I degaussers and hand-held magnets can purge that medium, referring users to DoD 5200.28-M for the complete procedure.

This is a 1991 security-guidance witness. It does **not** establish that every earlier core-memory installation used these procedures, that TCM-32 `Memory Clear` had been evaluated as a purge procedure, or that NCSC invented core overwriting/degaussing.

### H5. Erasure tooling needs its own assurance

The guide warns that degaussers can be misused, fail, or lose capability, and recommends periodic testing. It explicitly warns against assuming that a new or previously evaluated unit is necessarily still providing sufficient erasure.

Its 90 dB discussion concerns a special worst-case **tape** test signal used for degausser evaluation. This addendum does not transfer that number to a named core plane.

---

## Engineering reconstruction

Case 02 can now distinguish three closure conditions:

1. the old value is no longer the machine's current logical word;
2. the old value cannot be reconstructed through normal system capability;
3. the old value cannot be reconstructed under the stronger laboratory-oriented purge threat model.

A selected overwrite or whole-stack `Memory Clear` can establish the first at the product-interface level. The 1991 security vocabulary shows why the first alone cannot prove the second or third.

`Clear` therefore needs at least three qualifiers:

```text
mechanism: ordinary overwrite / internal bulk reset / external degaussing
scope:     selected word / all addressable locations / physical magnetic medium
assurance: logical replacement / normal-interface clearing / laboratory-oriented purging
```

An overwrite can only replace state it actually reaches. NCSC's broader overwrite discussion therefore makes addressability and coverage part of security erasure: `write command completed` is weaker than `all security-relevant retained locations were overwritten`.

Degaussing also changes the authority path. Ordinary overwrite relies on the memory's selection/write path; degaussing acts through an applied magnetic field and can bypass ordinary logical addressing. Yet `procedure selected`, `procedure executed correctly`, and `erasure effectiveness established` remain separate relations.

---

## Functional analogy — bounded only

Later Flash/NVMe cases likewise distinguish logical invalidation, physical erase, sanitization objective, operation completion, and verification. The safe comparison is only relational:

```text
logical unavailability
    !=
security sanitization
    !=
verification that sanitization met its objective
```

Core overwrite/degauss is not Flash block erase, FTL reclamation, or NVMe Sanitize, and no genealogy is claimed.

---

## Philosophical interpretation — deliberately narrow

A prior payload can cease to be current under the ordinary machine interface without thereby satisfying a stronger reconstruction-resistance criterion. The narrow interpretive result is: **technical forgetting can have operation-relative and reconstruction-relative closure conditions.** This does not make NCSC terminology a universal theory of human forgetting, cultural memory, or tertiary retention.

---

## Rejected / unsupported claims

- **X — `TCM-32 Memory Clear = NCSC clearing`.** Shared wording does not establish identical semantics.
- **X — `whole-stack ZERO reset = demonstrated security purge`.**
- **X — `degaussed = logical ZERO`.** The physical/control paths differ.
- **X — `DoD-approved in 1991 = standard practice in every early core-memory installation`.**
- **X — `1991 Version 2 = invention priority`.** It names a 1985 predecessor.
- **X — `90 dB tape-degausser test = measured core-memory erasure margin`.**
- **X — `procedure invoked = erasure assured`.**
- **X — `data remanence = current authoritative payload`.**

---

## Related-repository boundary

The broad core-memory mechanism and engineering history are already covered in [`tmzncty/computing-archaeology: Why Was Magnetic-Core Memory Worth Weaving by Hand?`](https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md).

A fresh repository search for `degauss`, `sanitization`, and magnetic-core remanence found no dedicated companion case to reuse. Broad degausser history, magnetic-security-policy genealogy, material/coercivity studies, and experimental remanence measurement belong primarily in `computing-archaeology` if developed.

The retention-specific result kept here is: **product-level state replacement, security clearing, laboratory-oriented purging, degaussing, and evidence that an erasure apparatus still works are separable relations even when they concern the same magnetic-core substrate.**

---

## Readiness assessment

This closes the bounded **magnetic-core security-erasure vocabulary / clear-versus-purge / overwrite-versus-degauss** seam left open after the 1964 TCM-32 addendum.

Still open are direct analog post-switch remanence measurements on a named core plane, exact 1960s/1970s classified-core degaussing genealogy, direct inspection of the 1985 predecessor, material-specific thresholds for named products, and post-degauss service consequences.
