#!/usr/bin/env bash
set -euo pipefail

git pull --ff-only origin main

EVIDENCE='evidence/20-nvme-2014-atomic-write-torn-write-deepening.md'
if [[ -e "$EVIDENCE" ]]; then
  echo "refusing to overwrite existing $EVIDENCE" >&2
  exit 1
fi

cat > "$EVIDENCE" <<'EOF'
# Case 20 deepening evidence — NVMe 1.1b torn-write semantics and the atomicity/durability boundary

## Scope

This evidence record deepens Case 20 with a bounded later normative witness: **NVM Express Revision 1.1b, dated 2 July 2014**. Case 20 already establishes from Revision 1.0 that NVMe exposes ordinary command completion, volatile write cache state, Flush, FUA, AWUN, and AWUPF as distinct interface relations. The purpose here is narrower:

> What does the later 1.1b wording let us say precisely about a power-fail-interrupted write, and why is that guarantee not the same as newest-value durability?

This record does **not** claim that NVMe invented atomic writes, torn-write protection, write-ahead recovery, or power-loss protection. It also does not infer a controller's internal FTL journal, capacitor bank, NAND program unit, or firmware commit protocol from an interface guarantee.

---

## Evidence ledger

| Source | Date / status | What it grounds | What it does not ground |
| --- | --- | --- | --- |
| NVM Express, **Revision 1.0 Gold** | ratified 2011-03-01 | the original Case 20 interface boundary: VWC, Flush, FUA, AWUN, AWUPF | a named controller implementation or later wording |
| NVM Express, **Revision 1.1b** | 2014-07-02; official NVM Express archive | explicit AWUN/AWUPF separation; torn-write definition; all-old/all-new failure result within AWUPF; completed-write volatile-cache exception | invention priority; internal implementation mechanism |

Primary facsimiles:

- NVM Express 1.0 Gold: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_0-Gold.pdf>
- NVM Express 1.1b: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_1b-1.pdf>
- NVM Express specification archive: <https://nvmexpress.org/nvm-express-specification-archives/>

---

## Historical record

### H/P — Revision 1.1b is a dated later normative witness, not a new origin claim

The official Revision 1.1b front matter is dated **2 July 2014** and states that Revision 1.1 had been ratified on 11 October 2012. This deepening uses the 1.1b text because it makes the relevant atomic-operation semantics unusually explicit. It does not rewrite the bounded 2011 date of Case 20 and does not turn the 2014 wording into an invention date.

### H/P — AWUN is the normal-operation atomicity envelope, not the power-fail envelope

The Identify Controller definition and §6.4.1 say that **AWUN** controls atomicity in normal operation and explicitly exclude write errors caused by power failure from AWUN's applicability. Section 6.4 describes AWUN primarily as inter-command serialization: within the supported unit, overlapping new writes are not allowed to leave an arbitrary mixture of data from those new commands.

This is stronger evidence than treating `atomic write unit` as one undifferentiated number.

### H/P — AWUPF is a separately reported power-fail/error envelope and cannot exceed AWUN

The Identify Controller definition states that **AWUPF** is the atomic write size during power-fail or error conditions and constrains `AWUPF <= AWUN`. Section 6.4.2 then defines the interrupted-write behavior separately from AWUN.

The historical relation is therefore:

```text
normal-operation write atomicity (AWUN)
        !=
power-fail/error interrupted-write atomicity (AWUPF)
```

### H/P — the specification names and bounds the torn-write failure

Section 6.4 calls AWUPF protection against **torn writes**. The failure it describes is a contiguous multi-block write for which only part of the intended range reaches NVM, leaving a mixture of old and new logical-block contents.

For a write no larger than AWUPF that is interrupted by power failure or another error, §6.4.2 constrains later reads of the affected range to one coherent endpoint: **all old data or all new data**. For a write larger than AWUPF, the specification gives no such data-result guarantee.

This is a coherence guarantee over the result of an interrupted write. It is not a promise that the newest version wins.

### H/P — successful completion can still be weaker than power-loss persistence when volatile caching is in the path

Immediately after the AWUPF example, Revision 1.1b gives a bounded exception to the usual completed-write read-currentness rule. Older data may be returned after shutdown when all of the relevant conditions hold: the controller has a volatile write cache, that cache is enabled, the write did not use FUA, no relevant Flush successfully completed before shutdown, and shutdown occurred without completing the specified normal or abrupt shutdown procedure.

This is first-party normative evidence for a distinction already central to Case 20:

```text
command completed
        !=
newest value guaranteed to survive every power-loss path
```

The exception should not be generalized beyond the conditions stated by the specification.

---

## Engineering reconstruction

### E — failure atomicity preserves an admissible version boundary, not necessarily the newest version

