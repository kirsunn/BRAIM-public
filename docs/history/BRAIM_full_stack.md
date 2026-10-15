# BRAIM Full Stack — технологический стек

> Связанная карта технологий: что используется на каждом слое, какие стандарты, какие реализации.
> Принцип: **открытые стандарты + open-source ядро + BRAIM как оркестратор поверх**.

---

## Схема стека (слои снизу вверх)

```
┌─────────────────────────────────────────────────────────────┐
│                    BRAIM (оркестратор / шина)                  │
│   транзакции · Quality Gate · lifecycle_fork · снапшоты       │
├─────────────────────────────────────────────────────────────┤
│  GUI / веб-просмотр       │  Авторинг                        │
│  That Open (web-ifc)      │  Bonsai (BlenderBIM)              │
│  IFClite (Rust+WASM)      │  FreeCAD NativeIFC               │
├─────────────────────────────────────────────────────────────┤
│  Валидация                │  Связь / замечания               │
│  IfcTester (IDS)          │  BCF (XML + REST API)             │
│  IfcOpenShell API         │  OpenCDE API                     │
├─────────────────────────────────────────────────────────────┤
│  Версионирование          │  Граф / запросы                  │
│  git + ifcmerge           │  Neo4j (Cypher)                  │
│  ifc-commit              │  IfcOpenShell → CSV → Neo4j       │
├─────────────────────────────────────────────────────────────┤
│  Словарь / классификация                                      │
│  bSDD (REST API) · Uniclass · OmniClass · КСИ                │
├─────────────────────────────────────────────────────────────┤
│  Формат данных                                                │
│  IFC (SPF / STEP) · IDS (XML) · BCF (XML/JSON)                │
├─────────────────────────────────────────────────────────────┤
│  Хранение                                                    │
│  Файловая система (git repo) · Neo4j · CDE-сервер            │
└─────────────────────────────────────────────────────────────┘
```

---

## Слой 0: Формат данных

| Технология | Что это | Роль в BRAIM |
|---|---|---|
| **IFC** (ISO 16739) | открытый формат обмена данными о здании | ядро, носитель модели |
| **IDS** v1.0 | спецификация требований к информации (XML) | определение «что должно быть в модели» |
| **BCF** | формат обмена замечаниями (XML/JSON + REST API) | отчёты валидатора, коммуникация |
| **bSDD** | словарь данных buildingSMART (REST API) | единая терминология свойств и классификаций |

**Лицензии:** все четыре — открытые стандарты buildingSMART, бесплатны.

---

## Слой 1: Хранение

| Компонент | Технология | Лицензия | Что хранит |
|---|---|---|---|
| **Git-репозиторий** | git (any) | GPL | IFC-файлы, история, ветки, DAG |
| **Neo4j** | Neo4j Community | GPLv3 | граф сущностей, связей, свойств |
| **CDE-сервер** | любой с поддержкой OpenCDE API | — | контейнеры, статусы, маршруты согласования |

**Neo4j** — графовое хранилище, источник истины для связей. IFC загружается через IfcOpenShell → CSV → Neo4j (рабочий пайплайн, проверенный в исследованиях). [web_15_0_0_18] [web_15_0_0_21]

**Git** — хранилище версий и веток. IFC-файлы лежат в git-репозитории, ifcmerge обрабатывает конфликты слияния. [web_15_0_0_5]

**CDE** — среда общих данных. Не хранит саму модель, а управляет контейнерами, статусами (WIP/SHR/PUB/ARC), маршрутами. В РФ: BIMeister, SAREX, TDLS «Фарватер», Pilot-ICE. [web_15_0_0_12]

---

## Слой 2: Версионирование

| Компонент | Язык | Лицензия | Что делает |
|---|---|---|---|
| **git** | C | GPL | базовый контроль версий, DAG, branch, merge |
| **ifcmerge** | Rust | open-source | трёхстороннее слияние IFC, вызывается как `git mergetool` |
| **ifc-commit** | Python | open-source | декомпозиция IFC по этажам/дисциплинам, вписание provenance в Pset |
| **ifcgit.py** | Python (Blender add-on) | GPL | UI-панель для git-операций в Bonsai |

**ifcmerge** уже поставляется в комплекте с Bonsai. Команда:
```
ifcmerge base.ifc local_fork.ifc remote_fork.ifc result_merged.ifc
```

**ifc-commit** вписывает `CommitHash`, `CommitAuthor`, `CommitBranch` прямо в IFC как `Pset_GitCommit`. Это готовый **provenance** для снапшота. [web_15_0_0_5]

**Связь с BRAIM:**
- `lifecycle_fork` → `git branch` + `ifcmerge`
- Снапшот → `git commit` + `ifc-commit` provenance
- Quality Gate → проверка перед `git merge`

---

