# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Tamil
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

def test_stanza_tam():
    test_stanza.wl_test_stanza(
        lang = 'tam',
        results_sentence_tokenize = ['தமிழ் (Tamil language) தமிழர்களினதும் தமிழ் பேசும் பலரின் தாய்மொழி ஆகும்.', 'தமிழ், உலகில் உள்ள முதன்மையான மொழிகளில் ஒன்றும் செம்மொழியும் ஆகும்.', 'இந்தியா, இலங்கை, மலேசியா, சிங்கப்பூர் ஆகிய நாடுகளில் அதிக அளவிலும், ஐக்கிய அரபு அமீரகம், தென்னாப்பிரிக்கா, மொரிசியசு, பிசி, இரீயூனியன், திரினிடாடு போன்ற நாடுகளில் சிறிய அளவிலும் தமிழ் பேசப்படுகிறது.', '1997-ஆம் ஆண்டுப் புள்ளி விவரப்படி உலகம் முழுவதிலும் 8 கோடி (80 மில்லியன்) மக்களால் பேசப்படும் தமிழ்,[13] ஒரு மொழியைத் தாய்மொழியாகக் கொண்டு பேசும் மக்களின் எண்ணிக்கை அடிப்படையில் பதினெட்டாவது இடத்தில் உள்ளது.', '[14] இணையத்தில் அதிகம் பயன்படுத்தப்படும் இந்திய மொழிகளில் தமிழ் முதன்மையாக உள்ளதாக 2017-ஆம் ஆண்டு நடைபெற்ற கூகுள் கணக்கெடுப்பில் தெரிய வந்தது.', '[15]'],
        results_word_tokenize = ['தமிழ்', '(', 'Tamil', 'language', ')', 'தமிழர்களினதும்', 'தமிழ்', 'பேசும்', 'பலரின்', 'தாய்மொழி', 'ஆகும்', '.'],
        results_pos_tag = [('தமிழ்', 'NEN-3SN--'), ('(', 'Z:-------'), ('Tamil', 'NEN-3SN--'), ('language', 'NNN-3SN--'), (')', 'Z:-------'), ('தமிழர்களினத்', 'NEN-3PA--'), ('உம்', 'Tv-------'), ('தமிழ்', 'NEN-3SN--'), ('பேசும்', 'Jd-F----A'), ('பலரின்', 'NON-3SN--'), ('தாய்மொழி', 'NNN-3SN--'), ('ஆகும்', 'VR-F3SNAA'), ('.', 'Z#-------')],
        results_pos_tag_universal = [('தமிழ்', 'PROPN'), ('(', 'PUNCT'), ('Tamil', 'PROPN'), ('language', 'NOUN'), (')', 'PUNCT'), ('தமிழர்களினத்', 'PROPN'), ('உம்', 'PART'), ('தமிழ்', 'PROPN'), ('பேசும்', 'ADJ'), ('பலரின்', 'PROPN'), ('தாய்மொழி', 'NOUN'), ('ஆகும்', 'AUX'), ('.', 'PUNCT')],
        results_lemmatize = ['தமிழ்', '(', 'Tamil', 'language', ')', 'தமிழர்', 'உம்', 'தமிழ்', 'பேசு', 'பலரின்', 'தாய்மொழி', 'ஆகு', '.'],
        results_dependency_parse = [('தமிழ்', 'language', 'nmod', 3), ('(', 'language', 'punct', 2), ('Tamil', 'language', 'nmod', 1), ('language', 'தமிழர்களினத்', 'nmod', 2), (')', 'தமிழர்களினத்', 'punct', 1), ('தமிழர்களினத்', 'பேசும்', 'nmod', 3), ('உம்', 'தமிழர்களினத்', 'advmod:emph', -1), ('தமிழ்', 'பேசும்', 'nmod', 1), ('பேசும்', 'தாய்மொழி', 'amod', 2), ('பலரின்', 'தாய்மொழி', 'nmod', 1), ('தாய்மொழி', 'தாய்மொழி', 'root', 0), ('ஆகும்', 'தாய்மொழி', 'aux', -1), ('.', 'தாய்மொழி', 'punct', -2)]
    )

if __name__ == '__main__':
    test_stanza_tam()
