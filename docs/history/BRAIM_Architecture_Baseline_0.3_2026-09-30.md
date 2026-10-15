# BRAIM — актуализированная архитектурная база

**Версия:** 0.3.0  
**Статус:** Architecture Baseline / Research Draft  
**Дата актуализации:** 30 сентября 2026  
**Регион и фокус пилота:** Республика Татарстан, Россия  
**Назначение:** единый исправленный документ для проектирования MVP, технического аудита, подготовки пилота и грантовых материалов.

---

## 1. Позиционирование без завышенных обещаний

**BRAIM (Building Information Atomic Model)** — openBIM-ориентированный слой оркестрации процессов управления информацией. BRAIM не является авторской BIM-системой, не заменяет CDE и не обязан хранить все исходные файлы. Он связывает неизменяемые информационные артефакты, машиночитаемые правила, запуски проверок, замечания, решения, снапшоты и контролируемые выпуски.

Ценность BRAIM:

```text
контейнер / IFC-артефакт
→ версия правила и область применимости
→ проверка
→ доказательства и BCF-замечания
→ Quality Gate
→ неизменяемый снапшот
→ контролируемый выпуск / блокировка / эскалация
```

### 1.1. Что BRAIM может заявлять

- Регистрирует артефакты и их контрольные суммы.
- Запускает версионируемые правила проверки IFC и связанных данных.
- Поддерживает IDS-проверки через подходящий валидатор, например IfcTester.
- Собирает результаты геометрических, топологических, информационных и процессных проверок.
- Формирует доказуемое решение Quality Gate: `Go`, `Hold`, `No-Go`, а при необходимости — отдельный аудитируемый `Waived`.
- Хранит прослеживаемость между артефактом, версией правила, запуском валидатора, BCF-замечанием, проектным решением и снапшотом.
- Интегрируется с CDE через адаптеры и доступные возможности конкретной системы: API, BCF, файлы, polling или webhooks.

### 1.2. Что BRAIM не должен заявлять

- «Проверяет соответствие всем ГОСТ, СП и нормативам».
- «Гарантирует пожарную безопасность, прохождение экспертизы или отсутствие рисков».
- «Делает универсальный git merge любого IFC без участия человека».
- «Все CDE поддерживают OpenCDE или BCF API».
- «Все Pset и provenance всегда переживают round-trip через Revit, Archicad, Renga и другие авторские системы».
- «Ноль clash означает полную координацию модели».

Корректная формулировка: **BRAIM автоматизирует проверку конкретных, явно определённых, версионированных и машиночитаемых правил. Результат является доказательной основой для назначенной проектной роли, а не автоматическим нормативным сертификатом.**

---

## 2. Что принято и что ещё не принято

### 2.1. Принятые направления

- OpenBIM-first: IFC, IDS, BCF и проектные профили обмена.
- Федеративная модель: дисциплинарные контейнеры независимы; координация основана на связях, scope и правилах.
- Снапшот неизменяем: исправление создаёт новый снапшот, а не редактирует старый.
- История снапшотов может быть DAG: есть обычные родители и узлы merge.
- CDE suitability/state отделено от байтового содержимого артефакта.
- Контракты шины отделяют команды, события, запросы и большие артефакты.
- Quality Gate основан на versioned policy packs и сохраняет evidence.

### 2.2. Не принятые / требующие восстановления решения

Дыры 1–3 отсутствуют в исходном контексте. До восстановления исходных формулировок, альтернатив, принятого решения и критерия приёмки они имеют статус:

```text
ARCHITECTURAL GAP — UNKNOWN — BLOCKS ARCHITECTURE FREEZE
```

Нельзя заявлять, что «все девять дыр закрыты». Корректно: **документированы и предварительно закрыты вопросы 4–9; вопросы 1–3 требуют восстановления и отдельного ADR.**

---

## 3. Нормативные и технологические рамки

### 3.1. Как использовать стандарты

