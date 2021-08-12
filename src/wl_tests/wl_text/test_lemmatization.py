#
# Wordless: Tests - Text - Lemmatization
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import sys

sys.path.append('.')

import pytest

from wl_tests import wl_test_init, wl_test_lang_examples
from wl_text import wl_lemmatization, wl_word_tokenization
from wl_utils import wl_conversion, wl_misc

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

    tokens = wl_word_tokenization.wl_word_tokenize(
        main,
        text = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}'),
        lang = lang
    )
    
    lemmas = wl_lemmatization.wl_lemmatize(
        main,
        tokens = wl_misc.flatten_list(tokens),
        lang = lang,
        lemmatizer = lemmatizer
    )

    print(lemmas)

    if lang == 'ast':
        assert lemmas == ["L'asturianu", 'ser', 'unu', 'llingua', 'romance', 'propiu', "d'Asturies,[1", ']', 'perteneciente', 'al', 'subgrupu', 'asturllionés', '.']
    elif lang == 'ben':
        assert lemmas == ['বাংলা', 'ভাষা', '(', 'বাঙলা', ',', 'বাঙ্গলা', ',', 'তথা', 'বাঙ্গালা', 'নামগুলোতেও', 'পরিচিত', ')', 'একটি', 'ইন্দো', '-', 'আর্য', 'ভাষা', ',', 'যা', 'দক্ষিণ', 'এশিয়ার', 'বাঙালি', 'জাতির', 'প্রধান', 'কথ্য', 'ও', 'লেখ্য', 'ভাষা', '।']
    elif lang == 'bul':
        assert lemmas == ['Бъ̀лгарският', 'езѝк', 'съм', 'индоевропейски', 'език', 'от', 'група', 'на', 'южнославянските', 'език', '.']
    elif lang == 'cat':
        if lemmatizer == 'Lemmatization Lists - Catalan Lemma List':
            assert lemmas == ['El', 'català', '(', 'denominació', 'oficial', 'a', 'Catalunya', ',', 'a', 'ell', 'Illes', 'Balears', ',', 'a', 'Andorra', ',', 'a', 'ell', 'ciutat', 'de', 'ell', 'Alguer', 'i', 'tradicional', 'a', 'Catalunya', 'Nord', ')', 'o', 'valencià', '(', 'denominació', 'oficial', 'al', 'País', 'Valencià', 'i', 'tradicional', 'al', 'Carxe', ')', 'ser', 'un', 'llengua', 'romànic', 'parlar', 'a', 'Catalunya', ',', 'ell', 'País', 'Valencià', '(', 'treure', 'de', 'algun', 'comarca', 'i', 'localitat', 'de', 'ell', 'interior', ')', ',', 'ell', 'Illes', 'Balears', ',', 'Andorra', ',', 'ell', 'Franja', 'de', 'Ponent', '(', 'a', 'ell', 'Aragó', ')', ',', 'ell', 'ciutat', 'de', 'ell', 'Alguer', '(', 'a', 'ell', 'illa', 'de', 'Sardenya', ')', ',', 'ell', 'Catalunya', 'del', 'Nord,[8', ']', 'ell', 'Carxe', '(', 'un', 'petit', 'territori', 'de', 'Múrcia', 'poblar', 'per', 'immigrar', 'valencians),[9][10', ']', 'i', 'en', 'comunitat', 'arreu', 'del', 'món', '(', 'entrar', 'ell', 'qual', 'destacar', 'ell', 'de', 'ell', 'Argentina', ',', 'amb', '198.000', 'parlants).[11', ']']
        elif lemmatizer == 'spaCy - Catalan Lemmatizer':
            assert lemmas == ['el', 'català', '(', 'denominació', 'oficial', 'a', 'Catalunya', ',', 'a', 'el', 'Illes', 'Balears', ',', 'a', 'Andorra', ',', 'a', 'el', 'ciutat', 'de', 'el', 'Alguer', 'i', 'tradicional', 'a', 'Catalunya', 'Nord', ')', 'o', 'valencià', '(', 'denominació', 'oficial', 'al', 'País', 'Valencià', 'i', 'tradicional', 'al', 'Carxe', ')', 'és', 'un', 'llengua', 'romànic', 'parlat', 'a', 'Catalunya', ',', 'el', 'País', 'Valencià', '(', 'tret', "d'", 'algun', 'comarca', 'i', 'localitat', 'de', 'el', 'interior', ')', ',', 'el', 'Illes', 'Balears', ',', 'Andorra', ',', 'el', 'Franja', 'de', 'Ponent', '(', 'a', 'el', 'Aragó', ')', ',', 'el', 'ciutat', 'de', 'el', 'Alguer', '(', 'a', 'el', 'illa', 'de', 'Sardenya', ')', ',', 'el', 'Catalunya', 'del', 'Nord,[8', ']', 'el', 'Carxe', '(', 'un', 'petit', 'territori', 'de', 'Múrcia', 'poblat', 'per', 'immigrat', 'valencians),[9][10', ']', 'i', 'en', 'comunitat', 'arreu', 'del', 'món', '(', 'entre', 'el', 'quals', 'destacar', 'el', 'de', 'el', 'Argentina', ',', 'amb', '198.000', 'parlants).[11', ']']
    elif lang == 'hrv':
        assert lemmas == ['Hrvatski', 'jezik', '(', 'ISO', '639', '-', '3', ':', 'hrv', ')', 'skupni', 'biti', 'naziv', 'za', 'nacionalan', 'standardan', 'jezik', 'Hrvata', ',', 'te', 'za', 'skup', 'narječje', 'i', 'govor', 'koji', 'govoriti', 'ili', 'biti', 'nekada', 'govoriti', 'Hrvati', '.']
    elif lang == 'ces':
        assert lemmas == ['Čeština', 'neboli', 'český', 'jazyk', 'on', 'západoslovanský', 'jazyk', ',', 'blízký', 'slovenštině', ',', 'poté', 'lužické', 'srbštině', 'a', 'polštině', '.']
    elif lang == 'dan':
        assert lemmas == ['Dansk', 'være', 'en', 'nordgermansk', 'sprog', 'af', 'den', 'østnordiske', '(', 'kontinental', ')', 'gruppe', ',', 'der', 'tale', 'af', 'ca.', 'seks', 'million', 'menneske', '.']
    elif lang == 'nld':
        assert lemmas == ['het', 'nederlands', 'is', 'een', 'west-germaans', 'taal', 'en', 'de', 'officieel', 'taal', 'van', 'nederland', ',', 'suriname', 'en', 'e', 'van', 'de', 'drie', 'officieel', 'taal', 'van', 'belgië', '.']
    elif lang in ['eng_gb', 'eng_us']:
        if lemmatizer in ['Lemmatization Lists - English Lemma List',
                          'NLTK - WordNet Lemmatizer']:
            assert lemmas == ['English', 'be', 'a', 'West', 'Germanic', 'language', 'originally', 'speak', 'by', 'the', 'inhabitant', 'of', 'early', 'medieval', 'England.[3][4][5', ']']
        elif lemmatizer == 'spaCy - English Lemmatizer':
            assert lemmas == ['English', 'be', 'a', 'west', 'germanic', 'language', 'originally', 'speak', 'by', 'the', 'inhabitant', 'of', 'early', 'medieval', 'England.[3][4][5', ']']
    elif lang == 'est':
        assert lemmas == ['Eesti', 'kee', '(', 'varasem', 'nimetu', 'maakeel', ')', 'olema', 'läänemeresoome', 'lõunarühma', 'kuuluma', 'kee', '.']
    elif lang == 'fra':
        if lemmatizer == 'Lemmatization Lists - French Lemma List':
            assert lemmas == ['Le', 'français', 'être', 'un', 'langue', 'indo-européen', 'de', 'le', 'famille', 'un', 'langue', 'roman', 'dont', 'le', 'locuteurs', 'être', 'appeler', 'francophone', '.']
        elif lemmatizer == 'spaCy - French Lemmatizer':
            assert lemmas == ['le', 'français', 'être', 'un', 'langue', 'indo-européen', 'de', 'le', 'famille', 'de', 'langue', 'roman', 'dont', 'le', 'locuteur', 'être', 'appeler', 'francophone', '.']
    elif lang == 'glg':
        assert lemmas == ['O', 'galego', '(', '[', 'ɡaˈleɣo̝', ']', ')', 'ser', 'un', 'lingua', 'indoeuropeo', 'que', 'pertencer', 'á', 'póla', 'de', 'lingua', 'románico', '.']
    elif lang in ['deu_at', 'deu_de', 'deu_ch']:
        if lemmatizer == 'Lemmatization Lists - German Lemma List':
            assert lemmas == ['Die', 'deutsch', 'Sprache', 'bzw.', 'der', 'deutschen', '(', '[', 'dɔɪ̯tʃ];[26', ']', 'abkürzen', 'dt', '.', 'oder', 'dtsch', '.', ')', 'sein', 'einen', 'westgermanische', 'Sprache', ',', 'der', 'weltweit', 'etwa', '90', 'bis', '105', 'Million', 'Mensch', 'als', 'Muttersprache', 'und', 'weit', 'rund', '80', 'Million', 'als', 'Zweit-', 'oder', 'Fremdsprache', 'dienen', '.']
        elif lemmatizer == 'spaCy - German Lemmatizer':
            assert lemmas == ['der', 'deutsch', 'Sprache', 'bzw.', 'der', 'deutschen', '(', '[', 'dɔɪ̯tʃ];[26', ']', 'abkürzen', 'dt', '.', 'oder', 'dtsch', '.', ')', 'sein', 'einen', 'westgermanische', 'Sprache', ',', 'der', 'weltweit', 'etwa', '90', 'bis', '105', 'Million', 'Mensch', 'als', 'Muttersprache', 'und', 'weit', 'rund', '80', 'Million', 'als', 'Zweit-', 'oder', 'Fremdsprache', 'dienen', '.']
    elif lang == 'grc':
        assert lemmas == ['Ὅτι', 'μὲν', 'σύ', ',', 'ὦ', 'ἀνήρ', 'Ἀθηναῖοι', ',', 'πεπόνθατε', 'ὑπὸ', 'ὁ', 'ἐμός', 'κατηγόρων', ',', 'οὐ', 'οἶδα', '·', 'ἐγὼ', 'δέ', 'οὖν', 'καὶ', 'αὐτὸς', 'ὑπό', 'αὐτός', 'ὀλίγου', 'ἐμαυτοῦ', 'ἐπελαθόμην', ',', 'οὕτως', 'πιθανόω', 'λέγω', '.']
    elif lang == 'ell':
        assert lemmas == ['η', 'ελληνικός', 'γλώσσα', 'ανήκω', 'στην', 'ινδοευρωπαϊκός', 'οικογένεια[10', ']', 'και', 'αποτελώ', 'το', 'μοναδικό', 'μέλος', 'το', 'ελληνικός', 'κλάδος', ',', 'ενώ', 'είναι', 'η', 'επίσημη', 'γλώσσα', 'της', 'ελλάδος', 'και', 'της', 'κύπρος', '.']
    elif lang == 'hun':
        assert lemmas == ['A', 'magyar', 'nyelv', 'az', 'uráli', 'nyelvcsalád', 'tag', ',', 'a', 'finnugor', 'nyelv', 'köz', 'tartozó', 'ugor', 'nyelv', 'egyik', '.']
    elif lang == 'ind':
        assert lemmas == ['Bahasa', 'Indonesia', 'adalah', 'bahasa', 'Melayu', 'baku', 'yang', 'dijadikan', 'bagai', 'bahasa', 'resmi', 'Republik', 'Indonesia[1', ']', 'dan', 'bahasa', 'satu', 'bangsa', 'Indonesia.[2', ']']
    elif lang == 'gle':
        assert lemmas == ['Is', 'ceann', 'de', 'na', 'teangach', 'Ceilteacha', 'í', 'an', 'Ghaeilge', '(', 'nó', 'Gaeilge', 'na', 'hÉireann', 'mar', 'a', 'tabhair', 'ar', 'corruair', ')', ',', 'agus', 'ceann', 'den', 'trí', 'ceann', 'de', 'teangach', 'Ceilteacha', 'air', 'a', 'tabhair', 'na', 'teangach', 'Gaelacha', '(', '.i.', 'an', 'Ghaeilge', ',', 'Gaeilge', 'na', 'hAlban', 'agus', 'Gaeilge', 'Mhanann', ')', 'go', 'áirithe', '.']
    elif lang == 'ita':
        if lemmatizer == 'Lemmatization Lists - Italian Lemma List':
            assert lemmas == ["L'", 'italiano', '(', '[', 'itaˈljaːno][Nota', '1', ']', 'ascolta[?·info', ']', ')', 'essere', 'una', 'lingua', 'romanzo', 'parlato', 'principalmente', 'in', 'Italia', '.']
        elif lemmatizer == 'spaCy - Italian Lemmatizer':
            assert lemmas == ['il', 'italiano', '(', '[', 'itaˈljaːno][nota', '1', ']', 'ascolta[?·info', ']', ')', 'essere', 'uno', 'lingua', 'romanza', 'parlare', 'principalmente', 'in', 'Italia', '.']
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
        if lemmatizer == 'Lemmatization Lists - Persian Lemma List':
            assert lemmas == ['فارسی', 'یا', 'پارسی', 'یکی', 'از', 'زبان\u200cهای', 'هندواروپایی', 'در', 'شاخهٔ', 'زبان\u200cهای', 'ایرانی', 'جنوب', 'غربی', 'است', 'که', 'در', 'کشورهای', 'ایران', '،', 'افغانستان،[۳', ']', 'تاجیکستان[۴', ']', 'را', 'ازبکستان[۵', ']', 'به', 'آن', 'سخن', 'می\u200cگویند', '.']
        elif lemmatizer == 'spaCy - Persian Lemmatizer':
            assert lemmas == ['فارسی', 'یا', 'پارسی', 'یکی', 'از', 'زبان\u200cهای', 'هندواروپایی', 'در', 'شاخهٔ', 'زبان\u200cهای', 'ایرانی', 'جنوب', 'غربی', 'است', 'که', 'در', 'کشورهای', 'ایران', '،', 'افغانستان،[۳', ']', 'تاجیکستان[۴', ']', 'و', 'ازبکستان[۵', ']', 'به', 'آن', 'سخن', 'می\u200cگویند', '.']
    elif lang == 'pol':
        assert lemmas == ['język', 'polski', ',', 'polszczyzna', '–', 'język', 'lechicki', 'z', 'grupa', 'zachodniosłowiańskiej', '(', 'do', 'której', 'należeć', 'również', 'czeski', ',', 'kaszubski', ',', 'słowacki', 'i', 'język', 'łużycki', ')', ',', 'stanowiącej', 'część', 'rodzina', 'indoeuropejski', '.']
    elif lang in ['por_br', 'por_pt']:
        assert lemmas == ['A', 'língua', 'portuguesar', ',', 'também', 'designar', 'português', ',', 'ser', 'umar', 'língua', 'românico', 'flexivo', 'ocidental', 'originar', 'o', 'galego-português', 'falar', 'o', 'Reino', 'da', 'Galiza', 'e', 'o', 'norte', 'de', 'Portugal', '.']
    elif lang == 'ron':
        assert lemmas == ['Limba', 'român', 'fi', 'vrea', 'limbă', 'indo-european', ',', 'din', 'grup', 'italic', 'și', 'din', 'subgrupul', 'oriental', 'al', 'limbă', 'romanice', '.']
    elif lang == 'rus':
        assert lemmas == ['ру́сский', 'язы́к', '(', '[', 'ˈruskʲɪi̯', 'jɪˈzɨk', ']', 'информация', 'о', 'файл', 'слушать', ')', '[', '~', '3', ']', '[', '⇨', ']', '—', 'один', 'из', 'восточнославянский', 'язык', ',', 'национальный', 'язык', 'русский', 'народ', '.']
    elif lang == 'gla':
        assert lemmas == ["'S", 'i', 'cànan', 'dùthchasach', 'na', 'h', '-', 'Alba', 'a', 'th', "'", 'anns', 'a', "'", 'Ghàidhlig', '.']
    elif lang == 'srp_cyrl':
        assert lemmas == ['Српски', 'језик', 'припадати', 'словенски', 'група', 'језик', 'породица', 'индоевропских', 'језика.[12', ']']
    elif lang == 'slk':
        assert lemmas == ['Slovenčina', 'patriť', 'do', 'skupina', 'západoslovanský', 'jazyk', '(', 'spolu', 's', 'čeština', ',', 'poľština', ',', 'horný', 'as', 'dolný', 'lužickou', 'srbčina', 'as', 'kašubčinou', ')', '.']
    elif lang == 'slv':
        assert lemmas == ['Slovenščina', '[', 'slovénščina', ']', '/', '[', 'sloˈʋenʃtʃina', ']', 'onbiti', 'združen', 'naziv', 'za', 'uraden', 'knjižen', 'jezik', 'Slovenec', 'in', 'skupen', 'ime', 'za', 'narečje', 'in', 'govoriti', ',', 'ki', 'on', 'govoriti', 'ali', 'biti', 'on', 'nekoč', 'govoriti', 'Slovenec', '.']
    elif lang == 'spa':
        if lemmatizer == 'Lemmatization Lists - Spanish Lemma List':
            assert lemmas == ['El', 'español', 'o', 'castellano', 'ser', 'uno', 'lengua', 'romance', 'procedente', 'del', 'latín', 'hablar', '.']
        elif lemmatizer == 'spaCy - Spanish Lemmatizer':
            assert lemmas == ['el', 'español', 'o', 'castellano', 'ser', 'uno', 'lenguo', 'romance', 'procedente', 'del', 'latín', 'hablado', '.']
    elif lang == 'swe':
        if lemmatizer == 'Lemmatization Lists - Swedish Lemma List':
            assert lemmas == ['Svenska', '(', 'svensk', '(', 'info', ')', ')', 'vara', 'en', 'östnordiskt', 'språka', 'som', 'tala', 'av', 'ungefär', 'tio', 'miljon', 'person', 'främst', 'i', 'Sverige', 'där', 'språk', 'hare', 'man', 'dominant', 'ställning', 'som', 'huvudspråk', ',', 'mena', 'även', 'som', 'en', 'en', 'nationalspråk', 'i', 'Finland', 'och', 'som', 'enda', 'officiell', 'språka', 'på', 'Åland', '.']
        elif lemmatizer == 'spaCy - Swedish Lemmatizer':
            assert lemmas == ['svenska', '(', 'svenska', '(', 'info', ')', ')', 'är', 'ett', 'östnordiskt', 'språk', 'som', 'talas', 'av', 'ungefär', 'tio', 'miljoner', 'personer', 'främst', 'i', 'sverige', 'där', 'språket', 'har', 'en', 'dominant', 'ställning', 'som', 'huvudspråk', ',', 'men', 'även', 'som', 'det', 'ena', 'nationalspråket', 'i', 'finland', 'och', 'som', 'enda', 'officiella', 'språk', 'på', 'åland', '.']
    elif lang == 'tgl':
        assert lemmas == ['Ang', 'Wikang', 'Tagalog[2', ']', '(', 'Baybayin', ':', 'ᜏᜒᜃᜅ᜔', 'ᜆᜄᜎᜓᜄ᜔', ')', ',', 'na', 'kilala', 'rin', 'sa', 'payak', 'na', 'pangalang', 'Tagalog', ',', 'ay', 'isa', 'sa', 'mga', 'pangunahing', 'wika', 'ng', 'Pilipinas', 'at', 'sinasabing', 'ito', 'ang', 'de', 'facto', '(', '"', 'sa', 'katunayan', '"', ')', 'ngunit', 'hindî', 'de', 'jure', '(', '"', 'sa', 'batas', '"', ')', 'na', 'batayan', 'na', 'siyang', 'pambansang', 'Wikang', 'Filipino', '(', 'mula', '1961', 'hanggang', '1987', ':', 'Pilipino).[2', ']']
    elif lang == 'bod':
        assert lemmas == ['བོད་', 'གི་', 'སྐད་ཡིག་', 'ནི་', 'བོད་ཡུལ་', 'དང་', 'དེ་', 'གི་', 'ཉེ་འཁོར་', 'གི་', 'ས་ཁུལ་', 'སྟེ་', ' །']
    elif lang == 'tur':
        assert lemmas == ['Türkçe', 'ya', 'da', 'Türk', 'dil', ',', 'batı', 'Balkanlar’dan', 'başla', 'doğu', 'Hazar', 'Denizi', 'saha', 'kadar', 'konuş', 'Türkî', 'dil', 'dil', 'aile', 'ait', 'son', 'ekle', 'bir', 'dil.[12', ']']
    elif lang == 'ukr':
        if lemmatizer == 'Lemmatization Lists - Ukrainian Lemma List':
            assert lemmas == ['Украї́нська', 'мо́ва', '(', 'МФА', ':', '[', 'ukrɑ̽ˈjɪnʲsʲkɑ̽', 'ˈmɔwɑ̽', ']', ',', 'історичний', 'назвати', '—', 'ру́ська', ',', 'руси́нська[9][10][11', ']', '[', '*', '2', ']', ')', '—', 'національний', 'мова', 'українець', '.']
        elif lemmatizer == 'pymorphy2 - Morphological Analyzer':
            assert lemmas == ['украї́нський', 'мо́вий', '(', 'мфа', ':', '[', 'ukrɑ̽ˈjɪnʲsʲkɑ̽', 'ˈmɔwɑ̽', ']', ',', 'історичний', 'назва', '—', 'ру́ський', ',', 'руси́нська[9][10][11', ']', '[', '*', '2', ']', ')', '—', 'національний', 'мова', 'українець', '.']
    elif lang == 'urd':
        assert lemmas == ['اُردُو', 'لشکری', 'زبان[8', ']', '(', 'یا', 'جدید', 'معیاری', 'اردو', ')', 'برصغیر', 'کم', 'معیاری', 'زبان', 'میں', 'سے', 'ایک', 'ہونا', '۔']
    elif lang == 'cym':
        assert lemmas == ['Aelod', "o'r", 'cangen', 'Frythonaidd', "o'r", 'iaith', 'Celtaidd', 'a', 'siarad', 'bod', 'brodorol', 'yn', 'Nghymru', ',', 'can', 'Gymry', 'a', 'pobl', 'arall', 'aredig', 'gwasgar', 'bod', 'Lloegr', ',', 'a', 'can', 'cymuno', 'bechan', 'bod', 'Y', 'Wladfa', ',', 'gwybod', 'Ariannin[7', ']', "yw'r", 'Gymraeg', '(', 'hefyd', 'Cymraeg', 'heb', 'yr', 'bannod', ')', '.']
    else:
        raise Exception(f'Warning: language code "{lang}" is absent from the list!')

if __name__ == '__main__':
    for lang, lemmatizer in test_lemmatizers:
        test_lemmatize(lang, lemmatizer)
