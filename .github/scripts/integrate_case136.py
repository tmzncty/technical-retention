from pathlib import Path
import re

EVIDENCE = Path('evidence/136-dell-2013-2018-perc-puncture-source-readability-deepening.md')
CASE = Path('cases/136-megaraid-perc-rebuild-rate-repair-priority.md')
ROADMAP = Path('ROADMAP.md')
INDEX = Path('CASE_INDEX.md')

assert not EVIDENCE.exists(), 'evidence already exists'

EVIDENCE.write_text(r'''# Evidence 136B — Dell PERC degraded-rebuild source unreadability and RAID puncture

## Status

**`grounded`** — bounded primary-source deepening for Case 136. This record asks what happens when rebuild is scheduled and progressing but a surviving source contribution required for reconstruction is unreadable. It does **not** estimate universal URE probability, generalize RAID 5 behavior to RAID 6, or infer undocumented PERC firmware internals.

## Scope question

Case 136 already separates rebuild-rate policy from repair obligation and rebuild execution. This slice asks a narrower question:

> On documented Dell PERC systems, can a degraded rebuild continue even when a local stripe cannot be reconstructed because a surviving source contribution is unreadable, and what state remains afterward?

## Source set and provenance

### Dell OpenManage Server Administrator Storage Management User's Guide — March 2013

- Dell Inc., *OpenManage Server Administrator Storage Management User's Guide*, March 2013.
- Official Dell-hosted manufacturer PDF.
- Relevant sections: `A Rebuild Completes with Errors` (PDF page 299) and `Receive a “Bad Block” Alert with “Replacement,” “Sense,” or “Medium” Error` (PDF page 304).
- <https://dl.dell.com/manuals/all-products/esuprt_electronics/esuprt_software/esuprt_ent_sys_mgmt/dell-opnmang-srvr-admin-mngd-das_user's%20guide_en-us.pdf>
- Accessed 2026-09-12.

### Dell EMC PowerEdge Servers Troubleshooting Guide — November 2018, Rev. A11

- Dell EMC, *PowerEdge Servers Troubleshooting Guide*, Rev. A11, November 2018.
- Official Dell-hosted manufacturer PDF.
- Relevant section: `RAID puncture`, PDF pages 97–99.
- <https://dl.dell.com/manuals/common/servertroubleshootingguide_en.pdf>
- Accessed 2026-09-12.

### Current Dell knowledge-base continuity witness

- Dell, `PowerEdge: How to fix Double Faults and Punctures in RAID Arrays`.
- <https://www.dell.com/support/kbdoc/en-us/000139251/double-faults-and-punctures-in-raid-arrays>
- Used only as a maintained terminology/operational-continuity witness, not as first-use or invention evidence.

## Historical record

### March 2013: rebuild can complete while a damaged portion remains unrestored

Dell's March 2013 OpenManage guide has a section titled `A Rebuild Completes with Errors` for PERC 4/SC, 4/DC, 4e/DC, 4/Di, 4e/Si, and 4e/Di. It says a rebuild may complete successfully while reporting errors when part of the disk containing redundant/parity information is damaged: healthy portions can be restored while the damaged portion cannot. Alert 2163 can accompany this state.

The same section says that if backup of the degraded virtual disk encounters errors, user data has been damaged and cannot be recovered from the virtual disk; recovery then depends on an earlier backup.

This supplies a bounded manufacturer documentation floor by **March 2013** for:

> **rebuild completion status != proof that every damaged region was reconstructed.**

This is not an invention-priority claim.

### March 2013: damaged media discovered during degraded operation can cross a recoverability boundary

The guide says medium/bad-block damage can be discovered during consistency check, rebuild, virtual-disk format, or I/O. For alerts 2146–2150 received during rebuild or while the virtual disk is degraded, Dell says damaged data cannot be recovered from that disk without restoration from backup.

Thus a rebuild task can exist and run while not every source region needed by reconstruction remains readable.

### November 2018: Dell explicitly names `RAID puncture` / `rebuild with errors`

Dell's November 2018 PowerEdge troubleshooting guide defines `RAID puncture` as a PERC feature and also calls it `rebuild with errors`. When a double fault leaves insufficient redundancy to recover an impacted stripe, the controller creates a puncture in that stripe and allows rebuild to continue. The guide says affected stripe data is lost and future access to the affected data continues to encounter uncorrectable errors.

### Concrete RAID 5 example: one unavailable member plus one unreadable surviving contribution

Dell gives a three-member RAID 5 example: drive 0 fails and is replaced; drives 1 and 2 supply remaining data/parity; when rebuild reaches a stripe where drive 1 has a data error, insufficient information remains to reconstruct the missing stripe contribution. That stripe is unrecoverable/lost and becomes punctured during rebuild.

The second damaging condition is not another whole-drive failure. A local unreadable source region can consume the contribution the degraded stripe still needed.

> **latent surviving-source defect != second whole-device failure**, even though either can remove a contribution required by a particular reconstruction.

### Global redundancy can be restored while local payload loss remains

The 2018 guide says puncturing can restore redundancy and return the array to an `optimal` state while the affected stripe's data remains lost.

This directly separates:

- **rebuild complete != every payload byte recovered**;
- **redundancy restored != every prior stripe reconstructable**;
- **array optimal != no data loss has occurred**.

### Post-puncture consistency check is not lost-data recovery

Dell says Check Consistency after a puncture is induced does not resolve it. The guide recommends regular Check Consistency, especially before drive replacement when possible. Its post-puncture remedy is destructive at array scope: preserve recoverable data, delete/recreate and fully initialize the array, verify consistency, then restore data.

That is an operational recovery/reset path, not evidence of secure sanitization or forensic erasure.

## Engineering reconstruction

The following is a project reconstruction of documented relations, not a claim about undocumented firmware internals:

```text
member failure
    -> degraded array / repair obligation
    -> replacement destination available
    -> rebuild admitted and scheduled
    -> read surviving stripe contributions
        -> sufficient/readable: reconstruct missing contribution
        -> required surviving contribution unreadable and redundancy exhausted:
             local stripe reconstruction fails
             -> affected stripe punctured
             -> global rebuild can continue
    -> redundancy may later be restored / array may return optimal
       while punctured payload remains lost
```

### Source readability is a constitutive repair input

Case 136 already has scheduling state (`rebuild rate`) and task/progress state. This evidence adds an independent requirement:

> **rebuild rate / repair priority != source readability.**

A useful decomposition is:

```text
repair obligation
+ replacement destination
+ surviving-source readability/reconstructability
+ admitted scheduling/resources
-> possible reconstruction work
```

None alone proves successful recovery of every stripe.

### Progress is not reconstructable coverage

The Dell record permits global rebuild continuation after a local unrecoverable stripe is punctured.

> **rebuild progress/completion != reconstructable coverage.**

### Puncture is a retained negative condition, not a deletion primitive

Dell says accesses to punctured data continue to encounter uncorrectable errors and eliminating the puncture requires recreating the array and restoring data. At project level this supports treating puncture as a retained **negative condition / error relation** on an affected logical extent: later access remains constrained by an earlier failed reconstruction event.

This does not identify whether that relation is encoded in a BBM table, parity bytes, controller metadata, member media, or a combination.

### Proactive readability qualification != rebuild

A Check Consistency operation while the array is still optimal can expose conditions before another member loss consumes redundancy margin.

> **proactive integrity/readability maintenance != reconstruction after member loss.**

## Functional comparisons — not mechanism identity

### Case 18 — ZFS scrub; Cases 101 / 102 — medium scan and patrol read

The functional analogy is that proactive observation can expose latent integrity/media defects while enough redundancy remains to correct or retire them. Dell PERC Check Consistency, ZFS scrub, medium scan, and patrol read are not thereby the same mechanism.

### Case 94 — RAID 6 P/Q boundary

Dell's worked example is RAID 5. Case 94 is a counterexample to over-generalization because RAID 6 has a different erasure margin.

> **RAID 5 single-parity reconstruction boundary != universal RAID failure boundary.**

### Case 96 — dRAID / reduced repair exposure

Faster reconstruction can reduce time spent with diminished redundancy, but speed and source readability remain separate variables.

> **shorter degraded interval != certification that surviving source regions are readable.**

## Prior-art and chronology boundary

Safe chronology:

- by **March 2013**, Dell publicly documented `A Rebuild Completes with Errors` for named PERC 4 controllers;
- by **November 2018**, Dell explicitly used `RAID puncture` and equated it with `rebuild with errors`, including a concrete RAID 5 degraded-rebuild example.

These are documentation floors only. They do not establish Dell invention, first industry use of `puncture`, identical implementation across PERC generations, or direct implementation genealogy.

## Stop conditions / rejected upgrades

Do not upgrade this record without new evidence into claims that:

- `puncture == sanitize` or secure deletion;
- `array optimal == no data loss`;
- post-puncture Check Consistency recovers the lost stripe;
- one unreadable surviving block equals a second whole-drive failure;
- the 2013 guide proves Dell invented the feature or phrase;
- the 2018 wording proves identical firmware implementation across controller generations;
- the RAID 5 example applies automatically to RAID 6 or other codes;
- rebuild-rate priority itself causes or prevents punctures;
- these manuals establish universal URE probability, failure rate, correlation, or quantitative rebuild-risk curves;
- destructive array recreation proves forensic erasure of previous physical embodiments.

## Remaining evidence debt

- controller-generation-specific telemetry and persistence mechanism for punctured/error locations;
- named RAID 6 / multi-parity PERC behavior;
- cross-vendor behavior and terminology;
- probabilistic and correlated read-error models tied to named media/controller generations;
- independent fault injection reproducing local source unreadability during rebuild;
- interaction among rebuild scheduling, patrol read/check consistency, cache policy, and media-error handling;
- implementation history before the March 2013 documentation floor.

## Related-repository check

Fresh searches of `tmzncty/computing-archaeology` for `PERC puncture` and `RAID rebuild unrecoverable read error` returned no dedicated overlapping module during this round.

Division of labor:

- `technical-retention`: repair obligation, scheduling, source readability, local reconstruction failure, retained error condition, and restored redundancy;
- `computing-archaeology`: broader controller genealogy, prior terminology, firmware lineage, patrol-read/consistency-check history, and quantitative historical reconstruction if later developed.
''', encoding='utf-8')

