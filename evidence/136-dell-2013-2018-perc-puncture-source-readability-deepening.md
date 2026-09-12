# Evidence 136B — Dell PERC degraded-rebuild source unreadability and RAID puncture

## Status

**`grounded`** — bounded primary-source deepening for Case 136. This record asks what happens when rebuild is scheduled and progressing but a surviving source contribution required for reconstruction is unreadable. It does **not** estimate universal URE probability, generalize RAID 5 behavior to RAID 6, or infer undocumented PERC firmware internals.

## Scope question

Case 136 already separates rebuild-rate policy from repair obligation and rebuild execution. This slice asks a narrower question:

> On documented Dell PERC systems, can a degraded rebuild continue even when a local stripe cannot be reconstructed because a surviving source contribution is unreadable, and what state remains afterward?

## Source set and provenance

### Dell OpenManage Server Administrator Storage Management User's Guide — March 2013

- Dell Inc., *OpenManage Server Administrator Storage Management User's Guide*, March 2013.
- Official Dell-hosted manufacturer PDF.
- Relevant sections: `A Rebuild Completes with Errors` (PDF page 299) and `Receive a “Bad Block” Alert with “Replacement,” “Sense,” or “Medium” Error` (PDF page 304).
- <https://dl.dell.com/manuals/all-products/esuprt_electronics/esuprt_software/esuprt_ent_sys_mgmt/dell-opnmang-srvr-admin-mngd-das_user's%20guide_en-us.pdf>
- Accessed 2026-09-12.

### Dell EMC PowerEdge Servers Troubleshooting Guide — November 2018, Rev. A11

- Dell EMC, *PowerEdge Servers Troubleshooting Guide*, Rev. A11, November 2018.
- Official Dell-hosted manufacturer PDF.
- Relevant section: `RAID puncture`, PDF pages 97–99.
- <https://dl.dell.com/manuals/common/servertroubleshootingguide_en.pdf>
- Accessed 2026-09-12.

### Current Dell knowledge-base continuity witness

- Dell, `PowerEdge: How to fix Double Faults and Punctures in RAID Arrays`.
- <https://www.dell.com/support/kbdoc/en-us/000139251/double-faults-and-punctures-in-raid-arrays>
- Used only as a maintained terminology/operational-continuity witness, not as first-use or invention evidence.

## Historical record

### March 2013: rebuild can complete while a damaged portion remains unrestored

Dell's March 2013 OpenManage guide has a section titled `A Rebuild Completes with Errors` for PERC 4/SC, 4/DC, 4e/DC, 4/Di, 4e/Si, and 4e/Di. It says a rebuild may complete successfully while reporting errors when part of the disk containing redundant/parity information is damaged: healthy portions can be restored while the damaged portion cannot. Alert 2163 can accompany this state.

The same section says that if backup of the degraded virtual disk encounters errors, user data has been damaged and cannot be recovered from the virtual disk; recovery then depends on an earlier backup.

This supplies a bounded manufacturer documentation floor by **March 2013** for:

> **rebuild completion status != proof that every damaged region was reconstructed.**

This is not an invention-priority claim.

### March 2013: damaged media discovered during degraded operation can cross a recoverability boundary

The guide says medium/bad-block damage can be discovered during consistency check, rebuild, virtual-disk format, or I/O. For alerts 2146–2150 received during rebuild or while the virtual disk is degraded, Dell says damaged data cannot be recovered from that disk without restoration from backup.

Thus a rebuild task can exist and run while not every source region needed by reconstruction remains readable.

### November 2018: Dell explicitly names `RAID puncture` / `rebuild with errors`

Dell's November 2018 PowerEdge troubleshooting guide defines `RAID puncture` as a PERC feature and also calls it `rebuild with errors`. When a double fault leaves insufficient redundancy to recover an impacted stripe, the controller creates a puncture in that stripe and allows rebuild to continue. The guide says affected stripe data is lost and future access to the affected data continues to encounter uncorrectable errors.

### Concrete RAID 5 example: one unavailable member plus one unreadable surviving contribution

Dell gives a three-member RAID 5 example: drive 0 fails and is replaced; drives 1 and 2 supply remaining data/parity; when rebuild reaches a stripe where drive 1 has a data error, insufficient information remains to reconstruct the missing stripe contribution. That stripe is unrecoverable/lost and becomes punctured during rebuild.

The second damaging condition is not another whole-drive failure. A local unreadable source region can consume the contribution the degraded stripe still needed.

> **latent surviving-source defect != second whole-device failure**, even though either can remove a contribution required by a particular reconstruction.

### Global redundancy can be restored while local payload loss remains

The 2018 guide says puncturing can restore redundancy and return the array to an `optimal` state while the affected stripe's data remains lost.

This directly separates:

- **rebuild complete != every payload byte recovered**;
- **redundancy restored != every prior stripe reconstructable**;
- **array optimal != no data loss has occurred**.

### Post-puncture consistency check is not lost-data recovery

