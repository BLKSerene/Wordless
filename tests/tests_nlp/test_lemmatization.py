# ----------------------------------------------------------------------
# Tests: NLP - Lemmatization
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

import pytest

from tests import wl_test_init, wl_test_lang_examples
from wordless.wl_nlp import wl_lemmatization, wl_texts, wl_word_tokenization
from wordless.wl_utils import wl_misc

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')
is_linux = wl_misc.check_os()[2]

test_lemmatizers = []
test_lemmatizers_local = []

for lang, lemmatizers in main.settings_global['lemmatizers'].items():
    for lemmatizer in lemmatizers:
        if lemmatizer in ('botok_xct', 'modern_botok_bod'):
            test_lemmatizers.append(pytest.param(
                lang, lemmatizer,
                marks = pytest.mark.xfail(
                    is_linux,
                    reason = 'Different results on AppVeyor, Azure Pipelines, and GitHub Actions'
                )
            ))

            test_lemmatizers_local.append((lang, lemmatizer))
        elif (
            lemmatizer not in (
                'spacy_cat', 'spacy_zho', 'spacy_hrv', 'spacy_dan', 'spacy_nld',
                'spacy_eng', 'spacy_fin', 'spacy_fra', 'spacy_deu', 'spacy_ell',
                'spacy_ita', 'spacy_jpn', 'spacy_kor', 'spacy_lit', 'spacy_mkd',
                'spacy_nob', 'spacy_pol', 'spacy_por', 'spacy_ron', 'spacy_rus',
                'spacy_slv', 'spacy_spa', 'spacy_swe', 'spacy_ukr'
            )
            and not lemmatizer.startswith('stanza_')
        ):
            test_lemmatizers.append((lang, lemmatizer))
            test_lemmatizers_local.append((lang, lemmatizer))

