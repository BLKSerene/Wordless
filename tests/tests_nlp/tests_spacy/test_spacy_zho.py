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
    results_word_tokenize = ['汉语', '又', '称', '中文', '、', '华语', '[6', ']', '、', '唐话', '[', '7', ']', '，', '概指', '由', '上古', '汉语', '（', '先', '秦雅言', '）', '发展', '而', '来', '、', '书面', '使用', '汉字', '的', '分析语', '，', '为', '汉藏', '语系', '最', '大', '的', '一', '支', '语族', '。']

    test_spacy.wl_test_spacy(
        lang = 'zho_cn',
        results_sentence_tokenize_trf = ['汉语又称中文、华语[6]、唐话[7]，概指由上古汉语（先秦雅言）发展而来、书面使用汉字的分析语，为汉藏语系最大的一支语族。如把整个汉语族视为单一语言，则汉语为世界使用人数最多的语言，目前全世界有五分之一人口将汉语做为母语或第二语言。'],
        results_word_tokenize = results_word_tokenize,
        results_pos_tag = [('汉语', 'NN'), ('又', 'AD'), ('称', 'VV'), ('中文', 'NN'), ('、', 'PU'), ('华语', 'NN'), ('[6', 'CD'), (']', 'PU'), ('、', 'PU'), ('唐话', 'NN'), ('[', 'PU'), ('7', 'CD'), (']', 'PU'), ('，', 'PU'), ('概指', 'NN'), ('由', 'P'), ('上古', 'NT'), ('汉语', 'NN'), ('（', 'PU'), ('先', 'JJ'), ('秦雅言', 'NR'), ('）', 'PU'), ('发展', 'VV'), ('而', 'MSP'), ('来', 'VV'), ('、', 'PU'), ('书面', 'NN'), ('使用', 'VV'), ('汉字', 'NN'), ('的', 'DEG'), ('分析语', 'NN'), ('，', 'PU'), ('为', 'VC'), ('汉藏', 'NR'), ('语系', 'NN'), ('最', 'AD'), ('大', 'VA'), ('的', 'DEC'), ('一', 'CD'), ('支', 'M'), ('语族', 'NN'), ('。', 'PU')],
        results_pos_tag_universal = [('汉语', 'NOUN'), ('又', 'ADV'), ('称', 'VERB'), ('中文', 'NOUN'), ('、', 'PUNCT'), ('华语', 'NOUN'), ('[6', 'NUM'), (']', 'PUNCT'), ('、', 'PUNCT'), ('唐话', 'NOUN'), ('[', 'PUNCT'), ('7', 'NUM'), (']', 'PUNCT'), ('，', 'PUNCT'), ('概指', 'NOUN'), ('由', 'ADP'), ('上古', 'NOUN'), ('汉语', 'NOUN'), ('（', 'PUNCT'), ('先', 'ADJ'), ('秦雅言', 'PROPN'), ('）', 'PUNCT'), ('发展', 'VERB'), ('而', 'PART'), ('来', 'VERB'), ('、', 'PUNCT'), ('书面', 'NOUN'), ('使用', 'VERB'), ('汉字', 'NOUN'), ('的', 'PART'), ('分析语', 'NOUN'), ('，', 'PUNCT'), ('为', 'VERB'), ('汉藏', 'PROPN'), ('语系', 'NOUN'), ('最', 'ADV'), ('大', 'VERB'), ('的', 'PART'), ('一', 'NUM'), ('支', 'NUM'), ('语族', 'NOUN'), ('。', 'PUNCT')],
        results_lemmatize = results_word_tokenize,
        results_dependency_parse = [('汉语', '称', 'nsubj', 2), ('又', '称', 'advmod', 1), ('称', '称', 'ROOT', 0), ('中文', '华语', 'conj', 2), ('、', '华语', 'punct', 1), ('华语', '称', 'dobj', -3), ('[6', '唐话', 'conj', 3), (']', '[6', 'punct', -1), ('、', '唐话', 'punct', 1), ('唐话', '称', 'dobj', -7), ('[', '称', 'punct', -8), ('7', '称', 'dep', -9), (']', '7', 'punct', -1), ('，', '称', 'punct', -11), ('概指', '发展', 'nsubj', 8), ('由', '汉语', 'case', 2), ('上古', '汉语', 'compound:nn', 1), ('汉语', '发展', 'nmod:prep', 5), ('（', '秦雅言', 'punct', 2), ('先', '秦雅言', 'amod', 1), ('秦雅言', '汉语', 'parataxis:prnmod', -3), ('）', '秦雅言', 'punct', -1), ('发展', '称', 'conj', -20), ('而', '来', 'aux:prtmod', 1), ('来', '发展', 'conj', -2), ('、', '发展', 'punct', -3), ('书面', '使用', 'nsubj', 1), ('使用', '发展', 'conj', -5), ('汉字', '分析语', 'nmod:assmod', 2), ('的', '汉字', 'case', -1), ('分析语', '使用', 'dobj', -3), ('，', '称', 'punct', -29), ('为', '语族', 'cop', 8), ('汉藏', '语系', 'nmod:assmod', 1), ('语系', '语族', 'compound:nn', 6), ('最', '大', 'advmod', 1), ('大', '语族', 'amod', 4), ('的', '大', 'mark', -1), ('一', '语族', 'nummod', 2), ('支', '一', 'mark:clf', -1), ('语族', '称', 'conj', -38), ('。', '称', 'punct', -39)]
    )

    results_word_tokenize = ['漢語', '又', '稱', '中文', '、', '華語', '[', '6', ']', '、', '唐話[', '7', ']', '，', '概指', '由', '上古', '漢語', '（', '先', '秦雅言', '）', '發展', '而', '來', '、', '書面', '使用', '漢字', '的', '分析語', '，', '為漢', '藏語', '系', '最', '大', '的', '一', '支', '語族', '。']

    test_spacy.wl_test_spacy(
        lang = 'zho_tw',
        results_sentence_tokenize_trf = ['漢語又稱中文、華語[6]、唐話[7]，概指由上古漢語（先秦雅言）發展而來、書面使用漢字的分析語，為漢藏語系最大的一支語族。', '如把整個漢語族視為單一語言，則漢語為世界使用人數最多的語言，目前全世界有五分之一人口將漢語做為母語或第二語言。'],
        results_word_tokenize = results_word_tokenize,
        results_pos_tag = [('漢語', 'NN'), ('又', 'AD'), ('稱', 'VV'), ('中文', 'NN'), ('、', 'PU'), ('華語', 'NN'), ('[', 'PU'), ('6', 'CD'), (']', 'PU'), ('、', 'PU'), ('唐話[', 'NR'), ('7', 'CD'), (']', 'PU'), ('，', 'PU'), ('概指', 'VV'), ('由', 'P'), ('上古', 'NR'), ('漢語', 'NR'), ('（', 'PU'), ('先', 'JJ'), ('秦雅言', 'NR'), ('）', 'PU'), ('發展', 'VV'), ('而', 'MSP'), ('來', 'VV'), ('、', 'PU'), ('書面', 'NN'), ('使用', 'VV'), ('漢字', 'NN'), ('的', 'DEC'), ('分析語', 'NN'), ('，', 'PU'), ('為漢', 'VV'), ('藏語', 'NR'), ('系', 'NN'), ('最', 'AD'), ('大', 'VA'), ('的', 'DEC'), ('一', 'CD'), ('支', 'M'), ('語族', 'NN'), ('。', 'PU')],
        results_pos_tag_universal = [('漢語', 'NOUN'), ('又', 'ADV'), ('稱', 'VERB'), ('中文', 'NOUN'), ('、', 'PUNCT'), ('華語', 'NOUN'), ('[', 'PUNCT'), ('6', 'NUM'), (']', 'PUNCT'), ('、', 'PUNCT'), ('唐話[', 'PROPN'), ('7', 'NUM'), (']', 'PUNCT'), ('，', 'PUNCT'), ('概指', 'VERB'), ('由', 'ADP'), ('上古', 'PROPN'), ('漢語', 'PROPN'), ('（', 'PUNCT'), ('先', 'ADJ'), ('秦雅言', 'PROPN'), ('）', 'PUNCT'), ('發展', 'VERB'), ('而', 'PART'), ('來', 'VERB'), ('、', 'PUNCT'), ('書面', 'NOUN'), ('使用', 'VERB'), ('漢字', 'NOUN'), ('的', 'PART'), ('分析語', 'NOUN'), ('，', 'PUNCT'), ('為漢', 'VERB'), ('藏語', 'PROPN'), ('系', 'NOUN'), ('最', 'ADV'), ('大', 'VERB'), ('的', 'PART'), ('一', 'NUM'), ('支', 'NUM'), ('語族', 'NOUN'), ('。', 'PUNCT')],
        results_lemmatize = results_word_tokenize,
        results_dependency_parse = [('漢語', '稱', 'nsubj', 2), ('又', '稱', 'advmod', 1), ('稱', '稱', 'ROOT', 0), ('中文', '華語', 'conj', 2), ('、', '華語', 'punct', 1), ('華語', '稱', 'dobj', -3), ('[', '6', 'punct', 1), ('6', '稱', 'dep', -5), (']', '6', 'punct', -1), ('、', '6', 'punct', -2), ('唐話[', '6', 'dep', -3), ('7', '6', 'dep', -4), (']', '7', 'punct', -1), ('，', '稱', 'punct', -11), ('概指', '稱', 'conj', -12), ('由', '漢語', 'case', 2), ('上古', '漢語', 'compound:nn', 1), ('漢語', '發展', 'nmod:prep', 5), ('（', '秦雅言', 'punct', 2), ('先', '秦雅言', 'amod', 1), ('秦雅言', '漢語', 'parataxis:prnmod', -3), ('）', '秦雅言', 'punct', -1), ('發展', '分析語', 'acl', 8), ('而', '來', 'aux:prtmod', 1), ('來', '發展', 'conj', -2), ('、', '發展', 'punct', -3), ('書面', '使用', 'nsubj', 1), ('使用', '發展', 'conj', -5), ('漢字', '使用', 'dobj', -1), ('的', '發展', 'mark', -7), ('分析語', '概指', 'dobj', -16), ('，', '稱', 'punct', -29), ('為漢', '稱', 'conj', -30), ('藏語', '系', 'compound:nn', 1), ('系', '大', 'dep', 2), ('最', '大', 'advmod', 1), ('大', '語族', 'amod', 4), ('的', '大', 'mark', -1), ('一', '語族', 'nummod', 2), ('支', '一', 'mark:clf', -1), ('語族', '為漢', 'dobj', -8), ('。', '稱', 'punct', -39)]
    )

if __name__ == '__main__':
    test_spacy_zho()
