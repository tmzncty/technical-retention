# Evidence 127 — 2015–2016 DDR3 scrambling, remanence, and semantic recovery boundary

**Status:** bounded deepening complete

**Parent case:** [`cases/127-dram-power-off-remanence-gradual-decay.md`](../cases/127-dram-power-off-remanence-gradual-decay.md)

**Earlier grounding:** [`evidence/127-dram-1979-2008-remanence-grounding.md`](127-dram-1979-2008-remanence-grounding.md)

**Adjacent cryogenic boundary:** [`evidence/127-1984-1991-cryogenic-dram-refresh-suppression-boundary-deepening.md`](127-1984-1991-cryogenic-dram-refresh-suppression-boundary-deepening.md)

## Bounded question

Case 127 already establishes that DRAM can retain a degraded physical residue after power and refresh stop, and that cooling changes the decay window. This slice asks a narrower question that becomes visible on later DDR3 systems:

> If the physical DRAM residue survives a power boundary, is that sufficient for the original logical memory image to remain directly readable?

The answer, for the Intel DDR3 systems experimentally studied by Bauer, Gruhn, and Freiling in 2016, is **no**. A memory-controller scrambling relation can sit between the logical image and the physical bit pattern stored in DRAM. The physical residue may survive while the interpretation state used to turn that residue back into the logical image changes, disappears, or is replaced by another system's state.

This slice therefore separates four things that are easy to collapse:

1. physical DRAM-cell remanence;
2. the scrambled physical representation resident in DRAM;
3. the controller-side scrambling relation used during the original write;
4. later semantic recovery of the original plaintext image.

The historical record, engineering reconstruction, functional analogy, and philosophical interpretation are kept distinct below.

---

## Result in one sentence

**On the bounded Intel DDR3 systems studied in 2015–2016, surviving DRAM charge was not by itself sufficient to preserve directly readable logical memory: the stored physical image was controller-scrambled, and recovering the historical plaintext after a cold start or module transplant could require reconstructing the relation between the surviving physical image, the original scrambler stream, the acquisition scrambler stream, address/channel interleaving, and bit-decay noise.**

---

# 1. Source custody and evidence classes

## Source A — Bauer, Gruhn, Freiling 2016

**Document:** Johannes Bauer, Michael Gruhn, Felix C. Freiling, “Lest we forget: Cold-boot attacks on scrambled DDR3 memory,” *Digital Investigation* 16 (2016), S65–S74, DFRWS Europe 2016.

**DOI:** `10.1016/j.diin.2016.01.009`

**Official open-access host:** DFRWS.

- landing page: <https://dfrws.org/presentation/lest-we-forget-cold-boot-attacks-on-scrambled-ddr3-memory/>
- paper PDF: <https://dfrws.org/sites/default/files/session-files/2016_EU_paper_lest_we_forget_-_cold-boot_attacks_on_scrambled_ddr3_memory.pdf>

**Evidence class:** `H/P + X`.

- `H/P` for the authors' own experiments, measured platforms, acquisition procedure, observed scrambling behavior, cooling/power-off behavior, and recovery results;
- `X` where this record reconstructs the retention consequence from those measurements.

The paper is especially useful because it does not merely say that DDR3 “has remanence.” It observes the additional interpretation layer created by Intel memory scrambling and experimentally reconstructs enough of that layer to recover images after cold-boot acquisition.

### Inspection note

Claims below are grounded only in text present in the DFRWS-hosted open-access paper or in the authors' official presentation. No claim depends solely on an unlabeled figure or visual impression.

## Source B — Intel/Mozak scrambling patent

**Document:** Christopher P. Mozak / Intel Corp., US Patent `US7945050B2`, “Suppressing power supply noise using data scrambling in double data rate memory systems.”

**Priority / filing:** 28 September 2007.

**Publication:** `US20090086972A1`, 2 April 2009.

**Grant:** `US7945050B2`, 17 May 2011.

**Public text:** <https://patents.google.com/patent/US7945050B2/en>

**Evidence class:** `H/P` for disclosed Intel design embodiments; **not** proof that every later Intel controller implemented every disclosed embodiment exactly.

The patent describes memory-controller transmit and receive paths in which data is XORed with pseudo-random outputs, including LFSR-based embodiments seeded at least partly from address information, in order to reduce data-pattern-dependent power-supply noise.

