# Deepening Record — Intel SA-1100 Alternate-Master DRAM-Integrity Handoff

## Target case

[`cases/03-dram-refresh-as-scheduled-restoration.md`](../cases/03-dram-refresh-as-scheduled-restoration.md)

## Status

**`bounded deepening complete`**

Canonical maturity remains **`grounded`** in [`CASE_INDEX.md`](../CASE_INDEX.md). This record does not promote Case 03 and does not turn it into a general StrongARM, shared-memory-bus, DMA, or DRAM-controller history.

## Research question

Case 03 already separates the DRAM payload from the timer / request / coverage / arbitration state that causes refresh to happen. Its existing SA-1100 sleep slice adds one authority-transfer pattern: before ordinary memory-controller state is reset, the controller places DRAM into self-refresh so the device itself carries the retention obligation across sleep.

The SA-1100 manual documents a second, importantly different pattern in the immediately adjacent memory-controller chapter:

> What happens when the SA-1100 deliberately gives another external bus master control of the DRAM pins while the SA-1100 itself can no longer issue refresh cycles?

Intel's answer is explicit. Before granting the bus, the SA-1100 finishes pending / in-progress memory work and any outstanding DRAM refresh cycle. During alternate mastership, the SA-1100 cannot refresh. Intel therefore assigns responsibility for **DRAM integrity** to the alternate master. That responsibility can be discharged in either of two bounded ways:

1. keep alternate mastership much shorter than the DRAM refresh period; or
2. make the alternate master capable of issuing refresh at the required intervals.

When control returns, a refresh request that became due in the SA-1100 during the alternate master's tenure is serviced before other stalled bus work.

This gives Case 03 a clean named-system witness for:

```text
bus ownership
    !=
payload ownership
    !=
refresh execution authority
    !=
refresh obligation
```

and for two different ways to preserve a deadline-governed relation across a temporary authority gap:

```text
use remaining deadline slack
    OR
transfer active maintenance capability
```

---

# 1. Source custody and chronology

## 1.1 Intel SA-1100 Technical Reference Manual — September 1998

Intel Corporation, **_SA-1100 Microprocessor Technical Reference Manual_**, September 1998, Order Number `278088-001`.

Public archival copy inspected as a page-preserving PDF:

<https://stuff.mit.edu/afs/sipb/contrib/doc/specs/ic/cpu/arm/sa1100-techref.pdf>

The PDF identifies itself as Intel documentation and as an intermediate draft. It is therefore used as a **manufacturer-primary draft artifact**, not as evidence that every production stepping necessarily behaved identically.

Relevant sections:

- §10.3.3, `DRAM Refresh`, printed p. 10-18;
- §10.8, `Alternate Memory Bus Master Mode`, printed p. 10-31;
- §16.8, `Memory Bus Alternate Master`, printed p. 16-10.

The present slice is grounded primarily in §10.8. The chapter-16 test-interface description independently restates the same bounded hazard: while an external device is master, the SA-1100 does not perform DRAM refresh, so alternate tenure should not exceed the refresh period unless refresh is supplied elsewhere.

## 1.2 Intel StrongARM SA-1100 Developer's Manual — August 1999

Intel Corporation, **_Intel StrongARM SA-1100 Microprocessor Developer's Manual_**, August 1999, Order Number `278088-004`.

A public manual index preserves §10.8 `Alternate Memory Bus Master Mode` in the later edition:

<https://www.manualsdir.com/manuals/126682/intel-strongarm-sa-1100.html>

A separately indexed copy of the 1999 manual reproduces the same core sequence: complete pending memory / refresh work, grant the tristated bus, make the alternate master responsible for DRAM integrity, and service a refresh that became due during alternate tenure before stalled transactions after return.

The 1998 Intel PDF remains the directly inspected detailed anchor. The 1999 edition is a continuity witness, not a substitute for page-level inspection of every later revision.

## 1.3 Related-repository check

Fresh searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `SA-1100` and `StrongARM` found no dedicated reusable module.

A broad history of StrongARM shared-bus architecture, alternate-master modes, GPIO handshake design, embedded coprocessors, and successor PXA/SA-1110 bus-master behavior belongs primarily in `computing-archaeology` if developed. This record keeps only the retention-specific authority / deadline relation.

---

# 2. Historical record

## H/P — the grant is ordered after already-admitted memory and refresh work

Intel §10.8 says an alternate master requests the memory bus by asserting `MBREQ`. The SA-1100 does **not** immediately tristate the bus. It first completes:

- any pending or in-progress memory operation; and
- any outstanding DRAM refresh cycle.

Only then does it assert `MBGNT` and tristate the memory-bus address, data, chip-select, output-enable, write-enable, RAS, and CAS pins.

The documented grant therefore has a closure boundary:

```text
alternate-master request
    ↓
finish admitted memory work
    + finish outstanding refresh
    ↓
grant bus / tristate SA-1100 pins
```

This is historical ordering in the Intel manual. It should not be inflated into a universal bus-handoff rule.

**Primary anchor:** Intel SA-1100 TRM, September 1998, §10.8, printed p. 10-31.

---

## H/P — while the alternate master owns the bus, the SA-1100 cannot perform DRAM refresh

During the tristate interval, `MBREQ` and `MBGNT` remain asserted and the external device controls the bus pins. Intel then states the retention consequence directly: the SA-1100 is unable to perform DRAM refresh cycles during that period.

This separates physical payload presence from the controller's current ability to execute maintenance:

```text
DRAM payload still physically present
    !=
SA-1100 currently able to refresh it
```

The bus handoff is therefore also a handoff in the machinery capable of meeting a time-bounded retention obligation.

**Primary anchor:** Intel SA-1100 TRM, §10.8, printed p. 10-31.

---

## H/P — Intel explicitly transfers responsibility for DRAM integrity to the alternate master

The manual's wording is unusually strong: during alternate mastership, **the alternate master must assume responsibility for DRAM integrity**.

Intel does not reduce that responsibility to one mandatory implementation. Instead it gives two engineering choices:

1. design the system so alternate mastership lasts **much less than the refresh period**; or
2. make the alternate master implement a refresh counter so it can perform refresh at the proper intervals.

Thus the period manual itself distinguishes:

```text
short authority absence tolerated by deadline slack
```

from:

```text
longer authority transfer backed by replacement refresh machinery
```

The source does not say that the alternate master must duplicate every SA-1100 memory-controller register or internal state bit.

**Primary anchor:** Intel SA-1100 TRM, §10.8, printed p. 10-31.

---

## H/P — a refresh can become due inside the SA-1100 while it lacks execution authority

Intel also describes bus return. The alternate master deasserts `MBREQ`; the SA-1100 deasserts `MBGNT` and resumes driving the bus.

The important retention detail comes next: if the **refresh counter inside the SA-1100 requested a refresh cycle during the alternate-master tenure**, that refresh cycle is run first, before other bus transactions that stalled during the same interval.

This means that at least one maintenance relation can continue evolving while the controller cannot execute the resulting maintenance action:

```text
internal refresh timing / request state
    can become due
while
refresh execution authority is unavailable
```

and after reacquisition:

```text
pending refresh obligation
    -> serviced before deferred ordinary traffic
```

The manual does not state how many refresh deadlines could be represented as pending, whether requests coalesce, or what happens after an overlong / defective alternate-master tenure. Those remain open.

**Primary anchor:** Intel SA-1100 TRM, §10.8, printed p. 10-31.

---

## H/P — chapter 16 independently restates the refresh-period hazard

The SA-1100 boundary-scan / test-interface chapter describes the alternate-master facility again for specialized systems / development platforms. It warns that an external device should not remain memory-bus master longer than a DRAM refresh period because the SA-1100 will not perform refresh while the external device is master.

This second location matters as an internal consistency check within the same manufacturer manual. It is not an independent product or independent validation source.

**Primary anchor:** Intel SA-1100 TRM, §16.8, printed p. 16-10.

---

# 3. Engineering reconstruction

The following are **E — engineering reconstructions** from Intel's documented behavior. They are not Intel's philosophical vocabulary.

## E1 — ownership of the bus and ownership of the retention obligation are distinct relations

It is tempting to say that the alternate master simply “owns memory.” That is too coarse.

At least four relations are separable:

```text
who may drive the memory bus now
    !=
where the DRAM payload physically resides
    !=
who can issue refresh cycles now
    !=
who is responsible for ensuring deadlines are met
```

Before grant, the SA-1100 owns bus execution and refresh scheduling. During alternate mastership, the external device owns the bus and Intel assigns it the integrity obligation. The DRAM payload itself remains in the same physical devices.

---

## E2 — an obligation can transfer without transferring the original controller's complete maintenance state

Intel's first permitted strategy is simply to keep alternate tenure much shorter than the refresh period.

