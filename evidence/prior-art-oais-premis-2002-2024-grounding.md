# Prior-art grounding — OAIS and PREMIS: bit survival, intelligibility, environment, and preservation evidence (2002–2024)

This evidence note deepens [`../docs/PRIOR_ART.md`](../docs/PRIOR_ART.md). It does **not** open a generic history of digital preservation.

**Bounded question:** which claims about long-term technical retention are already explicit in the OAIS and PREMIS traditions, and therefore cannot be presented as novel results of `technical-retention`?

The answer matters especially for the repository's access-apparatus and integrity syntheses. Digital-preservation work already states, in much more precise archival vocabulary, that retaining bits is not sufficient for retaining usable information, that interpretation depends on retained representation/context information, and that preservation actions and their outcomes can themselves be retained as evidence.

---

## Source A — OAIS original issue, January 2002

**Document:** Consultative Committee for Space Data Systems, *Reference Model for an Open Archival Information System (OAIS)*, CCSDS 650.0-B-1, Blue Book, Issue 1, January 2002.

**Preserved full scan:** <https://digital.library.unt.edu/ark:/67531/metadc123533/m2/1/high_res_d/650x0b1.pdf>

**Archival catalog record:** <https://digital.library.unt.edu/ark:/67531/metadc123533/>

**Evidence class:** `H/P*` — a period consensus technical recommendation preserved by the University of North Texas Libraries. The historical author is CCSDS/NASA, not UNT.

Useful anchors in the preserved scan:

- p. 2-1: OAIS says a major purpose of the model is to avoid confusion with simple `bit storage` functions and instead define a long-term information-preservation and access function;
- p. 3-3: the archive must determine a **Designated Community** so that it can judge whether preserved information, as represented, will remain understandable to that community; the text explicitly anticipates that the community definition may evolve;
- p. 5-6: a Transformation may change Content Information or PDI bits while attempting to preserve full information content, with corresponding changes in Representation Information;
- the 2002 text already uses **Representation Information** as a core part of the information model.

This is the main historical floor for the bounded prior-art claim. Later OAIS wording should not be projected backward where the revision history says a concept was added later.

---

## Source B — OAIS current issue, December 2024

**Document:** CCSDS, *Reference Model for an Open Archival Information System (OAIS)*, CCSDS 650.0-M-3, Recommended Practice, Issue 3, December 2024.

**Official publication record:** <https://ccsds.org/publications/allpubs/entry/3054/>

**Official PDF:** <https://ccsds.org/Pubs/650x0m3.pdf>

**Evidence class:** `H/P` — current primary standards body publication.

Document control on printed p. v records the genealogy relevant here: original issue `650.0-B-1` in January 2002, Issue 2 in June 2012, and current Issue 3 in December 2024. The same page says Issue 3 **introduced Preservation Objectives** to make `Independently Understandable` more consistently testable. Therefore:

```text
Designated Community / Representation Information in OAIS
    predates 2024

Preservation Objectives as an explicit OAIS concept
    = 2024 addition in Issue 3
```

The current model defines Long Term Preservation around information being **Independently Understandable by a Designated Community**, with evidence supporting Authenticity. The AIP must carry Representation Information adequate for that community plus PDI for the associated Content Data Object.

Current §4.3 also makes the interpretive dependency concrete: Representation Information can include structure, semantics, software, algorithms, encryption information, and written instructions. It can form a recursive representation network. The model says that preserving the meaning of an Information Object requires preserving its Representation Information as well.

This is a strong prior-art boundary for any claim that `bits survived but the information became unusable or unintelligible` is a novel discovery of this repository.

---

## Source C — PREMIS Version 1.0, May 2005

**Document:** PREMIS Working Group, *Data Dictionary for Preservation Metadata: Final Report of the PREMIS Working Group*, Version 1.0, May 2005.

**Official Library of Congress page:** <https://www.loc.gov/standards/premis/v1/>

**Official PDF:** <https://www.loc.gov/standards/premis/v1/premis-dd_1.0_2005_May.pdf>

**Evidence class:** `H/P` — period preservation-metadata specification hosted by the Library of Congress.

PREMIS defines preservation metadata as information a repository needs to support digital materials over the long term and organizes it around Objects, Events, Rights, Agents, and (in Version 1) Intellectual Entities.

Version 1 is also useful as a stop condition. Its scope discussion says detailed format-specific technical metadata is necessary for many preservation strategies but is left to format specialists, and it explicitly leaves detailed media/hardware description to specialists. That means PREMIS is prior art for **preservation metadata**, not a replacement for device- and mechanism-level engineering history.

The 2005 document therefore already blocks two overclaims:

