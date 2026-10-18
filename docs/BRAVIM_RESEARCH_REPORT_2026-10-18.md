# BRAVIM Research Report — 2026-10-18

Status: Research / Manifesto  
Date: 2026-10-18  
Project: BRAVIM / Building Avatar (BAV)  
Scope: consolidated research decisions and manifests

## 1. Main shift

BRAVIM evolved from the idea of an “AI IFC validator” into a broader research concept:

```text
BRAVIM — a research platform for the Building Avatar.
BAV — a living digital avatar of a building.
IFCA — an experimental research representation and exchange prototype for BAV.
IFC 4.3 — a compatibility bridge to current BIM systems.
IFC 5 / IFCX — a primary source of architectural ideas.
```

BRAVIM does not replace the GAP, GIP, designer or expert. It helps understand what is required or recommended, analyses the BAV, explains inconsistencies, proposes alternatives and forecasts consequences.

## 2. Naming manifesto

```text
BRAVIM = Building Avatar Intelligence Model
BAV    = Building Avatar
BRAIM  = legacy working name
IFCA   = IFC Avatar — research prototype
BAVX   = potential future exchange format
```

| Level | Name | Meaning |
|---|---|---|
| Research platform | **BRAVIM** | Environment, brain and orchestration |
| Central entity | **BAV** | Living building avatar |
| Local core | **BAV Local Core** | Body, memory and project graph |
| Cloud intelligence | **BRAVIM Planet / Cloud Brain** | Verified knowledge and services |
| Research format | **IFCA** | JSON representation of BAV |
| Potential public format | **BAVX** | Building Avatar eXchange |
| Legacy name | **BRAIM** | Former working name |

Slogans:

```text
BRAVIM — the Building Avatar Platform.
BRAVIM creates BAV.
BAV — the avatar of your building.

BRAVIM knows what is required.
The designer decides how to achieve it.
```

## 3. Building Avatar manifesto

```text
BAV is not a file.
BAV is a living, versioned state of a building.
```

```text
BAV
├── Identity
├── Body
├── Memory
├── Requirements
├── Evidence
├── Relationships
├── Health
└── Future
```

A BAV can be created at any lifecycle stage: from an idea, site, PDF, IFC file, CAD model, survey, as-built documentation, operation data or pre-demolition data.

## 4. BAV Local Core manifesto

```text
BAV Local Core — the local body, memory and nervous system of the avatar.
```

```text
BAV Local Core
├── BAV Graph Store
├── BAV Document Store
├── BAV Version Store
├── Rules Cache
├── Project Rules
├── Validator
├── Diagnostic
├── Treatment Builder
└── Connector Layer
```

Principles:

```text
Locally — the body and memory of BAV.
In the cloud — intelligence, normative knowledge and collaboration.
Data leaves the local environment only according to the project data policy.
```

## 5. BRAVIM Planet manifesto

```text
BRAVIM Planet — a verifiable “planet of knowledge”.
```

Planet is the authoritative publisher of normative packages, evidence and updates. The Local Core does not invent criteria; it receives, caches and pins the required version.

```text
Planet publishes criteria.
Local Core subscribes to the required set.
BAV is checked against a pinned version.
```

```text
Planet = source of truth for knowledge.
Local Core = source of truth for project state.
Rules Cache = agreement on a specific knowledge version.
```

## 6. Normative source manifesto

BRAVIM does not sign normative documents and does not claim ownership over them.

```text
Official source — the source of truth.
BRAVIM Planet — index, interpretation and navigation.
BAV — consumer of verified knowledge.
```

For `publication.pravo.gov.ru`:

```text
NormativeRule
→ EvidenceFragment
→ OfficialPublication
→ OfficialSource
```

Required reference fields:

```text
official_url
publication_id / eo_number
publish_date
edition / status
accessed_at
content_hash
fragment locator
```

## 7. Provenance and inheritance manifesto

```text
Every entity has a source.
But not every entity needs to store the full provenance chain.
```

