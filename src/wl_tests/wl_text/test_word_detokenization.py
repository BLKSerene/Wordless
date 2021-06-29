# -*- coding: utf-8 -*-

#
# Wordless: Tests - Text - Word Detokenization
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
from wl_text import wl_word_detokenization, wl_word_tokenization
from wl_utils import wl_conversion, wl_misc

test_word_detokenizers = []

main = wl_test_init.Wl_Test_Main()

for lang, word_detokenizers in main.settings_global['word_detokenizers'].items():
    for word_detokenizer in word_detokenizers:
        if lang not in ['other']:
            test_word_detokenizers.append((lang, word_detokenizer))

@pytest.mark.parametrize('lang, word_detokenizer', test_word_detokenizers)
def test_word_detokenize(lang, word_detokenizer, show_results = False):
    lang_text = wl_conversion.to_lang_text(main, lang)

    tokens = wl_word_tokenization.wl_word_tokenize(
        main,
        text = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}'),
        lang = lang
    )
    tokens = list(wl_misc.flatten_list(tokens))
    
    text = wl_word_detokenization.wl_word_detokenize(
        main,
        tokens = tokens,
        lang = lang,
        word_detokenizer = word_detokenizer
    )

    if show_results:
        print(f'{lang} / {word_detokenizer}:')
        print(text)

    if lang == 'asm':
        assert text == 'অসমীয়া ভাষা হৈছে সকলোতকৈ পূৰ্বীয় ভাৰতীয়-আৰ্য ভাষা ।'
    elif lang == 'ben':
        assert text == 'বাংলা ভাষা (বাঙলা, বাঙ্গলা, তথা বাঙ্গালা নামগুলোতেও পরিচিত) একটি ইন্দো - আর্য ভাষা, যা দক্ষিণ এশিয়ার বাঙালি জাতির প্রধান কথ্য ও লেখ্য ভাষা ।'
    elif lang == 'cat':
        assert text == "El català (denominació oficial a Catalunya, a les Illes Balears, a Andorra, a la ciutat de l' Alguer i tradicional a Catalunya Nord) o valencià (denominació oficial al País Valencià i tradicional al Carxe) és una llengua romànica parlada a Catalunya, el País Valencià (tret d' algunes comarques i localitats de l' interior), les Illes Balears, Andorra, la Franja de Ponent (a l' Aragó), la ciutat de l' Alguer (a l' illa de Sardenya), la Catalunya del Nord,[8] el Carxe (un petit territori de Múrcia poblat per immigrats valencians),[9][10] i en petites comunitats arreu del món (entre les quals destaca la de l' Argentina, amb 195.000 parlants).[11]"
    elif lang == 'zho_cn':
        assert text == '汉语，又称汉文、中文、中国话、中国语、华语、华文、唐话[2]，或被视为一个语族，或被视为隶属于汉藏语系汉语族之一种语言。'
    elif lang == 'zho_tw':
        assert text == '漢語，又稱漢文、中文、中國話、中國語、華語、華文、唐話[2]，或被視為一個語族，或被視為隸屬於漢藏語系漢語族之一種語言。'
    elif lang == 'ces':
        assert text == 'Čeština neboli český jazyk je západoslovanský jazyk, nejbližší slovenštině, poté lužické srbštině a polštině.'
    elif lang == 'nld':
        assert text == 'Het Nederlands is een West-Germaanse taal en de moedertaal van de meeste inwoners van Nederland, België en Suriname.'
    elif lang == 'eng':
        assert text == 'English is a West Germanic language originally spoken by the early medieval England.[3][4][5]'
    elif lang == 'fin':
        assert text == 'Suomen kieli (suomi) on uralilaisten kielten itämerensuomalaiseen ryhmään kuuluva kieli.'
    elif lang == 'fra':
        assert text == 'Le français est une langue indo-européenne de la famille des langues romanes.'
    elif lang == 'deu':
        if word_detokenizer == 'NLTK - Penn Treebank Detokenizer':
            assert text == 'Die deutsche Sprache bzw. Deutsch ([dɔʏ̯t͡ʃ];abgekürzt dt . oder dtsch .) ist eine westgermanische Sprache.'
        elif word_detokenizer == 'Sacremoses - Moses Detokenizer':
            assert text == 'Die deutsche Sprache bzw. Deutsch ([dɔʏ̯t͡ʃ];abgekürzt dt. oder dtsch.) ist eine westgermanische Sprache.'
    elif lang == 'ell':
        assert text == 'Η ελληνική γλώσσα ανήκει στην ινδοευρωπαϊκή οικογένεια[9]και συγκεκριμένα στον ελληνικό κλάδο, μαζί με την τσακωνική, ενώ είναι η επίσημη γλώσσα της Ελλάδος και της Κύπρου.'
    elif lang == 'guj':
        assert text == 'ગુજરાતી ‍(/ɡʊdʒəˈrɑːti/[૭], રોમન લિપિમાં: Gujarātī, ઉચ્ચાર: [ɡudʒəˈɾɑːtiː]) ભારત દેશના ગુજરાત રાજ્યની ઇન્ડો-આર્યન ભાષા છે, અને મુખ્યત્વે ગુજરાતી લોકો દ્વારા બોલાય છે.'
    elif lang == 'hin':
        assert text == 'हिन्दी विश्व की एक प्रमुख भाषा है एवं भारत की राजभाषा है ।'
    elif lang == 'hun':
        assert text == 'A magyar nyelv az uráli nyelvcsalád tagja, a finnugor nyelvek közé tartozó ugor nyelvek egyike.'
    elif lang == 'isl':
        assert text == 'Íslenska er vesturnorrænt, germanskt og indóevrópskt tungumál sem er einkum talað og ritað á Íslandi og er móðurmál langflestra Íslendinga.[4]'
    elif lang == 'gle':
        assert text == 'Is ceann de na teangacha Ceilteacha í an Ghaeilge (nó Gaeilge na hÉireann mar a thugtar uirthi corruair), agus ceann den dtrí cinn de theangacha Ceilteacha ar a dtugtar na teangacha Gaelacha (.i. an Ghaeilge, Gaeilge na hAlban agus Gaeilge Mhanann) go háirithe.'
    elif lang == 'ita':
        if word_detokenizer == 'NLTK - Penn Treebank Detokenizer':
            assert text == "L' italiano ([itaˈljaːno][Nota 1] ascolta[?·info]) è una lingua romanza parlata principalmente in Italia."
        elif word_detokenizer == 'Sacremoses - Moses Detokenizer':
            assert text == "L'italiano ([itaˈljaːno][Nota 1] ascolta[?·info]) è una lingua romanza parlata principalmente in Italia."
    elif lang == 'jpn':
        assert text == '日本語(にほんご、にっぽんご[注1])は、主に日本国内や日本人同士の間で使用されている言語である。'
    elif lang == 'kan':
        assert text == 'ದ್ರಾವಿಡ ಭಾಷೆಗಳಲ್ಲಿ ಪ್ರಾಮುಖ್ಯವುಳ್ಳ ಭಾಷೆಯೂ ಭಾರತದ ಪುರಾತನವಾದ ಭಾಷೆಗಳಲ್ಲಿ ಒಂದೂ ಆಗಿರುವ ಕನ್ನಡ ಭಾಷೆಯನ್ನು ಅದರ ವಿವಿಧ ರೂಪಗಳಲ್ಲಿ ಸುಮಾರು ೪೫ ದಶಲಕ್ಷ ಜನರು ಆಡು ನುಡಿಯಾಗಿ ಬಳಸುತ್ತಲಿದ್ದಾರೆ.'
    elif lang == 'lav':
        assert text == 'Latviešu valoda ir dzimtā valoda apmēram 1,7 miljoniem cilvēku, galvenokārt Latvijā, kur tā ir vienīgā valsts valoda.[3]'
    elif lang == 'lit':
        assert text == 'Lietuvių kalba – iš baltų prokalbės kilusi lietuvių tautos kalba, kuri Lietuvoje yra valstybinė, o Europos Sąjungoje – viena iš oficialiųjų kalbų.'
    elif lang == 'mal':
        assert text == 'ഇന്ത്യയിൽ പ്രധാനമായും കേരള സംസ്ഥാനത്തിലും ലക്ഷദ്വീപിലും പുതുച്ചേരിയുടെ ഭാഗമായ മയ്യഴിയിലും സംസാരിക്കപ്പെടുന്ന ഭാഷയാണ് മലയാളം.'
    elif lang == 'mar':
        assert text == 'मराठीभाषा ही इंडो - युरोपीय भाषाकुलातील एक भाषा आहे.'
    elif lang == 'mni':
        assert text == 'ꯃꯤꯇꯩꯂꯣꯟ ꯍꯥꯏꯕꯁꯤ ꯏꯟꯗꯤꯌꯥ ꯑꯋꯥꯡ-ꯅꯣꯡꯄꯣꯛꯇ ꯂꯩꯕ ꯃꯅꯤꯄꯨꯔꯗ ꯃꯔꯨꯑꯣꯏꯅ ꯉꯥꯡꯅꯕ ꯇꯤꯕꯦꯇꯣ-ꯕꯔꯃꯟ ꯀꯥꯡꯂꯨꯞꯇ ꯆꯤꯡꯕ ꯂꯣꯟ ꯑꯃꯅꯤ ꯫ ꯚꯥꯔꯠ ꯂꯩꯉꯥꯛꯅꯥ ꯁꯛꯈꯪꯂꯕ ꯂꯣꯟ ꯲꯲ ꯁꯤꯡꯒꯤ ꯃꯅꯨꯡꯗ ꯃꯤꯇꯩꯂꯣꯟꯁꯤꯁꯨ ꯑꯃꯅꯤ ꯫ ꯃꯤꯇꯩꯂꯣꯟ ꯑꯁꯤ ꯏꯟꯗꯤꯌꯥꯒꯤ ꯁ ꯭ ꯇꯦꯠ ꯑꯣꯏꯔꯤꯕ ꯑꯁꯥꯝ ꯑꯃꯁꯨꯡ ꯇ ꯭ ꯔꯤꯄꯨꯔꯥ ꯑꯃꯗꯤ ꯑꯇꯩ ꯂꯩꯕꯥꯛꯁꯤꯡꯗ ꯍꯥꯏꯕꯗꯤ ꯕꯥꯡꯂꯥꯗꯦꯁ ꯑꯃꯁꯨꯡ ꯑꯋꯥꯗꯁꯨ ꯉꯥꯡꯅꯩ ꯫ ꯏꯪ ꯀꯨꯝꯖ ꯲꯰꯱꯱ ꯒꯤ ꯃꯤꯀꯣꯛ ꯊꯤꯕꯗ ꯃꯤꯇꯩꯂꯣꯟꯕꯨ ꯏꯃꯥꯂꯣꯟ ꯑꯣꯢꯅ ꯉꯥꯡꯕꯒꯤ ꯃꯤꯁꯤꯡ ꯂꯤꯆꯥ ꯱꯸ ꯃꯨꯛ ꯁꯨꯢ ꯫'
    elif lang == 'ori':
        assert text == 'ଓଡ଼ିଆ (ଇଂରାଜୀ ଭାଷାରେ Odia / əˈdiːə / or Oriya / ɒˈriːə /,) ଏକ ଭାରତୀୟ ଭାଷା ଯାହା ଏକ ଇଣ୍ଡୋ-ଇଉରୋପୀୟ ଭାଷାଗୋଷ୍ଠୀ ଅନ୍ତର୍ଗତ ଇଣ୍ଡୋ-ଆର୍ଯ୍ୟ ଭାଷା ।'
    elif lang == 'pol':
        assert text == 'Język polski, polszczyzna – język lechicki z grupy zachodniosłowiańskiej (do której należą również czeski, kaszubski, słowacki i języki łużyckie), stanowiącej część rodziny indoeuropejskiej.'
    elif lang == 'por':
        assert text == 'A língua portuguesa, também designada português, é uma língua românica flexiva ocidental originada no galego-português falado no Reino da Galiza e no norte de Portugal.'
    elif lang == 'pan':
        assert text == 'ਪੰਜਾਬੀ ਭਾਸ਼ਾ / pʌnˈdʒɑːbi / (ਸ਼ਾਹਮੁਖੀ: ‎ پنجابی ‎) (ਗੁਰਮੁਖੀ: ਪੰਜਾਬੀ) ਪੰਜਾਬ ਦੀ ਭਾਸ਼ਾ, ਜਿਸ ਨੂੰ ਪੰਜਾਬ ਖੇਤਰ ਦੇ ਵਸਨੀਕ ਜਾਂ ਸੰਬੰਧਿਤ ਲੋਕ ਬੋਲਦੇ ਹਨ । [1]'
    elif lang == 'ron':
        assert text == 'Limba română este o limbă indo-europeană, din grupul italic și din subgrupul oriental al limbilor romanice.'
    elif lang == 'rus':
        assert text == 'Ру́сский язы́к ([ˈruskʲɪi̯ jɪˈzɨk] Информация о файле слушать) [~ 3] [⇨] — один из восточнославянских языков, национальный язык русского народа.'
    elif lang == 'slk':
        assert text == 'Slovenčina patrí do skupiny západoslovanských jazykov (spolu s češtinou, poľštinou, hornou a dolnou lužickou srbčinou a kašubčinou).'
    elif lang == 'slv':
        assert text == 'Slovenščina [slovénščina] / [sloˈʋenʃtʃina] je združeni naziv za uradni knjižni jezik Slovencev in skupno ime za narečja in govore, ki jih govorijo ali so jih nekoč govorili Slovenci.'
    elif lang == 'spa':
        assert text == 'El español o castellano es una lengua romance procedente del latín hablado.'
    elif lang == 'swe':
        assert text == 'Svenska (svenska (info)) är ett östnordiskt språk som talas av ungefär tio miljoner personer främst i Sverige där språket har en dominant ställning som huvudspråk, men även som det ena nationalspråket i Finland och som enda officiella språk på Åland.'
    elif lang == 'tam':
        assert text == 'தமிழ் மொழி (Tamil language) தமிழர்களினதும், தமிழ் பேசும் பலரதும் தாய்மொழி ஆகும்.'
    elif lang == 'tel':
        assert text == 'ఆంధ్ర ప్రదేశ్, తెలంగాణ రాష్ట్రాల అధికార భాష తెలుగు.'
    elif lang == 'tdt':
        assert text == "Tetun (iha portugés: tétum; iha inglés: Tetum) ne 'e lian nasionál no ko-ofisiál Timór Lorosa' e nian."
    elif lang == 'tha':
        assert text == 'ภาษาไทยหรือภาษาไทยกลางเป็นภาษาราชการและภาษาประจำชาติของประเทศไทย'
    elif lang == 'bod':
        assert text == 'བོད་ཀྱི་སྐད་ཡིག་ནི་བོད་ཡུལ་དང་དེའི་ཉེ་འཁོར་གྱི་ས་ཁུལ་ཏེ།'
    else:
        raise Exception(f'Warning: language code "{lang}" is absent from the list!')

if __name__ == '__main__':
    for lang, word_detokenizer in test_word_detokenizers:
        test_word_detokenize(lang, word_detokenizer, show_results = True)
