from pathlib import Path
import re

SYNTHESIS_PATH = Path('docs/SYNTHESIS_22_ERASE_INVALIDATION_SANITIZATION_VERIFICATION.md')

SYNTHESIS = r'''# Synthesis 22 — Erase, Invalidation, Sanitization, and Verification

## Status

**Bounded cross-case synthesis** — this document reuses already-grounded historical and technical evidence from Cases 04, 11, 12, 13, 44, 47, and 84. It adds no invention-priority claim and does not replace the primary-source grounding records attached to those cases.

The bounded question is:

> When a technical system says that a state has been deleted, erased, reset, reclaimed, overwritten, or sanitized, which retained relation has actually been destroyed, and what evidence is sufficient to know that the intended forgetting operation completed?

This synthesis advances the Phase-4 `physical erase` and `overwrite` roadmap items specifically at the floating-gate / Flash / SSD interface layer. It does **not** close physical forgetting across magnetic recording, optical media, phase-change media, analog remanence, or every contemporary SSD implementation.

It also extends [`SYNTHESIS_AUDIT_05_TECHNICAL_FORGETTING.md`](SYNTHESIS_AUDIT_05_TECHNICAL_FORGETTING.md). That audit established, from the repository's first five grounded regimes, that logical invalidation and physical erasure are different events. The present synthesis asks a narrower later question: what additional distinctions become mandatory once the repository includes historical erase mechanisms, mapped Flash, standardized sanitization, and controller-bypassing verification.

---

## 1. Evidence base and historical boundaries

The historical record remains in the canonical cases and their evidence ledgers:

- [`Case 11 — Intel/Frohman Floating-Gate EPROM`](../cases/11-intel-frohman-floating-gate-eprom-erasure.md): 1970–1971 Intel/Frohman disclosures ground trapped-charge retention, addressed electrical programming, nondestructive lower-stress read, and deliberate discharge by radiation. Earlier Kahng/Bell Labs floating-gate work blocks an unrestricted invention claim.
- [`Case 12 — Intel 2816 EEPROM`](../cases/12-intel-2816-eeprom-electrical-erasure.md): Intel's 1981 product documentation grounds byte erase/write, chip erase, elevated-voltage/timed electrical control, erase-before-write, and finite cycling. The case does not identify the accompanying Intel tunneling patent as the exact production 2816 cell.
- [`Case 13 — Early Flash EEPROM`](../cases/13-early-flash-coarse-erase-asymmetric-rewrite.md): 1980–1988 Toshiba/Intel evidence grounds shared/coarse erase authority, whole-array electrical erase in bounded designs, finer program/read selection, verify work, and the density/control tradeoff. It does not project later FTL vocabulary backward.
- [`Case 04 — Flash Virtual Mapping`](../cases/04-flash-virtual-mapping-logical-identity.md): 1992–1998 evidence grounds out-of-place update, `deleted`/dirty old embodiments, copy-current → erase-old → remap reclamation, and logical identity surviving physical relocation.
- [`Case 44 — NVMe Deallocate and Sanitize`](../cases/44-nvme13-deallocate-sanitize-forgetting.md): NVMe 1.3 distinguishes advisory Deallocate from Sanitize and distinguishes Block Erase, Crypto Erase, and Overwrite; earlier ATA and TCG evidence supplies bounded prior-art controls.
- [`Case 47 — FAST '11 SSD Sanitization Verification`](../cases/47-fast11-ssd-sanitization-verification.md): Wei et al. bypass the controller and inspect raw flash, showing that ordinary-interface disappearance, advertised command support, reported success, and verified removal of digital remnants are not equivalent.
- [`Case 84 — NVMe ZNS Reset Zone`](../cases/84-nvme-zns-zone-reset-logical-reuse.md): Reset Zone returns an eligible zone to `ZSE:Empty`, rewinds its write pointer, and marks logical blocks deallocated for reuse without thereby becoming NVMe Sanitize or proving physical media erasure.

The chronology is useful only as a set of bounded mechanism changes. It must not be rewritten as an inevitable linear ladder `EPROM -> EEPROM -> Flash -> SSD sanitization`, nor as an invention genealogy running through every cited actor and standard.

---

## 2. Historical record: one word `erase` already covers different operations

### 2.1 Radiation discharge in the bounded EPROM case

Case 11's Intel/Frohman evidence makes erasure a physical discharge route different from normal read and electrical programming. The important historical fact is not merely that the device can be forgotten; it is that the retention barrier, program mechanism, read mechanism, and deliberate erase intervention are physically and operationally distinct.

At this layer:

```text
program/read selection
    !=
erase intervention
```

and nonvolatility means resistance to ordinary power removal, not immunity to an intentionally imposed erasure environment.

### 2.2 Electrical erasure does not imply one erase granularity

Case 12's Intel 2816 moves erasure into electrical, in-system control while preserving exceptional voltage, timing, sequencing, and finite cycling. The same named device exposes both byte erase and chip erase.

Therefore the historical transition `optical erase -> electrical erase` does **not** establish:

```text
electrical erase = ordinary overwrite
```

or:

```text
electrical erase = one fixed physical scope
```

Erase authority has a geometry of its own.

### 2.3 Early Flash deliberately makes forgetting coarser than ordinary access

Case 13 supplies a stronger asymmetry. In the bounded Toshiba/Intel Flash designs, read/program selection remains finer than the shared or whole-array erase operation. Intel's command/verify machinery also demonstrates that a coarse physical state change can require much finer observation and control work.

Thus:

```text
erase domain
    !=
read/program addressability
    !=
verification granularity
```

The historical evidence supports this asymmetry without asserting that those early devices already had an FTL or SSD garbage collector.

---

## 3. Engineering reconstruction: five layers of technical forgetting

The following vocabulary is an **engineering reconstruction**. It is not substituted for the historical actors' own terms.

### Layer A — current logical identity / allocation

A system decides which value or embodiment currently counts for a logical identity. Marking an old Flash block `deleted`, deallocating an LBA, or returning a ZNS zone to Empty can change this relation while some lower-layer physical state survives.

### Layer B — physical medium state

A cell or recording region undergoes a state-changing operation such as floating-gate discharge or Flash block erase. This is the narrowest sense in which this synthesis uses **physical erase**.

### Layer C — reclamation / reuse authority

A former embodiment becomes available for later use. In mapped Flash, current contents can be copied elsewhere before an erase unit is reclaimed. Reclamation therefore concerns safe reuse and free-space recovery, not necessarily secure destruction of every prior witness.

### Layer D — sanitization objective / contract

A storage interface can require prior user data to become inaccessible across a scope broader than currently allocated LBAs. NVMe explicitly permits Block Erase, Crypto Erase, and Overwrite as distinct sanitize mechanisms.

### Layer E — evidence that forgetting actually occurred

A request, command completion, operation-completion status, and independent lower-layer verification are different evidentiary states. FAST '11 demonstrates why this layer cannot be omitted: a controller can report success while raw-flash fingerprints remain.

The central decomposition is therefore:

```text
logical invalidation
    !=
physical erase
    !=
reclamation / reuse
    !=
sanitization objective
    !=
verification evidence
```

No one of these layers can safely stand in for all the others.

---

## 4. Logical invalidation can precede physical erasure

Mapped Flash Case 04 already supplies the cleanest counterexample. A rewritten logical block can acquire a new current physical embodiment while the old embodiment is marked `deleted` or otherwise noncurrent and remains physically present until later reclamation.

Case 44 reaches the same boundary at a later host/controller interface from another direction. NVMe Deallocate is advisory, and the standard permits a deallocated logical block read to return the last data written under one allowed behavior. Deallocation therefore cannot be treated as proof that the old media state is gone.

Case 84 adds a zoned-storage version: Reset Zone changes the zone-control state, rewinds the write frontier, and marks the logical blocks deallocated for reuse, while the specification does not identify that transition with Sanitize or promise that every lower-layer physical trace has disappeared.

So:

> **logical no-longer-current / no-longer-allocated ≠ physical erasure.**

This is a historical/engineering boundary grounded independently in mapped Flash and later standardized interfaces; it is not merely a forensic slogan imported after the fact.

---

## 5. Physical erase can occur without logical forgetting

The converse is equally important and is easiest to see in Case 04.

During reclamation, still-current values may be copied out of an erase unit, the old unit physically erased, and the logical mapping retained or updated so future access resolves to the replacement embodiment. The old physical token disappears precisely so that the higher-level logical object can continue.

Therefore:

> **destruction of one physical embodiment ≠ destruction of the retained logical identity.**

Physical erase can be retention maintenance.

This blocks an overly material equation in which every destroyed substrate witness automatically counts as forgetting at every layer. The target must be named: cell state, physical embodiment, logical value, logical identity, or service relation.

---

## 6. Physical erase is not automatically sanitization

NVMe 1.3 provides an unusually explicit counterexample because the same standard names three sanitize actions:

- Block Erase;
- Crypto Erase;
- Overwrite.

If the higher-level objective were identical to one physical act, three different mechanism classes would be unnecessary. Crypto Erase can satisfy the intended accessibility transition by changing key state while ciphertext remains on the medium; Overwrite changes stored patterns; Block Erase invokes a media-specific erase operation.

Therefore:

```text
sanitize objective
    !=
one universal substrate operation
```

and specifically:

```text
Block Erase != Crypto Erase != Overwrite
```

The mechanisms can be compared because one interface assigns them related sanitization work, not because their material consequences are identical.

This also limits the phrase `secure erase`. A secure-erasure or sanitization contract is a claim about a target scope and post-operation accessibility/security condition. Whether a particular implementation actually fulfills it is a separate evidence problem.

---

## 7. Overwrite is not a universal substitute for physical erase

Case 47 makes the overwrite problem concrete for SSDs with FTL indirection.

A host can overwrite the visible LBA range while stale physical pages, over-provisioned regions, remapped locations, or old embodiments remain outside direct host enumeration. Wei et al.'s 2011 tests found whole-drive overwrite often effective in their bounded sample but not uniformly reliable, and their tested single-file overwrite protocols consistently failed to remove all target data from raw flash.

The correct conclusion is deliberately narrower than `overwrite never sanitizes SSDs`:

> **host-visible overwrite coverage ≠ guaranteed physical-remnant coverage on an FTL-managed SSD.**

Case 44's earlier ATA Enhanced Security Erase prior-art boundary supplies the converse design lesson: a device-internal operation can be specified to reach reallocated user-data sectors that ordinary host-addressed overwriting may not reach. Interface location and scope matter.

So the roadmap item `overwrite` cannot be closed by one slogan. At least three questions have to stay separate:

1. what logical range did the host address?;
2. what physical embodiments can the controller reach?;
3. what post-operation evidence establishes that the intended target scope was actually transformed?

---

## 8. Erase verification is not the same thing as forensic verification

Case 13's Intel Flash evidence already contains erase verification: after a collective erase pulse, the controller walks addresses and tests whether cells satisfy the device's required erased condition, retrying or signaling failure as necessary.

That is **operational erase verification** inside a device algorithm.

Case 47 asks a different question. The researchers bypass the SSD controller, read raw flash with custom hardware, and search for structured fingerprints. Their test is **independent lower-layer digital-remnant verification**.

These two verification regimes should not be conflated:

```text
internal erase-verify pass
    !=
independent sanitization verification
```

The first establishes that the device's state-transition criterion has been met under the device algorithm. The second challenges a broader claim about surviving old data outside normal logical visibility.

FAST '11 also explicitly leaves **analog sanitization / analog remanence after a correctly executed erase** outside its experimental result. Therefore absence of recoverable digital fingerprints in that study would not, by itself, prove the absence of every possible analog physical witness.

This produces another necessary boundary:

> **verified digital sanitization ≠ proof of zero analog remanence under every measurement model.**

---

## 9. Command success, operation completion, and verified forgetting are separate states

Case 44 shows that NVMe Sanitize command completion starts a background sanitize operation; the operation has separate progress and completion state. That already gives:

```text
request accepted
    !=
sanitation operation complete
```

Case 47 adds a stronger empirical counterexample. In the bounded FAST '11 sample, anonymized Drive B reported successful sanitization while all data remained intact and the filesystem remained mountable.

Hence:

```text
reported success
    !=
verified forgetting
```

The two cases operate at different historical layers and dates. They are not evidence that NVMe inherited the specific bugs of the FAST '11 ATA devices. Together they establish only a cross-case evidentiary rule:

> an interface-defined completion condition and independent evidence of implementation compliance are different claim classes.

This is particularly important in a repository about retention because forgetting operations often destroy the very payload that would otherwise serve as evidence. Systems therefore retain status, completion, keys, counters, or verification results while trying to eliminate another state class.

---

## 10. Forgetting can require retaining control state

The apparent paradox resolves once state classes are separated.

- Case 13 retains command, timing, retry, and verify state long enough to orchestrate coarse erase.
- Case 44 retains sanitize progress/status so the host can distinguish started, in-progress, failed, and completed operations.
- Case 84 retains zone state and a write pointer so later reuse is governed correctly after reset.

Therefore:

> **forgetting payload does not imply forgetting the control evidence that makes forgetting safe or knowable.**

This is an engineering reconstruction, not a historical claim that the cited standards or designers formulated a theory of second-order memory.

---

## 11. Reclamation is not sanitization

Mapped Flash gives a final anti-collapse rule.

Garbage collection / reclamation is primarily about recovering reusable erase units while preserving current logical state. A reclamation erase may incidentally destroy stale physical embodiments, but its correctness target is not necessarily the same as a sanitization contract covering every location that may contain prior user data.

NVMe Sanitize makes the stronger scope explicit by including caches and unallocated/deallocated media locations able to contain user data in the bounded 1.3 contract.

Thus:

```text
reclamation closure
    !=
sanitation closure
```

and:

```text
free again
    !=
proven forgotten under a security target
```

This also prevents Case 04's garbage-collection/reclamation machinery from being silently rewritten as secure deletion.

---

## 12. Cross-case comparison table

| Regime | What changes | What can survive | What proves completion in the bounded source? | What must not be inferred |
| --- | --- | --- | --- | --- |
| Case 11 EPROM | floating-gate charge is deliberately discharged by radiation | unrelated control/interpretive state; exact production 1702 details remain outside patent proof | bounded physical mechanism disclosure, not a modern sanitize status | `nonvolatile = immutable`; `program = erase` |
| Case 12 EEPROM | selected byte or whole chip is electrically erased under special conditions | other bytes under byte erase; finite wear history | product-defined timed/mode operation | `electrical erase = ordinary overwrite`; `erase = unlimited mutability` |
| Case 13 early Flash | shared/coarse domain is electrically erased | copied/preserved state outside the erase event; controller transient state | device erase-verify loop | `coarse erase = coarse read/program`; `verify = forensic audit` |
| Case 04 mapped Flash | old embodiment invalidated, later erase unit reclaimed | stale old embodiment before reclamation; logical identity across relocation | mapping/currentness + successful reclamation path | `deleted = physically gone`; `erased embodiment = lost logical object` |
| Case 44 NVMe | deallocation or subsystem sanitize transition | deallocated prior data may remain under allowed semantics; ciphertext under crypto erase | sanitize-operation status for interface contract | `Deallocate = Sanitize`; `Sanitize = one physical erase mechanism` |
| Case 47 FAST '11 | empirical sanitization/overwrite tested below controller | raw-flash digital remnants can survive ordinary logical disappearance or failed command implementations | raw-flash fingerprint search in bounded experiment | `reported success = verified sanitization`; `digital test = analog-remanence proof` |
| Case 84 ZNS | zone state/write frontier reset; logical blocks deallocated for reuse | unspecified lower-layer prior physical state | successful zone-management transition at interface | `Reset Zone = NAND block erase`; `Empty = sanitized` |

---

## 13. Functional analogies that are allowed

The following comparisons are useful **functional analogies**, not genealogical claims:

- UV EPROM erasure and Flash block erase both show that forgetting can have a geometry different from ordinary read selection;
- Flash reclamation and distributed replica retirement both show that destruction of one embodiment can preserve a higher-level identity, but their mechanisms and authority models differ;
- NVMe Crypto Erase and loss of an interpretation/key relation both show that physical payload survival can coexist with operational inaccessibility, but cryptographic key destruction has a specific security mechanism and threat model;
- SSD sanitize status and distributed maintenance-progress metadata both retain evidence about unfinished work, but they are not one historical system family.

No arrow of historical descent is asserted by these comparisons.

---

## 14. Philosophical limit

The technical record permits a narrow philosophical interpretation:

> forgetting in technical systems is not simply the inverse of storage. It is an achieved relation whose target, authority, scope, material operation, and evidence can differ.

But that sentence remains an interpretation. Intel, Toshiba, M-Systems, NVM Express, and the FAST '11 authors are evidence for concrete mechanisms and interface claims, not for a shared philosophy of forgetting.

A stronger philosophical claim — for example that all technical erasure is a form of selective disclosure, exteriorization, or temporal politics — would require separate argument and cannot be smuggled out of erase-command semantics.

---

## 15. Roadmap result and remaining gaps

This synthesis is enough to mark **physical erase as substantially advanced at the floating-gate / Flash / SSD layers**, while leaving the Phase-4 umbrella open.

The following work remains genuinely distinct:

- magnetic overwrite, degaussing, and remanence under period and modern recording systems;
- optical and phase-change physical erase/rewrite regimes;
- direct analog-remanence work after a correctly completed semiconductor erase;
- named contemporary SSD/controller conformance across Block Erase, Crypto Erase, and Overwrite;
- sanitization under damaged metadata, inaccessible spare areas, key-store failure, and interrupted firmware recovery;
- filesystem/application overwrite semantics under copy-on-write, snapshots, deduplication, and replication;
- secure-destruction standards and threat models beyond the bounded ATA/NVMe/TCG witnesses already in Case 44.

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) surfaced no dedicated Flash-erase / SSD-sanitization history to reuse in this slice. Broader EPROM→EEPROM→Flash device history, controller implementation history, magnetic/optical erase genealogy, and material engineering should be developed there rather than duplicated here.

---

## Compact result

The cross-case result is:

```text
not current
    !=
not allocated
    !=
physically erased
    !=
reclaimed for reuse
    !=
sanitation objective satisfied
    !=
independently verified forgotten
```

and, in the opposite direction:

```text
physical embodiment destroyed
    !=
logical identity forgotten
```

The useful object of study is therefore not `erase` as one verb, but the chain of relations by which a system decides **what no longer counts, what has materially changed, what may be reused, what must be inaccessible, and what evidence is sufficient to trust that transition**.
'''


