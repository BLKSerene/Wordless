# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Russian (Old)
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

def test_stanza_orv():
    test_stanza.wl_test_stanza(
        lang = 'orv',
        results_sentence_tokenize = ['шаибатъ же ѿ бедерѧ г҃ мсци', 'а ѿ дабылѧ до шаибата в҃ мсца', 'моремъ итьти'],
        results_word_tokenize = ['шаибатъ', 'же', 'ѿ', 'бедерѧ', 'г҃', 'мсци'],
        results_pos_tag = [('шаибатъ', 'Ne'), ('же', 'Df'), ('ѿ', 'R-'), ('бедерѧ', 'Ne'), ('г҃', 'Ma'), ('мсци', 'Nb')],
        results_pos_tag_universal = [('шаибатъ', 'PROPN'), ('же', 'ADV'), ('ѿ', 'ADP'), ('бедерѧ', 'PROPN'), ('г҃', 'NUM'), ('мсци', 'NOUN')],
        results_lemmatize = ['шаибатъ', 'же', 'отъ', 'бедерь', 'трие', 'мѣсяць'],
        results_dependency_parse = [('шаибатъ', 'шаибатъ', 'root', 0), ('же', 'шаибатъ', 'discourse', -1), ('ѿ', 'бедерѧ', 'case', 1), ('бедерѧ', 'шаибатъ', 'nmod', -3), ('г҃', 'мсци', 'nummod', 1), ('мсци', 'шаибатъ', 'orphan', -5)]
    )

if __name__ == '__main__':
    test_stanza_orv()
