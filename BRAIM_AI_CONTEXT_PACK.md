# BRAVO v0.4 Architecture Update

> **Architecture update v0.4:** BRAIM is hosted inside BRAVIUM-Planet. The BRAV container is `IFCA + BAR + BAV + RAG + BAG`. BAV is validated against RAG; BAG records activity and decisions. See [`BRAVO_ARCHITECTURE_V0_4.md`](./BRAVO_ARCHITECTURE_V0_4.md).

# BRAIM AI Context Pack

## Версия

- Version: `0.2.0`
- Date: 2026-10-18
- Intended users: external AI systems, reviewers, developers and research agents

## Task

Analyze, extend or prototype BRAIM and its Building Avatar extension BRAVIM/BAV — a research and prototype openBIM platform for construction requirements, spatial entities, planning generation, validation, IFC/Archicad coordination and documentation.

Do not treat the repository as a completed product. Treat it as a structured set of drafts, hypotheses, schemas and prototypes.

## Product family & naming

| Name | Meaning |
|---|---|
| **BRAIM** | Governance platform: artifact registry, provenance, Quality Gate, snapshots, CDE integration |
| **BRAVIM** | Building Avatar platform |
| **BAV** | Building Avatar: the building as a verifiable entity |
| **BAR** | Building Avatar Registry: registry of avatars, versions, evidence and rules |
| **VAR** | Versioned Avatar Representation: versioned representation for storage, exchange and reproducibility |
| **RAG** | Requirements & Constraints Graph: project-specific graph of applicable requirements and constraints |
| **BAG** | Building Activity Log: chronological history of actions, checks and decisions |
| **IFCA** | Exchange format for BAV |
| **BRAVO** | Umbrella product suite: BRAIM + BRAVIM/BAV + IFCA |

```text
BRAV = IFCA + BAR + BAV + RAG + BAG
```

A rule is not merely a quotation from a regulation. It is a verifiable statement linked to an official source and executable over BAV.

## Core rules

- One concept ID and one instance ID across all representations.
- Semantic layers and discipline views are separate axes.
- Normative source, project requirement, AI inference and derived calculation are different evidence classes.
- `Room != Zone`; `Opening != Filling`; `Adjacency != Access`.
- Hard constraints reject candidates; soft constraints affect ranking.
- Unknown values remain unknown.
- Never invent a current normative requirement without an official source and applicability.
- Mark uncertain reasoning as `PROPOSED` or `NEEDS_REVIEW`.
- Preserve source passages and conflicts.
- Do not publish WIP materials as final specifications.
- Do not treat a Ruleset Package as an official normative document; it is a versioned, source-linked knowledge package.
- Do not apply a Ruleset Package without pinning its version and content hash.

## Semantic layers

> Канон — [`BRAIM_Layer_Model_v0_1.md`](./BRAIM_Layer_Model_v0_1.md) (v0.1.2). Старые коды L6-X graph, L7-O openings, L8-I infrastructure, L11-V generator, L14-E operation устарели и не используются.

```text
L0-N normative
L1-C canonical
L2-F functional
L3-R requirements
L4-G geometry
L5-T topology
L6-X extended (уточнить)
L7-O operational/occupancy
L8-CST cost
L9-B BIM/openBIM
L10-A authoring
L11-INT interior/finish (MVP-adjacent)
L12-Q quality
L13-D documentation
L14-E energy/environmental
L15-P provenance
L16-GN generator (DEFERRED 2027+)
L17-MEP MEP systems (RESERVED v0.2+)
```

## Discipline views

```text
D0-GEN coordination
D1-ARC architecture
D2-STR structure
D3-MEP engineering
D4-ELE electrical
D5-FIR fire safety
D6-SIT site
D7-ENV environment/daylight
D8-CST cost
D9-CON construction
D10-FM facility management
D11-INT interior
D12-GEO survey/geospatial/point clouds
D13-SEC information security
```

## Generation directions

```text
PLAN_TO_FORM:
requirements → topology → rooms/zones → geometry → openings → mass/facade

FORM_TO_PLAN:
form/volume → sections/usable fields → rooms/zones → openings → validation

ITERATIVE:
plan → form → facade → constraints → plan update
```

## Current highest-value tasks

- complete the BRAIM Entity Meta-Model;
- define Attribute Registry;
- define Claim/Evidence Registry;
- define Model View Registry;
- implement Core Validation Kernel;
- normalize terminology from TERMINY.xlsx;
- implement topology-first layout generation;
- implement geospatial/point-cloud data contracts;
- prototype the hexagonal swept-loop house;
- define public/private CDE synchronization;
- develop BAV, IFCA, Evidence Fragment, Ruleset Package and Treatment Package specifications;
- keep BAV Local Core version pinning and evidence references consistent.