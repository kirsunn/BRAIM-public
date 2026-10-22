# BRAIM Classification Model

## Статус

- Версия: `0.1.0` (draft)
- Дата: 2026-10-15
- Назначение: фасетная модель классификации сущностей BRAIM
- Основания: открытый вопрос AQ-15 (STATUS), Layer Model v0.1.2 (L2-F, L3-R), новейшая итерация концепции (ClassificationAssignment в Canonical Model, §3), adversarial-ревью LIMS §4.5 (сравнение ISO 12006-2 / КСИ / CoClass / CCS)

> Методология — фасетная классификация по **ISO 12006-2** (framework для систем классификации застроенной среды); **CoClass** (Molio, Дания) — методологический референс-реализация этого принципа, как Uniclass и OmniClass. Точные коды таблиц CoClass сверяются с официальным изданием при применении (принцип первоисточников, R-05).

---

## 1. Решения (CL-01..CL-07)

| ID | Решение | Смысл |
|---|---|---|
| CL-01 | **Фасетность как принцип, не привязка к датским таблицам** | Классификация = независимые фасеты по ISO 12006-2; таблицы — конфигурация проекта. AQ-15 закрыт: не «КСИ vs Uniclass», а методология + настраиваемые таблицы |
| CL-02 | **ClassificationAssignment — first-class сущность** | `{entity_ref, facet, table_ref+edition, code, assigned_by, source}`; на сущность — одно **primary**-назначение на фасет + необязательные alternates; конфликты не разрешаются молча (инвариант Zero Bus №3) |
| CL-03 | **Пилотный набор фасетов: FUNCTION + SPACE + DISCIPLINE** | Минимум для архитектурного пилота; FORM/LOCATION/MATERIAL/PRODUCT — в реестре, активируются вместе с правилами |
| CL-04 | **IFC-транспорт нативный** | Каждая привязка → `IfcClassificationReference`; IFC допускает несколько references на элемент — фасетность транспортируется без расширений схемы |
| CL-05 | **Таблицы версионируются как артефакты policy pack** | edition + digest; assignment хранит редакцию, на которую ссылается код |
| CL-06 | **КСИ = таблица экспорта** | КСИ (российский классификатор строительной информации) подключается через versioned mapping profile для экспертизы/документации; КСИ-код не смешивается с функциональным фасетом в одном поле |
| CL-07 | **Семейства правил `CLS.*`** | Полнота фасетов, один primary, валидность кода в редакции, round-trip без потерь |

---

## 2. Понятия

```text
Facet                  — независимая ось классификации (FUNCTION, SPACE, …);
                         каждый фасет отвечает на один вопрос
Classification Table   — версионируемый справочник кодов одного фасета
                         (КСИ, CoClass-подобная таблица, проектная таблица);
                         edition + digest
Classification         — привязка сущности к коду одного фасета одной
  Assignment             таблицы (schema: braim-spec/schemas/
                         classification-assignment.json, id: cls_)
Mapping Profile        — версионируемое соответствие между фасетами BRAIM
                         и кодами конкретной таблицы (напр., FUNCTION → КСИ)
```

## 3. Фасеты BRAIM

| Фасет | Вопрос | Пилот v0.1 | Пример применения | Слой |
|---|---|---|---|---|
| `FUNCTION` | Какова функция объекта? | ✅ Активен | жилая комната, коридор, техническое помещение | L2-F |
| `SPACE` | Какое пространство/зона? | ✅ Активен | Room 42, Apartment, зона кухни | L2-F |
| `DISCIPLINE` | Какой раздел/дисциплина? | ✅ Активен | АР, КР, ОВ, ВК, ЭО | L9-B, L13-D |
| `FORM` | Какова форма? | ⏳ Резерв | линейный, точечный, кольцевой | L4-G |
| `LOCATION` | Где расположен? | ⏳ Резерв | фасад северный, подземный уровень | L4-G |
| `MATERIAL` | Из чего? | ⏳ Резерв | кирпич, бетон, древесина | L1-C |
| `PRODUCT` | Какое изделие? | ⏳ Резерв | дверь EI60, радиатор | L11-INT |

Правило: фасет активируется только вместе с правилами, которые его проверяют (урок Layer Model: никаких «слоёв/фасетов на бумаге»).

## 4. ClassificationAssignment

Пример:

```json
{
  "assignment_id": "cls_a1b2c3d4e5f6a7b8c9d0",
  "entity_ref": "ent_room_000042",
  "facet": "SPACE",
  "role": "primary",
  "table_ref": {
    "system": "custom",
    "edition": "pilot-tatarstan-2026.10",
    "table": "spaces",
    "digest": "sha256:…"
  },
  "code": "SP-RES-LIV",
  "assigned_at": "2026-10-15T10:00:00+00:00",
  "assigned_by": "role:architect",
  "source": "authoring"
}
```

Правила:

1. На пару (entity, facet) — ровно одно `role: primary`; альтернативы — `role: alternate` (напр., код в другой таблице).
2. `source`: `authoring` (из Archicad/Revit/Renga через адаптер), `rule` (назначено правилом), `manual`, `imported` (из IFC).
3. Назначение из авторинг-системы не становится фактом автоматически — проходит через Zero Bus (Canonical → Enriched), статус решения фиксируется в provenance.
4. Смена редакции таблицы не переписывает старые assignments — они ссылаются на свою edition (историчность).

