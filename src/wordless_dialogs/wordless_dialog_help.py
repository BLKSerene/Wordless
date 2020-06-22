#
# Wordless: Dialogs - Help
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import copy
import csv
import platform
import re

import requests

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_dialogs import wordless_dialog
from wordless_utils import wordless_misc, wordless_threading
from wordless_widgets import (wordless_box, wordless_label, wordless_layout,
                              wordless_table)

class Wordless_Dialog_Citing(wordless_dialog.Wordless_Dialog_Info):
    def __init__(self, main):
        super().__init__(main, main.tr('Citing'),
                         width = 420,
                         no_button = True)

        self.label_citing = wordless_label.Wordless_Label_Dialog(
            self.tr('''
                <div>
                    If you publish work that uses Wordless, please cite as follows.
                </div>
            '''),
            self
        )

        self.label_citation_sys = QLabel(self.tr('Citation System:'), self)
        self.combo_box_citation_sys = wordless_box.Wordless_Combo_Box(self)
        self.text_edit_citing = QTextEdit(self)
    
        self.button_copy = QPushButton(self.tr('Copy'), self)
        self.button_close = QPushButton(self.tr('Close'), self)
    
        self.combo_box_citation_sys.addItems([
            self.tr('APA (7th Edition)'),
            self.tr('MLA (8th Edition)')
        ])
    
        self.button_copy.setFixedWidth(100)
        self.button_close.setFixedWidth(100)
    
        self.text_edit_citing.setFixedHeight(100)
        self.text_edit_citing.setReadOnly(True)
    
        self.combo_box_citation_sys.currentTextChanged.connect(self.citation_sys_changed)
    
        self.button_copy.clicked.connect(self.copy)
        self.button_close.clicked.connect(self.accept)
    
        layout_citation_sys = wordless_layout.Wordless_Layout()
        layout_citation_sys.addWidget(self.label_citation_sys, 0, 0)
        layout_citation_sys.addWidget(self.combo_box_citation_sys, 0, 1)
    
        layout_citation_sys.setColumnStretch(2, 1)
    
        self.wrapper_info.layout().addWidget(self.label_citing, 0, 0, 1, 2)
        self.wrapper_info.layout().addLayout(layout_citation_sys, 1, 0, 1, 2)
        self.wrapper_info.layout().addWidget(self.text_edit_citing, 2, 0, 1, 2)
    
        self.wrapper_buttons.layout().addWidget(self.button_copy, 0, 0)
        self.wrapper_buttons.layout().addWidget(self.button_close, 0, 1)

        self.load_settings()

        self.set_fixed_height()

    def load_settings(self):
        settings = copy.deepcopy(self.main.settings_custom['menu']['help']['citing'])

        self.combo_box_citation_sys.setCurrentText(settings['citation_sys'])

        self.citation_sys_changed()

    def citation_sys_changed(self):
        settings = self.main.settings_custom['menu']['help']['citing']

        settings['citation_sys'] = self.combo_box_citation_sys.currentText()

        if settings['citation_sys'] == self.tr('APA (7th Edition)'):
            self.text_edit_citing.setHtml(f'Ye, L. (2020). <i>Wordless</i> (Version {self.main.ver}) [Computer software]. Github. https://github.com/BLKSerene/Wordless')
        elif settings['citation_sys'] == self.tr('MLA (8th Edition)'):
            self.text_edit_citing.setHtml(f'Ye Lei. <i>Wordless</i>, version {self.main.ver}, 2020. <i>Github</i>, https://github.com/BLKSerene/Wordless.')

    def copy(self):
        self.text_edit_citing.setFocus()
        self.text_edit_citing.selectAll()
        self.text_edit_citing.copy()

