# BRAIM Lifecycle Model

## Статус

- Версия: `0.1.0` (draft)
- Дата: 2026-10-15
- Назначение: scoped-модель фаз жизненного цикла, статусов проверки и переходов
- Основания: промпт независимого анализа §9 (`docs/analysis/`), EIM Maturity Profile v0.2 draft, adversarial-ревью BAIM-LIMS v1.0 (§2.2), CDE State Machine v0.1

> Документ фиксирует модель ЖЦ как спецификацию v0.1. Он не является нормативным заявлением о российских стадийностях (ПП/РД/экспертиза) — словарь стадий конфигурируемый (см. LC-02, R-05).

---

## 1. Решения (LC-01..LC-07)

| ID | Решение | Смысл |
|---|---|---|
| LC-01 | **Scoped lifecycle** | ЖЦ принадлежит scope-у (проект, здание, этаж, помещение, подзона, система, элемент), а не «элементу вообще». Элемент наследует ЖЦ охватывающего scope, если явно не переопределён. Прямой ответ на фатальную претензию ревью LIMS §2.2 |
| LC-02 | **Четыре раздельные оси** | `phase` → `stage` → `transition` → `status` (см. §3). Смешение осей запрещено (урок §2.4 ревью LIMS: профиль не смешивает измерение и требование) |
| LC-03 | **Шесть статусов проверки** | `PASS / FAIL / UNKNOWN / INCOMPLETE / NOT_APPLICABLE / STALE` — канонический набор; точная семантика в §5 |
| LC-04 | **Переход = Decision + новый Snapshot** | Переход ЖЦ всегда оформляется как decision (`decision.json`, `decision_type: approval`) + запечатанный snapshot (`snapshot.json`). Валидация сама никогда не двигает ЖЦ (human-in-the-loop) |
| LC-05 | **LC и cde_state — независимые оси** | Контейнер в `WIP` может описывать объект в `OPERATION` (as-built обследование). Автоматической связки нет — только осознанное соответствие (§7) |
| LC-06 | **Конфликты scope не разрешаются молча** | Элемент в нескольких scope с разными ЖЦ имеет отдельный LC-view на каждое участие; унификация — только явным decision с rationale/waiver |
| LC-07 | **Хранение вне IFC** | IFC не моделирует историю (`IfcOwnerHistory` — только последнее изменение). LC-утверждения — first-class записи реестра; в IFC экспортируются опционально как Pset-расширение (Phase 2+), не как source of truth |

---

## 2. Основные понятия

```text
Scope        — контекст, владеющий ЖЦ: project, site, facility, building,
               section, storey, apartment, space, subzone, system,
               element, work_package
LC Statement — утверждение «scope S в итерации I находится в P/S/M»
               (schema: braim-spec/schemas/lifecycle-state.json, id: lc_)
LC View      — LC Statement для одного участия элемента в scope
               (элемент может иметь несколько views)
Transition   — управляемый перевод scope: from → to (§4)
Gate Result  — результат одной проверки в момент перехода (§5)
```

Запись состояния (компактная форма, машиночитаемая и говорящая):

```text
LC:P=DESIGN/S=DESIGN_DOC/T=VALIDATE/M=IN_TRANSITION
```

где `P` — фаза, `S` — стадия, `T` — текущий процесс перехода, `M` — статус scope. Вне перехода `T` опускается: `LC:P=OPERATION/S=USE/M=ACTIVE`.

---

## 3. Оси: phase / stage / transition / status

### 3.1. Phase (макрофаза жизни scope)

```text
DESIGN → CONSTRUCTION → OPERATION → RECONSTRUCTION → OPERATION → … → DEMOLITION
```

Фиксированный перечень: `DESIGN | CONSTRUCTION | OPERATION | RECONSTRUCTION | DEMOLITION`. `RECONSTRUCTION` может возвращать scope в `OPERATION`; `DEMOLITION` терминальна.

### 3.2. Stage (стадия внутри фазы)

Словарь **по умолчанию** (конфигурируется проектной политикой, аналог BRAIM-LIMS):

