# Case 52 Deepening — Micron 2006 Read-Disturb Failure Taxonomy and Maintenance Choices

## Status

**`bounded deepening complete`** for the 2006 Micron design-guidance slice described here.

Canonical case: [`../cases/52-nand-flash-read-disturb-access-induced-decay.md`](../cases/52-nand-flash-read-disturb-access-induced-decay.md).

Parent grounding record: [`52-cai-2009-2015-nand-read-disturb-grounding.md`](52-cai-2009-2015-nand-read-disturb-grounding.md).

## Why this slice exists

Case 52 already has an early Fujitsu device-level read-disturb patent, a 2008 NASA/JPL qualification witness, a 2009-priority controller patent, a 2013 FTL paper, and the 2015 Cai et al. commercial-chip characterization. What it lacked was an early **manufacturer design guide that explicitly classifies read disturb as a recoverable temporary failure and then gives system-level maintenance choices for repeatedly read NAND data**.

Micron's **TN-29-17, _NAND Flash Design and Use Considerations_**, Rev. A, August 2006, supplies that missing layer.

The bounded question is:

> Before the later experimental and controller literature used in Case 52, did a NAND manufacturer already distinguish read-disturb errors from permanent bad-block identity, and did it already describe multiple system policies for preventing repeatedly read data from exhausting ECC margin?

For this source, the answer is **yes**.

The important historical result is not merely that Micron knew the term `Read Disturb`. The note separates three decisions that are easy to collapse in later summaries:

```text
an error mechanism is observed
    !=
the carrier has a permanent bad-block identity
    !=
which maintenance policy the system chooses
```

## Source and provenance

### Primary technical content, surviving mirror

Micron Technology, Inc., **TN-29-17: _NAND Flash Design and Use Considerations_**, Rev. A, **8/06**.

A surviving copy of the Micron-authored document is available through a third-party document mirror. The visible document itself carries Micron's title, document number, copyright, revision, and product-support language. The historical Micron download URL was:

`http://download.micron.com/pdf/technotes/nand/tn2917.pdf`

Surviving mirror / extracted copy used for the bounded text inspection:

- <https://www.scribd.com/document/919510643/design-and-use-considerations>

A later surviving copy of the same Micron technical-note family is available as Rev. C, 11/18:

- <https://borecraft.com/PDF/Datasheets%2C%20WP%2C%20Specs/tn2917.pdf>

The evidence status is therefore:

> **manufacturer-primary content on surviving non-Micron hosting**.

It is stronger for what Micron's note says than for proving the complete publication/archive history of every TN-29-17 revision.

### Date corroboration

Multiple later patent/reference records cite Micron's _NAND Flash Design and Use Considerations_ at the historical Micron URL and date it **1 August 2006**. The Rev. A document itself prints `Rev. A 8/06`.

A later copy prints `Rev. B 4/10`; another surviving copy prints `Rev. C 11/18`. This record does **not** claim a paragraph-by-paragraph genealogy across every revision. The historical claim here is bounded to the Rev. A wording inspected and to later continuity only where the later surviving text is directly consistent.

### Current Micron support continuity — separate evidence class

Micron's current official sales/support FAQ still describes `READ disturb` as occurring when the same data are read repeatedly and recommends refreshing data to reduce repeated access. The same FAQ separately gives terse guidance to mark blocks bad in response to `READ errors`.

Official current source:

- <https://www.micron.com/sales-support/sales/faqs>

Those FAQ answers are useful as present-day continuity evidence, but they are **not** used to rewrite the 2006 taxonomy. `READ error` in a short support answer is not automatically identical in scope to TN-29-17's specifically classified temporary `Read Disturb` failure.

## Historical record

### H/P — Micron explicitly separates permanent from temporary NAND failures

TN-29-17 first divides NAND failures into **permanent** and **temporary** categories.

For permanent failures, the note describes bits that are stuck in a state and cannot be altered by PROGRAM or ERASE. It says that when a permanent failure occurs, the block must be added to the bad-block table and avoided in future use.

For temporary failures, it says the failing location can be recovered and that **the block need not be added to the bad-block table**.

This establishes a manufacturer-primary control distinction:

```text
failure observed
    !=
permanent carrier retirement
```

