# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Turkish
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

def test_stanza_tur():
    test_stanza.wl_test_stanza(
        lang = 'tur',
        results_sentence_tokenize = ["Türkçe ya da Türk dili, Güneydoğu Avrupa ve Batı Asya'da konuşulan, Türk dilleri dil ailesine ait sondan eklemeli bir dil.", '[12] Türk dilleri ailesinin Oğuz dilleri grubundan bir Batı Oğuz dili olan Osmanlı Türkçesinin devamını oluşturur.', "Dil, başta Türkiye olmak üzere Balkanlar, Ege Adaları, Kıbrıs ve Orta Doğu'yu kapsayan eski Osmanlı İmparatorluğu coğrafyasında konuşulur.", "[12] Ethnologue'a göre Türkçe, yaklaşık 83 milyon konuşuru ile dünyada en çok konuşulan 16. dildir.", "[13] Türkçe Türkiye, Kıbrıs Cumhuriyeti ve Kuzey Kıbrıs'ta ulusal resmî dil statüsüne sahiptir.", '[', '12]'],
        results_word_tokenize = ['Türkçe', 'ya', 'da', 'Türk', 'dili', ',', 'Güneydoğu', 'Avrupa', 've', 'Batı', "Asya'da", 'konuşulan', ',', 'Türk', 'dilleri', 'dil', 'ailesine', 'ait', 'sondan', 'eklemeli', 'bir', 'dil', '.', '[', '12', ']'],
        results_pos_tag = [('Türkçe', 'Prop'), ('ya', 'Conj'), ('da', 'Conj'), ('Türk', 'Adj'), ('dili', 'Noun'), (',', 'Punc'), ('Güneydoğu', 'Adj'), ('Avrupa', 'Prop'), ('ve', 'Conj'), ('Batı', 'Adj'), ("Asya'da", 'Prop'), ('konuşulan', 'Verb'), (',', 'Punc'), ('Türk', 'Adj'), ('dilleri', 'Noun'), ('dil', 'Noun'), ('ailesine', 'Noun'), ('ait', 'PCDat'), ('sondan', 'Noun'), ('eklemeli', 'Adj'), ('bir', 'ANum'), ('dil', 'Noun'), ('.', 'Punc'), ('[', 'Punc'), ('12', 'NNum'), (']', 'Punc')],
        results_pos_tag_universal = [('Türkçe', 'PROPN'), ('ya', 'CCONJ'), ('da', 'CCONJ'), ('Türk', 'ADJ'), ('dili', 'NOUN'), (',', 'PUNCT'), ('Güneydoğu', 'ADJ'), ('Avrupa', 'PROPN'), ('ve', 'CCONJ'), ('Batı', 'ADJ'), ("Asya'da", 'PROPN'), ('konuşulan', 'VERB'), (',', 'PUNCT'), ('Türk', 'ADJ'), ('dilleri', 'NOUN'), ('dil', 'NOUN'), ('ailesine', 'NOUN'), ('ait', 'ADP'), ('sondan', 'NOUN'), ('eklemeli', 'ADJ'), ('bir', 'DET'), ('dil', 'NOUN'), ('.', 'PUNCT'), ('[', 'PUNCT'), ('12', 'NUM'), (']', 'PUNCT')],
        results_lemmatize = ['Türkçe', 'ya', 'da', 'Türk', 'dil', ',', 'güneydoğu', 'Avrupa', 've', 'batı', 'Asya', 'konuş', ',', 'Türk', 'dil', 'dil', 'aile', 'ait', 'son', 'eklemeli', 'bir', 'dil', '.', '(', '12', ')'],
        results_dependency_parse = [('Türkçe', 'konuşulan', 'obl', 11), ('ya', 'dili', 'cc', 3), ('da', 'ya', 'fixed', -1), ('Türk', 'dili', 'nmod:poss', 1), ('dili', 'Türkçe', 'conj', -4), (',', 'konuşulan', 'punct', 6), ('Güneydoğu', 'konuşulan', 'obl', 5), ('Avrupa', 'Güneydoğu', 'flat', -1), ('ve', 'Batı', 'cc', 1), ('Batı', 'Güneydoğu', 'conj', -3), ("Asya'da", 'Batı', 'flat', -1), ('konuşulan', 'dil', 'acl', 10), (',', 'konuşulan', 'punct', -1), ('Türk', 'dilleri', 'nmod:poss', 1), ('dilleri', 'ailesine', 'nmod:poss', 2), ('dil', 'ailesine', 'nmod:poss', 1), ('ailesine', 'eklemeli', 'obl', 3), ('ait', 'ailesine', 'case', -1), ('sondan', 'eklemeli', 'obl', 1), ('eklemeli', 'dil', 'amod', 2), ('bir', 'dil', 'det', 1), ('dil', 'dil', 'root', 0), ('.', 'dil', 'punct', -1), ('[', '[', 'root', 0), ('12', '12', 'root', 0), (']', '12', 'punct', -1)]
    )

if __name__ == '__main__':
    test_stanza_tur()
