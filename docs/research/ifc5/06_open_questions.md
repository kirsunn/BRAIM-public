# IFC 5 → BAV / IFCA Open Questions

Status: Research registry  
Date: 2026-10-18  
Project: BRAVIM / Building Avatar (BAV)  
Purpose: track open questions and research priorities

## 1. Purpose

This document collects questions that must be answered before IFCA can move from a research prototype to a more stable model.

## 2. Open questions

| ID | Area | Question | Priority | Status |
|---|---|---|---|---|
| Q-001 | IFC 5 Core | Which IFC 5 Core entities are stable enough to map to BAV? | High | Open |
| Q-002 | Identity | How should BAV ID coexist with IFC GlobalId? | High | Open |
| Q-003 | Types | How should BAV Type → Occurrence inheritance be implemented? | High | Open |
| Q-004 | Properties | Should BAV reuse IFC property sets or define its own assertion model? | High | Open |
| Q-005 | References | How should external documents, geometry and normative sources be referenced? | High | Open |
| Q-006 | Spatial structure | What is the minimal BAV spatial hierarchy? | High | Open |
| Q-007 | Provenance | How should provenance assertions be structured without overloading entities? | Medium | Open |
| Q-008 | Lifecycle | How should hierarchical lifecycle states be inherited? | Medium | Open |
| Q-009 | Normative data | How should rules link to official publications such as pravo.gov.ru? | High | Open |
| Q-010 | IFC 4.3 | What is the minimal IFC 4.3 ↔ IFCA mapping? | High | Open |
| Q-011 | IFCX | When should IFCA align with IFCX serialization? | Medium | Deferred |
| Q-012 | Viewer | What minimum data does BAV Viewer need? | Medium | Open |
| Q-013 | IFCA schema | What should IFCA JSON Schema v0.1 contain? | High | Open |
| Q-014 | CAD connectors | How should CAD mappings be stored for Archicad, Revit, Renga and nanoCAD? | Medium | Open |
| Q-015 | Planet | How should Ruleset Packages be versioned and pinned? | High | Open |

## 3. Priority order

```text
1. IFC 5 Core and stable entities
2. BAV Core and identity
3. Minimal spatial hierarchy
4. IFCA JSON Schema v0.1
5. IFC 4.3 mapping
6. Normative references and evidence
7. Provenance and lifecycle
8. Viewer and CAD connectors
```

## 4. Status labels

| Status | Meaning |
|---|---|
| Open | Needs research |
| In progress | Being analysed |
| Decided | Decision recorded |
| Deferred | Postponed |
| Closed | No longer relevant |

## 5. Rule

Every answered question should create or update:

```text
- a decision in 05_ifca_prototype_decisions.md
- a mapping entry in 04_ifc5_to_bav_mapping.md
- a source reference in 00_sources.md
```