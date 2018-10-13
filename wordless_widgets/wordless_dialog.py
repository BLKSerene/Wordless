#
# Wordless: Dialogs
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

import platform

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

def wordless_message_jre_not_installed(main):
	sys_bit = platform.architecture()[0][:2]
	if sys_bit == '32':
		sys_bit_x = 'x86'
	else:
		sys_bit_x = 'x64'

	QMessageBox.information(main,
                            main.tr('Java Runtime Environment Not Installed'),
                            main.tr(f'''
                            			<p>The HanLP library requires Java Runtime Environment (JRE) to be installed on your computer.</p>
                            			<p>You can download the latest version of JRE here: <a href="https://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html">https://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html</a>.</p>
                            			<p>After JRE is properly installed, please try again.</p>
                            			<p>Note: You are running the {sys_bit}-bit version of Wordless, so you should install the {sys_bit_x} version of JRE!</p>
                            		'''),
                            QMessageBox.Ok)

def wordless_message_empty_search_term(main):
    QMessageBox.warning(main,
                        main.tr('Empty Search Term'),
                        main.tr('Please enter your search term(s) first!'),
                        QMessageBox.Ok)

def wordless_message_empty_results_table(main):
    QMessageBox.information(main,
                            main.tr('No Search Results'),
                            main.tr('There is nothing to be shown in the table.<br>You might want to change your search term(s) and/or your settings, and then try again.'),
                            QMessageBox.Ok)

def wordless_message_empty_results_plot(main):
    QMessageBox.information(main,
                            main.tr('No Search Results'),
                            main.tr('There is nothing to be shown in the figure.<br>You might want to change your search term(s) and/or your settings, and then try again.'),
                            QMessageBox.Ok)