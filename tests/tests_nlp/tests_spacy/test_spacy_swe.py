# ----------------------------------------------------------------------
# Tests: NLP - spaCy - Swedish
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

from tests.tests_nlp.tests_spacy import test_spacy

def test_spacy_swe():
    results_sentence_tokenize = ['Svenska (svenska\u2009(info)) är ett östnordiskt språk som talas av ungefär tio miljoner personer främst i Sverige där språket har en dominant ställning som huvudspråk, men även som det ena nationalspråket i Finland och som enda officiella språk på Åland.', 'I övriga Finland talas det som modersmål framförallt i de finlandssvenska kustområdena i Österbotten, Åboland och Nyland.', 'En liten minoritet svenskspråkiga finns även i Estland.', 'Svenska är nära besläktat och i hög grad ömsesidigt begripligt med danska och norska.', 'De andra nordiska språken, isländska och färöiska, är mindre ömsesidigt begripliga med svenska.', 'Liksom de övriga nordiska språken härstammar svenskan från en gren av fornnordiska, vilket var det språk som talades av de germanska folken i Skandinavien.']

    test_spacy.wl_test_spacy(
        lang = 'swe',
        results_sentence_tokenize_trf = results_sentence_tokenize,
        results_sentence_tokenize_lg = results_sentence_tokenize,
        results_word_tokenize = ['Svenska', '(', 'svenska', '(', 'info', ')', ')', 'är', 'ett', 'östnordiskt', 'språk', 'som', 'talas', 'av', 'ungefär', 'tio', 'miljoner', 'personer', 'främst', 'i', 'Sverige', 'där', 'språket', 'har', 'en', 'dominant', 'ställning', 'som', 'huvudspråk', ',', 'men', 'även', 'som', 'det', 'ena', 'nationalspråket', 'i', 'Finland', 'och', 'som', 'enda', 'officiella', 'språk', 'på', 'Åland', '.'],
        results_pos_tag = [('Svenska', 'JJ|POS|UTR/NEU|SIN|DEF|NOM'), ('(', 'PAD'), ('svenska', 'JJ|POS|UTR/NEU|SIN|DEF|NOM'), ('(', 'PAD'), ('info', 'NN|UTR|SIN|IND|NOM'), (')', 'PAD'), (')', 'PAD'), ('är', 'VB|PRS|AKT'), ('ett', 'DT|NEU|SIN|IND'), ('östnordiskt', 'JJ|POS|NEU|SIN|IND|NOM'), ('språk', 'NN|NEU|SIN|IND|NOM'), ('som', 'HP|-|-|-'), ('talas', 'VB|PRS|SFO'), ('av', 'PP'), ('ungefär', 'AB'), ('tio', 'RG|NOM'), ('miljoner', 'NN|UTR|PLU|IND|NOM'), ('personer', 'NN|UTR|PLU|IND|NOM'), ('främst', 'AB|SUV'), ('i', 'PP'), ('Sverige', 'PM|NOM'), ('där', 'HA'), ('språket', 'NN|NEU|SIN|DEF|NOM'), ('har', 'VB|PRS|AKT'), ('en', 'DT|UTR|SIN|IND'), ('dominant', 'JJ|POS|UTR|SIN|IND|NOM'), ('ställning', 'NN|UTR|SIN|IND|NOM'), ('som', 'KN'), ('huvudspråk', 'NN|NEU|SIN|IND|NOM'), (',', 'MID'), ('men', 'KN'), ('även', 'AB'), ('som', 'HA'), ('det', 'DT|NEU|SIN|DEF'), ('ena', 'JJ|POS|UTR/NEU|SIN/PLU|IND/DEF|NOM'), ('nationalspråket', 'NN|NEU|SIN|DEF|NOM'), ('i', 'PP'), ('Finland', 'PM|NOM'), ('och', 'KN'), ('som', 'HP|-|-|-'), ('enda', 'JJ|POS|UTR/NEU|SIN/PLU|IND/DEF|NOM'), ('officiella', 'JJ|POS|UTR/NEU|PLU|IND/DEF|NOM'), ('språk', 'NN|NEU|PLU|IND|NOM'), ('på', 'PP'), ('Åland', 'PM|NOM'), ('.', 'MAD')],
        results_pos_tag_universal = [('Svenska', 'ADJ'), ('(', 'PUNCT'), ('svenska', 'ADJ'), ('(', 'PUNCT'), ('info', 'NOUN'), (')', 'PUNCT'), (')', 'PUNCT'), ('är', 'AUX'), ('ett', 'DET'), ('östnordiskt', 'ADJ'), ('språk', 'NOUN'), ('som', 'PRON'), ('talas', 'VERB'), ('av', 'ADP'), ('ungefär', 'ADV'), ('tio', 'NUM'), ('miljoner', 'NOUN'), ('personer', 'NOUN'), ('främst', 'ADV'), ('i', 'ADP'), ('Sverige', 'PROPN'), ('där', 'ADV'), ('språket', 'NOUN'), ('har', 'VERB'), ('en', 'DET'), ('dominant', 'ADJ'), ('ställning', 'NOUN'), ('som', 'SCONJ'), ('huvudspråk', 'NOUN'), (',', 'PUNCT'), ('men', 'CCONJ'), ('även', 'ADV'), ('som', 'ADV'), ('det', 'DET'), ('ena', 'ADJ'), ('nationalspråket', 'NOUN'), ('i', 'ADP'), ('Finland', 'PROPN'), ('och', 'CCONJ'), ('som', 'PRON'), ('enda', 'ADJ'), ('officiella', 'ADJ'), ('språk', 'NOUN'), ('på', 'ADP'), ('Åland', 'PROPN'), ('.', 'PUNCT')],
        results_lemmatize = ['Svenska', '(', 'svensk', '(', 'info', ')', ')', 'vara', 'en', 'östnordisk', 'språk', 'som', 'tala', 'av', 'ungefär', 'tio', 'miljon', 'person', 'främst', 'i', 'Sverige', 'där', 'språk', 'ha', 'en', 'dominant', 'ställning', 'som', 'huvudspråk', ',', 'men', 'även', 'som', 'en', 'ena', 'nationalspråk', 'i', 'Finland', 'och', 'som', 'enda', 'officiell', 'språk', 'på', 'Åland', '.'],
        results_dependency_parse = [('Svenska', 'språk', 'nsubj', 11), ('(', 'Svenska', 'punct', -1), ('svenska', 'Svenska', 'appos', -2), ('\u2009', 'svenska', 'dep', -1), ('(', 'Svenska', 'punct', -4), ('info', 'Svenska', 'appos', -5), (')', 'Svenska', 'punct', -6), (')', 'Svenska', 'punct', -7), ('är', 'språk', 'cop', 3), ('ett', 'språk', 'det', 2), ('östnordiskt', 'språk', 'amod', 1), ('språk', 'språk', 'ROOT', 0), ('som', 'talas', 'nsubj:pass', 1), ('talas', 'språk', 'acl:relcl', -2), ('av', 'personer', 'case', 4), ('ungefär', 'tio', 'advmod', 1), ('tio', 'miljoner', 'nummod', 1), ('miljoner', 'personer', 'nmod', 1), ('personer', 'talas', 'obl:agent', -5), ('främst', 'Sverige', 'advmod', 2), ('i', 'Sverige', 'case', 1), ('Sverige', 'talas', 'obl', -8), ('där', 'har', 'advmod', 2), ('språket', 'har', 'nsubj', 1), ('har', 'Sverige', 'acl:relcl', -3), ('en', 'ställning', 'det', 2), ('dominant', 'ställning', 'amod', 1), ('ställning', 'har', 'obj', -3), ('som', 'huvudspråk', 'mark', 1), ('huvudspråk', 'har', 'xcomp', -5), (',', 'nationalspråket', 'punct', 6), ('men', 'nationalspråket', 'cc', 5), ('även', 'nationalspråket', 'advmod', 4), ('som', 'nationalspråket', 'case', 3), ('det', 'nationalspråket', 'det', 2), ('ena', 'nationalspråket', 'amod', 1), ('nationalspråket', 'språk', 'conj', -25), ('i', 'Finland', 'case', 1), ('Finland', 'nationalspråket', 'nmod', -2), ('och', 'språk', 'cc', 4), ('som', 'språk', 'mark', 3), ('enda', 'språk', 'amod', 2), ('officiella', 'språk', 'amod', 1), ('språk', 'Finland', 'conj', -5), ('på', 'Åland', 'case', 1), ('Åland', 'språk', 'nmod', -2), ('.', 'språk', 'punct', -35)]
    )

if __name__ == '__main__':
    test_spacy_swe()
