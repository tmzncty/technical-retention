# Case 02 Deepening — RCA/Rajchman Filing, Public Disclosure, and Later Patent Publication Provenance (1952–1959)

**Status:** `bounded deepening complete`

**Canonical case:** [`../cases/02-magnetic-core-destructive-read.md`](../cases/02-magnetic-core-destructive-read.md)

**Evidence navigation:** [`02-core-retention-evidence-index.md`](02-core-retention-evidence-index.md)

## Purpose

Case 02 already has a strong 1952 RCA mechanism witness: Jan A. Rajchman's June 1952 paper, `Static Magnetic Matrix Memory and Switching Circuits`, publicly describes stable magnetic states, no-holding-power retention, an operating 256-bit experimental model, and access-triggered restoration.

This slice does **not** repeat that mechanism history. It closes a narrower provenance problem left open by the Case-02 evidence index:

> how should the repository relate a later patent's recital of an earlier application filing to the date of a public technical disclosure, a later patent publication/issue, and an invention-priority claim?

The answer is deliberately conservative. The records inspected here support a chronology of **document events**. They do not, by themselves, adjudicate who first conceived magnetic-core memory, when an unpublished application first became publicly inspectable, or which filed embodiment first became a production machine.

The bounded distinction is:

```text
application filing event
    !=
public technical disclosure
    !=
patent publication / issue
    !=
product embodiment
    !=
invention-priority adjudication
```

Claim layers remain separate: **Historical record**, **Engineering reconstruction**, **Functional analogy**, and **Philosophical interpretation**.

---

## Why this slice belongs in `technical-retention`

A broad genealogy of RCA magnetic-memory patents, laboratory groups, assignees, inventors, manufacturing, and product adoption belongs primarily in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology).

The retention-specific problem here is evidence control. Case 02 uses the June 1952 Rajchman paper as a public technical witness for quiescent no-holding-power retention plus read/restore. Later patents point backward to applications filed before or around that paper. Unless those events are typed correctly, an innocent chronology can silently turn into a false priority claim.

This file therefore treats dates as **typed evidence events** rather than as interchangeable points on one timeline.

A fresh companion-repository search for a dedicated Rajchman / RCA filing-provenance packet found no narrower module to reuse in this round.

---

# Sources inspected

## A. Jan A. Rajchman, June 1952 RCA Review paper

Existing direct Case-02 evidence already grounds:

- Jan A. Rajchman, `Static Magnetic Matrix Memory and Switching Circuits`;
- *RCA Review*, vol. XIII, no. 2, June 1952, pp. 183–201;
- period public technical description of the RCA magnetic-matrix memory;
- an operating 256-bit experimental model;
- no-holding-power quiescent retention;
- read/interrogation followed by conditional restoration.

See [`02-rca-1952-static-memory-no-holding-power-read-restore-deepening.md`](02-rca-1952-static-memory-no-holding-power-read-restore-deepening.md).

For this provenance slice, the important event type is:

```text
June 1952
PUBLIC TECHNICAL PAPER
```

The paper is not treated here as proof of first conception or first filing.

## B. Jan A. Rajchman, `US2734184A — Magnetic switching devices`

Primary patent record:

- <https://patents.google.com/patent/US2734184A/en>
- filing date shown for the issued patent: **20 February 1953**;
- publication / grant date: **7 February 1956**;
- the patent states that the relevant magnetic-switch type had been described in Rajchman's June 1952 RCA Review article;
- it further states that such switches were described in **application Serial No. 275,622, filed 8 March 1952, entitled `Magnetic Matrix and Computing Devices`**, by the applicant and assigned to the same assignee;
- it also points to copending **Serial No. 327,234, filed 22 December 1952** for related switching features.

The central evidence value is retrospective provenance:

```text
1956 patent text
    -> records existence/title/date of an earlier 8-Mar-1952 application
```

This record does **not** make the March 1952 application a March 1952 public publication.

### Source-boundary note

In this round, the repository has not directly inspected the complete original file wrapper or complete text of Serial No. 275,622. Therefore the exact scope of that application is not reconstructed from its title or from the later patent's short recital.

