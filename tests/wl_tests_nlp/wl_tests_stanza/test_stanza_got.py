# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Stanza - Gothic
# Copyright (C) 2018-2023  Ye Lei (叶磊)
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

from tests.wl_tests_nlp.wl_tests_stanza import test_stanza

def test_stanza_got():
    test_stanza.wl_test_stanza(
        lang = 'got',
        results_sentence_tokenize = ['𐌲𐌿𐍄𐌰𐍂𐌰𐌶𐌳𐌰, 𐌲𐌿𐍄𐍂𐌰𐌶𐌳𐌰 𐌰𐌹𐌸𐌸𐌰𐌿 𐌲𐌿𐍄𐌹𐍃𐌺𐌰 𐍂𐌰𐌶𐌳𐌰 𐌹𐍃𐍄 𐌲𐌰𐍃𐍅𐌿𐌻𐍄𐌰𐌽𐌰 𐌰𐌿𐍃𐍄𐍂𐌰𐌲𐌰𐌹𐍂𐌼𐌰𐌽𐌹𐍃𐌺𐌰 𐍂𐌰𐌶𐌳𐌰 𐍂𐍉𐌳𐌹𐌳𐌰 𐍆𐍂𐌰𐌼 𐌲𐌿𐍄𐌰𐌼. 𐍃𐌹 𐌹𐍃𐍄 𐌰𐌹𐌽𐌰𐌷𐍉 𐌰𐌿𐍃𐍄𐍂𐌰𐌲𐌰𐌹𐌼𐌰𐌽𐌹𐍃𐌺𐌰 𐍂𐌰𐌶𐌳𐌰 𐍃𐍉𐌴𐌹 𐌷𐌰𐌱𐌰𐌹𐌸 𐌲𐌰𐌼𐌴𐌻𐌴𐌹𐌽𐌹𐌽𐍃', '.'],
        results_word_tokenize = ['𐌲𐌿𐍄𐌰𐍂𐌰𐌶𐌳𐌰,', '𐌲𐌿𐍄𐍂𐌰𐌶𐌳𐌰', '𐌰𐌹𐌸𐌸𐌰𐌿', '𐌲𐌿𐍄𐌹𐍃𐌺𐌰', '𐍂𐌰𐌶𐌳𐌰', '𐌹𐍃𐍄', '𐌲𐌰𐍃𐍅𐌿𐌻𐍄𐌰𐌽𐌰', '𐌰𐌿𐍃𐍄𐍂𐌰𐌲𐌰𐌹𐍂𐌼𐌰𐌽𐌹𐍃𐌺𐌰', '𐍂𐌰𐌶𐌳𐌰', '𐍂𐍉𐌳𐌹𐌳𐌰', '𐍆𐍂𐌰𐌼', '𐌲𐌿𐍄𐌰𐌼', '.'],
        results_pos_tag = [('𐌲𐌿𐍄𐌰𐍂𐌰𐌶𐌳𐌰,', 'Ne'), ('𐌲𐌿𐍄𐍂𐌰𐌶𐌳𐌰', 'Ne'), ('𐌰𐌹𐌸𐌸𐌰𐌿', 'Pp'), ('𐌲𐌿𐍄𐌹𐍃𐌺𐌰', 'Pp'), ('𐍂𐌰𐌶𐌳𐌰', 'Pp'), ('𐌹𐍃𐍄', 'Pp'), ('𐌲𐌰𐍃𐍅𐌿𐌻𐍄𐌰𐌽𐌰', 'Ne'), ('𐌰𐌿𐍃𐍄𐍂𐌰𐌲𐌰𐌹𐍂𐌼𐌰𐌽𐌹𐍃𐌺𐌰', 'Ne'), ('𐍂𐌰𐌶𐌳𐌰', 'Pp'), ('𐍂𐍉𐌳𐌹𐌳𐌰', 'Pp'), ('𐍆𐍂𐌰𐌼', 'Pp'), ('𐌲𐌿𐍄𐌰𐌼', 'Ne'), ('.', 'C-')],
        results_pos_tag_universal = [('𐌲𐌿𐍄𐌰𐍂𐌰𐌶𐌳𐌰,', 'PROPN'), ('𐌲𐌿𐍄𐍂𐌰𐌶𐌳𐌰', 'PROPN'), ('𐌰𐌹𐌸𐌸𐌰𐌿', 'PRON'), ('𐌲𐌿𐍄𐌹𐍃𐌺𐌰', 'PRON'), ('𐍂𐌰𐌶𐌳𐌰', 'PRON'), ('𐌹𐍃𐍄', 'PRON'), ('𐌲𐌰𐍃𐍅𐌿𐌻𐍄𐌰𐌽𐌰', 'PROPN'), ('𐌰𐌿𐍃𐍄𐍂𐌰𐌲𐌰𐌹𐍂𐌼𐌰𐌽𐌹𐍃𐌺𐌰', 'PROPN'), ('𐍂𐌰𐌶𐌳𐌰', 'PRON'), ('𐍂𐍉𐌳𐌹𐌳𐌰', 'PRON'), ('𐍆𐍂𐌰𐌼', 'PRON'), ('𐌲𐌿𐍄𐌰𐌼', 'PROPN'), ('.', 'CCONJ')],
        results_lemmatize = ['𐌲𐌿𐍄𐌰𐍂𐌰𐌶𐌳𐌰,', '𐌲𐌿𐍄𐍂𐌰𐌶𐌳𐌰', '𐌰𐌹𐌸𐌸𐌰𐌿', '𐌲𐌿𐍄𐌹𐍃𐌺𐌰', '𐍂𐌰𐌶𐌳𐌰', '𐌹𐍃𐍄', '𐌲𐌰𐍃𐍅𐌿𐌻𐍄𐌰𐌽𐌰', '𐌰𐌿𐍃𐍄𐍂𐌰𐌲𐌰𐌹𐍂𐌼𐌰𐌽𐌹𐍃𐌺𐌰', '𐍂𐌰𐌶𐌳𐌰', '𐍂𐍉𐌳𐌹𐌳𐌰', '𐍆𐍂𐌰𐌼', '𐌲𐌿𐍄𐌰𐌼', '-uh'],
        results_dependency_parse = [('𐌲𐌿𐍄𐌰𐍂𐌰𐌶𐌳𐌰,', '𐌲𐌿𐍄𐌰𐍂𐌰𐌶𐌳𐌰,', 'root', 0), ('𐌲𐌿𐍄𐍂𐌰𐌶𐌳𐌰', '𐌲𐌿𐍄𐌰𐍂𐌰𐌶𐌳𐌰,', 'appos', -1), ('𐌰𐌹𐌸𐌸𐌰𐌿', '𐌲𐌿𐍄𐍂𐌰𐌶𐌳𐌰', 'appos', -1), ('𐌲𐌿𐍄𐌹𐍃𐌺𐌰', '𐌲𐌿𐍄𐌰𐍂𐌰𐌶𐌳𐌰,', 'nsubj', -3), ('𐍂𐌰𐌶𐌳𐌰', '𐌲𐌿𐍄𐌰𐍂𐌰𐌶𐌳𐌰,', 'nsubj', -4), ('𐌹𐍃𐍄', '𐌲𐌰𐍃𐍅𐌿𐌻𐍄𐌰𐌽𐌰', 'flat:name', 1), ('𐌲𐌰𐍃𐍅𐌿𐌻𐍄𐌰𐌽𐌰', '𐌲𐌿𐍄𐌰𐍂𐌰𐌶𐌳𐌰,', 'appos', -6), ('𐌰𐌿𐍃𐍄𐍂𐌰𐌲𐌰𐌹𐍂𐌼𐌰𐌽𐌹𐍃𐌺𐌰', '𐌲𐌰𐍃𐍅𐌿𐌻𐍄𐌰𐌽𐌰', 'flat:name', -1), ('𐍂𐌰𐌶𐌳𐌰', '𐌲𐌰𐍃𐍅𐌿𐌻𐍄𐌰𐌽𐌰', 'flat:name', -2), ('𐍂𐍉𐌳𐌹𐌳𐌰', '𐌲𐌰𐍃𐍅𐌿𐌻𐍄𐌰𐌽𐌰', 'appos', -3), ('𐍆𐍂𐌰𐌼', '𐌲𐌿𐍄𐌰𐌼', 'nsubj', 1), ('𐌲𐌿𐍄𐌰𐌼', '𐌲𐌰𐍃𐍅𐌿𐌻𐍄𐌰𐌽𐌰', 'appos', -5), ('.', '.', 'root', 0)]
    )

if __name__ == '__main__':
    test_stanza_got()
