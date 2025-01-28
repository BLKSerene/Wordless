# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Polish
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

def test_stanza_pol():
    test_stanza.wl_test_stanza(
        lang = 'pol',
        results_sentence_tokenize = ['Język polski, polszczyzna – język z grupy zachodniosłowiańskiej (do której należą również czeski, kaszubski, słowacki i języki łużyckie), stanowiącej część rodziny indoeuropejskiej.', 'Jest językiem urzędowym w Polsce oraz należy do oficjalnych języków Unii Europejskiej.'],
        results_word_tokenize = ['Język', 'polski', ',', 'polszczyzna', '–', 'język', 'z', 'grupy', 'zachodniosłowiańskiej', '(', 'do', 'której', 'należą', 'również', 'czeski', ',', 'kaszubski', ',', 'słowacki', 'i', 'języki', 'łużyckie', ')', ',', 'stanowiącej', 'część', 'rodziny', 'indoeuropejskiej', '.'],
        results_pos_tag = [('Język', 'subst:sg:nom:m3'), ('polski', 'adj:sg:nom:m3:pos'), (',', 'interp'), ('polszczyzna', 'subst:sg:nom:f'), ('–', 'interp'), ('język', 'subst:sg:nom:m3'), ('z', 'prep:gen:nwok'), ('grupy', 'subst:sg:gen:f'), ('zachodniosłowiańskiej', 'adj:sg:gen:f:pos'), ('(', 'interp'), ('do', 'prep:gen'), ('której', 'adj:sg:gen:f:pos'), ('należą', 'fin:pl:ter:imperf'), ('również', 'part'), ('czeski', 'adj:sg:nom:m3:pos'), (',', 'interp'), ('kaszubski', 'adj:sg:nom:m3:pos'), (',', 'interp'), ('słowacki', 'adj:sg:nom:m3:pos'), ('i', 'conj'), ('języki', 'subst:pl:nom:m3'), ('łużyckie', 'adj:pl:nom:m3:pos'), (')', 'interp'), (',', 'interp'), ('stanowiącej', 'pact:sg:gen:f:imperf:aff'), ('część', 'subst:sg:acc:f'), ('rodziny', 'subst:sg:gen:f'), ('indoeuropejskiej', 'adj:sg:gen:f:pos'), ('.', 'interp')],
        results_pos_tag_universal = [('Język', 'NOUN'), ('polski', 'ADJ'), (',', 'PUNCT'), ('polszczyzna', 'NOUN'), ('–', 'PUNCT'), ('język', 'NOUN'), ('z', 'ADP'), ('grupy', 'NOUN'), ('zachodniosłowiańskiej', 'ADJ'), ('(', 'PUNCT'), ('do', 'ADP'), ('której', 'DET'), ('należą', 'VERB'), ('również', 'PART'), ('czeski', 'ADJ'), (',', 'PUNCT'), ('kaszubski', 'ADJ'), (',', 'PUNCT'), ('słowacki', 'ADJ'), ('i', 'CCONJ'), ('języki', 'NOUN'), ('łużyckie', 'ADJ'), (')', 'PUNCT'), (',', 'PUNCT'), ('stanowiącej', 'ADJ'), ('część', 'NOUN'), ('rodziny', 'NOUN'), ('indoeuropejskiej', 'ADJ'), ('.', 'PUNCT')],
        results_lemmatize = ['język', 'polski', ',', 'polszczyzna', '–', 'język', 'z', 'grupa', 'zachodniosłowiański', '(', 'do', 'który', 'należeć', 'również', 'czeski', ',', 'kaszubski', ',', 'słowacki', 'i', 'język', 'łużycki', ')', ',', 'stanowić', 'część', 'rodzina', 'indoeuropejski', '.'],
        results_dependency_parse = [('Język', 'Język', 'root', 0), ('polski', 'Język', 'amod', -1), (',', 'polszczyzna', 'punct', 1), ('polszczyzna', 'Język', 'conj', -3), ('–', 'język', 'punct', 1), ('język', 'Język', 'conj', -5), ('z', 'grupy', 'case', 1), ('grupy', 'język', 'nmod', -2), ('zachodniosłowiańskiej', 'grupy', 'amod', -1), ('(', 'należą', 'punct', 3), ('do', 'której', 'case', 1), ('której', 'należą', 'obl:arg', 1), ('należą', 'grupy', 'acl:relcl', -5), ('również', 'czeski', 'advmod:emph', 1), ('czeski', 'należą', 'nsubj', -2), (',', 'kaszubski', 'punct', 1), ('kaszubski', 'czeski', 'conj', -2), (',', 'słowacki', 'punct', 1), ('słowacki', 'czeski', 'conj', -4), ('i', 'języki', 'cc', 1), ('języki', 'czeski', 'conj', -6), ('łużyckie', 'języki', 'amod', -1), (')', 'należą', 'punct', -10), (',', 'stanowiącej', 'punct', 1), ('stanowiącej', 'grupy', 'acl', -17), ('część', 'stanowiącej', 'xcomp:pred', -1), ('rodziny', 'część', 'nmod:arg', -1), ('indoeuropejskiej', 'rodziny', 'amod', -1), ('.', 'Język', 'punct', -28)]
    )

if __name__ == '__main__':
    test_stanza_pol()
