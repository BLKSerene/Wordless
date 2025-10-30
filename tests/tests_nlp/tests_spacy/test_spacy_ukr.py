# ----------------------------------------------------------------------
# Tests: NLP - spaCy - Ukrainian
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

def test_spacy_ukr():
    results_sentence_tokenize = ['Украї́нська мо́ва (МФА: [ʊkrɐˈjinʲsʲkɐ ˈmɔʋɐ], історична назва — ру́ська[10][11][12][* 1]) — національна мова українців.', "Належить до східнослов'янської групи слов'янських мов, що входять до індоєвропейської мовної сім'ї, поряд із романськими, германськими, кельтськими, грецькою, албанською, вірменською та найближче спорідненими зі слов'янськими балтійськими мовами[13][14][* 2]."]
    results_pos_tag = [('Украї́нська', 'ADJ'), ('мо́ва', 'PROPN'), ('(', 'PUNCT'), ('МФА', 'PROPN'), (':', 'PUNCT'), ('[', 'SYM'), ('ʊkrɐˈjinʲsʲkɐ', 'ADJ'), ('ˈmɔʋɐ', 'NOUN'), (']', 'SYM'), (',', 'PUNCT'), ('історична', 'ADJ'), ('назва', 'NOUN'), ('—', 'PUNCT'), ('ру́ська[10][11][12', 'NOUN'), (']', 'PUNCT'), ('[', 'SYM'), ('*', 'SYM'), ('1', 'NUM'), (']', 'NOUN'), (')', 'PUNCT'), ('—', 'PUNCT'), ('національна', 'ADJ'), ('мова', 'NOUN'), ('українців', 'NOUN'), ('.', 'PUNCT')]

    test_spacy.wl_test_spacy(
        lang = 'ukr',
        results_sentence_tokenize_dependency_parser = results_sentence_tokenize,
        results_sentence_tokenize_sentence_recognizer = results_sentence_tokenize,
        results_word_tokenize = ['Украї́нська', 'мо́ва', '(', 'МФА', ':', '[', 'ʊkrɐˈjinʲsʲkɐ', 'ˈmɔʋɐ', ']', ',', 'історична', 'назва', '—', 'ру́ська[10][11][12', ']', '[', '*', '1', ']', ')', '—', 'національна', 'мова', 'українців', '.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['украї́нська', 'мо́ва', '(', 'мфа', ':', '[', 'ʊkrɐˈjinʲsʲkɐ', 'ˈmɔʋɐ', ']', ',', 'історичний', 'назва', '—', 'ру́ська[10][11][12', ']', '[', '*', '1', ']', ')', '—', 'національний', 'мова', 'українець', '.'],
        results_dependency_parse = [('Украї́нська', 'мо́ва', 'amod', 1), ('мо́ва', 'мова', 'nsubj', 21), ('(', 'МФА', 'punct', 1), ('МФА', 'мо́ва', 'appos', -2), (':', 'ˈmɔʋɐ', 'punct', 3), ('[', 'ˈmɔʋɐ', 'punct', 2), ('ʊkrɐˈjinʲsʲkɐ', 'ˈmɔʋɐ', 'amod', 1), ('ˈmɔʋɐ', 'МФА', 'parataxis', -4), (']', 'ˈmɔʋɐ', 'punct', -1), (',', 'назва', 'punct', 2), ('історична', 'назва', 'amod', 1), ('назва', 'мо́ва', 'conj', -10), ('—', 'ру́ська[10][11][12', 'punct', 1), ('ру́ська[10][11][12', 'назва', 'appos', -2), (']', 'ру́ська[10][11][12', 'punct', -1), ('[', 'мо́ва', 'punct', -14), ('*', '1', 'punct', 1), ('1', 'мо́ва', 'parataxis', -16), (']', 'мо́ва', 'punct', -17), (')', 'мо́ва', 'punct', -18), ('—', 'мова', 'punct', 2), ('національна', 'мова', 'amod', 1), ('мова', 'мова', 'ROOT', 0), ('українців', 'мова', 'nmod', -1), ('.', 'мова', 'punct', -2)]
    )

if __name__ == '__main__':
    test_spacy_ukr()
