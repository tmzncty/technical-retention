# Case 02 — MTC 1956–1957 nonvolatile-medium / system boundary

## Scope

This bounded deepening asks whether mid-1950s sources already distinguished **nonvolatile media** from **whole systems that actually retain usable information through loss of power**.

Two primary witnesses answer yes:

- IRE Standard **56 IRE 8.S1**, *IRE Standards on Electronic Computers: Definitions of Terms, 1956*, `Proceedings of the IRE` 44(9), September 1956, pp. 1166–1173, DOI 10.1109/JRPROC.1956.275171.
- MIT Lincoln Laboratory's 1957 loose-leaf `MTC Service Manual` for the Memory Test Computer.

The result is deliberately narrow:

```text
nonvolatile medium
    != system power-removal retention
    != useful restart continuity
```

Case 02 remains `grounded`.

## Sources

IRE metadata and later dictionary reprint:

- <https://doi.org/10.1109/JRPROC.1956.275171>
- <https://www.worldradiohistory.com/Archive-IRE/IRE-Dictionary-1961.pdf>
- <https://eurekamag.com/research/097/774/097774629.php>

MTC archival scan and searchable mirror:

- <https://www.bitsavers.org/pdf/mit/lincolnLaboratory/mtc/MTC_Service_Manual_Apr57.pdf>
- <https://manuals.plus/m/5e67346e95f6d272d7b9fec609c6340771958a9ef9cdea3b203500a5a5e1ad74>

H. L. Ziegler's MTC cover memorandum is dated 15 April 1957. Relevant loose-leaf pages are later: power-control material is dated 27–28 June 1957, while Section 22's glossary is dated 12 August 1957.

The glossary explicitly says its general computing terms are reprinted from the September 1956 `Proceedings of the IRE`. Thus the `Volatile` wording below is IRE terminology reproduced by MTC, not terminology invented by MTC personnel.

## Historical record — IRE already separates medium and system

IRE 56 IRE 8.S1 defines `volatile` at the **storage-medium** level: the defining condition is inability to retain information without continuous power dissipation.

Its accompanying note then blocks the inverse inference. A device or system can use a nonvolatile medium yet still either retain or fail to retain information when power is removed.

Therefore the following anti-collapse is itself historically grounded by 1956 professional terminology:

```text
medium nonvolatility
    != device/system power-removal behavior
```

The standard does not provide a universal failure taxonomy and does not establish later concepts such as persistence domains or crash consistency as 1956 vocabulary.

## Historical record — MTC power transitions are ordered operations

The MTC manual says interlocks require voltages to be applied in a certain order to protect circuits.

Normal turn-off proceeds through Standby, loss of DC supplies, Power Off, and then breaker/control-power steps. Normal turn-on requires the relevant breakers, Standby and a roughly two-minute wait, then Power On; after a five-second warning interval, five supply indicators should appear sequentially over roughly three seconds.

This grounds:

```text
power transition
    != one instantaneous logical edge
```

The source says the order protects **circuits**. It does not specifically say the sequence protects core data. The later PDP-7 evidence in Case 02 remains the stronger source for that narrower claim.

## Historical record — core nonvolatility coexists with a powered operating margin

The MTC air-conditioning section reports that the core-memory stall normally runs at about 80°F or below. It warns that parity alarms occur if the magnetic cores get much above 90°F and instructs technicians to shut the machine down before the stated temperature limits are exceeded.

This is not a shelf-life result. It is a powered-service boundary:

```text
remanence without refresh
    != environment-independent correct access
```

Quantitative cross-machine margin history remains primarily Case 70 / computing-archaeology work.

## Historical record — anticipated shutdown captures both memory and context

When a shutdown can be anticipated, the MTC instructions tell the duty technician to dump core memory, probably to tape, and separately record the program counter plus other registers specified by the programmer.

That procedure exposes two retained-state classes:

```text
core payload
    -> copied to another representation

execution context
    -> PC + selected registers recorded separately
```

The procedure must not be misread. A pre-shutdown dump does **not** prove that ordinary power-off erases core. It occurs under an abnormal thermal condition and is compatible with prudent recovery insurance around uncertain shutdown/service conditions.

So:

```text
pre-shutdown copy
    != proof of volatile core
```

## Historical record — a program present in core still needs an entry path

The MTC panel-memory section says `Start Over` fetches its first instruction from panel-memory register 0. Programs usually begin in core memory, so panel-memory instructions commonly transfer control to the actual program's specified start address.

This is ordinary operation, not explicitly a power-recovery procedure. It nevertheless establishes a separate mechanism:

```text
program present in core
    != processor automatically enters it
```

That fact complements the shutdown procedure's separate recording of the program counter and selected registers.

## Engineering reconstruction

The period evidence supports four separable relations:

1. **medium retention** — does the material state remain without continuous power?
2. **transition integrity** — does movement between powered and unpowered states avoid unintended disturbance?
3. **operational qualification** — is the powered memory inside the environment/electrical margin required for correct access?
4. **restart-context availability** — are entry point and other state required for useful continuation available or reconstructable?

Therefore:

```text
medium retains
    != transition was safe
    != powered service is qualified
    != execution context survives
    != useful computation resumes
```

These four labels are project engineering reconstruction, not historical MTC/IRE terms.

The MTC procedures also make a power interval more precise than a binary on/off model:

```text
qualified operation
    -> capture useful state when possible
    -> ordered shutdown
    -> unpowered interval
    -> ordered energization
    -> explicit re-entry to program execution
```

This is a bounded model of the documented relations, not a claim that every MTC shutdown followed the same recoverable path.

## Functional analogy

Later persistent-memory, journal, SSD power-loss-protection, and distributed-recovery systems can be compared at one functional level:

```text
durable payload
    != durable complete machine state
```

No genealogy is claimed. Substrates, failure models and recovery protocols differ.

## Philosophical interpretation

The technical fact is that material endurance and system-level operational availability were already separable in period engineering vocabulary and practice.

A bounded interpretation is that persistence can depend on a **relation among retained payload, transition conditions, operating qualification and restart apparatus**, rather than on a durable substrate alone.

This interpretation is ours; it is not attributed to IRE or MTC engineers.

## Chronology and non-claims

This slice advances Case 02's open 1950s power-transition/restart-context debt by adding:

- a September 1956 professional terminology witness; and
- a named MIT/Lincoln MTC operational witness from 1957.

It moves this bounded evidence earlier than the existing IBM 7090 (1960–1962), IBM 1401 (1965), and PDP-7 (1966) witnesses.

It does **not** establish first use of `volatile` / `nonvolatile`, first core-memory power sequencing, invention priority, a Whirlwind-specific shutdown procedure, MTC→IBM/DEC genealogy, or arbitrary brownout behavior.

Still open are direct Whirlwind startup/shutdown primary evidence, pre-1956 terminology history, earlier transition circuits, uncontrolled partial-rail/brownout evidence, and machine-specific restart-software reconstruction.

Fresh searches in `tmzncty/computing-archaeology` for MTC power, the 1957 service manual, and the IRE nonvolatile-power-removal distinction found no dedicated packet to reuse.

## Result

```text
nonvolatile medium
    != system retention guarantee

quiescent remanence
    != safe transition
    != powered operating margin

core payload present
    != complete restart context

normal ordered shutdown
    != arbitrary outage

pre-shutdown dump
    != proof of core volatility

MTC 1957 procedure
    != universal magnetic-core contract
```

**Status:** Case 02 remains `grounded`. This is evidence deepening, not a maturity promotion.
