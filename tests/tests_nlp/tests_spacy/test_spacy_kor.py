# ----------------------------------------------------------------------
# Tests: NLP - spaCy - Korean
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

from tests.tests_nlp.tests_spacy import test_spacy

def test_spacy_kor():
    results_sentence_tokenize = ['한국어(韓國語), 조선어(朝鮮語)는 대한민국과 조선민주주의인민공화국의 공용어이다.', '둘은 표기나 문법, 동사 어미나 표현에서 약간의 차이가 있다.']

    test_spacy.wl_test_spacy(
        lang = 'kor',
        results_sentence_tokenize_trf = results_sentence_tokenize,
        results_sentence_tokenize_lg = results_sentence_tokenize,
        results_word_tokenize = ['한국어', '(', '韓國語', ')', ',', '조선어', '(', '朝鮮語', ')', '는', '대한민국과', '조선민주주의인민공화국의', '공용어이다', '.'],
        results_pos_tag = [('한국어', 'nq'), ('(', 'sl'), ('韓國語', 'nq'), (')', 'sr'), (',', 'sp'), ('조선어', 'nq'), ('(', 'sl'), ('朝鮮語', 'nq'), (')', 'sr'), ('는', 'jxt'), ('대한민국과', 'nq+jcj'), ('조선민주주의인민공화국의', 'nq+ncn+jcm'), ('공용어이다', 'ncn+jp+ef'), ('.', 'sf')],
        results_pos_tag_universal = [('한국어', 'PROPN'), ('(', 'PUNCT'), ('韓國語', 'PROPN'), (')', 'PUNCT'), (',', 'PUNCT'), ('조선어', 'PROPN'), ('(', 'PUNCT'), ('朝鮮語', 'PROPN'), (')', 'PUNCT'), ('는', 'ADP'), ('대한민국과', 'CCONJ'), ('조선민주주의인민공화국의', 'PROPN'), ('공용어이다', 'VERB'), ('.', 'PUNCT')],
        results_lemmatize = ['한국어', '(', '韓國語', ')', ',', '조선어', '(', '朝鮮語', ')', '는', '대한민국+과', '조선민주주의인민공+화국+의', '공용어+이+다', '.'],
        results_dependency_parse = [('한국어', '공용어이다', 'advmod', 12), ('(', '韓國語', 'punct', 1), ('韓國語', '한국어', 'appos', -2), (')', '韓國語', 'punct', -1), (',', '한국어', 'punct', -4), ('조선어', '한국어', 'flat', -5), ('(', '朝鮮語', 'punct', 1), ('朝鮮語', '조선어', 'appos', -2), (')', '朝鮮語', 'punct', -1), ('는', '조선어', 'case', -4), ('대한민국과', '공용어이다', 'nmod', 2), ('조선민주주의인민공화국의', '대한민국과', 'conj', -1), ('공용어이다', '공용어이다', 'ROOT', 0), ('.', '공용어이다', 'punct', -1)]
    )

if __name__ == '__main__':
    test_spacy_kor()
