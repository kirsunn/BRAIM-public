# IFC5 / IFCX Primary Sources

Status: Research registry  
Date: 2026-10-18  
Project: BRAVIM / Building Avatar (BAV)  
Purpose: fixed list of primary sources for IFC 5 / IFCX research

## 1. Research principle

BRAVIM does not fork IFC 5 and does not claim ownership of its materials.

We study official buildingSMART sources, extract ideas relevant to Building Avatar (BAV), and always preserve a link to the primary source.

```text
Study → extract → map to BAV → reference primary source
```

IFC 5 / IFCX materials are experimental and may change. They must not be treated as a stable production standard.

## 2. Primary sources

| ID | Source | URL | Purpose |
|---|---|---|---|
| SRC-IFC5-LEARN | buildingSMART IFC 5 learning portal | https://ifc5.technical.buildingsmart.org/ | Concepts, learning materials, current IFC 5 direction |
| SRC-IFC5-DEV | buildingSMART IFC 5 development repository | https://github.com/buildingSMART/IFC5-development | Schema, examples, viewer, utilities, issues |
| SRC-IFC5-PLAN | IFC 5 Core Project Plan | https://www.buildingsmart.org/ifc-5-core-project-plan-is-now-out-for-review-by-the-standards-committee/ | Core scope, modularisation and project direction |
| SRC-IFC4X3 | IFC 4.3 documentation | https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/ | Current IFC compatibility and mapping baseline |
| SRC-PRAVO | Official Russian legal publication portal | https://publication.pravo.gov.ru/ | Normative references and evidence links |

## 3. Repository areas to study

| Area in IFC5-development | Research question | BAV relevance |
|---|---|---|
| `schema/` | What is minimal in the IFC 5 Core? | BAV Core entities and extension slots |
| `examples/` | How are projects, spatial structures and elements composed? | BAV graph and IFCA examples |
| `src/` | How are schemas parsed, validated and processed? | IFCA tooling and validation |
| `docs/viewer/` | How is IFC 5 data visualised? | BAV Viewer requirements |
| Issues / Discussions | What problems and decisions are being discussed? | Open questions and future alignment |

## 4. Citation template

Every extracted idea or decision must record:

```yaml
source_id: SRC-IFC5-DEV
source_url: https://github.com/buildingSMART/IFC5-development
path: schema/...
commit_or_version: <commit sha or release>
accessed_at: 2026-10-18
note: <what was studied>
```

## 5. Rules

1. Do not copy IFC 5 materials into BRAVIM as if they were ours.
2. Always link to the official source.
3. Record the accessed date and, where possible, commit or release.
4. Separate facts from our interpretation.
5. Mark all IFCA decisions as experimental.
6. Do not treat IFC 5 alpha examples as production-ready.

## 6. Status

```text
IFC 5 / IFCX = primary research source
IFCA = BRAVIM research prototype
BAV = BRAVIM central concept
```