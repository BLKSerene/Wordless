# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Sanskrit
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

def test_stanza_san():
    results_pos_tag = [('संस्कृतम्', 'NOUN'), ('जगतः', 'PRON'), ('एकतमा', 'NOUN'), ('अतिप्राचीना', 'NOUN'), ('समृद्धा', 'NOUN'), ('शास्त्रीया', 'NOUN'), ('च', 'ADJ'), ('भाषासु', 'NOUN'), ('वर्तते', 'NOUN'), ('।', 'NOUN')]

    test_stanza.wl_test_stanza(
        lang = 'san',
        results_sentence_tokenize = ['संस्कृतम् जगतः एकतमा', 'अतिप्राचीना समृद्धा शास्त्रीया', 'च भाषासु वर्तते। संस्कृतम् भारतस्य जगत: वा भाषासु एकतमा\u200c प्राचीनतमा। भारती, सुरभारती, अमरभारती, अमरवाणी, सुरवाणी, गीर्वाणवाणी, गीर्वाणी, देववाणी, देवभाषा, संस्कृतावाक्, दैवीवाक्, इत्यादिभिः नामभिः एतद्भाषा प्रसिद्धा', '।'],
        results_word_tokenize = ['संस्कृतम्', 'जगतः', 'एकतमा', 'अतिप्राचीना', 'समृद्धा', 'शास्त्रीया', 'च', 'भाषासु', 'वर्तते', '।'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['संस्कृतम्', 'जगतः', 'एकतमा', 'अतिप्राचीना', 'समृद्धा', 'शास्त्रीया', 'च', 'भाषासु', 'वर्तते', '।'],
        results_dependency_parse = [('संस्कृतम्', 'संस्कृतम्', 'root', 0), ('जगतः', 'एकतमा', 'nmod', 1), ('एकतमा', 'संस्कृतम्', 'vocative', -2), ('अतिप्राचीना', 'शास्त्रीया', 'nsubj', 2), ('समृद्धा', 'शास्त्रीया', 'nsubj', 1), ('शास्त्रीया', 'शास्त्रीया', 'root', 0), ('च', 'च', 'root', 0), ('भाषासु', 'च', 'nsubj', -1), ('वर्तते', 'च', 'conj', -2), ('।', '।', 'root', 0)]
    )

if __name__ == '__main__':
    test_stanza_san()
