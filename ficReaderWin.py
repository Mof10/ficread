from PyQt5.QtWidgets import QTextBrowser

import parent

class html(QTextBrowser):

	def __init__(self, dts, font):
		super().__init__()
		self.dts = dts
		self.setFont(font)

	def left()