## C. `US2734183A — Magnetic switching devices`

Google Patents indexes a closely adjacent publication:

- <https://patents.google.com/patent/US2734183A/en>
- prior-art / filing context shown as **22 December 1952**;
- publication / grant date: **7 February 1956**.

This is relevant because `US2734184A` identifies copending Serial No. 327,234 with the same 22 December 1952 filing date.

However, this round does not rely on an inferred one-to-one mapping between a serial number and this publication unless the relation is directly visible in a primary record. The safe result is simply that a public patent record exists for a closely related Rajchman magnetic-switch filing on that date, while the exact file-wrapper genealogy remains a separate archival task.

## D. Jan A. Rajchman, `US2792563A — Magnetic system`

Primary patent record:

- <https://patents.google.com/patent/US2792563A/en>
- current application filed **1 February 1954**;
- publication / grant date **14 May 1957**;
- the patent itself states on its face `Original Filed Nov. 25, 1952`;
- the specification states that it is a **continuation of application Serial No. 322,491, filed 25 November 1952, then abandoned, entitled `Magnetic Memory System`**;
- it cites Forrester's January 1951 article and Rajchman's June 1952 RCA Review article as earlier descriptions of magnetic-core information storage.

This source permits a stronger statement than an inferred database family link because the continuation relation is written into the patent text itself.

It permits:

```text
parent application filed 25-Nov-1952
    -> later continuation filed 1-Feb-1954
    -> published / issued 14-May-1957
```

It does **not** establish that the parent application was publicly available in November 1952, nor that every claim or drawing in the 1957 publication was present unchanged in the parent.

## E. Milton Rosenberg, `US2900623A — Magnetic core memory system`

Primary later patent record:

- <https://patents.google.com/patent/US2900623A/en>
- filed **5 April 1954**;
- published / granted **18 August 1959**;
- inventor: Milton Rosenberg;
- assignee shown in the issued record: Telemeter Magnetics, Inc.;
- the specification explicitly points readers to Forrester's January 1951 paper, Rajchman's June 1952 RCA Review paper, and Rajchman's October 1953 IRE paper as prior technical descriptions.

This is valuable as a **later reception witness**. It shows those public papers functioning as acknowledged prior technical literature in a later magnetic-core patent.

It is not evidence that Rosenberg's 1954 filing was the source of Rajchman's 1952 work, and it is not a basis for assigning invention priority among MIT, RCA, or other actors.

---

# Historical record

## H1 — June 1952 is a directly inspected public-document anchor, not necessarily the earliest RCA work event

The existing Case-02 RCA record establishes a public technical paper in June 1952. That is the correct event type to attach to the public claim:

```text
By June 1952:
Rajchman's RCA magnetic-matrix work was publicly described in RCA Review.
```

The later `US2734184A` adds a different fact: its 1956 text says an application entitled `Magnetic Matrix and Computing Devices` had been filed on 8 March 1952.

Therefore the chronology can now safely say:

```text
8-Mar-1952
    later-attested application filing

June-1952
    directly inspected public technical paper
```

It should **not** say:

```text
8-Mar-1952
    public disclosure
```

unless a source establishing public availability on that date is found.

## H2 — The March 1952 filing is attested retrospectively by a later public patent

`US2734184A` was not published until 1956. Its statement about Serial No. 275,622 is therefore a later public record about an earlier filing event.

This distinction matters because a historian can know in 2026 that a filing occurred in March 1952 without thereby claiming that a member of the technical public in March 1952 could inspect that filing.

The evidence form is:

```text
later public document
    -> retrospective metadata about earlier non-public-or-unverified event
```

That is still useful primary evidence. It is simply not the same source class as the June 1952 paper.

## H3 — A November 1952 parent filing is directly named in a later continuation

`US2792563A` states that the 1954 application is a continuation of Serial No. 322,491, filed 25 November 1952 and then abandoned.

This supplies a documented application genealogy:

```text
Ser. 322,491
filed 25-Nov-1952
    ↓ continuation
US407200A
filed 1-Feb-1954
    ↓ publication / grant
US2792563A
14-May-1957
```

