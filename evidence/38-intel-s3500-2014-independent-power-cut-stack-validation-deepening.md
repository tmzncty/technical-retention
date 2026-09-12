# Evidence 38B — Intel DC S3500 independent system-stack power-cut validation deepening

**Status:** `grounded`

## Scope

This record closes one bounded part of Case 38's open evidence debt: add an **independent named-product power-cut observation** without silently promoting it into isolated component certification.

The named device is Intel's **DC S3500**, a sibling product explicitly covered alongside S3700 by Intel's PLI material already used in Case 38. The independent witness is Nordeus Engineering's December-2014 hard-power-cut test, published 12 November 2015.

The distinction this record is meant to preserve is:

```text
component PLI self-test
    != manufacturer whole-device validation
    != independent system-stack power-cut observation
    != universal product / stack compliance
```

The evidence does **not** establish that S3500 and S3700 are internally identical, and it does not turn one successful stack test into a general SSD guarantee.

---

## Claim classification

### Historical / primary product record (`H/P`)

Intel's January-2015 **Intel Solid-State Drive DC S3500 Series Product Specification** lists both `Enhanced power-loss data protection` and `Power loss protection capacitor self-test` as product features. Section 2.8 states that the drive supports testing its power-loss capacitor through SMART attribute `AFh`.

The same SMART table keeps two records separate:

- `AEh` — `Unexpected Power Loss`, a cumulative count of unclean shutdowns, defined independently of whether PLI capacitor activity occurred;
- `AFh` — `Power Loss Protection Failure`, carrying the last capacitor-test result, minutes since the last test, and lifetime test count.

This preserves the Case-38 distinction between **event exposure** and **protection-apparatus health** before bringing in an independent fault test.

### Historical / independent practitioner record (`H/P`, source role qualified)

Nordeus Engineering reports that in **December 2014** it directly tested three named SSD models, including the **Intel DC S3500**. The article was published on **12 November 2015**.

The reported test stack was:

- Dell R420;
- H710p RAID controller;
- two SSDs under test;
- 48 GB RAM;
- CentOS 6.5;
- XFS;
- PostgreSQL 9.3 for the database test.

This is an independent practitioner / operator source, not an Intel validation document and not an academic component-certification study. Its value is precisely that it observes the named drive inside a realistic storage stack while also making that stack an explicit confounder.

---

## Nordeus hard-power-cut procedure

### `fsync` path (`H/P`)

Nordeus used `diskchecker.pl` with a second host recording what the test host said it had written. The test host performed writes followed by `fsync`; after five minutes the testers **physically unplugged server power**, waited ten minutes, powered the host back on, and verified the resulting file against the side-channel record.

The article states that each tested parameter combination was repeated **at least five times**, stopping on first failure; a combination needed at least five passes to be marked passed. The tested dimensions were:

- SSD disk cache on/off;
- filesystem barriers on/off;
- RAID controller write-back/write-through.

For the displayed highest-performance combination — disk cache **on**, barriers **off**, H710p **write-back** — both tested Intel S3500 drives are reported `OK`.

### PostgreSQL path (`H/P`)

The second path used PostgreSQL 9.3 with data checksums, split data/index activity across the two SSDs, ran `pgbench`, physically unplugged the host, waited ten minutes, restarted it, and ran `pg_dumpall` so reads would exercise checksum verification.

For the displayed Intel S3500 configuration — disk cache **on**, barriers **off**, RAID write-back — the result is reported `OK`.

The record therefore provides a named, independently operated, real-power-cut witness at both a file-`fsync` boundary and an application/database recovery boundary.

---

## Engineering reconstruction

### E — independent system-stack observation != component PLI self-test

AFh asks whether the capacitor subsystem passed a bounded health probe. Nordeus instead removes host power while real software and I/O are active and checks what survives after reboot. These are different evidence layers.

A self-test may pass while another part of the emergency path fails; conversely, a successful stack recovery does not tell us the exact capacitor discharge margin that existed during the event.

### E — named product under test != isolated component-only causality

The S3500 was not wired to a component-only power-fault bench. The observed causal path also included the H710p controller and its cache policy, SATA transport, kernel/block layer, XFS, PostgreSQL, host power behavior, and the actual drive firmware/media state.

Therefore:

```text
named S3500 present in a passing stack
    != proof that every observed success is attributable only to S3500 PLI
```

The same-stack comparison against other named drives is useful differential evidence, but it does not remove all shared-stack confounding.

### E — repeated passes in one stack != complete failure-envelope coverage

The Nordeus criterion of at least five successful repetitions is meaningful fault-injection evidence for the tested configuration. It is not equivalent to Intel's much larger first-party validation loop already recorded in Case 38, and neither establishes every possible field condition.

The article does not systematically sweep, for example:

