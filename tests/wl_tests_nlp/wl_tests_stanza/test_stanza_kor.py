# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Stanza - Korean
# Copyright (C) 2018-2023  Ye Lei (叶磊)
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

from tests.wl_tests_nlp.wl_tests_stanza import test_stanza

def test_stanza_kor():
    test_stanza.wl_test_stanza(
        lang = 'kor',
        results_sentence_tokenize = ['한국어(韓國語)는 대한민국과 조선민주주의인민공화국의 공용어이다.', '조선말, 한국말, 조선어로도 불린다.'],
        results_word_tokenize = ['한국', '어(', '韓國語', ')', '는', '대한민국과', '조선민주주의인민공화국의', '공용어이다', '.'],
        results_pos_tag = [('한국', 'nq'), ('어(', 'sl'), ('韓國語', 'nq'), (')', 'sr'), ('는', 'jxt'), ('대한민국과', 'nq+jcj+jcj'), ('조선민주주의인민공화국의', 'ncn+ncn+ncn+jcm'), ('공용어이다', 'ncn+jp+ef'), ('.', 'sf')],
        results_pos_tag_universal = [('한국', 'PROPN'), ('어(', 'PUNCT'), ('韓國語', 'PROPN'), (')', 'PUNCT'), ('는', 'ADP'), ('대한민국과', 'CCONJ'), ('조선민주주의인민공화국의', 'NOUN'), ('공용어이다', 'VERB'), ('.', 'PUNCT')],
        results_lemmatize = ['한국', '어(', '韓國語', ')', '는', '대한+민국+과', '조선민주주의+인민+공화+의', '공용어+이+다', '.'],
        results_dependency_parse = [('한국', '공용어이다', 'dislocated', 7), ('어(', '韓國語', 'compound', 1), ('韓國語', '한국', 'appos', -2), (')', '韓國語', 'punct', -1), ('는', '한국', 'case', -4), ('대한민국과', '공용어이다', 'nmod', 2), ('조선민주주의인민공화국의', '대한민국과', 'conj', -1), ('공용어이다', '공용어이다', 'root', 0), ('.', '공용어이다', 'punct', -1)]
    )

if __name__ == '__main__':
    test_stanza_kor()
