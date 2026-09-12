from pathlib import Path

EVIDENCE_PATH = Path('evidence/38-intel-s3500-2014-independent-power-cut-stack-validation-deepening.md')
assert not EVIDENCE_PATH.exists(), EVIDENCE_PATH
EVIDENCE = r'''# Evidence 38B — Intel DC S3500 independent system-stack power-cut validation deepening

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
'''
EVIDENCE_PATH.write_text(EVIDENCE, encoding='utf-8')

case_path = Path('cases/38-intel-dc-s3700-pli-self-test-validation.md')
case = case_path.read_text(encoding='utf-8')
assert '38-intel-s3500-2014-independent-power-cut-stack-validation-deepening.md' not in case
marker = '## Engineering reconstruction\n'
assert marker in case
follow = r'''## Independent named-product follow-up — Intel DC S3500 system-stack power-cut observation

A bounded independent follow-up is now available in [`evidence/38-intel-s3500-2014-independent-power-cut-stack-validation-deepening.md`](../evidence/38-intel-s3500-2014-independent-power-cut-stack-validation-deepening.md).

Intel's January-2015 S3500 product specification independently anchors `Enhanced power-loss data protection`, the power-loss capacitor self-test, and the separation between `AEh` unexpected-power-loss history and `AFh` protection-health state. Nordeus Engineering then supplies a different source role: it reports **December-2014 hard-power-cut testing of a named Intel DC S3500** inside a Dell R420 / H710p / CentOS 6.5 / XFS stack. Its `fsync` test used an external side-channel record, physically unplugged the server, waited ten minutes, rebooted, and verified the file; its PostgreSQL 9.3 path used data checksums and `pg_dumpall` after the same class of hard cut. The displayed S3500 configuration with disk cache on, barriers off, and RAID write-back is reported `OK` in both test families, with tested parameter combinations requiring at least five successful repetitions to count as passed.

This closes only the **independent named-product witness** part of the old evidence debt. It is explicitly **system-stack evidence**, not isolated SSD-only certification: RAID-controller behavior, software, host power transition, and drive state all remain in the causal path. `>=5 observed passes != complete failure-envelope coverage`, and successful filesystem/database recovery does not expose every hidden FTL/controller-metadata path.

'''
case = case.replace(marker, follow + marker, 1)

old = '''### E — manufacturer validation ≠ independent compliance evidence

Intel's 7000-repeat validation flow is meaningful first-party evidence for the test method Intel describes. It is not an independent field study of every shipped device, nor does it identify the anonymized FAST '13 devices from Case 15.
'''
assert old in case
new = old + r'''
### E — independent system-stack observation ≠ isolated SSD-only causality

Nordeus supplies an independent named-product fault observation, but the S3500 is tested inside a Dell/H710p/Linux/XFS/PostgreSQL stack rather than on an isolated component bench. A passing stack is evidence about that tested composition; it does not prove that every successful outcome is attributable only to the drive-local PLI mechanism.

### E — repeated pass ≠ complete power-fault envelope

Nordeus requires at least five passes for a parameter combination and reports success for the displayed S3500 configuration. That is useful independent fault-injection evidence, but it does not sweep supply waveform, cut timing against every internal operation, temperature, age, firmware, or every host/controller/software composition.
'''
case = case.replace(old, new, 1)

source_marker = '---\n\n## Status\n'
assert source_marker in case
source_add = r'''### Independent practitioner — Nordeus S3500 power-cut test

Strahinja Kustudic, Nordeus Engineering, **“Power Failure Testing with SSDs,”** published 12 November 2015; the article states testing was performed in December 2014.

<https://engineering.nordeus.com/power-failure-testing-with-ssds/>

Directly inspected:

- named Intel DC S3500 test subject and test date;
- Dell R420 / H710p / CentOS 6.5 / XFS stack;
- `fsync` side-channel + physical-unplug procedure;
- PostgreSQL 9.3 checksums + `pg_dumpall` recovery procedure;
- at-least-five-pass rule and displayed S3500 results.

See the bounded evidence record for source-role and causality limits.

'''
case = case.replace(source_marker, source_add + source_marker, 1)

old_status = '''**`grounded`** for the bounded PLI-health / self-test / manufacturer-validation relation.

The sources are unusually strong for the historical/product layer because they directly expose not only the power-fail mechanism but also the drive's own health state, self-test procedure, operator-visible control surface, and Intel's validation workflow. The unresolved next step is deliberately different: **independent named-product fault-compliance evidence or deeper controller-metadata recovery**, not another repetition of the capacitor-transfer mechanism.'''
assert old_status in case
new_status = '''**`grounded`** for the bounded PLI-health / self-test / manufacturer-validation relation, now with an independent named-product **system-stack** power-cut witness.

The first-party sources directly expose the power-fail mechanism, drive health state, self-test procedure, operator-visible control surface, and Intel's validation workflow. Nordeus adds independent December-2014 hard-power-cut observations of a named Intel DC S3500 in a documented storage/software stack. That closes the earlier independent named-product witness debt only at stack scope. Remaining work is narrower: **controlled component-only S3500/S3700 power-waveform replication, lifetime/temperature coverage, and deeper controller-metadata recovery evidence**, not another repetition of the capacitor-transfer mechanism.'''
case = case.replace(old_status, new_status, 1)
case_path.write_text(case, encoding='utf-8')

