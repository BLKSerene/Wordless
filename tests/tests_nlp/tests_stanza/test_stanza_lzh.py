# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Stanza - Chinese (Classical)
# Copyright (C) 2018-2024  Ye Lei (叶磊)
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

from tests.tests_nlp.tests_stanza import test_stanza

def test_stanza_lzh():
    test_stanza.wl_test_stanza(
        lang = 'lzh',
        results_sentence_tokenize = ['先民言語，傳乎口耳', '，至結繩以記，事日贅，', '是結繩之不足，', '求諸繪圖，繪圖', '猶逾，而創字製文，金石竹帛載之，', '自劉漢而書諸紙。', '唐宋降，文士崇古非今，尚先秦', '古文，規法矩繩，典模乃定。', '由是，口述耳', '聞者雖變於百歲', '千載，手書目觀者猶通，前', '後貫延三代。', '唯文言非創於一舉而得，', '所式所尊，莫衷', '一是，時比燕越。'],
        results_word_tokenize = ['先', '民', '言', '語', '，', '傳', '乎', '口', '耳', '，', '至', '結', '繩', '以', '記', '，', '事', '日', '贅', '，', '是', '結', '繩', '之', '不', '足', '，', '求', '諸', '繪', '圖', '，', '繪', '圖', '猶', '逾', '，', '而', '創', '字', '製', '文', '，', '金', '石', '竹', '帛', '載', '之', '，', '自', '劉', '漢', '而', '書', '諸', '紙', '。'],
        results_pos_tag = [('先', 'n,名詞,固定物,関係'), ('民', 'n,名詞,人,人'), ('言', 'v,動詞,行為,伝達'), ('語', 'n,名詞,可搬,伝達'), ('，', 'v,副詞,否定,無界'), ('傳', 'v,動詞,行為,伝達'), ('乎', 'v,前置詞,基盤,*'), ('口', 'n,名詞,不可譲,身体'), ('耳', 'p,助詞,句末,*'), ('，', 'n,名詞,制度,儀礼'), ('至', 'v,動詞,行為,移動'), ('結', 'v,動詞,行為,動作'), ('繩', 'n,名詞,可搬,道具'), ('以', 'v,動詞,行為,動作'), ('記', 'v,動詞,行為,動作'), ('，', 'n,名詞,制度,儀礼'), ('事', 'n,名詞,可搬,成果物'), ('日', 'n,名詞,時,*'), ('贅', 'v,動詞,描写,形質'), ('，', 'v,動詞,描写,形質'), ('是', 'n,代名詞,指示,*'), ('結', 'v,動詞,行為,動作'), ('繩', 'n,名詞,可搬,道具'), ('之', 'p,助詞,接続,属格'), ('不', 'v,副詞,否定,無界'), ('足', 'v,助動詞,可能,*'), ('，', 'v,動詞,行為,動作'), ('求', 'v,動詞,行為,動作'), ('諸', 'n,名詞,数量,*'), ('繪', 'n,名詞,可搬,伝達'), ('圖', 'n,名詞,可搬,伝達'), ('，', 'n,名詞,可搬,道具'), ('繪', 'v,動詞,行為,動作'), ('圖', 'n,名詞,可搬,伝達'), ('猶', 'v,副詞,頻度,重複'), ('逾', 'v,動詞,行為,移動'), ('，', 'n,名詞,可搬,成果物'), ('而', 'p,助詞,接続,並列'), ('創', 'v,動詞,行為,設置'), ('字', 'n,名詞,不可譲,属性'), ('製', 'v,動詞,行為,動作'), ('文', 'n,名詞,可搬,伝達'), ('，', 'n,名詞,可搬,道具'), ('金', 'n,名詞,可搬,道具'), ('石', 'n,名詞,可搬,道具'), ('竹', 'n,名詞,固定物,樹木'), ('帛', 'n,名詞,可搬,道具'), ('載', 'n,名詞,人,名'), ('之', 'p,助詞,接続,属格'), ('，', 'n,名詞,可搬,成果物'), ('自', 'v,前置詞,経由,*'), ('劉', 'n,名詞,人,姓氏'), ('漢', 'n,名詞,人,名'), ('而', 'p,助詞,接続,並列'), ('書', 'v,動詞,行為,動作'), ('諸', 'n,代名詞,人称,他'), ('紙', 'n,名詞,可搬,道具'), ('。', 'p,助詞,句末,*')],
        results_pos_tag_universal = [('先', 'NOUN'), ('民', 'NOUN'), ('言', 'VERB'), ('語', 'NOUN'), ('，', 'ADV'), ('傳', 'VERB'), ('乎', 'ADP'), ('口', 'NOUN'), ('耳', 'PART'), ('，', 'NOUN'), ('至', 'VERB'), ('結', 'VERB'), ('繩', 'NOUN'), ('以', 'ADV'), ('記', 'VERB'), ('，', 'NOUN'), ('事', 'NOUN'), ('日', 'NOUN'), ('贅', 'VERB'), ('，', 'VERB'), ('是', 'PRON'), ('結', 'VERB'), ('繩', 'NOUN'), ('之', 'SCONJ'), ('不', 'ADV'), ('足', 'AUX'), ('，', 'VERB'), ('求', 'VERB'), ('諸', 'NOUN'), ('繪', 'NOUN'), ('圖', 'NOUN'), ('，', 'NOUN'), ('繪', 'VERB'), ('圖', 'NOUN'), ('猶', 'ADV'), ('逾', 'VERB'), ('，', 'NOUN'), ('而', 'CCONJ'), ('創', 'VERB'), ('字', 'NOUN'), ('製', 'VERB'), ('文', 'NOUN'), ('，', 'NOUN'), ('金', 'NOUN'), ('石', 'NOUN'), ('竹', 'NOUN'), ('帛', 'NOUN'), ('載', 'PROPN'), ('之', 'SCONJ'), ('，', 'NOUN'), ('自', 'ADP'), ('劉', 'PROPN'), ('漢', 'PROPN'), ('而', 'CCONJ'), ('書', 'VERB'), ('諸', 'PRON'), ('紙', 'NOUN'), ('。', 'PART')],
        results_lemmatize = ['先', '民', '言', '語', '，', '傳', '乎', '口', '耳', '，', '至', '結', '繩', '以', '記', '，', '事', '日', '贅', '，', '是', '結', '繩', '之', '不', '足', '，', '求', '諸', '繪', '圖', '，', '繪', '圖', '猶', '逾', '，', '而', '創', '字', '製', '文', '，', '金', '石', '竹', '帛', '載', '之', '，', '自', '劉', '漢', '而', '書', '諸', '紙', '。'],
        results_dependency_parse = [('先', '民', 'nmod', 1), ('民', '言', 'nmod', 1), ('言', '傳', 'nsubj', 3), ('語', '言', 'conj', -1), ('，', '傳', 'advmod', 1), ('傳', '傳', 'root', 0), ('乎', '口', 'case', 1), ('口', '傳', 'obl', -2), ('耳', '傳', 'discourse:sp', -3), ('，', '至', 'nsubj', 1), ('至', '至', 'root', 0), ('結', '至', 'ccomp', -1), ('繩', '結', 'obj', -1), ('以', '記', 'advmod', 1), ('記', '至', 'parataxis', -4), ('，', '事', 'nmod', 1), ('事', '記', 'obj', -2), ('日', '贅', 'obl:tmod', 1), ('贅', '記', 'ccomp', -4), ('，', '贅', 'flat:vv', -1), ('是', '結', 'nsubj', 1), ('結', '結', 'root', 0), ('繩', '，', 'nsubj', 4), ('之', '繩', 'case', -1), ('不', '足', 'advmod', 1), ('足', '，', 'aux', 1), ('，', '結', 'ccomp', -5), ('求', '求', 'root', 0), ('諸', '繪', 'nmod', 1), ('繪', '圖', 'nmod', 1), ('圖', '求', 'obj', -3), ('，', '圖', 'nmod', 2), ('繪', '圖', 'amod', 1), ('圖', '求', 'obj', -6), ('猶', '逾', 'advmod', 1), ('逾', '逾', 'root', 0), ('，', '逾', 'obj', -1), ('而', '創', 'cc', 1), ('創', '逾', 'conj', -3), ('字', '創', 'obj', -1), ('製', '逾', 'conj', -5), ('文', '製', 'obj', -1), ('，', '文', 'conj', -1), ('金', '文', 'conj', -2), ('石', '金', 'flat', -1), ('竹', '金', 'nmod', -2), ('帛', '竹', 'nmod', -1), ('載', '帛', 'nmod', -1), ('之', '載', 'case', -1), ('，', '創', 'obj', -11), ('自', '劉', 'case', 1), ('劉', '，', 'conj', -2), ('漢', '劉', 'flat', -1), ('而', '書', 'cc', 1), ('書', '劉', 'conj', -3), ('諸', '紙', 'nmod', 1), ('紙', '書', 'obj', -2), ('。', '書', 'discourse:sp', -3)]
    )

if __name__ == '__main__':
    test_stanza_lzh()
