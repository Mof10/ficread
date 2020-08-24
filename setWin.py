from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QFileDialog, QGridLayout, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal
import parent
import webView

if __name__ == "__main__":
	from PyQt5.QtWidgets import QApplication
	app = QApplication([])

import alertBox

class setWin(QWidget, parent.posClass, parent.win):

	def __init__(self, ficSave, iniSave, url, doAsk):
		super().__init__()

		self.dim = [600,500]
		# self.setGeometry(100, 100, 600, 500)

		self.browse = QFileDialog()
		# self.browse.setAcceptMode(QFileDialog.AcceptOpen)
		# self.browse.setFileMode(QFileDialog.Directory)

		self.win = webView.webWin()
		self.win.web.urlChanged.connect(self.win.openSubmit2)

		self.ficSavePath = QLineEdit(ficSave)
		self.ficSavePath.setReadOnly(True)
		self.ficSBButton = QPushButton("Browse")
		# self.ficSaveBrowse = QFileDialog()
		self.ficSaveLab = QLabel("Where will downloaded fic HTMLs be saved?")

		self.iniSavePath = QLineEdit(iniSave)
		self.iniSavePath.setReadOnly(True)
		self.iniSBButton = QPushButton("Browse")
		# self.iniSaveBrowse = QFileDialog()
		self.iniSaveLab = QLabel("Where will saved reads be saved? (saved as INI file)")

		self.URLLabel = QLabel("What is the default AO3 URL that will load when a browser window is opened?")
		self.defaultURL = QLineEdit(url)
		self.defaultURL.setReadOnly(True)
		self.changeURLButton = QPushButton("Change URL")

		self.doAsk = QCheckBox()
		self.doAsk.setChecked(doAsk)
		self.doAskLab = QLabel("Always ask before saving HTMLs?")
		# self.doAskLab.setAlignment(Qt.AlignBottom)
		self.doAskLab.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)

		self.fill = QLabel("")

		self.apply = QPushButton("Apply")

		layout = QGridLayout()

		layout.addWidget(self.ficSaveLab, 0, 0, 1, -1)
		layout.addWidget(self.ficSavePath, 1, 0, 1, 3)
		layout.addWidget(self.ficSBButton, 1, 3, 1, 1)

		layout.addWidget(self.fill, 2, 0, 1, -1)
		layout.setRowMinimumHeight(2, 100)

		layout.addWidget(self.iniSaveLab, 3, 0, 1, -1)
		layout.addWidget(self.iniSavePath, 4, 0, 1, 3)
		layout.addWidget(self.iniSBButton, 4, 3, 1, 1)

		layout.addWidget(self.fill, 5, 0, 1, -1)
		layout.setRowMinimumHeight(5, 100)

		layout.addWidget(self.URLLabel, 6, 0, 1, -1)
		layout.addWidget(self.defaultURL, 7, 0, 1, 3)
		layout.addWidget(self.changeURLButton, 7, 3, 1, 1)

		layout.addWidget(self.fill, 8, 0, 1, -1)
		layout.setRowMinimumHeight(8, 50)

		layout.addWidget(self.apply, 9, 0, 1, 2)
		layout.addWidget(self.doAsk, 9, 3, 1, 1)
		layout.addWidget(self.doAskLab, 8, 2, 1, 2)

		self.setLayout(layout)

		self.buttons = [self.ficSBButton, self.iniSBButton, self.changeURLButton, self.apply]

		self.ficSBButton.clicked.connect(self.getFicSave)
		self.iniSBButton.clicked.connect(self.getIniSave)
		self.changeURLButton.clicked.connect(self.getURL)

	def getFicSave(self):
		self.disButtons()
		folder = self.openBrowse()
		if(folder != ""):
			self.ficSavePath.setText(folder)
		self.enButtons()

	def getIniSave(self):
		self.disButtons()
		folder = self.openBrowse()
		if(folder != ""):
			self.iniSavePath.setText(folder)
		self.enButtons()


	def getURL(self):
		def changeURL():
			self.defaultURL.setText(self.win.dispURL.text())
			self.win.close()
		self.win.show()
		self.win.subButton.clicked.connect(changeURL)


	def openBrowse(self):
		return self.browse.getExistingDirectory()

	def disButtons(self):
		for x in self.buttons:
			x.setDisabled(True)

	def enButtons(self):
		for x in self.buttons:
			x.setDisabled(False)



if __name__ == "__main__":
	test = setWin("", "", "", 1)
	test.show()

	app.exec_()