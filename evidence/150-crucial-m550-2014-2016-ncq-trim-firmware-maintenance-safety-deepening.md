# Case 150 deepening — Crucial M550 queued-TRIM firmware boundary and maintenance-safety separation (2014–2016)

## Status

**Evidence deepening for grounded Case 150.** This packet does not change the canonical maturity level.

## Why this slice exists

Case 150 already grounds a managed-SSD reclamation chain in which host retirement knowledge, TRIM/deallocation, controller invalidity/currentness state, live-data relocation, and erase-block reclamation must not be collapsed into one event.

A remaining named-device gap was whether the host-to-device retirement path itself could become conditional on **firmware trust**, rather than merely on whether the command set nominally exposed TRIM.

The Crucial/Micron M550 gives a bounded source-controlled answer. Linux carried a model-specific workaround because M550 queued TRIM could corrupt data; later, after Micron released MU02, upstream Linux narrowed the workaround to **MU01**. Crucial's maintained M550 support page independently says MU02 corrected NCQ TRIM error handling. A later public mailing-list message from a Micron employee also distinguishes the M550's protection of already-written data during internal activity such as garbage collection from full protection of the volatile host-write cache.

The retention-specific question is therefore:

> **What happens when the communication that authorizes forgetting is itself unsafe under one command path / firmware revision, while a separate device-local power-loss mechanism protects already-retained data during internal maintenance without promising full in-flight-write durability?**

The bounded answer is:

```text
TRIM capability advertised
    != queued-TRIM path trusted
    != deallocation intent safely communicated through every command form

firmware revision changes command-path admissibility
    != old payload physically erased
    != garbage collection completed

maintenance-transaction protection
    != host-write-cache durability
```

This is not an M550 firmware reverse-engineering report. It does not reconstruct the precise queued-TRIM bug, internal FTL data structures, capacitor sizing, victim selection, page-pair schedule, or crash-recovery algorithm.

---

## Source set and source criticism

### Primary / near-primary engineering sources

1. Linux upstream commit `2a13772a144d2956a7fedd18685921d0a9b8b783`, **“libata: widen Crucial M550 blacklist matching”**, 2014. The commit states that Crucial M550 may cause data corruption on queued TRIM and widens the model match so 1 TB devices are also covered.
   - Stable-tree archive preserving the upstream commit message and patch: <https://lkml.rescloud.iu.edu/hypermail/linux/kernel/1409.3/08764.html>
   - Upstream commit id recorded by the stable review: `2a13772a144d2956a7fedd18685921d0a9b8b783`.

2. Linux upstream commit `ff7f53fb82a7801a778e5902bdbbc5e195ab0de0`, **“libata: Update Crucial/Micron blacklist”**, authored and committed **27 March 2015**. It states that Micron released MU02 for M510/M550/MX100 to fix queued-TRIM issues and changes the blacklist so M550 is restricted only when firmware revision is `MU01`.
   - <https://github.com/torvalds/linux/commit/ff7f53fb82a7801a778e5902bdbbc5e195ab0de0>

3. Crucial, **M550 SSD firmware and support**, maintained support page. The current page says MU02 updates M550 from MU01, is a mandatory cut-in for new factory production but optional for field drives, and includes **“Corrected error handling NCQ Trim Commands”** among the changes.
   - <https://www.crucial.com/support/ssd-support/m550-support>

4. Wes Vaske (`wvaske@micron.com`), Micron-domain reply on the PostgreSQL `pgsql-performance` mailing list, **7 July 2016**, preserved by Postgres Professional. Vaske distinguishes M550 capacitor protection for data already written to the device — including avoiding corruption of old data when data is read during garbage collection — from protection of the entire volatile cache.
   - <https://postgrespro.com/list/thread-id/2071335>
   - Mirror used during this research: <https://postgrespro.ru/list/thread-id/2071335>

### Supporting kernel terminology source

