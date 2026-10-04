# BRAIM-public

**BRAIM** (Building Information Atomic Model) — openBIM-oriented orchestration and information-governance layer для федеративных BIM/CDE-процессов.

> Этот репозиторий — публичное зеркало спецификаций, схем и политик BRAIM. Production IFC-артефакты хранятся в CDE заказчика и/или object storage; Git используется только для кода, схем, policy packs, mappings, ADR, snapshot manifests и Golden Corpus.

## Назначение репозитория

- Публикация версионированных спецификаций BRAIM (schemas, policy packs, mappings, ADR).
- Реестры: standards, claims, grants evidence.
- Golden Corpus и benchmark protocol для валидации.
- Документация: концепция, архитектура, дорожная карта.

## Ключевые документы

| Документ | Описание |
|---|---|
| [`BRAIM_Concept_v1.0.md`](./BRAIM_Concept_v1.0.md) | Формализованная концепция продукта, архитектура, решения, roadmap. |
| [`BRAIM_Handover_Package_v1.0_2026-09-30.md`](./BRAIM_Handover_Package_v1.0_2026-09-30.md) | Основной пакет передачи (handover) для пилота. |
| [`BRAIM_Master_Context_1.0_2026-09-30.md`](./BRAIM_Master_Context_1.0_2026-09-30.md) | Единый рабочий архитектурный baseline (локальный master). |
| [`BRAIM_STATUS_AND_OPEN_QUESTIONS.md`](./BRAIM_STATUS_AND_OPEN_QUESTIONS.md) | Текущий статус и открытые вопросы. |

## Что такое BRAIM

BRAIM — это не авторский инструмент и не замена CDE. Это оркестратор, который:

- регистрирует неизменяемые IFC/IDS/BCF/отчётные артефакты;
- запускает versioned machine-checkable policy packs;
- объединяет результаты information, geometry, topology, process и domain checks;
- принимает и сохраняет решения Quality Gate;
- создаёт immutable iteration snapshots;
- обеспечивает provenance между артефактом, правилом, валидацией, BCF issue и выпуском.

## Зафиксированные решения (пилот)

| ID | Решение | Статус |
|---|---|---|
| D-01 | CDE-master: CDE заказчика — контрактный master; BRAIM — immutable mirror + provenance | Подтверждено |
| D-02 | Git scope: только код, схемы, policy packs, mappings, ADR, snapshots, Golden Corpus | Подтверждено |
| D-03 | Strict Quality Gate: Critical→No-Go, Major→Hold, Minor→Go with findings | Подтверждено |
| D-04 | KPI: только R&D targets, проверяются benchmark protocol | Подтверждено |
| D-05 | Один глубокий пилот с реальным объектом и evidence chain | Подтверждено |
| D-06 | Neo4j Community для MVP/Phase 1–2 | Подтверждено |

## Архитектура (кратко)

```
Customer CDE (master)
    ↓
BRAIM Artifact Registry (hash, immutable mirror/reference)
    ↓
IFC integrity → IDS validation → Topology/Geometry checks
    ↓
BCF issues + JSON reports
    ↓
Quality Gate (strict decision)
    ↓
Sealed snapshot + provenance
```

Control plane: snapshot registry, policy engine, quality gate, decisions, audit. Data plane: CDE + object storage, IFC/IDS/topology workers, CDE/BCF/UI adapters. Связь через BuildBus (commands, events, artifact refs).

## Стандарты

- **IFC:** 2x3, 4, 4x3 (production); IFC5 — R&D sandbox.
- **IDS:** 1.0 (production).
- **BCF:** 3.0 (production).
- **ISO 19650:** CDE process (WIP→SHR→PUB→ARC).
- **ГОСТ Р 58439.1-2019:** коды состояния, ревизии, метаданные.

## Дорожная карта

| Фаза | Название | Длительность | Результат |
|---|---|---|---|
| 0 | Фундамент | 4–6 нед. | Naming, Snapshot Schema, BRAIM-LIMS 0.1, Golden Corpus |
| 1 | Транспорт | 6–8 нед. | IFC→Neo4j, provenance, vertical slice (CDE→Gate→Snapshot) |
| 2 | Валидация | 8–10 нед. | IDS, topology validator, BCF reports, benchmark |
| 3 | Оркестратор | 8–12 нед. | Quality Gate, BuildBus, snapshot manager, CDE adapter |
| 4 | UI | 6–8 нед. | Viewer, dashboard, evidence timeline |

## Статус

- **Версия спецификации:** 0.1.0 (draft).
- **Пилот:** Республика Татарстан, Россия.
- **Следующие действия:** Phase 0 — architecture freeze, schemas, BRAIM-LIMS 0.1, Golden Corpus, CDE capability discovery.

## Лицензия и контакты

- Репозиторий: [kirsunn/BRAIM-public](https://github.com/kirsunn/BRAIM-public)
- Лицензия: [указать при публикации]

---

*Последнее обновление: 2026-10-04*
