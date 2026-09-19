# LTO Generational Compatibility: Retained Reader Dependency and Media Obsolescence

**Status:** `grounded`

Grounding record: [`../evidence/130-lto-generational-compatibility-grounding.md`](../evidence/130-lto-generational-compatibility-grounding.md).

Deepening record: [`../evidence/130-ibm-2003-2010-lto-bridge-generation-host-path-deepening.md`](../evidence/130-ibm-2003-2010-lto-bridge-generation-host-path-deepening.md).

## Scope

This case asks one bounded retention question:

> If an LTO Ultrium cartridge and its recorded magnetic state survive, what additional hardware and access-path compatibility relations must also survive for a later system to read or rewrite that cartridge?

The evidence base is deliberately narrow: official LTO Program compatibility documentation, IBM cartridge/drive compatibility documentation, IBM Storage Protect support matrices for LTO-8 and LTO-9, IBM Redbooks continuity, and period IBM product records for LTO-2/LTO-3 plus later IBM host-attachment documentation. The purpose is not to write a general magnetic-tape history, but to isolate **media/device obsolescence and reader-path obsolescence as retention boundaries**.

This is not a study of magnetic coercivity, binder chemistry, shelf life, bit decay, LTFS internals, encryption-key retention, every LTO generation, or the entire history of tape-format migration. It does not claim that LTO invented generational compatibility or media migration.

Fresh searches of `tmzncty/computing-archaeology` for `7-track`, `IBM 729`, `magnetic tape`, and `LTO` found no dedicated tape-history / LTO packet in the current search surface. Broader tape-device genealogy, IBM 7-track/9-track transitions, SCSI/Fibre-Channel/SAS attachment history, transport mechanics, and recording-density history belong there if developed.

## Vocabulary and claim boundary

Source vocabulary includes:

- `backward compatibility` / `backwards compatibility`;
- `read` and `write` compatibility;
- `generation`;
- `media` / `cartridge`;
- `read format` and `write format`;
- `interchangeability` / interoperability;
- mixed-generation libraries;
- SCSI, Fibre Channel, SAS, host interface, device driver, and host-bus adapter.

Project engineering vocabulary (`E`) includes:

- **reader dependency** — the requirement that a compatible drive generation remain available for surviving media;
- **compatibility window** — the bounded set of media generations a particular drive can read and/or write;
- **media-device admissibility** — whether a given drive/media/operation tuple is supported;
- **migration obligation** — the operational need to move retained data before the required reader population disappears;
- **bridge generation** — a drive generation that still provides a supported operation on older media during a migration path;
- **last writable bridge** / **last readable bridge** — operation-specific endpoints of that documented path;
- **host-attachment admissibility** — whether the retained drive can still participate in a supported host/interface/software configuration.

These project terms are not attributed to LTO Program or IBM authors.

## Historical / institutional record

### H/S — LTO compatibility is explicitly bounded by generation

The current LTO Program compatibility guidance states that drives through generation 7 can read media from two generations back and write media from one generation back. It then records narrower later windows:

- LTO-8 reads/writes LTO-8 and LTO-7 media (including the documented LTO-7 Type M case);
- LTO-9 reads/writes LTO-9 and LTO-8 media;
- LTO-10 reads/writes LTO-10 media only.

The current LTO Program roadmap likewise says generations through 7 supported two-generation read / one-generation write backward compatibility, generations 8 and 9 support one generation back, and generation 10 does **not** support backward compatibility. The roadmap attributes the LTO-10 break to a drive-head redesign.

These are current official-program statements, not contemporaneous invention records.

The retention consequence is direct:

> **same LTO family ≠ unlimited cross-generation readability.**

### H/P — the early IBM bridge can be seen directly in period product records

IBM's 3580 Model L23 LTO-2 product record gives a worldwide announce date of **9 September 2003** and says the LTO-2 drive can read and write original LTO-1 cartridges.

IBM's 2005-era 3583 material then says LTO-3 drives read and write LTO-2 cartridges but read LTO-1 cartridges. IBM's current compatibility table makes the next endpoint explicit: LTO-4 supports LTO-4/LTO-3 read-write and LTO-2 read-only, not LTO-1.

For one unchanged media generation, the inspected sequence is therefore:

```text
LTO-1 cartridge + LTO-2 drive -> read/write
LTO-1 cartridge + LTO-3 drive -> read-only
LTO-1 cartridge + LTO-4 drive -> unsupported in the documented matrix
```

This is a period-product grounding of a staged operation horizon, not only a current LTO Program retrospective.

