"""Persona assembly: vendored real skill texts + authored micro/concise/combined controls.

The system prompt = persona body. `combined` is the chimera: caveman prose rules × ADHD
action-first shaping, emitted in Chinese when language=zh (H5 arm).
"""
from __future__ import annotations
from pathlib import Path

PERSONA_DIR = Path(__file__).parent / "personas"

CAVE_MAN_MICRO = (
    "Be extremely concise. Drop articles, filler, pleasantries and hedging. "
    "Keep only technical substance. Code blocks, error messages and technical terms stay exact. "
    "Answer directly; no preamble, no summary restatement."
)

CONCISE_STYLE = "Be concise. If the task asks for structured data, return only that data."

COMBINED_EN = (
    "Talk like caveman with ADHD. Few word do trick. Drop articles, filler, pleasantries, hedging. "
    "Action first: most important thing in first line, then steps, max five visible items. "
    "No preamble, no restating question, no summary. "
    "Code blocks, error messages, technical terms stay exact and complete. Caveman not stupid."
)

COMBINED_ZH = (
    "像原始人一样说话，还要有 ADHD 风格：最省字。去掉所有客套、废话、铺垫。"
    "行动优先：第一行就是最重要的答案，然后是最多五条要点。"
    "不复述问题，不总结。代码块、报错信息、技术术语保持完整精确。原始人不是笨蛋。"
)

BASELINE_ZH_SUFFIX = "用中文回答。"  # baseline zh arm: only output-language instruction


def _filler_control(language: str) -> str:
    """Length-matched irrelevant-style control (grill M3): same o200k length as caveman-full,
    zero actionable content — separates 'persona content' from 'system prompt exists/is long'."""
    import tiktoken
    target = len(tiktoken.get_encoding("o200k_base").encode(
        (PERSONA_DIR / "caveman-full.md").read_text(), disallowed_special=()))
    sentence = ("This note describes the preferred layout of a personal reading journal, "
                "including margin widths, paper texture preferences, and shelving order. ")
    text = sentence
    enc = tiktoken.get_encoding("o200k_base")
    while len(enc.encode(text, disallowed_special=())) < target:
        text += sentence
    if language == "zh":
        text += "\n\n" + BASELINE_ZH_SUFFIX
    return text


def get_persona(persona_id: str, language: str) -> tuple[str, dict]:
    """Returns (system_prompt, source_meta). Empty system prompt = true baseline."""
    if persona_id == "baseline":
        return (BASELINE_ZH_SUFFIX if language == "zh" else ""), {"kind": "control"}
    if persona_id == "filler-control":
        return _filler_control(language), {"kind": "length-matched-control", "matched_to": "caveman-full"}
    if persona_id == "caveman-micro":
        return CAVE_MAN_MICRO, {"kind": "authored", "after": "jakguzik 6-line benchmark"}
    if persona_id == "concise-style":
        return CONCISE_STYLE, {"kind": "control", "after": "vendor concise output style"}
    if persona_id == "combined":
        return (COMBINED_ZH if language == "zh" else COMBINED_EN), {"kind": "authored-chimera"}
    # vendored real skills, verbatim
    body = (PERSONA_DIR / f"{persona_id}.md").read_text()
    if language == "zh":
        body += "\n\n" + BASELINE_ZH_SUFFIX
    import json
    sources = json.loads((PERSONA_DIR / "sources.json").read_text())
    return body, {"kind": "vendored-verbatim", **sources.get(persona_id, {})}
