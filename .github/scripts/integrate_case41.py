from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def insert_after(text: str, anchor: str, addition: str, label: str) -> str:
    return replace_once(text, anchor, anchor + addition, label)


# README
p = Path("README.md")
text = p.read_text()
case40 = "- [`cases/40-raidr-retention-aware-dram-refresh.md`](cases/40-raidr-retention-aware-dram-refresh.md) — grounded retention-aware DRAM-refresh bridge: RAIDR retains row-level profiling/bin metadata in the memory controller to assign selective refresh cadence, while the 2013 commodity-DDR3 study shows that data-pattern dependence and variable retention time can make a surviving profile incomplete or non-conservative.\n"
case41 = "- [`cases/41-apache-cassandra-tombstone-gc-grace-resurrection.md`](cases/41-apache-cassandra-tombstone-gc-grace-resurrection.md) — grounded distributed-deletion/repair bridge: Cassandra retains tombstones so missed deletes can later defeat stale positive replicas; `gc_grace_seconds`, compaction overlap, repair, and optional repaired-state gating keep deletion convergence, age eligibility, and actual reclamation distinct, while premature loss of deletion evidence can let repair resurrect older data.\n"
text = insert_after(text, case40, case41, "README case anchor")
ev40 = "- [`evidence/40-raidr-2012-2013-retention-profile-grounding.md`](evidence/40-raidr-2012-2013-retention-profile-grounding.md) — Case-40 grounding record: the ISCA 2012 RAIDR mechanism and ISCA 2013 248-chip retention study separate physical retention margin, profiling, row/bin maintenance metadata, conservative Bloom-filter representation, global temperature scaling, and future profile validity without claiming commercial deployment.\n"
ev41 = "- [`evidence/41-cassandra-3x-tombstone-repair-grounding.md`](evidence/41-cassandra-3x-tombstone-repair-grounding.md) — Case-41 grounding record: Apache Cassandra 3.11 documentation, 3.x release notes, branch source, and unit tests separate tombstone negative currentness, hint delivery, anti-entropy repair, `gc_grace_seconds`, compaction eligibility, repaired/unrepaired state, and data-resurrection risk without equating reclamation with secure erasure.\n"
text = insert_after(text, ev40, ev41, "README evidence anchor")
p.write_text(text)

# ROADMAP
p = Path("ROADMAP.md")
text = p.read_text()
text = replace_once(
    text,
    "- [ ] distributed replication and erasure coding beyond RADOS — **partially advanced by grounded Cases 19, 23, 24, 25, 26, 27, 28, and 29**.",
    "- [ ] distributed replication and erasure coding beyond RADOS — **partially advanced by grounded Cases 19, 23, 24, 25, 26, 27, 28, 29, and 41**.",
    "ROADMAP distributed-case count",
)
marker = " The broad item stays unchecked because other mutable-EC consistency protocols,"
addition = " [`cases/41-apache-cassandra-tombstone-gc-grace-resurrection.md`](cases/41-apache-cassandra-tombstone-gc-grace-resurrection.md), grounded by [`evidence/41-cassandra-3x-tombstone-repair-grounding.md`](evidence/41-cassandra-3x-tombstone-repair-grounding.md), adds a distinct distributed-delete reclamation regime: tombstones retain negative currentness across replica outages; `gc_grace_seconds` creates an age/failure envelope rather than a repair guarantee; compaction overlap and optional repaired-state gating separate expiry from actual purge; and losing deletion evidence while a stale positive replica remains can let repair resurrect the older value."
text = replace_once(text, marker, addition + marker, "ROADMAP Case 41 insertion")
text = replace_once(
    text,
    "because other mutable-EC consistency protocols, cross-region coded maintenance, later Swift durability-marker/on-disk evolution,",
    "because other mutable-EC consistency protocols, cross-region coded maintenance, later Cassandra tombstone/repair semantics, later Swift durability-marker/on-disk evolution,",
    "ROADMAP remaining-work list",
)
p.write_text(text)

