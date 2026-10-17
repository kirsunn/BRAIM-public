# BRAIM Graph Schema v0.1 — единая модель данных (P0-26.1)

> **Провенанс:** вклад автора 2026-10-18 (мини-план: «единый граф, единые ID, версионность, разделить норму и правило»). Это **документ-согласование**, а не код. Цель — чтобы Нормы, Обогащатель, Recipe, Findings жили в **одной семантической модели** и не разъехались по версиям/ID.
> **Когда:** до любого нового кода в `normpipe/`, `enricher/`, `recipes/` — все они сверяются с этой схемой.

## 1. Слой 1: Нормативный

Содержит **«что требует норматив»** (только ссылки/метаданные — L0-N no_full_copies).

```yaml
- norm_id: "SP-54-13330-2022"
  title: "Здания жилые многоквартирные"
  status: mandatory                # mandatory | recommended | regional | conditional | superseded
  effective_from: "2022-06-14"
  publisher: "Минстрой России"
  approval_prk: {number: "361/пр", date: "2022-05-13"}
  amendment: null
  source_url: "https://..."
  source_hash: "sha256:..."        # опционально — для верификации неизменности
  previous_edition: null

- norm_id: "SP-50-13330-2024"
  ...
```

## 2. Слой 2: Пункт + Требование

Связывает норматив → пункт → **что именно требуется** (NormRequirement).

```yaml
- clause_id: "SP-54-13330-2022-cl-4.8"      # Stable ID: norm_id + clause
  document_id: "SP-54-13330-2022"
  clause: "4.8"
  text_excerpt: "…"                    # короткая цитата для верификации (L0-N)
  requirement:
    requirement_id: "req-SP54-4.8-area"   # Stable
    kind: "area_min"                    # = template_id
    operator: ">="
    value: 14
    unit: "м²"
    applicable_to: ["IfcSpace", "жилые_комнаты"]
    severity: "CRITICAL"
    source_hash: "sha256:..."            # snapshot of source at extraction time
    extracted_by: "BRAIM/linguist:14b"
    extracted_at: "2026-10-17T..."
```

**Разделение:**
- `Requirement` — **что** требуется (из норматива)
- `Criterion` (в Skill 6) — **наша нормализованная форма** (с порогом/правилом/etc.)
- `ExecutableRule` (в Skill 4) — **как** мы это проверяем в модели
- `Recipe` (в Skill 5) — **как** мы это считаем

## 3. Слой 3: Модельный (IFC-снапшот)

**Читается только** (immutable, по N1 — снапшот нельзя менять).

```yaml
- snapshot_id: "snap-SP-545-2025-12-15-v1"
  model_name: "SampleProject"
  ifc_version: "IFC 4.3.2.0"
  taken_at: "2025-12-15T10:00:00+00:00"
  element: 
    ifc_guid: "abc123"
    type: "IfcDoor"
    name: "D1*л_1500х2100"
    parent_space: "SPACE-101"     # через IfcRelContainedInSpatialStructure
    properties:
      Width: 0.9
      FireRating: null
  # ...
```

## 4. Слой 4: Зависимости (DEP)

**Связь** между элементами модели: «элемент нуждается в других элементах».

```yaml
- dep_id: "DEP-001"
  name: "Помещение должно быть замкнуто стенами"
  document_id: "SP-48-13330-2019"
  clause: "5.2"
  relation: "enclosed_by"
  parent: "IfcSpace"
  child: "IfcWall"
  min_count: 3
  validation: "geometry.is_closed == true"
  severity: "CRITICAL"
  cascade: ["enriched.set_status:INVALID", "enriched.set_volume:0", "enriched.set_cost:0"]
  evidence_required: true
  approved_by: "human:expert"
```

## 5. Слой 5: Recipe (как считаем)

**Детерминированный расчёт** с подтверждёнными входами.

```yaml
- recipe_id: "thermal_resistance_wall_v0.1"
  version: "0.1"
  status: draft                    # draft | needs_inputs | needs_approval | approved | deprecated
  author: "BRAIM+эксперт"
  approved_by: null
  ifc_version_target: "IFC 4.3.2.0"
  inputs: [...]
  formula: "R_a = 1/alpha_int + sum(δ_i/λ_i) + 1/alpha_ext"
  ...
  # см. recipes/thermal_resistance_wall_v0.1.yaml — это **полный** шаблон
```

