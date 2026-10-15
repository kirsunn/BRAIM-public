# BRAIM — Master Context 1.0

**Статус:** единый рабочий архитектурный baseline  
**Дата фиксации:** 30 сентября 2026  
**Регион пилота:** Республика Татарстан, Россия  
**Основание:** объединение `BRAIM_full_context.md`, `BRAIM_full_context_updated-1.md`, `Text-Document.txt` и принятых решений пользователя от 30.09.2026.

---

## 0. Зафиксированные решения

Пользователь подтвердил следующие решения:

| ID | Решение | Принято |
|---|---|---|
| D-01 | Source of IFC on first pilot | **CDE-master**: CDE заказчика — контрактный master; BRAIM хранит/ведёт immutable mirror и provenance |
| D-02 | Git scope | **Git только для кода, schemas, policy packs, mappings, ADR, snapshot manifests и Golden Corpus; IFC production artefacts — в CDE/object storage** |
| D-03 | First-pilot Quality Gate | **Строгий режим с первого дня:** Critical/Blocking → No-Go; Major → Hold; Minor → Go with findings |
| D-04 | KPI | **Только R&D targets:** метрики проверяются benchmark protocol, не объявляются подтверждёнными эффектами до пилота |
| D-05 | Pilot strategy | **Один глубокий пилот** с реальным объектом, CDE boundary, evidence chain и измеримым эффектом |
| D-06 | Neo4j | **Neo4j Community для MVP / Phase 1–2**, Enterprise/managed только после нагрузочного, security и licensing review |

---

## 1. Product definition

**BRAIM (Building Information Atomic Model)** — openBIM-oriented orchestration and information-governance layer for federated BIM/CDE workflows.

BRAIM:

- регистрирует неизменяемые IFC/IDS/BCF/отчётные артефакты;
- запускает versioned machine-checkable policy packs;
- объединяет результаты information, geometry, topology, process и формализованных domain checks;
- принимает и сохраняет решения Quality Gate;
- создаёт immutable iteration snapshots;
- обеспечивает provenance между артефактом, версией правила, запуском валидатора, BCF issue, проектным решением и выпуском;
- подключается к CDE, authoring и viewer системам через capability-driven adapters.

BRAIM не является:

- системой авторинга и не редактирует геометрию как основную функцию;
- полноценной заменой CDE;
- автоматическим сертификатором соответствия всем ГОСТ/СП;
- универсальным IFC merge engine;
- production implementation IFC5 на текущем этапе.

Корректная формулировка продукта:

> BRAIM автоматизирует проверку конкретных, явно определённых, версионированных и машиночитаемых правил. Его результаты являются доказательной основой для назначенных проектных ролей, но не автоматическим подтверждением полного нормативного соответствия, безопасности объекта или прохождения экспертизы.

---

## 2. IFC5-first policy

### 2.1. Принцип

BRAIM должен быть **IFC5-ready, но не IFC5-dependent**.

Production scope сейчас: IFC2x3, IFC4 и IFC4x3 — только в реально протестированном объёме. IFC5 рассматривается как R&D/adapter sandbox до появления утверждённой версии стандарта, зрелого toolchain и подтверждённой совместимости.

### 2.2. Canonical Building Information Model

```text
IFC-SPF / IFCXML / future IFC5 JSON/API
            ↓
      Ingestion adapters
            ↓
CBIM: narrow canonical internal model
            ↓
Snapshots · Policies · Graph projection · Validators · CDE adapters · UI
```

Для каждого импорта обязательны:

```text
source_schema
source_serialization
source_artifact_sha256
adapter_version
mapping_profile_digest
loss_report
imported_at
```

Оригинальный IFC-артефакт никогда не заменяется конвертированным silently.

### 2.3. Запрещённые обещания

- «IFC5 уже production-ready».
- «IFC5 решает version control/merge автоматически».
- «IFC5 JSON отменяет semantic mapping».
- «IFC5 заменяет IFC4x3 в текущей поставке».

