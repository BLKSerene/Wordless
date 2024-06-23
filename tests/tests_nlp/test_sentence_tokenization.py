# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Sentence tokenization
# Copyright (C) 2018-2024  Ye Lei (叶磊)
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
from wordless.wl_nlp import wl_sentence_tokenization
from wordless.wl_utils import wl_misc

_, is_macos, _ = wl_misc.check_os()

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')

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
test_langs_split = list(main.settings_global['sentence_tokenizers'].keys())

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

    match lang:
        case 'xcl':
            assert sentences == ['Զգոյշ լերուք ողորմութեան ձերում՝ մի առնել առաջի մարդկան՝ որպէս թե ի ցոյց ինչ նոցա,', 'գուցէ եւ վարձս ոչ ընդունիցիք ի հաւրէ ձերմէ որ յերկինսն է:', 'Այղ յորժամ առնիցես ողորմութիւն,', 'մի հարկաներ փող առաջի քո.', 'որպէս կեղծաւորքն առնեն ի ժողովուրդս եւ ի հրապարակս.', 'որպէս զի փառաւորեսցին ի մարդկանէ:']
        case 'ces':
            assert sentences == ['Čeština neboli český jazyk je západoslovanský jazyk, nejbližší slovenštině, poté lužické srbštině a polštině.', 'Patří mezi slovanské jazyky, do rodiny jazyků indoevropských.', 'Čeština se vyvinula ze západních nářečí praslovanštiny na konci 10. století.', 'Je částečně ovlivněná latinou a němčinou.', 'Česky psaná literatura se objevuje od 14. století.', 'První písemné památky jsou však již z 12. století.']
        case 'dan':
            assert sentences == ['Dansk er et østnordisk sprog indenfor den germanske gren af den indoeuropæiske sprogfamilie.', 'Det danske sprog tales af ca. seks millioner mennesker, hovedsageligt i Danmark, men også i Sydslesvig, på Færøerne og Grønland.', '[1] Dansk er tæt beslægtet med norsk, svensk og islandsk, og sproghistorisk har dansk været stærkt påvirket af plattysk.']
        case 'nld':
            assert sentences == ['Het Nederlands is een West-Germaanse taal, de meest gebruikte taal in Nederland en België, de officiële taal van Suriname en een van de drie officiële talen van België.', 'Binnen het Koninkrijk der Nederlanden is het Nederlands ook een officiële taal van Aruba, Curaçao en Sint-Maarten.', 'Het Nederlands is na Engels en Duits de meest gesproken Germaanse taal.']
        case 'ang':
            assert sentences == ['Seo ænglisce spræc (Englisc gereord) is Westgermanisc spræc,', 'þe fram Englalande aras.', 'Heo is sibb þæm Ealdfresiscan and þære Ealdseaxiscan spræcum.', 'Hit is gastleas spræc,', 'and ne hæfþ nane gebyrdlice sprecan todæg,', 'ac sume menn leorniaþ hit on Betweoxnette and writaþ on him,', 'swa swa her on þissum Wicipædian.']
        case 'eng_gb' | 'eng_us' | 'other':
            assert sentences == ['English is a West Germanic language in the Indo-European language family.', 'Originating in early medieval England,[3][4][5] today English is both the most spoken language in the world[6] and the third most spoken native language, after Mandarin Chinese and Spanish.', '[7] English is the most widely learned second language and is either the official language or one of the official languages in 59 sovereign states.', 'There are more people who have learned English as a second language than there are native speakers.', 'As of 2005, it was estimated that there were over two billion speakers of English.', '[8]']
        case 'est':
            assert sentences == ['Eesti keelel on kaks suuremat murderühma (põhjaeesti ja lõunaeesti), mõnes käsitluses eristatakse ka kirderanniku murdeid eraldi murderühmana.', 'Liikumisvõimaluste laienemine ning põhjaeesti keskmurde alusel loodud normitud eesti kirjakeele kasutus on põhjustanud murdeerinevuste taandumise.']
        case 'fin':
            assert sentences == ['Suomen kieli eli suomi on uralilaisten kielten itämerensuomalaiseen ryhmään kuuluva kieli, jota puhuvat pääosin suomalaiset.', 'Suomessa suomen kieltä puhuu äidinkielenään 4,8 miljoonaa ja toisena kielenään 0,5 miljoonaa ihmistä.', 'Suurimmat suomea puhuvat vähemmistöt ovat Ruotsissa, Norjassa ja Venäjällä.']
        case 'fra':
            assert sentences == ['Le français est une langue indo-européenne de la famille des langues romanes dont les locuteurs sont appelés francophones.', 'Elle est parfois surnommée la langue de Molière.']
        case 'deu_at' | 'deu_de' | 'deu_ch':
            assert sentences == ['Das Deutsche ist eine plurizentrische Sprache, enthält also mehrere Standardvarietäten in verschiedenen Regionen.', 'Ihr Sprachgebiet umfasst Deutschland, Österreich, die Deutschschweiz, Liechtenstein, Luxemburg, Ostbelgien, Südtirol, das Elsass und Lothringen sowie Nordschleswig.', 'Außerdem ist Deutsch eine Minderheitensprache in einigen europäischen und außereuropäischen Ländern, z.', 'B. in Rumänien und Südafrika sowie Nationalsprache im afrikanischen Namibia.', 'Deutsch ist die meistgesprochene Muttersprache in der Europäischen Union (EU).', '[26]']
        case 'ell':
            assert sentences == ['Η ελληνική γλώσσα ανήκει στην ινδοευρωπαϊκή οικογένεια[9] και αποτελεί το μοναδικό μέλος του ελληνικού κλάδου, ενώ είναι η επίσημη γλώσσα της Ελλάδας και της Κύπρου.', 'Ανήκει επίσης στο βαλκανικό γλωσσικό δεσμό.', 'Στην ελληνική γλώσσα, έχουμε γραπτά κείμενα ήδη από τον 15ο αιώνα π.Χ.. Σαν Παγκόσμια Ημέρα Ελληνικής Γλώσσας, κάθε έτος, έχει καθιερωθεί η 9η Φεβρουαρίου.', 'Έχει την μακροβιότερη καταγεγραμμένη ιστορία από οποιαδήποτε άλλη ζωντανή ινδοευρωπαϊκή γλώσσα με τουλάχιστον 3.400 χρόνια γραπτής ιστορίας.', '[10] Γράφεται με το ελληνικό αλφάβητο, το οποίο χρησιμοποιείται αδιάκοπα (αρχικά με τοπικές παραλλαγές, μετέπειτα υπό μια, ενιαία μορφή) εδώ και περίπου 2.600 χρόνια.', '[11][12] Προηγουμένως η ελληνική γλώσσα γραφόταν με τη Γραμμική Β και το κυπριακό συλλαβάριο.', '[13] Το ελληνικό αλφάβητο προέρχεται από το φοινικικό αλφάβητο, με κάποιες προσαρμογές.', 'Στο ελληνικό αλφάβητο βασίζεται το λατινικό, το κυριλλικό, το αρμενικό, το κοπτικό, το γοτθικό και πολλά άλλα αλφάβητα.']
        case 'ita':
            assert sentences == ["L'italiano ([itaˈljaːno][Nota 1] ascoltaⓘ) è una lingua romanza parlata principalmente in Italia.", "Per ragioni storiche e geografiche, l'italiano è la lingua romanza meno divergente dal latino.", '[2][3][4][Nota 2]']
        case 'khm':
            assert sentences == ['ភាសាខ្មែរ គឺជាភាសាកំណើតរបស់ជនជាតិខ្មែរនិងជាភាសាផ្លូវការរបស់ប្រទេសកម្ពុជា។', 'ភាសាសំស្ក្រឹតនិងភាសាបាលីបាន\u200bជួយបង្កើតខេមរភាសា ព្រោះភាសាខ្មែរបានខ្ចីពាក្យច្រើនពីភាសាទាំងពីរនេះ។', '\u200bមានអក្សរក្រមវែងជាងគេនៅលើពិភពលោក ។', '\u200b វាជាភាសាមួយដ៏ចំណាស់\u200b ដែលប្រហែលជាមានដើមកំណើតតាំងតែពី\u200b២០០០ឆ្នាំមុនមកម៉្លេះ។']
        case 'lao':
            assert sentences == ['ພາສາລາວ (Lao: ລາວ, [láːw] ຫຼື ພາສາລາວ, [pʰáːsǎːláːw]) ເປັນພາສາຕະກູນໄທ-ກະໄດຂອງຄົນລາວ ໂດຍມີຄົນເວົ້າໃນປະເທດລາວ ເຊິ່ງເປັນພາສາລັດຖະການຂອງສາທາລະນະລັດ ປະຊາທິປະໄຕ ປະຊາຊົນລາວ ຂອງປະຊາກອນປະມານ 7 ລ້ານຄົນ ແລະໃນພື້ນທີ່ພາກຕາເວັນອອກສຽງເໜືອຂອງປະເທດໄທທີ່ມີຄົນເວົ້າປະມານ 23 ລ້ານຄົນ ທາງລັດຖະບານປະເທດໄທມີການສະໜັບສະໜຸນໃຫ້ເອີ້ນພາສາລາວຖິ່ນໄທວ່າ ພາສາລາວຖິ່ນອີສານ ນອກຈາກນີ້, ຢູ່ທາງພາກຕາເວັນອອກສຽງເໜືອຂອງປະເທດກຳປູເຈຍກໍມີຄົນເວົ້າພາສາລາວຄືກັນ.', 'ພາສາລາວເປັນແມ່ຂອງຄົນເຊື້ອຊາດລາວທັງຢູ່ພາຍໃນແລະຕ່າງປະເທດ ທັງເປັນພາສາກາງຂອງພົນລະເມືອງໃນປະເທດລາວທີ່ມີພາສາອື່ນອີກຫຼາຍພາສາ ເຊິ່ງບາງພາສາບໍ່ມີຄວາມກ່ຽວຂ້ອງກັບພາສານີ້[3] .']
        case 'mal':
            assert sentences == ['ദ്രാവിഡഭാഷാ കുടുംബത്തിൽ ഉൾപ്പെടുന്ന മലയാളത്തിന് ഇതര ഭാരതീയ ഭാഷകളായ സംസ്കൃതം, തമിഴ് എന്നീ ഉദാത്തഭാഷകളുമായി പ്രകടമായ ബന്ധമുണ്ട്[8].', 'പൂക്കാട്ടിയൂർ ലിഖിതങ്ങൾ 8 ക്രി.മു മുതൽ 3000 ക്രി.മു അടുത്ത് വരെയും പഴക്കം ചെന്നതാണ്.']
        case 'nob':
            assert sentences == ['Bokmål er en av to offisielle målformer av norsk skriftspråk, hvorav den andre er nynorsk.', 'I skrift har 87,3% bokmål som hovedmål i skolen.', '[1] Etter skriftreformene av riksmål i 1987 og bokmål i 1981 og 2005 er det lite som skiller bokmål og riksmål i alminnelig bruk.']
        case 'nno':
            assert sentences == ['Nynorsk, før 1929 offisielt kalla landsmål, er sidan jamstillingsvedtaket av 12. mai 1885 ei av dei to offisielle målformene av norsk; den andre forma er bokmål.', 'Nynorsk vert i dag nytta av om lag 10–15% av innbyggjarane i Noreg.', '[1][2] Skriftspråket er basert på nynorsk talemål, det vil seie dei moderne norske dialektane til skilnad frå gamalnorsk og mellomnorsk.', 'Når ein seier at nokon snakkar nynorsk, meiner ein helst at dei snakkar nynorsk normaltalemål.', 'Dei færraste dialekttalande nordmenn seier at dei snakkar nynorsk, men det er ikkje uvanleg i kjerneområda til nynorsken.', 'Dette tilhøvet mellom tale og skrift ligg bak målrørsla sitt slagord sidan 1970-talet: «Snakk dialekt – skriv nynorsk!» Nynorske dialektar vart snakka over heile landet, men det er berre på Vestlandet utanom dei største byene og i dei austlandske fjellbygdene at skriftspråket står sterkt.', 'Det vil seie at dei fleste dialekttalarane har bokmål som det primære skriftspråket sitt.']
        case 'pol':
            assert sentences == ['Język polski, polszczyzna – język z grupy zachodniosłowiańskiej (do której należą również czeski, kaszubski, słowacki i języki łużyckie), stanowiącej część rodziny indoeuropejskiej.', 'Jest językiem urzędowym w Polsce oraz należy do oficjalnych języków Unii Europejskiej.']
        case 'por_br' | 'por_pt':
            assert sentences == ['A língua portuguesa, também designada português, é uma língua indo-europeia românica flexiva ocidental originada no galego-português falado no Reino da Galiza e no norte de Portugal.', 'Com a criação do Reino de Portugal em 1139 e a expansão para o sul na sequência da Reconquista, deu-se a difusão da língua pelas terras conquistadas e mais tarde, com as descobertas portuguesas, para o Brasil, África e outras partes do mundo.', '[8] O português foi usado, naquela época, não somente nas cidades conquistadas pelos portugueses, mas também por muitos governantes locais nos seus contatos com outros estrangeiros poderosos.', 'Especialmente nessa altura a língua portuguesa também influenciou várias línguas.', '[9]']
        case 'rus':
            assert sentences == ['Ру́сский язы́к (МФА: [ˈruskʲɪi̯ jɪˈzɨk]ⓘ)[~ 3][⇨] — язык восточнославянской группы славянской ветви индоевропейской языковой семьи, национальный язык русского народа.', 'Является одним из наиболее распространённых языков мира — восьмым среди всех языков мира по общей численности говорящих[5] и седьмым по численности владеющих им как родным (2022)[2].', 'Русский является также самым распространённым славянским языком[8] и самым распространённым языком в Европе — географически и по числу носителей языка как родного[6].']
        case 'slv':
            assert sentences == ['Slovenščina [sloˈʋenʃtʃina] je združeni naziv za uradni knjižni jezik Slovencev in skupno ime za narečja in govore, ki jih govorijo ali so jih nekoč govorili Slovenci.', 'Govori ga okoli 2,5 (dva in pol) milijona govorcev po svetu, od katerih jih večina živi v Sloveniji.', 'Glede na število govorcev ima razmeroma veliko narečij.', 'Slovenščina je zahodni južnoslovanski jezik in eden redkih indoevropskih jezikov, ki je ohranil dvojino.', 'Za zapisovanje slovenskega jezika se danes uporablja gajica, pisava imenovana po hrvaškem jezikoslovcu Ljudevitu Gaju, ki jo je priredil po češkem črkopisu.', 'Slovenska gajica se imenuje slovenica.', 'Pišemo jo od marčne revolucije 1848.', 'Do takrat smo uporabljali bohoričico.']
        case 'spa':
            assert sentences == ['El español o castellano es una lengua romance procedente del latín hablado, perteneciente a la familia de lenguas indoeuropeas.', 'Forma parte del grupo ibérico y es originaria de Castilla, reino medieval de la península ibérica.', 'Se conoce también informalmente como castillan.', '1\u200b33\u200b34\u200b en algunas áreas rurales e indígenas de América,35\u200b pues el español se empezó a enseñar poco después de la incorporación de los nuevos territorios a la Corona de Castilla.36\u200b37\u200b38\u200b39\u200b40\u200b41\u200b']
        case 'swe':
            assert sentences == ['Svenska (svenska\u2009(info)) är ett östnordiskt språk som talas av ungefär tio miljoner personer främst i Sverige där språket har en dominant ställning som huvudspråk, men även som det ena nationalspråket i Finland och som enda officiella språk på Åland.', 'I övriga Finland talas det som modersmål framförallt i de finlandssvenska kustområdena i Österbotten, Åboland och Nyland.', 'En liten minoritet svenskspråkiga finns även i Estland.', 'Svenska är nära besläktat och i hög grad ömsesidigt begripligt med danska och norska.', 'De andra nordiska språken, isländska och färöiska, är mindre ömsesidigt begripliga med svenska.', 'Liksom de övriga nordiska språken härstammar svenskan från en gren av fornnordiska, vilket var det språk som talades av de germanska folken i Skandinavien.']
        case 'tha':
            match sentence_tokenizer:
                case 'pythainlp_crfcut':
                    assert sentences == ['ภาษาไทย หรือ ภาษาไทยกลาง เป็นภาษาในกลุ่มภาษาไท ซึ่งเป็นกลุ่มย่อยของตระกูลภาษาขร้า-ไท และเป็นภาษาราชการ และภาษาประจำชาติของประเทศไทย[3][4]', 'มีการสันนิษฐานว่าภาษาในตระกูลนี้มีถิ่นกำเนิดจากทางตอนใต้ของประเทศจีน และนักภาษาศาสตร์บางส่วนเสนอว่า ภาษาไทยน่าจะมีความเชื่อมโยงกับตระกูลภาษาออสโตร-เอเชียติก', 'ตระกูลภาษาออสโตรนีเซียน และตระกูลภาษาจีน-ทิเบต']
                case 'pythainlp_thaisumcut':
                    assert sentences == ['ภาษาไทย', 'หรือ ภาษาไทยกลาง เป็นภาษาในกลุ่มภาษาไท', 'ซึ่งเป็นกลุ่มย่อยของตระกูลภาษาขร้า-ไท และเป็นภาษาราชการ', 'และภาษาประจำชาติของประเทศไทย[3][4] มีการสันนิษฐานว่าภาษาในตระกูลนี้มีถิ่นกำเนิดจากทางตอนใต้ของประเทศจีน', 'และนักภาษาศาสตร์บางส่วนเสนอว่า ภาษาไทยน่าจะมีความเชื่อมโยงกับตระกูลภาษาออสโตร-เอเชียติก ตระกูลภาษาออสโตรนีเซียน และตระกูลภาษาจีน-ทิเบต']
                case _:
                    tests_lang_util_skipped = True
        case 'bod':
            assert sentences == ['བོད་ཀྱི་སྐད་ཡིག་ནི་བོད་ཡུལ་དང་ཉེ་འཁོར་གྱི་ས་ཁུལ་བལ་ཡུལ། འབྲུག་དང་འབྲས་ལྗོངས། ལ་དྭགས་ནས་ལྷོ་མོན་རོང་སོགས་སུ་བེད་སྤྱོད་བྱེད་པའི་སྐད་ཡིག་དེ།', 'ད་ཆར་ཡོངས་གྲགས་སུ་བོད་ཀྱི་ཡུལ་གྲུ་སྟོད་སྨད་བར་གསུམ་ལ་ལྟོས་ཏེ་ནང་གསེས་རིགས་གསུམ་དུ་ཕྱེ་བ་སྟེ།', 'སྟོད་དབུས་གཙང་གི་སྐད་དང་། བར་ཁམས་པའི་སྐད་དང་། སྨད་ཨ་མདོའི་སྐད་རྣམས་སོ།', 'བོད་སྐད་ནི་ཧོར་སོག་ལ་སོགས་པ་གྲངས་ཉུང་མི་རིགས་གཞན་པ་ཁག་ཅིག་གིས་བེད་སྤྱོད་གཏོང་བཞིན་ཡོད་པར་མ་ཟད། བལ་ཡུལ་དང་། འབྲས་ལྗོངས། འབྲུག་ཡུལ་། རྒྱ་གར་ཤར་དང་བྱང་རྒྱུད་མངའ་སྡེ་ཁག་གཅིག་བཅས་ཀྱི་རྒྱལ་ཁབ་རྣམས་སུའང་བེད་སྤྱོད་གཏོང་བཞིན་ཡོད།']
        case 'tur':
            assert sentences == ["Türkçe ya da Türk dili, Güneydoğu Avrupa ve Batı Asya'da konuşulan, Türk dilleri dil ailesine ait sondan eklemeli bir dil.", '[12] Türk dilleri ailesinin Oğuz dilleri grubundan bir Batı Oğuz dili olan Osmanlı Türkçesinin devamını oluşturur.', "Dil, başta Türkiye olmak üzere Balkanlar, Ege Adaları, Kıbrıs ve Orta Doğu'yu kapsayan eski Osmanlı İmparatorluğu coğrafyasında konuşulur.", "[12] Ethnologue'a göre Türkçe, yaklaşık 83 milyon konuşuru ile dünyada en çok konuşulan 16.", 'dildir.', "[13] Türkçe Türkiye, Kıbrıs Cumhuriyeti ve Kuzey Kıbrıs'ta ulusal resmî dil statüsüne sahiptir.", '[12]']
        case 'vie':
            assert sentences == ['Tiếng Việt, cũng gọi là tiếng Việt Nam[9] hay Việt ngữ là ngôn ngữ của người Việt và là ngôn ngữ chính thức tại Việt Nam.', 'Đây là tiếng mẹ đẻ của khoảng 85% dân cư Việt Nam cùng với hơn 4 triệu người Việt kiều.', 'Tiếng Việt còn là ngôn ngữ thứ hai của các dân tộc thiểu số tại Việt Nam và là ngôn ngữ dân tộc thiểu số được công nhận tại Cộng hòa Séc.']
        case _:
            raise wl_test_init.Wl_Exception_Tests_Lang_Skipped(lang)

    if tests_lang_util_skipped:
        raise wl_test_init.Wl_Exception_Tests_Lang_Util_Skipped(sentence_tokenizer)

