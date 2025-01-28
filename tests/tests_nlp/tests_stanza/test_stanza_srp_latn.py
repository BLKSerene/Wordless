# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Serbian (Latin script)
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

def test_stanza_srp_latn():
    test_stanza.wl_test_stanza(
        lang = 'srp_latn',
        results_sentence_tokenize = ['Srpski jezik je zvaničan u Srbiji, Bosni i Hercegovini i Crnoj Gori i govori ga oko 12 miliona ljudi.[13]', 'Takođe je manjinski jezik u državama centralne i istočne Evrope.[13]'],
        results_word_tokenize = ['Srpski', 'jezik', 'je', 'zvaničan', 'u', 'Srbiji', ',', 'Bosni', 'i', 'Hercegovini', 'i', 'Crnoj', 'Gori', 'i', 'govori', 'ga', 'oko', '12', 'miliona', 'ljudi', '.[', '13]'],
        results_pos_tag = [('Srpski', 'Agpmsny'), ('jezik', 'Ncmsn'), ('je', 'Var3s'), ('zvaničan', 'Agpmsnn'), ('u', 'Sl'), ('Srbiji', 'Npfsl'), (',', 'Z'), ('Bosni', 'Npfsl'), ('i', 'Cc'), ('Hercegovini', 'Npfsl'), ('i', 'Cc'), ('Crnoj', 'Agpfsly'), ('Gori', 'Ncfsl'), ('i', 'Cc'), ('govori', 'Vmr3s'), ('ga', 'Pp3msa'), ('oko', 'Rgp'), ('12', 'Mdc'), ('miliona', 'Ncmpg'), ('ljudi', 'Ncmpg'), ('.[', 'Z'), ('13]', 'Mdm')],
        results_pos_tag_universal = [('Srpski', 'ADJ'), ('jezik', 'NOUN'), ('je', 'AUX'), ('zvaničan', 'ADJ'), ('u', 'ADP'), ('Srbiji', 'PROPN'), (',', 'PUNCT'), ('Bosni', 'PROPN'), ('i', 'CCONJ'), ('Hercegovini', 'PROPN'), ('i', 'CCONJ'), ('Crnoj', 'ADJ'), ('Gori', 'NOUN'), ('i', 'CCONJ'), ('govori', 'VERB'), ('ga', 'PRON'), ('oko', 'ADV'), ('12', 'NUM'), ('miliona', 'NOUN'), ('ljudi', 'NOUN'), ('.[', 'PUNCT'), ('13]', 'NUM')],
        results_lemmatize = ['srpski', 'jezik', 'biti', 'zvaničan', 'u', 'Srbija', ',', 'Bosna', 'i', 'Hercegovina', 'i', 'crn', 'gora', 'i', 'govoriti', 'on', 'oko', '12', 'milion', 'čovek', '.[', '13]'],
        results_dependency_parse = [('Srpski', 'jezik', 'amod', 1), ('jezik', 'zvaničan', 'nsubj', 2), ('je', 'zvaničan', 'cop', 1), ('zvaničan', 'zvaničan', 'root', 0), ('u', 'Srbiji', 'case', 1), ('Srbiji', 'zvaničan', 'obl', -2), (',', 'Bosni', 'punct', 1), ('Bosni', 'Srbiji', 'conj', -2), ('i', 'Bosni', 'flat', -1), ('Hercegovini', 'Bosni', 'flat', -2), ('i', 'Crnoj', 'cc', 1), ('Crnoj', 'Gori', 'amod', 1), ('Gori', 'Srbiji', 'conj', -7), ('i', 'govori', 'cc', 1), ('govori', 'zvaničan', 'conj', -11), ('ga', 'govori', 'obj', -1), ('oko', '12', 'advmod', 1), ('12', 'ljudi', 'nummod:gov', 2), ('miliona', '12', 'flat', -1), ('ljudi', 'govori', 'obl', -5), ('.[', '13]', 'case', 1), ('13]', 'govori', 'obl', -7)]
    )

if __name__ == '__main__':
    test_stanza_srp_latn()
