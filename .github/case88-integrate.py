from pathlib import Path

case_path = 'cases/88-linux-md-raid5-partial-parity-log.md'
ev_path = 'evidence/88-linux-1993-2017-raid5-ppl-grounding.md'

assert Path(case_path).exists(), case_path
assert Path(ev_path).exists(), ev_path

# README
p = Path('README.md')
s = p.read_text()
if case_path not in s:
    lines = s.splitlines()
    idx = next(i for i, line in enumerate(lines)
               if 'cases/87-scsi2-writeback-cache-fua-synchronize-cache.md' in line)
    new = ('- [`cases/88-linux-md-raid5-partial-parity-log.md`](cases/88-linux-md-raid5-partial-parity-log.md) — '
           'grounded Linux MD RAID5 write-hole bridge: the 2017 PPL implementation persists checked partial-parity plus stripe-identification evidence before ordinary data/parity writes are released, allowing bounded dirty-start parity recovery without promising preservation of all in-flight payload; its original volatile-member-cache warning also makes lower-layer durability/order part of the array-level guarantee; see '
           '[`evidence/88-linux-1993-2017-raid5-ppl-grounding.md`](evidence/88-linux-1993-2017-raid5-ppl-grounding.md).')
    lines.insert(idx + 1, new)
    p.write_text('\n'.join(lines) + '\n')

# ROADMAP
p = Path('ROADMAP.md')
s = p.read_text()
if case_path not in s:
    lines = s.splitlines()
    idx = next(i for i, line in enumerate(lines)
               if 'cases/87-scsi2-writeback-cache-fua-synchronize-cache.md' in line)
    new = ('- [x] Linux MD RAID5 Partial Parity Log / write-hole recovery-evidence boundary — '
           '[`cases/88-linux-md-raid5-partial-parity-log.md`](cases/88-linux-md-raid5-partial-parity-log.md), grounded by '
           '[`evidence/88-linux-1993-2017-raid5-ppl-grounding.md`](evidence/88-linux-1993-2017-raid5-ppl-grounding.md), '
           'separates physically surviving parity from parity currentness, a compact partial-parity recovery witness from a full in-flight payload journal, and software-before ordering from actual lower-layer power-fail durability. Linux 4.12 explicitly says PPL is not a true journal and does not protect all in-flight data; 1993 parity-logging research and 1995-filed DEC write-hole recovery block invention claims. Full Intel IMSM/controller genealogy and modern fault-injection validation remain separate work, with broad RAID history routed to `computing-archaeology`.')
    lines.insert(idx + 1, new)
    p.write_text('\n'.join(lines) + '\n')

# CASE_INDEX ledger
p = Path('CASE_INDEX.md')
s = p.read_text()
if case_path not in s:
    lines = s.splitlines()
    marker = '| [SCSI-2 Write-Back Cache, FUA, and SYNCHRONIZE CACHE:'
    idx = next(i for i, line in enumerate(lines) if line.startswith(marker))
    row = ('| [Linux MD RAID5 Partial Parity Log: Retaining Just Enough Recovery Evidence Before a Non-Atomic Stripe Update]'
           '(cases/88-linux-md-raid5-partial-parity-log.md) | **grounded** | RAID5 data/parity stripe + checked member-local partial-parity log + affected-stripe/generation metadata + lower-layer durability/order assumption | '
           'separate parity presence from parity currentness; recovery-sufficient relation data from a full write journal; write-hole closure from interrupted-payload atomicity; and software issue order from power-fail-persistent ordering | '
           '[1993–2017 parity/PPL grounding](evidence/88-linux-1993-2017-raid5-ppl-grounding.md); Intel IMSM origin/version genealogy, later PPL cache-flush evolution, cross-controller comparison, and hardware fault injection remain separate work |')
    lines.insert(idx + 1, row)
    s = '\n'.join(lines) + '\n'

# comparison row
if '| Linux MD RAID5 PPL / 2017 bounded regime |' not in s:
    lines = s.splitlines()
    candidates = [i for i, line in enumerate(lines)
                  if line.startswith('| SCSI-2 / SBC-2 cache durability / 1994–2004 bounded chain |')]
    assert len(candidates) == 1, candidates
    idx = candidates[0]
    row = ('| Linux MD RAID5 PPL / 2017 bounded regime | RAID5 data/parity chunks + member-local PPL header/partial-parity evidence + generation/checksum metadata + array relation | '
           'derive partial parity while old/current chunks remain available; persist PPL before ordinary member writes; recover parity after dirty shutdown; retire temporary evidence after closure | '
           'ordinary reads remain RAID5 reads; recovery may use PPL to re-establish trustworthy parity, but PPL does not promise the newest interrupted user write | '
           'stripe/member/parity-disk identity plus logged data-sector/size relation; PPL lives in member metadata rather than a dedicated journal device | '
           'member payload locations normally remain fixed for the bounded update; what changes is whether the cross-member parity relation is trustworthy after interruption | '
           'no complete write history: retains bounded temporary recovery evidence sufficient for the documented write-hole recovery relation, not all in-flight payload |')
    lines.insert(idx + 1, row)
    s = '\n'.join(lines) + '\n'

