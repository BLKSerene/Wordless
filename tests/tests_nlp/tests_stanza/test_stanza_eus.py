# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Basque
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

def test_stanza_eus():
    results_pos_tag = [('Euskara', 'NOUN'), ('Euskal', 'PROPN'), ('Herriko', 'NOUN'), ('hizkuntza', 'NOUN'), ('da', 'AUX'), ('.', 'PUNCT'), ('[8]', 'PUNCT')]

    test_stanza.wl_test_stanza(
        lang = 'eus',
        results_sentence_tokenize = ['Euskara Euskal Herriko hizkuntza da.', '[8] Hizkuntza bakartua da, ez baitzaio ahaidetasunik aurkitu.', 'Morfologiari dagokionez, hizkuntza eranskari eta ergatiboa da.', 'Euskaraz mintzo direnei euskaldun deritze.', 'Gaur egun, Euskal Herrian bertan ere hizkuntza gutxitua da, lurralde horretan gaztelania eta frantsesa nagusitu baitira.'],
        results_word_tokenize = ['Euskara', 'Euskal', 'Herriko', 'hizkuntza', 'da', '.', '[8]'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['euskara', 'Euskal', 'herri', 'hizkuntza', 'izan', '.', '[8]'],
        results_dependency_parse = [('Euskara', 'hizkuntza', 'nsubj', 3), ('Euskal', 'Herriko', 'compound', 1), ('Herriko', 'hizkuntza', 'nmod', 1), ('hizkuntza', 'hizkuntza', 'root', 0), ('da', 'hizkuntza', 'cop', -1), ('.', 'hizkuntza', 'punct', -2), ('[8]', '[8]', 'root', 0)]
    )

if __name__ == '__main__':
    test_stanza_eus()
