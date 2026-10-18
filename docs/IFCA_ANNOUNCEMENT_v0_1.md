# IFCA v0.1 — Building Avatar Interchange Prototype

Status: Experimental / Alpha  
Date: 2026-10-18  
Project: BRAVIM / Building Avatar (BAV)  
Inspiration: IFC 5 / IFCX concepts  
Compatibility target: IFC 4.3

## 1. What is IFCA?

**IFCA (IFC Avatar)** is an experimental, JSON-first interchange prototype for a **Building Avatar (BAV)** — a living, versioned digital representation of a building across its lifecycle.

IFCA is **not a replacement for IFC** and **not a fork of the IFC standard**. It is a practical prototype exploring ideas expected in the next generation of openBIM, including IFC 5 / IFCX:

- minimal core;
- modular extensions;
- references instead of duplicated data;
- JSON-first representation;
- graph-friendly semantics;
- explicit provenance;
- lifecycle-aware data.

```text
IFCA = IFC Avatar
IFCA = a prototype interchange format for BAV
```

## 2. Position

```text
BAV Graph — source of truth for a building avatar
IFCA      — JSON serialization and exchange container for BAV
IFC 4.3   — current openBIM compatibility layer
IFC 5/IFCX — future-oriented architectural inspiration
```

```text
BAV Local Core
   ↕
IFCA (.ifca / JSON)
   ↕
BAV Viewer · BRAVIM Planet · Connectors
   ↕
IFC 4.3 · Archicad · Revit · Renga · nanoCAD
```

## 3. Design principles

1. **Core-first** — the core contains only essential identity, typing and spatial structure.
2. **Reference-first** — external knowledge, documents and rules are referenced, not copied.
3. **Module-first** — geometry, normative data, provenance and lifecycle are separate modules.
4. **JSON-first** — IFCA is designed as a readable, machine-friendly JSON container.
5. **Immutable history** — changes create deltas and snapshots; history is never silently overwritten.
6. **Explicit provenance** — every important assertion can be traced to its source.
7. **IFC-compatible mapping** — IFCA must remain mappable to IFC 4.3 and future IFCX.
8. **Human-in-the-loop** — IFCA may contain proposed changes, but approval remains a human decision.

## 4. Minimal core

The IFCA core avoids placing every possible attribute on every entity.

```json
{
  "ifca": {
    "format": "IFCA",
    "version": "0.1.0",
    "bav_id": "BAV-000123",
    "snapshot": "SNAP-000045",
    "core": {
      "project": {
        "id": "PRJ-001",
        "name": "Residential building"
      },
      "spatial": {
        "site": "SITE-001",
        "building": "BLDG-001",
        "storeys": ["STOREY-01", "STOREY-02"],
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

## 5. Modules

| Module | Purpose | Example content |
|---|---|---|
| `geometry` | Geometry, placement, representations | Mesh, BRep reference, placement |
| `normative` | Rules, evidence, official source references | Rule ID, severity, evidence fragment |
| `provenance` | Origin, author, operation, snapshot | Import batch, user, timestamp, hash |
| `lifecycle` | Stage, status, transitions | Concept, design, construction, operation |
| `cost` | Quantities, resources, estimates | Volume, material, cost item |
| `operation` | Maintenance, equipment, repairs | Asset, service history |
| `cad` | Mapping to CAD/BIM platforms | Archicad, Revit, Renga, nanoCAD IDs |

## 6. Inheritance model

IFCA uses inheritance to keep entities lightweight:

```text
1. Entity override
2. Entity type / profile
3. Scope: room → storey → project
4. Snapshot / import batch
5. BRAVIM Planet ruleset
```

Example:

```text
Fire rating
→ entity override, if present
→ otherwise wall type
→ otherwise project profile
→ otherwise applicable ruleset
```

This follows the IFC-inspired distinction between a **type** and an **occurrence**: common information belongs to the type, while the occurrence stores only its unique data and overrides.

## 7. Normative references

IFCA does not claim ownership of legal or normative documents.

Instead, it stores references to official primary sources, for example `publication.pravo.gov.ru`, together with:

- official URL;
- publication identifier;
- publication date;
- accessed-at timestamp;
- content hash;
- specific section or fragment;
- extracted rule and its severity.

Example:

```json
{
  "rule_id": "SP-252_6.14_C001",
  "severity": "required",
  "statement": "Evacuation path width must be at least 1.2 m",
  "evidence": {
    "official_url": "https://publication.pravo.gov.ru/document/0001202610160045",
    "publication_id": "0001202610160045",
    "section": "6.14",
    "accessed_at": "2026-10-18T06:45:00+03:00",
    "content_hash": "sha256:..."
  }
}
```

## 8. Relationship to IFC 4.3 and IFCX

IFCA is designed as a bridge, not a replacement:

```text
BAV Graph
   ↕
IFCA JSON
   ↕
IFC 4.3 adapter
   ↕
Existing BIM tools
```

The first practical target is reliable mapping between IFCA and IFC 4.3. As IFC 5 / IFCX matures, IFCA may evolve toward closer alignment with its final schemas and serialization approach.

## 9. MVP roadmap

```text
1. IFCA JSON Schema v0.1
2. BAV Core: project, site, storey, space, element
3. Type → occurrence inheritance
4. Geometry references
5. Provenance module
6. Normative reference module
7. IFC 4.3 import/export adapter
8. BAV Viewer: graph, 3D, entity card
```

## 10. Status

IFCA is an **experimental alpha proposal**.

It is intended for research, prototyping and community discussion. It is not yet a production interchange standard and should not be treated as a replacement for IFC.

## 11. Invitation

We invite discussion around:

- minimal core entities;
- module boundaries;
- provenance model;
- normative reference model;
- IFC 4.3 mapping;
- future IFCX alignment;
- JSON Schema and validation.

> **IFCA — a prototype interchange format for the Building Avatar.**