@pytest.mark.parametrize('lang, lemmatizer', test_lemmatizers)
def test_lemmatize(lang, lemmatizer):
    tests_lang_util_skipped = False
    test_sentence = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}')

    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = test_sentence,
        lang = lang
    )

    match lang:
        case 'sqi':
            results = ['Keto', 'gjuhë', 'kryesisht', 'perdoret', 'në', 'Shqipëri', ',', 'Kosovë', 'jap', 'Maqedoninë', 'ai', 'veri', ',', 'por', 'edhe', 'në', 'zonë', 'ti', 'tjera', 'ti', 'Evropës', 'Juglindore', 'ku', 'kam', 'një', 'popullsi', 'shqiptar', ',', 'duk', 'përfshij', 'mal', 'ai', 'Zi', 'jap', 'luginë', 'ai', 'Preshevës', '.']
        case 'hye' | 'hyw':
            results = ['հայերեն', '(', 'ավանդական՝', 'հայերէն', ')', ',', 'հնդեվրոպական', 'լեզվաընտանիք', 'առանձին', 'ճյուղ', 'հանդիսացող', 'լեզու։']
        case 'ast':
            results = ["L'asturianu", 'ser', 'un', 'llingua', 'romance', 'propiu', "d'Asturies", ',', '[', '1', ']', 'perteneciente', 'al', 'subgrupu', 'asturllionés', '.']
        case 'ben':
            results = ['বাংলা', 'ভাষা', '(', 'বাঙলা', ',', 'বাঙ্গলা', ',', 'তথা', 'বাঙ্গালা', 'নামেও', 'পরিচিত', ')', 'একটি', 'ধ্রুপদী', 'ইন্দো', '-', 'আর্য', 'ভাষা', ',', 'যা', 'দক্ষিণ', 'এশিয়ার', 'বাঙালি', 'জাতির', 'প্রধান', 'কথ্য', 'ও', 'লেখ্য', 'ভাষা', '।']
        case 'bul':
            results = ['бъ̀лгарският', 'езѝк', 'съм', 'индоевропейски', 'език', 'от', 'група', 'на', 'южнославянскит', 'език', ',', 'като', 'образувам', 'негова', 'източен', 'подгрупа', '.']
        case 'cat':
            results = ['hi', 'haver', 'altre', 'glotònims', 'tradicional', 'que', 'ell', 'fer', 'servir', 'comar', 'a', 'sinònim', 'de', '``', 'català', "''", 'al', 'llarg', 'del', 'dominar', 'lingüístic', '.']
        case 'hrv':
            results = ['hrvatski', 'jezik', 'obuhvaćati', 'govoriti', 'i', 'pisati', 'hrvatski', 'standardni', 'jezik', 'i', 'svako', 'narodni', 'govoriti', 'kojima', 'govoriti', 'i', 'pisati', 'Hrvati.', '[', '4', ']']
        case 'ces':
            match lemmatizer:
                case 'simplemma_ces':
                    results = ['čeština', 'neboli', 'český', 'jazyk', 'být', 'západoslovanský', 'jazyk', ',', 'nejbližší', 'slovenština', ',', 'poté', 'lužické', 'srbštině', 'a', 'polština', '.']
                case 'spacy_ces':
                    results = ['Čeština', 'neboli', 'český', 'jazyk', 'on', 'západoslovanský', 'jazyk', ',', 'blízký', 'slovenštině', ',', 'poté', 'lužické', 'srbštině', 'a', 'polštině', '.']
                case _:
                    tests_lang_util_skipped = True
        case 'dan':
            results = ['dansk', 'være', 'en', 'østnordisk', 'sprog', 'indenfor', 'den', 'germansk', 'gren', 'af', 'den', 'indoeuropæiske', 'sprogfamilie', '.']
        case 'nld':
            results = ['het', 'Nederlands', 'zijn', 'een', 'west-germaans', 'talen', ',', 'de', 'veel', 'gebruiken', 'talen', 'in', 'Nederland', 'en', 'België', ',', 'de', 'officieel', 'talen', 'van', 'Suriname', 'en', 'een', 'van', 'de', 'drie', 'officieel', 'tale', 'van', 'België', '.']
        case 'enm':
            results = ['Forrþrihht', 'anan', 'see', 'timen', 'comm', 'þatt', 'eure', 'Drihhtin', 'wollde', 'been', 'borenn', 'in', 'þiss', 'middellærd', 'forr', 'all', 'mannkinne', 'neden', 'hem', 'chæs', 'him', 'sonne', 'kinnessmenn', 'all', 'swillke', 'summ', 'hem', 'wollde', 'and', 'whær', 'hem', 'wollde', 'borenn', 'been', 'hem', 'chæs', 'all', 'att', 'his', 'willen', '.']
        case 'eng_gb' | 'eng_us':
            match lemmatizer:
                case 'nltk_wordnet':
                    results = ['English', 'be', 'a', 'West', 'Germanic', 'language', 'in', 'the', 'Indo', '-', 'European', 'language', 'family', ',', 'whose', 'speaker', ',', 'call', 'Anglophones', ',', 'originate', 'in', 'early', 'medieval', 'England', 'on', 'the', 'island', 'of', 'Great', 'Britain.[4][5][6', ']']
                case 'simplemma_eng':
                    results = ['English', 'be', 'a', 'west', 'germanic', 'language', 'in', 'the', 'Indo-European', 'language', 'family', ',', 'whose', 'speaker', ',', 'call', 'anglophone', ',', 'originate', 'in', 'early', 'medieval', 'England', 'on', 'the', 'island', 'of', 'great', 'Britain.', '[', '4', ']', '[', '5', ']', '[', '6', ']']
                case _:
                    tests_lang_util_skipped = True
        case 'est':
            results = ['Eesti', 'keel', '(', 'varasem', 'nimetus', 'maakeel', ')', 'olema', 'läänemeresoome', 'lõuna', 'kuuluv', 'keel', '.']
        case 'fin':
            results = ['Suomi', 'kieli', 'eli', 'suomi', 'olla', 'uralilainen', 'kieli', 'itämerensuomalainen', 'ryhmä', 'kuuluva', 'kieli', ',', 'jota', 'puhua', 'pääosa', 'suomalainen', '.']
        case 'fra':
            results = ['le', 'français', 'être', 'un', 'langue', 'indo-européen', 'de', 'le', 'famille', 'un', 'langue', 'roman', 'dont', 'le', 'locuteurs', 'être', 'appelé', '«', 'francophone', '»', '.']
        case 'glg':
            results = ['O', 'galego', '(', '[', 'ɡaˈleɣo̝', ']', '[', '1', ']', ')', 'ser', 'un', 'lingua', 'indoeuropeo', 'que', 'pertencer', 'á', 'póla', 'de', 'lingua', 'románico', '.']
        case 'kat':
            results = ['ქართული', 'ენა', '—', 'ქართველურ', 'ენათა', 'ოჯახის', 'ენა', '.']
        case 'deu_at' | 'deu_de' | 'deu_ch':
            results = ['der', 'deutsch', 'Sprache', 'oder', 'deutsch', '[', 'dɔɪ̯tʃ', ']', '[', '24', ']', 'sein', 'ein', 'westgermanische', 'Sprache', ',', 'der', 'weltweit', 'etwa', '90', 'bis', '105', 'Million', 'Mensch', 'als', 'Muttersprache', 'und', 'weit', 'rund', '80', 'Million', 'als', 'Zweit-', 'oder', 'Fremdsprache', 'dienen', '.']
        case 'grc':
            results = ['ἔρχομαι', 'δέ', 'ὁ', 'δύο', 'ἄγγελος', 'εἰς', 'Σόδομα', 'ἑσπέρα', '·', 'Λὼτ', 'δέ', 'κάθημαι', 'παρά', 'ὁ', 'πύλη', 'Σοδόμων', '.', 'εἶδον', 'δέ', 'Λὼτ', 'ἐξανίστημι', 'εἰς', 'συνάντησιν', 'αὐτός', 'καί', 'προσκυνέω', 'ὁ', 'πρόσωπον', 'ἐπί', 'ὁ', 'γῆ']
        case 'ell':
            results = ['ο', 'ελληνικός', 'γλώσσα', 'ανήκω', 'στην', 'ινδοευρωπαϊκή', 'οικογένεια', '[', '9', ']', 'secεπίσος', 'στο', 'βαλκανικός', 'γλωσσικός', 'δεσμός', '.']
        case 'hin':
            results = ['हिंदी', 'या', 'आधुनिक', 'मानक', 'हिंदी', 'विश्व', 'का', 'एक', 'प्रमुख', 'भाषा', 'होना', 'और', 'भारत', 'का', 'एक', 'राजभाषा', 'है।']
        case 'hun':
            match lemmatizer:
                case 'simplemma_hun':
                    results = ['a', 'magyar', 'nyelv', 'az', 'uráli', 'nyelvcsalád', 'tag', ',', 'az', 'belül', 'a', 'finnugor', 'nyelve', 'köz', 'tartozik', 'ugor', 'nyelve', 'egyik', '.']
                case 'spacy_hun':
                    results = ['A', 'magyar', 'nyelv', 'az', 'uráli', 'nyelvcsalád', 'tag', ',', 'az', 'belül', 'a', 'finnugor', 'nyelv', 'köz', 'tartozó', 'ugor', 'nyelv', 'egyik', '.']
                case _:
                    tests_lang_util_skipped = True
        case 'isl':
            results = ['íslenskur', 'vera', 'vesturnorrænt', ',', 'germanskur', 'og', 'indóevrópskur', 'tungumál', 'semja', 'vera', 'einkum', 'tala', 'og', 'rita', 'ær', 'Ísland', 'og', 'vera', 'móðurmál', 'langflestra', 'Íslendinga.', '[', '6', ']']
        case 'ind':
            match lemmatizer:
                case 'simplemma_ind':
                    results = ['bahasa', 'Indonesia', '(', '[', 'baˈhasa', 'indoˈnesija', ']', ')', 'merupakan', 'bahasa', 'resmi', 'sekaligus', 'bahasa', 'nasional', 'di', 'Indonesia.', '[', '16', ']']
                case 'spacy_ind':
                    results = ['Bahasa', 'Indonesia', '(', '[', 'baˈhasa', 'indoˈnesija', ']', ')', 'rupa', 'bahasa', 'resmi', 'sekaligus', 'bahasa', 'nasional', 'di', 'Indonesia.[16', ']']
                case _:
                    tests_lang_util_skipped = True
        case 'gle':
            match lemmatizer:
                case 'simplemma_gle':
                    results = ['labhair', 'in', 'Éire', 'go', 'príomh', 'í', ',', 'ach', 'bí', 'cainteoir', 'Gaeilge', 'ina', 'cónaí', 'in', 'áit', 'eil', 'ar', 'fud', 'an', 'domhan', '.']
                case 'spacy_gle':
                    results = ['labhraítear', 'in', 'éirinn', 'go', 'príomha', 'í', ',', 'ach', 'tá', 'cainteoirí', 'gaeilge', 'ina', 'gcónaí', 'in', 'áiteanna', 'eile', 'ar', 'fud', 'an', 'domhain', '.']
                case _:
                    tests_lang_util_skipped = True
        case 'ita':
            results = ["L'italiano", 'essere', 'uno', 'lingua', 'romanza', 'parlato', 'principalmente', 'in', 'Italia', '.']
        case 'jpn':
            results = ['日本語', '(', 'にほん', 'ご', '、', 'にっぽん', 'ご', '[', '注釈', '3', ']', ')', 'は', '、', '日本', '国', '内', 'や', '、', 'かつて', 'の', '日本', '領', 'だ', 'た', '国', '、', 'そして', '国外', '移民', 'や', '移住者', 'を', '含む', '日本人', '同士', 'の', '間', 'で', '使用', 'する', 'れる', 'て', 'いる', '言語', '。']
        case 'lat':
            results = ['Latinum', ',', 'lingua', 'Latina', ',', '[', '1', ']', 'sive', 'sermo', 'Latinus', ',', '[', '2', ']', 'sum', 'lingua', 'indoeuropaeus', 'qui', 'primus', 'Latinus', 'universus', 'et', 'Romanus', 'antiquus', 'in', 'primus', 'loquor', 'quamobrem', 'interdum', 'etiam', 'lingua', 'Latius', '[', '3', ']', '(', 'in', 'Latium', 'enim', 'suetus', ')', 'et', 'lingua', 'romanus', '[', '4', ']', '(', 'nam', 'imperium', 'Romanus', 'sermo', 'sollemne', ')', 'appello', '.']
        case 'lav':
            results = ['latviete', 'valoda', 'būt', 'dzimta', 'valoda', 'apmērs', '1,5', 'miljons', 'cilvēks', ',', 'galvenokārt', 'Latvija', ',', 'kur', 'tā', 'būt', 'vienīgs', 'valsts', 'valoda', '(', '1', ')', '(', '3', ')']
        case 'lit':
            results = ['lietuvė', 'kalba', '–', 'ižti', 'baltas', 'prokalbė', 'kilęs', 'lietuvė', 'tauta', 'kalba', ',', 'kurti', 'Lietuva', 'irti', 'valstybinis', ',', 'o', 'Europa', 'sąjunga', '–', 'Viena', 'ižti', 'oficialus', 'kalbus', '.']
        case 'ltz':
            match lemmatizer:
                case 'simplemma_ltz':
                    results = ["D'Lëtzebuergesch", 'ginn', 'an', 'der', 'däitsch', 'Dialektologie', 'als', 'een', 'westgermanesch', ',', 'mëtteldäitsch', 'Dialekt', 'aklasséiert', ',', 'deen', 'zum', 'muselfränkesch', 'gehéiert', '.']
                case 'spacy_ltz':
                    results = ["D'", 'Lëtzebuergesch', 'ginn', 'an', 'der', 'däitsch', 'Dialektologie', 'als', 'een', 'westgermanesch', ',', 'mëtteldäitsch', 'Dialekt', 'aklasséieren', ',', 'deen', 'zum', 'Muselfränkesche', 'gehéieren', '.']
                case _:
                    tests_lang_util_skipped = True
        case 'mkd':
            results = ['македонски', 'јазик', '—', 'јужнословенски', 'јазик', ',', 'дел', 'од', 'група', 'словенски', 'јазик', 'од', 'јазичното', 'семејство', 'на', 'индоевропски', 'јазик', '.']
        case 'msa':
            results = ['jumlah', 'penutur', 'bahasa', 'اين', 'mencakupi', 'lebih', 'daripada', '290', 'جوتا', 'penutur', '[', '4', ']', '(', 'termasuk', 'sebanyak', '260', 'جوتا', 'orang', 'penutur', 'bahasa', 'Indonesia', ')', '[', '5', ']', 'merentasi', 'kawasan', 'maritim', 'Asia', 'tenggara', '.']
        case 'glv':
            results = ['She', 'Gaelg', '(', 'graït', ':', '/gɪlg/', ')', 'çhengey', 'Gaelagh', 'Mannin', '.']
        case 'nob':
            results = ['bokmål', 'være', 'enn', 'av', 'to', 'offisiell', 'målform', 'av', 'norsk', 'skriftspråk', ',', 'hvorav', 'den', 'annen', 'være', 'nynorsk', '.']
        case 'nno':
            results = ['nynorsk', ',', 'føra', '1929', 'offisiell', 'kall', 'landsmål', ',', 'vera', 'sidan', 'jamstillingsvedtaket', 'av', '12', '.', 'mai', '1885', 'ein', 'av', 'den', 'to', 'offisiell', 'målformene', 'av', 'norsk', ';', 'den', 'annan', 'forme', 'vera', 'bokmål', '.']
        case 'fas':
            match lemmatizer:
                case 'simplemma_fas':
                    results = ['فارسی', 'یا', 'پارسی', 'یکی', 'از', 'زبان\u200cهای', 'ایرانی', 'غربی', 'از', 'زیرگروه', 'ایرانی', 'شاخهٔ', 'هندوایرانیِ', 'خانوادهٔ', 'زبان\u200cهای', 'هندواروپایی', 'است', 'که', 'در', 'کشورهای', 'ایران،', 'افغانستان،', 'تاجیکستان،', 'ازبکستان،', 'پاکستان،', 'عراق،', 'ترکمنستان', 'را', 'آذربایجان', 'به', 'آن', 'سخن', 'می\u200cگویند', '.']
                case 'spacy_fas':
                    results = ['فارسی', 'یا', 'پارسی', 'یکی', 'از', 'زبان\u200cهای', 'ایرانی', 'غربی', 'از', 'زیرگروه', 'ایرانی', 'شاخهٔ', 'هندوایرانیِ', 'خانوادهٔ', 'زبان\u200cهای', 'هندواروپایی', 'است', 'که', 'در', 'کشورهای', 'ایران', '،', 'افغانستان', '،', 'تاجیکستان', '،', 'ازبکستان', '،', 'پاکستان', '،', 'عراق', '،', 'ترکمنستان', 'و', 'آذربایجان', 'به', 'آن', 'سخن', 'می\u200cگویند', '.']
                case _:
                    tests_lang_util_skipped = True
        case 'pol':
            results = ['język', 'polski', ',', 'polszczyzna', '–', 'język', 'lechicki', 'z', 'grupa', 'zachodniosłowiański', '(', 'do', 'który', 'należeć', 'również', 'czeski', ',', 'kaszubski', ',', 'słowacki', ',', 'język', 'łużycki', 'czy', 'wymarły', 'język', 'drzewiański', ')', ',', 'stanowić', 'część', 'rodzina', 'indoeuropejski', '.']
        case 'por_br' | 'por_pt':
            results = ['o', 'língua', 'portuguesar', ',', 'também', 'designado', 'português', ',', 'ser', 'umar', 'língua', 'indo-europeu', 'românico', 'flexivo', 'ocidental', 'originado', 'o', 'galego-português', 'falar', 'o', 'reino', 'da', 'galiza', 'e', 'o', 'norte', 'de', 'portugal', '.']
        case 'ron':
            results = ['limbă', 'român', '(', '[', 'ˈlimba', 'roˈmɨnə', ']', '(', 'audio', ')', 'sau', 'românește', '[', 'romɨˈneʃte', ']', ')', 'fi', 'limbă', 'oficial', 'și', 'principal', 'al', 'România', 'și', 'al', 'republică', 'Moldova', '.']
        case 'rus':
            match lemmatizer:
                case 'simplemma_rus':
                    results = ['язык', 'язык', '(', 'МФА', ':', '[', 'ˈruskʲɪɪ̯', 'ɪ̯ɪˈzɨk', ']', 'о', 'файл', ')', '[', '~', '3', ']', '—', 'язык', 'восточнославянский', 'группа', 'славянский', 'ветвь', 'индоевропейский', 'языковый', 'семья', ',', 'национальный', 'язык', 'русский', 'народ', '.']
                case 'pymorphy3_morphological_analyzer':
                    results = ['русский', 'язык', '(', 'мфа', ':', '[', 'ˈruskʲɪɪ̯', 'ɪ̯ɪˈzɨk', ']', 'о', 'файл', ')', '[', '~', '3', ']', '—', 'язык', 'восточнославянский', 'группа', 'славянский', 'ветвь', 'индоевропейский', 'языковой', 'семья', ',', 'национальный', 'язык', 'русский', 'народ', '.']
                case _:
                    tests_lang_util_skipped = True
        case 'sme':
            results = ['davvisámegiella', 'gullát', 'sámegiella', 'oarjesámegielaid', 'davvejovkui', 'ovttastit', 'julev-', 'ja', 'bihtánsámegielain', '.']
        case 'gla':
            results = ["'S", 'i', 'cànan', 'dùthchasach', 'na', 'h-alba', 'a', 'th', "'", 'anns', 'a', "'", 'gàidhlig', '.']
        case 'srp_cyrl':
            results = ['Српски', 'језик', 'припадати', 'словенски', 'група', 'језик', 'породица', 'индоевропских', 'језика.[12', ']']
        case 'srp_latn':
            results = ['srpski', 'jezik', 'pripadati', 'slovenski', 'grupa', 'jezika', 'porodica', 'indoevropski', 'jezika.', '[', '12', ']']
        case 'slk':
            results = ['slovenčina', 'patriť', 'do', 'skupina', 'západoslovanský', 'jazyk', '(', 'spolu', 's', 'čeština', ',', 'poľština', ',', 'horný', 'a', 'dolný', 'lužickou', 'srbčina', 'a', 'kašubčiný', ')', '.']
        case 'slv':
            results = ['slovenščina', '[', 'sloˈʋenʃtʃina', ']', 'on', 'združen', 'naziv', 'za', 'uraden', 'knjižen', 'jezik', 'Slovenec', 'in', 'skupen', 'ime', 'za', 'narečje', 'in', 'govor', ',', 'ki', 'on', 'govoriti', 'ali', 'biti', 'on', 'nekoč', 'govorilo', 'Slovenec', '.']
        case 'spa':
            results = ['el', 'español', 'o', 'castellano', 'ser', 'uno', 'lengua', 'romance', 'procedente', 'del', 'latín', 'hablar', ',', 'perteneciente', 'a', 'el', 'familia', 'de', 'lengua', 'indoeuropeo', '.']
        case 'swa':
            results = ['Kiswahili', '(', 'Sawāḥilī', 'kiarabu', 'Swahili', 'Kiingereza', ')', 'ni', 'lugha', 'ya', 'Kibantu', 'amba', 'huzungumzwa', 'Afrika', 'mashariki', 'wa', 'na', 'msemaji', 'kadiri', 'milioni', '200', 'kama', 'lugha', 'ya', 'anza', 'na', 'ya', 'pili', '.']
        case 'swe':
            results = ['svensk', '(', 'svensk', '(', 'fila', ')', ')', 'ära', 'en', 'östnordiskt', 'språka', 'som', 'tala', 'av', 'ungefär', 'tio', 'miljon', 'person', ',', 'främst', 'i', 'Sverige', 'där', 'språk', 'ha', 'man', 'dominant', 'ställning', 'som', 'huvudspråk', ',', 'mena', 'även', 'som', 'den', 'en', 'nationalspråk', 'i', 'Finland', 'och', 'som', 'enda', 'officiell', 'språka', 'på', 'Åland', '.']
        case 'tgl':
            match lemmatizer:
                case 'simplemma_tgl':
                    results = ['Ang', 'wikang', 'Tagalog', '[', '1', ']', '(', 'Baybayin', ':', 'ᜏᜒᜃᜅ᜔', 'Tagalog', ')', ',', 'o', 'ang', 'Tagalog', ',', 'ay', 'isa', 'sa', 'mga', 'pinakaginagamit', 'na', 'wikain', 'ng', 'Pilipinas', '.']
                case 'spacy_tgl':
                    results = ['Ang', 'wikang', 'Tagalog[1', ']', '(', 'Baybayin:ᜏᜒᜃᜅ᜔', 'ᜆᜄᜎᜓᜄ᜔', ')', ',', 'o', 'ang', 'Tagalog', ',', 'ay', 'isa', 'sa', 'mga', 'pinakaginagamit', 'na', 'wika', 'ng', 'Pilipinas', '.']
                case _:
                    tests_lang_util_skipped = True
        case 'xct':
            results = ['བོད་', 'གི་', 'སྐད་ཡིག་', 'ནི་', 'བོད་ཡུལ་', 'དང་', 'ཉེ་འཁོར་', 'གི་', 'ས་ཁུལ་', 'བལ་ཡུལ་', '།', 'འབྲུག་', 'དང་', 'འབྲས་ལྗོངས་', '།', 'ལ་དྭགས་', 'ནས་', 'ལྷོ་', 'མོན་', 'རོང་', 'སོགས་', 'སུ་', 'བེད་སྤྱོད་', 'བྱེད་པ་', 'གི་', 'སྐད་ཡིག་', 'དེ་', '།']
        case 'bod':
            results = ['བོད་', 'གི་', 'སྐད་ཡིག་', 'ནི་', 'བོད་ཡུལ་', 'དང་ཉེ་', 'འཁོ་', 'གི་', 'ས་ཁུལ་', 'བལ་ཡུལ་', '།', 'འབྲུག་', 'དང་', 'འབྲས་ལྗོངས་', '།', 'ལ་དྭགས་', 'ནས་', 'ལྷོ་', 'མོན་', 'རོང་', 'སོགས་', 'སུ་', 'བེད་སྤྱོད་', 'བྱེད་པ་', 'གི་', 'སྐད་ཡིག་', 'དེ་', '།']
        case 'tur':
            match lemmatizer:
                case 'simplemma_tur':
                    results = ['türkçe', 'ya', 'da', 'Türk', 'dil', ',', 'güneydoğu', 'avrupa', 've', 'batı', 'asya', 'konuş', ',', 'Türk', 'dil', 'dil', 'aile', 'ait', 'son', 'ekle', 'bir', 'dildir.', '[', '10', ']']
                case 'spacy_tur':
                    results = ['Türkçe', 'ya', 'da', 'Türk', 'dil', ',', 'Güneydoğu', 'Avrupa', 've', 'Batı', "Asya'da", 'konuş', ',', 'Türk', 'dil', 'dil', 'aile', 'ait', 'son', 'ekle', 'bir', 'dildir.[10', ']']
                case _:
                    tests_lang_util_skipped = True
        case 'ukr':
            match lemmatizer:
                case 'pymorphy3_morphological_analyzer':
                    results = ['украї́нський', 'мо́вий', '(', 'мфа', ':', '[', 'ʊkrɐˈjinʲsʲkɐ', 'ˈmɔʋɐ', ']', ',', 'історичний', 'назва', '—', 'ру́ський', '[', '10', ']', '[', '11', ']', '[', '12', ']', '[', '*', '1', ']', ')', '—', 'національний', 'мова', 'українець', '.']
                case 'simplemma_ukr':
                    results = ['Українськ', 'мо́ва', '(', 'мфа', ':', '[', 'ʊkrɐˈjinʲsʲkɐ', 'ˈmɔʋɐ', ']', ',', 'історичний', 'назва', '—', 'руський', '[', '10', ']', '[', '11', ']', '[', '12', ']', '[', '*', '1', ']', ')', '—', 'національний', 'мова', 'українець', '.']
                case _:
                    tests_lang_util_skipped = True
        case 'urd':
            results = ['اُردُو', '،', 'برصغیر', 'پاک', 'و', 'ہند', 'کم', 'معیاری', 'زبان', 'میں', 'سے', 'ایک', 'ہونا', '۔']
        case 'cym':
            results = ['aelod', 'prpers', "'", 'rhoi', 'cangen', 'Frythonaidd', 'prpers', "'", 'rhoi', 'iaith', 'celtaidd', 'a', 'siarad', 'bod', 'brodorol', 'yn', 'cymru', ',', 'can', 'cymry', 'a', 'pobl', 'arall', 'aredig', 'gwasgar', 'bod', 'lloegr', ',', 'a', 'can', 'cymuned', 'bechan', 'bod', 'yr', 'gwladfa', ',', 'gŵr', 'Ariannin', '[', '8', ']', 'ywen', "'", 'rhoi', 'cymraeg', '(', 'hefyd', 'cymraeg', 'heb', 'yr', 'bannod', ')', '.']
        case _:
            raise wl_test_init.Wl_Exc_Tests_Lang_Skipped(lang)

    if tests_lang_util_skipped:
        raise wl_test_init.Wl_Exc_Tests_Lang_Util_Skipped(lemmatizer)

    wl_test_lemmatize_models(lang, lemmatizer, test_sentence, tokens, results)

