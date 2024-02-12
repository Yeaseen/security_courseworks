# generate_traces_with_timestamp.py
#!/usr/bin/env python3

import sys
import time
from pymodbus.client import ModbusTcpClient as ModbusClient
from pymodbus.exceptions import ConnectionException

ip = sys.argv[1]
duration = int(sys.argv[2])  # Duration in seconds for which the traces will be generated
sample_time = 0.5

client = ModbusClient(ip, port=502)
client.connect()

with open("traces.txt", "w") as f:
    start_time = time.time()
    while time.time() - start_time < duration:
        rr = client.read_holding_registers(1, 16)
        elapsed_time = time.time() - start_time
        f.write(str(elapsed_time) + "," + ",".join(map(str, rr.registers)) + "\n")
        time.sleep(sample_time)