If an interrupted write no larger than AWUPF may resolve to either the old version or the new version, but not a mixture, then the interface preserves **version coherence** without promising **newest-value durability**.

A compact reconstruction is:

```text
AWUPF-sized interrupted write
        -> admissible post-failure versions {old, new}
        -> forbidden torn mixture within the covered range
```

That is different from a durability rule whose only admissible post-failure value is `new`.

### E — atomicity and persistence ordering are independent axes

AWUN/AWUPF constrain which combinations of block contents are admissible. FUA/Flush constrain whether data cross the volatile/nonvolatile boundary under their respective contracts. Host/application ordering remains another relation again.

Therefore:

```text
atomicity != durability != cross-command persistence ordering
```

One cannot repair a missing FUA/Flush persistence guarantee merely by observing that a write fits within AWUPF.

### E — command completion and coherent failure outcome are not synonyms

The completed-write volatile-cache exception shows why `completed`, `atomic if interrupted`, and `durably newest` must remain separate predicates. A system can provide a coherent failure result while still allowing the older coherent version to remain after a qualifying power-loss path.

### E — interface guarantee does not identify the mechanism below it

Nothing in these fields proves that a controller uses capacitors, batteries, a particular FTL journal, NAND-page atomic programming, copy-on-write metadata, or a particular physical page size. Those mechanisms require evidence from a named implementation.

---

## Functional analogy

### A — Case 15: named SSD power-loss protection

Case 15 grounds a concrete Intel SSD 320 implementation path involving volatile state, power-fail detection, stored energy, firmware prioritization, and transfer to NAND. Case 20/this evidence record instead ground an **interface guarantee**. The two can satisfy related host needs but are not the same mechanism.

### A — Case 39: FTL metadata recovery

Case 39 studies an internal power-failure recovery design for mapped Flash metadata. AWUPF supplies no evidence that an NVMe controller implements that recovery algorithm. The useful comparison is only functional: both constrain the set of states that may survive interruption.

### A — Cases 143 and 152: journal/WAL coherent-state selection

SQLite rollback-journal and WAL cases also distinguish admissible crash-recovery states from simple newest-byte survival. That is a higher-layer functional analogy, not an implementation lineage: SQLite page/journal protocols and NVMe AWUPF are different state machines at different interfaces.

---

## Philosophical interpretation

### I — retention may preserve coherence rather than recency

**Interpretive, not historical terminology:** a retention guarantee can preserve a boundary between coherent admissible states without promising that the most recent attempted state is the one retained. AWUPF is a useful technical witness because the old version and the new version can both be allowed outcomes while a torn hybrid is disallowed.

This interpretation must stay downstream of the normative facts above; the NVMe specification does not present itself as a philosophy of memory or identity.

---

## Boundaries and anti-overclaim

- `AWUN != AWUPF`.
- `AWUPF-sized atomicity != newest-value durability`.
- `all-old-or-all-new != always-new`.
- `command completion != guaranteed media persistence` when the specification's volatile-cache exception applies.
- `failure atomicity != Flush/FUA persistence semantics`.
- `failure atomicity != sanitization`.
- `interface contract != internal FTL / capacitor / NAND mechanism`.
- `2014 explicit wording != invention date`.
- earlier or broader atomic-write genealogy is not established here.

---

## Prior art and related-repository boundary

Case 20 already refuses a novelty claim for Flush/FUA and points to earlier storage-interface work. For the narrower **atomic-write / torn-write** genealogy, this evidence record deliberately stops short of naming an origin from incomplete evidence.

A repository search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `AWUPF` and `atomic write NVMe` found no existing dedicated treatment at the time of this slice. A broader pre-NVMe genealogy of atomic-sector, atomic-block, RAID, database, SCSI/ATA, and controller guarantees belongs there if pursued; it should not be reconstructed backwards from NVMe terminology alone.

---

## Open evidence debt

- establish a properly sourced pre-NVMe genealogy for atomic-sector / atomic-block / torn-write terminology without conflating database transactions, disk-sector physical atomicity, and host-interface guarantees;
- identify named NVMe products that publish both AWUN/AWUPF values and a separately documented PLP mechanism, then compare contract with mechanism;
- fault-inject real hardware at write sizes below, at, and above reported AWUPF, while separately varying WCE, FUA, Flush, and shutdown path;
- trace later NVMe namespace atomic-boundary fields and technical proposals only if they add a genuinely different retention relation.

---

## Status

**`grounded`** as a bounded Case 20 evidence deepening for the 2014 normative torn-write / atomicity-versus-durability distinction.
EOF

python3 - <<'PY'
from pathlib import Path
import re

