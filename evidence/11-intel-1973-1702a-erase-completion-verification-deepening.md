# Case 11 deepening — Intel 1702A erase completion, verification, and programming-regime compatibility

## Status

**`bounded deepening complete`**

This note deepens [`../cases/11-intel-frohman-floating-gate-eprom-erasure.md`](../cases/11-intel-frohman-floating-gate-eprom-erasure.md) at the product-operation layer.

The existing Case 11 grounding establishes the mechanism-level partition:

```text
hold
    != program
    != read
    != erase
```

from the 1970–1971 Intel/Frohman patent record. The unresolved archival question was narrower:

> When the floating-gate mechanism became an actual Intel 1702/1702A development product, what counted operationally as an erase procedure, and what evidence counted as erase completion?

The answer matters because a physical erase intervention and a verified postcondition are not the same thing.

This note also records a second, adjacent boundary from the same period manual:

> A 1702A could be pin-for-pin compatible with the 1702 while requiring a different programming duty cycle, severe enough that using the 1702A programming control on a 1702 could permanently damage the older part.

That is useful retention evidence because stable package/interface compatibility does not imply stable program/maintenance semantics.

---

## Source set and date control

### P1 — Intel, _MCS-4 User's Manual_, period product/development manual

Primary manufacturer text, mirrored as an HTML/OCR transcript:

- <https://manualzilla.com/doc/7026262/intel-mcs-4-user-s-manual>

The same scan is archived under the descriptive filename `MCS-4_UsersManual_Feb73.pdf` at several historical-computing mirrors, including:

- <https://www.bitsavers.org/components/intel/MCS4/MCS-4_UsersManual_Feb73.pdf>
- <https://deramp.com/downloads/mfe_archive/011-Other%20Computers%20and%20Boards/Intel/MCS-4/MCS-4_UsersManual_Feb73.pdf>

An independent historical-computing reference from the University of Stuttgart's computer-museum community identifies the copy as **February 1973, Revision 4**:

- <https://www.mail-archive.com/search?f=1&l=cctalk%40classiccmp.org&o=newest&q=date%3A20160319>

The current web transcript does not expose the original cover date in searchable text, so this note keeps the source date as a **catalogue / scan-identification fact** rather than pretending that the date was re-read from a visible cover in this run.

### Source-quality boundary

The engineering claims below come from Intel's own period manual text, not from a modern EPROM summary.

The HTML host is a later mirror/transcription. Accordingly:

```text
period manufacturer content
    !=
original hosting provenance
```

The mirror is sufficient for directly checking the operational wording quoted/paraphrased here, but it does not establish a new first-publication date beyond the bounded 1973 manual identification.

---

## Historical record

### H/P — erase is specified as a physical UV exposure procedure

The Intel manual's `1701, 1702 ERASING PROCEDURE` section states that the devices may be erased by **high-intensity short-wave ultraviolet light** at approximately **2537 Å**.

The manual gives a recommended integrated dose of approximately **6 W·s/cm²** and names example short-wave UV lamps. It says that, for the example lamps, a 1702A can be erased in approximately **10–20 minutes** when placed about **one inch** from the lamp tubes.

Relevant transcript neighborhood:

- lines 6122–6128 in the currently indexed HTML transcript.

The numerical values are therefore treated as **period Intel operating guidance for this product family**, not as universal EPROM constants.

### H/P — elapsed exposure is not the only completion criterion in the manual

Immediately before the erase-procedure section, the manual describes the PROM listing facility as a way to verify whether a 1701/1702 is completely erased.

Its operational rule is simple: when the PROM is completely erased, the listing presents the erased-state symbol in **every location**.

Relevant transcript neighborhood:

- lines 6118–6121.

This is a stronger retention/control fact than merely saying that the package has a quartz window or that UV can discharge a floating gate.

The manual provides a host-visible postcondition:

```text
apply erase exposure
    -> read/list addressable contents
    -> require every location to present erased state
```

Thus, in the period product workflow:

```text
recommended UV dose/time elapsed
    !=
verified whole-device erase completion
```

### H/P — programming likewise includes verification

Elsewhere in the same Intel manual, the MCS-4 programming workflow instructs the operator to insert an **erased 1702A** into the programmer, start the programming operation, and states that the PROM is then **automatically programmed and checked for correct content**.

Relevant transcript neighborhood:

- lines 8172–8176.

This establishes a product workflow in which both sides of the state transition are observable:

```text
erase workflow:
    physical UV intervention
    -> read/list verification of erased postcondition

program workflow:
    electrical programming operation
    -> automatic content check
```

The historical source does not use the repository terms `postcondition`, `admissibility witness`, or `state-transition evidence`; those are engineering reconstruction terms below.

### H/P — a detected bad programming result leads back through erase and reprogram

The programming/listing discussion also states that when a ROM is found faulty in this workflow, the ROM should be **erased and reprogrammed**.

