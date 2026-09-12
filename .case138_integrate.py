from pathlib import Path
from textwrap import dedent

# Update Case 138.
case_path = Path('cases/138-redis26-aof-rewrite-current-state-reserialization.md')
case = case_path.read_text(encoding='utf-8')
link = 'Automatic-rewrite genealogy deepening: [`../evidence/138-redis-2011-2012-auto-aof-rewrite-genealogy-deepening.md`](../evidence/138-redis-2011-2012-auto-aof-rewrite-genealogy-deepening.md).'
if link not in case:
    marker = 'Grounding record: [`../evidence/138-redis26-aof-rewrite-grounding.md`](../evidence/138-redis26-aof-rewrite-grounding.md).'
    if marker in case:
        case = case.replace(marker, marker + '\n\n' + link, 1)
    else:
        case = link + '\n\n' + case

section_title = '## Historical deepening — manual rewrite vs automatic rewrite policy, 2011 to Redis 2.4'
if section_title not in case:
    deepening = dedent('''

    ## Historical deepening — manual rewrite vs automatic rewrite policy, 2011 to Redis 2.4

    The companion 2011–2012 evidence closes one of this case's original genealogy debts without turning the case into a general Redis history.

    Released Redis **2.2.0** (22 February 2011) already contains `bgrewriteaofCommand()` and `rewriteAppendOnlyFileBackground()`. Its configuration tells operators to use `BGREWRITEAOF` when an append log becomes too large, but the released tree does not expose the later automatic-rewrite percentage/minimum-size policy.

    On **10 June 2011**, public commit `b333e2399778e624174e00d123c2cb3785333e3d` adds automatic AOF rewrite as a policy layer: percentage/minimum-size configuration, remembered base/current AOF sizes, scheduled-rewrite state, and a `serverCron` trigger that can invoke the existing background rewrite path. The commit message itself calls this the first implementation and says it still needs testing.

    The following public history matters methodologically. Within hours and days Redis fixes division-by-zero, option parsing, child-concurrency, and the growth formula; on **12 June 2011** commit `0b17517...` changes the calculation from current-size percentage to **growth above the remembered base**. On **9 August 2011**, `11aaf523...` widens the base arithmetic after an integer-overflow report. Released **2.4.0** (14 October 2011) contains the automatic-rewrite controls and guarded trigger.

    This establishes a bounded chain:

    > `manual/background rewrite mechanism exists` **before** `automatic rewrite policy exists`.

    and:

    > `maintenance threshold due != work admitted now != rewrite completed != replacement installed`.

    The first inequality is grounded by the 2.2→June-2011 source history; the later phases remain grounded by this case's 2.6 handoff analysis. The retained base-size/current-size bookkeeping is maintenance-control state: small state about prior rewrite/startup history that governs a future large representation-maintenance action.

    The chronology is not an invention-priority claim. It does not establish the first Redis AOF or `BGREWRITEAOF` commit, private experiments, or broader database checkpoint/log-compaction priority. Those broader questions still belong primarily in `computing-archaeology`.
    ''')
    marker = '## Philosophical interpretation — bounded'
    if marker in case:
        case = case.replace(marker, deepening + '\n' + marker, 1)
    else:
        case = case.rstrip() + deepening + '\n'

case = case.replace(
    '- establish the 2.4 automatic-rewrite genealogy from release/source history;',
    '- the bounded June-2011 -> Redis-2.4 automatic-rewrite introduction/release chain is now closed by the companion genealogy deepening; exact first AOF/BGREWRITEAOF implementation history remains open;'
)
case = case.replace(
    'the earliest AOF/BGREWRITEAOF/automatic-rewrite commits/releases, background-fork design constraints, RDB/AOF evolution, and Redis 7 multipart-AOF transition;',
    'the earliest AOF/BGREWRITEAOF commits/releases, broader automatic-maintenance/database-checkpoint precedents, background-fork design constraints, RDB/AOF evolution, and Redis 7 multipart-AOF transition;'
)
case_path.write_text(case, encoding='utf-8')

