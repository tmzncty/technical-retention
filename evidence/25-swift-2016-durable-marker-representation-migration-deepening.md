# Case 25 deepening — Swift 2.11.0 durability-witness representation migration (2016)

**Status:** bounded deepening complete

## Purpose

This addendum deepens [`Case 25 — OpenStack Swift EC Overwrites`](../cases/25-openstack-swift-ec-overwrite-durable-currentness.md) at one revision boundary that the original case deliberately left outside scope:

> **Can the retained fact that an EC fragment cohort is durable survive a change in the on-disk representation used to encode that fact?**

Swift 2.11.0 provides an unusually clean primary-source answer. Earlier Swift represented EC durability with a separate zero-byte `<timestamp>.durable` file. Change `b13b49a27caac17ae55b19f315d5ce31801c9522` changed new writes so the object server instead renames a fragment archive from:

```text
<timestamp>#<frag_index>.data
```

to:

```text
<timestamp>#<frag_index>#d.data
```

The release retained support for legacy `.durable` files, normalized both physical encodings to the same consistency-engine state, and explicitly warned that EC data written by 2.11.0-or-later would not be accessible to earlier Swift versions.

The bounded retention question is therefore not generic upgrade compatibility. It is narrower:

> **what remains invariant when a distributed durability/currentness fact migrates from a separate marker inode into the filename of a payload-bearing fragment archive?**

This record does **not** claim that the two representations are byte-for-byte equivalent, that every mixed-version deployment is safe, that rename is universally crash-atomic on every filesystem, or that Swift 2.11.0 changed the mathematical erasure code.

---

## Source set

### P1 — lower-version Newton patch line retaining the separate `.durable` representation

OpenStack Swift `2.10.1`, annotated tag dated **2016-12-13T19:15:44Z**, series metadata `newton`, target commit `3129a55d4418e0dc4207c2026e7ef8c59704c6a1`:

<https://github.com/openstack/swift/tree/2.10.1>

Its `doc/source/overview_erasure_code.rst` describes the older representation:

```text
<timestamp>#<frag_index>.data
<timestamp>.durable
```

and says commit confirmation causes an object server to create `ts.durable`.

**Chronology guardrail:** although the 2.10.1 patch release was tagged after 2.11.0 in wall-clock time, it belongs to the older `newton` release line and retains the old on-disk representation. It must not be treated as a chronological successor of the 2.11.0 format change merely because its tag date is later.

### P2 — implementation change, 10 October 2016

OpenStack Swift commit `b13b49a27caac17ae55b19f315d5ce31801c9522`, **2016-10-10**, `EC - eliminate .durable files`:

<https://github.com/openstack/swift/commit/b13b49a27caac17ae55b19f315d5ce31801c9522>

The commit message states the design change directly:

- stop creating a separate `.durable` file for new commits;
- rename the fragment archive to include `#d` in its filename;
- save one inode for every EC fragment archive;
- make suffix hashing produce the same consistency state for the new durable-data filename and the legacy `.durable` representation;
- retain test scenarios for both representations because legacy `.durable` files remain in deployed clusters.

### P3 — Swift 2.11.0 annotated release tag, 18 November 2016

The annotated `2.11.0` tag was created by the OpenStack Release Bot on **2016-11-18T16:26:02Z**, identifies series `ocata`, and points to release commit `bf473ddc9d3fcb3a3fe516b5221a588c5b196a1d`:

<https://github.com/openstack/swift/tree/2.11.0>

This establishes that P2 reached a tagged release.

### P4 — Swift 2.11.0 release note

`releasenotes/notes/2_11_0_release-ac1d256e455d347e.yaml` at tag `2.11.0`:

<https://github.com/openstack/swift/blob/2.11.0/releasenotes/notes/2_11_0_release-ac1d256e455d347e.yaml>

The release note says:

- the separate `.durable` file is replaced for new writes by a durable marker in the `.data` filename;
- the purpose includes saving one inode per EC `.data` file;
- existing `.durable` files are **not removed** and continue to work;
- after writing EC data with Swift 2.11.0 or later, that data is **not accessible to earlier versions of Swift**.

The last point is crucial: compatibility is intentionally asymmetric.

### P5 — Swift 2.11.0 EC overview

`doc/source/overview_erasure_code.rst` at tag `2.11.0`:

<https://github.com/openstack/swift/blob/2.11.0/doc/source/overview_erasure_code.rst>

The document makes the new on-disk encoding and commit transition explicit:

```text
first phase:
    <ts>#<frag_index>.data

second-phase commit:
    rename -> <ts>#<frag_index>#d.data
```

It also records the legacy representation in a note and continues to define GET success in terms of a same-timestamp coded cohort plus at least one durable fragment archive at that timestamp.

### P6 — Swift 2.11.0 `swift/obj/diskfile.py`

