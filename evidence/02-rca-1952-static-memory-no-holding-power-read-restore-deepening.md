# Case 02 Deepening — RCA 1952 `Static` Magnetic Memory: No Holding Power != Read Invariance

**Status:** `bounded deepening complete`

## Purpose

This record deepens [`../cases/02-magnetic-core-destructive-read.md`](../cases/02-magnetic-core-destructive-read.md) around one narrow historical and technical boundary:

> what did `static` and no-holding-power retention mean in a period magnetic-memory source when the same realized system still used access-triggered restoration?

Case 02 already grounds magnetic remanence, coincident-current selection, destructive/interrogative read semantics, and rewrite/restore through Forrester, Papian, Brown, Widrow, and named production systems. It also has a later IBM 705 vocabulary deepening in which 1955 public sales literature describes core memory with apparently horizonless retention language.

The new contribution here is different. Jan A. Rajchman's June 1952 RCA technical paper gives a contemporaneous, independently realized **RCA experimental magnetic-matrix memory** and places three properties in the same source:

1. the article itself calls the design **`Static Magnetic Matrix Memory`**;
2. its summary and conclusion describe quiescent storage as requiring **no external holding power**;
3. its operating description shows that interrogation can disturb the selected core and that the read path restores the prior state when necessary.

This gives a direct period counterexample to an overbroad modern reading of `static`:

```text
quiescent state needs no holding power
    !=
access leaves the physical state untouched
    !=
no restoration work occurs during service
```

The slice also closes one explicit open item in [`02-ibm-705-1954-1955-indefinite-retention-vocabulary-deepening.md`](02-ibm-705-1954-1955-indefinite-retention-vocabulary-deepening.md): add a controlled non-IBM vendor comparison without assuming shared circuitry from shared retention adjectives.

Claim layers remain separated as required by repository policy: **Historical record**, **Engineering reconstruction**, **Functional analogy**, and **Philosophical interpretation**.

---

## Sources inspected

### A. Jan A. Rajchman, `Static Magnetic Matrix Memory and Switching Circuits`, *RCA Review*, June 1952

Primary technical paper:

- Jan A. Rajchman, **`Static Magnetic Matrix Memory and Switching Circuits`**, *RCA Review*, vol. XIII, no. 2, June 1952, pp. 183–201;
- author affiliation printed in the paper: Research Department, RCA Laboratories Division, Princeton, New Jersey;
- period issue scan: <https://www.worldradiohistory.com/ARCHIVE-RCA/RCA-Review/RCA-Review-1952-Jun.pdf>;
- alternate preserved scan / extracted-text mirror used for line-level inspection in this research environment: <https://device.report/m/283cceb7e6eba8fa9ce843f1ff177ce02677e2b5e2d66c270dbb644d4de06880>.

The issue table of contents places the paper at printed p. 183. The issue identifies *RCA Review* as a technical journal of the RCA Laboratories Division and is dated June 1952.

The paper's summary says the memory has several-microsecond access, **`indefinitely long storage requiring no holding power`**, and reports an operating experimental model with a capacity of **256 bits**.

The conclusion returns to the same physical relation, describing the two remanent states as providing indefinite storage without external holding power.

### Source-custody note

The full June 1952 issue was located through two period-scan mirrors. The current research environment could inspect the extracted primary text and printed pagination but the direct PDF hosts returned HTTP 403 when page-image rendering was attempted. Accordingly:

- claims below are restricted to text whose printed-page position and wording are recoverable from the scanned issue's extracted text;
- no argument depends on interpreting an unrendered circuit figure;
- figure-level details are not promoted beyond what the article's prose explicitly states.

This is a source-access limitation, not a reason to substitute a later textbook for the period paper.

### B. Milton Rosenberg, `Magnetic Core Memory System`, US 2,900,623

Later primary patent used only as a reception / prior-art cross-check:

- Milton Rosenberg, **`Magnetic Core Memory System`**, U.S. Patent 2,900,623;
- filed 5 April 1954;
- published / issued 18 August 1959;
- <https://patents.google.com/patent/US2900623A/en>.

The patent's background explicitly cites both Forrester's January 1951 magnetic-core paper and Rajchman's June 1952 `Static Magnetic Matrix Memory and Switching Circuits` paper while describing coincident-current core memory.

This later patent is **not** used to move the 1952 publication date, establish Rajchman priority, or prove that the 1952 implementation already had every later patent feature. It is useful only as an independent primary record that the 1952 paper became part of the technical prior-art chain visible to later magnetic-memory work.

