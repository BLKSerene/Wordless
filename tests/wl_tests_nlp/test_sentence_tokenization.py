# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Sentence Tokenization
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
from wordless.wl_nlp import wl_sentence_tokenization, wl_word_tokenization

main = wl_test_init.Wl_Test_Main()

test_sentence_tokenizers = []

for lang, sentence_tokenizers in main.settings_global['sentence_tokenizers'].items():
    for sentence_tokenizer in sentence_tokenizers:
        if lang not in ['other']:
            if (
                lang.startswith('eng')
                # Skip tests of spaCy's sentencizer
                or (
                    not lang.startswith('eng')
                    and sentence_tokenizer != 'spacy_sentencizer'
                )
            ):
                test_sentence_tokenizers.append((lang, sentence_tokenizer))

test_langs = [lang for lang, _ in test_sentence_tokenizers]

@pytest.mark.parametrize('lang, sentence_tokenizer', test_sentence_tokenizers)
def test_sentence_tokenize(lang, sentence_tokenizer):
    sentences = wl_sentence_tokenization.wl_sentence_tokenize(
        main,
        text = getattr(wl_test_lang_examples, f'TEXT_{lang.upper()}'),
        lang = lang,
        sentence_tokenizer = sentence_tokenizer
    )

    print(f'{lang} / {sentence_tokenizer}:')
    print(f'{sentences}\n')

    # The count of sentences should be more than 1
    assert len(sentences) > 1

    if lang == 'zho_cn':
        assert sentences == ['汉语又称华语[3]、唐话[4]，概指由上古汉语（先秦雅言）发展而来、书面使用汉字的分析语，为汉藏语系最大的一支语族。', '如把整个汉语族视为单一语言，则汉语为世界使用人数最多的语言，目前全世界有五分之一人口将汉语做为母语或第二语言。']
    elif lang == 'zho_tw':
        assert sentences == ['漢語又稱華語[3]、唐話[4]，概指由上古漢語（先秦雅言）發展而來、書面使用漢字的分析語，為漢藏語系最大的一支語族。', '如把整個漢語族視為單一語言，則漢語為世界使用人數最多的語言，目前全世界有五分之一人口將漢語做為母語或第二語言。']
    elif lang == 'ces':
        assert sentences == ['Čeština neboli český jazyk je západoslovanský jazyk, nejbližší slovenštině, poté lužické srbštině a polštině.', 'Patří mezi slovanské jazyky, do rodiny jazyků indoevropských.', 'Čeština se vyvinula ze západních nářečí praslovanštiny na konci 10. století.', 'Je částečně ovlivněná latinou a němčinou.', 'Česky psaná literatura se objevuje od 14. století.', 'První písemné památky jsou však již z 12. století.']
    elif lang == 'dan':
        if sentence_tokenizer == 'nltk_punkt':
            assert sentences == ['Dansk er et østnordisk sprog indenfor den germanske gren af den indoeuropæiske sprogfamilie.', 'Det danske sprog tales af ca. seks millioner mennesker, hovedsageligt i Danmark, men også i Sydslesvig (i Flensborg ca. 20 %), på Færøerne og Grønland.', '[1] Dansk er tæt forbundet med norsk og svensk, og sproghistorisk har dansk været stærkt påvirket af plattysk.']
        elif sentence_tokenizer == 'spacy_sentence_recognizer':
            assert sentences == ['Dansk er et østnordisk sprog indenfor den germanske gren af den indoeuropæiske sprogfamilie.', 'Det danske sprog tales af ca. seks millioner mennesker, hovedsageligt i Danmark, men også i Sydslesvig (i Flensborg ca. 20 %), på Færøerne og Grønland.[1] Dansk er tæt forbundet med norsk og svensk, og sproghistorisk har dansk været stærkt påvirket af plattysk.']
        else:
            raise Exception(f'Error: Tests for sentence tokenizer "{sentence_tokenizer}" is skipped!')
    elif lang == 'nld':
        assert sentences == ['Het Nederlands is een West-Germaanse taal en de officiële taal van Nederland, Suriname en een van de drie officiële talen van België.', 'Binnen het Koninkrijk der Nederlanden is het Nederlands ook een officiële taal van Aruba, Curaçao en Sint-Maarten.', 'Het Nederlands is de op twee na meest gesproken Germaanse taal.']
    elif lang.startswith('eng_'):
        if sentence_tokenizer == 'nltk_punkt':
            assert sentences == ['English is a West Germanic language of the Indo-European language family, originally spoken by the inhabitants of early medieval England.', '[3][4][5] It is named after the Angles, one of the ancient Germanic peoples that migrated from Anglia, a peninsula on the Baltic Sea (not to be confused with East Anglia in England), to the area of Great Britain later named after them: England.', 'The closest living relatives of English include Scots, followed by the Low Saxon and Frisian languages.', 'While English is genealogically West Germanic, its vocabulary is also distinctively influenced by dialects of French (about 29% of modern English words) and Latin (also about 29%), as well as by Old Norse (a North Germanic language).', '[6][7][8] Speakers of English are called Anglophones.']
        elif sentence_tokenizer == 'spacy_sentence_recognizer':
            assert sentences == ['English is a West Germanic language of the Indo-European language family, originally spoken by the inhabitants of early medieval England.[3][4][5] It is named after the Angles, one of the ancient Germanic peoples that migrated from Anglia, a peninsula on the Baltic Sea (not to be confused with East Anglia in England), to the area of Great Britain later named after them: England.', 'The closest living relatives of English include Scots, followed by the Low Saxon and Frisian languages.', 'While English is genealogically West Germanic, its vocabulary is also distinctively influenced by dialects of French (about 29% of modern English words) and Latin (also about 29%), as well as by Old Norse (a North Germanic language).[6][7][8] Speakers of English are called Anglophones.']
        else:
            raise Exception(f'Error: Tests for sentence tokenizer "{sentence_tokenizer}" is skipped!')
    elif lang == 'est':
        assert sentences == ['Eesti keel (varasem nimetus maakeel) on läänemeresoome lõunarühma kuuluv keel.', 'Eesti keel on Eesti riigikeel ja 2004. aastast ka üks Euroopa Liidu ametlikke keeli.']
    elif lang == 'fin':
        assert sentences == ['Suomen kieli (suomi) on uralilaisten kielten itämerensuomalaiseen ryhmään kuuluva kieli, jota puhuvat pääosin suomalaiset.', 'Sitä puhuu äidinkielenään Suomessa 4,8 miljoonaa ja toisena kielenä 0,5 miljoonaa ihmistä.', 'Suurimmat suomea puhuvat vähemmistöt ovat Ruotsissa, Norjassa ja Venäjällä.']
    elif lang == 'fra':
        assert sentences == ['Le français est une langue indo-européenne de la famille des langues romanes dont les locuteurs sont appelés francophones, également surnommé la langue de Molière.', "Le français est parlé, en 2022[Lien à corriger], sur tous les continents par environ 321 millions de personnes5,2 : 235 millions l'emploient quotidiennement, et 90 millions3 en sont des locuteurs natifs.", "En 2018, 80 millions d'élèves et étudiants s'instruisent en français dans le monde6.", "Selon l'Organisation internationale de la francophonie (OIF), il pourrait y avoir 700 millions de francophones sur Terre en 20507."]
    elif lang.startswith('deu_'):
        if sentence_tokenizer == 'nltk_punkt':
            assert sentences == ['Die deutsche Sprache bzw. Deutsch ([dɔɪ̯tʃ];[26] abgekürzt dt.', 'oder dtsch.)', 'ist eine westgermanische Sprache, die weltweit etwa 90 bis 105 Millionen Menschen als Muttersprache und weiteren rund 80 Millionen als Zweit- oder Fremdsprache dient.', 'Das Deutsche ist eine plurizentrische Sprache, enthält also mehrere Standardvarietäten in verschiedenen Regionen.', 'Ihr Sprachgebiet umfasst Deutschland, Österreich, die Deutschschweiz, Liechtenstein, Luxemburg, Ostbelgien, Südtirol, das Elsass und Lothringen sowie Nordschleswig.', 'Außerdem ist Deutsch eine Minderheitensprache in einigen europäischen und außereuropäischen Ländern, z.', 'B. in Rumänien und Südafrika sowie Nationalsprache im afrikanischen Namibia.', 'Deutsch ist die meistgesprochene Muttersprache in der Europäischen Union (EU).', '[27]']
        elif sentence_tokenizer == 'spacy_sentence_recognizer':
            assert sentences == ['Die deutsche Sprache bzw. Deutsch ([dɔɪ̯tʃ];[26] abgekürzt dt.', 'oder dtsch.) ist eine westgermanische Sprache, die weltweit etwa 90 bis 105 Millionen Menschen als Muttersprache und weiteren rund 80 Millionen als Zweit- oder Fremdsprache dient.', 'Das Deutsche ist eine plurizentrische Sprache, enthält also mehrere Standardvarietäten in verschiedenen Regionen.', 'Ihr Sprachgebiet umfasst Deutschland, Österreich, die Deutschschweiz, Liechtenstein, Luxemburg, Ostbelgien, Südtirol, das Elsass und Lothringen sowie Nordschleswig.', 'Außerdem ist Deutsch eine Minderheitensprache in einigen europäischen und außereuropäischen Ländern, z. B. in Rumänien und Südafrika sowie Nationalsprache im afrikanischen Namibia.', 'Deutsch ist die meistgesprochene Muttersprache in der Europäischen Union (EU).[27]']
        else:
            raise Exception(f'Error: Tests for sentence tokenizer "{sentence_tokenizer}" is skipped!')
    elif lang == 'ell':
        if sentence_tokenizer == 'nltk_punkt':
            assert sentences == ['Η ελληνική γλώσσα ανήκει στην ινδοευρωπαϊκή οικογένεια[9] και αποτελεί το μοναδικό μέλος του ελληνικού κλάδου, ενώ είναι η επίσημη γλώσσα της Ελλάδας και της Κύπρου.', 'Ανήκει επίσης στο βαλκανικό γλωσσικό δεσμό.', 'Στην ελληνική γλώσσα, έχουμε γραπτά κείμενα ήδη από τον 15ο αιώνα π.Χ.. Σαν Παγκόσμια Ημέρα Ελληνικής Γλώσσας, κάθε έτος, έχει καθιερωθεί η 9η Φεβρουαρίου.', 'Έχει την μακροβιότερη καταγεγραμμένη ιστορία από οποιαδήποτε άλλη ζωντανή ινδοευρωπαϊκή γλώσσα με τουλάχιστον 3.400 χρόνια γραπτής ιστορίας.', '[10] Γράφεται με το ελληνικό αλφάβητο το οποίο χρησιμοποιείται για περίπου 2.600 χρόνια.', '[11][12] Προηγουμένως η ελληνική γλώσσα γραφόταν με τη Γραμμική Β και το κυπριακό συλλαβάριο.', '[13] Το ελληνικό αλφάβητο προέρχεται από το φοινικικό αλφάβητο.', 'Στο ελληνικό αλφάβητο βασίζεται το λατινικό, το κυριλλικό, το αρμενικό, το κοπτικό, το γοτθικό και πολλά άλλα αλφάβητα.']
        elif sentence_tokenizer == 'spacy_sentence_recognizer':
            assert sentences == ['Η ελληνική γλώσσα ανήκει στην ινδοευρωπαϊκή οικογένεια[9] και αποτελεί το μοναδικό μέλος του ελληνικού κλάδου, ενώ είναι η επίσημη γλώσσα της Ελλάδας και της Κύπρου.', 'Ανήκει επίσης στο βαλκανικό γλωσσικό δεσμό.', 'Στην ελληνική γλώσσα, έχουμε γραπτά κείμενα ήδη από τον 15ο αιώνα π.', 'Χ..', 'Σαν Παγκόσμια Ημέρα Ελληνικής Γλώσσας, κάθε έτος, έχει καθιερωθεί η 9η Φεβρουαρίου.', 'Έχει την μακροβιότερη καταγεγραμμένη ιστορία από οποιαδήποτε άλλη ζωντανή ινδοευρωπαϊκή γλώσσα με τουλάχιστον 3.400 χρόνια γραπτής ιστορίας.[10] Γράφεται με το ελληνικό αλφάβητο το οποίο χρησιμοποιείται για περίπου 2.600 χρόνια.[11][12] Προηγουμένως η ελληνική γλώσσα γραφόταν με τη Γραμμική Β και το κυπριακό συλλαβάριο.[13] Το ελληνικό αλφάβητο προέρχεται από το φοινικικό αλφάβητο.', 'Στο ελληνικό αλφάβητο βασίζεται το λατινικό, το κυριλλικό, το αρμενικό, το κοπτικό, το γοτθικό και πολλά άλλα αλφάβητα.']
        else:
            raise Exception(f'Error: Tests for sentence tokenizer "{sentence_tokenizer}" is skipped!')
    elif lang == 'ita':
        if sentence_tokenizer == 'nltk_punkt':
            assert sentences == ["L'italiano ([itaˈljaːno][Nota 1] ascolta[?·info]) è una lingua romanza parlata principalmente in Italia.", 'È classificato al 23º posto tra le lingue per numero di parlanti nel mondo e, in Italia, è utilizzato da circa 58 milioni di residenti.', "[2] Nel 2015 l'italiano era la lingua materna del 90,4% dei residenti in Italia,[3] che spesso lo acquisiscono e lo usano insieme alle varianti regionali dell'italiano, alle lingue regionali e ai dialetti.", "In Italia viene ampiamente usato per tutti i tipi di comunicazione della vita quotidiana ed è largamente prevalente nei mezzi di comunicazione nazionali, nell'amministrazione pubblica dello Stato italiano e nell'editoria."]
        elif sentence_tokenizer == 'spacy_sentence_recognizer':
            assert sentences == ["L'italiano ([itaˈljaːno][Nota 1] ascolta[?·info]) è una lingua romanza parlata principalmente in Italia.", "È classificato al 23º posto tra le lingue per numero di parlanti nel mondo e, in Italia, è utilizzato da circa 58 milioni di residenti.[2] Nel 2015 l'italiano era la lingua materna del 90,4% dei residenti in Italia,[3] che spesso lo acquisiscono e lo usano insieme alle varianti regionali dell'italiano, alle lingue regionali e ai dialetti.", "In Italia viene ampiamente usato per tutti i tipi di comunicazione della vita quotidiana ed è largamente prevalente nei mezzi di comunicazione nazionali, nell'amministrazione pubblica dello Stato italiano e nell'editoria."]
        else:
            raise Exception(f'Error: Tests for sentence tokenizer "{sentence_tokenizer}" is skipped!')
    elif lang == 'jpn':
        assert sentences == ['日本語（にほんご、にっぽんご[注 2]）は、日本国内や、かつての日本領だった国、そして日本人同士の間で使用されている言語。', '日本は法令によって公用語を規定していないが、法令その他の公用文は全て日本語で記述され、各種法令[10]において日本語を用いることが規定され、学校教育においては「国語」の教科として学習を行う等、事実上、日本国内において唯一の公用語となっている。']
    elif lang == 'lit':
        assert sentences == ['Lietuvių kalba – iš baltų prokalbės kilusi lietuvių tautos kalba, kuri Lietuvoje yra valstybinė, o Europos Sąjungoje – viena iš oficialiųjų kalbų.', 'Lietuviškai kalba apie tris milijonus žmonių (dauguma jų gyvena Lietuvoje).', 'Drauge su latvių, mirusiomis prūsų, jotvingių ir kitomis baltų kalbomis priklauso indoeuropiečių kalbų šeimos baltų kalbų grupei.']
    elif lang == 'nob':
        if sentence_tokenizer == 'nltk_punkt':
            assert sentences == ['Bokmål er en varietet av norsk skriftspråk.', 'Bokmål er en av to offisielle målformer av norsk skriftspråk, hvorav den andre er nynorsk.', 'I skrift benyttes bokmål av anslagsvis 90 % av befolkningen i Norge.', '[1][2] Etter skriftreformene av riksmål i 1987 og bokmål i 1981 og 2005 er det lite som skiller bokmål og riksmål i alminnelig bruk.']
        elif sentence_tokenizer == 'spacy_sentence_recognizer':
            assert sentences == ['Bokmål er en varietet av norsk skriftspråk.', 'Bokmål er en av to offisielle målformer av norsk skriftspråk, hvorav den andre er nynorsk.', 'I skrift benyttes bokmål av anslagsvis 90 % av befolkningen i Norge.[1][2]', 'Etter skriftreformene av riksmål i 1987 og bokmål i 1981 og 2005 er det lite som skiller bokmål og riksmål i alminnelig bruk.']
        else:
            raise Exception(f'Error: Tests for sentence tokenizer "{sentence_tokenizer}" is skipped!')
    elif lang == 'nno':
        assert sentences == ['Nynorsk, før 1929 offisielt kalla landsmål, er sidan jamstillingsvedtaket av 12. mai 1885 ei av dei to offisielle målformene av norsk; den andre forma er bokmål.', 'Nynorsk blir i dag nytta av om lag 10–15% av innbyggjarane[1][2] i Noreg.', 'Skriftspråket er basert på nynorsk talemål, det vil seie dei moderne norske dialektane til skilnad frå gamalnorsk og mellomnorsk.', 'Når ein seier at nokon snakkar nynorsk, meiner ein helst at dei snakkar nynorsk normaltalemål.', 'Dei færraste dialekttalande nordmenn seier at dei snakkar nynorsk, men det er ikkje uvanleg i kjerneområda til nynorsken.', 'Dette tilhøvet mellom tale og skrift ligg bak målrørsla sitt slagord sidan 1970-talet: «Snakk dialekt – skriv nynorsk!» Nynorske dialektar blir snakka over heile landet, men det er berre på Vestlandet utanom dei største byene og i dei austlandske fjellbygdene at skriftspråket står sterkt.', 'Det vil seie at dei fleste dialekttalarane har bokmål som det primære skriftspråket sitt.']
    elif lang == 'pol':
        assert sentences == ['Język polski, polszczyzna – język lechicki z grupy zachodniosłowiańskiej (do której należą również czeski, kaszubski, słowacki i języki łużyckie), stanowiącej część rodziny indoeuropejskiej.', 'Jest językiem urzędowym w Polsce oraz należy do oficjalnych języków Unii Europejskiej.', 'Ocenia się, że jest mową ojczystą ok. 44 mln ludzi na świecie[1] (w literaturze naukowej można spotkać szacunki od 39[2][3] do 48 mln[4]).', 'Językiem tym posługują się przede wszystkim mieszkańcy Polski oraz przedstawiciele tak zwanej Polonii, czyli ludność polska zamieszkała za granicą.']
    elif lang.startswith('por_'):
        if sentence_tokenizer == 'nltk_punkt':
            assert sentences == ['A língua portuguesa, também designada português, é uma língua indo-europeia românica flexiva ocidental originada no galego-português falado no Reino da Galiza e no norte de Portugal.', 'Com a criação do Reino de Portugal em 1139 e a expansão para o sul na sequência da Reconquista, deu-se a difusão da língua pelas terras conquistadas e mais tarde, com as descobertas portuguesas, para o Brasil, África e outras partes do mundo.', '[3] O português foi usado, naquela época, não somente nas cidades conquistadas pelos portugueses, mas também por muitos governantes locais nos seus contatos com outros estrangeiros poderosos.', 'Especialmente nessa altura a língua portuguesa também influenciou várias línguas.', '[4]']
        elif sentence_tokenizer == 'spacy_sentence_recognizer':
            assert sentences == ['A língua portuguesa, também designada português, é uma língua indo-europeia românica flexiva ocidental originada no galego-português falado no Reino da Galiza e no norte de Portugal.', 'Com a criação do Reino de Portugal em 1139 e a expansão para o sul na sequência da Reconquista, deu-se a difusão da língua pelas terras conquistadas e mais tarde, com as descobertas portuguesas, para o Brasil, África e outras partes do mundo.[3]', 'O português foi usado, naquela época, não somente nas cidades conquistadas pelos portugueses, mas também por muitos governantes locais nos seus contatos com outros estrangeiros poderosos.', 'Especialmente nessa altura a língua portuguesa também influenciou várias línguas.[4]']
        else:
            raise Exception(f'Error: Tests for sentence tokenizer "{sentence_tokenizer}" is skipped!')
    elif lang == 'ron':
        assert sentences == ['Limba română este o limbă indo-europeană, din grupul italic și din subgrupul oriental al limbilor romanice.', 'Printre limbile romanice, româna este a cincea după numărul de vorbitori, în urma spaniolei, portughezei, francezei și italienei.', 'Din motive de diferențiere tipologică, limba română mai este numită în lingvistica comparată limba dacoromână sau dialectul dacoromân.', 'De asemenea, este înregistrată ca limbă de stat atât în România cât și în Republica Moldova, unde circa 75% din populație o consideră limbă maternă (inclusiv sub denumirea de „limba moldovenească”).']
    elif lang == 'rus':
        assert sentences == ['Ру́сский язы́к ([ˈruskʲɪi̯ jɪˈzɨk] Информация о файле слушать)[~ 3][⇨] — язык восточнославянской группы славянской ветви индоевропейской языковой семьи, национальный язык русского народа.', 'Является одним из наиболее распространённых языков мира — шестым среди всех языков мира по общей численности говорящих и восьмым по численности владеющих им как родным[9].', 'Русский является также самым распространённым славянским языком[10] и самым распространённым языком в Европе — географически и по числу носителей языка как родного[7].']
    elif lang == 'slv':
        assert sentences == ['Slovenščina [sloˈʋenʃtʃina] je združeni naziv za uradni knjižni jezik Slovencev in skupno ime za narečja in govore, ki jih govorijo ali so jih nekoč govorili Slovenci.', 'Govori ga okoli 2,5 (dva in pol) milijona govorcev po svetu, od katerih jih večina živi v Sloveniji.', 'Glede na število govorcev ima razmeroma veliko narečij.', 'Slovenščina je zahodni južnoslovanski jezik in eden redkih indoevropskih jezikov, ki je ohranil dvojino.', 'Za zapisovanje slovenskega jezika se danes uporablja gajica, pisava imenovana po Ljudevitu Gaju, ki jo je priredil po češkem črkopisu.', 'Slovenska gajica se imenuje slovenica.', 'Pišemo jo od marčne revolucije 1848.', 'Do takrat smo uporabljali bohoričico.']
    elif lang == 'spa':
        assert sentences == ['El español o castellano es una lengua romance procedente del latín hablado, perteneciente a la familia de lenguas indoeuropeas.', 'Forma parte del grupo ibérico y es originaria de Castilla, reino medieval de la península ibérica.', 'Se conoce también informalmente como «castilla»,n.', '1\u200b31\u200b32\u200b en algunas áreas rurales e indígenas de América,33\u200b pues el español se empezó a enseñar poco después de la incorporación de los nuevos territorios a la Corona de Castilla.34\u200b35\u200b36\u200b37\u200b38\u200b39\u200b']
    elif lang == 'swe':
        assert sentences == ['Svenska (svenska\u2009(info)) är ett östnordiskt språk som talas av ungefär tio miljoner personer främst i Sverige där språket har en dominant ställning som huvudspråk, men även som det ena nationalspråket i Finland och som enda officiella språk på Åland.', 'I övriga Finland talas det som modersmål framförallt i de finlandssvenska kustområdena i Österbotten, Åboland och Nyland.', 'En liten minoritet svenskspråkiga finns även i Estland.', 'Svenska är nära besläktat och i hög grad ömsesidigt begripligt med danska och norska.', 'De andra nordiska språken, isländska och färöiska, är mindre ömsesidigt begripliga med svenska.', 'Liksom de övriga nordiska språken härstammar svenskan från en gren av fornnordiska, vilket var det språk som talades av de germanska folken i Skandinavien.']
    elif lang == 'tha':
        assert sentences == ['ภาษาไทย หรือ ภาษาไทยกลาง เป็นภาษาในกลุ่มภาษาไท ซึ่งเป็นกลุ่มย่อยของตระกูลภาษาขร้า-ไท และเป็นภาษาราชการ และภาษาประจำชาติของประเทศไทย[3][4] มีการสันนิษฐานว่าภาษาในตระกูลนี้มีถิ่นกำเนิดจากทางตอนใต้ของประเทศจีน และนักภาษาศาสตร์บางส่วนเสนอว่า ภาษาไทยน่าจะมีความเชื่อมโยงกับตระกูลภาษาออสโตร-เอเชียติก', 'ตระกูลภาษาออสโตรนีเซียน และตระกูลภาษาจีน-ทิเบต']
    elif lang == 'bod':
        assert sentences == ['བོད་ཀྱི་སྐད་ཡིག་ནི་བོད་ཡུལ་དང་ཉེ་འཁོར་གྱི་ས་ཁུལ་བལ་ཡུལ། འབྲུག་དང་འབྲས་ལྗོངས། ལ་དྭགས་ནས་ལྷོ་མོན་རོང་སོགས་སུ་བེད་སྤྱོད་བྱེད་པའི་སྐད་ཡིག་དེ།', 'ད་ཆར་ཡོངས་གྲགས་སུ་བོད་ཀྱི་ཡུལ་གྲུ་སྟོད་སྨད་བར་གསུམ་ལ་ལྟོས་ཏེ་ནང་གསེས་རིགས་གསུམ་དུ་ཕྱེ་བ་སྟེ།', 'སྟོད་དབུས་གཙང་གི་སྐད་དང་། བར་ཁམས་པའི་སྐད་དང་། སྨད་ཨ་མདོའི་སྐད་རྣམས་སོ།', 'བོད་སྐད་ནི་ཧོར་སོག་ལ་སོགས་པ་གྲངས་ཉུང་མི་རིགས་གཞན་པ་ཁག་ཅིག་གིས་བེད་སྤྱོད་གཏོང་བཞིན་ཡོད་པར་མ་ཟད། བལ་ཡུལ་དང་། འབྲས་ལྗོངས། འབྲུག་ཡུལ་། རྒྱ་གར་ཤར་དང་བྱང་རྒྱུད་མངའ་སྡེ་ཁག་གཅིག་བཅས་ཀྱི་རྒྱལ་ཁབ་རྣམས་སུའང་བེད་སྤྱོད་གཏོང་བཞིན་ཡོད།']
    elif lang == 'tur':
        assert sentences == ["Türkçe ya da Türk dili, Güneydoğu Avrupa ve Batı Asya'da konuşulan, Türk dilleri dil ailesine ait sondan eklemeli bir dil.", '[12] Türk dilleri ailesinin Oğuz dilleri grubundan bir Batı Oğuz dili olan Osmanlı Türkçesinin devamını oluşturur.', "Dil, başta Türkiye olmak üzere Balkanlar, Ege Adaları, Kıbrıs ve Orta Doğu'yu kapsayan eski Osmanlı İmparatorluğu coğrafyasında konuşulur.", "[12] Ethnologue'a göre Türkçe, yaklaşık 83 milyon konuşuru ile dünyada en çok konuşulan 16.", 'dildir.', "[13] Türkçe Türkiye, Kıbrıs Cumhuriyeti ve Kuzey Kıbrıs'ta ulusal resmî dil statüsüne sahiptir.", '[12]']
    elif lang == 'vie':
        assert sentences == ['Tiếng Việt, cũng gọi là tiếng Việt Nam[8] hay Việt ngữ là ngôn ngữ của người Việt và là ngôn ngữ chính thức tại Việt Nam.', 'Đây là tiếng mẹ đẻ của khoảng 85% dân cư Việt Nam cùng với hơn 4 triệu người Việt kiều.', 'Tiếng Việt còn là ngôn ngữ thứ hai của các dân tộc thiểu số tại Việt Nam và là ngôn ngữ dân tộc thiểu số được công nhận tại Cộng hòa Séc.']
    else:
        raise Exception(f'Error: Tests for language "{lang}" is skipped!')

