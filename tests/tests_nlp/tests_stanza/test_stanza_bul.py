# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Bulgarian
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

def test_stanza_bul():
    test_stanza.wl_test_stanza(
        lang = 'bul',
        results_sentence_tokenize = ['Бъ̀лгарският езѝк е индоевропейски език от групата на южнославянските езици, като образува неговата източна подгрупа.', 'Той е официалният език на Република България и един от 24-те официални езика на Европейския съюз.', 'Българският език е плурицентричен език – има няколко книжовни норми.', 'Наред с използваната в България основна норма, съществуват още македонска норма, която също използва кирилица, и банатска норма, която използва латиница.'],
        results_word_tokenize = ['Бъ̀лгарският', 'езѝк', 'е', 'индоевропейски', 'език', 'от', 'групата', 'на', 'южнославянските', 'езици', ',', 'като', 'образува', 'неговата', 'източна', 'подгрупа', '.'],
        results_pos_tag = [('Бъ̀лгарският', 'Amsf'), ('езѝк', 'Ncmsi'), ('е', 'Vxitf-r3s'), ('индоевропейски', 'Amsi'), ('език', 'Ncmsi'), ('от', 'R'), ('групата', 'Ncfsd'), ('на', 'R'), ('южнославянските', 'A-pd'), ('езици', 'Ncmpi'), (',', 'punct'), ('като', 'Cs'), ('образува', 'Vpitf-r3s'), ('неговата', 'Psol-s3fdm'), ('източна', 'Afsi'), ('подгрупа', 'Ncfsi'), ('.', 'punct')],
        results_pos_tag_universal = [('Бъ̀лгарският', 'ADJ'), ('езѝк', 'NOUN'), ('е', 'AUX'), ('индоевропейски', 'ADJ'), ('език', 'NOUN'), ('от', 'ADP'), ('групата', 'NOUN'), ('на', 'ADP'), ('южнославянските', 'ADJ'), ('езици', 'NOUN'), (',', 'PUNCT'), ('като', 'SCONJ'), ('образува', 'VERB'), ('неговата', 'DET'), ('източна', 'ADJ'), ('подгрупа', 'NOUN'), ('.', 'PUNCT')],
        results_lemmatize = ['Бъ̀лгарският', 'езѝк', 'съм', 'индоевропейски', 'език', 'от', 'група', 'на', 'южнославянски', 'език', ',', 'като', 'образувам', 'мой', 'източен', 'подгрупа', '.'],
        results_dependency_parse = [('Бъ̀лгарският', 'езѝк', 'amod', 1), ('езѝк', 'език', 'nsubj', 3), ('е', 'език', 'cop', 2), ('индоевропейски', 'език', 'amod', 1), ('език', 'език', 'root', 0), ('от', 'групата', 'case', 1), ('групата', 'език', 'nmod', -2), ('на', 'езици', 'case', 2), ('южнославянските', 'езици', 'amod', 1), ('езици', 'групата', 'nmod', -3), (',', 'образува', 'punct', 2), ('като', 'образува', 'mark', 1), ('образува', 'език', 'advcl', -8), ('неговата', 'подгрупа', 'det', 2), ('източна', 'подгрупа', 'amod', 1), ('подгрупа', 'образува', 'obj', -3), ('.', 'език', 'punct', -12)]
    )

if __name__ == '__main__':
    test_stanza_bul()
