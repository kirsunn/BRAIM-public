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
| P0-11 | ADR-009: IFC5 sandbox + composition-native alignment (IFC5/IFC X — слои данных; production = IFC 4.x) | 2026-10-15 | ✅ Done ([`docs/adr/ADR-009`](./docs/adr/ADR-009_ifc5_sandbox_and_composition_alignment.md) — первый из 14 обязательных ADR) |
| P0-12 | ADR-015: bSDD как базовый словарь (ISO 12006-3/23386; локальный реестр + bSDD-совместимость; с Phase 1; pinning словарей) | 2026-10-15 | ✅ Done ([`docs/adr/ADR-015`](./docs/adr/ADR-015_bsdd_as_base_dictionary.md); Attribute Registry → v0.1.1 `bsdd_property_ref`; Classification Model → v0.1.1) |
| P0-13 | ADR-016: BRAIM Composition Format — IFCX-совместимая слоистая сериализация (path-узлы, imports, precedence внутри владельца; Project Package слоями — deliverable Phase 1) | 2026-10-15 | ✅ Done ([`docs/adr/ADR-016`](./docs/adr/ADR-016_ifcx_aligned_composition_format.md); референс IFC5-development → `_library/ifc5-reference`) |
| P0-14 | **Concept v1.1**: §1.3 два режима, §1.4 вертикали, §1.5 guardrails G-1..G-7, D-07..D-11, §4.2 +стандарты, §8 EIM → G-D-C-M-P-R-V, §9.2 вехи под финансовую лестницу | 2026-10-15 | ✅ Done ([`BRAIM_Concept_v1.1.md`](./BRAIM_Concept_v1.1.md)) |
| P0-15 | Схема validation-result.json: добавить `coverage_statement` (G-3) и `scope_element_ids`/инкрементальная инвалидация (G-4) | Phase 1 | 📋 Planned (реализация вместе с обёрткой IfcTester → validation-result) |
| P0-16 | Threat model: раздел DataBoundaryPolicy (G-6) — CLIENT_CONFIDENTIAL по умолчанию, публичные ИИ-сервисы запрещены | Phase 1 | 📋 Planned (расширение docs/security/THREAT_MODEL_v0_1.md) |
| P0-17 | **BRAIM Pset v0.1** — собственный сет свойств поверх authoring-моделей (аналог RusSet_AGR): классификация, ТЭП-атрибуты, LC-refs; IDs/GUIDs автора произвольны — BRAIM Pset накладывается сверху | Phase 1–2 | 📋 Planned (решение автора 2026-10-16) |
| P0-18 | Standards Register: **процесс верификации нормативов** — первоисточник с сайта Минстроя (свободный доступ); для каждого: версия, дата, URL/URI, hash, статус; сканы → OCR | Phase 1 | 📋 Planned (решение автора 2026-10-16) |
| P0-19 | **Резервирование**: rclone → Яндекс.Диск (основное, артефакты/_library/_storage) + Google Drive (вторичная копия критичного) | Phase 1 | 📋 Planned (F-09) |

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
| AQ-11 | Первый пилот: какой CDE у заказчика? (Pilot-BIM, Renga, другое) | Пилот, Фаза 0 | ✅ Решено 2026-10-15: заказчик = мы; пилотный объект — собственная АГР-модель (стадия концепции/АГР); AD-03 | — |
| AQ-12 | Capability manifest: какие API доступны? (webhooks, polling, BCF) | Adapter design, Фаза 0 | 🟡 Снижен: для собственного хранилища capability manifest тривиален (файл-drop + BCFzip); остаётся открытым для будущего внешнего CDE | Integration |
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
| AD-01 | Message broker | NATS / RabbitMQ / другой | 2026-10-18 | ✅ Решено ([ADR-013](./docs/adr/ADR-013_full_stack.md): NATS, Phase 3) |
| AD-02 | Transactional registry | PostgreSQL / другой SQL | 2026-10-18 | ✅ Решено ([ADR-013](./docs/adr/ADR-013_full_stack.md): PostgreSQL 16) |
| AD-03 | Первый пилот CDE | Pilot-BIM / Renga / другой | 2026-10-11 | ✅ **Решено 2026-10-15: заказчиком будем мы.** Фолбэк (собственное файловое хранилище + BCFzip/file-drop) — primary для Phase 1; пилотный объект — собственная АГР-модель; внешний CDE заказчика подключается адаптером в будущем (см. AQ-11/12) |
| AD-04 | OIDC provider | Keycloak / Auth0 / другой | 2026-10-25 | ⏳ Pending (не блокирует Phase 1: solo-режим) |

