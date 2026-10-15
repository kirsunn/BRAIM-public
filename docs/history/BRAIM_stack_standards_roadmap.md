# BRAIM: полный стек, стандарты, дорожная карта и технический долг

> Версия документа: Research Draft
> Дата: 2026-09-30
> Связанные файлы: BRAIM_glossary_final.md, BRAIM_full_stack.md

---

## 1. Стек технологий — слои и версии

Все версии проверены на актуальность по состоянию на сентябрь 2026.

### 1.1. Схема стека

```
┌─────────────────────────────────────────────────────┐
│  8. BRAIM (оркестратор)                               │
│     шина + Quality Gate + снапшоты + транзакции       │
│     🔨 СТРОИМ                                         │
├─────────────────────────────────────────────────────┤
│  7. Веб-просмотр                                      │
│     That Open (web-ifc, WASM)  · IFClite (Rust+WASM)  │
│     ✅ OPEN-SOURCE                                    │
├─────────────────────────────────────────────────────┤
│  6. Авторинг                                          │
│     Bonsai (BlenderBIM) — нативная IFC-запись + git   │
│     ✅ OPEN-SOURCE (GPL)                              │
├─────────────────────────────────────────────────────┤
│  5. Связь и обмен замечаниями                         │
│     BCF API 3.0 (REST/JSON) · BCF-XML 3.0             │
│     OpenCDE API (Foundation 1.1, Documents 1.0)      │
│     ✅ ОТКРЫТЫЕ СТАНДАРТЫ                             │
├─────────────────────────────────────────────────────┤
│  4. Валидация                                         │
│     IfcTester 0.8.5 (IDS) · Xbim.IDS.Validator (.NET) │
│     ✅ OPEN-SOURCE                                    │
├─────────────────────────────────────────────────────┤
│  3. Граф                                              │
│     IfcOpenShell 0.8.5 → Neo4j (Cypher)               │
│     ✅ OPEN-SOURCE                                    │
├─────────────────────────────────────────────────────┤
│  2. Версионирование                                    │
│     git + ifcmerge (Rust, 3-way merge)                │
│     + ifc-commit (Pset_GitCommit provenance)          │
│     ✅ OPEN-SOURCE                                    │
├─────────────────────────────────────────────────────┤
│  1. Хранение                                          │
│     git (IFC-файлы) · Neo4j (граф связей)             │
│     CDE (контейнеры + метаданные)                     │
│     ✅ OPEN-SOURCE / СУЩЕСТВУЮЩИЕ CDE                 │
├─────────────────────────────────────────────────────┤
│  0. Форматы                                           │
│     IFC 4.3.2.0 · IDS 1.0 · BCF 3.0 · bSDD            │
│     ✅ ОТКРЫТЫЕ СТАНДАРТЫ buildingSMART               │
└─────────────────────────────────────────────────────┘
```

### 1.2. Версии и статусы

| Слой | Компонент | Версия | Статус | Лицензия |
|---|---|---|---|---|
| 0 | IFC | 4.3.2.0 (build 20260924) | Working Draft → Candidate | открытый стандарт |
| 0 | IDS | 1.0 (утверждён 3 июня 2024) | Final Standard | открытый стандарт |
| 0 | BCF | 3.0 (XML + API) | Final Standard | открытый стандарт |
| 0 | BCF API | 4.0 | в разработке | открытый стандарт |
| 0 | OpenCDE API | Foundation 1.1, Documents 1.0 | Final / GitHub | открытый стандарт |
| 0 | bSDD | актуальная | Live service | открытый словарь |
| 1 | git | 2.x | Stable | GPL |
| 1 | Neo4j | 5.x Community / Enterprise | Stable | GPLv3 / Commercial |
| 2 | ifcmerge | alpha/pre-release | Экспериментальный | open-source (Rust) |
| 2 | ifc-commit | pre-release | Экспериментальный | open-source |
| 3 | IfcOpenShell | 0.8.5 (13 апреля 2026) | Stable | LGPL / MIT |
| 4 | IfcTester | 0.8.5 (13 апреля 2026) | Stable | LGPL |
| 4 | Xbim.IDS.Validator | 1.x (.NET) | Stable, 100% IDS test pass | открытый (xCAD) |
| 5 | bcf-client (Python) | 0.8.5 | Stable (в составе IfcOpenShell) | LGPL |
| 6 | Bonsai (BlenderBIM) | 0.8.5 | Stable | GPL |
| 7 | That Open Engine | актуальная | Stable | MIT |
| 7 | IFClite | актуальная | Stable | MPL 2.0 |
| 8 | **BRAIM** | — | 🔨 **СТРОИМ** | TBD |

