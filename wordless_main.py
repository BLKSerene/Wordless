#
# Wordless: An integrated tool for language & translation studies.
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

import pickle
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_widgets import *
from wordless_utils import *

import init_settings
import wordless_settings
import wordless_files
import tab_overview
import tab_concordancer
import tab_wordlist
import tab_ngram
import tab_collocation
import tab_semantics

class Wordless_Acknowledgements(wordless_dialog.Wordless_Dialog_Info):
    def __init__(self, main):
        def table_item_clicked(item):
            table_acknowledgements.cellWidget(item.row(), item.column())

        super().__init__(main, main.tr('Acknlwdgements'))

        self.setFixedSize(850, 500)

        label_acknowledgements = QLabel(self.tr('Many thanks to the following open-source projects on which Wordless is built on:'), self)

        table_acknowledgements = wordless_table.Wordless_Table(self,
                                                               headers = [
                                                                   self.tr('Name'),
                                                                   self.tr('Version'),
                                                                   self.tr('Author(s)'),
                                                                   self.tr('Contact'),
                                                                   self.tr('License')
                                                               ],
                                                               cols_stretch = [
                                                                   self.tr('Contact')
                                                               ])

        table_acknowledgements.setSelectionMode(QAbstractItemView.NoSelection)

        table_acknowledgements.itemClicked.connect(table_item_clicked)

        table_acknowledgements.button_export_selected.hide()
        table_acknowledgements.button_export_all.hide()
        table_acknowledgements.button_clear.hide()

        table_acknowledgements.setRowCount(16)

        table_acknowledgements.setCellWidget(0, 0, QLabel('<a href="https://www.python.org/">Python</a>', self))
        table_acknowledgements.setCellWidget(0, 1, QLabel('3.6.6', self))
        table_acknowledgements.setCellWidget(0, 2, QLabel('Python Software Foundation', self))
        table_acknowledgements.setCellWidget(0, 3, QLabel('<a href="https://www.python.org/psf/">https://www.python.org/psf/</a>', self))
        table_acknowledgements.setCellWidget(0, 4, QLabel('<a href="https://docs.python.org/3.6/license.html">PSF</a>', self))

        table_acknowledgements.setCellWidget(1, 0, QLabel('<a href="https://www.crummy.com/software/BeautifulSoup/">Beautiful Soup</a>', self))
        table_acknowledgements.setCellWidget(1, 1, QLabel('4.6.3', self))
        table_acknowledgements.setCellWidget(1, 2, QLabel('Leonard Richardson', self))
        table_acknowledgements.setCellWidget(1, 3, QLabel('<a href="https://www.crummy.com/self/contact.html">https://www.crummy.com/self/contact.html</a>', self))
        table_acknowledgements.setCellWidget(1, 4, QLabel('<a href="https://bazaar.launchpad.net/~leonardr/beautifulsoup/bs4/view/head:/LICENSE">MIT</a>', self))

        table_acknowledgements.setCellWidget(2, 0, QLabel('<a href="https://github.com/michmech/lemmatization-lists">Lemmatization Lists</a>', self))
        table_acknowledgements.setCellWidget(2, 1, QLabel('', self))
        table_acknowledgements.setCellWidget(2, 2, QLabel('Michal Boleslav Měchura', self))
        table_acknowledgements.setCellWidget(2, 3, QLabel('<a href="http://www.lexiconista.com/en/#contact">http://www.lexiconista.com/en/#contact</a>', self))
        table_acknowledgements.setCellWidget(2, 4, QLabel('<a href="https://github.com/michmech/lemmatization-lists/blob/master/LICENCE">ODbL</a>', self))

        table_acknowledgements.setCellWidget(3, 0, QLabel('<a href="https://matplotlib.org/">Matplotlib</a>', self))
        table_acknowledgements.setCellWidget(3, 1, QLabel('3.0.0', self))
        table_acknowledgements.setCellWidget(3, 2, QLabel('Matplotlib Development Team', self))
        table_acknowledgements.setCellWidget(3, 3, QLabel('<a href="https://github.com/matplotlib/matplotlib#contact">https://github.com/matplotlib/matplotlib#contact</a>', self))
        table_acknowledgements.setCellWidget(3, 4, QLabel('<a href="https://matplotlib.org/users/license.html">Matplotlib</a>', self))

        table_acknowledgements.setCellWidget(4, 0, QLabel('<a href="http://www.nltk.org/">NLTK</a>', self))
        table_acknowledgements.setCellWidget(4, 1, QLabel('3.3', self))
        table_acknowledgements.setCellWidget(4, 2, QLabel('NLTK Project', self))
        table_acknowledgements.setCellWidget(4, 3, QLabel('<a href="http://www.nltk.org/contribute.html">http://www.nltk.org/contribute.html</a>', self))
        table_acknowledgements.setCellWidget(4, 4, QLabel('<a href="https://github.com/nltk/nltk/blob/develop/LICENSE.txt">Apache-2.0</a></td>', self))

        table_acknowledgements.setCellWidget(5, 0, QLabel('<a href="http://networkx.github.io/">NetworkX</a>', self))
        table_acknowledgements.setCellWidget(5, 1, QLabel('2.1', self))
        table_acknowledgements.setCellWidget(5, 2, QLabel('Aric Hagberg<br>Dan Schult<br>Pieter Swart', self))
        table_acknowledgements.setCellWidget(5, 3, QLabel('hagberg@lanl.gov<br>dschult@colgate.edu<br>swart@lanl.gov', self))
        table_acknowledgements.setCellWidget(5, 4, QLabel('<a href="https://github.com/networkx/networkx/blob/master/LICENSE.txt">BSD-3-Clause</a>', self))
        
        table_acknowledgements.setCellWidget(6, 0, QLabel('<a href="http://www.numpy.org/">NumPy</a>', self))
        table_acknowledgements.setCellWidget(6, 1, QLabel('1.15.2', self))
        table_acknowledgements.setCellWidget(6, 2, QLabel('Aric Hagberg<br>Dan Schult<br>Pieter Swart', self))
        table_acknowledgements.setCellWidget(6, 3, QLabel('hagberg@lanl.gov<br>dschult@colgate.edu<br>swart@lanl.gov', self))
        table_acknowledgements.setCellWidget(6, 4, QLabel('<a href="https://github.com/networkx/networkx/blob/master/LICENSE.txt">BSD-3-Clause</a>', self))

        table_acknowledgements.setCellWidget(7, 0, QLabel('<a href="https://www.riverbankcomputing.com/software/pyqt/intro">PyQt</a>', self))
        table_acknowledgements.setCellWidget(7, 1, QLabel('5.11.2', self))
        table_acknowledgements.setCellWidget(7, 2, QLabel('Riverbank Computing Limited', self))
        table_acknowledgements.setCellWidget(7, 3, QLabel('info@riverbankcomputing.com', self))
        table_acknowledgements.setCellWidget(7, 4, QLabel('<a href="http://pyqt.sourceforge.net/Docs/  PyQt5/introduction.html#license">GPL-3.0</a>', self))

        table_acknowledgements.setCellWidget(8, 0, QLabel('<a href="https://github.com/stopwords-iso/stopwords-iso">Stopwords ISO</a>', self))
        table_acknowledgements.setCellWidget(8, 1, QLabel('0.4.0', self))
        table_acknowledgements.setCellWidget(8, 2, QLabel('Gene Diaz', self))
        table_acknowledgements.setCellWidget(8, 3, QLabel('genediazjr@gmail.com', self))
        table_acknowledgements.setCellWidget(8, 4, QLabel('<a href="https://github.com/stopwords-iso/stopwords-iso/blob/master/LICENSE">MIT</a>', self))

        table_acknowledgements.setCellWidget(9, 0, QLabel('<a href="https://github.com/chardet/chardet">chardet</a>', self))
        table_acknowledgements.setCellWidget(9, 1, QLabel('3.0.4', self))
        table_acknowledgements.setCellWidget(9, 2, QLabel('Daniel Blanchard', self))
        table_acknowledgements.setCellWidget(9, 3, QLabel('dan.blanchard@gmail.com', self))
        table_acknowledgements.setCellWidget(9, 4, QLabel('<a href="https://github.com/chardet/chardet/blob/master/LICENSE">LGPL-2.1</a>', self))
        
        table_acknowledgements.setCellWidget(10, 0, QLabel('<a href="https://lexically.net/downloads/BNC_wordlists/e_lemma.txt">e_lemma.txt</a>', self))
        table_acknowledgements.setCellWidget(10, 1, QLabel('2', self))
        table_acknowledgements.setCellWidget(10, 2, QLabel('Yasumasa Someya (染谷泰正)', self))
        table_acknowledgements.setCellWidget(10, 3, QLabel('<a href="http://www.someya-net.com/index2.html">http://www.someya-net.com/index2.html</a>', self))
        table_acknowledgements.setCellWidget(10, 4, QLabel('<a href="https://lexically.net/downloads/BNC_wordlists/e_lemma.txt">Free to use for any research;<br>and/or educational purposes.</a>', self))

        table_acknowledgements.setCellWidget(11, 0, QLabel('<a href="https://github.com/Mimino666/langdetect">langdetect</a>', self))
        table_acknowledgements.setCellWidget(11, 1, QLabel('1.0.7', self))
        table_acknowledgements.setCellWidget(11, 2, QLabel('Michal Mimino Danilak', self))
        table_acknowledgements.setCellWidget(11, 3, QLabel('michal.danilak@gmail.com', self))
        table_acknowledgements.setCellWidget(11, 4, QLabel('<a href="https://github.com/Mimino666/langdetect/blob/master/LICENSE">Apache-2.0</a>', self))

        table_acknowledgements.setCellWidget(12, 0, QLabel('<a href="https://lxml.de/">lxml</a>', self))
        table_acknowledgements.setCellWidget(12, 1, QLabel('4.2.4', self))
        table_acknowledgements.setCellWidget(12, 2, QLabel('Stefan Behnel', self))
        table_acknowledgements.setCellWidget(12, 3, QLabel('<a href="http://consulting.behnel.de">http://consulting.behnel.de</a>', self))
        table_acknowledgements.setCellWidget(12, 4, QLabel('<a href="https://github.com/lxml/lxml/blob/master/doc/licenses/  BSD.txt">BSD-3-Clause</a>', self))

        table_acknowledgements.setCellWidget(13, 0, QLabel('<a href="https://openpyxl.readthedocs.io/en/stable/#">openpyxl</a>', self))
        table_acknowledgements.setCellWidget(13, 1, QLabel('2.5.5', self))
        table_acknowledgements.setCellWidget(13, 2, QLabel('Eric Gazoni<br>Charlie Clark', self))
        table_acknowledgements.setCellWidget(13, 3, QLabel('<br>charlie.clark@clark-consulting.eu', self))
        table_acknowledgements.setCellWidget(13, 4, QLabel('<a href="https://bitbucket.org/openpyxl/openpyxl/src/5983d4ba5c18b85171185e8b1ca136876ec52864/LICENCE.rst?at=default&fileviewer=file-view-default">MIT</a>', self))

        table_acknowledgements.setCellWidget(14, 0, QLabel('<a href="https://github.com/6/stopwords-json">stopwords-json</a>', self))
        table_acknowledgements.setCellWidget(14, 1, QLabel('', self))
        table_acknowledgements.setCellWidget(14, 2, QLabel('Peter Graham', self))
        table_acknowledgements.setCellWidget(14, 3, QLabel('pete@gigadrill.com', self))
        table_acknowledgements.setCellWidget(14, 4, QLabel('<a href="https://bitbucket.org/openpyxl/openpyxl/src/5983d4ba5c18b85171185e8b1ca1368  76ec52864/LICENCE.rst?at=default&fileviewer=file-view-default">MIT</a>', self))

        table_acknowledgements.setCellWidget(15, 0, QLabel('<a href="https://github.com/fxsjy/jieba">“结巴”中文分词</a>', self))
        table_acknowledgements.setCellWidget(15, 1, QLabel('0.39', self))
        table_acknowledgements.setCellWidget(15, 2, QLabel('Sun Junyi', self))
        table_acknowledgements.setCellWidget(15, 3, QLabel('ccnusjy@gmail.com', self))
        table_acknowledgements.setCellWidget(15, 4, QLabel('<a href="https://github.com/fxsjy/jieba/blob/master/LICENSE">MIT</a>', self))

        self.wrapper_info.setLayout(QGridLayout())
        self.wrapper_info.layout().addWidget(label_acknowledgements, 0, 0)
        self.wrapper_info.layout().addWidget(table_acknowledgements, 1, 0)

