from pathlib import Path

CASE = Path('cases/44-nvme13-deallocate-sanitize-forgetting.md')
EVIDENCE = Path('evidence/44-nvme12-13-deallocate-sanitize-grounding.md')
ROADMAP = Path('ROADMAP.md')
INDEX = Path('CASE_INDEX.md')

MARKER = '## Earlier device-level prior art — ATA Enhanced Security Erase and reallocated sectors (1996–1998)'
FINDING_MARKER = '- **1898 — ATA Enhanced Security Erase proposal != NVMe Sanitize origin:**'


def replace_once(text, old, new, label):
    if old not in text:
        raise RuntimeError(f'missing anchor in {label}: {old[:120]!r}')
    if text.count(old) != 1:
        raise RuntimeError(f'non-unique anchor in {label}: {old[:120]!r}')
    return text.replace(old, new, 1)


case = CASE.read_text(encoding='utf-8')
if MARKER not in case:
    old_status = (
        '**`grounded`** — bounded to the NVM Express 1.3 interface semantics for Dataset Management `Deallocate` and `Sanitize`, '
        'with NVM Express 1.2.1 `Format NVM` secure-erase semantics used as the immediate prior-version boundary. '
        'TCG Opal 1.0 Revision 1.0 (January 2009) is now used as an earlier storage-security prior-art boundary for media-encryption-key eradication and for the explicit `KeepGlobalRangeKey` counterexample in which a security-provider lifecycle reset occurs without cryptographic erase. '
        'The case asks what the interface means when a host says that a logical range is no longer needed, versus when it requests that prior user data be made unavailable across the NVM subsystem.'
    )
    new_status = (
        '**`grounded`** — bounded to the NVM Express 1.3 interface semantics for Dataset Management `Deallocate` and `Sanitize`, '
        'with NVM Express 1.2.1 `Format NVM` secure-erase semantics used as the immediate prior-version boundary. '
        'The T13 D96156 proposal trail and the ATA/ATAPI-4 revision-18 record (1996–1998) are now used as an earlier device-internal overwrite/reallocated-sector prior-art boundary; '
        'TCG Opal 1.0 Revision 1.0 (January 2009) remains the earlier bounded storage-security witness for media-encryption-key eradication and for the explicit `KeepGlobalRangeKey` non-erasure counterexample. '
        'The case asks what the interface means when a host says that a logical range is no longer needed, versus when it requests that prior user data be made unavailable across the NVM subsystem.'
    )
    case = replace_once(case, old_status, new_status, 'Case 44 status')

    insert_before = '## Earlier storage-security prior art — TCG Opal 1.0 key eradication (2009)\n'
    ata_section = '''## Earlier device-level prior art — ATA Enhanced Security Erase and reallocated sectors (1996–1998)\n\nThe T13 archive records **D96156r0, “Enhanced security erase unit proposal,” submitted October 14, 1996**, followed by r1 on January 14, 1997 and r2 on January 28, 1997. The late ATA/ATAPI-4 working draft, **T13/1153D Revision 18 (August 19, 1998)**, supplies the crucial proposal-to-draft bridge: its revision history states that Revision 9 (February 10, 1997) **added enhanced security erase proposal D96156R2**. T13 separately lists the published project as **INCITS 317-1998 (1153D), ATA/ATAPI-4**, dated August 18, 1998.\n\nHistorical identity must stay exact. The inspected Revision-18 facsimile labels itself an **internal working document** and explicitly says it is not itself the approved standard. Therefore this case uses it as late-draft primary evidence tied to the published 1153D project, while the T13 published-standard index and later maintained Seagate ATA-security documentation supply continuity that Enhanced Security Erase belongs to the ATA/ATAPI-4 feature history. It does **not** silently relabel the inspected draft as the final ANSI text.\n\nRevision 18 §8.31.8 separates two erase modes. In normal mode, `SECURITY ERASE UNIT` writes zeroes to all user-data areas. Enhanced mode is optional; when selected, the device writes predetermined patterns to all user-data areas and explicitly includes **sectors no longer in use because of reallocation**. The command also requires an immediately preceding `SECURITY ERASE PREPARE`; failure to overwrite the data area is one reason for command abort.\n\nThat clause exposes an older hidden-embodiment problem that later Flash/SSD sanitization makes especially visible:\n\n> **host-addressable sequential overwrite != device-internal overwrite reach after defect reallocation.**\n\nA sector can cease to be reachable through ordinary host writes because the drive has remapped its logical designation, while the older physical sector remains part of the historical user-data population. Enhanced Security Erase therefore moves the forgetting operation behind the ordinary write-addressing boundary and makes the device responsible for reaching a class of stale embodiments that normal host writes cannot name.\n\nThis is earlier prior art for **device-internal overwrite coverage of reallocated user-data sectors**. It is not the same thing as NVMe 1.3 Sanitize:\n\n- the ATA evidence here is an overwrite/security-erase relation, not a cryptographic-erase witness;\n- it does not establish NVMe's Block Erase / Crypto Erase / Overwrite action taxonomy;\n- it does not establish NVMe's background-operation status model, reset/power-cycle continuation contract, or `Global Data Erased` state;\n- it does not prove that every non-user-data or implementation-hidden region is covered merely because reallocated sectors are;\n- it does not prove direct ATA → NVMe genealogy.\n\nThe bounded prior-art conclusion is therefore:\n\n> **1996–1998 ATA Enhanced Security Erase blocks any claim that NVMe 1.3 originated the general idea of device-internal whole-user-data forgetting that reaches reallocated stale embodiments.**\n\nBut a second boundary is equally important:\n\n> **earlier overwrite-based secure erase != earlier cryptographic erase.**\n\nThe TCG Opal 2009 evidence below remains necessary for the separate history in which forgetting can be achieved by retiring media-key relations rather than by overwriting every ciphertext-bearing location.\n\n### Engineering reconstruction — address retirement can create a forgetting obligation\n\nThe ATA case adds a useful inverse to Case 14 defect reassignment. Case 14 asks how a logical block designation can survive while a failed physical sector is replaced. The security-erase evidence asks what happens to the **retired physical embodiment** after that successful continuity operation. The same remapping that preserves present service can create a later sanitization obligation toward state no longer reachable through ordinary logical addressing.\n\nSo, at the bounded functional level:\n\n```text\nreassignment preserves logical service\n    -> old embodiment may leave ordinary addressability\n    -> ordinary host overwrite may no longer reach it\n    -> device-internal erase path can assume the forgetting obligation\n```\n\nThis is an engineering reconstruction of the sourced interface relation, not historical T13 vocabulary and not a claim that defect reassignment exists for the purpose of later sanitization.\n\n'''
    case = replace_once(case, insert_before, ata_section + insert_before, 'Case 44 ATA section anchor')

    old_broader = (
        'Media-sanitization vocabulary and cryptographic erasure also predate NVMe 1.3. The TCG Opal 1.0 witness above pushes explicit storage-interface key-eradication / cryptographic-erase semantics back to 2009. '
        'NIST SP 800-88 Rev. 1 was finalized in December 2014 and defines media sanitization as rendering access to target data infeasible for a stated level of effort; its keyword set includes `crypto erase` and `secure erase`.'
    )
    new_broader = (
        'Whole-device secure-erasure mechanisms predate NVMe 1.3 by much more than the existing 2009 cryptographic-erasure witness. '
        'T13 D96156r0 (October 1996) and the ATA/ATAPI-4 Revision-18 history/command text establish an earlier device-internal overwrite path whose enhanced mode reaches reallocated user-data sectors. '
        'That is an overwrite/reachability prior-art floor, not a cryptographic-erasure floor. The TCG Opal 1.0 witness separately pushes explicit storage-interface key-eradication / cryptographic-erase semantics back to 2009. '
        'NIST SP 800-88 Rev. 1 was finalized in December 2014 and defines media sanitization as rendering access to target data infeasible for a stated level of effort; its keyword set includes `crypto erase` and `secure erase`.'
    )
    case = replace_once(case, old_broader, new_broader, 'Case 44 broader prior art')

    claim_anchor = '| Opal `RevertSP` with `KeepGlobalRangeKey=true` can reset/turn off the Locking SP while preserving the Global-range media key and avoiding cryptographic erase for that range | H/P | Opal 1.0 Rev. 1.0 §5.2.3, printed p. 77 |\n'
    claim_rows = (
        '| T13 records D96156r0 `Enhanced security erase unit proposal` on October 14, 1996, with r1/r2 in January 1997 | H/P | official T13 document archive |\n'
        '| ATA/ATAPI-4 Revision 18 records that Revision 9 added D96156R2 and defines optional Enhanced Erase over user-data areas including sectors no longer used due to reallocation | H/P | T13/1153D Revision 18 revision history + §8.31.8; inspected facsimile is a working draft, not silently promoted to final ANSI text |\n'
        '| host-addressable overwrite reaches every stale sector embodiment after drive-internal reassignment | X | contradicted by the Enhanced Security Erase motivation/reallocated-sector coverage boundary |\n'
        '| ATA overwrite-based Enhanced Security Erase established cryptographic erase | X | mechanism is overwrite-based in the bounded source; TCG Opal remains the separate 2009 crypto-erase witness |\n'
    )
    case = replace_once(case, claim_anchor, claim_rows + claim_anchor, 'Case 44 claim ledger')

    source_anchor = '### Primary\n\n'
    ata_sources = (
        '- T13 document archive, **D96156r0/r1/r2, “Enhanced security erase unit proposal”** (October 14, 1996; January 14 and January 28, 1997): <https://www.t13.org/docsearch>. The archive establishes document identity/dates.\n'
        '- T13, **1153D Revision 18, ATA/ATAPI-4**, August 19, 1998, revision history and §8.31.8 `SECURITY ERASE UNIT`; publicly preserved facsimile used for exact late-draft text: <https://ptacts.uspto.gov/ptacts/public-informations/petitions/1554771/download-documents?artifactId=0EWigRzVKg7sPjzD0givwKpcihsaStqqZz6WGAMqZ789VgCRCY9LVrg>.\n'
        '- T13, **Expired Standards** index, listing INCITS 317-1998 (1153D), ATA/ATAPI-4: <https://www.t13.org/standards-expired>.\n'
    )
    case = replace_once(case, source_anchor, source_anchor + ata_sources, 'Case 44 sources')

    old_related = '`tmzncty/computing-archaeology` was searched before writing for `NVMe sanitize`, `secure erase`, `deallocate`, `TRIM`, SSD sanitization, and during this deepening for `cryptographic erase`, `Opal`, `key destruction`, `wrapping key`, and `key escrow`. No dedicated retention/sanitization or key-hierarchy case was found.'
    new_related = '`tmzncty/computing-archaeology` was searched before writing for `NVMe sanitize`, `secure erase`, `deallocate`, `TRIM`, SSD sanitization, and during the later deepenings for `cryptographic erase`, `Opal`, `key destruction`, `wrapping key`, `key escrow`, `ATA secure erase`, and `security erase ATA/ATAPI`. No dedicated retention/sanitization, ATA Secure Erase, or key-hierarchy case was found.'
    case = replace_once(case, old_related, new_related, 'Case 44 related repo')

    CASE.write_text(case, encoding='utf-8')


