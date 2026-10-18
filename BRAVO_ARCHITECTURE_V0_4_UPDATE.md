# BRAVO v0.4 Architecture Update

Date: 2026-10-18
Status: Current architecture baseline

## Key change

BRAIM is hosted inside BRAVIUM-Planet. It is not a separate intermediate layer between Planet and BRAVIM.

```text
BRAVIUM-Planet (cloud)
├── BRAIM — criteria, norms, integrations
├── Project Registry
├── Ruleset Packages
└── Evidence / Knowledge Base

        ↕ API

BRAVIM (local client)
└── BRAV container
    ├── IFCA — exchange
    ├── BAR — version registry
    ├── BAV — building avatar
    ├── RAG — requirements and constraints graph
    └── BAG — activity log
```

## Updated formula

```text
BRAV = IFCA + BAR + BAV + RAG + BAG
```

| Component | Role |
|---|---|
| BRAIM | Cloud knowledge core: criteria, norms, integrations |
| BRAVIM | Local client: project work, validation, UI |
| BRAV | Project container |
| IFCA | Exchange format |
| BAR | Avatar and version registry |
| BAV | Building avatar |
| RAG | Requirements & Constraints Graph |
| BAG | Activity log |

## Main flow

```text
BRAVIM requests applicable knowledge through the Planet API.
BRAIM provides current criteria and Ruleset Package versions.
BRAVIM pins the version and validates BAV against RAG.
BAG records every important action and decision.
A human approves changes.
```

The full specification is available in [`BRAVO_ARCHITECTURE_V0_4.md`](./BRAVO_ARCHITECTURE_V0_4.md).