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

from tests import wl_test_init, wl_test_lang_examples
from wordless.wl_nlp import wl_pos_tagging, wl_texts, wl_word_tokenization
from wordless.wl_utils import wl_misc

_, is_macos, _ = wl_misc.check_os()

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')

test_pos_taggers = []
test_pos_taggers_local = []

for lang, pos_taggers in main.settings_global['pos_taggers'].items():
    for pos_tagger in pos_taggers:
        if pos_tagger == 'botok_bod':
            test_pos_taggers.append(pytest.param(
                lang, pos_tagger,
                marks = pytest.mark.xfail(is_macos, reason = 'https://github.com/OpenPecha/Botok/issues/76')
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
            results = [('English', 'NNP'), ('is', 'VBZ'), ('a', 'DT'), ('West', 'NNP'), ('Germanic', 'NNP'), ('language', 'NN'), ('in', 'IN'), ('the', 'DT'), ('Indo-European', 'JJ'), ('language', 'NN'), ('family', 'NN'), ('.', '.')]
            results_universal = [('English', 'PROPN'), ('is', 'VERB'), ('a', 'DET'), ('West', 'PROPN'), ('Germanic', 'PROPN'), ('language', 'NOUN'), ('in', 'ADP/SCONJ'), ('the', 'DET'), ('Indo-European', 'ADJ'), ('language', 'NOUN'), ('family', 'NOUN'), ('.', 'PUNCT')]
        case 'jpn':
            results = [('日本語', '名詞-普通名詞-一般'), ('（', '補助記号-括弧開'), ('にほん', '名詞-固有名詞-地名-国'), ('ご', '接尾辞-名詞的-一般'), ('、', '補助記号-読点'), ('にっぽん', '名詞-固有名詞-地名-国'), ('ご', '接尾辞-名詞的-一般'), ('[', '補助記号-括弧開'), ('注釈', '名詞-普通名詞-サ変可能'), ('2', '名詞-数詞'), (']', '補助記号-括弧閉'), ('）', '補助記号-括弧閉'), ('は', '助詞-係助詞'), ('、', '補助記号-読点'), ('日本', '名詞-固有名詞-地名-国'), ('国', '接尾辞-名詞的-一般'), ('内', '接尾辞-名詞的-一般'), ('や', '助詞-副助詞'), ('、', '補助記号-読点'), ('かつて', '副詞'), ('の', '助詞-格助詞'), ('日本', '名詞-固有名詞-地名-国'), ('領', '接尾辞-名詞的-一般'), ('だっ', '助動詞'), ('た', '助動詞'), ('国', '名詞-普通名詞-一般'), ('、', '補助記号-読点'), ('そして', '接続詞'), ('国外', '名詞-普通名詞-一般'), ('移民', '名詞-普通名詞-サ変可能'), ('や', '助詞-副助詞'), ('移住者', '名詞-普通名詞-一般'), ('を', '助詞-格助詞'), ('含む', '動詞-一般'), ('日本人', '名詞-普通名詞-一般'), ('同士', '接尾辞-名詞的-一般'), ('の', '助詞-格助詞'), ('間', '名詞-普通名詞-副詞可能'), ('で', '助詞-格助詞'), ('使用', '名詞-普通名詞-サ変可能'), ('さ', '動詞-非自立可能'), ('れ', '助動詞'), ('て', '助詞-接続助詞'), ('いる', '動詞-非自立可能'), ('言語', '名詞-普通名詞-一般'), ('。', '補助記号-句点')]
            results_universal = [('日本語', 'NOUN'), ('（', 'PUNCT'), ('にほん', 'PROPN'), ('ご', 'NOUN'), ('、', 'PUNCT'), ('にっぽん', 'PROPN'), ('ご', 'NOUN'), ('[', 'PUNCT'), ('注釈', 'NOUN'), ('2', 'NUM'), (']', 'PUNCT'), ('）', 'PUNCT'), ('は', 'ADP'), ('、', 'PUNCT'), ('日本', 'PROPN'), ('国', 'NOUN'), ('内', 'NOUN'), ('や', 'ADP'), ('、', 'PUNCT'), ('かつて', 'ADV'), ('の', 'ADP'), ('日本', 'PROPN'), ('領', 'NOUN'), ('だっ', 'AUX'), ('た', 'AUX'), ('国', 'NOUN'), ('、', 'PUNCT'), ('そして', 'CCONJ'), ('国外', 'NOUN'), ('移民', 'NOUN'), ('や', 'ADP'), ('移住者', 'NOUN'), ('を', 'ADP'), ('含む', 'VERB'), ('日本人', 'NOUN'), ('同士', 'NOUN'), ('の', 'ADP'), ('間', 'NOUN'), ('で', 'ADP'), ('使用', 'NOUN'), ('さ', 'AUX'), ('れ', 'AUX'), ('て', 'SCONJ'), ('いる', 'AUX'), ('言語', 'NOUN'), ('。', 'PUNCT')]
        case 'khm':
            results = [('ភាសា', 'n'), ('ខ្មែរ', 'n'), ('គឺជា', 'v'), ('ភាសា', 'n'), ('កំណើត', 'n'), ('របស់', 'o'), ('ជនជាតិ', 'n'), ('ខ្មែរ', 'n'), ('និង', 'o'), ('ជា', 'v'), ('ភាសា', 'n'), ('ផ្លូវការ', 'n'), ('របស់', 'o'), ('ប្រទេស', 'n'), ('កម្ពុជា', 'n'), ('។', '.')]
            results_universal = [('ភាសា', 'NOUN'), ('ខ្មែរ', 'NOUN'), ('គឺជា', 'VERB'), ('ភាសា', 'NOUN'), ('កំណើត', 'NOUN'), ('របស់', 'PART'), ('ជនជាតិ', 'NOUN'), ('ខ្មែរ', 'NOUN'), ('និង', 'PART'), ('ជា', 'VERB'), ('ភាសា', 'NOUN'), ('ផ្លូវការ', 'NOUN'), ('របស់', 'PART'), ('ប្រទេស', 'NOUN'), ('កម្ពុជា', 'NOUN'), ('។', 'PUNCT')]
        case 'kor':
            results = [('세계', 'NNG'), ('여러', 'MM'), ('지역', 'NNG'), ('에', 'JKB'), ('한', 'MM'), ('민족', 'NNG'), ('인구', 'NNG'), ('가', 'JKS'), ('거주', 'NNG'), ('하', 'XSA'), ('게', 'EC'), ('되', 'VV'), ('면서', 'EC'), ('전', 'MM'), ('세계', 'NNG'), ('각지', 'NNG'), ('에서', 'JKB'), ('한국어', 'NNG'), ('가', 'JKS'), ('사용', 'NNG'), ('되', 'VV'), ('고', 'EC'), ('있', 'VX'), ('다', 'EF'), ('.', 'SF')]
            results_universal = [('세계', 'NOUN'), ('여러', 'DET'), ('지역', 'NOUN'), ('에', 'ADP'), ('한', 'DET'), ('민족', 'NOUN'), ('인구', 'NOUN'), ('가', 'ADP'), ('거주', 'NOUN'), ('하', 'X'), ('게', 'X'), ('되', 'VERB'), ('면서', 'X'), ('전', 'DET'), ('세계', 'NOUN'), ('각지', 'NOUN'), ('에서', 'ADP'), ('한국어', 'NOUN'), ('가', 'ADP'), ('사용', 'NOUN'), ('되', 'VERB'), ('고', 'X'), ('있', 'AUX'), ('다', 'X'), ('.', 'PUNCT')]
        case 'lao':
            match pos_tagger:
                case 'laonlp_seqlabeling':
                    results = [('ພາສາລາວ', 'N'), ('(', 'V'), ('Lao', 'PRN'), (':', 'PUNCT'), ('ລາວ', 'PRS'), (',', 'PUNCT'), ('[', 'PUNCT'), ('l', 'PRN'), ('áː', 'PRN'), ('w', 'PRN'), (']', 'PUNCT'), ('ຫຼື', 'COJ'), ('ພາສາລາວ', 'PRN'), (',', 'PUNCT'), ('[', 'N'), ('p', 'PRN'), ('ʰáː', 'PRN'), ('s', 'PRN'), ('ǎː', 'PRN'), ('l', 'PRN'), ('áː', 'PRN'), ('w', 'PRN'), ('])', 'PRN'), ('ເປັນ', 'V'), ('ພາສາ', 'N'), ('ຕະກູນ', 'PRN'), ('ໄທ', 'PRN'), ('-', 'PUNCT'), ('ກະໄດ', 'N'), ('ຂອງ', 'PRE'), ('ຄົນ', 'N'), ('ລາວ', 'PRS'), ('ໂດຍ', 'PRE'), ('ມີ', 'V'), ('ຄົນ', 'N'), ('ເວົ້າ', 'V'), ('ໃນປະເທດລາວ', 'N'), ('ເຊິ່ງ', 'REL'), ('ເປັນ', 'V'), ('ພາສາ', 'N'), ('ລັດຖະການ', 'N'), ('ຂອງ', 'PRE'), ('ສາທາລະນະລັດ', 'N'), ('ປະຊາທິປະໄຕ', 'N'), ('ປະຊາຊົນ', 'N'), ('ລາວ', 'PRS'), ('ຂອງ', 'PRE'), ('ປະຊາກອນ', 'N'), ('ປະມານ', 'IBQ'), ('7', 'V'), ('ລ້ານ', 'N'), ('ຄົນ', 'N'), ('ແລະ', 'COJ'), ('ໃນ', 'PRE'), ('ພື້ນທີ່', 'N'), ('ພາກ', 'N'), ('ຕາເວັນອອກສຽງ', 'N'), ('ເໜືອ', 'PRN'), ('ຂອງ', 'PRE'), ('ປະເທດໄທ', 'PRN'), ('ທີ່ມີ', 'V'), ('ຄົນ', 'N'), ('ເວົ້າ', 'V'), ('ປະມານ', 'IBQ'), ('23', 'V'), ('ລ້ານ', 'N'), ('ຄົນ', 'N'), ('ທາງ', 'PRE'), ('ລັດຖະບານ', 'N'), ('ປະເທດໄທ', 'PRN'), ('ມີການສະໜັບສະໜຸນ', 'V'), ('ໃຫ້', 'PVA'), ('ເອີ້ນ', 'V'), ('ພາສາລາວ', 'N'), ('ຖິ່ນ', 'N'), ('ໄທ', 'PRN'), ('ວ່າ', 'COJ'), ('ພາສາລາວ', 'PRN'), ('ຖິ່ນ', 'PRN'), ('ອີສານ', 'N'), ('ນອກຈາກ', 'PRE'), ('ນີ້', 'DMN'), (',', 'PUNCT'), ('ຢູ່', 'PRE'), ('ທາງ', 'N'), ('ພາກ', 'N'), ('ຕາເວັນອອກສຽງ', 'N'), ('ເໜືອ', 'N'), ('ຂອງ', 'PRE'), ('ປະເທດກຳປູເຈຍ', 'N'), ('ກໍ', 'IAC'), ('ມີ', 'V'), ('ຄົນ', 'N'), ('ເວົ້າ', 'V'), ('ພາສາລາວ', 'N'), ('ຄືກັນ', 'ADJ'), ('.', 'PUNCT')]
                    results_universal = [('ພາສາລາວ', 'NOUN'), ('(', 'VERB'), ('Lao', 'PROPN'), (':', 'PUNCT'), ('ລາວ', 'PRON'), (',', 'PUNCT'), ('[', 'PUNCT'), ('l', 'PROPN'), ('áː', 'PROPN'), ('w', 'PROPN'), (']', 'PUNCT'), ('ຫຼື', 'CONJ'), ('ພາສາລາວ', 'PROPN'), (',', 'PUNCT'), ('[', 'NOUN'), ('p', 'PROPN'), ('ʰáː', 'PROPN'), ('s', 'PROPN'), ('ǎː', 'PROPN'), ('l', 'PROPN'), ('áː', 'PROPN'), ('w', 'PROPN'), ('])', 'PROPN'), ('ເປັນ', 'VERB'), ('ພາສາ', 'NOUN'), ('ຕະກູນ', 'PROPN'), ('ໄທ', 'PROPN'), ('-', 'PUNCT'), ('ກະໄດ', 'NOUN'), ('ຂອງ', 'ADP'), ('ຄົນ', 'NOUN'), ('ລາວ', 'PRON'), ('ໂດຍ', 'ADP'), ('ມີ', 'VERB'), ('ຄົນ', 'NOUN'), ('ເວົ້າ', 'VERB'), ('ໃນປະເທດລາວ', 'NOUN'), ('ເຊິ່ງ', 'PRON'), ('ເປັນ', 'VERB'), ('ພາສາ', 'NOUN'), ('ລັດຖະການ', 'NOUN'), ('ຂອງ', 'ADP'), ('ສາທາລະນະລັດ', 'NOUN'), ('ປະຊາທິປະໄຕ', 'NOUN'), ('ປະຊາຊົນ', 'NOUN'), ('ລາວ', 'PRON'), ('ຂອງ', 'ADP'), ('ປະຊາກອນ', 'NOUN'), ('ປະມານ', 'DET'), ('7', 'VERB'), ('ລ້ານ', 'NOUN'), ('ຄົນ', 'NOUN'), ('ແລະ', 'CONJ'), ('ໃນ', 'ADP'), ('ພື້ນທີ່', 'NOUN'), ('ພາກ', 'NOUN'), ('ຕາເວັນອອກສຽງ', 'NOUN'), ('ເໜືອ', 'PROPN'), ('ຂອງ', 'ADP'), ('ປະເທດໄທ', 'PROPN'), ('ທີ່ມີ', 'VERB'), ('ຄົນ', 'NOUN'), ('ເວົ້າ', 'VERB'), ('ປະມານ', 'DET'), ('23', 'VERB'), ('ລ້ານ', 'NOUN'), ('ຄົນ', 'NOUN'), ('ທາງ', 'ADP'), ('ລັດຖະບານ', 'NOUN'), ('ປະເທດໄທ', 'PROPN'), ('ມີການສະໜັບສະໜຸນ', 'VERB'), ('ໃຫ້', 'AUX'), ('ເອີ້ນ', 'VERB'), ('ພາສາລາວ', 'NOUN'), ('ຖິ່ນ', 'NOUN'), ('ໄທ', 'PROPN'), ('ວ່າ', 'CONJ'), ('ພາສາລາວ', 'PROPN'), ('ຖິ່ນ', 'PROPN'), ('ອີສານ', 'NOUN'), ('ນອກຈາກ', 'ADP'), ('ນີ້', 'PRON'), (',', 'PUNCT'), ('ຢູ່', 'ADP'), ('ທາງ', 'NOUN'), ('ພາກ', 'NOUN'), ('ຕາເວັນອອກສຽງ', 'NOUN'), ('ເໜືອ', 'NOUN'), ('ຂອງ', 'ADP'), ('ປະເທດກຳປູເຈຍ', 'NOUN'), ('ກໍ', 'DET'), ('ມີ', 'VERB'), ('ຄົນ', 'NOUN'), ('ເວົ້າ', 'VERB'), ('ພາສາລາວ', 'NOUN'), ('ຄືກັນ', 'ADJ'), ('.', 'PUNCT')]
                case 'laonlp_yunshan_cup_2020':
                    results = [('ພາສາລາວ', 'PRN'), ('(', 'PUNCT'), ('Lao', 'PRN'), (':', 'PUNCT'), ('ລາວ', 'PRS'), (',', 'PUNCT'), ('[', 'COJ'), ('l', 'N'), ('áː', 'N'), ('w', 'N'), (']', 'PUNCT'), ('ຫຼື', 'COJ'), ('ພາສາລາວ', 'PRN'), (',', 'PUNCT'), ('[', 'PUNCT'), ('p', 'PRN'), ('ʰáː', 'PRN'), ('s', 'PRN'), ('ǎː', 'PRN'), ('l', 'PRN'), ('áː', 'PRN'), ('w', 'PRN'), ('])', 'PRN'), ('ເປັນ', 'V'), ('ພາສາ', 'N'), ('ຕະກູນ', 'PRN'), ('ໄທ', 'PRN'), ('-', 'PUNCT'), ('ກະໄດ', 'N'), ('ຂອງ', 'PRE'), ('ຄົນ', 'N'), ('ລາວ', 'PRS'), ('ໂດຍ', 'PRE'), ('ມີ', 'V'), ('ຄົນ', 'N'), ('ເວົ້າ', 'V'), ('ໃນປະເທດລາວ', 'N'), ('ເຊິ່ງ', 'REL'), ('ເປັນ', 'V'), ('ພາສາ', 'N'), ('ລັດຖະການ', 'N'), ('ຂອງ', 'PRE'), ('ສາທາລະນະລັດ', 'N'), ('ປະຊາທິປະໄຕ', 'N'), ('ປະຊາຊົນ', 'N'), ('ລາວ', 'PRS'), ('ຂອງ', 'PRE'), ('ປະຊາກອນ', 'N'), ('ປະມານ', 'IBQ'), ('7', 'V'), ('ລ້ານ', 'V'), ('ຄົນ', 'N'), ('ແລະ', 'COJ'), ('ໃນ', 'PRE'), ('ພື້ນທີ່', 'N'), ('ພາກ', 'N'), ('ຕາເວັນອອກສຽງ', 'V'), ('ເໜືອ', 'PRN'), ('ຂອງ', 'PRE'), ('ປະເທດໄທ', 'PRN'), ('ທີ່ມີ', 'V'), ('ຄົນ', 'N'), ('ເວົ້າ', 'V'), ('ປະມານ', 'IBQ'), ('23', 'V'), ('ລ້ານ', 'CLF'), ('ຄົນ', 'N'), ('ທາງ', 'PRE'), ('ລັດຖະບານ', 'N'), ('ປະເທດໄທ', 'PRN'), ('ມີການສະໜັບສະໜຸນ', 'V'), ('ໃຫ້', 'PVA'), ('ເອີ້ນ', 'V'), ('ພາສາລາວ', 'N'), ('ຖິ່ນ', 'N'), ('ໄທ', 'PRN'), ('ວ່າ', 'COJ'), ('ພາສາລາວ', 'PRN'), ('ຖິ່ນ', 'PRN'), ('ອີສານ', 'N'), ('ນອກຈາກ', 'PRE'), ('ນີ້', 'DMN'), (',', 'PUNCT'), ('ຢູ່', 'ADV'), ('ທາງ', 'PRE'), ('ພາກ', 'N'), ('ຕາເວັນອອກສຽງ', 'N'), ('ເໜືອ', 'N'), ('ຂອງ', 'PRE'), ('ປະເທດກຳປູເຈຍ', 'N'), ('ກໍ', 'IAC'), ('ມີ', 'V'), ('ຄົນ', 'N'), ('ເວົ້າ', 'V'), ('ພາສາລາວ', 'N'), ('ຄືກັນ', 'ADJ'), ('.', 'PUNCT')]
                    results_universal = [('ພາສາລາວ', 'PROPN'), ('(', 'PUNCT'), ('Lao', 'PROPN'), (':', 'PUNCT'), ('ລາວ', 'PRON'), (',', 'PUNCT'), ('[', 'CONJ'), ('l', 'NOUN'), ('áː', 'NOUN'), ('w', 'NOUN'), (']', 'PUNCT'), ('ຫຼື', 'CONJ'), ('ພາສາລາວ', 'PROPN'), (',', 'PUNCT'), ('[', 'PUNCT'), ('p', 'PROPN'), ('ʰáː', 'PROPN'), ('s', 'PROPN'), ('ǎː', 'PROPN'), ('l', 'PROPN'), ('áː', 'PROPN'), ('w', 'PROPN'), ('])', 'PROPN'), ('ເປັນ', 'VERB'), ('ພາສາ', 'NOUN'), ('ຕະກູນ', 'PROPN'), ('ໄທ', 'PROPN'), ('-', 'PUNCT'), ('ກະໄດ', 'NOUN'), ('ຂອງ', 'ADP'), ('ຄົນ', 'NOUN'), ('ລາວ', 'PRON'), ('ໂດຍ', 'ADP'), ('ມີ', 'VERB'), ('ຄົນ', 'NOUN'), ('ເວົ້າ', 'VERB'), ('ໃນປະເທດລາວ', 'NOUN'), ('ເຊິ່ງ', 'PRON'), ('ເປັນ', 'VERB'), ('ພາສາ', 'NOUN'), ('ລັດຖະການ', 'NOUN'), ('ຂອງ', 'ADP'), ('ສາທາລະນະລັດ', 'NOUN'), ('ປະຊາທິປະໄຕ', 'NOUN'), ('ປະຊາຊົນ', 'NOUN'), ('ລາວ', 'PRON'), ('ຂອງ', 'ADP'), ('ປະຊາກອນ', 'NOUN'), ('ປະມານ', 'DET'), ('7', 'VERB'), ('ລ້ານ', 'VERB'), ('ຄົນ', 'NOUN'), ('ແລະ', 'CONJ'), ('ໃນ', 'ADP'), ('ພື້ນທີ່', 'NOUN'), ('ພາກ', 'NOUN'), ('ຕາເວັນອອກສຽງ', 'VERB'), ('ເໜືອ', 'PROPN'), ('ຂອງ', 'ADP'), ('ປະເທດໄທ', 'PROPN'), ('ທີ່ມີ', 'VERB'), ('ຄົນ', 'NOUN'), ('ເວົ້າ', 'VERB'), ('ປະມານ', 'DET'), ('23', 'VERB'), ('ລ້ານ', 'PART'), ('ຄົນ', 'NOUN'), ('ທາງ', 'ADP'), ('ລັດຖະບານ', 'NOUN'), ('ປະເທດໄທ', 'PROPN'), ('ມີການສະໜັບສະໜຸນ', 'VERB'), ('ໃຫ້', 'AUX'), ('ເອີ້ນ', 'VERB'), ('ພາສາລາວ', 'NOUN'), ('ຖິ່ນ', 'NOUN'), ('ໄທ', 'PROPN'), ('ວ່າ', 'CONJ'), ('ພາສາລາວ', 'PROPN'), ('ຖິ່ນ', 'PROPN'), ('ອີສານ', 'NOUN'), ('ນອກຈາກ', 'ADP'), ('ນີ້', 'PRON'), (',', 'PUNCT'), ('ຢູ່', 'ADV'), ('ທາງ', 'ADP'), ('ພາກ', 'NOUN'), ('ຕາເວັນອອກສຽງ', 'NOUN'), ('ເໜືອ', 'NOUN'), ('ຂອງ', 'ADP'), ('ປະເທດກຳປູເຈຍ', 'NOUN'), ('ກໍ', 'DET'), ('ມີ', 'VERB'), ('ຄົນ', 'NOUN'), ('ເວົ້າ', 'VERB'), ('ພາສາລາວ', 'NOUN'), ('ຄືກັນ', 'ADJ'), ('.', 'PUNCT')]
                case _:
                    tests_lang_util_skipped = True
        case 'rus':
            match pos_tagger:
                case 'nltk_perceptron_rus':
                    results = [('Ру́сский', 'A=m'), ('язы́к', 'S'), ('(', 'NONLEX'), ('МФА', 'S'), (':', 'NONLEX'), ('[', 'NONLEX'), ('ˈruskʲɪi̯', 'NONLEX'), ('jɪˈzɨk', 'NONLEX'), (']', 'NONLEX'), ('ⓘ', 'NONLEX'), (')', 'NONLEX'), ('[', 'NONLEX'), ('~', 'NONLEX'), ('3', 'NUM=ciph'), (']', 'NONLEX'), ('[', 'NONLEX'), ('⇨', 'NONLEX'), (']', 'NONLEX'), ('—', 'NONLEX'), ('язык', 'S'), ('восточнославянской', 'A=f'), ('группы', 'S'), ('славянской', 'A=f'), ('ветви', 'S'), ('индоевропейской', 'A=f'), ('языковой', 'A=f'), ('семьи', 'S'), (',', 'NONLEX'), ('национальный', 'A=m'), ('язык', 'S'), ('русского', 'A=m'), ('народа', 'S'), ('.', 'NONLEX')]
                    results_universal = [('Ру́сский', 'ADJ'), ('язы́к', 'NOUN'), ('(', 'PUNCT/SYM'), ('МФА', 'NOUN'), (':', 'PUNCT/SYM'), ('[', 'PUNCT/SYM'), ('ˈruskʲɪi̯', 'PUNCT/SYM'), ('jɪˈzɨk', 'PUNCT/SYM'), (']', 'PUNCT/SYM'), ('ⓘ', 'PUNCT/SYM'), (')', 'PUNCT/SYM'), ('[', 'PUNCT/SYM'), ('~', 'PUNCT/SYM'), ('3', 'NUM'), (']', 'PUNCT/SYM'), ('[', 'PUNCT/SYM'), ('⇨', 'PUNCT/SYM'), (']', 'PUNCT/SYM'), ('—', 'PUNCT/SYM'), ('язык', 'NOUN'), ('восточнославянской', 'ADJ'), ('группы', 'NOUN'), ('славянской', 'ADJ'), ('ветви', 'NOUN'), ('индоевропейской', 'ADJ'), ('языковой', 'ADJ'), ('семьи', 'NOUN'), (',', 'PUNCT/SYM'), ('национальный', 'ADJ'), ('язык', 'NOUN'), ('русского', 'ADJ'), ('народа', 'NOUN'), ('.', 'PUNCT/SYM')]
                case 'pymorphy3_morphological_analyzer':
                    results = [('Ру́сский', 'NOUN'), ('язы́к', 'NOUN'), ('(', 'PNCT'), ('МФА', 'UNKN'), (':', 'PNCT'), ('[', 'PNCT'), ('ˈruskʲɪi̯', 'UNKN'), ('jɪˈzɨk', 'UNKN'), (']', 'PNCT'), ('ⓘ', 'UNKN'), (')', 'PNCT'), ('[', 'PNCT'), ('~', 'UNKN'), ('3', 'NUMB'), (']', 'PNCT'), ('[', 'PNCT'), ('⇨', 'UNKN'), (']', 'PNCT'), ('—', 'PNCT'), ('язык', 'NOUN'), ('восточнославянской', 'ADJF'), ('группы', 'NOUN'), ('славянской', 'ADJF'), ('ветви', 'NOUN'), ('индоевропейской', 'ADJF'), ('языковой', 'ADJF'), ('семьи', 'NOUN'), (',', 'PNCT'), ('национальный', 'ADJF'), ('язык', 'NOUN'), ('русского', 'ADJF'), ('народа', 'NOUN'), ('.', 'PNCT')]
                    results_universal = [('Ру́сский', 'NOUN'), ('язы́к', 'NOUN'), ('(', 'PUNCT'), ('МФА', 'SYM/X'), (':', 'PUNCT'), ('[', 'PUNCT'), ('ˈruskʲɪi̯', 'SYM/X'), ('jɪˈzɨk', 'SYM/X'), (']', 'PUNCT'), ('ⓘ', 'SYM/X'), (')', 'PUNCT'), ('[', 'PUNCT'), ('~', 'SYM/X'), ('3', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('⇨', 'SYM/X'), (']', 'PUNCT'), ('—', 'PUNCT'), ('язык', 'NOUN'), ('восточнославянской', 'ADJ'), ('группы', 'NOUN'), ('славянской', 'ADJ'), ('ветви', 'NOUN'), ('индоевропейской', 'ADJ'), ('языковой', 'ADJ'), ('семьи', 'NOUN'), (',', 'PUNCT'), ('национальный', 'ADJ'), ('язык', 'NOUN'), ('русского', 'ADJ'), ('народа', 'NOUN'), ('.', 'PUNCT')]
                case _:
                    tests_lang_util_skipped = True
        case 'tha':
            match pos_tagger:
                case 'pythainlp_perceptron_blackboard':
                    results = [('ภาษาไทย', 'NN'), ('หรือ', 'CC'), ('ภาษาไทย', 'NN'), ('กลาง', 'NN'), ('เป็น', 'VV'), ('ภาษา', 'NN'), ('ใน', 'PS'), ('กลุ่ม', 'NN'), ('ภาษา', 'NN'), ('ไท', 'NN'), ('ซึ่ง', 'CC'), ('เป็น', 'VV'), ('กลุ่มย่อย', 'NN'), ('ของ', 'PS'), ('ตระกูล', 'NN'), ('ภาษา', 'NN'), ('ข', 'NN'), ('ร้า', 'NN'), ('-', 'PU'), ('ไท', 'NN'), ('และ', 'CC'), ('เป็น', 'VV'), ('ภาษาราชการ', 'NN'), ('และ', 'CC'), ('ภาษาประจำชาติ', 'NN'), ('ของ', 'PS'), ('ประเทศ', 'NN'), ('ไทย', 'NN'), ('[3][4]', 'NN')]
                    results_universal = [('ภาษาไทย', 'NOUN'), ('หรือ', 'CCONJ'), ('ภาษาไทย', 'NOUN'), ('กลาง', 'NOUN'), ('เป็น', 'VERB'), ('ภาษา', 'NOUN'), ('ใน', 'ADP'), ('กลุ่ม', 'NOUN'), ('ภาษา', 'NOUN'), ('ไท', 'NOUN'), ('ซึ่ง', 'CCONJ'), ('เป็น', 'VERB'), ('กลุ่มย่อย', 'NOUN'), ('ของ', 'ADP'), ('ตระกูล', 'NOUN'), ('ภาษา', 'NOUN'), ('ข', 'NOUN'), ('ร้า', 'NOUN'), ('-', 'PUNCT'), ('ไท', 'NOUN'), ('และ', 'CCONJ'), ('เป็น', 'VERB'), ('ภาษาราชการ', 'NOUN'), ('และ', 'CCONJ'), ('ภาษาประจำชาติ', 'NOUN'), ('ของ', 'ADP'), ('ประเทศ', 'NOUN'), ('ไทย', 'NOUN'), ('[3][4]', 'NOUN')]
                case 'pythainlp_perceptron_orchid':
                    results = [('ภาษาไทย', 'NPRP'), ('หรือ', 'JCRG'), ('ภาษาไทย', 'NPRP'), ('กลาง', 'VATT'), ('เป็น', 'VSTA'), ('ภาษา', 'NCMN'), ('ใน', 'RPRE'), ('กลุ่ม', 'NCMN'), ('ภาษา', 'NCMN'), ('ไท', 'NCMN'), ('ซึ่ง', 'PREL'), ('เป็น', 'VSTA'), ('กลุ่มย่อย', 'NCMN'), ('ของ', 'RPRE'), ('ตระกูล', 'NCMN'), ('ภาษา', 'NCMN'), ('ข', 'NCMN'), ('ร้า', 'NCMN'), ('-', 'PUNC'), ('ไท', 'NCMN'), ('และ', 'JCRG'), ('เป็น', 'VSTA'), ('ภาษาราชการ', 'NCMN'), ('และ', 'JCRG'), ('ภาษาประจำชาติ', 'NCMN'), ('ของ', 'RPRE'), ('ประเทศ', 'NCMN'), ('ไทย', 'NPRP'), ('[3][4]', 'NCMN')]
                    results_universal = [('ภาษาไทย', 'PROPN'), ('หรือ', 'CCONJ'), ('ภาษาไทย', 'PROPN'), ('กลาง', 'ADJ'), ('เป็น', 'VERB'), ('ภาษา', 'NOUN'), ('ใน', 'ADP'), ('กลุ่ม', 'NOUN'), ('ภาษา', 'NOUN'), ('ไท', 'NOUN'), ('ซึ่ง', 'SCONJ'), ('เป็น', 'VERB'), ('กลุ่มย่อย', 'NOUN'), ('ของ', 'ADP'), ('ตระกูล', 'NOUN'), ('ภาษา', 'NOUN'), ('ข', 'NOUN'), ('ร้า', 'NOUN'), ('-', 'PUNCT'), ('ไท', 'NOUN'), ('และ', 'CCONJ'), ('เป็น', 'VERB'), ('ภาษาราชการ', 'NOUN'), ('และ', 'CCONJ'), ('ภาษาประจำชาติ', 'NOUN'), ('ของ', 'ADP'), ('ประเทศ', 'NOUN'), ('ไทย', 'PROPN'), ('[3][4]', 'NOUN')]
                case 'pythainlp_perceptron_pud':
                    results = results_universal = [('ภาษาไทย', 'NOUN'), ('หรือ', 'CCONJ'), ('ภาษาไทย', 'NOUN'), ('กลาง', 'NOUN'), ('เป็น', 'AUX'), ('ภาษา', 'NOUN'), ('ใน', 'ADP'), ('กลุ่ม', 'NOUN'), ('ภาษา', 'NOUN'), ('ไท', 'PROPN'), ('ซึ่ง', 'DET'), ('เป็น', 'AUX'), ('กลุ่มย่อย', 'NOUN'), ('ของ', 'ADP'), ('ตระกูล', 'NOUN'), ('ภาษา', 'NOUN'), ('ข', 'NOUN'), ('ร้า', 'NOUN'), ('-', 'PUNCT'), ('ไท', 'PROPN'), ('และ', 'CCONJ'), ('เป็น', 'AUX'), ('ภาษาราชการ', 'NOUN'), ('และ', 'CCONJ'), ('ภาษาประจำชาติ', 'NOUN'), ('ของ', 'ADP'), ('ประเทศ', 'NOUN'), ('ไทย', 'PROPN'), ('[3][4]', 'NOUN')]
                case _:
                    tests_lang_util_skipped = True
        case 'bod':
            results = [('བོད་', 'PROPN'), ('ཀྱི་', 'PART'), ('སྐད་ཡིག་', 'NOUN'), ('ནི་', 'NO_POS'), ('བོད་ཡུལ་', 'PROPN'), ('དང་', 'NO_POS'), ('ཉེ་འཁོར་', 'NOUN'), ('གྱི་', 'PART'), ('ས་ཁུལ་', 'OTHER'), ('བལ་ཡུལ', 'PROPN'), ('།', 'PUNCT'), ('འབྲུག་', 'NOUN'), ('དང་', 'NO_POS'), ('འབྲས་ལྗོངས', 'OTHER'), ('།', 'PUNCT')]
            results_universal = [('བོད་', 'PROPN'), ('ཀྱི་', 'PART'), ('སྐད་ཡིག་', 'NOUN'), ('ནི་', 'X'), ('བོད་ཡུལ་', 'PROPN'), ('དང་', 'X'), ('ཉེ་འཁོར་', 'NOUN'), ('གྱི་', 'PART'), ('ས་ཁུལ་', 'X'), ('བལ་ཡུལ', 'PROPN'), ('།', 'PUNCT'), ('འབྲུག་', 'NOUN'), ('དང་', 'X'), ('འབྲས་ལྗོངས', 'X'), ('།', 'PUNCT')]
        case 'ukr':
            results = [('Украї́нська', 'ADJF'), ('мо́ва', 'ADJF'), ('(', 'PNCT'), ('МФА', 'UNKN'), (':', 'PNCT'), ('[', 'PNCT'), ('ukrɑ̽ˈjɪnʲsʲkɑ̽', 'UNKN'), ('ˈmɔwɑ̽', 'UNKN'), (']', 'PNCT'), (',', 'PNCT'), ('історичні', 'ADJF'), ('назви', 'NOUN'), ('—', 'PNCT'), ('ру́ська', 'ADJF'), ('[', 'PNCT'), ('10', 'NUMB'), (']', 'PNCT'), ('[', 'PNCT'), ('11', 'NUMB'), (']', 'PNCT'), ('[', 'PNCT'), ('12', 'NUMB'), (']', 'PNCT'), ('[', 'PNCT'), ('*', 'PNCT'), ('1', 'NUMB'), (']', 'PNCT'), (')', 'PNCT'), ('—', 'PNCT'), ('національна', 'ADJF'), ('мова', 'NOUN'), ('українців', 'NOUN'), ('.', 'PNCT')]
            results_universal = [('Украї́нська', 'ADJ'), ('мо́ва', 'ADJ'), ('(', 'PUNCT'), ('МФА', 'SYM/X'), (':', 'PUNCT'), ('[', 'PUNCT'), ('ukrɑ̽ˈjɪnʲsʲkɑ̽', 'SYM/X'), ('ˈmɔwɑ̽', 'SYM/X'), (']', 'PUNCT'), (',', 'PUNCT'), ('історичні', 'ADJ'), ('назви', 'NOUN'), ('—', 'PUNCT'), ('ру́ська', 'ADJ'), ('[', 'PUNCT'), ('10', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('11', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('12', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('*', 'PUNCT'), ('1', 'NUM'), (']', 'PUNCT'), (')', 'PUNCT'), ('—', 'PUNCT'), ('національна', 'ADJ'), ('мова', 'NOUN'), ('українців', 'NOUN'), ('.', 'PUNCT')]
        case 'vie':
            results = [('Tiếng', 'N'), ('Việt', 'Np'), (',', 'CH'), ('cũng', 'R'), ('gọi là', 'X'), ('tiếng', 'N'), ('Việt Nam', 'Np'), ('[', 'V'), ('9', 'M'), (']', 'CH'), ('hay', 'C'), ('Việt ngữ', 'V'), ('là', 'V'), ('ngôn ngữ', 'N'), ('của', 'E'), ('người', 'Nc'), ('Việt', 'Np'), ('và', 'C'), ('là', 'V'), ('ngôn ngữ', 'N'), ('chính thức', 'A'), ('tại', 'E'), ('Việt Nam', 'Np'), ('.', 'CH')]
            results_universal = [('Tiếng', 'NOUN'), ('Việt', 'PROPN'), (',', 'PUNCT'), ('cũng', 'X'), ('gọi là', 'X'), ('tiếng', 'NOUN'), ('Việt Nam', 'PROPN'), ('[', 'VERB'), ('9', 'NUM'), (']', 'PUNCT'), ('hay', 'CCONJ'), ('Việt ngữ', 'VERB'), ('là', 'VERB'), ('ngôn ngữ', 'NOUN'), ('của', 'ADP'), ('người', 'NOUN'), ('Việt', 'PROPN'), ('và', 'CCONJ'), ('là', 'VERB'), ('ngôn ngữ', 'NOUN'), ('chính thức', 'ADJ'), ('tại', 'ADP'), ('Việt Nam', 'PROPN'), ('.', 'PUNCT')]
        case _:
            raise wl_test_init.Wl_Exception_Tests_Lang_Skipped(lang)

    if tests_lang_util_skipped:
        raise wl_test_init.Wl_Exception_Tests_Lang_Util_Skipped(pos_tagger)

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
    assert all((tag for token, tag in tokens_tags_untokenized))
    assert all((tag for token, tag in tokens_tags_untokenized_universal))
    assert all((tag for token, tag in tokens_tags_tokenized))
    assert all((tag for token, tag in tokens_tags_tokenized_universal))

    # Universal tags should not all be "X"
    assert any((tag for token, tag in tokens_tags_untokenized_universal if tag != 'X'))
    assert any((tag for token, tag in tokens_tags_tokenized_universal if tag != 'X'))

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

def test_pos_tag_misc():
    # Default tagset with universal tagset conversion
    main.settings_custom['pos_tagging']['pos_tagger_settings']['to_universal_pos_tags'] = True

    wl_pos_tagging.wl_pos_tag(
        main,
        inputs = getattr(wl_test_lang_examples, 'SENTENCE_ENG_US'),
        lang = 'eng_us'
    )

    main.settings_custom['pos_tagging']['pos_tagger_settings']['to_universal_pos_tags'] = False

if __name__ == '__main__':
    test_to_content_function()

    for lang, pos_tagger in test_pos_taggers_local:
        test_pos_tag(lang, pos_tagger)

    test_pos_tag_misc()
