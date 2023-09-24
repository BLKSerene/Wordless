# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Sentence tokenization
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
from wordless.wl_nlp import wl_sentence_tokenization, wl_word_tokenization
from wordless.wl_utils import wl_misc

_, is_macos, _ = wl_misc.check_os()

main = wl_test_init.Wl_Test_Main()
wl_test_init.change_default_tokenizers(main)

test_sentence_tokenizers = []
test_sentence_tokenizers_local = []

for lang, sentence_tokenizers in main.settings_global['sentence_tokenizers'].items():
    for sentence_tokenizer in sentence_tokenizers:
        if sentence_tokenizer == 'botok_bod':
            test_sentence_tokenizers.append(pytest.param(
                lang, sentence_tokenizer,
                marks = pytest.mark.xfail(is_macos, reason = 'https://github.com/OpenPecha/Botok/issues/76')
            ))

            test_sentence_tokenizers_local.append((lang, sentence_tokenizer))
        elif not sentence_tokenizer.startswith(('spacy_', 'stanza_')):
            test_sentence_tokenizers.append((lang, sentence_tokenizer))
            test_sentence_tokenizers_local.append((lang, sentence_tokenizer))

test_langs = list(dict.fromkeys([lang for lang, _ in test_sentence_tokenizers_local]))
test_langs_local = test_langs[:]

test_langs[test_langs.index('bod')] = pytest.param(
    'bod',
    marks = pytest.mark.xfail(is_macos, reason = 'https://github.com/OpenPecha/Botok/issues/76')
)

