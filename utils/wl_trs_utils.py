# ----------------------------------------------------------------------
# Utilities: Translations - Utilities
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

import glob
import subprocess

import bs4

# Fix format of ts files
def fix_ts_format(ts_file):
    with open(ts_file, 'r', encoding = 'utf_8') as f:
        contents = f.read()

    with open(ts_file, 'w', encoding = 'utf_8') as f:
        contents = contents.replace('<html><body><ts', '<TS')
        contents = contents.replace('</ts>\n</body></html>', '</TS>\n')

        f.write(contents)

def del_obsolete_trans(ts_file):
    with open(ts_file, 'r', encoding = 'utf_8') as f:
        soup = bs4.BeautifulSoup(f.read(), features = 'lxml')

    for element_context in soup.select('context'):
        for element_message in element_context.select('message'):
            element_tr = element_message.select_one('translation')

            # Remove obsolete translations
            if 'type' in element_tr.attrs and element_tr['type'] == 'obsolete':
                element_message.decompose()

    # Remove empty contexts
    for element_context in soup.select('context'):
        if not element_context.select('message'):
            element_context.decompose()

    with open(ts_file, 'w', encoding = 'utf_8') as f:
        f.write(str(soup))

    fix_ts_format(ts_file)

def release_trs():
    for ts_file in glob.glob('trs/*.ts'):
        subprocess.run(['lrelease', ts_file], check = True)

if __name__ == '__main__':
    release_trs()