| Область | Роль в BRAIM | Важное уточнение |
|---|---|---|
| ISO 19650 | Принципы управления информацией, CDE-процессы, роли, требования к информации | Не задаёт одну обязательную схему имён, один универсальный набор статусов или одну модель нумерации |
| ISO 19650-5 | Security-minded подход к управлению информацией | Не сводится к TLS/OIDC; нужны оценка рисков, роли, информационные требования и управленческие меры |
| IFC | Обменная модель и семантика объектов/отношений | Поддержка зависит от конкретной схемы, MVD/ER и реального toolchain |
| IDS | Машиночитаемая спецификация требований к доставляемой информации | Не является полным языком нормативной экспертизы, геометрии или всех бизнес-правил |
| BCF | Обмен замечаниями и контекстом координации | Нужно назначить system of record и правила синхронизации |
| OpenCDE | Целевая интероперабельность CDE | Наличие стандарта не означает реализацию у конкретного поставщика |
| ГОСТ/СП/методики | Источник требований, если правило формализовано и применимо | Каждое автоматическое правило требует версии источника, интерпретации, scope, допусков и ответственного эксперта |

### 3.2. IFC scope

BRAIM в MVP должен документировать точную область поддержки, а не писать «поддерживает весь IFC». Пример:

```yaml
supported_exchange_scope:
  formats: [IFC-SPF]
  schemas: [IFC2X3_TC1, IFC4_ADD2_TC1, IFC4X3_ADD2]
  operations:
    parse: tested
    information_validation: tested
    graph_projection: tested_for_selected_entities
    geometry: tested_for_selected_profiles
    authoring_roundtrip: per_tool_and_version_only
```

`IFC4x3 Add2` — корректное обозначение конкретной схемы, если оно действительно подтверждено тестами выбранного toolchain. Не следует связывать каждую возможность со словом «IFC 4.3» без указания уровня: parse, geometry, export, round-trip или validation.

### 3.3. IDS и BCF

IfcTester пригоден как один из компонентов IDS-валидации: он читает/создаёт IDS и проверяет IFC на соответствие IDS. Это информационная проверка; она не заменяет проверку формы, коллизий, достижимости, нормативной интерпретации или проектного решения.

BCF подходит для переноса замечаний. Для каждого BCF topic надо хранить внутренний `issue_id`, внешний ID, источник, fingerprint, scope, правило, версию правила, затронутые GUID и состояние синхронизации.

---

## 4. Источники истины и хранение

### 4.1. Исправленное правило

**Neo4j не является единственным источником истины.** Это пересобираемая графовая проекция, оптимизированная для анализа связей, влияния изменений, поиска и отчётов.

| Данные | Authoritative record | Проекция / кэш | Инвариант |
|---|---|---|---|
| Исходный модельный артефакт IFC | Контрактно назначенная CDE либо immutable object storage | Viewer cache, Neo4j projection | После регистрации конкретная версия не меняется |
| BCF/отчёты | Immutable object storage + registry record | CDE/issue UI | Имеют hash, версию правила и run ID |
| Состояние BRAIM (снапшоты, решения, gates, связи) | PostgreSQL или эквивалентный транзакционный реестр | API/UI/аналитика | Изменения аудируются |
| Policy packs, schemas, код | Git | deployment cache | Release/tag/digest фиксирован |
| Граф IFC | Neo4j projection | отчёты/запросы | Перестраиваем из артефакта и mapping profile |
| Статус/состояние контейнера CDE | CDE, если она его ведёт | BRAIM mirror | Владелец статуса фиксируется в adapter contract |

### 4.2. Хранилище артефактов

Вариант по умолчанию для MVP: S3-совместимое хранилище, например MinIO on-prem, с версионированием, контрольными суммами, политиками доступа, резервным копированием и, если требуется, object lock/retention. S3 API сам по себе не делает запись неизменяемой — это обеспечивается политиками и конфигурацией.

Каждый артефакт имеет:

```json
{
  "artifact_id": "art_01J...",
  "kind": "ifc|ids|bcf|validation-report|policy-pack|snapshot",
  "content_type": "application/x-step",
  "sha256": "sha256:...",
  "byte_size": 0,
  "stored_at": "2026-09-30T00:00:00Z",
  "source_system": "cde|git|user|validator",
  "source_reference": "...",
  "retention_class": "project-record"
}
```

### 4.3. Git

Git обязателен для исходного кода, JSON Schema, policy packs, ADR, mapping profiles, тестовых данных и manifests. Для больших IFC Git не является безусловно лучшим решением: допустимы CDE-managed versions, object storage или Git LFS — выбор фиксируется ADR исходя из размера, retention, требований заказчика, режима доступа и процедуры выпуска.

---

## 5. Идентичность, имена и версии

### 5.1. Идентичность не равна имени файла

