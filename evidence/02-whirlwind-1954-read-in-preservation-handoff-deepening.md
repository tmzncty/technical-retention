# Case 02 — Whirlwind 1954 read-in preservation / execution-handoff boundary

## Scope

This bounded deepening asks a narrower question than power-off retention:

> When Whirlwind I entered its normal `read-in` path and was about to replace the program resident in magnetic-core memory, what happened to the existing core image first?

Primary MIT Digital Computer Laboratory material from 1954 gives a concrete answer. The normal read-in path first copied the current magnetic-core-memory contents to auxiliary drum group 0, then loaded a utility / drum-input program from protected drum storage into core memory, and only then transferred control to that newly loaded program.

The result is deliberately narrow:

```text
active core payload present
    -> preserve current core image elsewhere
    -> repurpose core with bootstrap / utility program
    -> transfer execution control

preservation before overwrite
    != proof of power-failure recovery
    != proof of complete execution-context recovery
```

Case 02 remains `grounded`.

## Sources

Primary Whirlwind documents:

- Project Whirlwind, *Summary Report No. 38: Second Quarter 1954*, MIT Digital Computer Laboratory, especially printed p. 9:
  <https://archive.decromancer.ca/bitsavers.org/pdf/mit/whirlwind/Project_Whirlwind_Summary_Report_No_38_Second_Quarter_1954.pdf>
- Charles W. Adams, *The MIT Systems of Automatic Coding*, Report R-233, May 1954, especially p. 18:
  <https://www.bitsavers.org/pdf/mit/whirlwind/R-series/R-233_The_MIT_Systems_of_Automatic_Coding_May54.pdf>
- Philip R. Bagley, *Programming for In-Out Units*, Memorandum M-1623-2, originally 17 September 1952 and revised September 1954 by H. H. Denman, especially p. 10:
  <https://bitsavers.org/pdf/mit/whirlwind/M-series/M-1623-2_Programming_for_In-Out_Units_Sep54.pdf>
- *Whirlwind Programming Manual*, 2M-0277, October 1958, especially p. 28:
  <https://bitsavers.org/pdf/mit/whirlwind/M-series/2M-0277_Whirlwind_Programming_Manual_Oct58.pdf>

Related-repository division of labor:

- `tmzncty/computing-archaeology`, *Why Was Magnetic-Core Memory Worth Weaving by Hand?*:
  <https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md>

That archaeology chapter already covers core selection, destructive read / restoration, labor, and the broad nonvolatility warning. This packet therefore does **not** repeat the general history of Whirlwind core memory. It isolates a retention-specific software / storage handoff.

## Historical record — normal read-in preserves the current core image before replacement

*Summary Report No. 38* describes the utility-control path used in routine operation. It states that normal computer operation is initiated by the read-in button. Control first goes to a short program in test storage. That program:

1. records the contents of magnetic-core memory on drum group 0;
2. reads the utility control program from the drum into core memory; and
3. transfers computer control to the utility control program.

The order matters historically because the report does not describe a blind overwrite of the active core image. The old image is copied out before the utility-control image occupies core memory.

A conservative representation of the documented sequence is:

```text
current magnetic-core-memory image
    -> auxiliary drum group 0

utility-control program on drum
    -> magnetic-core memory

computer control
    -> newly loaded utility-control program
```

This is a normal operational read-in path. The report does **not** call it crash recovery, hibernation, checkpointing, or a power-failure restart protocol.

## Historical record — the bootstrap source and saved image have different retention roles

Adams's May 1954 R-233 report gives more structure to the same mechanism.

It describes Whirlwind registers 0 through 7 as `permanent non-erasable storage` for the program initiated by the read-in button. That program copies all of core memory to drum group 0 and then copies drum group 11 into core memory.

The same report says drum group 11 is permanently recorded, with its recording tubes disabled, and contains the path used to select conversion or service routines.

Thus at least three differently governed retained representations participate:

```text
small read-in program
    -> "permanent non-erasable storage" in the period source

drum group 11
    -> protected / permanently recorded bootstrap program

drum group 0
    -> destination for the current core-memory image
```

These are not one generic class of "persistent memory." They have different update and protection rules.

## Historical record — group 0 is a rolling preservation slot, not protected bootstrap storage

