# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Chinese (Traditional)
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

def test_stanza_zho_tw():
    results_word_tokenize = ['漢', '語', '又', '稱', '華', '語', '[', '6', ']', '[7', ']', '，', '是', '來', '自', '漢', '民族', '的', '語言', '[', '8]', '[7]', '[9', ']', '。']

    test_stanza.wl_test_stanza(
        lang = 'zho_tw',
        results_sentence_tokenize = ['漢語又稱華語[6][7]，是來自漢民族的語言[8][7][9]。', '漢語是漢藏語系中最大的一支語族，若把整個漢語族視為單一語言，則漢語為世界上母語使用者人數最多的語言，目前全世界有五分之一人口將其作為母語或第二語言。'],
        results_word_tokenize = results_word_tokenize,
        results_pos_tag = [('漢', 'NNP'), ('語', 'SFN'), ('又', 'RB'), ('稱', 'VV'), ('華', 'NNP'), ('語', 'SFN'), ('[', '('), ('6', 'CD'), (']', '/'), ('[7', 'NNP'), (']', ')'), ('，', ','), ('是', 'VC'), ('來', 'VV'), ('自', 'VV'), ('漢', 'NNP'), ('民族', 'NN'), ('的', 'DEC'), ('語言', 'NN'), ('[', '``'), ('8]', 'NN'), ('[7]', 'NNP'), ('[9', 'NN'), (']', ')'), ('。', '.')],
        results_pos_tag_universal = [('漢', 'PROPN'), ('語', 'PART'), ('又', 'SCONJ'), ('稱', 'VERB'), ('華', 'PROPN'), ('語', 'PART'), ('[', 'PUNCT'), ('6', 'NUM'), (']', 'SYM'), ('[7', 'PROPN'), (']', 'PUNCT'), ('，', 'PUNCT'), ('是', 'AUX'), ('來', 'VERB'), ('自', 'VERB'), ('漢', 'PROPN'), ('民族', 'NOUN'), ('的', 'SCONJ'), ('語言', 'NOUN'), ('[', 'PUNCT'), ('8]', 'NOUN'), ('[7]', 'PROPN'), ('[9', 'NOUN'), (']', 'PUNCT'), ('。', 'PUNCT')],
        results_lemmatize = results_word_tokenize,
        results_dependency_parse = [('漢', '語', 'compound', 1), ('語', '[9', 'nsubj', 21), ('又', '稱', 'mark', 1), ('稱', '[9', 'acl', 19), ('華', '語', 'compound', 1), ('語', '稱', 'obj', -2), ('[', '[7', 'punct', 3), ('6', '[7', 'nummod', 2), (']', '[7', 'nmod', 1), ('[7', '語', 'appos', -4), (']', '[7', 'punct', -1), ('，', '稱', 'punct', -8), ('是', '[9', 'cop', 10), ('來', '語言', 'acl:relcl', 5), ('自', '來', 'mark', -1), ('漢', '民族', 'nmod', 1), ('民族', '來', 'obj', -3), ('的', '來', 'mark:rel', -4), ('語言', '語言', 'root', 0), ('[', '[9', 'punct', 3), ('8]', '[9', 'nmod', 2), ('[7]', '[9', 'nmod', 1), ('[9', '語言', 'appos', -4), (']', '[9', 'punct', -1), ('。', '語言', 'punct', -6)]
    )

if __name__ == '__main__':
    test_stanza_zho_tw()
