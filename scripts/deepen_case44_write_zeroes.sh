#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
git pull --ff-only origin main

python3 - <<'PY'
from pathlib import Path
import re

case = Path('cases/44-nvme13-deallocate-sanitize-forgetting.md')
evidence = Path('evidence/44-nvme-2011-2017-write-zeroes-value-semantics-deepening.md')
index = Path('CASE_INDEX.md')
roadmap = Path('ROADMAP.md')

for p in [case, index, roadmap, Path('AGENTS.md'), Path('docs/METHOD.md'), Path('docs/PRIOR_ART.md'), Path('docs/TECHNICAL_SPINE.md'), Path('RELATED_REPOS.md')]:
    if not p.exists():
        raise SystemExit(f'missing prerequisite: {p}')
if evidence.exists():
    raise SystemExit(f'refusing to overwrite existing evidence file: {evidence}')

evidence_text = r'''# Case 44 Deepening — NVMe Write Zeroes, Deallocation, and Logical-Value Semantics (2011–2017)

## Purpose

This record deepens [`../cases/44-nvme13-deallocate-sanitize-forgetting.md`](../cases/44-nvme13-deallocate-sanitize-forgetting.md) around one bounded interface question:

> when an NVMe host wants a range to read as zero, how is that relation different from saying that the range is deallocated, and how are both different from sanitizing prior user data?

The existing Case 44 already grounds `Deallocate` and `Sanitize`. This addendum does **not** create a second generic erase case. It reconstructs the intervening `Write Zeroes` branch from official NVM Express 1.0, 1.1, and 1.3 material and uses it to keep three relations distinct:

```text
allocation/currentness state
    !=
future logical read-value contract
    !=
media-sanitization / prior-data-unrecoverability contract
```

Claim labels used below follow repository policy: **Historical record**, **Engineering reconstruction**, **Functional analogy**, and **Philosophical interpretation** are kept separate.

## Sources inspected

### NVM Express Revision 1.0 — March 1, 2011

Official NVM Express PDF:

- <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_0-Gold.pdf>

Directly inspected:

- front matter: Revision 1.0, dated and ratified **March 1, 2011**;
- §6 / Figure 98, `Opcodes for NVM Commands`, printed p. 87 / PDF page 86.

Figure 98 lists `Flush`, `Write`, `Read`, `Write Uncorrectable`, `Compare`, and `Dataset Management` as the standard NVM commands in that revision and states that opcodes not listed are reserved. `Write Zeroes` is not present in that command table.

**Historical-record boundary:** this establishes that the inspected NVMe 1.0 command set did not yet contain the later standardized `Write Zeroes` command. It does not establish that zero-fill operations, controller-side zero generation, or analogous commands were invented by NVMe 1.1.

### NVM Express Revision 1.1 — October 11, 2012

Official NVM Express PDF:

- <https://www.nvmexpress.org/wp-content/uploads/NVM-Express-1_1.pdf>

Directly inspected:

- front matter: Revision 1.1, **October 11, 2012**;
- Identify Controller `Optional NVM Command Support (ONCS)`, printed p. 86 / PDF page 85;
- §6 / Figure 121, NVM command opcodes, printed p. 110 / PDF page 109;
- §6.6.1.1 `Deallocate`, printed p. 117 / PDF page 116;
- §6.15 `Write Zeroes command`, printed p. 129 / PDF page 128.

The ONCS field makes `Write Zeroes` optional in Revision 1.1: bit 3 indicates whether the controller supports it. Figure 121 separately lists opcode `08h` as optional `Write Zeroes` and opcode `09h` as optional `Dataset Management`.

### NVM Express Revision 1.3 — May 1, 2017; ratified April 26, 2017

Official NVM Express PDF:

- <https://nvmexpress.org/wp-content/uploads/NVM_Express_Revision_1.3.pdf>

Official NVM Express revision-change summary:

- <https://nvmexpress.org/changes-in-nvme-revision-1-3/>

Directly inspected:

- Revision 1.3 front matter for date / ratification;
- §6.16 `Write Zeroes`, printed pp. 198–199 / PDF pages 197–198;
- the revision-change entry `Deallocated Value for Logical Block Data`, which points to Technical Proposal 019 and says Revision 1.3 added a mechanism for determining values returned for deallocated logical blocks and a mechanism for requesting deallocation as part of `Write Zeroes`.

The Technical Proposal itself is member-workspace material in the cited NVM Express page and was not used as if independently inspected here.

## Historical record — Revision 1.1 creates a value-setting path distinct from deallocation

Revision 1.1 §6.6.1.1 says that a deallocated LBA returns a deterministic value until another write, but that value may be:

- all zeroes;
- all ones; or
- the last data written to the LBA.

The same section explicitly compares NVMe Deallocate to ATA Data Set Management with Trim and SCSI UNMAP. It does not promise that deallocation alone establishes a zero-valued logical block.

Revision 1.1 §6.15 gives `Write Zeroes` a different contract: after successful completion, subsequent reads of the specified logical blocks **shall return zeroes until another write occurs**.

Therefore, within one dated specification:

> **deallocated != guaranteed-zero-on-read**.

And conversely:

> **guaranteed-zero-on-read != necessarily deallocated**.

The two operations answer different interface questions even though an implementation may later combine them.

## Historical record — Write Zeroes is optional in Revision 1.1

The Identify Controller `ONCS` field in Revision 1.1 assigns one capability bit to `Write Zeroes` and another to Dataset Management. A controller may therefore support one, both, or neither optional command under the bounded Revision-1.1 contract.

This blocks a common retrospective collapse:

> **NVMe 1.1 support != universal Write Zeroes support on every Revision-1.1 controller**.

It also supplies a clean interface-level separation between the command vocabulary and a particular product's implementation.

## Historical record — Force Unit Access strengthens persistence, not sanitization

Revision 1.1 `Write Zeroes` includes an `FUA` bit. When set, the specification says the data shall be written to non-volatile media before command completion and explicitly says that this creates no implied ordering with other commands.

The bounded conclusion is:

> **FUA-qualified Write Zeroes completion != sanitize completion**.

FUA strengthens the persistence boundary for the resulting write operation. It does not say that every previous physical embodiment, remapped location, cache residue outside the bounded write path, or forensic trace has been erased or made unrecoverable.

That distinction is especially important because Case 44 already grounds a much broader `Sanitize` target: locations in the subsystem capable of containing user data, including deallocated areas and caches under the Revision-1.3 contract.

## Historical record — Revision 1.3 can combine zero-read semantics with deallocation

Revision 1.3 §6.16 retains the `Write Zeroes` logical contract: successful completion makes subsequent reads return `00h` until another write.

It also adds the `DEAC` bit and conditions its behavior on the namespace's deallocated-read feature. Where the namespace supports zero-valued reads from deallocated logical blocks, a `Write Zeroes` command may produce its required zero-read result while deallocating the affected logical blocks. If the namespace cannot provide zero-valued deallocated reads, the controller shall not deallocate logical blocks in the range as part of that `Write Zeroes` operation.

The NVM Express Revision-1.3 changes page describes this explicitly as a change to deallocated-value behavior and as adding a host mechanism to request deallocation as part of `Write Zeroes`.

This produces a useful interface counterexample:

```text
same host-visible zero result
    can coexist with
allocated/write-zero state
    or
zero-reading deallocated state
```

The visible value contract therefore does not uniquely identify the allocation state underneath it.

## Engineering reconstruction — value, allocation, embodiment, and sanitization are separate axes

The standards evidence supports a four-axis reconstruction:

1. **logical value contract** — what a later read is required to return;
2. **allocation/deallocation relation** — whether the LBA is treated as deallocated;
3. **persistence boundary** — whether the command completion includes nonvolatile-media completion under `FUA`;
4. **prior-embodiment sanitization** — whether previous user data is required to be unrecoverable across the sanitize scope.

A single word such as `zeroed`, `trimmed`, `erased`, or `forgotten` cannot safely stand in for all four.

The most important counterexample is:

> **zero returned by future reads != proof that old physical embodiments have been sanitized**.

That conclusion is not a claim about one hidden NAND implementation. It follows from the interface contracts themselves: `Write Zeroes` specifies a later logical value, while `Sanitize` separately defines a stronger prior-data-unrecoverability objective over a broader subsystem scope.

## Engineering reconstruction — one visible value can have multiple admissible lower-layer realizations

Revision 1.3 makes the distinction unusually explicit because `Write Zeroes` can either write zero-valued data or use deallocation when the namespace guarantees zero-valued reads from deallocated blocks.

Thus:

> **logical zero is not a unique physical-state description**.

A future read returning `00h` establishes an interface-visible value relation. It does not, by itself, tell an observer whether the controller retained programmed zero data, changed mapping/allocation metadata, reclaimed media, or used another compliant embodiment.

This is a bounded reconstruction of the interface relation, not a claim that every controller uses FTL mapping or one specific zero optimization.

## Functional analogy — negative state and zero value must not be conflated

At a functional level only, this result resembles other repository cases in which a negative or retirement relation is not equivalent to one payload value. JFFS2 Case 145 distinguishes an explicit `JFFS2_COMPR_ZERO` node from mere absence/obsolescence; distributed cases distinguish tombstones or retired references from physical disappearance.

The analogy stops at the relation:

> **absence/retirement metadata and a positive value representation answer different questions**.

There is no claim of shared implementation, genealogy, or historical vocabulary between NVMe and those systems.

## Philosophical interpretation — replacement is not the same operation as forgetting

The technical fact that creates the conceptual problem is simple: a range may become observably zero without the interface claiming that every previous embodiment is unrecoverable, while a sanitize operation explicitly targets prior-data recovery.

A narrow philosophical interpretation is therefore:

> **making a new present value authoritative is not identical to eliminating every technical condition under which an older state might survive.**

This is an interpretation of the engineering distinction, not language attributed to NVM Express designers.

## Prior-art and anti-anachronism boundaries

This deepening makes only a narrow version-history claim:

- NVMe 1.0's inspected NVM command table lacks `Write Zeroes`;
- NVMe 1.1 explicitly contains optional `Write Zeroes` and its zero-read contract;
- NVMe 1.3 later couples `Write Zeroes` to optional deallocation semantics under defined namespace behavior.

It does **not** claim:

- that NVMe 1.1 invented zero-fill or controller-generated zeroing;
- that NVMe invented deallocation, which Revision 1.1 itself compares with ATA Trim and SCSI UNMAP;
- that `Write Zeroes` causes physical NAND programming in every implementation;
- that `FUA` implies media sanitization, whole-device durability ordering, or removal of stale remapped embodiments;
- that a zero-valued deallocated read proves physical erasure;
- that TP019's drafting chronology has been independently reconstructed from member-only proposal material;
- that one interface revision implies immediate implementation in every shipping SSD.

Broader zeroing/deallocation command genealogy, product adoption, controller optimizations, and device-level forensic validation belong primarily in `tmzncty/computing-archaeology` or in a future named-product validation slice rather than being inferred here.

## Resulting bounded distinctions

This addendum grounds the following reusable distinctions for Case 44:

```text
NVMe 1.0 command set
    !=
NVMe 1.1 optional Write Zeroes

Deallocate
    !=
Write Zeroes
    !=
Sanitize

deallocated
    !=
guaranteed-zero-on-read

guaranteed-zero-on-read
    !=
deallocated

logical zero
    !=
unique physical embodiment

FUA-qualified command completion
    !=
sanitation / prior-data-unrecoverability proof

zero-valued future read
    !=
proof of physical erase
    !=
proof of sanitization

Revision-1.3 DEAC coupling
    !=
collapse of value semantics and allocation semantics
```

## Open work deliberately left outside this slice

- exact proposal/ballot history between NVMe 1.0 and 1.1 for `Write Zeroes`;
- public TP019 drafting history beyond the NVM Express change summary;
- ATA `WRITE SAME` / SCSI `WRITE SAME`, UNMAP, and zeroing genealogy;
- named-controller / named-SSD implementation behavior for zero-write optimization;
- tracing of physical NAND behavior under `Write Zeroes` with and without `DEAC`;
- crash/power-cut experiments around FUA and controller caches;
- forensic comparison of logical zeroing, deallocation, secure erase, and Sanitize on named devices.

Those are separate technical-history or validation tasks, not prerequisites for the bounded interface distinction established here.
'''
evidence.write_text(evidence_text, encoding='utf-8')