# Case 136
case = CASE.read_text(encoding='utf-8')
assert '136-dell-2013-2018-perc-puncture' not in case
case = case.replace(
    'Grounding record: [`../evidence/136-lsi-2006-dell-perc-rebuild-rate-grounding.md`](../evidence/136-lsi-2006-dell-perc-rebuild-rate-grounding.md).',
    'Grounding records:\n\n- [`../evidence/136-lsi-2006-dell-perc-rebuild-rate-grounding.md`](../evidence/136-lsi-2006-dell-perc-rebuild-rate-grounding.md) — rebuild-rate / maintenance-policy semantics;\n- [`../evidence/136-dell-2013-2018-perc-puncture-source-readability-deepening.md`](../evidence/136-dell-2013-2018-perc-puncture-source-readability-deepening.md) — surviving-source unreadability, rebuild-with-errors, and RAID-puncture boundary.'
)
anchor = '### Rebuild urgency != payload correctness\n'
assert anchor in case
section = r'''### Surviving-source readability can limit reconstruction even while rebuild continues

Dell's March 2013 OpenManage guide documents `A Rebuild Completes with Errors` for named PERC 4 controllers: a rebuild can report successful completion while damaged portions cannot be restored. The same guide says medium/bad-block damage discovered during rebuild or degraded operation can cross a recovery boundary that requires restoration from backup.

Dell's November 2018 PowerEdge troubleshooting guide makes the relation more explicit under `RAID puncture` / `rebuild with errors`. Its RAID 5 example starts with one failed/replacement member; if a surviving member has a data error in the same stripe when rebuild reaches it, remaining information is insufficient to reconstruct that stripe. PERC can puncture that stripe and let global rebuild continue.

The guide says puncturing can restore redundancy and return the array to `optimal` while the affected stripe remains lost. Therefore:

> **rebuild progress/completion != reconstructable coverage.**
>
> **redundancy restored / array optimal != complete payload integrity.**
>
> **rebuild rate / repair priority != surviving-source readability.**

Source readability is a constitutive repair input alongside replacement destination and admitted controller resources. More scheduling priority cannot reconstruct information the redundancy code no longer has.

A local unreadable region on a surviving member must also remain distinct from a second whole-device failure. Both can remove a contribution required by a stripe, but they differ in scope and failure object.

Dell says affected punctured data continues to produce uncorrectable errors when accessed and post-puncture Check Consistency does not resolve the existing loss. At project level this supports treating puncture as a retained **negative condition / error relation** on the affected logical extent. It does not identify an undocumented firmware field or where that relation is physically encoded.

'''
case = case.replace(anchor, section + anchor)

