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

from wordless.wl_checking import wl_checking_misc
from wordless.wl_settings import wl_settings
from wordless.wl_utils import wl_paths
from wordless.wl_widgets import wl_boxes, wl_layouts, wl_widgets

class Wl_Settings_Figs(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['figs']
        self.settings_custom = self.main.settings_custom['figs']

        # Line Chart
        self.group_box_figs_line_charts = QGroupBox(self.tr('Line Charts'), self)

        self.label_figs_line_charts_font = QLabel(self.tr('Font:'), self)
        self.combo_box_figs_line_charts_font = wl_boxes.Wl_Combo_Box_Font_Family(self)

        self.group_box_figs_line_charts.setLayout(wl_layouts.Wl_Layout())
        self.group_box_figs_line_charts.layout().addWidget(self.label_figs_line_charts_font, 0, 0)
        self.group_box_figs_line_charts.layout().addWidget(self.combo_box_figs_line_charts_font, 0, 1)

        self.group_box_figs_line_charts.layout().setColumnStretch(2, 1)

        # Word Cloud
        self.group_box_figs_word_clouds = QGroupBox(self.tr('Word Clouds'), self)

        self.label_figs_word_clouds_font = QLabel(self.tr('Font:'), self)
        self.combo_box_figs_word_clouds_font = wl_boxes.Wl_Combo_Box(self)
        self.label_figs_word_clouds_font_path = QLabel(self.tr('Font Path:'), self)
        self.line_edit_figs_word_clouds_font_path = QLineEdit(self)
        self.button_figs_word_clouds_font_path = QPushButton(self.tr('Browse...'), self)
        self.label_figs_word_clouds_bg_color = QLabel(self.tr('Background Color:'), self)
        (
            self.label_figs_word_clouds_bg_color_pick,
            self.button_figs_word_clouds_bg_color_pick
        ) = wl_widgets.wl_widgets_pick_color(self)

        self.combo_box_figs_word_clouds_font.addItems([
            'Droid Sans Mono',
            'GNU Unifont',
            self.tr('Custom')
        ])

        self.combo_box_figs_word_clouds_font.currentTextChanged.connect(self.word_clouds_changed)
        self.button_figs_word_clouds_font_path.clicked.connect(self.browse_font_file)

        layout_word_clouds_font_path = wl_layouts.Wl_Layout()
        layout_word_clouds_font_path.addWidget(self.line_edit_figs_word_clouds_font_path, 0, 0)
        layout_word_clouds_font_path.addWidget(self.button_figs_word_clouds_font_path, 0, 1)

        self.group_box_figs_word_clouds.setLayout(wl_layouts.Wl_Layout())
        self.group_box_figs_word_clouds.layout().addWidget(self.label_figs_word_clouds_font, 0, 0)
        self.group_box_figs_word_clouds.layout().addWidget(self.combo_box_figs_word_clouds_font, 0, 1, 1, 2)
        self.group_box_figs_word_clouds.layout().addWidget(self.label_figs_word_clouds_font_path, 1, 0)
        self.group_box_figs_word_clouds.layout().addLayout(layout_word_clouds_font_path, 1, 1, 1, 3)
        self.group_box_figs_word_clouds.layout().addWidget(self.label_figs_word_clouds_bg_color, 2, 0)
        self.group_box_figs_word_clouds.layout().addWidget(self.label_figs_word_clouds_bg_color_pick, 2, 1)
        self.group_box_figs_word_clouds.layout().addWidget(self.button_figs_word_clouds_bg_color_pick, 2, 2)

        self.group_box_figs_word_clouds.layout().setColumnStretch(3, 1)

        # Network Graph
        self.group_box_figs_network_graphs = QGroupBox(self.tr('Network Graphs'), self)

        self.label_figs_network_graphs_layout = QLabel(self.tr('Layout:'), self)
        self.combo_box_figs_network_graphs_layout = wl_boxes.Wl_Combo_Box(self)
        self.label_figs_network_graphs_node_font = QLabel(self.tr('Node Font:'), self)
        self.combo_box_figs_network_graphs_node_font = wl_boxes.Wl_Combo_Box_Font_Family(self)
        self.label_figs_network_graphs_node_font_size = QLabel(self.tr('Node Font Size:'), self)
        self.spin_box_figs_network_graphs_node_font_size = wl_boxes.Wl_Spin_Box_Font_Size(self)
        self.label_figs_network_graphs_edge_font = QLabel(self.tr('Edge Font:'), self)
        self.combo_box_figs_network_graphs_edge_font = wl_boxes.Wl_Combo_Box_Font_Family(self)
        self.label_figs_network_graphs_edge_font_size = QLabel(self.tr('Edge Font Size:'), self)
        self.spin_box_figs_network_graphs_edge_font_size = wl_boxes.Wl_Spin_Box_Font_Size(self)
        self.label_figs_network_graphs_edge_color = QLabel(self.tr('Edge Color:'), self)
        (
            self.label_figs_network_graphs_edge_color_pick,
            self.combo_box_figs_network_graphs_color_pick
        ) = wl_widgets.wl_widgets_pick_color(self)

        self.combo_box_figs_network_graphs_layout.addItems([
            self.tr('Circular'),
            self.tr('Kamada-Kawai'),
            self.tr('Planar'),
            self.tr('Random'),
            self.tr('Shell'),
            self.tr('Spring'),
            self.tr('Spectral')
        ])

        self.group_box_figs_network_graphs.setLayout(wl_layouts.Wl_Layout())
        self.group_box_figs_network_graphs.layout().addWidget(self.label_figs_network_graphs_layout, 0, 0)
        self.group_box_figs_network_graphs.layout().addWidget(self.combo_box_figs_network_graphs_layout, 0, 1, 1, 2)
        self.group_box_figs_network_graphs.layout().addWidget(self.label_figs_network_graphs_node_font, 1, 0)
        self.group_box_figs_network_graphs.layout().addWidget(self.combo_box_figs_network_graphs_node_font, 1, 1, 1, 2)
        self.group_box_figs_network_graphs.layout().addWidget(self.label_figs_network_graphs_node_font_size, 2, 0)
        self.group_box_figs_network_graphs.layout().addWidget(self.spin_box_figs_network_graphs_node_font_size, 2, 1, 1, 2)
        self.group_box_figs_network_graphs.layout().addWidget(self.label_figs_network_graphs_edge_font, 3, 0)
        self.group_box_figs_network_graphs.layout().addWidget(self.combo_box_figs_network_graphs_edge_font, 3, 1, 1, 2)
        self.group_box_figs_network_graphs.layout().addWidget(self.label_figs_network_graphs_edge_font_size, 4, 0)
        self.group_box_figs_network_graphs.layout().addWidget(self.spin_box_figs_network_graphs_edge_font_size, 4, 1, 1, 2)
        self.group_box_figs_network_graphs.layout().addWidget(self.label_figs_network_graphs_edge_color, 5, 0)
        self.group_box_figs_network_graphs.layout().addWidget(self.label_figs_network_graphs_edge_color_pick, 5, 1)
        self.group_box_figs_network_graphs.layout().addWidget(self.combo_box_figs_network_graphs_color_pick, 5, 2)

        self.group_box_figs_network_graphs.layout().setColumnStretch(3, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.group_box_figs_line_charts, 0, 0)
        self.layout().addWidget(self.group_box_figs_word_clouds, 1, 0)
        self.layout().addWidget(self.group_box_figs_network_graphs, 2, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(3, 1)

    def browse_font_file(self):
        path_file = QFileDialog.getOpenFileName(
            parent = self.main,
            caption = self.tr('Select Font File'),
            directory = wl_checking_misc.check_dir(os.path.split(self.line_edit_figs_word_clouds_font_path.text())[0]),
            filter = ';;'.join(self.main.settings_global['file_types']['fonts']),
            initialFilter = self.main.settings_global['file_types']['fonts'][-1]
        )[0]

        if path_file:
            self.line_edit_figs_word_clouds_font_path.setText(wl_paths.get_normalized_path(path_file))

    def word_clouds_changed(self):
        if self.combo_box_figs_word_clouds_font.currentText() == self.tr('Custom'):
            self.label_figs_word_clouds_font_path.show()
            self.line_edit_figs_word_clouds_font_path.show()
            self.button_figs_word_clouds_font_path.show()
        else:
            self.label_figs_word_clouds_font_path.hide()
            self.line_edit_figs_word_clouds_font_path.hide()
            self.button_figs_word_clouds_font_path.hide()

    def change_fonts(self):
        if self.main.settings_custom['figs']['word_clouds']['font'] == 'Droid Sans Mono':
            wordcloud.wordcloud.FONT_PATH = os.path.join(wordcloud.wordcloud.FILE, 'DroidSansMono.ttf')
        elif self.main.settings_custom['figs']['word_clouds']['font'] == 'GNU Unifont':
            wordcloud.wordcloud.FONT_PATH = wl_paths.get_path_data('unifont-15.0.01.ttf')
        elif self.main.settings_custom['figs']['word_clouds']['font'] == self.tr('Custom'):
            wordcloud.wordcloud.FONT_PATH = self.main.settings_custom['figs']['word_clouds']['font_path']

        matplotlib.rcParams['font.family'] = self.main.settings_custom['figs']['line_charts']['font']

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        # Line Charts
        self.combo_box_figs_line_charts_font.setCurrentFont(QFont(settings['line_charts']['font']))

        # Word Clouds
        self.combo_box_figs_word_clouds_font.setCurrentText(settings['word_clouds']['font'])
        self.line_edit_figs_word_clouds_font_path.setText(settings['word_clouds']['font_path'])
        self.label_figs_word_clouds_bg_color_pick.set_color(settings['word_clouds']['bg_color'])

        # Network Graphs
        self.combo_box_figs_network_graphs_layout.setCurrentText(settings['network_graphs']['layout'])
        self.combo_box_figs_network_graphs_node_font.setCurrentFont(QFont(settings['network_graphs']['node_font']))
        self.spin_box_figs_network_graphs_node_font_size.setValue(settings['network_graphs']['node_font_size'])
        self.combo_box_figs_network_graphs_edge_font.setCurrentFont(QFont(settings['network_graphs']['edge_font']))
        self.spin_box_figs_network_graphs_edge_font_size.setValue(settings['network_graphs']['edge_font_size'])
        self.label_figs_network_graphs_edge_color_pick.set_color(settings['network_graphs']['edge_color'])

        self.word_clouds_changed()
        self.change_fonts()

    def validate_settings(self):
        if self.combo_box_figs_word_clouds_font.currentText() == self.tr('Custom'):
            return bool(self.validate_path_file(self.line_edit_figs_word_clouds_font_path))
        else:
            return True

    def apply_settings(self):
        # Line Charts
        self.settings_custom['line_charts']['font'] = self.combo_box_figs_line_charts_font.currentFont().family()

        # Word Clouds
        self.settings_custom['word_clouds']['font'] = self.combo_box_figs_word_clouds_font.currentText()
        if self.settings_custom['word_clouds']['font'] == self.tr('Custom'):
            self.settings_custom['word_clouds']['font_path'] = self.line_edit_figs_word_clouds_font_path.text()
        self.settings_custom['word_clouds']['bg_color'] = self.label_figs_word_clouds_bg_color_pick.get_color()

        # Network Graphs
        self.settings_custom['network_graphs']['layout'] = self.combo_box_figs_network_graphs_layout.currentText()
        self.settings_custom['network_graphs']['node_font'] = self.combo_box_figs_network_graphs_node_font.currentFont().family()
        self.settings_custom['network_graphs']['node_font_size'] = self.spin_box_figs_network_graphs_node_font_size.value()
        self.settings_custom['network_graphs']['edge_font'] = self.combo_box_figs_network_graphs_edge_font.currentFont().family()
        self.settings_custom['network_graphs']['edge_font_size'] = self.spin_box_figs_network_graphs_edge_font_size.value()
        self.settings_custom['network_graphs']['edge_color'] = self.label_figs_network_graphs_edge_color_pick.get_color()

        self.change_fonts()

        return True