## 5. Таблицы классификации

| Таблица | Роль | Статус |
|---|---|---|
| **Проектные таблицы BRAIM** (pilot-tatarstan) | Primary для пилота: FUNCTION, SPACE, DISCIPLINE | Создаются в Phase 0б/1, версионируются как policy pack артефакты |
| **bSDD** (ISO 12006-3, ISO 23386) | Базовый словарь: источник справочных таблиц и определений свойств; связи `IsEqualTo`/`HasSimilarity` — предпочтительная механика mapping (ADR-015, DICT-05) | Подключается с Phase 1; редакции пиннятся (DICT-04), runtime — без обращений к сервису |
| **КСИ** | Целевая таблица экспорта (экспертиза, документация L13-D) через mapping profile (CL-06) | Подключается при первом требовании экспертизы; редакция фиксируется |
| **CoClass / Uniclass / OmniClass** | Методологические референсы (ISO 12006-2); совместимы, не обязательны | Reference |

Mapping profile — версионируемый артефакт: `{facet, table_from, table_to, rules[]}` + digest; экспорт в КСИ — controlled export через Zero Bus, расхождения фиксируются в loss report.

## 6. IFC-транспорт

```text
BRAIM ClassificationAssignment (по фасету)
  → IfcClassification (Source = система/таблица, Edition = редакция)
  → IfcClassificationReference (Identification = code, Location = code_uri)
  → IfcRelAssociatesClassification → сущность
```

- Несколько references на элемент = фасеты; ничего расширять не нужно (IFC4/IFC4x3, ISO 16739:2024).
- Импорт: восстановление assignments по (system, edition, identification); нераспознанные коды → `UNMATCHED`, не молча.
- Round-trip: потери классификации фиксируются в loss report (инвариант Zero Bus №5).

## 7. Правила (семейства `CLS.*`)

| Семейство | Проверяет | Severity |
|---|---|---|
| `CLS.FACET_COMPLETENESS` | Для типов сущностей, где фасет обязателен (напр., Space → SPACE), назначение есть | minor/major — в policy pack |
| `CLS.SINGLE_PRIMARY` | Не более одного primary на (entity, facet) | major |
| `CLS.CODE_EDITION_VALID` | Код существует в заявленной редакции таблицы | major |
| `CLS.IFC_ROUNDTRIP` | Классификация переживает экспорт/импорт без потерь | minor |
| `CLS.MAPPING_COVERAGE` | Mapping profile покрывает все primary-assignments целевой таблицы | major |

## 8. Связь с механизмами

| Механизм | Связь |
|---|---|
| Layer Model v0.1.2 | Фасеты живут в слоях-проекциях: FUNCTION/SPACE → L2-F, DISCIPLINE → L9-B/L13-D; слой показывается через выборку, assignment — через реестр |
| Policy packs (D-03) | Таблицы + mapping profiles + правила `CLS.*` — версионируемые артефакты с digest |
| Zero Bus | Назначения проходят Raw → Canonical → Enriched; конфликты и потери — явно |
| IFC | IfcClassificationReference per facet (CL-04); IFC — транспорт, не source of truth |
| КСИ | Только как целевая таблица экспорта (CL-06); AQ-15 закрыт |

## 9. Открытые вопросы

| ID | Вопрос | Приоритет |
|---|---|---|
| CLQ-01 | Состав пилотных проектных таблиц FUNCTION/SPACE/DISCIPLINE (стартовый словарь Татарстана) | 🔴 Высокий |
| CLQ-02 | Mapping profile КСИ: объём (какие фасеты → какие разделы КСИ) — нужен domain expert | 🟡 Средний |
| CLQ-03 | Обработка UNMATCHED при импорте IFC: finding vs тихий реестр | 🟡 Средний |
| CLQ-04 | Фасеты FORM/LOCATION/MATERIAL/PRODUCT: активация вместе с правилами L4-G/L11-INT | 🟢 Низкий |
| CLQ-05 | code_uri конвенция (резолваемые URI таблиц) | 🟢 Низкий |

## 10. Changelog

### 0.1.1 — 2026-10-15

- `table_ref.system` += `bSDD`; в реестр таблиц добавлен bSDD (ISO 12006-3/23386) как базовый словарь; mapping классификаций — предпочтительно через связи bSDD (`IsEqualTo`/`HasSimilarity`); редакции словарей пиннятся как артефакты (ADR-015, DICT-04/05).

### 0.1.0 — 2026-10-15

- Первоначальная публикация: фасетность по ISO 12006-2 (CL-01), ClassificationAssignment как first-class сущность (CL-02), пилотные фасеты FUNCTION+SPACE+DISCIPLINE (CL-03), нативный IFC-транспорт (CL-04), версионирование таблиц (CL-05), КСИ как таблица экспорта (CL-06), семейства правил CLS.* (CL-07).
- Схема `braim-spec/schemas/classification-assignment.json`.
- AQ-15 (STATUS) закрыт; открытые вопросы CLQ-01..05.