| Phase | Stage (default) |
|---|---|
| DESIGN | `CONCEPT` → `SKETCH` → `DESIGN_DOC` → `WORKING_DOC` |
| CONSTRUCTION | `PREPARATION` → `EXECUTION` → `COMMISSIONING` |
| OPERATION | `USE` → `MAINTENANCE` |
| RECONSTRUCTION | `SURVEY` → `DESIGN` → `EXECUTION` → `ACCEPTANCE` |
| DEMOLITION | `PLANNING` → `EXECUTION` |

> ⚠️ Названия стадий — машинные коды проекта, **не** утверждение о соответствии российским стадиям ПП/РД/экспертизы. Отображение на нормативную стадийность — предмет policy pack (открытый вопрос LCQ-01).

### 3.3. Transition (процесс)

```text
VALIDATE → REVIEW → APPROVE
```

Действие, выполняемое над scope при переводе. Фиксирует, *что происходит*, а не *в каком состоянии объект*.

### 3.4. Status (состояние scope)

```text
ACTIVE | IN_TRANSITION | VALIDATED | APPROVED | BLOCKED | RETIRED
```

---

## 4. Модель перехода

Переход ЖЦ — управляемая транзакция, а не смена поля:

```text
Transition Request:
  scope_ref, kind
  from: LC:P=…/S=…/M=…        to: LC:P=…/S=…/M=…
  required_profile: EIM (G-D-C-M-P-R-V, фактический формат — EIM v0.2)
  gates: [rule_id…]
  evidence: [artifact_ref…]

Результат (атомарно):
  1. Gate results по каждому rule_id (§5)
  2. Decision (decision.json, decision_type: approval, decided_by: роль из policy)
  3. Новый sealed snapshot (snapshot.json)
  4. Новый LC Statement (lifecycle-state.json) с transition_ref = decision_id
```

Правила:

1. Переход невозможен без decision — валидации создают gate results, но не двигают ЖЦ.
2. Gate result в `FAIL` → `no_go` (согласуется с D-03: Critical→No-Go).
3. Gate result в `UNKNOWN`, `INCOMPLETE` или `STALE` **блокирует** переход (не является ни PASS, ни FAIL — это отсутствие доказательства).
4. Waiver возможен только через decision (`decision_type: waiver`) с rationale — молчаливых пропусков нет.
5. Участие элементов в переходе фиксируется ролями: `retained | replaced | new | removed` — в transition-записи, не в элементе.

---

## 5. Статусы проверки (канон)

| Статус | Семантика | Блокирует переход? |
|---|---|---|
| `PASS` | Проверка выполнена, требование подтверждено на текущем snapshot | нет |
| `FAIL` | Проверка выполнена, требование нарушено | да (`no_go`) |
| `UNKNOWN` | Проверка не выполнялась или результат не интерпретируем | да |
| `INCOMPLETE` | Доказательства не хватает частично (не все охваты/не все данные) | да |
| `NOT_APPLICABLE` | Требование неприменимо к данному scope/операции (с обоснованием) | нет |
| `STALE` | Результат устарел: разошёлся snapshot_id или policy_pack_digest | да |

Правило STALE (детерминированное): gate result привязан к тройке `(snapshot_id, policy_pack_digest, checked_at)`. Если текущий snapshot или digest политики не совпадают с зафиксированными в результате — результат автоматически `STALE`. Никакой эвристики «похоже, устарело».

Согласование с EIM v0.2: `INDETERMINATE` переименовывается в `UNKNOWN` (в следующей ревизии EIM), набор расширяется `INCOMPLETE` и `STALE`.

---

## 6. Смешанные и федеративные случаи

Ответы на фатальные примеры ревью LIMS §2.2:

| Случай | Как модель его описывает |
|---|---|
| Стена W1 между R1 (RECONSTRUCTION) и R2 (OPERATION) | У W1 нет «одного ЖЦ». Два LC-view: участие в R1 (например, роль `replaced`) и в R2 (роль `retained`). Унификация — только явным decision |
| Система отопления через несколько помещений | Система — самостоятельный scope (`kind: system`) со своим ЖЦ; помещения — свои |
| Федеративная модель / комплект документации | Федеративная сборка — scope (`kind: project` или `work_package`); контейнеры — cde_state (LC-05) |
| Дверь в стене, монтируемая в составе стены | Дверь — элемент; её LC-view наследует ЖЦ этажа/секции, участие в переходе стены — ролью |
| Расчёт на элементах из разных фаз | Расчёт — артефакт с provenance; его gate results ссылаются на конкретные snapshot_id; разные фазы входов → `STALE`/`INCOMPLETE` по правилу §5 |

---

## 7. Связь с другими механизмами

| Механизм | Связь |
|---|---|
| CDE State Machine v0.1 | Независимая ось контейнера (`WIP/SHARED/PUBLISHED/ARCHIVE`). LC описывает объект, cde_state — документ. Типовые сочетания для пилота фиксируются в capability manifest, не как правила |
| EIM v0.2 (G-D-C-M-P-R-V) | `required_profile` перехода; сравнение покомпонентное, без компенсаций (§14 EIM v0.2) |
| Snapshot / LIMS-итерации | Каждому LC Statement соответствует iteration_ref; ветвление итераций (DAG) даёт параллельные ветви ЖЦ — слияние создаёт новый снапшот и, при необходимости, новый LC Statement |
| Decision | Единственный механизм изменения ЖЦ (LC-04) |
| Quality Gate (D-03) | Результаты gate в статусах §5; mapping severity→статус — в policy pack |

---

## 8. Формат данных

Schema: [`braim-spec/schemas/lifecycle-state.json`](./braim-spec/schemas/lifecycle-state.json) (`id: lc_…`).

Пример LC Statement:

```json
{
  "lc_id": "lc_a1b2c3d4e5f6a7b8c9d0e1f2",
  "scope": { "kind": "space", "ref": "ROOM-001@IT03", "name": "Жилая комната 001" },
  "iteration_ref": "IT03",
  "snapshot_id": "snp_01JABCDEF0123456789ABCDEF",
  "phase": "DESIGN",
  "stage": "DESIGN_DOC",
  "status": "VALIDATED",
  "transition_ref": "dec_9876543210fedcba98765432",
  "required_profile": "G2-D1-C111-M3333-P33-R333-V0",
  "gate_results": [
    {
      "rule_id": "SP-ROOM-AREA-MIN",
      "result": "PASS",
      "validation_run_id": "val_0f1e2d3c4b5a69788796a5b4",
      "checked_at": "2026-10-15T10:00:00+00:00",
      "snapshot_id": "snp_01JABCDEF0123456789ABCDEF",
      "policy_pack_digest": "pp:base@0.1.0"
    }
  ],
  "evidence": ["art_1122334455aabbccddeeff00"],
  "entered_at": "2026-10-15T10:05:00+00:00",
  "entered_by": "role:architect"
}
```

---

## 9. Открытые вопросы

| ID | Вопрос | Приоритет |
|---|---|---|
| LCQ-01 | Отображение стадий на российскую стадийность (ПП/РД, экспертиза) — нужен domain expert | 🟡 Средний |
| LCQ-02 | Частичный охват STALE: правило для частично изменившегося снапшота (покоординатно?) | 🟡 Средний |
| LCQ-03 | Минимальный набор role-значений участия (retained/replaced/new/removed) — достаточно ли для пилота | 🟢 Низкий |
| LCQ-04 | Экспорт LC в IFC как Pset: формат BRAIM extension (Phase 2+) | 🟢 Низкий |
| LCQ-05 | Связь LC-переходов с BCF-топиками (авто-создание topic при FAIL) | 🟡 Средний |

---

## 10. Changelog

### 0.1.0 — 2026-10-15

- Первоначальная публикация: scoped lifecycle (LC-01), четыре оси (LC-02), шесть статусов проверки (LC-03), переход как Decision+Snapshot (LC-04), независимость от cde_state (LC-05), правила федеративных случаев (LC-06), хранение вне IFC (LC-07).
- Схема `braim-spec/schemas/lifecycle-state.json`.
- Открытые вопросы LCQ-01..05.
