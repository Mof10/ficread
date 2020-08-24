from PyQt5.QtWidgets import QTextEdit, QWidget, QGridLayout
from PyQt5.QtCore import pyqtSignal
import parent

if __name__ == "__main__":
	from PyQt5.QtWidgets import QApplication
	app = QApplication([])


class deetWin(QWidget, parent.posClass, parent.win):
	def __init__(self):
		super().__init__()
		self.win = QTextEdit()
		self.win.setReadOnly(True)
		self.layout = QGridLayout()
		self.layout.addWidget(self.win, 0, 0, -1, -1)
		self.setLayout(self.layout)
		self.dim = [720, 480]

if __name__ == "__main__":

	test = deetWin()
	# test.showText("C:\\Users\\Tomoya\\Desktop\\testhtml\\test11.html")

	app.exec_()

