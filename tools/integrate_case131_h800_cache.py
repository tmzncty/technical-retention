from pathlib import Path
import re

case = Path('cases/131-dell-perc-foreign-configuration-controller-replacement.md')
evidence = Path('evidence/131-dell-perc-2007-2011-foreign-configuration-grounding.md')
roadmap = Path('ROADMAP.md')
index = Path('CASE_INDEX.md')

c = case.read_text()
old = '- **Object / system:** Dell PowerEdge RAID Controller (PERC), bounded historically by PERC 6/i firmware released **20 November 2007** and PERC 6/E firmware released **6 December 2011**, with later Dell management documentation used only as continuity / operational witnesses.'
new = '- **Object / system:** Dell PowerEdge RAID Controller (PERC), bounded historically by PERC 6/i firmware released **20 November 2007**, the PERC H700/H800 documentation set revised **March 2011**, and PERC 6/E firmware released **6 December 2011**, with later Dell management documentation used only as continuity / operational witnesses.'
assert old in c
c = c.replace(old, new, 1)

old = "- **Retention question:** what array-defining state can remain on the member disks when the controller's current configuration disappears or no longer admits those disks, and what separate controller-local state can still prevent transparent recovery?"
new = "- **Retention question:** what array-defining state can remain on the member disks when the controller's current configuration disappears or no longer admits those disks, and under what bounded hardware design can pending controller-cache state itself survive a controller-card failure and move to a replacement controller?"
assert old in c
c = c.replace(old, new, 1)

marker = '### H/P — the 2011 PERC 6/E release separates foreign configuration from preserved dirty write cache\n'
assert marker in c
insert = '''### H/P — March 2011 PERC H800 makes a transportable failed-controller cache path explicit

Dell's _PERC H700 and H800 Technical Guide_, Revision 3 (**March 2011**), distinguishes the H800 from the H700 at the cache-carrier layer. The H800 cache options include a **512 MB transportable battery backup unit (TBBU)** and transportable 512 MB / 1 GB nonvolatile-cache options. Section 4.5.7.1 defines the TBBU as a cache-memory module with an integrated battery pack that can be transported into a new controller. Section 4.5.1 separately states that the nonvolatile-cache option uses battery energy to transfer cache contents to flash during a power cycle, with the guide specifying retention for up to ten years.

The Dell-authored _PERC H700 and H800 User's Guide_, March 2011 Rev. A02, makes the controller-failure use case explicit. Its `Cache Data Recovery` section says that after a **PERC H800 card failure** the complete TBBU/TNVC module can be moved to a new PERC H800 without putting preserved cache data at risk. Its transfer procedure further constrains the path: the replacement is another PERC H800 with no prior configuration, the original storage enclosures are reconnected, and the replacement controller then flushes the retained cache to the virtual disks.

The current Dell H800 support page still indexes this Dell User's Guide; the exact March-2011 page text used here survives on third-party mirrors because Dell's present support front end did not yield a stable directly fetchable copy during this research round. The controller-family design claim does **not** depend solely on that mirror: Dell's own still-hosted March-2011 Technical Guide independently establishes the transportable H800 cache module and the cache-to-flash power-loss path.

This changes the earlier open boundary in one important but narrow way:

> **controller card failure ≠ mandatory loss of controller-local dirty state, if the retained cache carrier itself survives and the documented H800 transplant conditions are met.**

It also requires a finer location distinction:

> **controller-local state ≠ state physically inseparable from the controller card.**

For the H800 TBBU/TNVC path, pending writes are controller-local in the protocol/ownership sense but can inhabit a removable state carrier that outlives the failed controller card.

The evidence does **not** license a universal PERC claim. It does not show that every H700/H800 cache option is transportable, that a destroyed/corrupt TBBU/TNVC can be recovered, that arbitrary later PERC generations accept the module, or that cache already committed to member disks is still only cache-resident.

'''
c = c.replace(marker, insert + marker, 1)

