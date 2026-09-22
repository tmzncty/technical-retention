# Evidence deepening — Case 04: Samsung NAND Copy-Back integrity boundary (2004–2010)

## Status

**`bounded deepening complete`** for the raw-NAND Copy-Back / integrity boundary described here.

This packet deepens [`../cases/04-flash-virtual-mapping-logical-identity.md`](../cases/04-flash-virtual-mapping-logical-identity.md). It does not turn a NAND device primitive into an FTL protocol, and it does not claim that the Samsung parts below define every historical or later Copy-Back implementation.

## Research question

Case 04 already establishes that logical identity can survive deliberate physical relocation when mapping/allocation state says which embodiment currently counts. The narrower question here is:

> When NAND provides an internal page Copy-Back path, does successful relocation/program completion by itself prove that the relocated logical payload has been revalidated?

For the bounded Samsung record, the answer is **no**.

The strongest compact result is:

```text
copy-back / program completion
    !=
source payload revalidated

logical identity preserved through relocation
    !=
latent error debt eliminated

physical relocation succeeded
    !=
integrity qualification succeeded
```

A later Samsung generation makes the separation especially explicit by exposing a controller-visible read/check/correct path before Copy-Back programming.

---

## Source set and provenance

### S1 — Samsung K9F1208U0B family, 64M × 8 NAND Flash

Manufacturer datasheet, Samsung Electronics, revision line beginning with initial issue **24 April 2004**. The inspected revision history records:

- `0.0` — initial issue, 24 April 2004;
- `0.1` — 11 October 2004;
- `0.2` — 22 April 2005;
- `0.3` — 6 May 2005.

The later revision text documents Copy-Back and warns that a source-page bit error caused by charge loss can be propagated and accumulated by repeated Copy-Back. It recommends two-bit ECC for Copy-Back use.

Archived manufacturer-datasheet mirror:

- <https://datasheet.octopart.com/K9F1208U0B-JIB0-Samsung-datasheet-11807018.pdf>

A searchable transcription of the same Samsung family is also available at:

- <https://www.scribd.com/document/881778286/K9F1208U0B-64M>

The mirror is not treated as a new secondary authority: the evidence is the Samsung manufacturer datasheet carried by the archive.

### S2 — Samsung K9GAG08U0E / K9LBG08U0E / K9HCG08U1E, 16 Gb E-die NAND Flash

Samsung Electronics manufacturer datasheet, **Final Rev. 0.9.1**, 2010. Its revision history records the initial issue on 12 June 2009 and the final-revision line in March 2010.

Section `5.4 Copy-back Program` documents a later workflow in which:

1. `Read for Copy-Back` moves the source page into the device's internal data buffer;
2. sequential data output lets the controller check for a bit error;
3. if no error is present, reloading is unnecessary;
4. if correction/modification is required, data can be supplied before the destination program;
5. destination programming has its own completion/pass-fail status.

Archived Samsung-datasheet transcription / mirror:

- <https://files.elektroda.pl/859743,k9gag08u0e.html>
- <https://www.alldatasheet.net/html-pdf/1134995/SAMSUNG/K9GAG08U0E/16185/46/K9GAG08U0E.html>

Again, the evidence class is manufacturer primary documentation, with the archive only supplying access.

---

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Samsung's K9F1208U0B-family documentation exposes Copy-Back as a device operation | H/P | direct manufacturer datasheet |
| The earlier Samsung datasheet warns that a source charge-loss bit error may be copied and accumulated across repeated Copy-Back | H/P | direct manufacturer warning |
| The earlier datasheet recommends two-bit ECC for Copy-Back | H/P | direct manufacturer recommendation |
| Samsung's 2010 K9GAG08U0E-family documentation exposes `Read for Copy-Back` and `Copy-Back Program` as distinct command steps | H/P | direct manufacturer datasheet |
| The 2010 procedure allows source data to be sequentially output so the controller can check bit errors before destination programming | H/P | direct manufacturer procedure |
| Copy-Back program completion/pass status is a distinct observation from the preceding payload-error check | H/P/E | direct sequence + bounded reconstruction |
| Program success by itself proves the source payload was logically correct | X | contradicted by the documented error-propagation/check distinction |
| Raw NAND Copy-Back is itself an FTL mapping-publication protocol | X | category error |
| Every NAND Copy-Back implementation bypasses ECC | X | unsupported universalization |
| Samsung invented Copy-Back in 2004 | X | not investigated / not claimed |
| The 2010 implementation is internally identical to the 2004/2005 implementation | X | not established |

---

## Historical record