old_rel = '### Cases 18 / 102 — scrub and patrol read\n'
assert old_rel in case
s = case.index(old_rel)
e = case.index('### Case 131 — PERC foreign configuration\n', s)
new_rel = r'''### Cases 18 / 101 / 102 — proactive integrity and media scans

The puncture evidence sharpens why proactive observation matters. A consistency check, scrub, medium scan, or patrol-read style operation can expose latent defects while enough redundancy remains to repair or retire them. After a separate member loss consumes redundancy margin, the same local unreadability can become unreconstructable.

This is a functional comparison only:

> **proactive integrity/readability maintenance != rebuild**, and Dell PERC Check Consistency is not thereby equivalent to ZFS scrub or another stack's checksum mechanism.

### Cases 94 / 96 — code margin and repair exposure

Case 94's RAID 6 P/Q example is a counterexample to universalizing Dell's RAID 5 example: code strength changes how many unavailable contributions a stripe can tolerate. Case 96 shows how faster reconstruction can reduce the interval spent degraded.

> **shorter repair exposure != proof that every surviving source region is readable**, and **RAID 5 failure geometry != RAID 6 failure geometry**.

'''
case = case[:s] + new_rel + case[e:]
old_open = '''- earlier pre-2006 RAID-controller rebuild-throttling genealogy;
- exact persistence location and reset/default semantics of the rebuild-rate property on named controllers;
- whether in-flight rebuild progress resumes or restarts from an earlier checkpoint after power loss on named MegaRAID/PERC generations;
- measured rebuild-rate-to-throughput mapping under controlled foreground workloads;
- rebuild-rate interaction with URE handling, patrol read, consistency check, cache policy, and SSD/HDD media mix;
- current PERC 12/13 generation semantics and firmware-specific mutability;
- fault injection and second-failure exposure measurements.'''
new_open = '''- earlier pre-2006 rebuild-throttling and pre-2013 rebuild-with-errors / puncture genealogy;
- exact persistence location and reset/default semantics of rebuild-rate policy on named controllers;
- whether in-flight rebuild progress resumes or restarts from an earlier checkpoint after power loss;
- controller-generation-specific telemetry and persistence mechanism for punctured/error locations;
- RAID 6 / multi-parity PERC behavior and cross-vendor handling of surviving-source unreadability;
- probabilistic/correlated URE models and measured rebuild-rate-to-throughput/risk curves;
- interaction among rebuild scheduling, patrol read/check consistency, cache policy, and media mix;
- current PERC 12/13 generation semantics and firmware-specific mutability;
- independent fault injection and second-failure/source-read-error exposure measurements.'''
assert old_open in case
CASE.write_text(case.replace(old_open, new_open), encoding='utf-8')

