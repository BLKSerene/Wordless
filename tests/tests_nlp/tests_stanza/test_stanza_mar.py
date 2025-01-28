# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Marathi
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

def test_stanza_mar():
    results_pos_tag = [('मराठी', 'ADJ'), ('भाषा', 'NOUN'), ('ही', 'PART'), ('इंडो', 'ADJ'), ('-', 'PUNCT'), ('युरोपीय', 'ADJ'), ('भाषाकुळातील', 'NOUN'), ('एक', 'DET'), ('भाषा', 'NOUN'), ('आहे', 'AUX'), ('.', 'PUNCT')]

    test_stanza.wl_test_stanza(
        lang = 'mar',
        results_sentence_tokenize = ['मराठी भाषा ही इंडो-युरोपीय भाषाकुळातील एक भाषा आहे.', 'मराठी ही भारताच्या २२ अधिकृत भाषांपैकी एक आहे.', 'मराठी महाराष्ट्र राज्याची अधिकृत तर गोवा राज्याची सहअधिकृत भाषा आहे.', '२०११ च्या जनगणनेनुसार, भारतात मराठी भाषकांची एकूण लोकसंख्या सुमारे १४ कोटी आहे.', 'मराठी मातृभाषा असणाऱ्या लोकांच्या संख्येनुसार मराठी ही जगातील दहावी व भारतातील तिसरी भाषा आहे.', 'मराठी भाषा भारताच्या प्राचीन भाषांपैकी एक असून महाराष्ट्री प्राकृतचे आधुनिक रूप आहे.', 'मराठीचे वय सुमारे २४०० वर्ष आहे.', 'महाराष्ट्र हे मराठी भाषिकांचे राज्य म्हणून मराठी भाषेला वेगळे महत्त्व प्राप्त झालेले आहे.', 'आजतागायत मराठी भाषेतून अनेक श्रेष्ठ साहित्यकृती निर्माण झालेल्या आहेत आणि त्यात सातत्यपूर्ण रीतीने भर पडत आहे.', 'गोवा, गुजरात सारख्या राज्यातही मराठी भाषा काही प्रमाणात बोलली जाते.', 'गोव्यात मराठीला समृद्ध असा इतिहास आहे.', '[१]'],
        results_word_tokenize = ['मराठी', 'भाषा', 'ही', 'इंडो', '-', 'युरोपीय', 'भाषाकुळातील', 'एक', 'भाषा', 'आहे', '.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['मराठी', 'भाष', 'ही', 'इंडो', '-', 'युरोपीय', 'भाषाकुळळत', 'एक', 'भाष', 'असणे', '.'],
        results_dependency_parse = [('मराठी', 'भाषा', 'amod', 1), ('भाषा', 'भाषा', 'obl', 7), ('ही', 'भाषा', 'discourse', -1), ('इंडो', 'भाषाकुळातील', 'amod', 3), ('-', 'इंडो', 'punct', -1), ('युरोपीय', 'भाषाकुळातील', 'amod', 1), ('भाषाकुळातील', 'भाषा', 'obl', 2), ('एक', 'भाषा', 'det', 1), ('भाषा', 'भाषा', 'root', 0), ('आहे', 'भाषा', 'cop', -1), ('.', 'भाषा', 'punct', -2)],
        results_sentiment_analayze = [0]
    )

if __name__ == '__main__':
    test_stanza_mar()
