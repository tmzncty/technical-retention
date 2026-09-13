# Evidence 111 — NetApp ONTAP Long-Power-Off Data-Removal and Field-Failure Deepening

## Status

**`bounded deepening complete`** for the public NetApp support record inspected on **2026-09-14**.

This slice deepens Case 111 with a genuinely separate vendor support record after the IBM/Lenovo provenance check showed why a second vendor-branded webpage cannot automatically be counted as independent engineering evidence.

The bounded question is:

> When NetApp warns about enterprise SSDs remaining unpowered for months, does it prescribe the same periodic powered-maintenance topology already documented by IBM and Dell, or a different operator intervention?

The answer in the accessible NetApp record is different: for an intended power-off interval greater than two months, NetApp's public ONTAP support text points to SU490 and a drive-preparation path that says to **remove all data from the drives**. That is a useful negative control on the idea that one shared retention-risk background implies one universal field-maintenance schedule.

This evidence does **not** claim that the gated SU490 bulletin has been fully inspected. Only public NetApp text and public support-page metadata are used below.

## Sources inspected

### NetApp Knowledge Base — extended-power-off recommendation

- _What are recommendations when powering off ONTAP Storage with Solid-State Drives (SSD) for an extended period of time?_
- <https://kb.netapp.com/on-prem/ontap/OHW/OHW-KBs/What_are_recommendations_when_powering_off_ONTAP_Storage_with_Solid_State_Drives_SSD_for_an_extended_period_of_time>
- Public page; observed 2026-09-14.
- Applies to `ONTAP`, `Storage maintenance`, and `Solid-State Drives (SSD)`.
- The page explicitly directs readers to customer bulletin **SU490** for SSD best practices.

### NetApp Knowledge Base — long-power-off preparation command path

- _How to use the scsi format command to prepare SSD drives for being powered off for long periods_
- <https://kb.netapp.com/on-prem/ontap/OHW/OHW-KBs/How_to_use_the_scsi_format_command_to_prepare_SSD_drives_for_being_powered_off_for_long_periods>
- Public landing text; observed 2026-09-14.
- Applies to `ONTAP 9`, `AFF/FAS Systems`, `Capacity Flash NVMe SSD`, `NVMe SSD`, and `SAS SSD`.
- Full procedure is authentication-gated; only the public description is treated as evidence here.

### NetApp Knowledge Base — graceful shutdown integration

- _How to perform graceful shutdown and power up of all ONTAP nodes in a cluster_
- <https://kb.netapp.com/on-prem/ontap/OHW/OHW-KBs/How_to_perform_graceful_shutdown_and_power_up_of_all_ONTAP_nodes_in_a_cluster>
- Public page; observed 2026-09-14.
- Applies to ONTAP 9 AFF/FAS systems, excluding MetroCluster configurations.
- Its requirements section routes SSD users to SU490 before ordinary shutdown/power-up work.

### NetApp Knowledge Base — named-drive field symptom

- _ONTAP SSD TPM3 and TPM4 drives fail with "Failed-Unsupported" after being off for an extended period_
- <https://kb.netapp.com/on-prem/ontap/OHW/OHW-KBs/X358_TPM4V3T8AME_Drives_failed_with_Failed_Unsupported_after_disks_powered_on>
- Public issue section; observed 2026-09-14.
- Applies specifically to `X358_TPM4V3T8AME`, `X357_TPM4V3T8AME`, and `X365_TPM3V1T6AMD` in FAS/AFF systems.
- The resolution/root-cause portion is authentication-gated and is therefore **not** reconstructed here.

### SU490 title witness

NetApp's public KB pages identify the support bulletin as SU490. A current Lenovo NetApp support-bulletin index exposes the longer title:

- `SU490: [Impact: Critical] SSD Best Practices: Avoid risk of drive failure and data loss if powered off for more than two months`
- <https://www.lenovonetapp.com/technical-service/support/support-bulletin/support-bulletin-list.html>

