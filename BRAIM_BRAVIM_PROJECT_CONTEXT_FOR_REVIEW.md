# BRAVIM / BRAVO — Project Context for External Review

Version: 0.1.0
Date: 2026-10-18
Status: Research concept, open for critique
Purpose: give an external reviewer a complete, code-free understanding of the project

## 1. One-paragraph summary

**BRAVO** is a proposed openBIM-oriented platform in which a building exists as a **Building Avatar (BAV)**: a versioned, verifiable digital entity that can answer questions about itself, be checked against applicable requirements, preserve evidence, propose changes, and keep a human in control of decisions. BRAIM provides the governance layer; BRAVIM/BAV provides the building-avatar layer; IFCA provides an exchange format; BAR and VAR provide registry and versioned representation concepts.

## 2. Problem

Modern BIM workflows suffer from several recurring problems:

- project knowledge is scattered across IFC files, PDFs, spreadsheets, BCF issues, emails and CDE folders;
- normative requirements are often used as text, but not as traceable, versioned, machine-checkable knowledge;
- validation results are frequently disconnected from their sources, applicable editions and project context;
- design decisions and their justifications are hard to reconstruct later;
- AI tools can generate plausible answers, but their provenance, applicability and reliability are unclear;
- teams need collaboration, but also need local control over sensitive project data.

BRAVO aims to address these problems by combining governance, a verifiable building model, source-linked knowledge and human-approved change proposals.

## 3. Product family

| Name | Layer | Purpose |
|---|---|---|
| **BRAIM** | Governance platform | Project information governance: artifact registry, provenance, Quality Gate, snapshots, CDE integration |
| **BRAVIM** | Building Avatar platform | Platform where a building exists as a living, verifiable avatar |
| **BAV** | Building Avatar | The building as a versioned, identifiable, checkable entity |
| **BAR** | Building Avatar Registry | Registry of avatars, versions, evidence, rules and statuses |
| **VAR** | Versioned Avatar Representation | Versioned representation of an avatar for storage, exchange and reproducibility |
| **IFCA** | Exchange format | Transport/exchange format for BAV |
| **BRAVO** | Product suite | Umbrella name for the combined system |

```text
BRAVO = BRAIM (governance)
      + BRAVIM/BAV (building avatar)
      + BAR (registry)
      + VAR (versioned representation)
      + IFCA (exchange)
```

## 4. Core idea

A building is treated not merely as a set of geometric objects, but as an avatar with:

- identity;
- semantic classification;
- geometry and spatial relations;
- properties;
- lifecycle state;
- evidence references;
- applicable rules;
- validation results;
- proposed treatments;
- decision and approval history.

The central formula is:

```text
A rule is not merely a quotation from a regulation.
A rule is a verifiable statement linked to an official source
and executable over BAV.
```

## 5. Architecture

```text
BRAVIM Planet
   | publishes
Ruleset Package
   | downloads and pins
BAV Local Core / Rules Cache
   | applies
BAV Validator
   |
Findings / Diagnostics / Treatment Packages
   |
Human decision
```

### BRAVIM Planet

Planet is the knowledge-publishing side. It:

- curates normative and analytical knowledge;
- links rules to official sources;
- publishes versioned Ruleset Packages;
- proposes updates;
- does not silently change knowledge used by projects.

### BAV Local Core

Local Core is the project-side execution environment. It:

- stores or accesses the project's BAV;
- downloads applicable Ruleset Packages;
- pins package version and content hash;
- runs checks;
- produces findings and diagnostics;
- prepares Treatment Packages;
- keeps the human in control.

### Validator

The validator applies rules to BAV and returns results. A result should contain at least:

- rule ID;
- affected BAV entity;
- expected condition;
- actual condition;
- result;
- evidence ID;
- ruleset version;
- severity.

## 6. BAV: Building Avatar

BAV is not a copy of IFC and not simply a "smart BIM model". It is an information model of a building designed to be queryable, checkable and traceable.

A BAV may include:

- identifiable entities, such as `BAV-*` IDs;
- semantic classifications;
- geometry;
- spatial and topological relations;
- properties and attributes;
- lifecycle states;
- evidence references;
- rule bindings;
- validation history;
- treatment history.

### Design principles

```text
Room != Zone
Opening != Filling
Adjacency != Access
Concept ID != Instance ID
Normative source != AI inference
Project requirement != derived calculation
```

Unknown values remain unknown. Uncertain reasoning is marked as proposed or requiring review.

## 7. Evidence Fragment

An **Evidence Fragment** preserves the connection between a statement, rule or decision and its source.

It may include:

- evidence ID;
- official URL;
- publication ID;
- document title;
- publisher;
- edition;
- locator, such as section or clause;
- access date;
- content hash;
- verification status.

Important boundary:

```text
BRAVO does not sign or replace official normative documents.
It preserves references to primary sources and records interpretation context.
```

## 8. Ruleset Package

A **Ruleset Package** is a versioned, verifiable set of normative and analytical criteria.

