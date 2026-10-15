# BRAIM Concept v1.1

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

### 1.3. Два режима работы

**Режим А «Аудит»** (Phase 1–2, primary): модель в BIM-программе (Archicad — primary; файл = БД, хранение таблицами-first, геометрия как проекция/предпросмотр) → BRAIM разбирает через аддоны → canonical model → проверки (IDS + расчётное ядро) → итерации с архитектором → согласование → документация, визуализации, расчётные схемы. Коннекторы Renga/Revit — отдельные адаптеры.

**Режим Б «Генерация по ТЗ»** (L16-GN, 2027+): виртуальное помещение/квартира/этаж/дом по ТЗ с учётом IDS, ГК, ФЗ, СП, ГОСТ, СанПиН → поиск вариантов (критерии: эргономика-графы + нормативы) → итоговая модель в BIM-программе. Основная модель живёт под капотом BRAIM; двусторонняя связь через Tapir-адаптеры.

### 1.4. Вертикали применения

| # | Вертикаль | Механизмы | Зрелость |
|---|---|---|---|
| 1 | АГР (Москва): IFC4 RV + GeoJSON-приложение + ТЭП → Архкомиссия | IDS-конвейер, профиль agr-geojson, cross-artifact | Phase 1 — работает на эталонах |
| 2 | Стройэкспертиза междисциплинарная (783/пр) | IDS × федерация, матрица пересечений, топология | Phase 2 |
| 3 | Поиск ОПР (квартира → дом → микрорайон) | L16-GN, эргономические графы, расчётное ядро как фильтр | 2027+ |
| 4 | Автоматизация документации (КМ/КМД, спецификации) | L13-D, Composition Format | Phase 3–4 |
| 5 | Библиотеки элементов (фермы, перегородки, сэндвич-панели, фасады) | параметрические каталоги со встроенными проверками | по вертикалям |

Связка: библиотеки (5) + проверки (1–2) = генерация (3) — элементы со встроенными правилами становятся кубиками Режима Б.

### 1.5. Архитектурные ограждения (Guardrails — REQUIRED)

**G-1. Многоредакционность нормативов.** Применимость редакции норматива определяется lifecycle-контекстом объекта (дата проектирования, стадия, явное указание в задании); дата прогона валидации не определяет применимость редакции.

```yaml
NormativeReference:
  norm_id: SP-XXX
  edition: 2020
  status: ACTIVE | SUPERSEDED | TRANSITIONAL
  applicable_from: 2020-01-01
  applicable_until: null | 2026-12-31
  binding_context: {design_date, project_stage, explicit_instruction}
```

**G-2. Мета-валидация политик.** Ни один policy pack не становится активным без meta-validation: schema-валидация, уникальность rule_id, детект конфликтующих порогов, полнота applicability, валидность ссылок на редакции, AI-правила — только через human approval. Результат мета-валидации входит в provenance policy pack.

**G-3. Coverage statement.** Каждый отчёт BRAIM содержит измеримое покрытие: `applicable_requirements_total / automated_checked / manual_only / not_covered / coverage_ratio`. Отсутствие покрытия — явное значение `NOT_COVERED`, не молчание. Это измеримая юридическая граница продукта.

**G-4. Инкрементальность.** Результат валидации привязан не только к `snapshot_id`, но и к `scope_element_ids`; изменение элемента инвалидирует только результаты, чей scope включает этот элемент или его зависимости. Цикл «правка → проверка» пересчитывает затронутый подграф, не всю модель.

**G-5. ИИ-акторы в provenance.** Каждый ИИ-актор идентифицируем: модель, версия, роль, что предложено, кто и когда подтвердил (`AIActor`). ИИ-предложение не может стать APPROVED без human approval (согласуется со статусом AI_PROPOSED в Attribute Registry).

**G-6. Граница данных.** Клиентские модели по умолчанию классифицируются как CLIENT_CONFIDENTIAL и не отправляются в публичные ИИ-сервисы; ИИ-обработка — только приватный контур / on-prem / локальные модели. Подробно — docs/security/THREAT_MODEL (§ DataBoundaryPolicy).