class Wordless_Dialog_Acks(wordless_dialog.Wordless_Dialog_Info):
    def __init__(self, main):
        super().__init__(main, main.tr('Acknowledgments'),
                         width = 550)

        with open('wordless_acks/wordless_acks_general.csv', 'r', encoding = 'utf_8', newline = '') as f:
            csv_reader = csv.reader(f, delimiter = '|')

            self.ACKS_GENERAL = [row for row in csv_reader]

        with open('wordless_acks/wordless_acks_nlp.csv', 'r', encoding = 'utf_8', newline = '') as f:
            csv_reader = csv.reader(f, delimiter = '|')

            self.ACKS_NLP = [row for row in csv_reader]

        with open('wordless_acks/wordless_acks_lang_data.csv', 'r', encoding = 'utf_8', newline = '') as f:
            csv_reader = csv.reader(f, delimiter = '|')

            self.ACKS_LANG_DATA = [row for row in csv_reader]

        with open('wordless_acks/wordless_acks_plotting.csv', 'r', encoding = 'utf_8', newline = '') as f:
            csv_reader = csv.reader(f, delimiter = '|')

            self.ACKS_PLOTTING = [row for row in csv_reader]

        with open('wordless_acks/wordless_acks_misc.csv', 'r', encoding = 'utf_8', newline = '') as f:
            csv_reader = csv.reader(f, delimiter = '|')

            self.ACKS_MISC = [row for row in csv_reader]

        self.label_acks = wordless_label.Wordless_Label_Dialog(
            self.tr('''
                <div>
                    I would like to extend my sincere gratitude to the following open-source projects without which this project would not have been possible:
                </div>
            '''),
            self
        )
        self.label_browse_category = QLabel(self.tr('Browse by category:'), self)
        self.combo_box_browse_category = wordless_box.Wordless_Combo_Box(self)

        self.table_acks = wordless_table.Wordless_Table(
            self,
            headers = [
                self.tr('Name'),
                self.tr('Version'),
                self.tr('Author(s)'),
                self.tr('License')
            ]
        )

        self.combo_box_browse_category.addItems([
            self.tr('General'),
            self.tr('Natural Language Processing'),
            self.tr('Language Data'),
            self.tr('Plotting'),
            self.tr('Miscellaneous')
        ])

        self.table_acks.setFixedHeight(250)

        self.combo_box_browse_category.currentTextChanged.connect(self.browse_category_changed)

        layout_browse_category = wordless_layout.Wordless_Layout()
        layout_browse_category.addWidget(self.label_browse_category, 0, 0)
        layout_browse_category.addWidget(self.combo_box_browse_category, 0, 1)

        layout_browse_category.setColumnStretch(2, 1)

        self.wrapper_info.layout().addWidget(self.label_acks, 0, 0)
        self.wrapper_info.layout().addLayout(layout_browse_category, 1, 0)
        self.wrapper_info.layout().addWidget(self.table_acks, 2, 0)

        self.load_settings()

        self.set_fixed_height()

    def load_settings(self):
        settings = copy.deepcopy(self.main.settings_custom['menu']['help']['acks'])

        self.combo_box_browse_category.setCurrentText(settings['browse_category'])

        self.browse_category_changed()

    def browse_category_changed(self):
        settings = self.main.settings_custom['menu']['help']['acks']

        settings['browse_category'] = self.combo_box_browse_category.currentText()

        if settings['browse_category'] == self.tr('General'):
            acks = self.ACKS_GENERAL
        elif settings['browse_category'] == self.tr('Natural Language Processing'):
            acks = self.ACKS_NLP
        elif settings['browse_category'] == self.tr('Language Data'):
            acks = self.ACKS_LANG_DATA
        elif settings['browse_category'] == self.tr('Plotting'):
            acks = self.ACKS_PLOTTING
        elif settings['browse_category'] == self.tr('Miscellaneous'):
            acks = self.ACKS_MISC

        self.table_acks.clear_table()

        self.table_acks.blockSignals(True)
        self.table_acks.setUpdatesEnabled(False)

        self.table_acks.setRowCount(len(acks))

        for i, (project_name, project_url, ver, authors, license_name, licence_url) in enumerate(acks):
            project = f'<a href="{project_url}">{project_name}</a>'
            license = f'<a href="{licence_url}">{license_name}</a>'

            # Pad cells with whitespace
            project = project.replace('<br>', '&nbsp;<br>&nbsp;')
            ver = ver.replace('<br>', '&nbsp;<br>&nbsp;')
            authors = authors.replace('<br>', '&nbsp;<br>&nbsp;')
            license = license.replace('<br>', '&nbsp;<br>&nbsp;')

            project = f'&nbsp;{project}&nbsp;'
            ver = f'&nbsp;{ver}&nbsp;'
            authors = f'&nbsp;{authors}&nbsp;'
            license = f'&nbsp;{license}&nbsp;'

            self.table_acks.setCellWidget(i, 0, wordless_label.Wordless_Label_Html(project, self))
            self.table_acks.setCellWidget(i, 1, wordless_label.Wordless_Label_Html(ver, self))
            self.table_acks.setCellWidget(i, 2, wordless_label.Wordless_Label_Html(authors, self))
            self.table_acks.setCellWidget(i, 3, wordless_label.Wordless_Label_Html(license, self))

        self.table_acks.blockSignals(False)
        self.table_acks.setUpdatesEnabled(True)

        self.table_acks.itemChanged.emit(self.table_acks.item(0, 0))

