# Case 25 deepening — Swift EC SSYNC receiver persistence boundary

**Status:** bounded deepening complete  
**Canonical case:** [`Case 25 — OpenStack Swift EC Overwrites`](../cases/25-openstack-swift-ec-overwrite-durable-currentness.md)  
**Evidence class:** implementation / protocol reconstruction / filesystem-persistence boundary  
**Case maturity:** remains `grounded`

## Purpose

This addendum closes the highest-priority bounded debt left by the current Case 25 evidence index:

> **When an EC SSYNC receiver reports a fragment update as successful, what filesystem persistence work has actually completed before that success is returned, and what does that still fail to prove?**

The question is deliberately narrower than whole-object durability, erasure-code reconstructability, kernel/filesystem crash consistency, block-device power-loss behavior, or handoff source retirement. The preceding Case 25 deepening already established that handoff retirement is gated by per-destination/per-object synchronization evidence. This note moves one layer downward into the receiver and asks what that evidence rests on.

The strongest current implementation evidence is pinned to OpenStack Swift commit:

`6b83d7f3fcf95539b17dc1e3f5f1074c29afc487` — **2026-09-20**.

The bounded result is:

```text
successful durable-fragment SSYNC update
    -> object-server PUT completed
    -> payload + object metadata fsync completed
    -> non-durable fragment pathname published with directory fsync
    -> EC durable-name transition completed with directory fsync
    -> receiver reported update success

but

Swift/OS filesystem persistence work completed
    != empirical proof of survival under every power-loss / device-cache / HBA / firmware failure model
```

A second result is equally important:

```text
filesystem-persisted fragment
    != Swift-qualified durable fragment
```

because SSYNC can intentionally carry a non-durable fragment using `X-Backend-No-Commit: True`: the receiving object server still performs the ordinary file finalization and filesystem sync work, but deliberately skips the EC `commit()` transition that marks the fragment durable in Swift's on-disk state.

---

## Source set

### P1 — current SSYNC sender

Pinned source:

<https://github.com/openstack/swift/blob/6b83d7f3fcf95539b17dc1e3f5f1074c29afc487/swift/obj/ssync_sender.py>

Relevant behavior:

- `Sender.__call__()` performs `missing_check()` and, for ordinary synchronization, `updates()` before returning session success;
- `updates()` sends requested object state and then waits for the receiver's `:UPDATES:` completion response;
- when sending a data fragment, the sender computes whether the source fragment is durable;
- `send_put()` sends `X-Backend-No-Commit: True` only for the less-common non-durable case;
- without that header, the receiver-side object server follows its default commit behavior.

### P2 — current SSYNC receiver

Pinned source:

<https://github.com/openstack/swift/blob/6b83d7f3fcf95539b17dc1e3f5f1074c29afc487/swift/obj/ssync_receiver.py>

Relevant behavior:

- `Receiver.__call__()` runs the missing-check and update phases under the replication lock;
- `updates()` translates received PUT/POST/DELETE records into object-server subrequests;
- subrequest HTTP success counts as success, while failures are accumulated and can abort the session;
- if any failures remain at the end, `updates()` raises an error instead of emitting a clean `:UPDATES: END` response;
- only the no-failure path emits the normal update-completion markers;
- `_check_local()` can make an already-present same-timestamp EC fragment durable locally, without retransmitting its payload, by calling `writer.commit()` and then rechecking local state.

### P3 — current object server PUT path

Pinned source:

<https://github.com/openstack/swift/blob/6b83d7f3fcf95539b17dc1e3f5f1074c29afc487/swift/obj/server.py>

Relevant behavior:

- object bytes are staged through a `DiskFileWriter`;
- the object server calls `writer.put(metadata)` after receiving and checking the body;
- unless `X-Backend-No-Commit` is true, it next calls `writer.commit(request.timestamp)`;
- the writer is closed in `finally`;
- only after these operations does the PUT path proceed to post-commit container updates and return `201 Created`.

### P4 — current diskfile implementation

Pinned source:

<https://github.com/openstack/swift/blob/6b83d7f3fcf95539b17dc1e3f5f1074c29afc487/swift/obj/diskfile.py>

