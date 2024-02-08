import sys
import time
from pymodbus.client.tcp import ModbusTcpClient as ModbusClient
from pymodbus.exceptions import ConnectionException

class MODBUS:
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
                    if not r==0:
                        print(f"{i}-{r}",end=", ")
                #print(rr.registers)
                time.sleep(0.1)
                print()
            except ConnectionException:
                print(f"Could not connect to Modbus port on {self.target_ip}")
                sys.exit()
    def read_coils(self) -> 1:
        while True:
            try:
        # read 10 bits (= coils) at address 0, store result in coils list
                coils_l = self.client.read_coils(0, 256)

                # if success display registers
                if coils_l:
                    for i,coil in enumerate(coils_l.bits):
                        if coil==True:
                            print(i,end=', ')

                    #print('coil ad #0 to 9: %s' % coils_l.bits)
                else:
                    print('unable to read coils')
                # sleep 2s before next polling
                time.sleep(0.1)
                print()
            except ConnectionException:
                print(f"Could not connect to Modbus port on {self.target_ip}")
                sys.exit()
    
    def read_discrete_inputs(self):
        while True:
            try:
                result = self.client.read_discrete_inputs(0, 256)
                if result.isError():
                    print('Unable to read discrete inputs')
                else:
                    for i, r in enumerate(result.bits):
                        if r==True:
                            print(f"{i}-1",end=", ")
                    #print('Discrete Inputs: %s' % result.bits)
                time.sleep(0.1)
                print()
            except ConnectionException:
                print(f"Could not connect to Modbus port on {self.target_ip}")
                sys.exit()

    def read_input_registers(self):
        while True:
            try:
                result = self.client.read_input_registers(1, 100)
                #if result.isError():
                    #print('Unable to read input registers')
                #else:
                for i, r in enumerate(result.registers):
                #if r==True:
                    print(f"{i}-{r}",end=", ")
                time.sleep(0.1)
                print()
                    #print('Input Registers: %s' % result.registers)
            except ConnectionException:
                print(f"Could not connect to Modbus port on {self.target_ip}")
                sys.exit()