roadmap_path = Path('ROADMAP.md')
roadmap = roadmap_path.read_text(encoding='utf-8')
assert 'Case 38 Intel DC S3500 independent power-cut stack validation' not in roadmap
phase = '## Phase 2 — Build missing technical bridges\n\n'
assert phase in roadmap
bullet = "- [x] **Case 38 Intel DC S3500 independent power-cut stack validation:** [`cases/38-intel-dc-s3700-pli-self-test-validation.md`](cases/38-intel-dc-s3700-pli-self-test-validation.md) + [`evidence/38-intel-s3500-2014-independent-power-cut-stack-validation-deepening.md`](evidence/38-intel-s3500-2014-independent-power-cut-stack-validation-deepening.md) add Nordeus's December-2014 named-product hard-power-cut observation above Intel's first-party PLI self-test and validation evidence. The slice separates device-local capacitor health, manufacturer validation, independent system-stack fault observation, and universal compliance; records `named product in a passing stack != isolated SSD-only causality` and `repeated pass != complete power-fault envelope`; and leaves controlled component-only waveform/lifetime testing plus hidden controller-metadata recovery open. Broader SSD fault-testing genealogy remains for `computing-archaeology`.\n\n"
roadmap = roadmap.replace(phase, phase + bullet, 1)
roadmap_path.write_text(roadmap, encoding='utf-8')

index_path = Path('CASE_INDEX.md')
idx = index_path.read_text(encoding='utf-8')
assert '- **3527 —' in idx
assert '- **3528 —' not in idx
add = r'''

## Case 38 — Intel DC S3500 independent power-cut stack-validation deepening findings

Deepening record: [`evidence/38-intel-s3500-2014-independent-power-cut-stack-validation-deepening.md`](evidence/38-intel-s3500-2014-independent-power-cut-stack-validation-deepening.md).

- **3528 — S3500 first-party PLI contract:** Intel's January-2015 S3500 product specification lists enhanced power-loss data protection and a power-loss capacitor self-test, grounding the named product's protection/readiness surface independently of the later operator test. (`H/P`)
- **3529 — unexpected-power-loss history != PLI-health history:** the S3500 SMART table keeps `AEh` unclean-shutdown count separate from `AFh` capacitor-test result/recency/lifetime count, preventing event exposure from being read as protection failure. (`H/P, E`)
- **3530 — independent named S3500 fault witness:** Nordeus reports direct December-2014 power-failure testing of Intel DC S3500; the article was published 12-Nov-2015 and is an operator/practitioner source rather than Intel validation. (`H/P`, source-role qualified)
- **3531 — tested product is embedded in a documented stack:** Dell R420, H710p RAID, two SSDs, CentOS 6.5, and XFS are part of the reported test environment, so the observation is explicitly system-stack scoped. (`H/P`)
- **3532 — physical power removal is the injected fault:** the reported procedures unplug host power, wait ten minutes, reboot, and verify, supplying real hard-power-cut evidence rather than only a synthetic capacitor self-test. (`H/P`)
- **3533 — fsync durable-write witness:** Nordeus's `diskchecker.pl` path sends an external record of writes, calls `fsync`, then verifies after power cut; the displayed S3500 cache-on / barriers-off / RAID-write-back configuration is `OK`, with combinations requiring at least five passes to count as passed. (`H/P`)
- **3534 — PostgreSQL recovery/checksum witness:** the PostgreSQL 9.3 path uses data checksums, `pgbench`, physical power removal, reboot, and `pg_dumpall`; the displayed S3500 cache-on / barriers-off / RAID-write-back configuration is reported `OK`. (`H/P`)
- **3535 — independent stack fault observation != component PLI self-test:** AFh probes bounded capacitor readiness, while a live-workload hard cut exercises a wider failure path; neither substitutes for the other. (`E`)
- **3536 — named product under test != isolated SSD-only causality:** H710p/cache policy, SATA, kernel, XFS/PostgreSQL, host power behavior, firmware, and media state remain in the causal path even when the S3500 is the named drive. (`E, X`)
- **3537 — >=5 repeated passes != complete failure-envelope coverage:** the operator repetition rule is useful evidence for tested configurations but does not sweep waveform, timing against every internal operation, temperature, lifetime/age, firmware, or every stack. (`E, X`)
- **3538 — filesystem/database recovery success != exhaustive hidden-metadata correctness:** side-channel `fsync` verification and checksum-aware PostgreSQL traversal are stronger than simple reboot success, but they do not expose every FTL/controller metadata path or latent media fault. (`E, X`)
- **3539 — Case 15 ~ Case 38 only as durability-assurance layering:** SSD 320's persistence/failure boundary and Case 38's readiness/manufacturer/independent-observation layers can be compared functionally, without asserting shared controller/firmware/capacitor design or direct product genealogy. (`A, X`)
- **3540 — durability confidence as evidence layers is project interpretation:** contract, health state, manufacturer qualification, and independent fault observation can be treated as differently scoped evidence for retention confidence; Intel and Nordeus are not credited with this repository vocabulary. (`I, X`)
- **3541 — independent S3500 witness != universal compliance:** the Nordeus result must not be upgraded into proof of all S3500 units, all power-loss conditions, S3700 identity, every acknowledged ATA write, or every higher-layer durability invariant. (`X`)
'''
idx = idx.rstrip() + add + '\n'
index_path.write_text(idx, encoding='utf-8')

for tmp in [
    Path('.github/workflows/tmp-case38-s3500-independent-validation.yml'),
    Path('.github/scripts/tmp_case38_s3500_integrate.py'),
]:
    assert tmp.exists(), tmp
    tmp.unlink()
