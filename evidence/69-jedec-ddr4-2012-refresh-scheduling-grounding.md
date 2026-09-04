# Case 69 grounding record — JEDEC DDR4 refresh scheduling, 2010–2013

## Scope

This record grounds [`../cases/69-jedec-ddr4-refresh-postponement-pullin.md`](../cases/69-jedec-ddr4-refresh-postponement-pullin.md).

The bounded question is not `how does all DDR4 refresh work?` It is:

> What primary evidence establishes that ordinary DDR4 retention refresh can be postponed or pulled in within explicit bounds, and how do 1x/2x/4x Fine Granularity Refresh modes preserve a retention-safe accounting relation across rate and Self Refresh transitions?

## Source A — JEDEC JESD79-4, September 2012

**Type:** `H/P`, normative standard.

**Artifact:** JEDEC Solid State Technology Association, `JESD79-4: DDR4 SDRAM`, September 2012.

**Inspected copy:** JEDEC-authored PDF mirrored by Texas Instruments E2E:
<https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/196/JESD79_2D00_4.pdf>

The cover/copyright pages identify the document as JEDEC Standard No. 79-4, DDR4 SDRAM, September 2012. The mirror is not treated as a separate TI standard or a claim of TI authorship.

### §4.26 / printed p. 123 — ordinary REF scheduling

Direct inspection establishes:

- `REF` is used during normal operation and is nonpersistent, so it must be issued each time refresh is required;
- refresh addresses are generated internally once `REF` begins;
- refresh cycles are required at an **average** interval `tREFI`;
- 1x permits at most 8 postponed refresh commands, with a maximum surrounding-command gap of `9 × tREFI`;
- 2x/4x scale the postponed limits to 16/32 and maximum gaps to `17 × tREFI2` / `33 × tREFI4`;
- up to 8/16/32 commands may be pulled in and each allowed pulled-in command reduces one later regular command requirement;
- additional pull-ins beyond the specified cap do not continue buying later exemptions.

**Supported relations:**

- `nominal tREFI ≠ exact per-command timestamp`;
- `bounded postponement ≠ canceled maintenance`;
- `pull-in ≠ unlimited future credit`.

### §4.9.1–4.9.2 / printed p. 35 — FGR mode vocabulary

Direct inspection establishes:

- MR3 selects Fixed 1x, Fixed 2x, Fixed 4x, enable-on-the-fly 2x, or enable-on-the-fly 4x;
- in 2x, refresh-command frequency is doubled relative to base while a distinct `tRFC2` applies;
- in 4x, frequency is quadrupled while a distinct `tRFC4` applies;
- on-the-fly modes allow the command to select between the permitted rate pairs.

The case therefore treats FGR as a **frequency / per-command-cycle-time composition**, not a one-dimensional `more refresh` scale.

### §4.9.3–4.9.4 / printed p. 36 — rate-change and temperature constraints

Direct inspection establishes:

- new `tREFI` / `tRFC` timing applies from a rate change;
- an even number of `REF2x` commands is required in the specified 2x transition/grouping cases;
- a multiple of four `REF4x` commands is required in the specified 4x cases;
- the standard warns that data retention cannot be guaranteed if these conditions are not satisfied;
- Temperature Controlled Refresh in this revision is allowed only in normal Fixed 1x; other FGR modes require it disabled.

**Supported relation:** a mode-setting change does not erase the relevance of recent refresh sequence history.

### §4.9.5 / printed p. 37 — Self Refresh boundary

Direct inspection establishes:

- Self Refresh may be entered from 1x/2x/4x without a pre-entry restriction on how many relevant FGR commands have already occurred;
- on exit, incomplete 2x/4x grouping can require extra refresh command(s);
- those catch-up commands are not counted in the average-`tREFI` calculation.

**Supported relation:** Self Refresh can preserve payload while leaving a bounded externally discharged maintenance obligation at exit.

## Source B — IBM `Elastic Refresh`, MICRO 2010

**Type:** `H/S`, institutional record of a peer-reviewed research paper; used for prior-art boundary, not as the DDR4 normative source.

IBM Research record:
<https://research.ibm.com/publications/elastic-refresh-techniques-to-mitigate-refresh-penalties-in-high-density-memory>