## 6. Слой 6: Исполнительский (как проверяем)

**Связь** Requirement + ExecutableRule + Recipe + ModelElement = **проверка** на снапшоте.

```yaml
- executable_rule_id: "ER-001"  # = наш IDS + каскады
  requirement_id: "req-SP54-4.8-area"   # ССЫЛКА на слой 2
  recipe_id: "thermal_resistance_wall_v0.1"  # опционально, если не вычислительная
  ifc_versions: ["IFC 4.3.2.0", "IFC 4.3.1.0"]  # привязка к версии IFC!
  model_classes: ["IfcSpace", "IfcWallStandardCase"]
  template_id: "area_min"
  approved_by: "human:expert"
  deprecation: null
```

## 7. Слой 7: Запуск + Результат

**Воспроизводимый прогон** + **обогащённый оверлей** (не снапшот! по N1).

```yaml
- run_id: "run-2026-10-15-Sample-001"
  snapshot_id: "snap-SP-545-2025-12-15-v1"
  executable_rule_ids: ["ER-001", "ER-002"]
  executed_by: "BRAIM/enricher-v0.2"
  started_at: "2026-10-15T10:05:00"
  completed_at: "2026-10-15T10:05:12"
  findings:
    - finding_id: "f-001"
      element_ref: "abc123"
      rule_id: "ER-001"
      template_id: "area_min"
      verdict: "FAIL"
      actual: 12.5
      required: 14.0
      unit: "м²"
      source: "СП 54.13330.2022, п. 4.8"
  enriched_overlay:
    "abc123": {cascades: [...], status: "INVALID", volume_m3: 0}
  # ошибка — нумеруются findings, overlay — в обогащённый СЛОЙ, а не в снапшот
  # см. N1 в методологии GRAPHS_AND_SNAPSHOTS_v0_1
```

## 8. Кто чем владеет — соглашение

| Сущность | Где живёт | Кто пишет |
|---|---|---|
| `NormDocument` (слой 1) | `Braim-Registry` (P0-28, `docs/registry/`) | Регистратор (автоматически + ручная правка) |
| `Clause` + `Requirement` (слой 2) | `norm_graph_v0.2.json` (DEP) + `templates_v0.1.yaml` (templates) + `normbase_seed/` (extracted) | Обогащатель + Эксперт-валидатор |
| `Snapshot` (слой 3) | `snapshots/SNAP-*/` (immutable) | Обогащатель v0.1 (IFC input) |
| `Dependency` (слой 4) | `core/norm_graph_v0.2.json` (DEP) | Автор (rules — не машина) |
| `Recipe` (слой 5) | `recipes/*.yaml` | Эксперт-валидатор + Регистратор |
| `ExecutableRule` (слой 6) | `templates/` + generation script → IDS + обогатитель v0.3 | Обогащатель (генератор) + Эксперт-валидатор (подтверждение) |
| `Run` (слой 7) | `reports/run-*/` (validation-result.json) | Обогащатель v0.2 (исполнитель) |

## 9. ID-конвенция — **самое срочное**

```
norm_id:      SP-{N}-{NNNNN}-{YYYY}              # SP-54-13330-2022
clause_id:    {norm_id}-cl-{NN[.NN[.NN]]}         # SP-54-13330-2022-cl-4.8
requirement_id: req-{norm_id}-cl-{NN}-{slug}   # req-SP54-13330-2022-cl-4.8-area-min
criterion_id: nrm_{hash4}                       # наш внутренний, не связан с norm_id
dep_id:       DEP-{NNN}                           # DEP-001
recipe_id:    {slug}-v{N.M}                      # thermal_resistance_wall-v0.1
exec_rule_id: ER-{NNN}                          # ER-001
snapshot_id:  snap-{slug}-{YYYY-MM-DD}-v{N}     # snap-SP-545-2025-12-15-v1
run_id:       run-{YYYY-MM-DD}-{slug}-{NNN}      # run-2026-10-15-Sample-001
finding_id:   f-{NNN}                            # f-001
ifc_guid:     оставляем IFC-формат (22 символа)
```

**Цель:** `req-SP54-13330-2022-cl-4.8-area-min` в `norm_graph` — это **тот же ID**, что и в `IDS-file` и в `validation-result.json`. Один ID на все 7 слоёв.

## 10. Что выбираем для ID: **человекочитаемые slug vs hash**

