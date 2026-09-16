# Evidence 150 — Crucial 2013 Support-Page Version Provenance: Page Identity, Link Existence, and Content-Version Boundaries

## Status

**`bounded deepening complete`**

This record deepens [Case 150 — Crucial M550 Active Garbage Collection](../cases/150-crucial-m550-active-garbage-collection.md) and narrows the historical-provenance debt left by [the earlier 2013–2015 AGC provenance / m4 experiment record](150-crucial-2013-2015-agc-provenance-experiment-deepening.md).

The earlier record established that a public **18 August 2013** reproduction of Crucial support correspondence already carried the `Active Garbage Collection` + `6–8 hours` powered-idle procedure, while a March 2014 forum post quoted related text from Crucial's website. The remaining question was whether the named Crucial support page itself can be placed earlier in 2013 without pretending that a surviving secondary quotation is an authenticated origin archive.

This slice adds two independent period witnesses:

1. **12 June 2013:** Mac Geek Gab episode 453 lists a resource titled **“My SSD used to be so much faster… What happened?”** among its complete show notes, alongside an item about enabling TRIM on a Crucial SSD.
2. **29 September 2014:** an Overclockers UK thread reproduces the Crucial article title and a page-header attribution reading **`by Moderator Crucial_Katana`**, **`01-17-2013 04:30 PM`**, edited **`10-23-2013 09:41 AM`**, followed by the Active Garbage Collection explanation and powered-idle troubleshooting text.

The result is useful but deliberately bounded:

> **The public web record now supports existence of the named Crucial support resource by 12 June 2013 and preserves a later secondary report that the page itself carried a 17 January 2013 creation timestamp. It still does not authenticate the exact January content version or prove that the later `6–8 hours` wording was already present on 17 January.**

This distinction matters because a stable page identity can survive edits while the text attached to that identity changes.

---

## 1. Bounded question

The chronology problem can be written as four different claims that must not be collapsed:

```text
page identity existed
    !=
page carried a particular text version
    !=
text version is preserved verbatim
    !=
origin-hosted copy is authenticated today
```

The earlier evidence had a strong **text-preservation floor** of 18 August 2013 for the `6–8 hours` support procedure, but no earlier witness for the named support page itself.

This slice asks only:

> **How early can the named Crucial support-page identity be placed, and what does the surviving evidence permit us to say about the content version attached to that page?**

It does not attempt to reconstruct Crucial's forum database, recover deleted revision history, or infer SSD firmware behavior from web-page timestamps.

---

## 2. Historical record — 12 June 2013 contemporaneous show notes already name the Crucial support resource

Mac Geek Gab episode 453 is dated **12 June 2013**. Its page says the show notes are complete and lists, among the resources discussed:

- `Enabling TRIM on Crucial SSD?`;
- `TRIM and SSD performance: why is it important?`;
- **`My SSD used to be so much faster… What happened?`**;
- `TRIM Enabler`.

The title is distinctive and matches the historical Crucial support article later cited by forum users and preserved in later quotations.

This gives a stronger chronology relation than the August support-email reproduction:

```text
12 Jun 2013
named Crucial-support resource is already being linked/discussed publicly
```

The source does **not** preserve the article body in the search-visible record inspected here. Therefore it cannot establish which revision of the support text was present on that day or whether the exact `6–8 hours` instructions had already been added.

The proper claim is therefore **resource/page-identity existence**, not content-version identity.

---

## 3. Historical record — a 2014 quotation preserves reported Crucial page metadata back to 17 January 2013

An Overclockers UK thread started **29 September 2014** quotes the same support article under the title **“My SSD used to be so much faster... What happened?”** and reproduces a header attribution:

```text
by Moderator Crucial_Katana
01-17-2013 04:30 PM
edited 10-23-2013 09:41 AM
```

The same quotation then describes `Active Garbage Collection` as a controller maintenance feature triggered when the SSD has power but no data throughput, explains the need for idle periods, and reproduces the powered-idle recovery procedure.

This is valuable provenance because it preserves **version metadata** that is no longer available from the current vendor page path inspected in this project.

