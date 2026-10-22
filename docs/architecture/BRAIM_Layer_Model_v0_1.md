# BRAIM Layer Model

> **Провенанс:** передано автором проекта 2026-10-15 (существовало только в чате); v0.1.1 — правки согласованности с Lifecycle Model / policy packs (обсуждение 2026-10-15); v0.1.2 — итоговый список слоёв L0–L17 от автора (L16-GN DEFERRED, L17-MEP RESERVED).
> **Синхронизировано:** `BRAIM_AI_CONTEXT_PACK.md` переведён со старых кодов `L11-V generator` / `L14-E operation` на канон `L11-INT` / `L14-E` (+ зарезервированные L16-GN/L17-MEP).

## Статус документа

Версия: 0.1.2

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
- какие семейства правил применяются внутри слоя.

## 2. Базовые понятия

### Сущность (Entity)

Сущность — основополагающий контейнер информации и «жизни» объекта в проекте. У сущности есть:

- instance_id — единый идентификатор во всех представлениях;
- entity_type — тип сущности (Wall, Room, Opening, и т.д.);
- атрибуты;
- связи с другими сущностями;
- provenance (источник, статус, версия).

### IFC-домен

IFC Domain — тематический модуль внутри IFC-схемы: группа определений сущностей для конкретной дисциплины (Architecture, Structural, HVAC, Plumbing, Electrical, Construction Management). IFC — открытый vendor-neutral стандарт buildingSMART, опубликованный как ISO 16739; текущий официальный релиз — IFC 4.3.2.0.

IFC-домен определяет классификацию сущности (к какой тематической группе она относится), но не заменяет слой.

### Слой (Layer)

Слой — это проекция/выборка над сущностями. Слой определяет:

- selection_rule — какие сущности попадают в слой;
- owns_attributes — какие атрибуты слой «владеет»;
- validation_rules_ref — ссылки на семейства правил в policy pack;
- validation_semantics — краткая семантика (что проверяют семейства слоя, одно предложение);
- ifc_domain — к какому IFC-домену относится слой (опционально; для транспортных слоёв — версии схемы).

## 3. Модель слоя

Каждый слой описывается по единому шаблону:

```text
Layer <ID>:
  name: <название>
  selection_rule: <какие сущности попадают>
  owns_attributes: [список атрибутов]
  validation_rules_ref: [семейства правил в policy pack: FAMILY_ID, …]
  validation_semantics: <одно предложение — что проверяют семейства слоя>
  ifc_domain: <IFC-домен или — (null)>
```

Пример:

```text
Layer L4-G:
  name: Geometric
  selection_rule: "физические элементы с GeometryRepresentation в канонической модели"
  owns_attributes: [x, y, width, height, polygon]
  validation_rules_ref: [GEO.GRID_QUANTUM, GEO.OVERLAP, GEO.CONTAINMENT]
  validation_semantics: "соответствие угловой/модульной сетке; недопустимые пересечения; вложенность"
  ifc_domain: Architecture
```

**Гибридная модель правил (решение 2026-10-15):** слой хранит **ссылку на семейство правил + краткую семантику**; конкретные версионированные правила, severity и пороги — исключительно в policy pack (Concept v1.0 §6, D-03). Результат валидации (`validation-result.json`) ссылается на `policy_pack_digest`, а не на слой — так строится provenance правил. Полная спецификация семейства живёт в манифесте policy pack.

## 4. Полный список слоёв L0–L17

Ниже — итоговый список всех 18 слоёв. Для Core v0.1 реализуются слои с пометкой MVP (9) + MVP-adjacent (частично, по потребности пилота).