<https://github.com/openstack/swift/blob/2.11.0/swift/obj/diskfile.py>

The implementation provides the strongest representation-migration evidence:

- `make_on_disk_filename(... durable=True)` adds `#d` to EC `.data` names;
- `parse_on_disk_filename()` returns a boolean `durable` flag for filenames carrying that marker;
- `_finalize_durable()` uses `os.rename()` from the non-durable data filename to the durable filename and then `fsync_dir()`;
- `_process_ondisk_files()` still recognizes legacy `.durable` files;
- a newer `#d` data file can define the durable timestamp in the presence of an older legacy marker;
- an isolated legacy `.durable` without a matching durable fragment set is treated as obsolete;
- `_update_suffix_hashes()` deliberately maps either representation to the abstract string `<timestamp>.durable` when updating the durability hash bucket.

That final normalization is direct implementation evidence that Swift's consistency engine distinguishes the **abstract durable state** from its concrete filename/inode representation.

---

## Historical record (`H/P`)

### H/P1 — before the change, durability was represented by an additional inode

In the old form retained by the 2.10.1 Newton branch, a fragment archive such as:

```text
1418673556.92690#5.data
```

was accompanied by:

```text
1418673556.92690.durable
```

The marker was timestamp-scoped rather than fragment-index-scoped. Commit confirmation created the marker after the first-phase fragment write.

### H/P2 — the 2016 change moves the marker into the fragment filename

P2 and P5 document a different namespace transition:

```text
<ts>#<fi>.data
    -- commit -->
<ts>#<fi>#d.data
```

The payload-bearing fragment remains the object being renamed. No second zero-byte marker inode is needed for the new representation.

### H/P3 — the stated implementation motivation includes inode economy

P2/P4 explicitly say the new representation saves **one inode for every EC `.data` file**.

This is a concrete engineering reason, not a retrospective philosophical explanation. The source does not say the change was made to alter erasure-code mathematics or client-visible object semantics.

### H/P4 — legacy durability state remains readable by the new implementation

P4 says existing `.durable` files are not removed and continue to work. P6 implements that promise by recognizing `.durable` alongside new durable filenames.

Therefore the release does not require an eager, cluster-wide rewrite of every old durability witness merely to upgrade the reader.

### H/P5 — the consistency engine normalizes old and new physical representations

P2/P6 explicitly normalize the durable portion of suffix hashing to the same abstract `<timestamp>.durable` string whether durability is observed as:

```text
<t>.durable + <t>#<fi>.data
```

or as:

```text
<t>#<fi>#d.data
```

The commit message explains the intended consequence: a fragment reconstructed across old/new representations can appear in the same state to the consistency engine.

### H/P6 — compatibility is one-way, not symmetric

P4 warns that EC data written with Swift 2.11.0 or later is not accessible to earlier versions.

Thus:

```text
new Swift reads legacy durability representation
    !=
old Swift reads new durability representation
```

The change supports forward migration of old retained state into a newer software environment, but it does not preserve downgrade readability for newly written state.

### H/P7 — wall-clock release order and format generation do not form one simple line

P3 tags 2.11.0/Ocata on **2016-11-18**. P1 tags 2.10.1/Newton on **2016-12-13**, almost a month later, yet 2.10.1 still documents the old separate `.durable` representation.

This is ordinary release-branch behavior, but it matters for source criticism:

```text
later tag date
    !=
newer on-disk-format generation
```

Version/series lineage must be retained when reconstructing storage semantics.

---

## Engineering reconstruction (`E`)

### E1 — durability relation != durability representation

Across the bounded 2.10/2.11 boundary, the service still needs a retained fact that a timestamped coded cohort has crossed the commit condition. What changes is how that fact is embodied locally.

```text
2.10-style:
    payload fragment + separate marker inode

2.11-style:
    payload fragment whose filename includes #d
```

The invariant is not a particular inode layout. It is the relation used by object-server/proxy/reconstructor logic to identify a durable timestamped fragment set.

### E2 — control metadata can migrate into the namespace of a payload-bearing object

In the old form, durability is represented by a separate zero-byte file. In the new form, the same kind of control distinction is encoded in the **name** of a fragment archive.

That does not make the control fact identical to the fragment payload. A change to the filename still changes how the implementation interprets the fragment's protocol state.

### E3 — logical state equivalence can be stronger than byte-level representation identity

Swift's suffix-hash normalization is a concrete implementation of this distinction:

```text
legacy fileset A
    != byte-for-byte/filesystem-identical to
new fileset B

but

consistency-state(A)
    == consistency-state(B)
```

for the bounded durability relation Swift intentionally normalizes.

This is not a claim that every property of A and B is equivalent; inode count and downgrade readability plainly differ.

### E4 — representation migration can be lazy

