# Case 02 Deepening — DEC PDP-8 Memory Power-Cycle Diagnostics and Retention Validation (1966–1969)

**Status:** `bounded deepening complete`

## Purpose

This record deepens [`../cases/02-magnetic-core-destructive-read.md`](../cases/02-magnetic-core-destructive-read.md) around one narrow question left after the existing power-transition evidence:

> if a magnetic-core array is described as nonvolatile, how did a period computer vendor turn that material expectation into a machine-level maintenance test, and what exactly did a failed test mean?

The existing Case-02 power-transition record already establishes from IBM 1401 and DEC PDP-7 manuals that:

```text
quiescent magnetic retention
    !=
power-transition immunity
    !=
whole-machine restart continuity
```

Case 86 separately establishes the PDP-8 `KR01` / later PDP-8-family power-fail save-and-restart path for preserving selected volatile execution state in core before power disappears.

This slice does **not** duplicate either result. It adds a different form of evidence: DEC's maintenance ecosystem included a dedicated **Memory Power On/Off Test** whose stated purpose was to detect bits that dropped out or were picked up after a simulated power failure. Later surviving diagnostic media and modern restoration runs show that this was an operationally executable retention test, not merely a descriptive claim in a handbook.

The bounded result is:

```text
material nonvolatility claim
    !=
transition-retention qualification
    !=
a particular diagnostic pass

and

power-cycle survival
    can be made an observed maintenance property
    rather than assumed from substrate class alone
```

Claim layers remain separate throughout: **Historical record**, **Engineering reconstruction**, **Functional analogy**, and **Philosophical interpretation**.

---

## Sources inspected

### 1. DEC PDP-8 Program Abstracts — MAINDEC 829

Digital Equipment Corporation, surviving archival scan:

- `DEC-08-BA1A-D_PDP-8_Program_Abstracts_19661011.pdf`
- Bitsavers: <https://bitsavers.org/pdf/dec/pdp8/software/DEC-08-BA1A-D_PDP-8_Program_Abstracts_19661011.pdf>

The DEC abstract identifies:

- `Maindec 829`;
- title: **PDP-8 Memory Power On/Off Test**;
- purpose: **tests memory for bit dropout and pickup after a simulated power failure**.

This is the strongest primary source in this slice because it directly states DEC's intended diagnostic object and failure vocabulary.

### 2. Surviving MAINDEC-08-D1AC artifacts and catalog genealogy

Several archival/software indexes preserve the later replacement diagnostic:

- Bitsavers PDP-8 diagnostic directory includes `MAINDEC-08-D1AC-D.pdf`: <https://bitsavers.trailing-edge.com/pdf/dec/pdp8/diag/MAINDEC-08-D1AC-D.pdf>
- David Gesswein's PDP-8 software index records `Memory Power On/Off Test (replaces maindec-829)` and identifies revision-C document/media part numbers `AC-5822C / MAINDEC-08-D1AC-D` and `AK-5824C / MAINDEC-08-D1AC-PB`: <https://so-much-stuff.com/pdp8/software/dec.php>
- Jay Jaeger's archived paper-tape inventory records `MAINDEC-08-D1AC-PB`, **PDP-8 MEMORY POWER ON/OFF TEST**, dated **16 September 1968**: <https://www.bitsavers.org/bits/DEC/pdp12/papertapeimages/From_JayJaeger/PaperTape-List-PDP8-PDP12.pdf>
- ACONIT's PDP-8 software repository preserves a paper-tape image described as `Memory power on-off test (1969-09-16 MAINDEC-08-D1AC-pb)`: <https://pop.aconit.org/Programs/>

These records establish survival and revision genealogy of the executable diagnostic family. They do not by themselves settle the exact first-release date of D1AC or every revision difference between MAINDEC 829, D1AA, and D1AC.

### 3. Rhode Island Computer Museum PDP-8/L restoration log

Modern restoration record:

- Rhode Island Computer Museum, PDP-8/L restoration blog: <https://www.ricomputermuseum.org/collections-gallery/equipment/pdp-8-l/pdp-8-l_blog>

The restoration team reports locating revision-C `MAINDEC-08-D1AC-D.pdf`, following its operating sequence, and seeing the program halt at the documented error halt (`0055`) rather than continue looping. They then inspected recorded memory locations to determine where the error occurred and which bits were implicated.

