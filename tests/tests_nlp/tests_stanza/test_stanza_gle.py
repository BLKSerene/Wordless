# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Irish
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

def test_stanza_gle():
    test_stanza.wl_test_stanza(
        lang = 'gle',
        results_sentence_tokenize = ['Is ceann de na teangacha Ceilteacha í an Ghaeilge (nó Gaeilge na hÉireann mar a thugtar uirthi corruair), agus ceann de na trí cinn de theangacha Ceilteacha ar a dtugtar na teangacha Gaelacha (Gaeilge, Gaeilge Mhanann agus Gaeilge na hAlban) go háirithe.', 'Labhraítear in Éirinn go príomha í, ach tá cainteoirí Gaeilge ina gcónaí in áiteanna eile ar fud an domhain.'],
        results_word_tokenize = ['Is', 'ceann', 'de', 'na', 'teangacha', 'Ceilteacha', 'í', 'an', 'Ghaeilge', '(', 'nó', 'Gaeilge', 'na', 'hÉireann', 'mar', 'a', 'thugtar', 'uirthi', 'corruair', ')', ',', 'agus', 'ceann', 'de', 'na', 'trí', 'cinn', 'de', 'theangacha', 'Ceilteacha', 'ar', 'a', 'dtugtar', 'na', 'teangacha', 'Gaelacha', '(', 'Gaeilge', ',', 'Gaeilge', 'Mhanann', 'agus', 'Gaeilge', 'na', 'hAlban', ')', 'go', 'háirithe', '.'],
        results_pos_tag = [('Is', 'Cop'), ('ceann', 'Noun'), ('de', 'Simp'), ('na', 'Art'), ('teangacha', 'Noun'), ('Ceilteacha', 'Adj'), ('í', 'Pers'), ('an', 'Art'), ('Ghaeilge', 'Noun'), ('(', 'Punct'), ('nó', 'Coord'), ('Gaeilge', 'Noun'), ('na', 'Art'), ('hÉireann', 'Noun'), ('mar', 'Subord'), ('a', 'Vb'), ('thugtar', 'VTI'), ('uirthi', 'Prep'), ('corruair', 'Noun'), (')', 'Punct'), (',', 'Punct'), ('agus', 'Coord'), ('ceann', 'Noun'), ('de', 'Simp'), ('na', 'Art'), ('trí', 'Num'), ('cinn', 'Noun'), ('de', 'Simp'), ('theangacha', 'Noun'), ('Ceilteacha', 'Adj'), ('ar', 'Simp'), ('a', 'Vb'), ('dtugtar', 'VTI'), ('na', 'Art'), ('teangacha', 'Noun'), ('Gaelacha', 'Adj'), ('(', 'Punct'), ('Gaeilge', 'Noun'), (',', 'Punct'), ('Gaeilge', 'Noun'), ('Mhanann', 'Noun'), ('agus', 'Coord'), ('Gaeilge', 'Noun'), ('na', 'Art'), ('hAlban', 'Noun'), (')', 'Punct'), ('go', 'Ad'), ('háirithe', 'Adj'), ('.', '.')],
        results_pos_tag_universal = [('Is', 'AUX'), ('ceann', 'NOUN'), ('de', 'ADP'), ('na', 'DET'), ('teangacha', 'NOUN'), ('Ceilteacha', 'ADJ'), ('í', 'PRON'), ('an', 'DET'), ('Ghaeilge', 'PROPN'), ('(', 'PUNCT'), ('nó', 'CCONJ'), ('Gaeilge', 'PROPN'), ('na', 'DET'), ('hÉireann', 'PROPN'), ('mar', 'SCONJ'), ('a', 'PART'), ('thugtar', 'VERB'), ('uirthi', 'ADP'), ('corruair', 'NOUN'), (')', 'PUNCT'), (',', 'PUNCT'), ('agus', 'CCONJ'), ('ceann', 'NOUN'), ('de', 'ADP'), ('na', 'DET'), ('trí', 'NUM'), ('cinn', 'NOUN'), ('de', 'ADP'), ('theangacha', 'NOUN'), ('Ceilteacha', 'ADJ'), ('ar', 'ADP'), ('a', 'PART'), ('dtugtar', 'VERB'), ('na', 'DET'), ('teangacha', 'NOUN'), ('Gaelacha', 'ADJ'), ('(', 'PUNCT'), ('Gaeilge', 'PROPN'), (',', 'PUNCT'), ('Gaeilge', 'PROPN'), ('Mhanann', 'PROPN'), ('agus', 'CCONJ'), ('Gaeilge', 'PROPN'), ('na', 'DET'), ('hAlban', 'PROPN'), (')', 'PUNCT'), ('go', 'PART'), ('háirithe', 'ADJ'), ('.', 'PUNCT')],
        results_lemmatize = ['is', 'ceann', 'de', 'an', 'teanga', 'Ceilteach', 'í', 'an', 'Gaeilge', '(', 'nó', 'Gaeilge', 'an', 'Éire', 'mar', 'a', 'tabhair', 'ar', 'corruair', ')', ',', 'agus', 'ceann', 'de', 'an', 'trí', 'ceann', 'de', 'teanga', 'Ceilteach', 'ar', 'a', 'tabhair', 'an', 'teanga', 'gaelach', '(', 'Gaeilge', ',', 'Gaeilge', 'Manann', 'agus', 'Gaeilge', 'an', 'Albain', ')', 'go', 'áirithe', '.'],
        results_dependency_parse = [('Is', 'ceann', 'cop', 1), ('ceann', 'ceann', 'root', 0), ('de', 'teangacha', 'case', 2), ('na', 'teangacha', 'det', 1), ('teangacha', 'ceann', 'nmod', -3), ('Ceilteacha', 'teangacha', 'amod', -1), ('í', 'ceann', 'nmod', -5), ('an', 'Ghaeilge', 'det', 1), ('Ghaeilge', 'ceann', 'nsubj', -7), ('(', 'Gaeilge', 'punct', 2), ('nó', 'Gaeilge', 'cc', 1), ('Gaeilge', 'Ghaeilge', 'conj', -3), ('na', 'hÉireann', 'det', 1), ('hÉireann', 'Gaeilge', 'nmod', -2), ('mar', 'thugtar', 'mark', 2), ('a', 'thugtar', 'mark:prt', 1), ('thugtar', 'ceann', 'advcl', -15), ('uirthi', 'thugtar', 'obl:prep', -1), ('corruair', 'thugtar', 'obj', -2), (')', 'corruair', 'punct', -1), (',', 'ceann', 'punct', 2), ('agus', 'ceann', 'cc', 1), ('ceann', 'ceann', 'conj', -21), ('de', 'cinn', 'case', 3), ('na', 'cinn', 'det', 2), ('trí', 'cinn', 'nummod', 1), ('cinn', 'ceann', 'nmod', -4), ('de', 'theangacha', 'case', 1), ('theangacha', 'cinn', 'nmod', -2), ('Ceilteacha', 'theangacha', 'amod', -1), ('ar', 'dtugtar', 'case', 2), ('a', 'dtugtar', 'obl', 1), ('dtugtar', 'cinn', 'acl:relcl', -6), ('na', 'teangacha', 'det', 1), ('teangacha', 'dtugtar', 'obj', -2), ('Gaelacha', 'teangacha', 'amod', -1), ('(', 'Gaeilge', 'punct', 1), ('Gaeilge', 'teangacha', 'nmod', -3), (',', 'Gaeilge', 'punct', 1), ('Gaeilge', 'Gaeilge', 'conj', -2), ('Mhanann', 'Gaeilge', 'nmod', -1), ('agus', 'Gaeilge', 'cc', 1), ('Gaeilge', 'Gaeilge', 'conj', -5), ('na', 'hAlban', 'det', 1), ('hAlban', 'Gaeilge', 'nmod', -2), (')', 'Gaeilge', 'punct', -8), ('go', 'háirithe', 'mark:prt', 1), ('háirithe', 'dtugtar', 'advmod', -15), ('.', 'ceann', 'punct', -47)]
    )

if __name__ == '__main__':
    test_stanza_gle()
