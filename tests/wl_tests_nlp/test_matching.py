# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Matching
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

from tests import wl_test_init
from wordless.wl_nlp import wl_matching

main = wl_test_init.Wl_Test_Main()

main.settings_custom['files']['tags']['header_tag_settings'].extend([
    ['Non-embedded', 'Header', '< tei Header >', '</ tei Header >'],
    ['Non-embedded', 'Header', '<>', '</>'],
    ['Non-embedded', 'Header', '< >', '</ >']
])
main.settings_custom['files']['tags']['body_tag_settings'].extend([
    ['Embedded', 'Part of Speech', '_', 'N/A'],
    ['Non-embedded', 'Others', '< * >', '</ * >'],
    ['Non-embedded', 'Others', '< T AG >', '</ T AG >'],
    ['Non-embedded', 'Others', '<>', '</>'],
    ['Non-embedded', 'Others', '< >', '</ >']
])
main.settings_custom['files']['tags']['xml_tag_settings'].extend([
    ['Non-embedded', 'Paragraph', '< p p >', '</ p p >'],
    ['Non-embedded', 'Paragraph', '<>', '</>'],
    ['Non-embedded', 'Paragraph', '< >', '</ >']
])

def test_split_tag_embedded():
    assert wl_matching.split_tag_embedded(r'_TAG') == ('_', 'TAG')
    assert wl_matching.split_tag_embedded(r'_/TAG') == ('_/', 'TAG')
    assert wl_matching.split_tag_embedded(r'_/T_AG') == ('_/', 'T_AG')
    assert wl_matching.split_tag_embedded(r'_/') == ('_/', '')

def test_split_tag_non_embedded():
    assert wl_matching.split_tag_non_embedded(r'<TAG>') == ('<', 'TAG', '>')
    assert wl_matching.split_tag_non_embedded(r'<_TAG_>') == ('<_', 'TAG', '_>')
    assert wl_matching.split_tag_non_embedded(r'<_T<A_G_>') == ('<_', 'T<A_G', '_>')
    assert wl_matching.split_tag_non_embedded(r'<_ TAG_>') == ('<_', ' TAG', '_>')
    assert wl_matching.split_tag_non_embedded(r'<_T AG_>') == ('<_', 'T AG', '_>')
    assert wl_matching.split_tag_non_embedded(r'<_TAG _>') == ('<_', 'TAG ', '_>')
    assert wl_matching.split_tag_non_embedded(r'<_ _>') == ('<_', ' ', '_>')
    assert wl_matching.split_tag_non_embedded(r'<__>') == ('<_', '', '_>')
    assert wl_matching.split_tag_non_embedded(r'<__?>') == ('<_', '', '_?>')

    # Wildcards
    assert wl_matching.split_tag_non_embedded(r'<*TAG*>') == ('<*', 'TAG', '*>')
    assert wl_matching.split_tag_non_embedded(r'<*>') == ('<', '*', '>')
    assert wl_matching.split_tag_non_embedded(r'< * >') == ('<', ' * ', '>')
    assert wl_matching.split_tag_non_embedded(r'<T*AG>') == ('<', 'T*AG', '>')

def test_get_re_tags():
    re_tags_header = wl_matching.get_re_tags(main, tag_type = 'header')
    re_tags_body = wl_matching.get_re_tags(main, tag_type = 'body')
    re_tags_xml = wl_matching.get_re_tags(main, tag_type = 'xml')

    print(re_tags_header)
    print(re_tags_body)
    print(re_tags_xml)

    assert re_tags_header == r'</?teiHeader>|</?\ tei\ Header\ >|</?>|</?\ >'
    assert re_tags_body == r'_\S*(?=\s|$)|/\S*(?=\s|$)|_(?=\s|$)|</?.*?>|</?\ \*\ >|</?\ T\ AG\ >|</?>|</?\ >'
    assert re_tags_xml == r'</?p>|</?s>|</?w>|</?c>|</?\ p\ p\ >|</?>|</?\ >'

    assert re.search(re_tags_header, r'token<teiHeader>').group() == '<teiHeader>'
    assert re.search(re_tags_header, r'</teiHeader>token').group() == '</teiHeader>'
    assert re.search(re_tags_header, r'<teiHeader>token</teiHeader>').group() == '<teiHeader>'
    assert re.search(re_tags_header, r'< tei Header >token</ tei Header >').group() == '< tei Header >'
    assert re.search(re_tags_header, r'<>token</>').group() == '<>'
    assert re.search(re_tags_header, r'< >token</ >').group() == '< >'

    assert re.search(re_tags_body, r'token_TAG').group() == '_TAG'
    assert re.search(re_tags_body, r'token_T_AG').group() == '_T_AG'
    assert re.search(re_tags_body, r'token_').group() == '_'
    assert re.search(re_tags_body, r'token/TAG').group() == '/TAG'
    assert re.search(re_tags_body, r'token<TAG>').group() == '<TAG>'
    assert re.search(re_tags_body, r'</TAG>token').group() == '</TAG>'
    assert re.search(re_tags_body, r'< T AG >token</ T AG >').group() == '< T AG >'
    assert re.search(re_tags_body, r'<TAG>token</TAG>').group() == '<TAG>'
    assert re.search(re_tags_body, r'<>token</>').group() == '<>'
    assert re.search(re_tags_body, r'< >token</ >').group() == '< >'
    assert re.search(re_tags_body, r'< * >token</ * >').group() == '< * >'

    assert re.search(re_tags_xml, r'token<p>').group() == '<p>'
    assert re.search(re_tags_xml, r'</p>token').group() == '</p>'
    assert re.search(re_tags_xml, r'<p>token</p>').group() == '<p>'
    assert re.search(re_tags_xml, r'< p p >token</ p p >').group() == '< p p >'
    assert re.search(re_tags_xml, r'<>token</>').group() == '<>'
    assert re.search(re_tags_xml, r'< >token</ >').group() == '< >'

