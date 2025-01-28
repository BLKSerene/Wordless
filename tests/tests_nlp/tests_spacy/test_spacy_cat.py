# ----------------------------------------------------------------------
# Tests: NLP - spaCy - Catalan
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

def test_spacy_cat():
    results_pos_tag = [('El', 'DET'), ('català', 'NOUN'), ('té', 'VERB'), ('cinc', 'NUM'), ('grans', 'ADJ'), ('dialectes', 'NOUN'), ('(', 'PUNCT'), ('valencià', 'PROPN'), (',', 'PUNCT'), ('nord-occidental', 'ADJ'), (',', 'PUNCT'), ('central', 'ADJ'), (',', 'PUNCT'), ('balear', 'ADJ'), ('i', 'CCONJ'), ('rossellonès', 'NOUN'), (')', 'PUNCT'), ('que', 'PRON'), ('juntament', 'ADV'), ('amb', 'ADP'), ("l'", 'DET'), ('alguerès', 'NOUN'), (',', 'PUNCT'), ('es', 'PRON'), ('divideixen', 'VERB'), ('fins', 'ADV'), ('a', 'ADP'), ('vint-i-una', 'NUM'), ('varietats', 'NOUN'), ('i', 'CCONJ'), ("s'", 'PRON'), ('agrupen', 'VERB'), ('en', 'ADP'), ('dos', 'NUM'), ('grans', 'ADJ'), ('blocs', 'NOUN'), (':', 'PUNCT'), ('el', 'DET'), ('català', 'NOUN'), ('occidental', 'ADJ'), ('i', 'CCONJ'), ('el', 'DET'), ('català', 'NOUN'), ('oriental', 'ADJ'), ('.', 'PUNCT')]

    test_spacy.wl_test_spacy(
        lang = 'cat',
        results_sentence_tokenize_trf = ["El català té cinc grans dialectes (valencià, nord-occidental, central, balear i rossellonès) que juntament amb l'alguerès, es divideixen fins a vint-i-una varietats i s'agrupen en dos grans blocs: el català occidental i el català oriental.", 'Les propostes normatives permeten reduir les diferències entre aquests dialectes en el català estàndard des del punt de vista gramatical, fonètic i de lèxic.'],
        results_word_tokenize = ['El', 'català', 'té', 'cinc', 'grans', 'dialectes', '(', 'valencià', ',', 'nord-occidental', ',', 'central', ',', 'balear', 'i', 'rossellonès', ')', 'que', 'juntament', 'amb', "l'", 'alguerès', ',', 'es', 'divideixen', 'fins', 'a', 'vint-i-una', 'varietats', 'i', "s'", 'agrupen', 'en', 'dos', 'grans', 'blocs', ':', 'el', 'català', 'occidental', 'i', 'el', 'català', 'oriental', '.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['el', 'català', 'tenir', 'cinc', 'gran', 'dialecte', '(', 'valencià', ',', 'nord-occidental', ',', 'central', ',', 'balear', 'i', 'rossellonè', ')', 'que', 'juntament', 'amb', 'el', 'alguerès', ',', 'se', 'dividir', 'fins', 'a', 'vint-i-un', 'varietat', 'i', 'se', 'agrupar', 'en', 'dos', 'gran', 'bloc', ':', 'el', 'català', 'occidental', 'i', 'el', 'català', 'oriental', '.'],
        results_dependency_parse = [('El', 'català', 'det', 1), ('català', 'té', 'nsubj', 1), ('té', 'té', 'ROOT', 0), ('cinc', 'dialectes', 'nummod', 2), ('grans', 'dialectes', 'amod', 1), ('dialectes', 'té', 'obj', -3), ('(', 'valencià', 'punct', 1), ('valencià', 'dialectes', 'appos', -2), (',', 'nord-occidental', 'punct', 1), ('nord-occidental', 'valencià', 'conj', -2), (',', 'central', 'punct', 1), ('central', 'valencià', 'conj', -4), (',', 'balear', 'punct', 1), ('balear', 'valencià', 'conj', -6), ('i', 'rossellonès', 'cc', 1), ('rossellonès', 'valencià', 'conj', -8), (')', 'valencià', 'punct', -9), ('que', 'divideixen', 'nsubj', 7), ('juntament', 'alguerès', 'case', 3), ('amb', 'juntament', 'fixed', -1), ("l'", 'alguerès', 'det', 1), ('alguerès', 'que', 'nmod', -4), (',', 'que', 'punct', -5), ('es', 'divideixen', 'obj', 1), ('divideixen', 'dialectes', 'acl', -19), ('fins', 'vint-i-una', 'advmod', 2), ('a', 'fins', 'fixed', -1), ('vint-i-una', 'varietats', 'nummod', 1), ('varietats', 'divideixen', 'obj', -4), ('i', 'agrupen', 'cc', 2), ("s'", 'agrupen', 'obj', 1), ('agrupen', 'divideixen', 'conj', -7), ('en', 'blocs', 'case', 3), ('dos', 'blocs', 'nummod', 2), ('grans', 'blocs', 'amod', 1), ('blocs', 'agrupen', 'obj', -4), (':', 'català', 'punct', 2), ('el', 'català', 'det', 1), ('català', 'blocs', 'appos', -3), ('occidental', 'català', 'amod', -1), ('i', 'català', 'cc', 2), ('el', 'català', 'det', 1), ('català', 'català', 'conj', -4), ('oriental', 'català', 'amod', -1), ('.', 'té', 'punct', -42)]
    )

if __name__ == '__main__':
    test_spacy_cat()