# aggregate count
old = 'After eighty-eight bounded cases, **all eighty-eight cases are now `grounded`.**'
new = 'After eighty-nine bounded cases, **all eighty-nine cases are now `grounded`.**'
assert old in s or new in s
s = s.replace(old, new, 1)

# findings
if '## Case 88 — Linux MD RAID5 PPL findings' not in s:
    assert '1084. **the required retention boundary depends on the transition to be survived**' in s
    block = '''

## Case 88 — Linux MD RAID5 PPL findings

1085. **parity presence ≠ parity currentness** — a parity block can remain physically readable after a dirty shutdown while no longer matching the surviving data chunks needed for trustworthy reconstruction;
1086. **write-hole closure ≠ preservation of the interrupted newest payload** — Linux explicitly says PPL is not a true journal and does not protect all in-flight data;
1087. **recovery-sufficient evidence ≠ complete payload duplicate** — PPL retains partial parity plus bounded stripe metadata rather than another complete copy of every modified data chunk;
1088. **pre-update recovery evidence can be constitutive retention state** — PPL must be written before the ordinary data/parity writes are released into the non-atomic update interval;
1089. **partial parity ≠ ordinary RAID parity** — the PPL relation is auxiliary recovery evidence derived for an update, while the normal parity chunk is the array's standing redundancy contribution;
1090. **PPL header/checksum state ≠ user payload** — affected-stripe, size, generation, parity-disk, and checksum metadata qualify whether retained recovery evidence can be interpreted and trusted;
1091. **full-stripe write ≠ partial-stripe logging requirement** — the implementation can omit partial-parity payload for full-stripe writes and retain only enough marking to recalculate parity after an unclean shutdown;
1092. **distributed log ≠ dedicated journal device** — Linux PPL places per-stripe evidence in RAID-member metadata, associated with the stripe's parity disk, rather than requiring one separate journal drive;
1093. **PPL ≠ `raid5-cache`** — both can address the write hole, but Linux's own documentation/patch discussion keeps their stored evidence and journal roles distinct;
1094. **logical-before ordering ≠ power-fail-persistent ordering through the stack** — the initial 2017 implementation warns that volatile member-drive write-back caches can defeat the PPL guarantee unless the needed lower-layer persistence/order relation is enforced;
1095. **array-level recovery metadata depends on lower-layer durability semantics** — a correct parity-recovery algorithm is insufficient if its precursor record disappears below the block layer during the same power failure it is meant to survive;
1096. **parity-consistency recovery ≠ member replacement / restored failure margin** — PPL can restore a trustworthy redundancy relation without repairing a failed disk or restoring consumed redundancy capacity;
1097. **temporary recovery state can become correctly forgettable after closure** — once the relevant update/recovery relation is safely resolved, retaining that PPL evidence indefinitely is not the mechanism's purpose;
1098. **Linux 4.12 PPL ≠ invention of parity logging** — Stodolsky, Holland, and Gibson explicitly publish parity logging for redundant disk arrays in 1993;
1099. **Linux 4.12 PPL ≠ invention of RAID5 write-hole recovery** — a 1995-filed Digital Equipment Corporation patent already describes retained non-volatile write/cache metadata used to recover parity consistency after interrupted RAID5 writes;
1100. **retention can preserve a relation selected for one future failure model rather than maximal information** — PPL is a bounded example in which less than the complete interrupted write is deliberately retained because that smaller relation is sufficient to keep a later reconstruction from silently trusting inconsistent parity;
'''
    s = s.rstrip() + block + '\n'

p.write_text(s)

# validations
readme = Path('README.md').read_text()
roadmap = Path('ROADMAP.md').read_text()
index = Path('CASE_INDEX.md').read_text()
assert readme.count(case_path) == 2, readme.count(case_path)
assert readme.count(ev_path) == 2, readme.count(ev_path)
assert roadmap.count(case_path) == 2, roadmap.count(case_path)
assert roadmap.count(ev_path) == 2, roadmap.count(ev_path)
assert index.count(case_path) == 1, index.count(case_path)
assert index.count(ev_path) == 1, index.count(ev_path)
assert '| Linux MD RAID5 PPL / 2017 bounded regime |' in index
assert 'After eighty-nine bounded cases, **all eighty-nine cases are now `grounded`.**' in index
assert '1085. **parity presence ≠ parity currentness**' in index
assert '1100. **retention can preserve a relation selected for one future failure model rather than maximal information**' in index