5. Linux's `ATA_HORKAGE_NO_NCQ_TRIM` was introduced specifically as a mechanism to disable **queued** TRIM for drives that advertised the capability but handled that command form incorrectly. The original M500 patch says the bad behavior could lead to silent data corruption; later kernel headers explicitly gloss the flag as `don't use queued TRIM` and distinguish it from `ATA_HORKAGE_NOTRIM`, which disables TRIM altogether.
   - Stable discussion of the original quirk: <https://lkml.rescloud.iu.edu/hypermail/linux/kernel/1401.0/02131.html>
   - Later stable patch showing `NO_NCQ_TRIM` versus `NOTRIM`: <https://lkml.iu.edu/hypermail/linux/kernel/1509.0/00695.html>

### Chronology caution: the current Crucial page's displayed release date is not authoritative for 2015 chronology

The maintained Crucial page currently displays MU02 as **“Released January 8, 2018.”** That cannot be used literally as the first release date because Linux commit `ff7f53...`, dated **27 March 2015**, already says Micron **has released** MU02 for M510/M550/MX100 and changes the compatibility table accordingly.

Period technology-news pages from January 2015 also reproduce the MU02 change list and describe it as newly released, but they are secondary evidence and are not needed for the stronger bounded conclusion here.

Therefore this packet uses:

```text
27 Mar 2015 upstream Linux commit
    -> hard latest bound: MU02 already existed and was treated as fixing queued TRIM

current migrated Crucial page
    -> first-party changelog continuity
    != trustworthy first-release chronology by itself
```

The discrepancy is itself methodologically useful: a maintained vendor support page can preserve a changelog while later CMS migration or metadata transformation makes its displayed release date unsafe as historical chronology.

---

# Historical record

## H1 — by 2014 Linux treated M550 queued TRIM as unsafe

The 2014 Linux stable record for upstream commit `2a13772a...` is unusually explicit:

- Crucial M550 was already blacklisted for queued TRIM;
- the reason given was that M550 **may cause data corruption on queued trims**;
- the change being made in that commit was not a new safety theory but a correction to the device-name pattern so the 1 TB M550 would actually match the existing workaround.

The code change widens:

```text
Crucial_CT???M550SSD*
```

to:

```text
Crucial_CT*M550SSD*
```

while retaining `ATA_HORKAGE_NO_NCQ_TRIM`.

This establishes a named-device, operating-system-level safety intervention. It does **not** establish the internal failure mechanism inside the M550.

## H2 — the Linux workaround disabled queued TRIM, not all TRIM

Linux distinguishes at least two relevant quirks:

```text
ATA_HORKAGE_NO_NCQ_TRIM
    = don't use queued TRIM

ATA_HORKAGE_NOTRIM
    = don't use TRIM
```

That distinction matters. The M550 evidence supports:

> **one command form / transport path was considered unsafe**

not:

> **the drive could not support any deallocation/TRIM operation at all.**

The host could therefore change *how* retirement knowledge was communicated without necessarily abandoning the higher-level retirement relation.

## H3 — MU02 changed the firmware-qualified trust boundary

Linux upstream commit `ff7f53...` on 27 March 2015 says:

- Micron had released MU02 for M510/M550/MX100;
- MU02 fixed the queued-TRIM issues on those models;
- M500 remained broken;
- the blacklist should be updated to reflect this.

The patch changes the M550 entry from an all-firmware model restriction to:

```text
{ "Crucial_CT*M550*", "MU01", ATA_HORKAGE_NO_NCQ_TRIM | ... }
```

The historical relation is therefore not simply:

```text
model = M550
    -> queued TRIM unsafe forever
```

but rather:

```text
model + firmware revision
    -> host compatibility / command-path policy
```

Within the Linux evidence:

```text
M550 + MU01
    -> queued TRIM disabled by libata

M550 + fixed later firmware such as MU02
    -> that specific M550/MU01 queued-TRIM prohibition no longer applies
```

This is a firmware-qualified **admission boundary**, not evidence that every other command and failure mode became bug-free.

## H4 — Crucial's maintained firmware page independently names NCQ TRIM error handling

Crucial's maintained M550 support page says the update is from MU01 to MU02 and includes:

- improved stability/efficiency/performance during power-state transitions;
- improved handling of unstable power supplies;
- improved SATA signal-integrity handling;
- improved SMART-read response;
- **corrected error handling for NCQ Trim Commands**;
- corrected SMART Attribute 5 reporting.

The page also says MU02 would be a mandatory cut-in for new product built in Micron factories while remaining optional for drives already in the field.

This gives a useful deployment distinction:

```text
firmware fix exists
    != every already-deployed M550 has the fixed firmware
