# ----------------------------------------------------------------------
# Utilities: Generate acknowledgment files
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

FILES = [
    'ACKS.md',
    'doc/trs/zho_cn/ACKS.md',
    'doc/trs/zho_tw/ACKS.md'
]
HEADER_LANGS = ['English', 'Chinese (Simplified)', 'Chinese (Traditional)']
TITLES = ['Acknowledgments', '致谢', '致謝']
DESCRIPTIONS = [
    'As Wordless stands on the shoulders of giants, I hereby extend my sincere gratitude to the following open-source projects without which this project would not have been possible:',
    '鉴于 Wordless 立于巨人的肩膀之上，我谨在此向下列开源项目致以本人诚挚的感谢，若没有它们，本项目将无法完成：',
    '鑑於 Wordless 立於巨人的肩膀之上，我謹在此向下列開源專案致以本人誠摯的感謝，若沒有它們，本專案將無法完成：'
]
COL_HEADERS = [
    'Name|Version|Authors|License',
    '名称|版本|作者|许可',
    '名稱|版本|作者|許可'
]

# SPDX License List: https://spdx.org/licenses/
ACKS = [
    [
        'Beautiful Soup', 'https://www.crummy.com/software/BeautifulSoup/',
        '4.12.3', 'Leonard Richardson',
        'MIT', 'https://git.launchpad.net/beautifulsoup/tree/LICENSE'
    ], [
        'Botok', 'https://github.com/OpenPecha/Botok',
        '0.8.12', 'Hélios Drupchen Hildt',
        'Apache-2.0', 'https://github.com/OpenPecha/Botok/blob/master/LICENSE'
    ], [
        'Charset Normalizer', 'https://github.com/Ousret/charset_normalizer',
        '3.3.2', 'TAHRI Ahmed R.',
        'MIT', 'https://github.com/Ousret/charset_normalizer/blob/master/LICENSE'
    ], [
        'khmer-nltk', 'https://github.com/VietHoang1512/khmer-nltk',
        '1.6', 'Phan Viet Hoang',
        'Apache-2.0', 'https://github.com/VietHoang1512/khmer-nltk/blob/main/LICENSE'
    ], [
        'LaoNLP', 'https://github.com/wannaphong/LaoNLP',
        '1.2.0', 'Wannaphong Phatthiyaphaibun (วรรณพงษ์ ภัททิยไพบูลย์)',
        'Apache-2.0', 'https://github.com/wannaphong/LaoNLP/blob/master/LICENSE'
    ], [
        'Lingua', 'https://github.com/pemistahl/lingua-py',
        '2.0.2', 'Peter M. Stahl',
        'Apache-2.0', 'https://github.com/pemistahl/lingua-py/blob/main/LICENSE.txt'
    ], [
        'Matplotlib', 'https://matplotlib.org/',
        '3.9.0', 'Matplotlib Development Team',
        'Matplotlib', 'https://matplotlib.org/stable/users/project/license.html'
    ], [
        'NetworkX', 'https://networkx.org/',
        '3.3', 'NetworkX Developers, Aric Hagberg, Dan Schult,<br>Pieter Swart',
        'BSD-3-Clause', 'https://github.com/networkx/networkx/blob/main/LICENSE.txt'
    ], [
        'NLTK', 'https://www.nltk.org/',
        '3.8.1', 'Steven Bird, Edward Loper, Ewan Klein',
        'Apache-2.0', 'https://github.com/nltk/nltk/blob/develop/LICENSE.txt'
    ], [
        'NumPy', 'https://www.numpy.org/',
        '1.26.4', 'NumPy Developers',
        'BSD-3-Clause', 'https://github.com/numpy/numpy/blob/main/LICENSE.txt'
    ], [
        'opencc-python', 'https://github.com/yichen0831/opencc-python',
        '0.1.7', 'Carbo Kuo (郭家宝), Yicheng Huang',
        'Apache-2.0', 'https://github.com/yichen0831/opencc-python/blob/master/LICENSE.txt'
    ], [
        'openpyxl', 'https://foss.heptapod.net/openpyxl/openpyxl',
        '3.1.5', 'Eric Gazoni, Charlie Clark',
        'MIT', 'https://foss.heptapod.net/openpyxl/openpyxl/-/blob/branch/3.1/LICENCE.rst'
    ], [
        'PyInstaller', 'https://pyinstaller.org/',
        '6.8.0', 'Hartmut Goebel, Jasper Harrison, Bryan A. Jones,<br>Brénainn Woodsend, Rok Mandeljc',
        'Bootloader-exception', 'https://github.com/pyinstaller/pyinstaller/blob/develop/COPYING.txt'
    ], [
        'pymorphy3', 'https://github.com/no-plagiarism/pymorphy3',
        '2.0.2', 'Mikhail Korobov, Danylo Halaiko',
        'MIT', 'https://github.com/no-plagiarism/pymorphy3/blob/master/LICENSE.txt'
    ], [
        'pypdf', 'https://github.com/py-pdf/pypdf',
        '4.2.0', 'Mathieu Fenniak, Ashish Kulkarni, Steve Witham, Martin Thoma',
        'BSD-3-Clause', 'https://github.com/py-pdf/pypdf/blob/main/LICENSE'
    ], [
        'Pyphen', 'https://pyphen.org/',
        '0.15.0', 'Guillaume Ayoub',
        'GPL-2.0-or-later/LGPL-2.1-or-later/MPL-1.1', 'https://github.com/Kozea/Pyphen/blob/master/LICENSE'
    ], [
        'PyQt', 'https://riverbankcomputing.com/software/pyqt/',
        '5.15.10', 'Riverbank Computing',
        'Commercial-License/GPL-3.0-only', 'https://www.riverbankcomputing.com/static/Docs/PyQt5/introduction.html#license'
    ], [
        'PyThaiNLP', 'https://github.com/PyThaiNLP/pythainlp',
        '5.0.4', 'Wannaphong Phatthiyaphaibun (วรรณพงษ์ ภัททิยไพบูลย์)',
        'Apache-2.0', 'https://github.com/PyThaiNLP/pythainlp/blob/dev/LICENSE'
    ], [
        'python-docx', 'https://github.com/python-openxml/python-docx',
        '1.1.2', 'Steve Canny',
        'MIT', 'https://github.com/python-openxml/python-docx/blob/master/LICENSE'
    ], [
        'python-mecab-ko', 'https://github.com/jonghwanhyeon/python-mecab-ko',
        '1.3.5', 'Jonghwan Hyeon',
        'BSD-3-Clause', 'https://github.com/jonghwanhyeon/python-mecab-ko/blob/main/LICENSE'
    ], [
        'python-pptx', 'https://github.com/scanny/python-pptx',
        '0.6.23', 'Steve Canny',
        'MIT', 'https://github.com/scanny/python-pptx/blob/master/LICENSE'
    ], [
        'Requests', 'https://github.com/psf/requests',
        '2.32.3', 'Kenneth Reitz',
        'Apache-2.0', 'https://github.com/psf/requests/blob/main/LICENSE'
    ], [
        'Sacremoses', 'https://github.com/hplt-project/sacremoses',
        '0.1.1', 'Liling Tan, Jelmer van der Linde',
        'MIT', 'https://github.com/hplt-project/sacremoses/blob/master/LICENSE'
    ], [
        'SciPy', 'https://scipy.org/scipylib/',
        '1.14.0', 'SciPy Developers',
        'BSD-3-Clause', 'https://github.com/scipy/scipy/blob/main/LICENSE.txt'
    ], [
        'simplemma', 'https://github.com/adbar/simplemma',
        '1.0.0', 'Adrien Barbaresi',
        'MIT', 'https://github.com/adbar/simplemma/blob/main/LICENSE'
    ], [
        'spaCy', 'https://spacy.io/',
        '3.7.5', "Matthew Honnibal, Ines Montani, Sofie Van Landeghem,<br>Adriane Boyd, Paul O'Leary McCann",
        'MIT', 'https://github.com/explosion/spaCy/blob/master/LICENSE'
    ], [
        'spacy-pkuseg', 'https://github.com/explosion/spacy-pkuseg',
        '0.0.33', 'Ruixuan Luo (罗睿轩), Jingjing Xu (许晶晶),<br>Xuancheng Ren (任宣丞), Yi Zhang (张艺),<br>Zhiyuan Zhang (张之远), Bingzhen Wei (位冰镇),<br>Xu Sun (孙栩)<br>Adriane Boyd, Ines Montani',
        'MIT', 'https://github.com/explosion/spacy-pkuseg/blob/master/LICENSE'
    ], [
        'Stanza', 'https://github.com/stanfordnlp/stanza',
        '1.8.2', 'Peng Qi (齐鹏), Yuhao Zhang (张宇浩),<br>Yuhui Zhang (张钰晖), Jason Bolton,<br>Tim Dozat, John Bauer',
        'Apache-2.0', 'https://github.com/stanfordnlp/stanza/blob/main/LICENSE'
    ], [
        'SudachiPy', 'https://github.com/WorksApplications/sudachi.rs',
        '0.6.8', 'Works Applications Co., Ltd.',
        'Apache-2.0', 'https://github.com/WorksApplications/sudachi.rs/blob/develop/LICENSE'
    ], [
        'Underthesea', 'https://undertheseanlp.com/',
        '6.8.4', 'Vu Anh',
        'GPL-3.0-or-later', 'https://github.com/undertheseanlp/underthesea/blob/main/LICENSE'
    ], [
        'VADER', 'https://github.com/cjhutto/vaderSentiment',
        '3.3.2', 'C.J. Hutto',
        'MIT', 'https://github.com/cjhutto/vaderSentiment/blob/master/LICENSE.txt'
    ], [
        'wordcloud', 'https://github.com/amueller/word_cloud',
        '1.9.3', 'Andreas Christian Müller',
        'MIT', 'https://github.com/amueller/word_cloud/blob/main/LICENSE'
    ]
]
ACKS_TRS = {
    'Matplotlib Development Team': [
        'Matplotlib 开发团队',
        'Matplotlib 開發團隊'
    ],
    'NetworkX Developers, Aric Hagberg, Dan Schult,<br>Pieter Swart': [
        'NetworkX 开发人员, Aric Hagberg, Dan Schult,<br>Pieter Swart',
        'NetworkX 開發人員, Aric Hagberg, Dan Schult,<br>Pieter Swart'
    ],
    'NumPy Developers': [
        'NumPy 开发人员',
        'NumPy 開發人員'
    ],
    'Carbo Kuo (郭家宝), Yicheng Huang': [
        '郭家宝, Yicheng Huang',
        '郭家寶, Yicheng Huang'
    ],
    'SciPy Developers': [
        'SciPy 开发人员',
        'SciPy 開發人員'
    ],
    'Ruixuan Luo (罗睿轩), Jingjing Xu (许晶晶),<br>Xuancheng Ren (任宣丞), Yi Zhang (张艺),<br>Zhiyuan Zhang (张之远), Bingzhen Wei (位冰镇),<br>Xu Sun (孙栩)<br>Adriane Boyd, Ines Montani': [
        '罗睿轩, 许晶晶, 任宣丞, 张艺, 张之远, 位冰镇, 孙栩<br>Adriane Boyd, Ines Montani',
        '羅睿軒, 許晶晶, 任宣丞, 張藝, 張之遠, 位冰鎮, 孫栩<br>Adriane Boyd, Ines Montani'
    ],
    'Peng Qi (齐鹏), Yuhao Zhang (张宇浩),<br>Yuhui Zhang (张钰晖), Jason Bolton,<br>Tim Dozat, John Bauer': [
        '齐鹏, 张宇浩, 张钰晖,<br>Jason Bolton, Tim Dozat, John Bauer',
        '齊鵬, 張宇浩, 張鈺暉,<br>Jason Bolton, Tim Dozat, John Bauer'
    ]
}

for i, (file, header_lang, title, description, col_headers) in enumerate(zip(
    FILES, HEADER_LANGS, TITLES, DESCRIPTIONS, COL_HEADERS
)):
    with open(file, 'w', encoding = 'utf_8') as f:
        f.write(f'''<!----------------------------------------------------------------------
# Wordless: README - Acknowledgments - {header_lang}
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
# --------------------------------------------------------------------->

<div align="center"><h1>{title}</h1></div>

{description}

&nbsp;|{col_headers}
-----:|----|:-----:|-------|:-----:
''')
        # Translations
        if i > 0:
            for row in ACKS:
                for j, cell in enumerate(row):
                    for cell_tr, trs in ACKS_TRS.items():
                        if cell == cell_tr:
                            row[j] = trs[i - 1]

        for j, (
            proj_name, proj_homepage,
            proj_ver, proj_authors,
            proj_license, proj_license_file
        ) in enumerate(ACKS):
            f.write(f'{j + 1}|[{proj_name}]({proj_homepage})|{proj_ver}|{proj_authors}|[{proj_license}]({proj_license_file})\n')