This is **not period evidence** for how every PDP-8 behaved in service. It is a modern hardware-restoration experiment showing that the surviving diagnostic can still be used as an executable observation procedure on an actual restored PDP-8/L.

### 4. PDP-8 Straight-8 restoration log

Modern restoration record:

- David Gesswein, PDP-8 Straight-8 functional restoration: <https://www.pdp8online.com/straight8/functional_restore.shtml>
- diagnostic index / operation notes: <https://www.pdp8online.com/straight8/straight8-maindecs.shtml>

The restoration log reports that `maindec-08-d1ac` intermittently failed because memory locations were being cleared on power-off. The companion diagnostic page summarizes the surviving operating sequence as loading/start preparation, reaching a halt, starting the retention loop, powering off/on, and starting again.

Again, this is modern restoration evidence, not a DEC factory acceptance record and not a controlled statistical lifetime test.

### 5. Source-handling limitation

The archived `MAINDEC-08-D1AC-D.pdf` is directly locatable as a seven-page DEC diagnostic document, but page-image rendering through the research interface failed with an archival cache error during this pass. Therefore this record does **not** claim page-level direct-facsimile inspection of the D1AC document body.

Claims about the **purpose** of the diagnostic come from DEC's directly indexed 1966 Program Abstracts entry. Claims about the **revision-C operating sequence and observed failures** are explicitly attributed to modern restoration records that say they used the surviving D1AC document/program. The surviving artifact/catalog references are used to establish custody and genealogy, not to invent unseen manual text.

---

## Historical record — DEC treated power-cycle retention as a testable memory property

The 1966 DEC Program Abstracts entry is unusually concise but conceptually strong. It does not merely call magnetic core `nonvolatile` or say that memory should survive power removal. It names a dedicated maintenance program whose purpose is to test for two transition-associated error classes:

- **bit dropout**;
- **bit pickup**;

after a **simulated power failure**.

This directly grounds a period-vendor distinction between:

```text
expected retention property
    !=
observed post-transition bit state
```

A core location can be intended to retain state across a power transition and still be worth testing for both directions of corruption.

The vocabulary `dropout` and `pickup` is important. The test is not described only as looking for erasure to zero. A power transition can be treated as capable of producing either loss of previously set bits or appearance of bits that should not be set.

This does **not** prove that every electrical failure mode on every PDP-8 reduces cleanly to those two categories. It establishes DEC's diagnostic classification for this test.

---

## Historical record — the diagnostic survived as an executable maintenance artifact

The later MAINDEC catalog trail identifies `MAINDEC-08-D1A` as **Memory Power On/Off Test** and explicitly says it **replaces maindec-829**. Revision-C document and paper-tape identifiers survive, and archived tape inventories preserve a `MAINDEC-08-D1AC-PB` artifact dated 16 September 1968.

The cautious genealogy is therefore:

```text
by 1966:
MAINDEC 829
PDP-8 Memory Power On/Off Test
    ↓
by the late 1960s:
MAINDEC-08-D1A family
Memory Power On/Off Test
(replacement relation preserved in later catalog indexes)
```

This record does **not** infer that the code was byte-for-byte continuous, that 829 and D1AC used identical test patterns, or that 16 September 1968 is the first date on which D1A existed.

---

## Historical record — diagnostic qualification is narrower than automatic restart

Case 86 shows a different PDP-8 power-failure relation: the optional KR01 path detects low power, provides a bounded interval for software to save selected volatile processor state into core, then later reconstructs that state and resumes through a restart routine.

The memory power-cycle diagnostic asks a prior and narrower question:

> did the core-resident bits that are supposed to persist remain correct through the transition being exercised?

Therefore:

```text
memory survives tested power cycle
    !=
volatile CPU state saved
    !=
restart routine succeeds
    !=
peripheral state remains coherent
```

The MAINDEC test and KR01 are related only because both cross a power boundary. They validate different retained relations.

---

## Modern restoration experiment — a period retention test can still fail on real hardware

The Rhode Island Computer Museum restoration log reports using the revision-C D1AC diagnostic on its PDP-8/L. The team followed the documented setup, expected the program to loop, and instead saw it reach the error halt at `0055`. They then used memory locations retained by the diagnostic to investigate where the memory error occurred and which bits were implicated.

David Gesswein's Straight-8 restoration independently reports a more directly retention-shaped symptom: `maindec-08-d1ac` could intermittently fail with **memory locations getting cleared on power off**.