## Source C — Lindenlauf, Höfken, Schuba 2015

**Document family:** Simon Lindenlauf, Hans-Wilhelm Höfken, Marko Schuba, “Cold Boot Attacks on DDR2 and DDR3 SDRAM,” ARES 2015, pp. 287–292; plus the authors' February 2015 Nullcon presentation “Cold Boot Attack on DDR2 and DDR3 RAM.”

**Official author/publication page:** <https://www.fh-aachen.de/en/people/schuba/forschung/veroeffentlichungen/>

**Official conference presentation host:** <https://nullcon.net/talk/cold-boot-attack-on-ddr2-and-ddr3-ram/>

**DOI:** `10.1109/ARES.2015.28`

**Evidence class:** `H/P` for the authors' 2015 test setup and measured DDR2/DDR3 results exposed in their official presentation; bibliographic/venue metadata for the ARES paper.

This source is used as an adjacent experimental witness, not as a substitute for Bauer et al.'s scrambling analysis.

---

# 2. Historical / technical record

## 2.1 Intel's disclosed scrambling is an interface transform, not a DRAM-cell storage primitive

The 2007-priority Intel patent describes a memory controller coupled to DRAM through a memory interconnect. In the disclosed transmit path, write data is XORed with pseudo-random outputs before being sent to memory. In the receive path, read data is XORed again with matching pseudo-random outputs to recover the original data.

The patent's stated engineering motivation is power-supply-noise suppression: data-dependent current patterns on increasingly fast DDR interfaces can create jitter/noise problems, and scrambling makes the transmitted pattern approximately white / balanced.

The retention-relevant boundary is therefore:

```text
logical data P
    -> controller transform K(address, state, implementation)
    -> physical/bus representation M
    -> DRAM cells
```

The transform belongs to the memory-controller path. It is not evidence that a DRAM capacitor itself contains both `P` and `K`, nor that the DRAM module independently knows the original logical plaintext.

## 2.2 The Intel patent does not prove Bauer et al.'s exact measured implementation

`US7945050B2` discloses embodiments using parallel LFSRs and address-derived seeds. It explicitly permits alternative output widths, polynomials, address portions, and even seed inputs other than the address.

Therefore this evidence record uses the patent for the **historical engineering possibility and stated design motivation**, while using Bauer et al.'s experiments for the **measured behavior of their systems**.

Do not collapse:

```text
patent embodiment
    != exact undocumented shipping implementation
```

## 2.3 Bauer et al. treat the physical RAM image as scrambled state

Bauer et al. write the relation as:

```text
M = P XOR K
```

where:

- `P` is the logical/plain image visible to ordinary software during normal operation;
- `K` is the memory-controller scrambling stream;
- `M` is the representation resident in DRAM.

During ordinary operation the controller transparently applies the transform on writes and the inverse transform on reads. Software can therefore behave as though it were reading and writing `P`, while the physical DRAM contains `M`.

This is a direct counterexample to an overly simple retention model in which “the bits that survive in memory” and “the application's historical logical bits” are always the same representation.

## 2.4 Scrambler configuration has a different lifetime from cell charge

Bauer et al. report that firmware programs the memory controller hub during initialization, including scrambler configuration and seed. In their trials, a reset-button reboot did **not** reset the seed, while a transition from unpowered to powered state is the point at which a reseed can occur.

That observation gives a bounded lifetime distinction:

```text
reset-button reboot
    may preserve controller interpretation state

cold start / different acquisition machine
    may instantiate different interpretation state
```

This is an experiment-specific observation from their tested Intel systems. It is not a universal x86, DDR3, UEFI, or firmware rule.

## 2.5 A transplanted module can preserve physical residue while losing the original controller relation

The paper's transplantation case is retention-relevant because the DRAM module can physically carry the old scrambled pattern into another machine while the acquisition controller uses a different scrambling stream.

If the original machine wrote:

```text
M = P XOR K0
```

and the acquisition system reads the same residue through a different controller stream `K1`, then the captured image is effectively:

```text
I = P XOR K0 XOR K1
```

Thus:

```text
M survives
    != P is directly observable
```

The historical plaintext may remain recoverable, but recovery now depends on reconstructing enough of the old/new transformation relation.

## 2.6 Constant-scrambling systems provide the opposite boundary case

Bauer et al. also observed systems using a constant scrambling configuration. If the same scrambling stream is reused on the same system, XOR application on write and read can cancel, making the system behave for acquisition purposes as though scrambling were absent.

