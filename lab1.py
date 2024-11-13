import asyncio
import time
import psycopg2

from pyModbusTCP.client import ModbusClient
from pyModbusTCP.utils import decode_ieee, word_list_to_long

SERVER_1_PORT = 502
SERVER_2_PORT = 503

lock = asyncio.Lock()

conn = psycopg2.connect(dbname="postgres", user="postgres", password="12345678", host="127.0.0.1")
conn.autocommit = True
cursor = conn.cursor()


async def read_client1():
    client1 = ModbusClient(host='localhost', port=SERVER_1_PORT)

    while True:
        regs = client1.read_holding_registers(0, 2)

        if regs:
            regs_value = [decode_ieee(f) for f in word_list_to_long(regs)][0]
            print('Server 1, reg1:', regs_value)

            #cursor.execute("INSERT INTO modbus (server_num, reg_addr, value) VALUES (%s, %s, %s)",
            #                   (1, 0, regs_value))

        else:
            print('unable to read registers')

        await asyncio.sleep(0.1)


async def read_client2():
    client2 = ModbusClient(host='localhost', port=SERVER_2_PORT)

    while True:
        regs = client2.read_holding_registers(0, 2)

        if regs:
            regs_value = [decode_ieee(f) for f in word_list_to_long(regs)][0]
            print('Server 2, reg1:', regs_value)

            #cursor.execute("INSERT INTO modbus (server_num, reg_addr, value) VALUES (%s, %s, %s)",
            #                   (2, 0, regs_value))

        else:
            print('unable to read registers')

        await asyncio.sleep(0.1)


async def main():
    await asyncio.gather(read_client1(), read_client2())


if __name__ == '__main__':
    try:
        asyncio.run(main())

    except KeyboardInterrupt as e:
        print("Exiting...")
        cursor.close()
        conn.close()
