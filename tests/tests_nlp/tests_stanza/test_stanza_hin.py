# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Hindi
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

def test_stanza_hin():
    test_stanza.wl_test_stanza(
        lang = 'hin',
        results_sentence_tokenize = ['हिन्दी जिसके मानकीकृत रूप को मानक हिन्दी कहा जाता है, विश्व की एक प्रमुख भाषा है और भारत की एक राजभाषा है।', 'केन्द्रीय स्तर पर भारत में सह-आधिकारिक भाषा अंग्रेजी है।', 'यह हिन्दुस्तानी भाषा की एक मानकीकृत रूप है जिसमें संस्कृत के तत्सम तथा तद्भव शब्दों का प्रयोग अधिक है और अरबी–फ़ारसी शब्द कम हैं।', 'हिन्दी संवैधानिक रूप से भारत की राजभाषा और भारत की सबसे अधिक बोली और समझी जाने वाली भाषा है।', 'हिन्दी भारत की राष्ट्रभाषा नहीं है क्योंकि भारत के संविधान में किसी भी भाषा को ऐसा दर्जा नहीं दिया गया है।', '[5][6] एथनोलॉग के अनुसार हिन्दी विश्व की तीसरी सबसे अधिक बोली जाने वाली भाषा है।', '[7] विश्व आर्थिक मंच की गणना के अनुसार यह विश्व की दस शक्तिशाली भाषाओं में से एक है।', '[8]'],
        results_word_tokenize = ['हिन्दी', 'जिसके', 'मानकीकृत', 'रूप', 'को', 'मानक', 'हिन्दी', 'कहा', 'जाता', 'है', ',', 'विश्व', 'की', 'एक', 'प्रमुख', 'भाषा', 'है', 'और', 'भारत', 'की', 'एक', 'राजभाषा', 'है', '।'],
        results_pos_tag = [('हिन्दी', 'NN'), ('जिसके', 'PRP'), ('मानकीकृत', 'JJ'), ('रूप', 'NN'), ('को', 'PSP'), ('मानक', 'JJ'), ('हिन्दी', 'NN'), ('कहा', 'VM'), ('जाता', 'VAUX'), ('है', 'VAUX'), (',', 'SYM'), ('विश्व', 'NN'), ('की', 'PSP'), ('एक', 'QC'), ('प्रमुख', 'JJ'), ('भाषा', 'NN'), ('है', 'VM'), ('और', 'CC'), ('भारत', 'NNP'), ('की', 'PSP'), ('एक', 'QC'), ('राजभाषा', 'NN'), ('है', 'VM'), ('।', 'SYM')],
        results_pos_tag_universal = [('हिन्दी', 'NOUN'), ('जिसके', 'PRON'), ('मानकीकृत', 'ADJ'), ('रूप', 'NOUN'), ('को', 'ADP'), ('मानक', 'ADJ'), ('हिन्दी', 'NOUN'), ('कहा', 'VERB'), ('जाता', 'AUX'), ('है', 'AUX'), (',', 'PUNCT'), ('विश्व', 'NOUN'), ('की', 'ADP'), ('एक', 'NUM'), ('प्रमुख', 'ADJ'), ('भाषा', 'NOUN'), ('है', 'AUX'), ('और', 'CCONJ'), ('भारत', 'PROPN'), ('की', 'ADP'), ('एक', 'NUM'), ('राजभाषा', 'NOUN'), ('है', 'AUX'), ('।', 'PUNCT')],
        results_lemmatize = ['हिन्दी', 'जो', 'मानकीकृत', 'रूप', 'को', 'मानक', 'हिन्दी', 'कह', 'जा', 'है', ',', 'विश्व', 'का', 'एक', 'प्रमुख', 'भाषा', 'है', 'और', 'भारत', 'का', 'एक', 'राजभाषा', 'है', '।'],
        results_dependency_parse = [('हिन्दी', 'भाषा', 'nsubj', 15), ('जिसके', 'रूप', 'nmod', 2), ('मानकीकृत', 'रूप', 'amod', 1), ('रूप', 'कहा', 'obj', 4), ('को', 'रूप', 'case', -1), ('मानक', 'हिन्दी', 'amod', 1), ('हिन्दी', 'कहा', 'acl', 1), ('कहा', 'हिन्दी', 'acl:relcl', -7), ('जाता', 'कहा', 'aux:pass', -1), ('है', 'कहा', 'aux:pass', -2), (',', 'कहा', 'punct', -3), ('विश्व', 'भाषा', 'nmod', 4), ('की', 'विश्व', 'case', -1), ('एक', 'भाषा', 'nummod', 2), ('प्रमुख', 'भाषा', 'amod', 1), ('भाषा', 'भाषा', 'root', 0), ('है', 'भाषा', 'cop', -1), ('और', 'राजभाषा', 'cc', 4), ('भारत', 'राजभाषा', 'nmod', 3), ('की', 'भारत', 'case', -1), ('एक', 'राजभाषा', 'nummod', 1), ('राजभाषा', 'भाषा', 'conj', -6), ('है', 'राजभाषा', 'cop', -1), ('।', 'भाषा', 'punct', -8)]
    )

if __name__ == '__main__':
    test_stanza_hin()