The abstract states that then-current methods did not fully exploit DRAM flexibility to **postpone** refresh and that the proposed Elastic Refresh mechanisms exploit the dynamic range allowed by JEDEC DDRx SDRAM specifications.

This blocks the claim:

> `DDR4 2012 invented the general idea of postponable refresh scheduling`.

The case makes only the narrower claim about the exact DDR4 composition visible in JESD79-4.

## Source C — IBM/Cornell FGR analysis, ISCA 2013

**Type:** `H/S`, institutional record of peer-reviewed analysis.

IBM Research record:
<https://research.ibm.com/publications/understanding-and-mitigating-refresh-overheads-in-high-density-ddr4-dram-systems>

The abstract describes FGR as a feature recently announced in JEDEC's DDR4 specification, explicitly characterizes it as a trade-off between refresh latency and refresh frequency, and reports that no one mode fits every workload.

This source is used to support an engineering boundary, not to substitute for the standard:

- shorter `tRFC` does not imply universally lower system-level refresh cost;
- FGR is not IBM's invention claim in this paper;
- workload choice among modes is a later policy layer over the JEDEC contract.

## Claim ledger

| Claim | Status | Evidence |
| --- | --- | --- |
| JESD79-4 uses average `tREFI` and permits bounded postponement/pull-in | supported `H/P` | Source A §4.26 |
| 1x allows 8 postponed / 8 pulled-in commands and max `9 × tREFI` gap | supported `H/P` | Source A §4.26 |
| 2x/4x use 16/32 limits and `17 × tREFI2` / `33 × tREFI4` gaps | supported `H/P` | Source A §4.26 |
| FGR couples command frequency to distinct `tRFC` values | supported `H/P` | Source A §§4.9.1–4.9.2 |
| FGR rate change is unconstrained | rejected `X` | Source A §4.9.3 |
| Self Refresh erases all prior FGR schedule obligations | rejected `X` | Source A §4.9.5 |
| non-1x FGR freely composes with Temperature Controlled Refresh in 2012 | rejected `X` | Source A §4.9.4 |
| exact controller implementation uses a JEDEC-defined `debt counter` | unsupported `X` | representation is not prescribed by inspected clauses |
| some schedule/accounting state must be retained or derivable | engineering reconstruction `E` | follows from finite postpone/pull-in and transition constraints |
| DDR4 invented postponable refresh | rejected `X` | Source B predates DDR4 standard and cites JEDEC DDRx flexibility |
| FGR has one universally best mode | rejected `X` | Source C |

## Historical / engineering boundary

The following are JEDEC historical/normative facts:

- the exact 1x/2x/4x modes and command constraints;
- bounded postponement and pull-in;
- maximum gaps;
- rate-transition grouping requirements;
- the bounded 2012 TCR/FGR compatibility rule;
- Self Refresh exit catch-up requirements.

The following are project engineering vocabulary:

- `maintenance debt` / `maintenance credit`;
- `schedule-control state`;
- `temporal scheduling elasticity`;
- describing pull-in as `pre-paying` maintenance.

These phrases summarize the relation but must not be attributed to JEDEC actors.

## What this evidence does not establish

It does **not** establish:

- a full JEDEC revision-by-revision genealogy before or after September 2012;
- the exact hardware counter/register structure of any memory controller;
- compliance of a named DIMM/controller implementation;
- empirical failure thresholds after intentionally violating the specification;
- that 1x/2x/4x FGR changes the underlying cell-retention physics;
- that FGR universally improves performance, energy, or reliability;
- that later DDR4/DDR5 temperature or per-bank refresh rules remain identical to the 2012 text.

## Related-repository check

`tmzncty/computing-archaeology` was searched before this slice for a dedicated `Fine Granularity Refresh` case; no matching case was found. A future broad standards chronology should be routed there, while `technical-retention` keeps this bounded maintenance-accounting comparison.

## Grounding decision

**`grounded`** for the bounded 2012 DDR4 scheduling claim.

Reason: the central numeric and sequencing claims come directly from an inspected JEDEC standard artifact, and independent IBM research records supply both earlier postponement prior art and contemporaneous FGR engineering interpretation. The unresolved gaps concern later genealogy, exact controller implementation, and empirical compliance, not the bounded standard-level mechanism.
