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
    results_sentence_tokenize = ['세계 여러 지역에 한민족 인구가 거주하게 되면서 전 세계 각지에서 한국어가 사용 되고 있다.', '2016년 1월 초 기준으로 한국어 사용 인구는 약 8,000만 명으로 추산된다.[1]']

    test_spacy.wl_test_spacy(
        lang = 'kor',
        results_sentence_tokenize_trf = results_sentence_tokenize,
        results_sentence_tokenize_lg = results_sentence_tokenize,
        results_word_tokenize = ['세계', '여러', '지역에', '한민족', '인구가', '거주하게', '되면서', '전', '세계', '각지에서', '한국어가', '사용', '되고', '있다', '.'],
        results_pos_tag = [('세계', 'ncn'), ('여러', 'mma'), ('지역에', 'ncn+jca'), ('한민족', 'ncn'), ('인구가', 'ncn+jcs'), ('거주하게', 'ncpa+xsv+ecx'), ('되면서', 'px+ecc'), ('전', 'mma'), ('세계', 'ncn'), ('각지에서', 'ncn+jca'), ('한국어가', 'ncn+jcs'), ('사용', 'ncpa'), ('되고', 'pvg+ecx'), ('있다', 'px+ef'), ('.', 'sf')],
        results_pos_tag_universal = [('세계', 'NOUN'), ('여러', 'ADJ'), ('지역에', 'ADV'), ('한민족', 'NOUN'), ('인구가', 'NOUN'), ('거주하게', 'VERB'), ('되면서', 'CCONJ'), ('전', 'ADJ'), ('세계', 'NOUN'), ('각지에서', 'ADV'), ('한국어가', 'NOUN'), ('사용', 'NOUN'), ('되고', 'VERB'), ('있다', 'AUX'), ('.', 'PUNCT')],
        results_lemmatize = ['세계', '여러', '지역+에', '한민족', '인구+가', '거주+하+게', '되+면서', '전', '세계', '각지+에서', '한국어+가', '사용', '되+고', '있+다', '.'],
        results_dependency_parse = [('세계', '지역에', 'compound', 2), ('여러', '지역에', 'amod', 1), ('지역에', '거주하게', 'obl', 3), ('한민족', '인구가', 'compound', 1), ('인구가', '거주하게', 'nsubj', 1), ('거주하게', '거주하게', 'ROOT', 0), ('되면서', '거주하게', 'aux', -1), ('전', '세계', 'amod', 1), ('세계', '각지에서', 'compound', 1), ('각지에서', '되고', 'advcl', 3), ('한국어가', '사용', 'nsubj', 1), ('사용', '되고', 'dep', 1), ('되고', '거주하게', 'conj', -7), ('있다', '되고', 'aux', -1), ('.', '있다', 'punct', -1)]
    )

if __name__ == '__main__':
    test_spacy_kor()
