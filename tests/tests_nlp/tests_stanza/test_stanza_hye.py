# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Armenian
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

results_sentence_tokenize = ['Հայոց լեզվով ստեղծվել է մեծ գրականություն։', 'Գրաբարով է ավանդված հայ հին պատմագրությունը, գիտափիլիսոփայական, մաթեմատիկական, բժշկագիտական, աստվածաբանական-դավանաբանական գրականությունը։', 'Միջին գրական հայերենով են մեզ հասել միջնադարյան հայ քնարերգության գլուխգործոցները, բժշկագիտական, իրավագիտական նշանակալի աշխատություններ։', 'Գրական նոր հայերենի արևելահայերեն ու արևմտահայերեն գրական տարբերակներով ստեղծվել է գեղարվեստական, հրապարակախոսական ու գիտական բազմատիպ ու բազմաբնույթ հարուստ գրականություն։']
results_word_tokenize = ['Հայոց', 'լեզվով', 'ստեղծվել', 'է', 'մեծ', 'գրականություն', '։', 'Գրաբարով', 'է', 'ավանդված', 'հայ', 'հին', 'պատմագրությունը', ',', 'գիտափիլիսոփայական', ',', 'մաթեմատիկական', ',', 'բժշկագիտական', ',', 'աստվածաբանական', '-', 'դավանաբանական', 'գրականությունը', '։']
results_pos_tag = [('Հայոց', 'NOUN'), ('լեզվով', 'NOUN'), ('ստեղծվել', 'VERB'), ('է', 'AUX'), ('մեծ', 'ADJ'), ('գրականություն', 'NOUN'), ('։', 'PUNCT'), ('Գրաբարով', 'NOUN'), ('է', 'AUX'), ('ավանդված', 'VERB'), ('հայ', 'ADJ'), ('հին', 'ADJ'), ('պատմագրությունը', 'NOUN'), (',', 'PUNCT'), ('գիտափիլիսոփայական', 'ADJ'), (',', 'PUNCT'), ('մաթեմատիկական', 'ADJ'), (',', 'PUNCT'), ('բժշկագիտական', 'ADJ'), (',', 'PUNCT'), ('աստվածաբանական', 'ADJ'), ('-', 'PUNCT'), ('դավանաբանական', 'ADJ'), ('գրականությունը', 'NOUN'), ('։', 'PUNCT')]

def test_stanza_hye():
    test_stanza.wl_test_stanza(
        lang = 'hye',
        results_sentence_tokenize = results_sentence_tokenize,
        results_word_tokenize = results_word_tokenize,
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['հայ', 'լեզու', 'ստեղծվել', 'եմ', 'մեծ', 'գրականություն', '։', 'գրաբար', 'եմ', 'ավանդել', 'հայ', 'հին', 'պատմագրություն', ',', 'գիտափիլիսոփայական', ',', 'մաթեմատիկական', ',', 'բժշկագիտական', ',', 'աստվածաբանական', '-', 'դավանաբանական', 'գրականություն', '։'],
        results_dependency_parse = [('Հայոց', 'լեզվով', 'nmod:poss', 1), ('լեզվով', 'ստեղծվել', 'obl', 1), ('ստեղծվել', 'ստեղծվել', 'root', 0), ('է', 'ստեղծվել', 'aux', -1), ('մեծ', 'գրականություն', 'amod', 1), ('գրականություն', 'ստեղծվել', 'nsubj', -3), ('։', 'ստեղծվել', 'punct', -4), ('Գրաբարով', 'ավանդված', 'obl', 2), ('է', 'Գրաբարով', 'cop', -1), ('ավանդված', 'ավանդված', 'root', 0), ('հայ', 'պատմագրությունը', 'amod', 2), ('հին', 'պատմագրությունը', 'amod', 1), ('պատմագրությունը', 'ավանդված', 'nsubj:pass', -3), (',', 'գիտափիլիսոփայական', 'punct', 1), ('գիտափիլիսոփայական', 'գրականությունը', 'amod', 9), (',', 'մաթեմատիկական', 'punct', 1), ('մաթեմատիկական', 'գիտափիլիսոփայական', 'conj', -2), (',', 'բժշկագիտական', 'punct', 1), ('բժշկագիտական', 'գիտափիլիսոփայական', 'conj', -4), (',', 'աստվածաբանական', 'punct', 1), ('աստվածաբանական', 'գիտափիլիսոփայական', 'conj', -6), ('-', 'դավանաբանական', 'punct', 1), ('դավանաբանական', 'գիտափիլիսոփայական', 'conj', -8), ('գրականությունը', 'պատմագրությունը', 'conj', -11), ('։', 'ավանդված', 'punct', -15)]
    )

def test_stanza_hyw():
    test_stanza.wl_test_stanza(
        lang = 'hyw',
        results_sentence_tokenize = results_sentence_tokenize,
        results_word_tokenize = results_word_tokenize,
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['Հայ', 'լեզվ', 'ստեղծվել', 'եմ', 'մեծ', 'գրականութիւն', '։', 'գրաբար', 'եմ', 'ավանդվել', 'հայ', 'հին', 'պատմագրութիւն', ',', 'գիտափիլիսոփայական', ',', 'մաթեմատիկական', ',', 'բժշկագիտական', ',', 'աստվածաբանական', '-', 'դավանաբանական', 'գրականութիւն', '։'],
        results_dependency_parse = [('Հայոց', 'լեզվով', 'nmod:poss', 1), ('լեզվով', 'ստեղծվել', 'obl', 1), ('ստեղծվել', 'ստեղծվել', 'root', 0), ('է', 'ստեղծվել', 'aux', -1), ('մեծ', 'գրականություն', 'amod', 1), ('գրականություն', 'ստեղծվել', 'obj', -3), ('։', 'ստեղծվել', 'punct', -4), ('Գրաբարով', 'ավանդված', 'obl', 2), ('է', 'ավանդված', 'aux', 1), ('ավանդված', 'ավանդված', 'root', 0), ('հայ', 'պատմագրությունը', 'amod', 2), ('հին', 'պատմագրությունը', 'amod', 1), ('պատմագրությունը', 'ավանդված', 'nsubj', -3), (',', 'գրականությունը', 'punct', 10), ('գիտափիլիսոփայական', 'գրականությունը', 'amod', 9), (',', 'մաթեմատիկական', 'punct', 1), ('մաթեմատիկական', 'գիտափիլիսոփայական', 'conj', -2), (',', 'բժշկագիտական', 'punct', 1), ('բժշկագիտական', 'գիտափիլիսոփայական', 'conj', -4), (',', 'աստվածաբանական', 'punct', 1), ('աստվածաբանական', 'գիտափիլիսոփայական', 'conj', -6), ('-', 'դավանաբանական', 'punct', 1), ('դավանաբանական', 'գիտափիլիսոփայական', 'conj', -8), ('գրականությունը', 'պատմագրությունը', 'conj', -11), ('։', 'ավանդված', 'punct', -15)]
    )

if __name__ == '__main__':
    test_stanza_hye()
    test_stanza_hyw()