Relevant behavior:

- object payload is first written to a temporary file;
- `BaseDiskFileWriter._finalize_put()` writes object metadata before calling `fsync()` on the file descriptor;
- it then publishes the file at its target pathname with `renamer()` or `link_fd_to_path()`;
- `ECDiskFileWriter.put()` deliberately leaves an EC `.data` fragment non-durable and defers cleanup;
- `ECDiskFileWriter.commit()` renames that EC fragment to the filename form containing the durable marker;
- `_finalize_durable()` then calls `fsync_dir()` on the object data directory before returning.

### P5 — Swift filesystem-sync helpers

Pinned source:

<https://github.com/openstack/swift/blob/6b83d7f3fcf95539b17dc1e3f5f1074c29afc487/swift/common/utils/__init__.py>

Relevant behavior:

- Swift's `fsync(fd)` uses `F_FULLSYNC` where available and otherwise `os.fsync(fd)`;
- `fsync_dir()` opens the directory and syncs its directory entries;
- `renamer(..., fsync=True)` syncs the destination directory, and any newly created parent directories, after the rename;
- `link_fd_to_path(..., fsync=True)` performs analogous directory syncing for the unnamed-temp-file path.

### P6 — pinned source-state identity

The inspected OpenStack Swift commit is:

<https://github.com/openstack/swift/commit/6b83d7f3fcf95539b17dc1e3f5f1074c29afc487>

The commit timestamp is **2026-09-20 06:33:32 UTC**. This note treats that SHA as a current implementation witness. It does not project this exact call ordering backward onto Swift 2.3.0, 2.10.1, or every historical EC release.

---

## Historical / implementation record (`H/P`)

The labels in this section describe directly inspected implementation behavior at the pinned source state. They are not claims that Swift has always behaved identically.

### H/P1 — SSYNC receiver success is downstream of object-server subrequest success

The receiver's update phase does not merely acknowledge receipt of network bytes. It constructs backend PUT/POST/DELETE subrequests and executes them against the object server.

For each subrequest:

```text
SSYNC receiver parses update
    -> constructs backend subrequest
    -> subreq.get_response(object server)
    -> inspects HTTP status
```

HTTP success increments the receiver's success count. A failed subrequest increments the failure count; too many failures abort the exchange, and any remaining failure count at the end causes an error rather than a clean update completion.

Therefore:

```text
SSYNC bytes arrived at receiver
    != object-server update succeeded

object-server update failed
    != clean SSYNC update completion
```

The prior handoff-retirement deepening used this boundary at the protocol level. This addendum now traces what the successful PUT itself contains.

### H/P2 — a durable source fragment is sent without `X-Backend-No-Commit`

On the sender, when SSYNC decides to transmit a data fragment, it compares the source diskfile's durable timestamp and data timestamp.

The send path is effectively:

```text
is_durable := (durable_timestamp == data_timestamp)

if is_durable:
    send PUT normally
else:
    send PUT with X-Backend-No-Commit: True
```

The comment in `send_put()` states that the header is sent only for the less-common non-durable case; without it, object servers assume their default commit behavior.

This distinction lets the protocol preserve **durability state**, rather than treating every copied fragment as durable merely because bytes were transferred.

### H/P3 — object-server PUT finishes `writer.put()` before it can return success

The object-server PUT path stages the request body into a diskfile writer, constructs metadata, then calls:

```text
writer.put(metadata)
```

before it can reach the successful return.

For the normal POSIX diskfile implementation, `writer.put()` is not just an in-memory association. It drives `_finalize_put()` in the thread pool.

### H/P4 — `_finalize_put()` fsyncs payload and metadata before pathname publication

`BaseDiskFileWriter._finalize_put()` first writes the object's metadata to the same file descriptor. Its source comment explicitly says this occurs before `fsync()` so that **both data and metadata are flushed to disk**.

The sequence is:

```text
temporary file contains received payload
    -> write object metadata / xattrs
    -> fsync(file descriptor)
    -> drop cache hint
    -> invalidate suffix hash
    -> rename/link temporary file into object pathname
```

