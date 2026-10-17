# Ingest Lifecycle v0.1 — «не знаю → понимаю → размещаю»

**Дата:** 2026-10-17 · **Статус:** draft, тестируется на 17 СП из INBOX
**Суть:** файл проходит жизненный цикл от «непонятого» до «полностью размеченного и активированного в policy pack». Каждый этап — проверяемое состояние; ни один нельзя перепрыгнуть.

## 1. Стадии

```text
0 INBOX
  └─ что это вообще? (тип: PDF/DOCX/HTML/…; язык; страницы; подсказки из имени файла)
1 RECON (разведка)
  └─ OCR / pdfplumber / docx2txt → plaintext + метаданные (pages, density_text, sha256)
2 CLASSIFY (классификация)
  └─ это норматив? (СП/ГОСТ/СанПиН/ФЗ/НПА/…); номер; редакция; status (active/draft/superseded)
3 LINK (привязка к реестру)
  └─ StandardsRegistry: norm_id, system, edition, date, url, status; binding_context (G-1)
4 EXTRACT (извлечение)
  └─ текст → таблицы (координаты) → критерии (Linguist → Recognizer → norm-criterion)
5 VALIDATE (мета-валидация G-2)
  └─ jsonschema; дубли; конфликты порогов; полнота applicability; ссылки на редакции
6 APPROVE (human approval, G-5)
  └─ provenance.approved_by = human:…; approved_at
7 ACTIVATE (активация)
  └─ перенос в VERIFIED/SP-NNN_YYYY_ru/; INBOX_INDEX.md обновлён; policy pack v0.X
8 MONITOR (P0-20, только предложение статуса)
  └─ агент сверяет current_edition; ставит superseded_candidate — без применения
```

Состояние файла — это **стадия + дата перехода + кто/что выполнил**. Никаких «частично распознанных» файлов в policy pack: переход в VERIFIED требует ≥ status `APPROVED` по каждому извлечённому правилу.

## 2. Где это живёт в коде

| Стадия | Реализация | Когда |
|---|---|---|
| 0–1 | `normpipe detect <inbox.pdf>` → recon JSON | Phase 1 — первый день на СП 545 |
| 2 | `normpipe classify <recon.json>` → кандидат StandardsRegistry | Phase 1 |
| 3 | `normpipe link <recon.json> <registry.yaml>` → связано | Phase 1 |
| 4 | `linguist + recognize + gen-` (уже есть) | ✅ работает |
| 5 | `normpipe meta-validate <criteria.json>` — G-2 | Phase 1 (это новая подкоманда) |
| 6 | UI Expert Console (Phase 2) | Phase 2 — пока human через git approve + commit |
| 7 | `normpipe activate` — перенос в VERIFIED + manifest.json | Phase 1 |
| 8 | `tools/aktualnost/` (отдельный агент, P0-20) | Phase 2 |

## 3. Что меняется в normpipe v0.2 (план)

Добавляются подкоманды:
- `detect` — метаданные PDF/DOCX: pages, text_density, has_text_layer, sha256, first_page_preview
- `classify` — норматив? тип? реквизиты шапки (МИНСТРОЙ/ГОССТРОЙ/дата утв.)
- `link` — сопоставление с StandardsRegistry; если не нашли → создать новую запись
- `meta-validate` — G-2 (схема, дубли, конфликты, полнота applicability, валидность source_ref)
- `activate` — сгенерировать `manifest.json`, переместить в VERIFIED, обновить INBOX_INDEX.md

`linguist + recognize + gen-*` (уже есть) — это стадия 4.

## 4. Связь с INBOX_INDEX.md

`INBOX_INDEX.md` — это «лог всех файлов, прошедших через pipeline». Поля: дата, URL, filename, sha256, **текущая стадия**, кто/что перевёл на следующую.

## 5. Что **не** делаем (NOT-DOING-9, NOT-DOING-14)

- Не делаем auto-activate без human approval (NOT-DOING § 12)
- Не пытаемся «угадывать» type без текста — стадия 0 возвращает `unknown` если не смогли прочитать, **файл остаётся в INBOX**, и человек разбирается
- Не делаем постоянного хранения state в БД — стадия вычисляется из наличия артефактов (manifest, source.pdf, criteria) в `VERIFIED/<SP>/`

## 6. Changelog

- 0.1 — 2026-10-17: первая загрузка (инсайт автора «не знаю → понимаю → раскладываю» + скелет нормpipe v0.2).