This matters because “DDR3 scrambling exists” does **not** imply that every power cycle destroys the interpretation relation.

The stronger statement is only:

> The semantic readability of surviving physical state can depend on controller configuration whose persistence horizon is independent of the DRAM-cell residue.

## 2.7 Randomized and constant configurations were both observed

Bauer et al. report an MSI H55M-P33 with Intel Core i5-760 using constant scrambling in their tests, while an MSI B75MA-P45 with Intel Core i3-3225 used random scrambling.

They did not find a tested machine with scrambling disabled altogether.

This is an experimental population, not a census of Intel systems.

---

# 3. Experimental recovery evidence

## 3.1 Platforms

Bauer et al.'s measurements were performed predominantly on:

- Intel Core i3-3225 + MSI B75MA-P45.

They also report confirming their results on:

- Intel i5-760 + MSI H55M-P33;
- Intel i5-2520M + Dell 03PH4G;
- Intel i5-2400 + Esprimo P900 E90+.

This named-platform list is valuable because it prevents the result from silently becoming a claim about “DDR3” as an undifferentiated technology.

## 3.2 Controlled data placement and power interruption

The authors placed known grayscale images and recognizable pattern blocks in memory. They cooled the memory module to about `-30 °C`, cut power completely, and restarted after approximately `2–5 s` of power-off latency.

They then acquired the memory image and used the derived descrambling procedure to recover the historical image.

This directly demonstrates, for the tested configuration:

```text
power removed
    -> some physical DRAM state survives
    -> controller interpretation relation changes / must be handled
    -> reconstruction can recover historical logical content
```

## 3.3 Surviving representation was not equivalent to readable plaintext

With cooled memory, the authors report that the captured image still visibly contained the source image's structure but was distorted by a repeating scrambling pattern. After reconstructing and applying the most probable key/stencil, the result was close to the original except for occasional bit errors.

The important retention lesson is not the image itself. It is the layered failure model:

```text
physical decay noise
    + representation transform mismatch
    + channel/address mapping
    = observed acquisition image
```

Recovering a retained object can therefore require correcting both **material degradation** and **lost/changed interpretation relations**.

## 3.4 Known-plaintext requirement is small relative to the whole image

The paper presents a stencil attack requiring `64 bytes` of known plaintext per memory channel, or at most `128 bytes` on a dual-channel system. By exploiting mathematical relations in the differential stream, it reduces this to `25 bytes` per channel / `50 bytes` for dual channel.

This does **not** mean the original scrambler seed is recovered. The authors emphasize that their acquisition path reconstructs differential streams; they do not claim to recover the original key stream itself.

So:

```text
semantic recovery succeeds
    != original controller state is restored bit-for-bit
```

## 3.5 Dual-channel interleaving is another interpretation relation

Each memory channel can have an independent scrambler. The authors therefore had to determine how captured data was interleaved between channels, separate the two channel images, descramble them independently, and interleave them again.

This adds another layer:

```text
retained cells
    != retained logical ordering
```

A physical residue can remain present while its original logical ordering still has to be reconstructed from architecture-specific relations.

---

# 4. Physical decay evidence remains bounded and device-specific

## 4.1 Bauer et al. saw fast decay on their 2013-era DDR3 modules

In their experiments, cooled DDR3 at roughly `-30 °C` produced usable results, but the authors observed about `10 s` before total decay even with cooling. At roughly `+30 °C` they report that they could not acquire a usable image because content had dissipated.

They explicitly contrast this with earlier DDR2 results and with Lindenlauf et al.'s DDR3 measurements.

This is evidence of strong device dependence, not a universal DDR3 retention constant.

## 4.2 Lindenlauf et al. provide an adjacent 2015 DDR3 witness

The authors' official Nullcon presentation reports experiments across:

- DDR2 and DDR3;
- 7 manufacturers;
- 16 individual modules;
- 2 mainboards;
- different temperatures and power-off intervals.

For a selected `10 s` power-off test at `-35 °C` to `-30 °C`, the presentation lists three DDR3 modules with bit-error rates of approximately:

- `0.000703%`;
- `0.001034%`;
- `0.067%`.

It also reports that platform behavior mattered: the ASUS P53E board used in their experiments did not overwrite DDR3 in the same way as many tested PC mainboards, and one DDR3 type could be attacked without cooling but at a very high error rate.

