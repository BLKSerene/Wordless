# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Estonian
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

def test_stanza_est():
    test_stanza.wl_test_stanza(
        lang = 'est',
        results_sentence_tokenize = ['Eesti keelel on kaks suuremat murderühma (põhjaeesti ja lõunaeesti), mõnes käsitluses eristatakse ka kirderanniku murdeid eraldi murderühmana.', 'Liikumisvõimaluste laienemine ning põhjaeesti keskmurde alusel loodud normitud eesti kirjakeele kasutus on põhjustanud murdeerinevuste taandumise.'],
        results_word_tokenize = ['Eesti', 'keelel', 'on', 'kaks', 'suuremat', 'murderühma', '(', 'põhjaeesti', 'ja', 'lõunaeesti', ')', ',', 'mõnes', 'käsitluses', 'eristatakse', 'ka', 'kirderanniku', 'murdeid', 'eraldi', 'murderühmana', '.'],
        results_pos_tag = [('Eesti', 'S'), ('keelel', 'S'), ('on', 'V'), ('kaks', 'N'), ('suuremat', 'A'), ('murderühma', 'S'), ('(', 'Z'), ('põhjaeesti', 'G'), ('ja', 'J'), ('lõunaeesti', 'S'), (')', 'Z'), (',', 'Z'), ('mõnes', 'P'), ('käsitluses', 'S'), ('eristatakse', 'V'), ('ka', 'D'), ('kirderanniku', 'S'), ('murdeid', 'S'), ('eraldi', 'A'), ('murderühmana', 'S'), ('.', 'Z')],
        results_pos_tag_universal = [('Eesti', 'PROPN'), ('keelel', 'NOUN'), ('on', 'AUX'), ('kaks', 'NUM'), ('suuremat', 'ADJ'), ('murderühma', 'NOUN'), ('(', 'PUNCT'), ('põhjaeesti', 'ADJ'), ('ja', 'CCONJ'), ('lõunaeesti', 'NOUN'), (')', 'PUNCT'), (',', 'PUNCT'), ('mõnes', 'DET'), ('käsitluses', 'NOUN'), ('eristatakse', 'VERB'), ('ka', 'ADV'), ('kirderanniku', 'NOUN'), ('murdeid', 'NOUN'), ('eraldi', 'ADJ'), ('murderühmana', 'NOUN'), ('.', 'PUNCT')],
        results_lemmatize = ['Eesti', 'keel', 'olema', 'kaks', 'suurem', 'murde_rühm', '(', 'põhja_eesti', 'ja', 'lõuna_eesti', ')', ',', 'mõni', 'käsitlus', 'eristama', 'ka', 'kirde_rannik', 'murde', 'eraldi', 'murde_rühm', '.'],
        results_dependency_parse = [('Eesti', 'keelel', 'nmod', 1), ('keelel', 'keelel', 'root', 0), ('on', 'keelel', 'cop', -1), ('kaks', 'murderühma', 'nummod', 2), ('suuremat', 'murderühma', 'amod', 1), ('murderühma', 'keelel', 'nsubj:cop', -4), ('(', 'põhjaeesti', 'punct', 1), ('põhjaeesti', 'murderühma', 'parataxis', -2), ('ja', 'lõunaeesti', 'cc', 1), ('lõunaeesti', 'põhjaeesti', 'conj', -2), (')', 'põhjaeesti', 'punct', -3), (',', 'eristatakse', 'punct', 3), ('mõnes', 'käsitluses', 'det', 1), ('käsitluses', 'eristatakse', 'obl', 1), ('eristatakse', 'keelel', 'conj', -13), ('ka', 'murdeid', 'advmod', 2), ('kirderanniku', 'murdeid', 'nmod', 1), ('murdeid', 'eristatakse', 'obj', -3), ('eraldi', 'murderühmana', 'amod', 1), ('murderühmana', 'eristatakse', 'obl', -5), ('.', 'keelel', 'punct', -19)]
    )

if __name__ == '__main__':
    test_stanza_est()
