#!/usr/bin/env python3
from modbus import MODBUS

def menu():
    print("MORE OPTIONS WILL BE ADD\n-------------------------------------")
    print("[1] Read Registers\n[2] Write Single Register")
    x = input("Your Choise: ")
    while not (x == "1" or x == "2"):
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
            pass

if __name__ == "__main__":
    main()