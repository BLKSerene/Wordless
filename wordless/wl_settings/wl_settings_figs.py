# ----------------------------------------------------------------------
# Wordless: Settings - Figures
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

import matplotlib
import matplotlib.backends.backend_qtagg
import matplotlib.pyplot
import networkx
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (
    QCheckBox,
    QDesktopWidget,
    QGroupBox,
    QLabel,
    QLineEdit
)

from wordless.wl_settings import wl_settings
from wordless.wl_utils import wl_paths
from wordless.wl_widgets import wl_boxes, wl_buttons, wl_layouts

_tr = QCoreApplication.translate

MATPLOTLIB_SHAPES = {
    _tr('wl_settings_figs', 'Square'): 's',
    _tr('wl_settings_figs', 'Circle'): 'o',
    _tr('wl_settings_figs', 'Triangle up'): '^',
    _tr('wl_settings_figs', 'Triangle right'): '>',
    _tr('wl_settings_figs', 'Triangle down'): 'v',
    _tr('wl_settings_figs', 'Triangle left'): '<',
    _tr('wl_settings_figs', 'Thin diamond'): 'd',
    _tr('wl_settings_figs', 'Pentagon'): 'p',
    _tr('wl_settings_figs', 'Hexagon'): 'h',
    _tr('wl_settings_figs', 'Octagon'): '8'
}
MATPLOTLIB_CONNECTION_STYLES = {
    _tr('wl_settings_figs', 'Arc3'): 'arc3',
    _tr('wl_settings_figs', 'Arc'): 'arc',
    _tr('wl_settings_figs', 'Angle3'): 'angle3',
    _tr('wl_settings_figs', 'Angle'): 'angle',
    _tr('wl_settings_figs', 'Bar'): 'bar'
}
MATPLOTLIB_LINE_STYLES = {
    _tr('wl_settings_figs', 'Solid'): 'solid',
    _tr('wl_settings_figs', 'Dashed'): 'dashed',
    _tr('wl_settings_figs', 'Dash-dotted'): 'dashdot',
    _tr('wl_settings_figs', 'Dotted'): 'dotted'
}
MATPLOTLIB_ARROW_STYLES = {
    _tr('wl_settings_figs', 'Curve'): '-',
    _tr('wl_settings_figs', 'Curve A'): '<-',
    _tr('wl_settings_figs', 'Curve B'): '->',
    _tr('wl_settings_figs', 'Curve AB'): '<->',
    _tr('wl_settings_figs', 'Curve filled A'): '<|-',
    _tr('wl_settings_figs', 'Curve filled B'): '-|>',
    _tr('wl_settings_figs', 'Curve filled AB'): '<|-|>',
    _tr('wl_settings_figs', 'Bracket A'): ']-',
    _tr('wl_settings_figs', 'Bracket B'): '-[',
    _tr('wl_settings_figs', 'Bracket AB'): ']-[',
    _tr('wl_settings_figs', 'Bar AB'): '|-|',
    _tr('wl_settings_figs', 'Bracket curve'): '<-[',
    _tr('wl_settings_figs', 'Simple'): 'simple',
    _tr('wl_settings_figs', 'Fancy'): 'fancy',
    _tr('wl_settings_figs', 'Wedge'): 'wedge'
}
NETWORKX_LAYOUTS = {
    _tr('wl_settings_figs', 'Circular'): networkx.circular_layout,
    'Kamada-Kawai': networkx.kamada_kawai_layout,
    _tr('wl_settings_figs', 'Planar'): networkx.planar_layout,
    _tr('wl_settings_figs', 'Random'): networkx.random_layout,
    _tr('wl_settings_figs', 'Shell'): networkx.shell_layout,
    _tr('wl_settings_figs', 'Spring'): networkx.spring_layout,
    _tr('wl_settings_figs', 'Spectral'): networkx.spectral_layout,
    _tr('wl_settings_figs', 'Spiral'): networkx.spiral_layout
}

# Figures - Line Charts
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

