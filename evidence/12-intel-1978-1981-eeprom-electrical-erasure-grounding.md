# Case 12 grounding record — Intel floating-gate EEPROM electrical erasure, 1978–1981

## Purpose

This record grounds the bounded mechanism claims used by [`../cases/12-intel-2816-eeprom-electrical-erasure.md`](../cases/12-intel-2816-eeprom-electrical-erasure.md).

The case is deliberately narrower than a general history of EEPROM or a teleological `EPROM → EEPROM → Flash` story. It asks what changes in the retention comparison when deliberate forgetting moves from an external optical/radiation intervention into an electrically controlled, address-sensitive operating mode of a nonvolatile memory device.

The two primary source layers are intentionally kept distinct:

1. an Intel manufacturer product/application document for the **2816 E²PROM**, directly inspected as a page-preserving scan, which grounds the actual product's read / byte-erase / byte-write / chip-erase modes, voltages, timing, in-system use, erase geometry, and bounded endurance specification;
2. an Intel-assigned floating-gate tunneling patent with 1978 priority, which grounds a manufacturer-primary physical mechanism for electrically programming and electrically erasing an insulated floating gate through a thin oxide.

The patent is **not silently identified as the exact production 2816 cell topology**. It grounds a contemporary Intel mechanism class; the product document grounds the 2816 operating semantics.

## Source classes

### P1 — Intel 2816 manufacturer datasheet/application document

Intel Corporation, **2816 — 16K (2K × 8) Electrically Erasable PROM**, AFN-01635B, copyright 1981; surviving scan stamped `2. Sep. 1981`.

Page-preserving scan:

<https://ethw-images.s3.us-east-va.perf.cloud.ovh.us/ethw/e/ea/MEMO-data_2816.pdf>

Archive/file record:

<https://ethw.org/File:MEMO-data_2816.pdf>

Directly inspected scan anchors used here:

- printed p. 1: title, `HMOS-E FLOTOX Cell Design`, `Reliable Floating Gate Technology`, single-byte erase/write, 10 ms byte erase/write, 10 ms chip erase, 5 V read supply, single 21 V write/erase pulse, in-system nonvolatile alteration, and Figure 1 functional block diagram;
- printed p. 2: Table 1 `Mode Selection`, separating READ, STANDBY, BYTE ERASE, BYTE WRITE, CHIP ERASE, and E/W INHIBIT; VPP is held at 4–6 V for read/standby and pulsed to 21 V for erase/write;
- printed p. 4: `Write Mode`, explicit contrast with optically erased EPROM, byte versus chip erase, erase-before-data-write sequence, 9–15 ms programming pulse, per-byte cycling independence, and the product requirement of up to `1 × 10^4` erase/write cycles per byte;
- printed p. 5: `Chip Erase Mode`, returning all 2K bytes to logic 1 / `FF` in approximately 10 ms through a distinct chip-erase control condition.

Central sourced facts:

1. Intel calls the 2816 a `16K (2K × 8) ELECTRICALLY ERASABLE PROM` / `E²PROM` and identifies an `HMOS-E FLOTOX Cell Design`.
2. Ordinary read uses a 5 V operating regime, while erase/write requires a 21 V VPP pulse.
3. The device supports **single-byte erase/write** without affecting data in other bytes and also supports **whole-chip erase**.
4. Byte erase and byte write are separate operations: the selected location is erased first; the operation is then repeated with the intended data to write it.
5. Intel explicitly contrasts the 2816's electrical erasure with EPROMs requiring UV light and markets the resulting operation as `in-system` alteration of nonvolatile information.
6. The product is not infinitely rewritable: the manufacturer specifies applications requiring up to `1 × 10^4` erase/write cycles per byte.
7. Chip erase and byte erase are both electrical but are not the same selection/control geometry.

The document contains application-market claims such as the frequency with which byte erase would be useful. Those claims are not required for the retention argument and are not promoted into general historical facts about all EEPROM use.

### P2 — Intel thin-oxide floating-gate tunneling patent