This reinforces two bounded points:

```text
DDR generation
    != sufficient predictor of remanence outcome

module physics
    + temperature
    + time without power
    + motherboard/firmware behavior
    + acquisition path
    -> observed recoverability
```

## 4.3 Bauer et al. explicitly caution against overreading the 2015 long-decay result

Bauer et al. note that Lindenlauf et al. reported very low error rates at `-30 °C` to `-35 °C` and power-off intervals up to `50 s`, but state that it was not apparent to them whether the longest intervals applied to DDR3 or only DDR2.

This record therefore does **not** promote “DDR3 survives 50 seconds at -35 °C” into a general claim.

---

# 5. Engineering reconstruction

This section is an engineering reconstruction from the primary/experimental record, not language used by the historical actors.

## 5.1 Retention has at least two separable horizons here

For the bounded system we can distinguish:

```text
H1: physical-state horizon
    how long enough capacitor state remains recoverable

H2: interpretation-state horizon
    how long the controller/configuration relations needed to read
    that state with its original meaning remain available or reconstructable
```

The two horizons can fail independently.

Examples:

- `H1` fails first: the cells decay; correct scrambler knowledge cannot recreate vanished bit state.
- `H2` fails first: cells still contain a strong scrambled residue, but a new controller seed makes a direct read semantically wrong.
- both partly fail: reconstruction must tolerate bit-decay noise while recovering the transformation relation.

## 5.2 A retained object can require a retained or reconstructed decoder relation

The surviving physical DRAM image in Bauer et al.'s model is not self-describing. It only becomes the historical logical image under the relevant transform.

Therefore:

```text
retained carrier state
    + absent decoder relation
    != directly usable retained object
```

But this does not require the exact original decoder state itself to survive. The 2016 work shows that enough structure can be inferred to reconstruct the logical object without restoring every historical controller register.

So a more precise relation is:

```text
original decoder state lost
    != semantic recovery impossible

provided that
    surviving representation
    + structural constraints
    + known plaintext / redundancy
    -> sufficient reconstruction evidence
```

## 5.3 Representation persistence and semantic persistence are not identical

This case therefore adds a useful axis to `technical-retention`:

```text
physical representation persists
    != original semantic view persists automatically
```

The distinction is stronger than ordinary “metadata is needed.” The transformation can be transparent during service, invisible to software, and still become decisive only after a failure boundary.

## 5.4 Cold-start reseeding is a relation change, not cell erasure

If a new cold start changes `K`, the DRAM residue does not thereby physically disappear. Instead, the default read interpretation changes.

This is an important negative result for reasoning about restart:

```text
new interpretation state
    != old physical state destroyed
```

The system can therefore move from “historical content directly readable” to “historical content still physically present but misinterpreted.”

---

# 6. Functional comparisons

These comparisons are **functional analogies only**. They do not assert historical descent.

## 6.1 Comparison with Case 04 TrueFFS mapping reconstruction

Case 04 separates surviving Flash-resident data/mapping evidence from a volatile RAM mapping table that can be rebuilt after restart.

Case 127's DDR3 scrambling boundary is different but functionally related:

```text
Case 04:
    payload + authoritative mapping evidence
        -> rebuild volatile logical map

Case 127:
    physical scrambled residue + transform/interleaving evidence
        -> reconstruct historical logical image
```

In both cases, **one runtime representation may disappear while a higher-level relation remains recoverable**. The actual mechanisms and histories are unrelated.

## 6.2 Comparison with Case 42 Kafka checkpoint currentness

Kafka demonstrates that a persisted coordinate can remain bitwise present yet lose semantic currentness when its referent geometry changes.

DDR3 scrambling shows another failure of naive “bytes survived, therefore meaning survived” reasoning:

```text
Kafka:
    coordinate survives
    referent geometry changes

DDR3 cold boot:
    physical image survives
    decoder/configuration relation changes
```

Both require checking the relation between a retained representation and the context that gives it meaning.

## 6.3 Comparison with archival format interpretation

A distant functional analogy is an old file whose bytes survive while the software/encoding needed to interpret it disappears.

The analogy is useful only at the abstract level:

```text
carrier persistence
    != interpretability persistence
```

It must not be used to claim that DDR3 scrambling is historically or technically the same as file-format preservation.

---

# 7. Philosophical interpretation

