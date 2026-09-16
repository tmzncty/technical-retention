# Case 69 deepening record — DDR4 Self-Refresh Abort, refresh-counter credit, and exit compensation, 2012–2017

## Scope

This record deepens [`../cases/69-jedec-ddr4-refresh-postponement-pullin.md`](../cases/69-jedec-ddr4-refresh-postponement-pullin.md).

The existing grounding record establishes bounded postponement/pull-in, Fine Granularity Refresh (FGR), rate-transition grouping, and Self Refresh exit catch-up in the initial September 2012 DDR4 standard.

This slice asks a narrower question that the first pass did not isolate:

> What happens when DDR4 leaves autonomous Self Refresh while an internally timed refresh may already be in progress, and how does the standard distinguish interrupting that work from crediting it as completed maintenance?

The bounded answer is unusually explicit. JESD79-4 defines a programmable **Self Refresh Abort** mode in MR4 A9. With abort enabled, Self Refresh exit may abort an ongoing internal refresh and the device **does not increment the refresh counter** for that aborted work. A shorter `tXS_ABORT` exit path becomes available, but the ordinary requirement to issue at least one extra refresh before re-entering Self Refresh remains.

The slice therefore adds a retention-control distinction not made explicit in the original Case 69 text:

```text
maintenance may have started
    !=
maintenance has earned accounting credit

faster service resumption
    !=
maintenance obligation erased
```

This is not a full DDR4 Self Refresh history, a transistor-level account of the internal refresh engine, or an invention-priority claim for abortable maintenance.

---

## Source A — JEDEC JESD79-4, September 2012

**Type:** `H/P`, normative primary standard.

**Artifact:** JEDEC Solid State Technology Association, **JESD79-4: DDR4 SDRAM**, September 2012.

**Inspected copy:** JEDEC-authored PDF mirrored by Texas Instruments E2E:
<https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/196/JESD79_2D00_4.pdf>

The cover identifies the artifact as `JESD79-4`, September 2012. The following claims are therefore bounded to the initial DDR4 standard rather than inferred from a later revision.

### A1 — MR4 A9 is explicitly `Self Refresh Abort`

The MR4 table on printed p. 20 assigns A9 to `Self Refresh Abort` with disabled/enabled settings.

This is important because abort behavior is not merely a controller-side optimization inferred from timing tables. It is part of the device-visible mode-register contract in the initial standard.

**Historical/normative fact:**

```text
MR4 A9 = 0
    -> Self Refresh Abort disabled

MR4 A9 = 1
    -> Self Refresh Abort enabled
```

The standard does not expose the internal circuit implementation of this bit.

### A2 — ordinary `tXS` waits for an internally started refresh to complete

In §4.27, the standard explains the ordinary Self Refresh exit path. The normal exit delay `tXS` is `tRFC + 10 ns`; the stated reason for that delay is to allow a refresh already started internally by the DRAM to finish.

Thus an SRX event can encounter an internal maintenance operation that is already underway. Ordinary exit semantics permit that work to finish before the relevant class of normal commands resumes.

This supports a historical distinction between:

- the command/state transition that asks the device to leave Self Refresh;
- the internal refresh operation that may already be executing;
- the time at which foreground commands become admissible again.

Those are not one event.

### A3 — abort mode explicitly withholds refresh-counter credit

The same §4.27 text defines the alternative behavior when MR4 A9 enables Self Refresh Abort:

- an ongoing refresh may be aborted;
- the refresh counter is **not incremented** for that aborted refresh;
- a controller may issue a valid command not requiring a locked DLL after `tXS_ABORT` rather than the ordinary `tXS` path.

This is the central new evidence for Case 69.

The standard itself therefore distinguishes:

```text
refresh activity was in progress
    !=
refresh counter advanced
```

The repository uses `maintenance credit` as an engineering reconstruction for this relation. JEDEC's historical vocabulary is the narrower statement that the device does **not increment the refresh counter** after the ongoing refresh is aborted.

Nothing in the inspected clause licenses the stronger claim that a partially executed refresh performed zero physical work. The source specifies the protocol/accounting result, not a row-by-row analogue model of an interrupted internal cycle.

### A4 — `tXS_ABORT` exposes a service-latency / maintenance-completion trade

The timing table distinguishes:

- `tXS`: exit Self Refresh to commands not requiring a locked DLL, with minimum `tRFC + 10 ns`;
- `tXS_ABORT`: the corresponding path with Self Refresh Abort, with minimum `tRFC4 + 10 ns` in the inspected table;
- `tXS_FAST`: a separate shorter timing class for a restricted set of ZQ/MRS commands.

The normative point is not that all of these are interchangeable. Rather, the standard provides different exit-admission paths with different command classes and prerequisites.

