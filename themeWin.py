from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from bs4 import BeautifulSoup
from PyQt5.QtCore import pyqtSignal
import re
import parent

if __name__ == "__main__":
	from PyQt5.QtWidgets import QApplication
	app = QApplication([])

class themeWin(QWidget):
	closed = pyqtSignal()

	def __init__(self, filename):
		super().__init__()

		self.dim = [720, 480]
		self.fpath = filename
		self.testDisp = QTextEdit()
		self.bgColor = QLineEdit()
		self.tColor = QLineEdit()
		self.bgColor.setReadOnly(True)
		self.tColor.setReadOnly(True)
		self.testDisp.setReadOnly(True)
		self.changeBg = QPushButton("Change Background")
		self.changeT = QPushButton("Change Text")
		self.apply = QPushButton("Apply")

		self.colorDia = QColorDialog()

		# self.changeBg.clicked.connect(self.colorDialog)

		layout = QGridLayout()

		layout.addWidget(self.testDisp, 0, 0, 3, -1)
		layout.addWidget(self.bgColor, 3, 0, 1, 1)
		layout.addWidget(self.changeBg, 3, 1, 1, 1)
		layout.addWidget(self.tColor, 3, 2, 1, 1)
		layout.addWidget(self.changeT, 3, 3, 1, 1)
		layout.addWidget(self.apply, 3, 4, 1, 1)

		self.openDark = QAction("&Dark Theme")
		self.openDark.triggered.connect(self.setDark)

		self.openLit = QAction("&Light Theme")
		self.openLit.triggered.connect(self.setLit)

		self.menuBar = QMenuBar()
		self.fMenu = self.menuBar.addMenu("&Default Themes")
		self.fMenu.addAction(self.openDark)
		self.fMenu.addAction(self.openLit)		
		layout.setMenuBar(self.menuBar)

		self.setGeometry(100, 100, 720, 480)

		self.setLayout(layout)

		self.soup = BeautifulSoup(open(filename, 'r'), 'html.parser')
		self.html = str(self.soup.find("html"))
		self.style = str(self.soup.find("style"))

		self.findColours()
		self.allPre = "<html><head>"
		self.allPos = "</head></html>"

		self.defString = '<body><h2> Heading! </h2> <p> This is some text </p></body>'

		self.testDisp.setText(self.allPre + self.defString + self.allPos)

		self.changeBg.clicked.connect(self.changeBGfunct)
		self.changeT.clicked.connect(self.changeTfunct)
		self.apply.clicked.connect(self.saveFile)

		
		font = QFont()
		font.setFamily("Times")
		font.setPointSize(24)
		self.testDisp.setFont(font)

		self.changeHTML()

	def colorDialog(self):
		return self.colorDia.getColor()
		
	def changeBGfunct(self):
		color = self.colorDialog().name()
		self.bgColor.setText(color)
		self.changeHTML()

	def changeTfunct(self):
		color = self.colorDialog().name()
		self.tColor.setText(color)
		self.changeHTML()

	def setDark(self):
		self.bgColor.setText("#1e1e1e")
		self.tColor.setText("#cecece")
		self.changeHTML()

	def setLit(self):
		self.bgColor.setText("#ffffff")
		self.tColor.setText("#000000")
		self.changeHTML()

	def findColours(self):
		bgColor = re.findall(r"background-color:#\w\w\w\w\w\w", self.style)
		tColor = re.findall(r"\scolor:#\w\w\w\w\w\w", self.style)
		bgColor = str(bgColor[0])
		tColor = str(tColor[0])
		bgColor = bgColor[len(bgColor) - 7: len(bgColor)]
		tColor = tColor[len(tColor) - 7: len(tColor)]
		self.bgColor.setText(bgColor)
		self.tColor.setText(tColor)

	def changeHTML(self):
		inter = re.finditer(r"#\w\w\w\w\w\w", self.style)
		indexed = [m.start(0) for m in inter]
		for x in indexed:
			if(self.style[x-7:x] == '-color:'):
				self.style = self.style.replace(self.style[x:x+7], self.bgColor.text())
			else:
				self.style = self.style.replace(self.style[x:x+7], self.tColor.text())
		self.testDisp.setText(self.allPre + self.style + self.defString + self.allPos)

	def setHTML(self):
		self.testDisp.setText(self.defString)
		

	def saveFile(self):
		toSave = self.allPre + self.style + self.allPos
		with open(self.fpath, 'w') as file:
			file.write(self.style)

	def closeEvent(self, event):
		self.closed.emit()
		self.saveFile()
		self.close()

if __name__ == "__main__":
	
	test = themeWin("C:\\Users\\Tomoya\\Desktop\\python fic\\src\\main\\python\\test.html")
	test.show()

	app.exec_()