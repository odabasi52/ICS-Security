#!/usr/bin/env python3
from modbus import MODBUS

def menu():
    print("MORE OPTIONS WILL BE ADD\n-------------------------------------")
    print("[1] Read Registers\n[2] Write Single Register\n[3] Read Coils\n[4] Read Discrete Inputs\n[5] Read Input Registers\n[6] Exit\n-------------------------------------")
    x = input("Your Choise: ")
    while not (x == "1" or x == "2" or x == "3" or x=="4" or x=="5" or x=="6"):
        x = input("Please enter valid choise: ")
    return x

def main():
    choise = menu()
    client = MODBUS()
    client.create_client()

    match choise:
        case "1":
            client.read_registers()
        case "2":
            client.write_single_register()
        case "3":
        	client.read_coils()
        case "4":
            client.read_discrete_inputs()
        case "5":
            client.read_input_registers()
        case "6":
            pass
if __name__ == "__main__":
    main()