# Case 02 Deepening — IBM 705 "Indefinite" Magnetic-Core Retention Vocabulary (1954–1955)

**Status:** `bounded deepening complete`

## Purpose

This record deepens [`../cases/02-magnetic-core-destructive-read.md`](../cases/02-magnetic-core-destructive-read.md) around one deliberately narrow historical-language question:

> by the first commercial IBM 705 promotional literature, how was the temporal endurance of magnetic-core memory described to users, and how far can that wording legitimately be converted into a technical retention claim?

The useful result is not a new claim that magnetic core was nonvolatile; Case 02 already grounds remanence, destructive read, restoration, operating margins, and later power-transition behavior. The new result is a source-controlled boundary around the word **`indefinitely`** in IBM's 1955 public 705 literature.

The 1955 brochure says that magnetic cores can "remember" information indefinitely and that the cores are extremely stable and will last indefinitely. That wording is historically important because it shows IBM publicly presenting magnetic-core memory through an apparently horizonless retention vocabulary. It is not, however, a quantified lifetime specification, a field-failure distribution, a power-cycle qualification, a restart guarantee, or a promise that every logical value remains correct under arbitrary machine operation.

This record therefore separates:

```text
period retention vocabulary
    !=
quantified retention specification
    !=
power-transition qualification
    !=
restart-preservation policy
    !=
whole-machine execution continuity
```

Claim layers follow repository policy: **Historical record**, **Engineering reconstruction**, **Functional analogy**, and **Philosophical interpretation** remain distinct.

---

## Sources inspected

### 1. IBM, *Magnetic Cores for Memory in Microseconds in a Great New IBM Electronic Data Processing Machine for Business* (1954)

Primary IBM promotional literature preserved by the Computer History Museum (CHM), accession **102646305**.

CHM catalog record:

- <https://www.computerhistory.org/brochures/doc-4372957027054/>

Preserved scan:

- <https://d1yx3ys82bpsa0.cloudfront.net/brochures/ibm.705.1954.102646305.pdf>

CHM dates the brochure to **1954** and identifies it as IBM Data Processing Division promotional material for the 705. The inspected scan emphasizes magnetic-core memory's random accessibility, a **17-microsecond-per-character** access figure, the **20,000-character** core capacity, and calls it the fastest electronic storage then developed.

A direct text search of the inspected 1954 scan finds no occurrence of `indefinite` or `remember`. This is useful only as a version boundary for the **surviving inspected brochure**. It does not prove that IBM had never used similar language elsewhere in 1954, nor that no un-OCRed graphic or separate publication used it.

**Evidence boundary:** the 1954 brochure establishes an earlier IBM 705 commercial core-memory document whose surviving searchable text foregrounds speed, capacity, and random accessibility. It is not evidence that the later 1955 retention vocabulary had not yet been conceived.

### 2. IBM, *705 EDPM Electronic Data Processing Machine* (1955)

Primary IBM promotional literature preserved by CHM, accession **102646306**.

CHM catalog record:

- <https://www.computerhistory.org/brochures/doc-4372957022230/>

Preserved scan:

- <https://s3data.computerhistory.org/brochures/ibm.705-edpm.1955.102646306.pdf>

CHM dates this brochure to **1955**. On scanned page 8, under `Magnetic Core Memory`, IBM describes magnetic cores as objects that can **"remember" information indefinitely** and later states that the cores are extremely stable and **"will last indefinitely."** The same paragraph also gives the 705's 20,000-character capacity and 17-microsecond access figure.

The brochure's description is product-facing rather than a materials-test report. No numerical retention duration, temperature envelope, confidence level, bit-error criterion, power-cycle procedure, or allowed disturbance history accompanies the word `indefinitely` on that page.

The same 1955 brochure also uses `permanent files` for magnetic-tape data. That neighboring vocabulary is a useful warning against silently reading one promotional adjective as a modern standardized reliability quantity.

**Evidence boundary:** this source directly establishes a public IBM 705 **wording floor by 1955**. It does not establish first coinage, universal IBM terminology, literal infinite physical lifetime, or a formal warranty contract.

### 3. Aaron Sidney Wright, “The Physics of Forgetting: Thermodynamics of Information at IBM 1959–1982” (2016)

Peer-reviewed historical study:

- Aaron Sidney Wright, *Perspectives on Science* 24(1), 2016, pp. 112–141;
- DOI: <https://doi.org/10.1162/POSC_a_00194>
- MIT Press record: <https://direct.mit.edu/posc/article/24/1/112/15526/The-Physics-of-Forgetting-Thermodynamics-of>

