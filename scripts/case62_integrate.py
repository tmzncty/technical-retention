from pathlib import Path
import re


def replace_once(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"{label}: expected one exact anchor, found {n}")
    return text.replace(old, new, 1)


# README navigation and evidence ledger.
p = Path("README.md")
s = p.read_text(encoding="utf-8")
case61 = "- [`cases/61-apache-hdfs-observer-stateid-read-freshness.md`](cases/61-apache-hdfs-observer-stateid-read-freshness.md) — grounded HDFS Observer read-freshness bridge: RPC-carried client state IDs record a monotonic lower bound on namespace progress; coordinated Observer reads wait/retry until the Observer catches up, while `msync()` imports an Active frontier across client/out-of-band boundaries and writes remain Active-only."
case62 = "- [`cases/62-ibm-system360-model40-tros-replaceable-control-store.md`](cases/62-ibm-system360-model40-tros-replaceable-control-store.md) — grounded IBM System/360 Model 40 TROS bridge: fixed printed control-tape routing links or bypasses transformer positions to encode microinstructions; runtime access is read-only, while IBM explicitly moves deliberate revision into physical control-tape replacement, keeping magnetic transduction, payload geometry, update authority, and invention priority separate."
if case62 not in s:
    s = replace_once(s, case61, case61 + "\n" + case62, "README case navigation")
ev62 = "- [`evidence/62-ibm-bell-1950-1970-tros-grounding.md`](evidence/62-ibm-bell-1950-1970-tros-grounding.md) — Case-62 grounding record: IBM 1964/1970 engineering evidence separates fixed control-tape conductor routing, transformer sensing, runtime read-only authority, and physical tape replacement, while Dimond/Bell 1950–1952 inductive-translation evidence prevents a false System/360 invention claim."
if ev62 not in s:
    ev_pat = re.compile(r'^- \[`evidence/61-hadoop-2017-2020-observer-stateid-grounding\.md`\].*$', re.M)
    m = ev_pat.search(s)
    if not m:
        raise SystemExit("README evidence/61 anchor missing")
    s = s[:m.end()] + "\n" + ev62 + s[m.end():]
p.write_text(s.rstrip() + "\n", encoding="utf-8")


# ROADMAP: deepen the fixed-topology bridge rather than create a generic ROM history.
p = Path("ROADMAP.md")
s = p.read_text(encoding="utf-8")
newroad = "- [x] magnetic-core retained state → wired-core fixed topology / replaceable transformer control media — **advanced by grounded Cases 02, 60, and 62**. [`cases/02-magnetic-core-destructive-read.md`](cases/02-magnetic-core-destructive-read.md) keeps classic remanent magnetic payload plus destructive-read restore distinct. [`cases/60-apollo-core-rope-wired-topology.md`](cases/60-apollo-core-rope-wired-topology.md), grounded by [`evidence/60-apollo-core-rope-1964-1972-grounding.md`](evidence/60-apollo-core-rope-1964-1972-grounding.md), then shows a fixed program encoded in sense-wire/core topology while ferrite switching serves read transduction. [`cases/62-ibm-system360-model40-tros-replaceable-control-store.md`](cases/62-ibm-system360-model40-tros-replaceable-control-store.md), grounded by [`evidence/62-ibm-bell-1950-1970-tros-grounding.md`](evidence/62-ibm-bell-1950-1970-tros-grounding.md), adds a distinct System/360 Model 40 regime in which printed TROS control tapes encode microinstructions through transformer link/bypass routing, ordinary execution can only read them, and deliberate revision occurs by physically changing the control tapes. Bell/Dimond inductive-translation evidence predating System/360 blocks an IBM-first claim. The bounded bridge is closed; a full Bell Model VI/No. 5 Crossbar → IBM Hursley SCAMP → System/360 genealogy, CCROS/BCROS comparison, manufacturing economics, and semiconductor-ROM descent remain separate future work;"
if newroad not in s:
    pat = re.compile(r'^- \[x\] magnetic-core retained state → wired-core fixed topology — .*;$', re.M)
    ms = list(pat.finditer(s))
    if len(ms) != 1:
        raise SystemExit(f"ROADMAP magnetic bridge anchor count={len(ms)}")
    s = s[:ms[0].start()] + newroad + s[ms[0].end():]
p.write_text(s.rstrip() + "\n", encoding="utf-8")


# CASE_INDEX case ledger, comparison matrix, count, and findings.
p = Path("CASE_INDEX.md")
s = p.read_text(encoding="utf-8")
row62 = "| [IBM System/360 Model 40 TROS: Runtime Read-Only State in Replaceable Transformer Control Tapes](cases/62-ibm-system360-model40-tros-replaceable-control-store.md) | **grounded** | fixed printed control-tape drive-line routing + transformer link/bypass sensing + physical carrier replacement | separate magnetic transduction from magnetic-state payload; runtime read-only from lifecycle immutability; fine addressability from runtime update authority; and product introduction from invention priority | [1950–1970 Bell/IBM TROS grounding](evidence/62-ibm-bell-1950-1970-tros-grounding.md); full Bell→Hursley genealogy, CCROS/BCROS comparison, field-failure statistics, and exact service/manufacturing archaeology remain separate work |"
if row62 not in s:
    split = s.index("## Comparison matrix — provisional")
    head, tail = s[:split], s[split:]
    case_pat = re.compile(r'^\| \[Apache HDFS Observer NameNode: State-ID Read Freshness Beyond Writer Authority\]\(cases/61-apache-hdfs-observer-stateid-read-freshness\.md\).*$', re.M)
    m = case_pat.search(head)
    if not m:
        raise SystemExit("CASE_INDEX Case61 row missing")
    head = head[:m.end()] + "\n" + row62 + head[m.end():]
    s = head + tail

