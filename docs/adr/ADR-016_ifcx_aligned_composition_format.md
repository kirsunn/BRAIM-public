# ADR-016: BRAIM Composition Format — IFCX-совместимая слоистая сериализация

- **Статус:** Accepted (draft; спецификация формата — в Phase 1 vertical slice)
- **Дата:** 2026-10-15
- **Относится к:** ADR-009 (IFC5 sandbox + composition-native alignment), Zero Bus (Project Package), Layer Model v0.1.2, новейшая итерация концепции
- **Источники:** [buildingSMART/IFC5-development (Examples_FAQ)](https://github.com/buildingSMART/IFC5-development/blob/main/Examples_FAQ.md), [IFCX Data Format (deepwiki)](https://deepwiki.com/buildingSMART/IFC5-development/2-ifcx-data-format), [Glossary (deepwiki)](https://deepwiki.com/buildingSMART/IFC5-development/8-glossary), [ifcJSON Documentation](https://github.com/buildingsmart-community/ifcJSON/blob/master/Documentation/README.md); референс-клон: `_library/ifc5-reference` (examples: Hello Wall, Linear placement of signals; schema/ifcx.tsp)

---

## 1. Контекст

**IFCX** — экспериментальный JSON-формат IFC 5/IFC X: не «IFC в JSON», а модульная система. Файл `.ifcx` = `header` + `imports` (зависимости по URI) + `schemas` (локальные расширения) + `data` (узлы `IfcxNode`, адресуемые по `path`). Схема — TypeSpec → JSON Schema (ifcx.dev). Ключевой механизм — **layer composition**: стек `.ifcx`-файлов; верхний слой дополняет/переопределяет данные узла по его `path` (пример: base-геометрия → слой FireRating → слой статусов проверки). Статус — альфа: схема меняется, валидация неполная, не для production (ADR-009 D1 это уже зафиксировал).

Исследование автора (2026-10-15): «это наш вектор — мы должны его реализовать». Настоящий ADR определяет, **что именно** реализуем, не нарушая sandbox-правил ADR-009.

## 2. Решения

| ID | Решение | Смысл |
|---|---|---|
| D1 | **Композиция IFCX — родной способ сериализации артефактов BRAIM** | BRAIM принимает модель IFCX: path-адресованные узлы, imports по URI, локальные схемы, слоистый стек — как формат **своих** canonical/enriched/export-артефактов («BRAIM Composition Format», BCF-style bundle). Имена полей — свои; маппинг на IFCX задокументирован. Не зависим от альфа-схемы IFCX |
| D2 | **Precedence с оговоркой BRAIM** | Приоритет верхнего слоя действует **внутри стека одного владельца/этапа**. Между слоями разных владельцев (архитектор vs пожарный инженер) пересечение значений = **конфликт → явное разрешение**, а не молчаливое перекрытие (инвариант Zero Bus №3). Это осознанное отличие от IFCX-механики «верхний просто побеждает» |
| D3 | **Project Package сериализуется слоями** | Пакет Zero Bus: `manifest.json` + слои (canonical nodes ← Parsed/Canonical; enrich-слои ← PropertyAssertion/evidence; exports; evidence). Каждый слой — самодостаточный артефакт с snapshot_id и provenance (ADR-009 P1). Спецификация формата v0.1 — deliverable Phase 1 vertical slice |
| D4 | **Path — адресация, не идентичность** | `path` узла (как в IFCX) — способ адресации внутри пакета; идентичность остаётся `instance_id ↔ externalIdentity (GUID)` через IdentityLink (ADR-009 P2). Path может меняться, идентичность — нет |
| D5 | **Sandbox-наблюдение IFC5-development** | Репо склонировано в `_library/ifc5-reference` (не зависимость, вне git BRAIM): изучение примеров (Hello Wall, Linear placement) и `schema/ifcx.tsp` — задача sandbox Phase 1. Ноль production-кода IFCX до триггеров ADR-009 D4 |

## 3. Соответствие IFCX → BRAIM

| IFCX | BRAIM Composition Format | Замечание |
|---|---|---|
| `header` | `manifest.json` пакета (schema, snapshot_id, layers) | Плюс provenance и policy_pack_digest |
| `imports` по URI | imports слоёв/словарей по URI + pinned digests (DICT-04) | Воспроизводимость: версии зафиксированы |
| `schemas` (локальные расширения) | `validation_semantics`/policy pack-семейства; локальные схемы узлов | Расширяемость без изменения базовой схемы — совпадает |
| `IfcxNode.data` по `path` | canonical/enriched узлы с `path` + `instance_id` | Path = адрес, идентичность — отдельная ось (D4) |
| Layer composition, precedence | Стек слоёв Project Package; precedence только внутри владельца (D2) | Отличие: cross-owner конфликт — явно |
| TypeSpec → JSON Schema | braim-spec JSON Schemas (draft 2020-12) | При триггере — генерация из TypeSpec не исключена |
| ifcJSON (старый проект) | Не используем: это конвертация EXPRESS, а не композиция | Убережение от ложного пути |

## 4. Последствия

- **Положительные:** формат BRAIM и IFCX сближаются по построению — при созревании IFC X (триггеры ADR-009 D4) маппинг станет технической работой, а не переработкой; сценарий «архитектор публикует геометрию → инженер добавляет слой огнестойкости → координатор слой статусов → CDE собирает федерацию без перезаписи» — это буквально Zero Bus + LC-views.
- **Цена/риски:** своя сериализация = своя поддержка; дисциплина «не скопировать альфа-схему IFCX дословно» (она изменится); 195 МБ референс-клона — только локально, вне git BRAIM.
- **Что не меняется:** production-форматы Phase 1–2 (IFC 4.x, JSON-схемы braim-spec, BCF 3.0); sandbox-правила ADR-009.

## 5. Changelog

- 0.1 — 2026-10-15: создан (D1..D5). Связан с ADR-009.
