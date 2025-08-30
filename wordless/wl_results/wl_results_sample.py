# ----------------------------------------------------------------------
# Wordless: Results - Sample
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

import numpy
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from wordless.wl_dialogs import wl_dialogs
from wordless.wl_widgets import (
    wl_boxes,
    wl_buttons,
    wl_layouts
)

_tr = QtCore.QCoreApplication.translate

class Wl_Dialog_Results_Sample(wl_dialogs.Wl_Dialog):
    def __init__(self, main, table):
        super().__init__(
            main,
            title = _tr('Wl_Dialog_Results_Sample', 'Sample'),
            width = 500
        )

        self.tab = table.tab
        self.table = table
        self.settings = self.main.settings_custom[self.tab]['results_sample']

        self.label_sampling_method = QtWidgets.QLabel(self.tr('Sampling Method:'), self)
        self.combo_box_sampling_method = wl_boxes.Wl_Combo_Box(self)

        self.stacked_widget_sample_size_label = wl_layouts.Wl_Stacked_Widget_Resizable(self)
        self.label_sample_size_random = QtWidgets.QLabel(self.tr('Sample Size:'), self)
        self.label_sample_size_systematic_interval = QtWidgets.QLabel(self.tr('Sampling Interval:'), self)
        self.label_sample_size_systematic_size = QtWidgets.QLabel(self.tr('Sample Size:'), self)

        self.stacked_widget_sample_size_val = wl_layouts.Wl_Stacked_Widget_Resizable(self)
        self.spin_box_sample_size_random = wl_boxes.Wl_Spin_Box(self)
        self.spin_box_sample_size_systematic_interval = wl_boxes.Wl_Spin_Box(self)
        self.spin_box_sample_size_systematic_size = wl_boxes.Wl_Spin_Box(self)

        self.stacked_widget_sample_size_label.addWidget(self.label_sample_size_random)
        self.stacked_widget_sample_size_label.addWidget(self.label_sample_size_systematic_interval)
        self.stacked_widget_sample_size_label.addWidget(self.label_sample_size_systematic_size)

        self.stacked_widget_sample_size_val.addWidget(self.spin_box_sample_size_random)
        self.stacked_widget_sample_size_val.addWidget(self.spin_box_sample_size_systematic_interval)
        self.stacked_widget_sample_size_val.addWidget(self.spin_box_sample_size_systematic_size)

        self.combo_box_sampling_method.addItems([
            self.tr('None'),
            self.tr('Simple random sampling'),
            self.tr('Systematic sampling (fixed interval)'),
            self.tr('Systematic sampling (fixed size)')
        ])

        self.spin_box_sample_size_random.setRange(1, 1000000)
        self.spin_box_sample_size_systematic_interval.setRange(2, 10000)
        self.spin_box_sample_size_systematic_size.setRange(1, 10000)

        self.combo_box_sampling_method.currentTextChanged.connect(self.settings_changed)
        self.spin_box_sample_size_random.valueChanged.connect(self.settings_changed)
        self.spin_box_sample_size_systematic_interval.valueChanged.connect(self.settings_changed)
        self.spin_box_sample_size_systematic_size.valueChanged.connect(self.settings_changed)

        self.button_restore_default_vals = wl_buttons.Wl_Button_Restore_Default_Vals(self, load_settings = self.load_settings)
        self.button_sample = QtWidgets.QPushButton(self.tr('Sample'), self)
        self.button_close = QtWidgets.QPushButton(self.tr('Close'), self)

        self.button_sample.setDefault(True)

        self.button_sample.clicked.connect(lambda: self.sample()) # pylint: disable=unnecessary-lambda
        self.button_close.clicked.connect(self.reject)

        layout_buttons_bottom = wl_layouts.Wl_Layout()
        layout_buttons_bottom.addWidget(self.button_restore_default_vals, 0, 0)
        layout_buttons_bottom.addWidget(self.button_sample, 0, 2)
        layout_buttons_bottom.addWidget(self.button_close, 0, 3)

        layout_buttons_bottom.setColumnStretch(1, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.label_sampling_method, 0, 0)
        self.layout().addWidget(self.combo_box_sampling_method, 0, 1)
        self.layout().addWidget(self.stacked_widget_sample_size_label, 1, 0)
        self.layout().addWidget(self.stacked_widget_sample_size_val, 1, 1)

        self.layout().addWidget(wl_layouts.Wl_Separator(self), 2, 0, 1, 2)
        self.layout().addLayout(layout_buttons_bottom, 3, 0, 1, 2)

        self.layout().setColumnStretch(1, 1)

        self.load_settings()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default[self.tab]['results_sample'])
        else:
            settings = copy.deepcopy(self.settings)

        self.combo_box_sampling_method.setCurrentText(settings['sampling_method'])
        self.spin_box_sample_size_random.setValue(settings['sample_size_random'])
        self.spin_box_sample_size_systematic_interval.setValue(settings['sample_size_systematic_interval'])
        self.spin_box_sample_size_systematic_size.setValue(settings['sample_size_systematic_size'])

        self.settings_changed()

    def settings_changed(self):
        self.settings['sampling_method'] = self.combo_box_sampling_method.currentText()
        self.settings['sample_size_random'] = self.spin_box_sample_size_random.value()
        self.settings['sample_size_systematic_interval'] = self.spin_box_sample_size_systematic_interval.value()
        self.settings['sample_size_systematic_size'] = self.spin_box_sample_size_systematic_size.value()

        # Sampling Method
        if self.settings['sampling_method'] == self.tr('None'):
            self.stacked_widget_sample_size_val.setEnabled(False)
        else:
            self.stacked_widget_sample_size_val.setEnabled(True)

            if self.settings['sampling_method'] == self.tr('Simple random sampling'):
                self.stacked_widget_sample_size_label.setCurrentIndex(0)
                self.stacked_widget_sample_size_val.setCurrentIndex(0)
            elif self.settings['sampling_method'] == self.tr('Systematic sampling (fixed interval)'):
                self.stacked_widget_sample_size_label.setCurrentIndex(1)
                self.stacked_widget_sample_size_val.setCurrentIndex(1)
            elif self.settings['sampling_method'] == self.tr('Systematic sampling (fixed size)'):
                self.stacked_widget_sample_size_label.setCurrentIndex(2)
                self.stacked_widget_sample_size_val.setCurrentIndex(2)

    def sample(self):
        self.table.rows_sample.clear()

        rows_to_sample = numpy.array(sorted(set(range(self.table.model().rowCount())) - self.table.rows_filter))
        num_rows_to_filter = rows_to_sample.size
        samples = rows_to_sample.copy()

        if self.settings['sampling_method'] == self.tr('Simple random sampling'):
            sample_size = self.settings['sample_size_random']

            if sample_size < num_rows_to_filter:
                samples = numpy.random.choice(rows_to_sample, sample_size, replace = False)
        elif self.settings['sampling_method'] == self.tr('Systematic sampling (fixed interval)'):
            sample_interval = self.settings['sample_size_systematic_interval']

            start = numpy.random.choice(range(sample_interval))
            samples = rows_to_sample[start::sample_interval]
        elif self.settings['sampling_method'] == self.tr('Systematic sampling (fixed size)'):
            sample_size = self.settings['sample_size_systematic_size']

            if sample_size < num_rows_to_filter:
                sample_interval = num_rows_to_filter // sample_size

                start = numpy.random.choice(range(sample_interval))
                samples = rows_to_sample[start::sample_interval][:sample_size]

        self.table.rows_sample = set(range(self.table.model().rowCount())) - set(samples)
        self.table.filter_table()