### 1.3. Что берём готовым vs что строим

| Компонент | Источник | Зрелость | Действие |
|---|---|---|---|
| IFC чтение/запись/геометрия | IfcOpenShell 0.8.5 | production-ready | берём как есть |
| IFC → граф (Neo4j) | IfcOpenShell + py2neo | проверено в исследованиях | собираем пайплайн |
| IDS-валидация (свойства, классы) | IfcTester 0.8.5 | production-ready | берём как есть |
| IDS-валидация (.NET альтернатива) | Xbim.IDS.Validator | production-ready | берём как есть |
| BCF (замечания, топики) | bcf-client + BCF API 3.0 | production-ready | берём как есть |
| git-ветвление для IFC | ifcmerge + ifc-commit | экспериментальный | **адаптируем, тестируем** |
| visual diff (3D) | Bonsai | работает в Bonsai | **интегрируем через API** |
| веб-просмотр IFC | That Open / IFClite | production-ready | берём как есть |
| OpenCDE API (документы) | Foundation 1.1 + Documents 1.0 | final standard | **реализуем сервер** |
| **Оркестратор (шина)** | — | не существует | **СТРОИМ** |
| **Quality Gate** | — | не существует | **СТРОИМ** |
| **Снапшот (JSON Schema)** | — | не существует | **СТРОИМ** |
| **Геометрический валидатор** | — | частично в IfcOpenShell | **ДОСТРАИВАЕМ** |
| **Топологический валидатор** | — | не существует | **СТРОИМ** |

---

## 2. Стандарты — реестр

### 2.1. Международные стандарты (buildingSMART / ISO)

| Стандарт | Версия | Что даёт BRAIM | Статус в РФ |
|---|---|---|---|
| **ISO 19650-1** | 2018 | Принципы CDE, понятие контейнера, статусы | принят как ГОСТ Р 58439.1-2019 |
| **ISO 19650-2** | 2018 | Рабочие процессы, коды состояний (WIP/SHR/PUB/ARC) | принят как ГОСТ Р 58439.2-2019 |
| **ISO 19650-3** | 2020 | Эксплуатационная модель | принят |
| **ISO 19650-5** | 2020 | Информационная безопасность | принят |
| **ISO 7817-1** | 2024 | Level of Information Need (LoIN) | на рассмотрении |
| **IFC** | 4.3.2.0 | Формат данных модели | ISO 16739-1:2024 |
| **IDS** | 1.0 | Требования к информации, 6 фасетов | buildingSMART Final |
| **BCF** | 3.0 (XML + API) | Обмен замечаниями | buildingSMART Final |
| **OpenCDE API** | Foundation 1.1, Documents 1.0 | REST-интерфейс к CDE | buildingSMART Final |
| **bSDD** | live | Словарь свойств и классификаций | buildingSMART Live |
| **ISO 12006-3** | 2021 | Модель данных строительных объектов (основа bSDD) | принят |

### 2.2. Российские стандарты

| Стандарт | Что даёт | Соответствие BRAIM |
|---|---|---|
| **ГОСТ Р 58439.1-2019** | Термины и общие принципы BIM | базовые термины — используем |
| **ГОСТ Р 58439.2-2019** | Рабочие процессы, CDE | статусы — берём, адаптируем |
| **ГОСТ Р 10.04.0001** | ЕСИМ, базовые подходы | контейнер + метаданные |
| **Методические рекомендации Минстроя** | Сводная ИМ, федеративная модель | совпадает с нашим определением |
| **СП 301.1325800.2017** | Требования к ЭМ | при необходимости |

### 2.3. Стандарты BRAIM (внутренние, разрабатываем)

