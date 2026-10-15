# BRAIM Layer Model

> **Провенанс:** передано автором проекта 2026-10-15 (существовало только в чате, в репозиториях отсутствовало); зафиксировано в репозитории как есть — v0.1.0 draft, на обсуждение.
> **Известное расхождение:** `BRAIM_AI_CONTEXT_PACK.md` использует старые коды `L11-V generator` и `L14-E operation`; настоящий документ вводит `L11-INT Interior/Finish` и `L14-E Energy/Environmental`. Канон — настоящий документ; Context Pack подлежит синхронизации.

## Статус документа

Версия: 0.1.0

Статус: Draft / концептуальная спецификация

Дата: 2026-10-15

Название: BRAIM Layer Model

Назначение: определить, что такое слой в BRAIM, как слой связан с сущностью и IFC-доменом, и какая специфика принадлежит каждому слою.

Этот документ фиксирует согласованную концепцию слоёв. Он не является нормативным стандартом и требует проверки на реальных IFC/Archicad-проектах.

## 1. Назначение

Слой в BRAIM — это не свойство объекта и не отдельная сущность. Слой — это рабочее поле для определённого ядра: способ выборки, владения атрибутами и применения правил к сущностям.

Слой отвечает на три вопроса:

- какие сущности попадают в этот слой;
- какие атрибуты этот слой «владеет»;
- какие правила валидации и логика применяются внутри слоя.

## 2. Базовые понятия

### Сущность (Entity)

Сущность — основополагающий контейнер информации и «жизни» объекта в проекте. У сущности есть:

- instance_id — единый идентификатор во всех представлениях;
- entity_type — тип сущности (Wall, Room, Opening, и т.д.);
- атрибуты;
- связи с другими сущностями;
- provenance (источник, статус, версия).

### IFC-домен

IFC Domain — тематический модуль внутри IFC-схемы: группа определений сущностей для конкретной дисциплины (Architecture, Structural, HVAC, Construction Management). IFC — открытый vendor-neutral стандарт buildingSMART, опубликованный как ISO 16739; текущий официальный релиз — IFC 4.3.2.0.

IFC-домен определяет классификацию сущности (к какой тематической группе она относится), но не заменяет слой.

### Слой (Layer)

Слой — это проекция/выборка над сущностями. Слой определяет:

- selection_rule — какие сущности попадают в слой;
- owns_attributes — какие атрибуты слой «владеет»;
- validation_rules — какие правила применяются внутри слоя;
- ifc_domain — к какому IFC-домену относится слой.

## 3. Модель слоя

Каждый слой описывается по единому шаблону:

```text
Layer <ID>:
  name: <название>
  selection_rule: <какие сущности попадают>
  owns_attributes: [список атрибутов]
  validation_rules: [список правил]
  ifc_domain: <IFC-домен>
```

Пример:

```text
Layer L4-G:
  name: Geometric
  selection_rule: "сущности с геометрическими атрибутами"
  owns_attributes: [x, y, width, height, polygon]
  validation_rules: [grid_quantum, overlap, containment]
  ifc_domain: Architecture
```

## 4. Полный список слоёв L0–L15

Ниже — концептуальное описание всех 16 слоёв. Для Core v0.1 реализуются только слои, помеченные MVP.