class Wordless_Dialog_Need_Help(wordless_dialog.Wordless_Dialog_Info):
    def __init__(self, main):
        super().__init__(main, main.tr('Need Help?'),
                         width = 500,
                         height = 500)

        self.label_need_help = wordless_label.Wordless_Label_Dialog(
            self.tr('''
                <div>
                    If you encounter a problem, find a bug, or require any further information, feel free to ask questions, submit bug reports, or provide feedback by <a href="https://github.com/BLKSerene/Wordless/issues/new">creating an issue</a> on Github if you fail to find the answer by searching <a href="https://github.com/BLKSerene/Wordless/issues">existing issues</a> first.
                </div>

                <div>
                    If you need to post sample texts or other information that cannot be shared or you do not want to share publicly, you may send me an email.
                </div>
            '''),
            self
        )

        self.table_need_help = wordless_table.Wordless_Table(
            self,
            headers = [
                self.tr('Channel'),
                self.tr('Contact Information')
            ],
            cols_stretch = [
                self.tr('Contact Information')
            ]
        )

        self.table_need_help.setRowCount(4)
        self.table_need_help.verticalHeader().setHidden(True)

        self.table_need_help.setCellWidget(0, 0, wordless_label.Wordless_Label_Html_Centered(self.tr('Home Page'), self))
        self.table_need_help.setCellWidget(0, 1, wordless_label.Wordless_Label_Html('<a href="https://github.com/BLKSerene/Wordless">https://github.com/BLKSerene/Wordless</a>', self))
        self.table_need_help.setCellWidget(1, 0, wordless_label.Wordless_Label_Html_Centered(self.tr('Documentation'), self))
        self.table_need_help.setCellWidget(1, 1, wordless_label.Wordless_Label_Html('<a href="https://github.com/BLKSerene/Wordless#-documentation">https://github.com/BLKSerene/Wordless#documentation</a>', self))
        self.table_need_help.setCellWidget(2, 0, wordless_label.Wordless_Label_Html_Centered(self.tr('Email'), self))
        self.table_need_help.setCellWidget(2, 1, wordless_label.Wordless_Label_Html('<a href="mailto:blkserene@gmail.com">blkserene@gmail.com</a>', self))
        self.table_need_help.setCellWidget(3, 0, wordless_label.Wordless_Label_Html_Centered(self.tr('<a href="https://www.wechat.com/en/">WeChat</a><br>Official Account'), self))
        self.table_need_help.setCellWidget(3, 1, wordless_label.Wordless_Label_Html_Centered('<img src="imgs/wechat_official_account.jpg">', self))

        self.label_need_help_note = wordless_label.Wordless_Label_Dialog(
            self.tr('''
                <div>
                    <span style="color: #F00;"><b>Important Note</b></span>: I <b>CANNOT GUARANTEE</b> that all emails will always be checked or replied in time. I <b>WILL NOT REPLY</b> to irrelevant emails and I reserve the right to <b>BLOCK AND/OR REPORT</b> people who send me spam emails.
                </div>
            '''),
            self
        )

        self.wrapper_info.layout().addWidget(self.label_need_help, 0, 0)
        self.wrapper_info.layout().addWidget(self.table_need_help, 1, 0)
        self.wrapper_info.layout().addWidget(self.label_need_help_note, 2, 0)