This section is interpretation, not a historical actor claim.

## 7.1 “The state” is not always one layer

A naive account says that RAM either remembers or forgets. The bounded DDR3 evidence suggests a layered account instead:

```text
material residue
    -> encoded representation
    -> controller interpretation
    -> logical object
```

Failure can occur at any arrow, not only in the material carrier.

## 7.2 Forgetting can be relational rather than purely material

A system can lose immediate access to historical meaning while substantial physical traces remain. Conversely, lost interpretive state can sometimes be reconstructed from redundancy and structure.

That makes “retention” partly a property of relations among surviving states, not merely a property of one storage medium.

## 7.3 Recovery need not reproduce the historical machine

Bauer et al.'s reconstruction does not require restoring the exact original machine-controller state. They infer enough of the transform to recover the plaintext image.

A retained object's continuity can therefore be supported by **reconstructable equivalence**, not only by literal persistence of every original mechanism.

---

# 8. Failure-window matrix

| Boundary | What can survive? | What can change/disappear? | Consequence |
| --- | --- | --- | --- |
| normal powered operation | cells + active controller transform | ordinary transient controller activity | software sees plaintext transparently |
| reset-button reboot on Bauer et al.'s tested systems | DRAM state; observed scrambler seed continuity | some software/firmware state | direct acquisition may remain comparatively simple |
| cold power-off, cooled, same platform | degraded scrambled DRAM residue | some controller initialization state; possible seed/config change | physical content may survive but require transform recovery |
| module transplant | degraded scrambled DRAM residue | original controller/seed context | acquisition controller may apply a different stream; image becomes differential/misinterpreted |
| warm/no-cooling power-off on their tested 2013 modules | little or no usable physical residue | interpretation state also may change | semantic reconstruction cannot recover information that physically decayed |
| dual-channel acquisition | per-module residue | original channel association may be obscured in acquired image | deinterleaving becomes part of semantic recovery |

The matrix is descriptive for the bounded experimental evidence. It is not a platform-independent specification.

---

# 9. Explicit non-claims

This evidence file does **not** claim any of the following:

1. all DDR3 systems use Intel-style scrambling;
2. all Intel DDR3 controllers use exactly the LFSR or polynomial disclosed in `US7945050B2`;
3. the patent proves the exact shipping implementation measured by Bauer et al.;
4. scrambling is encryption in the cryptographic-security sense;
5. memory scrambling was designed as a cold-boot defense;
6. the scrambler seed is always random;
7. the scrambler seed always changes at cold start;
8. the scrambler seed always survives reset-button reboot on every platform;
9. DDR3 universally retains data for 10 s at `-30 °C`;
10. DDR3 universally loses all data within 10 s at `-30 °C`;
11. DDR2 always retains data longer than DDR3;
12. all 2015 Lindenlauf measurements apply equally to DDR2 and DDR3;
13. a 50 s cooled result is established here as a DDR3 universal bound;
14. bit-decay errors are uniformly random;
15. a visually recognizable image proves exact bitwise recovery;
16. Bauer et al. recover the original scrambler seed or exact historical controller registers;
17. differential-stream reconstruction is identical to restoring the historical machine state;
18. module transplantation is required for every cold-boot acquisition;
19. BIOS/UEFI behavior is identical across boards;
20. every reboot preserves RAM contents;
21. every cold start overwrites RAM contents;
22. a surviving physical bit pattern is self-describing;
23. successful descrambling repairs physically decayed bits without redundancy or inference;
24. Case 127's DDR3 relation is historically descended from Flash mapping, Kafka checkpointing, or archival-format interpretation;
25. the unavailable direct Link & May 1979 facsimile debt has been closed by this slice.

---

# 10. Claim ledger

