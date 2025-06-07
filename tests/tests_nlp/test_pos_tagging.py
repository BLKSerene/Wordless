# ----------------------------------------------------------------------
# Tests: NLP - POS tagging
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

import pytest

from tests import (
    wl_test_init,
    wl_test_lang_examples
)
from wordless.wl_nlp import (
    wl_pos_tagging,
    wl_texts,
    wl_word_tokenization
)
from wordless.wl_utils import wl_misc

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')
is_linux = wl_misc.check_os()[2]

test_pos_taggers = []
test_pos_taggers_local = []

for lang, pos_taggers in main.settings_global['pos_taggers'].items():
    for pos_tagger in pos_taggers:
        if pos_tagger in ('botok_xct', 'modern_botok_bod'):
            test_pos_taggers.append(pytest.param(
                lang, pos_tagger,
                marks = pytest.mark.xfail(
                    is_linux,
                    reason = 'Different results on AppVeyor, Azure Pipelines, and GitHub Actions'
                )
            ))

            test_pos_taggers_local.append((lang, pos_tagger))
        elif not pos_tagger.startswith(('spacy_', 'stanza_')):
            test_pos_taggers.append((lang, pos_tagger))
            test_pos_taggers_local.append((lang, pos_tagger))

def test_to_content_function():
    assert wl_pos_tagging.to_content_function('ADJ') == 'Content words'
    assert wl_pos_tagging.to_content_function('ADP') == 'Function words'
    assert wl_pos_tagging.to_content_function('None') is None

