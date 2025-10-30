# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Tests: NLP - Sentence tokenization
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
from wordless.wl_nlp import wl_sentence_tokenization

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')

langs_sentence_tokenize = []

for lang, sentence_tokenizers in main.settings_global['sentence_tokenizers'].items():
    for sentence_tokenizer in sentence_tokenizers:
        if (
            not sentence_tokenizer.startswith(('spacy_', 'stanza_'))
            # Skip tests of spaCy's and Stanza's sentence tokenizers for most languages
            or (
                lang in {'eng_gb', 'eng_us', 'srp_cyrl', 'srp_latn', 'other'}
                and not sentence_tokenizer.startswith(('spacy_dependency_parser_', 'stanza_'))
            )
        ):
            langs_sentence_tokenize.append((lang, sentence_tokenizer))

langs_sentence_split = list(main.settings_global['sentence_tokenizers'])

@pytest.mark.parametrize('lang, sentence_tokenizer', langs_sentence_tokenize)
def test_sentence_tokenize(lang, sentence_tokenizer):
    tests_lang_util_skipped = False

    match lang:
        case 'ces':
            results = ['Čeština neboli český jazyk je západoslovanský jazyk, nejbližší slovenštině, poté lužické srbštině a polštině.', 'Patří mezi slovanské jazyky, do rodiny jazyků indoevropských.']
        case 'dan':
            results = ['Dansk er et østnordisk sprog indenfor den germanske gren af den indoeuropæiske sprogfamilie.', 'Det danske sprog tales af ca. seks millioner mennesker, hovedsageligt i Danmark, men også i Sydslesvig, på Færøerne og Grønland.', '[1]']
        case 'nld':
            results = ['Het Nederlands is een West-Germaanse taal, de meest gebruikte taal in Nederland en België, de officiële taal van Suriname en een van de drie officiële talen van België.', 'Binnen het Koninkrijk der Nederlanden is het Nederlands ook een officiële taal van Aruba, Curaçao en Sint-Maarten.']
        case 'eng_gb' | 'eng_us' | 'other':
            match sentence_tokenizer:
                case 'nltk_punkt_eng':
                    results = ['English is a West Germanic language in the Indo-European language family, whose speakers, called Anglophones, originated in early medieval England on the island of Great Britain.', '[4][5][6] The namesake of the language is the Angles, one of the Germanic peoples that migrated to Britain after its Roman occupiers left.']
                case 'spacy_sentencizer':
                    results = ['English is a West Germanic language in the Indo-European language family, whose speakers, called Anglophones, originated in early medieval England on the island of Great Britain.[4][5][6] The namesake of the language is the Angles, one of the Germanic peoples that migrated to Britain after its Roman occupiers left.']
                case _:
                    tests_lang_util_skipped = True
        case 'est':
            results = ['Eesti keel (varasem nimetus maakeel) on läänemeresoome lõunarühma kuuluv keel.', 'Eesti keel on Eesti riigikeel ja 2004. aastast ka üks Euroopa Liidu ametlikke keeli.']
        case 'fin':
            results = ['Suomen kieli eli suomi on uralilaisten kielten itämerensuomalaiseen ryhmään kuuluva kieli, jota puhuvat pääosin suomalaiset.', 'Suomessa suomen kieltä puhuu äidinkielenään 4,8 miljoonaa ja toisena kielenään 0,5 miljoonaa ihmistä.']
        case 'fra':
            results = ['Le français est une langue indo-européenne de la famille des langues romanes dont les locuteurs sont appelés « francophones ».', "Il est la cinquième langue parlée au monde après l'anglais, le mandarin, le hindi et l'espagnol."]
        case 'deu_at' | 'deu_de' | 'deu_ch':
            results = ['Die deutsche Sprache oder Deutsch [dɔɪ̯tʃ][24] ist eine westgermanische Sprache, die weltweit etwa 90 bis 105 Millionen Menschen als Muttersprache und weiteren rund 80 Millionen als Zweit- oder Fremdsprache dient.', 'Das Deutsche ist eine plurizentrische Sprache, enthält also mehrere Standardvarietäten in verschiedenen Regionen.']
        case 'ell':
            results = ['Η ελληνική γλώσσα ανήκει στην ινδοευρωπαϊκή οικογένεια[9] secεπίσης στο βαλκανικό γλωσσικό δεσμό.', 'ελληνική γλώσσα, έχουμε γραπτά κείμενα ήδη από τον 15ο αιώνα π.Χ..']
        case 'ita':
            results = ["L'italiano è una lingua romanza parlata principalmente in Italia.", "Per ragioni storiche e geografiche, l'italiano è la lingua romanza meno divergente dal latino (complessivamente a pari merito, anche se in parametri diversi, con la lingua sarda).", '[2][3][4][5]']
        case 'khm':
            results = ['ភាសាខ្មែរ គឺជាភាសាកំណើតរបស់ជនជាតិខ្មែរនិងជាភាសាផ្លូវការរបស់ប្រទេសកម្ពុជា។', 'ភាសាសំស្ក្រឹតនិងភាសាបាលីបានជួយបង្កើតខេមរភាសា ព្រោះភាសាខ្មែរបានខ្ចីពាក្យច្រើនពីភាសាទាំងពីរនេះ។']
        case 'lao':
            results = ['ພາສາລາວສືບທອດມາຈາກພາສາຕະກຸນໄຕ-ກະໄດ ຢູ່ພາກໃຕ້ຂອງປະເທດຈີນ ເຊິ່ງເປັນຈຸດເດີມຂອງຫຼາຍພາສາໃນຕະກຸນນີ້ທີ່ຍັງຖືກໃຊ້ ແລະ ຖືກເວົ້າຢູ່ໂດຍຫຼາຍຊົນເຜົ່າໃນປັດຈຸບັນ.', 'ເນື່ອງຈາກຖືກຄວາມກົດດັນຈາກການຂະຫຍາຍຕົວຂອງອານາຈັກຈີນ, ການບຸກຮຸກຮານຂອງຊາວມົງໂກລີ ແລະ ການປູກຝັງທຳມາຫາກິນ, ຄົນໄຕ (ໄທ) ໄດ້ຍົກຍ້າຍລົງມາທາງໃຕ້ກະຈາຍໄປຕາມແຫຼ່ງທໍາມາຫາກິນທີ່ເໝາະສົມກັບຕົນ.']
        case 'mal':
            results = ['ഇതു ദ്രാവിഡ ഭാഷാ കുടുംബത്തിൽപ്പെടുന്നു.', 'ഇന്ത്യയിൽ ശ്രേഷ്ഠഭാഷാ പദവി ലഭിക്കുന്ന അഞ്ചാമത്തെ ഭാഷയാണ് മലയാളം[5].']
        case 'nob':
            results = ['Bokmål er en av to offisielle målformer av norsk skriftspråk, hvorav den andre er nynorsk.', 'I skrift har 87,3 % bokmål som hovedmål i skolen.', '[3]']
        case 'pol':
            results = ['Język polski, polszczyzna – język lechicki z grupy zachodniosłowiańskiej (do której należą również czeski, kaszubski, słowacki, języki łużyckie czy wymarły język drzewiański), stanowiącej część rodziny indoeuropejskiej.', 'Jest językiem urzędowym w Polsce oraz należy do oficjalnych języków Unii Europejskiej.']
        case 'por_br' | 'por_pt':
            results = ['A língua portuguesa, também designada português, é uma língua indo-europeia românica flexiva ocidental originada no galego-português falado no Reino da Galiza e no norte de Portugal.', 'Com a criação do Reino de Portugal em 1139 e a expansão para o sul na sequência da Reconquista, deu-se a difusão da língua pelas terras conquistadas e, mais tarde, com as descobertas portuguesas, para o Brasil, África e outras partes do mundo.', '[9]']
        case 'rus':
            results = ['Русский язык (МФА: [ˈruskʲɪɪ̯ ɪ̯ɪˈzɨk]о файле)[~ 3] — язык восточнославянской группы славянской ветви индоевропейской языковой семьи, национальный язык русского народа.', 'Является одним из наиболее распространённых языков мира — восьмым среди всех языков мира по общей численности говорящих[5] и седьмым по численности владеющих им как родным (2022)[2].']
        case 'srp_cyrl':
            results = ['Српски језик припада словенској групи језика породице индоевропских језика.[12] Српски језик је званичан у Србији, Босни и Херцеговини и Црној Гори и говори га око 12 милиона људи.[13]']
        case 'srp_latn':
            results = ['Srpski jezik pripada slovenskoj grupi jezika porodice indoevropskih jezika.[12] Srpski jezik je zvaničan u Srbiji, Bosni i Hercegovini i Crnoj Gori i govori ga oko 12 miliona ljudi.[13]']
        case 'slv':
            results = ['Slovenščina [sloˈʋenʃtʃina] je združeni naziv za uradni knjižni jezik Slovencev in skupno ime za narečja in govore, ki jih govorijo ali so jih nekoč govorili Slovenci.', 'Govori ga okoli 2,5 (dva in pol) milijona govorcev po svetu, od katerih jih večina živi v Sloveniji.']
        case 'spa':
            results = ['El español o castellano es una lengua romance procedente del latín hablado, perteneciente a la familia de lenguas indoeuropeas.', 'Forma parte del grupo ibérico y es originaria de Castilla, reino medieval de la península ibérica.']
        case 'swe':
            results = ['Svenska (svenska\u2009(fil)) är ett östnordiskt språk som talas av ungefär tio miljoner personer, främst i Sverige där språket har en dominant ställning som huvudspråk, men även som det ena nationalspråket i Finland och som enda officiella språk på Åland.', 'I övriga Finland talas det som modersmål framförallt i de finlandssvenska kustområdena i Österbotten, Åboland och Nyland.']
        case 'tha':
            match sentence_tokenizer:
                case 'pythainlp_crfcut':
                    results = ['ภาษาไทย หรือ ภาษาไทยกลาง เป็นภาษาในกลุ่มภาษาไท สาขาย่อยเชียงแสน ซึ่งเป็นกลุ่มย่อยของตระกูลภาษาขร้า-ไท และเป็นภาษาราชการ และภาษาประจำชาติของประเทศไทย[3][4]', 'มีการสันนิษฐานว่าภาษาในตระกูลนี้มีถิ่นกำเนิดจากทางตอนใต้ของประเทศจีน และนักภาษาศาสตร์บางส่วนเสนอว่า ภาษาไทยน่าจะมีความเชื่อมโยงกับตระกูลภาษาออสโตร-เอเชียติก', 'ตระกูลภาษาออสโตรนีเซียน และตระกูลภาษาจีน-ทิเบต']
                case 'pythainlp_thaisumcut':
                    results = ['ภาษาไทย', 'หรือ ภาษาไทยกลาง เป็นภาษาในกลุ่มภาษาไท สาขาย่อยเชียงแสน', 'ซึ่งเป็นกลุ่มย่อยของตระกูลภาษาขร้า-ไท และเป็นภาษาราชการ', 'และภาษาประจำชาติของประเทศไทย[3][4] มีการสันนิษฐานว่าภาษาในตระกูลนี้มีถิ่นกำเนิดจากทางตอนใต้ของประเทศจีน', 'และนักภาษาศาสตร์บางส่วนเสนอว่า ภาษาไทยน่าจะมีความเชื่อมโยงกับตระกูลภาษาออสโตร-เอเชียติก ตระกูลภาษาออสโตรนีเซียน และตระกูลภาษาจีน-ทิเบต']
                case _:
                    tests_lang_util_skipped = True
        case 'xct' | 'bod':
            results = ['བོད་ཀྱི་སྐད་ཡིག་ནི་བོད་ཡུལ་དང་ཉེ་འཁོར་གྱི་ས་ཁུལ་བལ་ཡུལ། འབྲུག་དང་འབྲས་ལྗོངས། ལ་དྭགས་ནས་ལྷོ་མོན་རོང་སོགས་སུ་བེད་སྤྱོད་བྱེད་པའི་སྐད་ཡིག་དེ།', 'ད་ཆར་ཡོངས་གྲགས་སུ་བོད་ཀྱི་ཡུལ་གྲུ་སྟོད་སྨད་བར་གསུམ་ལ་ལྟོས་ཏེ་ནང་གསེས་རིགས་གསུམ་དུ་ཕྱེ་བ་སྟེ།']
        case 'tur':
            results = ["Türkçe ya da Türk dili, Güneydoğu Avrupa ve Batı Asya'da konuşulan, Türk dilleri dil ailesine ait sondan eklemeli bir dildir.", '[10] Türk dilleri ailesinin Oğuz dilleri grubundan bir Batı Oğuz dili olan Osmanlı Türkçesinin devamını oluşturur.']
        case 'vie':
            results = ['Tiếng Việt hay tiếng Kinh là một ngôn ngữ thuộc ngữ hệ Nam Á, được công nhận là ngôn ngữ chính thức tại Việt Nam.', 'Đây là tiếng mẹ đẻ của khoảng 85% dân cư Việt Nam cùng với hơn 4 triệu người Việt kiều.']
        case _:
            raise wl_test_init.Wl_Exc_Tests_Lang_Skipped(lang)

    if tests_lang_util_skipped:
        raise wl_test_init.Wl_Exc_Tests_Lang_Util_Skipped(sentence_tokenizer)

    wl_test_sentence_tokenize_models(lang, sentence_tokenizer, results)

