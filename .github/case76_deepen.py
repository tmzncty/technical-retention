from pathlib import Path


def read(path):
    return Path(path).read_text(encoding="utf-8")


def write(path, text):
    Path(path).write_text(text, encoding="utf-8")


# Case 76: standards chronology + qualification semantics.
p = "cases/76-jedec-ssd-endurance-retention-qualification.md"
text = read(p)
section = r'''### The September 2010 standards pair was not workload-complete for both classes

The original JESD218 and JESD219 were published as a pair in September 2010, but their coverage was not yet symmetrical. JESD218 Table 1 already defines both `Client` and `Enterprise` application classes and points the workload column to JESD219.[^jesd218] The September 2010 JESD219, however, contains only an `Enterprise endurance workload` section and explicitly says that the client workloads were still under development and would be added when available.[^jesd219-2010]

That creates a release-bounded historical distinction that the earlier Case 76 text did not make explicit:

> **application-class requirement specified ≠ complete companion workload available in the same publication moment**.

This does not mean that JESD218 lacked a client retention requirement. The one-year, 30 °C power-off condition and the client UBER/FFR requirements are already present in the September 2010 JESD218. It means more narrowly that the referenced workload standard did not yet supply a normative client workload alongside its enterprise workload in that original issue.

A contemporaneous August 2011 presentation by Alvin Cox, chairman of JEDEC JC-64.8, names `JESD218A`, describes both client and enterprise workload work under JESD219, and labels the client workload as based on a real trace including TRIM. The same presentation says one client-test detail — testing at 100% full — was still under discussion.[^cox2011] This is useful committee-chair evidence that the standards pair was evolving, but it is not silently substituted for a directly inspected normative JESD219 revision.

The bounded chronology therefore remains:

```text
September 2010 JESD218
    defines Client + Enterprise endurance/retention classes

September 2010 JESD219
    supplies Enterprise endurance workload
    + explicitly says Client workload is still under development

by August 2011
    JC-64.8 chair presents JESD218A
    + an evolving JESD219 Client workload
```

Direct facsimile archaeology of JESD218A and the later normative JESD219A client-workload text remains open. The purpose of this deepening is to prevent later revisions from being silently projected backward into September 2010.

### Retention qualification is controller-inclusive and statistically bounded

The original 2010 JESD218 also gives a stronger boundary than a simple `one year` or `three months` slogan.

First, clause 7.1.1 makes endurance/retention verification a **sample-based qualification exercise**: the sample must be large enough to establish the FFR and UBER requirements at 60% confidence.[^jesd218] This does not turn the standard into a deterministic countdown for every individual drive.

Second, Annex D treats useful retention as an SSD-level recoverability relation rather than a requirement for physically error-free NAND. It permits raw bit error rate (`RBER`) to grow with cycling and retention time, then requires the extrapolated RBER to remain below the SSD controller's ECC capability. It also warns that the ECC calculation assumes randomly distributed errors more perfectly than real devices provide, so a safety margin is required for device-to-device and location-to-location variation.[^jesd218]

This supports two engineering reconstructions:

> **raw-media bit errors ≠ host-visible data loss**

and

> **retention qualification ≠ zero raw errors in the NVM**.

ECC is part of the qualified recovery relation. This does not imply that ECC creates unlimited retention: the extrapolated raw-error population still has to remain inside a guarded correction envelope.

Third, the Table 1 temperatures are explicitly use-period temperatures for endurance/retention estimation, not datasheet absolute maxima/minima. Informative Annex C then shows that the expected retention duration changes when active-use or power-off temperature changes; its example maps the standard client condition (40 °C active, 30 °C power off) to 52 weeks, but a 25 °C power-off condition to at least 105 weeks under the stated model.[^jesd218]

So the historically defensible claim is not `client SSDs retain for one year` as a substrate constant. It is:

> **the September 2010 client qualification relation requires one year of power-off retention at its specified class conditions, under the standard's test/model/error criteria**.

The model-dependent Annex C extrapolation is not generalized here to every later NAND generation, charge-trap implementation, TLC/QLC device, controller ECC design, or storage environment.

'''
anchor = "### Verification may be accelerated without changing the target use condition\n"
if "### The September 2010 standards pair was not workload-complete for both classes" not in text:
    if anchor not in text:
        raise RuntimeError("Case 76 insertion anchor missing")
    text = text.replace(anchor, section + anchor, 1)