- `preservation metadata = complete technical model of the storage apparatus`;
- `archival metadata standards already supply the device-level retention mechanism analysis this repository is trying to do`.

Both are false.

---

## Source D — PREMIS Version 3.0, June/November 2015

**Document:** PREMIS Editorial Committee, *PREMIS Data Dictionary for Preservation Metadata*, Version 3.0, 2015; the Library of Congress full document is marked updated November 2015.

**Official Library of Congress page:** <https://www.loc.gov/standards/premis/v3/index.html>

**Official PDF:** <https://www.loc.gov/standards/premis/v3/premis-3-0-final.pdf>

**Evidence class:** `H/P` — primary preservation-metadata specification.

Two parts are especially relevant.

### Fixity and retained preservation-event evidence

PREMIS 3.0 semantic unit `1.5.2 fixity` is information used to verify whether a file/bitstream has been altered in an undocumented or unauthorized way. A prior message digest is compared with a later digest. The **act** of performing the fixity check and its date are recorded as an Event, while the check result is recorded as `eventOutcome`.

The Event model separately defines `eventOutcomeInformation`, and `eventOutcome` can categorize success, partial success, or failure. PREMIS explicitly notes that a failed fixity check can become an actionable and permanent Event record.

This yields a useful prior-art distinction:

```text
retained object bits
    !=
retained fixity reference
    !=
fixity-check execution
    !=
retained outcome of that check
```

But PREMIS fixity does **not** by itself establish semantics, authenticity in every sense, current logical authority, or future renderability.

### Environment dependencies

PREMIS 3.0's special topic on **Environment** states that application software, operating systems, computing resources, and even network connectivity can be interposed between user and digital content, and that separating content from environmental context can make it unusable.

Version 3.0 changed how those dependencies are modeled. The document explicitly says that before 3.0 there was an `environment` container within an Object; in 3.0, an environment may instead be described as an Object in its own right and linked by dependency relations. Examples include a physical floppy-drive instance and a software driver. Environment representations can themselves be retained independently.

Therefore the useful historical statement is not `PREMIS always modeled environment objects this way`. The safe statement is:

```text
PREMIS before 3.0 already modeled environment information,
while PREMIS 3.0 changed the model so environments could be described as Objects
and connected through dependency relations.
```

---

## Historical record — what this prior art already establishes

### H1. `Bit storage != long-term information preservation` was explicit by 2002

OAIS 2002 directly distinguishes its long-term information-preservation/access problem from simple bit-storage functions. `technical-retention` therefore must not claim this general distinction as novel.

### H2. Interpretability was already modeled as relational

OAIS ties the required amount of Representation Information to a Designated Community and its Knowledge Base. The archive's problem is not merely whether a bitstream physically exists but whether the preserved information remains understandable to the community for which preservation responsibility is being discharged.

### H3. Information continuity can survive controlled bit changes

OAIS migration/Transformation vocabulary explicitly permits changes to bit-level representation while the archive attempts to preserve the information content. This is prior art for the broad proposition:

```text
same information retained
    does not require
same bit pattern retained forever
```

This does not mean every transformation preserves all properties or that OAIS supplies a universal identity criterion.

### H4. Preservation evidence can itself be retained state

PREMIS formalizes fixity references, preservation Events, dates, agents, and outcomes. A repository can therefore retain evidence **about preservation work** separately from the content object.

### H5. Technical environment is part of the preservation problem

PREMIS 3.0 explicitly treats software/hardware/runtime/network dependencies as preservation-relevant environmental context. This is strong prior art against any novelty claim that `a file can survive while its access environment disappears` was first noticed here.

---

## Engineering reconstruction — what remains useful for this repository

OAIS and PREMIS operate at a different level from most cases in `technical-retention`. They tell an archive what information, dependencies, evidence, and responsibilities may need to survive. They generally do **not** tell us, for example, how a NAND BBT chooses a current copy, how DRAM refresh counters are reconstituted, how an SSD maps logical blocks, or how a distributed store qualifies a replica.

That gives a clean division:

```text
OAIS / PREMIS
    archival information model + preservation responsibility + metadata/evidence

technical-retention cases
    exact physical/logical/protocol mechanisms that make retained relations survive
```

The layers interact but are not interchangeable.

A file's PREMIS environment metadata may accurately say that a particular runtime, driver, or device is required. That metadata is not itself the runtime, driver, or device. Likewise, OAIS Representation Information can describe how a Data Object maps into meaningful concepts without being identical to one concrete reader apparatus.

The following counterexamples should therefore remain explicit:

