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
    results_pos_tag = [('سنڌي', 'NOUN'), ('(', 'PUNCT'), ('/', 'PUNCT'), ('ˈsɪndi', 'PROPN'), ('/', 'PUNCT'), ('[6]सिन्धी,', 'PUNCT'), ('Sindhi', 'PROPN'), (')', 'PUNCT'), ('ھڪ', 'NUM'), ('ھند', 'PROPN'), ('-', 'PUNCT'), ('آريائي', 'ADJ'), ('ٻولي', 'NOUN'), ('آھي', 'AUX'), ('جيڪا', 'DET'), ('سنڌ', 'PROPN'), ('جي', 'ADP'), ('تاريخي', 'ADJ'), ('خطي', 'NOUN'), ('۾', 'ADP'), ('سنڌي', 'NOUN'), ('ماڻھن', 'NOUN'), ('پاران', 'ADP'), ('ڳالھائي', 'VERB'), ('وڃي', 'VERB'), ('ٿي', 'AUX'), ('.', 'PUNCT')]

    test_stanza.wl_test_stanza(
        lang = 'snd',
        results_sentence_tokenize = ['سنڌي (/ˈsɪndi/[6]सिन्धी, Sindhi)ھڪ ھند-آريائي ٻولي آھي جيڪا سنڌ جي تاريخي خطي ۾ سنڌي ماڻھن پاران ڳالھائي وڃي ٿي.', 'سنڌي پاڪستان جي صوبي سنڌ جي سرڪاري ٻولي آھي.', '[7][8][9] انڊيا ۾، سنڌي وفاقي سرڪار پاران مڃتا حاصل ڪيل ٻولين يعني شيڊيولڊ ٻولين مان ھڪ آھي.', 'گھڻا سنڌي ڳالھائيندڙ پاڪستان جي صوبي سنڌ، ڀارت جي رياست گجرات جي علائقي ڪڇ ۽ مھاراشٽر جي علائقي الھاس نگر ۾ رھن ٿا.', 'ڀارت ۾ بچيل ڳالھائيندڙ سنڌي ھندو آھن جن پاڪستان جي آزادي کان بعد 1948ع ۾ ڀارت ۾ رھائش اختيار ڪئي ۽ باقي سنڌي سڄي دنيا جي مختلف علائقن ۾ رھن ٿا.', 'سنڌي ٻولي پاڪستان جي صوبن سنڌ، بلوچستان ۽ پنجاب، سان گڏوگڏ ڀارت جي رياستن راجستان، پنجاب ۽ گجرات ۾ ڳالھائي وڃي ٿي.', 'ان سان گڏوگڏ ھانگ ڪانگ، عمان، انڊونيشيا، سنگاپور، گڏيل عرب اماراتون، گڏيل بادشاھت ۽ آمريڪا ۾ لڏي ويل جماعتن پاران بہ ڳالھائي وڃي ٿي.', '[10]'],
        results_word_tokenize = ['سنڌي', '(', '/', 'ˈsɪndi', '/', '[6]सिन्धी,', 'Sindhi', ')', 'ھڪ', 'ھند', '-', 'آريائي', 'ٻولي', 'آھي', 'جيڪا', 'سنڌ', 'جي', 'تاريخي', 'خطي', '۾', 'سنڌي', 'ماڻھن', 'پاران', 'ڳالھائي', 'وڃي', 'ٿي', '.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_dependency_parse = [('سنڌي', 'ٻولي', 'nsubj', 12), ('(', 'ˈsɪndi', 'punct', 2), ('/', 'ˈsɪndi', 'punct', 1), ('ˈsɪndi', 'سنڌي', 'conj', -3), ('/', 'ˈsɪndi', 'punct', -1), ('[6]सिन्धी,', 'ˈsɪndi', 'punct', -2), ('Sindhi', 'سنڌي', 'conj', -6), (')', 'Sindhi', 'punct', -1), ('ھڪ', 'ھند', 'nummod', 1), ('ھند', 'ٻولي', 'nmod', 3), ('-', 'آريائي', 'cc', 1), ('آريائي', 'ھند', 'conj', -2), ('ٻولي', 'ٻولي', 'root', 0), ('آھي', 'ٻولي', 'cop', -1), ('جيڪا', 'ڳالھائي', 'mark', 9), ('سنڌ', 'خطي', 'nmod', 3), ('جي', 'سنڌ', 'case', -1), ('تاريخي', 'خطي', 'amod', 1), ('خطي', 'ڳالھائي', 'obl', 5), ('۾', 'خطي', 'case', -1), ('سنڌي', 'ماڻھن', 'nmod', 1), ('ماڻھن', 'ڳالھائي', 'obl', 2), ('پاران', 'ماڻھن', 'case', -1), ('ڳالھائي', 'ٻولي', 'acl:relcl', -11), ('وڃي', 'ڳالھائي', 'compound', -1), ('ٿي', 'ڳالھائي', 'aux', -2), ('.', 'ڳالھائي', 'punct', -3)]
    )

if __name__ == '__main__':
    test_stanza_snd()