if "[^jesd219-2010]:" not in text:
    text = text.rstrip() + r'''

[^jesd219-2010]: JEDEC, **JESD219, _Solid-State Drive (SSD) Endurance Workloads_**, September 2010. Public text-preserving inspection copy: <https://studylib.net/doc/18339575/jesd219>. Cover/scope identify the September 2010 issue; printed p. 1 states that the client workloads were still under development and were to be added when available, while §3 is the enterprise endurance workload. This mirror is used for document inspection and cross-checked against contemporaneous September 2010 publication notices; it is not used for invention priority.
[^cox2011]: Alvin Cox (Seagate; Chairman, JEDEC JC-64.8), **_JEDEC SSD Endurance Workloads_**, Flash Memory Summit, 10 August 2011: <https://old.flashmemorysummit.com/English/Collaterals/Proceedings/2011/20110810_T1B_Cox.pdf>. Slides 3–7 identify JESD218A and the class requirements; slides 12–13 describe the client workload as based on a real trace including TRIM and note that testing at 100% full was still under discussion. This is contemporaneous committee-chair presentation evidence, not a substitute for a normative standards facsimile.
'''
write(p, text)

# Evidence 76: add exact inspected sources and boundaries.
p = "evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md"
text = read(p)
if "7. **JEDEC JESD219 (September 2010)**" not in text:
    needle = "6. **Belgal et al., IEEE IRPS 2002** — period technical evidence for program/erase-cycling-conditioned Flash retention physics.\n"
    replacement = needle + "7. **JEDEC JESD219 (September 2010)** — normative companion-workload primary text, inspected to bound the original enterprise-only workload coverage and the still-developing client workload;\n8. **Alvin Cox / JEDEC JC-64.8 presentation (August 2011)** — contemporaneous committee-chair evidence for the evolving JESD218A/JESD219 client-workload state, kept below normative standards text in authority.\n"
    if needle not in text:
        raise RuntimeError("Evidence source-hierarchy anchor missing")
    text = text.replace(needle, replacement, 1)