This secondary index is used only to expose the bulletin title. It is not used to invent inaccessible SU490 body text.

## Historical / product record

### H/P — NetApp's public ONTAP guidance frames long power-off as a NAND-retention risk

The public extended-power-off KB says that NAND-flash SSDs slowly lose stored charge while left unpowered for long periods. It paraphrases a JEDEC source as saying SSDs should not remain unpowered for more than roughly **2–3 months**, because data may not be recoverable when power returns.

The same page immediately adds that time-to-risk varies with:

- the amount of wear on the SSD;
- the temperature of the environment in which the SSD is stored.

For this repository, that wording is retained as a **NetApp support interpretation of a JEDEC retention relation**. It is not promoted into an exact normative JEDEC clause. Case 76 remains the canonical standards-level grounding.

Therefore:

```text
NetApp support paraphrase of JEDEC
    !=
verbatim normative JESD218 requirement
```

and:

```text
2–3 month support horizon
    !=
deterministic individual-drive failure clock
```

### H/P — for intended power-off beyond two months, a public NetApp page says to remove all data

The public description of _How to use the scsi format command to prepare SSD drives for being powered off for long periods_ states:

> As described in Support Bulletin SU490, if removing power from Enterprise SSDs for greater than two months, remove all data from the drives to avoid impact to SSD usability in the future.

The accessible page therefore exposes a different intervention topology from the IBM and Dell periodic-powered-maintenance records already grounded in Case 111.

At the public policy level, NetApp exposes:

```text
intended long power-off > two months
    -> remove all data / prepare drives before storage
```

rather than publishing, in this accessible page, a rule of the form:

```text
power off for N months
    -> power on for M weeks
    -> resume long unpowered storage with payload retained
```

That distinction is the main result of this deepening.

### H/P — the preparation guidance spans SAS and NVMe SSD contexts

The same public NetApp page lists:

- ONTAP 9;
- AFF/FAS systems;
- Capacity Flash NVMe SSD;
- NVMe SSD;
- SAS SSD.

This is useful because the operator policy is not presented only as one legacy SAS-drive note. It is a system-support rule spanning multiple SSD interface classes in the listed ONTAP context.

It does **not** prove identical controllers, NAND generations, format semantics, or internal retention mechanisms across those classes.

### H/P — SU490 is integrated into ordinary ONTAP shutdown workflow

The public graceful-shutdown article describes routine reasons to shut down an ONTAP cluster, including:

- scheduled site power outage;
- data-center maintenance;
- physical system move;
- preparation for future repurposing.

In its requirements, it separately says that when SSDs are present the operator should refer to **SU490**.

This matters because the long-power-off rule is not isolated from system operations. NetApp integrates the SSD-retention warning into the normal shutdown decision path.

The bounded historical relation is:

```text
ordinary system shutdown procedure
    + SSD present
    -> additional retention-specific support branch
```

That is operator-policy evidence, not firmware-implementation evidence.

### H/P — NetApp exposes a named-drive field symptom after storage / repurposing

A separate public NetApp KB records that some customers experienced **multiple drive failures after power-on** when drives were brought out of storage and repurposed. It narrows the article to three specific drive identifiers:

- `X358_TPM4V3T8AME`;
- `X357_TPM4V3T8AME`;
- `X365_TPM3V1T6AMD`.

The public issue text says the drives can appear in `sysconfig -a` as `0.0GB 0B/sect (Failed-Unsupported)` after power-up.

This is valuable as a bounded field-observation witness because it shows that NetApp's long-offline concern was not expressed only as an abstract retention slide or generic best practice.

But the public portion does **not** establish:

- the exact duration for which those drives were stored;
- the drive wear state before storage;
- storage temperature;
- whether user payload bits themselves became uncorrectable;
- whether controller metadata, firmware state, NAND payload, interface initialization, or another mechanism caused `Failed-Unsupported`;
- whether SU490's data-removal preparation would have prevented every such occurrence.

