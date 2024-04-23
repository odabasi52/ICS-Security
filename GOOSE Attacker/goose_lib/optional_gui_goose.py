import scapy.all as scp
import time
from uuid import getnode

class GOOSE:    
    goose_msg = {
        "appId"                 : 1,
        "gocbRef"               : b"GEDeviceF650/LLN0$GO$gcb01",
        "timeAllowedToLive"     : 4000,                          
        "datSet"                : b"GEDeviceF650/LLN0$GOOSE1",
        "goId"                  : b"GEDevGOOSE1",               
        "t"                     : time.time(),
        "stNum"                 : 1,
        "sqNum"                 : 1,
        "simulation"            : False,
        "confRev"               : 1,
        "ndsCom"                : False,
        "numDatSetEntries"      : 0,
        "allData"               : b""
    }

    def __init__(self):
        self.src_mac = self.get_src_mac()
        self.dest_mac = "ff:ff:ff:ff:ff:ff"

    def send(self):
        self.convert_values_to_bytes()
        scp.sendp(self.create_pack())

    def convert_values_to_bytes(self):
        self.appId = b"\x00" + self.goose_msg["appId"].to_bytes(length=1, byteorder="big")
        self.gocbRef = b"\x00\x91\x00\x00\x00\x00a\x81\x86\x80" + bytes([len(self.goose_msg["gocbRef"])]) + self.goose_msg["gocbRef"]
        self.timeAllowedToLive = b"\x81\x03\x00" + self.goose_msg["timeAllowedToLive"].to_bytes(length=2, byteorder="big")
        self.datSet = b"\x82" + bytes([len(self.goose_msg["datSet"])]) + self.goose_msg["datSet"]
        self.goId = b"\x83" + bytes([len(self.goose_msg["goId"])])+ self.goose_msg["goId"]
        self.t =  b"\x84\x08" +  int(self.goose_msg["t"]).to_bytes(length=4, byteorder="big") + b"\x00\x00\x00\x00"
        self.stNum = b"\x85\x01" + self.goose_msg["stNum"].to_bytes(length=1, byteorder="big")
        self.sqNum = b"\x86\x01" + self.goose_msg["sqNum"].to_bytes(length=1, byteorder="big")
        self.simulation = b"\x87\x01" + self.goose_msg["simulation"].to_bytes(length=1, byteorder="big")
        self.confRev = b"\x88\x01" + self.goose_msg["confRev"].to_bytes(length=1, byteorder="big")
        self.ndsCom = b"\x89\x01" + self.goose_msg["ndsCom"].to_bytes(length=1, byteorder="big")
        self.numDatSetEntries = b"\x8a\x01" + self.goose_msg["numDatSetEntries"].to_bytes(length=1, byteorder="big")
        self.allData = self.goose_msg["allData"]
        if self.allData != b"":
            self.allData = b"\xab " + self.goose_msg["allData"]

    def generate_msg(self):
        goose = self.appId + self.gocbRef + self.timeAllowedToLive + self.datSet + self.goId + self.t + self.stNum + self.sqNum + self.simulation + self.confRev + self.ndsCom + self.numDatSetEntries
        return (goose + self.allData)
    
    def create_pack(self):
        self.convert_values_to_bytes()
        ether_layer = scp.Ether(src=self.src_mac, dst=self.dest_mac, type=0x88b8)
        data = scp.Raw(load=self.generate_msg())
        packet = ether_layer/data
        return (packet)

    def get_src_mac(self):
        return (':'.join(['{:02x}'.format((getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1]))