| Документ | Статус | Что фиксирует |
|---|---|---|
| **BRAIM-LIMS** | Research Draft 0.x | Спецификация стандартов, словарь, фасеты |
| **Iteration Snapshot Schema** | 🔨 нет | JSON Schema снапшота итерации |
| **Naming Convention** | 🔨 нет | Правила именования контейнеров |
| **Quality Gate Spec** | 🔨 нет | Критерии Go / Hold / No-Go |
| **Provenance Spec** | 🔨 нет | Формат записи provenance |
| **Geometric Validator Spec** | 🔨 нет | Три уровня проверок, формат отчёта BCF |

---

## 3. JSON Schema снапшота итерации

### 3.1. Иерархия пяти уровней

```
standard_version   — версия спецификации BRAIM (semver: 0.x → 1.0)
iteration_snapshot — снимок проектной итерации (неизменяемый)
release            — выпуск модели для обмена (несколько на снапшот)
revision           — внутренняя итерация работы над release
cde_state          — состояние в СОД (WIP / SHR / PUB / ARC) — метаданные
```

### 3.2. Формальная схема

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://braim.dev/schemas/iteration-snapshot.json",
  "title": "BRAIM Iteration Snapshot",
  "description": "Неизменяемый снимок проектной итерации. Связывает версию стандарта, проект, итерацию ЖЦ, release/revision, CDE-состояния, варианты и решения.",
  "type": "object",
  "required": [
    "snapshot_id",
    "project_id",
    "iteration_id",
    "baim_standard_version",
    "created_at",
    "created_by",
    "baseline_ref",
    "status"
  ],
  "properties": {
    "snapshot_id": {
      "type": "string",
      "format": "uuid",
      "description": "Уникальный идентификатор снапшота (UUID v4)"
    },
    "project_id": {
      "type": "string",
      "description": "Идентификатор проекта/объекта"
    },
    "iteration_id": {
      "type": "string",
      "pattern": "^IT[0-9]{3}$",
      "description": "Номер итерации (счётчик снимков), формат IT001"
    },
    "parent_snapshot_id": {
      "type": ["string", "null"],
      "format": "uuid",
      "description": "Снапшот-предок. null для начальной итерации. При merge — массив в parent_snapshot_ids"
    },
    "parent_snapshot_ids": {
      "type": "array",
      "items": { "type": "string", "format": "uuid" },
      "description": "Снапшоты-предки при слиянии веток (DAG). Пустой массив = линейное продолжение"
    },
    "baim_standard_version": {
      "type": "string",
      "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$",
      "description": "Версия спецификации BRAIM (semver)"
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
    "created_by": {
      "type": "string",
      "description": "Автор снапшота (актёр или система)"
    },
    "description": {
      "type": "string",
      "description": "Человекочитаемое описание итерации"
    },
    "status": {
      "type": "string",
      "enum": ["draft", "fixed", "superseded"],
      "description": "Жизненный цикл самого снапшота: draft → fixed (неизменяем) → superseded (заменён новой итерацией)"
    },
    "scope": {
      "type": "object",
      "description": "Область изменений в данной итерации",
      "properties": {
        "affected_elements": {
          "type": "array",
          "items": { "type": "string" },
          "description": "GUID затронутых элементов IFC"
        },
        "affected_spaces": {
          "type": "array",
          "items": { "type": "string" },
          "description": "GUID затронутых пространств"
        },
        "disciplines": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["arch", "struct", "mep", "infra", "other"]
          }
        }
      }
    },
    "baseline_model_ref": {
      "type": "object",
      "description": "Ссылка на базовую модель (опорную ИМ)",
      "properties": {
        "container_id": { "type": "string" },
        "ifc_guid": { "type": "string" },
        "git_commit_hash": { "type": "string" },
        "mvd": { "type": "string", "description": "Model View Definition" }
      },
      "required": ["container_id", "git_commit_hash"]
    },
    "releases": {
      "type": "array",
      "description": "Выпуски модели для обмена (несколько на снапшот)",
      "items": {
        "type": "object",
        "required": ["release_id", "release_number", "cde_state", "container_ref"],
        "properties": {
          "release_id": {
            "type": "string",
            "format": "uuid"
          },
          "release_number": {
            "type": "string",
            "pattern": "^R[0-9]{2}$",
            "description": "Номер релиза, формат R01"
          },
          "revisions": {
            "type": "array",
            "description": "Внутренние итерации работы над release",
            "items": {
              "type": "object",
              "required": ["revision_number", "author", "timestamp"],
              "properties": {
                "revision_number": {
                  "type": "string",
                  "pattern": "^\\.[0-9]{2}$",
                  "description": "Номер ревизии, формат .01"
                },
                "author": { "type": "string" },
                "timestamp": { "type": "string", "format": "date-time" },
                "change_description": { "type": "string" }
              }
            }
          },
          "cde_state": {
            "type": "string",
            "enum": ["WIP", "SHR", "PUB", "ARC"],
            "description": "Состояние в СОД — метаданные, не часть имени файла"
          },
          "container_ref": {
            "type": "object",
            "properties": {
              "container_id": { "type": "string" },
              "file_name": { "type": "string" },
              "file_uri": { "type": "string", "format": "uri" },
              "classification_code": { "type": "string" }
            }
          },
          "mvd": {
            "type": "string",
            "description": "Model View Definition — в метаданных, не в имени"
          }
        }
      }
    },
    "variants": {
      "type": "array",
      "description": "Рассмотренные варианты (пена)",
      "items": {
        "type": "object",
        "required": ["variant_id", "description", "outcome"],
        "properties": {
          "variant_id": { "type": "string", "format": "uuid" },
          "description": { "type": "string" },
          "source_branch": { "type": "string", "description": "git branch name" },
          "fork_parent": {
            "type": "string",
            "format": "uuid",
            "description": "snapshot_id, от которого ответвился вариант"
          },
          "outcome": {
            "type": "string",
            "enum": ["accepted", "rejected", "deferred", "merged"],
            "description": "Решение по варианту"
          },
          "quality_gate_result": {
            "type": "string",
            "enum": ["Go", "Hold", "No-Go"],
            "description": "Результат Quality Gate для варианта"
          }
        }
      }
    },
    "decisions": {
      "type": "array",
      "description": "Принятые решения",
      "items": {
        "type": "object",
        "required": ["decision_id", "description", "decided_by", "decided_at"],
        "properties": {
          "decision_id": { "type": "string", "format": "uuid" },
          "description": { "type": "string" },
          "rationale": { "type": "string" },
          "decided_by": { "type": "string" },
          "decided_at": { "type": "string", "format": "date-time" },
          "related_variants": {
            "type": "array",
            "items": { "type": "string", "format": "uuid" }
          }
        }
      }
    },
    "provenance": {
      "type": "object",
      "description": "Происхождение снапшота — история и связи",
      "properties": {
        "git_commit_hash": {
          "type": "string",
          "description": "Хэш git-коммита, в котором зафиксирован снапшот"
        },
        "git_branch": { "type": "string" },
        "git_tags": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Теги git (milestones: issued-for-construction, as-built, ...)"
        },
        "ifcgit_pset": {
          "type": "object",
          "description": "Данные из Pset_GitCommit (если используется ifc-commit)",
          "properties": {
            "commit_hash": { "type": "string" },
            "commit_author": { "type": "string" },
            "commit_branch": { "type": "string" },
            "commit_message": { "type": "string" }
          }
        },
        "transformation_log": {
          "type": "array",
          "description": "Журнал трансформаций графа (для графового diff/merge)",
          "items": {
            "type": "object",
            "properties": {
              "operation": {
                "type": "string",
                "enum": ["add", "remove", "modify", "glue", "push-out", "context"]
              },
              "target_guid": { "type": "string" },
              "target_class": { "type": "string" },
              "timestamp": { "type": "string", "format": "date-time" }
            }
          }
        }
      }
    },
    "quality_gate": {
      "type": "object",
      "description": "Результат проверки Quality Gate перед фиксацией снапшота",
      "required": ["result", "checked_at"],
      "properties": {
        "result": {
          "type": "string",
          "enum": ["Go", "Hold", "No-Go"]
        },
        "checked_at": { "type": "string", "format": "date-time" },
        "checked_by": { "type": "string" },
        "checks": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["check_id", "check_type", "passed"],
            "properties": {
              "check_id": { "type": "string" },
              "check_type": {
                "type": "string",
                "enum": ["geometric", "topological", "functional", "ids"]
              },
              "passed": { "type": "boolean" },
              "details": { "type": "string" },
              "bcf_topic_guid": {
                "type": "string",
                "description": "GUID BCF-топика, если есть замечание"
              }
            }
          }
        }
      }
    },
    "profiles": {
      "type": "array",
      "description": "Профили BRAIM, применённые в итерации",
      "items": {
        "type": "object",
        "properties": {
          "profile_id": { "type": "string" },
          "profile_name": { "type": "string" },
          "facet_filters": {
            "type": "object",
            "description": "Активные фасеты в данной итерации"
          }
        }
      }
    }
  }
}
```

### 3.3. Пример заполненного снапшота

```json
{
  "snapshot_id": "550e8400-e29b-41d4-a716-446655440000",
  "project_id": "PRJ-2026-001",
  "iteration_id": "IT004",
  "parent_snapshot_id": "550e8400-e29b-41d4-a716-446655440001",
  "parent_snapshot_ids": [],
  "baim_standard_version": "0.4.2",
  "created_at": "2026-09-30T19:10:23+03:00",
  "created_by": "architect@studio.ru",
  "description": "Реконструкция 4 этажа: переразмещение технических помещений",
  "status": "fixed",
  "scope": {
    "affected_elements": ["3xWp...guid1", "3xWp...guid2"],
    "affected_spaces": ["2xWp...space1"],
    "disciplines": ["arch", "mep"]
  },
  "baseline_model_ref": {
    "container_id": "CTR-IT003-R02",
    "ifc_guid": "2xWp...root",
    "git_commit_hash": "a1b2c3d4e5f6",
    "mvd": "ReferenceView"
  },
  "releases": [
    {
      "release_id": "rel-001",
      "release_number": "R01",
      "revisions": [
        {
          "revision_number": ".01",
          "author": "architect@studio.ru",
          "timestamp": "2026-09-28T10:00:00+03:00",
          "change_description": "Начальная редакция"
        },
        {
          "revision_number": ".02",
          "author": "mep@studio.ru",
          "timestamp": "2026-09-29T14:00:00+03:00",
          "change_description": "Добавлены воздуховоды"
        }
      ],
      "cde_state": "SHR",
      "container_ref": {
        "container_id": "CTR-IT004-R01",
        "file_name": "PRJ-2026-001-IT004-R01.02.ifc",
        "file_uri": "cde://projects/PRJ-2026-001/IT004/R01.02.ifc",
        "classification_code": "Uniclass EF_25"
      },
      "mvd": "ReferenceView"
    }
  ],
  "variants": [
    {
      "variant_id": "var-001",
      "description": "Вариант А: коридор 1.8 м",
      "source_branch": "IT004-corridor-wide",
      "fork_parent": "550e8400-e29b-41d4-a716-446655440001",
      "outcome": "accepted",
      "quality_gate_result": "Go"
    },
    {
      "variant_id": "var-002",
      "description": "Вариант Б: коридор 1.5 м",
      "source_branch": "IT004-corridor-narrow",
      "fork_parent": "550e8400-e29b-41d4-a716-446655440001",
      "outcome": "rejected",
      "quality_gate_result": "No-Go"
    }
  ],
  "decisions": [
    {
      "decision_id": "dec-001",
      "description": "Принят вариант А (коридор 1.8 м) — соответствует СП",
      "rationale": "Минимальная ширина коридора 1.5 м не проходит функциональную проверку",
      "decided_by": "architect@studio.ru",
      "decided_at": "2026-09-30T18:00:00+03:00",
      "related_variants": ["var-001", "var-002"]
    }
  ],
  "provenance": {
    "git_commit_hash": "f6e5d4c3b2a1",
    "git_branch": "IT004-main",
    "git_tags": ["issued-for-coordination"],
    "ifcgit_pset": {
      "commit_hash": "f6e5d4c3b2a1",
      "commit_author": "architect@studio.ru",
      "commit_branch": "IT004-main",
      "commit_message": "IT004: corridor redesign accepted"
    }
  },
  "quality_gate": {
    "result": "Go",
    "checked_at": "2026-09-30T18:30:00+03:00",
    "checked_by": "braim-orchestrator",
    "checks": [
      {
        "check_id": "chk-001",
        "check_type": "ids",
        "passed": true,
        "details": "All IDS requirements met (Pset_WallCommon.FireRating present)"
      },
      {
        "check_id": "chk-002",
        "check_type": "geometric",
        "passed": true,
        "details": "No clashes detected"
      },
      {
        "check_id": "chk-003",
        "check_type": "topological",
        "passed": true,
        "details": "All spaces watertight, normals correct"
      },
      {
        "check_id": "chk-004",
        "check_type": "functional",
        "passed": true,
        "details": "Corridor width ≥ 1.8 m (SP requirement)"
      }
    ]
  },
  "profiles": [
    {
      "profile_id": "prof-reconstruction",
      "profile_name": "Реконструкция",
      "facet_filters": {
        "discipline": ["arch", "mep"],
        "stage": "detailed_design"
      }
    }
  ]
}
```

---

## 4. Дорожная карта

### 4.1. Фазы разработки

```
Фаза 0 — Фундамент (4–6 недель)
│
├── 0.1  JSON Schema снапшота → валидация, тесты
├── 0.2  Naming Convention → спецификация имени файла
├── 0.3  Provenance Spec → формат записи (включая Pset_GitCommit)
├── 0.4  Quality Gate Spec → критерии Go / Hold / No-Go
└── 0.5  Базовый git-репозиторий → структура, .gitignore, hooks

