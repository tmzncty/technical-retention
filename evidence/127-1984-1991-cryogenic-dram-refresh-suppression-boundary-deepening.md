# Case 127 deepening — 1984–1991 cryogenic DRAM: refresh suppression is not power-off remanence

**Status:** `bounded deepening complete`

## Why this slice exists

Case 127 is grounded primarily in the 2008 cold-boot experiments of Halderman et al.: ordinary DRAM can retain a partially recoverable physical image for some time after platform power and refresh stop, and cooling can lengthen that residual window. The case also carries a cautious 1979 prior-art lead through Halderman et al.'s citation to W. Link and H. May, but the original 1979 article has not yet been directly facsimile-inspected.

This addendum asks a narrower historical and engineering question that can be answered with independent 1980s–1990s evidence:

> **What happens to the meaning of `refresh-dependent` when temperature is deliberately changed so that charge leakage becomes much smaller while the memory remains an operating semiconductor system?**

The answer matters because `refresh removed`, `power removed`, and `state no longer volatile` are not equivalent transitions.

The bounded record below uses:

1. a Hitachi low-temperature semiconductor patent with a **9 May 1984 priority date** and U.S. publication/issue on **1 December 1987**;
2. an IBM-authored **1989** low-temperature DRAM experiment;
3. an IBM-authored **1991** 4-Mbit DRAM fabricated specifically for cryogenic operation;
4. P. Wyns and R. L. Anderson's **1989** commercial-DRAM study only as a secondary bibliographic/abstract cross-check where the full paper was not directly inspected in this slice.

This is a **cryogenic-operation boundary** for Case 127, not a replacement for the still-open direct inspection of Link and May 1979.

---

## Claim-type discipline

### Historical record

Statements directly supported by the patent text or the institutional publication records are labeled **H/P**.

### Secondary historical cross-check

The indexed abstract for Wyns and Anderson 1989 is labeled **H/S** because this slice did not inspect the IEEE article facsimile directly.

### Engineering reconstruction

Relations such as `thermal support can substitute for frequent temporal refresh` are labeled **E**. They summarize the mechanism and are not period vocabulary.

### Functional analogy

Comparisons with ordinary DRAM refresh and cold-boot remanence are labeled **A**. They do not assert mechanism identity or genealogy.

### Philosophical interpretation

The final vocabulary note is labeled **I** and remains subordinate to the engineering evidence.

---

## 1. Historical record

### H/P — Hitachi treats low temperature as a way to suppress charge-loss maintenance while the circuit remains operational

U.S. Patent **US 4,710,648**, assigned to Hitachi, is titled **“Semiconductor including signal processor and transient detector for low temperature operation.”** The Google Patents family record gives a **9 May 1984** priority date; the U.S. patent issued on **1 December 1987**. The public patent text describes operation below about **200 K** as a way to reduce MOS junction leakage by many orders of magnitude.

The patent's background contrasts ordinary dynamic circuitry with static circuitry. In the ordinary dynamic case, stored node potential changes because of leakage, so cyclic timing/charge-supply activity is needed. The proposed low-temperature design instead relies on markedly reduced leakage so charge at a circuit node changes only negligibly over long intervals.

The patent then gives a RAM-specific embodiment. For a one-bit dynamic memory cell with a storage capacitor and dummy-cell sense arrangement, it states that below about 200 K the **charge-storage period becomes sufficiently long that a special refresh operation is unnecessary**.

The bounded historical claim is therefore:

```text
ordinary dynamic charge storage
    + ordinary-temperature leakage
    -> recurring refresh / charge restoration needed

low-temperature dynamic charge storage
    + much lower leakage
    -> refresh requirement can become extremely infrequent
       or unnecessary in the described operating regime
```

This is an industrial design disclosure, not proof that a named commercial DRAM product shipped with exactly this architecture.

**Primary source:** Hitachi, U.S. Patent 4,710,648, filed in the mid-1980s from a 1984-priority family, issued 1 December 1987, description of low-temperature MOS leakage and the RAM embodiment: <https://patents.justia.com/patent/4710648>.