### H/P — the 2004–2005 Samsung family documents Copy-Back as an internal relocation fast path

The K9F1208U0B-family documentation presents Copy-Back as a page-movement operation that avoids the ordinary host-side reload path. The source page is read into internal device storage and then used for programming a destination page, subject to device-specific address / plane restrictions.

The historical fact needed here is narrow:

```text
raw NAND already exposes
an internal source-page -> destination-page relocation primitive
```

That is not yet an FTL. It is a device command surface that a higher layer may use while implementing reclaim, block replacement, wear management, or another relocation policy.

### H/P — the same documentation warns that relocation can preserve an error

The crucial reliability note says that even when the Copy-Back operation itself reports its program status, a **source page bit error caused by charge loss** can be carried into the copied page. Repeated Copy-Back can therefore accumulate such errors. Samsung recommends two-bit ECC for the operation.

The important historical distinction is consequently already explicit in the vendor record:

```text
copy operation status
    !=
source-data correctness
```

This is not a hypothetical failure invented by later reconstruction. The manufacturer itself warns about error propagation through the relocation path.

### H/P — the 2010 Samsung family makes checking visible in the command sequence

The 2010 K9GAG08U0E-family datasheet describes `Read for Copy-Back` as loading the whole source page into an internal data buffer. It then says the data can be output sequentially so a bit error can be checked.

If there is no bit error, the controller does not need to reload the page before issuing the Copy-Back program sequence. The datasheet also permits data modification through the data-input command before destination programming.

Thus the later bounded procedure exposes three conceptually different moments:

```text
source page acquired
    ->
source payload checked / optionally corrected
    ->
destination page programmed
```

The final program operation has its own ready/status/pass-fail observation.

That status does not retroactively collapse the preceding source-validation step.

### H/P — repeated relocation is conditional on an integrity workflow, not merely on program success

The later datasheet states that the Copy-Back sequence can be repeated without a fixed repetition count in the documented workflow. Read together with the immediately preceding bit-error-check language, the useful bounded conclusion is not “repetition is always safe.” It is:

> the vendor's later workflow treats repeated Copy-Back as compatible with an explicit opportunity to inspect and correct the data carried forward.

This packet does **not** infer an unlimited retention lifetime or unlimited error budget from the absence of a command-count limit.

---

## Engineering reconstruction

### E — Copy-Back moves an embodiment; it does not automatically certify the meaning of that embodiment

For Case 04 the relocation can be represented as:

```text
source physical page
    ↓
read into NAND internal register / buffer
    ↓
[optional / required-by-policy integrity observation and correction]
    ↓
destination program
    ↓
program completion / status
```

The brackets are deliberate. The exact check/correction requirement depends on the device generation and controller policy. What the sources establish is that the integrity layer and program-status layer are **not the same evidence**.

### E — A successful destination program can faithfully reproduce the wrong source bits

If charge loss has already changed the source representation, an internal copy mechanism may transfer that changed representation successfully. In that case the destination program can satisfy its own device-level success criterion while still carrying a payload that should have been corrected by a higher integrity mechanism.

Therefore:

```text
destination media successfully programmed
    !=
intended logical payload re-established
```

This is exactly why the earlier Samsung note can simultaneously discuss successful Copy-Back mechanics and accumulated bit-error risk.

### E — Relocation currentness has at least two independent predicates

A higher-level mapped-storage system needs more than “some new page was programmed.” At minimum it must establish both:

```text
placement / identity predicate:
    this destination is the embodiment that should now count

integrity predicate:
    this destination represents an acceptable version of the intended payload
```

Case 04's existing mapping evidence primarily grounds the first predicate. This packet deepens the second.

A useful bounded formula is:

```text
current logical object
    =
currentness authority / mapping
    +
qualified payload embodiment
```

The plus sign is conceptual, not an implementation claim about one metadata structure.

### E — Device primitive and FTL publication must remain separate

Samsung's raw-NAND datasheets establish a physical-page relocation mechanism. They do **not** establish when an FTL should publish a new logical-to-physical mapping, when it should invalidate the old page, or what crash-consistency protocol surrounds that publication.

Accordingly, the safe layered reconstruction is:

```text
raw NAND Copy-Back
    provides a relocation primitive

FTL / controller policy
    may decide why to relocate
    may validate / correct data
    may publish a new mapping
    may retire the old location
```

No ordering among those higher-level publication steps is attributed to these Samsung device datasheets unless separately sourced.

### E — Integrity debt can survive physical movement

This case adds a useful form of maintenance debt:

```text
old physical location retired
    !=
old uncertainty retired
```