The parent filing date can therefore be stated without treating Google's family metadata alone as the proof.

## H4 — Later patent publication preserves an earlier development trace even where the earlier application is not directly inspected

The March and November 1952 application references illustrate two different levels of custody:

```text
Ser. 275,622:
later patent recital gives title + filing date;
complete original application not directly inspected here

Ser. 322,491:
later continuation expressly identifies parent title + date + abandoned status;
current published continuation is directly inspectable
```

This is not a trivial cataloguing detail. The strength of a chronology depends on what part of the earlier record is actually visible.

## H5 — Rosenberg's 1959 patent is a reception witness for public literature, not an origin witness for that literature

`US2900623A` explicitly names the 1951 Forrester article, the June 1952 Rajchman article, and the October 1953 Rajchman IRE article while describing the prior state of magnetic-core memory.

Thus it supports:

```text
by the mid-1950s patent-writing context,
these earlier publications were treated as prior technical descriptions
```

It does not support:

```text
Rosenberg invented the mechanisms described in the cited earlier papers
```

or:

```text
citation order resolves invention priority
```

## H6 — Filing chronology and public-literature chronology can cross without contradiction

The inspected record now contains at least four event types:

| Date | Event | Evidence class |
| --- | --- | --- |
| Jan. 1951 | Forrester public article cited by later RCA/Rosenberg patents | public technical literature |
| 8 Mar. 1952 | Rajchman application Ser. 275,622, as later recited by `US2734184A` | retrospectively attested filing |
| Apr. 1952 | Papian public IRE article, already grounded elsewhere in Case 02 / Case 70 | public technical literature |
| Jun. 1952 | Rajchman RCA Review paper | directly inspected public technical literature |
| 25 Nov. 1952 | Rajchman parent Ser. 322,491, expressly named by later continuation | parent filing attested by continuation |
| 22 Dec. 1952 | related Rajchman magnetic-switch filing context | filing / later patent context |
| 20 Feb. 1953 | application leading to `US2734184A` | filing |
| 1 Feb. 1954 | continuation leading to `US2792563A` | filing |
| 5 Apr. 1954 | Rosenberg application leading to `US2900623A` | filing |
| 7 Feb. 1956 | `US2734184A` publication / grant | public patent record |
| 14 May 1957 | `US2792563A` publication / grant | public patent record |
| 18 Aug. 1959 | `US2900623A` publication / grant | public patent record |

This table is a document chronology, **not** an invention-priority ranking.

---

# Engineering reconstruction

## E1 — Provenance needs an event type, not just a date

For technical-retention research, a date without its event type is unsafe.

A compact evidence tuple is:

```text
claim
+ actor / document
+ event type
+ event date
+ public-availability status
+ custody strength
```

For example:

```text
"Serial No. 275,622 existed"
+ Rajchman / RCA-related patent chain
+ application filing
+ 8-Mar-1952
+ public availability on that date not established here
+ later primary patent recital
```

That is stronger and more reproducible than attaching `1952` to an undifferentiated `prior art` label.

## E2 — Later visibility of an earlier filing does not move the public-disclosure floor backward automatically

A later patent can preserve metadata about an earlier event.

That creates two times:

```text
time of underlying event
    !=
time at which the inspected public record exposes that event
```

The historical event may be real and earlier. The evidence available to contemporaries may nevertheless be later.

This is why the repository should keep:

```text
application filing floor
    !=
public-document floor
```

## E3 — A continuation relation preserves genealogy without proving identical contents

`US2792563A` gives a formal continuation relation to the November 1952 parent. That is meaningful legal/document genealogy.

But a safe technical reconstruction still separates:

```text
continuity of application family
    !=
identity of every claim
    !=
identity of every drawing
    !=
proof that every 1957-described detail was present in the parent exactly as published
```

The published continuation may be used to establish the relation it expressly states; it should not become a time machine for every later sentence.

## E4 — Patent citation is evidence of reception, not automatic evidence of technical descent

When Rosenberg cites Forrester and Rajchman, the citation is evidence that those works were recognized as relevant prior technical descriptions in that patent's framing.

It does not by itself show:

