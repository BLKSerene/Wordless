# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Chinese (Simplified)
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

def test_stanza_zho_cn():
    results_word_tokenize = ['汉', '语', '又', '称', '华', '语', '[', '6][7', ']', '，', '是', '来', '自', '汉', '民族', '的', '语言', '[', '8][7]', '[9', ']', '。']

    test_stanza.wl_test_stanza(
        lang = 'zho_cn',
        results_sentence_tokenize = ['汉语又称华语[6][7]，是来自汉民族的语言[8][7][9]。', '汉语是汉藏语系中最大的一支语族，若把整个汉语族视为单一语言，则汉语为世界上母语使用者人数最多的语言，目前全世界有五分之一人口将其作为母语或第二语言。'],
        results_word_tokenize = results_word_tokenize,
        results_pos_tag = [('汉', 'NNP'), ('语', 'SFN'), ('又', 'RB'), ('称', 'VV'), ('华', 'NNP'), ('语', 'SFN'), ('[', '('), ('6][7', 'CD'), (']', ')'), ('，', ','), ('是', 'VC'), ('来', 'VV'), ('自', 'VV'), ('汉', 'NNP'), ('民族', 'NN'), ('的', 'DEC'), ('语言', 'NN'), ('[', '('), ('8][7]', 'CD'), ('[9', 'CD'), (']', ')'), ('。', '.')],
        results_pos_tag_universal = [('汉', 'PROPN'), ('语', 'PART'), ('又', 'SCONJ'), ('称', 'VERB'), ('华', 'PROPN'), ('语', 'PART'), ('[', 'PUNCT'), ('6][7', 'NUM'), (']', 'PUNCT'), ('，', 'PUNCT'), ('是', 'AUX'), ('来', 'VERB'), ('自', 'VERB'), ('汉', 'PROPN'), ('民族', 'NOUN'), ('的', 'SCONJ'), ('语言', 'NOUN'), ('[', 'PUNCT'), ('8][7]', 'NUM'), ('[9', 'NUM'), (']', 'PUNCT'), ('。', 'PUNCT')],
        results_lemmatize = results_word_tokenize,
        results_dependency_parse = [('汉', '语', 'compound', 1), ('语', '语言', 'nsubj', 15), ('又', '称', 'mark', 1), ('称', '语言', 'acl', 13), ('华', '语', 'compound', 1), ('语', '称', 'obj', -2), ('[', '6][7', 'punct', 1), ('6][7', '语', 'appos', -2), (']', '6][7', 'punct', -1), ('，', '称', 'punct', -6), ('是', '语言', 'cop', 6), ('来', '语言', 'acl:relcl', 5), ('自', '来', 'mark', -1), ('汉', '民族', 'nmod', 1), ('民族', '来', 'obj', -3), ('的', '来', 'mark:rel', -4), ('语言', '语言', 'root', 0), ('[', '[9', 'punct', 2), ('8][7]', '[9', 'nummod', 1), ('[9', '语言', 'appos', -3), (']', '[9', 'punct', -1), ('。', '语言', 'punct', -5)],
        results_sentiment_analayze = [0]
    )

if __name__ == '__main__':
    test_stanza_zho_cn()
