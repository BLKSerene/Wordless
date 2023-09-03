# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Stanza - Maltese
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

def test_stanza_mlt():
    test_stanza.wl_test_stanza(
        lang = 'mlt',
        results_sentence_tokenize = ["Il-Malti huwa l-ilsien nazzjonali tar-Repubblika ta' Malta.", "Huwa l-ilsien uffiċjali flimkien mal-Ingliż; kif ukoll wieħed mill-ilsna uffiċjali u l-uniku wieħed ta' oriġini Għarbija (Semitiku) tal-Unjoni Ewropea.", "Dan l-ilsien għandu sisien u għerq semitiku, ta' djalett Għarbi li ġej mit-Tramuntana tal-Afrika, għalħekk qatt ma kellu rabta mill-qrib mal-Għarbi Klassiku.", "Iżda tul iż-żminijiet, minħabba proċess tal-Latinizzazzjoni ta' Malta, bdew deħlin bosta elementi lingwistiċi mill-Isqalli, djalett ta' art li wkoll għaddiet minn żmien ta' ħakma Għarbija.", "Wara l-Isqalli beda dieħel ukoll it-Taljan, fuq kollox fiż-żmien tad-daħla tal-Kavallieri tal-Ordni ta' San Ġwann sa meta l-Ingliż ħa post it-Taljan bħala l-ilsien uffiċjali fil-Kostituzzjoni Kolonjali tal-1934.", "Il-Malti huwa l-ilsien waħdieni ta' għajn semitika li jinkiteb b'ittri Latini.", 'Studju tal-2016 juri li, fil-lingwaġġ bażiku ta’ kuljum, il-Maltin kapaċi jifhmu madwar terz ta’ dak li jingħad lilhom bl-Għarbi Tuneżin li huwa Għarbi tal-Maghrebi relatat mal-Għarbi Sqalli, filwaqt li dawk li jitkellmu bl-Għarbi Tuneżin (Tuneżin) huma kapaċi jifhmu madwar 40% ta’ dak li jingħad lilhom bil-Malti.', '[1]'],
        results_word_tokenize = ['Il-', 'Malti', 'huwa', 'l-', 'ilsien', 'nazzjonali', 'tar-', 'Repubblika', "ta'", 'Malta', '.'],
        results_pos_tag = [('Il-', 'DEF'), ('Malti', 'NOUN'), ('huwa', 'PRON_PERS'), ('l-', 'DEF'), ('ilsien', 'NOUN'), ('nazzjonali', 'ADJ'), ('tar-', 'GEN_DEF'), ('Repubblika', 'NOUN'), ("ta'", 'GEN'), ('Malta', 'NOUN_PROP'), ('.', 'X_PUN')],
        results_pos_tag_universal = [('Il-', 'DET'), ('Malti', 'NOUN'), ('huwa', 'PRON'), ('l-', 'DET'), ('ilsien', 'NOUN'), ('nazzjonali', 'ADJ'), ('tar-', 'ADP'), ('Repubblika', 'NOUN'), ("ta'", 'ADP'), ('Malta', 'PROPN'), ('.', 'PUNCT')],
        results_dependency_parse = [('Il-', 'Malti', 'det', 1), ('Malti', 'ilsien', 'nsubj', 3), ('huwa', 'ilsien', 'cop', 2), ('l-', 'ilsien', 'det', 1), ('ilsien', 'ilsien', 'root', 0), ('nazzjonali', 'ilsien', 'amod', -1), ('tar-', 'Repubblika', 'case:det', 1), ('Repubblika', 'ilsien', 'nmod:poss', -3), ("ta'", 'Malta', 'case', 1), ('Malta', 'Repubblika', 'nmod:poss', -2), ('.', 'ilsien', 'punct', -6)]
    )

if __name__ == '__main__':
    test_stanza_mlt()
