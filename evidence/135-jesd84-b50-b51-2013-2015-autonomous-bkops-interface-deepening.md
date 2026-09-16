# Case 135 deepening evidence — e.MMC 5.0→5.1 autonomous-BKOPS interface boundary (2013–2015)

## Status

**`bounded deepening complete`** for a direct endpoint comparison between the inspected September-2013 e.MMC 5.0 text (`JESD84-B50`) and the inspected February-2015 e.MMC 5.1 text (`JESD84-B51`).

The bounded result is deliberately narrower than a first-introduction claim:

> e.MMC 5.0 already standardizes mandatory Background Operations and separately acknowledges devices capable of autonomously initiating background operations in the Sleep-notification path, while its generic `BKOPS_EN[163]` interface is still manual-only (`bit[0] ENABLE`, `bit[7:1] Reserved`). e.MMC 5.1 explicitly splits manual and autonomous initiation and assigns `BKOPS_EN[163] bit[1]` to `AUTO_EN`.

This closes the **directly inspected 5.0-vs-5.1 interface endpoint**. It does **not** establish the exact revision in which `AUTO_EN` first entered the standard, because JESD84-B51 identifies itself as a revision of **JESD84-B50.1 (July 2014)** and B50.1 has not been directly clause-inspected in this slice.

## Research question

Case 135 already has three separate evidence layers:

1. e.MMC 4.41 / 2010 period material establishing a conservative public floor for generic **manual** BKOPS;
2. e.MMC 5.0 / 2013 `SET_TIME` and `PERIODIC_WAKEUP` evidence showing that host-supplied time and host-granted maintenance opportunities can be standardized without exposing the hidden maintenance algorithm;
3. e.MMC 5.1 / 2015 evidence showing `MANUAL_EN`, `AUTO_EN`, urgency reporting, and generic background-maintenance control.

The remaining seam was easy to overstate:

> Did e.MMC 5.0 already expose the same host-visible autonomous-BKOPS control that is explicit in e.MMC 5.1, or did 5.0 merely contain other forms of device-autonomous background behavior?

The distinction matters because these propositions are not equivalent:

```text
device can perform some internal work autonomously
    !=
standard exposes a generic host permission bit for autonomous idle-time BKOPS
    !=
host has opened that autonomous scheduling regime
    !=
background work is currently due
    !=
background work is currently executing
```

## Source boundary

### Primary standards text — e.MMC 5.0

JEDEC Solid State Technology Association, **JESD84-B50, _Embedded Multi-Media Card (e•MMC) Electrical Standard (5.0)_**, September 2013.

The inspected text-preserving copy retains JEDEC pagination and section numbering:

- cover / date and revision statement: <https://pdfcoffee.com/jesd84-b50-pdf-free.html>;
- §6.6.28 `Background Operations`, JEDEC p. 85;
- §6.6.38 / power-off and Sleep-notification path, JEDEC p. 105;
- §7.4.75 `BKOPS_START[164]` and §7.4.76 `BKOPS_EN[163]`, JEDEC p. 192.

The mirror is not treated as the standards publisher. Claims are attributed to the JEDEC text it preserves.

### Primary standards text — e.MMC 5.1

JEDEC Solid State Technology Association, **JESD84-B51, _Embedded Multi-Media Card (e•MMC) Electrical Standard (5.1)_**, February 2015.

The inspected text-preserving copy retains JEDEC pagination and section numbering:

- cover states `Revision of JESD84-B50.1, July 2014`: <https://studylib.net/doc/27873175/emmc5.1%E5%AE%98%E6%96%B9%E6%A0%87%E5%87%86%E5%8D%8F%E8%AE%AE>;
- §6.6.25 `Background Operations`, JEDEC pp. 93–94;
- §7.4.81 `BKOPS_START[164]` and §7.4.82 `BKOPS_EN[163]`, JEDEC pp. 214–215.

### Publication-change corroboration

A 24-February-2015 report reproducing JEDEC's e.MMC 5.1 publication announcement lists **Background Operation Control** among features added in v5.1:

- CDRInfo, `JEDEC Releases e.MMC Standard Update v5.1`: <https://cdrinfo.com/d7/content/jedec-releases-emmc-standard-update-v51>.

This announcement is supporting chronology evidence only. The exact interface claims below are anchored to the standards text itself.