def wl_test_sentence_tokenize_models(lang, sentence_tokenizer, results):
    print(f'{lang} / {sentence_tokenizer}:')

    test_sentence = ''.join(getattr(wl_test_lang_examples, f'TEXT_{lang.upper()}'))
    sentences = wl_sentence_tokenization.wl_sentence_tokenize(
        main,
        # Empty lines should be ignored
        text = f'\n\n{test_sentence}\n\n\n0\n\n\n',
        lang = lang,
        sentence_tokenizer = sentence_tokenizer
    )

    print(f'{sentences}\n')

    # The count of sentences should be exactly 3
    match lang:
        case 'ara' | 'chu' | 'cop' | 'fro' | 'pcm' | 'qpm':
            assert len(sentences) == 2
        case 'hrv':
            if sentence_tokenizer == 'spacy_sentence_recognizer_hrv':
                assert len(sentences) == 2
            else:
                assert len(sentences) == 3
        case 'dan' | 'ita' | 'nob' | 'por_br' | 'por_pt':
            if sentence_tokenizer in {
                'spacy_dependency_parser_dan',
                'spacy_dependency_parser_ita',
                'spacy_dependency_parser_nob',
                'spacy_dependency_parser_por',
                'spacy_sentence_recognizer_dan',
                'spacy_sentence_recognizer_ita',
                'spacy_sentence_recognizer_nob',
                'spacy_sentence_recognizer_por'
            }:
                assert len(sentences) == 3
            else:
                assert len(sentences) == 4
        case 'eng_gb' | 'eng_us' | 'srp_cyrl' | 'srp_latn' | 'other':
            if sentence_tokenizer in {
                'spacy_dependency_parser_eng',
                'spacy_sentence_recognizer_eng',
                'spacy_sentencizer'
            }:
                assert len(sentences) == 2
            else:
                assert len(sentences) == 3
        case 'ell':
            match sentence_tokenizer:
                case 'spacy_dependency_parser_ell':
                    assert len(sentences) == 5
                case 'spacy_sentence_recognizer_ell':
                    assert len(sentences) == 4
                case _:
                    assert len(sentences) == 3
        case 'grc' | 'snd':
            assert len(sentences) == 5
        case 'swe':
            if sentence_tokenizer == 'spacy_dependency_parser_swe':
                assert len(sentences) == 4
            else:
                assert len(sentences) == 3
        case 'tha':
            match sentence_tokenizer:
                case 'pythainlp_crfcut':
                    assert len(sentences) == 4
                case 'pythainlp_thaisumcut':
                    assert len(sentences) == 6
                case _:
                    assert len(sentences) == 3
        case _:
            assert len(sentences) == 3

    assert sentences == [*results, '0']

