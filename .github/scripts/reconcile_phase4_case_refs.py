from pathlib import Path

p = Path('ROADMAP.md')
text = p.read_text(encoding='utf-8')
old = '- [ ] logical deletion / invalidation — **partially advanced by grounded Cases 44, 73, 74, and now 91**: Case 41 adds distributed negative-state retention, showing that a delete can require a tombstone to remain authoritative over older SSTable/replica values until purge is locally admissible and stale replicas cannot legitimately restore the old value; broader database deletion, object lifecycle, key-destruction, and secure-erasure genealogies remain open;'
new = '- [ ] logical deletion / invalidation — **partially advanced by grounded Cases 41, 44, 73, and 74**: Case 41 adds distributed negative-state retention, showing that a delete can require a tombstone to remain authoritative over older SSTable/replica values until purge is locally admissible and stale replicas cannot legitimately restore the old value; broader database deletion, object lifecycle, key-destruction, and secure-erasure genealogies remain open;'
if text.count(old) != 1:
    raise SystemExit(f'expected one stale Case-91 Phase-4 reference, found {text.count(old)}')
text = text.replace(old, new)
old2 = 'The first bounded cross-case forgetting audit is now complete in [`docs/SYNTHESIS_AUDIT_05_TECHNICAL_FORGETTING.md`](docs/SYNTHESIS_AUDIT_05_TECHNICAL_FORGETTING.md). It establishes a five-case decomposition among physical disturbance/destruction, missed maintenance obligations, logical invalidation/deauthorization, relation/metadata loss, and service/recoverability loss. It also records the counterexamples `physical loss ≠ logical forgetting`, `physical survival ≠ retained current state`, and `unavailability ≠ forgetting`. The unchecked items above remain open because key destruction, obsolescence, bit rot, and several controller/institutional mechanisms have not yet been grounded by dedicated cases.'
new2 = 'The first bounded cross-case forgetting audit is now complete in [`docs/SYNTHESIS_AUDIT_05_TECHNICAL_FORGETTING.md`](docs/SYNTHESIS_AUDIT_05_TECHNICAL_FORGETTING.md). It establishes a five-case decomposition among physical disturbance/destruction, missed maintenance obligations, logical invalidation/deauthorization, relation/metadata loss, and service/recoverability loss. It also records the counterexamples `physical loss ≠ logical forgetting`, `physical survival ≠ retained current state`, and `unavailability ≠ forgetting`. The unchecked items above remain open because several mechanism families are only partially grounded: Case 44 now advances key destruction, Case 83 advances replicated-block bit-rot detection, and Case 98 advances failed distributed repair, while obsolescence and several controller/institutional forgetting regimes still lack dedicated closure.'
if text.count(old2) != 1:
    raise SystemExit(f'expected one stale Phase-4 summary, found {text.count(old2)}')
text = text.replace(old2, new2)
p.write_text(text, encoding='utf-8')
