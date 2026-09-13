# Evidence 150 — Crucial SSD Active Garbage Collection: Powered Idle, Sleep States, and Maintenance Opportunity

## Status

**`bounded deepening complete`**

This record deepens [Case 150](../cases/150-crucial-m550-active-garbage-collection.md). It does not replace the canonical case and does not attempt to reconstruct proprietary Crucial/Micron firmware.

## Bounded question

Case 150 already establishes that Crucial describes Active Garbage Collection as controller-local background cleanup that benefits from powered idle time. The narrower question here is:

> **Is host-visible idleness by itself enough to constitute a maintenance opportunity, or does the storage device also have to remain in a power state in which controller-local work is allowed to proceed?**

This distinction matters because the 2014 Crucial M550 product flyer lists both **Active Garbage Collection** and **Device Sleep support**, while Crucial's maintained support instructions explicitly tell operators to keep an SSD powered and idle, and to change sleep-related power settings when trying to provide garbage-collection opportunity.

The evidence supports a strong engineering boundary but not a proprietary scheduler reconstruction:

```text
host has no foreground I/O
        !=
device is in a maintenance-eligible power state
        !=
garbage collection is currently executing
        !=
reclamation is complete
```

The project phrase **maintenance-eligible power state** is an engineering reconstruction. It is not claimed as Crucial or SATA-IO historical vocabulary.

---

## 1. Historical record — one product publicly exposed both reclamation and sleep features

The Crucial M550 product flyer is revision-dated **29 January 2014**. Its advanced-feature list includes, separately:

- `Active Garbage Collection`;
- `TRIM support`;
- `Power Loss Protection`;
- `Device Sleep support`;
- SMART and ECC.

The same flyer identifies the family as SATA 6 Gb/s, based on 20 nm Micron MLC NAND, with user-upgradeable firmware.

This establishes only a product-level coexistence fact:

> **By the M550 launch period, Crucial could ship a managed SSD that advertised both controller-local reclamation and a low-power sleep capability.**

It does **not** establish how M550 firmware arbitrated those features, whether garbage collection could run in any particular SATA low-power state, or what internal resources remained powered in Device Sleep.

The flyer itself does not document an idle timer, GC threshold, power-state eligibility table, or transition diagram.

---

## 2. Maintained Crucial guidance — powered idle is deliberately constructed

Crucial's maintained support article **“My SSD used to be so much faster, but recently it's been slowing down...”**, dated **15 November 2024** on localized Crucial support sites, describes Active Garbage Collection as a controller-resident maintenance feature that runs when the SSD has power but is not actively reading or writing.

The article then gives an unusually explicit operational procedure when performance has degraded:

- power the SSD on;
- leave it idle for **6–8 hours**;
- on a PC, enter BIOS/UEFI so the SSD remains powered while the operating system does not generate normal storage traffic;
- on a Mac, use Startup Manager for the same broad purpose;
- adjust power settings so the SSD remains powered when the computer sleeps, thereby giving garbage collection opportunity to run.

For SATA SSDs, the maintained page tells Windows users to set the hard-disk sleep field to **Never**. For NVMe SSDs it separately points to PCI Express Link State Power Management. The article is therefore discussing system policy that preserves a useful maintenance window, not merely the absence of application I/O.

The bounded historical/operational claim is:

> **Crucial currently treats “powered and idle” as an intentionally constructed condition for background maintenance, and explicitly warns that ordinary system power-management behavior can remove that opportunity.**

Because the article is maintained in 2024, this claim is a current family-level support contract. It is **not** back-projected into 2014 as proof that M550 MU01 used the same 6–8-hour troubleshooting duration, identical sleep-state gates, or identical scheduler logic.

---

## 3. The 6–8-hour interval is a runbook window, not a physical constant

The support page's `6–8 hours` is operational advice for forcing an extended idle opportunity after observed performance degradation.

The evidence does **not** justify any of the following stronger readings:

- that exactly six hours is a firmware trigger;
- that eight hours guarantees completion of every outstanding reclaim operation;
- that all Crucial SSDs require the same amount of internal work;
- that the value is an M550-specific 2014 engineering constant;
- that the interval is a NAND data-retention refresh period;
- that a drive which has not been idle for six hours is already unsafe or corrupt.

The safer reconstruction is:

```text
long support-prescribed idle window
        ->
raises probability / opportunity for background cleanup
```

not:

```text
6 hours
        ->
universal deterministic GC completion threshold
```

The amount of reclaim work can depend on workload history, free space, stale/live-page distribution, firmware policy, temperature, wear state, and other factors that the support page does not enumerate.

---

## 4. SATA Device Sleep — `sleep` is an interface/power-state term, not a synonym for idle

SATA-IO's public **TPR 038: DEVSLP** for the SATA Revision 3.1 proposal set distinguishes several interface power states. In its interface-state table:

- `PHYRDY` keeps the PHY logic and main PLL active;
- `Partial` and `Slumber` are reduced-power states with different wake latencies;
- `DevSleep` permits the PHY logic to be powered down and has a substantially longer allowed exit latency than ordinary active operation.

SATA-IO's later interoperability test document states that, after DEVSLP is asserted, a supporting device enters the DevSleep interface power state, does not initiate device-to-host communication, and ignores host-to-device communication until the defined exit path.

These documents establish a protocol/power-state distinction, not a Crucial garbage-collector behavior.

They are useful here because they prevent a vocabulary collapse:

```text
host workload idle
    != SATA interface Partial
    != SATA interface Slumber
    != SATA Device Sleep
    != system S3/S0ix/etc.
    != device internally powered enough for some unspecified background task
```

A support instruction that says “leave the SSD powered and idle” therefore cannot safely be paraphrased as “any sleep state is equivalent.”

At the same time, SATA-IO's public DevSleep materials do **not** specify Crucial's internal NAND-controller power islands or whether any M550 housekeeping task may execute while its SATA interface is in DevSleep.

Therefore this evidence record deliberately does **not** claim:

> `DevSleep -> Active Garbage Collection impossible`.

The narrower supported conclusion is:

> **Interface idleness, interface sleep, and controller maintenance eligibility are distinct variables unless a product-specific source proves they coincide.**

---

## 5. Co-presence creates a scheduling tradeoff, not a contradiction

The M550 flyer publicly lists both Active Garbage Collection and Device Sleep support. Crucial's maintained support material later recommends keeping an SSD powered rather than letting ordinary power-management policy remove the idle maintenance window.

This is not evidence that the product is internally contradictory. It shows that two useful objectives can compete for the same wall-clock interval:

```text
objective A: minimize idle energy
    -> enter deeper low-power states sooner

objective B: spend idle opportunity on controller-local maintenance
    -> keep enough device resources available for background work
```

The exact arbitration belongs to firmware and platform policy. The public sources inspected here do not expose that arbitration for M550.

The technical-retention point is narrower and stronger:

> **An interval in which no user-visible work is occurring can still have alternative technical uses, and power policy can determine which of those uses remains available.**

Thus:

- `foreground inactivity != unallocated time at every lower layer`;
- `energy-saving opportunity != maintenance opportunity`;
- `wall-clock idle time != effective maintenance time`;
- `device supplied with some power != proof that all background engines remain eligible`.

---

## 6. Product-specific revision sensitivity — M550 power-state behavior was not frozen at launch

Crucial's M550 support page records firmware **MU02**, released **8 January 2018**, with release notes including:

- improved stability, efficiency, and performance during **power state transitions**;
- improved handling of environments with unstable power supplies;
- improved handling of SATA signal-integrity environments;
- corrected NCQ TRIM error handling.

This source is useful as a guardrail, not as a GC implementation disclosure.

It shows that M550's observable power-state behavior remained a firmware-maintained engineering surface after the 2014 launch. Therefore a current family-level support article should not be silently projected backward into one timeless M550 scheduler.

The release note does **not** say that MU02 changed garbage-collection eligibility, idle thresholds, victim selection, or DevSleep GC behavior. No such causal link is claimed here.

The only justified reconstruction is:

```text
same product family
    + firmware revisions affecting power-state transitions
        ->
power-management behavior is revision-sensitive enough that scheduler claims require version-specific evidence
```

---

## 7. Engineering reconstruction — maintenance opportunity is conjunctive

The combined evidence supports modeling controller-local cleanup opportunity as a conjunction rather than a single `idle` flag.

A deliberately simplified reconstruction is:

```text
maintenance opportunity
    requires some combination of:
        device energy available
        + controller/flash resources eligible
        + foreground demand low enough
        + sufficient relocation workspace
        + firmware policy deciding work is due
```

The exact predicates are implementation-specific. Crucial's maintained page directly supports powered idle and free-space dependence; the remaining terms are generic engineering decomposition and must not be mistaken for an M550 state machine.

This decomposition gives several useful inequalities:

```text
host idle != maintenance eligible
maintenance eligible != maintenance scheduled
maintenance scheduled != maintenance completed
maintenance completed != sanitization completed
```

It also clarifies why a support technician may use BIOS/UEFI or Startup Manager: those environments are not magical SSD commands. They are practical ways to create a long interval with power present and ordinary OS storage traffic suppressed.

---

## 8. Functional comparison — Case 111 long-offline SSD guidance

Case 111 concerns a different retention problem: enterprise SSDs stored without power for long periods and vendor runbooks that either restore powered maintenance opportunity or move data away before prolonged shutdown.

Case 150 concerns controller-local reclamation after ordinary managed-SSD workloads.

The functional analogy is only:

```text
some retained technical relations require future powered opportunity
```

The mechanisms and obligations differ:

- Case 111 is about long-offline data-retention risk and operational preservation policy;
- Case 150 is about reclaiming erase-block capacity and preserving live data while stale physical embodiments are retired;
- Case 111's weeks/months cadence must not be imported into Case 150;
- Case 150's 6–8-hour troubleshooting window must not be imported into long-term NAND retention qualification.

No genealogy is claimed.

---

## 9. Functional comparison — DRAM refresh cases

Cases 03, 09, and 10 concern DRAM whose payload state physically decays unless charge is periodically restored.

Case 150 is importantly different:

- an SSD can retain current NAND payload while accumulating reclamation debt;
- lack of garbage-collection opportunity may first appear as reduced free-space flexibility or performance pressure, not immediate payload decay;
- Active Garbage Collection relocates and erases managed-Flash embodiments; it is not periodic refresh of every current bit.

The comparison is useful precisely because it rejects a vague equation:

```text
background maintenance != refresh
```

Both can require power and time, but their failure semantics differ.

---

## 10. Functional comparison — JFFS2 and exposed scheduling authority

Case 145 documents JFFS2 garbage collection on raw Flash. There, filesystem code and its data structures expose more of the reclamation state machine to inspection.

Case 150 hides victim selection, mapping updates, and crash recovery behind a block-device interface.

The new power-state boundary adds another difference:

- in JFFS2, the operating system/filesystem directly participates in deciding when GC work runs;
- in a managed SSD, the host can influence workload, deallocation, power, and idle opportunity while controller firmware retains internal scheduling authority.

Shared vocabulary does not imply shared scheduling semantics.

---

## 11. Failure and observability boundary

Crucial's maintained support article associates insufficient idle cleanup with performance degradation and possible system freezes. That is an operator-visible symptom class, not a direct measurement of erase-block state.

Therefore:

```text
performance recovers after long powered idle
    != direct proof of which physical blocks were erased
```

and:

```text
performance remains degraded
    != direct proof that garbage collection never ran
```

A named-device experimental deepening would need lower-layer observables such as internal-write counters, latency traces, SMART/vendor telemetry, controlled free-space history, or direct firmware instrumentation. Even then, mapping individual internal writes to exact victim-block transitions would require care.

This record remains documentary, not experimental.

---

## 12. Explicit non-claims

This evidence does **not** establish that:

1. Crucial or Micron invented SSD garbage collection.
2. M550 MU01 used the same scheduler as Crucial's 2024 support guidance.
3. `6–8 hours` is a firmware constant or completion guarantee.
4. every Crucial SSD performs GC only when completely idle.
5. M550 cannot perform any background work while the SATA interface is in Partial, Slumber, or DevSleep.
6. SATA DevSleep removes all electrical power from NAND, DRAM, controller, or every internal power island.
7. the presence of `Device Sleep support` proves any specific M550 low-power implementation beyond advertised protocol support.
8. operating-system sleep is identical to SATA DevSleep.
9. keeping a drive awake guarantees that GC is immediately scheduled.
10. lack of GC opportunity is equivalent to immediate payload corruption.
11. ordinary garbage collection is a security sanitize operation.
12. a performance improvement after idle proves physical erasure of all stale embodiments.
13. MU02's power-state-transition fix modified Active Garbage Collection.
14. the SATA-IO DevSleep proposal specifies proprietary Crucial controller behavior.
15. modern NVMe Link State Power Management guidance can be back-projected onto a 2014 SATA M550.
16. controller-local housekeeping has one universal power-state policy across SSD vendors.

---

## 13. Claim ledger

| Claim | Type | Strength | Evidence / boundary |
| --- | --- | --- | --- |
| M550's 2014 flyer lists both Active Garbage Collection and Device Sleep support | historical record / primary | strong | Crucial M550 flyer, rev. 2014-01-29 |
| Crucial currently instructs operators to keep an SSD powered and idle for extended AGC opportunity | historical/current vendor record / primary | strong for maintained support policy | Crucial support article, 2024-11-15 |
| Crucial's maintained instructions explicitly adjust system sleep/power settings to preserve that opportunity | historical/current vendor record / primary | strong | same support article |
| `6–8 hours` is a support runbook window, not proven universal GC constant | engineering reconstruction | strong negative boundary | page wording + absence of implementation claim |
| SATA Device Sleep is a distinct interface power state from ordinary PHYRDY/Partial/Slumber | historical/protocol record / primary | strong | SATA-IO TPR 038 and interoperability documentation |
| M550 GC definitely stops in DevSleep | rejected | unsupported | no product-specific source inspected says this |
| Host idle and maintenance-eligible power state should be treated as separate analytical variables | engineering reconstruction | strong | Crucial power guidance + SATA state distinction |
| M550 power-state behavior is firmware-version-sensitive | historical/product record | moderate-strong | MU02 release note explicitly changes power-state-transition handling |
| MU02 changed GC scheduling | rejected | unsupported | release note does not say so |
| Case 150 and Case 111 share a general dependence on powered opportunity | functional analogy | bounded | different mechanisms/cadences retained |