These observations are valuable because they block a common retrospective shortcut:

```text
ferrite core is nonvolatile
    therefore
any powered-off PDP-8 must preserve every bit correctly
```

Real machine-level success still depends on the memory stack plus its drivers, inhibit/write paths, supply sequencing, noise margins, and transition behavior.

The modern logs do **not** tell us that the original core material itself had lost remanence. A post-cycle wrong bit can result from a transition disturbance, a write/inhibit fault, a driver problem, marginal timing, or another machine-level fault. The diagnostic observes the retained logical result; it does not by itself localize the physical cause.

---

## Engineering reconstruction — qualification adds an observation protocol to retention

The sources support a simple decomposition:

```text
pre-transition logical pattern
    ↓
controlled / simulated power-failure event
    ↓
unpowered or transition interval
    ↓
power restoration
    ↓
post-transition readback / comparison
    ↓
pass or dropout/pickup evidence
```

This is an **engineering reconstruction** of what makes the diagnostic retention-specific. It is not claimed as DEC's formal conceptual model.

The important result is that retention is not operationally established merely by knowing the substrate category. A maintenance organization can require:

1. a known precondition;
2. a defined disturbance or transition;
3. later observation;
4. a comparison rule;
5. failure evidence that remains inspectable long enough to diagnose the machine.

So:

```text
retention capability
    !=
retention assertion
    !=
retention test coverage
    !=
retention test pass
```

---

## Engineering reconstruction — transition retention and shelf retention are different experiments

The MAINDEC abstract specifies a **simulated power failure**. That is a transition experiment, not a long-duration shelf-retention experiment.

The diagnostic can expose corruption associated with:

- power removal;
- power restoration;
- transition sequencing;
- support-circuit behavior around the transition;
- the core array's ability to preserve the written distinction while unpowered for the exercised interval.

It does not, from the evidence inspected here, establish:

- retention after days, months, or years without power;
- a universal ferrite magnetic-decay constant;
- environmental qualification across temperature/humidity ranges;
- arbitrary brownout waveforms;
- immunity to every partial-rail or repeated-flapping sequence.

Thus:

```text
passes a power-cycle diagnostic
    !=
quantified long-term retention lifetime
```

---

## Engineering reconstruction — a passing test does not identify which layer supplied the success

If the observed memory contents are correct after the tested power cycle, several relations have jointly succeeded:

```text
pre-cycle pattern was written correctly
+
transition did not spuriously rewrite selected cores
+
remanent state survived the unpowered interval
+
power-up did not corrupt the array
+
post-cycle read/restore path classified the bits correctly
=
observed diagnostic pass
```

The pass is a system result. It should not be re-described as a direct measurement of ferrite remanence alone.

Conversely, failure is underdetermined until further diagnosis:

```text
wrong post-cycle bit
    !=
proved remanence decay
```

This is precisely why the restoration logs' hardware troubleshooting matters as a bounded experimental complement: the same visible retention failure can lead technicians toward drivers, memory-control circuitry, or marginal modules rather than toward a simplistic claim that `the core forgot`.

---

## Engineering reconstruction — diagnostic evidence has a coverage boundary

A program can only validate the states, addresses, patterns, transition conditions, and repetitions it actually exercises.

Therefore:

```text
no failure observed in one diagnostic run
    !=
all addresses / patterns / transitions universally safe
```

This sounds obvious, but it matters for cross-case comparison. Later memories expose retention qualification through bake tests, refresh-margin sweeps, ECC telemetry, patrol reads, media scrubs, power-cut tests, and qualification standards. The shared relation is **bounded observation under a specified stress**, not identical physics or test methodology.

---

## Functional analogy — later power-cut and persistence testing

A narrow functional analogy can be made to later storage and persistent-state tests:

```text
known state
    -> disturb power / interrupt service
    -> recover
    -> inspect retained state
```

The analogy is useful because all such tests distinguish **intended persistence semantics** from **empirically observed recovery state**.

The analogy stops there. PDP-8 core power-cycle diagnostics are not historically:

- filesystem crash-consistency tests;
- SSD capacitor-backed power-loss-protection certification;
- DRAM retention-time profiling;
- NVDIMM persistence-domain validation;
- distributed fault injection.

No genealogy is inferred from the shared experimental form.

---

## Cross-case comparison

### Case 02 — core destructive read / remanence

