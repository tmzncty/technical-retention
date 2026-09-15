# Evidence 111D — IBM / Lenovo 2020–2022 extended-shutdown cadence and documentation-lineage deepening

**Status:** `bounded deepening complete`

## Scope

This record deepens one narrow part of Case 111:

> when several enterprise-storage documents invoke the same three-month / 40 °C SSD-retention background, do their operator schedules form one universal rule, and does similar wording across IBM and Lenovo count as independent cross-vendor corroboration?

The answer supported by the inspected first-party record is **no** on both points.

The bounded 2020–2022 record contains at least three different IBM operational schedules around the same standards-level background, plus a Lenovo support article whose wording and product context are closely tied to the IBM Storwize-for-Lenovo lineage. A later IBM ESS alert also separates a short **automatic scrub trigger after more than seven days powered off** from the much longer **operator intervention schedule after two months off**.

This evidence is therefore about:

- operator-policy granularity;
- product-family / system-context dependence;
- documentation lineage;
- maintenance-trigger vs maintenance-window semantics;
- anti-double-counting when apparently independent vendor pages share a platform/document family.

It is **not**:

- a re-derivation of JESD218;
- a claim that any one IBM schedule is physically optimal;
- a controller-firmware implementation study;
- proof that the same SSD model was used across every listed platform;
- proof that Lenovo independently measured the same retention boundary;
- an invention-priority claim for SSD refresh or scrubbing.

---

## Source map

### H/P — IBM generic support flash, created 16 December 2020

IBM's first-party support-content page **“Potential for SSD data loss after extended shutdown”** records:

- creation by Richard Hopkins on **16 December 2020**;
- the enterprise-SSD background of at least **three months at 40 °C**;
- a recommendation that a system and enclosed drives be powered up for **at least two weeks after two months of system power off**;
- backup, sub-40 °C environment, and end-of-life cautions;
- a `chdrive -task format <drive-id>` path for drives in a system being retired and later reused.

The affected-product metadata spans multiple IBM storage families, including Storwize V7000 / V5000, SAN Volume Controller, and FlashSystem families.

Primary source:

<https://supportcontent.ibm.com/support/pages/potential-ssd-data-loss-after-extended-shutdown>

Current IBM page:

<https://www.ibm.com/support/pages/potential-ssd-data-loss-after-extended-shutdown>

### H/P — IBM TS7770 notice, first published 17 December 2020

IBM's **“TS7770 with FC 8081 may experience issues when being powered off for more than three months”** repeats the same three-month / 40 °C background, but its recommended action differs:

- power the system and enclosed drives for **at least one week after two months of system power off**;
- maintain backups;
- avoid extended shutdown for end-of-life drives;
- keep the powered-off environment below 40 °C.

IBM marks the notification **Date first published: 17 December 2020**.

Primary source:

<https://www.ibm.com/support/pages/node/6382550>

The important bounded observation is:

```text
same vendor
+ same standards-level background
+ almost the same publication moment
    !=
one universal powered-maintenance dwell time
```

The generic IBM flash says **two weeks** after two months off; the TS7770 notice says **one week** after two months off.

### H/P — IBM Redbooks ESS 5000 first edition, December 2020

IBM Redbooks **_Implementation Guide for IBM Elastic Storage System 5000_**, SG24-8498-00, states **First Edition (December 2020)**.

In the ESS 5000 reliability / availability / serviceability section, under **“Potential for SSD data loss after extended shutdown and best practices,”** it repeats the same three-month / 40 °C background and gives a third cadence:

- **power on at least one week every six weeks of system power-off**.

It separately recommends backups, keeping the powered-off system below 40 °C, and reformatting drives when a retired system will be used for another activity.

Primary source:

<https://www.redbooks.ibm.com/redbooks/pdfs/sg248498.pdf>

Inspected location in the surviving PDF text layer:

- publication statement: front matter / pp. ii–iii;
- extended-shutdown guidance: PDF page around the printed p. 28, section 2.4.1.

The PDF text layer gives the key sequence as:

```text
three-month / 40 °C background
    -> ESS 5000 best practice
    -> one week powered every six weeks off
```

This schedule is more conservative in calendar spacing than the generic two-month intervention point, and it again prevents the standards headline from being treated as the field schedule itself.

### H/P — Lenovo HT511702, original publication 24 January 2021

Lenovo Support article **HT511702, “Potential for SSD data loss after extended shutdown”** records:

- **Original Publish Date: 24 January 2021**;
- **Last Modified Date: 25 January 2021**;
- the same three-month / 40 °C enterprise-SSD background;
- a recommendation to power the system and enclosed drives for **at least two weeks after two months of system power off**;
- the same backup, environment, end-of-life, and `chdrive -task format` structure as the IBM generic flash.