| ID | Название | Назначение | IFC-домен | MVP | Статус |
|---|---|---|---|---|---|
| L0-N | Normative | Ссылки на внешние нормы (СП, ГОСТ, ISO), не копии текста | — | Да | Активен |
| L1-C | Canonical | Единая модель сущностей BRAIM, source of truth (включая MEP-сущности до активации L17-MEP) | — | Да | Активен |
| L2-F | Functional | Помещения, зоны, ниши, функциональные требования | Architecture | Да | Активен |
| L3-R | Requirements | Проектные требования, извлечённые из норм и задач | — | Да | Активен |
| L4-G | Geometric | Размеры, координаты, формы | Architecture | Да | Активен |
| L5-T | Topological | Связность, графы смежности, доступность | — | Да | Активен |
| L6-X | Extended | Расширенные свойства (уточнить) | — | Нет | Требует уточнения |
| L7-O | Operational/Occupancy | Эксплуатационные данные, заполнение | — | Нет | Требует уточнения |
| L8-CST | Cost | Сметы, стоимость материалов и работ | — | Нет | Требует уточнения |
| L9-B | BIM/IFC | IFC4X3, openBIM, обмен с внешними системами (включая MEP-обмен до активации L17-MEP) | — (schema: IFC2X3/IFC4/IFC4X3) | Да | Активен |
| L10-A | Authoring | Archicad, Revit, Renga — конкретные CAD/BIM | — | Нет | Требует уточнения |
| L11-INT | Interior/Finish | Финишные покрытия, мебель, оборудование | Architecture | MVP-adjacent | Активен |
| L12-Q | Quality/Validation | Правила валидации, hard/soft constraints | — | Да | Активен |
| L13-D | Documentation | Планы, экспликации, ведомости | — | Нет | Требует уточнения |
| L14-E | Energy/Environmental | Энергоанализ, инсоляция, соляризация | HVAC | Нет | Требует уточнения |
| L15-P | Provenance | Цепочка Source→Activity→Claim→Evidence→Verification→Decision + ссылки на LC-утверждения (lc_id[]) | — | Да | Активен |
| L16-GN | Generator | Генерация планировок (Functional & Ergonomic Planning Gyrus) | — | Нет | DEFERRED (2027+) |
| L17-MEP | MEP Systems | Отопление, вентиляция, водоснабжение | HVAC, Plumbing, Electrical | Нет | RESERVED (v0.2+) |

### Сводка по статусам

| Статус | Количество | Слои |
|---|---|---|
| MVP (активен) | 9 | L0-N, L1-C, L2-F, L3-R, L4-G, L5-T, L9-B, L12-Q, L15-P |
| MVP-adjacent | 1 | L11-INT |
| Требует уточнения | 6 | L6-X, L7-O, L8-CST, L10-A, L13-D, L14-E |
| DEFERRED (2027+) | 1 | L16-GN |
| RESERVED (v0.2+) | 1 | L17-MEP |

> **MVP-adjacent** — слой не входит в ядро Core v0.1, но частично реализуется по потребности пилота (атрибуты интерьера/отделки приходят из authoring-модели).
>
> **Коды стабильны.** DEFERRED/RESERVED-коды закрепляются заранее, чтобы не переиспользовать существующие коды под другой смысл (урок конфликта L11-V/L14-E).

## 5. Специфика каждого слоя

### L0-N — Normative

```text
Layer L0-N:
  name: Normative
  selection_rule: "сущности, ссылающиеся на внешние нормы"
  owns_attributes: [norm_ref, edition, applicability]
  validation_rules_ref: [NORM.SOURCE_REQUIRED, NORM.NO_FULL_COPIES]
  validation_semantics: "у каждой ссылки на норму есть источник; копии текста норм запрещены"
  ifc_domain: —
```

Правило: слой хранит только ссылки и applicability, не копии текста норм.

### L1-C — Canonical

```text
Layer L1-C:
  name: Canonical
  selection_rule: "все сущности BRAIM"
  owns_attributes: [instance_id, entity_type, version]
  validation_rules_ref: [CANON.UNIQUE_ID, CANON.OWNER_PRESENT]
  validation_semantics: "идентификаторы уникальны; владелец указан"
  ifc_domain: —
```

