# Evidence 150 — Crucial 2013–2015 AGC Provenance and m4 Experiment Boundary

## Status

**`bounded deepening complete`**

This record deepens [Case 150 — Crucial M550 Active Garbage Collection](../cases/150-crucial-m550-active-garbage-collection.md). It narrows two open debts without pretending to reconstruct proprietary Crucial firmware:

1. how far back the surviving public record carries Crucial's powered-idle / `6–8 hours` Active Garbage Collection support wording; and
2. what a peer-reviewed named-device recovery experiment on a Crucial m4 actually proves about TRIM, garbage collection, and stale-data recoverability.

The result is deliberately asymmetric. The 2013–2014 support wording is preserved by contemporaneous third parties rather than an authenticated Crucial archive, so it narrows chronology without becoming a primary-origin web capture. The 2014 SecureComm experiment is a named-device scholarly observation, but its inference that the tested m4 therefore had no background garbage collector is stronger than the measured evidence supports.

The bounded retention claim is:

> **Powered time, maintenance-engine presence, logical invalidation knowledge, reclaim eligibility, garbage-collection execution, physical erase, and later host-level recoverability are separate relations. A stale-data recovery result can show that physical embodiments survived a tested path; it does not by itself prove that the controller lacked a garbage collector.**

---

## Bounded question

The canonical case already grounds, from a 2014 M550 product flyer and maintained Crucial documentation, that `Active Garbage Collection` and `TRIM support` are separate advertised relations and that powered idle can be maintenance opportunity.

The remaining seam was historical and experimental:

```text
modern maintained support wording
    ?= period support wording

recoverable stale data after quick format
    ?= proof that no background garbage collector exists
```

This slice answers both conservatively:

```text
2013/2014 contemporaneous preservation witnesses
    -> support wording circulated by then
    != authenticated origin-hosted Crucial archive

recoverable stale data in one tested path
    -> physical embodiments remained recoverable under that path
    != proof that GC firmware was absent
```

---

## 1. Historical record — an August 2013 public reproduction preserves Crucial support's 6–8-hour procedure

A Swedish-language personal blog post dated **18 August 2013** says the author had received an email from Crucial concerning a **Crucial V4 SSD** and reproduces the English support reply.

The reproduced message says, in substance, that:

- Crucial SSDs contain a feature called `Active Garbage Collection`;
- extended operation of that feature can clean deleted cells and restore the SSD to a healthy state;
- the SSD should be left **idle for 6 to 8 hours**;
- on a desktop, the SATA data cable can be disconnected while power remains connected;
- on a laptop, the system can be left in BIOS for the same interval;
- the hard-disk power setting should be changed to `never` so the drive retains powered idle opportunity.

This is valuable because it moves the public-circulation floor of the support procedure substantially earlier than Crucial's maintained 2024 page.

But its evidence class must remain exact:

> **It is a contemporaneous user-preserved reproduction of purported Crucial support correspondence, not an authenticated Crucial-origin archive.**

Therefore it supports:

```text
Crucial-branded AGC + 6–8 h powered-idle wording
    publicly preserved by 18 Aug 2013
```

but not:

```text
all wording independently authenticated as an unmodified Crucial primary document
```

Nor does a V4 support message prove the exact scheduler of the later M550.

---

## 2. Historical record — a March 2014 forum post preserves a quotation attributed to Crucial's website

A MacRumors post dated **22 March 2014** introduces a passage as an extract from Crucial's website under the heading **“Crucial SSDs and TRIM/Garbage Collection.”** The reproduced passage says that not all operating systems support TRIM, that Crucial SSDs have `Active Garbage Collection`, and that garbage collection is part of the SSD/firmware rather than being dependent on the host operating system or filesystem.

Again, this is not an archived Crucial page. It is a contemporaneous quotation attributed to the vendor site.

Its proper historical use is therefore narrower:

```text
by Mar 2014:
public discussion preserved vendor-attributed wording
that treated AGC as controller/firmware-local
and distinguished it from OS TRIM support
```

