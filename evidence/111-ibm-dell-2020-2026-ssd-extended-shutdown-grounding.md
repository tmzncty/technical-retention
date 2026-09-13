# Evidence 111 — IBM / Dell Enterprise-SSD Extended-Shutdown Guidance, 2020–2026

## Scope

This record grounds a narrow operational-retention case: two infrastructure vendors publish guidance for enterprise SSD/NVMe systems that may remain powered off long enough for power-off retention to become an operator concern.

It does **not** independently reproduce JESD218; that standards relation is already grounded in Case 76. It does not infer undocumented firmware algorithms from support prose.

Cadence/source-provenance follow-on: [`111-ibm-lenovo-2020-2021-cadence-provenance-deepening.md`](111-ibm-lenovo-2020-2021-cadence-provenance-deepening.md). That deepening shows that IBM itself published different minimum powered-run durations for different product contexts while invoking the same broad retention background, and that Lenovo's later near-matching Storwize-family guidance should not be counted naively as an independent cross-vendor witness.

Independent-vendor intervention-topology follow-on: [`111-netapp-ontap-long-poweroff-data-removal-deepening.md`](111-netapp-ontap-long-poweroff-data-removal-deepening.md). NetApp's public ONTAP support path supplies a distinct system-vendor witness: for intended enterprise-SSD power-off beyond two months, the accessible preparation guidance says to remove all data rather than publishing another IBM/Dell-style periodic powered-maintenance cadence. The same deepening records a named-drive post-storage `Failed-Unsupported` field symptom while refusing to infer its lower-level cause from the public issue text.

## Source 1 — IBM Support: “Potential for SSD data loss after extended shutdown”

**Current page:** <https://www.ibm.com/support/pages/potential-ssd-data-loss-after-extended-shutdown>

**Support-content mirror:** <https://supportcontent.ibm.com/support/pages/potential-ssd-data-loss-after-extended-shutdown>

**Publication metadata observed:**

- surviving support-content mirror: `Created by Richard Hopkins on Wed, 12/16/2020 - 09:26`;
- current IBM page: `Modified date: 28 March 2023`;
- UID: `ibm16382908`.

### Directly grounded record

The current IBM page states:

- JEDEC enterprise SSD retention background of a minimum **three months at 40 °C**;
- after extended power-off there is potential for data loss and/or drive failures;
- a system and its enclosed drives should be **powered up at least two weeks after two months of system power off**;
- drives reporting end-of-life status should not be powered off for extended periods;
- the powered-off environment should remain below 40 °C;
- regular/recent backup is recommended before extended shutdown.

The affected-product metadata spans IBM storage products including Storwize, SAN Volume Controller, and FlashSystem families. The present case does not claim the same physical SSD model or controller implementation across all of them.

### Evidence boundary

IBM's wording is support/runbook guidance. It does not publish:

- controller firmware source;
- a NAND-page rewrite trace;
- proof that all maintenance completes in exactly two weeks;
- raw qualification data;
- a deterministic three-month failure threshold.

The 16 December 2020 mirror timestamp is used as a public guidance floor, not an invention date for the underlying technical mechanism.

---

## Source 2 — Dell Technologies Support article 000198930

**Document:** _PowerEdge: Data Retention Occur with SSD or Nvme Drives Due to Prolonged Power off_

**URL:** <https://www.dell.com/support/kbdoc/en-us/000198930/ssd-data-retention-considerations-when-powering-off-systems-for-a-prolonged-duration>

**Article properties observed:**

- Article Number: **000198930**;
- Article Type: **Solution**;
- Version: **3**;
- Last Modified: **14 May 2026**.

### Exact semantic locations inspected

`Symptoms` / `Cause`:

- Dell says enterprise SSD/NVMe retains data via NAND voltage levels;
- it says drive firmware performs background tasks as part of data retention;
- while powered, SSD/NVMe devices carry out data-retention tasks and wear-leveling can occur while idle or under host I/O;
- extended power-off prevents those tasks from running.

`Resolution`:

- Dell invokes JESD218/JESD219 and a **three-month** power-off interval at maximum rated endurance;
- it separately lists P/E-cycle/TBW state, active-use temperature, and power-off temperature as retention-relevant conditions;
- it recommends powering SSD/NVMe with user data **once every 2.5 months for a minimum duration of three weeks** so background tasks can complete;
- it states larger capacities require longer powered duration;
- it gives an alternative: **read all used NAND cells** to trigger data-retention tasks, recommended for larger drives;
- it recommends decommissioning/backing up servers stored powered off longer than three months until they can return to production use.

