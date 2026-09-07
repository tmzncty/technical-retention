# Evidence 117 — Hadoop 2008–2017 startup Safemode grounding

## Purpose

Ground the bounded Case 117 claim that HDFS startup composes two different recovery channels — persisted namespace replay and current DataNode block re-observation — and deliberately withholds ordinary mutation/replication authority until a configurable minimum-replica admission condition has been observed.

This record is not a general history of HDFS recovery, Safemode-like systems, NameNode HA, or distributed-filesystem startup.

## Evidence classification

- **H/P** — Apache release records, released documentation, released source.
- **E** — engineering reconstruction constrained by those documents.
- **A** — bounded functional comparison with already grounded repository cases.
- **X** — explicitly rejected stronger claim.

---

## Source A — Apache Hadoop 0.18.0 release record

**Identity**

- Apache Hadoop, `release 0.18.0 available`.
- Date: **2008-08-22**.
- URL: <https://hadoop.apache.org/release/0.18.0.html>

**What it establishes**

- an official public release chronology anchor for the 0.18.0 generation;
- a safe lower bound for saying the project had public released documentation in this period.

**What it does not establish**

- first Safemode design;
- first implementation;
- first production deployment;
- first recovery gate in a distributed storage system.

**Claim strength**

`H/P`, chronology floor only.

---

## Source B — HDFS Architecture Guide

**Identity**

- Apache Hadoop, `HDFS Architecture Guide`.
- Inspected stable rendering: <https://hadoop.apache.org/docs/r1.2.1/hdfs_design.html>
- The document carries the early HDFS architecture description used here; Case 117 does not infer that every sentence first appeared in exactly the same release revision.

### B1 — NameNode/DataNode authority and Blockreport

The guide assigns namespace management and block-replication decisions to the NameNode. DataNodes store blocks and periodically send `Heartbeat` and `Blockreport`; a Blockreport contains the list of blocks hosted by that DataNode.

**Supports**

- payload embodiment on DataNodes;
- NameNode knowledge of current DataNode holdings as a reported relation;
- separation between payload presence and control-plane observation.

### B2 — Safemode startup sequence

The Safemode section states that:

- the NameNode enters Safemode on startup;
- data-block replication does not occur while in Safemode;
- Heartbeat and Blockreport messages arrive;
- a block is considered safely replicated after its minimum number of replicas has checked in;
- after a configurable percentage of safe blocks plus an additional delay, the NameNode leaves Safemode;
- after exit it identifies blocks still below their specified replication requirement and replicates them.

**Supports**

- minimum-replica check-in as startup qualification;
- `safe` ≠ full configured redundancy;
- withheld replication during incomplete observation;
- post-gate repair as a distinct later phase.

### B3 — namespace persistence

The persistence section says:

- namespace changes are recorded in the `EditLog`;
- the namespace, including block-to-file mapping and file-system properties, is stored in `FsImage`;
- at startup the NameNode reads `FsImage` and `EditLog`, applies logged transactions, and creates the renewed in-memory/on-disk image.

**Supports**

- retained historical metadata / replay channel;
- namespace reconstruction distinct from DataNode location observation.

### B4 — DataNode startup block inventory

The DataNode local-storage section says a DataNode stores an HDFS block as a separate file and at startup scans its local filesystem, creates a list of HDFS blocks, and sends that list to the NameNode as a Blockreport.

**Supports**

- current location knowledge rebuilt from surviving embodiments;
- `Blockreport` as re-observation rather than payload creation.

**Limits**

- the guide does not prove media integrity for every reported block;
- it does not prove rack-placement satisfaction from the safe-block count;
- it does not establish a complete cross-release source-code genealogy.

**Claim strength**

`H/P` for documented architecture; `E` for the replay-vs-re-observation decomposition.

---

## Source C — Hadoop 1.0.4 HDFS Users Guide

**Identity**

