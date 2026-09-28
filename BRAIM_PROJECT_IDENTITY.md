# BRAIM Project Identity

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
