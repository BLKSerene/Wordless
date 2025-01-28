# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Sámi (Northern)
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

def test_stanza_sme():
    test_stanza.wl_test_stanza(
        lang = 'sme',
        results_sentence_tokenize = ['Davvisámegiella gullá sámegielaid oarjesámegielaid davvejovkui ovttas julev- ja bihtánsámegielain.', 'Eará oarjesámegielat leat ubmisámegiella ja lullisámegiella.'],
        results_word_tokenize = ['Davvisámegiella', 'gullá', 'sámegielaid', 'oarjesámegielaid', 'davvejovkui', 'ovttas', 'julev-', 'ja', 'bihtánsámegielain', '.'],
        results_pos_tag = [('Davvisámegiella', 'N'), ('gullá', 'V'), ('sámegielaid', 'N'), ('oarjesámegielaid', 'N'), ('davvejovkui', 'N'), ('ovttas', 'Adv'), ('julev-', 'N'), ('ja', 'CC'), ('bihtánsámegielain', 'N'), ('.', 'CLB')],
        results_pos_tag_universal = [('Davvisámegiella', 'NOUN'), ('gullá', 'VERB'), ('sámegielaid', 'NOUN'), ('oarjesámegielaid', 'NOUN'), ('davvejovkui', 'NOUN'), ('ovttas', 'ADV'), ('julev-', 'NOUN'), ('ja', 'CCONJ'), ('bihtánsámegielain', 'NOUN'), ('.', 'PUNCT')],
        results_lemmatize = ['davvisámegiella', 'gullat', 'sámegiella', 'oarjesámegiella', 'davvejoavku', 'ovttas', 'julle', 'ja', 'bihtánsámegiella', '.'],
        results_dependency_parse = [('Davvisámegiella', 'gullá', 'nsubj', 1), ('gullá', 'gullá', 'root', 0), ('sámegielaid', 'gullá', 'obj', -1), ('oarjesámegielaid', 'davvejovkui', 'nmod:poss', 1), ('davvejovkui', 'gullá', 'obl', -3), ('ovttas', 'gullá', 'advmod', -4), ('julev-', 'gullá', 'obl', -5), ('ja', 'julev-', 'cc', -1), ('bihtánsámegielain', 'julev-', 'conj', -2), ('.', 'gullá', 'punct', -8)]
    )

if __name__ == '__main__':
    test_stanza_sme()