@pytest.mark.parametrize('lang', test_langs_split)
def test_sentence_split(lang):
    print(f'Testing {lang} / Sentence Splitter...')

    sentences_split = wl_sentence_tokenization.wl_sentence_split(
        main,
        text = ''.join(getattr(wl_test_lang_examples, f'TEXT_{lang.upper()}'))
    )

    if lang not in [
        'lzh', 'zho_cn', 'zho_tw', 'chu', 'cop', 'hbo', 'isl', 'jpn', 'orv', 'srp_latn',
        'tha', 'bod'
    ]:
        assert len(sentences_split) > 1

@pytest.mark.parametrize('lang', test_langs_split)
def test_sentence_seg_tokenize(lang):
    sentence_segs = wl_sentence_tokenization.wl_sentence_seg_tokenize(
        main,
        text = ''.join(getattr(wl_test_lang_examples, f'TEXT_{lang.upper()}'))
    )

    print(f'{lang} / Sentence Segment Tokenizer:')
    print(f'{sentence_segs}\n')

    if lang not in ['chu', 'cop', 'orv', 'tha']:
        assert len(sentence_segs) > 1

    match lang:
        case 'afr':
            assert sentence_segs == ["Afrikaans is tipologies beskou 'n Indo-Europese,", 'Wes-Germaanse,', 'Nederfrankiese taal,', '[2] wat aan die suidpunt van Afrika onder invloed van verskeie ander tale en taalgroepe ontstaan het.', "Afrikaans is op 8 Mei 1925 as 'n amptelike taal van Suid-Afrika erken en is tans die derde jongste Germaanse taal wat amptelike status geniet,", 'naas Faroëes wat in 1948 grondwetlik erken is en Luxemburgs wat hierdie status in 1984 verkry het.']
        case 'ara':
            assert sentence_segs == ['تحتوي اللغة العربية 28 حرفاً مكتوباً.', 'ويرى بعضُ اللغويين أنه يجب إضافة حرف الهمزة إلى حروف العربية،', 'ليصبحَ عدد الحروف 29.', 'تُكتب العربية من اليمين إلى اليسار - ومثلها اللغة الفارسية والعبرية على عكس كثير من اللغات العالمية - ومن أعلى الصفحة إلى أسفلها.']
        case 'xcl':
            assert sentence_segs == ['Զգոյշ լերուք ողորմութեան ձերում՝ մի առնել առաջի մարդկան՝ որպէս թե ի ցոյց ինչ նոցա,', 'գուցէ եւ վարձս ոչ ընդունիցիք ի հաւրէ ձերմէ որ յերկինսն է:', 'Այղ յորժամ առնիցես ողորմութիւն,', 'մի հարկաներ փող առաջի քո.', 'որպէս կեղծաւորքն առնեն ի ժողովուրդս եւ ի հրապարակս.', 'որպէս զի փառաւորեսցին ի մարդկանէ:']
        case 'hye':
            assert sentence_segs == ['Հայոց լեզվով ստեղծվել է մեծ գրականություն։', 'Գրաբարով է ավանդված հայ հին պատմագրությունը,', 'գիտափիլիսոփայական,', 'մաթեմատիկական,', 'բժշկագիտական,', 'աստվածաբանական-դավանաբանական գրականությունը։', 'Միջին գրական հայերենով են մեզ հասել միջնադարյան հայ քնարերգության գլուխգործոցները,', 'բժշկագիտական,', 'իրավագիտական նշանակալի աշխատություններ։', 'Գրական նոր հայերենի արևելահայերեն ու արևմտահայերեն գրական տարբերակներով ստեղծվել է գեղարվեստական,', 'հրապարակախոսական ու գիտական բազմատիպ ու բազմաբնույթ հարուստ գրականություն։']
        case 'hyw':
            assert sentence_segs == ['Հայոց լեզվով ստեղծվել է մեծ գրականություն։', 'Գրաբարով է ավանդված հայ հին պատմագրությունը,', 'գիտափիլիսոփայական,', 'մաթեմատիկական,', 'բժշկագիտական,', 'աստվածաբանական-դավանաբանական գրականությունը։', 'Միջին գրական հայերենով են մեզ հասել միջնադարյան հայ քնարերգության գլուխգործոցները,', 'բժշկագիտական,', 'իրավագիտական նշանակալի աշխատություններ։', 'Գրական նոր հայերենի արևելահայերեն ու արևմտահայերեն գրական տարբերակներով ստեղծվել է գեղարվեստական,', 'հրապարակախոսական ու գիտական բազմատիպ ու բազմաբնույթ հարուստ գրականություն։']
        case 'eus':
            assert sentence_segs == ['Euskara Euskal Herriko hizkuntza da.', '[8] Hizkuntza bakartua da,', 'ez baitzaio ahaidetasunik aurkitu.', 'Morfologiari dagokionez,', 'hizkuntza eranskari eta ergatiboa da.', 'Euskaraz mintzo direnei euskaldun deritze.', 'Gaur egun,', 'Euskal Herrian bertan ere hizkuntza gutxitua da,', 'lurralde horretan gaztelania eta frantsesa nagusitu baitira.']
        case 'bel':
            assert sentence_segs == ['Белару́ская мо́ва — нацыянальная мова беларусаў,', "уваходзіць у індаеўрапейскую моўную сям'ю,", 'славянскую групу,', 'усходнеславянскую падгрупу.', 'Пашырана ў асноўным у Беларусі.', 'Распаўсюджана таксама і ў іншых краінах,', 'галоўным чынам у Польшчы,', 'Украіне,', 'Расіі,', 'Літве,', 'Латвіі[2].', 'Беларуская мова мае шмат агульных граматычных і лексічных уласцівасцей з іншымі ўсходнеславянскімі мовамі.']
        case 'bul':
            assert sentence_segs == ['Бъ̀лгарският езѝк е индоевропейски език от групата на южнославянските езици,', 'като образува неговата източна подгрупа.', 'Той е официалният език на Република България и един от 24-те официални езика на Европейския съюз.', 'Българският език е плурицентричен език – има няколко книжовни норми.', 'Наред с използваната в България основна норма,', 'съществуват още македонска норма,', 'която също използва кирилица,', 'и банатска норма,', 'която използва латиница.']
        case 'mya':
            assert sentence_segs == ['မြန်မာဘာသာစကား (အင်္ဂလိပ်:', 'Myanmar Language)သည် မြန်မာနိုင်ငံ၏ ရုံးသုံး ဘာသာစကားဖြစ်သည်။', 'ဗမာလူမျိုးနှင့် ဗမာနွယ်ဝင်(ဓနု၊', 'အင်းသား၊', 'တောင်ရိုးနှင့် ယော)တို့၏ ဇာတိစကားဖြစ်သည်။', 'ဗမာလူမျိုးတို့သည် တိဘက်-ဗမာနွယ် ဘာသာစကားများ (Tibeto-Burman Languages) ပြောဆိုသည့် လူမျိုးနွယ်စုကြီးမှ အကြီးဆုံးသော လူမျိုးဖြစ်သည်။', 'လူဦးရေ ၃၈သန်းကျော်ခန့်သည် မြန်မာဘာသာစကားကို မိခင်ဘာသာစကား အနေဖြင့် သုံး၍ မြန်မာတိုင်းရင်သားများသည် ဒုတိယဘာသာစကား အနေဖြင့် သုံးသည်။']
        case 'bxr':
            assert sentence_segs == ['Буряад хэлэн (буряад-монгол хэлэн) Алтайн хэлэнэй изагуурай буряад арад түмэнһөө хэрэглэгдэжэ бай монгол хэлэнэй бүлэгэй xэлэн-аялгуу юм.', 'Бүгэдэ Найрамдаха Буряад Улас,', 'Эрхүү можо,', 'Забайкалиин хизаар,', 'Усть-Ордын болон Агын тойрогууд,', 'мүн Монгол Уласай хойто аймагууд,', 'Хитадай зүүн-хойто орондо ажаһуудаг буряадууд хэлэлсэдэг.', 'Орос гүрэндэ (1989 оной тоололгоор) 376 мянга оршом хүн буряадаар дуугардаг.', 'Буряадай 86,', '6%-нь буряад хэлые,', '13,', '3%-нь ород хэлые эхэ (түрэлхи) хэлэн гэһэн байна.', 'Баруун (эхирэд,', 'булагад),', 'дундада (алайр,', 'түнхэн),', 'зүүн (хори),', 'урда (сонгоол,', 'сартуул) гэхэ мэтэ аялгуутай.']
        case 'cat':
            assert sentence_segs == ['El català té cinc grans dialectes (valencià,', 'nord-occidental,', 'central,', "balear i rossellonès) que juntament amb l'alguerès,", "es divideixen fins a vint-i-una varietats i s'agrupen en dos grans blocs:", 'el català occidental i el català oriental.', 'Les propostes normatives permeten reduir les diferències entre aquests dialectes en el català estàndard des del punt de vista gramatical,', 'fonètic i de lèxic.']
        case 'lzh':
            assert sentence_segs == ['先民言語，', '傳乎口耳，', '至結繩以記，', '事日贅，', '是結繩之不足，', '求諸繪圖，', '繪圖猶逾，', '而創字製文，', '金石竹帛載之，', '自劉漢而書諸紙。', '唐宋降，', '文士崇古非今，', '尚先秦古文，', '規法矩繩，', '典模乃定。', '由是，', '口述耳聞者雖變於百歲千載，', '手書目觀者猶通，', '前後貫延三代。', '唯文言非創於一舉而得，', '所式所尊，', '莫衷一是，', '時比燕越。']
        case 'zho_cn':
            assert sentence_segs == ['汉语又称中文、', '华语[6]、', '唐话[7]，', '概指由上古汉语（先秦雅言）发展而来、', '书面使用汉字的分析语，', '为汉藏语系最大的一支语族。', '如把整个汉语族视为单一语言，', '则汉语为世界使用人数最多的语言，', '目前全世界有五分之一人口将汉语做为母语或第二语言。']
        case 'zho_tw':
            assert sentence_segs == ['漢語又稱中文、', '華語[6]、', '唐話[7]，', '概指由上古漢語（先秦雅言）發展而來、', '書面使用漢字的分析語，', '為漢藏語系最大的一支語族。', '如把整個漢語族視為單一語言，', '則漢語為世界使用人數最多的語言，', '目前全世界有五分之一人口將漢語做為母語或第二語言。']
        case 'chu':
            assert sentence_segs == ['ВЪ И҃ В҃ ДЬНЬ КЛꙆМЕНТА Бъ҃ ꙇже нъи лѣта огрѧдѫцѣ блаженаго климента мѫченіка твоего ꙇ папежа чьстьѭ веселішꙇ подазь мілостівъі да егоже чьсть чьстімъ сілоѭ ѹбо мѫчениѣ его наслѣдѹемъ г҃мь']
        case 'cop':
            assert sentence_segs == ['ϭⲟⲗ · ⲛⲉⲛⲧⲁⲩⲕⲗⲏⲣⲟⲛⲟⲙⲉⲓ ⲉⲛⲉϩ ⲛⲧⲙⲛⲧⲣⲣⲟ ⲙⲡⲛⲟⲩⲧⲉ ·']
        case 'hrv':
            assert sentence_segs == ['Hrvatski jezik (ISO 639-3:', 'hrv) skupni je naziv za nacionalni standardni jezik Hrvata,', 'te za skup narječja i govora kojima govore ili su nekada govorili Hrvati.', 'Njime govori više od 5,', '5 milijuna ljudi,', '[2] poglavito Hrvata u Hrvatskoj,', '3\u202f980\u202f000 (popis iz 2001.', ') i Bosni i Hercegovini,', '469\u202f000 (2004.', ').', '[3] Hrvatski je materinski jezik za Hrvate u drugim zemljama:', 'Sjedinjenim Američkim Državama,', '58\u202f400 (popis iz 2000.', ');', '[1] Austriji,', '19\u202f400 (popis iz 2001.', ');', 'Srbiji,', '19\u202f223 (popis iz 2011.', ');', '[4] Mađarskoj,', '14\u202f300 (popis iz 2001.', ');', 'Italiji,', '3500 (Vincent 1987.', ');', 'Crnoj Gori,', '6810 (2006.', ');', 'Slovačkoj,', '890 (popis iz 2001.', ').']
        case 'ces':
            assert sentence_segs == ['Čeština neboli český jazyk je západoslovanský jazyk,', 'nejbližší slovenštině,', 'poté lužické srbštině a polštině.', 'Patří mezi slovanské jazyky,', 'do rodiny jazyků indoevropských.', 'Čeština se vyvinula ze západních nářečí praslovanštiny na konci 10.', 'století.', 'Je částečně ovlivněná latinou a němčinou.', 'Česky psaná literatura se objevuje od 14.', 'století.', 'První písemné památky jsou však již z 12.', 'století.']
        case 'dan':
            assert sentence_segs == ['Dansk er et østnordisk sprog indenfor den germanske gren af den indoeuropæiske sprogfamilie.', 'Det danske sprog tales af ca.', 'seks millioner mennesker,', 'hovedsageligt i Danmark,', 'men også i Sydslesvig,', 'på Færøerne og Grønland.', '[1] Dansk er tæt beslægtet med norsk,', 'svensk og islandsk,', 'og sproghistorisk har dansk været stærkt påvirket af plattysk.']
        case 'nld':
            assert sentence_segs == ['Het Nederlands is een West-Germaanse taal,', 'de meest gebruikte taal in Nederland en België,', 'de officiële taal van Suriname en een van de drie officiële talen van België.', 'Binnen het Koninkrijk der Nederlanden is het Nederlands ook een officiële taal van Aruba,', 'Curaçao en Sint-Maarten.', 'Het Nederlands is na Engels en Duits de meest gesproken Germaanse taal.']
        case 'ang':
            assert sentence_segs == ['Seo ænglisce spræc (Englisc gereord) is Westgermanisc spræc,', 'þe fram Englalande aras.', 'Heo is sibb þæm Ealdfresiscan and þære Ealdseaxiscan spræcum.', 'Hit is gastleas spræc,', 'and ne hæfþ nane gebyrdlice sprecan todæg,', 'ac sume menn leorniaþ hit on Betweoxnette and writaþ on him,', 'swa swa her on þissum Wicipædian.']
        case 'eng_gb' | 'eng_us' | 'other':
            assert sentence_segs == ['English is a West Germanic language in the Indo-European language family.', 'Originating in early medieval England,', '[3][4][5] today English is both the most spoken language in the world[6] and the third most spoken native language,', 'after Mandarin Chinese and Spanish.', '[7] English is the most widely learned second language and is either the official language or one of the official languages in 59 sovereign states.', 'There are more people who have learned English as a second language than there are native speakers.', 'As of 2005,', 'it was estimated that there were over two billion speakers of English.', '[8]']
        case 'myv':
            assert sentence_segs == ['Э́рзянь кель — совавтови суоминь-равонь тарадонтень суоми-угрань келень семиянь группанть пельксэнтень,', 'уралонь келень семиянтень.', 'Эрзянь кельсэ кортыть эрзянь ломанть.']
        case 'est':
            assert sentence_segs == ['Eesti keelel on kaks suuremat murderühma (põhjaeesti ja lõunaeesti),', 'mõnes käsitluses eristatakse ka kirderanniku murdeid eraldi murderühmana.', 'Liikumisvõimaluste laienemine ning põhjaeesti keskmurde alusel loodud normitud eesti kirjakeele kasutus on põhjustanud murdeerinevuste taandumise.']
        case 'fao':
            assert sentence_segs == ['Føroyskt er høvuðsmálið í Føroyum.', 'Føroyskt er almenna málið í Føroyum,', 'og tað er tjóðarmál føroyinga.', 'Harafturat verður nógv føroyskt tosað í Danmark og Íslandi.', 'Í Føroyum tosa 48.', '000 fólk føroyskt,', 'í Danmark umleið 25.', '000 og í Íslandi umleið 5.', '000,', 'so samlaða talið av fólkum,', 'ið duga føroyskt liggur um 75-80.', '000.', 'Føroyskt er tí í altjóða høpi eitt lítið mál.', 'Føroyskt mál hevur fýra føll og trý kyn,', 'og grammatiski málbygningurin líkist ógvuliga nógv íslendskum,', 'meðan orðatilfarið og í summum lutum úttalan líkist norska landsmálinum.']
        case 'fin':
            assert sentence_segs == ['Suomen kieli eli suomi on uralilaisten kielten itämerensuomalaiseen ryhmään kuuluva kieli,', 'jota puhuvat pääosin suomalaiset.', 'Suomessa suomen kieltä puhuu äidinkielenään 4,', '8 miljoonaa ja toisena kielenään 0,', '5 miljoonaa ihmistä.', 'Suurimmat suomea puhuvat vähemmistöt ovat Ruotsissa,', 'Norjassa ja Venäjällä.']
        case 'fra':
            assert sentence_segs == ['Le français est une langue indo-européenne de la famille des langues romanes dont les locuteurs sont appelés francophones.', 'Elle est parfois surnommée la langue de Molière.']
        case 'fro':
            assert sentence_segs == ["Si l'orrat Carles,", 'ki est as porz passant.', 'Je vos plevis,', 'ja returnerunt Franc.']
        case 'glg':
            assert sentence_segs == ['O galego ([ɡaˈleɣo̝][1]) é unha lingua indoeuropea que pertence á póla de linguas románicas.', 'É a lingua propia de Galicia,', '[5] onde é falada por uns 2,', '4 millóns de galegos.', '[6] Á parte de en Galicia,', 'a lingua fálase tamén en territorios limítrofes con esta comunidade,', 'aínda que sen estatuto de oficialidade (agás en casos puntuais,', 'como na Veiga),', '[7] así como pola diáspora galega que emigrou a outras partes de España,', 'a América Latina,', 'os Estados Unidos,', 'Suíza e outros países de Europa.']
        case 'deu_at' | 'deu_de' | 'deu_ch':
            assert sentence_segs == ['Das Deutsche ist eine plurizentrische Sprache,', 'enthält also mehrere Standardvarietäten in verschiedenen Regionen.', 'Ihr Sprachgebiet umfasst Deutschland,', 'Österreich,', 'die Deutschschweiz,', 'Liechtenstein,', 'Luxemburg,', 'Ostbelgien,', 'Südtirol,', 'das Elsass und Lothringen sowie Nordschleswig.', 'Außerdem ist Deutsch eine Minderheitensprache in einigen europäischen und außereuropäischen Ländern,', 'z.', 'B.', 'in Rumänien und Südafrika sowie Nationalsprache im afrikanischen Namibia.', 'Deutsch ist die meistgesprochene Muttersprache in der Europäischen Union (EU).', '[26]']
        case 'got':
            assert sentence_segs == ['𐌲𐌿𐍄𐌰𐍂𐌰𐌶𐌳𐌰,', '𐌲𐌿𐍄𐍂𐌰𐌶𐌳𐌰 𐌰𐌹𐌸𐌸𐌰𐌿 𐌲𐌿𐍄𐌹𐍃𐌺𐌰 𐍂𐌰𐌶𐌳𐌰 𐌹𐍃𐍄 𐌲𐌰𐍃𐍅𐌿𐌻𐍄𐌰𐌽𐌰 𐌰𐌿𐍃𐍄𐍂𐌰𐌲𐌰𐌹𐍂𐌼𐌰𐌽𐌹𐍃𐌺𐌰 𐍂𐌰𐌶𐌳𐌰 𐍂𐍉𐌳𐌹𐌳𐌰 𐍆𐍂𐌰𐌼 𐌲𐌿𐍄𐌰𐌼.', '𐍃𐌹 𐌹𐍃𐍄 𐌰𐌹𐌽𐌰𐌷𐍉 𐌰𐌿𐍃𐍄𐍂𐌰𐌲𐌰𐌹𐌼𐌰𐌽𐌹𐍃𐌺𐌰 𐍂𐌰𐌶𐌳𐌰 𐍃𐍉𐌴𐌹 𐌷𐌰𐌱𐌰𐌹𐌸 𐌲𐌰𐌼𐌴𐌻𐌴𐌹𐌽𐌹𐌽𐍃.']
        case 'grc':
            assert sentence_segs == ['ἦλθον δὲ οἱ δύο ἄγγελοι εἰς Σόδομα ἑσπέρας· Λὼτ δὲ ἐκάθητο παρὰ τὴν πύλην Σοδόμων.', 'ἰδὼν δὲ Λὼτ ἐξανέστη εἰς συνάντησιν αὐτοῖς καὶ προσεκύνησεν τῷ προσώπῳ ἐπὶ τὴν γῆν καὶ εἶπεν,', 'ἰδού,', 'κύριοι,', 'ἐκκλίνατε εἰς τὸν οἶκον τοῦ παιδὸς ὑμῶν καὶ καταλύσατε καὶ νίψασθε τοὺς πόδας ὑμῶν,', 'καὶ ὀρθρίσαντες ἀπελεύσεσθε εἰς τὴν ὁδὸν ὑμῶν.', 'εἶπαν δέ,', 'οὐχί,', 'ἀλλ᾿ ἐν τῇ πλατείᾳ καταλύσομεν.']
        case 'ell':
            assert sentence_segs == ['Η ελληνική γλώσσα ανήκει στην ινδοευρωπαϊκή οικογένεια[9] και αποτελεί το μοναδικό μέλος του ελληνικού κλάδου,', 'ενώ είναι η επίσημη γλώσσα της Ελλάδας και της Κύπρου.', 'Ανήκει επίσης στο βαλκανικό γλωσσικό δεσμό.', 'Στην ελληνική γλώσσα,', 'έχουμε γραπτά κείμενα ήδη από τον 15ο αιώνα π.', 'Χ..', 'Σαν Παγκόσμια Ημέρα Ελληνικής Γλώσσας,', 'κάθε έτος,', 'έχει καθιερωθεί η 9η Φεβρουαρίου.', 'Έχει την μακροβιότερη καταγεγραμμένη ιστορία από οποιαδήποτε άλλη ζωντανή ινδοευρωπαϊκή γλώσσα με τουλάχιστον 3.', '400 χρόνια γραπτής ιστορίας.', '[10] Γράφεται με το ελληνικό αλφάβητο,', 'το οποίο χρησιμοποιείται αδιάκοπα (αρχικά με τοπικές παραλλαγές,', 'μετέπειτα υπό μια,', 'ενιαία μορφή) εδώ και περίπου 2.', '600 χρόνια.', '[11][12] Προηγουμένως η ελληνική γλώσσα γραφόταν με τη Γραμμική Β και το κυπριακό συλλαβάριο.', '[13] Το ελληνικό αλφάβητο προέρχεται από το φοινικικό αλφάβητο,', 'με κάποιες προσαρμογές.', 'Στο ελληνικό αλφάβητο βασίζεται το λατινικό,', 'το κυριλλικό,', 'το αρμενικό,', 'το κοπτικό,', 'το γοτθικό και πολλά άλλα αλφάβητα.']
        case 'hbo':
            assert sentence_segs == ['וַ֠יָּבֹאוּ שְׁנֵ֨י הַמַּלְאָכִ֤ים סְדֹ֨מָה֙ בָּעֶ֔רֶב וְלֹ֖וט יֹשֵׁ֣ב בְּשַֽׁעַר־סְדֹ֑ם וַיַּרְא־לֹוט֙ וַיָּ֣קָם לִקְרָאתָ֔ם וַיִּשְׁתַּ֥חוּ אַפַּ֖יִם אָֽרְצָה׃', 'וַיֹּ֜אמֶר הִנֶּ֣ה נָּא־אֲדֹנַ֗י ס֣וּרוּ נָ֠א אֶל־בֵּ֨ית עַבְדְּכֶ֤ם וְלִ֨ינוּ֙ וְרַחֲצ֣וּ רַגְלֵיכֶ֔ם וְהִשְׁכַּמְתֶּ֖ם וַהְלַכְתֶּ֣ם לְדַרְכְּכֶ֑ם וַיֹּאמְר֣וּ לֹּ֔א כִּ֥י בָרְחֹ֖וב נָלִֽין׃']
        case 'heb':
            assert sentence_segs == ['עִבְרִית היא שפה שמית,', 'ממשפחת השפות האפרו-אסיאתיות,', 'הידועה כשפתם של היהודים ושל השומרונים.', 'העברית היא שפתה הרשמית של מדינת ישראל,', 'מעמד שעוגן בשנת תשע"ח,', '2018,', 'בחוק יסוד:', 'ישראל – מדינת הלאום של העם היהודי.']
        case 'hin':
            assert sentence_segs == ['हिन्दी जिसके मानकीकृत रूप को मानक हिन्दी कहा जाता है,', 'विश्व की एक प्रमुख भाषा है और भारत की एक राजभाषा है।', 'केन्द्रीय स्तर पर भारत में सह-आधिकारिक भाषा अंग्रेजी है।', 'यह हिन्दुस्तानी भाषा की एक मानकीकृत रूप है जिसमें संस्कृत के तत्सम तथा तद्भव शब्दों का प्रयोग अधिक है और अरबी–फ़ारसी शब्द कम हैं।', 'हिन्दी संवैधानिक रूप से भारत की राजभाषा और भारत की सबसे अधिक बोली और समझी जाने वाली भाषा है।', 'हिन्दी भारत की राष्ट्रभाषा नहीं है क्योंकि भारत के संविधान में किसी भी भाषा को ऐसा दर्जा नहीं दिया गया है।', '[5][6] एथनोलॉग के अनुसार हिन्दी विश्व की तीसरी सबसे अधिक बोली जाने वाली भाषा है।', '[7] विश्व आर्थिक मंच की गणना के अनुसार यह विश्व की दस शक्तिशाली भाषाओं में से एक है।', '[8]']
        case 'hun':
            assert sentence_segs == ['A magyar nyelv az uráli nyelvcsalád tagja,', 'a finnugor nyelvek közé tartozó ugor nyelvek egyike.', 'Legközelebbi rokonai a manysi és a hanti nyelv,', 'majd utánuk az udmurt,', 'a komi,', 'a mari és a mordvin nyelvek.', 'Vannak olyan vélemények,', 'melyek szerint a moldvai csángó önálló nyelv – különösen annak északi,', 'középkori változata –,', 'így ez volna a magyar legközelebbi rokonnyelve.', '[1]']
        case 'isl':
            assert sentence_segs == ['Íslenska er vesturnorrænt,', 'germanskt og indóevrópskt tungumál sem er einkum talað og ritað á Íslandi og er móðurmál langflestra Íslendinga.', '[5] Það hefur tekið minni breytingum frá fornnorrænu en önnur norræn mál[5] og er skyldara norsku og færeysku en sænsku og dönsku.', '[2][3]']
        case 'ind':
            assert sentence_segs == ['Bahasa Indonesia adalah bahasa nasional dan resmi di seluruh wilayah Indonesia.', 'Ini merupakan bahasa komunikasi resmi,', 'diajarkan di sekolah-sekolah,', 'dan digunakan untuk penyiaran di media elektronik dan digital.', 'Sebagai negara dengan tingkat multilingual (terutama trilingual)[12][13] teratas di dunia,', 'mayoritas orang Indonesia juga mampu bertutur dalam bahasa daerah atau bahasa suku mereka sendiri,', 'dengan yang paling banyak dituturkan adalah bahasa Jawa dan Sunda yang juga memberikan pengaruh besar ke dalam elemen bahasa Indonesia itu sendiri.', '[14][15]']
        case 'gle':
            assert sentence_segs == ['Is ceann de na teangacha Ceilteacha í an Ghaeilge (nó Gaeilge na hÉireann mar a thugtar uirthi corruair),', 'agus ceann de na trí cinn de theangacha Ceilteacha ar a dtugtar na teangacha Gaelacha (Gaeilge,', 'Gaeilge Mhanann agus Gaeilge na hAlban) go háirithe.', 'Labhraítear in Éirinn go príomha í,', 'ach tá cainteoirí Gaeilge ina gcónaí in áiteanna eile ar fud an domhain.']
        case 'ita':
            assert sentence_segs == ["L'italiano ([itaˈljaːno][Nota 1] ascoltaⓘ) è una lingua romanza parlata principalmente in Italia.", 'Per ragioni storiche e geografiche,', "l'italiano è la lingua romanza meno divergente dal latino.", '[2][3][4][Nota 2]']
        case 'jpn':
            assert sentence_segs == ['日本語（にほんご、', 'にっぽんご[注釈 2]）は、', '日本国内や、', 'かつての日本領だった国、', 'そして国外移民や移住者を含む日本人同士の間で使用されている言語。', '日本は法令によって公用語を規定していないが、', '法令その他の公用文は全て日本語で記述され、', '各種法令[注釈 3]において日本語を用いることが規定され、', '学校教育においては「国語」の教科として学習を行うなど、', '事実上日本国内において唯一の公用語となっている。']
        case 'khm':
            assert sentence_segs == ['ភាសាខ្មែរ គឺជាភាសាកំណើតរបស់ជនជាតិខ្មែរនិងជាភាសាផ្លូវការរបស់ប្រទេសកម្ពុជា។', 'ភាសាសំស្ក្រឹតនិងភាសាបាលីបាន\u200bជួយបង្កើតខេមរភាសា ព្រោះភាសាខ្មែរបានខ្ចីពាក្យច្រើនពីភាសាទាំងពីរនេះ។', '\u200bមានអក្សរក្រមវែងជាងគេនៅលើពិភពលោក ។', '\u200b វាជាភាសាមួយដ៏ចំណាស់\u200b ដែលប្រហែលជាមានដើមកំណើតតាំងតែពី\u200b២០០០ឆ្នាំមុនមកម៉្លេះ។']
        case 'kaz':
            assert sentence_segs == ['Қазақ тілі (төте:', 'قازاق ٴتىلى\u200e,', 'латын:', 'qazaq tili) — Қазақстан Республикасының мемлекеттік тілі,', 'сонымен қатар Ресей,', 'Өзбекстан,', 'Қытай,', 'Моңғолия жəне т.', 'б.', 'елдерде тұратын қазақтардың ана тілі.']
        case 'kor':
            assert sentence_segs == ['세계 여러 지역에 한민족 인구가 거주하게 되면서 전 세계 각지에서 한국어가 사용 되고 있다.', '2016년 1월 초 기준으로 한국어 사용 인구는 약 8,', '000만 명으로 추산된다.', '[1]']
        case 'kmr':
            assert sentence_segs == ['Kurmancî,', 'Kurdiya jorîn yan jî Kurdiya bakurî yek ji zaravayên zimanê kurdî ye ku ji aliyê kurdan ve tê axaftin.', 'Zaravayê kurmancî li herçar parçeyên Kurdistanê bi awayekî berfireh tê axaftin û rêjeya zêde ya kurdan bi zaravayê kurmancî diaxivin.', 'Kurmancî li henek deverên herêmên Kurdistanê bi navên cuda cuda hatiye binavkirin.', 'Li Rojhilatê Kurdistanê wekî şikakî û li Başurê Kurdistanê jî wek badînî hatiye binavkirin.']
        case 'kir':
            assert sentence_segs == ['Кыргыз тили — Кыргыз Республикасынын мамлекеттик тили,', 'түрк тилдери курамына,', 'анын ичинде кыргыз-кыпчак же тоо-алтай тобуна кирет.', 'Кыргыз Республикасынын түптүү калкынын,', 'Кытайдагы,', 'Өзбекстан,', 'Тажикстан,', 'Республикасында Ооганстан,', 'Түркия,', 'Орусияда жашап жаткан кыргыздардын эне тили.', '2009 ж.', 'өткөн элди жана турак-жай фондун каттоонун жыйынтыгында Кыргыз Республикасында кыргыз тилин 3 830 556 адам өз эне тили катары көрсөтүшкөн жана 271 187 адам кыргыз тилин экинчи тил катары биле тургандыгы аныкталган[1].', 'Бул КРсындагы калктын 76% кыргыз тилинде сүйлөйт дегенди билдирет.', 'Кыргыз тилинде 1 720 693 адам орус тилин дагы билише тургандыгын көргөзүшкөн[2].', 'Бул 2 109 863 адам кыргыз тилинде гана сүйлөй билишет дегенди билдирет.', 'Болжолдуу эсеп менен дүйнө жүзү боюнча кыргыз тилинде 6 700 000 адам сүйлөйт.']
        case 'lao':
            assert sentence_segs == ['ພາສາລາວ (Lao:', 'ລາວ,', '[láːw] ຫຼື ພາສາລາວ,', '[pʰáːsǎːláːw]) ເປັນພາສາຕະກູນໄທ-ກະໄດຂອງຄົນລາວ ໂດຍມີຄົນເວົ້າໃນປະເທດລາວ ເຊິ່ງເປັນພາສາລັດຖະການຂອງສາທາລະນະລັດ ປະຊາທິປະໄຕ ປະຊາຊົນລາວ ຂອງປະຊາກອນປະມານ 7 ລ້ານຄົນ ແລະໃນພື້ນທີ່ພາກຕາເວັນອອກສຽງເໜືອຂອງປະເທດໄທທີ່ມີຄົນເວົ້າປະມານ 23 ລ້ານຄົນ ທາງລັດຖະບານປະເທດໄທມີການສະໜັບສະໜຸນໃຫ້ເອີ້ນພາສາລາວຖິ່ນໄທວ່າ ພາສາລາວຖິ່ນອີສານ ນອກຈາກນີ້,', 'ຢູ່ທາງພາກຕາເວັນອອກສຽງເໜືອຂອງປະເທດກຳປູເຈຍກໍມີຄົນເວົ້າພາສາລາວຄືກັນ.', 'ພາສາລາວເປັນແມ່ຂອງຄົນເຊື້ອຊາດລາວທັງຢູ່ພາຍໃນແລະຕ່າງປະເທດ ທັງເປັນພາສາກາງຂອງພົນລະເມືອງໃນປະເທດລາວທີ່ມີພາສາອື່ນອີກຫຼາຍພາສາ ເຊິ່ງບາງພາສາບໍ່ມີຄວາມກ່ຽວຂ້ອງກັບພາສານີ້[3] .']
        case 'lat':
            assert sentence_segs == ['Lingua Latina,', '[1] sive sermo Latinus,', '[2] est lingua Indoeuropaea qua primum Latini universi et Romani antiqui in primis loquebantur quamobrem interdum etiam lingua Latia[3] (in Latio enim sueta) et lingua Romana[4] (nam imperii Romani sermo sollemnis) appellatur.', 'Nomen linguae ductum est a terra quam gentes Latine loquentes incolebant,', 'Latium vetus interdum appellata,', 'in paeninsula Italica inter Tiberim,', 'Volscos,', 'Appenninum,', 'et mare Inferum sita.']
        case 'lav':
            assert sentence_segs == ['Latviešu valoda ir dzimtā valoda apmēram 1,', '5 miljoniem cilvēku,', 'galvenokārt Latvijā,', 'kur tā ir vienīgā valsts valoda.', '[1][3] Lielākās latviešu valodas pratēju kopienas ārpus Latvijas ir Apvienotajā Karalistē,', 'ASV,', 'Īrijā,', 'Austrālijā,', 'Vācijā,', 'Zviedrijā,', 'Kanādā,', 'Brazīlijā,', 'Krievijas Federācijā.', 'Latviešu valoda pieder pie indoeiropiešu valodu saimes baltu valodu grupas.', 'Senākie rakstu paraugi latviešu valodā — jau no 15.', 'gadsimta — ir atrodami Jāņa ģildes alus nesēju biedrības grāmatās.', 'Tajā lielākoties bija latvieši,', 'un no 1517.', 'gada arī brālības vecākie bija latvieši.', 'Pirmais teksts latviski iespiests 1507.', 'gadā izdotajā baznīcas rokasgrāmatā „AGENDA”.', '[4]']
        case 'lij':
            assert sentence_segs == ["O baxin d'influensa di dialetti lìguri o l'é de çirca 2 milioìn de personn-e anche se,", "specialmente inti ùrtimi çinquant'anni,", "pe coscì de variante locali se son pèrse e de âtre son a reizego tutt'òua,", "anche pe córpa da mancansa de 'n pâ de generaçioin inta continoasion da parlâ.", 'Coscî,', 'ancheu,', "a popolaçion ch'a conosce a léngoa a l'é ben ben infeiô e ancón meno son quelli che a pàrlan e a scrîvan."]
        case 'lit':
            assert sentence_segs == ['Lietuvių kalba – iš baltų prokalbės kilusi lietuvių tautos kalba,', 'kuri Lietuvoje yra valstybinė,', 'o Europos Sąjungoje – viena iš oficialiųjų kalbų.', 'Lietuviškai kalba apie tris milijonus žmonių (dauguma jų gyvena Lietuvoje).', 'Drauge su latvių,', 'mirusiomis prūsų,', 'jotvingių ir kitomis baltų kalbomis priklauso indoeuropiečių kalbų šeimos baltų kalbų grupei.']
        case 'mkd':
            assert sentence_segs == ['Македонски јазик — јужнословенски јазик,', 'дел од групата на словенски јазици од јазичното семејство на индоевропски јазици.', 'Македонскиот е службен и национален јазик во Македонија,', 'а воедно е и официјално признат како регионален службен јазик во Горица и Пустец во Албанија каде што живее бројно македонско население,', 'но и во Србија како официјален во општините Јабука и Пландиште,', 'Романија и Косово.', 'Македонски се зборува и во Австралија,', 'Бугарија,', 'Грција,', 'Канада,', 'САД,', 'Црна Гора,', 'Турција,', 'во некои земји−членки на Европската Унија и останатата македонска дијаспора.', 'Вкупниот број на македонски говорници е тешко да се утврди поради несоодветни пописи,', 'но бројката се движи од околу 2,', '5 до 3 милиони луѓе.']
        case 'mal':
            assert sentence_segs == ['ദ്രാവിഡഭാഷാ കുടുംബത്തിൽ ഉൾപ്പെടുന്ന മലയാളത്തിന് ഇതര ഭാരതീയ ഭാഷകളായ സംസ്കൃതം,', 'തമിഴ് എന്നീ ഉദാത്തഭാഷകളുമായി പ്രകടമായ ബന്ധമുണ്ട്[8].', 'പൂക്കാട്ടിയൂർ ലിഖിതങ്ങൾ 8 ക്രി.', 'മു മുതൽ 3000 ക്രി.', 'മു അടുത്ത് വരെയും പഴക്കം ചെന്നതാണ്.']
        case 'mlt':
            assert sentence_segs == ['L-oriġini tal-ilsien Malti huma attribwiti għall-wasla,', 'kmieni fis-seklu 11,', 'ta’ settlers minn Sqallija ġirien,', 'fejn kien mitkellem is-sikolu-Għarbi,', 'li biddel il-konkwista tal-gżira mill-Kalifat Fatimid fl-aħħar tas-seklu 9[18].', 'Din it-talba ġiet ikkorroborata minn studji ġenetiċi,', 'li juru li l-Maltin kontemporanji jaqsmu antenati komuni ma’ Sqallin u Calabrians,', 'bi ftit input ġenetiku mill-Afrika ta’ Fuq u l-Levant.']
        case 'glv':
            assert sentence_segs == ['She Gaelg (graït:', '/gɪlg/) çhengey Ghaelagh Vannin.', 'Haink y Ghaelg woish Shenn-Yernish,', "as t'ee cosoylagh rish Yernish as Gaelg ny h-Albey."]
        case 'mar':
            assert sentence_segs == ['मराठी भाषा ही इंडो-युरोपीय भाषाकुळातील एक भाषा आहे.', 'मराठी ही भारताच्या २२ अधिकृत भाषांपैकी एक आहे.', 'मराठी महाराष्ट्र राज्याची अधिकृत तर गोवा राज्याची सहअधिकृत भाषा आहे.', '२०११ च्या जनगणनेनुसार,', 'भारतात मराठी भाषकांची एकूण लोकसंख्या सुमारे १४ कोटी आहे.', 'मराठी मातृभाषा असणाऱ्या लोकांच्या संख्येनुसार मराठी ही जगातील दहावी व भारतातील तिसरी भाषा आहे.', 'मराठी भाषा भारताच्या प्राचीन भाषांपैकी एक असून महाराष्ट्री प्राकृतचे आधुनिक रूप आहे.', 'मराठीचे वय सुमारे २४०० वर्ष आहे.', 'महाराष्ट्र हे मराठी भाषिकांचे राज्य म्हणून मराठी भाषेला वेगळे महत्त्व प्राप्त झालेले आहे.', 'आजतागायत मराठी भाषेतून अनेक श्रेष्ठ साहित्यकृती निर्माण झालेल्या आहेत आणि त्यात सातत्यपूर्ण रीतीने भर पडत आहे.', 'गोवा,', 'गुजरात सारख्या राज्यातही मराठी भाषा काही प्रमाणात बोलली जाते.', 'गोव्यात मराठीला समृद्ध असा इतिहास आहे.', '[१]']
        case 'pcm':
            assert sentence_segs == ['Naijá na pijin,', 'a langwej for oda langwej.', 'Naijá for Inglish an wey Afrikan langwej.']
        case 'nob':
            assert sentence_segs == ['Bokmål er en av to offisielle målformer av norsk skriftspråk,', 'hvorav den andre er nynorsk.', 'I skrift har 87,', '3% bokmål som hovedmål i skolen.', '[1] Etter skriftreformene av riksmål i 1987 og bokmål i 1981 og 2005 er det lite som skiller bokmål og riksmål i alminnelig bruk.']
        case 'nno':
            assert sentence_segs == ['Nynorsk,', 'før 1929 offisielt kalla landsmål,', 'er sidan jamstillingsvedtaket av 12.', 'mai 1885 ei av dei to offisielle målformene av norsk;', 'den andre forma er bokmål.', 'Nynorsk vert i dag nytta av om lag 10–15% av innbyggjarane i Noreg.', '[1][2] Skriftspråket er basert på nynorsk talemål,', 'det vil seie dei moderne norske dialektane til skilnad frå gamalnorsk og mellomnorsk.', 'Når ein seier at nokon snakkar nynorsk,', 'meiner ein helst at dei snakkar nynorsk normaltalemål.', 'Dei færraste dialekttalande nordmenn seier at dei snakkar nynorsk,', 'men det er ikkje uvanleg i kjerneområda til nynorsken.', 'Dette tilhøvet mellom tale og skrift ligg bak målrørsla sitt slagord sidan 1970-talet:', '«Snakk dialekt – skriv nynorsk!', '» Nynorske dialektar vart snakka over heile landet,', 'men det er berre på Vestlandet utanom dei største byene og i dei austlandske fjellbygdene at skriftspråket står sterkt.', 'Det vil seie at dei fleste dialekttalarane har bokmål som det primære skriftspråket sitt.']
        case 'fas':
            assert sentence_segs == ['فارسی یا پارسی یک زبان ایرانی غربی از زیرگروه ایرانی شاخهٔ هندوایرانیِ خانوادهٔ زبان\u200cهای هندواروپایی است که در کشورهای ایران،', 'افغانستان،', 'تاجیکستان،', 'ازبکستان،', 'پاکستان،', 'عراق،', 'ترکمنستان و آذربایجان به آن سخن می\u200cگویند.', 'فارسی یک زبان چندکانونی و زبان رسمی ایران،', 'تاجیکستان و افغانستان به\u200cشمار می\u200cرود.', 'این زبان در ایران و افغانستان به الفبای فارسی،', 'که از خط عربی ریشه گرفته،', 'و در تاجیکستان و ازبکستان به الفبای تاجیکی،', 'که از سیریلیک آمده،', 'نوشته می\u200cشود.', 'زبان فارسی در افغانستان به\u200cطور رسمی دَری (از ۱۳۴۳ خورشیدی) و در تاجیکستان تاجیکی (از دورهٔ شوروی) خوانده می\u200cشود.']
        case 'pol':
            assert sentence_segs == ['Język polski,', 'polszczyzna – język z grupy zachodniosłowiańskiej (do której należą również czeski,', 'kaszubski,', 'słowacki i języki łużyckie),', 'stanowiącej część rodziny indoeuropejskiej.', 'Jest językiem urzędowym w Polsce oraz należy do oficjalnych języków Unii Europejskiej.']
        case 'qpm':
            assert sentence_segs == ['Kážyjte nǽko,', 'de!', 'Še go preskókneme!']
        case 'por_br' | 'por_pt':
            assert sentence_segs == ['A língua portuguesa,', 'também designada português,', 'é uma língua indo-europeia românica flexiva ocidental originada no galego-português falado no Reino da Galiza e no norte de Portugal.', 'Com a criação do Reino de Portugal em 1139 e a expansão para o sul na sequência da Reconquista,', 'deu-se a difusão da língua pelas terras conquistadas e mais tarde,', 'com as descobertas portuguesas,', 'para o Brasil,', 'África e outras partes do mundo.', '[8] O português foi usado,', 'naquela época,', 'não somente nas cidades conquistadas pelos portugueses,', 'mas também por muitos governantes locais nos seus contatos com outros estrangeiros poderosos.', 'Especialmente nessa altura a língua portuguesa também influenciou várias línguas.', '[9]']
        case 'ron':
            assert sentence_segs == ['Limba română este o limbă indo-europeană din grupul italic și din subgrupul oriental al limbilor romanice.', 'Printre limbile romanice,', 'româna este a cincea după numărul de vorbitori,', 'în urma spaniolei,', 'portughezei,', 'francezei și italienei.', 'Din motive de diferențiere tipologică,', 'româna mai este numită în lingvistica comparată limba dacoromână sau dialectul dacoromân.', 'De asemenea,', 'este limba oficială în România și în Republica Moldova.']
        case 'rus':
            assert sentence_segs == ['Ру́сский язы́к (МФА:', '[ˈruskʲɪi̯ jɪˈzɨk]ⓘ)[~ 3][⇨] — язык восточнославянской группы славянской ветви индоевропейской языковой семьи,', 'национальный язык русского народа.', 'Является одним из наиболее распространённых языков мира — восьмым среди всех языков мира по общей численности говорящих[5] и седьмым по численности владеющих им как родным (2022)[2].', 'Русский является также самым распространённым славянским языком[8] и самым распространённым языком в Европе — географически и по числу носителей языка как родного[6].']
        case 'orv':
            assert sentence_segs == ['шаибатъ же ѿ бедерѧ г҃ мсци а ѿ дабылѧ до шаибата в҃ мсца моремъ итьти']
        case 'sme':
            assert sentence_segs == ['Davvisámegiella gullá sámegielaid oarjesámegielaid davvejovkui ovttas julev- ja bihtánsámegielain.', 'Eará oarjesámegielat leat ubmisámegiella ja lullisámegiella.']
        case 'san':
            assert sentence_segs == ['संस्कृतम् जगतः एकतमा अतिप्राचीना समृद्धा शास्त्रीया च भाषासु वर्तते।', 'संस्कृतम् भारतस्य जगत:', 'वा भाषासु एकतमा\u200c प्राचीनतमा।', 'भारती,', 'सुरभारती,', 'अमरभारती,', 'अमरवाणी,', 'सुरवाणी,', 'गीर्वाणवाणी,', 'गीर्वाणी,', 'देववाणी,', 'देवभाषा,', 'संस्कृतावाक्,', 'दैवीवाक्,', 'इत्यादिभिः नामभिः एतद्भाषा प्रसिद्धा।']
        case 'gla':
            assert sentence_segs == ["'S i cànan dùthchasach na h-Alba a th' anns a' Ghàidhlig.", "'S i ball den teaghlach de chànanan Ceilteach dhen mheur Ghoidhealach a tha anns a' Ghàidhlig.", "Tha Goidhealach a' gabhail a-steach na cànanan Gàidhealach gu lèir;", 'Gàidhlig na h-Èireann,', 'Gàidhlig Mhanainn,', 'agus Gàidhlig agus gu dearbh chan eil anns an fhacal "Goidhealach" ach seann fhacal a tha a\' ciallachadh "Gàidhealach".']
        case 'srp_latn':
            assert sentence_segs == ['Srpski jezik je zvaničan u Srbiji,', 'Bosni i Hercegovini i Crnoj Gori i govori ga oko 12 miliona ljudi.', '[13] Takođe je manjinski jezik u državama centralne i istočne Evrope.', '[13]']
        case 'snd':
            assert sentence_segs == ['سنڌي (/ˈsɪndi/[6]सिन्धी,', 'Sindhi)ھڪ ھند-آريائي ٻولي آھي جيڪا سنڌ جي تاريخي خطي ۾ سنڌي ماڻھن پاران ڳالھائي وڃي ٿي.', 'سنڌي پاڪستان جي صوبي سنڌ جي سرڪاري ٻولي آھي.', '[7][8][9] انڊيا ۾،', 'سنڌي وفاقي سرڪار پاران مڃتا حاصل ڪيل ٻولين يعني شيڊيولڊ ٻولين مان ھڪ آھي.', 'گھڻا سنڌي ڳالھائيندڙ پاڪستان جي صوبي سنڌ،', 'ڀارت جي رياست گجرات جي علائقي ڪڇ ۽ مھاراشٽر جي علائقي الھاس نگر ۾ رھن ٿا.', 'ڀارت ۾ بچيل ڳالھائيندڙ سنڌي ھندو آھن جن پاڪستان جي آزادي کان بعد 1948ع ۾ ڀارت ۾ رھائش اختيار ڪئي ۽ باقي سنڌي سڄي دنيا جي مختلف علائقن ۾ رھن ٿا.', 'سنڌي ٻولي پاڪستان جي صوبن سنڌ،', 'بلوچستان ۽ پنجاب،', 'سان گڏوگڏ ڀارت جي رياستن راجستان،', 'پنجاب ۽ گجرات ۾ ڳالھائي وڃي ٿي.', 'ان سان گڏوگڏ ھانگ ڪانگ،', 'عمان،', 'انڊونيشيا،', 'سنگاپور،', 'گڏيل عرب اماراتون،', 'گڏيل بادشاھت ۽ آمريڪا ۾ لڏي ويل جماعتن پاران بہ ڳالھائي وڃي ٿي.', '[10]']
        case 'slk':
            assert sentence_segs == ['Slovenčina je oficiálne úradným jazykom Slovenska,', 'Vojvodiny a od 1.', 'mája 2004 jedným z jazykov Európskej únie.', 'Jazykový kód alebo po anglicky Language Code je sk príp.', 'slk podľa ISO 639.', 'Slovenčina je známa ako „esperanto“ slovanských jazykov,', 'vníma sa ako najzrozumiteľnejšia aj pre používateľov iných slovanských jazykov.', '[2]']
        case 'slv':
            assert sentence_segs == ['Slovenščina [sloˈʋenʃtʃina] je združeni naziv za uradni knjižni jezik Slovencev in skupno ime za narečja in govore,', 'ki jih govorijo ali so jih nekoč govorili Slovenci.', 'Govori ga okoli 2,', '5 (dva in pol) milijona govorcev po svetu,', 'od katerih jih večina živi v Sloveniji.', 'Glede na število govorcev ima razmeroma veliko narečij.', 'Slovenščina je zahodni južnoslovanski jezik in eden redkih indoevropskih jezikov,', 'ki je ohranil dvojino.', 'Za zapisovanje slovenskega jezika se danes uporablja gajica,', 'pisava imenovana po hrvaškem jezikoslovcu Ljudevitu Gaju,', 'ki jo je priredil po češkem črkopisu.', 'Slovenska gajica se imenuje slovenica.', 'Pišemo jo od marčne revolucije 1848.', 'Do takrat smo uporabljali bohoričico.']
        case 'hsb':
            assert sentence_segs == ['Hornjoserbšćina je zapadosłowjanska rěč,', 'kotraž so w Hornjej Łužicy wokoło městow Budyšin,', 'Kamjenc a Wojerecy rěči.', 'Wona je přiwuzna z delnjoserbšćinu w susodnej Delnjej Łužicy,', 'čěšćinu,', 'pólšćinu,', 'słowakšćinu a kašubšćinu.', 'Jako słowjanska rěč hornjoserbšćina k indoeuropskim rěčam słuša.']
        case 'spa':
            assert sentence_segs == ['El español o castellano es una lengua romance procedente del latín hablado,', 'perteneciente a la familia de lenguas indoeuropeas.', 'Forma parte del grupo ibérico y es originaria de Castilla,', 'reino medieval de la península ibérica.', 'Se conoce también informalmente como castillan.', '1\u200b33\u200b34\u200b en algunas áreas rurales e indígenas de América,', '35\u200b pues el español se empezó a enseñar poco después de la incorporación de los nuevos territorios a la Corona de Castilla.', '36\u200b37\u200b38\u200b39\u200b40\u200b41\u200b']
        case 'swe':
            assert sentence_segs == ['Svenska (svenska\u2009(info)) är ett östnordiskt språk som talas av ungefär tio miljoner personer främst i Sverige där språket har en dominant ställning som huvudspråk,', 'men även som det ena nationalspråket i Finland och som enda officiella språk på Åland.', 'I övriga Finland talas det som modersmål framförallt i de finlandssvenska kustområdena i Österbotten,', 'Åboland och Nyland.', 'En liten minoritet svenskspråkiga finns även i Estland.', 'Svenska är nära besläktat och i hög grad ömsesidigt begripligt med danska och norska.', 'De andra nordiska språken,', 'isländska och färöiska,', 'är mindre ömsesidigt begripliga med svenska.', 'Liksom de övriga nordiska språken härstammar svenskan från en gren av fornnordiska,', 'vilket var det språk som talades av de germanska folken i Skandinavien.']
        case 'tam':
            assert sentence_segs == ['தமிழ் (Tamil language) தமிழர்களினதும் தமிழ் பேசும் பலரின் தாய்மொழி ஆகும்.', 'தமிழ்,', 'உலகில் உள்ள முதன்மையான மொழிகளில் ஒன்றும் செம்மொழியும் ஆகும்.', 'இந்தியா,', 'இலங்கை,', 'மலேசியா,', 'சிங்கப்பூர் ஆகிய நாடுகளில் அதிக அளவிலும்,', 'ஐக்கிய அரபு அமீரகம்,', 'தென்னாப்பிரிக்கா,', 'மொரிசியசு,', 'பிசி,', 'இரீயூனியன்,', 'திரினிடாடு போன்ற நாடுகளில் சிறிய அளவிலும் தமிழ் பேசப்படுகிறது.', '1997-ஆம் ஆண்டுப் புள்ளி விவரப்படி உலகம் முழுவதிலும் 8 கோடி (80 மில்லியன்) மக்களால் பேசப்படும் தமிழ்,', '[13] ஒரு மொழியைத் தாய்மொழியாகக் கொண்டு பேசும் மக்களின் எண்ணிக்கை அடிப்படையில் பதினெட்டாவது இடத்தில் உள்ளது.', '[14] இணையத்தில் அதிகம் பயன்படுத்தப்படும் இந்திய மொழிகளில் தமிழ் முதன்மையாக உள்ளதாக 2017-ஆம் ஆண்டு நடைபெற்ற கூகுள் கணக்கெடுப்பில் தெரிய வந்தது.', '[15]']
        case 'tel':
            assert sentence_segs == ['తెలుగు అనేది ద్రావిడ భాషల కుటుంబానికి చెందిన భాష.', 'దీనిని మాట్లాడే ప్రజలు ప్రధానంగా ఆంధ్ర,', 'తెలంగాణాలో ఉన్నారు.', 'ఇది ఆ రాష్ట్రాలలో అధికార భాష.', 'భారతదేశంలో ఒకటి కంటే ఎక్కువ రాష్ట్రాల్లో ప్రాథమిక అధికారిక భాషా హోదా కలిగిన కొద్ది భాషలలో హిందీ,', 'బెంగాలీలతో పాటు ఇది కూడా ఉంది.', '[5][6] పుదుచ్చేరిలోని యానం జిల్లాలో తెలుగు అధికారిక భాష.', 'ఒడిశా,', 'కర్ణాటక,', 'తమిళనాడు,', 'కేరళ,', 'పంజాబ్,', 'ఛత్తీస్\u200cగఢ్,', 'మహారాష్ట్ర,', 'అండమాన్ నికోబార్ దీవులలో గుర్తింపబడిన అల్పసంఖ్యాక భాష.', 'దేశ ప్రభుత్వం భారతదేశ ప్రాచీన భాషగా గుర్తించిన ఆరు భాషలలో ఇది ఒకటి.', '[7][8]']
        case 'tha':
            assert sentence_segs == ['ภาษาไทย หรือ ภาษาไทยกลาง เป็นภาษาในกลุ่มภาษาไท ซึ่งเป็นกลุ่มย่อยของตระกูลภาษาขร้า-ไท และเป็นภาษาราชการ และภาษาประจำชาติของประเทศไทย[3][4] มีการสันนิษฐานว่าภาษาในตระกูลนี้มีถิ่นกำเนิดจากทางตอนใต้ของประเทศจีน และนักภาษาศาสตร์บางส่วนเสนอว่า ภาษาไทยน่าจะมีความเชื่อมโยงกับตระกูลภาษาออสโตร-เอเชียติก ตระกูลภาษาออสโตรนีเซียน และตระกูลภาษาจีน-ทิเบต']
        case 'bod':
            assert sentence_segs == ['བོད་ཀྱི་སྐད་ཡིག་ནི་བོད་ཡུལ་དང་ཉེ་འཁོར་གྱི་ས་ཁུལ་བལ་ཡུལ།', 'འབྲུག་དང་འབྲས་ལྗོངས།', 'ལ་དྭགས་ནས་ལྷོ་མོན་རོང་སོགས་སུ་བེད་སྤྱོད་བྱེད་པའི་སྐད་ཡིག་དེ།', 'ད་ཆར་ཡོངས་གྲགས་སུ་བོད་ཀྱི་ཡུལ་གྲུ་སྟོད་སྨད་བར་གསུམ་ལ་ལྟོས་ཏེ་ནང་གསེས་རིགས་གསུམ་དུ་ཕྱེ་བ་སྟེ།', 'སྟོད་དབུས་གཙང་གི་སྐད་དང་།', 'བར་ཁམས་པའི་སྐད་དང་།', 'སྨད་ཨ་མདོའི་སྐད་རྣམས་སོ།', 'བོད་སྐད་ནི་ཧོར་སོག་ལ་སོགས་པ་གྲངས་ཉུང་མི་རིགས་གཞན་པ་ཁག་ཅིག་གིས་བེད་སྤྱོད་གཏོང་བཞིན་ཡོད་པར་མ་ཟད།', 'བལ་ཡུལ་དང་།', 'འབྲས་ལྗོངས།', 'འབྲུག་ཡུལ་།', 'རྒྱ་གར་ཤར་དང་བྱང་རྒྱུད་མངའ་སྡེ་ཁག་གཅིག་བཅས་ཀྱི་རྒྱལ་ཁབ་རྣམས་སུའང་བེད་སྤྱོད་གཏོང་བཞིན་ཡོད།']
        case 'tur':
            assert sentence_segs == ['Türkçe ya da Türk dili,', "Güneydoğu Avrupa ve Batı Asya'da konuşulan,", 'Türk dilleri dil ailesine ait sondan eklemeli bir dil.', '[12] Türk dilleri ailesinin Oğuz dilleri grubundan bir Batı Oğuz dili olan Osmanlı Türkçesinin devamını oluşturur.', 'Dil,', 'başta Türkiye olmak üzere Balkanlar,', 'Ege Adaları,', "Kıbrıs ve Orta Doğu'yu kapsayan eski Osmanlı İmparatorluğu coğrafyasında konuşulur.", "[12] Ethnologue'a göre Türkçe,", 'yaklaşık 83 milyon konuşuru ile dünyada en çok konuşulan 16.', 'dildir.', '[13] Türkçe Türkiye,', "Kıbrıs Cumhuriyeti ve Kuzey Kıbrıs'ta ulusal resmî dil statüsüne sahiptir.", '[12]']
        case 'ukr':
            assert sentence_segs == ['Украї́нська мо́ва (МФА:', '[ukrɑ̽ˈjɪnʲsʲkɑ̽ ˈmɔwɑ̽],', 'історичні назви — ру́ська[10][11][12][* 1]) — національна мова українців.', "Належить до східнослов'янської групи слов'янських мов,", "що входять до індоєвропейської мовної сім'ї,", 'поряд з романськими,', 'германськими,', 'кельтськими,', 'грецькою,', 'албанською,', "вірменською та найближче спорідненими зі слов'янськими балтійськими мовами[13][14][* 2].", 'Є державною мовою в Україні[13][15].']
        case 'urd':
            assert sentence_segs == ['1837ء میں،', 'اردو برطانوی ایسٹ انڈیا کمپنی کی سرکاری زبان بن گئی،', 'کمپنی کے دور میں پورے شمالی ہندوستان میں فارسی کی جگہ لی گئی۔', 'فارسی اس وقت تک مختلف ہند-اسلامی سلطنتوں کی درباری زبان کے طور پر کام کرتی تھی۔', '[11] یورپی نوآبادیاتی دور میں مذہبی،', 'سماجی اور سیاسی عوامل پیدا ہوئے جنھوں نے اردو اور ہندی کے درمیان فرق کیا،', 'جس کی وجہ سے ہندی-اردو تنازعہ شروع ہوا ۔']
        case 'uig':
            assert sentence_segs == ['ئۇيغۇر تىلى ئۇيغۇر جۇڭگو شىنجاڭ ئۇيغۇر ئاپتونوم رايونىنىڭ ئېيتقان بىر تۈركىي تىلى.', 'ئۇ ئۇزاق ئەسىرلىك تەرەققىيات داۋامىدا قەدىمكى تۈركىي تىللار دەۋرى،', 'ئورخۇن ئۇيغۇر تىلى دەۋرى،', 'ئىدىقۇت-خاقانىيە ئۇيغۇر تىلى دەۋرى،', 'چاغاتاي ئۇيغۇر تىلى دەۋرىنى بېسىپ ئۆتكەن.', 'بۇ جەرياندا ئۇيغۇر تىلى ئورخۇن-يېنسەي يېزىقى،', 'قەدىمكى ئۇيغۇر يېزىقى،', 'بىراخما يېزىقى،', 'مانى يېزىقى،', '،', 'ئەرەب يېزىقى قاتارلىق يېزىقلار بىلەن خاتىرىلەنگەن (بەئزى يېزىقلار ئومۇميۈزلۈك،', 'بەزى يېزىقلار قىسمەن قوللىنىلغان)،', 'شۇنداقلا سانسىكرىتچە،', 'ساكچە،', 'تۇخارچە،', 'سوغدچە،', 'ئەرەبچە،', 'پارسچە،', 'موڭغۇلچە،', 'خىتايچە قاتارلىق نۇرغۇرن تىللار بىلەن ئۇچرىشىپ ھەم ئۆزئارا تەسىر كۆرسىتىپ،', 'ئۈزلۈكسىز مۇكەممەللەشكەن ۋە ھازىرقى زامان ئۇيغۇر تىلى دەۋرىگە كىرگەن.']
        case 'vie':
            assert sentence_segs == ['Tiếng Việt,', 'cũng gọi là tiếng Việt Nam[9] hay Việt ngữ là ngôn ngữ của người Việt và là ngôn ngữ chính thức tại Việt Nam.', 'Đây là tiếng mẹ đẻ của khoảng 85% dân cư Việt Nam cùng với hơn 4 triệu người Việt kiều.', 'Tiếng Việt còn là ngôn ngữ thứ hai của các dân tộc thiểu số tại Việt Nam và là ngôn ngữ dân tộc thiểu số được công nhận tại Cộng hòa Séc.']
        case 'cym':
            assert sentence_segs == ['Yng Nghyfrifiad y DU (2011),', 'darganfuwyd bod 19% (562,', '000) o breswylwyr Cymru (tair blwydd a throsodd) yn gallu siarad Cymraeg.', "O'r ffigwr hwn,", 'darganfuwyd bod 77% (431,', '000) yn gallu siarad,', 'darllen,', "ac ysgrifennu'r iaith;", 'dywedodd 73% o breswylwyr Cymru (2.', '2 miliwn) fod dim sgiliau yn y Gymraeg ganddynt.', '[8] Gellir cymharu hwn â Chyfrifiad 2001,', 'a ddarganfu fod 20.', "8% o'r boblogaeth yn gallu siarad Cymraeg,", 'gyda 57% (315,', "000) o'r ffigwr hon yn dweud eu bod yn rhugl yn yr iaith.", '[9]']
        case 'wol':
            assert sentence_segs == ['Wolof làkk la wu ñuy wax ci Gàmbi (Gàmbi Wolof),', 'Gànnaar (Gànnaar Wolof),', 'ak Senegaal (Senegaal Wolof).', 'Mi ngi bokk nag moom wolof ci bànqaasub atlas bu làkki Kongóo yu kojug nit ñu ñuul ñi.', 'Mbokkoo gi mu am ak làkku pël lu yàgg la.', 'Am na it lumu séq ak yeneen làkk ci gox bi niki séeréer,', 'joolaa ak basari.']
        case _:
            raise wl_test_init.Wl_Exception_Tests_Lang_Skipped(lang)

