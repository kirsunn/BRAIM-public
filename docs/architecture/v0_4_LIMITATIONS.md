# BRAVO v0.4 — Limitations (Solo Development)

> Added 2026-10-18. Honest document layer between BRAVO v0.4 (8-layer target architecture) and BRAIM v0.4 (1-developer realisation).

## Why 8 layers cannot be built by a single developer

A single developer at ~12 h/week cannot deliver and maintain an 8-repository microservice architecture.

| Resource | BRAVO v0.4 (8 layers) | BRAIM v0.4 (1 dev) |
|---|---|---|
| Repositories | 8 | 1 |
| CI/CD | 8 | 1 |
| Security audit | 8 | self-audit (NOT-DOING §18) |
| Release trains | 8 | 1 (main + feat/*) |
| UI surfaces | 8 | 0 (text/file) |

## Mapping to our realisation

See `docs/architecture/v0_4_MAPPING.md` for the explicit mapping between BRAVO v0.4 components and our 5-6 directories.

## Why this is honest, not a weakness

- We are not building a generic platform.
- We are building a **specific product** (BRAIM) for **specific user scenarios** (MKD norms verification, AGT, forensic audit).
- The decomposition to 5-6 dirs is the **correct** architecture for 1 dev + 12 h/week.
- BRAVO remains the **target architecture** for future scale-out (when team grows).

## What we explicitly do not implement (NOT-DOING)

- API Gateway (NOT-DOING §11 — no microservices without need)
- Security Module as a separate layer (NOT-DOING §18 — solo cannot deliver production security)
- UI/UX (NOT-DOING §11 — text/file based, not GUI)
- 3 separate Data Storages (Metadata/Geometry/History) — collapsed into audit/
- Distributed RAG (RAG in BRAV container) — collapsed to our 5 dirs

## Honest trade-off table

| Aspect | BRAVO v0.4 (target) | BRAIM v0.4 (1 dev) | Trade-off rationale |
|---|---|---|---|
| Microservices | Yes (8 repos) | No (1 repo) | We don't need microservices; we need a working extraction pipeline |
| Security module | Yes (separate) | No (lives in 5 dirs) | We cannot deliver production security as a solo dev; that's an honest gap |
| UI/UX | Yes (8 surfaces) | No (text/file) | Our user scenarios (norms check, AGT) don't need a GUI for MVP |
| 3 Data Storages | Yes (Metadata/Geometry/History) | No (1 audit log) | We collapse them into one place for simplicity |
| Distributed RAG | Yes (in BRAV) | No (local norm_graph) | Local norm_graph serves the same purpose for our scope |

## When to revisit

If the team grows beyond 1 dev, OR if user scenarios require GUI / API / multi-tenant, we revisit this and decompose per the BRAVO v0.4 spec.
