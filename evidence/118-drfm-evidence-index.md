# Case 118 — DDR5 Directed Refresh Management Evidence Navigation

**Canonical case:** [`../cases/118-micron-ddr5-directed-refresh-management.md`](../cases/118-micron-ddr5-directed-refresh-management.md)

**Current maturity:** `grounded` in the canonical case / current roadmap context. **No maturity promotion is made by this navigation file.**

This is a focused Case-118 navigation index. Its purpose is to separate the already-grounded physical-neighbor DRFM contract from the newly deepened **mode-register policy lifetime across reset**.

---

## Evidence map

| Slice | Evidence | What it establishes | Boundary |
| --- | --- | --- | --- |
| **2012–2024 DRFM grounding / prior-art floor** | [`118-micron-2012-2024-ddr5-drfm-grounding.md`](118-micron-2012-2024-ddr5-drfm-grounding.md) | named Micron DDR5 product contract for sampled-address-directed refresh of physically adjacent rows, BRC2/3/4 behavior, product-specific `tDRFM`, and earlier Intel address-directed targeted-refresh prior art | sampled address != physical neighbor; bounded scope != uniform per-command refresh; product contract != invention genealogy |
| **2022–2024 MR59 reset-policy lifetime** | [`118-micron-2022-2024-drfm-mode-register-reset-policy-deepening.md`](118-micron-2022-2024-drfm-mode-register-reset-policy-deepening.md) | MR59 separates implementation status from host enable, defines BRC as host-visible policy with a default, and reset/initialization requires nondefault MR policy to be re-established | silicon capability != current policy != platform intent; reset complete != nondefault maintenance policy restored |

---

## Retention decomposition now supported

Case 118 should no longer be compressed into only:

```text
sampled row
    -> refresh nearby physical rows
```

The evidence now supports a larger but still bounded chain:

```text
DRFM capability implemented by die
    !=
DRFM host-enable state
    !=
selected BRC policy
    !=
controller/platform desired policy
    !=
post-reset reconstruction of that policy
```

The spatial side remains:

```text
sampled address
    -> device-specific physical-neighbor resolution
    -> bounded neighbor coverage selected by BRC
    -> product-specific refresh ratio / service time
```

The lifetime side now adds:

```text
nondefault MR59 policy active before reset
    -> RESET_n / initialization regime
    -> required MRW reconstruction
    -> intended maintenance policy active again
```

The important negative statement is:

```text
DRFM still supported by the silicon
    !=
previous nondefault DRFM policy may be assumed still active
```

---

## Historical / engineering / analogy / interpretation boundary

### Historical record

Use the manufacturer and standards records only for what they directly expose:

- Micron 2022 core data sheet: MR59 status/enable/BRC fields and defaults; reset initialization wording.
- JEDEC JESD79-5 public text copy: DDR5 reset/default/configuration framework, with mirror custody noted.
- Micron 2024 16Gb product addendum: named-product DRFM support, default host-write view, BRC support, physical-neighbor contract, and product-specific maintenance duration.
- Intel 2012-priority / 2014-public patent in the grounding: earlier address-directed targeted-refresh functional prior art.

Do not turn filing priority into public-documentation date, standards wording into a named-product fault trace, or a product manual into an invention-priority claim.

### Engineering reconstruction

Repository-level terms such as:

- `maintenance-policy state`;
- `policy-restoration obligation`;
- `reset-time reconstruction debt`;
- `maintenance closure`;

are modern engineering descriptions of the documented interface relations. They are not claimed as Micron or JEDEC actor terminology.

### Functional comparison

Controlled comparisons are useful with:

- **Case 38** — maintenance capability versus current/saved SCT feature policy;
- **Case 21** — DRAM maintenance-mode handoff obligation;
- **Case 03** — maintenance-control state itself can have a lifetime requirement;
- **Case 54** — broader DDR5 RFM/RAA split authority.

These comparisons are functional only. They do not establish shared circuits, persistence mechanisms, or genealogy.

### Philosophical interpretation

Case 118 now supports a bounded project-level interpretation:

```text
mechanism continuity
    !=
policy continuity
```

and:

```text
retaining past payload
    !=
retaining / reconstructing what maintenance must happen next
```

Those are project interpretations, not period historical vocabulary.

---

## Related-repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for a dedicated `DRFM` / `MR59` / `BRC` packet did not locate a narrower artifact to reuse in this round.

Accordingly:

- broad DRAM / memory technology history should continue to route to `computing-archaeology` when a relevant packet exists;
- `technical-retention` keeps the narrow focus on maintenance-state lifetime, reset/configuration seams, evidence strength, and cross-case retention comparison.

Do not create a duplicate DDR5/RowHammer general history here merely to enlarge Case 118.

---

## Maturity / status

Case 118 remains **`grounded`**.

The reset-policy slice materially improves:

- manufacturer-level evidence that DRFM capability and host enable are distinct;
- manufacturer-level evidence that BRC selection is current mode-register policy with a default;
- standards/manufacturer evidence for re-establishing required nondefault MR state after reset initialization;
- the distinction between maintenance mechanism, maintenance policy, and the state that reconstructs policy.

It does **not** justify promotion because substantial evidence debt remains.

---

## Remaining bounded debt

High-value follow-ons include:

- controller or firmware source/trace showing real MR59 programming and post-reset restoration;
- logic-analyzer or simulator observation of MR59 before and after RESET_n;
- full standards-version genealogy for DRFM, ARFM, RFM, and later PRAC-related mechanisms;
- cross-vendor named-product comparison;
- PPR/remapping interaction with physical-neighbor selection;
- fault injection / RowHammer experiments under deliberately altered BRC or DRFM-enable policy;
- independent observation of the product's outer-row refresh ratio behavior;
- exact boundary between host-visible policy restoration and any device-internal retained state not exposed by the public register contract.

These remain separate slices rather than reasons to overstate the current record.