@pytest.mark.parametrize('lang', test_langs)
def test_sentence_seg_tokenize_tokens(lang):
    print(f'Testing {lang} / Sentence Segment Tokenizer with tokens...')

    tokens = ''.join(getattr(wl_test_lang_examples, f'TEXT_{lang.upper()}')).split()
    sentence_segs = wl_sentence_tokenization.wl_sentence_seg_tokenize_tokens(main, tokens)

    if lang not in [
        'lzh', 'zho_cn', 'zho_tw', 'chu', 'cop', 'jpn', 'orv', 'tha'
    ]:
        assert len(sentence_segs) > 1

def test_sentence_tokenize_misc():
    # Sentences and sentence segments should not be split within pre-tokenized tokens
    assert wl_sentence_tokenization.wl_sentence_split(main, text = 'a.b c') == ['a.b c']
    assert wl_sentence_tokenization.wl_sentence_seg_tokenize_tokens(main, tokens = ['a,b', 'c']) == [['a,b', 'c']]

if __name__ == '__main__':
    for lang, sentence_tokenizer in test_sentence_tokenizers_local:
        test_sentence_tokenize(lang, sentence_tokenizer)

    for lang in test_langs_split:
        test_sentence_split(lang)

    for lang in test_langs_split:
        test_sentence_seg_tokenize(lang)

    for lang in test_langs_split:
        test_sentence_seg_tokenize_tokens(lang)

    test_sentence_tokenize_misc()