def test_get_re_tags_with_tokens():
    re_tags_header = wl_matching.get_re_tags_with_tokens(main, tag_type = 'header')
    re_tags_body = wl_matching.get_re_tags_with_tokens(main, tag_type = 'body')
    re_tags_xml = wl_matching.get_re_tags_with_tokens(main, tag_type = 'xml')

    print(re_tags_header)
    print(re_tags_body)
    print(re_tags_xml)

    assert re_tags_header == r'<teiHeader>.*</teiHeader>|<\ tei\ Header\ >.*</\ tei\ Header\ >|<>.*</>|<\ >.*</\ >'
    assert re_tags_body == r'\S*_\S*(?=\s|$)|\S*/\S*(?=\s|$)|\S*_(?=\s|$)|<.*?>.*?</.*?>|<\ \*\ >.*</\ \*\ >|<\ T\ AG\ >.*</\ T\ AG\ >|<>.*</>|<\ >.*</\ >'
    assert re_tags_xml == r'<p>.*</p>|<s>.*</s>|<w>.*</w>|<c>.*</c>|<\ p\ p\ >.*</\ p\ p\ >|<>.*</>|<\ >.*</\ >'

    assert re.search(re_tags_header, r'token <teiHeader>token</teiHeader> token').group() == '<teiHeader>token</teiHeader>'
    assert re.search(re_tags_header, r'token <teiHeader>token</teiHeader> token').group() == '<teiHeader>token</teiHeader>'
    assert re.search(re_tags_header, r'token < tei Header >token</ tei Header > token').group() == '< tei Header >token</ tei Header >'
    assert re.search(re_tags_header, r'token <>token</> token').group() == '<>token</>'
    assert re.search(re_tags_header, r'token < >token</ > token').group() == '< >token</ >'

    assert re.search(re_tags_body, r'token token_TAG token').group() == 'token_TAG'
    assert re.search(re_tags_body, r'token token/TAG token').group() == 'token/TAG'
    assert re.search(re_tags_body, r'token token_T_AG token').group() == 'token_T_AG'
    assert re.search(re_tags_body, r'token token_ token').group() == 'token_'
    assert re.search(re_tags_body, r'token <TAG>token</TAG> token').group() == '<TAG>token</TAG>'
    assert re.search(re_tags_body, r'token < T AG >token</ T AG > token').group() == '< T AG >token</ T AG >'
    assert re.search(re_tags_body, r'token <>token</> token').group() == '<>token</>'
    assert re.search(re_tags_body, r'token < >token</ > token').group() == '< >token</ >'
    assert re.search(re_tags_body, r'token < * >token</ * > token').group() == '< * >token</ * >'

    assert re.search(re_tags_xml, r'token <p>token</p> token').group() == '<p>token</p>'
    assert re.search(re_tags_xml, r'token < p p >token</ p p > token').group() == '< p p >token</ p p >'
    assert re.search(re_tags_xml, r'token <>token</> token').group() == '<>token</>'
    assert re.search(re_tags_xml, r'token < >token</ > token').group() == '< >token</ >'

if __name__ == '__main__':
    test_split_tag_embedded()
    test_split_tag_non_embedded()
    test_get_re_tags()
    test_get_re_tags_with_tokens()