Therefore:

```text
field failure after extended storage
    !=
proved NAND-payload retention mechanism
```

and:

```text
Failed-Unsupported
    !=
automatically "user data charge leaked away"
```

The symptom is retained exactly at the service/interface layer where NetApp exposes it.

## Engineering reconstruction

### E — same broad risk does not imply one maintenance topology

Case 111 already has two powered-maintenance styles:

- IBM: after two months off, power the system for a product-dependent minimum interval;
- Dell: periodically power drives for a minimum interval, or read all used NAND to trigger retention tasks.

NetApp's accessible ONTAP support path contributes a third operator strategy:

- for planned power-off longer than two months, **remove all data from the drives** and prepare them for storage.

The defensible cross-vendor relation is therefore:

```text
same broad offline-retention concern
    !=
same operator intervention topology
```

More specifically:

```text
retain payload + periodically restore maintenance opportunity
    !=
remove payload before long unpowered storage
```

The two policies solve different operational problems. The former tries to preserve a live data-bearing system across an offline interval; the latter removes the requirement that those drives continue to carry the retained user payload during the long storage interval.

### E — an operator can reduce retention obligation instead of extending maintenance availability

The NetApp path highlights a distinction that the IBM/Dell evidence alone does not expose as sharply.

A retention problem can be managed by changing either side of the obligation:

```text
A. preserve payload on this carrier
   -> periodically restore powered maintenance opportunity

B. eliminate payload-retention obligation on this carrier
   -> evacuate/remove data before prolonged storage
```

This is an engineering reconstruction of the runbooks, not NetApp's historical terminology.

It is useful because it prevents an overly narrow model in which every flash-retention policy must be a refresh cadence.

### E — `remove all data` is not automatically a sanitization claim

The public NetApp page is titled around the `scsi format` command, but the detailed procedure is gated. The accessible sentence says to remove all data to avoid future SSD-usability impact.

That supports an operational preparation claim. It does **not** by itself prove:

- cryptographic erase;
- NIST purge-level assurance;
- overwrite of every physical NAND embodiment;
- destruction of remapped/overprovisioned copies;
- equivalence to NVMe Sanitize;
- forensic irrecoverability.

Therefore:

```text
long-storage data removal / drive preparation
    !=
sanitization assurance
```

Case 44 remains the place where sanitize command semantics and recovery authority are grounded.

### E — interface label does not disclose physical maintenance mechanism

The preparation article's title exposes a SCSI-format command path while its Applies To list includes NVMe as well as SAS SSDs.

Without the gated procedure, the repository should not infer how ONTAP maps that administrative operation onto each listed device class.

Thus:

```text
operator command label
    !=
proved identical device-level command on every SSD class
```

and:

```text
same support policy across SAS/NVMe
    !=
same controller implementation
```

### E — field service state and retained payload correctness are separate observations

The named-drive KB exposes a post-storage service symptom: multiple devices can return as `Failed-Unsupported` and report no normal capacity.

That is stronger than saying only that a future bit-error probability increased, but weaker than proving which retained physical state failed.

For technical-retention decomposition:

```text
payload charge state
controller / device metadata
firmware / boot state
device enumeration / support state
system admission state
```

are distinct possible layers.

The public field report tells us the final system-visible admission/service state; it does not resolve the lower-layer cause.

### E — independent-vendor evidence should be counted by provenance, not page count

The previous Case 111 provenance deepening showed why Lenovo's near-matching Storwize guidance should not simply be counted as a new independent vendor sample.

NetApp is more useful here because the support material belongs to a distinct ONTAP/AFF/FAS operational context and, crucially, exposes a **different** intervention topology rather than merely echoing IBM wording.

This supports:

```text
independent evidence value
    depends on provenance + distinct engineering context
    not merely on number of branded webpages
```