That strategy does not require the alternate master to reconstruct the SA-1100's exact refresh-timer phase. It relies on a bounded interval in which the existing DRAM state can remain recoverable without another refresh.

Therefore:

```text
retention obligation transferred
    !=
original maintenance microstate transferred bit-for-bit
```

The handoff can be safe because a **deadline budget** survives the authority transition.

---

## E3 — deadline slack is itself part of the safe handoff envelope

For the short-tenure strategy, the useful resource is not another copy of the payload. It is time before the next required refresh deadline becomes unsafe.

A bounded reconstruction is:

```text
last qualifying refresh
    ↓
remaining refresh slack
    ↓
bus authority moves away from SA-1100
    ↓
alternate tenure completes before slack is exhausted
    ↓
SA-1100 reacquires bus and refreshes as needed
```

Thus:

```text
no refresh during handoff interval
    !=
immediate data loss
```

but also:

```text
payload still readable now
    !=
unbounded permission to defer refresh
```

The manual supplies a design recommendation, not an empirical distribution of weak-cell retention times.

---

## E4 — replacement maintenance capability is a second route to continuity

For a longer tenure, Intel recommends that the alternate master implement a refresh counter and perform refresh at the proper intervals.

This produces a different authority path:

```text
SA-1100 refresh authority
    ↓ handoff
alternate-master refresh authority
    ↓ return
SA-1100 refresh authority
```

Continuity therefore can be maintained by **moving active refresh execution capability between controllers** rather than moving the payload or placing the DRAM into self-refresh.

The source does not establish that the two controllers share one counter value, one row-coverage cursor, or one atomic checkpoint.

---

## E5 — pending maintenance evidence can survive temporary loss of execution authority

Intel's statement that the SA-1100 can detect a refresh becoming due during alternate tenure and service it first afterward supports a narrower distinction:

```text
maintenance due-state
    !=
maintenance execution
```

A controller can retain enough local timing / request state to know that refresh is owed even while it is temporarily unable to touch the bus.

This is not a durable checkpoint claim. The state is ordinary powered runtime control state.

---

## E6 — post-handoff priority is not proof that the deadline was safely met

On bus return, servicing the pending refresh first is a conservative scheduling choice. It does **not** prove that an overlong alternate tenure caused no retention damage.

Therefore:

```text
refresh serviced immediately after reacquisition
    !=
proof all prior refresh deadlines were satisfied
```

and:

```text
controller knows refresh is due
    !=
payload integrity has been independently requalified
```

The inspected manual contains no fault-injection evidence for deliberately violating the refresh-period recommendation.

---

# 4. Contrast with the existing SA-1100 sleep/self-refresh slice

The existing evidence record [`03-intel-sa1100-1998-1999-sleep-self-refresh-control-state-handoff-deepening.md`](03-intel-sa1100-1998-1999-sleep-self-refresh-control-state-handoff-deepening.md) documents a different handoff:

```text
ordinary SA-1100 refresh
    -> DRAM self-refresh
    -> ordinary controller state lost / rebuilt
    -> SA-1100 refresh resumes
```

The present slice instead documents:

```text
ordinary SA-1100 refresh
    -> external alternate-master bus tenure
       [deadline slack OR external refresh]
    -> SA-1100 refresh resumes
```

The distinction matters:

```text
handoff to autonomous media/device maintenance
    !=
handoff to another external controller
```

In sleep mode, ordinary memory-controller configuration can be intentionally lost while the DRAM self-refresh relation remains active. In alternate-master mode, the SA-1100 remains powered enough for its refresh counter to register a due request, yet loses the physical execution authority needed to issue the refresh until the bus returns.

Together the two slices show that **maintenance authority is not fixed to one physical location or one continuity model**.

---

# 5. Functional comparisons — not genealogy

## 5.1 Case 21 — SDRAM refresh-mode handoff

Case 21 separates a request to enter / exit self-refresh from the transition's completion and later access admission.

The present SA-1100 slice is functionally comparable because it also has a handoff boundary before ordinary traffic changes authority. But it is not the same mechanism: one moves a DRAM between operating modes; the other transfers the shared bus to another master.

No direct genealogy is claimed.

## 5.2 Case 105 — per-bank refresh coordination

Case 105 shows that maintenance authority can be split across controller/device roles at bank granularity. The SA-1100 alternate-master case instead moves bus-level refresh responsibility across masters.

The shared functional lesson is only:

```text
maintenance obligation
    != fixed controller identity
```

The interfaces, standards, and historical lines remain distinct.

## 5.3 Distributed maintenance cases

Later distributed systems can retain repair debt while the worker capable of executing repair changes. That is a useful analogy for `obligation != executor`, but the SA-1100 case is not a distributed-storage ancestor and should not be presented as one.

---

# 6. Philosophical interpretation

A narrow project-level interpretation is defensible:

> A retained state can depend on an obligation whose **executor is replaceable**. Continuity may be secured either by transferring the work or by completing the authority gap before the substrate's deadline slack is exhausted.

The useful decomposition is:

```text
thing retained
    !=
obligation to maintain it
    !=
agent currently authorized to perform that maintenance
    !=
time budget within which another agent may safely take over
```

This is project vocabulary. Intel describes memory-bus handshaking, refresh, and DRAM-integrity responsibility; it does not present a philosophical theory of delegated memory or institutional responsibility.

---

# 7. Failure and forgetting boundaries

Distinct failures must remain separate:

- the alternate master obtains bus authority but never returns it;
- alternate tenure exceeds the safe refresh envelope without supplying replacement refresh;
- the alternate master implements refresh but schedules it incorrectly;
- the SA-1100 records a refresh request while unable to execute it;
- bus ownership returns and the SA-1100 performs the pending refresh, but an earlier deadline may already have been violated;
- the DRAM remains physically readable for some interval despite a violated controller contract;
- one or more cells lose sufficient charge before useful access resumes.

None of these is equivalent to secure erasure, deliberate deletion, or proof that every DRAM bit changed.

---

# 8. Explicit non-claims

This deepening does **not** claim that:

1. the SA-1100 invented alternate memory-bus masters or delegated refresh;
2. every production SA-1100 stepping exactly matches the 1998 intermediate draft;
3. bus ownership is logically identical to refresh responsibility in all systems;
4. the alternate master receives a copy of the SA-1100's internal refresh-counter state;
5. Intel documents an atomic transfer of refresh-counter state;
6. the alternate master's recommended `refresh counter` has the same implementation as the SA-1100 counter;
7. the two masters share a common row-coverage cursor;
8. a single pending refresh bit can represent arbitrary missed refresh intervals;
9. the SA-1100 can safely tolerate alternate tenure up to an exact universal numerical limit independent of the attached DRAM;
10. `much less than the refresh period` is a measured weak-cell retention distribution;
11. servicing a pending refresh first after bus return proves that no deadline was violated;
12. DRAM payload corruption is certain immediately when the specified refresh interval is exceeded;
13. the alternate-master path uses DRAM self-refresh;
14. the sleep/self-refresh path and alternate-master path are the same handoff mechanism;
15. later PXA / SA-1110 behavior is identical to SA-1100 without separate inspection;
16. any analogy to distributed maintenance implies historical influence.

---

# 9. What this slice closes

This pass closes one bounded debt from [`03-dram-evidence-index.md`](03-dram-evidence-index.md):

> **Alternate-master refresh handoff:** the SA-1100 manual separately assigns DRAM-integrity responsibility to an alternate bus master while the SA-1100 cannot refresh.

The relation is now source-controlled at the level of:

- grant ordering;
- temporary loss of SA-1100 refresh execution authority;
- explicit assignment of DRAM-integrity responsibility;
- short-tenure deadline-slack strategy;
- replacement-refresh strategy;
- pending-refresh priority on return.

It does **not** close silicon fault validation, attached-DRAM timing margins, or cross-vendor genealogy.

---

# 10. Remaining high-value debt

1. **Fault-window validation:** exercise alternate tenure across the attached DRAM's specified refresh interval and measure when errors first appear.
2. **Named board / alternate-master pairing:** identify a period SA-1100 development platform that actually used this feature and the external master involved.
3. **Counter/request semantics:** determine from additional implementation documentation whether due refresh requests can coalesce or accumulate during alternate tenure.
4. **Attached-DRAM contract:** combine a named DRAM part's refresh period / self-refresh behavior with the SA-1100 bus handoff.
5. **Successor comparison:** inspect SA-1110 / PXA changes only if they materially alter the retention relation; broad product genealogy belongs in `computing-archaeology`.

---

# 11. Status decision

**No maturity change.**

Case 03 remains **`grounded`**. The new evidence deepens the authority-transfer axis but does not establish a universal rule for DRAM systems or provide empirical fault validation.