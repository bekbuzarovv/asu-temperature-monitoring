# Мини-АСУ ТП: Мониторинг температуры (Эмуляция ПЛК + Modbus TCP + Grafana)

## Проблема
В учебных условиях нет доступа к промышленному ПЛК и дорогостоящей SCADA-системе. Проект решает эту проблему, имитируя полный контур сбора данных: от «датчика» до дашборда диспетчера.

## Скриншот
![Дашборд Grafana](dashboard.png) 

## Стек технологий
*   Python 3.10 (pymodbus, asyncio, sqlite3)
*   Протокол Modbus TCP
*   База данных SQLite
*   Визуализация Grafana (плагин frser-sqlite-datasource)

## Архитектура
`[Эмулятор ПЛК (Python, Modbus TCP сервер)]` → `[Сборщик (Python, Modbus клиент)]` → `[SQLite]` → `[Grafana]`

## Как запустить
1. Установите Python 3.10+ и создайте виртуальное окружение.
2. Установите зависимости: `pip install "pymodbus>=3.8,<3.10"`
3. Запустите эмулятор ПЛК: `python plc_emulator.py`
4. В новом окне запустите сборщик: `python collector.py`
5. Установите Grafana, плагин `frser-sqlite-datasource`, подключите файл `temperature.db` как источник данных.
6. Создайте дашборд со следующим SQL-запросом:
   ```sql
   SELECT
     strftime('%s', timestamp, 'utc') AS time,
     temperature AS value
   FROM readings
   ORDER BY timestamp