# Add the deepening record and a bounded section to Case 44.
s = case.read_text(encoding='utf-8')
ground = 'Grounding record: [`../evidence/44-nvme12-13-deallocate-sanitize-grounding.md`](../evidence/44-nvme12-13-deallocate-sanitize-grounding.md).'
deep = 'Deepening record: [`../evidence/44-nvme-2011-2017-write-zeroes-value-semantics-deepening.md`](../evidence/44-nvme-2011-2017-write-zeroes-value-semantics-deepening.md).'
if deep not in s:
    if ground not in s:
        raise SystemExit('Case44 grounding-record anchor missing')
    s = s.replace(ground, ground + '\n\n' + deep, 1)

section_heading = '## Intervening semantic branch — NVMe 1.1 Write Zeroes separates value replacement from deallocation'
if section_heading not in s:
    anchor = '## Mechanism 2 — Sanitization scopes beyond the currently allocated LBA set'
    if anchor not in s:
        raise SystemExit('Case44 mechanism-2 anchor missing')
    section = r'''## Intervening semantic branch — NVMe 1.1 Write Zeroes separates value replacement from deallocation

A bounded look one revision earlier sharpens the deallocation argument. NVM Express 1.0 (March 1, 2011) lists its standard NVM commands without `Write Zeroes`; NVM Express 1.1 (October 11, 2012) adds optional `Write Zeroes` support, exposed independently from Dataset Management in the `ONCS` capability field.

Revision 1.1 already gives the two operations different visible contracts. A deallocated LBA may read as all zeroes, all ones, or the last data written. `Write Zeroes`, by contrast, requires subsequent reads of the affected range to return zero until another write occurs.

Therefore:

> **deallocated != guaranteed-zero-on-read**

and:

> **guaranteed-zero-on-read != necessarily deallocated**.

This matters for retention because a new logical value can become authoritative without establishing that an earlier physical embodiment has been sanitized. `Write Zeroes` also includes `FUA`; when set, command completion requires the resulting write to have reached nonvolatile media, but that is a persistence boundary for the new operation, not a subsystem-wide prior-data-unrecoverability guarantee.

Revision 1.3 then makes the separation more explicit by adding `DEAC` behavior to `Write Zeroes`. Where a namespace can guarantee zero-valued reads from deallocated LBAs, a `Write Zeroes` command may satisfy its zero-read contract while deallocating the range. Where that zero-read property is unavailable, the controller must not use deallocation for the `Write Zeroes` range. NVM Express's own Revision-1.3 change summary identifies this as a deallocated-value / Write-Zeroes change associated with TP019.

The resulting engineering reconstruction is:

```text
logical read-value contract
    !=
allocation/deallocation state
    !=
physical embodiment
    !=
sanitation state
```

So **zero-valued future reads do not prove physical erase or sanitization**. Conversely, deallocation does not, by itself, promise the zero-valued result that `Write Zeroes` does. Revision 1.3 can couple the two relations in one command without making them conceptually identical.

This addendum makes no invention claim for zero-fill operations or deallocation and no device-internal claim about how a particular SSD realizes zeroes. Exact proposal chronology, ATA/SCSI genealogy, named-product implementation, and physical-NAND validation remain separate work, primarily for `computing-archaeology` or a future validation case.

'''
    s = s.replace(anchor, section + anchor, 1)