But the evidence ceiling remains explicit:

- the Overclockers post is **not** an origin-hosted Crucial capture;
- the `01-17-2013` and `10-23-2013` timestamps are **reported page metadata preserved by a later third party**;
- the quoted body was copied in 2014, after the reported October 2013 edit;
- therefore the body cannot automatically be assigned to the January 2013 version.

The safe chronology is:

```text
reported page creation metadata: 17 Jan 2013
    ↓
independent public link/title witness: 12 Jun 2013
    ↓
detailed Crucial-support-email reproduction: 18 Aug 2013
    ↓
reported page edit metadata: 23 Oct 2013
    ↓
2014 quotation preserves post-edit-era body text
```

The first date is a **secondary preservation of origin metadata**. The second is an **independent contemporaneous existence witness**. The third is a **detailed contemporaneous text witness**. These evidence roles are different.

---

## 4. Historical record — the 18 August 2013 support-email reproduction remains the safer floor for the detailed `6–8 hours` procedure

The earlier evidence record uses a Swedish-language blog post dated **18 August 2013** that reproduces an English Crucial support reply concerning a Crucial V4 SSD. That text explicitly contains:

- `Active Garbage Collection`;
- extended powered idle;
- the **`6 to 8 hours`** interval;
- desktop power-only / SATA-data-disconnected instructions;
- laptop BIOS idling;
- a recommendation to prevent the hard disk from being powered down during the maintenance opportunity.

The new January/June provenance evidence does **not** supersede that text floor.

Instead it changes the chronology into two separate floors:

```text
page/resource existence floor
    <= 12 Jun 2013 directly witnessed
    <= 17 Jan 2013 only as later-preserved page metadata

specific detailed 6–8 h wording floor
    <= 18 Aug 2013 in a contemporaneous reproduced support reply
```

That separation prevents an attractive but unsupported back-dating move.

---

## 5. Historical record — March 2014 still independently preserves vendor-site vocabulary around the M550 launch

A MacRumors post dated **22 March 2014** quotes a passage it attributes to Crucial's website under **“Crucial SSDs and TRIM/Garbage Collection.”** The passage describes `Active Garbage Collection` as a feature inside the SSD/firmware and distinguishes it from operating-system TRIM support.

This remains useful even after the chronology is moved earlier because it shows the vocabulary still circulating around the M550 launch period.

The roles are now:

```text
Jan/Jun 2013 provenance
    -> named support-page identity / reported page metadata

Aug 2013 correspondence reproduction
    -> detailed 6–8 h powered-idle text

Mar 2014 website quotation
    -> vendor-site AGC/TRIM vocabulary near M550 launch

Jan/Mar 2014 first-party M550 records
    -> named-product feature / availability evidence
```

These are complementary witnesses rather than interchangeable duplicates.

---

## 6. Engineering reconstruction — page identity is not content-version identity

The main methodological result is not about NAND internals at all. It is about how technical-support documentation itself must be treated as retained state.

A support page can keep the same title, URL family, author identity, or post identifier while its body changes.

Therefore:

```text
same page identity
    !=
same body text
    !=
same troubleshooting contract
```

The reported metadata in the 2014 quotation makes this concrete: the page is said to have existed from January 2013 and to have been edited in October 2013. A 2014 copy of the body is thus evidence for a **post-edit state**, not automatic evidence for the **pre-edit state**.

This is an engineering/documentation reconstruction, not a claim about how Crucial's forum software internally stored revisions.

---

## 7. Engineering reconstruction — chronology has more than one lower bound

It is useful to distinguish at least four chronology variables:

1. **resource-existence floor** — when the named article can be shown to exist in the public web ecology;
2. **reported creation floor** — the date later-preserved page metadata assigns to the article;
3. **specific-text floor** — when a particular wording is independently preserved;
4. **product-contract floor** — when a named product first-party document advertises the relevant feature.

For this slice:

```text
reported creation metadata      17 Jan 2013   (secondary preservation)
resource-existence witness       12 Jun 2013   (period independent page)
detailed 6–8 h text witness      18 Aug 2013   (period support-email reproduction)
reported edit metadata           23 Oct 2013   (secondary preservation)
M550 flyer revision              29 Jan 2014   (first-party product document)
M550 availability                18 Mar 2014   (first-party announcement)
```