### H/P — the Hitachi patent itself places the 1979 Link/May work inside an earlier low-temperature-memory literature

The same patent's background cites three earlier low-temperature semiconductor/memory records, including:

- F. H. Gaensslen et al., 1977, on small MOSFETs at low temperature;
- **W. Link and H. May, “Eigenschaften von MOS-Ein-Transistorspeicherzellen bei tiefen Temperaturen,” 1979**;
- T. Moro-oka et al., 1984, on dynamic RAM operation at low temperature.

This is historically useful because it supplies an **independent period-adjacent industrial witness** that Link/May belonged to a known low-temperature MOS-memory literature before the 2008 security framing.

It does **not** close the exact-content debt for the 1979 paper. The Hitachi patent is not a substitute for page-level inspection of Link and May, and its citation cannot be used to attribute exact numerical claims to that paper unless the original article is recovered.

Thus:

```text
period patent cites Link/May 1979
    -> independent evidence that the work circulated in the field

period patent citation
    != direct inspection of the 1979 experiment
```

### H/P — IBM 1989 reports strongly enhanced retention in a functioning low-temperature DRAM experiment

IBM Research's institutional record for **“Experimental low temperature DRAM”** identifies the Symposium on VLSI Circuits 1989 paper by W. H. Henkels and colleagues. The abstract reports a 512-Kbit CMOS DRAM operated at liquid-nitrogen temperature, with 12-ns access, measured soft-error behavior, and **greatly enhanced retention time with no evidence of early failures** in the reported experiment.

The point for Case 127 is not the speed result. It is that a conventional dynamic-memory mechanism can move into a dramatically different retention regime when temperature changes, while still functioning as an actively powered memory system.

**Primary/institutional source:** IBM Research, “Experimental low temperature DRAM,” Symposium on VLSI Circuits 1989: <https://research.ibm.com/publications/experimental-low-temperature-dram>. DOI cross-record: `10.1109/VLSIC.1989.1037471`.

### H/P — IBM 1991 reports an LT-optimized DRAM with cell retention exceeding eight hours at 85 K

IBM Research's institutional record for **“A 4-Mb Low-Temperature DRAM”** describes what it calls the first DRAM fabricated in a technology specifically optimized for cryogenic operation. The record reports that at **85 K**, storage retention time of the trench-capacitor memory cells **exceeded eight hours** and that the device had a wide operating margin/process window for data retention.

The corresponding IEEE Journal of Solid-State Circuits article is bibliographically identified as volume 26, issue 11, pp. 1519–1529 (1991), DOI `10.1109/4.98967`.

The safe claim is only that an intentionally cryogenic DRAM design demonstrated a very long cell-retention interval relative to ordinary refresh periods while functioning as a powered DRAM system.

It is not evidence that:

- the chip could preserve data for eight hours with all supply rails removed;
- the reported retention time was a shelf-retention guarantee;
- ordinary commodity DRAM at 85 K has the same interval;
- the 1991 design is a direct descendant of the 1979 experiment.

**Primary/institutional source:** IBM Research, “A 4-Mb Low-Temperature DRAM,” 1991: <https://research.ibm.com/publications/a-4-mb-low-temperature-dram>.

### H/S — commercial DRAM studies also reported multi-day refresh intervals at low temperature, but the full article still needs direct inspection

P. Wyns and R. L. Anderson's **“Low-Temperature Operation of Silicon Dynamic Random-Access Memories,”** *IEEE Transactions on Electron Devices* 36(8), 1989, DOI `10.1109/16.30954`, is indexed as testing commercial 16-, 64-, and 256-Kbit DRAMs from five manufacturers.

The available abstract/index record reports refresh intervals as long as **4.6 days at 183 K** and describes a change in the dominant leakage mechanism as temperature falls. Because this slice did not inspect the IEEE facsimile directly, those exact quantitative details remain **H/S**, not a page-level primary quotation.

This source is useful as corroboration that the low-temperature effect was not confined to one custom IBM chip or one patent proposal. It should not be used to generalize one refresh interval to all DRAM.

