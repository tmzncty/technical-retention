# Case 112 deepening evidence — Rambus HBM3 controller RFM commercial-support boundary, 2021–2026

## Status

**`bounded deepening complete`** — this record closes one narrow Case-112 debt at the public product-contract level:

> A named commercial HBM3 controller-IP vendor publicly offered an HBM3-ready digital-controller subsystem before final HBM3 publication, later offered HBM3 controller IP for licensing, and its current HBM3E/HBM3 controller product contract explicitly lists **Refresh Management (RFM) support** alongside self-refresh, power-down, RAS support, and a hardware performance Activity Monitor.

This is evidence that RFM is not only a standards-level abstract responsibility. It is **not** evidence for the controller's hidden RAA implementation, commercial ARFM level-selection policy, customer deployment, victim-row selection, or a specific physical mitigation algorithm.

The record deliberately separates three dates/statuses:

```text
2021 HBM3-ready controller/subsystem announcement
    !=
2022 final public HBM3 standard publication
    !=
2023 HBM3 controller licensing announcement
    !=
2026 inspection of a current product page that explicitly lists RFM support
```

The current page is not silently back-dated to 2021 or 2023.

---

## Why this slice belongs in Case 112

The existing Case 112 standards evidence establishes a split-authority contract:

```text
DRAM publishes RFM capability / thresholds
    +
controller retains activity-pressure bookkeeping and schedules RFM opportunity
    +
DRAM performs opaque internal management
```

That contract left a bounded implementation/adoption question open:

> Is there a named controller product whose public feature list actually says it supports HBM3 RFM?

Rambus provides such a witness. The public material is useful precisely because it is **less detailed** than the standard: it establishes a commercial controller boundary without exposing the internal bookkeeping needed to claim an exact implementation.

Broader HBM-controller history, Rambus/Northwest Logic product genealogy, PHY architecture, and AI-accelerator adoption remain outside this slice and belong primarily in `tmzncty/computing-archaeology` if pursued.

---

## Source 1 — Rambus HBM3-ready subsystem announcement, 16 August 2021

**Source:** Rambus Inc., **“Rambus Advances AI/ML Performance with 8.4 Gbps HBM3-Ready Memory Subsystem,”** 16 August 2021.  
**Official investor-relations release:** <https://investor.rambus.com/press-releases/press-release-details/2021/Rambus-Advances-AIML-Performance-with-8.4-Gbps-HBM3-Ready-Memory-Subsystem/default.aspx>  
**Official corporate copy:** <https://www.rambus.com/rambus-advances-ai-ml-performance-with-hbm3-ready-memory-subsystem/>

### H/P — a pre-final-standard HBM3-ready controller/PHY subsystem was publicly offered

The release announces an **HBM3-ready memory interface subsystem** consisting of a fully integrated PHY and digital controller, supporting data rates up to 8.4 Gbps and more than one terabyte per second of aggregate bandwidth.

The release also says the subsystem:

- supports HBM3 RAS features;
- includes a built-in hardware-level performance activity monitor;
- is a controller + PHY subsystem rather than only a DRAM-stack product;
- builds on Rambus HBM2/HBM2E deployment experience.

This is a useful chronological floor for public **HBM3-ready controller engineering** before the January-2022 JESD238 publication used by Case 112.

It is not an RFM-specific floor.

### X — do not back-project the current RFM feature list into the 2021 announcement

The 2021 release does **not** explicitly say `Refresh Management`, `RFM`, `RAA`, `RAAIMT`, `RAAMMT`, or `ARFM`.

Therefore:

```text
2021 HBM3-ready controller + HBM3 RAS support
    !=
proved 2021 public RFM implementation claim
```

and:

```text
current Rambus page lists RFM
    !=
current wording may be silently attributed to the 2021 product announcement
```

This matters because the repository is specifically trying to avoid turning later interface vocabulary into earlier historical evidence.

---

## Source 2 — Rambus HBM3 controller licensing announcement, 25 October 2023

**Source:** Rambus Inc., **“Rambus Boosts AI Performance with 9.6 Gbps HBM3 Memory Controller IP,”** 25 October 2023.  
**Official investor-relations release:** <https://investor.rambus.com/press-releases/press-release-details/2023/Rambus-Boosts-AI-Performance-with-9.6-Gbps-HBM3-Memory-Controller-IP/default.aspx>  
**Official corporate copy:** <https://www.rambus.com/rambus-boosts-ai-performance-with-9-6-gbps-hbm3-memory-controller-ip/>

