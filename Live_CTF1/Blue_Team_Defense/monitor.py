#!/usr/bin/env python3
from pymodbus.constants import Endian
from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.exceptions import ConnectionException
import time
import random
import sys

# Connect to OpenPLC
client = ModbusTcpClient("localhost", port=502)
client.connect()

minRed = 20
desiredDistanceFill = 7.0

#plc_num = sys.argv[1]

while True:
	# reading input registers (colorSensor and RangeSensor)
	#rr_input = client.read_input_registers(0, 4) # %IW0 to %IW3
	#if not rr_input.isError():
	#	print("Input Registers:", rr_input.registers)
	#else:
	#	print(f"Error reading input Registers: {rr_input}")
			
	# reading coils (pump, doser_red, doser_blue, treatmentComplete)
	doser_response = client.read_coils(6,2) # %QX0.0 to %QX0.7
	if not doser_response.isError():
		print("Red doser:", doser_response.bits[0])
		print("Blue doser", doser_response.bits[1])
	else:
		print(f"Error reading Coils: {doser_response}")
	
	pump = client.read_coils(4) # %QX0.0 to %QX0.7
	if not pump.isError():
		print("Pump:", pump.bits[0])
	else:
		print(f"Error reading Coils: {pump}")
		
	treatmentCom = client.read_coils(0,1) # %QX0.0 to %QX0.7
	if not treatmentCom.isError():
		print("TreatmentComplete:", treatmentCom.bits[0])
	else:
		print(f"Error reading Coils: {treatmentCom}")
		

	rr_stage = client.read_holding_registers(4) # %QW4
	if not rr_stage.isError():	
		print("Stage:", rr_stage.registers[0])
	else:
		print(f"Error reading stage: {rr_stage}")
	rr_holding = client.read_holding_registers(0, 4) # %QW0-3
	if not rr_holding.isError():	
		print("ColorSensorRed, Green, Blue, RangeSensor:", rr_holding.registers)
	else:
		print(f"Error reading stage: {rr_holding}")
		
	
	doseTimerDone = client.read_coils(12,1) # %QX0.0 to %QX0.7
	if not doseTimerDone.isError():
		print("doserTimerDone:", doseTimerDone.bits[0])
	else:
		print(f"Error reading Coils: {doseTimerDone}")
	
		
	if rr_stage.registers[0] == 0:
		print()
		
	elif rr_stage.registers[0] == 1:
		if pump.bits[0] == True: 
			print("attack detected at Pump at Stage 1")
		
	elif rr_stage.registers[0] == 2:
		if doseTimerDone.bits[0] == True and doser_response.bits[0] != False:
			print("attack detected at DoserRed at Stage 2")
	elif rr_stage.registers[0] == 3:
		if doseTimerDone.bits[0] == True and doser_response.bits[1] != False:
			print("attack detected at DoserBlue at Stage 3")
	
	elif rr_stage.registers[0] == 5:
		if pump.bits[0] == True or doseTimerDone.bits[0] == True or doser_response.bits[0] == True or doser_response.bits[1] == True or treatmentCom.bits[0] == False:
			print("attack detected at Stage 5")
			
	else:
		print()
	
	
		
	print("------------------------------")
			
	time.sleep(1)



#monitor PLC_2 when argv is 2





#except KeyboardInterrupt:
#    pass  # Exit the loop on Ctrl-C


client.close()