# CASE_INDEX
p = Path("CASE_INDEX.md")
text = p.read_text()
case40row = "| [RAIDR Retention-Aware DRAM Refresh: Row Binning, Profiling Metadata, and Variable-Retention Limits](cases/40-raidr-retention-aware-dram-refresh.md) | **grounded** | volatile dynamic payload + measured row-retention heterogeneity + retained controller profile/bin metadata + Bloom-filter conservative representation + row-selective cadence + global temperature scaler | separate physical retention margin, measured profile, profile validity, row-level cadence policy, and controller-side maintenance authority; use DPD/VRT to show retained maintenance metadata can survive while becoming non-conservative | [2012–2013 RAIDR/profiling grounding](evidence/40-raidr-2012-2013-retention-profile-grounding.md); commercial deployment, online VRT-aware profiling/ECC, JEDEC standardization, and RowHammer-oriented refresh remain separate work |\n"
case41row = "| [Apache Cassandra GC Grace: Tombstone Retention, Repair Windows, and Data Resurrection](cases/41-apache-cassandra-tombstone-gc-grace-resurrection.md) | **grounded** | replicated positive values + timestamped tombstone negative state + hints/repair + SSTable repaired/unrepaired state + compaction/overlap reclamation constraints | show deletion can depend on retained negative evidence; separate tombstone age, replica convergence, repair evidence, and physical reclamation; show forgetting deletion evidence can make older payload current again | [Cassandra 3.x tombstone/repair grounding](evidence/41-cassandra-3x-tombstone-repair-grounding.md); later Cassandra repair/tombstone evolution, secure erasure, cross-version semantics, and broader tombstone genealogy remain separate work |\n"
text = insert_after(text, case40row, case41row, "CASE_INDEX case row")

matrix40 = "| RAIDR retention-aware DRAM refresh / 2012–2013 bounded research regime | dynamic-cell charge + measured row-retention profile + Bloom-filter/bin membership + controller scheduling/temperature-scaler state | controller profiles rows and applies shorter cadence to weak-row bins; global temperature scaling is separately applied; 2013 DPD/VRT evidence challenges static conservative profiles | ordinary service reads remain DRAM reads; profiling deliberately disables refresh to observe failure thresholds, while normal retention policy restores selected rows by activation/RAS-only-style refresh | row address plus controller-retained bin membership; row retention time is the minimum over cells in the row | fixed DRAM row location; identity does not migrate, but the maintenance classification attached to the row can change after re-profiling | no application history; the profile is second-order maintenance state and may be saved across boots, yet its survival does not guarantee future validity |\n"
matrix41 = "| Apache Cassandra tombstone/GC-grace / 3.x bounded regime | replicated positive values + timestamped tombstone negative currentness + hint state + repaired/unrepaired SSTable relation + compaction overlap | DELETE retains tombstones; hints can temporarily deliver missed mutations; read/anti-entropy repair converges replicas; compaction later reclaims eligible tombstones, optionally only after repaired status | a stale positive embodiment can remain physically readable yet be suppressed by a newer tombstone; after deletion evidence is lost, repair can make that older value current again | logical partition/row/column designation resolves across replicas and timestamped states; compaction additionally reasons over SSTable overlap and repaired status | positive and negative embodiments can coexist across replicas/SSTables; deletion identity is relational rather than one physical absence | no complete history; bounded negative currentness, repair status, hints, and reclamation-control state are retained long enough to sustain deletion |\n"
text = insert_after(text, matrix40, matrix41, "CASE_INDEX matrix row")

text = replace_once(
    text,
    "After thirty-eight bounded cases, **all thirty-eight cases are now `grounded`.**",
    "After forty-two bounded cases, **all forty-two cases are now `grounded`.**",
    "CASE_INDEX synthesis count",
)
old80 = "80. **category coherence is provisional and evidence-gated** — forty-one grounded regimes now support the current relational criterion, including the grounded delay-line circulation/temperature-control regime plus powered flip-flop, static-MOS, cache-policy, refresh-address-internalization, autonomous leakage-tracked refresh-scheduling, SDRAM refresh-mode handoff, floating-gate EPROM erase-asymmetry, byte-erasable EEPROM, coarse-erase early Flash, HDD defect-reassignment, SSD power-loss-durability, BSD FFS crash-admissibility, RAID parity-reconstruction, ZFS proactive-scrubbing, f4 distributed-erasure-coding, NVMe 1.0 persistence-interface, IBM paging/backing-copy-currentness, Dynamo divergent-version/anti-entropy, Windows Azure LRC repair-locality/representation-handoff, Swift mutable-EC currentness, GFS distributed-integrity-verification, Ceph EC checksum-authority/deep-scrub, Swift distributed-delete/tombstone-consistency, Ceph Luminous scrub-repair-authority, NVMe 1.4 persistent-memory-region, SNIA persistence-domain, Intel ADR/eADR power-fail-domain, DDR5 same-bank-refresh-localization, temperature-conditioned DRAM-refresh, and commercial Mobile-DDR automatic-TCSR/selective-retention, NAND-Flash FCR controller-maintenance, commercial Samsung 840 EVO old-data performance-refresh, Intel DC S3700/S3500 PLI-health/validation, GeckoFTL controller-metadata-recovery, and RAIDR retention-profile/row-selective-refresh bridges; future write-back-cache, filesystem, refresh, virtual-memory, and distributed regimes must still be allowed to break or revise it rather than being forced into it;"
new80 = "80. **category coherence is provisional and evidence-gated** — forty-two grounded regimes now support the current relational criterion, including the grounded delay-line circulation/temperature-control regime plus powered flip-flop, static-MOS, cache-policy, refresh-address-internalization, autonomous leakage-tracked refresh-scheduling, SDRAM refresh-mode handoff, floating-gate EPROM erase-asymmetry, byte-erasable EEPROM, coarse-erase early Flash, HDD defect-reassignment, SSD power-loss-durability, BSD FFS crash-admissibility, RAID parity-reconstruction, ZFS proactive-scrubbing, f4 distributed-erasure-coding, NVMe 1.0 persistence-interface, IBM paging/backing-copy-currentness, Dynamo divergent-version/anti-entropy, Windows Azure LRC repair-locality/representation-handoff, Swift mutable-EC currentness, GFS distributed-integrity-verification, Ceph EC checksum-authority/deep-scrub, Swift distributed-delete/tombstone-consistency, Ceph Luminous scrub-repair-authority, NVMe 1.4 persistent-memory-region, SNIA persistence-domain, Intel ADR/eADR power-fail-domain, DDR5 same-bank-refresh-localization, temperature-conditioned DRAM-refresh, commercial Mobile-DDR automatic-TCSR/selective-retention, NAND-Flash FCR controller-maintenance, commercial Samsung 840 EVO old-data performance-refresh, Intel DC S3700/S3500 PLI-health/validation, GeckoFTL controller-metadata-recovery, RAIDR retention-profile/row-selective-refresh, and Cassandra tombstone/repair-window bridges; future write-back-cache, filesystem, refresh, virtual-memory, and distributed regimes must still be allowed to break or revise it rather than being forced into it;"
text = replace_once(text, old80, new80, "CASE_INDEX finding 80 count")

