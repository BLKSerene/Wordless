# ----------------------------------------------------------------------
# Tests: NLP - Word tokenization
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

from tests import (
    wl_test_init,
    wl_test_lang_examples
)
from wordless.wl_nlp import (
    wl_texts,
    wl_word_tokenization
)
from wordless.wl_utils import wl_misc

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')
# Avoid loading spaCy's Japanese model when testing the Japanese kanji tokenizer
main.settings_default['word_tokenization']['word_tokenizer_settings']['jpn'] = 'sudachipy_jpn_split_mode_a'

test_word_tokenizers = []

for lang, word_tokenizers in main.settings_global['word_tokenizers'].items():
    for word_tokenizer in word_tokenizers:
        if (
            word_tokenizer not in {
                'spacy_cat', 'spacy_zho', 'spacy_hrv', 'spacy_dan', 'spacy_nld',
                'spacy_eng', 'spacy_fin', 'spacy_fra', 'spacy_deu', 'spacy_ell',
                'spacy_ita', 'spacy_jpn', 'spacy_kor', 'spacy_lit', 'spacy_mkd',
                'spacy_nob', 'spacy_pol', 'spacy_por', 'spacy_ron', 'spacy_rus',
                'spacy_slv', 'spacy_spa', 'spacy_swe', 'spacy_ukr'
            }
            and not word_tokenizer.startswith('stanza_')
            # Skip tests of NLTK's tokenizers for languages except English and Other languages
            and (
                lang in {'eng_gb', 'eng_us', 'other'}
                or word_tokenizer not in {'nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter'}
            )
        ):
            test_word_tokenizers.append((lang, word_tokenizer))

