# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Thai
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

from tests.tests_nlp.tests_stanza import test_stanza

results_pos_tag = [('ภาษา', 'NOUN'), ('ไทย', 'PROPN'), ('หรือ', 'CCONJ'), ('ภาษา', 'NOUN'), ('ไทย', 'PROPN'), ('กลาง', 'NOUN'), ('เป็น', 'AUX'), ('ภาษา', 'NOUN'), ('ใน', 'ADP'), ('กลุ่ม', 'NOUN'), ('ภาษา', 'NOUN'), ('ไท', 'PROPN'), ('สาขา', 'NOUN'), ('ย่อย', 'NOUN'), ('เชียง', 'PROPN'), ('แสน', 'NUM'), ('ซึ่ง', 'PRON'), ('เป็น', 'AUX'), ('กลุ่ม', 'NOUN'), ('ย่อย', 'ADJ'), ('ของ', 'ADP'), ('ตระกูล', 'NOUN'), ('ภาษา', 'NOUN'), ('ขร้า', 'PROPN'), ('-', 'PUNCT'), ('ไท', 'PROPN'), ('และ', 'CCONJ'), ('เป็น', 'AUX'), ('ภาษา', 'NOUN'), ('ราชการ', 'NOUN'), ('และ', 'CCONJ'), ('ภาษา', 'NOUN'), ('ประจำ', 'VERB'), ('ชาติ', 'NOUN'), ('ของ', 'ADP'), ('ประเทศ', 'NOUN'), ('ไทย', 'PROPN'), ('[3', 'PUNCT'), (']', 'PUNCT'), ('[4', 'PUNCT'), (']', 'PUNCT')]

def test_stanza_tha():
    test_stanza.wl_test_stanza(
        lang = 'tha',
        results_sentence_tokenize = ['ภาษาไทย หรือ ภาษาไทยกลาง เป็นภาษาในกลุ่มภาษาไท สาขาย่อยเชียงแสน ซึ่งเป็นกลุ่มย่อยของตระกูลภาษาขร้า-ไท และเป็นภาษาราชการ และภาษาประจำชาติของประเทศไทย[3][4] มีการสันนิษฐานว่าภาษาในตระกูลนี้มีถิ่นกำเนิดจากทางตอนใต้ของประเทศจีน และนักภาษาศาสตร์บางส่วนเสนอว่า ภาษาไทย', 'น่าจะมีความเชื่อมโยงกับตระกูลภาษาออสโตร-เอเชียติก ตระกูลภาษาออสโตรนีเซียน และตระกูลภาษาจีน-ทิเบต'],
        results_word_tokenize = ['ภาษา', 'ไทย', 'หรือ', 'ภาษา', 'ไทย', 'กลาง', 'เป็น', 'ภาษา', 'ใน', 'กลุ่ม', 'ภาษา', 'ไท', 'สาขา', 'ย่อย', 'เชียง', 'แสน', 'ซึ่ง', 'เป็น', 'กลุ่ม', 'ย่อย', 'ของ', 'ตระกูล', 'ภาษา', 'ขร้า', '-', 'ไท', 'และ', 'เป็น', 'ภาษา', 'ราชการ', 'และ', 'ภาษา', 'ประจำ', 'ชาติ', 'ของ', 'ประเทศ', 'ไทย', '[3', ']', '[4', ']'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_dependency_parse = [('ภาษา', 'ภาษา', 'nsubj', 7), ('ไทย', 'ภาษา', 'nmod', -1), ('หรือ', 'ภาษา', 'cc', 1), ('ภาษา', 'ภาษา', 'conj', -3), ('ไทย', 'ภาษา', 'nmod', -1), ('กลาง', 'ภาษา', 'nmod', -2), ('เป็น', 'ภาษา', 'cop', 1), ('ภาษา', 'ภาษา', 'root', 0), ('ใน', 'กลุ่ม', 'case', 1), ('กลุ่ม', 'ภาษา', 'nmod', -2), ('ภาษา', 'กลุ่ม', 'nmod', -1), ('ไท', 'ภาษา', 'nmod', -1), ('สาขา', 'กลุ่ม', 'nmod', -3), ('ย่อย', 'สาขา', 'nmod', -1), ('เชียง', 'ย่อย', 'nmod', -1), ('แสน', 'เชียง', 'nummod', -1), ('ซึ่ง', 'กลุ่ม', 'nsubj', 2), ('เป็น', 'กลุ่ม', 'cop', 1), ('กลุ่ม', 'ภาษา', 'acl', -11), ('ย่อย', 'กลุ่ม', 'amod', -1), ('ของ', 'ตระกูล', 'case', 1), ('ตระกูล', 'กลุ่ม', 'nmod', -3), ('ภาษา', 'ตระกูล', 'nmod', -1), ('ขร้า', 'ภาษา', 'nmod', -1), ('-', 'ไท', 'punct', 1), ('ไท', 'ตระกูล', 'nmod', -4), ('และ', 'ภาษา', 'cc', 2), ('เป็น', 'ภาษา', 'cop', 1), ('ภาษา', 'ภาษา', 'conj', -21), ('ราชการ', 'ภาษา', 'compound', -1), ('และ', 'ภาษา', 'cc', 1), ('ภาษา', 'ภาษา', 'conj', -3), ('ประจำ', 'ภาษา', 'acl', -1), ('ชาติ', 'ประจำ', 'obj', -1), ('ของ', 'ประเทศ', 'case', 1), ('ประเทศ', 'ภาษา', 'nmod', -4), ('ไทย', 'ประเทศ', 'nmod', -1), ('[3', 'ประเทศ', 'punct', -2), (']', '[4', 'punct', 1), ('[4', 'ภาษา', 'punct', -11), (']', 'ภาษา', 'punct', -12)]
    )

if __name__ == '__main__':
    test_stanza_tha()
