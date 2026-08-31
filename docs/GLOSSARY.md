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

The ability to select a particular retained state or region from a larger set.

Addressability may be:

- spatial;
- sequential;
- temporal;
- indexed;
- associative;
- content-addressed;
- logical rather than physical.

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

Examples include bad-sector replacement and Flash Translation Layers.

Remapping is central to the distinction between **identity persistence** and **location persistence**.

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

## technical forgetting

Loss, invalidation, or inaccessibility of retained state through a specific mechanism.

Do not use `forgetting` without identifying the mechanism where possible.

Candidate mechanisms include:

- decay;
- power loss;
- refresh failure;
- overwrite;
- erase;
- logical deletion;
- garbage collection;
- index loss;
- metadata loss;
- key destruction;
- corruption;
- bit rot;
- controller failure;
- format obsolescence;
- institutional abandonment.

## availability

The condition in which retained state can actually be called upon for use.

A state may physically survive while becoming unavailable because its index, key, interface, software, interpretation, or institutional context has been lost.

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
