# Evidence 111 Addendum — NetApp Rated-Life Telemetry as an Offline-Retention Admission Signal

## Scope

This addendum deepens Case 111 with a third enterprise-vendor relation that is **not another periodic power-up schedule**. NetApp ONTAP documentation ties SSD `rated life used` telemetry to whether a drive should still be trusted for long powered-off retention and to an operator replacement policy.

The bounded question is:

> What changes when a system retains an estimate of SSD endurance consumption and uses that estimate to qualify future power-off retention policy?

This record does **not** establish the internal NAND wear model, a universal SSD failure threshold, an IBM/Dell-style powered-maintenance cadence, or first invention of SSD wear telemetry.

## Source 1 — NetApp ONTAP 9.9.1 EMS Event Catalog, May 2021

**Document:** _ONTAP 9.9.1 EMS Event Catalog_, May 2021, document `215-15259_A0`.

**Official PDF:** <https://docs.netapp.com/p/ontap/9x/9.9.1/EMS-Event-Catalog.pdf>

The preserved NetApp catalog contains three related `shm.threshold` events:

- `shm.threshold.ratedLife` — NOTICE when SSD rated life used exceeds **90%**;
- `shm.threshold.ratedLife2` — ERROR when rated life used exceeds **95%**;
- `shm.threshold.ratedLifeMax` — ALERT when rated life used exceeds **100%**.

For the 90% and 95% events, NetApp says that when an SSD reaches 100% of rated life it **might not be able to retain data while powered off for long periods of time**. The corrective action says the reported number of weeks remaining is an **estimate based on past usage** and tells the operator to plan replacement as rated life approaches 100% if the SSD is expected to remain in service beyond that estimate.

For the over-100% event, NetApp gives the same long-power-off retention warning and directly instructs the operator to **replace** SSDs that have reached end of rated life.

### Historical boundary

The May 2021 catalog is a directly inspected vendor-documentation floor for this relation. It is **not** used as the first appearance of the event family, the invention date of rated-life telemetry, or the first product deployment of endurance-aware replacement policy.

## Source 2 — NetApp current `shm.threshold` event documentation

**Official page:** <https://docs.netapp.com/us-en/ontap-ems/shm-threshold-events.html>

The current NetApp event page preserves the same semantic separation:

```text
>90% rated life used
    -> NOTICE + replacement planning

>95%
    -> ERROR + replacement planning

>100%
    -> ALERT + replace drive
```

The severity ladder is operational policy. The wording does not say a drive is physically unreadable at 100%, and it does not say one particular bit fails exactly when the estimate crosses a threshold.

Therefore:

> **rated-life threshold crossing ≠ deterministic payload failure instant**.

At the same time, the threshold does change what the vendor asks the operator to trust about future service, especially long powered-off retention.

## Source 3 — NetApp `storage disk show -ssd-wear`

**Official CLI page:** <https://docs.netapp.com/us-en/ontap-cli/storage-disk-show.html>

NetApp documents `-ssd-wear` as a view of SSD wear-life information. The fields include:

- `Rated Life Used` — an estimate of the percentage of device life used, based on actual device usage and the manufacturer's prediction of device life;
- `Spare Blocks Consumed Limit`;
- `Spare Blocks Consumed`.

The CLI documentation explicitly says that a `Rated Life Used` value greater than 99 means estimated endurance has been used, but **does not necessarily indicate device failure**.

That statement is crucial for the retention boundary:

```text
estimated endurance consumed
    !=
immediate device failure
    !=
continued qualification for long powered-off retention
```

The EMS policy can withdraw operator confidence in long-offline retention even while the CLI refuses to equate the endurance estimate with immediate failure.

## Engineering reconstruction

### E — payload survival and offline-retention admission are different states

A drive can still be online and serving data while its retained endurance estimate approaches the end of rated life. NetApp's warning changes the **future operating policy** before the evidence says the current payload has vanished.

Therefore:

> **current readable payload ≠ continued qualification for extended powered-off retention**.

This is a currentness/admissibility relation about future retention service, not evidence of immediate physical erasure.

### E — retained health telemetry can become retention infrastructure

The `Rated Life Used` estimate is not user payload, yet NetApp uses it to decide when an operator should plan or perform drive replacement because future long-power-off retention may no longer be trustworthy.

Thus:

> **non-payload health state can qualify whether payload retention is operationally trusted**.

This is a direct bridge to Case 55: retained device-history/model state can participate in future service admission without becoming the payload itself.

### E — forecast, threshold, and action are separate relations

NetApp's 90%/95% messages describe a remaining-weeks estimate based on past usage, while the 100% event changes the prescribed action to replacement. These should not be collapsed into one physical clock.

```text
past-use telemetry
    -> estimated rated-life consumption / weeks remaining
    -> warning severity
    -> operator replacement policy
```

The arrows are a project engineering reconstruction of the documented relation. NetApp does not expose the internal statistical model or guarantee that the estimate is a wall-clock countdown.

### E — rated-life telemetry and spare-block telemetry are not synonyms

`storage disk show -ssd-wear` exposes `Rated Life Used` separately from `Spare Blocks Consumed` and its limit. The host-visible interface therefore blocks a shortcut in which all SSD wear state is treated as one scalar.

