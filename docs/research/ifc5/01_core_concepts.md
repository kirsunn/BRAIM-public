# IFC 5 Core Concepts for BAV

Status: Research notes  
Date: 2026-10-18  
Project: BRAVIM / Building Avatar (BAV)  
Purpose: extract IFC 5 / IFCX concepts relevant to BAV and IFCA

## 1. Research principle

This document separates:

```text
IFC 5 fact → BAV interpretation → IFCA decision
```

All decisions are experimental and may change as IFC 5 evolves.

Primary sources:

- https://ifc5.technical.buildingsmart.org/
- https://github.com/buildingSMART/IFC5-development

## 2. Concept review

| IFC 5 concept | Essence | BAV interpretation | Decision |
|---|---|---|---|
| Minimal Core | Keep only domain-neutral essentials in the core | BAV Core: identity, type, spatial containment, references, extension slots | ADOPT |
| Modularisation | Add domain capabilities through modules | Geometry, normative, provenance, lifecycle, cost, operation and CAD modules | ADOPT |
| JSON-first | Use JSON as a primary machine-friendly representation | IFCA is a JSON container for BAV | ADOPT |
| References | Link to external data instead of duplicating it | Normative rules, evidence, documents and geometry are referenced | ADOPT |
| Type / Occurrence | Separate shared type information from individual occurrences | BAV Type defines common data; BAV Entity stores overrides | ADOPT |
| Spatial structure | Model containment and spatial relationships | Site → building → storey → space hierarchy | ADAPT |
| Relationships | Treat relationships as meaningful first-class structures | BAV graph edges and relationship entities | ADOPT |
| Provenance | Preserve origin, actor and history | BAV provenance assertions and source references | ADAPT |
| Lifecycle | Represent stages and transitions | Hierarchical lifecycle states for project fragments | ADAPT |
| Cloud collaboration | Enable shared, live project interaction | BRAVIM Planet / Cloud Brain services | ADAPT |

## 3. BAV Core candidate

```text
BAV Core
├── BAV ID
├── Type
├── Spatial containment
├── References
└── Extension slots
```

The core must remain small. Everything else should be added through modules.

## 4. What BAV changes

BAV does not simply copy IFC 5. It adds:

- Building Avatar as the central user-facing concept;
- normative knowledge and evidence as first-class concerns;
- local-first data ownership;
- treatment packages and human approval;
- lifecycle-oriented diagnostics and forecasting;
- explicit mapping to CAD/BIM platforms.

## 5. Open questions

1. Which IFC 5 Core entities are stable enough to map now?
2. How should BAV IDs coexist with IFC GlobalId?
3. Should IFCA reuse IFC property-set semantics or define its own assertion model?
4. How should geometry be referenced without making the core heavy?
5. How should lifecycle states be inherited across scopes?

## 6. Status

```text
IFC 5 / IFCX = primary research source
BAV = BRAVIM central model
IFCA = experimental JSON research prototype
```