# BRAIM Concept v1.0

**Статус:** Draft / концептуальная спецификация  
**Дата:** 2026-10-04  
**Версия:** 1.0.0  
**Регион пилота:** Республика Татарстан, Россия

Этот документ формализует концепцию BRAIM на основе `BRAIM_Master_Context_1.0`, `BRAIM_full_context-3.md` и `BRAIM_Handover_Package_v1.0`. [file:103][file:104][github_mcp_direct:1]

---

## 1. Vision & Product Definition

### 1.1. Vision

Создать openBIM-oriented orchestration and information-governance layer, который автоматизирует проверку конкретных, явно определённых, версионированных и машиночитаемых правил в федеративных BIM/CDE-процессах. [file:103]

### 1.2. Product Definition

**BRAIM (Building Information Atomic Model)** — оркестратор и governance-слой для федеративных BIM/CDE-workflow.

BRAIM:

- регистрирует неизменяемые IFC/IDS/BCF/отчётные артефакты;
- запускает versioned machine-checkable policy packs;
- объединяет результаты information, geometry, topology, process и domain checks;
- принимает и сохраняет решения Quality Gate;
- создаёт immutable iteration snapshots;
- обеспечивает provenance между артефактом, правилом, валидацией, BCF issue и выпуском;
- подключается к CDE, authoring и viewer системам через capability-driven adapters. [file:103]

**BRAIM не является:**

- системой авторинга (не редактирует геометрию как основную функцию);
- полноценной заменой CDE;
- автоматическим сертификатором соответствия всем ГОСТ/СП;
- универсальным IFC merge engine;
- production implementation IFC5 на текущем этапе. [file:103]

> Корректная формулировка: BRAIM автоматизирует проверку конкретных, явно определённых, версионированных и машиночитаемых правил. Его результаты являются доказательной основой для назначенных проектных ролей, но не автоматическим подтверждением полного нормативного соответствия, безопасности объекта или прохождения экспертизы. [file:103]

---

## 2. Key Decisions (Пилот)

| ID | Решение | Смысл | Статус |
|---|---|---|---|
| D-01 | CDE-master | CDE заказчика — контрактный master; BRAIM — immutable mirror + provenance | Подтверждено [file:103] |
| D-02 | Git scope | Git — только код, схемы, policy packs, mappings, ADR, snapshots, Golden Corpus; IFC production — в CDE/object storage | Подтверждено [file:103] |
| D-03 | Strict Quality Gate | Critical/Blocking→No-Go; Major→Hold; Minor→Go with findings | Подтверждено [file:103] |
| D-04 | KPI | Только R&D targets; метрики проверяются benchmark protocol | Подтверждено [file:103] |
| D-05 | Pilot strategy | Один глубокий пилот с реальным объектом, CDE boundary, evidence chain | Подтверждено [file:103] |
| D-06 | Neo4j | Neo4j Community для MVP/Phase 1–2; Enterprise — после review | Подтверждено [file:103] |

---

## 3. Architecture Overview

### 3.1. Control Plane / Data Plane

```
                          BRAIM Control Plane
    snapshot registry · policy engine · quality gate · decisions · audit
                                  │
        ┌─────────────────────────┼──────────────────────────┐
        │                         │                          │
 Artifact plane             Processing plane          Integration plane
 CDE + object storage       IFC/IDS/topology workers  CDE/BCF/UI/authoring adapters
 hashes/retention           graph projection           capability manifests
                                  │
                            BuildBus
                    commands · events · artifact refs
```

Control plane: snapshot registry, policy engine, quality gate, decisions, audit. Data plane: artifact storage (CDE + object storage), processing workers (IFC/IDS/topology), integration adapters (CDE/BCF/UI). Связь через BuildBus. [file:103]

### 3.2. BuildBus

- **Command:** request to a concrete owner.
- **Event:** fact that occurred.
- **Query:** synchronous API read, not a bus event.
- **Artifact ref:** ID/URI/hash; no IFC/BCF binary payload in messages.
- **Delivery:** at-least-once.
- **Consumers:** idempotent.
- **Registry + event publication:** transactional outbox.
- **Failure:** retry/backoff → DLQ → reconciliation. [file:103]

---

## 4. IFC & Standards Policy