def write_synthesis():
    if SYNTHESIS_PATH.exists():
        current = SYNTHESIS_PATH.read_text(encoding='utf-8')
        if current != SYNTHESIS:
            raise SystemExit('Synthesis 22 already exists with unexpected content')
    else:
        SYNTHESIS_PATH.write_text(SYNTHESIS, encoding='utf-8')


def update_readme():
    p = Path('README.md')
    text = p.read_text(encoding='utf-8')
    marker = 'A bounded erase/invalidation/sanitization comparison is now available in [`docs/SYNTHESIS_22_ERASE_INVALIDATION_SANITIZATION_VERIFICATION.md`](docs/SYNTHESIS_22_ERASE_INVALIDATION_SANITIZATION_VERIFICATION.md).'
    if marker in text:
        return
    anchor = 'This chain is a **research heuristic**, not a claim that all of these mechanisms are historically or philosophically identical.'
    if text.count(anchor) != 1:
        raise SystemExit(f'expected one README synthesis-chain anchor, found {text.count(anchor)}')
    para = (
        'A bounded erase/invalidation/sanitization comparison is now available in '
        '[`docs/SYNTHESIS_22_ERASE_INVALIDATION_SANITIZATION_VERIFICATION.md`]'
        '(docs/SYNTHESIS_22_ERASE_INVALIDATION_SANITIZATION_VERIFICATION.md). '
        'Across grounded EPROM/EEPROM/early-Flash, mapped-Flash, NVMe, ZNS, and FAST ’11 SSD evidence it separates logical invalidation, physical medium erase, reclamation/reuse, sanitization objective, operation-completion state, and independent verification. '
        'It fixes the counterexamples `logical deletion ≠ physical erase`, `physical erase of one embodiment ≠ logical forgetting`, `reclamation ≠ sanitization`, `Block Erase ≠ Crypto Erase ≠ Overwrite`, `reported success ≠ verified forgetting`, and `digital-remnant verification ≠ proof of zero analog remanence`.'
    )
    text = text.replace(anchor, para + '\n\n' + anchor, 1)
    p.write_text(text, encoding='utf-8')