def test_sentence_terminators():
    num_sentence_terminators = len(wl_sentence_tokenization.SENTENCE_TERMINATORS)

    for i, char in enumerate(wl_sentence_tokenization.SENTENCE_TERMINATORS):
        assert char < '\U00020000'

        if i < num_sentence_terminators - 1:
            char_next = wl_sentence_tokenization.SENTENCE_TERMINATORS[i + 1]

            assert char < char_next, f'Wrong order for {hex(ord(char))} and {hex(ord(char_next))}!'

@pytest.mark.parametrize('lang', langs_sentence_split)
def test_sentence_split(lang):
    sentences_split = wl_sentence_tokenization.wl_sentence_split(
        main,
        text = ''.join(getattr(wl_test_lang_examples, f'TEXT_{lang.upper()}')),
        lang = lang
    )

    print(f'{lang} / Sentence Splitter - Length: {len(sentences_split)}')

    if len(sentences_split) != 2:
        print(sentences_split)

    assert all(sentences_split)

    match lang:
        case 'ara' | 'eus' | 'chu' | 'cop' | 'hrv' | 'eng_gb' | 'eng_us' | 'hbo' | 'isl' | 'ind' | 'orv' | 'srp_cyrl' | 'srp_latn' | 'tha' | 'xct' | 'bod' | 'tur' | 'other':
            assert len(sentences_split) == 1
        case 'xcl' | 'dan' | 'est' | 'grc' | 'kaz' | 'kpv' | 'pcm' | 'nno' | 'slk':
            assert len(sentences_split) == 3
        case 'mya' :
            assert len(sentences_split) == 4
        case _:
            assert len(sentences_split) == 2

def test_sentence_seg_terminators():
    num_sentence_seg_terminators = len(wl_sentence_tokenization.SENTENCE_SEG_TERMINATORS)

    for i, char in enumerate(wl_sentence_tokenization.SENTENCE_SEG_TERMINATORS):
        assert char < '\U00020000'

        if i < num_sentence_seg_terminators - 1:
            char_next = wl_sentence_tokenization.SENTENCE_SEG_TERMINATORS[i + 1]

            assert char < char_next, f'Wrong order for {hex(ord(char))} and {hex(ord(char_next))}!'