It answers:

- which requirements apply;
- where they come from;
- which edition is applicable;
- what is mandatory, recommended, informational or assumed;
- which package version was used for a validation.

A rule includes:

- stable rule ID;
- human-readable statement;
- formal or executable check;
- severity;
- category;
- applicability;
- evidence references;
- relationships to other rules;
- lifecycle and recheck conditions.

Severity model:

| Severity | Meaning |
|---|---|
| `required` | Mandatory requirement; violation may become a blocker |
| `recommended` | Recommendation or good practice |
| `informational` | Context or reference information |
| `assumption` | Assumption requiring human confirmation |

Versioning principle:

```text
A package is never changed retroactively.
A change creates a new package version.
A Local Core pins a specific version.
A validation result records the used version.
Planet may propose an update, but does not apply it automatically.
```

## 9. Treatment Package

A **Treatment Package** is a proposed, reviewable change intended to resolve one or more findings.

It may include:

- goal;
- related diagnosis or finding;
- affected BAV entities;
- proposed operations;
- rules to recheck;
- evidence references;
- impact preview;
- approval status.

A Treatment Package is not applied silently. The intended flow is:

```text
Finding -> Diagnosis -> Treatment proposal -> Human approval -> Controlled application -> Recheck
```

## 10. Governance principles

BRAIM remains the governance foundation:

- immutable or append-oriented artifact registry;
- provenance between artifact, rule, validation, issue and decision;
- Quality Gate decisions;
- sealed snapshots;
- controlled publication;
- separation of working, shared and published states.

Key governance rules:

```text
Do not publish WIP as final.
Do not treat AI output as a normative source.
Do not hide provenance.
Do not apply changes without approval.
Do not lose rejected or superseded knowledge.
```

## 11. Human-in-the-loop

BRAVO is not intended to be an autonomous designer.

The intended autonomy model is:

| Level | Meaning |
|---|---|
| `SUGGEST` | System proposes options; human decides |
| `AUTO_SAFE` | System may perform limited, policy-bounded actions |
| `ESCALATE` | Conflict, risk or ambiguity goes to a human |

An AI agent may participate in an iteration loop only within approved policies: propose variants, check them, avoid worsening results, and escalate conflicts.

## 12. MVP direction

The first practical slice is intentionally narrow:

```text
1. One Ruleset Package
2. A small number of rules
3. required and recommended severities
4. Evidence references to official sources
5. Simple checks: numeric minimum, numeric maximum, existence, classification
6. Local Core version pinning
7. Simple validation result
8. One Treatment Package flow with human approval
```

The goal is not to cover all construction norms at once. The goal is to prove the chain:

```text
Official source -> Evidence -> Rule -> BAV check -> Finding -> Treatment -> Human decision -> Recheck
```

## 13. Explicit non-goals

BRAVO does not aim to:

- replace architects, engineers, experts or responsible decision-makers;
- replace CDE platforms;
- replace design or calculation software;
- replace official normative documents;
- certify compliance;
- automatically publish project information;
- give legal opinions;
- generate unchecked AI conclusions as facts;
- copy full normative texts without source linkage;
- create an opaque black-box AI system.

## 14. Current open questions

1. What is the minimal, stable BAV Core Schema?
2. How should BAR register avatars, versions, evidence and rules?
3. What exactly should VAR contain: full snapshot, delta, manifest, or all three?
4. How should IFCA relate to IFC5 without duplicating its model?
5. How should Planet authenticate published Ruleset Packages?
6. How should Local Core handle conflicting rules from different packages?
7. What is the right granularity of a rule: clause, criterion, check, or diagnostic?
8. How should regional and project-specific requirements be composed?
9. How should calculation results be linked to rules without pretending they are approvals?
10. What is the minimum viable Treatment Package format?
11. How should rejected or superseded knowledge remain visible without polluting active workflows?
12. What governance model is appropriate for community-contributed rules?

## 15. Questions for critics

We specifically welcome critique on:

- Is the separation BRAIM / BRAVIM / BAV / BAR / VAR / IFCA / BRAVO clear or over-engineered?
- Is "Building Avatar" a useful concept, or is it a renaming of a digital twin?
- Is the Ruleset Package model sufficiently precise for real normative knowledge?
- Is the evidence model strong enough for professional and regulatory use?
- Is the human-in-the-loop model credible for real design workflows?
- Is the local-first approach compatible with team collaboration and CDE requirements?
- Is the proposed MVP too narrow, too broad, or correctly scoped?
- What are the biggest risks: regulatory acceptance, data modelling, AI reliability, adoption, or governance?
- What should be removed from the concept to make it simpler?
- What is missing that would prevent a real pilot?

## 16. Main formula

```text
Planet verifies and publishes knowledge.
Ruleset Package packages knowledge.
BAR registers avatars and versions.
VAR preserves representations.
IFCA transports them.
Local Core pins and applies knowledge.
BAV is checked against that knowledge.
A human makes the decision.
BRAVO is the whole system.
```
