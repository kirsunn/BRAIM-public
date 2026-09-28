# BRAIM Model View Registry

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
