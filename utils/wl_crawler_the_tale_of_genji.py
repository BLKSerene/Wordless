# ----------------------------------------------------------------------
# Wordless: Crawler - The Tale of Genji
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

import re

import bs4
import requests

# Contents
url_chapters = {}
url_domain = 'https://ja.wikisource.org'

r = requests.get(f'{url_domain}/wiki/%E6%BA%90%E6%B0%8F%E7%89%A9%E8%AA%9E_(%E6%B8%8B%E8%B0%B7%E6%A0%84%E4%B8%80%E6%A0%A1%E8%A8%82)')
soup = bs4.BeautifulSoup(r.text, features = 'lxml')

for element_li in soup.select('.mw-parser-output > ul li'):
    url_chapters[element_li.a.text] = url_domain + element_li.a['href']

with open('源氏物語.txt', 'w', encoding = 'utf_8') as f:
    for title, url in url_chapters.items():
        print(f'Downloading chapter {title}...')

        r = requests.get(url)

        if r.status_code == 200:
            soup = bs4.BeautifulSoup(r.text, features = 'lxml')

            for element_p in soup.select('.mw-parser-output > p'):
                f.write(element_p.text + '\n')
        else:
            raise Exception(f'HTTP Error: {r.status_code}!')

# Clean text
with open('源氏物語.txt', 'r', encoding = 'utf_8') as f:
    text = f.read()

text = re.sub(r'\n{3,}', r'\n\n', text)
text = text.strip()

with open('源氏物語.txt', 'w', encoding = 'utf_8') as f:
    f.write(text + '\n')

print('All done!')
