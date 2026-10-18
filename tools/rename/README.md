# Filename normalization toolkit

Вариант A: полное переименование с сохранением audit trail.

## Контракт имён

`PREFIX-ID[-EDITION][-SUFFIX].ext`

Примеры:
- `SP-252.13330-2022.pdf`
- `SP-252.13330-2022-IZM-3-887pr-2024-12-20.pdf`
- `GOST-21.1101-2023.pdf`
- `FZ-384-2009.pdf`
- `PDF-2026-10-18-unrecognized-name.pdf`
- `IFC-AGR-001-2026-10-18.ifc`

## Порядок

1. Сделать полную копию исходной папки.
2. Запустить dry-run:
   `python tools/rename/normalize_names.py --source TN_DOWNLOADS --map tools/rename/doc_type_map.csv --dry-run`
3. Проверить `doc_type_map.csv`.
4. Выполнить переименование без `--dry-run`.
5. Проверить: количество файлов не уменьшилось; нет `error`; нет дублей целевых имён.
6. Только после проверки — нормализовать `download/`; `_library/normative/sp_extracted/` пока не трогать.

## Роли

- Адаптатор: нормализация входных имён до EXTRACT.
- Регистратор: ведение `doc_type_map.csv`.
- Инспектор: проверка количества, дублей, статусов и целостности.

## Ограничения

Скрипт распознаёт базовые шаблоны SP/GOST/GOST-R/SNiP/SanPiN/FZ. Сложные случаи попадают в `PDF-*` и требуют ручного уточнения в mapping-таблице. Он не определяет юридическую актуальность или редакцию норматива.
