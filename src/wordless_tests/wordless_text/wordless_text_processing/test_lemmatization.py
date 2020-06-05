#
# Wordless: Tests - Text - Text Processing - Lemmatization
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import sys

sys.path.append('.')

import pytest

from wordless_tests import wordless_test_init, wordless_test_lang_examples
from wordless_text import wordless_text_processing
from wordless_utils import wordless_conversion

test_lemmatizers = []

main = wordless_test_init.Wordless_Test_Main()

for lang, lemmatizers in main.settings_global['lemmatizers'].items():
    for lemmatizer in lemmatizers:
        # Temporarily disable testing of Tibetan lemmatizer due to memory issues relating to botok
        if lang != 'bod':
            test_lemmatizers.append((lang, lemmatizer))

@pytest.mark.parametrize('lang, lemmatizer', test_lemmatizers)
def test_lemmatize(lang, lemmatizer, show_results = False):
    lang_text = wordless_conversion.to_lang_text(main, lang)

    tokens = wordless_text_processing.wordless_word_tokenize(
        main,
        text = getattr(wordless_test_lang_examples, f'SENTENCE_{lang.upper()}'),
        lang = lang
    )
    
    lemmas = wordless_text_processing.wordless_lemmatize(
        main,
        tokens = tokens,
        lang = lang,
        lemmatizer = lemmatizer
    )

    if show_results:
        print(lemmas)

    if lang == 'ast':
        assert lemmas == ["L'asturianu", 'ser', 'unu', 'llingua', 'romance', 'propiu', "d'Asturies,[1", ']', 'perteneciente', 'al', 'subgrupu', 'asturllionés', '.']
    elif lang == 'bul':
        assert lemmas == ['Бъ̀лгарският', 'езѝк', 'съм', 'индоевропейски', 'език', 'от', 'група', 'на', 'южнославянските', 'език', '.']
    elif lang == 'cat':
        assert lemmas == ['El', 'català', '(', 'denominació', 'oficial', 'a', 'Catalunya', ',', 'a', 'ell', 'Illes', 'Balears', ',', 'a', 'Andorra', ',', 'a', 'ell', 'ciutat', 'de', 'ell', 'Alguer', 'i', 'tradicional', 'a', 'Catalunya', 'Nord', ')', 'o', 'valencià', '(', 'denominació', 'oficial', 'al', 'País', 'Valencià', 'i', 'tradicional', 'al', 'Carxe', ')', 'ser', 'un', 'llengua', 'romànic', 'parlar', 'a', 'Catalunya', ',', 'ell', 'País', 'Valencià', '(', 'treure', 'de', 'algun', 'comarca', 'i', 'localitat', 'de', 'ell', 'interior', ')', ',', 'ell', 'Illes', 'Balears', ',', 'Andorra', ',', 'ell', 'Franja', 'de', 'Ponent', '(', 'a', 'ell', 'Aragó', ')', ',', 'ell', 'ciutat', 'de', 'ell', 'Alguer', '(', 'a', 'ell', 'illa', 'de', 'Sardenya', ')', ',', 'ell', 'Catalunya', 'del', 'Nord,[8', ']', 'ell', 'Carxe', '(', 'un', 'petit', 'territori', 'de', 'Múrcia', 'poblar', 'per', 'immigrar', 'valencians),[9][10', ']', 'i', 'en', 'petita', 'comunitat', 'arreu', 'del', 'món', '(', 'entrar', 'ell', 'qual', 'destacar', 'ell', 'de', 'ell', 'Argentina', ',', 'amb', '195.000', 'parlants).[11', ']']
    elif lang == 'ces':
        assert lemmas == ['Čeština', 'neboli', 'český', 'jazyk', 'on', 'západoslovanský', 'jazyk', ',', 'blízký', 'slovenštině', ',', 'poté', 'lužické', 'srbštině', 'a', 'polštině', '.']
    elif lang == 'nld':
        assert lemmas == ['het', 'nederlands', 'zijn', 'een', 'west-germaans', 'taal', 'en', 'de', 'moedertaal', 'van', 'de', 'veel', 'inwoner', 'van', 'nederland', ',', 'belgië', 'en', 'suriname', '.']
    elif lang == 'eng':
        if lemmatizer == 'Lemmatization Lists - English Lemma List':
            assert lemmas == ['English', 'be', 'a', 'West', 'Germanic', 'language', 'that', 'be', '1', 'speak', 'in', 'early', 'medieval', 'England', 'and', 'eventually', 'become', 'a', 'global', 'lingua', 'franca.[4][5', ']']
        elif lemmatizer == 'NLTK - WordNet Lemmatizer':
            assert lemmas == ['English', 'be', 'a', 'West', 'Germanic', 'language', 'that', 'be', 'first', 'speak', 'in', 'early', 'medieval', 'England', 'and', 'eventually', 'become', 'a', 'global', 'lingua', 'franca.[4][5', ']']
        elif lemmatizer == 'spaCy - English Lemmatizer':
            assert lemmas == ['English', 'be', 'a', 'West', 'germanic', 'language', 'that', 'be', 'first', 'speak', 'in', 'early', 'medieval', 'England', 'and', 'eventually', 'become', 'a', 'global', 'lingua', 'franca.[4][5', ']']
    elif lang == 'est':
        assert lemmas == ['Eesti', 'kee', '(', 'varasem', 'nimetu', ':', 'maakeel', ')', 'olema', 'läänemeresoome', 'lõunarühma', 'kuuluma', 'kee', '.']
    elif lang == 'fra':
        if lemmatizer == 'Lemmatization Lists - French Lemma List':
            assert lemmas == ['Le', 'français', 'être', 'un', 'langue', 'indo-européen', 'de', 'le', 'famille', 'un', 'langue', 'roman', '.']
        elif lemmatizer == 'spaCy - French Lemmatizer':
            assert lemmas == ['le', 'français', 'être', 'un', 'langue', 'indo-européen', 'de', 'le', 'famille', 'un', 'langue', 'roman', '.']
    elif lang == 'glg':
        assert lemmas == ['O', 'galego', '(', '[', 'ɡaˈleɣo̝', ']', ')', 'ser', 'un', 'lingua', 'indoeuropeo', 'que', 'pertencer', 'á', 'póla', 'de', 'lingua', 'románico', '.']
    elif lang == 'deu':
        if lemmatizer == 'Lemmatization Lists - German Lemma List':
            assert lemmas == ['Die', 'deutsch', 'Sprache', 'bzw.', 'Deutsch', '(', '[', 'dɔʏ̯t͡ʃ', ']', ';', 'abkürzen', 'dt', '.', 'oder', 'dtsch', '.', ')', 'sein', 'einen', 'westgermanische', 'Sprache', '.']
        elif lemmatizer == 'spaCy - German Lemmatizer':
            assert lemmas == ['der', 'deutsch', 'Sprache', 'bzw.', 'Deutsch', '(', '[', 'dɔʏ̯t͡ʃ', ']', ';', 'abkürzen', 'dt', '.', 'oder', 'dtsch', '.', ')', 'sein', 'einen', 'westgermanische', 'Sprache', '.']
    elif lang == 'grc':
        assert lemmas == ['Με', 'τον', 'όρο', 'αρχαία', 'ελληνική', 'γλώσσα', 'εννοείται', 'μια', 'μορφή', 'της', 'ελληνικής', 'γλώσσας', ',', 'πού', 'ομιλούνταν', 'κατά', 'τους', 'αρχαϊκούς', 'χρόνους', 'και', 'την', 'κλασική', 'αρχαιότητα', '.']
    elif lang == 'ell':
        assert lemmas == ['η', 'ελληνικός', 'γλώσσα', 'ανήκω', 'στην', 'ινδοευρωπαϊκός', 'οικογένεια[9', ']', 'και', 'συγκεκριμένα', 'στον', 'ελληνικό', 'κλάδο', ',', 'μαζί', 'με', 'την', 'τσακωνικός', ',', 'ενώ', 'είναι', 'η', 'επίσημη', 'γλώσσα', 'της', 'Ελλάδος', 'και', 'της', 'Κύπρου', '.']
    elif lang == 'hun':
        assert lemmas == ['A', 'magyar', 'nyelv', 'az', 'uráli', 'nyelvcsalád', 'tag', ',', 'a', 'finnugor', 'nyelv', 'köz', 'tartozó', 'ugor', 'nyelv', 'egyik', '.']
    elif lang == 'gle':
        assert lemmas == ['Is', 'ceann', 'de', 'na', 'teangach', 'Ceilteacha', 'í', 'an', 'Ghaeilge', '(', 'nó', 'Gaeilge', 'na', 'hÉireann', 'mar', 'a', 'tabhair', 'ar', 'corruair', ')', ',', 'agus', 'ceann', 'den', 'trí', 'ceann', 'de', 'teangach', 'Ceilteacha', 'air', 'a', 'tabhair', 'na', 'teangach', 'Gaelacha', '(', '.i.', 'an', 'Ghaeilge', ',', 'Gaeilge', 'na', 'hAlban', 'agus', 'Gaeilge', 'Mhanann', ')', 'go', 'áirithe', '.']
    elif lang == 'ita':
        assert lemmas == ["L'", 'italiano', '(', '[', 'itaˈljaːno][Nota', '1', ']', 'ascolta[?·info', ']', ')', 'essere', 'una', 'lingua', 'romanzo', 'parlato', 'principalmente', 'in', 'Italia', '.']
    elif lang == 'lit':
        assert lemmas == ['lietuvė', 'kalbėti', '–', 'ižti', 'baltas', 'prokalbės', 'kilęs', 'lietuvė', 'tauta', 'kalbėti', ',', '-PRON-', 'Lietuvoje', 'būti', 'valstybinis', ',', 'o', 'Europos', 'sąjunga', '–', 'viena', 'ižti', 'oficialus', 'kalbus', '.']
    elif lang == 'glv':
        assert lemmas == ['She', 'Gaelg', '(', 'graït', ':', '/gɪlg/', ')', 'çhengey', 'Gaelagh', 'Mannin', '.']
    elif lang == 'nob':
        assert lemmas == ['bokmål', 'være', 'en', 'varietet', 'av', 'norsk', 'språk', '.']
    elif lang == 'fas':
        assert lemmas == ['فارسی', 'یا', 'پارسی', 'یکی', 'از', 'زبان\u200cهای', 'هندواروپایی', 'در', 'شاخهٔ', 'زبان\u200cهای', 'ایرانی', 'جنوب', 'غربی', 'است', 'که', 'در', 'کشورهای', 'ایران', '،', 'افغانستان،[۳', ']', 'تاجیکستان[۴', ']', 'را', 'ازبکستان[۵', ']', 'به', 'آن', 'سخن', 'می\u200cگویند', '.']
    elif lang == 'por':
        assert lemmas == ['A', 'língua', 'portuguesar', ',', 'também', 'designar', 'português', ',', 'ser', 'umar', 'língua', 'românico', 'flexivo', 'ocidental', 'originar', 'o', 'galego-português', 'falar', 'o', 'Reino', 'da', 'Galiza', 'e', 'o', 'norte', 'de', 'Portugal', '.']
    elif lang == 'ron':
        assert lemmas == ['Limba', 'român', 'fi', 'vrea', 'limbă', 'indo', '-', 'european', ',', 'din', 'grup', 'italic', 'și', 'din', 'subgrupul', 'oriental', 'al', 'limbă', 'romanice', '.']
    elif lang == 'rus':
        assert lemmas == ['ру́сский', 'язы́к', '(', '[', 'ˈruskʲɪi̯', 'jɪˈzɨk', ']', 'информация', 'о', 'файл', 'слушать', ')', '[', '~', '3', ']', '[', '⇨', ']', '—', 'один', 'из', 'восточнославянский', 'язык', ',', 'национальный', 'язык', 'русский', 'народ', '.']
    elif lang == 'gla':
        assert lemmas == ["'S", 'i', 'cànan', 'dùthchasach', 'na', 'h', '-', 'Alba', 'a', 'th', "'", 'anns', 'a', "'", 'Ghàidhlig', '.']
    elif lang == 'slk':
        assert lemmas == ['Slovenčina', 'patriť', 'do', 'skupina', 'západoslovanský', 'jazyk', '(', 'spolu', 's', 'čeština', ',', 'poľština', ',', 'horný', 'as', 'dolný', 'lužickou', 'srbčina', 'as', 'kašubčinou', ')', '.']
    elif lang == 'slv':
        assert lemmas == ['Slovenščina', '[', 'slovénščina', ']', '/', '[', 'sloˈʋenʃtʃina', ']', 'onbiti', 'združen', 'naziv', 'za', 'uraden', 'knjižen', 'jezik', 'Slovenec', 'in', 'skupen', 'ime', 'za', 'narečje', 'in', 'govoriti', ',', 'ki', 'on', 'govoriti', 'ali', 'biti', 'on', 'nekoč', 'govoriti', 'Slovenec', '.']
    elif lang == 'spa':
        assert lemmas == ['El', 'español', 'o', 'castellano', 'ser', 'uno', 'lengua', 'romance', 'procedente', 'del', 'latín', 'hablar', '.']
    elif lang == 'swe':
        assert lemmas == ['Svenska', '(', 'svensk', '(', 'info', ')', ')', 'vara', 'en', 'östnordiskt', 'språka', 'som', 'tala', 'av', 'ungefär', 'tio', 'miljon', 'person', 'främst', 'i', 'Sverige', 'där', 'språk', 'hare', 'man', 'dominant', 'ställning', 'som', 'huvudspråk', ',', 'mena', 'även', 'som', 'en', 'en', 'nationalspråk', 'i', 'Finland', 'och', 'som', 'enda', 'officiell', 'språka', 'på', 'Åland', '.']
    elif lang == 'bod':
        assert lemmas == ['༄༅། ། ', 'རྒྱ་གར་', 'སྐད་', 'དུ་', ' ། ', 'བོ་', ' དྷི་', ' སཏྭ་', ' ཙརྻ་', 'ཨ་བ་', 'ཏ་', 'ར་', ' ། ', 'བོད་སྐད་', 'དུ་', ' ། ', 'བྱང་ཆུབ་', 'སེམས་དཔའ་', 'གི་', 'སྤྱོད་པ་', 'ལ་', 'འཇུག་པ་', ' ། ། ', 'སངས་རྒྱས་', 'དང་', 'བྱང་ཆུབ་', 'སེམས་དཔའ་', 'ཐམས་ཅད་', 'ལ་', 'ཕྱག་', 'འཚལ་', 'ལོ་', ' ། ། ', 'བདེ་གཤེགས་', 'ཆོ་', 'ཀྱི་', 'སྐུ་', 'མངའ་', 'སྲ་', 'བཅའ་', 'དང་', ' ། ། ', 'ཕྱག་འོས་', 'ཀུན་', 'ལ་', 'ཀྱང་', 'གུས་པ་', 'ལ་', 'ཕྱག་', 'འཚལ་', 'ཏེ་', ' ། ། ', 'བདེ་གཤེགས་', 'སྲ་', 'ཀྱི་', 'སྡོམ་', 'ལ་', 'འཇུག་པ་', 'ནི་', ' ། ། ', 'ལུང་', 'བཞིན་', 'མདོར་བསྡུས་', 'ན་', 'ནི་', 'བརྗོད་པ་', 'ལ་', 'བྱ་', ' ། །']
    elif lang == 'ukr':
        if lemmatizer == 'Lemmatization Lists - Ukrainian Lemma List':
            assert lemmas == ['Украї́нська', 'мо́ва', '(', 'МФА', ':', '[', 'ukrɑ̽ˈjɪnʲsʲkɑ̽', 'ˈmɔwɑ̽', ']', ',', 'історичний', 'назвати', '—', 'ру́ська', ',', 'руси́нська[9][10][11', ']', '[', '*', '2', ']', ')', '—', 'національний', 'мова', 'українець', '.']
        elif lemmatizer == 'pymorphy2 - Morphological Analyzer':
            assert lemmas == ['украї́нський', 'мо́вий', '(', 'мфа', ':', '[', 'ukrɑ̽ˈjɪnʲsʲkɑ̽', 'ˈmɔwɑ̽', ']', ',', 'історичний', 'назва', '—', 'ру́ський', ',', 'руси́нська[9][10][11', ']', '[', '*', '2', ']', ')', '—', 'національний', 'мова', 'українець', '.']
    elif lang == 'cym':
        assert lemmas == ['Aelod', "o'r", 'cangen', 'Frythonaidd', "o'r", 'iaith', 'Celtaidd', 'a', 'siarad', 'bod', 'brodorol', 'yn', 'Nghymru', ',', 'can', 'Gymry', 'a', 'pobl', 'arall', 'aredig', 'gwasgar', 'bod', 'Lloegr', ',', 'a', 'can', 'cymuno', 'bechan', 'bod', 'Y', 'Wladfa', ',', 'gwybod', 'Ariannin[7', ']', "yw'r", 'Gymraeg', '(', 'hefyd', 'Cymraeg', 'heb', 'yr', 'bannod', ')', '.']

if __name__ == '__main__':
    for lang, lemmatizers in main.settings_global['lemmatizers'].items():
        for lemmatizer in lemmatizers:
            if lang not in ['bod']:
                test_lemmatize(lang, lemmatizer, show_results = True)