# Figures - Word Clouds
class Wl_Settings_Figs_Word_Clouds(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['figs']['word_clouds']
        self.settings_custom = self.main.settings_custom['figs']['word_clouds']

        # Font Settings
        self.group_box_font_settings = QGroupBox(self.tr('Font Settings'), self)

        desktop_widget = QDesktopWidget()

        self.label_font = QLabel(self.tr('Font:'), self)
        self.combo_box_font = wl_boxes.Wl_Combo_Box(self)
        self.line_edit_font_path = QLineEdit(self)
        self.button_font_path_browse = wl_buttons.Wl_Button_Browse(
            parent = self,
            line_edit = self.line_edit_font_path,
            caption = self.tr('Select Font'),
            filters = self.main.settings_global['file_types']['fonts']
        )

        self.label_font_size = QLabel(self.tr('Font size:'), self)

        (
            self.label_font_size_min, self.spin_box_font_size_min,
            self.label_font_size_max, self.spin_box_font_size_max
        ) = wl_boxes.wl_spin_boxes_min_max(
            self,
            label_min = self.tr('Minimum'), label_max = self.tr('Maximum'),
            val_min = 1, val_max = desktop_widget.height()
        )

        self.label_relative_scaling = QLabel(self.tr('Relative scaling:'), self)
        self.double_spin_box_relative_scaling = wl_boxes.Wl_Double_Spin_Box(self)

        self.label_font_color = QLabel(self.tr('Font color:'), self)
        self.combo_box_font_color = wl_boxes.Wl_Combo_Box(self)
        self.stacked_widget_font_color = wl_layouts.Wl_Stacked_Widget_Resizable(self)
        self.button_font_color_monochrome = wl_buttons.wl_button_color(self)
        self.combo_box_font_color_colormap = wl_boxes.Wl_Combo_Box(self)
        self.label_font_color_colormap = QLabel('', self)

        self.combo_box_font.addItems([
            'Droid Sans Mono',
            'GNU Unifont',
            self.tr('Custom')
        ])
        self.combo_box_font_color.addItems([
            self.tr('Monochrome'),
            self.tr('Colormap')
        ])
        self.combo_box_font_color_colormap.addItems(matplotlib.pyplot.colormaps()) # pylint: disable=not-callable
        self.stacked_widget_font_color.addWidget(self.button_font_color_monochrome)
        self.stacked_widget_font_color.addWidget(self.combo_box_font_color_colormap)

        self.double_spin_box_relative_scaling.setRange(-0.01, 1)
        self.double_spin_box_relative_scaling.setSingleStep(0.01)
        self.double_spin_box_relative_scaling.setSpecialValueText(self.tr('Auto'))
        self.label_font_color_colormap.setScaledContents(True)

        self.combo_box_font.currentTextChanged.connect(self.font_settings_changed)
        self.combo_box_font_color.currentTextChanged.connect(self.font_settings_changed)
        self.combo_box_font_color_colormap.currentTextChanged.connect(self.font_settings_changed)

        layout_font = wl_layouts.Wl_Layout()
        layout_font.addWidget(self.line_edit_font_path, 0, 0)
        layout_font.addWidget(self.button_font_path_browse, 0, 1)

        layout_font_size_min = wl_layouts.Wl_Layout()
        layout_font_size_min.addWidget(self.label_font_size_min, 0, 0)
        layout_font_size_min.addWidget(self.spin_box_font_size_min, 0, 1)

        layout_font_size_max = wl_layouts.Wl_Layout()
        layout_font_size_max.addWidget(self.label_font_size_max, 0, 0)
        layout_font_size_max.addWidget(self.spin_box_font_size_max, 0, 1)

        self.group_box_font_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_font_settings.layout().addWidget(self.label_font, 0, 0)
        self.group_box_font_settings.layout().addWidget(self.combo_box_font, 0, 1)
        self.group_box_font_settings.layout().addLayout(layout_font, 0, 2, 1, 2)

        self.group_box_font_settings.layout().addWidget(self.label_font_size, 2, 0)
        self.group_box_font_settings.layout().addLayout(layout_font_size_min, 2, 1)
        self.group_box_font_settings.layout().addLayout(layout_font_size_max, 2, 2)
        self.group_box_font_settings.layout().addWidget(self.label_relative_scaling, 3, 0)
        self.group_box_font_settings.layout().addWidget(self.double_spin_box_relative_scaling, 3, 1)

        self.group_box_font_settings.layout().addWidget(self.label_font_color, 4, 0)
        self.group_box_font_settings.layout().addWidget(self.combo_box_font_color, 4, 1)
        self.group_box_font_settings.layout().addWidget(self.stacked_widget_font_color, 4, 2)
        self.group_box_font_settings.layout().addWidget(self.label_font_color_colormap, 4, 3)

        self.group_box_font_settings.layout().setColumnStretch(3, 1)

        # Background Settings
        self.group_box_bg_settings = QGroupBox(self.tr('Background Settings'), self)

        self.label_bg_color = QLabel(self.tr('Background color:'), self)
        (
            self.button_bg_color,
            self.checkbox_bg_color_transparent
        ) = wl_buttons.wl_button_color(self, allow_transparent = True)

        self.group_box_bg_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_bg_settings.layout().addWidget(self.label_bg_color, 0, 0)
        self.group_box_bg_settings.layout().addWidget(self.button_bg_color, 0, 1)
        self.group_box_bg_settings.layout().addWidget(self.checkbox_bg_color_transparent, 0, 2)

        self.group_box_bg_settings.layout().setColumnStretch(3, 1)

        # Mask Settings
        self.group_box_mask_settings = QGroupBox(self.tr('Mask Settings'), self)
        self.group_box_mask_settings.setCheckable(True)

        self.label_mask_path = QLabel(self.tr('Mask path:'), self)
        self.line_edit_mask_path = QLineEdit(self)
        self.button_mask_path_browse = wl_buttons.Wl_Button_Browse(
            parent = self,
            line_edit = self.line_edit_mask_path,
            caption = self.tr('Select Mask'),
            filters = self.main.settings_global['file_types']['masks']
        )
        self.label_contour_width = QLabel(self.tr('Contour width:'), self)
        self.spin_box_contour_width = wl_boxes.Wl_Spin_Box(self)
        self.label_contour_color = QLabel(self.tr('Contour color:'), self)
        self.button_contour_color = wl_buttons.wl_button_color(self)

        self.spin_box_contour_width.setRange(0, 10)

        layout_mask_path = wl_layouts.Wl_Layout()
        layout_mask_path.addWidget(self.line_edit_mask_path, 0, 0)
        layout_mask_path.addWidget(self.button_mask_path_browse, 0, 1)

        self.group_box_mask_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_mask_settings.layout().addWidget(self.label_mask_path, 0, 0)
        self.group_box_mask_settings.layout().addLayout(layout_mask_path, 0, 1, 1, 2)
        self.group_box_mask_settings.layout().addWidget(self.label_contour_width, 1, 0)
        self.group_box_mask_settings.layout().addWidget(self.spin_box_contour_width, 1, 1)
        self.group_box_mask_settings.layout().addWidget(self.label_contour_color, 2, 0)
        self.group_box_mask_settings.layout().addWidget(self.button_contour_color, 2, 1)

        self.group_box_mask_settings.layout().setColumnStretch(2, 1)

        # Advanced Settings
        self.group_box_advanced_settings = QGroupBox(self.tr('Advanced Settings'), self)

        self.label_prefer_hor = QLabel(self.tr('Prefer horizontal:'), self)
        self.spin_box_prefer_hor = wl_boxes.Wl_Spin_Box(self)
        self.checkbox_allow_repeated_words = QCheckBox(self.tr('Allow repeated words'), self)

        self.spin_box_prefer_hor.setRange(0, 100)
        self.spin_box_prefer_hor.setSuffix('%')

        self.group_box_advanced_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_advanced_settings.layout().addWidget(self.label_prefer_hor, 0, 0)
        self.group_box_advanced_settings.layout().addWidget(self.spin_box_prefer_hor, 0, 1)
        self.group_box_advanced_settings.layout().addWidget(self.checkbox_allow_repeated_words, 1, 0, 1, 2)

        self.group_box_advanced_settings.layout().setColumnStretch(2, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.group_box_font_settings, 0, 0)
        self.layout().addWidget(self.group_box_bg_settings, 1, 0)
        self.layout().addWidget(self.group_box_mask_settings, 2, 0)
        self.layout().addWidget(self.group_box_advanced_settings, 3, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(4, 1)

    def font_settings_changed(self):
        if self.combo_box_font.currentText() == self.tr('Custom'):
            self.line_edit_font_path.show()
            self.button_font_path_browse.show()
        else:
            self.line_edit_font_path.hide()
            self.button_font_path_browse.hide()

        if self.combo_box_font_color.currentText() == self.tr('Monochrome'):
            self.stacked_widget_font_color.setCurrentIndex(0)
            self.label_font_color_colormap.hide()
        elif self.combo_box_font_color.currentText() == self.tr('Colormap'):
            self.stacked_widget_font_color.setCurrentIndex(1)
            self.label_font_color_colormap.show()

            # Reference: https://stackoverflow.com/a/58463913
            fig, ax = matplotlib.pyplot.subplots(figsize = (1, .1))
            ax.set_axis_off()

            matplotlib.colorbar.ColorbarBase(
                ax,
                cmap = matplotlib.pyplot.get_cmap(self.combo_box_font_color_colormap.currentText()),
                orientation = 'horizontal'
            )

            path_colormap_temp = wl_paths.get_path_img('_matplotlib_colormap.png')
            fig.savefig(path_colormap_temp, bbox_inches = 'tight', pad_inches = 0)
            matplotlib.pyplot.close()

            self.label_font_color_colormap.setPixmap(QPixmap(path_colormap_temp))
            os.remove(path_colormap_temp)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        # Font Settings
        self.combo_box_font.setCurrentText(settings['font_settings']['font'])
        self.line_edit_font_path.setText(settings['font_settings']['font_path'])

        self.spin_box_font_size_min.setValue(settings['font_settings']['font_size_min'])
        self.spin_box_font_size_max.setValue(settings['font_settings']['font_size_max'])
        self.double_spin_box_relative_scaling.setValue(settings['font_settings']['relative_scaling'])

        self.combo_box_font_color.setCurrentText(settings['font_settings']['font_color'])
        self.button_font_color_monochrome.set_color(settings['font_settings']['font_color_monochrome'])
        self.combo_box_font_color_colormap.setCurrentText(settings['font_settings']['font_color_colormap'])

        # Background Settings
        self.button_bg_color.set_color(settings['bg_settings']['bg_color'])
        self.checkbox_bg_color_transparent.setChecked(settings['bg_settings']['bg_color_transparent'])

        # Mask Settings
        self.group_box_mask_settings.setChecked(settings['mask_settings']['mask_settings'])
        self.line_edit_mask_path.setText(settings['mask_settings']['mask_path'])
        self.spin_box_contour_width.setValue(settings['mask_settings']['contour_width'])
        self.button_contour_color.set_color(settings['mask_settings']['contour_color'])

        # Advanced Settings
        self.spin_box_prefer_hor.setValue(settings['advanced_settings']['prefer_hor'])
        self.checkbox_allow_repeated_words.setChecked(settings['advanced_settings']['allow_repeated_words'])

        self.font_settings_changed()

    # Only validate settings when paths are changed
    def validate_settings(self):
        if (
            self.combo_box_font.currentText() == self.tr('Custom')
            and (
                self.combo_box_font.currentText() != self.settings_custom['font_settings']['font']
                or self.line_edit_font_path.text() != self.settings_custom['font_settings']['font_path']
            )
            and not self.validate_path_file(self.line_edit_font_path)
        ):
            return False

        if (
            self.group_box_mask_settings.isChecked()
            and self.line_edit_mask_path.text() != self.settings_custom['mask_settings']['mask_path']
            and not self.validate_path_file(self.line_edit_mask_path)
        ):
            return False

        return True

    def apply_settings(self):
        # Font Settings
        self.settings_custom['font_settings']['font'] = self.combo_box_font.currentText()
        self.settings_custom['font_settings']['font_path'] = self.line_edit_font_path.text()

        self.settings_custom['font_settings']['font_size_min'] = self.spin_box_font_size_min.value()
        self.settings_custom['font_settings']['font_size_max'] = self.spin_box_font_size_max.value()
        self.settings_custom['font_settings']['relative_scaling'] = self.double_spin_box_relative_scaling.value()

        self.settings_custom['font_settings']['font_color'] = self.combo_box_font_color.currentText()
        self.settings_custom['font_settings']['font_color_monochrome'] = self.button_font_color_monochrome.get_color()
        self.settings_custom['font_settings']['font_color_colormap'] = self.combo_box_font_color_colormap.currentText()

        # Background Settings
        self.settings_custom['bg_settings']['bg_color'] = self.button_bg_color.get_color()
        self.settings_custom['bg_settings']['bg_color_transparent'] = self.checkbox_bg_color_transparent.isChecked()

        # Mask Settings
        self.settings_custom['mask_settings']['mask_settings'] = self.group_box_mask_settings.isChecked()
        self.settings_custom['mask_settings']['mask_path'] = self.line_edit_mask_path.text()
        self.settings_custom['mask_settings']['contour_width'] = self.spin_box_contour_width.value()
        self.settings_custom['mask_settings']['contour_color'] = self.button_contour_color.get_color()

        # Advanced Settings
        self.settings_custom['advanced_settings']['prefer_hor'] = self.spin_box_prefer_hor.value()
        self.settings_custom['advanced_settings']['allow_repeated_words'] = self.checkbox_allow_repeated_words.isChecked()

        return True

# Figures - Network Graphs
class Wl_Settings_Figs_Network_Graphs(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['figs']['network_graphs']
        self.settings_custom = self.main.settings_custom['figs']['network_graphs']

        # Node Settings
        self.group_box_node_settings = QGroupBox(self.tr('Node Settings'), self)

        self.label_node_shape = QLabel(self.tr('Node shape:'), self)
        self.combo_box_node_shape = wl_boxes.Wl_Combo_Box_Enums(self, enums = MATPLOTLIB_SHAPES)
        self.label_node_size = QLabel(self.tr('Node size:'), self)
        self.spin_box_node_size = wl_boxes.Wl_Spin_Box(self)
        self.label_node_color = QLabel(self.tr('Node color:'), self)
        self.button_node_color = wl_buttons.wl_button_color(self)
        self.label_node_opacity = QLabel(self.tr('Node opacity:'), self)
        self.double_spin_box_node_opacity = wl_boxes.Wl_Double_Spin_Box_Alpha(self)

        self.spin_box_node_size.setRange(1, 1000)

        self.group_box_node_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_node_settings.layout().addWidget(self.label_node_shape, 0, 0)
        self.group_box_node_settings.layout().addWidget(self.combo_box_node_shape, 0, 1)
        self.group_box_node_settings.layout().addWidget(self.label_node_size, 1, 0)
        self.group_box_node_settings.layout().addWidget(self.spin_box_node_size, 1, 1)
        self.group_box_node_settings.layout().addWidget(self.label_node_color, 2, 0)
        self.group_box_node_settings.layout().addWidget(self.button_node_color, 2, 1)
        self.group_box_node_settings.layout().addWidget(self.label_node_opacity, 3, 0)
        self.group_box_node_settings.layout().addWidget(self.double_spin_box_node_opacity, 3, 1)

        self.group_box_node_settings.layout().setColumnStretch(2, 1)

        # Node Label Settings
        self.group_box_node_label_settings = QGroupBox(self.tr('Node Label Settings'), self)

        self.label_label_font_node = QLabel(self.tr('Label font:'), self)
        self.combo_box_label_font_node = wl_boxes.Wl_Combo_Box_Font_Family(self)
        self.label_label_font_size_node = QLabel(self.tr('Label font size:'), self)
        self.spin_box_label_font_size_node = wl_boxes.Wl_Spin_Box_Font_Size(self)
        self.label_label_font_weight_node = QLabel(self.tr('Label font weight:'), self)
        self.spin_box_label_font_weight_node = wl_boxes.Wl_Spin_Box_Font_Weight(self)
        self.label_label_font_color_node = QLabel(self.tr('Label font color:'), self)
        self.button_label_font_color_node = wl_buttons.wl_button_color(self)
        self.label_label_opacity_node = QLabel(self.tr('Label opacity:'), self)
        self.double_spin_box_label_opacity_node = wl_boxes.Wl_Double_Spin_Box_Alpha(self)

        self.group_box_node_label_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_node_label_settings.layout().addWidget(self.label_label_font_node, 0, 0)
        self.group_box_node_label_settings.layout().addWidget(self.combo_box_label_font_node, 0, 1)
        self.group_box_node_label_settings.layout().addWidget(self.label_label_font_size_node, 1, 0)
        self.group_box_node_label_settings.layout().addWidget(self.spin_box_label_font_size_node, 1, 1)
        self.group_box_node_label_settings.layout().addWidget(self.label_label_font_weight_node, 2, 0)
        self.group_box_node_label_settings.layout().addWidget(self.spin_box_label_font_weight_node, 2, 1)
        self.group_box_node_label_settings.layout().addWidget(self.label_label_font_color_node, 3, 0)
        self.group_box_node_label_settings.layout().addWidget(self.button_label_font_color_node, 3, 1)
        self.group_box_node_label_settings.layout().addWidget(self.label_label_opacity_node, 4, 0)
        self.group_box_node_label_settings.layout().addWidget(self.double_spin_box_label_opacity_node, 4, 1)

        self.group_box_node_label_settings.layout().setColumnStretch(2, 1)

        # Edge Settings
        self.group_box_edge_settings = QGroupBox(self.tr('Edge Settings'), self)

        self.label_connection_style = QLabel(self.tr('Connection style:'), self)
        self.combo_box_connection_style = wl_boxes.Wl_Combo_Box_Enums(self, enums = MATPLOTLIB_CONNECTION_STYLES)
        self.label_edge_width = QLabel(self.tr('Edge width:'), self)

        (
            self.label_edge_width_min, self.double_spin_box_edge_width_min,
            self.label_edge_width_max, self.double_spin_box_edge_width_max
        ) = wl_boxes.wl_spin_boxes_min_max(
            self,
            label_min = self.tr('Minimum'), label_max = self.tr('Maximum'),
            val_min = 0.1, val_max = 10,
            double = True
        )

        self.label_edge_style = QLabel(self.tr('Edge style:'), self)
        self.combo_box_edge_style = wl_boxes.Wl_Combo_Box_Enums(self, enums = MATPLOTLIB_LINE_STYLES)
        self.label_edge_color = QLabel(self.tr('Edge color:'), self)
        self.button_edge_color = wl_buttons.Wl_Button_Color(self)
        self.label_edge_opacity = QLabel(self.tr('Edge opacity:'), self)
        self.double_spin_box_edge_opacity = wl_boxes.Wl_Double_Spin_Box_Alpha(self)
        self.label_arrow_style = QLabel(self.tr('Arrow style:'), self)
        self.combo_box_arrow_style = wl_boxes.Wl_Combo_Box_Enums(self, enums = MATPLOTLIB_ARROW_STYLES)
        self.label_arrow_size = QLabel(self.tr('Arrow size:'), self)
        self.spin_box_arrow_size = wl_boxes.Wl_Spin_Box(self)

        self.spin_box_arrow_size.setRange(1, 100)

        layout_edge_width = wl_layouts.Wl_Layout()
        layout_edge_width.addWidget(self.label_edge_width_min, 0, 0)
        layout_edge_width.addWidget(self.double_spin_box_edge_width_min, 0, 1)
        layout_edge_width.addWidget(self.label_edge_width_max, 0, 2)
        layout_edge_width.addWidget(self.double_spin_box_edge_width_max, 0, 3)

        self.group_box_edge_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_edge_settings.layout().addWidget(self.label_connection_style, 0, 0)
        self.group_box_edge_settings.layout().addWidget(self.combo_box_connection_style, 0, 1)
        self.group_box_edge_settings.layout().addWidget(self.label_edge_width, 1, 0)
        self.group_box_edge_settings.layout().addLayout(layout_edge_width, 1, 1)
        self.group_box_edge_settings.layout().addWidget(self.label_edge_style, 2, 0)
        self.group_box_edge_settings.layout().addWidget(self.combo_box_edge_style, 2, 1)
        self.group_box_edge_settings.layout().addWidget(self.label_edge_color, 3, 0)
        self.group_box_edge_settings.layout().addWidget(self.button_edge_color, 3, 1)
        self.group_box_edge_settings.layout().addWidget(self.label_edge_opacity, 4, 0)
        self.group_box_edge_settings.layout().addWidget(self.double_spin_box_edge_opacity, 4, 1)
        self.group_box_edge_settings.layout().addWidget(self.label_arrow_style, 6, 0)
        self.group_box_edge_settings.layout().addWidget(self.combo_box_arrow_style, 6, 1)
        self.group_box_edge_settings.layout().addWidget(self.label_arrow_size, 7, 0)
        self.group_box_edge_settings.layout().addWidget(self.spin_box_arrow_size, 7, 1)

        self.group_box_edge_settings.layout().setColumnStretch(2, 1)

        # Edge Label Settings
        self.group_box_edge_label_settings = QGroupBox(self.tr('Edge Label Settings'), self)

        self.label_label_position = QLabel(self.tr('Label position:'), self)
        self.double_spin_box_label_position = wl_boxes.Wl_Double_Spin_Box_Alpha(self)
        self.checkbox_rotate_labels = QCheckBox(self.tr('Rotate labels to lie parallel to edges'), self)
        self.label_label_font_edge = QLabel(self.tr('Label font:'), self)
        self.combo_box_label_font_edge = wl_boxes.Wl_Combo_Box_Font_Family(self)
        self.label_label_font_size_edge = QLabel(self.tr('Label font size:'), self)
        self.spin_box_label_font_size_edge = wl_boxes.Wl_Spin_Box_Font_Size(self)
        self.label_label_font_weight_edge = QLabel(self.tr('Label font weight:'), self)
        self.spin_box_label_font_weight_edge = wl_boxes.Wl_Spin_Box_Font_Weight(self)
        self.label_label_font_color_edge = QLabel(self.tr('Label font color:'), self)
        self.button_label_font_color_edge = wl_buttons.wl_button_color(self)
        self.label_label_opacity_edge = QLabel(self.tr('Label opacity:'), self)
        self.double_spin_box_label_opacity_edge = wl_boxes.Wl_Double_Spin_Box_Alpha(self)

        self.group_box_edge_label_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_edge_label_settings.layout().addWidget(self.label_label_position, 0, 0)
        self.group_box_edge_label_settings.layout().addWidget(self.double_spin_box_label_position, 0, 1)
        self.group_box_edge_label_settings.layout().addWidget(self.checkbox_rotate_labels, 1, 0, 1, 2)
        self.group_box_edge_label_settings.layout().addWidget(self.label_label_font_edge, 2, 0)
        self.group_box_edge_label_settings.layout().addWidget(self.combo_box_label_font_edge, 2, 1)
        self.group_box_edge_label_settings.layout().addWidget(self.label_label_font_size_edge, 3, 0)
        self.group_box_edge_label_settings.layout().addWidget(self.spin_box_label_font_size_edge, 3, 1)
        self.group_box_edge_label_settings.layout().addWidget(self.label_label_font_weight_edge, 4, 0)
        self.group_box_edge_label_settings.layout().addWidget(self.spin_box_label_font_weight_edge, 4, 1)
        self.group_box_edge_label_settings.layout().addWidget(self.label_label_font_color_edge, 5, 0)
        self.group_box_edge_label_settings.layout().addWidget(self.button_label_font_color_edge, 5, 1)
        self.group_box_edge_label_settings.layout().addWidget(self.label_label_opacity_edge, 6, 0)
        self.group_box_edge_label_settings.layout().addWidget(self.double_spin_box_label_opacity_edge, 6, 1)

        self.group_box_edge_label_settings.layout().setColumnStretch(2, 1)

        # Advanced Settings
        self.group_box_advanced_settings = QGroupBox(self.tr('Advanced Settings'), self)

        self.label_layout = QLabel(self.tr('Layout:'), self)
        self.combo_box_layout = wl_boxes.Wl_Combo_Box_Enums(self, enums = NETWORKX_LAYOUTS)

        self.group_box_advanced_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_advanced_settings.layout().addWidget(self.label_layout, 0, 0)
        self.group_box_advanced_settings.layout().addWidget(self.combo_box_layout, 0, 1)

        self.group_box_advanced_settings.layout().setColumnStretch(2, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.group_box_node_settings, 0, 0)
        self.layout().addWidget(self.group_box_node_label_settings, 1, 0)
        self.layout().addWidget(self.group_box_edge_settings, 2, 0)
        self.layout().addWidget(self.group_box_edge_label_settings, 3, 0)
        self.layout().addWidget(self.group_box_advanced_settings, 4, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(5, 1)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        # Node Settings
        self.combo_box_node_shape.set_val(settings['node_settings']['node_shape'])
        self.spin_box_node_size.setValue(settings['node_settings']['node_size'])
        self.button_node_color.set_color(settings['node_settings']['node_color'])
        self.double_spin_box_node_opacity.setValue(settings['node_settings']['node_opacity'])

        # Node Label Settings
        self.combo_box_label_font_node.setCurrentFont(QFont(settings['node_label_settings']['label_font']))
        self.spin_box_label_font_size_node.setValue(settings['node_label_settings']['label_font_size'])
        self.spin_box_label_font_weight_node.setValue(settings['node_label_settings']['label_font_weight'])
        self.button_label_font_color_node.set_color(settings['node_label_settings']['label_font_color'])
        self.double_spin_box_label_opacity_node.setValue(settings['node_label_settings']['label_opacity'])

        # Edge Settings
        self.combo_box_connection_style.set_val(settings['edge_settings']['connection_style'])
        self.double_spin_box_edge_width_min.setValue(settings['edge_settings']['edge_width_min'])
        self.double_spin_box_edge_width_max.setValue(settings['edge_settings']['edge_width_max'])
        self.combo_box_edge_style.set_val(settings['edge_settings']['edge_style'])
        self.button_edge_color.set_color(settings['edge_settings']['edge_color'])
        self.double_spin_box_edge_opacity.setValue(settings['edge_settings']['edge_opacity'])
        self.combo_box_arrow_style.set_val(settings['edge_settings']['arrow_style'])
        self.spin_box_arrow_size.setValue(settings['edge_settings']['arrow_size'])

        # Edge Label Settings
        self.double_spin_box_label_position.setValue(settings['edge_label_settings']['label_position'])
        self.checkbox_rotate_labels.setChecked(settings['edge_label_settings']['rotate_labels'])
        self.combo_box_label_font_edge.setCurrentFont(QFont(settings['edge_label_settings']['label_font']))
        self.spin_box_label_font_size_edge.setValue(settings['edge_label_settings']['label_font_size'])
        self.spin_box_label_font_weight_edge.setValue(settings['edge_label_settings']['label_font_weight'])
        self.button_label_font_color_edge.set_color(settings['edge_label_settings']['label_font_color'])
        self.double_spin_box_label_opacity_edge.setValue(settings['edge_label_settings']['label_opacity'])

        # Advanced Settings
        self.combo_box_layout.set_val(settings['advanced_settings']['layout'])

    def apply_settings(self):
        # Node Settings
        self.settings_custom['node_settings']['node_shape'] = self.combo_box_node_shape.get_val()
        self.settings_custom['node_settings']['node_size'] = self.spin_box_node_size.value()
        self.settings_custom['node_settings']['node_color'] = self.button_node_color.get_color()
        self.settings_custom['node_settings']['node_opacity'] = self.double_spin_box_node_opacity.value()

        # Node Label Settings
        self.settings_custom['node_label_settings']['label_font'] = self.combo_box_label_font_node.currentFont().family()
        self.settings_custom['node_label_settings']['label_font_size'] = self.spin_box_label_font_size_node.value()
        self.settings_custom['node_label_settings']['label_font_weight'] = self.spin_box_label_font_weight_node.value()
        self.settings_custom['node_label_settings']['label_font_color'] = self.button_label_font_color_node.get_color()
        self.settings_custom['node_label_settings']['label_opacity'] = self.double_spin_box_label_opacity_node.value()

        # Edge Settings
        self.settings_custom['edge_settings']['connection_style'] = self.combo_box_connection_style.get_val()
        self.settings_custom['edge_settings']['edge_width_min'] = self.double_spin_box_edge_width_min.value()
        self.settings_custom['edge_settings']['edge_width_max'] = self.double_spin_box_edge_width_max.value()
        self.settings_custom['edge_settings']['edge_style'] = self.combo_box_edge_style.get_val()
        self.settings_custom['edge_settings']['edge_color'] = self.button_edge_color.get_color()
        self.settings_custom['edge_settings']['edge_opacity'] = self.double_spin_box_edge_opacity.value()
        self.settings_custom['edge_settings']['arrow_style'] = self.combo_box_arrow_style.get_val()
        self.settings_custom['edge_settings']['arrow_size'] = self.spin_box_arrow_size.value()

        # Edge Label Settings
        self.settings_custom['edge_label_settings']['label_position'] = self.double_spin_box_label_position.value()
        self.settings_custom['edge_label_settings']['rotate_labels'] = self.checkbox_rotate_labels.isChecked()
        self.settings_custom['edge_label_settings']['label_font'] = self.combo_box_label_font_edge.currentFont().family()
        self.settings_custom['edge_label_settings']['label_font_size'] = self.spin_box_label_font_size_edge.value()
        self.settings_custom['edge_label_settings']['label_font_weight'] = self.spin_box_label_font_weight_edge.value()
        self.settings_custom['edge_label_settings']['label_font_color'] = self.button_label_font_color_edge.get_color()
        self.settings_custom['edge_label_settings']['label_opacity'] = self.double_spin_box_label_opacity_edge.value()

        # Advanced Settings
        self.settings_custom['advanced_settings']['layout'] = self.combo_box_layout.get_val()

        return True