---

## 4. Риски

| Risk ID | Risk | Control | Статус |
|---|---|---|---|
| R-01 | IFC5 immaturity | Sandbox adapter only; no production dependency | 🟡 Мониторинг |
| R-02 | CDE API mismatch | Capability manifest + BCF/file fallback | 🟡 Мониторинг |
| R-03 | Experimental merge (ifcmerge) | Report-only diff; manual resolution; Golden Corpus | 🟡 Мониторинг |
| R-11 | KPI overclaim | R&D target label + benchmark protocol | 🟡 Мониторинг |
| R-16 | Threat model не определён | Draft подготовлен 2026-10-15 ([`docs/security/THREAT_MODEL_v0_1.md`](./docs/security/THREAT_MODEL_v0_1.md)) — требует подтверждения автора до первого артефакта пилота | 🟡 Draft (было 🔴 Блокирующий) |
| R-17 | Licence conflict (LGPL/GPL) | SBOM + legal review перед пилотом | 🟡 Мониторинг |

---

## 5. Следующие действия (обновлено 2026-10-15)

### Завершено к 2026-10-15 (сводка)

Спек-ядро закрыто: Concept v1.1 (два режима, вертикали, guardrails G-1..G-7), Lifecycle/Layer/Classification-модели, ADR-009/015/016, 7 JSON-схем, Attribute Registry v0.1.1. IDS-конвейер работает на официальных эталонах Москвы (~14,6 тыс. проверок; найден FAIL-кейс 3×IfcRailing). Threat model draft. Финансовая лестница зафиксирована (соцконтракт подан). Корпус наполовину собран (эталоны ЛК + Онежская 14Б).

### Phase 0 — остаток (до конца 2026)

1. 📋 Standards Register v0.1 (P0-05): + стек Москвы (ПП 614, 783/пр, ГОСТ Р 10.0.02, ГОСТ Р 10.00.00.01-2025, ПНСТ 909, СП 59/333/331), СанПиН 1.2.3685-20, RFC 7946 + профиль АГР, ISO 12006-2/3, ISO 23386.
2. 📋 Golden Corpus (P0-06): оформить структуру (эталоны + FAIL-кейсы + АГР-экспорты автора), benchmark protocol (baseline: 14,6k checks / 3,5 мин).
3. 📋 BRAIM-LIMS 0.1 (P0-04): профиль совместимости с маской наименования ЦИМ (`K01_XXX_П_X`).
4. 📋 SBOM + pinning (P0-07): ifcopenshell, ifctester, uv/tapir-mcp (интерактивный слой — вне production-зависимостей).
5. 🔄 КСИ: завершить дамп → конвертер в bSDD import model → словарь ФНО.
6. ✅ P0-08 (CDE discovery) закрыт: заказчик = мы, фолбэк-хранилище.
7. ⏳ От автора: подтвердить threat model (бэкап, фолбэк-хранилище, шифрование диска); утвердить CHECKS_LIST; экспорты АГР-модели для корпуса.

### Phase 1 — вертикальный срез (дек 2026 – фев 2027, веха M1)

1. Обёртка IfcTester → `validation-result.json` (+ coverage_statement P0-15, инкрементальность G-4).
2. Policy pack v0.1: официальные IDS Москвы (digests + meta-validation G-2) + braim.py + AGR-GEOJSON.*.
3. Фолбэк-хранилище (file-drop) + artifact registry.
4. Cross-artifact: GeoJSON ↔ ТЭП-XML ↔ IFC.
5. BCF findings (первый кейс — 3×IfcRailing).
6. Sealed snapshot + provenance query.
7. 🎯 **Найти заказ или пример объекта для подготовки модели к АГР** (F-08) — демо: «проверка АГР-модели по требованиям».

