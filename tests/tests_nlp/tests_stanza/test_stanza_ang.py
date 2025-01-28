# ----------------------------------------------------------------------
# Tests: NLP - Stanza - English (Old)
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

def test_stanza_ang():
    test_stanza.wl_test_stanza(
        lang = 'ang',
        results_sentence_tokenize = ['Seo ænglisce spræc (Englisc gereord) is Westgermanisc spræc, þe fram Englalande aras.', 'Heo is sibb þæm Ealdfresiscan and þære Ealdseaxiscan spræcum.', 'Hit is gastleas spræc, and ne hæfþ nane gebyrdlice sprecan todæg, ac sume menn leorniaþ hit on Betweoxnette and writaþ on him, swa swa her on þissum Wicipædian.'],
        results_word_tokenize = ['Seo', 'ænglisce', 'spræc', '(', 'Englisc', 'gereord', ')', 'is', 'Westgermanisc', 'spræc', ',', 'þe', 'fram', 'Englalande', 'aras', '.'],
        results_pos_tag = [('Seo', 'demonstrative-article'), ('ænglisce', 'adjective'), ('spræc', 'main-verb'), ('(', 'punctuation'), ('Englisc', 'adjective'), ('gereord', 'common noun'), (')', 'punctuation'), ('is', 'auxiliary-verb'), ('Westgermanisc', 'proper noun'), ('spræc', 'main-verb'), (',', 'punctuation'), ('þe', 'pronoun'), ('fram', 'adposition'), ('Englalande', 'proper noun'), ('aras', 'main-verb'), ('.', 'punctuation')],
        results_pos_tag_universal = [('Seo', 'DET'), ('ænglisce', 'ADJ'), ('spræc', 'VERB'), ('(', 'PUNCT'), ('Englisc', 'ADJ'), ('gereord', 'NOUN'), (')', 'PUNCT'), ('is', 'AUX'), ('Westgermanisc', 'PROPN'), ('spræc', 'VERB'), (',', 'PUNCT'), ('þe', 'PRON'), ('fram', 'ADP'), ('Englalande', 'PROPN'), ('aras', 'VERB'), ('.', 'PUNCT')],
        results_lemmatize = ['se-sēo-ðæt (DEM)', 'ǣnglisc', 'sprecan(ge)', '(', 'Englisc', 'reord(ge) ‘voice; language, speech’', ')', 'bēon/wesan/sēon ‘to be’', 'Westgermanisc', 'sprecan(ge)', ',', 'þe', 'fram ‘from, by; since’ (PREP)', 'Englaland', 'ārīsan ‘to arise; to rise; to spring from; to ascend’', '.'],
        results_dependency_parse = [('Seo', 'ænglisce', 'det', 1), ('ænglisce', 'spræc', 'nsubj', 1), ('spræc', 'spræc', 'root', 0), ('(', 'gereord', 'punct', 2), ('Englisc', 'gereord', 'amod', 1), ('gereord', 'spræc', 'nsubj', -3), (')', 'spræc', 'punct', 3), ('is', 'spræc', 'cop', 2), ('Westgermanisc', 'spræc', 'nsubj', 1), ('spræc', 'spræc', 'parataxis', -7), (',', 'aras', 'punct', 4), ('þe', 'aras', 'nsubj', 3), ('fram', 'Englalande', 'case', 1), ('Englalande', 'aras', 'obl:lmod', 1), ('aras', 'Westgermanisc', 'acl:relcl', -6), ('.', 'aras', 'punct', -1)]
    )

if __name__ == '__main__':
    test_stanza_ang()
