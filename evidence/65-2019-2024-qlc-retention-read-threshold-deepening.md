# Case 65 Deepening — 2019–2024 Direct QLC Retention / Read-Threshold Evidence

## Status

**`bounded deepening complete`** for the minimal generation-transfer question left open after the 2022–2024 TLC deepening: whether retention-conditioned threshold/read-reference behavior is directly measured in **3D QLC NAND**, rather than inferred from MLC/TLC work.

This packet closes that narrow evidence gap with two generation-specific scholarly records:

1. a 2019 IEEE International Memory Workshop paper whose abstract explicitly covers **3-D TLC and QLC NAND flash memories**, measured threshold-voltage distributions after different retention times and P/E-cycle counts, and read-voltage optimization; and
2. a 2024 IEEE EDTM paper from IBM researchers that directly evaluates data retention in **state-of-the-art 3D charge-trap QLC NAND**, characterizing raw bit error rate and optimal-read-voltage offsets under different P/E counts, dwell times, and cycling temperatures.

It does **not** establish a universal QLC retention law, a named commercial SSD/controller policy, a direct replication of Luo et al.'s 2018 early-retention curve, or a QLC analogue of every TLC/MLC mechanism already covered by Case 65.

## Scope

The question is deliberately narrow:

> Is there direct QLC-generation evidence that later read interpretation depends on retention-conditioned threshold/error state and cycling history, rather than only a projection from MLC/TLC measurements?

The answer is **yes, at the measurement level**.

The packet therefore distinguishes four propositions:

```text
2018 direct 3D-MLC early-retention measurement
    !=
2022/2024 direct 3D-TLC retention/read-voltage measurement
    !=
2019/2024 direct 3D-QLC retention/read-threshold measurement
    !=
universal cross-generation quantitative law
```

The first three are evidence classes tied to particular tested regimes. The fourth is not established.

## Source roles and provenance

### Source A — Wang et al., IEEE IMW 2019

Kunliang Wang, Gang Du, Zhiyuan Lun, Xiaoyan Liu, **“The Method of Predicting Retention Threshold Voltage Distribution for NAND Flash Memory Based on Back-Propagation Neural Network,”** *2019 IEEE 11th International Memory Workshop (IMW)*, DOI `10.1109/IMW.2019.8739277`.

The Peking University institutional repository record identifies the title, authors, 2019 venue, retention / NAND / read-voltage-optimization keywords, and an abstract explicitly describing **3-D TLC and QLC NAND flash memories**. The abstract says predicted threshold-voltage (`Vth`) distributions after different retention times and program/erase (`P/E`) cycles show good agreement with the measurements and can be used for read-voltage optimization.

**Role:** peer-reviewed conference / institutional bibliographic record with mechanism-bearing abstract.

**Custody limit:** this packet does not claim line-by-line inspection of the paywalled IEEE full paper. Claims below are therefore limited to what the publisher/institutional abstract supports.

### Source B — Sciacca, Kosuru, Papandreou, IEEE EDTM 2024

M. Dean Sciacca, Trinadhachari Kosuru, Nikolaos Papandreou, **“Cycling Condition Impacts on 3D QLC NAND Reliability,”** *2024 8th IEEE Electron Devices Technology & Manufacturing Conference (EDTM)*, DOI `10.1109/EDTM58488.2024.10511536`, conference-paper date 3 March 2024.

IBM Research's publication page states that the study evaluates the impact of cycling conditions on data retention using **state-of-the-art 3D charge-trap QLC NAND flash** and characterizes:

- raw bit error rate (`RBER`);
- optimal read-voltage offsets;
- program/erase cycle count;
- dwell time; and
- cycling temperature.

The authors frame the results as guidance for reliability analysis and flash-management algorithms.

**Role:** institutional author/employer publication record for a peer-reviewed IEEE conference paper.

**Custody limit:** unless a full paper is separately inspected, this packet does not invent device geometry, vendor identity, exact numerical curves, retention duration, or controller implementation details absent from the institutional abstract.

## Historical record

### H-65Q.1 — direct QLC threshold-distribution evidence is public by 2019

The 2019 IMW record is important because its object is not merely “multi-bit NAND” in the abstract. It explicitly names both **3-D TLC and QLC NAND flash memories**.

Its abstract links three variables directly:

```text
retention time
    +
P/E-cycle count
    ->
measured threshold-voltage distributions
```