**G-7. Registry-ready.** Позиция «готовы к реестру отечественного ПО» без обязательств: лицензионная карта всех зависимостей, архитектурная возможность on-prem, коннекторы как отдельные адаптеры. Решение о подаче в реестр Минцифры — отдельная веха.

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
| D-07 | Два режима работы | Режим А «Аудит» — Phase 1–2; Режим Б «Генерация по ТЗ» — L16-GN, 2027+ | Подтверждено (2026-10-15) |
| D-08 | Расчётное ядро | Проверочные расчёты (не проектирование), без MEP до v0.2+: СП 50, СП 1.13130+ФЗ-123, СП 59, СанПиН 1.2.3685-20, СП 63/16/22 (проверка заданного). Сложные расчёты — внешние комплексы через адаптеры | Подтверждено (2026-10-15) |
| D-09 | Guardrails | G-1..G-7 — обязательные архитектурные требования | Подтверждено (2026-10-15) |
| D-10 | Граница данных | CLIENT_CONFIDENTIAL по умолчанию; публичные ИИ-сервисы запрещены для клиентских моделей | Подтверждено (2026-10-15) |
| D-11 | Registry-ready | Позиция готовности к реестру отечественного ПО без обязательств; решение о подаче — отдельная веха | Принято (2026-10-15) |

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
| ISO 12006-2 | 2020 | Framework классификации (методология фасетов) | Действует |
| ISO 12006-3 / ISO 23386 | — | Словари данных (bSDD — ADR-015) | Действует |
| RFC 7946 (GeoJSON) + профиль АГР | — | GeoJSON-приложение к АГР (ObjectFeature, локальная СК) | Де-факто (портал + эталон) |
| Требования Москвы к IFC АГР (ЦИМ АГР) | 2026 | IFC4 ReferenceView, RusSet_*, МССК, JSON-приложение | Действует (расп. ДИТ/ДГП 2026) |

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

### 8.1. Structure: G-D-C-M-P-R-V (по EIM Maturity Profile v0.2 draft)

```
G-D-C-M-P-R-V

G — Geometry representation (G0–G5)
D — Data/Information level (D0–D5)
C — Conformance [данные][логика][геометрия] (000–222)
M — Model geometry maturity [size,form,location,orientation] (4×0–5)
P — Precision [источник][представление] (2×0–5)
R — Relationships [геом.][лог.][инф.] (3×0–5)
V — Verification / field verification (V0–V5)
```

Канонический пример: `G2-D1-C111-M3423-P35-R343-V4`.

Полная спецификация регистров — `docs/history/eim_maturity_profile_v0_2_draft_2026-09-25.md` (заменяeт структуру G-I-C-A v1.0; агрегат `A` исключён; `0`/`null`/`not_applicable` разведены; required/actual профили разделены; координация — отдельный профиль, не через R/V).

### 8.2. Применение

Требуемый и фактический профили хранятся отдельно; сравнение покомпонентное, без компенсаций. EIM-профиль — условие перехода Lifecycle (LC-04, BRAIM_Lifecycle_Model_v0_1).

---

## 9. Roadmap & Milestones

### 9.1. Phases (обновлено 2026-10-15)