evidence = EVIDENCE.read_text(encoding='utf-8')
if '### T13 D96156 / ATA/ATAPI-4 Enhanced Security Erase (1996–1998)' not in evidence:
    evidence = replace_once(
        evidence,
        '# Case 44 Grounding — TCG Opal / NVMe Deallocate and Sanitize (2009–2017)',
        '# Case 44 Grounding — ATA / TCG Opal / NVMe Deallocate and Sanitize (1996–2017)',
        'Evidence 44 title',
    )
    old_purpose = 'This record grounds [`../cases/44-nvme13-deallocate-sanitize-forgetting.md`](../cases/44-nvme13-deallocate-sanitize-forgetting.md) in official TCG Opal 1.0 Revision 1.0 plus NVM Express Revision 1.3 / Revision 1.2.1 text, and uses NIST SP 800-88 Rev. 1 (December 2014) as an institutional historical source for the conditions under which cryptographic-key sanitization can support a Cryptographic Erase claim.'
    new_purpose = 'This record grounds [`../cases/44-nvme13-deallocate-sanitize-forgetting.md`](../cases/44-nvme13-deallocate-sanitize-forgetting.md) in the T13 D96156 / ATA/ATAPI-4 Enhanced Security Erase record, official TCG Opal 1.0 Revision 1.0, and NVM Express Revision 1.3 / Revision 1.2.1 text, and uses NIST SP 800-88 Rev. 1 (December 2014) as an institutional historical source for the conditions under which cryptographic-key sanitization can support a Cryptographic Erase claim.'
    evidence = replace_once(evidence, old_purpose, new_purpose, 'Evidence 44 purpose')

    primary_anchor = '### NVM Express Revision 1.3\n'
    ata_primary = '''### T13 D96156 / ATA/ATAPI-4 Enhanced Security Erase (1996–1998)\n\nOfficial T13 archival records inspected:\n\n- **D96156r0, “Enhanced security erase unit proposal,” October 14, 1996**;\n- D96156r1, January 14, 1997;\n- D96156r2, January 28, 1997;\n- **T13/1153D Revision 18, ATA/ATAPI-4, August 19, 1998**;\n- T13 Expired Standards index entry for **INCITS 317-1998 (1153D), ATA/ATAPI-4**, dated August 18, 1998.\n\nArchive/index sources:\n\n- <https://www.t13.org/docsearch>\n- <https://www.t13.org/standards-expired>\n\nLate-draft facsimile used for exact revision-history and command text:\n\n- <https://ptacts.uspto.gov/ptacts/public-informations/petitions/1554771/download-documents?artifactId=0EWigRzVKg7sPjzD0givwKpcihsaStqqZz6WGAMqZ789VgCRCY9LVrg>\n\nSections inspected in Revision 18:\n\n- front matter / document status, which explicitly identifies the file as an internal working document rather than an approved final standard;\n- revision history, where Revision 9 (February 10, 1997) says **“Added enhanced security erase proposal (D96156R2)”**;\n- §8.31.6–§8.31.8, especially `SECURITY ERASE UNIT` prerequisites, abort conditions, and Normal/Enhanced erase descriptions.\n\nEvidence-strength boundary: the T13 archive establishes proposal identity/date and the published 1153D project identity; the inspected exact command wording comes from Revision 18, which must remain labeled a late working draft. The repository therefore does not claim to have visually verified the final ANSI/INCITS publication page-for-page.\n\n'''
    evidence = replace_once(evidence, primary_anchor, ata_primary + primary_anchor, 'Evidence 44 ATA primary')

    claims_anchor = '### Revision 1.3 §6.7 — Dataset Management is advisory\n'
    ata_claims = '''### T13 D96156 / ATA/ATAPI-4 — reallocation creates a hidden-embodiment erase problem\n\nThe official T13 archive dates the first `Enhanced security erase unit proposal` record to October 14, 1996. Revision 18 of the ATA/ATAPI-4 working draft later records that Revision 9 added D96156R2 and contains the resulting `SECURITY ERASE UNIT` semantics.\n\nIn §8.31.8, Normal erase writes zeroes to all user-data areas. Enhanced erase is optional and writes predetermined patterns to all user-data areas; critically, the text says this includes sectors no longer in use because of **reallocation**. The command must be immediately preceded by `SECURITY ERASE PREPARE`, and inability to overwrite the data area is an abort condition.\n\n**Supported historical claim:** by the ATA/ATAPI-4 development record, the standards process explicitly treated ordinary host-visible overwrite reach and reallocated stale-sector reach as different problems and added a device-internal enhanced erase path whose target includes reallocated user-data sectors.\n\n**Engineering consequence:** `logical address retired by reassignment` does not imply `old physical user-data embodiment already forgotten`; a later forgetting operation may need an authority below ordinary host addressing.\n\n**Scope guardrails:**\n\n- `reallocated sectors included` does not prove every implementation-hidden, HPA/DCO, firmware, cache, or non-user-data region is included;\n- overwrite-based ATA Enhanced Erase is not evidence of cryptographic erase;\n- Revision-18 late-draft semantics plus the T13 published-project index do not justify silently calling the inspected facsimile the final ANSI standard;\n- proposal/adoption chronology does not prove invention priority or a direct ATA→NVMe genealogy.\n\n'''
    evidence = replace_once(evidence, claims_anchor, ata_claims + claims_anchor, 'Evidence 44 ATA claims')

    old_broader = 'TCG **Opal 1.0 Revision 1.0**, dated January 27, 2009, now provides the earlier storage-interface witness for media-key eradication and explicit `cryptographic erase` semantics. This moves the repository\'s bounded prior-art line earlier than both NIST SP 800-88 Rev. 1 and NVMe secure-erase/sanitize revisions without making an invention-priority claim.'
    new_broader = 'For overwrite-based whole-user-data erasure, the bounded prior-art line now moves earlier: T13 D96156r0 (October 1996) and the ATA/ATAPI-4 Revision-18 record establish Enhanced Security Erase coverage of reallocated user-data sectors. TCG **Opal 1.0 Revision 1.0**, dated January 27, 2009, remains the earlier storage-interface witness in this case for the **different** media-key-eradication / explicit `cryptographic erase` mechanism class. Neither boundary is an invention-priority claim.'
    evidence = replace_once(evidence, old_broader, new_broader, 'Evidence 44 broader prior art')

    old_related_phrase = 'No dedicated retention/sanitization or key-hierarchy case was found.'
    if old_related_phrase in evidence:
        evidence = evidence.replace(old_related_phrase, 'No dedicated retention/sanitization, ATA Secure Erase, or key-hierarchy case was found.', 1)
    if '`ATA secure erase`' not in evidence:
        evidence += '\n\n## Related-repository recheck — ATA Secure Erase deepening\n\nCurrent `tmzncty/computing-archaeology` searches for `ATA secure erase` and `security erase ATA/ATAPI` returned no dedicated case. Broad ATA security-command genealogy belongs there if developed; this record keeps only the retention-specific boundary between logical reassignment/address reach and device-internal forgetting reach.\n'

    EVIDENCE.write_text(evidence, encoding='utf-8')