- supply fall-time waveform;
- cut timing against every internal controller operation;
- capacitor age / SSD lifetime state;
- temperature;
- every queue depth / command mix;
- firmware revisions and capacities;
- every RAID/controller/OS/filesystem combination.

So:

```text
repeated observed pass
    != exhaustive power-fault envelope
```

### E — filesystem/database recovery success != exhaustive hidden-metadata correctness

The `fsync` test checks a concrete durable-write expectation against an external record. The PostgreSQL path checks whether the database can be traversed/dumped under checksum validation after the fault.

Those are stronger observations than "the drive enumerated after reboot", but they still do not expose every controller mapping journal, spare-area metadata structure, FTL recovery path, or latent media error.

Thus:

```text
successful post-cut application recovery
    != exhaustive proof of all hidden controller metadata
```

---

## Functional analogy / cross-case comparison

### A — Case 15 vs Case 38: durability-assurance layering only

[Case 15 — Intel SSD 320 power-loss durability](../cases/15-intel-ssd320-power-loss-durability.md) centers the emergency persistence contract and a named firmware failure boundary. Case 38 adds a later readiness/self-test layer and, with this evidence, a separate independent stack-level observation layer.

The comparison is functional:

```text
persistence mechanism / contract
    -> readiness evidence
    -> manufacturer fault-validation evidence
    -> independent stack-level fault observation
```

This is **not** a claim that SSD 320, S3500, and S3700 share the same controller, firmware, capacitor design, or direct implementation genealogy.

---

## Philosophical / project interpretation

### I — durability confidence is evidence-layered

For this repository, a useful bounded interpretation is that confidence in technical retention is itself assembled from differently scoped evidence: an interface/product contract, health state, manufacturer qualification, and independent observation under fault.

That is project interpretation, not terminology attributed to Intel or Nordeus. It also does not imply that accumulating more evidence turns an engineering guarantee into certainty.

---

## Prior art and related-repository boundary

No invention-priority claim is made here.

Fresh searches of `tmzncty/computing-archaeology` for combinations of `S3500`, `PLI`, `power loss capacitor`, and `SSD power loss fault injection` found no dedicated reusable historical module. The bounded named-product validation relation therefore stays in `technical-retention`; broader SSD power-failure-testing genealogy belongs in `computing-archaeology` if developed later.

---

## Explicit stop conditions / unsupported upgrades

This record does **not** establish:

- universal S3500 compliance under every sudden-power-loss condition;
- isolated SSD-only causality for Nordeus's passing results;
- internal identity between S3500 and S3700;
- that five successful cycles are statistically sufficient for field reliability;
- that `pg_dumpall` plus PostgreSQL checksums detect every latent storage fault;
- that a successful `fsync`-level test proves every acknowledged ATA command survives every permitted power transition;
- exact controller/FTL metadata-recovery implementation;
- invention priority for PLI, capacitor backup, `fsync` testing, or power-cut fault injection;
- direct technical genealogy from Intel SSD 320 to S3500/S3700.

---

## Sources

### Primary product document

Intel Corporation, **_Intel Solid-State Drive DC S3500 Series Product Specification_**, January 2015, order number 328860-008US.

<https://www.intel.com/content/dam/www/public/us/en/documents/product-specifications/ssd-dc-s3500-spec.pdf>

Inspected anchors:

- feature summary: enhanced power-loss data protection + capacitor self-test;
- §2.8: power-loss capacitor test via SMART `AFh`;
- SMART table: `AEh` Unexpected Power Loss vs `AFh` Power Loss Protection Failure.

### Independent practitioner / operator record

Strahinja Kustudic, Nordeus Engineering, **“Power Failure Testing with SSDs,”** published 12 November 2015; article states the testing was performed in December 2014.

<https://engineering.nordeus.com/power-failure-testing-with-ssds/>

Inspected anchors:

- named test models and December-2014 date;
- Dell R420 / H710p / CentOS 6.5 / XFS stack;
- repetition rule and cache/barrier/RAID variables;
- physical-unplug `fsync` procedure and S3500 result;
- PostgreSQL 9.3 checksum / `pg_dumpall` procedure and S3500 result.

---

## Bounded conclusion

Case 38 can now distinguish three directly evidenced assurance layers around Intel's PLI family:

1. **device-local readiness evidence** — capacitor self-test and retained AFh health state;
2. **manufacturer fault-validation evidence** — Intel's own repeated hot-unplug validation flow already grounded in the canonical case;
3. **independent named-product system-stack observation** — Nordeus's December-2014 hard-power-cut testing of Intel DC S3500.

The third layer closes the bounded “independent named-product witness” gap, but only at **system-stack scope**. Controlled component-only S3500/S3700 power-waveform testing, independent replication, lifetime/temperature sweeps, and hidden controller-metadata recovery remain open.
