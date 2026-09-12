import asyncio
from machine import Pin, UART

from constants import GeneralConstants
from subsystems import chassis

uart = UART(
    0, 
    baudrate=GeneralConstants.UART.BAUD_RATE, 
    tx=Pin(GeneralConstants.UART.TX_PIN), 
    rx=Pin(GeneralConstants.UART.RX_PIN)
)


class Transmitter:
    def __init__(self, uart: UART, m_chassis: chassis.Chassis):
        self.uart = uart
        self.chassis = m_chassis

    async def transmit_sensors(self):
        while True:
            print("67")
            await asyncio.sleep_ms(5)

    async def receive_commands(self):
        while True:
            print("76")
            # if self.uart.any():
            #     pass
            await asyncio.sleep_ms(5)

async def main():
    transmitter = Transmitter(uart, chassis.Chassis())
    receive_task = asyncio.create_task(transmitter.receive_commands())
    transmit_task = asyncio.create_task(transmitter.transmit_sensors())

    try:
        await asyncio.gather(receive_task, transmit_task)
    finally:
        receive_task.cancel()
        transmit_task.cancel()
        await asyncio.gather(receive_task, transmit_task, return_exceptions=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted by user")
        pass