old = '''Most importantly, the 2011 preserved-cache evidence belongs to the **same controller retaining cache across missing-disk episodes**. The inspected sources do not prove that dirty cache trapped on a failed old controller is magically transferred into a replacement controller.

Therefore:

> **foreign-configuration recovery after controller replacement ≠ recovery of dirty cache from the failed controller.**

That failed-controller dirty-cache question remains open.'''
new = '''The PERC 6/E preserved-cache evidence still belongs to the **same controller retaining cache across missing-disk episodes** and, by itself, does not prove failed-card cache transfer. The March-2011 H800 material supplies a separate bounded counterexample: if the TBBU/TNVC survives, Dell documents moving that cache carrier to a replacement H800 and then flushing the retained cache to the virtual disks.

Therefore the stronger boundary is now:

> **foreign-configuration recovery after controller replacement ≠ failed-controller dirty-cache recovery by itself.**

but also:

> **failed controller card ≠ failed retained-cache carrier.**

The H800 path composes two independently retained state transports: member disks can carry array configuration/payload embodiments, while TBBU/TNVC can carry pending write state. Recovery completeness can depend on both. Failed or corrupt cache modules, nontransportable controller designs, cross-generation compatibility, and independent fault injection remain open.'''
assert old in c
c = c.replace(old, new, 1)

source_marker = '### Later Dell operational / continuity witnesses\n'
assert source_marker in c
source_insert = '''### PERC H800 March-2011 cache-portability deepening

3. Dell, **Dell PERC H700 and H800 Technical Guide**, Revision 3, March 2011. Dell-hosted primary source. H800 overview lists transportable TBBU/TNVC cache options; §4.5.1 distinguishes battery-held cache from NV-cache transfer to flash; §4.5.7.1 defines the TBBU as a cache module that can move with its battery to a new controller.  
   https://i.dell.com/sites/csdocuments/shared-content_data-sheets_documents/en/perc-technical-guidebook.pdf

4. Dell, **PowerEdge RAID Controller H700 and H800 User's Guide**, March 2011 Rev. A02, especially `Cache Data Recovery` (p. 37) and `Transferring a TBBU or TNVC Between PERC H800 Cards` (p. 63). Dell's current H800 support page continues to index the User's Guide; exact page text was checked against a surviving Dell-authored mirror.  
   https://www.dell.com/support/product-details/en-us/product/poweredge-rc-h800/resources/manuals

'''
c = c.replace(source_marker, source_insert + source_marker, 1)
case.write_text(c)

