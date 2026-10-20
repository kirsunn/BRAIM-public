# NORMATIVE_VERIFICATION_CHECKLIST_v0.1

**Статус:** proposed
**Дата:** 2026-10-20
**Назначение:** первичный чек-лист нормативных документов для верификации по ADR-0009.
**Граница:** это заготовка, а не источник правды. Формат хранения — NDJSON, CSV или SQLite — выбирается отдельно.

## Принцип

Все записи начинают жизнь как:

```text
needs_verification
```

или, если идентификация документа неполна:

```text
pending_resolution
```

Поля `verified_by`, `verified_at`, `verified_source` и `evidence` остаются пустыми до ручной верификации.

## 1. Список документов

| # | Обозначение | Описание | Статус |
|---|---|---|---|
| 1 | СП 548.1325800.2025 | Яхтенные гавани. Правила проектирования. Контрольный документ первого вертикального среза. | needs_verification |
| 2 | СП 333.1325800.2020 | Формирование информационной модели на различных стадиях жизненного цикла. | needs_verification |
| 3 | СП 404.1325800.2018 | Разработка планов программы информационного моделирования. | needs_verification |
| 4 | СП 480.1325800.2020 | Требования к информационным моделям для эксплуатации многоквартирных домов. | needs_verification |
| 5 | СП 301.1325800.2017 | Организация работ производственно-техническими отделами. | needs_verification |
| 6 | СП 481.1325800.2020 | Применение типовой проектной документации повторного использования. | needs_verification |
| 7 | СП 444 | Требуется уточнить полное обозначение и год. | pending_resolution |

## 2. Записи

```json
{"id":"norm:sp-548-2025","title":"Яхтенные гавани. Правила проектирования","designation":"СП 548.1325800.2025","year":2025,"edition":"","publisher":"","source_url":"","status":"needs_verification","verified_by":"","verified_at":"","verified_source":"","evidence":"","extracted_in":["dry-runs/slice_63cca1c9_2026-10-19_dryrun/"],"notes":"Контрольный документ первого вертикального среза."}
{"id":"norm:sp-333-2020","title":"","designation":"СП 333.1325800.2020","year":2020,"edition":"","publisher":"","source_url":"","status":"needs_verification","verified_by":"","verified_at":"","verified_source":"","evidence":"","extracted_in":[],"notes":"Полное наименование требует сверки с первоисточником."}
{"id":"norm:sp-404-2018","title":"","designation":"СП 404.1325800.2018","year":2018,"edition":"","publisher":"","source_url":"","status":"needs_verification","verified_by":"","verified_at":"","verified_source":"","evidence":"","extracted_in":[],"notes":"Полное наименование требует сверки с первоисточником."}
{"id":"norm:sp-480-2020","title":"","designation":"СП 480.1325800.2020","year":2020,"edition":"","publisher":"","source_url":"","status":"needs_verification","verified_by":"","verified_at":"","verified_source":"","evidence":"","extracted_in":[],"notes":"Полное наименование требует сверки с первоисточником."}
{"id":"norm:sp-301-2017","title":"","designation":"СП 301.1325800.2017","year":2017,"edition":"","publisher":"","source_url":"","status":"needs_verification","verified_by":"","verified_at":"","verified_source":"","evidence":"","extracted_in":[],"notes":"Полное наименование требует сверки с первоисточником."}
{"id":"norm:sp-481-2020","title":"","designation":"СП 481.1325800.2020","year":2020,"edition":"","publisher":"","source_url":"","status":"needs_verification","verified_by":"","verified_at":"","verified_source":"","evidence":"","extracted_in":[],"notes":"Полное наименование требует сверки с первоисточником."}
{"id":"norm:sp-444-pending","title":"","designation":"","year":"","edition":"","publisher":"","source_url":"","status":"pending_resolution","verified_by":"","verified_at":"","verified_source":"","evidence":"","extracted_in":[],"notes":"Обозначение и год не подтверждены; до уточнения не входит в needs_verification."}
```

## 3. Поля записи

| Поле | Тип | Описание |
|---|---|---|
| `id` | string | стабильный ID с префиксом `norm:` |
| `title` | string | полное наименование |
| `designation` | string | каноническое обозначение |
| `year` | integer | год |
| `edition` | string | редакция или изменение |
| `publisher` | string | издатель |
| `source_url` | string | URL первоисточника |
| `status` | enum | статус верификации |
| `verified_by` | string | кто проверил |
| `verified_at` | date | когда проверено |
| `verified_source` | string | где проверено |
| `evidence` | string | SHA, ссылка на копию, скриншот или иной артефакт |
| `extracted_in` | array | срезы, в которых ссылка реально использовалась |
| `notes` | string | примечания |

## 4. Правило

```text
Запись становится verified
только после ручной проверки
первоисточника.

Обязательны:
verified_by;
verified_at;
verified_source;
evidence.
```

## 5. Boundary

- Формат хранения не выбран.
- Файл не заменяет ADR-0009.
- Push, commit и PR выполняются отдельной командой.
- СП 444 остаётся в `pending_resolution` до уточнения обозначения и года.