# Update grounding record.
ground_path = Path('evidence/138-redis26-aof-rewrite-grounding.md')
ground = ground_path.read_text(encoding='utf-8')
companion = 'Companion genealogy deepening: [`138-redis-2011-2012-auto-aof-rewrite-genealogy-deepening.md`](138-redis-2011-2012-auto-aof-rewrite-genealogy-deepening.md)'
if companion not in ground:
    marker = '[`../cases/138-redis26-aof-rewrite-current-state-reserialization.md`](../cases/138-redis26-aof-rewrite-current-state-reserialization.md)'
    if marker in ground:
        ground = ground.replace(marker, marker + '\n\n' + companion, 1)
    else:
        ground = companion + '\n\n' + ground
old = '2. Exact first automatic-rewrite implementation and its 2.4 release genealogy.'
new = '2. **Closed for the bounded automatic-rewrite chain:** the June-2011 public implementation/hardening -> Redis-2.4 release genealogy is established in [`138-redis-2011-2012-auto-aof-rewrite-genealogy-deepening.md`](138-redis-2011-2012-auto-aof-rewrite-genealogy-deepening.md); exact first AOF/BGREWRITEAOF implementation history remains open.'
if old in ground:
    ground = ground.replace(old, new, 1)
ground_path.write_text(ground, encoding='utf-8')

# Update the single Case 138 ROADMAP item.
road_path = Path('ROADMAP.md')
lines = road_path.read_text(encoding='utf-8').splitlines()
prefix = '- [x] Case 138 Redis 2.6 AOF rewrite / current-state re-serialization slice — '
replacement = (
    '- [x] Case 138 Redis 2.6 AOF rewrite / current-state re-serialization slice — '
    '[`cases/138-redis26-aof-rewrite-current-state-reserialization.md`](cases/138-redis26-aof-rewrite-current-state-reserialization.md) + '
    '[`evidence/138-redis26-aof-rewrite-grounding.md`](evidence/138-redis26-aof-rewrite-grounding.md) + '
    '[`evidence/138-redis-2011-2012-auto-aof-rewrite-genealogy-deepening.md`](evidence/138-redis-2011-2012-auto-aof-rewrite-genealogy-deepening.md): '
    'the released 22-October-2012 `2.6.0` tree separates ordinary replayable AOF history, a fork-time current-dataset rewrite, parent-held concurrent differences, replacement-file authority handoff, size-growth rewrite scheduling, and independent `appendfsync` policy. '
    'The 2011->2.4 genealogy deepening closes the bounded automatic-policy chain: released 2.2.0 already has manual `BGREWRITEAOF` but no later auto-rewrite controls; 10-June-2011 public history adds percentage/min-size/base/current-size scheduling state, immediate fixes correct arithmetic/config/concurrency, 12-June corrects growth-above-base semantics, 9-August fixes size-width overflow, and released 2.4.0 retains the guarded automatic trigger. '
    'This establishes `manual rewrite mechanism != automatic rewrite policy`, `maintenance due != admitted != completed != installed`, and `first implementation != settled semantics` without claiming invention priority or sanitization. Exact first AOF/BGREWRITEAOF genealogy, Redis 7 multipart-AOF evolution, and power-cut/fault validation remain open; broader Redis persistence/database-checkpoint history belongs primarily in `computing-archaeology`.'
)
matched = False
for i, line in enumerate(lines):
    if line.startswith(prefix):
        lines[i] = replacement
        matched = True
        break
if not matched:
    raise RuntimeError('Case 138 ROADMAP item not found')
road_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')