and more specifically:

```text
temporary error condition
    !=
bad-block-table admission
```

The note's classification is period engineering vocabulary, not a project-created taxonomy.

### H/P — Micron places Read Disturb inside the temporary-failure category

Within the temporary-failure section, TN-29-17 identifies `Read Disturb` as an error in which bits can change during a READ operation on pages in the same block other than the page being read. It says large numbers — hundreds of thousands or millions — of reads to individual pages before an ERASE can exacerbate the error.

For this failure mode, the note's prescribed recovery is to **erase the block where the error occurred and reprogram the data to that block**.

That wording matters because it is incompatible with an automatic equation:

```text
read-disturb error
    ==
permanently bad physical block
```

The 2006 guide instead presents a path in which the **same block can be renewed and reused** after erase/reprogram.

This does not prove that every real read error on every Micron NAND part was recoverable. It proves the narrower historical design-guidance classification in this technical note.

### H/P — the note makes repeated executable-code reads a system-design problem

TN-29-17 then leaves the failure taxonomy and discusses a concrete system pattern: NAND used to hold executable code under **demand paging**.

The note warns that systems may repeatedly access code stored in one physical area of NAND. If code is loaded once and then assumed to remain indefinitely readable without a maintenance path, the system can overlook NAND's repeated-read susceptibility.

The important layer change is:

```text
physical read-disturb mechanism
    ->
software / memory-architecture access pattern
    ->
retention-maintenance obligation
```

This is not an SSD FTL claim. The note is giving design guidance for systems using raw NAND.

### H/P — Micron gives three distinct ways to reduce the repeated-read hazard

The note's “Correcting Errors Due to Frequent Data Access” section gives three strategies.

**1. Mimic a Hard Drive.** Provide enough volatile memory to hold all executable code so the NAND copy is read only once on each system power-on.

**2. Build in Redundancy.** Keep a master copy and a working copy in separate NAND blocks. After a system-designated number of reads to the working copy, erase/replace the working copy with a fresh copy from the master.

**3. Use More Powerful ECC.** Use stronger ECC than the NAND data sheet requires, define a threshold below the ECC-correctable limit, and when that threshold is reached, move the data to another block and continue reading from the new location.

These are not three names for one hidden controller algorithm. They are architecturally different ways to manage the same broad risk.

The source therefore directly supports:

```text
same read-disturb risk
    !=
one mandatory maintenance topology
```

and:

```text
avoid repeated NAND reads
    !=
periodically renew the same logical object
    !=
relocate before ECC exhaustion
```

### H/P — one policy uses read count as a system-chosen maintenance threshold

The redundancy strategy says the working copy is replaced after a **designated number of reads, as determined by the system**.

That wording is unusually useful for Case 52. It shows that a read count can be treated as a maintenance clock without implying that the number is a universal physical failure constant.

Thus, already in this 2006 manufacturer guide:

```text
read count as policy input
    !=
universal device failure threshold
```

This sits cleanly beside the later NASA/JPL 2008 negative result, where large prescribed read counts did not reproduce a disturb failure in the tested devices.

### H/P — the ECC strategy places maintenance before the hard correction boundary

Micron's stronger-ECC strategy does not tell the system to wait until ECC has already failed. It recommends a threshold for the maximum number of bad bits **under the ECC-correctable limit**, then migration when that threshold is met.

That establishes an early vendor-design version of a recurring technical-retention relation:

```text
currently correctable payload
    !=
no maintenance required yet
```

and:

```text
maintenance threshold
    !=
uncorrectable-error boundary
```

The exact threshold remains system- and implementation-dependent in the inspected note.

## Engineering reconstruction

### E — error classification and carrier authority are different state

The note's strongest contribution to this repository is a separation between the **condition of the data** and the **future admissibility of the physical block**.

A temporary read-disturb failure can require erase/reprogram while leaving the block eligible for reuse. A permanent failure changes the block's future allocation status and requires bad-block-table exclusion.

Therefore:

```text
payload error state
    !=
carrier-retirement state
```

and:

```text
recovery obligation
    !=
permanent exclusion obligation
```