### What this source directly grounds

**H/P:** Dell currently documents an operator-facing relation among extended power-off, background-retention opportunity, powered run time, capacity, and a read-triggered maintenance path.

**E:** the document makes `power restored` distinguishable from `background retention work given time/opportunity to complete`.

**E:** because a read sweep is described as triggering retention tasks, the host-visible read operation and the hidden maintenance action should be modeled separately.

### Evidence boundary

The inspected page does not disclose:

- whether the retention task rewrites every page, migrates selected blocks, adjusts read references, or uses some other controller policy;
- thresholds for selecting cells/blocks;
- maintenance-completion telemetry;
- a formula relating capacity to minimum powered duration;
- whether identical behavior applies outside the listed PowerEdge/Express Flash context;
- the article's original first-publication date before version 3.

Therefore `read all used NAND cells triggers retention tasks` is retained as a **vendor-specific operational claim**, not generalized into `all NAND reads refresh cells`.

---

## Cross-source comparison

| Relation | IBM | Dell | Bounded conclusion |
| --- | --- | --- | --- |
| standards background | cites enterprise 3 months / 40 °C | cites enterprise 3 months at maximum rated endurance and ≤40 °C storage | same broad risk/qualification background |
| intervention point | after 2 months off | every 2.5 months | operator schedule is earlier than/around headline boundary |
| powered duration | at least 2 weeks | minimum 3 weeks | no universal vendor cadence |
| explicit hidden task | not specified in detail | powered background/data-retention tasks | power presence and maintenance work are separable |
| read-trigger path | not stated | full read of used NAND triggers retention tasks | Dell-specific trigger, not universalized |
| capacity dependence | not stated | larger capacity requires longer powered duration | qualitative relation only; no scaling law |
| backup / long-storage policy | recent backup; avoid extended off at EOL | backup/decommission if stored off >3 months | retention runbook includes operational safety margin |

The strongest cross-source finding is negative:

```text
same three-month enterprise retention background
    !=
one standardized power-up schedule
    !=
one standardized maintenance-completion rule
```

The vendor runbooks layer operational policy above a qualification relation.

## Follow-on — IBM / Lenovo cadence and source independence

The bounded follow-on in [`111-ibm-lenovo-2020-2021-cadence-provenance-deepening.md`](111-ibm-lenovo-2020-2021-cadence-provenance-deepening.md) adds two source controls:

- IBM's general guidance, with a surviving creation date of **16 December 2020**, asks for at least **two weeks** powered after two months off;
- IBM's TS7770-specific notice, first published **17 December 2020**, invokes the same broad three-month / 40 °C background but asks for at least **one week** powered after two months off;
- Lenovo HT511702, originally published **24 January 2021**, repeats the two-month / two-week schedule for a platform list that includes `Storwize V7000 for Lenovo`, while older Lenovo support material explicitly groups IBM Storwize-for-Lenovo and Lenovo Storage V-series firmware planning.

The resulting evidence rule is:

```text
same qualification background != uniquely determined field cadence
separate vendor webpage != automatically independent engineering evidence
```

Lenovo therefore remains useful as a provenance/control witness, but it is **not counted as an independent new vendor sample** for a universal powered-maintenance schedule.

## Follow-on — NetApp changes the intervention topology

The bounded follow-on in [`111-netapp-ontap-long-poweroff-data-removal-deepening.md`](111-netapp-ontap-long-poweroff-data-removal-deepening.md) adds a distinct ONTAP/AFF/FAS system-vendor support record rather than another Storwize-derived page.

NetApp's public long-power-off preparation page says that, when removing power from enterprise SSDs for **greater than two months**, operators should **remove all data from the drives** to avoid future SSD-usability impact. Its accessible scope includes ONTAP 9, AFF/FAS, Capacity Flash NVMe SSD, NVMe SSD, and SAS SSD. A separate ordinary ONTAP graceful-shutdown page routes SSD users to critical bulletin SU490, embedding the retention concern into routine shutdown procedure.

That gives a stronger negative control than another cadence number:

```text
same broad offline-retention concern
    !=
same operator intervention topology

retain payload + periodically restore powered maintenance opportunity
    !=
remove payload before prolonged unpowered storage
```

A separate public NetApp KB also reports multiple `Failed-Unsupported` failures for three named TPM3/TPM4 SSD identifiers after drives were brought out of storage and repurposed. The public issue text does not expose the root cause, exact storage duration, wear state, or temperature, so the deepening explicitly keeps `post-storage service failure != proved NAND user-payload charge loss`.