The paper then proposes a back-propagation neural-network model whose predicted distributions are compared with those measurements and used for read-voltage optimization.

Therefore the minimum historical claim is:

> **By 2019, peer-reviewed work directly treated measured retention-conditioned threshold-voltage distributions in 3-D QLC NAND as an input to read-voltage optimization.**

This closes the narrow “QLC only by projection” gap left after the prior TLC deepening.

It does **not** establish that every QLC device has the same distribution movement or that the model was deployed in a shipping SSD.

### H-65Q.2 — direct charge-trap QLC retention/read-offset evidence continues in 2024

The 2024 EDTM record is independent evidence that the same broad problem survives in a modern charge-trap QLC regime.

Its institutional abstract states:

```text
cycling condition
    = P/E count + dwell time + cycling temperature

cycling condition
    -> data-retention behavior
    -> RBER / optimal-read-voltage offset characterization
```

Therefore:

> **Direct QLC evidence is not limited to a 2019 modeling paper; a 2024 charge-trap QLC study explicitly characterizes retention through raw-error and optimal-read-voltage observables under different cycling histories.**

Again, this is a source-bounded statement about the study, not a universal NAND rule.

### H-65Q.3 — the vocabulary is already read-interpretation vocabulary

The two records use engineering terms including:

- `retention threshold voltage distribution`;
- `data retention time`;
- `program/erase cycles`;
- `read voltage optimization`;
- `raw bit error rate`;
- `optimal read voltage offsets`;
- `dwell time`;
- `cycling temperature`.

These are historical/technical source terms.

Project phrases such as `interpretation state`, `history-conditioned legibility`, `context-dependent read boundary`, and `persistence horizon` remain analytical vocabulary and are not attributed to the authors.

## Engineering reconstruction

### E-65Q.1 — QLC closes the minimal generation-transfer evidence gap

Before this packet, Case 65 had direct evidence for:

```text
3D MLC
    -> early-retention / read-reference movement (2018)

3D TLC
    -> retention-after-cycling / optimal-read-voltage behavior (2022)
    -> later retention conditioned by prior P/E timing + temperature (2024)
```

The 2019 and 2024 QLC records add:

```text
3D QLC
    -> measured retention-conditioned Vth distributions
    -> measured RBER / optimal-read-voltage offsets
    -> dependence on retention/cycling conditions
```

This supports a bounded engineering conclusion:

> **The need to reason about retention-conditioned read thresholds is directly evidenced in QLC; it need not be imported from TLC/MLC by analogy alone.**

But the direct evidence is qualitative/mechanism-level for this repository unless exact comparable raw curves are inspected.

### E-65Q.2 — a read-reference problem is not a charge-restoration operation

Both QLC records are about measuring, predicting, or selecting a better read criterion for an aged/worn physical distribution.

Therefore:

```text
threshold-distribution prediction
    !=
optimal-read-voltage estimation
    !=
physical charge restoration
    !=
rewrite / refresh
```

A controller may later combine these functions, but the sources do not collapse them into one operation.

This preserves the Case 36 boundary:

> **better interpretation of retained charge ≠ renewal of the retained charge.**

### E-65Q.3 — model agreement is not a retention guarantee

The 2019 abstract says model-predicted threshold distributions agree well with measurements. That statement is evidence about a prediction relation in the tested data.

It is not evidence that:

- the payload will remain recoverable for a specified warranty period;
- an SSD meets a JEDEC retention specification;
- RBER/UBER stays below a product threshold;
- the controller always finds the optimum read voltage; or
- all QLC populations share the model.

Therefore:

> **prediction agreement ≠ payload-retention probability ≠ device-level retention guarantee.**

### E-65Q.4 — history-conditioned physics does not require a literal history log

The 2024 QLC study varies P/E-cycle count, dwell time, and cycling temperature and observes data-retention behavior through RBER and read-voltage offsets.

The engineering distinction is:

```text
prior operating conditions
    -> condition present physical distribution/error state

but

present state depends on history
    !=
device stores a complete event-history record
```

A physical embodiment can carry consequences of prior operation without encoding those events as explicit controller metadata.

This complements, rather than replaces, the Toshiba/ReMAR side of Case 65 where explicit time/control metadata can also be used.

### E-65Q.5 — elapsed retention time is not the whole state description

Together, the two QLC records support a bounded multi-variable view:

```text
retention time
    + P/E wear
    + dwell/cycling condition
    -> threshold/error/read-offset state
```

