"""
	SnakeClient
	-------------------------------------------------
	Control modular robots using the SnakeServer protocol

"""

__author__ = 'David Estevez-Fernandez'
__license__ = 'GPLv3'

# Imports
# ------------------------------------------------------------------------------
import serial
import time

# Define constants:
# ------------------------------------------------------------------------------
X_AXIS = 0
Y_AXIS = 1
ALL_AXES = -1

# Generate commands
def commandWave( amplitude, offset, phase, axis=-1, index=-1 ):
	"""
		Generates the string containing the command to be sent to the 
		server for movement
	"""

	# Convert axis information: 	
	if axis == X_AXIS:
		axis = 'X'
	elif axis == Y_AXIS:
		axis = 'Y'
	elif axis == ALL_AXES:
		axis = 'XY'
	else:
		raise ValueError

	# -1 means all modules
	if index == -1:
		index = ''

	# Command:
	command = axis + str(index) + ' A' + str(amplitude) + ' O' + str(offset) + ' P' + str(phase)
	return command

def commandPeriod( period):
	"""
		Generates the string containing the command to be sent to the 
		server for setting the period
	"""

	if period < 0:
		raise ValueError
	else:
		return 'T' + str(period)

def authenticate( serialPort, key):
	"""
		Authenticates with the server
	"""
	serialPort.write( 'i' + key) 


def setupSerialPort( name, baudRate):
	"""
		Creates a serial connection with the specified parameters
	"""	

	# Create a serial object
	serialPort = serial.Serial()

	# Set the main parameters
	serialPort.port = name
	serialPort.baudrate = baudRate

	# Open port
	serialPort.open()
	
	# Feedback
	if serialPort.isOpen():
		print '[+] Connected successfully to ' + name + ' at ' + str(baudRate) + ' bauds'
	else: 
		print '[+] Error connecting to ' + name + ' at ' + str(baudRate) + ' bauds'

	return serialPort



def readPort( serialPort):
	"""
		Reads a string from the serial port
	"""
	
	string = ''
	
	while serialPort.inWaiting() > 0:
		string += serialPort.read(1)

	return string


def reset( serialPort):			
	serialPort.setDTR(1)
	time.sleep(0.2)
	serialPort.setDTR(0)

def startup( portName, baudRate):
	"""
		Starts the system
	"""
	serialPort = setupSerialPort(portName, baudRate)

	print '[+] Waiting for the robot...'
	reset( serialPort)

	# Wait for the robot to be ready
	read = False
	while not read or read == ' ' or read == '':
		read = readPort( serialPort)
		if read == 'Ready':
			read = True 
		time.sleep(0.05)

	# Authenticate on the robot:
	authenticate( serialPort, '1234')
	time.sleep(0.05)
	print 'SnakeServer> ' + readPort(serialPort)
	
	return serialPort

# Main function:
# ------------------------------------------------------------------------------
def main():
	print '[+] Testing command generation...'
	print commandWave(60,  0,  0, X_AXIS)
	print commandWave( 0, 60,  0, ALL_AXES)

	print '[+] Testing connection...'
	serialPort = startup( '/dev/ttyUSB0', 9600)


	serialPort.write( commandPeriod( 4000) )
	time.sleep(0.05)
	serialPort.write( commandWave(60, 0, 0, X_AXIS) )
	
	

if __name__ == '__main__':
	main()
