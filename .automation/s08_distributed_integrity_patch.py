from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text()
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"{path}: expected one anchor, found {n}")
    p.write_text(text.replace(old, new))


# Deepen Synthesis 08 rather than creating a redundant Synthesis 14.
s08 = Path("docs/SYNTHESIS_08_PROACTIVE_INTEGRITY_REPAIR_MARGIN.md")
s08_text = s08.read_text()
anchor = "## Relationship to Synthesis 07\n"
if s08_text.count(anchor) != 1:
    raise SystemExit("Synthesis 08: relationship anchor not unique")
addendum = r'''## Distributed replica-integrity lifecycle addendum

The roadmap also asked a narrower distributed-storage question:

> How should `version currentness`, `checksum validity`, `demand-time versus idle-time discovery`, `fallback read availability`, `valid-replica count`, `clone repair`, and `restored replication goal` be separated?

The already-grounded GFS and HDFS cases supply a direct answer, while Ceph supplies the counterexample that prevents checksum metadata from being treated as unquestionable truth. This subsection therefore **deepens this existing synthesis instead of creating another near-duplicate synthesis document**.

### Version/currentness is not checksum validity

GFS Case 26 gives the cleanest historical split. Chunk version numbers exclude stale replicas from ordinary service; per-replica checksums separately qualify the contents of a replica that belongs to the expected version. HDFS Case 83 similarly separates Blockreport/inventory presence from later checksum verification. A physical copy can therefore be present yet inadmissible because it is stale, or current yet later rejected because its local integrity relation fails.

This yields a qualified-count rule:

```text
physical replica count
    != current-version replica count
    != integrity-qualified replica count
```

The last count is the one relevant to immediate repair opportunity under the bounded accidental-corruption model.

### Demand-time discovery is not idle/periodic discovery

GFS verifies checksum blocks before returning requested data and can also `scan and verify` inactive chunks during idle periods. HDFS documentation describes client-side checksum checking on retrieval, while the DataNode `BlockScanner` / `VolumeScanner` path deliberately reads replicas without an application request, under a rate-limited periodic/suspect-triggered maintenance regime.

The integrity relation may be the same kind of checksum relation, but the **trigger and timing of discovery differ**:

```text
demand-time verification
    -> defect is discovered because current service touched the replica

idle / periodic verification
    -> defect may be discovered before current service needs the replica
```

Background verification therefore changes the interval during which a latent defect can silently consume future repair margin. It does not prove that corruption happened during the scan, nor does a successful scan create permanent future validity.

### Fallback read availability is not repair completion

In GFS, a checksum mismatch can cause the requester to use another replica while the master separately arranges cloning from a valid source. HDFS likewise allows checksum failure on one replica to be bypassed by retrieving another copy while distributed control later handles re-replication.

So a successful request can occur in a degraded-but-serviceable state:

```text
one replica rejected
    -> another valid replica serves the read
    -> configured replication goal may still be unmet
    -> clone / re-replication remains pending
```

`read succeeded` therefore says less than `repair completed`, and both say less than `all intended replicas are again present and qualified`.

### Valid-replica count is a qualified count, not an inventory count

GFS explicitly warns that an inactive corrupted replica can make the master believe enough valid replicas exist until the defect is discovered. HDFS Case 79/83 provides the complementary inventory counterexample: a Blockreport can positively re-observe a block location without establishing that a later full checksum verification will succeed.

The system can consequently move through several different counts:

```text
inventoried / physically present replicas
        ↓ currentness filter
current-version replicas
        ↓ integrity qualification
currently acceptable repair/service sources
        ↓ clone / re-replication
restored configured replication goal
```

These counts can coincide in a healthy steady state, but they are not the same retained relation.

### Clone repair is not discovery, and restored goal is not revalidation of everything

GFS makes the ordering particularly explicit: after corruption is detected, another **valid replica** is used to create a replacement; only after the replacement exists does the master tell the server holding the corrupted copy to delete it. The clone consumes network/disk bandwidth and is throttled separately from ordinary service. HDFS's DataNode scanner similarly stops at verification/reporting; NameNode-directed re-replication is a later distributed action.

This gives a bounded lifecycle:

```text
currentness + integrity qualification
        ↓
defect discovery
        ↓
repair-source admissibility
        ↓
(optional) fallback service
        ↓
clone / re-replication
        ↓
configured replication goal restored
        ↓
future periodic verification remains necessary
```

The final line matters. Restoring the replica goal recreates multiplicity; it does not turn every embodiment into timelessly verified state. Later scans can still discover new corruption, and Ceph Case 27 shows that integrity metadata itself can require requalification.

### What this distributed addendum does not establish

This relation map does **not** establish that GFS, HDFS, Ceph, and ZFS share one repair implementation or historical lineage. It does not equate GFS `scan and verify` with the later historical term `scrub`, does not treat HDFS BlockScanner as the origin of distributed integrity maintenance, and does not turn checksum equality into a Byzantine-authenticity proof. It also does not collapse anti-entropy/version reconciliation into corruption detection: GFS itself explicitly notes that legal replicas can diverge, so bytewise equality is not its universal corruption criterion.

The bounded result is narrower: in distributed replicated storage, **currentness, integrity qualification, discovery timing, request fallback, qualified replica count, repair execution, and restored replication goal are separate retention relations even when a healthy system often makes them appear to move together**.

---

'''
s08.write_text(s08_text.replace(anchor, addendum + anchor))