@pytest.mark.parametrize('lang, word_tokenizer', test_word_tokenizers)
def test_word_tokenize(lang, word_tokenizer):
    tests_lang_util_skipped = False

    match lang:
        case 'afr':
            results = ['Afrikaans', 'is', 'tipologies', 'beskou', "'", 'n', 'Indo', '-', 'Europese', ',', 'Wes', '-', 'Germaanse', ',', 'Nederfrankiese', 'taal,[2', ']', 'wat', 'aan', 'die', 'suidpunt', 'van', 'Afrika', 'onder', 'invloed', 'van', 'verskeie', 'ander', 'tale', 'en', 'taalgroepe', 'ontstaan', 'het', '.']
        case 'sqi':
            results = ['Keto', 'gjuhe', 'kryesisht', 'perdoret', 'në', 'Shqipëri', ',', 'Kosovë', 'dhe', 'Maqedoninë', 'e', 'Veriut', ',', 'por', 'edhe', 'në', 'zona', 'të', 'tjera', 'të', 'Evropës', 'Juglindore', 'ku', 'ka', 'një', 'popullsi', 'shqiptare', ',', 'duke', 'përfshirë', 'Malin', 'e', 'Zi', 'dhe', 'Luginën', 'e', 'Preshevës', '.']
        case 'amh':
            results = ['አማርኛ[1', ']', '፡', 'የኢትዮጵያ', '፡', 'መደበኛ', '፡', 'ቋንቋ', '፡', 'ነው', '።']
        case 'ara':
            results = ['ٱللُّغَةُ', 'ٱلْعَرَبِيَّة', 'هي', 'أكثر', 'اللغات', 'السامية', 'تحدثًا', '،', 'وإحدى', 'أكثر', 'اللغات', 'انتشاراً', 'في', 'العالم', '،', 'يتحدثها', 'أكثر', 'من', '467', 'مليون', 'نسمة.(1', ')']
        case 'hye' | 'hyw':
            results = ['Հայերեն', '(', 'ավանդական՝', 'հայերէն', ')', ',', 'հնդեվրոպական', 'լեզվաընտանիքի', 'առանձին', 'ճյուղ', 'հանդիսացող', 'լեզու։']
        case 'asm':
            results = ['অসমীয়া', 'ভাষা', '(', 'ইংৰাজী', ':', 'Assamese', 'language', ')', 'হৈছে', 'সকলোতকৈ', 'পূৰ্বীয়', 'ভাৰতীয়-আৰ্য', 'ভাষা', 'তথা', 'অসমৰ', 'ৰাজ্যিক', 'ভাষা', '।']
        case 'aze':
            results = ['Azərbaycan', 'dili[2][3', ']', 'və', 'ya', 'Azərbaycan', 'türkcəsi[4', ']', ',', 'keçmişdə', 'Azərbaycan', 'Respublikasında', 'sadəcə', 'Türk', 'dili[5', ']', '(', 'Güney', 'Azərbaycanda', ':', 'Türk', 'dili[6][7', ']', ')', '—', 'Azərbaycan', 'Respublikasının', 'və', 'Rusiya', 'Federasiyası', 'Dağıstan', 'Respublikasının[8', ']', 'rəsmi', 'dövlət', 'dili', '.']
        case 'eus':
            results = ['Euskara', 'Euskal', 'Herriko', 'hizkuntza', 'da.[8', ']']
        case 'ben':
            match word_tokenizer:
                case 'sacremoses_moses':
                    results = ['বাংলা', 'ভাষা', '(', 'বাঙলা', ',', 'বাঙ্গলা', ',', 'তথা', 'বাঙ্গালা', 'নামেও', 'পরিচিত', ')', 'একটি', 'ধ্রুপদী', 'ইন্দো-আর্য', 'ভাষা', ',', 'যা', 'দক্ষিণ', 'এশিয়ার', 'বাঙালি', 'জাতির', 'প্রধান', 'কথ্য', 'ও', 'লেখ্য', 'ভাষা', '।']
                case 'spacy_ben':
                    results = ['বাংলা', 'ভাষা', '(', 'বাঙলা', ',', 'বাঙ্গলা', ',', 'তথা', 'বাঙ্গালা', 'নামেও', 'পরিচিত', ')', 'একটি', 'ধ্রুপদী', 'ইন্দো', '-', 'আর্য', 'ভাষা', ',', 'যা', 'দক্ষিণ', 'এশিয়ার', 'বাঙালি', 'জাতির', 'প্রধান', 'কথ্য', 'ও', 'লেখ্য', 'ভাষা', '।']
                case _:
                    tests_lang_util_skipped = True
        case 'bul':
            results = ['Бъ̀лгарският', 'езѝк', 'е', 'индоевропейски', 'език', 'от', 'групата', 'на', 'южнославянските', 'езици', ',', 'като', 'образува', 'неговата', 'източна', 'подгрупа', '.']
        case 'cat':
            results = ['Hi', 'ha', 'altres', 'glotònims', 'tradicionals', 'que', 'es', 'fan', 'servir', 'com', 'a', 'sinònim', 'de', '"', 'català', '"', 'al', 'llarg', 'del', 'domini', 'lingüístic', '.']
        case 'zho_cn':
            match word_tokenizer:
                case 'pkuseg_zho':
                    results = ['汉语', '又', '称', '华语', '[6]', '[7]', '，', '是', '来自', '汉', '民族', '的', '语言', '[', '8', ']', '[', '7', ']', '[', '9', ']', '。']
                case 'wordless_zho_char':
                    results = ['汉', '语', '又', '称', '华', '语', '[', '6', ']', '[', '7', ']', '，', '是', '来', '自', '汉', '民', '族', '的', '语', '言', '[', '8', ']', '[', '7', ']', '[', '9', ']', '。']
                case _:
                    tests_lang_util_skipped = True
        case 'zho_tw':
            match word_tokenizer:
                case 'pkuseg_zho':
                    results = ['漢語', '又', '稱', '華語', '[6]', '[7]', '，', '是', '來自', '漢', '民族', '的', '語言', '[8]', '[', '7', ']', '[', '9', ']', '。']
                case 'wordless_zho_char':
                    results = ['漢', '語', '又', '稱', '華', '語', '[', '6', ']', '[', '7', ']', '，', '是', '來', '自', '漢', '民', '族', '的', '語', '言', '[', '8', ']', '[', '7', ']', '[', '9', ']', '。']
                case _:
                    tests_lang_util_skipped = True
        case 'ces':
            results = ['Čeština', 'neboli', 'český', 'jazyk', 'je', 'západoslovanský', 'jazyk', ',', 'nejbližší', 'slovenštině', ',', 'poté', 'lužické', 'srbštině', 'a', 'polštině', '.']
        case 'nld':
            results = ['Het', 'Nederlands', 'is', 'een', 'West-Germaanse', 'taal', ',', 'de', 'meest', 'gebruikte', 'taal', 'in', 'Nederland', 'en', 'België', ',', 'de', 'officiële', 'taal', 'van', 'Suriname', 'en', 'een', 'van', 'de', 'drie', 'officiële', 'talen', 'van', 'België', '.']
        case 'eng_gb' | 'eng_us' | 'other':
            match word_tokenizer:
                case 'nltk_nist':
                    results = ['English', 'is', 'a', 'West', 'Germanic', 'language', 'in', 'the', 'Indo', '-', 'European', 'language', 'family', ',', 'whose', 'speakers', ',', 'called', 'Anglophones', ',', 'originated', 'in', 'early', 'medieval', 'England', 'on', 'the', 'island', 'of', 'Great', 'Britain', '.', '[4]', '[', '5]', '[', '6]']
                case 'nltk_nltk' | 'nltk_penn_treebank' | 'nltk_tok_tok':
                    results = ['English', 'is', 'a', 'West', 'Germanic', 'language', 'in', 'the', 'Indo-European', 'language', 'family', ',', 'whose', 'speakers', ',', 'called', 'Anglophones', ',', 'originated', 'in', 'early', 'medieval', 'England', 'on', 'the', 'island', 'of', 'Great', 'Britain.', '[', '4', ']', '[', '5', ']', '[', '6', ']']
                case 'nltk_regex':
                    results = ['English', 'is', 'a', 'West', 'Germanic', 'language', 'in', 'the', 'Indo', '-', 'European', 'language', 'family', ',', 'whose', 'speakers', ',', 'called', 'Anglophones', ',', 'originated', 'in', 'early', 'medieval', 'England', 'on', 'the', 'island', 'of', 'Great', 'Britain', '.[', '4', '][', '5', '][', '6', ']']
                case 'nltk_twitter' | 'sacremoses_moses':
                    results = ['English', 'is', 'a', 'West', 'Germanic', 'language', 'in', 'the', 'Indo-European', 'language', 'family', ',', 'whose', 'speakers', ',', 'called', 'Anglophones', ',', 'originated', 'in', 'early', 'medieval', 'England', 'on', 'the', 'island', 'of', 'Great', 'Britain', '.', '[', '4', ']', '[', '5', ']', '[', '6', ']']
                case 'wordless_other_char':
                    results = ['E', 'n', 'g', 'l', 'i', 's', 'h', 'i', 's', 'a', 'W', 'e', 's', 't', 'G', 'e', 'r', 'm', 'a', 'n', 'i', 'c', 'l', 'a', 'n', 'g', 'u', 'a', 'g', 'e', 'i', 'n', 't', 'h', 'e', 'I', 'n', 'd', 'o', '-', 'E', 'u', 'r', 'o', 'p', 'e', 'a', 'n', 'l', 'a', 'n', 'g', 'u', 'a', 'g', 'e', 'f', 'a', 'm', 'i', 'l', 'y', ',', 'w', 'h', 'o', 's', 'e', 's', 'p', 'e', 'a', 'k', 'e', 'r', 's', ',', 'c', 'a', 'l', 'l', 'e', 'd', 'A', 'n', 'g', 'l', 'o', 'p', 'h', 'o', 'n', 'e', 's', ',', 'o', 'r', 'i', 'g', 'i', 'n', 'a', 't', 'e', 'd', 'i', 'n', 'e', 'a', 'r', 'l', 'y', 'm', 'e', 'd', 'i', 'e', 'v', 'a', 'l', 'E', 'n', 'g', 'l', 'a', 'n', 'd', 'o', 'n', 't', 'h', 'e', 'i', 's', 'l', 'a', 'n', 'd', 'o', 'f', 'G', 'r', 'e', 'a', 't', 'B', 'r', 'i', 't', 'a', 'i', 'n', '.', '[', '4', ']', '[', '5', ']', '[', '6', ']']
                case _:
                    tests_lang_util_skipped = True
        case 'est':
            results = ['Eesti', 'keel', '(', 'varasem', 'nimetus', 'maakeel', ')', 'on', 'läänemeresoome', 'lõunarühma', 'kuuluv', 'keel', '.']
        case 'fao':
            results = ['Føroyskt', 'er', 'høvuðsmálið', 'í', 'Føroyum', '.']
        case 'fin':
            results = ['Suomen', 'kieli', 'eli', 'suomi', 'on', 'uralilaisten', 'kielten', 'itämerensuomalaiseen', 'ryhmään', 'kuuluva', 'kieli', ',', 'jota', 'puhuvat', 'pääosin', 'suomalaiset', '.']
        case 'fra':
            results = ['Le', 'français', 'est', 'une', 'langue', 'indo-européenne', 'de', 'la', 'famille', 'des', 'langues', 'romanes', 'dont', 'les', 'locuteurs', 'sont', 'appelés', '«', 'francophones', '»', '.']
        case 'lug':
            results = ['Luganda', '/', 'Oluganda', 'lwe', 'lulimi', 'olwogerwa', 'Abaganda', 'e', 'Yuganda', '.']
        case 'deu_at' | 'deu_de' | 'deu_ch':
            match word_tokenizer:
                case 'nltk_tok_tok':
                    results = ['Die', 'deutsche', 'Sprache', 'oder', 'Deutsch', '[', 'dɔɪ̯tʃ', ']', '[', '24', ']', 'ist', 'eine', 'westgermanische', 'Sprache', ',', 'die', 'weltweit', 'etwa', '90', 'bis', '105', 'Millionen', 'Menschen', 'als', 'Muttersprache', 'und', 'weiteren', 'rund', '80', 'Millionen', 'als', 'Zweit-', 'oder', 'Fremdsprache', 'dient', '.']
                case 'sacremoses_moses':
                    results = ['Die', 'deutsche', 'Sprache', 'oder', 'Deutsch', '[', 'dɔɪ', '̯', 'tʃ', ']', '[', '24', ']', 'ist', 'eine', 'westgermanische', 'Sprache', ',', 'die', 'weltweit', 'etwa', '90', 'bis', '105', 'Millionen', 'Menschen', 'als', 'Muttersprache', 'und', 'weiteren', 'rund', '80', 'Millionen', 'als', 'Zweit-', 'oder', 'Fremdsprache', 'dient', '.']
        case 'grc':
            results = ['ἦλθον', 'δὲ', 'οἱ', 'δύο', 'ἄγγελοι', 'εἰς', 'Σόδομα', 'ἑσπέρας', '·', 'Λὼτ', 'δὲ', 'ἐκάθητο', 'παρὰ', 'τὴν', 'πύλην', 'Σοδόμων', '.', 'ἰδὼν', 'δὲ', 'Λὼτ', 'ἐξανέστη', 'εἰς', 'συνάντησιν', 'αὐτοῖς', 'καὶ', 'προσεκύνησεν', 'τῷ', 'προσώπῳ', 'ἐπὶ', 'τὴν', 'γῆν']
        case 'ell':
            results = ['Η', 'ελληνική', 'γλώσσα', 'ανήκει', 'στην', 'ινδοευρωπαϊκή', 'οικογένεια', '[', '9', ']', 'secεπίσης', 'στο', 'βαλκανικό', 'γλωσσικό', 'δεσμό', '.']
        case 'guj':
            match word_tokenizer:
                case 'sacremoses_moses':
                    results = ['ગુજરાતી', '\u200d', '(', '/', 'ɡʊdʒəˈrɑːti', '/', '[', '૬', ']', ',', 'રોમન', 'લિપિમાં', ':', 'Gujarātī', ',', 'ઉચ્ચાર', ':', '[', 'ɡudʒəˈɾɑːtiː', ']', ')', 'ભારત', 'દેશના', 'ગુજરાત', 'રાજ્યની', 'ઇન્ડો-આર્યન', 'ભાષા', 'છે', 'અને', 'મુખ્યત્વે', 'ગુજરાતી', 'લોકો', 'દ્વારા', 'બોલાય', 'છે', '.']
                case 'spacy_guj':
                    results = ['ગુજરાતી', '\u200d(/ɡʊdʒəˈrɑːti/[૬', ']', ',', 'રોમન', 'લિપિમાં', ':', 'Gujarātī', ',', 'ઉચ્ચાર', ':', '[', 'ɡudʒəˈɾɑːtiː', ']', ')', 'ભારત', 'દેશના', 'ગુજરાત', 'રાજ્યની', 'ઇન્ડો-આર્યન', 'ભાષા', 'છે', 'અને', 'મુખ્યત્વે', 'ગુજરાતી', 'લોકો', 'દ્વારા', 'બોલાય', 'છે.']
                case _:
                    tests_lang_util_skipped = True
        case 'heb':
            results = ['עִבְרִית', 'היא', 'שפה', 'שמית', ',', 'ממשפחת', 'השפות', 'האפרו', '-', 'אסייתיות', ',', 'הידועה', 'כשפתם', 'של', 'היהודים', 'ושל', 'השומרונים', '.']
        case 'hin':
            results = ['हिन्दी', 'या', 'आधुनिक', 'मानक', 'हिन्दी', 'विश्व', 'की', 'एक', 'प्रमुख', 'भाषा', 'है', 'और', 'भारत', 'की', 'एक', 'राजभाषा', 'है', '।']
        case 'hun':
            results = ['A', 'magyar', 'nyelv', 'az', 'uráli', 'nyelvcsalád', 'tagja', ',', 'azon', 'belül', 'a', 'finnugor', 'nyelvek', 'közé', 'tartozó', 'ugor', 'nyelvek', 'egyike', '.']
        case 'isl':
            match word_tokenizer:
                case 'sacremoses_moses':
                    results = ['Íslenska', 'er', 'vesturnorrænt', ',', 'germanskt', 'og', 'indóevrópskt', 'tungumál', 'sem', 'er', 'einkum', 'talað', 'og', 'ritað', 'á', 'Íslandi', 'og', 'er', 'móðurmál', 'langflestra', 'Íslendinga', '.', '[', '6', ']']
                case 'spacy_isl':
                    results = ['Íslenska', 'er', 'vesturnorrænt', ',', 'germanskt', 'og', 'indóevrópskt', 'tungumál', 'sem', 'er', 'einkum', 'talað', 'og', 'ritað', 'á', 'Íslandi', 'og', 'er', 'móðurmál', 'langflestra', 'Íslendinga.[6', ']']
                case _:
                    tests_lang_util_skipped = True
        case 'ind':
            results = ['Bahasa', 'Indonesia', '(', '[', 'baˈhasa', 'indoˈnesija', ']', ')', 'merupakan', 'bahasa', 'resmi', 'sekaligus', 'bahasa', 'nasional', 'di', 'Indonesia.[16', ']']
        case 'gle':
            results = ['Labhraítear', 'in', 'Éirinn', 'go', 'príomha', 'í', ',', 'ach', 'tá', 'cainteoirí', 'Gaeilge', 'ina', 'gcónaí', 'in', 'áiteanna', 'eile', 'ar', 'fud', 'an', 'domhain', '.']
        case 'ita':
            results = ["L'", 'italiano', 'è', 'una', 'lingua', 'romanza', 'parlata', 'principalmente', 'in', 'Italia', '.']
        case 'jpn':
            match word_tokenizer:
                case 'sudachipy_jpn_split_mode_a':
                    results = ['日本', '語', '（', 'にほん', 'ご', '、', 'にっぽん', 'ご', '[', '注釈', '3', ']', '）', 'は', '、', '日本', '国', '内', 'や', '、', 'かつて', 'の', '日本', '領', 'だっ', 'た', '国', '、', 'そして', '国外', '移民', 'や', '移住', '者', 'を', '含む', '日本', '人', '同士', 'の', '間', 'で', '使用', 'さ', 'れ', 'て', 'いる', '言語', '。']
                case 'sudachipy_jpn_split_mode_b' | 'sudachipy_jpn_split_mode_c':
                    results = ['日本語', '（', 'にほん', 'ご', '、', 'にっぽん', 'ご', '[', '注釈', '3', ']', '）', 'は', '、', '日本', '国', '内', 'や', '、', 'かつて', 'の', '日本', '領', 'だっ', 'た', '国', '、', 'そして', '国外', '移民', 'や', '移住者', 'を', '含む', '日本人', '同士', 'の', '間', 'で', '使用', 'さ', 'れ', 'て', 'いる', '言語', '。']
                case 'wordless_jpn_kanji':
                    results = ['日', '本', '語', '（', 'にほん', 'ご', '、', 'にっぽん', 'ご', '[', '注', '釈', '3', ']', '）', 'は', '、', '日', '本', '国', '内', 'や', '、', 'かつて', 'の', '日', '本', '領', 'だっ', 'た', '国', '、', 'そして', '国', '外', '移', '民', 'や', '移', '住', '者', 'を', '含', 'む', '日', '本', '人', '同', '士', 'の', '間', 'で', '使', '用', 'さ', 'れ', 'て', 'いる', '言', '語', '。']
                case _:
                    tests_lang_util_skipped = True
        case 'kan':
            results = ['ದ್ರಾವಿಡ', 'ಭಾಷೆಗಳಲ್ಲಿ', 'ಪ್ರಾಮುಖ್ಯವುಳ್ಳ', 'ಭಾಷೆಯೂ', 'ಭಾರತದ', 'ಪುರಾತನವಾದ', 'ಭಾಷೆಗಳಲ್ಲಿ', 'ಒಂದೂ', 'ಆಗಿರುವ', 'ಕನ್ನಡ', 'ಭಾಷೆಯನ್ನು', 'ಅದರ', 'ವಿವಿಧ', 'ರೂಪಗಳಲ್ಲಿ', 'ಸುಮಾರು', '೪೫', 'ದಶಲಕ್ಷ', '(', '೪', '.', '೫', 'ಕೋಟಿ', ')', 'ಜನರು', 'ಆಡು', 'ನುಡಿಯಾಗಿ', 'ಬಳಸುತ್ತಲಿದ್ದಾರೆ', '.']
        case 'khm':
            results = ['ភាសា', 'ខ្មែរ', 'គឺជា', 'ភាសា', 'កំណើត', 'របស់', 'ជនជាតិ', 'ខ្មែរ', 'និង', 'ជា', 'ភាសា', 'ផ្លូវការ', 'របស់', 'ប្រទេស', 'កម្ពុជា', '។']
        case 'kor':
            results = ['한국어', '(', '韓', '國語', ')', ',', '조선어', '(', '朝鮮', '語', ')', '는', '대한민국', '과', '조선', '민주주의', '인민공화국', '의', '공용어', '이', '다', '.']
        case 'kmr':
            results = ['Kurmancî', ',', 'kurdiya', 'jorîn', 'yan', 'jî', 'kurdiya', 'bakurî', 'yek', 'ji', 'zaravayên', 'zimanê', 'kurdî', 'ye', 'ku', 'ji', 'aliyê', 'kurdan', 've', 'tê', 'axaftin', '.']
        case 'kir':
            results = ['Кыргыз', 'тили', '—', 'Кыргыз', 'Республикасынын', 'мамлекеттик', 'тили', ',', 'түрк', 'тилдери', 'курамына', ',', 'анын', 'ичинде', 'кыргыз-кыпчак', 'же', 'тоо-алтай', 'тобуна', 'кирет', '.']
        case 'lao':
            results = ['ພາສາລາວ', 'ສືບທອດ', 'ມາຈາກ', 'ພາສາ', 'ຕະກຸນ', 'ໄຕ', '-', 'ກະໄດ', 'ຢູ່', 'ພາກ', 'ໃຕ້', 'ຂອງ', 'ປະເທດຈີນ', 'ເຊິ່ງ', 'ເປັນ', 'ຈຸດ', 'ເດີມ', 'ຂອງ', 'ຫຼາຍ', 'ພາສາ', 'ໃນ', 'ຕະກຸນ', 'ນີ້', 'ທີ່', 'ຍັງ', 'ຖືກ', 'ໃຊ້', 'ແລະ', 'ຖືກ', 'ເວົ້າ', 'ຢູ່', 'ໂດຍ', 'ຫຼາຍ', 'ຊົນເຜົ່າ', 'ໃນ', 'ປັດຈຸບັນ', '.']
        case 'lat':
            results = ['Latīnum', ',', 'lingua', 'Latīna,[1', ']', 'sive', 'sermō', 'Latīnus,[2', ']', 'est', 'lingua', 'Indoeuropaea', 'qua', 'primum', 'Latini', 'universi', 'et', 'Romani', 'antiqui', 'in', 'primis', 'loquebantur', 'quamobrem', 'interdum', 'etiam', 'lingua', 'Latia[3', ']', '(', 'in', 'Latio', 'enim', 'sueta', ')', 'et', 'lingua', 'Rōmāna[4', ']', '(', 'nam', 'imperii', 'Romani', 'sermo', 'sollemnis', ')', 'appellabatur', '.']
        case 'lav':
            match word_tokenizer:
                case 'sacremoses_moses':
                    results = ['Latviešu', 'valoda', 'ir', 'dzimtā', 'valoda', 'apmēram', '1,5', 'miljoniem', 'cilvēku', ',', 'galvenokārt', 'Latvijā', ',', 'kur', 'tā', 'ir', 'vienīgā', 'valsts', 'valoda', '.', '[', '1', ']', '[', '3', ']']
                case 'spacy_lav':
                    results = ['Latviešu', 'valoda', 'ir', 'dzimtā', 'valoda', 'apmēram', '1,5', 'miljoniem', 'cilvēku', ',', 'galvenokārt', 'Latvijā', ',', 'kur', 'tā', 'ir', 'vienīgā', 'valsts', 'valoda.[1][3', ']']
                case _:
                    tests_lang_util_skipped = True
        case 'lij':
            results = ['E', 'variante', 'ciù', 'importanti', 'son', 'o', 'zeneize', ',', 'o', 'savoneize', ',', 'o', 'spezzin', ',', 'o', 'ventemigliusu', ',', 'o', 'tabarchin', ',', 'o', 'monegasco', ',', 'e', 'o', 'noveize', ',', 'dîto', 'ascî', 'lìgure', "d'", 'Otrazôvo', '.']
        case 'lit':
            results = ['Lietuvių', 'kalba', '–', 'iš', 'baltų', 'prokalbės', 'kilusi', 'lietuvių', 'tautos', 'kalba', ',', 'kuri', 'Lietuvoje', 'yra', 'valstybinė', ',', 'o', 'Europos', 'Sąjungoje', '–', 'viena', 'iš', 'oficialiųjų', 'kalbų', '.']
        case 'ltz':
            results = ["D'", 'Lëtzebuergesch', 'gëtt', 'an', 'der', 'däitscher', 'Dialektologie', 'als', 'ee', 'westgermaneschen', ',', 'mëtteldäitschen', 'Dialekt', 'aklasséiert', ',', 'deen', 'zum', 'Muselfränkesche', 'gehéiert', '.']
        case 'msa':
            results = ['Jumlah', 'penutur', 'bahasa', 'ini', 'mencakupi', 'lebih', 'daripada', '290', 'juta', 'penutur[4', ']', '(', 'termasuk', 'sebanyak', '260', 'juta', 'orang', 'penutur', 'bahasa', 'Indonesia)[5', ']', 'merentasi', 'kawasan', 'maritim', 'Asia', 'Tenggara', '.']
        case 'mal':
            match word_tokenizer:
                case 'sacremoses_moses':
                    results = ['ഇതു', 'ദ്രാവിഡ', 'ഭാഷാ', 'കുടുംബത്തിൽപ്പെടുന്നു', '.']
                case 'spacy_mal':
                    results = ['ഇതു', 'ദ്രാവിഡ', 'ഭാഷാ', 'കുടുംബത്തിൽപ്പെടുന്നു.']
                case _:
                    tests_lang_util_skipped = True
        case 'mni_mtei':
            results = ['ꯃꯤꯇꯩꯂꯣꯟ', '(', 'ꯃꯤꯇꯩꯂꯣꯜ', ')', 'ꯅꯠꯇ', '꯭', 'ꯔꯒ', 'ꯃꯩꯇꯩꯂꯣꯟ', '(', 'ꯃꯩꯇꯩꯂꯣꯜ', ')', 'ꯅꯠꯇ', '꯭', 'ꯔꯒ', 'ꯃꯅꯤꯄꯨꯔꯤ', 'ꯂꯣꯟ', '(', 'ꯃꯅꯤꯄꯨꯔꯤ', 'ꯂꯣꯜ', ')', 'ꯑꯁꯤ', 'ꯑꯋꯥꯡ-ꯅꯣꯡꯄꯣꯛ', 'ꯏꯟꯗꯤꯌꯥꯒꯤ', 'ꯃꯅꯤꯄꯨꯔꯗ', 'ꯃꯄꯨꯡ', 'ꯑꯣꯢꯅ', 'ꯉꯥꯡꯅꯕ', 'ꯂꯣꯟ', 'ꯑꯃꯅꯤ', '꯫']
        case 'mar':
            match word_tokenizer:
                case 'sacremoses_moses':
                    results = ['मराठी', 'भाषा', 'ही', 'इंडो-युरोपीय', 'भाषाकुळातील', 'एक', 'भाषा', 'आहे', '.']
                case 'spacy_mar':
                    results = ['मराठी', 'भाषा', 'ही', 'इंडो', '-', 'युरोपीय', 'भाषाकुळातील', 'एक', 'भाषा', 'आहे', '.']
                case _:
                    tests_lang_util_skipped = True
        case 'nep':
            results = ['नेपाली', 'भाषा', 'एक', 'आर्य', 'भाषा', 'हो', 'जुन', 'दक्षिण', 'एसियाको', 'हिमालय', 'क्षेत्रमा', 'बोलिन्छ', '।']
        case 'nno':
            results = ['Nynorsk', ',', 'før', '1929', 'offisielt', 'kalla', 'landsmål', ',', 'er', 'sidan', 'jamstillingsvedtaket', 'av', '12.', 'mai', '1885', 'ei', 'av', 'dei', 'to', 'offisielle', 'målformene', 'av', 'norsk', ';', 'den', 'andre', 'forma', 'er', 'bokmål', '.']
        case 'ori':
            results = ['ଓଡ଼ିଆ', '(', 'ଇଂରାଜୀ', 'ଭାଷାରେ', 'Odia', '/', 'əˈdiːə', '/', 'or', 'Oriya', '/', 'ɒˈriːə', '/', ',', ')', 'ଇଣ୍ଡୋ-ଇଉରୋପୀୟ', 'ଭାଷାଗୋଷ୍ଠୀ', 'ଅନ୍ତର୍ଗତ', 'ଏକ', 'ଇଣ୍ଡୋ-ଆର୍ଯ୍ୟ', 'ଭାରତୀୟ', 'ଭାଷା', '।']
        case 'pan_guru':
            results = ['ਪੰਜਾਬੀ', 'ਭਾਸ਼ਾ', '(', 'ਸ਼ਾਹਮੁਖੀ', 'ਲਿਪੀ', ':', '\u200e', 'پنجابی', ',', 'ਪੰਜਾਬੀ', ')', 'ਪੰਜਾਬ', 'ਦੀ', 'ਭਾਸ਼ਾ', 'ਹੈ', ',', 'ਜਿਸ', 'ਨੂੰ', 'ਪੰਜਾਬ', 'ਖੇਤਰ', 'ਦੇ', 'ਵਸਨੀਕ', 'ਜਾਂ', 'ਸੰਬੰਧਿਤ', 'ਲੋਕ', 'ਬੋਲਦੇ', 'ਹਨ', '।', '[', '18', ']']
        case 'fas':
            results = ['فارسی', 'یا', 'پارسی', 'یکی', 'از', 'زبان\u200cهای', 'ایرانی', 'غربی', 'از', 'زیرگروه', 'ایرانی', 'شاخهٔ', 'هندوایرانیِ', 'خانوادهٔ', 'زبان\u200cهای', 'هندواروپایی', 'است', 'که', 'در', 'کشورهای', 'ایران', '،', 'افغانستان', '،', 'تاجیکستان', '،', 'ازبکستان', '،', 'پاکستان', '،', 'عراق', '،', 'ترکمنستان', 'و', 'آذربایجان', 'به', 'آن', 'سخن', 'می\u200cگویند', '.']
        case 'pol':
            results = ['Język', 'polski', ',', 'polszczyzna', '–', 'język', 'lechicki', 'z', 'grupy', 'zachodniosłowiańskiej', '(', 'do', 'której', 'należą', 'również', 'czeski', ',', 'kaszubski', ',', 'słowacki', ',', 'języki', 'łużyckie', 'czy', 'wymarły', 'język', 'drzewiański', ')', ',', 'stanowiącej', 'część', 'rodziny', 'indoeuropejskiej', '.']
        case 'por_br' | 'por_pt':
            results = ['A', 'língua', 'portuguesa', ',', 'também', 'designada', 'português', ',', 'é', 'uma', 'língua', 'indo-europeia', 'românica', 'flexiva', 'ocidental', 'originada', 'no', 'galego-português', 'falado', 'no', 'Reino', 'da', 'Galiza', 'e', 'no', 'norte', 'de', 'Portugal', '.']
        case 'ron':
            results = ['Limba', 'română', '(', '[', 'ˈlimba', 'roˈmɨnə', ']', '(', 'audio', ')', 'sau', 'românește', '[', 'romɨˈneʃte', ']', ')', 'este', 'limba', 'oficială', 'și', 'principală', 'a', 'României', 'și', 'a', 'Republicii', 'Moldova', '.']
        case 'rus':
            match word_tokenizer:
                case 'nltk_tok_tok':
                    results = ['Русский', 'язык', '(', 'МФА', ':', '[', 'ˈruskʲɪɪ̯', 'ɪ̯ɪˈzɨk', ']', 'о', 'файле', ')', '[', '~', '3', ']', '—', 'язык', 'восточнославянской', 'группы', 'славянской', 'ветви', 'индоевропейской', 'языковой', 'семьи', ',', 'национальный', 'язык', 'русского', 'народа', '.']
                case 'sacremoses_moses':
                    results = ['Русский', 'язык', '(', 'МФА', ':', '[', 'ˈruskʲɪɪ', '̯', 'ɪ', '̯', 'ɪˈzɨk', ']', 'о', 'файле', ')', '[', '~', '3', ']', '—', 'язык', 'восточнославянской', 'группы', 'славянской', 'ветви', 'индоевропейской', 'языковой', 'семьи', ',', 'национальный', 'язык', 'русского', 'народа', '.']
                case _:
                    tests_lang_util_skipped = True
        case 'san':
            results = ['संस्कृतं', 'जगत', 'एकतमातिप्राचीना', 'समृद्धा', 'शास्त्रीया', 'च', 'भाषासु', 'वर्तते', '।']
        case 'gla':
            results = ["'S", 'i', 'cànan', 'dùthchasach', 'na', 'h', '-', 'Alba', 'a', "th'", 'anns', "a'", 'Ghàidhlig', '.']
        case 'srp_cyrl':
            results = ['Српски', 'језик', 'припада', 'словенској', 'групи', 'језика', 'породице', 'индоевропских', 'језика.[12', ']']
        case 'sin':
            results = ['ශ්\u200dරී', 'ලංකාවේ', 'ප්\u200dරධාන', 'ජාතිය', 'වන', 'සිංහල', 'ජනයාගේ', 'මව්', 'බස', 'සිංහල', 'වෙයි', '.']
        case 'slk':
            results = ['Slovenčina', 'patrí', 'do', 'skupiny', 'západoslovanských', 'jazykov', '(', 'spolu', 's', 'češtinou', ',', 'poľštinou', ',', 'hornou', 'a', 'dolnou', 'lužickou', 'srbčinou', 'a', 'kašubčinou', ')', '.']
        case 'slv':
            results = ['Slovenščina', '[', 'sloˈʋenʃtʃina', ']', 'je', 'združeni', 'naziv', 'za', 'uradni', 'knjižni', 'jezik', 'Slovencev', 'in', 'skupno', 'ime', 'za', 'narečja', 'in', 'govore', ',', 'ki', 'jih', 'govorijo', 'ali', 'so', 'jih', 'nekoč', 'govorili', 'Slovenci', '.']
        case 'dsb':
            results = ['Dolnoserbšćina', 'gromaźe', 'z', 'górnoserbšćinu', 'słušatej', 'k', 'kupce', 'serbskeju', 'rěcowu', 'w', 'ramiku', 'pódwjacornosłowjańskich', 'rěcy', '.']
        case 'hsb':
            results = ['Hornjoserbšćina', 'je', 'zapadosłowjanska', 'rěč', ',', 'kotraž', 'so', 'w', 'Hornjej', 'Łužicy', 'wokoło', 'městow', 'Budyšin', ',', 'Kamjenc', 'a', 'Wojerecy', 'rěči', '.']
        case 'spa':
            results = ['El', 'español', 'o', 'castellano', 'es', 'una', 'lengua', 'romance', 'procedente', 'del', 'latín', 'hablado', ',', 'perteneciente', 'a', 'la', 'familia', 'de', 'lenguas', 'indoeuropeas', '.']
        case 'swe':
            results = ['Svenska', '(', 'svenska', '(', 'fil', ')', ')', 'är', 'ett', 'östnordiskt', 'språk', 'som', 'talas', 'av', 'ungefär', 'tio', 'miljoner', 'personer', ',', 'främst', 'i', 'Sverige', 'där', 'språket', 'har', 'en', 'dominant', 'ställning', 'som', 'huvudspråk', ',', 'men', 'även', 'som', 'det', 'ena', 'nationalspråket', 'i', 'Finland', 'och', 'som', 'enda', 'officiella', 'språk', 'på', 'Åland', '.']
        case 'tgl':
            results = ['Ang', 'wikang', 'Tagalog[1', ']', '(', 'Baybayin:ᜏᜒᜃᜅ᜔', 'ᜆᜄᜎᜓᜄ᜔', ')', ',', 'o', 'ang', 'Tagalog', ',', 'ay', 'isa', 'sa', 'mga', 'pinakaginagamit', 'na', 'wika', 'ng', 'Pilipinas', '.']
        case 'tgk':
            results = ['Забони', 'тоҷикӣ', '(', 'дар', 'солҳои', '1989', '—', '1991', '—', 'забони', 'форсии', 'тоҷикӣ', ';', '1991', '—', '1999', '–', 'забони', 'тоҷикии', 'форсӣ', ',', 'дарӣ', ':', 'زبان', 'تاجیکی', ')', '—', 'шакли', 'забони', 'порсӣ', 'буда', ',', 'дар', 'Тоҷикистон', 'ҳамчун', 'забони', 'давлатӣ', 'мебошад', '.']
        case 'tam':
            results = ['தமிழ்', '(', 'Tamil', 'language', ')', 'தமிழர்களினதும்', 'தமிழ்', 'பேசும்', 'பலரின்', 'தாய்மொழி', 'ஆகும்', '.']
        case 'tat':
            results = ['Татар', 'теле', '—', 'татарларның', 'милли', 'теле', ',', 'Татарстанның', 'дәүләт', 'теле', ',', 'таралышы', 'буенча', 'Россиядә', 'икенче', 'тел', '.']
        case 'tel':
            results = ['తెలుగు', 'ఆంధ్ర', ',', 'తెలంగాణ', 'రాష్ట్రాలలో', 'మున్నధికారిక', 'నుడి', '.']
        case 'tdt':
            results = ['Tetun', '(', 'iha', 'portugés', ':', 'tétum', ';', 'iha', 'inglés', ':', 'Tetum', ')', 'neke', 'lian', 'nasionál', 'no', 'co-ofisiál', 'Timór', 'Lorosake', 'nian', '.']
        case 'tha':
            match word_tokenizer:
                case 'pythainlp_longest_matching':
                    results = ['ภาษาไทย', 'หรือ', 'ภาษาไทย', 'กลาง', 'เป็น', 'ภาษา', 'ใน', 'กลุ่ม', 'ภาษา', 'ไท', 'สาขา', 'ย่อย', 'เชียงแสน', 'ซึ่ง', 'เป็น', 'กลุ่มย่อย', 'ของ', 'ตระกูล', 'ภาษา', 'ข', 'ร้า', '-', 'ไท', 'และ', 'เป็น', 'ภาษาราชการ', 'และ', 'ภาษาประจำชาติ', 'ของ', 'ประเทศ', 'ไทย', '[', '3', '][', '4', ']']
                case 'pythainlp_max_matching' | 'pythainlp_nercut':
                    results = ['ภาษาไทย', 'หรือ', 'ภาษาไทยกลาง', 'เป็น', 'ภาษา', 'ใน', 'กลุ่ม', 'ภาษา', 'ไท', 'สาขาย่อย', 'เชียงแสน', 'ซึ่ง', 'เป็น', 'กลุ่มย่อย', 'ของ', 'ตระกูล', 'ภาษา', 'ข', 'ร้า', '-', 'ไท', 'และ', 'เป็น', 'ภาษาราชการ', 'และ', 'ภาษาประจำชาติ', 'ของ', 'ประเทศ', 'ไทย', '[', '3', '][', '4', ']']
                case 'pythainlp_max_matching_tcc':
                    results = ['ภาษาไทย', 'หรือ', 'ภาษาไทย', 'กลาง', 'เป็น', 'ภาษา', 'ใน', 'กลุ่ม', 'ภาษา', 'ไท', 'สาขา', 'ย่อย', 'เชียงแสน', 'ซึ่ง', 'เป็น', 'กลุ่มย่อย', 'ของ', 'ตระกูล', 'ภาษา', 'ข', 'ร้า', '-', 'ไท', 'และ', 'เป็น', 'ภาษาราชการ', 'และ', 'ภาษาประจำชาติ', 'ของ', 'ประเทศ', 'ไทย', '[3][4]']
                case _:
                    tests_lang_util_skipped = True
        case 'xct':
            results = ['བོད་', 'ཀྱི་', 'སྐད་ཡིག་', 'ནི་', 'བོད་ཡུལ་', 'དང་', 'ཉེ་འཁོར་', 'གྱི་', 'ས་ཁུལ་', 'བལ་ཡུལ', '།', 'འབྲུག་', 'དང་', 'འབྲས་ལྗོངས', '།', 'ལ་དྭགས་', 'ནས་', 'ལྷོ་', 'མོན་', 'རོང་', 'སོགས་', 'སུ་', 'བེད་སྤྱོད་', 'བྱེད་པ', 'འི་', 'སྐད་ཡིག་', 'དེ', '།']
        case 'bod':
            results = ['བོད་', 'ཀྱི་', 'སྐད་ཡིག་', 'ནི་', 'བོད་ཡུལ་', 'དང་ཉེ་', 'འཁོར་', 'གྱི་', 'ས་ཁུལ་', 'བལ་ཡུལ', '།', 'འབྲུག་', 'དང་', 'འབྲས་ལྗོངས', '།', 'ལ་དྭགས་', 'ནས་', 'ལྷོ་', 'མོན་', 'རོང་', 'སོགས་', 'སུ་', 'བེད་སྤྱོད་', 'བྱེད་པ', 'འི་', 'སྐད་ཡིག་', 'དེ', '།']
        case 'tir':
            results = ['ትግርኛ', 'ኣብ', 'ኤርትራን', 'ኣብ', 'ሰሜናዊ', 'ኢትዮጵያን', 'ኣብ', 'ክልል', 'ትግራይ', 'ዝዝረብ', 'ሴማዊ', 'ቋንቋ', 'እዩ', '።']
        case 'tsn':
            results = ['Setswana', 'ke', 'teme', 'e', 'e', 'buiwang', 'mo', 'mafatsheng', 'a', 'Aforika', 'Borwa', ',', 'Botswana', ',', 'Namibia', 'le', 'Zimbabwe', '.']
        case 'tur':
            results = ['Türkçe', 'ya', 'da', 'Türk', 'dili', ',', 'Güneydoğu', 'Avrupa', 've', 'Batı', "Asya'da", 'konuşulan', ',', 'Türk', 'dilleri', 'dil', 'ailesine', 'ait', 'sondan', 'eklemeli', 'bir', 'dildir.[10', ']']
        case 'urd':
            results = ['اُردُو', '،', 'برصغیر', 'پاک', 'و', 'ہند', 'کی', 'معیاری', 'زبانوں', 'میں', 'سے', 'ایک', 'ہے', '۔']
        case 'vie':
            match word_tokenizer:
                case 'nltk_tok_tok':
                    results = ['Tiếng', 'Việt', 'hay', 'tiếng', 'Kinh', 'là', 'một', 'ngôn', 'ngữ', 'thuộc', 'ngữ', 'hệ', 'Nam', 'Á', ',', 'được', 'công', 'nhận', 'là', 'ngôn', 'ngữ', 'chính', 'thức', 'tại', 'Việt', 'Nam', '.']
                case 'underthesea_vie':
                    results = ['Tiếng', 'Việt', 'hay', 'tiếng', 'Kinh', 'là', 'một', 'ngôn ngữ', 'thuộc ngữ', 'hệ', 'Nam Á', ',', 'được', 'công nhận', 'là', 'ngôn ngữ', 'chính thức', 'tại', 'Việt Nam', '.']
                case _:
                    tests_lang_util_skipped = True
        case 'yor':
            results = ['Èdè', 'Yorùbá', 'Ni', 'èdè', 'tí', 'ó', 'ṣàkójọpọ̀', 'gbogbo', 'ọmọ', 'káàárọ̀-oò', '-', 'jíire', 'bí', ',', 'ní', 'apá', 'Ìwọ̀-Oòrùn', 'ilẹ̀', 'Nàìjíríà', ',', 'tí', 'a', 'bá', 'wo', 'èdè', 'Yorùbá', ',', 'àwọn', 'onímọ̀', 'pín', 'èdè', 'náà', 'sábẹ́', 'ẹ̀yà', 'Kwa', 'nínú', 'ẹbí', 'èdè', 'Niger', '-', 'Congo', '.']
        case _:
            raise wl_test_init.Wl_Exc_Tests_Lang_Skipped(lang)

    if tests_lang_util_skipped:
        raise wl_test_init.Wl_Exc_Tests_Lang_Util_Skipped(word_tokenizer)

    wl_test_word_tokenize_models(lang, word_tokenizer, results)