def update_roadmap():
    p = Path('ROADMAP.md')
    lines = p.read_text(encoding='utf-8').splitlines()
    replacements = {
        '- [ ] overwrite;': '- [ ] overwrite — **partially advanced at the SSD/interface sanitization layer by grounded Cases 44 and 47 plus Synthesis 22**: NVMe separates Overwrite from Block Erase and Crypto Erase, while FAST ’11 shows that host-visible overwrite coverage can miss stale FTL-managed physical embodiments. Filesystem/application overwrite under copy-on-write, snapshots, deduplication, replication, magnetic overwrite, named contemporary device conformance, and broader overwrite genealogy remain open;',
        '- [ ] physical erase;': '- [ ] physical erase — **substantially advanced at the floating-gate / Flash / SSD layers by grounded Cases 11–13, 04, 44, and 47 plus Synthesis 22**: the repository now separates radiation/electrical cell-state erasure, erase geometry, logical invalidation before erase, reclamation erase that preserves logical identity, NVMe Block Erase from Crypto Erase/Overwrite, and interface completion from independent raw-flash verification. Magnetic/optical/phase-change erase, analog remanence after a correctly completed erase, named contemporary controller conformance, damaged-metadata/key-store cases, and broader physical-erasure genealogy remain open;',
    }
    found = {k: 0 for k in replacements}
    logical_found = 0
    for i, line in enumerate(lines):
        if line in replacements:
            found[line] += 1
            lines[i] = replacements[line]
        if line.startswith('- [ ] logical deletion / invalidation —'):
            logical_found += 1
            lines[i] = '- [ ] logical deletion / invalidation — **partially advanced by grounded Cases 04, 41, 44, 73, 74, and 84 plus Synthesis 22**: mapped Flash grounds logical invalidation before later physical erase; Cassandra/GFS/JBD retain negative or retirement evidence across reclamation/replay boundaries; NVMe Deallocate remains weaker than Sanitize; and ZNS Reset Zone returns logical blocks to a deallocated/reusable state without proving physical sanitization. Database/object lifecycle, filesystem unlink semantics beyond the bounded cases, key-destruction, provider deletion contracts, and broader secure-erasure genealogies remain open;'
    for old, count in found.items():
        if count != 1 and replacements[old] not in lines:
            raise SystemExit(f'expected one ROADMAP line {old!r}, found {count}')
    if logical_found != 1 and not any('Cases 04, 41, 44, 73, 74, and 84 plus Synthesis 22' in x for x in lines):
        raise SystemExit(f'expected one logical-deletion roadmap line, found {logical_found}')
    p.write_text('\n'.join(lines).rstrip() + '\n', encoding='utf-8')


