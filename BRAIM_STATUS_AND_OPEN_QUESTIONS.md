# BRAIM Status and Open Questions

## Статус

- Версия: `0.1.0`
- Дата: 2026-09-28
- Release class: `CONCEPT_AND_PROTOTYPE`
- Public status: `DOCUMENTATION_PREVIEW`

## Уже сформулировано

- единая мультислойная сущность;
- семантические слои `L0–L15`;
- дисциплинарные представления `D0–D13`;
- единый `instance_id` во всех представлениях;
- источник истины и владелец атрибутов;
- provenance, validation и verification;
- микрокернельная архитектура, plugin manager, zero bus и оркестратор;
- различение помещения, зоны, ниши, проёма и заполнения;
- `PLAN_TO_FORM`, `FORM_TO_PLAN` и итерация планировка ↔ форма ↔ фасад;
- геодезия, облака точек, scan-to-BIM и шестигранный swept-loop дом.

## Пока не реализовано

```text
BRAIM Core runtime
Schema Registry
Attribute Registry
Claim/Evidence Registry
Model View Registry
CDE state machine
Dependency/impact engine
JSON Schema tests
Rules engine
Topology-first layout solver
Form-to-plan solver
Plan-to-form solver
Hexagonal form geometry engine
Point cloud processing implementation
Scan-to-BIM pipeline
IFC4X3 implementation
IDS/BCF integration
Archicad connector
Control Center
Public release automation
```

## Открытые вопросы

1. Утвердить английскую расшифровку BRAIM.
2. Утвердить окончательную структуру `L0–L15`.
3. Утвердить набор дисциплин `D0–D13`.
4. Решить, является ли IFC транспортом или внешним представлением.
5. Определить canonical storage.
6. Утвердить JSON Schema для сущности.
7. Утвердить источники численных требований.
8. Определить точную модель `Room` и `FunctionalRoom/FinishRoom`.
9. Выбрать геометрический движок.
10. Определить публичную лицензию.

Ничего не считать реализованным только потому, что это описано в драфте. Документированная идея имеет статус `SPECIFIED`, пока не существуют schema, implementation, test и validation report.
