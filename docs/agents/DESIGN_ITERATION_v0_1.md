# Design Iteration Loop v0.1 (P0-32, вклад автора)

> **Провенанс:** вклад автора 2026-10-18. Принцип: **не «ИИ решает», а «ИИ ведёт цикл»**. Три уровня автономии, четыре механизма защиты от зацикливания, четыре сущности.

## 1. Принцип

> **ИИ-агент ведёт ограниченный цикл проектирования: предлагает допустимые варианты, проверяет их через BRAIM, откатывает ухудшения и эскалирует конфликт человеку.**
>
> Агент может работать без человека **только в пределах заранее утверждённых политик** и **никогда не принимает нормативно ответственные решения сам**.

## 2. Три уровня автономии (SUGGEST / AUTO_SAFE / ESCALATE)

| Режим | Кто выбирает | Пример |
|---|---|---|
| **`SUGGEST`** | ИИ предлагает, человек утверждает | Изменить толщину утеплителя, добавить стену |
| **`AUTO_SAFE`** | ИИ выбирает из заранее разрешённого списка | Пересчёт recipe после изменения входа; выбор допустимого типоразмера |
| **`ESCALATE`** | Никто: цикл останавливается | Конфликт норм, нет сходимости, исчерпаны лимиты, критическое решение |

## 3. Четыре механизма защиты от зацикливания

### 3.1. Явный критерий успеха

```yaml
success_criteria:
  - "all target_findings are RESOLVED|NOT_APPLICABLE|WAIVED"
  - "no new CRITICAL findings"
  - "all required inputs available"
  - "calculations approved|pending_human"
  - "no regression: number of CRITICAL/HIGH ≤ previous iteration"
```

Итерация без измеримого критерия **не должна запускаться**.

### 3.2. Лимиты

```yaml
limits:
  max_iterations: 5
  max_model_changes: 20
  max_llm_calls: 30
  max_wallclock_seconds: 600
  on_no_progress: ESCALATE
```

Лимиты — стандартная защита от бесконечных циклов и исчерпания ресурсов.

### 3.3. Детектор повторов (fingerprint)

```yaml
fingerprint_inputs: ["snapshot_id", "findings_summary", "changed_guids", "key_parameters"]
on_duplicate: STOP
on_regression: ROLLBACK
```

**Fingerprint** = снимок состояния. Если повторяется — цикл останавливается. Если хуже предыдущей итерации — откат к последней допустимой.

### 3.4. Правило «не ухудшать»

Принимаем вариант, **только если**:

- CRITICAL не вырос;
- HIGH не вырос без компенсации;
- целевые findings улучшились;
- не нарушены `forbidden_actions`;
- все расчёты (recipes) — `status_calc: APPROVED|REJECTED`, не `PENDING` без причины.

## 4. Четыре сущности (слои поверх существующих)

### 4.1. `IterationPolicy` — заранее утверждённые правила

```yaml
policy_id: house_residential_mvp_v0.1
version: "0.1"
applicable:
  building_type: ["МКД"]
  building_height_max_m: 75
  region: ["Москва"]

allowed_actions:           # AUTO_SAFE — без человека
  - "adjust_wall_position"   # в пределах min_room_area
  - "adjust_door_width"      # в пределах min_door_width
  - "regenerate_layout_variant"  # из каталога утверждённых
  - "run_enricher"
  - "run_recipe"
  - "select_typ_size_from_catalog"  # каталог утверждён

forbidden_actions:          # всегда человек
  - "change_approved_recipe"
  - "change_norm_requirement"
  - "publish_report"
  - "export_bcf"
  - "modify_structural_loads"  # конструктив — за человеком

success_criteria:
  - "all target_findings RESOLVED|NOT_APPLICABLE|WAIVED"
  - "no new CRITICAL"
  - "all recipes APPROVED|REJECTED"

limits:
  max_iterations: 5
  max_model_changes: 20
  max_llm_calls: 30
  max_wallclock_seconds: 600

fingerprint_inputs: ["snapshot_id", "findings_summary", "changed_guids", "key_parameters"]
on_duplicate: STOP
on_regression: ROLLBACK
on_no_progress: ESCALATE

approved_by: "human:kirsunn"
```

### 4.2. `DesignVariant` — кандидат решения

```yaml
variant_id: "V003"
iteration_id: "iter-007"
policy_id: "house_residential_mvp_v0.1"
base_snapshot: "snap-SP-545-2025-12-15-v1"

changes:
  - "increase_door_width 0.9 → 1.2"
  - "recompute_R_a"
rationale: |
  DEP-001 (нет стен) был закрыт добавлением стены в ИУЛ 2.3.
  Этот вариант ещё добавляет 0.3м к ширине двери (СП 59.13330 табл. 6.1)
  чтобы исключить finding FIRE-EVAC-001.

expected_score:
  critical_count: 0
  high_count: 0
  area_m2: 64.5
  cost: 14_200_000

check_results:
  - finding_id: "DEP-001"
    verdict: "RESOLVED"
  - finding_id: "FIRE-EVAC-001"
    verdict: "RESOLVED"

requires_human_approval: true
approved_by: null
```

