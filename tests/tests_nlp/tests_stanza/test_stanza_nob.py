# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Norwegian (Bokmål)
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

def test_stanza_nob():
    test_stanza.wl_test_stanza(
        lang = 'nob',
        results_sentence_tokenize = ['Bokmål er en av to offisielle målformer av norsk skriftspråk, hvorav den andre er nynorsk.', 'I skrift har 87,3% bokmål som hovedmål i skolen.', '[1] Etter skriftreformene av riksmål i 1987 og bokmål i 1981 og 2005 er det lite som skiller bokmål og riksmål i alminnelig bruk.'],
        results_word_tokenize = ['Bokmål', 'er', 'en', 'av', 'to', 'offisielle', 'målformer', 'av', 'norsk', 'skriftspråk', ',', 'hvorav', 'den', 'andre', 'er', 'nynorsk', '.'],
        results_pos_tag = [('Bokmål', 'subst'), ('er', 'verb'), ('en', 'det'), ('av', 'prep'), ('to', 'det'), ('offisielle', 'adj'), ('målformer', 'subst'), ('av', 'prep'), ('norsk', 'adj'), ('skriftspråk', 'subst'), (',', '<komma>'), ('hvorav', 'adv'), ('den', 'det'), ('andre', 'det'), ('er', 'verb'), ('nynorsk', 'adj'), ('.', 'clb')],
        results_pos_tag_universal = [('Bokmål', 'NOUN'), ('er', 'AUX'), ('en', 'DET'), ('av', 'ADP'), ('to', 'NUM'), ('offisielle', 'ADJ'), ('målformer', 'NOUN'), ('av', 'ADP'), ('norsk', 'ADJ'), ('skriftspråk', 'NOUN'), (',', 'PUNCT'), ('hvorav', 'ADV'), ('den', 'DET'), ('andre', 'DET'), ('er', 'AUX'), ('nynorsk', 'ADJ'), ('.', 'PUNCT')],
        results_lemmatize = ['bokmål', 'være', 'en', 'av', 'to', 'offisiell', 'målform', 'av', 'norsk', 'skriftspråk', '$,', 'hvorav', 'den', 'annen', 'være', 'nynorsk', '$.'],
        results_dependency_parse = [('Bokmål', 'en', 'nsubj', 2), ('er', 'en', 'cop', 1), ('en', 'en', 'root', 0), ('av', 'målformer', 'case', 3), ('to', 'målformer', 'nummod', 2), ('offisielle', 'målformer', 'amod', 1), ('målformer', 'en', 'nmod', -4), ('av', 'skriftspråk', 'case', 2), ('norsk', 'skriftspråk', 'amod', 1), ('skriftspråk', 'målformer', 'nmod', -3), (',', 'nynorsk', 'punct', 5), ('hvorav', 'nynorsk', 'advmod', 4), ('den', 'andre', 'det', 1), ('andre', 'nynorsk', 'nsubj', 2), ('er', 'nynorsk', 'cop', 1), ('nynorsk', 'en', 'conj', -13), ('.', 'en', 'punct', -14)]
    )

if __name__ == '__main__':
    test_stanza_nob()