| ID | Название | Назначение | IFC-домен | MVP |
|---|---|---|---|---|
| L0-N | Normative | Ссылки на внешние нормы (СП, ГОСТ, ISO), не копии текста | — | Да |
| L1-C | Canonical | Единая модель сущностей BRAIM, source of truth | — | Да |
| L2-F | Functional | Помещения, зоны, ниши, функциональные требования | Architecture | Да |
| L3-R | Requirements | Проектные требования, извлечённые из норм и задач | — | Да |
| L4-G | Geometric | Размеры, координаты, формы | Architecture | Да |
| L5-T | Topological | Связность, графы смежности, доступность | — | Да |
| L6-X | Extended | Расширенные свойства (уточнить) | — | Нет |
| L7-O | Operational/Occupancy | Эксплуатационные данные, заполнение | — | Нет |
| L8-CST | Cost | Сметы, стоимость материалов и работ | — | Нет |
| L9-B | BIM/IFC | IFC4X3, openBIM, обмен с внешними системами | — | Да |
| L10-A | Authoring | Archicad, Revit, Renga — конкретные CAD/BIM | — | Нет |
| L11-INT | Interior/Finish | Финишные покрытия, мебель, оборудование | Architecture | Нет |
| L12-Q | Quality/Validation | Правила валидации, hard/soft constraints | — | Да |
| L13-D | Documentation | Планы, экспликации, ведомости | — | Нет |
| L14-E | Energy/Environmental | Энергоанализ, инсоляция, соляризация | HVAC | Нет |
| L15-P | Provenance/Lifecycle | Цепочка Source→Activity→Claim→Evidence→Verification→Decision | — | Да |

## 5. Специфика каждого слоя

### L0-N — Normative

```text
Layer L0-N:
  name: Normative
  selection_rule: "сущности, ссылающиеся на внешние нормы"
  owns_attributes: [norm_ref, edition, applicability]
  validation_rules: [source_required, no_full_copies]
  ifc_domain: —
```

Правило: слой хранит только ссылки и applicability, не копии текста норм.

### L1-C — Canonical

```text
Layer L1-C:
  name: Canonical
  selection_rule: "все сущности BRAIM"
  owns_attributes: [instance_id, entity_type, version]
  validation_rules: [unique_id, owner_present]
  ifc_domain: —
```

Правило: это source of truth, все остальные слои — проекции.

### L2-F — Functional

```text
Layer L2-F:
  name: Functional
  selection_rule: "Room, Zone, Niche"
  owns_attributes: [function, area, occupancy_type]
  validation_rules: [room_zone_distinction, adjacency]
  ifc_domain: Architecture
```

Правило: Room ≠ Zone, Niche — подзона внутри Room.

### L3-R — Requirements

```text
Layer L3-R:
  name: Requirements
  selection_rule: "сущности-требования"
  owns_attributes: [requirement_id, threshold, source_ref]
  validation_rules: [applicability_required, source_required]
  ifc_domain: —
```

Правило: требование — проектное извлечение из нормы, не сама норма.

### L4-G — Geometric

```text
Layer L4-G:
  name: Geometric
  selection_rule: "сущности с геометрическими атрибутами"
  owns_attributes: [x, y, width, height, polygon, orientation]
  validation_rules: [grid_quantum, overlap, containment]
  ifc_domain: Architecture
```

Правило: ориентация определяется относительно осей участка, не абсолютный азимут.

### L5-T — Topological

```text
Layer L5-T:
  name: Topological
  selection_rule: "сущности с топологическими связями"
  owns_attributes: [adjacency, access, connectivity]
  validation_rules: [reachability, no_forbidden_relations]
  ifc_domain: —
```

Правило: Adjacency ≠ Access — смежность и доступность разные вещи.

### L6-X — Extended

```text
Layer L6-X:
  name: Extended
  selection_rule: "уточнить"
  owns_attributes: [уточнить]
  validation_rules: [уточнить]
  ifc_domain: —
```

Статус: требует уточнения — что именно входит в «расширенные» свойства.

### L7-O — Operational/Occupancy

```text
Layer L7-O:
  name: Operational/Occupancy
  selection_rule: "сущности с эксплуатационными данными"
  owns_attributes: [occupancy, maintenance, usage]
  validation_rules: [уточнить]
  ifc_domain: —
```

Статус: требует уточнения.

### L8-CST — Cost

```text
Layer L8-CST:
  name: Cost
  selection_rule: "сущности с финансовыми данными"
  owns_attributes: [cost, quantity, unit_price]
  validation_rules: [уточнить]
  ifc_domain: —
```

Статус: требует уточнения.

### L9-B — BIM/IFC

```text
Layer L9-B:
  name: BIM/IFC
  selection_rule: "сущности для обмена через IFC"
  owns_attributes: [ifc_type, ifc_guid, pset_mapping]
  validation_rules: [ifc_schema_compliance]
  ifc_domain: все
```

