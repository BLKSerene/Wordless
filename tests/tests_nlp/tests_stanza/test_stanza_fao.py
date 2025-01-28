# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Faroese
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

def test_stanza_fao():
    test_stanza.wl_test_stanza(
        lang = 'fao',
        results_sentence_tokenize = ['Føroyskt er høvuðsmálið í Føroyum.', 'Føroyskt er almenna málið í Føroyum, og tað er tjóðarmál føroyinga.', 'Harafturat verður nógv føroyskt tosað í Danmark og Íslandi.', 'Í Føroyum tosa 48.', '000 fólk føroyskt, í Danmark umleið 25.', '000 og í Íslandi umleið 5.000, so samlaða talið av fólkum, ið duga føroyskt liggur um 75-80.', '000.', 'Føroyskt er tí í altjóða høpi eitt lítið mál.', 'Føroyskt mál hevur fýra føll og trý kyn, og grammatiski málbygningurin líkist ógvuliga nógv íslendskum, meðan orðatilfarið og í summum lutum úttalan líkist norska landsmálinum.'],
        results_word_tokenize = ['Føroyskt', 'er', 'høvuðsmálið', 'í', 'Føroyum', '.'],
        results_pos_tag = [('Føroyskt', 'ADJ-N'), ('er', 'BEPI'), ('høvuðsmálið', 'N-N'), ('í', 'P'), ('Føroyum', 'N-D'), ('.', '.')],
        results_pos_tag_universal = [('Føroyskt', 'ADJ'), ('er', 'AUX'), ('høvuðsmálið', 'NOUN'), ('í', 'ADP'), ('Føroyum', 'NOUN'), ('.', 'PUNCT')],
        results_dependency_parse = [('Føroyskt', 'Føroyskt', 'root', 0), ('er', 'Føroyskt', 'cop', -1), ('høvuðsmálið', 'Føroyskt', 'nsubj', -2), ('í', 'Føroyum', 'case', 1), ('Føroyum', 'Føroyskt', 'obl', -4), ('.', 'Føroyum', 'punct', -1)]
    )

if __name__ == '__main__':
    test_stanza_fao()
