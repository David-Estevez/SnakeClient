"""
	Graphic User Interface for SnakeClient
	
"""
__author__ = 'David Estevez-Fernandez'
__license__ = 'GPLv3'

import wx
import glob
import time

class MainWin( wx.Frame):

	def __init__(self, parent, core):
		# Store the SnakeClient core
		self.core = core

		# Load Config file:
		self.parseConfig()
	
		# Construct the window
		super( MainWin, self).__init__(parent, title='SnakeClient', size=(600, 100+100*max( self.x_sets, self.y_sets)), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

		self.InitUI()
		self.Centre()
		self.Show()


	def InitUI(self):
		self.panel = wx.Panel(self)

		font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
		font.SetPointSize(9)
	
		# Control for the period
		self.textT = wx.StaticText( self.panel, label='Period (ms):', pos=(5, 10) )
		self.spinT = wx.SpinCtrl( self.panel, pos=(80, 5), size=(60, -1))
		self.spinT.SetRange(1, 20000)
		self.spinT.SetValue(4000)
		self.spinT.Bind( wx.EVT_SPINCTRL, self.sendT)
	
		# Control sets
		self.setsX = []
		self.setsY = []
		
		for i in range( self.x_sets ):
			self.setsX.append( ControlSet( self, label='X Axis ' + str(i), pos = (5, 40 + 100*i ),
						 identifier=(0,i)))

		for i in range( self.y_sets):
			self.setsY.append( ControlSet( self, label='Y Axis' + str(i), pos = (300, 40+ 100*i ),
						identifier=(1, i)))
		
		# Serial connection controls
		self.serialControls = SerialControls( self, pos = (5, 40 + 100*max( self.x_sets, self.y_sets) ))
		

	def parseConfig(self):
		"""
			Opens the file "config.txt" and reads the configuration values
		"""
		try:
			f = open( './config.txt', 'r')
			self.x_sets = int( f.readline().strip('x_axis=').strip('\n'))
			self.y_sets = int( f.readline().strip('y_axis=').strip('\n'))
			f.close()
		except Exception, e:
			print e
			exit(1)
	
	def sendT( self, e):
		"""
			Sends the period to the robot
		"""
		self.core.sendPeriod( self.spinT.GetValue() )


# class ControlSet
# ---------------------------------------------------------------------------------------
# Controls for controlling one module
	
class ControlSet( ):
	
	def __init__( self, parent, label, pos, identifier):
		"""
			Create the layout of the custom widget
		"""
		self.parent = parent
		self.identifier = identifier
		panel = self.parent.panel

		# Box around the controls
		self.box = wx.StaticBox( panel, label=label, pos=pos, size=(290, 90)) 


		# Controls for the amplitude
		self.textA = wx.StaticText( panel, label='A ', pos=(pos[0]+5, pos[1]+20) )
		self.sliderA = wx.Slider( panel , value=0, minValue=0, maxValue=90, 
				pos=(pos[0]+25, pos[1]+15), size=(230, -1), style=wx.SL_HORIZONTAL) 
		self.valueA = wx.StaticText( panel, label='0', pos=( pos[0]+260, pos[1]+20) )

		self.sliderA.Bind( wx.EVT_SCROLL, self.OnSliderScrollA)	


		# Controls for the offset
		self.textO = wx.StaticText( panel, label='O ', pos=(pos[0]+5,  pos[1]+40) )
		self.sliderO = wx.Slider( panel , value=0, minValue=-90, maxValue=90, 
				pos=(pos[0]+25, pos[1]+35), size=(230, -1), style=wx.SL_HORIZONTAL) 	

		self.valueO = wx.StaticText( panel, label='0', pos=( pos[0]+260, pos[1]+40) )

		self.sliderO.Bind( wx.EVT_SCROLL, self.OnSliderScrollO)	


		# Controls for the phase
		self.textPh = wx.StaticText( panel, label='Ph ', pos=(pos[0]+5,  pos[1]+60) )
		self.sliderPh = wx.Slider( panel , value=0, minValue=0, maxValue=360, 
				pos=(pos[0]+25, pos[1]+55), size=(230, -1), style=wx.SL_HORIZONTAL)

		self.valuePh = wx.StaticText( panel, label='0', pos=( pos[0]+260, pos[1]+60) )

		self.sliderPh.Bind( wx.EVT_SCROLL, self.OnSliderScrollPh)	



	def OnSliderScrollA(self, e):
		"""
			Actions to be performed when the slider is moved
		"""
		# Get Value from slider
		value = self.sliderA.GetValue()

		# Set Value to label
		self.valueA.SetLabel( str(value) )

		# Send Value
		self.send()
		

		 	
	def OnSliderScrollO(self, e):
		"""
			Actions to be performed when the slider is moved
		"""
		# Get Value from slider
		value = self.sliderO.GetValue()

		# Set Value to label
		self.valueO.SetLabel( str(value) )

		# Send Value
		self.send()


	def OnSliderScrollPh(self, e):
		"""
			Actions to be performed when the slider is moved
		"""
		# Get Value from slider
		value = self.sliderPh.GetValue()

		# Set Value to label
		self.valuePh.SetLabel( str(value) )

		# Send Value
		self.send()

	def send( self):
		valueA = self.sliderA.GetValue()
		valueO = self.sliderO.GetValue()
		valuePh = self.sliderPh.GetValue()

		self.parent.core.sendWave( valueA, valueO, valuePh, self.identifier[0], self.identifier[1])
		time.sleep(0.01)

# class SerialControls
# --------------------------------------------------------------------------------------
# Controls to connect through a serial interface

class SerialControls:
	def __init__(self, parent, pos):
		"""
			Controls for connecting to the robot
		"""

		# Obtain parameters
		x = pos[0]
		y = pos[1]

		self.parent = parent
		panel = self.parent.panel

		# Serial controls
		self.serialBox = wx.StaticBox( panel, label='Serial Settings', pos=(x, y), size=(580, 55))

		self.buttonPort = wx.Button( panel, label='Port:', pos=(x+5, y+20), size=(50, 25))
		self.buttonPort.Bind( wx.EVT_BUTTON, self.refresh)
		self.portList = self.getSerialPorts()
		self.portCombo = wx.ComboBox( panel, pos=(x+55, y+20), size=(120,25), 
				choices = self.portList, style=wx.CB_READONLY)

		if ( len(self.portList) > 0):
			self.portCombo.SetStringSelection( self.portList[0])

		self.textBaudRate = wx.StaticText( panel, label='BaudRate:', pos=(x+180, y+25))
		self.inputBaudRate = wx.TextCtrl( panel, pos=(x+245, y+20), size=(70, 25))
		self.inputBaudRate.SetValue('9600')

		self.textStatus = wx.StaticText( panel, label='Status:', pos=(x+325, y+25))
	
		self.connectButton = wx.Button( panel, label='Connect', size=(80, 25), pos=(x+490, y+20))
		self.connectButton.Bind( wx.EVT_BUTTON, self.connect)


	def connect(self, e):
		"""
			Connects to the robot
		"""
		portName = self.portCombo.GetStringSelection()
		baudRate = self.inputBaudRate.GetString(0, -1)

		if ( portName and baudRate ):
			# Show password dialog:
			self.passwordDialog = wx.PasswordEntryDialog( self.parent, 'Insert SnakeServer password:', 'Insert password')
			self.passwordDialog.ShowModal()

			self.setStatus('Waiting for reset')
			self.parent.core.startup( portName, baudRate, self.passwordDialog.GetValue())
			self.setStatus('connected')

		
	def setStatus( self, text):
		"""
			Sets the status
		"""
		self.textStatus.SetLabel( 'Status: ' + text)


	def getSerialPorts(self):
		"""
			Returns the available serial ports
		"""
		return glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*') + glob.glob("/dev/tty.*") + glob.glob("/dev/cu.*") + glob.glob("/dev/rfcomm*")


	def refresh(self, e):
		"""
			Updates the list of ports
		"""
		self.portCombo.Clear()

		for port in self.getSerialPorts():
			self.portCombo.Append( port)
		
	

if __name__ == '__main__':
	app = wx.App()
	MainWin( None, None)
	app.MainLoop()