This strengthens the chronology around the M550 launch period without silently promoting a forum quotation into primary-origin documentation.

The surviving quotation is especially useful beside the M550 flyer, which independently and directly lists `Active Garbage Collection` and `TRIM support` as separate product features. The two source roles are different:

- the **M550 flyer** is first-party product evidence;
- the **forum quotation** is a contemporaneous preservation/provenance witness for support vocabulary.

---

## 3. Experiment — SecureComm 2014 tests a named Crucial m4 under three attachment/OS paths

Zubair Shah, Abdun Naser Mahmood, and Jill Slay's peer-reviewed SecureComm 2014 paper, published in the 2015 revised proceedings, identifies one test device as:

- **Crucial M4 SSD CT064M4SSD2**;
- 64 GB;
- 2.5-inch form factor.

The experiment is not on the M550. It is useful as a nearby named Crucial product-family witness and as a controlled warning about what can and cannot be inferred from recoverability observations.

### Experiment 1 — USB attachment

The authors connect the Crucial m4 through a Kingston USB case, fill almost the entire drive with repeated JPEG data, quick-format it, reboot, and then run file recovery. They report recovering **17,625 of 17,627** images after a recovery scan lasting roughly 32 hours.

From this outcome the paper concludes that the m4 `does not have background garbage collector` and that TRIM did not work in that setup.

The recovery observation is strong for the tested path:

> **Almost all of the tested pre-format file content remained recoverable after the quick-format / USB sequence.**

The device-feature conclusion is weaker and should not be imported uncritically into this repository.

### Experiment 2 — secondary SATA attachment

The same paper attaches the m4 as a secondary SATA device while Windows 7 resides on another primary disk. It fills a 5.85 GB partition, quick-formats it, reboots, and reports that **almost all files were recovered**. The authors state that TRIM did not work on that secondary-SATA path in their setup.

This adds an important negative control:

```text
same named SSD
    + different host attachment / OS path
        -> stale contents may remain recoverable
```

It does not identify the exact command trace delivered to the device, the firmware version, or the internal validity-map state.

### Experiment 3 — primary SATA with Windows 7 installed on the SSD

For the third setup, Windows 7 Professional is installed on each tested SSD, the SSD is attached as the primary SATA device, and the authors say TRIM is enabled through the OS/BIOS configuration.

For the Crucial m4, a 3.90 GB partition is filled with 1,522 JPEG images and then quick-formatted. After reboot, the recovery scan reports **no recoverable data** from that partition. The authors attribute the difference to TRIM operating in this setup.

The most defensible cross-experiment result is therefore:

```text
same Crucial m4 model
    + quick format
    + different host / OS command path
        -> radically different stale-data recoverability outcome
```

This is evidence that the retention/forgetting outcome is mediated by more than the bare presence of NAND cells.

---

## 4. Engineering reconstruction — recoverability does not diagnose garbage-collector presence by itself

The paper's explicit conclusion that the m4 `does not have background garbage collector` does not follow uniquely from the measured recovery result.

A managed-Flash controller must distinguish pages that remain authoritative from pages it is allowed to discard. If the host path does not deliver deallocation/TRIM evidence, or if the controller otherwise still treats those logical contents as current, then a garbage collector may have to **preserve** those pages while reclaiming mixed erase blocks.

Therefore the repository separates:

```text
GC engine implemented
    != stale pages classified reclaimable
    != maintenance opportunity available
    != GC scheduled on those pages
    != containing block physically erased
    != stale payload unrecoverable through the tested interface
```

The experiment measures the last relation directly enough for its setup. It does not directly instrument the first five.

This matters because `garbage collection` is not synonymous with `erase everything that the filesystem no longer names`. The controller needs a device-level basis for deciding which physical embodiments are obsolete.

So:

> **successful forensic recovery after quick format ≠ proof that the SSD lacks garbage collection.**

