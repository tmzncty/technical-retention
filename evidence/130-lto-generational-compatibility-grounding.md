# Evidence 130 — LTO generational compatibility / reader-obsolescence grounding

**Case:** [`cases/130-lto-generational-compatibility-reader-obsolescence.md`](../cases/130-lto-generational-compatibility-reader-obsolescence.md)

## Question and evidence discipline

What direct technical/institutional evidence supports the bounded claim that a physically surviving LTO cartridge still depends on a compatible drive generation, and that read compatibility, write compatibility, vendor interchangeability, and media survival are different relations?

Labels follow repository convention: `H/P` historical-primary; `H/S` institutional/high-quality secondary or later official continuity; `E` engineering reconstruction; `A` functional analogy; `I` interpretation; `X` rejected overclaim.

This evidence pack is intentionally dominated by official LTO Program and IBM documentation. It does **not** use those current documents to claim invention priority or reconstruct undocumented early-LTO design deliberations.

## S1 — LTO Program generation-compatibility guidance

Source: <https://www.lto.org/lto-generation-compatibility/>

The current official LTO Program page states:

- drive generations 1–7 can read media from two generations prior and write media from the immediately prior generation;
- LTO-8 can read/write LTO-7 and LTO-8 media, including the documented LTO-7 Type M case;
- LTO-9 can read/write LTO-8 and LTO-9 media only;
- LTO-10 can read/write LTO-10 media only.

**Classification:** `H/S` current official-program documentation.

**Supports:** compatibility is generation-bounded and operation-dependent.

**Rejects:** `same LTO family => every later drive reads every earlier cartridge`. (`X`)

## S2 — LTO Program roadmap and the LTO-10 break

Source: <https://www.lto.org/roadmap/>

The current official roadmap states that backward-compatibility policy through generation 7 was two generations for read and one for write; generations 8 and 9 use one-generation-back read/write compatibility; generation 10 does not support backward compatibility. The page attributes the generation-10 break to a drive-head redesign.

**Classification:** `H/S` current official-program documentation.

**Supports:** backward compatibility is a design property that can contract across generations; later hardware need not monotonically subsume earlier read paths.

**Rejects:** `newer hardware => strict superset of legacy-media access`. (`X`)

**Boundary:** the roadmap does not imply that LTO-9 cartridges are erased or instantly inaccessible when LTO-10 exists; an LTO-9-compatible reader can remain available.

## S3 — LTO Program FAQ: interchangeability and backward compatibility are separate claims

Source: <https://www.lto.org/faqs-about-lto/>

The FAQ says use of the Ultrium format trademark follows annual third-party compliance verification intended to ensure compliance with the Ultrium format specification and product interchangeability. In a separate answer it gives the same bounded backward-compatibility rules, including LTO-9 reading/writing LTO-8 and LTO-10 reading/writing only LTO-10.

**Classification:** `H/S` current official-program documentation.

**Supports:** vendor/product interoperability inside the certified format and cross-generation compatibility are separate relations.

**Rejects:** `open/interoperable format => time-unbounded generation compatibility`. (`X`)

## S4 — IBM cartridge compatibility table

Source: <https://www.ibm.com/docs/en/t-tt-and-t?topic=cartridges-cartridge-compatibility>

IBM's current compatibility table distinguishes `Read/Write`, `Read Only`, and unsupported cells for drive/media generation pairs. Examples include:

- Ultrium 6: read/write Ultrium 6 and 5; read-only Ultrium 4;
- Ultrium 7: read/write Ultrium 7 and 6;
- Ultrium 8: read/write Ultrium 8, M8, and 7;
- Ultrium 9: read/write Ultrium 9 and 8.

**Classification:** `H/S` current IBM technical documentation.

**Supports:** `readability ≠ writability`; compatibility is a relation between a drive generation, a cartridge generation, and an operation.

## S5 — IBM LTO-8 Storage Protect support matrix

Source: <https://www.ibm.com/support/pages/node/300753>

IBM records this support page as modified **20 September 2023**. It lists LTO-8 read formats and write formats as Ultrium 7/8 variants and says LTO-8 drives can read/write Ultrium 8 and 7 but cannot read or write Ultrium 6.

It also gives mixed-generation library rules. Where mixed generations are not supported, all scratch and read-write volumes must be readable and writable by all drives; an LTO-8/LTO-7 mix therefore constrains common read-write media to Ultrium 7.

**Classification:** `H/S` vendor support documentation.

**Supports:** a functioning newer drive can exclude an older still-surviving cartridge generation; compatibility intersections become a library/configuration constraint.

**Rejects:** `library contains a working drive => every cartridge in the LTO family is serviceable`. (`X`)

## S6 — IBM LTO-9 Storage Protect support matrix

Source: <https://www.ibm.com/support/pages/node/6487463>

IBM records this page as modified **9 February 2026**. It states that LTO-9 drives support read/write on Ultrium 8 and 9 media, but not M8 or Ultrium 7. It lists `ULTRIUM8`, `ULTRIUM8C`, `ULTRIUM9`, and `ULTRIUM9C` as supported read/write formats.

The mixed-generation section says that in an LTO-9/LTO-8 library without mixed-generation support, Ultrium 8 is the common read-write medium because both drive generations can read/write it.

**Classification:** `H/S` vendor support documentation.