def update_case_index():
    p = Path('CASE_INDEX.md')
    text = p.read_text(encoding='utf-8').rstrip()
    if '**2297 — logical invalidation ≠ physical erase:**' in text:
        return
    nums = [int(x) for x in re.findall(r'^- \*\*(\d+) —', text, flags=re.M)]
    if not nums or max(nums) != 2296:
        raise SystemExit(f'expected current max finding 2296, got {max(nums) if nums else None}')
    addition = r'''

## Synthesis 22 findings — erase, invalidation, sanitization, and verification

- **2297 — logical invalidation ≠ physical erase:** a logical embodiment can cease to count as current or allocated while lower-layer state still survives; mapped Flash, NVMe Deallocate, and ZNS Reset Zone ground different versions of this boundary. (`H/P`, `E`)
- **2298 — logical invalidation can precede physical erasure:** Case 04's old embodiment can be marked deleted/noncurrent before later erase-unit reclamation, so the currentness transition and substrate transition have different times. (`H/P`, `E`)
- **2299 — physical erasure of one embodiment ≠ logical forgetting:** copy-current → erase-old → remap can destroy an old physical token while preserving the logical identity through another current embodiment. (`H/P`, `E`)
- **2300 — erase domain ≠ logical-object boundary:** EPROM/EEPROM/early-Flash evidence shows that erase authority can be device-wide, byte-selectable, chip-wide, shared, or coarse relative to read/program addressing. (`H/P`, `E`)
- **2301 — electrical erasability ≠ ordinary overwrite:** Intel 2816 electrical erase remains a special voltage/timing/mode operation with finite cycling and erase-before-write semantics. (`H/P`, `X`)
- **2302 — Block Erase ≠ Crypto Erase ≠ Overwrite:** NVMe 1.3 assigns these as distinct sanitize mechanisms; a shared sanitization objective does not make their physical state transformations identical. (`H/P`, `E`)
- **2303 — sanitization objective ≠ one universal physical erase act:** cryptographic key destruction or overwrite can satisfy a higher-level sanitization relation without being the same substrate mechanism as Block Erase. (`H/P`, `E`)
- **2304 — deallocation/reset-for-reuse ≠ sanitization:** NVMe Deallocate and ZNS Reset Zone can withdraw logical allocation/currentness and enable reuse without thereby proving that prior physical media state has been sanitized. (`H/P`, `E`)
- **2305 — sanitize command completion ≠ sanitize-operation completion:** NVMe 1.3 keeps background operation progress/completion separate from the command that starts the operation. (`H/P`)
- **2306 — interface completion contract ≠ independent compliance evidence:** a specification can define successful operation completion without independently establishing that every named implementation correctly fulfills the contract. (`E`, `X`)
- **2307 — reported erase success ≠ verified digital sanitization:** FAST ’11 Drive B reported successful sanitization while raw-flash testing found all data intact, directly grounding the need to separate controller report from measured result. (`H/P`)
- **2308 — ordinary-interface inaccessibility ≠ lower-layer witness absence:** FTL remapping and hidden physical capacity can leave digital remnants outside current LBA visibility. (`H/P`, `E`)
- **2309 — digital-remnant verification ≠ proof of zero analog remanence:** FAST ’11 verifies bounded digital remnants and explicitly leaves analog sanitization outside the experiment, so stronger physical claims remain unsupported. (`H/P`, `X`)
- **2310 — reclamation closure ≠ sanitization closure:** reclaiming an erase unit safely for future writes is a different correctness target from making prior user data inaccessible across a sanitization scope. (`E`, `A`)
- **2311 — internal erase verification ≠ forensic verification:** early Flash address-walking erase-verify checks the device's operational erase criterion, while FAST ’11 bypasses the controller to search raw flash for old fingerprints. (`H/P`, `E`)
- **2312 — forgetting payload can require retained control evidence:** command/verify state, sanitize progress/status, and zone state/write-frontier metadata can remain necessary while another state class is being deliberately retired. (`H/P`, `E`)
- **2313 — EPROM→EEPROM→Flash comparison ≠ inevitable linear genealogy:** the bounded cases support comparison of erase control and geometry, not a claim that every cited mechanism or actor belongs to one teleological invention chain. (`A`, `X`)
- **2314 — related-repository boundary:** a fresh `tmzncty/computing-archaeology` search surfaced no dedicated Flash-erase / SSD-sanitization case to reuse; broader device/material erase history and cross-media genealogy belong there, while this synthesis remains a retention-specific cross-case comparison. (`H/P` project-state record)
'''
    p.write_text(text + addition + '\n', encoding='utf-8')


write_synthesis()
update_readme()
update_roadmap()
update_case_index()

# Canonical invariants for this bounded integration.
assert SYNTHESIS_PATH.exists()
assert 'SYNTHESIS_22_ERASE_INVALIDATION_SANITIZATION_VERIFICATION.md' in Path('README.md').read_text(encoding='utf-8')
roadmap = Path('ROADMAP.md').read_text(encoding='utf-8')
assert 'physical erase — **substantially advanced at the floating-gate / Flash / SSD layers' in roadmap
assert 'overwrite — **partially advanced at the SSD/interface sanitization layer' in roadmap
index = Path('CASE_INDEX.md').read_text(encoding='utf-8')
for n in range(2297, 2315):
    assert f'**{n} —' in index
