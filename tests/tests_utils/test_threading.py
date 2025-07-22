# ----------------------------------------------------------------------
# Tests: Utilities - Threading
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

from tests import wl_test_init
from wordless.wl_dialogs import wl_dialogs_misc
from wordless.wl_utils import wl_threading

main = wl_test_init.Wl_Test_Main()

def test_wl_worker():
    wl_threading.Wl_Worker(main, wl_dialogs_misc.Wl_Dialog_Progress(main, 'test'))

def test_wl_worker_no_progress():
    wl_threading.Wl_Worker_No_Progress(main)

if __name__ == '__main__':
    test_wl_worker()
    test_wl_worker_no_progress()
