# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Hebrew (Modern)
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

def test_stanza_heb():
    results_pos_tag = [('עִבְרִית', 'ADV'), ('היא', 'PRON'), ('שפה', 'NOUN'), ('שמית', 'ADJ'), (',', 'PUNCT'), ('מ', 'ADP'), ('משפחת', 'NOUN'), ('ה', 'DET'), ('שפות', 'NOUN'), ('ה', 'DET'), ('אפרו', 'ADV'), ('-', 'PUNCT'), ('אסיאתיות', 'ADJ'), (',', 'PUNCT'), ('ה', 'SCONJ'), ('ידועה', 'ADJ'), ('כש', 'SCONJ'), ('פתם', 'NOUN'), ('של', 'ADP'), ('ה', 'DET'), ('יהודים', 'NOUN'), ('ו', 'CCONJ'), ('של', 'ADP'), ('ה', 'DET'), ('שומרונים', 'NOUN'), ('.', 'PUNCT')]

    test_stanza.wl_test_stanza(
        lang = 'heb',
        results_sentence_tokenize = ['עִבְרִית היא שפה שמית, ממשפחת השפות האפרו-אסיאתיות, הידועה כשפתם של היהודים ושל השומרונים.', 'העברית היא שפתה הרשמית של מדינת ישראל, מעמד שעוגן בשנת תשע"ח, 2018, בחוק יסוד: ישראל – מדינת הלאום של העם היהודי.'],
        results_word_tokenize = ['עִבְרִית', 'היא', 'שפה', 'שמית', ',', 'ממשפחת', 'השפות', 'האפרו', '-', 'אסיאתיות', ',', 'הידועה', 'כשפתם', 'של', 'היהודים', 'ושל', 'השומרונים', '.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['עִבְרִית', 'הוא', 'שפה', 'שמי', ',', 'מ', 'משפחה', 'ה', 'שפה', 'ה', 'אפרו', '-', 'אסיאתי', ',', 'ה', 'ידוע', 'כש', 'פתם', 'של', 'ה', 'יהודי', 'ו', 'של', 'ה', 'שומרוני', '.'],
        results_dependency_parse = [('עִבְרִית', 'שפה', 'advmod', 2), ('היא', 'שפה', 'nsubj', 1), ('שפה', 'שפה', 'root', 0), ('שמית', 'שפה', 'amod', -1), (',', 'משפחת', 'punct', 2), ('מ', 'משפחת', 'case', 1), ('משפחת', 'שפה', 'nmod', -4), ('ה', 'שפות', 'det', 1), ('שפות', 'משפחת', 'compound', -2), ('ה', 'אסיאתיות', 'det', 3), ('אפרו', 'שפות', 'amod', -2), ('-', 'אסיאתיות', 'punct', 1), ('אסיאתיות', 'אפרו', 'dep', -2), (',', 'ידועה', 'punct', 2), ('ה', 'ידועה', 'mark', 1), ('ידועה', 'שפות', 'acl:relcl', -7), ('כש', 'פתם', 'mark', 1), ('פתם', 'ידועה', 'advcl', -2), ('של', 'יהודים', 'case', 2), ('ה', 'יהודים', 'det', 1), ('יהודים', 'פתם', 'nmod:poss', -3), ('ו', 'שומרונים', 'cc', 3), ('של', 'שומרונים', 'case', 2), ('ה', 'שומרונים', 'det', 1), ('שומרונים', 'יהודים', 'conj', -4), ('.', 'שפה', 'punct', -23)]
    )

if __name__ == '__main__':
    test_stanza_heb()
