"""
	Graphic User Interface for SnakeClient
	
"""
__author__ = 'David Estevez-Fernandez'
__license__ = 'GPLv3'

import wx

class MainWin( wx.Frame):

	def __init__(self, parent, title):
		super( MainWin, self).__init__(parent, title=title, size=(600, 150) )

		self.InitUI()
		self.Centre()
		self.Show()

	def InitUI(self):
		panel = wx.Panel(self)
	
		# Control for the period
		self.textT = wx.StaticText( panel, label='Period (ms):', pos=(5, 10) )
		self.spinT = wx.SpinCtrl( panel, pos=(80, 5), size=(60, -1))
		self.spinT.SetRange(0, 20000)
		self.spinT.SetValue(4000)
	
		# Control sets
		ControlSet( panel, label='X Axis 1', pos = (5, 40) )
		ControlSet( panel, label='Y Axis 1', pos = (300, 40) )

		# Controls for connecting to robot
		self.textPortName = wx.StaticText( panel, label='Port:', pos=(5, 130))


class ControlSet( ):
	
	def __init__( self, panel, label, pos):
		"""
			Create the layout of the custom widget
		"""
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
		obj = e.GetEventObject()
		value = obj.GetValue()

		# Set Value to label
		self.valueA.SetLabel( str(value) )

		 	
	def OnSliderScrollO(self, e):
		"""
			Actions to be performed when the slider is moved
		"""
		# Get Value from slider
		obj = e.GetEventObject()
		value = obj.GetValue()

		# Set Value to label
		self.valueO.SetLabel( str(value) )


	def OnSliderScrollPh(self, e):
		"""
			Actions to be performed when the slider is moved
		"""
		# Get Value from slider
		obj = e.GetEventObject()
		value = obj.GetValue()

		# Set Value to label
		self.valuePh.SetLabel( str(value) )


if __name__ == '__main__':
	app = wx.App()
	MainWin( None, title='SnakeClient')
	app.MainLoop()