@pytest.mark.parametrize('lang', test_langs)
def test_sentence_split(lang):
    print(f'Testing {lang} / Sentence Splitter...')

    sentences_split = wl_sentence_tokenization.wl_sentence_split(
        main,
        text = getattr(wl_test_lang_examples, f'TEXT_{lang.upper()}')
    )

    if lang not in ['zho_cn', 'zho_tw', 'jpn', 'tha', 'bod']:
        assert len(sentences_split) > 1

@pytest.mark.parametrize('lang', test_langs)
def test_sentence_seg_tokenize(lang):
    sentence_segs = wl_sentence_tokenization.wl_sentence_seg_tokenize(
        main,
        text = getattr(wl_test_lang_examples, f'TEXT_{lang.upper()}')
    )

    print(f'{lang} / Sentence Segment Tokenizer:')
    print(f'{sentence_segs}\n')

    if lang not in ['tha']:
        assert len(sentence_segs) > 1

    if lang == 'zho_cn':
        assert sentence_segs == ['汉语又称华语[3]、', '唐话[4]，', '概指由上古汉语（先秦雅言）发展而来、', '书面使用汉字的分析语，', '为汉藏语系最大的一支语族。', '如把整个汉语族视为单一语言，', '则汉语为世界使用人数最多的语言，', '目前全世界有五分之一人口将汉语做为母语或第二语言。']
    elif lang == 'zho_tw':
        assert sentence_segs == ['漢語又稱華語[3]、', '唐話[4]，', '概指由上古漢語（先秦雅言）發展而來、', '書面使用漢字的分析語，', '為漢藏語系最大的一支語族。', '如把整個漢語族視為單一語言，', '則漢語為世界使用人數最多的語言，', '目前全世界有五分之一人口將漢語做為母語或第二語言。']
    elif lang == 'ces':
        assert sentence_segs == ['Čeština neboli český jazyk je západoslovanský jazyk,', 'nejbližší slovenštině,', 'poté lužické srbštině a polštině.', 'Patří mezi slovanské jazyky,', 'do rodiny jazyků indoevropských.', 'Čeština se vyvinula ze západních nářečí praslovanštiny na konci 10.', 'století.', 'Je částečně ovlivněná latinou a němčinou.', 'Česky psaná literatura se objevuje od 14.', 'století.', 'První písemné památky jsou však již z 12.', 'století.']
    elif lang == 'dan':
        assert sentence_segs == ['Dansk er et østnordisk sprog indenfor den germanske gren af den indoeuropæiske sprogfamilie.', 'Det danske sprog tales af ca.', 'seks millioner mennesker,', 'hovedsageligt i Danmark,', 'men også i Sydslesvig (i Flensborg ca.', '20 %),', 'på Færøerne og Grønland.', '[1] Dansk er tæt forbundet med norsk og svensk,', 'og sproghistorisk har dansk været stærkt påvirket af plattysk.']
    elif lang == 'nld':
        assert sentence_segs == ['Het Nederlands is een West-Germaanse taal en de officiële taal van Nederland,', 'Suriname en een van de drie officiële talen van België.', 'Binnen het Koninkrijk der Nederlanden is het Nederlands ook een officiële taal van Aruba,', 'Curaçao en Sint-Maarten.', 'Het Nederlands is de op twee na meest gesproken Germaanse taal.']
    elif lang.startswith('eng_'):
        assert sentence_segs == ['English is a West Germanic language of the Indo-European language family,', 'originally spoken by the inhabitants of early medieval England.', '[3][4][5] It is named after the Angles,', 'one of the ancient Germanic peoples that migrated from Anglia,', 'a peninsula on the Baltic Sea (not to be confused with East Anglia in England),', 'to the area of Great Britain later named after them:', 'England.', 'The closest living relatives of English include Scots,', 'followed by the Low Saxon and Frisian languages.', 'While English is genealogically West Germanic,', 'its vocabulary is also distinctively influenced by dialects of French (about 29% of modern English words) and Latin (also about 29%),', 'as well as by Old Norse (a North Germanic language).', '[6][7][8] Speakers of English are called Anglophones.']
    elif lang == 'est':
        assert sentence_segs == ['Eesti keel (varasem nimetus maakeel) on läänemeresoome lõunarühma kuuluv keel.', 'Eesti keel on Eesti riigikeel ja 2004.', 'aastast ka üks Euroopa Liidu ametlikke keeli.']
    elif lang == 'fin':
        assert sentence_segs == ['Suomen kieli (suomi) on uralilaisten kielten itämerensuomalaiseen ryhmään kuuluva kieli,', 'jota puhuvat pääosin suomalaiset.', 'Sitä puhuu äidinkielenään Suomessa 4,', '8 miljoonaa ja toisena kielenä 0,', '5 miljoonaa ihmistä.', 'Suurimmat suomea puhuvat vähemmistöt ovat Ruotsissa,', 'Norjassa ja Venäjällä.']
    elif lang == 'fra':
        assert sentence_segs == ['Le français est une langue indo-européenne de la famille des langues romanes dont les locuteurs sont appelés francophones,', 'également surnommé la langue de Molière.', 'Le français est parlé,', 'en 2022[Lien à corriger],', 'sur tous les continents par environ 321 millions de personnes5,', '2 :', "235 millions l'emploient quotidiennement,", 'et 90 millions3 en sont des locuteurs natifs.', 'En 2018,', "80 millions d'élèves et étudiants s'instruisent en français dans le monde6.", "Selon l'Organisation internationale de la francophonie (OIF),", 'il pourrait y avoir 700 millions de francophones sur Terre en 20507.']
    elif lang.startswith('deu_'):
        assert sentence_segs == ['Die deutsche Sprache bzw.', 'Deutsch ([dɔɪ̯tʃ];', '[26] abgekürzt dt.', 'oder dtsch.', ') ist eine westgermanische Sprache,', 'die weltweit etwa 90 bis 105 Millionen Menschen als Muttersprache und weiteren rund 80 Millionen als Zweit- oder Fremdsprache dient.', 'Das Deutsche ist eine plurizentrische Sprache,', 'enthält also mehrere Standardvarietäten in verschiedenen Regionen.', 'Ihr Sprachgebiet umfasst Deutschland,', 'Österreich,', 'die Deutschschweiz,', 'Liechtenstein,', 'Luxemburg,', 'Ostbelgien,', 'Südtirol,', 'das Elsass und Lothringen sowie Nordschleswig.', 'Außerdem ist Deutsch eine Minderheitensprache in einigen europäischen und außereuropäischen Ländern,', 'z.', 'B.', 'in Rumänien und Südafrika sowie Nationalsprache im afrikanischen Namibia.', 'Deutsch ist die meistgesprochene Muttersprache in der Europäischen Union (EU).', '[27]']
    elif lang == 'ell':
        assert sentence_segs == ['Η ελληνική γλώσσα ανήκει στην ινδοευρωπαϊκή οικογένεια[9] και αποτελεί το μοναδικό μέλος του ελληνικού κλάδου,', 'ενώ είναι η επίσημη γλώσσα της Ελλάδας και της Κύπρου.', 'Ανήκει επίσης στο βαλκανικό γλωσσικό δεσμό.', 'Στην ελληνική γλώσσα,', 'έχουμε γραπτά κείμενα ήδη από τον 15ο αιώνα π.', 'Χ..', 'Σαν Παγκόσμια Ημέρα Ελληνικής Γλώσσας,', 'κάθε έτος,', 'έχει καθιερωθεί η 9η Φεβρουαρίου.', 'Έχει την μακροβιότερη καταγεγραμμένη ιστορία από οποιαδήποτε άλλη ζωντανή ινδοευρωπαϊκή γλώσσα με τουλάχιστον 3.', '400 χρόνια γραπτής ιστορίας.', '[10] Γράφεται με το ελληνικό αλφάβητο το οποίο χρησιμοποιείται για περίπου 2.', '600 χρόνια.', '[11][12] Προηγουμένως η ελληνική γλώσσα γραφόταν με τη Γραμμική Β και το κυπριακό συλλαβάριο.', '[13] Το ελληνικό αλφάβητο προέρχεται από το φοινικικό αλφάβητο.', 'Στο ελληνικό αλφάβητο βασίζεται το λατινικό,', 'το κυριλλικό,', 'το αρμενικό,', 'το κοπτικό,', 'το γοτθικό και πολλά άλλα αλφάβητα.']
    elif lang == 'ita':
        assert sentence_segs == ["L'italiano ([itaˈljaːno][Nota 1] ascolta[?", '·info]) è una lingua romanza parlata principalmente in Italia.', 'È classificato al 23º posto tra le lingue per numero di parlanti nel mondo e,', 'in Italia,', 'è utilizzato da circa 58 milioni di residenti.', "[2] Nel 2015 l'italiano era la lingua materna del 90,", '4% dei residenti in Italia,', "[3] che spesso lo acquisiscono e lo usano insieme alle varianti regionali dell'italiano,", 'alle lingue regionali e ai dialetti.', 'In Italia viene ampiamente usato per tutti i tipi di comunicazione della vita quotidiana ed è largamente prevalente nei mezzi di comunicazione nazionali,', "nell'amministrazione pubblica dello Stato italiano e nell'editoria."]
    elif lang == 'jpn':
        assert sentence_segs == ['日本語（にほんご、', 'にっぽんご[注 2]）は、', '日本国内や、', 'かつての日本領だった国、', 'そして日本人同士の間で使用されている言語。', '日本は法令によって公用語を規定していないが、', '法令その他の公用文は全て日本語で記述され、', '各種法令[10]において日本語を用いることが規定され、', '学校教育においては「国語」の教科として学習を行う等、', '事実上、', '日本国内において唯一の公用語となっている。']
    elif lang == 'lit':
        assert sentence_segs == ['Lietuvių kalba – iš baltų prokalbės kilusi lietuvių tautos kalba,', 'kuri Lietuvoje yra valstybinė,', 'o Europos Sąjungoje – viena iš oficialiųjų kalbų.', 'Lietuviškai kalba apie tris milijonus žmonių (dauguma jų gyvena Lietuvoje).', 'Drauge su latvių,', 'mirusiomis prūsų,', 'jotvingių ir kitomis baltų kalbomis priklauso indoeuropiečių kalbų šeimos baltų kalbų grupei.']
    elif lang == 'nob':
        assert sentence_segs == ['Bokmål er en varietet av norsk skriftspråk.', 'Bokmål er en av to offisielle målformer av norsk skriftspråk,', 'hvorav den andre er nynorsk.', 'I skrift benyttes bokmål av anslagsvis 90 % av befolkningen i Norge.', '[1][2] Etter skriftreformene av riksmål i 1987 og bokmål i 1981 og 2005 er det lite som skiller bokmål og riksmål i alminnelig bruk.']
    elif lang == 'nno':
        assert sentence_segs == ['Nynorsk,', 'før 1929 offisielt kalla landsmål,', 'er sidan jamstillingsvedtaket av 12.', 'mai 1885 ei av dei to offisielle målformene av norsk;', 'den andre forma er bokmål.', 'Nynorsk blir i dag nytta av om lag 10–15% av innbyggjarane[1][2] i Noreg.', 'Skriftspråket er basert på nynorsk talemål,', 'det vil seie dei moderne norske dialektane til skilnad frå gamalnorsk og mellomnorsk.', 'Når ein seier at nokon snakkar nynorsk,', 'meiner ein helst at dei snakkar nynorsk normaltalemål.', 'Dei færraste dialekttalande nordmenn seier at dei snakkar nynorsk,', 'men det er ikkje uvanleg i kjerneområda til nynorsken.', 'Dette tilhøvet mellom tale og skrift ligg bak målrørsla sitt slagord sidan 1970-talet:', '«Snakk dialekt – skriv nynorsk!', '» Nynorske dialektar blir snakka over heile landet,', 'men det er berre på Vestlandet utanom dei største byene og i dei austlandske fjellbygdene at skriftspråket står sterkt.', 'Det vil seie at dei fleste dialekttalarane har bokmål som det primære skriftspråket sitt.']
    elif lang == 'pol':
        assert sentence_segs == ['Język polski,', 'polszczyzna – język lechicki z grupy zachodniosłowiańskiej (do której należą również czeski,', 'kaszubski,', 'słowacki i języki łużyckie),', 'stanowiącej część rodziny indoeuropejskiej.', 'Jest językiem urzędowym w Polsce oraz należy do oficjalnych języków Unii Europejskiej.', 'Ocenia się,', 'że jest mową ojczystą ok.', '44 mln ludzi na świecie[1] (w literaturze naukowej można spotkać szacunki od 39[2][3] do 48 mln[4]).', 'Językiem tym posługują się przede wszystkim mieszkańcy Polski oraz przedstawiciele tak zwanej Polonii,', 'czyli ludność polska zamieszkała za granicą.']
    elif lang.startswith('por_'):
        assert sentence_segs == ['A língua portuguesa,', 'também designada português,', 'é uma língua indo-europeia românica flexiva ocidental originada no galego-português falado no Reino da Galiza e no norte de Portugal.', 'Com a criação do Reino de Portugal em 1139 e a expansão para o sul na sequência da Reconquista,', 'deu-se a difusão da língua pelas terras conquistadas e mais tarde,', 'com as descobertas portuguesas,', 'para o Brasil,', 'África e outras partes do mundo.', '[3] O português foi usado,', 'naquela época,', 'não somente nas cidades conquistadas pelos portugueses,', 'mas também por muitos governantes locais nos seus contatos com outros estrangeiros poderosos.', 'Especialmente nessa altura a língua portuguesa também influenciou várias línguas.', '[4]']
    elif lang == 'ron':
        assert sentence_segs == ['Limba română este o limbă indo-europeană,', 'din grupul italic și din subgrupul oriental al limbilor romanice.', 'Printre limbile romanice,', 'româna este a cincea după numărul de vorbitori,', 'în urma spaniolei,', 'portughezei,', 'francezei și italienei.', 'Din motive de diferențiere tipologică,', 'limba română mai este numită în lingvistica comparată limba dacoromână sau dialectul dacoromân.', 'De asemenea,', 'este înregistrată ca limbă de stat atât în România cât și în Republica Moldova,', 'unde circa 75% din populație o consideră limbă maternă (inclusiv sub denumirea de „limba moldovenească”).']
    elif lang == 'rus':
        assert sentence_segs == ['Ру́сский язы́к ([ˈruskʲɪi̯ jɪˈzɨk] Информация о файле слушать)[~ 3][⇨] — язык восточнославянской группы славянской ветви индоевропейской языковой семьи,', 'национальный язык русского народа.', 'Является одним из наиболее распространённых языков мира — шестым среди всех языков мира по общей численности говорящих и восьмым по численности владеющих им как родным[9].', 'Русский является также самым распространённым славянским языком[10] и самым распространённым языком в Европе — географически и по числу носителей языка как родного[7].']
    elif lang == 'slv':
        assert sentence_segs == ['Slovenščina [sloˈʋenʃtʃina] je združeni naziv za uradni knjižni jezik Slovencev in skupno ime za narečja in govore,', 'ki jih govorijo ali so jih nekoč govorili Slovenci.', 'Govori ga okoli 2,', '5 (dva in pol) milijona govorcev po svetu,', 'od katerih jih večina živi v Sloveniji.', 'Glede na število govorcev ima razmeroma veliko narečij.', 'Slovenščina je zahodni južnoslovanski jezik in eden redkih indoevropskih jezikov,', 'ki je ohranil dvojino.', 'Za zapisovanje slovenskega jezika se danes uporablja gajica,', 'pisava imenovana po Ljudevitu Gaju,', 'ki jo je priredil po češkem črkopisu.', 'Slovenska gajica se imenuje slovenica.', 'Pišemo jo od marčne revolucije 1848.', 'Do takrat smo uporabljali bohoričico.']
    elif lang == 'spa':
        assert sentence_segs == ['El español o castellano es una lengua romance procedente del latín hablado,', 'perteneciente a la familia de lenguas indoeuropeas.', 'Forma parte del grupo ibérico y es originaria de Castilla,', 'reino medieval de la península ibérica.', 'Se conoce también informalmente como «castilla»,', 'n.', '1\u200b31\u200b32\u200b en algunas áreas rurales e indígenas de América,', '33\u200b pues el español se empezó a enseñar poco después de la incorporación de los nuevos territorios a la Corona de Castilla.', '34\u200b35\u200b36\u200b37\u200b38\u200b39\u200b']
    elif lang == 'swe':
        assert sentence_segs == ['Svenska (svenska\u2009(info)) är ett östnordiskt språk som talas av ungefär tio miljoner personer främst i Sverige där språket har en dominant ställning som huvudspråk,', 'men även som det ena nationalspråket i Finland och som enda officiella språk på Åland.', 'I övriga Finland talas det som modersmål framförallt i de finlandssvenska kustområdena i Österbotten,', 'Åboland och Nyland.', 'En liten minoritet svenskspråkiga finns även i Estland.', 'Svenska är nära besläktat och i hög grad ömsesidigt begripligt med danska och norska.', 'De andra nordiska språken,', 'isländska och färöiska,', 'är mindre ömsesidigt begripliga med svenska.', 'Liksom de övriga nordiska språken härstammar svenskan från en gren av fornnordiska,', 'vilket var det språk som talades av de germanska folken i Skandinavien.']
    elif lang == 'tha':
        assert sentence_segs == ['ภาษาไทย หรือ ภาษาไทยกลาง เป็นภาษาในกลุ่มภาษาไท ซึ่งเป็นกลุ่มย่อยของตระกูลภาษาขร้า-ไท และเป็นภาษาราชการ และภาษาประจำชาติของประเทศไทย[3][4] มีการสันนิษฐานว่าภาษาในตระกูลนี้มีถิ่นกำเนิดจากทางตอนใต้ของประเทศจีน และนักภาษาศาสตร์บางส่วนเสนอว่า ภาษาไทยน่าจะมีความเชื่อมโยงกับตระกูลภาษาออสโตร-เอเชียติก ตระกูลภาษาออสโตรนีเซียน และตระกูลภาษาจีน-ทิเบต']
    elif lang == 'bod':
        assert sentence_segs == ['བོད་ཀྱི་སྐད་ཡིག་ནི་བོད་ཡུལ་དང་ཉེ་འཁོར་གྱི་ས་ཁུལ་བལ་ཡུལ།', 'འབྲུག་དང་འབྲས་ལྗོངས།', 'ལ་དྭགས་ནས་ལྷོ་མོན་རོང་སོགས་སུ་བེད་སྤྱོད་བྱེད་པའི་སྐད་ཡིག་དེ།', 'ད་ཆར་ཡོངས་གྲགས་སུ་བོད་ཀྱི་ཡུལ་གྲུ་སྟོད་སྨད་བར་གསུམ་ལ་ལྟོས་ཏེ་ནང་གསེས་རིགས་གསུམ་དུ་ཕྱེ་བ་སྟེ།', 'སྟོད་དབུས་གཙང་གི་སྐད་དང་།', 'བར་ཁམས་པའི་སྐད་དང་།', 'སྨད་ཨ་མདོའི་སྐད་རྣམས་སོ།', 'བོད་སྐད་ནི་ཧོར་སོག་ལ་སོགས་པ་གྲངས་ཉུང་མི་རིགས་གཞན་པ་ཁག་ཅིག་གིས་བེད་སྤྱོད་གཏོང་བཞིན་ཡོད་པར་མ་ཟད།', 'བལ་ཡུལ་དང་།', 'འབྲས་ལྗོངས།', 'འབྲུག་ཡུལ་།', 'རྒྱ་གར་ཤར་དང་བྱང་རྒྱུད་མངའ་སྡེ་ཁག་གཅིག་བཅས་ཀྱི་རྒྱལ་ཁབ་རྣམས་སུའང་བེད་སྤྱོད་གཏོང་བཞིན་ཡོད།']
    elif lang == 'tur':
        assert sentence_segs == ['Türkçe ya da Türk dili,', "Güneydoğu Avrupa ve Batı Asya'da konuşulan,", 'Türk dilleri dil ailesine ait sondan eklemeli bir dil.', '[12] Türk dilleri ailesinin Oğuz dilleri grubundan bir Batı Oğuz dili olan Osmanlı Türkçesinin devamını oluşturur.', 'Dil,', 'başta Türkiye olmak üzere Balkanlar,', 'Ege Adaları,', "Kıbrıs ve Orta Doğu'yu kapsayan eski Osmanlı İmparatorluğu coğrafyasında konuşulur.", "[12] Ethnologue'a göre Türkçe,", 'yaklaşık 83 milyon konuşuru ile dünyada en çok konuşulan 16.', 'dildir.', '[13] Türkçe Türkiye,', "Kıbrıs Cumhuriyeti ve Kuzey Kıbrıs'ta ulusal resmî dil statüsüne sahiptir.", '[12]']
    elif lang == 'vie':
        assert sentence_segs == ['Tiếng Việt,', 'cũng gọi là tiếng Việt Nam[8] hay Việt ngữ là ngôn ngữ của người Việt và là ngôn ngữ chính thức tại Việt Nam.', 'Đây là tiếng mẹ đẻ của khoảng 85% dân cư Việt Nam cùng với hơn 4 triệu người Việt kiều.', 'Tiếng Việt còn là ngôn ngữ thứ hai của các dân tộc thiểu số tại Việt Nam và là ngôn ngữ dân tộc thiểu số được công nhận tại Cộng hòa Séc.']
    else:
        raise Exception(f'Error: Tests for language "{lang}" is skipped!')

