# ----------------------------------------------------------------------
# Tests: NLP - spaCy - German
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

def test_spacy_deu():
    test_spacy.wl_test_spacy(
        lang = 'deu_de',
        results_sentence_tokenize_trf = ['Das Deutsche ist eine plurizentrische Sprache, enthält also mehrere Standardvarietäten in verschiedenen Regionen.', 'Ihr Sprachgebiet umfasst Deutschland, Österreich, die Deutschschweiz, Liechtenstein, Luxemburg, Ostbelgien, Südtirol, das Elsass und Lothringen sowie Nordschleswig.', 'Außerdem ist Deutsch eine Minderheitensprache in einigen europäischen und außereuropäischen Ländern, z. B. in Rumänien und Südafrika sowie Nationalsprache im afrikanischen Namibia.', 'Deutsch ist die meistgesprochene Muttersprache in der Europäischen Union (EU).[26]'],
        results_word_tokenize = ['Das', 'Deutsche', 'ist', 'eine', 'plurizentrische', 'Sprache', ',', 'enthält', 'also', 'mehrere', 'Standardvarietäten', 'in', 'verschiedenen', 'Regionen', '.'],
        results_pos_tag = [('Das', 'ART'), ('Deutsche', 'NN'), ('ist', 'VAFIN'), ('eine', 'ART'), ('plurizentrische', 'ADJA'), ('Sprache', 'NN'), (',', '$,'), ('enthält', 'VVFIN'), ('also', 'ADV'), ('mehrere', 'PIAT'), ('Standardvarietäten', 'NN'), ('in', 'APPR'), ('verschiedenen', 'ADJA'), ('Regionen', 'NN'), ('.', '$.')],
        results_pos_tag_universal = [('Das', 'DET'), ('Deutsche', 'NOUN'), ('ist', 'AUX'), ('eine', 'DET'), ('plurizentrische', 'ADJ'), ('Sprache', 'NOUN'), (',', 'PUNCT'), ('enthält', 'VERB'), ('also', 'ADV'), ('mehrere', 'DET'), ('Standardvarietäten', 'NOUN'), ('in', 'ADP'), ('verschiedenen', 'ADJ'), ('Regionen', 'NOUN'), ('.', 'PUNCT')],
        results_lemmatize = ['der', 'deutsche', 'sein', 'ein', 'plurizentrisch', 'Sprache', '--', 'enthalten', 'also', 'mehrere', 'Standardvarietät', 'in', 'verschieden', 'Region', '--'],
        results_dependency_parse = [('Das', 'Deutsche', 'nk', 1), ('Deutsche', 'ist', 'sb', 1), ('ist', 'ist', 'ROOT', 0), ('eine', 'Sprache', 'nk', 2), ('plurizentrische', 'Sprache', 'nk', 1), ('Sprache', 'ist', 'pd', -3), (',', 'ist', 'punct', -4), ('enthält', 'ist', 'cj', -5), ('also', 'enthält', 'mo', -1), ('mehrere', 'Standardvarietäten', 'nk', 1), ('Standardvarietäten', 'enthält', 'oa', -3), ('in', 'Standardvarietäten', 'mnr', -1), ('verschiedenen', 'Regionen', 'nk', 1), ('Regionen', 'in', 'nk', -2), ('.', 'ist', 'punct', -12)]
    )

if __name__ == '__main__':
    test_spacy_deu()
