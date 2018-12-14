# -*- coding: utf-8 -*-

#
# Wordless: Testing for Text Processing
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import sys

from PyQt5.QtCore import *

sys.path.append('E:/Wordless')

import wordless_text_processing
from wordless_settings import init_settings_global

main = QObject()

init_settings_global.init_settings_global(main)

# Chinese (Simplified)
text_zho_cn = '作为语言而言，为世界使用人数最多的语言，目前世界有五分之一人口做为母语。汉语有多种分支，当中标准官话最为流行，为中华人民共和国的国家通用语言（又称为普通话）、以及中华民国的国语。此外，汉语还是联合国官方语文[3]，并被上海合作组织等国际组织采用为官方语言。在中国大陆，汉语通称为“汉语”。在联合国、台湾、香港及澳门，通称为“中文”。在新加坡及马来西亚，通称为“华语”[注 1]。'

print('Sentence Tokenization / Chinese (Simplified) / Wordless - Chinese Sentence Tokenizer:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_zho_cn, 'zho_CN',
                                                                    sentence_tokenizer = 'Wordless - Chinese Sentence Tokenizer'):
    print(f'\t{sentence}')

print('Sentence Tokenization / Chinese (Simplified) / HanLP - Sentence Segmenter:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_zho_cn, 'zho_CN',
                                                                    sentence_tokenizer = 'HanLP - Sentence Segmenter'):
    print(f'\t{sentence}')

# Chinese (Traditional)
text_zho_tw = '作為語言而言，為世界使用人數最多的語言，目前世界有五分之一人口做為母語。漢語有多種分支，當中標準官話最為流行，為中華人民共和國的國家通用語言（又稱為普通話）、以及中華民國的國語。此外，漢語還是聯合國官方語文[3]，並被上海合作組織等國際組織採用為官方語言。在中國大陸，漢語通稱為「漢語」。在聯合國、臺灣、香港及澳門，通稱為「中文」。在新加坡及馬來西亞，通稱為「華語」[註 1]。'

print('Sentence Tokenization / Chinese (Traditional) / Wordless - Chinese Sentence Tokenizer:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_zho_tw, 'zho_TW',
                                                                    sentence_tokenizer = 'Wordless - Chinese Sentence Tokenizer'):
    print(f'\t{sentence}')

print('Sentence Tokenization / Chinese (Traditional) / HanLP - Sentence Segmenter:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_zho_tw, 'zho_TW',
                                                                    sentence_tokenizer = 'HanLP - Sentence Segmenter'):
    print(f'\t{sentence}')

# Czech
text_ces = 'Český jazyk neboli čeština je západoslovanský jazyk, nejbližší slovenštině, poté lužické srbštině a polštině. Patří mezi slovanské jazyky, do rodiny jazyků indoevropských. Čeština se vyvinula ze západních nářečí praslovanštiny na konci 10. století. Je částečně ovlivněná latinou a němčinou. Česky psaná literatura se objevuje od 14. století. První písemné památky jsou však již z 12. století.'