- Apache Hadoop 1.0.4, `HDFS Users Guide`.
- URL: <https://hadoop.apache.org/docs/r1.0.4/hdfs_user_guide.html>

### C1 — restart metadata reconstruction

The guide says the NameNode reads HDFS state from `fsimage`, applies `edits`, and reconstructs the current file-system metadata view during startup.

### C2 — Safemode rationale

The Safemode section says the NameNode waits for DataNodes to report blocks so that it does not **prematurely** begin replication when enough replicas may already exist.

This is especially important for the retention argument: delayed action is explicitly justified by incomplete controller knowledge, not by absence of a replication policy.

### C3 — read-only service boundary

The same section describes Safemode as essentially read-only and says modifications to the file system or blocks are not allowed during it.

### C4 — normal versus manual entry

The guide says Safemode normally leaves automatically after DataNodes have reported that most blocks are available, while administrators may also explicitly enter Safemode with `dfsadmin`.

**Supports**

- `retained/readable` ≠ `ordinary mutation allowed`;
- withholding replication can avoid unnecessary work based on incomplete observations;
- manual entry exists as a separate authority path, though the stronger lifecycle difference is grounded by Source E.

**Claim strength**

`H/P`.

---

## Source D — Hadoop 1.0.4 `hdfs-default.html`

**Identity**

- Apache Hadoop 1.0.4, released default HDFS configuration.
- URL: <https://hadoop.apache.org/docs/r1.0.4/hdfs-default.html>

**Relevant entries**

- `dfs.replication.min = 1`;
- `dfs.safemode.threshold.pct = 0.999f`;
- `dfs.safemode.extension = 30000`.

The threshold description defines the value as the fraction of blocks that should satisfy the minimum replication requirement. It also documents that values above 1 make Safemode permanent under that configuration contract. The extension is the duration after threshold attainment before leaving Safemode.

**Supports**

- safe-block percentage is configurable;
- 99.9% is a release-bounded default rather than a definition of Safemode;
- minimum replication and ordinary configured replication factor are not interchangeable concepts;
- threshold condition and final exit are separated by retained temporal state.

**Rejected inference**

`0.999f` is not treated as a universal HDFS constant, reliability law, or proof that the remaining 0.1% is lost.

**Claim strength**

`H/P`.

---

## Source E — Hadoop 2.8.0 `FSNamesystem.SafeModeInfo`

**Identity**

- Apache Hadoop 2.8.0 released source rendering.
- `org.apache.hadoop.hdfs.server.namenode.FSNamesystem.SafeModeInfo`.
- URL: <https://hadoop.apache.org/docs/r2.8.0/hadoop-project-dist/hadoop-hdfs/api/src-html/org/apache/hadoop/hdfs/server/namenode/FSNamesystem.SafeModeInfo.html>

### E1 — automatic startup counting

The class documentation says that during NameNode startup `SafeModeInfo` counts `safe blocks`, defined as blocks with at least the minimal number of replicas, computes their ratio to total blocks, and starts the monitor when the threshold is reached.

### E2 — extension and reached state

The source retains fields including:

- `threshold`;
- minimum DataNode threshold;
- `extension`;
- `safeReplication`;
- `blockTotal`;
- `blockSafe`;
- `reached`, whose documented values distinguish Safemode off, threshold not yet reached, and extension period.

This grounds:

> threshold evidence can already exist while the service remains in Safemode.

### E3 — automatic startup ≠ manual Safemode

The class documentation explicitly says that if Safemode is turned on manually, safe blocks are not tracked for automatic exit because the NameNode is not intended to leave that mode through the startup condition.

**Supports**

- same `Safemode` name can cover different control-state lifecycles;
- startup progress state and manual administrator authority must not be collapsed;
- service admission depends on retained/derived control evidence in addition to payload and namespace survival.

**Limits**

The same 2.8.0 source contains HA/resource-low complexity that Case 117 deliberately does not generalize. Those branches remain evidence debt rather than being silently folded into the startup case.

