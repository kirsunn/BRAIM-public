# Formula trace, 2026-10-20

**Purpose:** read-only отчёт о том, существует ли в утверждённых источниках смысловой эквивалент формулы «ТЗ = нормы + ситуация + оператор».

**Scope:** только read-only. Никаких правок файлов.

**Status:** evidence для ревью `SPECIFICATION_FORMULA_v0.1.md` и блокировки `ADR-0004`.

## 1. Проверенные файлы

| # | Файл |
|---|---|
| 1 | `BRAIM-public/docs/agents/NORMA_unified_working_package_v0_3.md` |
| 2 | `BRAIM-public/docs/agents/LINKING_MODEL_v0_1.md` |
| 3 | `BRAIM-public/docs/agents/DESIGN_ITERATION_v0_1.md` |
| 4 | `BRAIM-public/docs/agents/ROLES.md` |
| 5 | `BRAIM-public/docs/history/BRAIM_Architecture_Baseline_0.3_2026-09-30.md` |
| 6 | `BRAIM-public/docs/history/BRAIM_CONSOLIDATED.md` |
| 7 | `BRAIM-public/docs/history/baim-legacy/BAIM-LIMS_IFC5_Mapping.md` |
| 8 | `BRAIM/docs/**` |

## 2. Использованные шаблоны

Проверялись:

- точная русская формула;
- вариации «ТЗ = нормы + …»;
- сочетания «нормы + состояние проекта»;
- сочетания «критерии + оператор»;
- «ТЗ формируется …»;
- английские аналоги `requirements + project state`, `specification is derived from`, `requirements + operator`;
- контексты `operator / intent`.

## 3. Что найдено

Сырых совпадений: 4. Уникальных контекстов: 2.

Все совпадения находятся в:

```text
BRAIM-public/docs/agents/SPECIFICATION_FORMULA_v0_1.md
```

Это новый черновик, созданный для сохранения формулы при отказе от метафоры.

## 4. Что не найдено

В следующих источниках совпадений не найдено:

```text
NORMA_unified_working_package_v0_3.md
LINKING_MODEL_v0_1.md
DESIGN_ITERATION_v0_1.md
ROLES.md
BRAIM_Architecture_Baseline_0.3_2026-09-30.md
BRAIM_CONSOLIDATED.md
BAIM-LIMS_IFC5_Mapping.md
BRAIM/docs/**
```

## 5. Вывод

```text
Формула «ТЗ = нормы + ситуация + оператор» — новая.

В утверждённых источниках эквивалент не найден.

Единственный зафиксированный экземпляр —
черновик SPECIFICATION_FORMULA_v0.1.md.
```

Следовательно:

```text
ADR-0004 — Metaphor Is Internal —
не принимается,
пока SPECIFICATION_FORMULA_v0.1
не будет согласован.
```

## 6. Связанные документы

- `docs/agents/SPECIFICATION_FORMULA_v0_1.md`
- `docs/adr/ADR-0009-normative-verification.md`

## 7. Границы отчёта

Отчёт:

- не правит файлы;
- не создаёт новые документы;
- не выполняет push, commit или PR;
- не верифицирует нормативные ссылки;
- не выбирает формат хранения реестра.
