# Prompt for Independent AI Analysis of BRAIM

> **Провенанс:** документ передан автором проекта 2026-10-15 (существовал только в чате, в репозиториях отсутствовал). Это новейшая известная итерация концепции BRAIM — после Master Context 1.0 (2026-09-30) и BRAIM Concept v1.0 (2026-10-04). Учитывает выводы adversarial-ревью BAIM-LIMS v1.0 (см. `docs/history/BAIM-LIMS_Adversarial_Technical_Review_2026-09-30.md`).

---

Ты — независимый ведущий архитектор BIM/openBIM-платформ, специалист по IFC4.3, IDS, BCF, ISO 19650, геометрии, инженерным расчётам, нормативной проверке, knowledge graphs, генеративному проектированию и human-in-the-loop системам.

Тебе нужно критически проанализировать концепцию BRAIM. Не принимай текст ниже как готовую истину. Отделяй подтверждённые факты, проектные решения, гипотезы и неподтверждённые нормативные сведения.

## 1. Что такое BRAIM

BRAIM — IFC-first платформа воспроизводимой проверки BIM-моделей, экспертной работы, семантического перевода и постепенного генеративного проектирования.

BRAIM не должен начинаться как универсальный автономный проектировщик. Первый продукт:

```text
BRAIM Model Audit
```

Он должен:

```text
принять IFC
→ создать immutable snapshot
→ разрешить идентичность объектов
→ построить Canonical Model
→ выполнить проверки
→ показать findings на модели
→ сформировать BCF и отчёт
→ сохранить provenance и evidence
```

## 2. Zero Bus

Главный принцип:

> Что BRAIM принял, то он должен отразить: сохранить, понять, обогатить, проверить и либо выгрузить обратно, либо показать отчёт о потерях.

Zero Bus — активный канонический интеграционный слой. Ни одно ядро не получает сырой файл напрямую.

```text
Raw → Parsed → Canonical → Enriched → Controlled Export
```

Project Package:

```text
incoming/
parsed/
canonical/
enriched/
requirements/
derived/
exports/
evidence/
manifest.json
```

Обязательные инварианты:

1. Raw-файлы не перезаписываются.
2. Любое значение имеет provenance.
3. Конфликты не разрешаются молча.
4. Каждый экспорт связан со snapshot.
5. Потери round-trip отражаются в loss report.

## 3. Canonical Model

Canonical Model — нормализованное представление наблюдаемых данных и связей, а не полная замена Revit, Archicad, Renga или nanoCAD.

Основные сущности:

```text
Project
SourceArtifact
ImportRun
Snapshot
ModelElement
PropertyAssertion
ClassificationAssignment
Relation
GeometryRepresentation
IdentityLink
Finding
Evidence
Decision
```

Идентичность не является гарантированной простой цепочкой:

```text
BRAIM ID ↔ source ID ↔ IFC GUID
```

Нужны:

```text
braimEntityId
snapshotElementId
externalIdentity
```

Сопоставления:

```text
MATCHED
SPLIT_FROM
MERGED_FROM
POSSIBLE_MATCH
UNMATCHED
```

Неопределённое сопоставление не должно автоматически становиться фактом.

## 4. Semantic projections / worlds

Один канонический объект может иметь несколько согласованных представлений:

```text
Spatial Projection
Functional Projection
Engineering Projection
Structural Projection
Ergonomic Projection
Documentation Projection
Lifecycle Projection
Evidence Projection
```

Это не восемь независимых копий здания, а проекции одной канонической модели.

Пример кухни-столовой:

```text
Spatial:
  один физический CompoundSpace

Functional:
  Subzone Kitchen + Subzone Dining

Engineering:
  один HVAC/heating calculation volume

Ergonomic:
  storage → preparation → sink → preparation → hob → serving

Documentation:
  составное помещение с функциональными подзонами

Lifecycle:
  design → approved → construction → operation
```

## 5. Spatial ontology

```text
Physical Element
Spatial Unit
Functional Zone
Logical Zone
Calculation Zone
Aggregate
Connector
```

Основные отношения:

```text
CONTAINS
PART_OF
ADJACENT_TO
CONNECTED_BY
BOUNDED_BY
OPENS_TO
SERVES
SPANS
VERTICALLY_CONNECTED_TO
DERIVED_FROM
```

IFC alignment:

```text
IfcSpace          = пространство
IfcZone           = группировка spaces/zones без собственной геометрии
IfcSpatialZone    = пространственная/функциональная зона с возможной геометрией
IfcOpeningElement = проём / boundary connector
IfcDoor/Window    = заполнение проёма
IfcStair          = вертикальная физическая связь
IfcBuildingStorey = группа на уровне
```

Пример:

```text
IfcBuildingStorey
└── IfcZone — Apartment 42
    ├── IfcSpace — Living Room
    │   └── BRAIM Functional Subzone — Kitchen Niche
    ├── IfcSpace — Bedroom
    ├── IfcSpace — Bathroom
    └── IfcSpace — Internal Corridor
```

## 6. CompoundSpace and Subzone

```text
CompoundSpace: Kitchen-Dining
├── Subzone: Kitchen
└── Subzone: Dining
```

CompoundSpace — один физический и/или расчётный объём с несколькими функциональными трактовками.

Subzone:

- часть родительского CompoundSpace;
- может иметь физическую, условную или виртуальную границу;
- имеет функциональное назначение;
- не становится самостоятельным помещением автоматически;
- может иметь отдельные cost/documentation/ergonomic значения;
- может оставаться частью общего HVAC/heating volume.

Кухня-ниша рассматривается как функциональная подзона, а не как самостоятельный `IfcSpace`, если отсутствует физическая или нормативная сепарация.

## 7. IFC4.3 domain map

Классические домены IFC:

```text
Building Controls
HVAC
Electrical
Plumbing / Fire Protection
Structural Elements
Structural Analysis
Architecture
Construction Management
```

Они опираются на Resource, Core и Shared/Interoperability layers.

BRAIM использует их как дисциплинарную основу, но добавляет собственные домены:

```text
Spatial Semantics
Functional Planning
Ergonomics & Typology
Lifecycle
EIM / Maturity
Compliance
Identity / Provenance
Evidence
Cost & Resources
Human Decisions
```

IFC Domain Schema не равен BRAIM computational core. IFC даёт стандартизированные сущности; BRAIM строит проекции, вычисляет, проверяет, обогащает и оркестрирует.

## 8. Functional and ergonomic planning

Предложи отдельное ядро:

```text
Functional & Ergonomic Planning Gyrus
```

Оно должно работать с:

```text
Activity Graph
Access Graph
Adjacency Graph
Service Graph
Dependency Graph
Ergonomic Graph
```

Пример кухонной последовательности:

```text
Холодильник
→ подготовительная поверхность
→ мойка
→ подготовительная поверхность
→ плита
→ подача / столовая
```

Neufert/Architects' Data может быть одним источником справочных знаний по эргономике и типологии, но его рекомендации нельзя автоматически считать нормативами. Учитывай лицензирование и происхождение знаний.

## 9. Lifecycle and EIM

ЖЦ локален для любого scope: project, site, building, block, section, storey, apartment, room, subzone, system, element.

```text
LC:P=DESIGN/S=CONCEPT/E=VALIDATE/M=VALIDATED
```

EIM:

```text
G2-I1-C010-A2
```

EIM — контекстное утверждение:

```text
Scope
+ Lifecycle Context
+ Intended Use
+ Required Profile
+ Actual Profile
+ Gate Results
+ Evidence
```

Переход ЖЦ:

```text
Current State
+ Target State
+ Required EIM
+ Validation Gates
+ Evidence
+ Approval
→ New Snapshot / New Lifecycle State
```

Состояния проверки:

```text
PASS
FAIL
UNKNOWN
INCOMPLETE
NOT_APPLICABLE
STALE
```

## 10. Validation stack

Раздели:

```text
IFC schema validation
IDS validation
Geometry rules
Spatial rules
Quantity / TEP rules
Classification rules
Regulatory rules
Heuristics
Expert review
```

IDS — информационный слой требований, не полный нормативный движок.

Не принимай московский профиль, RUS_* атрибуты, RusSet_*, коды МССК, допуски или версии IFC как подтверждённые без официальных первоисточников.