**Claim strength**

`H/P` for source behavior; `E` for the control-state decomposition.

---

## Cross-case controls

### Case 80 — HDFS DataNode decommission / placement

Grounded Case 80 distinguishes sufficient replica count from placement-policy satisfaction. Therefore Case 117 uses startup safe-block count only as the bounded Safemode predicate and does not treat it as a rack/failure-domain certificate.

**Result**

`safe-block count ≠ placement qualification` (`A`, bounded within HDFS).

### Case 83 — HDFS DataNode block scanner

Grounded Case 83 distinguishes replica presence from checksum/integrity verification.

**Result**

`reported/safe replica ≠ integrity-qualified replica` (`A`, bounded within HDFS).

### Case 116 — HDFS DataNode maintenance state

Case 116 retains a per-DataNode temporary-withdrawal/admin-state relation and an expiry. Case 117 retains a NameNode-wide startup admission relation while block-location knowledge is re-established.

**Result**

`startup Safemode ≠ DataNode maintenance mode` (`A`; no genealogy claim).

---

## Related-repository check

Searches of `tmzncty/computing-archaeology` for `HDFS safemode` returned no dedicated case in this round.

Therefore this repository keeps the narrow retention argument. If a broad history of HDFS startup recovery, GFS/HDFS recovery genealogy, block-report protocol evolution, or distributed-storage service-admission design is developed, it should be routed to `computing-archaeology` and linked back rather than duplicated here.

---

## Claim ledger

| Claim | Type | Strength | Evidence / limit |
| --- | --- | --- | --- |
| HDFS has a public 2008 release-era Safemode record | H/P | strong bounded chronology | Apache 0.18.0 release + architecture record; no invention claim |
| NameNode namespace is reconstructed from FsImage/EditLog | H/P | strong | Apache architecture/users guide |
| DataNode block holdings are re-observed through Blockreports | H/P | strong | Apache architecture guide |
| startup Safemode suppresses block replication | H/P | strong | Apache architecture guide |
| Safemode avoids premature replication while reports are incomplete | H/P | strong | Hadoop 1.0.4 Users Guide |
| startup Safemode is essentially read-only in 1.0.4 | H/P | strong release-bounded | Users Guide |
| a safe block satisfies a minimum-replica check-in predicate | H/P | strong | architecture guide + 2.8.0 source |
| safe-block threshold may be below 100% | H/P | strong release-bounded | 1.0.4 default `0.999f` |
| threshold attainment precedes final exit when extension applies | H/P | strong | 1.0.4 config + 2.8.0 source |
| startup automatic Safemode differs from manual Safemode lifecycle | H/P | strong | 2.8.0 source |
| namespace replay and replica-location re-observation are distinct recovery mechanisms | E | strong reconstruction | Sources B/C/E |
| payload survival does not imply NameNode has already re-observed its location | E | strong reconstruction | Source B blockreport path |
| safe-block admission does not establish rack placement | A/X | strong guardrail | Case 80 owns placement qualification |
| safe-block admission does not establish checksum integrity | A/X | strong guardrail | Case 83 owns scanner/integrity relation |
| Safemode withholding does not imply physical WORM or sanitization | E/X | strong guardrail | service state only; no media-erasure evidence |

---

## Evidence debt

Still unresolved and intentionally outside this slice:

1. pre-2008 HDFS Safemode proposal, mailing-list, and commit genealogy;
2. exact behavior changes across 0.18, 0.20/1.x, 2.x, and 3.x;
3. NameNode HA active/standby startup and edit-tailing semantics;
4. resource-low Safemode and forced exit;
5. erasure-coded HDFS startup qualification;
6. persistence/crash behavior of Safemode progress/control state itself;
7. production traces showing late DataNode reports and avoided premature repair;
8. fault-injection reproduction of report/threshold/extension transitions;
9. direct comparison with earlier distributed-file-system recovery gates;
10. physical media integrity and sanitization below HDFS.