---

## 2. Engineering reconstruction

### E — `refresh removed` has at least two technically different meanings

Case 127's 2008 cold-boot regime begins when both ordinary power support and refresh stop. The low-temperature records above expose another possibility: refresh can become unnecessary or extremely infrequent **while the semiconductor system remains powered and intentionally operated in a cryogenic environment**.

These are different states:

```text
ordinary powered DRAM
    = electrical power
    + ordinary thermal environment
    + periodic refresh

cryogenic powered DRAM
    = electrical power
    + deliberately cold environment
    + much longer charge-retention interval
    + refresh possibly suppressed in the bounded design

cold-boot remanence
    = ordinary service power absent
    + refresh absent
    + residual charge decaying toward loss
```

Therefore:

> **refresh absent != power absent**

and:

> **refresh absent != nonvolatile storage contract**.

### E — maintenance can be reduced because the substrate's loss rate changed, not because the logical obligation disappeared

In ordinary DRAM, periodic refresh compensates for charge leakage fast enough to preserve the service guarantee. Cooling changes semiconductor leakage and therefore changes how quickly the physical distinction needs to be renewed.

The logical requirement — preserve a distinguishable cell state — remains. What changes is the frequency and sometimes the necessity of the explicit restoration operation in the bounded temperature regime.

A useful decomposition is:

```text
retention obligation
    != physical loss rate
    != maintenance cadence
```

The same payload obligation can be implemented with a different maintenance cadence when the substrate/environment changes.

### E — thermal infrastructure can substitute for temporal maintenance without being the same mechanism

The Hitachi and IBM records make temperature itself part of the operating envelope. In that sense, deliberate cooling can reduce the need for repeated refresh work.

But:

```text
cryogenic cooling
    != DRAM refresh command
```

Cooling changes the rate at which charge is lost. Refresh senses/restores cell state. They are different physical interventions that can partly substitute at the level of the higher retention objective.

This supports the bounded project term **maintenance substitution**:

> one infrastructure relation can reduce the frequency of another maintenance operation without becoming the same operation.

The term is an engineering reconstruction, not historical vocabulary from Hitachi or IBM.

### E — `long retention time` still has to be tied to the support conditions under which it was measured

The 1991 IBM result (>8 h at 85 K) is meaningful only together with the device, temperature, voltage, measurement method, and operating regime. It is not a free-standing statement that “DRAM retains for eight hours.”

So:

```text
retention interval
    + omitted operating conditions
    -> misleading portability
```

For Case 127 this is especially important because a powered cryogenic retention measurement and an unpowered cold-boot decay measurement can both contain the word `retention` while answering different questions.

### E — residual recoverability after support withdrawal is distinct from engineered low-loss operation

The 2008 cold-boot experiment asks what remains **after** the ordinary support regime is withdrawn. The 1980s–1990s cryogenic work asks how changing the operating environment can make an active dynamic memory retain charge much longer **within** a designed operating regime.

Thus:

```text
engineered long retention while support remains
    !=
residual recoverability after support is withdrawn
```

This distinction prevents the cryogenic literature from being back-projected into a claim that cold-boot remnants were specified, guaranteed, or intentionally exposed as a product feature.

---

## 3. Functional comparisons

### A — Case 03 ordinary DRAM refresh

Case 03 treats ordinary DRAM as deadline-driven retention: cells leak, the system refreshes them before the error boundary is reached, and the refresh cadence is part of the normal operating contract.

The cryogenic records add a parameterized boundary:

```text
same broad capacitor-storage family
    + lower leakage environment
    -> much longer safe interval between restoration events
```

This is not a claim that every historical DRAM implements one identical leakage model. It is a functional comparison showing that a maintenance deadline is conditional on substrate/device/environment parameters.

### A — Case 127 cold-boot decay

Case 127's original relation is:

```text
power/refresh withdrawn
    -> ordinary service guarantee ends
    -> physical state can remain temporarily recoverable
```

The cryogenic-operation relation is instead:

