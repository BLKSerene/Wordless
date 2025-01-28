# ----------------------------------------------------------------------
# Tests: NLP - Stanza - German
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

def test_stanza_deu():
    test_stanza.wl_test_stanza(
        lang = 'deu_de',
        results_sentence_tokenize = ['Das Deutsche ist eine plurizentrische Sprache, enthält also mehrere Standardvarietäten in verschiedenen Regionen.', 'Ihr Sprachgebiet umfasst Deutschland, Österreich, die Deutschschweiz, Liechtenstein, Luxemburg, Ostbelgien, Südtirol, das Elsass und Lothringen sowie Nordschleswig.', 'Außerdem ist Deutsch eine Minderheitensprache in einigen europäischen und außereuropäischen Ländern, z. B. in Rumänien und Südafrika sowie Nationalsprache im afrikanischen Namibia.', 'Deutsch ist die meistgesprochene Muttersprache in der Europäischen Union (EU).', '[26]'],
        results_word_tokenize = ['Das', 'Deutsche', 'ist', 'eine', 'plurizentrische', 'Sprache', ',', 'enthält', 'also', 'mehrere', 'Standardvarietäten', 'in', 'verschiedenen', 'Regionen', '.'],
        results_pos_tag = [('Das', 'ART'), ('Deutsche', 'NN'), ('ist', 'VAFIN'), ('eine', 'ART'), ('plurizentrische', 'ADJA'), ('Sprache', 'NN'), (',', '$,'), ('enthält', 'VVFIN'), ('also', 'ADV'), ('mehrere', 'PIAT'), ('Standardvarietäten', 'NN'), ('in', 'APPR'), ('verschiedenen', 'ADJA'), ('Regionen', 'NN'), ('.', '$.')],
        results_pos_tag_universal = [('Das', 'DET'), ('Deutsche', 'PROPN'), ('ist', 'AUX'), ('eine', 'DET'), ('plurizentrische', 'ADJ'), ('Sprache', 'NOUN'), (',', 'PUNCT'), ('enthält', 'VERB'), ('also', 'ADV'), ('mehrere', 'DET'), ('Standardvarietäten', 'NOUN'), ('in', 'ADP'), ('verschiedenen', 'ADJ'), ('Regionen', 'NOUN'), ('.', 'PUNCT')],
        results_lemmatize = ['der', 'deutsch', 'sein', 'ein', 'plurizentrisch', 'Sprache', ',', 'enthalten', 'also', 'mehr', 'Standardvarietät', 'in', 'verschieden', 'Region', '.'],
        results_dependency_parse = [('Das', 'Deutsche', 'det', 1), ('Deutsche', 'Sprache', 'nsubj', 4), ('ist', 'Sprache', 'cop', 3), ('eine', 'Sprache', 'det', 2), ('plurizentrische', 'Sprache', 'amod', 1), ('Sprache', 'Sprache', 'root', 0), (',', 'enthält', 'punct', 1), ('enthält', 'Sprache', 'conj', -2), ('also', 'enthält', 'advmod', -1), ('mehrere', 'Standardvarietäten', 'det', 1), ('Standardvarietäten', 'enthält', 'obj', -3), ('in', 'Regionen', 'case', 2), ('verschiedenen', 'Regionen', 'amod', 1), ('Regionen', 'Standardvarietäten', 'nmod', -3), ('.', 'Sprache', 'punct', -9)],
        results_sentiment_analayze = [0]
    )

if __name__ == '__main__':
    test_stanza_deu()