The base case explains why a selected ferrite core can retain a magnetic distinction without continuous power and why ordinary read may require restoration.

This deepening adds:

```text
quiescent element-level nonvolatility
    !=
verified survival across a machine power transition
```

### Case 86 — PDP-8 automatic restart

Case 86 preserves selected **volatile execution context** by transferring it into core before power disappears.

This deepening tests whether the **core-resident state itself** remains correct through the exercised transition.

Therefore:

```text
save volatile state into core
    presupposes
core transition-retention is usable

but
core transition-retention pass
    !=
complete restart continuity
```

### Case 70 — operating margins and disturbance

Case 70 treats half-select disturbance and machine operating margins. A failed power-cycle test is another reminder that retained state is embedded in a driver/sense/power apparatus, but it is not evidence that half-select disturbance caused the power-cycle failure.

---

## Philosophical interpretation — endurance becomes answerable to a test

The exact technical fact is modest: DEC provided a diagnostic whose purpose was to compare memory state across a simulated power failure and classify bit dropout/pickup.

A bounded interpretation follows:

> technical endurance is not only a property attributed to a material; in maintenance practice it can become a claim that must survive a repeatable interruption-and-return procedure.

This clarifies one project theme: a future operation may treat a past state as still available only after a chain of material survival, controlled transition, readback, and validation succeeds.

The interpretation stops there. It does not imply that DEC engineers held a philosophical theory of persistence, nor that every retention relation requires the same style of explicit diagnostic.

---

## Failure boundaries exposed by this slice

The diagnostic perspective separates at least these failures:

1. **dropout** — an expected set state is absent after the exercised transition;
2. **pickup** — an unexpected set state appears;
3. **test/setup failure** — the diagnostic was not correctly loaded, initialized, or resumed;
4. **write-path fault** — the pre-cycle expected pattern was not established correctly;
5. **transition disturbance** — power sequencing/support circuitry alters stored state;
6. **read/classification fault** — the state survives but post-cycle sensing reports the wrong logical value;
7. **intermittent margin failure** — repeated executions need not fail identically;
8. **coverage failure** — a passing run leaves unexercised patterns/conditions outside the claim.

The period abstract directly names only dropout/pickup after simulated power failure. The remaining categories are engineering reconstruction used to prevent causal overclaiming.

---

## Explicit non-claims

This deepening does **not** claim:

1. that DEC invented power-cycle memory testing;
2. that MAINDEC 829 was the first diagnostic of magnetic-core retention;
3. that MAINDEC-08-D1AC is byte-for-byte identical to MAINDEC 829;
4. that 16 September 1968 is the exact first-release date of D1AC;
5. that a D1AC failure proves ferrite remanence physically decayed;
6. that a D1AC pass measures long-term shelf retention;
7. that the diagnostic covers arbitrary brownouts, partial rails, repeated power flapping, or every transition waveform;
8. that all PDP-8 models use identical memory power sequencing;
9. that modern restoration failures reproduce a historically common field failure rate;
10. that the Rhode Island Computer Museum or PDP-8 Online restoration observations are DEC-period production evidence;
11. that the diagnostic validates volatile processor registers, I/O state, or peripherals across power loss;
12. that the diagnostic is equivalent to KR01/KP8 automatic restart testing;
13. that the archived D1AC PDF body was page-level facsimile-inspected in this research pass;
14. that one successful diagnostic run proves every bit/pattern/environment safe;
15. that modern crash-consistency, persistence-domain, or fault-injection terminology was historical DEC vocabulary.

---

## Resulting bounded distinctions

```text
magnetic remanence
    !=
machine-level power-cycle qualification

vendor says memory is nonvolatile
    !=
diagnostic observes correct post-cycle contents

simulated power-failure test
    !=
long-duration shelf-retention test

bit dropout / pickup observed
    !=
physical root cause localized

one passing run
    !=
universal transition immunity

core transition-retention
    !=
volatile execution-state retention
    !=
automatic restart continuity

period diagnostic artifact survives
    !=
every revision semantic fully reconstructed
```

