# IFCA Prototype Decisions

Status: Research decisions  
Date: 2026-10-18  
Project: BRAVIM / Building Avatar (BAV)  
Basis: IFC 5 / IFCX research

## 1. Purpose

This document records the initial IFCA decisions derived from the study of IFC 5 / IFCX.

IFCA remains an experimental research prototype. Decisions may change as IFC 5 evolves.

## 2. Accepted decisions

| Decision | Choice | Rationale |
|---|---|---|
| Format | JSON-first | IFCA should be readable, tool-friendly and suitable for APIs |
| File extension | `.ifca` | Short, clear and aligned with the IFCA research name |
| Core | Minimal BAV Core | Identity, type, spatial containment, references and extension slots |
| Inheritance | Type → Occurrence | Common data belongs to types; entities store overrides |
| Modules | Separate extension modules | Geometry, normative, provenance, lifecycle, cost and CAD mappings |
| References | Reference external data | Normative documents, evidence and geometry are not copied into entities |
| Provenance | Assertion-based | Provenance is stored as assertions and source references |
| Lifecycle | Scope-based | Lifecycle states belong to scopes and project fragments |
| IFC compatibility | IFC 4.3 adapter | IFCA must remain mappable to current BIM workflows |
| Human approval | Required for changes | IFCA may contain proposals, but humans approve changes |

## 3. IFCA container

```text
.ifca
├── ifca.format
├── ifca.version
├── bav_id
├── snapshot
├── core
├── modules
└── references
```

Example:

```json
{
  "ifca": {
    "format": "IFCA",
    "version": "0.1.0",
    "bav_id": "BAV-000123",
    "snapshot": "SNAP-000045",
    "core": {
      "project": { "id": "PRJ-001" },
      "spatial": {
        "site": "SITE-001",
        "building": "BLDG-001",
        "storeys": ["STOREY-01"],
        "spaces": ["SPACE-101"]
      },
      "entities": [
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
      ]
    },
    "modules": {
      "geometry": "GEOM-SNAP-000045",
      "normative": "RULESET-2026.10.1",
      "provenance": "PROV-SNAP-000045",
      "lifecycle": "LC-DESIGN"
    }
  }
}
```

## 4. Deferred decisions

| Topic | Decision | Reason |
|---|---|---|
| IFCX serialization | Defer | IFC 5 / IFCX is still alpha and may change |
| Graph database engine | Defer | Start with a stable canonical model; choose storage later |
| Full lifecycle support | Defer | Start with concept, design and review |
| Full normative coverage | Defer | Begin with a small verified ruleset |
| Public BAVX format | Defer | Keep IFCA as the research prototype for now |

## 5. Review criteria

IFCA decisions should be reviewed when:

- IFC 5 / IFCX releases a stable schema;
- a real IFC 4.3 ↔ IFCA adapter is tested;
- the first BAV Viewer prototype works;
- normative rules and evidence are validated;
- a complete minimal `.ifca` example is created.

## 6. Status

```text
IFCA = experimental research prototype
BAV = BRAVIM central model
IFC 5 / IFCX = primary research source
```