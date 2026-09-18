# Case 77 deepening — Data General MV/4000 named-product refresh-coupled memory sniffing (1982–1984)

## Status

**`bounded deepening complete`**

Canonical case: [`../cases/77-data-general-dram-sniff-refresh-ecc-scrub.md`](../cases/77-data-general-dram-sniff-refresh-ecc-scrub.md)

This pass closes one previously open part of Case 77:

> Can a named Data General product be tied, by period product documentation rather than patent inference alone, to the same functional pattern of dynamic-RAM refresh plus periodic ECC `sniffing` and corrective stored-state repair?

Answer: **yes, for the ECLIPSE MV/4000 at the product-documentation level.**

A 1982 Data General MV/4000 system-characteristics manual states that the memory controller checks for memory errors while performing the refresh operations required by the dynamic RAM modules, explicitly calls this operation `sniffing`, and says that sniffing verifies all memory locations and corrects single-bit errors in memory even when the location is not being used by a program. A 1984 SUGI proceedings panel speaking from a Data General product perspective independently lists `error correcting memory and memory sniffing` among MV/4000 features and says every memory location is tested every four seconds.

This is substantially stronger than the earlier Case-77 patent-only record. It establishes a **named-product refresh-coupled sniffing witness**. It does **not** prove that the MV/4000 implemented every circuit, counter width, timing constant, pipeline detail, or claim of US4380812A unchanged.

---

## Research boundary

### Included

- Data General's 1982 product-level MV/4000 system-characteristics documentation;
- the manual's explicit coupling of dynamic-RAM refresh with error checking called `sniffing`;
- the manual's statement that sniffing covers all memory locations and corrects a single-bit error in stored memory;
- a 1984 SUGI proceedings product-description witness that names MV/4000 memory sniffing and gives a four-second whole-memory test interval;
- comparison with Data General US4380812A, filed in 1980, which discloses a refresh-coupled sniff mechanism and an illustrative two-second same-word interval;
- the distinction between **patent disclosure**, **named-product feature documentation**, and **exact implementation identity**;
- bounded comparisons with later DDR5 ECS and storage scrub without claiming genealogy.

### Excluded

- claiming that US4380812A is a literal MV/4000 schematic;
- claiming that every MV/4000 memory configuration had exactly the same sniff cadence;
- reconstructing undocumented MV/4000 memory-controller microcode or gate-level logic;
- identifying the exact memory-module option or board revision used by every installed MV/4000;
- claiming that the four-second SUGI statement is a formal hardware timing guarantee for every configuration;
- claiming that MV/4000 was the first shipping system with memory scrub/sniff;
- broad ECLIPSE MV product history;
- a full history of SEC-DED, alpha-particle soft errors, Chipkill, patrol scrub, or DDR5 ECS.

---

## Source custody

### H/P — Data General MV/4000 system-characteristics manual, 1982

**Artifact:** Data General Corporation, document part number **014-000736-00**, archived as `MV4000_SystemChar_Dec82.pdf`.

**Date evidence:** the archived copy carries Data General copyright **1982**; the archive filename identifies the copy as December 1982.

**Archive:**

<https://bitsavers.trailing-edge.com/pdf/dg/mv4000/014-000736-00_MV4000_SystemChar_Dec82.pdf>

This is the strongest source in this pass because it is manufacturer-primary, product-specific documentation.

### H/P — SUGI '84 proceedings panel, 1984

**Artifact:** Jon Fleig, Jerry Harber, Steve Sashihara, `Panel Discussion of SAS Users under the AOS/VS Operating System`, SUGI '84 proceedings, Hollywood Beach, Florida, 18–21 March 1984.

Proceedings index:

<https://support.sas.com/resources/papers/proceedings-archive/SUGI84/proceedings.html>

PDF:

<https://support.sas.com/resources/papers/proceedings-archive/SUGI84/Sugi-84-136%20Harber%20Fleig%20Sashihara.pdf>

The paper speaks from a Data General product perspective (`we at Data General`, `our MVs`) and discusses the MV/4000, MV/8000, and MV/10000 as current product-family members. For Case 77 it is used as a contemporary corroborating product-description source, not as a circuit manual.

### H/P — Data General US4380812A, 1980 filing / 1983 publication

**Artifact:** Michael L. Ziegler II, Michael B. Druke, John R. Van Roekel, Ward Baxter II / Data General Corporation, `Refresh and error detection and correction technique for a data processing system`, US4380812A.

**Filed:** 25 April 1980.

**Published / granted:** 19 April 1983.

<https://patents.google.com/patent/US4380812A/en>

This remains the detailed primary mechanism source for the refresh-coupled sniff design. In this pass it is used as a mechanism comparator against the product manual, not as a substitute for product evidence.