| Поле | Назначение | Пример |
|---|---|---|
| `project_id` | внутренний глобальный ID проекта | `prj_01J...` |
| `container_id` | логический информационный контейнер | `cnt_01J...` |
| `artifact_id` | неизменяемая версия файла/отчёта | `art_01J...` |
| `snapshot_id` | глобальный ID снапшота | `snp_01J...` |
| `iteration_code` | удобный alias | `IT004` |
| `release_id` | логический выпуск | `rel_01J...` |
| `revision_code` | код, требуемый проектом/CDE | `P01.02` |
| `variant_id` | вариант решения | `var_01J...` |
| `ifc_global_id` | идентичность IFC-сущности в конкретном model version | `3xWq...` |
| `sha256` | целостность содержимого | `sha256:...` |

Имя файла — человекочитаемый alias. Нельзя использовать его как единственный технический ключ.

### 5.2. BRAIM LIMS: конфигурируемая политика

BRAIM-LIMS должен быть versioned project policy, а не заявлением об универсальном правиле отрасли.

```yaml
naming_policy:
  version: 0.1.0
  filename_template: "{project}-{originator}-{discipline}-{zone}-{type}-{revision}.ifc"
  include_cde_status_in_filename: false
  external_revision_policy: "client-defined"
  snapshot_alias_template: "IT{sequence:03d}"
  exchange_profile_metadata: true
  state_codes_source: "project-information-standard"
```

Правило по умолчанию: mutable CDE status хранится в метаданных, чтобы смена suitability не требовала переименования и не ломала ссылки. Но если EIR/BEP/контракт предписывает статус в имени, policy может это включить.

### 5.3. Снапшоты и ревизии

Снапшот — неизменяемый checkpoint BRAIM. Его нумерация не должна автоматически навязывать внешнюю схему ревизий CDE. Несколько снапшотов могут существовать внутри одного внешнего revision workflow, а один снапшот может фиксировать несколько артефактов/дисциплин.

```text
BRAIM snapshot: техническая и аудиторская фиксация состояния
CDE revision/release: контрактный/проектный выпуск контейнера
CDE suitability/state: процессный статус контейнера
```

---

## 6. Domain model и жизненные циклы

### 6.1. Агрегаты

```text
Project
 ├─ InformationContainer
 │   └─ ArtifactVersion
 ├─ IterationSnapshot (immutable)
 ├─ Release
 ├─ Variant
 ├─ Decision
 ├─ ValidationRun
 ├─ QualityGateDecision
 ├─ PolicyPack
 ├─ IssueLink
 └─ LifecycleFork
```

### 6.2. Состояния

**Container state** (настраивается проектной политикой):

```text
WIP → SHR → PUB → ARC
```

Это пример процессной модели, а не доказательство того, что все CDE используют именно эти коды. Переходы должны быть согласованы с EIR/BEP/контрактом.

**Variant:**

```text
proposed → evaluating → selected → implemented → superseded
                 ├→ rejected
                 └→ on_hold
```

**Quality Gate:**

```text
pending → running → go
                  → hold → resolved → running
                  → no_go → remediating → running
                  → waived
```

`waived` — не синоним `go`; это управляемое исключение с владельцем риска, основанием, сроком действия, ролью утверждающего и audit trail.

---

## 7. BuildBus: контракты взаимодействия

### 7.1. Разделение типов сообщений

- **Command** — запрос выполнить действие, имеющий одного владельца.
- **Event** — зафиксированный факт, потенциально имеющий много подписчиков.
- **Query** — синхронное получение данных через API, не сообщение шины.
- **Artifact reference** — ссылка на крупный объект; IFC/BCF не передаётся в body события.

Для MVP допустим NATS JetStream, RabbitMQ или другой брокер после ADR-сравнения. Нельзя утверждать, что один из них «объективно проще» без привязки к объёму, команде, on-prem ограничениям, durability, порядку доставки и эксплуатации.

### 7.2. Envelope

```json
{
  "specversion": "1.0",
  "id": "evt_01J...",
  "type": "org.braim.validation.completed.v1",
  "source": "braim://validator/ids",
  "subject": "project/prj_01J.../snapshot/snp_01J...",
  "time": "2026-09-30T18:00:00Z",
  "datacontenttype": "application/json",
  "correlation_id": "cor_01J...",
  "causation_id": "evt_01J...",
  "tenant_id": "ten_01J...",
  "project_id": "prj_01J...",
  "actor": {"type": "service", "id": "svc-ids-validator"},
  "data": {}
}
```

