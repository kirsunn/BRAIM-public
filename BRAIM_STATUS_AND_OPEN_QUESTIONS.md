# BRAIM Status and Open Questions

**Статус:** Draft / рабочий документ  
**Дата обновления:** 2026-10-04  
**Версия:** 0.2.0

---

## 1. Текущий статус

### 1.1. Завершённые работы

| ID | Работа | Дата | Статус |
|---|---|---|---|
| W-01 | Создание репозитория `BRAIM-public` | 2026-09-30 | ✅ Done |
| W-02 | Публикация Handover Package v1.0 | 2026-09-30 | ✅ Done |
| W-03 | Публикация реестров (Attribute, Claim-Evidence, Model View, CDE State Machine) | 2026-09-30 | ✅ Done |
| W-04 | Публикация Project Identity и CDE Manifest | 2026-09-30 | ✅ Done |
| W-05 | Создание README.md с описанием проекта | 2026-10-04 | ✅ Done |
| W-06 | Формализация концепции BRAIM Concept v1.0 | 2026-10-04 | ✅ Done |

### 1.2. В работе (Phase 0)

| ID | Работа | Плановая дата | Статус |
|---|---|---|---|
| P0-01 | Architecture freeze (Master Context 1.0) | 2026-10-04 | ✅ Done |
| P0-02 | Публикация Concept v1.0 | 2026-10-04 | ✅ Done |
| P0-03 | JSON Schema: artifact, snapshot, decision, event | 2026-10-11 | ✅ Done (2026-10-15: опубликованы в [`braim-spec/schemas/`](./braim-spec/schemas/) — artifact, snapshot, decision, event, validation-result, policy-manifest) |
| P0-04 | BRAIM-LIMS 0.1 (naming & versioning policy) | 2026-10-18 | 📋 Planned |
| P0-05 | Standards/Claims/Grants registers (публичные) | 2026-10-18 | 📋 Planned |
| P0-06 | Golden Corpus: структура и benchmark protocol | 2026-10-25 | 📋 Planned |
| P0-07 | Toolchain SBOM и pinning (IfcOpenShell, IfcTester, Neo4j) | 2026-10-25 | 📋 Planned |
| P0-08 | CDE capability discovery (первый пилот) | 2026-11-01 | 📋 Planned |
| P0-09 | Lifecycle Model v0.1 (scoped LC, 6 статусов проверки, переходы как Decision+Snapshot) | 2026-10-15 | ✅ Done ([`BRAIM_Lifecycle_Model_v0_1.md`](./BRAIM_Lifecycle_Model_v0_1.md) + schema `lifecycle-state.json`) |
| P0-10 | Classification Model v0.1 (фасетность ISO 12006-2; пилот FUNCTION+SPACE+DISCIPLINE; КСИ = таблица экспорта) | 2026-10-15 | ✅ Done ([`BRAIM_Classification_Model_v0_1.md`](./BRAIM_Classification_Model_v0_1.md) + schema `classification-assignment.json`) |

### 1.3. Зафиксированные решения (пилот)

| ID | Решение | Статус |
|---|---|---|
| D-01 | CDE-master: CDE заказчика — контрактный master; BRAIM — immutable mirror + provenance | ✅ Подтверждено |
| D-02 | Git scope: только код, схемы, policy packs, mappings, ADR, snapshots, Golden Corpus | ✅ Подтверждено |
| D-03 | Strict Quality Gate: Critical→No-Go, Major→Hold, Minor→Go with findings | ✅ Подтверждено |
| D-04 | KPI: только R&D targets, проверяются benchmark protocol | ✅ Подтверждено |
| D-05 | Один глубокий пилот с реальным объектом и evidence chain | ✅ Подтверждено |
| D-06 | Neo4j Community для MVP/Phase 1–2 | ✅ Подтверждено |

---

## 2. Открытые вопросы

### 2.1. Архитектурные

| ID | Вопрос | Влияние | Приоритет | Ответственный |
|---|---|---|---|---|
| AQ-01 | Выбор message broker для BuildBus (NATS vs RabbitMQ) | Фаза 1, транспорт | 🔴 Высокий | Архитектор |
| AQ-02 | Transactional registry: PostgreSQL vs другой SQL | Фаза 1, хранение | 🔴 Высокий | Архитектор |
| AQ-03 | Object storage: S3-compatible vs MinIO self-hosted | Фаза 1, артефакты | 🟡 Средний | DevOps |
| AQ-04 | OIDC provider для аутентификации | Безопасность, Фаза 1 | 🟡 Средний | Security |

