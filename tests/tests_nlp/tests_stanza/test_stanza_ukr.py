# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Ukrainian
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

def test_stanza_ukr():
    test_stanza.wl_test_stanza(
        lang = 'ukr',
        results_sentence_tokenize = ['Украї́нська мо́ва (МФА: [ukrɑ̽ˈjɪnʲsʲkɑ̽ ˈmɔwɑ̽], історичні назви — ру́ська[10][11][12][* 1]) — національна мова українців.', "Належить до східнослов'янської групи слов'янських мов, що входять до індоєвропейської мовної сім'ї, поряд з романськими, германськими, кельтськими, грецькою, албанською, вірменською та найближче спорідненими зі слов'янськими балтійськими мовами[13][14][* 2].", 'Є державною мовою в Україні[13][15].'],
        results_word_tokenize = ['Украї́нська', 'мо́ва', '(', 'МФА', ':', '[ukrɑ̽ˈjɪnʲsʲkɑ', '̽', 'ˈ', 'mɔwɑ̽', ']', ',', 'історичні', 'назви', '—', 'ру́ська', '[', '10', ']', '[', '11', ']', '[', '12', ']', '[*', '1', ']', ')', '—', 'національна', 'мова', 'українців', '.'],
        results_pos_tag = [('Украї́нська', 'Ao-fsns'), ('мо́ва', 'Ncfsnn'), ('(', 'U'), ('МФА', 'Y'), (':', 'U'), ('[ukrɑ̽ˈjɪnʲsʲkɑ', 'X'), ('̽', 'X'), ('ˈ', 'X'), ('mɔwɑ̽', 'X'), (']', 'U'), (',', 'U'), ('історичні', 'Ao--pns'), ('назви', 'Ncfpnn'), ('—', 'U'), ('ру́ська', 'Ao-fsns'), ('[', 'U'), ('10', 'Mlc-n'), (']', 'U'), ('[', 'U'), ('11', 'Mlc-n'), (']', 'U'), ('[', 'U'), ('12', 'Mlc-n'), (']', 'U'), ('[*', 'U'), ('1', 'Mlc-sn'), (']', 'U'), (')', 'U'), ('—', 'U'), ('національна', 'Ao-fsns'), ('мова', 'Ncfsnn'), ('українців', 'Ncmpgy'), ('.', 'U')],
        results_pos_tag_universal = [('Украї́нська', 'ADJ'), ('мо́ва', 'NOUN'), ('(', 'PUNCT'), ('МФА', 'NOUN'), (':', 'PUNCT'), ('[ukrɑ̽ˈjɪnʲsʲkɑ', 'X'), ('̽', 'SYM'), ('ˈ', 'X'), ('mɔwɑ̽', 'X'), (']', 'PUNCT'), (',', 'PUNCT'), ('історичні', 'ADJ'), ('назви', 'NOUN'), ('—', 'PUNCT'), ('ру́ська', 'ADJ'), ('[', 'PUNCT'), ('10', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('11', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('12', 'NUM'), (']', 'PUNCT'), ('[*', 'PUNCT'), ('1', 'NUM'), (']', 'PUNCT'), (')', 'PUNCT'), ('—', 'PUNCT'), ('національна', 'ADJ'), ('мова', 'NOUN'), ('українців', 'NOUN'), ('.', 'PUNCT')],
        results_lemmatize = ['український', 'мова', '(', 'МФА', ':', '[ukrɑ̽ˈjɪnʲsʲkɑ', '̽', 'ˈ', 'mɔwɑ̽', ']', ',', 'історичний', 'назва', '—', 'ру́ський', '[', '10', ']', '[', '11', ']', '[', '12', ']', '[*', '1', ']', ')', '—', 'національний', 'мова', 'українець', '.'],
        results_dependency_parse = [('Украї́нська', 'мо́ва', 'amod', 1), ('мо́ва', 'мова', 'nsubj', 29), ('(', 'МФА', 'punct', 1), ('МФА', 'мо́ва', 'parataxis', -2), (':', '[ukrɑ̽ˈjɪnʲsʲkɑ', 'punct', 1), ('[ukrɑ̽ˈjɪnʲsʲkɑ', 'МФА', 'flat:foreign', -2), ('̽', 'МФА', 'flat:foreign', -3), ('ˈ', 'МФА', 'flat:foreign', -4), ('mɔwɑ̽', 'МФА', 'flat:foreign', -5), (']', 'МФА', 'punct', -6), (',', 'назви', 'punct', 2), ('історичні', 'назви', 'amod', 1), ('назви', 'мо́ва', 'conj', -11), ('—', 'ру́ська', 'punct', 1), ('ру́ська', 'назви', 'appos', -2), ('[', '10', 'punct', 1), ('10', 'ру́ська', 'flat:range', -2), (']', 'ру́ська', 'punct', -3), ('[', '11', 'punct', 1), ('11', 'ру́ська', 'parataxis', -5), (']', '11', 'punct', -1), ('[', '12', 'punct', 1), ('12', '11', 'parataxis', -3), (']', '12', 'punct', -1), ('[*', '1', 'punct', 1), ('1', '12', 'appos', -3), (']', '12', 'punct', -4), (')', '11', 'punct', -8), ('—', 'мова', 'punct', 2), ('національна', 'мова', 'amod', 1), ('мова', 'мова', 'root', 0), ('українців', 'мова', 'nmod', -1), ('.', 'мова', 'punct', -2)]
    )

if __name__ == '__main__':
    test_stanza_ukr()
