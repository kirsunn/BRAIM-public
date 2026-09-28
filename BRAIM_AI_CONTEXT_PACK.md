# BRAIM AI Context Pack

## Версия

- Version: `0.1.0`
- Date: 2026-09-28
- Intended users: external AI systems, reviewers, developers and research agents

## Task

Analyze, extend or prototype BRAIM — a research and prototype openBIM platform for construction requirements, spatial entities, planning generation, validation, IFC/Archicad coordination and documentation.

Do not treat the repository as a completed product. Treat it as a structured set of drafts, hypotheses, schemas and prototypes.

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

## Semantic layers

```text
L0-N normative
L1-C canonical
L2-F functional
L3-R requirements
L4-G geometry
L5-T topology
L6-X graph
L7-O openings
L8-I infrastructure
L9-B BIM/openBIM
L10-A authoring
L11-V generator
L12-Q quality
L13-D documentation
L14-E operation
L15-P provenance
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
- define public/private CDE synchronization.