@pytest.mark.parametrize('lang, sentence_tokenizer', test_sentence_tokenizers)
def test_sentence_tokenize(lang, sentence_tokenizer):
    sentences = wl_sentence_tokenization.wl_sentence_tokenize(
        main,
        text = ''.join(getattr(wl_test_lang_examples, f'TEXT_{lang.upper()}')),
        lang = lang,
        sentence_tokenizer = sentence_tokenizer
    )

    print(f'{lang} / {sentence_tokenizer}:')
    print(f'{sentences}\n')

    # The count of sentences should be more than 1
    assert len(sentences) > 1

    tests_lang_util_skipped = False

    if lang == 'ces':
        assert sentences == ['Čeština neboli český jazyk je západoslovanský jazyk, nejbližší slovenštině, poté lužické srbštině a polštině.', 'Patří mezi slovanské jazyky, do rodiny jazyků indoevropských.', 'Čeština se vyvinula ze západních nářečí praslovanštiny na konci 10. století.', 'Je částečně ovlivněná latinou a němčinou.', 'Česky psaná literatura se objevuje od 14. století.', 'První písemné památky jsou však již z 12. století.']
    elif lang == 'dan':
        assert sentences == ['Dansk er et østnordisk sprog indenfor den germanske gren af den indoeuropæiske sprogfamilie.', 'Det danske sprog tales af ca. seks millioner mennesker, hovedsageligt i Danmark, men også i Sydslesvig (i Flensborg ca. 20 %), på Færøerne og Grønland.', '[1] Dansk er tæt beslægtet med norsk, svensk og islandsk, og sproghistorisk har dansk været stærkt påvirket af plattysk.']
    elif lang == 'nld':
        assert sentences == ['Het Nederlands is een West-Germaanse taal, de meest gebruikte taal in Nederland en België, de officiële taal van Suriname en een van de drie officiële talen van België.', 'Binnen het Koninkrijk der Nederlanden is het Nederlands ook een officiële taal van Aruba, Curaçao en Sint-Maarten.', 'Het Nederlands is na Engels en Duits de meest gesproken Germaanse taal.']
    elif lang.startswith('eng_') or lang == 'other':
        assert sentences == ['English is a West Germanic language in the Indo-European language family that originated in early medieval England.', '[3][4][5] It is the most spoken language in the world[6] and the third most spoken native language in the world, after Standard Chinese and Spanish.', '[7] Today, English is the primary language of the Anglosphere, which is usually defined as the United States, the United Kingdom, Canada, Australia, and New Zealand.', 'English is also the primary language of the Republic of Ireland, although it is not typically included within the Anglosphere.']
    elif lang == 'est':
        assert sentences == ['Eesti keelel on kaks suuremat murderühma (põhjaeesti ja lõunaeesti), mõnes käsitluses eristatakse ka kirderanniku murdeid eraldi murderühmana.', 'Liikumisvõimaluste laienemine ning põhjaeesti keskmurde alusel loodud normitud eesti kirjakeele kasutus on põhjustanud murdeerinevuste taandumise.']
    elif lang == 'fin':
        assert sentences == ['Suomen kieli eli suomi on uralilaisten kielten itämerensuomalaiseen ryhmään kuuluva kieli, jota puhuvat pääosin suomalaiset.', 'Suomessa suomen kieltä puhuu äidinkielenään 4,8 miljoonaa ja toisena kielenään 0,5 miljoonaa ihmistä.', 'Suurimmat suomea puhuvat vähemmistöt ovat Ruotsissa, Norjassa ja Venäjällä.']
    elif lang == 'fra':
        assert sentences == ['Le français est une langue indo-européenne de la famille des langues romanes dont les locuteurs sont appelés francophones.', 'Elle est parfois surnommée la langue de Molière.']
    elif lang.startswith('deu_'):
        assert sentences == ['Das Deutsche ist eine plurizentrische Sprache, enthält also mehrere Standardvarietäten in verschiedenen Regionen.', 'Ihr Sprachgebiet umfasst Deutschland, Österreich, die Deutschschweiz, Liechtenstein, Luxemburg, Ostbelgien, Südtirol, das Elsass und Lothringen sowie Nordschleswig.', 'Außerdem ist Deutsch eine Minderheitensprache in einigen europäischen und außereuropäischen Ländern, z.', 'B. in Rumänien und Südafrika sowie Nationalsprache im afrikanischen Namibia.', 'Deutsch ist die meistgesprochene Muttersprache in der Europäischen Union (EU).', '[26]']
    elif lang == 'ell':
        assert sentences == ['Η ελληνική γλώσσα ανήκει στην ινδοευρωπαϊκή οικογένεια[9] και αποτελεί το μοναδικό μέλος του ελληνικού κλάδου, ενώ είναι η επίσημη γλώσσα της Ελλάδας και της Κύπρου.', 'Ανήκει επίσης στο βαλκανικό γλωσσικό δεσμό.', 'Στην ελληνική γλώσσα, έχουμε γραπτά κείμενα ήδη από τον 15ο αιώνα π.Χ.. Σαν Παγκόσμια Ημέρα Ελληνικής Γλώσσας, κάθε έτος, έχει καθιερωθεί η 9η Φεβρουαρίου.', 'Έχει την μακροβιότερη καταγεγραμμένη ιστορία από οποιαδήποτε άλλη ζωντανή ινδοευρωπαϊκή γλώσσα με τουλάχιστον 3.400 χρόνια γραπτής ιστορίας.', '[10] Γράφεται με το ελληνικό αλφάβητο, το οποίο χρησιμοποιείται αδιάκοπα (αρχικά με τοπικές παραλλαγές, μετέπειτα υπό μια, ενιαία μορφή) εδώ και περίπου 2.600 χρόνια.', '[11][12] Προηγουμένως η ελληνική γλώσσα γραφόταν με τη Γραμμική Β και το κυπριακό συλλαβάριο.', '[13] Το ελληνικό αλφάβητο προέρχεται από το φοινικικό αλφάβητο, με κάποιες προσαρμογές.', 'Στο ελληνικό αλφάβητο βασίζεται το λατινικό, το κυριλλικό, το αρμενικό, το κοπτικό, το γοτθικό και πολλά άλλα αλφάβητα.']
    elif lang == 'ita':
        assert sentences == ["L'italiano ([itaˈljaːno][Nota 1] ascolta[?·info]) è una lingua romanza parlata principalmente in Italia.", "Per ragioni storiche e geografiche, l'italiano è la lingua romanza meno divergente dal latino.", '[2][3][4][Nota 2]']
    elif lang == 'khm':
        assert sentences == ['ភាសាខ្មែរ គឺជាភាសាកំណើតរបស់ជនជាតិខ្មែរនិងជាភាសាផ្លូវការរបស់ប្រទេសកម្ពុជា។', 'ភាសាសំស្ក្រឹតនិងភាសាបាលីបាន\u200bជួយបង្កើតខេមរភាសា ព្រោះភាសាខ្មែរបានខ្ចីពាក្យច្រើនពីភាសាទាំងពីរនេះ។', '\u200bមានអក្សរក្រមវែងជាងគេនៅលើពិភពលោក ។', '\u200b វាជាភាសាមួយដ៏ចំណាស់\u200b ដែលប្រហែលជាមានដើមកំណើតតាំងតែពី\u200b២០០០ឆ្នាំមុនមកម៉្លេះ។']
    elif lang == 'lao':
        assert sentences == ['ພາສາລາວ (Lao: ລາວ, [láːw] ຫຼື ພາສາລາວ, [pʰáːsǎːláːw]) ເປັນພາສາຕະກູນໄທ-ກະໄດຂອງຄົນລາວ ໂດຍມີຄົນເວົ້າໃນປະເທດລາວ ເຊິ່ງເປັນພາສາລັດຖະການຂອງສາທາລະນະລັດ ປະຊາທິປະໄຕ ປະຊາຊົນລາວ ຂອງປະຊາກອນປະມານ 7 ລ້ານຄົນ ແລະໃນພື້ນທີ່ພາກຕາເວັນອອກສຽງເໜືອຂອງປະເທດໄທທີ່ມີຄົນເວົ້າປະມານ 23 ລ້ານຄົນ ທາງລັດຖະບານປະເທດໄທມີການສະໜັບສະໜຸນໃຫ້ເອີ້ນພາສາລາວຖິ່ນໄທວ່າ ພາສາລາວຖິ່ນອີສານ ນອກຈາກນີ້, ຢູ່ທາງພາກຕາເວັນອອກສຽງເໜືອຂອງປະເທດກຳປູເຈຍກໍມີຄົນເວົ້າພາສາລາວຄືກັນ.', 'ພາສາລາວເປັນແມ່ຂອງຄົນເຊື້ອຊາດລາວທັງຢູ່ພາຍໃນແລະຕ່າງປະເທດ ທັງເປັນພາສາກາງຂອງພົນລະເມືອງໃນປະເທດລາວທີ່ມີພາສາອື່ນອີກຫຼາຍພາສາ ເຊິ່ງບາງພາສາບໍ່ມີຄວາມກ່ຽວຂ້ອງກັບພາສານີ້[3] .']
    elif lang == 'mal':
        assert sentences == ['ഇന്ത്യയിൽ കേരള സംസ്ഥാനത്തിലും കേന്ദ്രഭരണപ്രദേശങ്ങളായ ലക്ഷദ്വീപിലും പോണ്ടിച്ചേരിയുടെ ഭാഗമായ മാഹിയിലും തമിഴ്നാട്ടിലെ കന്യാകുമാരി ജില്ലയിലും നീലഗിരി ജില്ലയിലെ ഗൂഡല്ലൂർ താലൂക്കിലും സംസാരിക്കപ്പെടുന്ന ഭാഷയാണ് മലയാളം.', 'ഇതു ദ്രാവിഡ ഭാഷാ കുടുംബത്തിൽപ്പെടുന്നു.', 'ഇന്ത്യയിൽ ശ്രേഷ്ഠഭാഷാ പദവി ലഭിക്കുന്ന അഞ്ചാമത്തെ ഭാഷയാണ് മലയാളം[5].', '2013 മെയ് 23-നു ചേർന്ന കേന്ദ്രമന്ത്രിസഭായോഗമാണ് മലയാളത്തെ ശ്രേഷ്ഠഭാഷയായി അംഗീകരിച്ചത്.', 'ക്ലാസിക്കൽ ലാംഗ്വേജ് എന്ന പദവിയാണ് ലൽകിയത്.', 'അതിനു മലയാളത്തിൽ നൽകിയ വിവർത്തനം ആണ് ശ്രേഷ്ഠഭാഷ എന്നത്.', 'വാസ്തവത്തിൽ ഇത് അത്രശരിയായ വിവർത്തനമോ ശരിയായ പ്രയോഗമോ അല്ല.', 'ശ്രേഷ്ഠം മോശം എന്ന നിലയിൽ ഭാഷകളെ വിലയിരുത്തുന്നത് ശാസ്ത്രീയമായ കാര്യമല്ല.', 'ഭാഷകളിൽ ശ്രേഷ്ഠമെന്നും അല്ലാത്തത് എന്നുമുള്ള വിഭജനം ഇല്ല.', 'ഇന്ത്യൻ ഭരണഘടനയിലെ എട്ടാം ഷെഡ്യൂളിൽ ഉൾപ്പെടുത്തിയിരിക്കുന്ന ഇന്ത്യയിലെ ഇരുപത്തിരണ്ട് ഔദ്യോഗിക ഭാഷകളിൽ ഒന്നാണ് മലയാളം[6].', 'മലയാള ഭാഷ കൈരളി,മലനാട് ഭാഷ എന്നും അറിയപ്പെടുന്നു.കേരള സംസ്ഥാനത്തിലെ ഭരണഭാഷയും കൂടിയാണ്\u200c മലയാളം.', 'കേരളത്തിനും ലക്ഷദ്വീപിനും പുറമേ തമിഴ്നാട്ടിലെ ചില ഭാഗങ്ങളിലും കന്യാകുമാരി ജില്ല, നീലഗിരി ജില്ല കർണാടകയുടെ ദക്ഷിണ കന്നഡ ജില്ല, കൊടഗ് ഭാഗങ്ങളിലും ഗൾഫ് രാജ്യങ്ങൾ, സിംഗപ്പൂർ, മലേഷ്യ എന്നിവിടങ്ങളിലെ കേരളീയ പൈതൃകമുള്ള അനേകം ജനങ്ങളും മലയാളം ഉപയോഗിച്ചുപോരുന്നു.ദേശീയ ഭാഷയായി ഉൾപ്പെടുത്തിയത് മറ്റ് 21 ഭാഷകളുടേതുപോലെ തനതായ വ്യക്തിത്വം ഉള്ളതിനാലാണ്.', 'മലയാള ഭാഷയുടെ ഉല്പത്തിയും പ്രാചീനതയും സംബന്ധിച്ച കാര്യങ്ങൾ ഇന്നും അവ്യക്തമാണ്.', 'പഴയ തമിഴിനും മുൻപത്തെ മൂലദ്രാവിഡമാണ് മലയാളത്തിന്റെ ആദ്യ രൂപം എന്നു കരുതുന്നു.യു.എ.ഇ-യിലെ നാല് ഔദ്യോഗിക ഭാഷകളിൽ ഒന്നു മലയാളമാണ്.', '[അവലംബം ആവശ്യമാണ്]']
    elif lang == 'nob':
        assert sentences == ['Bokmål er en varietet av norsk skriftspråk.', 'Bokmål er en av to offisielle målformer av norsk skriftspråk, hvorav den andre er nynorsk.', 'I skrift har 87,3% bokmål som hovedmål i skolen.', '[1] Etter skriftreformene av riksmål i 1987 og bokmål i 1981 og 2005 er det lite som skiller bokmål og riksmål i alminnelig bruk.']
    elif lang == 'nno':
        assert sentences == ['Nynorsk, før 1929 offisielt kalla landsmål, er sidan jamstillingsvedtaket av 12. mai 1885 ei av dei to offisielle målformene av norsk; den andre forma er bokmål.', 'Nynorsk vert i dag nytta av om lag 10–15% av innbyggjarane i Noreg.', '[1][2] Skriftspråket er basert på nynorsk talemål, det vil seie dei moderne norske dialektane til skilnad frå gamalnorsk og mellomnorsk.', 'Når ein seier at nokon snakkar nynorsk, meiner ein helst at dei snakkar nynorsk normaltalemål.', 'Dei færraste dialekttalande nordmenn seier at dei snakkar nynorsk, men det er ikkje uvanleg i kjerneområda til nynorsken.', 'Dette tilhøvet mellom tale og skrift ligg bak målrørsla sitt slagord sidan 1970-talet: «Snakk dialekt – skriv nynorsk!» Nynorske dialektar vart snakka over heile landet, men det er berre på Vestlandet utanom dei største byene og i dei austlandske fjellbygdene at skriftspråket står sterkt.', 'Det vil seie at dei fleste dialekttalarane har bokmål som det primære skriftspråket sitt.']
    elif lang == 'pol':
        assert sentences == ['Język polski, polszczyzna – język z grupy zachodniosłowiańskiej (do której należą również czeski, kaszubski, słowacki i języki łużyckie), stanowiącej część rodziny indoeuropejskiej.', 'Jest językiem urzędowym w Polsce oraz należy do oficjalnych języków Unii Europejskiej.']
    elif lang.startswith('por_'):
        assert sentences == ['A língua portuguesa, também designada português, é uma língua indo-europeia românica flexiva ocidental originada no galego-português falado no Reino da Galiza e no norte de Portugal.', 'Com a criação do Reino de Portugal em 1139 e a expansão para o sul na sequência da Reconquista, deu-se a difusão da língua pelas terras conquistadas e mais tarde, com as descobertas portuguesas, para o Brasil, África e outras partes do mundo.', '[8] O português foi usado, naquela época, não somente nas cidades conquistadas pelos portugueses, mas também por muitos governantes locais nos seus contatos com outros estrangeiros poderosos.', 'Especialmente nessa altura a língua portuguesa também influenciou várias línguas.', '[9]']
    elif lang == 'rus':
        assert sentences == ['Ру́сский язы́к ([ˈruskʲɪi̯ jɪˈzɨk] Информация о файле слушать)[~ 3][⇨] — язык восточнославянской группы славянской ветви индоевропейской языковой семьи, национальный язык русского народа.', 'Является одним из наиболее распространённых языков мира — восьмым среди всех языков мира по общей численности говорящих[5] и седьмым по численности владеющих им как родным (2022)[2].', 'Русский является также самым распространённым славянским языком[8] и самым распространённым языком в Европе — географически и по числу носителей языка как родного[6].']
    elif lang == 'slv':
        assert sentences == ['Slovenščina [sloˈʋenʃtʃina] je združeni naziv za uradni knjižni jezik Slovencev in skupno ime za narečja in govore, ki jih govorijo ali so jih nekoč govorili Slovenci.', 'Govori ga okoli 2,5 (dva in pol) milijona govorcev po svetu, od katerih jih večina živi v Sloveniji.', 'Glede na število govorcev ima razmeroma veliko narečij.', 'Slovenščina je zahodni južnoslovanski jezik in eden redkih indoevropskih jezikov, ki je ohranil dvojino.', 'Za zapisovanje slovenskega jezika se danes uporablja gajica, pisava imenovana po Ljudevitu Gaju, ki jo je priredil po češkem črkopisu.', 'Slovenska gajica se imenuje slovenica.', 'Pišemo jo od marčne revolucije 1848.', 'Do takrat smo uporabljali bohoričico.']
    elif lang == 'spa':
        assert sentences == ['El español o castellano es una lengua romance procedente del latín hablado, perteneciente a la familia de lenguas indoeuropeas.', 'Forma parte del grupo ibérico y es originaria de Castilla, reino medieval de la península ibérica.', 'Se conoce también informalmente como castillan.', '1\u200b32\u200b33\u200b en algunas áreas rurales e indígenas de América,34\u200b pues el español se empezó a enseñar poco después de la incorporación de los nuevos territorios a la Corona de Castilla.35\u200b36\u200b37\u200b38\u200b39\u200b40\u200b']
    elif lang == 'swe':
        assert sentences == ['Svenska (svenska\u2009(info)) är ett östnordiskt språk som talas av ungefär tio miljoner personer främst i Sverige där språket har en dominant ställning som huvudspråk, men även som det ena nationalspråket i Finland och som enda officiella språk på Åland.', 'I övriga Finland talas det som modersmål framförallt i de finlandssvenska kustområdena i Österbotten, Åboland och Nyland.', 'En liten minoritet svenskspråkiga finns även i Estland.', 'Svenska är nära besläktat och i hög grad ömsesidigt begripligt med danska och norska.', 'De andra nordiska språken, isländska och färöiska, är mindre ömsesidigt begripliga med svenska.', 'Liksom de övriga nordiska språken härstammar svenskan från en gren av fornnordiska, vilket var det språk som talades av de germanska folken i Skandinavien.']
    elif lang == 'tha':
        if sentence_tokenizer == 'pythainlp_crfcut':
            assert sentences == ['ภาษาไทย หรือ ภาษาไทยกลาง เป็นภาษาในกลุ่มภาษาไท ซึ่งเป็นกลุ่มย่อยของตระกูลภาษาขร้า-ไท และเป็นภาษาราชการ และภาษาประจำชาติของประเทศไทย[3][4] มีการสันนิษฐานว่าภาษาในตระกูลนี้มีถิ่นกำเนิดจากทางตอนใต้ของประเทศจีน และนักภาษาศาสตร์บางส่วนเสนอว่า ภาษาไทยน่าจะมีความเชื่อมโยงกับตระกูลภาษาออสโตร-เอเชียติก', 'ตระกูลภาษาออสโตรนีเซียน และตระกูลภาษาจีน-ทิเบต']
        elif sentence_tokenizer == 'pythainlp_thaisumcut':
            assert sentences == ['ภาษาไทย', 'หรือ ภาษาไทยกลาง เป็นภาษาในกลุ่มภาษาไท', 'ซึ่งเป็นกลุ่มย่อยของตระกูลภาษาขร้า-ไท และเป็นภาษาราชการ', 'และภาษาประจำชาติของประเทศไทย[3][4] มีการสันนิษฐานว่าภาษาในตระกูลนี้มีถิ่นกำเนิดจากทางตอนใต้ของประเทศจีน', 'และนักภาษาศาสตร์บางส่วนเสนอว่า ภาษาไทยน่าจะมีความเชื่อมโยงกับตระกูลภาษาออสโตร-เอเชียติก ตระกูลภาษาออสโตรนีเซียน และตระกูลภาษาจีน-ทิเบต']
        else:
            tests_lang_util_skipped = True
    elif lang == 'bod':
        assert sentences == ['བོད་ཀྱི་སྐད་ཡིག་ནི་བོད་ཡུལ་དང་ཉེ་འཁོར་གྱི་ས་ཁུལ་བལ་ཡུལ། འབྲུག་དང་འབྲས་ལྗོངས། ལ་དྭགས་ནས་ལྷོ་མོན་རོང་སོགས་སུ་བེད་སྤྱོད་བྱེད་པའི་སྐད་ཡིག་དེ།', 'ད་ཆར་ཡོངས་གྲགས་སུ་བོད་ཀྱི་ཡུལ་གྲུ་སྟོད་སྨད་བར་གསུམ་ལ་ལྟོས་ཏེ་ནང་གསེས་རིགས་གསུམ་དུ་ཕྱེ་བ་སྟེ།', 'སྟོད་དབུས་གཙང་གི་སྐད་དང་། བར་ཁམས་པའི་སྐད་དང་། སྨད་ཨ་མདོའི་སྐད་རྣམས་སོ།', 'བོད་སྐད་ནི་ཧོར་སོག་ལ་སོགས་པ་གྲངས་ཉུང་མི་རིགས་གཞན་པ་ཁག་ཅིག་གིས་བེད་སྤྱོད་གཏོང་བཞིན་ཡོད་པར་མ་ཟད། བལ་ཡུལ་དང་། འབྲས་ལྗོངས། འབྲུག་ཡུལ་། རྒྱ་གར་ཤར་དང་བྱང་རྒྱུད་མངའ་སྡེ་ཁག་གཅིག་བཅས་ཀྱི་རྒྱལ་ཁབ་རྣམས་སུའང་བེད་སྤྱོད་གཏོང་བཞིན་ཡོད།']
    elif lang == 'tur':
        assert sentences == ["Türkçe ya da Türk dili, Güneydoğu Avrupa ve Batı Asya'da konuşulan, Türk dilleri dil ailesine ait sondan eklemeli bir dil.", '[12] Türk dilleri ailesinin Oğuz dilleri grubundan bir Batı Oğuz dili olan Osmanlı Türkçesinin devamını oluşturur.', "Dil, başta Türkiye olmak üzere Balkanlar, Ege Adaları, Kıbrıs ve Orta Doğu'yu kapsayan eski Osmanlı İmparatorluğu coğrafyasında konuşulur.", "[12] Ethnologue'a göre Türkçe, yaklaşık 83 milyon konuşuru ile dünyada en çok konuşulan 16.", 'dildir.', "[13] Türkçe Türkiye, Kıbrıs Cumhuriyeti ve Kuzey Kıbrıs'ta ulusal resmî dil statüsüne sahiptir.", '[12]']
    elif lang == 'vie':
        assert sentences == ['Tiếng Việt, cũng gọi là tiếng Việt Nam[9] hay Việt ngữ là ngôn ngữ của người Việt và là ngôn ngữ chính thức tại Việt Nam.', 'Đây là tiếng mẹ đẻ của khoảng 85% dân cư Việt Nam cùng với hơn 4 triệu người Việt kiều.', 'Tiếng Việt còn là ngôn ngữ thứ hai của các dân tộc thiểu số tại Việt Nam và là ngôn ngữ dân tộc thiểu số được công nhận tại Cộng hòa Séc.']
    else:
        raise wl_test_init.Wl_Exception_Tests_Lang_Skipped(lang)

    if tests_lang_util_skipped:
        raise wl_test_init.Wl_Exception_Tests_Lang_Util_Skipped(sentence_tokenizer)

