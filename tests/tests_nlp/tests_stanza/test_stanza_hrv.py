# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Croatian
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

def test_stanza_hrv():
    test_stanza.wl_test_stanza(
        lang = 'hrv',
        results_sentence_tokenize = ['Hrvatski jezik (ISO 639-3: hrv) skupni je naziv za nacionalni standardni jezik Hrvata, te za skup narječja i govora kojima govore ili su nekada govorili Hrvati.', 'Njime govori više od 5,5 milijuna ljudi,[2] poglavito Hrvata u Hrvatskoj, 3\u202f980\u202f000 (popis iz 2001.) i Bosni i Hercegovini, 469\u202f000 (2004.).[', '3] Hrvatski je materinski jezik za Hrvate u drugim zemljama: Sjedinjenim Američkim Državama, 58\u202f400 (popis iz 2000.);[1] Austriji, 19\u202f400 (popis iz 2001.); Srbiji, 19\u202f223 (popis iz 2011.);[4] Mađarskoj, 14\u202f300 (popis iz 2001.); Italiji, 3500 (Vincent 1987.); Crnoj Gori, 6810 (2006.); Slovačkoj, 890 (popis iz 2001.).'],
        results_word_tokenize = ['Hrvatski', 'jezik', '(', 'ISO', '639-3', ':', 'hrv', ')', 'skupni', 'je', 'naziv', 'za', 'nacionalni', 'standardni', 'jezik', 'Hrvata', ',', 'te', 'za', 'skup', 'narječja', 'i', 'govora', 'kojima', 'govore', 'ili', 'su', 'nekada', 'govorili', 'Hrvati', '.'],
        results_pos_tag = [('Hrvatski', 'Agpmsny'), ('jezik', 'Ncmsn'), ('(', 'Z'), ('ISO', 'Xf'), ('639-3', 'Mdc'), (':', 'Z'), ('hrv', 'Xf'), (')', 'Z'), ('skupni', 'Agpmsny'), ('je', 'Var3s'), ('naziv', 'Ncmsn'), ('za', 'Sa'), ('nacionalni', 'Agpmsayn'), ('standardni', 'Agpmsayn'), ('jezik', 'Ncmsan'), ('Hrvata', 'Npmpg'), (',', 'Z'), ('te', 'Cc'), ('za', 'Sa'), ('skup', 'Ncmsan'), ('narječja', 'Ncnsg'), ('i', 'Cc'), ('govora', 'Ncmsg'), ('kojima', 'Pi-mpd'), ('govore', 'Vmr3p'), ('ili', 'Cc'), ('su', 'Var3p'), ('nekada', 'Rgp'), ('govorili', 'Vmp-pm'), ('Hrvati', 'Npmpn'), ('.', 'Z')],
        results_pos_tag_universal = [('Hrvatski', 'ADJ'), ('jezik', 'NOUN'), ('(', 'PUNCT'), ('ISO', 'X'), ('639-3', 'NUM'), (':', 'PUNCT'), ('hrv', 'X'), (')', 'PUNCT'), ('skupni', 'ADJ'), ('je', 'AUX'), ('naziv', 'NOUN'), ('za', 'ADP'), ('nacionalni', 'ADJ'), ('standardni', 'ADJ'), ('jezik', 'NOUN'), ('Hrvata', 'PROPN'), (',', 'PUNCT'), ('te', 'CCONJ'), ('za', 'ADP'), ('skup', 'NOUN'), ('narječja', 'NOUN'), ('i', 'CCONJ'), ('govora', 'NOUN'), ('kojima', 'DET'), ('govore', 'VERB'), ('ili', 'CCONJ'), ('su', 'AUX'), ('nekada', 'ADV'), ('govorili', 'VERB'), ('Hrvati', 'PROPN'), ('.', 'PUNCT')],
        results_lemmatize = ['hrvatski', 'jezik', '(', 'iso', '639-3', ':', 'hrv', ')', 'skupni', 'biti', 'naziv', 'za', 'nacionalan', 'standardan', 'jezik', 'Hrvat', ',', 'te', 'za', 'skup', 'narječje', 'i', 'govor', 'koji', 'govoriti', 'ili', 'biti', 'nekada', 'govoriti', 'Hrvat', '.'],
        results_dependency_parse = [('Hrvatski', 'jezik', 'amod', 1), ('jezik', 'naziv', 'nsubj', 9), ('(', 'ISO', 'punct', 1), ('ISO', 'jezik', 'appos', -2), ('639-3', 'ISO', 'flat', -1), (':', 'ISO', 'punct', -2), ('hrv', 'ISO', 'flat:foreign', -3), (')', 'ISO', 'punct', -4), ('skupni', 'naziv', 'amod', 2), ('je', 'naziv', 'cop', 1), ('naziv', 'naziv', 'root', 0), ('za', 'jezik', 'case', 3), ('nacionalni', 'jezik', 'amod', 2), ('standardni', 'jezik', 'amod', 1), ('jezik', 'naziv', 'nmod', -4), ('Hrvata', 'jezik', 'nmod', -1), (',', 'skup', 'punct', 3), ('te', 'skup', 'cc', 2), ('za', 'skup', 'case', 1), ('skup', 'jezik', 'conj', -5), ('narječja', 'skup', 'nmod', -1), ('i', 'govora', 'cc', 1), ('govora', 'narječja', 'conj', -2), ('kojima', 'govore', 'obj', 1), ('govore', 'govora', 'acl', -2), ('ili', 'govorili', 'cc', 3), ('su', 'govorili', 'aux', 2), ('nekada', 'govorili', 'advmod', 1), ('govorili', 'govore', 'conj', -4), ('Hrvati', 'govorili', 'nsubj', -1), ('.', 'naziv', 'punct', -20)]
    )

if __name__ == '__main__':
    test_stanza_hrv()
