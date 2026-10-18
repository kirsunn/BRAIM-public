# BRAVO v0.4 → BRAIM (v0.4) — mapping архитектурных компонентов

> **Назначение:** фиксирует соответствие BRAVO v0.4 (8 слоёв) → наша фактическая реализация на соло-разработчике (5-6 папок, 1 репо). Не переименовывает BRAVO, не отменяет его.
> **Статус:** draft v0.1 — для BRAIM v0.4.

## Принцип

BRAVO v0.4 описывает **идеальную архитектуру** для полноценной команды. BRAIM в v0.4 = **наша реализация** (subset + декомпозиция под 1 разработчика + 12 ч/нед).

## Таблица соответствия

| BRAVO v0.4 (облако) | Наша 5-6-папок (1 dev) | Тип соответствия |
|---|---|---|
| **BRAVIUM-Planet** (BRAIM core) | `core/` + `core_kernel/` | subset (нормы, критерии, recipes, ADRs) |
| **BRAIM** (governance engine) | `core/norm_graph/` + `core/rules_engine/` | subset (норм. граф + движок правил) |
| **Registry & Log (BAR + BAG)** | `audit/` + `output/reports/` | subset (snapshot registry + immutable activity log) |
| **API Gateway** | `protocols/rest_api.py` (если нужен) | NOT-DOING (solo + локально, без API) |
| **BRAVIM (Client)** | `enricher/` (Итерационный цикл) | subset (enricher v0.3 + iteration_loop v0.4) |
| **BAV Core** | `input/` (PDF + DOCX + чанки) | subset (только extract layer) |
| **Validator** | `enricher/validator.py` (= enricher v0.3) | subset |
| **Treatment Manager** | `enricher/iteration_loop.py` (= Iteration Loop v0.4) | subset |
| **Data Storage × 3** (Metadata/Geometry/History) | `audit/` (snapshot registry + meta) | NOT-DOING (Geometry = в IFC; History = в audit_log) |
| **Security Module** | (отсутствует) | **NOT-DOING §18** — solo не делает "настоящий security" |
| **UI/UX Layer** | (отсутствует) | **NOT-DOING §11** — text/file based, не GUI |
| **Integration Hub** | `protocols/` (BCF, IDS экспорт) | subset (только экспорт) |

## Что НЕ покрыто (и почему)

| BRAVO v0.4 (отсутствует в нашей реализации) | Почему |
|---|---|
| **API Gateway** | 1 разработчик + 12 ч/нед ≠ API-сервис. Принцип: local-first. |
| **Security Module** | solo-разработчик не делает "production security" — это обязательство перед заказчиком, которое мы НЕ можем выполнить. NOT-DOING §18. |
| **UI/UX** | text/file, command-line (Expert Console v0.4). NOT-DOING §11. |
| **Treatment Manager как отдельный слой** | v0.4 разделяет validate vs treat. В нашей реализации (Iteration Loop v0.4) это **один** цикл: validate → treat → validate. Разделение не нужно для 1 dev. |
| **History DB** (отдельно от Metadata) | audit_log включает и metadata, и action history. |
| **3 Data Storage** (Metadata/Geometry/History) | 8-слойная схема соло-не подъёмна. NOT-DOING §11. |

## Архитектурные папки нашего v0.4 (декомпозиция 1 dev)

```text
BRAIM-public/
├── core/                    # BRAVO «BRAIM» + «Registry & Log» subset
│   ├── norm_graph_v0_2.json
│   ├── rules_engine/
│   ├── recipes/
│   └── adr/
├── enricher/               # BRAVIM-Client subset
│   ├── enricher_v0_3.py
│   ├── iteration_loop_v0_4.py
│   ├── safe_json_array.py
│   └── v0_4_3_archive/
├── audit/                   # Registry & Log subset
│   ├── snapshot_registry/
│   ├── activity_log/
│   └── coverage_statements/
├── input/                   # BAV Core subset
│   ├── ocr_chunks/
│   ├── pdf_extractor/
│   └── clause_chunker/
├── output/                  # Treatment Manager + Integration Hub subset
│   ├── ids_files/
│   ├── validation_reports/
│   ├── bcf_files/
│   └── golden_corpus/
├── protocols/              # API Gateway subset
│   ├── ifc_x_wrapper.py
│   └── bcf_client.py
├── docs/                    # BRAVO-Planet subset
│   ├── specs/
│   ├── architecture/        # v0_4_MAPPING.md
│   ├── methodology/
│   ├── priorities/
│   └── agents/
├── examples/                # BAV + BRAIM subset
├── _library/                # Приватный контур (только наш ПК)
│   ├── normative/
│   ├── bSDD-reference/
│   └── ocr/
└── tools/                   # BRAVIM subset
```

## Ограничения соло-разработки (Limitations, Solo Development)

> Раздел для **включения в `BRAVO_ARCHITECTURE_V0_4.md`** — для честности.

### Почему 8-слойная схема не воспроизводима одним разработчиком

| Фактор | Требование | Реальность (1 dev, 12 ч/нед) |
|---|---|---|
| Время на разработку | 8 × 1.5 = 12 unit-month | 12 ч/нед = 0.6 unit-month |
| Поддержка | 8 × 1×0.5 maintenance hours/week = 4 ч/нед | 12 ч/нед - 4 = 8 ч/нед остаётся на развитие |
| CI/CD × 8 репо | 8 × (1 ч setup + 0.5 ч maintenance) = 12 ч initial | Не подъёмно |
| Security audit × 8 | 8 × 0.5 ч/нед maintenance | **NOT-DOING §18** (на соло не делаем «production security») |
| Кросс-компонентный integration test | 8 × N тестов | Хрупкая |
| Версионирование × 8 | semver 8 репо | Усложняет F-08 |

### Что мы делаем вместо

| BRAVO v0.4 (декомпозиция 1 dev) | 1 dev = папка |
|---|---|
| 8 репо | 1 репо |
| 8 CI/CD | 1 GitHub Actions (single matrix) |
| 8 security audit | self-audit (только `sast` + manual review) |
| 8 release trains | 1 train (`main` + `feat/*`) |
| 8 витрин UI | 0 (мы text/file) |

### Где v0.4 НЕ реализуем без команды

| Что | Почему не 1 dev |
|---|---|
| API Gateway (production rate limit) | нужен JWT/auth — соло не пишет |
| Multi-tenant | клиент = 1, нет смысла |
| HA / DR | бюджет > того, что у соло |
| 24/7 SLA | NOT-DOING §18 |

## Открытые вопросы (нужны решения, прежде чем v0.4 → v0.5)

| Вопрос | Статус | Блокер для F-08? |
|---|---|---|
| Naming: RAG→NORMS_GRAPH, BAG→AUDIT_LOG, IFCA→IFC_X_WRAPPER, BRAV→BRAIM_CLIENT? | **Open** | Нет (для кода — names внутренние) |
| 8 слоёв vs 5-6 папок — финальный mapping? | **Open** (этот документ — draft) | Нет (если mapping верна для нашей реализации) |
| BRAVO как public brand vs BRAIM-only? | **Open** (можем обсудить) | Нет (в code мы используем BRAIM; BRAVO только в README) |
| F-08 timeline | Open (single F-08) | Нет (пока ищем заказ) |

## Changelog

- 0.1 — 2026-10-18: первая версия; mapping BRAVO v0.4 → 5-6 папок нашей реализации
