# braim-spec

Governing repository для спецификаций, схем и политик BRAIM.

## Структура

```
braim-spec/
├── README.md              # Этот файл
├── adr/                   # Architectural Decision Records
│   └── 0001-source-of-truth-and-cde-master.md
├── schemas/               # JSON Schemas
│   ├── artifact.json
│   ├── snapshot.json
│   ├── decision.json
│   ├── event.json
│   ├── validation-result.json
│   └── policy-manifest.json
├── policy-packs/          # Versioned policy packs
│   ├── ids-profiles/
│   ├── topology-rules/
│   └── thermal-protection/
├── mappings/              # IFC-to-CBIM и CBIM-to-graph mapping profiles
│   ├── ifc2x3-mapping-profile.json
│   ├── ifc4-mapping-profile.json
│   └── ifc4x3-mapping-profile.json
├── registers/             # Standards, claims, grants registers
│   ├── standards-register.json
│   ├── claims-register.json
│   └── grants-evidence-register.json
├── golden-corpus/         # Test cases и expected results
│   ├── ifc2x3/
│   ├── ifc4/
│   ├── ifc4x3/
│   ├── ifc5-alpha-sandbox/
│   ├── invalid/
│   ├── ids/
│   ├── bcf/
│   ├── topology/
│   ├── diff/
│   ├── thermal/
│   ├── cde-fixtures/
│   └── expected/
├── benchmark-protocol/    # Benchmark protocol и CI baseline
│   ├── protocol.md
│   └── ci-baseline.yaml
├── grant-evidence-register/ # Evidence для грантов
│   └── evidence-log.json
└── docs/                  # Дополнительная документация
    ├── architecture-overview.md
    ├── buildbus-specification.md
    └── quality-gate-specification.md
```

## Статус

- **Версия:** 0.1.0 (draft)
- **Дата:** 2026-10-04
- **Следующие действия:**
  - P0-03: JSON Schema (artifact, snapshot, decision, event)
  - P0-04: BRAIM-LIMS 0.1
  - P0-05: Registers (standards, claims, grants)
  - P0-06: Golden Corpus structure
  - P0-07: Toolchain SBOM

## Связанные документы

- [BRAIM_Concept_v1.0.md](../BRAIM_Concept_v1.0.md)
- [BRAIM_STATUS_AND_OPEN_QUESTIONS.md](../BRAIM_STATUS_AND_OPEN_QUESTIONS.md)
- [BRAIM_Handover_Package_v1.0_2026-09-30.md](../BRAIM_Handover_Package_v1.0_2026-09-30.md)

---

*Последнее обновление: 2026-10-04*
