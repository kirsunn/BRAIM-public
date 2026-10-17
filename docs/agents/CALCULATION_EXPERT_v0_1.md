# Расчёты + человек-эксперт в BRAIM — роль и формат (P0-31)

> **Провенанс:** вклад автора, 2026-10-17. Базовый шаблон — `NormCalcRecipe` (автор). Цель — сделать **каждый расчёт проверяемым артефактом**, а не «результатом доверия LLM».
> **Принцип:** BRAIM = **оркестратор и валидатор**, не «полный расчётный комплекс». Расчёты делают внешние инструменты (NormCAD, ЛИРА, SCAD, Excel) или внутренний движок; BRAIM проверяет входы, воспроизводимость, единицы, ссылки на пункты и **сам не выдумывает значения**.

## 1. Два режима расчётов

| Режим | Что BRAIM делает | Когда |
|---|---|---|
| **Проверка (validation-only)** | Получает уже выполненный расчёт — проверяет входы, единицы, пределы, ссылки на редакцию, воспроизводимость формулы | 80% случаев (NormCAD, ЛИРА, Excel-таблицы) |
| **Автопроверка (calculation)** | Сам собирает входы из IFC + контекста проекта, применяет рецепт; если не хватает — возвращает **INDETERMINATE + список missing inputs** (G-3: не угадывать) | Только для «замкнутых» рецептов с однозначными входами |

## 2. Роль: **Эксперт-валидатор** (P0-31, новая роль в команде)

В lifecycle стадия 6 APPROVE (G-5) сейчас «человек-эксперт утверждает». Это **включает**:

- **Подтверждение расчёта** — проверил по входам/формуле/выходу, выносит verdict: `accepted` / `rejected` / `needs_revision` (а не «LLM-придумал»).
- **Подтверждение рецепта** — версионирует `NormCalcRecipe` (recipe_id, edition, author, date).
- **Подтверждение наследования значения** (для Артефакта-Археолога, P0-30) — принимает `value_inherited_from: {doc, edition, clause}`.
- **Эскалация к человеку-проектировщику** — «переменная X задана как допустимое приближение 0.85, нужно уточнение».

В Expert Console это уже работает (✓/✗). Добавить вердикт «recipe approved / rejected» = **новая колонка** в decisions.json, без изменения архитектуры.

## 3. Тип правила `calculation` в `norm-criterion.json`

Расширение `check.kind` (для v0.2):

```yaml
- threshold:   # как сейчас: value, unit, operator
- presence:    # как сейчас
- computed:     # value вычисляется из других (как сейчас, без рецепта)
- script:       # ссылка на версионированный скрипт (как сейчас)
- calculation:  # НОВОЕ — NormCalcRecipe целиком
```

Поля `calculation`:
```yaml
recipe_ref: "thermal_resistance_wall_v0.1"   # ссылка на recipes/thermal_resistance_wall_v0.1.yaml
inputs:
  - {symbol: R_req,  label: "требуемое сопротивление", unit: "м²·°C/Вт", source: "СП 50.13330, табл.3"}
  - {symbol: alpha,  label: "коэффициент теплоотдачи внутр.", unit: "Вт/(м²·°C)", value: 8.7, source: "СП 50.13330, п.5.7"}
formula: "R_a = 1/alpha + sum(δ_i/λ_i) + 1/alpha_ext"
output_unit: "м²·°C/Вт"
check: {operator: ">=", against: "R_req", message: "..."}
evidence: {intermediate_steps: true, intermediate_vars: [...]}
```

## 4. Шаблон `NormCalcRecipe` (v0.1)

```yaml
# recipes/thermal_resistance_wall_v0.1.yaml
recipe_id: thermal_resistance_wall_v0.1
version: "0.1"
author: "BRAIM+эксперт"
approved_by: "human:kirsunn"
approved_at: "2026-10-17"
status: approved   # approved | draft | deprecated

normative_reference:
  - document_id: SP50.13330
    edition: "2012"
    clause: "п.5.7, табл.3"
    source_hash: "sha256:..."   # опционально — для проверки неизменности
    verified_by: "human:expert"

applicability:
  building_use: ["DOO", "жилые"]
  object_type: ["IfcWall", "EXTERNAL"]
  conditions: ["климатический_район:любой"]

inputs:
  - {symbol: alpha_int,  label: "коэффициент теплоотдачи внутренней поверхности",  unit: "Вт/(м²·°C)", source: "табл.4"}
  - {symbol: alpha_ext,  label: "коэффициент теплоотдачи наружной поверхности",        unit: "Вт/(м²·°C)", source: "табл.4"}
  - {symbol: R_req,      label: "требуемое приведённое сопротивление теплопередаче",  unit: "м²·°C/Вт", source: "табл.3"}
  - {symbol: layers,     label: "слои ограждения (толщина δ_i, теплопроводность λ_i)", unit: "[м; Вт/(м·°C)]", source: "IFC + ручной ввод"}

formula: "R_a = 1/alpha_int + sum(δ_i/λ_i) + 1/alpha_ext"
output_unit: "м²·°C/Вт"
check:
  operator: ">="
  against: "R_req"
  message: "Фактическое сопротивление теплопередаче ниже нормативного"
evidence:
  intermediate_steps: true
  intermediate_vars: ["R_in=1/alpha_int", "R_layers=sum(δ_i/λ_i)", "R_out=1/alpha_ext"]
  show_substitution: true
```

## 5. MVP — теплопроводность стены

| Шаг | Что |
|---|---|
| 1 | `recipes/thermal_resistance_wall_v0.1.yaml` (шаблон выше) |
| 2 | `--recipe` подкоманда в Обогащателе v0.3: считывает входы → считает → сравнивает с лимитом |
| 3 | Тестовые IFC: pass / fail / missing_inputs / invalid_unit |
| 4 | Отчёт в `reports/calc_thermal_<id>.json` с промежуточными шагами (для проверяемости) |
| 5 | НЕ начинать с конструкций — там ответственность за результат |

## 6. Что точно не делаем

- Копировать модули/таблицы/алгоритмы NormCAD (проприетарно)
- «LLM придумал порог» — у нас в rule `value` + `source` (G-3)
- Расчёты без доказательства: каждый шаг расчёта логируется в `evidence`
- Заменять эксперта: «проверяет — утверждает — эскалирует» — ровно роль P0-31

## 7. Changelog

- 0.1 — 2026-10-17: идея и шаблон от автора; роль Эксперт-валидатор (P0-31); MVP — теплопроводность стены.
