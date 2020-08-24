from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSignal
from bs4 import BeautifulSoup
from unidecode import unidecode
import parse
import sys
import HTML
import fontWin
import findini
import setWin
import webView
import alertBox
import ficDeets
import parent
import themeWin
import codecs
import re
import configparser
import os
from os.path import isfile
from os.path import dirname, abspath
import requests
import ctypes

GLOBALdoLog = True
GLOBALlogPath = dirname(abspath(__file__)) + "\\log.txt"

#Screen width and height

#TOADD
#Fic Details //done
#Default save place //done
#Chapter Notes!!!!!: done
#Edit font / size, likely through another window done
#Default save folder with 'Ask where to save every html file?' done
#Check for updated fic?
#Any extra windows open in the centre of the central window
#Changing themes

# def rem_Non_Ascii(text):
# 	return unidecode(unicode(text, encoding = "utf-8"))

class URLWin(QWidget, parent.posClass):
	closed = pyqtSignal()

	def __init__(self):
		super().__init__()
		self.setWindowTitle("AO3 Work URL")
		self.dim = [350, 75]
		self.templay = QHBoxLayout()
		self.tempBox = QLineEdit()
		self.tempBox.setPlaceholderText("Enter AO3 Work URL Here.")
		self.tempEnt = QPushButton("Submit")
		self.templay.addWidget(self.tempBox)
		self.templay.addWidget(self.tempEnt)
		self.setLayout(self.templay)

		#Usually, the close event is just to emit a closed signal, though the 
		#main window should close all active windows as it closes.
	def closeEvent(self, event):
		self.closed.emit()
		self.close()

class detail():
	def __init__(self):
		#The chapter contents, structures as a list of lists, [Num, Title, chapCon[]]
		self.chapters = []
		#The current pages for every given chapter (As an index)
		self.currPages = []
		#The current chapter number
		self.chapter = 0
		self.paraCountstr = "0 out of 0"
		self.filepath = ""
		self.url = ""
		self.title = ""
		self.author = ""
		self.fandom = ""
		self.pre = "<html>"
		self.post = "</body></html>"
		self.style = ""
		self.tempimg = ""

		#Formats the current page numbers to save in the fic ini file.
	def pageString(self):
		temp = ""
		for x in self.currPages:
			temp += str(x) + "-"
		return temp

		#Clears the two lists in this class.
	def clear(self):
		self.chapters.clear()
		self.currPages.clear()

		#Parse file, reads the provided html file on the filepath parameter
		#It will also initialize the chapter page numbers.
	def pFile(self, height, width):
		self.chapters.clear()
		self.currPages.clear()
		self.chapter = 0
		parse.getChaps(self.chapters, self.filepath, self.tempimg, height, width)
		self.initPages()

		#Sets up the paragraph counter, usually called from the main window
	def setParaCount(self):
		self.paraCountstr = str(self.currPages[self.chapter] + 1) + " out of " + str(len(self.chapters[self.chapter][2]))		

		#Sets all pagees to 0
	def initPages(self):
		for x in range(0, len(self.chapters)):
			self.currPages.append(0)

		#Iterates the current page count and increments the paragraph counter
	def nextP(self):
		self.currPages[self.chapter] += 1
		self.setParaCount()

		#Opposite of next
	def prevP(self):
		self.currPages[self.chapter] -= 1
		self.setParaCount()

	def pageText(self):
		return self.pre + self.style + self.chapters[self.chapter][2][self.currPages[self.chapter]] + self.post


#Find aspects of an html file that are needed to set in the detail class.
def findTags(file):
	#searching for the tag window, title + author, fandom, and the URL.

	def findURL(href):
		return href and re.compile("works").search(href)
	temp = []
	soup = BeautifulSoup(codecs.open(file, 'r', 'utf-8'), "html.parser")
	temp.append(str(soup.find("dl", class_="tags")))
	temp.append(soup.find("h1").get_text() + " by " + soup.find("a", rel="author").get_text())
	fandom = soup.find(text="Fandom:")
	fandom = fandom.next_element
	fandom = fandom.next_element
	temp.append(str(fandom.get_text()))
	temp.append(str(soup.find("a", href=findURL).get("href")))

	return temp