Conversely:

> **vendor advertisement of garbage collection ≠ proof that a particular stale embodiment will be erased before a later recovery attempt.**

Both overclaims are rejected.

---

## 5. Engineering reconstruction — reclaim eligibility is itself retained control state

Case 150 already treats logical invalidation and physical reclamation as separate transitions. The SecureComm result makes the control-state seam easier to see.

For a controller to erase an old physical embodiment safely, it needs enough retained authority to decide that the data no longer count as current.

A simplified state chain is:

```text
host-level deletion / quick format
        ↓
possibly no device-level deallocation knowledge
        ↓
controller may still treat mapped pages as live
        ↓
GC can relocate/preserve them rather than discard them
        ↓
physical stale-looking contents remain recoverable
```

versus:

```text
host-level retirement
        ↓
TRIM / deallocation reaches device
        ↓
controller can mark affected logical ranges non-current
        ↓
reclaim/erase becomes permissible under firmware policy
        ↓
old payload may cease to be recoverable
```

The exact m4 internals are not published in the inspected evidence. These are engineering state relations, not a reverse-engineered m4 algorithm.

The broader retention point is:

> **The ability to forget safely can depend on retaining reliable evidence that a prior embodiment is no longer authoritative.**

---

## 6. Powered time remains only opportunity, not deterministic reclamation

The USB experiment is also a useful warning against a naïve reading of wall-clock power-on time. Recovery scanning ran for many hours, yet almost all old data remained recoverable in that setup.

That does **not** prove the device's internal controller performed no background work. It shows only that whatever maintenance occurred did not erase those recoverable embodiments under the tested state/path before the observation completed.

Therefore:

```text
powered for many hours
    != all reclaimable blocks erased
    != all host-obsolete data made unrecoverable
```

This complements the existing powered-idle deepening:

```text
powered idle
    != maintenance eligibility for every task
    != task execution
    != task completion
```

The additional qualifier is that maintenance work may also lack authority to discard a page when the relevant logical invalidation has not reached the controller.

---

## 7. Historical/product boundary — m4 evidence is not M550 firmware evidence

The experiment uses the Crucial **m4**, while the canonical product anchor is the later **M550**.

The sources justify only a bounded comparison:

- Crucial support vocabulary about Active Garbage Collection was circulating publicly by 2013–2014;
- a 2014 peer-reviewed experiment observed path-dependent stale-data recoverability on a named Crucial m4;
- the 2014 M550 flyer independently lists Active Garbage Collection and TRIM support.

They do **not** justify:

```text
m4 firmware scheduler == M550 firmware scheduler
```

or:

```text
m4 forensic outcome -> M550 forensic outcome
```

Controller, firmware, NAND, mapping policy, TRIM handling, and reclamation behavior can differ between product generations.

The m4 experiment is therefore an **experimental comparison witness**, not a substitute for M550-specific traces.

---

## 8. Functional comparison — Case 04 mapped Flash currentness

Case 04 establishes that logical currentness can be separated from physical location and that old physical embodiments can persist after mapping/currentness changes.

This slice adds the complementary direction:

> **if a lower layer has not received or retained sufficient retirement authority, an upper-layer deletion event need not make the corresponding physical embodiment reclaimable.**

The comparison is functional. It does not assert that the m4 uses the exact mapping structures described in Case 04's historical patent witness.

---

## 9. Functional comparison — Cases 44 / 47 sanitization and forensic remanence

A quick format in Shah et al.'s experiment is not an NVMe Sanitize operation and is not a security purge contract.

The observed difference between recoverable and unrecoverable stale data is useful precisely because it demonstrates that:

```text
namespace / filesystem retirement
    != physical trace retirement
    != sanitize completion
```

Cases 44 and 47 remain the canonical sanitize/remanence boundary. This slice does not convert a forensic recovery test into a sanitize-conformance test.

---

## 10. Prior art and related-repository boundary