def wl_test_word_tokenize_models(lang, word_tokenizer, results):
    print(f'{lang} / {word_tokenizer}:')

    sentence = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}')
    tokens = wl_word_tokenization.wl_word_tokenize(
        main,
        text = f'\n\n{sentence}\n\n\n0\n\n\n',
        lang = lang,
        word_tokenizer = word_tokenizer
    )
    tokens[2] = wl_texts.to_display_texts(wl_misc.flatten_list(tokens[2]))

    print(f'{tokens}\n')

    # The count of tokens should be more than 1
    assert len(tokens) > 1

    # The count of tokens should be more than the length of tokens split by space, except Vietnamese
    match lang:
        case 'chu' | 'cop' | 'pcm' | 'orv':
            assert len(tokens[2]) == len(sentence.split())
        case 'mal':
            if word_tokenizer == 'spacy_mal':
                assert len(tokens[2]) == len(sentence.split())
            else:
                assert len(tokens[2]) > len(sentence.split())
        case 'vie':
            if word_tokenizer == 'underthesea_vie':
                assert len(tokens[2]) < len(sentence.split())
            else:
                assert len(tokens[2]) > len(sentence.split())
        case _:
            assert len(tokens[2]) > len(sentence.split())

    # Empty lines should be tokenized as empty paragraphs
    assert tokens == [[], [], results, [], [], [[[wl_texts.Wl_Token('0')]]], [], []]