Это CloudEvents-inspired envelope. Называть его полностью совместимым CloudEvents можно только после формальной проверки соответствия выбранному binding/specification.

### 7.3. Надёжность

1. Доставка сообщений: `at-least-once`.
2. Каждый consumer идемпотентен по `event_id`/idempotency key.
3. Изменение реестра и публикация события согласуются через transactional outbox.
4. Retry имеет backoff и ограничение попыток; затем сообщение попадает в DLQ.
5. Должны существовать reconciliation jobs, компенсирующие действия и мониторинг несогласованных состояний.
6. Нельзя переносить большие IFC/BCF payload через брокер.
7. Несовместимое изменение контракта создаёт новый type/version, например `...v2`.

### 7.4. Минимальные темы

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

## 8. Коннекторы и их границы

### 8.1. Правило ports-and-adapters

Бизнес-логика BRAIM не зависит от конкретного HTTP API, SDK или вендора. Внутренний порт описывает намерение; адаптер переводит его в конкретную интеграцию.

```text
BRAIM domain service → internal port → adapter → CDE / validator / storage / authoring tool
```

### 8.2. Приоритетные коннекторы

| ID | Коннектор | Ответственность | Реалистичный MVP | Что нельзя обещать |
|---|---|---|---|---|
| C-01 | Artifact Store | put/get/seal, hash, retention | S3/MinIO + SHA-256 | юридическая неизменяемость без политики retention |
| C-02 | Snapshot Registry | создать и seal manifest | PostgreSQL + schema validation | изменяемые snapshot records |
| C-03 | IFC Ingest | parse/index/diagnostics | IfcOpenShell, selected entities | полную поддержку любого IFC |
| C-04 | IDS Validator | информационные проверки | IfcTester + IDS policy | нормативную экспертизу |
| C-05 | BCF Adapter | создавать/синхронизировать issues | BCFzip + internal issue model | идеальный sync со всеми CDE |
| C-06 | Quality Gate | aggregate evidence, decision | rules v0 | экспертную замену человека |
| C-07 | Graph Projection | queryable IFC relationships | Neo4j selected graph | единственный source of truth |
| C-08 | CDE Adapter | файл/метаданные/status/BCF | один конкретный CDE | универсальный OpenCDE support |
| C-09 | Merge Provider | diff/conflict assessment | report-only | universal auto-merge |
| C-10 | Topology Validator | selected topology rules | containment/connectivity | вся топология всех дисциплин |

### 8.3. IFC Ingest

Вход: immutable IFC artifact, schema declaration, mapping profile, scope.  
Выход: parse report, canonical element index, graph projection event, warning report.

Последовательность:

1. Проверить SHA-256, размер, content type и доступ.
2. Открыть IFC в изолированном worker.
3. Определить schema identifier, units, `IfcProject`, GlobalId issues, spatial hierarchy.
4. Извлечь индекс: element GUID, class, name, type, containment, selected Psets/classifications.
5. Создать или обновить graph projection с ссылкой на `artifact_id` и `mapping_profile_digest`.
6. Сохранить machine-readable diagnostics.

GUID недостаточен для всех IFC-сущностей. Для secondary entities нужен детерминированный ID с происхождением, например `(artifact_id, parent GUID, entity type, structural path/hash)`.

### 8.4. Graph Projection

Минимальный граф:

```text
(:ModelVersion {artifact_id, sha256, schema, mapping_digest})
(:Element {global_id, ifc_class, name, type_name})
(:Spatial {global_id, ifc_class})
(:PropertySet {name})
(:Property {name, value, value_type})
(:ClassificationReference {system, code, name})

(ModelVersion)-[:CONTAINS]->(Element)
(Element)-[:CONTAINED_IN]->(Spatial)
(Element)-[:HAS_PSET]->(PropertySet)-[:HAS_PROPERTY]->(Property)
(Element)-[:CLASSIFIED_AS]->(ClassificationReference)
(Element)-[:RELATES_TO {ifc_rel_class}]->(Element)
```

Не переносить в MVP каждый geometric primitive в отдельный графовый узел. Геометрию хранить как производный артефакт/mesh/BREP reference; в графе — лишь нужные индексы, связи, bbox и вычисленные признаки.

### 8.5. CDE Adapter и capabilities

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

