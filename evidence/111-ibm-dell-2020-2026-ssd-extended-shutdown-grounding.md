# Evidence 111 — IBM / Dell Enterprise-SSD Extended-Shutdown Guidance, 2020–2026

## Scope

This record grounds a narrow operational-retention case: two infrastructure vendors publish guidance for enterprise SSD/NVMe systems that may remain powered off long enough for power-off retention to become an operator concern.

It does **not** independently reproduce JESD218; that standards relation is already grounded in Case 76. It does not infer undocumented firmware algorithms from support prose.

Cadence/source-provenance follow-on: [`111-ibm-lenovo-2020-2021-cadence-provenance-deepening.md`](111-ibm-lenovo-2020-2021-cadence-provenance-deepening.md). That deepening shows that IBM itself published different minimum powered-run durations for different product contexts while invoking the same broad retention background, and that Lenovo's later near-matching Storwize-family guidance should not be counted naively as an independent cross-vendor witness.

Independent-vendor intervention-topology follow-on: [`111-netapp-ontap-long-poweroff-data-removal-deepening.md`](111-netapp-ontap-long-poweroff-data-removal-deepening.md). NetApp's public ONTAP support path supplies a distinct system-vendor witness: for intended enterprise-SSD power-off beyond two months, the accessible preparation guidance says to remove all data rather than publishing another IBM/Dell-style periodic powered-maintenance cadence. The same deepening records a named-drive post-storage `Failed-Unsupported` field symptom while refusing to infer its lower-level cause from the public issue text.

Earlier independent periodic-power-up follow-on: [`111-hitachi-2014-2016-flashmax-periodic-poweron-deepening.md`](111-hitachi-2014-2016-flashmax-periodic-poweron-deepening.md). Surviving Hitachi/HGST FlashMAX product documentation supplies a separate vendor/product-family witness by instructing operators to turn on the server once every three months during storage, alongside a wear-dependent maximum-power-off table. It closes the broad independent periodic-power-up witness gap while preserving a narrower open question: the inspected FlashMAX sources do **not** state a retention-specific minimum powered duration or completion signal.

Named-device all-bit-refresh follow-on: [`111-oracle-2020-2021-nvme-all-bit-refresh-recommissioning-deepening.md`](111-oracle-2020-2021-nvme-all-bit-refresh-recommissioning-deepening.md). Oracle's 6.4 TB NVMe SSD v1 documentation closes that narrower gap for a distinct product/document corpus: the firmware refresh policy runs while powered, approximately fourteen days are required for the policy to reach all bits, and the fixed-issue table says two weeks powered fully resolves Bug 27759886. The same source supplies a destructive secure-erase path for immediate all-bit refresh, making `medium renewal != old-payload preservation` explicit. Oracle's own product guide identifies an Intel controller and Intel proprietary controller firmware, so the Oracle corpus is not double-counted as an independent controller lineage.

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

The NetApp record narrows the broader independent-vendor long-offline-policy gap but exposes a different pre-storage data-removal topology.

## Follow-on — Hitachi / HGST FlashMAX supplies an earlier independent periodic-power-up witness

The bounded follow-on in [`111-hitachi-2014-2016-flashmax-periodic-poweron-deepening.md`](111-hitachi-2014-2016-flashmax-periodic-poweron-deepening.md) adds a separate vendor/product-family record from the FlashMAX PCIe SSD era.

The Hitachi user guide gives a wear-dependent maximum-power-off table: 5 years at 90% remaining write capacity, 18 months at 67%, 9 months at 50%, and 3 months at 0%. Immediately after that table it tells the operator to turn on the server **once every three months even while the device is stored**. A later `-03` guide preserves the same relation. HGST's May/August 2015 FlashMAX datasheet separately lists **3-month retention at 40 °C at EOL** for FlashMAX II/III.

This closes the prior evidence gap for a genuinely separate periodic-power-up instruction outside IBM/Dell/Lenovo lineage:

```text
wear-conditioned maximum-power-off duration
    != operator cadence that must vary one-for-one with wear

product retention specification
    != operator storage runbook
```

