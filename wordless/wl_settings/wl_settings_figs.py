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
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from wordless.wl_settings import wl_settings
from wordless.wl_utils import wl_paths
from wordless.wl_widgets import (
    wl_boxes,
    wl_buttons,
    wl_editors,
    wl_layouts
)

_tr = QtCore.QCoreApplication.translate

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
MATPLOTLIB_HOR_ALIGNMENT = {
    _tr('wl_settings_figs', 'Center'): 'center',
    _tr('wl_settings_figs', 'Right'): 'right',
    _tr('wl_settings_figs', 'Left'): 'left'
}
MATPLOTLIB_VERT_ALIGNMENT = {
    _tr('wl_settings_figs', 'Center'): 'center',
    _tr('wl_settings_figs', 'Top'): 'top',
    _tr('wl_settings_figs', 'Bottom'): 'bottom',
    _tr('wl_settings_figs', 'Baseline'): 'baseline',
    _tr('wl_settings_figs', 'Center baseline'): 'center_baseline'
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
        self.group_box_general_settings = QtWidgets.QGroupBox(self.tr('General Settings'), self)

        self.label_font = QtWidgets.QLabel(self.tr('Font:'), self)
        self.combo_box_font = wl_boxes.Wl_Combo_Box_Font_Family(self)

        self.group_box_general_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_general_settings.layout().addWidget(self.label_font, 0, 0)
        self.group_box_general_settings.layout().addWidget(self.combo_box_font, 0, 1)

        self.group_box_general_settings.layout().setColumnStretch(2, 1)

        self.layout().addWidget(self.group_box_general_settings, 0, 0)

        self.layout().setRowStretch(1, 1)

    def change_fonts(self):
        matplotlib.rcParams['font.family'] = self.settings_custom['general_settings']['font']

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        # General Settings
        self.combo_box_font.setCurrentFont(QtGui.QFont(settings['general_settings']['font']))

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
        self.group_box_font_settings = QtWidgets.QGroupBox(self.tr('Font Settings'), self)

        desktop_widget = QtWidgets.QDesktopWidget()

        self.label_font = QtWidgets.QLabel(self.tr('Font:'), self)
        self.combo_box_font = wl_boxes.Wl_Combo_Box(self)
        self.line_edit_font_path = wl_editors.Wl_Line_Edit_Path_File(self)
        self.button_font_path_browse = wl_buttons.Wl_Button_Browse(
            parent = self,
            line_edit = self.line_edit_font_path,
            caption = self.tr('Select Font'),
            filters = self.main.settings_global['file_types']['fonts']
        )

        self.label_font_size = QtWidgets.QLabel(self.tr('Font size:'), self)

        (
            self.label_font_size_min, self.spin_box_font_size_min,
            self.label_font_size_max, self.spin_box_font_size_max
        ) = wl_boxes.wl_spin_boxes_min_max(
            self,
            label_min = self.tr('Minimum'), label_max = self.tr('Maximum'),
            val_min = 1, val_max = desktop_widget.height()
        )

        self.label_relative_scaling = QtWidgets.QLabel(self.tr('Relative scaling:'), self)
        self.double_spin_box_relative_scaling = wl_boxes.Wl_Double_Spin_Box(self)

        self.label_font_color = QtWidgets.QLabel(self.tr('Font color:'), self)
        self.combo_box_font_color = wl_boxes.Wl_Combo_Box(self)
        self.stacked_widget_font_color = wl_layouts.Wl_Stacked_Widget_Resizable(self)
        self.button_font_color_monochrome = wl_buttons.Wl_Button_Color(self)
        self.combo_box_font_color_colormap = wl_boxes.Wl_Combo_Box(self)
        self.label_font_color_colormap = QtWidgets.QLabel('', self)

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
        self.group_box_bg_settings = QtWidgets.QGroupBox(self.tr('Background Settings'), self)

        self.label_bg_color = QtWidgets.QLabel(self.tr('Background color:'), self)
        (
            self.button_bg_color,
            self.checkbox_bg_color_transparent
        ) = wl_buttons.wl_button_color_transparent(self)

        self.group_box_bg_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_bg_settings.layout().addWidget(self.label_bg_color, 0, 0)
        self.group_box_bg_settings.layout().addWidget(self.button_bg_color, 0, 1)
        self.group_box_bg_settings.layout().addWidget(self.checkbox_bg_color_transparent, 0, 2)

        self.group_box_bg_settings.layout().setColumnStretch(3, 1)

        # Mask Settings
        self.group_box_mask_settings = QtWidgets.QGroupBox(self.tr('Mask Settings'), self)
        self.group_box_mask_settings.setCheckable(True)

        self.label_mask_path = QtWidgets.QLabel(self.tr('Mask path:'), self)
        self.line_edit_mask_path = wl_editors.Wl_Line_Edit_Path_File(self)
        self.button_mask_path_browse = wl_buttons.Wl_Button_Browse(
            parent = self,
            line_edit = self.line_edit_mask_path,
            caption = self.tr('Select Mask'),
            filters = self.main.settings_global['file_types']['masks']
        )
        self.label_contour_width = QtWidgets.QLabel(self.tr('Contour width:'), self)
        self.spin_box_contour_width = wl_boxes.Wl_Spin_Box(self)
        self.label_contour_color = QtWidgets.QLabel(self.tr('Contour color:'), self)
        self.button_contour_color = wl_buttons.Wl_Button_Color(self)

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
        self.group_box_advanced_settings = QtWidgets.QGroupBox(self.tr('Advanced Settings'), self)

        self.label_prefer_hor = QtWidgets.QLabel(self.tr('Prefer horizontal:'), self)
        self.spin_box_prefer_hor = wl_boxes.Wl_Spin_Box(self)
        self.checkbox_allow_repeated_words = QtWidgets.QCheckBox(self.tr('Allow repeated words'), self)

        self.spin_box_prefer_hor.setRange(0, 100)
        self.spin_box_prefer_hor.setSuffix('%')

        self.group_box_advanced_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_advanced_settings.layout().addWidget(self.label_prefer_hor, 0, 0)
        self.group_box_advanced_settings.layout().addWidget(self.spin_box_prefer_hor, 0, 1)
        self.group_box_advanced_settings.layout().addWidget(self.checkbox_allow_repeated_words, 1, 0, 1, 2)

        self.group_box_advanced_settings.layout().setColumnStretch(2, 1)

        self.layout().addWidget(self.group_box_font_settings, 0, 0)
        self.layout().addWidget(self.group_box_bg_settings, 1, 0)
        self.layout().addWidget(self.group_box_mask_settings, 2, 0)
        self.layout().addWidget(self.group_box_advanced_settings, 3, 0)

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

            self.label_font_color_colormap.setPixmap(QtGui.QPixmap(path_colormap_temp))
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
            and not self.line_edit_font_path.validate(self.settings_custom['font_settings']['font_path'])
        ):
            return False
        elif (
            self.group_box_mask_settings.isChecked()
            and (
                self.group_box_mask_settings.isChecked() != self.settings_custom['mask_settings']['mask_settings']
                or self.line_edit_mask_path.text() != self.settings_custom['mask_settings']['mask_path']
            )
            and not self.line_edit_mask_path.validate(self.settings_custom['mask_settings']['mask_path'])
        ):
            return False
        else:
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
        self.group_box_node_settings = QtWidgets.QGroupBox(self.tr('Node Settings'), self)

        self.label_node_shape = QtWidgets.QLabel(self.tr('Node shape:'), self)
        self.combo_box_node_shape = wl_boxes.Wl_Combo_Box_Enums(self, enums = MATPLOTLIB_SHAPES)
        self.label_node_size = QtWidgets.QLabel(self.tr('Node size:'), self)
        self.spin_box_node_size = wl_boxes.Wl_Spin_Box(self)
        self.label_node_color = QtWidgets.QLabel(self.tr('Node color:'), self)
        self.button_node_color = wl_buttons.Wl_Button_Color(self)
        self.label_node_opacity = QtWidgets.QLabel(self.tr('Node opacity:'), self)
        self.double_spin_box_node_opacity = wl_boxes.Wl_Double_Spin_Box_Alpha(self)
        self.label_border_width = QtWidgets.QLabel(self.tr('Border width:'), self)
        self.spin_box_border_width = wl_boxes.Wl_Spin_Box(self)
        self.label_border_color = QtWidgets.QLabel(self.tr('Border color:'), self)
        self.button_border_color = wl_buttons.Wl_Button_Color(self)
        self.checkbox_same_as_node_color = QtWidgets.QCheckBox(self.tr('Same as node color'), self)

        self.spin_box_node_size.setRange(1, 1000)
        self.spin_box_border_width.setRange(0, 1000)

        self.checkbox_same_as_node_color.stateChanged.connect(self.settings_changed)

        self.group_box_node_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_node_settings.layout().addWidget(self.label_node_shape, 0, 0)
        self.group_box_node_settings.layout().addWidget(self.combo_box_node_shape, 0, 1)
        self.group_box_node_settings.layout().addWidget(self.label_node_size, 1, 0)
        self.group_box_node_settings.layout().addWidget(self.spin_box_node_size, 1, 1)
        self.group_box_node_settings.layout().addWidget(self.label_node_color, 2, 0)
        self.group_box_node_settings.layout().addWidget(self.button_node_color, 2, 1)
        self.group_box_node_settings.layout().addWidget(self.label_node_opacity, 3, 0)
        self.group_box_node_settings.layout().addWidget(self.double_spin_box_node_opacity, 3, 1)
        self.group_box_node_settings.layout().addWidget(self.label_border_width, 4, 0)
        self.group_box_node_settings.layout().addWidget(self.spin_box_border_width, 4, 1)
        self.group_box_node_settings.layout().addWidget(self.label_border_color, 5, 0)
        self.group_box_node_settings.layout().addWidget(self.button_border_color, 5, 1)
        self.group_box_node_settings.layout().addWidget(self.checkbox_same_as_node_color, 5, 2)

        self.group_box_node_settings.layout().setColumnStretch(3, 1)

        # Node Label Settings
        self.group_box_node_label_settings = QtWidgets.QGroupBox(self.tr('Node Label Settings'), self)

        self.label_node_font_family = QtWidgets.QLabel(self.tr('Font family:'), self)
        self.combo_box_node_font_family = wl_boxes.Wl_Combo_Box_Font_Family(self)
        self.label_node_font_size = QtWidgets.QLabel(self.tr('Font size:'), self)
        self.spin_box_node_font_size = wl_boxes.Wl_Spin_Box_Font_Size(self)
        self.label_node_font_weight = QtWidgets.QLabel(self.tr('Font weight:'), self)
        self.spin_box_node_font_weight = wl_boxes.Wl_Spin_Box_Font_Weight(self)
        self.label_node_font_color = QtWidgets.QLabel(self.tr('Font color:'), self)
        self.button_node_font_color = wl_buttons.Wl_Button_Color(self)
        self.label_node_label_opacity = QtWidgets.QLabel(self.tr('Label opacity:'), self)
        self.double_spin_box_node_label_opacity = wl_boxes.Wl_Double_Spin_Box_Alpha(self)
        self.label_node_hor_alignment = QtWidgets.QLabel(self.tr('Horizontal alignment:'), self)
        self.combo_box_node_hor_alignment = wl_boxes.Wl_Combo_Box_Enums(self, enums = MATPLOTLIB_HOR_ALIGNMENT)
        self.label_node_vert_alignment = QtWidgets.QLabel(self.tr('Vertical alignment:'), self)
        self.combo_box_node_vert_alignment = wl_boxes.Wl_Combo_Box_Enums(self, enums = MATPLOTLIB_VERT_ALIGNMENT)

        self.group_box_node_label_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_node_label_settings.layout().addWidget(self.label_node_font_family, 0, 0)
        self.group_box_node_label_settings.layout().addWidget(self.combo_box_node_font_family, 0, 1)
        self.group_box_node_label_settings.layout().addWidget(self.label_node_font_size, 1, 0)
        self.group_box_node_label_settings.layout().addWidget(self.spin_box_node_font_size, 1, 1)
        self.group_box_node_label_settings.layout().addWidget(self.label_node_font_weight, 2, 0)
        self.group_box_node_label_settings.layout().addWidget(self.spin_box_node_font_weight, 2, 1)
        self.group_box_node_label_settings.layout().addWidget(self.label_node_font_color, 3, 0)
        self.group_box_node_label_settings.layout().addWidget(self.button_node_font_color, 3, 1)
        self.group_box_node_label_settings.layout().addWidget(self.label_node_label_opacity, 4, 0)
        self.group_box_node_label_settings.layout().addWidget(self.double_spin_box_node_label_opacity, 4, 1)
        self.group_box_node_label_settings.layout().addWidget(self.label_node_hor_alignment, 5, 0)
        self.group_box_node_label_settings.layout().addWidget(self.combo_box_node_hor_alignment, 5, 1)
        self.group_box_node_label_settings.layout().addWidget(self.label_node_vert_alignment, 6, 0)
        self.group_box_node_label_settings.layout().addWidget(self.combo_box_node_vert_alignment, 6, 1)

        self.group_box_node_label_settings.layout().setColumnStretch(2, 1)

        # Edge Settings
        self.group_box_edge_settings = QtWidgets.QGroupBox(self.tr('Edge Settings'), self)

        self.label_connection_style = QtWidgets.QLabel(self.tr('Connection style:'), self)
        self.combo_box_connection_style = wl_boxes.Wl_Combo_Box_Enums(self, enums = MATPLOTLIB_CONNECTION_STYLES)
        self.label_edge_width = QtWidgets.QLabel(self.tr('Edge width:'), self)

        (
            self.label_edge_width_min, self.double_spin_box_edge_width_min,
            self.label_edge_width_max, self.double_spin_box_edge_width_max
        ) = wl_boxes.wl_spin_boxes_min_max(
            self,
            label_min = self.tr('Minimum'), label_max = self.tr('Maximum'),
            val_min = 0.1, val_max = 10,
            double = True
        )

        self.label_edge_style = QtWidgets.QLabel(self.tr('Edge style:'), self)
        self.combo_box_edge_style = wl_boxes.Wl_Combo_Box_Enums(self, enums = MATPLOTLIB_LINE_STYLES)
        self.label_edge_color = QtWidgets.QLabel(self.tr('Edge color:'), self)
        self.button_edge_color = wl_buttons.Wl_Button_Color(self)
        self.label_edge_opacity = QtWidgets.QLabel(self.tr('Edge opacity:'), self)
        self.double_spin_box_edge_opacity = wl_boxes.Wl_Double_Spin_Box_Alpha(self)
        self.label_arrow_style = QtWidgets.QLabel(self.tr('Arrow style:'), self)
        self.combo_box_arrow_style = wl_boxes.Wl_Combo_Box_Enums(self, enums = MATPLOTLIB_ARROW_STYLES)
        self.label_arrow_size = QtWidgets.QLabel(self.tr('Arrow size:'), self)
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
        self.group_box_edge_label_settings = QtWidgets.QGroupBox(self.tr('Edge Label Settings'), self)

        self.label_label_position = QtWidgets.QLabel(self.tr('Label position:'), self)
        self.double_spin_box_label_position = wl_boxes.Wl_Double_Spin_Box_Alpha(self)
        self.checkbox_rotate_labels = QtWidgets.QCheckBox(self.tr('Rotate labels to lie parallel to edges'), self)
        self.label_edge_font_family = QtWidgets.QLabel(self.tr('Font family:'), self)
        self.combo_box_edge_font_family = wl_boxes.Wl_Combo_Box_Font_Family(self)
        self.label_edge_font_size = QtWidgets.QLabel(self.tr('Font size:'), self)
        self.spin_box_edge_font_size = wl_boxes.Wl_Spin_Box_Font_Size(self)
        self.label_edge_font_weight = QtWidgets.QLabel(self.tr('Font weight:'), self)
        self.spin_box_edge_font_weight = wl_boxes.Wl_Spin_Box_Font_Weight(self)
        self.label_edge_font_color = QtWidgets.QLabel(self.tr('Font color:'), self)
        self.button_edge_font_color = wl_buttons.Wl_Button_Color(self)
        self.label_edge_label_opacity = QtWidgets.QLabel(self.tr('Label opacity:'), self)
        self.double_spin_box_edge_label_opacity = wl_boxes.Wl_Double_Spin_Box_Alpha(self)
        self.label_edge_hor_alignment = QtWidgets.QLabel(self.tr('Horizontal alignment:'), self)
        self.combo_box_edge_hor_alignment = wl_boxes.Wl_Combo_Box_Enums(self, enums = MATPLOTLIB_HOR_ALIGNMENT)
        self.label_edge_vert_alignment = QtWidgets.QLabel(self.tr('Vertical alignment:'), self)
        self.combo_box_edge_vert_alignment = wl_boxes.Wl_Combo_Box_Enums(self, enums = MATPLOTLIB_VERT_ALIGNMENT)

        self.group_box_edge_label_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_edge_label_settings.layout().addWidget(self.label_label_position, 0, 0)
        self.group_box_edge_label_settings.layout().addWidget(self.double_spin_box_label_position, 0, 1)
        self.group_box_edge_label_settings.layout().addWidget(self.checkbox_rotate_labels, 1, 0, 1, 2)
        self.group_box_edge_label_settings.layout().addWidget(self.label_edge_font_family, 2, 0)
        self.group_box_edge_label_settings.layout().addWidget(self.combo_box_edge_font_family, 2, 1)
        self.group_box_edge_label_settings.layout().addWidget(self.label_edge_font_size, 3, 0)
        self.group_box_edge_label_settings.layout().addWidget(self.spin_box_edge_font_size, 3, 1)
        self.group_box_edge_label_settings.layout().addWidget(self.label_edge_font_weight, 4, 0)
        self.group_box_edge_label_settings.layout().addWidget(self.spin_box_edge_font_weight, 4, 1)
        self.group_box_edge_label_settings.layout().addWidget(self.label_edge_font_color, 5, 0)
        self.group_box_edge_label_settings.layout().addWidget(self.button_edge_font_color, 5, 1)
        self.group_box_edge_label_settings.layout().addWidget(self.label_edge_label_opacity, 6, 0)
        self.group_box_edge_label_settings.layout().addWidget(self.double_spin_box_edge_label_opacity, 6, 1)
        self.group_box_edge_label_settings.layout().addWidget(self.label_edge_hor_alignment, 7, 0)
        self.group_box_edge_label_settings.layout().addWidget(self.combo_box_edge_hor_alignment, 7, 1)
        self.group_box_edge_label_settings.layout().addWidget(self.label_edge_vert_alignment, 8, 0)
        self.group_box_edge_label_settings.layout().addWidget(self.combo_box_edge_vert_alignment, 8, 1)

        self.group_box_edge_label_settings.layout().setColumnStretch(2, 1)

        # Advanced Settings
        self.group_box_advanced_settings = QtWidgets.QGroupBox(self.tr('Advanced Settings'), self)

        self.label_layout = QtWidgets.QLabel(self.tr('Layout:'), self)
        self.combo_box_layout = wl_boxes.Wl_Combo_Box_Enums(self, enums = NETWORKX_LAYOUTS)

        self.group_box_advanced_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_advanced_settings.layout().addWidget(self.label_layout, 0, 0)
        self.group_box_advanced_settings.layout().addWidget(self.combo_box_layout, 0, 1)

        self.group_box_advanced_settings.layout().setColumnStretch(2, 1)

        self.layout().addWidget(self.group_box_node_settings, 0, 0)
        self.layout().addWidget(self.group_box_node_label_settings, 1, 0)
        self.layout().addWidget(self.group_box_edge_settings, 2, 0)
        self.layout().addWidget(self.group_box_edge_label_settings, 3, 0)
        self.layout().addWidget(self.group_box_advanced_settings, 4, 0)

        self.layout().setRowStretch(5, 1)

        self.settings_changed()

    def settings_changed(self):
        if self.checkbox_same_as_node_color.isChecked():
            self.button_border_color.setEnabled(False)
        else:
            self.button_border_color.setEnabled(True)

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
        self.spin_box_border_width.setValue(settings['node_settings']['border_width'])
        self.button_border_color.set_color(settings['node_settings']['border_color'])
        self.checkbox_same_as_node_color.setChecked(settings['node_settings']['same_as_node_color'])

        # Node Label Settings
        self.combo_box_node_font_family.setCurrentFont(QtGui.QFont(settings['node_label_settings']['font_family']))
        self.spin_box_node_font_size.setValue(settings['node_label_settings']['font_size'])
        self.spin_box_node_font_weight.setValue(settings['node_label_settings']['font_weight'])
        self.button_node_font_color.set_color(settings['node_label_settings']['font_color'])
        self.double_spin_box_node_label_opacity.setValue(settings['node_label_settings']['label_opacity'])
        self.combo_box_node_hor_alignment.set_val(settings['node_label_settings']['hor_alignment'])
        self.combo_box_node_vert_alignment.set_val(settings['node_label_settings']['vert_alignment'])

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
        self.combo_box_edge_font_family.setCurrentFont(QtGui.QFont(settings['edge_label_settings']['font_family']))
        self.spin_box_edge_font_size.setValue(settings['edge_label_settings']['font_size'])
        self.spin_box_edge_font_weight.setValue(settings['edge_label_settings']['font_weight'])
        self.button_edge_font_color.set_color(settings['edge_label_settings']['font_color'])
        self.double_spin_box_edge_label_opacity.setValue(settings['edge_label_settings']['label_opacity'])
        self.combo_box_edge_hor_alignment.set_val(settings['edge_label_settings']['hor_alignment'])
        self.combo_box_edge_vert_alignment.set_val(settings['edge_label_settings']['vert_alignment'])

        # Advanced Settings
        self.combo_box_layout.set_val(settings['advanced_settings']['layout'])

    def apply_settings(self):
        # Node Settings
        self.settings_custom['node_settings']['node_shape'] = self.combo_box_node_shape.get_val()
        self.settings_custom['node_settings']['node_size'] = self.spin_box_node_size.value()
        self.settings_custom['node_settings']['node_color'] = self.button_node_color.get_color()
        self.settings_custom['node_settings']['node_opacity'] = self.double_spin_box_node_opacity.value()
        self.settings_custom['node_settings']['border_width'] = self.spin_box_border_width.value()
        self.settings_custom['node_settings']['border_color'] = self.button_border_color.get_color()
        self.settings_custom['node_settings']['same_as_node_color'] = self.checkbox_same_as_node_color.isChecked()

        # Node Label Settings
        self.settings_custom['node_label_settings']['font_family'] = self.combo_box_node_font_family.currentFont().family()
        self.settings_custom['node_label_settings']['font_size'] = self.spin_box_node_font_size.value()
        self.settings_custom['node_label_settings']['font_weight'] = self.spin_box_node_font_weight.value()
        self.settings_custom['node_label_settings']['font_color'] = self.button_node_font_color.get_color()
        self.settings_custom['node_label_settings']['label_opacity'] = self.double_spin_box_node_label_opacity.value()
        self.settings_custom['node_label_settings']['hor_alignment'] = self.combo_box_node_hor_alignment.get_val()
        self.settings_custom['node_label_settings']['vert_alignment'] = self.combo_box_node_vert_alignment.get_val()

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
        self.settings_custom['edge_label_settings']['font_family'] = self.combo_box_edge_font_family.currentFont().family()
        self.settings_custom['edge_label_settings']['font_size'] = self.spin_box_edge_font_size.value()
        self.settings_custom['edge_label_settings']['font_weight'] = self.spin_box_edge_font_weight.value()
        self.settings_custom['edge_label_settings']['font_color'] = self.button_edge_font_color.get_color()
        self.settings_custom['edge_label_settings']['label_opacity'] = self.double_spin_box_edge_label_opacity.value()
        self.settings_custom['edge_label_settings']['hor_alignment'] = self.combo_box_edge_hor_alignment.get_val()
        self.settings_custom['edge_label_settings']['vert_alignment'] = self.combo_box_edge_vert_alignment.get_val()

        # Advanced Settings
        self.settings_custom['advanced_settings']['layout'] = self.combo_box_layout.get_val()

        return True