Если webhook отсутствует — polling. Если BCF API отсутствует — BCFzip. Если metadata write отсутствует — sidecar registry с явным предупреждением о расхождении. Никакая конкретная CDE не считается совместимой до теста её версии и возможностей.

### 8.6. BCF Adapter

Нужен fingerprint, чтобы повторная проверка обновляла существующее замечание, а не плодила дубли:

```text
sha256(rule_id + policy_digest + sorted(affected_guids) + normalized_location)
```

Внутренняя запись issue содержит `issue_id`, `external_topic_id`, `source_system`, `snapshot_id`, `validation_run_id`, `rule_id`, severity, state, assignee, due date, first_seen, last_seen, resolved, affected elements и artifact refs.

### 8.7. Merge Provider

До квалификации конкретного продукта/версии и прохождения golden corpus реализуется только:

```text
semantic diff → conflict classification → BCF/decision workflow → Hold/No-Go
```

Исходы assessment:

- `auto_mergeable_candidate` — независимые изменения, требующие policy check;
- `requires_decision` — конфликт значения/свойства/связи;
- `unsafe` — delete-vs-modify, сломанная containment hierarchy, schema conflict;
- `unsupported` — не поддержан mapping/profile.

Автоматический write-merge не входит в MVP-обещание.

---

## 9. Quality Gate и policy packs

### 9.1. Уровни проверки

| Уровень | Вопрос | Пример |
|---|---|---|
| Integrity | Можно ли доверенно обработать артефакт? | hash, parse, schema, units, duplicate GUIDs |
| Information | Доставлена ли требуемая информация? | IDS entity/property/classification |
| Geometry | Есть ли измеримые пространственные нарушения? | clash, clearance, distance, tolerance |
| Topology | Корректны ли связи, замкнутость и достижимость? | containment, components, boundaries |
| Process | Имеются ли обязательные approvals/checks? | role, status, mandatory validator run |
| Domain rule | Выполнено ли конкретное формализованное требование? | rule with source edition and scope |

### 9.2. Severity

```text
blocking — файл/процесс нельзя считать обрабатываемым
critical — нарушение обязательного формализованного правила
major — существенная проблема, требующая решения
minor — не блокирующее отклонение
info — наблюдение
```

Пример aggregator policy:

```yaml
quality_gate:
  required_validators: [integrity, ids]
  aggregation:
    - when: "required_validators_missing == true"
      outcome: no_go
    - when: "summary.blocking > 0"
      outcome: no_go
    - when: "summary.critical > 0"
      outcome: no_go
    - when: "summary.major > 0"
      outcome: hold
    - when: "all_required_checks_passed == true"
      outcome: go
  waiver:
    allowed_roles: [information_manager, project_director]
    requires: [rationale, risk_owner, expiry_at, approval_reference]
```

### 9.3. Policy pack

```text
policy-pack/
  manifest.yaml
  ids/
  geometry/
  topology/
  process/
  mappings/
  tests/
  changelog.md
```

```yaml
id: braim.project.example.stage-P
version: 1.0.0
ifc_schemas: [IFC2X3_TC1, IFC4_ADD2_TC1, IFC4X3_ADD2]
required_validators: [integrity, ids, topology]
source_register_refs:
  - STD-IDS-001
  - STD-PROJECT-001
rules:
  - id: ids.architecture.v3
  - id: topology.spatial.containment.v1
  - id: process.shared-release.v1
```

Каждый gate хранит hashes входных артефактов, policy digest, образ/версию валидатора, результаты, BCF links, алгоритм агрегации, timestamp, actor/service identity и override, если он был.

---

## 10. Топологический и геометрический валидатор

### 10.1. Разделение терминов

- Геометрия: форма, расстояние, пересечение, координаты, допуски.
- Топология: связность, соседство, замкнутость, ориентированность, достижимость.
- Семантика: класс и роль элемента.
- Норма: формализованное правило с источником, редакцией, scope и интерпретацией.

### 10.2. MVP rules

| Rule ID | Проверка | Ограничение |
|---|---|---|
| `topology.spatial.containment.v1` | Допустимая пространственная принадлежность выбранных элементов | Работает только для согласованного mapping profile |
| `topology.mep.connected-components.v1` | Число компонент связности выбранной сети | Требует корректных ports/connectivity данных |
| `topology.space.boundary.v1` | Наличие/целостность выбранных границ IfcSpace | Не доказывает физическую герметичность здания |
| `topology.egress.reachability.v1` | Наличие пути в графе помещений/дверей по заданным правилам | Не заменяет пожарный расчёт и экспертизу |
| `geometry.clash.selected-scope.v1` | Clash в заданных дисциплинах и допусках | Ноль clash не доказывает полную координацию |