It also creates a new negative control. Unlike IBM/Dell, the inspected FlashMAX guide says **when** to restore server power but does not state a retention-specific minimum powered duration or a completion signal. Therefore:

```text
periodic power-on instruction
    != minimum powered duration
    != maintenance-completion evidence
```

The same manual separately scopes an integrity check to **unanticipated shutdown**, so that restart check is not silently promoted into the mechanism behind the periodic-storage instruction.

## Follow-on — Oracle supplies a named-device powered-duration and issue-completion witness

The bounded follow-on in [`111-oracle-2020-2021-nvme-all-bit-refresh-recommissioning-deepening.md`](111-oracle-2020-2021-nvme-all-bit-refresh-recommissioning-deepening.md) closes the narrower FlashMAX gap without turning one product into a universal SSD rule.

Oracle's June 2020 user guide gives the 6.4 TB NVMe SSD a three-month power-off retention specification at rated write endurance and 40 °C. The November 2021 v1 product notes then document Bug ID **27759886**, fixed in RF30, and state that the firmware refresh policy works in the background while the drive remains powered. Applying that policy to **all bits** takes approximately **14 days** and varies by product. The fixed-issues table further says that, absent the immediate erase sequence, the issue is **fully resolved after two weeks of device power-on**.

That gives a new state decomposition:

```text
power restored
    != refresh-policy coverage complete
    != issue-scoped completion
```

Oracle also offers secure erase when immediate refresh of all bits is desired and warns that erase destroys all device data. This supplies a second retention boundary inside one named issue:

```text
renewing / refreshing medium state
    != preserving the old logical payload
```

The background powered-wait path and the destructive erase path can both close the documented long-offline issue while carrying opposite payload contracts.

The source-lineage boundary is equally important. Oracle's own product guide identifies one Intel Flash Memory NVMe Controller and Intel custom/proprietary PCIe-to-NAND controller firmware. Oracle therefore supplies an independent **operator/product-document corpus** relative to IBM/Dell/Hitachi, but is not counted as proof of an independent controller architecture or controller-firmware lineage from Intel.

## Cross-case grounding

### Case 76

Case 76 establishes that the JESD218 number belongs to a workload/endurance/temperature/error-bounded SSD qualification relation. Evidence 111 therefore does not interpret `three months` as a free-standing physical shelf-life constant.

NetApp's public support page paraphrases a JEDEC-derived 2–3 month horizon and says risk varies with wear and storage temperature. That wording is retained as vendor support interpretation rather than substituted for the normative standard.

The HGST 2015 datasheet contributes a named commercial-product statement — `3-month retention at 40 °C at EOL` — while the Hitachi guide separately contributes the stored-device power-on cadence. Their shared number is not treated as identity of evidence type or as a proof that JEDEC mandated that runbook.

Oracle independently supplies a named-product three-month / 40 °C retention specification at rated write endurance, while its product notes separately supply the powered all-bit-refresh duration for Bug 27759886. Numerical proximity does not collapse qualification and maintenance into one relation.

### Case 37

Case 37 grounds a Samsung 840 EVO product-specific periodic-refresh statement and the fact that the described background feature does not operate while powered off. That is a useful earlier product-level witness for `unpowered persistence != powered maintenance availability`, but it is not evidence for IBM/Dell/NetApp/FlashMAX/Oracle implementation identity.

Oracle's issue also supplies a useful negative control: its long-offline problem can exceed ECC capability and surface as uncorrectable reads or power-on ASSERT/BAD_CONTEXT, rather than merely as the old-data read-performance degradation at issue in Case 37.

### Case 44

NetApp's public phrase `remove all data` is a long-storage preparation instruction. It is **not** treated as proof of NVMe Sanitize, cryptographic erase, purge assurance, or physical erasure of every hidden NAND embodiment. Case 44 remains the device-level sanitize-semantics comparison; the relation here is functional contrast only.

Oracle's secure-erase path is likewise retained as the vendor's destructive immediate-refresh operation in this issue context; it is not promoted into an independent sanitization-verification result.

### computing-archaeology reuse check