case_path = Path('cases/20-nvme10-fua-flush-persistence-ordering.md')
text = case_path.read_text()
if '20-nvme-2014-atomic-write-torn-write-deepening.md' in text:
    raise SystemExit('Case20 deepening already integrated')

hist_anchor = '\n---\n\n## Retained state\n'
hist_insert = r'''

### H/P — Revision 1.1b makes the interrupted-write contract explicit

A later official NVM Express witness, **Revision 1.1b dated 2 July 2014**, sharpens the distinction already exposed by Revision 1.0. Its Identify Controller text says AWUN applies to normal-operation atomicity and is not the power-fail/error guarantee; AWUPF is reported separately for power-fail/error conditions and is constrained to be no larger than AWUN.

Section 6.4 then names **torn writes** as the failure AWUPF is meant to constrain. For an interrupted write no larger than AWUPF, later reads of the affected range are constrained to one coherent endpoint — all old data or all new data — rather than an old/new mixture. Above AWUPF, that result guarantee is not provided.

This later wording deepens the semantics of the already-present 2011 AWUPF field. It is **not** used here as an invention date or as evidence for one internal controller mechanism.

### H/P — completed write and power-loss persistence remain different predicates

Revision 1.1b also states a bounded exception to completed-write currentness: older data may reappear after shutdown when volatile write cache is supported and enabled, the write did not use FUA, no relevant Flush successfully completed before shutdown, and the controller shut down without completing the specified normal or abrupt shutdown procedure.

That clause makes the retention boundary unusually clear:

```text
command completed
        !=
newest value guaranteed to survive every qualifying power-loss path
```

See [`../evidence/20-nvme-2014-atomic-write-torn-write-deepening.md`](../evidence/20-nvme-2014-atomic-write-torn-write-deepening.md) for the bounded 1.1b evidence ledger and anti-overclaim notes.
'''
if hist_anchor not in text:
    raise SystemExit('Case20 historical insertion anchor not found')
text = text.replace(hist_anchor, hist_insert + hist_anchor, 1)

eng_anchor = '\n---\n\n## Functional analogies\n'
eng_insert = r'''

### E — failure atomicity ≠ newest-value durability

Revision 1.1b's all-old/all-new rule supplies a stronger reconstruction than the bare fact that AWUPF exists. Within the covered interrupted-write size, **version coherence** is protected while **recency** is not guaranteed: both the predecessor and successor are admissible, while a torn hybrid is not.

```text
coherent admissible state after interruption
        !=
newest attempted state must survive
```

AWUN, AWUPF, FUA/Flush, and host-enforced ordering therefore describe different axes: normal-operation command atomicity, failure atomicity, volatile-to-nonvolatile commitment, and cross-command order.

### E — interface anti-torn guarantee ≠ internal recovery mechanism

The normative result does not identify whether a controller obtains it through stored energy, a journal, copy-on-write metadata, NAND program geometry, firmware replay, or another mechanism. Those are implementation questions requiring named-product or implementation evidence. AWUPF also says nothing about sanitization of superseded physical embodiments.
'''
if eng_anchor not in text:
    raise SystemExit('Case20 engineering insertion anchor not found')
text = text.replace(eng_anchor, eng_insert + eng_anchor, 1)

source_anchor = 'Grounding details and direct facsimile checks are recorded in [`../evidence/20-nvme10-2011-flush-fua-grounding.md`](../evidence/20-nvme10-2011-flush-fua-grounding.md).'
source_insert = '''- NVM Express, **_NVM Express Revision 1.1b_**, 2 July 2014, official archived PDF: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_1b-1.pdf>.\n  - Identify Controller pp. 91–92 — AWUN normal-operation boundary, AWUPF power-fail/error boundary, and `AWUPF <= AWUN`;\n  - §6.4, printed pp. 120–122 — atomic operations, torn-write definition, all-old/all-new AWUPF result, and completed-write volatile-cache exception.\n\nGrounding details for the 2011 slice remain in [`../evidence/20-nvme10-2011-flush-fua-grounding.md`](../evidence/20-nvme10-2011-flush-fua-grounding.md). The 2014 deepening is recorded in [`../evidence/20-nvme-2014-atomic-write-torn-write-deepening.md`](../evidence/20-nvme-2014-atomic-write-torn-write-deepening.md).'''
if source_anchor not in text:
    raise SystemExit('Case20 source anchor not found')
text = text.replace(source_anchor, source_insert, 1)
case_path.write_text(text)

