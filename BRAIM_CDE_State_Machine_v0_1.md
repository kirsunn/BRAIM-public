# BRAIM CDE State Machine

## Статус

- Версия: `0.1.0`
- Дата: 2026-09-28
- CDE: `SHARED`
- Назначение: управляемые состояния документа, схемы, модели или утверждения

## Состояния

```text
WIP
SHARED
PUBLISHED
ARCHIVE
```

Дополнительные состояния review/release:

```text
DRAFT | IN_REVIEW | CHANGES_REQUESTED | APPROVED
RELEASED | RETIRED | BLOCKED | OUTDATED
```

## Разделение статусов

```yaml
cde_state: WIP|SHARED|PUBLISHED|ARCHIVE
review_state: DRAFT|IN_REVIEW|CHANGES_REQUESTED|APPROVED|REJECTED
release_state: NOT_RELEASED|RELEASE_CANDIDATE|RELEASED|RETIRED
visibility: PRIVATE|TEAM|CLIENT|PUBLIC
```

## Допустимые переходы

```text
WIP → SHARED
SHARED → WIP
SHARED → PUBLISHED
PUBLISHED → ARCHIVE
PUBLISHED_PRIVATE → PUBLISHED_PUBLIC
PUBLISHED → OUTDATED
OUTDATED → SHARED
```

## Условия публичной публикации

```text
public_allowed == true
security scan pass
secrets scan pass
license check pass
private data absent
full protected normative copies absent
external links reviewed
```

Публичная копия должна содержать только файлы, прошедшие манифест публикации. `PUBLISHED` не означает автоматически разрешённую публичную публикацию.
