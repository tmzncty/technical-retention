# Case 81 grounding — Chain Replication, OSDI 2004

## Research question

What exactly must remain between an update's arrival at a replicated storage chain and the point at which the protocol can treat that update as completed, and how does the 2004 Chain Replication design preserve that relation when a replica fails or a new tail is added?

This record is intentionally retention-specific. It is not a general replication history and makes no invention-priority claim for primary/backup, state-machine replication, acknowledgements, or failover.

---

## Source ledger

### P1 — van Renesse & Schneider, OSDI 2004 full paper

**Source:** Robbert van Renesse and Fred B. Schneider, “Chain Replication for Supporting High Throughput and Availability,” *OSDI 04*, USENIX Association.

**Full HTML:** <https://www.usenix.org/legacy/events/osdi04/tech/full_papers/renesse/renesse_html/>

**Directly inspected locations:**

- **§2 / Figure 1:** formal client-view state `Hist_objID` and `Pending_objID`; client retry and non-idempotent-update warning.
- **§3, normal protocol:** linear chain, `head`, `tail`, tail reply/query role, head update ingress, reliable FIFO propagation, tail serialization.
- **§3, failure handling:** tail-defined `Hist`, internal failure, `Sent_i`, backward `ack(r)`, missing-suffix repair, `Update Propagation Invariant`, `Inprocess Requests Invariant`.
- **§3, extending a chain:** state transfer from old tail, concurrent `Sent_T` accumulation, invariant closure, then tail/master/client role transition.
- **§4:** explicit statement that Chain Replication is a form of primary/backup and primary/backup an instance of the state-machine approach.
- **Endnote 2:** explicit statement that an implementation would probably store the current object value rather than the full update sequence used in the proof.

**Evidence class:** primary / contemporary technical paper (`H/P`).

### P2 — USENIX proceedings record

**Source:** USENIX, “Chain Replication for Supporting High Throughput and Availability.”

**URL:** <https://www.usenix.org/conference/osdi-04/chain-replication-supporting-high-throughput-and-availability>

**What it establishes:**

- publication venue: 6th Symposium on Operating Systems Design & Implementation (OSDI 04);
- authors: Robbert van Renesse and Fred B. Schneider;
- year/month: 2004 / December;
- institutional proceedings metadata and links to the paper.

**Evidence class:** institutional bibliographic record (`H/P`).

### P3 — author retrospective boundary

**Source:** Robbert van Renesse, Cornell home page, “Chain Replication” section.

**URL:** <https://www.cs.cornell.edu/people/rvr/>

**Use:** later authorial confirmation that the protocol was published with Schneider at OSDI 2004 and that later work addressed original-protocol dependence on a configuration service.

**Boundary:** this retrospective is not used to rewrite the 2004 mechanism or to claim production deployment details.

**Evidence class:** author retrospective / institutional page (`H/S`).

---

## Claim matrix

| Claim | Type | Grounding |
| --- | --- | --- |
| replicas for one object are linearly ordered; first is head, last is tail | `H/P` | P1 §3 |
| queries go to the tail; updates enter at the head and flow toward the tail | `H/P` | P1 §3 |
| tail serialization is the paper's basis for the strong-consistency argument | `H/P` | P1 §3 |
| client-view `Hist_objID` is tied to the tail while `Pending_objID` includes requests not yet tail-processed | `H/P` | P1 §§2–3 |
| every server retains forwarded, possibly not-yet-tail-processed updates in `Sent_i` | `H/P` | P1 §3 |
| tail completion sends `ack(r)` backward; receiving servers delete `r` from `Sent_i` | `H/P` | P1 §3 |
| internal-failure reconnection transfers the missing suffix before normal forwarding continues | `H/P` | P1 §3 |
| successor sequence-number evidence can avoid resending an already-received prefix | `H/P` | P1 §3 |
| a new tail is initialized by old-tail state transfer while concurrent updates accumulate in `Sent_T` | `H/P` | P1 §3 |
| new-tail role begins only after the paper's invariant is established and configuration/client direction changes | `H/P` | P1 §3 |
| lost reply is distinct from update execution; retries of non-idempotent updates require care | `H/P` | P1 §2 |
| the proof's full `Hist` sequence is not a required implementation representation | `H/P` | P1 endnote 2 |
| `Sent_i` can be reconstructed as temporary forwarding/recovery obligation state | `E` | follows from P1's add/ack-delete/failure-suffix use |
| safe deletion from `Sent_i` is not deletion of the object payload | `E` | follows from P1's separate object history/state and Sent semantics |
| state transfer alone does not confer tail authority | `E` | follows from P1 extension protocol + master/client role transition |
| Chain Replication is not treated here as invention of primary/backup/state-machine replication | `X/H` | P1 §4 explicitly places it inside those prior-art families |

