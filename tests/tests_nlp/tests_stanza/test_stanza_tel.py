# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Telugu
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

def test_stanza_tel():
    results_pos_tag = [('తెలుగు', 'PROPN'), ('అనేది', 'PRON'), ('ద్రావిడ', 'PROPN'), ('భాషల', 'NOUN'), ('కుటుంబానికి', 'NOUN'), ('చెందిన', 'VERB'), ('భాష', 'NOUN'), ('.', 'PUNCT')]

    test_stanza.wl_test_stanza(
        lang = 'tel',
        results_sentence_tokenize = ['తెలుగు అనేది ద్రావిడ భాషల కుటుంబానికి చెందిన భాష.', 'దీనిని మాట్లాడే ప్రజలు ప్రధానంగా ఆంధ్ర, తెలంగాణాలో ఉన్నారు.', 'ఇది ఆ రాష్ట్రాలలో అధికార భాష.', 'భారతదేశంలో ఒకటి', 'కంటే ఎక్కువ రాష్ట్రాల్లో ప్రాథమిక అధికారిక భాషా హోదా కలిగిన కొద్ది భాషలలో హిందీ, బెంగాలీలతో పాటు ఇది కూడా ఉంది.', '[5][6] పుదుచ్చేరిలోని యానం జిల్లాలో తెలుగు అధికారిక భాష.', 'ఒడిశా, కర్ణాటక, తమిళనాడు, కేరళ, పంజాబ్, ఛత్తీస్\u200cగఢ్, మహారాష్ట్ర, అండమాన్ నికోబార్ దీవులలో గుర్తింపబడిన అల్పసంఖ్యాక భాష.', 'దేశ ప్రభుత్వం భారతదేశ ప్రాచీన భాషగా గుర్తించిన ఆరు భాషలలో ఇది ఒకటి.', '[7][8]'],
        results_word_tokenize = ['తెలుగు', 'అనేది', 'ద్రావిడ', 'భాషల', 'కుటుంబానికి', 'చెందిన', 'భాష', '.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_dependency_parse = [('తెలుగు', 'అనేది', 'compound', 1), ('అనేది', 'చెందిన', 'nsubj', 4), ('ద్రావిడ', 'అనేది', 'nmod', -1), ('భాషల', 'చెందిన', 'obl', 2), ('కుటుంబానికి', 'చెందిన', 'obl', 1), ('చెందిన', 'భాష', 'acl', 1), ('భాష', 'భాష', 'root', 0), ('.', 'భాష', 'punct', -1)]
    )

if __name__ == '__main__':
    test_stanza_tel()
