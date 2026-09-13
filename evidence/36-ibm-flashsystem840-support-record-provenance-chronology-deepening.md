# Case 36 Deepening — IBM FlashSystem 840 Support-Record / Attachment Provenance Chronology

## Purpose

This addendum closes one narrow source-control ambiguity left open by [`36-ibm-flashsystem840-2014-2015-commercial-refresh-deepening.md`](36-ibm-flashsystem840-2014-2015-commercial-refresh-deepening.md):

> What can the current IBM Support page's `Original Publication Date: 16 October 2013` actually date, given that the current page points to a FlashSystem 840-specific attachment named `External-6-6-14.pdf` and the public FlashSystem 840 / V840 product chronology is later?

**Bounded result:** the 16-October-2013 value is safe evidence for the **support record / page identity's own original-publication metadata**, but it is not safe evidence that the **current 840-specific attachment**, the current 840/V840 abstract, or their present wording already existed on that date. IBM's own product chronology shows FlashSystem 840 public announcement references on 17 December 2013 and general availability on 24 January 2014; IBM publicly introduced FlashSystem V840 in February 2014, with the storage-enclosure models reaching general availability on 7 March 2014. The current attachment itself carries the date-coded name `External-6-6-14.pdf`.

The source-history distinction is therefore:

```text
support-record original-publication metadata
    !=
current page revision/content date
    !=
current attachment revision/publication date
    !=
product announcement date
    !=
product general-availability date
```

This repairs the earlier shorthand `metadata conflicts with product chronology`. The stronger, better-supported statement is that **one persistent IBM support record now exposes metadata and attached/current content from different chronological layers**. Exact first-publication time of the current PDF remains unresolved.

## Sources inspected

### A. Current IBM Support record — `Flash Data Retention`

<https://www.ibm.com/support/pages/flash-data-retention>

The current page exposes all of the following at once:

- abstract: `This document discusses techniques used by the FlashSystem 840 and FlashSystem V840...`;
- `Original Publication Date`: **16 October 2013**;
- attached file: `Flashsystem 840 Data Retention - External-6-6-14.pdf`;
- current modified date: **17 February 2023**;
- stable support UID: **`ssg1S7004533`**.

These fields are manufacturer-primary provenance evidence for the current support record. They do **not** themselves say that every currently attached object or every current body field was present unchanged on 16 October 2013.

**Evidence class:** `H/P` for the exposed IBM metadata; `E` for the source-version inference below.

### B. Current attached IBM PDF

<https://www.ibm.com/support/pages/system/files/support/ssg/ssgdocs.nsf/0/e02429f9c68ec7ea85257c0600743ccd/$FILE/Flashsystem%20840%20Data%20Retention%20-%20External-6-6-14.pdf>

The current one-page attachment names **FlashSystem 840** directly and states the already-grounded product behavior: automatic refresh of host-unchanged data, an up-to-90-day / up-to-40 °C powered-off envelope, and automatic `deep scrub and refresh` after more than seven days powered off.

The public filename and document title expose the date-coded label **`External-6-6-14`**. This is strong provenance for the identity of the current attached artifact, but the inspected page does not contain a formal publication/revision field saying what `6-6-14` means. The repository therefore records it as a **date-coded artifact label**, not as an independently authenticated publication date.

The PDF's page-level text was inspected. Image rendering was not available in the research environment, so no claim here depends on a visual feature beyond the extracted text/title/filename.

**Evidence class:** `H/P` for the current IBM attachment and artifact label; `X` against silently converting the filename into a certified release date.

### C. IBM United States Hardware Announcement 114-032 — 16 January 2014

<https://www.ibm.com/docs/en/announcement_archive/ENUS114-032/ENUS114-032.PDF>

IBM's 16-January-2014 announcement is explicitly titled `Revised availability: Select FlashSystem 840 features`. It identifies machine type-models **9840-AE1** and **9843-AE1**, says selected features were moved from a planned availability of 24 January 2014 to 7 March 2014, and points readers to the complete FlashSystem 840 product information in Hardware Announcements **113-173** and **113-183**, both dated **17 December 2013**.