```text
Entity = minimal container of unique data.
Scope = shared context: project → storey → room.
Assertion = a statement about a property.
Source = where the statement came from.
```

Inheritance order:

```text
1. Entity override
2. Type / profile
3. Scope: room → storey → project
4. Snapshot / import batch
5. BRAVIM Planet ruleset
```

Example:

```json
{
  "id": "WALL-001",
  "type": "wall",
  "typeRef": "WALL-TYPE-014",
  "originRef": "IMP-000123",
  "overrides": {
    "fire_rating": "REI 60"
  }
}
```

## 8. IFCA manifesto

```text
IFCA = IFC Avatar
IFCA = experimental JSON research prototype for BAV
```

IFCA is not a replacement for IFC, not a fork, and not a new official standard. It is a research laboratory for testing IFC 5 / IFCX-inspired ideas.

Principles:

```text
Core-first
Reference-first
Module-first
JSON-first
Immutable history
Explicit provenance
IFC-compatible mapping
Human-in-the-loop
```

```text
.ifca
├── core: project, spatial, entities
├── modules: geometry, normative, provenance, lifecycle
└── references: IFC 4.3, IFCX, documents
```

## 9. IFC 5 / IFCX manifesto

```text
IFC 5 / IFCX — architectural compass.
IFCA — our working research implementation for BAV.
IFC 4.3 — bridge to the existing world.
```

We take from IFC 5:

- minimal core;
- modular extensions;
- references instead of copies;
- JSON-first approach;
- Type → Occurrence inheritance;
- relationship objects;
- cloud collaboration model.

We do not copy IFC 5 examples into production and do not create a derivative repository. We use them as research material, reference the primary sources and may participate through issues or pull requests.

Primary sources:

- buildingSMART IFC 5 learning portal: https://ifc5.technical.buildingsmart.org/
- buildingSMART IFC 5 development repository: https://github.com/buildingSMART/IFC5-development
- IFC 4.3 documentation: https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/
- Official Russian legal publication portal: https://publication.pravo.gov.ru/

## 10. Connector manifesto

```text
BAV Connector — the senses and actions of the avatar.
```

```text
BAV Eye    — IFC, PDF, DWG, photos
BAV Ear    — requirements, dialogue, IDS
BAV Hand   — Archicad, Revit, Renga, nanoCAD
BAV Memory — snapshots, versions, history
BAV Voice  — reports and explanations
BAV Action — Treatment Package and approved changes
```

A connector is not merely an exporter. It is a translator of design intent:

```text
Source Model
→ Semantic Understanding
→ Canonical BAV State
→ Target-Specific Reconstruction
→ Native Model
```

## 11. File extension manifesto

```text
.ifca — IFCA research prototype
.bavx — potential future public BAV format
.ifc  — IFC 4.3
.ifcx — IFC 5 / IFCX
```

Windows supports four-character extensions; the historical three-character limitation belongs to DOS/FAT, not modern NTFS/Windows.

Recommendation:

```text
Now: .ifca
Future public format: .bavx
Interoperability: .ifc and .ifcx
```

## 12. Next steps

```text
1. Study IFC5-development: schema, examples, docs
2. Create an IFC5 → BAV mapping
3. Fix BAV Core v0.1
4. Create IFCA JSON Schema v0.1
5. Create the first .ifca example
6. Build an IFC 4.3 ↔ IFCA adapter
7. Prototype the BAV Viewer
8. Fix the Ruleset Package and provenance model
```

## 13. Main formula

```text
BAV — a living avatar of a building.
BRAVIM — the environment that understands and develops it.
BAV Local Core — its body and memory.
BRAVIM Planet — its knowledge and normative memory.
IFCA — its research representation.
IFC 4.3 — its bridge to today’s world.
IFC 5 / IFCX — its orientation toward the future.
```

> **BRAVIM creates BAV.**  
> **BAV lives through the entire building lifecycle.**  
> **IFCA helps BAV remain understandable, verifiable and portable.**