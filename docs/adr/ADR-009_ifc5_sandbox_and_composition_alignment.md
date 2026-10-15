# ADR-009: IFC5 sandbox, production exclusion и composition-native alignment

- **Статус:** Accepted (draft → first review при Phase 1 close)
- **Дата:** 2026-10-15
- **Относится к:** Concept v1.0 §4.1 (IFC5-First Policy), §11 ADR-009; риски R-01, R-03
- **Источники:** [buildingSMART — An update on IFC developments](https://www.buildingsmart.org/an-update-on-ifc-developments/), [buildingSMART.de — IFC roadmap (Porto): 4.4, затем IFC 5 → IFC X](https://www.buildingsmart.de/buildingsmart/aktuelles/ifc-roadmap-nach-porto-version-44-kommt-ifc-5-wird-zu-ifc-x), [ifc5.technical.buildingsmart.org](https://ifc5.technical.buildingsmart.org/), [IFC5-development (deepwiki)](https://deepwiki.com/buildingSMART/IFC5-development)

---

## 1. Контекст

IFC 4.3 — завершённый стандарт (ISO 16739-1): монолитная EXPRESS-схема с четырьмя слоями (Resource, Core, Interoperability/Shared, Domain) и фиксированными доменными схемами (`IfcArchitectureDomain`, `IfcHvacDomain`, `IfcRoadDomain`, …). Обмен — целым файлом STEP/EXPRESS.

IFC 5 (направление переименовывается в **IFC X**) — следующее поколение: альфа/разработка; JSON-ориентированный формат **IFCX** (TypeSpec → JSON Schema); **вместо фиксированных доменных схем — композиция данных из независимых файлов/слоёв**: базовая модель несёт геометрию и идентификацию, дисциплинарные данные (свойства, классификация, FireRating, результаты расчётов, эксплуатация) подключаются отдельными расширениями-слоями, в т.ч. инкрементально, без пересборки исходной модели.

**Ключевой вектор (зафиксирован автором 2026-10-15):** в IFC 5 «домен» перестаёт быть веткой монолитной схемы и становится подключаемым слоем данных.

## 2. Решения

### D1. Production остаётся на IFC 4.x — без изменений

Production scope BRAIM: **IFC2x3, IFC4, IFC4x3** (Concept §4.1). IFC 4.4 лишь расширяет 4.3 — принимается без отдельного решения при появлении стабильного toolchain. IFC 5/IFC X — **R&D sandbox, ноль production-зависимостей** (R-01), до: стабилизации стандарта, зрелого toolchain (reader/writer/validator) и подтверждённой IDS-поддержки.

### D2. «IFC5-ready» определяется архитектурно, а не форматом

BRAIM считается IFC5-ready тогда, когда его собственные механизмы не предполагают монолитность исходной модели. Зафиксированные **composition-native принципы**:

| # | Принцип | Уже обеспечено |
|---|---|---|
| P1 | Каждый артефакт BRAIM самодостаточен: ссылается на (snapshot_id, identity anchors), а не на «файл целиком» | схемы artifact/snapshot/validation-result/lifecycle-state/classification-assignment |
| P2 | Идентичность не зависит от монолита: `instance_id ↔ externalIdentity (GUID)`; объект может приходить из базового слоя и из расширений | Canonical Model: IdentityLink, MATCHED/SPLIT_FROM/MERGED_FROM/POSSIBLE_MATCH/UNMATCHED |
| P3 | Каждый слой данных несёт provenance: кто, когда, из какого источника, какая редакция | Zero Bus инвариант №2; PropertyAssertion + evidence |
| P4 | Конфликты между слоями не разрешаются молча | Zero Bus инвариант №3; LC-views, primary/alternate assignments |
| P5 | Адаптеры IFC5 маппят слои → проекции BRAIM, а не сплющивают в монолит | Layer Model: слои = выборки; адаптер — integration plane |
| P6 | Инкрементальное обогащение (напр., FireRating отдельным слоем) = BRAIM enrich-шаг с own artifact, а не перезапись | Zero Bus: Raw → Parsed → Canonical → **Enriched** → Controlled Export |

### D3. Соответствие механизмов BRAIM вектору IFC5

| IFC 5 / IFC X | Механизм BRAIM | Замечание |
|---|---|---|
| Слой данных (extension) | Проекция Layer Model (L0–L17) + enrich-артефакт | Не копия данных: выборка + владение атрибутами |
| Инкрементальное обновление (FireRating слоем) | PropertyAssertion/PropertySet-артефакт со snapshot_id + source | Изменение не трогает базу — additive |
| JSON Schema / TypeSpec | braim-spec JSON Schemas (draft 2020-12) | Формат совпадает по духу; IFCX-схемы не копируем |
| Домены → расширения | Layer Model + фасеты Classification Model | Дисциплинарность — проекция/фасет, не ветка схемы |
| Идентичность across files | IdentityLink, разрешение идентичности | Центральный механизм для композиции |
| IFCX-валидация | IDS-воркер + `CLS.*`/policy pack — по слоям, не по монолиту | Ожидание: IDS для IFCX появится позже — не форсировать |

### D4. Триггеры пересмотра

ADR пересматривается при любом из событий: (1) IFC X переходит из alpha в beta/public draft; (2) появляется production-ready reader/writer IFCX в мейнстрим-тулчейне (ifcopenshell и др.); (3) buildingSMART объявляет IDS-поддержку IFCX; (4) пилотный заказчик запрашивает IFCX-поток. До триггеров — только sandbox-наблюдение.

## 3. Последствия

- **Положительные:** архитектура BRAIM не потребует переработки при приходе IFC5 — композиция уже родная; IFC5-адаптер станет маппингом слоёв, а не конвертацией; identity-механика (CL/CANON) окупится раньше срока.
- **Цена/риски:** sandbox-наблюдение требует времени без немедленной отдачи (осознанно, R-01); не начать писать IFCX-код раньше триггеров — соблазн «поиграть» отложить до D4.
- **Не меняется:** production-стек Phase 1–2 (IFC 4.x, IDS, BCF 3.0), Layer Model, Classification Model.

## 4. Changelog

- 0.1 — 2026-10-15: создан. Первый написанный ADR из 14 обязательных (Concept §11).