road_path = Path('ROADMAP.md')
road = road_path.read_text()
road_marker = '**Case 20 atomicity-vs-durability deepening (NVMe 1.1b):**'
if road_marker not in road:
    phase = '## Phase 2 — Evidence-backed expansion with comparison discipline\n'
    if phase not in road:
        raise SystemExit('ROADMAP Phase 2 anchor not found')
    item = ('\n- [x] **Case 20 atomicity-vs-durability deepening (NVMe 1.1b):** added first-party 2014 normative evidence that AWUN does not cover power-fail errors, AWUPF is a separate no-larger envelope, AWUPF-sized interrupted writes resolve all-old or all-new rather than torn, and a completed write may still lose newest-value persistence under the specified volatile-cache/no-FUA/no-Flush/improper-shutdown conjunction. Kept interface guarantee separate from internal FTL/PLP mechanism, made no atomic-write invention claim, and left broader pre-NVMe genealogy to `computing-archaeology`.\n')
    road = road.replace(phase, phase + item, 1)
    road_path.write_text(road)

idx_path = Path('CASE_INDEX.md')
idx = idx_path.read_text()
if 'NVMe 1.1b explicitly separates AWUN normal-operation atomicity' in idx:
    raise SystemExit('CASE_INDEX Case20 deepening already integrated')
nums = [int(m.group(1)) for m in re.finditer(r'(?m)^(\d+)\.\s', idx)]
if not nums:
    raise SystemExit('No numbered CASE_INDEX findings found')
mx = max(nums)
if mx < 3349:
    raise SystemExit(f'Unexpected CASE_INDEX tail: {mx}')
last = list(re.finditer(rf'(?m)^{mx}\.\s.*$', idx))
if not last:
    raise SystemExit('Could not locate final numbered finding')
pos = last[-1].end()
next_heading = idx.find('\n## ', pos)
if next_heading == -1:
    next_heading = len(idx)
start = mx + 1
findings = [
    ('Historical record', 'NVMe 1.1b (2014-07-02) explicitly separates AWUN normal-operation atomicity from power-fail/error behavior; AWUN is not the applicable power-fail guarantee.'),
    ('Historical record', 'NVMe 1.1b reports AWUPF separately for power-fail/error conditions and requires `AWUPF <= AWUN`.'),
    ('Historical record', 'NVMe 1.1b defines a torn write as an interrupted contiguous write that leaves a mixture of original and new logical-block contents.'),
    ('Historical record', 'For an interrupted write no larger than AWUPF, NVMe 1.1b constrains later reads to a coherent endpoint: all old data or all new data, rather than a torn mixture.'),
    ('Historical record', 'For a write larger than AWUPF, NVMe 1.1b does not provide the same post-failure data-result guarantee.'),
    ('Engineering reconstruction', '`all-old or all-new` failure coherence does not imply newest-value durability; an older coherent predecessor remains an admissible result.'),
    ('Historical record', 'NVMe 1.1b permits older data after shutdown under the stated conjunction of enabled volatile write cache, no FUA, no successful relevant Flush, and shutdown without completing the specified normal/abrupt procedure.'),
    ('Engineering reconstruction', 'Generic command completion therefore remains distinct from guaranteed persistence of the newest value when the volatile-cache exception applies.'),
    ('Engineering reconstruction', 'AWUN inter-command atomicity, AWUPF interrupted-write atomicity, FUA/Flush persistence, and host-enforced ordering are separate interface relations.'),
    ('Method / prior art', 'The 2014 text is used as a later explicit normative witness, not as an invention-priority claim for atomic writes or torn-write protection; broader genealogy remains open.'),
    ('Functional analogy', 'Case 15 named-product PLP and Case 39 FTL recovery may constrain related failure outcomes, but AWUPF alone does not establish either implementation mechanism.'),
    ('Philosophical interpretation', 'The project may describe AWUPF as preserving a coherent admissible-state boundary rather than guaranteed recency; this is interpretive vocabulary, not NVMe historical terminology.'),
    ('Security boundary', 'Atomic-write / anti-torn semantics do not establish sanitization of superseded physical embodiments.')
]
block = '\n\n' + '\n'.join(f'{start+i}. **{kind}:** {body}' for i, (kind, body) in enumerate(findings)) + '\n'
idx = idx[:next_heading] + block + idx[next_heading:]
idx_path.write_text(idx)
print(f'CASE_INDEX findings added: {start}-{start+len(findings)-1}')
PY

git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'

git add cases/20-nvme10-fua-flush-persistence-ordering.md "$EVIDENCE" CASE_INDEX.md ROADMAP.md
rm -f scripts/integrate-case20-nvme-torn-write.sh .github/workflows/integrate-case20-nvme-torn-write.yml
git add -A

if git diff --cached --quiet; then
  echo 'No changes to commit' >&2
  exit 1
fi

git commit -m 'case20: deepen NVMe torn-write atomicity'
git push origin HEAD:main
