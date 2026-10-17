# Агенты BRAIM: роли и состав (P0-25, 2026-10-17)

**Дата:** 2026-10-17 · **Статус:** активный реестр
**Принцип:** у каждого агента — `actor_id` в provenance (G-5). Ни один агент не повышает статус «молча» — `needs_source → confirmed` только человек (NOT-DOING §12).

## Команда

| # | Имя | Стадия lifecycle | Что делает | Реализация |
|---|---|---|---|---|
| 1 | **Ревизор** (Recon) | 1 | Метаданные PDF: pages, density, has_text_layer, sha256, превью | `normpipe detect` (план) |
| 2 | **Сортировщик** (Classifier) | 2 | «Что это?» — норматив? СП/ГОСТ/НПА? Реквизит (Минстрой, № приказа, дата) | `normpipe classify` (план) |
| 3 | **Привратник** (Linker) | 3 | StandardsRegistry: связать с записью; новое → завести; superseded → перенаправить | `normpipe link` (план) |
| 4 | **Лингвист** (Linguist) | 4a | Извлекает требования из текста (LLM, локальный Ollama или облако по F-06) | `normpipe linguist` ✅ работает |
| 5 | **Табельщик** (Tabulator) | 4б | pdfplumber (текст) первым; Tesseract (сканы); ячейки + координаты | `normpipe extract-tables` (P0-23, план) |
| 6 | **Распознаватель** (Recognizer) | 4в | Сырой JSON → norm-criterion.json (jsonschema) | `normpipe recognize` ✅ работает |
| 7 | **Картограф** (Mapper) | 4б→4в | Таблица → параметры/условия → правила; LLM только для семантики | (после табельщика, P0-23) |
| 8 | **Инспектор** (Validator) | 5 | Мета-валидация G-2: jsonschema, дубли правил, конфликты порогов, полнота applicability, валидность source_ref | `normpipe meta-validate` (план) |
| 9 | **Эксперт** (Expert) | 6 | Человек (ты или приглашённый ревизор). Утверждение/правка критериев через git commit (MVP), UI Expert Console (Phase 2) | git + planned UI |
| 10 | **Архивариус** (Archivist) | 7 | Перенос в `VERIFIED/SP-NNN_YYYY_ru/`; генерация `manifest.json`; обновление `INBOX_INDEX.md` | `normpipe activate` (план) |
| 11 | **Оформитель** (Formatter) | 5.5 | HTML-сверщик: слева скан/цитата, справа критерий, чекбоксы confirm/reject — MVP Expert Console без React | `normpipe review-report` (план) |
| 12 | **Дозорный** (Watcher) | 8 | Сверяет current_edition с сайтом Минстроя; **только предлагает** superseded_candidate (NOT-DOING §12) | `tools/aktualnost/` (P0-20, Phase 2) |

## Назначение (по источнику «нормативной документации»)

```
                              ┌──── 0 INBOX (файл получен)
                              │     ↓ Ревизор: метаданные PDF
                              │     ↓ Сортировщик: тип + реквизит
                              │     ↓ Привратник: StandardsRegistry
                              ├──── 3 LINK (norm_id связан)
                              │     ↓
                              │     Табельщик ─── Картограф
                              │     Лингвист    Распознаватель
                              ├──── 4 EXTRACT (rules + tables)
                              │     ↓
                              │     Инспектор (G-2 meta-validate)
                              │     ↓ Оформитель (HTML-сверщик)
                              │     ↓ Эксперт (human, G-5)
                              ├──── 6 APPROVED (provenance.approved_by)
                              │     ↓ Архивариус
                              ├──── 7 ACTIVE (VERIFIED/, manifest.json)
                              │     ↓
                              └──── 8 Дозорный (только propose superseded_candidate)
```

## Правила (для всех)

1. **У каждого агента — `actor_id` в provenance** (G-5): `human:author`, `human:kirsunn@rev`, `ai:ollama:qwen7b@local`, `normpipe:recognize@0.2` и т.п.
2. **Ни один агент не «молча» повышает статус** — `needs_source → confirmed` только человек (NOT-DOING §12).
3. **Шаги (1–5) — без сети/облака по умолчанию**; Лингвист — локально Ollama; облако — только F-06 (публичные нормы, G-6 не нарушается).
4. **Новый агент** добавляется через ADR-номер в `docs/adr/`.

## Связь

- `docs/ingest/INGEST_LIFECYCLE.md` — стадии 0–8.
- `docs/specs/...` — схемы артефактов (`metadata.yaml`, `norm-criterion.json`, `manifest.json`).
- `NOT-DOING.md` — что агенты **не делают** (авто-activate, облачные модели по умолчанию, Renga и т.п.).

## Changelog

- 0.1 — 2026-10-17: первая загрузка (12 ролей, 4 уровня, привязка к lifecycle).