---

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| DEC listed `Maindec 829` as `PDP-8 Memory Power On/Off Test` | `H/P` | strong primary, DEC Program Abstracts |
| DEC said the program tests memory for bit dropout and pickup after a simulated power failure | `H/P` | strong primary, explicit abstract |
| later catalogs identify MAINDEC-08-D1A as the Memory Power On/Off Test replacing Maindec 829 | `H/P*` | strong archival catalog/index evidence; exact DEC replacement document not facsimile-inspected here |
| a surviving D1AC paper-tape artifact is cataloged with a 16-Sep-1968 date | `H/P*` | archival media inventory |
| modern PDP-8/L restorers used revision-C D1AC and observed its error halt | `Experiment / later record` | restoration log |
| a Straight-8 restoration reported D1AC intermittently exposing locations cleared on power-off | `Experiment / later record` | restoration log |
| a post-cycle wrong bit does not by itself localize the physical cause | `E` | mechanism/test reconstruction |
| a power-cycle diagnostic pass is not a quantified long-term retention lifetime | `E` | scope reconstruction |
| the diagnostic and KR01 prove the same retained relation | `X` | rejected; core payload qualification vs execution-state save/restart |
| the modern restoration results establish historical field failure frequency | `X` | rejected |

`H/P*` marks claims grounded in archival indexes/media custody rather than direct page-level inspection of the underlying DEC D1AC document body in this pass.

---

## What this slice closes

For Case 02, this closes a bounded part of the previously open **hardware restoration / diagnostic validation** debt:

- DEC had a period maintenance program explicitly dedicated to checking memory after simulated power failure;
- the test vocabulary distinguished bit dropout and pickup;
- the diagnostic family survives as executable media;
- modern PDP-8 restoration work demonstrates that the diagnostic can expose real post-power-cycle corruption on surviving hardware.

It does **not** close:

- Whirlwind / Memory Test Computer startup-shutdown primary evidence;
- 1950s genealogy of power-transition qualification;
- exact D1AC revision-by-revision code/document genealogy;
- controlled brownout / partial-rail fault matrices;
- quantitative environmental/temperature dependence of transition survival;
- instrumented current/voltage traces tying a failed diagnostic to one physical mechanism;
- statistically controlled repeated-power-cycle experiments across multiple restored machines.

Those are separate slices. Broader maintenance-diagnostic and core-memory engineering history belongs primarily in `tmzncty/computing-archaeology`; this record keeps only the retention-specific boundary.

---

## Sources

### Primary / period

1. Digital Equipment Corporation, *PDP-8 Program Abstracts*, `DEC-08-BA1A-D`, archival file dated 1966-10-11; entry `Maindec 829 — PDP-8 Memory Power On/Off Test`. Bitsavers: <https://bitsavers.org/pdf/dec/pdp8/software/DEC-08-BA1A-D_PDP-8_Program_Abstracts_19661011.pdf>.
2. Digital Equipment Corporation, `MAINDEC-08-D1AC-D`, *Memory Power On/Off Test*, surviving seven-page diagnostic document in Bitsavers' PDP-8 diagnostic archive: <https://bitsavers.trailing-edge.com/pdf/dec/pdp8/diag/MAINDEC-08-D1AC-D.pdf>. The document was located but its page images could not be rendered in this pass; no unseen wording is attributed to it here.
3. Surviving DEC paper-tape inventory entry, `MAINDEC-08-D1AC-PB — PDP-8 MEMORY POWER ON/OFF TEST`, dated 16-Sep-68, in Jay Jaeger's PDP-8/PDP-12 tape collection inventory: <https://www.bitsavers.org/bits/DEC/pdp12/papertapeimages/From_JayJaeger/PaperTape-List-PDP8-PDP12.pdf>.

### Archival indexes / custody

4. David Gesswein, PDP-8 software file index, entry `Memory Power On/Off Test (replaces maindec-829)` with revision-C part numbers: <https://so-much-stuff.com/pdp8/software/dec.php>.
5. ACONIT PDP-8/p Software Repository, surviving D1AC paper-tape artifact listing: <https://pop.aconit.org/Programs/>.

### Modern restoration / experiment records

6. Rhode Island Computer Museum, PDP-8/L restoration log, revision-C D1AC execution and error-halt investigation: <https://www.ricomputermuseum.org/collections-gallery/equipment/pdp-8-l/pdp-8-l_blog>.
7. David Gesswein, PDP-8 Straight-8 functional restoration, intermittent D1AC failure with locations cleared on power-off: <https://www.pdp8online.com/straight8/functional_restore.shtml>.
8. David Gesswein, PDP-8 Straight-8 diagnostics page, summarized D1AC operating sequence and surviving binary: <https://www.pdp8online.com/straight8/straight8-maindecs.shtml>.