The affected Lenovo platforms include Lenovo Storage V3500 / V3700 / V3700 V2 / V5000 / V5030 / V7000 and **Storwize V7000 for Lenovo**.

Primary source:

<https://support.lenovo.com/za/en/solutions/ht511702>

A surviving indexed copy with the publication metadata is also available through Lenovo's data-center support site under the same document ID `HT511702`.

### H/P — first-party product context ties the Lenovo page to an IBM Storwize lineage

Lenovo Press product guide **TIPS1302, “IBM Storwize V7000 for Lenovo,”** explicitly names the product **IBM Storwize V7000 for Lenovo (Machine Type 6195)** and describes it as a Storwize V7000 system available from Lenovo.

Primary source:

<https://lenovopress.lenovo.com/tips1302-ibm-storwize-v7000-for-lenovo>

Lenovo firmware-support records likewise describe firmware update through the **IBM Storwize V7000 for Lenovo** web UI / CLI.

Example first-party support record:

<https://support.lenovo.com/us/en/downloads/ds505434-firmware-update-bundle-v8136-storwize-v7000-for-lenovo>

This does not prove that every affected Lenovo V-series platform is literally identical to an IBM-branded machine. It does, however, make one anti-anachronistic point unavoidable:

> the Lenovo HT511702 page should not automatically be counted as an independent third-vendor discovery of the same retention policy merely because the support page carries a Lenovo masthead.

The wording, command vocabulary, affected Storwize-for-Lenovo family, timing, and first-party product lineage all support treating it as **documentation / platform-lineage evidence** unless stronger independent engineering evidence is found.

### H/P — IBM ESS alert, modified 23 May 2022, introduces a distinct automatic scrub trigger

IBM's later **“IBM ESS Alert: Potential for SSD data loss after extended shutdown”** covers ESS 3000 / 3200 / 3500 and other ESS models.

It retains the familiar operator guidance:

- after **two months** powered off, provide at least **two weeks** powered;
- keep the environment below 40 °C;
- maintain backups and avoid long power-off for end-of-life drives.

But it adds a different threshold and a named automatic behavior:

> if, after installation, the system has been powered off **longer than seven days**, the system automatically starts an ESS background scrub routine on return to service; IBM describes that routine as reading data and rewriting **only if it finds a problem**.

Primary source:

<https://www.ibm.com/support/pages/ibm-ess-alert-potential-ssd-data-loss-after-extended-shutdown>

Document metadata visible on the current page:

- modified **23 May 2022**;
- UID `ibm16574831`.

This source supplies a useful state-machine distinction that the headline three-month number obscures.

---

## Historical record — bounded chronology

The surviving sources support the following narrow chronology:

```text
December 2020
    IBM ESS 5000 Redbook:
        1 week powered every 6 weeks off

16 December 2020
    IBM generic support flash:
        2 months off -> at least 2 weeks powered

17 December 2020
    IBM TS7770 notice:
        2 months off -> at least 1 week powered

24 January 2021
    Lenovo HT511702:
        2 months off -> at least 2 weeks powered
        wording / Storwize context closely tracks IBM generic flash

by 23 May 2022 surviving ESS alert
    2 months off -> at least 2 weeks powered
    AND
    >7 days off after installation -> automatic ESS background scrub on return
```

This chronology is not a claim that every text was authored independently on the stated date. It is the chronology of the surviving, dated documents inspected in this slice.

---

## Engineering reconstruction

The terms below are project reconstruction unless explicitly attributed to the vendor sources.

### E — one qualification relation can feed multiple field policies

The records repeatedly invoke a common standards-level background, yet operator schedules differ even within IBM documentation.

Therefore:

```text
qualification relation
    !=
operator intervention threshold
    !=
powered dwell recommendation
```

A field schedule includes product/system assumptions and safety margin that are not recoverable from the headline qualification interval alone.

The evidence does **not** tell us why IBM chose one week for TS7770, two weeks for the generic flash, or one week every six weeks for the ESS 5000 Redbook. Those reasons remain undisclosed in the inspected sources.

### E — cadence is system-policy metadata, not a NAND physical constant

Because distinct IBM documents map the same background to different schedules, the schedule itself must be treated as a **system/operator policy relation** rather than as a direct readout of one universal NAND decay constant.

That does not mean the schedules are arbitrary. It means the historical source level matters:

```text
physical retention risk
    -> vendor / system interpretation
    -> operational cadence
```

The middle layer cannot be safely erased by quoting only `three months at 40 °C`.

### E — automatic scrub trigger and long-offline intervention threshold are different clocks

The later ESS alert contains both:

- an automatic scrub trigger after more than **seven days** off;
- a recommendation for a much longer **two-month** offline interval followed by **two weeks** powered.

These thresholds perform different jobs.

A bounded reconstruction is:

```text
short offline history threshold
    -> admit automatic scrub on return

long offline policy threshold
    -> operator should schedule a substantial powered-maintenance interval
```

The seven-day threshold is not evidence that data becomes unsafe on day eight. The two-month threshold is not evidence that the automatic scrub is absent before two months. They are separate policy/control conditions in the same ESS record.

### E — automatic scrub can be selective repair rather than blanket rewrite

The ESS alert says the background scrub is designed to **read the data and rewrite only if a problem is found**.

Therefore, for this named system record:

```text
scrub admitted
    !=
blanket rewrite of all retained data
```

and:

```text
read all / inspect all at system layer
    !=
rewrite all physical NAND pages
```

This is compatible with the separate Case 111 evidence on operator-visible scrub completion, but it does not identify the SSD firmware's hidden refresh algorithm.

### E — apparent cross-vendor agreement may be documentation inheritance

If two support pages have near-identical wording, the evidentiary question is not only “do two companies say the same thing?” but also “are these two independent technical observations?”

Here, Lenovo's page:

- appears shortly after the IBM flash;
- uses the same title and recommendation structure;
- carries the same `chdrive` command vocabulary;
- covers Storwize-family systems including `Storwize V7000 for Lenovo`;
- sits next to first-party Lenovo documentation explicitly naming `IBM Storwize V7000 for Lenovo`.

Thus the safe evidence model is:

```text
second corporate masthead
    !=
independent engineering witness
```

until an independent test, design document, or independently developed support policy is recovered.

This is a documentation-lineage caution, not a claim that IBM and Lenovo had no organizational or engineering independence elsewhere.

---

## Functional analogy / cross-case comparison

### A — Case 76: qualification boundary vs field policy

Case 76 grounds the standards-level endurance / retention qualification relation. This slice strengthens the negative comparison:

```text
same qualification background
    -> multiple field schedules
```

So Case 76's qualification table cannot be converted mechanically into one fleet runbook.

### A — Case 111C: scrub completion vs scrub admission

The existing IBM ESS scrub-completion deepening shows a per-vdisk completion witness in Spectrum Scale RAID documentation.

This slice adds the earlier transition:

```text
offline-history threshold
    -> scrub admitted / automatically started
    -> scrub executes
    -> completion can later be observed
```

Admission and completion are different control states.

### A — Case 37 / Case 36: no algorithm identity

Samsung 840 EVO periodic refresh and academic Flash Correct-and-Refresh remain useful functional comparisons for powered maintenance, but this evidence does not identify either algorithm inside IBM ESS, TS7770, Lenovo Storwize, or Dell systems.

`background scrub`, `periodic refresh`, `read reclaim`, and `FCR` remain separate historical vocabularies unless a direct genealogy is found.

---

## Prior art and related-repository boundary

No invention-priority claim is made for any schedule, scrub trigger, patrol read, read-rewrite policy, or operator runbook.

A fresh search of `tmzncty/computing-archaeology` for enterprise-SSD extended-shutdown / retention-maintenance history found no dedicated reusable case. The complete IBM Storwize / ESS / TS7700 platform genealogy would belong there if developed.

This record keeps only the retention-specific historical relations needed by Case 111:

- qualification background vs field schedule;
- schedule variance within one vendor;
- scrub trigger vs scrub completion;
- documentation lineage vs independent corroboration.

---

## Philosophical / project interpretation

A bounded project interpretation is that **maintenance time is itself classified by institutions**. The same material risk can be translated into multiple operator clocks: a qualification horizon, a recommissioning trigger, a powered dwell recommendation, an automatic scrub admission threshold, and a completion condition.

The historical IBM and Lenovo sources do not use this philosophical vocabulary.

The safe claim is only that retention responsibility is distributed across several clocks and control layers. It is not that time itself is “stored,” nor that every schedule is equivalent to a physical refresh mechanism.

---

## Claim ledger

