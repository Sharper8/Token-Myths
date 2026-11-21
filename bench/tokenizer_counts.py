"""Offline exact token counting across tokenizer families — zero model calls.

This is the H3 arm: the "Chinese is cheaper" myth is decidable EXACTLY at the tokenizer
level, for frontier tokenizers (o200k/cl100k) we could never afford to run behaviorally.
Every prompt/reference-output artifact gets a per-tokenizer count; ratios are derived
per-artifact (never ratio-of-sums) so small artifacts aren't swamped by big ones.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

TOKENIZERS = {
    "o200k_base": ("tiktoken", "o200k_base"),        # GPT-4o / GPT-5.x
    "cl100k_base": ("tiktoken", "cl100k_base"),      # GPT-4 / GPT-3.5
    "p50k_base": ("tiktoken", "p50k_base"),          # GPT-3 era
    "qwen2.5": ("hf", "Qwen/Qwen2.5-7B-Instruct"),   # Chinese-vocab BPE
    "llama-3.1": ("hf", "NousResearch/Meta-Llama-3.1-8B"),  # Western BPE (ungated mirror)
    "glm-4": ("hf", "THUDM/GLM-4-9B-0414"),          # the family where ZH flips cheaper
}

_cache: dict = {}

def _get(name: str):
    if name in _cache:
        return _cache[name]
    kind, ident = TOKENIZERS[name]
    if kind == "tiktoken":
        import tiktoken
        tok = tiktoken.get_encoding(ident)
        fn = lambda s: len(tok.encode(s, disallowed_special=()))
    else:
        from transformers import AutoTokenizer
        tok = AutoTokenizer.from_pretrained(ident)
        fn = lambda s: len(tok.encode(s, add_special_tokens=False))
    _cache[name] = fn
    return fn

def count_all(text: str) -> dict[str, int | None]:
    """Token counts for one text across every tokenizer. None = tokenizer unavailable."""
    out = {}
    for name in TOKENIZERS:
        try:
            out[name] = _get(name)(text)
        except Exception as e:
            print(f"WARN tokenizer {name} failed: {type(e).__name__}: {e}", file=sys.stderr)
            out[name] = None
    return out

def run_offline_arm(corpus_path: Path, out_path: Path) -> None:
    """Corpus: JSONL of {artifact_id, lang, family, text}. Appends full per-artifact records."""
    with open(corpus_path) as f, open(out_path, "a") as out:
        for line in f:
            a = json.loads(line)
            rec = dict(a)
            rec["chars"] = len(a["text"])
            rec["utf8_bytes"] = len(a["text"].encode())
            rec["tokens"] = count_all(a["text"])
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    run_offline_arm(Path(sys.argv[1]), Path(sys.argv[2]))
