# Controlled Vocabulary

This glossary is not a dictionary of universal meanings. It defines **working terms for this repository** so that cases from abaci to distributed storage can be compared without silently changing the question.

Terms should be revised when cases expose a bad distinction.

## retained state

A distinguishable configuration that remains available beyond the event that produced it and can matter to a later operation, interpretation, or decision.

A retained state may be:

- physical;
- logical;
- symbolic;
- replicated;
- reconstructed;
- human-readable;
- machine-readable;
- or both.

The term does **not** imply long duration.

## retention

The set of conditions by which a state remains recoverable or actionable across time.

Retention may depend on:

- passive physical stability;
- continuous power;
- refresh;
- recirculation;
- remanence;
- charge trapping;
- error correction;
- remapping;
- replication;
- migration;
- human or institutional procedure.

## working retention

Short- or medium-lived retention whose primary purpose is to preserve an operational state for later steps in an ongoing activity.

Examples may include:

- an abacus configuration between arithmetic steps;
- a CPU register;
- a stack frame;
- a buffer.

This term does not imply archival durability.

## archival retention

Retention whose purpose is to preserve a record across long intervals and usually across changes of operator, session, device, or institution.

Archival retention often requires preservation of metadata, format knowledge, software, keys, and institutional responsibility in addition to the carrier itself.

## substrate

The physical or logical system in which distinctions are embodied.

Examples:

- bead position;
- gear angle;
- relay state;
- capacitor charge;
- magnetic orientation;
- trapped charge;
- block mapping;
- replicated log entry.

`Substrate` should not be assumed to mean one fixed physical location.

## persistence

A user- or system-level property in which an identity or value continues to be treated as present over time.

Use carefully. Persistence may be an **emergent effect** of refresh, rewrite, repair, remapping, or migration rather than passive durability of one carrier.

## volatility

Dependence of retained state on continuing conditions such as power, refresh, circulation, or active control.

`Volatile` and `nonvolatile` are not complete descriptions of maintenance requirements.

## addressability

The operational ability to **designate and select / resolve toward a particular retained state or region from a larger set**.

Addressability is an umbrella term, not a claim that every system has a numeric machine address. Selection may be:

- human-mediated spatial selection;
- sequential or temporal selection;
- coordinate-decoded;
- indexed;
- associative;
- content-addressed;
- logical-to-physical translated;
- algorithmically or distributively resolved.

The grounded addressability audit requires several distinctions:

1. **designation** — what identity, place, key, row, block, object, or procedural position is requested;
2. **selection / resolution** — how that designation is turned into one or more candidate physical embodiments;
3. **currentness / admissibility** — where required, which candidate is allowed to count as the current state;
4. **read / recovery / interpretation** — how the selected state becomes usable.

Do not collapse these steps. In particular:

- retention does not require an autonomous machine-readable address;
- an address is not necessarily a physical location;
- stable logical designation does not imply stable physical location;
- resolving a candidate copy does not prove that it is current;
- addressability is not identical to availability.

See [`SYNTHESIS_AUDIT_03_ADDRESSABILITY.md`](SYNTHESIS_AUDIT_03_ADDRESSABILITY.md).

## access geometry

The constraints that determine how retained states can be reached.

Examples:

- a rod or column on an abacus;
- a recurring time slot in a delay line;
- a track/sector on disk;
- a row/column in DRAM;
- a logical block translated through an FTL;
- an object key resolved through distributed metadata.

## read semantics

What happens to retained state when it is read.

Possible categories:

- nondestructive read;
- destructive read followed by rewrite;
- read-disturb risk;
- reconstruction from redundant state;
- interpretation that requires an external human procedure.

## write semantics

The mechanism and constraints by which a retained state is created or changed.

A write may require:

- direct repositioning;
- switching;
- charging;
- magnetization;
- erase-before-write;
- copy-on-write;
- append-only logging;
- quorum agreement.

## refresh

Periodic restoration required because the physical state would otherwise decay or become unreliable.

Refresh is not merely maintenance performed after failure. In some systems it is **constitutive of ordinary persistence**.

## remanence

Persistence of a physical distinction after the external stimulus that created it is removed.