class Wordless_Dialog_Donating(wordless_dialog.Wordless_Dialog_Info):
    def __init__(self, main):
        super().__init__(main, main.tr('Donating'),
                         width = 450)

        self.label_donating = wordless_label.Wordless_Label_Dialog(
            self.tr('''
                <div>
                    If you would like to support the development of Wordless, you may donate via <a href="https://www.paypal.com/">PayPal</a>, <a href="https://global.alipay.com/">Alipay</a>, or <a href="https://pay.weixin.qq.com/index.php/public/wechatpay_en">WeChat Pay</a>.
                </div>
            '''),
            self
        )
        self.label_donating_via = QLabel(self.tr('Donating via:'), self)
        self.combo_box_donating_via = wordless_box.Wordless_Combo_Box(self)
        self.label_donating_via_img = wordless_label.Wordless_Label_Html('', self)
        self.label_donating_note = wordless_label.Wordless_Label_Dialog(
            self.tr('''
                <div>
                    <span style="color: #F00;"><b>Important Note</b></span>: I <b>WILL NOT PROVIDE</b> invoices, receipts, refund services, detailed spending reports, my contact information other than email addresses, my personal social media accounts, private email/phone support, or guarantees on bug fixes, enhancements, new features, or new releases of Wordless for donation.
                </div>
            '''),
            self
        )

        self.combo_box_donating_via.addItems([
            self.tr('PayPal'),
            self.tr('Alipay'),
            self.tr('WeChat Pay')
        ])

        self.combo_box_donating_via.currentTextChanged.connect(self.donating_via_changed)

        layout_donating_via = wordless_layout.Wordless_Layout()
        layout_donating_via.addWidget(self.label_donating_via, 0, 0)
        layout_donating_via.addWidget(self.combo_box_donating_via, 0, 1)

        layout_donating_via.setColumnStretch(2, 1)

        self.wrapper_info.layout().addWidget(self.label_donating, 0, 0)
        self.wrapper_info.layout().addLayout(layout_donating_via, 1, 0)
        self.wrapper_info.layout().addWidget(self.label_donating_via_img, 2, 0, Qt.AlignHCenter | Qt.AlignVCenter)
        self.wrapper_info.layout().addWidget(self.label_donating_note, 3, 0)

        # Calculate height
        donating_via_old = self.main.settings_custom['menu']['help']['donating']['donating_via']

        self.combo_box_donating_via.setCurrentText('PayPal')
        self.donating_via_changed()

        height_donating_via_paypal = self.label_donating_via_img.sizeHint().height()
        self.height_paypal = self.heightForWidth(self.width())

        self.combo_box_donating_via.setCurrentText('Alipay')
        self.donating_via_changed()

        height_donating_via_alipay = self.label_donating_via_img.sizeHint().height()
        self.height_alipay = self.heightForWidth(self.width()) + (height_donating_via_alipay - height_donating_via_paypal)

        self.main.settings_custom['menu']['help']['donating']['donating_via'] = donating_via_old

        self.load_settings()

    def load_settings(self):
        settings = copy.deepcopy(self.main.settings_custom['menu']['help']['donating'])

        self.combo_box_donating_via.setCurrentText(settings['donating_via'])

        self.donating_via_changed()

    def donating_via_changed(self):
        settings = self.main.settings_custom['menu']['help']['donating']

        settings['donating_via'] = self.combo_box_donating_via.currentText()

        if settings['donating_via'] == self.tr('PayPal'):
            self.label_donating_via_img.setText('<a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=V2V54NYE2YD32"><img src="imgs/donating_paypal.gif"></a>')
        elif settings['donating_via'] == self.tr('Alipay'):
            self.label_donating_via_img.setText('<img src="imgs/donating_alipay.png">')
        elif settings['donating_via'] == self.tr('WeChat Pay'):
            self.label_donating_via_img.setText('<img src="imgs/donating_wechat_pay.png">')

        if 'height_alipay' in self.__dict__:
            if settings['donating_via'] == self.tr('PayPal'):
                self.setFixedHeight(self.height_paypal)
            elif settings['donating_via'] in [self.tr('Alipay'), self.tr('WeChat Pay')]:
                self.setFixedHeight(self.height_alipay)

        if platform.system() in ['Windows', 'Linux']:
            self.move_to_center()

class Worker_Check_Updates(QObject):
    worker_done = pyqtSignal(str, str)

    def __init__(self, main):
        super().__init__()

        self.main = main
        self.stopped = False

    def run(self):
        ver_new = ''

        try:
            r = requests.get('https://raw.githubusercontent.com/BLKSerene/Wordless/master/src/VERSION', timeout = 10)

            if r.status_code == 200:
                for line in r.text.splitlines():
                    if line and not line.startswith('#'):
                        ver_new = line.rstrip()

                if self.is_newer_version(ver_new):
                    updates_status = 'updates_available'
                else:
                    updates_status = 'no_updates'
            else:
                updates_status = 'network_error'
        except Exception as e:
            print('Warning: An error occurred when checking for updates!')
            print(f'Error: {e}')

            updates_status = 'network_error'

        if self.stopped:
            updates_status == 'canceled'

        self.worker_done.emit(updates_status, ver_new)

    def is_newer_version(self, ver_new):
        ver_major_new, ver_minor_new, ver_patch_new = wordless_misc.split_wordless_ver(ver_new)

        if (self.main.ver_major < ver_major_new or
            self.main.ver_minor < ver_minor_new or
            self.main.ver_patch < ver_patch_new):
            return True
        else:
            return False

    def stop(self):
        self.stopped = True