- direct collaboration;
- copying of a particular circuit;
- identical material selection;
- identical restore sequence;
- a single institutional genealogy.

For repository purposes:

```text
cited as prior technical literature
    !=
direct implementation lineage
```

## E5 — Product adoption is another independent event type

None of the patent dates in this slice demonstrates named product shipment or production deployment.

Case 02 already uses other machine manuals and reports for product/system behavior. That division should remain intact:

```text
paper / patent mechanism evidence
    !=
named-machine operational evidence
```

This avoids turning an RCA filing chronology into an unsupported claim about IBM, DEC, Whirlwind, or a commercial RCA product.

---

# Functional analogy

A limited analogy applies to other repository cases where the meaning of a technical state depends on a versioned contract or evidence epoch.

For example, a later standard revision can tell us how a mechanism was specified at that revision without proving that the same rule applied unchanged in an earlier revision. Likewise, a later patent can tell us that an earlier filing existed without making every sentence in the later publication contemporaneous with the earlier filing.

The shared functional relation is:

```text
current visible record
    can preserve evidence about an earlier state
```

but:

```text
retrospective visibility
    !=
contemporaneous public visibility
```

This is an evidence-management analogy only. It does not claim that patent prosecution and memory-state recovery are technically the same mechanism.

---

# Philosophical interpretation

The chronology illustrates a bounded distinction between **an event having happened** and **that event being publicly available as evidence**.

An application can have a filing date before a public paper while the paper remains the earlier directly inspected public technical disclosure. A later patent can preserve the trace of that prior filing. In that limited sense, documentary history itself has retention layers:

```text
past technical act
    !=
public record at the time
    !=
later surviving evidence of the act
```

This is a methodological interpretation, not a claim that patent offices are storage systems equivalent to magnetic memory, and not a theory of invention priority.

---

# Prior-art and anti-anachronism boundaries

The following claims are **not established** by this slice:

1. Rajchman was the first inventor of magnetic-core memory.
2. RCA was the first institution to conceive coincident-current magnetic memory.
3. Serial No. 275,622 was publicly available on 8 March 1952.
4. Every detail later mentioned in `US2734184A` was present verbatim in Serial No. 275,622.
5. The title `Magnetic Matrix and Computing Devices` is enough to reconstruct the full technical scope of Serial No. 275,622.
6. The later patent recital establishes a legal priority judgment against Forrester, Papian, or any other actor.
7. Filing before publication means conception occurred on the filing date.
8. Filing order is equivalent to invention order.
9. Publication order is equivalent to invention order.
10. Patent grant date is equivalent to first technical disclosure.
11. A continuation contains exactly the same claims or drawings as its parent.
12. The 25 November 1952 parent of `US2792563A` was publicly inspectable on its filing date.
13. A later patent's citation to an earlier paper proves direct circuit descent.
14. Rosenberg's 1954 filing is the source of Rajchman's 1952 mechanism.
15. The RCA 256-bit experimental unit implemented every circuit later appearing in the patents discussed here.
16. Any cited patent demonstrates a named shipping product.
17. The record resolves broad MIT-versus-RCA invention-priority disputes.
18. The record settles exact internal RCA chronology before March 1952.
19. The record establishes the complete disposition or public mapping of every cited serial-number application.
20. Patent-family database metadata should override express text in the inspected primary document where they differ.

---

# Claim ledger

| Claim | Layer | Evidence strength | Boundary |
| --- | --- | ---: | --- |
| Rajchman's magnetic-matrix paper was publicly published in June 1952 | Historical record | strong primary / existing direct Case-02 record | public paper date; not first-conception claim |
| `US2734184A` states that Ser. 275,622, `Magnetic Matrix and Computing Devices`, was filed 8 Mar. 1952 | Historical record | strong later primary recital | filing metadata; original complete application not inspected here |
| `US2734184A` points to a related copending Ser. 327,234 filed 22 Dec. 1952 | Historical record | strong later primary recital | exact complete genealogy remains bounded |
| `US2792563A` states it continues Ser. 322,491 filed 25 Nov. 1952 and then abandoned | Historical record | strong primary continuation statement | parent filing != public availability on filing date |
| `US2900623A` cites Forrester 1951 and Rajchman 1952/1953 as earlier technical descriptions | Historical record | strong later primary reception evidence | citation != invention priority or implementation genealogy |
| filing event and public-disclosure event should be recorded separately | Engineering reconstruction | strong, directly required by chronology | modern evidence-control rule |
| a later publication can preserve evidence of an earlier filing without backdating public availability | Engineering reconstruction | strong | no legal priority adjudication |
| application-family continuity means every later technical detail existed unchanged in the parent | `X` | rejected | unsupported overreach |
| filing order determines first invention | `X` | rejected | unsupported / legal-historical overreach |
| patent citation proves direct engineering descent | `X` | rejected | reception evidence only |