### 2.2. IFC/Graph mapping

| ID | Вопрос | Влияние | Приоритет | Ответственный |
|---|---|---|---|---|
| AQ-05 | Поддерживаемые IFC-классы для MVP mapping (D-01) | Фаза 1, граф | 🔴 Высокий | IFC-инженер |
| AQ-06 | Mapping profile versioning и hashing strategy | Провенанс, Фаза 1 | 🟡 Средний | Архитектор |
| AQ-07 | Обработка дубликатов GlobalId (ошибка vs warning) | Integrity check, Фаза 1 | 🟡 Средний | IFC-инженер |

### 2.3. Validation & Quality Gate

| ID | Вопрос | Влияние | Приоритет | Ответственный |
|---|---|---|---|---|
| AQ-08 | Минимальный набор IDS-профилей для MVP | Фаза 2, валидация | 🔴 Высокий | Domain expert |
| AQ-09 | Topology validation: какие корни разрешены (IfcProject, IfcSite, IfcBuilding)? | D-03, Фаза 2 | 🟡 Средний | Архитектор |
| AQ-10 | BCF 3.0 adapter: нативный API vs BCFzip fallback | CDE integration, Фаза 2 | 🟡 Средний | Integration |

### 2.4. CDE Integration

| ID | Вопрос | Влияние | Приоритет | Ответственный |
|---|---|---|---|---|
| AQ-11 | Первый пилот: какой CDE у заказчика? (Pilot-BIM, Renga, другое) | Пилот, Фаза 0 | 🔴 Высокий | PM |
| AQ-12 | Capability manifest: какие API доступны? (webhooks, polling, BCF) | Adapter design, Фаза 0 | 🔴 Высокий | Integration |
| AQ-13 | Immutable mirror: object storage у заказчика или BRAIM? | Storage architecture, Фаза 0 | 🟡 Средний | DevOps |

### 2.5. Standards & Compliance

| ID | Вопрос | Влияние | Приоритет | Ответственный |
|---|---|---|---|---|
| AQ-14 | СП 50.13330.2024: какие климатические зоны для пилота? | Thermal policy, Фаза 2 | 🟡 Средний | Domain expert |
| AQ-15 | Классификация: КСИ vs Uniclass vs другая | Classification policy, Фаза 1 | ✅ Решено 2026-10-15 ([Classification Model](./BRAIM_Classification_Model_v0_1.md) CL-01..07: фасетная методология ISO 12006-2; таблицы — конфигурация; КСИ = таблица экспорта) | — |

### 2.6. Security & Licensing

| ID | Вопрос | Влияние | Приоритет | Ответственный |
|---|---|---|---|---|
| AQ-16 | Threat model: какая классификация данных для пилота? | Security baseline, Фаза 0 | 🔴 Высокий | Security |
| AQ-17 | SBOM: лицензии IfcOpenShell (LGPL), Neo4j Community (GPL) | Compliance, Фаза 0 | 🟡 Средний | Legal/DevOps |
| AQ-18 | Container digests: pinning strategy для workers | Reproducibility, Фаза 1 | 🟡 Средний | DevOps |

---

## 3. Решения, требующие подтверждения

| ID | Решение | Варианты | Дедлайн | Статус |
|---|---|---|---|---|
| AD-01 | Message broker | NATS / RabbitMQ / другой | 2026-10-18 | ⏳ Pending |
| AD-02 | Transactional registry | PostgreSQL / другой SQL | 2026-10-18 | ⏳ Pending |
| AD-03 | Первый пилот CDE | Pilot-BIM / Renga / другой | 2026-10-11 | ⏳ Pending |
| AD-04 | OIDC provider | Keycloak / Auth0 / другой | 2026-10-25 | ⏳ Pending |

---

## 4. Риски