> **Финансирование:** заявка на соцконтракт подана; ООО — по факту участия/выигрыша грантов. Вехи — [`BRAIM_Concept_v1.1.md`](./BRAIM_Concept_v1.1.md) §9.2 и [`docs/funding/FUNDING_STATUS.md`](./docs/funding/FUNDING_STATUS.md).

---

## 6. Changelog

### 0.3.1 — 2026-10-16

- F-05..F-10 (FUNDING_STATUS): соцконтракт выведен из вех (внеплановая возможность, средства на LLM-ПК); план Б — облачные мощности для нормативного конвейера (норм. тексты публичны, G-6 не нарушается); грант-подготовка (тема НИОКР базовая принята, название адаптируемо); демо = «проверка АГР»; ёмкость автора 12–16 ч/нед.
- Concept v1.1 §9.2: вехи M0–M5 переопределены (M0 = прототип + найти заказ/пример АГР); v1.1 M0-соцконтракт удалён.
- Новые задачи: P0-17 BRAIM Pset (свой сет свойств поверх authoring-моделей), P0-18 процесс верификации нормативов (Минстрой: версия/дата/URL/hash/OCR), P0-19 резервирование rclone (Яндекс — основное, Google — вторичное).
- Git visibility policy: git = только наш оригинальный контент; сторонние материалы (эталоны, PDF, КСИ) — вне git (_library + Яндекс); пилотные модели заказчиков — никогда не в git.

### 0.3.0 — 2026-10-15

- P0-14 выполнен: **BRAIM_Concept_v1.1.md** (файл переименован, ссылки обновлены): §1.3 два режима работы, §1.4 пять вертикалей применения, §1.5 архитектурные ограждения G-1..G-7 (многоредакционность нормативов, мета-валидация политик, coverage statement, инкрементальность, ИИ-акторы в provenance, граница данных, registry-ready), решения D-07..D-11, §4.2 дополнен стандартами (ISO 12006-2/3, ISO 23386, RFC 7946 + профиль АГР, требования Москвы ЦИМ АГР), §8 EIM переведён на G-D-C-M-P-R-V (G-I-C-A удалена), §9.2 вехи переписаны под финансовую лестницу (v1.0 M0/M1 отменены).
- P0-15/P0-16 запланированы: расширение схемы validation-result (coverage_statement, scope_element_ids) и Threat Model (DataBoundaryPolicy) — при реализации Phase 1.

### 0.2.9 — 2026-10-15

- **Зафиксированы два режима работы продукта (решение автора):**
  - **Режим А «Аудит»** (Phase 1–2): модель в BIM-программе (Archicad — primary; файл = БД, хранение таблицами-first, геометрия как предпросмотр/проекция) → BRAIM разбирает через аддоны → canonical → проверки (IDS + расчётное ядро) → итерации с архитектором → согласование → документация/визуализации/расчётные схемы. Коннекторы Renga/Revit — позднее.
  - **Режим Б «Генерация по ТЗ»** (L16-GN, 2027+): виртуальное помещение/квартира/этаж/дом по ТЗ с учётом IDS/ГК/ФЗ/СП/ГОСТ/СанПиН → поиск вариантов → итоговая модель в BIM-программе. Основная модель живёт под капотом BRAIM, двусторонняя связь (Tapir: braim_tapir + tapir-archicad-mcp).
- **Расчётное ядро (проверочные расчёты, не проектирование; решение автора — без MEP до v0.2+):** СП 50.13330 (теплотехника ограждений), СП 1.13130 + ФЗ-123 (эвакуация), СП 59.13330 (МГН), СанПиН 1.2.3685-20 (инсоляция/естественное освещение), СП 63/16/22 (несущие — проверка заданного сечения). Сложные расчёты — внешние комплексы (BASE, ЛИРА, SCAD) через адаптеры, результаты принимаются обратно с provenance. Каждый расчёт = формула + нормативная ссылка + юнит-тест → policy pack.
- Новые нормативы-кандидаты в Standards Register: СанПиН 1.2.3685-20; (ПУЭ, СП 30/60.13330 — вместе с MEP после v0.2).
- **Concept v1.1 (задача):** вехи M0/M1 под подтверждённое финансирование + §8 EIM на G-D-C-M-P-R-V + §1.2 два режима работы + расчётное ядро.

