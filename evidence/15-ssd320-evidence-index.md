# Case 15 Evidence Index — Intel SSD 320 Power-Loss Durability

## Status

**Case 15 remains `grounded`.**

This file is navigation, not a maturity promotion. It groups the current evidence-bearing slices for the Intel SSD 320 power-loss case and keeps three different questions separate:

1. **How does state move from volatile controller staging into NAND during normal/abnormal shutdown?**
2. **What history does the drive retain about abnormal shutdown events?**
3. **What must still be correct after restart for the retained media to be presented as a usable logical device?**

Canonical case:

- [`../cases/15-intel-ssd320-power-loss-durability.md`](../cases/15-intel-ssd320-power-loss-durability.md)

Focused deepenings:

- [`15-intel320-2011-unsafe-shutdown-telemetry-deepening.md`](15-intel320-2011-unsafe-shutdown-telemetry-deepening.md)
- [`15-intel-2011-bad-ctx-recovery-context-boundary-deepening.md`](15-intel-2011-bad-ctx-recovery-context-boundary-deepening.md)

---

## Evidence chain A — volatile staging, flush, and emergency retention work

### Main question

What must happen between a host-visible write relation and a recoverable nonvolatile SSD state when the controller contains volatile staging and system state?

### Primary anchors already carried by the canonical case

- T13 ATA8-ACS working-draft `FLUSH CACHE` / `FLUSH CACHE EXT` semantics;
- Intel SSD 320 Power Loss Data Protection brief, order **325207-001US**, March 2011;
- Intel SSD 320 Product Specification, order **325152-002US**, September 2011;
- Intel Enterprise Server/Storage Addendum, order **325170-002US**, April 2011;
- Zheng et al., FAST '13, as an independent cross-device fault-injection boundary rather than named-product identification.

### Grounded relation

```text
host-visible write
    -> volatile controller staging may still exist
    -> explicit flush / clean shutdown or emergency power-loss path
    -> NAND programming + required controller/system state
    -> recoverable device state
```

### Strongest boundaries

```text
nonvolatile NAND present
    !=
every currently necessary SSD state already nonvolatile
```

```text
stored capacitor charge
    = retention infrastructure
    != retained user payload
```

```text
interface flush contract
    != empirical proof of every firmware implementation
```

---

## Evidence chain B — unsafe-shutdown telemetry

### File

[`15-intel320-2011-unsafe-shutdown-telemetry-deepening.md`](15-intel320-2011-unsafe-shutdown-telemetry-deepening.md)

### Main question

What does SMART attribute `C0h` retain, and what does that retained event evidence not prove?

### Primary anchors

Intel SSD 320 Product Specification, September 2011, Tables 12–13; Intel March 2011 power-loss brief.

### Grounded relation

```text
abnormal shutdown condition
    -> cumulative unsafe-shutdown event count
```

but:

```text
unsafe-shutdown event counted
    != PLP failure verdict
    != payload corruption verdict
```

The counter is compressed lifetime event history, not a per-event log. Its documented semantics do not expose exact counter-update atomicity.

---

## Evidence chain C — BAD_CTX recovery-context boundary

### File

[`15-intel-2011-bad-ctx-recovery-context-boundary-deepening.md`](15-intel-2011-bad-ctx-recovery-context-boundary-deepening.md)

### Main question

What does the August 2011 `BAD_CTX 13x` / 8 MB firmware history add after the emergency transfer mechanism has already been documented?

### Primary / period anchors

- Intel-authored SSD Firmware Update Tool revision history, document **328292-030US**, preserving the August 2011 `4PC10362` entry;
- archived Intel Communities post from Intel's NVM Solutions Group, **17 August 2011**;
- March 2011 Intel SSD 320 power-loss architecture brief as the earlier protection-side witness.

### Grounded historical record

Intel's revision history says firmware `4PC10362` fixes issues related to `BAD_CTX 13x` (`8MB capacity`) problems associated with unsafe power-loss situations.

The Intel NVM Solutions Group support post describes the affected state as:

- 8 MB reported capacity;
- electronic serial field `BAD_CTX 0000013x`;
- no ordinary user-data access;
- no ordinary read/write operation;
- replacement or secure erase as the already-affected-drive support path;
- firmware update not recovering prior user data.

### Engineering boundary

```text
emergency power-loss protection architecture exists
    != restart-time recovery/context correctness proved
```