e = evidence.read_text()
marker = '## Rejected / unsupported claims\n'
assert marker in e
add = '''## March 2011 H800 transportable-cache deepening

### Source F — Dell PERC H700 and H800 Technical Guide, Revision 3

**Type:** `H/P` — Dell-hosted vendor primary.  
**Revision:** **March 2011**.  
**URL:** https://i.dell.com/sites/csdocuments/shared-content_data-sheets_documents/en/perc-technical-guidebook.pdf

Directly inspected points:

- the H800 overview lists a standard 512 MB **transportable battery backup unit (TBBU)** and transportable 512 MB / 1 GB nonvolatile-cache options;
- §4.5.1 distinguishes battery-held cache from the NV-cache path in which battery energy transfers cache contents to flash on a power cycle, with retention stated as up to ten years;
- §4.5.7.1 defines the TBBU as a cache-memory module with an integrated battery pack that enables moving the cache module with its battery into a new controller;
- the same section describes H700 BBU separately, blocking an automatic projection of H800 transportability onto every PERC cache design.

### Source G — Dell PERC H700 and H800 User's Guide, March 2011 Rev. A02

**Type:** `H/P*` — Dell-authored primary manual, with a preservation/provenance caveat.  
**Revision:** **March 2011, Rev. A02**.  
**Dell support index:** https://www.dell.com/support/product-details/en-us/product/poweredge-rc-h800/resources/manuals  
**Surviving page-text mirrors checked:**  
- https://www.manualshelf.com/manual/dell/poweredge-raid-controller-h700/instruction-manual-english.html  
- https://dell.manymanuals.com/computer-hardware/poweredge-raid-controller-h800/user-manual-11966/37  
- https://dell.manymanuals.com/computer-hardware/poweredge-raid-controller-h800/user-manual-11966/63

The current Dell support page still indexes the User's Guide but did not expose a stable directly fetchable copy in this research round. The surviving Dell-authored manual text records:

- `Cache Data Recovery` (p. 37): after a PERC H800 card failure, the complete TBBU/TNVC can be transferred to a new PERC H800 without putting preserved cache data at risk;
- p. 63: if the controller fails after a power failure, the TBBU/TNVC can be moved to a replacement controller; the replacement should have no prior configuration; after original storage enclosures are reconnected, the replacement controller flushes the retained cache to the virtual disks.

This is stronger than merely inferring portability from the module name. It directly documents a failed-controller recovery procedure, but only for the bounded H800 path.

### Claim-ledger additions

| ID | Claim | Label | Evidence | Strength / limit |
| --- | --- | --- | --- | --- |
| G-131.17 | By March 2011 Dell documented PERC H800 TBBU/TNVC cache options as transportable state carriers. | `H/P` | F | strong Dell-hosted product record |
| G-131.18 | H800 TBBU transportability means controller-local cache state need not be physically inseparable from the controller card. | `E` | F | bounded reconstruction |
| G-131.19 | The H800 nonvolatile-cache path can transfer cached data to flash during a power cycle rather than merely holding DRAM alive continuously. | `H/P` | F | direct Dell-hosted mechanism statement |
| G-131.20 | The March-2011 H800 User's Guide explicitly documents moving a surviving TBBU/TNVC to a replacement H800 after controller-card failure. | `H/P*` | G | Dell-authored manual; mirrored page text |
| G-131.21 | The documented replacement path requires another PERC H800 with no prior configuration and reconnecting the original storage enclosures before cache flush. | `H/P*` | G | bounded procedure, not universal migration |
| G-131.22 | Controller-card failure need not imply dirty-cache loss when the separate retained-cache carrier survives and the documented transplant path remains admissible. | `E` | F, G | bounded to H800 TBBU/TNVC |
| G-131.23 | Transportable cache survival is not the same event as commitment of those pending writes to member disks; the replacement controller still has to flush them. | `H/P*`, `E` | G | direct sequence + reconstruction |
| G-131.24 | Foreign-configuration import and cache-module transfer are separate recovery relations even when one recovery episode may require both disk-resident configuration and pending cache state. | `E` | A-E, F-G | cross-source decomposition |
| G-131.25 | H800 transportability does not establish a universal PERC, cross-generation, or cross-vendor cache-transplant contract. | `X` | F, G | anti-overclaim |
| G-131.26 | March 2011 is a directly inspected Dell product-documentation floor for this H800 portability path, not an invention-priority claim for transportable RAID cache. | `X` | F, G | chronology guardrail |

'''
e = e.replace(marker, add + marker, 1)
old = '- "Controller replacement preserves every dirty write that was on the failed controller."'
new = '- "Every PERC controller replacement preserves every dirty write that was on the failed controller."\n- "The H800 TBBU/TNVC recovery path works after destruction, loss, or corruption of the cache module itself."\n- "A PERC H800 TBBU/TNVC can be transplanted into arbitrary later PERC generations or third-party controllers."'
assert old in e
e = e.replace(old, new, 1)
evidence.write_text(e)

r = roadmap.read_text()
old = '- [ ] **controller failure** — substantially advanced at the RAID configuration/admissibility layer by Case 131: Dell PERC foreign configuration can survive on member disks and be imported after controller replacement, while controller-local uncommitted write cache remains a separate failure domain. Still open: failed-controller dirty-cache recovery, controller-NVRAM corruption, cross-generation/vendor metadata compatibility, encrypted-key loss, and fault-injection evidence.'
new = "- [ ] **controller failure** — substantially advanced at the RAID configuration/admissibility layer by Case 131 and now partially at the failed-controller dirty-cache layer: Dell's March-2011 PERC H800 documentation makes TBBU/TNVC a transportable retained-cache carrier that can be moved to a replacement H800 and flushed to the virtual disks, while member disks separately carry foreign configuration/payload embodiments. This closes only the bounded **controller card fails but the H800 retained-cache module survives and remains admissible** path. Still open: failed/corrupt/nontransportable cache modules, controller-NVRAM corruption, cross-generation/vendor metadata compatibility, encrypted-key loss, and independent fault injection."
assert old in r
r = r.replace(old, new, 1)
roadmap.write_text(r)