### Intermediate revision metadata only

JESD84-B51's own cover says it revises **JESD84-B50.1, July 2014**. A commercial standards record independently identifies JESD84-B50.1 as e.MMC 5.01, dated July 2014:

- <https://www.topstds.com/standards/jedec-jesd84-b501>.

The B50.1 body was **not directly inspected** in this slice. It therefore acts as a chronology caution, not as evidence for or against `AUTO_EN` semantics.

## Historical record

### H/P — e.MMC 5.0 already has mandatory generic Background Operations

JESD84-B50 §6.6.28 says devices have internal maintenance operations that are better performed while the host is not being serviced. It separates foreground host-servicing operations from background operations and makes Background Operations support mandatory for e.MMC 5.0 devices.

This blocks a common chronology error:

> **e.MMC 5.1 Background Operation Control != first existence of standardized e.MMC Background Operations.**

The earlier Case-135 e.MMC-4.41 slice already moves the generic manual-BKOPS floor still earlier; the 5.0 endpoint matters here because it exposes the exact pre-5.1 control shape.

### H/P — the generic e.MMC 5.0 BKOPS path is manual

In B50 §6.6.28:

- the host writes any value to `BKOPS_START[164]` to **manually start** background operations;
- the device remains busy until no more background processing is needed;
- the host sets bit 0 of `BKOPS_EN[163]` to indicate that it expects to write `BKOPS_START` periodically;
- the device may defer some maintenance until those host-opened windows;
- `BKOPS_STATUS[246]` reports four urgency levels.

The register definition is even more explicit. B50 §7.4.76 gives:

```text
BKOPS_EN[163]
    bit[7:1] = Reserved
    bit[0]   = ENABLE
```

and defines bit 0 as whether the host is expected to periodically write `BKOPS_START` to **manually** start background operations.

Thus, in the directly inspected 5.0 generic BKOPS control surface:

```text
manual BKOPS handshake exists
AUTO_EN field does not exist in BKOPS_EN
bit 1 is reserved
```

This is a direct register-layout comparison, not an inference from a missing keyword search.

### H/P — e.MMC 5.0 nevertheless acknowledges autonomous internal background operation in a different transition path

B50's Sleep / Power-Off Notification text supplies an important counterexample to an overly simple statement such as `5.0 has no autonomous background operation`.

Before Sleep, a host **may** set `POWER_OFF_NOTIFICATION` to `SLEEP_NOTIFICATION (0x04)` if the host is aware that the device is capable of **autonomously initiating background operations** for possible performance improvements. The host waits for busy de-assertion before entering Sleep.

This historical wording means that by the inspected 5.0 text, device-autonomous internal background work is already a recognized possibility.

But the mechanism is not the same interface relation as 5.1 `AUTO_EN`:

```text
B50 SLEEP_NOTIFICATION opportunity
    -> transition-specific busy interval before Sleep

B51 AUTO_EN
    -> generic host permission for device-initiated background work during idle time
```

The standard itself therefore prevents the simplistic history:

> `autonomous background work` first appears only when `AUTO_EN` appears.

The safer claim is about **host-visible control semantics**, not the first existence of autonomous internal activity.

### H/P — e.MMC 5.1 explicitly separates manual and autonomous initiation

JESD84-B51 §6.6.25 keeps the familiar foreground/background distinction but then adds a further explicit split:

- **manually initiated background operations**;
- **autonomously initiated background operations**.

For the manual method, `MANUAL_EN` remains bit 0 of `BKOPS_EN[163]` and the host still uses `BKOPS_START[164]`.

For the autonomous method, the host sets `AUTO_EN` in `BKOPS_EN[163]` bit 1. While enabled, the device may start or stop background operations whenever it sees fit during idle time, without notifying the host. The standard advises the host to keep device power active while this permission is enabled, and allows the host to set or clear it according to power constraints or other considerations.

### H/P — e.MMC 5.1 turns the formerly reserved bit 1 into `AUTO_EN`

B51 §7.4.82 defines:

```text
BKOPS_EN[163]
    bit[7:2] = Reserved
    bit[1]   = AUTO_EN
    bit[0]   = MANUAL_EN
```

`AUTO_EN` is read/write/erasable (`R/W/E`) and its default is vendor-specific. Its standardized semantic distinction is:

```text
AUTO_EN = 0
    -> device shall not perform background operations while not servicing the host

AUTO_EN = 1
    -> device may perform background operations while not servicing the host
```

The useful endpoint delta is therefore concrete and field-level:

```text
JESD84-B50 / 2013:
    BKOPS_EN bit1 = Reserved
    bit0 = manual handshake

JESD84-B51 / 2015:
    BKOPS_EN bit1 = AUTO_EN
    bit0 = MANUAL_EN
```

### H/P* — the exact insertion revision remains unresolved

B51 is not a direct revision of B50; its cover says `Revision of JESD84-B50.1, July 2014`.

Therefore the direct endpoint comparison supports:

```text
AUTO_EN absent from directly inspected B50
AUTO_EN present in directly inspected B51
```

but **not**:

```text
AUTO_EN was first standardized in B51
```

until B50.1 is directly clause-inspected.

The 2015 announcement's phrase `Background Operation Control` is consistent with a 5.1 control-surface change, but it is not sufficient to erase the intermediate-revision uncertainty.

## Engineering reconstruction

### E — autonomous internal capability is not the same retained relation as generic autonomous-scheduling permission

B50's `SLEEP_NOTIFICATION` wording proves that a device may already possess autonomous background capability while the generic `BKOPS_EN` bit1 remains reserved.

This separates at least three layers:

```text
internal capability
    !=
standardized host-visible permission state
    !=
current autonomous execution
```

A capability can exist without a generic control bit; a control bit can permit behavior without proving that work is currently due; permitted work can remain idle if no work is outstanding.

### E — transition-specific opportunity and regime-wide scheduling authority differ

The B50 Sleep path gives the device a transition-specific interval in which background operations may matter before the host enters Sleep. B51 `AUTO_EN` instead authorizes device-controlled background scheduling whenever the device is idle while that permission remains enabled.

Thus:

```text
one transition-time opportunity
    !=
retained scheduling regime
```

This is an engineering reconstruction of the interface relation, not JEDEC's own conceptual vocabulary.

### E — host-visible policy granularity can change while the hidden maintenance algorithm remains unspecified

The endpoint change exposes a new host-visible control state (`AUTO_EN`) and an explicit manual/autonomous initiation distinction. The standard still does not disclose a universal internal page-selection, relocation, erase, wear-leveling, or retention-refresh algorithm.

Therefore:

> **interface-control evolution != demonstrated hidden-algorithm evolution.**

The same hidden operation family could in principle be scheduled under different host/device authority arrangements; conversely, similar control bits do not prove identical internal work across vendors.

### E — `AUTO_EN` is permission, not debt, progress, or completion

The B51 field says whether the device may perform background work while not servicing the host. It is not `BKOPS_STATUS`, and it is not a progress log.

```text
AUTO_EN = 1
    != background work outstanding
    != background work urgent
    != background work running now
    != background work complete
```

Likewise, `AUTO_EN = 0` does not imply that no maintenance obligation exists; it can mean that the host has withdrawn autonomous scheduling authority.

### E — vendor-specific default does not make the standardized semantic relation vendor-specific

B51 says the `AUTO_EN` default value is vendor-specific, while the meanings of 0 and 1 are standardized.

That gives a useful control-state distinction:

```text
standardized state semantics
    != standardized initial policy choice
```

The repository must not infer a product's actual default without product-specific evidence.

## Functional analogy only

### Manual BKOPS vs autonomous BKOPS

At the project level, the change can be compared to moving from an externally granted maintenance appointment to a standing permission for opportunistic work.

The analogy stops at the authority relation:

```text
host-granted service window
    <functional comparison>
standing device scheduling permission
```

It does not make e.MMC maintenance equivalent to an operating-system scheduler, a human maintenance contract, or DRAM refresh.

### Case 135 Micron/Armadillo self refresh

The later Micron/Armadillo path uses reset, `SET_TIME`, elapsed-time qualification, bus idleness, an ECC-related selection threshold, and vendor telemetry.

Generic B51 `AUTO_EN` proves only that e.MMC has a standard autonomous-background-work permission surface. It does **not** prove:

- that Micron self refresh is implemented as `AUTO_EN` BKOPS;
- that `BKOPS_STATUS` is Micron's self-refresh queue;
- that the one-day rule comes from generic BKOPS;
- that `AUTO_EN` causes retention refresh rather than other hidden maintenance.

