# ----------------------------------------------------------------------
# Utilities: Translations - Chinese (Traditional)
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

import bs4
import opencc

import wl_trs_utils

with open('../trs/zho_cn.ts', 'r', encoding = 'utf_8') as f:
    soup = bs4.BeautifulSoup(f.read(), features = 'lxml')

cc = opencc.OpenCC('s2twp')

# Change language
soup.ts['language'] = 'zh_TW'
# Translate Simplified Chinese into Traditional Chinese
for element_context in soup.select('context'):
    for element_message in element_context.select('message'):
        element_trans = element_message.select_one('translation')

        element_trans.string = cc.convert(element_trans.text)

with open('../trs/zho_tw.ts', 'w', encoding = 'utf_8') as f:
    f.write(str(soup))

# Release
wl_trs_utils.fix_ts_format('../trs/zho_tw.ts')
wl_trs_utils.release_trs()
