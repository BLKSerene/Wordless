# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Uyghur
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

def test_stanza_uig():
    test_stanza.wl_test_stanza(
        lang = 'uig',
        results_sentence_tokenize = ['ئۇيغۇر تىلى ئۇيغۇر جۇڭگو شىنجاڭ ئۇيغۇر ئاپتونوم رايونىنىڭ ئېيتقان بىر تۈركىي تىلى.', 'ئۇ ئۇزاق ئەسىرلىك تەرەققىيات داۋامىدا قەدىمكى تۈركىي تىللار دەۋرى،', 'ئورخۇن ئۇيغۇر تىلى دەۋرى، ئىدىقۇت-خاقانىيە ئۇيغۇر تىلى دەۋرى، چاغاتاي ئۇيغۇر تىلى دەۋرىنى بېسىپ ئۆتكەن.', 'بۇ جەرياندا ئۇيغۇر تىلى ئورخۇن-يېنسەي يېزىقى، قەدىمكى ئۇيغۇر يېزىقى، بىراخما يېزىقى، مانى يېزىقى، ، ئەرەب يېزىقى قاتارلىق يېزىقلار بىلەن خاتىرىلەنگەن (بەئزى يېزىقلار ئومۇميۈزلۈك، بەزى يېزىقلار قىسمەن قوللىنىلغان)، شۇنداقلا سانسىكرىتچە، ساكچە، تۇخارچە، سوغدچە، ئەرەبچە، پارسچە، موڭغۇلچە، خىتايچە قاتارلىق نۇرغۇرن تىللار بىلەن ئۇچرىشىپ ھەم ئۆزئارا تەسىر كۆرسىتىپ، ئۈزلۈكسىز مۇكەممەللەشكەن ۋە ھازىرقى زامان ئۇيغۇر تىلى دەۋرىگە كىرگەن.'],
        results_word_tokenize = ['ئۇيغۇر', 'تىلى', 'ئۇيغۇر', 'جۇڭگو', 'شىنجاڭ', 'ئۇيغۇر', 'ئاپتونوم', 'رايونىنىڭ', 'ئېيتقان', 'بىر', 'تۈركىي', 'تىلى', '.'],
        results_pos_tag = [('ئۇيغۇر', 'N'), ('تىلى', 'N'), ('ئۇيغۇر', 'N'), ('جۇڭگو', 'N'), ('شىنجاڭ', 'N'), ('ئۇيغۇر', 'N'), ('ئاپتونوم', 'N'), ('رايونىنىڭ', 'N'), ('ئېيتقان', 'V'), ('بىر', 'M'), ('تۈركىي', 'N'), ('تىلى', 'N'), ('.', 'Y')],
        results_pos_tag_universal = [('ئۇيغۇر', 'NOUN'), ('تىلى', 'NOUN'), ('ئۇيغۇر', 'NOUN'), ('جۇڭگو', 'PROPN'), ('شىنجاڭ', 'PROPN'), ('ئۇيغۇر', 'NOUN'), ('ئاپتونوم', 'ADJ'), ('رايونىنىڭ', 'NOUN'), ('ئېيتقان', 'VERB'), ('بىر', 'NUM'), ('تۈركىي', 'ADJ'), ('تىلى', 'NOUN'), ('.', 'PUNCT')],
        results_lemmatize = ['ئۇيغۇر', 'تىل', 'ئۇيغۇر', 'جۇڭگو', 'شىنجاڭ', 'ئۇيغۇر', 'ئاپتونوم', 'رايون', 'ئېيتقان', 'بىر', 'تۈركىي', 'تىل', '.'],
        results_dependency_parse = [('ئۇيغۇر', 'تىلى', 'compound', 1), ('تىلى', 'تىلى', 'nsubj', 10), ('ئۇيغۇر', 'جۇڭگو', 'compound', 1), ('جۇڭگو', 'تىلى', 'nsubj', 8), ('شىنجاڭ', 'ئۇيغۇر', 'compound', 1), ('ئۇيغۇر', 'رايونىنىڭ', 'nmod', 2), ('ئاپتونوم', 'رايونىنىڭ', 'nmod', 1), ('رايونىنىڭ', 'تىلى', 'nmod:poss', 4), ('ئېيتقان', 'تىلى', 'acl', 3), ('بىر', 'تىلى', 'nummod', 2), ('تۈركىي', 'تىلى', 'amod', 1), ('تىلى', 'تىلى', 'root', 0), ('.', 'تىلى', 'punct', -1)]
    )

if __name__ == '__main__':
    test_stanza_uig()
