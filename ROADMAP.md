# Token Myths — ROADMAP (agent self-start queue)

Legend: `[ ]` todo · `[~]` in progress · `[x]` done. Primary = next thing an agent should pick up.

## Phase 0 — infra & scaffold
- [x] Public repo + SPEC + vault entity + MC registry (2026-11-21)
- [~] PRIMARY: MLX model downloads on M4 Pro (Qwen3-32B-4bit, Qwen3-8B-4bit, Llama-3.1-8B-4bit) → `~/token-myths-logs/dl-*.log`
- [x] Grill pass: GO-WITH-CHANGES, M1–M6 applied to SPEC + vault note (2026-11-21)
- [x] Vendor real persona texts (caveman full+micro, ponytail, chisle, i-have-adhd, concise, combined) with source URL+hash
- [ ] New VPS onboarding (BLOCKED: Sylva must share VW item "apps VPS hetzner" to agents collection; OpenBao sealed blocker open)

## Phase 1 — harness core
- [ ] `bench/schema.py` versioned JSONL run record (blog-complete fields per SPEC)
- [ ] `bench/tokenizers.py` offline exact counts (o200k, cl100k, Qwen, Llama, GLM if available)
- [ ] `bench/runner.py` OpenAI-compatible async runner, checkpoint-resume, retry/backoff
- [ ] Task suite v1: 4 tasks/family × {codegen, debug, extract, explain}, EN+ZH
- [ ] `bench/sandbox.py` docker no-net pytest gate
- [ ] `bench/scorers.py` computable scorers
- [ ] pytest green + baseline-vs-baseline noise-floor cell

## Phase 2 — runs
- [x] Thin slice smoke cells end-to-end on Mac (baseline/caveman-full/combined × en + baseline zh) + scorer validation on real output
- [ ] Offline tokenizer arm (no model calls) → FIRST publishable result
- [ ] Core factorial run (checkpointed; grill-corrected budget: ≤8000 runs ≈5–8 days continuous on MLX, NOT hours-days)
- [ ] Validation arm: sparse key cells on OR :free + Gemini free

## Phase 3 — publication
- [ ] `bench/analyze.py` aggregates + figures + stats (bootstrap CIs, paired)
- [ ] Report (H1–H6 each answered with a figure)
- [ ] `blog/DATA.md` figure index + headline stats (Sylva's blog-post requirement)
- [ ] Combined "prehistoric-ADHD-Chinese" skill packaged from measured winner(s)
- [ ] Build-in-public thread + HN/Reddit posts
