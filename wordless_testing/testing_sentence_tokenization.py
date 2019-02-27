# -*- coding: utf-8 -*-

#
# Wordless: Testing - Sentence Tokenization
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import sys

sys.path.append('.')

from wordless_testing import testing_init
from wordless_text import wordless_text_processing, wordless_text_utils
from wordless_utils import wordless_conversion

main = testing_init.Testing_Main()

def testing_sentence_tokenize(lang, sentence_tokenizer):
    lang_text = wordless_conversion.to_lang_text(main, lang)

    print(f'{lang_text} / {sentence_tokenizer}:')

    wordless_text_utils.check_sentence_tokenizers(main, lang, sentence_tokenizer = sentence_tokenizer)

    for sentence in wordless_text_processing.wordless_sentence_tokenize(main, globals()[f'text_{lang}'],
                                                                        lang = lang,
                                                                        sentence_tokenizer = sentence_tokenizer):
        print(f'\t{sentence}')

text_zho_cn = '作为语言而言，为世界使用人数最多的语言，目前世界有五分之一人口做为母语。汉语有多种分支，当中标准官话最为流行，为中华人民共和国的国家通用语言（又称为普通话）、以及中华民国的国语。此外，汉语还是联合国官方语文[3]，并被上海合作组织等国际组织采用为官方语言。在中国大陆，汉语通称为“汉语”。在联合国、台湾、香港及澳门，通称为“中文”。在新加坡及马来西亚，通称为“华语”[注 1]。'
text_zho_tw = '作為語言而言，為世界使用人數最多的語言，目前世界有五分之一人口做為母語。漢語有多種分支，當中官話最為流行，為中華人民共和國的國家通用語言（又稱為普通話）、以及台灣的[國語]。此外，中文還是聯合國正式語文[3]，並被上海合作組織等國際組織採用為官方語言。在中國大陸，漢語通稱為「漢語」。在聯合國[4]、 臺灣[5]、 香港[6]及 澳門[7] ，通稱為「中文」。在新加坡及馬來西亞，通稱為「華語」[註 1]。'

text_ces = 'Čeština neboli český jazyk je západoslovanský jazyk, nejbližší slovenštině, poté lužické srbštině a polštině. Patří mezi slovanské jazyky, do rodiny jazyků indoevropských. Čeština se vyvinula ze západních nářečí praslovanštiny na konci 10. století. Je částečně ovlivněná latinou a němčinou. Česky psaná literatura se objevuje od 14. století. První písemné památky jsou však již z 12. století.'

text_dan = 'Dansk er et nordgermansk sprog af den østnordiske (kontinentale) gruppe, der tales af ca. seks millioner mennesker. Det er stærkt påvirket af plattysk. Dansk tales også i Sydslesvig (i Flensborg ca. 20 %) samt på Færøerne og Grønland [1]. Dansk er tæt forbundet med norsk. Fra et sprogvidenskabeligt synspunkt kan den fremherskende form af norsk, bokmål (og i endnu højere grad riksmål), betragtes som dansk, i hvert fald hvad skriftsproget angår.[kilde mangler] Både dansk, norsk og svensk er skandinaviske sprog og minder meget om hinanden.'

text_nld = 'Het Nederlands is een West-Germaanse taal en de moedertaal van de meeste inwoners van Nederland, België en Suriname. In de Europese Unie spreken ongeveer 23 miljoen mensen Nederlands als eerste taal, en een bijkomende vijf miljoen als tweede taal. Verder is het Nederlands ook een officiële taal van de Caraïbische (ei)landen Aruba, Curaçao en Sint-Maarten, terwijl de Franse Westhoek en de regio rondom de Duitse stad Kleef van oudsher Nederlandstalige gebieden zijn, en daar Nederlandse dialecten mogelijk nog gesproken worden door de oudste generaties. Ook in de voormalige kolonie Indonesië kunnen in sommige gebieden de oudste generaties nog Nederlands spreken. Het aantal sprekers van het Nederlands in Verenigde Staten, Canada en Australië wordt geschat op ruim een half miljoen. De Kaap-Hollandse dialecten van Zuid-Afrika en Namibië werden gestandaardiseerd tot Afrikaans, een dochtertaal van het Nederlands.'

text_eng = 'English is a West Germanic language that was first spoken in early medieval England and eventually became a global lingua franca.[4][5] Named after the Angles, one of the Germanic tribes that migrated to the area of Great Britain that would later take their name, England, both names ultimately deriving from the Anglia peninsula in the Baltic Sea. It is closely related to the Frisian languages, but its vocabulary has been significantly influenced by other Germanic languages, particularly Norse (a North Germanic language), as well as by Latin and French.[6]'

