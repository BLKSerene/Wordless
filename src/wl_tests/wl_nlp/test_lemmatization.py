# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Lemmatization
# Copyright (C) 2018-2022  Ye Lei (叶磊)
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

import pytest

from wl_nlp import wl_lemmatization, wl_word_tokenization
from wl_tests import wl_test_init, wl_test_lang_examples
from wl_utils import wl_conversion

test_lemmatizers = []

main = wl_test_init.Wl_Test_Main()

for lang, lemmatizers in main.settings_global['lemmatizers'].items():
    for lemmatizer in lemmatizers:
        if lang not in ['other']:
            test_lemmatizers.append((lang, lemmatizer))

@pytest.mark.parametrize('lang, lemmatizer', test_lemmatizers)
def test_lemmatize(lang, lemmatizer):
    lang_text = wl_conversion.to_lang_text(main, lang)

    print(f'{lang_text} ({lang}) / {lemmatizer}:')

    # Untokenized
    lemmas = wl_lemmatization.wl_lemmatize(
        main,
        inputs = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}'),
        lang = lang,
        lemmatizer = lemmatizer
    )

    # Tokenized
    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}'),
        lang = lang
    )
    lemmas_tokenized = wl_lemmatization.wl_lemmatize(
        main,
        inputs = tokens,
        lang = lang,
        lemmatizer = lemmatizer
    )

    print(lemmas)

    # Check for missing lemmas
    assert all(lemmas)
    assert all(lemmas_tokenized)
    
    # Tokenization should not be modified
    assert len(tokens) == len(lemmas_tokenized)

    if lang == 'ast':
        assert lemmas == ["L'asturianu", 'ser', 'unu', 'llingua', 'romance', 'propiu', "d'Asturies,[1", ']', 'perteneciente', 'al', 'subgrupu', 'asturllionés', '.']
    elif lang == 'ben':
        assert lemmas == ['বাংলা', 'ভাষা', '(', 'বাঙলা', ',', 'বাঙ্গলা', ',', 'তথা', 'বাঙ্গালা', 'নামগুলোতেও', 'পরিচিত', ')', 'একটি', 'ইন্দো', '-', 'আর্য', 'ভাষা', ',', 'যা', 'দক্ষিণ', 'এশিয়ার', 'বাঙালি', 'জাতির', 'প্রধান', 'কথ্য', 'ও', 'লেখ্য', 'ভাষা', '।']
    elif lang == 'bul':
        assert lemmas == ['Бъ̀лгарският', 'езѝк', 'съм', 'индоевропейски', 'език', 'от', 'група', 'на', 'южнославянските', 'език', '.']
    elif lang == 'cat':
        if lemmatizer == 'lemmatization_lists_cat':
            assert lemmas == ['El', 'català', '(', 'denominació', 'oficial', 'a', 'Catalunya', ',', 'a', 'ell', 'Illes', 'Balears', ',', 'a', 'Andorra', ',', 'a', 'ell', 'ciutat', 'de', "l'Alguer", 'i', 'tradicional', 'a', 'Catalunya', 'Nord', ')', 'o', 'valencià', '(', 'denominació', 'oficial', 'al', 'País', 'Valencià', 'i', 'tradicional', 'al', 'Carxe', ')', 'ser', 'un', 'llengua', 'romànic', 'parlar', 'a', 'Catalunya', ',', 'ell', 'País', 'Valencià', '(', 'treure', "d'algunes", 'comarca', 'i', 'localitat', 'de', "l'interior", ')', ',', 'ell', 'Illes', 'Balears', ',', 'Andorra', ',', 'ell', 'Franja', 'de', 'Ponent', '(', 'a', "l'Aragó", ')', ',', 'ell', 'ciutat', 'de', "l'Alguer", '(', 'a', "l'illa", 'de', 'Sardenya', ')', ',', 'ell', 'Catalunya', 'del', 'Nord,[8', ']', 'ell', 'Carxe', '(', 'un', 'petit', 'territori', 'de', 'Múrcia', 'poblar', 'per', 'immigrar', 'valencians),[9][10', ']', 'i', 'en', 'comunitat', 'arreu', 'del', 'món', '(', 'entrar', 'ell', 'qual', 'destacar', 'ell', 'de', "l'Argentina", ',', 'amb', '198.000', 'parlants).[11', ']']
        elif lemmatizer == 'spacy_cat':
            assert lemmas == ['el', 'català', '(', 'denominació', 'oficial', 'a', 'Catalunya', ',', 'a', 'el', 'Illes', 'Balears', ',', 'a', 'Andorra', ',', 'a', 'el', 'ciutat', 'de', 'el', 'Alguer', 'i', 'tradicional', 'a', 'Catalunya', 'Nord', ')', 'o', 'valencià', '(', 'denominació', 'oficial', 'a', 'el', 'País', 'Valencià', 'i', 'tradicional', 'a', 'el', 'Carxe', ')', 'ser', 'un', 'llengua', 'romànic', 'parlat', 'a', 'Catalunya', ',', 'el', 'País', 'Valencià', '(', 'tret', 'de', 'algun', 'comarca', 'i', 'localitat', 'de', 'el', 'interior', ')', ',', 'el', 'Illes', 'Balears', ',', 'Andorra', ',', 'el', 'Franja', 'de', 'Ponent', '(', 'a', 'el', 'Aragó', ')', ',', 'el', 'ciutat', 'de', 'el', 'Alguer', '(', 'a', 'el', 'illa', 'de', 'Sardenya', ')', ',', 'el', 'Catalunya', 'de', 'el', 'Nord,[8', ']', 'el', 'Carxe', '(', 'un', 'petit', 'territori', 'de', 'Múrcia', 'poblat', 'per', 'immigrat', 'valencians),[9][10', ']', 'i', 'en', 'comunitat', 'arreu', 'de', 'el', 'món', '(', 'entre', 'el', 'qual', 'destacar', 'el', 'de', 'el', 'Argentina', ',', 'amb', '198.000', 'parlants).[11', ']']
        else:
            raise Exception(f'Error: Tests for lemmatizer "{lemmatizer}" is skipped!')
    elif lang == 'hrv':
        assert lemmas == ['Hrvatski', 'jezik', '(', 'ISO', '639', '-', '3', ':', 'hrv', ')', 'skupni', 'biti', 'naziv', 'za', 'nacionalan', 'standardan', 'jezik', 'Hrvata', ',', 'te', 'za', 'skup', 'narječje', 'i', 'govor', 'koji', 'govoriti', 'ili', 'biti', 'nekada', 'govoriti', 'Hrvati', '.']
    elif lang == 'ces':
        assert lemmas == ['Čeština', 'neboli', 'český', 'jazyk', 'on', 'západoslovanský', 'jazyk', ',', 'blízký', 'slovenštině', ',', 'poté', 'lužické', 'srbštině', 'a', 'polštině', '.']
    elif lang == 'dan':
        assert lemmas == ['Dansk', 'være', 'en', 'nordgermansk', 'sprog', 'af', 'den', 'østnordiske', '(', 'kontinental', ')', 'gruppe', ',', 'der', 'tale', 'af', 'ca.', 'seks', 'million', 'menneske', '.']
    elif lang == 'nld':
        assert lemmas == ['het', 'nederlands', 'is', 'een', 'west-germaans', 'taal', 'en', 'de', 'officieel', 'taal', 'van', 'nederland', ',', 'suriname', 'en', 'e', 'van', 'de', 'drie', 'officieel', 'taal', 'van', 'belgië', '.']
    elif lang in ['eng_gb', 'eng_us']:
        if lemmatizer in ['lemmatization_lists_eng', 'nltk_wordnet']:
            assert lemmas == ['English', 'be', 'a', 'West', 'Germanic', 'language', 'of', 'the', 'Indo', '-', 'European', 'language', 'family', ',', 'originally', 'speak', 'by', 'the', 'inhabitant', 'of', 'early', 'medieval', 'England.[3][4][5', ']']
        elif lemmatizer == 'spacy_eng':
            assert lemmas == ['English', 'be', 'a', 'West', 'Germanic', 'language', 'of', 'the', 'Indo', '-', 'european', 'language', 'family', ',', 'originally', 'speak', 'by', 'the', 'inhabitant', 'of', 'early', 'medieval', 'England.[3][4][5', ']']
        else:
            raise Exception(f'Error: Tests for lemmatizer "{lemmatizer}" is skipped!')
    elif lang == 'est':
        assert lemmas == ['Eesti', 'kee', '(', 'varasem', 'nimetu', 'maakeel', ')', 'olema', 'läänemeresoome', 'lõunarühma', 'kuuluma', 'kee', '.']
    elif lang == 'fra':
        if lemmatizer == 'lemmatization_lists_fra':
            assert lemmas == ['Le', 'français', 'être', 'un', 'langue', 'indo', '-', 'européen', 'de', 'le', 'famille', 'un', 'langue', 'roman', 'do', 'nt', 'le', 'locuteurs', 'être', 'appeler', 'francophone', '.']
        elif lemmatizer == 'spacy_fra':
            assert lemmas == ['le', 'français', 'être', 'un', 'langue', 'indo-européen', 'de', 'le', 'famille', 'de', 'langue', 'roman', 'dont', 'le', 'locuteur', 'être', 'appeler', 'francophone', '.']
        else:
            raise Exception(f'Error: Tests for lemmatizer "{lemmatizer}" is skipped!')
    elif lang == 'glg':
        assert lemmas == ['O', 'galego', '(', '[', 'ɡaˈleɣo̝', ']', ')', 'ser', 'un', 'lingua', 'indoeuropeo', 'que', 'pertencer', 'á', 'póla', 'de', 'lingua', 'románico', '.']
    elif lang in ['deu_at', 'deu_de', 'deu_ch']:
        if lemmatizer == 'lemmatization_lists_deu':
            assert lemmas == ['Die', 'deutsch', 'Sprache', 'bzw', '.', 'der', 'deutschen', '(', '[', 'dɔɪ̯tʃ];[26', ']', 'abkürzen', 'dt', '.', 'oder', 'dtsch', '.', ')', 'sein', 'einen', 'westgermanische', 'Sprache', ',', 'der', 'weltweit', 'etwa', '90', 'bis', '105', 'Million', 'Mensch', 'als', 'Muttersprache', 'und', 'weit', 'rund', '80', 'Million', 'als', 'Zweit-', 'oder', 'Fremdsprache', 'dienen', '.']
        elif lemmatizer == 'spacy_deu':
            assert lemmas == ['der', 'deutsch', 'Sprache', 'bzw.', 'der', 'deutschen', '(', '[', 'dɔɪ̯tʃ];[26', ']', 'abkürzen', 'dt', '.', 'oder', 'dtsch', '.', ')', 'sein', 'einen', 'westgermanische', 'Sprache', ',', 'der', 'weltweit', 'etwa', '90', 'bis', '105', 'Million', 'Mensch', 'als', 'Muttersprache', 'und', 'weit', 'rund', '80', 'Million', 'als', 'Zweit-', 'oder', 'Fremdsprache', 'dienen', '.']
        else:
            raise Exception(f'Error: Tests for lemmatizer "{lemmatizer}" is skipped!')
    elif lang == 'grc':
        assert lemmas == ['Ὅτι', 'μέν', 'σύ', ',', 'ὦ', 'ἀνήρ', 'Ἀθηναῖοι', ',', 'πάσχω', 'ὑπό', 'ὁ', 'ἐμός', 'κατηγόρων', ',', 'οὐ', 'οἶδα', '·', 'ἐγώ', 'δέ', 'οὖν', 'καί', 'αὐτός', 'ὑπό', 'αὐτός', 'ὀλίγος', 'ἐμαυτοῦ', 'ἐπελαθόμην', ',', 'οὕτως', 'πιθανῶς', 'λέγω', '.']
    elif lang == 'ell':
        assert lemmas == ['η', 'ελληνικός', 'γλώσσα', 'ανήκω', 'στην', 'ινδοευρωπαϊκός', 'οικογένεια[10', ']', 'και', 'αποτελώ', 'το', 'μοναδικό', 'μέλος', 'το', 'ελληνικός', 'κλάδος', ',', 'ενώ', 'είναι', 'η', 'επίσημη', 'γλώσσα', 'της', 'ελλάδος', 'και', 'της', 'κύπρος', '.']
    elif lang == 'hun':
        assert lemmas == ['A', 'magyar', 'nyelv', 'az', 'uráli', 'nyelvcsalád', 'tag', ',', 'a', 'finnugor', 'nyelv', 'köz', 'tartozó', 'ugor', 'nyelv', 'egyik', '.']
    elif lang == 'ind':
        assert lemmas == ['Bahasa', 'Indonesia', 'adalah', 'bahasa', 'Melayu', 'baku', 'yang', 'dijadikan', 'bagai', 'bahasa', 'resmi', 'Republik', 'Indonesia[1', ']', 'dan', 'bahasa', 'satu', 'bangsa', 'Indonesia.[2', ']']
    elif lang == 'gle':
        if lemmatizer == 'lemmatization_lists_gle':
            assert lemmas == ['Is', 'ceann', 'de', 'na', 'teangach', 'Ceilteacha', 'í', 'an', 'Ghaeilge', '(', 'nó', 'Gaeilge', 'na', 'hÉireann', 'mar', 'a', 'tabhair', 'ar', 'corruair', ')', ',', 'agus', 'ceann', 'den', 'trí', 'ceann', 'de', 'teangach', 'Ceilteacha', 'air', 'a', 'tabhair', 'na', 'teangach', 'Gaelacha', '(', '.i', '.', 'an', 'Ghaeilge', ',', 'Gaeilge', 'na', 'hAlban', 'agus', 'Gaeilge', 'Mhanann', ')', 'go', 'áirithe', '.']
        elif lemmatizer == 'spacy_gle':
            assert lemmas == ['is', 'ceann', 'de', 'na', 'teangacha', 'ceilteacha', 'í', 'an', 'ghaeilge', '(', 'nó', 'gaeilge', 'na', 'héireann', 'mar', 'a', 'thugtar', 'uirthi', 'corruair', ')', ',', 'agus', 'ceann', 'den', 'dtrí', 'cinn', 'de', 'theangacha', 'ceilteacha', 'ar', 'a', 'dtugtar', 'na', 'teangacha', 'gaelacha', '(', '.i.', 'an', 'ghaeilge', ',', 'gaeilge', 'na', 'halban', 'agus', 'gaeilge', 'mhanann', ')', 'go', 'háirithe', '.']
        else:
            raise Exception(f'Error: Tests for lemmatizer "{lemmatizer}" is skipped!')
    elif lang == 'ita':
        if lemmatizer == 'lemmatization_lists_ita':
            assert lemmas == ["L'italiano", '(', '[', 'itaˈljaːno][Nota', '1', ']', 'ascolta[?·info', ']', ')', 'essere', 'una', 'lingua', 'romanzo', 'parlato', 'principalmente', 'in', 'Italia', '.']
        elif lemmatizer == 'spacy_ita':
            assert lemmas == ['il', 'italiano', '(', '[', 'itaˈljaːno][nota', '1', ']', 'ascolta[?·info', ']', ')', 'essere', 'uno', 'lingua', 'romanza', 'parlare', 'principalmente', 'in', 'Italia', '.']
        else:
            raise Exception(f'Error: Tests for lemmatizer "{lemmatizer}" is skipped!')
    elif lang == 'jpn':
        if lemmatizer == 'spacy_jpn':
            assert lemmas == ['日本', '語', '（', 'にほん', 'ご', '、', 'にっぽん', 'ご', '［', '注', '2', '］', '、', '英', '：', 'Japanese', ')', 'は', '、', '日本', '国', '内', 'や', '、', 'かつて', 'の', '日本', '領', 'だ', 'た', '国', '、', 'そして', '日本', '人', '同士', 'の', '間', 'で', '使用', 'する', 'れる', 'て', 'いる', '言語', '。']
        elif lemmatizer == 'sudachipy_jpn':
            assert lemmas == ['日本語', '（', 'にほん', 'ご', '、', 'にっぽん', 'ご', '［', '注', '2', '］', '、', '英', '：', 'Japanese', ')', 'は', '、', '日本', '国', '内', 'や', '、', 'かつて', 'の', '日本', '領', 'だ', 'た', '国', '、', 'そして', '日本人', '同士', 'の', '間', 'で', '使用', 'する', 'れる', 'て', 'いる', '言語', '。']
        else:
            raise Exception(f'Error: Tests for lemmatizer "{lemmatizer}" is skipped!')
    elif lang == 'lit':
        assert lemmas == ['lietuvė', 'kalbėti', '–', 'ižti', 'baltas', 'prokalbės', 'kilęs', 'lietuvė', 'tauta', 'kalbėti', ',', 'kuri', 'Lietuvoje', 'irti', 'valstybinis', ',', 'o', 'Europos', 'sąjunga', '–', 'viena', 'ižti', 'oficialus', 'kalbus', '.']
    elif lang == 'ltz':
        assert lemmas == ["D'", 'Lëtzebuergesch', 'ginn', 'an', 'der', 'däitsch', 'Dialektologie', 'als', 'een', 'westgermanesch', ',', 'mëtteldäitsch', 'Dialekt', 'aklasséieren', ',', 'deen', 'zum', 'Muselfränkesche', 'gehéieren', '.']
    elif lang == 'mkd':
        assert lemmas == ['Македонски', 'јаз', '—', 'јужнословенски', 'јаз', ',', 'дел', 'од', 'група', 'на', 'словенски', 'јазик', 'од', 'јазичен', 'семејство', 'на', 'индоевропски', 'јазик', '.']
    elif lang == 'glv':
        assert lemmas == ['She', 'Gaelg', '(', 'graït', ':', '/gɪlg/', ')', 'çhengey', 'Gaelagh', 'Mannin', '.']
    elif lang == 'nob':
        assert lemmas == ['bokmål', 'er', 'en', 'varietet', 'av', 'norsk', 'språk', '.']
    elif lang == 'fas':
        if lemmatizer == 'lemmatization_lists_fas':
            assert lemmas == ['فارسی', 'یا', 'پارسی', 'یکی', 'از', 'زبان\u200cهای', 'هندواروپایی', 'در', 'شاخهٔ', 'زبان\u200cهای', 'ایرانی', 'جنوب', 'غربی', 'است', 'که', 'در', 'کشورهای', 'ایران', '،', 'افغانستان،[۳', ']', 'تاجیکستان[۴', ']', 'را', 'ازبکستان[۵', ']', 'به', 'آن', 'سخن', 'می\u200cگویند', '.']
        elif lemmatizer == 'spacy_fas':
            assert lemmas == ['فارسی', 'یا', 'پارسی', 'یکی', 'از', 'زبان\u200cهای', 'هندواروپایی', 'در', 'شاخهٔ', 'زبان\u200cهای', 'ایرانی', 'جنوب', 'غربی', 'است', 'که', 'در', 'کشورهای', 'ایران', '،', 'افغانستان،[۳', ']', 'تاجیکستان[۴', ']', 'و', 'ازبکستان[۵', ']', 'به', 'آن', 'سخن', 'می\u200cگویند', '.']
        else:
            raise Exception(f'Error: Tests for lemmatizer "{lemmatizer}" is skipped!')
    elif lang == 'pol':
        assert lemmas == ['język', 'polski', ',', 'polszczyzna', '–', 'język', 'lechicki', 'z', 'grupa', 'zachodniosłowiańskiej', '(', 'do', 'której', 'należeć', 'również', 'czeski', ',', 'kaszubski', ',', 'słowacki', 'i', 'język', 'łużycki', ')', ',', 'stanowiącej', 'część', 'rodzina', 'indoeuropejski', '.']
    elif lang in ['por_br', 'por_pt']:
        if lemmatizer == 'lemmatization_lists_por':
            assert lemmas == ['A', 'língua', 'portuguesar', ',', 'também', 'designar', 'português', ',', 'ser', 'umar', 'língua', 'românico', 'flexivo', 'ocidental', 'originar', 'o', 'galego', '-', 'português', 'falar', 'o', 'Reino', 'da', 'Galiza', 'e', 'o', 'norte', 'de', 'Portugal', '.']
        elif lemmatizer == 'spacy_por':
            assert lemmas == ['A', 'língua', 'portuguesar', ',', 'também', 'designar', 'português', ',', 'ser', 'umar', 'língua', 'românico', 'flexivo', 'ocidental', 'originar', 'o', 'galego-português', 'falar', 'o', 'Reino', 'da', 'Galiza', 'e', 'o', 'norte', 'de', 'Portugal', '.']
        else:
            raise Exception(f'Error: Tests for lemmatizer "{lemmatizer}" is skipped!')
    elif lang == 'ron':
        if lemmatizer == 'lemmatization_lists_ron':
            assert lemmas == ['Limba', 'român', 'fi', 'vrea', 'limbă', 'indo', '-', 'european', ',', 'din', 'grup', 'italic', 'și', 'din', 'subgrupul', 'oriental', 'al', 'limbă', 'romanice', '.']
        elif lemmatizer == 'spacy_ron':
            assert lemmas == ['Limba', 'român', 'fi', 'vrea', 'limbă', 'indo-european', ',', 'din', 'grup', 'italic', 'și', 'din', 'subgrupul', 'oriental', 'al', 'limbă', 'romanice', '.']
        else:
            raise Exception(f'Error: Tests for lemmatizer "{lemmatizer}" is skipped!')
    elif lang == 'rus':
        if lemmatizer == 'lemmatization_lists_rus':
            assert lemmas == ['Ру́сский', 'язы́к', '(', '[', 'ˈruskʲɪi̯', 'jɪˈzɨk', ']', 'Информация', 'о', 'файл', 'слушать)[~', '3', ']', '[', '⇨', ']', 'стальной', 'один', 'из', 'восточнославянский', 'языковый', ',', 'национальный', 'язык', 'русский', 'народ', '.']
        elif lemmatizer == 'pymorphy2_morphological_analyzer':
            assert lemmas == ['ру́сский', 'язы́к', '(', '[', 'ˈruskʲɪi̯', 'jɪˈzɨk', ']', 'информация', 'о', 'файл', 'слушать', ')', '[', '~', '3', ']', '[', '⇨', ']', '—', 'один', 'из', 'восточнославянский', 'язык', ',', 'национальный', 'язык', 'русский', 'народ', '.']
        elif lemmatizer == 'spacy_rus':
            assert lemmas == ['ру́сский', 'язы́к', '(', '[', 'ˈruskʲɪi̯', 'jɪˈzɨk', ']', 'информация', 'о', 'файл', 'слушать)[~', '3', ']', '[', '⇨', ']', '—', 'один', 'из', 'восточнославянский', 'язык', ',', 'национальный', 'язык', 'русский', 'народ', '.']
        else:
            raise Exception(f'Error: Tests for lemmatizer "{lemmatizer}" is skipped!')
    elif lang == 'gla':
        assert lemmas == ["'S", 'i', 'cànan', 'dùthchasach', 'na', 'h', '-', 'Alba', 'a', 'th', "'", 'anns', 'a', "'", 'Ghàidhlig', '.']
    elif lang == 'srp_cyrl':
        assert lemmas == ['Српски', 'језик', 'припадати', 'словенски', 'група', 'језик', 'породица', 'индоевропских', 'језика.[12', ']']
    elif lang == 'slk':
        assert lemmas == ['Slovenčina', 'patriť', 'do', 'skupina', 'západoslovanský', 'jazyk', '(', 'spolu', 's', 'čeština', ',', 'poľština', ',', 'horný', 'as', 'dolný', 'lužickou', 'srbčina', 'as', 'kašubčinou', ')', '.']
    elif lang == 'slv':
        assert lemmas == ['Slovenščina', '[', 'slovénščina', ']', '/', '[', 'sloˈʋenʃtʃina', ']', 'onbiti', 'združen', 'naziv', 'za', 'uraden', 'knjižen', 'jezik', 'Slovenec', 'in', 'skupen', 'ime', 'za', 'narečje', 'in', 'govoriti', ',', 'ki', 'on', 'govoriti', 'ali', 'biti', 'on', 'nekoč', 'govoriti', 'Slovenec', '.']
    elif lang == 'spa':
        if lemmatizer == 'lemmatization_lists_spa':
            assert lemmas == ['El', 'español', 'o', 'castellano', 'ser', 'uno', 'lengua', 'romance', 'procedente', 'del', 'latín', 'hablar', ',', 'perteneciente', 'a', 'lo', 'familia', 'de', 'lengua', 'indoeuropeo', '.']
        elif lemmatizer == 'spacy_spa':
            assert lemmas == ['el', 'español', 'o', 'castellano', 'ser', 'uno', 'lengua', 'romance', 'procedente', 'del', 'latín', 'hablado', ',', 'perteneciente', 'a', 'el', 'familia', 'de', 'lengua', 'indoeuropea', '.']
        else:
            raise Exception(f'Error: Tests for lemmatizer "{lemmatizer}" is skipped!')
    elif lang == 'swe':
        if lemmatizer == 'lemmatization_lists_swe':
            assert lemmas == ['Svenska', '(', 'svensk', '(', 'info', ')', ')', 'vara', 'en', 'östnordiskt', 'språka', 'som', 'tala', 'av', 'ungefär', 'tio', 'miljon', 'person', 'främst', 'i', 'Sverige', 'där', 'språk', 'hare', 'man', 'dominant', 'ställning', 'som', 'huvudspråk', ',', 'mena', 'även', 'som', 'en', 'en', 'nationalspråk', 'i', 'Finland', 'och', 'som', 'enda', 'officiell', 'språka', 'på', 'Åland', '.']
        elif lemmatizer == 'spacy_swe':
            assert lemmas == ['svenska', '(', 'svenska', '(', 'info', ')', ')', 'är', 'ett', 'östnordiskt', 'språk', 'som', 'talas', 'av', 'ungefär', 'tio', 'miljoner', 'personer', 'främst', 'i', 'sverige', 'där', 'språket', 'har', 'en', 'dominant', 'ställning', 'som', 'huvudspråk', ',', 'men', 'även', 'som', 'det', 'ena', 'nationalspråket', 'i', 'finland', 'och', 'som', 'enda', 'officiella', 'språk', 'på', 'åland', '.']
        else:
            raise Exception(f'Error: Tests for lemmatizer "{lemmatizer}" is skipped!')
    elif lang == 'tgl':
        assert lemmas == ['Ang', 'Wikang', 'Tagalog[2', ']', '(', 'Baybayin', ':', 'ᜏᜒᜃᜅ᜔', 'ᜆᜄᜎᜓᜄ᜔', ')', ',', 'na', 'kilala', 'rin', 'sa', 'payak', 'na', 'pangalang', 'Tagalog', ',', 'ay', 'isa', 'sa', 'mga', 'pangunahing', 'wika', 'ng', 'Pilipinas', 'at', 'sinasabing', 'ito', 'ang', 'de', 'facto', '(', '"', 'sa', 'katunayan', '"', ')', 'ngunit', 'hindî', 'de', 'jure', '(', '"', 'sa', 'batas', '"', ')', 'na', 'batayan', 'na', 'siyang', 'pambansang', 'Wikang', 'Filipino', '(', 'mula', '1961', 'hanggang', '1987', ':', 'Pilipino).[2', ']']
    elif lang == 'bod':
        assert lemmas == ['བོད་', 'གི་', 'སྐད་ཡིག་', 'ནི་', 'བོད་ཡུལ་', 'དང་', 'དེ་', 'གི་', 'ཉེ་འཁོར་', 'གི་', 'ས་ཁུལ་', 'སྟེ་', '།']
    elif lang == 'tur':
        assert lemmas == ['Türkçe', 'ya', 'da', 'Türk', 'dil', ',', 'batı', 'Balkanlar’dan', 'başla', 'doğu', 'Hazar', 'Denizi', 'saha', 'kadar', 'konuş', 'Türkî', 'dil', 'dil', 'aile', 'ait', 'son', 'ekle', 'bir', 'dil.[12', ']']
    elif lang == 'ukr':
        if lemmatizer == 'lemmatization_lists_ukr':
            assert lemmas == ['Украї́нська', 'мо́ва', '(', 'МФА', ':', '[', 'ukrɑ̽ˈjɪnʲsʲkɑ̽', 'ˈmɔwɑ̽', ']', ',', 'історичний', 'назвати', '—', 'ру́ська', ',', 'руси́нська[9][10][11', ']', '[', '*', '2', ']', ')', '—', 'національний', 'мова', 'українець', '.']
        elif lemmatizer == 'pymorphy2_morphological_analyzer':
            assert lemmas == ['украї́нський', 'мо́вий', '(', 'мфа', ':', '[', 'ukrɑ̽ˈjɪnʲsʲkɑ̽', 'ˈmɔwɑ̽', ']', ',', 'історичний', 'назва', '—', 'ру́ський', ',', 'руси́нська[9][10][11', ']', '[', '*', '2', ']', ')', '—', 'національний', 'мова', 'українець', '.']
        else:
            raise Exception(f'Error: Tests for lemmatizer "{lemmatizer}" is skipped!')
    elif lang == 'urd':
        assert lemmas == ['اُردُو', 'لشکری', 'زبان[8', ']', '(', 'یا', 'جدید', 'معیاری', 'اردو', ')', 'برصغیر', 'کم', 'معیاری', 'زبان', 'میں', 'سے', 'ایک', 'ہونا', '۔']
    elif lang == 'cym':
        assert lemmas == ['Aelod', "o'r", 'cangen', 'Frythonaidd', "o'r", 'iaith', 'Celtaidd', 'a', 'siarad', 'bod', 'brodorol', 'yn', 'Nghymru', ',', 'can', 'Gymry', 'a', 'pobl', 'arall', 'aredig', 'gwasgar', 'bod', 'Lloegr', ',', 'a', 'can', 'cymuno', 'bechan', 'bod', 'Y', 'Wladfa', ',', 'gwybod', 'Ariannin[7', ']', "yw'r", 'Gymraeg', '(', 'hefyd', 'Cymraeg', 'heb', 'yr', 'bannod', ')', '.']
    else:
        raise Exception(f'Error: Tests for language "{lang}" is skipped!')

if __name__ == '__main__':
    for lang, lemmatizer in test_lemmatizers:
        test_lemmatize(lang, lemmatizer)
