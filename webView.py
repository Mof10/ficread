import sys
from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QPushButton
if __name__ == "__main__":
	from PyQt5.QtWidgets import QApplication
import parent

class webWin(QWidget, parent.posClass, parent.win):
	def __init__(self):
		super().__init__()
		self.dim = [0, 0]
		self.web = QWebEngineView()			
		self.layout = QGridLayout()
		self.dispURL = QLineEdit()
		self.dispURL.setReadOnly(True)
		self.subButton = QPushButton("Load")
		self.subButton.setDisabled(True)
		self.left = QPushButton("<--")
		self.right = QPushButton("-->")
		self.ref = QPushButton("Refresh")	
		self.setup()

	def updateDim(self):
		self.dim[0] = self.geometry().width()
		self.dim[1] = self.geometry().height()

	def setURL(self, URL):
		self.web.load(QUrl(URL))

	def reset(self):
		self.web.load(QUrl("https://archiveofourown.org/media"))

	def isArchive(self, url):
		test = "https://archiveofourown.org"
		if(url.find(test) != -1):
			return True
		else:
			return False		

	def isWork(self, url):
		test = "https://archiveofourown.org/works"
		isNot = "https://archiveofourown.org/works/search"
		if(url.find(test) != -1 and url.find(isNot) == -1):
			return True
		else:
			return False

	def openSubmit(self):
		self.dispURL.setText(self.web.title())
		if(self.isWork(self.web.title())):
			self.subButton.setDisabled(False)
		else:
			self.subButton.setDisabled(True)

	def openSubmit2(self):
		self.dispURL.setText(self.web.title())
		if(self.isArchive(self.web.title())):
			self.subButton.setDisabled(False)
		else:
			self.subButton.setDisabled(True)			

	def setup(self):
	
		self.web.load(QUrl("https://archiveofourown.org/media"))
		self.web.urlChanged.connect(self.openSubmit)

		self.left.clicked.connect(self.web.back)
		self.right.clicked.connect(self.web.forward)
		self.ref.clicked.connect(self.web.reload)

		self.layout.addWidget(self.left, 0, 0, 1, 1)
		self.layout.addWidget(self.right, 0, 1, 1, 1)
		self.layout.addWidget(self.ref, 0, 3, 1, 1)
		self.layout.addWidget(self.web, 1, 0, 4, 5)
		self.layout.addWidget(self.dispURL, 5, 0, 1, -1)
		self.layout.addWidget(self.subButton, 5, 4, 1, 1)
		self.setLayout(self.layout)

if __name__ == "__main__":
	app = QApplication([])
	temp = webWin()
	temp.show()
	sys.exit(app.exec_())