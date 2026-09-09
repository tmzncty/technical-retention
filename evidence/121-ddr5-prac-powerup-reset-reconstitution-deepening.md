# Case 121 Deepening — DDR5 PRAC Power-Up / System-Reset Reconstitution

## Scope

This note deepens [`../cases/121-ddr5-prac-activation-counter-initialization.md`](../cases/121-ddr5-prac-activation-counter-initialization.md) at one narrow boundary:

> What happens to the *authority* of PRAC activation-counter state across a reset or power-up boundary, and what must be re-established before the device may rely on those counters again?

The purpose is not to write a general DDR5 reset history. It is to separate four relations that are easy to collapse:

1. physical survival of activation-counter cells;
2. host-visible PRAC enable state;
3. host-visible ACI-completion/readiness evidence;
4. the protocol authority to use the counters for activation tracking and Alert Back-Off (ABO).

The bounded result is that a reset can invalidate readiness/authority even when the inspected product text does not establish physical erasure of the counter cells, while a later Micron patent disclosure treats power-up as a condition in which counter bits may be unknown and therefore require reinitialization.

## Source custody and evidence confidence

### Micron DDR5 SDRAM Product Core Data Sheet, Rev. E (11/2024)

The manufacturer-authored Micron core data sheet is currently inspectable through an Avnet-hosted PDF mirror:

- Micron Technology, *DDR5 SDRAM Product Core Data Sheet*, Rev. E, 11/2024, section `Per Row Activation Counting` / MR70.
- Mirror: <https://www.avnet.com/wcm/connect/dacdfea7-999f-4ee0-b514-6f9e0bf68c6d/ddr5-sdram-core.pdf?MOD=AJPERES>

This pass uses the indexed PDF text rather than claiming a fresh Micron-hosted facsimile custody chain. The source is still manufacturer-authored product documentation; the hosting/provenance limitation is recorded instead of silently treating the mirror as a different source family.

### US20250316301A1, Micron Technology

- Micron Technology, Inc., `Apparatuses and methods for activation counter initialization`, US20250316301A1, filed 21 March 2025, published 9 October 2025.
- Public record: <https://patents.justia.com/patent/20250316301>

This is a patent disclosure, not a normative DDR5 product contract and not proof that every disclosed embodiment shipped. It is used only to deepen the power-up/reinitialization mechanism boundary already visible in the product documentation.

## Historical record

### November 2024 product contract: system reset clears PRAC readiness evidence

Micron Rev. E already establishes the ordinary PRAC/ACI handoff used in the main Case 121 record:

- PRAC is optional and disabled by default in the bounded product contract;
- after the host enables PRAC, a full-array ACI is required;
- activation tracking and ABO are withheld until ACI is complete;
- completion is exposed through MR70 `OP[3]`;
- entering ACI again clears that completion indication until initialization finishes.

The same product text adds the reset boundary needed here: a system reset that disables PRAC also resets MR70 `OP[3]` to zero.

This establishes a product-level fact about **control/readiness state**. It does **not** say that system reset physically erases every activation-counter cell or proves what analog values remain in those cells immediately after reset.

### October 2025 patent disclosure: power-up can make counter values unknown

Micron's later ACI patent application describes embodiments in which activation-counter bits may be in an unknown state at power-up or after DRAM refresh requirements have been violated. The disclosed response is initialization to a known state before the counters are relied upon. The application also repeats the enable → full-array ACI → completion → counting/ABO sequence and the system-reset clearing of ACI-completion status.

This provides a primary public mechanism witness for the stronger **power-up reconstitution** relation, but it must remain source-typed correctly:

> product reset semantics ≠ patent embodiment ≠ universal JEDEC rule.

The patent can support an engineering explanation of why reinitialization is useful. It cannot be silently substituted for an inspected normative JESD79-5C reset clause or for cross-vendor product behavior.

## Engineering reconstruction

### Readiness invalidation ≠ demonstrated physical erasure

The product contract clears ACI completion when system reset disables PRAC. That is enough to show that the old `ready` relation is not allowed to survive transparently across that transition.

It is not enough to establish what happened to the underlying counter-cell charge.

Therefore:

> **ACI-complete cleared ≠ activation-counter cells physically erased.**

and:

> **possible physical survival ≠ post-reset protocol authority.**

A retained embodiment can outlive the permission to trust it.

### Reconstitution is a protocol path, not recovery of old history

The bounded restart path is better represented as:

```text
pre-reset PRAC-active regime
    -> system reset disables PRAC and clears ACI-complete evidence
    -> host enables PRAC again
    -> full-array ACI establishes known counter values
    -> ACI completion becomes true
    -> activation tracking / ABO may resume
```

ACI therefore creates a new trusted starting condition. It does not reconstruct the precise pre-reset activation-count history.

> **counter reinitialization ≠ counter-history recovery.**

The previous per-row counts may have been useful while the old powered/refresh regime was current; the protocol can deliberately stop treating them as authoritative after the regime boundary.

