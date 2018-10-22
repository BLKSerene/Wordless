#
# Wordless: Main Window
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
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
import tab_colligation
import tab_semantics

class Wordless_Acknowledgements(wordless_dialog.Wordless_Dialog_Info):
    def __init__(self, main):
        super().__init__(main, main.tr('Acknowledgements'))

        acknowledgements = [
            ['<a href="https://www.python.org/">Python</a>',
             '3.7.0',
             '<a href="mailto:guido@python.org">Guido van Rossum</a><br><a href="mailto:psf@python.org">Python Software Foundation</a>',
             '<a href="https://docs.python.org/3.7/license.html#psf-license-agreement-for-python-release">PSF</a>'],

            ['<a href="https://github.com/jpype-project/jpype/">JPype</a>',
             '0.6.3',
             'Steve Menard<br>Luis Nell',
             '<a href="https://github.com/jpype-project/jpype/blob/master/LICENSE">Apache-2.0</a>'],

            ['<a href="https://www.riverbankcomputing.com/software/pyqt/intro">PyQt</a>',
             '5.11.3',
             '<a href="mailto:info@riverbankcomputing.com">Riverbank Computing Limited</a>',
             '<a href="http://pyqt.sourceforge.net/Docs/PyQt5/introduction.html#license">GPL-3.0</a>'],

            ['<a href="http://hanlp.com/">HanLP</a>',
             '1.68',
             '<a href="mailto:hankcs.cn@gmail.com">He Han (何晗)</a>',
             '<a href="https://github.com/hankcs/HanLP/blob/master/LICENSE">Apache-2.0</a>'],

            ['<a href="https://github.com/hankcs/pyhanlp">pyhanlp</a>',
             '0.1.44',
             '<a href="mailto:hankcs.cn@gmail.com">He Han (何晗)</a>',
             '<a href="https://github.com/hankcs/pyhanlp/blob/master/LICENSE">Apache-2.0</a>'],

            [main.tr('<a href="https://github.com/fxsjy/jieba">jieba</a>'),
             '0.39',
             '<a href="mailto:ccnusjy@gmail.com">Sun Junyi</a>',
             '<a href="https://github.com/fxsjy/jieba/blob/master/LICENSE">MIT</a>'],

            ['<a href="http://www.nltk.org/">NLTK</a>',
             '3.3',
             '<a href="http://www.nltk.org/contribute.html">NLTK Project</a>',
             '<a href="https://github.com/nltk/nltk/blob/develop/LICENSE.txt">Apache-2.0</a>'],

            ['<a href="https://github.com/delph-in/pydelphin">PyDelphin</a>',
             '0.8.0',
             '<a href="mailto:goodman.m.w@gmail.com">Michael Wayne Goodman</a>',
             '<a href="https://github.com/delph-in/pydelphin/blob/develop/LICENSE">MIT</a>'],

            ['<a href="https://spacy.io/">spaCy</a>',
             '2.0.16',
             '<a href="mailto:matt@explosion.ai">Matthew Honnibal</a><br>spaCy GmbH<br><a href="mailto:contact@explosion.ai">ExplosionAI UG (haftungsbeschränkt)</a>',
             '<a href="https://github.com/explosion/spaCy/blob/master/LICENSE">MIT</a>'],

            ['<a href="https://stanfordnlp.github.io/CoreNLP/">Stanford CoreNLP</a>',
             '3.9.2',
             '<a href="mailto:java-nlp-support@lists.stanford.edu">Stanford NLP</a>',
             '<a href="https://github.com/stanfordnlp/CoreNLP/blob/master/LICENSE.txt">GPL-3.0</a>'],

            ['<a href="https://github.com/stanfordnlp/python-stanford-corenlp">Stanford CoreNLP Python Interface</a>',
             '3.8.0',
             '<a href="mailto:java-nlp-support@lists.stanford.edu">Stanford NLP</a>',
             '<a href="https://github.com/stanfordnlp/python-stanford-corenlp/blob/master/LICENSE">MIT</a>'],

            ['<a href="https://www.crummy.com/software/BeautifulSoup/">Beautiful Soup</a>',
             '4.6.3',
             '<a href="https://www.crummy.com/self/contact.html">Leonard Richardson</a>',
             '<a href="https://bazaar.launchpad.net/~leonardr/beautifulsoup/bs4/view/head:/LICENSE">MIT</a>'],

            ['<a href="https://github.com/chardet/chardet">chardet</a>',
             '3.0.4',
             '<a href="mailto:dan.blanchard@gmail.com">Daniel Blanchard</a>',
             '<a href="https://github.com/chardet/chardet/blob/master/LICENSE">LGPL-2.1</a>'],

            ['<a href="https://github.com/Mimino666/langdetect">langdetect</a>',
             '1.0.7',
             '<a href="mailto:michal.danilak@gmail.com">Michal Mimino Danilak</a>',
             '<a href="https://github.com/Mimino666/langdetect/blob/master/LICENSE">Apache-2.0</a>'],

            ['<a href="https://lxml.de/">lxml</a>',
             '4.2.5',
             '<a href="http://consulting.behnel.de">Stefan Behnel</a>',
             '<a href="https://github.com/lxml/lxml/blob/master/doc/licenses/BSD.txt">BSD-3-Clause</a>'],

            ['<a href="https://matplotlib.org/">Matplotlib</a>',
             '3.0.0',
             '<a href="https://github.com/matplotlib/matplotlib#contact">Matplotlib Development Team</a>',
             '<a href="https://matplotlib.org/users/license.html">Matplotlib</a>'],

            ['<a href="http://networkx.github.io/">NetworkX</a>',
             '2.1',
             '<a href="mailto:hagberg@lanl.gov">Aric Hagberg</a><br><a href="mailto:dschult@colgate.edu">Dan Schult</a><br><a href="mailto:swart@lanl.gov">Pieter Swart</a>',
             '<a href="https://github.com/networkx/networkx/blob/master/LICENSE.txt">BSD-3-Clause</a>'],

             ['<a href="http://www.numpy.org/">NumPy</a>',
             '1.15.2',
             'NumPy Developers',
             '<a href="http://www.numpy.org/license.html">BSD-3-Clause</a>'],

            ['<a href="https://openpyxl.readthedocs.io/en/stable/">openpyxl</a>',
             '2.5.8',
             'Eric Gazoni<br><a href="mailto:charlie.clark@clark-consulting.eu">Charlie Clark</a>',
             '<a href="https://bitbucket.org/openpyxl/openpyxl/src/5983d4ba5c18b85171185e8b1ca136876ec52864/LICENCE.rst?at=default&fileviewer=file-view-default">MIT</a>'],

            ['<a href="https://www.scipy.org/">SciPy</a>',
             '1.1.0',
             'SciPy developers',
             '<a href="https://www.scipy.org/scipylib/license.html">BSD-3-Clause</a>'],

            ['<a href="https://lexically.net/downloads/BNC_wordlists/e_lemma.txt">e_lemma.txt</a>',
             '2',
             '<a href="http://www.someya-net.com/index2.html">Yasumasa Someya (染谷泰正)</a>',
             '<a href="https://lexically.net/downloads/BNC_wordlists/e_lemma.txt">Free to use for any research;<br>and/or educational purposes.</a>'],

            ['<a href="https://github.com/michmech/lemmatization-lists">Lemmatization Lists</a>',
             '',
             '<a href="http://www.lexiconista.com/en/#contact">Michal Boleslav Měchura</a>',
             '<a href="https://github.com/michmech/lemmatization-lists/blob/master/LICENCE">ODbL</a>'],

            ['<a href="https://github.com/stopwords-iso/stopwords-iso">Stopwords ISO</a>',
             '0.4.0',
             '<a href="mailto:genediazjr@gmail.com">Gene Diaz</a>',
             '<a href="https://github.com/stopwords-iso/stopwords-iso/blob/master/LICENSE">MIT</a>'],

            ['<a href="https://github.com/6/stopwords-json">stopwords-json</a>',
             '',
             '<a href="mailto:pete@gigadrill.com">Peter Graham</a>',
             '<a href="https://bitbucket.org/openpyxl/openpyxl/src/5983d4ba5c18b85171185e8b1ca136876ec52864/LICENCE.rst?at=default&fileviewer=file-view-default">MIT</a>'],
        ]

        self.setFixedSize(700, 400)

        label_acknowledgements = QLabel(self.tr('Many thanks to the following open-source projects on which Wordless is built on:'), self)

        table_acknowledgements = wordless_table.Wordless_Table(self,
                                                               headers = [
                                                                   self.tr('Name'),
                                                                   self.tr('Version'),
                                                                   self.tr('Author(s)'),
                                                                   self.tr('License')
                                                               ],
                                                               cols_stretch = [
                                                                   self.tr('Author(s)')
                                                               ])

        table_acknowledgements.setSelectionMode(QAbstractItemView.NoSelection)

        table_acknowledgements.setRowCount(len(acknowledgements))

        for i, (name, ver, authors, license) in enumerate(acknowledgements):
            table_acknowledgements.setCellWidget(i, 0, QLabel(name, self))
            table_acknowledgements.setCellWidget(i, 1, QLabel(ver, self))
            table_acknowledgements.setCellWidget(i, 2, QLabel(authors, self))
            table_acknowledgements.setCellWidget(i, 3, QLabel(license, self))

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
        action_show_status_bar.triggered.connect(show_status_bar)

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
            if self.tabs.currentIndex() == 6:
                self.widget_files.hide()

                self.centralWidget().layout().setRowStretch(1, 0)
            else:
                self.widget_files.show()

                self.centralWidget().layout().setRowStretch(1, 1)

        self.tabs = QTabWidget(self)
        self.tabs.addTab(tab_overview.init(self), self.tr('Overview'))
        self.tabs.addTab(tab_concordancer.init(self), self.tr('Concordancer'))
        self.tabs.addTab(tab_wordlist.init(self), self.tr('Wordlist'))
        self.tabs.addTab(tab_ngram.init(self), self.tr('N-gram'))
        self.tabs.addTab(tab_collocation.init(self), self.tr('Collocation'))
        self.tabs.addTab(tab_colligation.init(self), self.tr('Colligation'))
        self.tabs.addTab(tab_semantics.init(self), self.tr('Semantics'))

        self.tabs.currentChanged.connect(current_tab_changed)

        return self.tabs

if __name__ == '__main__':
    app = QApplication(sys.argv)

    wordless_main = Wordless_Main()
    wordless_main.showMaximized()

    sys.exit(app.exec_())
    