### H/P — the controller was a licensable product, not only a standards example

The dated release says Rambus HBM3 Memory Controller IP:

- supports data rates up to 9.6 Gbps;
- can provide more than 1.2 TB/s aggregate throughput;
- is intended for high-throughput, low-latency applications;
- is modular and highly configurable;
- can be integrated and validated with a customer's choice of third-party HBM3 PHY;
- was **available for licensing** on the announcement date.

This establishes a named commercial controller-IP product and a controller/PHY integration boundary.

It does **not** by itself establish the RFM feature because the release does not enumerate RFM.

### E — controller policy logic and physical interface can be separate product boundaries

The 2023 release describes controller IP that can be combined with a customer-selected HBM3 PHY.

For retention analysis, this is a useful architectural separation:

```text
controller command / scheduling logic
    !=
PHY electrical signaling implementation
    !=
HBM3 DRAM internal maintenance algorithm
```

This is an engineering reconstruction from the public subsystem boundary. It does not identify where every timing counter or RAA register is physically implemented in a particular integration.

---

## Source 3 — current Rambus HBM3E/HBM3 Controller IP product page, inspected 14 September 2026

**Source:** Rambus, **“HBM3E / HBM3 Controller IP.”**  
**Official product page:** <https://www.rambus.com/interface-ip/hbm/hbm3-controller/>  
**Inspection date:** 2026-09-14.

The page is a current product description. It does not expose a publication date for the exact feature-list revision inspected here.

### H/P — RFM support is explicitly a controller feature

The current feature list explicitly includes:

- `Supports HBM3E / HBM3 memory devices`;
- `Refresh Management (RFM) support`;
- self-refresh and power-down low-power modes;
- HBM3 RAS features;
- a built-in hardware-level performance Activity Monitor;
- DFI compatibility;
- end-to-end data parity;
- AXI or native user-logic interfaces.

The page also describes the controller as combinable with a customer-selected PHY to form a complete HBM3E memory subsystem.

This closes the bounded public-product question:

> **At least one named commercial HBM3 controller-IP product currently and explicitly advertises RFM support.**

It does not establish how that support is implemented internally.

### H/P — RFM and self-refresh are separately advertised features

The same product list separately names `Refresh Management (RFM)` and `Self-refresh and Power-down Low Power Modes`.

That is useful as a product-level semantic guardrail:

```text
RFM support
    !=
self-refresh support
    !=
power-down support
```

This matches, but does not independently prove, the standards-level Case-112 distinction between activity-conditioned RFM and ordinary/self-refresh retention regimes.

### X — the Activity Monitor is not proven to be the JEDEC RAA implementation

The product page calls the block a **performance Activity Monitor**. It does not say:

- that the monitor stores per-bank RAA values;
- that it implements the JESD238 suggested RAA algorithm;
- that it drives RFM scheduling;
- that its counters use `RAAIMT`, `RAAMMT`, or `RAADEC` semantics;
- that its output is retained across reset, self-refresh, or power transitions.

Therefore:

```text
performance Activity Monitor present
    !=
proved RAA bookkeeping implementation
```

and:

```text
RFM support + Activity Monitor on one feature list
    !=
proved causal connection between those two advertised features
```

This negative result is central to the slice. A tempting architecture inference remains unsupported unless controller documentation or traces expose the connection.

### X — `RFM support` is not an internal-algorithm disclosure

The product page does not identify:

- victim-row selection;
- hidden in-DRAM counters;
- physical row adjacency;
- whether a device uses targeted refresh, remapping, repair, throttling, or another mitigation internally;
- how controller-side postponement is scheduled;
- whether all optional ARFM levels are supported by a particular customer configuration.

Thus:

> **controller feature support != disclosure of the DRAM's mitigation mechanism**.

---

## Historical chronology — what can and cannot be dated

The three Rambus records support a deliberately asymmetric chronology:

```text
2021-08-16
    public HBM3-ready digital-controller + PHY subsystem
    HBM3 RAS + performance activity monitor advertised
    RFM not explicitly named in the inspected release

2022-01
    JESD238 public HBM3 standard floor used by Case 112
    RFM / RAA / ARFM contract explicitly documented

2023-10-25
    HBM3 Memory Controller IP announced at 9.6 Gbps
    product available for licensing
    controller can pair with third-party HBM3 PHY
    RFM not enumerated in the inspected release

2026-09-14 inspection
    current Rambus HBM3E/HBM3 Controller IP feature list
    explicitly advertises Refresh Management (RFM) support
```

