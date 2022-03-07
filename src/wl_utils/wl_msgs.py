# ----------------------------------------------------------------------
# Wordless: Utilities - Messages
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

from PyQt5.QtCore import QCoreApplication

_tr = QCoreApplication.translate

def wl_msg_fatal_error(main):
    main.statusBar().showMessage(_tr('wl_msgs', 'A fatal error has occurred!'))

def wl_msg_generate_table_success(main):
    main.statusBar().showMessage(_tr('wl_msgs', 'The table has been successfully generated.'))

def wl_msg_generate_table_error(main):
    main.statusBar().showMessage(_tr('wl_msgs', 'An error occured while the table is being generated!'))

def wl_msg_generate_fig_success(main):
    main.statusBar().showMessage(_tr('wl_msgs', 'The figure has been successfully generated.'))

def wl_msg_generate_fig_error(main):
    main.statusBar().showMessage(_tr('wl_msgs', 'An error occured while the figure is being generated!'))

def wl_msg_results_filter_success(main):
    main.statusBar().showMessage(_tr('wl_msgs', 'The results in the table has been successfully filtered.'))