### 4.1. IFC5-First Policy

BRAIM должен быть **IFC5-ready, но не IFC5-dependent**.

- **Production scope:** IFC2x3, IFC4, IFC4x3 — только в реально протестированном объёме.
- **IFC5:** R&D/adapter sandbox до утверждённой версии стандарта, зрелого toolchain и подтверждённой совместимости. [file:103]

### 4.2. Supported Standards

| Стандарт | Версия | Статус |
|---|---|---|
| IFC | 2x3, 4, 4x3 | Production (tested scope) [file:103] |
| IFC | 5 alpha | R&D sandbox only [file:103] |
| IDS | 1.0 | Production [file:103] |
| BCF | 3.0 | Production [file:103] |
| ISO 19650 | 2018 (1, 2, 5) | Действует [file:104] |
| ГОСТ Р 58439.1 | 2019 | Действует [file:104] |

---

## 5. Source of Truth & Storage

### 5.1. CDE-Master Decision

На первом пилоте CDE заказчика — контрактный/операционный master для информационных контейнеров и их статусов. BRAIM создаёт immutable mirror или registered reference к каждой версии. [file:103]

### 5.2. Authoritative Data Matrix

| Data type | Authoritative system | BRAIM role |
|---|---|---|
| IFC/IDS/BCF/reports artefact | CDE master + immutable mirror | Register, hash, validate [file:103] |
| CDE container state | Customer CDE | Mirror/enforce workflow [file:103] |
| Snapshots, gates, decisions | BRAIM registry | Authoritative workflow state [file:103] |
| Code, schemas, policies | Git | Authoritative versioned spec [file:103] |
| IFC graph | Neo4j Community | Rebuildable projection [file:103] |

**Hard rule:** Neo4j is never the sole source of truth. [file:103]

---

## 6. Validation Architecture

### 6.1. Layers

| Layer | Purpose | Output |
|---|---|---|
| Integrity | file/hash/schema/units/GUID/relations | Blocking findings [file:103] |
| Information | IDS entity/attribute/property/classification | IDS result + BCF [file:103] |
| Geometry | clashes, dimensions, clearances | Geometry report + BCF [file:103] |
| Topology | containment, cycles, connectivity | Topology report + BCF [file:103] |
| Process | roles, evidence, policy version | Gate evidence [file:103] |
| Domain rules | SP/GOST/project rules | Policy-specific evidence [file:103] |

### 6.2. Quality Gate (Strict Decision Policy)

```
Blocking / Critical → NO_GO
Major               → HOLD
Minor               → GO_WITH_FINDINGS
Information         → GO_WITH_INFO
Missing mandatory validator/evidence → NO_GO
```

`GO_WITH_FINDINGS` рендерится как `go` плюс findings. [file:103]

---

## 7. Snapshot & Provenance

### 7.1. Snapshot Structure

```json
{
  "snapshot_id": "snp_01J...",
  "iteration_code": "IT004",
  "snapshot_schema_version": "1.0.0",
  "state": "sealed",
  "content_digest": "sha256:...",
  "project_id": "prj_01J...",
  "parent_snapshot_ids": ["snp_01J..."],
  "artifact_refs": [],
  "policy_refs": [],
  "validation_run_refs": [],
  "decision_refs": [],
  "quality_gate_ref": "qg_01J...",
  "provenance": {
    "source_schema": "IFC4X3_ADD2",
    "adapter_version": "...",
    "mapping_profile_digest": "sha256:..."
  },
  "signatures": []
}
```

### 7.2. Sealing Protocol

1. Create candidate manifest.
2. Validate schema and business invariants.
3. Verify artefact existence and SHA-256.
4. Verify mandatory validations and policy evidence.
5. Calculate canonical content digest.
6. In one registry transaction set snapshot to `sealed` and insert outbox event.
7. Publish event.
8. Any change creates a new snapshot with parent link. [file:103]

---

## 8. EIM Maturity Profile

### 8.1. Structure: G-I-C-A

```
G-I-C-A

G — Geometry level (G0–G5)
I — Information level (I0–I5)
C — Conformance level (C000–C222)
A — Accuracy/Maturity aggregate (A0–A5)
```

Полная форма: `G2-I1-C111-A2[3423;3;343]`, где:

- `3423` — GM (Size, Form, Location, Orientation);
- `3` — TOL (tolerance level);
- `343` — REL (Geometric, Logical, Informational relationships). [file:105]

### 8.2. Aggregate Calculation

```
GM = min(R,F,L,O)
REL = min(G,L,I)
A = min(GM,TOL,REL)
```

Требуемый и фактический профили хранятся отдельно. [file:105]

---

## 9. Roadmap & Milestones

### 9.1. Phases

| Фаза | Название | Длительность | Результат |
|---|---|---|---|
| 0 | Фундамент | 4–6 нед. | Naming, Snapshot Schema, BRAIM-LIMS 0.1, Golden Corpus | [file:103][file:104] |
| 1 | Транспорт | 6–8 нед. | IFC→Neo4j, provenance, vertical slice | [file:103] |
| 2 | Валидация | 8–10 нед. | IDS, topology validator, BCF reports | [file:103] |
| 3 | Оркестратор | 8–12 нед. | Quality Gate, BuildBus, snapshot manager | [file:103] |
| 4 | UI | 6–8 нед. | Viewer, dashboard, evidence timeline | [file:103] |

### 9.2. Milestones

| Веха | Что | Когда |
|---|---|---|
| M0 | Регистрация ООО + статус МТК | окт–нояб 2026 [file:104] |
| M1 | Заявка Старт-ЦТ-1 (до 5 млн ₽) | ноябрь 2026 [file:104] |
| M3 | Прототип: IFC→Neo4j→IfcTester→BCF→Quality Gate | сентябрь 2027 [file:104] |
| M5 | Заявка Развитие-ЦТ (до 20 млн ₽) | ноябрь 2027 [file:104] |
| M6 | Build UP / РФРИТ (пилот) | весна 2028 [file:104] |

---

## 10. Risks & Controls

| Risk ID | Risk | Control |
|---|---|---|
| R-01 | IFC5 immaturity | Sandbox adapter only; no production dependency [file:103] |
| R-02 | CDE API mismatch | Capability manifest + BCF/file fallback [file:103] |
| R-03 | Experimental merge | Report-only diff; manual resolution; Golden Corpus [file:103] |
| R-05 | False normative claim | Versioned scope/expert-owned policy pack [file:103] |
| R-09 | Security/data leakage | Threat model, RBAC, storage/bus controls, audit [file:103] |
| R-11 | KPI overclaim | R&D target label + benchmark protocol [file:103] |

---

## 11. Mandatory ADRs

1. Source of truth and CDE-master first pilot.
2. Git scope and artifact storage policy.
3. Snapshot identity, sealing and provenance rules.
4. BuildBus delivery/idempotency/outbox/DLQ/reconciliation.
5. IFC-to-CBIM and CBIM-to-graph mapping profile.
6. Neo4j projection and snapshot-qualified identity model.
7. Quality Gate strict policy and waiver rules.
8. CDE adapter ownership and capabilities.
9. IFC5 sandbox / production exclusion policy.
10. Topology policy and allowed roots/exceptions.
11. SP/GOST policy governance and expert ownership.
12. Security threat model and data classification.
13. Toolchain version/pinning/licence/SBOM.
14. Benchmark protocol and KPI publication rule. [file:103]

---

## 12. Next Actions

1. **Phase 0 — Architecture freeze and evidence (4–6 недель):**
   - Recover/approve this master context and ADRs.
   - Publish schemas: artifact, snapshot, decision, event, validation result, policy manifest.
   - Publish BRAIM-LIMS 0.1 as configurable project policy.
   - Create standards/claims/grants registers.
   - Establish Golden Corpus, benchmark protocol and CI baseline.
   - Pin toolchain/image digests and create licence SBOM.
   - Select first-pilot CDE and complete capability discovery. [file:103]

2. **Phase 1 — Evidence-driven vertical slice (6–8 недель):**
   - CDE artifact registration → hash + immutable mirror/reference.
   - IFC integrity inspection.
   - IDS validation.
   - BCF findings.
   - Strict Quality Gate.
   - Sealed snapshot.
   - Provenance query. [file:103]

---

*Версия: 1.0.0 | Дата: 2026-10-04 | Регион пилота: Республика Татарстан, Россия*