text_est = 'Eesti keel (varasem nimetus: maakeel) on läänemeresoome lõunarühma kuuluv keel. Selle lähemad sugulased on läänemeresoome keeled vadja ja liivi keel.'

text_fin = 'Suomen kieli (suomi) on uralilaisten kielten itämerensuomalaiseen ryhmään kuuluva kieli. Sitä puhuu äidinkielenään Suomessa 4,9 miljoonaa ja toisena kielenä 0,5 miljoonaa henkilöä. Suurimmat suomea puhuvat vähemmistöt ovat Ruotsissa, Norjassa ja Venäjällä.'

text_fra = "Le français est une langue indo-européenne de la famille des langues romanes. Le français s'est formé en France (variété de la « langue d’oïl », qui est la langue de la partie septentrionale du pays) et est en 2018 parlé sur tous les continents par environ 300 millions de personnes1,4 dont 235 millions l'utilisent quotidiennement, 90 millions2 en étant des locuteurs natifs. En 2018, 80 millions d'élèves et étudiants s'instruisent en français dans le monde5. Elle est une des six langues officielles et une des deux langues de travail (avec l’anglais) de l’Organisation des Nations unies, et langue officielle ou de travail de plusieurs organisations internationales ou régionales, dont l’Union européenne. Après avoir été à l’époque de l’Ancien Régime la langue des cours royales et princières, des tsars de Russie aux rois d’Espagne et d'Angleterre en passant par les princes de l’Allemagne, elle demeure une langue importante de la diplomatie internationale aux côtés de l’anglais."

text_deu = 'Ihr Sprachraum umfasst Deutschland, Österreich, die Deutschschweiz, Liechtenstein, Luxemburg, Ostbelgien, Südtirol, das Elsass und Lothringen sowie Nordschleswig. Außerdem ist sie eine Minderheitensprache in einigen europäischen und außereuropäischen Ländern, z. B. in Rumänien und Südafrika, sowie Nationalsprache im afrikanischen Namibia.'

text_ell = 'Η ελληνική γλώσσα είναι μια από τις ινδοευρωπαϊκές γλώσσες[9] και αποτελεί το μοναδικό μέλος ενός ανεξάρτητου κλάδου, αυτής της οικογένειας γλωσσών, ενώ είναι η επίσημη γλώσσα της Ελλάδος και της Κύπρου. Ανήκει επίσης στον βαλκανικό γλωσσικό δεσμό. Στην ελληνική γλώσσα, έχουμε γραπτά κείμενα ήδη από τον 15ο αιώνα π.Χ.'

text_ita = "È classificato al 21º posto tra le lingue per numero di parlanti nel mondo e, in Italia, è utilizzato da circa 58 milioni di residenti.[4] Viene considerato la lingua materna del 95% dei cittadini italiani residenti in Italia,[5] che spesso lo acquisiscono e lo usano insieme alle varianti regionali dell'italiano, alle lingue regionali e ai dialetti. In Italia viene ampiamente usato per tutti i tipi di comunicazione della vita quotidiana ed è la lingua della quasi totalità dei mezzi di comunicazione nazionali, dell'editoria e dell'amministrazione pubblica dello Stato italiano."

text_jpn = '使用人口について正確な統計はないが、日本国内の人口、および日本国外に住む日本人や日系人、日本がかつて統治した地域の一部住民など、約1億3千万人以上と考えられている[7]。統計によって前後する場合もあるが、この数は世界の母語話者数で上位10位以内に入る人数である。'

text_nob = 'Norsk er et nordisk språk som snakkes som morsmål av rundt 5 millioner mennesker,[1][trenger bedre kilde] først og fremst i Norge, hvor det er offisielt språk. Det snakkes også av over 50 000 norsk-amerikanere i USA, spesielt i Midtvesten. Norsk, svensk og dansk utgjør sammen de fastlandsnordiske språkene, et kontinuum av mer eller mindre innbyrdes forståelige dialekter i Skandinavia.[2] Norsk kan føres tilbake til de vestnordiske dialektene av norrønt, som også islandsk og færøysk har utgått fra, men avstanden til disse øynordiske språkene er i dag langt større enn avstanden til de østnordiske språkene dansk og svensk. Det er vanskelig å avgrense norsk mot svensk og dansk etter rent språklige kriterier; i praksis kan moderne norsk sies å være de skandinaviske dialekter og standardspråk som har geografisk tilknytning til Norge.'
text_nno = 'Norsk er eit germansk språk som høyrer til den nordiske, eller nordgermanske, greina. Norsk blir for det meste snakka i Noreg, men òg i norske utvandrarsamfunn, som blant norsk-amerikanarar i USA. I dei gamle norske provinsane i Sverige — Jemtland, Herjedalen og Båhuslen — har dialektane mange likskapar med norsk, særleg nord i området.[1]'

