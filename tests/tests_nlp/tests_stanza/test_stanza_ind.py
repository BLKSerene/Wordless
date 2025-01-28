# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Indonesian
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

def test_stanza_ind():
    test_stanza.wl_test_stanza(
        lang = 'ind',
        results_sentence_tokenize = ['Bahasa Indonesia adalah bahasa nasional dan resmi di seluruh wilayah Indonesia.', 'Ini merupakan bahasa komunikasi resmi, diajarkan di sekolah-sekolah, dan digunakan untuk penyiaran di media elektronik dan digital.', 'Sebagai negara dengan tingkat multilingual (terutama trilingual)[12][13] teratas di dunia, mayoritas orang Indonesia juga mampu bertutur dalam bahasa daerah atau bahasa suku mereka sendiri, dengan yang paling banyak dituturkan adalah bahasa Jawa dan Sunda yang juga memberikan pengaruh besar ke dalam elemen bahasa Indonesia itu sendiri.', '[14][15]'],
        results_word_tokenize = ['Bahasa', 'Indonesia', 'adalah', 'bahasa', 'nasional', 'dan', 'resmi', 'di', 'seluruh', 'wilayah', 'Indonesia', '.'],
        results_pos_tag = [('Bahasa', 'NSD'), ('Indonesia', 'NSD'), ('adalah', 'O--'), ('bahasa', 'NSD'), ('nasional', 'ASP'), ('dan', 'H--'), ('resmi', 'ASP'), ('di', 'R--'), ('seluruh', 'B--'), ('wilayah', 'NSD'), ('Indonesia', 'NSD'), ('.', 'Z--')],
        results_pos_tag_universal = [('Bahasa', 'PROPN'), ('Indonesia', 'PROPN'), ('adalah', 'AUX'), ('bahasa', 'NOUN'), ('nasional', 'ADJ'), ('dan', 'CCONJ'), ('resmi', 'ADJ'), ('di', 'ADP'), ('seluruh', 'DET'), ('wilayah', 'NOUN'), ('Indonesia', 'PROPN'), ('.', 'PUNCT')],
        results_lemmatize = ['bahasa', 'indonesia', 'adalah', 'bahasa', 'nasional', 'dan', 'resmi', 'di', 'seluruh', 'wilayah', 'indonesia', '.'],
        results_dependency_parse = [('Bahasa', 'bahasa', 'nsubj', 3), ('Indonesia', 'Bahasa', 'flat:name', -1), ('adalah', 'bahasa', 'cop', 1), ('bahasa', 'bahasa', 'root', 0), ('nasional', 'bahasa', 'amod', -1), ('dan', 'resmi', 'cc', 1), ('resmi', 'bahasa', 'conj', -3), ('di', 'wilayah', 'case', 2), ('seluruh', 'wilayah', 'det', 1), ('wilayah', 'bahasa', 'nmod', -6), ('Indonesia', 'wilayah', 'nmod', -1), ('.', 'bahasa', 'punct', -8)]
    )

if __name__ == '__main__':
    test_stanza_ind()
