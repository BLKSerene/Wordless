#
# Wordless: Testing - Word Tokenization
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import itertools
import re
import sys

sys.path.append('.')

from wordless_testing import testing_init
from wordless_text import wordless_text_processing
from wordless_utils import wordless_conversion

SENTENCE_AFR = "Afrikaans is tipologies gesien 'n Indo-Europese, Wes-Germaanse, Nederfrankiese taal,[2] wat sy ontstaan aan die suidpunt van Afrika gehad het onder invloed van verskeie ander tale en taalgroepe."
SENTENCE_SQI = 'Gjuha shqipe (ose thjeshtë shqipja) është gjuhë dhe degë e veçantë e familjes indo-evropiane të folur nga më shumë se 6 milionë njerëz[4], kryesisht në Shqipëri, Kosovë dhe Republikën e Maqedonisë, por edhe në zona të tjera të Evropës Jugore ku ka një popullsi shqiptare, duke përfshirë Malin e Zi dhe Luginën e Preshevës.'
SENTENCE_ARA = 'اللُّغَة العَرَبِيّة هي أكثر اللغات تحدثاً ونطقاً ضمن مجموعة اللغات السامية، وإحدى أكثر اللغات انتشاراً في العالم، يتحدثها أكثر من 467 مليون نسمة،[4](1) ويتوزع متحدثوها في الوطن العربي، بالإضافة إلى العديد من المناطق الأخرى المجاورة كالأحواز وتركيا وتشاد ومالي والسنغال وإرتيريا وإثيوبيا وجنوب السودان وإيران.'
SENTENCE_BEN = 'বাংলা ভাষা একটি ইন্দো-আর্য ভাষা, যা দক্ষিণ এশিয়ার বাঙালি জাতির প্রধান কথ্য ও লেখ্য ভাষা।'
SENTENCE_BUL = 'Бъ̀лгарският езѝк е индоевропейски език от групата на южнославянските езици.'
SENTENCE_CAT = "El català (denominació oficial a Catalunya, a les Illes Balears, a Andorra, a la ciutat de l'Alguer i tradicional a Catalunya Nord) o valencià (denominació oficial al País Valencià i tradicional al Carxe) és una llengua romànica parlada per més d'onze milions de persones, a Catalunya, al País Valencià (tret d'algunes comarques i localitats de l'interior), les Illes Balears, Andorra, la Franja de Ponent (a l'Aragó), la ciutat de l'Alguer (a l'illa de Sardenya), la Catalunya del Nord,[8] el Carxe (un petit territori de Múrcia poblat per immigrats valencians),[9][10] i en petites comunitats arreu del món (entre les quals destaca la de l'Argentina, amb 195.000 parlants).[11]"
SENTENCE_ZHO_CN = '汉语，又称中文、华文、唐话[2]，或被视为汉藏语系汉语族下之语言，或被视为语族。'
SENTENCE_ZHO_TW = '漢語，又稱中文、華文、唐話[2]，或被視為漢藏語系漢語族下之語言，或被視為語族。'
SENTENCE_HRV = 'Hrvatski jezik (ISO 639-3: hrv) skupni je naziv za nacionalni standardni jezik Hrvata, te za skup narječja i govora kojima govore ili su nekada govorili Hrvati.'
SENTENCE_CES = 'Čeština neboli český jazyk je západoslovanský jazyk, nejbližší slovenštině, poté lužické srbštině a polštině.'
SENTENCE_DAN = 'Dansk er et nordgermansk sprog af den østnordiske (kontinentale) gruppe, der tales af ca. seks millioner mennesker.'
SENTENCE_NLD = 'Het Nederlands is een West-Germaanse taal en de moedertaal van de meeste inwoners van Nederland, België en Suriname.'
SENTENCE_ENG = 'English is a West Germanic language that was first spoken in early medieval England and eventually became a global lingua franca.[4][5]'
SENTENCE_FIN = 'Suomen kieli (suomi) on uralilaisten kielten itämerensuomalaiseen ryhmään kuuluva kieli.'
SENTENCE_FRA = 'Le français est une langue indo-européenne de la famille des langues romanes.'
SENTENCE_DEU = 'Die deutsche Sprache bzw. Deutsch ([dɔʏ̯t͡ʃ]; abgekürzt Dt. oder Dtsch.) ist eine westgermanische Sprache.'
SENTENCE_ELL = 'Η ελληνική γλώσσα είναι μια από τις ινδοευρωπαϊκές γλώσσες[9] και αποτελεί το μοναδικό μέλος ενός ανεξάρτητου κλάδου, αυτής της οικογένειας γλωσσών, ενώ είναι η επίσημη γλώσσα της Ελλάδος και της Κύπρου.'
SENTENCE_HEB = 'עִבְרִית היא שפה שמית, ממשפחת השפות האפרו-אסיאתיות, הידועה כשפתם של היהודים ושל השומרונים, אשר ניב מודרני שלה (עברית ישראלית) הוא שפתה הרשמית של מדינת ישראל, מעמד שעוגן בשנת 2018 בחוק יסוד: ישראל – מדינת הלאום של העם היהודי.'
SENTENCE_HIN = 'हिंदी विश्व की एक प्रमुख भाषा है एवं भारत की राजभाषा है।'
SENTENCE_HUN = 'A magyar nyelv az uráli nyelvcsalád tagja, a finnugor nyelvek közé tartozó ugor nyelvek egyike.'
SENTENCE_ISL = 'Íslenska er vesturnorrænt, germanskt og indóevrópskt tungumál sem er einkum talað og ritað á Íslandi og er móðurmál langflestra Íslendinga.[4]'
SENTENCE_IND = 'Bahasa Indonesia adalah bentuk standar bahasa Melayu yang dijadikan sebagai bahasa resmi Republik Indonesia[1] dan bahasa persatuan bangsa Indonesia.[2]'
SENTENCE_GLE = 'Is ceann de na teangacha Ceilteacha í an Ghaeilge (nó Gaeilge na hÉireann mar a thugtar uirthi corruair), agus ceann den dtrí cinn de theangacha Ceilteacha ar a dtugtar na teangacha Gaelacha (.i. an Ghaeilge, Gaeilge na hAlban agus Gaeilge Mhanann) go háirithe.'
SENTENCE_ITA = "L'italiano ([itaˈljaːno][Nota 1] ascolta[?·info]) è una lingua romanza parlata principalmente in Italia."
SENTENCE_JPN = '使用人口について正確な統計はないが、日本国内の人口、および日本国外に住む日本人や日系人、日本がかつて統治した地域の一部住民など、約1億3千万人以上と考えられている[7]。'
SENTENCE_KAN = 'ದ್ರಾವಿಡ ಭಾಷೆಗಳಲ್ಲಿ ಪ್ರಾಮುಖ್ಯವುಳ್ಳ ಭಾಷೆಯೂ ಭಾರತದ ಪುರಾತನವಾದ ಭಾಷೆಗಳಲ್ಲಿ ಒಂದೂ ಆಗಿರುವ ಕನ್ನಡ ಭಾಷೆಯನ್ನು ಅದರ ವಿವಿಧ ರೂಪಗಳಲ್ಲಿ ಸುಮಾರು ೪೫ ದಶಲಕ್ಷ ಜನರು ಆಡು ನುಡಿಯಾಗಿ ಬಳಸುತ್ತಲಿದ್ದಾರೆ.'
SENTENCE_LAV = 'Latviešu valoda ir dzimtā valoda apmēram 1,7 miljoniem cilvēku, galvenokārt Latvijā, kur tā ir vienīgā valsts valoda.[3]'
SENTENCE_LIT = 'Lietuvių kalba – daugiausia vartotojų turinti rytų baltų kalba.'
SENTENCE_MAR = 'मराठीभाषा ही इंडो-युरोपीय भाषाकुलातील एक भाषा आहे.'
SENTENCE_NOB = 'Norsk er et nordisk språk som snakkes som morsmål av rundt 5 millioner mennesker,[1][trenger bedre kilde] først og fremst i Norge, hvor det er offisielt språk.'
SENTENCE_FAS = 'فارسی یا پارسی یکی از زبان‌های هندواروپایی در شاخهٔ زبان‌های ایرانی جنوب غربی است که در کشورهای ایران، افغانستان،[۳] تاجیکستان[۴] و ازبکستان[۵] به آن سخن می‌گویند.'
SENTENCE_POL = 'Język polski, polszczyzna, skrót: pol. – język naturalny należący do grupy języków zachodniosłowiańskich (do której należą również czeski, słowacki, kaszubski, dolnołużycki, górnołużycki i wymarły połabski), stanowiącej część rodziny języków indoeuropejskich.'
SENTENCE_POR = 'A língua portuguesa, também designada português, é uma língua românica flexiva ocidental originada no galego-português falado no Reino da Galiza e no norte de Portugal.'
SENTENCE_RON = 'Limba română este o limbă indo-europeană, din grupul italic și din subgrupul oriental al limbilor romanice.'
SENTENCE_RUS = 'Ру́сский язы́к ([ˈruskʲɪi̯ jɪˈzɨk] Информация о файле слушать)[~ 3][⇨] — один из восточнославянских языков, национальный язык русского народа.'
SENTENCE_SRP_CYRL = 'Српски језик припада словенској групи језика породице индоевропских језика.[12]'
SENTENCE_SRP_LATN = 'Srpski jezik pripada slovenskoj grupi jezika porodice indoevropskih jezika.[12]'
SENTENCE_SIN = 'ශ්‍රී ලංකාවේ ප්‍රධාන ජාතිය වන සිංහල ජනයාගේ මව් බස සිංහල වෙයි.'
SENTENCE_SLK = 'Slovenčina patrí do skupiny západoslovanských jazykov (spolu s češtinou, poľštinou, hornou a dolnou lužickou srbčinou a kašubčinou).'
SENTENCE_SLV = 'Slovenščina [slovénščina] / [sloˈʋenʃtʃina] je združeni naziv za uradni knjižni jezik Slovencev in skupno ime za narečja in govore, ki jih govorijo ali so jih nekoč govorili Slovenci.'
SENTENCE_SPA = 'El idioma español o castellano es una lengua romance procedente del latín hablado.'
SENTENCE_SWE = 'Svenska (svenska (info)) är ett östnordiskt språk som talas av drygt elva miljoner personer[källa behövs] främst i Sverige där språket har en dominant ställning som huvudspråk, men även som det ena nationalspråket i Finland och som enda officiella språk på Åland.'
SENTENCE_TGL = 'Ang Wikang Tagalog[2] (Baybayin: ᜏᜒᜃᜅ᜔ ᜆᜄᜎᜓᜄ᜔), na kilala rin sa payak na pangalang Tagalog, ay isa sa mga pangunahing wika ng Pilipinas at sinasabing ito ang de facto ("sa katunayan") ngunit hindî de jure ("sa batas") na batayan na siyang pambansang Wikang Filipino (mula 1961 hanggang 1987: Pilipino).[2]'
SENTENCE_TGK = 'Забони тоҷикӣ — забоне, ки дар Эрон: форсӣ, ва дар Афғонистон дарӣ номида мешавад, забони давлатии кишварҳои Тоҷикистон, Эрон ва Афғонистон мебошад.'
SENTENCE_TAM = 'தமிழ் மொழி (Tamil language) தமிழர்களினதும், தமிழ் பேசும் பலரதும் தாய்மொழி ஆகும்.'
SENTENCE_TAT = 'Татар теле — татарларның милли теле, Татарстанның дәүләт теле, таралышы буенча Русиядә икенче тел.'
SENTENCE_TEL = 'ఆంధ్ర ప్రదేశ్, తెలంగాణ రాష్ట్రాల అధికార భాష తెలుగు.'
SENTENCE_THA = 'ภาษาไทย หรือ ภาษาไทยกลาง เป็นภาษาราชการและภาษาประจำชาติของประเทศไทย'
SENTENCE_BOD = '༄༅། །རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྻ་ཨ་བ་ཏ་ར། བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ། །སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང༌། །ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །བདེ་གཤེགས་སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི། །ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ། །'
SENTENCE_TUR = 'Türkçe ya da Türk dili, batıda Balkanlar’dan başlayıp doğuda Hazar Denizi sahasına kadar konuşulan Altay dillerinden biridir.'
SENTENCE_UKR = 'Украї́нська мо́ва (МФА: [ʊkrɐˈjɪɲsʲkɐ ˈmɔwɐ], історичні назви — ру́ська, руси́нська[9][10][11][* 2]) — національна мова українців.'
SENTENCE_URD = 'اُردُو (یا جدید معیاری اردو) ہندوستانی زبان کی معیاری قسم ہے۔'
SENTENCE_VIE = 'Tiếng Việt, còn gọi tiếng Việt Nam[5] hay Việt ngữ, là ngôn ngữ của người Việt (người Kinh) và là ngôn ngữ chính thức tại Việt Nam.'

def testing_word_tokenize(lang, word_tokenizer):
    lang_text = wordless_conversion.to_lang_text(main, lang)

    print(f'{lang_text} / {word_tokenizer}:')

    tokens_sentences = wordless_text_processing.wordless_word_tokenize(main, globals()[f'SENTENCE_{lang.upper()}'],
                                                                       lang = lang,
                                                                       word_tokenizer = word_tokenizer)
    tokens = itertools.chain.from_iterable(tokens_sentences)

    print(f"\t{' '.join(tokens)}")

main = testing_init.Testing_Main()

for lang, word_tokenizers in main.settings_global['word_tokenizers'].items():
    for word_tokenizer in word_tokenizers:
        if lang != 'other':
            testing_word_tokenize(lang = lang,
                                  word_tokenizer = word_tokenizer)