text_pol = 'Język polski, polszczyzna, skrót: pol. – język naturalny należący do grupy języków zachodniosłowiańskich (do której należą również czeski, słowacki, kaszubski, dolnołużycki, górnołużycki i wymarły połabski), stanowiącej część rodziny języków indoeuropejskich. Polszczyzna jest jednym z oficjalnych języków Unii Europejskiej.'

text_por = 'A língua portuguesa, também designada português, é uma língua românica flexiva ocidental originada no galego-português falado no Reino da Galiza e no norte de Portugal. Com a criação do Reino de Portugal em 1139 e a expansão para o sul como parte da Reconquista deu-se a difusão da língua pelas terras conquistadas e mais tarde, com as descobertas portuguesas, para o Brasil, África e outras partes do mundo.[3] O português foi usado, naquela época, não somente nas cidades conquistadas pelos portugueses, mas também por muitos governantes locais nos seus contatos com outros estrangeiros poderosos. Especialmente nessa altura a língua portuguesa também influenciou várias línguas.[4]'

text_slv = 'Slovenščina [slovénščina] / [sloˈʋenʃtʃina] je združeni naziv za uradni knjižni jezik Slovencev in skupno ime za narečja in govore, ki jih govorijo ali so jih nekoč govorili Slovenci. Govori ga 2.500.000 govorcev po svetu, od katerih jih večina živi v Sloveniji. Glede na število govorcev ima razmeroma veliko narečij. Slovenščina je zahodni južnoslovanski jezik in eden redkih indoevropskih jezikov, ki je ohranil dualizem - dvojino. Za zapisovanje slovenskega jezika se danes uporablja gajica, pisava imenovana po Ljudevitu Gaju, ki jo je priredil po češkem črkopisu. Slovenska gajica se imenuje slovenica. Pišemo jo od marčne revolucije 1848. Do takrat smo uporabljali bohoričico.'

text_spa = 'El idioma español o castellano es una lengua romance procedente del latín hablado. Pertenece al grupo ibérico y es originaria de Castilla, reino medieval de la península ibérica. Se conoce también por el americanismo coloquial castilla (por ejemplo: «hablar castilla», «entender castilla»),nota 1​32​33​ común en áreas rurales e indígenas entre México, Perú y la Patagonia.34​'

text_swe = 'Svenska (svenska (info)) är ett östnordiskt språk som talas av drygt elva miljoner personer[källa behövs] främst i Sverige där språket har en dominant ställning som huvudspråk, men även som det ena nationalspråket i Finland och som enda officiella språk på Åland. I övriga Finland talas det som modersmål framförallt i de finlandssvenska kustområdena i Österbotten, Åboland och Nyland. En liten minoritet svenskspråkiga finns även i Estland. Svenska är nära besläktat och i hög grad ömsesidigt begripligt med danska och norska. De andra nordiska språken, isländska och färöiska, är mindre ömsesidigt begripliga med svenska. Liksom de övriga nordiska språken härstammar svenskan från en gren av fornnordiska, vilket var det språk som talades av de germanska folken i Skandinavien.'

text_tha = 'ภาษาไทย หรือ ภาษาไทยกลาง เป็นภาษาราชการและภาษาประจำชาติของประเทศไทย ภาษาไทยเป็นภ าษาในกลุ่มภาษาไท ซึ่งเป็นกลุ่มย่อยของตระกูลภาษาไท-กะได สันนิษฐานว่า ภาษาในตระกูลนี้มีถิ่นกำเนิดจากทางตอนใต้ของประเทศจีน และนักภาษาศาสตร์บางส่วนเสนอว่า ภาษาไทยน่าจะมีความเชื่อมโยงกับตระกูลภาษาออสโตร-เอเชียติก ตระกูลภาษาออสโตรนีเซียน และตระกูลภาษาจีน-ทิเบต'

text_tur = 'Türkçe ya da Türk dili, batıda Balkanlar’dan başlayıp doğuda Hazar Denizi sahasına kadar konuşulan Altay dillerinden biridir. Yaşı, en eski hesaplara göre 8500 olan Türkçe, bugün yaşayan Dünya dilleri arasında en eski yazılı belgelere sahip olan dildir. Bu belgeler, çivi yazılı Sümerce tabletlerdeki alıntı kelimelerdir.[12][13] Türk yazı dilleri içinde Oğuz sahası yazı dillerinden Osmanlı Türkçesinin devamını oluşturur. Başta Türkiye olmak üzere eski Osmanlı İmparatorluğu coğrafyasında konuşulan Türkçe, dünyada en fazla konuşulan 5. dildir. Türkçe sondan eklemeli bir dildir.[14] Bundan ötürü kullanılan herhangi bir eylem üzerinden istenildiği kadar sözcük türetilebilir.[15] Türkiye Türkçesi bu yönünden dolayı diğer Türk dilleriyle ortak ya da ayrık bulunan onlarca eke sahiptir.[16] Türkçe çok geniş kullanımıyla birlikte zengin bir dil olmasının yanı sıra, genel itibarıyla “özne-nesne-yüklem” biçimindeki cümle kuruluşuna sahiptir.'