Because new software continues to understand old `.durable` files and the release note says they are not removed, upgrade does not require every old object to be rewritten into `#d.data` immediately.

The useful project relation is:

```text
reader understands old representation
    -> old state may remain physically old-form
       while still participating in current service semantics
```

This is a bounded example of **semantic continuity without eager physical normalization**.

### E5 — maintenance-state migration has a compatibility direction

The release boundary makes an important asymmetry visible:

```text
old durable witness
    -- readable by new code -->
continued service

new durable witness
    -- not readable by old code -->
downgrade boundary
```

Therefore `representation migration succeeded` must be qualified by **which software generation is doing the interpreting**.

### E6 — commit operation changed even though the higher-level durability role remained

The old design's commit-side local action creates/fsyncs a separate durable-state file. The new design renames the data file and fsyncs the directory.

Thus:

```text
same higher-level role
    !=
same local write primitive
```

This record does not infer more than the source establishes. In particular, it does not promote `os.rename() + fsync_dir()` into a universal proof of crash atomicity across all supported filesystems and failure modes.

### E7 — a retained-state schema can itself be part of the retention dependency chain

After 2.11.0 writes the new filename form, an older Swift implementation cannot interpret those EC files through its normal path. Payload bytes may physically remain, but the software generation lacks the schema/filename semantics needed to admit them.

So in this bounded case:

```text
payload embodiment survives
    !=
older interpreter can recover the service-level object
```

This is a compatibility/access claim, not a claim that the bytes become physically destroyed.

---

## Functional analogies (`A`) — bounded only

### A1 — Case 04 mapped Flash

Case 04 shows logical identity surviving changes in physical Flash location through retained mapping state. Case 25's 2.11.0 change instead preserves a durability/currentness relation while changing **its metadata representation**.

The analogy is only:

> a service-visible invariant can survive while the lower-level embodiment used to carry the invariant changes.

There is no shared algorithm or historical genealogy.

### A2 — Case 100 ZFS DTL persistence

Case 100 separates a durable maintenance basis from runtime-derived maintenance views. This Swift slice separates a durability/currentness fact from two concrete on-disk encodings of that fact.

The common comparison is that **control state may be reconstructed/interpreted through a representation layer rather than equated with one physical file shape**. ZFS DTL and Swift EC durability markers are otherwise different mechanisms.

### A3 — preservation-format migration

There is a broad functional resemblance to file-format migration: newer software deliberately reads an older representation while producing a new one. The resemblance stops at that function. Swift's EC marker migration is an internal object-server format change, not an archival migration policy and not evidence of OAIS provenance practice.

---

## Philosophical interpretation (`I`) — deliberately narrow

The technical record supports one modest observation:

> **continuity of a retained relation does not require continuity of its material encoding, but it does require an interpreter that still knows how to recognize the encoding in use.**

Swift makes this unusually concrete because the project deliberately maps two filesystem layouts to one consistency-engine durability state while simultaneously publishing a downgrade incompatibility for newly written data.

This does not make filenames philosophical memory objects. It does not establish a general theory of identity across all migrations. The historical claim remains the 2016 Swift representation change and compatibility contract.

---

## Counterexamples and stop conditions (`X`)

- **`#d` != a new erasure-code fragment type.** It marks durable status in the filename; coding mathematics is not changed by this evidence.
- **new representation != new quorum semantics.** This slice is about representation of the durability witness, not a claim that 2.11.0 invented a different coding threshold.
- **one durable fragment filename != every fragment locally marked durable.** The 2.11.0 GET documentation still permits a usable same-timestamp cohort when at least one returned fragment supplies durability evidence.
- **legacy-readable != downgrade-safe.** The release note explicitly warns that older Swift cannot access EC data written by 2.11.0-or-later.
- **legacy support != eager conversion.** Existing `.durable` files are said not to be removed and continue to work.
- **hash equivalence != byte/filesystem equivalence.** Swift intentionally normalizes a durability relation for consistency-engine comparison; inode count and filenames remain different.
- **rename != universal crash-atomicity proof.** The inspected implementation uses `os.rename()` and `fsync_dir()`; broader filesystem guarantees are not established here.
- **later wall-clock release != newer format generation.** 2.10.1/Newton was tagged after 2.11.0/Ocata yet retains the old representation.
- **format incompatibility != payload destruction.** The release note describes accessibility by older software, not physical disappearance of fragment bytes.
- **one Swift migration != universal distributed-storage migration law.** Other systems may use explicit metadata databases, journals, versioned schemas, or completely different upgrade contracts.

---

## Claim ledger