For the retention question, Self Refresh Abort permits foreground service to resume without waiting for an in-progress internal refresh to receive normal completion/accounting treatment.

A bounded engineering reconstruction is:

> DDR4 can trade some waiting for completion of autonomous maintenance against an explicit decision to abort that maintenance and withhold its counter progress.

This does **not** prove how much useful analogue restoration occurred before the abort or why the internal design chose `tRFC4` as the timing basis.

### A5 — an exit can miss an internally timed refresh event even without abort mode

Immediately before defining Self Refresh Abort, §4.27 says that raising CKE to exit Self Refresh creates the possibility that an internally timed refresh event is missed.

The standard therefore requires at least one extra refresh command before the device is put back into Self Refresh.

This requirement is not conditional on Self Refresh Abort being enabled. The standard explicitly keeps it the same irrespective of the MR4 abort setting.

Therefore:

```text
Self Refresh exit completed
    !=
all retention-maintenance accounting is closed
```

and:

```text
abort disabled
    !=
no exit compensation required
```

There are at least two reasons the exit boundary cannot be modeled as `leave mode -> all refresh history settled`:

1. an internally timed event can be missed at the transition;
2. with abort enabled, an in-progress refresh can be explicitly stopped without counter increment.

The specification supplies one conservative re-entry rule for both settings: issue at least one extra refresh before returning to Self Refresh.

### A6 — re-entry compensation is separate from ordinary average-`tREFI` scheduling state

Case 69's first grounding record already documents another Self Refresh exit obligation: incomplete FGR grouping before entry can require extra `REF1x`, `REF2x`, or `REF4x` commands under §4.9.5.

The §4.27 one-extra-refresh rule has a different stated trigger: the Self Refresh exit boundary itself can miss an internally timed refresh event, and Self Refresh Abort can interrupt one.

These rules should not be collapsed into one generic `catch-up refresh` without keeping their conditions separate.

At minimum, the 2012 standard exposes distinct maintenance-history relations around the same mode boundary:

```text
pre-entry external FGR grouping position
    -> may create FGR-specific exit catch-up

internal Self Refresh timing / possible in-progress refresh
    -> requires an extra refresh before Self Refresh re-entry
```

One command might satisfy more than one applicable constraint in a concrete controller sequence, but the clauses state different reasons. This record does not infer a universal implementation algorithm that merges them.

### A7 — command admission remains restricted during the abort interval

Figure 137 and its notes specify that only DESELECT is allowed during `tXS_ABORT`; the standard then identifies command classes that become legal after the relevant exit timing.

Thus:

> **abort authorization ≠ immediate unrestricted service**.

The transition still has an explicit timing/admission boundary even when the ongoing refresh is not allowed to complete normally.

---

## Source B — Samsung DDR4 Device Operation, Rev. 1.1, October 2014

**Type:** `H/P`, manufacturer-primary device-operation documentation.

**Artifact:** Samsung Electronics, **Device Operation — DDR4 SDRAM**, Rev. 1.1, October 2014.

Archived/indexed manufacturer PDF location:
<https://image.semiconductor.samsung.com/resources/data-sheet/DDR4_Device_Operations_Rev11_Oct_14-0.pdf>

The indexed manufacturer document reproduces the same bounded semantics in its Self Refresh section:

- the normal `tXS` delay exists to let an internally started refresh complete;
- MR4 A9 enables Self Refresh Abort;
- aborting an ongoing refresh does not increment the refresh counter;
- `tXS_abort` governs the shorter command-admission path;
- at least one extra refresh is still required before another Self Refresh entry regardless of the abort-bit setting.

This is useful as a named-vendor witness that the JEDEC contract appeared in manufacturer operational documentation by October 2014.

It is **not** independent evidence for invention priority: Samsung's document is implementing/describing a JEDEC DDR4 interface, not claiming to originate the mechanism.

---

## Source C — Micron DDR4 product documentation, 2017

**Type:** `H/P`, manufacturer-primary product documentation as indexed from Micron datasheets.

Two bounded examples were recovered:

- Micron **4Gb x4/x8/x16 DDR4 SDRAM**, Rev. G, January 2017;
- Micron **8Gb x4/x8/x16 DDR4 SDRAM**, Rev. M, October 2017.

Indexed copies include the same Self Refresh Abort semantics:

- MR4[9] selects the abort behavior;
- an ongoing refresh is aborted without incrementing the refresh counter;
- `tXS_ABORT` controls the earlier exit-to-command path;
- one extra REFRESH is required before re-entering Self Refresh.

Example indexed 8Gb datasheet copy:
<https://www.micron-electronic.com/pdf-80/mt40a1g8sa-075-h.pdf>