Therefore:

> **same nominal retention age ≠ necessarily same read margin.**

This does not say every listed variable has equal influence or that one formula works across generations.

## Functional comparison

### With the 2018 MLC ReMAR evidence

Safe comparison:

```text
retention-conditioned physical distribution
    -> changed best read boundary
    -> read-side adaptation/model can improve interpretation
```

Stop condition:

- 2019 QLC BpNN is not ReMAR;
- QLC evidence does not prove the 2018 MLC early-loss curve shape recurs quantitatively;
- shared function does not establish genealogy.

### With the 2022/2024 TLC evidence

Safe comparison:

- TLC and QLC both have direct scholarly evidence relating retention/cycling state to threshold/error/read-voltage behavior.

Stop condition:

> **direct TLC evidence != direct QLC evidence != quantitative portability between them.**

The point of this packet is precisely to avoid using the TLC record as a substitute for QLC measurement.

### With Case 36 physical refresh

Case 36 asks when a controller restores/renews physical margin through reprogram/rewrite.

This packet asks how the surviving aged QLC distribution is measured or read more appropriately.

Therefore:

> **read-threshold adaptation ≠ physical refresh.**

### With Case 59 program interference

Case 59 concerns write-event-induced neighboring-cell effects and protection state.

The 2024 QLC record concerns cycling-condition effects on retention at a higher level of description.

No source here establishes that the observed QLC retention behavior is Case 59's program-interference mechanism.

## Philosophical interpretation — bounded

Only after the historical and engineering layers are fixed does the QLC evidence support a narrow interpretation:

> **Persistence is not exhausted by whether charge remains physically present; future legibility can depend on a read criterion appropriate to the aged and history-conditioned distribution.**

A second bounded point follows:

> **Technical history can be embodied materially without being retained as an explicit symbolic log.**

That is an analytical reading of the engineering relation, not actor vocabulary from the IEEE papers.

It should not be generalized into a claim that all material systems “remember” their histories in the same sense.

## Explicit non-claims

This packet does **not** claim that:

1. the 2019 paper is the first QLC retention study;
2. the 2024 paper is the first charge-trap QLC reliability study;
3. either paper establishes invention priority for retention-aware QLC reading;
4. the 2019 model was deployed in a named commercial SSD;
5. the 2024 study identifies a shipping SSD/controller firmware policy;
6. every QLC generation has the same retention curve;
7. every QLC generation has the same optimal-read-voltage shift;
8. QLC quantitatively follows the 2018 MLC early-retention curve;
9. QLC quantitatively follows the 2022/2024 TLC measurements;
10. model prediction accuracy is a data-retention success probability;
11. model prediction accuracy is RBER or UBER;
12. read-voltage optimization restores leaked charge;
13. threshold-distribution prediction refreshes NAND cells;
14. an RBER change proves immediate user-visible data loss;
15. a read-voltage offset change proves ECC exhaustion;
16. P/E count alone completely determines retention behavior;
17. dwell time alone completely determines retention behavior;
18. cycling temperature alone completely determines retention behavior;
19. the controller must persist a literal log of every prior cycling event;
20. history-conditioned physical state is the same thing as explicit metadata;
21. the 2019 and 2024 papers use the same device population;
22. the 2019 and 2024 papers use the same controller/model;
23. the two papers form a demonstrated historical genealogy;
24. QLC retention behavior is identical to read disturb;
25. QLC retention behavior is identical to program interference;
26. the QLC evidence proves a named product's warranty/JEDEC retention compliance;
27. the sources prove crash-atomic persistence of any controller-side age/model state;
28. the sources prove how FTL relocation carries retention-age metadata;
29. the sources prove neighbor-state recovery such as ReNAC is deployed in QLC; or
30. direct QLC measurement closes all remaining Case 65 deployment and cross-generation debts.

## Claim ledger

