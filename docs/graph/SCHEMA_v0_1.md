# BRAIM Graph Schema v0.1

**Дата:** 2026-10-17 · **Статус:** draft, на первой загрузке из 3–5 таблиц одного СП
**Хранилище:** NetworkX (Python) + генератор Cypher-seed для Neo4j (Phase 2)

## 1. Узлы

| Label | Атрибуты | Карта в наш словарь |
|---|---|---|
| `Document` | code, title, edition, date, url, status, sha256, period_from, period_until | StandardRegistry (P0-18) |
| `Table` | id, page, bbox, caption, units, headers[], n_rows, n_cols | один документ — много таблиц |
| `Row` | id, table_id, row_idx, raw_text, cells[] (col_idx → {value, unit, parse_status}) | могут быть пустыми/мультизаголовочными — обработка явная |
| `Parameter` | id, name, value, unit, scale, normal_form | BRAIM Pset (слой B словарной политики) |
| `Condition` | id, parameter_ref, op, value, unit | зеркало `applicability.conditions` в norm-criterion |
| `Rule` | id, statement, kind (threshold/computed/presence/script), source_table_ref, target_para, target_attr, threshold, computed, presence, script_ref | зеркало norm-criterion.check |
| `Criterion` | id, title, source_ref, modality, verification, binding_context, prose, summary | отражение norm-criterion.json (P0-17) |
| `Property` | id, bsdd_property_ref, attr_id, unit, data_type, ifc_binding | BRAIM Pset (bSDD-совместимый словарь) |
| `Evidence` | id, kind (pdf_scan|excel|web|book), uri, sha256, captured_at, who | провенанс-узел |
| `Org` | id, name, role (developer/designer/owner) | ТЭП-ведомость, штамп |

## 2. Связи

| Тип | Откуда → куда | Семантика |
|---|---|---|
| `SOURCED_FROM` | Row/Table/Rule → Document/Table/Row | источник правила/параметра |
| `EXTRACTED_FROM` | Parameter/Condition/Rule → Row | из какой строки |
| `CONTAINS` | Table → Row, Document → Table | иерархия |
| `HAS_CONDITION` | Rule → Condition | условие применимости |
| `HAS_PARAMETER` | Rule/Condition → Parameter | ссылки на параметры |
| `IMPLEMENTED_BY` | Criterion → Rule | criterion=что, rule=как применить |
| `MEASURED_BY` | Criterion/Rule → Property | измеряется через это свойство |
| `APPLIES_TO` | Rule/Criterion → ElementType (Wall/Room/System) | BIM-привязка |
| `MAPS_TO` | Property → bSDD | результат словарного водопада (CL-05) |
| `SUPERSEDES` / `SUPERSEDED_BY` | Document → Document | G-1 (применимость редакций) |
| `APPROVED_BY` / `AI_DRAFTED_BY` | Criterion/Rule → Actor (human|ai:model) | G-5 (ИИ-акторы) |

## 3. Принципы

- **Ячейка ≠ узел.** Таблица — документ с provenance; правило из неё — узел.
- **Condition** — отдельный узел (1 правило ↔ N условий), а не свойство правила — для запросов типа «что изменится при увеличении этажности?».
- **Criterion и Rule** — разные сущности: criterion = нормализованное требование (что должно соблюдаться), rule = правило валидации (как проверить на IFC-модели).
- **Property** живёт в BRAIM Pset (bSDD-совместимый словарь), а не в графе — иначе дублирование определений.
- **ИИ-акторы** — отдельный узел Actor с типом (human|ai:model@version), связи APPROVED_BY/DRAFTED_BY обязательны (G-5).
- **Pinned digests** на Document и Evidence — версионирование таблиц и проверка неизменности (DICT-04).

## 4. Что **не делаем** в v0.1

- Каждая ячейка = узел (взрыв графа, без пользы)
- Графовое хранилище в БД (Phase 2 при масштабе) — пока NetworkX-граф в Python-процессе
- Полная синхронизация с bSDD-онтологией (словарный водопад постепенно)
- Шаблоны графа для каждого домена (физика, пожарка, МГН) — добавим по мере подключения

## 5. Связь с другими артефактами

- `norm-criterion.json` (schema) ↔ `Criterion`/`Rule` (graph) — модель данных
- `policy pack` ↔ snapshot словаря (edition+digest) — provenance
- `validation-result.json` ↔ `Criterion` (findings.affected_guids) — исполнение

## 6. Changelog

- 0.1 — 2026-10-17: первая загрузка схемы (γ: заложить основу графа на NetworkX; источник — референс BAIM_Roadmap_v0_1 + решения автора).
