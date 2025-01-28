# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Afrikaans
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

def test_stanza_afr():
    test_stanza.wl_test_stanza(
        lang = 'afr',
        results_sentence_tokenize = ["Afrikaans is tipologies beskou 'n Indo-Europese, Wes-Germaanse, Nederfrankiese taal,[2] wat aan die suidpunt van Afrika onder invloed van verskeie ander tale en taalgroepe ontstaan het.", "Afrikaans is op 8 Mei 1925 as 'n amptelike taal van Suid-Afrika erken en is tans die derde jongste Germaanse taal wat amptelike status geniet, naas Faroëes wat in 1948 grondwetlik erken is en Luxemburgs wat hierdie status in 1984 verkry het."],
        results_word_tokenize = ['Afrikaans', 'is', 'tipologies', 'beskou', "'n", 'Indo-Europese', ',', 'Wes-Germaanse', ',', 'Nederfrankiese', 'taal', ',', '[2', ']', 'wat', 'aan', 'die', 'suidpunt', 'van', 'Afrika', 'onder', 'invloed', 'van', 'verskeie', 'ander', 'tale', 'en', 'taalgroepe', 'ontstaan', 'het', '.'],
        results_pos_tag = [('Afrikaans', 'NEE'), ('is', 'VTHOK'), ('tipologies', 'BS'), ('beskou', 'VTHOG'), ("'n", 'LO'), ('Indo-Europese', 'ASA'), (',', 'ZM'), ('Wes-Germaanse', 'ASA'), (',', 'ZM'), ('Nederfrankiese', 'ASA'), ('taal', 'NSE'), (',', 'ZM'), ('[2', 'RS'), (']', 'ZPR'), ('wat', 'PB'), ('aan', 'SVS'), ('die', 'LB'), ('suidpunt', 'NSE'), ('van', 'SVS'), ('Afrika', 'NEE'), ('onder', 'SVS'), ('invloed', 'NA'), ('van', 'SVS'), ('verskeie', 'ASA'), ('ander', 'ASA'), ('tale', 'NSM'), ('en', 'KN'), ('taalgroepe', 'NSM'), ('ontstaan', 'VTHOO'), ('het', 'VUOT'), ('.', 'ZE')],
        results_pos_tag_universal = [('Afrikaans', 'PROPN'), ('is', 'AUX'), ('tipologies', 'ADV'), ('beskou', 'VERB'), ("'n", 'DET'), ('Indo-Europese', 'ADJ'), (',', 'PUNCT'), ('Wes-Germaanse', 'ADJ'), (',', 'PUNCT'), ('Nederfrankiese', 'ADJ'), ('taal', 'NOUN'), (',', 'PUNCT'), ('[2', 'SYM'), (']', 'PUNCT'), ('wat', 'PRON'), ('aan', 'ADP'), ('die', 'DET'), ('suidpunt', 'NOUN'), ('van', 'ADP'), ('Afrika', 'PROPN'), ('onder', 'ADP'), ('invloed', 'NOUN'), ('van', 'ADP'), ('verskeie', 'ADJ'), ('ander', 'ADJ'), ('tale', 'NOUN'), ('en', 'CCONJ'), ('taalgroepe', 'NOUN'), ('ontstaan', 'VERB'), ('het', 'AUX'), ('.', 'PUNCT')],
        results_lemmatize = ['Afrikaans', 'wees', 'tipologies', 'beskou', "'n", 'indo-Europes', ',', 'Wes-sermaans', ',', 'nederfrankies', 'taal', ',', '[2', ']', 'wat', 'aan', 'die', 'suidpunt', 'van', 'Afrika', 'onder', 'invloed', 'van', 'verskeie', 'ander', 'taal', 'en', 'taalgroep', 'ontstaan', 'het', '.'],
        results_dependency_parse = [('Afrikaans', 'beskou', 'nsubj:pass', 3), ('is', 'beskou', 'aux:pass', 2), ('tipologies', 'beskou', 'advmod', 1), ('beskou', 'beskou', 'root', 0), ("'n", 'taal', 'det', 6), ('Indo-Europese', 'taal', 'amod', 5), (',', 'Indo-Europese', 'punct', -1), ('Wes-Germaanse', 'Indo-Europese', 'conj', -2), (',', 'Wes-Germaanse', 'punct', -1), ('Nederfrankiese', 'Wes-Germaanse', 'conj', -2), ('taal', 'beskou', 'obj', -7), (',', '[2', 'punct', 1), ('[2', 'taal', 'appos', -2), (']', '[2', 'punct', -1), ('wat', 'ontstaan', 'nsubj', 14), ('aan', 'suidpunt', 'case', 2), ('die', 'suidpunt', 'det', 1), ('suidpunt', 'ontstaan', 'obl', 11), ('van', 'Afrika', 'case', 1), ('Afrika', 'suidpunt', 'nmod', -2), ('onder', 'invloed', 'case', 1), ('invloed', 'ontstaan', 'obl', 7), ('van', 'tale', 'case', 3), ('verskeie', 'tale', 'amod', 2), ('ander', 'tale', 'amod', 1), ('tale', 'invloed', 'nmod', -4), ('en', 'tale', 'cc', -1), ('taalgroepe', 'tale', 'conj', -2), ('ontstaan', 'beskou', 'ccomp', -25), ('het', 'ontstaan', 'aux', -1), ('.', 'ontstaan', 'punct', -2)]
    )

if __name__ == '__main__':
    test_stanza_afr()
