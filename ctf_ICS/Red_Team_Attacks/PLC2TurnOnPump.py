#!/usr/bin/env python3

import sys
import time
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.exceptions import ConnectionException

if len(sys.argv) > 2:
    ip = sys.argv[1]
else:
    ip = "0.0.0.0"

client = ModbusClient(ip, port=502)
client.connect()
while True:
    client.write_coil(4, True) # Turn on pump
   
