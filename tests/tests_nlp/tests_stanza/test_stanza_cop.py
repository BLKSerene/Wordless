# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Coptic
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

def test_stanza_cop():
    test_stanza.wl_test_stanza(
        lang = 'cop',
        results_sentence_tokenize = ['ϭⲟⲗ ·', 'ⲛⲉⲛⲧⲁⲩⲕⲗⲏⲣⲟⲛⲟⲙⲉⲓ ⲉⲛⲉϩ ⲛⲧⲙⲛⲧⲣⲣⲟ ⲙⲡⲛⲟⲩⲧⲉ ·'],
        results_word_tokenize = ['ϭⲟⲗ', '·'],
        results_pos_tag = [('ϭⲟⲗ', 'VIMP'), ('·', 'PUNCT')],
        results_pos_tag_universal = [('ϭⲟⲗ', 'VERB'), ('·', 'PUNCT')],
        results_lemmatize = ['ϭⲟⲗ', '·'],
        results_dependency_parse = [('ϭⲟⲗ', 'ϭⲟⲗ', 'root', 0), ('·', 'ϭⲟⲗ', 'punct', -1)]
    )

if __name__ == '__main__':
    test_stanza_cop()