**Supports:** compatibility is a set-intersection problem at fleet/library scope, not only a media-health property.

## S7 — IBM Redbooks continuity for the older two-read/one-write window

Source: <https://www.redbooks.ibm.com/Redbooks.nsf/e03826cbbba0636c852569d000606d00/afdae387b8ecf8c185257fcd0071adfb>

The 2016 IBM Redbooks material for TS3100/TS3200 documents:

- LTO-7 reads/writes LTO-7 and LTO-6 and reads LTO-5;
- LTO-6 reads/writes LTO-6 and LTO-5 and reads LTO-4;
- LTO-5 reads/writes LTO-5 and LTO-4.

**Classification:** `H/S` IBM technical publication, useful as period continuity for the pre-LTO-8 compatibility policy.

**Supports:** the official-program summary of the earlier compatibility window is reflected in IBM product/library documentation.

## S8 — IBM current LTO-10 product family witness

Source: <https://www.ibm.com/products/lto-tape-drive>

IBM's current LTO product family page identifies LTO-10 as the current generation. IBM localized generation tables explicitly describe LTO-10 as having no backward compatibility, consistent with the LTO Program roadmap.

**Classification:** `H/S` current IBM product documentation.

**Use:** corroboration only; the LTO Program remains the better source for the cross-generation rule and its stated head-redesign rationale.

## Claim matrix

| ID | Claim | Label | Best source |
| --- | --- | --- | --- |
| G-130.1 | LTO generation compatibility is bounded rather than universal | `H/S` | S1/S2 |
| G-130.2 | generations 1–7 use a two-generation read / one-generation write backward window | `H/S` | S1/S2/S7 |
| G-130.3 | LTO-8 reads/writes LTO-7/8 but not LTO-6 | `H/S` | S1/S5 |
| G-130.4 | LTO-9 reads/writes LTO-8/9 but not LTO-7 or M8 | `H/S` | S1/S6 |
| G-130.5 | LTO-10 does not provide backward compatibility | `H/S` | S1/S2/S8 |
| G-130.6 | read support and write support can differ for one media generation | `H/S` | S4/S7 |
| G-130.7 | mixed drive generations can constrain the common read-write media set | `H/S` | S5/S6 |
| G-130.8 | Ultrium certification/interchangeability does not imply unlimited generational compatibility | `H/S`,`E` | S3 |
| G-130.9 | surviving cartridge state alone guarantees later access | `X` | S1–S7 |
| G-130.10 | a new incompatible drive generation physically erases older cartridges | `X` | mechanism boundary |
| G-130.11 | newest drive generation is always the best reader for the oldest archive | `X` | S1/S2/S5/S6 |
| G-130.12 | preserving a compatible drive alone guarantees access regardless of host/software/keys | `X` | scope boundary |
| G-130.13 | LTO invented removable-media compatibility or migration | `X` | prior-art boundary |

## Engineering reconstruction

The sources support this bounded relation (`E`):

```text
surviving magnetic inscription
  + compatible drive/media generation pair
  + compatible operation (read or write)
  + usable host/software path
  -> possible archive access
```

Project conclusions:

- `media survival ≠ reader availability`;
- `reader obsolescence ≠ physical erasure`;
- `read compatibility ≠ write compatibility`;
- `newer drive ≠ universal legacy reader`;
- `vendor interchangeability ≠ time-unbounded generation compatibility`;
- `current-generation acquisition ≠ legacy-media access`;
- `generation transition ≠ immediate data loss`;
- bounded reader compatibility can create a migration obligation before compatible readers disappear.

The last point is a reconstruction, not a vendor quotation or a universal migration schedule.

## Functional comparison boundaries

- **Case 129 / ZFS feature flags (`A`):** both require an interpreter relation, but ZFS feature support is software-format admissibility and LTO is a physical drive/media generation gate.
- **Case 111 / enterprise SSD extended shutdown (`A`):** both concern long-lived storage, but Case 111's failure mode can be physical charge-retention degradation; Case 130 can lose practical access with intact magnetic state if the reader disappears.
- **Case 89 / ATA LBA-CHS (`A`):** both reject treating access as a property of payload alone; address translation and tape-generation compatibility are unrelated mechanisms.

No genealogy is inferred from these comparisons.

## Prior-art / related-repository boundary

No invention claim is made. Earlier magnetic-tape and removable-media systems had reader/format compatibility problems. A fresh `computing-archaeology` search found no dedicated `7-track`, `IBM 729`, or `magnetic tape` case in the current search surface, so this repository does not duplicate that wider history.

Direct inspection of IBM 7-track/9-track manuals and other earlier media transitions remains an open companion-repository task before making a detailed genealogy claim.

## Open gaps

Still open:

- direct primary-specification chronology for each LTO generation;
- direct LTO-10 engineering specification / head-geometry evidence beyond the current official roadmap statement;
- named-drive failure/maintenance data for aging legacy readers;
- host-interface and driver obsolescence layered above a preserved tape drive;
- encryption-key and LTFS/software dependencies layered above the drive/media relation;
- controlled migration/fault experiments across real generations;
- earlier IBM 7-track/9-track and other removable-media prior-art archaeology;
- broader optical, floppy, magneto-optical, and proprietary-tape media obsolescence comparisons.