---

## 3. Source of truth and pilot storage

### 3.1. CDE-master decision

На первом пилоте CDE заказчика является контрактным/операционным master для информационных контейнеров и их статусов. BRAIM не заменяет его, а создаёт immutable mirror либо immutable registered reference к каждой обрабатываемой версии.

```text
Customer CDE (master)
  ├─ container / revision / suitability status
  └─ IFC/BCF/IDS artefact version
             ↓
BRAIM Artifact Registry
  ├─ artifact_id
  ├─ SHA-256
  ├─ immutable mirror or verified URI
  ├─ CDE version reference
  └─ provenance / validation / snapshot links
```

### 3.2. Authoritative data matrix

| Data type | Authoritative system | BRAIM role | Projection/cache |
|---|---|---|---|
| IFC/IDS/BCF/reports artefact version | CDE customer master and/or immutable mirror | register, hash, retain reference, validate | viewer cache, Neo4j graph |
| CDE container suitability/state | Customer CDE | mirror and enforce workflow where adapter allows | registry cache |
| Snapshots, gates, decisions, links | BRAIM transactional registry | authoritative workflow state | UI/API |
| Code, schemas, policies, mappings, ADR | Git | authoritative versioned specification | deployment cache |
| IFC graph | Neo4j Community | rebuildable analysis/read model | Cypher/reporting |

**Hard rule:** Neo4j is never the sole source of truth.

### 3.3. Object storage

BRAIM may use S3-compatible storage/MinIO to hold immutable mirror artefacts, reports and snapshots. It requires explicit versioning, retention/object-lock where required, tenant/project access policies, hashes, backup/restore test and audit trail. An S3 API alone does not guarantee immutability.

---

## 4. Git policy and version model

### 4.1. Git scope

Git stores:

```text
source code
JSON Schemas
policy packs
IDS profiles
mapping profiles
ADR
snapshot manifests
BCF templates / structured reports where appropriate
Golden Corpus and expected results
CI configuration
```

Git does not store production IFC artefacts as the default. Git LFS is permitted only for R&D/sandbox and Golden Corpus fixtures.

### 4.2. Identity model

File name is a human-readable alias, never the only key.

| ID | Purpose |
|---|---|
| `project_id` | global project identity |
| `container_id` | logical CDE information container |
| `artifact_id` | immutable IFC/IDS/BCF/report instance |
| `artifact_sha256` | content integrity |
| `snapshot_id` | immutable BRAIM snapshot global ID |
| `iteration_code` | human alias, e.g. `IT004` |
| `release_id` | logical release |
| `revision_code` | client/CDE-required revision code |
| `variant_id` | alternative design/decision branch |
| `validation_run_id` | one validation execution |
| `quality_gate_id` | one gate decision |
| `policy_pack_digest` | exact rules used |
| `correlation_id` | end-to-end operation ID |

### 4.3. Versioning rule

BRAIM snapshot, external release/revision and CDE state are separate concepts:

```text
BRAIM snapshot      = immutable technical/audit checkpoint
CDE release/revision = contractual issue/version convention
CDE state            = workflow/suitability state
```

BRAIM-LIMS is a configurable project policy. The customer EIR/BEP/contract naming convention has priority. Default policy keeps mutable CDE status in metadata to avoid broken links, but it can include status in a filename if contractually required.

---

## 5. Architecture and BuildBus

### 5.1. Control plane / data plane