The overlap remains **maintenance opportunity / scheduling authority**, not mechanism identity.

## Philosophical interpretation — bounded

A narrow project-level interpretation is defensible:

> Technical maintenance can have a retained **authority state** distinct from both the state being preserved and the maintenance debt that may later act on it.

B50 and B51 make this visible because host/device authority over background work changes at the interface while user payload semantics and the hidden maintenance mechanism remain separately specified or undisclosed.

The interpretation stops there. JEDEC does not present `AUTO_EN`, `BKOPS_EN`, or Sleep notification as a philosophy of autonomy, memory, or temporality.

## Prior-art / chronology result

The safe chronology after this slice is:

```text
by e.MMC 4.41 / 2010:
    public generic manual-BKOPS control surface

JESD84-B50 / e.MMC 5.0 / September 2013:
    mandatory Background Operations
    manual BKOPS_START/BKOPS_EN bit0 path
    BKOPS_EN bit1 reserved
    separate Sleep-notification text recognizes autonomous background-operation capability

JESD84-B50.1 / e.MMC 5.01 / July 2014:
    intermediate revision exists
    exact AUTO_EN semantics not inspected in this slice

JESD84-B51 / e.MMC 5.1 / February 2015:
    explicit manual-vs-autonomous initiation split
    BKOPS_EN bit1 = AUTO_EN
    autonomous idle-time start/stop permission standardized
```

This changes the novelty boundary in two directions at once:

1. **against a late-origin claim:** generic manual BKOPS is much older than 5.1, and autonomous device activity is already acknowledged in B50;
2. **against an early-equivalence claim:** B50's autonomous-capability/Sleep wording is not the same host-visible generic control relation as B51 `AUTO_EN`.

## Explicit non-claims

This evidence does **not** establish that:

1. e.MMC 5.1 invented autonomous Flash maintenance;
2. `AUTO_EN` first appeared in B51 rather than B50.1;
3. B50 devices could never perform background work autonomously;
4. B50 `SLEEP_NOTIFICATION` is the same state machine as B51 `AUTO_EN`;
5. a reserved B50 bit proves anything about undocumented vendor-specific internal controls;
6. every 5.1 device used the same hidden maintenance algorithms;
7. `AUTO_EN=1` means background work is currently executing;
8. `AUTO_EN=0` means no maintenance is due;
9. `BKOPS_STATUS=0` proves all NAND retention margins are freshly renewed;
10. autonomous BKOPS is Micron automotive self refresh;
11. autonomous BKOPS is garbage collection, wear leveling, read reclaim, or sanitize unless product-specific evidence says so;
12. the 2015 announcement alone establishes the exact normative insertion revision;
13. B50.1 semantics can be reconstructed from its title/date alone;
14. identical field names imply identical vendor implementation;
15. interface chronology proves inventor-to-inventor or vendor-to-JEDEC genealogy.

## Resulting bounded relations

```text
standardized Background Operations != first invention of internal maintenance
manual BKOPS support != autonomous BKOPS permission
internal autonomous capability != generic AUTO_EN control surface
Sleep-transition opportunity != idle-regime scheduling permission
AUTO_EN permission != maintenance debt
maintenance debt != maintenance execution
execution != completion
interface-control evolution != hidden-algorithm evolution
standardized bit semantics != standardized default policy
B50 absence + B51 presence != exact first-introduction revision while B50.1 is uninspected
shared idle opportunity != shared retention mechanism
```

## Remaining evidence debt

- directly inspect **JESD84-B50.1 (e.MMC 5.01, July 2014)** and determine whether `AUTO_EN` is present there;
- if exact standardization chronology matters, inspect JEDEC change/ballot records rather than inferring from endpoint covers or press-release wording;
- trace the earlier 4.41→4.5→4.51 evolution only if a retention-specific control change emerges; broader e.MMC protocol genealogy belongs primarily in `computing-archaeology`;
- obtain a named product / controller trace that records `AUTO_EN`, `BKOPS_STATUS`, and actual background-work timing if implementation behavior becomes material;
- keep the standard control surface separate from Micron automotive self-refresh internals until a vendor source explicitly relates them.

Fresh searches of `tmzncty/computing-archaeology` for `BKOPS` and `eMMC background operations` returned no dedicated module to reuse during this pass.