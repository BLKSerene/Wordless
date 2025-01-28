# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Icelandic
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

def test_stanza_isl():
    test_stanza.wl_test_stanza(
        lang = 'isl',
        results_sentence_tokenize = ['Íslenska er vesturnorrænt, germanskt og indóevrópskt tungumál sem er einkum talað og ritað á Íslandi og er móðurmál langflestra Íslendinga.', '[5] Það hefur tekið minni breytingum frá fornnorrænu en önnur norræn mál[5] og er skyldara norsku og færeysku en sænsku og dönsku.', '[2][3]'],
        results_word_tokenize = ['Íslenska', 'er', 'vesturnorrænt', ',', 'germanskt', 'og', 'indóevrópskt', 'tungumál', 'sem', 'er', 'einkum', 'talað', 'og', 'ritað', 'á', 'Íslandi', 'og', 'er', 'móðurmál', 'langflestra', 'Íslendinga', '.', '[5', ']'],
        results_pos_tag = [('Íslenska', 'ADJ-N'), ('er', 'BEPI'), ('vesturnorrænt', 'N-N'), (',', ','), ('germanskt', 'N-N'), ('og', 'CONJ'), ('indóevrópskt', 'ADJ-N'), ('tungumál', 'NSN'), ('sem', 'C'), ('er', 'BEPI'), ('einkum', 'ADV'), ('talað', 'VAN'), ('og', 'CONJ'), ('ritað', 'VAN'), ('á', 'P'), ('Íslandi', 'NPR-D'), ('og', 'CONJ'), ('er', 'BEPI'), ('móðurmál', 'N-N'), ('langflestra', 'QS-G'), ('Íslendinga', 'NPRS-G'), ('.', '.'), ('[5', 'NUM-N'), (']', 'INTJ')],
        results_pos_tag_universal = [('Íslenska', 'ADJ'), ('er', 'AUX'), ('vesturnorrænt', 'NOUN'), (',', 'PUNCT'), ('germanskt', 'NOUN'), ('og', 'CCONJ'), ('indóevrópskt', 'ADJ'), ('tungumál', 'NOUN'), ('sem', 'SCONJ'), ('er', 'AUX'), ('einkum', 'ADV'), ('talað', 'VERB'), ('og', 'CCONJ'), ('ritað', 'VERB'), ('á', 'ADP'), ('Íslandi', 'PROPN'), ('og', 'CCONJ'), ('er', 'AUX'), ('móðurmál', 'NOUN'), ('langflestra', 'DET'), ('Íslendinga', 'PROPN'), ('.', 'PUNCT'), ('[5', 'NUM'), (']', 'INTJ')],
        results_lemmatize = ['íslenskur', 'vera', 'vesturnorrænt', ',', 'germanskt', 'og', 'indóevrópskur', 'tungumál', 'sem', 'vera', 'einkum', 'tala', 'og', 'rita', 'á', 'ísland', 'og', 'vera', 'móðurmál', 'langflestur', 'íslendingur', '.', '[5', ']'],
        results_dependency_parse = [('Íslenska', 'Íslenska', 'root', 0), ('er', 'Íslenska', 'cop', -1), ('vesturnorrænt', 'Íslenska', 'nsubj', -2), (',', 'germanskt', 'punct', 1), ('germanskt', 'vesturnorrænt', 'conj', -2), ('og', 'tungumál', 'cc', 2), ('indóevrópskt', 'tungumál', 'amod', 1), ('tungumál', 'vesturnorrænt', 'conj', -5), ('sem', 'talað', 'mark', 3), ('er', 'talað', 'cop', 2), ('einkum', 'talað', 'advmod', 1), ('talað', 'tungumál', 'acl:relcl', -4), ('og', 'talað', 'cc', -1), ('ritað', 'talað', 'xcomp', -2), ('á', 'Íslandi', 'case', 1), ('Íslandi', 'talað', 'obl', -4), ('og', 'móðurmál', 'cc', 2), ('er', 'móðurmál', 'cop', 1), ('móðurmál', 'Íslenska', 'conj', -18), ('langflestra', 'Íslendinga', 'amod', 1), ('Íslendinga', 'móðurmál', 'nmod:poss', -2), ('.', 'Íslendinga', 'punct', -1), ('[5', '[5', 'root', 0), (']', '[5', 'discourse', -1)]
    )

if __name__ == '__main__':
    test_stanza_isl()
