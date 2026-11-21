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
- **H3 tokenizer flip**: Chinese costs more on Western tokenizers, less on Chinese-vocab tokenizers — shown on BOTH the offline token-count axis (exact, tiktoken/HF) and the behavioral axis (local Qwen vs Llama).
- **H4 reasoning interaction**: savings and quality deltas measured at reasoning low AND high (JetBrains gap).
- **H5 combination**: the combined "prehistoric-ADHD-Chinese" persona — additive or interference collapse.
- **H6 negative results**: some viral skills *increase* cost (rtk precedent, +7.6% JetBrains).

## Experimental design

### Axes (full factorial on the core arm)

- **Persona**: `baseline`, `caveman-full`, `caveman-micro` (6-line), `ponytail`, `chisle`,
  `i-have-adhd`, `concise-style` (vendor-style one-liner control), `combined` (caveman×adhd×chinese
  chimera). Persona texts are the REAL published skill files, vendored verbatim under
  `bench/personas/` with source URL + commit hash.
- **Language**: `en`, `zh` (prompts AND expected output language; translations reviewed, same task
  semantics). Offline arm adds exact token counts for every prompt across tokenizers.
- **Reasoning effort**: `low`, `high` (Qwen3 thinking toggle on local; effort param where supported).
- **Model/tokenizer family**: local `qwen3-32b` (Chinese-vocab, thinking toggle) + `llama-3.1-8b`
  (Western BPE) + `qwen3-8b` (matched-size pair control). Validation arm (sparse key cells):
  OpenRouter `:free` + Gemini free tier. NO paid plans for test runs (Sylva constraint).
- **Task family**: `codegen` (unit-tested, docker no-net sandbox), `debug` (known-bug fix, test-gated),
  `extract` (JSON exact-match), `explain` (fact-coverage checklist, rubric-scored deterministically).

### Controls (mandatory)

- Injection cost reported per single-call AND amortized multi-turn (1/10/50 turns, cache on/off model).
- Same base task prompts across all arms; paired seeds; N≥10 per core cell; bootstrap 95% CIs.
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