Фаза 1 — Транспорт (6–8 недель)
│
├── 1.1  IfcOpenShell → Neo4j пайплайн (IFC → граф)
├── 1.2  ifcmerge → тестирование, адаптация под наши сценарии
├── 1.3  ifc-commit → интеграция Pset_GitCommit
├── 1.4  BCF-клиент → приём и отправка BCF-топиков
└── 1.5  OpenCDE API сервер → Foundation + Documents (минимальный)

Фаза 2 — Валидация (8–10 недель)
│
├── 2.1  IfcTester → IDS-проверки (функциональный уровень)
├── 2.2  Геометрический валидатор → clash, distance, duplicates
├── 2.3  Топологический валидатор → watertight, normals, adjacency
├── 2.4  Сводный отчёт → BCF из всех трёх уровней
└── 2.5  Quality Gate → оркестрация проверок, решение Go / Hold / No-Go

Фаза 3 — Оркестратор (8–12 недель)
│
├── 3.1  Шина BRAIM → маршрутизация вызовов между движками
├── 3.2  lifecycle_fork → создание/слитие веток, DAG
├── 3.3  Снапшот-менеджер → создание, фиксация, сравнение
├── 3.4  Профили BRAIM → применение фасетов к итерациям
└── 3.5  API BRAIM → REST для внешних систем

