# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Stanza - Chinese (Traditional)
# Copyright (C) 2018-2023  Ye Lei (叶磊)
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

from tests.wl_tests_nlp.wl_tests_stanza import test_stanza

def test_stanza_zho_tw():
    test_stanza.wl_test_stanza(
        lang = 'zho_tw',
        results_sentence_tokenize = ['漢語又稱中文、華語[6]、唐話[7]，概指由上古漢語（先秦雅言）發展而來、書面使用漢字的分析語，為漢藏語系最大的一支語族。', '如把整個漢語族視為單一語言，則漢語為世界使用人數最多的語言，目前全世界有五分之一人口將漢語做為母語或第二語言。'],
        results_word_tokenize = ['漢', '語', '又', '稱', '中', '文', '、', '華', '語', '[', '6', ']', '、', '唐話', '[', '7', ']', '，', '概', '指', '由', '上古', '漢', '語', '（', '先', '秦', '雅言', '）', '發展', '而來', '、', '書面', '使用', '漢字', '的', '分析', '語', '，', '為', '漢', '藏', '語', '系', '最大', '的', '一', '支', '語族', '。'],
        results_pos_tag = [('漢', 'NNP'), ('語', 'SFN'), ('又', 'RB'), ('稱', 'VV'), ('中', 'NNP'), ('文', 'SFN'), ('、', 'EC'), ('華', 'NNP'), ('語', 'SFN'), ('[', '('), ('6', 'CD'), (']', ')'), ('、', 'EC'), ('唐話', 'NNP'), ('[', 'HYPH'), ('7', 'CD'), (']', ')'), ('，', ','), ('概', 'RB'), ('指', 'VV'), ('由', 'VV'), ('上古', 'NNP'), ('漢', 'NNP'), ('語', 'SFN'), ('（', '('), ('先', 'PFA'), ('秦', 'NNP'), ('雅言', 'NNP'), ('）', ')'), ('發展', 'VV'), ('而來', 'VV'), ('、', 'EC'), ('書面', 'VV'), ('使用', 'VV'), ('漢字', 'NN'), ('的', 'DEC'), ('分析', 'VV'), ('語', 'SFN'), ('，', ','), ('為', 'VC'), ('漢', 'NNP'), ('藏', 'NNP'), ('語', 'SFN'), ('系', 'SFN'), ('最大', 'JJ'), ('的', 'DEC'), ('一', 'CD'), ('支', 'NNB'), ('語族', 'NN'), ('。', '.')],
        results_pos_tag_universal = [('漢', 'PROPN'), ('語', 'PART'), ('又', 'ADV'), ('稱', 'VERB'), ('中', 'PROPN'), ('文', 'PART'), ('、', 'PUNCT'), ('華', 'PROPN'), ('語', 'PART'), ('[', 'PUNCT'), ('6', 'NUM'), (']', 'PUNCT'), ('、', 'PUNCT'), ('唐話', 'PROPN'), ('[', 'PUNCT'), ('7', 'NUM'), (']', 'PUNCT'), ('，', 'PUNCT'), ('概', 'ADV'), ('指', 'VERB'), ('由', 'VERB'), ('上古', 'PROPN'), ('漢', 'PROPN'), ('語', 'PART'), ('（', 'PUNCT'), ('先', 'PART'), ('秦', 'PROPN'), ('雅言', 'PROPN'), ('）', 'PUNCT'), ('發展', 'VERB'), ('而來', 'VERB'), ('、', 'PUNCT'), ('書面', 'VERB'), ('使用', 'VERB'), ('漢字', 'NOUN'), ('的', 'PART'), ('分析', 'VERB'), ('語', 'PART'), ('，', 'PUNCT'), ('為', 'AUX'), ('漢', 'PROPN'), ('藏', 'PROPN'), ('語', 'PART'), ('系', 'PART'), ('最大', 'ADJ'), ('的', 'PART'), ('一', 'NUM'), ('支', 'NOUN'), ('語族', 'NOUN'), ('。', 'PUNCT')],
        results_lemmatize = ['漢', '語', '又', '稱', '中', '文', '、', '華', '語', '[', '6', ']', '、', '唐話', '[', '7', ']', '，', '概', '指', '由', '上古', '漢', '語', '（', '先', '秦', '雅言', '）', '發展', '而來', '、', '書面', '使用', '漢字', '的', '分析', '語', '，', '為', '漢', '藏', '語', '系', '最大', '的', '一', '支', '語族', '。'],
        results_dependency_parse = [('漢', '語', 'compound', 1), ('語', '語族', 'nsubj', 47), ('又', '稱', 'mark', 1), ('稱', '語族', 'acl', 45), ('中', '文', 'compound', 1), ('文', '稱', 'obj', -2), ('、', '語', 'punct', 2), ('華', '語', 'compound', 1), ('語', '文', 'conj', -3), ('[', '6', 'punct', 1), ('6', '文', 'conj', -5), (']', '6', 'punct', -1), ('、', '唐話', 'punct', 1), ('唐話', '文', 'conj', -8), ('[', '7', 'punct', 1), ('7', '唐話', 'conj', -2), (']', '唐話', 'punct', -3), ('，', '語族', 'punct', 31), ('概', '指', 'advmod', 1), ('指', '語族', 'acl', 29), ('由', '語', 'acl:relcl', 17), ('上古', '語', 'nmod', 2), ('漢', '語', 'compound', 1), ('語', '發展', 'nsubj', 6), ('（', '雅言', 'punct', 3), ('先', '雅言', 'case', 2), ('秦', '雅言', 'nmod', 1), ('雅言', '語', 'appos', -4), ('）', '雅言', 'punct', -1), ('發展', '由', 'ccomp', -9), ('而來', '發展', 'obj', -1), ('、', '書面', 'punct', 1), ('書面', '發展', 'conj', -3), ('使用', '由', 'conj', -13), ('漢字', '使用', 'obj', -1), ('的', '由', 'mark:rel', -15), ('分析', '語', 'compound', 1), ('語', '指', 'obj', -18), ('，', '語族', 'punct', 10), ('為', '語族', 'cop', 9), ('漢', '系', 'nmod', 3), ('藏', '語', 'compound', 1), ('語', '系', 'compound', 1), ('系', '最大', 'nsubj', 1), ('最大', '語族', 'acl:relcl', 4), ('的', '最大', 'mark:rel', -1), ('一', '支', 'nummod', 1), ('支', '語族', 'clf', 1), ('語族', '語族', 'root', 0), ('。', '語族', 'punct', -1)]
    )

if __name__ == '__main__':
    test_stanza_zho_tw()
