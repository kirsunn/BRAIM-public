# BRAIM — Unified External AI Review Bundle v0.1

> Единый файл для передачи внешнему ИИ. Материалы являются рабочими спецификациями, прототипными идеями и draft-документами, если явно не указано иное.

---

# Part 1. External AI Review Instructions

## Назначение

Этот файл предназначен для передачи внешнему ИИ, который не может надёжно открыть GitHub-репозиторий BRAIM. Он объединяет контекст проекта, опубликованные документы и инструкции для архитектурного анализа.

## Правила чтения

1. Сначала составь таблицу реально прочитанных разделов.
2. Не делай выводов только по заголовкам.
3. Не считай документированную идею реализованной.
4. Если сведений недостаточно, помечай это как `UNKNOWN`.
5. Не выдумывай нормативные значения.
6. Разделяй официальный источник, пользовательский ввод, измерение, расчёт, AI-интерпретацию, проектное решение и проверенное утверждение.
7. Сохраняй различия:

```text
Room != Zone
Zone != Niche
Opening != Filling
Adjacency != Access
Requirement != Constraint
```

## Требуемый формат таблицы чтения

| Раздел | Прочитан | Источник внутри bundle | Что использовано |
|---|---:|---|---|

## Требуемый анализ

### A. Краткое заключение

Оцени зрелость BRAIM. Отдели пригодное для прототипирования от преждевременных идей.

### B. Архитектурные риски

Ищи дублирование ответственности, циклические зависимости, слишком широкое ядро, отсутствие владельца истины, отсутствие версий и миграций, смешение норм и гипотез, неконтролируемые AI-выводы, отсутствие воспроизводимости, negative tests, преждевременную привязку к Archicad и неясные границы IFC.

### C. Минимальное ядро BRAIM Core v0.1

Раздели компоненты на обязательное ядро, плагины, внешние адаптеры и документационные/управленческие функции.

### D. Слои и дисциплины

Проверь взаимодействие semantic layers `L0–L15` и discipline views `D0–D13`. Укажи конфликты, недостающие элементы и способ представления обеих осей в одной сущности.

### E. Метамодель сущностей

Предложи минимальный набор сущностей и для каждой укажи идентификаторы, обязательные атрибуты, владельца истины, статусы, связи, unknown и derived values.

### F. Реестры

Проверь Attribute Registry, Claim/Evidence Registry, Model View Registry и CDE State Machine. Предложи минимальные схемы, версии, владельцев, статусы, конфликты, устаревание и тесты.

Для provenance покажи цепочку:

```text
Source → Activity → Claim → Rule → Validation Result → Decision
```

### G. Validation Kernel

Опиши входы, выходы, severity, hard/soft constraints, обработку UNKNOWN, источники, `instance_id`, блокировку публикации и warnings. Приведи минимум пять проверок без выдуманных нормативных чисел.

### H. CDE

Проверь состояния WIP, SHARED, PUBLISHED, ARCHIVE и review/release-статусы. Предложи переходы, автоматические события, ручные подтверждения, публичные ограничения и повторную проверку после изменения источника.

### I. Topology-first prototype

Предложи минимальный воспроизводимый прототип с помещениями, зонами, required/forbidden relations, access graph, прямоугольной геометрией, проверкой пересечений, достижимости и seed. Размеры должны быть project-defined placeholders.

### J. Интеграции

Определи границы внутренней модели BRAIM, внутреннего формата, внешнего представления, адаптера и экспорта для IFC, IDS, BCF, Archicad, point clouds, geospatial data и Model View Registry.

### K. Три первых прототипа

Выбери только три прототипа с максимальной ценностью. Для каждого укажи цель, входы, выходы, зависимости, сценарий, тесты, критерии успеха и исключённые функции.

### L. Дорожная карта и файлы

Предложи порядок реализации и конкретные файлы для создания, изменения, объединения, переименования или сохранения.

