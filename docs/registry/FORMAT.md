# Формат реестра нормативов BRAIM (P0-28, v0.1)

**Дата:** 2026-10-17 · **Статус:** draft
**Хранилище:** `docs/registry/<norm_id>.json` (в git)
**Источники:** Росстандарт (карточки), Минстрой (приказы), Новостник (P0-26)

## 1. Структура записи

```json
{
  "norm_id": "СП 252.1325800.2016",
  "title_ru": "...",
  "title_en": "...",
  "edition": "2016",
  "status": "Действует",
  "as_of": "2026-10-17",
  "registry": {
    "okp_oks": "91.040.99",
    "okved": null,
    "tech_committee": "465 — Строительство",
    "developers": ["..."]
  },
  "approval_prk": {"number": "573/пр", "date": "2016-08-17", "issuer": "Минстрой России"},
  "effective_from": "2017-02-18",
  "effective_until": null,
  "applicability": "...",
  "keywords": ["свод правил", "..."],
  "source": {"kind": "rosstandart_card", "url": null, "captured_at": "2026-10-17", "captured_by": "author:paste"},
  "supersedes": [],
  "superseded_by": [],
  "amendments": [
    {"number": 3, "approved_by_prk": "887/пр", "approved_at": "2024-12-20",
     "from_prk": "https://protect.gost.ru/", "note": "АО «Кодекс»", "source_provided_by": "author"}
  ]
}
```

## 2. Поля

- `norm_id` — **глобальный идентификатор** (напр. `СП 252.1325800.2016`); равен `edition=2016` для текущей редакции. Изменения живут в `amendments[]`, а не множат `norm_id` — это требование G-1 (применимость по lifecycle-контексту, не по версии нормы).
- `amendments[]` — массив с полями `number`, `approved_by_prk`, `approved_at` (ISO 8601), `from_prk` (URL приказа), `note`. **Версия даётся через `approved_at` текущего amendment**, а не через изменение `norm_id`.
- `supersedes / superseded_by` — для случаев, когда СП был заменён целиком (на сегодняшний день: крайне редко в РФ).
- `status` — `Действует | Не действует | Проект | Действует частично` (как в Росстандарте).

## 3. Кто имеет право писать

- **Регистратор** (P0-28) — единственная роль с правом `PUT/PATCH` (NOT-DOING §12). Автоповышения статуса нет.
- **Дозорный** (P0-20) — предлагает изменения, **не применяет**.
- **Новостник** (P0-26) — лента событий, не запись.
- **Эксперт** (человек) — approve через git commit.

## 4. Связь с другими артефактами

- `metadata.yaml` в `VERIFIED/<SP>/` ссылается на реестр по `norm_id` (повторное хранение запрещено, единый источник истины = реестр).
- `norm-criterion.json` ссылается на `source.approval_prk` + `amendment.number` для трассировки.
- `INBOX_INDEX.md` ссылается на `<norm_id>.json` для текущей стадии.

## 5. Парсер карточки Росстандарта (для Новостника, P0-26)

Формат: `<label>\n<value(s)>` где label — фиксированный набор. Простой split по меткам даёт точный dict (см. `tools/registrar/parse_order.py` + тест-скрипт в EXTRACTION_NOTES).

## 6. Changelog

- 0.1 — 2026-10-17: первая запись (СП 252.1325800.2016 + 3 Изменения), формат сформирован.
