#
# Wordless: Dialog
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Wordless_Dialog_Info(QDialog):
	def __init__(self, main, title):
		super().__init__(main)

		self.setWindowTitle(title)
		self.setWindowIcon(QIcon('images/wordless_icon.png'))

		self.wrapper_info = QWidget(self)

		self.button_ok = QPushButton(self.tr('OK'), self)

		self.button_ok.clicked.connect(self.accept)

		self.setLayout(QGridLayout())
		self.layout().addWidget(self.wrapper_info, 0, 0)
		self.layout().addWidget(self.button_ok, 1, 0, Qt.AlignRight)
