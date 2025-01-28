# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Maltese
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

def test_stanza_mlt():
    test_stanza.wl_test_stanza(
        lang = 'mlt',
        results_sentence_tokenize = ['L-oriġini tal-ilsien Malti huma attribwiti għall-wasla, kmieni fis-seklu 11, ta’ settlers minn Sqallija ġirien, fejn kien mitkellem is-sikolu-Għarbi, li biddel il-konkwista tal-gżira mill-Kalifat Fatimid fl-aħħar tas-seklu 9[18].', 'Din it-talba ġiet ikkorroborata minn studji ġenetiċi, li juru li l-Maltin kontemporanji jaqsmu antenati komuni ma’ Sqallin u Calabrians, bi ftit input ġenetiku mill-Afrika ta’ Fuq u l-Levant.'],
        results_word_tokenize = ['L-', 'oriġini', 'tal-', 'ilsien', 'Malti', 'huma', 'attribwiti', 'għall-', 'wasla', ',', 'kmieni', 'fis-', 'seklu', '11', ',', 'ta’', 'settlers', 'minn', 'Sqallija', 'ġirien', ',', 'fejn', 'kien', 'mitkellem', 'is-', 'sikolu', '-Għarbi', ',', 'li', 'biddel', 'il-', 'konkwista', 'tal-', 'gżira', 'mill-', 'Kalifat', 'Fatimid', 'fl-', 'aħħar', 'tas-', 'seklu', '9[18', ']', '.'],
        results_pos_tag = [('L-', 'DEF'), ('oriġini', 'NOUN'), ('tal-', 'GEN_DEF'), ('ilsien', 'NOUN'), ('Malti', 'ADJ'), ('huma', 'PRON_PERS'), ('attribwiti', 'NOUN'), ('għall-', 'PREP_DEF'), ('wasla', 'NOUN'), (',', 'X_PUN'), ('kmieni', 'ADV'), ('fis-', 'PREP_DEF'), ('seklu', 'NOUN'), ('11', 'X_DIG'), (',', 'X_PUN'), ('ta’', 'GEN'), ('settlers', 'NOUN'), ('minn', 'PREP'), ('Sqallija', 'NOUN'), ('ġirien', 'ADJ'), (',', 'X_PUN'), ('fejn', 'PRON_INT'), ('kien', 'KIEN'), ('mitkellem', 'PART_PASS'), ('is-', 'DEF'), ('sikolu', 'NOUN'), ('-Għarbi', 'ADJ'), (',', 'X_PUN'), ('li', 'COMP'), ('biddel', 'VERB'), ('il-', 'DEF'), ('konkwista', 'NOUN'), ('tal-', 'GEN_DEF'), ('gżira', 'NOUN'), ('mill-', 'PREP_DEF'), ('Kalifat', 'NOUN'), ('Fatimid', 'ADJ'), ('fl-', 'PREP_DEF'), ('aħħar', 'NOUN'), ('tas-', 'GEN_DEF'), ('seklu', 'NOUN'), ('9[18', 'X_DIG'), (']', 'X_PUN'), ('.', 'X_PUN')],
        results_pos_tag_universal = [('L-', 'DET'), ('oriġini', 'NOUN'), ('tal-', 'ADP'), ('ilsien', 'NOUN'), ('Malti', 'ADJ'), ('huma', 'PRON'), ('attribwiti', 'NOUN'), ('għall-', 'ADP'), ('wasla', 'NOUN'), (',', 'PUNCT'), ('kmieni', 'ADV'), ('fis-', 'ADP'), ('seklu', 'NOUN'), ('11', 'NUM'), (',', 'PUNCT'), ('ta’', 'ADP'), ('settlers', 'NOUN'), ('minn', 'ADP'), ('Sqallija', 'NOUN'), ('ġirien', 'ADJ'), (',', 'PUNCT'), ('fejn', 'ADV'), ('kien', 'AUX'), ('mitkellem', 'VERB'), ('is-', 'DET'), ('sikolu', 'NOUN'), ('-Għarbi', 'ADJ'), (',', 'PUNCT'), ('li', 'SCONJ'), ('biddel', 'VERB'), ('il-', 'DET'), ('konkwista', 'NOUN'), ('tal-', 'ADP'), ('gżira', 'NOUN'), ('mill-', 'ADP'), ('Kalifat', 'NOUN'), ('Fatimid', 'ADJ'), ('fl-', 'ADP'), ('aħħar', 'NOUN'), ('tas-', 'ADP'), ('seklu', 'NOUN'), ('9[18', 'NUM'), (']', 'PUNCT'), ('.', 'PUNCT')],
        results_dependency_parse = [('L-', 'oriġini', 'det', 1), ('oriġini', 'attribwiti', 'nsubj', 5), ('tal-', 'ilsien', 'case:det', 1), ('ilsien', 'oriġini', 'nmod:poss', -2), ('Malti', 'ilsien', 'amod', -1), ('huma', 'attribwiti', 'cop', 1), ('attribwiti', 'attribwiti', 'root', 0), ('għall-', 'wasla', 'case:det', 1), ('wasla', 'attribwiti', 'obl', -2), (',', 'attribwiti', 'punct', -3), ('kmieni', 'attribwiti', 'advmod', -4), ('fis-', 'seklu', 'case:det', 1), ('seklu', 'attribwiti', 'nmod', -6), ('11', 'aħħar', 'nmod', 25), (',', 'settlers', 'punct', 2), ('ta’', 'settlers', 'case', 1), ('settlers', 'wasla', 'nmod:poss', -8), ('minn', 'Sqallija', 'case', 1), ('Sqallija', 'settlers', 'nmod', -2), ('ġirien', 'Sqallija', 'amod', -1), (',', 'mitkellem', 'punct', 3), ('fejn', 'mitkellem', 'advmod', 2), ('kien', 'mitkellem', 'cop', 1), ('mitkellem', 'attribwiti', 'acl', -17), ('is-', 'sikolu', 'det', 1), ('sikolu', 'mitkellem', 'nsubj:pass', -2), ('-Għarbi', 'sikolu', 'amod', -1), (',', 'mitkellem', 'punct', -4), ('li', 'biddel', 'mark', 1), ('biddel', 'sikolu', 'acl', -4), ('il-', 'konkwista', 'det', 1), ('konkwista', 'biddel', 'obj', -2), ('tal-', 'gżira', 'case:det', 1), ('gżira', 'konkwista', 'nmod:poss', -2), ('mill-', 'Kalifat', 'case:det', 1), ('Kalifat', 'gżira', 'nmod', -2), ('Fatimid', 'Kalifat', 'amod', -1), ('fl-', 'aħħar', 'case:det', 1), ('aħħar', 'biddel', 'obl', -9), ('tas-', 'seklu', 'case:det', 1), ('seklu', 'aħħar', 'nmod:poss', -2), ('9[18', 'aħħar', 'nummod', -3), (']', 'biddel', 'punct', -13), ('.', 'attribwiti', 'punct', -37)]
    )

if __name__ == '__main__':
    test_stanza_mlt()
