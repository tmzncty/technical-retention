# Case 135 deepening evidence — JESD84-B50.1 / e.MMC 5.01 AUTO_EN chronology corroboration (2014–2015)

## Status

**`bounded corroboration complete`** for the question whether the generic `BKOPS_EN[163] bit[1] = AUTO_EN` control already belonged to **e.MMC 5.01 / JESD84-B50.1 (July 2014)** or instead belongs to the **e.MMC 5.1** interface change.

The strongest result of this slice is deliberately source-bounded:

> A directly inspected e.MMC 5.1 standard gives `BKOPS_EN[163] bit[1] = AUTO_EN`; a contemporaneous January-2015 Linux compatibility patch by a SanDisk engineer says e.MMC 5.1 changed `BKOPS_EN` to have two operational bits and that **previous eMMC revisions supported only bit 0**; JEDEC's February-2015 publication announcement lists **Background Operation Control** among features added in e.MMC 5.1. Together these strongly corroborate a **5.1 version boundary** for the generic `AUTO_EN` bit rather than a 5.01/B50.1 origin.

This is **not yet direct clause-level proof from the B50.1 body**. The full B50.1 standard text was not publicly retrievable in this research pass, so the remaining debt is now narrow: obtain the B50.1 body or an official redline and inspect `BKOPS_EN[163]` directly.

## Research question

The preceding Case-135 evidence established a direct endpoint contrast:

```text
JESD84-B50 / e.MMC 5.0 / September 2013
    BKOPS_EN bit[7:1] = Reserved
    BKOPS_EN bit[0]   = manual ENABLE

JESD84-B51 / e.MMC 5.1 / February 2015
    BKOPS_EN bit[7:2] = Reserved
    BKOPS_EN bit[1]   = AUTO_EN
    BKOPS_EN bit[0]   = MANUAL_EN
```

But B51 identifies itself as a revision of **JESD84-B50.1, July 2014**, leaving an intermediate-revision ambiguity:

> Did B50.1 already assign bit 1 to autonomous BKOPS, or did the field change with 5.1?

This slice does not pretend to replace direct B50.1 inspection. It asks how far the chronology can be narrowed using contemporaneous implementation evidence plus directly inspected 5.1 standard text and publication metadata.

## Source boundary

### 1. JESD84-B50.1 metadata — publication identity only

A standards catalog record identifies:

- **JEDEC JESD84-B50.1**;
- title: _Embedded Multi-media card (e•MMC), Electrical Standard (5.01)_;
- date: **1 July 2014**;
- publisher: JEDEC Solid State Technology Association.

Source:

- <https://www.topstds.com/standards/jedec-jesd84-b501>

This source is used only to corroborate edition identity/date. It is **not** used as a substitute for the unavailable B50.1 clauses.

### 2. JESD84-B51 — directly inspected standard text through a pagination-preserving mirror

JEDEC, **JESD84-B51, _Embedded Multi-Media Card (e•MMC) Electrical Standard (5.1)_**, February 2015.

Inspected mirror:

- <https://studylib.net/doc/27873175/emmc5.1%E5%AE%98%E6%96%B9%E6%A0%87%E5%87%86%E5%8D%8F%E8%AE%AE>

Relevant text:

- cover: B51 is a **Revision of JESD84-B50.1, July 2014**;
- §6.6.25: `AUTO_EN` authorizes device-started/stopped background operations during idle time;
- §7.4.61 / Table 139: `EXT_CSD_REV = 7` covers MMC v5.0 and v5.01, while `EXT_CSD_REV = 8` covers v5.1;
- §7.4.82 / Table 159: `BKOPS_EN[163] bit[1] = AUTO_EN`, `bit[0] = MANUAL_EN`.

The mirror is not treated as the standards publisher; claims are attributed to the JEDEC text it preserves.

### 3. January-2015 Linux compatibility patch — contemporaneous implementation evidence

Alexey Skidanov, `[PATCH v2] mmc: Resolve BKOPS compatability issue`, linux-mmc mailing list, **29 January 2015**:

- <https://www.mail-archive.com/linux-mmc%40vger.kernel.org/msg30419.html>

Merged Linux commit:

- `0501be6429e4eb02f417ad83eacd84b8c57b0283`, _mmc: Resolve BKOPS compatability issue_;
- archive record: <https://marc.info/?l=git-commits-head&m=142368227616039&w=4>.

The commit identifies Alexey Skidanov with a SanDisk address and states that in eMMC 5.1 `BKOPS_EN` changed to two operational bits:

```text
bit 0 -> MANUAL_EN
bit 1 -> AUTO_EN
```

and that **previous eMMC revisions supported only bit 0**.

The code change also stops treating the whole `BKOPS_EN` byte as the manual-enable boolean and instead masks it with `0x01` (`EXT_CSD_MANUAL_BKOPS_MASK`).

This is primary **host-software compatibility evidence**, not the normative JEDEC standard itself.

### 4. JEDEC publication announcement — revision-level corroboration

A 24 February 2015 reproduction of JEDEC's e.MMC 5.1 publication announcement lists **Background Operation Control** among features added to e.MMC version 5.1:

- <https://us.design-reuse.com/news/36653/jedec-e-mmc-standard-update-v5-1.html>

This supports the revision-level chronology. It does not, by itself, prove the exact `BKOPS_EN` bit layout.

### 5. Related-repository check

Fresh searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `BKOPS` and `eMMC` found no dedicated module to reuse. A broad eMMC revision genealogy still belongs there if developed; this record keeps only the retention-relevant control-state boundary.

## Historical record

### H/P — B50.1 / e.MMC 5.01 is the immediate published intermediate revision

B51's own cover identifies B50.1, July 2014, as the revision it supersedes. Independent catalog metadata identifies that edition as e.MMC 5.01.

Therefore the chronology must not jump directly from September-2013 B50 to February-2015 B51 while silently pretending no intermediate published edition existed.

### H/P — B51 groups 5.0 and 5.01 under EXT_CSD revision 1.7, then assigns 5.1 revision 1.8

B51 Table 139 defines:

```text
EXT_CSD_REV = 7 -> Revision 1.7 (for MMC v5.0, v5.01)
EXT_CSD_REV = 8 -> Revision 1.8 (for MMC v5.1)
```

This is direct standard evidence that the device-visible `EXT_CSD_REV` generation boundary moves at 5.1, while 5.0 and 5.01 share revision value 7.

It does **not** establish that every clause or every EXT_CSD field is textually identical between B50 and B50.1.

### H/P — B51 directly assigns AUTO_EN to BKOPS_EN bit 1

B51 §7.4.82 / Table 159 defines:

```text
BKOPS_EN[163]
    bit[7:2] = Reserved
    bit[1]   = AUTO_EN
    bit[0]   = MANUAL_EN
```

B51 §6.6.25 says that when the host sets `AUTO_EN`, the device may start or stop background operations during idle time without notifying the host; the host should keep the device powered while the permission is active.

This remains the direct normative endpoint for the autonomous-idle-time scheduling permission used in Case 135.

### H/P* — the January-2015 Linux patch says the two-bit interpretation is an e.MMC-5.1 change

The Linux compatibility patch predates the 24-February-2015 public announcement by several weeks and describes the problem in versioned interface terms:

```text
eMMC 5.1:
    bit0 = MANUAL_EN
    bit1 = AUTO_EN

previous eMMC revisions:
    only bit0 supported
```

Because B50.1 / 5.01 is the immediately preceding published revision, this is strong contemporaneous implementation evidence **against** reading `AUTO_EN` as an already-established 5.01 generic BKOPS field.

However:

> **contemporaneous implementation statement != direct inspection of the B50.1 normative clause**.

The evidence is therefore marked `H/P*`, not upgraded to clause-level proof.

### H/P* — the compatibility fix exposes a real semantic hazard at the same byte offset

