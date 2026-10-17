# BRAIM Pset v0.1.1 — Knowledge Core

Ядро базы знаний BRAIM (P0-26). Конвергенция всех слоёв в одну структуру.

## Содержимое
- `knowledge_core_v0.1.1.json` (80 КБ) — основное ядро: документы, edges, атрибуты (17), defaults (10), templates (26), rules (75), formulas (1), tables (1), mapping (10)
- `braim_pset_v0.1_bsdd.json` — bSDD import model, готов к загрузке в bSDD custom dictionary через REST API
- `braim_knowledge_core_v0.1.1.ids` — IDS 1.0 (75 specifications) сгенерирован из rules
- `templates_v0.1.yaml` — типовые шаблоны требований (НЕ копия Минстроя, структура наша)
- `knowledge_core_v0.1.json` (80 КБ) — предыдущая версия

## Что **НЕ** копируется
- Тексты Минстроя/ГОСТ/СП (L0-N no_full_copies)
- Готовые правила «под ключ» (NOT-DOING §11)
- Чужие классификаторы в виде данных (mapping — только индекс наших templates)

## Доктрины
- L0-N no_full_copies
- G-1 редакции привязываются к lifecycle-контексту
- G-2 мета-валидация политик
- G-3 coverage statement
- G-5 actor_id в provenance
- G-6 клиентские модели не в облако; норм. тексты — допустимо
- G-7 registry-ready без обязательств
- NOT-DOING §12: автоповышение только человек

## Использование

```python
import json
core = json.load(open('knowledge_core_v0.1.1.json', encoding='utf-8'))
# Rules: список нормализованных правил
rules = core['rules']
# Defaults: атрибут → принятое значение
defaults = {d['attribute']: d for d in core['defaults']}
# Graph: document references
edges = core['graph']['edges']
```

## Генерация IDS

```bash
python tools/normpipe/normpipe.py gen-ids <rules.json> <output.ids>
```

## Следующие шаги (P0-26 → v0.2)

- Расширить `defaults` (4 → 10) ✅ v0.1.1
- Расширить `attributes` (10 → 16) ✅ v0.1.1
- Расширить `mapping` (2 → 10) ✅ v0.1.1
- Генерация IDS из rules ✅ v0.1.1
- Добавить формулы/таблицы (за рамками 1 СП) — Phase 2
- F-08 найти заказ АГР — приоритет
