# Micron DDR5 On-Die ECC and Error Check Scrub: Read Correction, Array Repair, and Error Transparency

## Status

**`grounded`** — bounded to Micron's public DDR5 product/technical material from the commercial DDR5 platform period, with Linux 6.15 EDAC scrub documentation used as a later host-control and terminology boundary and a 2021 peer-reviewed DDR5-ECS discussion used as an independent technical qualification.

Grounding record: [`../evidence/45-micron-ddr5-2021-2026-odecc-ecs-grounding.md`](../evidence/45-micron-ddr5-2021-2026-odecc-ecs-grounding.md).

## Scope

This case asks a narrow question left open by Cases 33, 40, and 43:

> What changes when a commercial DDR5 device contains both **on-die error correction** and an **error-check-and-scrub path that writes corrected state back into the array**, while ordinary DRAM refresh remains a separate maintenance mechanism?

The bounded mechanism is:

```text
stored DDR5 data + on-die ECC code
        |
        +-- ordinary READ
        |      -> internal ECC evaluation
        |      -> correct a single-bit error for the returned data
        |
        +-- ECS
               -> internally read array state
               -> detect/correct a single-bit error
               -> write corrected state back
               -> accumulate/report correction evidence
```

Micron's public DDR5 material also lists `Same Bank Refresh` as a separate DDR5 reliability/availability feature. That separation is methodologically useful: a DRAM can perform ordinary refresh to keep charge from decaying past the retention deadline and also perform ECC-based scrubbing to stop already-manifested correctable errors from accumulating.

This case is **not**:

- a complete audit of JEDEC JESD79-5 normative text or revision chronology;
- a claim that Micron invented ECC, memory scrubbing, or DDR5 ECS;
- a claim that on-die ECC replaces server, DIMM, controller, link, or software-level RAS;
- a claim that ECS is another name for DRAM refresh;
- a claim that ECS is AVATAR-style retention-aware refresh reclassification;
- a claim that every DDR5 product exposes identical ECS controls to an operating system;
- a field-reliability study of all Micron DDR5 devices.

The contribution is a product-level **maintenance composition**: read-path correction, stored-array repair, ordinary refresh, correction telemetry, and later host-visible scrub policy are related but distinct retention relations.

## Relation to earlier cases

### Case 33 — Same Bank Refresh

Case 33 studies **where refresh blocks service**: DDR5 `Same Bank Refresh` / `REFsb` changes the target and interference geometry of refresh while the underlying DRAM retention obligation continues.

Case 45 adds a different operation:

```text
refresh target / interference geometry
    !=
ECC-based integrity scrub and corrective writeback
```

Micron's own DDR5 material lists `ODECC`, `ECS`, and `Same Bank Refresh` separately. The separation is not merely project taxonomy imported after the fact.

### Cases 40 and 43 — RAIDR / AVATAR

RAIDR and AVATAR are research architectures for changing **future refresh policy** according to profiled or observed row-retention behavior.

DDR5 ECS, in the bounded evidence here, instead does this:

```text
find a correctable error
    -> correct it
    -> write corrected data back
    -> expose correction evidence
```

Nothing in the inspected Micron or Linux material establishes that ECS changes a row's future refresh class. Therefore:

> **scrub-derived error evidence ≠ retention-aware refresh reclassification**.

AVATAR remains a feedback policy case; DDR5 ECS is an integrity-maintenance case inside a commercial DRAM generation.

## Historical vocabulary and record

Micron's public DDR5 material uses the following terms directly:

- `On-die error correction code (ODECC)`;
- `Error check and scrub (ECS)`;
- `Same bank refresh`;
- `128b+8b SEC` in the product comparison table;
- `manual` and `automatic` ECS;
- a recommended `24-hour` period for completing ECS;
- error counts reported after a scrub.

A January 2023 Micron article describing DDR5 on 4th-generation Intel Xeon platforms presents ODECC, ECS, and same-bank refresh as three distinct DDR5 reliability/availability capabilities. It explains that for a DDR5 write, an ECC code is generated and stored with the data; on read, the DRAM evaluates the combined data and can correct a single-bit error. It then describes ECS as an additional function that internally corrects data, can operate manually or automatically, and can report the number of corrected errors after scrubbing.

Micron's DDR5 product page independently lists `On-die ECC` as `128b+8b SEC, error check and scrub`, while listing `REFRESH commands` separately as all-bank and same-bank refresh capability.