class Wordless_Dialog_Check_Updates(wordless_dialog.Wordless_Dialog_Info):
    def __init__(self, main, on_startup = False):
        super().__init__(main, main.tr('Check for Updates'),
                         width = 420,
                         no_button = True)

        self.on_startup = on_startup

        self.label_check_updates = wordless_label.Wordless_Label_Dialog('', self)
        self.checkbox_check_updates_on_startup = QCheckBox(self.tr('Check for updates on startup'), self)
        
        self.button_try_again = QPushButton(self.tr('Try Again'), self)
        self.button_cancel = QPushButton(self.tr('Cancel'), self)

        self.checkbox_check_updates_on_startup.stateChanged.connect(self.check_updates_on_startup_changed)

        self.button_try_again.clicked.connect(self.check_updates)

        self.wrapper_info.layout().addWidget(self.label_check_updates, 0, 0)

        self.wrapper_buttons.layout().addWidget(self.checkbox_check_updates_on_startup, 0, 0)
        self.wrapper_buttons.layout().addWidget(self.button_try_again, 0, 2)
        self.wrapper_buttons.layout().addWidget(self.button_cancel, 0, 3)

        self.wrapper_buttons.layout().setColumnStretch(1, 1)

        self.load_settings()

        self.set_fixed_height()

    def check_updates(self):
        self.updates_status_changed('checking')

        self.main.worker_check_updates = Worker_Check_Updates(self.main)
        thread_check_updates = wordless_threading.Wordless_Thread(self.main.worker_check_updates)

        self.main.threads_check_updates.append(thread_check_updates)

        thread_check_updates.destroyed.connect(lambda: self.main.threads_check_updates.remove(thread_check_updates))

        if self.on_startup:
            self.main.worker_check_updates.worker_done.connect(self.updates_status_changed_on_startup)

        self.main.worker_check_updates.worker_done.connect(self.updates_status_changed)
        self.main.worker_check_updates.worker_done.connect(thread_check_updates.quit)
        self.main.worker_check_updates.worker_done.connect(self.main.worker_check_updates.deleteLater)

        thread_check_updates.start()

    def check_updates_stopped(self):
        self.main.worker_check_updates.stop()

        self.reject()

    def updates_status_changed(self, status, ver_new = ''):
        if status == 'checking':
            self.label_check_updates.set_text(self.tr('''
                <div>
                    Checking for updates...<br>
                    Please wait, it may take a few seconds.
                </div>
            '''))

            self.button_try_again.hide()
            self.button_cancel.setText(self.tr('Cancel'))

            self.button_cancel.disconnect()
            self.button_cancel.clicked.connect(self.check_updates_stopped)
        elif status == 'no_updates':
            self.label_check_updates.set_text(self.tr('''
                <div>
                    Hooray, you are using the latest version of Wordless!
                </div>
            '''))

            self.button_try_again.hide()
            self.button_cancel.setText(self.tr('OK'))

            self.button_cancel.disconnect()
            self.button_cancel.clicked.connect(self.accept)
        elif status == 'updates_available':
            self.label_check_updates.set_text(self.tr(f'''
                <div>
                    Wordless v{ver_new} is out, click <a href="https://github.com/BLKSerene/Wordless/releases/tag/v{ver_new}"><b>HERE</b></a> to download the latest version of Wordless.
                </div>
            '''))

            self.button_try_again.hide()
            self.button_cancel.setText(self.tr('OK'))

            self.button_cancel.disconnect()
            self.button_cancel.clicked.connect(self.accept)
        elif status == 'network_error':
            self.label_check_updates.set_text(self.tr('''
                <div>
                    A network error occurred, please check your network settings and try again or <a href="https://github.com/BLKSerene/Wordless/releases">manually check for updates</a>.
                </div>
            '''))

            self.button_try_again.show()
            self.button_cancel.setText(self.tr('Close'))

            self.button_cancel.disconnect()
            self.button_cancel.clicked.connect(self.accept)

    def updates_status_changed_on_startup(self, status):
        if status == 'updates_available':
            self.open()
            self.setFocus()
        else:
            self.accept()

    def load_settings(self):
        settings = self.main.settings_custom['general']['update_settings']

        self.checkbox_check_updates_on_startup.setChecked(settings['check_updates_on_startup'])

        self.check_updates()

    def check_updates_on_startup_changed(self):
        settings = self.main.settings_custom['general']['update_settings']

        settings['check_updates_on_startup'] = self.checkbox_check_updates_on_startup.isChecked()