| Claim | Evidence class | Source | Strength / boundary |
| --- | --- | --- | --- |
| Intel disclosed DDR memory-controller scrambling to reduce data-pattern-dependent supply noise | `H/P` | `US7945050B2` | strong historical design disclosure |
| disclosed embodiments XOR write/read data with pseudo-random outputs and may seed LFSRs from address information | `H/P` | `US7945050B2` | strong for disclosed embodiments, not universal implementation proof |
| Bauer et al. model physical DRAM content as `M = P XOR K` on the studied Intel DDR3 systems | `H/P` | Bauer et al. 2016 | strong bounded model + experiment |
| firmware programs scrambler configuration/seed during initialization on their studied systems | `H/P` | Bauer et al. 2016 | strong bounded observation/reconstruction |
| in their trials a reset-button reboot did not reset the seed | `H/P` | Bauer et al. 2016 | strong but platform-bounded |
| cold start / transplant can put surviving physical data under a different scrambler stream | `H/P + X` | Bauer et al. 2016 | strong bounded recovery model |
| cooled modules around `-30 °C`, power-off around `2–5 s`, yielded recoverable images in their experiments | `H/P` | Bauer et al. 2016 experimental results | strong named experiment |
| operating-temperature tests around `+30 °C` on their modules yielded no usable image | `H/P` | Bauer et al. 2016 | strong sample-specific result |
| the paper reports roughly 10 s before total decay even with cooling on its tested DDR3 modules | `H/P` | Bauer et al. 2016 | bounded sample result only |
| the logical image can be recovered without restoring the exact original controller state | `H/P + X` | Bauer et al. 2016 stencil/mathematical recovery | strong bounded engineering inference |
| 2015 authors tested DDR2/DDR3 across multiple modules/manufacturers/mainboards | `H/P` | official Nullcon 2015 presentation | strong adjacent witness |
| selected 2015 cooled DDR3 10 s tests showed very low but nonzero error rates on three modules | `H/P` | official Nullcon 2015 presentation | strong exact presentation result |
| physical-state retention and semantic interpretability have separable lifetimes | `X` | synthesis of A–C | engineering reconstruction, not actor terminology |
| a retained representation can require a retained or reconstructed interpretation relation | `X/P` | synthesis of Bauer experiments | strong functional conclusion |

---

# 11. What this changes in Case 127

The earlier Case 127 grounding can safely retain its core statement:

```text
power removed
    != immediate physical erasure
```

This slice adds a second inequality:

```text
physical state survives
    != historical logical image remains directly readable
```

And a constructive recovery relation:

```text
surviving scrambled residue
    + bounded decay
    + reconstructable transform relation
    + channel/address structure
    -> historical logical image can remain recoverable
```

This makes Case 127 more useful to the repository's central question. Retention is not merely the survival of matter or bits; it can depend on whether the relations that turn a surviving representation into an operative object are themselves retained, reproduced, or reconstructed.

---

# 12. Remaining evidence debt

This bounded slice does not close every Case 127 question.

The most useful next debts are:

1. **Direct Link & May 1979 facsimile inspection remains open.** Search in this run confirmed the bibliographic trail but did not produce a directly inspectable copy; the one-week liquid-nitrogen statement must therefore remain secondary in the earlier evidence record.
2. A named DDR4/LPDDR-generation remanence replication with open primary measurements would test how far the 2015–2016 DDR3 conclusions extend.
3. A firmware/processor-generation study could separate scrambler-seed lifetime from other memory-controller training state more precisely.
4. Raw-bus acquisition work could test recovery when the acquisition system's descrambler is bypassed entirely.
5. A source-level reconstruction of the authors' released `ddr3descramble` code would sharpen which parts of the semantic relation were inferred versus assumed.

---

# 13. Related-repository boundary

Fresh searches of `tmzncty/computing-archaeology` for the exact Link/May title, `Link May`, and `cryogenic DRAM` did not find a dedicated packet to reuse.

This repository should therefore retain only the bounded seam:

> **DRAM physical remanence → controller-scrambled physical representation → loss/change of interpretation state across reset/power/transplant boundaries → reconstruction of semantic readability.**

A broad history of DDR memory scrambling, Intel memory-controller generations, DDR3/DDR4 platform evolution, cold-boot attack history, and DRAM-forensics tooling belongs in `computing-archaeology` if developed later.

---

# 14. Readiness assessment

This is a **bounded deepening**, not a maturity upgrade request. Case 127 already has a grounded physical-remanence base. The new material adds:

- a primary Intel design disclosure for controller-side scrambling;
- a peer-reviewed open-access 2016 experiment on named Intel/DDR3 platforms;
- a 2015 adjacent DDR3 remanence experiment from the authors' official conference material;
- explicit separation of material survival, representation survival, interpretation-state survival, and semantic reconstruction;
- negative claims that prevent patent-to-product, sample-to-generation, and physical-to-semantic overreach.

The canonical case should remain `grounded` unless the repository's authoritative maturity review independently changes it.