Repository search for `SSD data retention extended shutdown power-off refresh`, `SU490`, `SSD power off retention`, `FlashMAX`, `Oracle 6.4 TB NVMe SSD`, and `27759886` in `tmzncty/computing-archaeology` returned no dedicated case to reuse in these slices. Generic SSD/controller, Virident/HGST, and Intel/Oracle product history remains out of scope here.

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
| Hitachi FlashMAX guide says to turn on the server once every 3 months while stored | H/P | strong; vendor product guide |
| Hitachi FlashMAX wear-dependent retention table ranges down to 3 months at 0% remaining write capacity | H/P | strong; table is not deterministic individual failure time |
| HGST 2015 FlashMAX datasheet states 3-month retention at 40 °C at EOL | H/P | strong; commercial product statement |
| Hitachi/HGST supplies an independent periodic-power-up witness outside IBM/Dell/Lenovo support lineage | H/E | strong at vendor/product-document level; not a component-supply-chain-independence claim |
| FlashMAX periodic power-on establishes a minimum powered duration or completion event | X | rejected; inspected source states neither |
| Oracle 6.4 TB NVMe v1 firmware policy refreshes media in the background while powered | H/P | strong; named product notes / Bug 27759886 |
| Oracle says all-bit refresh-policy coverage takes about 14 days and varies by product | H/P | strong; product-specific duration, not universal constant |
| Oracle says two weeks powered fully resolves Bug 27759886 | H/P | strong; issue-scoped completion, not universal device-health certificate |
| Oracle secure erase provides immediate all-bit refresh while destroying device data | H/P | strong; destructive alternative in the same issue context |
| medium renewal == preservation of old logical payload | X | rejected directly by Oracle's paired background-wait / secure-erase paths |
| Oracle documentation proves an independent controller lineage from Intel | X | rejected; Oracle identifies Intel controller ASIC and proprietary Intel controller firmware |
| NetApp `remove all data` proves sanitization assurance | X | rejected |
| named NetApp post-storage `Failed-Unsupported` reports prove NAND user-bit charge loss | X | rejected; public issue text does not resolve cause |
| vendor guidance proves one universal SSD refresh algorithm | X | rejected |
| three months is deterministic device failure time | X | rejected |
| Case 37 -> IBM/Dell/NetApp/FlashMAX/Oracle direct genealogy | X | rejected |

## Evidence gaps deliberately left open

1. first-publication archaeology for Dell article 000198930 before the 14 May 2026 version-3 modification;
2. named-drive/controller mapping for Dell's described hidden retention tasks;
3. independent host-visible telemetry or service logs proving **device-local** all-bit/background-retention completion outside the ESS system-level scrub witness — Oracle supplies issue-scoped duration/completion semantics but not a progress counter in the inspected pages;
4. independent post-endurance fault/retention tests of the recommended shutdown schedules;
5. the prior gap for a separate vendor witness combining periodic/powered maintenance with an explicit minimum powered duration and completion semantics is now **closed in bounded form by Oracle 6.4 TB NVMe v1 / Bug 27759886**; remaining work is cross-generation generality, direct firmware internals, and observable progress telemetry;
6. direct firmware or patent evidence for Dell's read-triggered retention path;
7. capacity-to-maintenance-time scaling beyond Oracle's explicit `varies by product` and Dell's qualitative larger-capacity statement;
8. public engineering rationale for IBM's one-week TS7770 cadence versus the two-week general Storwize/FlashSystem cadence;
9. full authenticated SU490 text plus publication/revision chronology;
10. public root-cause/resolution evidence for NetApp's named TPM3/TPM4 post-storage `Failed-Unsupported` cases;
11. exact SAS/NVMe device-level semantics of NetApp's gated `scsi format` preparation procedure;
12. FlashMAX revision/publication genealogy, a retention-specific minimum powered duration if one exists, and any operator-visible completion evidence tied specifically to long-offline retention rather than unexpected-shutdown recovery;
13. Oracle RF30 first-release chronology, exact internal refresh/rewrite geometry, and whether later Intel/Oracle product generations preserve the same approximately fourteen-day policy.