Правило: это source of truth, все остальные слои — проекции. До активации L17-MEP включает и инженерные сущности.

### L2-F — Functional

```text
Layer L2-F:
  name: Functional
  selection_rule: "Room, Zone, CompoundSpace, Subzone, Niche"
  owns_attributes: [function, area, occupancy_type]
  validation_rules_ref: [SP.ROOM_ZONE_DISTINCTION, SP.ADJACENCY]
  validation_semantics: "Room ≠ Zone; ниша/подзона — не самостоятельное помещение без сепарации"
  ifc_domain: Architecture
```

Правило: Room ≠ Zone, Niche — подзона внутри Room. Терминология CompoundSpace/Subzone — по новейшей итерации концепции (docs/analysis/, §6).

### L3-R — Requirements

```text
Layer L3-R:
  name: Requirements
  selection_rule: "сущности-требования"
  owns_attributes: [requirement_id, threshold, source_ref]
  validation_rules_ref: [REQ.APPLICABILITY_REQUIRED, REQ.SOURCE_REQUIRED]
  validation_semantics: "у требования есть применимость и источник"
  ifc_domain: —
```

Правило: требование — проектное извлечение из нормы, не сама норма.

### L4-G — Geometric

```text
Layer L4-G:
  name: Geometric
  selection_rule: "физические элементы с GeometryRepresentation в канонической модели"
  owns_attributes: [x, y, width, height, polygon, orientation]
  validation_rules_ref: [GEO.GRID_QUANTUM, GEO.OVERLAP, GEO.CONTAINMENT]
  validation_semantics: "соответствие сетке; пересечения; вложенность"
  ifc_domain: Architecture
```

Правило: ориентация определяется относительно осей участка, не абсолютный азимут. Selection определяется типами сущностей/каноническими представлениями, а не владеемыми атрибутами (устранена цикличность).

### L5-T — Topological

```text
Layer L5-T:
  name: Topological
  selection_rule: "сущности с топологическими связями"
  owns_attributes: [adjacency, access, connectivity]
  validation_rules_ref: [TOP.REACHABILITY, TOP.NO_FORBIDDEN_RELATIONS]
  validation_semantics: "достижимость; запрещённые связи отсутствуют"
  ifc_domain: —
```

Правило: Adjacency ≠ Access — смежность и доступность разные вещи.

### L6-X — Extended

```text
Layer L6-X:
  name: Extended
  selection_rule: "уточнить"
  owns_attributes: [уточнить]
  validation_rules_ref: [уточнить]
  validation_semantics: уточнить
  ifc_domain: —
```

Статус: требует уточнения — что именно входит в «расширенные» свойства.

### L7-O — Operational/Occupancy

```text
Layer L7-O:
  name: Operational/Occupancy
  selection_rule: "сущности с эксплуатационными данными"
  owns_attributes: [occupancy, maintenance, usage]
  validation_rules_ref: [уточнить]
  validation_semantics: уточнить
  ifc_domain: —
```

Статус: требует уточнения.

### L8-CST — Cost

```text
Layer L8-CST:
  name: Cost
  selection_rule: "сущности с финансовыми данными"
  owns_attributes: [cost, quantity, unit_price]
  validation_rules_ref: [уточнить]
  validation_semantics: уточнить
  ifc_domain: —
```

Статус: требует уточнения.

### L9-B — BIM/IFC

```text
Layer L9-B:
  name: BIM/IFC
  selection_rule: "сущности для обмена через IFC"
  owns_attributes: [ifc_type, ifc_guid, pset_mapping]
  validation_rules_ref: [IFC.SCHEMA_COMPLIANCE]
  validation_semantics: "соответствие выбранной версии схемы IFC"
  ifc_schema: [IFC2X3, IFC4, IFC4X3]
  ifc_domain: —
```

Правило: IFC — транспорт/представление, не замена BRAIM. Слой транспортный: вместо IFC-домена фиксирует поддерживаемые версии схемы (IFC-домен не бывает «всё»).

