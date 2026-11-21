# Token Myths

Full-factorial benchmark of viral token-compression tricks (caveman/ADHD/Chinese/Ponytail/Chisle) — quality-per-dollar, build-in-public

_Scaffolded 2026-11-21 by `pai new-project`. Spec-first: fill in [SPEC.md](SPEC.md) before writing code._

## Status

Draft — scaffolded, nothing built yet.

## Observability (wired at birth)

- **Mission Control**: registered as `Token Myths` in the project registry, so repo activity, uptime
  probes and KPIs are collected without further setup.
- **PAI vault**: `Project - Token Myths` is the entity note — problem, goals, decisions live there,
  not in this README.
- **GlitchTip error tracking**: wired at birth — set `GLITCHTIP_DSN` in `.env`
  (copy from `.env.example`). Each project needs its own GlitchTip project + DSN:
  create it in the GlitchTip UI (or reuse an existing DSN from the Bitwarden
  `glitchtip` item) and the Sentry SDK ships errors on the first build.
- **Plausible analytics**: wired at birth — set `VITE_PLAUSIBLE_DOMAIN` in `.env`
  (copy from `.env.example`) to `analytics.devprocore.com`. On deploy, add
  `VITE_PLAUSIBLE_DOMAIN` to the CI environment (no secret needed — the domain is
  public) and the tracking script loads. No-op in dev without it.

- **Token metering**: delegated builds run through the metered wrapper so the cost lands in the
  ledger tagged `Token Myths`:

```
/root/.hermes/scripts/claude-metered.sh "Token Myths" 30 "/var/tmp/Token-Myths" "Read SPEC.md and implement the first thin slice of Token Myths."
```

## Tests

```
python -m pytest
```