# Close the already-answerable roadmap relation without pretending the broader history is complete.
roadmap_old = "- [ ] In distributed integrity maintenance, how should `version currentness`, `checksum validity`, `demand-time versus idle-time discovery`, `fallback read availability`, `valid-replica count`, `clone repair`, and `restored replication goal` be separated?"
roadmap_new = "- [x] In distributed integrity maintenance, separate `version currentness`, `checksum validity`, `demand-time versus idle/periodic discovery`, `fallback read availability`, `integrity-qualified replica count`, `clone/re-replication`, and `restored replication goal` — closed at the bounded relation level by the distributed-replica addendum in [`docs/SYNTHESIS_08_PROACTIVE_INTEGRITY_REPAIR_MARGIN.md`](docs/SYNTHESIS_08_PROACTIVE_INTEGRITY_REPAIR_MARGIN.md), using grounded Cases 26 and 83 with Cases 27/79 as authority/inventory counterexamples. Full GFS→HDFS scanner genealogy, controller patrol-read history, distributed scan coordination, correlated corruption, and production fault injection remain open."
replace_once("ROADMAP.md", roadmap_old, roadmap_new)

# Update README navigation text in place rather than adding another synthesis entry.
readme_old = "A bounded proactive-integrity comparison is now available in [`docs/SYNTHESIS_08_PROACTIVE_INTEGRITY_REPAIR_MARGIN.md`](docs/SYNTHESIS_08_PROACTIVE_INTEGRITY_REPAIR_MARGIN.md). Across grounded GFS, ZFS, HDFS, Ceph, and OpenZFS cases it separates physical presence, currentness/admissibility, integrity evidence, verification coverage, defect discovery, repair-source qualification, repairability, fallback service, restored redundancy, and later revalidation."
readme_new = readme_old + " A focused distributed-replica addendum now also separates version currentness, checksum validity, demand-time versus idle/periodic discovery, fallback reads, integrity-qualified replica count, clone/re-replication, and restoration of the configured replication goal without treating those stages as one health bit."
replace_once("README.md", readme_old, readme_new)

# Append compact findings to the authoritative ledger.
idx = Path("CASE_INDEX.md")
text = idx.read_text().rstrip()
expected_tail = "1492. **durability-handoff synthesis ≠ one universal pipeline or historical genealogy** — SCSI cache commands, NVMe namespace semantics, Intel SSD PLI, SNIA mapped persistent memory, ADR/eADR, and PLI validation are compared only at the relation level; their command sets, physical mechanisms, failure envelopes, and historical lineages remain distinct."
if not text.endswith(expected_tail):
    raise SystemExit("CASE_INDEX.md: unexpected findings tail")
findings = r'''

### Distributed replica-integrity lifecycle deepening — currentness, discovery timing, fallback, and restored goal

1493. **physical replica count ≠ current-version replica count** — GFS can retain stale replicas physically while chunk-version state excludes them from ordinary service, so inventory multiplicity is weaker than currentness-qualified multiplicity.
1494. **current-version replica count ≠ integrity-qualified replica count** — a replica can belong to the expected version and still fail its local checksum/read relation; currentness and integrity are orthogonal filters.
1495. **demand-time verification ≠ idle/periodic verification** — GFS read-path checks and idle `scan and verify`, plus HDFS client retrieval checks and DataNode background scanning, can exercise similar integrity relations under different triggers and discovery times.
1496. **background discovery time ≠ corruption creation time** — finding a latent defect during an idle/periodic pass dates the observation, not necessarily the physical/software event that created the defect.
1497. **fallback read success ≠ local replica repair** — another valid replica may satisfy the current request while the rejected embodiment remains bad and replacement work has not yet occurred.
1498. **fallback read availability ≠ restored replication goal** — service can continue with reduced integrity-qualified multiplicity; the configured future-failure margin is restored only after enough replacement replicas are materialized.
1499. **corrupt-replica report ≠ clone/re-replication completion** — GFS detection and HDFS `reportBadBlocks` create distributed repair work; neither event is itself the completed replacement copy.
1500. **valid repair source exists ≠ replacement replica exists** — a trustworthy source makes clone/re-replication possible, but network/disk scheduling, destination placement, and transfer completion remain separate obligations.
1501. **restored replication goal ≠ timeless verification of every replica** — replacing a bad copy restores multiplicity, while later scans/checks can still withdraw trust from an embodiment or its integrity metadata.
1502. **replica equality ≠ universal integrity verdict** — GFS explicitly permits legal byte divergence under some mutation semantics, so distributed integrity qualification cannot be reduced to simple equality voting across replicas.
1503. **distributed integrity maintenance ≠ anti-entropy/version reconciliation** — background work can target local corruption, causal/version divergence, or both, but those functions must not be collapsed merely because each compares or repairs distributed state.
1504. **distributed replica-integrity lifecycle synthesis ≠ implementation genealogy** — GFS, HDFS, Ceph, and ZFS are compared at the relation level only; shared functions do not establish direct descent, identical algorithms, or one historical vocabulary.
'''
idx.write_text(text + findings)

# Basic integrity checks.
assert "## Distributed replica-integrity lifecycle addendum" in s08.read_text()
assert "1504. **distributed replica-integrity lifecycle synthesis ≠ implementation genealogy**" in idx.read_text()
assert roadmap_new in Path("ROADMAP.md").read_text()
assert readme_new in Path("README.md").read_text()