The Linux 6.15 EDAC scrub documentation supplies a later composition boundary. It describes DDR5 ECS, via the CXL control model, as a JEDEC DDR5 feature in which the DRAM internally reads data, corrects single-bit errors, writes corrected data back to the DRAM array, and exposes error-count information. Current Linux scrub control can in turn make some ECS policy attributes visible to host userspace through a standardized RAS control surface.

These sources are not silently merged into one timeless specification. Micron 2023 grounds a commercial manufacturer description; Linux 6.15 grounds a later system-software control model; the peer-reviewed 2021 literature provides an independent mechanism discussion. Exact JESD79-5 mode-register language remains outside the claims of this case because the normative standard text was not directly audited here.

## Mechanism

### 1. On-die ECC can repair the value returned by a read

Micron describes DDR5 on-die ECC as storing an ECC code alongside each protected data unit and evaluating data plus code during a read. A correctable single-bit error can be corrected before the result is passed toward the host.

At the retention level, this means a raw stored embodiment can contain a correctable error while the logical value returned by an ordinary read is still correct.

Therefore:

> **raw stored error ≠ immediate logical read failure**.

This is analogous to other ECC-protected storage only at the level of the relation. It does not make NAND ECC, RAID parity, DRAM ODECC, and filesystem checksums historically or mechanically identical.

### 2. Returning corrected data is not the same as repairing the stored embodiment

An ordinary ECC-protected read answers the immediate service question: can the requested logical value be recovered correctly now?

ECS adds a separate maintenance action. The Linux documentation describes the scrub path as internally reading, correcting a single-bit error, and **writing corrected data bits back to the DRAM array**. The 2021 scholarly account describes the same read/check/correct/writeback cycle.

This gives the case's central distinction:

> **read-path correction ≠ stored-array repair**.

The first can make a current access succeed. The second changes the retained array state so the already-observed error is not simply left in place to combine with another fault later.

A system can therefore preserve logical continuity in two steps that are often hidden under one word, `ECC`:

```text
recover current value
        !=
renew the stored codeword/state for future accesses
```

### 3. ECS and refresh preserve different failure margins

DDR5 remains DRAM. Its ordinary refresh obligation exists because cell charge must be periodically restored before leakage destroys the represented state. Cases 03, 21, 33, 34, and 35 already ground that family of mechanisms and its scheduling/geometry variants.

ECS acts on another failure relation: errors that are present in the ECC-protected array and still fall within the single-bit correction envelope.

Micron's 2023 material places ECS on a recommended full-scrub timescale of up to 24 hours, while ordinary DRAM refresh operates on the much shorter retention-deadline regime established in the earlier DRAM cases.

Therefore:

> **ECS scrub ≠ DRAM refresh**

and:

> **refresh deadline ≠ scrub coverage interval**.

Both may involve internal reads/restoration/writeback at some circuit level, but their trigger predicates, safety margins, timescales, and purpose are not interchangeable.

### 4. Correct payload can coexist with evidence of degradation

Micron says DDR5 can report the number of errors corrected after the scrub. The device can therefore produce a correct retained value **and** retain/report evidence that correction work was necessary.

This separates two observables:

```text
payload returned correctly
        !=
no internal correction was required
```

and therefore:

> **payload availability ≠ error observability**.

On-die correction can hide a correctable physical defect from the ordinary data path while ECS telemetry exposes aggregated evidence that such defects occurred.

This is an important counterexample to treating a successful read as proof that the underlying retained embodiment is healthy.

### 5. Correction telemetry is second-order retention state

An ECS correction count is not application payload. It is state **about the condition and maintenance history of the payload-bearing medium**.

That makes it another form of second-order retention infrastructure, comparable only functionally to:

- Case 38's PLI-health/test state;
- Case 40's retention-profile metadata;
- Case 43's row-refresh classification;
- Case 18's scrub/integrity evidence.

The mechanisms and authorities are different, but the shared relation is useful:

> a system may have to retain evidence about the work required to keep first-order state trustworthy.

In DDR5 ECS, correction telemetry can inform later RAS decisions without itself being the user value being preserved.

### 6. Automatic device maintenance does not remove external policy

Micron describes ECS as supporting both manual and automatic operation. That already prevents a simple equation:

```text
automatic ECS
    =
all scrub-policy authority permanently disappears inside the DRAM
```