| Risk ID | Risk | Control | Статус |
|---|---|---|---|
| R-01 | IFC5 immaturity | Sandbox adapter only; no production dependency | 🟡 Мониторинг |
| R-02 | CDE API mismatch | Capability manifest + BCF/file fallback | 🟡 Мониторинг |
| R-03 | Experimental merge (ifcmerge) | Report-only diff; manual resolution; Golden Corpus | 🟡 Мониторинг |
| R-11 | KPI overclaim | R&D target label + benchmark protocol | 🟡 Мониторинг |
| R-16 | Threat model не определён | Требуется до начала пилота | 🔴 Блокирующий |
| R-17 | Licence conflict (LGPL/GPL) | SBOM + legal review перед пилотом | 🟡 Мониторинг |

---

## 5. Следующие действия

### Ближайшие 2 недели (до 2026-10-18)

1. ✅ **Завершено:** README.md и BRAIM_Concept_v1.0.md опубликованы.
2. ✅ **Завершено (2026-10-15):** JSON Schema — artifact, snapshot, decision, event, validation-result, policy-manifest (см. [`braim-spec/schemas/`](./braim-spec/schemas/)).
3. 📋 **План:** BRAIM-LIMS 0.1 (naming & versioning policy).
4. 📋 **План:** Standards/Claims/Grants registers (публичные версии).
5. 🔴 **Блокер:** Выбрать первый пилот CDE (AQ-11, AD-03) — с fallback-вариантом (S3-compatible + BCFzip/file-drop), чтобы Phase 1 не блокировалась на решении заказчика.
6. 🔴 **Блокер:** Определить threat model и классификацию данных (AQ-16).

> **Финансирование (2026-10-15):** заявка на соцконтракт подана; ООО — по факту участия/выигрыша грантов. Вехи M0/M1 из Concept v1.0 отменены — см. [`docs/funding/FUNDING_STATUS.md`](./docs/funding/FUNDING_STATUS.md).

### Ближайшие 4 недели (до 2026-11-01)

1. Завершить Phase 0: architecture freeze, schemas, BRAIM-LIMS 0.1.
2. Подготовить Golden Corpus структуру и benchmark protocol.
3. Завершить toolchain SBOM и pinning.
4. Провести CDE capability discovery для первого пилота.

---

## 6. Changelog

### 0.2.3 — 2026-10-15

- P0-10 выполнен: BRAIM_Classification_Model_v0_1.md (решения CL-01..07, фасетность ISO 12006-2, CoClass как методологический референс) + схема classification-assignment.json.
- AQ-15 закрыт: классификация — фасетная методология, таблицы конфигурируемы, КСИ — целевая таблица экспорта через versioned mapping profile.
- Пилотные фасеты: FUNCTION, SPACE, DISCIPLINE; FORM/LOCATION/MATERIAL/PRODUCT — резерв до появления проверок.

### 0.2.2 — 2026-10-15

- P0-09 выполнен: опубликован BRAIM_Lifecycle_Model_v0_1.md (решения LC-01..LC-07) и схема lifecycle-state.json.
- Канонический набор статусов проверки: PASS/FAIL/UNKNOWN/INCOMPLETE/NOT_APPLICABLE/STALE; EIM v0.2 INDETERMINATE → UNKNOWN при следующей ревизии.
- Открытые вопросы LCQ-01..05 (отображение стадий на нормативную стадийность, частичный STALE, роли участия, IFC-экспорт LC, BCF-связка).

### 0.2.1 — 2026-10-15

- P0-03 переведён в Done: JSON-схемы (artifact, snapshot, decision, event, validation-result, policy-manifest) опубликованы в braim-spec/schemas/.
- $id схем переименован с baim.dev на braim.dev (решение об имени проекта: BRAIM).
- Добавлены docs/funding/ (FUNDING_STATUS, дорожная карта запуска) и docs/history/ (критика, ревью, архивные контексты).
- Финансовая лестница подтверждена: соцконтракт (заявка подана) → подготовка к грантам → ООО по факту участия/выигрыша; вехи M0/M1 Concept v1.0 отменены.

### 0.2.0 — 2026-10-04

- Добавлены завершённые работы W-05, W-06 (README, Concept v1.0).
- Обновлён статус Phase 0: P0-01, P0-02 завершены.
- Добавлены открытые вопросы AQ-01..AQ-18.
- Добавлены решения, требующие подтверждения (AD-01..AD-04).
- Обновлены риски с ссылками на Master Context.
- Обновлены следующие действия с дедлайнами.

### 0.1.0 — 2026-09-30

- Первоначальная публикация статуса и открытых вопросов.

---

*Последнее обновление: 2026-10-15*