Фаза 4 — UI и интеграция (6–8 недель)
│
├── 4.1  Веб-просмотр IFC (That Open / IFClite)
├── 4.2  Visual diff (подсветка изменений в 3D)
├── 4.3  Dashboard итераций и снапшотов
└── 4.4  Интеграция с Bonsai (нативный авторинг)
```

### 4.2. Зависимости между фазами

```
0.1 (Schema) ──┬──> 1.1 (пайплайн) ──> 2.1 (IDS) ──┐
0.2 (Naming) ──┤                                   ├──> 3.1 (шина) ──> 4.1 (UI)
0.3 (Provenance)┤──> 1.3 (ifc-commit) ──────────────┤
0.4 (QG Spec) ─┤──> 1.2 (ifcmerge) ──> 2.2 (geom) ─┤
0.5 (git repo) ─┘──> 1.4 (BCF) ──> 2.3 (topo) ─────┘──> 2.4 (отчёт) ──> 2.5 (QG) ──> 3.2 (fork) ──> 3.3 (snapshot)
```

---

## 5. Технический долг

### 5.1. Категории долга

| Категория | Что значит | Риск |
|---|---|---|
| **Структурный** | нет формальной схемы, нет спецификации | блокирует разработку |
| **Зависимостный** | опираемся на экспериментальный инструмент | может сломаться |
| **Совместимостный** | стандарты развиваются, версии меняются | устаревание |
| **Интеграционный** | компоненты не склеены в один конвейер | ручная работа |
| **Методологический** | правила определены концептуально, но не формализованы | двоякие трактовки |

### 5.2. Реестр долга

| ID | Категория | Что | Влияние | План закрытия | Фаза |
|---|---|---|---|---|---|
| D-01 | Структурный | Нет формальной JSON Schema снапшота | блокирует хранение и сравнение | **закрыто в этом документе** (раздел 3) | 0 |
| D-02 | Структурный | Нет спецификации Naming Convention | двоякие имена файлов | спецификация в Фазе 0 | 0 |
| D-03 | Структурный | Нет спецификации Quality Gate | нет критериев Go/Hold/No-Go | спецификация в Фазе 0 | 0 |
| D-04 | Структурный | Нет спецификации Provenance | непонятно, что хранить | спецификация в Фазе 0 | 0 |
| D-05 | Зависимостный | ifcmerge — alpha/pre-release | merge IFC может сломаться | тестирование в Фазе 1, fallback — ручное слияние | 1 |
| D-06 | Зависимостный | ifc-commit — pre-release | provenance может не записаться | интеграция в Фазе 1, fallback — ручная запись в снапшот | 1 |
| D-07 | Зависимостный | IFC 4.3.2.0 — Working Draft | формат может измениться | использовать IFC 4.3 как основу, отслеживать изменения | 0–4 |
| D-08 | Совместимостный | BCF API 4.0 в разработке | расширения могут измениться | использовать 3.0, мониторить 4.0 | 1–3 |
| D-09 | Совместимостный | IDS 1.1 и 2.0 планируются | новые фасеты, изменённая семантика | использовать IDS 1.0, закладывать расширяемость | 0–4 |
| D-10 | Совместимостный | OpenCDE Documents API 1.0 — минимальный | нет вложенности контейнеров | расширять в BRAIM-слое | 1 |
| D-11 | Интеграционный | IFC → Neo4j пайплайн не автоматизирован | ручная загрузка | сборка пайплайна в Фазе 1 | 1 |
| D-12 | Интеграционный | IfcTester → BCF не склеен с топологией | два раздельных отчёта | единый BCF в Фазе 2 | 2 |
| D-13 | Методологический | Правило «класс vs свойство» концептуально | разные реализации | формализация в BRAIM-LIMS | 0 |
| D-14 | Методологический | Правила lifecycle_fork концептуальны | нет формального DAG-контракта | спецификация в Фазе 3 | 3 |
| D-15 | Структурный | Нет геометрического валидатора (топология) | функциональные проверки не работают | разработка в Фазе 2 | 2 |
| D-16 | Интеграционный | Bonsai git-интеграция — в Bonsai, не вынесена | привязка к одному авторингу | API-обёртка в Фазе 3 | 3 |
| D-17 | Методологический | ГОСТ Р 58439 не покрывает fork/snapshot | несоответствие РФ-стандартам | расширение в BRAIM-СТО | 0–4 |
| D-18 | Зависимостный | IFClite — независимый проект | может прекратить развитие | fallback — That Open Engine | 4 |

### 5.3. Приоритизация долга

**Блокирующее (закрыть в Фазе 0):** D-01, D-02, D-03, D-04, D-13
**Высокий риск (закрыть в Фазе 1):** D-05, D-06, D-11
**Средний риск (Фаза 2–3):** D-12, D-14, D-15, D-16
**Мониторинг (весь проект):** D-07, D-08, D-09, D-10, D-17, D-18

---

## 6. Сводка: что у нас есть и чего нет

| Есть (готово / open-source) | Нет (строим) |
|---|---|
| IFC — формат данных модели | Оркестратор (шина) |
| IDS — требования к информации | Quality Gate (Go/Hold/No-Go) |
| BCF — обмен замечаниями | Снапшот — формальная схема (**закрыта здесь**) |
| IfcOpenShell — чтение/запись IFC | Геометрический валидатор (топология) |
| IfcTester — IDS-валидация | Топологический валидатор |
| Neo4j — графовая база | Naming Convention (спецификация) |
| git — версионирование | Provenance Spec (формальная) |
| ifcmerge — слияние IFC (alpha) | lifecycle_fork (формальный DAG-контракт) |
| ifc-commit — provenance в IFC (pre) | OpenCDE API сервер (минимальный) |
| Bonsai — нативный авторинг IFC | Веб-UI итераций и снапшотов |
| That Open / IFClite — веб-просмотр | Профили BRAIM (применение фасетов) |
| OpenCDE API — стандарт | BRAIM API (REST для внешних систем) |