@pytest.mark.parametrize('lang', test_langs)
def test_sentence_seg_split(lang):
    print(f'Testing {lang} / Sentence Segment Splitter...')

    sentence_segs = wl_sentence_tokenization.wl_sentence_seg_split(
        main,
        text = getattr(wl_test_lang_examples, f'TEXT_{lang.upper()}')
    )

    if lang not in ['zho_cn', 'zho_tw', 'jpn', 'tha']:
        assert len(sentence_segs) > 1

@pytest.mark.parametrize('lang', test_langs)
def test_sentence_seg_tokenize_tokens(lang):
    print(f'Testing {lang} / Sentence Segment Tokenizer with tokens...')

    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = getattr(wl_test_lang_examples, f'TEXT_{lang.upper()}'),
        lang = lang
    )
    sentence_segs = wl_sentence_tokenization.wl_sentence_seg_tokenize_tokens(main, tokens)

    if lang not in ['tha']:
        assert len(sentence_segs) > 1

if __name__ == '__main__':
    for lang, sentence_tokenizer in test_sentence_tokenizers:
        test_sentence_tokenize(lang, sentence_tokenizer)

    for lang in test_langs:
        test_sentence_split(lang)

    for lang in test_langs:
        test_sentence_seg_tokenize(lang)

    for lang in test_langs:
        test_sentence_seg_split(lang)

    for lang in test_langs:
        test_sentence_seg_tokenize_tokens(lang)