## Слой 3: Граф и запросы

| Компонент | Язык | Лицензия | Что делает |
|---|---|---|---|
| **IfcOpenShell** | C++ / Python | LGPL | чтение, запись, парсинг IFC, геометрия через OpenCASCADE |
| **Neo4j + Cypher** | Java | GPLv3 (Community) | графовое хранилище, запросы по связям |
| **ifc2cypher** | Python | open-source | конвертер IFC → Cypher (запросы для Neo4j) |
| **BIM_graph_agent** | Python | MIT | IFC → Neo4j + AI-запросы на естественном языке |

**Пайплайн:** IFC → IfcOpenShell → CSV/JSON → Neo4j. Узлы = сущности IFC, рёбра = связи (IfcRelContainedInSpatialStructure, IfcRelDefinesByProperties, …). [web_15_0_0_21] [web_15_0_0_18]

**Связь с BRAIM:**
- Граф — источник истины (дыра 7)
- Таблицы (ведомости, спецификации) — проекция графа
- Топологические проверки валидатора (дыра 9) — запросы к графу

---

## Слой 4: Валидация

| Компонент | Язык | Лицензия | Что делает |
|---|---|---|---|
| **IfcTester** | Python | LGPL | проверка IFC по IDS, отчёты JSON/HTML |
| **IfcOpenShell IDS** | Python | LGPL | `ids_file.validate(ifc_file)` — API для программной проверки |
| **IDS Audit Tool** | — | open-source | проверка самих IDS-файлов на соответствие схеме |

**Рабочий код:**
```python
import ifcopenshell
import ifctester
import ifctester.reporter

ifc_file = ifcopenshell.open('model.ifc')
ids = ifctester.ids.open('requirements.ids')
ids.validate(ifc_file)
reporter = ifctester.reporter.Html(ids)
reporter.report()
reporter.to_file('report.html')
```
[web_15_1_0_10] [web_15_1_0_9]

**Что проверяет IDS (6 фасетов):**
1. Entity — IFC-класс объекта
2. Attribute — встроенные атрибуты (Name, Description)
3. Property — свойства из Pset
4. Material — материалы
5. Classification — внешние коды
6. PartOf — пространственная иерархия

**Связь с BRAIM:**
- IDS = требования к обмену (exchange requirements)
- IfcTester = ядро валидации, вызывается через шину
- Отчёт → BCF-топики → BRAIM → Quality Gate (Go/No-Go/Hold)

---

## Слой 5: Связь и коммуникация

| Компонент | Формат | Лицензия | Что делает |
|---|---|---|---|
| **BCF API** | REST (JSON) | open standard | обмен замечаниями между системами |
| **BCF XML** | XML | open standard | файловый обмен замечаниями |
| **OpenCDE API** | REST (OpenAPI/Swagger) | open standard | унифицированный интерфейс между разными CDE |

**OpenCDE API** включает:
- Foundation API — авторизация, сессии
- Documents API — загрузка/выгрузка контейнеров
- BCF API — обмен замечаниями
- bSDD API — доступ к словарю данных

[web_15_1_0_15] [web_15_1_0_14]

**Связь с BRAIM:**
- BCF — формат отчётов валидатора
- OpenCDE API — шина между BRAIM и внешними CDE
- bSDD API — справочник свойств при генерации IDS

---

## Слой 6: Авторинг

| Компонент | Платформа | Лицензия | Что делает |
|---|---|---|---|
| **Bonsai** (ex-BlenderBIM) | Blender | GPL | нативный авторинг IFC, git-интеграция, visual diff |
| **FreeCAD NativeIFC** | FreeCAD | LGPL | открытие/редактирование IFC, хранение в .FCStd |

**Bonsai** — единственный инструмент с нативной IFC-записью (не экспорт, а сохранение в IFC как родной формат). Поддерживает:
- Прямое редактирование IFC-классов и свойств
- Git: commit, branch, merge, diff (через ifcgit.py + ifcmerge)
- Visual diff — добавленные/удалённые/изменённые объекты подсвечиваются в 3D
- Provenance через ifc-commit

[web_15_0_0_9] [web_15_0_0_8]

**Native IFC** — ключевая концепция:
1. Не менять ID сущности при редактировании атрибутов
2. Не переиспользовать числовые ID удалённых сущностей
3. Писать сущности в том же формате, что в исходном файле

Это делает IFC-файл дружественным к git: diff минимальный, merge предсказуемый. [web_15_0_0_8]

---

## Слой 7: Веб-просмотр и GUI

| Компонент | Технология | Лицензия | Что делает |
|---|---|---|---|
| **That Open** (ex-IFC.js) | JS + WASM (C++) | MIT/MPL-2.0 | просмотр IFC в браузере, WebGL, без сервера |
| **IFClite** | Rust + WASM | MPL-2.0 | парсинг, просмотр, запросы к IFC в браузере, WebGPU |
| **web-ifc** | C++/WASM/JS | MIT | ядро чтения/записи IFC в браузере на нативной скорости |