```text
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

### 5.2. BuildBus requirements

- Command: request to a concrete owner.
- Event: fact that occurred.
- Query: synchronous API read, not a bus event.
- Artifact ref: ID/URI/hash; no IFC/BCF binary payload inside messages.
- Delivery: at-least-once.
- Consumers: idempotent.
- Registry + event publication: transactional outbox.
- Failure: retry/backoff → DLQ → reconciliation.
- Contracts: schema-versioned; breaking change means new event version.
- Security: no secrets or unnecessary model data in bus payload.

### 5.3. Event envelope

```json
{
  "id": "evt_01J...",
  "type": "org.braim.validation.completed.v1",
  "source": "braim://validator/ids",
  "subject": "project/prj_.../snapshot/snp_...",
  "time": "2026-09-30T18:00:00Z",
  "correlation_id": "cor_01J...",
  "causation_id": "evt_01J...",
  "tenant_id": "ten_01J...",
  "project_id": "prj_01J...",
  "actor": {"type": "service", "id": "svc-ids-validator"},
  "data": {
    "validation_run_id": "val_01J...",
    "artifact_ref": {"artifact_id": "art_01J...", "sha256": "sha256:..."}
  }
}
```

### 5.4. Minimum command/event catalog

```text
braim.command.artifact.register.v1
braim.command.graph.ingest.v1
braim.command.validation.request.v1
braim.command.quality-gate.evaluate.v1
braim.command.snapshot.seal.v1
braim.command.cde.transition-state.v1
braim.command.issue.sync.v1

braim.event.artifact.registered.v1
braim.event.graph.ingested.v1
braim.event.validation.started.v1
braim.event.validation.completed.v1
braim.event.quality-gate.decided.v1
braim.event.snapshot.sealed.v1
braim.event.cde.status-changed.v1
braim.event.issue.created.v1
braim.event.issue.updated.v1
braim.event.merge.assessment.completed.v1
```

---

## 6. Recovered architectural gaps 1–3

### D-01. Deterministic IFC → Graph mapping

**Problem statement:** create a deterministic, idempotent mapping from tested IFC schemas to a labelled property-graph projection. Preserve source identity, provenance, snapshot separation, mapping profile and evidence of coverage.

#### D-01 design rules

1. Source identity is not just `GlobalId`.
2. Each graph entity key is snapshot-qualified:

```text
entity_snapshot_key = sha256(snapshot_id + ":" + ifc_global_id + ":" + source_step_id)
```

3. Original `ifc_global_id` is immutable and never modified with a suffix.
4. A duplicate IFC GlobalId is an integrity finding; it is not silently repaired.
5. Mapping profile is versioned and hashed.
6. Neo4j stores a rebuildable projection from immutable artefact plus mapping profile.
7. APOC/GDS are optional optimizations, not mandatory dependencies.

#### D-01 graph model

```text
(:ModelVersion {artifact_id, snapshot_id, sha256, schema, mapping_profile_digest})
(:IfcEntity {entity_snapshot_key, snapshot_id, ifc_global_id, step_id, ifc_class, name})
(:PsetInstance {snapshot_id, owner_key, name, source_step_id})
(:Property {name, value, value_type, unit})
(:Material {snapshot_id, source_step_id, name})
(:ClassRef {snapshot_id, system, edition, identification, source_step_id})
(:SpaceBoundary {snapshot_id, source_step_id, physical_or_virtual, internal_or_external})

