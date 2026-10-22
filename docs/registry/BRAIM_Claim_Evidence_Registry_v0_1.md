# BRAIM Claim and Evidence Registry

## Статус

- Версия: `0.1.0`
- Дата: 2026-09-28
- CDE: `SHARED`
- Назначение: хранить источники, факты, интерпретации, AI-выводы, расчёты и решения пользователей

BRAIM не смешивает первичный источник, факт извлечения, интерпретацию, AI-гипотезу, проектное решение и верифицированное правило.

## Типы утверждений

```text
SOURCE_FACT | EXTRACTED_FACT | MEASURED_FACT | CALCULATED_RESULT
AI_INTERPRETATION | PROJECT_DECISION | VALIDATED_CLAIM | CONFLICTING_CLAIM
```

## Статусы

```text
OBSERVED | EXTRACTED | INTERPRETED | PROPOSED | SUPPORTED
VERIFIED | APPROVED | REJECTED | OUTDATED | CONFLICTED
```

## Правила

1. AI-вывод никогда не маскируется под цитату нормы.
2. Любое утверждение, влияющее на генератор, имеет `claim_id`.
3. Утверждение, влияющее на валидатор, имеет проверенный источник или утверждённое решение.
4. Конфликтующие источники сохраняются оба.
5. Уверенность не заменяет верификацию.
6. Публичная публикация разрешена только для утверждений с `public_allowed: true`.
7. Изменение источника создаёт impact analysis.