| Подход | Плюсы | Минусы |
|---|---|---|
| Человекочитаемый (`req-SP54-...-area-min`) | Видно глазом, ссылаешься в обсуждении | Длинные, меняются при переформулировке нормы |
| Hash (`nrm_a7f3e2`) | Стабильные, короткие | Невидимые, трудно найти |

**Решение:** для **Requirement и Criterion** — slug (человекочитаемо); для **Finding, Run, Snapshot** — slug+timestamp; для внутренних служебных — hash. **NormDocument, DepRule, Recipe** — slug (мы их называем).

## 11. Версионирование — **отдельное для каждого слоя**

| Слой | Версия | Как меняется |
|---|---|---|
| Норматив | `edition` (2022) + `amendment` | Редакции СП/ГОСТ (с ПП 614) |
| Requirement | `version` (1.0) | Пересмотр формулировки |
| Recipe | `version` (0.1) | Уточнение методики |
| ExecutableRule | `version` (1.0) | Изменение IDS, каскадов |
| IFC-снапшот | `version` (1, 2, …) | Каждое новое извлечение |
| Finding | `finding_id` (без версии) | Один finding = один факт |
| Validation Run | `run_id` (timestamp) | Каждый запуск |

**Правило:** Finding — **неизменный** (как кадр в бухгалтерии), Snapshot — **неизменный** (immutable), Run — **неизменный** (audit trail), а Requirement, Recipe, ExecutableRule — **версионируются**.

## 12. Аналоги OSCAL (без перехода на OSCAL)

OSCAL нам даёт паттерны, а не формат:

| OSCAL | BRAIM |
|---|---|
| Catalog | `norm_graph.json` (deps) + `NORMPACK_*.yaml` (выборки) |
| Profile | `recipes/normpack_*.yaml` (комбинации для объекта) |
| Control | `ExecutableRule` (слой 6) |
| Assessment Plan | `run` (слой 7) с выбором snapshot + rule_ids |
| Finding | `finding_id` в `validation-result.json` |
| Evidence | `provenance[]` (rule_id + snapshot_id + extraction_id) |

## 13. Аналоги SHACL (без RDF)

| SHACL | BRAIM |
|---|---|
| Shape | `templates_v0.1.yaml` (pattern для критерия) |
| Target | `applicability` (Condition, IFC-class) |
| Property Path | `attribute` (например, `width_m` → IfcDoor.Width) |
| Validator | `enricher_v02.py` (Применяет rules к snapshot) |
| Report | `validation-result.json` |
| Severity | `severity: critical \| major \| minor \| information` (у нас: critical/high/medium/low/info — но лучше привести к SHACL-совместимому) |

**Принципиально:** SHACL-формат не нужен. Нам нужна **декларативная** дисциплина (как в SHACL), а не SHACL-движок. Наши `enricher_v02.py` — это и есть наш мини-SHACL.

## 14. Чек-лист «согласовано» (следующая неделя)

- [ ] Всё, что называется `requirement_id` / `criterion_id` / `rule_id` — проходит через **одну ID-фабрику** (нет ручных правок)
- [ ] `norm_graph_v0.2.json` + `templates_v0.1.yaml` + `recipes/*.yaml` — используют **одни** ID, **без дублей** по NormDocument
- [ ] `enricher_v02.py` — issue содержит `requirement_id` (а не свой внутренний id)
- [ ] `validation-result.json` — содержит поля `snapshot_id`, `run_id`, `executable_rule_id`, `finding_id`
- [ ] `Braim-Registry` (P0-28) — хранит `documents[].norm_id + edition + status`; не дублирует, а **только ссылается** на `Requirement` (слой 2)
- [ ] Versioning: 1 пример в `recipes/` (recipe версия → snapshot версия → finding версия)
- [ ] Audit trail: в `finding` указываем `provenance.requirement_id` (а не «непонятный номер»)

## 15. Что я НЕ делаю в этой схеме

- **Не переходим на RDF/SHACL** (автор явно сказал — «не переходим сейчас»)
- **Не вводим новый ID-генератор** — используем простые human-readable slug
- **Не делаем обратную совместимость** для всего старого — обновляем в 3-файлах и коммитим
- **Не делаем migration scripts** — для MVP достаточно «найди и замени»

## 16. Changelog

- 0.1 — 2026-10-18: идея + скелет схемы по 7 слоям; ID-конвенция; версионирование; OSKAL/SHACL аналоги; чек-лист.