Dov Frohman-Bentchkowsky, Jerry Mar, George Perlegos, and William S. Johnson, Intel Corporation, US4203158A, **Electrically programmable and erasable MOS floating gate memory device employing tunneling and method of fabricating same**. Priority 24 February 1978; filed 15 December 1978; published 13 May 1980.

Primary transcription:

<https://patents.google.com/patent/US4203158A/en>

Mechanism anchors in the patent description:

- the floating polysilicon gate is completely surrounded by oxide so that transferred charge remains on the gate;
- a local thin-oxide region of approximately 70–200 Å is disclosed as the tunneling path;
- programming applies approximately 20 V so electrons tunnel from a doped substrate region onto the floating gate;
- erasing reverses the transfer direction: approximately 20 V at the source-region side causes electrons to tunnel from the floating gate through the thin oxide back into the substrate region;
- state is sensed at approximately +5 V by source-drain current;
- the patent discusses finite program/erase cycling of the thin oxide rather than treating electrical alterability as cost-free;
- the disclosed cells may be combined with a selection transistor for electrically alterable PROM arrays.

Central sourced facts:

1. Electrical erasure can remove the same floating-gate charge whose insulation supplies quiescent nonvolatility.
2. Program, erase, and read use distinct electrical field conditions even though all are electrical operations.
3. Electrical erase does not abolish the physical retention barrier; it creates a controlled field under which carriers cross that barrier.
4. Repeated program/erase stresses the thin-oxide transport path, producing a finite cycling regime.

The patent's preferred-embodiment endurance range and projected retention life are **not transferred to the 2816 product**. For the 2816, only the manufacturer's own `1 × 10^4` per-byte erase/write specification is used.

## Prior-art boundary

US4203158A itself blocks a broad invention-priority claim. Its prior-art section says that electrically erasable integrated-circuit PROMs were already known, including devices using silicon-nitride storage structures, and reviews earlier tunneling and avalanche-erasure approaches.

Accordingly this case does **not** claim:

- Intel invented electrically erasable semiconductor memory in general;
- Frohman/Mar/Perlegos/Johnson invented EEPROM as an unrestricted category;
- FLOTOX is the only path from EPROM to electrical erasure;
- US4203158A is necessarily the exact production cell implementation of the 2816.

The bounded historical claim is narrower: by 1978–1981, Intel primary sources directly document a floating-gate tunneling design with electrical program/erase and a commercial 2816 E²PROM whose erase and rewrite operations are electrical, in-system, and available at byte as well as chip granularity.

## Grounded claim ledger

| Claim | Label | Grounding |
| --- | --- | --- |
| Intel's 1981 2816 is a 16K / 2K×8 electrically erasable PROM using an HMOS-E FLOTOX cell design | H/P | Intel 2816, p. 1 |
| ordinary read and erase/write occupy distinct electrical regimes | H/P | Intel 2816 pp. 1–2; US4203158A |
| the 2816 supports byte-level erase/write without altering adjacent bytes | H/P | Intel 2816 pp. 1, 4 |
| the 2816 also supports whole-chip erase | H/P | Intel 2816 pp. 1, 5 |
| a byte must be erased before the bounded 2816 data-write operation | H/P | Intel 2816 p. 4 |
| Intel describes the device as electrically rather than optically erased and suitable for in-system nonvolatile alteration | H/P | Intel 2816 pp. 1, 4 |
| Intel's 2816 product specification bounds erase/write use to applications requiring up to `1 × 10^4` cycles per byte | H/P | Intel 2816 p. 4 |
| Intel disclosed a floating-gate device programmed and erased by tunneling through a thin oxide | H/P | US4203158A |
| electrically controlled erase means erasure has become identical to ordinary read/write service | X | contradicted by separate VPP, timing, mode, and erase-before-write conditions |
| byte erase means the device has only one erase granularity | X | contradicted by the separate chip-erase mode |
| electrical erasability means unlimited rewrite endurance | X | contradicted by the bounded cycling specification and thin-oxide stress |
| US4203158A proves the exact production transistor topology of the Intel 2816 | X | product-to-patent identity not established by the sources used here |
| Intel invented EEPROM generally | X | blocked by the patent's own prior-art discussion |
| Intel 2816 byte erase should be called Flash block erase | X | later Flash terminology/mechanism must be separately sourced |

