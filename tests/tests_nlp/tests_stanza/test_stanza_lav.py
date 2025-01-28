# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Latvian
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

def test_stanza_lav():
    test_stanza.wl_test_stanza(
        lang = 'lav',
        results_sentence_tokenize = ['Latviešu valoda ir dzimtā valoda apmēram 1,5 miljoniem cilvēku, galvenokārt Latvijā, kur tā ir vienīgā valsts valoda.', '[1][3] Lielākās latviešu valodas pratēju kopienas ārpus Latvijas ir Apvienotajā Karalistē, ASV, Īrijā, Austrālijā, Vācijā, Zviedrijā, Kanādā, Brazīlijā, Krievijas Federācijā.', 'Latviešu valoda pieder pie indoeiropiešu valodu saimes baltu valodu grupas.', 'Senākie rakstu paraugi latviešu valodā — jau no 15. gadsimta — ir atrodami Jāņa ģildes alus nesēju biedrības grāmatās.', 'Tajā lielākoties bija latvieši, un no 1517. gada arī brālības vecākie bija latvieši.', 'Pirmais teksts latviski iespiests 1507. gadā izdotajā baznīcas rokasgrāmatā „AGENDA”.', '[4]'],
        results_word_tokenize = ['Latviešu', 'valoda', 'ir', 'dzimtā', 'valoda', 'apmēram', '1,5', 'miljoniem', 'cilvēku', ',', 'galvenokārt', 'Latvijā', ',', 'kur', 'tā', 'ir', 'vienīgā', 'valsts', 'valoda', '.', '[', '1', ']', '[', '3', ']'],
        results_pos_tag = [('Latviešu', 'ncmpg2'), ('valoda', 'ncfsn4'), ('ir', 'vcnipii30an'), ('dzimtā', 'vmnpdfsnpsypn'), ('valoda', 'ncfsn4'), ('apmēram', 'r0qn'), ('1,5', 'xn'), ('miljoniem', 'ncmpd1'), ('cilvēku', 'ncmpg1'), (',', 'zc'), ('galvenokārt', 'r0mn'), ('Latvijā', 'npfsl4'), (',', 'zc'), ('kur', 'r0pn'), ('tā', 'pd3fsnn'), ('ir', 'vcnipii30an'), ('vienīgā', 'affsnyp'), ('valsts', 'ncfsg6'), ('valoda', 'ncfsn4'), ('.', 'zs'), ('[', 'zb'), ('1', 'xn'), (']', 'zb'), ('[', 'zb'), ('3', 'xn'), (']', 'zb')],
        results_pos_tag_universal = [('Latviešu', 'NOUN'), ('valoda', 'NOUN'), ('ir', 'AUX'), ('dzimtā', 'VERB'), ('valoda', 'NOUN'), ('apmēram', 'ADV'), ('1,5', 'NUM'), ('miljoniem', 'NOUN'), ('cilvēku', 'NOUN'), (',', 'PUNCT'), ('galvenokārt', 'ADV'), ('Latvijā', 'PROPN'), (',', 'PUNCT'), ('kur', 'ADV'), ('tā', 'PRON'), ('ir', 'AUX'), ('vienīgā', 'ADJ'), ('valsts', 'NOUN'), ('valoda', 'NOUN'), ('.', 'PUNCT'), ('[', 'PUNCT'), ('1', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('3', 'NUM'), (']', 'PUNCT')],
        results_lemmatize = ['latvietis', 'valoda', 'būt', 'dzimt', 'valoda', 'apmēram', '1,5', 'miljons', 'cilvēks', ',', 'galvenokārt', 'Latvija', ',', 'kur', 'tā', 'būt', 'vienīgs', 'valsts', 'valoda', '.', '[', '1', ']', '[', '3', ']'],
        results_dependency_parse = [('Latviešu', 'valoda', 'nmod', 1), ('valoda', 'valoda', 'nsubj', 3), ('ir', 'valoda', 'cop', 2), ('dzimtā', 'valoda', 'amod', 1), ('valoda', 'valoda', 'root', 0), ('apmēram', '1,5', 'advmod', 1), ('1,5', 'miljoniem', 'nummod', 1), ('miljoniem', 'valoda', 'nmod', -3), ('cilvēku', 'miljoniem', 'nmod', -1), (',', 'Latvijā', 'punct', 2), ('galvenokārt', 'Latvijā', 'advmod', 1), ('Latvijā', 'valoda', 'conj', -7), (',', 'valoda', 'punct', 6), ('kur', 'valoda', 'advmod', 5), ('tā', 'valoda', 'nsubj', 4), ('ir', 'valoda', 'cop', 3), ('vienīgā', 'valoda', 'amod', 2), ('valsts', 'valoda', 'nmod', 1), ('valoda', 'Latvijā', 'acl', -7), ('.', 'valoda', 'punct', -15), ('[', '1', 'punct', 1), ('1', '1', 'root', 0), (']', '1', 'punct', -1), ('[', '3', 'punct', 1), ('3', '1', 'dep', -3), (']', '3', 'punct', -1)]
    )

if __name__ == '__main__':
    test_stanza_lav()