This provides a first-party public chronology boundary for the 840 name/product family:

```text
17 Dec 2013 — referenced complete-product announcement records
16 Jan 2014 — revised-availability announcement
24 Jan 2014 — base product GA date in IBM lifecycle records
```

The announcement date is not an invention date and is not evidence about when internal IBM/TMS engineering or draft documentation began.

**Evidence class:** `H/P`.

### D. IBM lifecycle records — 9840-AE1 and 9843-AE1

Current IBM product-lifecycle records:

- 9840-AE1: <https://www.ibm.com/support/pages/node/7094794>
- 9843-AE1: <https://www.ibm.com/support/pages/node/7092436>

Both records identify the products as **IBM FlashSystem 840** and give **24 January 2014** as General Availability.

This independently prevents a source-control shortcut in which the support page's October-2013 node date is treated as the GA date or as proof that the current attached 840 document was a public shipped-product document at that time.

**Evidence class:** `H/P`.

### E. IBM FlashSystem V840 public chronology

IBM's own 11-February-2014 storage announcement/blog calls the V840 a new IBM FlashSystem V840 Enterprise Performance Solution:

<https://community.ibm.com/community/user/blogs/tony-pearson1/2014/02/11/fall-in-love-with-ibm-flashsystem-v840-enterprise-performance-solution>

IBM's lifecycle pages give **7 March 2014** as General Availability for V840 storage-enclosure models 9846-AE1 and 9848-AE1:

- <https://www.ibm.com/support/pages/node/7093190>
- <https://www.ibm.com/support/pages/node/7093208>

IBM Redbooks' V840 Product Guide was published at the end of February / beginning of March 2014 and describes the named product:

<https://www.redbooks.ibm.com/abstracts/tips1158.html>

This matters because the **current** `Flash Data Retention` support-page abstract names **both 840 and V840** while the page simultaneously exposes an `Original Publication Date` of 16 October 2013. That combination is direct evidence that the current page body/metadata surface is not a trustworthy frozen snapshot of one October-2013 document revision.

It does **not** prove the exact date on which IBM first edited that support record to mention V840.

**Evidence class:** `H/P` for the product chronology; `E` for the revision-layer conclusion.

## Historical record

### H/P — the support record has a persistent identity across revisions

The current page has UID `ssg1S7004533`, an original-publication field dated 16 October 2013, a current modified date of 17 February 2023, a current abstract naming both 840 and V840, and a current attachment whose public filename carries `External-6-6-14`.

At minimum, IBM's current support system is presenting a **record whose identity and original-date field persist while other visible fields and attachments can reflect later revisions**.

The safe historical claim is therefore:

> IBM currently reports that support record `ssg1S7004533` originated on 16 October 2013.

The unsafe stronger claim is:

> the current 840/V840 wording and current `External-6-6-14.pdf` were publicly available in this exact form on 16 October 2013.

No inspected first-party source establishes the stronger claim.

### H/P — FlashSystem 840's public product chronology is later than the support record's original-date field

IBM Announcement 114-032 points to the complete 840 product announcements of 17 December 2013 and identifies January/March 2014 availability dates. IBM's current lifecycle records give 24 January 2014 GA for 9840-AE1 and 9843-AE1.

Thus:

> **support-record original date != FlashSystem 840 public product-announcement / GA date**.

This does not make the support record metadata erroneous. It means that the metadata field is dating a record identity, not automatically every current artifact attached to it.

### H/P — the current abstract contains an even later product name

The current support-page abstract names V840. IBM's own public announcement/blog names V840 as a new solution on 11 February 2014, and current IBM lifecycle records put the V840 storage-enclosure GA on 7 March 2014.

Therefore the current abstract is itself a **later-content witness** relative to the page's 16-October-2013 original-date field.

This is the cleanest negative control in the slice:

```text
Original Publication Date of support record
    !=
date of every string currently displayed on that record
```