## Формат ответа внешнего ИИ

```text
A. Executive assessment
B. Что оставить
C. Что изменить немедленно
D. BRAIM Core v0.1
E. Таблица сущностей
F. Таблица реестров
G. Validation Result schema
H. Три прототипа
I. Roadmap
J. Риски
K. Assumptions и Unknowns
L. Файлы к созданию/изменению
```

Каждую рекомендацию помечай `REQUIRED`, `PROPOSED` или `OPTIONAL` и указывай затрагиваемые L-слои и D-дисциплины.

---

# Part 2. BRAIM Project Identity

## Статус

- Версия: `0.1.0`
- Дата: 2026-09-28
- CDE: `SHARED`
- Public allowed: `true`
- Название: `BRAIM`
- Legacy name: `BAIM`

BRAIM — исследовательская и прототипная openBIM-платформа для формализации строительных требований, представления пространственных сущностей, генерации объёмно-планировочных решений, проверки данных и координации IFC/Archicad/дисциплинарных представлений.

BRAIM не является готовой нормативной системой, сертифицированным программным продуктом или заменой проектировщика/эксперта.

Рабочая семантика названия:

```text
Building Representation, Architecture and Information Model
```

Статус расшифровки: `WORKING`. Она может измениться без изменения `project_id`.

```yaml
project_id: braim
canonical_name: BRAIM
legacy_names: [BAIM]
name_status: CANONICAL_WORKING
expansion_status: WORKING
```

Основная идея:

```text
микрокернель
+ единая модель сущностей
+ нулевая шина
+ подключаемые специализированные ядра
+ дисциплинарные представления
+ контролируемая нормативная база
```

BRAIM не должен выдавать непроверенные AI-выводы за нормы, заменять официальные документы, скрывать происхождение данных, автоматически публиковать WIP-материалы, быть только генератором изображений или смешивать помещение, зону, проём и заполнение.

Основные направления: Entity Meta-Model, Normative Knowledge, Room/Zone/Niche Passport, Variant Strategy Engine, Plan-to-Form, Form-to-Plan, Geospatial and Point Cloud, IFC/IDS/BCF, Archicad Connector, Model View Registry, Validation and Verification, Control Center.

```text
BAIM → legacy project name
BRAIM → current canonical project name
BRAIN → rejected name; do not use
```

---

# Part 3. BRAIM Status and Open Questions

## Статус

- Версия: `0.1.0`
- Дата: 2026-09-28
- Release class: `CONCEPT_AND_PROTOTYPE`
- Public status: `DOCUMENTATION_PREVIEW`

## Уже сформулировано

- единая мультислойная сущность;
- семантические слои `L0–L15`;
- дисциплинарные представления `D0–D13`;
- единый `instance_id` во всех представлениях;
- источник истины и владелец атрибутов;
- provenance, validation и verification;
- микрокернельная архитектура, plugin manager, zero bus и оркестратор;
- различение помещения, зоны, ниши, проёма и заполнения;
- `PLAN_TO_FORM`, `FORM_TO_PLAN` и итерация планировка ↔ форма ↔ фасад;
- геодезия, облака точек, scan-to-BIM и шестигранный swept-loop дом.

## Пока не реализовано

```text
BRAIM Core runtime
Schema Registry
Attribute Registry
Claim/Evidence Registry
Model View Registry
CDE state machine
Dependency/impact engine
JSON Schema tests
Rules engine
Topology-first layout solver
Form-to-plan solver
Plan-to-form solver
Hexagonal form geometry engine
Point cloud processing implementation
Scan-to-BIM pipeline
IFC4X3 implementation
IDS/BCF integration
Archicad connector
Control Center
Public release automation
```

## Открытые вопросы

