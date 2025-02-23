# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Albanian
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

results_pos_tag = [('Keto', 'PRON'), ('gjuhe', 'NOUN'), ('kryesisht', 'ADV'), ('perdoret', 'VERB'), ('në', 'ADP'), ('Shqipëri', 'PROPN'), (',', 'PUNCT'), ('Kosovë', 'PROPN'), ('dhe', 'CCONJ'), ('Maqedoninë', 'PROPN'), ('e', 'DET'), ('Veriut', 'ADJ'), (',', 'PUNCT'), ('por', 'CCONJ'), ('edhe', 'ADV'), ('në', 'ADP'), ('zona', 'NOUN'), ('të', 'DET'), ('tjera', 'PRON'), ('të', 'DET'), ('Evropës', 'PROPN'), ('Juglindore', 'ADJ'), ('ku', 'ADV'), ('ka', 'VERB'), ('një', 'DET'), ('popullsi', 'NOUN'), ('shqiptare', 'ADJ'), (',', 'PUNCT'), ('duke', 'PART'), ('përfshirë', 'VERB'), ('Malin', 'NOUN'), ('e', 'DET'), ('Zi', 'ADJ'), ('dhe', 'CCONJ'), ('Luginën', 'NOUN'), ('e', 'DET'), ('Preshevës', 'NOUN'), ('.', 'PUNCT')]

def test_stanza_sqi():
    test_stanza.wl_test_stanza(
        lang = 'sqi',
        results_sentence_tokenize = ['Keto gjuhe kryesisht perdoret në Shqipëri, Kosovë dhe Maqedoninë e Veriut, por edhe në zona të tjera të Evropës Juglindore ku ka një popullsi shqiptare, duke përfshirë Malin e Zi dhe Luginën e Preshevës.', 'Shqipja është gjuha zyrtare e Shqipërisë dhe Kosovës, gjuhë bashkë-zyrtare e Maqedonisë së Veriut si dhe një nga gjuhët zyrtare e Malit të Zi.'],
        results_word_tokenize = ['Keto', 'gjuhe', 'kryesisht', 'perdoret', 'në', 'Shqipëri', ',', 'Kosovë', 'dhe', 'Maqedoninë', 'e', 'Veriut', ',', 'por', 'edhe', 'në', 'zona', 'të', 'tjera', 'të', 'Evropës', 'Juglindore', 'ku', 'ka', 'një', 'popullsi', 'shqiptare', ',', 'duke', 'përfshirë', 'Malin', 'e', 'Zi', 'dhe', 'Luginën', 'e', 'Preshevës', '.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['keto', 'gjuh', 'kryesisht', 'perdor', 'në', 'Shqipëri', ',', 'kosovë', 'dhe', 'Maqedoninë', 'e', 'Veri', ',', 'por', 'edhe', 'në', 'zonë', 'të', 'tjetër', 'të', 'Evropë', 'Juglindor', 'ku', 'kam', 'një', 'popullsi', 'shqiptar', ',', 'duke', 'përfshir', 'Mal', 'e', 'Zi', 'dhe', 'Luginë', 'e', 'preshevë', '.'],
        results_dependency_parse = [('Keto', 'gjuhe', 'det', 1), ('gjuhe', 'perdoret', 'nsubj', 2), ('kryesisht', 'perdoret', 'advmod', 1), ('perdoret', 'perdoret', 'root', 0), ('në', 'Shqipëri', 'case', 1), ('Shqipëri', 'perdoret', 'obl', -2), (',', 'perdoret', 'punct', -3), ('Kosovë', 'perdoret', 'parataxis', -4), ('dhe', 'Maqedoninë', 'cc', 1), ('Maqedoninë', 'perdoret', 'parataxis', -6), ('e', 'Veriut', 'det:adj', 1), ('Veriut', 'Maqedoninë', 'amod', -2), (',', 'por', 'punct', 1), ('por', 'zona', 'cc', 3), ('edhe', 'zona', 'advmod', 2), ('në', 'zona', 'case', 1), ('zona', 'ka', 'obl', 7), ('të', 'tjera', 'det', 1), ('tjera', 'zona', 'nmod:poss', -2), ('të', 'Evropës', 'det', 1), ('Evropës', 'tjera', 'nmod:poss', -2), ('Juglindore', 'Evropës', 'amod', -1), ('ku', 'ka', 'advmod', 1), ('ka', 'perdoret', 'conj', -20), ('një', 'popullsi', 'det', 1), ('popullsi', 'ka', 'obj', -2), ('shqiptare', 'popullsi', 'amod', -1), (',', 'ka', 'punct', -4), ('duke', 'përfshirë', 'mark', 1), ('përfshirë', 'ka', 'advcl', -6), ('Malin', 'përfshirë', 'obj', -1), ('e', 'Zi', 'det:adj', 1), ('Zi', 'Malin', 'amod', -2), ('dhe', 'Luginën', 'cc', 1), ('Luginën', 'përfshirë', 'conj', -5), ('e', 'Preshevës', 'det', 1), ('Preshevës', 'Luginën', 'nmod:poss', -2), ('.', 'perdoret', 'punct', -34)]
    )

if __name__ == '__main__':
    test_stanza_sqi()
