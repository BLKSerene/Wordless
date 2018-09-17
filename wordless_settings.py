#
# Wordless: Settings
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

import copy
import os
import pickle

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import nltk

from wordless_utils import *

class Wordless_Settings(QDialog):
    def __init__(self, parent):
        def selection_changed():
            self.settings_general.hide()
            self.settings_lemmatization.hide()

            selected_items = self.tree_settings.selectedItems()
            if not selected_items:
                self.tree_settings.findItems(self.tr('General'), Qt.MatchExactly)[0].setSelected(True)
            else:
                if selected_items[0].text(0) == 'General':
                    self.settings_general.show()
                elif selected_items[0].text(0) == 'Lemmatization':
                    self.settings_lemmatization.show()

        super().__init__(parent)

        self.main = parent

        self.setWindowTitle(self.tr('Settings'))
        self.setFixedHeight(600)

        self.accepted.connect(self.apply)

        self.tree_settings = wordless_tree.Wordless_Tree(self)

        self.tree_settings.addTopLevelItem(QTreeWidgetItem(self.tree_settings, [self.tr('General')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem(self.tree_settings, [self.tr('Lemmatization')]))

        self.tree_settings.itemSelectionChanged.connect(selection_changed)

        wrapper_settings = QWidget()

        layout_wrapper_settings = QGridLayout()
        layout_wrapper_settings.addWidget(self.init_settings_general(), 0, 0)
        layout_wrapper_settings.addWidget(self.init_settings_lemmatization(), 0, 0)

        wrapper_settings.setLayout(layout_wrapper_settings)

        scroll_area_settings = wordless_tab.Wordless_Scroll_Area(self.main, wrapper_settings)

        button_restore_defaults = QPushButton(self.tr('Restore Defaults'), self)
        button_save = QPushButton(self.tr('Save'), self)
        button_apply = QPushButton(self.tr('Apply'), self)
        button_cancel = QPushButton(self.tr('Cancel'), self)

        button_restore_defaults.setFixedWidth(150)
        button_save.setFixedWidth(100)
        button_cancel.setFixedWidth(100)
        button_apply.setFixedWidth(100)

        button_restore_defaults.clicked.connect(lambda: self.load_settings(defaults = True))
        button_save.clicked.connect(self.accept)
        button_apply.clicked.connect(self.apply)
        button_cancel.clicked.connect(self.reject)

        layout_settings_buttons = QGridLayout()
        layout_settings_buttons.addWidget(button_restore_defaults, 0, 0)
        layout_settings_buttons.addWidget(button_save, 0, 1)
        layout_settings_buttons.addWidget(button_apply, 0, 2)
        layout_settings_buttons.addWidget(button_cancel, 0, 3)

        layout_settings = QGridLayout()
        layout_settings.addWidget(self.tree_settings, 0, 0)
        layout_settings.addWidget(scroll_area_settings, 0, 1)
        layout_settings.addLayout(layout_settings_buttons, 1, 0, 1, 2, Qt.AlignRight)

        layout_settings.setColumnStretch(0, 1)
        layout_settings.setColumnStretch(1, 4)

        self.setLayout(layout_settings)

        selection_changed()

    def init_settings_general(self):
        self.settings_general = QWidget(self)

        group_box_encoding = QGroupBox(self.tr('Default Encodings'))

        self.label_encoding_input = QLabel(self.tr('Input Encoding:'), self)
        self.combo_box_encoding_input = wordless_widgets.Wordless_Combo_Box_Encoding(self.main)
        self.label_encoding_output = QLabel(self.tr('Output Encoding:'), self)
        self.combo_box_encoding_output = wordless_widgets.Wordless_Combo_Box_Encoding(self.main)

        layout_encoding = QGridLayout()
        layout_encoding.addWidget(self.label_encoding_input, 0, 0)
        layout_encoding.addWidget(self.combo_box_encoding_input, 0, 1)
        layout_encoding.addWidget(self.label_encoding_output, 1, 0)
        layout_encoding.addWidget(self.combo_box_encoding_output, 1, 1)

        group_box_encoding.setLayout(layout_encoding)

        self.label_precision = QLabel(self.tr('Precision:'), self)
        self.spin_box_precision = QSpinBox(self)

        self.spin_box_precision.setRange(0, 10)

        layout_settings_general = QGridLayout()
        layout_settings_general.addWidget(group_box_encoding, 0, 0, 1, 2, Qt.AlignTop)
        layout_settings_general.addWidget(self.label_precision, 1, 0, Qt.AlignTop)
        layout_settings_general.addWidget(self.spin_box_precision, 1, 1, Qt.AlignTop)

        self.settings_general.setLayout(layout_settings_general)

        return self.settings_general

    def init_settings_lemmatization(self):
        self.settings_lemmatization = QWidget(self)

        self.label_lemmatization_eng = QLabel(self.tr('English:'), self.main)
        self.combo_box_lemmatization_eng = QComboBox(self.main)
        self.label_lemmatization_ast = QLabel(self.tr('Asturian:'), self.main)
        self.combo_box_lemmatization_ast = QComboBox(self.main)
        self.label_lemmatization_bul = QLabel(self.tr('Bulgarian:'), self.main)
        self.combo_box_lemmatization_bul = QComboBox(self.main)
        self.label_lemmatization_cat = QLabel(self.tr('Catalan:'), self.main)
        self.combo_box_lemmatization_cat = QComboBox(self.main)
        self.label_lemmatization_ces = QLabel(self.tr('Czech:'), self.main)
        self.combo_box_lemmatization_ces = QComboBox(self.main)
        self.label_lemmatization_est = QLabel(self.tr('Estonian:'), self.main)
        self.combo_box_lemmatization_est = QComboBox(self.main)
        self.label_lemmatization_fra = QLabel(self.tr('French:'), self.main)
        self.combo_box_lemmatization_fra = QComboBox(self.main)
        self.label_lemmatization_gla = QLabel(self.tr('Gaelic (Scots):'), self.main)
        self.combo_box_lemmatization_gla = QComboBox(self.main)
        self.label_lemmatization_glg = QLabel(self.tr('Galician:'), self.main)
        self.combo_box_lemmatization_glg = QComboBox(self.main)
        self.label_lemmatization_deu = QLabel(self.tr('German:'), self.main)
        self.combo_box_lemmatization_deu = QComboBox(self.main)
        self.label_lemmatization_hun = QLabel(self.tr('Hungarian:'), self.main)
        self.combo_box_lemmatization_hun = QComboBox(self.main)
        self.label_lemmatization_gle = QLabel(self.tr('Irish:'), self.main)
        self.combo_box_lemmatization_gle = QComboBox(self.main)
        self.label_lemmatization_ita = QLabel(self.tr('Italian:'), self.main)
        self.combo_box_lemmatization_ita = QComboBox(self.main)
        self.label_lemmatization_glv = QLabel(self.tr('Manx:'), self.main)
        self.combo_box_lemmatization_glv = QComboBox(self.main)
        self.label_lemmatization_fas = QLabel(self.tr('Persian:'), self.main)
        self.combo_box_lemmatization_fas = QComboBox(self.main)
        self.label_lemmatization_por = QLabel(self.tr('Portuguese:'), self.main)
        self.combo_box_lemmatization_por = QComboBox(self.main)
        self.label_lemmatization_ron = QLabel(self.tr('Romanian:'), self.main)
        self.combo_box_lemmatization_ron = QComboBox(self.main)
        self.label_lemmatization_slk = QLabel(self.tr('Slovak:'), self.main)
        self.combo_box_lemmatization_slk = QComboBox(self.main)
        self.label_lemmatization_slv = QLabel(self.tr('Slovenian:'), self.main)
        self.combo_box_lemmatization_slv = QComboBox(self.main)
        self.label_lemmatization_spa = QLabel(self.tr('Spanish:'), self.main)
        self.combo_box_lemmatization_spa = QComboBox(self.main)
        self.label_lemmatization_swe = QLabel(self.tr('Swedish:'), self.main)
        self.combo_box_lemmatization_swe = QComboBox(self.main)
        self.label_lemmatization_ukr = QLabel(self.tr('Ukrainian:'), self.main)
        self.combo_box_lemmatization_ukr = QComboBox(self.main)
        self.label_lemmatization_cym = QLabel(self.tr('Welsh:'), self.main)
        self.combo_box_lemmatization_cym = QComboBox(self.main)

        self.combo_box_lemmatization_eng.addItems(self.main.lemmatizers[self.tr('English')])
        self.combo_box_lemmatization_ast.addItems(self.main.lemmatizers[self.tr('Asturian')])
        self.combo_box_lemmatization_bul.addItems(self.main.lemmatizers[self.tr('Bulgarian')])
        self.combo_box_lemmatization_cat.addItems(self.main.lemmatizers[self.tr('Catalan')])
        self.combo_box_lemmatization_ces.addItems(self.main.lemmatizers[self.tr('Czech')])
        self.combo_box_lemmatization_est.addItems(self.main.lemmatizers[self.tr('Estonian')])
        self.combo_box_lemmatization_fra.addItems(self.main.lemmatizers[self.tr('French')])
        self.combo_box_lemmatization_gla.addItems(self.main.lemmatizers[self.tr('Gaelic (Scots)')])
        self.combo_box_lemmatization_glg.addItems(self.main.lemmatizers[self.tr('Galician')])
        self.combo_box_lemmatization_deu.addItems(self.main.lemmatizers[self.tr('German')])
        self.combo_box_lemmatization_hun.addItems(self.main.lemmatizers[self.tr('Hungarian')])
        self.combo_box_lemmatization_gle.addItems(self.main.lemmatizers[self.tr('Irish')])
        self.combo_box_lemmatization_ita.addItems(self.main.lemmatizers[self.tr('Italian')])
        self.combo_box_lemmatization_glv.addItems(self.main.lemmatizers[self.tr('Manx')])
        self.combo_box_lemmatization_fas.addItems(self.main.lemmatizers[self.tr('Persian')])
        self.combo_box_lemmatization_por.addItems(self.main.lemmatizers[self.tr('Portuguese')])
        self.combo_box_lemmatization_ron.addItems(self.main.lemmatizers[self.tr('Romanian')])
        self.combo_box_lemmatization_slk.addItems(self.main.lemmatizers[self.tr('Slovak')])
        self.combo_box_lemmatization_slv.addItems(self.main.lemmatizers[self.tr('Slovenian')])
        self.combo_box_lemmatization_spa.addItems(self.main.lemmatizers[self.tr('Spanish')])
        self.combo_box_lemmatization_swe.addItems(self.main.lemmatizers[self.tr('Swedish')])
        self.combo_box_lemmatization_ukr.addItems(self.main.lemmatizers[self.tr('Ukrainian')])
        self.combo_box_lemmatization_cym.addItems(self.main.lemmatizers[self.tr('Welsh')])

        layout_settings_lemmatization = QGridLayout()
        layout_settings_lemmatization.addWidget(self.label_lemmatization_eng, 0, 0)
        layout_settings_lemmatization.addWidget(self.combo_box_lemmatization_eng, 0, 1)
        layout_settings_lemmatization.addWidget(self.label_lemmatization_ast, 1, 0)
        layout_settings_lemmatization.addWidget(self.combo_box_lemmatization_ast, 1, 1)
        layout_settings_lemmatization.addWidget(self.label_lemmatization_bul, 2, 0)
        layout_settings_lemmatization.addWidget(self.combo_box_lemmatization_bul, 2, 1)
        layout_settings_lemmatization.addWidget(self.label_lemmatization_cat, 3, 0)
        layout_settings_lemmatization.addWidget(self.combo_box_lemmatization_cat, 3, 1)
        layout_settings_lemmatization.addWidget(self.label_lemmatization_ces, 4, 0)
        layout_settings_lemmatization.addWidget(self.combo_box_lemmatization_ces, 4, 1)
        layout_settings_lemmatization.addWidget(self.label_lemmatization_est, 5, 0)
        layout_settings_lemmatization.addWidget(self.combo_box_lemmatization_est, 5, 1)
        layout_settings_lemmatization.addWidget(self.label_lemmatization_fra, 6, 0)
        layout_settings_lemmatization.addWidget(self.combo_box_lemmatization_fra, 6, 1)
        layout_settings_lemmatization.addWidget(self.label_lemmatization_gla, 7, 0)
        layout_settings_lemmatization.addWidget(self.combo_box_lemmatization_gla, 7, 1)
        layout_settings_lemmatization.addWidget(self.label_lemmatization_glg, 8, 0)
        layout_settings_lemmatization.addWidget(self.combo_box_lemmatization_glg, 8, 1)
        layout_settings_lemmatization.addWidget(self.label_lemmatization_deu, 9, 0)
        layout_settings_lemmatization.addWidget(self.combo_box_lemmatization_deu, 9, 1)
        layout_settings_lemmatization.addWidget(self.label_lemmatization_hun, 10, 0)
        layout_settings_lemmatization.addWidget(self.combo_box_lemmatization_hun, 10, 1)
        layout_settings_lemmatization.addWidget(self.label_lemmatization_gle, 11, 0)
        layout_settings_lemmatization.addWidget(self.combo_box_lemmatization_gle, 11, 1)
        layout_settings_lemmatization.addWidget(self.label_lemmatization_ita, 12, 0)
        layout_settings_lemmatization.addWidget(self.combo_box_lemmatization_ita, 12, 1)
        layout_settings_lemmatization.addWidget(self.label_lemmatization_glv, 13, 0)
        layout_settings_lemmatization.addWidget(self.combo_box_lemmatization_glv, 13, 1)
        layout_settings_lemmatization.addWidget(self.label_lemmatization_fas, 14, 0)
        layout_settings_lemmatization.addWidget(self.combo_box_lemmatization_fas, 14, 1)
        layout_settings_lemmatization.addWidget(self.label_lemmatization_por, 15, 0)
        layout_settings_lemmatization.addWidget(self.combo_box_lemmatization_por, 15, 1)
        layout_settings_lemmatization.addWidget(self.label_lemmatization_ron, 16, 0)
        layout_settings_lemmatization.addWidget(self.combo_box_lemmatization_ron, 16, 1)
        layout_settings_lemmatization.addWidget(self.label_lemmatization_slk, 17, 0)
        layout_settings_lemmatization.addWidget(self.combo_box_lemmatization_slk, 17, 1)
        layout_settings_lemmatization.addWidget(self.label_lemmatization_slv, 18, 0)
        layout_settings_lemmatization.addWidget(self.combo_box_lemmatization_slv, 18, 1)
        layout_settings_lemmatization.addWidget(self.label_lemmatization_spa, 19, 0)
        layout_settings_lemmatization.addWidget(self.combo_box_lemmatization_spa, 19, 1)
        layout_settings_lemmatization.addWidget(self.label_lemmatization_swe, 20, 0)
        layout_settings_lemmatization.addWidget(self.combo_box_lemmatization_swe, 20, 1)
        layout_settings_lemmatization.addWidget(self.label_lemmatization_ukr, 21, 0)
        layout_settings_lemmatization.addWidget(self.combo_box_lemmatization_ukr, 21, 1)
        layout_settings_lemmatization.addWidget(self.label_lemmatization_cym, 22, 0)
        layout_settings_lemmatization.addWidget(self.combo_box_lemmatization_cym, 22, 1)

        self.settings_lemmatization.setLayout(layout_settings_lemmatization)

        return self.settings_lemmatization

    def load_settings(self, defaults = False):
        if defaults:
            settings = self.main.default_settings
        else:
            settings = self.main.settings

        self.combo_box_encoding_input.setCurrentText(wordless_misc.convert_encoding(self.main, *settings['general']['encoding_input']))
        self.combo_box_encoding_output.setCurrentText(wordless_misc.convert_encoding(self.main, *settings['general']['encoding_output']))

        self.spin_box_precision.setValue(settings['general']['precision'])

        self.combo_box_lemmatization_eng.setCurrentText(settings['lemmatization']['eng'])
        self.combo_box_lemmatization_ast.setCurrentText(settings['lemmatization']['ast'])
        self.combo_box_lemmatization_bul.setCurrentText(settings['lemmatization']['bul'])
        self.combo_box_lemmatization_cat.setCurrentText(settings['lemmatization']['cat'])
        self.combo_box_lemmatization_ces.setCurrentText(settings['lemmatization']['ces'])
        self.combo_box_lemmatization_est.setCurrentText(settings['lemmatization']['est'])
        self.combo_box_lemmatization_fra.setCurrentText(settings['lemmatization']['fra'])
        self.combo_box_lemmatization_gla.setCurrentText(settings['lemmatization']['gla'])
        self.combo_box_lemmatization_glg.setCurrentText(settings['lemmatization']['glg'])
        self.combo_box_lemmatization_deu.setCurrentText(settings['lemmatization']['deu'])
        self.combo_box_lemmatization_hun.setCurrentText(settings['lemmatization']['hun'])
        self.combo_box_lemmatization_gle.setCurrentText(settings['lemmatization']['gle'])
        self.combo_box_lemmatization_ita.setCurrentText(settings['lemmatization']['ita'])
        self.combo_box_lemmatization_glv.setCurrentText(settings['lemmatization']['glv'])
        self.combo_box_lemmatization_fas.setCurrentText(settings['lemmatization']['fas'])
        self.combo_box_lemmatization_por.setCurrentText(settings['lemmatization']['por'])
        self.combo_box_lemmatization_ron.setCurrentText(settings['lemmatization']['ron'])
        self.combo_box_lemmatization_slk.setCurrentText(settings['lemmatization']['slk'])
        self.combo_box_lemmatization_slv.setCurrentText(settings['lemmatization']['slv'])
        self.combo_box_lemmatization_spa.setCurrentText(settings['lemmatization']['spa'])
        self.combo_box_lemmatization_swe.setCurrentText(settings['lemmatization']['swe'])
        self.combo_box_lemmatization_ukr.setCurrentText(settings['lemmatization']['ukr'])
        self.combo_box_lemmatization_cym.setCurrentText(settings['lemmatization']['cym'])

    def apply(self):
        self.main.settings['general']['encoding_input'] = wordless_misc.convert_encoding(self.main, self.combo_box_encoding_input.currentText())
        self.main.settings['general']['encoding_output'] = wordless_misc.convert_encoding(self.main, self.combo_box_encoding_output.currentText())

        self.main.settings['general']['precision'] = self.spin_box_precision.value()

        self.main.settings['lemmatization']['eng'] = self.combo_box_lemmatization_eng.currentText()
        self.main.settings['lemmatization']['ast'] = self.combo_box_lemmatization_ast.currentText()
        self.main.settings['lemmatization']['bul'] = self.combo_box_lemmatization_bul.currentText()
        self.main.settings['lemmatization']['cat'] = self.combo_box_lemmatization_cat.currentText()
        self.main.settings['lemmatization']['ces'] = self.combo_box_lemmatization_ces.currentText()
        self.main.settings['lemmatization']['est'] = self.combo_box_lemmatization_est.currentText()
        self.main.settings['lemmatization']['fra'] = self.combo_box_lemmatization_fra.currentText()
        self.main.settings['lemmatization']['gla'] = self.combo_box_lemmatization_gla.currentText()
        self.main.settings['lemmatization']['glg'] = self.combo_box_lemmatization_glg.currentText()
        self.main.settings['lemmatization']['deu'] = self.combo_box_lemmatization_deu.currentText()
        self.main.settings['lemmatization']['hun'] = self.combo_box_lemmatization_hun.currentText()
        self.main.settings['lemmatization']['gle'] = self.combo_box_lemmatization_gle.currentText()
        self.main.settings['lemmatization']['ita'] = self.combo_box_lemmatization_ita.currentText()
        self.main.settings['lemmatization']['glv'] = self.combo_box_lemmatization_glv.currentText()
        self.main.settings['lemmatization']['fas'] = self.combo_box_lemmatization_fas.currentText()
        self.main.settings['lemmatization']['por'] = self.combo_box_lemmatization_por.currentText()
        self.main.settings['lemmatization']['ron'] = self.combo_box_lemmatization_ron.currentText()
        self.main.settings['lemmatization']['slk'] = self.combo_box_lemmatization_slk.currentText()
        self.main.settings['lemmatization']['slv'] = self.combo_box_lemmatization_slv.currentText()
        self.main.settings['lemmatization']['spa'] = self.combo_box_lemmatization_spa.currentText()
        self.main.settings['lemmatization']['swe'] = self.combo_box_lemmatization_swe.currentText()
        self.main.settings['lemmatization']['ukr'] = self.combo_box_lemmatization_ukr.currentText()
        self.main.settings['lemmatization']['cym'] = self.combo_box_lemmatization_cym.currentText()

    def load(self):
        self.load_settings()

        self.tree_settings.clearSelection()

        self.exec()

def init_settings(main):
    main.file_langs = {
        main.tr('Afrikaans'): 'afr',
        main.tr('Asturian'): 'ast',
        main.tr('Albanian'): 'sqi',
        main.tr('Arabic'): 'ara',
        main.tr('Bengali'): 'ben',
        main.tr('Bulgarian'): 'bul',
        main.tr('Catalan'): 'cat',
        main.tr('Chinese (Simplified)'): 'zho-cn',
        main.tr('Chinese (Traditional)'): 'zho-tw',
        main.tr('Croatian'): 'hrv',
        main.tr('Czech'): 'ces',
        main.tr('Danish'): 'dan',
        main.tr('Dutch'): 'nld',
        main.tr('English'): 'eng',
        main.tr('Estonian'): 'est',
        main.tr('Finnish'): 'fin',
        main.tr('French'): 'fra',
        main.tr('Gaelic (Scots)'): 'gla',
        main.tr('Galician'): 'glg',
        main.tr('German'): 'deu',
        main.tr('Greek'): 'ell',
        main.tr('Gujarati'): 'guj',
        main.tr('Hebrew'): 'heb',
        main.tr('Hindi'): 'hin',
        main.tr('Hungarian'): 'hun',
        main.tr('Indonesian'): 'ind',
        main.tr('Irish'): 'gle',
        main.tr('Italian'): 'ita',
        main.tr('Japanese'): 'jpn',
        main.tr('Kannada'): 'kan',
        main.tr('Korean'): 'kor',
        main.tr('Latvian'): 'lav',
        main.tr('Lithuanian'): 'lit',
        main.tr('Macedonian'): 'mkd',
        main.tr('Malayalam'): 'mal',
        main.tr('Manx'): 'glv',
        main.tr('Marathi'): 'mar',
        main.tr('Nepali'): 'nep',
        main.tr('Norwegian'): 'nno',
        main.tr('Panjabi/Punjabi'): 'pan',
        main.tr('Persian'): 'fas',
        main.tr('Polish'): 'pol',
        main.tr('Portuguese'): 'por',
        main.tr('Romanian'): 'ron',
        main.tr('Russian'): 'rus',
        main.tr('Slovak'): 'slk',
        main.tr('Slovenian'): 'slv',
        main.tr('Somali'): 'som',
        main.tr('Spanish (Castilian)'): 'spa',
        main.tr('Swahili'): 'swa',
        main.tr('Swedish'): 'swe',
        main.tr('Tagalog'): 'tgl',
        main.tr('Tamil'): 'tam',
        main.tr('Telugu'): 'tel',
        main.tr('Thai'): 'tha',
        main.tr('Turkish'): 'tur',
        main.tr('Ukrainian'): 'ukr',
        main.tr('Urdu'): 'urd',
        main.tr('Vietnamese'): 'vie',
        main.tr('Welsh'): 'cym'
    }

    main.file_exts = {
        '.txt': main.tr('Text File (*.txt)'),
        '.htm': main.tr('HTML Page (*.htm; *.html)'),
        '.html': main.tr('HTML Page (*.htm; *.html)')
    }

    main.file_encodings = {
        main.tr('All Languages(UTF-8 Without BOM)'): 'utf_8',
        main.tr('All Languages(UTF-8 With BOM)'): 'utf_8_sig',
        main.tr('All Languages(UTF-16)'): 'utf_16',
        main.tr('All Languages(UTF-16 Big Endian)'): 'utf_16_be',
        main.tr('All Languages(UTF-16 Little Endian)'): 'utf_16_le',
        main.tr('All Languages(UTF-32)'): 'utf_32',
        main.tr('All Languages(UTF-32 Big Endian)'): 'utf_32_be',
        main.tr('All Languages(UTF-32 Little Endian)'): 'utf_32_le',
        main.tr('All Languages(UTF-7)'): 'utf_7',
        main.tr('All Languages(CP65001)'): 'cp65001',

        main.tr('Baltic Languages(CP775)'): 'cp775',
        main.tr('Baltic Languages(Windows-1257)'): 'cp1257',
        main.tr('Baltic Languages(ISO-8859-4)'): 'iso8859_4',
        main.tr('Baltic Languages(ISO-8859-13)'): 'iso8859_13',

        main.tr('Celtic Languages(ISO-8859-14)'): 'iso8859_14',

        main.tr('Nordic Languages(ISO-8859-10)'): 'iso8859_10',

        main.tr('Europe(HP Roman-8)'): 'hp_roman8',

        main.tr('Central Europe(Mac OS Central European)'): 'mac_centeuro',
        main.tr('Central Europe(Mac OS Latin 2)'): 'mac_latin2',

        main.tr('Central and Eastern Europe(CP852)'): 'cp852',
        main.tr('Central and Eastern Europe(Windows-1250)'): 'cp1250',
        main.tr('Central and Eastern Europe(ISO-8859-2)'): 'iso8859_2',
        main.tr('Central and Eastern Europe(Mac Latin)'): 'mac_latin2',

        main.tr('South-Eastern Europe(ISO-8859-16)'): 'iso8859_16',

        main.tr('Western Europe(EBCDIC 500)'): 'cp500',
        main.tr('Western Europe(CP850)'): 'cp850',
        main.tr('Western Europe(CP858)'): 'cp858',
        main.tr('Western Europe(CP1140)'): 'cp1140',
        main.tr('Western Europe(Windows-1252)'): 'windows_1252',
        main.tr('Western Europe(ISO-2022-JP-2)'): 'iso2022_jp_2',
        main.tr('Western Europe(ISO-8859-1)'): 'iso_8859_1',
        main.tr('Western Europe(ISO-8859-15)'): 'iso_8859_15',
        main.tr('Western Europe(Mac OS Roman)'): 'mac_roman',

        main.tr('Arabic(CP720)'): 'cp720',
        main.tr('Arabic(CP864)'): 'cp864',
        main.tr('Arabic(Windows-1256)'): 'cp1256',
        main.tr('Arabic(ISO-8859-6)'): 'iso_8859_6',
        main.tr('Arabic(Mac OS Arabic)'): 'mac_arabic',

        main.tr('Bulgarian(IBM855)'): 'cp855',
        main.tr('Bulgarian(Windows-1251)'): 'windows_1251',
        main.tr('Bulgarian(ISO-8859-5)'): 'iso_8859_5',
        main.tr('Bulgarian(Mac OS Cyrillic)'): 'mac_cyrillic',

        main.tr('Byelorussian(IBM855)'): 'cp855',
        main.tr('Byelorussian(Windows-1251)'): 'cp1251',
        main.tr('Byelorussian(ISO-8859-5)'): 'iso_8859_5',
        main.tr('Byelorussian(Mac OS Cyrillic)'): 'mac_cyrillic',

        main.tr('Canadian(CP863)'): 'cp863',

        main.tr('Simplified Chinese(GB2312)'): 'gb2312',
        main.tr('Simplified Chinese(HZ)'): 'hz_gb_2312',
        main.tr('Simplified Chinese(ISO-2022-JP-2)'): 'iso2022_jp_2',

        main.tr('Traditional Chinese(Big-5)'): 'big5',
        main.tr('Traditional Chinese(Big5-HKSCS)'): 'big5hkscs',
        main.tr('Traditional Chinese(CP950)'): 'cp950',

        main.tr('Unified Chinese(GBK)'): 'gbk',
        main.tr('Unified Chinese(GB18030)'): 'gb18030',

        main.tr('Croatian(Mac OS Croatian)'): 'mac_croatian',

        main.tr('Danish(CP865)'): 'cp865',

        main.tr('English(ASCII)'): 'ascii',
        main.tr('English(EBCDIC 037)'): 'cp037',
        main.tr('English(CP437)'): 'cp437',

        main.tr('Esperanto(ISO-8859-3)'): 'iso_8859_3',

        main.tr('German(EBCDIC 273)'): 'cp273',

        main.tr('Greek(CP737)'): 'cp737',
        main.tr('Greek(CP869)'): 'cp869',
        main.tr('Greek(CP875)'): 'cp875',
        main.tr('Greek(Windows-1253)'): 'windows_1253',
        main.tr('Greek(ISO-2022-JP-2)'): 'iso2022_jp_2',
        main.tr('Greek(ISO-8859-7)'): 'iso_8859_7',
        main.tr('Greek(Mac OS Greek)'): 'mac_greek',

        main.tr('Hebrew(EBCDIC 424)'): 'cp424',
        main.tr('Hebrew(CP856)'): 'cp856',
        main.tr('Hebrew(CP862)'): 'cp862',
        main.tr('Hebrew(Windows-1255)'): 'windows_1255',
        main.tr('Hebrew(ISO-8859-8)'): 'iso_8859_8',

        main.tr('Icelandic(CP861)'): 'cp861',
        main.tr('Icelandic(Mac OS Icelandic)'): 'mac_iceland',

        main.tr('Japanese(CP932)'): 'cp932',
        main.tr('Japanese(EUC-JP)'): 'euc_jp',
        main.tr('Japanese(EUC-JIS-2004)'): 'euc_jis_2004',
        main.tr('Japanese(EUC-JISx0213)'): 'euc_jisx0213',
        main.tr('Japanese(ISO-2022-JP)'): 'iso_2022_jp',
        main.tr('Japanese(ISO-2022-JP-1)'): 'iso2022_jp_1',
        main.tr('Japanese(ISO-2022-JP-2)'): 'iso2022_jp_2',
        main.tr('Japanese(ISO-2022-JP-2)'): 'iso2022_jp_2004',
        main.tr('Japanese(ISO-2022-JP-3)'): 'iso2022_jp_3',
        main.tr('Japanese(ISO-2022-JP-EXT)'): 'iso2022_jp_ext',
        main.tr('Japanese(Shift_JIS)'): 'shift_jis',
        main.tr('Japanese(Shift_JIS-2004)'): 'shift_jis_2004',
        main.tr('Japanese(Shift_JISx0213)'): 'shift_jisx0213',

        main.tr('Kazakh(KZ-1048)'): 'kz1048',
        main.tr('Kazakh(PTCP154)'): 'ptcp154',

        main.tr('Korean(Windows-949)'): 'cp949',
        main.tr('Korean(EUC-KR)'): 'euc_kr',
        main.tr('Korean(ISO-2022-JP-2)'): 'iso2022_jp_2',
        main.tr('Korean(ISO-2022-KR)'): 'iso_2022_kr',
        main.tr('Korean(JOHAB)'): 'johab',

        main.tr('Macedonian(IBM855)'): 'cp855',
        main.tr('Macedonian(Windows-1251)'): 'cp1251',
        main.tr('Macedonian(ISO-8859-5)'): 'iso_8859_5',
        main.tr('Macedonian(Mac OS Cyrillic)'): 'maccyrillic',

        main.tr('Maltese(ISO-8859-3)'): 'iso_8859_3',

        main.tr('Norwegian(CP865)'): 'cp865',

        main.tr('Persian(Mac OS Farsi)'): 'mac_farsi',

        main.tr('Portuguese(CP860)'): 'cp860',

        main.tr('Romanian(Mac OS Romanian)'): 'mac_romanian',

        main.tr('Russian(IBM855)'): 'ibm855',
        main.tr('Russian(IBM866)'): 'ibm866',
        main.tr('Russian(Windows-1251)'): 'windows_1251',
        main.tr('Russian(ISO-8859-5)'): 'iso_8859_5',
        main.tr('Russian(KOI8-R)'): 'koi8_r',
        main.tr('Russian(Mac OS Cyrillic)'): 'maccyrillic',

        main.tr('Serbian(IBM855)'): 'cp855',
        main.tr('Serbian(Windows-1251)'): 'cp1251',
        main.tr('Serbian(ISO-8859-5)'): 'iso8859_5',
        main.tr('Serbian(Mac OS Cyrillic)'): 'maccyrillic',

        main.tr('Tajik(KOI8-T)'): 'koi8_t',

        main.tr('Thai(CP874)'): 'cp874',
        main.tr('Thai(ISO-8859-11)'): 'iso8859_11',
        main.tr('Thai(TIS-620)'): 'tis_620',

        main.tr('Turkish(CP857)'): 'cp857',
        main.tr('Turkish(EBCDIC 1026)'): 'cp1026',
        main.tr('Turkish(Windows-1254)'): 'cp1254',
        main.tr('Turkish(ISO-8859-9)'): 'iso_8859_9',
        main.tr('Turkish(Mac OS Turkish)'): 'mac_turkish',

        main.tr('Ukrainian(CP1125)'): 'cp1125',
        main.tr('Ukrainian(KOI8-U)'): 'koi8_u',

        main.tr('Urdu(CP1006)'): 'cp1006',
        main.tr('Urdu(Mac OS Farsi)'): 'mac_farsi',

        main.tr('Vietnamese(CP1258)'): 'cp1258'
    }

    main.lemmatizers = {
        main.tr('English'): [
            main.tr('NLTK (NLTK Project)'),
            main.tr('Lemmatization List (Michal Boleslav Měchura)')
        ],

        main.tr('Asturian'): [main.tr('Lemmatization List (Michal Boleslav Měchura)')],
        main.tr('Bulgarian'): [main.tr('Lemmatization List (Michal Boleslav Měchura)')],
        main.tr('Catalan'): [main.tr('Lemmatization List (Michal Boleslav Měchura)')],
        main.tr('Czech'): [main.tr('Lemmatization List (Michal Boleslav Měchura)')],
        main.tr('Estonian'): [main.tr('Lemmatization List (Michal Boleslav Měchura)')],
        main.tr('French'): [main.tr('Lemmatization List (Michal Boleslav Měchura)')],
        main.tr('Gaelic (Scots)'): [main.tr('Lemmatization List (Michal Boleslav Měchura)')],
        main.tr('Galician'): [main.tr('Lemmatization List (Michal Boleslav Měchura)')],
        main.tr('German'): [main.tr('Lemmatization List (Michal Boleslav Měchura)')],
        main.tr('Hungarian'): [main.tr('Lemmatization List (Michal Boleslav Měchura)')],
        main.tr('Irish'): [main.tr('Lemmatization List (Michal Boleslav Měchura)')],
        main.tr('Italian'): [main.tr('Lemmatization List (Michal Boleslav Měchura)')],
        main.tr('Manx'): [main.tr('Lemmatization List (Michal Boleslav Měchura)')],
        main.tr('Persian'): [main.tr('Lemmatization List (Michal Boleslav Měchura)')],
        main.tr('Portuguese'): [main.tr('Lemmatization List (Michal Boleslav Měchura)')],
        main.tr('Romanian'): [main.tr('Lemmatization List (Michal Boleslav Měchura)')],
        main.tr('Slovak'): [main.tr('Lemmatization List (Michal Boleslav Měchura)')],
        main.tr('Slovenian'): [main.tr('Lemmatization List (Michal Boleslav Měchura)')],
        main.tr('Spanish'): [main.tr('Lemmatization List (Michal Boleslav Měchura)')],
        main.tr('Swedish'): [main.tr('Lemmatization List (Michal Boleslav Měchura)')],
        main.tr('Ukrainian'): [main.tr('Lemmatization List (Michal Boleslav Měchura)')],
        main.tr('Welsh'): [main.tr('Lemmatization List (Michal Boleslav Měchura)')]
    }

    main.style_dialog = '''
        <head>
          <style>
            * {
              margin: 0;
              border: 0;
              padding: 0;

              line-height: 1.2;
              text-align: justify;
            }

            h1 {
              margin-bottom: 10px;
              font-size: 16px;
              font-weight: bold;
            }

            p {
              margin-bottom: 5px;
            }

            table th {
              font-weight: bold;
            }
          </style>
        </head>
    '''

    main.assoc_measures_bigram = {
        main.tr('Frequency'): nltk.collocations.BigramAssocMeasures().raw_freq,
        main.tr('Student\'s T-test'): nltk.collocations.BigramAssocMeasures().student_t,
        main.tr('Pearson\'s Chi-squared Test'): nltk.collocations.BigramAssocMeasures().chi_sq,
        main.tr('Phi Coefficient'): nltk.collocations.BigramAssocMeasures().phi_sq,
        main.tr('Pointwise Mutual Information'): nltk.collocations.BigramAssocMeasures().pmi,
        main.tr('Likelihood Ratios'): nltk.collocations.BigramAssocMeasures().likelihood_ratio,
        main.tr('Poisson-Stirling'): nltk.collocations.BigramAssocMeasures().poisson_stirling,
        main.tr('Jaccard Index'): nltk.collocations.BigramAssocMeasures().jaccard,
        main.tr('Fisher\'s Exact Test'): nltk.collocations.BigramAssocMeasures().fisher,
        main.tr('Dice\'s coefficient'): nltk.collocations.BigramAssocMeasures().dice
    }

    main.assoc_measures_trigram = {
        main.tr('Frequency'): nltk.collocations.TrigramAssocMeasures().raw_freq,
        main.tr('Student\'s T-test'): nltk.collocations.TrigramAssocMeasures().student_t,
        main.tr('Pearson\'s Chi-squared Test'): nltk.collocations.TrigramAssocMeasures().chi_sq,
        main.tr('Pointwise Mutual Information'): nltk.collocations.TrigramAssocMeasures().pmi,
        main.tr('Likelihood Ratios'): nltk.collocations.TrigramAssocMeasures().likelihood_ratio,
        main.tr('Poisson-Stirling'): nltk.collocations.TrigramAssocMeasures().poisson_stirling,
        main.tr('Jaccard Index'): nltk.collocations.TrigramAssocMeasures().jaccard
    }

    main.assoc_measures_quadgram = {
        main.tr('Frequency'): nltk.collocations.QuadgramAssocMeasures().raw_freq,
        main.tr('Student\'s T-test'): nltk.collocations.QuadgramAssocMeasures().student_t,
        main.tr('Pearson\'s Chi-squared Test'): nltk.collocations.QuadgramAssocMeasures().chi_sq,
        main.tr('Pointwise Mutual Information'): nltk.collocations.QuadgramAssocMeasures().pmi,
        main.tr('Likelihood Ratios'): nltk.collocations.QuadgramAssocMeasures().likelihood_ratio,
        main.tr('Poisson-Stirling'): nltk.collocations.QuadgramAssocMeasures().poisson_stirling,
        main.tr('Jaccard Index'): nltk.collocations.QuadgramAssocMeasures().jaccard
    }

    main.default_settings = {
        'general': {
            'encoding_input': ('utf_8', main.tr('All Languages')),
            'encoding_output': ('utf_8', main.tr('All Languages')),

            'font_monospaced': 'Consolas',

            'precision': 2,
            'style_highlight': 'border: 1px solid Red;'
        },
    
        'file': {
            'files_open': [],
            'files_closed': [],
            'root_path': '.',

            'subfolders': True,

            'auto_detect_encoding': True,
            'auto_detect_lang': True
        },

        'lemmatization': {
            'eng': 'NLTK (NLTK Project)',
            'ast': 'Lemmatization List (Michal Boleslav Měchura)',
            'bul': 'Lemmatization List (Michal Boleslav Měchura)',
            'cat': 'Lemmatization List (Michal Boleslav Měchura)',
            'ces': 'Lemmatization List (Michal Boleslav Měchura)',
            'est': 'Lemmatization List (Michal Boleslav Měchura)',
            'fra': 'Lemmatization List (Michal Boleslav Měchura)',
            'gla': 'Lemmatization List (Michal Boleslav Měchura)',
            'glg': 'Lemmatization List (Michal Boleslav Měchura)',
            'deu': 'Lemmatization List (Michal Boleslav Měchura)',
            'hun': 'Lemmatization List (Michal Boleslav Měchura)',
            'gle': 'Lemmatization List (Michal Boleslav Měchura)',
            'ita': 'Lemmatization List (Michal Boleslav Měchura)',
            'glv': 'Lemmatization List (Michal Boleslav Měchura)',
            'fas': 'Lemmatization List (Michal Boleslav Měchura)',
            'por': 'Lemmatization List (Michal Boleslav Měchura)',
            'ron': 'Lemmatization List (Michal Boleslav Měchura)',
            'slk': 'Lemmatization List (Michal Boleslav Měchura)',
            'slv': 'Lemmatization List (Michal Boleslav Měchura)',
            'spa': 'Lemmatization List (Michal Boleslav Měchura)',
            'swe': 'Lemmatization List (Michal Boleslav Měchura)',
            'ukr': 'Lemmatization List (Michal Boleslav Měchura)',
            'cym': 'Lemmatization List (Michal Boleslav Měchura)'
        },

        'overview': {
    
        },
    
        'concordancer': {
            'search_term': '',
            'search_terms': [],
            'ignore_case': True,
            'lemmatized_forms': True,
            'whole_word': True,
            'regex': False,
            'multi_search': False,
    
            'line_width_char': 80,
            'line_width_token': 20,
            'line_width_mode': 'Tokens',
    
            'number_lines': 25,
            'number_lines_no_limit': True,
    
            'punctuations': False,
    
            'sort_by': [main.tr('Offset'), main.tr('In Ascending Order')],
            'multi_sort_by': [[main.tr('Offset'), main.tr('Ascending')]],
            'multi_sort_colors': [
                '#bb302d',
                '#c2691d',
                '#cbbe01',
                '#569834',
                '#428989',
                '#172e7c',
                '#811570'
            ],
            'multi_sort': False
        },
    
        'wordlist': {
            'words': True,
            'lowercase': True,
            'uppercase': True,
            'title_cased': True,
            'numerals': True,
            'punctuations': False,
    
            'search_term': '',
            'search_terms': [],
            'ignore_case': True,
            'lemmatization': True,
            'whole_word': True,
            'regex': False,
            'multi_search': False,

            'generation_ignore_case': True,
            'generation_lemmatization': True,

            'show_pct': True,
            'show_cumulative': True,
            'show_breakdown': True,

            'rank_no_limit': False,
            'rank_min': 1,
            'rank_max': 50,
            'cumulative': False,
    
            'freq_no_limit': True,
            'freq_min': 0,
            'freq_max': 1000,
            'freq_apply_to': 'Total',
            'len_no_limit': True,
            'len_min': 1,
            'len_max': 20,
            'files_no_limit': True,
            'files_min': 1,
            'files_max': 100
        },
    
        'ngram': {
            'words': True,
            'lowercase': True,
            'uppercase': True,
            'title_cased': True,
            'numerals': True,
            'punctuations': False,
    
            'search_terms': [],
            'keyword_position_no_limit': True,
            'keyword_position_min': 1,
            'keyword_position_max': 2,
            'ignore_case': True,
            'lemmatization': True,
            'whole_word': True,
            'regex': False,
            'multi_search': False,
            'show_all': False,

            'ngram_size_sync': False,
            'ngram_size_min': 2,
            'ngram_size_max': 2,
            'allow_skipped_tokens': 0,

            'show_pct': True,
            'show_cumulative': True,
            'show_breakdown': True,
    
            'rank_no_limit': False,
            'rank_min': 1,
            'rank_max': 50,
            'cumulative': False,
    
            'freq_no_limit': True,
            'freq_min': 0,
            'freq_max': 1000,
            'freq_apply_to': 'Total',
            'len_no_limit': True,
            'len_min': 1,
            'len_max': 20,
            'files_no_limit': True,
            'files_min': 1,
            'files_max': 100
        },

        'collocation': {
            'words': True,
            'lowercase': True,
            'uppercase': True,
            'title_cased': True,
            'numerals': True,
            'punctuations': False,
    
            'search_terms': [],
            'ignore_case': True,
            'lemmatization': True,
            'whole_word': True,
            'regex': False,
            'multi_search': False,
            'show_all': False,

            'window_sync': False,
            'window_left': ['L', 1],
            'window_right': ['R', 1],
            'search_for': main.tr('Bigrams'),
            'assoc_measure': main.tr('Pearson\'s Chi-squared Test'),

            'show_pct': True,
            'show_cumulative': True,
            'show_breakdown': True,

    
            'rank_no_limit': False,
            'rank_min': 1,
            'rank_max': 50,
            'cumulative': False,

            'score_no_limit': True,
            'score_min': 1,
            'score_max': 1000,
            'score_apply_to': 'Total',
            'len_no_limit': True,
            'len_min': 1,
            'len_max': 20,
            'files_no_limit': True,
            'files_min': 1,
            'files_max': 100
        },
    
        'semantics': {
            'search_term': '',
            'search_mode': main.tr('Word'),
            'search_for': main.tr('Synonyms'),
    
            'degree_max': 10,
            'degree_no_limit': True,
            'depth_max': 5,
            'depth_no_limit': True,
            'recursive': True,
            'show_lemmas': True,
    
            'parts_of_speech': {
                'n': main.tr('Noun'),
                'v': main.tr('Verb'),
                'a': main.tr('Adjective'),
                's': main.tr('Adjective Satellite'),
                'r': main.tr('Adverb')
            }
        }
    }

    if os.path.exists('wordless_settings.pkl'):
        with open(r'wordless_settings.pkl', 'rb') as f:
            main.settings = pickle.load(f)
    else:
        main.settings = copy.deepcopy(main.default_settings)

    main.wordless_settings = Wordless_Settings(main)