print('Sentence Tokenization / Czech / NLTK - Punkt Sentence Tokenizer:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_ces, 'ces',
                                                                    sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer'):
    print(f'\t{sentence}')

# Danish
text_dan = 'Dansk er et nordgermansk sprog af den østnordiske (kontinentale) gruppe, der tales af ca. seks millioner mennesker. Det er stærkt påvirket af plattysk. Dansk tales også i Sydslesvig (i Flensborg ca. 20 %) samt på Færøerne og Grønland [1]. Dansk er tæt forbundet med norsk. Fra et sprogvidenskabeligt synspunkt kan den fremherskende form af norsk, bokmål (og i endnu højere grad riksmål), betragtes som dansk, i hvert fald hvad skriftsproget angår.[kilde mangler] Både dansk, norsk og svensk er skandinaviske sprog og minder meget om hinanden.'

print('Sentence Tokenization / Danish / NLTK - Punkt Sentence Tokenizer:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_dan, 'dan',
                                                                    sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer'):
    print(f'\t{sentence}')

# Dutch
text_nld = 'Het Nederlands is een West-Germaanse taal en de moedertaal van de meeste inwoners van Nederland, België en Suriname. In de Europese Unie spreken ongeveer 23 miljoen mensen Nederlands als eerste taal, en een bijkomende vijf miljoen als tweede taal. Verder is het Nederlands ook een officiële taal van de Caraïbische (ei)landen Aruba, Curaçao en Sint-Maarten, terwijl de Franse Westhoek en de regio rondom de Duitse stad Kleef van oudsher Nederlandstalige gebieden zijn, en daar Nederlandse dialecten mogelijk nog gesproken worden door de oudste generaties. Ook in de voormalige kolonie Indonesië kunnen in sommige gebieden de oudste generaties nog Nederlands spreken. Het aantal sprekers van het Nederlands in Verenigde Staten, Canada en Australië wordt geschat op ruim een half miljoen. De Kaap-Hollandse dialecten van Zuid-Afrika en Namibië werden gestandaardiseerd tot Afrikaans, een dochtertaal van het Nederlands.'

print('Sentence Tokenization / Dutch / NLTK - Punkt Sentence Tokenizer:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_nld, 'nld',
                                                                    sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer'):
    print(f'\t{sentence}')

# English
text_eng = 'English is a West Germanic language that was first spoken in early medieval England and eventually became a global lingua franca.[4][5] Named after the Angles, one of the Germanic tribes that migrated to the area of Great Britain that would later take their name, England, both names ultimately deriving from the Anglia peninsula in the Baltic Sea. It is closely related to the Frisian languages, but its vocabulary has been significantly influenced by other Germanic languages, particularly Norse (a North Germanic language), as well as by Latin and French.[6]'

print('Sentence Tokenization / English / NLTK - Punkt Sentence Tokenizer:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_eng, 'eng',
                                                                    sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer'):
    print(f'\t{sentence}')

# Estonian
text_est = 'Eesti keel (varasem nimetus: maakeel) on läänemeresoome lõunarühma kuuluv keel. Selle lähemad sugulased on läänemeresoome keeled vadja ja liivi keel.'

print('Sentence Tokenization / Estonian / NLTK - Punkt Sentence Tokenizer:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_est, 'est',
                                                                    sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer'):
    print(f'\t{sentence}')

# Finnish
text_fin = 'Suomen kieli (suomi) on uralilaisten kielten itämerensuomalaiseen ryhmään kuuluva kieli. Sitä puhuu äidinkielenään Suomessa 4,9 miljoonaa ja toisena kielenä 0,5 miljoonaa henkilöä. Suurimmat suomea puhuvat vähemmistöt ovat Ruotsissa, Norjassa ja Venäjällä.'

print('Sentence Tokenization / Finnish / NLTK - Punkt Sentence Tokenizer:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_fin, 'fin',
                                                                    sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer'):
    print(f'\t{sentence}')

# French
text_fra = "Le français est une langue indo-européenne de la famille des langues romanes. Le français s'est formé en France (variété de la « langue d’oïl », qui est la langue de la partie septentrionale du pays) et est en 2018 parlé sur tous les continents par environ 300 millions de personnes1,4 dont 235 millions l'utilisent quotidiennement, 90 millions2 en étant des locuteurs natifs. En 2018, 80 millions d'élèves et étudiants s'instruisent en français dans le monde5. Elle est une des six langues officielles et une des deux langues de travail (avec l’anglais) de l’Organisation des Nations unies, et langue officielle ou de travail de plusieurs organisations internationales ou régionales, dont l’Union européenne. Après avoir été à l’époque de l’Ancien Régime la langue des cours royales et princières, des tsars de Russie aux rois d’Espagne et d'Angleterre en passant par les princes de l’Allemagne, elle demeure une langue importante de la diplomatie internationale aux côtés de l’anglais."

print('Sentence Tokenization / French / NLTK - Punkt Sentence Tokenizer:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_fra, 'fra',
                                                                    sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer'):
    print(f'\t{sentence}')


# German
text_deu = 'Ihr Sprachraum umfasst Deutschland, Österreich, die Deutschschweiz, Liechtenstein, Luxemburg, Ostbelgien, Südtirol, das Elsass und Lothringen sowie Nordschleswig. Außerdem ist sie eine Minderheitensprache in einigen europäischen und außereuropäischen Ländern, z. B. in Rumänien und Südafrika, sowie Nationalsprache im afrikanischen Namibia.'

print('Sentence Tokenization / German / NLTK - Punkt Sentence Tokenizer:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_deu, 'deu',
                                                                    sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer'):
    print(f'\t{sentence}')

# Greek
text_ell = 'Η ελληνική γλώσσα είναι μια από τις ινδοευρωπαϊκές γλώσσες[9] και αποτελεί το μοναδικό μέλος ενός ανεξάρτητου κλάδου, αυτής της οικογένειας γλωσσών, ενώ είναι η επίσημη γλώσσα της Ελλάδος και της Κύπρου. Ανήκει επίσης στον βαλκανικό γλωσσικό δεσμό. Στην ελληνική γλώσσα, έχουμε γραπτά κείμενα ήδη από τον 15ο αιώνα π.Χ.'

print('Sentence Tokenization / Greek / NLTK - Punkt Sentence Tokenizer:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_ell, 'ell',
                                                                    sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer'):
    print(f'\t{sentence}')

# Italian
text_ita = "È classificato al 21º posto tra le lingue per numero di parlanti nel mondo e, in Italia, è utilizzato da circa 58 milioni di residenti.[4] Viene considerato la lingua materna del 95% dei cittadini italiani residenti in Italia,[5] che spesso lo acquisiscono e lo usano insieme alle varianti regionali dell'italiano, alle lingue regionali e ai dialetti. In Italia viene ampiamente usato per tutti i tipi di comunicazione della vita quotidiana ed è la lingua della quasi totalità dei mezzi di comunicazione nazionali, dell'editoria e dell'amministrazione pubblica dello Stato italiano."

print('Sentence Tokenization / Italian / NLTK - Punkt Sentence Tokenizer:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_ita, 'ita',
                                                                    sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer'):
    print(f'\t{sentence}')

# Norwegian
text_nor = 'Norsk er et nordisk språk som snakkes som morsmål av rundt 5 millioner mennesker,[1][trenger bedre kilde] først og fremst i Norge, hvor det er offisielt språk. Det snakkes også av over 50 000 norsk-amerikanere i USA, spesielt i Midtvesten. Norsk, svensk og dansk utgjør sammen de fastlandsnordiske språkene, et kontinuum av mer eller mindre innbyrdes forståelige dialekter i Skandinavia.[2] Norsk kan føres tilbake til de vestnordiske dialektene av norrønt, som også islandsk og færøysk har utgått fra, men avstanden til disse øynordiske språkene er i dag langt større enn avstanden til de østnordiske språkene dansk og svensk. Det er vanskelig å avgrense norsk mot svensk og dansk etter rent språklige kriterier; i praksis kan moderne norsk sies å være de skandinaviske dialekter og standardspråk som har geografisk tilknytning til Norge.'

print('Sentence Tokenization / Norwegian / NLTK - Punkt Sentence Tokenizer:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_nor, 'nor',
                                                                    sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer'):
    print(f'\t{sentence}')

# Polish
text_pol = 'Język polski, polszczyzna, skrót: pol. – język naturalny należący do grupy języków zachodniosłowiańskich (do której należą również czeski, słowacki, kaszubski, dolnołużycki, górnołużycki i wymarły połabski), stanowiącej część rodziny języków indoeuropejskich. Polszczyzna jest jednym z oficjalnych języków Unii Europejskiej.'

print('Sentence Tokenization / Polish / NLTK - Punkt Sentence Tokenizer:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_pol, 'pol',
                                                                    sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer'):
    print(f'\t{sentence}')

# Portuguese
text_por = 'A língua portuguesa, também designada português, é uma língua românica flexiva ocidental originada no galego-português falado no Reino da Galiza e no norte de Portugal. Com a criação do Reino de Portugal em 1139 e a expansão para o sul como parte da Reconquista deu-se a difusão da língua pelas terras conquistadas e mais tarde, com as descobertas portuguesas, para o Brasil, África e outras partes do mundo.[3] O português foi usado, naquela época, não somente nas cidades conquistadas pelos portugueses, mas também por muitos governantes locais nos seus contatos com outros estrangeiros poderosos. Especialmente nessa altura a língua portuguesa também influenciou várias línguas.[4]'

print('Sentence Tokenization / Portuguese / NLTK - Punkt Sentence Tokenizer:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_por, 'por',
                                                                    sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer'):
    print(f'\t{sentence}')

# Slovenian
text_slv = 'Slovenščina [slovénščina] / [sloˈʋenʃtʃina] je združeni naziv za uradni knjižni jezik Slovencev in skupno ime za narečja in govore, ki jih govorijo ali so jih nekoč govorili Slovenci. Govori ga 2.500.000 govorcev po svetu, od katerih jih večina živi v Sloveniji. Glede na število govorcev ima razmeroma veliko narečij. Slovenščina je zahodni južnoslovanski jezik in eden redkih indoevropskih jezikov, ki je ohranil dualizem - dvojino. Za zapisovanje slovenskega jezika se danes uporablja gajica, pisava imenovana po Ljudevitu Gaju, ki jo je priredil po češkem črkopisu. Slovenska gajica se imenuje slovenica. Pišemo jo od marčne revolucije 1848. Do takrat smo uporabljali bohoričico.'

print('Sentence Tokenization / Slovenian / NLTK - Punkt Sentence Tokenizer:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_slv, 'slv',
                                                                    sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer'):
    print(f'\t{sentence}')

# Spanish
text_spa = 'El idioma español o castellano es una lengua romance procedente del latín hablado. Pertenece al grupo ibérico y es originaria de Castilla, reino medieval de la península ibérica. Se conoce también por el americanismo coloquial castilla (por ejemplo: «hablar castilla», «entender castilla»),nota 1​32​33​ común en áreas rurales e indígenas entre México, Perú y la Patagonia.34'

print('Sentence Tokenization / Spanish / NLTK - Punkt Sentence Tokenizer:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_spa, 'spa',
                                                                    sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer'):
    print(f'\t{sentence}')

# Swedish
text_swe = 'Svenska (svenska (info)) är ett östnordiskt språk som talas av drygt tio miljoner personer främst i Sverige där språket har en dominant ställning som huvudspråk, men även som det ena nationalspråket i Finland och som enda officiella språk på Åland. I övriga Finland talas det som modersmål framförallt i de finlandssvenska kustområdena i Österbotten, Åboland och Nyland. En liten minoritet svenskspråkiga finns även i Estland. Svenska är nära besläktat och i hög grad ömsesidigt begripligt med danska och norska. De andra nordiska språken, isländska och färöiska, är mindre ömsesidigt begripliga med svenska. Liksom de övriga nordiska språken härstammar svenskan från en gren av fornnordiska, vilket var det språk som talades av de germanska folken i Skandinavien.'

print('Sentence Tokenization / Swedish / NLTK - Punkt Sentence Tokenizer:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_swe, 'swe',
                                                                    sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer'):
    print(f'\t{sentence}')

# Turkish
text_tur = 'Türkçe ya da Türk dili, batıda Balkanlar’dan başlayıp doğuda Hazar Denizi sahasına kadar konuşulan Altay dillerinden biridir. Yaşı, en eski hesaplara göre 8500 olan Türkçe, bugün yaşayan Dünya dilleri arasında en eski yazılı belgelere sahip olan dildir. Bu belgeler, çivi yazılı Sümerce tabletlerdeki alıntı kelimelerdir.[12][13] Türk yazı dilleri içinde Oğuz sahası yazı dillerinden Osmanlı Türkçesinin devamını oluşturur. Başta Türkiye olmak üzere eski Osmanlı İmparatorluğu coğrafyasında konuşulan Türkçe, dünyada en fazla konuşulan 5. dildir. Türkçe sondan eklemeli bir dildir.[14] Bundan ötürü kullanılan herhangi bir eylem üzerinden istenildiği kadar sözcük türetilebilir.[15] Türkiye Türkçesi bu yönünden dolayı diğer Türk dilleriyle ortak ya da ayrık bulunan onlarca eke sahiptir.[16] Türkçe çok geniş kullanımıyla birlikte zengin bir dil olmasının yanı sıra, genel itibarıyla “özne-nesne-yüklem” biçimindeki cümle kuruluşuna sahiptir.'

print('Sentence Tokenization / Turkish / NLTK - Punkt Sentence Tokenizer:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_tur, 'tur',
                                                                    sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer'):
    print(f'\t{sentence}')

# Other Languages (Esperanto)
text_epo = 'Esperanto, origine la Lingvo Internacia, estas la plej disvastigita internacia planlingvo.[4] En 1887 Esperanton parolis nur manpleno da homoj; Esperanto havis unu el la plej malgrandaj lingvo-komunumoj de la mondo. Ĝi funkciis dekomence kiel lingvo de alternativa komunikado kaj de arta kreivo[5]. En 2012, la lingvo fariĝis la 64-a tradukebla per Google Translate[6]; laŭ 2016, Esperanto aperis en listoj de lingvoj plej lernataj[7] kaj konataj en Hungarujo[8]. La nomo de la lingvo venas de la kaŝnomo “D-ro Esperanto„ sub kiu la juda kuracisto Ludoviko Lazaro Zamenhofo en la jaro 1887 publikigis la bazon de la lingvo. La unua versio, la rusa, ricevis la cenzuran permeson disvastiĝi en la 26-a de julio; ĉi tiun daton oni konsideras la naskiĝtago de Esperanto[9][10]. Li celis kaj sukcesis krei facile lerneblan neŭtralan lingvon, taŭgan por uzo en la internacia komunikado; la celo tamen ne estas anstataŭigi aliajn, naciajn lingvojn.'

print('Sentence Tokenization / Other Languages (Esperanto) / NLTK - Punkt Sentence Tokenizer:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_epo, 'epo',
                                                                    sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer'):
    print(f'\t{sentence}')