# ROADMAP
roadmap = ROADMAP.read_text(encoding='utf-8')
assert 'Case 136 deepening — Dell PERC surviving-source unreadability' not in roadmap
lines = roadmap.splitlines()
flags = [False, False, False]
for i, line in enumerate(lines):
    if line.startswith('- [x] Case 136 MegaRAID/PERC rebuild-rate'):
        lines[i] = '- [x] Case 136 MegaRAID/PERC rebuild-rate / repair-priority policy slice — grounded LSI 2006 and later Dell PERC documentation separate repair obligation, rebuild execution/progress, controller resource-priority policy, and array configuration. Dell 2013/2018 source-readability evidence now adds `rebuild completes with errors` / `RAID puncture`: a degraded RAID 5 rebuild can continue after a surviving same-stripe source becomes unreadable, later restoring redundancy / `optimal` state while local payload remains lost. Pre-2006 throttling genealogy, pre-2013 puncture terminology, exact policy/progress/puncture persistence locations, RAID 6 and cross-vendor behavior, probabilistic URE models, throughput/risk curves, and independent fault injection remain open.'
        flags[0] = True
    elif line.startswith('- [ ] RAID / scrubbing / rebuild'):
        lines[i] = line.replace('Cases 17, 18, and 140', 'Cases 17, 18, 136, and 140').replace('Cases 17, 18', 'Cases 17, 18, 136', 1) if '136' not in line else line
        lines[i] += ' Case 136 now also grounds a named-controller boundary where surviving-source unreadability can make one degraded RAID 5 stripe unreconstructable while global rebuild continues.'
        flags[1] = True
    elif line.startswith('- [ ] inconsistent parity, stale/invalid reconstruction state, second failure before rebuild, or unreadable surviving data needed for reconstruction;'):
        lines[i] = '- [ ] inconsistent parity, stale/invalid reconstruction state, second failure before rebuild, or unreadable surviving data needed for reconstruction — **partially advanced by Case 136 PERC puncture deepening**: Dell 2013/2018 grounds a named RAID 5 path where one member is unavailable and a surviving same-stripe source is unreadable, making that stripe unreconstructable; PERC may puncture it, continue global rebuild, and later return the array to `optimal` / restored redundancy while local payload remains lost. Stale parity/currentness, second whole-device failure, RAID 6/multi-parity behavior, probabilistic URE policy, cross-vendor controllers, and independent fault injection remain open;'
        flags[2] = True