---

## Historical record

### 1. The 1982 MV/4000 manual explicitly ties ERCC to refresh access

The MV/4000 product documentation describes a memory system with error detection and correction on ordinary double-word reads and on memory accessed during a refresh operation. It says the memory controller generates seven ERCC check bits for each double word sent to a memory module and checks those bits when the word is read.

The manual therefore gives a named-product relationship rather than an abstract design alone:

```text
ECLIPSE MV/4000
    dynamic-RAM memory
    + ERCC-protected double words
    + memory-controller refresh activity
```

This directly closes the older Case-77 gap in which the 1980 patent had not yet been tied to a named product.

### 2. The manual names refresh-time checking `sniffing`

The decisive product statement is that, when the MV/4000 memory controller performs the refresh operations required by the dynamic RAM modules, the controller also checks for memory errors, and that **this operation is called sniffing**.

That supports a bounded product-level relation:

```text
DRAM refresh operation
    -> recurring controller opportunity
    -> error check during that opportunity
    -> `sniffing`
```

The wording is especially important because it rules out a weaker interpretation in which `sniffing` might merely mean an independent background diagnostic that happens to exist on the same machine.

For the documented MV/4000 memory system, refresh and sniff are explicitly composed in the controller path.

### 3. Sniffing is whole-memory preventive integrity maintenance, not only demand-path correction

The same manual says sniffing verifies **all memory locations** and corrects a single-bit error **in memory**, even if the location is not being used by a program.

It explains the preventive purpose: avoid unused memory accumulating single-bit errors and avoid intermittent single-bit errors growing into uncorrectable multiple-bit errors.

This supports the Case-77 distinction:

```text
foreground read succeeds after ECC correction
    !=
stored codeword has been proactively repaired
```

and adds named-product evidence that the second operation was deliberately performed outside demand access.

### 4. The system control program can observe ERCC/sniff errors

The MV/4000 documentation says the system control program can log ordinary ERCC errors and can also log sniffing errors.

That does not make logging part of the physical correction mechanism, but it adds a distinct observability relation:

```text
physical/codeword maintenance event
    -> machine-visible error evidence
    -> possible system-level logging
```

The historical source does not, in the inspected passage, establish persistence duration, log format, or operator workflow for those records.

### 5. The 1984 SUGI record independently names MV/4000 memory sniffing

The SUGI '84 proceedings list product features of the **MV/4000** and include:

- error-correcting memory;
- memory sniffing;
- testing every memory location every **four seconds**.

This is valuable because it is later than the 1982 manual and appears in a product-family discussion rather than in a patent. It corroborates that `memory sniffing` was not only an internal patent term; it was exposed in contemporary product descriptions of the MV/4000.

The safe claim is:

> By 1982–1984, Data General publicly documented the named ECLIPSE MV/4000 as using refresh-coupled memory error checking called `sniffing`, and a 1984 product presentation described a whole-memory sniff cycle on the order of four seconds.

### 6. Product cadence and patent embodiment cadence are not identical facts

US4380812A gives an illustrative interval of about **two seconds** between sniffing the same word in its disclosed configuration. The 1984 MV/4000 product description says every memory location is tested every **four seconds**.

This is not evidence of contradiction.

The patent itself says the sniff interval is a function of refresh period and the number of words in memory and explicitly notes that substantially longer intervals can be suitable for larger memories. The patent's two-second value belongs to its illustrative organization; the SUGI four-second value belongs to a product description.

Therefore:

```text
same functional mechanism family
    !=
same literal cadence constant
```

and:

> **timing parameter continuity is not required for mechanism-family continuity.**

### 7. Named-product documentation still does not prove exact patent-circuit identity

The MV/4000 manual now establishes the key functional composition that had been missing:

- dynamic RAM requires refresh;
- refresh-time memory access is also checked by ERCC;
- this is called sniffing;
- all memory locations are eventually covered;
- correctable single-bit errors can be corrected in memory;
- errors can be logged.

US4380812A supplies much more circuit detail: refresh interval timer, refresh address counters, row/column/module sequencing, request preemption/retry, corrective writeback, and a pipelined re-read before delayed writeback.

The product manual passage does **not** independently enumerate every one of those patent internals. Thus the correct historical relation is:

```text
1980-filed patent
    detailed refresh-coupled sniff mechanism

1982 MV/4000 manual
    named-product refresh-coupled sniff behavior

1984 MV/4000 product presentation
    named-product sniff feature + four-second coverage claim
```

not:

```text
US4380812A figures == proven literal MV/4000 implementation
```

---

## Engineering reconstruction

The following terms are repository-level reconstructions, not quotations from the historical actors.

### E1. The slice closes `design disclosed` versus `product behavior documented`

