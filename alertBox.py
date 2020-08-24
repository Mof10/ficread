from PyQt5.QtWidgets import QTextEdit, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal
import parent

if __name__ == "__main__":
	from PyQt5.QtWidgets import QApplication
	app = QApplication([])	

class alertWin(QWidget, parent.posClass, parent.win):

	def __init__(self):
		super().__init__()
		self.dim = [450,150]
		self.alert = QLabel("")
		self.alert.setWordWrap(True)
		self.layout = QVBoxLayout()

		# self.setGeometry(100, 100, 200, 100)
		self.exButton = QPushButton("Close")
		self.alert.setAlignment(Qt.AlignCenter)

		font = QFont()
		font.setPointSize(12)

		self.alert.setFont(font)

		self.layout.setAlignment(Qt.AlignCenter)
		self.layout.addWidget(self.alert)
		self.setWindowTitle("Alert")
		self.layout.addWidget(self.exButton)

		self.setLayout(self.layout)
		self.exButton.clicked.connect(self.closeWin)

	def updateDim(self):
		self.dim[0] = self.geometry().width()
		self.dim[1] = self.geometry().height()

	def disAlert(self, text):
		self.updateDim()
		self.alert.setText(text)
		self.show()

	def closeWin(self):
		self.close()


if __name__ == "__main__":

	test = alertWin()
	test.disAlert("Test")
	app.exec_()