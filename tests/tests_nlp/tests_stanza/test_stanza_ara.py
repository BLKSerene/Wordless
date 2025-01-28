# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Arabic
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

def test_stanza_ara():
    test_stanza.wl_test_stanza(
        lang = 'ara',
        results_sentence_tokenize = ['تحتوي اللغة العربية 28 حرفاً مكتوباً. ويرى بعضُ اللغويين أنه يجب إضافة حرف الهمزة إلى حروف العربية، ليصبحَ عدد الحروف 29. تُكتب العربية من اليمين إلى اليسار - ومثلها اللغة الفارسية والعبرية على عكس كثير من اللغات العالمية - ومن أعلى الصفحة إلى أسفلها.'],
        results_word_tokenize = ['تحتوي', 'اللغة', 'العربية', '28', 'حرفاً', 'مكتوباً', '.'],
        results_pos_tag = [('تحتوي', 'VIIA-3FS--'), ('اللغة', 'N------S1D'), ('العربية', 'A-----FS1D'), ('28', 'Q---------'), ('حرفاً', 'N------S4I'), ('مكتوباً', 'A-----MS4I'), ('.', 'G---------')],
        results_pos_tag_universal = [('تحتوي', 'VERB'), ('اللغة', 'NOUN'), ('العربية', 'ADJ'), ('28', 'NUM'), ('حرفاً', 'NOUN'), ('مكتوباً', 'ADJ'), ('.', 'PUNCT')],
        results_lemmatize = ['اِحتَوَى', 'لُغَة', 'عَرَبِيّ', '28', 'حَرف', 'مُكتَوِب', '.'],
        results_dependency_parse = [('تحتوي', 'تحتوي', 'root', 0), ('اللغة', 'تحتوي', 'nsubj', -1), ('العربية', 'اللغة', 'amod', -1), ('28', 'تحتوي', 'obj', -3), ('حرفاً', '28', 'nmod', -1), ('مكتوباً', 'حرفاً', 'amod', -1), ('.', 'تحتوي', 'punct', -6)]
    )

if __name__ == '__main__':
    test_stanza_ara()