```text
host-visible capacity collapse
    != proof of physical NAND population collapse
```

```text
restore device operability
    != restore prior user payload
```

The evidence does **not** identify `BAD_CTX` as a specific FTL map, superblock, capacitor, or NAND-programming failure.

---

## Cross-chain model

The three evidence chains should be composed without being merged:

```text
                           ┌─────────────────────────────┐
                           │ abnormal power transition   │
                           └──────────────┬──────────────┘
                                          │
                ┌─────────────────────────┼──────────────────────────┐
                │                         │                          │
                v                         v                          v
      emergency retention work    event-history update      restart/recovery path
                │                         │                          │
                v                         v                          v
      NAND-targeted handoff       cumulative C0h count      capacity/addressability
                │                                                    │
                └──────────────────────┬─────────────────────────────┘
                                       v
                              usable logical device
```

No one branch proves the success of the others.

A counted unsafe shutdown can coexist with successful emergency protection. Conversely, the BAD_CTX defect shows that a device can possess the documented power-loss-protection architecture while still containing a recovery-path firmware defect associated with unsafe power loss.

---

## Controlled comparison with adjacent cases

### Case 04 — mapped Flash

Case 04 supplies the mechanism-level reason not to equate physical embodiment with logical currentness/addressability. It is a **functional comparison only**. The Case 15 evidence does not establish that `BAD_CTX` was a specific FTL-map corruption.

### Case 38 — Intel S3700 PLI test state

Case 38 concerns testing/telemetry around power-loss-immunity readiness and control-state persistence. Case 15 instead concerns the actual fault boundary of a different named product. Do not transfer S3700 test semantics backward to SSD 320.

### Case 55 — NVMe health history

Case 55 is useful for comparing cumulative retained health/event state with current device state. It is not a genealogy claim from SSD 320 SMART C0h to NVMe SMART/Health.

### Case 76 / 111 — SSD retention qualification and powered maintenance

Those cases concern retention across aging/offline intervals and powered maintenance. Case 15 concerns a short unsafe-power-loss transition and restart recovery. `power loss` and `power-off retention` are not interchangeable failure regimes.

---

## Historical record / engineering reconstruction / analogy / interpretation discipline

### Historical record

Safe historical claims are limited to what Intel/T13/FAST sources actually say or demonstrate: documented flush semantics, documented SSD 320 power-loss architecture, documented SMART event count, documented August 2011 BAD_CTX-related firmware fix, and the archived Intel support description of the affected 8 MB state.

### Engineering reconstruction

The repository may reconstruct separate obligations for:

- volatile-state handoff;
- stored-energy support;
- nonvolatile programming/currentness;
- retained event telemetry;
- restart-time context interpretation;
- capacity/addressability re-presentation.

These terms do not become Intel's historical vocabulary merely because they fit the evidence.

### Functional analogy

Mapped-Flash currentness and later diagnostic-history cases may illuminate the relation structure. They do not identify the hidden BAD_CTX implementation.

### Philosophical interpretation

The bounded interpretive result is only that technical availability can fail even when the underlying medium is nonvolatile, because access depends on retained/reconstructed authority and interpretation relations. Do not infer complete physical payload survival from that statement.

---

## Current research debt

The highest-value remaining Case 15 work is now narrower than another generic SSD power-loss survey:

- an Intel engineering advisory/erratum identifying the internal `BAD_CTX 13x` structure;
- named SSD 320 pre-/post-`4PC10362` power-cut experiments;
- OEM firmware lineage and whether later release notes document related recovery-context fixes;
- raw-media or forensic evidence capable of distinguishing payload survival from controller presentation failure;
- exact power-fail behavior of C0h event-count persistence;
- ATA/SFF history of the inherited `Power-Off Retract Count` label, primarily as `computing-archaeology` work.

No maturity promotion is justified by the present deepening: the canonical case was already `grounded`, and the new evidence sharpens one failure boundary rather than broadening the case into a complete SSD-320 firmware history.

---

## Related-repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Intel SSD 320`, `BAD_CTX`, and SSD power-loss vocabulary found no dedicated packet to reuse.

Accordingly, `technical-retention` keeps only the retention-specific relations above. Broader Intel SSD product genealogy, controller architecture, firmware lineage, SATA-market history, and SSD commercialization history belong in `computing-archaeology` if pursued later.