extra = r'''## Source 7 — JEDEC JESD219, September 2010

**Document:** JEDEC, _Solid-State Drive (SSD) Endurance Workloads_, JESD219, September 2010.

**Public text-preserving inspection copy:** <https://studylib.net/doc/18339575/jesd219>

**Contemporaneous publication cross-check:** JEDEC's September 2010 publication announcement was reproduced by period trade press as announcing JESD218 and JESD219 together; the historical direct JEDEC URL was `jedec.org/sites/default/files/docs/JESD219.pdf`.

### Exact locations inspected

- cover: `JESD219`, September 2010;
- printed p. 1, §1 Scope: workloads are for endurance rating/verification and are to be used with JESD218;
- printed p. 1, scope note: client workloads were still under development and were to be added when available;
- printed p. 1 onward, §3: the body supplies an `Enterprise endurance workload` with transfer-size, LBA-distribution, and randomized-data requirements.

### What this source adds

The September 2010 standards pair is historically **asymmetric**:

- JESD218 already defines client and enterprise class endurance/retention requirements;
- the same-month JESD219 supplies the enterprise workload but not yet the client workload it says is still under development.

This grounds `class requirement published ≠ every referenced companion workload simultaneously complete`.

### Evidence limit

The public inspection copy is a text-preserving third-party mirror of the JEDEC document rather than an official-host facsimile currently served by JEDEC. Its cover/scope/body are cross-checked against contemporaneous publication records, but this source is not used for figure-level claims, cryptographic provenance, or invention priority. Direct archival facsimile recovery remains desirable.

---

## Source 8 — Alvin Cox, JEDEC JC-64.8 / Flash Memory Summit, August 10, 2011

**Document:** Alvin Cox, _JEDEC SSD Endurance Workloads_, Flash Memory Summit 2011. Cox is identified on the presentation as Seagate and Chairman, JC-64.8.

**Inspected PDF:** <https://old.flashmemorysummit.com/English/Collaterals/Proceedings/2011/20110810_T1B_Cox.pdf>

### Exact locations inspected

- slide 3: names `JESD218A` and JESD219 as the active JEDEC SSD standards pair;
- slides 4–7: repeats TBW as a user-interface/application-class rating tied to capacity, UBER, FFR, and power-off retention;
- slide 12: describes a client workload based on a real trace, including TRIM commands, and separately describes the enterprise workload;
- slide 13: labels the client workload `JESD219`, describes preconditioning and trace replay, and says testing at 100% full was still under discussion.

### What this source adds

By August 2011 the committee chair was publicly presenting JESD218A and a client-workload design associated with JESD219. This is a useful dated bridge between the September 2010 enterprise-only JESD219 and later revised workload standards.

### Evidence limit

A conference presentation by the standards subcommittee chair is **contemporary committee evidence**, not the normative text of JESD218A or JESD219A. The phrase `still under discussion` is especially important: it blocks silently treating every slide detail as a finalized standard requirement.

---

## Qualification-semantics deepening from the original JESD218 facsimile

Additional directly inspected locations in the September 2010 JESD218 facsimile sharpen the existing case:

- printed p. 7, §6.3: Table 1 temperatures are use-period case temperatures for endurance/retention estimation, not absolute datasheet max/min values;
- printed p. 8, §7: direct and extrapolation methods both perform endurance verification followed by retention verification;
- printed p. 8, §7.1.1: the qualification sample is sized to establish FFR and UBER requirements at **60% confidence**;
- printed p. 24, Annex C: the same qualified SSD can have a different expected retention duration under different active-use/power-off temperatures; the client example gives 52 weeks at 40 °C active / 30 °C off and at least 105 weeks at 40 °C active / 25 °C off under the stated model;
- printed p. 25, Annex D: retention-time/p-e-cycle RBER extrapolation must remain below the SSD controller's ECC capability; the standard warns that random-error assumptions are imperfect and requires margin for device/location variation.

These passages support the bounded reconstruction:

```text
raw NVM error population
    !=
controller-correctable population
    !=
host-visible data error
    !=
class-level UBER/FFR qualification result
```

They also make the test epistemology explicit: **qualification evidence is sampled, statistical, controller-inclusive, and conditioned on a declared use/model envelope**. None of those adjectives means the standard is weak; they specify what kind of claim it actually establishes.

---

'''
marker = "## Prior art boundary\n"
if "## Source 7 — JEDEC JESD219, September 2010" not in text:
    if marker not in text:
        raise RuntimeError("Evidence prior-art anchor missing")
    text = text.replace(marker, extra + marker, 1)

old_future = "A pre-2000 qualification genealogy, direct original A117/A117B facsimile archaeology, JESD219 history, and revision-by-revision JESD218A/B history belong in future standards-history work or `computing-archaeology`, not in this bounded case."
new_future = "A pre-2000 qualification genealogy and direct original A117/A117B facsimile archaeology remain open. The September-2010 JESD218/JESD219 coverage mismatch and an August-2011 committee bridge are now grounded here, while direct normative facsimiles of JESD218A/JESD219A, later JESD218 B/C revision history, and the full workload-standard genealogy remain future standards-history work best coordinated with `computing-archaeology`."
if old_future in text:
    text = text.replace(old_future, new_future, 1)

