# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Lemmatization
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

import pytest

from tests import wl_test_init, wl_test_lang_examples
from wordless.wl_nlp import wl_lemmatization, wl_word_tokenization

main = wl_test_init.Wl_Test_Main()
wl_test_init.change_default_tokenizers(main)

test_lemmatizers = []

for lang, lemmatizers in main.settings_global['lemmatizers'].items():
    for lemmatizer in lemmatizers:
        if (
            lemmatizer not in [
                'spacy_cat', 'spacy_zho', 'spacy_hrv', 'spacy_dan', 'spacy_nld',
                'spacy_eng', 'spacy_fin', 'spacy_fra', 'spacy_deu', 'spacy_ell',
                'spacy_ita', 'spacy_jpn', 'spacy_kor', 'spacy_lit', 'spacy_mkd',
                'spacy_nob', 'spacy_pol', 'spacy_por', 'spacy_ron', 'spacy_rus',
                'spacy_slv', 'spacy_spa', 'spacy_swe', 'spacy_ukr'
            ]
            and not lemmatizer.startswith('stanza_')
        ):
            test_lemmatizers.append((lang, lemmatizer))

@pytest.mark.parametrize('lang, lemmatizer', test_lemmatizers)
def test_lemmatize(lang, lemmatizer):
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

    print(f'{lang} / {lemmatizer}:')
    print(f'{lemmas}\n')

    # Check for empty lemmas
    assert lemmas
    assert lemmas_tokenized
    assert all(lemmas)
    assert all(lemmas_tokenized)

    # Tokenization should not be modified
    assert len(tokens) == len(lemmas_tokenized)

    # Tagged texts
    main.settings_custom['files']['tags']['body_tag_settings'] = [['Embedded', 'Part of speech', '_*', 'N/A']]

    lemmas_tokenized_tagged = wl_lemmatization.wl_lemmatize(
        main,
        inputs = [token + '_TEST' for token in tokens],
        lang = lang,
        lemmatizer = lemmatizer,
        tagged = True
    )

    assert lemmas_tokenized_tagged == [lemma + '_TEST' for lemma in lemmas_tokenized]

    # Long texts
    lemmas_tokenized_long = wl_lemmatization.wl_lemmatize(
        main,
        inputs = [str(i) for i in range(101) for j in range(10)],
        lang = lang,
        lemmatizer = lemmatizer
    )

    assert lemmas_tokenized_long == [str(i) for i in range(101) for j in range(10)]

    tests_lang_util_skipped = False

    if lang == 'sqi':
        assert lemmas == ['gjuhë', 'shqip', '(', 'ose', 'thjesht', 'shqipe', ')', 'jam', 'gjuhë', 'jap', 'degë', 'ai', 'veçantë', 'ai', 'familje', 'indo-evropiane', 'që', 'flitet', 'nga', 'rreth', '7-10', 'milionë', 'njeri', 'në', 'botë', ',', '[', '1', ']', 'kryesisht', 'në', 'Shqipëri', ',', 'Kosovë', 'jap', 'Maqedoninë', 'ai', 'veri', ',', 'por', 'edhe', 'në', 'zonë', 'ti', 'tjera', 'ti', 'Evropës', 'Juglindore', 'ku', 'kam', 'një', 'popullsi', 'shqiptar', ',', 'duk', 'përfshij', 'mal', 'ai', 'Zi', 'jap', 'luginë', 'ai', 'Preshevës', '.']
    elif lang == 'hye':
        assert lemmas == ['հայոց', 'լեզվով', 'ստեղծվել', 'է', 'մեծ', 'գրականություն։', 'գրաբար', 'է', 'ավանդված', 'հայ', 'հին', 'պատմագրությունը', ',', 'գիտափիլիսոփայական', ',', 'մաթեմատիկական', ',', 'բժշկագիտական', ',', 'աստվածաբանական-դավանաբանական', 'գրականությունը։']
    elif lang == 'ast':
        assert lemmas == ["L'asturianu", 'ser', 'un', 'llingua', 'romance', 'propiu', "d'Asturies", ',', '[', '1', ']', 'perteneciente', 'al', 'subgrupu', 'asturllionés', '.']
    elif lang == 'ben':
        assert lemmas == ['বাংলা', 'ভাষা', '(', 'বাঙলা', ',', 'বাঙ্গলা', ',', 'তথা', 'বাঙ্গালা', 'নামেও', 'পরিচিত', ')', 'একটি', 'ইন্দো', '-', 'আর্য', 'ভাষা', ',', 'যা', 'দক্ষিণ', 'এশিয়ার', 'বাঙালি', 'জাতির', 'প্রধান', 'কথ্য', 'ও', 'লেখ্য', 'ভাষা', '।']
    elif lang == 'bul':
        assert lemmas == ['бъ̀лгарският', 'езѝк', 'съм', 'индоевропейски', 'език', 'от', 'група', 'на', 'южнославянскит', 'език', ',', 'като', 'образувам', 'негова', 'източен', 'подгрупа', '.']
    elif lang == 'cat':
        assert lemmas == ['ell', 'català', '(', 'denominació', 'oficial', 'a', 'Catalunya', ',', 'a', 'el', 'illa', 'balear', ',', 'a', 'Andorra', ',', 'a', 'el', 'ciutat', 'de', "l'Alguer", 'i', 'tradicional', 'a', 'Catalunya', 'del', 'nord', ')', 'o', 'valencià', '(', 'denominació', 'oficial', 'al', 'pair', 'valencià', 'i', 'tradicional', 'al', 'Carxe', ')', 'ser', 'un', 'llengua', 'romànic', 'parlar', 'a', 'Catalunya', ',', 'ell', 'pair', 'valencià', '(', 'treure', "d'algunes", 'comarca', 'i', 'localitat', 'de', "l'interior", ')', ',', 'el', 'illa', 'balear', '(', 'on', 'també', 'rebre', 'ell', 'nòmer', 'de', 'mallorquí', ',', 'menorquí', ',', 'eivissenc', 'o', 'formenterer', 'segon', "l'illa", ')', ',', 'Andorra', ',', 'el', 'franjar', 'de', 'pondre', '(', 'a', "l'Aragó", ')', ',', 'el', 'ciutat', 'de', "l'Alguer", '(', 'a', "l'illa", 'de', 'Sardenya', ')', ',', 'el', 'Catalunya', 'del', 'nord', ',', '[', '8', ']', 'ell', 'Carxe', '(', 'un', 'petit', 'territori', 'de', 'Múrcia', 'habitar', 'per', 'poblador', 'valencià', ')', ',', '[', '9', ']', '[', '10', ']', 'i', 'en', 'comunitat', 'arreu', 'del', 'món', '(', 'entrar', 'el', 'qual', 'destacar', 'el', 'de', "l'Argentina", ',', 'amb', '200.000', 'parlant', ')', '.', '[', '11', ']']
    elif lang == 'hrv':
        assert lemmas == ['hrvatski', 'jezik', '(', 'ISO', '639-3', ':', 'hrv', ')', 'skupni', 'ju', 'naziv', 'за', 'nacionalni', 'standardni', 'jezik', 'Hrvat', ',', 'ti', 'за', 'skup', 'narječje', 'i', 'govora', 'kojima', 'govoriti', 'ili', 'biti', 'nekada', 'govoriti', 'Hrvat', '.']
    elif lang == 'ces':
        if lemmatizer == 'simplemma_ces':
            assert lemmas == ['čeština', 'neboli', 'český', 'jazyk', 'být', 'západoslovanský', 'jazyk', ',', 'nejbližší', 'slovenština', ',', 'poté', 'lužické', 'srbštině', 'a', 'polština', '.']
        elif lemmatizer == 'spacy_ces':
            assert lemmas == ['Čeština', 'neboli', 'český', 'jazyk', 'on', 'západoslovanský', 'jazyk', ',', 'blízký', 'slovenštině', ',', 'poté', 'lužické', 'srbštině', 'a', 'polštině', '.']
        else:
            tests_lang_util_skipped = True
    elif lang == 'dan':
        assert lemmas == ['dansk', 'være', 'en', 'østnordisk', 'sprog', 'indenfor', 'den', 'germansk', 'gren', 'af', 'den', 'indoeuropæiske', 'sprogfamilie', '.']
    elif lang == 'nld':
        assert lemmas == ['het', 'Nederlands', 'zijn', 'een', 'west-germaans', 'talen', ',', 'de', 'veel', 'gebruiken', 'talen', 'in', 'Nederland', 'en', 'België', ',', 'de', 'officieel', 'talen', 'van', 'Suriname', 'en', 'een', 'van', 'de', 'drie', 'officieel', 'tale', 'van', 'België', '.']
    elif lang == 'enm':
        assert lemmas == ['Forrþrihht', 'anan', 'see', 'timen', 'comm', 'þatt', 'eure', 'Drihhtin', 'wollde', 'been', 'borenn', 'in', 'þiss', 'middellærd', 'forr', 'all', 'mannkinne', 'neden', 'hem', 'chæs', 'him', 'sonne', 'kinnessmenn', 'all', 'swillke', 'summ', 'hem', 'wollde', 'and', 'whær', 'hem', 'wollde', 'borenn', 'been', 'hem', 'chæs', 'all', 'att', 'his', 'willen', '.']
    elif lang.startswith('eng_'):
        if lemmatizer == 'nltk_wordnet':
            assert lemmas == ['English', 'be', 'a', 'West', 'Germanic', 'language', 'in', 'the', 'Indo-European', 'language', 'family', 'that', 'originate', 'in', 'early', 'medieval', 'England.', '[', '3', ']', '[', '4', ']', '[', '5', ']']
        elif lemmatizer == 'simplemma_eng':
            assert lemmas == ['English', 'be', 'a', 'west', 'germanic', 'language', 'in', 'the', 'Indo-European', 'language', 'family', 'that', 'originate', 'in', 'early', 'medieval', 'England.', '[', '3', ']', '[', '4', ']', '[', '5', ']']
        else:
            tests_lang_util_skipped = True
    elif lang == 'est':
        assert lemmas == ['Eesti', 'keel', 'olema', 'kaks', 'suurem', 'murd', '(', 'põhi', 'ja', 'lõuna', ')', ',', 'mõni', 'käsitlus', 'eristama', 'ka', 'kirderannik', 'murre', 'eraldi', 'murderühmana', '.']
    elif lang == 'fin':
        assert lemmas == ['Suomi', 'kieli', 'eli', 'suomi', 'olla', 'uralilainen', 'kieli', 'itämerensuomalainen', 'ryhmä', 'kuuluva', 'kieli', ',', 'jota', 'puhua', 'pääosa', 'Suomalainen', '.']
    elif lang == 'fra':
        assert lemmas == ['le', 'français', 'être', 'un', 'langue', 'indo-européen', 'de', 'le', 'famille', 'un', 'langue', 'roman', 'dont', 'le', 'locuteurs', 'être', 'appelé', 'francophone', '.']
    elif lang == 'glg':
        assert lemmas == ['O', 'galego', '(', '[', 'ɡaˈleɣo̝', ']', '[', '1', ']', ')', 'ser', 'un', 'lingua', 'indoeuropeo', 'que', 'pertencer', 'á', 'póla', 'de', 'lingua', 'románico', '.']
    elif lang == 'kat':
        assert lemmas == ['ქართული', 'ენა', '—', 'იბერიულ-კავკასიურ', 'ენათა', 'ოჯახის', 'ქართველურ', 'ენათა', 'ჯგუფი', 'ენა', '.']
    elif lang.startswith('deu_'):
        assert lemmas == ['der', 'Deutscher', 'sein', 'ein', 'plurizentrische', 'Sprache', ',', 'enthalten', 'also', 'mehrere', 'Standardvarietät', 'in', 'verschieden', 'Region', '.']
    elif lang == 'grc':
        assert lemmas == ['ἔρχομαι', 'δέ', 'ὁ', 'δύο', 'ἄγγελος', 'εἰς', 'Σόδομα', 'ἑσπέρα', '·', 'Λὼτ', 'δέ', 'κάθημαι', 'παρά', 'ὁ', 'πύλη', 'Σοδόμων', '.', 'εἶδον', 'δέ', 'Λὼτ', 'ἐξανίστημι', 'εἰς', 'συνάντησιν', 'αὐτός', 'καί', 'προσκυνέω', 'ὁ', 'πρόσωπον', 'ἐπί', 'ὁ', 'γῆ']
    elif lang == 'ell':
        assert lemmas == ['ο', 'ελληνικός', 'γλώσσα', 'ανήκω', 'στην', 'ινδοευρωπαϊκή', 'οικογένεια', '[', '9', ']', 'και', 'αποτελώ', 'ο', 'μοναδικός', 'μέλος', 'ο', 'ελληνικός', 'κλάδος', ',', 'ενώ', 'είμαι', 'ο', 'επίσημος', 'γλώσσα', 'ο', 'Ελλάδα', 'και', 'ο', 'Κύπρος', '.']
    elif lang == 'hin':
        assert lemmas == ['हिंदी', 'जिसके', 'मानकीकृत', 'रूप', 'को', 'मानक', 'हिंदी', 'कहना', 'जाना', 'होना', ',', 'विश्व', 'का', 'एक', 'प्रमुख', 'भाषा', 'होना', 'और', 'भारत', 'का', 'एक', 'राजभाषा', 'है।']
    elif lang == 'hun':
        if lemmatizer == 'simplemma_hun':
            assert lemmas == ['a', 'magyar', 'nyelv', 'az', 'uráli', 'nyelvcsalád', 'tag', ',', 'a', 'finnugor', 'nyelve', 'köz', 'tartozik', 'ugor', 'nyelve', 'egyik', '.']
        elif lemmatizer == 'spacy_hun':
            assert lemmas == ['A', 'magyar', 'nyelv', 'az', 'uráli', 'nyelvcsalád', 'tag', ',', 'a', 'finnugor', 'nyelv', 'köz', 'tartozó', 'ugor', 'nyelv', 'egyik', '.']
        else:
            tests_lang_util_skipped = True
    elif lang == 'isl':
        assert lemmas == ['íslenskur', 'vera', 'vesturnorrænt', ',', 'germanskur', 'og', 'indóevrópskur', 'tungumál', 'semja', 'vera', 'einkum', 'tala', 'og', 'rita', 'ær', 'Ísland', 'og', 'vera', 'móðurmál', 'langflestra', 'Íslendinga.', '[', '5', ']']
    elif lang == 'ind':
        if lemmatizer == 'simplemma_ind':
            assert lemmas == ['bahasa', 'Indonesia', 'adalah', 'bahasa', 'nasional', 'dan', 'resmi', 'di', 'seluruh', 'wilayah', 'Indonesia', '.']
        elif lemmatizer == 'spacy_ind':
            assert lemmas == ['Bahasa', 'Indonesia', 'adalah', 'bahasa', 'nasional', 'dan', 'resmi', 'di', 'seluruh', 'wilayah', 'Indonesia', '.']
        else:
            tests_lang_util_skipped = True
    elif lang == 'gle':
        if lemmatizer == 'simplemma_gle':
            assert lemmas == ['Is', 'ceann', 'de', 'na', 'teangach', 'ceilteach', 'í', 'an', 'gaeilge', '(', 'nó', 'Gaeilge', 'na', 'hÉireann', 'mar', 'a', 'tabhair', 'ar', 'corruair', ')', ',', 'agus', 'ceann', 'de', 'na', 'trí', 'ceann', 'de', 'teangach', 'ceilteach', 'ar', 'a', 'tabhair', 'na', 'teangach', 'gaelach', '(', 'Gaeilge', ',', 'Gaeilge', 'manainn', 'agus', 'Gaeilge', 'na', 'hAlban', ')', 'go', 'áirithe', '.']
        elif lemmatizer == 'spacy_gle':
            assert lemmas == ['is', 'ceann', 'de', 'na', 'teangacha', 'ceilteacha', 'í', 'an', 'ghaeilge', '(', 'nó', 'gaeilge', 'na', 'héireann', 'mar', 'a', 'thugtar', 'uirthi', 'corruair', ')', ',', 'agus', 'ceann', 'de', 'na', 'trí', 'cinn', 'de', 'theangacha', 'ceilteacha', 'ar', 'a', 'dtugtar', 'na', 'teangacha', 'gaelacha', '(', 'gaeilge', ',', 'gaeilge', 'mhanann', 'agus', 'gaeilge', 'na', 'halban', ')', 'go', 'háirithe', '.']
        else:
            tests_lang_util_skipped = True
    elif lang == 'ita':
        assert lemmas == ["L'italiano", '(', '[', 'itaˈljaːno', ']', '[', 'nota', '1', ']', 'ascoltare', '[', '?', '·info', ']', ')', 'essere', 'uno', 'lingua', 'romanza', 'parlato', 'principalmente', 'in', 'Italia', '.']
    elif lang == 'jpn':
        assert lemmas == ['日本語', '(', 'にほん', 'ご', '、', 'にっぽん', 'ご', '[', '注釈', '2', ']', '、', '英語', ':', 'Japanese', 'language', ')', 'は', '、', '日本', '国', '内', 'や', '、', 'かつて', 'の', '日本', '領', 'だ', 'た', '国', '、', 'そして', '国外', '移民', 'や', '移住者', 'を', '含む', '日本人', '同士', 'の', '間', 'で', '使用', 'する', 'れる', 'て', 'いる', '言語', '。']
    elif lang == 'kor':
        assert lemmas == ['한국어', '(', '韓國語', ')', '는', '대한민+국과', '조선민주주의인민공화국+의', '공용어이다', '.']
    elif lang == 'lat':
        assert lemmas == ['lingua', 'Latinus', ',', '[', '1', ']', 'sive', 'sermo', 'Latinus', ',', '[', '2', ']', 'sum', 'lingua', 'indoeuropaeus', 'qui', 'primus', 'Latinus', 'universus', 'et', 'Romanus', 'antiquus', 'in', 'primus', 'loquor', 'quamobrem', 'interdum', 'etiam', 'lingua', 'Latius', '[', '3', ']', '(', 'in', 'Latium', 'enim', 'suetus', ')', 'et', 'lingua', 'Romanus', '[', '4', ']', '(', 'nam', 'imperium', 'Romanus', 'sermo', 'sollemne', ')', 'appello', '.']
    elif lang == 'lav':
        assert lemmas == ['latviete', 'valoda', 'būt', 'dzimta', 'valoda', 'apmērs', '1,5', 'miljons', 'cilvēks', ',', 'galvenokārt', 'Latvija', ',', 'kur', 'tā', 'būt', 'vienīgs', 'valsts', 'valoda.', '[', '1', ']', '[', '3', ']']
    elif lang == 'lit':
        assert lemmas == ['lietuvė', 'kalba', '–', 'ižti', 'baltas', 'prokalbė', 'kilęs', 'lietuvė', 'tauta', 'kalba', ',', 'kurti', 'Lietuva', 'irti', 'valstybinis', ',', 'o', 'Europa', 'sąjunga', '–', 'Viena', 'ižti', 'oficialus', 'kalbus', '.']
    elif lang == 'ltz':
        if lemmatizer == 'simplemma_ltz':
            assert lemmas == ["D'Lëtzebuergesch", 'ginn', 'an', 'der', 'däitsch', 'Dialektologie', 'als', 'een', 'westgermanesch', ',', 'mëtteldäitsch', 'Dialekt', 'aklasséiert', ',', 'deen', 'zum', 'muselfränkesch', 'gehéiert', '.']
        elif lemmatizer == 'spacy_ltz':
            assert lemmas == ["D'", 'Lëtzebuergesch', 'ginn', 'an', 'der', 'däitsch', 'Dialektologie', 'als', 'een', 'westgermanesch', ',', 'mëtteldäitsch', 'Dialekt', 'aklasséieren', ',', 'deen', 'zum', 'Muselfränkesche', 'gehéieren', '.']
        else:
            tests_lang_util_skipped = True
    elif lang == 'mkd':
        assert lemmas == ['македонски', 'јазик', '—', 'јужнословенски', 'јазик', ',', 'дел', 'од', 'група', 'на', 'словенски', 'јазик', 'од', 'јазичното', 'семејство', 'на', 'индоевропски', 'јазик', '.']
    elif lang == 'msa':
        assert lemmas == ['bahasa', 'Melayu', '(', 'tulisan', 'Jawi', ':', 'bahasa', 'Melayu', ';', 'rencong', ':', 'ꤷꥁꤼ', 'ꤸꥍꤾꤿꥈ', ')', 'ialah', 'salah', 'ساتو', 'daripada', 'bahasa', 'Melayu-Polinesia', 'di', 'bawah', 'keluarga', 'bahasa', 'Austronesia', ',', 'hiang', 'merupakan', 'bahasa', 'rasmi', 'di', 'Brunei', ',', 'Indonesia', ',', 'Malaysia', 'دان', 'Singapura', ',', 'serta', 'dituturkan', 'di', 'timur', 'Leste', 'دان', 'sebahagian', 'wilayah', 'di', 'Kemboja', ',', 'Filipina', 'دان', 'Thailand', '.']
    elif lang == 'glv':
        assert lemmas == ['She', 'Gaelg', '(', 'graït', ':', '/gɪlg/', ')', 'çhengey', 'Gaelagh', 'Mannin', '.']
    elif lang == 'nob':
        assert lemmas == ['bokmål', 'være', 'enn', 'varietet', 'av', 'norsk', 'skriftspråk', '.']
    elif lang == 'nno':
        assert lemmas == ['nynorsk', ',', 'føra', '1929', 'offisiell', 'kall', 'landsmål', ',', 'vera', 'sidan', 'jamstillingsvedtaket', 'av', '12', '.', 'mai', '1885', 'ein', 'av', 'den', 'to', 'offisiell', 'målformene', 'av', 'norsk', ';', 'den', 'annan', 'forme', 'vera', 'bokmål', '.']
    elif lang == 'fas':
        if lemmatizer == 'simplemma_fas':
            assert lemmas == ['فارسی', 'یا', 'پارسی', 'یک', 'زبان', 'ایرانی', 'غربی', 'از', 'زیرگروه', 'ایرانی', 'شاخهٔ', 'هندوایرانیِ', 'خانوادهٔ', 'زبان\u200cهای', 'هندواروپایی', 'است', 'که', 'در', 'کشورهای', 'ایران،', 'افغانستان،', 'تاجیکستان،', 'ازبکستان،', 'پاکستان،', 'عراق،', 'ترکمنستان', 'را', 'آذربایجان', 'به', 'آن', 'سخن', 'می\u200cگویند', '.']
        elif lemmatizer == 'spacy_fas':
            assert lemmas == ['فارسی', 'یا', 'پارسی', 'یک', 'زبان', 'ایرانی', 'غربی', 'از', 'زیرگروه', 'ایرانی', 'شاخهٔ', 'هندوایرانیِ', 'خانوادهٔ', 'زبان\u200cهای', 'هندواروپایی', 'است', 'که', 'در', 'کشورهای', 'ایران', '،', 'افغانستان', '،', 'تاجیکستان', '،', 'ازبکستان', '،', 'پاکستان', '،', 'عراق', '،', 'ترکمنستان', 'و', 'آذربایجان', 'به', 'آن', 'سخن', 'می\u200cگویند', '.']
        else:
            tests_lang_util_skipped = True
    elif lang == 'pol':
        assert lemmas == ['język', 'polski', ',', 'polszczyzna', '–', 'język', 'z', 'grupa', 'zachodniosłowiański', '(', 'do', 'który', 'należeć', 'również', 'czeski', ',', 'kaszubski', ',', 'słowacki', 'i', 'język', 'łużycki', ')', ',', 'stanowić', 'część', 'rodzina', 'indoeuropejski', '.']
    elif lang.startswith('por_'):
        assert lemmas == ['o', 'língua', 'portuguesar', ',', 'também', 'designado', 'português', ',', 'ser', 'umar', 'língua', 'indo-europeu', 'românico', 'flexivo', 'ocidental', 'originado', 'o', 'galego-português', 'falar', 'o', 'reino', 'da', 'galiza', 'e', 'o', 'norte', 'de', 'portugal', '.']
    elif lang == 'ron':
        assert lemmas == ['limbă', 'român', 'fi', 'el', 'limbă', 'indo-european', 'din', 'grup', 'italic', 'și', 'din', 'subgrupul', 'oriental', 'al', 'limbă', 'romanice', '.']
    elif lang == 'rus':
        if lemmatizer == 'simplemma_rus':
            assert lemmas == ['Ру́сский', 'язы́к', '(', '[', 'ˈruskʲɪi̯', 'jɪˈzɨk', ']', 'информация', 'о', 'файл', 'слушать', ')', '[', '~', '3', ']', '[', '⇨', ']', '—', 'язык', 'восточнославянский', 'группа', 'славянский', 'ветвь', 'индоевропейский', 'языковый', 'семья', ',', 'национальный', 'язык', 'русский', 'народ', '.']
        elif lemmatizer == 'pymorphy3_morphological_analyzer':
            assert lemmas == ['ру́сский', 'язы́к', '(', '[', 'ˈruskʲɪi̯', 'jɪˈzɨk', ']', 'информация', 'о', 'файл', 'слушать', ')', '[', '~', '3', ']', '[', '⇨', ']', '—', 'язык', 'восточнославянский', 'группа', 'славянский', 'ветвь', 'индоевропейский', 'языковой', 'семья', ',', 'национальный', 'язык', 'русский', 'народ', '.']
        else:
            tests_lang_util_skipped = True
    elif lang == 'sme':
        assert lemmas == ['davvisámegiella', 'gullát', 'sámegiella', 'oarjesámegielaid', 'davvejovkui', 'ovttastit', 'julev-', 'ja', 'bihtánsámegielain', '.']
    elif lang == 'gla':
        assert lemmas == ["'S", 'i', 'cànan', 'dùthchasach', 'na', 'h-alba', 'a', 'th', "'", 'anns', 'a', "'", 'gàidhlig', '.']
    elif lang == 'srp_cyrl':
        assert lemmas == ['Српски', 'језик', 'бити', 'званичан', 'у', 'Србији', ',', 'Босни', 'и', 'Херцеговини', 'и', 'Црној', 'Гори', 'и', 'говорити', 'он', 'око', '12', 'милион', 'људи.[13', ']']
    elif lang == 'srp_latn':
        assert lemmas == ['srpski', 'jezik', 'ju', 'zvaničan', 'u', 'Srbija', ',', 'Bosna', 'i', 'Hercegovina', 'i', 'crn', 'gora', 'i', 'govoriti', 'ih', 'oko', '12', 'milion', 'ljudi.', '[', '13', ']']
    elif lang == 'slk':
        assert lemmas == ['slovenčina', 'byť', 'oficiálne', 'úradný', 'jazyk', 'Slovensko', ',', 'vojvodiny', 'a', 'od', '1', '.', 'máj', '2004', 'jeden', 'z', 'jazyk', 'európsky', 'únia', '.']
    elif lang == 'slv':
        assert lemmas == ['slovenščina', '[', 'sloˈʋenʃtʃina', ']', 'on', 'združen', 'naziv', 'za', 'uraden', 'knjižen', 'jezik', 'Slovenec', 'in', 'skupen', 'ime', 'za', 'narečje', 'in', 'govor', ',', 'ki', 'on', 'govoriti', 'ali', 'biti', 'on', 'nekoč', 'govorilo', 'Slovenec', '.']
    elif lang == 'spa':
        assert lemmas == ['el', 'español', 'o', 'castellano', 'ser', 'uno', 'lengua', 'romance', 'procedente', 'del', 'latín', 'hablar', ',', 'perteneciente', 'a', 'el', 'familia', 'de', 'lengua', 'indoeuropeo', '.']
    elif lang == 'swa':
        assert lemmas == ['Kiswahili', 'ni', 'lugha', 'ya', 'Kibantu', 'enye', 'msamiati', 'ingi', 'ya', 'Kiarabu', '(', '35', '%', '[', '1', ']', ')', ',', 'laki', 'sasa', 'ya', 'Kiingereza', 'pia', '(', '10', '%', ')', ',', 'inayozungumzwa', 'katika', 'eneo', 'kubwa', 'la', 'Afrika', 'ya', 'mashariki', '.']
    elif lang == 'swe':
        assert lemmas == ['svensk', '(', 'svensk', '(', 'info', ')', ')', 'ära', 'en', 'östnordiskt', 'språka', 'som', 'tala', 'av', 'ungefär', 'tio', 'miljon', 'person', 'främst', 'i', 'Sverige', 'där', 'språk', 'ha', 'man', 'dominant', 'ställning', 'som', 'huvudspråk', ',', 'mena', 'även', 'som', 'den', 'en', 'nationalspråk', 'i', 'Finland', 'och', 'som', 'enda', 'officiell', 'språka', 'på', 'Åland', '.']
    elif lang == 'tgl':
        if lemmatizer == 'simplemma_tgl':
            assert lemmas == ['Ang', 'wikang', 'Tagalog', '[', '1', ']', '(', 'Baybayin', ':', 'ᜏᜒᜃᜆᜄᜎᜓ', ')', ',', 'o', 'ang', 'Tagalog', ',', 'ay', 'isa', 'sa', 'mga', 'pinakaginagamit', 'na', 'wikain', 'ng', 'Pilipinas', '.']
        elif lemmatizer == 'spacy_tgl':
            assert lemmas == ['Ang', 'wikang', 'Tagalog[1', ']', '(', 'Baybayin', ':', 'ᜏᜒᜃᜆᜄᜎᜓ', ')', ',', 'o', 'ang', 'Tagalog', ',', 'ay', 'isa', 'sa', 'mga', 'pinakaginagamit', 'na', 'wika', 'ng', 'Pilipinas', '.']
        else:
            tests_lang_util_skipped = True
    elif lang == 'bod':
        assert lemmas == ['བོད་', 'གི་', 'སྐད་ཡིག་', 'ནི་', 'བོད་ཡུལ་', 'དང་', 'ཉེ་འཁོར་', 'གི་', 'ས་ཁུལ་', 'བལ་ཡུལ་', '།', 'འབྲུག་', 'དང་', 'འབྲས་ལྗོངས་', '།']
    elif lang == 'tur':
        if lemmatizer == 'simplemma_tur':
            assert lemmas == ['türkçe', 'ya', 'da', 'Türk', 'dil', ',', 'güneydoğu', 'avrupa', 've', 'batı', 'asya', 'konuş', ',', 'Türk', 'dil', 'dil', 'aile', 'ait', 'son', 'ekle', 'bir', 'dil.', '[', '12', ']']
        elif lemmatizer == 'spacy_tur':
            assert lemmas == ['Türkçe', 'ya', 'da', 'Türk', 'dil', ',', 'Güneydoğu', 'Avrupa', 've', 'Batı', "Asya'da", 'konuş', ',', 'Türk', 'dil', 'dil', 'aile', 'ait', 'son', 'ekle', 'bir', 'dil.[12', ']']
        else:
            tests_lang_util_skipped = True
    elif lang == 'ukr':
        if lemmatizer == 'pymorphy3_morphological_analyzer':
            assert lemmas == ['украї́нський', 'мо́вий', '(', 'мфа', ':', '[', 'ukrɑ̽ˈjɪnʲsʲkɑ̽', 'ˈmɔwɑ̽', ']', ',', 'історичний', 'назва', '—', 'ру́ський', '[', '10', ']', '[', '11', ']', '[', '12', ']', '[', '*', '1', ']', ')', '—', 'національний', 'мова', 'українець', '.']
        elif lemmatizer == 'simplemma_ukr':
            assert lemmas == ['Українськ', 'мо́ва', '(', 'мфа', ':', '[', 'ukrɑ̽ˈjɪnʲsʲkɑ̽', 'ˈmɔwɑ̽', ']', ',', 'історичний', 'назва', '—', 'руський', '[', '10', ']', '[', '11', ']', '[', '12', ']', '[', '*', '1', ']', ')', '—', 'національний', 'мова', 'українець', '.']
        else:
            tests_lang_util_skipped = True
    elif lang == 'urd':
        assert lemmas == ['اُردُو[8', ']', 'برصغیر', 'کم', 'معیاری', 'زبان', 'میں', 'سے', 'ایک', 'ہونا', '۔']
    elif lang == 'cym':
        assert lemmas == ['yn', 'cyfrifiad', 'yr', 'tu', '(', '2011', ')', ',', 'darganfod', 'bodio', '19', '%', '(', '562,000', ')', 'prpers', 'preswylwr', 'cymru', '(', 'tair', 'blwydd', 'a', 'trosodd', ')', 'bod', 'gallu', 'siarad', 'cymraeg', '.']
    else:
        raise wl_test_init.Wl_Exception_Tests_Lang_Skipped(lang)

    if tests_lang_util_skipped:
        raise wl_test_init.Wl_Exception_Tests_Lang_Util_Skipped(lemmatizer)

if __name__ == '__main__':
    for lang, lemmatizer in test_lemmatizers:
        test_lemmatize(lang, lemmatizer)