1. Утвердить английскую расшифровку BRAIM.
2. Утвердить окончательную структуру `L0–L15`.
3. Утвердить набор дисциплин `D0–D13`.
4. Решить, является ли IFC транспортом или внешним представлением.
5. Определить canonical storage.
6. Утвердить JSON Schema для сущности.
7. Утвердить источники численных требований.
8. Определить точную модель `Room` и `FunctionalRoom/FinishRoom`.
9. Выбрать геометрический движок.
10. Определить публичную лицензию.

Ничего не считать реализованным только потому, что это описано в драфте. Документированная идея имеет статус `SPECIFIED`, пока не существуют schema, implementation, test и validation report.

---

# Part 4. BRAIM AI Context Pack

## Версия

- Version: `0.1.0`
- Date: 2026-09-28
- Intended users: external AI systems, reviewers, developers and research agents

## Task

Analyze, extend or prototype BRAIM — a research and prototype openBIM platform for construction requirements, spatial entities, planning generation, validation, IFC/Archicad coordination and documentation.

Do not treat the repository as a completed product. Treat it as a structured set of drafts, hypotheses, schemas and prototypes.

## Core rules

- One concept ID and one instance ID across all representations.
- Semantic layers and discipline views are separate axes.
- Normative source, project requirement, AI inference and derived calculation are different evidence classes.
- `Room != Zone`; `Opening != Filling`; `Adjacency != Access`.
- Hard constraints reject candidates; soft constraints affect ranking.
- Unknown values remain unknown.
- Never invent a current normative requirement without an official source and applicability.
- Mark uncertain reasoning as `PROPOSED` or `NEEDS_REVIEW`.
- Preserve source passages and conflicts.
- Do not publish WIP materials as final specifications.

## Semantic layers

```text
L0-N normative
L1-C canonical
L2-F functional
L3-R requirements
L4-G geometry
L5-T topology
L6-X graph
L7-O openings
L8-I infrastructure
L9-B BIM/openBIM
L10-A authoring
L11-V generator
L12-Q quality
L13-D documentation
L14-E operation
L15-P provenance
```

## Discipline views

```text
D0-GEN coordination
D1-ARC architecture
D2-STR structure
D3-MEP engineering
D4-ELE electrical
D5-FIR fire safety
D6-SIT site
D7-ENV environment/daylight
D8-CST cost
D9-CON construction
D10-FM facility management
D11-INT interior
D12-GEO survey/geospatial/point clouds
D13-SEC information security
```

## Generation directions

```text
PLAN_TO_FORM:
requirements → topology → rooms/zones → geometry → openings → mass/facade

FORM_TO_PLAN:
form/volume → sections/usable fields → rooms/zones → openings → validation

ITERATIVE:
plan → form → facade → constraints → plan update
```

## Current highest-value tasks

- complete the BRAIM Entity Meta-Model;
- define Attribute Registry;
- define Claim/Evidence Registry;
- define Model View Registry;
- implement Core Validation Kernel;
- normalize terminology from TERMINY.xlsx;
- implement topology-first layout generation;
- implement geospatial/point-cloud data contracts;
- prototype the hexagonal swept-loop house;
- define public/private CDE synchronization.

---

# Part 5. Public Project Notice

BRAIM is an early-stage research and prototype project.

The public documentation contains working specifications, conceptual models, experimental schemas, algorithm prototypes and proposed workflows. It is not an official standard, certified BIM implementation, legal opinion or substitute for a qualified architect, engineer, surveyor, fire-safety specialist or other responsible professional.

Normative requirements must be checked against the current official edition, applicable jurisdiction, project type, mandatory lists and contract requirements before professional use.

AI-generated interpretations are hypotheses or derived claims unless explicitly marked as verified and approved. They must not be treated as primary normative sources.

The project may contain incomplete or intentionally unresolved concepts. Public materials are published for research, discussion, review, interoperability experiments and collaborative development.

---

# Part 6. Public CDE Manifest