| Claim | Type | Strength | Boundary |
| --- | --- | --- | --- |
| IBM generic support flash recommends at least 2 weeks powered after 2 months off | H/P | strong | generic affected IBM storage-system guidance |
| IBM TS7770 notice recommends at least 1 week powered after 2 months off | H/P | strong | TS7770 / FC 8081 context |
| IBM ESS 5000 Redbook recommends at least 1 week powered every 6 weeks off | H/P | strong | ESS 5000 first-edition product guidance |
| Lenovo HT511702 recommends at least 2 weeks powered after 2 months off | H/P | strong | affected Lenovo V-series / Storwize-for-Lenovo context |
| surviving IBM documents map the same three-month / 40 °C background to different field cadences | H/E | strong | does not explain the undisclosed engineering rationale |
| ESS alert automatically starts background scrub after >7 days off after installation | H/P | strong | named ESS behavior in the inspected alert |
| ESS alert says scrub reads data and rewrites only if a problem is found | H/P | strong | system-layer statement, not NAND-page implementation proof |
| >7-day scrub trigger and 2-month intervention schedule are separate control thresholds | E | strong | reconstruction from coexisting vendor rules |
| Lenovo page is safe to count as an independent third-vendor engineering validation | X | rejected | strong documentation / platform-lineage evidence argues against automatic double-counting |
| different IBM cadences prove one of the documents is wrong | X | rejected | products, system contexts, safety margins, and policy revisions may differ |
| one-week or two-week dwell is a universal Flash physical constant | X | rejected | source level is operator/system policy |
| automatic scrub after >7 days means data becomes unsafe on day 8 | X | rejected | trigger threshold != failure threshold |
| ESS scrub rewrites every NAND cell | X | rejected | IBM says rewrite only if a problem is found; physical firmware geometry undisclosed |

---

## Remaining uncertainty

This slice does **not** close:

- the engineering reason for each IBM cadence;
- exact drive/controller part numbers behind each platform and revision;
- whether the Lenovo article was mechanically copied, contractually syndicated, or independently reissued from a shared service corpus;
- the earliest internal publication of the ESS automatic >7-day scrub rule;
- exact scrub geometry and firmware-level read-reclaim / rewrite thresholds;
- whether later product generations changed these windows;
- independent experimental validation of the schedules.

A particularly useful future source would be an IBM/Lenovo service bulletin, firmware design note, or revision history that explicitly explains **why** the cadence differs by platform.

---

## Sources

### Primary / first-party

IBM Support Content, **“Potential for SSD data loss after extended shutdown”**, created 16 December 2020.

<https://supportcontent.ibm.com/support/pages/potential-ssd-data-loss-after-extended-shutdown>

IBM Support, **“TS7770 with FC 8081 may experience issues when being powered off for more than three months,”** first published 17 December 2020.

<https://www.ibm.com/support/pages/node/6382550>

IBM Redbooks, **_Implementation Guide for IBM Elastic Storage System 5000_**, SG24-8498-00, First Edition, December 2020.

<https://www.redbooks.ibm.com/redbooks/pdfs/sg248498.pdf>

Lenovo Support, **HT511702 — “Potential for SSD data loss after extended shutdown,”** original publication 24 January 2021, modified 25 January 2021.

<https://support.lenovo.com/za/en/solutions/ht511702>

Lenovo Press, **TIPS1302 — “IBM Storwize V7000 for Lenovo,”** product guide.

<https://lenovopress.lenovo.com/tips1302-ibm-storwize-v7000-for-lenovo>

Lenovo Support, **DS505434 — Firmware Update Bundle (v8.1.3.6), Storwize V7000 for Lenovo**, describing IBM Storwize V7000 for Lenovo UI/CLI update path.

<https://support.lenovo.com/us/en/downloads/ds505434-firmware-update-bundle-v8136-storwize-v7000-for-lenovo>

IBM Support, **“IBM ESS Alert : Potential for SSD data loss after extended shutdown,”** current page modified 23 May 2022, UID `ibm16574831`.

<https://www.ibm.com/support/pages/ibm-ess-alert-potential-ssd-data-loss-after-extended-shutdown>

---

## Bounded conclusion

The 2020–2022 IBM / Lenovo record makes the operational layer more precise than a single `three months at 40 °C` slogan.

Within IBM documentation alone, the same standards-level background is translated into at least three surviving powered-maintenance schedules:

```text
ESS 5000:   1 week powered every 6 weeks off
TS7770:     1 week powered after 2 months off
IBM generic: 2 weeks powered after 2 months off
```

A later ESS alert also adds a different control clock:

```text
>7 days off after installation
    -> automatic background scrub on return

2 months off
    -> operator should provide a substantial powered-maintenance interval
```

Meanwhile, Lenovo's 2021 support page closely tracks the IBM generic wording and lives inside an explicit `IBM Storwize V7000 for Lenovo` product/document lineage. It is therefore useful evidence of **policy propagation across a product/support lineage**, but should not be automatically counted as an independent engineering discovery.

The resulting retention relation is:

```text
standards qualification
    != system maintenance schedule
    != automatic maintenance trigger
    != maintenance completion
    != independent corroborating source
```

That distinction is now grounded without claiming one hidden firmware mechanism or one universal SSD clock.