### H/S — read compatibility and write compatibility are different axes

IBM's cartridge-compatibility table makes the asymmetry concrete. For example, an Ultrium 6 drive is documented as read/write for Ultrium 6 and 5 media but read-only for Ultrium 4. The LTO-1 bridge sequence above shows the same distinction in earlier IBM product generations.

Therefore:

> **readable ≠ writable.**

A retained cartridge can remain recoverable for extraction even after it has fallen outside the generation's writable set.

### H/S — later drives do not monotonically subsume all earlier media

IBM's LTO-8 Storage Protect guidance, modified 20 September 2023, says LTO-8 drives can read/write Ultrium 8 and 7 media but cannot read or write Ultrium 6 media. IBM's LTO-9 guidance, modified 9 February 2026, says LTO-9 drives read/write Ultrium 9 and 8 but not M8 or Ultrium 7.

The current IBM cartridge table and LTO Program material extend the same point to LTO-10: the newest generation is not a universal reader for previous LTO media.

Thus:

> **newer drive generation ≠ superset of every older reader capability.**

### H/S — mixed-generation libraries expose compatibility as an operational constraint

IBM's LTO-9 Storage Protect documentation says that where mixed generations are not supported, all scratch volumes and read-write volumes must be readable and writable by all drives. In an LTO-9/LTO-8 mix, the common read-write medium is Ultrium 8; LTO-9-only media cannot be treated as writable by the LTO-8 drives.

This is useful because it moves the issue above one cartridge/drive pair. A library can contain functioning drives and intact cartridges yet still require topology/configuration choices based on the intersection of their compatibility sets.

### H/S — interoperability inside a format does not erase the generation boundary

The LTO Program FAQ says the Ultrium trademark is granted after annual third-party compliance verification intended to support interchangeability among Ultrium-format products. That is a same-format/vendor-interoperability claim.

It does not imply that every future Ultrium drive reads every historical Ultrium cartridge. The same official program separately publishes bounded generation-compatibility rules.

Therefore:

> **vendor interchangeability ≠ time-unbounded generational compatibility.**

### H/P/H/S — the reader itself sits inside a host attachment and software relation

IBM's September 2003 3580 L23 record documents an **Ultra160 SCSI LVD** attachment, bundled SCSI cabling/termination, open-systems device drivers, minimum OS levels, supported host families, and bus/cable limits. IBM's 2005 3583 record documents LTO-3 attachment variants using Ultra160 LVD SCSI and 2 Gbps switched-fabric Fibre Channel. A later IBM Gen 3 / Gen 4 product overview documents 6 Gbps SAS, supported host-bus adapters, supported systems, supported operating systems, and backup software.

The bounded historical point is:

> **compatible tape drive ≠ host-independent reader.**

IBM documented these drives as components of host/interface/software configurations. This does not mean that every configuration outside an IBM support matrix is physically impossible.

## Retained relation

The bounded engineering reconstruction is now:

```text
surviving cartridge / recorded magnetic state
        +
compatible drive generation
        +
requested operation (read or write)
        +
compatible host attachment / HBA / cabling path
        +
usable driver / OS / application path
        ->
possible data access
```

The case does not claim every term is independently sufficient.

At the media/drive layer, LTO documentation demonstrates a generation-indexed relation:

```text
media_admissible = f(drive generation, media generation, operation)
```

At the apparatus/host layer, IBM product documentation additionally demonstrates that the retained reader is deployed through named attachment and software requirements.

The relation is not reducible to cartridge survival alone, and it is not reducible to cartridge-plus-drive survival alone.

## Engineering reconstruction

### E — media survival and reader survival are separate retention problems

A cartridge may remain physically intact while the available drive fleet moves beyond its compatibility window. Conversely, preserving a compatible old drive can extend practical access without changing the recorded cartridge state.

Hence:

> **media survival ≠ reader availability.**

and:

> **reader obsolescence ≠ physical erasure.**

This is the media/device analogue of an interpreter dependency: legibility is relational.

### E — compatibility loss can occur in stages

The LTO-1 / LTO-2 / LTO-3 / LTO-4 sequence gives a clean staged form:

```text
read/write authority
    -> read-only authority
    -> no documented media authority
```

Nothing in that sequence requires the LTO-1 cartridge inscription itself to change. What changes is the relation between the media generation, the available drive generation, and the requested operation.

Therefore:

> **last writable bridge ≠ last readable bridge.**

and:

> **rewrite window ≠ recovery/extraction window.**