This distinction is directly relevant to Case 78's later bad-block-marker/BBT evidence, but the cases remain separate: Case 52 is about access-induced decay and maintenance; Case 78 is about persistent carrier classification and exclusion authority.

### E — erase/reprogram can be renewal rather than retirement

Within the temporary read-disturb path, erase/reprogram removes the accumulated state that made the current contents unsafe and recreates the logical payload.

The physical operation `ERASE` therefore cannot be assigned a single repository-wide semantic meaning.

In this source:

```text
erase + reprogram
    ->
renew a temporarily degraded block
```

In Case 78's bad-block evidence:

```text
erasing a bad-block marker
    ->
can destroy exclusion evidence
```

The operation is similar; the state and authority context are not.

### E — changing the access architecture can itself be retention maintenance

Micron's first strategy does not repair NAND more cleverly. It changes **where repeated execution reads happen** by keeping code in volatile memory after an initial NAND load.

This is a useful system-level result:

```text
reduce physical access frequency
    ->
reduce access-induced retention stress
```

The retained master copy in NAND still matters across power loss, while volatile RAM absorbs hot execution reads during the powered session.

That makes DRAM capacity and boot/load policy part of the bounded retention design without making DRAM itself the durable medium.

### E — redundancy separates authoritative source from expendable hot embodiment

The master/working-copy strategy creates a simple authority relation:

```text
master copy
    -> source for renewal
working copy
    -> hot embodiment allowed to accumulate read stress
```

The note does not use the project terms `authority` or `embodiment`. They are engineering reconstruction.

The important result is functional: repeated access can be directed at a replaceable physical instance while another copy supplies the state needed to renew it.

This is not evidence for one later SSD FTL implementation.

### E — stronger ECC converts correction margin into an intervention signal

The third strategy explicitly treats some ECC-correctable errors as **maintenance evidence**, not merely errors to hide from the application.

That is a two-layer use of ECC:

```text
ECC as current reconstruction mechanism
    +
ECC error count/margin as future-maintenance signal
```

The note does not specify the exact counter format, persistence mechanism, or controller metadata layout. Those would require product/controller evidence.

### E — the three strategies spend different resources

The strategies trade different resources:

- more volatile memory reduces repeated NAND reads;
- duplicate NAND copies consume storage capacity and require renewal work;
- stronger ECC consumes coding/compute margin and uses relocation before the correction limit.

Therefore a high-level statement such as “refresh the data” hides materially different mechanisms and budgets.

For technical-retention purposes:

```text
same preservation objective
    !=
same retained control state
    !=
same resource cost
    !=
same failure boundary
```

## Cross-case comparison

### Case 78 — bad-block marker / BBT

Case 78's KIOXIA 2018–2019 product guidance states that random/read bit errors do not automatically mean a block is bad and distinguishes read-recovery/rewrite behavior from program/erase-status-failure block replacement.

TN-29-17 gives an earlier manufacturer design-guide witness for a compatible but not identical distinction: a `Read Disturb` failure is classified as temporary and the block need not enter the bad-block table, whereas a permanent failure does require bad-block-table exclusion.

The safe cross-case result is:

```text
read-path degradation
    !=
automatic permanent-retirement authority
```

No Micron → KIOXIA genealogy is asserted.

### Case 36 — Flash Correct-and-Refresh

Case 36 later formalizes proactive renewal before retention errors exceed ECC capability. Micron's 2006 note already recommends using an ECC threshold below the correction limit to trigger movement for repeated-read stress.

The functional analogy is strong at the policy level:

```text
intervene before ECC exhaustion
```

but the trigger differs:

```text
Case 36: retention age / wear
Case 52 Micron slice: repeated-read disturbance / ECC-error threshold
```

This is not evidence that Cai et al.'s FCR derived from TN-29-17.

### Case 67 — later adaptive 3-D NAND read reclaim

Case 67 uses a later SK hynix disclosure in which read-count proxies and ECC qualification participate in conditional reclaim for 3-D NAND.

Micron 2006 is useful prior context for the generic system-policy family — count accesses, observe error margin, renew or move data — but it does not establish the later 3-D policy's implementation or invention genealogy.

### Case 04 — logical identity and physical relocation

