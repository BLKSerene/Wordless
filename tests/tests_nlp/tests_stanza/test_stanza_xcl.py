# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Armenian (Classical)
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

results_pos_tag = [('Զգոյշ', 'ADJ'), ('լերուք', 'AUX'), ('ողորմութեան', 'NOUN'), ('ձերում', 'DET'), ('՝', 'PUNCT'), ('մի', 'PART'), ('առնել', 'VERB'), ('առաջի', 'ADP'), ('մարդկան', 'NOUN'), ('՝', 'PUNCT'), ('որպէս', 'ADV'), ('թե', 'SCONJ'), ('ի', 'ADP'), ('ցոյց', 'NOUN'), ('ինչ', 'PRON'), ('նոցա', 'PRON'), (',', 'PUNCT'), ('գուցէ', 'PART'), ('եւ', 'CCONJ'), ('վարձս', 'NOUN'), ('ոչ', 'PART'), ('ընդունիցիք', 'VERB'), ('ի', 'ADP'), ('հաւրէ', 'NOUN'), ('ձերմէ', 'DET'), ('որ', 'PRON'), ('յ', 'ADP'), ('երկինս', 'NOUN'), ('ն', 'DET'), ('է', 'AUX'), (':', 'PUNCT')]

def test_stanza_xcl():
    test_stanza.wl_test_stanza(
        lang = 'xcl',
        results_sentence_tokenize = ['Զգոյշ լերուք ողորմութեան ձերում՝ մի առնել առաջի մարդկան՝ որպէս թե ի ցոյց ինչ նոցա, գուցէ եւ վարձս ոչ ընդունիցիք ի հաւրէ ձերմէ որ յերկինսն է:', 'Այղ յորժամ առնիցես ողորմութիւն, մի հարկաներ փող առաջի քո. որպէս կեղծաւորքն առնեն ի ժողովուրդս եւ ի հրապարակս. որպէս զի փառաւորեսցին ի մարդկանէ:'],
        results_word_tokenize = ['Զգոյշ', 'լերուք', 'ողորմութեան', 'ձերում', '՝', 'մի', 'առնել', 'առաջի', 'մարդկան', '՝', 'որպէս', 'թե', 'ի', 'ցոյց', 'ինչ', 'նոցա', ',', 'գուցէ', 'եւ', 'վարձս', 'ոչ', 'ընդունիցիք', 'ի', 'հաւրէ', 'ձերմէ', 'որ', 'յ', 'երկինս', 'ն', 'է', ':'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['զգոյշ', 'լինիմ', 'ողորմութիւն', 'ձեր', '՝', 'մի', 'առնեմ', 'առաջի', 'մարդիկ', '՝', 'որպէս', 'թե', 'ի', 'ցոյց', 'ինչ', 'նա', ',', 'գուցէ', 'եւ', 'վարձ', 'ոչ', 'ընդունիմ', 'ի', 'հայր', 'ձեր', 'որ', 'ի', 'երկին', 'ն', 'եմ', ':'],
        results_dependency_parse = [('Զգոյշ', 'Զգոյշ', 'root', 0), ('լերուք', 'Զգոյշ', 'cop', -1), ('ողորմութեան', 'Զգոյշ', 'iobj', -2), ('ձերում', 'ողորմութեան', 'det', -1), ('՝', 'առնել', 'punct', 2), ('մի', 'առնել', 'advmod', 1), ('առնել', 'Զգոյշ', 'xcomp', -6), ('առաջի', 'մարդկան', 'case', 1), ('մարդկան', 'առնել', 'obl', -2), ('՝', 'ցոյց', 'punct', 4), ('որպէս', 'ցոյց', 'mark', 3), ('թե', 'ցոյց', 'mark', 2), ('ի', 'ցոյց', 'case', 1), ('ցոյց', 'ընդունիցիք', 'advcl', 8), ('ինչ', 'ցոյց', 'det', -1), ('նոցա', 'ցոյց', 'nmod', -2), (',', 'ընդունիցիք', 'punct', 5), ('գուցէ', 'ընդունիցիք', 'discourse', 4), ('եւ', 'վարձս', 'cc', 1), ('վարձս', 'ընդունիցիք', 'obj', 2), ('ոչ', 'ընդունիցիք', 'advmod', 1), ('ընդունիցիք', 'առնել', 'advcl', -15), ('ի', 'հաւրէ', 'case', 1), ('հաւրէ', 'ընդունիցիք', 'obl', -2), ('ձերմէ', 'հաւրէ', 'det', -1), ('որ', 'երկինս', 'nsubj', 2), ('յ', 'երկինս', 'case', 1), ('երկինս', 'հաւրէ', 'acl', -4), ('ն', 'երկինս', 'det', -1), ('է', 'երկինս', 'cop', -2), (':', 'Զգոյշ', 'punct', -30)]
    )

if __name__ == '__main__':
    test_stanza_xcl()