class Wordless_Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(self.tr('Wordless Version 1.0'))
        self.setWindowIcon(QIcon('images/wordless_icon.png'))

        init_settings.init_settings(self)
        self.wordless_settings = wordless_settings.Wordless_Settings(self)

        self.init_central_widget()

        self.init_menu()

        self.status_bar = self.statusBar()
        self.status_bar.showMessage(self.tr('Ready!'))

        self.setStyleSheet('* {font-family: Arial, sans-serif; color: #292929; font-size: 12px}')

    def closeEvent(self, event):
        reply = QMessageBox.question(self,
                                     self.tr('Exit Confirmation'),
                                     self.tr('Do you really want to quit?'),
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Reset some settings
            self.settings_custom['file']['files_closed'].clear()

            with open('wordless_settings.pkl', 'wb') as f:
                pickle.dump(self.settings_custom, f)

            event.accept()
        else:
            event.ignore()

    def init_menu(self):
        def show_status_bar():
            if self.status_bar.isVisible():
                self.status_bar.hide()
            else:
                self.status_bar.show()

        def need_help():
            message_box = QMessageBox(QMessageBox.Information,
                                      self.tr('Need Help?'),
                                      self.tr(self.style_dialog +
                                              '''
                                              <body>
                                                <p>If you need any further information or encounter any problems while using Wordless, please feel free to contact me, and I will reply as soon as possible.</p>
                                                <p>Home Page: <a href="https://github.com/BLKSerene/Wordless">https://github.com/BLKSerene/Wordless</p>
                                                <p>Email: blkserene@gmail.com</p>
                                              </body>
                                              '''),
                                      QMessageBox.Ok,
                                      self)

            message_box.setTextInteractionFlags(Qt.TextSelectableByMouse)

            message_box.exec_()

        def feedback():
            QMessageBox.information(self,
                                    self.tr('Feedback'),
                                    self.tr(self.style_dialog +
                                            '''
                                            <body>
                                              <p>If you find any bugs while using Wordless, you might want to report it via Github\'s bug tracker <a href="https://github.com/BLKSerene/Wordless/issues">Issues</a>.</p>
                                              <p>Feedback, enhancement proposals, feature requests and code contribution are also welcomed.</p>
                                            </body>
                                            '''),
                                    QMessageBox.Ok)

        def citation():
            def citation_sys_changed():
                if combo_box_citation_sys.currentIndex() == 0:
                    text_edit_citation.setHtml('Ye Lei. Wordless, version 1.0, 2018, https://github.com/BLKSerene/Wordless.')
                elif combo_box_citation_sys.currentIndex() == 1:
                    text_edit_citation.setHtml('Ye, L. (2018) Wordless (Version 1.0) [Computer Software]. Retrieved from https://github.com/BLKSerene/Wordless')
                elif combo_box_citation_sys.currentIndex() == 2:
                    text_edit_citation.setHtml('Ye, Lei. <i>Wordless</i> (Version 1.0). Windows. Shanghai: Ye Lei, 2018.')
                elif combo_box_citation_sys.currentIndex() == 3:
                    text_edit_citation.setHtml('叶磊. Wordless version 1.0[CP]. (2018). https://github.com/BLKSerene/Wordless.')

                if combo_box_citation_sys.currentIndex() <= 2:
                    text_edit_citation.setFont(QFont('Times New Roman', 12))
                elif combo_box_citation_sys.currentIndex() == 3:
                    text_edit_citation.setFont(QFont('宋体', 12))

            def copy():
                text_edit_citation.setFocus()
                text_edit_citation.selectAll()
                text_edit_citation.copy()

            dialog_citation = QDialog(self)

            dialog_citation.setWindowTitle(self.tr('Citation'))

            dialog_citation.setFixedSize(dialog_citation.sizeHint().width(), 160)

            label_citation = QLabel(self.tr('If you publish work that uses Wordless, please cite Wordless as follows.'), self)
            label_citation_sys = QLabel(self.tr('Citation System:'), self)
            combo_box_citation_sys = QComboBox(self)
            text_edit_citation = QTextEdit(self)

            button_copy = QPushButton(self.tr('Copy'), self)
            button_close = QPushButton(self.tr('Close'), self)

            combo_box_citation_sys.addItems([
                                                 self.tr('MLA (8th Edition)'),
                                                 self.tr('APA (6th Edition)'),
                                                 self.tr('Chicago (17th Edition)'),
                                                 self.tr('GB (GB/T 7714—2015)')
                                            ])

            button_copy.setFixedWidth(100)
            button_close.setFixedWidth(100)

            text_edit_citation.setReadOnly(True)

            combo_box_citation_sys.currentTextChanged.connect(citation_sys_changed)
            button_copy.clicked.connect(copy)
            button_close.clicked.connect(dialog_citation.accept)

            layout_citation = QGridLayout()
            layout_citation.addWidget(label_citation, 0, 0, 1, 2)
            layout_citation.addWidget(label_citation_sys, 1, 0)
            layout_citation.addWidget(combo_box_citation_sys, 1, 1)
            layout_citation.addWidget(text_edit_citation, 2, 0, 1, 2)
            layout_citation.addWidget(button_copy, 3, 0, Qt.AlignHCenter)
            layout_citation.addWidget(button_close, 3, 1, Qt.AlignHCenter)

            dialog_citation.setLayout(layout_citation)

            citation_sys_changed()

            dialog_citation.exec_()

        def acknowledgements():
            dialog_acknowledgements = Wordless_Acknowledgements(self)

            dialog_acknowledgements.exec()

        def about_wordless():
            QMessageBox.about(self,
                              self.tr('About Wordless'),
                              self.tr(self.style_dialog +
                                      '''
                                      <body style="text-align: center">
                                        <h1>Wordless Version 1.0</h1>
                                        <p>An integrated tool for language & translation studies.</p>
                                        <p style="margin: 0;">Designed and Developed by Ye Lei (叶磊)</p>
                                        <hr>
                                        <p>Licensed under GPL Version 3.0</p>
                                        <p>Copyright (C) 2018 Ye Lei</p>
                                      </body>'''))

        menu = self.menuBar()
        menu_file = menu.addMenu(self.tr('File'))
        menu_pref = menu.addMenu(self.tr('Preferences'))
        menu_help = menu.addMenu(self.tr('Help'))

        action_open_files = QAction(self.tr('Open File(s)...'), self)
        action_open_files.setStatusTip(self.tr('Open file(s)'))
        action_open_files.triggered.connect(self.open_files)

        action_open_dir = QAction(self.tr('Open Folder...'), self)
        action_open_dir.setStatusTip(self.tr('Open a folder'))
        action_open_dir.triggered.connect(self.open_dir)

        action_close_selected = QAction(self.tr('Close Selected File(s)'), self)
        action_close_selected.setStatusTip(self.tr('Close selected file(s)'))
        action_close_selected.triggered.connect(self.close_selected)

        action_close_all = QAction(self.tr('Close All Files'), self)
        action_close_all.setStatusTip(self.tr('Close all files'))
        action_close_all.triggered.connect(self.close_all)

        self.action_reopen = QAction(self.tr('Reopen Closed File(s)'), self)
        self.action_reopen.setStatusTip(self.tr('Reopen closed file(s)'))
        self.action_reopen.triggered.connect(self.reopen)

        action_exit = QAction(self.tr('Exit...'), self)
        action_exit.setStatusTip(self.tr('Exit the program'))
        action_exit.triggered.connect(self.close)

        self.action_reopen.setEnabled(False)

        menu_file.addAction(action_open_files)
        menu_file.addAction(action_open_dir)
        menu_file.addSeparator()
        menu_file.addAction(action_close_selected)
        menu_file.addAction(action_close_all)
        menu_file.addSeparator()
        menu_file.addAction(self.action_reopen)
        menu_file.addSeparator()
        menu_file.addAction(action_exit)

        action_language = QAction(self.tr('Language'), self)
        action_language.setStatusTip(self.tr('Change display language'))

        action_settings = QAction(self.tr('Settings'), self)
        action_settings.setStatusTip(self.tr('Change settings'))
        action_settings.triggered.connect(self.wordless_settings.load)

        action_show_status_bar = QAction(self.tr('Show Status Bar'), self, checkable = True)
        action_show_status_bar.setChecked(True)
        action_show_status_bar.setStatusTip(self.tr('Show/Hide the status bar'))
        action_show_status_bar.triggered.connect(lambda: show_status_bar(self))

        menu_pref.addAction(action_settings)
        menu_pref.addSeparator()
        menu_pref.addAction(action_show_status_bar)

        action_need_help = QAction(self.tr('Need Help?'), self)
        action_need_help.setStatusTip(self.tr('Show help information'))
        action_need_help.triggered.connect(need_help)

        action_feedback = QAction(self.tr('Feedback'), self)
        action_feedback.setStatusTip(self.tr('Show information about feedback'))
        action_feedback.triggered.connect(feedback)

        action_citation = QAction(self.tr('Citation'), self)
        action_citation.setStatusTip(self.tr('Show information about citation'))
        action_citation.triggered.connect(citation)

        action_acknowledgements = QAction(self.tr('Acknowledgements'), self)
        action_acknowledgements.setStatusTip(self.tr('Show acknowledgements'))
        action_acknowledgements.triggered.connect(acknowledgements)

        action_about_wordless = QAction(self.tr('About Wordless'), self)
        action_about_wordless.setStatusTip(self.tr('Show information about Wordless'))
        action_about_wordless.triggered.connect(about_wordless)

        menu_help.addAction(action_need_help)
        menu_help.addAction(action_feedback)
        menu_help.addSeparator()
        menu_help.addAction(action_citation)
        menu_help.addSeparator()
        menu_help.addAction(action_acknowledgements)
        menu_help.addAction(action_about_wordless)

    def init_central_widget(self):
        central_widget = QWidget(self)

        self.widget_files = wordless_files.init(self)

        central_widget.setLayout(QGridLayout())
        central_widget.layout().addWidget(self.init_tabs(), 0, 0)
        central_widget.layout().addWidget(self.widget_files, 1, 0)

        central_widget.layout().setRowStretch(0, 2)
        central_widget.layout().setRowStretch(1, 1)

        self.setCentralWidget(central_widget)

    def init_tabs(self):
        def current_tab_changed():
            if self.tabs.currentIndex() == 5:
                self.widget_files.hide()

                self.centralWidget().layout().setRowStretch(1, 0)
            else:
                self.widget_files.show()

                self.centralWidget().layout().setRowStretch(1, 1)

        self.tabs = QTabWidget(self)

        self.tabs.addTab(tab_overview.init(self), self.tr('Overview'))
        self.tabs.addTab(tab_concordancer.init(self), self.tr('Concordancer'))
        self.tabs.addTab(tab_wordlist.init(self), self.tr('Wordlist'))
        self.tabs.addTab(tab_ngram.init(self), self.tr('N-Gram'))
        self.tabs.addTab(tab_collocation.init(self), self.tr('Collocation'))
        self.tabs.addTab(tab_semantics.init(self), self.tr('Semantics'))

        self.tabs.currentChanged.connect(current_tab_changed)

        return self.tabs

if __name__ == '__main__':
    app = QApplication(sys.argv)

    wordless_main = Wordless_Main()
    wordless_main.showMaximized()

    sys.exit(app.exec_())