assert all(flags), f'ROADMAP anchors not all found: {flags}'
roadmap = '\n'.join(lines) + ('\n' if roadmap.endswith('\n') else '')
header = '### Recent bounded evidence deepening'
assert header in roadmap
entry = '- [x] **Case 136 deepening — Dell PERC surviving-source unreadability / RAID puncture boundary** — [Case 136](cases/136-megaraid-perc-rebuild-rate-repair-priority.md) now adds [Dell 2013/2018 evidence](evidence/136-dell-2013-2018-perc-puncture-source-readability-deepening.md): by March 2013 Dell documented `A Rebuild Completes with Errors`; by November 2018 its PERC guide explicitly described `RAID puncture` / `rebuild with errors`, including a RAID 5 example where a failed member plus a surviving same-stripe data error leaves insufficient information for that stripe. This grounds `rebuild completion != reconstructable coverage`, `array optimal / restored redundancy != complete payload integrity`, and `rebuild-rate policy != source readability`, without generalizing to RAID 6 or inferring universal URE probabilities.'
pos = roadmap.index(header) + len(header)
ROADMAP.write_text(roadmap[:pos] + '\n\n' + entry + roadmap[pos:], encoding='utf-8')

# CASE_INDEX — infer current table schema instead of hard-coding it.
idx = INDEX.read_text(encoding='utf-8')
ids = [int(x) for x in re.findall(r'(?m)^\|\s*(\d+)\s*\|', idx)]
assert ids and max(ids) == 3603, f'expected last finding 3603; got {max(ids) if ids else None}'
rows = idx.splitlines()
last_i = max(i for i, line in enumerate(rows) if re.match(r'^\|\s*3603\s*\|', line))
header_i = None
for j in range(last_i - 1, -1, -1):
    if rows[j].startswith('|') and j + 1 < len(rows) and re.match(r'^\|\s*:?-{3,}', rows[j + 1]):
        header_i = j
        break