text_vie = 'Tiếng Việt, còn gọi tiếng Việt Nam[5] hay Việt ngữ, là ngôn ngữ của người Việt (người Kinh) và là ngôn ngữ chính thức tại Việt Nam. Đây là tiếng mẹ đẻ của khoảng 85% dân cư Việt Nam, cùng với hơn bốn triệu người Việt hải ngoại. Tiếng Việt còn là ngôn ngữ thứ hai của các dân tộc thiểu số tại Việt Nam. Mặc dù tiếng Việt có một số từ vựng vay mượn từ tiếng Hán và trước đây dùng chữ Nôm — một hệ chữ dựa trên chữ Hán — để viết nhưng tiếng Việt được coi là một trong số các ngôn ngữ thuộc ngữ hệ Nam Á có số người nói nhiều nhất (nhiều hơn một số lần so với các ngôn ngữ khác cùng hệ cộng lại). Ngày nay, tiếng Việt dùng bảng chữ cái Latinh, gọi là chữ Quốc ngữ, cùng các dấu thanh để viết.'

testing_sentence_tokenize(lang = 'zho_cn',
                          sentence_tokenizer = 'Wordless - Chinese Sentence Tokenizer')
testing_sentence_tokenize(lang = 'zho_tw',
                          sentence_tokenizer = 'Wordless - Chinese Sentence Tokenizer')

testing_sentence_tokenize(lang = 'ces',
                          sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer')

testing_sentence_tokenize(lang = 'dan',
                          sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer')

testing_sentence_tokenize(lang = 'nld',
                          sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer')
testing_sentence_tokenize(lang = 'nld',
                          sentence_tokenizer = 'spaCy - Dutch Sentence Tokenizer')

testing_sentence_tokenize(lang = 'eng',
                          sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer')
testing_sentence_tokenize(lang = 'eng',
                          sentence_tokenizer = 'spaCy - English Sentence Tokenizer')

testing_sentence_tokenize(lang = 'est',
                          sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer')

testing_sentence_tokenize(lang = 'fin',
                          sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer')

testing_sentence_tokenize(lang = 'fra',
                          sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer')
testing_sentence_tokenize(lang = 'fra',
                          sentence_tokenizer = 'spaCy - French Sentence Tokenizer')

testing_sentence_tokenize(lang = 'deu',
                          sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer')
testing_sentence_tokenize(lang = 'deu',
                          sentence_tokenizer = 'spaCy - German Sentence Tokenizer')

testing_sentence_tokenize(lang = 'ell',
                          sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer')
testing_sentence_tokenize(lang = 'ell',
                          sentence_tokenizer = 'spaCy - Greek (Modern) Sentence Tokenizer')

testing_sentence_tokenize(lang = 'ita',
                          sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer')
testing_sentence_tokenize(lang = 'ita',
                          sentence_tokenizer = 'spaCy - Italian Sentence Tokenizer')

testing_sentence_tokenize(lang = 'jpn',
                          sentence_tokenizer = 'Wordless - Japanese Sentence Tokenizer')

testing_sentence_tokenize(lang = 'nob',
                          sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer')
testing_sentence_tokenize(lang = 'nno',
                          sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer')

testing_sentence_tokenize(lang = 'pol',
                          sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer')

testing_sentence_tokenize(lang = 'por',
                          sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer')
testing_sentence_tokenize(lang = 'por',
                          sentence_tokenizer = 'spaCy - Portuguese Sentence Tokenizer')

testing_sentence_tokenize(lang = 'slv',
                          sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer')

testing_sentence_tokenize(lang = 'spa',
                          sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer')
testing_sentence_tokenize(lang = 'spa',
                          sentence_tokenizer = 'spaCy - Spanish Sentence Tokenizer')

testing_sentence_tokenize(lang = 'swe',
                          sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer')

testing_sentence_tokenize(lang = 'tha',
                          sentence_tokenizer = 'PyThaiNLP - Thai Sentence Tokenizer')

testing_sentence_tokenize(lang = 'tur',
                          sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer')

testing_sentence_tokenize(lang = 'vie',
                          sentence_tokenizer = 'Underthesea - Vietnamese Sentence Tokenizer')