class Wordless_Dialog_Changelog(wordless_dialog.Wordless_Dialog_Info):
    def __init__(self, main):
        changelog = []

        try:
            with open('CHANGELOG.md', 'r', encoding = 'utf_8') as f:
                for line in f:
                    # Changelog headers
                    if line.startswith('## '):
                        release_ver = re.search(r'(?<=\[)[^\]]+?(?=\])', line).group()
                        release_link = re.search(r'(?<=\()[^\)]+?(?=\))', line).group()
                        release_date = re.search(r'(?<=\- )[0-9?]{2}/[0-9?]{2}/[0-9?]{4}', line).group()

                        changelog.append({
                            'release_ver': release_ver,
                            'release_link': release_link,
                            'release_date': release_date,
                            'changelog_sections': []
                        })

                    # Changelog section headers
                    elif line.startswith('### '):
                        changelog[-1]['changelog_sections'].append({
                            'section_header': line.replace('###', '').strip(),
                            'section_list': []
                        })
                    # Changelog section lists
                    elif line.startswith('- '):
                        changelog[-1]['changelog_sections'][-1]['section_list'].append(line.replace('-', '').strip())
        except:
            pass

        changelog_text = f'''
            {main.settings_global['styles']['style_changelog']}
            <body>
        '''

        for release in changelog:
            changelog_text += f'''
                <div class="changelog">
                    <div class="changelog-header"><a href="{release['release_link']}">{release['release_ver']}</a> - {release['release_date']}</div>
                    <hr>
            '''

            for changelog_section in release['changelog_sections']:
                changelog_text += f'''
                    <div class="changelog-section">
                        <div class="changelog-section-header">{changelog_section['section_header']}</div>
                        <ul>
                '''

                for item in changelog_section['section_list']:
                    changelog_text += f'''
                        <li>{item}</li>
                    '''

                changelog_text += f'''
                        </ul>
                    </div>
                '''

            changelog_text += f'''
                </div>
            '''

        changelog_text += f'''
            </body>
        '''

        super().__init__(main, main.tr('Changelog'),
                         width = 480,
                         height = 420)

        text_edit_changelog = wordless_box.Wordless_Text_Browser(self)

        text_edit_changelog.setHtml(changelog_text)

        self.wrapper_info.layout().addWidget(text_edit_changelog, 0, 0)

class Wordless_Dialog_About(wordless_dialog.Wordless_Dialog_Info):
    def __init__(self, main):
        super().__init__(main, main.tr('About Wordless'))

        img_wordless_icon = QPixmap('imgs/wordless_icon_about.png')
        img_wordless_icon = img_wordless_icon.scaled(64, 64)

        label_about_icon = QLabel('', self)
        label_about_icon.setPixmap(img_wordless_icon)

        label_about_title = wordless_label.Wordless_Label_Dialog_No_Wrap(
            self.tr(f'''
                <div style="text-align: center;">
                    <h2>Wordless Version {main.ver}</h2>
                    <div>
                        An Integrated Corpus Tool with Multi-Language Support<br>
                        for the Study of Language, Literature, and Translation
                    </div>
                </div>
            '''),
            self
        )
        label_about_copyright = wordless_label.Wordless_Label_Dialog_No_Wrap(
            self.tr('''
                <hr>
                <div style="text-align: center;">
                    Copyright (C) 2018-2019 Ye Lei (<span style="font-family: simsun">叶磊</span>)<br>
                    Licensed Under GNU GPLv3<br>
                    All Other Rights Reserved
                </div>
            '''),
            self
        )

        self.wrapper_info.layout().addWidget(label_about_icon, 0, 0)
        self.wrapper_info.layout().addWidget(label_about_title, 0, 1)
        self.wrapper_info.layout().addWidget(label_about_copyright, 1, 0, 1, 2)

        self.wrapper_info.layout().setColumnStretch(1, 1)
        self.wrapper_info.layout().setVerticalSpacing(0)

        self.set_fixed_size()
        self.setFixedWidth(self.width() + 10)