If a latent source error is copied without correction, physical placement has changed while the integrity problem persists—and may worsen under repeated copying.

Thus relocation can move **error debt** as well as payload state.

---

## Relation to the rest of Case 04

Case 04 already has four historical/engineering layers:

1. late-1980s NAND device geometry;
2. 1993-filed virtual/physical mapping and relocation semantics;
3. 1995–1996 FTL terminology / standardization chronology;
4. 2008–2014 FTL power-loss recovery and reconstructed mapping authority.

This packet adds a fifth layer:

5. **raw-NAND relocation can complete while integrity qualification remains a separate obligation.**

The combined model is now:

```text
logical address / object
    ↓
current mapping authority
    ↓
physical source page
    ↓
relocation primitive
    ↓
integrity observation / correction
    ↓
physical destination page
    ↓
(mapping publication / retirement policy at a higher layer)
```

The parenthesized final step is intentionally not sourced from the Samsung device documents. It remains part of the controller/FTL layer.

---

## Functional analogies — structural only

### A — distributed repair / representation conversion

There is a controlled structural analogy to distributed-storage repair and redundancy-mode conversion:

```text
new embodiment produced
    !=
new embodiment validated as current / acceptable
```

This is useful for cross-case comparison, but no common implementation lineage is claimed.

### A — Case 85 read-retry

Case 85 separates media condition from reader configuration and retry state. This Copy-Back slice adds another separation: the device may perform a successful physical relocation while payload integrity still depends on independent observation/correction.

The shared abstraction is only:

```text
operation success at one layer
    !=
truth / acceptability established at every higher layer
```

No genealogy is implied.

---

## Philosophical / media-theoretical interpretation

### I — persistence can preserve an error as faithfully as it preserves intended data

A downstream interpretation, not manufacturer language, is that persistence is neutral with respect to correctness. A mechanism that faithfully carries a representation forward can also carry forward accumulated corruption.

That makes “continued existence” weaker than “continued identity under the system's correctness rules.”

### I — relocation does not automatically renew the retained object

Moving a representation to fresh physical cells may renew its **placement** without renewing its **epistemic status**. Qualification—ECC, validation, or another integrity check—answers a different question from location.

These interpretations remain downstream of the engineering record and should not be attributed to Samsung.

---

## Explicit non-claims

This packet does **not** claim that:

- Samsung invented NAND Copy-Back;
- April 2004 is the first use or first commercial shipment of Copy-Back;
- all NAND devices implement Copy-Back;
- all Copy-Back implementations bypass ECC;
- every controller uses the exact 2010 check/correct sequence;
- a successful NAND program proves logical payload correctness;
- the 2004/2005 and 2010 products share an identical internal datapath;
- the internal data buffer's circuit implementation is known from these documents;
- Copy-Back is itself an FTL mapping algorithm;
- a device-level program-status bit proves that mapping publication is crash-safe;
- the Samsung sources establish mapping-publication ordering, old-page retirement ordering, or power-fail atomicity;
- the structural analogies to distributed repair or other repository cases establish genealogy.

---

## Remaining evidence debt

This slice closes the narrow question “can Copy-Back program success be equated with source-payload revalidation?” for the bounded Samsung record. It leaves several stronger questions open:

1. **Power interruption during Copy-Back** — obtain named-device documentation or fault-injection evidence for reset / power-loss boundaries between source read, internal-buffer residence, destination program, and status reporting.
2. **FTL publication ordering** — find a controller / firmware / patent source that explicitly orders Copy-Back destination validation, logical-map publication, source invalidation, and later erase.
3. **On-die ECC generations** — establish how later NAND with internal ECC changes the boundary between device-internal relocation and controller-visible correction.
4. **Telemetry** — find named products exposing corrected-bit counts, ECC margin, relocation counters, or other evidence that a controller can use before retiring an old embodiment.
5. **Fault injection** — seek an implementation paper or controller test where a corrupted source page is deliberately relocated and the destination/current mapping is checked.
6. **Historical genealogy** — if the broader origin and vendor lineage of Copy-Back is pursued, route that product/command history primarily through `tmzncty/computing-archaeology` rather than rebuilding it here.

---

## Related repository routing

A fresh search of `tmzncty/computing-archaeology` for `copyback` / `copy-back` did not expose a dedicated packet that can be reused in this pass.

That absence should not turn this repository into a full NAND-command history. `technical-retention` keeps only the retention-specific result:

> relocation completion and integrity qualification are distinct evidence classes.

A broader Copy-Back chronology, vendor comparison, command genealogy, controller adoption history, or die-level implementation lineage belongs in `computing-archaeology` if built later.