Magnetic core and magnetic recording are major cases, but the concept should not be generalized beyond appropriate physical mechanisms.

## destructive read

A read operation that disturbs or destroys the stored physical state and therefore requires restoration if the logical value is to remain retained.

## remapping

Maintenance of logical identity while the physical location that embodies that identity changes.

Examples include bad-sector replacement and Flash address-translation systems.

Remapping is central to the distinction between **identity persistence** and **location persistence**.

Grounded Case 04 adds an important refinement: remapping metadata may itself be part of the retained state needed to decide which physical embodiment currently counts.

## Flash Translation Layer (FTL)

A historical and technical term that must be dated rather than projected backward automatically.

For this repository, Intel Application Note AP-619 (August 1995) is a directly inspected primary terminology anchor: Intel reported that a sector-oriented Flash-media format had been approved by PCMCIA as the **Flash Translation Layer (FTL)** format. The same document describes FTL as remapping host-style block writes to free Flash areas, invalidating old areas, recording physical placement, and presenting logical-to-physical virtual block semantics.

Use `FTL` freely for sources and systems that use or clearly inherit the term. For earlier systems such as Ban's 1993-filed `Flash file system` patent, preserve the source's own vocabulary (`virtual map`, `logical unit`, `physical address`, `transfer unit`) unless making an explicitly labeled later functional comparison.

The current evidence establishes `FTL` **no later than 1995** in this PCMCIA/Intel context. It does not establish first coinage.

## logical invalidation

A change in metadata or allocation state by which a physical embodiment ceases to count as the current logical object, even though the underlying physical region has not necessarily been erased or destroyed.

In the bounded 1993 M-Systems Flash case, a block can be marked `deleted and not writable` while the containing erase unit remains physically unerased until later reclamation. Wells's 1992-lineage Intel work similarly describes replaced physical sectors becoming `dirty` before later block clean-up.

Do not assume that logical invalidation implies forensic recoverability. It establishes a semantic/architectural distinction from physical erasure, not a universal recovery result.

## physical erasure

A medium-specific operation that materially resets or destroys a previously retained physical state.

Examples include:

- electrically erasing a Flash erase unit;
- degaussing or overwriting magnetic media, depending on the bounded mechanism;
- physically destroying a carrier.

Physical erasure must be kept separate from:

- file deletion;
- unlinking;
- address deallocation;
- controller invalidation;
- key destruction;
- policy expiration.

Those operations may make data unavailable without performing the same physical transformation.

## reclamation

Maintenance that recovers storage capacity previously occupied by obsolete / invalid state while preserving state that still counts as current.

A reclamation cycle may include:

1. identifying a region containing a mixture of current and obsolete state;
2. copying or reconstructing the current state elsewhere;
3. erasing / freeing the old region;
4. updating identity or allocation metadata.

The term is broader than any one implementation's `garbage collection` or `clean-up` algorithm. Do not use these as automatic historical synonyms.

Grounded Flash evidence makes an additional rule necessary:

> **reclamation is not automatically wear leveling.**

A reclaim operation can be selected simply because a region contains enough obsolete state to make erasure worthwhile. A wear-leveling policy introduces an additional lifetime objective based on how much erase/program/switching burden regions have already received.

## wear leveling

A placement or reclamation policy whose objective is to distribute finite program/erase/switching burden across a Flash medium so that a frequently updated workload does not consume some regions' usable life much earlier than others.

The repository's early primary anchor is Steven E. Wells / Intel, `Method for wear leveling in a flash EEPROM memory`, with application lineage to 30 October 1992. That source explicitly distinguishes ordinary `cleaning up a block` from choosing clean-up work using both invalid-sector count and accumulated switching operations.

Therefore:

- **reclamation** answers a capacity question: which obsolete physical state should be erased so writable space returns?
- **wear leveling** answers a lifetime-distribution question: where should writes/erases be placed so physical wear is not pathologically concentrated?

One operation may serve both purposes, but the concepts are not identical.

## migration

Transfer of retained state to a new carrier, format, system, or infrastructure while preserving some agreed identity or meaning.

Long-term digital preservation is often a migration regime rather than preservation of one eternal medium.

## state retention

