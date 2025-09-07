# ----------------------------------------------------------------------
# Utilities: Generate - README - Chinese (Traditional)
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

import opencc

def convert_to_zho_tw(file_name, opencc_dict = 'auto'):
    opencc_s2t = opencc.OpenCC('s2t')
    opencc_s2twp = opencc.OpenCC('s2twp')

    header = []
    content = []

    with open(f'doc/trs/zho_cn/{file_name}.md', 'r', encoding = 'utf_8') as f:
        for line in f:
            line = line.rstrip()

            # README
            if (
                file_name == 'README'
                and line == '    <b>中文（简体）</b> | <a href="/doc/trs/zho_tw/README.md">中文（繁體）</a> | <a href="https://github.com/BLKSerene/Wordless#readme">English</a>'
            ):
                content.append('    <a href="/doc/trs/zho_cn/README.md">中文（简体）</a> | <b>中文（繁體）</b> | <a href="https://github.com/BLKSerene/Wordless#readme">English</a>')

                continue

            if line.startswith(('<!-', '#')) and not line.startswith('##'):
                header.append(line.replace('Chinese (Simplified)', 'Chinese (Traditional)'))
            else:
                line = line.replace('/zho_cn/', '/zho_tw/')

                match opencc_dict:
                    case 's2t':
                        content.append(opencc_s2t.convert(line))
                    case 's2twp':
                        content.append(opencc_s2twp.convert(line))
                    case 'auto':
                        if line.startswith('<div class="s2twp">'):
                            content.append(opencc_s2twp.convert(line))
                        else:
                            content.append(opencc_s2t.convert(line))

    header = '\n'.join(header)
    content = '\n'.join(content)

    with open(f'doc/trs/zho_tw/{file_name}.md', 'w', encoding = 'utf_8') as f:
        f.write(f'{header}\n{content}\n')

def convert_readme_zho_tw():
    # Acknowledgments
    convert_to_zho_tw('ACKS')

    # Contributing
    convert_to_zho_tw('CONTRIBUTING', opencc_dict = 's2twp')

    # README
    convert_to_zho_tw('README', opencc_dict = 's2twp')

    # Works Using Wordless
    convert_to_zho_tw('WORKS_USING_WORDLESS')

if __name__ == '__main__':
    convert_readme_zho_tw()