**That Open** — модульная open-source экосистема: просмотр IFC в браузере, работает на стороне клиента, без облачной обработки. 15 строк кода — и модель открыта. [web_15_1_0_4]

**IFClite** — Rust-ядро + WebGPU-рендеринг, парсит 169 МБ / 60 284 продуктов за 4.2 секунды. [web_15_1_0_3]

**Связь с BRAIM:**
- Веб-просмотр = «сумрак» для человека (визуальная проекция модели)
- web-ifc / IFClite — движок для браузерного клиента BRAIM
- Visual diff из Bonsai — прототип для веб-просмотра изменений

---

## Слой 8: BRAIM (оркестратор)

BRAIM не входит в стек как компонент — он **сидит поверх стека** и оркестирует:

| Механизм BRAIM | Какие компоненты стека задействует |
|---|---|
| **Транзакция** | OpenCDE API (Documents) + git commit |
| **Quality Gate** | IfcTester (IDS) → BCF-отчёт → решение Go/No-Go/Hold |
| **lifecycle_fork** | git branch + ifcmerge |
| **Снапшот** | git commit + ifc-commit (provenance) |
| **Представление (MVD)** | IDS-спецификация → IfcTester → фильтрация |
| **Веб-просмотр** | That Open / IFClite |
| **Граф** | IfcOpenShell → Neo4j → Cypher |
| **Словарь** | bSDD API |

---

## Стек одной строкой

```
IFC → IfcOpenShell → Neo4j → git + ifcmerge → IfcTester (IDS) → BCF → OpenCDE API → BRAIM → Bonsai / That Open
```

---

## Что открыто / что закрыто в стеке

| Компонент | Статус | Примечание |
|---|---|---|
| Формат данных (IFC/IDS/BCF) | ✅ стандарт | утверждён, v1.0+ |
| Парсинг IFC (IfcOpenShell) | ✅ open-source | LGPL, зрелый |
| Версионирование (git+ifcmerge) | ✅ работает | ifcmerge в комплекте Bonsai |
| Валидация (IfcTester) | ✅ open-source | IDS v1.0 утверждён июнь 2024 |
| Граф (Neo4j) | ✅ open-source | Community Edition — GPLv3 |
| Веб-просмотр (That Open) | ✅ open-source | MIT/MPL |
| Авторинг (Bonsai) | ✅ open-source | GPL, но не в реестре РФ |
| CDE | ⚠️ выбор | РФ: BIMeister, SAREX, Pilot-ICE; open-source альтернативы не в реестре |
| OpenCDE API | ⚠️ ранний | спецификация развивается, Documents API не финализирован |
| BRAIM (оркестратор) | 🔨 строим | шина + Quality Gate + снапшоты |
| Геометрический валидатор | 🔨 строим | топологические + функциональные проверки |
| Формальная схема снапшота | 🔨 строим | JSON Schema для IterationSnapshot |

---

## Референсные реализации для каждого механизма BRAIM

| Механизм BRAIM | Референс | Автор | Статус |
|---|---|---|---|
| lifecycle_fork | ifcmerge + ifcgit.py | Bruno Postle / IfcOpenShell | работает в Bonsai |
| provenance | ifc-commit | IfcOpenShell community | CLI, вписывает Pset_GitCommit |
| visual diff | Bonsai visual diff | IfcOpenShell | первый в индустрии |
| IFC → graph | ifc2cypher / IfcOpenShell → Neo4j | ysangkok / исследователи | рабочий пайплайн |
| IDS validation | IfcTester | IfcOpenShell | IDS v1.0, Python API |
| BCF issue exchange | BCF API + BCF XML | buildingSMART | стандарт, REST + XML |
| CDE interoperability | OpenCDE API | buildingSMART | ранний, развивается |
| Веб-просмотр IFC | web-ifc / That Open | That Open Company | MIT, WASM |
| Native IFC authoring | Bonsai | IfcOpenShell | GPL, единственный |

---

## Лицензионная карта

| Лицензия | Компоненты |
|---|---|
| **GPL** | git, Bonsai, Neo4j Community, ifcgit.py |
| **LGPL** | IfcOpenShell, FreeCAD |
| **MIT / MPL** | web-ifc, That Open Components, IFClite |
| **Open standard** | IFC, IDS, BCF, bSDD, OpenCDE API |
| **Проприетарное** | Neo4j Enterprise (не нужно — Community хватает) |

**Вывод:** весь стек кроме CDE можно собрать из open-source. CDE в РФ — отдельный выбор, но через OpenCDE API BRAIM абстрагируется от конкретного вендора.