@pytest.mark.parametrize('lang', langs_sentence_split)
def test_sentence_seg_tokenize(lang):
    sentence_segs = wl_sentence_tokenization.wl_sentence_seg_tokenize(
        main,
        text = ''.join(getattr(wl_test_lang_examples, f'TEXT_{lang.upper()}'))
    )

    print(f'{lang} / Sentence Segment Tokenizer:')
    print(f'{sentence_segs}\n')

    assert all(sentence_segs)

    if lang not in {'chu', 'cop', 'orv', 'tha'}:
        assert len(sentence_segs) > 1
    else:
        assert len(sentence_segs) == 1

    match lang:
        case 'afr':
            assert sentence_segs == ["Afrikaans is tipologies beskou 'n Indo-Europese,", 'Wes-Germaanse,', 'Nederfrankiese taal,', '[2] wat aan die suidpunt van Afrika onder invloed van verskeie ander tale en taalgroepe ontstaan het.', "Afrikaans is op 8 Mei 1925 as 'n amptelike taal van Suid-Afrika erken en is tans die derde jongste Germaanse taal wat amptelike status geniet,", 'naas Faroëes wat in 1948 grondwetlik erken is en Luxemburgs wat hierdie status in 1984 verkry het.']
        case 'sqi':
            assert sentence_segs == ['Keto gjuhe kryesisht perdoret në Shqipëri,', 'Kosovë dhe Maqedoninë e Veriut,', 'por edhe në zona të tjera të Evropës Juglindore ku ka një popullsi shqiptare,', 'duke përfshirë Malin e Zi dhe Luginën e Preshevës.', 'Shqipja është gjuha zyrtare e Shqipërisë dhe Kosovës,', 'gjuhë bashkë-zyrtare e Maqedonisë së Veriut si dhe një nga gjuhët zyrtare e Malit të Zi.']
        case 'ara':
            assert sentence_segs == ['ٱللُّغَةُ ٱلْعَرَبِيَّة هي أكثر اللغات السامية تحدثًا،', 'وإحدى أكثر اللغات انتشاراً في العالم،', 'يتحدثها أكثر من 467 مليون نسمة.', '(1) ويتوزع متحدثوها في الوطن العربي،', 'بالإضافة إلى العديد من المناطق الأخرى المجاورة كالأحواز وتركيا وتشاد ومالي والسنغال وإرتيريا وإثيوبيا وجنوب السودان وإيران.']
        case 'xcl':
            assert sentence_segs == ['Զգոյշ լերուք ողորմութեան ձերում՝ մի առնել առաջի մարդկան՝ որպէս թե ի ցոյց ինչ նոցա,', 'գուցէ եւ վարձս ոչ ընդունիցիք ի հաւրէ ձերմէ որ յերկինսն է:', 'Այղ յորժամ առնիցես ողորմութիւն,', 'մի հարկաներ փող առաջի քո.', 'որպէս կեղծաւորքն առնեն ի ժողովուրդս եւ ի հրապարակս.', 'որպէս զի փառաւորեսցին ի մարդկանէ:']
        case 'hye' | 'hyw':
            assert sentence_segs == ['Հայերեն (ավանդական՝ հայերէն),', 'հնդեվրոպական լեզվաընտանիքի առանձին ճյուղ հանդիսացող լեզու։', 'Հայաստանի և Արցախի պետական լեզուն է։']
        case 'eus':
            assert sentence_segs == ['Euskara Euskal Herriko hizkuntza da.', '[8] Hizkuntza bakartua da,', 'ez baitzaio ahaidetasunik aurkitu.']
        case 'bel':
            assert sentence_segs == ['Белару́ская мо́ва — нацыянальная мова беларусаў,', 'уваходзіць у індаеўрапейскую моўную сям’ю,', 'славянскую групу,', 'усходнеславянскую падгрупу.', 'Пашырана ў асноўным у Беларусі.']
        case 'bul':
            assert sentence_segs == ['Бъ̀лгарският езѝк е индоевропейски език от групата на южнославянските езици,', 'като образува неговата източна подгрупа.', 'Той е официалният език на Република България и един от 24-те официални езика на Европейския съюз.']
        case 'mya':
            assert sentence_segs == ['မြန်မာဘာသာ (အင်္ဂလိပ်:', 'Myanmar Language)သည် မြန်မာနိုင်ငံ၏ ရုံးသုံး ဘာသာစကားဖြစ်သည။', 'ဗမာလူမျိုးနှင့် ဗမာနွယ်ဝင်(ဓနု၊', 'အင်းသား၊', 'တောင်ရိုးနှင့် ယော)တို့၏ ဇာတိစကားဖြစ်သည်။']
        case 'bxr':
            assert sentence_segs == ['Буряад хэлэн (буряад-монгол хэлэн) Алтайн хэлэнэй изагуурай буряад арад түмэнһөө хэрэглэгдэжэ бай монгол хэлэнэй бүлэгэй xэлэн-аялгуу юм.', 'Бүгэдэ Найрамдаха Буряад Улас,', 'Эрхүү можо,', 'Забайкалиин хизаар,', 'Усть-Ордын болон Агын тойрогууд,', 'мүн Монгол Уласай хойто аймагууд,', 'Хитадай зүүн-хойто орондо ажаһуудаг буряадууд хэлэлсэдэг.']
        case 'cat':
            assert sentence_segs == ['Hi ha altres glotònims tradicionals que es fan servir com a sinònim de "català" al llarg del domini lingüístic.', 'Així,', 'per exemple,', "a l'Alguer se li diu alguerès,", 'a Fraga,', 'fragatí,', 'a Maella,', 'maellà i a la comarca de la Llitera,', 'lliterà.']
        case 'lzh':
            assert sentence_segs == ['文言者，', '華夏、', '四裔所以書其言，', '而述志表情也。', '先民言語，', '傳乎口耳，', '至結繩以記，', '事日贅，', '是結繩之不足，', '求諸繪圖，', '繪圖猶逾，', '而創字製文，', '金石竹帛載之，', '自劉漢而書諸紙。']
        case 'zho_cn':
            assert sentence_segs == ['汉语又称华语[6][7]，', '是来自汉民族的语言[8][7][9]。', '汉语是汉藏语系中最大的一支语族，', '若把整个汉语族视为单一语言，', '则汉语为世界上母语使用者人数最多的语言，', '目前全世界有五分之一人口将其作为母语或第二语言。']
        case 'zho_tw':
            assert sentence_segs == ['漢語又稱華語[6][7]，', '是來自漢民族的語言[8][7][9]。', '漢語是漢藏語系中最大的一支語族，', '若把整個漢語族視為單一語言，', '則漢語為世界上母語使用者人數最多的語言，', '目前全世界有五分之一人口將其作為母語或第二語言。']
        case 'chu':
            assert sentence_segs == ['ВЪ И҃ В҃ ДЬНЬ КЛꙆМЕНТА Бъ҃ ꙇже нъи лѣта огрѧдѫцѣ блаженаго климента мѫченіка твоего ꙇ папежа чьстьѭ веселішꙇ подазь мілостівъі да егоже чьсть чьстімъ сілоѭ ѹбо мѫчениѣ его наслѣдѹемъ г҃мь']
        case 'cop':
            assert sentence_segs == ['ϭⲟⲗ · ⲛⲉⲛⲧⲁⲩⲕⲗⲏⲣⲟⲛⲟⲙⲉⲓ ⲉⲛⲉϩ ⲛⲧⲙⲛⲧⲣⲣⲟ ⲙⲡⲛⲟⲩⲧⲉ ·']
        case 'hrv':
            assert sentence_segs == ['Hrvatski jezik obuhvaća govoreni i pisani hrvatski standardni jezik i sve narodne govore kojima govore i pišu Hrvati.', '[4] Povijesno,', 'obuhvaća sve govore i sve književne jezike izgrađene na tim govorima,', 'kojima su se služili Hrvati.', '[5][6]']
        case 'ces':
            assert sentence_segs == ['Čeština neboli český jazyk je západoslovanský jazyk,', 'nejbližší slovenštině,', 'poté lužické srbštině a polštině.', 'Patří mezi slovanské jazyky,', 'do rodiny jazyků indoevropských.']
        case 'dan':
            assert sentence_segs == ['Dansk er et østnordisk sprog indenfor den germanske gren af den indoeuropæiske sprogfamilie.', 'Det danske sprog tales af ca.', 'seks millioner mennesker,', 'hovedsageligt i Danmark,', 'men også i Sydslesvig,', 'på Færøerne og Grønland.', '[1]']
        case 'nld':
            assert sentence_segs == ['Het Nederlands is een West-Germaanse taal,', 'de meest gebruikte taal in Nederland en België,', 'de officiële taal van Suriname en een van de drie officiële talen van België.', 'Binnen het Koninkrijk der Nederlanden is het Nederlands ook een officiële taal van Aruba,', 'Curaçao en Sint-Maarten.']
        case 'ang':
            assert sentence_segs == ['Ænglisc geþeode bið Westgermanisc geþeode on hwelc spræcon Engle swelce of 450 oþ 1150 gear.', 'Ænglisc boccræft ætiewde on seofoþe gearhundred.']
        case 'eng_gb' | 'eng_us' | 'other':
            assert sentence_segs == ['English is a West Germanic language in the Indo-European language family,', 'whose speakers,', 'called Anglophones,', 'originated in early medieval England on the island of Great Britain.', '[4][5][6] The namesake of the language is the Angles,', 'one of the Germanic peoples that migrated to Britain after its Roman occupiers left.']
        case 'myv':
            assert sentence_segs == ['Э́рзянь кель те уралонь кель,', 'кона совавтови суоми-угрань келень семиянть суоминь-равонь тарадонтень.', 'Эрзянь кельсэ кортыть эрзят.']
        case 'est':
            assert sentence_segs == ['Eesti keel (varasem nimetus maakeel) on läänemeresoome lõunarühma kuuluv keel.', 'Eesti keel on Eesti riigikeel ja 2004.', 'aastast ka üks Euroopa Liidu ametlikke keeli.']
        case 'fao':
            assert sentence_segs == ['Føroyskt er høvuðsmálið í Føroyum.', 'Føroyskt er almenna málið í Føroyum,', 'og tað er tjóðarmál føroyinga.']
        case 'fin':
            assert sentence_segs == ['Suomen kieli eli suomi on uralilaisten kielten itämerensuomalaiseen ryhmään kuuluva kieli,', 'jota puhuvat pääosin suomalaiset.', 'Suomessa suomen kieltä puhuu äidinkielenään 4,', '8 miljoonaa ja toisena kielenään 0,', '5 miljoonaa ihmistä.']
        case 'fra':
            assert sentence_segs == ['Le français est une langue indo-européenne de la famille des langues romanes dont les locuteurs sont appelés « francophones ».', "Il est la cinquième langue parlée au monde après l'anglais,", 'le mandarin,', "le hindi et l'espagnol."]
        case 'fro':
            assert sentence_segs == ["Si l'orrat Carles,", 'ki est as porz passant.', 'Je vos plevis,', 'ja returnerunt Franc.']
        case 'glg':
            assert sentence_segs == ['O galego ([ɡaˈleɣo̝][1]) é unha lingua indoeuropea que pertence á póla de linguas románicas.', 'É a lingua propia de Galicia,', '[5] onde é falada por uns 2,', '4 millóns de galegos.', '[6]']
        case 'kat':
            assert sentence_segs == ['ქართული ენა — ქართველურ ენათა ოჯახის ენა.', 'ქართველების მშობლიური ენა,', 'საქართველოს სახელმწიფო ენა (აფხაზეთის ავტონომიურ რესპუბლიკაში,', 'მასთან ერთად სახელმწიფო ენად აღიარებულია აფხაზური ენა).']
        case 'deu_at' | 'deu_de' | 'deu_ch':
            assert sentence_segs == ['Die deutsche Sprache oder Deutsch [dɔɪ̯tʃ][24] ist eine westgermanische Sprache,', 'die weltweit etwa 90 bis 105 Millionen Menschen als Muttersprache und weiteren rund 80 Millionen als Zweit- oder Fremdsprache dient.', 'Das Deutsche ist eine plurizentrische Sprache,', 'enthält also mehrere Standardvarietäten in verschiedenen Regionen.']
        case 'nds':
            assert sentence_segs == ['Plattdüütsch,', 'kort Platt,', 'ook Nedderdüütsch oder Neddersassisch heten,', 'is ene Regionaalspraak un Dialektgrupp,', 'de rund 2 Minschen in Noorddüütschland un an de 2 Millionen Minschen in Oostnedderland snackt.', 'Besünners mit dat mennistsche Plautdietsch het sik de Spraak ook weltwied uutbreidt.']
        case 'got':
            assert sentence_segs == ['𐌲𐌿𐍄𐌰𐍂𐌰𐌶𐌳𐌰,', '𐌲𐌿𐍄𐍂𐌰𐌶𐌳𐌰 𐌰𐌹𐌸𐌸𐌰𐌿 𐌲𐌿𐍄𐌹𐍃𐌺𐌰 𐍂𐌰𐌶𐌳𐌰 𐌹𐍃𐍄 𐌲𐌰𐍃𐍅𐌿𐌻𐍄𐌰𐌽𐌰 𐌰𐌿𐍃𐍄𐍂𐌰𐌲𐌰𐌹𐍂𐌼𐌰𐌽𐌹𐍃𐌺𐌰 𐍂𐌰𐌶𐌳𐌰 𐍂𐍉𐌳𐌹𐌳𐌰 𐍆𐍂𐌰𐌼 𐌲𐌿𐍄𐌰𐌼.', '𐍃𐌹 𐌹𐍃𐍄 𐌰𐌹𐌽𐌰𐌷𐍉 𐌰𐌿𐍃𐍄𐍂𐌰𐌲𐌰𐌹𐍂𐌼𐌰𐌽𐌹𐍃𐌺𐌰 𐍂𐌰𐌶𐌳𐌰 𐍃𐍉𐌴𐌹 𐌷𐌰𐌱𐌰𐌹𐌸 𐌲𐌰𐌼𐌴𐌻𐌴𐌹𐌽𐌹𐌽𐍃.']
        case 'grc':
            assert sentence_segs == ['ἦλθον δὲ οἱ δύο ἄγγελοι εἰς Σόδομα ἑσπέρας· Λὼτ δὲ ἐκάθητο παρὰ τὴν πύλην Σοδόμων.', 'ἰδὼν δὲ Λὼτ ἐξανέστη εἰς συνάντησιν αὐτοῖς καὶ προσεκύνησεν τῷ προσώπῳ ἐπὶ τὴν γῆν καὶ εἶπεν,', 'ἰδού,', 'κύριοι,', 'ἐκκλίνατε εἰς τὸν οἶκον τοῦ παιδὸς ὑμῶν καὶ καταλύσατε καὶ νίψασθε τοὺς πόδας ὑμῶν,', 'καὶ ὀρθρίσαντες ἀπελεύσεσθε εἰς τὴν ὁδὸν ὑμῶν.', 'εἶπαν δέ,', 'οὐχί,', 'ἀλλ᾿ ἐν τῇ πλατείᾳ καταλύσομεν.']
        case 'ell':
            assert sentence_segs == ['Η ελληνική γλώσσα ανήκει στην ινδοευρωπαϊκή οικογένεια[9] secεπίσης στο βαλκανικό γλωσσικό δεσμό.', 'ελληνική γλώσσα,', 'έχουμε γραπτά κείμενα ήδη από τον 15ο αιώνα π.', 'Χ..']
        case 'hbo':
            assert sentence_segs == ['וַ֠יָּבֹאוּ שְׁנֵ֨י הַמַּלְאָכִ֤ים סְדֹ֨מָה֙ בָּעֶ֔רֶב וְלֹ֖וט יֹשֵׁ֣ב בְּשַֽׁעַר־סְדֹ֑ם וַיַּרְא־לֹוט֙ וַיָּ֣קָם לִקְרָאתָ֔ם וַיִּשְׁתַּ֥חוּ אַפַּ֖יִם אָֽרְצָה׃', 'וַיֹּ֜אמֶר הִנֶּ֣ה נָּא־אֲדֹנַ֗י ס֣וּרוּ נָ֠א אֶל־בֵּ֨ית עַבְדְּכֶ֤ם וְלִ֨ינוּ֙ וְרַחֲצ֣וּ רַגְלֵיכֶ֔ם וְהִשְׁכַּמְתֶּ֖ם וַהְלַכְתֶּ֣ם לְדַרְכְּכֶ֑ם וַיֹּאמְר֣וּ לֹּ֔א כִּ֥י בָרְחֹ֖וב נָלִֽין׃']
        case 'heb':
            assert sentence_segs == ['עִבְרִית היא שפה שמית,', 'ממשפחת השפות האפרו-אסייתיות,', 'הידועה כשפתם של היהודים ושל השומרונים.', 'היא שייכת למשפחת השפות הכנעניות והשפה הכנענית היחידה המדוברת כיום.']
        case 'hin':
            assert sentence_segs == ['हिन्दी या आधुनिक मानक हिन्दी विश्व की एक प्रमुख भाषा है और भारत की एक राजभाषा है।', 'केन्द्रीय स्तर पर भारत में सह-आधिकारिक भाषा अंग्रेज़ी है।']
        case 'hun':
            assert sentence_segs == ['A magyar nyelv az uráli nyelvcsalád tagja,', 'azon belül a finnugor nyelvek közé tartozó ugor nyelvek egyike.', 'Legközelebbi rokonai a manysi és a hanti nyelv,', 'majd utánuk az udmurt,', 'a komi,', 'a mari és a mordvin nyelvek.']
        case 'isl':
            assert sentence_segs == ['Íslenska er vesturnorrænt,', 'germanskt og indóevrópskt tungumál sem er einkum talað og ritað á Íslandi og er móðurmál langflestra Íslendinga.', '[6] Það hefur tekið minni breytingum frá fornnorrænu en önnur norræn mál[6] og er skyldara norsku og færeysku en sænsku og dönsku.', '[3][4]']
        case 'ind':
            assert sentence_segs == ['Bahasa Indonesia ([baˈhasa indoˈnesija]) merupakan bahasa resmi sekaligus bahasa nasional di Indonesia.', '[16] Bahasa Indonesia merupakan varietas yang dibakukan dari bahasa Melayu,', '[17] sebuah bahasa rumpun Austronesia yang digolongkan ke dalam rumpun Melayik yang sendirinya merupakan cabang turunan dari cabang Melayu-Polinesia.']
        case 'gle':
            assert sentence_segs == ['Labhraítear in Éirinn go príomha í,', 'ach tá cainteoirí Gaeilge ina gcónaí in áiteanna eile ar fud an domhain.', 'Is í an teanga náisiúnta nó dhúchais agus an phríomhtheanga oifigiúil i bPoblacht na hÉireann í an Ghaeilge.']
        case 'ita':
            assert sentence_segs == ["L'italiano è una lingua romanza parlata principalmente in Italia.", 'Per ragioni storiche e geografiche,', "l'italiano è la lingua romanza meno divergente dal latino (complessivamente a pari merito,", 'anche se in parametri diversi,', 'con la lingua sarda).', '[2][3][4][5]']
        case 'jpn':
            assert sentence_segs == ['日本語（にほんご、', 'にっぽんご[注釈 3]）は、', '日本国内や、', 'かつての日本領だった国、', 'そして国外移民や移住者を含む日本人同士の間で使用されている言語。', '日本は法令によって公用語を規定していないが、', '法令その他の公用文は全て日本語で記述され、', '各種法令[注釈 4]において日本語を用いることが規定され、', '学校教育においては「国語」の教科として学習を行うなど、', '事実上日本国内において唯一の公用語となっている。']
        case 'kaz':
            assert sentence_segs == ['Қазақ тілі (төте:', 'قازاق ٴتىلى\u200e,', 'латын:', 'qazaq tılı) — Қазақстан Республикасының мемлекеттік тілі,', 'сонымен қатар Ресей,', 'Өзбекстан,', 'Қытай,', 'Моңғолия жəне т.', 'б.', 'елдерде тұратын қазақтардың ана тілі.', 'Қазақ тілі түркі тілдерінің қыпшақ тобына,', 'соның ішінде қарақалпақ,', 'ноғай,', 'қарашай тілдерімен бірге қыпшақ-ноғай тармағына жатады.']
        case 'khm':
            assert sentence_segs == ['ភាសាខ្មែរ គឺជាភាសាកំណើតរបស់ជនជាតិខ្មែរនិងជាភាសាផ្លូវការរបស់ប្រទេសកម្ពុជា។', 'ភាសាសំស្ក្រឹតនិងភាសាបាលីបានជួយបង្កើតខេមរភាសា ព្រោះភាសាខ្មែរបានខ្ចីពាក្យច្រើនពីភាសាទាំងពីរនេះ។']
        case 'kpv':
            assert sentence_segs == ['Коми кыв — финн-йӧгра кывъясысь ӧти,', 'коми войтырлӧн чужан кыв.', 'Коми кывйын кызь гӧгӧр сёрнисикас да кык гижӧда кыв:', 'зырян коми да перым коми.', 'Коми кыв — Коми Республикаын каналан кыв (кыдзи и роч кыв).']
        case 'kor':
            assert sentence_segs == ['한국어(韓國語),', '조선어(朝鮮語)는 대한민국과 조선민주주의인민공화국의 공용어이다.', '둘은 표기나 문법,', '동사 어미나 표현에서 약간의 차이가 있다.']
        case 'kmr':
            assert sentence_segs == ['Kurmancî,', 'kurdiya jorîn yan jî kurdiya bakurî yek ji zaravayên zimanê kurdî ye ku ji aliyê kurdan ve tê axaftin.', 'Zaravayê kurmancî zimanê herî berfireh ê Kurdistanê ye ku li her çar parçeyên Kurdistanê bi awayekî berfireh tê axavtin.']
        case 'kir':
            assert sentence_segs == ['Кыргыз тили — Кыргыз Республикасынын мамлекеттик тили,', 'түрк тилдери курамына,', 'анын ичинде кыргыз-кыпчак же тоо-алтай тобуна кирет.', 'Кыргыз Республикасынын түптүү калкынын,', 'Кытайдагы,', 'Өзбекстан,', 'Тажикстан Республикасында Ооганстан,', 'Түркия,', 'Орусияда жашап жаткан кыргыздардын эне тили.']
        case 'lao':
            assert sentence_segs == ['ພາສາລາວສືບທອດມາຈາກພາສາຕະກຸນໄຕ-ກະໄດ ຢູ່ພາກໃຕ້ຂອງປະເທດຈີນ ເຊິ່ງເປັນຈຸດເດີມຂອງຫຼາຍພາສາໃນຕະກຸນນີ້ທີ່ຍັງຖືກໃຊ້ ແລະ ຖືກເວົ້າຢູ່ໂດຍຫຼາຍຊົນເຜົ່າໃນປັດຈຸບັນ.', 'ເນື່ອງຈາກຖືກຄວາມກົດດັນຈາກການຂະຫຍາຍຕົວຂອງອານາຈັກຈີນ,', 'ການບຸກຮຸກຮານຂອງຊາວມົງໂກລີ ແລະ ການປູກຝັງທຳມາຫາກິນ,', 'ຄົນໄຕ (ໄທ) ໄດ້ຍົກຍ້າຍລົງມາທາງໃຕ້ກະຈາຍໄປຕາມແຫຼ່ງທໍາມາຫາກິນທີ່ເໝາະສົມກັບຕົນ.']
        case 'lat':
            assert sentence_segs == ['Latīnum,', 'lingua Latīna,', '[1] sive sermō Latīnus,', '[2] est lingua Indoeuropaea qua primum Latini universi et Romani antiqui in primis loquebantur quamobrem interdum etiam lingua Latia[3] (in Latio enim sueta) et lingua Rōmāna[4] (nam imperii Romani sermo sollemnis) appellabatur.', 'Nomen linguae ductum est a terra quam gentes Latine loquentes incolebant,', 'Latium vetus interdum appellata,', 'in paeninsula Italica inter Tiberim,', 'Volscos,', 'Appenninum,', 'et mare Inferum sita.']
        case 'lav':
            assert sentence_segs == ['Latviešu valoda ir dzimtā valoda apmēram 1,', '5 miljoniem cilvēku,', 'galvenokārt Latvijā,', 'kur tā ir vienīgā valsts valoda.', '[1][3] Lielākās latviešu valodas pratēju kopienas ārpus Latvijas ir Apvienotajā Karalistē,', 'ASV,', 'Īrijā,', 'Austrālijā,', 'Vācijā,', 'Zviedrijā,', 'Kanādā,', 'Brazīlijā,', 'Krievijas Federācijā.', 'Latviešu valoda pieder pie indoeiropiešu valodu saimes baltu valodu grupas.']
        case 'lij':
            assert sentence_segs == ['E variante ciù importanti son o zeneize,', 'o savoneize,', 'o spezzin,', 'o ventemigliusu,', 'o tabarchin,', 'o monegasco,', 'e o noveize,', "dîto ascî lìgure d'Otrazôvo.", 'Tra i dialetti Liguri e o Piemonteise ciù a nord,', "gh'è poi de variante dite de tranxission,", 'comme i dialetti da val Bormia,', 'de Calissan e do Sascello.']
        case 'lit':
            assert sentence_segs == ['Lietuvių kalba – iš baltų prokalbės kilusi lietuvių tautos kalba,', 'kuri Lietuvoje yra valstybinė,', 'o Europos Sąjungoje – viena iš oficialiųjų kalbų.', 'Lietuviškai kalba apie tris milijonus žmonių (dauguma jų gyvena Lietuvoje).']
        case 'mkd':
            assert sentence_segs == ['Македонски јазик — јужнословенски јазик,', 'дел од групата словенски јазици од јазичното семејство на индоевропски јазици.', 'Македонскиот е службен и национален јазик во Македонија,', 'а воедно е и официјално признат како регионален службен јазик во Горица и Пустец во Албанија каде што живее бројно македонско население,', 'но и во Србија како официјален во општините Јабука и Пландиште,', 'Романија и Косово.']
        case 'mal':
            assert sentence_segs == ['ഇതു ദ്രാവിഡ ഭാഷാ കുടുംബത്തിൽപ്പെടുന്നു.', 'ഇന്ത്യയിൽ ശ്രേഷ്ഠഭാഷാ പദവി ലഭിക്കുന്ന അഞ്ചാമത്തെ ഭാഷയാണ് മലയാളം[5].']
        case 'mlt':
            assert sentence_segs == ["Il-Malti huwa l-ilsien nazzjonali tar-Repubblika ta' Malta.", 'Huwa l-ilsien uffiċjali flimkien mal-Ingliż;', "kif ukoll wieħed mill-ilsna uffiċjali u l-uniku wieħed ta' oriġini Għarbija (Semitiku) tal-Unjoni Ewropea."]
        case 'glv':
            assert sentence_segs == ['She Gaelg (graït:', '/gɪlg/) çhengey Ghaelagh Vannin.', 'Haink y Ghaelg woish Shenn-Yernish,', "as t'ee cosoylagh rish Yernish as Gaelg ny h-Albey."]
        case 'mar':
            assert sentence_segs == ['मराठी भाषा ही इंडो-युरोपीय भाषाकुळातील एक भाषा आहे.', 'मराठी ही भारताच्या २२ अधिकृत भाषांपैकी एक आहे.']
        case 'pcm':
            assert sentence_segs == ['Naijá langwej na popula langwej for Naija an pipul wey dey spik am for Naijá pas 75 miliọn.', 'Naijá na pijin,', 'a langwej for oda langwej.', 'Naijá for Inglish an wey Afrikan langwej.']
        case 'nob':
            assert sentence_segs == ['Bokmål er en av to offisielle målformer av norsk skriftspråk,', 'hvorav den andre er nynorsk.', 'I skrift har 87,', '3 % bokmål som hovedmål i skolen.', '[3]']
        case 'nno':
            assert sentence_segs == ['Nynorsk,', 'før 1929 offisielt kalla landsmål,', 'er sidan jamstillingsvedtaket av 12.', 'mai 1885 ei av dei to offisielle målformene av norsk;', 'den andre forma er bokmål.', 'Nynorsk vert i dag nytta av om lag 10–15% av innbyggjarane i Noreg.', '[1][2]']
        case 'fas':
            assert sentence_segs == ['فارسی یا پارسی یکی از زبان\u200cهای ایرانی غربی از زیرگروه ایرانی شاخهٔ هندوایرانیِ خانوادهٔ زبان\u200cهای هندواروپایی است که در کشورهای ایران،', 'افغانستان،', 'تاجیکستان،', 'ازبکستان،', 'پاکستان،', 'عراق،', 'ترکمنستان و آذربایجان به آن سخن می\u200cگویند.', 'فارسی زبان چندکانونی و فراقومی است و زبان رسمی ایران،', 'تاجیکستان و افغانستان به\u200cشمار می\u200cرود.']
        case 'pol':
            assert sentence_segs == ['Język polski,', 'polszczyzna – język lechicki z grupy zachodniosłowiańskiej (do której należą również czeski,', 'kaszubski,', 'słowacki,', 'języki łużyckie czy wymarły język drzewiański),', 'stanowiącej część rodziny indoeuropejskiej.', 'Jest językiem urzędowym w Polsce oraz należy do oficjalnych języków Unii Europejskiej.']
        case 'qpm':
            assert sentence_segs == ['Kážyjte nǽko,', 'de!', 'Še go preskókneme!']
        case 'por_br' | 'por_pt':
            assert sentence_segs == ['A língua portuguesa,', 'também designada português,', 'é uma língua indo-europeia românica flexiva ocidental originada no galego-português falado no Reino da Galiza e no norte de Portugal.', 'Com a criação do Reino de Portugal em 1139 e a expansão para o sul na sequência da Reconquista,', 'deu-se a difusão da língua pelas terras conquistadas e,', 'mais tarde,', 'com as descobertas portuguesas,', 'para o Brasil,', 'África e outras partes do mundo.', '[9]']
        case 'ron':
            assert sentence_segs == ['Limba română ([ˈlimba roˈmɨnə]  ( audio) sau românește [romɨˈneʃte]) este limba oficială și principală a României și a Republicii Moldova.', 'Face parte din subramura orientală a limbilor romanice,', 'un grup lingvistic evoluat din diverse dialecte ale latinei vulgare separate de limbile romanice occidentale între secolele V și VIII.', '[2]']
        case 'rus':
            assert sentence_segs == ['Русский язык (МФА:', '[ˈruskʲɪɪ̯ ɪ̯ɪˈzɨk]о файле)[~ 3] — язык восточнославянской группы славянской ветви индоевропейской языковой семьи,', 'национальный язык русского народа.', 'Является одним из наиболее распространённых языков мира — восьмым среди всех языков мира по общей численности говорящих[5] и седьмым по численности владеющих им как родным (2022)[2].']
        case 'orv':
            assert sentence_segs == ['шаибатъ же ѿ бедерѧ г҃ мсци а ѿ дабылѧ до шаибата в҃ мсца моремъ итьти']
        case 'sme':
            assert sentence_segs == ['Davvisámegiella gullá sámegielaid oarjesámegielaid davvejovkui ovttas julev- ja bihtánsámegielain.', 'Eará oarjesámegielat leat ubmisámegiella ja lullisámegiella.']
        case 'san':
            assert sentence_segs == ['संस्कृतं जगत एकतमातिप्राचीना समृद्धा शास्त्रीया च भाषासु वर्तते।', 'संस्कृतं भारतस्य जगतो वा भाषास्वेकतमा\u200c प्राचीनतमा।']
        case 'gla':
            assert sentence_segs == ["'S i cànan dùthchasach na h-Alba a th' anns a' Ghàidhlig.", "'S i ball den teaghlach de chànanan Ceilteach dhen mheur Ghoidhealach a tha anns a' Ghàidhlig."]
        case 'srp_cyrl':
            assert sentence_segs == ['Српски језик припада словенској групи језика породице индоевропских језика.', '[12] Српски језик је званичан у Србији,', 'Босни и Херцеговини и Црној Гори и говори га око 12 милиона људи.', '[13]']
        case 'srp_latn':
            assert sentence_segs == ['Srpski jezik pripada slovenskoj grupi jezika porodice indoevropskih jezika.', '[12] Srpski jezik je zvaničan u Srbiji,', 'Bosni i Hercegovini i Crnoj Gori i govori ga oko 12 miliona ljudi.', '[13]']
        case 'snd':
            assert sentence_segs == ['سنڌي (/ˈsɪndi/[6]सिन्धी,', 'Sindhi)ھڪ ھند-آريائي ٻولي آھي جيڪا سنڌ جي تاريخي خطي ۾ سنڌي ماڻھن پاران ڳالھائي وڃي ٿي.', 'سنڌي پاڪستان جي صوبي سنڌ جي سرڪاري ٻولي آھي.', '[7][8][9]']
        case 'slk':
            assert sentence_segs == ['Slovenčina patrí do skupiny západoslovanských jazykov (spolu s češtinou,', 'poľštinou,', 'hornou a dolnou lužickou srbčinou a kašubčinou).', 'Slovenčina je oficiálne úradným jazykom Slovenska,', 'Vojvodiny a od 1.', 'mája 2004 jedným z jazykov Európskej únie.']
        case 'slv':
            assert sentence_segs == ['Slovenščina [sloˈʋenʃtʃina] je združeni naziv za uradni knjižni jezik Slovencev in skupno ime za narečja in govore,', 'ki jih govorijo ali so jih nekoč govorili Slovenci.', 'Govori ga okoli 2,', '5 (dva in pol) milijona govorcev po svetu,', 'od katerih jih večina živi v Sloveniji.']
        case 'hsb':
            assert sentence_segs == ['Hornjoserbšćina je zapadosłowjanska rěč,', 'kotraž so w Hornjej Łužicy wokoło městow Budyšin,', 'Kamjenc a Wojerecy rěči.', 'Wona je přiwuzna z delnjoserbšćinu w susodnej Delnjej Łužicy,', 'čěšćinu,', 'pólšćinu,', 'słowakšćinu a kašubšćinu.']
        case 'spa':
            assert sentence_segs == ['El español o castellano es una lengua romance procedente del latín hablado,', 'perteneciente a la familia de lenguas indoeuropeas.', 'Forma parte del grupo ibérico y es originaria de Castilla,', 'reino medieval de la península ibérica.']
        case 'swe':
            assert sentence_segs == ['Svenska (svenska\u2009(fil)) är ett östnordiskt språk som talas av ungefär tio miljoner personer,', 'främst i Sverige där språket har en dominant ställning som huvudspråk,', 'men även som det ena nationalspråket i Finland och som enda officiella språk på Åland.', 'I övriga Finland talas det som modersmål framförallt i de finlandssvenska kustområdena i Österbotten,', 'Åboland och Nyland.']
        case 'tam':
            assert sentence_segs == ['தமிழ் (Tamil language) தமிழர்களினதும் தமிழ் பேசும் பலரின் தாய்மொழி ஆகும்.', 'தமிழ்,', 'உலகில் உள்ள முதன்மையான மொழிகளில் ஒன்றும் செம்மொழியும் ஆகும்.']
        case 'tel':
            assert sentence_segs == ['తెలుగు ఆంధ్ర,', 'తెలంగాణ రాష్ట్రాలలో మున్నధికారిక నుడి.', 'ఇది ద్రావిడ కుటుంబానికి చెందిన నుడి.']
        case 'tha':
            assert sentence_segs == ['ภาษาไทย หรือ ภาษาไทยกลาง เป็นภาษาในกลุ่มภาษาไท สาขาย่อยเชียงแสน ซึ่งเป็นกลุ่มย่อยของตระกูลภาษาขร้า-ไท และเป็นภาษาราชการ และภาษาประจำชาติของประเทศไทย[3][4] มีการสันนิษฐานว่าภาษาในตระกูลนี้มีถิ่นกำเนิดจากทางตอนใต้ของประเทศจีน และนักภาษาศาสตร์บางส่วนเสนอว่า ภาษาไทยน่าจะมีความเชื่อมโยงกับตระกูลภาษาออสโตร-เอเชียติก ตระกูลภาษาออสโตรนีเซียน และตระกูลภาษาจีน-ทิเบต']
        case 'xct' | 'bod':
            assert sentence_segs == ['བོད་ཀྱི་སྐད་ཡིག་ནི་བོད་ཡུལ་དང་ཉེ་འཁོར་གྱི་ས་ཁུལ་བལ་ཡུལ།', 'འབྲུག་དང་འབྲས་ལྗོངས།', 'ལ་དྭགས་ནས་ལྷོ་མོན་རོང་སོགས་སུ་བེད་སྤྱོད་བྱེད་པའི་སྐད་ཡིག་དེ།', 'ད་ཆར་ཡོངས་གྲགས་སུ་བོད་ཀྱི་ཡུལ་གྲུ་སྟོད་སྨད་བར་གསུམ་ལ་ལྟོས་ཏེ་ནང་གསེས་རིགས་གསུམ་དུ་ཕྱེ་བ་སྟེ།']
        case 'tur':
            assert sentence_segs == ['Türkçe ya da Türk dili,', "Güneydoğu Avrupa ve Batı Asya'da konuşulan,", 'Türk dilleri dil ailesine ait sondan eklemeli bir dildir.', '[10] Türk dilleri ailesinin Oğuz dilleri grubundan bir Batı Oğuz dili olan Osmanlı Türkçesinin devamını oluşturur.']
        case 'ota':
            assert sentence_segs == ['Musahabeme nihayet vermeden evvel edebiyat-ı hazıra-ı ricalden ziyade edebiyat-ı nisvanın bir feyz-i latife mazhar olduğunu söylemek isterim .', 'En başında Halide Salih Hanımefendi olduğu hâlde Nesl-i Cedid Edibelerinin ateşîn musahebelerini ,', 'rengîn mensur şiirlerini ,', 'teşrih-i ruha dair küçük hikâyelerini okudum .']
        case 'ukr':
            assert sentence_segs == ['Украї́нська мо́ва (МФА:', '[ʊkrɐˈjinʲsʲkɐ ˈmɔʋɐ],', 'історична назва — ру́ська[10][11][12][* 1]) — національна мова українців.', "Належить до східнослов'янської групи слов'янських мов,", "що входять до індоєвропейської мовної сім'ї,", 'поряд із романськими,', 'германськими,', 'кельтськими,', 'грецькою,', 'албанською,', "вірменською та найближче спорідненими зі слов'янськими балтійськими мовами[13][14][* 2]."]
        case 'urd':
            assert sentence_segs == ['اُردُو،', 'برصغیر پاک و ہند کی معیاری زبانوں میں سے ایک ہے۔', 'یہ پاکستان کی قومی اور رابطہ عامہ کی زبان ہے،', 'جبکہ بھارت کی چھ ریاستوں کی دفتری زبان کا درجہ رکھتی ہے۔']
        case 'uig':
            assert sentence_segs == ['ئۇيغۇر تىلى ئۇيغۇر جۇڭگو شىنجاڭ ئۇيغۇر ئاپتونوم رايونىنىڭ ئېيتقان بىر تۈركىي تىلى.', 'ئۇ ئۇزاق ئەسىرلىك تەرەققىيات داۋامىدا قەدىمكى تۈركىي تىللار دەۋرى،', 'ئورخۇن ئۇيغۇر تىلى دەۋرى،', 'ئىدىقۇت-خاقانىيە ئۇيغۇر تىلى دەۋرى،', 'چاغاتاي ئۇيغۇر تىلى دەۋرىنى بېسىپ ئۆتكەن.']
        case 'vie':
            assert sentence_segs == ['Tiếng Việt hay tiếng Kinh là một ngôn ngữ thuộc ngữ hệ Nam Á,', 'được công nhận là ngôn ngữ chính thức tại Việt Nam.', 'Đây là tiếng mẹ đẻ của khoảng 85% dân cư Việt Nam cùng với hơn 4 triệu người Việt kiều.']
        case 'cym':
            assert sentence_segs == ["Aelod o'r gangen Frythonaidd o'r ieithoedd Celtaidd a siaredir yn frodorol yng Nghymru,", 'gan Gymry a phobl eraill ar wasgar yn Lloegr,', 'a chan gymuned fechan yn Y Wladfa,', "yr Ariannin[8] yw'r Gymraeg (hefyd Cymraeg heb y fannod).", 'Yng Nghyfrifiad y DU (2011),', 'darganfuwyd bod 19% (562,', '000) o breswylwyr Cymru (tair blwydd a throsodd) yn gallu siarad Cymraeg.']
        case 'wol':
            assert sentence_segs == ['Wolof làkk la wu ñuy wax ci Gàmbi (Gàmbi Wolof),', 'Gànnaar (Gànnaar Wolof),', 'ak Senegaal (Senegaal Wolof).', 'Mi ngi bokk nag moom wolof ci bànqaasub atlas bu làkki Kongóo yu kojug nit ñu ñuul ñi.']
        case _:
            raise wl_test_init.Wl_Exc_Tests_Lang_Skipped(lang)

