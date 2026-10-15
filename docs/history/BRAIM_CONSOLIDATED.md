# BRAIM — Consolidated Project Document v0.1.0

> Единый документ, объединяющий все решения, обсуждённые в серии чатов.
> Дата: 2026-10-01. Статус: CONCEPT_AND_PROTOTYPE.

---

## Содержание

1. [Идентичность проекта](#1-идентичность-проекта)
2. [Архитектурные принципы](#2-архитектурные-принципы)
3. [Семантические слои и дисциплины](#3-семантические-слои-и-дисциплины)
4. [Метамодель сущностей Core v0.1](#4-метамодель-сущностей-core-v01)
5. [ConstraintProfile](#5-constraintprofile)
6. [ProjectConfig и AnalyticalLayout](#6-projectconfig-и-analyticallayout)
7. [Attribute Registry](#7-attribute-registry)
8. [Claim/Evidence Registry](#8-claimevidence-registry)
9. [Validation Kernel (V0–V2)](#9-validation-kernel-v0v2)
10. [CDE State Machine](#10-cde-state-machine)
11. [Model View Registry](#11-model-view-registry)
12. [Интеграционные границы](#12-интеграционные-границы)
13. [IFC-экспорт](#13-ifc-экспорт)
14. [IDS-профиль](#14-ids-профиль)
15. [Три первых прототипа](#15-три-первых-прототипа)
16. [Дорожная карта](#16-дорожная-карта)
17. [Известные ограничения](#17-известные-ограничения)
18. [Структура файлов](#18-структура-файлов)
19. [Ключевые правила и инварианты](#19-ключевые-правила-и-инварианты)
20. [Глоссарий различий](#20-глоссарий-различий)

---

## 1. Идентичность проекта

```yaml
project_id: braim
canonical_name: BRAIM
legacy_names: [BAIM]
name_status: CANONICAL_WORKING
expansion_status: WORKING
working_expansion: "Building Representation, Architecture and Information Model"
release_class: CONCEPT_AND_PROTOTYPE
public_status: DOCUMENTATION_PREVIEW
normative_authority: false
production_use: NOT_RECOMMENDED
```

BRAIM — исследовательская и прототипная openBIM-платформа для:
- формализации строительных требований;
- представления пространственных сущностей;
- генерации планировочных и объёмных вариантов;
- проверки модели и требований;
- координации IFC/IDS/BCF/Archicad;
- работы с геодезией, облаками точек и существующим состоянием.

**BRAIM не является** готовой нормативной системой, сертифицированным продуктом
или заменой проектировщика.

---

## 2. Архитектурные принципы

### Инварианты (REQUIRED, L0-N, D0-GEN)

1. **IFC-first** — IFC является первичным входом; всё остальное — надстройка.
2. **Immutable snapshot** — raw-данные не перезаписываются.
3. **Provenance для каждого значения** — источник, timestamp, actor.
4. **Конфликты не разрешаются молча** — сохраняются оба значения.
5. **Экспорт связан со snapshot** — loss report при round-trip.
6. **Один instance_id** во всех дисциплинарных представлениях.
7. **Hard constraints отвергают кандидаты**; soft constraints влияют на ранжирование.
8. **Unknown остаётся unknown** — не превращается в false или zero.
9. **AI-вывод не маскируется под норму** — `AI_PROPOSED` не становится `VERIFIED` автоматически.
10. **Публикация WIP запрещена** — только `PUBLISHED` через манифест.

### Принципы единиц (REQUIRED, L1-C, D1-ARC)

- Координаты и линейные размеры: `int mm` без суффикса (`6000`, не `6.0 м`).
- Площади: `float m2`.
- `grid_quantum_mm = 100`.
- `rounding_policy = reject` (нарушение кратности → ERROR).
- `max_planning_module_mm = 10000` — только для boundary bbox.
- Размеры в осях здания — в мм.
- Геодезия/генплан — метры с десятичной точностью (`15.22`).

---

## 3. Семантические слои и дисциплины

### Семантические слои L0–L15

```
L0-N  normative
L1-C  canonical
L2-F  functional
L3-R  requirements
L4-G  geometry
L5-T  topology
L6-X  graph
L7-O  openings
L8-I  infrastructure
L9-B  BIM/openBIM
L10-A authoring
L11-V generator
L12-Q quality
L13-D documentation
L14-E operation
L15-P provenance
```

### Дисциплины D0–D13

```
D0-GEN  coordination
D1-ARC  architecture
D2-STR  structure
D3-MEP  engineering
D4-ELE  electrical
D5-FIR  fire safety
D6-SIT  site
D7-ENV  environment/daylight
D8-CST  cost
D9-CON  construction
D10-FM  facility management
D11-INT  interior
D12-GEO  survey/geospatial/point clouds
D13-SEC  information security
```

### Используемые в MVP v0.1

- **Слои:** L0-N, L1-C, L2-F, L4-G, L5-T, L9-B, L15-P.
- **Дисциплины:** D0-GEN, D1-ARC, D4-ELE (для аудита).

### Представление в сущности

Каждая сущность BRAIM несёт две независимые оси:
```json
{
  "semantic_layer": "L1-C",
  "discipline_view": "D1-ARC"
}
```

---

## 4. Метамодель сущностей Core v0.1

| entity_type | Обязательные ID | Обязательные атрибуты | Владелец истины | Статусы | Unknown | Derived |
|---|---|---|---|---|---|---|
| `Project` | `braim_id` | `name`, `schema_version`, `created_at` | BRAIM | DRAFT, ACTIVE, ARCHIVED | — | — |
| `Boundary` | `braim_id`, `project_id` | `width_mm`, `height_mm` | ProjectConfig | DEFINED | `polygon` | `area_m2` |
| `RoomConfig` | `braim_id`, `project_id` | `id`, `type`, `min_area_m2`, `min_dimension_mm` | ProjectConfig | REQUESTED | `target_area_m2` | — |
| `AnalyticalRoom` | `braim_id`, `layout_id`, `config_id` | `x_mm`, `y_mm`, `width_mm`, `height_mm` | Generator | PLACED, REJECTED | — | `computed_area_m2` |
| `ForbiddenZone` | `braim_id`, `layout_id` | `x_mm`, `y_mm`, `width_mm`, `height_mm`, `type` | ProjectConfig | DEFINED | — | — |
| `ConstraintProfile` | `braim_id`, `project_id` | `grid_quantum_mm`, `rounding_policy`, `max_planning_module_mm` | BRAIM config | ACTIVE | — | — |
| `ValidationIssue` | `braim_id`, `report_id` | `rule_id`, `severity`, `elements`, `message` | ValidationEngine | OPEN, RESOLVED | `geometry` | — |
| `ValidationReport` | `braim_id`, `layout_id` | `status`, `summary`, `issues[]` | ValidationEngine | VALID, VALID_WITH_WARNINGS, INVALID | — | `summary` |

---

## 5. ConstraintProfile

```json
{
  "schema_version": "0.1.0",
  "units": {
    "length": "mm",
    "area": "m2",
    "coordinate_type": "int"
  },
  "solver_constraints": {
    "grid_quantum_mm": 100,
    "rounding_policy": "reject",
    "max_planning_module_mm": 10000,
    "min_corridor_width_mm": 1200
  },
  "v0_rules": [
    "CONFIG-JSON-001",
    "CONFIG-PROFILE-001",
    "CONFIG-BOUNDARY-001",
    "CONFIG-ROOMS-001",
    "CONFIG-ID-001",
    "CONFIG-GRID-001",
    "CONFIG-MAXSIDE-001"
  ]
}
```

---

## 6. ProjectConfig и AnalyticalLayout

### Разделение (REQUIRED, L1-C, D1-ARC)

- **ProjectConfig** — проектные требования (id, type, area, min_dimension).
  Не содержит геометрии (x/y/width/height).
- **AnalyticalLayout** — сгенерированная геометрия (координаты, размеры, полигоны).
  Не содержит проектных требований.

### Пример ProjectConfig

```json
{
  "schema_version": "0.1.0",
  "project_id": "test_10000x7000",
  "boundary": {
    "width_mm": 10000,
    "height_mm": 7000
  },
  "room_program": [
    {
      "id": "living_room",
      "type": "living_room",
      "target_area_m2": 20.0,
      "min_area_m2": 14.0,
      "min_dimension_mm": 3000,
      "max_dimension_mm": 6000,
      "max_aspect_ratio": 4.0,
      "requires_facade": true,
      "is_wet_room": false,
      "is_private": false
    }
  ],
  "total_target_area_m2": 56.0
}
```

### Пример AnalyticalLayout

```json
{
  "schema_version": "0.1.0",
  "layout_id": "uuid-v7",
  "rooms": [
    {
      "id": "living",
      "config_id": "living_room",
      "x_mm": 0,
      "y_mm": 0,
      "width_mm": 4000,
      "height_mm": 4000,
      "declared_area_m2": 16.0
    }
  ],
  "forbidden_zones": [],
  "entrance_offset_mm": 0,
  "entrance_width_mm": 900,
  "walls": [],
  "doors": []
}
```

---

## 7. Attribute Registry

### Минимальная схема атрибута (REQUIRED, L1-C, D0-GEN)

```json
{
  "attr_id": "room.net_floor_area",
  "entity_type": "AnalyticalRoom",
  "name": "NetFloorArea",
  "type": "decimal",
  "unit": "m2",
  "origin": "DERIVED",
  "status": "VERIFIED",
  "owner": "BRAIM Core",
  "version": "0.1.0",
  "ifc_mapping": "Pset_SpaceCommon.NetFloorArea"
}
```

### Типы данных

```
string | integer | decimal | boolean | enum | reference
list | set | map | quantity.length | quantity.area
quantity.volume | quantity.angle | quantity.time
geometry.point | geometry.line | geometry.polygon | geometry.solid
modularity.constraint
```

### Статусы значения

```
UNKNOWN | ASSUMED | USER_DEFINED | SOURCE_DEFINED | AI_PROPOSED
DERIVED | VERIFIED | APPROVED | OUTDATED | CONFLICT
NOT_APPLICABLE | NEEDS_REVIEW
```

### Правила

1. Одинаковый `attribute_id` не имеет разные смыслы.
2. Фактическое значение не заменяет требуемое.
3. `null` означает неизвестность, не ноль.
4. Единица обязательна для quantity-типов.
5. Нормативное значение имеет источник (`source_ref`).
6. Производный атрибут имеет формулу или список источников.
7. Один владелец, список потребителей.
8. Изменение владельца → impact analysis.
9. `AI_PROPOSED` не становится `APPROVED` автоматически.
10. Публичная версия не содержит приватных значений.

### Примеры атрибутов

| attr_id | type | unit | origin | ifc_mapping |
|---|---|---|---|---|
| `boundary.width` | integer | mm | USER_DEFINED | — |
| `room.net_floor_area` | decimal | m2 | DERIVED | Pset_SpaceCommon.NetFloorArea |
| `room.min_dimension` | integer | mm | USER_DEFINED | — |
| `room.occupancy_type` | string | — | SOURCE_DEFINED | Pset_SpaceCommon.Reference |
| `room.ergonomic_clearance` | decimal | mm | AI_PROPOSED | — |
| `zone.fire_rating` | string | — | SOURCE_DEFINED | Pset_ZoneCommon.FireRating |
| `door.clear_width` | integer | mm | MEASURED | Pset_DoorCommon.ClearWidth |
| `wall.fire_resistance` | boolean | — | CALCULATED | Pset_WallCommon.FireRating |

---

## 8. Claim/Evidence Registry

### Цепочка provenance (REQUIRED, L15-P, D0-GEN)

```
Source → Activity → Claim → Rule → Validation Result → Decision
```

### Типы утверждений

```
SOURCE_FACT | EXTRACTED_FACT | MEASURED_FACT | CALCULATED_RESULT
AI_INTERPRETATION | PROJECT_DECISION | VALIDATED_CLAIM | CONFLICTING_CLAIM
```

### Статусы

```
OBSERVED | EXTRACTED | INTERPRETED | PROPOSED | SUPPORTED
VERIFIED | APPROVED | REJECTED | OUTDATED | CONFLICTED
```

### Правила

1. AI-вывод никогда не маскируется под цитату нормы.
2. Любое утверждение, влияющее на генератор, имеет `claim_id`.
3. Утверждение, влияющее на валидатор, имеет проверенный источник.
4. Конфликтующие источники сохраняются оба.
5. Уверенность не заменяет верификацию.
6. Публичная публикация — только `public_allowed: true`.
7. Изменение источника → impact analysis.

### Пример цепочки

```
Source: СП 54.13330.2016, п. 5.2 (гипотетический)
  ↓
Activity: извлечение минимальной площади спальни
  ↓
Claim: "Минимальная площадь спальни — 8 м2" (SOURCE_FACT, VERIFIED)
  ↓
Rule: V1-MIN-AREA-001: room.area_m2 >= 8.0 для type=bedroom
  ↓
Validation Result: room "bedroom_01" area=7.5 → FAIL (ERROR)
  ↓
Decision: отклонить вариант, вернуть в генератор
```

---

## 9. Validation Kernel (V0–V2)

### Уровни проверок

| Уровень | Что проверяет | Статус MVP |
|---|---|---|
| **V0 Config** | Структура конфига, presence полей, grid alignment, max side, ID уникальность | ✅ реализован, 45 тестов |
| **V1 Geometry** | Пересечения, выход за boundary, forbidden zones, min dimension, aspect ratio | ❌ создать |
| **V2 Functional** | BFS reachability от входа, required/forbidden adjacency | ❌ создать |
| V3 Construction | Стены, двери, окна, конструктив | 🔲 будущее |
| V4 IFC/IDS | Валидация IFC по IDS через ifctester | 🔲 будущее |
| V5 Export | Консистентность IFC/SVG/JSON | 🔲 будущее |

### V0 Правила (реализованы)

| Rule ID | Описание | Severity |
|---|---|---|
| `CONFIG-JSON-001` | Конфиг — валидный JSON-объект | ERROR |
| `CONFIG-PROFILE-001` | Constraint profile существует, parsable, valid | ERROR |
| `CONFIG-BOUNDARY-001` | Boundary присутствует, width_mm и height_mm заданы | ERROR |
| `CONFIG-ROOMS-001` | room_program непустой | ERROR |
| `CONFIG-ID-001` | ID комнат уникальны | ERROR |
| `CONFIG-GRID-001` | Координаты кратны grid_quantum_mm (при reject → ERROR) | ERROR |
| `CONFIG-MAXSIDE-001` | max(boundary.width, boundary.height) <= 10000 | ERROR |
| `LAYOUT-ROOM-FIELDS-001` | Сгенерированная комната имеет геометрию | ERROR |

### Статусы

- `INVALID` — есть хотя бы один ERROR.
- `VALID_WITH_WARNINGS` — ERROR нет, но есть WARNING.
- `VALID` — нет ERROR и WARNING.

### Hard vs Soft

| Тип | Пример | Нарушение |
|---|---|---|
| Hard | Комната внутри boundary | ERROR → INVALID |
| Hard | Нет пересечений комнат | ERROR → INVALID |
| Hard | Площадь ≥ min_area | ERROR → INVALID |
| Hard | Доступ от входа ко всем комнатам | ERROR → INVALID |
| Soft | Предпочтительная смежность | WARNING |
| Soft | Минимизация остаточных площадей | INFO |

### Обработка UNKNOWN

- UNKNOWN не превращается в `false` или `0`.
- Для hard constraint: UNKNOWN → ERROR с `actual=null`, `expected="value required"`.
- Для soft constraint: UNKNOWN → WARNING с суффиксом `-UNKNOWN`.

### ValidationReport (JSON)

```json
{
  "report_id": "uuid-v7",
  "layout_id": "uuid-v7",
  "status": "INVALID",
  "summary": { "total": 2, "errors": 2, "warnings": 0, "info": 0 },
  "issues": [
    {
      "rule_id": "V1-OVERLAP-001",
      "severity": "ERROR",
      "elements": ["room_living", "room_kitchen"],
      "actual": { "overlap_area_m2": 1.5 },
      "expected": { "overlap_area_m2": 0.0 },
      "message": "Rooms overlap by 1.5 m2",
      "suggestion": "Adjust room positions",
      "geometry": { "type": "Polygon", "coordinates": [] }
    }
  ],
  "provenance": {
    "validator_version": "0.1.0",
    "validated_at": "2026-10-01T08:00:00+03:00",
    "constraint_profile_ref": "configs/constraints/mvp_concept_100.json"
  }
}
```

### 5 примеров проверок (без нормативных чисел)

| rule_id | Уровень | Проверка | Hard/Soft | При неудаче |
|---|---|---|---|---|
| `V0-GRID-001` | V0 | Координаты кратны grid_quantum_mm | Hard | ERROR |
| `V1-OVERLAP-001` | V1 | Пересечение полигонов = 0 | Hard | ERROR |
| `V1-CONTAINMENT-001` | V1 | Полигон внутри boundary | Hard | ERROR |
| `V1-FORBIDDEN-001` | V1 | Пересечение с forbidden zone = 0 | Hard | ERROR |
| `V2-REACHABILITY-001` | V2 | BFS от входа достигает все комнаты | Hard | ERROR |

### IFC-экспорт

- `can_export_ifc()` разрешает экспорт только при `status == VALID`.
- При `INVALID` или `VALID_WITH_WARNINGS` — блокируется.
- `override=True` — явная пользовательская команда для обхода.

---

## 10. CDE State Machine

### Состояния (REQUIRED, L12-Q, D13-SEC)

```
WIP → SHARED → PUBLISHED → ARCHIVE
```

### 4-осевая модель

```yaml
cde_state: WIP|SHARED|PUBLISHED|ARCHIVE
review_state: DRAFT|IN_REVIEW|CHANGES_REQUESTED|APPROVED|REJECTED
release_state: NOT_RELEASED|RELEASE_CANDIDATE|RELEASED|RETIRED
visibility: PRIVATE|TEAM|CLIENT|PUBLIC
```

### Переходы

```
WIP → SHARED
SHARED → WIP
SHARED → PUBLISHED
PUBLISHED → ARCHIVE
PUBLISHED_PRIVATE → PUBLISHED_PUBLIC
PUBLISHED → OUTDATED
OUTDATED → SHARED
```

### Условия публичной публикации

```
public_allowed == true
security scan PASS
secrets scan PASS
license check PASS
private data absent
full protected normative copies absent
external links reviewed
```

---

## 11. Model View Registry

### Принцип (REQUIRED, L9-B, D0-GEN)

Изоляция — не удаление объекта из модели, а управляемая проекция.
Все отображаемые сущности сохраняют исходный `instance_id`.

### Базовые виды

| ID | Вид | Дисциплина |
|---|---|---|
| VIEW-ARC-PLAN | Архитектурный план | D1-ARC |
| VIEW-ARC-ELEVATION | Фасад | D1-ARC |
| VIEW-ARC-SECTION | Разрез | D1-ARC |
| VIEW-STR-PLAN | Конструктивный план | D2-STR |
| VIEW-MEP-VENT | Вентиляция | D3-MEP |
| VIEW-ELE-PLAN | Электрика | D4-ELE |
| VIEW-FIRE-EVAC | Эвакуация | D5-FIR |
| VIEW-SITE | Генплан | D6-SIT |
| VIEW-SURVEY | Существующее состояние | D12-GEO |
| VIEW-CLOUD | Облако точек | D12-GEO |
| VIEW-IFC-COORDINATION | Координационный IFC-вид | D0-GEN |
| VIEW-ROOM-REPORT | Паспорт помещений | D1-ARC |

### Проверки вида

- view schema valid
- all included entity types exist
- filters are resolvable
- source model version defined
- no forbidden private objects included
- annotations have sources
- schedules are reproducible

---

## 12. Интеграционные границы

| Сущность | Категория | Пояснение |
|---|---|---|
| IFC | Внешнее представление / адаптер | Транспорт, не ядро. Не решено: транспорт или внешняя модель |
| IDS | Внешний стандарт требований | Валидация через ifctester — адаптер |
| BCF | Формат обмена замечаниями | Экспорт — адаптер |
| Archicad | Адаптер | Отложить до v0.3 |
| Point clouds | Внешние данные | Отложить до v0.2 |
| Geospatial | Внешние данные | Отложить до v0.2 |
| Model View Registry | Внутренний компонент | Часть BRAIM Core |

---

## 13. IFC-экспорт

### Скрипт create_valid_ifc.py

Создаёт минимальную IFC4-модель:
- IfcProject (Name="BRAIM Apartment")
- IfcSite (Name="Test Site")
- IfcBuilding (Name="Test Building")
- IfcBuildingStorey (Name="Ground Floor")
- IfcSpace (Name="Living Room") + Pset_SpaceCommon.Reference = "LIV-001"
- IfcWall (Name="Wall 001")
- IfcDoor (Name="Door 001")
- IfcWindow (Name="Window 001")

Иерархия: IfcProject → IfcSite → IfcBuilding → IfcBuildingStorey.

Использует IfcOpenShell API (`ifcopenshell.api.run`).

### Ограничения

- Нет 3D-геометрии (только сущности с containment).
- Нет ObjectPlacement (элементы в начале координат).
- Только IFC4.
- `ifcopenshell.geom` требует C++-библиотек.

---

## 14. IDS-профиль

### ids/apartment_mvp.ids (PROPOSED, L9-B, D0-GEN)

Минимальный набор 5–10 правил:
- IfcProject с Name
- IfcSite с Name
- IfcBuilding с Name
- IfcBuildingStorey с Name
- IfcSpace с Name
- IfcSpace с Pset_SpaceCommon.Reference
- IfcWall с Name
- IfcDoor с Name
- IfcWindow с Name

---

## 15. Три первых прототипа

### Прототип 1: Constraint-Based Floorplan Validator (REQUIRED)

- **Цель:** JSON Layout → V0+V1+V2 → SVG-оверлей
- **Вход:** ProjectConfig, AnalyticalLayout, ConstraintProfile
- **Выход:** ValidationReport (JSON), SVG с подсветкой
- **Зависимости:** shapely, jsonschema
- **Тесты:** overlap, out_of_boundary, forbidden zone, unreachable, duplicate ID, grid, corridor < 1200, max side > 10000
- **Не реализуется:** CP-SAT, IFC, двери/окна, UI

### Прототип 2: Topology-First Graph Builder (REQUIRED)

- **Цель:** Adjacency rules → граф → проверка связности
- **Вход:** ProjectConfig с adjacency rules
- **Выход:** DOT-граф, JSON матрица смежности
- **Зависимости:** networkx (или ручной BFS/DFS)
- **Тесты:** валидный граф, противоречивые правила, недостижимая комната
- **Не реализуется:** геометрия, IFC, UI

### Прототип 3: IFC → IDS Audit (PROPOSED)

- **Цель:** IFC → IDS → BCF + JSON-отчёт
- **Вход:** valid.ifc, apartment_mvp.ids
- **Выход:** ValidationReport, BCF-файл
- **Зависимости:** ifcopenshell, ifctester
- **Тесты:** валидный IFC, IFC без Pset, IFC без IfcProject
- **Не реализуется:** геометрические проверки, генерация

---

## 16. Дорожная карта

| Phase | Длительность | Деливераблы | L/D |
|---|---|---|---|
| Phase 0 — Schemas | 1 нед | JSON Schemas со schema_version | L0-N, D0 |
| Phase 1 — Core entities | 1 нед | instance_id, Attribute Registry, Claim/Evidence | L1-C, D0 |
| Phase 2 — Validation V0+V1+V2 | 2 нед | V0 готов; V1 (geometry); V2 (access) | L2-F, D4 |
| Phase 3 — Topology prototype | 2 нед | Functional graph, adjacency, DOT | L5-T, D1 |
| Phase 4 — Model views & CDE | 1 нед | ModelViewRegistry, CDE State Machine | L9-B, D0 |
| Phase 5 — IFC/IDS/BCF | 2 нед | IFC import, IDS validation, BCF export | L9-B, D0 |
| Phase 6 — Geospatial & clouds | 2 нед | GeospatialAdapter, PointCloudAdapter | L10-A, D12 |
| Phase 7 — Archicad connector | 2 нед | ArchicadAdapter, двусторонний обмен | L10-A, D1 |

### Порядок обоснован

- Схемы раньше кода (без версий миграции невозможны).
- Валидация раньше генерации (нельзя генерировать непроверяемое).
- Топология раньше геометрии (граф дешевле solver).
- IFC/IDS после Core (адаптер, не ядро).
- Archicad последним (vendor lock-in).

---

## 17. Известные ограничения

1. Реализован только V0. V1–V5 — запланированы.
2. JSON Schema проверяется программно через jsonschema.
3. Нет проверки вложенности комнат внутри boundary (это V1).
4. CONFIG-GRID-001 проверяет boundary и rooms, но не doors (отложено).
5. Нет CP-SAT, дверей, UI — намеренно.
6. ifcopenshell не импортируется в V0–V2 — намеренно.
7. ifcopenshell.geom требует C++-библиотек.
8. Нет тестов на произвольные полигональные контуры.
9. README.md пуст — требует заполнения.
10. Лицензия не указана.

---

## 18. Структура файлов

```
braim/
├── BRAIM_CONSOLIDATED.md          ← этот документ
├── create_valid_ifc.py             ← генератор IFC4
├── configs/
│   └── constraints/
│       └── mvp_concept_100.json    ← профиль ограничений
├── schemas/
│   ├── constraint_profile.schema.json
│   ├── attribute_registry.schema.json
│   ├── claim_evidence.schema.json
│   ├── validation_report.schema.json
│   └── source_registry.schema.json
├── ids/
│   └── apartment_mvp.ids           ← IDS-профиль
├── src/
│   └── braim_floorplan_generator/
│       ├── __init__.py
│       ├── constraints_profile.py
│       ├── analytical_model.py
│       ├── validation/
│       │   ├── __init__.py
│       │   ├── models.py           ← Severity, ValidationIssue, ValidationReport
│       │   ├── config_validator.py  ← V0ConfigValidator
│       │   ├── engine.py           ← ValidationEngine
│       │   ├── v1_geometry.py      ← V1 (создать)
│       │   └── v2_functional.py     ← V2 (создать)
│       └── core/                   ← (создать)
│           ├── instance_id.py
│           ├── attribute_registry.py
│           ├── claim_evidence.py
│           └── provenance.py
└── tests/
    ├── fixtures/
    │   └── valid_project_10000x7000.json
    ├── test_constraint_profile.py
    ├── test_validation_v0.py
    ├── test_validation_v1.py        ← (создать)
    └── test_validation_v2.py        ← (создать)
```

---

## 19. Ключевые правила и инварианты

1. **IFC создаётся только при VALID** (или `override=True`).
2. **CONFIG-GRID-001 → ERROR** при `rounding_policy = "reject"`.
3. **CONFIG-MAXSIDE-001** — только для boundary bbox, не для комнат.
4. **ProjectConfig ≠ AnalyticalLayout** — два отдельных метода валидации.
5. **Stable IDs** — `braim_id` (UUID v7) для всех сущностей.
6. **Не выдумывать нормативные числа** — всё с `source_ref`.
7. **ifcopenshell запрещён в V0–V2** — аналитическая валидация независима.
8. **Legacy-модули не трогать** — generator.py, functional_layout.py, old validator.py.

---

## 20. Глоссарий различий

| Пара | Различие | L/D |
|---|---|---|
| Room ≠ Zone | Room — физический объём с геометрией; Zone — группировка без собственной геометрии | L2-F, D1 |
| Zone ≠ Niche | Zone — функциональная область; Niche — подзона внутри Room без физической сепарации | L2-F, D1 |
| Opening ≠ Filling | Opening — пустота в стене (IfcOpeningElement); Filling — элемент, заполняющий проём (IfcDoor/IfcWindow) | L7-O, D1 |
| Adjacency ≠ Access | Adjacency — геометрическое касание; Access — наличие пути через дверь/проём | L5-T, D1 |
| Requirement ≠ Constraint | Requirement — что должно быть (IDS); Constraint — параметр solver (CP-SAT) | L3-R, D4 |
| Normative fact ≠ Project decision | Normative fact — из официального документа; Project decision — выбор проектировщика | L0-N, D0 |
| AI interpretation ≠ Verified rule | AI interpretation — AI_PROPOSED, не блокирует; Verified rule — VERIFIED, может блокировать | L15-P, D4 |

---

## Конец документа

BRAIM_CONSOLIDATED.md — v0.1.0 — 2026-10-01