```yaml
manifest:
  project_id: braim
  canonical_name: BRAIM
  release_name: BRAIM Public Documentation Preview
  release_version: 0.1.0
  cde_state: PUBLISHED
  visibility: PUBLIC
  maturity: CONCEPT_AND_PROTOTYPE
  normative_authority: false
  external_ai_analysis: ALLOWED
  production_use: NOT_RECOMMENDED
  last_reviewed_at: 2026-09-28

publication_policy:
  allowed_states: [PUBLISHED, RELEASED]
  required_flags:
    public_allowed: true
    security_scan: PASS
    secrets_scan: PASS
    license_check: PASS
    source_references_reviewed: true
  forbidden_content:
    - personal_data
    - client_models
    - credentials
    - private_project_data
    - full_protected_normative_copies
    - unreviewed_ai_claims_as_normative_facts
```

---

# Part 7. Attribute Registry

## Статус

- Версия: `0.1.0`
- Дата: 2026-09-28
- CDE: `SHARED`
- Назначение: единый реестр типизированных атрибутов BRAIM

Атрибут — это типизированное значение с владельцем, источником истины, статусом, единицей, ограничениями и правилами производности.

```text
Attribute = id + type + value + unit + owner + source + constraints + status
```

## Типы данных

```text
string | integer | decimal | boolean | enum | reference
list | set | map | quantity.length | quantity.area
quantity.volume | quantity.angle | quantity.time
geometry.point | geometry.line | geometry.polygon | geometry.solid
modularity.constraint
```

## Статусы значения

```text
UNKNOWN | ASSUMED | USER_DEFINED | SOURCE_DEFINED | AI_PROPOSED
DERIVED | VERIFIED | APPROVED | OUTDATED | CONFLICT
NOT_APPLICABLE | NEEDS_REVIEW
```

## Правила

1. Одинаковый `attribute_id` не должен иметь разные смыслы.
2. Фактическое значение не заменяет требуемое.
3. `null` означает неизвестность, а не ноль.
4. Единица измерения обязательна для quantity-типов.
5. Нормативное значение должно иметь источник.
6. Производный атрибут должен иметь формулу или список источников.
7. У каждого атрибута один владелец и список потребителей.
8. Изменение владельца истины создаёт impact analysis.
9. `AI_PROPOSED` не становится `APPROVED` автоматически.
10. Публичная версия не содержит приватных значений.

---

# Part 8. Claim and Evidence Registry

## Статус

- Версия: `0.1.0`
- Дата: 2026-09-28
- CDE: `SHARED`
- Назначение: хранить источники, факты, интерпретации, AI-выводы, расчёты и решения пользователей

BRAIM не смешивает первичный источник, факт извлечения, интерпретацию, AI-гипотезу, проектное решение и верифицированное правило.

## Типы утверждений

```text
SOURCE_FACT | EXTRACTED_FACT | MEASURED_FACT | CALCULATED_RESULT
AI_INTERPRETATION | PROJECT_DECISION | VALIDATED_CLAIM | CONFLICTING_CLAIM
```

## Статусы

```text
OBSERVED | EXTRACTED | INTERPRETED | PROPOSED | SUPPORTED
VERIFIED | APPROVED | REJECTED | OUTDATED | CONFLICTED
```

## Правила

1. AI-вывод никогда не маскируется под цитату нормы.
2. Любое утверждение, влияющее на генератор, имеет `claim_id`.
3. Утверждение, влияющее на валидатор, имеет проверенный источник или утверждённое решение.
4. Конфликтующие источники сохраняются оба.
5. Уверенность не заменяет верификацию.
6. Публичная публикация разрешена только для утверждений с `public_allowed: true`.
7. Изменение источника создаёт impact analysis.

---

# Part 9. Model View Registry

## Статус

- Версия: `0.1.0`
- Дата: 2026-09-28
- CDE: `SHARED`
- Назначение: описывать, что модельный вид показывает, скрывает и как оформляет

