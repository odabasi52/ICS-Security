import sys
import time
from pymodbus.client.tcp import ModbusTcpClient as ModbusClient
from pymodbus.exceptions import ConnectionException

class MODBUS:
    def __init__(self):
        self.target_ip = None
        self.client = None

    def create_client(self):
        self.target_ip = input("Target IP: ")
        self.client = ModbusClient(self.target_ip, port=502)
        try:
            self.client.connect()
        except ConnectionException:
            print(f"Could not connect to Modbus port on {self.target_ip}")
            sys.exit()

    def read_registers(self) -> 3:
        while True:
            try:
                rr = self.client.read_holding_registers(0, 100)
                for i, r in enumerate(rr.registers):
                    if r != 0:
                        print(f"({i}, {r})")
                print()
                time.sleep(0.2)
            except ConnectionException:
                print(f"Could not connect to Modbus port on {self.target_ip}")
                sys.exit()

    def write_single_register(self) -> 6:
        reg = 3
        val = 1
        try:
            reg = int(input("Registiry [0 - 100]: "))
            val = int(input("Value to be set: "))
            
        except:
            print("Enter valid input next time")
            sys.exit()
        
        while True:
            try:
                self.client.write_register(reg, val)
            except ConnectionException:
                print(f"Could not connect to Modbus port on {self.target_ip}")
                sys.exit()