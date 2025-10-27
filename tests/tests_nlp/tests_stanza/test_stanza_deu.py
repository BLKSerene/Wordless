# ----------------------------------------------------------------------
# Tests: NLP - Stanza - German
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

def test_stanza_deu():
    test_stanza.wl_test_stanza(
        lang = 'deu_de',
        results_sentence_tokenize = ['Die deutsche Sprache oder Deutsch [dɔɪ̯tʃ][24] ist eine westgermanische Sprache, die weltweit etwa 90 bis 105 Millionen Menschen als Muttersprache und weiteren rund 80 Millionen als Zweit- oder Fremdsprache dient.', 'Das Deutsche ist eine plurizentrische Sprache, enthält also mehrere Standardvarietäten in verschiedenen Regionen.'],
        results_word_tokenize = ['Die', 'deutsche', 'Sprache', 'oder', 'Deutsch', '[', 'dɔɪ̯tʃ][24', ']', 'ist', 'eine', 'westgermanische', 'Sprache', ',', 'die', 'weltweit', 'etwa', '90', 'bis', '105', 'Millionen', 'Menschen', 'als', 'Muttersprache', 'und', 'weiteren', 'rund', '80', 'Millionen', 'als', 'Zweit', '-', 'oder', 'Fremdsprache', 'dient', '.'],
        results_pos_tag = [('Die', 'ART'), ('deutsche', 'ADJA'), ('Sprache', 'NN'), ('oder', 'KON'), ('Deutsch', 'NN'), ('[', '$('), ('dɔɪ̯tʃ][24', 'NE'), (']', '$('), ('ist', 'VAFIN'), ('eine', 'ART'), ('westgermanische', 'ADJA'), ('Sprache', 'NN'), (',', '$,'), ('die', 'PRELS'), ('weltweit', 'ADJD'), ('etwa', 'ADV'), ('90', 'CARD'), ('bis', 'KON'), ('105', 'CARD'), ('Millionen', 'NN'), ('Menschen', 'NN'), ('als', 'KOKOM'), ('Muttersprache', 'NN'), ('und', 'KON'), ('weiteren', 'ADJA'), ('rund', 'ADV'), ('80', 'CARD'), ('Millionen', 'NN'), ('als', 'KOKOM'), ('Zweit', 'TRUNC'), ('-', '$('), ('oder', 'KON'), ('Fremdsprache', 'NN'), ('dient', 'VVFIN'), ('.', '$.')],
        results_pos_tag_universal = [('Die', 'DET'), ('deutsche', 'ADJ'), ('Sprache', 'NOUN'), ('oder', 'CCONJ'), ('Deutsch', 'NOUN'), ('[', 'PUNCT'), ('dɔɪ̯tʃ][24', 'PROPN'), (']', 'PUNCT'), ('ist', 'AUX'), ('eine', 'DET'), ('westgermanische', 'ADJ'), ('Sprache', 'NOUN'), (',', 'PUNCT'), ('die', 'PRON'), ('weltweit', 'ADJ'), ('etwa', 'ADV'), ('90', 'NUM'), ('bis', 'ADP'), ('105', 'NUM'), ('Millionen', 'NOUN'), ('Menschen', 'NOUN'), ('als', 'ADP'), ('Muttersprache', 'NOUN'), ('und', 'CCONJ'), ('weiteren', 'ADJ'), ('rund', 'ADV'), ('80', 'NUM'), ('Millionen', 'NOUN'), ('als', 'ADP'), ('Zweit', 'NOUN'), ('-', 'PUNCT'), ('oder', 'CCONJ'), ('Fremdsprache', 'NOUN'), ('dient', 'VERB'), ('.', 'PUNCT')],
        results_lemmatize = ['der', 'deutsch', 'Sprache', 'oder', 'deutsch', '[', 'denfellelhuldellulfelliehueruu', ']', 'sein', 'ein', 'westgermanisch', 'Sprache', ',', 'der', 'weltweit', 'etwa', '90', 'bis', '105', 'Million', 'Mensch', 'als', 'Muttersprache', 'und', 'weit', 'rund', '80', 'Million', 'als', 'Zweit', '-', 'oder', 'Fremdsprache', 'dienen', '.'],
        results_dependency_parse = [('Die', 'Sprache', 'det', 2), ('deutsche', 'Sprache', 'amod', 1), ('Sprache', 'Sprache', 'nsubj', 9), ('oder', 'Deutsch', 'cc', 1), ('Deutsch', 'Sprache', 'conj', -2), ('[', 'dɔɪ̯tʃ][24', 'punct', 1), ('dɔɪ̯tʃ][24', 'Sprache', 'appos', -4), (']', 'dɔɪ̯tʃ][24', 'punct', -1), ('ist', 'Sprache', 'cop', 3), ('eine', 'Sprache', 'det', 2), ('westgermanische', 'Sprache', 'amod', 1), ('Sprache', 'Sprache', 'root', 0), (',', 'dient', 'punct', 21), ('die', 'dient', 'nsubj', 20), ('weltweit', 'dient', 'advmod', 19), ('etwa', '90', 'advmod', 1), ('90', 'Millionen', 'nummod', 3), ('bis', '105', 'case', 1), ('105', 'Millionen', 'nmod', 1), ('Millionen', 'Menschen', 'nmod', 1), ('Menschen', 'dient', 'obj', 13), ('als', 'Muttersprache', 'case', 1), ('Muttersprache', 'dient', 'obl', 11), ('und', 'Millionen', 'cc', 4), ('weiteren', 'Millionen', 'amod', 3), ('rund', '80', 'advmod', 1), ('80', 'Millionen', 'nummod', 1), ('Millionen', 'Zweit', 'nmod', 2), ('als', 'Zweit', 'case', 1), ('Zweit', 'dient', 'obl', 4), ('-', 'Fremdsprache', 'punct', 2), ('oder', 'Fremdsprache', 'cc', 1), ('Fremdsprache', 'Zweit', 'conj', -3), ('dient', 'Sprache', 'acl', -22), ('.', 'Sprache', 'punct', -23)],
        results_sentiment_analayze = [0]
    )

if __name__ == '__main__':
    test_stanza_deu()