The pattern must not be projected mechanically onto LTO-8/9/10, whose official compatibility windows differ.

### E — a compatibility window can create a migration obligation

If a later generation no longer reads an older medium, data migration must occur while at least one compatible read path still exists, unless an older reader is intentionally retained and kept serviceable.

The period LTO-1 sequence makes the planning boundary finer: migration can become relevant already when an archive enters a **read-only bridge**, before the last extraction path disappears.

This is not an LTO Program quotation. It is a project reconstruction from the published compatibility records.

The important boundary remains:

> **generation transition ≠ immediate data loss.**

No universal migration cadence is inferred.

### E — preserving the drive does not preserve the whole reader path

The 2003 IBM record makes a second retention boundary visible:

```text
media-to-drive compatibility
    !=
drive-to-host attachment compatibility
    !=
host-to-driver/software usability
```

A retained 3580 L23 drive may satisfy the LTO-1 media relation while practical access still depends on a workable Ultra160 LVD SCSI path, cabling/topology, host adapter, driver/OS, and application route.

So:

> **drive survival ≠ host attachability.**

> **host attachability ≠ supported software path.**

> **media + drive survival ≠ documented end-to-end recoverability.**

This does not claim a modern adapter or unofficial software path can never work; it says those paths must be established rather than inferred from drive possession alone.

### E — interface succession is a second obsolescence axis

The named IBM records expose LTO reader products through Ultra160 LVD SCSI, Fibre Channel, and SAS attachment variants.

The retention lesson is not that one interface necessarily replaces another on a precise date. It is narrower:

> **media-generation compatibility and apparatus-to-host compatibility are independent access relations.**

An archive can therefore lose practical accessibility at either layer.

### E — latest hardware is not necessarily the archive's reader

LTO-10's documented lack of backward compatibility provides a particularly clean counterexample to the assumption that hardware refresh automatically preserves old-media access.

> **current-generation acquisition ≠ legacy-media access.**

A retention program therefore may need to preserve old drives, preserve or reconstruct an attachment/software path, maintain a staged migration ladder, or some combination. This is an engineering conclusion, not a universal prescription.

### E — compatibility is a relation, not a media property

Calling an LTO-7 cartridge “readable” without naming a drive generation hides the relevant condition. Calling an old drive “usable” without naming its host path hides another condition.

The defensible form is relational:

```text
LTO-7 cartridge + LTO-8 drive + read -> documented supported media path
LTO-7 cartridge + LTO-9 drive + read -> documented unsupported media path

LTO-2-era drive + retained cartridge
    != automatically a usable host/software path
```

This is different from saying the cartridge itself became physically unreadable or the drive itself physically failed.

## Prior-art boundary

No invention-priority claim is made. Magnetic-tape systems had format/device compatibility, host-interface dependencies, and migration problems long before LTO.

The 2003–2005 IBM records improve the **contemporaneous product-history floor inside this case**; they do not establish the origin of backward compatibility or reader obsolescence. A broader chronology — including IBM 7-track/9-track transitions and earlier removable-media reader dependencies — belongs in `computing-archaeology` once primary manuals are directly inspected.

Project terms such as `bridge generation`, `last writable bridge`, `last readable bridge`, and `apparatus-to-host boundary` are engineering vocabulary, not IBM/LTO historical terminology.

## Cross-case boundaries

- **Case 129 / ZFS feature flags:** both show that surviving state may require a compatible interpreter, but Case 129's gate is software-format semantics while Case 130 includes both drive/media generation compatibility and host-attachment compatibility. `software-format admissibility ≠ physical reader admissibility ≠ host attachment admissibility`.
- **Case 111 / enterprise SSD extended shutdown:** Case 111 asks whether flash remains physically recoverable through an offline interval and maintenance schedule. Case 130 can fail even with perfectly preserved magnetic state because the required reader or its access path is unavailable. `media decay ≠ reader/apparatus obsolescence`.
- **Case 89 / ATA LBA-CHS addressing:** both involve a relation between stored state and an access mechanism, but address translation and removable-media generation / host attachment are unrelated mechanisms.

These are functional analogies (`A`), not genealogy.

## Philosophical interpretation

`I` — A durable inscription is not by itself a durable access path. Technical retention can require preserving a **relation between object and reader**, not only preserving the object.

`I` — The early LTO bridge sequence shows that access authority can age in stages: the same retained object can move from writable to read-only to unsupported as the surrounding reader fleet changes.

`I` — Preserving the reader object is still not the end of the chain. Practical legibility may depend on `medium -> drive -> interface -> host -> driver/software`.