| ID | Claim | Layer | Evidence strength / boundary |
| --- | --- | --- | --- |
| H-65Q.1 | 2019 IMW work explicitly studies 3-D TLC and QLC NAND retention-threshold distributions | `H/P` | Peking University institutional record / IEEE paper metadata and abstract |
| H-65Q.2 | predicted Vth distributions after different retention times and P/E cycles are compared with measurements and used for read-voltage optimization | `H/P` | abstract-level claim; no invented full-paper details |
| H-65Q.3 | 2024 EDTM work evaluates data retention in state-of-the-art 3D charge-trap QLC NAND | `H/P` | IBM Research institutional publication record |
| H-65Q.4 | 2024 work characterizes RBER and optimal-read-voltage offsets for different P/E counts, dwell times, and cycling temperatures | `H/P` | IBM Research abstract |
| E-65Q.5 | retention-conditioned read-threshold behavior is directly evidenced in QLC, not merely projected from TLC/MLC | `E` | synthesis of the two QLC records |
| E-65Q.6 | prediction/read-offset adaptation is not physical charge restoration | `E` | operation-boundary reconstruction |
| E-65Q.7 | history-conditioned physics does not imply a separately persisted event-history log | `E` | representation-boundary reconstruction |
| F-65Q.8 | MLC/TLC/QLC share a broad retention-conditioned read-interpretation problem | `F/A` | functional analogy only; quantitative portability blocked |
| F-65Q.9 | QLC read adaptation is functionally distinct from Case 36 physical refresh | `F/A` | comparison boundary |
| I-65Q.10 | retained material can remain present while its best later read criterion changes with age/history | `I` | downstream interpretation only |
| X-65Q.11 | the two QLC papers prove one universal QLC retention law | `X` | explicitly unsupported |
| X-65Q.12 | direct QLC measurement proves a named shipping controller policy | `X` | deployment evidence still open |

## What this changes in Case 65

The former open debt:

> direct QLC measurements rather than carrying forward a TLC/MLC projection

can now be narrowed to:

> direct **QLC measurement exists** for retention-conditioned threshold/error/read-voltage behavior, but stronger cross-generation comparability, longer-horizon device-specific retention studies, named product/controller behavior, and direct testing of the 2018 early-retention / neighbor-conditioned curve in QLC remain open.

That distinction matters. It closes a minimal evidence-class gap without pretending the broader QLC problem is solved.

## Related-repository routing

A fresh search of `tmzncty/computing-archaeology` for QLC NAND retention found no dedicated reusable packet.

The following broader topics should therefore remain there rather than being duplicated here:

- QLC architecture and product-generation chronology;
- vendor/process genealogy;
- charge-trap versus floating-gate QLC product history;
- SSD-controller adoption history;
- BiCS / V-NAND / other product-line evolution; and
- commercial deployment chronology for read-reference algorithms.

This repository keeps only the retention-specific seam:

```text
QLC retention/cycling condition
    -> threshold/error distribution
    -> best read boundary / offset
    -> logical recoverability relation
```

## Remaining evidence debt

Direct QLC measurement is no longer the minimal open gap, but stronger evidence remains useful for:

- full-text inspection of the 2019 IMW experiment and exact device/test details;
- full-text inspection of the 2024 EDTM experiment and exact numerical retention/read-offset curves;
- directly comparable MLC/TLC/QLC experiments on the same platform and protocol;
- named QLC device/vendor studies with long retention horizons;
- QLC-specific early-retention curve measurements directly comparable with Luo et al. 2018;
- QLC-specific retention-interference / neighbor-conditioned measurements;
- interaction with LDPC soft decoding and multi-step read retry;
- firmware traces showing how a shipping controller chooses/readjusts reference voltages;
- power-loss / restart behavior for any retained age/model metadata;
- FTL relocation and garbage-collection semantics for retention-age/control state; and
- named SSD/product evidence that converts raw-device measurement into a deployed retention policy.

## Sources

1. Kunliang Wang, Gang Du, Zhiyuan Lun, Xiaoyan Liu, **“The Method of Predicting Retention Threshold Voltage Distribution for NAND Flash Memory Based on Back-Propagation Neural Network,”** *2019 IEEE 11th International Memory Workshop (IMW)*, 2019, DOI `10.1109/IMW.2019.8739277`. Peking University institutional repository record: <https://ir.pku.edu.cn/handle/20.500.11897/544481>; IEEE record: <https://ieeexplore.ieee.org/document/8739277/>.
2. M. Dean Sciacca, Trinadhachari Kosuru, Nikolaos Papandreou, **“Cycling Condition Impacts on 3D QLC NAND Reliability,”** *2024 8th IEEE Electron Devices Technology & Manufacturing Conference (EDTM)*, 3 March 2024, DOI `10.1109/EDTM58488.2024.10511536`. IBM Research publication record: <https://research.ibm.com/publications/cycling-condition-impacts-on-3d-qlc-nand-reliability>.
