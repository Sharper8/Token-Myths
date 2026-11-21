"""OpenAI-compatible benchmark runner. Full JSONL logging per SPEC 'Blog-data requirement'."""
from __future__ import annotations
import argparse, json, time, urllib.request
from pathlib import Path

from . import schema, persona_defs
from .tokenizer_counts import count_all
from .tasks import load_task, score

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / "results" / "runs.jsonl"


def call_endpoint(endpoint: str, model: str, system: str, user: str,
                  reasoning: str, max_tokens: int = 4096) -> dict:
    body = {
        "model": model, "max_tokens": max_tokens, "temperature": 0.0,
        "messages": ([{"role": "system", "content": system}] if system else [])
        + [{"role": "user", "content": user}],
    }
    if reasoning == "low":
        body["chat_template_kwargs"] = {"enable_thinking": False}
    elif reasoning == "high":
        body["chat_template_kwargs"] = {"enable_thinking": True}
    req = urllib.request.Request(
        endpoint.rstrip("/") + "/v1/chat/completions",
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=1800) as resp:
        return json.load(resp)


def run_cell(persona: str, language: str, reasoning: str, model: str, endpoint: str,
             model_id: str, family: str, task_id: str, rep: int) -> schema.RunRecord:
    task = load_task(family, task_id, language)
    system, src = persona_defs.get_persona(persona, language)
    # grill M5/F7: unique run salt defeats prefix-cache contamination without changing semantics
    salt = f"<!-- run-salt: {schema.utc_now()} {rep} -->"
    system = (system + "\n" + salt) if system else salt
    rec = schema.RunRecord(
        run_id=schema.new_run_id(dict(persona=persona, lang=language, reasoning=reasoning,
                                      model=model, task=task_id, rep=rep, sha=schema.git_sha(REPO))),
        ts_utc=schema.utc_now(), persona=persona, language=language, reasoning=reasoning,
        model=model, family=family, task_id=task_id, rep=rep, seed=rep,
        endpoint=endpoint, harness_git_sha=schema.git_sha(REPO), persona_source=src,
        system_prompt=system, user_prompt=task["prompt"])
    t0 = time.time()
    try:
        resp = call_endpoint(endpoint, model_id, system, task["prompt"], reasoning)
        rec.output_text = resp["choices"][0]["message"]["content"] or ""
        u = resp.get("usage", {})
        rec.usage = {"prompt": u.get("prompt_tokens"), "completion": u.get("completion_tokens"),
                     "reasoning": (u.get("completion_tokens_details") or {}).get("reasoning_tokens")}
    except Exception as e:
        rec.error = f"{type(e).__name__}: {e}"
    rec.wall_seconds = round(time.time() - t0, 3)
    if not rec.error:
        rec.quality = score(family, task, rec.output_text)
        rec.tokens_offline = {"input": count_all(system + "\n" + task["prompt"]),
                              "output": count_all(rec.output_text)}
        rec.injection_tokens = count_all(system) if system else {k: 0 for k in rec.tokens_offline["input"]}
    RESULTS.parent.mkdir(exist_ok=True)
    with open(RESULTS, "a") as f:
        f.write(json.dumps(rec.to_json(), ensure_ascii=False) + "\n")
    return rec


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--persona", default="baseline")
    p.add_argument("--language", default="en")
    p.add_argument("--reasoning", default="low")
    p.add_argument("--model", default="qwen3-8b")
    p.add_argument("--model-id", default="mlx-community/Qwen3-8B-4bit")
    p.add_argument("--endpoint", default="http://localhost:8321")
    p.add_argument("--family", default="explain")
    p.add_argument("--task", default="race-condition")
    p.add_argument("--n", type=int, default=1)
    a = p.parse_args()
    for rep in range(a.n):
        rec = run_cell(a.persona, a.language, a.reasoning, a.model, a.endpoint,
                       a.model_id, a.family, a.task, rep)
        print(json.dumps({"run_id": rec.run_id, "error": rec.error,
                          "wall_s": rec.wall_seconds, "usage": rec.usage,
                          "quality": rec.quality, "out_chars": len(rec.output_text)}))


if __name__ == "__main__":
    main()