(:ModelVersion)-[:CONTAINS]->(:IfcEntity)
(:IfcEntity)-[:AGGREGATES]->(:IfcEntity)
(:IfcEntity)-[:CONTAINS]->(:IfcEntity)
(:IfcEntity)-[:NESTS]->(:IfcEntity)
(:IfcEntity)-[:TYPED_BY]->(:IfcEntity)
(:IfcEntity)-[:HAS_PSET]->(:PsetInstance)-[:HAS_PROPERTY]->(:Property)
(:IfcEntity)-[:HAS_MATERIAL]->(:Material)
(:IfcEntity)-[:CLASSIFIED_AS]->(:ClassRef)
(:IfcEntity)-[:CONNECTS]->(:IfcEntity)
(:IfcEntity)-[:HAS_BOUNDARY]->(:SpaceBoundary)-[:RELATES_TO]->(:IfcEntity)
(:IfcEntity)-[:VOIDED_BY]->(:IfcEntity)-[:FILLED_BY]->(:IfcEntity)
```

Fast indexed Pset properties may be materialized on `IfcEntity` for declared frequent queries. They do not replace normalized Pset instances.

#### D-01 supported mapping minimum

| IFC relationship | BRAIM edge | Direction |
|---|---|---|
| `IfcRelAggregates` | `AGGREGATES` | parent → child |
| `IfcRelNests` | `NESTS` | parent → child |
| `IfcRelContainedInSpatialStructure` | `CONTAINS` | spatial container → element |
| `IfcRelDefinesByType` | `TYPED_BY` | element → type |
| `IfcRelAssociatesMaterial` | `HAS_MATERIAL` | element → material |
| `IfcRelAssociatesClassification` | `CLASSIFIED_AS` | element → class reference |
| `IfcRelConnectsElements` | `CONNECTS` | relating → related |
| `IfcRelSpaceBoundary` | boundary subgraph | space → boundary → related element |
| `IfcRelVoidsElement` | `VOIDED_BY` | building element → opening |
| `IfcRelFillsElement` | `FILLED_BY` | opening → filling element |

#### D-01 acceptance criteria (R&D target)

- zero loss of original mandatory GlobalIds in supported entity scope;
- all duplicates reported as integrity errors;
- mapping idempotency: same artifact + same profile produces same graph fingerprint;
- coverage report explicitly lists unsupported entities/relations;
- performance target: 10,000 entities within 60 seconds on fixed benchmark hardware; not a product guarantee until measured.

### D-02. IDS / BCF Quality Gate

**Problem statement:** given an immutable IFC artefact or Git manifest reference, execute a versioned IDS policy, generate machine-readable evidence and BCF issues, then make a strict Quality Gate decision.

#### D-02 workflow

```text
Artifact registered
→ validate IFC integrity/schema
→ resolve exact IDS/policy pack digest
→ validate through IfcTester in pinned container
→ JSON report + BCF topics with stable fingerprint
→ Quality Gate aggregation
→ strict decision
→ sealed snapshot evidence
```

#### D-02 strict decision policy (confirmed)

```text
Blocking / Critical → NO_GO
Major               → HOLD
Minor               → GO_WITH_FINDINGS
Information         → GO_WITH_INFO
Missing mandatory validator/evidence → NO_GO
```

`GO_WITH_FINDINGS` is rendered as `go` plus findings in existing simple schema, or as an explicit outcome in the next schema version.

#### D-02 evidence key

```text
artifact_sha256 + policy_pack_digest + validator_image_digest + mapping_profile_digest
```

Cache is valid only for this complete key. Cache storage is registry/object storage; Neo4j may index it but is not the authoritative cache record.

#### D-02 BCF rule

Each issue includes at minimum:

```text
issue_id
fingerprint
rule_id
policy digest
severity
artifact_id / artifact_sha256
snapshot_id / validation_run_id
affected IFC GUID(s)
BCF external topic ID
first_seen / last_seen / status
```

### D-03. Topology validation

**Problem statement:** detect structural anomalies in the explicitly defined hierarchy subgraph, without treating all IFC relations as acyclic and without assuming every element belongs to a building storey.

#### D-03 hierarchy set

```text
H = {AGGREGATES, NESTS, CONTAINS}
```

Cycles in `CONNECTS`, `BOUNDED_BY` and other non-hierarchical relations are not errors by default.

#### D-03 algorithms

| Check | Baseline method | Optional accelerator |
|---|---|---|
| Self-loop / two-node cycle | parameterized bounded Cypher | none required |
| Arbitrary hierarchy cycle | Python Tarjan SCC, O(V+E) | Neo4j GDS if qualified |
| Orphan/isolated entity | parameterized Cypher and Python confirmation | none required |
| Reachability | Python BFS from policy-defined roots | Neo4j projection/query |
| Multiple containment | graph query + policy exceptions | none required |
| High-degree review | report hubs; avoid unbounded Cypher recursion | GDS optional |

#### D-03 initial rules

| Rule ID | Finding | Default outcome |
|---|---|---|
| `TOPOLOGY.HIERARCHY.CYCLE` | cycle inside H | No-Go |
| `TOPOLOGY.SPATIAL.NO_PARENT` | no allowed hierarchy parent | Hold |
| `TOPOLOGY.SPATIAL.UNREACHABLE` | no path from allowed root | Hold |
| `TOPOLOGY.SPATIAL.MULTI_PARENT` | multiple invalid spatial parents | Hold |
| `TOPOLOGY.GRAPH.MISSING_REFERENCE` | relationship references absent entity | No-Go |
| `TOPOLOGY.HIGH_DEGREE.REVIEW` | hub node over policy threshold | Info/Review |

Allowed roots and exclusions are policy-defined. They may include `IfcProject`, `IfcSite`, `IfcBuilding`, `IfcBuildingStorey`, `IfcFacility`, `IfcFacilityPart` or project-specific classes. Default maximum traversal depth is configurable, not hardcoded to 5.

---

## 7. Validation architecture

### 7.1. Layers

| Layer | Purpose | Output |
|---|---|---|
| Integrity | file/hash/schema/units/GUID/required relations | blocking findings |
| Information | IDS entity/attribute/property/classification/material/part-of as supported | IDS result + BCF |
| Geometry | defined clashes, dimensions, clearances with explicit tolerance | geometry report + BCF |
| Topology | containment, cycles, connectivity, boundaries | topology report + BCF |
| Process | required roles, evidence, policy version, status workflow | gate evidence |
| Domain rules | selected SP/GOST/project rules | policy-specific evidence |

### 7.2. SP/GOST rule-as-code

Every executable rule must include:

```yaml
rule_id: "SP50.13330.2024.P5.R_VALUE"
norm_source: "СП 50.13330.2024"
source_edition: "2024"
source_clause: "verified project reference"
applicability: "explicit building/type/climate scope"
input_mapping: "IFC / calculation artefact properties"
tolerance: "explicit value and unit"
severity: "CRITICAL"
responsible_expert_role: "thermal engineer"
policy_version: "1.0.0"
test_cases: "golden corpus references"
```

### 7.3. Thermal protection: SP 50.13330.2024

Use current `СП 50.13330.2024`, not the superseded 2012 edition.

Core check:

\[
R_{0,actual} \ge R_{0,required}
\]

Heating degree days:

\[
ГСОП = (t_{in} - t_{heating}) \times z_{heating}
\]

The thermal policy pack must preserve locality, climate-source edition/table row, threshold, indoor temperature, outdoor heating-period mean, duration, calculated ГСОП, building category/use, humidity regime, approved `R_required` values, calculation artefact and responsible specialist.

MVP validates approved declared/calculated R or U. It does not claim full calculation of thermal bridges, temperature fields, moisture regime or entire SP compliance.

---

## 8. Snapshot and provenance

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

Snapshot sealing protocol:

1. Create candidate manifest.
2. Validate schema and business invariants.
3. Verify artefact existence and SHA-256.
4. Verify mandatory validations and policy evidence.
5. Calculate canonical content digest.
6. In one registry transaction set snapshot to `sealed` and insert outbox event.
7. Publish event.
8. Any change creates a new snapshot with parent link.

Technical signatures/hashes only prove technical integrity when key custody, canonicalization, rotation, revocation and audit procedures exist. They do not replace legally significant e-signatures when required.

---

## 9. CDE adapters and BCF

CDE adapters are capability-driven. No CDE is considered compatible because it nominally supports a standard; compatibility is proven per vendor, version and deployment.

```json
{
  "adapter_id": "cde.vendor-x.v1",
  "capabilities": {
    "webhooks": false,
    "polling": true,
    "bcf_api": true,
    "bcf_zip": true,
    "metadata_read": true,
    "metadata_write": false,
    "state_transition": false,
    "version_history": true,
    "open_cde_documents": false
  },
  "ownership": {
    "container_state": "cde",
    "issue_system_of_record": "braim"
  }
}
```

Fallback order:

```text
Native API/webhook → polling → BCF API → BCFzip → controlled file/metadata exchange
```

---

## 10. Security baseline

- Threat model and information classification before onboarding real pilot data.
- OIDC for human users; scoped service identities for workers.
- TLS everywhere; mTLS based on the threat model.
- RBAC with project scope; separation of duties for waivers and releases.
- Parameterized Cypher only; no dynamic interpolation of user/model data.
- Escape/sanitize IFC/BCF text before HTML/UI rendering; treat IFC attributes as untrusted input.
- Do not put IFC contents, secrets, bearer tokens or unnecessary PII into event payloads.
- Object storage policies, retention, versioning, backup/restore drills.
- SBOM, pinned container digests and dependency scanning before pilot/on-prem delivery.
- Audit log: actor, action, target, before/after, time, correlation ID.

---

## 11. Quality and benchmark policy

All performance/accuracy figures are R&D targets until demonstrated through a published benchmark protocol and Golden Corpus result.

| Target | Status | Evidence required |
|---|---|---|
| 10,000 entities mapping ≤60s | R&D target | fixed hardware, fixed corpus, mapping profile, repeat runs |
| IDS validation ≤30s | R&D target | fixed model/IDS, container digest, warm/cold measurements |
| Topology validation ≤45s | R&D target | graph size, algorithm, hardware, repeat runs |
| ≥98% topology precision, ≤2% FP | R&D target | independently labelled anomaly corpus |
| Reduced manual review time | pilot hypothesis | before/after process measurement |
| 500× improvement / defect-rate claims | prohibited until pilot evidence | signed pilot results and methodology |

---

## 12. Golden Corpus and compatibility matrix

```text
golden-corpus/
├── ifc2x3/
├── ifc4/
├── ifc4x3/
├── ifc5-alpha-sandbox/
├── invalid/
├── ids/
├── bcf/
├── topology/
├── diff/
├── thermal/
├── cde-fixtures/
└── expected/
```

Each case includes input SHA, policy digest, adapter/container version, expected JSON/BCF and acceptance result.

| Capability | IFC2x3 | IFC4 | IFC4x3 | IFC5 alpha | Commitment |
|---|---|---|---|---|---|
| Parse | test required | test required | test required | sandbox only | only qualified schemas |
| IDS | test required | test required | test required | sandbox only | selected profiles |
| Graph projection | test required | test required | test required | sandbox only | selected mapping profile |
| Geometry | selected scope | selected scope | selected scope | no commitment | per profile/tool |
| Round-trip | per tool/version | per tool/version | per tool/version | no commitment | never universal |
| IFC5 import | no | no | no | R&D adapter | no production commitment |

---

## 13. Technology stack

| Layer | Selected baseline | Status / restriction |
|---|---|---|
| Formats | IFC2x3/IFC4/IFC4x3, IDS 1.0, BCF 3.0 | exact scope tested; IFC5 sandbox only |
| Artifact storage | customer CDE master + immutable mirror/reference | first-pilot decision confirmed |
| Registry | PostgreSQL or equivalent transactional database | required before real workflow state |
| Versioned specifications | Git | production IFC excluded by default |
| IFC processing | IfcOpenShell + pinned container | version must be fixed after qualification |
| IDS | IfcTester + pinned container | information validation only |
| Graph | Neo4j Community | projection; no source-of-truth role |
| Topology | Python Tarjan/BFS baseline | GDS optional after qualification |
| BCF | BCF 3.0 adapter + BCFzip fallback | CDE capability dependent |
| Bus | broker selected by ADR | NATS/RabbitMQ candidates; no untested claim |
| Viewer | That Open/IFClite spike | choice deferred to test matrix |
| Merge | semantic diff/assessment | automatic write-merge deferred |

---

## 14. Roadmap

### Phase 0 — Architecture freeze and evidence, 4–6 weeks

- Recover/approve this master context and ADRs.
- Publish schemas: artifact, snapshot, decision, event, validation result, policy manifest.
- Publish BRAIM-LIMS 0.1 as configurable project policy.
- Create standards/claims/grants registers.
- Establish Golden Corpus, benchmark protocol and CI baseline.
- Pin toolchain/image digests and create licence SBOM.
- Select first-pilot CDE and complete capability discovery.

### Phase 1 — Evidence-driven vertical slice, 6–8 weeks

```text
CDE artifact registration
→ hash + immutable mirror/reference
→ IFC integrity inspection
→ IDS validation
→ BCF findings
→ strict Quality Gate
→ sealed snapshot
→ provenance query
```

- Transactional registry, object storage, broker, OIDC, containerized workers.
- IFC mapping D-01 minimum implementation.
- Strict gate D-02 implementation.

### Phase 2 — Graph/topology and deep pilot boundary, 8–10 weeks

- Neo4j Community projection.
- D-03 topology rules.
- One CDE adapter capability implementation.
- Decision Register and variants.
- Semantic diff report-only.
- Benchmark result and pilot acceptance review.

### Phase 3 — Controlled release, 8–12 weeks

- Policy packs, waiver/approval and process rules.
- CDE state transition where capability allows.
- Security hardening, audit export, backup/restore drill.
- Dashboard and evidence timeline.

### Phase 4 — UI / expansion

- Viewer selection after spike.
- Second adapter only after first deep pilot evidence.
- On-prem packaging and commercialization readiness.

---

## 15. Risks

| Risk ID | Risk | Control |
|---|---|---|
| R-01 | IFC5 immaturity | sandbox adapter only; no production dependency |
| R-02 | CDE API mismatch | capability manifest and BCF/file fallback |
| R-03 | Experimental merge | report-only diff; manual resolution; Golden Corpus |
| R-04 | Invalid graph identity/history | snapshot-qualified keys; projection rebuildability |
| R-05 | False normative claim | versioned scope/expert-owned policy pack |
| R-06 | Thermal input missing | `THERMAL_CONTEXT_NOT_APPROVED` → Hold |
| R-07 | Strict gate adoption friction | explicit rule ownership, explainable BCF/evidence, calibration on corpus |
| R-08 | Graph/topology false positives | policy exceptions, labelled corpus, rule-level metrics |
| R-09 | Security/data leakage | threat model, RBAC, storage/bus controls, audit |
| R-10 | Licence conflict | SBOM and legal review before deployment |
| R-11 | KPI overclaim | R&D target label and benchmark protocol |
| R-12 | Grant information drift | evidence register and official call check immediately before filing |

---

## 16. Mandatory ADRs

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
14. Benchmark protocol and KPI publication rule.

---

## 17. Claim discipline

No technology, standard, licensing, normative or grant claim enters sales/grant/technical documentation without one of:

```text
official source reference
pinned implementation/version evidence
Golden Corpus test result
pilot measurement
legal/licensing review
```

If evidence is missing, the claim is written as `UNVERIFIED`, `R&D hypothesis`, `design decision` or `target`, not as fact.

---

## 18. Current next action

Create `braim-spec` as the governing repository:

```text
braim-spec/
  adr/
  schemas/
  policy-packs/
  mappings/
  standards-register/
  claims-register/
  compatibility-matrix/
  golden-corpus/
  benchmark-protocol/
  grant-evidence-register/
  docs/
```

Then build the Phase-1 vertical slice before UI expansion, automatic IFC merge, multi-CDE support or broad regulatory claims.