Before this pass, Case 77 had strong patent evidence but retained a deployment ambiguity.

Now at least three evidence layers can be distinguished:

```text
design-level mechanism
    US4380812A

named-product functional implementation
    1982 MV/4000 system characteristics

contemporary product-facing description
    1984 SUGI panel
```

The second layer is the important new one. It moves the case beyond `a manufacturer once patented this idea` without pretending to have gate-level field-engineering proof.

### E2. Product identity, behavior, and embodiment must remain separate predicates

This pass supports:

```text
named product has refresh-coupled sniffing
```

It does not support:

```text
named product is byte-for-byte / gate-for-gate the patent embodiment
```

The distinction matters because the same functional retention relation can survive implementation changes in module capacity, timing, pipeline organization, or controller revision.

### E3. Scan cadence is retained-policy state, not a universal property of `sniffing`

The patent's illustrative two-second interval and the product-facing four-second interval show why the project should not define sniffing by one magic number.

A more robust model is:

```text
refresh opportunity rate
    + memory population / address-space size
    + scan progression policy
        -> revisit interval for a protected word
```

The exact product formula remains partly undocumented in this pass, so this is a bounded reconstruction rather than a recovered MV/4000 timing equation.

### E4. Proactive repair protects remaining ECC margin

The MV/4000 manual's rationale is directly compatible with the Case-77 model: a correctable single-bit error should not be allowed to sit indefinitely in unused memory until a second error converts the word into an uncorrectable condition.

The retention-specific chain is:

```text
latent correctable error
    -> periodic verification
    -> correction in stored memory
    -> restored single-error margin
```

This is maintenance of **future recoverability**, not merely successful current decoding.

### E5. Logging is evidence retention, not payload retention

The product manual's logging statement adds another state class:

- payload/codeword state;
- ECC redundancy state;
- refresh/sniff progress state;
- event/diagnostic evidence available to system software.

Those are not interchangeable. Losing a diagnostic log does not imply payload loss; successful physical correction does not imply the historical error event remains observable forever.

---

## Functional comparison — not genealogy

### A — Case 45, DDR5 ODECC / ECS

Case 45 gives a much later device-internal Error Check and Scrub regime. Case 77's MV/4000 witness places refresh-coupled error checking in the system memory controller and explicitly exposes `sniffing` in product documentation.

Shared functional relation:

```text
correctable error now
    -> correction
    -> stored-state renewal
    -> renewed margin against another error
```

Historical vocabulary, integration locus, interfaces, and mechanism lineage remain different.

### A — Case 101, disk Background Medium Scan / Patrol Read lineage

Both can proactively inspect material that foreground workload has not recently demanded. But disk BMS/Patrol Read deals with medium readability, defect handling, and sometimes redundancy-assisted repair. MV/4000 sniffing deals with ECC-protected dynamic memory and is explicitly coupled to DRAM refresh opportunities.

Shared relation only:

> **lack of foreground access must not be allowed to turn a latent recoverable defect into a later unrecoverable one.**

No direct historical genealogy is claimed.

### A — Case 18, ZFS scrub

ZFS scrub is an end-to-end checksummed storage traversal with different authority and fault-domain semantics. The commonality is proactive verification/repair before demand exposes accumulated damage, not the mechanism.

---

## Philosophical limit

The new product evidence supports a restrained project-level observation:

> technical continuity can require recurrent operations on state that appears idle, because `not currently requested` is not the same as `safe to leave indefinitely unexamined`.

That is an engineering consequence of bounded correction margin. It is not evidence that the computer `remembers`, `cares`, or `anticipates` in a psychological sense.

Likewise, the term `sniffing` is historical vocabulary for a machine operation, not a license to anthropomorphize it.

---

## Explicit non-claims

1. The MV/4000 manual does **not** prove Data General invented memory scrubbing.
2. The MV/4000 manual does **not** prove US4380812A was implemented literally and unchanged.
3. The 1984 SUGI paper does **not** substitute for a field-engineering schematic.
4. The SUGI four-second statement is **not** generalized to every MV/4000 configuration or revision.
5. The patent's two-second interval is **not** generalized to the MV/4000 product.
6. A two-second patent example and four-second product statement are **not** treated as a contradiction.
7. `sniffing` is **not** defined by one fixed interval.
8. Refresh-time checking does **not** mean charge refresh and ECC scrub have the same success predicate.
9. Correcting a single-bit error does **not** prove the underlying hardware is permanently healthy.
10. Whole-memory scan coverage does **not** prove every location is checked simultaneously.
11. System-level logging does **not** prove logs survive reboot or power failure.
12. Error logging does **not** imply the corrected payload remains historically reconstructible from the log.
13. The product sources do **not** establish the exact ECC polynomial or code construction beyond the documented ERCC organization.
14. The sources do **not** establish the exact reset semantics of the sniff scan cursor.
15. The sources do **not** establish whether an interrupted sweep resumes or restarts.
16. The sources do **not** establish `PAGEINH` behavior for the MV/4000 product; that remains a separate 1985 patent-family witness.
17. MV/4000 sniffing is **not** equated with DDR5 ECS, ZFS scrub, SCSI BMS, or RAID patrol read.
18. A named-product manual is **not** the same evidentiary category as independent field reliability measurement.
19. A contemporary product presentation is **not** used to prove invention priority.
20. The wider ECLIPSE MV product genealogy is **not** reconstructed in this evidence file.