@pytest.mark.parametrize('lang', langs_sentence_split)
def test_sentence_seg_tokenize_tokens(lang):
    tokens = ''.join(getattr(wl_test_lang_examples, f'TEXT_{lang.upper()}')).split()
    sentence_segs = wl_sentence_tokenization.wl_sentence_seg_tokenize_tokens(main, tokens)

    print(f'{lang} / Sentence Segment Tokenizer with tokens - Length: {len(sentence_segs)}')

    if len(sentence_segs) == 1:
        print(sentence_segs)

    assert all(sentence_segs)

    if lang in {
        'lzh', 'zho_cn', 'zho_tw', 'chu', 'cop', 'ind', 'jpn', 'orv', 'tha'
    }:
        assert len(sentence_segs) == 1
    else:
        assert len(sentence_segs) > 1

def test_sentence_tokenize_misc():
    # Sentences and sentence segments should not be split within pre-tokenized tokens
    assert wl_sentence_tokenization.wl_sentence_split(main, text = 'a.b c', lang = 'eng_us') == ['a.b c']
    assert wl_sentence_tokenization.wl_sentence_split(main, text = '试。测试', lang = 'zho_cn') == ['试。', '测试']
    assert wl_sentence_tokenization.wl_sentence_seg_tokenize_tokens(main, tokens = ['a,b', 'c']) == [['a,b', 'c']]

if __name__ == '__main__':
    for lang, sentence_tokenizer in langs_sentence_tokenize:
        test_sentence_tokenize(lang, sentence_tokenizer)

    test_sentence_terminators()

    for lang in langs_sentence_split:
        test_sentence_split(lang)

    test_sentence_seg_terminators()

    for lang in langs_sentence_split:
        test_sentence_seg_tokenize(lang)

    for lang in langs_sentence_split:
        test_sentence_seg_tokenize_tokens(lang)

    test_sentence_tokenize_misc()
