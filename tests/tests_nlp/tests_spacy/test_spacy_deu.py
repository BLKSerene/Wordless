# ----------------------------------------------------------------------
# Tests: NLP - spaCy - German
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

def test_spacy_deu():
    test_spacy.wl_test_spacy(
        lang = 'deu_de',
        results_sentence_tokenize_trf = ['Die deutsche Sprache oder Deutsch [dɔɪ̯tʃ][24] ist eine westgermanische Sprache, die weltweit etwa 90 bis 105 Millionen Menschen als Muttersprache und weiteren rund 80 Millionen als Zweit- oder Fremdsprache dient.', 'Das Deutsche ist eine plurizentrische Sprache, enthält also mehrere Standardvarietäten in verschiedenen Regionen.'],
        results_word_tokenize = ['Die', 'deutsche', 'Sprache', 'oder', 'Deutsch', '[', 'dɔɪ̯tʃ][24', ']', 'ist', 'eine', 'westgermanische', 'Sprache', ',', 'die', 'weltweit', 'etwa', '90', 'bis', '105', 'Millionen', 'Menschen', 'als', 'Muttersprache', 'und', 'weiteren', 'rund', '80', 'Millionen', 'als', 'Zweit-', 'oder', 'Fremdsprache', 'dient', '.'],
        results_pos_tag = [('Die', 'ART'), ('deutsche', 'ADJA'), ('Sprache', 'NN'), ('oder', 'KON'), ('Deutsch', 'NN'), ('[', '$('), ('dɔɪ̯tʃ][24', 'NE'), (']', '$('), ('ist', 'VAFIN'), ('eine', 'ART'), ('westgermanische', 'ADJA'), ('Sprache', 'NN'), (',', '$,'), ('die', 'PRELS'), ('weltweit', 'ADJD'), ('etwa', 'ADV'), ('90', 'CARD'), ('bis', 'KON'), ('105', 'CARD'), ('Millionen', 'NN'), ('Menschen', 'NN'), ('als', 'APPR'), ('Muttersprache', 'NN'), ('und', 'KON'), ('weiteren', 'ADJA'), ('rund', 'ADV'), ('80', 'CARD'), ('Millionen', 'NN'), ('als', 'APPR'), ('Zweit-', 'TRUNC'), ('oder', 'KON'), ('Fremdsprache', 'NN'), ('dient', 'VVFIN'), ('.', '$.')],
        results_pos_tag_universal = [('Die', 'DET'), ('deutsche', 'ADJ'), ('Sprache', 'NOUN'), ('oder', 'CCONJ'), ('Deutsch', 'NOUN'), ('[', 'PUNCT'), ('dɔɪ̯tʃ][24', 'PUNCT'), (']', 'PUNCT'), ('ist', 'AUX'), ('eine', 'DET'), ('westgermanische', 'ADJ'), ('Sprache', 'NOUN'), (',', 'PUNCT'), ('die', 'PRON'), ('weltweit', 'ADV'), ('etwa', 'ADV'), ('90', 'NUM'), ('bis', 'CCONJ'), ('105', 'NUM'), ('Millionen', 'NOUN'), ('Menschen', 'NOUN'), ('als', 'ADP'), ('Muttersprache', 'NOUN'), ('und', 'CCONJ'), ('weiteren', 'ADJ'), ('rund', 'ADV'), ('80', 'NUM'), ('Millionen', 'NOUN'), ('als', 'ADP'), ('Zweit-', 'X'), ('oder', 'CCONJ'), ('Fremdsprache', 'NOUN'), ('dient', 'VERB'), ('.', 'PUNCT')],
        results_lemmatize = ['der', 'deutsch', 'Sprache', 'oder', 'Deutsch', '[', 'dɔɪ̯tʃ][24', ']', 'sein', 'ein', 'westgermanisch', 'Sprache', '--', 'der', 'weltweit', 'etwa', '90', 'bis', '105', 'Million', 'Mensch', 'als', 'Muttersprache', 'und', 'weit', 'rund', '80', 'Million', 'als', 'Zweit', 'oder', 'Fremdsprache', 'dienen', '--'],
        results_dependency_parse = [('Die', 'Sprache', 'nk', 2), ('deutsche', 'Sprache', 'nk', 1), ('Sprache', 'ist', 'sb', 6), ('oder', 'Sprache', 'cd', -1), ('Deutsch', 'oder', 'cj', -1), ('[', 'Sprache', 'punct', -3), ('dɔɪ̯tʃ][24', 'Sprache', 'par', -4), (']', 'ist', 'punct', 1), ('ist', 'ist', 'ROOT', 0), ('eine', 'Sprache', 'nk', 2), ('westgermanische', 'Sprache', 'nk', 1), ('Sprache', 'ist', 'pd', -3), (',', 'Sprache', 'punct', -1), ('die', 'dient', 'sb', 19), ('weltweit', 'dient', 'mo', 18), ('etwa', 'Millionen', 'mo', 4), ('90', 'Millionen', 'nmc', 3), ('bis', '90', 'cd', -1), ('105', 'bis', 'cj', -1), ('Millionen', 'weltweit', 'nk', -5), ('Menschen', 'Millionen', 'nk', -1), ('als', 'Millionen', 'mnr', -2), ('Muttersprache', 'als', 'nk', -1), ('und', 'Millionen', 'nmc', 4), ('weiteren', 'Millionen', 'nmc', 3), ('rund', 'Millionen', 'mo', 2), ('80', 'Millionen', 'nmc', 1), ('Millionen', 'Millionen', 'nk', -8), ('als', 'Millionen', 'nk', -9), ('Zweit-', 'oder', 'cj', 1), ('oder', 'Fremdsprache', 'cd', 1), ('Fremdsprache', 'als', 'nk', -3), ('dient', 'Sprache', 'rc', -21), ('.', 'ist', 'punct', -25)]
    )

if __name__ == '__main__':
    test_spacy_deu()