### L10-A — Authoring

```text
Layer L10-A:
  name: Authoring
  selection_rule: "сущности, привязанные к CAD/BIM"
  owns_attributes: [archicad_id, revit_id, renga_id]
  validation_rules_ref: [уточнить]
  validation_semantics: уточнить
  ifc_domain: —
```

Правило: Archicad — адаптер, не ядро (см. integrations/archicad-tapir в код-репо).

### L11-INT — Interior/Finish

```text
Layer L11-INT:
  name: Interior/Finish
  selection_rule: "сущности отделки и интерьера"
  owns_attributes: [finish_type, material, furniture]
  validation_rules_ref: [уточнить]
  validation_semantics: уточнить
  ifc_domain: Architecture
```

Статус: активен, MVP-adjacent — частичная реализация по потребности пилота; состав требует уточнения.

### L12-Q — Quality/Validation

```text
Layer L12-Q:
  name: Quality/Validation
  selection_rule: "сущности с правилами валидации"
  owns_attributes: [rule_id, severity, blocking]
  validation_rules_ref: [QA.HARD_SOFT, QA.UNKNOWN_HANDLING]
  validation_semantics: "hard/soft-ограничения; обработка UNKNOWN"
  ifc_domain: —
```

Правило: severity и blocking — независимые поля. По гибридной модели конкретные severity/пороги — в манифесте policy pack (открытый вопрос №7).

### L13-D — Documentation

```text
Layer L13-D:
  name: Documentation
  selection_rule: "сущности для выпуска документации"
  owns_attributes: [view_id, sheet, schedule]
  validation_rules_ref: [уточнить]
  validation_semantics: уточнить
  ifc_domain: —
```

Статус: требует уточнения.

### L14-E — Energy/Environmental

```text
Layer L14-E:
  name: Energy/Environmental
  selection_rule: "сущности, участвующие в энергоанализе"
  owns_attributes: [u_value, r_value, thermal_bridge, insolation]
  validation_rules_ref: [уточнить]
  validation_semantics: уточнить
  ifc_domain: HVAC
```

Правило: атрибут «внутри/снаружи» хранится на сущности (в IFC — `Pset_SpaceCommon.IsExternal`), но интерпретируется теплотехническим расчётом на уровне расчётного мира/зоны. Различие «где хранится» и «где интерпретируется» — осознанное.

### L15-P — Provenance

```text
Layer L15-P:
  name: Provenance
  selection_rule: "все сущности с provenance"
  owns_attributes: [source_ref, activity_id, claim_id, evidence_ref, verification_ref, decision_ref, lc_refs]
  validation_rules_ref: [PROV.CHAIN_COMPLETE, PROV.NO_AI_AS_NORM, PROV.LC_REF_VALID]
  validation_semantics: "цепочка доказательств полна; ИИ-вывод не является нормой; ссылки на LC корректны"
  ifc_domain: —
```

Правило: цепочка Source→Activity→Claim→Evidence→Verification→Decision обязательна. **Жизненный цикл не является атрибутом слоя:** слой держит ссылки (`lc_refs`) на LC-утверждения scope (`braim-spec/schemas/lifecycle-state.json`); сам ЖЦ живёт в scope-утверждениях по LC-01 (`BRAIM_Lifecycle_Model_v0_1.md`).

### L16-GN — Generator

```text
Layer L16-GN:
  name: Generator
  selection_rule: "уточняется при старте функциональной генерации"
  owns_attributes: [уточнить]
  validation_rules_ref: [уточнить]
  validation_semantics: уточнить
  ifc_domain: —
```

Статус: **DEFERRED (2027+)** — реализация после Развитие-ЦТ. Код закреплён заранее (наследник идеи `L11-V generator` из AI Context Pack и «Functional & Ergonomic Planning Gyrus» из новейшей итерации концепции, §8).

### L17-MEP — MEP Systems