i = index.read_text()
old = '- **2341 — Controller replacement recovery ≠ failed-controller dirty-cache recovery.** The inspected 2011 source proves preserved cache on the controller experiencing missing disks, not transfer of dirty cache from a dead controller into its replacement. (`X`, `E`)'
new = '- **2341 — PERC 6/E foreign-config evidence ≠ failed-controller dirty-cache recovery.** The December-2011 PERC 6/E source proves preserved cache on the same controller during missing-disk episodes; it does not by itself establish card-failure cache transplant. The March-2011 H800 deepening below separately grounds a TBBU/TNVC transplant path. (`H/P`, `X`, `E`)'
assert old in i
i = i.replace(old, new, 1)
assert '**2347' not in i
i = i.rstrip() + '''

## Case 131 deepening — PERC H800 transportable retained-cache findings

- **2347 — controller-local state ≠ state physically inseparable from the controller card.** Dell's March-2011 H800 TBBU is a cache-memory module with integrated battery explicitly designed to move into a new controller. (`H/P`, `E`)
- **2348 — controller-card failure ≠ retained-cache-carrier failure.** The H800 User's Guide documents a failed-card recovery path in which the TBBU/TNVC survives and is transferred to a replacement H800. (`H/P*`, `E`)
- **2349 — failed-controller dirty-cache recovery ≠ automatic controller replacement.** The bounded procedure requires a surviving TBBU/TNVC, another PERC H800 with no prior configuration, and reconnection of the original storage enclosures. (`H/P*`)
- **2350 — transportable cache survival ≠ member-disk commitment.** After transplant, the replacement controller still flushes preserved cache to the virtual disks; survival of pending state and completion of its destage obligation are distinct events. (`H/P*`, `E`)
- **2351 — foreign configuration transport ≠ dirty-cache transport.** Member disks can carry array-definition state while TBBU/TNVC carries uncommitted writes; one recovery episode may need both independently retained state carriers. (`H/P`, `H/P*`, `E`)
- **2352 — power-loss retention mechanism ≠ controller-failure portability relation.** NV cache's cache-to-flash transfer and TBBU/TNVC's physical portability answer different failure boundaries even when combined in one controller family. (`H/P`, `E`)
- **2353 — battery-backed retention horizon ≠ flash-backed retention horizon.** Dell's Technical Guide gives battery-held cache a guaranteed 24-hour window (typically longer) while its NV-cache path states up to ten years in flash; they are not one retention contract. (`H/P`)
- **2354 — removable retained cache ≠ portable across arbitrary controller generations.** The documented transplant target is another PERC H800, so H800 portability does not establish cross-generation or cross-vendor admissibility. (`H/P*`, `X`)
- **2355 — failed controller ≠ erased pending operation.** A write already acknowledged into write-back cache can survive the controller card that accepted it if the separate retained-cache carrier survives; its future significance remains an obligation to destage, not merely a historical trace. (`E`)
- **2356 — pending-write carrier survival ≠ payload-integrity proof.** A surviving TBBU/TNVC does not establish that member disks, array topology, or every cache bit are otherwise healthy; configuration admission and later integrity checks remain distinct. (`E`, `X`)
- **2357 — March-2011 H800 recovery documentation ≠ invention priority for transportable RAID cache.** It is a directly inspected Dell product-documentation floor; earlier RAID-cache modules and MegaRAID genealogy remain open. (`H/P`, `X`)
- **2358 — related-repository boundary remains unchanged.** A fresh `tmzncty/computing-archaeology` search found no dedicated PERC H800/TBBU/TNVC controller-cache case to reuse; broad RAID-controller/cache-module genealogy belongs there, while this deepening keeps only the retention/failure-boundary result. (`H/P` project-state record)
'''
nums = re.findall(r'\*\*(\d+)\s+—', i)
dups = sorted({n for n in nums if nums.count(n) > 1})
assert not dups, dups
index.write_text(i)
