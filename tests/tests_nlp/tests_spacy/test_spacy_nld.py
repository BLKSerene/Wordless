# ----------------------------------------------------------------------
# Tests: NLP - spaCy - Dutch
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

from tests.tests_nlp.tests_spacy import test_spacy

def test_spacy_nld():
    results_sentence_tokenize = ['Het Nederlands is een West-Germaanse taal, de meest gebruikte taal in Nederland en België, de officiële taal van Suriname en een van de drie officiële talen van België.', 'Binnen het Koninkrijk der Nederlanden is het Nederlands ook een officiële taal van Aruba, Curaçao en Sint-Maarten.', 'Het Nederlands is na Engels en Duits de meest gesproken Germaanse taal.']

    test_spacy.wl_test_spacy(
        lang = 'nld',
        results_sentence_tokenize_trf = results_sentence_tokenize,
        results_sentence_tokenize_lg = results_sentence_tokenize,
        results_word_tokenize = ['Het', 'Nederlands', 'is', 'een', 'West-Germaanse', 'taal', ',', 'de', 'meest', 'gebruikte', 'taal', 'in', 'Nederland', 'en', 'België', ',', 'de', 'officiële', 'taal', 'van', 'Suriname', 'en', 'een', 'van', 'de', 'drie', 'officiële', 'talen', 'van', 'België', '.'],
        results_pos_tag = [('Het', 'LID|bep|stan|evon'), ('Nederlands', 'N|eigen|ev|basis|onz|stan'), ('is', 'WW|pv|tgw|ev'), ('een', 'LID|onbep|stan|agr'), ('West-Germaanse', 'ADJ|prenom|basis|met-e|stan'), ('taal', 'N|soort|ev|basis|zijd|stan'), (',', 'LET'), ('de', 'LID|bep|stan|rest'), ('meest', 'VNW|onbep|grad|stan|vrij|zonder|sup'), ('gebruikte', 'WW|vd|prenom|met-e'), ('taal', 'N|soort|ev|basis|zijd|stan'), ('in', 'VZ|init'), ('Nederland', 'N|eigen|ev|basis|onz|stan'), ('en', 'VG|neven'), ('België', 'N|eigen|ev|basis|onz|stan'), (',', 'LET'), ('de', 'LID|bep|stan|rest'), ('officiële', 'ADJ|prenom|basis|met-e|stan'), ('taal', 'N|soort|ev|basis|zijd|stan'), ('van', 'VZ|init'), ('Suriname', 'N|eigen|ev|basis|onz|stan'), ('en', 'VG|neven'), ('een', 'TW|hoofd|nom|zonder-n|basis'), ('van', 'VZ|init'), ('de', 'LID|bep|stan|rest'), ('drie', 'TW|hoofd|prenom|stan'), ('officiële', 'ADJ|prenom|basis|met-e|stan'), ('talen', 'N|soort|mv|basis'), ('van', 'VZ|init'), ('België', 'N|eigen|ev|basis|onz|stan'), ('.', 'LET')],
        results_pos_tag_universal = [('Het', 'DET'), ('Nederlands', 'PROPN'), ('is', 'AUX'), ('een', 'DET'), ('West-Germaanse', 'ADJ'), ('taal', 'NOUN'), (',', 'PUNCT'), ('de', 'DET'), ('meest', 'ADV'), ('gebruikte', 'VERB'), ('taal', 'NOUN'), ('in', 'ADP'), ('Nederland', 'PROPN'), ('en', 'CCONJ'), ('België', 'PROPN'), (',', 'PUNCT'), ('de', 'DET'), ('officiële', 'ADJ'), ('taal', 'NOUN'), ('van', 'ADP'), ('Suriname', 'PROPN'), ('en', 'CCONJ'), ('een', 'NUM'), ('van', 'ADP'), ('de', 'DET'), ('drie', 'NUM'), ('officiële', 'ADJ'), ('talen', 'NOUN'), ('van', 'ADP'), ('België', 'PROPN'), ('.', 'PUNCT')],
        results_lemmatize = ['het', 'Nederlands', 'zijn', 'een', 'West-Germaans', 'taal', ',', 'de', 'veel', 'gebruiken', 'taal', 'in', 'Nederland', 'en', 'België', ',', 'de', 'officieel', 'taal', 'van', 'Suriname', 'en', 'één', 'van', 'de', 'drie', 'officieel', 'taal', 'van', 'België', '.'],
        results_dependency_parse = [('Het', 'Nederlands', 'det', 1), ('Nederlands', 'taal', 'nsubj', 4), ('is', 'taal', 'cop', 3), ('een', 'taal', 'det', 2), ('West-Germaanse', 'taal', 'amod', 1), ('taal', 'taal', 'ROOT', 0), (',', 'taal', 'punct', 4), ('de', 'taal', 'det', 3), ('meest', 'gebruikte', 'advmod', 1), ('gebruikte', 'taal', 'acl', 1), ('taal', 'taal', 'conj', -5), ('in', 'Nederland', 'case', 1), ('Nederland', 'taal', 'nmod', -2), ('en', 'België', 'cc', 1), ('België', 'Nederland', 'conj', -2), (',', 'taal', 'punct', 3), ('de', 'taal', 'det', 2), ('officiële', 'taal', 'amod', 1), ('taal', 'taal', 'conj', -13), ('van', 'Suriname', 'case', 1), ('Suriname', 'taal', 'nmod', -2), ('en', 'een', 'cc', 1), ('een', 'taal', 'conj', -17), ('van', 'talen', 'case', 4), ('de', 'talen', 'det', 3), ('drie', 'talen', 'nummod', 2), ('officiële', 'talen', 'amod', 1), ('talen', 'een', 'nmod', -5), ('van', 'België', 'case', 1), ('België', 'talen', 'nmod', -2), ('.', 'taal', 'punct', -25)]
    )

if __name__ == '__main__':
    test_spacy_nld()
