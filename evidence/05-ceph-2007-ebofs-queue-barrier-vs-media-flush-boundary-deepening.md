# Case 05 — Ceph 2007 EBOFS queue barrier versus media-persistence barrier

## Status

- Case: 05, RADOS replicated objects.
- Source baseline: Ceph commit `c93efe01c518c2e90ba62245352baaac5fa675f2`, 5 September 2007.
- Lower-layer comparison: Linux v2.6.22 block-layer barrier documentation.
- Maturity remains **grounded**.

## Historical record

The existing EBOFS packet left `dev.barrier()` as an explicit lower-layer evidence debt. Direct inspection closes its source-level meaning.

In `Ebofs::commit_thread_entry()`, EBOFS starts prior-epoch inode and B-tree writes, calls `dev.barrier()`, waits for buffer-cache, inode, and node-pool work to finish, then writes the alternating checkpoint superblock with a blocking `dev.write()`, and only afterwards calls `journal->commit_epoch_finish()`.

Ceph's own `BlockDevice.h` defines `BarrierQueue::barrier()` as forcing completion of prior I/O before future I/O is started. The implementation creates a later `ElevatorQueue`; dequeue remains on the front queue until it empties. This is a Ceph scheduler/order boundary.

On Linux, `BlockDevice::open_fd()` opens the raw device with `O_RDWR|O_SYNC|O_DIRECT`. Low-level writes use aligned `writev()`; Ceph produces completion after that call returns. The inspected `BlockDevice.cc` contains no explicit `REQ_HARDBARRIER`, `REQ_FUA`, `blkdev_issue_flush`, `fsync()`, or `fdatasync()` call.

Linux v2.6.22's `Documentation/block/barrier.txt` uses **I/O barrier** for a stronger block-layer relation: request ordering plus forced flushing to physical medium when a volatile write-back cache requires it. The same tree exposes `REQ_HARDBARRIER`, `REQ_FUA`, ordered modes, and `blkdev_issue_flush()`.

Therefore:

    Ceph BlockDevice::barrier()
        = queue-order boundary between Ceph I/O subqueues

    Linux hard I/O barrier
        = ordered block request
          + cache flush / FUA semantics where required

    same word "barrier"
        != same primitive
        != same persistence guarantee

## Engineering reconstruction

Project-level predicates:

    queue-order completion
        != BlockDevice/syscall completion
        != media-persistence completion under a stated failure model

The source establishes deliberate software ordering and completion: prior EBOFS work is ordered and explicitly waited before the checkpoint superblock write. It does not, by source inspection alone, prove that arbitrary 2007 controller/device volatile caches have reached nonvolatile media.

So:

    queue drained != volatile device cache necessarily flushed
    write syscall completed != universal proof of power-loss persistence
    software checkpoint order != hardware persistence order for every storage stack
    Ceph "barrier" != Linux REQ_HARDBARRIER

The converse overclaim is also rejected. Absence of an explicit hard-barrier call is not proof that EBOFS must lose data; `O_SYNC|O_DIRECT` is positive evidence of synchronous/direct-I/O intent. Exact power-loss behavior needs the lower Linux path plus a named device/controller/cache configuration.

These labels are engineering reconstructions, not period Ceph or Linux vocabulary.

## Functional analogy

Later repository cases also separate operation completion, persistence-boundary arrival, and crash-consistency closure. The comparison is functional only: no historical descent or equivalent hardware/failure model is claimed.

## Philosophical interpretation

The technical fact is that one write may be "complete" at several interfaces. It can be complete enough for a scheduler or checkpoint state machine to advance while sudden-power-loss survivability still depends on a deeper persistence boundary.

Bounded interpretation: **completion is relative to an interface and a failure model.**

## What this closes

This closes the earlier EBOFS packet's source-level `dev.barrier()` ambiguity:

- it partitions/drains Ceph I/O queues;
- it is not itself the contemporary Linux hard-barrier/flush interface;
- EBOFS separately waits for earlier writes before the blocking superblock write;
- software ordering evidence must not be promoted into an arbitrary-hardware power-loss guarantee.

## Remaining evidence debt

1. Trace Linux v2.6.22 `O_SYNC|O_DIRECT` block-device writes through direct I/O and request completion if a stronger kernel-level claim is needed.
2. Use a named controller/disk/cache configuration before making a stronger power-cut claim.
3. Broad Linux-barrier, EBOFS/FileStore, and drive-cache genealogy remains `computing-archaeology` work. Fresh searches there found no dedicated reusable packet.

## Primary sources

- Ceph commit: https://github.com/ceph/ceph/commit/c93efe01c518c2e90ba62245352baaac5fa675f2
- Ceph `BlockDevice.h`: https://github.com/ceph/ceph/blob/c93efe01c518c2e90ba62245352baaac5fa675f2/trunk/ceph/ebofs/BlockDevice.h
- Ceph `BlockDevice.cc`: https://github.com/ceph/ceph/blob/c93efe01c518c2e90ba62245352baaac5fa675f2/trunk/ceph/ebofs/BlockDevice.cc
- Ceph `Ebofs.cc`: https://github.com/ceph/ceph/blob/c93efe01c518c2e90ba62245352baaac5fa675f2/trunk/ceph/ebofs/Ebofs.cc
- Linux v2.6.22 barrier documentation: https://github.com/torvalds/linux/blob/v2.6.22/Documentation/block/barrier.txt
- Linux v2.6.22 block definitions: https://github.com/torvalds/linux/blob/v2.6.22/include/linux/blkdev.h
- Linux v2.6.22 block-device path: https://github.com/torvalds/linux/blob/v2.6.22/fs/block_dev.c

## Bounded result

> The September-2007 EBOFS source proves a deliberate software ordering/completion protocol, but `dev.barrier()` is a Ceph queue barrier, not the Linux hard I/O barrier primitive. Queue ordering, write completion, and media-persistence completion remain separate retention predicates.
