# IFC 5 Schema Overview for BAV

Status: Research plan  
Date: 2026-10-18  
Project: BRAVIM / Building Avatar (BAV)  
Purpose: define what to study in the IFC 5 schema and how it affects BAV / IFCA

## 1. Source

Primary repository:

https://github.com/buildingSMART/IFC5-development

Relevant area:

```text
schema/
```

All findings must include the source path, commit or release, and accessed date.

## 2. Research questions

| Question | BAV relevance |
|---|---|
| What is included in the IFC 5 Core? | Define the minimal BAV Core |
| How are types and occurrences related? | Design BAV Type → BAV Entity inheritance |
| How are external references represented? | Design BAV Reference and Planet links |
| How are property sets and templates structured? | Design BAV Attribute Profiles and Assertions |
| How is spatial containment modelled? | Design BAV Spatial Graph |
| How are relationships represented? | Design BAV graph relationships |
| How is provenance represented? | Design BAV Provenance module |
| How is lifecycle represented? | Design BAV Lifecycle module |
| How are extensions added? | Design IFCA module system |
| How is JSON serialization organized? | Design `.ifca` and future `.ifcx` alignment |

## 3. Analysis template

For every important schema area, record:

```yaml
source_id: SRC-IFC5-DEV
source_url: https://github.com/buildingSMART/IFC5-development
schema_path: schema/...
commit_or_version: <sha or release>
accessed_at: 2026-10-18
ifc5_concept: <name>
bav_concept: <name>
decision: STUDY | ADOPT | ADAPT | REJECT | DEFER
notes: <findings>
```

## 4. Initial BAV interpretation

```text
BAV Core
├── BAV ID
├── Type
├── Spatial containment
├── References
└── Extension slots
```

BAV should remain lighter than IFC: the core stores identity and structure, while domain knowledge lives in modules.

## 5. Open questions

1. Which IFC 5 Core entities are stable?
2. Which parts of the schema are likely to change?
3. Should BAV reuse IFC property-set semantics?
4. How should BAV IDs map to IFC GlobalId?
5. What is the minimal viable IFCA schema?

## 6. Status

```text
IFC 5 schema = research object
BAV = BRAVIM central model
IFCA = experimental JSON research prototype
```