## Engineering reconstruction supported by the sources

The bounded retention relation is now:

```text
quiescent hold
    floating-gate charge remains behind an insulating barrier

read
    low-voltage sensing recovers the state without invoking erase/program stress

byte erase
    address/control selects one byte
    + elevated VPP / timed erase condition
    -> stored state is reset electrically

byte write
    erase first
    + elevated VPP / timed data-write condition
    -> new byte state is established

chip erase
    separate control condition
    -> all bytes are reset together
```

This changes Case 11's partition without making it disappear. EPROM established:

```text
electrical program/read geometry != external radiation erase geometry
```

The 2816 establishes a different relation:

```text
electrical erase can enter the address/control system
    while still requiring
special voltage + timing + mode + finite cycling budget
```

Electrical control therefore changes **who/what can authorize forgetting and at what granularity**, not the fact that erasure is a physically exceptional state-changing operation.

## Failure / forgetting boundaries

The primary sources support several distinct failure classes:

- **retention failure:** trapped charge no longer remains within the state margin;
- **erase failure:** the selected byte or chip is not fully returned to the intended erased state;
- **program/write failure:** the new state is not established after erase;
- **mode/control failure:** ordinary read, byte erase, byte write, chip erase, and inhibit conditions are not correctly separated;
- **high-voltage/timing failure:** the required erase/write pulse is absent, mistimed, or otherwise out of specification;
- **endurance exhaustion / oxide degradation:** repeated charge transport consumes a finite cycling budget.

The 2816 product document does not justify a universal EEPROM wear law, and the patent's endurance discussion is not a license to infer a precise failure distribution for the 2816.

## Anti-anachronism and terminology controls

Direct period terms retained in the case include:

- `electrically erasable PROM` / `E²PROM`;
- `HMOS-E FLOTOX Cell Design`;
- `byte erase`;
- `byte write`;
- `chip erase`;
- `VPP` / programming voltage;
- `in-system alteration`;
- `floating gate`;
- `tunneling`.

Project comparison terms such as `erase authority`, `erase geometry`, `exceptional maintenance`, and `endurance-bounded forgetting` are modern analytical labels and must remain marked as such.

`Flash`, `sector erase`, `page program`, `block erase`, FTL, wear leveling, ECC, and SSD-controller vocabulary are not assigned to the 2816. The later Flash transition requires a separate period-primary case.

## Related-repository duplication check

Searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `EEPROM`, `FLOTOX`, `2816`, and floating-gate / Flash combinations returned no dedicated EEPROM case to reuse.

Accordingly this record keeps only the retention-specific transition from external erase to electrically orchestrated erase. A broader semiconductor-memory genealogy, process history, vendor comparison, and device-economics account belongs primarily in `computing-archaeology` if developed later.

## Promotion decision

**Case 12 is `grounded` at the bounded product-and-mechanism level.**

Promotion is justified because:

- a directly inspected Intel manufacturer scan gives product-specific read/erase/write modes, voltages, timing, erase granularity, in-system semantics, and endurance bounds;
- an Intel-assigned period patent directly supplies a floating-gate electrical program/erase tunneling mechanism;
- the patent's own prior-art discussion prevents a false broad invention-priority claim;
- product semantics are not silently equated with the exact patent embodiment;
- historical vocabulary and modern comparison terms are separated;
- failure/forgetting and endurance boundaries are explicit;
- related-repository duplication was checked.

The next bounded bridge is **not another generic EEPROM survey**. It should isolate the later Flash transition in which electrically erasable floating-gate storage deliberately adopts a coarser erase unit / fast bulk erase organization, and ask what that change does to forgetting geometry, rewrite work, copying/reclamation, and endurance. Case 04 can then be linked upward as the controller/mapping consequence without rewriting its already-grounded FTL history.
