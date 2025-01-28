# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Hebrew (Ancient)
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

def test_stanza_hbo():
    test_stanza.wl_test_stanza(
        lang = 'hbo',
        results_sentence_tokenize = ['וַ֠יָּבֹאוּ שְׁנֵ֨י הַמַּלְאָכִ֤ים סְדֹ֨מָה֙ בָּעֶ֔רֶב וְלֹ֖וט יֹשֵׁ֣ב בְּשַֽׁעַר־סְדֹ֑ם וַיַּרְא־לֹוט֙ וַיָּ֣קָם לִקְרָאתָ֔ם וַיִּשְׁתַּ֥חוּ אַפַּ֖יִם אָֽרְצָה׃', 'וַיֹּ֜אמֶר הִנֶּ֣ה נָּא־אֲדֹנַ֗י ס֣וּרוּ נָ֠א אֶל־בֵּ֨ית עַבְדְּכֶ֤ם וְלִ֨ינוּ֙ וְרַחֲצ֣וּ רַגְלֵיכֶ֔ם וְהִשְׁכַּמְתֶּ֖ם וַהְלַכְתֶּ֣ם לְדַרְכְּכֶ֑ם וַיֹּאמְר֣וּ לֹּ֔א כִּ֥י בָרְחֹ֖וב נָלִֽין׃'],
        results_word_tokenize = ['וַ֠יָּבֹאוּ', 'שְׁנֵ֨י', 'הַמַּלְאָכִ֤ים', 'סְדֹ֨מָה֙', 'בָּעֶ֔רֶב', 'וְלֹ֖וט', 'יֹשֵׁ֣ב', 'בְּשַֽׁעַר', '־', 'סְדֹ֑ם', 'וַיַּרְא', '־', 'לֹוט֙', 'וַיָּ֣קָם', 'לִקְרָאתָ֔ם', 'וַיִּשְׁתַּ֥חוּ', 'אַפַּ֖יִם', 'אָֽרְצָה', '׃'],
        results_pos_tag = [('ו', 'conj'), ('בוא', 'verb'), ('שְׁנֵ֨י', 'subs'), ('ה', 'art'), ('מלאך', 'subs'), ('סְדֹ֨מָה֙', 'subs'), ('ב', 'prep'), ('ה', 'art'), ('ערב', 'subs'), ('ו', 'conj'), ('לוט', 'nmpr'), ('יֹשֵׁ֣ב', 'verb'), ('ב', 'prep'), ('שׁער', 'verb'), ('־', 'punct'), ('סְדֹ֑ם', 'subs'), ('ו', 'conj'), ('ראה', 'verb'), ('־', 'punct'), ('לֹוט֙', 'subs'), ('ו', 'conj'), ('קום', 'verb'), ('ל', 'prep'), ('קרא', 'verb'), ('הם', 'prn'), ('ו', 'conj'), ('חוה', 'verb'), ('אַפַּ֖יִם', 'subs'), ('אָֽרְצָה', 'subs'), ('׃', 'punct')],
        results_pos_tag_universal = [('ו', 'CCONJ'), ('בוא', 'VERB'), ('שְׁנֵ֨י', 'NOUN'), ('ה', 'DET'), ('מלאך', 'NOUN'), ('סְדֹ֨מָה֙', 'NOUN'), ('ב', 'ADP'), ('ה', 'DET'), ('ערב', 'NOUN'), ('ו', 'CCONJ'), ('לוט', 'PROPN'), ('יֹשֵׁ֣ב', 'NOUN'), ('ב', 'ADP'), ('שׁער', 'VERB'), ('־', 'PUNCT'), ('סְדֹ֑ם', 'NOUN'), ('ו', 'CCONJ'), ('ראה', 'VERB'), ('־', 'PUNCT'), ('לֹוט֙', 'ADV'), ('ו', 'CCONJ'), ('קום', 'VERB'), ('ל', 'ADP'), ('קרא', 'VERB'), ('הם', 'PRON'), ('ו', 'CCONJ'), ('חוה', 'VERB'), ('אַפַּ֖יִם', 'NOUN'), ('אָֽרְצָה', 'NOUN'), ('׃', 'PUNCT')],
        results_lemmatize = ['ו', 'בוא', 'שׁנה', 'ה', 'מלאך', 'סדומה', 'ב', 'ה', 'ערב', 'ו', 'לוט', 'ישׁב', 'ב', 'שׁער', '־', 'סדם', 'ו', 'ראה', '־', 'לוט', 'ו', 'קום', 'ל', 'קרא', 'הם', 'ו', 'חוה', 'אף', 'ארץ', '׃'],
        results_dependency_parse = [('ו', 'בוא', 'cc', 1), ('בוא', 'בוא', 'root', 0), ('שְׁנֵ֨י', 'בוא', 'nsubj', -1), ('ה', 'מלאך', 'det', 1), ('מלאך', 'שְׁנֵ֨י', 'compound:smixut', -2), ('סְדֹ֨מָה֙', 'בוא', 'obj', -4), ('ב', 'ערב', 'case', 2), ('ה', 'ערב', 'det', 1), ('ערב', 'בוא', 'obl', -7), ('ו', 'לוט', 'cc', 1), ('לוט', 'בוא', 'conj', -9), ('יֹשֵׁ֣ב', 'לוט', 'nsubj', -1), ('ב', 'שׁער', 'case', 1), ('שׁער', 'יֹשֵׁ֣ב', 'acl', -2), ('־', 'סְדֹ֑ם', 'punct', 1), ('סְדֹ֑ם', 'שׁער', 'obj', -2), ('ו', 'ראה', 'cc', 1), ('ראה', 'בוא', 'conj', -16), ('־', 'לֹוט֙', 'punct', 1), ('לֹוט֙', 'ראה', 'advmod', -2), ('ו', 'קום', 'cc', 1), ('קום', 'בוא', 'conj', -20), ('ל', 'קרא', 'case', 1), ('קרא', 'קום', 'advcl', -2), ('הם', 'קרא', 'obj', -1), ('ו', 'חוה', 'cc', 1), ('חוה', 'בוא', 'conj', -25), ('אַפַּ֖יִם', 'חוה', 'nsubj', -1), ('אָֽרְצָה', 'חוה', 'obl', -2), ('׃', 'בוא', 'punct', -28)]
    )

if __name__ == '__main__':
    test_stanza_hbo()