Micron's stronger-ECC strategy can move data to another block. Case 04 supplies the broader mapped-Flash distinction between logical identity and physical embodiment.

The Case 52 source does not require an SSD-style FTL to make its point; raw-NAND system software can also maintain a relation between the object being preserved and a changed physical location.

## Current Micron FAQ — a vocabulary warning, not a retroactive rewrite

Micron's current official FAQ contains two terse pieces of guidance:

- repeated reading can cause `READ disturb`, and refreshing data is recommended to mitigate it;
- a separate question asks whether blocks should be marked bad due to `READ errors`, and answers yes.

Those statements should **not** be forced into a contradiction with TN-29-17 without a matching device/context definition of `READ errors`.

The 2006 note defines a specific temporary `Read Disturb` category and explains its recovery. The current FAQ's short `READ errors` answer does not expose whether it means persistent uncorrectable read failures, all corrected reads, a product-specific policy, or something else.

Therefore:

```text
same vendor + similar words across time
    !=
same scoped engineering term
```

This is a useful anti-anachronism constraint for future product-level work.

## Historical / engineering / analogy / interpretation split

### Historical record

Micron's 2006 TN-29-17:

- explicitly classifies failures as permanent or temporary;
- places Read Disturb in the temporary category;
- says the block need not be added to the bad-block table for temporary failures;
- prescribes erase/reprogram recovery for read disturb;
- gives demand-paging/repeated-code-read as a design problem;
- gives three mitigation strategies: volatile-memory residency, redundant master/working copies with read-count renewal, and stronger ECC with a pre-limit migration threshold.

### Engineering reconstruction

This repository infers that:

- error state and carrier-retirement authority are different;
- a read count can function as a maintenance clock without being a universal failure clock;
- ECC margin can be both reconstruction capacity and maintenance evidence;
- changing the memory/access architecture can reduce physical retention stress;
- renewal in place and relocation are distinct maintenance policies.

### Functional analogy

Case 36, Case 67, and Case 78 contain later mechanisms with similar preservation functions. They are comparison targets, not genealogy claims.

### Philosophical interpretation

The bounded conceptual observation is that **continued identity of stored information can depend on choosing when to stop trusting its current embodiment, even before the embodiment has become permanently defective**.

That sentence is project interpretation. It is not Micron's historical vocabulary.

## Explicit non-claims

This record does **not** claim that:

1. Micron discovered read disturb in 2006.
2. TN-29-17 is the first publication to use the term `Read Disturb`.
3. Every NAND read error is temporary.
4. Every read-disturb event is recoverable by erase/reprogram.
5. A block that passes one erase/reprogram cycle is guaranteed healthy forever.
6. Hundreds of thousands or millions of reads form a universal failure threshold.
7. Micron's system-designated read count is a NAND-device specification limit.
8. The stronger-ECC strategy waits until ECC is exhausted; the note explicitly proposes a lower intervention threshold.
9. The three strategies are implemented together in one commercial controller.
10. Demand paging is historically unique to NAND or was invented by Micron.
11. Moving data to another block proves an SSD-style FTL implementation.
12. The 2006 note proves the detailed physical `Vpass` mechanism later characterized by Cai et al.; that mechanism is grounded elsewhere in Case 52.
13. The current Micron FAQ's broad `READ errors` wording has the same scope as the 2006 `Read Disturb` temporary-failure category.
14. KIOXIA's later bad-block guidance derives from Micron TN-29-17.
15. Case 36 FCR or Case 67 adaptive reclaim derives from this technical note.
16. Erase/reprogram is free: it consumes time, write/erase work, and potentially endurance, even where the note treats the failure as recoverable.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Micron TN-29-17 Rev. A is dated 8/06 and was distributed from a Micron technical-note URL | H/P | printed Rev. A date + later bibliographic/patent references to historical Micron URL |
| TN-29-17 separates permanent and temporary NAND failures | H/P | direct manufacturer-authored technical-note text |
| Permanent failures require bad-block-table exclusion in the note | H/P | direct text |
| Temporary failures can be recoverable without adding the block to the BBT | H/P | direct text |
| Micron classifies Read Disturb as a temporary failure in this note | H/P | direct text |
| The note prescribes erase + reprogram of the affected block for read disturb | H/P | direct text |
| Repeated demand-paging reads can create a NAND reliability problem | H/P | direct best-practices section |
| The note proposes volatile residency, redundant working-copy renewal, and stronger-ECC/pre-limit migration as distinct strategies | H/P | direct best-practices section |
| Read count is a universal physical failure threshold | X | the note says the designated count is determined by the system; NASA/JPL later gives an explicit negative-result boundary |
| ECC-correctable state means no maintenance is warranted | X | the stronger-ECC strategy proposes intervention below the ECC correction limit |
| Read-disturb failure automatically creates permanent bad-block identity | X | contradicted by the note's temporary-failure classification |
| The same block may be erased/reprogrammed and reused after the bounded temporary failure | H/P/E | direct recovery wording; engineering interpretation limited to this source's guidance |
| Current Micron FAQ wording can be used to redefine the 2006 taxonomy | X | scopes are not shown to be identical |

