# BRAVO Architecture v0.3 — Client-Server Model with BAG

Version: 0.3
Date: 2026-10-18
Status: Architecture proposal
Purpose: define the BRAVO client-server architecture, the BRAV container and the Building Activity Log (BAG)

## 1. Summary

BRAVO is a client-server platform in which a building exists as a **Building Avatar (BAV)**. The server side, **BRAVIUM Planet**, publishes verified knowledge and manages project registries. The client side, **BRAVIM Local Core**, works with project data, applies rules and keeps a complete activity history.

The central project artifact is the **BRAV container**:

```text
BRAV container = IFCA + BAR + BAV + BAG
```

| Component | Role |
|---|---|
| **IFCA** | Exchange and interoperability format |
| **BAR** | Registry of avatars, versions and statuses |
| **BAV** | The building avatar itself |
| **BAG** | Building Activity Log: chronological history of actions, checks and decisions |

## 2. Core principle

```text
BAV answers: "What does the building represent now?"
BAG answers: "What happened to it, who did it, and why?"
BAR answers: "Which avatars and versions exist?"
VAR answers: "How is a specific version represented and exchanged?"
IFCA answers: "How do components and systems exchange data?"
```

BAG is not a duplicate of BAR. BAR stores state and versions; BAG stores events and history.

## 3. System components

### BRAVIUM Planet — server side

Planet is the central knowledge and coordination service.

It provides:

- project registry;
- normative knowledge repository;
- Ruleset Package publication;
- Evidence Fragment registry;
- version management;
- authentication and authorization;
- synchronization endpoints;
- publication and distribution of updates.

Planet does not silently change knowledge used by a project. It publishes new versions and lets the Local Core decide when to adopt them.

### BRAVIM Local Core — client side

The Local Core is installed on a user workstation or project server.

It provides:

- local project workspace;
- BRAV container storage or access;
- Rules Cache;
- validation engine;
- treatment proposal engine;
- local UI;
- synchronization with Planet;
- local activity logging.

The Local Core may work offline or with limited connectivity. It does not require uploading the full BAV to Planet.

### BRAIM — governance layer

BRAIM remains the governance and integration layer.

It provides:

- artifact governance;
- provenance;
- Quality Gate;
- snapshots;
- access control;
- integration with external systems;
- connection to public services where applicable.

## 4. BRAV container

```text
BRAV container
├── IFCA — exchange format
├── BAR — avatar registry and versions
├── BAV — building avatar
└── BAG — activity log
```

### IFCA

IFCA is the exchange format between components and external systems.

It provides:

- standardized data exchange;
- compatibility with external tools;
- integrity references;
- module-based representation.

### BAR

BAR is the registry.

It stores:

- avatar identities;
- version history;
- statuses;
- evidence references;
- rule bindings;
- publication state.

### BAV

BAV is the building avatar.

It contains:

- entities and IDs;
- classifications;
- geometry;
- spatial and topological relations;
- properties;
- lifecycle state;
- validation results;
- treatment references.

### BAG

BAG is the Building Activity Log.

It records:

- project creation;
- entity creation and modification;
- rule application;
- validation runs;
- findings;
- treatment proposals;
- approvals and rejections;
- synchronization events;
- publication events;
- user actions.

## 5. BAG specification

### Event structure

Every BAG event should contain:

```text
event_id
timestamp
actor
actor_role
action
target_type
target_id
before_state
after_state
related_rule
related_evidence
related_treatment
result
source
```

### Event categories

```text
project
entity
property
geometry
classification
validation
finding
treatment
approval
publication
synchronization
access
```

### Example events

```text
PROJECT_CREATED
BAV_ENTITY_CREATED
BAV_PROPERTY_CHANGED
RULE_APPLIED
VALIDATION_RUN
FINDING_CREATED
TREATMENT_PROPOSED
TREATMENT_APPROVED
TREATMENT_REJECTED
RECHECK_COMPLETED
RULESET_VERSION_PINNED
PROJECT_PUBLISHED
```

### BAG principles

```text
1. Every important action is recorded.
2. Events are append-oriented.
3. Events are linked to actors and targets.
4. Validation events link to rules and evidence.
5. Decision events link to treatments.
6. Sensitive data is not exposed through logs.
7. Logs support filtering, search and export.
```

## 6. Interaction flow

### Project initialization

```text
1. Create project on Planet.
2. Download or initialize BRAVIM Local Core.
3. Connect to Planet.
4. Initialize BRAV container.
5. Initialize BAG.
6. Pin initial Ruleset Package version.
```

### Project work

```text
1. Load normative knowledge through BRAIM / Planet.
2. Create or edit BAV.
3. Apply rules.
4. Record actions in BAG.
5. Produce findings.
6. Propose treatments.
7. Obtain human approval.
8. Recheck.
9. Generate reports.
```

### Synchronization

```text
1. Local Core exchanges project references and required metadata with Planet.
2. Planet proposes Ruleset Package updates.
3. Local Core pins or adopts a new version.
4. BAG records synchronization and version changes.
5. Project data remains locally controlled.
```

## 7. Security and access

### Principles

```text
1. Project data remains under project control.
2. Local Core may work without sending the full model to Planet.
3. Planet receives only the minimum data needed for rule selection.
4. Access is role-based.
5. Important actions are recorded in BAG.
6. Sensitive data is not exposed through logs.
7. Public specifications and private project data are separated.
```

### Minimum roles

```text
owner
editor
reviewer
viewer
administrator
```

### Security measures

```text
- authentication and authorization
- role-based access
- audit logging through BAG
- encryption of sensitive data where required
- controlled export
- no automatic full-model upload
```

## 8. MVP scope

The v0.3 MVP should prove one complete chain:

```text
1. One residential building fragment.
2. One BRAV container.
3. One Ruleset Package.
4. 3-5 rules.
5. One validation run.
6. One grouped finding.
7. One treatment proposal.
8. One human approval.
9. One recheck.
10. Complete BAG history for the scenario.
```

The MVP succeeds if a reviewer can reconstruct:

```text
What changed?
Who changed it?
Which rule was applied?
What evidence was used?
What finding appeared?
What treatment was proposed?
Who approved it?
What was the recheck result?
```

## 9. What we do not do in v0.3

```text
No mandatory microservices architecture
No mandatory cloud deployment
No automatic full-model upload
No autonomous design
No silent conflict resolution
No replacement of CDE
No replacement of calculation tools
No black-box AI decisions
```

Technology choices such as NoSQL, graph database, vector storage or message broker are implementation decisions. They should be selected when real scale and workload require them.

## 10. v0.3 roadmap

| Step | Result |
|---|---|
| 1 | BRAV container definition |
| 2 | BAG event model v0.1 |
| 3 | BAR / BAG separation rules |
| 4 | Planet API contract v0.1 |
| 5 | Local Core synchronization contract v0.1 |
| 6 | BAG-based audit timeline |
| 7 | MVP scenario with full activity history |
| 8 | Security and access model refinement |

## 11. Main formula

```text
Planet publishes knowledge.
BRAIM governs information.
BRAVIM works locally.
BAV represents the building.
BAR registers versions.
BAG remembers activity.
IFCA exchanges data.
A human decides.
BRAVO is the whole system.
```

> The goal of v0.3 is not to build a maximal platform.
> The goal is to make every important project action visible, traceable and recoverable.