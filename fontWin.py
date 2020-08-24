from PyQt5.QtWidgets import QWidget, QGridLayout, QComboBox, QTextEdit
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont, QFontDatabase
import parent
if __name__ == "__main__":
	from PyQt5.QtWidgets import QApplication
	app = QApplication([])

class fontWin(QWidget, parent.posClass, parent.win):

	def __init__(self, font, size):#, screenSize, parPos):
		super().__init__()


		self.dim = [720, 480]
		# self.setGeometry(100, 100, 720, 480)
		self.layout = QGridLayout()

		self.sizeBox = QComboBox()
		self.fontBox = QComboBox()
		self.sizeBox.setEditable(False)
		self.fontBox.setEditable(False)

		self.sizeBox.activated.connect(self.reload)
		self.fontBox.activated.connect(self.reload)

		self.sampleText = QTextEdit()
		self.sampleText.setText("Please select font size and family, and then close the window.")

		self.font = QFont()
		self.font.setFamily(font)
		self.font.setPointSize(int(size))

		self.loadSize()

		self.sizeBox.setCurrentText(size)

		self.layout.addWidget(self.sizeBox, 2, 0, 1, 1)
		self.layout.addWidget(self.fontBox, 2, 4, 1, 3)
		self.layout.addWidget(self.sampleText, 0, 0, 2, -1)
		self.setLayout(self.layout)

		self.loadFonts()
		self.sampleText.setFont(self.font)

		self.fontBox.setCurrentText(font)


	# def updatePos(self, parentPos, parentDim):
	# 	pos = self.findPos(parentPos, parentDim, self.dim)

	# 	self.setGeometry(pos[0], pos[1], self.dim[0], self.dim[1])

	def reload(self):
		self.font.setFamily(self.fontBox.currentText())
		self.font.setPointSize(int(self.sizeBox.currentText()))
		self.sampleText.setFont(self.font)


	def loadFonts(self):
		database = QFontDatabase()
		for family in database.families():
			self.fontBox.insertItem(999999, family)


	def loadSize(self):
		for x in range(7, 73):
			if x % 2 == 0:
				self.sizeBox.insertItem(100, str(x))


if __name__ == "__main__":
	teest = fontWin("Times New Roman", "16")
	teest.show()

	app.exec_()