# ----------------------------------------------------------------------
# Wordless: Settings - General
# Copyright (C) 2018-2025  Ye Lei (叶磊)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import copy
import os

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QCheckBox,
    QDialog,
    QFileDialog,
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton
)

from wordless.wl_dialogs import wl_dialogs_misc
from wordless.wl_settings import wl_settings
from wordless.wl_utils import wl_conversion, wl_paths
from wordless.wl_widgets import wl_boxes, wl_layouts

# General
class Wl_Settings_General(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['general']
        self.settings_custom = self.main.settings_custom['general']

        # UI Settings
        self.group_box_ui_settings = QGroupBox(self.tr('User Interface Settings'), self)

        self.label_interface_scaling = QLabel(self.tr('Interface scaling:'), self)
        self.combo_box_interface_scaling = wl_boxes.Wl_Combo_Box(self)
        self.label_font_family = QLabel(self.tr('Font family:'), self)
        self.combo_box_font_family = wl_boxes.Wl_Combo_Box_Font_Family(self)
        self.label_font_size = QLabel(self.tr('Font size:'), self)
        self.spin_box_font_size = wl_boxes.Wl_Spin_Box_Font_Size(self)

        self.combo_box_interface_scaling.addItems([
            f'{scaling_factor}%'
            for scaling_factor in range(100, 301, 25)
        ])

        self.group_box_ui_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_ui_settings.layout().addWidget(self.label_interface_scaling, 0, 0)
        self.group_box_ui_settings.layout().addWidget(self.combo_box_interface_scaling, 0, 1)
        self.group_box_ui_settings.layout().addWidget(self.label_font_family, 1, 0)
        self.group_box_ui_settings.layout().addWidget(self.combo_box_font_family, 1, 1)
        self.group_box_ui_settings.layout().addWidget(self.label_font_size, 2, 0)
        self.group_box_ui_settings.layout().addWidget(self.spin_box_font_size, 2, 1)

        self.group_box_ui_settings.layout().setColumnStretch(2, 1)

        # Proxy Settings
        self.group_box_proxy_settings = QGroupBox(self.tr('Proxy Settings'), self)

        self.checkbox_use_proxy = QCheckBox(self.tr('Use proxy'), self)
        self.label_address = QLabel(self.tr('Address:'), self)
        self.line_edit_address = QLineEdit(self)
        self.label_port = QLabel(self.tr('Port:'), self)
        self.line_edit_port = QLineEdit(self)
        self.label_username = QLabel(self.tr('Username:'), self)
        self.line_edit_username = QLineEdit(self)
        self.label_password = QLabel(self.tr('Password:'), self)
        self.line_edit_password = QLineEdit(self)

        self.line_edit_address.setInputMask('000.000.000.000')
        self.line_edit_port.setInputMask('00000')
        self.line_edit_password.setEchoMode(QLineEdit.Password)

        self.checkbox_use_proxy.clicked.connect(self.proxy_settings_changed)

        self.group_box_proxy_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_proxy_settings.layout().addWidget(self.checkbox_use_proxy, 0, 0, 1, 4)
        self.group_box_proxy_settings.layout().addWidget(self.label_address, 1, 0)
        self.group_box_proxy_settings.layout().addWidget(self.line_edit_address, 1, 1)
        self.group_box_proxy_settings.layout().addWidget(self.label_port, 1, 2)
        self.group_box_proxy_settings.layout().addWidget(self.line_edit_port, 1, 3)
        self.group_box_proxy_settings.layout().addWidget(self.label_username, 2, 0)
        self.group_box_proxy_settings.layout().addWidget(self.line_edit_username, 2, 1)
        self.group_box_proxy_settings.layout().addWidget(self.label_password, 2, 2)
        self.group_box_proxy_settings.layout().addWidget(self.line_edit_password, 2, 3)

        # Update Settings
        self.group_box_update_settings = QGroupBox(self.tr('Update Settings'), self)

        self.checkbox_check_updates_on_startup = QCheckBox(self.tr('Check for updates on startup'), self)

        self.group_box_update_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_update_settings.layout().addWidget(self.checkbox_check_updates_on_startup, 0, 0)

        # Miscellaneous Settings
        self.group_box_misc_settings = QGroupBox(self.tr('Miscellaneous Settings'), self)

        self.checkbox_always_confirm_on_exit = QCheckBox(self.tr('Always confirm on exit'), self)

        self.group_box_misc_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_misc_settings.layout().addWidget(self.checkbox_always_confirm_on_exit, 0, 0)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.group_box_ui_settings, 0, 0)
        self.layout().addWidget(self.group_box_proxy_settings, 1, 0)
        self.layout().addWidget(self.group_box_update_settings, 2, 0)
        self.layout().addWidget(self.group_box_misc_settings, 3, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(4, 1)

    def proxy_settings_changed(self):
        if self.checkbox_use_proxy.isChecked():
            self.line_edit_address.setEnabled(True)
            self.line_edit_port.setEnabled(True)
            self.line_edit_username.setEnabled(True)
            self.line_edit_password.setEnabled(True)
        else:
            self.line_edit_address.setEnabled(False)
            self.line_edit_port.setEnabled(False)
            self.line_edit_username.setEnabled(False)
            self.line_edit_password.setEnabled(False)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        # UI Settings
        self.combo_box_interface_scaling.setCurrentText(settings['ui_settings']['interface_scaling'])
        self.combo_box_font_family.setCurrentFont(QFont(settings['ui_settings']['font_family']))
        self.spin_box_font_size.setValue(settings['ui_settings']['font_size'])

        # Proxy Settings
        self.checkbox_use_proxy.setChecked(settings['proxy_settings']['use_proxy'])
        self.line_edit_address.setText(settings['proxy_settings']['address'])
        self.line_edit_port.setText(settings['proxy_settings']['port'])
        self.line_edit_username.setText(settings['proxy_settings']['username'])
        self.line_edit_password.setText(settings['proxy_settings']['password'])

        # Update Settings
        self.checkbox_check_updates_on_startup.setChecked(settings['update_settings']['check_updates_on_startup'])

        # Miscellaneous Settings
        self.checkbox_always_confirm_on_exit.setChecked(settings['misc_settings']['always_confirm_on_exit'])

        self.proxy_settings_changed()

    def apply_settings(self):
        # Check UI settings
        ui_settings_old = [
            self.settings_custom['ui_settings']['interface_scaling'],
            self.settings_custom['ui_settings']['font_family'],
            self.settings_custom['ui_settings']['font_size']
        ]

        ui_settings_new = [
            self.combo_box_interface_scaling.currentText(),
            self.combo_box_font_family.currentFont().family(),
            self.spin_box_font_size.value()
        ]

        if ui_settings_new == ui_settings_old:
            result = 'skip'
        else:
            if wl_dialogs_misc.Wl_Dialog_Restart_Required(self.main).exec_() == QDialog.Accepted:
                result = 'restart'
            else:
                result = 'cancel'

        if result in ['skip', 'restart']:
            # Font Settings
            self.settings_custom['ui_settings']['interface_scaling'] = self.combo_box_interface_scaling.currentText()
            self.settings_custom['ui_settings']['font_family'] = self.combo_box_font_family.currentFont().family()
            self.settings_custom['ui_settings']['font_size'] = self.spin_box_font_size.value()

            # Proxy Settings
            self.settings_custom['proxy_settings']['use_proxy'] = self.checkbox_use_proxy.isChecked()
            self.settings_custom['proxy_settings']['address'] = self.line_edit_address.text()
            self.settings_custom['proxy_settings']['port'] = self.line_edit_port.text()
            self.settings_custom['proxy_settings']['username'] = self.line_edit_username.text()
            self.settings_custom['proxy_settings']['password'] = self.line_edit_password.text()

            # Update Settings
            self.settings_custom['update_settings']['check_updates_on_startup'] = self.checkbox_check_updates_on_startup.isChecked()

            # Miscellaneous Settings
            self.settings_custom['misc_settings']['always_confirm_on_exit'] = self.checkbox_always_confirm_on_exit.isChecked()

            if result == 'restart':
                self.main.restart()

            return True
        elif result == 'cancel':
            self.combo_box_interface_scaling.setCurrentText(ui_settings_old[0])
            self.combo_box_font_family.setCurrentFont(QFont(ui_settings_old[1]))
            self.spin_box_font_size.setValue(ui_settings_old[2])

            return False

        return None

# General - Import
class Wl_Settings_General_Imp(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['general']['imp']
        self.settings_custom = self.main.settings_custom['general']['imp']

        # Files
        self.group_box_files = QGroupBox(self.tr('Files'), self)

        self.label_files_default_path = QLabel(self.tr('Default path:'), self)
        self.line_edit_files_default_path = QLineEdit(self)
        self.button_files_browse = QPushButton(self.tr('Browse...'), self)

        self.button_files_browse.clicked.connect(self.browse_files)

        self.group_box_files.setLayout(wl_layouts.Wl_Layout())
        self.group_box_files.layout().addWidget(self.label_files_default_path, 0, 0)
        self.group_box_files.layout().addWidget(self.line_edit_files_default_path, 0, 1)
        self.group_box_files.layout().addWidget(self.button_files_browse, 0, 2)

        # Search Terms
        self.group_box_search_terms = QGroupBox(self.tr('Search Terms'), self)

        self.label_search_terms_default_path = QLabel(self.tr('Default path:'), self)
        self.line_edit_search_terms_default_path = QLineEdit(self)
        self.button_search_terms_browse = QPushButton(self.tr('Browse...'), self)
        self.label_search_terms_default_encoding = QLabel(self.tr('Default encoding:'), self)
        self.combo_box_search_terms_default_encoding = wl_boxes.Wl_Combo_Box_Encoding(self)
        self.checkbox_search_terms_detect_encodings = QCheckBox(self.tr('Auto-detect encodings'))

        self.button_search_terms_browse.clicked.connect(self.browse_search_terms)
        self.checkbox_search_terms_detect_encodings.stateChanged.connect(self.detect_encodings_changed)

        self.group_box_search_terms.setLayout(wl_layouts.Wl_Layout())
        self.group_box_search_terms.layout().addWidget(self.label_search_terms_default_path, 0, 0)
        self.group_box_search_terms.layout().addWidget(self.line_edit_search_terms_default_path, 0, 1)
        self.group_box_search_terms.layout().addWidget(self.button_search_terms_browse, 0, 2)
        self.group_box_search_terms.layout().addWidget(self.label_search_terms_default_encoding, 1, 0)
        self.group_box_search_terms.layout().addWidget(self.combo_box_search_terms_default_encoding, 1, 1, 1, 2)
        self.group_box_search_terms.layout().addWidget(self.checkbox_search_terms_detect_encodings, 2, 0, 1, 3)

        # Stop Words
        self.group_box_stop_words = QGroupBox(self.tr('Stop Words'), self)

        self.label_stop_words_default_path = QLabel(self.tr('Default path:'), self)
        self.line_edit_stop_words_default_path = QLineEdit(self)
        self.button_stop_words_browse = QPushButton(self.tr('Browse...'), self)
        self.label_stop_words_default_encoding = QLabel(self.tr('Default encoding:'), self)
        self.combo_box_stop_words_default_encoding = wl_boxes.Wl_Combo_Box_Encoding(self)
        self.checkbox_stop_words_detect_encodings = QCheckBox(self.tr('Auto-detect encodings'))

        self.button_stop_words_browse.clicked.connect(self.browse_stop_words)
        self.checkbox_stop_words_detect_encodings.stateChanged.connect(self.detect_encodings_changed)

        self.group_box_stop_words.setLayout(wl_layouts.Wl_Layout())
        self.group_box_stop_words.layout().addWidget(self.label_stop_words_default_path, 0, 0)
        self.group_box_stop_words.layout().addWidget(self.line_edit_stop_words_default_path, 0, 1)
        self.group_box_stop_words.layout().addWidget(self.button_stop_words_browse, 0, 2)
        self.group_box_stop_words.layout().addWidget(self.label_stop_words_default_encoding, 1, 0)
        self.group_box_stop_words.layout().addWidget(self.combo_box_stop_words_default_encoding, 1, 1, 1, 2)
        self.group_box_stop_words.layout().addWidget(self.checkbox_stop_words_detect_encodings, 2, 0, 1, 3)

        # Temporary Files
        self.group_box_temp_files = QGroupBox(self.tr('Temporary Files'), self)

        self.label_temp_files_default_path = QLabel(self.tr('Default path:'), self)
        self.line_edit_temp_files_default_path = QLineEdit(self)
        self.button_temp_files_browse = QPushButton(self.tr('Browse...'), self)

        self.button_temp_files_browse.clicked.connect(self.browse_temp_files)

        self.group_box_temp_files.setLayout(wl_layouts.Wl_Layout())
        self.group_box_temp_files.layout().addWidget(self.label_temp_files_default_path, 0, 0)
        self.group_box_temp_files.layout().addWidget(self.line_edit_temp_files_default_path, 0, 1)
        self.group_box_temp_files.layout().addWidget(self.button_temp_files_browse, 0, 2)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.group_box_files, 0, 0)
        self.layout().addWidget(self.group_box_search_terms, 1, 0)
        self.layout().addWidget(self.group_box_stop_words, 2, 0)
        self.layout().addWidget(self.group_box_temp_files, 3, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(4, 1)

    def browse_files(self):
        path_file = QFileDialog.getExistingDirectory(
            self.main,
            self.tr('Select Folder'),
            self.settings_custom['files']['default_path']
        )

        if path_file:
            self.line_edit_files_default_path.setText(wl_paths.get_normalized_path(path_file))

    def browse_search_terms(self):
        path_file = QFileDialog.getExistingDirectory(
            self.main,
            self.tr('Select Folder'),
            self.settings_custom['search_terms']['default_path']
        )

        if path_file:
            self.line_edit_search_terms_default_path.setText(wl_paths.get_normalized_path(path_file))

    def browse_stop_words(self):
        path_file = QFileDialog.getExistingDirectory(
            self.main,
            self.tr('Select Folder'),
            self.settings_custom['stop_words']['default_path']
        )

        if path_file:
            self.line_edit_stop_words_default_path.setText(wl_paths.get_normalized_path(path_file))

    def browse_temp_files(self):
        path_file = QFileDialog.getExistingDirectory(
            self.main,
            self.tr('Select Folder'),
            self.settings_custom['temp_files']['default_path']
        )

        if path_file:
            self.line_edit_temp_files_default_path.setText(wl_paths.get_normalized_path(path_file))

    def detect_encodings_changed(self):
        if self.checkbox_search_terms_detect_encodings.isChecked():
            self.combo_box_search_terms_default_encoding.setEnabled(False)
        else:
            self.combo_box_search_terms_default_encoding.setEnabled(True)

        if self.checkbox_stop_words_detect_encodings.isChecked():
            self.combo_box_stop_words_default_encoding.setEnabled(False)
        else:
            self.combo_box_stop_words_default_encoding.setEnabled(True)

    def check_path(self, settings):
        if os.path.exists(self.settings_custom[settings]['default_path']):
            return self.settings_custom[settings]['default_path']
        # Fall back to default settings if the path does not exist
        else:
            # If the default path does not exist, create it
            if not os.path.exists(self.settings_default[settings]['default_path']):
                os.makedirs(self.settings_default[settings]['default_path'], exist_ok = True)

            return self.settings_default[settings]['default_path']

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        # Files
        self.line_edit_files_default_path.setText(self.check_path(settings = 'files'))

        # Search Terms
        self.line_edit_search_terms_default_path.setText(self.check_path(settings = 'search_terms'))
        self.combo_box_search_terms_default_encoding.setCurrentText(wl_conversion.to_encoding_text(self.main, settings['search_terms']['default_encoding']))
        self.checkbox_search_terms_detect_encodings.setChecked(settings['search_terms']['detect_encodings'])

        # Stop Words
        self.line_edit_stop_words_default_path.setText(self.check_path(settings = 'stop_words'))
        self.combo_box_stop_words_default_encoding.setCurrentText(wl_conversion.to_encoding_text(self.main, settings['stop_words']['default_encoding']))
        self.checkbox_stop_words_detect_encodings.setChecked(settings['stop_words']['detect_encodings'])

        # Temporary Files
        self.line_edit_temp_files_default_path.setText(self.check_path(settings = 'temp_files'))

        self.detect_encodings_changed()

    def validate_settings(self):
        return bool(
            self.validate_path_dir(self.line_edit_files_default_path)
            and self.validate_path_dir(self.line_edit_search_terms_default_path)
            and self.validate_path_dir(self.line_edit_stop_words_default_path)
            and self.confirm_path(self.line_edit_temp_files_default_path)
        )

    def apply_settings(self):
        # Files
        self.settings_custom['files']['default_path'] = self.line_edit_files_default_path.text()

        # Search Terms
        self.settings_custom['search_terms']['default_path'] = self.line_edit_search_terms_default_path.text()
        self.settings_custom['search_terms']['default_encoding'] = wl_conversion.to_encoding_code(self.main, self.combo_box_search_terms_default_encoding.currentText())
        self.settings_custom['search_terms']['detect_encodings'] = self.checkbox_search_terms_detect_encodings.isChecked()

        # Stop Words
        self.settings_custom['stop_words']['default_path'] = self.line_edit_stop_words_default_path.text()
        self.settings_custom['stop_words']['default_encoding'] = wl_conversion.to_encoding_code(self.main, self.combo_box_stop_words_default_encoding.currentText())
        self.settings_custom['stop_words']['detect_encodings'] = self.checkbox_stop_words_detect_encodings.isChecked()

        # Temporary Files
        self.settings_custom['temp_files']['default_path'] = self.line_edit_temp_files_default_path.text()

        return True

# General - Export
class Wl_Settings_General_Exp(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['general']['exp']
        self.settings_custom = self.main.settings_custom['general']['exp']

        # Tables
        self.group_box_tables = QGroupBox(self.tr('Tables'), self)

        self.label_tables_default_path = QLabel(self.tr('Default path:'), self)
        self.line_edit_tables_default_path = QLineEdit(self)
        self.button_tables_default_path = QPushButton(self.tr('Browse...'), self)
        self.label_tables_default_type = QLabel(self.tr('Default type:'), self)
        self.combo_box_tables_default_type = wl_boxes.Wl_Combo_Box(self)
        self.label_tables_default_encoding = QLabel(self.tr('Default encoding:'), self)
        self.combo_box_tables_default_encoding = wl_boxes.Wl_Combo_Box_Encoding(self.main)

        self.combo_box_tables_default_type.addItems(self.main.settings_global['file_types']['exp_tables'])

        self.button_tables_default_path.clicked.connect(self.browse_tables)
        self.combo_box_tables_default_type.currentTextChanged.connect(self.tables_default_type_changed)

        self.group_box_tables.setLayout(wl_layouts.Wl_Layout())
        self.group_box_tables.layout().addWidget(self.label_tables_default_path, 0, 0)
        self.group_box_tables.layout().addWidget(self.line_edit_tables_default_path, 0, 1)
        self.group_box_tables.layout().addWidget(self.button_tables_default_path, 0, 2)
        self.group_box_tables.layout().addWidget(self.label_tables_default_type, 1, 0)
        self.group_box_tables.layout().addWidget(self.combo_box_tables_default_type, 1, 1, 1, 2)
        self.group_box_tables.layout().addWidget(self.label_tables_default_encoding, 2, 0)
        self.group_box_tables.layout().addWidget(self.combo_box_tables_default_encoding, 2, 1, 1 ,2)

        # Search Terms
        self.group_box_search_terms = QGroupBox(self.tr('Search Terms'), self)

        self.label_search_terms_default_path = QLabel(self.tr('Default path:'), self)
        self.line_edit_search_terms_default_path = QLineEdit(self)
        self.button_search_terms_default_path = QPushButton(self.tr('Browse...'), self)
        self.label_search_terms_default_encoding = QLabel(self.tr('Default encoding:'), self)
        self.combo_box_search_terms_default_encoding = wl_boxes.Wl_Combo_Box_Encoding(self)

        self.button_search_terms_default_path.clicked.connect(self.browse_search_terms)

        self.group_box_search_terms.setLayout(wl_layouts.Wl_Layout())
        self.group_box_search_terms.layout().addWidget(self.label_search_terms_default_path, 0, 0)
        self.group_box_search_terms.layout().addWidget(self.line_edit_search_terms_default_path, 0, 1)
        self.group_box_search_terms.layout().addWidget(self.button_search_terms_default_path, 0, 2)
        self.group_box_search_terms.layout().addWidget(self.label_search_terms_default_encoding, 1, 0)
        self.group_box_search_terms.layout().addWidget(self.combo_box_search_terms_default_encoding, 1, 1, 1, 2)

        # Stop Words
        self.group_box_stop_words = QGroupBox(self.tr('Stop Words'), self)

        self.label_stop_words_default_path = QLabel(self.tr('Default path:'), self)
        self.line_edit_stop_words_default_path = QLineEdit(self)
        self.button_stop_words_default_path = QPushButton(self.tr('Browse...'), self)
        self.label_stop_words_default_encoding = QLabel(self.tr('Default encoding:'), self)
        self.combo_box_stop_words_default_encoding = wl_boxes.Wl_Combo_Box_Encoding(self)

        self.button_stop_words_default_path.clicked.connect(self.browse_stop_words)

        self.group_box_stop_words.setLayout(wl_layouts.Wl_Layout())
        self.group_box_stop_words.layout().addWidget(self.label_stop_words_default_path, 0, 0)
        self.group_box_stop_words.layout().addWidget(self.line_edit_stop_words_default_path, 0, 1)
        self.group_box_stop_words.layout().addWidget(self.button_stop_words_default_path, 0, 2)
        self.group_box_stop_words.layout().addWidget(self.label_stop_words_default_encoding, 1, 0)
        self.group_box_stop_words.layout().addWidget(self.combo_box_stop_words_default_encoding, 1, 1, 1, 2)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.group_box_tables, 0, 0)
        self.layout().addWidget(self.group_box_search_terms, 1, 0)
        self.layout().addWidget(self.group_box_stop_words, 2, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(3, 1)

        self.tables_default_type_changed()

    def tables_default_type_changed(self):
        if '*.xlsx' in self.combo_box_tables_default_type.currentText():
            self.combo_box_tables_default_encoding.setEnabled(False)
        else:
            self.combo_box_tables_default_encoding.setEnabled(True)

    def browse_tables(self):
        path_file = QFileDialog.getExistingDirectory(
            self,
            self.tr('Select Folder'),
            self.settings_custom['tables']['default_path']
        )

        if path_file:
            self.line_edit_tables_default_path.setText(wl_paths.get_normalized_path(path_file))

    def browse_search_terms(self):
        path_file = QFileDialog.getExistingDirectory(
            self,
            self.tr('Select Folder'),
            self.settings_custom['search_terms']['default_path']
        )

        if path_file:
            self.line_edit_search_terms_default_path.setText(wl_paths.get_normalized_path(path_file))

    def browse_stop_words(self):
        path_file = QFileDialog.getExistingDirectory(
            self,
            self.tr('Select Folder'),
            self.settings_custom['stop_words']['default_path']
        )

        if path_file:
            self.line_edit_stop_words_default_path.setText(wl_paths.get_normalized_path(path_file))

    def check_path(self, settings):
        if os.path.exists(self.settings_custom[settings]['default_path']):
            return self.settings_custom[settings]['default_path']
        # Fall back to default settings if the path does not exist
        else:
            # If the default path does not exist, create it
            if not os.path.exists(self.settings_default[settings]['default_path']):
                os.makedirs(self.settings_default[settings]['default_path'], exist_ok = True)

            return self.settings_default[settings]['default_path']

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        # Tables
        self.line_edit_tables_default_path.setText(self.check_path(settings = 'tables'))
        self.combo_box_tables_default_type.setCurrentText(settings['tables']['default_type'])
        self.combo_box_tables_default_encoding.setCurrentText(wl_conversion.to_encoding_text(self.main, settings['tables']['default_encoding']))

        # Search Terms
        self.line_edit_search_terms_default_path.setText(self.check_path(settings = 'search_terms'))
        self.combo_box_search_terms_default_encoding.setCurrentText(wl_conversion.to_encoding_text(self.main, settings['search_terms']['default_encoding']))

        # Stop Words
        self.line_edit_stop_words_default_path.setText(self.check_path(settings = 'stop_words'))
        self.combo_box_stop_words_default_encoding.setCurrentText(wl_conversion.to_encoding_text(self.main, settings['stop_words']['default_encoding']))

    def validate_settings(self):
        return bool(
            self.confirm_path(self.line_edit_tables_default_path)
            and self.confirm_path(self.line_edit_search_terms_default_path)
            and self.confirm_path(self.line_edit_stop_words_default_path)
        )

    def apply_settings(self):
        # Tables
        self.settings_custom['tables']['default_path'] = self.line_edit_tables_default_path.text()
        self.settings_custom['tables']['default_type'] = self.combo_box_tables_default_type.currentText()
        self.settings_custom['tables']['default_encoding'] = wl_conversion.to_encoding_code(self.main, self.combo_box_tables_default_encoding.currentText())

        # Search Terms
        self.settings_custom['search_terms']['default_path'] = self.line_edit_search_terms_default_path.text()
        self.settings_custom['search_terms']['default_encoding'] = wl_conversion.to_encoding_code(self.main, self.combo_box_search_terms_default_encoding.currentText())

        # Stop Words
        self.settings_custom['stop_words']['default_path'] = self.line_edit_stop_words_default_path.text()
        self.settings_custom['stop_words']['default_encoding'] = wl_conversion.to_encoding_code(self.main, self.combo_box_stop_words_default_encoding.currentText())

        return True
