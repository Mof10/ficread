from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
import ctypes

class posClass():
	# def __init__(self):

	def retScreen(self):
		user32 = ctypes.windll.user32
		screenW = user32.GetSystemMetrics(0)
		screenH = user32.GetSystemMetrics(1)

		return [screenW, screenH]

	def findPos(self, screenPos, parentWinDim, childWinDim):
		#Size = list, width, height
		#pos = x, y of parent window

		screenSize = self.retScreen()

		#Where the parent window SHOULD be if it is centered
		intendedX = int((screenSize[0] - parentWinDim[0]) / 2) 
		intendedY = int((screenSize[1] - parentWinDim[1]) / 2)

		#Offset if window is off of where if should be
		xOff = screenPos[0] - intendedX
		yOff = screenPos[1] - intendedY

		#Find where the calling window needs to be
		intendedX = int((screenSize[0] - childWinDim[0]) / 2) 
		intendedY = int((screenSize[1] - childWinDim[1]) / 2)

		return [intendedX + xOff, intendedY + yOff]

	def updatePos(self, parentPos, parentDim):
		pos = self.findPos(parentPos, parentDim, self.dim)

		self.setGeometry(pos[0], pos[1], self.dim[0], self.dim[1])

class win():

	closed = pyqtSignal()

	def closeEvent(self, event):
		self.closed.emit()
		self.close()