Модельный вид создаётся от результата документации:

```text
альбом/чертёж
→ назначение вида
→ дисциплина
→ фильтр сущностей
→ графические правила
→ марки и спецификации
```

Изоляция — не удаление объекта из модели, а управляемая проекция объекта в конкретном виде.

## Базовые виды

| ID | Вид | Дисциплина |
|---|---|---|
| `VIEW-ARC-PLAN` | Архитектурный план | D1-ARC |
| `VIEW-ARC-ELEVATION` | Фасад | D1-ARC |
| `VIEW-ARC-SECTION` | Разрез | D1-ARC |
| `VIEW-STR-PLAN` | Конструктивный план | D2-STR |
| `VIEW-MEP-VENT` | Вентиляция | D3-MEP |
| `VIEW-ELE-PLAN` | Электрика | D4-ELE |
| `VIEW-FIRE-EVAC` | Эвакуация | D5-FIR |
| `VIEW-SITE` | Генплан/участок | D6-SIT |
| `VIEW-SURVEY` | Существующее состояние | D12-GEO |
| `VIEW-CLOUD` | Облако точек | D12-GEO |
| `VIEW-IFC-COORDINATION` | Координационный IFC-вид | D0-GEN |
| `VIEW-ROOM-REPORT` | Паспорт/экспликация помещений | D1-ARC |

## Проверки вида

```text
view schema valid
all included entity types exist
filters are resolvable
source model version defined
no forbidden private objects included
annotations have sources
schedules are reproducible
```

Все отображаемые сущности сохраняют исходный `instance_id`.

---

# Part 10. CDE State Machine

## Статус

- Версия: `0.1.0`
- Дата: 2026-09-28
- CDE: `SHARED`
- Назначение: управляемые состояния документа, схемы, модели или утверждения

## Состояния

```text
WIP
SHARED
PUBLISHED
ARCHIVE
```

Дополнительные состояния review/release:

```text
DRAFT | IN_REVIEW | CHANGES_REQUESTED | APPROVED
RELEASED | RETIRED | BLOCKED | OUTDATED
```

## Разделение статусов

```yaml
cde_state: WIP|SHARED|PUBLISHED|ARCHIVE
review_state: DRAFT|IN_REVIEW|CHANGES_REQUESTED|APPROVED|REJECTED
release_state: NOT_RELEASED|RELEASE_CANDIDATE|RELEASED|RETIRED
visibility: PRIVATE|TEAM|CLIENT|PUBLIC
```

## Допустимые переходы

```text
WIP → SHARED
SHARED → WIP
SHARED → PUBLISHED
PUBLISHED → ARCHIVE
PUBLISHED_PRIVATE → PUBLISHED_PUBLIC
PUBLISHED → OUTDATED
OUTDATED → SHARED
```

## Условия публичной публикации

```text
public_allowed == true
security scan pass
secrets scan pass
license check pass
private data absent
full protected normative copies absent
external links reviewed
```

Публичная копия должна содержать только файлы, прошедшие манифест публикации. `PUBLISHED` не означает автоматически разрешённую публичную публикацию.

---

# Part 11. External Review Metadata

```yaml
bundle_id: BRAIM-EXTERNAL-AI-REVIEW-0.1
project_id: braim
canonical_name: BRAIM
source_repository: https://github.com/kirsunn/BRAIM-public
source_repository_status: public_documentation_preview
analysis_scope: documentation_and_architecture
normative_authority: false
production_readiness: not_established
unknown_values_policy: preserve_unknown
ai_claims_policy: proposed_until_verified
```

## Как использовать файл

1. Передать этот файл внешнему ИИ.
2. Попросить сначала подтвердить прочитанные разделы.
3. Получить архитектурный анализ по Part 1.
4. Не принимать рекомендации автоматически.
5. Перед внесением изменений сверить выводы с текущим репозиторием и проектными решениями.