| Фаза | Название | Результат |
|---|---|---|
| 0 | Фундамент | Спек-ядро (✅ Concept v1.1, 7 схем, 3 ADR, 4 модели), LIMS-профиль совместимости с маской ЦИМ (`K01_XXX_П_X`), Standards Register, Golden Corpus (эталоны Москвы + FAIL-кейсы), SBOM, КСИ→bSDD-словарь |
| 1 | Вертикальный срез | Обёртка IfcTester→validation-result (+coverage_statement, инкрементальность G-4); policy pack v0.1 = официальные IDS Москвы (meta-validated) + braim.py + AGR-GEOJSON; фолбэк-CDE + artifact registry; cross-artifact (GeoJSON↔ТЭП-XML↔IFC); BCF findings; sealed snapshot + provenance query; **демо для соцконтракта** |
| 2 | Валидация | IDS × федерация + матрица пересечений (0/30/80), topology validator, benchmark protocol на корпусе, старт расчётного ядра (СП 50, эвакуация, МГН), Neo4j-проекция |
| 3 | Оркестратор | Quality Gate, BuildBus (NATS), snapshot manager, waiver; seed документации (КМ/КМД) |
| 4 | UI | **Node-canvas** (React Flow, философия Grasshopper/ComfyUI: каждый этап — управляемый узел с панелью и approve), стадийные панели: сверщик OCR (скан СП ↔ правило), планировка 2D/3D (граф вариантов), фасад 3D, таблицы ТЭП/расчётов с инвариантами, визуализация графов (провенанс, эргономика), timeline снапшотов с diff + панель Quality Gate (GO/NO-GO, LC-04); web-дашборд, IFC-viewer (web-ifc), генерация ТЭП-ведомости |

Режим Б (L16-GN, генерация по ТЗ) — 2027+, после Развитие-ЦТ (см. §1.3, D-07).

### 9.2. Milestones

| Веха | Что | Когда |
|---|---|---|
| M0 | Социальный контракт (до 350 тыс. ₽) — заявка подана; оборудование для MVP | осень–зима 2026 |
| M1 | Прототип evidence chain (IFC→проверки→Gate→snapshot) на эталонах АГР | дек 2026 – фев 2027 |
| M2 | Сколково (статус участника, физлицо) | зима 2027 |
| M3 | Регистрация ООО — по факту готовности к грантам | весна 2027 |
| M4 | Заявка ФСИ «Старт» (до 4 млн ₽) | весна–лето 2027 |
| M5 | Прототип: IFC→Neo4j→IfcTester→BCF→Quality Gate (полный) | сентябрь 2027 |
| M6 | Развитие / Build UP / РФРИТ; Режим Б (L16-GN) | 2027–2028 |

> Вехи v1.0 (ООО окт–ноя 2026, Старт-ЦТ-1 ноя 2026) отменены решением о финансовой лестнице — см. docs/funding/FUNDING_STATUS.md.

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

Написанные ADR: [ADR-009](./docs/adr/ADR-009_ifc5_sandbox_and_composition_alignment.md) (IFC5 sandbox + composition alignment), [ADR-015](./docs/adr/ADR-015_bsdd_as_base_dictionary.md) (bSDD как базовый словарь), [ADR-016](./docs/adr/ADR-016_ifcx_aligned_composition_format.md) (IFCX-совместимая сериализация).

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

*Версия: 1.1.0 | Дата: 2026-10-15 | Регион пилота: Республика Татарстан, Россия*

---

## 13. Changelog

### 1.1.0 — 2026-10-15

- §1.3: два режима работы (А «Аудит» — Phase 1–2; Б «Генерация по ТЗ» — 2027+).
- §1.4: карта вертикалей применения (АГР, стройэкспертиза, ОПР, документация КМ/КМД, библиотеки элементов).
- §1.5: архитектурные ограждения G-1..G-7 (многоредакционность нормативов, мета-валидация политик, coverage statement, инкрементальность, ИИ-акторы, граница данных, registry-ready).
- §2: решения D-07..D-11.
- §4.2: добавлены ISO 12006-2/3, ISO 23386, RFC 7946 + профиль АГР, требования Москвы к ЦИМ АГР.
- §8: EIM переведён на G-D-C-M-P-R-V (по draft v0.2); G-I-C-A удалена.
- §9.2: вехи переписаны под подтверждённую финансовую лестницу (соцконтракт → Сколково → ООО → ФСИ «Старт»); вехи v1.0 M0/M1 отменены.
- §11: отмечены написанные ADR-009/015/016.

### 1.0.0 — 2026-10-04

- Первоначальная публикация.