---

## Claim ledger

| Claim | Type | Evidence | Confidence |
| --- | --- | --- | --- |
| Data General had a named MV/4000 product document with ERCC-protected dynamic memory | H/P | 1982 MV/4000 system characteristics | high |
| the MV/4000 memory controller checks for memory errors while performing DRAM refresh | H/P | 1982 MV/4000 system characteristics | high |
| the manual explicitly calls this refresh-time error checking `sniffing` | H/P | 1982 MV/4000 system characteristics | high |
| MV/4000 sniffing verifies all memory locations and can correct single-bit errors in stored memory | H/P | 1982 MV/4000 system characteristics | high |
| the stated rationale includes preventing unused memory from accumulating correctable errors into uncorrectable multiple-bit errors | H/P | 1982 MV/4000 system characteristics | high |
| the system control program can log ERCC/sniffing errors | H/P | 1982 MV/4000 system characteristics | high |
| a 1984 Data General-oriented SUGI product discussion lists MV/4000 error-correcting memory and memory sniffing | H/P | SUGI '84 proceedings | high |
| the 1984 product description says every memory location is tested every four seconds | H/P | SUGI '84 proceedings | high, product-description scope |
| US4380812A gives a two-second same-word interval in an illustrative embodiment | H/P | US4380812A | high |
| different two/four-second numbers do not by themselves imply different functional mechanism | E | bounded reconstruction | high |
| the exact US4380812A circuit shipped unchanged in MV/4000 | X | not established | rejected |
| MV/4000 was the first commercial system with memory scrub/sniff | X | not established | rejected |
| sniff cursor persistence across reset/power loss is known | X | not established | rejected |
| MV/4000 sniffing and DDR5 ECS are the same mechanism | X/A | only functional analogy | rejected |

---

## What this pass changes in Case 77

The previous evidence debt asked for a named Data General product/service manual establishing whether the refresh-coupled sniff mechanism actually appeared in a product context.

This pass closes that debt at the **product-functional** level:

```text
1980 patent disclosure
    + 1982 manufacturer product manual
    + 1984 contemporary product description
        -> named MV/4000 refresh-coupled sniffing is now grounded
```

The remaining debt is narrower and more technical:

```text
named-product behavior grounded
    != exact patent embodiment identity grounded
    != reset/power-loss scan-progress semantics grounded
```

---

## Related-repository check

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Data General sniff` and `MV/4000 memory` returned no dedicated packet to reuse.

Accordingly, this file keeps only the retention-specific seam:

> **refresh-coupled controller opportunity → systematic ECC inspection → stored correction → renewed correction margin → separately observable error evidence.**

A broad history of ECLIPSE MV hardware, Eagle/MV/8000 development, MV/4000 memory-board revisions, ERCC implementation genealogy, service diagnostics, and the wider migration of memory scrub authority belongs in `computing-archaeology` rather than being duplicated here.

---

## Remaining evidence debt

1. Recover a period MV/4000 field-engineering or logic manual that exposes the exact sniff counter/state machine and compare it clause-by-clause with US4380812A.
2. Determine whether the sniff scan position survives reset, power interruption, or controller replacement, or simply restarts.
3. Determine whether the four-second whole-memory figure is fixed, capacity-dependent, or configuration/revision dependent in product engineering documents.
4. Find named MV/8000 primary product documentation that independently describes `sniffing`, rather than relying on later retellings or inaccessible trade-press snippets.
5. Identify which memory module/board revisions correspond to the product manual's ERCC/sniff description.
6. Locate period service records or reliability studies that quantify correctable-error rates and sniff-detected errors in deployed MV systems.
7. Keep the separate 1985 `PAGEINH` classification/persistence question open until a named-product service source ties that behavior to deployed hardware.
8. Continue terminology genealogy (`sniff`, `scrub`, `memory scrubbing`, `patrol scrub`) without retroactively renaming Data General's mechanism.

None of these gaps blocks the bounded conclusion that the ECLIPSE MV/4000 is now a named-product witness for refresh-coupled memory sniffing.