# BRAIM Attribute Registry

## Статус

- Версия: `0.1.0`
- Дата: 2026-09-28
- CDE: `SHARED`
- Назначение: единый реестр типизированных атрибутов BRAIM

Атрибут — это типизированное значение с владельцем, источником истины, статусом, единицей, ограничениями и правилами производности.

```text
Attribute = id + type + value + unit + owner + source + constraints + status
```

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