> **rated-life estimate ≠ spare-block consumption**.

The two may both inform service decisions, but this evidence does not establish one-to-one causality between them.

### E — NetApp policy differs from IBM/Dell maintenance cadence

Case 111's IBM and Dell evidence gives operator schedules for restoring powered maintenance opportunity during long shutdowns. The NetApp evidence inspected here instead says that approaching/end-of-rated-life drives may be unsuitable for long powered-off retention and should be planned for replacement/replaced.

Therefore:

> **wear-state admission policy ≠ periodic power-up maintenance schedule**.

Both are operator-facing retention infrastructure, but they intervene on different variables.

## Cross-case comparison

### Case 55 — NVMe SMART / Health endurance telemetry

Case 55 grounds `Percentage Used` as a vendor-specific estimate and preserves the important rule that 100% estimated endurance consumed does not necessarily mean device failure. NetApp's `Rated Life Used` operationalizes the same broad kind of model-derived wear evidence at the storage-system layer: the estimate becomes an input to warning severity and replacement planning.

This is a **functional/interface comparison**, not proof that NetApp's field is copied directly from one NVMe field or that every attached SSD uses NVMe.

### Case 76 — JESD218 SSD endurance/retention qualification

Case 76 establishes that rated endurance and power-off retention are related through a bounded qualification contract. NetApp adds an operator-layer relation after deployment: once rated-life telemetry approaches or exceeds the qualification horizon, future long-offline retention is no longer treated as an unqualified assumption.

Thus:

> **qualification rating ≠ current field evidence about remaining qualified margin**.

### Case 111 — IBM/Dell extended-shutdown policy

IBM and Dell turn extended shutdown into a schedule for backup, environmental control, powered time, and hidden maintenance. NetApp adds a different gate: even before deciding how long to power a system, the operator may need to ask whether the SSD's **wear state still makes long powered-off retention an admissible plan**.

## Historical record / engineering / analogy boundaries

- **H/P:** NetApp's documented 90/95/100% event thresholds, severity levels, long-power-off warning, replacement action, and CLI field semantics.
- **E:** decomposing telemetry → estimate → policy action and treating this as an admission relation for future retention service.
- **A:** comparison to NVMe `Percentage Used`, JESD218 qualification, and IBM/Dell shutdown runbooks.
- **X:** `100% rated life = immediate physical data loss`.
- **X:** `NetApp rated-life events = one documented NAND refresh algorithm`.
- **X:** `NetApp policy = IBM/Dell periodic power-up schedule`.
- **X:** `May 2021 = invention or first-deployment date`.

## Claim ledger

| Claim | Type | Strength | Boundary |
| --- | --- | --- | --- |
| ONTAP 9.9.1 EMS documentation contains 90%, 95%, and >100% rated-life events | H/P | strong | vendor-system event contract, not physical wear law |
| NetApp links end of rated life to possible inability to retain data during long power-off | H/P | strong | probabilistic/vendor wording, not deterministic failure |
| 90/95% events tell operators to plan replacement; >100% tells them to replace | H/P | strong | operator policy, not proof current payload is unreadable |
| `storage disk show -ssd-wear` separates Rated Life Used from spare-block consumption | H/P | strong | host-visible model/telemetry separation; internals undisclosed |
| `>99` estimated endurance used does not necessarily mean device failure | H/P | strong | directly stated by NetApp CLI docs |
| readable now ≠ qualified for extended powered-off retention | E | strong | cross-source policy decomposition |
| health telemetry can be retention infrastructure without being payload | E/A | medium | project interpretation, not NetApp vocabulary |
| NetApp policy proves IBM/Dell-style background-maintenance cadence | X | rejected | no such cadence in inspected NetApp evidence |
| rated-life threshold proves physical failure instant | X | rejected | NetApp explicitly blocks the stronger reading |

## Open questions

- When did the `shm.threshold.ratedLife*` event family first appear before the inspected May 2021 ONTAP 9.9.1 catalog?
- Which underlying drive-health field(s) feed NetApp `Rated Life Used` for each supported SSD/SAS/NVMe family?
- How does ONTAP combine rated-life estimate, spare-block consumption, media errors, and other telemetry in replacement decisions outside these documented events?
- Are there independent field/fault studies showing how NetApp's replacement thresholds correlate with actual powered-off retention after rated endurance?
- How do other enterprise storage stacks expose or act on the same `online but no longer trusted for long-offline retention` state?

## Sources

- NetApp, _ONTAP 9.9.1 EMS Event Catalog_, May 2021, doc `215-15259_A0`: <https://docs.netapp.com/p/ontap/9x/9.9.1/EMS-Event-Catalog.pdf>.
- NetApp, `shm.threshold events`: <https://docs.netapp.com/us-en/ontap-ems/shm-threshold-events.html>.
- NetApp, `storage disk show`: <https://docs.netapp.com/us-en/ontap-cli/storage-disk-show.html>.
- Internal comparison: [`Case 55 — NVM Express SMART / Health Endurance Telemetry`](../cases/55-nvme-smart-health-endurance-telemetry.md).
- Internal comparison: [`Case 76 — JEDEC JESD218 SSD Endurance Qualification`](../cases/76-jedec-ssd-endurance-retention-qualification.md).
