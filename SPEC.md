# Token Myths — specification

_Vault entity of record: `Project - Token Myths` (4b6a926f-2670-48a0-b971-6cf29714b7b4).
Public build-in-public benchmark. Owner: Sylva (Sharper8). Runtime: Hermes/kimi-k3 autonomous._

## Problem

Viral "speak cheaper" tricks (caveman, i-have-adhd, ponytail, chisle, Chinese prompting) carry
contradictory, non-comparable numbers: caveman claims 65–75% savings; JetBrains measured 8.5%;
Better Stack showed single-call net loss once injection cost is counted. Nobody has run the
**full factorial** (persona × language × reasoning effort × tokenizer family) with
**quality-per-dollar** as the metric. The Chinese-efficiency claim is already busted on Western
tokenizers (arXiv 2604.14210) but flips on Chinese-vocab tokenizers (GLM) — untested under one
harness.

## Research questions (each must map to ≥1 figure in the report)

- **H1 persona ceiling**: prose-persona tricks cluster at ≤~10% real savings (HN mmastrac hypothesis).
- **H2 mechanism split**: behavior-changing skills (ponytail: less code) > prose-compression skills (caveman-class).
- **H3 tokenizer flip (offline-only claim)**: Chinese costs more on Western tokenizers, less on
  Chinese-vocab tokenizers — claimed ONLY on the offline exact-count axis (Qwen-vs-Llama behavioral
  comparisons confound tokenizer with vendor/size/training: grill F3). Behavioral language arm is
  exploratory: savings reported conditioned on quality-pass, phrased "consistent with", never causal.
- **H4 reasoning interaction**: savings and quality deltas at reasoning low AND high, Qwen3 only
  (Llama has no thinking toggle: grill F2). Not comparable across endpoints.
- **H5 combination**: downgraded (grill): "does the chimera beat its best single component?"
  Additivity/interference is NOT claimable without a 2³ sub-factorial; optional cheap arm:
  8-cell (caveman × adhd × chinese presence/absence) × en × low × qwen3-8b × one family.
- **H6 negative results**: some viral skills *increase* cost (rtk precedent, +7.6% JetBrains).

## Experimental design

### Axes (fractional factorial — grill M2)

**Experimental unit = (persona × lang × reasoning × model × task_id), N=10 per task** (grill M1:
N per family would be pseudoreplication; CIs cluster-bootstrap at task level, analysis script
committed+frozen before the full run).

- **Persona**: `baseline`, `filler-control` (length-matched to caveman-full, irrelevant style
  content — grill M3, non-negotiable before packaging any combined skill), `caveman-full`,
  `caveman-micro` (6-line), `ponytail`, `chisle`, `i-have-adhd`, `concise-style`, `combined`.
- **Language**: `en`, `zh`. Difficulty-equivalence pretest first (grill M5): baseline solve-rate
  EN vs ZH within tolerance before task versions enter the matrix; table published in appendix.
- **Reasoning effort**: `low`, `high` — **Qwen3 models only** (thinking toggle). Absent for Llama.
- **Models**: `qwen3-8b` = full-factorial workhorse. `qwen3-32b` = sparse key-cell grid only
  (baseline, caveman-full, caveman-micro, combined × en/zh × low × all families). `llama-3.1-8b` =
  H3-relevant cells + offline arm only. Validation arm: sparse snapshot cells on OR `:free` +
  Gemini free, exact model revision + date per run, labeled "snapshot validation" (grill F8).
  NO paid plans for test runs (Sylva constraint).
- **Task family**: `codegen` (unit-tested, docker no-net sandbox), `debug` (known-bug fix, test-gated),
  `extract` (JSON exact-match), `explain` (fact-coverage checklist, rubric-scored deterministically).

### Controls (mandatory)

