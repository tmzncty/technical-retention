# Case 36 Grounding Record — Cai et al. 2012 Flash Correct-and-Refresh

## Purpose

This record grounds [`../cases/36-nand-flash-correct-and-refresh-maintenance.md`](../cases/36-nand-flash-correct-and-refresh-maintenance.md).

The promotion question is deliberately narrow:

> Is there strong period-primary evidence for a NAND-Flash retention regime in which a nonvolatile medium is periodically read, ECC-corrected, and reprogrammed/remapped in order to keep time/wear-dependent retention errors inside a controller-level recoverability margin?

**Result:** yes, for the **2012 FCR proposal/evaluation**. The evidence is strong enough for `grounded` status because the primary paper directly specifies the mechanism, error model, controller/FTL implementation locus, side effects, adaptive scheduling state, evaluation method, and explicit limitations. The case does **not** claim commercial deployment or universal NAND semantics.

## Primary source identity

Yu Cai, Gulay Yalcin, Onur Mutlu, Erich F. Haratsch, Adrian Cristal, Osman S. Unsal, and Ken Mai, **“Flash Correct-and-Refresh: Retention-Aware Error Management for Increased Flash Memory Lifetime,”** *Proceedings of the 30th IEEE International Conference on Computer Design (ICCD)*, Montreal, September 2012, pp. 94–101, DOI `10.1109/ICCD.2012.6378623`.

Directly inspected author-hosted PDF:

<https://users.ece.cmu.edu/~omutlu/pub/flash-correct-and-refresh_iccd12.pdf>

Independent/institutional bibliographic controls:

- ETH Zurich Systems Group: <https://publications.systems.ethz.ch/publication/791>;
- Carnegie Mellon KiltHub record: <https://kilthub.cmu.edu/articles/journal_contribution/Flash_Correct-and-Refresh_Retention-Aware_Error_Management_for_Increased_Flash_Memory_Lifetime/6468821>.

## Directly inspected anchors

### Printed p. 1 — abstract and proposal summary

The abstract directly establishes:

- the bounded motivation: increasing NAND error rate with P/E wear;
- the paper's observation that retention errors, caused by charge loss over time, dominate the tested regime;
- the named technique `Flash Correct-and-Refresh (FCR)`;
- the core operation: periodically read, correct, then `reprogram (in-place) or remap` before errors exceed simple ECC;
- the evaluation boundary: detailed **SSD simulation** driven by measured experimental characterization data;
- the reported `46x average lifetime improvement` as an evaluation result, not a field-deployment measurement.

The introduction further says FCR can be implemented in device-driver software or NAND-controller firmware and can leverage existing read/write/remapping functions.

**Use:** H/P for the historical proposal and its own stated evaluation; X against claims of production deployment.

### Printed pp. 1–2 — SSD/FTL and error-path context

The paper describes the SSD controller as running an FTL that includes address mapping, wear leveling, and garbage collection, with an ECC engine between raw Flash data and host-visible corrected data.

Its retention-error definition is specific: an already-programmed floating-gate cell gradually loses charge, threshold state can shift, and a read may return the wrong raw value. ECC correction occurs in the controller; UBER remains possible when raw errors exceed correction capability.

**Use:** H/P for the layered relation `cell charge/readout → ECC → corrected logical payload`, and E for the reconstruction that raw-state degradation can precede logical data loss.

### Printed p. 3 — required storage time and remapping-based FCR

Figure 2 and §IV use the measured/modelled 3x-nm MLC data to show that guaranteed storage time and P/E-cycle lifetime trade against one another for a fixed ECC. The paper gives a concrete example in which a 512-bit BCH code corresponds to roughly 3k P/E cycles at a three-year storage requirement and roughly 150k at a three-day requirement, then proposes refreshing every three days to synthesize a longer logical storage interval.

**Boundary:** these values are a paper-specific example, not universal NAND constants.

§IV.A directly specifies remapping-based FCR:

1. select valid data needing refresh;
2. read pages into the SSD controller;
3. correct accumulated errors with ECC;
4. select a new free block;
5. program corrected data there;
6. remap the logical address.

The paper says this leverages wear-leveling and garbage-collection mechanisms already present in contemporary systems.

It also gives the first important negative result: more frequent remapping creates extra erase/reclaim cycles, and beyond an inflection point increasing refresh rate can reduce lifetime.

**Use:** H/P for mechanism and side effect; E/A for comparison to Case 04 mapping-triggered identity continuity.

### Printed pp. 4–5 — in-place reprogramming and hybrid repair

§IV.B explains the physical asymmetry used by in-place FCR. Retention errors in the bounded model move threshold voltage toward lower-charge states. ISPP can add electrons and restore the intended state without an erase operation.

The same mechanism has explicit limits:

- in-place programming cannot remove electrons;
- program-interference errors can shift cells in the opposite direction;
- repeated reprogramming can introduce additional program errors;
- once accumulated errors approach ECC capability, the next refresh may fail to recover the page.

Hybrid FCR therefore monitors right-shift/program-error count and uses in-place reprogramming below a threshold while remapping to a new block above that threshold.

**Use:** H/P for asymmetric repair and hybrid fallback; E for `maintenance operation ≠ error-neutral repair`.

### Printed p. 5 — adaptive-rate FCR and retained maintenance metadata

§IV.C says refresh need not have one fixed period. In the paper's measured regime, early-life retention error rate can remain below the simplest BCH correction bound; adaptive-rate FCR therefore starts with no refresh and increases refresh frequency as P/E cycles accumulate.