Допуски — часть policy:

```yaml
geometry_tolerance:
  linear_m: 0.001
  angular_deg: 0.1
  gap_closure_m: 0.01
```

### 10.3. Алгоритмический pipeline

```text
IFC artifact
→ extract / normalize units and placements
→ build spatial, connectivity and adjacency graphs
→ execute rule with declared tolerance and scope
→ create evidence JSON + BCF topic
→ send ValidationCompleted
→ Quality Gate aggregates result
```

Все результаты должны быть объяснимыми: затронутые GUID, путь в графе/набор рёбер, используемые допуски и версия правила.

---

## 11. Снапшоты, provenance и решения

### 11.1. Дополнение схемы снапшота

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
  "provenance": {},
  "signatures": []
}
```

### 11.2. Sealing protocol

1. Создать candidate snapshot.
2. Проверить JSON Schema и бизнес-инварианты.
3. Проверить наличие и hashes всех artifact refs.
4. Проверить обязательные validation runs и policy pack.
5. Рассчитать canonical JSON digest.
6. В транзакции установить `sealed`.
7. Положить в outbox событие `snapshot.sealed`.
8. Любое изменение создаёт новый snapshot с parent link.

Техническая подпись/hash подтверждает техническую целостность только при определённых процедурах key custody, canonicalization, rotation, revocation, timestamping и аудите. Она не заменяет юридически значимую электронную подпись, когда такая нужна.

### 11.3. Decision Register

```json
{
  "decision_id": "dec_01J...",
  "project_id": "prj_01J...",
  "subject_type": "variant",
  "subject_id": "var_01J...",
  "outcome": "selected",
  "rationale": "...",
  "evidence_refs": ["val_01J...", "art_01J..."],
  "decided_by": "usr_01J...",
  "authority_role": "chief_project_engineer",
  "decided_at": "2026-09-30T00:00:00Z",
  "supersedes": null
}
```

---

## 12. Безопасность и эксплуатация

### 12.1. Базовый security baseline

- Оценка угроз и классификация информации до пилота.
- OIDC для пользователей; service identities для workers.
- TLS на внешних и внутренних соединениях; mTLS там, где оправдано моделью угроз.
- RBAC с project scope; разделение обязанностей для waiver/override.
- Полный audit event: actor, action, target, before/after, time, correlation ID.
- Не передавать IFC, секреты, токены и лишние персональные данные в event payload.
- Проверять загружаемые файлы, архивы и контейнерные образы.
- Регулярный backup/restore drill.
- SBOM и инвентаризация лицензий перед поставкой on-prem.

### 12.2. Роли

```text
viewer
model_author
coordinator
information_manager
quality_manager
project_director
system_administrator
```

Пользователь, загрузивший модель, не должен единолично отменять блокирующий Quality Gate без режима исключения, разделения ролей и audit trail.

### 12.3. Наблюдаемость

Все работы связываются `correlation_id`:

```text
artifact registered
→ graph ingested
→ IDS completed
→ topology completed
→ BCF synchronized
→ gate hold
→ decision recorded
→ revalidation
→ gate go
→ snapshot sealed
```

Метрики: длительность pipeline, `Go/Hold/No-Go`, доля ретраев, failed jobs, повторно открытые BCF issues, дубликаты, скорость parse, coverage golden corpus, неавторизованные попытки доступа.

---

## 13. Стратегия интеграции и тестирования

### 13.1. Матрица совместимости

Ни один компонент не имеет статуса «готово» без конкретных версий и тестов.

| Компонент | Версия | Подтверждено | Не подтверждено | Статус |
|---|---|---|---|---|
| IfcOpenShell | фиксируется в контейнере | parse выбранных IFC | полный round-trip | Test required |
| IfcTester | фиксируется в контейнере | выбранные IDS tests | нормативная экспертиза | Test required |
| Viewer | кандидат + версия | selected model viewing | все IFC/BCF workflows | Spike required |
| CDE adapter | vendor + version | конкретные capabilities | универсальная интеграция | Pilot required |
| Merge provider | repo/tag/commit | diff corpus | universal merge | Experimental |
| Authoring tool | tool + version | отдельный round-trip matrix | generic preservation | Test required |

### 13.2. Golden corpus

Обязательные наборы:

- синтетические и обезличенные IFC2x3/IFC4/IFC4x3 модели в реально обещаемом scope;
- модели с ожидаемыми IDS pass/fail;
- намеренно повреждённые metadata/GUID/units cases;
- cases для containment, connectivity, space boundaries;
- BCF expected outputs;
- diff и delete-vs-modify scenarios;
- CDE import/export fixtures;
- round-trip fixtures для каждого заявленного authoring tool/version.

У каждого теста: входной artifact hash, policy digest, ожидаемый JSON/BCF, версия контейнера валидатора.

### 13.3. Лицензии

До коммерческой поставки создать SBOM:

```text
component → version → direct/transitive → licence → distribution implication → owner → evidence
```

Не смешивать заявления о лицензии core library с лицензиями всех инструментов/плагинов/контейнеров. Проверить обязательства GPL/LGPL/MIT/MPL и условия распространения/модификации отдельно с профильным юристом.

---

## 14. Актуализированная дорожная карта

### Phase 0 — architecture freeze, 4–6 недель

- Восстановить дыры 1–3 и оформить ADR.
- Принять BRAIM-LIMS 0.1 как конфигурируемую project policy.
- Зафиксировать schema: artifact, snapshot, decision, policy pack, event envelope, validation result.
- Выпустить Quality Gate Specification 0.1.
- Создать standards/source register и claims register.
- Создать golden corpus и CI baseline.
- Сделать toolchain/licence inventory.
- Подготовить юрлицо/грантовую стратегию только по текущим официальным условиям конкурса.

### Phase 1 — узкая сквозная вертикаль, 6–8 недель

```text
IFC registration
→ hash + immutable storage
→ basic IFC inspection
→ IDS validation
→ BCF export
→ Quality Gate v0
→ sealed snapshot + provenance query
```

Инфраструктура: PostgreSQL, object storage, один event broker после ADR, OIDC, containerized workers.

### Phase 2 — граф и пилотный CDE boundary, 8–10 недель

- Neo4j projection для выбранных запросов.
- Один CDE adapter с capability manifest.
- Decision Register и variants.
- Semantic diff report-only.
- Топология MVP.
- Pilot readiness test.

### Phase 3 — контролируемый выпуск, 8–12 недель

- Policy packs, gate aggregation, waiver/approval.
- CDE status workflow, если capability доступна.
- Security hardening, audit export, backup/restore drill.
- Метрики качества и dashboard.

### Phase 4 — UI и расширение

- Выбор viewer по результатам spike.
- Snapshot timeline, issue context, evidence navigation.
- Второй adapter и on-prem packaging после пилота.

---

## 15. Реестр известных рисков

| Risk ID | Риск | Митигирование | Stop condition |
|---|---|---|---|
| R-01 | Дыры 1–3 неизвестны | Восстановить и ADR до freeze | Нет freeze без закрытия |
| R-02 | IFC merge dependency | diff-only MVP, fallback/manual workflow, golden corpus | Не обещать auto-merge |
| R-03 | CDE API недоступен | capability adapter, BCFzip/file fallback | Не включать в контракт непроверенную интеграцию |
| R-04 | Ложные нормативные claims | policy scope, expert review, legal wording | Нет «полного compliance» в маркетинге |
| R-05 | Round-trip теряет данные | vendor/version regression matrix | Не заявлять preservation без теста |
| R-06 | Graph drift | rebuild from artifacts, mapping profile digest | Neo4j не authoritative |
| R-07 | Неповторяемые gates | hashes, immutable reports, pinned container images | No evidence → no Go |
| R-08 | Security/data leakage | threat model, classification, RBAC, audit, storage controls | Нет реального пилота до baseline review |
| R-09 | Грантовые параметры устарели | official call check before submission | Не использовать старый слайд/таблицу |

---

## 16. Гранты: только актуальная и безопасная формулировка

На дату актуализации нельзя фиксировать будущие дедлайны как факт без текущего официального объявления. Параметры конкретных конкурсов меняются по очередям.

Проверенное направление для планирования:

- Для проверенного объявления **Старт-ЦТ-1** в 2026 году: до 5 млн ₽, срок выполнения 12 месяцев. Условия допуска участников, требования к команде, МТК и РИД необходимо подтверждать непосредственно по документации актуальной очереди.
- Для проверенного объявления **Развитие-ЦТ** в 2026 году: до 30 млн ₽, срок 12 или 18 месяцев, внебюджетное софинансирование — не менее 20%. Это не следует переносить на будущий конкурс без повторной проверки.
- Утверждение «статус МТК даёт +1–2 балла» должно заменяться точной формулировкой из документации конкретного конкурса: доступные источники для разных конкурсов указывают разные значения.
- ООО и статус МСП могут быть необходимы для конкурсов, адресованных малым предприятиям, но нельзя говорить, что ООО является безусловным блокером каждого трека без проверки условий актуальной очереди.
- РФРИТ, Build UP, региональные программы, суммы и сроки требуют отдельной официальной верификации непосредственно перед применением в стратегии.

Для грантового пакета нужен отдельный `Grant Evidence Register`: программа, очередь, URL/документ, дата публикации, дата проверки, требования, сумма, срок, софинансирование, eligibility, ответственный и дата следующего review.

---

## 17. Обязательные ADR

1. **ADR-001 Source of truth:** registry и immutable artefacts authoritative; Neo4j projection rebuildable.
2. **ADR-002 Event delivery:** at-least-once, idempotent consumers, transactional outbox, DLQ, reconciliation.
3. **ADR-003 Artifact transport:** IFC/BCF не передаются через broker, только refs + hashes.
4. **ADR-004 Merge:** semantic diff/assessment first; no universal auto-merge claim.
5. **ADR-005 Policies:** policy packs versioned, hashed, tested and retained with every gate.
6. **ADR-006 CDE:** capability-driven adapters, BCF/file fallback.
7. **ADR-007 Claims:** machine-checkable rules, not blanket regulatory certification.
8. **ADR-008 LIMS:** configurable project policy; external naming/revision/status requirements prevail when contractually mandated.
9. **ADR-009 Toolchain:** exact versions, container image digests, licence SBOM and golden corpus required before supported status.
10. **ADR-010 Security:** threat model and information classification required before customer model onboarding.

---

## 18. Definition of Done для MVP

MVP считается готовым только если на golden corpus и пилотном сценарии доказано:

1. Артефакт получает immutable reference и SHA-256.
2. IFC проходит воспроизводимый parse в заявленном scope.
3. IDS policy запускается с зафиксированной версией валидатора и policy pack.
4. Ошибки формируют стабильные BCF/issue records без лавины дублей при повторном запуске.
5. Quality Gate объясняет свой результат через конкретные evidence refs.
6. Sealed snapshot невозможно тихо изменить.
7. По artifact/snapshot доступна provenance chain.
8. При сбое broker/worker возможен retry/reconciliation без двойных релизов и снапшотов.
9. Все заявленные возможности имеют запись в compatibility matrix.
10. Нет маркетинговых/грантовых claim, которые не привязаны к источнику или тесту.

---

## 19. Следующее действие

Первый технический артефакт после этого baseline — не UI и не merge engine. Это репозиторий `braim-spec` со следующей структурой:

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
  grant-evidence-register/
  docs/
```