### C. Existing repository evidence used for bounded comparison

This slice reuses rather than duplicates:

- [`02-magnetic-core-1951-1954-grounding.md`](02-magnetic-core-1951-1954-grounding.md), for Forrester/Papian/Brown/Widrow mechanism grounding;
- [`02-ibm-705-1954-1955-indefinite-retention-vocabulary-deepening.md`](02-ibm-705-1954-1955-indefinite-retention-vocabulary-deepening.md), for IBM's later public `indefinitely` vocabulary and the warning that a horizonless adjective is not a quantified retention test;
- [`02-1965-1966-core-power-transition-retention-deepening.md`](02-1965-1966-core-power-transition-retention-deepening.md), for the later distinction between remanence and power-transition immunity;
- [`02-ibm-7090-1960-1962-power-on-clear-retention-policy-deepening.md`](02-ibm-7090-1960-1962-power-on-clear-retention-policy-deepening.md), for the later distinction between material nonvolatility and machine restart policy.

The broad history of core selection, Whirlwind, manufacturing, and why core memory was worth building remains in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md).

---

# Historical record

## 1. `Static magnetic matrix memory` is period vocabulary by June 1952

The strongest terminology fact is in the article title itself:

```text
Static Magnetic Matrix Memory and Switching Circuits
```

That matters because the project does not need to invent `static` as a retrospective label for this particular RCA design. It is contemporary vocabulary used by Rajchman in a public RCA technical journal.

The safe historical statement is therefore:

> **By June 1952, Rajchman publicly described the RCA design as a `static magnetic matrix memory`.**

The unsafe statement would be:

> **June 1952 was the first use or invention of `static memory`.**

This slice does not establish first coinage. It establishes a conservative public-document floor in one inspected source.

## 2. The source defines the storage problem through stable physical states

On printed p. 183 Rajchman distinguishes matrix memory from memories that use time as a switching variable. In the matrix case, a storage cell must have at least two physical stable states and must be switchable through coincident inputs.

This is period technical framing, not a later philosophical paraphrase:

```text
stable physical states
+
selective matrix switching
->
addressable stored bit
```

Rajchman then treats switching nonlinearity, not the mere existence of a stable state, as the hard system problem.

That wording is important for retention analysis because the state does not count as useful memory merely by surviving. It must remain selectively addressable and controllably changeable.

## 3. The summary explicitly joins long storage with absence of holding power

The paper's printed summary gives the design three salient properties together:

- access in several microseconds;
- apparently horizonless storage with no holding power;
- the possibility of large capacity at low cost.

It also states that an operating **256-bit experimental model** had been built.

The bounded historical claim is:

> **RCA's June 1952 technical paper publicly connected magnetic-remanent storage with no holding-power requirement and did so in the context of an actually operating 256-bit experimental model.**

This is stronger than a purely hypothetical patent proposal and narrower than a commercial-shipment claim.

## 4. The paper's interrogation sequence includes conditional restoration

Printed pp. 190–191 describe a three-step operating schedule for the memory matrix.

For reading / interrogation:

1. the selected memory core is driven toward one reference direction (`P`);
2. the presence or absence of a read signal indicates whether it had initially been in the opposite (`N`) or already-reference (`P`) state;
3. if the first step disturbed an `N` core by driving it toward `P`, the commutator restoration sequence returns it to its initial `N` state;
4. if no signal occurred because the core was already in `P`, the subsequent sequence leaves it in `P`.

The paper also describes an alternative two-step schedule in which the read signal determines whether an inhibit pulse is used so that a disturbed core is restored to its pre-read state.

The exact circuit schedule is source-specific. The retention point is simple:

```text
read determines old state
    by a physical operation that may change the selected core

continued logical retention
    can therefore require conditional restore
```

This is not a modern analogy imposed on the source. Restoration is part of the period operating description.

## 5. The complete 256-bit unit was wired for nondestructive logical readout by restoration

Printed pp. 199–200 describe the experimental 16 × 16 matrix, i.e. **256 storing cores**, driven by two 16-core commutator switches.

The paper says the reading circuit was connected to restoring circuits so that the complete unit could read without losing the logical information. The experimental system used a three-step schedule; Rajchman reports approximately **15–24 microseconds** access for that particular setup, derived from core turnover times of roughly 5–8 microseconds.