That still does not prove that NetApp's individual SSDs use NAND or controllers unrelated to every drive sold in other vendors' systems. The independence claim here is about the **system-vendor support/runbook record**, not semiconductor supply-chain independence.

## Cross-case comparison

### Case 76 — JESD218 qualification

Case 76 owns the standards-level retention/endurance relation. NetApp's public KB cites/paraphrases JEDEC, but this evidence deliberately does not use NetApp's wording as a substitute for the standard.

Functional relation:

```text
qualification relation
    !=
field support horizon
    !=
operator storage-preparation policy
```

### Case 111 — IBM / Dell powered-maintenance guidance

IBM and Dell demonstrate that restoring powered time can be scheduled as retention infrastructure. NetApp adds the negative control that an enterprise vendor may instead tell the operator to remove data before an intentionally long power-off interval.

Therefore:

```text
shared risk regime
    != universal power-up cadence
    != universal maintenance action
```

### Case 44 — sanitize / erase semantics

The NetApp public phrase `remove all data` is purpose-specific: preparing SSDs for a long unpowered interval to avoid future usability impact.

Case 44 asks a different question: what device-level sanitize operation occurred, what state records it, and what recovery/assurance semantics follow.

Only a functional contrast is asserted:

```text
remove data for retention-risk avoidance
    !=
prove sanitization
```

No genealogy or implementation identity is claimed.

### Existing NetApp rated-life deepening

`111-netapp-rated-life-offline-retention-telemetry-deepening.md` grounds another NetApp relation: ONTAP rated-life telemetry changes replacement/admission policy because an SSD at 100% rated life may no longer be trusted for long powered-off retention.

The present evidence adds a different axis:

```text
wear-state admission policy
    !=
planned-long-shutdown preparation policy
```

They are complementary, not duplicate evidence.

## Historical record vs engineering reconstruction vs analogy vs interpretation

### Historical / product record

Directly supported by the inspected NetApp pages:

- public ONTAP guidance directs SSD users to SU490;
- it says long unpowered NAND retention depends on wear and storage temperature;
- it paraphrases a JEDEC-derived 2–3 month risk horizon;
- a public preparation article says that for enterprise SSD power-off longer than two months, operators should remove all data to avoid future SSD-usability impact;
- that article lists ONTAP 9, AFF/FAS, Capacity Flash NVMe SSD, NVMe SSD, and SAS SSD;
- the ordinary graceful-shutdown article explicitly routes SSD systems to SU490;
- a named-drive KB reports multiple `Failed-Unsupported` drive failures after drives were brought out of storage and repurposed.

### Engineering reconstruction

Project-level decomposition supported by those records:

- NetApp's accessible long-offline mitigation changes the **payload-retention obligation**, rather than documenting a periodic powered refresh cadence;
- field service/admission failure should be separated from direct proof of user-payload bit loss;
- `remove data` and `sanitize` are different claims;
- system-vendor support provenance should be separated from component supply-chain identity.

### Functional analogy

Functional comparison only:

- IBM/Dell periodic powered maintenance;
- NetApp pre-storage payload removal;
- Case 76 standards qualification;
- Case 44 sanitize assurance.

No direct technical genealogy among these mechanisms is asserted.

### Philosophical interpretation

A limited project interpretation is that retention obligations can be preserved not only by repeatedly repairing a carrier, but also by **moving the thing that must persist elsewhere before the carrier enters a hostile interval**.

That is not NetApp's historical vocabulary and is not evidence for a general philosophy of identity. It is retained only as a cross-case conceptual aid after the engineering distinctions are established.

## Explicit non-claims

This evidence does **not** claim that:

1. every NetApp SSD loses data after exactly two or three months without power;
2. NetApp's public 2–3 month sentence is a verbatim normative JESD218 clause;
3. the current KB publication date is known merely from its present web page;
4. the full authenticated SU490 bulletin has been inspected;
5. the inaccessible SCSI-format procedure can be reconstructed from its title;
6. `scsi format` here is equivalent to NVMe Sanitize;
7. `remove all data` proves NIST purge/clear assurance or forensic irrecoverability;
8. removing payload physically rejuvenates NAND cells;
9. periodic power-up would be ineffective on all NetApp SSDs;
10. NetApp's support policy proves one controller implementation across SAS and NVMe devices;
11. the three named TPM3/TPM4 drive families fail for the same lower-level reason;
12. `Failed-Unsupported` directly proves user NAND payload became uncorrectable;
13. the field failures occurred at a known wear state, storage temperature, or exact offline duration;
14. every drive in AFF/FAS systems is covered by the named-drive field article;
15. a distinct NetApp system-vendor support record proves component-vendor or NAND-fab independence;
16. IBM, Dell, and NetApp derived their runbooks from one another;
17. similarity of month-scale horizons establishes a shared hidden firmware algorithm;
18. the accessible public record is sufficient to validate the runbook experimentally.

## Claim ledger

| Claim | Type | Strength / boundary |
| --- | --- | --- |
| NetApp currently routes ONTAP SSD extended-power-off questions to SU490 | H/P | strong; public NetApp KB |
| NetApp says offline retention risk varies with wear and storage temperature | H/P | strong; public NetApp KB |
| NetApp public support text uses a 2–3 month JEDEC-derived horizon | H/P | strong as NetApp wording; not treated as the normative standard itself |
| For >2 months intended power-off, NetApp's public preparation page says to remove all data | H/P | strong; exact public description |
| The preparation page applies across listed SAS and NVMe SSD categories | H/P | strong for support scope; weak for implementation identity |
| Graceful ONTAP shutdown explicitly branches SSD users to SU490 | H/P | strong |
| Named TPM3/TPM4 drives have a public post-storage `Failed-Unsupported` field report | H/P | strong for the reported symptom; cause remains unresolved in public text |
| NetApp exposes a different operator intervention topology from IBM/Dell periodic powered time | E | strong bounded comparison |
| Data removal can eliminate the requirement that the stored drives retain the live user payload during long storage | E | strong operational reconstruction |
| `remove all data` proves secure sanitization | X | rejected |
| post-storage `Failed-Unsupported` proves NAND user-bit charge loss | X | rejected |
| all enterprise SSD vendors should use NetApp's preparation policy | X | rejected |
| shared month-scale horizon proves shared mechanism | X | rejected |

## Remaining evidence debt

1. Obtain the full authenticated **SU490** text and preserve its publication/revision chronology.
2. Recover a public or archival revision history for the two NetApp long-power-off KB pages rather than inferring first publication from current search-engine metadata.
3. Inspect the complete `scsi format` preparation procedure and determine exactly what ONTAP sends to SAS versus NVMe devices.
4. Determine whether the preparation path changes only logical allocation state, performs a format/erase, or triggers additional drive-local maintenance; do not infer this from the title.
5. Recover public root-cause/resolution evidence for the three TPM3/TPM4 `Failed-Unsupported` drive families.
6. Find telemetry or fault-injection traces covering long-offline return-to-service and showing which layer first loses authority: payload ECC, controller metadata, firmware, device enumeration, or system admission.
7. Map the affected named drive families to controller/NAND vendors only from primary product or teardown evidence.
8. Find a genuinely independent vendor that documents a **non-destructive periodic power-up** schedule, to extend the IBM/Dell powered-maintenance comparison without OEM/provenance ambiguity.
9. Test whether wear-state thresholds from the existing NetApp rated-life evidence alter SU490's storage-preparation advice.
10. Keep standards archaeology in Case 76 and generic SSD/controller history in `computing-archaeology`; no duplicate broad history is needed here.

## computing-archaeology reuse check

A repository search of `tmzncty/computing-archaeology` for `SU490` and `SSD power off retention` returned no dedicated technical-history module to reuse in this slice. The present file therefore records only the Case-111-specific retention relation rather than creating a new generic SSD history.