### 4.3. `IterationRun` — прогон цикла

```yaml
run_id: "iter-007"
policy_id: "house_residential_mvp_v0.1"
input_snapshot: "snap-SP-545-2025-12-15-v1"
target_findings: ["DEP-001", "FIRE-EVAC-001"]

started_at: "2026-10-15T10:00:00"
completed_at: "2026-10-15T10:00:18"
final_state: "ESCALATE"   # SUGGEST | AUTO_SAFE | ESCALATE

variants_evaluated:
  - variant_id: "V001"
    generated_by: "agent:llm-gpt4-style"
    score: {critical: 1, high: 0}
    status: "rejected"      # no improvement
  - variant_id: "V002"
    generated_by: "agent:catalog_gen_2"
    score: {critical: 0, high: 0, area: 65.0}
    status: "candidate"     # meets criteria, pending human
  - variant_id: "V003"
    generated_by: "agent:catalog_gen_3"
    score: {critical: 0, high: 0, area: 64.5}
    status: "approved"      # BEST

fingerprint: "fpr-2026-10-15-100018-iter007"   # двойной хеш состояния
```

### 4.4. `Escalation` — нельзя продолжать

```yaml
escalation_id: "esc-007"
run_id: "iter-007"
reason: "no_progress"     # no_progress | conflict | missing_data | limit_exceeded | conflict_norm
details: |
  Итерации 1-5 не привели к сходимости.
  Fingerprint: fpr-2026-10-15-100018 vs fpr-2026-10-15-100014 — повтор.
  Targets: DEP-001 (стен нет), FIRE-EVAC-001 (дверь <1.2) — оба зависли.
attempted_actions:
  - "add_wall in_zones:z2_3,2_4"
  - "increase_door_width 0.9→1.2 in_d:door_main"
  - "relocate_room_partition"
human_action_required:
  - "specify_acceptable_zones_for_walls"
  - "approve_standard_door_width:1.2"
```

## 5. MVP «автоисправление одного finding» (первый рабочий сценарий)

1. **enricher v0.3** находит `DEP-001: помещение SPACE-102 без стен`;
2. **agent** предлагает **2–3 варианта** из утверждённого каталога (добавить стену в зоне X / Y / пометить пространство как открытое);
3. **enricher** прогоняет **каждый** вариант, считает findings и метрики;
4. **agent** сравнивает: только варианты, **снижающие** CRITICAL без увеличения HIGH, идут в кандидаты;
5. Если **один** однозначно лучше — `SUGGEST` (человек утверждает);
6. Если **несколько** — все в отчёт, `ESCALATE`;
7. Если **все ухудшают** — `ROLLBACK` к предыдущему snapshot, `ESCALATE` с описанием.

## 6. Связь с существующими слоями (GRAPH_SCHEMA v0.1)

| Слой | В GRAPH_SCHEMA | В новом design cycle |
|---|---|---|
| Нормативный | `NormDocument`, `Requirement` | `IterationPolicy.allowed_actions` (что *можно* менять) |
| Модельный | `Snapshot` | `IterationRun.input_snapshot` |
| Зависимостный | `DEP-001` | → становится `target_findings[0]` |
| Recipe | `Recipe` | `DesignVariant.changes[]` (recipe v0.1 уже поддерживает calc-changes) |
| Исполнительский | `ExecutableRule` | `IterationRun.variants_evaluated[].check_results` |
| Результатный | `Finding` | `Escalation.reason` + `DesignVariant.check_results[].verdict` |

**Новых типов слоёв нет** — мы только добавляем динамику поверх существующих 7 слоёв.

## 7. Что **точно не делаем** (NOT-DOING)

- **Не делаем** автономное проектирование (Phase 3+, L16-GN).
- **Не используем** LangGraph как зависимость — паттерн берём, но реализуем сами.
- **Не делаем** `commit_approved_recipe` без человека (NOT-DOING §12).
- **Не публикуем** отчёт/BCF автоматически.
- **Не модифицируем** нормативы.

## 8. Дорожная карта

| Шаг | Что | Когда |
|---|---|---|
| 1 | IterationPolicy шаблон (мы уже знаем структуру) | **Сейчас** — после этого коммита |
| 2 | enrichment loop в v0.3 (каждое изменение → перезапуск enricher) | Phase 1 (v0.4) |
| 3 | fingerprint и детектор повторов | Phase 1 (v0.4) |
| 4 | v0.5 — минимальный MVP: enricher v0.3 + LLM-loop + 1 demo на СП-545 | Phase 1 |
| 5 | v0.6 — полноценный цикл: agent предлагает, enricher валидирует, rollback | Phase 2 |
| 6 | v1.0 — multi-policy, multi-объект | Phase 2+ |

## 9. Changelog

- 0.1 — 2026-10-18: идея + 4 сущности + 3 уровня автономии + 4 механизма защиты + MVP.