These dates answer different historical questions. Treating the earliest one as the answer to all of them would erase source-version uncertainty.

---

## 8. Functional comparison — technical documentation can retain control obligations imperfectly

Case 150 is about retained control state inside a storage system: invalidity knowledge, mapping/currentness, maintenance opportunity, and reclamation completion.

The documentation provenance problem has a limited structural analogy:

```text
page identity retained
    !=
prior content version retained
```

just as:

```text
logical designation retained
    !=
old physical embodiment retained
```

The analogy stops at the state-separation pattern. A web page revision history is not an SSD FTL, and no technical genealogy is asserted between the two.

---

## 9. Prior-art / related-repository boundary

This chronology does not change the invention-priority boundary for SSD garbage collection. SNIA and older flash-management literature already predate the M550, and the repository already has a 2009-priority IBM controller witness.

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Crucial Active Garbage Collection powered idle` returned no dedicated historical module to reuse.

A full reconstruction of the Crucial forum migration, Lithium/Khoros page identifiers, Micron/Crucial support-site history, or m4/V4/M500/M550 controller genealogy belongs there if pursued. This record keeps only the provenance needed to bound the retention case.

---

## 10. Philosophical interpretation — bounded

A restrained interpretation is possible: **continuity of a named technical object does not guarantee continuity of all the state once attached to that object.**

Here the named object is a support page. Its identity can persist across edits while an earlier body version becomes difficult to recover. That is useful as a documentation analogue for the repository's broader insistence that designation, embodiment, content, and operational authority are separable relations.

This is a bounded methodological observation, not a philosophical claim attributed to Crucial, Mac Geek Gab, or forum participants.

---

## 11. Explicit non-claims

This evidence does **not** establish that:

1. an authenticated Crucial-origin January 2013 capture has been recovered;
2. the `01-17-2013` timestamp has been independently verified against Crucial's original database;
3. the `10-23-2013` edit timestamp identifies the only edit ever made to the page;
4. the article body quoted in September 2014 is identical to the January 2013 body;
5. the exact `6–8 hours` wording was present on 17 January 2013;
6. Mac Geek Gab's June 2013 resource listing preserves the full article body;
7. the June show-note link destination has been independently reconstructed here from an archived HTTP response;
8. the August 2013 V4 support reply and the historical forum article were textually identical;
9. V4, m4, M500, and M550 used the same controller or garbage-collection scheduler;
10. a support-page timestamp dates the first firmware implementation of Active Garbage Collection;
11. Crucial invented SSD garbage collection or powered-idle maintenance;
12. the reported page edit in October 2013 changed the `6–8 hours` language specifically;
13. the current Crucial support article is byte-for-byte continuous with the 2013 forum article;
14. documentation continuity proves firmware-policy continuity.

---

## 12. Claim ledger

| Claim | Type | Strength | Boundary |
| --- | --- | --- | --- |
| Mac Geek Gab episode 453 on 12-Jun-2013 lists `My SSD used to be so much faster… What happened?` among Crucial/TRIM resources | historical provenance | strong period witness | proves named-resource existence in public web ecology, not body text |
| a Sep-2014 Overclockers quotation preserves page metadata saying `Crucial_Katana`, `01-17-2013`, edited `10-23-2013` | historical provenance | moderate | later secondary preservation of reported origin metadata |
| the 2014 quotation also preserves AGC/powered-idle body text | historical provenance | moderate | copied after the reported Oct-2013 edit; cannot be back-dated wholesale to Jan |
| the detailed `6–8 hours` procedure is publicly preserved by 18-Aug-2013 | historical provenance | moderate | contemporaneous support-email reproduction, not authenticated origin page |
| the named support resource therefore definitely had the later 2014 body on 17-Jan-2013 | rejected | unsupported | page identity / creation metadata != content-version identity |
| a support-page creation date is the date Crucial first implemented AGC in firmware | rejected | unsupported | documentation chronology != firmware chronology |
| the M550 implemented the same scheduler described for earlier Crucial products | rejected | unsupported | cross-product algorithm identity not established |

---

## 13. Source ledger

### C1 — Mac Geek Gab episode 453, 12 June 2013 — `S/period`, contemporaneous link/title witness

Dave Hamilton, **“MGG 453: WWDC, TiVo, Mixed-Spectrum SSIDs,”** published 12 June 2013:

<https://www.macgeekgab.com/episode/453/>

The complete show notes list `Enabling TRIM on Crucial SSD?` and the distinctive title `My SSD used to be so much faster… What happened?`. Used only to establish that the named support resource was already part of contemporaneous public discussion by that date. It does not preserve the support article body in the inspected record.

### C2 — Overclockers UK, 29 September 2014 — `S/period`, page-metadata/body preservation witness

**“SSD died twice, prevention ?”**:

<https://forums.overclockers.co.uk/threads/ssd-died-twice-prevention.18626927/?starter_only=1>

The thread reproduces the Crucial article title, author/moderator attribution, `01-17-2013 04:30 PM` creation metadata, `10-23-2013 09:41 AM` edit metadata, and later AGC/powered-idle wording. Used as a later secondary preservation of the page header and body, not as an authenticated Crucial archive.

### C3 — Prylmani, 18 August 2013 — `S/period`, detailed support-correspondence preservation witness

August 2013 archive entry reproducing a Crucial support reply concerning a Crucial V4 SSD:

<https://prylmani.blogspot.com/2013/08/>

Used as the safer surviving floor for the detailed `Active Garbage Collection` + `6–8 hours` powered-idle procedure.

### C4 — MacRumors, 22 March 2014 — `S/period`, vendor-website quotation witness

**“Which SSD - Crucial or OWC?”**:

<https://forums.macrumors.com/threads/which-ssd-crucial-or-owc.1718624/>

Preserves a passage explicitly introduced as an extract from Crucial's website under `Crucial SSDs and TRIM/Garbage Collection`. Used for period vocabulary and continuity, not as an origin archive.

### P1 — Crucial maintained support article — `H/P-current`, continuity comparison only

Crucial Support, **“SSD used to be faster but has slowed down”**:

<https://www.crucial.jp/support/articles-faq-ssd/ssd-used-to-be-faster-but-has-slowed-down>

Used only as the current vendor contract already grounded elsewhere in Case 150. The current page is not back-projected into 2013.

---

## 14. Result and remaining debt

This slice tightens but does not eliminate the provenance debt.

Closed / narrowed:

- the **named support-resource existence floor** moves from the earlier August 2013 witness to **12 June 2013** via an independent contemporaneous link/title record;
- a later quotation preserves **reported page creation metadata of 17 January 2013** and **edit metadata of 23 October 2013**;
- chronology is now explicitly version-aware: the detailed 2014 body is not silently back-dated to January.

Still open:

1. recover an authenticated Crucial-origin or web-archived capture from **January–October 2013**;
2. compare at least two historical body revisions to determine what changed on or before the reported 23 October 2013 edit;
3. recover the exact link target from the June 2013 show notes through an archived HTTP/page capture rather than title matching alone;
4. keep documentation chronology separate from firmware/product implementation chronology;
5. keep broad support-site migration and Crucial product genealogy in `computing-archaeology` if pursued.

The final bounded chronology is therefore:

```text
17 Jan 2013   reported origin-page creation metadata
              (secondary preservation; body version unknown)

12 Jun 2013   independent contemporaneous named-resource witness
              (page/resource existed publicly by this date)

18 Aug 2013   detailed 6–8 h AGC support text preserved
              (support-correspondence reproduction)

23 Oct 2013   reported page edit metadata
              (what changed remains unknown)

29 Jan 2014   first-party M550 flyer revision
              (AGC + TRIM separately advertised)

18 Mar 2014   first-party M550 availability announcement

22 Mar 2014   vendor-site AGC/TRIM wording quoted publicly
```

The key boundary is simple:

> **earlier page identity != earlier proof of the same text version.**