Правило: IFC — транспорт/представление, не замена BRAIM.

### L10-A — Authoring

```text
Layer L10-A:
  name: Authoring
  selection_rule: "сущности, привязанные к CAD/BIM"
  owns_attributes: [archicad_id, revit_id, renga_id]
  validation_rules: [уточнить]
  ifc_domain: —
```

Правило: Archicad — адаптер, не ядро.

### L11-INT — Interior/Finish

```text
Layer L11-INT:
  name: Interior/Finish
  selection_rule: "сущности отделки и интерьера"
  owns_attributes: [finish_type, material, furniture]
  validation_rules: [уточнить]
  ifc_domain: Architecture
```

Статус: требует уточнения.

### L12-Q — Quality/Validation

```text
Layer L12-Q:
  name: Quality/Validation
  selection_rule: "сущности с правилами валидации"
  owns_attributes: [rule_id, severity, blocking]
  validation_rules: [hard_soft, unknown_handling]
  ifc_domain: —
```

Правило: severity и blocking — независимые поля.

### L13-D — Documentation

```text
Layer L13-D:
  name: Documentation
  selection_rule: "сущности для выпуска документации"
  owns_attributes: [view_id, sheet, schedule]
  validation_rules: [уточнить]
  ifc_domain: —
```

Статус: требует уточнения.

### L14-E — Energy/Environmental

```text
Layer L14-E:
  name: Energy/Environmental
  selection_rule: "сущности, участвующие в энергоанализе"
  owns_attributes: [u_value, r_value, thermal_bridge, insolation]
  validation_rules: [уточнить]
  ifc_domain: HVAC
```

Правило: внутри/снаружи — атрибут на уровне мира (теплотехника), не на уровне сущности.

### L15-P — Provenance/Lifecycle

```text
Layer L15-P:
  name: Provenance/Lifecycle
  selection_rule: "все сущности с provenance"
  owns_attributes: [source_ref, activity_id, claim_id, decision_id]
  validation_rules: [chain_complete, no_ai_as_norm]
  ifc_domain: —
```

Правило: цепочка Source→Activity→Claim→Evidence→Verification→Decision обязательна.

## 6. Связь слоя с сущностью

Сущность может принадлежать нескольким слоям одновременно. Связь фиксируется через массив layers в сущности:

```json
{
  "instance_id": "wall-123",
  "entity_type": "Wall",
  "layers": ["L1-C", "L2-F", "L4-G", "L9-B", "L12-Q", "L15-P"],
  "attributes": {
    "geometry": {"x": 0, "y": 0, "width": 5000, "height": 3000},
    "function": "partition",
    "fire_rating": "EI60",
    "ifc_type": "IfcWall"
  }
}
```

Правило: атрибут принадлежит сущности, но «показывается» через слой как выборка.

## 7. Правила реализации

1. Слой — это выборка, а не отдельная структура данных.
2. Слой владеет атрибутами, правилами и логикой.
3. IFC-домен определяет классификацию, слой — проекцию.
4. Сущность может быть в нескольких слоях.
5. Для Core v0.1 реализуются только слои с пометкой MVP.
6. Остальные слои описаны концептуально, реализация — в v0.2+.

## 8. Открытые вопросы

1. Уточнить состав слоя L6-X (Extended).
2. Уточнить состав слоя L7-O (Operational/Occupancy).
3. Уточнить состав слоя L8-CST (Cost).
4. Уточнить состав слоя L11-INT (Interior/Finish).
5. Определить, как слой связан с schema_version и миграциями.
6. Определить, как слой связан с axis_id (если он будет введён).

## 9. Changelog

### 0.1.0 — 2026-10-15

- Зафиксировано определение слоя как выборки/проекции.
- Зафиксирована связь слоя с сущностью и IFC-доменом.
- Описаны все 16 слоёв L0–L15.
- Выделены 8 слоёв для Core v0.1 (MVP).
- Зафиксирован шаблон описания слоя.