case.write_text(s, encoding='utf-8')

# Add numbered findings immediately before the comparison matrix. Number from the current ledger maximum.
s = index.read_text(encoding='utf-8')
marker = '## Comparison matrix — provisional\n'
if marker not in s:
    raise SystemExit('CASE_INDEX comparison-matrix marker missing')
route = 'Case 44 Write Zeroes value-semantics deepening'
if route not in s:
    nums = [int(m.group(1)) for m in re.finditer(r'(?m)^(\d+)\.\s', s)]
    if not nums:
        raise SystemExit('CASE_INDEX contains no numbered findings')
    n = max(nums) + 1
    findings = [
        'NVM Express 1.0 (1-Mar-2011) lists its standard NVM command set without `Write Zeroes`; unlisted opcodes are reserved, so the inspected 1.0 interface predates the later standardized command without implying invention priority for zero-fill operations.',
        'NVM Express 1.1 (11-Oct-2012) exposes `Write Zeroes` as an optional command through a distinct ONCS capability bit; interface support therefore does not imply universal controller implementation.',
        'Revision-1.1 Deallocate permits deterministic reads returning all zeroes, all ones, or the last data written, while Revision-1.1 Write Zeroes requires subsequent reads to return zero until another write.',
        '`deallocated != guaranteed-zero-on-read` and `guaranteed-zero-on-read != necessarily deallocated`; allocation state and logical value contract are separate interface relations.',
        'Revision-1.1 Write Zeroes `FUA` requires the resulting data to reach nonvolatile media before completion when asserted, but that persistence boundary does not establish sanitization of previous embodiments.',
        'Revision-1.3 Write Zeroes adds `DEAC` behavior conditioned on the namespace ability to return zeroes for deallocated logical blocks; zero-read semantics can therefore coexist with a deallocated state.',
        'Revision-1.3 forbids using deallocation for Write Zeroes when the namespace cannot provide the required zero-valued deallocated reads, proving that deallocation is an implementation/admission path under a stronger visible value contract rather than the value contract itself.',
        'A later read of zero does not uniquely identify the lower-layer realization: compliant interface semantics permit value replacement and, under defined conditions, zero-reading deallocation.',
        '`zero-valued future read != proof of physical erase != proof of sanitization`; Case 44 now separates value replacement from allocation retirement and subsystem-wide prior-data-unrecoverability.',
        'The NVM Express Revision-1.3 change summary attributes deallocated-value and Write-Zeroes/deallocation coupling to TP019, but the member-only proposal chronology is not treated as independently inspected evidence.',
        'The direct 1.0→1.1→1.3 revision comparison is a specification-history boundary, not a claim that NVMe invented zeroing, deallocation, TRIM-like semantics, or controller-side optimization.',
        'Cross-case comparisons to JFFS2 explicit zero nodes or distributed negative state are functional only: negative/retirement relations and positive zero-value representations answer different questions and do not imply shared genealogy.'
    ]
    block = '### Case 44 Write Zeroes value-semantics deepening\n\n'
    for i, text in enumerate(findings):
        block += f'{n+i}. {text}\n'
    block += '\n'
    s = s.replace(marker, block + marker, 1)
    index.write_text(s, encoding='utf-8')

