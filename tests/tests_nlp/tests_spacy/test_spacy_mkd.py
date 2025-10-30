# ----------------------------------------------------------------------
# Tests: NLP - spaCy - Macedonian
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

def test_spacy_mkd():
    results_sentence_tokenize = ['Македонски јазик — јужнословенски јазик, дел од групата словенски јазици од јазичното семејство на индоевропски јазици.', 'Македонскиот е службен и национален јазик во Македонија, а воедно е и официјално признат како регионален службен јазик во Горица и Пустец во Албанија каде што живее бројно македонско население, но и во Србија како официјален во општините Јабука и Пландиште, Романија и Косово.']
    results_pos_tag = [('Македонски', 'ADJ'), ('јазик', 'NOUN'), ('—', 'PUNCT'), ('јужнословенски', 'ADJ'), ('јазик', 'NOUN'), (',', 'PUNCT'), ('дел', 'NOUN'), ('од', 'ADP'), ('групата', 'NOUN'), ('словенски', 'ADJ'), ('јазици', 'NOUN'), ('од', 'ADP'), ('јазичното', 'ADJ'), ('семејство', 'NOUN'), ('на', 'ADP'), ('индоевропски', 'ADJ'), ('јазици', 'NOUN'), ('.', 'PUNCT')]

    test_spacy.wl_test_spacy(
        lang = 'mkd',
        results_sentence_tokenize_dependency_parser = results_sentence_tokenize,
        results_sentence_tokenize_sentence_recognizer = results_sentence_tokenize,
        results_word_tokenize = ['Македонски', 'јазик', '—', 'јужнословенски', 'јазик', ',', 'дел', 'од', 'групата', 'словенски', 'јазици', 'од', 'јазичното', 'семејство', 'на', 'индоевропски', 'јазици', '.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['Македонски', 'јаз', '—', 'јужнословенски', 'јаз', ',', 'дел', 'од', 'група', 'словенски', 'јазик', 'од', 'јазичен', 'семејство', 'на', 'индоевропски', 'јазик', '.'],
        results_dependency_parse = [('Македонски', 'јазик', 'att', 1), ('јазик', 'јазик', 'ROOT', 0), ('—', 'јазик', 'punct', -1), ('јужнословенски', 'јазик', 'att', 1), ('јазик', 'јазик', 'dep', -3), (',', 'јазик', 'punct', -4), ('дел', 'јазик', 'dep', -5), ('од', 'дел', 'prep', -1), ('групата', 'јазици', 'att', 2), ('словенски', 'јазици', 'att', 1), ('јазици', 'од', 'pobj', -3), ('од', 'јазици', 'prep', -1), ('јазичното', 'семејство', 'att', 1), ('семејство', 'јазици', 'pobj', -3), ('на', 'јазици', 'prep', -4), ('индоевропски', 'јазици', 'att', 1), ('јазици', 'на', 'pobj', -2), ('.', 'јазик', 'punct', -16)]
    )

if __name__ == '__main__':
    test_spacy_mkd()
