# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Georgian
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

def test_stanza_kat():
    test_stanza.wl_test_stanza(
        lang = 'kat',
        results_sentence_tokenize = ['ქართული ენა — ქართველურ ენათა ოჯახის ენა.', 'ქართველების მშობლიური ენა, საქართველოს სახელმწიფო ენა (აფხაზეთის ავტონომიურ რესპუბლიკაში, მასთან ერთად სახელმწიფო ენად აღიარებულია აფხაზური ენა).', 'ქართულ ენაზე 5 მილიონზე მეტი ადამიანი ლაპარაკობს.'],
        results_word_tokenize = ['ქართული', 'ენა', '—', 'ქართველურ', 'ენათა', 'ოჯახის', 'ენა', '.'],
        results_pos_tag = [('ქართული', 'Adj'), ('ენა', 'Noun'), ('—', 'F'), ('ქართველურ', 'Adj'), ('ენათა', 'Noun'), ('ოჯახის', 'Noun'), ('ენა', 'Noun'), ('.', 'F')],
        results_pos_tag_universal = [('ქართული', 'ADJ'), ('ენა', 'NOUN'), ('—', 'PUNCT'), ('ქართველურ', 'ADJ'), ('ენათა', 'NOUN'), ('ოჯახის', 'NOUN'), ('ენა', 'NOUN'), ('.', 'PUNCT')],
        results_lemmatize = ['ქართული', 'ენა', '—', 'ქართველური', 'ენა', 'ოჯახი', 'ენა', '.'],
        results_dependency_parse = [('ქართული', 'ენა', 'amod', 1), ('ენა', 'ენა', 'nsubj', 5), ('—', 'ენა', 'punct', 4), ('ქართველურ', 'ენათა', 'amod', 1), ('ენათა', 'ოჯახის', 'nmod', 1), ('ოჯახის', 'ენა', 'nmod', 1), ('ენა', 'ენა', 'root', 0), ('.', 'ენა', 'punct', -1)]
    )

if __name__ == '__main__':
    test_stanza_kat()
