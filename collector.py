import time
import sqlite3
from datetime import datetime
from pymodbus.client import ModbusTcpClient

# 1. База данных SQLite
conn = sqlite3.connect('temperature.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        temperature REAL NOT NULL
    )
''')
conn.commit()

# 2. Подключаемся к эмулятору ПЛК
client = ModbusTcpClient('127.0.0.1', port=5020)
if not client.connect():
    print("Не удалось подключиться к эмулятору ПЛК. Убедитесь, что plc_emulator.py запущен.")
    raise SystemExit(1)

print("Сборщик данных запущен. Нажмите Ctrl+C для остановки.")

try:
    while True:
        rr = client.read_holding_registers(address=0, count=1, slave=0x00)
        if not rr.isError():
            temp = rr.registers[0] / 10.0
            now = datetime.now().isoformat()
            cursor.execute(
                "INSERT INTO readings (timestamp, temperature) VALUES (?, ?)",
                (now, temp)
            )
            conn.commit()
            print(f"[{now}] Записано: {temp} °C")
        else:
            print(f"Ошибка чтения: {rr}")
        time.sleep(2)
except KeyboardInterrupt:
    print("\nОстановка сбора данных.")
finally:
    client.close()
    conn.close()