### H/P — the current attachment is a 840-specific artifact with a 2014-coded filename

The linked PDF's current filename/title is `Flashsystem 840 Data Retention - External-6-6-14`. The repository does not expand `6-6-14` into a formal publication date because no inspected IBM document-control field states that meaning.

What the filename can safely do is bound provenance qualitatively:

> the current artifact is **not source-controlled as an October-2013 frozen attachment** merely because the enclosing support record says `Original Publication Date: 16 October 2013`.

## Engineering / source-control reconstruction

### E — a durable record identifier can outlive one content revision

This is a source-provenance issue rather than an SSD mechanism claim, but it mirrors a general rule needed throughout the repository:

```text
stable identifier
    !=
stable payload
    !=
stable revision metadata
```

A persistent IBM Support UID can continue to designate a support topic while its abstract, product associations, attachments, and modified date evolve.

This is **not** a claim that IBM Support internally implements any particular version-control model. It is only the minimum inference required by the mutually dated fields currently exposed.

### E — document chronology must be typed by object

The earlier evidence record used the phrase `metadata conflicts with product chronology`. That is too coarse because several different objects are being dated:

- support-record creation/original-publication metadata;
- current support-page body/abstract;
- attached PDF artifact/revision;
- product announcement;
- product GA;
- later support-system migration/modification.

Once those objects are separated, there is no need to choose one date and declare the others wrong.

The repository should instead ask:

> **which object does this date actually qualify?**

### E — current vendor hosting does not erase revision history ambiguity

Current first-party hosting is strong evidence that IBM now stands behind the page and attachment as support material. It is weaker evidence for **when each sentence first became public**.

Therefore:

> **current first-party provenance != exact first-publication chronology of the current revision**.

That distinction matters whenever a product manual/support article is used to set a technology's earliest public evidence floor.

## Functional comparison and limits

### Functional comparison to version/currentness cases

At a very abstract level, this source-provenance problem resembles the repository's broader distinction between stable designation and current embodiment: a stable support UID points to a current content representation that need not be byte-identical to its original revision.

That is a **functional analogy only**. IBM Support document management is not being identified with an FTL, distributed currentness protocol, or any other storage mechanism in the repository.

### No philosophical promotion

The revision layering is useful methodological evidence about how technical sources themselves persist and change. It is not evidence that IBM engineers were making a philosophical claim about identity, memory, or retention.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| IBM currently reports `Original Publication Date: 16 October 2013` for support record `ssg1S7004533` | H/P | current IBM Support page |
| IBM currently reports `Modified date: 17 February 2023` for the same support record | H/P | current IBM Support page |
| The current page abstract names both FlashSystem 840 and V840 | H/P | current IBM Support page |
| The current page links `Flashsystem 840 Data Retention - External-6-6-14.pdf` | H/P | current IBM Support page |
| The attached PDF itself is FlashSystem-840-specific and describes automatic refresh / post-off deep scrub | H/P | current IBM attachment |
| IBM Announcement 114-032 points to complete FlashSystem 840 announcements dated 17-Dec-2013 | H/P | IBM Hardware Announcement 114-032 |
| IBM lifecycle records give 24-Jan-2014 GA for 9840-AE1 and 9843-AE1 | H/P | IBM lifecycle records |
| IBM publicly announced the V840 as a new solution in February 2014; V840 storage-enclosure lifecycle records give 7-Mar-2014 GA | H/P | IBM announcement/blog + lifecycle records |
| `16-Oct-2013` securely dates the current attached PDF | X | the field is attached to the support record; current content/attachment expose later product/revision evidence |
| `16-Oct-2013` securely dates the current 840/V840 abstract wording | X | V840 is a later public product; exact page-revision date remains unknown |
| `External-6-6-14` is independently authenticated as the PDF's formal publication date | X | it is a date-coded filename/title; no inspected formal revision field defines it |
| FlashSystem 840 was generally available in October 2013 | X | IBM lifecycle records give 24-Jan-2014 GA |
| Support-node original date and product-announcement date must be identical | X | they qualify different objects/events |
| Current first-party hosting proves exact first-publication date of each current sentence | X | current provenance and revision chronology are different evidence questions |

