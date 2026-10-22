# BRAIM Attribute Registry

## Статус

- Версия: `0.1.1`
- Дата: 2026-10-15
- CDE: `SHARED`
- Назначение: единый реестр типизированных атрибутов BRAIM
- 0.1.1: добавлен словарный слой — `bsdd_property_ref` (ADR-015, bSDD / ISO 12006-3, ISO 23386)

Атрибут — это типизированное значение с владельцем, источником истины, статусом, единицей, ограничениями и правилами производности.

```text
Attribute = id + type + value + unit + owner + source + constraints + status
          + [bsdd_property_ref]
```

`bsdd_property_ref` — URI/GUID определения свойства в bSDD (buildingSMART Data Dictionary) или в локальном bSDD-совместимом реестре (ADR-015, DICT-02/03). Обязателен, когда словарное определение существует; проектные свойства без словарного определения регистрируются локально с обязательным provenance.

## Типы данных

```text
string | integer | decimal | boolean | enum | reference
list | set | map | quantity.length | quantity.area
quantity.volume | quantity.angle | quantity.time
geometry.point | geometry.line | geometry.polygon | geometry.solid
modularity.constraint
```

## Статусы значения

```text
UNKNOWN | ASSUMED | USER_DEFINED | SOURCE_DEFINED | AI_PROPOSED
DERIVED | VERIFIED | APPROVED | OUTDATED | CONFLICT
NOT_APPLICABLE | NEEDS_REVIEW
```

## Правила

1. Одинаковый `attribute_id` не должен иметь разные смыслы.
2. Фактическое значение не заменяет требуемое.
3. `null` означает неизвестность, а не ноль.
4. Единица измерения обязательна для quantity-типов.
5. Нормативное значение должно иметь источник.
6. Производный атрибут должен иметь формулу или список источников.
7. У каждого атрибута один владелец и список потребителей.
8. Изменение владельца истины создаёт impact analysis.
9. `AI_PROPOSED` не становится `APPROVED` автоматически.
10. Публичная версия не содержит приватных значений.
11. Если словарное определение свойства существует (bSDD или локальный bSDD-совместимый реестр, ADR-015), атрибут ссылается на него через `bsdd_property_ref`. Локальное переопределение типа/единицы при наличии словарного определения — расхождение (finding `DICT.DEFINITION_CONFLICT`, severity — в policy pack).
12. Runtime-валидация не обращается к внешнему сервису словаря: используемые редакции словарей пиннятся как артефакты (edition + digest, ADR-015 DICT-04).
