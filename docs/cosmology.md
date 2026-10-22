# BAIM Cosmology

Version: 0.2.0-draft
Date: 2026-10-22
Status: Draft — top-level architecture, ArchiMate notation

## 1. Назначение
Фиксирует, кто где живёт в системе BAIM и как взаимодействует.
Верхний уровень — ArchiMate. Декомпозиция — BPMN, UML, Property Graph.

## 2. ArchiMate: верхний уровень

### Business Layer (кто и зачем)
- Actor: human.plt (проектировщик, эксперт, заказчик)
- Role: «Утверждающий» — принимает решения по замечаниям
- Value: «Прозрачная проверка здания по нормативам»
- Process: «Итеративная проверка и согласование»

### Application Layer (что и как)
- Application Component: brAVium.pla.loc — исполняет проверки
- Application Component: brAVium.pla.pub — публикует знания
- Application Service: «Проверка по нормативам»
- Application Component: SPU — модуль знаний (norma, mudro)
- Application Component: ZERO-BUS — нейтральная шина сообщений

### Technology Layer (на чём)
- Node: Graph DB (Neo4j)
- Node: Message Bus (Kafka/RabbitMQ)
- Artifact: IFC5 file / IFC-хранилище
- Artifact: Ruleset Package

## 3. Иерархия и адресация

GAL → STA → PLA → [SPU]
- GAL — контейнер звёзд, глобальные политики
- STA — домен/кластер
- PLA — рабочая среда, объекты
- SPU — модуль знаний, опционален в пути

path = "GAL01.STA03.PLA07[.SPU02]"

## 4. Ядра brAVium (1:1 с сущностью)

| Сущность | Ядро | Роль |
|---|---|---|
| GAL | brAVium.gal | политики, маршруты, квоты |
| STA | brAVium.sta | домены, доступ, задачи |
| PLA | brAVium.pla.pub / .loc | публикация знаний / исполнение проверок |
| SPU | brAVium.spu | хранит и отдаёт знания |

## 5. Объекты на планете

- build.plt — аватар здания, ссылается на IFC5 по GUID
- road.plt — инфраструктурный объект
- human.plt — участник принятия решений

## 6. ZERO-BUS

Нейтральная шина сообщений между ядрами, SPU и внешними системами.
Не хранит бизнес-логику. Функции: маршрутизация, очередь,
метаданные, версионирование, трейсинг.

## 7. Графовая модель (Property Graph)

Узлы: :GAL :STA :PLA :SPU :Build :Road :Human :Core :Norma :CheckResult
Связи: :CONTAINS :HAS_CORE :USES :REQUIRES_APPROVAL :APPROVES :FIXED_BY
Свойства: code, path, coclass, ifc_guid, iteration, decision_log

## 8. Цикл проверок

brAVium.pla.loc → SPU (нормы) → проверка build.plt
→ несоответствие → human.plt утверждает
→ CheckResult в графе → повторная проверка

## 9. Разрешение конфликтов

Приоритет: brAVium.pla > brAVium.sta > brAVium.gal
Конфликт SPU → эскалация к human.plt

## 10. Связь с IFC5

BAV (build.plt) ссылается на IFC5-сущность по GUID.
Геометрия и свойства — в IFC5, граф — индекс знаний и связей.

## 11. Связь с PROJECT_CONTEXT

PLA ≈ BRAVIM Planet / BAV Local Core
SPU ≈ источник Ruleset Packages
ZERO-BUS ≈ транспорт между ними
human.plt ≈ Human-in-the-loop