- **Stateless fresh context per run; unique run salt; prefix caching disabled or salted** (grill M5/F7).
- Injection cost reported per single-call AND amortized multi-turn (1/10/50 turns, cache on/off model).
- Same base task prompts across all arms; paired seeds; N=10 per task; task-level cluster bootstrap.
- **Primary metric (pre-registered, grill M4/F5): quality gate FIRST — modeled cost and token deltas
  computed on quality-passing runs only; cost = modeled at published API prices, never "measured".**
  Raw savings = secondary. turns-to-correct = secondary (repair protocol interacts with persona, F7).
- Offline tokenizer arm needs NO model calls: exact token counts of all prompts+reference outputs
  across `o200k`, `cl100k`, Qwen2/3, GLM, Llama tokenizers → H3 provable for frontier models for free.

### Metrics per run

input/output/reasoning tokens (API-reported + offline recomputed), wall time, quality score
(computable: tests-pass / JSON-valid exact-match / checklist coverage), turns-to-correct
(capped follow-up protocol), LOC-written (codegen), injected-persona token overhead, cost model
($ at published per-model prices, 0 spend but priced for the blog).

## Blog-data requirement (Sylva, 2026-11-21 — binding)

Every run appends ONE JSONL record containing EVERYTHING a blog post needs without re-running:
run_id, utc timestamp, full cell coordinates, model+endpoint+git-sha of harness, persona id+version+
source-url, full prompt and full output text, all token counts (per-tokenizer dict), timings,
quality sub-scores, sandbox verdict, error state. `results/runs.jsonl` is authoritative;
`results/aggregate.csv`, `figures/`, `blog/DATA.md` (figure index + headline stats) are derived and
regenerable via `python -m bench.analyze`. No figure may exist without the raw rows behind it.

## Architecture

- `bench/` Python package: `config.yaml` (matrix), `personas/`, `tasks/`, `runner.py` (async,
  checkpoint-resume, per-cell state), `tokenizers.py` (offline counts), `sandbox.py` (docker
  `--network none --memory 512m`, pytest inside), `scorers.py`, `analyze.py` (CSV+figures+stats).
- Inference: OpenAI-compatible endpoints. Local = `mlx_lm.server` on the M4 Pro (mesh/SSH tunnel);
  validation = OR `:free` / Gemini free. Rate-limit-aware, retry-with-backoff, cell checkpointing.
- Results committed to the repo (JSONL gz + aggregates + figures) — the repo IS the blog dataset.

## Non-goals (for v0)

- Paid API runs; Kimi/Claude plan tokens for test runs (allowed: building this harness).
- Agent-harness-level benchmarking (Claude Code etc. contaminate the persona variable — raw API only).
- Human preference eval; LLM-judge scoring (computable-only doctrine).
- Production deployment / web app (report + skill are the deliverables).

## First thin slice

`python -m bench.runner --cell baseline/en/low/qwen3-8b/explain --n 2` end-to-end on the Mac:
runs, scores, logs full JSONL, `python -m bench.analyze` emits one figure. Then the offline
tokenizer arm (zero model calls) as the first publishable result.

## Interfaces

- CLI: `python -m bench.runner --matrix core|validation|offline --n N [--only cell-filter]`
- `results/runs.jsonl` schema = `bench/schema.py` (versioned).
- Persona/task registration = drop a file + config entry; no code edits.

## Verification

- `python -m pytest` green (scorers, tokenizer counts vs known strings, sandbox, JSONL schema).
- Smoke cell end-to-end with payload readback of runs.jsonl (not exit codes).
- Statistical sanity: baseline-vs-baseline arm shows ~0 delta (harness noise floor).

## Open questions

- Chisle/ponytail canonical source repos to vendor (verify authenticity before use).
- ZH translations: agent-produced + back-translation check (deterministic diff of task semantics).
- New VPS (ubuntu-4gb-hel1-5) becomes the orchestration host once the SSH key share lands;
  until then harness dev in /var/tmp, inference on the Mac, sandbox on homelab docker.