Wright independently reproduces the 1955 IBM 705 wording while discussing IBM's ferrite-core material context and explicitly characterizes the `indefinite` formulation as hyperbolic marketing. This later scholarship is useful as source criticism, not as a substitute for the primary IBM brochure.

**Evidence boundary:** Wright supports the interpretation that the brochure's rhetoric should not be promoted into a literal infinite-retention specification. The technical mechanism and period wording remain grounded in primary sources.

---

## Historical record — IBM publicly used horizonless retention language by 1955

The primary 1955 brochure establishes that IBM was willing to describe magnetic-core memory to prospective users with language that erased an explicit time horizon. The same page couples that language to familiar product quantities such as capacity and access time:

```text
20,000 characters
17 microseconds access
"indefinitely" retained / enduring core state
```

The categories are not evidentially equivalent. Capacity and access time are numerical product characteristics; `indefinitely` is not accompanied by an equivalent test condition or numerical limit.

This is nevertheless real historical vocabulary. It should not be replaced by a modern paraphrase such as `nonvolatile NVM with infinite data-retention time`, because the latter imports later categories and a precision the brochure does not supply.

The bounded historical statement is:

> **By 1955, surviving IBM 705 public promotional literature described ferrite-core memory using `indefinitely` as an endurance/retention adjective.**

That statement is stronger than saying only that later historians call core memory nonvolatile, and weaker than saying IBM certified infinite retention.

---

## Historical record — the surviving 1954 and 1955 brochures should not be silently merged

The inspected 1954 705 brochure already makes magnetic-core memory central to the product. Its surviving searchable text emphasizes:

- random accessibility;
- 17 microseconds per character;
- 20,000 stored alphabetic/numerical characters;
- magnetic core as exceptionally fast electronic storage.

The inspected 1955 brochure adds explicit `remember ... indefinitely` / `last indefinitely` language.

This supports a document-version distinction:

```text
1954 inspected brochure
    -> core-memory speed / capacity / access rhetoric

1955 inspected brochure
    -> same product family
    -> explicit "indefinitely" retention rhetoric
```

But this is **not** a demonstrated conceptual transition inside IBM. The source set is too small to infer when the wording was drafted, whether other 1954 sales sheets already used it, or whether the 1955 sentence came from a technical manual, advertising copy, or another internal source.

Therefore:

```text
first wording found in this bounded source set
    !=
first wording ever used by IBM
```

---

## Historical record — `indefinitely` coexists with destructive access semantics

The 1955 brochure's broad wording does not repeal the mechanism already grounded in Case 02. Classic coincident-current magnetic-core memory can be stable while idle and still use a read operation that changes the selected magnetic state and requires regeneration/rewrite.

This matters because `indefinitely` could otherwise be misread as `the same physical configuration remains untouched forever`.

The retention relation is more specific:

```text
quiescent magnetic remanence can be highly stable

ordinary access can intentionally alter the selected core state

logical persistence through access can depend on restore / rewrite
```

The new brochure evidence therefore belongs at the **vocabulary** layer. The mechanism remains grounded by the Forrester/Papian/Widrow evidence already cited in Case 02.

---

## Engineering reconstruction — a horizonless adjective is not a retention test

A modern technical retention specification normally needs at least some combination of:

- a duration or lower bound;
- environmental conditions;
- a permitted error criterion;
- a defined stored state population;
- a disturbance/access history;
- a power condition;
- a test method and observation point.

The inspected IBM 705 promotional paragraph does not supply those dimensions for `indefinitely`.

Therefore the strongest justified engineering reconstruction is negative:

> **the 1955 wording is insufficient to calculate or bound a core's physical retention lifetime.**

That is not evidence that the cores were unreliable. It is a statement about what this source can and cannot establish.

The distinction is especially important in this repository because Case 02 already shows several other ways a core-memory system can fail while the ferrite element remains capable of remanence: half-select disturbance, sense/drive margin loss, failed regeneration, destructive power-transition currents, and deliberate startup clearing.

---

## Engineering reconstruction — material endurance, transition survival, and restart authority are separate relations

Later Case-02 evidence provides a useful stress test for the 1955 commercial wording.

The IBM 7090 record shows a machine policy in which `Reset` can leave core storage unchanged while ordinary Power On includes a `Clear` operation. The 1965 IBM 1401 and 1966 DEC PDP-7 records show other machines in which controlled power transitions can preserve core contents, with the PDP-7 explicitly sequencing supplies to prevent destructive transition currents.

