# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Stanza - Urdu
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

from tests.tests_nlp.tests_stanza import test_stanza

def test_stanza_urd():
    test_stanza.wl_test_stanza(
        lang = 'urd',
        results_sentence_tokenize = ['اُردُو[8] برصغیر کی معیاری زبانوں میں سے ایک ہے۔', 'یہ پاکستان کی قومی اور رابطہ عامہ کی زبان ہے، جبکہ بھارت کی چھ ریاستوں کی دفتری زبان کا درجہ رکھتی ہے۔', 'آئین ہند کے مطابق اسے 22 دفتری شناخت شدہ زبانوں میں شامل کیا جا چکا ہے۔', '2001ء کی مردم شماری کے مطابق اردو کو بطور مادری زبان بھارت میں 5.01% فیصد لوگ بولتے ہیں اور اس لحاظ سے ہی بھارت کی چھٹی بڑی زبان ہے جبکہ پاکستان میں اسے بطور مادری زبان 7.59% فیصد لوگ استعمال کرتے ہیں، یہ پاکستان کی پانچویں بڑی زبان ہے۔', 'اردو تاریخی طور پر ہندوستان کی مسلم آبادی سے جڑی ہے۔', '[9] زبانِ اردو کو پہچان و ترقی اس وقت ملی جب برطانوی دور میں انگریز حکمرانوں نے اسے فارسی کی بجائے انگریزی کے ساتھ شمالی ہندوستان کے علاقوں اور جموں و کشمیر میں اسے 1846ء اور پنجاب میں 1849ء میں بطور دفتری زبان نافذ کیا۔', 'اس کے علاوہ خلیجی، یورپی، ایشیائی اور امریکی علاقوں میں اردو بولنے والوں کی ایک بڑی تعداد آباد ہے جو بنیادی طور پر جنوبی ایشیاء سے کوچ کرنے والے اہلِ اردو ہیں۔', '1999ء کے اعداد و شمار کے مطابق اردو زبان کے مجموعی متکلمین کی تعداد دس کروڑ ساٹھ لاکھ کے لگ بھگ تھی۔', 'اس لحاظ سے یہ دنیا کی نویں بڑی زبان ہے۔', 'اردو زبان کو کئی ہندوستانی ریاستوں میں سرکاری حیثیت بھی حاصل ہے۔', 'نیپال میں، اردو ایک رجسٹرڈ علاقائی بولی ہے [12] اور جنوبی افریقہ میں یہ آئین میں ایک محفوظ زبان ہے۔', 'یہ افغانستان اور بنگلہ دیش میں اقلیتی زبان کے طور پر بھی بولی جاتی ہے، جس کی کوئی سرکاری حیثیت نہیں ہے۔'],
        results_word_tokenize = ['اُردُو[8]', 'برصغیر', 'کی', 'معیاری', 'زبانوں', 'میں', 'سے', 'ایک', 'ہے', '۔'],
        results_pos_tag = [('اُردُو[8]', 'NNPC'), ('برصغیر', 'NN'), ('کی', 'PSP'), ('معیاری', 'JJ'), ('زبانوں', 'NN'), ('میں', 'PSP'), ('سے', 'PSP'), ('ایک', 'QC'), ('ہے', 'VM'), ('۔', 'SYM')],
        results_pos_tag_universal = [('اُردُو[8]', 'PROPN'), ('برصغیر', 'NOUN'), ('کی', 'ADP'), ('معیاری', 'ADJ'), ('زبانوں', 'NOUN'), ('میں', 'ADP'), ('سے', 'ADP'), ('ایک', 'NUM'), ('ہے', 'AUX'), ('۔', 'PUNCT')],
        results_lemmatize = ['اُردُو[8]', 'برصغیر', 'کا', 'معیاری', 'زبان', 'میں', 'سے', 'ایک', 'ہے', '۔'],
        results_dependency_parse = [('اُردُو[8]', 'ایک', 'nsubj', 7), ('برصغیر', 'زبانوں', 'nmod', 3), ('کی', 'برصغیر', 'case', -1), ('معیاری', 'زبانوں', 'amod', 1), ('زبانوں', 'ایک', 'obl', 3), ('میں', 'زبانوں', 'case', -1), ('سے', 'زبانوں', 'case', -2), ('ایک', 'ایک', 'root', 0), ('ہے', 'ایک', 'cop', -1), ('۔', 'ایک', 'punct', -2)]
    )

if __name__ == '__main__':
    test_stanza_urd()