The paper explicitly says this requires per-block P/E-cycle tracking and that this information is already maintained for wear leveling.

§IV.D adds that:

- FCR needs no hardware changes but does require FTL/software/firmware changes;
- per-block validity and P/E-cycle information are reused;
- Flash must be powered to perform refresh;
- refresh may be background/idle work and can be deprioritized/interrupted to reduce response-time interference;
- environmental changes such as temperature can alter retention-error rate, and the policy can adjust from observed error-rate changes.

**Use:** H/P for controller/FTL locus, adaptive cadence, power/service cost, and metadata dependence.

### Printed pp. 6–7 — evaluation boundary and maintenance trade-off

The evaluation uses DiskSim with SSD extensions, real workload traces, and energy/error inputs derived from an experimental Flash platform. The paper explicitly notes that multi-year full-lifetime traces were not available and that lifetime is extrapolated from simulated wear.

For some read/write-balanced and read-heavy workloads, remapping-based FCR can lose the benefit of more frequent refresh because additional erase cycles dominate. This is direct evidence that retention work has a wear cost and that `more refresh` is not monotonically equivalent to `more lifetime`.

**Use:** H/P for evaluation method and trade-off; X against treating `46x` as directly measured multi-year production lifetime.

## Later boundary evidence — not folded into 2012 semantics

Yu Cai, Yixin Luo, Erich F. Haratsch, Ken Mai, and Onur Mutlu, **“Data Retention in MLC NAND Flash Memory: Characterization, Optimization, and Recovery,”** HPCA 2015, pp. 551–563, DOI `10.1109/HPCA.2015.7056062`.

Institutional abstract:

<https://www.istc-cc.cmu.edu/publications/papers/2015/flash-memory-data-retention_hpca15_abs.shtml>

This later work characterizes real 2y-nm MLC chips and reports that threshold-voltage distributions and optimal read-reference voltage change with retention age, with different regions able to have different retention ages.

**Use only as a later boundary:** it reinforces that physical retained charge, read interpretation, and controller recovery parameters can change differently over time. It is not evidence that the 2012 FCR algorithm was deployed or that every later NAND generation uses the same policy.

## Claim-type ledger

| Claim | Label | Grounding |
| --- | --- | --- |
| FCR is a named 2012 ICCD proposal | H/P | primary paper + institutional bibliographic records |
| Retention errors arise from charge loss / threshold drift in the bounded 3x-nm MLC regime | H/P | primary paper §§I, III |
| FCR reads, ECC-corrects, then reprograms/remaps before correctability is exhausted | H/P | abstract + §IV |
| Remapping FCR changes the serving physical block while preserving logical designation | H/P/E | §IV.A + Case-04 comparison |
| In-place reprogramming is physically asymmetric and can create program-interference errors | H/P | §IV.B |
| Hybrid FCR switches to remapping when the in-place path's error evidence becomes too large | H/P | §IV.B |
| Adaptive FCR uses P/E-cycle state to change refresh frequency | H/P | §IV.C–D |
| Nonvolatile medium can still participate in maintenance-dependent reliable retention | E | reconstruction bounded to the FCR target/error model |
| Flash FCR is DRAM refresh | X/A | only a functional analogy is allowed; the paper explicitly distinguishes them |
| 46x is a measured production-drive lifetime result | X | evaluation is simulation driven by measured characterization/workload data |
| FCR was universally deployed in commercial SSDs | X | not established by source set |
| The authors' “to our knowledge” priority statement proves invention priority | X | broader prior-art search required |

## Cross-case consequences

The evidence is strong enough to add the following controlled separations to `CASE_INDEX.md`:

- nonvolatile medium ≠ maintenance-free reliable retention at a specified error target;
- raw physical error accumulation ≠ immediate logical payload loss;
- ECC-correctability margin ≠ indefinite retention margin;
- long logical retention interval ≠ one uninterrupted physical-embodiment interval;
- Flash FCR refresh ≠ DRAM refresh;
- retention maintenance ≠ location stability;
- more maintenance ≠ more lifetime;
- maintenance operation ≠ error-neutral repair;
- refresh cadence ≠ one fixed medium constant;
- payload retention can depend on retained maintenance metadata;
- FCR proposal/evaluation ≠ commercial deployment;
- retention refresh ≠ integrity scrub.

## Related-repository audit

[`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) was checked before creating this case. Its current index and audit identify Flash-controller history as a technical bridge still needing deeper period sourcing; there is no dedicated FCR retention case to reuse. Therefore:

- **general NAND/SSD controller history** should be developed there;
- **the cross-mechanism retention comparison** belongs here.

Case 36 links to Case 04 rather than rewriting its 1993 mapping history, and to Cases 03/21/33–35 rather than calling all semiconductor maintenance `refresh` in one undifferentiated sense.

## Promotion decision

**Promote directly to `grounded`.**

Reason:

- one strong peer-reviewed primary paper directly supplies terminology, mechanism, timing/policy state, error model, failure trade-offs, implementation locus, and evaluation limits;
- institutional publication records independently control bibliographic identity;
- later experimental work supplies a bounded read/retention-age cross-check without being projected backward;
- unsupported deployment and invention-priority claims are explicitly rejected;
- related-repository duplication has been checked.

Remaining work is **not a promotion blocker**: commercial-controller deployment archaeology, later 3D-NAND refresh/read-retry interaction, manufacturer-specific refresh commands, and broader controller reliability history remain separate future cases or belong in `computing-archaeology`.
