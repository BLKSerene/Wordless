# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Urdu
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

def test_stanza_urd():
    test_stanza.wl_test_stanza(
        lang = 'urd',
        results_sentence_tokenize = ['1837ء میں، اردو برطانوی ایسٹ انڈیا کمپنی کی سرکاری زبان بن گئی، کمپنی کے دور میں پورے شمالی ہندوستان میں فارسی کی جگہ لی گئی۔', 'فارسی اس وقت تک مختلف ہند-اسلامی سلطنتوں کی درباری زبان کے طور پر کام کرتی تھی۔', '[11] یورپی نوآبادیاتی دور میں مذہبی، سماجی اور سیاسی عوامل پیدا ہوئے جنھوں نے اردو اور ہندی کے درمیان فرق کیا، جس کی وجہ سے ہندی-اردو تنازعہ شروع ہوا ۔'],
        results_word_tokenize = ['1837ء', 'میں', '،', 'اردو', 'برطانوی', 'ایسٹ', 'انڈیا', 'کمپنی', 'کی', 'سرکاری', 'زبان', 'بن', 'گئی', '،', 'کمپنی', 'کے', 'دور', 'میں', 'پورے', 'شمالی', 'ہندوستان', 'میں', 'فارسی', 'کی', 'جگہ', 'لی', 'گئی', '۔'],
        results_pos_tag = [('1837ء', 'NNP'), ('میں', 'PSP'), ('،', 'SYM'), ('اردو', 'NNP'), ('برطانوی', 'NNPC'), ('ایسٹ', 'NNPC'), ('انڈیا', 'NNPC'), ('کمپنی', 'NNP'), ('کی', 'PSP'), ('سرکاری', 'JJ'), ('زبان', 'NN'), ('بن', 'VM'), ('گئی', 'VAUX'), ('،', 'SYM'), ('کمپنی', 'NN'), ('کے', 'PSP'), ('دور', 'NN'), ('میں', 'PSP'), ('پورے', 'JJ'), ('شمالی', 'JJ'), ('ہندوستان', 'NNP'), ('میں', 'PSP'), ('فارسی', 'NN'), ('کی', 'PSP'), ('جگہ', 'NN'), ('لی', 'VM'), ('گئی', 'VAUX'), ('۔', 'SYM')],
        results_pos_tag_universal = [('1837ء', 'PROPN'), ('میں', 'ADP'), ('،', 'PUNCT'), ('اردو', 'PROPN'), ('برطانوی', 'PROPN'), ('ایسٹ', 'PROPN'), ('انڈیا', 'PROPN'), ('کمپنی', 'PROPN'), ('کی', 'ADP'), ('سرکاری', 'ADJ'), ('زبان', 'NOUN'), ('بن', 'VERB'), ('گئی', 'AUX'), ('،', 'PUNCT'), ('کمپنی', 'NOUN'), ('کے', 'ADP'), ('دور', 'NOUN'), ('میں', 'ADP'), ('پورے', 'ADJ'), ('شمالی', 'ADJ'), ('ہندوستان', 'PROPN'), ('میں', 'ADP'), ('فارسی', 'NOUN'), ('کی', 'ADP'), ('جگہ', 'NOUN'), ('لی', 'VERB'), ('گئی', 'AUX'), ('۔', 'PUNCT')],
        results_lemmatize = ['1837ء', 'میں', '،', 'اردو', 'برطانوی', 'ایسٹ', 'انڈیا', 'کمپنی', 'کا', 'سرکاری', 'زبان', 'بن', 'جا', '،', 'کمپنی', 'کا', 'دور', 'میں', 'پورا', 'شمالی', 'ہندوستان', 'میں', 'فارسی', 'کا', 'جگہ', 'لے', 'جا', '۔'],
        results_dependency_parse = [('1837ء', 'بن', 'obl', 11), ('میں', '1837ء', 'case', -1), ('،', '1837ء', 'punct', -2), ('اردو', 'کمپنی', 'nmod', 4), ('برطانوی', 'کمپنی', 'compound', 3), ('ایسٹ', 'کمپنی', 'compound', 2), ('انڈیا', 'کمپنی', 'compound', 1), ('کمپنی', 'زبان', 'nmod', 3), ('کی', 'کمپنی', 'case', -1), ('سرکاری', 'زبان', 'amod', 1), ('زبان', 'بن', 'xcomp', 1), ('بن', 'کمپنی', 'acl:relcl', 3), ('گئی', 'بن', 'aux', -1), ('،', 'بن', 'punct', -2), ('کمپنی', 'دور', 'nmod', 2), ('کے', 'کمپنی', 'case', -1), ('دور', 'لی', 'obl', 9), ('میں', 'دور', 'case', -1), ('پورے', 'ہندوستان', 'amod', 2), ('شمالی', 'ہندوستان', 'amod', 1), ('ہندوستان', 'لی', 'obl', 5), ('میں', 'ہندوستان', 'case', -1), ('فارسی', 'جگہ', 'nmod', 2), ('کی', 'فارسی', 'case', -1), ('جگہ', 'لی', 'obl', 1), ('لی', 'لی', 'root', 0), ('گئی', 'لی', 'aux', -1), ('۔', 'لی', 'punct', -2)]
    )

if __name__ == '__main__':
    test_stanza_urd()