# Record the completed bounded deepening in ROADMAP beside Case 44 when possible.
s = roadmap.read_text(encoding='utf-8')
road_line = '- [x] **Case 44 NVMe Write Zeroes / deallocation value-semantics deepening** — [`cases/44-nvme13-deallocate-sanitize-forgetting.md`](cases/44-nvme13-deallocate-sanitize-forgetting.md) + [`evidence/44-nvme-2011-2017-write-zeroes-value-semantics-deepening.md`](evidence/44-nvme-2011-2017-write-zeroes-value-semantics-deepening.md): official NVMe 1.0/1.1/1.3 text now separates deallocation state, guaranteed zero-read semantics, FUA-qualified persistence, physical embodiment, and sanitization. Revision 1.1 makes `Write Zeroes` optional and stronger than Deallocate as a read-value contract; Revision 1.3 can couple zero semantics to deallocation through `DEAC` only where deallocated reads can satisfy the zero contract. This closes the bounded `deallocated != guaranteed-zero`, `logical zero != unique physical embodiment`, and `FUA completion != sanitization` seams without claiming zeroing invention priority, product implementation, or physical NAND erasure. Exact proposal/ballot genealogy, ATA/SCSI zeroing lineage, named-device behavior, and power-cut/forensic validation remain open; broad command genealogy belongs primarily in `computing-archaeology`.'
if '44-nvme-2011-2017-write-zeroes-value-semantics-deepening.md' not in s:
    lines = s.splitlines()
    anchors = [i for i, line in enumerate(lines) if 'cases/44-nvme13-deallocate-sanitize-forgetting.md' in line]
    if anchors:
        lines.insert(anchors[0] + 1, road_line)
    else:
        lines.append(road_line)
    roadmap.write_text('\n'.join(lines) + ('\n' if s.endswith('\n') else ''), encoding='utf-8')

# Integrity checks.
for p in [case, evidence, index, roadmap]:
    if not p.exists() or p.stat().st_size == 0:
        raise SystemExit(f'empty/missing output: {p}')
if '44-nvme-2011-2017-write-zeroes-value-semantics-deepening.md' not in case.read_text(encoding='utf-8'):
    raise SystemExit('Case44 does not link deepening evidence')
if 'Case 44 Write Zeroes value-semantics deepening' not in index.read_text(encoding='utf-8'):
    raise SystemExit('CASE_INDEX findings missing')
if '44-nvme-2011-2017-write-zeroes-value-semantics-deepening.md' not in roadmap.read_text(encoding='utf-8'):
    raise SystemExit('ROADMAP status missing')
PY

rm -f .github/workflows/deepen-case44-write-zeroes.yml scripts/deepen_case44_write_zeroes.sh

git add -A
if git diff --cached --quiet; then
  echo "No changes to commit"
  exit 0
fi
git commit -m "case44: deepen Write Zeroes value-retention semantics"
git push origin main