| Claim | Source | Layer | Strength |
| --- | --- | --- | --- |
| legacy Swift represented EC durability with `<timestamp>.durable` | P1 | H/P | direct |
| commit `b13b49a2` changes new durability representation to `#d.data` | P2 | H/P | direct |
| the stated motivation includes saving one inode per EC data file | P2/P4 | H/P | direct |
| 2.11.0 was tagged 2016-11-18 on the Ocata series | P3 | H/P | direct |
| existing `.durable` files are retained and continue to work | P4/P6 | H/P | direct |
| 2.11.0 commit finalization renames `.data` to `#d.data` and fsyncs the directory | P5/P6 | H/P | direct |
| 2.11.0 parser/process logic recognizes both new and legacy durability representations | P6 | H/P | direct |
| suffix hashing normalizes either representation to the same abstract durability hash update | P2/P6 | H/P | direct |
| data written with 2.11.0+ is not accessible to earlier Swift versions | P4 | H/P | direct |
| 2.10.1/Newton was tagged later in wall-clock time yet retained the old representation | P1/P3 | H/P | direct |
| durability relation is separable from the concrete inode/filename representation | P1–P6 | E | strong reconstruction |
| migration compatibility is directional rather than symmetric | P4/P6 | E | strong reconstruction |
| semantic continuity can coexist with lazy retention of old physical representation | P4/P6 | E | strong reconstruction |
| interpreter/schema compatibility is part of service-level recoverability | P4/P6 | E/I | bounded synthesis |

---

## Explicit non-claims

This addendum does **not** establish that:

1. Swift invented marker-file commits, namespace encoding, rolling upgrades, or metadata migration;
2. `.durable` and `#d` are byte-for-byte or filesystem-identical;
3. every old `.durable` layout is retained forever by all later Swift versions;
4. every mixed 2.10/2.11 deployment ordering is supported;
5. downgrade after any 2.11 write is safe;
6. `os.rename()` alone proves crash durability;
7. the `#d` marker is payload data;
8. every fragment in a committed cohort must carry `#d` locally;
9. the migration changes Reed–Solomon coding parameters;
10. a suffix-hash match proves all object bytes are valid;
11. 2.10.1 is historically later in format lineage merely because its tag date is later;
12. the release-note compatibility warning means fragment bytes were physically destroyed;
13. this is a generic archival-format migration case;
14. current Swift still has exactly the same implementation details as 2.11.0;
15. the representation change by itself proves a production incident or data-loss event.

---

## Related-repository check

A current GitHub search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `OpenStack Swift` returned no dedicated treatment to reuse.

Routing remains:

- broad Swift release/upgrade history, filesystem namespace design, or general object-storage implementation history -> `computing-archaeology` if developed there;
- this bounded comparison of **durability/currentness semantics, representation migration, compatibility direction, and consistency-state normalization** -> `technical-retention`.

The existing Case 25 grounding remains authoritative for 2015–2016 quorum/currentness semantics. This addendum only deepens the on-disk representation boundary.

---

## Remaining evidence debt

This slice closes the narrow question `did Swift migrate the durability witness from a separate marker file to a filename marker while retaining legacy readability?`.

Still open:

- an operator-facing rolling-upgrade document that specifies safe mixed-version ordering around the 2.11.0 EC format boundary;
- probe-test or production trace showing a real object directory containing legacy and new durability representations during upgrade;
- a bounded fault-injection trace across the commit rename/fsync sequence;
- later genealogy for when/if legacy `.durable` support was changed or retired;
- independent operational evidence for how frequently downgrade incompatibility mattered in deployed clusters.

None is required for the narrower representation-migration result above.

---

## Sources

1. OpenStack Swift `2.10.1` annotated tag, Newton series, tagger date 13 December 2016: <https://github.com/openstack/swift/tree/2.10.1>
2. OpenStack Swift 2.10.1, `doc/source/overview_erasure_code.rst`: <https://github.com/openstack/swift/blob/2.10.1/doc/source/overview_erasure_code.rst>
3. OpenStack Swift commit `b13b49a27caac17ae55b19f315d5ce31801c9522`, 10 October 2016, `EC - eliminate .durable files`: <https://github.com/openstack/swift/commit/b13b49a27caac17ae55b19f315d5ce31801c9522>
4. OpenStack Swift `2.11.0` annotated tag, Ocata series, tagger date 18 November 2016: <https://github.com/openstack/swift/tree/2.11.0>
5. OpenStack Swift 2.11.0 release note: <https://github.com/openstack/swift/blob/2.11.0/releasenotes/notes/2_11_0_release-ac1d256e455d347e.yaml>
6. OpenStack Swift 2.11.0, `doc/source/overview_erasure_code.rst`: <https://github.com/openstack/swift/blob/2.11.0/doc/source/overview_erasure_code.rst>
7. OpenStack Swift 2.11.0, `swift/obj/diskfile.py`: <https://github.com/openstack/swift/blob/2.11.0/swift/obj/diskfile.py>
