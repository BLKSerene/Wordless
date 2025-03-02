# ----------------------------------------------------------------------
# Tests: NLP - spaCy - Chinese
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

def test_spacy_zho():
    results_word_tokenize = ['汉语', '又', '称', '华语', '[6', ']', '[', '7', ']', '，', '是', '来自', '汉民族', '的', '语言', '[', '8', ']', '[', '7', ']', '[', '9', ']', '。']

    test_spacy.wl_test_spacy(
        lang = 'zho_cn',
        results_sentence_tokenize_trf = ['汉语又称华语[6][7]，是来自汉民族的语言[8][7][9]。', '汉语是汉藏语系中最大的一支语族，若把整个汉语族视为单一语言，则汉语为世界上母语使用者人数最多的语言，目前全世界有五分之一人口将其作为母语或第二语言。'],
        results_word_tokenize = results_word_tokenize,
        results_pos_tag = [('汉语', 'NN'), ('又', 'AD'), ('称', 'VV'), ('华语', 'NN'), ('[6', 'CD'), (']', 'PU'), ('[', 'PU'), ('7', 'CD'), (']', 'PU'), ('，', 'PU'), ('是', 'VC'), ('来自', 'VV'), ('汉民族', 'NN'), ('的', 'DEC'), ('语言', 'NN'), ('[', 'PU'), ('8', 'CD'), (']', 'PU'), ('[', 'PU'), ('7', 'CD'), (']', 'PU'), ('[', 'PU'), ('9', 'CD'), (']', 'PU'), ('。', 'PU')],
        results_pos_tag_universal = [('汉语', 'NOUN'), ('又', 'ADV'), ('称', 'VERB'), ('华语', 'NOUN'), ('[6', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('7', 'NUM'), (']', 'PUNCT'), ('，', 'PUNCT'), ('是', 'VERB'), ('来自', 'VERB'), ('汉民族', 'NOUN'), ('的', 'PART'), ('语言', 'NOUN'), ('[', 'PUNCT'), ('8', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('7', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('9', 'NUM'), (']', 'PUNCT'), ('。', 'PUNCT')],
        results_lemmatize = results_word_tokenize,
        results_dependency_parse = [('汉语', '称', 'nsubj', 2), ('又', '称', 'advmod', 1), ('称', '称', 'ROOT', 0), ('华语', '称', 'dobj', -1), ('[6', '称', 'punct', -2), (']', '[6', 'punct', -1), ('[', '称', 'punct', -4), ('7', '称', 'dep', -5), (']', '7', 'punct', -1), ('，', '称', 'punct', -7), ('是', '语言', 'cop', 4), ('来自', '语言', 'acl', 3), ('汉民族', '来自', 'dobj', -1), ('的', '来自', 'mark', -2), ('语言', '称', 'conj', -12), ('[', '语言', 'punct', -1), ('8', '语言', 'dep', -2), (']', '8', 'punct', -1), ('[', '7', 'punct', 1), ('7', '称', 'dep', -17), (']', '7', 'punct', -1), ('[', '9', 'punct', 1), ('9', '7', 'dep', -3), (']', '9', 'punct', -1), ('。', '称', 'punct', -22)]
    )

    results_word_tokenize = ['漢語', '又', '稱華', '語[', '6', ']', '[', '7', ']', '，', '是', '來', '自漢', '民族', '的', '語言[', '8', ']', '[', '7', ']', '[', '9', ']', '。']

    test_spacy.wl_test_spacy(
        lang = 'zho_tw',
        results_sentence_tokenize_trf = ['漢語又稱華語[6][7]，是來自漢民族的語言[8][7][9]。', '漢語是漢藏語系中最大的一支語族，若把整個漢語族視為單一語言，則漢語為世界上母語使用者人數最多的語言，目前全世界有五分之一人口將其作為母語或第二語言。'],
        results_word_tokenize = results_word_tokenize,
        results_pos_tag = [('漢語', 'NN'), ('又', 'AD'), ('稱華', 'VV'), ('語[', 'NN'), ('6', 'CD'), (']', 'PU'), ('[', 'PU'), ('7', 'CD'), (']', 'PU'), ('，', 'PU'), ('是', 'VC'), ('來', 'VV'), ('自漢', 'VV'), ('民族', 'NN'), ('的', 'DEC'), ('語言[', 'NN'), ('8', 'CD'), (']', 'PU'), ('[', 'PU'), ('7', 'CD'), (']', 'PU'), ('[', 'PU'), ('9', 'CD'), (']', 'PU'), ('。', 'PU')],
        results_pos_tag_universal = [('漢語', 'NOUN'), ('又', 'ADV'), ('稱華', 'VERB'), ('語[', 'NOUN'), ('6', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('7', 'NUM'), (']', 'PUNCT'), ('，', 'PUNCT'), ('是', 'VERB'), ('來', 'VERB'), ('自漢', 'VERB'), ('民族', 'NOUN'), ('的', 'PART'), ('語言[', 'NOUN'), ('8', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('7', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('9', 'NUM'), (']', 'PUNCT'), ('。', 'PUNCT')],
        results_lemmatize = results_word_tokenize,
        results_dependency_parse = [('漢語', '稱華', 'nsubj', 2), ('又', '稱華', 'advmod', 1), ('稱華', '稱華', 'ROOT', 0), ('語[', '稱華', 'punct', -1), ('6', '稱華', 'dep', -2), (']', '6', 'punct', -1), ('[', '7', 'punct', 1), ('7', '稱華', 'dep', -5), (']', '7', 'punct', -1), ('，', '7', 'punct', -2), ('是', '語言[', 'cop', 5), ('來', '自漢', 'xcomp', 1), ('自漢', '語言[', 'acl', 3), ('民族', '自漢', 'dobj', -1), ('的', '自漢', 'mark', -2), ('語言[', '稱華', 'conj', -13), ('8', '稱華', 'dep', -14), (']', '8', 'punct', -1), ('[', '7', 'punct', 1), ('7', '稱華', 'dep', -17), (']', '7', 'punct', -1), ('[', '9', 'punct', 1), ('9', '7', 'dep', -3), (']', '9', 'punct', -1), ('。', '稱華', 'punct', -22)]
    )

if __name__ == '__main__':
    test_spacy_zho()
