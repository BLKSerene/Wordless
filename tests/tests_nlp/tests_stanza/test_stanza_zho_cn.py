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
    test_stanza.wl_test_stanza(
        lang = 'zho_cn',
        results_sentence_tokenize = ['汉语又称中文、华语[6]、唐话[7]，概指由上古汉语（先秦雅言）发展而来、书面使用汉字的分析语，为汉藏语系最大的一支语族。', '如把整个汉语族视为单一语言，则汉语为世界使用人数最多的语言，目前全世界有五分之一人口将汉语做为母语或第二语言。'],
        results_word_tokenize = ['汉', '语', '又', '称', '中', '文', '、', '华', '语', '[', '6', ']', '、', '唐', '话', '[', '7', ']', '，', '概', '指', '由', '上古', '汉', '语', '（', '先', '秦', '雅言', '）', '发展', '而', '来', '、', '书面', '使用', '汉', '字', '的', '分析', '语', '，', '为', '汉', '藏', '语', '系', '最大', '的', '一', '支', '语族', '。'],
        results_pos_tag = [('汉', 'NNP'), ('语', 'SFN'), ('又', 'RB'), ('称', 'VV'), ('中', 'NNP'), ('文', 'SFN'), ('、', 'EC'), ('华', 'NNP'), ('语', 'SFN'), ('[', '('), ('6', 'CD'), (']', ')'), ('、', 'EC'), ('唐', 'NNP'), ('话', 'SFN'), ('[', '('), ('7', 'CD'), (']', ')'), ('，', ','), ('概', 'RB'), ('指', 'VV'), ('由', 'VV'), ('上古', 'NN'), ('汉', 'NNP'), ('语', 'SFN'), ('（', '('), ('先', 'NNP'), ('秦', 'NNP'), ('雅言', 'NNP'), ('）', ')'), ('发展', 'VV'), ('而', 'RB'), ('来', 'VV'), ('、', 'EC'), ('书面', 'NN'), ('使用', 'VV'), ('汉', 'NNP'), ('字', 'SFN'), ('的', 'DEC'), ('分析', 'VV'), ('语', 'SFN'), ('，', ','), ('为', 'VC'), ('汉', 'NNP'), ('藏', 'NNP'), ('语', 'SFN'), ('系', 'SFN'), ('最大', 'JJ'), ('的', 'DEC'), ('一', 'CD'), ('支', 'NNB'), ('语族', 'NN'), ('。', '.')],
        results_pos_tag_universal = [('汉', 'PROPN'), ('语', 'PART'), ('又', 'ADV'), ('称', 'VERB'), ('中', 'PROPN'), ('文', 'PART'), ('、', 'PUNCT'), ('华', 'PROPN'), ('语', 'PART'), ('[', 'PUNCT'), ('6', 'NUM'), (']', 'PUNCT'), ('、', 'PUNCT'), ('唐', 'PROPN'), ('话', 'PART'), ('[', 'PUNCT'), ('7', 'NUM'), (']', 'PUNCT'), ('，', 'PUNCT'), ('概', 'ADV'), ('指', 'VERB'), ('由', 'VERB'), ('上古', 'NOUN'), ('汉', 'PROPN'), ('语', 'PART'), ('（', 'PUNCT'), ('先', 'PROPN'), ('秦', 'PROPN'), ('雅言', 'PROPN'), ('）', 'PUNCT'), ('发展', 'VERB'), ('而', 'ADV'), ('来', 'VERB'), ('、', 'PUNCT'), ('书面', 'NOUN'), ('使用', 'VERB'), ('汉', 'PROPN'), ('字', 'PART'), ('的', 'PART'), ('分析', 'VERB'), ('语', 'PART'), ('，', 'PUNCT'), ('为', 'AUX'), ('汉', 'PROPN'), ('藏', 'PROPN'), ('语', 'PART'), ('系', 'PART'), ('最大', 'ADJ'), ('的', 'PART'), ('一', 'NUM'), ('支', 'NOUN'), ('语族', 'NOUN'), ('。', 'PUNCT')],
        results_lemmatize = ['汉', '语', '又', '称', '中', '文', '、', '华', '语', '[', '6', ']', '、', '唐', '话', '[', '7', ']', '，', '概', '指', '由', '上古', '汉', '语', '（', '先', '秦', '雅言', '）', '发展', '而', '来', '、', '书面', '使用', '汉', '字', '的', '分析', '语', '，', '为', '汉', '藏', '语', '系', '最大', '的', '一', '支', '语族', '。'],
        results_dependency_parse = [('汉', '语', 'compound', 1), ('语', '语族', 'nsubj', 50), ('又', '称', 'mark', 1), ('称', '语族', 'acl', 48), ('中', '文', 'compound', 1), ('文', '称', 'obj', -2), ('、', '语', 'punct', 2), ('华', '语', 'compound', 1), ('语', '文', 'conj', -3), ('[', ']', 'punct', 2), ('6', ']', 'nummod', 1), (']', '文', 'conj', -6), ('、', '话', 'punct', 2), ('唐', '话', 'compound', 1), ('话', '文', 'conj', -9), ('[', '7', 'punct', 1), ('7', '话', 'nummod', -2), (']', '7', 'punct', -1), ('，', '称', 'punct', -15), ('概', '指', 'advmod', 1), ('指', '语族', 'acl', 31), ('由', '指', 'xcomp', -1), ('上古', '语', 'nmod', 2), ('汉', '语', 'compound', 1), ('语', '发展', 'nsubj', 6), ('（', '先', 'punct', 1), ('先', '语', 'appos', -2), ('秦', '先', 'flat:name', -1), ('雅言', '先', 'appos', -2), ('）', '先', 'punct', -3), ('发展', '由', 'ccomp', -9), ('而', '来', 'mark', 1), ('来', '由', 'ccomp', -11), ('、', '使用', 'punct', 2), ('书面', '使用', 'nsubj', 1), ('使用', '来', 'conj', -3), ('汉', '字', 'compound', 1), ('字', '使用', 'obj', -2), ('的', '来', 'mark:rel', -6), ('分析', '语', 'compound', 1), ('语', '指', 'obj', -20), ('，', '指', 'punct', -21), ('为', '语族', 'cop', 9), ('汉', '系', 'nmod', 3), ('藏', '语', 'compound', 1), ('语', '系', 'compound', 1), ('系', '最大', 'nsubj', 1), ('最大', '语族', 'acl:relcl', 4), ('的', '最大', 'mark:rel', -1), ('一', '支', 'nummod', 1), ('支', '语族', 'clf', 1), ('语族', '语族', 'root', 0), ('。', '语族', 'punct', -1)],
        results_sentiment_analayze = [0]
    )

if __name__ == '__main__':
    test_stanza_zho_cn()
