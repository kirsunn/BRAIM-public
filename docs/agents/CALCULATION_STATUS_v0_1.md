# Статусы расчётной задачи (P0-31, v0.2)

> **Провенанс:** вклад автора, 2026-10-17 (handoff-документ `BRAIM_norm_calculator_handoff.md`).
> Положение: `docs/agents/CALCULATION_EXPERT_v0_1.md` § 2 + `norm-criterion.json` (новый тип `calculation`).

## 1. Семь статусов (на один расчёт)

| Статус | Значение | Что делать |
|---|---|---|
| `INPUT_REQUIRED` | Не хватает обязательных входов | `to_calculate` список; Обогащатель — `missing_inputs` |
| `READY_FOR_REVIEW` | Данные собраны, но **расчёт ещё не выполнен** (человек должен подтвердить входы перед запуском) | operator_review |
| `CALCULATED` | Расчёт выполнен, но **не утверждён человеком** | Готов к показу в Expert Console |
| `REVIEW_REQUIRED` | Конфликт данных / неоднозначность / ручной ввод, который не согласован | Срочно к человеку-валидатору (P0-31) |
| `APPROVED` | Человек подтвердил результат | Закрытая запись в `reports/calc_*.json` (нельзя изменять без новой ревизии) |
| `REJECTED` | Расчёт или входные данные отклонены | `rejected_by: human:<id>`, `reason: <text>` |
| `NOT_APPLICABLE` | Условия применимости не выполнены | Снимок: `conditions_satisfied: false` |

**Критически:** `CALCULATED ≠ APPROVED`. Это разделение — основание для forensic-вертикали: «что показано расчётчиком» ≠ «что утверждено в дело».

## 2. Расширение `norm-criterion.json` (v0.2)

Новый `check.kind: calculation` (уже было) + новые поля в `check.calculation`:

```yaml
check:
  kind: calculation
  recipe_ref: thermal_resistance_wall_v0.1
  inputs:
    - {symbol: alpha_int, required: true}
    - {symbol: alpha_ext, required: true}
    - {symbol: R_req, required: true}
    - {symbol: layers, required: true}
  formula: "R_a = 1/alpha_int + sum(δ_i/λ_i) + 1/alpha_ext"
  output_unit: "м²·°C/Вт"
  # статусы и качество — вычисляются движком, не вручную
  status_calc: CALCULATED          # INPUT_REQUIRED | READY_FOR_REVIEW | CALCULATED | REVIEW_REQUIRED | APPROVED | REJECTED | NOT_APPLICABLE
  status_provenance:
    calculated_by: normpipe/calc-v0.1
    calculated_at: "2026-10-17T19:00:00+00:00"
    inputs_hash: "sha256:..."         # для определения STALE
  # если STALE — отдельный маркер
  stale: false
  stale_reason: null                # если true: "изменился слой X в IFC" и т.п.
  approval:
    required: true
    reviewer_role: "engineer"
    approved_by: null
    approved_at: null
```

## 3. «Расчёт устарел» — Quality Gate

> «При изменении входного параметра расчёт помечается как устаревший»

**Механика:**
1. После каждого прогона Обогащателя сохраняем `inputs_hash` (sha256 от конкатенации значений входов);
2. На следующем прогоне сравниваем текущий `inputs_hash` с сохранённым;
3. Если отличается — `stale: true`, `stale_reason: "изменился слой X"` (берём дифф по IFC-объектам);
4. Расчёт **не удаляется** (это доказательный артефакт), но `status_calc` → `REVIEW_REQUIRED`.

**Связь с lifecycle:** переход в `REVIEW_REQUIRED` — это «расчёт более не доверенный» → идёт в `to_calculate` отчёт Обогащателя. НЕ сразу в `APPROVED`.

## 4. Шаблон отчёта для экспертизы (8 разделов)

Согласно handoff, отчёт содержит:

```
РАСЧЁТ № BRAIM-CALC-0001
1. Задача расчёта
2. Нормативная база: документ, редакция, изменение, пункт
3. Исходные данные: параметр, значение, единица, источник, статус
4. Методика: формула, переменные, допущения
5. Расчёт: формула → подстановка → промежуточные значения → результат
6. Проверка критерия: фактическое vs требуемое
7. Вывод расчётчика
8. Утверждение: кто выполнил, проверил, утвердил, дата, версия
```

Реализуем как YAML-шаблон `report_template_v0.1.yaml` в `_library/templates/`. Каждый раздел → поле в `recipe.output`; Обогащатель заполняет автоматически, человек-валидатор — финальное утверждение.

## 5. Что **точно** не делаем

- Не выдаём `APPROVED` без человека (NOT-DOING § 12, § 18)
- Не выдаём `APPROVED` для расчётов конструкций (ответственность, § 5)
- Не обещаем «гарантированно пройдёт экспертизу» (handoff, § 218-222)
- Не «выдумываем» значения (G-3)
- Не заменяем специализированное ПО (NOT-DOING § 14)

## 6. Changelog

- 0.1 — 2026-10-17: handoff → 7 статусов + STALE-механика + шаблон отчёта для экспертизы.