matrix62 = "| IBM System/360 Model 40 TROS / 1964–1970 bounded regime | printed control-tape drive-line routing through/bypass transformer positions + sense windings; fixed microinstruction/control-word state | no periodic payload refresh established; operating read current plus carrier/configuration integrity; deliberate revision by physical control-tape replacement | addressed drive-line pulse is inductively sensed; logically nondestructive with respect to the encoded tape route | ROAR/ROSCAR selects one fixed control word; fine addressability does not create runtime write authority | high within one installed tape set; current microprogram can change by physical carrier replacement while superseded tapes survive | no operation history by default; a removed carrier can preserve an obsolete complete microinstruction pattern |"
if matrix62 not in s:
    matrix_pat = re.compile(r'^\| Apollo AGC core rope / wired-in fixed memory \|.*$', re.M)
    m = matrix_pat.search(s)
    if not m:
        raise SystemExit("CASE_INDEX Apollo matrix row missing")
    s = s[:m.end()] + "\n" + matrix62 + s[m.end():]

oldcount = "After sixty-two bounded cases, **all sixty-two cases are now `grounded`.**"
newcount = "After sixty-three bounded cases, **all sixty-three cases are now `grounded`.**"
if newcount not in s:
    s = replace_once(s, oldcount, newcount, "CASE_INDEX count")

findings = [
    "## Case 62 — IBM Model 40 TROS replaceable-control-store findings",
    "",
    "669. **runtime read-only ≠ lifecycle immutable** — Model 40 TROS exposes no ordinary runtime write path, yet IBM explicitly changes retained information by physically changing control tapes;",
    "670. **magnetic transduction ≠ magnetic-state payload retention** — TROS uses transformer induction to recover a bit whose persistent distinction is carried by conductor link/bypass routing;",
    "671. **fine runtime addressability ≠ fine runtime update authority** — ROAR/ROSCAR can select individual fixed control words while deliberate modification remains a physical service operation;",
    "672. **state-bearing control-tape route ≠ sensing-transformer state** — the printed conductor geometry carries the fixed distinction while transformer/sense circuitry makes it recoverable;",
    "673. **read-only ≠ physically inactive** — reading requires drive current and induction even though the bit-defining route is not rewritten;",
    "674. **physical control-tape replacement ≠ in-place electronic write** — both can change which logical program is current, but they impose different mechanisms, granularity, and authority;",
    "675. **superseded carrier survival ≠ current configured program** — an old TROS tape can remain physically encoded after a replacement becomes authoritative;",
    "676. **fixed microprogram ≠ hardwired combinational logic** — Model 40 control is represented as addressable microinstructions even though the bounded store is runtime read-only;",
    "677. **retained executable diagnostic code ≠ automatic proof of medium integrity** — using fixed TROS routines to test CPU/storage is distinct from independently validating every TROS carrier/sense path;",
    "678. **power-independent payload geometry ≠ power-independent service availability** — conductor routing can survive without operating current while address, drive, sense, latch, and control electronics still require power to execute it;",
    "679. **shared topology-coupled readout ≠ same carrier/revision regime** — Apollo rope and IBM TROS both couple conductor geometry to magnetic sensing but organize bits, carriers, and program replacement differently;",
    "680. **System/360 product introduction ≠ transformer-ROM invention priority** — Bell/Dimond inductive-translator evidence from 1950–1952 predates IBM's 1964 System/360 TROS;",
    "681. **control-store role identity ≠ physical ROS mechanism identity** — TROS, CCROS/BCROS, and later semiconductor ROM may all serve microprogram control roles without sharing a retention substrate;",
    "682. **quiescent retention ≠ zero lifecycle retention labor** — a fixed non-refreshed control-tape pattern still depends on manufacture, configuration, installation, diagnosis, and service replacement;",
    "683. **configuration forgetting ≠ physical sanitization** — removing or replacing a control tape can make its microprogram non-current without destroying the old encoded carrier;",
    "684. **IBM Model 40 TROS ≠ Apollo core rope ≠ classic writable core RAM** — transformer/ferrite material and broad read-only-memory analogy do not erase the different state-bearing and update mechanisms.",
]
if findings[0] not in s:
    s = s.rstrip() + "\n\n" + "\n".join(findings) + "\n"
p.write_text(s.rstrip() + "\n", encoding="utf-8")


# Validation.
assert Path("cases/62-ibm-system360-model40-tros-replaceable-control-store.md").is_file()
assert Path("evidence/62-ibm-bell-1950-1970-tros-grounding.md").is_file()
assert len(list(Path("cases").glob("[0-9][0-9]-*.md"))) == 63
readme = Path("README.md").read_text(encoding="utf-8")
roadmap = Path("ROADMAP.md").read_text(encoding="utf-8")
idx = Path("CASE_INDEX.md").read_text(encoding="utf-8")
assert readme.count("cases/62-ibm-system360-model40-tros-replaceable-control-store.md") == 2
assert readme.count("evidence/62-ibm-bell-1950-1970-tros-grounding.md") == 2
assert roadmap.count("cases/62-ibm-system360-model40-tros-replaceable-control-store.md") >= 2
assert idx.count("cases/62-ibm-system360-model40-tros-replaceable-control-store.md") >= 1
assert newcount in idx
nums = [int(x) for x in re.findall(r'(?m)^(\d+)\. \*\*', idx)]
assert max(nums) == 684
