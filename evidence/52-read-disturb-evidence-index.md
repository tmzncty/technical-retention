# Case 52 — NAND Read-Disturb Evidence Index

Canonical case: [`../cases/52-nand-flash-read-disturb-access-induced-decay.md`](../cases/52-nand-flash-read-disturb-access-induced-decay.md)

## Maturity

**Case 52 remains `grounded`.**

This index is navigation, not a maturity promotion. The case has strong device-physics, manufacturer-guidance, institutional-test, controller-state, prevention-policy, and targeted-maintenance evidence, but named-product firmware behavior, restart-safe maintenance-obligation handling, and modern 3-D NAND product validation remain incomplete.

`CASE_INDEX.md` is currently empty even though `ROADMAP.md` still describes it as the authoritative maturity ledger. Until that repository-wide inconsistency is repaired as its own bounded task, this index follows the canonical Case 52 status and does not invent a separate global status.

## Evidence lines

### 1. Physical mechanism / characterization grounding

[`52-cai-2009-2015-nand-read-disturb-grounding.md`](52-cai-2009-2015-nand-read-disturb-grounding.md)

Role:

- establishes read disturb as access-induced threshold-voltage/error growth in NAND;
- separates selected-page logical read success from stress on unselected cells;
- grounds `Vpass Tuning` and `Read Disturb Recovery` as later research mechanisms;
- keeps read disturb separate from retention-age error and program interference.

Primary boundary:

```text
successful logical READ
    !=
zero physical effect on neighboring retained state
```

### 2. Manufacturer maintenance-policy / failure-taxonomy line

[`52-micron-2006-read-disturb-temporary-failure-maintenance-deepening.md`](52-micron-2006-read-disturb-temporary-failure-maintenance-deepening.md)

Role:

- grounds Micron's 2006 classification of read disturb as a recoverable/temporary failure class rather than automatic permanent bad-block identity;
- shows several system-level mitigation topologies rather than one universal policy;
- separates a system-designated renewal threshold from a universal physical failure count.

Primary boundary:

```text
recoverable read-disturb condition
    !=
permanent carrier-retirement authority
```

### 3. Persistent access-history / checkpoint line

[`52-denali-2008-2009-persistent-read-count-checkpoint-deepening.md`](52-denali-2008-2009-persistent-read-count-checkpoint-deepening.md)

Role:

- gives an explicit controller embodiment in which per-block read-count state is retained in a non-volatile block table;
- distinguishes live RAM state from periodically/shutdown-checkpointed state;
- grounds power-up reconstitution of maintenance-control state;
- preserves the crash-durability gap between newest live increments and latest checkpoint.

Primary boundary:

```text
retained access-history summary
    !=
complete access event log
    !=
every newest increment crash-durable
```

### 4. Preventive exposure-avoidance prior-art line

[`52-sandisk-2004-2007-read-disturb-exposure-avoidance-prior-art-deepening.md`](52-sandisk-2004-2007-read-disturb-exposure-avoidance-prior-art-deepening.md)

Role:

- shows that read-disturb management need not begin with accumulating risk and later repairing it;
- grounds an addressability/capacity-sacrifice topology that avoids placing useful payload in repeatedly stressed neighbors;
- grounds a separate electrical read-sequence mitigation line;
- shows that protection-policy metadata and its own read path can be part of retention-risk control.

Primary boundary:

```text
prevent hazardous exposure
    !=
observe degradation and renew later
```

### 5. Targeted-sampling / queue-lifetime line

[`52-sandisk-2012-2013-targeted-read-scrub-control-state-deepening.md`](52-sandisk-2012-2013-targeted-read-scrub-control-state-deepening.md)

Role:

- supplies a counterexample to the assumption that read-disturb maintenance requires persistent per-block read counters;
- grounds probabilistic scan admission in response to host reads;
- separates retained manufacturer-derived policy parameters from exact access history;
- shows sampled local ECC/error evidence authorizing whole-block pending maintenance;
- explicitly shows the refresh queue may be stored in controller RAM or non-volatile memory;
- preserves the open restart/crash-consistency question rather than treating both queue embodiments as equivalent.

Primary boundaries:

```text
exact READ-count history
    !=
maintenance capability
```