@pytest.mark.parametrize('lang', test_langs_local)
def test_sentence_split(lang):
    print(f'Testing {lang} / Sentence Splitter...')

    sentences_split = wl_sentence_tokenization.wl_sentence_split(
        main,
        text = ''.join(getattr(wl_test_lang_examples, f'TEXT_{lang.upper()}'))
    )

    if lang not in ['tha', 'bod']:
        assert len(sentences_split) > 1

@pytest.mark.parametrize('lang', test_langs_local)
def test_sentence_seg_tokenize(lang):
    sentence_segs = wl_sentence_tokenization.wl_sentence_seg_tokenize(
        main,
        text = ''.join(getattr(wl_test_lang_examples, f'TEXT_{lang.upper()}'))
    )

    print(f'{lang} / Sentence Segment Tokenizer:')
    print(f'{sentence_segs}\n')

    if lang not in ['tha']:
        assert len(sentence_segs) > 1

    if lang == 'ces':
        assert sentence_segs == ['Čeština neboli český jazyk je západoslovanský jazyk,', 'nejbližší slovenštině,', 'poté lužické srbštině a polštině.', 'Patří mezi slovanské jazyky,', 'do rodiny jazyků indoevropských.', 'Čeština se vyvinula ze západních nářečí praslovanštiny na konci 10.', 'století.', 'Je částečně ovlivněná latinou a němčinou.', 'Česky psaná literatura se objevuje od 14.', 'století.', 'První písemné památky jsou však již z 12.', 'století.']
    elif lang == 'dan':
        assert sentence_segs == ['Dansk er et østnordisk sprog indenfor den germanske gren af den indoeuropæiske sprogfamilie.', 'Det danske sprog tales af ca.', 'seks millioner mennesker,', 'hovedsageligt i Danmark,', 'men også i Sydslesvig (i Flensborg ca.', '20 %),', 'på Færøerne og Grønland.', '[1] Dansk er tæt beslægtet med norsk,', 'svensk og islandsk,', 'og sproghistorisk har dansk været stærkt påvirket af plattysk.']
    elif lang == 'nld':
        assert sentence_segs == ['Het Nederlands is een West-Germaanse taal,', 'de meest gebruikte taal in Nederland en België,', 'de officiële taal van Suriname en een van de drie officiële talen van België.', 'Binnen het Koninkrijk der Nederlanden is het Nederlands ook een officiële taal van Aruba,', 'Curaçao en Sint-Maarten.', 'Het Nederlands is na Engels en Duits de meest gesproken Germaanse taal.']
    elif lang.startswith('eng_') or lang == 'other':
        assert sentence_segs == ['English is a West Germanic language in the Indo-European language family that originated in early medieval England.', '[3][4][5] It is the most spoken language in the world[6] and the third most spoken native language in the world,', 'after Standard Chinese and Spanish.', '[7] Today,', 'English is the primary language of the Anglosphere,', 'which is usually defined as the United States,', 'the United Kingdom,', 'Canada,', 'Australia,', 'and New Zealand.', 'English is also the primary language of the Republic of Ireland,', 'although it is not typically included within the Anglosphere.']
    elif lang == 'est':
        assert sentence_segs == ['Eesti keelel on kaks suuremat murderühma (põhjaeesti ja lõunaeesti),', 'mõnes käsitluses eristatakse ka kirderanniku murdeid eraldi murderühmana.', 'Liikumisvõimaluste laienemine ning põhjaeesti keskmurde alusel loodud normitud eesti kirjakeele kasutus on põhjustanud murdeerinevuste taandumise.']
    elif lang == 'fin':
        assert sentence_segs == ['Suomen kieli eli suomi on uralilaisten kielten itämerensuomalaiseen ryhmään kuuluva kieli,', 'jota puhuvat pääosin suomalaiset.', 'Suomessa suomen kieltä puhuu äidinkielenään 4,', '8 miljoonaa ja toisena kielenään 0,', '5 miljoonaa ihmistä.', 'Suurimmat suomea puhuvat vähemmistöt ovat Ruotsissa,', 'Norjassa ja Venäjällä.']
    elif lang == 'fra':
        assert sentence_segs == ['Le français est une langue indo-européenne de la famille des langues romanes dont les locuteurs sont appelés francophones.', 'Elle est parfois surnommée la langue de Molière.']
    elif lang.startswith('deu_'):
        assert sentence_segs == ['Das Deutsche ist eine plurizentrische Sprache,', 'enthält also mehrere Standardvarietäten in verschiedenen Regionen.', 'Ihr Sprachgebiet umfasst Deutschland,', 'Österreich,', 'die Deutschschweiz,', 'Liechtenstein,', 'Luxemburg,', 'Ostbelgien,', 'Südtirol,', 'das Elsass und Lothringen sowie Nordschleswig.', 'Außerdem ist Deutsch eine Minderheitensprache in einigen europäischen und außereuropäischen Ländern,', 'z.', 'B.', 'in Rumänien und Südafrika sowie Nationalsprache im afrikanischen Namibia.', 'Deutsch ist die meistgesprochene Muttersprache in der Europäischen Union (EU).', '[26]']
    elif lang == 'ell':
        assert sentence_segs == ['Η ελληνική γλώσσα ανήκει στην ινδοευρωπαϊκή οικογένεια[9] και αποτελεί το μοναδικό μέλος του ελληνικού κλάδου,', 'ενώ είναι η επίσημη γλώσσα της Ελλάδας και της Κύπρου.', 'Ανήκει επίσης στο βαλκανικό γλωσσικό δεσμό.', 'Στην ελληνική γλώσσα,', 'έχουμε γραπτά κείμενα ήδη από τον 15ο αιώνα π.', 'Χ..', 'Σαν Παγκόσμια Ημέρα Ελληνικής Γλώσσας,', 'κάθε έτος,', 'έχει καθιερωθεί η 9η Φεβρουαρίου.', 'Έχει την μακροβιότερη καταγεγραμμένη ιστορία από οποιαδήποτε άλλη ζωντανή ινδοευρωπαϊκή γλώσσα με τουλάχιστον 3.', '400 χρόνια γραπτής ιστορίας.', '[10] Γράφεται με το ελληνικό αλφάβητο,', 'το οποίο χρησιμοποιείται αδιάκοπα (αρχικά με τοπικές παραλλαγές,', 'μετέπειτα υπό μια,', 'ενιαία μορφή) εδώ και περίπου 2.', '600 χρόνια.', '[11][12] Προηγουμένως η ελληνική γλώσσα γραφόταν με τη Γραμμική Β και το κυπριακό συλλαβάριο.', '[13] Το ελληνικό αλφάβητο προέρχεται από το φοινικικό αλφάβητο,', 'με κάποιες προσαρμογές.', 'Στο ελληνικό αλφάβητο βασίζεται το λατινικό,', 'το κυριλλικό,', 'το αρμενικό,', 'το κοπτικό,', 'το γοτθικό και πολλά άλλα αλφάβητα.']
    elif lang == 'ita':
        assert sentence_segs == ["L'italiano ([itaˈljaːno][Nota 1] ascolta[?", '·info]) è una lingua romanza parlata principalmente in Italia.', 'Per ragioni storiche e geografiche,', "l'italiano è la lingua romanza meno divergente dal latino.", '[2][3][4][Nota 2]']
    elif lang == 'khm':
        assert sentence_segs == ['ភាសាខ្មែរ គឺជាភាសាកំណើតរបស់ជនជាតិខ្មែរនិងជាភាសាផ្លូវការរបស់ប្រទេសកម្ពុជា។', 'ភាសាសំស្ក្រឹតនិងភាសាបាលីបាន\u200bជួយបង្កើតខេមរភាសា ព្រោះភាសាខ្មែរបានខ្ចីពាក្យច្រើនពីភាសាទាំងពីរនេះ។', '\u200bមានអក្សរក្រមវែងជាងគេនៅលើពិភពលោក ។', '\u200b វាជាភាសាមួយដ៏ចំណាស់\u200b ដែលប្រហែលជាមានដើមកំណើតតាំងតែពី\u200b២០០០ឆ្នាំមុនមកម៉្លេះ។']
    elif lang == 'lao':
        assert sentence_segs == ['ພາສາລາວ (Lao:', 'ລາວ,', '[láːw] ຫຼື ພາສາລາວ,', '[pʰáːsǎːláːw]) ເປັນພາສາຕະກູນໄທ-ກະໄດຂອງຄົນລາວ ໂດຍມີຄົນເວົ້າໃນປະເທດລາວ ເຊິ່ງເປັນພາສາລັດຖະການຂອງສາທາລະນະລັດ ປະຊາທິປະໄຕ ປະຊາຊົນລາວ ຂອງປະຊາກອນປະມານ 7 ລ້ານຄົນ ແລະໃນພື້ນທີ່ພາກຕາເວັນອອກສຽງເໜືອຂອງປະເທດໄທທີ່ມີຄົນເວົ້າປະມານ 23 ລ້ານຄົນ ທາງລັດຖະບານປະເທດໄທມີການສະໜັບສະໜຸນໃຫ້ເອີ້ນພາສາລາວຖິ່ນໄທວ່າ ພາສາລາວຖິ່ນອີສານ ນອກຈາກນີ້,', 'ຢູ່ທາງພາກຕາເວັນອອກສຽງເໜືອຂອງປະເທດກຳປູເຈຍກໍມີຄົນເວົ້າພາສາລາວຄືກັນ.', 'ພາສາລາວເປັນແມ່ຂອງຄົນເຊື້ອຊາດລາວທັງຢູ່ພາຍໃນແລະຕ່າງປະເທດ ທັງເປັນພາສາກາງຂອງພົນລະເມືອງໃນປະເທດລາວທີ່ມີພາສາອື່ນອີກຫຼາຍພາສາ ເຊິ່ງບາງພາສາບໍ່ມີຄວາມກ່ຽວຂ້ອງກັບພາສານີ້[3] .']
    elif lang == 'mal':
        assert sentence_segs == ['ഇന്ത്യയിൽ കേരള സംസ്ഥാനത്തിലും കേന്ദ്രഭരണപ്രദേശങ്ങളായ ലക്ഷദ്വീപിലും പോണ്ടിച്ചേരിയുടെ ഭാഗമായ മാഹിയിലും തമിഴ്നാട്ടിലെ കന്യാകുമാരി ജില്ലയിലും നീലഗിരി ജില്ലയിലെ ഗൂഡല്ലൂർ താലൂക്കിലും സംസാരിക്കപ്പെടുന്ന ഭാഷയാണ് മലയാളം.', 'ഇതു ദ്രാവിഡ ഭാഷാ കുടുംബത്തിൽപ്പെടുന്നു.', 'ഇന്ത്യയിൽ ശ്രേഷ്ഠഭാഷാ പദവി ലഭിക്കുന്ന അഞ്ചാമത്തെ ഭാഷയാണ് മലയാളം[5].', '2013 മെയ് 23-നു ചേർന്ന കേന്ദ്രമന്ത്രിസഭായോഗമാണ് മലയാളത്തെ ശ്രേഷ്ഠഭാഷയായി അംഗീകരിച്ചത്.', 'ക്ലാസിക്കൽ ലാംഗ്വേജ് എന്ന പദവിയാണ് ലൽകിയത്.', 'അതിനു മലയാളത്തിൽ നൽകിയ വിവർത്തനം ആണ് ശ്രേഷ്ഠഭാഷ എന്നത്.', 'വാസ്തവത്തിൽ ഇത് അത്രശരിയായ വിവർത്തനമോ ശരിയായ പ്രയോഗമോ അല്ല.', 'ശ്രേഷ്ഠം മോശം എന്ന നിലയിൽ ഭാഷകളെ വിലയിരുത്തുന്നത് ശാസ്ത്രീയമായ കാര്യമല്ല.', 'ഭാഷകളിൽ ശ്രേഷ്ഠമെന്നും അല്ലാത്തത് എന്നുമുള്ള വിഭജനം ഇല്ല.', 'ഇന്ത്യൻ ഭരണഘടനയിലെ എട്ടാം ഷെഡ്യൂളിൽ ഉൾപ്പെടുത്തിയിരിക്കുന്ന ഇന്ത്യയിലെ ഇരുപത്തിരണ്ട് ഔദ്യോഗിക ഭാഷകളിൽ ഒന്നാണ് മലയാളം[6].', 'മലയാള ഭാഷ കൈരളി,', 'മലനാട് ഭാഷ എന്നും അറിയപ്പെടുന്നു.', 'കേരള സംസ്ഥാനത്തിലെ ഭരണഭാഷയും കൂടിയാണ്\u200c മലയാളം.', 'കേരളത്തിനും ലക്ഷദ്വീപിനും പുറമേ തമിഴ്നാട്ടിലെ ചില ഭാഗങ്ങളിലും കന്യാകുമാരി ജില്ല,', 'നീലഗിരി ജില്ല കർണാടകയുടെ ദക്ഷിണ കന്നഡ ജില്ല,', 'കൊടഗ് ഭാഗങ്ങളിലും ഗൾഫ് രാജ്യങ്ങൾ,', 'സിംഗപ്പൂർ,', 'മലേഷ്യ എന്നിവിടങ്ങളിലെ കേരളീയ പൈതൃകമുള്ള അനേകം ജനങ്ങളും മലയാളം ഉപയോഗിച്ചുപോരുന്നു.', 'ദേശീയ ഭാഷയായി ഉൾപ്പെടുത്തിയത് മറ്റ് 21 ഭാഷകളുടേതുപോലെ തനതായ വ്യക്തിത്വം ഉള്ളതിനാലാണ്.', 'മലയാള ഭാഷയുടെ ഉല്പത്തിയും പ്രാചീനതയും സംബന്ധിച്ച കാര്യങ്ങൾ ഇന്നും അവ്യക്തമാണ്.', 'പഴയ തമിഴിനും മുൻപത്തെ മൂലദ്രാവിഡമാണ് മലയാളത്തിന്റെ ആദ്യ രൂപം എന്നു കരുതുന്നു.', 'യു.', 'എ.', 'ഇ-യിലെ നാല് ഔദ്യോഗിക ഭാഷകളിൽ ഒന്നു മലയാളമാണ്.', '[അവലംബം ആവശ്യമാണ്]']
    elif lang == 'nob':
        assert sentence_segs == ['Bokmål er en varietet av norsk skriftspråk.', 'Bokmål er en av to offisielle målformer av norsk skriftspråk,', 'hvorav den andre er nynorsk.', 'I skrift har 87,', '3% bokmål som hovedmål i skolen.', '[1] Etter skriftreformene av riksmål i 1987 og bokmål i 1981 og 2005 er det lite som skiller bokmål og riksmål i alminnelig bruk.']
    elif lang == 'nno':
        assert sentence_segs == ['Nynorsk,', 'før 1929 offisielt kalla landsmål,', 'er sidan jamstillingsvedtaket av 12.', 'mai 1885 ei av dei to offisielle målformene av norsk;', 'den andre forma er bokmål.', 'Nynorsk vert i dag nytta av om lag 10–15% av innbyggjarane i Noreg.', '[1][2] Skriftspråket er basert på nynorsk talemål,', 'det vil seie dei moderne norske dialektane til skilnad frå gamalnorsk og mellomnorsk.', 'Når ein seier at nokon snakkar nynorsk,', 'meiner ein helst at dei snakkar nynorsk normaltalemål.', 'Dei færraste dialekttalande nordmenn seier at dei snakkar nynorsk,', 'men det er ikkje uvanleg i kjerneområda til nynorsken.', 'Dette tilhøvet mellom tale og skrift ligg bak målrørsla sitt slagord sidan 1970-talet:', '«Snakk dialekt – skriv nynorsk!', '» Nynorske dialektar vart snakka over heile landet,', 'men det er berre på Vestlandet utanom dei største byene og i dei austlandske fjellbygdene at skriftspråket står sterkt.', 'Det vil seie at dei fleste dialekttalarane har bokmål som det primære skriftspråket sitt.']
    elif lang == 'pol':
        assert sentence_segs == ['Język polski,', 'polszczyzna – język z grupy zachodniosłowiańskiej (do której należą również czeski,', 'kaszubski,', 'słowacki i języki łużyckie),', 'stanowiącej część rodziny indoeuropejskiej.', 'Jest językiem urzędowym w Polsce oraz należy do oficjalnych języków Unii Europejskiej.']
    elif lang.startswith('por_'):
        assert sentence_segs == ['A língua portuguesa,', 'também designada português,', 'é uma língua indo-europeia românica flexiva ocidental originada no galego-português falado no Reino da Galiza e no norte de Portugal.', 'Com a criação do Reino de Portugal em 1139 e a expansão para o sul na sequência da Reconquista,', 'deu-se a difusão da língua pelas terras conquistadas e mais tarde,', 'com as descobertas portuguesas,', 'para o Brasil,', 'África e outras partes do mundo.', '[8] O português foi usado,', 'naquela época,', 'não somente nas cidades conquistadas pelos portugueses,', 'mas também por muitos governantes locais nos seus contatos com outros estrangeiros poderosos.', 'Especialmente nessa altura a língua portuguesa também influenciou várias línguas.', '[9]']
    elif lang == 'rus':
        assert sentence_segs == ['Ру́сский язы́к ([ˈruskʲɪi̯ jɪˈzɨk] Информация о файле слушать)[~ 3][⇨] — язык восточнославянской группы славянской ветви индоевропейской языковой семьи,', 'национальный язык русского народа.', 'Является одним из наиболее распространённых языков мира — восьмым среди всех языков мира по общей численности говорящих[5] и седьмым по численности владеющих им как родным (2022)[2].', 'Русский является также самым распространённым славянским языком[8] и самым распространённым языком в Европе — географически и по числу носителей языка как родного[6].']
    elif lang == 'slv':
        assert sentence_segs == ['Slovenščina [sloˈʋenʃtʃina] je združeni naziv za uradni knjižni jezik Slovencev in skupno ime za narečja in govore,', 'ki jih govorijo ali so jih nekoč govorili Slovenci.', 'Govori ga okoli 2,', '5 (dva in pol) milijona govorcev po svetu,', 'od katerih jih večina živi v Sloveniji.', 'Glede na število govorcev ima razmeroma veliko narečij.', 'Slovenščina je zahodni južnoslovanski jezik in eden redkih indoevropskih jezikov,', 'ki je ohranil dvojino.', 'Za zapisovanje slovenskega jezika se danes uporablja gajica,', 'pisava imenovana po Ljudevitu Gaju,', 'ki jo je priredil po češkem črkopisu.', 'Slovenska gajica se imenuje slovenica.', 'Pišemo jo od marčne revolucije 1848.', 'Do takrat smo uporabljali bohoričico.']
    elif lang == 'spa':
        assert sentence_segs == ['El español o castellano es una lengua romance procedente del latín hablado,', 'perteneciente a la familia de lenguas indoeuropeas.', 'Forma parte del grupo ibérico y es originaria de Castilla,', 'reino medieval de la península ibérica.', 'Se conoce también informalmente como castillan.', '1\u200b32\u200b33\u200b en algunas áreas rurales e indígenas de América,', '34\u200b pues el español se empezó a enseñar poco después de la incorporación de los nuevos territorios a la Corona de Castilla.', '35\u200b36\u200b37\u200b38\u200b39\u200b40\u200b']
    elif lang == 'swe':
        assert sentence_segs == ['Svenska (svenska\u2009(info)) är ett östnordiskt språk som talas av ungefär tio miljoner personer främst i Sverige där språket har en dominant ställning som huvudspråk,', 'men även som det ena nationalspråket i Finland och som enda officiella språk på Åland.', 'I övriga Finland talas det som modersmål framförallt i de finlandssvenska kustområdena i Österbotten,', 'Åboland och Nyland.', 'En liten minoritet svenskspråkiga finns även i Estland.', 'Svenska är nära besläktat och i hög grad ömsesidigt begripligt med danska och norska.', 'De andra nordiska språken,', 'isländska och färöiska,', 'är mindre ömsesidigt begripliga med svenska.', 'Liksom de övriga nordiska språken härstammar svenskan från en gren av fornnordiska,', 'vilket var det språk som talades av de germanska folken i Skandinavien.']
    elif lang == 'tha':
        assert sentence_segs == ['ภาษาไทย หรือ ภาษาไทยกลาง เป็นภาษาในกลุ่มภาษาไท ซึ่งเป็นกลุ่มย่อยของตระกูลภาษาขร้า-ไท และเป็นภาษาราชการ และภาษาประจำชาติของประเทศไทย[3][4] มีการสันนิษฐานว่าภาษาในตระกูลนี้มีถิ่นกำเนิดจากทางตอนใต้ของประเทศจีน และนักภาษาศาสตร์บางส่วนเสนอว่า ภาษาไทยน่าจะมีความเชื่อมโยงกับตระกูลภาษาออสโตร-เอเชียติก ตระกูลภาษาออสโตรนีเซียน และตระกูลภาษาจีน-ทิเบต']
    elif lang == 'bod':
        assert sentence_segs == ['བོད་ཀྱི་སྐད་ཡིག་ནི་བོད་ཡུལ་དང་ཉེ་འཁོར་གྱི་ས་ཁུལ་བལ་ཡུལ།', 'འབྲུག་དང་འབྲས་ལྗོངས།', 'ལ་དྭགས་ནས་ལྷོ་མོན་རོང་སོགས་སུ་བེད་སྤྱོད་བྱེད་པའི་སྐད་ཡིག་དེ།', 'ད་ཆར་ཡོངས་གྲགས་སུ་བོད་ཀྱི་ཡུལ་གྲུ་སྟོད་སྨད་བར་གསུམ་ལ་ལྟོས་ཏེ་ནང་གསེས་རིགས་གསུམ་དུ་ཕྱེ་བ་སྟེ།', 'སྟོད་དབུས་གཙང་གི་སྐད་དང་།', 'བར་ཁམས་པའི་སྐད་དང་།', 'སྨད་ཨ་མདོའི་སྐད་རྣམས་སོ།', 'བོད་སྐད་ནི་ཧོར་སོག་ལ་སོགས་པ་གྲངས་ཉུང་མི་རིགས་གཞན་པ་ཁག་ཅིག་གིས་བེད་སྤྱོད་གཏོང་བཞིན་ཡོད་པར་མ་ཟད།', 'བལ་ཡུལ་དང་།', 'འབྲས་ལྗོངས།', 'འབྲུག་ཡུལ་།', 'རྒྱ་གར་ཤར་དང་བྱང་རྒྱུད་མངའ་སྡེ་ཁག་གཅིག་བཅས་ཀྱི་རྒྱལ་ཁབ་རྣམས་སུའང་བེད་སྤྱོད་གཏོང་བཞིན་ཡོད།']
    elif lang == 'tur':
        assert sentence_segs == ['Türkçe ya da Türk dili,', "Güneydoğu Avrupa ve Batı Asya'da konuşulan,", 'Türk dilleri dil ailesine ait sondan eklemeli bir dil.', '[12] Türk dilleri ailesinin Oğuz dilleri grubundan bir Batı Oğuz dili olan Osmanlı Türkçesinin devamını oluşturur.', 'Dil,', 'başta Türkiye olmak üzere Balkanlar,', 'Ege Adaları,', "Kıbrıs ve Orta Doğu'yu kapsayan eski Osmanlı İmparatorluğu coğrafyasında konuşulur.", "[12] Ethnologue'a göre Türkçe,", 'yaklaşık 83 milyon konuşuru ile dünyada en çok konuşulan 16.', 'dildir.', '[13] Türkçe Türkiye,', "Kıbrıs Cumhuriyeti ve Kuzey Kıbrıs'ta ulusal resmî dil statüsüne sahiptir.", '[12]']
    elif lang == 'vie':
        assert sentence_segs == ['Tiếng Việt,', 'cũng gọi là tiếng Việt Nam[9] hay Việt ngữ là ngôn ngữ của người Việt và là ngôn ngữ chính thức tại Việt Nam.', 'Đây là tiếng mẹ đẻ của khoảng 85% dân cư Việt Nam cùng với hơn 4 triệu người Việt kiều.', 'Tiếng Việt còn là ngôn ngữ thứ hai của các dân tộc thiểu số tại Việt Nam và là ngôn ngữ dân tộc thiểu số được công nhận tại Cộng hòa Séc.']
    else:
        raise wl_test_init.Wl_Exception_Tests_Lang_Skipped(lang)

