# Token Myths — specification

_Stub generated 2026-11-21 by `pai new-project`. Written before the code, per the PAI spec-first
policy; the vault note `Project - Token Myths` (4b6a926f-2670-48a0-b971-6cf29714b7b4) is the entity of record._

## Problem

<!-- What is broken/missing today, in one paragraph. Concrete, observed, not aspirational. -->

## Goals

1.
2.

## Non-goals (for v0)

-

## First thin slice

<!-- The smallest thing that is end-to-end useful and verifiable. -->

-

## Interfaces

<!-- CLI/HTTP/file contracts. What another component can rely on. -->

## Verification

<!-- How we know it works: tests, a command to run, an observable signal. -->

- `python -m pytest` green (CI runs it on every push)
- `GLITCHTIP_DSN` set (see `.env.example`) — the Sentry SDK reports errors to GlitchTip
- `VITE_PLAUSIBLE_DOMAIN` set (see `.env.example`) — the Plausible tracking script loads on deploy

## Open questions

-
