# ----------------------------------------------------------------------
# Wordless: Widgets - Editors
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

from PyQt5.QtWidgets import QTextBrowser

from wordless.wl_utils import wl_misc

class Wl_Text_Browser(QTextBrowser):
    def __init__(self, parent):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)

        self.setOpenExternalLinks(True)
        self.setContentsMargins(3, 3, 3, 3)
 