Those later machine-specific sources are not evidence about the 705 itself. They are counterexamples to an overbroad interpretation of the word `indefinitely`:

```text
core can physically retain a magnetic state
    !=
startup policy must preserve the old logical image

core can retain state while unpowered
    !=
power transition cannot disturb it

core payload can survive
    !=
CPU / control / peripheral state survives
```

Thus the 1955 brochure's retention rhetoric belongs to a narrower physical/product-description layer than machine restart semantics.

---

## Engineering reconstruction — `indefinite` is not the same as `maintenance-free`

The brochure describes the core as stable, but the assembled memory remains an active electromechanical/electronic system when in service. Case 02 already grounds:

- destructive read followed by rewrite in the classic scheme;
- sensitivity to drive and sensing margins;
- disturbance of half-selected neighbors as a design concern;
- later temperature-dependent margin-control strategies;
- machine-specific power-transition protections.

Therefore:

```text
no periodic refresh needed to preserve an idle remanent bit
    !=
no maintenance or control work anywhere in the memory system
```

The 1955 wording should not be turned into a claim that magnetic-core memory had no operational maintenance burden.

---

## Functional analogy — contrast with later numerical retention contracts

A bounded functional comparison to later semiconductor-storage documentation is useful because later Flash/SSD documents often state finite retention intervals under named temperature/endurance conditions.

The comparison is only about **document semantics**:

```text
IBM 705 promotional adjective:
    "indefinitely"
    without an explicit numerical qualification envelope on the page

later retention qualification / product contracts:
    finite interval
    + stated operating / endurance / temperature conditions
```

This does not mean later SSD standards descend from IBM 705 brochure language, nor that one documentation style is universally more truthful. It shows why the project must not normalize unlike period claims into one modern `retention time` field without preserving their evidential form.

---

## Philosophical interpretation — the word `indefinite` can hide the apparatus around endurance

The technical fact is modest: a product brochure uses an apparently unlimited temporal adjective for a physical storage element while the working memory system still depends on read/regenerate cycles, addressing, operating margins, and machine policy.

A bounded interpretation is therefore:

> **commercial language can present endurance as absence of a time horizon even when operational persistence remains conditional on an apparatus and a sequence of permitted operations.**

This is a project interpretation, not a claim that IBM engineers adopted a philosophy of timeless memory.

The point also stops short of saying that `indefinite` is false. In engineering prose, an indefinite practical lifetime can mean that another system limit dominates before spontaneous state decay becomes the relevant failure mode. The brochure does not supply enough evidence to determine such a quantitative crossover.

---

## Source-genre boundary — sales literature is evidence, but for a different question

Promotional literature is sometimes dismissed as `not technical`. That would be a mistake here. It is primary evidence for:

- what a vendor chose to tell customers;
- which properties were made salient;
- which vocabulary entered public product discourse;
- how a new storage mechanism was framed relative to older media.

But source genre matters. A sales brochure is weaker than a controlled test report for:

- retention distributions;
- environmental margins;
- failure probabilities;
- warranty conditions;
- exact power-transition behavior;
- field-reliability statistics.

The correct use of the 1955 IBM source is therefore neither `ignore it` nor `read it literally as a lifetime certification`.

---

## Prior-art and genealogy boundaries

This deepening does **not** claim:

- that IBM invented magnetic-core memory;
- that IBM first used `indefinite` or `indefinitely` for technical memory;
- that the 1955 brochure is the first IBM document to use the wording;
- that the absence of a searchable match in the inspected 1954 brochure proves IBM did not use similar language elsewhere in 1954;
- that every IBM 705 installation preserved core contents through arbitrary outage or power cycling;
- that `indefinitely` means infinite thermodynamic lifetime;
- that `indefinitely` is a quantified warranty or a bit-error-rate promise;
- that core-state endurance implies nondestructive reads;
- that physical core-state endurance implies preserved CPU, control, peripheral, or operator context;
- that the IBM 7090, 1401, PDP-7, and 705 share one startup or power-control circuit;
- that later terms such as `nonvolatile memory`, `persistent memory`, `data-retention specification`, or `persistence domain` were IBM's 1955 product vocabulary;
- that later JEDEC/SSD retention contracts are genealogically descended from this brochure.

Historical ordering is not engineering genealogy.

---

## Related-repository routing