### 0.2.8 — 2026-10-15

- **Первый прогон по официальным материалам Москвы** (docs/phase1/MOSCOW_IDS_RESULTS_v0_1.md): IDS v9 × эталонные IFC → IfcTester: С00 339/339, С01 (50 МБ) 9524/9524, С02 4220/4220; МССК-классификация нашла 3 IfcRailing (МГН-ограждения) без RUS_MSSK_Element_Code — эталон не полностью проходит собственный IDS (кейс Golden Corpus). braim.py: ПС/БиО/С00 VALID.
- **GeoJSON-приложение АГР включено в стек** (docs/dictionaries/AGR_GEOJSON_v0_1.md): RFC 7946 + городское расширение (ObjectFeature, локальная СК); поля из эталона; проверки AGR-GEOJSON.* (высотный инвариант, согласование площадей — в эталоне расхождение 25 м², классификатор ФНО); профиль agr-geojson Composition Format.
- ТЭП-атрибуты v0.1 (docs/phase1/TEP_ATTRIBUTES_v0_1.md) — из сервиса ТЭП-XML (УИН, ГПЗУ/ППТ/ГЗК/КРТ/ППМ → externalIdentity).
- Корпус: эталоны ЛК (ПС/БиО/АР×3, вкл. 50 МБ) + эталон FBX/GeoJSON (Онежская 14Б, НПМ+ВПМ).

### 0.2.7 — 2026-10-15

- **Брифинг по распылению; работа по блокерам.**
- AD-03 решён: **заказчиком будем мы** — фолбэк-хранилище (файл-drop + BCFzip) как primary для Phase 1; пилотный объект — собственная АГР-модель. AQ-11 закрыт, AQ-12 понижен.
- R-16: draft threat model ([`docs/security/THREAT_MODEL_v0_1.md`](./docs/security/THREAT_MODEL_v0_1.md)) — открытые решения: бэкап, фолбэк-хранилище, шифрование диска.
- Кандидаты проверок Phase 1 ([`docs/phase1/CHECKS_LIST_v0_1.md`](./docs/phase1/CHECKS_LIST_v0_1.md)): 6 готовы (braim.py + GEO-GRID), 4 — гибрид IDS + свои критерии (проёмы, проходы, ФЗ-123, МГН) со статусом `needs_source`; СП 59.13330 (МГН) — добавить в Standards Register.
- AD-01/02/04 понижены: не блокируют Phase 1.

### 0.2.6 — 2026-10-15

- P0-13 выполнен: ADR-016 — BRAIM Composition Format, IFCX-совместимая слоистая сериализация собственных артефактов (path-узлы, imports по URI с pinned digests, локальные схемы, слоистый стек Project Package). Отличие от IFCX: precedence внутри владельца; cross-owner пересечение — конфликт с явным разрешением. Спецификация формата v0.1 — deliverable Phase 1. ADR-009 дополнен связью (v0.2). Референс IFC5-development склонирован в _library/ifc5-reference (вне git).

### 0.2.5 — 2026-10-15

- P0-12 выполнен: ADR-015 — bSDD (ISO 12006-3/23386) как базовый словарь. Решения DICT-01..06: локальный реестр с bSDD-совместимой моделью для проектных определений; подключение с Phase 1; pinning редакций словарей (runtime без внешнего сервиса); mapping классификаций через связи bSDD; языки пилота ru+en.
- Attribute Registry → v0.1.1: поле `bsdd_property_ref`, правила 11–12 (DICT.DEFINITION_CONFLICT).
- Classification Model → v0.1.1: table_ref.system += bSDD; mapping через связи bSDD.
- Схема classification-assignment.json: описание system дополнено bSDD.

### 0.2.4 — 2026-10-15

- P0-11 выполнен: ADR-009 (docs/adr/) — production остаётся на IFC 4.x; IFC5/IFC X — sandbox; зафиксированы 6 composition-native принципов (самодостаточные артефакты, identity вне монолита, provenance слоёв, конфликты явно, маппинг слоёв→проекций, инкрементальное обогащение) и триггеры пересмотра.

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