- `bit survival != intelligibility`;
- `fixity evidence != intelligibility`;
- `fixity evidence != complete authenticity proof`;
- `preservation metadata != preservation mechanism`;
- `documented dependency != available dependency`;
- `Representation Information != one concrete reader apparatus`;
- `environment description != executable environment`;
- `Designated Community relative understandability != timeless universal meaning`.

---

## Functional comparison with existing syntheses — bounded only

### Synthesis 23 — access apparatus / compatibility

[`../docs/SYNTHESIS_23_RETENTION_INTERPRETER_ACCESS_APPARATUS.md`](../docs/SYNTHESIS_23_RETENTION_INTERPRETER_ACCESS_APPARATUS.md) separates material embodiment, restart legibility, software-format interpretation, physical reader capability, controller admission, and operation-specific service.

OAIS/PREMIS are strong **prior art around the representation/environment side** of that problem. The synthesis remains useful only if it continues below that archival abstraction and asks mechanism-specific questions such as:

- which exact hardware or software relation is missing;
- whether the surviving representation is current/admissible;
- whether the medium is still readable;
- whether the controller accepts it;
- whether read and write compatibility differ;
- whether migration or reconstruction can restore the relation.

The safe comparison is:

```text
OAIS Representation Information / PREMIS environment dependency
    overlaps functionally with
technical-retention's interpretation/access-apparatus questions

but

archival information model != device/protocol mechanism taxonomy
```

No genealogy is asserted from OAIS/PREMIS to the repository's hardware/distributed classifications.

### Integrity and maintenance syntheses

PREMIS fixity/Event semantics also bound Syntheses 08 and 22: preserving a digest, performing a check, recording the outcome, repairing an object, and later verifying the repair are distinct actions/relations. The repository's contribution, if any, is not the generic idea of keeping checksums or audit events. It is the cross-mechanism decomposition of what those signals can and cannot authorize at lower technical layers.

---

## Philosophical interpretation — deliberately narrow

OAIS's Designated Community makes one philosophical point technically concrete: preservation is not exhausted by substrate continuity. Availability of a meaningful record can depend on a changing relation among data, representation knowledge, software/hardware environment, and a community's assumed knowledge.

That observation should discipline philosophical work, not replace it. In particular:

- a Designated Community is an archival responsibility construct, not a universal theory of meaning;
- Representation Information is not automatically Stieglerian tertiary retention;
- PREMIS metadata is not `memory of memory` simply because it records preservation Events;
- environment dependencies do not imply that all technical being is reducible to access.

---

## Revised novelty boundary

This bounded review changes the repository's novelty claim in a concrete way.

`technical-retention` should **not** present any of the following as novel:

- bits can survive while information becomes unusable;
- format/semantic/context information may need to be preserved;
- software/hardware environments can be preservation dependencies;
- integrity/fixity checks need retained reference information;
- preservation actions and outcomes can themselves be recorded;
- migration can preserve information while changing its representation.

The narrower contribution opportunity is:

> **Trace these archival-level requirements downward into exact physical, controller, filesystem, protocol, and distributed mechanisms, and compare which retained relations—embodiment, currentness, integrity evidence, mapping, interpreter, environment, authority, repair state, and migration state—must survive or be reconstituted for a future operation to recover what the higher layer calls preserved information.**

That is materially narrower than `digital preservation already knows that context matters`, and it avoids competing with OAIS/PREMIS on territory they already occupy.

---

## Related-repository boundary

A fresh search found no dedicated OAIS/PREMIS study in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology). That repository should remain the home for device/history details if a preservation case depends on obsolete hardware or interface genealogy.

[`tmzncty/old-web-archaeology`](https://github.com/tmzncty/old-web-archaeology) is the more direct companion for concrete historical web-preservation cases. Its scope already distinguishes archived captures, screenshots, browser assumptions, missing resources, and later reconstructions. `technical-retention` should cite those cases when it needs evidence about browser/runtime/environment dependence rather than duplicating old-web capture and reconstruction work.

---

## Readiness assessment

This closes only a **bounded OAIS/PREMIS prior-art mapping**:

- original OAIS issue and its bit-storage / Designated-Community / Representation-Information boundary;
- current OAIS revision control and the 2024 addition of Preservation Objectives;
- PREMIS preservation-metadata scope;
- PREMIS fixity/Event separation;
- PREMIS 3.0 environment-dependency modeling;
- the resulting novelty restriction for `technical-retention`.

Still open are a broader digital-preservation genealogy (RLG/OCLC 1996, emulation/migration debates, LOCKSS, NDSA Levels, significant-properties literature, format registries, authenticity/trust standards, ISO 16363, and born-digital preservation practice). Those should be pursued only when they change a concrete project claim rather than as a generic literature survey.