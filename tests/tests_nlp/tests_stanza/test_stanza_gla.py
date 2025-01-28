# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Scottish Gaelic
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

def test_stanza_gla():
    test_stanza.wl_test_stanza(
        lang = 'gla',
        results_sentence_tokenize = ["'S i cànan dùthchasach na h-Alba a th' anns a' Ghàidhlig.", "'S i ball den teaghlach de chànanan Ceilteach dhen mheur Ghoidhealach a tha anns a' Ghàidhlig.", 'Tha Goidhealach a\' gabhail a-steach na cànanan Gàidhealach gu lèir; Gàidhlig na h-Èireann, Gàidhlig Mhanainn, agus Gàidhlig agus gu dearbh chan eil anns an fhacal "Goidhealach" ach seann fhacal a tha a\' ciallachadh "Gàidhealach".'],
        results_word_tokenize = ["'S", 'i', 'cànan', 'dùthchasach', 'na', 'h-Alba', 'a', "th'", 'anns', "a'", 'Ghàidhlig', '.'],
        results_pos_tag = [("'S", 'Wp-i'), ('i', 'Pp3sf'), ('cànan', 'Ncsmn'), ('dùthchasach', 'Aq-smn'), ('na', 'Tdsfg'), ('h-Alba', 'Nt'), ('a', 'Q-r'), ("th'", 'V-p'), ('anns', 'Sp'), ("a'", 'Tdsf'), ('Ghàidhlig', 'Ncsfd'), ('.', 'Fe')],
        results_pos_tag_universal = [("'S", 'AUX'), ('i', 'PRON'), ('cànan', 'NOUN'), ('dùthchasach', 'ADJ'), ('na', 'DET'), ('h-Alba', 'PROPN'), ('a', 'PART'), ("th'", 'VERB'), ('anns', 'ADP'), ("a'", 'DET'), ('Ghàidhlig', 'NOUN'), ('.', 'PUNCT')],
        results_lemmatize = ['is', 'i', 'cànan', 'dùthchasach', 'an', 'Alba', 'a', 'bi', 'an', 'an', 'gàidhlig', '.'],
        results_dependency_parse = [("'S", 'cànan', 'cop', 2), ('i', "'S", 'fixed', -1), ('cànan', 'cànan', 'root', 0), ('dùthchasach', 'cànan', 'amod', -1), ('na', 'h-Alba', 'det', 1), ('h-Alba', 'cànan', 'nmod', -3), ('a', "th'", 'nsubj', 1), ("th'", 'cànan', 'csubj:cleft', -5), ('anns', 'Ghàidhlig', 'case', 2), ("a'", 'Ghàidhlig', 'det', 1), ('Ghàidhlig', "th'", 'xcomp:pred', -3), ('.', 'cànan', 'punct', -9)]
    )

if __name__ == '__main__':
    test_stanza_gla()