```

and:

```text
new-production cut-in
    != field-fleet convergence
```

A host therefore had reason to qualify behavior by reported firmware revision even after a fix existed.

## H5 — the M550's named “Power Loss Protection” did not mean enterprise-style in-flight-write durability

In the 7 July 2016 `pgsql-performance` thread, a correspondent using a `micron.com` address, Wes Vaske, explicitly rejects the assumption that the Crucial M550's advertised power-loss protection means full cache protection.

His bounded M550 statement is that the drive's capacitors protect data that has already been written to the device, and he gives a garbage-collection example: if existing data are read during a GC operation, the M550 protects that data rather than introducing corruption of old data. He contrasts that with protection of the **entire cache**, which the M550 does not provide in the enterprise sense relevant to database/log durability.

This source is not a formal product specification. It is a public engineering statement by a Micron-domain participant and should therefore be weighted below a revision-controlled product manual. But it is useful because it explicitly disambiguates a product feature label that the M550 flyer itself leaves broad.

The safe historical reading is:

```text
M550 “Power Loss Protection” feature label
    != proof that acknowledged volatile-cache contents survive surprise power loss
```

while the mailing-list explanation supports a narrower old-data / data-at-rest protection role during internal operations.

---

# Engineering reconstruction

## E1 — retirement authority has a transport path

Case 150 already separates a host decision that logical data are no longer needed from the device's later physical reclamation.

The M550 queued-TRIM record adds another layer:

```text
host retirement decision
    -> deallocation/TRIM request prepared
    -> command transport / ordering form selected
    -> device safely interprets request
    -> controller retirement knowledge changes
    -> later reclamation work may use that knowledge
```

The first two steps can be correct while the third or fourth is unsafe.

Thus:

```text
correct retirement intent
    != safe retirement-message transport
```

and:

```text
TRIM capability in the interface
    != every supported-looking TRIM command path is trustworthy
```

## E2 — compatibility metadata can govern whether a forgetting request is allowed to use a particular path

Linux's blacklist entry is itself retained operational knowledge:

```text
(model pattern, firmware revision)
    -> disable queued TRIM
```

That host-side compatibility relation changes future command generation. It is not the SSD's logical-to-physical map and it is not the user's payload. Yet it affects whether the system will use a particular mechanism for communicating that some old payload no longer needs to remain current.

This yields a second-order retention relation:

```text
retained compatibility knowledge
    -> constrains command path
    -> constrains how retirement authority is transmitted
    -> indirectly constrains later reclamation behavior
```

If that compatibility knowledge is missing or wrong, the system can select a command path that period kernel maintainers considered capable of corrupting data.

This does **not** mean the Linux blacklist is part of M550 firmware or part of the ATA standard. It is host software policy layered above both.

## E3 — firmware revision changes admissibility, not the meaning of physical erasure

MU02's role in the Linux source is to change whether queued TRIM is trusted for M550.

It does not collapse the later Case-150 chain:

```text
queued TRIM accepted safely
    != stale page physically erased now
    != garbage collection run now
    != erase block reusable now
    != sanitize completed
```

A safer command path only makes the **retirement communication** usable. It does not prove the downstream physical work has happened.

## E4 — maintenance transaction protection is a different durability contract from host-write durability

The 2016 Micron-domain explanation helps separate two kinds of power-loss question that are easy to merge because the product sheet uses one broad feature name.

### A. Existing-data protection during internal maintenance

During GC, the controller may read or relocate already-retained data. A power interruption during such internal activity should not be allowed to corrupt data that were already part of the accepted current state.

### B. New/in-flight host-write durability

Host data still buffered in volatile memory, or not yet committed to NAND, require a different protection contract if the host expects them to survive surprise power failure.

Therefore:

```text
protect old/current data while maintenance is in flight
    !=
make all newly acknowledged volatile writes durable
```

and:

```text
maintenance safety
    != write-cache persistence