For large objects, `write()` may also issue intermediate `fdatasync()` calls according to `bytes_per_sync`; those are incremental writeback operations, not the final persistence boundary used here. The final file `fsync()` is the important bounded witness.

### H/P5 — ordinary pathname publication is followed by directory syncing

The named-temp-file branch calls `renamer()` with the helper's default `fsync=True`. The unnamed `O_TMPFILE` branch calls `link_fd_to_path()` with its default `fsync=True`.

Both helpers synchronize the destination directory after publishing the file and also synchronize newly created parent directories where needed.

Thus current Swift does not stop at:

```text
fsync(temp file)
    -> rename
    -> return
```

The current implementation additionally carries out directory-entry sync work after the rename/link.

This matters because file-content persistence and namespace-entry persistence are different filesystem obligations.

### H/P6 — an EC `put()` first publishes a non-durable fragment state

`ECDiskFileWriter.put()` differs from the replicated-policy writer in one important respect: for an EC data fragment it calls the base `_put()` with cleanup deferred.

At this point, Swift has a receiver-side fragment whose payload/metadata file has undergone the file-finalization path and whose pathname has been published, but the EC fragment has not yet undergone `ECDiskFileWriter.commit()`.

That gives a concrete state distinction:

```text
received EC fragment published on filesystem
    != EC fragment marked durable by Swift
```

This distinction is not philosophical wording imposed on the code. The implementation has separate operations for `put()` and `commit()` and exposes the difference through EC on-disk naming/currentness behavior.

### H/P7 — normal durable SSYNC PUT calls EC `commit()` before `201 Created`

After `writer.put(metadata)`, the object server checks `X-Backend-No-Commit`.

If the flag is absent or false, it calls:

```text
writer.commit(request.timestamp)
```

For an EC diskfile, `commit()` computes the non-durable and durable paths and calls `_finalize_durable()`.

Only after this returns can the PUT path eventually return `HTTPCreated`.

Therefore, on the current durable-fragment SSYNC path:

```text
object-server 201
    is downstream of
EC writer.commit() returning
```

### H/P8 — EC `commit()` renames to durable state and fsyncs the object directory

`ECDiskFileWriter._finalize_durable()` performs:

```text
os.rename(data_file_path, durable_data_file_path)
fsync_dir(self._datadir)
```

before it treats the durable-finalization operation as complete.

In current Swift, the durable marker is encoded in the EC fragment filename. The rename therefore changes the filesystem representation by which the fragment participates in Swift's durable/current state.

The subsequent directory fsync means:

```text
durable-name transition issued
    != durable-name transition finalization returned
```

There is an explicit filesystem sync operation between those two moments.

### H/P9 — a successful durable-fragment SSYNC update therefore crosses two separate sync boundaries

Combining P2–P5, the normal current path for a durable fragment is:

```text
sender identifies source fragment as durable
    -> SSYNC PUT without X-Backend-No-Commit

receiver routes PUT to object server
    -> receive payload into temporary file
    -> write object metadata
    -> fsync(fragment file)
    -> publish non-durable fragment pathname
    -> fsync destination directory path(s)
    -> EC commit renames fragment to durable-name form
    -> fsync object data directory
    -> object server returns HTTP success
    -> receiver counts subrequest success
    -> receiver emits clean :UPDATES: completion
    -> sender accepts SSYNC update phase as successful
```

The file fsync and durable-name directory fsync serve different state transitions:

```text
file fsync
    -> payload + file metadata persistence request

directory fsync after durable rename
    -> persistence request for the namespace/currentness transition
```

It would be incorrect to collapse them into one generic `write completed` event.

### H/P10 — non-durable SSYNC deliberately skips the EC durable-state transition

If the source fragment is not durable, the sender adds:

```text
X-Backend-No-Commit: True
```

The receiver forwards the subrequest to the object server. The object-server PUT still executes `writer.put(metadata)`, including the ordinary file finalization path, but skips `writer.commit()`.

Therefore current Swift can have:

```text
received file content + metadata fsynced
    + pathname published/synced
    + successful object-server PUT

while

EC durable-name transition intentionally not performed
```