## Remaining evidence debt

This slice closes the early manufacturer **design-guidance / failure-taxonomy** gap for Case 52. It does not close the broader history.

Useful future work remains:

- obtain a first-party archived Micron copy of Rev. A 8/06 or a trustworthy web-archive capture rather than relying on surviving third-party document hosting;
- diff Rev. A, Rev. B, and Rev. C to establish when wording changed rather than assuming revision continuity;
- bind the guidance to a named Micron NAND product/data sheet and its exact ECC/read-disturb specification;
- find controller/firmware traces showing the recommended read counter or ECC threshold in an implemented product;
- characterize when a temporary read-disturb condition is escalated to permanent retirement after unsuccessful recovery;
- reconcile the current FAQ's terse `READ errors` bad-block advice with a product-specific error-management document;
- find field evidence of the demand-paging / redundant-working-copy strategy in a deployed system.

## Related repositories

A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `TN-29-17` and `read disturb` found no dedicated historical module to reuse. A broader history of NAND controller evolution and demand-paged embedded systems belongs there; this record stays bounded to the retention-specific failure classification and maintenance choices.

## Sources

1. Micron Technology, Inc., **TN-29-17: _NAND Flash Design and Use Considerations_**, Rev. A, 8/06. Historical first-party URL recorded in contemporary/later references: `http://download.micron.com/pdf/technotes/nand/tn2917.pdf`. Surviving Rev. A extracted mirror used here: <https://www.scribd.com/document/919510643/design-and-use-considerations>.
2. Micron Technology, Inc., **TN-29-17: _NAND Flash Design and Use Considerations_**, later surviving revision family; Rev. C 11/18 copy: <https://borecraft.com/PDF/Datasheets%2C%20WP%2C%20Specs/tn2917.pdf>. Used only for continuity/provenance, not to backdate later wording.
3. Micron Technology, Inc., **FAQs**, current official support page, sections on `READ DISTURB`, ECC/read errors, and bad blocks: <https://www.micron.com/sales-support/sales/faqs>.
4. Fujitsu Ltd., **“Read disturb alleviated flash memory,”** US20030137873A1 / US6707714B2, priority 22 January 2002, publication 24 July 2003: <https://patents.google.com/patent/US20030137873A1/en>.
5. Douglas Sheldon and Michael Freie, **_Disturb Testing in Flash Memories_**, JPL Publication 08-7, March 2008, NASA/JPL NEPP: <https://nepp.nasa.gov/files/13582/07-100%20Sheldon_JPL%20Distrub%20Testing%20in%20Flash%20Mem.pdf>.
6. Yu Cai et al., **“Read Disturb Errors in MLC NAND Flash Memory: Characterization, Mitigation, and Recovery,”** DSN 2015, DOI `10.1109/DSN.2015.49`: <https://istc-cc.cmu.edu/publications/papers/2015/flash-read-disturb-errors_dsn15.pdf>.

## Completion note

This deepening is complete for the bounded question:

> **By 2006, Micron's manufacturer design guidance already treated read disturb as a recoverable temporary failure rather than automatic permanent block death, and it exposed multiple system-level ways to prevent repeated reads from exhausting recoverability margin.**

The remaining work is implementation/product genealogy and revision-specific provenance, not more repetition of that bounded conclusion.