@pytest.mark.parametrize('lang, pos_tagger', test_pos_taggers)
def test_pos_tag(lang, pos_tagger):
    tests_lang_util_skipped = False
    test_sentence = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}')

    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = test_sentence,
        lang = lang
    )

    match lang:
        case 'eng_gb' | 'eng_us':
            results = [('English', 'NNP'), ('is', 'VBZ'), ('a', 'DT'), ('West', 'NNP'), ('Germanic', 'NNP'), ('language', 'NN'), ('in', 'IN'), ('the', 'DT'), ('Indo-European', 'JJ'), ('language', 'NN'), ('family', 'NN'), (',', ','), ('whose', 'WP$'), ('speakers', 'NNS'), (',', ','), ('called', 'VBN'), ('Anglophones', 'NNS'), (',', ','), ('originated', 'VBN'), ('in', 'IN'), ('early', 'JJ'), ('medieval', 'NN'), ('England', 'NNP'), ('on', 'IN'), ('the', 'DT'), ('island', 'NN'), ('of', 'IN'), ('Great', 'NNP'), ('Britain.', 'NNP'), ('[', 'NNP'), ('4', 'CD'), (']', 'NNP'), ('[', 'VBD'), ('5', 'CD'), (']', 'NNP'), ('[', 'VBD'), ('6', 'CD'), (']', 'NN')]
            results_universal = [('English', 'PROPN'), ('is', 'VERB'), ('a', 'DET'), ('West', 'PROPN'), ('Germanic', 'PROPN'), ('language', 'NOUN'), ('in', 'ADP/SCONJ'), ('the', 'DET'), ('Indo-European', 'ADJ'), ('language', 'NOUN'), ('family', 'NOUN'), (',', 'PUNCT'), ('whose', 'PRON'), ('speakers', 'NOUN'), (',', 'PUNCT'), ('called', 'VERB'), ('Anglophones', 'NOUN'), (',', 'PUNCT'), ('originated', 'VERB'), ('in', 'ADP/SCONJ'), ('early', 'ADJ'), ('medieval', 'NOUN'), ('England', 'PROPN'), ('on', 'ADP/SCONJ'), ('the', 'DET'), ('island', 'NOUN'), ('of', 'ADP/SCONJ'), ('Great', 'PROPN'), ('Britain.', 'PROPN'), ('[', 'PROPN'), ('4', 'NUM'), (']', 'PROPN'), ('[', 'VERB'), ('5', 'NUM'), (']', 'PROPN'), ('[', 'VERB'), ('6', 'NUM'), (']', 'NOUN')]
        case 'jpn':
            results = [('日本語', '名詞-普通名詞-一般'), ('（', '補助記号-括弧開'), ('にほん', '名詞-固有名詞-地名-国'), ('ご', '接尾辞-名詞的-一般'), ('、', '補助記号-読点'), ('にっぽん', '名詞-固有名詞-地名-国'), ('ご', '接尾辞-名詞的-一般'), ('[', '補助記号-括弧開'), ('注釈', '名詞-普通名詞-サ変可能'), ('3', '名詞-数詞'), (']', '補助記号-括弧閉'), ('）', '補助記号-括弧閉'), ('は', '助詞-係助詞'), ('、', '補助記号-読点'), ('日本', '名詞-固有名詞-地名-国'), ('国', '接尾辞-名詞的-一般'), ('内', '接尾辞-名詞的-一般'), ('や', '助詞-副助詞'), ('、', '補助記号-読点'), ('かつて', '副詞'), ('の', '助詞-格助詞'), ('日本', '名詞-固有名詞-地名-国'), ('領', '接尾辞-名詞的-一般'), ('だっ', '助動詞'), ('た', '助動詞'), ('国', '名詞-普通名詞-一般'), ('、', '補助記号-読点'), ('そして', '接続詞'), ('国外', '名詞-普通名詞-一般'), ('移民', '名詞-普通名詞-サ変可能'), ('や', '助詞-副助詞'), ('移住者', '名詞-普通名詞-一般'), ('を', '助詞-格助詞'), ('含む', '動詞-一般'), ('日本人', '名詞-普通名詞-一般'), ('同士', '接尾辞-名詞的-一般'), ('の', '助詞-格助詞'), ('間', '名詞-普通名詞-副詞可能'), ('で', '助詞-格助詞'), ('使用', '名詞-普通名詞-サ変可能'), ('さ', '動詞-非自立可能'), ('れ', '助動詞'), ('て', '助詞-接続助詞'), ('いる', '動詞-非自立可能'), ('言語', '名詞-普通名詞-一般'), ('。', '補助記号-句点')]
            results_universal = [('日本語', 'NOUN'), ('（', 'PUNCT'), ('にほん', 'PROPN'), ('ご', 'NOUN'), ('、', 'PUNCT'), ('にっぽん', 'PROPN'), ('ご', 'NOUN'), ('[', 'PUNCT'), ('注釈', 'NOUN'), ('3', 'NUM'), (']', 'PUNCT'), ('）', 'PUNCT'), ('は', 'ADP'), ('、', 'PUNCT'), ('日本', 'PROPN'), ('国', 'NOUN'), ('内', 'NOUN'), ('や', 'ADP'), ('、', 'PUNCT'), ('かつて', 'ADV'), ('の', 'ADP'), ('日本', 'PROPN'), ('領', 'NOUN'), ('だっ', 'AUX'), ('た', 'AUX'), ('国', 'NOUN'), ('、', 'PUNCT'), ('そして', 'CCONJ'), ('国外', 'NOUN'), ('移民', 'NOUN'), ('や', 'ADP'), ('移住者', 'NOUN'), ('を', 'ADP'), ('含む', 'VERB'), ('日本人', 'NOUN'), ('同士', 'NOUN'), ('の', 'ADP'), ('間', 'NOUN'), ('で', 'ADP'), ('使用', 'NOUN'), ('さ', 'AUX'), ('れ', 'AUX'), ('て', 'SCONJ'), ('いる', 'AUX'), ('言語', 'NOUN'), ('。', 'PUNCT')]
        case 'khm':
            results = [('ភាសា', 'n'), ('ខ្មែរ', 'n'), ('គឺជា', 'v'), ('ភាសា', 'n'), ('កំណើត', 'n'), ('របស់', 'o'), ('ជនជាតិ', 'n'), ('ខ្មែរ', 'n'), ('និង', 'o'), ('ជា', 'v'), ('ភាសា', 'n'), ('ផ្លូវការ', 'n'), ('របស់', 'o'), ('ប្រទេស', 'n'), ('កម្ពុជា', 'n'), ('។', '.')]
            results_universal = [('ភាសា', 'NOUN'), ('ខ្មែរ', 'NOUN'), ('គឺជា', 'VERB'), ('ភាសា', 'NOUN'), ('កំណើត', 'NOUN'), ('របស់', 'PART'), ('ជនជាតិ', 'NOUN'), ('ខ្មែរ', 'NOUN'), ('និង', 'PART'), ('ជា', 'VERB'), ('ភាសា', 'NOUN'), ('ផ្លូវការ', 'NOUN'), ('របស់', 'PART'), ('ប្រទេស', 'NOUN'), ('កម្ពុជា', 'NOUN'), ('។', 'PUNCT')]
        case 'kor':
            results = [('한국어', 'NNG'), ('(', 'SSO'), ('韓', 'NNG'), ('國語', 'NNG'), (')', 'SSC'), (',', 'SC'), ('조선어', 'NNG'), ('(', 'SSO'), ('朝鮮', 'NNG'), ('語', 'XSN'), (')', 'SSC'), ('는', 'JX'), ('대한민국', 'NNP'), ('과', 'JC'), ('조선', 'NNP'), ('민주주의', 'NNG'), ('인민공화국', 'NNP'), ('의', 'JKG'), ('공용어', 'NNG'), ('이', 'VCP'), ('다', 'EF'), ('.', 'SF')]
            results_universal = [('한국어', 'NOUN'), ('(', 'PUNCT'), ('韓', 'NOUN'), ('國語', 'NOUN'), (')', 'PUNCT'), (',', 'PUNCT'), ('조선어', 'NOUN'), ('(', 'PUNCT'), ('朝鮮', 'NOUN'), ('語', 'X'), (')', 'PUNCT'), ('는', 'ADP'), ('대한민국', 'PROPN'), ('과', 'CONJ'), ('조선', 'PROPN'), ('민주주의', 'NOUN'), ('인민공화국', 'PROPN'), ('의', 'ADP'), ('공용어', 'NOUN'), ('이', 'ADP'), ('다', 'X'), ('.', 'PUNCT')]
        case 'lao':
            match pos_tagger:
                case 'laonlp_seqlabeling':
                    results = [('ພາສາລາວ', 'N'), ('ສືບທອດ', 'N'), ('ມາຈາກ', 'PRE'), ('ພາສາ', 'N'), ('ຕະກຸນ', 'N'), ('ໄຕ', 'N'), ('-', 'PUNCT'), ('ກະໄດ', 'N'), ('ຢູ່', 'PRE'), ('ພາກ', 'N'), ('ໃຕ້', 'N'), ('ຂອງ', 'PRE'), ('ປະເທດຈີນ', 'N'), ('ເຊິ່ງ', 'REL'), ('ເປັນ', 'V'), ('ຈຸດ', 'N'), ('ເດີມ', 'ADJ'), ('ຂອງ', 'PRE'), ('ຫຼາຍ', 'ADJ'), ('ພາສາ', 'N'), ('ໃນ', 'PRE'), ('ຕະກຸນ', 'N'), ('ນີ້', 'DMN'), ('ທີ່', 'REL'), ('ຍັງ', 'ADV'), ('ຖືກ', 'PRA'), ('ໃຊ້', 'V'), ('ແລະ', 'COJ'), ('ຖືກ', 'PRA'), ('ເວົ້າ', 'V'), ('ຢູ່', 'ADV'), ('ໂດຍ', 'PRE'), ('ຫຼາຍ', 'ADJ'), ('ຊົນເຜົ່າ', 'N'), ('ໃນ', 'PRE'), ('ປັດຈຸບັນ', 'ADJ'), ('.', 'PUNCT')]
                    results_universal = [('ພາສາລາວ', 'NOUN'), ('ສືບທອດ', 'NOUN'), ('ມາຈາກ', 'ADP'), ('ພາສາ', 'NOUN'), ('ຕະກຸນ', 'NOUN'), ('ໄຕ', 'NOUN'), ('-', 'PUNCT'), ('ກະໄດ', 'NOUN'), ('ຢູ່', 'ADP'), ('ພາກ', 'NOUN'), ('ໃຕ້', 'NOUN'), ('ຂອງ', 'ADP'), ('ປະເທດຈີນ', 'NOUN'), ('ເຊິ່ງ', 'PRON'), ('ເປັນ', 'VERB'), ('ຈຸດ', 'NOUN'), ('ເດີມ', 'ADJ'), ('ຂອງ', 'ADP'), ('ຫຼາຍ', 'ADJ'), ('ພາສາ', 'NOUN'), ('ໃນ', 'ADP'), ('ຕະກຸນ', 'NOUN'), ('ນີ້', 'PRON'), ('ທີ່', 'PRON'), ('ຍັງ', 'ADV'), ('ຖືກ', 'AUX'), ('ໃຊ້', 'VERB'), ('ແລະ', 'CONJ'), ('ຖືກ', 'AUX'), ('ເວົ້າ', 'VERB'), ('ຢູ່', 'ADV'), ('ໂດຍ', 'ADP'), ('ຫຼາຍ', 'ADJ'), ('ຊົນເຜົ່າ', 'NOUN'), ('ໃນ', 'ADP'), ('ປັດຈຸບັນ', 'ADJ'), ('.', 'PUNCT')]
                case 'laonlp_yunshan_cup_2020':
                    results = [('ພາສາລາວ', 'N'), ('ສືບທອດ', 'N'), ('ມາຈາກ', 'PRE'), ('ພາສາ', 'N'), ('ຕະກຸນ', 'N'), ('ໄຕ', 'N'), ('-', 'PUNCT'), ('ກະໄດ', 'N'), ('ຢູ່', 'PRE'), ('ພາກ', 'N'), ('ໃຕ້', 'PRE'), ('ຂອງ', 'PRE'), ('ປະເທດຈີນ', 'N'), ('ເຊິ່ງ', 'REL'), ('ເປັນ', 'V'), ('ຈຸດ', 'N'), ('ເດີມ', 'ADJ'), ('ຂອງ', 'PRE'), ('ຫຼາຍ', 'ADJ'), ('ພາສາ', 'N'), ('ໃນ', 'PRE'), ('ຕະກຸນ', 'N'), ('ນີ້', 'DMN'), ('ທີ່', 'REL'), ('ຍັງ', 'ADV'), ('ຖືກ', 'PRA'), ('ໃຊ້', 'V'), ('ແລະ', 'COJ'), ('ຖືກ', 'PRA'), ('ເວົ້າ', 'V'), ('ຢູ່', 'ADV'), ('ໂດຍ', 'PRE'), ('ຫຼາຍ', 'CLF'), ('ຊົນເຜົ່າ', 'N'), ('ໃນ', 'PRE'), ('ປັດຈຸບັນ', 'ADJ'), ('.', 'PUNCT')]
                    results_universal = [('ພາສາລາວ', 'NOUN'), ('ສືບທອດ', 'NOUN'), ('ມາຈາກ', 'ADP'), ('ພາສາ', 'NOUN'), ('ຕະກຸນ', 'NOUN'), ('ໄຕ', 'NOUN'), ('-', 'PUNCT'), ('ກະໄດ', 'NOUN'), ('ຢູ່', 'ADP'), ('ພາກ', 'NOUN'), ('ໃຕ້', 'ADP'), ('ຂອງ', 'ADP'), ('ປະເທດຈີນ', 'NOUN'), ('ເຊິ່ງ', 'PRON'), ('ເປັນ', 'VERB'), ('ຈຸດ', 'NOUN'), ('ເດີມ', 'ADJ'), ('ຂອງ', 'ADP'), ('ຫຼາຍ', 'ADJ'), ('ພາສາ', 'NOUN'), ('ໃນ', 'ADP'), ('ຕະກຸນ', 'NOUN'), ('ນີ້', 'PRON'), ('ທີ່', 'PRON'), ('ຍັງ', 'ADV'), ('ຖືກ', 'AUX'), ('ໃຊ້', 'VERB'), ('ແລະ', 'CONJ'), ('ຖືກ', 'AUX'), ('ເວົ້າ', 'VERB'), ('ຢູ່', 'ADV'), ('ໂດຍ', 'ADP'), ('ຫຼາຍ', 'PART'), ('ຊົນເຜົ່າ', 'NOUN'), ('ໃນ', 'ADP'), ('ປັດຈຸບັນ', 'ADJ'), ('.', 'PUNCT')]
                case _:
                    tests_lang_util_skipped = True
        case 'rus':
            match pos_tagger:
                case 'nltk_perceptron_rus':
                    results = [('Русский', 'A=m'), ('язык', 'S'), ('(', 'NONLEX'), ('МФА', 'S'), (':', 'NONLEX'), ('[', 'NONLEX'), ('ˈruskʲɪɪ̯', 'NONLEX'), ('ɪ̯ɪˈzɨk', 'NONLEX'), (']', 'NONLEX'), ('о', 'PR'), ('файле', 'S'), (')', 'NONLEX'), ('[', 'NONLEX'), ('~', 'NONLEX'), ('3', 'NUM=ciph'), (']', 'NONLEX'), ('—', 'NONLEX'), ('язык', 'S'), ('восточнославянской', 'A=f'), ('группы', 'S'), ('славянской', 'A=f'), ('ветви', 'S'), ('индоевропейской', 'A=f'), ('языковой', 'A=f'), ('семьи', 'S'), (',', 'NONLEX'), ('национальный', 'A=m'), ('язык', 'S'), ('русского', 'A=m'), ('народа', 'S'), ('.', 'NONLEX')]
                    results_universal = [('Русский', 'ADJ'), ('язык', 'NOUN'), ('(', 'PUNCT/SYM'), ('МФА', 'NOUN'), (':', 'PUNCT/SYM'), ('[', 'PUNCT/SYM'), ('ˈruskʲɪɪ̯', 'PUNCT/SYM'), ('ɪ̯ɪˈzɨk', 'PUNCT/SYM'), (']', 'PUNCT/SYM'), ('о', 'ADP'), ('файле', 'NOUN'), (')', 'PUNCT/SYM'), ('[', 'PUNCT/SYM'), ('~', 'PUNCT/SYM'), ('3', 'NUM'), (']', 'PUNCT/SYM'), ('—', 'PUNCT/SYM'), ('язык', 'NOUN'), ('восточнославянской', 'ADJ'), ('группы', 'NOUN'), ('славянской', 'ADJ'), ('ветви', 'NOUN'), ('индоевропейской', 'ADJ'), ('языковой', 'ADJ'), ('семьи', 'NOUN'), (',', 'PUNCT/SYM'), ('национальный', 'ADJ'), ('язык', 'NOUN'), ('русского', 'ADJ'), ('народа', 'NOUN'), ('.', 'PUNCT/SYM')]
                case 'pymorphy3_morphological_analyzer':
                    results = [('Русский', 'ADJF'), ('язык', 'NOUN'), ('(', 'PNCT'), ('МФА', 'UNKN'), (':', 'PNCT'), ('[', 'PNCT'), ('ˈruskʲɪɪ̯', 'UNKN'), ('ɪ̯ɪˈzɨk', 'UNKN'), (']', 'PNCT'), ('о', 'PREP'), ('файле', 'NOUN'), (')', 'PNCT'), ('[', 'PNCT'), ('~', 'UNKN'), ('3', 'NUMB'), (']', 'PNCT'), ('—', 'PNCT'), ('язык', 'NOUN'), ('восточнославянской', 'ADJF'), ('группы', 'NOUN'), ('славянской', 'ADJF'), ('ветви', 'NOUN'), ('индоевропейской', 'ADJF'), ('языковой', 'ADJF'), ('семьи', 'NOUN'), (',', 'PNCT'), ('национальный', 'ADJF'), ('язык', 'NOUN'), ('русского', 'ADJF'), ('народа', 'NOUN'), ('.', 'PNCT')]
                    results_universal = [('Русский', 'ADJ'), ('язык', 'NOUN'), ('(', 'PUNCT'), ('МФА', 'SYM/X'), (':', 'PUNCT'), ('[', 'PUNCT'), ('ˈruskʲɪɪ̯', 'SYM/X'), ('ɪ̯ɪˈzɨk', 'SYM/X'), (']', 'PUNCT'), ('о', 'ADP'), ('файле', 'NOUN'), (')', 'PUNCT'), ('[', 'PUNCT'), ('~', 'SYM/X'), ('3', 'NUM'), (']', 'PUNCT'), ('—', 'PUNCT'), ('язык', 'NOUN'), ('восточнославянской', 'ADJ'), ('группы', 'NOUN'), ('славянской', 'ADJ'), ('ветви', 'NOUN'), ('индоевропейской', 'ADJ'), ('языковой', 'ADJ'), ('семьи', 'NOUN'), (',', 'PUNCT'), ('национальный', 'ADJ'), ('язык', 'NOUN'), ('русского', 'ADJ'), ('народа', 'NOUN'), ('.', 'PUNCT')]
                case _:
                    tests_lang_util_skipped = True
        case 'tha':
            match pos_tagger:
                case 'pythainlp_perceptron_blackboard':
                    results = [('ภาษาไทย', 'NN'), ('หรือ', 'CC'), ('ภาษาไทย', 'NN'), ('กลาง', 'NN'), ('เป็น', 'VV'), ('ภาษา', 'NN'), ('ใน', 'PS'), ('กลุ่ม', 'NN'), ('ภาษา', 'NN'), ('ไท', 'NN'), ('สาขา', 'NN'), ('ย่อย', 'VV'), ('เชียงแสน', 'NN'), ('ซึ่ง', 'CC'), ('เป็น', 'VV'), ('กลุ่มย่อย', 'NN'), ('ของ', 'PS'), ('ตระกูล', 'NN'), ('ภาษา', 'NN'), ('ข', 'NN'), ('ร้า', 'NN'), ('-', 'PU'), ('ไท', 'NN'), ('และ', 'CC'), ('เป็น', 'VV'), ('ภาษาราชการ', 'NN'), ('และ', 'CC'), ('ภาษาประจำชาติ', 'NN'), ('ของ', 'PS'), ('ประเทศ', 'NN'), ('ไทย', 'NN'), ('[3][4]', 'NN')]
                    results_universal = [('ภาษาไทย', 'NOUN'), ('หรือ', 'CCONJ'), ('ภาษาไทย', 'NOUN'), ('กลาง', 'NOUN'), ('เป็น', 'VERB'), ('ภาษา', 'NOUN'), ('ใน', 'ADP'), ('กลุ่ม', 'NOUN'), ('ภาษา', 'NOUN'), ('ไท', 'NOUN'), ('สาขา', 'NOUN'), ('ย่อย', 'VERB'), ('เชียงแสน', 'NOUN'), ('ซึ่ง', 'CCONJ'), ('เป็น', 'VERB'), ('กลุ่มย่อย', 'NOUN'), ('ของ', 'ADP'), ('ตระกูล', 'NOUN'), ('ภาษา', 'NOUN'), ('ข', 'NOUN'), ('ร้า', 'NOUN'), ('-', 'PUNCT'), ('ไท', 'NOUN'), ('และ', 'CCONJ'), ('เป็น', 'VERB'), ('ภาษาราชการ', 'NOUN'), ('และ', 'CCONJ'), ('ภาษาประจำชาติ', 'NOUN'), ('ของ', 'ADP'), ('ประเทศ', 'NOUN'), ('ไทย', 'NOUN'), ('[3][4]', 'NOUN')]
                case 'pythainlp_perceptron_orchid':
                    results = [('ภาษาไทย', 'NPRP'), ('หรือ', 'JCRG'), ('ภาษาไทย', 'NPRP'), ('กลาง', 'VATT'), ('เป็น', 'VSTA'), ('ภาษา', 'NCMN'), ('ใน', 'RPRE'), ('กลุ่ม', 'NCMN'), ('ภาษา', 'NCMN'), ('ไท', 'NCMN'), ('สาขา', 'NCMN'), ('ย่อย', 'VATT'), ('เชียงแสน', 'VATT'), ('ซึ่ง', 'PREL'), ('เป็น', 'VSTA'), ('กลุ่มย่อย', 'NCMN'), ('ของ', 'RPRE'), ('ตระกูล', 'NCMN'), ('ภาษา', 'NCMN'), ('ข', 'NCMN'), ('ร้า', 'NCMN'), ('-', 'PUNC'), ('ไท', 'NCMN'), ('และ', 'JCRG'), ('เป็น', 'VSTA'), ('ภาษาราชการ', 'NCMN'), ('และ', 'JCRG'), ('ภาษาประจำชาติ', 'NCMN'), ('ของ', 'RPRE'), ('ประเทศ', 'NCMN'), ('ไทย', 'NPRP'), ('[3][4]', 'NCMN')]
                    results_universal = [('ภาษาไทย', 'PROPN'), ('หรือ', 'CCONJ'), ('ภาษาไทย', 'PROPN'), ('กลาง', 'ADJ'), ('เป็น', 'VERB'), ('ภาษา', 'NOUN'), ('ใน', 'ADP'), ('กลุ่ม', 'NOUN'), ('ภาษา', 'NOUN'), ('ไท', 'NOUN'), ('สาขา', 'NOUN'), ('ย่อย', 'ADJ'), ('เชียงแสน', 'ADJ'), ('ซึ่ง', 'SCONJ'), ('เป็น', 'VERB'), ('กลุ่มย่อย', 'NOUN'), ('ของ', 'ADP'), ('ตระกูล', 'NOUN'), ('ภาษา', 'NOUN'), ('ข', 'NOUN'), ('ร้า', 'NOUN'), ('-', 'PUNCT'), ('ไท', 'NOUN'), ('และ', 'CCONJ'), ('เป็น', 'VERB'), ('ภาษาราชการ', 'NOUN'), ('และ', 'CCONJ'), ('ภาษาประจำชาติ', 'NOUN'), ('ของ', 'ADP'), ('ประเทศ', 'NOUN'), ('ไทย', 'PROPN'), ('[3][4]', 'NOUN')]
                case 'pythainlp_perceptron_pud':
                    results = results_universal = [('ภาษาไทย', 'NOUN'), ('หรือ', 'CCONJ'), ('ภาษาไทย', 'NOUN'), ('กลาง', 'NOUN'), ('เป็น', 'AUX'), ('ภาษา', 'NOUN'), ('ใน', 'ADP'), ('กลุ่ม', 'NOUN'), ('ภาษา', 'NOUN'), ('ไท', 'PROPN'), ('สาขา', 'NOUN'), ('ย่อย', 'ADJ'), ('เชียงแสน', 'PROPN'), ('ซึ่ง', 'DET'), ('เป็น', 'AUX'), ('กลุ่มย่อย', 'NOUN'), ('ของ', 'ADP'), ('ตระกูล', 'NOUN'), ('ภาษา', 'NOUN'), ('ข', 'NOUN'), ('ร้า', 'NOUN'), ('-', 'PUNCT'), ('ไท', 'PROPN'), ('และ', 'CCONJ'), ('เป็น', 'AUX'), ('ภาษาราชการ', 'NOUN'), ('และ', 'CCONJ'), ('ภาษาประจำชาติ', 'NOUN'), ('ของ', 'ADP'), ('ประเทศ', 'NOUN'), ('ไทย', 'PROPN'), ('[3][4]', 'NOUN')]
                case _:
                    tests_lang_util_skipped = True
        case 'xct':
            results = [('བོད་', 'PROPN'), ('ཀྱི་', 'PART'), ('སྐད་ཡིག་', 'NOUN'), ('ནི་', 'NO_POS'), ('བོད་ཡུལ་', 'PROPN'), ('དང་', 'NO_POS'), ('ཉེ་འཁོར་', 'NOUN'), ('གྱི་', 'PART'), ('ས་ཁུལ་', 'OTHER'), ('བལ་ཡུལ', 'PROPN'), ('།', 'PUNCT'), ('འབྲུག་', 'NOUN'), ('དང་', 'NO_POS'), ('འབྲས་ལྗོངས', 'OTHER'), ('།', 'PUNCT'), ('ལ་དྭགས་', 'PROPN'), ('ནས་', 'PART'), ('ལྷོ་', 'NOUN'), ('མོན་', 'PROPN'), ('རོང་', 'PROPN'), ('སོགས་', 'DET'), ('སུ་', 'ADP'), ('བེད་སྤྱོད་', 'OTHER'), ('བྱེད་པ', 'VERB'), ('འི་', 'PART'), ('སྐད་ཡིག་', 'NOUN'), ('དེ', 'DET'), ('།', 'PUNCT')]
            results_universal = [('བོད་', 'PROPN'), ('ཀྱི་', 'PART'), ('སྐད་ཡིག་', 'NOUN'), ('ནི་', 'X'), ('བོད་ཡུལ་', 'PROPN'), ('དང་', 'X'), ('ཉེ་འཁོར་', 'NOUN'), ('གྱི་', 'PART'), ('ས་ཁུལ་', 'X'), ('བལ་ཡུལ', 'PROPN'), ('།', 'PUNCT'), ('འབྲུག་', 'NOUN'), ('དང་', 'X'), ('འབྲས་ལྗོངས', 'X'), ('།', 'PUNCT'), ('ལ་དྭགས་', 'PROPN'), ('ནས་', 'PART'), ('ལྷོ་', 'NOUN'), ('མོན་', 'PROPN'), ('རོང་', 'PROPN'), ('སོགས་', 'DET'), ('སུ་', 'ADP'), ('བེད་སྤྱོད་', 'X'), ('བྱེད་པ', 'VERB'), ('འི་', 'PART'), ('སྐད་ཡིག་', 'NOUN'), ('དེ', 'DET'), ('།', 'PUNCT')]
        case 'bod':
            results = results_universal = [('བོད་', 'NOUN'), ('ཀྱི་', 'ADP'), ('སྐད་ཡིག་', 'NOUN'), ('ནི་', 'PART'), ('བོད་ཡུལ་', 'PROPN'), ('དང་ཉེ་', 'PROPN'), ('འཁོར་', 'NOUN'), ('གྱི་', 'ADP'), ('ས་ཁུལ་', 'NOUN'), ('བལ་ཡུལ', 'ADJ'), ('།', 'PUNCT'), ('འབྲུག་', 'NOUN'), ('དང་', 'CCONJ'), ('འབྲས་ལྗོངས', 'NOUN'), ('།', 'PUNCT'), ('ལ་དྭགས་', 'PROPN'), ('ནས་', 'ADP'), ('ལྷོ་', 'NOUN'), ('མོན་', 'PROPN'), ('རོང་', 'NOUN'), ('སོགས་', 'NOUN'), ('སུ་', 'ADP'), ('བེད་སྤྱོད་བྱེད་པ', 'VERB'), ('འི་', 'ADP'), ('སྐད་ཡིག་', 'NOUN'), ('དེ', 'PRON'), ('།', 'PUNCT')]
        case 'ukr':
            results = [('Украї́нська', 'ADJF'), ('мо́ва', 'ADJF'), ('(', 'PNCT'), ('МФА', 'UNKN'), (':', 'PNCT'), ('[', 'PNCT'), ('ʊkrɐˈjinʲsʲkɐ', 'UNKN'), ('ˈmɔʋɐ', 'UNKN'), (']', 'PNCT'), (',', 'PNCT'), ('історична', 'ADJF'), ('назва', 'NOUN'), ('—', 'PNCT'), ('ру́ська', 'ADJF'), ('[', 'PNCT'), ('10', 'NUMB'), (']', 'PNCT'), ('[', 'PNCT'), ('11', 'NUMB'), (']', 'PNCT'), ('[', 'PNCT'), ('12', 'NUMB'), (']', 'PNCT'), ('[', 'PNCT'), ('*', 'PNCT'), ('1', 'NUMB'), (']', 'PNCT'), (')', 'PNCT'), ('—', 'PNCT'), ('національна', 'ADJF'), ('мова', 'NOUN'), ('українців', 'NOUN'), ('.', 'PNCT')]
            results_universal = [('Украї́нська', 'ADJ'), ('мо́ва', 'ADJ'), ('(', 'PUNCT'), ('МФА', 'SYM/X'), (':', 'PUNCT'), ('[', 'PUNCT'), ('ʊkrɐˈjinʲsʲkɐ', 'SYM/X'), ('ˈmɔʋɐ', 'SYM/X'), (']', 'PUNCT'), (',', 'PUNCT'), ('історична', 'ADJ'), ('назва', 'NOUN'), ('—', 'PUNCT'), ('ру́ська', 'ADJ'), ('[', 'PUNCT'), ('10', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('11', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('12', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('*', 'PUNCT'), ('1', 'NUM'), (']', 'PUNCT'), (')', 'PUNCT'), ('—', 'PUNCT'), ('національна', 'ADJ'), ('мова', 'NOUN'), ('українців', 'NOUN'), ('.', 'PUNCT')]
        case 'vie':
            results = [('Tiếng', 'N'), ('Việt', 'Np'), ('hay', 'C'), ('tiếng', 'N'), ('Kinh', 'Np'), ('là', 'V'), ('một', 'M'), ('ngôn ngữ', 'N'), ('thuộc ngữ', 'V'), ('hệ', 'N'), ('Nam Á', 'Np'), (',', 'CH'), ('được', 'V'), ('công nhận', 'V'), ('là', 'C'), ('ngôn ngữ', 'N'), ('chính thức', 'A'), ('tại', 'E'), ('Việt Nam', 'Np'), ('.', 'CH')]
            results_universal = [('Tiếng', 'NOUN'), ('Việt', 'PROPN'), ('hay', 'CCONJ'), ('tiếng', 'NOUN'), ('Kinh', 'PROPN'), ('là', 'VERB'), ('một', 'NUM'), ('ngôn ngữ', 'NOUN'), ('thuộc ngữ', 'VERB'), ('hệ', 'NOUN'), ('Nam Á', 'PROPN'), (',', 'PUNCT'), ('được', 'VERB'), ('công nhận', 'VERB'), ('là', 'CCONJ'), ('ngôn ngữ', 'NOUN'), ('chính thức', 'ADJ'), ('tại', 'ADP'), ('Việt Nam', 'PROPN'), ('.', 'PUNCT')]
        case _:
            raise wl_test_init.Wl_Exc_Tests_Lang_Skipped(lang)

    if tests_lang_util_skipped:
        raise wl_test_init.Wl_Exc_Tests_Lang_Util_Skipped(pos_tagger)

    wl_test_pos_tag_models(lang, pos_tagger, test_sentence, tokens, results, results_universal)

def wl_test_pos_tag_models(lang, pos_tagger, test_sentence, tokens, results, results_universal):
    # Untokenized
    tokens_untokenized = wl_pos_tagging.wl_pos_tag(
        main,
        inputs = test_sentence,
        lang = lang,
        pos_tagger = pos_tagger
    )
    tokens_untokenized_universal = wl_pos_tagging.wl_pos_tag(
        main,
        inputs = test_sentence,
        lang = lang,
        pos_tagger = pos_tagger,
        tagset = 'universal'
    )

    # Remove separators between token and tags
    tokens_tags_untokenized = [(str(token), token.tag[1:]) for token in tokens_untokenized]
    tokens_tags_untokenized_universal = [(str(token), token.tag[1:]) for token in tokens_untokenized_universal]

    print(f'{lang} / {pos_tagger}:')
    print(tokens_tags_untokenized)
    print(f'{tokens_tags_untokenized_universal}\n')

    # Tokenized
    tokens_tokenized = wl_pos_tagging.wl_pos_tag(
        main,
        inputs = tokens,
        lang = lang,
        pos_tagger = pos_tagger,
        force = True
    )
    tokens_tokenized_universal = wl_pos_tagging.wl_pos_tag(
        main,
        inputs = tokens,
        lang = lang,
        pos_tagger = pos_tagger,
        tagset = 'universal',
        force = True
    )

    tokens_tags_tokenized = [(str(token), token.tag) for token in tokens_tokenized]
    tokens_tags_tokenized_universal = [(str(token), token.tag) for token in tokens_tokenized_universal]

    assert tokens_tags_untokenized == results
    assert tokens_tags_untokenized_universal == results_universal

    # Check for empty tags
    assert tokens_tags_untokenized
    assert tokens_tags_untokenized_universal
    assert tokens_tags_tokenized
    assert tokens_tags_tokenized_universal
    assert all((tag for _, tag in tokens_tags_untokenized))
    assert all((tag for _, tag in tokens_tags_untokenized_universal))
    assert all((tag for _, tag in tokens_tags_tokenized))
    assert all((tag for _, tag in tokens_tags_tokenized_universal))

    # Universal tags should not all be "X"
    assert any((tag for _, tag in tokens_tags_untokenized_universal if tag != 'X'))
    assert any((tag for _, tag in tokens_tags_tokenized_universal if tag != 'X'))

    # Tokenization should not be modified
    assert len(tokens) == len(tokens_tags_tokenized) == len(tokens_tags_tokenized_universal)

    # Long
    tokens_long = wl_pos_tagging.wl_pos_tag(
        main,
        inputs = wl_texts.to_tokens(wl_test_lang_examples.TOKENS_LONG, lang = lang),
        lang = lang,
        pos_tagger = pos_tagger
    )

    assert [str(token) for token in tokens_long] == wl_test_lang_examples.TOKENS_LONG

    # Tagged
    tags_orig = ['_TEST']
    tokens_tagged = wl_pos_tagging.wl_pos_tag(
        main,
        inputs = wl_texts.to_tokens(['test'], lang = lang, tags = tags_orig),
        lang = lang,
        pos_tagger = pos_tagger
    )
    tags_tagged = [token.tag for token in tokens_tagged]

    assert tags_tagged == tags_orig

@pytest.mark.parametrize('lang, pos_tagger', test_pos_taggers)
def test_pos_tag_universal(lang, pos_tagger):
    for i, _ in enumerate(main.settings_custom['pos_tagging']['tagsets']['mapping_settings'][lang][pos_tagger]):
        main.settings_custom['pos_tagging']['tagsets']['mapping_settings'][lang][pos_tagger][i][1] = 'TAG'
        main.settings_custom['pos_tagging']['tagsets']['mapping_settings'][lang][pos_tagger][i][2] = 'CONTENT_FUNCTION'

    main.settings_custom['pos_tagging']['pos_tagger_settings']['to_universal_pos_tags'] = True

    test_sentence = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}')

    tokens_tagged = wl_pos_tagging.wl_pos_tag(
        main,
        inputs = test_sentence,
        lang = lang,
        pos_tagger = pos_tagger
    )

    for token in tokens_tagged:
        assert token.tag == '_TAG'
        assert token.tag_universal == 'TAG'
        assert token.content_function == 'CONTENT_FUNCTION'

    main.settings_custom['pos_tagging']['pos_tagger_settings']['to_universal_pos_tags'] = False

    tokens_tagged = wl_pos_tagging.wl_pos_tag(
        main,
        inputs = test_sentence,
        lang = lang,
        pos_tagger = pos_tagger
    )

    for token in tokens_tagged:
        assert token.tag != '_TAG'
        assert token.tag_universal == 'TAG'
        assert token.content_function == 'CONTENT_FUNCTION'

def test_pos_tag_separator():
    main.settings_custom['pos_tagging']['pos_tagger_settings']['separator_between_tokens_pos_tags'] = '/'

    tokens_tagged = wl_pos_tagging.wl_pos_tag(
        main,
        inputs = getattr(wl_test_lang_examples, 'SENTENCE_ENG_US'),
        lang = 'eng_us',
    )

    for token in tokens_tagged:
        assert token.tag.startswith('/')

if __name__ == '__main__':
    test_to_content_function()

    for lang, pos_tagger in test_pos_taggers_local:
        test_pos_tag(lang, pos_tagger)
        test_pos_tag_universal(lang, pos_tagger)

    test_pos_tag_separator()