---

## Retention decomposition

### Payload continuity

Each live replica contains object state corresponding to a prefix of the ordered update stream. The physical storage implementation beneath a server is outside this case.

### Currentness / completion continuity

The paper's service specification takes the tail's state as the current completed history for the client view.

### In-process continuity

`Sent_i` preserves exactly a different relation: work already forwarded whose completion at the tail may not yet be known. This information becomes useful when an internal chain edge must be repaired.

### Configuration continuity

The master-provided predecessor/successor/head/tail relation determines where an otherwise surviving replica may act.

### Recovery continuity

Internal-failure repair uses successor progress plus predecessor `Sent` state to close only the missing suffix. Chain extension uses old-tail state transfer plus concurrent-delta retention before role admission.

---

## Prior-art control

The OSDI paper is unusually explicit about its own genealogy:

- Chain Replication is described as a **form of primary/backup**.
- Primary/backup is described as an **instance of the state-machine approach**.
- The paper contrasts the distribution/sequencing roles rather than claiming to invent replication itself.

Therefore reject:

- `Chain Replication invented primary/backup`;
- `Chain Replication invented replicated storage`;
- `Chain Replication invented acknowledgement-based replication`;
- `Chain Replication invented state-machine replication`.

The bounded historical contribution asserted here is the specific 2004 organization of head/tail roles, tail-qualified completion, `Sent`-based in-process retention, and invariant-preserving reconfiguration.

---

## Cross-repository duplication check

A GitHub search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Chain Replication van Renesse Schneider` returned no dedicated case in this run.

**Decision:** keep the retention-specific decomposition here. If a broader replication genealogy is later developed, place the historical engineering narrative in `computing-archaeology` and link back rather than copying it.

---

## Rejected overclaims

- `tail = only physical copy` — false; it is one replica with a specific protocol role.
- `head processing = completed update` — false in the paper's client-view specification.
- `tail processing = client definitely received success` — false; reply loss and retry are separate.
- `Sent_i = application history` — unsupported; it is bounded in-process/recovery control state.
- `Hist proof sequence = implementation must preserve complete update history` — explicitly rejected by the paper's endnote.
- `acknowledgement = secure persistence to physical media` — unsupported at this layer.
- `adding a replica = immediate role admission` — false for the new-tail protocol.
- `removing a failed server = erasing its media` — unsupported.
- `the fail-stop protocol proves partition or Byzantine safety` — outside scope.
- `the prototype/simulation = production deployment proof` — unsupported.

---

## Remaining gaps

Useful future slices, none required for this case's grounded status:

- production implementations such as Hibari and their product-specific stable-storage contracts;
- later CRAQ / chain-replication descendants and read scaling;
- exact master/configuration-service durability and reconfiguration genealogy;
- partition and Byzantine variants;
- fault-injection validation of suffix repair and tail extension;
- composition with filesystem/database persistence and hardware storage guarantees.

---

## Promotion decision

**Case 81 status: `grounded`.**

Reason:

1. the exact protocol is directly described in a contemporary primary paper;
2. the relevant state variables and failure transitions are explicit;
3. the paper itself supplies a strong prior-art boundary;
4. the proof-model-versus-implementation distinction is explicitly documented;
5. the case has clear counterexamples and scope limits;
6. companion-repository duplication was checked.