Preservation of a current configuration or value.

## history retention

Preservation of the sequence of earlier states or operations that produced a current state.

These are separate. A system may strongly retain current state while retaining no history at all.

## maintenance

The continuing work that makes a retained state remain usable.

Maintenance may be performed by:

- users;
- hardware;
- firmware;
- software;
- operators;
- repair systems;
- facilities;
- preservation institutions.

Maintenance triggers can differ. Current cases expose at least:

- continuous maintenance (delay-line circulation);
- access-triggered restoration (classic destructive-read core);
- deadline-driven scheduled maintenance (DRAM refresh);
- capacity/reclaim-triggered maintenance (mapped Flash);
- wear/lifetime-driven placement or reclamation (mapped Flash / early wear-leveling evidence);
- failure/repair-triggered maintenance (RADOS; bounded later NAND block replacement).

These categories remain provisional until more cases test them.

## technical forgetting

A **layer-specific loss of recoverability, currentness, identity, interpretation, or serviceability through an identifiable mechanism**.

After [`SYNTHESIS_AUDIT_05_TECHNICAL_FORGETTING.md`](SYNTHESIS_AUDIT_05_TECHNICAL_FORGETTING.md), do not use `forgotten` as a synonym for any one of `physically destroyed`, `deleted`, `stale`, `unavailable`, or `unreachable`.

A technical-forgetting claim should identify at least:

1. **target layer** — physical distinction, logical value/identity, relation/currentness, serviceability, history, or durable threshold;
2. **mechanism** — disturbance/destruction, missed maintenance, logical invalidation/deauthorization, relation/metadata loss, or failed reconstruction;
3. **masking condition** — whether another current embodiment or reconstruction path preserves the higher-level state;
4. **recoverability boundary** — temporary unavailability, stale/obsolete residue, logical deletion, or actual loss of recoverable current state.

Grounded examples include:

- moved/reset positional state;
- destructive core read without required rewrite;
- DRAM charge decay after a missed refresh obligation;
- Flash logical invalidation before later physical erasure;
- loss of Flash mapping/allocation relations needed to identify the current embodiment;
- RADOS stale/deauthorized replicas versus actual loss of recoverable current state;
- failed reconstruction after redundancy has degraded.

Important counterexamples:

- **physical loss does not always imply logical forgetting** — DRAM reconstruction, Flash relocation/reclamation, and RADOS replica replacement can preserve a higher-layer state;
- **physical survival does not always imply retained current state** — a positional configuration can lose interpretive context, and Flash/RADOS can retain stale or invalid embodiments;
- **unavailability is not automatically forgetting** — a state can be temporarily unreachable or not yet admissible and later return to service.

Candidate mechanisms not yet covered by the five-case bounded audit include key destruction, bit rot, media/format obsolescence, controller-wide failure, and institutional abandonment. Keep them as open research categories rather than treating the current taxonomy as complete.

## availability

The condition in which retained state can actually be called upon for use **now**.

Availability is broader than addressability. A state can be correctly designated and resolved yet still be unavailable because:

- the selected embodiment is stale or not authorized to answer;
- readout fails;
- reconstruction fails;
- a required key, interface, software layer, or interpretation is missing;
- the physical carrier or service is unreachable.

Conversely, a physical trace may survive while no designation or resolver remains to select it as the intended state.

Do not equate this working technical term with Heidegger's `Bestand`.

## functional analogy

A comparison between mechanisms based on a limited shared operation or role.

Example:

> An abacus configuration can be `register-like` because it can preserve an operational value between steps.

A functional analogy does **not** establish:

- shared historical vocabulary;
- direct technological descent;
- equivalent architecture;
- equivalent social meaning;
- identical philosophy.

## historical record

A claim grounded in surviving documents, artifacts, manuals, patents, standards, archival evidence, or scholarship about what existed, was said, or was done.

## engineering reconstruction

A reasoned claim about mechanism or constraint derived from technical evidence. It may be strong without being a historical actor's explicit explanation.

## philosophical interpretation

A conceptual reading that uses a technical case to test or sharpen questions about memory, temporality, technics, availability, inscription, identity, or forgetting.

It must not be silently presented as historical fact.