The later Linux 6.15 control model makes this boundary even clearer. For CXL DDR5 ECS, host software can expose or alter selected ECS controls such as error-count mode, reporting thresholds, and counter reset, and the platform/memory controller may decide when ECS should be initiated in response to observed error rates.

Therefore:

> **automatic maintenance ≠ elimination of external policy authority**.

This later Linux evidence must not be projected backward into every 2023 DDR5 platform. It demonstrates that a standardized device-internal maintenance mechanism can later become part of a host-visible RAS policy stack.

### 7. On-die ECC is not end-to-end ECC

Micron explicitly presents ODECC as a feature that **complements** server RAS and reduces some burden on the integrated memory controller. Its DDR5 product page separately lists read/write CRC and other RAS-related mechanisms.

Therefore:

> **on-die ECC ≠ end-to-end memory-system integrity**.

Correcting an error internal to the DRAM array does not, by itself, prove protection of every transfer path, controller state, DIMM component, address/command path, software-visible page, or system failure mode.

This case deliberately refuses the common shortcut `DDR5 has ECC, therefore ordinary ECC memory is unnecessary`.

## Maintenance and labor

The bounded sources expose several layers of maintenance work:

- the DRAM continuously remains subject to ordinary refresh scheduling;
- on ordinary reads, ODECC can perform internal correction before returning data;
- ECS can scan/check/correct/write back stored array state;
- automatic ECS can hide command-by-command maintenance from ordinary software;
- manual ECS preserves an explicit control path;
- later platform/software layers can expose scrub configuration and error-count policy to administrators or RAS daemons.

This gives a labor boundary familiar from earlier cases:

> **automation moves maintenance labor; it does not make maintenance disappear**.

Some work is absorbed into die logic and autonomous schedules, while configuration, monitoring, thresholds, fault escalation, repair policy, and platform validation can move outward to firmware, the memory controller, kernel, userspace, and operators.

## Failure and forgetting boundaries

This case adds failure modes that are distinct from simple charge leakage:

- **correctable stored error** — raw array state deviates while ODECC can still reconstruct the intended value;
- **error accumulation** — leaving one corrected-on-read error physically unrepaired can consume correction margin if additional faults arise;
- **scrub-coverage delay** — maintenance has not yet visited a vulnerable location;
- **correction-envelope exhaustion** — an error pattern exceeds the single-error-correction relation described by Micron's bounded public material;
- **telemetry invisibility** — ordinary successful reads need not reveal that internal correction was required;
- **policy mismatch** — a device/platform can support automatic or controlled ECS while actual scheduling/threshold policy is configured poorly;
- **scope confusion** — treating on-die ECC as if it covered all system-level failure paths can itself produce an invalid reliability argument.

The retention question is therefore no longer only `did the bit survive?` but also:

```text
Can the raw state be corrected?
Was the current read corrected?
Was the stored state repaired?
Has the array been covered by scrub?
Was correction evidence exposed?
Does the remaining error margin still satisfy the system's reliability target?
```

## Prior art and anti-anachronism

This case makes **no invention-priority claim** for ECC or memory scrubbing.

ECC and scrubbing long predate DDR5. The project's own Case 18 already uses 2004 disk-scrubbing prior art to block a false ZFS-invention narrative, and memory-specific ECC/scrub traditions are older still. The 2021 scholarly source also treats DDR5 ECS as one design point inside an established reliability field, not as the origin of error correction itself.

The bounded historical claim is narrower:

> Micron's commercial DDR5 documentation presents on-die ECC, Error Check and Scrub, and Same Bank Refresh as distinct DDR5 device capabilities, creating a product-level composition of read correction, corrective writeback, error telemetry, and ordinary refresh.

`stored-array repair`, `second-order retention state`, and `maintenance composition` are project engineering terms. They are not substituted for Micron's or JEDEC's historical vocabulary.

## Functional analogy and philosophical limit

A useful functional analogy compares ECS to preventive maintenance that repairs a defect while it is still within a recoverable margin rather than waiting for the next defect to make the state unrecoverable.

The analogy stops there. A DRAM die does not thereby `remember that it was sick` in a human sense, nor does an error counter become an archive merely because it records correction events.

The technically grounded conceptual pressure is narrower:

> The same logical state can remain continuously available while its physical embodiment passes through hidden error, correction, and repair states.

And:

> A system can preserve a value while separately preserving evidence that preserving the value required intervention.

That is useful for philosophy of technical retention because it makes **successful availability** and **evidence of the labor that produced availability** analytically separable.