`I` — Obsolescence is therefore sometimes non-destructive. Nothing needs to erase a cartridge for an institution to lose practical access; the compatible apparatus or attachment chain can disappear first.

These are project interpretations, not LTO/IBM historical claims.

## Limits

This case does not establish that:

- all older LTO cartridges remain physically good until their readers disappear;
- every unsupported drive/media pair is mechanically loadable or safely usable;
- `unsupported` means `physically impossible`;
- preserving a drive alone guarantees future access;
- preserving one old SCSI/FC/SAS adapter alone guarantees a complete future access path;
- every configuration omitted from an IBM supported-server matrix is technically impossible;
- a protocol converter necessarily restores a vendor-supported path;
- the LTO-1 -> LTO-2 -> LTO-3 -> LTO-4 operation sequence can be projected unchanged to later generations;
- LTO-10's design choice makes LTO-9 media immediately inaccessible where LTO-9 drives still exist;
- LTFS removes drive-generation or host-path compatibility limits;
- open-format branding means universal historical compatibility;
- media migration has one optimal interval;
- LTO invented backward compatibility, archive migration, host-interface obsolescence, or removable-media obsolescence.

## Evidence debt after the 130B deepening

The broad gaps around **earlier-generation period chronology** and **host-interface / driver dependency** are now partially closed and reframed. Remaining narrow debts include:

- contemporaneous launch/specification records for LTO-4 through LTO-10 rather than only later continuity matrices;
- direct engineering evidence for why individual generations changed their compatibility windows;
- direct LTO-10 head/servo/format engineering evidence beyond the current LTO Program roadmap statement;
- named archive migrations performed before the last compatible reader class disappeared;
- failure, maintenance, spare-parts, and serviceability data for retained legacy drives;
- controlled recovery experiments through old drives and modern adapter paths;
- encryption-key, LTFS, catalog, and application-layer dependencies above the hardware path;
- earlier magnetic-tape reader prior art in `computing-archaeology`.

## Sources

- LTO Program, **Roadmap**: <https://www.lto.org/roadmap/>
- LTO Program, **Frequently Asked Questions about LTO**: <https://www.lto.org/faqs-about-lto/>
- LTO Program, **LTO Generation Compatibility Details**: <https://www.lto.org/lto-generation-compatibility/>
- IBM Documentation, **Cartridge Compatibility**: <https://www.ibm.com/docs/en/t-tt-and-t?topic=cartridges-cartridge-compatibility>
- IBM Support, **Overview — IBM TotalStorage Ultrium Tape Drive (3580-L23)**, product record with worldwide announce date 9 September 2003: <https://www.ibm.com/support/pages/overview-ibm-totalstorage-ultrium-tape-drive-3580-l23>
- IBM Support, **User's Guide — IBM 400/800GB LTO 3 tape drive**, release date 5 May 2005: <https://www.ibm.com/support/pages/users-guide-ibm-400800gb-lto-3-tape-drive>
- IBM Support, **IBM TotalStorage Ultrium Scalable Tape Library 3583 Setup and Operator Guide for Multi-path Libraries**, publication `GA32-0411-06`, copyright 2003/2005: <https://www.ibm.com/support/pages/ibm-totalstorage-ultrium-scalable-tape-library-3583-setup-and-operator-guide-multi-path-libraries>
- IBM Support, **Overview — IBM Half-High LTO Gen 3 External SAS Tape Drive, IBM Half-High LTO Gen 4 External SAS Tape Drive**: <https://www.ibm.com/support/pages/overview-ibm-half-high-lto-gen-3-external-sas-tape-drive-ibm-half-high-lto-gen-4-external-sas-tape-drive>
- IBM Support, **HPE, IBM, and Quantum Ultrium Generation 8 (LTO-8) Drive Configuration Information for IBM Storage Protect Server**, modified 20 September 2023: <https://www.ibm.com/support/pages/node/300753>
- IBM Support, **HPE, IBM, and Quantum Ultrium Generation 9 (LTO-9) drive configuration information for IBM Storage Protect Server**, modified 9 February 2026: <https://www.ibm.com/support/pages/node/6487463>
- IBM Redbooks, **IBM TS3100 and TS3200 Tape Libraries** (2016): <https://www.redbooks.ibm.com/Redbooks.nsf/e03826cbbba0636c852569d000606d00/afdae387b8ecf8c185257fcd0071adfb>
- IBM, **LTO Tape Drive** (current product family, including LTO-10): <https://www.ibm.com/products/lto-tape-drive>