table_anchor = "| A117 device/cell qualification ≠ JESD218 SSD host-TBW qualification | E | A117E scope/definitions + JESD218 §§3.6/6.2 | strong interface-level reconstruction |\n"
new_rows = r'''| September 2010 JESD218 defines both client and enterprise classes while same-month JESD219 supplies only the enterprise workload | H/P | JESD218 §6.3 Table 1 + JESD219 §1/§3 | direct release-bounded standards comparison; JESD219 inspection copy is a public mirror |
| Client workload was explicitly still under development in the September 2010 JESD219 | H/P | JESD219 §1 note | direct document statement; does not erase JESD218's already-published client retention requirement |
| By August 2011 JC-64.8 chair Cox publicly presents JESD218A and a JESD219 client-workload design | H/P | Cox FMS 2011 slides 3, 12–13 | contemporary committee evidence; not normative facsimile |
| JESD218 qualification is sample/confidence based rather than a deterministic per-drive countdown | H/P/E | JESD218 §7.1.1 | direct 60% confidence requirement + bounded reconstruction |
| Retention qualification can allow raw bit errors that remain inside guarded controller-ECC capability | H/P/E | JESD218 Annex D | direct standard mechanism; does not imply unlimited retention |
| Table 1 retention duration is condition-specific rather than a universal shelf-life constant | H/P/E | JESD218 §6.3 + Annex C | direct standard/example + bounded interpretation |
'''
if "| September 2010 JESD218 defines both client and enterprise classes while same-month JESD219 supplies only the enterprise workload |" not in text:
    if table_anchor not in text:
        raise RuntimeError("Evidence claim-ledger anchor missing")
    text = text.replace(table_anchor, table_anchor + new_rows, 1)

reject_anchor = "- `A117 device-level cycling/retention qualification is the same contract as JESD218 SSD TBW.`\n"
reject_more = "- `The September 2010 JESD219 already contained a finalized client workload merely because JESD218 Table 1 referenced a client workload.`\n- `A JEDEC client one-year retention requirement means every individual client SSD has a deterministic one-year physical countdown.`\n- `Passing JESD218 retention requires zero raw NAND bit errors.`\n"
if "The September 2010 JESD219 already contained a finalized client workload" not in text:
    if reject_anchor not in text:
        raise RuntimeError("Evidence rejected-shortcut anchor missing")
    text = text.replace(reject_anchor, reject_anchor + reject_more, 1)
write(p, text)

# README navigation: enrich existing Case 76 map entry without adding a duplicate case.
p = "README.md"
lines = read(p).splitlines()
marker = "cases/76-jedec-ssd-endurance-retention-qualification.md"
changed = False
for i, line in enumerate(lines):
    if marker in line and "September-2010 JESD219 enterprise-only companion-workload gap" not in line:
        lines[i] = line.rstrip() + " The latest deepening also records the September-2010 JESD219 enterprise-only companion-workload gap, the evolving 2011 client-workload bridge, and JESD218 Annex C/D statistical/ECC qualification boundaries."
        changed = True
        break
if not changed and not any("September-2010 JESD219 enterprise-only companion-workload gap" in x for x in lines):
    raise RuntimeError("README Case 76 navigation line missing")
write(p, "\n".join(lines) + "\n")

# ROADMAP: record completed bounded deepening while leaving full standards genealogy open.
p = "ROADMAP.md"
text = read(p)
roadmap_item = "- [x] JESD218/JESD219 standards-completeness and qualification-semantics deepening — canonical [`cases/76-jedec-ssd-endurance-retention-qualification.md`](cases/76-jedec-ssd-endurance-retention-qualification.md), with [`evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md`](evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md), now distinguishes the September 2010 JESD218 client/enterprise class contract from the same-month JESD219 enterprise-only workload body, uses the explicit `client workloads ... under development` note plus an August 2011 JC-64.8 chair presentation as a bounded revision bridge, and deepens Annex C/D to separate class-conditioned retention, statistical qualification, raw-error growth, guarded controller-ECC recoverability, and host-visible data loss. Direct normative JESD218A/JESD219A facsimiles, later B/C revision history, post-rating fault tests, and TLC/QLC named-product validation remain open.\n"
if "JESD218/JESD219 standards-completeness and qualification-semantics deepening" not in text:
    anchor = "- [x] Ceph `deep scrub` historical prior-art deepening"
    pos = text.find(anchor)
    if pos < 0:
        raise RuntimeError("ROADMAP Phase-2 anchor missing")
    text = text[:pos] + roadmap_item + text[pos:]