Example indexed 4Gb datasheet page:
<https://www.alldatasheetde.com/html-pdf/928196/MICRON/MT40A512M8RH-075E/16466/71/MT40A512M8RH-075E.html>

These product documents establish implementation-facing continuity of the interface vocabulary. They do not prove that Samsung and Micron used identical internal refresh engines or analogue abort circuitry.

---

## Historical record

The bounded historical record from the inspected sources is:

```text
September 2012 JESD79-4
    MR4 A9 defines Self Refresh Abort
    normal tXS allows internally started refresh to complete
    abort path may stop ongoing refresh
    aborted refresh does not increment refresh counter
    tXS_ABORT provides a separate command-admission timing
    at least one extra refresh is required before Self Refresh re-entry

October 2014 Samsung DDR4 device-operation document
    same externally visible abort/counter/re-entry semantics

2017 Micron DDR4 product documents
    same externally visible abort/counter/re-entry semantics
```

No claim is made here that the 2012 standard invented abortable refresh, that the concept first appeared in DDR4, or that the manufacturer documents are independent design genealogies.

---

## Engineering reconstruction

### E1 — maintenance execution and maintenance credit are separate state relations

The strongest engineering lesson follows directly from the standard's own counter rule:

```text
ongoing refresh exists
    -> controller/device may choose abort path
    -> refresh counter is not incremented
```

The repository therefore distinguishes:

1. **maintenance activity state** — an internal refresh may be underway;
2. **maintenance-accounting state** — whether the refresh counter advances;
3. **service-admission state** — when foreground commands are legal after exit.

These dimensions are coupled by the protocol but are not identical.

### E2 — interruptibility creates an explicit preservation obligation

A maintenance operation can be interruptible without becoming optional.

The abort path shortens one exit wait, but the protocol does not convert the interrupted refresh into completed work. The counter does not advance, and a re-entry compensation rule remains.

Therefore:

> **interruptible maintenance ≠ dispensable maintenance**.

### E3 — faster availability can spend maintenance progress rather than eliminate maintenance cost

The difference between `tXS` and `tXS_ABORT` is a bounded example of a system making service available sooner by declining to wait for one internal maintenance operation to complete normally.

That is not equivalent to `faster refresh` in the sense of completing the same maintenance sooner. The source says the refresh is **aborted**.

So:

> **lower transition latency ≠ faster completion of the interrupted maintenance**.

### E4 — a mode boundary can preserve payload while leaving control obligations open

Self Refresh exists to retain DRAM data without external clocking, yet exiting it can leave an explicit requirement that constrains a later re-entry.

This means payload continuity across a mode boundary does not imply that all maintenance-control state has become irrelevant.

### E5 — a progress counter is meaningful only under its update rule

The refresh counter should not be interpreted as a raw clock or as proof that a row received arbitrary partial physical work. Its significance comes from the standard's state-transition rule: normal completed internal refresh processing advances it; aborting the ongoing refresh does not.

The exact row/address representation and counter circuit remain out of scope.

---

## Functional comparisons — not genealogy

### A — Case 21, Micron SDRAM refresh-mode handoff

Case 21 establishes the older high-level split between externally repeated AUTO REFRESH and autonomous SELF REFRESH. This deepening adds a more specific DDR4 transition rule: autonomous maintenance itself may be in progress at handoff, and exit semantics determine whether that operation receives counter progress.

The comparison is a refinement of authority handoff, not a claim that the 1999 device already implemented DDR4 Self Refresh Abort.

### A — Case 106, DDR5 Same-Bank Refresh accounting

Case 106 documents a later DDR5 rule in which a repeated REFsb can perform another refresh of the same row while the global refresh counter does not advance.

Case 69's mechanism is different: an **ongoing autonomous refresh is aborted** and the counter does not increment.

The bounded comparison is only:

```text
some maintenance-related physical/control activity
    !=
maintenance frontier/counter progress
```

This is a functional accounting comparison, not evidence of direct genealogy or identical counter architecture.

### A — Case 43, AVATAR feedback

AVATAR uses observed errors to change future refresh policy. DDR4 Self Refresh Abort instead changes one transition/command-admission path and its accounting result. Both make future maintenance depend on retained control state, but one is a research feedback policy and the other is a standardized mode-transition contract.

---

## Philosophical interpretation — bounded

A narrow conceptual result survives the engineering detail:

> A maintenance action can cease without being allowed to count as completed history.

That distinction matters for technical retention because `something happened to the substrate` is not enough to determine what the system may safely forget or count as finished. The operational rule that grants or withholds progress is part of the continuity mechanism.

The interpretation stops there. A refresh counter is not human memory, aborted refresh is not cultural forgetting, and the standard does not express a philosophy of incomplete action.

---

## Negative controls and rejected overclaims

This evidence does **not** support any of the following:

- `Self Refresh Abort was introduced in JESD79-4B` — false for this source set; it is already present in inspected September 2012 JESD79-4;
- `an aborted refresh performs no physical restoration at all` — not established; the standard specifies abort/counter semantics, not partial analogue effects;
- `refresh counter not incremented means the whole device refresh schedule resets` — not established;
- `tXS_ABORT means there is no exit latency` — false; it is itself a specified delay and command admission remains constrained;
- `one extra REFRESH before re-entry replaces every possible FGR catch-up obligation` — not established; §4.9.5 and §4.27 state distinct conditions;
- `Self Refresh exit loses payload` — not the mechanism described; the rule is part of preserving retention across the transition;
- `Samsung and Micron prove independent invention` — unsupported;
- `all DDR4 revisions and all products implement identical internal abort circuitry` — unsupported;
- `refresh counter` here is a host-visible lifetime counter — false category; this is device-internal refresh progress state in the Self Refresh protocol;
- `maintenance credit` is JEDEC vocabulary — false; it is project engineering vocabulary.

---

## Claim ledger

| Claim | Layer | Status / evidence |
| --- | --- | --- |
| September 2012 JESD79-4 exposes Self Refresh Abort at MR4 A9 | `H/P` | directly inspected MR4 table |
| normal `tXS` allows an internally started refresh to complete | `H/P` | directly inspected §4.27 |
| abort mode may abort an ongoing internal refresh | `H/P` | directly inspected §4.27 |
| aborted refresh does not increment refresh counter | `H/P` | directly inspected §4.27 |
| `tXS_ABORT` is a distinct exit-to-command timing | `H/P` | §4.27 + AC timing table |
| at least one extra refresh is required before Self Refresh re-entry irrespective of abort setting | `H/P` | directly inspected §4.27 |
| Samsung 2014 documents the same interface semantics | `H/P` | manufacturer device-operation document |
| Micron 2017 documents the same interface semantics | `H/P` | manufacturer product datasheets |
| refresh activity and refresh-accounting credit are distinct relations | `E` | reconstruction from explicit abort + no-counter-increment rule |
| shorter abort exit means interrupted refresh finished faster | `X` | contradicted by explicit `abort` semantics |
| one extra re-entry refresh automatically discharges every FGR transition obligation | `X` | source set does not establish this merge |
| Self Refresh Abort was invented by JEDEC DDR4 | `X` | no priority research performed |
| Samsung/Micron similarity proves common internal circuitry | `X` | interface behavior does not establish implementation identity |
| Case 69 and Case 106 use the same refresh-counter mechanism | `A/X` | only a functional accounting comparison is justified |

---

## Prior-art boundary

This slice does not attempt a pre-DDR4 genealogy of interruptible Self Refresh, internal refresh counters, or low-latency exit.

The defensible historical claim is deliberately narrow:

> **By the initial September 2012 JESD79-4 standard, DDR4 already specified an MR4-controlled Self Refresh Abort path in which an ongoing internal refresh may be aborted without refresh-counter increment, while a separate extra-refresh requirement remains before Self Refresh re-entry. Samsung and Micron later documented the same interface semantics in named DDR4 device/product documentation.**

Any claim about invention, committee proposal ancestry, DDR3 predecessors, or vendor-to-vendor technical transmission requires separate prior-art research.

---

## Related-repository check

`tmzncty/computing-archaeology` was searched again before this slice for `Fine Granularity Refresh`, `Self Refresh Abort`, and the DDR4 refresh-transition vocabulary. No dedicated technical-history slice was found.

Accordingly this record keeps only the retention-specific distinction among maintenance execution, accounting progress, service admission, and compensation. A broader genealogy of DDR Self Refresh exit mechanisms belongs in `computing-archaeology` if developed.

---

## Remaining evidence debt

Useful follow-up work, none of which blocks this bounded deepening:

1. recover JEDEC ballot / committee-item ancestry for MR4 A9 if invention or revision genealogy becomes important;
2. inspect earlier DDR3/LPDDR standards for comparable abort semantics before making any first-use claim;
3. recover manufacturer implementation notes that explain the internal microarchitectural reason for the `tRFC4`-based abort timing, if publicly documented;
4. test how real memory controllers expose or hide policy selection for MR4 A9;
5. determine, from normative wording rather than assumption, how controllers should compose the §4.27 extra-refresh rule with every possible §4.9.5 FGR catch-up case.

---

## Deepening decision

**Status: `bounded deepening complete`.**

The slice is complete for its narrow question because the central distinction comes directly from a page-inspected September 2012 JEDEC artifact and is corroborated by later Samsung and Micron manufacturer documentation. It does not change Case 69's overall `grounded` maturity; it sharpens the case's account of Self Refresh transitions and maintenance accounting.