@pytest.mark.parametrize('lang', test_langs_local)
def test_sentence_seg_split(lang):
    print(f'Testing {lang} / Sentence Segment Splitter...')

    sentence_segs = wl_sentence_tokenization.wl_sentence_seg_split(
        main,
        text = ''.join(getattr(wl_test_lang_examples, f'TEXT_{lang.upper()}'))
    )

    if lang not in ['tha']:
        assert len(sentence_segs) > 1

@pytest.mark.parametrize('lang', test_langs)
def test_sentence_seg_tokenize_tokens(lang):
    print(f'Testing {lang} / Sentence Segment Tokenizer with tokens...')

    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = ''.join(getattr(wl_test_lang_examples, f'TEXT_{lang.upper()}')),
        lang = lang
    )
    sentence_segs = wl_sentence_tokenization.wl_sentence_seg_tokenize_tokens(main, tokens)

    if lang not in ['tha']:
        assert len(sentence_segs) > 1

if __name__ == '__main__':
    for lang, sentence_tokenizer in test_sentence_tokenizers_local:
        test_sentence_tokenize(lang, sentence_tokenizer)

    for lang in test_langs_local:
        test_sentence_split(lang)

    for lang in test_langs_local:
        test_sentence_seg_tokenize(lang)

    for lang in test_langs_local:
        test_sentence_seg_split(lang)

    for lang in test_langs_local:
        test_sentence_seg_tokenize_tokens(lang)