The NetApp record therefore narrows one prior evidence gap: Case 111 now has a genuinely separate system-vendor long-offline witness, but not another independent **periodic-power-up** schedule. That latter comparison remains open.

## Cross-case grounding

### Case 76

Case 76 establishes that the JESD218 number belongs to a workload/endurance/temperature/error-bounded SSD qualification relation. Evidence 111 therefore does not interpret `three months` as a free-standing physical shelf-life constant.

NetApp's public support page paraphrases a JEDEC-derived 2–3 month horizon and says risk varies with wear and storage temperature. That wording is retained as vendor support interpretation rather than substituted for the normative standard.

### Case 37

Case 37 grounds a Samsung 840 EVO product-specific periodic-refresh statement and the fact that the described background feature does not operate while powered off. That is a useful earlier product-level witness for `unpowered persistence != powered maintenance availability`, but it is not evidence for IBM/Dell/NetApp implementation identity.

### Case 44

NetApp's public phrase `remove all data` is a long-storage preparation instruction. It is **not** treated as proof of NVMe Sanitize, cryptographic erase, purge assurance, or physical erasure of every hidden NAND embodiment. Case 44 remains the device-level sanitize-semantics comparison; the relation here is functional contrast only.

### computing-archaeology reuse check

Repository search for `SSD data retention extended shutdown power-off refresh`, `SU490`, and `SSD power off retention` in `tmzncty/computing-archaeology` returned no dedicated case to reuse in this slice. Generic SSD/controller history remains out of scope here.

## Claim-type ledger

| Claim | Type | Strength |
| --- | --- | --- |
| IBM publication/support guidance exists by December 2020 | H/P | strong for surviving support mirror |
| IBM recommends two months off + at least two weeks powered | H/P | strong |
| Dell version 3 recommends 2.5 months + minimum three weeks powered | H/P | strong |
| Dell documents powered background retention work | H/P | strong |
| Dell documents full-used-NAND read as a retention-task trigger | H/P | strong |
| qualification boundary != vendor runbook | E | strong |
| powered state != proved maintenance completion | E | strong |
| read sweep != verification-only in Dell's bounded regime | H/E | strong |
| IBM product-specific cadence can differ even with the same broad retention background | H/E | strong; TS7770 is the bounded negative control |
| Lenovo HT511702 is independent confirmation of a universal IBM-style cadence | X | rejected; visible Storwize-for-Lenovo/V-series support lineage makes independence unsafe to assume |
| NetApp publicly says to remove all data before planned >2-month enterprise-SSD power-off | H/P | strong for the accessible ONTAP preparation page |
| NetApp supplies a genuinely separate system-vendor long-offline policy witness | H/E | strong at runbook/provenance level; not a component-supply-chain independence claim |
| the NetApp preparation path is another IBM/Dell-style periodic powered-maintenance cadence | X | rejected; accessible guidance changes the intervention topology instead |
| NetApp `remove all data` proves sanitization assurance | X | rejected |
| named NetApp post-storage `Failed-Unsupported` reports prove NAND user-bit charge loss | X | rejected; public issue text does not resolve cause |
| vendor guidance proves one universal SSD refresh algorithm | X | rejected |
| three months is deterministic device failure time | X | rejected |
| Case 37 -> IBM/Dell/NetApp direct genealogy | X | rejected |

## Evidence gaps deliberately left open

1. first-publication archaeology for Dell article 000198930 before the 14 May 2026 version-3 modification;
2. named-drive/controller mapping for Dell's described hidden retention tasks;
3. telemetry or service logs proving maintenance completion;
4. independent post-endurance fault/retention tests of the recommended shutdown schedules;
5. genuinely independent cross-vendor **periodic-power-up** guidance beyond IBM and Dell: NetApp now closes the broader independent-vendor long-offline-policy gap but exposes a different pre-storage data-removal topology, while Lenovo HT511702 remains a lineage/provenance control rather than an independent sample;
6. direct firmware or patent evidence for Dell's read-triggered retention path;
7. capacity-to-maintenance-time scaling;
8. public engineering rationale for IBM's one-week TS7770 cadence versus the two-week general Storwize/FlashSystem cadence;
9. full authenticated SU490 text plus publication/revision chronology;
10. public root-cause/resolution evidence for NetApp's named TPM3/TPM4 post-storage `Failed-Unsupported` cases;
11. exact SAS/NVMe device-level semantics of NetApp's gated `scsi format` preparation procedure.