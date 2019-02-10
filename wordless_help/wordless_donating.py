#
# Wordless: Help - Donating
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import copy

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_widgets import *

class Wordless_Dialog_Donating(wordless_dialog.Wordless_Dialog_Info):
    def __init__(self, main):
        super().__init__(main, main.tr('Donating'),
                         width = 400,
                         height = 280)

        self.label_donating = wordless_label.Wordless_Label_Dialog(
            self.tr('''
                <div>
                    If you would like to support the development of Wordless, you may donate via PayPal, Alipay or WeChat.
                </div>

                <div>
                    <span style="color: #F00;"><b>Important Note</b></span>: I <b>WILL NOT PROVIDE</b> refund services, private email/phone support, information concerning my social media, gurantees on bug fixes, enhancements, new features or new releases of Wordless, invoices, receipts or detailed weekly/monthly/yearly/etc. spending report for donation. 
                </div>
            '''), self.main)
        self.label_donating_via = QLabel(self.tr('Donating via:'), self)
        self.combo_box_donating_via = wordless_box.Wordless_Combo_Box(self)
        self.label_donating_via_img = wordless_label.Wordless_Label_Html('', self)

        self.combo_box_donating_via.addItems([
            self.tr('PayPal'),
            self.tr('Alipay'),
            self.tr('WeChat')
        ])

        self.combo_box_donating_via.currentTextChanged.connect(self.donating_via_changed)

        layout_donating_via = QGridLayout()
        layout_donating_via.addWidget(self.label_donating_via, 0, 0)
        layout_donating_via.addWidget(self.combo_box_donating_via, 0, 1)

        layout_donating_via.setColumnStretch(2, 1)

        self.wrapper_info.layout().addWidget(self.label_donating, 0, 0)
        self.wrapper_info.layout().addLayout(layout_donating_via, 1, 0)
        self.wrapper_info.layout().addWidget(self.label_donating_via_img, 2, 0, Qt.AlignHCenter | Qt.AlignVCenter)

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

            self.setFixedHeight(280)
        elif settings['donating_via'] == self.tr('Alipay'):
            self.label_donating_via_img.setText('<img src="imgs/donating_alipay.png">')

            self.setFixedHeight(530)
        elif settings['donating_via'] == self.tr('WeChat'):
            self.label_donating_via_img.setText('<img src="imgs/donating_wechat.png">')

            self.setFixedHeight(530)

        self.move_to_center()