These numbers are machine-specific. They are useful here because they show that restoration was not merely a conceptual footnote: it occupied part of the realized operating schedule.

Therefore:

```text
logical nondestructive read service
    can be built from
physically disturbing interrogation + restoration
```

The phrase `nondestructive` at the logical-service level must not be confused with `the selected physical core was never disturbed`.

## 6. The conclusion repeats no-holding-power retention after describing active restore machinery

Printed pp. 200–201 return to the physical storage claim: the two remanent magnetization states provide indefinite storage without external holding power.

Because this conclusion comes **after** the paper's detailed operating and restoring sequences, the source itself blocks a simplistic equivalence:

```text
no holding power while quiescent
    !=
no active work when accessed
```

The distinction is historically visible inside one article rather than being assembled solely by comparing technologies separated by decades.

## 7. The paper acknowledges MIT/Papian material information, but this is not a complete genealogy

Rajchman's acknowledgments say the work was facilitated by information on materials from the MIT group, particularly W. N. Papian, and also name several material suppliers.

This is useful actor-level contact evidence. It permits the narrow statement:

> **RCA's 1952 work was not historically isolated from the MIT magnetic-core research milieu.**

It does **not** establish that:

- RCA copied the exact MIT memory circuit;
- the restoring schedule came from Papian;
- every magnetic material or core geometry was shared;
- one institution's design was simply a derivative implementation of the other.

The source explicitly says `information on materials`; genealogy must not be expanded beyond what is actually acknowledged.

---

# Engineering reconstruction

## 1. `Static` here is a quiescent-retention relation, not a promise of total operational stillness

The source permits a much more precise reconstruction than the modern shortcut `static = nothing changes`.

For the bounded RCA design:

```text
between operations:
remanent state can persist without holding power

on access:
selection currents act on the chosen core
interrogation may alter that core
restore logic may have to re-establish the old logical state
```

Thus:

```text
static retention
    !=
static physical trajectory during access
```

The stored logical relation can be stable while its immediate physical embodiment is intentionally switched and then reconstructed.

## 2. `No holding power` is not `no support apparatus`

The phrase concerns what is required to keep the remanent state during the storage interval. It does not eliminate:

- drive currents for selection;
- magnetic commutator switching;
- sense / read circuitry;
- restoring currents;
- timing / pulse sequencing;
- the energy required to read, write, or restore.

A correct engineering paraphrase is therefore:

> the quiescent storage state does not require continuous external holding power merely to remain represented.

It would be an overreach to rewrite that as:

> the memory requires no power or active support.

## 3. `Indefinite` is not a quantified retention lifetime

Like the later IBM 705 wording, Rajchman's `indefinite` language is not accompanied in this article by a numerical dormant-retention interval, confidence level, bit-error threshold, temperature envelope, or spontaneous-decay distribution.

The paper therefore supports:

```text
period claim of no practical stated storage horizon
```

but not:

```text
measured infinite lifetime
```

or:

```text
universal retention specification for ferrite / magnetic cores
```

The 1952 RCA source is technically richer than a sales brochure because it gives mechanism and an operating model. That still does not turn `indefinite` into a modern qualification test.

## 4. Quiescent retention and access retention are two separate contracts

The paper makes it possible to state two different retention questions using one historical system:

```text
Contract A — quiescent:
Does the represented state remain when no access is occurring?

Contract B — through access:
Does the logical value remain available after an interrogation that may switch the selected core?
```

Contract A is supported by remanence and no holding power.

Contract B is supported by the read / restore operating sequence.

A technology can satisfy A strongly while satisfying B only because active restoration closes the access cycle.

## 5. Logical nondestructiveness can be an achieved service property rather than an untouched-medium property

The complete experimental setup is described as reading nondestructively because its restoring circuitry makes the **logical value** survive the operation.

But the detailed schedule shows how that service property is produced:

```text
initial logical state
    -> interrogation
    -> possible physical disturbance
    -> sensed result
    -> conditional restore
    -> same logical state available again
```

This distinction is reusable across the repository:

```text
post-operation logical equality
    !=
absence of physical disturbance during the operation
```

The comparison is functional. It does not imply that every system achieving nondestructive logical service uses the same mechanism.

## 6. An operating experimental model is not a shipping product

The paper's 256-bit model is significant evidence because it ties the mechanism to hardware that Rajchman reports as operating successfully.

But the evidence class is:

```text
realized laboratory / experimental system
```

not:

```text
commercial production machine
```