```

This distinction matters especially for databases because the latter participates in the durability boundary of `fsync`/flush expectations, while the former protects the correctness of state that was already retained before internal housekeeping began.

## E5 — “no corruption of old data” is stronger than “losing only the operation in progress,” but weaker than full transactional durability

If an internal relocation or page-program sequence can damage previously valid data when power fails, then surprise power loss can retroactively reduce the integrity of an older accepted state.

A data-at-rest protection mechanism can prevent that specific backward damage without preserving every newer in-flight update.

The useful state separation is:

```text
S0 = previously accepted current data
S1 = internal maintenance transformation in progress
S2 = new host writes not yet safely committed

power-loss protection may preserve S0 across interruption of S1
    while still failing to guarantee S2
```

That is a materially different contract from either:

- “no power-loss protection at all,” or
- “full enterprise hold-up that commits every acknowledged volatile write.”

## E6 — field fleets can contain different retention-safety contracts under one model name

Crucial's page calls MU02 mandatory for new production but optional for existing field drives. Linux qualifies the workaround by firmware revision.

Therefore, for a period fleet:

```text
same commercial model family
    != same firmware
    != same queued-TRIM admission policy
```

A model-only inventory is insufficient to infer the host's safe command set.

This is an especially clean example of **retained interpretation context**: the model string alone does not determine the relevant behavior; the firmware revision must travel with it.

---

# Controlled functional comparison

## F1 — Case 04: standards-level TRIM semantics versus Case 150's named implementation defect

Case 04's reused T13 packet establishes the standards/interface distinction among deallocation notification, post-TRIM read semantics, and later physical reclamation.

The M550 evidence adds a different question:

```text
Case 04:
what does the interface allow a correctly executed TRIM to mean?

Case 150 / M550:
when does host software trust this named firmware to execute one queued command form safely?
```

These are complementary, not interchangeable.

A standards contract does not prove every implementation is correct. An implementation blacklist does not rewrite the standard.

## F2 — Case 15: volatile durability handoff versus Case 150 maintenance-currentness safety

Case 15's SSD power-loss work focuses on volatile staging, flush/durability handoff, orderly shutdown, capacitor-backed transfer, and recovery defects.

The M550 slice is narrower:

```text
Case 15:
when has newly submitted state crossed a persistence boundary?

Case 150 M550 maintenance boundary:
can already-current data survive interrupted internal housekeeping,
and can deallocation authority be communicated safely through this firmware/command path?
```

The comparison is functional only. It does not assert a common firmware design.

## F3 — Case 39: mapping reconstruction versus M550 queued-TRIM policy

Case 39 shows that payload may survive while volatile lookup state must be reconstructed from retained mapping/validity evidence.

Here, the Linux blacklist is not map reconstruction evidence. It is **compatibility policy** that controls whether the host will use queued TRIM at all.

Thus:

```text
mapping state
    != compatibility policy
    != deallocation authority
```

All three can affect whether an old physical embodiment remains current or reclaimable, but they sit at different layers.

## F4 — distributed-systems analogy, kept narrow

There is a bounded analogy to systems in which an operation is logically valid but one transport/version path is not currently admissible.

The common functional shape is only:

```text
intent exists
    + mechanism nominally exists
    + compatibility/currentness qualification fails
    -> operation path withheld
