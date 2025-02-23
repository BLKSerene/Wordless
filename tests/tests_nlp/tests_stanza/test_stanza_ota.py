# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Turkish (Ottoman)
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

def test_stanza_ota():
    test_stanza.wl_test_stanza(
        lang = 'ota',
        results_sentence_tokenize = ['Musahabeme nihayet vermeden evvel edebiyat-ı hazıra-ı ricalden ziyade edebiyat-ı nisvanın bir feyz-i latife mazhar olduğunu söylemek isterim.', 'En başında Halide Salih Hanımefendi olduğu hâlde Nesl-i Cedid Edibelerinin ateşîn musahebelerini , rengîn mensur şiirlerini , teşrih-i ruha dair küçük hikâyelerini okudum.'],
        results_word_tokenize = ['Musahabeme', 'nihayet', 'vermeden', 'evvel', 'edebiyat-ı', 'hazıra-ı', 'ricalden', 'ziyade', 'edebiyat-ı', 'nisvanın', 'bir', 'feyz-i', 'latife', 'mazhar', 'olduğunu', 'söylemek', 'isterim', '.'],
        results_pos_tag = [('Musahabeme', 'ADV'), ('nihayet', 'ADV'), ('vermeden', 'Ptcp'), ('evvel', 'PCAbl'), ('edebiyat-ı', 'NOUN'), ('hazıra-ı', 'NOUN'), ('ricalden', 'NOUN'), ('ziyade', 'Adj'), ('edebiyat-ı', 'NOUN'), ('nisvanın', 'NOUN'), ('bir', 'Indef'), ('feyz-i', 'NOUN'), ('latife', 'NOUN'), ('mazhar', 'NOUN'), ('olduğunu', 'Ptcp'), ('söylemek', 'Vnoun'), ('isterim', 'VERB'), ('.', 'Stop')],
        results_pos_tag_universal = [('Musahabeme', 'ADV'), ('nihayet', 'ADV'), ('vermeden', 'VERB'), ('evvel', 'ADP'), ('edebiyat-ı', 'NOUN'), ('hazıra-ı', 'NOUN'), ('ricalden', 'NOUN'), ('ziyade', 'ADJ'), ('edebiyat-ı', 'NOUN'), ('nisvanın', 'NOUN'), ('bir', 'DET'), ('feyz-i', 'NOUN'), ('latife', 'NOUN'), ('mazhar', 'NOUN'), ('olduğunu', 'VERB'), ('söylemek', 'VERB'), ('isterim', 'VERB'), ('.', 'PUNCT')],
        results_lemmatize = ['Musahabeme', 'nihayet', 'ver', 'evvel', 'edebiyat', 'hazıra-ı', 'rical', 'ziyade', 'edebiyat', 'nisva', 'bir', 'feyz-i', 'latife', 'mazhar', 'ol', 'söy', 'iste', '.'],
        results_dependency_parse = [('Musahabeme', 'vermeden', 'advmod', 2), ('nihayet', 'vermeden', 'advmod', 1), ('vermeden', 'isterim', 'advcl', 14), ('evvel', 'vermeden', 'case', -1), ('edebiyat-ı', 'ricalden', 'nmod:poss', 2), ('hazıra-ı', 'ricalden', 'nmod:poss', 1), ('ricalden', 'mazhar', 'obl', 7), ('ziyade', 'edebiyat-ı', 'amod', 1), ('edebiyat-ı', 'isterim', 'obl', 8), ('nisvanın', 'mazhar', 'obl', 4), ('bir', 'feyz-i', 'det', 1), ('feyz-i', 'mazhar', 'obl', 2), ('latife', 'mazhar', 'obl', 1), ('mazhar', 'söylemek', 'csubj', 2), ('olduğunu', 'mazhar', 'compound:lvc', -1), ('söylemek', 'isterim', 'ccomp', 1), ('isterim', 'isterim', 'root', 0), ('.', 'isterim', 'punct', -1)]
    )

if __name__ == '__main__':
    test_stanza_ota()