finding380 = "380. **research evaluation ≠ commercial deployment** — RAIDR's reported refresh/power/performance/storage figures are research evaluation results; the source set does not establish a shipped controller using RAIDR or a JEDEC per-row retention-profile contract.\n"
new_findings = """
381. **logical deletion ≠ immediate physical removal** — Cassandra 3.11 explicitly writes a tombstone rather than immediately removing underlying data; the user-visible delete and retirement of all old embodiments are different events.
382. **negative-state retention ≠ positive-payload retention** — a tombstone is retained so an older positive value will no longer count as current; preserving the fact of deletion and preserving the deleted payload are opposite operational roles even though both consume retained state.
383. **tombstone presence ≠ replica convergence** — a newer tombstone can coexist with a disconnected replica that still holds the older value; negative currentness remains a local/distributed relation until delivery or repair propagates it.
384. **`gc_grace_seconds` expiry ≠ immediate tombstone reclamation** — age only makes a tombstone eligible; Cassandra still requires a compaction event and overlap safety relative to older shadowed SSTable data.
385. **retention window ≠ repair guarantee** — the grace interval preserves anti-resurrection evidence but does not itself contact or reconcile a failed replica; repair remains separate maintenance work.
386. **hint retention ≠ tombstone retention ≠ anti-entropy repair** — Cassandra 3.11 calls hints best effort, gives them their own downtime window, and explicitly says they do not replace anti-entropy repair; similar-looking retained-control states have different guarantees and triggers.
387. **forgetting deletion evidence can resurrect older payload** — Apache's documented failure example shows that if the tombstone is gone while a stale replica retains the older value, later repair can make that value reappear across the cluster.
388. **repair can preserve forgetting or defeat it depending on surviving currentness evidence** — repair propagates the tombstone when deletion evidence survives, but can propagate the stale value when it does not; `repair` is not semantically independent of the states admitted as current inputs.
389. **repair-qualified forgetting ≠ cost-free safety** — `only_purge_repaired_tombstones` can delay purge until repaired-state evidence exists, while Apache's release note warns that failing to repair for long periods can retain tombstones long enough to cause other operational problems.
390. **tombstone reclamation ≠ secure erasure** — removing Cassandra's negative currentness marker is a distributed-storage reclamation event; it does not establish sanitization of every stale physical copy or lower-layer media trace.
"""
text = insert_after(text, finding380, new_findings, "CASE_INDEX new findings")
p.write_text(text)

# Sanity checks
assert Path("cases/41-apache-cassandra-tombstone-gc-grace-resurrection.md").exists()
assert Path("evidence/41-cassandra-3x-tombstone-repair-grounding.md").exists()
for path in [Path("README.md"), Path("ROADMAP.md"), Path("CASE_INDEX.md")]:
    data = path.read_text()
    if "cases/41-apache-cassandra-tombstone-gc-grace-resurrection.md" not in data:
        raise SystemExit(f"Case 41 missing from {path}")

print("Case 41 navigation/status integration completed")