roadmap = ROADMAP.read_text(encoding='utf-8')
roadmap_lines = roadmap.splitlines()
for i, line in enumerate(roadmap_lines):
    if 'cases/44-nvme13-deallocate-sanitize-forgetting.md' in line:
        roadmap_lines[i] = '- [x] NVMe Deallocate / Sanitize forgetting boundary, now deepened with ATA Enhanced Security Erase prior art — [`cases/44-nvme13-deallocate-sanitize-forgetting.md`](cases/44-nvme13-deallocate-sanitize-forgetting.md), grounded by [`evidence/44-nvme12-13-deallocate-sanitize-grounding.md`](evidence/44-nvme12-13-deallocate-sanitize-grounding.md): NVMe 1.3 still separates advisory deallocation from subsystem sanitize and operation completion, while T13 D96156 (1996–1997) plus ATA/ATAPI-4 Revision 18 (1998) establish an earlier device-internal overwrite path that explicitly reaches reallocated user-data sectors. TCG Opal 2009 remains the separate cryptographic-erase/key-eradication prior-art floor. This closes only the bounded `ordinary logical overwrite reach vs reallocated stale embodiment vs device-internal forgetting reach` novelty guardrail; final ANSI facsimile verification, complete ATA/SCSI erase genealogy, HPA/DCO evolution, named-device compliance, and fault/forensic validation remain open.'
        break