The evidence **does not** establish the first date on which Rambus publicly advertised RFM support.

That exact product-page revision / archival chronology remains open.

> **dated controller availability != dated first RFM-support publication**.

---

## Engineering reconstruction

### E — the standards-level split authority has a named commercial controller boundary

Case 112's JESD238 evidence gives the public protocol contract: activity-conditioned RFM requires controller-visible command/scheduling participation while internal DRAM work remains opaque.

The Rambus product page now supplies a named controller boundary that explicitly claims RFM support.

The strongest safe reconstruction is:

```text
HBM3 standard exposes RFM command/policy obligations
    +
named controller IP advertises RFM support
    +
controller integrates with an HBM3 PHY / memory subsystem
    ->
RFM responsibility is represented in a real controller product boundary
```

The weakest unsafe reconstruction would be:

```text
Rambus must implement the JEDEC suggested per-bank RAA algorithm exactly
```

That claim is **not** supported by the public evidence.

### E — support capability is not runtime policy state

A controller product can support a protocol feature without that feature being active in every attached device/configuration/workload.

```text
controller supports RFM
    !=
attached device requires RFM at default policy
    !=
ARFM supported
    !=
non-default ARFM level selected
    !=
RFM command currently due
```

This follows the same capability/default-policy/current-state decomposition already grounded in the Case-112 ARFM evidence.

### E — product modularity prevents a one-box ontology

The controller can be paired with customer-selected PHY IP, while the HBM DRAM stack remains a separate device.

Therefore the retention-maintenance relation spans product boundaries:

```text
SoC/controller policy state
    -> command scheduling
    -> PHY transport
    -> HBM command reception
    -> opaque in-DRAM management
```

This is a functional decomposition, not a claim about one Rambus customer's physical floorplan.

### E — bandwidth figures are not maintenance-completion evidence

Rambus advertises up to 9.6 Gbps/pin and >1.2 TB/s interface throughput. Those are foreground interface-performance figures.

They do not establish:

- RFM execution time in a particular device;
- maximum sustainable RFM rate;
- row-hammer safety margin;
- maintenance completion latency;
- performance overhead under a given activation pattern.

> **interface bandwidth != retention-maintenance throughput**.

---

## Functional comparisons

### Case 112 standards contract

The standards record says what an HBM3 controller/device relationship **must or may express at the interface**. The Rambus record says a named commercial controller product **advertises support** for that feature family.

```text
normative interface contract
    !=
commercial feature claim
    !=
measured implementation behavior
```

All three evidence layers are useful, but they answer different questions.

### Case 54 — DDR5 RFM

Case 54 also separates device-published requirements from controller-maintained activity state and opaque DRAM management.

The Rambus HBM3 controller witness strengthens only the broad functional point that controller products may explicitly own refresh-management support. It does not prove identical DDR5/HBM3 command geometry, accounting, or implementation.

### Cases 09 / 21 — self-refresh

The Rambus product page advertises self-refresh and RFM separately. Cases 09 and 21 already show that autonomous self-refresh and externally scheduled refresh commands differ in authority and service semantics.

The comparison supports:

```text
same DRAM subsystem can expose multiple maintenance regimes
    !=
those regimes are one mechanism
```

No genealogy is claimed.

---

## Philosophical interpretation boundary

The useful conceptual point is limited:

> A retained payload can depend on a maintenance relation distributed across separately supplied components whose public contracts expose only part of the work.

The controller, PHY, and DRAM stack need not each contain a complete description of the retention process. Persistence can therefore depend on a **relation among components and policies**, not only on a durable material state.

This does not make every interface relation “memory,” nor does it establish any historical actor's philosophical vocabulary.

---

## Explicit non-claims

This evidence does **not** establish that:

1. Rambus invented HBM3 RFM;
2. Rambus publicly supported RFM as early as August 2021;
3. the 2021 HBM3-ready activity monitor was an RAA counter;
4. the current Activity Monitor implements JEDEC per-bank RAA bookkeeping;
5. the Activity Monitor drives RFM scheduling;
6. Rambus uses the exact suggested JESD238 RAA algorithm internally;
7. all Rambus HBM3 customers enable RFM;
8. all HBM3 devices require RFM at the default level;
9. all HBM3 devices support ARFM;
10. a Rambus controller autonomously chooses ARFM Levels A/B/C from workload or temperature;
11. a particular GPU, accelerator, or SoC deployed this controller IP;
12. controller licensing proves silicon shipment volume;
13. integration/validation with a PHY proves RFM-specific fault-injection compliance;
14. RFM support reveals a victim-row algorithm;
15. RFM support proves PARA, targeted-row refresh, row remapping, or any other named mitigation;
16. an advertised performance Activity Monitor retains state across reset or power loss;
17. 9.6 Gbps interface bandwidth measures RFM service capacity;
18. HBM3E and HBM3 have identical RFM behavior merely because one current Rambus page supports both;
19. the current product page existed with identical wording in 2023;
20. 2023 is the first date Rambus implemented or advertised RFM support.