This is one of the strongest distinctions in this slice:

> **filesystem persistence work is not identical to Swift's EC durability qualification.**

A fragment can be deliberately retained on disk in a non-durable state.

### H/P11 — an already-present fragment may be promoted to durable without payload retransmission

The receiver's `_check_local()` has a separate optimization/repair path. If:

- the receiver already has the exact offered fragment;
- that fragment is newer than anything durable locally; and
- the remote side says the offered fragment is durable;

then the receiver can open a writer and call:

```text
writer.commit(remote['ts_data'])
```

without receiving the payload again. It then rechecks local state.

If the commit fails, it logs the failure and falls back to asking for a full update.

So:

```text
receiver becomes in-sync for durable state
    != receiver necessarily retransmitted payload in this SSYNC session
```

and, more precisely:

```text
payload embodiment already present
    + durable-state publication missing
    -> commit-only local transition may be sufficient
```

This reinforces the prior Case 25 conclusion that synchronization evidence is not a byte-transfer counter.

---

## Engineering reconstruction (`E`)

### E1 — there are at least three receiver-side persistence states

The current implementation makes it useful to distinguish:

```text
A. payload staged in temporary file
B. fragment file/metadata fsynced and pathname published
C. EC fragment additionally qualified by durable-name state
```

A is transient staging.

B is an on-filesystem fragment embodiment that has crossed Swift's ordinary file-finalization persistence calls.

C is an EC protocol/application state in which the fragment's on-disk representation also carries Swift's durable qualification.

The transitions are not interchangeable:

```text
A -> B
    != B -> C
```

and the existence of B is why a later local commit-only promotion is possible.

### E2 — receiver success is a layered acknowledgement, not a primitive fact

For the current durable-fragment PUT path, the sender-visible SSYNC success sits above several lower layers:

```text
payload received
    -> file write complete in userspace
    -> file fsync completed
    -> namespace publication completed
    -> namespace directory sync completed
    -> EC durable-state rename completed
    -> durable-state directory sync completed
    -> object-server HTTP success
    -> receiver update-phase success
    -> sender session success
```

The higher-level acknowledgement is therefore **constructed from lower-layer completions**.

But the layers retain different scopes. A protocol acknowledgement tells the sender what the Swift receiver stack has accepted and completed; it does not erase the assumptions of the layers below it.

### E3 — Swift durability is stronger than mere file presence but narrower than an all-failure-model theorem

Current Swift deliberately distinguishes:

```text
fragment present in filesystem
    != fragment marked durable in Swift EC state
```

The durable path adds explicit namespace/currentness publication and directory sync after the ordinary file data/metadata fsync.

However, the source code itself cannot prove:

```text
all lower storage layers honored every flush exactly
    + all relevant device caches are power safe
    + every filesystem/kernel/HBA combination provides identical crash semantics
    + every possible power-failure point preserves the state
```

Those are empirical/platform questions outside what the Python implementation alone can establish.

The bounded engineering statement is therefore:

> **Before current Swift reports a normal durable-fragment SSYNC PUT as successful, its POSIX diskfile path has requested and waited for explicit file and directory synchronization at the relevant publication boundaries.**

That statement is strong and source-grounded without pretending it is a hardware conformance test.

### E4 — semantic durability and physical persistence evidence are orthogonal enough to require separate vocabulary

The non-durable SSYNC path demonstrates the distinction directly.

A receiver may have substantial lower-layer persistence work completed while Swift deliberately keeps the fragment semantically non-durable:

```text
physical/filesystem persistence work
    != semantic currentness/durability qualification
```

Conversely, seeing a Swift durable marker after restart is evidence about the software-visible state the implementation created, but source inspection alone still does not establish every possible hardware failure guarantee.

This produces a useful two-axis model:

```text
axis 1: lower-layer persistence evidence
    staged -> fsynced file -> fsynced namespace publication

axis 2: Swift EC qualification
    non-durable -> durable/current for the timestamp/fragment relation
```

### E5 — source retirement depends on a chain of evidence, not one write

Combining this note with the preceding handoff-retirement deepening gives a longer chain:

```text
receiver already has / receives fragment state
    -> receiver establishes required durable/current state
    -> receiver reports per-object synchronization success
    -> reconstructor combines required destination results
    -> local handoff embodiment becomes purge-eligible
```

The handoff source is not retired merely because bytes were put on a socket, nor merely because a target file exists.

The decision rests on a **stacked relation** spanning filesystem persistence actions, Swift EC durability/currentness, SSYNC protocol success, and reconstructor placement policy.

### E6 — the commit-only path separates payload continuity from qualification continuity

When `_check_local()` promotes an already-present non-durable fragment, the payload embodiment can remain unchanged while only its qualification state changes.

That yields:

```text
payload continuity
    != durability/currentness continuity
```

and:

```text
new durable authority
    does not necessarily require
new payload bytes
```

For retention analysis this is useful because the retained object is not only a byte sequence. It includes relations that determine whether a physically present embodiment may count for later service, repair, and retirement decisions.

---

## Functional analogy (`A`)

### A1 — Case 04 mapped Flash: replacement publication before old-embodiment retirement

Functional analogy only:

```text
replacement embodiment exists
    != replacement embodiment is sufficiently published/current
    != old embodiment is disposable
```

Case 25's receiver-persistence path and Case 04's relocation/currentness work both make the retirement boundary depend on more than physical byte presence. They do **not** share a demonstrated historical genealogy or implementation mechanism.

### A2 — Case 88 RAID5 PPL: completion evidence and persistence work are not one bit

A second bounded analogy is with Case 88's separation of asynchronous operation completion, flush success, member authority, and later recovery obligations.

In both cases:

```text
operation observed as complete at one layer
    != all lower or higher retention obligations automatically collapse into that completion
```

The mechanisms are otherwise different: Linux MD PPL protects parity-update crash consistency, while Swift SSYNC transfers and qualifies distributed object-fragment state.

### A3 — repository durability-handoff synthesis

This slice is consistent with the repository-wide distinction already used in durability-handoff work:

```text
completion
    != persistence-boundary arrival
    != application-level crash/recovery correctness
```

Case 25 adds a distributed object-store example where a semantic durable/currentness marker itself has a filesystem publication path beneath it.

---

## Philosophical interpretation (`P`)

The technical fact that creates the conceptual problem is narrow:

> A receiver-side fragment may be physically present and even explicitly fsynced while still not count as `durable` in Swift's EC state; conversely, a higher-level `durable` qualification is established through a chain of lower-layer operations whose ultimate failure model is not exhausted by the word `durable`.

A useful interpretation is therefore that **technical persistence is relational and jurisdictional**: different layers answer different questions about what has been retained and what may now be trusted or retired.

This does not imply that “durability is merely conventional” or that physical storage is irrelevant. The software relation is made possible by concrete file writes, sync operations, directory publication, device behavior, and later protocol checks. The interpretation stops where the source evidence stops.

---

## Explicit non-claims

This addendum does **not** claim any of the following:

1. that `fsync()` is a universal proof of arbitrary power-loss survival on every Linux filesystem, kernel, HBA, RAID controller, drive cache, SSD firmware, or storage medium;
2. that every device correctly honors flush/FUA/cache-control semantics;
3. that the pinned source has been validated here with physical power-cut fault injection;
4. that a successful one-destination SSYNC proves the whole EC object has enough distinct fragments to reconstruct;
5. that one receiver's successful durable fragment establishes the configured cluster redundancy target;
6. that object-server `201 Created` proves container listing metadata is synchronously durable;
7. that Swift's semantic use of `durable` is equivalent to a database transaction commit, consensus commit, POSIX durability theorem, or generic stable-storage abstraction;
8. that a non-durable fragment is useless or immediately reclaimable;
9. that a non-durable fragment's file-level sync work makes it admissible wherever Swift requires durable state;
10. that a durable marker means the payload was retransmitted in the current SSYNC exchange;
11. that the current 2026 implementation order existed unchanged in Swift 2.3.0, 2.10.1, or 2.11.0;
12. that the exact lower-layer persistence contract of every filesystem supported by Swift is identical;
13. that Python source inspection establishes CPU/cache/barrier/device-level electrical ordering beyond the documented syscall path;
14. that `renamer()` / `fsync_dir()` behavior proves a particular filesystem's recovery behavior after every possible torn metadata update;
15. that the sender or receiver persists a separate durable SSYNC session journal containing all per-object synchronization results;
16. that handoff retirement after destination success is crash-atomic with the remote update;
17. that a receiver-side commit-only durable promotion duplicates payload data;
18. that current Swift invented file `fsync`, directory fsync, two-stage EC publication, or durability-marker concepts;
19. that Case 25 is promoted above `grounded` by this slice alone;
20. that functional similarities to Flash remapping, RAID logging, or database commit imply shared genealogy.

