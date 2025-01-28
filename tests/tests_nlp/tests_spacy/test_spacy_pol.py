# ----------------------------------------------------------------------
# Tests: NLP - spaCy - Polish
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

def test_spacy_pol():
    results_sentence_tokenize = ['Język polski, polszczyzna – język z grupy zachodniosłowiańskiej (do której należą również czeski, kaszubski, słowacki i języki łużyckie), stanowiącej część rodziny indoeuropejskiej.', 'Jest językiem urzędowym w Polsce oraz należy do oficjalnych języków Unii Europejskiej.']

    test_spacy.wl_test_spacy(
        lang = 'pol',
        results_sentence_tokenize_trf = results_sentence_tokenize,
        results_sentence_tokenize_lg = results_sentence_tokenize,
        results_word_tokenize = ['Język', 'polski', ',', 'polszczyzna', '–', 'język', 'z', 'grupy', 'zachodniosłowiańskiej', '(', 'do', 'której', 'należą', 'również', 'czeski', ',', 'kaszubski', ',', 'słowacki', 'i', 'języki', 'łużyckie', ')', ',', 'stanowiącej', 'część', 'rodziny', 'indoeuropejskiej', '.'],
        results_pos_tag = [('Język', 'SUBST'), ('polski', 'ADJ'), (',', 'INTERP'), ('polszczyzna', 'SUBST'), ('–', 'INTERP'), ('język', 'SUBST'), ('z', 'PREP'), ('grupy', 'SUBST'), ('zachodniosłowiańskiej', 'ADJ'), ('(', 'INTERP'), ('do', 'PREP'), ('której', 'ADJ'), ('należą', 'FIN'), ('również', 'QUB'), ('czeski', 'ADJ'), (',', 'INTERP'), ('kaszubski', 'ADJ'), (',', 'INTERP'), ('słowacki', 'ADJ'), ('i', 'CONJ'), ('języki', 'SUBST'), ('łużyckie', 'ADJ'), (')', 'SUBST'), (',', 'INTERP'), ('stanowiącej', 'PACT'), ('część', 'SUBST'), ('rodziny', 'SUBST'), ('indoeuropejskiej', 'ADJ'), ('.', 'SUBST')],
        results_pos_tag_universal = [('Język', 'NOUN'), ('polski', 'ADJ'), (',', 'PUNCT'), ('polszczyzna', 'NOUN'), ('–', 'PUNCT'), ('język', 'NOUN'), ('z', 'ADP'), ('grupy', 'NOUN'), ('zachodniosłowiańskiej', 'ADJ'), ('(', 'PUNCT'), ('do', 'ADP'), ('której', 'DET'), ('należą', 'VERB'), ('również', 'PART'), ('czeski', 'ADJ'), (',', 'PUNCT'), ('kaszubski', 'ADJ'), (',', 'PUNCT'), ('słowacki', 'ADJ'), ('i', 'CCONJ'), ('języki', 'NOUN'), ('łużyckie', 'ADJ'), (')', 'PUNCT'), (',', 'PUNCT'), ('stanowiącej', 'ADJ'), ('część', 'NOUN'), ('rodziny', 'NOUN'), ('indoeuropejskiej', 'ADJ'), ('.', 'PUNCT')],
        results_lemmatize = ['Język', 'polski', ',', 'polszczyzna', '–', 'język', 'z', 'grupa', 'zachodniosłowiański', '(', 'do', 'który', 'należeć', 'również', 'czeski', ',', 'kaszubski', ',', 'słowacki', 'i', 'język', 'łużycki', ')', ',', 'stanowić', 'część', 'rodzina', 'indoeuropejski', '.'],
        results_dependency_parse = [('Język', 'Język', 'ROOT', 0), ('polski', 'Język', 'amod', -1), (',', 'polszczyzna', 'punct', 1), ('polszczyzna', 'Język', 'conj', -3), ('–', 'język', 'punct', 1), ('język', 'Język', 'conj', -5), ('z', 'grupy', 'case', 1), ('grupy', 'język', 'nmod', -2), ('zachodniosłowiańskiej', 'grupy', 'amod', -1), ('(', 'należą', 'punct', 3), ('do', 'której', 'case', 1), ('której', 'należą', 'obl:arg', 1), ('należą', 'Język', 'parataxis:insert', -12), ('również', 'czeski', 'advmod:emph', 1), ('czeski', 'należą', 'nsubj', -2), (',', 'kaszubski', 'punct', 1), ('kaszubski', 'czeski', 'conj', -2), (',', 'słowacki', 'punct', 1), ('słowacki', 'czeski', 'conj', -4), ('i', 'języki', 'cc', 1), ('języki', 'czeski', 'conj', -6), ('łużyckie', 'języki', 'amod', -1), (')', 'należą', 'punct', -10), (',', 'stanowiącej', 'punct', 1), ('stanowiącej', 'Język', 'acl', -24), ('część', 'stanowiącej', 'xcomp:pred', -1), ('rodziny', 'część', 'nmod:arg', -1), ('indoeuropejskiej', 'rodziny', 'amod', -1), ('.', 'Język', 'punct', -28)]
    )

if __name__ == '__main__':
    test_spacy_pol()
