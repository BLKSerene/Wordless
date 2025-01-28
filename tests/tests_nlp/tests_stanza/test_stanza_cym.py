# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Welsh
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

def test_stanza_cym():
    test_stanza.wl_test_stanza(
        lang = 'cym',
        results_sentence_tokenize = ['Yng Nghyfrifiad y DU (2011), darganfuwyd bod 19% (562,000) o breswylwyr Cymru (tair blwydd a throsodd) yn gallu siarad Cymraeg.', "O'r ffigwr hwn, darganfuwyd bod 77% (431,000) yn gallu siarad, darllen, ac ysgrifennu'r iaith; dywedodd 73% o breswylwyr Cymru (2.2 miliwn) fod dim sgiliau yn y Gymraeg ganddynt.[8]", "Gellir cymharu hwn â Chyfrifiad 2001, a ddarganfu fod 20.8% o'r boblogaeth yn gallu siarad Cymraeg, gyda 57% (315,000) o'r ffigwr hon yn dweud eu bod yn rhugl yn yr iaith.", '[9]'],
        results_word_tokenize = ['Yng', 'Nghyfrifiad', 'y', 'DU', '(', '2011', ')', ',', 'darganfuwyd', 'bod', '19', '%', '(', '562,000', ')', 'o', 'breswylwyr', 'Cymru', '(', 'tair', 'blwydd', 'a', 'throsodd', ')', 'yn', 'gallu', 'siarad', 'Cymraeg', '.'],
        results_pos_tag = [('Yng', 'prep'), ('Nghyfrifiad', 'noun'), ('y', 'art'), ('DU', 'place'), ('(', 'punct'), ('2011', 'num'), (')', 'punct'), (',', 'punct'), ('darganfuwyd', 'verb'), ('bod', 'verbnoun'), ('19', 'num'), ('%', 'sym'), ('(', 'punct'), ('562,000', 'num'), (')', 'punct'), ('o', 'prep'), ('breswylwyr', 'noun'), ('Cymru', 'place'), ('(', 'punct'), ('tair', 'num'), ('blwydd', 'noun'), ('a', 'cconj'), ('tros', 'iprep'), ('e', 'indep'), (')', 'punct'), ('yn', 'impf'), ('gallu', 'verbnoun'), ('siarad', 'verbnoun'), ('Cymraeg', 'noun'), ('.', 'punct')],
        results_pos_tag_universal = [('Yng', 'ADP'), ('Nghyfrifiad', 'NOUN'), ('y', 'DET'), ('DU', 'PROPN'), ('(', 'PUNCT'), ('2011', 'NUM'), (')', 'PUNCT'), (',', 'PUNCT'), ('darganfuwyd', 'VERB'), ('bod', 'NOUN'), ('19', 'NUM'), ('%', 'SYM'), ('(', 'PUNCT'), ('562,000', 'NUM'), (')', 'PUNCT'), ('o', 'ADP'), ('breswylwyr', 'NOUN'), ('Cymru', 'PROPN'), ('(', 'PUNCT'), ('tair', 'NUM'), ('blwydd', 'NOUN'), ('a', 'CCONJ'), ('tros', 'ADP'), ('e', 'PRON'), (')', 'PUNCT'), ('yn', 'AUX'), ('gallu', 'NOUN'), ('siarad', 'NOUN'), ('Cymraeg', 'NOUN'), ('.', 'PUNCT')],
        results_lemmatize = ['yn', 'cyfrifiad', 'y', 'TU', '(', '2011', ')', ',', 'darganfod', 'bod', '19fed', '%', '(', '562000', ')', 'o', 'preswylwr', 'Cymru', '(', 'tri', 'blwydd', 'a', 'tros', 'e', ')', 'yn', 'gallu', 'siarad', 'Cymraeg', '.'],
        results_dependency_parse = [('Yng', 'Nghyfrifiad', 'case', 1), ('Nghyfrifiad', 'darganfuwyd', 'obl', 7), ('y', 'DU', 'det', 1), ('DU', 'Nghyfrifiad', 'nmod', -2), ('(', '2011', 'punct', 1), ('2011', 'DU', 'appos', -2), (')', '2011', 'punct', -1), (',', 'darganfuwyd', 'punct', 1), ('darganfuwyd', 'darganfuwyd', 'root', 0), ('bod', 'darganfuwyd', 'ccomp', -1), ('19', '%', 'nummod', 1), ('%', 'bod', 'nsubj', -2), ('(', '562,000', 'punct', 1), ('562,000', '%', 'appos', -2), (')', '562,000', 'punct', -1), ('o', 'breswylwyr', 'case', 1), ('breswylwyr', '%', 'nmod', -5), ('Cymru', 'breswylwyr', 'nmod', -1), ('(', 'blwydd', 'punct', 2), ('tair', 'blwydd', 'nummod', 1), ('blwydd', 'breswylwyr', 'conj', -4), ('a', 'e', 'cc', 2), ('tros', 'e', 'case', 1), ('e', 'breswylwyr', 'conj', -7), (')', 'blwydd', 'punct', -4), ('yn', 'gallu', 'aux', 1), ('gallu', 'bod', 'xcomp', -17), ('siarad', 'gallu', 'xcomp', -1), ('Cymraeg', 'siarad', 'obj', -1), ('.', 'darganfuwyd', 'punct', -21)]
    )

if __name__ == '__main__':
    test_stanza_cym()