This does not mean every semiconductor defect is recoverable by erasure. In context it documents the intended development cycle for a programmable/erasable part:

```text
program
    -> inspect / compare
    -> if content is wrong, erase
    -> program again
```

That is operational reuse of the same physical device, not evidence of infinite endurance.

### H/P — 1702A is described as pin-for-pin replacement but not programming-regime equivalent

The manual calls the 1702A a **pin-for-pin replacement for the 1702** and states that the MP7-03 programming system can program the 1702A substantially faster than the 1702.

It then gives an explicit warning: the newer A0543 programming-control PROM is for the 1702A and must not be used to program the 1702 because the programming duty cycle is too high and **may permanently damage the 1702**.

Relevant transcript neighborhood:

- lines 6134–6140.

This gives a contemporaneous product-level compatibility boundary:

```text
same external pinout / replacement role
    !=
same admissible programming waveform or duty cycle
```

and, more strongly:

```text
interface-compatible operation
    can still become destructive
    when the wrong generation-specific programming regime is applied
```

---

## Engineering reconstruction

The following are project-level interpretations of the historical record, not period Intel terminology.

### E/R — an erase action and evidence of erase completion are distinct technical objects

The UV dose/time guidance describes an **intervention**.

The listing check describes a **post-intervention observation**.

Those two things should not be collapsed:

```text
physical intervention performed
    !=
required logical postcondition observed
```

For this Intel workflow, erase completion becomes an observable relation over the entire address space:

```text
for every listed location:
    observed state == erased state
```

This is not a modern cryptographic sanitize guarantee. It is simply the bounded completion semantics exposed by the period development toolchain.

### E/R — erase completion is device-wide even though program/read selection is addressable

The Frohman array patent grounds fine-grained X/Y selection for programming and reading. The product manual grounds a UV erase procedure whose completion is checked by reading all locations.

Together they support the bounded decomposition:

```text
addressable program/read operations
    !=
device-level erase intervention
    !=
whole-address-space erase verification
```

The distinction is about control geometry and completion evidence. It does not imply that every microscopic cell receives exactly identical photon dose, nor does it supply a bit-by-bit analog threshold distribution.

### E/R — a nominal maintenance interval is not itself proof of completion

The manual gives example erase times and an integrated-dose recommendation, but also exposes a way to verify the resulting state.

Therefore the safe project-level reading is:

```text
10–20 minute example exposure
    = procedure guidance under named source/distance conditions

not

10–20 minutes elapsed
    = unconditional proof that every bit is erased
```

This distinction anticipates a recurring repository pattern: **time budget and completion evidence are different fields**.

The source itself does not discuss that pattern abstractly; it merely gives both the procedure and the verification mechanism.

### E/R — package compatibility does not preserve hidden control contracts

The 1702A/1702 warning demonstrates that stable pins do not preserve all acceptable electrical stress conditions.

A system can retain the same socket/interface shape while changing the permitted programming regime:

```text
physical interface identity
    !=
programming-control semantic identity
```

This is a useful control-plane retention lesson, but it is not evidence that Intel described the change philosophically as a problem of technical identity.

---

## Functional comparisons

These comparisons are analytical only. They do **not** assert genealogy.

### F/A — later storage maintenance also separates action from verified result

Across the repository, many maintenance procedures have a similar abstract shape:

```text
perform maintenance action
    -> obtain observation / status
    -> decide whether required state has actually been reached
```

The 1702A workflow is an early, small-scale semiconductor example of that shape.

It should not be called a predecessor of SSD sanitize verification, RAID consistency checking, or media scrub merely because the abstraction is similar.

### F/A — Case 04 Flash remapping differs from this erase model

Case 04 studies logical identity surviving remapping and erase-unit reclamation inside a managed Flash system.

Case 11's 1702A workflow has no FTL and no remapping layer in the evidence used here. Its comparison is instead:

```text
selected logical access
    versus
externally applied device erase
    versus
read-back confirmation of erased state
```

The similarity is limited to the fact that **forgetting has its own geometry and completion boundary**.

---

## Philosophical interpretation boundary

The product workflow makes one conceptual point unusually concrete:

> An object may be designed to forget, yet the act intended to make it forget is not identical to evidence that forgetting has completed.

That is a project-level interpretation.

Intel's manual is not evidence that Intel engineers advanced a philosophy of forgetting, memory, verification, or identity.

Likewise, the warning about programming a 1702 with the 1702A duty cycle can support a modern observation that interface continuity can hide changed operational constraints; it does not show that Intel framed the engineering warning as a theory of identity across generations.

---

## Claim ledger

