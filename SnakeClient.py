#!/usr/bin/python

"""
	SnakeClient
	-------------------------------------------------
	Control modular robots using the SnakeServer protocol

"""

__author__ = 'David Estevez-Fernandez'
__license__ = 'GPLv3'
__version__ = '2.0'

# Imports
# ------------------------------------------------------------------------------
from snakeclient.SnakeClientCore import Core
from snakeclient.GUI import MainWin
import wx
import time, sys

# Main function
# ------------------------------------------------------------------------------
def main():
	app = wx.App()
	snakeclientcore = Core()
	MainWin( None, snakeclientcore)
	app.MainLoop()


if __name__ == '__main__':
	main()