---

## Source-provenance notes

All three source groups are first-party Rambus material:

- a dated 2021 investor/corporate announcement;
- a dated 2023 investor/corporate announcement;
- the current official HBM3E/HBM3 Controller IP product page inspected in 2026.

The dated announcements are preferred for chronology. The undated/current product page is preferred only for the **current explicit feature claim**.

The current page is not used to manufacture a historical 2021/2023 RFM date.

---

## computing-archaeology reuse check

A fresh repository search for `HBM3 RFM Rambus` in `tmzncty/computing-archaeology` returned no dedicated topic to reuse.

That absence does not authorize a generic HBM-controller history here. If broader controller/PHY/vendor genealogy becomes important, it should be built in `computing-archaeology` and linked back to this bounded retention case.

---

## Claim ledger

| Claim | Type | Strength |
| --- | --- | --- |
| Rambus publicly announced an HBM3-ready controller+PHY subsystem on 2021-08-16 | H/P | strong |
| the 2021 release advertised HBM3 RAS and a hardware performance activity monitor | H/P | strong |
| the 2021 inspected release explicitly advertised RFM | X | rejected |
| Rambus announced licensable HBM3 Memory Controller IP on 2023-10-25 | H/P | strong |
| the 2023 controller could be paired with a customer-selected third-party HBM3 PHY | H/P | strong |
| current official Rambus HBM3E/HBM3 controller page explicitly lists RFM support | H/P | strong for current product contract |
| current page separately lists self-refresh/power-down and RFM | H/P | strong |
| current page separately lists a hardware-level performance Activity Monitor | H/P | strong |
| Activity Monitor is the JEDEC RAA implementation | X | rejected absent documentation |
| controller feature support proves hidden DRAM mitigation | X | rejected |
| controller/PHY/DRAM form separate retention-maintenance responsibility boundaries | E | strong as bounded architecture reconstruction |
| commercial feature support proves runtime RFM use in every configuration | X | rejected |
| current page proves first RFM-support publication date | X | rejected |

---

## Remaining evidence debt

This slice closes only the **named commercial controller public-support witness**.

Still open:

- archived product-page revisions or dated product briefs that establish the first Rambus public `RFM support` wording;
- controller documentation exposing whether/how per-bank RAA bookkeeping is implemented;
- commercial ARFM level-selection policy;
- named HBM3 DRAM parameter values paired with a controller configuration;
- independent command traces showing RFM scheduling and level transitions;
- customer/product deployment evidence;
- performance/energy measurements under RFM pressure;
- missed-RFM / threshold / fault-injection behavior;
- hidden in-DRAM victim selection or mitigation implementation.

## Sources

1. Rambus Inc., **“Rambus Advances AI/ML Performance with 8.4 Gbps HBM3-Ready Memory Subsystem,”** 16 August 2021: <https://investor.rambus.com/press-releases/press-release-details/2021/Rambus-Advances-AIML-Performance-with-8.4-Gbps-HBM3-Ready-Memory-Subsystem/default.aspx>.
2. Rambus Inc., **“Rambus Boosts AI Performance with 9.6 Gbps HBM3 Memory Controller IP,”** 25 October 2023: <https://investor.rambus.com/press-releases/press-release-details/2023/Rambus-Boosts-AI-Performance-with-9.6-Gbps-HBM3-Memory-Controller-IP/default.aspx>.
3. Rambus, **“HBM3E / HBM3 Controller IP,”** official current product page, inspected 14 September 2026: <https://www.rambus.com/interface-ip/hbm/hbm3-controller/>.
4. JEDEC HBM3 standards context remains grounded separately in [`112-jedec-hbm3-2022-2023-rfm-grounding.md`](112-jedec-hbm3-2022-2023-rfm-grounding.md) and [`112-jedec-hbm3-2022-2023-arfm-deepening.md`](112-jedec-hbm3-2022-2023-arfm-deepening.md).