M-1623-2, revised in September 1954, independently states that auxiliary drum group 11 contains the `Drum Input Program` permanently, with recording circuits normally disabled. It separately says auxiliary drum group 0 is used by the input program to hold a copy of MCM (magnetic-core memory).

The later 1958 *Whirlwind Programming Manual* makes the overwrite rule especially explicit: programmers normally avoid group 0 because pressing read-in causes the contents of the cores to be blocked out to group 0, thereby destroying whatever information group 0 previously held. Group 11, by contrast, continues to be described as holding the Drum Input Program permanently, with recording normally disabled.

Therefore:

```text
protected bootstrap source (group 11)
    != rolling saved-core destination (group 0)

group 0 contains a saved core image
    != group 0 is an append-only archive
    != group 0 preserves every earlier core image
```

The system preserves the image displaced by the current read-in, but the same preservation slot can be replaced on a later read-in.

## Engineering reconstruction — pre-overwrite preservation handoff

The project can reconstruct the mechanism as a **pre-overwrite preservation handoff**:

```text
active embodiment A: core image C0
    ↓ copy
retained alternate embodiment: drum group 0 = C0
    ↓
active core is repopulated with control image C1
    ↓
execution authority transfers to C1
```

`pre-overwrite preservation handoff`, `rolling preservation slot`, and `execution authority` are project engineering terms. They are **not** claimed as Whirlwind-era vocabulary.

The mechanism separates several relations that are easy to collapse:

1. **payload presence** — the old core words physically exist in core before read-in;
2. **preservation copy** — those words are copied to drum group 0;
3. **active embodiment** — core is then reused for a different program;
4. **bootstrap-source protection** — the source on group 11 is protected from ordinary recording;
5. **execution entry** — control is explicitly handed to the newly loaded utility program.

Therefore:

```text
payload preserved somewhere
    != payload remains in the active memory embodiment
    != old execution context remains active
    != old computation automatically resumes
```

## What this does and does not close in Case 02

This packet closes a bounded part of the prior `direct Whirlwind` debt:

- **closed:** a primary-source Whirlwind operational-entry / read-in handoff in which the current core image is preserved before core is repurposed;
- **still open:** actual Whirlwind power-on / power-off sequencing and arbitrary power-failure recovery;
- **still open:** whether and how a saved group-0 image was routinely restored as a whole computation;
- **still open:** which processor/control registers, I/O state, and entry information were required to resume a displaced computation;
- **still open:** the persistence behavior of the small test-storage/read-in state across actual power transitions.

The key non-claim is:

```text
normal read-in saves core first
    != power loss automatically saves core
    != saved core image is a crash-consistent whole-machine checkpoint
```

The 1954 report's separate discussion of improved power-distribution relays and better transient regulation is evidence about system reliability. It is not used here as proof that the read-in mechanism was designed specifically for power-fail preservation.

## Functional analogy

A later hibernation image, checkpoint, bootloader, or crash-recovery system can be compared only at the relation level:

```text
preserve displaced state
    -> reuse active substrate
    -> enter a control program
```

The analogy stops there.

Whirlwind's read-in path does not establish modern crash-consistency semantics, persistence domains, atomic checkpoint publication, or a lineage from this mechanism to later hibernation / checkpoint systems.

## Philosophical interpretation

The exact technical fact is modest but useful: Whirlwind could preserve a state by **changing its embodiment before changing what the active core memory was for**.

A bounded interpretation is that technical continuity need not mean keeping one material location untouched. Continuity can be staged through controlled displacement:

```text
remain available
    != remain in the same embodiment
```

But the source also limits that interpretation. A copied payload is not identical to continuation of the computation that produced it. Availability of the old image, authority of the newly loaded control program, and resumability of the earlier execution are distinct relations.

This philosophical interpretation is ours; it is not attributed to Whirlwind engineers.

## Result

```text
current core image
    -> copied to drum group 0 before read-in replacement

group 11 protected bootstrap
    != group 0 rolling saved-image slot

saved payload
    != same active embodiment

saved payload
    != complete execution context

normal read-in preservation
    != power-failure recovery

embodiment replacement
    != technical forgetting
    when a usable alternate representation is retained
```

**Status:** Case 02 remains `grounded`. This is evidence deepening, not a maturity promotion.
