# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Sindhi
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

def test_stanza_snd():
    test_stanza.wl_test_stanza(
        lang = 'snd',
        results_sentence_tokenize = ['سنڌي (/ˈsɪndi/[6]सिन्धी, Sindhi)ھڪ ھند-آريائي ٻولي آھي جيڪا سنڌ جي تاريخي خطي ۾ سنڌي ماڻھن پاران ڳالھائي وڃي ٿي.', 'سنڌي پاڪستان جي صوبي سنڌ جي سرڪاري ٻولي آھي.', '[', '7][8][9]'],
        results_word_tokenize = ['سنڌي', '(', '/', 'ˈsɪndi', '/', '[', '6', ']', 'सिन्धी,', 'Sindhi', ')', 'ھڪ', 'ھند', '-', 'آريائي', 'ٻولي', 'آھي', 'جيڪا', 'سنڌ', 'جي', 'تاريخي', 'خطي', '۾', 'سنڌي', 'ماڻھن', 'پاران', 'ڳالھائي', 'وڃي', 'ٿي', '.'],
        results_pos_tag = [('سنڌي', 'NNP'), ('(', 'PUNCT'), ('/', 'PUNCT'), ('ˈsɪndi', 'NNP'), ('/', 'PUNCT'), ('[', 'PUNCT'), ('6', 'NUM'), (']', 'PUNCT'), ('सिन्धी,', 'PUNCT'), ('Sindhi', 'NN'), (')', 'PUNCT'), ('ھڪ', 'NUM'), ('ھند', 'NNP'), ('-', 'PUNCT'), ('آريائي', 'JJ'), ('ٻولي', 'NN'), ('آھي', 'VAUX'), ('جيڪا', 'PRD'), ('سنڌ', 'NNP'), ('جي', 'PSPG'), ('تاريخي', 'JJ'), ('خطي', 'NN'), ('۾', 'PSPL'), ('سنڌي', 'NN'), ('ماڻھن', 'NN'), ('پاران', 'PSPL'), ('ڳالھائي', 'VM'), ('وڃي', 'VM'), ('ٿي', 'VAUX'), ('.', 'PUNCT')],
        results_pos_tag_universal = [('سنڌي', 'PROPN'), ('(', 'PUNCT'), ('/', 'PUNCT'), ('ˈsɪndi', 'PROPN'), ('/', 'PUNCT'), ('[', 'PUNCT'), ('6', 'NUM'), (']', 'PUNCT'), ('सिन्धी,', 'PUNCT'), ('Sindhi', 'NOUN'), (')', 'PUNCT'), ('ھڪ', 'NUM'), ('ھند', 'PROPN'), ('-', 'PUNCT'), ('آريائي', 'ADJ'), ('ٻولي', 'NOUN'), ('آھي', 'AUX'), ('جيڪا', 'DET'), ('سنڌ', 'PROPN'), ('جي', 'ADP'), ('تاريخي', 'ADJ'), ('خطي', 'NOUN'), ('۾', 'ADP'), ('سنڌي', 'NOUN'), ('ماڻھن', 'NOUN'), ('پاران', 'ADP'), ('ڳالھائي', 'VERB'), ('وڃي', 'VERB'), ('ٿي', 'AUX'), ('.', 'PUNCT')],
        results_lemmatize = ['سنڌ', '(', '/', 'ˈsɪndi', '/', '[', '6', ']', 'सिन्धी,', 'Sindhi', ')', 'ھڪ', 'ھند', '-', 'آريائي', 'ٻولي', 'آهي', 'جيڪو', 'سنڌ', 'جي', 'تاريخي', 'خطو', '۾', 'سنڌي', 'ماڻھو', 'پاران', 'ڳالھاءِ', 'وڃ', 'آهي', '.'],
        results_dependency_parse = [('سنڌي', 'ٻولي', 'parataxis', 15), ('(', 'ˈsɪndi', 'punct', 2), ('/', 'ˈsɪndi', 'punct', 1), ('ˈsɪndi', 'سنڌي', 'conj', -3), ('/', 'ˈsɪndi', 'punct', -1), ('[', 'ˈsɪndi', 'punct', -2), ('6', 'Sindhi', 'nummod', 3), (']', '6', 'punct', -1), ('सिन्धी,', 'Sindhi', 'punct', 1), ('Sindhi', 'سنڌي', 'conj', -9), (')', 'Sindhi', 'punct', -1), ('ھڪ', 'ھند', 'nummod', 1), ('ھند', 'ٻولي', 'nmod', 3), ('-', 'آريائي', 'punct', 1), ('آريائي', 'ھند', 'conj', -2), ('ٻولي', 'ٻولي', 'root', 0), ('آھي', 'ٻولي', 'cop', -1), ('جيڪا', 'ڳالھائي', 'nsubj', 9), ('سنڌ', 'خطي', 'nmod', 3), ('جي', 'سنڌ', 'case', -1), ('تاريخي', 'خطي', 'amod', 1), ('خطي', 'ڳالھائي', 'obl', 5), ('۾', 'خطي', 'case', -1), ('سنڌي', 'ماڻھن', 'nmod', 1), ('ماڻھن', 'ڳالھائي', 'obl', 2), ('پاران', 'ماڻھن', 'case', -1), ('ڳالھائي', 'ٻولي', 'acl:relcl', -11), ('وڃي', 'ڳالھائي', 'compound', -1), ('ٿي', 'ڳالھائي', 'aux', -2), ('.', 'ڳالھائي', 'punct', -3)]
    )

if __name__ == '__main__':
    test_stanza_snd()
