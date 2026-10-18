# IFC 5 Examples Review for BAV

Status: Research plan  
Date: 2026-10-18  
Project: BRAVIM / Building Avatar (BAV)  
Purpose: define how to study IFC 5 examples and extract patterns for BAV / IFCA

## 1. Source

Primary repository:

https://github.com/buildingSMART/IFC5-development

Relevant area:

```text
examples/
```

IFC 5 examples are alpha materials. They are useful for learning and prototyping, but must not be treated as production-ready.

## 2. What to study

| Example aspect | Research question | BAV relevance |
|---|---|---|
| Project composition | How is a project structured? | BAV project root |
| Spatial structure | How are site, building, storey and space connected? | BAV Spatial Graph |
| Elements | How are walls, doors, windows and openings represented? | BAV Entity and relationships |
| Types | How are type definitions separated from occurrences? | BAV Type → BAV Entity |
| Properties | How are property sets attached? | BAV Attribute Sets and Assertions |
| References | How are external files and data linked? | BAV Reference and Planet links |
| JSON structure | How is the `.ifcx` JSON organized? | IFCA serialization |
| Viewer data | What does the viewer need to display? | BAV Viewer requirements |

## 3. Example review template

```yaml
example: <file or directory>
source_id: SRC-IFC5-DEV
source_url: https://github.com/buildingSMART/IFC5-development
path: examples/...
commit_or_version: <sha or release>
accessed_at: 2026-10-18
observed_pattern: <what IFC 5 does>
bav_interpretation: <how BAV would represent it>
ifca_decision: STUDY | ADOPT | ADAPT | REJECT | DEFER
notes: <findings>
```

## 4. Minimal BAV example to derive

From the IFC 5 examples, derive a minimal BAV scenario:

```text
Site
└── Building
    └── Storey
        └── Space
            └── Wall
                └── Opening
                    └── Door
```

This will become the first `.ifca` prototype.

## 5. Open questions

1. Which examples best represent a minimal building?
2. How are openings and fillings related?
3. How are types reused across occurrences?
4. How are external references expressed?
5. What minimum data is needed for a useful BAV Viewer?

## 6. Status

```text
IFC 5 examples = research material
BAV = BRAVIM central model
IFCA = experimental JSON research prototype
```