После этого реализуется один вертикальный pipeline: `artifact → IDS → BCF → Gate → sealed snapshot`. Только когда он воспроизводим и доказуем, расширяются граф, CDE adapters, topology и UI.

---

## Appendix A — журнал исправлений

| Предыдущее утверждение | Исправление |
|---|---|
| Neo4j — источник истины | Neo4j — пересобираемая графовая проекция |
| IfcOpenShell 0.8.5 указан как актуальный | Версию фиксировать по tested container; проверенный upstream на дату ревизии указывает v0.9.0 |
| Развитие-ЦТ до 20 млн / 12–24 мес | Для проверенного 2026 объявления: до 30 млн / 12 или 18 мес / 20%+ co-financing |
| S0–A1 — универсальные коды ISO | Коды и naming — конфигурируемая project policy |
| Каждый snapshot сбрасывает release | Snapshot и внешний revision workflow разделены |
| ifcmerge — базовый механизм | Только optional experimental merge provider; MVP = diff + Hold |
| Pset provenance переживает любой round-trip | Только после tool/version regression test |
| OpenCDE обеспечит все CDE интеграции | Capability-driven adapters + fallbacks |
| БРАИМ проверяет нормы | Проверяет конкретные формализованные policy rules |
| 0 clash = координация | Только результат выбранного scope/rules/tolerances |
| “готово” для компонентов | Только “tested/qualified” с version/evidence |

