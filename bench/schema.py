"""Versioned run-record schema — every field a blog post could need, no re-running required."""
from __future__ import annotations
import hashlib, subprocess
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = 1

@dataclass
class RunRecord:
    run_id: str
    ts_utc: str
    # cell coordinates
    persona: str
    language: str
    reasoning: str
    model: str
    family: str
    task_id: str
    rep: int
    seed: int
    # provenance
    endpoint: str
    harness_git_sha: str
    persona_source: dict = field(default_factory=dict)
    # full artifacts (the blog requirement: nothing is re-derivable-only)
    system_prompt: str = ""
    user_prompt: str = ""
    output_text: str = ""
    # measurements
    usage: dict = field(default_factory=dict)          # API-reported {prompt, completion, reasoning}
    tokens_offline: dict = field(default_factory=dict) # per-tokenizer exact counts of in+out
    injection_tokens: dict = field(default_factory=dict)
    wall_seconds: float = 0.0
    quality: dict = field(default_factory=dict)        # scorer-specific sub-scores
    sandbox: dict = field(default_factory=dict)
    error: str | None = None

    def to_json(self) -> dict:
        return asdict(self)

def git_sha(repo: Path) -> str:
    try:
        return subprocess.run(["git","-C",str(repo),"rev-parse","HEAD"],
                              capture_output=True,text=True).stdout.strip()
    except Exception:
        return "unknown"

def new_run_id(parts: dict) -> str:
    raw = "|".join(f"{k}={v}" for k,v in sorted(parts.items()))
    return hashlib.sha256(raw.encode()).hexdigest()[:16]

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()
