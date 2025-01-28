# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Norwegian (Nynorsk)
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

def test_stanza_nno():
    test_stanza.wl_test_stanza(
        lang = 'nno',
        results_sentence_tokenize = ['Nynorsk, før 1929 offisielt kalla landsmål, er sidan jamstillingsvedtaket av 12. mai 1885 ei av dei to offisielle målformene av norsk; den andre forma er bokmål.', 'Nynorsk vert i dag nytta av om lag 10–15% av innbyggjarane i Noreg.', '[1][2]', 'Skriftspråket er basert på nynorsk talemål, det vil seie dei moderne norske dialektane til skilnad frå gamalnorsk og mellomnorsk.', 'Når ein seier at nokon snakkar nynorsk, meiner ein helst at dei snakkar nynorsk normaltalemål.', 'Dei færraste dialekttalande nordmenn seier at dei snakkar nynorsk, men det er ikkje uvanleg i kjerneområda til nynorsken.', 'Dette tilhøvet mellom tale og skrift ligg bak målrørsla sitt slagord sidan 1970-talet:', '«Snakk dialekt – skriv nynorsk!»', 'Nynorske dialektar vart snakka over heile landet, men det er berre på Vestlandet utanom dei største byene og i dei austlandske fjellbygdene at skriftspråket står sterkt.', 'Det vil seie at dei fleste dialekttalarane har bokmål som det primære skriftspråket sitt.'],
        results_word_tokenize = ['Nynorsk', ',', 'før', '1929', 'offisielt', 'kalla', 'landsmål', ',', 'er', 'sidan', 'jamstillingsvedtaket', 'av', '12.', 'mai', '1885', 'ei', 'av', 'dei', 'to', 'offisielle', 'målformene', 'av', 'norsk', ';', 'den', 'andre', 'forma', 'er', 'bokmål', '.'],
        results_pos_tag = [('Nynorsk', 'subst'), (',', '<komma>'), ('før', 'prep'), ('1929', 'det'), ('offisielt', 'adj'), ('kalla', 'adj'), ('landsmål', 'subst'), (',', '<komma>'), ('er', 'verb'), ('sidan', 'prep'), ('jamstillingsvedtaket', 'subst'), ('av', 'prep'), ('12.', 'adj'), ('mai', 'subst'), ('1885', 'det'), ('ei', 'det'), ('av', 'prep'), ('dei', 'det'), ('to', 'det'), ('offisielle', 'adj'), ('målformene', 'subst'), ('av', 'prep'), ('norsk', 'subst'), (';', 'clb'), ('den', 'det'), ('andre', 'adj'), ('forma', 'subst'), ('er', 'verb'), ('bokmål', 'subst'), ('.', 'clb')],
        results_pos_tag_universal = [('Nynorsk', 'NOUN'), (',', 'PUNCT'), ('før', 'ADP'), ('1929', 'NUM'), ('offisielt', 'ADJ'), ('kalla', 'ADJ'), ('landsmål', 'NOUN'), (',', 'PUNCT'), ('er', 'AUX'), ('sidan', 'ADP'), ('jamstillingsvedtaket', 'NOUN'), ('av', 'ADP'), ('12.', 'ADJ'), ('mai', 'NOUN'), ('1885', 'NUM'), ('ei', 'DET'), ('av', 'ADP'), ('dei', 'DET'), ('to', 'NUM'), ('offisielle', 'ADJ'), ('målformene', 'NOUN'), ('av', 'ADP'), ('norsk', 'NOUN'), (';', 'PUNCT'), ('den', 'DET'), ('andre', 'ADJ'), ('forma', 'NOUN'), ('er', 'AUX'), ('bokmål', 'NOUN'), ('.', 'PUNCT')],
        results_lemmatize = ['Nynorsk', '$,', 'før', '1929', 'offisiell', 'kalle', 'landsmål', '$,', 'vere', 'sidan', 'jamstillingsvedtak', 'av', '12.', 'mai', '1885', 'ein', 'av', 'dei', 'to', 'offisiell', 'målform', 'av', 'norsk', '$;', 'den', 'andre', 'form', 'vere', 'bokmål', '$.'],
        results_dependency_parse = [('Nynorsk', 'ei', 'nsubj', 15), (',', '1929', 'punct', 2), ('før', '1929', 'case', 1), ('1929', 'kalla', 'obl', 2), ('offisielt', 'kalla', 'advmod', 1), ('kalla', 'Nynorsk', 'amod', -5), ('landsmål', 'kalla', 'obj', -1), (',', 'kalla', 'punct', -2), ('er', 'ei', 'cop', 7), ('sidan', 'jamstillingsvedtaket', 'case', 1), ('jamstillingsvedtaket', 'ei', 'obl', 5), ('av', 'mai', 'case', 2), ('12.', 'mai', 'amod', 1), ('mai', 'jamstillingsvedtaket', 'nmod', -3), ('1885', 'mai', 'nmod', -1), ('ei', 'ei', 'root', 0), ('av', 'målformene', 'case', 4), ('dei', 'målformene', 'det', 3), ('to', 'målformene', 'nummod', 2), ('offisielle', 'målformene', 'amod', 1), ('målformene', 'ei', 'nmod', -5), ('av', 'norsk', 'case', 1), ('norsk', 'målformene', 'nmod', -2), (';', 'bokmål', 'punct', 5), ('den', 'forma', 'det', 2), ('andre', 'forma', 'amod', 1), ('forma', 'bokmål', 'nsubj', 2), ('er', 'bokmål', 'cop', 1), ('bokmål', 'ei', 'conj', -13), ('.', 'ei', 'punct', -14)]
    )

if __name__ == '__main__':
    test_stanza_nno()
