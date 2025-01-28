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
    results_pos_tag = [('Украї́нська', 'ADJ'), ('мо́ва', 'NOUN'), ('(', 'PUNCT'), ('МФА', 'NOUN'), (':', 'PUNCT'), ('[', 'PUNCT'), ('ukrɑ̽ˈjɪnʲsʲkɑ̽', 'X'), ('ˈmɔwɑ̽', 'X'), (']', 'PUNCT'), (',', 'PUNCT'), ('історичні', 'ADJ'), ('назви', 'NOUN'), ('—', 'PUNCT'), ('ру́ська[10][11][12', 'SYM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('*', 'SYM'), ('1', 'NUM'), (']', 'PUNCT'), (')', 'PUNCT'), ('—', 'PUNCT'), ('національна', 'ADJ'), ('мова', 'NOUN'), ('українців', 'NOUN'), ('.', 'PUNCT')]

    test_spacy.wl_test_spacy(
        lang = 'ukr',
        results_sentence_tokenize_trf = ['Украї́нська мо́ва (МФА: [ukrɑ̽ˈjɪnʲsʲkɑ̽ ˈmɔwɑ̽], історичні назви — ру́ська[10][11][12][* 1]) — національна мова українців.', "Належить до східнослов'янської групи слов'янських мов, що входять до індоєвропейської мовної сім'ї, поряд з романськими, германськими, кельтськими, грецькою, албанською, вірменською та найближче спорідненими зі слов'янськими балтійськими мовами[13][14][* 2].", 'Є державною мовою в Україні[13][15].'],
        results_word_tokenize = ['Украї́нська', 'мо́ва', '(', 'МФА', ':', '[', 'ukrɑ̽ˈjɪnʲsʲkɑ̽', 'ˈmɔwɑ̽', ']', ',', 'історичні', 'назви', '—', 'ру́ська[10][11][12', ']', '[', '*', '1', ']', ')', '—', 'національна', 'мова', 'українців', '.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['украї́нська', 'мо́ва', '(', 'мфа', ':', '[', 'ukrɑ̽ˈjɪnʲsʲkɑ̽', 'ˈmɔwɑ̽', ']', ',', 'історичний', 'назва', '—', 'ру́ська[10][11][12', ']', '[', '*', '1', ']', ')', '—', 'національний', 'мова', 'українець', '.'],
        results_dependency_parse = [('Украї́нська', 'мо́ва', 'amod', 1), ('мо́ва', 'мова', 'nsubj', 21), ('(', 'МФА', 'punct', 1), ('МФА', 'мо́ва', 'parataxis', -2), (':', 'ukrɑ̽ˈjɪnʲsʲkɑ̽', 'punct', 2), ('[', 'ukrɑ̽ˈjɪnʲsʲkɑ̽', 'punct', 1), ('ukrɑ̽ˈjɪnʲsʲkɑ̽', 'МФА', 'appos', -3), ('ˈmɔwɑ̽', 'ukrɑ̽ˈjɪnʲsʲkɑ̽', 'flat:foreign', -1), (']', 'ukrɑ̽ˈjɪnʲsʲkɑ̽', 'punct', -2), (',', 'назви', 'punct', 2), ('історичні', 'назви', 'amod', 1), ('назви', 'МФА', 'parataxis', -8), ('—', 'ру́ська[10][11][12', 'punct', 1), ('ру́ська[10][11][12', 'МФА', 'parataxis', -10), (']', 'МФА', 'punct', -11), ('[', '*', 'punct', 1), ('*', 'МФА', 'discourse', -13), ('1', '*', 'flat:title', -1), (']', '*', 'punct', -2), (')', 'МФА', 'punct', -16), ('—', 'мова', 'punct', 2), ('національна', 'мова', 'amod', 1), ('мова', 'мова', 'ROOT', 0), ('українців', 'мова', 'nmod', -1), ('.', 'мова', 'punct', -2)]
    )

if __name__ == '__main__':
    test_spacy_ukr()
