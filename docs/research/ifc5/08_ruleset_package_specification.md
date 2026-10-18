# Ruleset Package Specification v0.1

Status: Research specification  
Date: 2026-10-18  
Project: BRAVIM / Building Avatar (BAV)  
Purpose: define the structure of a BRAVIM Planet Ruleset Package and its rules

## 1. Purpose

A **Ruleset Package** is a versioned, verifiable set of normative and analytical criteria published by BRAVIM Planet and consumed by a BAV Local Core.

It answers:

- which requirements apply to a project;
- where each requirement comes from;
- which document edition is applicable;
- what is required, recommended, informational or assumed;
- which package version was used for a validation.

## 2. Architecture

```text
BRAVIM Planet
   ↓ publishes
Ruleset Package
   ↓ downloads and pins
BAV Local Core / Rules Cache
   ↓ applies
BAV Validator
   ↓
Findings / Diagnostic / Treatment
```

## 3. Package structure

```text
RulesetPackage
├── identity
├── publication
├── scope
├── rules
├── evidence
├── dependencies
├── lifecycle
└── audit
```

## 4. Package example

```json
{
  "ruleset_package": {
    "package_id": "RSP-RU-RESIDENTIAL-2026.10",
    "version": "2026.10.1",
    "status": "published",
    "published_at": "2026-10-18T07:20:00+03:00",
    "publisher": {
      "id": "BRAVIM-PLANET",
      "name": "BRAVIM Planet",
      "role": "knowledge_publisher"
    },
    "content_hash": "sha256:...",
    "previous_version": "2026.09.4",
    "supersedes": "RSP-RU-RESIDENTIAL-2026.09",
    "scope": {
      "country": "RU",
      "region": "Moscow",
      "building_type": "residential",
      "construction_type": "new_build",
      "lifecycle_stages": ["concept", "design", "review"],
      "disciplines": ["architecture", "fire", "ventilation", "water"]
    },
    "rules": [],
    "evidence": [],
    "dependencies": {
      "requires": [],
      "conflicts_with": [],
      "replaces": []
    },
    "lifecycle": {
      "applicable_stages": ["concept", "design", "review"],
      "mandatory_from": "design",
      "recheck_on_change": true
    },
    "audit": {
      "created_at": "2026-10-18T07:20:00+03:00",
      "created_by": "BRAVIM-PLANET",
      "change_log": []
    }
  }
}
```

## 5. Rule structure

```text
Rule
├── Identity
├── Statement
├── Severity
├── Category
├── Applicability
├── Check
├── Evidence
├── Relationships
├── Lifecycle
└── Metadata
```

### 5.1 Identity

```json
{
  "rule_id": "SP-252_6.14_C001",
  "version": "1.0.0",
  "status": "published",
  "created_at": "2026-10-18T07:21:00+03:00",
  "updated_at": "2026-10-18T07:21:00+03:00"
}
```

`rule_id` remains stable; wording or logic changes create a new rule version.

### 5.2 Statement

```json
{
  "statement": {
    "text": "Ширина эвакуационного пути должна быть не менее 1,2 м.",
    "language": "ru",
    "formal": "width >= 1.2 m",
    "explanation": "Требование относится к эвакуационным путям."
  }
}
```

### 5.3 Severity

| Severity | Meaning | BAV behaviour |
|---|---|---|
| `required` | Mandatory requirement | Violation becomes a blocker |
| `recommended` | Recommendation | Warning or advice |
| `informational` | Reference information | Context only |
| `assumption` | Assumption | Requires human confirmation |

### 5.4 Category

```json
{
  "category": "fire_safety",
  "subcategory": "evacuation"
}
```

Possible categories include:

```text
fire_safety
evacuation
planning
accessibility
ventilation
water_supply
electrical
structural
energy
operation
```

### 5.5 Applicability

```json
{
  "applicability": {
    "entity_types": ["corridor", "evacuation_path"],
    "building_types": ["residential"],
    "regions": ["RU-Moscow"],
    "lifecycle_stages": ["design", "review"],
    "conditions": {
      "building_height": ">= 28 m",
      "occupancy": "residential"
    }
  }
}
```

Applicability allows Planet to deliver only relevant rules to a project.

### 5.6 Check

```json
{
  "check": {
    "type": "numeric_min",
    "target": "width",
    "unit": "m",
    "threshold": 1.2,
    "scope": "entity",
    "tolerance": 0.001
  }
}
```

Check types:

| Type | Question | Example |
|---|---|---|
| `numeric_min` | Is value at least threshold? | Width ≥ 1.2 m |
| `numeric_max` | Is value at most threshold? | Height ≤ 3.2 m |
| `numeric_range` | Is value within range? | Area 15–40 m² |
| `existence` | Does entity or relation exist? | Evacuation exit exists |
| `classification` | Is classification correct? | Room is a living room |
| `spatial_relation` | Is spatial relation satisfied? | Bathroom is not above living room |
| `graph_query` | Is graph condition satisfied? | Path to exit exists |
| `external_calculation` | Is external calculation needed? | Fire resistance calculation |
| `human_confirmation` | Is human decision needed? | Complex project assumption |