def wl_test_lemmatize_models(lang, lemmatizer, test_sentence, tokens, results, lang_excs = ()):
    # Untokenized
    tokens_untokenized = wl_lemmatization.wl_lemmatize(
        main,
        inputs = test_sentence,
        lang = lang,
        lemmatizer = lemmatizer
    )
    lemmas_untokenized = [token.lemma for token in tokens_untokenized]

    print(f'{lang} / {lemmatizer}:')
    print(f'{lemmas_untokenized}\n')

    # Tokenized
    tokens_tokenized = wl_lemmatization.wl_lemmatize(
        main,
        inputs = tokens,
        lang = lang,
        lemmatizer = lemmatizer
    )
    lemmas_tokenized = [token.lemma for token in tokens_tokenized]

    assert lemmas_untokenized == results

    # Check for empty lemmas
    assert lemmas_untokenized
    assert lemmas_tokenized
    assert all(lemmas_untokenized)
    assert all(lemmas_tokenized)

    # Tokenization should not be modified
    assert len(tokens) == len(lemmas_tokenized)

    # Tagged
    main.settings_custom['files']['tags']['body_tag_settings'] = [['Embedded', 'Part of speech', '_*', 'N/A']]

    tokens_tagged = wl_lemmatization.wl_lemmatize(
        main,
        inputs = [wl_texts.Wl_Token(token, tag = '_TEST') for token in tokens],
        lang = lang,
        lemmatizer = lemmatizer
    )
    lemmas_tagged = [token.lemma for token in tokens_tagged]

    assert lemmas_tagged == lemmas_tokenized

    # Long
    tokens_long = wl_lemmatization.wl_lemmatize(
        main,
        inputs = wl_texts.to_tokens(wl_test_lang_examples.TOKENS_LONG, lang = lang),
        lang = lang,
        lemmatizer = lemmatizer
    )
    lemmas_long = [token.lemma for token in tokens_long]

    if lang in lang_excs:
        assert len(lemmas_long) == 101 * 10
    else:
        assert lemmas_long == wl_test_lang_examples.TOKENS_LONG

    # Lemmatized
    lemmas_orig = ['tests']
    tokens_lemmatized = wl_lemmatization.wl_lemmatize(
        main,
        inputs = wl_texts.to_tokens(['test'], lang = lang, lemmas = lemmas_orig),
        lang = lang,
        lemmatizer = lemmatizer
    )
    lemmas_lemmatized = [token.lemma for token in tokens_lemmatized]

    assert lemmas_lemmatized == lemmas_orig

def test_lemmatize_misc():
    # Unsupported languages
    wl_lemmatization.wl_lemmatize(
        main,
        inputs = 'test',
        lang = 'other'
    )

    wl_lemmatization.wl_lemmatize(
        main,
        inputs = [wl_texts.Wl_Token('test', lang = 'other')],
        lang = 'other'
    )

    # NLTK - WordNet lemmatizer
    wl_lemmatization.wl_lemmatize(
        main,
        inputs = 'happy John happily take a',
        lang = 'eng_us',
        lemmatizer = 'nltk_wordnet'
    )

    wl_lemmatization.wl_lemmatize(
        main,
        inputs = wl_texts.to_tokens(['happy', 'John', 'happily', 'take', 'a'], lang = 'eng_us'),
        lang = 'eng_us',
        lemmatizer = 'nltk_wordnet'
    )

if __name__ == '__main__':
    for lang, lemmatizer in test_lemmatizers_local:
        test_lemmatize(lang, lemmatizer)

    test_lemmatize_misc()
