"""Task registry v1 — explain family first (thin slice). Computable scorers only.

Each task: {task_id, family, prompts: {en, zh}, checklist: {en: [concept markers], zh: [...]}}.
Explain scorer = fraction of required concepts present (marker sets, case-insensitive).
Markers are alternative phrasings per concept; a concept counts if ANY marker appears.
"""
from __future__ import annotations

TASKS = {
    ("explain", "race-condition"): {
        "prompts": {
            "en": "Explain why a race condition can corrupt a shared counter even when each individual increment looks atomic in the source code. Include the role of the CPU cache and instruction interleaving.",
            "zh": "解释为什么即使每次自增在源码中看似原子操作，竞态条件仍会破坏共享计数器。需涵盖 CPU 缓存和指令交错的作用。",
        },
        "concepts": {
            # concept = list of FACETS (all required); facet = list of ALTERNATIVE markers (any hits)
            "load_add_store": {
                "en": [["load", "read", "fetch"], ["add", "increment"], ["store", "write"]],
                "zh": [["加载", "读取"], ["加法", "自增"], ["存储", "写回"]],
            },
            "interleaving": {
                "en": [["interleav", "two threads", "both read", "concurrent", "order of execution"]],
                "zh": [["交错", "两个线程", "同时读取", "都读到", "并发"]],
            },
            "lost_update": {
                "en": [["lost", "losing", "incorrect", "overwrite", "same value"]],
                "zh": [["丢失", "覆盖", "相同的值", "不正确"]],
            },
            "cache_staleness": {
                "en": [["stale", "private copy", "own cache", "cache coheren", "inconsistent views"]],
                "zh": [["过期", "私有副本", "缓存一致", "自己的缓存"]],
            },
            "fix": {
                "en": [["lock", "atomic", "mutex", "synchron"]],
                "zh": [["锁", "原子指令", "互斥", "同步"]],
            },
        },
    },
}


def load_task(family: str, task_id: str, language: str) -> dict:
    t = TASKS[(family, task_id)]
    return {"task_id": task_id, "family": family, "prompt": t["prompts"][language],
            "concepts": {k: v[language] for k, v in t["concepts"].items()}}


def score(family: str, task: dict, output: str) -> dict:
    if family == "explain":
        low = output.lower()
        hits = {}
        for concept, marker_sets in task["concepts"].items():
            # a concept counts when every marker GROUP has ≥1 hit (groups = facets of the concept)
            hits[concept] = all(any(m.lower() in low for m in group) for group in marker_sets)
        passed = sum(hits.values()) == len(hits)
        return {"concept_coverage": round(sum(hits.values()) / len(hits), 3),
                "concepts": hits, "pass": passed}
    raise ValueError(f"no scorer for family {family}")