| Claim | Label | Evidence |
| --- | --- | --- |
| Intel's period MCS-4 manual gives short-wave UV erasure guidance for the 1701/1702 family and explicitly describes example 1702A erase conditions | H/P | Intel _MCS-4 User's Manual_, erase-procedure section |
| The manual gives approximately 2537 Å, 6 W·s/cm², and example 10–20 minute / one-inch conditions | H/P | same |
| The manual provides a listing-based check for whether the PROM is completely erased | H/P | same, lines 6118–6121 in current transcript |
| The programming workflow automatically checks programmed content | H/P | same, lines 8172–8176 |
| The 1702A is described as a pin-for-pin replacement for 1702 | H/P | same, lines 6134–6137 |
| The 1702A-specific programming control may permanently damage a 1702 because its duty cycle is too high | H/P | same, lines 6138–6140 |
| Recommended exposure time by itself is unconditional proof of completed erasure | X | contradicted by the presence of an explicit complete-erase verification workflow |
| The period manual proves a modern secure-sanitize guarantee | X | unsupported category leap |
| `pin-for-pin replacement` means identical programming stress/timing is safe | X | directly contradicted by Intel's warning |
| A failed programming check proves a defective transistor | X | unsupported; workflow-level failure does not identify microscopic cause |
| Erase/reprogram may be repeated infinitely without wear | X | not established by this source |
| Every 1702/1702A revision uses exactly the same UV and programming limits | X | not established |

---

## What this adds to Case 11

The original grounding established **physical eraseability**.

This deepening adds **operational erase completion**:

```text
mechanism level:
    UV can remove trapped charge

product-operation level:
    prescribed UV exposure
        -> read/list the device
        -> require erased state at every location
```

It also adds a product-generation control boundary:

```text
1702A is pin-for-pin replacement for 1702
    but
1702A programming duty cycle can damage 1702
```

So Case 11 can now distinguish four layers that previously risked being collapsed:

```text
retention mechanism
    !=
erase mechanism
    !=
erase procedure
    !=
erase-completion evidence
```

and can separately distinguish:

```text
package/interface compatibility
    !=
programming-regime compatibility
```

---

## Explicit non-claims

This note does **not** claim:

1. that the 1973 manual is the first Intel document to publish these erase parameters;
2. that 6 W·s/cm² is a universal EPROM erase dose;
3. that 10–20 minutes is a universal erase time;
4. that elapsed exposure guarantees every cell has erased;
5. that the listing operation measures analog floating-gate charge directly;
6. that reading all erased values is equivalent to a modern secure-erasure certification;
7. that the manual establishes data-remanence resistance against forensic recovery;
8. that the 1702A and 1702 share identical internal cell geometry;
9. that pin compatibility implies timing/stress compatibility;
10. that the wrong programming duty cycle always destroys a 1702 — Intel says it **may** permanently damage it;
11. that every failed verify cycle identifies a permanent hardware defect;
12. that erase/reprogram endurance is unlimited;
13. that later EEPROM/Flash erase semantics should be projected back onto the 1702A;
14. that a modern maintenance/verification abstraction proves historical lineage to later scrub/sanitize systems.

---

## Related-repository check

Searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `EPROM` and `1702A` still return no dedicated technical-history module to reuse.

Accordingly, this file remains bounded to the **retention-specific operational contract**. A broader history of Intel's 1701/1702/1702A revisions, programmer hardware, package manufacturing, process changes, and later EPROM product families belongs in `computing-archaeology` if that repository later takes up the topic.

---

## Remaining bounded debt

The most useful next archival step for Case 11 is now narrower than before:

1. directly inspect an Intel 1702A **datasheet/data-book page** with product-specific erase and retention specifications;
2. distinguish datasheet qualification limits from development-system operating guidance;
3. if available, find a period source specifying retention duration, temperature assumptions, and erase/program endurance for a named 1702A revision;
4. keep any later EEPROM case separate, because electrical erasure changes the control geometry rather than merely refining this UV workflow.

None of these remaining items blocks the current `grounded` maturity of Case 11.

---

## Sources

1. Intel, _MCS-4 User's Manual_, period manufacturer manual, HTML/OCR mirror: <https://manualzilla.com/doc/7026262/intel-mcs-4-user-s-manual>.
2. Historical scan mirror, `MCS-4_UsersManual_Feb73.pdf`: <https://www.bitsavers.org/components/intel/MCS4/MCS-4_UsersManual_Feb73.pdf>.
3. Alternate scan mirror, same descriptive filename: <https://deramp.com/downloads/mfe_archive/011-Other%20Computers%20and%20Boards/Intel/MCS-4/MCS-4_UsersManual_Feb73.pdf>.
4. Klemens Krause / University of Stuttgart computer-museum community, 19 March 2016 mailing-list note identifying the held manual as `Feb. 1973, Rev. 4`: <https://www.mail-archive.com/search?f=1&l=cctalk%40classiccmp.org&o=newest&q=date%3A20160319>.

## Retrieval note

The relevant Intel-manual wording was directly inspected in the searchable HTML transcript. The PDF mirrors were discoverable but returned access errors to the current web reader, so this note does **not** claim page-image inspection of those PDF copies. That limitation affects cover/date provenance precision, not the directly checked erase/verify/programming text preserved by the HTML transcript.