```text
Layer L17-MEP:
  name: MEP Systems
  selection_rule: "инженерные системы и оборудование (IfcDistributionSystem, IfcDistributionElement и др.)"
  owns_attributes: [уточнить]
  validation_rules_ref: [уточнить]
  validation_semantics: уточнить
  ifc_domain: HVAC, Plumbing, Electrical
```

Статус: **RESERVED (v0.2+)** — реализуется вместе с инженерными проверками; до активации инженерные сущности живут в L1-C и обмениваются через L9-B.

## 6. Связь слоя с сущностью

Сущность может принадлежать нескольким слоям одновременно. Связь фиксируется через массив layers в сущности:

```json
{
  "instance_id": "ent_wall_000123",
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

Правило: атрибут принадлежит сущности, но «показывается» через слой как выборка. Конвенция instance_id — открытый вопрос №8.

## 7. Правила реализации

1. Слой — это выборка, а не отдельная структура данных.
2. Слой владеет атрибутами; правила — через ссылки на семейства.
3. IFC-домен определяет классификацию, слой — проекцию.
4. Сущность может быть в нескольких слоях.
5. Для Core v0.1 реализуются слои MVP (9) + MVP-adjacent (L11-INT, частично).
6. Остальные слои описаны концептуально; реализация — в v0.2+.
7. **Гибридная модель правил:** слой хранит ссылку на семейство (`validation_rules_ref`) + краткую семантику (`validation_semantics`); конкретные правила, severity и пороги — только в policy pack (решение 2026-10-15).
8. **Коды слоёв стабильны:** DEFERRED/RESERVED-коды (L16-GN, L17-MEP) закреплены заранее и не переиспользуются.

## 8. Открытые вопросы

1. Уточнить состав слоя L6-X (Extended).
2. Уточнить состав слоя L7-O (Operational/Occupancy).
3. Уточнить состав слоя L8-CST (Cost).
4. Уточнить состав слоя L11-INT (Interior/Finish).
5. Определить, как слой связан с schema_version и миграциями.
6. Определить, как слой связан с axis_id (если он будет введён).
7. L12-Q: разграничить rule-сущности слоя и манифест policy pack (severity/blocking — в манифесте).
8. Зафиксировать конвенцию instance_id (кандидат: префикс `ent_…`, по аналогии с art_/snp_/lc_).
9. Закрепить спецификацию L16-GN при старте функциональной генерации (после Развитие-ЦТ).
10. Активировать L17-MEP вместе с первыми инженерными проверками (v0.2+).

## 9. Changelog

### 0.1.2 — 2026-10-15

- Итоговый список слоёв L0–L17 от автора: добавлены L16-GN Generator (DEFERRED 2027+) и L17-MEP MEP Systems (RESERVED v0.2+); колонка Статус; сводка по статусам (MVP = 9, исправлена арифметика).
- Поле правил — гибрид: `validation_rules_ref` + `validation_semantics`; конкретные правила только в policy pack.
- L9-B: транспортный слой — `ifc_schema` вместо невалидного `ifc_domain: "все"`.
- L14-E: различие «где хранится» (Pset_SpaceCommon.IsExternal на сущности) и «где интерпретируется» (расчётный мир/зона).
- L4-G: устранена цикличность selection_rule.
- L6-X возвращён к «Extended (уточнить)» — генератор получил собственный код L16-GN.
- Синхронизирован BRAIM_AI_CONTEXT_PACK.md (L11-V/L14-E → L11-INT/L14-E, + L16-GN/L17-MEP).

### 0.1.1 — 2026-10-15

- Решения обсуждения: L15-P → Provenance (ЖЦ — ссылки на LC-утверждения, не атрибуты); гибрид правил (ссылка + семантика в слое, правила в policy pack); L11-INT остаётся, генератору — новый код; MEP-слой — позже.

### 0.1.0 — 2026-10-15

- Первоначальная фиксация: слой как выборка/проекция; связь с сущностью и IFC-доменом; 16 слоёв L0–L15; MVP-набор; шаблон слоя.
