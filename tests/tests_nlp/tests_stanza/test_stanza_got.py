# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Stanza - Gothic
# Copyright (C) 2018-2024  Ye Lei (叶磊)
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

from tests.tests_nlp.tests_stanza import test_stanza

def test_stanza_got():
    test_stanza.wl_test_stanza(
        lang = 'got',
        results_sentence_tokenize = ['𐌲𐌿𐍄𐌰𐍂𐌰𐌶𐌳𐌰, 𐌲𐌿𐍄𐍂𐌰𐌶𐌳𐌰 𐌰𐌹𐌸𐌸𐌰𐌿 𐌲𐌿𐍄𐌹𐍃𐌺𐌰 𐍂𐌰𐌶𐌳𐌰 𐌹𐍃𐍄 𐌲𐌰𐍃𐍅𐌿𐌻𐍄𐌰𐌽𐌰 𐌰𐌿𐍃𐍄𐍂𐌰𐌲𐌰𐌹𐍂𐌼𐌰𐌽𐌹𐍃𐌺𐌰 𐍂𐌰𐌶𐌳𐌰 𐍂𐍉𐌳𐌹𐌳𐌰 𐍆𐍂𐌰𐌼 𐌲𐌿𐍄𐌰𐌼. 𐍃𐌹 𐌹𐍃𐍄 𐌰𐌹𐌽𐌰𐌷𐍉 𐌰𐌿𐍃𐍄𐍂𐌰𐌲𐌰𐌹𐌼𐌰𐌽𐌹𐍃𐌺𐌰 𐍂𐌰𐌶𐌳𐌰 𐍃𐍉𐌴𐌹 𐌷𐌰𐌱𐌰𐌹𐌸 𐌲𐌰𐌼𐌴𐌻𐌴𐌹𐌽𐌹𐌽𐍃', '.'],
        results_word_tokenize = ['𐌲𐌿𐍄𐌰𐍂𐌰𐌶𐌳𐌰,', '𐌲𐌿𐍄𐍂𐌰𐌶𐌳𐌰', '𐌰𐌹𐌸𐌸𐌰𐌿', '𐌲𐌿𐍄𐌹𐍃𐌺𐌰', '𐍂𐌰𐌶𐌳𐌰', '𐌹𐍃𐍄', '𐌲𐌰𐍃𐍅𐌿𐌻𐍄𐌰𐌽𐌰', '𐌰𐌿𐍃𐍄𐍂𐌰𐌲𐌰𐌹𐍂𐌼𐌰𐌽𐌹𐍃𐌺𐌰', '𐍂𐌰𐌶𐌳𐌰', '𐍂𐍉𐌳𐌹𐌳𐌰', '𐍆𐍂𐌰𐌼', '𐌲𐌿𐍄𐌰𐌼', '.'],
        results_pos_tag = [('𐌲𐌿𐍄𐌰𐍂𐌰𐌶𐌳𐌰,', 'Nb'), ('𐌲𐌿𐍄𐍂𐌰𐌶𐌳𐌰', 'Nb'), ('𐌰𐌹𐌸𐌸𐌰𐌿', 'Pd'), ('𐌲𐌿𐍄𐌹𐍃𐌺𐌰', 'Pd'), ('𐍂𐌰𐌶𐌳𐌰', 'Pd'), ('𐌹𐍃𐍄', 'Pd'), ('𐌲𐌰𐍃𐍅𐌿𐌻𐍄𐌰𐌽𐌰', 'Nb'), ('𐌰𐌿𐍃𐍄𐍂𐌰𐌲𐌰𐌹𐍂𐌼𐌰𐌽𐌹𐍃𐌺𐌰', 'Nb'), ('𐍂𐌰𐌶𐌳𐌰', 'Pd'), ('𐍂𐍉𐌳𐌹𐌳𐌰', 'Pd'), ('𐍆𐍂𐌰𐌼', 'Pd'), ('𐌲𐌿𐍄𐌰𐌼', 'Nb'), ('.', 'Df')],
        results_pos_tag_universal = [('𐌲𐌿𐍄𐌰𐍂𐌰𐌶𐌳𐌰,', 'NOUN'), ('𐌲𐌿𐍄𐍂𐌰𐌶𐌳𐌰', 'NOUN'), ('𐌰𐌹𐌸𐌸𐌰𐌿', 'DET'), ('𐌲𐌿𐍄𐌹𐍃𐌺𐌰', 'DET'), ('𐍂𐌰𐌶𐌳𐌰', 'DET'), ('𐌹𐍃𐍄', 'DET'), ('𐌲𐌰𐍃𐍅𐌿𐌻𐍄𐌰𐌽𐌰', 'NOUN'), ('𐌰𐌿𐍃𐍄𐍂𐌰𐌲𐌰𐌹𐍂𐌼𐌰𐌽𐌹𐍃𐌺𐌰', 'NOUN'), ('𐍂𐌰𐌶𐌳𐌰', 'DET'), ('𐍂𐍉𐌳𐌹𐌳𐌰', 'DET'), ('𐍆𐍂𐌰𐌼', 'DET'), ('𐌲𐌿𐍄𐌰𐌼', 'NOUN'), ('.', 'ADV')],
        results_lemmatize = ['𐌲𐌿𐍄𐌰𐍂𐌰𐌶𐌳𐌰,', '𐌲𐌿𐍄𐍂𐌰𐌶𐌳𐌰', '𐌰𐌹𐌸𐌸𐌰𐌿', '𐌲𐌿𐍄𐌹𐍃𐌺𐌰', '𐍂𐌰𐌶𐌳𐌰', '𐌹𐍃𐍄', '𐌲𐌰𐍃𐍅𐌿𐌻𐍄𐌰𐌽𐌰', '𐌰𐌿𐍃𐍄𐍂𐌰𐌲𐌰𐌹𐍂𐌼𐌰𐌽𐌹𐍃𐌺𐌰', '𐍂𐌰𐌶𐌳𐌰', '𐍂𐍉𐌳𐌹𐌳𐌰', '𐍆𐍂𐌰𐌼', '𐌲𐌿𐍄𐌰𐌼', '-uh'],
        results_dependency_parse = [('𐌲𐌿𐍄𐌰𐍂𐌰𐌶𐌳𐌰,', '𐌲𐌿𐍄𐍂𐌰𐌶𐌳𐌰', 'vocative', 1), ('𐌲𐌿𐍄𐍂𐌰𐌶𐌳𐌰', '𐌲𐌿𐍄𐍂𐌰𐌶𐌳𐌰', 'root', 0), ('𐌰𐌹𐌸𐌸𐌰𐌿', '𐌲𐌿𐍄𐍂𐌰𐌶𐌳𐌰', 'det', -1), ('𐌲𐌿𐍄𐌹𐍃𐌺𐌰', '𐌲𐌰𐍃𐍅𐌿𐌻𐍄𐌰𐌽𐌰', 'det', 3), ('𐍂𐌰𐌶𐌳𐌰', '𐌲𐌰𐍃𐍅𐌿𐌻𐍄𐌰𐌽𐌰', 'det', 2), ('𐌹𐍃𐍄', '𐌲𐌰𐍃𐍅𐌿𐌻𐍄𐌰𐌽𐌰', 'det', 1), ('𐌲𐌰𐍃𐍅𐌿𐌻𐍄𐌰𐌽𐌰', '𐌲𐌿𐍄𐍂𐌰𐌶𐌳𐌰', 'appos', -5), ('𐌰𐌿𐍃𐍄𐍂𐌰𐌲𐌰𐌹𐍂𐌼𐌰𐌽𐌹𐍃𐌺𐌰', '𐌲𐌰𐍃𐍅𐌿𐌻𐍄𐌰𐌽𐌰', 'nmod', -1), ('𐍂𐌰𐌶𐌳𐌰', '𐌲𐌿𐍄𐌰𐌼', 'det', 3), ('𐍂𐍉𐌳𐌹𐌳𐌰', '𐌲𐌿𐍄𐌰𐌼', 'det', 2), ('𐍆𐍂𐌰𐌼', '𐌲𐌿𐍄𐌰𐌼', 'det', 1), ('𐌲𐌿𐍄𐌰𐌼', '𐌰𐌿𐍃𐍄𐍂𐌰𐌲𐌰𐌹𐍂𐌼𐌰𐌽𐌹𐍃𐌺𐌰', 'appos', -4), ('.', '.', 'root', 0)]
    )

if __name__ == '__main__':
    test_stanza_got()