assert header_i is not None
headers = [c.strip() for c in rows[header_i].strip().strip('|').split('|')]
assert len(headers) >= 4, headers
findings = [
(3604,'H/P','March 2013 Dell OpenManage documentation for named PERC 4 controllers says a rebuild can complete successfully while reporting errors and restore healthy portions but not a damaged portion.'),
(3605,'H/P','The 2013 guide says medium/bad-block damage discovered during rebuild or degraded operation can leave damaged data unrecoverable from the virtual disk without restoration from backup.'),
(3606,'H/P','Dell November 2018 documentation defines RAID puncture, also called rebuild with errors, as PERC behavior that can let rebuild continue when a double fault exceeds the impacted stripe redundancy.'),
(3607,'H/P','Dell worked RAID 5 example shows one failed/replacement member plus a data error on a surviving same-stripe member leaving insufficient information to reconstruct that stripe, which is lost/punctured during rebuild.'),
(3608,'H/P','The 2018 guide says puncturing can restore redundancy and return the array to an optimal state while the affected stripe remains lost.'),
(3609,'H/P','Dell says Check Consistency after a RAID puncture is induced does not resolve it, and recommends proactive Check Consistency, especially before drive replacement when possible.'),
(3610,'E','`rebuild progress/completion != reconstructable coverage`: global rebuild can continue after a local stripe becomes unreconstructable and is punctured.'),
(3611,'E','`array optimal / redundancy restored != complete payload integrity`: restored redundancy after puncture does not retroactively recover the lost stripe.'),
(3612,'E','`rebuild rate / repair priority != source readability`: surviving-source readability/reconstructability is a constitutive repair input independent of scheduling resources.'),
(3613,'E','`latent surviving-source defect != second whole-device failure`, although either can remove a contribution required by a particular degraded stripe.'),
(3614,'E/A','Proactive integrity/readability maintenance can preserve future repair opportunity by discovering latent defects before another member loss consumes redundancy margin; comparison to Cases 18/101/102 is functional only.'),
(3615,'A','Case 94 RAID 6 provides a code-margin counterexample: Dell concrete RAID 5 puncture geometry must not be generalized to dual-parity RAID without new evidence.'),
(3616,'A','Case 96 faster-repair comparison is limited to exposure time: faster rebuild or higher rebuild priority does not certify surviving-source readability or prevent puncture.'),
(3617,'X','RAID puncture is not sanitization; loss of a logical stripe does not establish forensic erasure of prior physical embodiments.'),
(3618,'X','The 2013 and 2018 Dell manuals establish documentation floors, not Dell invention priority, first use of puncture terminology, or identical firmware genealogy across PERC generations.'),
(3619,'X','No universal URE probability, failure rate, correlation model, or quantitative rebuild-risk curve is inferred from these vendor manuals; cross-vendor evidence and fault injection remain open.'),
]

def esc(s): return s.replace('|','\\|').replace('\n',' ')
case_link='[Case 136](cases/136-megaraid-perc-rebuild-rate-repair-priority.md)'
ev_link='[Evidence 136B](evidence/136-dell-2013-2018-perc-puncture-source-readability-deepening.md)'
new_rows=[]
for fid, typ, claim in findings:
    cells=[]
    for h in headers:
        k=h.lower().strip()
        if ('id' in k and ('finding' in k or k=='id')) or k in {'#','finding'}: val=str(fid)
        elif k in {'type','kind','class','label','evidence type'} or 'type' in k: val=typ
        elif 'case' in k: val=case_link
        elif any(x in k for x in ['claim','statement','description','finding text','summary']): val=claim
        elif any(x in k for x in ['evidence','source','record']): val=ev_link
        elif 'status' in k: val='grounded'
        else: val=''
        cells.append(esc(val))
    if str(fid) not in cells: cells[0]=str(fid)
    if typ not in cells and len(cells)>1: cells[1]=typ
    if esc(claim) not in cells:
        slot=next((p for p in range(2,len(cells)) if not cells[p]),None)
        assert slot is not None, headers
        cells[slot]=esc(claim)
    new_rows.append('| '+' | '.join(cells)+' |')
rows[last_i+1:last_i+1]=new_rows
INDEX.write_text('\n'.join(rows)+('\n' if idx.endswith('\n') else ''),encoding='utf-8')

# Final assertions
assert EVIDENCE.exists()
assert 'surviving-source readability can limit reconstruction' in CASE.read_text(encoding='utf-8').lower()
assert 'Case 136 deepening — Dell PERC surviving-source unreadability' in ROADMAP.read_text(encoding='utf-8')
final_idx=INDEX.read_text(encoding='utf-8')
for fid in range(3604,3620):
    assert re.search(rf'(?m)^\|\s*{fid}\s*\|', final_idx), fid
