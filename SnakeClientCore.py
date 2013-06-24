"""
	SnakeClientCore
	-------------------------------------------------
	Control modular robots using the SnakeServer protocol - core functionality

"""

__author__ = 'David Estevez-Fernandez'
__license__ = 'GPLv3'

# Imports
# ------------------------------------------------------------------------------
import serial
import time
import sys


class Core:
	def __init__(self):	
		# Define constants:
		# ------------------------------------------------------------------------------
		self.X_AXIS = 0
		self.Y_AXIS = 1
		self.ALL_AXES = -1

		# Define variables:
		# ------------------------------------------------------------------------------
		self.serialPort = None


	# Generate commands
	def commandWave(self, amplitude, offset, phase, axis=-1, index=-1 ):
		"""
			Generates the string containing the command to be sent to the 
			server for movement
		"""

		# Convert axis information: 	
		if axis == self.X_AXIS:
			axis = 'X'
		elif axis == self.Y_AXIS:
			axis = 'Y'
		elif axis == self.ALL_AXES:
			axis = 'XY'
		else:
			raise ValueError

		# -1 means all modules
		if index == -1:
			index = ''

		# Command:
		command = axis + str(index) + ' A' + str(amplitude) + ' O' + str(offset) + ' P' + str(phase)
		return command

	def commandPeriod(self, period):
		"""
			Generates the string containing the command to be sent to the 
			server for setting the period
		"""

		if period < 0:
			raise ValueError
		else:
			return 'T' + str(period)


	def sendWave(self, amplitude, offset, phase, axis=-1, index=-1 ):
		"""
			Sends a particular wave to the robot
		"""
		self.serialPort.write( self.commandWave( amplitude, offset, phase, axis, index))


	def sendPeriod( self, period):
		"""
			Sends the value for the period
		"""
		self.serialPort.write( self.commandPeriod( period))
 

	def authenticate(self, key):
		"""
			Authenticates with the server
		"""
		self.serialPort.write( 'i' + key) 


	def setupSerialPort(self, name, baudRate):
		"""
			Creates a serial connection with the specified parameters
		"""	

		# Create a serial object
		self.serialPort = serial.Serial()
	
		# Set the main parameters
		self.serialPort.port = name
		self.serialPort.baudrate = baudRate
	
		# Open port
		self.serialPort.open()
		
		# Feedback
		if self.serialPort.isOpen():
			print '[+] Connected successfully to ' + name + ' at ' + str(baudRate) + ' bauds'
		else: 
			print '[+] Error connecting to ' + name + ' at ' + str(baudRate) + ' bauds'



	def readPort(self):
		"""
			Reads a string from the serial port
		"""
		
		string = ''
		
		while self.serialPort.inWaiting() > 0:
			string += self.serialPort.read(1)

		return string


	def reset(self):	
		"""
			Resets the robot
		"""		
		self.serialPort.setDTR(1)
		time.sleep(0.2)
		self.serialPort.setDTR(0)
	

	def startup(self, portName, baudRate, key):
		"""
			Starts the system
		"""
		self.setupSerialPort(portName, baudRate)

		print '[+] Waiting for the robot...'
		self.reset()
	
		# Wait for the robot to be ready
		read = False
		while not read or read == ' ' or read == '':
			read = self.readPort()
		if read == 'Ready':
			read = True 
		time.sleep(0.05)

		# Authenticate on the robot:
		self.authenticate( key )
		time.sleep(0.05)
		print 'SnakeServer> ' + self.readPort()
		

# Main function:
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


	core.sendPeriod( 4000 )
	time.sleep(0.05)
	core.sendWave(60, 0, 0, core.X_AXIS) 
	
	

if __name__ == '__main__':
	main()