Before the fix, Linux stored the full `EXT_CSD_BKOPS_EN` byte in a boolean-like `bkops_en` member and used nonzero as evidence that manual BKOPS was enabled. Once bit 1 acquires an independent `AUTO_EN` meaning, that interpretation can become wrong: a byte with only bit 1 set is nonzero without implying manual BKOPS permission.

The merged fix masks the byte with `0x01` and renames the state to `man_bkops_en`.

This is implementation evidence that the field evolution mattered to host software, not merely editorial wording.

### H/P* — JEDEC's release announcement independently places Background Operation Control among 5.1 additions

The 24-February-2015 announcement lists `Background Operation Control` among features added in e.MMC 5.1.

Used together with the direct B51 bit definition and the January Linux compatibility patch, this reinforces the version boundary without being used as a substitute for the missing B50.1 body.

## Engineering reconstruction

### E — same byte address does not guarantee stable field semantics

`BKOPS_EN` remains at EXT_CSD byte 163 while its meaningful bit decomposition changes across the directly observed endpoint and the strongly corroborated version boundary.

Therefore:

```text
same register byte address
    != same bit-field semantics
```

A host that retains only a raw nonzero byte without retaining the applicable interpretation rule can conflate autonomous permission with manual permission.

### E — version context is part of correct interpretation, not user payload

For host software, the operational meaning of byte 163 depends on the applicable eMMC interface revision.

That gives a bounded retention relation:

```text
retained raw control byte
    + wrong / missing version semantics
    -> potentially wrong control-state interpretation
```

The standard revision is **interpretive context for the control register**, not part of the user's stored payload and not evidence that user data changed.

### E — a new permission bit is not evidence of a new hidden maintenance algorithm

The addition of `AUTO_EN` changes the standardized host/device authority relation:

```text
manual service-window permission
    vs
standing autonomous idle-time permission
```

It does not disclose the device's internal page-selection, garbage-collection, wear-leveling, read-reclaim, refresh, or block-retirement algorithms.

Thus:

> **control-interface evolution != demonstrated media-maintenance-algorithm evolution**.

### E — compatibility evidence narrows chronology without replacing the standard

A source hierarchy can preserve both facts:

1. the Linux patch is exceptionally useful because it is contemporaneous, implementation-facing, version-specific evidence;
2. only the missing B50.1 normative text or an official redline can close the clause-level documentary gap.

Therefore:

```text
strongly corroborated version boundary
    != direct standards-text proof
```

and also:

```text
missing direct B50.1 body
    != chronology completely unconstrained
```

### E — shared EXT_CSD revision number does not mean complete textual identity

B51 maps both v5.0 and v5.01 to `EXT_CSD_REV = 7`. That is useful version metadata, but it must not be expanded into:

```text
v5.0 text == v5.01 text in every clause
```

B50.1 can contain corrections, clarifications, or other changes while still sharing the same EXT_CSD revision value.

## Functional analogy only

### Case 104 — command/encoding interpretation changes

Case 104's 2002 Mobile SDRAM evidence shows that an electrical command encoding can acquire a different function in another device/specification context. Case 135 supplies a narrower register-field analogue: the same EXT_CSD byte address can require a different bit interpretation after interface evolution.

The bounded similarity is:

```text
stable encoding location
    != stable operation meaning
```

This is a functional comparison only. It does not establish any historical or engineering genealogy between Mobile SDRAM Deep Power-Down and e.MMC BKOPS.

## Philosophical interpretation — bounded

A narrow project-level interpretation survives the technical evidence:

> A retained technical state is usable only through an interpretation regime capable of distinguishing which parts of the representation currently mean what.

Here the point is modest and engineering-led. `0x02` at EXT_CSD byte 163 cannot be interpreted safely as “manual BKOPS enabled” merely because the byte is nonzero once the 5.1 field model exists.

This does **not** turn specification revisioning into human memory theory, nor does it make the standard version part of the user payload.

## Prior-art / chronology result

The safest chronology after this slice is:

```text
JESD84-B50 / e.MMC 5.0 / September 2013
    direct standard inspection:
        BKOPS_EN bit[7:1] Reserved
        bit0 manual ENABLE

JESD84-B50.1 / e.MMC 5.01 / July 2014
    edition existence/date established
    direct BKOPS_EN clause still not inspected here
    B51 later classifies 5.0 + 5.01 under EXT_CSD revision 1.7

29 January 2015 Linux compatibility patch
    contemporaneous implementation statement:
        eMMC 5.1 changes BKOPS_EN to MANUAL_EN + AUTO_EN
        previous eMMC revisions supported only bit0

JESD84-B51 / e.MMC 5.1 / February 2015
    direct standard inspection:
        EXT_CSD revision 1.8
        BKOPS_EN bit1 = AUTO_EN
        bit0 = MANUAL_EN

24 February 2015 JEDEC publication announcement
    Background Operation Control listed among 5.1 additions
```

The practical conclusion is stronger than the previous open interval but remains source-qualified:

> **The available evidence strongly corroborates `AUTO_EN` as a 5.1 generic-BKOPS interface change rather than a B50.1/5.01 feature; direct B50.1 clause inspection remains the final documentary check.**

## Explicit non-claims

This evidence does **not** establish that:

1. the B50.1 `BKOPS_EN[163]` clause has been directly inspected;
2. B50.1 is textually identical to B50 merely because both map to EXT_CSD revision 1.7;
3. the Linux patch is a normative JEDEC document;
4. the JEDEC announcement alone proves the exact bit layout of `BKOPS_EN`;
5. `AUTO_EN` created autonomous internal Flash maintenance as a physical capability;
6. pre-5.1 devices could never perform any internal work autonomously;
7. B50's Sleep-notification autonomous capability is identical to B51 `AUTO_EN`;
8. all vendors implement the same hidden operations behind generic BKOPS;
9. `AUTO_EN=1` means maintenance is currently due or currently executing;
10. `AUTO_EN=0` means no maintenance debt exists;
11. `EXT_CSD_REV=7` proves every 5.0 and 5.01 control field is identical;
12. a nonzero `BKOPS_EN` byte can be interpreted without applying the field layout of the relevant revision;
13. the 2015 Linux fix proves any particular vendor product shipped `AUTO_EN` before the final standard publication;
14. Background Operation Control is Micron automotive self refresh;
15. this interface history establishes invention priority for autonomous managed-Flash maintenance.

## Resulting bounded relations

```text
same byte offset != same field semantics
raw control byte != interpreted control state
version context != user payload
standardized permission != maintenance debt
permission != execution
execution != hidden-algorithm identity
strong chronology corroboration != direct B50.1 clause proof
shared EXT_CSD revision value != complete textual identity
```

## Navigation / relation to existing Case-135 evidence

Read this record together with:

- [`135-jesd84-b50-b51-2013-2015-autonomous-bkops-interface-deepening.md`](135-jesd84-b50-b51-2013-2015-autonomous-bkops-interface-deepening.md) — direct B50-vs-B51 field-level endpoint;
- [`135-jedec-emmc51-bkops-maintenance-opportunity-deepening.md`](135-jedec-emmc51-bkops-maintenance-opportunity-deepening.md) — BKOPS maintenance-opportunity semantics versus vendor self refresh;
- [`../cases/135-micron-emmc-self-refresh-time-trigger-maintenance.md`](../cases/135-micron-emmc-self-refresh-time-trigger-maintenance.md) — canonical Case 135.

This slice changes **chronology confidence**, not Case-135 maturity. The canonical case remains **`grounded`**.

## Remaining evidence debt

1. Obtain the full **JESD84-B50.1** body or an official B50.1→B51 redline and inspect `BKOPS_EN[163]` plus the Background Operations section directly.
2. If a redline is found, identify whether the `AUTO_EN` addition was introduced exactly in B51 final text or already in a pre-publication B51 draft; keep draft chronology separate from published-standard chronology.
3. Keep broader eMMC command/revision genealogy in `computing-archaeology` if it grows beyond this retention-specific control-state question.
4. Do not reopen generic manual-BKOPS origin here unless new 4.4/4.41 primary evidence materially changes the already bounded lower floor.