For MVP, use:

```text
numeric_min
numeric_max
existence
classification
```

### 5.7 Evidence

```json
{
  "evidence_ids": ["EV-SP252-6.14"]
}
```

Evidence is stored in the package-level `evidence` array:

```json
{
  "evidence_id": "EV-SP252-6.14",
  "official_url": "https://publication.pravo.gov.ru/document/0001202610160045",
  "publication_id": "0001202610160045",
  "locator": {
    "type": "section",
    "value": "6.14"
  },
  "accessed_at": "2026-10-18T07:21:00+03:00",
  "content_hash": "sha256:...",
  "verification": {
    "status": "verified",
    "verified_by": "BRAVIM-PLANET-REVIEWER",
    "verified_at": "2026-10-18T07:21:00+03:00"
  }
}
```

BRAVIM does not sign official documents. It preserves references to primary sources and records its interpretation context.

### 5.8 Relationships

```json
{
  "relationships": {
    "requires": ["RULE-EXIT-EXISTENCE"],
    "conflicts_with": [],
    "refines": [],
    "replaces": [],
    "related_to": ["RULE-CORRIDOR-WIDTH"]
  }
}
```

### 5.9 Lifecycle

```json
{
  "lifecycle": {
    "applicable_stages": ["design", "review"],
    "mandatory_from": "design",
    "recheck_on_change": true,
    "recheck_triggers": [
      "geometry.changed",
      "classification.changed",
      "space.changed"
    ]
  }
}
```

## 6. Full rule example

```json
{
  "rule_id": "SP-252_6.14_C001",
  "version": "1.0.0",
  "status": "published",
  "statement": {
    "text": "Ширина эвакуационного пути должна быть не менее 1,2 м.",
    "language": "ru",
    "formal": "width >= 1.2 m"
  },
  "severity": "required",
  "category": "fire_safety",
  "subcategory": "evacuation",
  "applicability": {
    "entity_types": ["corridor", "evacuation_path"],
    "building_types": ["residential"],
    "regions": ["RU-Moscow"],
    "lifecycle_stages": ["design", "review"],
    "conditions": {
      "building_height": ">= 28 m"
    }
  },
  "check": {
    "type": "numeric_min",
    "target": "width",
    "unit": "m",
    "threshold": 1.2
  },
  "evidence_ids": ["EV-SP252-6.14"],
  "relationships": {
    "requires": ["RULE-EXIT-EXISTENCE"],
    "conflicts_with": [],
    "related_to": ["RULE-CORRIDOR-WIDTH"]
  },
  "lifecycle": {
    "applicable_stages": ["design", "review"],
    "mandatory_from": "design",
    "recheck_on_change": true
  },
  "tags": ["evacuation", "fire_safety", "corridor"]
}
```

## 7. Package lifecycle

```text
Draft
→ In Review
→ Verified
→ Published
→ Deprecated
→ Superseded
```

| Status | Meaning |
|---|---|
| `draft` | Planet draft |
| `in_review` | Under review |
| `verified` | Verified |
| `published` | Available to clients |
| `deprecated` | Not recommended |
| `superseded` | Replaced by a newer version |

## 8. Versioning rules

```text
1. A package is never changed retroactively.
2. A change creates a new package version.
3. Local Core pins a specific version.
4. A validation result records the used package version.
5. Planet may propose an update, but does not apply it automatically.
```

Example:

```text
RSP-RU-RESIDENTIAL-2026.10.1
   ↓ supersedes
RSP-RU-RESIDENTIAL-2026.09.4
```

## 9. BAV usage flow

```text
1. BAV Local Core sends a project profile.
2. Planet returns applicable Ruleset Packages.
3. Local Core stores them in Rules Cache.
4. Local Core pins version and content_hash.
5. Validator checks BAV against the pinned version.
6. Result contains rule_id, evidence_id and ruleset_version.
7. Planet may propose an update.
8. User accepts, postpones or rejects it.
```

Example finding:

```json
{
  "finding_id": "FND-000123",
  "rule_id": "SP-252_6.14_C001",
  "bav_id": "CORRIDOR-001",
  "result": "violation",
  "expected": ">= 1.2 m",
  "actual": "1.05 m",
  "evidence_id": "EV-SP252-6.14",
  "ruleset_version": "2026.10.1",
  "severity": "required"
}
```

## 10. IFCA integration

In an `.ifca` file, the package is referenced:

```json
{
  "modules": {
    "normative": "RSP-RU-RESIDENTIAL-2026.10.1"
  }
}
```

The full package is stored in the Rules Cache or BRAVIM Planet.

## 11. MVP

```text
1. One Ruleset Package
2. 3–5 rules
3. required and recommended only
4. Evidence with pravo.gov.ru references
5. numeric_min / numeric_max / existence checks
6. Pinned version in Local Core
7. Simple validation result
```

## 12. Main formula

```text
Planet verifies knowledge.
Ruleset Package packages knowledge.
Local Core pins knowledge version.
BAV is checked against that version.
A human makes the decision.
```

> **A rule is not merely a quotation from a regulation.**  
> **A rule is a verifiable statement linked to an official source and executable over BAV.**