import asyncio
import random
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.server import StartAsyncTcpServer

# 1. Создаём хранилище (datastore) с 10 holding-регистрами.
# Начальное значение в регистре 0 — 250 (это 25.0 °C, так как мы храним температуру * 10).
# zero_mode=True означает, что адрес 0 в запросе клиента будет соответствовать первому элементу списка.
store = ModbusSlaveContext(
    hr=ModbusSequentialDataBlock(0, [250] * 10),
    #zero_mode=True
)
context = ModbusServerContext(slaves=store, single=True)

# 2. Фоновая задача, которая имитирует изменение температуры.
async def update_temperature(context):
    """Каждые 2 секунды меняет значение в регистре 0, имитируя датчик."""
    while True:
        # Генерируем температуру от 20.0 до 30.0 °C (значение * 10 = 200..300)
        new_temp = random.randint(200, 300)
        # Функция 3 = holding registers. Записываем в регистр 0 новое значение.
        context[0x00].setValues(3, 0, [new_temp])
        print(f"[PLC] Температура обновлена: {new_temp / 10.0} °C")
        await asyncio.sleep(2)

# 3. Запуск сервера и фоновой задачи
async def main():
    print("Эмулятор ПЛК запущен на 127.0.0.1:5020")
    # Запускаем фоновую задачу по изменению температуры
    asyncio.create_task(update_temperature(context))
    # Запускаем Modbus TCP сервер
    await StartAsyncTcpServer(
        context=context,
        address=("127.0.0.1", 5020)
    )

if __name__ == "__main__":
    asyncio.run(main())