---

# Resulting bounded distinctions

```text
filing date
    !=
public availability date

application family relation
    !=
identity of technical contents across every stage

later patent recital
    !=
direct inspection of the earlier file

public paper
    !=
patent application

patent publication / grant
    !=
first technical disclosure

citation as prior literature
    !=
direct implementation genealogy

filing chronology
    !=
invention-priority adjudication

mechanism evidence
    !=
named-product deployment evidence
```

---

# Relationship to Case 02

Case 02 remains **`grounded`**. This slice does not change the maturity classification.

It strengthens the evidence chain by removing one provenance ambiguity around the 1952 RCA record:

```text
Rajchman June-1952 public paper
    = public technical anchor already inspected

8-Mar-1952 RCA-related application
    = earlier filing event attested by a later primary patent

therefore:
    earlier filing can be recorded
    without silently backdating public technical disclosure
```

That improves prior-art hygiene but does not close other Case-02 questions about dormant-retention distributions, exact early power-transition behavior, production deployment, or cross-machine reliability.

---

# Remaining bounded debt after this slice

The former broad debt `exact patent chronology around Rajchman/Rosenberg` is now narrowed rather than treated as completely exhausted.

High-value follow-ons are:

- obtain and directly inspect the original file wrapper / complete contents for **Serial No. 275,622** if an accessible archival copy can be found;
- resolve the exact public patent mapping and disposition of **Serial No. 327,234** from a direct record rather than title/date inference;
- search for contemporaneous RCA internal, conference, laboratory, or correspondence material **before June 1952** that can establish what was documented before the public RCA Review paper;
- keep legal invention-priority disputes outside the repository unless a later bounded project explicitly requires them and can inspect the relevant prosecution/interference record.

These are provenance tasks. They do not require repeating the already-grounded mechanism description in the June 1952 paper.

---

# Sources

1. Jan A. Rajchman, `Static Magnetic Matrix Memory and Switching Circuits`, *RCA Review*, vol. XIII, no. 2, June 1952, pp. 183–201. Existing source-custody and mechanism notes: [`02-rca-1952-static-memory-no-holding-power-read-restore-deepening.md`](02-rca-1952-static-memory-no-holding-power-read-restore-deepening.md).
2. Jan A. Rajchman et al., `Magnetic switching devices`, U.S. Patent 2,734,184, filed 20 February 1953, issued 7 February 1956: <https://patents.google.com/patent/US2734184A/en>.
3. `Magnetic switching devices`, U.S. Patent 2,734,183, issued 7 February 1956, associated with 22 December 1952 filing context: <https://patents.google.com/patent/US2734183A/en>.
4. Jan A. Rajchman, `Magnetic system`, U.S. Patent 2,792,563, continuation filed 1 February 1954, issued 14 May 1957; specification states original parent Ser. 322,491 was filed 25 November 1952: <https://patents.google.com/patent/US2792563A/en>.
5. Milton Rosenberg, `Magnetic core memory system`, U.S. Patent 2,900,623, filed 5 April 1954, issued 18 August 1959: <https://patents.google.com/patent/US2900623A/en>.

## Source-custody note

Google Patents is used here as a convenient rendering/index of the issued U.S. patent text and bibliographic metadata. Where a claim depends on an earlier serial-number filing, the file distinguishes an **express recital in the later patent** from direct inspection of the earlier application. Database-derived `priority` fields are not used as a substitute for that distinction.
