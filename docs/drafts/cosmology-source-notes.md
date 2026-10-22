# Cosmology — Source Notes (draft)

Date: 2026-10-22
Status: Draft — raw source material for future decomposition
Purpose: сохранить исходные наработки, из которых собран cosmology.md

## 1. Философия (в духе Huawei) — справочно, не часть архитектуры

- Клиентоориентированность: приоритеты и набор проверок настраиваются под заказчика; human.plt — ключевой узел принятия решений; обратная связь превращается в новые правила и фасеты coclass.
- Упорство: история проверок как цепочка CheckResult; инкрементальные проверки только изменённых частей; устойчивость ядер к сбоям.
- Открытость: SPU — модульные источники знаний; ZERO-BUS — нейтральный транспорт; coclass — общий язык фасетов.
- Фокус: жёсткая иерархия GAL→STA→PLA→SPU, 3-буквенные коды, постепенное расширение.

## 2. Стандарт именования: 3-буквенные коды

| Сущность | Код | Префикс | Назначение |
|---|---|---|---|
| Галактика | GAL | AVGALAXY | Верхний уровень, контейнер звёзд |
| Звезда | STA | AVSTAR | Домен/кластер, контейнер планет |
| Планета | PLA | AVPLANET | Контейнер объектов среды |
| Модуль знаний | SPU | AVSPUTNIK | Логический модуль знаний по отраслям |

SPU — не космический объект, а модуль знаний, привязанный к домену (STA/PLA).

## 3. Ядра brAVium

У каждой сущности верхнего уровня — ровно одно ядро (1:1):

| Родитель | Ядро | Назначение |
|---|---|---|
| GAL | brAVium.gal | глобальные политики, маршруты, квоты |
| STA | brAVium.sta | домены, доступ, распределение задач |
| PLA | brAVium.pla | рабочий центр: проверки, объекты |
| SPU | brAVium.spu | хранит и отдаёт знания (norma, mudro) |

Примечание архитектора: в cosmology.md v0.2.0 ядро PLA разделено на brAVium.pla.pub (публикация знаний) и brAVium.pla.loc (исполнение проверок), чтобы не дублировать BRAVIM Planet / BAV Local Core из PROJECT_CONTEXT.

## 4. Объекты на планете

| Объект | Префикс | Назначение |
|---|---|---|
| Здание | build.plt | Аватар здания, ссылается на IFC5 по GUID |
| Дорога | road.plt | Инфраструктурный объект |
| Человек | human.plt | Аватар живого организма, участвует в решениях |

## 5. Путь (path)

path = "GAL01.STA03.PLA07[.SPU02]"
SPU в пути опционален.

## 6. Графовая модель (Neo4j)

Узлы:
```cypher
(:GAL {code: "GAL01", name: "MilkyWay"})
(:STA {code: "STA03", name: "Sol"})
(:PLA {code: "PLA07", name: "Earth"})
(:SPU {code: "SPU02", domain: "medicine"})
(:Build {prefix: "build.plt", ifc_template: "ResidentialBuilding_v2"})
(:Road {prefix: "road.plt"})
(:Human {prefix: "human.plt"})
(:Core {type: "brAVium", level: "gal/sta/pla/spu"})
```

Связи:
```cypher
(GAL)-[:CONTAINS]->(STA)
(STA)-[:CONTAINS]->(PLA)
(PLA)-[:CONTAINS]->(Build|Road|Human)
(PLA)-[:HAS_CORE]->(Core)
(SPU)-[:HAS_CORE]->(Core)
(Core {type: "brAVium.pla"})-[:USES]->(SPU)
(Human)-[:APPROVES]->(Build)
(Human)-[:REQUIRES_APPROVAL]->(Build)
```

## 7. Цикл проверок

1. brAVium.pla запускает проверку build.plt
2. Ядро обращается к SPU за нормативами (norma) и экспертными правилами (mudro)
3. Результаты — узлы CheckResult {iteration, status, rule}
4. При несоответствии — (Human)-[:REQUIRES_APPROVAL]->(Build)
5. human.plt принимает решение, фиксируется в графе
6. Повторная проверка

## 8. Нотации для декомпозиции

- ArchiMate — верхний уровень: ценность, роли, сервисы, мотивация
- BPMN — цикл проверок: пулы brAVium / Human / SPU, шлюзы XOR, цикл до approved
- UML/PlantUML — классы, пакеты, sequence-диаграммы; Build ← AvatarBase, brAVium ← CoreBase
- Property Graph / Cypher — исполняемая модель

## 9. Инструменты

- draw.io / Miro — схемы иерархии и связей, доска ревью
- Neo4j Desktop / Browser — графовая модель, Cypher
- ArchiCAD + IFC Viewer (Solibri, BIMvision) — BIM-контекст; в графе хранить ссылки (GUID, IfcGlobalId), не дублировать геометрию
- Lucidchart / PlantUML — ER и словарь сущностей
- Python + NetworkX — прототип логики ядра и итераций
- Notion/Confluence + Git — реестр, статусы, машиночитаемые артефакты

## 10. План быстрого старта (3–5 дней)

1. draw.io: схема GAL→STA→PLA→SPU, ядра, шина, человек; Markdown-словарь сущностей
2. Neo4j: минимальный граф, 2–3 Cypher-запроса
3. Python + NetworkX: генерация тестовых данных, имитация цикла проверки
4. Notion: реестр проверок, статусы, ссылки на СП/ГОСТ
5. Демо-отчёт для клиента на основе графа и логов
