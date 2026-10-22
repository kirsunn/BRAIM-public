# BRAVO Architecture v0.4

Version: 0.4
Date: 2026-10-18
Status: Architecture baseline for implementation planning
Purpose: define the BRAVO client-server architecture, BRAV container and readiness for the next development stage

## 1. Summary

BRAVO is a client-server platform in which a building exists as a **Building Avatar (BAV)**.

The cloud platform **BRAVIUM-Planet** hosts projects, knowledge and the **BRAIM** knowledge-and-integration core. The local client **BRAVIM** works with a project through a **BRAV container**.

```text
BRAVIUM-Planet (cloud)
├── BRAIM — knowledge, norms, integrations
├── Project Registry
├── Ruleset Packages
└── Evidence / Knowledge Base

        ↕ API

BRAVIM (local client)
└── BRAV container
    ├── IFCA — exchange format
    ├── BAR — version registry
    ├── BAV — building avatar
    ├── RAG — requirements and constraints graph
    └── BAG — activity log
```

## 2. Components and roles

| Component | Location | Function |
|---|---|---|
| **BRAVIUM-Planet** | Cloud | Stores projects, knowledge, rules and evidence |
| **BRAIM** | Inside Planet | Manages norms, criteria, integrations and knowledge verification |
| **BRAVIM** | Local PC or project server | Works with the project, performs checks and validation |
| **BRAV** | Inside BRAVIM | Project container with IFCA, BAR, BAV, RAG and BAG |

### BRAVIUM-Planet

Planet is the central cloud environment.

It provides:

- project registry;
- BRAIM knowledge core;
- Ruleset Packages;
- Evidence / Knowledge Base;
- authentication and authorization;
- synchronization API;
- publication and update distribution.

### BRAIM

BRAIM is hosted inside Planet.

It provides:

- current normative criteria;
- integration management;
- rule verification;
- evidence linkage;
- connection to external services, including public services where applicable.

BRAIM does not silently change knowledge used by a project. It publishes versions; BRAVIM decides when to adopt them.

### BRAVIM

BRAVIM is the local client.

It provides:

- local project workspace;
- BRAV container storage or access;
- Rules Cache;
- validation engine;
- treatment proposal engine;
- local UI;
- synchronization with Planet.

BRAVIM may work offline or with limited connectivity. It does not require uploading the full BAV to Planet.

## 3. BRAV container

```text
BRAV container
├── IFCA — exchange format
├── BAR — version registry
├── BAV — building avatar
├── RAG — requirements and constraints graph
└── BAG — activity log
```

### IFCA

IFCA is the exchange format between components and external systems.

It provides standardized exchange, compatibility and integrity references.

### BAR

BAR is the registry of avatars and versions.

It stores identities, version history, statuses, evidence references and rule bindings.

### BAV

BAV is the building avatar.

It contains entities, classifications, geometry, spatial relations, properties, lifecycle state, validation results and treatment references.

### RAG

**RAG** means **Requirements & Constraints Graph**.

It is stored inside the BRAV container and contains the requirements and constraints applicable to the project.

RAG includes:

- project requirements;
- customer constraints;
- site constraints;
- normative criteria;
- applicability conditions;
- priorities;
- dependencies;
- conflicts.

RAG is populated from BRAIM and linked to BAV for validation.

### BAG

BAG is the Building Activity Log.

It records project creation, entity changes, rule application, validation runs, findings, treatment proposals, approvals, rejections, synchronization and publication events.

## 4. How the system works

### On Planet

```text
1. BRAIM stores current normative criteria.
2. BRAIM manages integrations.
3. BRAIM verifies rules.
4. Planet publishes Ruleset Packages.
```

### On BRAVIM

```text
1. BRAVIM loads required data.
2. BRAVIM works with BAV.
3. BRAVIM applies rules received through BRAIM.
4. BRAVIM records results in BAG.
```

### Interaction

```text
1. BRAVIM requests rules through the Planet API.
2. BRAIM provides current applicable versions.
3. BRAVIM pins the received version.
4. BRAVIM validates BAV against RAG.
5. Results are recorded in BAG.
```

## 5. RAG in detail

RAG answers:

```text
Which requirements and constraints apply to this project,
under which conditions,
with which priority,
and how are they connected?
```

RAG is not a copy of all norms. It is the project-specific graph of applicable requirements and constraints.

```text
BRAIM publishes knowledge.
RAG contains the applicable project-specific subset.
BAV is checked against RAG.
BAG records the entire process.
```

## 6. Advantages

- centralized normative management;
- local project autonomy;
- clear separation of responsibilities;
- transparent links between knowledge, model, checks and decisions;
- effective activity logging through BAG;
- no mandatory full-model upload to the cloud.

## 7. Areas for further specification

### Planet API

- main endpoints;
- request and response formats;
- authentication protocol;
- version negotiation;
- caching strategy.

### RAG

- graph structure;
- requirement types;
- constraint types;
- validation algorithms;
- update mechanism;
- conflict representation.

### Synchronization

- synchronization strategy;
- conflict handling;
- offline mode;
- delta exchange;
- version adoption rules.

### BAR versioning

- version identity;
- status model;
- branching policy;
- supersession rules.

### Security

- access model;
- encryption approach;
- backup and recovery;
- audit requirements.

## 8. Readiness assessment

The architecture has reached sufficient maturity to begin implementation planning.

Strong points:

- clear separation of roles;
- transparent Planet–BRAVIM interaction;
- logical placement of BRAIM inside Planet;
- understandable BRAV container structure;
- clear responsibility for each element.

Before implementation, the following must be prepared:

- technical documentation;
- detailed implementation plan;
- development priorities;
- project roadmap.

## 9. Implementation principles

```text
1. Start with one narrow MVP scenario.
2. Do not build all integrations at once.
3. Keep project data locally controlled.
4. Pin every Ruleset Package version.
5. Record every important action in BAG.
6. Do not resolve rule conflicts silently.
7. Keep AI proposals separate from human decisions.
```

## 10. Main formula

```text
Planet hosts the project and BRAIM.
BRAIM provides criteria, norms and integrations.
BRAVIM works locally with the project.
BRAV contains IFCA, BAR, BAV, RAG and BAG.
BAV is checked against RAG.
BAG remembers everything.
A human decides.
BRAVO is the whole system.
```

> BRAVO v0.4 establishes the balance between centralized knowledge management and local project autonomy, while preserving transparency across all processes.