# Append non-duplicated findings.
index_path = Path('CASE_INDEX.md')
index = index_path.read_text(encoding='utf-8')
heading = '### Findings 3732–3747 — Case 138 Redis 2.2→2.4 manual/automatic AOF rewrite genealogy'
if heading not in index:
    block = dedent('''

    ### Findings 3732–3747 — Case 138 Redis 2.2→2.4 manual/automatic AOF rewrite genealogy

    - **3732 — H/P** — The official Redis `2.2.0` tag is dated 22-Feb-2011, providing a released lower bound for the inspected pre-auto-rewrite state rather than an invention-priority date.
    - **3733 — H/P** — Released Redis 2.2.0 `src/aof.c` already contains `bgrewriteaofCommand()` invoking background AOF rewrite, so background rewrite machinery predates the bounded automatic-trigger implementation.
    - **3734 — H/P** — Released Redis 2.2.0 `redis.conf` explicitly points operators to `BGREWRITEAOF` when the append log becomes too large, while the released tree lacks the later `auto-aof-rewrite-percentage` / minimum-size controls.
    - **3735 — H/P** — Official commit `b333e239...` on 10-Jun-2011 is the bounded public automatic-AOF-rewrite implementation event; its message explicitly says `first implementation` and `Still to be tested`.
    - **3736 — H/P** — `b333e239...` adds percentage/minimum-size configuration plus base-size, current-size, and scheduled-rewrite state, making automatic maintenance dependent on retained control/accounting state.
    - **3737 — H/P** — The same initial patch adds a `serverCron` trigger and scheduling around conflicting background save work rather than inventing a separate rewrite engine; it reuses the background rewrite path.
    - **3738 — H/P** — Same-day follow-ups fix division-by-zero, option parsing, observability, and child-concurrency conditions, establishing that the first public patch was not yet settled operating semantics.
    - **3739 — H/P** — Commit `0b17517...` on 12-Jun-2011 changes the trigger arithmetic to growth above the remembered base, explicitly fixing rewrites that started too early.
    - **3740 — H/P** — Commit `11aaf523...` on 9-Aug-2011 widens the trigger's base-size variable from `int` to `long long` to fix auto-rewrite integer overflow, making arithmetic width part of maintenance-policy correctness.
    - **3741 — H/P** — The official Redis `2.4.0` tag is dated 14-Oct-2011, and its released `redis.conf` / `src/redis.c` retain the automatic-rewrite controls and guarded trigger; this is a released adoption floor.
    - **3742 — E** — `manual/background rewrite mechanism exists != automatic rewrite policy exists`; the 2.2→2011 chain separates maintenance capability from the policy that decides when to invoke it.
    - **3743 — E** — Automatic rewrite is history-sensitive control logic: remembered post-rewrite/startup base size plus current AOF size governs future maintenance admission; small control history can govern replacement of a much larger recovery representation.
    - **3744 — E** — `size threshold due != rewrite admitted now != rewrite completed != replacement installed`; child-work guards establish the admission boundary, while Case 138's existing handoff evidence establishes completion/authority boundaries.
    - **3745 — A/E** — Cases 136 and 142 are functional comparison points for separating maintenance reason/policy from admission/execution; they do not establish Redis implementation or genealogy.
    - **3746 — X** — The 10-Jun-2011 public commit is not claimed as invention priority for log compaction/checkpointing, nor does absence of auto controls in released 2.2.0 exclude private branches, prototypes, or unpublished experiments.
    - **3747 — X** — Automatic AOF rewrite and later file replacement do not establish overwrite, Flash erase, crypto erase, or forensic disappearance of retired AOF bytes; media sanitization remains a separate lower-layer question.
    ''')
    index_path.write_text(index.rstrip() + block + '\n', encoding='utf-8')

# Final tree must contain no one-shot integration scaffolding.
for p in [
    '.github/workflows/case138-auto-aof-genealogy-integrate.yml',
    '.github/workflows/case138-auto-aof-recovery.yml',
    '.github/workflows/case138-auto-aof-integrate-v2.yml',
    '.case138_integrate.py',
    'case138-integration-debug.md',
]:
    Path(p).unlink(missing_ok=True)