```text
retained maintenance policy
    !=
retained pending-maintenance obligation
```

```text
error observed
    -> queued obligation
    !=
renewal completed
```

## Case-wide comparison map

The five evidence lines currently support the following bounded decomposition:

```text
host READ
    -> physical neighbor exposure
    -> possible raw-error growth

risk may then be handled by different topologies:

A. prevent / reduce exposure
B. retain an access-count summary and trigger at a threshold
C. probabilistically sample susceptible regions without exact read counters
D. measure current error evidence
E. queue renewal work
F. relocate / erase-reprogram / otherwise renew before correction margin is exhausted
G. recover an already-failing read through a separate recovery mechanism
```

These are **functional categories**, not one historical genealogy.

## Control-state decomposition

Across the inspected records, at least these states should remain distinct:

1. user/logical payload;
2. physical NAND threshold/charge state;
3. ECC-correctable raw-error state;
4. read/workload history or a compressed read-count proxy;
5. manufacturer-derived susceptibility / scan-frequency / threshold policy;
6. sampled error evidence;
7. pending refresh/reclaim obligation;
8. mapping/currentness state during relocation;
9. maintenance completion/history evidence;
10. permanent bad-block / carrier-retirement authority.

One evidence line may omit or reconstruct a state that another line persists directly. That difference is analytically important.

## Cross-case links

### Case 36 — Flash Correct-and-Refresh

[`../cases/36-nand-flash-correct-and-refresh-maintenance.md`](../cases/36-nand-flash-correct-and-refresh-maintenance.md)

Controlled comparison:

```text
retention-age / wear pressure
    !=
read-induced disturb pressure
```

Both can motivate ECC-bounded renewal, but trigger, evidence, physical failure process, and public chronology differ.

### Case 67 — adaptive read reclaim

[`../cases/67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md`](../cases/67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md)

Controlled comparison:

```text
persistent / resettable compressed read proxy
    !=
counter-free probabilistic scan admission
```

Both can combine workload-related policy with measured error evidence and later relocation. No influence or genealogy is asserted.

### Case 78 — bad-block management

The Case 52 manufacturer evidence is useful mainly for the negative boundary:

```text
renewal obligation
    !=
permanent future-allocation prohibition
```

Read disturb can require renewal before a block becomes a permanently retired carrier.

## Public-date guardrails

The index preserves source dates by evidence class:

- SanDisk-associated exposure-avoidance publication: public by 2005;
- Micron manufacturer guidance: 2006;
- NASA/JPL qualification witness: 2008;
- Denali public application: July 2009, despite its 2008 filing;
- Texas Memory Systems public patent record: 2010;
- SanDisk targeted-read-scrub filing: June 2012, but **public application only December 2013**;
- Cai et al. DSN characterization: 2015.

Therefore:

```text
filing / priority chronology
    !=
public-document chronology
```

and no 2012 filing is silently promoted into public prior art before its 2013 publication.

## Remaining high-value evidence debt

Priority follow-ups:

- named-product read-disturb/reclaim behavior tied to real firmware versions;
- restart semantics for a volatile pending-refresh queue;
- crash consistency / atomicity of a non-volatile pending-refresh queue;
- interrupted relocation and mapping/currentness handoff;
- modern 3-D NAND victim geometry tied to named devices;
- workload-to-telemetry experiments that distinguish read reclaim, patrol read, refresh, and ordinary GC;
- exact persistence/reset/overflow semantics of management counters;
- later SanDisk/Western Digital low-impact read-disturb / background-media-scan genealogy;
- independent experiments comparing deterministic read-count policies with sampled/probabilistic inspection;
- full related-repository technical history if controller/product genealogy becomes the research object.

## Related-repository boundary

Fresh inspection found no dedicated `US9053808` packet in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology).

Keep here:

- access-induced retention risk;
- exact-history versus sampled-policy control state;
- pending-work persistence horizon;
- ECC-margin qualification;
- relocation/renewal authority;
- restart evidence boundaries.

Move broader work there if the task becomes:

- SanDisk controller/product genealogy;
- read-scrub terminology history across vendors;
- patent-family lineage;
- manufacturing/process-node chronology;
- commercial deployment history independent of the retention argument.