def test_char_tokenizers():
    for lang, char_tokenizer in zip(
        ('zho_cn', 'zho_tw', 'jpn'),
        ('wordless_zho_char', 'wordless_zho_char', 'wordless_jpn_kanji')
    ):
        match lang:
            case 'zho_cn':
                sentence = wl_test_lang_examples.SENTENCE_ZHO_CN_CHAR_TOKENIZER + 'test'
            case 'zho_tw':
                sentence = wl_test_lang_examples.SENTENCE_ZHO_TW_CHAR_TOKENIZER + 'test'
            case 'jpn':
                sentence = wl_test_lang_examples.SENTENCE_JPN_KANJI_TOKENIZER + '\nあ阿、a阿、sあ、あs。\nあ\na'

        tokens = wl_word_tokenization.wl_word_tokenize_flat(
            main,
            text = sentence,
            lang = lang,
            word_tokenizer = char_tokenizer
        )
        tokens = wl_texts.to_display_texts(tokens)

        print(f'{lang} / {char_tokenizer}:')
        print(f'{tokens}\n')

        match lang:
            case 'zho_cn':
                assert tokens == ['英', '国', '的', '全', '称', '是', 'United', 'Kingdom', 'of', 'Great', 'Britain', '，', '由', '四', '个', '部', '分', '组', '成', '：', 'England', '、', 'Scotland', '、', 'Wales', '和', 'Northern', 'Ireland', '。', 'test']
            case 'zho_tw':
                assert tokens == ['英', '國', '的', '全', '稱', '是', 'United', 'Kingdom', 'of', 'Great', 'Britain', '，', '由', '四', '個', '部', '分', '組', '成', '：', 'England', '、', 'Scotland', '、', 'Wales', '和', 'Northern', 'Ireland', '。', 'test']
            case 'jpn':
                assert tokens == ['The', 'sentence', '``', '天', '気', 'が', 'いい', 'から', '、', '散', '歩', 'し', 'ましょう', '。', '``', 'means', ':', 'The', 'weather', 'is', 'good', 'so', 'let', "'s", 'take', 'a', 'walk', '.', 'あ', '阿', '、', 'a', '阿', '、', 's', 'あ', '、', 'あ', 's', '。', 'あ', 'a']

if __name__ == '__main__':
    for lang, word_tokenizer in test_word_tokenizers:
        test_word_tokenize(lang, word_tokenizer)

    test_char_tokenizers()
