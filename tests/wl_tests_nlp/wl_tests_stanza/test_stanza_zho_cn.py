# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Stanza - Chinese (Simplified)
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

def test_stanza_zho_cn():
    test_stanza.wl_test_stanza(
        lang = 'zho_cn',
        results_sentence_tokenize = ['汉语又称中文、华语[6]、唐话[7]，概指由上古汉语（先秦雅言）发展而来、书面使用汉字的分析语，为汉藏语系最大的一支语族。', '如把整个汉语族视为单一语言，则汉语为世界使用人数最多的语言，目前全世界有五分之一人口将汉语做为母语或第二语言。'],
        results_word_tokenize = ['汉', '语', '又', '称', '中', '文', '、', '华', '语', '[', '6', ']', '、', '唐话', '[', '7', ']', '，', '概指', '由', '上古', '汉', '语', '（', '先', '秦', '雅', '言', '）', '发展', '而', '来', '、', '书面', '使用', '汉字', '的', '分析', '语', '，', '为', '汉', '藏', '语系', '最大', '的', '一', '支', '语族', '。'],
        results_pos_tag = [('汉', 'NNP'), ('语', 'SFN'), ('又', 'RB'), ('称', 'VV'), ('中', 'NNP'), ('文', 'SFN'), ('、', 'EC'), ('华', 'NNP'), ('语', 'SFN'), ('[', 'NN'), ('6', 'CD'), (']', 'NN'), ('、', 'EC'), ('唐话', 'NNP'), ('[', '('), ('7', 'CD'), (']', ')'), ('，', ','), ('概指', 'NN'), ('由', 'VV'), ('上古', 'NNP'), ('汉', 'NNP'), ('语', 'SFN'), ('（', '('), ('先', 'NN'), ('秦', 'NNP'), ('雅', 'NNP'), ('言', 'VV'), ('）', ')'), ('发展', 'VV'), ('而', 'RB'), ('来', 'VV'), ('、', 'EC'), ('书面', 'NN'), ('使用', 'VV'), ('汉字', 'NN'), ('的', 'DEC'), ('分析', 'VV'), ('语', 'SFN'), ('，', ','), ('为', 'VC'), ('汉', 'NNP'), ('藏', 'NNP'), ('语系', 'NN'), ('最大', 'JJ'), ('的', 'DEC'), ('一', 'CD'), ('支', 'NNB'), ('语族', 'NN'), ('。', '.')],
        results_pos_tag_universal = [('汉', 'PROPN'), ('语', 'PART'), ('又', 'ADV'), ('称', 'VERB'), ('中', 'PROPN'), ('文', 'PART'), ('、', 'PUNCT'), ('华', 'PROPN'), ('语', 'PART'), ('[', 'NOUN'), ('6', 'NUM'), (']', 'NOUN'), ('、', 'PUNCT'), ('唐话', 'PROPN'), ('[', 'PUNCT'), ('7', 'NUM'), (']', 'PUNCT'), ('，', 'PUNCT'), ('概指', 'NOUN'), ('由', 'VERB'), ('上古', 'PROPN'), ('汉', 'PROPN'), ('语', 'PART'), ('（', 'PUNCT'), ('先', 'NOUN'), ('秦', 'PROPN'), ('雅', 'PROPN'), ('言', 'VERB'), ('）', 'PUNCT'), ('发展', 'VERB'), ('而', 'ADV'), ('来', 'VERB'), ('、', 'PUNCT'), ('书面', 'NOUN'), ('使用', 'VERB'), ('汉字', 'NOUN'), ('的', 'PART'), ('分析', 'VERB'), ('语', 'PART'), ('，', 'PUNCT'), ('为', 'AUX'), ('汉', 'PROPN'), ('藏', 'PROPN'), ('语系', 'NOUN'), ('最大', 'ADJ'), ('的', 'PART'), ('一', 'NUM'), ('支', 'NOUN'), ('语族', 'NOUN'), ('。', 'PUNCT')],
        results_lemmatize = ['汉', '语', '又', '称', '中', '文', '、', '华', '语', '[', '6', ']', '、', '唐话', '[', '7', ']', '，', '概指', '由', '上古', '汉', '语', '（', '先', '秦', '雅', '言', '）', '发展', '而', '来', '、', '书面', '使用', '汉字', '的', '分析', '语', '，', '为', '汉', '藏', '语系', '最大', '的', '一', '支', '语族', '。'],
        results_dependency_parse = [('汉', '语', 'compound', 1), ('语', '称', 'nsubj', 2), ('又', '称', 'mark', 1), ('称', '语族', 'acl', 45), ('中', '文', 'compound', 1), ('文', ']', 'nmod', 6), ('、', '语', 'punct', 2), ('华', '语', 'compound', 1), ('语', '文', 'conj', -3), ('[', ']', 'nmod', 2), ('6', ']', 'nummod', 1), (']', '称', 'obj', -8), ('、', '唐话', 'punct', 1), ('唐话', ']', 'conj', -2), ('[', '7', 'punct', 1), ('7', ']', 'nummod', -4), (']', '7', 'punct', -1), ('，', '称', 'punct', -14), ('概指', '语族', 'nsubj', 30), ('由', '语族', 'acl', 29), ('上古', '语', 'nmod', 2), ('汉', '语', 'compound', 1), ('语', '来', 'nsubj', 9), ('（', '言', 'punct', 4), ('先', '言', 'nsubj', 3), ('秦', '言', 'nsubj', 2), ('雅', '秦', 'flat:name', -1), ('言', '语', 'dislocated', -5), ('）', '言', 'punct', -1), ('发展', '来', 'advcl', 2), ('而', '来', 'mark', 1), ('来', '由', 'ccomp', -12), ('、', '使用', 'punct', 2), ('书面', '使用', 'nsubj', 1), ('使用', '语', 'acl:relcl', 4), ('汉字', '使用', 'obj', -1), ('的', '使用', 'mark:rel', -2), ('分析', '语', 'compound', 1), ('语', '由', 'obj', -19), ('，', '语族', 'punct', 9), ('为', '语族', 'cop', 8), ('汉', '语系', 'nmod', 2), ('藏', '语系', 'nmod', 1), ('语系', '最大', 'nsubj', 1), ('最大', '语族', 'acl:relcl', 4), ('的', '最大', 'mark:rel', -1), ('一', '支', 'nummod', 1), ('支', '语族', 'clf', 1), ('语族', '语族', 'root', 0), ('。', '语族', 'punct', -1)],
        results_sentiment_analayze = [0]
    )

if __name__ == '__main__':
    test_stanza_zho_cn()
