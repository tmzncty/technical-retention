# Evidence Addendum — FTL Terminology and PCMCIA Chronology, 1995–1996

## Purpose

This addendum deepens only the **terminology / standardization chronology** around [`Case 04`](../cases/04-flash-virtual-mapping-logical-identity.md). It does not change the bounded mechanism claim grounded in Amir Ban's 1993-filed `Flash file system` patent, and it does not claim that the phrase `Flash Translation Layer` names every earlier Flash mapping system.

The narrow questions are:

1. how early can public use of the term `Flash Translation Layer (FTL)` be directly attested in the currently inspected record?
2. can term use, PCMCIA approval, and a later-reported specification release date be kept distinct?

The answer from the bounded record is:

```text
public technical use by February 1995
        !=
first coinage / invention
        !=
PCMCIA approval event
        !=
public specification release date
```

---

## Source A — Dr. Dobb's, February 1995

**Type:** `H/S` — contemporary technical press; useful contemporaneous terminology evidence, but not the primary PCMCIA standard text.

**Article:** `FEB95: The Microsoft Flash File System`

**Date:** February 1995.

**Preserved transcription:** <https://jacobfilipp.com/DrDobbs/articles/DDJ/1995/9502/9502h/9502h.htm>

### Terminology evidence

The article describes a sector-translation device-driver approach and says that this type of driver is commonly known as a **Flash Translation Layer (FTL)**. It then explains the same broad interface problem that later FTL material addresses: DOS/FAT sector requests are translated to physical Flash locations, metadata records the sector arrangement, reads resolve a logical sector to a physical address, and cleanup reclaims deallocated space when clean space is exhausted.

This supports a conservative terminology floor:

> **`Flash Translation Layer (FTL)` was already in public contemporary technical use by February 1995.**

It does **not** establish:

- that February 1995 was the first coinage of the term;
- that Dr. Dobb's, Microsoft, Intel, or PCMCIA invented the underlying mapping idea;
- that every earlier virtual-map / Flash-file-system mechanism should be renamed `FTL`;
- the exact date on which PCMCIA balloted, approved, published, or distributed an FTL specification.

The wording `commonly known` is itself evidence against treating this article as a priority claim: it presents the term as already circulating.

---

## Source B — Intel AP-619, August 1995

**Type:** `H/P` — contemporary manufacturer application note reporting a PCMCIA-approved format.

**Document:** Kirk Blum and Peter Lam, `FTL Logger: Exchanging Data with FTL Systems`, Intel Application Note AP-619, order no. 292174-001, August 1995.

**Preserved scan already used by Evidence 04:** <https://intel-vintage-developer.eu5.org/DESIGN/FLCARD/APPLNOTS/292174_1.PDF>

Intel reports that several companies worked with Intel and PCMCIA to standardize the Flash-media format and says that the format had recently been approved by PCMCIA as the **Flash Translation Layer (FTL)** format.

AP-619 therefore remains the stronger primary-vendor anchor for the **PCMCIA approval relation** even though Source A moves the public terminology floor earlier.

The two claims are compatible:

```text
term publicly used by Feb 1995
        +
Intel reports recent PCMCIA approval by Aug 1995
```

Neither claim establishes first coinage.

---

## Source C — Later Intel patent record reporting a May 1996 specification release

**Type:** `H/P` (later retrospective record) — primary patent text from an Intel-assigned Flash-interface filing, used only for the chronology distinction it states.

**Record:** `Improved register interface for flash EEPROM memory arrays`, Google Patents record: <https://patents.google.com/patent/WO1998029876A1/en>

The patent text describes an upper-level `flash translation layer (FTL)` driver and parenthetically identifies a **PCMCIA specification release date of May 1996**.

This later statement must not be silently substituted for a contemporaneous PCMCIA ballot/publication record. Its value here is narrower: it shows why `approved` and `released` should not be collapsed into one event.

Accordingly, the safest bounded chronology is:

```text
February 1995
    public contemporary technical use of FTL terminology

August 1995
    Intel AP-619 reports that PCMCIA had recently approved the FTL format

May 1996
    later Intel patent text reports a PCMCIA specification release date
```

The exact PCMCIA ballot, approval, publication, and distribution chronology remains open until primary PCMCIA records are inspected directly.

---

## Claim ledger

| Claim | Label | Evidence | Status |
| --- | --- | --- | --- |
| `Flash Translation Layer (FTL)` was in public contemporary technical use by February 1995 | `H/S` | Dr. Dobb's, February 1995 | grounded as a terminology floor |
| Intel documented FTL as a PCMCIA-approved format by August 1995 | `H/P` | Intel AP-619, August 1995 | grounded |
| A later Intel patent record reports a PCMCIA specification release date of May 1996 | `H/P` later retrospective | WO1998029876A1 text | grounded only as a later-reported release date |
| February 1995 was the first coinage of `FTL` | `X` | no priority evidence | rejected / unsupported |
| PCMCIA approval and specification release are necessarily the same dated event | `X` | AP-619 versus later release-date report | rejected |
| Ban's 1993 `virtual map` terminology should be retroactively rewritten as historical `FTL` vocabulary | `X` | Ban uses its own vocabulary | rejected |
| Shared FTL terminology proves one implementation or algorithm | `X` | sources describe an abstraction family, not one fixed mapping/cleanup implementation | rejected |

---

## Engineering reconstruction

The terminology chronology does not change the mechanism already grounded in Case 04. It clarifies the relation between **mechanism history** and **name history**:

```text
mapping / relocation mechanism can exist
        ↓
without the later umbrella name being used in that source

later umbrella name can become common
        ↓
without proving one origin, implementation, or exact standard-release event
```

For this repository that yields a reusable rule:

> **mechanism attestation ≠ terminology attestation ≠ standardization milestone ≠ invention priority.**

---

## Functional analogy boundary

Later SSD documentation can use `FTL` for controller translation layers that are much more elaborate than the 1993–1995 systems discussed here. The functional continuity is useful at the level of logical-to-physical indirection, but it does not prove identical mapping granularity, metadata layout, cleanup policy, wear policy, error recovery, or controller architecture.

---

## Related-repository boundary

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) surfaced no dedicated FTL terminology / PCMCIA chronology case to reuse. Broad Flash/SSD/FTL engineering genealogy still belongs there if developed; this addendum remains limited to the retention project's terminology and anti-anachronism boundary.

---

## Remaining open work

- directly inspect the full 1987 Masuoka et al. IEDM paper already flagged by Case 04;
- locate primary PCMCIA ballot / specification copies that can date approval, publication, and distribution directly;
- search for pre-February-1995 public or internal uses of `Flash Translation Layer` before making any first-use claim;
- keep exact FTL implementation genealogy in `computing-archaeology` rather than expanding this addendum into a general SSD history.
