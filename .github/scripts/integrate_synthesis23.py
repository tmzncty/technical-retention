from pathlib import Path
import re

readme_path = Path('README.md')
readme = readme_path.read_text(encoding='utf-8')
readme_link = 'docs/SYNTHESIS_23_RETENTION_INTERPRETER_ACCESS_APPARATUS.md'
if readme_link not in readme:
    marker = '\n\nThis chain is a **research heuristic**'
    assert marker in readme, 'README synthesis insertion marker missing'
    paragraph = "\n\nA bounded access-apparatus / compatibility synthesis is now available in [`docs/SYNTHESIS_23_RETENTION_INTERPRETER_ACCESS_APPARATUS.md`](docs/SYNTHESIS_23_RETENTION_INTERPRETER_ACCESS_APPARATUS.md). Across grounded Flash mapping recovery, ZFS restart-root and feature-flag cases, LTO reader compatibility, and PERC controller replacement it separates material embodiment, restart legibility, software-format interpretation, physical reader/transducer capability, controller admission, operation-specific service mode, and later migration/repair. It fixes the counterexamples `material survival ≠ operational recoverability`, `restart legibility ≠ format interpretability`, `compatible interpreter ≠ media integrity`, `read compatibility ≠ write compatibility`, `controller admission ≠ pending-write commitment`, and `current apparatus unavailable ≠ irrecoverably forgotten`."
    readme = readme.replace(marker, paragraph + marker, 1)
    readme_path.write_text(readme, encoding='utf-8')

roadmap_path = Path('ROADMAP.md')
roadmap = roadmap_path.read_text(encoding='utf-8')
old = '- [ ] interpretive or procedural-context loss while physical state survives;'
new = '- [ ] interpretive or procedural-context loss while physical state survives — **substantially advanced at the machine-access-apparatus layer by grounded Cases 39 and 128–131 plus Synthesis 23**: the repository now separates material embodiment, restart/root legibility, reconstructible mapping, software-format capability, physical reader/transducer compatibility, controller admission, operation-specific read/write/import authority, and later migration/repair. This grounds `material survival ≠ operational recoverability`, `restart legibility ≠ format interpretability`, `read compatibility ≠ write compatibility`, and `current apparatus unavailable ≠ irrecoverably forgotten` without equating software interpretation, tape transduction, or controller recovery. Human procedural/cultural context, application schemas and encodings, emulator/OS dependency chains, host-interface adapters, reader maintenance labor, and controlled migration remain open;'
if old in roadmap:
    roadmap = roadmap.replace(old, new, 1)
    roadmap_path.write_text(roadmap, encoding='utf-8')
elif 'machine-access-apparatus layer by grounded Cases 39 and 128–131 plus Synthesis 23' not in roadmap:
    raise AssertionError('ROADMAP interpretive/context marker missing')

index_path = Path('CASE_INDEX.md')
index = index_path.read_text(encoding='utf-8').rstrip() + '\n'
heading = '## Synthesis 23 — retained state / interpreter / access-apparatus findings'
if heading not in index:
    assert '**2358 —' in index, 'expected current finding 2358 missing'
    findings = '''
## Synthesis 23 — retained state / interpreter / access-apparatus findings

- **2359 — material inscription survival ≠ operational recoverability.** Cases 39 and 128–131 show surviving Flash pages, pool blocks, magnetic tape, or RAID members can remain unusable until mapping, roots, compatible apparatus, or admission relations are available. (`E`)
- **2360 — restart legibility ≠ format interpretability.** Case 128 can supply a qualified ZFS root/topology while Case 129 separately asks whether the available software understands the active on-disk feature requirements. (`A`, `E`)
- **2361 — compatible interpreter ≠ verified media integrity.** Restoring ZFS software that understands the feature set removes one admissibility barrier but does not prove checksums, redundancy, or every payload block are healthy. (`E`, `X`)
- **2362 — read compatibility ≠ write compatibility.** ZFS feature classes and LTO generation rules both expose operation-specific capability sets in which a retained read path can be broader or different from a write path. (`H/P` inherited, `A`, `E`)
- **2363 — physical reader compatibility ≠ software-format compatibility.** LTO drive/media transduction and ZFS feature interpretation can both gate access to surviving state, but they are different hardware/software mechanisms and no common genealogy is asserted. (`A`, `X`)
- **2364 — controller recognition/admission ≠ pending-write commitment.** Case 131 separates importing disk-resident array configuration from later destaging a surviving H800 TBBU/TNVC; recovering topology does not itself commit dirty cache. (`H/P` inherited, `E`)
- **2365 — access apparatus can be retention infrastructure without containing the retained payload.** A compatible drive, interpreter, controller, boot path, or mapping-recovery substrate can be necessary for future access while storing no complete user-data copy. (`E`)
- **2366 — current-generation availability ≠ legacy-state accessibility.** Case 130 shows that acquiring a newer LTO generation need not preserve access to older cartridges; modernization of apparatus is not monotonic expansion of recoverability. (`H/S` inherited, `E`)
- **2367 — loss of an access relation ≠ physical erasure.** Software downgrade, reader obsolescence, missing controller admission, or lost volatile mapping can remove ordinary service while the material embodiment remains. (`E`, `I`)
- **2368 — restoring an access path can recover service without first rewriting payload.** Reinstalling compatible software, reintroducing a compatible reader/controller, or reconstructing a mapping relation can make surviving state usable again, so current unavailability is weaker than irreversible forgetting. (`E`)
- **2369 — compatibility windows can create migration obligations before media failure.** Case 130 makes the pressure explicit: preservation may require retaining readers or migrating while a viable reader path still exists even when cartridges are currently healthy. (`E`)
- **2370 — compatibility is typed by operation rather than one yes/no property.** `identify`, `read`, `write`, `import read-only`, `import read-write`, `boot`, `recover`, `destage`, and `migrate` can have different capability/admission requirements. (`E`)
- **2371 — access-path state and payload state can fail independently.** A healthy payload can become inaccessible through apparatus loss; conversely, a compatible apparatus can remain available while media, checksums, or payload are corrupt. (`E`, `X`)
- **2372 — machine compatibility ≠ preserved human/procedural meaning.** Restoring a tape drive, controller, mapping layer, or filesystem interpreter establishes a technical access path, not the cultural, linguistic, institutional, or application context needed to understand recovered content. (`I`, `X`)
- **2373 — Flash mapping, ZFS compatibility, LTO generations, and PERC replacement are functional comparisons, not one genealogy.** The synthesis compares a shared recoverability relation while preserving different physical mechanisms, historical vocabularies, and failure models. (`A`, `X`)
- **2374 — related-repository boundary remains explicit.** Broad tape-drive, controller-family, interface-adapter, boot-environment, and format/device genealogy belongs in `computing-archaeology`; Synthesis 23 keeps only the retention-specific cross-case decomposition. (`H/P` project-state record)
'''
    index += '\n' + findings.lstrip('\n')
    index_path.write_text(index, encoding='utf-8')

index_now = index_path.read_text(encoding='utf-8')
for n in range(2359, 2375):
    count = len(re.findall(rf'\*\*{n} —', index_now))
    assert count == 1, f'finding {n} count={count}'
assert readme_link in readme_path.read_text(encoding='utf-8')
assert 'Synthesis 23' in roadmap_path.read_text(encoding='utf-8')