user32 = ctypes.windll.user32
screenW = user32.GetSystemMetrics(0)
screenH = user32.GetSystemMetrics(1)

class window(QWidget):

		#Declare all needed widgets and set their focus policy
	def __init__(self, parent = None):
		super(window, self).__init__(parent)

		self.setFocusPolicy(Qt.StrongFocus)
		#Default paths at very first startup
		self.homePath = dirname(abspath(__file__))
		self.baseSave = self.homePath + "\\save\\"
		self.defSave = self.homePath + "\\save\\fichtml\\"
		self.defIniSave = self.homePath + "\\save\\fic\\"
		self.defURL = "https://archiveofourown.org/media"
		self.doAsk = False

		#This should replace all of the above defaults with any changed values.
		self.initDir()

		#If the ini file does not already exist, create it within the root folder.
		if not(os.path.exists(self.homePath + 'settings.ini')):
			self.saveSettings()
		if not(os.path.exists(GLOBALlogPath)):
			create = open(GLOBALlogPath, 'w', encoding='utf-8')
			create.write("")
			create.close()

		#Load all of the settings from the settings.ini file.
		self.loadSettings()	

		#Initializing the settings window with the current defaults
		self.setWin = setWin.setWin(self.defSave, self.defIniSave, self.defURL, self.doAsk)

		self.layout = QGridLayout(self)

		#A label that keeps track of the paragraph numbers: x out of y.
		self.paraCount = QLabel(self)
		#All needed buttons.
		self.lButton = QPushButton("<--", self)
		self.rButton = QPushButton("-->", self)
		self.sButton = QPushButton("Save", self)
		self.wbButton = QPushButton("Load From URL", self)
		self.ldButton = QPushButton("Load Saved Read", self)
		self.brButton = QPushButton("Load Fic HTML", self)
		self.webBrButton = QPushButton("Browse AO3", self)
		self.FDButton = QPushButton("Fic Details", self)
		self.jButton = QPushButton("Jump", self)
		self.openFicPage = QPushButton("Open Fic Page", self)

		self.startText = "<h2>Welcome!</h2><p>Feel free to change your settings, or select a fic from AO3 to load. Check the help page for more details."

		#Jump box, type in a number to jump to that paragraph.
		self.jBox = QLineEdit()

		#File browse window
		self.brWindow = QFileDialog(self)

		#The web browser window.
		self.web = webView.webWin()

		#A combination box with all of the chapter titles.
		self.chapterBox = QComboBox(self)

		self.buttons = [self.lButton, self.rButton, self.sButton, self.wbButton, self.ldButton, self.brButton, self.webBrButton, self.FDButton,
		self.jButton, self.jBox, self.chapterBox, self.openFicPage]		

		#Displays current filepath or URL, I forget which one at which times.
		self.filebox = QLineEdit("Filepath or URL: ", self)

		self.theme = themeWin.themeWin(self.baseSave + "style.html")
		
		# self.setColour()
		self.font = QFont()
		self.font.setPointSize(24)
		self.font.setFamily("Times New Roman")

		#Loads all of the saved fic ini files within the default ini folder
		#And displays them to be chosen by the user.
		self.iniWin = findini.iniWin(self.defIniSave)

		#Displays the current fic details (Tags, fandom, etc)
		self.detWin = ficDeets.deetWin()

		#Detail class. Stores the text and chapter numbers.
		self.dts = detail()
		self.dts.tempimg = self.baseSave + "\\tempimg\\"

		#The fic window.
		self.html = QTextBrowser(self)
		self.getStyle()		

		#Window where the user can change their font. Uses the current font family
		#From the font object
		self.fWin = fontWin.fontWin(self.font.family(), str(self.font.pointSize()))

		#The top menu bar.
		self.setMenu()

		#The window where the user can enter an AO3 URL to load the fic from.
		self.urlWin = URLWin()

		#Centers the window on the screen. Will change to center on the currently
		#Open main window.
		self.urlWin.setGeometry(int((screenW - 400) / 2), int((screenH - 100) / 2), 400, 100)


		#Set all of the child widgets to NoFocus (All of the widgets initialized with self in params)
		self.setChildrenFocusPolicy(Qt.NoFocus)

		#Shift all of the UI settings for the widgets that require it.
		self.initUI()

		self.show()

		#Load the font ini file.
		self.loadFont()

		#Prepare a window for any needed alerts.
		self.alert = alertBox.alertWin()

	# def setColour(self):
	# 	bCol = QColor()
	# 	bCol.setRgb(30, 30, 30)
	# 	tCol = QColor()
	# 	tCol.setRgb(206, 206, 206)
	# 	# print("done")
	# 	self.html.setTextBackgroundColor(bCol)
	# 	self.html.setTextBackgroundColor(tCol)


	#If the default directories don't exist (likely at first startup), create them.
	def initDir(self):
		if not os.path.exists(self.baseSave):
			os.mkdir(self.baseSave)
		if not os.path.exists(self.defSave):
			os.mkdir(self.defSave)
		if not os.path.exists(self.defIniSave):
			os.mkdir(self.defIniSave)
		if not os.path.exists(self.baseSave + "\\tempimg\\"):
			os.mkdir(self.baseSave + "\\tempimg\\")
		if not os.path.exists(self.baseSave + "style.html"):
			with open(self.baseSave + "style.html", 'w') as file:
				file.write("<style>\nbody {\n\tbackground-color:#FFFFFF;\n\tcolor:#000000;\n\tmargin-top:40px;\n\tmargin-bottom:10px;\n\tmargin-right:40px;\n\tmargin-left:40px; \n}\n a { \n\tcolor:#CECECE;\n}\n</style>")	


	def getStyle(self):
		soup = BeautifulSoup(open(self.baseSave + "style.html", 'r'), 'html.parser')
		self.html.setStyleSheet("background-color:" + self.theme.bgColor.text() + ";" + "padding-top:30px;" + "padding-left:20px;" + "padding-right:20px;" + "color:" + self.theme.tColor.text() + ";")
		self.dts.style = str(soup.find("style"))
		# print(self.dts.style)
		self.html.setText(self.startText)


	def setMenu(self):
		openFont = QAction("&Font Settings...", self)
		openFont.setShortcut("Ctrl+Shift+F")
		openFont.setStatusTip("Edit font settings...")
		openFont.triggered.connect(self.changeFont)

		openSet = QAction("Settings...", self)
		openSet.setShortcut("Ctrl+Shift+S")
		openSet.setStatusTip("Edit settings...")
		openSet.triggered.connect(self.changeSettings)

		openTheme = QAction("Theme...", self)
		openTheme.setShortcut("Ctrl+Shift+T")
		openTheme.setStatusTip("Change theme...")
		openTheme.triggered.connect(self.changeTheme)

		menuBar = QMenuBar(self)
		fMenu = menuBar.addMenu("&Settings")
		fMenu.addAction(openFont)
		fMenu.addAction(openSet)
		fMenu.addAction(openTheme)

		self.layout.setMenuBar(menuBar)


	#Save all of the editable settings as an ini file in the root folder.
	def saveSettings(self):
		saver = configparser.ConfigParser()
		#Url saved as separate text file because encoding didn't work
		urlTxt = open(self.homePath + "\\save\\url.txt", 'w', encoding='utf-8')
		urlTxt.write(self.defURL)
		urlTxt.close()
		saver['Settings'] = {'ficsavepath' : self.defSave,
							 'inisavepath' : self.defIniSave,
							 'defaulturlpath' :  self.homePath + "\\save\\url.text",
							 'doasksave' : int(self.doAsk)}
		with open(self.homePath + '\\save\\settings.ini', 'w') as configfile:
			saver.write(configfile)


	#Load all of the editable settings from ini file in the root folder.
	def loadSettings(self):
		if(os.path.exists(self.homePath + '\\save\\settings.ini')):
			file = open(self.homePath + "\\save\\url.txt", 'r', encoding='utf-8')
			loader = configparser.ConfigParser()
			loader.read(self.homePath + '\\save\\settings.ini')
			self.defSave = loader['Settings']['ficsavepath']
			self.defIniSave = loader['Settings']['inisavepath']
			self.defURL = file.readlines()[0]
			self.doAsk = int(loader['Settings']['doasksave'])
			file.close()
		else:
			#Handle case where this was called and there is no ini file, therefore
			#Need to create it first.
			self.saveSettings()

	def changeTheme(self):
		self.theme.show()
		def onClose():
			self.getStyle()
			self.setText()
		self.theme.closed.connect(onClose)
		self.theme.apply.clicked.connect(onClose)

	#Change the ini file once the user clicks apply in the change settings window
	def changeSettings(self):
		self.disButtons()
		dims = self.findDims()
		self.setWin.updatePos(dims[0], dims[1])
		self.setWin.show()
		def onClose():
			self.setWin.close()
			#Pretty standard function to re-enable buttons after a popped up window disabled
			#them
			if(self.dts.filepath != ""):
				self.enButtons()
			else:
				self.noFicEnButtons()
		#Change all of the current settings and save it as an ini
		#adding the slash at the end if needed ensures that additions
		#later are very easy to add.
		def change():
			self.defIniSave = self.setWin.iniSavePath.text()			
			if(self.defIniSave[-1] != '/'):
				self.defIniSave += '/'
			self.defSave = self.setWin.ficSavePath.text()
			if(self.defSave[-1] != '/'):
				self.defSave += '/'
			self.defURL = self.setWin.defaultURL.text()
			self.doAsk = self.setWin.doAsk.isChecked()
			self.saveSettings()
			self.showAlert("Changes Applied!")
			self.alert.exButton.clicked.connect(onClose)
			self.iniWin.folder = self.defIniSave
			self.iniWin.loadFiles()
		self.setWin.apply.clicked.connect(change)
		self.setWin.closed.connect(onClose)

	#On close, close all possible open windows.
	def closeEvent(self, event):
		def recursiveClose (parentQWidget):
			for childQWidget in parentQWidget.findChildren(QWidget):
				recursiveClose(childQWidget)
				childQWidget.close()
		recursiveClose(self)
		self.saveFont()
		self.saveSettings()
		self.setWin.close()
		self.fWin.close()
		self.html.close()
		self.web.close()
		self.urlWin.close()
		self.detWin.close()

		#Change the properties of each widget
	def initUI(self):
		self.filebox.setReadOnly(True)
		self.lButton.setDisabled(True)
		self.rButton.setDisabled(True)
		self.sButton.setDisabled(True)
		self.chapterBox.setDisabled(True)
		self.jButton.setDisabled(True)
		self.FDButton.setDisabled(True)
		self.jBox.setDisabled(True)
		self.openFicPage.setDisabled(True)
		if(len(self.iniWin.iniList) <= 0):
			self.ldButton.setDisabled(True)
		else:
			self.ldButton.setDisabled(False)

		self.detWin.win.setFont(self.font)

		self.html.setFont(self.font)
		self.html.setReadOnly(True)

		self.iniWin.loadFiles()

		self.brWindow.setFileMode(QFileDialog.AnyFile)

		self.jBox.setFocusPolicy(Qt.ClickFocus)
		self.jBox.setPlaceholderText("Jump to Para #")
		self.jBox.setReadOnly(False)
		self.jBox.setFixedWidth(100)
		self.lButton.setFixedWidth(100)

		self.setGeometry(int((screenW - 900) / 2), int((screenH - 720) / 2), 900, 720)
		self.setWindowTitle("Paragraph Fic Reader Beta")
		self.initLayout()
		self.setLayout(self.layout)
		self.connect()

		#Set the focus policy on all of the children to nofocus, in order to capture keypresses properly
	def setChildrenFocusPolicy (self, policy):
		def recursiveSetChildFocusPolicy (parentQWidget):
			for childQWidget in parentQWidget.findChildren(QWidget):
				childQWidget.setFocusPolicy(policy)
				recursiveSetChildFocusPolicy(childQWidget)
		recursiveSetChildFocusPolicy(self)


		#Load all of the widgets into the layout 
	def initLayout(self):
		self.layout.addWidget(self.html, 1, 0, 2, -1)
		self.layout.addWidget(self.chapterBox, 0, 0, 1, 3)
		self.layout.addWidget(self.FDButton, 0, 5, 1, 1)		
		self.layout.addWidget(self.paraCount, 0, 6, 1, 1)	
		self.layout.addWidget(self.filebox, 3, 0, 1, 3)
		self.layout.addWidget(self.brButton, 3, 4, 1, 1)
		self.layout.addWidget(self.wbButton, 3, 6, 1, 1)
		self.layout.addWidget(self.webBrButton, 3, 5, 1, 1)	
		self.layout.addWidget(self.lButton, 4, 2, 1, 1)
		self.layout.addWidget(self.rButton, 4, 3, 1, 1)
		self.layout.addWidget(self.sButton, 4, 5, 1, 1)
		self.layout.addWidget(self.ldButton, 4, 6, 1, 1)
		self.layout.addWidget(self.jButton, 0, 4, 1, 1)
		self.layout.addWidget(self.jBox, 0, 3, 1, 1)
		self.layout.addWidget(self.openFicPage, 4, 4, 1, 1)
		# self.layout.setColumnStretch(3, 2)

		#Connect any buttons to functions
		#Connect the buttons to their respective functions
	def connect(self):
		self.brButton.clicked.connect(self.ldFile)
		self.lButton.clicked.connect(self.left)
		self.rButton.clicked.connect(self.right)
		self.wbButton.clicked.connect(self.getURL)
		self.chapterBox.activated.connect(self.chapUpdate)
		self.webBrButton.clicked.connect(self.webGet)
		self.web.subButton.clicked.connect(self.retWeb)
		self.FDButton.clicked.connect(self.showDet)
		self.sButton.clicked.connect(self.saveFic)
		self.ldButton.clicked.connect(self.loadFicWin)
		self.jButton.clicked.connect(self.jump)
		self.jBox.returnPressed.connect(self.jump)
		self.openFicPage.clicked.connect(self.openAO3Page)


	def noFicEnButtons(self):
		self.brButton.setDisabled(False)
		self.webBrButton.setDisabled(False)
		self.wbButton.setDisabled(False)
		#Only enable the load button if there is something to load.
		if(len(self.iniWin.dirs) <= 0):
			self.ldButton.setDisabled(True)
		else:
			self.ldButton.setDisabled(False)

	def showAlert(self, text):
		self.alert.alert.setText(text)
		# self.alert.updateDim()
		self.alert.updatePos(self.findDims()[0], self.findDims()[1])
		self.alert.show()

	def jump(self):
		inBox = self.jBox.text().strip()
		def isInt(s):
			try:
				int(s)
				return True
			except ValueError:
				return False
		if(isInt(inBox)):
			inBox = int(inBox)
			if(inBox > 0 and inBox <= len(self.dts.chapters[self.dts.chapter][2])):
				self.dts.currPages[self.dts.chapter] = inBox - 1
				self.setText()
				self.setPara()
				self.jBox.setText("")
			else:
				self.showAlert("Alert: Input was outside of paragraph range.")
				self.disButtons()
				def onClose():
					self.enButtons()
					self.jBox.setText("")
				self.alert.closed.connect(onClose)
		else:
			self.showAlert("Alert: Input was not a number.")
			self.disButtons()
			def onClose():
				self.enButtons()
				self.jBox.setText("")
			self.alert.closed.connect(onClose)

	def disButtons(self):
		for x in self.buttons:
			x.setDisabled(True)

	def enButtons(self):

		for x in self.buttons:
			x.setDisabled(False)
		if(self.dts.filepath == ""):
			self.noFicEnButtons()
		if(len(self.iniWin.dirs) <= 0):
			self.ldButton.setDisabled(True)	
		if(self.windowTitle() == "Paragraph Fic Reader Beta"):
			self.sButton.setDisabled(True)

	def findDims(self):
		currentPos = [self.pos().x(), self.pos().y()]
		currentDim = [self.geometry().width(), self.geometry().height()]
		return [currentPos, currentDim]		

	def changeFont(self):
		dims = self.findDims()
		self.fWin.updatePos(dims[0], dims[1])
		self.fWin.show()
		self.disButtons()
		def setF():
			self.font.setFamily(self.fWin.fontBox.currentText())
			self.font.setPointSize(int(self.fWin.sizeBox.currentText()))
			self.html.setFont(self.font)
			if(self.dts.filepath != ""):
				self.enButtons()
			else:
				self.noFicEnButtons()
		self.fWin.closed.connect(setF)

	def saveFont(self):
		saver = configparser.ConfigParser()
		saver['FontDetails'] = {'Size' : str(self.font.pointSize()),
								'Name' : self.font.family()}
		with open(self.homePath + '\\save\\font.ini', 'w') as configfile:
			saver.write(configfile)

	def loadFont(self):
		if(os.path.exists(self.homePath + '\\save\\font.ini')):
			try:
				loader = configparser.ConfigParser()
				loader.read(self.homePath + '\\save\\font.ini')
				test = int(loader['FontDetails']['size'])
				# self.font.setPointSize(int(loader['FontDetails']['size']))
				self.font.setFamily(loader['FontDetails']['name'])
				self.html.setFont(self.font)
			except:
				print("Error in INI read")
		else:
			self.changeFont()
			self.saveFont()

			

	def showDet(self):
		dims = self.findDims()
		self.detWin.updatePos(dims[0], dims[1])		
		self.detWin.show()

	def webGet(self):
		self.disButtons()
		dims = self.findDims()
		self.web.updateDim()
		self.web.updatePos(dims[0], dims[1])			
		# self.web.web.load(QUrl("https://archiveofourown.org/media"))	
		def onClose():
			if(self.dts.filepath != ""):
				self.enButtons()
			else:
				self.noFicEnButtons()
		self.web.closed.connect(onClose)
		self.web.setURL(self.defURL)
		self.web.show()

	def retWeb(self):
		self.web.subButton.setDisabled(True)
		self.subURL(self.web.dispURL.text())
		if(self.filebox.text() != "Filepath:" and (self.filebox.text() == self.web.dispURL.text())):
			self.web.close()
		else:
			self.web.subButton.setDisabled(False)

		#Get the HTML filename from the user through browse
	def get_file(self):
		file = QFileDialog.getOpenFileName(self.brWindow, "", "", "Text files (*.txt, *.html)")	
		return file

		#Load chapterbox with chapter titles
		#Load the current chapter page list with zeroes, initialization
	def ldCBox(self):
		for x in range(0, len(chapters)):
			self.chapterBox.addItem(dts.chapters[x][1])
			dts.currPages.append(0)

		#Sets the html to what it should be, after an update
		#Set the paragraph text to what the dts class says is the current one.
	def setText(self):
		#This is stupid.
		if(self.dts.filepath != ""):
			self.html.setHtml(self.dts.pageText())
			# print(self.dts.pageText())
		else:
			self.html.setHtml(self.dts.pre + self.dts.style + self.startText + self.dts.post)
		#Updates the paragraph label to whatever is in the dts class
	def setPara(self):
		self.dts.setParaCount()
		self.paraCount.setText(self.dts.paraCountstr)

		#Go to the previous paragraph (if it exists)
	def left(self):
		if(self.dts.currPages[self.dts.chapter] > 0):
			self.dts.prevP()
			self.setPara()
			self.setText()
			if(self.dts.currPages[self.dts.chapter] == 0):
				self.lButton.setDisabled(True)
		self.rButton.setDisabled(False)
		# self.setFocus()
		#Go the the next paragraph (if it exists)
	def right(self):
		if(self.dts.currPages[self.dts.chapter] < len(self.dts.chapters[self.dts.chapter][2]) - 1):
			self.dts.nextP()
			self.setPara()
			self.setText()
			if(self.dts.currPages[self.dts.chapter] == len(self.dts.chapters[self.dts.chapter][2]) - 1):
				self.rButton.setDisabled(True)
			
		self.lButton.setDisabled(False)

		#Handle left and right key presses
	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Left:
			if(self.dts.filepath != ""):
				self.left()
		if event.key() == Qt.Key_Right:
			if(self.dts.filepath != ""):
				self.right()
		if event.key() == Qt.Key_Down:
			#Scroll Down
			self.html.verticalScrollBar().setValue(int(self.html.verticalScrollBar().value() + 1.5 * self.font.pointSize()))
		if event.key() == Qt.Key_Up:
			#Scroll Up
			self.html.verticalScrollBar().setValue((self.html.verticalScrollBar().value() - 1.5 * self.font.pointSize()))


	def loadChapBox(self):
		for x in range(0, len(self.dts.chapters)):
			self.chapterBox.addItem(str(x + 1) + ". " + self.dts.chapters[x][1])

	def chapUpdate(self):
		self.dts.chapter = self.chapterBox.currentIndex()
		self.setText()
		self.setPara()

	def getURL(self):
		self.disButtons()		
		def passURL():
			self.urlWin.tempEnt.setDisabled(True)
			self.subURL(self.urlWin.tempBox.text())
			self.urlWin.tempEnt.setDisabled(False)
		def onClose():
			if(self.dts.filepath != ""):
				self.enButtons()
			else:
				self.noFicEnButtons()
		self.urlWin.tempEnt.clicked.connect(passURL)
		self.urlWin.tempBox.returnPressed.connect(passURL)
		self.urlWin.closed.connect(onClose)
		dims = self.findDims()
		self.urlWin.updatePos(dims[0], dims[1])
		self.urlWin.show()		
		self.urlWin.show()

	def subURL(self, url):
		self.dts.url = url
		temp = HTML.importHTML(url, self.doAsk, self.defSave)
		if(temp != "False"):
			self.urlWin.tempBox.setText("")
			self.dts.filepath = temp[0]
			self.dts.title = temp[1]
			self.detWin.win.setText(temp[2])
			self.dts.fandom = temp[3]
			self.setWindowTitle(self.dts.title)
			self.chapterBox.clear()	
			self.dts.pFile(self.height(), self.width())
			self.initAfterFile()
			self.urlWin.close()

	def initAfterFile(self):
		self.setText()
		self.setPara()
		self.loadChapBox()		
		self.rButton.setDisabled(False)
		self.chapterBox.setDisabled(False)
		self.sButton.setDisabled(False)
		self.filebox.setText(self.dts.url)

	def ldIniHelper(self, file):
		temp = findTags(file)
		self.chapterBox.clear()		
		self.dts.filepath = file
		self.dts.title = temp[1]
		self.dts.fandom = temp[2]
		self.dts.url = temp[3]
		self.dts.pFile(self.height(), self.width())
		self.detWin.win.setText(temp[0])
		self.setWindowTitle(temp[1])
		self.initAfterFile()	

		#Load html file 
	def ldFile(self):
		self.disButtons()
		file = self.get_file()
		file = file[0]
		
		if(file != ""):
			try:
				temp = findTags(file)
				self.chapterBox.clear()
				self.dts.filepath = file
				self.dts.title = temp[1]
				self.dts.pFile(self.height(), self.width())
				self.detWin.win.setText(temp[0])
				self.setWindowTitle(temp[1])
				self.dts.fandom = temp[2]
				self.dts.url = temp[3]
				self.initAfterFile()
				if(self.dts.filepath != ""):
					self.enButtons()
				else:
					self.noFicEnButtons()

			except AttributeError as err:
				print(err)
				self.dts.filePath = ""
				self.showAlert("Alert: File Read Error. Please download AO3 files by the Download->HTML button on the fic page.")
				self.disButtons()
				def onClose():
					if(self.dts.filepath != ""):
						self.enButtons()
					else:
						self.noFicEnButtons()				

				self.alert.closed.connect(onClose)
		else:
			if(self.dts.filepath != ""):
				self.enButtons()
			else:
				self.noFicEnButtons()


	def saveFic(self):

		#Need to save:
		#Chapter Pages, somehow
		#Just the html, as that can be passed to the ldFile funct
		#Current chapter
		lisPages = self.dts.pageString()
		save = configparser.ConfigParser()
		save['FicDetails'] = {'Filepath' : self.dts.filepath,
								'Pages' : lisPages,
								'CurrCh' : self.dts.chapter,
								'Title' : str(self.dts.title),
								'Url' : self.dts.url,
								'Fandom' : str(self.dts.fandom)}
		with open(self.defIniSave + self.dts.title + ".ini", 'w') as configfile:
			save.write(configfile)
		if(len(self.iniWin.dirs) <= 0):
			self.iniWin.loadFiles()
			self.enButtons()

	def loadFic(self, file):
		load = configparser.ConfigParser()
		load.read(file)
		try:
			if(os.path.exists(load['FicDetails']['filepath'])):
				self.ldIniHelper(load['FicDetails']['filepath'])
				self.dts.currPages.clear()
				self.dts.chapter = int(load['FicDetails']['currch'])
				temp = re.findall(r'\d+', load['FicDetails']['pages'])
				for x in temp:
					self.dts.currPages.append(int(x))
				self.setPara()
				self.setText()
				self.chapterBox.setCurrentIndex(self.dts.chapter)
		except:
			print("Error")

	def loadFicWin(self):
		self.disButtons()	
		def onClose():
			if(self.dts.filepath != ""):
				self.enButtons()
			else:
				self.brButton.setDisabled(False)
				self.wbButton.setDisabled(False)
				self.webBrButton.setDisabled(False)
				self.ldButton.setDisabled(False)
		self.iniWin.folder = self.defIniSave + "/"
		self.iniWin.loadFiles()
		self.iniWin.closed.connect(onClose)
		def onRet():
			self.loadFic(self.iniWin.dirs[self.iniWin.iniList.currentIndex()])
			self.enButtons()
		self.iniWin.retSig.connect(onRet)

		dims = self.findDims()
		self.iniWin.updatePos(dims[0], dims[1])
		self.iniWin.show()	

	def openAO3Page(self):
		self.disButtons()
		# self.web.web.load(QUrl("https://archiveofourown.org/media"))	
		def onClose():
				self.enButtons()
		self.web.closed.connect(onClose)
		self.web.setURL(self.dts.url)
		self.web.show()


if __name__ == "__main__":
	app = ApplicationContext()	
	test = window()

	# test.show()
	exit_code = app.app.exec_()
	sys.exit(exit_code)