# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Stanza - Sindhi
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

from tests.wl_tests_nlp.wl_tests_stanza import test_stanza

def test_stanza_snd():
    test_stanza.wl_test_stanza(
        lang = 'snd',
        results_sentence_tokenize = ['سنڌي (/ˈsɪndi/[6]सिन्धी, Sindhi)ھڪ ھند-آريائي ٻولي آھي جيڪا سنڌ جي تاريخي خطي ۾ سنڌي ماڻھن پاران ڳالھائي وڃي ٿي.', 'سنڌي پاڪستان جي صوبي سنڌ جي سرڪاري ٻولي آھي.', '[7][8][9] انڊيا ۾، سنڌي وفاقي سرڪار پاران مڃتا حاصل ڪيل ٻولين يعني شيڊيولڊ ٻولين مان ھڪ آھي.', 'گھڻا سنڌي ڳالھائيندڙ پاڪستان جي صوبي سنڌ، ڀارت جي رياست گجرات جي علائقي ڪڇ ۽ مھاراشٽر جي علائقي الھاس نگر ۾ رھن ٿا.', 'ڀارت ۾ بچيل ڳالھائيندڙ سنڌي ھندو آھن جن پاڪستان جي آزادي کان بعد 1948ع ۾ ڀارت ۾ رھائش اختيار ڪئي ۽ باقي سنڌي سڄي دنيا جي مختلف علائقن ۾ رھن ٿا.', 'سنڌي ٻولي پاڪستان جي صوبن سنڌ، بلوچستان ۽ پنجاب، سان گڏوگڏ ڀارت جي رياستن راجستان، پنجاب ۽ گجرات ۾ ڳالھائي وڃي ٿي.', 'ان سان گڏوگڏ ھانگ ڪانگ، عمان، انڊونيشيا، سنگاپور، گڏيل عرب اماراتون، گڏيل بادشاھت ۽ آمريڪا ۾ لڏي ويل جماعتن پاران بہ ڳالھائي وڃي ٿي.', '[10]'],
        results_word_tokenize = ['سنڌي', '(', '/', 'ˈsɪndi', '/', '[6]सिन्धी,', 'Sindhi', ')', 'ھڪ', 'ھند', '-', 'آريائي', 'ٻولي', 'آھي', 'جيڪا', 'سنڌ', 'جي', 'تاريخي', 'خطي', '۾', 'سنڌي', 'ماڻھن', 'پاران', 'ڳالھائي', 'وڃي', 'ٿي', '.']
    )

if __name__ == '__main__':
    test_stanza_snd()
