# ----------------------------------------------------------------------
# Wordless: Utilities - Exceptions
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

class Wl_Exc(Exception):
    pass

class Wl_Exc_Word_Cloud(Wl_Exc):
    pass

class Wl_Exc_Word_Cloud_Font(Wl_Exc_Word_Cloud):
    pass

class Wl_Exc_Word_Cloud_Font_Nonexistent(Wl_Exc_Word_Cloud_Font):
    pass

class Wl_Exc_Word_Cloud_Font_Is_Dir(Wl_Exc_Word_Cloud_Font):
    pass

class Wl_Exc_Word_Cloud_Font_Unsupported(Wl_Exc_Word_Cloud_Font):
    pass

class Wl_Exc_Word_Cloud_Mask(Wl_Exc_Word_Cloud):
    pass

class Wl_Exc_Word_Cloud_Mask_Nonexistent(Wl_Exc_Word_Cloud_Mask):
    pass

class Wl_Exc_Word_Cloud_Mask_Is_Dir(Wl_Exc_Word_Cloud_Mask):
    pass

class Wl_Exc_Word_Cloud_Mask_Unsupported(Wl_Exc_Word_Cloud_Mask):
    pass
