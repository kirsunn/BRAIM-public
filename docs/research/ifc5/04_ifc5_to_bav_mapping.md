# IFC 5 → BAV Concept Mapping

Status: Initial research mapping  
Date: 2026-10-18  
Project: BRAVIM / Building Avatar (BAV)  
Purpose: compare IFC 5 / IFCX concepts with BAV and define the initial IFCA direction

## 1. Purpose

This document maps concepts from IFC 5 / IFCX to the BRAVIM Building Avatar (BAV) model.

It is a research artefact, not a final specification. Each decision may change as IFC 5 evolves.

Primary source:

- buildingSMART IFC 5 development repository: https://github.com/buildingSMART/IFC5-development
- buildingSMART IFC 5 learning portal: https://ifc5.technical.buildingsmart.org/

## 2. Decision labels

| Label | Meaning |
|---|---|
| `STUDY` | Needs further research |
| `ADOPT` | Use the idea in BAV / IFCA |
| `ADAPT` | Use the idea, but change it for BAV needs |
| `REJECT` | Do not use in the current BAV model |
| `DEFER` | Postpone until IFC 5 stabilises |

## 3. Initial mapping

| IFC 5 / IFCX concept | BAV concept | Decision | Notes |
|---|---|---|---|
| Minimal Core | BAV Core | ADOPT | BAV Core should contain only identity, basic typing and essential references |
| Modular extensions | BAV Extensions | ADOPT | Geometry, normative, provenance, lifecycle, cost and CAD mappings are separate modules |
| JSON-first representation | IFCA JSON | ADOPT | IFCA uses a readable JSON container |
| Reference to external data | BAV Reference | ADOPT | Normative documents, evidence and external schemas are referenced, not copied |
| Type → Occurrence | BAV Type → BAV Entity | ADOPT | Common properties belong to a type; occurrences store overrides |
| Property Set Template | BAV Attribute Profile | ADAPT | A profile defines fields and constraints for many attribute sets |
| Property Set | BAV Attribute Set / Assertion | ADAPT | Properties are grouped and can be attached to entities |
| Relationship object | BAV Relationship | ADOPT | Relationships remain first-class graph edges or relationship entities |
| Spatial structure | BAV Spatial Graph | ADAPT | Site → building → storey → space hierarchy remains central |
| GlobalId | BAV ID | ADAPT | BAV needs its own stable identity plus mappings to IFC GlobalId |
| Provenance / ownership history | BAV Provenance | ADAPT | Provenance is stored as assertions and references, not duplicated on every entity |
| Lifecycle | BAV Lifecycle | ADAPT | Lifecycle is scope-based and hierarchical |
| Cloud collaboration | BRAVIM Planet / Cloud Brain | ADAPT | Cloud provides knowledge and collaboration; local core remains the project body |
| Geometry representation | BAV Geometry Module | ADAPT | Geometry is referenced, not necessarily embedded in the core entity |
| IFC 4.3 compatibility | IFC 4.3 adapter | ADOPT | IFCA must remain mappable to current IFC 4.3 workflows |
| IFCX serialization | Future IFCA serialization target | DEFER | Follow IFC 5 / IFCX until the format stabilises |

## 4. BAV Core candidate

```text
BAV Core
├── BAV ID
├── Type
├── Spatial containment
├── References
└── Extension slots
```

Example:

```json
{
  "id": "WALL-001",
  "type": "wall",
  "typeRef": "WALL-TYPE-014",
  "geometryRef": "GEOM-WALL-001",
  "extensions": {
    "fire": "FIRE-SET-014",
    "provenance": "IMP-000123"
  }
}
```

## 5. Open questions

1. Which IFC 5 Core entities are stable enough to map now?
2. How should BAV IDs map to IFC GlobalId without losing either identity?
3. Should BAV use IFC property sets directly or define its own assertion model?
4. How should normative evidence reference official publications?
5. What is the minimal IFCA example: site → building → storey → space → wall?
6. How should CAD mappings be stored for Archicad, Revit, Renga and nanoCAD?
7. When should IFCA align with IFCX serialization?

## 6. Status

```text
IFC 5 / IFCX = primary research source
BAV = BRAVIM central model
IFCA = experimental JSON research prototype
```

> This mapping is a living research document. It will be updated as IFC 5 / IFCX materials and BRAVIM requirements evolve.