---

## 14. Source ledger

### P1 — Crucial M550 product flyer, revision 29 January 2014 — primary product evidence

Crucial / Micron, **“Crucial M550 Solid State Drive”**:

<https://content.crucial.com/content/dam/crucial/ssd-products/m550/flyer/crucial-m550-ssd-product-flyer-en.pdf>

Directly supports M550 product identity and the separately listed features `Active Garbage Collection`, `TRIM support`, `Power Loss Protection`, and `Device Sleep support`.

The flyer does not disclose GC power-state eligibility or scheduler internals.

### P2 — Crucial Support, “SSD used to be faster but has slowed down,” 15 November 2024 — primary maintained operational guidance

Localized origin-hosted copy inspected through Crucial JP:

<https://www.crucial.jp/support/articles-faq-ssd/ssd-used-to-be-faster-but-has-slowed-down>

Directly supports:

- controller-local Active Garbage Collection;
- operation while powered and not actively reading/writing;
- need for idle time and free space;
- the 6–8-hour powered-idle troubleshooting procedure;
- BIOS/UEFI / Startup Manager as ways to maintain power without normal I/O;
- changing SATA/NVMe power settings so system sleep does not remove the maintenance opportunity.

This 2024 maintained article is not treated as a verbatim 2014 M550 firmware specification.

### P3 — SATA-IO, TPR 038, `DEVSLP` — primary protocol proposal / standards-history evidence

**“SATA3.1 TPR C108 – Device Sleep,” Version 1.0a**:

<https://sata-io.org/sites/default/files/TP_038_SATA31_TPR_C108_DEVSLP_V1.0a.pdf>

SATA-IO's public proposal materials define `DevSleep` as a distinct interface power state in which PHY logic may be powered down, separate from PHYRDY, Partial, and Slumber.

Used only to bound interface/power-state vocabulary. It is not an M550 firmware source.

### P4 — SATA-IO Unified Test Document 1.6, Device Sleep tests — primary interoperability evidence

<https://sata-io.org/sites/default/files/documents/UTD_1_6_Rev1_1%20Released.pdf>

The Device Sleep tests state that, after DEVSLP assertion, a supporting device enters the DevSleep interface power state, does not initiate device-to-host communications, and ignores host-to-device communications until exit behavior applies.

Again, this does not specify internal SSD garbage-collection activity.

### P5 — Crucial M550 firmware/support page, MU02 released 8 January 2018 — primary product-maintenance evidence

Crucial Support, **M550 SSD firmware and support**:

<https://stage.crucial.com/content/crucial/en-us/home/support/ssd-support/m550-support.html>

The published MU02 notes include improved stability/efficiency/performance during power-state transitions and corrected handling of NCQ TRIM errors. Used only to establish revision sensitivity around power behavior, not a GC change.

### R1 — repository companion check

A fresh search of `tmzncty/computing-archaeology` for `M550`, `Device Sleep`, `DEVSLP`, and SSD garbage collection found no dedicated study to reuse. Generic SATA/SSD power-management history should go there if expanded; this record retains only the maintenance-opportunity relation.

---

## 15. Remaining evidence debt

1. Recover an origin-hosted or archived **2010–2014 Crucial** support page containing the older 6–8-hour/BIOS Active Garbage Collection instructions, so the operational guidance can be dated closer to M550 without relying on later maintained text or third-party quotation.
2. Find a **product-specific M550/Micron engineering document** that maps Active Garbage Collection eligibility to SATA power states or idle timers.
3. Obtain a direct named-device trace comparing active idle, Partial/Slumber, and DevSleep while controlling free space and prior write history.
4. Test whether internal-write/SMART counters expose enough signal to distinguish maintenance opportunity from actual GC execution without reverse-engineering firmware.
5. Keep broader SATA DevSleep genealogy, controller power-island design, and cross-vendor low-power policy in `computing-archaeology` unless a retention-specific comparison requires it.

---

## Result

The slice closes one conceptual ambiguity in Case 150:

> **“Idle” is not a single system-wide state. Background retention/reclamation work depends not only on absence of foreground I/O but also on whether platform and device power policy leave the relevant maintenance machinery eligible to run.**

For Crucial SSDs, maintained vendor guidance directly constructs that condition as **powered idle** and warns operators to prevent ordinary sleep policy from taking it away. The 2014 M550 simultaneously advertised Active Garbage Collection and Device Sleep, but no inspected product-specific source proves how those two features were arbitrated internally. That unknown remains explicit rather than being filled with a modern assumption.