```text
power remains
    + cooling deliberately supplied
    -> leakage greatly reduced
    -> refresh burden can collapse
```

The two regimes meet at the same physical fact — stored charge does not disappear instantaneously — but diverge in support conditions and system contract.

### A — magnetic core and nonvolatile Flash

Magnetic core and Flash are designed so their retained physical state survives without DRAM-style periodic refresh under their specified regimes. Cryogenic DRAM can imitate one *functional* aspect of that behavior by stretching charge-retention time, but that does not make its storage mechanism historically or physically identical to core or Flash.

`refresh-free under one cryogenic operating condition` is therefore not a synonym for `nonvolatile technology`.

---

## 4. Prior-art chronology and anti-anachronism

The inspected chain can be stated conservatively as:

```text
1979
    Link / May low-temperature MOS one-transistor memory-cell paper
    (known through later citations; direct facsimile still open)

1984 priority / 1987 U.S. issue
    Hitachi low-temperature semiconductor patent
    explicitly cites Link/May
    and describes a RAM embodiment where special refresh is unnecessary below ~200 K

1989
    IBM experimental cryogenic DRAM reports greatly enhanced retention
    commercial-device study by Wyns / Anderson independently reports very long low-temperature refresh intervals

1991
    IBM LT-optimized 4-Mb DRAM reports >8 h cell retention at 85 K

2008
    Halderman et al. reframe residual DRAM charge after power loss as a security/recovery problem
```

This chronology **does not establish a genealogy** from Link/May to Hitachi to IBM to Halderman. It establishes public technical continuity of the broader fact that DRAM/MOS charge-retention behavior changes strongly with temperature.

The following claims remain rejected:

- `Halderman et al. discovered that DRAM retention depends on temperature`;
- `the 1979 paper has now been directly verified`;
- `Hitachi's patent proves a shipped no-refresh commercial DRAM`;
- `IBM's cryogenic DRAM is nonvolatile memory`;
- `>8 h at 85 K means >8 h after complete power removal`;
- `all low-temperature DRAMs stop needing refresh below one universal temperature`;
- `shared low-temperature behavior proves one design lineage`.

---

## 5. Failure and forgetting boundaries

The added records sharpen several failure modes that should remain separate.

### Leakage-dominated maintenance pressure

At ordinary temperatures, leakage can force frequent restoration if the system is to preserve the specified state reliably.

### Cryogenic reduction of leakage

Cooling can enlarge the retention interval dramatically. That changes the maintenance requirement but is not itself a proof of indefinite storage.

### Circuit-operability floor

Very low temperature can introduce other circuit limits. A memory can have excellent charge retention yet still fail to operate correctly because sense, timing, threshold, or other circuit behavior leaves the valid operating envelope.

Therefore:

> **excellent cell retention != complete memory-system operability**.

### Power-off residual decay

Once electrical support and refresh are removed, Case 127's original cold-boot boundary applies: state may persist transiently but gradually becomes corrupted.

### Environmental-support failure

For a deliberately cryogenic memory system, loss of cooling changes the retention regime even if power remains. Thus the supporting environment can itself be part of retention infrastructure.

---

## 6. Evidence-strength ledger

| Claim | Type | Strength / boundary |
| --- | --- | --- |
| Hitachi publicly described sub-200 K MOS operation with strongly reduced leakage and a RAM embodiment requiring no special refresh | H/P | strong patent-text evidence; design disclosure, not product-deployment proof |
| the Hitachi patent cites Link/May 1979 as earlier low-temperature MOS-memory literature | H/P | direct patent background citation |
| the 1979 article's exact one-week/no-refresh experiment has been directly inspected here | X | false; still open |
| IBM's 1989 experimental low-temperature DRAM reported greatly enhanced retention | H/P | institutional record of peer-reviewed conference paper |
| IBM's 1991 LT-optimized 4-Mb DRAM reported cell retention exceeding 8 h at 85 K | H/P | institutional record + journal bibliographic anchor |
| commercial DRAMs from multiple vendors showed multi-day low-temperature refresh intervals in Wyns/Anderson 1989 | H/S | abstract/index evidence only in this slice; direct facsimile still desirable |
| refresh suppression proves power-off remanence | X | different support boundary |
| refresh-free cryogenic operation makes DRAM a nonvolatile-storage technology | X | unsupported category collapse |
| cooling and refresh are physically the same maintenance operation | X | false; one changes loss rate, the other restores state |
| support conditions are part of the meaning of a retention interval | E | supported engineering reconstruction |

