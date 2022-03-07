# ----------------------------------------------------------------------
# Wordless: Utilities - Crawler - War and Peace
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
import requests

num_pages = 361

with open('Война и мир.txt', 'w', encoding = 'utf_8') as f:
    for i in range(num_pages):
        print(f'Downloading page {i + 1}...')

        url = f'https://ilibrary.ru/text/11/p.{i + 1}/index.html'

        r = requests.get(url)

        if r.status_code == 200:
            soup = bs4.BeautifulSoup(r.text, features = 'lxml')

            text = soup.select_one('#text')
            # Book title
            text.select_one('#thdr').decompose()
            # Reference numbers
            for ref_num in text.select('.fnref'):
                ref_num.decompose()
            # Footnotes
            for footnote in text.select('.fns'):
                footnote.decompose()
            # Page numbers
            text.select_one('#bnbg').decompose()
            # "Table of Contents"
            text.select_one('.bttn').decompose()

            f.write(text.get_text())
        else:
            raise Exception(f'HTTP Error: {r.status_code}!')

print('All done!')
