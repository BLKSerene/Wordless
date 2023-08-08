# ----------------------------------------------------------------------
# Wordless: Tests - NLP - POS Tagging
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

import pytest

from tests import wl_test_init, wl_test_lang_examples
from wordless.wl_nlp import wl_pos_tagging, wl_word_tokenization

main = wl_test_init.Wl_Test_Main()
wl_test_init.change_default_tokenizers(main)

test_pos_taggers = []

for lang, pos_taggers in main.settings_global['pos_taggers'].items():
    for pos_tagger in pos_taggers:
        # The Korean blank model for sentencizer requires mecab-ko which would be replaced by python-mecab-ko in the upcoming spaCy 4.0
        if not pos_tagger.startswith('spacy_') and lang != 'kor':
            test_pos_taggers.append((lang, pos_tagger))

@pytest.mark.parametrize('lang, pos_tagger', test_pos_taggers)
def test_pos_tag(lang, pos_tagger):
    # Untokenized
    tokens_tagged = wl_pos_tagging.wl_pos_tag(
        main,
        inputs = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}'),
        lang = lang,
        pos_tagger = pos_tagger
    )
    tokens_tagged_universal = wl_pos_tagging.wl_pos_tag(
        main,
        inputs = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}'),
        lang = lang,
        pos_tagger = pos_tagger,
        tagset = 'universal'
    )

    # Tokenized
    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}'),
        lang = lang
    )
    tokens_tagged_tokenized = wl_pos_tagging.wl_pos_tag(
        main,
        inputs = tokens,
        lang = lang,
        pos_tagger = pos_tagger
    )
    tokens_tagged_universal_tokenized = wl_pos_tagging.wl_pos_tag(
        main,
        inputs = tokens,
        lang = lang,
        pos_tagger = pos_tagger,
        tagset = 'universal'
    )

    # Long texts
    tokens_tagged_tokenized_long = wl_pos_tagging.wl_pos_tag(
        main,
        inputs = [str(i) for i in range(101) for j in range(50)],
        lang = lang,
        pos_tagger = pos_tagger
    )

    print(f'{lang} / {pos_tagger}:')
    print(tokens_tagged)
    print(f'{tokens_tagged_universal}\n')

    # Check for empty tags
    assert tokens_tagged
    assert tokens_tagged_universal
    assert tokens_tagged_tokenized
    assert tokens_tagged_universal_tokenized
    assert all((tag for token, tag in tokens_tagged))
    assert all((tag for token, tag in tokens_tagged_universal))
    assert all((tag for token, tag in tokens_tagged_tokenized))
    assert all((tag for token, tag in tokens_tagged_universal_tokenized))
    # Universal tags should not all be "X"
    assert any((tag for token, tag in tokens_tagged_universal if tag != 'X'))
    assert any((tag for token, tag in tokens_tagged_universal_tokenized if tag != 'X'))

    # Tokenization should not be modified
    assert len(tokens) == len(tokens_tagged_tokenized) == len(tokens_tagged_universal_tokenized)

    # Long texts
    assert [token[0] for token in tokens_tagged_tokenized_long] == [str(i) for i in range(101) for j in range(50)]

    tests_lang_util_skipped = False

    if lang == 'zho_cn':
        assert tokens_tagged == [('汉语', 'nz'), ('又称', 'n'), ('中文', 'nz'), ('、', 'x'), ('华语', 'nz'), ('[', 'x'), ('6', 'x'), (']', 'x'), ('、', 'x'), ('唐', 'nr'), ('话', 'n'), ('[', 'x'), ('7', 'x'), (']', 'x'), ('，', 'x'), ('概指', 'n'), ('由', 'p'), ('上', 'f'), ('古汉语', 'nr'), ('（', 'x'), ('先秦', 't'), ('雅言', 'nr'), ('）', 'x'), ('发展', 'vn'), ('而', 'c'), ('来', 'v'), ('、', 'x'), ('书面', 'n'), ('使用', 'v'), ('汉字', 'nz'), ('的', 'uj'), ('分析语', 'n'), ('，', 'x'), ('为', 'p'), ('汉藏语系', 'nz'), ('最大', 'a'), ('的', 'uj'), ('一支', 'm'), ('语族', 'n'), ('。', 'x')]
        assert tokens_tagged_universal == [('汉语', 'PROPN'), ('又称', 'NOUN'), ('中文', 'PROPN'), ('、', 'PUNCT/SYM'), ('华语', 'PROPN'), ('[', 'PUNCT/SYM'), ('6', 'PUNCT/SYM'), (']', 'PUNCT/SYM'), ('、', 'PUNCT/SYM'), ('唐', 'PRONP'), ('话', 'NOUN'), ('[', 'PUNCT/SYM'), ('7', 'PUNCT/SYM'), (']', 'PUNCT/SYM'), ('，', 'PUNCT/SYM'), ('概指', 'NOUN'), ('由', 'ADP'), ('上', 'ADP'), ('古汉语', 'PRONP'), ('（', 'PUNCT/SYM'), ('先秦', 'NOUN'), ('雅言', 'PRONP'), ('）', 'PUNCT/SYM'), ('发展', 'VERB'), ('而', 'CONJ'), ('来', 'VERB'), ('、', 'PUNCT/SYM'), ('书面', 'NOUN'), ('使用', 'VERB'), ('汉字', 'PROPN'), ('的', 'PART'), ('分析语', 'NOUN'), ('，', 'PUNCT/SYM'), ('为', 'ADP'), ('汉藏语系', 'PROPN'), ('最大', 'ADJ'), ('的', 'PART'), ('一支', 'NUM'), ('语族', 'NOUN'), ('。', 'PUNCT/SYM')]
    elif lang == 'zho_tw':
        assert tokens_tagged == [('漢語', 'nz'), ('又', 'd'), ('稱', 'v'), ('中文', 'nz'), ('、', 'x'), ('華語', 'nz'), ('[', 'x'), ('6', 'x'), (']', 'x'), ('、', 'x'), ('唐', 'nr'), ('話', 'n'), ('[', 'x'), ('7', 'x'), (']', 'x'), ('，', 'x'), ('概指', 'n'), ('由', 'p'), ('上古', 'ns'), ('漢語', 'nz'), ('（', 'x'), ('先秦', 't'), ('雅言', 'nr'), ('）', 'x'), ('發展', 'vn'), ('而', 'c'), ('來', 'v'), ('、', 'x'), ('書面', 'n'), ('使用', 'v'), ('漢字', 'nz'), ('的', 'uj'), ('分析', 'vn'), ('語', 'x'), ('，', 'x'), ('為', 'p'), ('漢藏語', 'nz'), ('系', 'n'), ('最大', 'a'), ('的', 'uj'), ('一支', 'm'), ('語族', 'n'), ('。', 'x')]
        assert tokens_tagged_universal == [('漢語', 'PROPN'), ('又', 'ADV'), ('稱', 'VERB'), ('中文', 'PROPN'), ('、', 'PUNCT/SYM'), ('華語', 'PROPN'), ('[', 'PUNCT/SYM'), ('6', 'PUNCT/SYM'), (']', 'PUNCT/SYM'), ('、', 'PUNCT/SYM'), ('唐', 'PRONP'), ('話', 'NOUN'), ('[', 'PUNCT/SYM'), ('7', 'PUNCT/SYM'), (']', 'PUNCT/SYM'), ('，', 'PUNCT/SYM'), ('概指', 'NOUN'), ('由', 'ADP'), ('上古', 'PROPN'), ('漢語', 'PROPN'), ('（', 'PUNCT/SYM'), ('先秦', 'NOUN'), ('雅言', 'PRONP'), ('）', 'PUNCT/SYM'), ('發展', 'VERB'), ('而', 'CONJ'), ('來', 'VERB'), ('、', 'PUNCT/SYM'), ('書面', 'NOUN'), ('使用', 'VERB'), ('漢字', 'PROPN'), ('的', 'PART'), ('分析', 'VERB'), ('語', 'PUNCT/SYM'), ('，', 'PUNCT/SYM'), ('為', 'ADP'), ('漢藏語', 'PROPN'), ('系', 'NOUN'), ('最大', 'ADJ'), ('的', 'PART'), ('一支', 'NUM'), ('語族', 'NOUN'), ('。', 'PUNCT/SYM')]
    elif lang.startswith('eng_'):
        assert tokens_tagged == [('English', 'NNP'), ('is', 'VBZ'), ('a', 'DT'), ('West', 'NNP'), ('Germanic', 'NNP'), ('language', 'NN'), ('in', 'IN'), ('the', 'DT'), ('Indo-European', 'JJ'), ('language', 'NN'), ('family', 'NN'), ('that', 'WDT'), ('originated', 'VBD'), ('in', 'IN'), ('early', 'JJ'), ('medieval', 'NN'), ('England.', 'NNP'), ('[', 'VBZ'), ('3', 'CD'), (']', 'NN'), ('[', 'VBD'), ('4', 'CD'), (']', 'NNP'), ('[', 'VBD'), ('5', 'CD'), (']', 'NN')]
        assert tokens_tagged_universal == [('English', 'PROPN'), ('is', 'VERB'), ('a', 'DET'), ('West', 'PROPN'), ('Germanic', 'PROPN'), ('language', 'NOUN'), ('in', 'ADP/SCONJ'), ('the', 'DET'), ('Indo-European', 'ADJ'), ('language', 'NOUN'), ('family', 'NOUN'), ('that', 'DET'), ('originated', 'VERB'), ('in', 'ADP/SCONJ'), ('early', 'ADJ'), ('medieval', 'NOUN'), ('England.', 'PROPN'), ('[', 'VERB'), ('3', 'NUM'), (']', 'NOUN'), ('[', 'VERB'), ('4', 'NUM'), (']', 'PROPN'), ('[', 'VERB'), ('5', 'NUM'), (']', 'NOUN')]
    elif lang == 'jpn':
        assert tokens_tagged == [('日本語', '名詞-普通名詞-一般'), ('（', '補助記号-括弧開'), ('にほん', '名詞-固有名詞-地名-国'), ('ご', '接尾辞-名詞的-一般'), ('、', '補助記号-読点'), ('にっぽん', '名詞-固有名詞-地名-国'), ('ご', '接尾辞-名詞的-一般'), ('[', '補助記号-括弧開'), ('注釈', '名詞-普通名詞-サ変可能'), ('2', '名詞-数詞'), (']', '補助記号-括弧閉'), ('、', '補助記号-読点'), ('英語', '名詞-普通名詞-一般'), (':', '補助記号-一般'), ('Japanese', '名詞-普通名詞-一般'), ('language', '名詞-普通名詞-一般'), ('）', '補助記号-括弧閉'), ('は', '助詞-係助詞'), ('、', '補助記号-読点'), ('日本', '名詞-固有名詞-地名-国'), ('国', '接尾辞-名詞的-一般'), ('内', '接尾辞-名詞的-一般'), ('や', '助詞-副助詞'), ('、', '補助記号-読点'), ('かつて', '副詞'), ('の', '助詞-格助詞'), ('日本', '名詞-固有名詞-地名-国'), ('領', '接尾辞-名詞的-一般'), ('だっ', '助動詞'), ('た', '助動詞'), ('国', '名詞-普通名詞-一般'), ('、', '補助記号-読点'), ('そして', '接続詞'), ('国外', '名詞-普通名詞-一般'), ('移民', '名詞-普通名詞-サ変可能'), ('や', '助詞-副助詞'), ('移住者', '名詞-普通名詞-一般'), ('を', '助詞-格助詞'), ('含む', '動詞-一般'), ('日本人', '名詞-普通名詞-一般'), ('同士', '接尾辞-名詞的-一般'), ('の', '助詞-格助詞'), ('間', '名詞-普通名詞-副詞可能'), ('で', '助詞-格助詞'), ('使用', '名詞-普通名詞-サ変可能'), ('さ', '動詞-非自立可能'), ('れ', '助動詞'), ('て', '助詞-接続助詞'), ('いる', '動詞-非自立可能'), ('言語', '名詞-普通名詞-一般'), ('。', '補助記号-句点')]
        assert tokens_tagged_universal == [('日本語', 'NOUN'), ('（', 'PUNCT'), ('にほん', 'PROPN'), ('ご', 'NOUN'), ('、', 'PUNCT'), ('にっぽん', 'PROPN'), ('ご', 'NOUN'), ('[', 'PUNCT'), ('注釈', 'NOUN'), ('2', 'NUM'), (']', 'PUNCT'), ('、', 'PUNCT'), ('英語', 'NOUN'), (':', 'SYM'), ('Japanese', 'NOUN'), ('language', 'NOUN'), ('）', 'PUNCT'), ('は', 'ADP'), ('、', 'PUNCT'), ('日本', 'PROPN'), ('国', 'NOUN'), ('内', 'NOUN'), ('や', 'ADP'), ('、', 'PUNCT'), ('かつて', 'ADV'), ('の', 'ADP'), ('日本', 'PROPN'), ('領', 'NOUN'), ('だっ', 'AUX'), ('た', 'AUX'), ('国', 'NOUN'), ('、', 'PUNCT'), ('そして', 'CCONJ'), ('国外', 'NOUN'), ('移民', 'NOUN'), ('や', 'ADP'), ('移住者', 'NOUN'), ('を', 'ADP'), ('含む', 'VERB'), ('日本人', 'NOUN'), ('同士', 'NOUN'), ('の', 'ADP'), ('間', 'NOUN'), ('で', 'ADP'), ('使用', 'NOUN'), ('さ', 'AUX'), ('れ', 'AUX'), ('て', 'SCONJ'), ('いる', 'AUX'), ('言語', 'NOUN'), ('。', 'PUNCT')]
    elif lang == 'khm':
        assert tokens_tagged == [('ភាសា', 'n'), ('ខ្មែរ', 'n'), ('គឺជា', 'v'), ('ភាសា', 'n'), ('កំណើត', 'n'), ('របស់', 'o'), ('ជនជាតិ', 'n'), ('ខ្មែរ', 'n'), ('និង', 'o'), ('ជា', 'v'), ('ភាសា', 'n'), ('ផ្លូវការ', 'n'), ('របស់', 'o'), ('ប្រទេស', 'n'), ('កម្ពុជា', 'n'), ('។', '.')]
        assert tokens_tagged_universal == [('ភាសា', 'NOUN'), ('ខ្មែរ', 'NOUN'), ('គឺជា', 'VERB'), ('ភាសា', 'NOUN'), ('កំណើត', 'NOUN'), ('របស់', 'PART'), ('ជនជាតិ', 'NOUN'), ('ខ្មែរ', 'NOUN'), ('និង', 'PART'), ('ជា', 'VERB'), ('ភាសា', 'NOUN'), ('ផ្លូវការ', 'NOUN'), ('របស់', 'PART'), ('ប្រទេស', 'NOUN'), ('កម្ពុជា', 'NOUN'), ('។', 'PUNCT')]
    # To be tested when spaCy 4.0 is released
    elif lang == 'kor':
        assert tokens_tagged == []
        assert tokens_tagged_universal == []
    elif lang == 'rus':
        if pos_tagger == 'nltk_perceptron_rus':
            assert tokens_tagged == [('Ру́сский', 'A=m'), ('язы́к', 'S'), ('(', 'NONLEX'), ('[', 'NONLEX'), ('ˈruskʲɪi̯', 'NONLEX'), ('jɪˈzɨk', 'NONLEX'), (']', 'NONLEX'), ('Информация', 'S'), ('о', 'PR'), ('файле', 'S'), ('слушать', 'V'), (')', 'NONLEX'), ('[', 'NONLEX'), ('~', 'NONLEX'), ('3', 'NUM=ciph'), (']', 'NONLEX'), ('[', 'NONLEX'), ('⇨', 'NONLEX'), (']', 'NONLEX'), ('—', 'NONLEX'), ('язык', 'S'), ('восточнославянской', 'A=f'), ('группы', 'S'), ('славянской', 'A=f'), ('ветви', 'S'), ('индоевропейской', 'A=f'), ('языковой', 'A=f'), ('семьи', 'S'), (',', 'NONLEX'), ('национальный', 'A=m'), ('язык', 'S'), ('русского', 'A=m'), ('народа', 'S'), ('.', 'NONLEX')]
            assert tokens_tagged_universal == [('Ру́сский', 'ADJ'), ('язы́к', 'NOUN'), ('(', 'PUNCT/SYM'), ('[', 'PUNCT/SYM'), ('ˈruskʲɪi̯', 'PUNCT/SYM'), ('jɪˈzɨk', 'PUNCT/SYM'), (']', 'PUNCT/SYM'), ('Информация', 'NOUN'), ('о', 'ADP'), ('файле', 'NOUN'), ('слушать', 'VERB'), (')', 'PUNCT/SYM'), ('[', 'PUNCT/SYM'), ('~', 'PUNCT/SYM'), ('3', 'NUM'), (']', 'PUNCT/SYM'), ('[', 'PUNCT/SYM'), ('⇨', 'PUNCT/SYM'), (']', 'PUNCT/SYM'), ('—', 'PUNCT/SYM'), ('язык', 'NOUN'), ('восточнославянской', 'ADJ'), ('группы', 'NOUN'), ('славянской', 'ADJ'), ('ветви', 'NOUN'), ('индоевропейской', 'ADJ'), ('языковой', 'ADJ'), ('семьи', 'NOUN'), (',', 'PUNCT/SYM'), ('национальный', 'ADJ'), ('язык', 'NOUN'), ('русского', 'ADJ'), ('народа', 'NOUN'), ('.', 'PUNCT/SYM')]
        elif pos_tagger == 'pymorphy3_morphological_analyzer':
            assert tokens_tagged == [('Ру́сский', 'NOUN'), ('язы́к', 'NOUN'), ('(', 'PNCT'), ('[', 'PNCT'), ('ˈruskʲɪi̯', 'UNKN'), ('jɪˈzɨk', 'UNKN'), (']', 'PNCT'), ('Информация', 'NOUN'), ('о', 'PREP'), ('файле', 'NOUN'), ('слушать', 'INFN'), (')', 'PNCT'), ('[', 'PNCT'), ('~', 'UNKN'), ('3', 'NUMB'), (']', 'PNCT'), ('[', 'PNCT'), ('⇨', 'UNKN'), (']', 'PNCT'), ('—', 'PNCT'), ('язык', 'NOUN'), ('восточнославянской', 'ADJF'), ('группы', 'NOUN'), ('славянской', 'ADJF'), ('ветви', 'NOUN'), ('индоевропейской', 'ADJF'), ('языковой', 'ADJF'), ('семьи', 'NOUN'), (',', 'PNCT'), ('национальный', 'ADJF'), ('язык', 'NOUN'), ('русского', 'ADJF'), ('народа', 'NOUN'), ('.', 'PNCT')]
            assert tokens_tagged_universal == [('Ру́сский', 'NOUN'), ('язы́к', 'NOUN'), ('(', 'PUNCT'), ('[', 'PUNCT'), ('ˈruskʲɪi̯', 'SYM/X'), ('jɪˈzɨk', 'SYM/X'), (']', 'PUNCT'), ('Информация', 'NOUN'), ('о', 'ADP'), ('файле', 'NOUN'), ('слушать', 'VERB'), (')', 'PUNCT'), ('[', 'PUNCT'), ('~', 'SYM/X'), ('3', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('⇨', 'SYM/X'), (']', 'PUNCT'), ('—', 'PUNCT'), ('язык', 'NOUN'), ('восточнославянской', 'ADJ'), ('группы', 'NOUN'), ('славянской', 'ADJ'), ('ветви', 'NOUN'), ('индоевропейской', 'ADJ'), ('языковой', 'ADJ'), ('семьи', 'NOUN'), (',', 'PUNCT'), ('национальный', 'ADJ'), ('язык', 'NOUN'), ('русского', 'ADJ'), ('народа', 'NOUN'), ('.', 'PUNCT')]
        else:
            tests_lang_util_skipped = True
    elif lang == 'tha':
        if pos_tagger == 'pythainlp_perceptron_blackboard':
            assert tokens_tagged == [('ภาษาไทย', 'NN'), ('หรือ', 'CC'), ('ภาษาไทย', 'NN'), ('กลาง', 'NN'), ('เป็น', 'VV'), ('ภาษา', 'NN'), ('ใน', 'PS'), ('กลุ่ม', 'NN'), ('ภาษา', 'NN'), ('ไท', 'NN'), ('ซึ่ง', 'CC'), ('เป็น', 'VV'), ('กลุ่มย่อย', 'NN'), ('ของ', 'PS'), ('ตระกูล', 'NN'), ('ภาษา', 'NN'), ('ข', 'NN'), ('ร้า', 'NN'), ('-', 'PU'), ('ไท', 'NN'), ('และ', 'CC'), ('เป็น', 'VV'), ('ภาษาราชการ', 'NN'), ('และ', 'CC'), ('ภาษาประจำชาติ', 'NN'), ('ของ', 'PS'), ('ประเทศ', 'NN'), ('ไทย', 'NN'), ('[', 'NN'), ('3', 'NU'), ('][', 'CL'), ('4', 'NU'), (']', 'CL')]
            assert tokens_tagged_universal == [('ภาษาไทย', 'NOUN'), ('หรือ', 'CCONJ'), ('ภาษาไทย', 'NOUN'), ('กลาง', 'NOUN'), ('เป็น', 'VERB'), ('ภาษา', 'NOUN'), ('ใน', 'ADP'), ('กลุ่ม', 'NOUN'), ('ภาษา', 'NOUN'), ('ไท', 'NOUN'), ('ซึ่ง', 'CCONJ'), ('เป็น', 'VERB'), ('กลุ่มย่อย', 'NOUN'), ('ของ', 'ADP'), ('ตระกูล', 'NOUN'), ('ภาษา', 'NOUN'), ('ข', 'NOUN'), ('ร้า', 'NOUN'), ('-', 'PUNCT'), ('ไท', 'NOUN'), ('และ', 'CCONJ'), ('เป็น', 'VERB'), ('ภาษาราชการ', 'NOUN'), ('และ', 'CCONJ'), ('ภาษาประจำชาติ', 'NOUN'), ('ของ', 'ADP'), ('ประเทศ', 'NOUN'), ('ไทย', 'NOUN'), ('[', 'NOUN'), ('3', 'NUM'), ('][', 'NOUN'), ('4', 'NUM'), (']', 'NOUN')]
        elif pos_tagger == 'pythainlp_perceptron_orchid':
            assert tokens_tagged == [('ภาษาไทย', 'NPRP'), ('หรือ', 'JCRG'), ('ภาษาไทย', 'NPRP'), ('กลาง', 'VATT'), ('เป็น', 'VSTA'), ('ภาษา', 'NCMN'), ('ใน', 'RPRE'), ('กลุ่ม', 'NCMN'), ('ภาษา', 'NCMN'), ('ไท', 'NCMN'), ('ซึ่ง', 'PREL'), ('เป็น', 'VSTA'), ('กลุ่มย่อย', 'NCMN'), ('ของ', 'RPRE'), ('ตระกูล', 'NCMN'), ('ภาษา', 'NCMN'), ('ข', 'NCMN'), ('ร้า', 'NCMN'), ('-', 'PUNC'), ('ไท', 'NCMN'), ('และ', 'JCRG'), ('เป็น', 'VSTA'), ('ภาษาราชการ', 'NCMN'), ('และ', 'JCRG'), ('ภาษาประจำชาติ', 'NCMN'), ('ของ', 'RPRE'), ('ประเทศ', 'NCMN'), ('ไทย', 'NPRP'), ('[', 'NCMN'), ('3', 'NCNM'), ('][', 'PUNC'), ('4', 'NCNM'), (']', 'CMTR')]
            assert tokens_tagged_universal == [('ภาษาไทย', 'PROPN'), ('หรือ', 'CCONJ'), ('ภาษาไทย', 'PROPN'), ('กลาง', 'ADJ'), ('เป็น', 'VERB'), ('ภาษา', 'NOUN'), ('ใน', 'ADP'), ('กลุ่ม', 'NOUN'), ('ภาษา', 'NOUN'), ('ไท', 'NOUN'), ('ซึ่ง', 'SCONJ'), ('เป็น', 'VERB'), ('กลุ่มย่อย', 'NOUN'), ('ของ', 'ADP'), ('ตระกูล', 'NOUN'), ('ภาษา', 'NOUN'), ('ข', 'NOUN'), ('ร้า', 'NOUN'), ('-', 'PUNCT'), ('ไท', 'NOUN'), ('และ', 'CCONJ'), ('เป็น', 'VERB'), ('ภาษาราชการ', 'NOUN'), ('และ', 'CCONJ'), ('ภาษาประจำชาติ', 'NOUN'), ('ของ', 'ADP'), ('ประเทศ', 'NOUN'), ('ไทย', 'PROPN'), ('[', 'NOUN'), ('3', 'NOUN/NUM'), ('][', 'PUNCT'), ('4', 'NOUN/NUM'), (']', 'NOUN')]
        elif pos_tagger == 'pythainlp_perceptron_pud':
            assert tokens_tagged == tokens_tagged_universal == [('ภาษาไทย', 'NOUN'), ('หรือ', 'CCONJ'), ('ภาษาไทย', 'NOUN'), ('กลาง', 'NOUN'), ('เป็น', 'AUX'), ('ภาษา', 'NOUN'), ('ใน', 'ADP'), ('กลุ่ม', 'NOUN'), ('ภาษา', 'NOUN'), ('ไท', 'PROPN'), ('ซึ่ง', 'DET'), ('เป็น', 'AUX'), ('กลุ่มย่อย', 'NOUN'), ('ของ', 'ADP'), ('ตระกูล', 'NOUN'), ('ภาษา', 'NOUN'), ('ข', 'NOUN'), ('ร้า', 'NOUN'), ('-', 'PUNCT'), ('ไท', 'PROPN'), ('และ', 'CCONJ'), ('เป็น', 'AUX'), ('ภาษาราชการ', 'NOUN'), ('และ', 'CCONJ'), ('ภาษาประจำชาติ', 'NOUN'), ('ของ', 'ADP'), ('ประเทศ', 'NOUN'), ('ไทย', 'PROPN'), ('[', 'NOUN'), ('3', 'NUM'), ('][', 'NOUN'), ('4', 'NUM'), (']', 'NOUN')]
        else:
            tests_lang_util_skipped = True
    elif lang == 'bod':
        assert tokens_tagged == [('བོད་', 'PROPN'), ('ཀྱི་', 'PART'), ('སྐད་ཡིག་', 'NOUN'), ('ནི་', 'NO_POS'), ('བོད་ཡུལ་', 'PROPN'), ('དང་', 'NO_POS'), ('ཉེ་འཁོར་', 'NOUN'), ('གྱི་', 'PART'), ('ས་ཁུལ་', 'OTHER'), ('བལ་ཡུལ', 'PROPN'), ('།', 'PUNCT'), ('འབྲུག་', 'NOUN'), ('དང་', 'NO_POS'), ('འབྲས་ལྗོངས', 'OTHER'), ('།', 'PUNCT')]
        assert tokens_tagged_universal == [('བོད་', 'PROPN'), ('ཀྱི་', 'PART'), ('སྐད་ཡིག་', 'NOUN'), ('ནི་', 'X'), ('བོད་ཡུལ་', 'PROPN'), ('དང་', 'X'), ('ཉེ་འཁོར་', 'NOUN'), ('གྱི་', 'PART'), ('ས་ཁུལ་', 'X'), ('བལ་ཡུལ', 'PROPN'), ('།', 'PUNCT'), ('འབྲུག་', 'NOUN'), ('དང་', 'X'), ('འབྲས་ལྗོངས', 'X'), ('།', 'PUNCT')]
    elif lang == 'ukr':
        assert tokens_tagged == [('Украї́нська', 'ADJF'), ('мо́ва', 'ADJF'), ('(', 'PNCT'), ('МФА', 'UNKN'), (':', 'PNCT'), ('[', 'PNCT'), ('ukrɑ̽ˈjɪnʲsʲkɑ̽', 'UNKN'), ('ˈmɔwɑ̽', 'UNKN'), (']', 'PNCT'), (',', 'PNCT'), ('історичні', 'ADJF'), ('назви', 'NOUN'), ('—', 'PNCT'), ('ру́ська', 'ADJF'), ('[', 'PNCT'), ('10', 'NUMB'), (']', 'PNCT'), ('[', 'PNCT'), ('11', 'NUMB'), (']', 'PNCT'), ('[', 'PNCT'), ('12', 'NUMB'), (']', 'PNCT'), ('[', 'PNCT'), ('*', 'PNCT'), ('1', 'NUMB'), (']', 'PNCT'), (')', 'PNCT'), ('—', 'PNCT'), ('національна', 'ADJF'), ('мова', 'NOUN'), ('українців', 'NOUN'), ('.', 'PNCT')]
        assert tokens_tagged_universal == [('Украї́нська', 'ADJ'), ('мо́ва', 'ADJ'), ('(', 'PUNCT'), ('МФА', 'SYM/X'), (':', 'PUNCT'), ('[', 'PUNCT'), ('ukrɑ̽ˈjɪnʲsʲkɑ̽', 'SYM/X'), ('ˈmɔwɑ̽', 'SYM/X'), (']', 'PUNCT'), (',', 'PUNCT'), ('історичні', 'ADJ'), ('назви', 'NOUN'), ('—', 'PUNCT'), ('ру́ська', 'ADJ'), ('[', 'PUNCT'), ('10', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('11', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('12', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('*', 'PUNCT'), ('1', 'NUM'), (']', 'PUNCT'), (')', 'PUNCT'), ('—', 'PUNCT'), ('національна', 'ADJ'), ('мова', 'NOUN'), ('українців', 'NOUN'), ('.', 'PUNCT')]
    elif lang == 'vie':
        assert tokens_tagged == [('Tiếng', 'N'), ('Việt', 'Np'), (',', 'CH'), ('cũng', 'R'), ('gọi là', 'X'), ('tiếng', 'N'), ('Việt Nam', 'Np'), ('[', 'V'), ('9', 'M'), (']', 'CH'), ('hay', 'C'), ('Việt ngữ', 'V'), ('là', 'V'), ('ngôn ngữ', 'N'), ('của', 'E'), ('người', 'Nc'), ('Việt', 'Np'), ('và', 'C'), ('là', 'V'), ('ngôn ngữ', 'N'), ('chính thức', 'A'), ('tại', 'E'), ('Việt Nam', 'Np'), ('.', 'CH')]
        assert tokens_tagged_universal == [('Tiếng', 'NOUN'), ('Việt', 'PROPN'), (',', 'PUNCT'), ('cũng', 'X'), ('gọi là', 'X'), ('tiếng', 'NOUN'), ('Việt Nam', 'PROPN'), ('[', 'VERB'), ('9', 'NUM'), (']', 'PUNCT'), ('hay', 'CCONJ'), ('Việt ngữ', 'VERB'), ('là', 'VERB'), ('ngôn ngữ', 'NOUN'), ('của', 'ADP'), ('người', 'NOUN'), ('Việt', 'PROPN'), ('và', 'CCONJ'), ('là', 'VERB'), ('ngôn ngữ', 'NOUN'), ('chính thức', 'ADJ'), ('tại', 'ADP'), ('Việt Nam', 'PROPN'), ('.', 'PUNCT')]
    else:
        raise wl_test_init.Wl_Exception_Tests_Lang_Skipped(lang)

    if tests_lang_util_skipped:
        raise wl_test_init.Wl_Exception_Tests_Lang_Util_Skipped(pos_tagger)

if __name__ == '__main__':
    for lang, pos_tagger in test_pos_taggers:
        test_pos_tag(lang, pos_tagger)
