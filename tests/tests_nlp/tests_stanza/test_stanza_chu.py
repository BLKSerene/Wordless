# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Church Slavonic (Old)
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

def test_stanza_chu():
    test_stanza.wl_test_stanza(
        lang = 'chu',
        results_sentence_tokenize = ['ВЪ И҃ В҃ ДЬНЬ КЛꙆМЕНТА Бъ҃ ꙇже нъи лѣта огрѧдѫцѣ блаженаго климента мѫченіка твоего ꙇ папежа чьстьѭ веселішꙇ подазь мілостівъі да егоже чьсть чьстімъ сілоѭ ѹбо мѫчениѣ его наслѣдѹемъ г҃мь'],
        results_word_tokenize = ['ВЪ', 'И҃', 'В҃', 'ДЬНЬ', 'КЛꙆМЕНТА'],
        results_pos_tag = [('ВЪ', 'R-'), ('И҃', 'Ma'), ('В҃', 'Pd'), ('ДЬНЬ', 'Nb'), ('КЛꙆМЕНТА', 'Nb')],
        results_pos_tag_universal = [('ВЪ', 'ADP'), ('И҃', 'NUM'), ('В҃', 'DET'), ('ДЬНЬ', 'NOUN'), ('КЛꙆМЕНТА', 'NOUN')],
        results_lemmatize = ['въ', 'осмь', 'вьсть', 'дьнь', 'климена'],
        results_dependency_parse = [('ВЪ', 'И҃', 'case', 1), ('И҃', 'ДЬНЬ', 'nummod', 2), ('В҃', 'ДЬНЬ', 'det', 1), ('ДЬНЬ', 'ДЬНЬ', 'root', 0), ('КЛꙆМЕНТА', 'ДЬНЬ', 'nmod', -1)]
    )

if __name__ == '__main__':
    test_stanza_chu()
