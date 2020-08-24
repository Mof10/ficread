from PyQt5.QtWidgets import QWidget, QGridLayout, QComboBox, QPushButton, QLabel, QTextEdit
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
import os
import configparser
import codecs
from pathlib import Path
from bs4 import BeautifulSoup
import parent
from datetime import datetime
from os.path import dirname, abspath

if __name__ == "__main__":
	from PyQt5.QtWidgets import QApplication
	app = QApplication([])

GLOBALdoLog = True
GLOBALlogPath = dirname(abspath(__file__)) + "\\log.txt"

class iniWin(QWidget, parent.posClass):
	closed = pyqtSignal()
	retSig = pyqtSignal()

	def __init__(self, folder):
		super().__init__()
		self.dim = [600, 450]
		self.layout = QGridLayout()

		self.iniList = QComboBox()
		self.other = QPushButton("Load from other directory?")
		self.ldButton = QPushButton("Load Fic")

		self.fandomLab = QLabel("Fandom:")
		self.fandom = QTextEdit()
		self.font = QFont()
		self.font.setPointSize(16)
		self.fandom.setFont(self.font)
		self.fandom.setReadOnly(True)

		self.layout.addWidget(self.iniList, 0, 2, 1, 2)
		self.layout.addWidget(self.other, 0, 0, 1, 1)
		self.layout.addWidget(self.ldButton, 6, 3, 1, 1)
		# self.layout.addWidget(self.fandomLab, 2, 0, 1, 1)
		self.layout.addWidget(self.fandom, 3, 0, 3, -1)

		self.folder = folder
		self.dirs = []
		self.titles = []
		self.fandoms = []

		self.setLayout(self.layout)
		self.loadFiles()

		self.ldButton.clicked.connect(self.ret)
		self.iniList.activated.connect(self.loadFandom)

	def closeEvent(self, event):
		self.closed.emit()
		self.close()

	def ret(self):
		self.retSig.emit()
		self.close()

	def loadFandom(self):
		ind = self.iniList.currentIndex()
		load = configparser.ConfigParser()
		try:
			load.read(self.dirs[ind])
			self.fandom.setText("<h3>" + self.titles[ind] + "</h3>" + str(self.fandoms[ind]))	
		except:
			if __name__ != '__main__':
					with open(GLOBALlogPath, 'a') as f:
						now = datetime.now()
						# dd/mm/YY H:M:S
						dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
						f.write(dt_string + " : Error in loadFandoms reading: " + self.dirs[ind] + "\n")
			else:
				print("Error in loadFandoms reading: ", self.dirs[ind])
		

	def loadTitles(self):
		for x in self.dirs:
			load = configparser.ConfigParser()
			try:
				load.read(x)
				soup = BeautifulSoup(codecs.open(load['FicDetails']['filepath'], 'r', 'utf-8'), 'html.parser')
				self.titles.append(soup.find("h1").get_text() + " by " + soup.find("a", rel="author").get_text())
				self.fandoms.append(soup.find('dl', class_='tags'))				
			except:
				if __name__ != '__main__':
						with open(GLOBALlogPath, 'a') as f:
							now = datetime.now()
							# dd/mm/YY H:M:S
							dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
							f.write(dt_string + " : Error in loadFandoms reading: " + x + "\n")		
				else:		
					print("Error in loadTitles: ", x)


	def loadFiles(self):
		self.iniList.clear()
		self.dirs.clear()
		self.titles.clear()
		for file in os.listdir(self.folder):
			if file.endswith(".ini"):
				self.dirs.append(self.folder + file)
		self.dirs.sort(key=os.path.getmtime)
		self.dirs.reverse()
		if(len(self.dirs)):
			self.loadTitles()
			self.iniList.insertItems(0, self.titles)
			self.loadFandom()

if __name__ == "__main__":
	test = iniWin("C:\\Users\\Tomoya\\Desktop\\python fic\\src\\main\\python\\save\\fic\\")
	test.show()
	app.exec_()