```

This does not make Linux libata a consensus protocol, nor queued TRIM a distributed commit.

---

# Philosophical interpretation

The M550 slice sharpens one repository-wide proposition: **forgetting is not merely a negative absence; it can require a trusted positive act whose authority and transport must themselves be maintained.**

But this remains an interpretation layered over the engineering record.

The historical actors here discuss:

- queued TRIM;
- firmware revisions;
- corruption;
- blacklist/workaround policy;
- power-loss protection;
- garbage collection;
- cache protection.

They do not describe these mechanisms in philosophical language about forgetting, authority, or memory.

The bounded philosophical reading is:

> A system can be technically capable of forgetting while temporarily refusing one route by which permission to forget would be communicated. The ability to retire state therefore depends not only on the existence of a deletion operation, but also on retained knowledge about which implementation/path is admissible now.

The second bounded reading is:

> Preservation can be transactional rather than merely static: protecting an already-retained state may require ensuring that a maintenance transformation cannot damage the past state if interrupted, even when the system does not guarantee the survival of every newer in-flight write.

Neither claim should be back-projected as period vocabulary.

---

# Explicit non-claims

This packet does **not** claim that:

1. Crucial or Micron invented TRIM, queued TRIM, SSD garbage collection, or SSD power-loss protection.
2. M550 was the first SSD with a queued-TRIM defect.
3. `ATA_HORKAGE_NO_NCQ_TRIM` disables all TRIM.
4. ordinary non-queued TRIM was proven flawless on every M550 revision.
5. MU02 makes every M550 operation bug-free.
6. MU02 proves physical erase occurs synchronously with TRIM.
7. a successful TRIM proves garbage collection has run.
8. a successful TRIM proves stale NAND is unrecoverable.
9. queued TRIM failure necessarily means the same internal failure mechanism on M500, M510, M550, and MX100.
10. the Linux blacklist reveals proprietary M550 FTL internals.
11. the host blacklist is stored on the SSD.
12. the host blacklist is part of ATA/T13 normative semantics.
13. a firmware revision string alone proves the binary image has not been modified or corrupted.
14. every field M550 received MU02.
15. “mandatory cut-in” for new production means every retail drive immediately shipped with MU02 worldwide.
16. Crucial's current support-page displayed 2018 date is the true first-release date for MU02.
17. the 2015 Linux commit identifies the exact day MU02 first became publicly downloadable.
18. the 2016 Micron-domain mailing-list message is equivalent in evidential weight to a revision-controlled product manual.
19. M550 capacitors preserve the entire volatile DRAM cache.
20. M550 provides the same surprise-power-loss durability contract as Intel DC S3700 or an enterprise SSD with full in-flight-data hold-up.
21. all data read during every GC implementation are always copied or rewritten.
22. a protected GC operation means no maintenance progress can be lost on power failure.
23. preserving old data across interrupted maintenance proves exact worker/cursor resume.
24. data-at-rest protection is the same as filesystem/database transaction durability.
25. host `fsync` semantics can be inferred solely from the M550 product feature list.
26. firmware trust is identical to logical currentness.
27. deallocation authority is identical to physical erasure authority.
28. physical erasure is identical to sanitization.
29. compatibility policy is identical to device mapping metadata.
30. this implementation history establishes a direct genealogy from M550 to later Micron SSD firmware.

---

# What this slice adds to Case 150

Before this packet, Case 150 already had:

```text
logical retirement
    != TRIM knowledge
    != GC execution
    != physical reclaim
```

This packet adds two intermediate boundaries:

```text
logical retirement intent
    != command-path admissibility
    != safely received retirement authority
```

and:

```text
internal maintenance protected against retroactive corruption
    != full durability of new/in-flight host writes
```

A fuller bounded chain is now:

```text
host decides data are no longer needed
    -> host selects a deallocation command path
    -> model/firmware compatibility policy admits or withholds queued TRIM
    -> device safely receives retirement information
    -> controller updates validity/currentness knowledge
    -> GC may later relocate still-live data
    -> maintenance must not corrupt already-current state if interrupted
    -> old block eventually becomes erase-eligible / erased / reusable
```

No source inspected here proves that all of those arrows are one synchronous transaction.

---

# Remaining work

This slice closes the bounded named-device debt **“M550 host/deallocation path can be firmware-qualified rather than model-only.”** It also adds a named-source boundary for maintenance-data protection versus full cache durability.

Still open:

- the exact M550 MU01 queued-TRIM failure mechanism;
- original kernel Bugzilla 71371/81071 reporter traces and reproducer details beyond surviving commit summaries;
- a revision-controlled Micron/Crucial technical note that specifies M550's capacitor/GC transaction behavior in more detail than the 2016 mailing-list explanation;
- controlled MU01-versus-MU02 hardware experiments with queued and non-queued TRIM;
- power-cut fault injection specifically during M550 garbage collection;
- whether GC progress/cursor/transaction metadata survives or is reconstructed after power loss;
- exact victim-selection and live-page publication ordering;
- raw-NAND observation of stale embodiments before/after TRIM and GC;
- broader queued-TRIM implementation genealogy, which belongs primarily in `tmzncty/computing-archaeology`.

A fresh companion-repository search for `M550 queued TRIM MU02` found no dedicated packet to reuse, so this file keeps only the retention-specific implementation/authority boundary rather than attempting a broad ATA/SSD history.