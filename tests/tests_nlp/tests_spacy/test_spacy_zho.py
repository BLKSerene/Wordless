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
    results_sentence_tokenize = ['汉语又称华语[6][7]，是来自汉民族的语言[8][7][9]。', '汉语是汉藏语系中最大的一支语族，若把整个汉语族视为单一语言，则汉语为世界上母语使用者人数最多的语言，目前全世界有五分之一人口将其作为母语或第二语言。']
    results_word_tokenize = ['汉语', '又', '称', '华语', '[6', ']', '[', '7', ']', '，', '是', '来自', '汉民族', '的', '语言', '[', '8', ']', '[', '7', ']', '[', '9', ']', '。']

    test_spacy.wl_test_spacy(
        lang = 'zho_cn',
        results_sentence_tokenize_dependency_parser = results_sentence_tokenize,
        results_sentence_tokenize_sentence_recognizer = results_sentence_tokenize,
        results_word_tokenize = results_word_tokenize,
        results_pos_tag = [('汉语', 'NN'), ('又', 'AD'), ('称', 'VV'), ('华语', 'NN'), ('[6', 'JJ'), (']', 'NN'), ('[', 'PU'), ('7', 'CD'), (']', 'NN'), ('，', 'PU'), ('是', 'VC'), ('来自', 'VV'), ('汉民族', 'NN'), ('的', 'DEC'), ('语言', 'NN'), ('[', 'PU'), ('8', 'CD'), (']', 'NN'), ('[', 'PU'), ('7', 'CD'), (']', 'NN'), ('[', 'PU'), ('9', 'CD'), (']', 'NN'), ('。', 'PU')],
        results_pos_tag_universal = [('汉语', 'NOUN'), ('又', 'ADV'), ('称', 'VERB'), ('华语', 'NOUN'), ('[6', 'ADJ'), (']', 'NOUN'), ('[', 'PUNCT'), ('7', 'NUM'), (']', 'NOUN'), ('，', 'PUNCT'), ('是', 'VERB'), ('来自', 'VERB'), ('汉民族', 'NOUN'), ('的', 'PART'), ('语言', 'NOUN'), ('[', 'PUNCT'), ('8', 'NUM'), (']', 'NOUN'), ('[', 'PUNCT'), ('7', 'NUM'), (']', 'NOUN'), ('[', 'PUNCT'), ('9', 'NUM'), (']', 'NOUN'), ('。', 'PUNCT')],
        results_lemmatize = results_word_tokenize,
        results_dependency_parse = [('汉语', '称', 'nsubj', 2), ('又', '称', 'advmod', 1), ('称', '称', 'ROOT', 0), ('华语', '[6', 'nsubj', 1), ('[6', ']', 'amod', 1), (']', '称', 'dobj', -3), ('[', '称', 'punct', -4), ('7', ']', 'dep', 1), (']', '语言', 'dep', 6), ('，', '语言', 'punct', 5), ('是', '语言', 'cop', 4), ('来自', '语言', 'acl', 3), ('汉民族', '来自', 'dobj', -1), ('的', '来自', 'mark', -2), ('语言', '称', 'conj', -12), ('[', '称', 'punct', -13), ('8', ']', 'dep', 1), (']', '称', 'dep', -15), ('[', '称', 'punct', -16), ('7', ']', 'dep', 1), (']', '称', 'dep', -18), ('[', '称', 'ccomp', -19), ('9', ']', 'dep', 1), (']', '[', 'dobj', -2), ('。', '称', 'punct', -22)]
    )

    results_sentence_tokenize = ['漢語又稱華語[6][7]，是來自漢民族的語言[8][7][9]。', '漢語是漢藏語系中最大的一支語族，若把整個漢語族視為單一語言，則漢語為世界上母語使用者人數最多的語言，目前全世界有五分之一人口將其作為母語或第二語言。']
    results_word_tokenize = ['漢語', '又', '稱華', '語[', '6', ']', '[', '7', ']', '，', '是', '來', '自漢', '民族', '的', '語言[', '8', ']', '[', '7', ']', '[', '9', ']', '。']

    test_spacy.wl_test_spacy(
        lang = 'zho_tw',
        results_sentence_tokenize_dependency_parser = results_sentence_tokenize,
        results_sentence_tokenize_sentence_recognizer = results_sentence_tokenize,
        results_word_tokenize = results_word_tokenize,
        results_pos_tag = [('漢語', 'NN'), ('又', 'AD'), ('稱華', 'VV'), ('語[', 'CD'), ('6', 'CD'), (']', 'NN'), ('[', 'PU'), ('7', 'CD'), (']', 'NN'), ('，', 'PU'), ('是', 'VC'), ('來', 'NN'), ('自漢', 'VV'), ('民族', 'NN'), ('的', 'DEG'), ('語言[', 'CD'), ('8', 'CD'), (']', 'NN'), ('[', 'PU'), ('7', 'CD'), (']', 'NN'), ('[', 'PU'), ('9', 'CD'), (']', 'NN'), ('。', 'PU')],
        results_pos_tag_universal = [('漢語', 'NOUN'), ('又', 'ADV'), ('稱華', 'VERB'), ('語[', 'NUM'), ('6', 'NUM'), (']', 'NOUN'), ('[', 'PUNCT'), ('7', 'NUM'), (']', 'NOUN'), ('，', 'PUNCT'), ('是', 'VERB'), ('來', 'NOUN'), ('自漢', 'VERB'), ('民族', 'NOUN'), ('的', 'PART'), ('語言[', 'NUM'), ('8', 'NUM'), (']', 'NOUN'), ('[', 'PUNCT'), ('7', 'NUM'), (']', 'NOUN'), ('[', 'PUNCT'), ('9', 'NUM'), (']', 'NOUN'), ('。', 'PUNCT')],
        results_lemmatize = results_word_tokenize,
        results_dependency_parse = [('漢語', '稱華', 'nsubj', 2), ('又', '稱華', 'advmod', 1), ('稱華', '稱華', 'ROOT', 0), ('語[', '6', 'dep', 1), ('6', ']', 'dep', 1), (']', '稱華', 'dobj', -3), ('[', '稱華', 'punct', -4), ('7', ']', 'dep', 1), (']', ']', 'dep', 9), ('，', ']', 'punct', 8), ('是', ']', 'cop', 7), ('來', '民族', 'compound:nn', 2), ('自漢', '民族', 'compound:nn', 1), ('民族', '8', 'nmod:assmod', 3), ('的', '民族', 'case', -1), ('語言[', '8', 'dep', 1), ('8', ']', 'dep', 1), (']', '稱華', 'conj', -15), ('[', '稱華', 'punct', -16), ('7', ']', 'dep', 1), (']', '稱華', 'dep', -18), ('[', '稱華', 'punct', -19), ('9', ']', 'dep', 1), (']', '稱華', 'dobj', -21), ('。', '稱華', 'punct', -22)]
    )

if __name__ == '__main__':
    test_spacy_zho()
