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

test_lemmatizers = []

for lang, lemmatizers in main.settings_global['lemmatizers'].items():
    for lemmatizer in lemmatizers:
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

    lemmas_long_text_tokenized = wl_lemmatization.wl_lemmatize(
        main,
        inputs = [str(i) for i in range(101) for j in range(50)],
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

    # Test long texts
    assert lemmas_long_text_tokenized == [str(i) for i in range(101) for j in range(50)]

    lemmatizer_skipped = False

    if lang == 'sqi':
        assert lemmas == ['gjuhë', 'shqip', '(', 'ose', 'thjesht', 'shqipe', ')', 'jam', 'gjuhë', 'jap', 'degë', 'ai', 'veçantë', 'ai', 'familje', 'indo', 'flas', 'evropiane', 'që', 'flitet', 'nga', 'rreth', '7', 'flas', '10', 'milionë', 'njeri', 'në', 'botë,[1', ']', 'kryesisht', 'në', 'Shqipëri', ',', 'Kosovë', 'jap', 'Maqedoninë', 'ai', 'veri', ',', 'por', 'edhe', 'në', 'zonë', 'ti', 'tjera', 'ti', 'Evropës', 'Juglindore', 'ku', 'kam', 'një', 'popullsi', 'shqiptar', ',', 'duk', 'përfshij', 'mal', 'ai', 'Zi', 'jap', 'luginë', 'ai', 'Preshevës', '.']
    elif lang == 'hye':
        assert lemmas == ['հայերեն', '(', 'ավանդական՝', 'հայերէն', ')', ',', 'հնդեվրոպական', 'լեզվաընտանիք', 'առանձին', 'ճյուղ', 'հանդիսացող', 'լեզու։']
    elif lang == 'ast':
        assert lemmas == ["L'asturianu", 'ser', 'un', 'llingua', 'romance', 'propiu', "d'Asturies,[1", ']', 'perteneciente', 'al', 'subgrupu', 'asturllionés', '.']
    elif lang == 'ben':
        assert lemmas == ['বাংলা', 'ভাষা', '(', 'বাঙলা', ',', 'বাঙ্গলা', ',', 'তথা', 'বাঙ্গালা', 'নামেও', 'পরিচিত', ')', 'একটি', 'ইন্দো', '-', 'আর্য', 'ভাষা', ',', 'যা', 'দক্ষিণ', 'এশিয়ার', 'বাঙালি', 'জাতির', 'প্রধান', 'কথ্য', 'ও', 'লেখ্য', 'ভাষা', '।']
    elif lang == 'bul':
        assert lemmas == ['бъ̀лгарският', 'езѝк', 'съм', 'индоевропейски', 'език', 'от', 'група', 'на', 'южнославянскит', 'език', '.']
    elif lang == 'cat':
        if lemmatizer == 'simplemma_cat':
            assert lemmas == ['ell', 'català', '(', 'denominació', 'oficial', 'a', 'Catalunya', ',', 'a', 'el', 'illa', 'balear', ',', 'a', 'Andorra', ',', 'a', 'el', 'ciutat', 'de', 'el', 'alguer', 'i', 'tradicional', 'a', 'Catalunya', 'd', 'ell', 'nord', ')', 'o', 'valencià', '(', 'denominació', 'oficial', 'a', 'litre', 'pair', 'valencià', 'i', 'tradicional', 'a', 'litre', 'Carxe', ')', 'ser', 'un', 'llengua', 'romànic', 'parlar', 'a', 'Catalunya', ',', 'ell', 'pair', 'valencià', '(', 'treure', 'de', 'algun', 'comarca', 'i', 'localitat', 'de', 'el', 'interior', ')', ',', 'el', 'illa', 'balear', ',', 'Andorra', ',', 'el', 'franjar', 'de', 'pondre', '(', 'a', 'el', 'Aragó', ')', ',', 'el', 'ciutat', 'de', 'el', 'alguer', '(', 'a', 'el', 'illa', 'de', 'Sardenya', ')', ',', 'el', 'Catalunya', 'd', 'ell', 'Nord,[8', ']', 'ell', 'Carxe', '(', 'un', 'petit', 'territori', 'de', 'Múrcia', 'poblar', 'per', 'poblador', 'valencians),[9][10', ']', 'i', 'en', 'comunitat', 'arreu', 'd', 'ell', 'món', '(', 'entrar', 'el', 'qual', 'destacar', 'el', 'de', 'el', 'argentí', ',', 'amb', '200.000', 'parlants).[11', ']']
        elif lemmatizer == 'spacy_cat':
            assert lemmas == ['el', 'català', '(', 'denominació', 'oficial', 'a', 'Catalunya', ',', 'a', 'el', 'Illes', 'Balears', ',', 'a', 'Andorra', ',', 'a', 'el', 'ciutat', 'de', 'el', 'Alguer', 'i', 'tradicional', 'a', 'Catalunya', 'de', 'el', 'Nord', ')', 'o', 'valencià', '(', 'denominació', 'oficial', 'a', 'el', 'País', 'Valencià', 'i', 'tradicional', 'a', 'el', 'Carxe', ')', 'ser', 'un', 'llengua', 'romànic', 'parlat', 'a', 'Catalunya', ',', 'el', 'País', 'Valencià', '(', 'tret', 'de', 'algun', 'comarca', 'i', 'localitat', 'de', 'el', 'interior', ')', ',', 'el', 'Illes', 'Balears', ',', 'Andorra', ',', 'el', 'Franja', 'de', 'Ponent', '(', 'a', 'el', 'Aragó', ')', ',', 'el', 'ciutat', 'de', 'el', 'Alguer', '(', 'a', 'el', 'illa', 'de', 'Sardenya', ')', ',', 'el', 'Catalunya', 'de', 'el', 'Nord,[8', ']', 'el', 'Carxe', '(', 'un', 'petit', 'territori', 'de', 'Múrcia', 'poblat', 'per', 'poblador', 'valencians),[9][10', ']', 'i', 'en', 'comunitat', 'arreu', 'de', 'el', 'món', '(', 'entre', 'el', 'qual', 'destacar', 'el', 'de', 'el', 'Argentina', ',', 'amb', '200.000', 'parlants).[11', ']']
        else:
            lemmatizer_skipped = True
    elif lang == 'hrv':
        if lemmatizer == 'simplemma_hrv':
            assert lemmas == ['hrvatski', 'jezik', '(', 'ISO', '639', 'ga', '3', ':', 'hrv', 'inačica', 'izvorni', 'stranica', 'arhivirana', '18', '.', 'rujan', '2012', '.', ')', 'skupni', 'ju', 'naziv', 'за', 'nacionalni', 'standardni', 'jezik', 'Hrvat', ',', 'ti', 'за', 'skup', 'narječje', 'i', 'govora', 'kojima', 'govoriti', 'ili', 'biti', 'nekada', 'govoriti', 'Hrvat', '.']
        elif lemmatizer == 'spacy_hrv':
            assert lemmas == ['hrvatski', 'jezik', '(', 'ISO', '639', '-', '3', ':', 'hrv', 'Inačica', 'izvoran', 'stranica', 'arhiviran', '18', '.', 'rujan', '2012', '.', ')', 'skupni', 'biti', 'naziv', 'za', 'nacionalan', 'standardan', 'jezik', 'Hrvat', ',', 'te', 'za', 'skup', 'narječje', 'i', 'govor', 'koji', 'govoriti', 'ili', 'biti', 'nekada', 'govoriti', 'Hrvati', '.']
        else:
            lemmatizer_skipped = True
    elif lang == 'ces':
        if lemmatizer == 'simplemma_ces':
            assert lemmas == ['čeština', 'neboli', 'český', 'jazyk', 'být', 'západoslovanský', 'jazyk', ',', 'nejbližší', 'slovenština', ',', 'poté', 'lužické', 'srbštině', 'a', 'polština', '.']
        elif lemmatizer == 'spacy_ces':
            assert lemmas == ['Čeština', 'neboli', 'český', 'jazyk', 'on', 'západoslovanský', 'jazyk', ',', 'blízký', 'slovenštině', ',', 'poté', 'lužické', 'srbštině', 'a', 'polštině', '.']
        else:
            lemmatizer_skipped = True
    elif lang == 'dan':
        if lemmatizer == 'simplemma_dan':
            assert lemmas == ['dansk', 'være', 'en', 'østnordisk', 'sprog', 'indenfor', 'den', 'germansk', 'gren', 'af', 'den', 'indoeuropæiske', 'sprogfamilie', '.']
        elif lemmatizer == 'spacy_dan':
            assert lemmas == ['dansk', 'være', 'en', 'østnordisk', 'sprog', 'indenfor', 'den', 'germansk', 'gren', 'af', 'den', 'indoeuropæisk', 'sprogfamilie', '.']
        else:
            lemmatizer_skipped = True
    elif lang == 'nld':
        if lemmatizer == 'simplemma_nld':
            assert lemmas == ['het', 'Nederlands', 'zijn', 'een', 'west-germaans', 'talen', 'en', 'de', 'officieel', 'talen', 'van', 'Nederland', ',', 'Suriname', 'en', 'een', 'van', 'de', 'drie', 'officieel', 'tale', 'van', 'België', '.']
        elif lemmatizer == 'spacy_nld':
            assert lemmas == ['het', 'Nederlands', 'zijn', 'een', 'West-Germaans', 'taal', 'en', 'de', 'officieel', 'taal', 'van', 'Nederland', ',', 'Suriname', 'en', 'één', 'van', 'de', 'drie', 'officieel', 'taal', 'van', 'België', '.']
        else:
            lemmatizer_skipped = True
    elif lang == 'enm':
        assert lemmas == ['Forrþrihht', 'anan', 'see', 'timen', 'comm', 'þatt', 'eure', 'Drihhtin', 'wollde', 'been', 'borenn', 'in', 'þiss', 'middellærd', 'forr', 'all', 'mannkinne', 'neden', 'hem', 'chæs', 'him', 'sonne', 'kinnessmenn', 'all', 'swillke', 'summ', 'hem', 'wollde', 'and', 'whær', 'hem', 'wollde', 'borenn', 'been', 'hem', 'chæs', 'all', 'att', 'his', 'willen', '.']
    elif lang.startswith('eng_'):
        if lemmatizer == 'nltk_wordnet':
            assert lemmas == ['English', 'be', 'a', 'West', 'Germanic', 'language', 'of', 'the', 'Indo', '-', 'European', 'language', 'family', ',', 'originally', 'speak', 'by', 'the', 'inhabitant', 'of', 'early', 'medieval', 'England.[3][4][5', ']']
        elif lemmatizer == 'simplemma_eng':
            assert lemmas == ['English', 'be', 'a', 'west', 'germanic', 'language', 'of', 'the', 'Indo', '-', 'European', 'language', 'family', ',', 'originally', 'speak', 'by', 'the', 'inhabitant', 'of', 'early', 'medieval', 'England.[3][4][5', ']']
        elif lemmatizer == 'spacy_eng':
            assert lemmas == ['English', 'be', 'a', 'West', 'Germanic', 'language', 'of', 'the', 'Indo', '-', 'european', 'language', 'family', ',', 'originally', 'speak', 'by', 'the', 'inhabitant', 'of', 'early', 'medieval', 'England.[3][4][5', ']']
        else:
            lemmatizer_skipped = True
    elif lang == 'est':
        assert lemmas == ['Eesti', 'keel', '(', 'varasem', 'nimetus', 'maakeel', ')', 'olema', 'läänemeresoome', 'lõuna', 'kuuluv', 'keel', '.']
    elif lang == 'fin':
        if lemmatizer == 'simplemma_fin':
            assert lemmas == ['Suomi', 'kieli', '(', 'suomi', ')', 'olla', 'uralilainen', 'kieli', 'itämerensuomalainen', 'ryhmä', 'kuuluva', 'kieli', ',', 'jota', 'puhua', 'pääosa', 'Suomalainen', '.']
        elif lemmatizer == 'spacy_fin':
            assert lemmas == ['Suomi', 'kieli', '(', 'suomi', ')', 'olla', 'uralilainen', 'kieli', 'itämerensuomalainen', 'ryhmä', 'kuulua', 'kieli', ',', 'joka', 'puhua', 'pääosin', 'suomalainen', '.']
        else:
            lemmatizer_skipped = True
    elif lang == 'fra':
        if lemmatizer == 'simplemma_fra':
            assert lemmas == ['le', 'français', 'être', 'un', 'langue', 'indo-européen', 'de', 'le', 'famille', 'un', 'langue', 'roman', 'dont', 'le', 'locuteurs', 'être', 'appelé', 'francophone', ',', 'également', 'surnommer', 'le', 'langue', 'de', 'Molière', '.']
        elif lemmatizer == 'spacy_fra':
            assert lemmas == ['le', 'français', 'être', 'un', 'langue', 'indo-européen', 'de', 'le', 'famille', 'de', 'langue', 'romane', 'dont', 'le', 'locuteur', 'être', 'appeler', 'francophone', ',', 'également', 'surnommer', 'le', 'langue', 'de', 'molière', '.']
        else:
            lemmatizer_skipped = True
    elif lang == 'glg':
        assert lemmas == ['O', 'galego', '(', '[', 'ɡaˈleɣo̝', ']', ')', 'ser', 'un', 'lingua', 'indoeuropeo', 'que', 'pertencer', 'á', 'póla', 'de', 'lingua', 'románico', '.']
    elif lang == 'kat':
        assert lemmas == ['ქართული', 'ენა', '—', 'იბერიულ-კავკასიურ', 'ენათა', 'ოჯახის', 'ქართველურ', 'ენათა', 'ჯგუფი', 'ენა.']
    elif lang.startswith('deu_'):
        if lemmatizer == 'simplemma_deu':
            assert lemmas == ['der', 'deutsch', 'Sprache', 'bzw.', 'deutsch', '(', '[', 'dɔɪ̯tʃ];[26', ']', 'abkürzen', 'dt', '.', 'oder', 'dtsch', '.', ')', 'sein', 'ein', 'westgermanische', 'Sprache', ',', 'der', 'weltweit', 'etwa', '90', 'bis', '105', 'Million', 'Mensch', 'als', 'Muttersprache', 'und', 'weit', 'rund', '80', 'Million', 'als', 'Zweit-', 'oder', 'Fremdsprache', 'dienen', '.']
        elif lemmatizer == 'spacy_deu':
            assert lemmas == ['der', 'deutsch', 'Sprache', 'bzw.', 'Deutsch', '--', '[', 'dɔɪ̯tʃ];[26', ']', 'abgekürzt', 'dt', '--', 'oder', 'dtsch', '--', '--', 'sein', 'ein', 'westgermanisch', 'Sprache', '--', 'der', 'weltweit', 'etwa', '90', 'bis', '105', 'Million', 'Mensch', 'als', 'Muttersprache', 'und', 'weit', 'rund', '80', 'Million', 'als', 'Zweit', 'oder', 'Fremdsprache', 'dienen', '--']
        else:
            lemmatizer_skipped = True
    elif lang == 'grc':
        assert lemmas == ['Ὅτι', 'μέν', 'σύ', ',', 'ὦ', 'ἀνήρ', 'Ἀθηναῖοι', ',', 'πάσχω', 'ὑπό', 'ὁ', 'ἐμός', 'κατηγόρων', ',', 'οὐ', 'οἶδα', '·', 'ἐγώ', 'δέ', 'οὖν', 'καί', 'αὐτός', 'ὑπό', 'αὐτός', 'ὀλίγος', 'ἐμαυτοῦ', 'ἐπελαθόμην', ',', 'οὕτως', 'πιθανῶς', 'λέγω', '.']
    elif lang == 'ell':
        if lemmatizer == 'simplemma_ell':
            assert lemmas == ['ο', 'ελληνικός', 'γλώσσα', 'ανήκω', 'στην', 'ινδοευρωπαϊκή', 'οικογένεια', ']', 'και', 'αποτελώ', 'ο', 'μοναδικός', 'μέλος', 'ο', 'ελληνικός', 'κλάδος', ',', 'ενώ', 'είμαι', 'ο', 'επίσημος', 'γλώσσα', 'ο', 'Ελλάδα', 'και', 'ο', 'Κύπρος', '.']
        elif lemmatizer == 'spacy_ell':
            assert lemmas == ['ο', 'ελληνικός', 'γλώσσα', 'ανήκω', 'σε ο', 'ινδοευρωπαϊκός', 'οικογένεια[9', ']', 'και', 'αποτελώ', 'ο', 'μοναδικός', 'μέλος', 'ο', 'ελληνικός', 'κλάδος', ',', 'ενώ', 'είμαι', 'ο', 'επίσημος', 'γλώσσα', 'ο', 'Ελλάδα', 'και', 'ο', 'Κύπρος', '.']
        else:
            lemmatizer_skipped = True
    elif lang == 'hin':
        assert lemmas == ['हिंदी', 'या', 'हिंदी', 'जिसके', 'मानकीकृत', 'रूप', 'को', 'मानक', 'हिंदी', 'कहना', 'जाना', 'होना', ',', 'विश्व', 'का', 'एक', 'प्रमुख', 'भाषा', 'होना', 'एवं', 'भारत', 'का', 'एक', 'राजभाषा', 'होना', '।']
    elif lang == 'hun':
        if lemmatizer == 'simplemma_hun':
            assert lemmas == ['a', 'magyar', 'nyelv', 'az', 'uráli', 'nyelvcsalád', 'tag', ',', 'a', 'finnugor', 'nyelve', 'köz', 'tartozik', 'ugor', 'nyelve', 'egyik', '.']
        elif lemmatizer == 'spacy_hun':
            assert lemmas == ['A', 'magyar', 'nyelv', 'az', 'uráli', 'nyelvcsalád', 'tag', ',', 'a', 'finnugor', 'nyelv', 'köz', 'tartozó', 'ugor', 'nyelv', 'egyik', '.']
        else:
            lemmatizer_skipped = True
    elif lang == 'isl':
        assert lemmas == ['íslenskur', 'vera', 'vesturnorrænt', ',', 'germanskur', 'og', 'indóevrópskur', 'tungumál', 'semja', 'vera', 'einkum', 'tala', 'og', 'rita', 'ær', 'Ísland', 'og', 'vera', 'móðurmál', 'langflestra', 'Íslendingur', '.', '[', '4', ']']
    elif lang == 'ind':
        if lemmatizer == 'simplemma_ind':
            assert lemmas == ['bahasa', 'Indonesia', 'adalah', 'bahasa', 'nasional', 'dan', 'resmi', 'di', 'seluruh', 'Indonesia', '.']
        elif lemmatizer == 'spacy_ind':
            assert lemmas == ['Bahasa', 'Indonesia', 'adalah', 'bahasa', 'nasional', 'dan', 'resmi', 'di', 'seluruh', 'Indonesia', '.']
        else:
            lemmatizer_skipped = True
    elif lang == 'gle':
        if lemmatizer == 'simplemma_gle':
            assert lemmas == ['Is', 'ceann', 'de', 'na', 'teangach', 'ceilteach', 'í', 'an', 'gaeilge', '(', 'nó', 'Gaeilge', 'na', 'hÉireann', 'mar', 'a', 'tabhair', 'ar', 'corruair', ')', ',', 'agus', 'ceann', 'den', 'trí', 'ceann', 'de', 'teangach', 'ceilteach', 'ar', 'a', 'tabhair', 'na', 'teangach', 'gaelach', '(', 'Gaeilge', ',', 'Gaeilge', 'manainn', 'agus', 'Gaeilge', 'na', 'hAlban', ')', 'go', 'áirithe', '.']
        elif lemmatizer == 'spacy_gle':
            assert lemmas == ['is', 'ceann', 'de', 'na', 'teangacha', 'ceilteacha', 'í', 'an', 'ghaeilge', '(', 'nó', 'gaeilge', 'na', 'héireann', 'mar', 'a', 'thugtar', 'uirthi', 'corruair', ')', ',', 'agus', 'ceann', 'den', 'dtrí', 'cinn', 'de', 'theangacha', 'ceilteacha', 'ar', 'a', 'dtugtar', 'na', 'teangacha', 'gaelacha', '(', 'gaeilge', ',', 'gaeilge', 'mhanann', 'agus', 'gaeilge', 'na', 'halban', ')', 'go', 'háirithe', '.']
        else:
            lemmatizer_skipped = True
    elif lang == 'ita':
        assert lemmas == ['il', 'italiano', '(', '[', 'itaˈljaːno][Nota', '1', ']', 'ascolta[?·info', ']', ')', 'essere', 'uno', 'lingua', 'romanza', 'parlato', 'principalmente', 'in', 'Italia', '.']
    elif lang == 'jpn':
        if lemmatizer == 'spacy_jpn':
            assert lemmas == ['日本', '語', '(', 'にほん', 'ご', '、', 'にっぽん', 'ご', '[', '注', '2', ']', ')', 'は', '、', '日本', '国', '内', 'や', '、', 'かつて', 'の', '日本', '領', 'だ', 'た', '国', '、', 'そして', '日本', '人', '同士', 'の', '間', 'で', '使用', 'する', 'れる', 'て', 'いる', '言語', '。']
        elif lemmatizer == 'sudachipy_jpn':
            assert lemmas == ['日本語', '(', 'にほん', 'ご', '、', 'にっぽん', 'ご', '[', '注', '2', ']', ')', 'は', '、', '日本', '国', '内', 'や', '、', 'かつて', 'の', '日本', '領', 'だ', 'た', '国', '、', 'そして', '日本人', '同士', 'の', '間', 'で', '使用', 'する', 'れる', 'て', 'いる', '言語', '。']
        else:
            lemmatizer_skipped = True
    elif lang == 'lat':
        assert lemmas == ['lingua', 'Latina,[1', ']', 'sive', 'sermo', 'Latinus,[2', ']', 'sum', 'lingua', 'indoeuropaeus', 'qui', 'primus', 'Latinus', 'universus', 'et', 'Romanus', 'antiquus', 'in', 'primus', 'loquor', 'quamobrem', 'interdum', 'etiam', 'lingua', 'Latia[3', ']', '(', 'in', 'Latium', 'enim', 'suetus', ')', 'et', 'lingua', 'Romana[4', ']', '(', 'nam', 'imperium', 'Romanus', 'sermo', 'sollemne', ')', 'appello', '.']
    elif lang == 'lav':
        assert lemmas == ['latviete', 'valoda', 'būt', 'dzimta', 'valoda', 'apmērs', '1,7', 'miljons', 'cilvēks', ',', 'galvenokārt', 'Latvija', ',', 'kur', 'tā', 'būt', 'vienīgs', 'valsts', 'valoda', '.', '[', '3', ']']
    elif lang == 'lit':
        if lemmatizer == 'simplemma_lit':
            assert lemmas == ['lietuvė', 'kalba', '–', 'ižti', 'baltas', 'prokalbė', 'kilęs', 'lietuvė', 'tauta', 'kalba', ',', 'kurti', 'Lietuva', 'irti', 'valstybinis', ',', 'o', 'Europa', 'sąjunga', '–', 'Viena', 'ižti', 'oficialus', 'kalbus', '.']
        elif lemmatizer == 'spacy_lit':
            assert lemmas == ['Lietuvių', 'kalba', '–', 'iš', 'balti', 'prokalbė', 'kilusi', 'lietuvis', 'tauta', 'kalba', ',', 'kuris', 'Lietuva', 'būti', 'valstybinis', ',', 'o', 'Europa', 'Sąjungoje', '–', 'vienas', 'iš', 'oficialias', 'kalbų', '.']
        else:
            lemmatizer_skipped = True
    elif lang == 'ltz':
        if lemmatizer == 'simplemma_ltz':
            assert lemmas == ["D'", 'Lëtzebuergesch', 'ginn', 'an', 'der', 'däitsch', 'Dialektologie', 'als', 'een', 'westgermanesch', ',', 'mëtteldäitsch', 'Dialekt', 'aklasséiert', ',', 'deen', 'zum', 'muselfränkesch', 'gehéiert', '.']
        elif lemmatizer == 'spacy_ltz':
            assert lemmas == ["D'", 'Lëtzebuergesch', 'ginn', 'an', 'der', 'däitsch', 'Dialektologie', 'als', 'een', 'westgermanesch', ',', 'mëtteldäitsch', 'Dialekt', 'aklasséieren', ',', 'deen', 'zum', 'Muselfränkesche', 'gehéieren', '.']
        else:
            lemmatizer_skipped = True
    elif lang == 'mkd':
        if lemmatizer == 'simplemma_mkd':
            assert lemmas == ['македонски', 'јазик', '—', 'јужнословенски', 'јазик', ',', 'дел', 'од', 'група', 'на', 'словенски', 'јазик', 'од', 'јазичното', 'семејство', 'на', 'индоевропски', 'јазик', '.']
        elif lemmatizer == 'spacy_mkd':
            assert lemmas == ['Македонски', 'јаз', '—', 'јужнословенски', 'јаз', ',', 'дел', 'од', 'група', 'на', 'словенски', 'јазик', 'од', 'јазичен', 'семејство', 'на', 'индоевропски', 'јазик', '.']
        else:
            lemmatizer_skipped = True
    elif lang == 'msa':
        assert lemmas == ['bahasa', 'Melayu', '(', 'tulisan', 'Jawi', ':', 'bahasa', 'Melayu', ';', 'rencong', ':', 'ꤷꥁꤼ', 'ꤸꥍꤾꤿꥈ', ')', 'ialah', 'sejenis', 'bahasa', 'Melayu', '-', 'Polinesia', 'di', 'bawah', 'keluarga', 'bahasa', 'Austronesia', 'hiang', 'telah', 'digunakan', 'di', 'wilayah', 'Indonesia', ',', 'Malaysia', ',', 'دان', 'persekitaran', 'sejak', 'melebihi', '1,000', 'تاهون', 'lalu', '.']
    elif lang == 'glv':
        assert lemmas == ['She', 'Gaelg', '(', 'graït', ':', '/gɪlg/', ')', 'çhengey', 'Gaelagh', 'Mannin', '.']
    elif lang == 'nob':
        if lemmatizer == 'simplemma_nob':
            assert lemmas == ['bokmål', 'være', 'enn', 'varietet', 'av', 'norsk', 'språk', '.']
        elif lemmatizer == 'spacy_nob':
            assert lemmas == ['bokmål', 'være', 'en', 'varietet', 'av', 'norsk', 'språk', '$.']
        else:
            lemmatizer_skipped = True
    elif lang == 'nno':
        assert lemmas == ['nynorsk', ',', 'føra', '1929', 'offisiell', 'kall', 'landsmål', ',', 'vera', 'sidan', 'jamstillingsvedtaket', 'av', '12', '.', 'mai', '1885', 'ein', 'av', 'den', 'to', 'offisiell', 'målformene', 'av', 'norsk', ';', 'den', 'annan', 'forme', 'vera', 'bokmål', '.']
    elif lang == 'fas':
        if lemmatizer == 'simplemma_fas':
            assert lemmas == ['فارسی', 'یا', 'پارسی', 'یک', 'زبان', 'ایرانی', 'غربی', 'از', 'زیرگروه', 'ایرانی', 'شاخهٔ', 'هندوایرانیِ', 'خانوادهٔ', 'زبان\u200cهای', 'هندواروپایی', 'است', 'که', 'در', 'کشورهای', 'ایران', '،', 'افغانستان', '،', 'تاجیکستان', '،', 'ازبکستان', '،', 'پاکستان', '،', 'عراق', '،', 'ترکمنستان', 'را', 'آذربایجان', 'به', 'آن', 'سخن', 'می\u200cگویند', '.']
        elif lemmatizer == 'spacy_fas':
            assert lemmas == ['فارسی', 'یا', 'پارسی', 'یک', 'زبان', 'ایرانی', 'غربی', 'از', 'زیرگروه', 'ایرانی', 'شاخهٔ', 'هندوایرانیِ', 'خانوادهٔ', 'زبان\u200cهای', 'هندواروپایی', 'است', 'که', 'در', 'کشورهای', 'ایران', '،', 'افغانستان', '،', 'تاجیکستان', '،', 'ازبکستان', '،', 'پاکستان', '،', 'عراق', '،', 'ترکمنستان', 'و', 'آذربایجان', 'به', 'آن', 'سخن', 'می\u200cگویند', '.']
        else:
            lemmatizer_skipped = True
    elif lang == 'pol':
        if lemmatizer == 'simplemma_pol':
            assert lemmas == ['język', 'polski', ',', 'polszczyzna', '–', 'język', 'lechicki', 'z', 'grupa', 'zachodniosłowiański', '(', 'do', 'który', 'należeć', 'również', 'czeski', ',', 'kaszubski', ',', 'słowacki', 'i', 'język', 'łużycki', ')', ',', 'stanowić', 'część', 'rodzina', 'indoeuropejski', '.']
        elif lemmatizer == 'spacy_pol':
            assert lemmas == ['Język', 'polski', ',', 'polszczyzny', '–', 'język', 'lechicki', 'z', 'grupa', 'zachodniosłowiański', '(', 'do', 'który', 'należeć', 'również', 'czeski', ',', 'kaszubski', ',', 'słowacki', 'i', 'język', 'łużycki', ')', ',', 'stanowić', 'część', 'rodzina', 'indoeuropejski', '.']
        else:
            lemmatizer_skipped = True
    elif lang.startswith('por_'):
        if lemmatizer == 'simplemma_por':
            assert lemmas == ['o', 'língua', 'portuguesar', ',', 'também', 'designado', 'português', ',', 'ser', 'umar', 'língua', 'indo-europeu', 'românico', 'flexivo', 'ocidental', 'originado', 'o', 'galego-português', 'falar', 'o', 'reino', 'da', 'galiza', 'e', 'o', 'norte', 'de', 'portugal', '.']
        elif lemmatizer == 'spacy_por':
            assert lemmas == ['o', 'língua', 'português', ',', 'também', 'designar', 'português', ',', 'ser', 'um', 'língua', 'indo-europeia', 'românico', 'flexiva', 'ocidental', 'originar', 'em o', 'galego-português', 'falar', 'em o', 'Reino', 'de o', 'Galiza', 'e', 'em o', 'norte', 'de', 'Portugal', '.']
        else:
            lemmatizer_skipped = True
    elif lang == 'ron':
        if lemmatizer == 'simplemma_ron':
            assert lemmas == ['limbă', 'român', 'fi', 'el', 'limbă', 'indo-european', ',', 'din', 'grup', 'italic', 'și', 'din', 'subgrupul', 'oriental', 'al', 'limbă', 'romanice', '.']
        elif lemmatizer == 'spacy_ron':
            assert lemmas == ['limbă', 'român', 'fi', 'un', 'limbă', 'indo-european', ',', 'din', 'grup', 'italic', 'și', 'din', 'subgrup', 'oriental', 'al', 'limbilor', 'romanic', '.']
        else:
            lemmatizer_skipped = True
    elif lang == 'rus':
        if lemmatizer == 'simplemma_rus':
            assert lemmas == ['Ру́сский', 'язы́к', '(', '[', 'ˈruskʲɪi̯', 'jɪˈzɨk', ']', 'информация', 'о', 'файл', 'слушать)[~', '3', ']', '[', '⇨', ']', '—', 'один', 'из', 'восточнославянский', 'языковый', ',', 'национальный', 'язык', 'русский', 'народ', '.']
        elif lemmatizer in ['pymorphy2_morphological_analyzer', 'spacy_rus']:
            assert lemmas == ['ру́сский', 'язы́к', '(', '[', 'ˈruskʲɪi̯', 'jɪˈzɨk', ']', 'информация', 'о', 'файл', 'слушать)[~', '3', ']', '[', '⇨', ']', '—', 'один', 'из', 'восточнославянский', 'язык', ',', 'национальный', 'язык', 'русский', 'народ', '.']
        else:
            lemmatizer_skipped = True
    elif lang == 'sme':
        assert lemmas == ['davvisámegiella', 'gullát', 'sámegiella', 'oarjesámegielaid', 'davvejovkui', 'ovttastit', 'julev-', 'ja', 'bihtánsámegielain', '.']
    elif lang == 'gla':
        assert lemmas == ["'S", 'i', 'cànan', 'dùthchasach', 'na', 'h', '-', 'alba', 'a', 'th', "'", 'anns', 'a', "'", 'gàidhlig', '.']
    elif lang == 'srp_cyrl':
        assert lemmas == ['Српски', 'језик', 'припадати', 'словенски', 'група', 'језик', 'породица', 'индоевропских', 'језика.[12', ']']
    elif lang == 'srp_latn':
        assert lemmas == ['srpski', 'jezik', 'pripadati', 'slovenski', 'grupa', 'jezika', 'porodica', 'indoevropski', 'jezika.[12', ']']
    elif lang == 'slk':
        assert lemmas == ['slovenčina', 'patriť', 'do', 'skupina', 'západoslovanský', 'jazyk', '(', 'spolu', 's', 'čeština', ',', 'poľština', ',', 'horný', 'a', 'dolný', 'lužickou', 'srbčina', 'a', 'kašubčiný', ')', '.']
    elif lang == 'slv':
        assert lemmas == ['slovenščina', '[', 'sloˈʋenʃtʃina', ']', 'on', 'združen', 'naziv', 'za', 'uraden', 'knjižen', 'jezik', 'Slovenec', 'in', 'skupen', 'ime', 'za', 'narečje', 'in', 'govor', ',', 'ki', 'on', 'govoriti', 'ali', 'biti', 'on', 'nekoč', 'govorilo', 'Slovenec', '.']
    elif lang == 'spa':
        if lemmatizer == 'simplemma_spa':
            assert lemmas == ['el', 'español', 'o', 'castellano', 'ser', 'uno', 'lengua', 'romance', 'procedente', 'del', 'latín', 'hablar', ',', 'perteneciente', 'a', 'el', 'familia', 'de', 'lengua', 'indoeuropeo', '.']
        elif lemmatizer == 'spacy_spa':
            assert lemmas == ['el', 'español', 'o', 'castellano', 'ser', 'uno', 'lenguo', 'romance', 'procedente', 'del', 'latín', 'hablado', ',', 'perteneciente', 'a', 'el', 'familia', 'de', 'lengua', 'indoeuropea', '.']
        else:
            lemmatizer_skipped = True
    elif lang == 'swa':
        assert lemmas == ['Kiswahili', 'ni', 'lugha', 'ya', 'Kibantu', 'enye', 'msamiati', 'ingi', 'ya', 'Kiarabu', '(', '35%[1', ']', ')', ',', 'laki', 'sasa', 'ya', 'Kiingereza', 'pia', '(', '10', '%', ')', ',', 'inayozungumzwa', 'katika', 'eneo', 'kubwa', 'la', 'Afrika', 'ya', 'mashariki', '.']
    elif lang == 'swe':
        if lemmatizer == 'simplemma_swe':
            assert lemmas == ['svensk', '(', 'svensk', '(', 'info', ')', ')', 'ära', 'en', 'östnordiskt', 'språka', 'som', 'tala', 'av', 'ungefär', 'tio', 'miljon', 'person', 'främst', 'i', 'Sverige', 'där', 'språk', 'ha', 'man', 'dominant', 'ställning', 'som', 'huvudspråk', ',', 'mena', 'även', 'som', 'den', 'en', 'nationalspråk', 'i', 'Finland', 'och', 'som', 'enda', 'officiell', 'språka', 'på', 'Åland', '.']
        elif lemmatizer == 'spacy_swe':
            assert lemmas == ['Svenska', '(', 'svensk', '(', 'info', ')', ')', 'vara', 'en', 'östnordisk', 'språk', 'som', 'tala', 'av', 'ungefär', 'tio', 'miljon', 'person', 'främst', 'i', 'Sverige', 'där', 'språket', 'ha', 'en', 'dominant', 'ställning', 'som', 'huvudspråk', ',', 'men', 'även', 'som', 'en', 'ena', 'nationalspråk', 'i', 'Finland', 'och', 'som', 'enda', 'officiell', 'språk', 'på', 'Åland', '.']
        else:
            lemmatizer_skipped = True
    elif lang == 'tgl':
        if lemmatizer == 'simplemma_tgl':
            assert lemmas == ['Ang', 'wikang', 'Tagalog[1', ']', '(', 'Baybayin', ':', 'ᜏᜒᜃᜆᜄᜎᜓ', ')', ',', 'o', 'ang', 'Tagalog', ',', 'ay', 'isa', 'sa', 'mga', 'pinakaginagamit', 'na', 'wikain', 'ng', 'Pilipinas', '.']
        elif lemmatizer == 'spacy_tgl':
            assert lemmas == ['Ang', 'wikang', 'Tagalog[1', ']', '(', 'Baybayin', ':', 'ᜏᜒᜃᜆᜄᜎᜓ', ')', ',', 'o', 'ang', 'Tagalog', ',', 'ay', 'isa', 'sa', 'mga', 'pinakaginagamit', 'na', 'wika', 'ng', 'Pilipinas', '.']
        else:
            lemmatizer_skipped = True
    elif lang == 'bod':
        assert lemmas == ['བོད་', 'གི་', 'སྐད་ཡིག་', 'ནི་', 'བོད་ཡུལ་', 'དང་', 'དེ་', 'གི་', 'ཉེ་འཁོར་', 'གི་', 'ས་ཁུལ་', 'སྟེ་', '།']
    elif lang == 'tur':
        if lemmatizer == 'simplemma_tur':
            assert lemmas == ['türkçe', 'ya', 'da', 'Türk', 'dil', ',', 'güneydoğu', 'avrupa', 've', 'batı', 'asya', 'konuş', ',', 'Türk', 'dil', 'dil', 'aile', 'ait', 'son', 'ekle', 'bir', 'dil.[12', ']']
        elif lemmatizer == 'spacy_tur':
            assert lemmas == ['Türkçe', 'ya', 'da', 'Türk', 'dil', ',', 'Güneydoğu', 'Avrupa', 've', 'Batı', "Asya'da", 'konuş', ',', 'Türk', 'dil', 'dil', 'aile', 'ait', 'son', 'ekle', 'bir', 'dil.[12', ']']
        else:
            lemmatizer_skipped = True
    elif lang == 'ukr':
        if lemmatizer == 'pymorphy2_morphological_analyzer':
            assert lemmas == ['украї́нський', 'мо́вий', '(', 'мфа', ':', '[', 'ukrɑ̽ˈjɪnʲsʲkɑ̽', 'ˈmɔwɑ̽', ']', ',', 'історичний', 'назва', '—', 'ру́ський', ',', 'руси́нська[10][11][12', ']', '[', '*', '1', ']', ')', '—', 'національний', 'мова', 'українець', '.']
        elif lemmatizer == 'simplemma_ukr':
            assert lemmas == ['Українськ', 'мо́ва', '(', 'мфа', ':', '[', 'ukrɑ̽ˈjɪnʲsʲkɑ̽', 'ˈmɔwɑ̽', ']', ',', 'історичний', 'назва', '—', 'руський', ',', 'руси́нська[10][11][12', ']', '[', '*', '1', ']', ')', '—', 'національний', 'мова', 'українець', '.']
        elif lemmatizer == 'spacy_ukr':
            assert lemmas == ['украї́нська', 'мо́ва', '(', 'мфа', ':', '[', 'ukrɑ̽ˈjɪnʲsʲkɑ̽', 'ˈmɔwɑ̽', ']', ',', 'історичний', 'назва', '—', 'ру́ська', ',', 'руси́нська[10][11][12', ']', '[', '*', '1', ']', ')', '—', 'національний', 'мова', 'українець', '.']
        else:
            lemmatizer_skipped = True
    elif lang == 'urd':
        assert lemmas == ['اُردُو', 'یا', 'لشکری', 'زبان[8', ']', 'برصغیر', 'کم', 'معیاری', 'زبان', 'میں', 'سے', 'ایک', 'ہونا', '۔']
    elif lang == 'cym':
        assert lemmas == ['aelod', "o'r", 'cangen', 'Frythonaidd', "o'r", 'iaith', 'celtaidd', 'a', 'siarad', 'bod', 'brodorol', 'yn', 'cymru', ',', 'can', 'cymry', 'a', 'pobl', 'arall', 'aredig', 'gwasgar', 'bod', 'lloegr', ',', 'a', 'can', 'cymuned', 'bechan', 'bod', 'yr', 'gwladfa', ',', 'gŵr', 'Ariannin[7', ']', "yw'r", 'cymraeg', '(', 'hefyd', 'cymraeg', 'heb', 'yr', 'bannod', ')', '.']
    else:
        raise Exception(f'Error: Tests for language "{lang}" is skipped!')

    if lemmatizer_skipped:
        raise Exception(f'Error: Tests for lemmatizer "{lemmatizer}" is skipped!')

if __name__ == '__main__':
    for lang, lemmatizer in test_lemmatizers:
        test_lemmatize(lang, lemmatizer)
