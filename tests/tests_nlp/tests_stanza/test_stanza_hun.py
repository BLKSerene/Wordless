# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Hungarian
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

def test_stanza_hun():
    results_pos_tag = [('A', 'DET'), ('magyar', 'ADJ'), ('nyelv', 'NOUN'), ('az', 'DET'), ('uráli', 'ADJ'), ('nyelvcsalád', 'NOUN'), ('tagja', 'NOUN'), (',', 'PUNCT'), ('a', 'DET'), ('finnugor', 'NOUN'), ('nyelvek', 'NOUN'), ('közé', 'ADP'), ('tartozó', 'ADJ'), ('ugor', 'ADJ'), ('nyelvek', 'NOUN'), ('egyike', 'NOUN'), ('.', 'PUNCT')]

    test_stanza.wl_test_stanza(
        lang = 'hun',
        results_sentence_tokenize = ['A magyar nyelv az uráli nyelvcsalád tagja, a finnugor nyelvek közé tartozó ugor nyelvek egyike.', 'Legközelebbi rokonai a manysi és a hanti nyelv, majd utánuk az udmurt, a komi, a mari és a mordvin nyelvek.', 'Vannak olyan vélemények, melyek szerint a moldvai csángó önálló nyelv – különösen annak északi, középkori változata –, így ez volna a magyar legközelebbi rokonnyelve.', '[1]'],
        results_word_tokenize = ['A', 'magyar', 'nyelv', 'az', 'uráli', 'nyelvcsalád', 'tagja', ',', 'a', 'finnugor', 'nyelvek', 'közé', 'tartozó', 'ugor', 'nyelvek', 'egyike', '.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['a', 'magyar', 'nyelv', 'az', 'uráli', 'nyelvcsalád', 'tag', ',', 'a', 'finnugor', 'nyelv', 'közé', 'tartozó', 'ugor', 'nyelv', 'egyike', '.'],
        results_dependency_parse = [('A', 'nyelv', 'det', 2), ('magyar', 'nyelv', 'amod:att', 1), ('nyelv', 'tagja', 'nsubj', 4), ('az', 'nyelvcsalád', 'det', 2), ('uráli', 'nyelvcsalád', 'amod:att', 1), ('nyelvcsalád', 'tagja', 'nmod:att', 1), ('tagja', 'tagja', 'root', 0), (',', 'nyelvek', 'punct', 3), ('a', 'finnugor', 'det', 1), ('finnugor', 'nyelvek', 'nmod:att', 1), ('nyelvek', 'tartozó', 'obl', 2), ('közé', 'nyelvek', 'case', -1), ('tartozó', 'nyelvek', 'amod:att', 2), ('ugor', 'nyelvek', 'amod:att', 1), ('nyelvek', 'egyike', 'nmod:att', 1), ('egyike', 'tagja', 'conj', -9), ('.', 'egyike', 'punct', -1)]
    )

if __name__ == '__main__':
    test_stanza_hun()
