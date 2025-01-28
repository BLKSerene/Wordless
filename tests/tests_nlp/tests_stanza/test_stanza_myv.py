# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Erzya
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

def test_stanza_myv():
    test_stanza.wl_test_stanza(
        lang = 'myv',
        results_sentence_tokenize = ['Э́рзянь кель — совавтови суоминь-равонь тарадонтень суоми-угрань келень семиянь группанть пельксэнтень, уралонь келень семиянтень.', 'Эрзянь кельсэ кортыть эрзянь ломанть.'],
        results_word_tokenize = ['Э́рзянь', 'кель', '—', 'совавтови', 'суоминь-равонь', 'тарадонтень', 'суоми-угрань', 'келень', 'семиянь', 'группанть', 'пельксэнтень', ',', 'уралонь', 'келень', 'семиянтень', '.'],
        results_pos_tag = [('Э́рзянь', 'N'), ('кель', 'A'), ('—', 'PUNCT'), ('совавтови', 'V'), ('суоминь-равонь', 'N'), ('тарадонтень', 'N'), ('суоми-угрань', 'N'), ('келень', 'N'), ('семиянь', 'N'), ('группанть', 'N'), ('пельксэнтень', 'N'), (',', 'CLB'), ('уралонь', 'N'), ('келень', 'N'), ('семиянтень', 'N'), ('.', 'CLB')],
        results_pos_tag_universal = [('Э́рзянь', 'NOUN'), ('кель', 'ADJ'), ('—', 'PUNCT'), ('совавтови', 'VERB'), ('суоминь-равонь', 'NOUN'), ('тарадонтень', 'NOUN'), ('суоми-угрань', 'NOUN'), ('келень', 'NOUN'), ('семиянь', 'NOUN'), ('группанть', 'NOUN'), ('пельксэнтень', 'NOUN'), (',', 'PUNCT'), ('уралонь', 'NOUN'), ('келень', 'NOUN'), ('семиянтень', 'NOUN'), ('.', 'PUNCT')],
        results_lemmatize = ['Э́рзянь', 'кель', '—', 'совавтовомс', 'суомонь-раво', 'тарад', 'суомо-угань', 'кель', 'семия', 'группа', 'пелькс', ',', 'урал', 'кель', 'семия', '.'],
        results_dependency_parse = [('Э́рзянь', 'кель', 'nmod', 1), ('кель', 'совавтови', 'nsubj', 2), ('—', 'совавтови', 'punct', 1), ('совавтови', 'совавтови', 'root', 0), ('суоминь-равонь', 'тарадонтень', 'nmod', 1), ('тарадонтень', 'совавтови', 'obl', -2), ('суоми-угрань', 'группанть', 'nmod', 3), ('келень', 'группанть', 'nmod', 2), ('семиянь', 'группанть', 'nmod', 1), ('группанть', 'пельксэнтень', 'nmod', 1), ('пельксэнтень', 'совавтови', 'obl', -7), (',', 'пельксэнтень', 'punct', -1), ('уралонь', 'келень', 'nmod', 1), ('келень', 'семиянтень', 'nmod', 1), ('семиянтень', 'пельксэнтень', 'appos', -4), ('.', 'совавтови', 'punct', -12)]
    )

if __name__ == '__main__':
    test_stanza_myv()