---

## What this slice closes

The current implementation evidence now closes the Case 25 bounded debt:

> “Trace a successful SSYNC update through the object server and diskfile implementation far enough to state exactly what filesystem persistence actions occur before the receiver reports success.”

For the pinned 2026 implementation, the normal durable-fragment path is now grounded through:

- sender durable-state selection;
- receiver backend subrequest execution;
- object-server `writer.put()`;
- payload + object-metadata file `fsync()`;
- pathname publication with directory syncing;
- EC durable-name rename;
- object-directory `fsync()`;
- object-server HTTP success;
- receiver clean update completion;
- sender successful session result.

The evidence also closes two adjacent distinctions:

```text
filesystem-persisted fragment
    != Swift-qualified durable EC fragment
```

and:

```text
receiver becomes durably in-sync
    != payload bytes necessarily retransmitted in that exchange
```

Case 25 remains `grounded`.

---

## Remaining bounded debt

This slice narrows rather than eliminates the next research questions.

### 1. Physical power-cut validation of the receiver persistence path

Run or find fault-injection evidence across exact cut points such as:

```text
after file fsync
before pathname publication

after non-durable rename
before durable rename

after durable rename
before directory fsync

after directory fsync
before SSYNC response
```

This would test the difference between the documented syscall/order path and actual restart-visible state on named filesystem/device stacks.

### 2. Crash after remote success but before local handoff purge

The preceding handoff-retirement note leaves this open. The expected question is whether a later reconstructor pass simply rediscovers already-synchronized destination state and safely retries source retirement, but that should be demonstrated from tests/code/fault injection rather than inferred casually.

### 3. Historical evolution of the persistence ordering

Identify when Swift added or changed:

- file `fsync()` before publish;
- directory syncing in rename/link helpers;
- EC durable filename publication;
- SSYNC non-durable transfer semantics;
- local commit-only durable promotion.

The current source is not evidence that every earlier release had identical semantics.

### 4. Lower-stack persistence contract

A future bounded slice may compare Swift's syscall assumptions to named deployment guidance for XFS, controller caches, barriers/flushes, and storage hardware. This should remain a separate infrastructure study rather than being silently inferred from application code.

### 5. Partial success across reconstructor passes

Determine exactly what state a later pass re-observes after some destinations succeeded in an earlier pass and others failed, and whether all continuity comes from receiver disk state rather than retained sender-side session state.

---

## Related-repository check

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for Swift EC / SSYNC found no dedicated packet to reuse.

Accordingly, this file stays narrowly within `technical-retention`: it analyzes the **retention-specific persistence and currentness boundary**. A broad history of OpenStack Swift, SSYNC evolution, filesystems, XFS deployment, storage controllers, or block-device flush semantics would belong primarily in `computing-archaeology` if developed.

---

## Compact result

```text
current Swift EC durable SSYNC receive path:

source durable fragment
    -> SSYNC PUT
    -> temp payload write
    -> object metadata write
    -> fsync(file)
    -> publish non-durable EC fragment pathname
    -> fsync directory path(s)
    -> rename to durable EC filename
    -> fsync object directory
    -> object-server success
    -> receiver update success
    -> sender synchronization success

therefore:

network receipt
    != object-server success

file presence
    != Swift EC durable qualification

Swift durable qualification
    != universal hardware power-loss theorem

SSYNC in-sync result
    != proof that payload bytes moved in this session
```
