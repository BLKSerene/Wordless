# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Word Tokenization
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

from tests import wl_test_init, wl_test_lang_examples
from wordless.wl_nlp import wl_word_tokenization

main = wl_test_init.Wl_Test_Main()

test_word_tokenizers = []

for lang, word_tokenizers in main.settings_global['word_tokenizers'].items():
    for word_tokenizer in word_tokenizers:
        if (
            lang.startswith('eng_')
            # Skip tests of NLTK's tokenizers for languages other than English
            or (
                not lang.startswith('eng_')
                and word_tokenizer not in ['nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter']
            )
        ):
            test_word_tokenizers.append((lang, word_tokenizer))

@pytest.mark.parametrize('lang, word_tokenizer', test_word_tokenizers)
def test_word_tokenize(lang, word_tokenizer):
    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}'),
        lang = lang,
        word_tokenizer = word_tokenizer
    )

    print(f'{lang} / {word_tokenizer}:')
    print(f'{tokens}\n')

    # The count of tokens should be more than 1
    assert len(tokens) > 1
    # The count of tokens should be more than the length of tokens split by space
    assert len(tokens) > len(f'SENTENCE_{lang.upper()}'.split())

    word_tokenizer_skipped = False

    if lang == 'afr':
        assert tokens == ['Afrikaans', 'is', 'tipologies', 'beskou', "'", 'n', 'Indo', '-', 'Europese', ',', 'Wes', '-', 'Germaanse', ',', 'Nederfrankiese', 'taal,[2', ']', 'wat', 'aan', 'die', 'suidpunt', 'van', 'Afrika', 'onder', 'invloed', 'van', 'verskeie', 'ander', 'tale', 'en', 'taalgroepe', 'ontstaan', 'het', '.']
    elif lang == 'sqi':
        assert tokens == ['Gjuha', 'shqipe', '(', 'ose', 'thjesht', 'shqipja', ')', 'është', 'gjuhë', 'dhe', 'degë', 'e', 'veçantë', 'e', 'familjes', 'indo', '-', 'evropiane', 'që', 'flitet', 'nga', 'rreth', '7', '-', '10', 'milionë', 'njerëz', 'në', 'botë,[1', ']', 'kryesisht', 'në', 'Shqipëri', ',', 'Kosovë', 'dhe', 'Maqedoninë', 'e', 'Veriut', ',', 'por', 'edhe', 'në', 'zona', 'të', 'tjera', 'të', 'Evropës', 'Juglindore', 'ku', 'ka', 'një', 'popullsi', 'shqiptare', ',', 'duke', 'përfshirë', 'Malin', 'e', 'Zi', 'dhe', 'Luginën', 'e', 'Preshevës', '.']
    elif lang == 'amh':
        assert tokens == ['አማርኛ[1', ']', '፡', 'የኢትዮጵያ', '፡', 'መደበኛ', '፡', 'ቋንቋ', '፡', 'ነው', '።']
    elif lang == 'ara':
        assert tokens == ['اللُّغَة', 'العَرَبِيّة', 'هي', 'أكثر', 'اللغات', 'السامية', 'تحدثًا', '،', 'وإحدى', 'أكثر', 'اللغات', 'انتشاراً', 'في', 'العالم', '،', 'يتحدثها', 'أكثر', 'من', '467', 'مليون', 'نسمة،(1', ')', 'ويتوزع', 'متحدثوها', 'في', 'الوطن', 'العربي', '،', 'بالإضافة', 'إلى', 'العديد', 'من', 'المناطق', 'الأخرى', 'المجاورة', 'كالأحواز', 'وتركيا', 'وتشاد', 'ومالي', 'والسنغال', 'وإرتيريا', 'وإثيوبيا', 'وجنوب', 'السودان', 'وإيران', '.']
    elif lang == 'hye':
        assert tokens == ['Հայերեն', '(', 'ավանդական՝', 'հայերէն', ')', ',', 'հնդեվրոպական', 'լեզվաընտանիքի', 'առանձին', 'ճյուղ', 'հանդիսացող', 'լեզու։']
    elif lang == 'asm':
        assert tokens == ['অসমীয়া', 'ভাষা', 'হৈছে', 'সকলোতকৈ', 'পূৰ্বীয়', 'ভাৰতীয়-আৰ্য', 'ভাষা', '।']
    elif lang == 'aze':
        assert tokens == ['Azərbaycan', 'dili[2][3', ']', '(', 'Cənubi', 'Azərbaycanda', ':', 'Türk', 'dili[4][5', ']', ')', '—', 'Azərbaycan', 'Respublikasının', 'və', 'Rusiya', 'Federasiyası', 'Dağıstan', 'Respublikasının[6', ']', 'rəsmi', 'dövlət', 'dili', '.']
    elif lang == 'eus':
        assert tokens == ['Euskara', 'Euskal', 'Herriko', 'hizkuntza', 'da.[5', ']']
    elif lang == 'ben':
        if word_tokenizer == 'sacremoses_moses':
            assert tokens == ['বাংলা', 'ভাষা', '(', 'বাঙলা', ',', 'বাঙ্গলা', ',', 'তথা', 'বাঙ্গালা', 'নামেও', 'পরিচিত', ')', 'একটি', 'ইন্দো-আর্য', 'ভাষা', ',', 'যা', 'দক্ষিণ', 'এশিয়ার', 'বাঙালি', 'জাতির', 'প্রধান', 'কথ্য', 'ও', 'লেখ্য', 'ভাষা', '।']
        elif word_tokenizer == 'spacy_ben':
            assert tokens == ['বাংলা', 'ভাষা', '(', 'বাঙলা', ',', 'বাঙ্গলা', ',', 'তথা', 'বাঙ্গালা', 'নামেও', 'পরিচিত', ')', 'একটি', 'ইন্দো', '-', 'আর্য', 'ভাষা', ',', 'যা', 'দক্ষিণ', 'এশিয়ার', 'বাঙালি', 'জাতির', 'প্রধান', 'কথ্য', 'ও', 'লেখ্য', 'ভাষা', '।']
        else:
            word_tokenizer_skipped = True
    elif lang == 'bul':
        assert tokens == ['Бъ̀лгарският', 'езѝк', 'е', 'индоевропейски', 'език', 'от', 'групата', 'на', 'южнославянските', 'езици', '.']
    elif lang == 'cat':
        if word_tokenizer == 'sacremoses_moses':
            assert tokens == ['El', 'català', '(', 'denominació', 'oficial', 'a', 'Catalunya', ',', 'a', 'les', 'Illes', 'Balears', ',', 'a', 'Andorra', ',', 'a', 'la', 'ciutat', 'de', 'l', "'", 'Alguer', 'i', 'tradicional', 'a', 'Catalunya', 'del', 'Nord', ')', 'o', 'valencià', '(', 'denominació', 'oficial', 'al', 'País', 'Valencià', 'i', 'tradicional', 'al', 'Carxe', ')', 'és', 'una', 'llengua', 'romànica', 'parlada', 'a', 'Catalunya', ',', 'el', 'País', 'Valencià', '(', 'tret', 'd', "'", 'algunes', 'comarques', 'i', 'localitats', 'de', 'l', "'", 'interior', ')', ',', 'les', 'Illes', 'Balears', ',', 'Andorra', ',', 'la', 'Franja', 'de', 'Ponent', '(', 'a', 'l', "'", 'Aragó', ')', ',', 'la', 'ciutat', 'de', 'l', "'", 'Alguer', '(', 'a', 'l', "'", 'illa', 'de', 'Sardenya', ')', ',', 'la', 'Catalunya', 'del', 'Nord', ',', '[', '8', ']', 'el', 'Carxe', '(', 'un', 'petit', 'territori', 'de', 'Múrcia', 'poblat', 'per', 'pobladors', 'valencians', ')', ',', '[', '9', ']', '[', '10', ']', 'i', 'en', 'comunitats', 'arreu', 'del', 'món', '(', 'entre', 'les', 'quals', 'destaca', 'la', 'de', 'l', "'", 'Argentina', ',', 'amb', '200.000', 'parlants', ')', '.', '[', '11', ']']
        elif word_tokenizer == 'spacy_cat':
            assert tokens == ['El', 'català', '(', 'denominació', 'oficial', 'a', 'Catalunya', ',', 'a', 'les', 'Illes', 'Balears', ',', 'a', 'Andorra', ',', 'a', 'la', 'ciutat', 'de', "l'", 'Alguer', 'i', 'tradicional', 'a', 'Catalunya', 'd', 'el', 'Nord', ')', 'o', 'valencià', '(', 'denominació', 'oficial', 'a', 'l', 'País', 'Valencià', 'i', 'tradicional', 'a', 'l', 'Carxe', ')', 'és', 'una', 'llengua', 'romànica', 'parlada', 'a', 'Catalunya', ',', 'el', 'País', 'Valencià', '(', 'tret', "d'", 'algunes', 'comarques', 'i', 'localitats', 'de', "l'", 'interior', ')', ',', 'les', 'Illes', 'Balears', ',', 'Andorra', ',', 'la', 'Franja', 'de', 'Ponent', '(', 'a', "l'", 'Aragó', ')', ',', 'la', 'ciutat', 'de', "l'", 'Alguer', '(', 'a', "l'", 'illa', 'de', 'Sardenya', ')', ',', 'la', 'Catalunya', 'd', 'el', 'Nord,[8', ']', 'el', 'Carxe', '(', 'un', 'petit', 'territori', 'de', 'Múrcia', 'poblat', 'per', 'pobladors', 'valencians),[9][10', ']', 'i', 'en', 'comunitats', 'arreu', 'd', 'el', 'món', '(', 'entre', 'les', 'quals', 'destaca', 'la', 'de', "l'", 'Argentina', ',', 'amb', '200.000', 'parlants).[11', ']']
        else:
            word_tokenizer_skipped = True
    elif lang == 'zho_cn':
        if word_tokenizer == 'jieba_zho':
            assert tokens == ['汉语', '又称', '华语', '[', '3', ']', '、', '唐话', '[', '4', ']', '，', '概指', '由', '上', '古汉语', '（', '先秦', '雅言', '）', '发展', '而', '来', '、', '书面', '使用', '汉字', '的', '分析语', '，', '为', '汉藏语系', '最大', '的', '一支', '语族', '。']
        elif word_tokenizer == 'pkuseg_zho':
            assert tokens == ['汉语', '又', '称', '华语', '[', '3', ']', '、', '唐', '话[', '4]', '，', '概指', '由', '上古', '汉语', '（', '先秦', '雅言', '）', '发展', '而', '来', '、', '书面', '使用', '汉字', '的', '分析语', '，', '为', '汉藏', '语系', '最', '大', '的', '一', '支', '语族', '。']
        elif word_tokenizer == 'spacy_zho':
            assert tokens == ['汉语', '又', '称', '华语', '[3', ']', '、', '唐话', '[', '4', ']', '，', '概指', '由', '上古', '汉语', '（', '先', '秦雅言', '）', '发展', '而', '来', '、', '书面', '使用', '汉字', '的', '分析语', '，', '为', '汉藏', '语系', '最', '大', '的', '一', '支', '语族', '。']
        elif word_tokenizer == 'wordless_zho_char':
            assert tokens == ['汉', '语', '又', '称', '华', '语', '[', '3', ']', '、', '唐', '话', '[', '4', ']', '，', '概', '指', '由', '上', '古', '汉', '语', '（', '先', '秦', '雅', '言', '）', '发', '展', '而', '来', '、', '书', '面', '使', '用', '汉', '字', '的', '分', '析', '语', '，', '为', '汉', '藏', '语', '系', '最', '大', '的', '一', '支', '语', '族', '。']
        else:
            word_tokenizer_skipped = True
    elif lang == 'zho_tw':
        if word_tokenizer == 'jieba_zho':
            assert tokens == ['漢語', '又', '稱華語', '[', '3', ']', '、', '唐話', '[', '4', ']', '，', '概指', '由', '上古', '漢語', '（', '先秦', '雅言', '）', '發展', '而', '來', '、', '書面', '使用', '漢字', '的', '分析', '語', '，', '為漢藏', '語系', '最大', '的', '一支', '語族', '。']
        elif word_tokenizer == 'pkuseg_zho':
            assert tokens == ['漢語', '又', '稱華', '語[', '3', ']', '、', '唐', '話[', '4]', '，', '概指', '由', '上古', '漢語', '（', '先秦', '雅言', '）', '發展', '而', '來', '、', '書面', '使用', '漢字', '的', '分析', '語', '，', '為漢', '藏語系', '最', '大', '的', '一', '支', '語族', '。']
        elif word_tokenizer == 'spacy_zho':
            assert tokens == ['漢語', '又', '稱華', '語[', '3', ']', '、', '唐話[', '4', ']', '，', '概指', '由', '上古', '漢語', '（', '先', '秦雅言', '）', '發展', '而', '來', '、', '書面', '使用', '漢字', '的', '分析語', '，', '為漢', '藏語', '系', '最', '大', '的', '一', '支', '語族', '。']
        elif word_tokenizer == 'wordless_zho_char':
            assert tokens == ['漢', '語', '又', '稱', '華', '語', '[', '3', ']', '、', '唐', '話', '[', '4', ']', '，', '概', '指', '由', '上', '古', '漢', '語', '（', '先', '秦', '雅', '言', '）', '發', '展', '而', '來', '、', '書', '面', '使', '用', '漢', '字', '的', '分', '析', '語', '，', '為', '漢', '藏', '語', '系', '最', '大', '的', '一', '支', '語', '族', '。']
        else:
            word_tokenizer_skipped = True
    elif lang == 'hrv':
        assert tokens == ['Hrvatski', 'jezik', '(', 'ISO', '639', '-', '3', ':', 'hrv', 'Inačica', 'izvorne', 'stranice', 'arhivirana', '18', '.', 'rujna', '2012', '.', ')', 'skupni', 'je', 'naziv', 'za', 'nacionalni', 'standardni', 'jezik', 'Hrvata', ',', 'te', 'za', 'skup', 'narječja', 'i', 'govora', 'kojima', 'govore', 'ili', 'su', 'nekada', 'govorili', 'Hrvati', '.']
    elif lang == 'ces':
        assert tokens == ['Čeština', 'neboli', 'český', 'jazyk', 'je', 'západoslovanský', 'jazyk', ',', 'nejbližší', 'slovenštině', ',', 'poté', 'lužické', 'srbštině', 'a', 'polštině', '.']
    elif lang == 'dan':
        assert tokens == ['Dansk', 'er', 'et', 'østnordisk', 'sprog', 'indenfor', 'den', 'germanske', 'gren', 'af', 'den', 'indoeuropæiske', 'sprogfamilie', '.']
    elif lang == 'nld':
        assert tokens == ['Het', 'Nederlands', 'is', 'een', 'West-Germaanse', 'taal', 'en', 'de', 'officiële', 'taal', 'van', 'Nederland', ',', 'Suriname', 'en', 'een', 'van', 'de', 'drie', 'officiële', 'talen', 'van', 'België', '.']
    elif lang.startswith('eng_') or lang == 'other':
        if word_tokenizer == 'nltk_nist':
            assert tokens == ['English', 'is', 'a', 'West', 'Germanic', 'language', 'of', 'the', 'Indo', '-', 'European', 'language', 'family', ',', 'originally', 'spoken', 'by', 'the', 'inhabitants', 'of', 'early', 'medieval', 'England', '.', '[3]', '[', '4]', '[', '5]']
        elif word_tokenizer in ['nltk_nltk', 'nltk_penn_treebank']:
            assert tokens == ['English', 'is', 'a', 'West', 'Germanic', 'language', 'of', 'the', 'Indo-European', 'language', 'family', ',', 'originally', 'spoken', 'by', 'the', 'inhabitants', 'of', 'early', 'medieval', 'England.', '[', '3', ']', '[', '4', ']', '[', '5', ']']
        elif word_tokenizer == 'nltk_regex':
            assert tokens == ['English', 'is', 'a', 'West', 'Germanic', 'language', 'of', 'the', 'Indo', '-', 'European', 'language', 'family', ',', 'originally', 'spoken', 'by', 'the', 'inhabitants', 'of', 'early', 'medieval', 'England', '.[', '3', '][', '4', '][', '5', ']']
        elif word_tokenizer == 'nltk_tok_tok':
            assert tokens == ['English', 'is', 'a', 'West', 'Germanic', 'language', 'of', 'the', 'Indo-European', 'language', 'family', ',', 'originally', 'spoken', 'by', 'the', 'inhabitants', 'of', 'early', 'medieval', 'England.[', '3', ']', '[', '4', ']', '[', '5', ']']
        elif word_tokenizer in ['nltk_twitter', 'sacremoses_moses']:
            assert tokens == ['English', 'is', 'a', 'West', 'Germanic', 'language', 'of', 'the', 'Indo-European', 'language', 'family', ',', 'originally', 'spoken', 'by', 'the', 'inhabitants', 'of', 'early', 'medieval', 'England', '.', '[', '3', ']', '[', '4', ']', '[', '5', ']']
        elif word_tokenizer == 'spacy_eng':
            assert tokens == ['English', 'is', 'a', 'West', 'Germanic', 'language', 'of', 'the', 'Indo', '-', 'European', 'language', 'family', ',', 'originally', 'spoken', 'by', 'the', 'inhabitants', 'of', 'early', 'medieval', 'England.[3][4][5', ']']
        else:
            word_tokenizer_skipped = True
    elif lang == 'est':
        assert tokens == ['Eesti', 'keel', '(', 'varasem', 'nimetus', 'maakeel', ')', 'on', 'läänemeresoome', 'lõunarühma', 'kuuluv', 'keel', '.']
    elif lang == 'fin':
        assert tokens == ['Suomen', 'kieli', '(', 'suomi', ')', 'on', 'uralilaisten', 'kielten', 'itämerensuomalaiseen', 'ryhmään', 'kuuluva', 'kieli', ',', 'jota', 'puhuvat', 'pääosin', 'suomalaiset', '.']
    elif lang == 'fra':
        assert tokens == ['Le', 'français', 'est', 'une', 'langue', 'indo-européenne', 'de', 'la', 'famille', 'des', 'langues', 'romanes', 'dont', 'les', 'locuteurs', 'sont', 'appelés', 'francophones', ',', 'également', 'surnommé', 'la', 'langue', 'de', 'Molière', '.']
    elif lang.startswith('deu_'):
        if word_tokenizer == 'nltk_tok_tok':
            assert tokens == ['Die', 'deutsche', 'Sprache', 'bzw.', 'Deutsch', '(', '[', 'dɔɪ̯tʃ', ']', ';', '[', '26', ']', 'abgekürzt', 'dt', '.', 'oder', 'dtsch.', ')', 'ist', 'eine', 'westgermanische', 'Sprache', ',', 'die', 'weltweit', 'etwa', '90', 'bis', '105', 'Millionen', 'Menschen', 'als', 'Muttersprache', 'und', 'weiteren', 'rund', '80', 'Millionen', 'als', 'Zweit-', 'oder', 'Fremdsprache', 'dient', '.']
        elif word_tokenizer == 'sacremoses_moses':
            assert tokens == ['Die', 'deutsche', 'Sprache', 'bzw.', 'Deutsch', '(', '[', 'dɔɪ', '̯', 'tʃ', ']', ';', '[', '26', ']', 'abgekürzt', 'dt', '.', 'oder', 'dtsch', '.', ')', 'ist', 'eine', 'westgermanische', 'Sprache', ',', 'die', 'weltweit', 'etwa', '90', 'bis', '105', 'Millionen', 'Menschen', 'als', 'Muttersprache', 'und', 'weiteren', 'rund', '80', 'Millionen', 'als', 'Zweit-', 'oder', 'Fremdsprache', 'dient', '.']
        elif word_tokenizer == 'spacy_deu':
            assert tokens == ['Die', 'deutsche', 'Sprache', 'bzw.', 'Deutsch', '(', '[', 'dɔɪ̯tʃ];[26', ']', 'abgekürzt', 'dt', '.', 'oder', 'dtsch', '.', ')', 'ist', 'eine', 'westgermanische', 'Sprache', ',', 'die', 'weltweit', 'etwa', '90', 'bis', '105', 'Millionen', 'Menschen', 'als', 'Muttersprache', 'und', 'weiteren', 'rund', '80', 'Millionen', 'als', 'Zweit-', 'oder', 'Fremdsprache', 'dient', '.']
        else:
            word_tokenizer_skipped = True
    elif lang == 'grc':
        assert tokens == ['Ὅτι', 'μὲν', 'ὑμεῖς', ',', 'ὦ', 'ἄνδρες', 'Ἀθηναῖοι', ',', 'πεπόνθατε', 'ὑπὸ', 'τῶν', 'ἐμῶν', 'κατηγόρων', ',', 'οὐκ', 'οἶδα', '·', 'ἐγὼ', "δ'", 'οὖν', 'καὶ', 'αὐτὸς', "ὑπ'", 'αὐτῶν', 'ὀλίγου', 'ἐμαυτοῦ', 'ἐπελαθόμην', ',', 'οὕτω', 'πιθανῶς', 'ἔλεγον', '.']
    elif lang == 'ell':
        if word_tokenizer == 'sacremoses_moses':
            assert tokens == ['Η', 'ελληνική', 'γλώσσα', 'ανήκει', 'στην', 'ινδοευρωπαϊκή', 'οικογένεια', '[', '9', ']', 'και', 'αποτελεί', 'το', 'μοναδικό', 'μέλος', 'του', 'ελληνικού', 'κλάδου', ',', 'ενώ', 'είναι', 'η', 'επίσημη', 'γλώσσα', 'της', 'Ελλάδας', 'και', 'της', 'Κύπρου', '.']
        elif word_tokenizer == 'spacy_ell':
            assert tokens == ['Η', 'ελληνική', 'γλώσσα', 'ανήκει', 'στην', 'ινδοευρωπαϊκή', 'οικογένεια[9', ']', 'και', 'αποτελεί', 'το', 'μοναδικό', 'μέλος', 'του', 'ελληνικού', 'κλάδου', ',', 'ενώ', 'είναι', 'η', 'επίσημη', 'γλώσσα', 'της', 'Ελλάδας', 'και', 'της', 'Κύπρου', '.']
        else:
            word_tokenizer_skipped = True
    elif lang == 'guj':
        if word_tokenizer == 'sacremoses_moses':
            assert tokens == ['ગુજરાતી', '\u200d', '(', '/', 'ɡʊdʒəˈrɑːti', '/', '[', '૭', ']', ',', 'રોમન', 'લિપિમાં', ':', 'Gujarātī', ',', 'ઉચ્ચાર', ':', '[', 'ɡudʒəˈɾɑːtiː', ']', ')', 'ભારત', 'દેશના', 'ગુજરાત', 'રાજ્યની', 'ઇન્ડો-આર્યન', 'ભાષા', 'છે', ',', 'અને', 'મુખ્યત્વે', 'ગુજરાતી', 'લોકો', 'દ્વારા', 'બોલાય', 'છે', '.']
        elif word_tokenizer == 'spacy_guj':
            assert tokens == ['ગુજરાતી', '\u200d(/ɡʊdʒəˈrɑːti/[૭', ']', ',', 'રોમન', 'લિપિમાં', ':', 'Gujarātī', ',', 'ઉચ્ચાર', ':', '[', 'ɡudʒəˈɾɑːtiː', ']', ')', 'ભારત', 'દેશના', 'ગુજરાત', 'રાજ્યની', 'ઇન્ડો-આર્યન', 'ભાષા', 'છે', ',', 'અને', 'મુખ્યત્વે', 'ગુજરાતી', 'લોકો', 'દ્વારા', 'બોલાય', 'છે.']
        else:
            word_tokenizer_skipped = True
    elif lang == 'heb':
        assert tokens == ['עִבְרִית', '(', 'נקראת', 'גם', 'בשם', ':', 'עברית', 'מודרנית', ')', 'היא', 'שפה', 'שמית', ',', 'ממשפחת', 'השפות', 'האפרו', '-', 'אסיאתיות', ',', 'הידועה', 'כשפתם', 'של', 'היהודים', 'ושל', 'השומרונים', '.']
    elif lang == 'hin':
        assert tokens == ['हिन्दी', 'या', 'हिंदी', 'जिसके', 'मानकीकृत', 'रूप', 'को', 'मानक', 'हिंदी', 'कहा', 'जाता', 'है', ',', 'विश्व', 'की', 'एक', 'प्रमुख', 'भाषा', 'है', 'एवं', 'भारत', 'की', 'एक', 'राजभाषा', 'है', '।']
    elif lang == 'hun':
        assert tokens == ['A', 'magyar', 'nyelv', 'az', 'uráli', 'nyelvcsalád', 'tagja', ',', 'a', 'finnugor', 'nyelvek', 'közé', 'tartozó', 'ugor', 'nyelvek', 'egyike', '.']
    elif lang == 'isl':
        if word_tokenizer == 'sacremoses_moses':
            assert tokens == ['Íslenska', 'er', 'vesturnorrænt', ',', 'germanskt', 'og', 'indóevrópskt', 'tungumál', 'sem', 'er', 'einkum', 'talað', 'og', 'ritað', 'á', 'Íslandi', 'og', 'er', 'móðurmál', 'langflestra', 'Íslendinga', '.', '[', '4', ']']
        elif word_tokenizer == 'spacy_isl':
            assert tokens == ['Íslenska', 'er', 'vesturnorrænt', ',', 'germanskt', 'og', 'indóevrópskt', 'tungumál', 'sem', 'er', 'einkum', 'talað', 'og', 'ritað', 'á', 'Íslandi', 'og', 'er', 'móðurmál', 'langflestra', 'Íslendinga.[4', ']']
        else:
            word_tokenizer_skipped = True
    elif lang == 'ind':
        assert tokens == ['Bahasa', 'Indonesia', 'adalah', 'bahasa', 'nasional', 'dan', 'resmi', 'di', 'seluruh', 'Indonesia', '.']
    elif lang == 'gle':
        assert tokens == ['Is', 'ceann', 'de', 'na', 'teangacha', 'Ceilteacha', 'í', 'an', 'Ghaeilge', '(', 'nó', 'Gaeilge', 'na', 'hÉireann', 'mar', 'a', 'thugtar', 'uirthi', 'corruair', ')', ',', 'agus', 'ceann', 'den', 'dtrí', 'cinn', 'de', 'theangacha', 'Ceilteacha', 'ar', 'a', 'dtugtar', 'na', 'teangacha', 'Gaelacha', '(', 'Gaeilge', ',', 'Gaeilge', 'Mhanann', 'agus', 'Gaeilge', 'na', 'hAlban', ')', 'go', 'háirithe', '.']
    elif lang == 'ita':
        if word_tokenizer == 'sacremoses_moses':
            assert tokens == ["L'", 'italiano', '(', '[', 'itaˈljaːno', ']', '[', 'Nota', '1', ']', 'ascolta', '[', '?', '·', 'info', ']', ')', 'è', 'una', 'lingua', 'romanza', 'parlata', 'principalmente', 'in', 'Italia', '.']
        elif word_tokenizer == 'spacy_ita':
            assert tokens == ["L'", 'italiano', '(', '[', 'itaˈljaːno][Nota', '1', ']', 'ascolta[?·info', ']', ')', 'è', 'una', 'lingua', 'romanza', 'parlata', 'principalmente', 'in', 'Italia', '.']
        else:
            word_tokenizer_skipped = True
    elif lang == 'jpn':
        if word_tokenizer in [
            'spacy_jpn',
            'sudachipy_jpn_split_mode_a'
        ]:
            assert tokens == ['日本', '語', '（', 'にほん', 'ご', '、', 'にっぽん', 'ご', '[', '注', '2', ']', '）', 'は', '、', '日本', '国', '内', 'や', '、', 'かつて', 'の', '日本', '領', 'だっ', 'た', '国', '、', 'そして', '日本', '人', '同士', 'の', '間', 'で', '使用', 'さ', 'れ', 'て', 'いる', '言語', '。']
        elif word_tokenizer in [
            'sudachipy_jpn_split_mode_b',
            'sudachipy_jpn_split_mode_c'
        ]:
            assert tokens == ['日本語', '（', 'にほん', 'ご', '、', 'にっぽん', 'ご', '[', '注', '2', ']', '）', 'は', '、', '日本', '国', '内', 'や', '、', 'かつて', 'の', '日本', '領', 'だっ', 'た', '国', '、', 'そして', '日本人', '同士', 'の', '間', 'で', '使用', 'さ', 'れ', 'て', 'いる', '言語', '。']
        elif word_tokenizer == 'wordless_jpn_kanji':
            assert tokens == ['日', '本', '語', '（', 'にほんご', '、', 'にっぽん', 'ご', '[', '注', '2', ']', '）', 'は', '、', '日', '本', '国', '内', 'や', '、', 'かつて', 'の', '日', '本', '領', 'だっ', 'た', '国', '、', 'そして', '日', '本', '人', '同', '士', 'の', '間', 'で', '使', '用', 'さ', 'れ', 'て', 'いる', '言', '語', '。']
        else:
            word_tokenizer_skipped = True
    elif lang == 'kan':
        assert tokens == ['ದ್ರಾವಿಡ', 'ಭಾಷೆಗಳಲ್ಲಿ', 'ಪ್ರಾಮುಖ್ಯವುಳ್ಳ', 'ಭಾಷೆಯೂ', 'ಭಾರತದ', 'ಪುರಾತನವಾದ', 'ಭಾಷೆಗಳಲ್ಲಿ', 'ಒಂದೂ', 'ಆಗಿರುವ', 'ಕನ್ನಡ', 'ಭಾಷೆಯನ್ನು', 'ಅದರ', 'ವಿವಿಧ', 'ರೂಪಗಳಲ್ಲಿ', 'ಸುಮಾರು', '೪೫', 'ದಶಲಕ್ಷ', 'ಜನರು', 'ಆಡು', 'ನುಡಿಯಾಗಿ', 'ಬಳಸುತ್ತಲಿದ್ದಾರೆ', '.']
    elif lang == 'kir':
        assert tokens == ['Кыргыз', 'тили', '—', 'Кыргыз', 'Республикасынын', 'мамлекеттик', 'тили', ',', 'түрк', 'тилдеринин', 'курамына', ',', 'анын', 'ичинде', 'кыргыз-кыпчак', 'же', 'тоо-алтай', 'тобуна', 'кирет', '.']
    elif lang == 'lav':
        if word_tokenizer == 'sacremoses_moses':
            assert tokens == ['Latviešu', 'valoda', 'ir', 'dzimtā', 'valoda', 'apmēram', '1,7', 'miljoniem', 'cilvēku', ',', 'galvenokārt', 'Latvijā', ',', 'kur', 'tā', 'ir', 'vienīgā', 'valsts', 'valoda', '.', '[', '3', ']']
        elif word_tokenizer == 'spacy_lav':
            assert tokens == ['Latviešu', 'valoda', 'ir', 'dzimtā', 'valoda', 'apmēram', '1,7', 'miljoniem', 'cilvēku', ',', 'galvenokārt', 'Latvijā', ',', 'kur', 'tā', 'ir', 'vienīgā', 'valsts', 'valoda.[3', ']']
        else:
            word_tokenizer_skipped = True
    elif lang == 'lij':
        assert tokens == ['O', 'Lìgure', '(', 'in', 'monegasco', ':', 'lenga', 'ligüra', 'e', 'lenga', 'lìgura', ')', 'o', "l'", 'é', "'", 'na', 'lengoa[1', ']', 'do', 'gruppo', 'lengoìstego', 'itàlico', 'oçidentâ', 'parlâ', 'in', 'Italia', '(', 'Liguria', ',', 'Piemonte', ',', 'Emilia', '-', 'Romagna', 'e', 'Sardegna', ')', ',', 'into', 'sud', 'da', 'Fransa', ',', 'in', 'Còrsega', ',', 'e', 'into', 'Prinçipato', 'de', 'Monego', '.']
    elif lang == 'lit':
        assert tokens == ['Lietuvių', 'kalba', '–', 'iš', 'baltų', 'prokalbės', 'kilusi', 'lietuvių', 'tautos', 'kalba', ',', 'kuri', 'Lietuvoje', 'yra', 'valstybinė', ',', 'o', 'Europos', 'Sąjungoje', '–', 'viena', 'iš', 'oficialiųjų', 'kalbų', '.']
    elif lang == 'ltz':
        assert tokens == ["D'", 'Lëtzebuergesch', 'gëtt', 'an', 'der', 'däitscher', 'Dialektologie', 'als', 'ee', 'westgermaneschen', ',', 'mëtteldäitschen', 'Dialekt', 'aklasséiert', ',', 'deen', 'zum', 'Muselfränkesche', 'gehéiert', '.']
    elif lang == 'mkd':
        assert tokens == ['Македонски', 'јазик', '—', 'јужнословенски', 'јазик', ',', 'дел', 'од', 'групата', 'на', 'словенски', 'јазици', 'од', 'јазичното', 'семејство', 'на', 'индоевропски', 'јазици', '.']
    elif lang == 'mal':
        if word_tokenizer == 'sacremoses_moses':
            assert tokens == ['ഇന്ത്യയിൽ', 'കേരള', 'സംസ്ഥാനത്തിലും', 'കേന്ദ്രഭരണപ്രദേശങ്ങളായ', 'ലക്ഷദ്വീപിലും', 'പുതുച്ചേരിയുടെ', 'ഭാഗമായ', 'മയ്യഴിയിലും', 'തമിഴ്നാട്ടിലെ', 'കന്യാകുമാരി', 'ജില്ലയിലും', 'നീലഗിരി', 'ജില്ലയിലെ', 'ഗൂഡല്ലൂർ', 'താലൂക്കിലും', 'സംസാരിക്കപ്പെടുന്ന', 'ഭാഷയാണ്', 'മലയാളം', '.']
        elif word_tokenizer == 'spacy_mal':
            assert tokens == ['ഇന്ത്യയിൽ', 'കേരള', 'സംസ്ഥാനത്തിലും', 'കേന്ദ്രഭരണപ്രദേശങ്ങളായ', 'ലക്ഷദ്വീപിലും', 'പുതുച്ചേരിയുടെ', 'ഭാഗമായ', 'മയ്യഴിയിലും', 'തമിഴ്നാട്ടിലെ', 'കന്യാകുമാരി', 'ജില്ലയിലും', 'നീലഗിരി', 'ജില്ലയിലെ', 'ഗൂഡല്ലൂർ', 'താലൂക്കിലും', 'സംസാരിക്കപ്പെടുന്ന', 'ഭാഷയാണ്', 'മലയാളം.']
        else:
            word_tokenizer_skipped = True
    elif lang == 'mar':
        if word_tokenizer == 'sacremoses_moses':
            assert tokens == ['मराठी', 'भाषा', 'ही', 'इंडो-युरोपीय', 'भाषाकुळातील', 'एक', 'भाषा', 'आहे', '.']
        elif word_tokenizer == 'spacy_mar':
            assert tokens == ['मराठी', 'भाषा', 'ही', 'इंडो', '-', 'युरोपीय', 'भाषाकुळातील', 'एक', 'भाषा', 'आहे', '.']
        else:
            word_tokenizer_skipped = True
    elif lang == 'mni':
        assert tokens == ['ꯃꯤꯇꯩꯂꯣꯟ', 'ꯍꯥꯏꯕꯁꯤ', 'ꯏꯟꯗꯤꯌꯥ', 'ꯑꯋꯥꯡ-ꯅꯣꯡꯄꯣꯛꯇ', 'ꯂꯩꯕ', 'ꯃꯅꯤꯄꯨꯔꯗ', 'ꯃꯔꯨꯑꯣꯏꯅ', 'ꯉꯥꯡꯅꯕ', 'ꯇꯤꯕꯦꯇꯣ-ꯕꯔꯃꯟ', 'ꯀꯥꯡꯂꯨꯞꯇ', 'ꯆꯤꯡꯕ', 'ꯂꯣꯟ', 'ꯑꯃꯅꯤ', '꯫', 'ꯚꯥꯔꯠ', 'ꯂꯩꯉꯥꯛꯅꯥ', 'ꯁꯛꯈꯪꯂꯕ', 'ꯂꯣꯟ', '꯲꯲', 'ꯁꯤꯡꯒꯤ', 'ꯃꯅꯨꯡꯗ', 'ꯃꯤꯇꯩꯂꯣꯟꯁꯤꯁꯨ', 'ꯑꯃꯅꯤ', '꯫', 'ꯃꯤꯇꯩꯂꯣꯟ', 'ꯑꯁꯤ', 'ꯏꯟꯗꯤꯌꯥꯒꯤ', 'ꯁ', '꯭', 'ꯇꯦꯠ', 'ꯑꯣꯏꯔꯤꯕ', 'ꯑꯁꯥꯝ', 'ꯑꯃꯁꯨꯡ', 'ꯇ', '꯭', 'ꯔꯤꯄꯨꯔꯥ', 'ꯑꯃꯗꯤ', 'ꯑꯇꯩ', 'ꯂꯩꯕꯥꯛꯁꯤꯡꯗ', 'ꯍꯥꯏꯕꯗꯤ', 'ꯕꯥꯡꯂꯥꯗꯦꯁ', 'ꯑꯃꯁꯨꯡ', 'ꯑꯋꯥꯗꯁꯨ', 'ꯉꯥꯡꯅꯩ', '꯫', 'ꯏꯪ', 'ꯀꯨꯝꯖ', '꯲꯰꯱꯱', 'ꯒꯤ', 'ꯃꯤꯀꯣꯛ', 'ꯊꯤꯕꯗ', 'ꯃꯤꯇꯩꯂꯣꯟꯕꯨ', 'ꯏꯃꯥꯂꯣꯟ', 'ꯑꯣꯢꯅ', 'ꯉꯥꯡꯕꯒꯤ', 'ꯃꯤꯁꯤꯡ', 'ꯂꯤꯆꯥ', '꯱꯸', 'ꯃꯨꯛ', 'ꯁꯨꯢ', '꯫']
    elif lang == 'nep':
        assert tokens == ['नेपाली', 'भाषा', '(', 'अन्तर्राष्ट्रिय', 'ध्वन्यात्मक', 'वर्णमाला', '[', 'neˈpali', 'bʱaʂa', ']', ')', 'नेपालको', 'सम्पर्क', 'भाषा', 'तथा', 'भारत', ',', 'भुटान', 'र', 'म्यानमारको', 'केही', 'भागमा', 'मातृभाषाको', 'रूपमा', 'बोलिने', 'भाषा', 'हो', '।']
    elif lang == 'nob':
        assert tokens == ['Bokmål', 'er', 'en', 'varietet', 'av', 'norsk', 'språk', '.']
    elif lang == 'ori':
        assert tokens == ['ଓଡ଼ିଆ', '(', 'ଇଂରାଜୀ', 'ଭାଷାରେ', 'Odia', '/', 'əˈdiːə', '/', 'or', 'Oriya', '/', 'ɒˈriːə', '/', ',', ')', 'ଏକ', 'ଭାରତୀୟ', 'ଭାଷା', 'ଯାହା', 'ଏକ', 'ଇଣ୍ଡୋ-ଇଉରୋପୀୟ', 'ଭାଷାଗୋଷ୍ଠୀ', 'ଅନ୍ତର୍ଗତ', 'ଇଣ୍ଡୋ-ଆର୍ଯ୍ୟ', 'ଭାଷା', '।']
    elif lang == 'fas':
        assert tokens == ['فارسی', 'یا', 'پارسی', 'یک', 'زبان', 'ایرانی', 'غربی', 'از', 'زیرگروه', 'ایرانی', 'شاخهٔ', 'هندوایرانیِ', 'خانوادهٔ', 'زبان\u200cهای', 'هندواروپایی', 'است', 'که', 'در', 'کشورهای', 'ایران', '،', 'افغانستان', '،', 'تاجیکستان', '،', 'ازبکستان', '،', 'پاکستان', '،', 'عراق', '،', 'ترکمنستان', 'و', 'آذربایجان', 'به', 'آن', 'سخن', 'می\u200cگویند', '.']
    elif lang == 'pol':
        assert tokens == ['Język', 'polski', ',', 'polszczyzna', '–', 'język', 'lechicki', 'z', 'grupy', 'zachodniosłowiańskiej', '(', 'do', 'której', 'należą', 'również', 'czeski', ',', 'kaszubski', ',', 'słowacki', 'i', 'języki', 'łużyckie', ')', ',', 'stanowiącej', 'część', 'rodziny', 'indoeuropejskiej', '.']
    elif lang.startswith('por_'):
        assert tokens == ['A', 'língua', 'portuguesa', ',', 'também', 'designada', 'português', ',', 'é', 'uma', 'língua', 'indo-europeia', 'românica', 'flexiva', 'ocidental', 'originada', 'no', 'galego-português', 'falado', 'no', 'Reino', 'da', 'Galiza', 'e', 'no', 'norte', 'de', 'Portugal', '.']
    elif lang == 'pan_guru':
        assert tokens == ['ਪੰਜਾਬੀ', 'ਭਾਸ਼ਾ', '/', 'pʌnˈdʒɑːbi', '/', '(', 'ਸ਼ਾਹਮੁਖੀ', ':', '\u200e', 'پنجابی', '\u200e', ')', '(', 'ਗੁਰਮੁਖੀ', ':', 'ਪੰਜਾਬੀ', ')', 'ਪੰਜਾਬ', 'ਦੀ', 'ਭਾਸ਼ਾ', ',', 'ਜਿਸ', 'ਨੂੰ', 'ਪੰਜਾਬ', 'ਖੇਤਰ', 'ਦੇ', 'ਵਸਨੀਕ', 'ਜਾਂ', 'ਸੰਬੰਧਿਤ', 'ਲੋਕ', 'ਬੋਲਦੇ', 'ਹਨ', '।', '[', '1', ']']
    elif lang == 'ron':
        assert tokens == ['Limba', 'română', 'este', 'o', 'limbă', 'indo-europeană', ',', 'din', 'grupul', 'italic', 'și', 'din', 'subgrupul', 'oriental', 'al', 'limbilor', 'romanice', '.']
    elif lang == 'rus':
        if word_tokenizer == 'nltk_tok_tok':
            assert tokens == ['Ру́сский', 'язы́к', '(', '[', 'ˈruskʲɪi̯', 'jɪˈzɨk', ']', 'Информация', 'о', 'файле', 'слушать', ')', '[', '~', '3', ']', '[', '⇨', ']', '—', 'один', 'из', 'восточнославянских', 'языков', ',', 'национальный', 'язык', 'русского', 'народа', '.']
        elif word_tokenizer == 'sacremoses_moses':
            assert tokens == ['Ру', '́', 'сский', 'язы', '́', 'к', '(', '[', 'ˈruskʲɪi', '̯', 'jɪˈzɨk', ']', 'Информация', 'о', 'файле', 'слушать', ')', '[', '~', '3', ']', '[', '⇨', ']', '—', 'один', 'из', 'восточнославянских', 'языков', ',', 'национальный', 'язык', 'русского', 'народа', '.']
        elif word_tokenizer == 'spacy_rus':
            assert tokens == ['Ру́сский', 'язы́к', '(', '[', 'ˈruskʲɪi̯', 'jɪˈzɨk', ']', 'Информация', 'о', 'файле', 'слушать)[~', '3', ']', '[', '⇨', ']', '—', 'один', 'из', 'восточнославянских', 'языков', ',', 'национальный', 'язык', 'русского', 'народа', '.']
        else:
            word_tokenizer_skipped = True
    elif lang == 'san':
        assert tokens == ['संस्कृतम्', 'जगतः', 'एकतमा', 'अतिप्राचीना', 'समृद्धा', 'शास्त्रीया', 'च', 'भाषासु', 'वर्तते', '।']
    elif lang == 'srp_cyrl':
        assert tokens == ['Српски', 'језик', 'припада', 'словенској', 'групи', 'језика', 'породице', 'индоевропских', 'језика.[12', ']']
    elif lang == 'srp_latn':
        assert tokens == ['Srpski', 'jezik', 'pripada', 'slovenskoj', 'grupi', 'jezika', 'porodice', 'indoevropskih', 'jezika.[12', ']']
    elif lang == 'sin':
        assert tokens == ['ශ්\u200dරී', 'ලංකාවේ', 'ප්\u200dරධාන', 'ජාතිය', 'වන', 'සිංහල', 'ජනයාගේ', 'මව්', 'බස', 'සිංහල', 'වෙයි', '.']
    elif lang == 'slk':
        assert tokens == ['Slovenčina', 'patrí', 'do', 'skupiny', 'západoslovanských', 'jazykov', '(', 'spolu', 's', 'češtinou', ',', 'poľštinou', ',', 'hornou', 'a', 'dolnou', 'lužickou', 'srbčinou', 'a', 'kašubčinou', ')', '.']
    elif lang == 'slv':
        assert tokens == ['Slovenščina', '[', 'sloˈʋenʃtʃina', ']', 'je', 'združeni', 'naziv', 'za', 'uradni', 'knjižni', 'jezik', 'Slovencev', 'in', 'skupno', 'ime', 'za', 'narečja', 'in', 'govore', ',', 'ki', 'jih', 'govorijo', 'ali', 'so', 'jih', 'nekoč', 'govorili', 'Slovenci', '.']
    elif lang == 'dsb':
        assert tokens == ['Dolnoserbšćina', ',', 'dolnoserbska', 'rěc', '(', 'nimski', 'Niedersorbisch', 'abo', 'teke', 'Wendisch', ',', 'pólski', 'język', 'dolnołużycki', ',', 'česki', 'dolnolužická', 'srbština', ')', 'jo', 'jadna', 'z', 'dweju', 'rěcowu', 'Serbow', ',', 'kotaraž', 'se', 'wužywa', 'w', 'Dolnej', 'Łužycy', ',', 'w', 'pódpołdnjowej', 'Bramborskej', ',', 'na', 'pódzajtšu', 'Nimskej', '.']
    elif lang == 'hsb':
        assert tokens == ['Hornjoserbšćina', 'je', 'zapadosłowjanska', 'rěč', ',', 'kotraž', 'so', 'w', 'Hornjej', 'Łužicy', 'wokoło', 'městow', 'Budyšin', ',', 'Kamjenc', 'a', 'Wojerecy', 'rěči', '.']
    elif lang == 'spa':
        assert tokens == ['El', 'español', 'o', 'castellano', 'es', 'una', 'lengua', 'romance', 'procedente', 'del', 'latín', 'hablado', ',', 'perteneciente', 'a', 'la', 'familia', 'de', 'lenguas', 'indoeuropeas', '.']
    elif lang == 'swe':
        assert tokens == ['Svenska', '(', 'svenska', '(', 'info', ')', ')', 'är', 'ett', 'östnordiskt', 'språk', 'som', 'talas', 'av', 'ungefär', 'tio', 'miljoner', 'personer', 'främst', 'i', 'Sverige', 'där', 'språket', 'har', 'en', 'dominant', 'ställning', 'som', 'huvudspråk', ',', 'men', 'även', 'som', 'det', 'ena', 'nationalspråket', 'i', 'Finland', 'och', 'som', 'enda', 'officiella', 'språk', 'på', 'Åland', '.']
    elif lang == 'tgl':
        assert tokens == ['Ang', 'wikang', 'Tagalog[1', ']', '(', 'Baybayin', ':', 'ᜏᜒᜃᜆᜄᜎᜓ', ')', ',', 'o', 'ang', 'Tagalog', ',', 'ay', 'isa', 'sa', 'mga', 'pinakaginagamit', 'na', 'wika', 'ng', 'Pilipinas', '.']
    elif lang == 'tgk':
        assert tokens == ['Забони', 'тоҷикӣ', '—', 'забоне', ',', 'ки', 'дар', 'Эрон', ':', 'форсӣ', ',', 'ва', 'дар', 'Афғонистон', 'дарӣ', 'номида', 'мешавад', ',', 'забони', 'давлатии', 'кишварҳои', 'Тоҷикистон', ',', 'Эрон', 'ва', 'Афғонистон', 'мебошад', '.']
    elif lang == 'tam':
        assert tokens == ['தமிழ்', '(', 'Tamil', 'language', ')', 'தமிழர்களினதும்', 'தமிழ்', 'பேசும்', 'பலரின்', 'தாய்மொழி', 'ஆகும்', '.']
    elif lang == 'tat':
        assert tokens == ['Татар', 'теле', '—', 'татарларның', 'милли', 'теле', ',', 'Татарстанның', 'дәүләт', 'теле', ',', 'таралышы', 'буенча', 'Россиядә', 'икенче', 'тел', '.']
    elif lang == 'tel':
        assert tokens == ['తెలుగు', 'అనేది', 'ద్రావిడ', 'భాషల', 'కుటుంబానికి', 'చెందిన', 'భాష', '.']
    elif lang == 'tdt':
        assert tokens == ['Tetun', '(', 'iha', 'portugés', ':', 'tétum', ';', 'iha', 'inglés', ':', 'Tetum', ')', 'ne', "'", 'e', 'lian', 'nasionál', 'no', 'ko-ofisiál', 'Timór', 'Lorosa', "'", 'e', 'nian', '.']
    elif lang == 'tha':
        if word_tokenizer in [
            'pythainlp_longest_matching',
            'pythainlp_max_matching_tcc'
        ]:
            assert tokens == ['ภาษาไทย', 'หรือ', 'ภาษาไทย', 'กลาง', 'เป็น', 'ภาษา', 'ใน', 'กลุ่ม', 'ภาษา', 'ไท', 'ซึ่ง', 'เป็น', 'กลุ่มย่อย', 'ของ', 'ตระกูล', 'ภาษา', 'ข', 'ร้า', '-', 'ไท', 'และ', 'เป็น', 'ภาษาราชการ', 'และ', 'ภาษาประจำชาติ', 'ของ', 'ประเทศ', 'ไทย', '[', '3', '][', '4', ']']
        elif word_tokenizer == 'pythainlp_max_matching':
            assert tokens == ['ภาษาไทย', 'หรือ', 'ภาษาไทยกลาง', 'เป็น', 'ภาษา', 'ใน', 'กลุ่ม', 'ภาษา', 'ไท', 'ซึ่ง', 'เป็น', 'กลุ่มย่อย', 'ของ', 'ตระกูล', 'ภาษา', 'ข', 'ร้า', '-', 'ไท', 'และ', 'เป็น', 'ภาษาราชการ', 'และ', 'ภาษาประจำชาติ', 'ของ', 'ประเทศ', 'ไทย', '[', '3', '][', '4', ']']
        elif word_tokenizer == 'pythainlp_nercut':
            assert tokens == ['ภาษาไทย', 'หรือ', 'ภาษาไทย', 'กลาง', 'เป็น', 'ภาษา', 'ใน', 'กลุ่ม', 'ภาษา', 'ไท', 'ซึ่ง', 'เป็น', 'กลุ่มย่อย', 'ของ', 'ตระกูลภาษาขร้า', '-', 'ไท', 'และ', 'เป็น', 'ภาษาราชการ', 'และ', 'ภาษาประจำชาติ', 'ของ', 'ประเทศ', 'ไทย', '[', '3][4]']
        else:
            word_tokenizer_skipped = True
    elif lang == 'bod':
        assert tokens == ['བོད་', 'ཀྱི་', 'སྐད་ཡིག་', 'ནི་', 'བོད་ཡུལ་', 'དང་', 'དེ', 'འི་', 'ཉེ་འཁོར་', 'གྱི་', 'ས་ཁུལ་', 'ཏེ', '།']
    elif lang == 'tir':
        assert tokens == ['ትግርኛ', 'ኣብ', 'ኤርትራን', 'ኣብ', 'ሰሜናዊ', 'ኢትዮጵያን', 'ኣብ', 'ክልል', 'ትግራይ', 'ዝዝረብ', 'ሴማዊ', 'ቋንቋ', 'እዩ', '።']
    elif lang == 'tsn':
        assert tokens == ['Setswana', 'ke', 'teme', 'e', 'e', 'buiwang', 'mo', 'mafatsheng', 'a', 'Aforika', 'Borwa', ',', 'Botswana', ',', 'Namibia', 'le', 'Zimbabwe', '.']
    elif lang == 'tur':
        assert tokens == ['Türkçe', 'ya', 'da', 'Türk', 'dili', ',', 'Güneydoğu', 'Avrupa', 've', 'Batı', "Asya'da", 'konuşulan', ',', 'Türk', 'dilleri', 'dil', 'ailesine', 'ait', 'sondan', 'eklemeli', 'bir', 'dil.[12', ']']
    elif lang == 'ukr':
        assert tokens == ['Украї́нська', 'мо́ва', '(', 'МФА', ':', '[', 'ukrɑ̽ˈjɪnʲsʲkɑ̽', 'ˈmɔwɑ̽', ']', ',', 'історичні', 'назви', '—', 'ру́ська', ',', 'руси́нська[10][11][12', ']', '[', '*', '1', ']', ')', '—', 'національна', 'мова', 'українців', '.']
    elif lang == 'urd':
        assert tokens == ['اُردُو', 'یا', 'لشکری', 'زبان[8', ']', 'برصغیر', 'کی', 'معیاری', 'زبانوں', 'میں', 'سے', 'ایک', 'ہے', '۔']
    elif lang == 'vie':
        if word_tokenizer == 'nltk_tok_tok':
            assert tokens == ['Tiếng', 'Việt', ',', 'cũng', 'gọi', 'là', 'tiếng', 'Việt', 'Nam[', '9', ']', 'hay', 'Việt', 'ngữ', 'là', 'ngôn', 'ngữ', 'của', 'người', 'Việt', 'và', 'là', 'ngôn', 'ngữ', 'chính', 'thức', 'tại', 'Việt', 'Nam', '.']
        elif word_tokenizer == 'underthesea_vie':
            assert tokens == ['Tiếng', 'Việt', ',', 'cũng', 'gọi là', 'tiếng', 'Việt Nam', '[', '9 ]', 'hay', 'Việt ngữ', 'là', 'ngôn ngữ', 'của', 'người', 'Việt', 'và', 'là', 'ngôn ngữ', 'chính thức', 'tại', 'Việt Nam', '.']
        else:
            word_tokenizer_skipped = True
    elif lang == 'yor':
        assert tokens == ['Èdè', 'Yorùbá', 'Ni', 'èdè', 'tí', 'ó', 'ṣàkójọ', 'pọ̀', 'gbogbo', 'kú', 'oótu', 'o', '-', 'ò', '-', 'jíire', 'bí', ',', 'níapá', 'ìwọ̀', 'Oòrùn', 'ilẹ̀', 'Nàìjíríà', ',', 'tí', 'a', 'bá', 'wo', 'èdè', 'Yorùbá', ',', 'àwọn', 'onímọ̀', 'pín', 'èdè', 'náà', 'sábẹ́', 'ẹ̀yà', 'Kwa', 'nínú', 'ẹbí', 'èdè', 'Niger', '-', 'Congo', '.']
    else:
        raise Exception(f'Error: Tests for language "{lang}" is skipped!')

    if word_tokenizer_skipped:
        raise Exception(f'Error: Tests for word tokenizer "{word_tokenizer}" is skipped!')

if __name__ == '__main__':
    for lang, word_tokenizer in test_word_tokenizers:
        test_word_tokenize(lang, word_tokenizer)