## 11. Первый продукт и MVP

MVP-0:

```text
IFC + IDS
→ Raw
→ Parsed
→ Canonical
→ requirements snapshot
→ manifest
```

MVP-1:

```text
IFC
→ immutable snapshot
→ canonical model
→ 10–20 детерминированных checks
→ minimal viewer
→ findings
→ BCF
→ HTML report
→ evidence manifest
```

Тестовый корпус: 8–12 моделей, включая корректные, геометрические ошибки, ошибки свойств, ошибки spatial structure, два экспорта одной модели, крупную модель и обезличенные реальные модели.

Не делать в MVP-1:

```text
генеративный проектировщик
все native connectors
автоматические конструктивные/пожарные/legal conclusions
полный Moscow AGR verified profile
собственный IFC parser
собственное BRep ядро
```

## 12. Твоя задача

Подготовь независимый критический документ.

### A. Критика концепции

- что технически реалистично;
- что является настоящей инновацией;
- где слишком много метафор;
- какие понятия дублируются;
- где Canonical Model может стать чрезмерно широкой;
- нужен ли Multi-Domain Canonical Model;
- оправдана ли модель семантических проекций;
- корректно ли разделены IfcSpace, IfcZone, IfcSpatialZone, CompoundSpace, Subzone и LogicalZone.

### B. IFC-аудит

Проверь:

- точный состав IFC4.3 доменов;
- корректность описания Resource/Core/Shared/Domain layers;
- уместность маппинга IFC domains → BRAIM cores;
- ограничения IFC для функциональных зон и эргономики;
- где нужен BRAIM extension;
- где может возникнуть потеря семантики.

### C. Ontology / model design

Предложи:

- сущности;
- типы связей;
- правила наследования;
- разные проекции одной сущности;
- модель Composite Space / Subzone;
- представление квартиры, этажа, секции, здания и комплекса;
- пример JSON Schema или TypeScript.

### D. Lifecycle and EIM

Проверь:

- разделение phase/stage/step/status;
- scoped lifecycle;
- composite/mixed states;
- EIM как gate перехода;
- `G-I-C-A`;
- snapshot graph;
- условия перехода между состояниями;
- корректность `UNKNOWN`, `INCOMPLETE`, `STALE`.

### E. Functional and ergonomic gyrus

Оцени:

- нужен ли отдельный домен;
- как строить activity/adjacency/access graphs;
- как использовать Neufert и другие справочники;
- как отделить рекомендации от норм;
- как связать функциональный слой с геометрией и инженерными расчётами.

### F. Практический MVP

Предложи:

- первую тестовую модель квартиры;
- какие файлы использовать;
- какие 10 проверок реализовать;
- какие статусы показать;
- как построить первый viewer;
- критерии готовности;
- что должно быть ручным.

### G. Риски

Таблица:

```text
risk
probability
impact
indicator
mitigation
fallback
```

Обязательно рассмотрите:

- слишком широкую Canonical Model;
- рассинхронизацию проекций;
- неправильное объединение пространства и функций;
- потерю семантики IFC;
- ложные нормативные выводы;
- неподтверждённые источники;
- copyright/licensing Neufert;
- чрезмерную сложность EIM;
- слишком большой MVP.

### H. Final recommendation

Дай:

1. список решений, которые следует принять;
2. список идей, которые нужно отложить;
3. список терминов, которые нужно переименовать;
4. рекомендуемую архитектуру MVP;
5. конкретный первый пользовательский сценарий;
6. список тестов;
7. 20 скрытых предположений;
8. 10 противоречий или неоднозначностей;
9. упрощённую версию BRAIM на 8–12 недель.

## 13. Требования к ответу

- Не рекламируй.
- Отделяй факты IFC/IDS от проектных решений BRAIM.
- Проверяй стандарты по официальным источникам.
- Не объявляй московские требования подтверждёнными без первичных документов.
- Не считай LLM источником нормативной истины.
- Не предлагай микросервисы без необходимости.
- Отдельно указывай, где нужен человеческий эксперт.
- Если понятие «мультимировая модель» полезно как метафора, предложи точный технический термин.
- В конце дай компактное решение: что строить первым.
