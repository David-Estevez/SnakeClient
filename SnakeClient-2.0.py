"""
	SnakeClient
	-------------------------------------------------
	Control modular robots using the SnakeServer protocol

"""

__author__ = 'David Estevez-Fernandez'
__license__ = 'GPLv3'

# Imports
# ------------------------------------------------------------------------------
from SnakeClientCore import Core
import GUI
import time, sys

# Main function
# ------------------------------------------------------------------------------
def main():
	if len(sys.argv) == 3:
		portName = sys.argv[1]
		baudRate = int(sys.argv[2])
	else:
		portName = '/dev/ttyUSB0'
		baudRate = 9600
	
	core = Core()
	print '[+] Testing command generation...'
	print core.commandWave(60,  0,  0, core.X_AXIS)
	print core.commandWave( 0, 60,  0, core.ALL_AXES)

	print '[+] Testing connection...'
	core.startup( portName, baudRate)


	core.sendPeriod( 4000) 
	time.sleep(0.05)
	core.sendWave(60, 0, 0, core.X_AXIS) 
	
	

if __name__ == '__main__':
	main()