### Power-up unknown-state handling ≠ a durable checkpoint contract

The patent disclosure is especially useful as a negative boundary. It does not describe preserving every activation count in nonvolatile storage and replaying it after power returns. Instead, it permits the counter state to be unknown and restores a known initial condition before reliance.

That supports the bounded reconstruction:

> **PRAC activation-count state has a regime-bounded authority horizon in the inspected evidence; no cross-power durable-checkpoint guarantee is established.**

This does not mean the counters are useless or transient in an arbitrary sense. Within a valid powered and refreshed regime, their accumulated values are precisely what drives future disturbance-protection decisions.

### Reset of protection state ≠ reset of payload semantics

The product statement about system reset is specifically about disabling PRAC and clearing ACI-completion state. It must not be inflated into a claim that system reset itself physically erases user payload.

Separately, the ordinary ACI contract warns that pre-existing array data need not be preserved during ACI. Those are different transitions:

- **system reset:** invalidates PRAC enable/readiness relations in the bounded product text;
- **ACI:** establishes counter state and is not promised to preserve previously written main-array data;
- **refresh violation / power-up patent scenario:** may leave counter state unknown and can trigger the need for ACI.

Keeping these transitions separate prevents `reset`, `power loss`, `refresh violation`, and `ACI` from becoming one generic forgetting event.

### Reinitialization can be safer than retaining stale authority

A system that retained arbitrary counter bits across a regime boundary but continued to treat them as trustworthy would have a worse epistemic problem than one that explicitly clears readiness and reinitializes before use.

The engineering lesson is narrow:

> **forgetting the authority of maintenance metadata can preserve the correctness of later maintenance decisions.**

This is not a claim that every reset should erase maintenance history. It is specific to a state whose intended role can be re-established before the system relies on it again.

## Functional analogy — bounded

### Case 09: refresh-row enumerator

Case 09's bounded TI refresh counter can be initialized on power-on and then cyclically enumerates rows. Case 121's PRAC counters summarize per-row activation pressure and require ACI before they become trusted.

The functional similarity is that both are DRAM maintenance-control states that can be **reconstituted by initialization rather than treated as durable historical checkpoints**.

The mechanisms and meanings remain different:

> cyclic refresh-row phase ≠ per-row accumulated disturbance-pressure summary.

No genealogy is asserted.

### Case 83: HDFS BlockScanner cursor

The contrast is more useful than the similarity. HDFS saves a scanner cursor specifically so restart can resume maintenance progress and avoid replay from the beginning when the checkpoint remains usable. The bounded PRAC reset path instead withdraws authority from prior completion/count state and establishes a new starting condition through ACI.

> **restart-progress checkpoint ≠ reset-reinitialized protection summary.**

This strengthens Synthesis 26's rule that `maintenance-control state` does not imply one universal persistence horizon.

## Philosophical interpretation — bounded

This case adds a small refinement to the repository's account of persistence and authority:

> a technical state can remain materially possible while the system deliberately ceases to count it as an admissible continuation of the control relation that once made it meaningful.

For PRAC, the decisive transition is not merely whether charge remains somewhere in counter cells. The device/host protocol also needs a valid relation among enable state, known counter initialization, completion evidence, and later counting/ABO authority.

This is an engineering-derived interpretation. It is not Micron or JEDEC philosophical vocabulary, and it should not be generalized into a claim that all memory requires semantic reauthorization after reset.

## Rejected claims / stop conditions

This slice does **not** establish any of the following:

- system reset physically erases PRAC counter cells;
- PRAC activation counts are guaranteed to survive power loss;
- Micron's patent embodiment is the normative JESD79-5C reset contract;
- every DDR5 vendor implements the same counter-cell topology or reset path;
- ACI recovers the previous activation history;
- clearing ACI-complete status proves payload corruption;
- power-up, reset, refresh violation, and ACI are one identical failure mechanism;
- reinitializable maintenance metadata is always less important than durable metadata;
- the Case 09, Case 83, and Case 121 mechanisms share a historical genealogy.

## Related-repository boundary

A repository search found no existing PRAC/ACI-focused treatment in `tmzncty/computing-archaeology` during this pass. The broader history of DDR5 PRAC proposals, JEDEC revision chronology, cross-vendor counter implementations, and memory-controller deployment should primarily be built there if pursued. `technical-retention` keeps only the bounded retention relation: **reset/power-up can terminate the authority horizon of maintenance-control state and require reconstitution before reuse.**

## Remaining evidence debt

- direct normative JESD79-5C reset/power-up clauses and revision-by-revision PRAC changes;
- cross-vendor product documentation for ACI and reset semantics;
- named-controller traces showing reset → enable → ACI → completion → ABO readiness;
- independent fault injection across reset, aborted ACI, refresh violation, and power loss;
- physical characterization of whether/how activation-counter cells retain analog state across reset/power transitions;
- PRAC + ARFM/DRFM interaction after reinitialization.
