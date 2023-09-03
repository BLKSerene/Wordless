# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Stanza - Norwegian Nynorsk
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

def test_stanza_nno():
    results_pos_tag = [('Nynorsk', 'NOUN'), (',', 'PUNCT'), ('før', 'ADP'), ('1929', 'NUM'), ('offisielt', 'ADJ'), ('kalla', 'ADJ'), ('landsmål', 'NOUN'), (',', 'PUNCT'), ('er', 'AUX'), ('sidan', 'ADP'), ('jamstillingsvedtaket', 'NOUN'), ('av', 'ADP'), ('12.', 'ADJ'), ('mai', 'NOUN'), ('1885', 'NUM'), ('ei', 'DET'), ('av', 'ADP'), ('dei', 'DET'), ('to', 'NUM'), ('offisielle', 'ADJ'), ('målformene', 'NOUN'), ('av', 'ADP'), ('norsk', 'NOUN'), (';', 'PUNCT'), ('den', 'DET'), ('andre', 'ADJ'), ('forma', 'NOUN'), ('er', 'AUX'), ('bokmål', 'NOUN'), ('.', 'PUNCT')]

    test_stanza.wl_test_stanza(
        lang = 'nno',
        results_sentence_tokenize = ['Nynorsk, før 1929 offisielt kalla landsmål, er sidan jamstillingsvedtaket av 12. mai 1885 ei av dei to offisielle målformene av norsk; den andre forma er bokmål.', 'Nynorsk vert i dag nytta av om lag 10–15% av innbyggjarane i Noreg.[1][2]', 'Skriftspråket er basert på nynorsk talemål, det vil seie dei moderne norske dialektane til skilnad frå gamalnorsk og mellomnorsk.', 'Når ein seier at nokon snakkar nynorsk, meiner ein helst at dei snakkar nynorsk normaltalemål.', 'Dei færraste dialekttalande nordmenn seier at dei snakkar nynorsk, men det er ikkje uvanleg i kjerneområda til nynorsken.', 'Dette tilhøvet mellom tale og skrift ligg bak målrørsla sitt slagord sidan 1970-talet:', '«Snakk dialekt – skriv nynorsk!»', 'Nynorske dialektar vart snakka over heile landet, men det er berre på Vestlandet utanom dei største byene og i dei austlandske fjellbygdene at skriftspråket står sterkt.', 'Det vil seie at dei fleste dialekttalarane har bokmål som det primære skriftspråket sitt.'],
        results_word_tokenize = ['Nynorsk', ',', 'før', '1929', 'offisielt', 'kalla', 'landsmål', ',', 'er', 'sidan', 'jamstillingsvedtaket', 'av', '12.', 'mai', '1885', 'ei', 'av', 'dei', 'to', 'offisielle', 'målformene', 'av', 'norsk', ';', 'den', 'andre', 'forma', 'er', 'bokmål', '.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['Nynorsk', '$,', 'før', '1929', 'offisiell', 'kalle', 'landsmål', '$,', 'vere', 'sidan', 'jamstillingsvedtak', 'av', '12.', 'mai', '1885', 'ein', 'av', 'dei', 'to', 'offisiell', 'målform', 'av', 'norsk', '$;', 'den', 'andre', 'form', 'vere', 'bokmål', '$.'],
        results_dependency_parse = [('Nynorsk', 'jamstillingsvedtaket', 'nsubj', 10), (',', '1929', 'punct', 2), ('før', '1929', 'case', 1), ('1929', 'Nynorsk', 'nmod', -3), ('offisielt', 'kalla', 'advmod', 1), ('kalla', '1929', 'amod', -2), ('landsmål', 'kalla', 'obj', -1), (',', 'kalla', 'punct', -2), ('er', 'jamstillingsvedtaket', 'cop', 2), ('sidan', 'jamstillingsvedtaket', 'case', 1), ('jamstillingsvedtaket', 'jamstillingsvedtaket', 'root', 0), ('av', 'mai', 'case', 2), ('12.', 'mai', 'amod', 1), ('mai', 'jamstillingsvedtaket', 'nmod', -3), ('1885', 'mai', 'nmod', -1), ('ei', 'jamstillingsvedtaket', 'nmod', -5), ('av', 'målformene', 'case', 4), ('dei', 'målformene', 'det', 3), ('to', 'målformene', 'nummod', 2), ('offisielle', 'målformene', 'amod', 1), ('målformene', 'ei', 'nmod', -5), ('av', 'norsk', 'case', 1), ('norsk', 'målformene', 'nmod', -2), (';', 'bokmål', 'punct', 5), ('den', 'forma', 'det', 2), ('andre', 'forma', 'amod', 1), ('forma', 'bokmål', 'nsubj', 2), ('er', 'bokmål', 'cop', 1), ('bokmål', 'jamstillingsvedtaket', 'conj', -18), ('.', 'jamstillingsvedtaket', 'punct', -19)]
    )

if __name__ == '__main__':
    test_stanza_nno()