Therefore this slice does not claim shipment date, deployed reliability, field lifetime, or customer restart semantics.

## 7. Remanence does not answer the power-transition question

The phrase `no holding power` concerns the state while holding power is absent. It does not specify what happens **during the transition** into or out of that condition.

Later Case-02 evidence shows why the distinction matters in actual machines:

```text
quiescent unpowered retention
    !=
power-transition immunity
    !=
startup preservation policy
    !=
execution continuity
```

Nothing in Rajchman 1952 should be silently upgraded into a claim that the 256-bit experimental setup survived arbitrary brownouts, supply transients, or restart sequences with its logical image intact.

---

# Controlled functional comparison

## 1. RCA 1952 technical-paper vocabulary vs IBM 705 1955 product vocabulary

The existing IBM 705 deepening and this RCA source both use language with no explicit finite horizon, but the source genres differ.

```text
RCA 1952 technical paper:
    `static` magnetic matrix memory
    remanent states
    no holding power
    explicit interrogation / restore mechanism
    operating 256-bit experimental model

IBM 705 1955 promotional literature:
    public product-facing `indefinitely` vocabulary
    product capacity / access rhetoric
    no comparable retention-test envelope on that brochure page
```

The legitimate comparison is:

> by the early-to-mid 1950s, more than one vendor/institutional source could describe magnetic-core endurance with apparently horizonless language, while the evidential content of those documents remained different.

The illegitimate inference is:

> RCA and IBM therefore used the same circuitry, test method, or retention contract.

Shared adjectives do not establish shared mechanism.

## 2. RCA 1952 and the MIT/Whirlwind core case

Both source families deal with magnetic states and restorative read cycles, but the project should not duplicate the broad engineering history already maintained in `computing-archaeology`.

The useful bounded comparison is:

```text
RCA 1952:
no-holding-power quiescent retention
+
conditional restore in the experimental read schedule

MIT core evidence:
remanent retention
+
classic destructive read / rewrite in the documented memory cycle
```

Rajchman's acknowledgment of material information from the MIT group is real historical contact evidence. It is not enough to derive a complete circuit genealogy.

## 3. Functional bridge to DRAM — only at the restore-obligation level

A distant later comparison can be made only at one function:

```text
access can leave a storage element needing restoration
```

Core magnetization switching and DRAM charge sensing are physically different, historically separated mechanisms. The analogy must not be turned into a common-device genealogy or into the statement that core and DRAM are `the same kind of memory` because both restore.

---

# Philosophical interpretation

The technical fact that motivates interpretation is unusually crisp:

> the source calls the memory `static` and says its state requires no holding power, yet the same paper gives a temporally staged read/restore sequence that may disturb and reconstruct the selected stored state.

A bounded conceptual consequence is:

> **technical stillness is relation-specific.**

The state can be `static` with respect to the need for continuous holding energy while remaining operationally dynamic with respect to access.

That helps discipline broader claims about persistence:

```text
what remains
    depends on
which interval and which operation are being considered
```

This is a project interpretation, not Rajchman's philosophical vocabulary.

The paper should not be made to say that memory is metaphysically static, that technological permanence is an illusion, or that restoration constitutes identity in a philosophical sense. It supplies an engineering counterexample to any theory that treats `retained` and `unchanged at every physical instant` as synonyms.

---

# Prior-art boundary changed by this slice

Before this deepening, Case 02 already had strong mechanism evidence and a 1955 IBM public `indefinitely` vocabulary witness.

This source changes the conservative public-document floor for a more specific relation:

```text
by June 1952:
period public technical vocabulary directly joins
`static magnetic matrix memory`
+
no-holding-power quiescent storage
+
realized experimental hardware
+
access-triggered restoration
```

That is useful prior art against any project novelty claim phrased as:

> only later computer-memory discourse discovered that a state could persist without continuous holding energy while access still required active reconstruction.

The historically defensible project contribution is narrower:

> compare such retention relations across unlike mechanisms while preserving their exact source vocabulary, maintenance trigger, state boundary, and historical genealogy.

---

# Explicit non-claims

This evidence does **not** establish any of the following:

1. Rajchman invented magnetic-core memory.
2. RCA invented coincident-current selection.
3. June 1952 is the first use of the word `static` for a memory.
4. June 1952 is the first use of `indefinite` for technical storage.
5. `static magnetic matrix memory` is identical to the later formal category `static RAM` / SRAM.
6. `static` is identical to the later standardized category `nonvolatile memory`.
7. `indefinite` means literally infinite thermodynamic lifetime.
8. the article supplies a quantified dormant-retention distribution.
9. no holding power means no energy is used during read, write, selection, or restore.
10. no holding power means no peripheral electronics are needed.
11. no holding power proves immunity to power-on or power-off transients.
12. the experimental 256-bit model was a commercial product.
13. the experimental model's 15–24 microsecond access figure is universal for core memory.
14. logical nondestructive read means the physical core was never disturbed.
15. every magnetic-core read scheme is destructive.
16. RCA's restoration schedule is identical to MIT's or IBM's.
17. Rajchman's acknowledgment of MIT/Papian material information proves wholesale circuit transfer.
18. later patents citing Rajchman prove invention priority.
19. shared use of `indefinite` / `static` language proves shared vendor test methods.
20. retained core payload implies retained CPU, control, peripheral, or execution state.
21. remanence guarantees arbitrary restart continuity.
22. this slice replaces the broader magnetic-core history in `computing-archaeology`.
23. the project term `quiescent-retention contract` was used by Rajchman.
24. the project interpretation `technical stillness is relation-specific` was a historical actor's formulation.

---

# Resulting bounded distinctions

```text
period `static` vocabulary
    != modern SRAM taxonomy
    != universal NVM taxonomy

remanent stable state
    != quantified lifetime guarantee

no holding power during storage
    != no operating energy
    != no support apparatus

quiescent retention
    != read invariance

physical disturbance on access
    != logical data loss
    when restoration closes the cycle

logical nondestructive service
    != untouched physical embodiment

experimental model operating
    != product shipment
    != field reliability record

historical contact / acknowledged material information
    != complete mechanism genealogy

payload retained
    != transition immunity
    != restart preservation policy
    != execution continuity
```

---

# Related-repository routing

A fresh check of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found the existing broad core-memory history:

- [`docs/memory/why-core-memory-was-worth-weaving.md`](https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md)

That article already covers why coincident-current core was attractive, Whirlwind, selection geometry, destructive readout, and manufacturing. This record therefore keeps only the retention-specific source problem:

- period `static` vocabulary;
- no-holding-power quiescent retention;
- read-triggered physical disturbance and restoration;
- source-genre comparison with IBM's later `indefinite` wording;
- exact limits of the RCA↔MIT historical contact evidence.

A broader RCA magnetic-memory history, materials-supplier history, or institutional priority dispute belongs primarily in `computing-archaeology` if pursued.

---

# Open work deliberately left outside this slice

- search pre-June-1952 RCA internal reports, conference papers, patent applications, and lab memoranda for an earlier `static` / no-holding-power wording floor;
- determine whether Rajchman's 1952 paper's wording can be traced to a specific earlier internal RCA document;
- reconstruct the exact patent chronology around Rajchman / Rosenberg magnetic matrix and switching applications without converting filing order into invention priority;
- inspect surviving experimental documentation for the 256-bit RCA unit's actual power-down / power-up behavior;
- recover any specified environmental or long-duration remanence test for that exact RCA hardware;
- compare Burroughs, Remington Rand/UNIVAC, DEC, and other vendor period vocabulary without normalizing different source genres into one retention metric;
- keep broad magnetic-core engineering genealogy and manufacturing history in `computing-archaeology`;
- keep later restored-machine experiments separate from claims about the 1952 laboratory unit.

These are follow-on slices, not blockers for the bounded result established here.

---

# Sources

1. Jan A. Rajchman, **`Static Magnetic Matrix Memory and Switching Circuits`**, *RCA Review*, vol. XIII, no. 2, June 1952, pp. 183–201. Period issue scan: <https://www.worldradiohistory.com/ARCHIVE-RCA/RCA-Review/RCA-Review-1952-Jun.pdf>. Alternate preserved scan / text view: <https://device.report/m/283cceb7e6eba8fa9ce843f1ff177ce02677e2b5e2d66c270dbb644d4de06880>.
2. Milton Rosenberg, **`Magnetic Core Memory System`**, U.S. Patent 2,900,623, filed 5 April 1954, issued 18 August 1959. <https://patents.google.com/patent/US2900623A/en>.
3. Existing Case-02 grounding and follow-on evidence linked above.
4. [`tmzncty/computing-archaeology`, `Why Was Magnetic-Core Memory Worth Weaving by Hand?`](https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md), used for related-repository routing rather than duplicated here.
