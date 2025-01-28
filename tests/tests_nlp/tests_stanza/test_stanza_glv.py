# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Manx
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

def test_stanza_glv():
    results_pos_tag = [('She', 'AUX'), ('Gaelg', 'PROPN'), ('(graït', 'NOUN'), (':', 'PUNCT'), ('/gɪlg/', 'NOUN'), (')', 'PUNCT'), ('çhengey', 'NOUN'), ('Ghaelagh', 'PROPN'), ('Vannin', 'PROPN'), ('.', 'PUNCT')]

    test_stanza.wl_test_stanza(
        lang = 'glv',
        results_sentence_tokenize = ['She Gaelg (graït: /gɪlg/) çhengey Ghaelagh Vannin.', "Haink y Ghaelg woish Shenn-Yernish, as t'ee cosoylagh rish Yernish as Gaelg ny h-Albey."],
        results_word_tokenize = ['She', 'Gaelg', '(graït', ':', '/gɪlg/', ')', 'çhengey', 'Ghaelagh', 'Vannin', '.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['she', 'Gaelg', 'ben', ':', '/gɪlg/', ')', 'çhengey', 'Gaelagh', 'Mannin', '.'],
        results_dependency_parse = [('She', 'Gaelg', 'cop', 1), ('Gaelg', 'Gaelg', 'root', 0), ('(graït', 'Gaelg', 'nmod', -1), (':', '/gɪlg/', 'punct', 1), ('/gɪlg/', 'Gaelg', 'appos', -3), (')', '/gɪlg/', 'punct', -1), ('çhengey', 'Gaelg', 'parataxis', -5), ('Ghaelagh', 'çhengey', 'nmod', -1), ('Vannin', 'Ghaelagh', 'nmod', -1), ('.', 'Gaelg', 'punct', -8)]
    )

if __name__ == '__main__':
    test_stanza_glv()
