# Evidence index — Case 101: SCSI Background Medium Scan and proactive defect discovery

**Case status:** `grounded`

Canonical case: [`../cases/101-scsi-background-medium-scan-proactive-defect-discovery.md`](../cases/101-scsi-background-medium-scan-proactive-defect-discovery.md)

This index consolidates the current Case 101 evidence chain without changing maturity. It is intended to prevent later rounds from repeatedly re-reading the same standards, patents, and product manuals while keeping historical record, engineering reconstruction, functional analogy, and philosophical interpretation separate.

---

## 1. What Case 101 is about

Case 101 tracks the transition from host-issued foreground verification toward device-side background media scanning and proactive defect discovery, while preserving several distinctions that are easy to collapse:

```text
foreground read/verify
    != autonomous background scan

background scan capability
    != scan enabled
    != scan currently active
    != scan completed

progress observable
    != persistent checkpoint
    != unique completion evidence

suspected defect discovered
    != defect repaired
    != block successfully reassigned

background maintenance completed
    != retention-specific maintenance completed
```

The case remains **`grounded`**. None of the packets below justifies maturity promotion by itself.

---

## 2. Standards / interface grounding

### 2.1 T10 2004–2007 Background Medium Scan grounding

[`101-t10-2004-2007-background-medium-scan-grounding.md`](101-t10-2004-2007-background-medium-scan-grounding.md)

Role:

- grounds Background Medium Scan as a standards-era SCSI feature;
- distinguishes autonomous BMS from foreground host VERIFY;
- establishes Background Control and Background Scan Results surfaces;
- records status, progress, scan-count, and defect-result concepts;
- preserves the difference between discovery and subsequent repair/reassignment policy.

Use this packet when the question is **what the SCSI feature family exposes**, not when the question is a specific vendor's crash/power persistence behavior.

### 2.2 Foreground VERIFY prior art

[`101-scsi-1986-1994-verify-host-command-prior-art-deepening.md`](101-scsi-1986-1994-verify-host-command-prior-art-deepening.md)

Role:

- anchors earlier host-command media verification;
- prevents the history from being written as if proactive media checking began with BMS;
- preserves the architectural distinction between explicit foreground verification and autonomous background maintenance.

---

## 3. Earlier proactive-scan prior art

### 3.1 IBM 1986–1996 background-scan patent lineage

[`101-1986-1996-ibm-patent-background-scan-rooted-prior-art.md`](101-1986-1996-ibm-patent-background-scan-rooted-prior-art.md)

Role:

- supplies earlier device-side/background scanning prior art;
- keeps patent disclosure separate from proof of a named shipping implementation;
- prevents T10 standardization date from being mistaken for the invention date of every underlying maintenance concept.

### 3.2 IBM 1998 disk-scrubbing boundary

[`101-ibm-1998-disk-scrubbing-boundary-deepening.md`](101-ibm-1998-disk-scrubbing-boundary-deepening.md)

Role:

- deepens the pre-standardization / parallel history of periodic media scrubbing;
- separates historical terminology and implementation setting from later SCSI BMS vocabulary;
- provides a cross-era comparison without claiming identity of implementations.

---

## 4. Named-product policy and repair behavior

### 4.1 Hitachi 2008 BMS policy / log persistence

[`101-hitachi-2008-bms-policy-log-persistence-deepening.md`](101-hitachi-2008-bms-policy-log-persistence-deepening.md)

Role:

- grounds a named-product-family BMS implementation and policy surface;
- examines status/progress/scan-count monitoring;
- distinguishes generic log-parameter saving from proof of a persistent exact scan cursor;
- establishes:

```text
save-capable monitoring state
    != proved crash/power-persistent resume checkpoint
```

### 4.2 LSI 2010 media-patrol repair policy

[`101-lsi-2010-media-patrol-repair-policy-deepening.md`](101-lsi-2010-media-patrol-repair-policy-deepening.md)

Role:

- grounds controller-level media patrol behavior;
- distinguishes detection from repair policy;
- helps show that proactive scanning and corrective action are related but not the same control state.

### 4.3 Dell 2011 media-patrol host policy

[`101-dell-2011-media-patrol-host-policy-deepening.md`](101-dell-2011-media-patrol-host-policy-deepening.md)

Role:

- shows how background media patrol becomes an operator/controller policy issue in a named deployment context;
- keeps host/controller scheduling policy separate from low-level drive scan semantics.

### 4.4 Western Digital 2024 BMS progress / repair policy

[`101-wd-2024-bms-progress-repair-policy-deepening.md`](101-wd-2024-bms-progress-repair-policy-deepening.md)

Role:

- grounds a current named-drive-family manual;
- exposes progress plus repair/reassignment policy;
- records ordinary disable/re-enable suspension/resumption from the last scanned logical block;
- explicitly does **not** turn ordinary suspend/resume into proof of a cross-power persistent cursor.

---

## 5. Power-epoch observability boundary

### 5.1 Seagate 2010 zero-progress ambiguity

[`101-seagate-2010-bms-zero-progress-power-epoch-ambiguity-deepening.md`](101-seagate-2010-bms-zero-progress-power-epoch-ambiguity-deepening.md)

Role:

- closes the exact semantics of `BACKGROUND MEDIUM SCAN PROGRESS = 0000h` in Seagate's December-2010 SCSI command reference;
- establishes that the same value represents both:

```text
no BMS initiated since power on
```

and:

```text
most recent BMS completed
```

- therefore establishes:

```text
progress = 0000h
    != unique completion evidence
    != cross-power resume checkpoint
```

- introduces the repository analysis terms **power-epoch-scoped progress observable** and **many-to-one observability boundary**, explicitly as engineering reconstruction rather than historical vendor terminology.

This packet should be consulted before treating a zero progress value as evidence that a required maintenance pass completed.

---

## 6. Unified evidence chain

The current Case 101 chain is best read as:

```text
foreground verification prior art
    -> earlier proactive/background scan prior art
    -> SCSI BMS standardization
        -> enable / scheduling controls
        -> scan activity
        -> status + progress + count surfaces
        -> defect discovery
        -> policy-dependent repair / reassignment
        -> run history / logs
```

But the following inequalities remain essential:

```text
capability
    != enabled policy
    != active run
    != completed run

active-run progress
    != durable resume cursor

progress = 0
    != unique proof of completed run

scan result log
    != successful repair

successful BMS run
    != retention-refresh completion authority
```

---

## 7. Cross-case links

These are functional comparisons only; they are not genealogy claims.

### Case 111 — enterprise SSD extended-shutdown maintenance

Relevant packet:

[`111-seagate-xt2-maintenance-observability-boundary-deepening.md`](111-seagate-xt2-maintenance-observability-boundary-deepening.md)

Why it matters:

- the same Seagate command-reference family demonstrates rich BMS status/progress/result telemetry;
- XT.2 separately documents powered retention monitoring/rewrite;
- BMS observability does not become retention-refresh completion authority merely because both are background device work.

### Case 78 — NAND bad-block knowledge

Functional comparison:

- media-error discovery and durable exclusion knowledge are different stages;
- discovering a suspect location does not itself prove later retirement/reassignment metadata converged.

### Case 04 — Flash mapping / reclamation

Functional comparison:

- operation completion and successful qualification are distinct;
- a maintenance state transition should not be collapsed merely because one observable reaches an idle/default value.

---

## 8. Evidence-strength guardrails

When extending Case 101, preserve these boundaries:

```text
standards proposal
    != named-product implementation proof

patent disclosure
    != shipping-product proof

product manual
    != hidden-firmware implementation disclosure

ordinary suspend/resume
    != crash/power-loss recovery proof

save-capable log parameter
    != exact cursor persistence proof

host-visible ambiguity
    != proof of internal-state loss
```

A later packet should state explicitly which layer it strengthens.

---

## 9. Current open debt

The highest-value unresolved questions are now narrow rather than generic.

### P1 — exact cross-power cursor behavior

Find a named SAS/SCSI product whose first-party documentation explicitly says whether an interrupted BMS:

```text
resumes from a durable location after power cycle
```

or:

```text
restarts from a defined location after power cycle
```

### P1 — power-cycle fault trace

Produce or locate a trace that records:

```text
nonzero BMS progress
    -> power loss / device reset
    -> restart
    -> status
    -> progress
    -> scan count
    -> defect-result log
    -> observed resume/restart behavior
```

The experiment must distinguish actual power removal from software/controller reset.

### P2 — maintenance-completion evidence composition

Determine whether a realistic host can combine status, progress, count, error-log timestamps/power-on minutes, and externally retained observations to construct a stronger completion witness than any single field supplies.

### P2 — repair completion versus scan completion

Deepen named-device evidence for cases where:

```text
scan completed
    != every detected defect successfully reassigned
```

especially where the host/controller must perform a later repair action.

---

## 10. Navigation rule for future rounds

Before opening a new Case 101 research slice:

1. use the T10 grounding packet for standards semantics;
2. use the prior-art packets for chronology;
3. use the Hitachi/LSI/Dell/WD packets for named-product policy and repair distinctions;
4. use the Seagate 2010 packet for zero-progress / power-epoch observability;
5. only create another packet when it closes a genuinely new evidence boundary rather than restating those distinctions.

Current case status remains **`grounded`**.