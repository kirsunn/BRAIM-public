# BRAVIM Extensions on IFC 5 / IFCX

Status: Research extension manifest  
Date: 2026-10-18  
Project: BRAVIM / Building Avatar (BAV)  
Purpose: define what BRAVIM adds on top of IFC 5 / IFCX for BAV and IFCA

## 1. Position

IFC 5 / IFCX provides a future-oriented foundation for openBIM:

- minimal core;
- modular extensions;
- references;
- JSON-first representation;
- type/occurrence modelling;
- cloud collaboration.

BRAVIM does not replace IFC 5. It extends its ideas with the specific needs of a **Building Avatar**: normative intelligence, provenance, local ownership, diagnostics, forecasting and lifecycle support.

```text
IFC 5 / IFCX = openBIM foundation
BAV          = BRAVIM building avatar model
IFCA         = BRAVIM research representation of BAV
```

## 2. What BRAVIM adds

| IFC 5 / IFCX baseline | BRAVIM extension | IFCA module | Purpose |
|---|---|---|---|
| Core entities | Building Avatar | `bav` | A living, versioned avatar of a building |
| References | Normative references | `normative` | Links to official sources such as pravo.gov.ru |
| External data | Evidence model | `normative` | Traceable fragments, quotes, hashes and applicability |
| Property sets | Ruleset Packages | `normative` | Versioned, pinned sets of required/recommended criteria |
| Ownership history | Provenance assertions | `provenance` | Source, actor, operation, snapshot and trust context |
| Lifecycle | Hierarchical lifecycle | `lifecycle` | Fragment-level states from concept to demolition |
| Cloud collaboration | BRAVIM Planet | `planet` | Verified knowledge, rulesets, evidence and updates |
| Local data | BAV Local Core | `local` | Local body, memory, graph and project store |
| Model exchange | CAD connectors | `cad` | Archicad, Revit, Renga, nanoCAD mappings |
| Model changes | Treatment Packages | `treatment` | Proposed changes with impact preview and human approval |
| Validation | Diagnostic and Forecast | `diagnostic`, `forecast` | Findings, risks, consequences and alternatives |
| Serialization | IFCA / BAVX | `serialization` | `.ifca` research format and potential `.bavx` public format |

## 3. BAV-specific entities

### Building Avatar

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

A BAV is not a file. It is a versioned digital state of a building that can begin at any lifecycle stage.

### Normative Rule

```text
NormativeRule
├── rule_id
├── statement
├── severity: required | recommended | informational | assumption
├── applicability
├── evidence_ids
└── ruleset_version
```

BRAVIM does not sign official documents. It references them.

### Evidence Fragment

```text
EvidenceFragment
├── evidence_id
├── official_url
├── publication_id
├── section_or_fragment
├── accessed_at
├── content_hash
└── source_status
```

### Ruleset Package

```text
RulesetPackage
├── package_id
├── version
├── published_at
├── content_hash
├── scope
├── rules
└── evidence
```

The Local Core pins a Ruleset Package version so that a validation result remains reproducible.

### Treatment Package

```text
TreatmentPackage
├── package_id
├── goal
├── affected_bav_ids
├── operations
├── rules_checked
├── evidence_ids
├── impact_preview
└── approval_status
```

A Treatment Package is a proposed, explainable change. It is applied only after human approval.

## 4. Extension slots in IFCA

```json
{
  "id": "WALL-001",
  "type": "wall",
  "typeRef": "WALL-TYPE-001",
  "geometryRef": "GEOM-WALL-001",
  "extensions": {
    "fire": "FIRE-SET-001",
    "provenance": "IMP-000001",
    "lifecycle": "LC-DESIGN",
    "cost": "COST-SET-001",
    "cad": "CAD-MAP-001"
  }
}
```

The core entity remains lightweight. BRAVIM-specific knowledge is connected through extension references.

## 5. BRAVIM-specific principles

1. **Avatar-first** — the building avatar, not a file, is the central object.
2. **Normative-first** — requirements and evidence are first-class citizens.
3. **Local-first** — the user controls the local BAV body and memory.
4. **Planet-first for knowledge** — verified criteria come from BRAVIM Planet.
5. **Evidence-first** — a rule without a traceable source cannot become active.
6. **Human-in-the-loop** — BRAVIM proposes; a human approves.
7. **Consequence-aware** — changes are connected to forecasts and impacts.
8. **Lifecycle-native** — BAV exists from idea to demolition.
9. **Connector-native** — CAD/BIM systems are senses and hands of the avatar.
10. **IFC-compatible** — IFCA remains mappable to IFC 4.3 and future IFCX.

## 6. What IFC 5 does not yet cover

| Need | IFC 5 / IFCX status | BRAVIM answer |
|---|---|---|
| Verified normative knowledge | Not a core concern | BRAVIM Planet and Ruleset Packages |
| Official legal source linking | Not a core concern | Evidence Fragment and Official Publication |
| Local-first avatar ownership | Partially related | BAV Local Core |
| Treatment proposals with approval | Not a core concern | Treatment Package |
| Diagnostic and forecast semantics | Not a core concern | Diagnostic and Forecast modules |
| Russian normative context | Not a core concern | Normative profiles and evidence |
| Building Avatar as user-facing object | Not a core concern | BAV |

## 7. Relationship to IFCA

```text
IFCA Core
= BAV identity, spatial structure and references

IFCA Extensions
= geometry, normative, provenance, lifecycle, cost, operation, CAD

IFCA References
= IFC 4.3, IFCX, documents, Planet packages
```

IFCA is the research container where these extensions are tested.

## 8. Next steps

```text
1. Define BAV Extension Schema v0.1
2. Define Ruleset Package Schema v0.1
3. Define Evidence Fragment Schema v0.1
4. Define Treatment Package Schema v0.1
5. Add BRAVIM extensions to the minimal .ifca example
6. Create an IFC 4.3 ↔ IFCA mapping
```

## 9. Main formula

```text
IFC 5 / IFCX gives the openBIM foundation.
BRAVIM adds the Building Avatar layer.
BAV makes the building understandable, traceable and lifecycle-aware.
IFCA makes BAV representable and exchangeable.
```

> **IFC 5 / IFCX is the foundation.**  
> **BRAVIM adds the avatar, knowledge, memory and consequences.**  
> **IFCA is the research container for this extension.**