else:
    raise RuntimeError('ROADMAP Case 44 bullet not found')
ROADMAP.write_text('\n'.join(roadmap_lines) + '\n', encoding='utf-8')


index = INDEX.read_text(encoding='utf-8')
index_lines = index.splitlines()
for i, line in enumerate(index_lines):
    if 'cases/44-nvme13-deallocate-sanitize-forgetting.md' in line:
        index_lines[i] = '| [NVM Express 1.3 Deallocate and Sanitize: Logical Forgetting, Media Sanitization, and Completion State](cases/44-nvme13-deallocate-sanitize-forgetting.md) | **grounded** | advisory logical-range deallocation + controller allocation/currentness state + subsystem-wide sanitize + Block/Crypto/Overwrite mechanisms + retained progress/result state + earlier ATA device-internal overwrite of reallocated sectors + media-key/wrapping-key recoverability | separate logical deallocation from media erasure; ordinary host overwrite reach from stale/reallocated embodiment reach; request completion from operation completion; overwrite-based erase from crypto erase; and local key retirement from decryptability closure | [1996–2017 ATA/Opal/NIST/NVMe grounding](evidence/44-nvme12-13-deallocate-sanitize-grounding.md); T13 D96156/ATA-4 supplies earlier reallocated-sector overwrite prior art, Opal 1.0 supplies the separate key-eradication floor, and NIST adds key-copy/wrapping/escrow conditions; Case 47 retains independent raw-Flash validation; final ANSI facsimile, full ATA/SCSI genealogy, named-device compliance, and application/HSM/KMS hierarchies remain separate work |'
        break
