#
# Wordless: Settings - Figures
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import copy
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import wordcloud

from wl_widgets import wl_box, wl_layout, wl_tree, wl_widgets

class Wl_Settings_Figs(wl_tree.Wl_Settings):
    def __init__(self, main):
        super().__init__(main)

        # Line Chart
        group_box_figs_line_chart = QGroupBox(self.tr('Line Chart'), self)

        self.label_figs_line_chart_font = QLabel(self.tr('Font:'), self)
        self.combo_box_figs_line_chart_font = wl_box.Wl_Combo_Box_Font_Family(self)

        group_box_figs_line_chart.setLayout(wl_layout.Wl_Layout())
        group_box_figs_line_chart.layout().addWidget(self.label_figs_line_chart_font, 0, 0)
        group_box_figs_line_chart.layout().addWidget(self.combo_box_figs_line_chart_font, 0, 1)

        group_box_figs_line_chart.layout().setColumnStretch(2, 1)

        # Word Cloud
        group_box_figs_word_cloud = QGroupBox(self.tr('Word Cloud'), self)

        self.label_figs_word_cloud_font = QLabel(self.tr('Font:'), self)
        self.combo_box_figs_word_cloud_font = wl_box.Wl_Combo_Box(self)
        self.label_figs_word_cloud_bg_color = QLabel(self.tr('Background Color:'), self)
        (self.label_figs_word_cloud_bg_color_pick,
         self.button_figs_word_cloud_bg_color_pick) = wl_widgets.wl_widgets_pick_color(self)

        self.combo_box_figs_word_cloud_font.addItems([
            'DroidSansMono',
            'Code2000',
            'Unifont'
        ])

        group_box_figs_word_cloud.setLayout(wl_layout.Wl_Layout())
        group_box_figs_word_cloud.layout().addWidget(self.label_figs_word_cloud_font, 0, 0)
        group_box_figs_word_cloud.layout().addWidget(self.combo_box_figs_word_cloud_font, 0, 1, 1, 2)
        group_box_figs_word_cloud.layout().addWidget(self.label_figs_word_cloud_bg_color, 1, 0)
        group_box_figs_word_cloud.layout().addWidget(self.label_figs_word_cloud_bg_color_pick, 1, 1)
        group_box_figs_word_cloud.layout().addWidget(self.button_figs_word_cloud_bg_color_pick, 1, 2)

        group_box_figs_word_cloud.layout().setColumnStretch(3, 1)

        # Network Graph
        group_box_figs_network_graph = QGroupBox(self.tr('Network Graph'), self)

        self.label_figs_network_graph_layout = QLabel(self.tr('Layout:'), self)
        self.combo_box_figs_network_graph_layout = wl_box.Wl_Combo_Box(self)
        self.label_figs_network_graph_node_font = QLabel(self.tr('Node Font:'), self)
        self.combo_box_figs_network_graph_node_font = wl_box.Wl_Combo_Box_Font_Family(self)
        self.label_figs_network_graph_node_font_size = QLabel(self.tr('Node Font Size:'), self)
        self.spin_box_figs_network_graph_node_font_size = wl_box.Wl_Spin_Box_Font_Size(self)
        self.label_figs_network_graph_edge_font = QLabel(self.tr('Edge Font:'), self)
        self.combo_box_figs_network_graph_edge_font = wl_box.Wl_Combo_Box_Font_Family(self)
        self.label_figs_network_graph_edge_font_size = QLabel(self.tr('Edge Font Size:'), self)
        self.spin_box_figs_network_graph_edge_font_size = wl_box.Wl_Spin_Box_Font_Size(self)
        self.label_figs_network_graph_edge_color = QLabel(self.tr('Edge Color:'), self)
        (self.label_figs_network_graph_edge_color_pick,
         self.combo_box_figs_network_graph_color_pick) = wl_widgets.wl_widgets_pick_color(self)

        self.combo_box_figs_network_graph_layout.addItems([
            self.tr('Circular'),
            self.tr('Kamada-Kawai'),
            self.tr('Planar'),
            self.tr('Random'),
            self.tr('Shell'),
            self.tr('Spring'),
            self.tr('Spectral')
        ])

        group_box_figs_network_graph.setLayout(wl_layout.Wl_Layout())
        group_box_figs_network_graph.layout().addWidget(self.label_figs_network_graph_layout, 0, 0)
        group_box_figs_network_graph.layout().addWidget(self.combo_box_figs_network_graph_layout, 0, 1, 1, 2)
        group_box_figs_network_graph.layout().addWidget(self.label_figs_network_graph_node_font, 1, 0)
        group_box_figs_network_graph.layout().addWidget(self.combo_box_figs_network_graph_node_font, 1, 1, 1, 2)
        group_box_figs_network_graph.layout().addWidget(self.label_figs_network_graph_node_font_size, 2, 0)
        group_box_figs_network_graph.layout().addWidget(self.spin_box_figs_network_graph_node_font_size, 2, 1, 1, 2)
        group_box_figs_network_graph.layout().addWidget(self.label_figs_network_graph_edge_font, 3, 0)
        group_box_figs_network_graph.layout().addWidget(self.combo_box_figs_network_graph_edge_font, 3, 1, 1, 2)
        group_box_figs_network_graph.layout().addWidget(self.label_figs_network_graph_edge_font_size, 4, 0)
        group_box_figs_network_graph.layout().addWidget(self.spin_box_figs_network_graph_edge_font_size, 4, 1, 1, 2)
        group_box_figs_network_graph.layout().addWidget(self.label_figs_network_graph_edge_color, 5, 0)
        group_box_figs_network_graph.layout().addWidget(self.label_figs_network_graph_edge_color_pick, 5, 1)
        group_box_figs_network_graph.layout().addWidget(self.combo_box_figs_network_graph_color_pick, 5, 2)

        group_box_figs_network_graph.layout().setColumnStretch(3, 1)

        self.setLayout(wl_layout.Wl_Layout())
        self.layout().addWidget(group_box_figs_line_chart, 0, 0)
        self.layout().addWidget(group_box_figs_word_cloud, 1, 0)
        self.layout().addWidget(group_box_figs_network_graph, 2, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(3, 1)

    def change_wordcloud_font(self):
        font_dir = os.path.split(wordcloud.wordcloud.FONT_PATH)[0]

        if self.main.settings_custom['figs']['word_cloud']['font'] == 'DroidSansMono':
            wordcloud.wordcloud.FONT_PATH = os.path.join(font_dir, 'DroidSansMono.ttf')
        elif self.main.settings_custom['figs']['word_cloud']['font'] == 'Code2000':
            wordcloud.wordcloud.FONT_PATH = os.path.join(font_dir, 'Code2000.ttf')
        elif self.main.settings_custom['figs']['word_cloud']['font'] == 'Unifont':
            wordcloud.wordcloud.FONT_PATH = os.path.join(font_dir, 'unifont-12.1.03.ttf')

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default)
        else:
            settings = copy.deepcopy(self.main.settings_custom)

        self.combo_box_figs_line_chart_font.setCurrentText(settings['figs']['line_chart']['font'])

        self.combo_box_figs_word_cloud_font.setCurrentText(settings['figs']['word_cloud']['font'])
        self.label_figs_word_cloud_bg_color_pick.set_color(settings['figs']['word_cloud']['bg_color'])

        self.combo_box_figs_network_graph_layout.setCurrentText(settings['figs']['network_graph']['layout'])
        self.combo_box_figs_network_graph_node_font.setCurrentText(settings['figs']['network_graph']['node_font'])
        self.spin_box_figs_network_graph_node_font_size.setValue(settings['figs']['network_graph']['node_font_size'])
        self.combo_box_figs_network_graph_edge_font.setCurrentText(settings['figs']['network_graph']['edge_font'])
        self.spin_box_figs_network_graph_edge_font_size.setValue(settings['figs']['network_graph']['edge_font_size'])
        self.label_figs_network_graph_edge_color_pick.set_color(settings['figs']['network_graph']['edge_color'])

        # Change wordcloud's default font
        self.change_wordcloud_font()

    def apply_settings(self):
        settings = self.main.settings_custom

        settings['figs']['line_chart']['font'] = self.combo_box_figs_line_chart_font.currentText()

        settings['figs']['word_cloud']['font'] = self.combo_box_figs_word_cloud_font.currentText()
        settings['figs']['word_cloud']['bg_color'] = self.label_figs_word_cloud_bg_color_pick.get_color()

        settings['figs']['network_graph']['layout'] = self.combo_box_figs_network_graph_layout.currentText()
        settings['figs']['network_graph']['node_font'] = self.combo_box_figs_network_graph_node_font.currentText()
        settings['figs']['network_graph']['node_font_size'] = self.spin_box_figs_network_graph_node_font_size.value()
        settings['figs']['network_graph']['edge_font'] = self.combo_box_figs_network_graph_edge_font.currentText()
        settings['figs']['network_graph']['edge_font_size'] = self.spin_box_figs_network_graph_edge_font_size.value()
        settings['figs']['network_graph']['edge_color'] = self.label_figs_network_graph_edge_color_pick.get_color()

        # Change wordcloud's default font
        self.change_wordcloud_font()

        return True
