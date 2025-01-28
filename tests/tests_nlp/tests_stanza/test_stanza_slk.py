# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Slovak
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

def test_stanza_slk():
    test_stanza.wl_test_stanza(
        lang = 'slk',
        results_sentence_tokenize = ['Slovenčina je oficiálne úradným jazykom Slovenska, Vojvodiny a od 1. mája 2004 jedným z jazykov Európskej únie.', 'Jazykový kód alebo po anglicky Language', 'Code je sk príp. slk podľa ISO 639.', 'Slovenčina je známa ako „esperanto“ slovanských jazykov, vníma sa ako najzrozumiteľnejšia aj pre používateľov iných slovanských jazykov.', '[2]'],
        results_word_tokenize = ['Slovenčina', 'je', 'oficiálne', 'úradným', 'jazykom', 'Slovenska', ',', 'Vojvodiny', 'a', 'od', '1', '.', 'mája', '2004', 'jedným', 'z', 'jazykov', 'Európskej', 'únie', '.'],
        results_pos_tag = [('Slovenčina', 'SSfs1'), ('je', 'VKesc+'), ('oficiálne', 'Dx'), ('úradným', 'AAis7x'), ('jazykom', 'SSis7'), ('Slovenska', 'SSns2:r'), (',', 'Z'), ('Vojvodiny', 'SSfs2:r'), ('a', 'O'), ('od', 'Eu2'), ('1', '0'), ('.', 'Z'), ('mája', 'SSis2'), ('2004', '0'), ('jedným', 'NFis7'), ('z', 'Eu2'), ('jazykov', 'SSip2'), ('Európskej', 'AAfs2x:r'), ('únie', 'SSfs2'), ('.', 'Z')],
        results_pos_tag_universal = [('Slovenčina', 'NOUN'), ('je', 'AUX'), ('oficiálne', 'ADV'), ('úradným', 'ADJ'), ('jazykom', 'NOUN'), ('Slovenska', 'PROPN'), (',', 'PUNCT'), ('Vojvodiny', 'PROPN'), ('a', 'CCONJ'), ('od', 'ADP'), ('1', 'NUM'), ('.', 'PUNCT'), ('mája', 'NOUN'), ('2004', 'NUM'), ('jedným', 'NUM'), ('z', 'ADP'), ('jazykov', 'NOUN'), ('Európskej', 'ADJ'), ('únie', 'NOUN'), ('.', 'PUNCT')],
        results_lemmatize = ['slovenčina', 'byť', 'oficiálne', 'úradný', 'jazyk', 'slovensko', ',', 'vojvodiny', 'a', 'od', '1', '.', 'máj', '2004', 'jeden', 'z', 'jazyk', 'európsky', 'únia', '.'],
        results_dependency_parse = [('Slovenčina', 'jazykom', 'nsubj', 4), ('je', 'jazykom', 'cop', 3), ('oficiálne', 'úradným', 'advmod', 1), ('úradným', 'jazykom', 'amod', 1), ('jazykom', 'jazykom', 'root', 0), ('Slovenska', 'jazykom', 'nmod', -1), (',', 'Vojvodiny', 'punct', 1), ('Vojvodiny', 'Slovenska', 'conj', -2), ('a', 'jedným', 'cc', 6), ('od', 'mája', 'case', 3), ('1', 'mája', 'nummod', 2), ('.', '1', 'punct', -1), ('mája', 'jedným', 'obl', 2), ('2004', 'mája', 'nummod', -1), ('jedným', 'jazykom', 'conj', -10), ('z', 'jazykov', 'case', 1), ('jazykov', 'jedným', 'nmod', -2), ('Európskej', 'únie', 'amod', 1), ('únie', 'jazykov', 'nmod', -2), ('.', 'jazykom', 'punct', -15)]
    )

if __name__ == '__main__':
    test_stanza_slk()
