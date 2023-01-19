# ----------------------------------------------------------------------
# Wordless: Settings - Figures
# Copyright (C) 2018-2022  Ye Lei (叶磊)
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import copy
import os

import matplotlib
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFileDialog, QGroupBox, QLabel, QLineEdit, QPushButton
import wordcloud

from wordless.wl_checks import wl_checks_misc
from wordless.wl_settings import wl_settings
from wordless.wl_utils import wl_paths
from wordless.wl_widgets import wl_boxes, wl_layouts, wl_widgets

class Wl_Settings_Figs_Line_Charts(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['figs']['line_charts']
        self.settings_custom = self.main.settings_custom['figs']['line_charts']

        # General Settings
        self.group_box_general_settings = QGroupBox(self.tr('General Settings'), self)

        self.label_font = QLabel(self.tr('Font:'), self)
        self.combo_box_font = wl_boxes.Wl_Combo_Box_Font_Family(self)

        self.group_box_general_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_general_settings.layout().addWidget(self.label_font, 0, 0)
        self.group_box_general_settings.layout().addWidget(self.combo_box_font, 0, 1)

        self.group_box_general_settings.layout().setColumnStretch(2, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.group_box_general_settings, 0, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(1, 1)

    def change_fonts(self):
        matplotlib.rcParams['font.family'] = self.settings_custom['general_settings']['font']

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        # General Settings
        self.combo_box_font.setCurrentFont(QFont(settings['general_settings']['font']))

        self.change_fonts()

    def apply_settings(self):
        # General Settings
        self.settings_custom['general_settings']['font'] = self.combo_box_font.currentFont().family()

        self.change_fonts()

        return True

class Wl_Settings_Figs_Word_Clouds(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['figs']['word_clouds']
        self.settings_custom = self.main.settings_custom['figs']['word_clouds']

        # General Settings
        self.group_box_general_settings = QGroupBox(self.tr('General Settings'), self)

        self.label_font = QLabel(self.tr('Font:'), self)
        self.combo_box_font = wl_boxes.Wl_Combo_Box(self)
        self.label_font_path = QLabel(self.tr('Font Path:'), self)
        self.line_edit_font_path = QLineEdit(self)
        self.button_font_path = QPushButton(self.tr('Browse...'), self)
        self.label_bg_color = QLabel(self.tr('Background Color:'), self)
        (
            self.label_bg_color_pick,
            self.button_bg_color_pick
        ) = wl_widgets.wl_widgets_pick_color(self)

        self.combo_box_font.addItems([
            'Droid Sans Mono',
            'GNU Unifont',
            self.tr('Custom')
        ])

        self.combo_box_font.currentTextChanged.connect(self.word_clouds_changed)
        self.button_font_path.clicked.connect(self.browse_font_file)

        layout_font_path = wl_layouts.Wl_Layout()
        layout_font_path.addWidget(self.line_edit_font_path, 0, 0)
        layout_font_path.addWidget(self.button_font_path, 0, 1)

        self.group_box_general_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_general_settings.layout().addWidget(self.label_font, 0, 0)
        self.group_box_general_settings.layout().addWidget(self.combo_box_font, 0, 1, 1, 2)
        self.group_box_general_settings.layout().addWidget(self.label_font_path, 1, 0)
        self.group_box_general_settings.layout().addLayout(layout_font_path, 1, 1, 1, 3)
        self.group_box_general_settings.layout().addWidget(self.label_bg_color, 2, 0)
        self.group_box_general_settings.layout().addWidget(self.label_bg_color_pick, 2, 1)
        self.group_box_general_settings.layout().addWidget(self.button_bg_color_pick, 2, 2)

        self.group_box_general_settings.layout().setColumnStretch(3, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.group_box_general_settings, 0, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(1, 1)

    def browse_font_file(self):
        path_file = QFileDialog.getOpenFileName(
            parent = self.main,
            caption = self.tr('Select Font File'),
            directory = wl_checks_misc.check_dir(os.path.split(self.line_edit_font_path.text())[0]),
            filter = ';;'.join(self.main.settings_global['file_types']['fonts']),
            initialFilter = self.main.settings_global['file_types']['fonts'][-1]
        )[0]

        if path_file:
            self.line_edit_font_path.setText(wl_paths.get_normalized_path(path_file))

    def word_clouds_changed(self):
        if self.combo_box_font.currentText() == self.tr('Custom'):
            self.label_font_path.show()
            self.line_edit_font_path.show()
            self.button_font_path.show()
        else:
            self.label_font_path.hide()
            self.line_edit_font_path.hide()
            self.button_font_path.hide()

    def change_fonts(self):
        if self.settings_custom['general_settings']['font'] == 'Droid Sans Mono':
            wordcloud.wordcloud.FONT_PATH = os.path.join(wordcloud.wordcloud.FILE, 'DroidSansMono.ttf')
        elif self.settings_custom['general_settings']['font'] == 'GNU Unifont':
            wordcloud.wordcloud.FONT_PATH = wl_paths.get_path_data('unifont-15.0.01.ttf')
        elif self.settings_custom['general_settings']['font'] == self.tr('Custom'):
            wordcloud.wordcloud.FONT_PATH = self.settings_custom['general_settings']['font_path']

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        # General Settings
        self.combo_box_font.setCurrentText(settings['general_settings']['font'])
        self.line_edit_font_path.setText(settings['general_settings']['font_path'])
        self.label_bg_color_pick.set_color(settings['general_settings']['bg_color'])

        self.word_clouds_changed()
        self.change_fonts()

    def validate_settings(self):
        if self.combo_box_font.currentText() == self.tr('Custom'):
            return bool(self.validate_path_file(self.line_edit_font_path))
        else:
            return True

    def apply_settings(self):
        # Generation Settings
        self.settings_custom['general_settings']['font'] = self.combo_box_font.currentText()
        if self.settings_custom['general_settings']['font'] == self.tr('Custom'):
            self.settings_custom['general_settings']['font_path'] = self.line_edit_font_path.text()
        self.settings_custom['general_settings']['bg_color'] = self.label_bg_color_pick.get_color()

        self.change_fonts()

        return True

class Wl_Settings_Figs_Network_Graphs(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['figs']['network_graphs']
        self.settings_custom = self.main.settings_custom['figs']['network_graphs']

        # General Settings
        self.group_box_general_settings = QGroupBox(self.tr('General Settings'), self)

        self.label_layout = QLabel(self.tr('Layout:'), self)
        self.combo_box_layout = wl_boxes.Wl_Combo_Box(self)
        self.label_node_font = QLabel(self.tr('Node Font:'), self)
        self.combo_box_node_font = wl_boxes.Wl_Combo_Box_Font_Family(self)
        self.label_node_font_size = QLabel(self.tr('Node Font Size:'), self)
        self.spin_box_node_font_size = wl_boxes.Wl_Spin_Box_Font_Size(self)
        self.label_edge_font = QLabel(self.tr('Edge Font:'), self)
        self.combo_box_edge_font = wl_boxes.Wl_Combo_Box_Font_Family(self)
        self.label_edge_font_size = QLabel(self.tr('Edge Font Size:'), self)
        self.spin_box_edge_font_size = wl_boxes.Wl_Spin_Box_Font_Size(self)
        self.label_edge_color = QLabel(self.tr('Edge Color:'), self)
        (
            self.label_edge_color_pick,
            self.combo_box_color_pick
        ) = wl_widgets.wl_widgets_pick_color(self)

        self.combo_box_layout.addItems([
            self.tr('Circular'),
            self.tr('Kamada-Kawai'),
            self.tr('Planar'),
            self.tr('Random'),
            self.tr('Shell'),
            self.tr('Spring'),
            self.tr('Spectral')
        ])

        self.group_box_general_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_general_settings.layout().addWidget(self.label_layout, 0, 0)
        self.group_box_general_settings.layout().addWidget(self.combo_box_layout, 0, 1, 1, 2)
        self.group_box_general_settings.layout().addWidget(self.label_node_font, 1, 0)
        self.group_box_general_settings.layout().addWidget(self.combo_box_node_font, 1, 1, 1, 2)
        self.group_box_general_settings.layout().addWidget(self.label_node_font_size, 2, 0)
        self.group_box_general_settings.layout().addWidget(self.spin_box_node_font_size, 2, 1, 1, 2)
        self.group_box_general_settings.layout().addWidget(self.label_edge_font, 3, 0)
        self.group_box_general_settings.layout().addWidget(self.combo_box_edge_font, 3, 1, 1, 2)
        self.group_box_general_settings.layout().addWidget(self.label_edge_font_size, 4, 0)
        self.group_box_general_settings.layout().addWidget(self.spin_box_edge_font_size, 4, 1, 1, 2)
        self.group_box_general_settings.layout().addWidget(self.label_edge_color, 5, 0)
        self.group_box_general_settings.layout().addWidget(self.label_edge_color_pick, 5, 1)
        self.group_box_general_settings.layout().addWidget(self.combo_box_color_pick, 5, 2)

        self.group_box_general_settings.layout().setColumnStretch(3, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.group_box_general_settings, 0, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(1, 1)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        # General Settings
        self.combo_box_layout.setCurrentText(settings['general_settings']['layout'])
        self.combo_box_node_font.setCurrentFont(QFont(settings['general_settings']['node_font']))
        self.spin_box_node_font_size.setValue(settings['general_settings']['node_font_size'])
        self.combo_box_edge_font.setCurrentFont(QFont(settings['general_settings']['edge_font']))
        self.spin_box_edge_font_size.setValue(settings['general_settings']['edge_font_size'])
        self.label_edge_color_pick.set_color(settings['general_settings']['edge_color'])

    def apply_settings(self):
        # General Settings
        self.settings_custom['general_settings']['layout'] = self.combo_box_layout.currentText()
        self.settings_custom['general_settings']['node_font'] = self.combo_box_node_font.currentFont().family()
        self.settings_custom['general_settings']['node_font_size'] = self.spin_box_node_font_size.value()
        self.settings_custom['general_settings']['edge_font'] = self.combo_box_edge_font.currentFont().family()
        self.settings_custom['general_settings']['edge_font_size'] = self.spin_box_edge_font_size.value()
        self.settings_custom['general_settings']['edge_color'] = self.label_edge_color_pick.get_color()

        return True