No invention-priority claim is made for Active Garbage Collection, TRIM, FTL reclamation, or forensic SSD recovery.

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Active Garbage Collection Crucial M4 M550` found no dedicated case to reuse. A broad history of early commercial SSD garbage collection, Crucial controller genealogy, SATA TRIM transport, or product-by-product firmware belongs primarily there.

`technical-retention` keeps the narrower comparison:

```text
logical retirement knowledge
    + maintenance opportunity
    + controller policy
    -> conditions physical reclamation
```

---

## 11. Philosophical interpretation — bounded

A restrained interpretation is possible: technical forgetting is not simply the disappearance of a trace. A controller may need positive retained knowledge that an old embodiment has lost authority before it is safe to erase it.

That observation is grounded in the engineering distinction between currentness/deallocation state and physical reclamation. It is not a claim about human memory, social forgetting, or a universal ontology of erasure.

The experimentally visible survivor is also not automatically the `same object` in every sense. A forensic tool may recover bytes that are no longer authoritative in the filesystem or block-allocation state. Thus:

```text
forensic witness
    != authoritative current state
```

This is a project comparison term, not Shah et al.'s vocabulary.

---

## 12. Explicit non-claims

This evidence does **not** establish that:

1. the Prylmani 2013 reproduction is an authenticated Crucial-origin archive;
2. the March 2014 MacRumors quotation is a complete or independently authenticated copy of the historical Crucial webpage;
3. the exact `6–8 hours` procedure first originated in 2013;
4. the V4 and M550 use the same garbage-collection scheduler;
5. the m4 and M550 use the same controller, firmware, NAND, or internal metadata;
6. Shah et al.'s m4 definitely lacked a background garbage collector;
7. successful recovery proves that no controller-local maintenance executed during the test;
8. quick format is equivalent to TRIM, Secure Erase, Sanitize, or physical erase;
9. TRIM necessarily causes immediate physical erase on every SSD;
10. lack of TRIM means garbage collection never runs;
11. garbage collection may discard pages that the controller still regards as live;
12. the SecureComm experiment exposes the m4's internal validity map, FTL, victim-selection policy, or erase trace;
13. the primary-versus-secondary SATA result is a universal property of SATA rather than a result of the tested Windows 7 stack;
14. USB universally blocks TRIM on all later bridges/protocols;
15. hours of powered time guarantee completion of all SSD background work;
16. stale-data unrecoverability demonstrates a standards-compliant sanitize operation;
17. a forensic survivor remains authoritative current filesystem data;
18. Crucial invented Active Garbage Collection or the 6–8-hour maintenance pattern.

---

## 13. Claim ledger

| Claim | Type | Strength | Boundary |
| --- | --- | --- | --- |
| a public 18-Aug-2013 post preserves a Crucial-support-attributed 6–8-hour powered-idle AGC procedure | historical provenance | moderate | contemporaneous reproduction, not authenticated origin archive |
| a 22-Mar-2014 forum post preserves a Crucial-website-attributed description of AGC as SSD/firmware-local and OS-independent | historical provenance | moderate | contemporaneous quotation, not archived primary page |
| SecureComm tested a Crucial m4 CT064M4SSD2 64 GB | experiment / scholarly | strong | named test device, not M550 |
| m4 over USB retained 17,625/17,627 recoverable images after the tested quick-format sequence | experiment | strong for tested setup | does not identify internal GC execution |
| m4 as secondary SATA retained almost all tested files in that setup | experiment | strong for tested setup | Windows 7 / test configuration specific |
| m4 as primary SATA with Windows 7/TRIM enabled yielded no recovered data in the tested partition | experiment | strong for tested setup | not a sanitize-conformance test |
| the paper's `m4 has no BGC` conclusion is uniquely proved by its recovery observation | rejected | weak inference | recoverability cannot distinguish absence of engine from absence of discard eligibility/execution |
| reclaim eligibility and GC-engine presence are distinct relations | engineering reconstruction | strong | follows from safe managed-Flash reclamation semantics; exact m4 implementation not asserted |
| powered time alone guarantees physical reclamation | rejected | unsupported | maintenance opportunity, authority, scheduling, and completion remain separate |
| m4 experimental behavior is M550 behavior | rejected | unsupported | different product generation |

---

## 14. Source ledger

### C1 — Prylmani, 18 August 2013 — contemporaneous preservation witness

Prylmani / Andreas, August 2013 archive entry reproducing a Crucial support email concerning a Crucial V4 SSD:

<https://prylmani.blogspot.com/2013/08/>

Used only to establish a public-preservation floor for the `Active Garbage Collection` + `6–8 hours` + powered-idle support wording. It is not treated as a Crucial-origin primary source.

### C2 — MacRumors, 22 March 2014 — contemporaneous website-quotation witness

MacRumors forum thread, **“Which SSD - Crucial or OWC?”**, post #15:

<https://forums.macrumors.com/threads/which-ssd-crucial-or-owc.1718624/>

The poster attributes the quoted `Crucial SSDs and TRIM/Garbage Collection` passage to Crucial's website. Used for period vocabulary/provenance only, not as an authenticated historical webpage capture.

### A1 — Shah, Mahmood, Slay, SecureComm 2014 / published 2015 — peer-reviewed experiment

Zubair Shah, Abdun Naser Mahmood, Jill Slay, **“Forensic Potentials of Solid State Drives,”** in _10th International Conference on Security and Privacy in Communication Networks, SecureComm 2014, Revised Selected Papers_, LNICST 153, Springer, 2015, pp. 113–126, DOI `10.1007/978-3-319-23802-9_11`.

Institutional metadata:
<https://elmi.hbku.edu.qa/en/publications/forensic-potentials-of-solid-state-drives>

Open paper copy inspected:
<https://eudl.eu/pdf/10.1007/978-3-319-23802-9_11>

Used for the named m4 device and the USB / secondary-SATA / primary-SATA recovery outcomes. The authors' causal interpretations are recorded but not automatically adopted as device-internal fact.

### P1 — Canonical M550 first-party product evidence

Crucial / Micron, **“Crucial M550 Solid State Drive”**, revision 29 January 2014:
<https://content.crucial.com/content/dam/crucial/ssd-products/m550/flyer/crucial-m550-ssd-product-flyer-en.pdf>

This remains the first-party product anchor that lists `Active Garbage Collection` and `TRIM support` separately.

### P2 — Maintained Crucial support contract

Crucial Support, **“SSD used to be faster but has slowed down”**, maintained/localized copies dated 15 November 2024, including:
<https://www.crucial.jp/support/articles-faq-ssd/ssd-used-to-be-faster-but-has-slowed-down>

Used in the existing power-state deepening for the current family-level powered-idle maintenance procedure. The 2013/2014 witnesses narrow chronology but do not replace the need for a period origin archive.

---

## 15. Remaining debt

1. Recover an authenticated Crucial-origin or web-archived **2010–2014** support page containing the AGC / powered-idle procedure. This slice narrows public circulation to August 2013 but does not close origin provenance.
2. Recover the exact historical Crucial webpage quoted in March 2014 and compare wording/revision chronology.
3. Determine the firmware revision used on Shah et al.'s Crucial m4 and obtain command-level traces showing whether ATA DATA SET MANAGEMENT/TRIM actually reached the device in each setup.
4. Add a controlled named-device experiment that separately manipulates deallocation delivery, powered idle, SATA low-power states, and time while observing internal-write or media-reclamation telemetry.
5. Find first-party controller/firmware documentation for a managed SSD exposing victim selection, live-page relocation, authority update, and crash-recovery ordering.
6. Keep broad Crucial/m4/M550 controller and TRIM transport history in `computing-archaeology` if that genealogy is pursued.
7. Keep quick format / stale-data recovery distinct from sanitize/remanence conformance unless a security-command test is explicitly performed.
