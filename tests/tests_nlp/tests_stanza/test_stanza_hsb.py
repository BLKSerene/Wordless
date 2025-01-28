# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Sorbian (Upper)
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

def test_stanza_hsb():
    results_pos_tag = [('Hornjoserbšćina', 'NOUN'), ('je', 'AUX'), ('zapadosłowjanska', 'ADJ'), ('rěč', 'NOUN'), (',', 'PUNCT'), ('kotraž', 'DET'), ('so', 'PRON'), ('w', 'ADP'), ('Hornjej', 'ADJ'), ('Łužicy', 'PROPN'), ('wokoło', 'ADP'), ('městow', 'NOUN'), ('Budyšin', 'PROPN'), (',', 'PUNCT'), ('Kamjenc', 'PROPN'), ('a', 'CCONJ'), ('Wojerecy', 'PROPN'), ('rěči', 'VERB'), ('.', 'PUNCT')]

    test_stanza.wl_test_stanza(
        lang = 'hsb',
        results_sentence_tokenize = ['Hornjoserbšćina je zapadosłowjanska rěč, kotraž so w Hornjej Łužicy wokoło městow Budyšin, Kamjenc a Wojerecy rěči.', 'Wona je přiwuzna z delnjoserbšćinu w susodnej Delnjej Łužicy, čěšćinu, pólšćinu, słowakšćinu a kašubšćinu.', 'Jako słowjanska rěč hornjoserbšćina k indoeuropskim rěčam słuša.'],
        results_word_tokenize = ['Hornjoserbšćina', 'je', 'zapadosłowjanska', 'rěč', ',', 'kotraž', 'so', 'w', 'Hornjej', 'Łužicy', 'wokoło', 'městow', 'Budyšin', ',', 'Kamjenc', 'a', 'Wojerecy', 'rěči', '.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['hornjoserbšćina', 'być', 'zapadosłowjanski', 'rěč', ',', 'kotryž', 'so', 'w', 'horni', 'Łužica', 'wokoło', 'město', 'Budyšin', ',', 'Kamjenc', 'a', 'Wojerecy', 'rěčeć', '.'],
        results_dependency_parse = [('Hornjoserbšćina', 'rěč', 'nsubj', 3), ('je', 'rěč', 'cop', 2), ('zapadosłowjanska', 'rěč', 'amod', 1), ('rěč', 'rěč', 'root', 0), (',', 'rěči', 'punct', 13), ('kotraž', 'rěči', 'nsubj', 12), ('so', 'rěči', 'expl:pv', 11), ('w', 'Łužicy', 'case', 2), ('Hornjej', 'Łužicy', 'amod', 1), ('Łužicy', 'rěči', 'obl', 8), ('wokoło', 'městow', 'case', 1), ('městow', 'rěči', 'obl', 6), ('Budyšin', 'městow', 'nmod', -1), (',', 'Kamjenc', 'punct', 1), ('Kamjenc', 'Budyšin', 'conj', -2), ('a', 'Wojerecy', 'cc', 1), ('Wojerecy', 'Budyšin', 'conj', -4), ('rěči', 'rěč', 'acl', -14), ('.', 'rěč', 'punct', -15)]
    )

if __name__ == '__main__':
    test_stanza_hsb()