The broad engineering history of ferrite-core memory, manufacturing, Whirlwind, and why hand-woven core was economically/technically attractive belongs primarily in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology), especially:

- <https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md>

This `technical-retention` record keeps only the retention-specific source problem: how a period vendor's apparently unlimited retention vocabulary should be related to material remanence, access restoration, machine transitions, and restart authority.

No separate general IBM 700-series history is created here.

---

## Resulting bounded distinctions

```text
1955 public IBM wording
    -> an attested historical retention vocabulary

"indefinitely"
    != infinite measured lifetime
    != numerical retention specification
    != warranty envelope

stable core material
    != read-invariant logical state

quiescent remanence
    != power-transition immunity
    != startup preservation policy

payload retained
    != processor / control state retained
    != exact execution resumed

source wording floor
    != invention / first-usage priority

promotional literature
    != useless evidence
    != controlled reliability experiment
```

---

## Open work deliberately left outside this slice

- search earlier IBM 702/704/701, engineering bulletins, sales manuals, and service documents for an earlier or more precise `indefinite` / `permanent` core-retention vocabulary floor;
- inspect IBM 705 operating/maintenance documentation for machine-specific power-on, reset, clear, and uncontrolled-power-loss semantics rather than inferring them from the brochure;
- determine whether the 1955 brochure wording can be tied to an earlier IBM technical report, internal engineering text, or named author;
- recover quantitative ferrite-core quiescent retention / spontaneous-transition evidence under specified temperature and material conditions;
- compare period vendor vocabulary across IBM, RCA, Burroughs, Remington Rand/UNIVAC, and DEC without treating shared adjectives as shared circuitry;
- keep detailed 700-series engineering genealogy and manufacturing history in `computing-archaeology`;
- keep modern restored-machine power-cycle experiments separate from historical claims.

These are follow-on slices, not prerequisites for the bounded conclusion established here.

---

## Sources

1. International Business Machines Corporation, *Magnetic Cores for Memory in Microseconds in a Great New IBM Electronic Data Processing Machine for Business*, 1954. Computer History Museum accession 102646305. Catalog: <https://www.computerhistory.org/brochures/doc-4372957027054/>. Scan: <https://d1yx3ys82bpsa0.cloudfront.net/brochures/ibm.705.1954.102646305.pdf>.
2. International Business Machines Corporation, *705 EDPM Electronic Data Processing Machine*, 1955. Computer History Museum accession 102646306, especially scanned p. 8, `Magnetic Core Memory`. Catalog: <https://www.computerhistory.org/brochures/doc-4372957022230/>. Scan: <https://s3data.computerhistory.org/brochures/ibm.705-edpm.1955.102646306.pdf>.
3. Aaron Sidney Wright, “The Physics of Forgetting: Thermodynamics of Information at IBM 1959–1982,” *Perspectives on Science* 24, no. 1 (2016): 112–141. DOI: <https://doi.org/10.1162/POSC_a_00194>. MIT Press: <https://direct.mit.edu/posc/article/24/1/112/15526/The-Physics-of-Forgetting-Thermodynamics-of>.

## Evidence-strength summary

| Claim | Layer | Strength |
| --- | --- | --- |
| a CHM-preserved IBM 705 brochure exists from 1954 and foregrounds core-memory speed/capacity/random access | Historical record | strong primary artifact + institutional catalog |
| the inspected 1954 scan has no searchable `indefinite` / `remember` match | Historical record about inspected artifact | direct bounded inspection; not proof about all 1954 IBM literature |
| a CHM-preserved IBM 705 EDPM brochure from 1955 uses `indefinitely` for magnetic-core retention/endurance | Historical record | strong primary artifact + institutional catalog |
| the 1955 wording supplies a quantitative infinite-lifetime guarantee | Rejected | brochure supplies no such test envelope |
| Wright 2016 treats the wording as hyperbolic marketing | Historiography | strong peer-reviewed secondary source |
| quiescent material retention must be separated from read/restore, transition protection, and restart policy | Engineering reconstruction | strong when composed with existing grounded Case-02 evidence |
| the 1955 brochure establishes first use or invention priority | Rejected | source set is insufficient |
| IBM 705 core state necessarily survived every power event | Rejected | no machine-level power-transition evidence established here |

## Completion note

This slice is complete at the intended boundary. It adds a directly inspected 1954/1955 IBM commercial-document comparison and a source-genre guardrail without reopening the already-grounded general history of magnetic-core memory. Case 02 remains `grounded`; no maturity promotion is claimed.