write(p, text)

# CASE_INDEX: reconcile Case 76 next-work boundary and add findings.
p = "CASE_INDEX.md"
text = read(p)
old = "direct original A117/A117B facsimiles, exact JESD218/JESD219 revision history, post-rating fault testing, TLC/QLC named-product validation, and physical retention models remain separate work"
new = "direct original A117/A117B facsimiles remain open; the September-2010 JESD218/JESD219 coverage mismatch plus Annex C/D ECC/statistical qualification boundary are now grounded, while direct normative JESD218A/JESD219A facsimiles, later B/C revision history, post-rating fault testing, TLC/QLC named-product validation, and physical retention models remain separate work"
if old in text:
    text = text.replace(old, new, 1)
elif new not in text:
    raise RuntimeError("CASE_INDEX Case 76 row boundary missing")
findings = r'''

### Case 76 standards-completeness / qualification-semantics deepening findings

1345. **application-class requirement specified ≠ complete companion workload available in the same publication moment** — September 2010 JESD218 defines both client and enterprise endurance/retention classes, while the same-month JESD219 body supplies the enterprise workload and says the client workload is still under development.
1346. **standards published as a pair ≠ identical maturity across every referenced sub-contract** — JESD218 and JESD219 were announced together, yet their original workload coverage was release-asymmetric; standards chronology must be read revision by revision rather than flattened.
1347. **missing finalized client workload in JESD219 ≠ absence of client retention semantics in JESD218** — the one-year/30 °C power-off requirement plus client UBER/FFR already exist in JESD218 Table 1; the gap concerns the referenced workload definition, not the entire class contract.
1348. **committee-chair presentation ≠ normative standards text** — Cox's August 2011 JC-64.8 presentation is strong contemporary evidence for JESD218A and an evolving client workload, but its own `still under discussion` wording prevents treating every slide detail as finalized normative language.
1349. **workload definition is constitutive of an SSD TBW rating without becoming a substrate property** — the host-write endurance number depends on the workload presented to the controller and the resulting amplification/wear relation, so the same NAND technology does not imply one workload-independent TBW meaning.
1350. **raw bit error ≠ host-visible data error** — JESD218 Annex D explicitly compares extrapolated RBER with the SSD controller's ECC capability; correctable raw-media errors can exist while the SSD still satisfies the higher-level recovery relation.
1351. **retention qualification ≠ zero-error NAND** — the standard requires raw-error growth to remain inside a guarded correction envelope and class UBER/FFR limits, not that every physical bit remain unchanged for the entire interval.
1352. **sample/confidence qualification ≠ deterministic per-drive countdown** — the original JESD218 sizes samples to establish UBER/FFR at 60% confidence; this is population-level qualification evidence, not a timestamp predicting the exact failure moment of each unit.
1353. **class retention-use temperature/time ≠ datasheet absolute limits or universal shelf life** — JESD218 explicitly identifies Table 1 temperatures as use-period temperatures for estimation, and Annex C changes expected retention when active/off temperatures change.
1354. **informative retention extrapolation ≠ universal physical law across later Flash generations** — Annex C's JEP122/Arrhenius model and Annex D's error-distribution/ECC assumptions are bounded test models whose applicability must be re-established for later media and controllers rather than projected by analogy.
'''
if "### Case 76 standards-completeness / qualification-semantics deepening findings" not in text:
    if "1344. **persistent maintenance basis ≠ every derived maintenance state**" not in text:
        raise RuntimeError("CASE_INDEX final finding anchor missing")
    text = text.rstrip() + findings + "\n"
write(p, text)