else:
    raise RuntimeError('CASE_INDEX Case 44 row not found')
index = '\n'.join(index_lines)

if FINDING_MARKER not in index:
    if '- **1897 — related-repository boundary:**' not in index:
        raise RuntimeError('CASE_INDEX finding 1897 anchor not found')
    findings = '''\n\n## Case 44 deepening — ATA Enhanced Security Erase / hidden-embodiment prior-art findings\n\n- **1898 — ATA Enhanced Security Erase proposal != NVMe Sanitize origin:** T13 archives D96156r0 on October 14, 1996, and ATA/ATAPI-4 Revision 18 records D96156R2 as added in Revision 9, long before NVMe 1.3. (`H/P`, `X`)\n- **1899 — proposal record != approved-standard identity:** D96156 and the inspected 1153D Revision-18 facsimile establish committee chronology and late-draft semantics; Revision 18 explicitly calls itself an internal working document, while T13 separately indexes INCITS 317-1998 as the published ATA/ATAPI-4 project. (`H/P`, `X`)\n- **1900 — host-addressable overwrite != stale reallocated-sector reach:** the Enhanced Erase clause explicitly includes sectors no longer in use due to reallocation, showing why ordinary logical writes are not a complete inventory of historical physical user-data embodiments. (`H/P`, `E`)\n- **1901 — successful reassignment != retirement of the old payload embodiment:** Case 14 can preserve an LBA by replacing a defective sector while Case 44's ATA evidence shows the retired sector can remain a later erase target. (`E`, `A`)\n- **1902 — device-internal erase authority != ordinary host write authority:** Enhanced Security Erase moves the forgetting operation behind the normal addressing path precisely for a class of sectors the host can no longer select through ordinary writes. (`H/P`, `E`)\n- **1903 — reallocated-sector coverage != universal hidden-region coverage:** the bounded ATA clause supports reallocated user-data sectors; it does not by itself prove HPA/DCO, firmware, cache, non-user-data, or every vendor-private region is covered. (`H/P`, `X`)\n- **1904 — ATA Enhanced Security Erase != cryptographic erase:** the 1996–1998 bounded mechanism is overwrite-based; TCG Opal 2009 remains the separate earlier witness here for media-key eradication / cryptographic erase. (`H/P`, `X`)\n- **1905 — one forgetting objective != one physical transformation:** ATA overwrite, Opal key eradication, and NVMe Block/Crypto/Overwrite sanitize paths can all target old-data inaccessibility while changing different retained relations. (`E`, `A`)\n- **1906 — earlier ATA secure-erase prior art != proven ATA→NVMe genealogy:** chronological/mechanism precedence blocks an NVMe-origin claim but does not establish direct committee, personnel, text, or implementation descent. (`H/P`, `A`, `X`)\n- **1907 — late-draft clause continuity != named-device compliance:** a standards-development contract does not prove that a particular HDD/SSD actually overwrites every required stale embodiment; Case 47 remains the independent implementation/forensics counterexample class. (`H/P`, `A`, `X`)\n- **1908 — forgetting scope can be larger than current addressability before Flash FTLs:** the ATA reallocation case shows the logical/current address set was already insufficient as an erasure inventory in magnetic-disk practice; Flash indirection intensifies rather than originates that relation. (`E`, `A`)\n- **1909 — related-repository boundary:** current `computing-archaeology` searches for `ATA secure erase` and `security erase ATA/ATAPI` found no dedicated case; broad ATA security-command genealogy belongs there if developed, while Case 44 keeps the retention-specific address-reach/forgetting-reach boundary. (`H/P` project-state record)'''
    index += findings
INDEX.write_text(index.rstrip() + '\n', encoding='utf-8')

for p in (CASE, EVIDENCE, ROADMAP, INDEX):
    lines = p.read_text(encoding='utf-8').splitlines()
    p.write_text('\n'.join(line.rstrip() for line in lines) + '\n', encoding='utf-8')

print('Case 44 ATA prior-art integration complete')