---

## 7. Related-repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated low-temperature DRAM / Link-May / cryogenic-memory module to reuse.

If a broader history is later built, that companion repository should own:

- cryogenic CMOS and DRAM device genealogy;
- the 1977 MOSFET low-temperature literature;
- the full Link/May 1979 article reconstruction;
- the 1984 Japanese DRAM paper cited by Hitachi;
- IBM's late-1980s/early-1990s low-temperature VLSI program;
- device/circuit reasons for low-temperature speed, leakage, threshold, and sense behavior.

Case 127 should retain only the **retention-specific boundary** among refresh cadence, power support, thermal support, residual recoverability, and the meaning of `volatile`.

---

## 8. Remaining open evidence debt

This slice deliberately **does not** claim to close the oldest primary-source seam.

Still open:

1. recover and directly inspect the **Link & May 1979** article, including exact device type, supply condition, temperature, refresh condition, test duration, error criterion, and whether the often-repeated “one week without refresh in liquid nitrogen” wording matches the original paper precisely;
2. inspect the **Moro-oka et al. 1984** Japanese conference record directly rather than only through the Hitachi patent's citation;
3. page-check the full **Wyns & Anderson 1989** IEEE article for the exact 4.6-day measurement conditions and leakage-mechanism discussion;
4. if needed, inspect the full IBM 1989/1991 papers to separate refresh-disabled tests, explicit retention-time tests, and ordinary powered operation at page level.

These are bounded source-recovery tasks, not reasons to weaken the already-supported distinction between cryogenic powered operation and power-off remanence.

---

## Sources

### Primary / first-party technical sources

1. **Hitachi, Ltd., U.S. Patent 4,710,648, “Semiconductor including signal processor and transient detector for low temperature operation.”** Priority family dated 9 May 1984; U.S. issue 1 December 1987. Public patent text and bibliographic record: <https://patents.justia.com/patent/4710648>.
   - background: dynamic leakage / recurring timing requirement;
   - low-temperature design: leakage reduced strongly below about 200 K;
   - RAM embodiment: charge-storage period sufficiently long that special refresh is unnecessary;
   - prior-art references include Link/May 1979 and Moro-oka et al. 1984.
2. **W. H. Henkels et al., “Experimental low temperature DRAM,” Symposium on VLSI Circuits 1989.** IBM Research publication record: <https://research.ibm.com/publications/experimental-low-temperature-dram>. DOI `10.1109/VLSIC.1989.1037471`.
3. **W. H. Henkels et al., “A 4-Mb Low-Temperature DRAM,” IEEE Journal of Solid-State Circuits 26(11), 1991, 1519–1529.** IBM Research publication record: <https://research.ibm.com/publications/a-4-mb-low-temperature-dram>. DOI `10.1109/4.98967`.

### Secondary / abstract-level cross-check

4. **P. Wyns and R. L. Anderson, “Low-Temperature Operation of Silicon Dynamic Random-Access Memories,” IEEE Transactions on Electron Devices 36(8), 1989, 1423–1428.** DOI `10.1109/16.30954`. The direct article facsimile was not inspected in this slice; quantitative details are therefore kept at H/S strength.

### Existing Case-127 anchor

5. **J. Alex Halderman et al., “Lest We Remember: Cold Boot Attacks on Encryption Keys,” USENIX Security 2008.** <https://www.usenix.org/legacy/event/sec08/tech/full_papers/halderman/halderman_html/>.
   - used to keep the power-off/remanence boundary distinct from the cryogenic powered-operation evidence above.
