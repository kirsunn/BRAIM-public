# BRAVO v0.4 Architecture Update

> **Architecture update v0.4:** BRAIM is hosted inside BRAVIUM-Planet. The BRAV container is `IFCA + BAR + BAV + RAG + BAG`. BAV is validated against RAG; BAG records activity and decisions. See [`BRAVO_ARCHITECTURE_V0_4.md`](./BRAVO_ARCHITECTURE_V0_4.md).

# BRAIM Project Identity

## Статус

- Версия: `0.2.0`
- Дата: 2026-10-18
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

## Product Family & Naming

BRAIM является governance-слоем более широкой продуктовой семьи. Названия ниже описывают разные уровни одной системы, а не конкурирующие версии проекта.

| Название | Уровень | Назначение |
|---|---|---|
| **BRAIM** | Governance platform | Оркестрация проектной информации, provenance, Quality Gate, snapshots, CDE-интеграция |
| **BRAVIM** | Building Avatar platform | Платформа, в которой здание существует как живой верифицируемый аватар |
| **BAV** | Building Avatar | Сама модель/сущность здания: идентичность, свойства, отношения, доказательства, правила, жизненный цикл |
| **BAR** | Building Avatar Registry | Реестр аватаров, их версий, доказательств, правил и статусов |
| **VAR** | Versioned Avatar Representation | Версионированное представление аватара для хранения, обмена и воспроизводимости |
| **RAG** | Requirements & Constraints Graph | Граф требований, ограничений и нормативных критериев проекта |
| **BAG** | Building Activity Log | Журнал активности: изменения, проверки, решения |
| **IFCA** | Exchange format | Транспортный формат BAV: как аватар представляется и переносится между системами |
| **BRAVO** | Product suite | Зонтичное название объединённой системы |

```text
BRAVO = BRAIM (governance) + BRAVIM/BAV (building avatar) + IFCA (transport)
```

BRAIM не устаревает: он остаётся каноническим governance-именем. BRAVIM/BAV добавляет над ним слой «живого» здания, BAR обеспечивает реестр и версионность, VAR — версионированное представление, IFCA — обмен, BRAVO — объединённый продукт.

```yaml
product_family:
  umbrella: BRAVO
  governance: BRAIM
  avatar_platform: BRAVIM
  avatar: BAV
  avatar_registry: BAR
  avatar_representation: VAR
  requirements_graph: RAG
  activity_log: BAG
  exchange_format: IFCA
```

## Основная идея

```text
микрокернель
+ единая модель сущностей
+ нулевая шина
+ подключаемые специализированные ядра
+ дисциплинарные представления
+ контролируемая нормативная база
+ Building Avatar и Ruleset Packages
```

BRAIM не должен выдавать непроверенные AI-выводы за нормы, заменять официальные документы, скрывать происхождение данных, автоматически публиковать WIP-материалы, быть только генератором изображений или смешивать помещение, зону, проём и заполнение.

Основные направления: Entity Meta-Model, Normative Knowledge, Room/Zone/Niche Passport, Variant Strategy Engine, Plan-to-Form, Form-to-Plan, Geospatial and Point Cloud, IFC/IDS/BCF, Archicad Connector, Model View Registry, Validation and Verification, Control Center, Building Avatar, Ruleset Package, Evidence Fragment, Treatment Package.

```text
BAIM → legacy project name
BRAIM → current canonical governance name
BRAVIM → building avatar platform name
BAV → building avatar entity
BRAIN → rejected name; do not use
```