## Cross-case result

The DRAM maintenance decomposition now includes at least these independent axes:

```text
charge-retention deadline
    -> refresh obligation

refresh authority / schedule
    -> external AUTO REFRESH vs SELF REFRESH / internal timing

refresh target geometry
    -> all-bank / same-bank service interference

environment
    -> temperature-conditioned cadence

row-retention profile
    -> selective refresh policy (RAIDR)

runtime correctable failures
    -> refresh-class feedback (AVATAR)

on-die ECC
    -> correct current read

DDR5 ECS
    -> inspect + correct + write back stored state
    -> expose correction evidence
```

These operations can coexist in one memory subsystem without collapsing into one generic concept of `refresh` or `ECC`.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Micron's commercial DDR5 material lists ODECC, ECS, and Same Bank Refresh as distinct DDR5 capabilities | H/P | Micron 2023 manufacturer material |
| Micron describes DDR5 ODECC with 128 protected data bits plus an 8-bit code and single-bit correction on read | H/P | Micron manufacturer article/product page |
| Micron describes ECS as manual or automatic within a recommended 24-hour period and able to report corrected-error counts | H/P | Micron 2023 manufacturer article |
| Linux 6.15 documents DDR5 ECS as internal read, single-bit correction, and corrected-data writeback | H/P | Linux kernel EDAC documentation; later system-software boundary |
| Current Linux ECS control can expose selected count/threshold/reset policy through a host RAS control surface | H/P | Linux kernel documentation; not projected backward to all DDR5 platforms |
| Returning a corrected value and repairing the stored array are separate retention operations | E | reconstruction from ODECC read path versus ECS writeback path |
| ECS and ordinary DRAM refresh are distinct maintenance mechanisms | E/A | Micron lists separate features; earlier grounded DRAM cases establish refresh obligation |
| Successful payload delivery can coexist with hidden internal correction and separately visible correction evidence | E | reconstruction from ODECC transparency + ECS reporting |
| ECS correction telemetry is second-order retention infrastructure | E/A | project comparison, not historical vendor vocabulary |
| DDR5 ECS updates a row's future refresh class in the manner of AVATAR | X | not established in the bounded sources |
| On-die ECC is equivalent to end-to-end server memory protection | X | contradicted by Micron's own `complements RAS` framing and separate mechanisms |
| Micron or DDR5 invented ECC or memory scrubbing | X | no such priority claim; older ECC/scrubbing traditions exist |
| This case establishes complete normative JESD79-5 semantics or compliance of every DDR5 product | X | direct normative standard audit is outside the bounded evidence set |

## Sources

### Manufacturer-primary / commercial product evidence

- Micron Technology, **“Redefining performance With DDR5 and 4th Gen Intel Xeon scalable processors,”** 2023, especially the `Improved reliability` section: <https://www.micron.com/about/blog/company/partners/redefining-performance-with-ddr5-and-4th-gen-intel-xeon-scalable>.
- Micron Technology, **DDR5 DRAM** product page, DDR4/DDR5 feature comparison table: <https://www.micron.com/products/memory/dram-components/ddr5-sdram>.

### Later implementation / control-surface evidence

- Linux Kernel documentation, **“Scrub Control,”** written for Linux 6.15, especially `Error Check Scrub (ECS)`: <https://docs.kernel.org/6.15/edac/scrub.html>.
- Current Linux Kernel documentation, **“Scrub Control”**: <https://docs.kernel.org/edac/scrub.html>.

### Independent scholarly qualification

- Duy-Thanh Nguyen, Nhut-Minh Ho, Weng-Fai Wong, et al., **“OBET: On-the-Fly Byte-Level Error Tracking for Correcting and Detecting Faults in Unreliable DRAM Systems,”** *Sensors* 21(24), 8271, 2021, section 2.5 `DDR5 ECC Transparency and Scrubbing`, DOI `10.3390/s21248271`: <https://pmc.ncbi.nlm.nih.gov/articles/PMC8708231/>.

## Related repository check

`tmzncty/computing-archaeology` was searched for `DDR5`, `ECS`, and on-die-ECC/scrub combinations before this slice. No dedicated DDR5 ECS case was found. Broader ECC history, semiconductor scaling, and DDR-family technical chronology still belong primarily there; this case retains only the product-level retention comparison that changes the distinction between read correction, array repair, refresh, and error evidence.