## Relation to the parent Case 36 evidence

The parent commercial-product deepening remains valid on its substantive retention claims. Nothing in this chronology cleanup weakens the manufacturer-primary evidence that the current IBM attachment documents automatic refresh and post-power-off `deep scrub and refresh` for FlashSystem 840.

What changes is only the date/provenance wording:

**Old shorthand:**

> `Original Publication Date: 16 October 2013` conflicts with the 840 product chronology and attachment filename.

**Revised bounded statement:**

> IBM's current support record reports an original date of 16 October 2013, but the current record body and attachment incorporate later product/revision layers. That field therefore cannot by itself date the current 840/V840 wording or the current `External-6-6-14.pdf`. The 840 public-announcement floor is bounded by IBM's 17-December-2013 announcement references and 24-January-2014 GA, while the exact first-publication date of the current PDF remains open.

This is a source-control correction, not a change to the retention mechanism.

## Related-repository audit

A fresh GitHub search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `FlashSystem 840` returned no dedicated case to reuse in this slice.

The division of labor therefore remains:

- detailed TMS -> IBM product/controller genealogy and archival product-document chronology can move to `computing-archaeology` if it becomes a substantial hardware-history investigation;
- this repository keeps the narrow evidentiary rule needed by Case 36: do not use support-record metadata as an untyped earliest-publication date for a later attached product document.

## Remaining open work

This slice **closes the interpretation of the 16-Oct-2013 page field**: it is not a secure date for the current attachment or current abstract.

Still open:

- an archived 2013 snapshot of UID `ssg1S7004533` showing its original title/body/attachment, if any;
- IBM-internal or externally preserved document-control metadata that formally defines the `External-6-6-14` label;
- the exact first public availability date of the current one-page PDF;
- whether an earlier pre-840 / generic Flash-retention support article occupied the same UID before later revision;
- firmware/source-level reconstruction and independent validation of the 840 refresh mechanism, which remain separate engineering debts.

## Sources

1. IBM Support, **`Flash Data Retention`**, UID `ssg1S7004533`: <https://www.ibm.com/support/pages/flash-data-retention>.
2. IBM, **`Flashsystem 840 Data Retention - External-6-6-14.pdf`**: <https://www.ibm.com/support/pages/system/files/support/ssg/ssgdocs.nsf/0/e02429f9c68ec7ea85257c0600743ccd/$FILE/Flashsystem%20840%20Data%20Retention%20-%20External-6-6-14.pdf>.
3. IBM United States Hardware Announcement **114-032**, 16 January 2014: <https://www.ibm.com/docs/en/announcement_archive/ENUS114-032/ENUS114-032.PDF>.
4. IBM product lifecycle, **FlashSystem 840 (9840-AE1)**: <https://www.ibm.com/support/pages/node/7094794>.
5. IBM product lifecycle, **FlashSystem 840 (9843-AE1)**: <https://www.ibm.com/support/pages/node/7092436>.
6. IBM Storage announcement/blog, **`Fall In Love with IBM FlashSystem V840 Enterprise Performance Solution`**, 11 February 2014: <https://community.ibm.com/community/user/blogs/tony-pearson1/2014/02/11/fall-in-love-with-ibm-flashsystem-v840-enterprise-performance-solution>.
7. IBM product lifecycle, **FlashSystem V840 Storage Enclosure (9846-AE1)**: <https://www.ibm.com/support/pages/node/7093190>.
8. IBM product lifecycle, **FlashSystem V840 Storage Enclosure (9848-AE1)**: <https://www.ibm.com/support/pages/node/7093208>.
9. IBM Redbooks, **`IBM FlashSystem V840`** Product Guide, published 28 February 2014 (current Redbooks page): <https://www.redbooks.ibm.com/abstracts/tips1158.html>.