Dell says Check Consistency after a puncture is induced does not resolve it. The guide recommends regular Check Consistency, especially before drive replacement when possible. Its post-puncture remedy is destructive at array scope: preserve recoverable data, delete/recreate and fully initialize the array, verify consistency, then restore data.

That is an operational recovery/reset path, not evidence of secure sanitization or forensic erasure.

## Engineering reconstruction

The following is a project reconstruction of documented relations, not a claim about undocumented firmware internals:

```text
member failure
    -> degraded array / repair obligation
    -> replacement destination available
    -> rebuild admitted and scheduled
    -> read surviving stripe contributions
        -> sufficient/readable: reconstruct missing contribution
        -> required surviving contribution unreadable and redundancy exhausted:
             local stripe reconstruction fails
             -> affected stripe punctured
             -> global rebuild can continue
    -> redundancy may later be restored / array may return optimal
       while punctured payload remains lost
```

### Source readability is a constitutive repair input

Case 136 already has scheduling state (`rebuild rate`) and task/progress state. This evidence adds an independent requirement:

> **rebuild rate / repair priority != source readability.**

A useful decomposition is:

```text
repair obligation
+ replacement destination
+ surviving-source readability/reconstructability
+ admitted scheduling/resources
-> possible reconstruction work
```

None alone proves successful recovery of every stripe.

### Progress is not reconstructable coverage

The Dell record permits global rebuild continuation after a local unrecoverable stripe is punctured.

> **rebuild progress/completion != reconstructable coverage.**

### Puncture is a retained negative condition, not a deletion primitive

Dell says accesses to punctured data continue to encounter uncorrectable errors and eliminating the puncture requires recreating the array and restoring data. At project level this supports treating puncture as a retained **negative condition / error relation** on an affected logical extent: later access remains constrained by an earlier failed reconstruction event.

This does not identify whether that relation is encoded in a BBM table, parity bytes, controller metadata, member media, or a combination.

### Proactive readability qualification != rebuild

A Check Consistency operation while the array is still optimal can expose conditions before another member loss consumes redundancy margin.

> **proactive integrity/readability maintenance != reconstruction after member loss.**

## Functional comparisons — not mechanism identity

### Case 18 — ZFS scrub; Cases 101 / 102 — medium scan and patrol read

The functional analogy is that proactive observation can expose latent integrity/media defects while enough redundancy remains to correct or retire them. Dell PERC Check Consistency, ZFS scrub, medium scan, and patrol read are not thereby the same mechanism.

### Case 94 — RAID 6 P/Q boundary

Dell's worked example is RAID 5. Case 94 is a counterexample to over-generalization because RAID 6 has a different erasure margin.

> **RAID 5 single-parity reconstruction boundary != universal RAID failure boundary.**

### Case 96 — dRAID / reduced repair exposure

Faster reconstruction can reduce time spent with diminished redundancy, but speed and source readability remain separate variables.

> **shorter degraded interval != certification that surviving source regions are readable.**

## Prior-art and chronology boundary

Safe chronology:

- by **March 2013**, Dell publicly documented `A Rebuild Completes with Errors` for named PERC 4 controllers;
- by **November 2018**, Dell explicitly used `RAID puncture` and equated it with `rebuild with errors`, including a concrete RAID 5 degraded-rebuild example.

These are documentation floors only. They do not establish Dell invention, first industry use of `puncture`, identical implementation across PERC generations, or direct implementation genealogy.

## Stop conditions / rejected upgrades

Do not upgrade this record without new evidence into claims that:

- `puncture == sanitize` or secure deletion;
- `array optimal == no data loss`;
- post-puncture Check Consistency recovers the lost stripe;
- one unreadable surviving block equals a second whole-drive failure;
- the 2013 guide proves Dell invented the feature or phrase;
- the 2018 wording proves identical firmware implementation across controller generations;
- the RAID 5 example applies automatically to RAID 6 or other codes;
- rebuild-rate priority itself causes or prevents punctures;
- these manuals establish universal URE probability, failure rate, correlation, or quantitative rebuild-risk curves;
- destructive array recreation proves forensic erasure of previous physical embodiments.

## Remaining evidence debt

- controller-generation-specific telemetry and persistence mechanism for punctured/error locations;
- named RAID 6 / multi-parity PERC behavior;
- cross-vendor behavior and terminology;
- probabilistic and correlated read-error models tied to named media/controller generations;
- independent fault injection reproducing local source unreadability during rebuild;
- interaction among rebuild scheduling, patrol read/check consistency, cache policy, and media-error handling;
- implementation history before the March 2013 documentation floor.

## Related-repository check

Fresh searches of `tmzncty/computing-archaeology` for `PERC puncture` and `RAID rebuild unrecoverable read error` returned no dedicated overlapping module during this round.

Division of labor:

- `technical-retention`: repair obligation, scheduling, source readability, local reconstruction failure, retained error condition, and restored redundancy;
- `computing-archaeology`: broader controller genealogy, prior terminology, firmware lineage, patrol-read/consistency-check history, and quantitative historical reconstruction if later developed.
