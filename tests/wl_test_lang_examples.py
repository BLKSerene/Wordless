# ----------------------------------------------------------------------
# Tests: Language examples
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

from tests import wl_test_init

# Examples are extracted from Wikipedia in different languages
# Encodings
ENCODING_ARA = '''ٱللُّغَةُ ٱلْعَرَبِيَّة هي أكثر اللغات السامية تحدثًا، وإحدى أكثر اللغات انتشاراً في العالم، يتحدثها أكثر من 467 مليون نسمة.(1) ويتوزع متحدثوها في الوطن العربي، بالإضافة إلى العديد من المناطق الأخرى المجاورة كالأحواز وتركيا وتشاد ومالي والسنغال وإرتيريا وإثيوبيا وجنوب السودان وإيران. وبذلك فهي تحتل المركز الرابع أو الخامس من حيث اللغات الأكثر انتشارًا في العالم، وهي تحتل المركز الثالث تبعًا لعدد الدول التي تعترف بها كلغة رسمية؛ إذ تعترف بها 27 دولة لغةً رسميةً، واللغة الرابعة من حيث عدد المستخدمين على الإنترنت. اللغةُ العربيةُ ذات أهمية قصوى لدى المسلمين، فهي عندَهم لغةٌ مقدسة إذ إنها لغة القرآن، وهي لغةُ الصلاة وأساسيةٌ في القيام بالعديد من العبادات والشعائرِ الإسلامية. العربيةُ هي أيضاً لغة شعائرية رئيسية لدى عدد من الكنائس المسيحية في الوطن العربي، كما كُتبَت بها كثير من أهمِّ الأعمال الدينية والفكرية اليهودية في العصور الوسطى. ارتفعتْ مكانةُ اللغةِ العربية إثْرَ انتشارِ الإسلام بين الدول إذ أصبحت لغة السياسة والعلم والأدب لقرون طويلة في الأراضي التي حكمها المسلمون. وللغة العربية تأثير مباشر وغير مباشر على كثير من اللغات الأخرى في العالم الإسلامي، كالتركية والفارسية والأمازيغية والكردية والأردية والماليزية والإندونيسية والألبانية وبعض اللغات الإفريقية الأخرى مثل الهاوسا والسواحيلية والتجرية والأمهرية والصومالية، وبعض اللغات الأوروبية وخاصةً المتوسطية كالإسبانية والبرتغالية والمالطية والصقلية؛ ودخلت الكثير من مصطلحاتها في اللغة الإنجليزية واللغات الأخرى، مثل أدميرال والتعريفة والكحول والجبر وأسماء النجوم. كما أنها تُدرَّس بشكل رسمي أو غير رسمي في الدول الإسلامية والدول الإفريقية المحاذية للوطن العربي.

العربية لغةٌ رسمية في كل دول الوطن العربي إضافة إلى كونها لغة رسمية في تشاد وإريتريا. وهي إحدى اللغات الرسمية الست في منظمة الأمم المتحدة، ويُحتفل باليوم العالمي للغة العربية في 18 ديسمبر كذكرى اعتماد العربية بين لغات العمل في الأمم المتحدة. وفي سنة 2011 صنفت بلومبيرغ بيزنس ويك اللغة العربية في المرتبة الرابعة من حيث اللغات الأكثر فائدة في الأعمال التجارية على مستوى العالم. وفي 2013 نشر المجلس الثقافي البريطاني تقريرًا مفصلاً عن اللغات الأكثر طلباً في المملكة المتحدة تحت عنوان "لغات المستقبل" وتبين أن العربية تحتل المرتبة الثانية على مستوى العالم وفي عام 2017 احتلت المرتبة الرابعة. فيما يخص اللغات الأكثر جنيًا للأرباح في بريطانيا تأتي العربية في المرتبة الثانية وفقًا للمنظمة.

تحتوي اللغة العربية 28 حرفاً مكتوباً. ويرى بعضُ اللغويين أنه يجب إضافة حرف الهمزة إلى حروف العربية، ليصبحَ عدد الحروف 29. تُكتب العربية من اليمين إلى اليسار - ومثلها اللغة الفارسية والعبرية على عكس كثير من اللغات العالمية - ومن أعلى الصفحة إلى أسفلها.'''
ENCODING_ZHO_CN = '''汉语又称华语[6][7]，是来自汉民族的语言[8][7][9]。

汉语是汉藏语系中最大的一支语族，若把整个汉语族视为单一语言，则汉语为世界上母语使用者人数最多的语言，目前全世界有五分之一人口将其作为母语或第二语言。此外，汉语是中华人民共和国、中华民国和新加坡共和国的官方语言，也是海外华人地区、果敢族、东干族和塔兹族等少数民族社区的通用语，也是多个国家官方承认的少数民族语言，在国际事务上是联合国官方语言之一[10]，并被上海合作组织、金砖国家等国际组织采用为官方工作语言。历史上，汉语词汇和汉字也被一些受中华治世势力范围影响的周边国家借为使用，并形成汉字文化圈。

汉语圈的主要通用语是现代标准汉语[注 1]，其以北京官话为基础。在许多语境中，所谓“汉语”实际上指现代标准汉语。

汉语有多种方言变体，如官话、赣语、闽语、粤语、客家语、吴语、湘语等。对于汉语下属语言的分类，学界主要有两种观点，一种观点将汉语定义为语言，并将上述分支定义为一级方言；另一种观点则将汉语视为语族，各大分支因难以互相沟通而视为语支，而语支下面的各个方言被视为被统一文字团结在一起的独立语言[注 2][11]。无论用哪种观点，包括官话在内，上述各种汉语方言在分类中都处于平等的地位；而汉语是它们的集合体，并非专指它们当中的其中一种。上述所有汉语方言基本都有声调，并且在很大程度上是分析语。

汉语使用的书写形式是汉字，是一种意音文字[注 3]，在表意之同时也具一定表音功能。汉字如今有繁简两种字体。汉语存在书面语及口语的区分：古代书面语称为文言文，源自于上古汉语的表达方式；现代书面语一般指官话白话文，即使用标准官话语法、词汇的中文通行文体。汉语非官话方言区除采用官话白话文并辅以本地方音之外，也流行以本地方言直接记录白话文，如粤语区流行夹杂文言文、官话白话文及粤语白话文的三及第文体，闽语区亦偶有闽语白话文和台语白话文，吴语区亦偶有吴语白话文。

中文[注 4]是以汉语及汉字写就的文本的统称，且在许多情况下[注 5]被用于指代“汉语”语言本身。但在学术研究等领域中，“中文”“汉语”等概念应严格区分。'''
ENCODING_ZHO_TW = '''漢語又稱華語[6][7]，是來自漢民族的語言[8][7][9]。

漢語是漢藏語系中最大的一支語族，若把整個漢語族視為單一語言，則漢語為世界上母語使用者人數最多的語言，目前全世界有五分之一人口將其作為母語或第二語言。此外，漢語是中華人民共和國、中華民國和新加坡共和國的官方語言，也是海外華人地區、果敢族、東干族和塔茲族等少數民族社區的通用語，也是多個國家官方承認的少數民族語言，在國際事務上是聯合國官方語言之一[10]，並被上海合作組織、金磚國家等國際組織採用為官方工作語言。歷史上，漢語詞彙和漢字也被一些受中華治世勢力範圍影響的周邊國家借為使用，並形成漢字文化圈。

漢語圈的主要通用語是現代標準漢語[註 1]，其以北京官話為基礎。在許多語境中，所謂「漢語」實際上指現代標準漢語。

漢語有多種方言變體，如官話、贛語、閩語、粵語、客家語、吳語、湘語等。對於漢語下屬語言的分類，學界主要有兩種觀點，一種觀點將漢語定義為語言，並將上述分支定義為一級方言；另一種觀點則將漢語視為語族，各大分支因難以互相溝通而視為語支，而語支下面的各個方言被視為被統一文字團結在一起的獨立語言[註 2][11]。無論用哪種觀點，包括官話在內，上述各種漢語方言在分類中都處於平等的地位；而漢語是它們的集合體，並非專指它們當中的其中一種。上述所有漢語方言基本都有聲調，並且在很大程度上是分析語。

漢語使用的書寫形式是漢字，是一種意音文字[註 3]，在表意之同時也具一定表音功能。漢字如今有繁簡兩種字體。漢語存在書面語及口語的區分：古代書面語稱為文言文，源自於上古漢語的表達方式；現代書面語一般指官話白話文，即使用標準官話文法、詞彙的中文通行文體。漢語非官話方言區除採用官話白話文並輔以本地方音之外，也流行以本地方言直接記錄白話文，如粵語區流行夾雜文言文、官話白話文及粵語白話文的三及第文體，閩語區亦偶有閩語白話文和台語白話文，吳語區亦偶有吳語白話文。

中文[註 4]是以漢語及漢字寫就的文本的統稱，且在許多情況下[註 5]被用於指代「漢語」語言本身。但在學術研究等領域中，「中文」「漢語」等概念應嚴格區分。'''
ENCODING_HRV = '''Hrvatski jezik obuhvaća govoreni i pisani hrvatski standardni jezik i sve narodne govore kojima govore i pišu Hrvati.[4] Povijesno, obuhvaća sve govore i sve književne jezike izgrađene na tim govorima, kojima su se služili Hrvati.[5][6] Status hrvatskoga kao službenoga jezika u Hrvatskoj propisan je Zakonom o hrvatskom jeziku (NN 14/2024.).[7]

Njime govori više od 5,5 milijuna ljudi[2] u Hrvatskoj i hrvatskim zajednicama u inozemstvu. Hrvatskim jezikom kao materinskim služi se 3 687 735 stanovnika prema podatcima popisa stanovništva Hrvatske iz 2021.[8]

Hrvatski je službeni jezik Republike Hrvatske, jedan od triju službenih jezika Bosne i Hercegovine te jedan od 24 službena jezika Europske unije.[2]

Prema poredbenom jezikoslovlju hrvatski jezik jest sustav triju narječja:

čakavskog
kajkavskog
štokavskog.
Proučavanje hrvatskog jezika cilj je znanstvene discipline kroatistike.

Hrvatski sabor utemeljio je 1997. Dane hrvatskoga jezika od 11. do 17. ožujka.[9] Institut za hrvatski jezik od 2013. obilježava Mjesec hrvatskoga jezika, od 21. veljače (Međunarodnoga dana materinskog jezika) do 17. ožujka (dana potpisa Deklaracije o nazivu i položaju hrvatskog književnog jezika).[9]'''
ENCODING_ENG_US = '''English is a West Germanic language in the Indo-European language family, whose speakers, called Anglophones, originated in early medieval England on the island of Great Britain.[4][5][6] The namesake of the language is the Angles, one of the Germanic peoples that migrated to Britain after its Roman occupiers left. English is the most spoken language in the world, primarily due to the global influences of the former British Empire (succeeded by the Commonwealth of Nations) and the United States.[7] English is the third-most spoken native language, after Mandarin Chinese and Spanish;[8] it is also the most widely learned second language in the world, with more second-language speakers than native speakers.

English is either the official language or one of the official languages in 59 sovereign states (such as India, Ireland, and Canada). In some other countries, it is the sole or dominant language for historical reasons without being explicitly defined by law (such as in the United States and United Kingdom).[9] It is a co-official language of the United Nations, the European Union, and many other international and regional organisations. It has also become the de facto lingua franca of diplomacy, science, technology, international trade, logistics, tourism, aviation, entertainment, and the Internet.[10] English accounts for at least 70% of total native speakers of the Germanic languages, and Ethnologue estimated that there were over 1.5 billion speakers worldwide as of 2021.[3]

Old English emerged from a group of West Germanic dialects spoken by the Anglo-Saxons. Late Old English borrowed some grammar and core vocabulary from Old Norse, a North Germanic language.[11][12][13] Then, Middle English borrowed vocabulary extensively from French dialects, which are the source of approximately 28% of Modern English words, and from Latin, which is the source of an additional 28%.[14] While Latin and the Romance languages are thus the source for a majority of its lexicon taken as a whole, English grammar and phonology retain a family resemblance with the Germanic languages, and most of its basic everyday vocabulary remains Germanic in origin. English exists on a dialect continuum with Scots; it is next-most closely related to Low Saxon and Frisian.'''
ENCODING_FRA = '''Le français est une langue indo-européenne de la famille des langues romanes dont les locuteurs sont appelés « francophones ».

Il est la cinquième langue parlée au monde après l'anglais, le mandarin, le hindi et l'espagnol. Elle est également la deuxième langue apprise sur le globe et la troisième langue des affaires et du commerce. Le français se classe deuxième parmi les langues étrangères les plus fréquemment enseignées à travers le monde6. Il est également la quatrième langue utilisée sur Internet après l'espagnol, le mandarin et l'anglais7,8, langue dont le vocabulaire a été fortement enrichi par le français.

En 2018, 80 millions d'élèves et étudiants s'instruisent en français dans le monde9.

Selon l'Observatoire démographique et statistique de l'espace francophone (ODSEF) de l'Université Laval et l'Observatoire de la langue française de l'OIF, en 2024, le français, on vient de le dire, est la cinquième langue la plus parlée au monde, avec 343 millions10 de locuteurs représentant 4,2 % de la population mondiale (1 personne sur 24), dont 270 millions en font un usage quotidien (pays européens et/ou hors européens), ce qui représente 3,3 % de la population mondiale (1 personne sur 30). Ce nombre de 343 millions de francophones en 2024 devrait approcher les 700 millions en 2050 selon l'Organisation internationale de la francophonie (OIF)6, soit 8 % de la population (1 personne sur 12), et 85 % de ces francophones seront en Afrique, du fait de la forte croissance démographique de ce continent.

Les chiffres avancés par l'OIF ont été contestés, notamment en raison des méthodes de calcul utilisées et de la définition du terme « francophone ». Selon les auteurs d'un ouvrage publié en 2017 qui dresse un portrait exhaustif de la francophonie dans le monde, une estimation crédible des francophones réels, c'est-à-dire qui utilisent le français quotidiennement comme langue maternelle ou deuxième, se situerait autour de 130 millions, ce qui placerait le français au neuvième rang des langues les plus parlées comme langue maternelle ou deuxième11.

Dans le monde, vingt-sept États ont le français comme langue officielle. C'est une des six langues officielles ainsi qu'une des deux langues de travail de l'Organisation des Nations unies. Le français est une langue officielle ou de travail de nombreuses organisations gouvernementales internationales, parmi lesquelles l'Union postale universelle ou les trois autorités mondiales de régulation du système métrique. Il est aussi langue officielle ou de travail de nombreuses organisations gouvernementales régionales, telles que l'Union africaine ou l’Union européenne, et est aussi langue officielle ou de travail de nombreuses organisations non gouvernementales internationales, comme le Comité international olympique ou le Mouvement international de la Croix-Rouge et du Croissant-Rouge.

Grâce à sa présence sur tous les continents et du fait qu'elle est l'une des langues officielles de l'ONU ainsi qu'une de ses langues de travail, le français figure parmi les langues les plus influentes du monde12.

L'histoire du français et des francophones est celle de la rencontre et de l'échange entre de nombreux peuples. Le français est une variété de la langue d'oïl, un groupe de langues romanes parlées originellement dans la partie septentrionale du domaine gallo-roman, sur le territoire des actuelles France, Suisse et Belgique. Les langues gallo-romanes résultent de l'évolution, sous l'influence de langues germaniques, tel que le vieux-francique des Francs, du latin populaire parlé en Gaule par les Gallo-Romains. Ces derniers formaient un ensemble de peuples d'origines principalement celtes qui furent progressivement romanisés à la suite de la conquête romaine de la région, terminée aux alentours de 52 av. J.-C. En 843, l'historien franc Nithard, petit-fils de Charlemagne, produit ce qui est considéré comme le premier texte connu en langue française. Il s'agit d'une chronique qui retranscrit les serments d'alliance, prononcés à Strasbourg l'année précédente, par Louis le Germanique, premier souverain allemand.

Durant le Moyen Âge européen, en particulier entre le Xe et le XIIIe siècle, alors que le système de déclinaisons de l'ancien français s'effondre, les langues d'oïl commencent à se diffuser hors de leur domaine d'origine du fait des invasions normandes des îles Britanniques, du sud de l'Italie ou bien des croisades qui, en établissant des États latins au Levant, font du français une base de la lingua franca méditerranéenne. En 1539, par l’ordonnance de Villers-Cotterêts, le moyen français, langue maternelle des dynasties capétiennes, devient la langue juridique et administrative en France. À la même période, il commence à se diffuser plus massivement hors d'Europe, d'abord en Amérique, puis en Afrique, en Asie et en Océanie, sous l'effet de l'expansion des empires coloniaux français puis belge. À partir du XVIIe siècle, dans les océans Atlantique, Indien et Pacifique, les déportations de populations pratiquées par les empires européens vers leurs colonies amènent, dans un contexte principalement d'esclavage, à la formation de nombreux créoles à base lexicale française.

En 1794, par le décret révolutionnaire du 2 thermidor an II et bien qu'il ait été, sous l'Ancien Régime, la langue des cours royales et princières européennes, le français classique, langue des Lumières, devient la seule langue officielle de la Première République française13. Une des particularités du français se trouve dans le fait que son développement et sa codification ont été en partie l'œuvre de groupes intellectuels, comme la Pléiade, ou d'institutions, comme l'Académie française. Le français est ainsi souvent considéré comme une langue « académique ». À partir du XIXe siècle, et malgré quelques réformes au cours des siècles suivants, son orthographe codifiée commence à se figer. Elle est considérée comme transparente dans le sens de la lecture, mais opaque dans le sens de l'écriture. Au cours du XXe siècle, le français devient une langue d'envergure mondiale en même temps qu'il s'émancipe de l'Europe : à partir de ce siècle le nombre de francophones vivant hors d'Europe dépasse le nombre de locuteurs sur le continent d'origine de la langue.

Entre le 16 mars et le 20 mars 1970 et sous l'impulsion de ceux qui deviendront les « cinq pères fondateurs de la Francophonie » — Léopold Sédar Senghor, poète, écrivain et premier président de la république du Sénégal, Habib Bourguiba, avocat et premier président de la République tunisienne, Hamani Diori, professeur et premier président de la république du Niger, Norodom Sihanouk, roi du Cambodge et Jean-Marc Léger, écrivain et journaliste canadien — a lieu, dans la salle des séances de l'Assemblée nationale du Niger, la conférence de Niamey. Celle-ci, une des premières conférences réunissant les gouvernements des états francophones, établit l'Agence de coopération culturelle et technique, le premier organisme intergouvernemental francophone, et jette ainsi les bases pour la création d'une Organisation internationale de la francophonie (OIF) qui réunit les peuples partageant la langue française. En 1988, en commémoration de cet évènement, les États membres de l'Organisation font du 20 mars la Journée internationale de la francophonie.

En 1989, ont lieu au Maroc les premiers jeux de la Francophonie qui réunissent pour la première fois les athlètes de la communauté francophone autour de la langue qu'ils partagent. En 1997, à Hanoï, capitale du Viêt Nam, les États francophones adoptent la Charte institutionnelle de la Francophonie qui sera complétée en 2005 à Antananarivo, capitale de Madagascar, par la Charte de la Francophonie. Ces deux chartes présentent l'importance du multilinguisme pour le monde francophone, les valeurs de solidarité, d'égalité et de fraternité entre les peuples qui doivent être véhiculées par la langue française, vecteur de progrès et de modernité, ainsi que le rôle actif que doivent exercer les francophones pour la préservation de la diversité linguistique et culturelle. En 2010, l'Organisation des Nations unies déclare que le 20 mars de chaque année sera observée à travers le monde la Journée de la langue française en souvenir de la conférence de Niamey. Les organisations francophones proposent autour de cette date des semaines d'échanges et de discussions souvent appelées « Semaine de la langue française et de la francophonie ».

La langue française est un attribut culturel souverain pour de nombreux peuples et États comme en France où depuis 1992 « la langue de la République est le français » ou au Québec où depuis 1977 elle « permet au peuple québécois d’exprimer son identité ». Elle est également le principal véhicule des cultures francophones dans le monde et le moyen principal d'expression de leurs pensées. La langue, parfois surnommée « langue de Molière14 », ne cesse de s'enrichir que ce soit de façon formelle, par des décrets par exemple, mais aussi de façon informelle.'''
ENCODING_DEU = '''Die deutsche Sprache oder Deutsch [dɔɪ̯tʃ][24] ist eine westgermanische Sprache, die weltweit etwa 90 bis 105 Millionen Menschen als Muttersprache und weiteren rund 80 Millionen als Zweit- oder Fremdsprache dient.

Das Deutsche ist eine plurizentrische Sprache, enthält also mehrere Standardvarietäten in verschiedenen Regionen. Ihr Sprachgebiet umfasst Deutschland, Österreich, die Deutschschweiz, Liechtenstein, Luxemburg, Ostbelgien, Südtirol, das Elsass und den Nordosten Lothringens sowie Nordschleswig. Außerdem ist Deutsch eine Minderheitensprache in einigen europäischen und außereuropäischen Ländern, z. B. in Rumänien und Nationalsprache im afrikanischen Namibia. Deutsch ist die meistgesprochene Muttersprache in der Europäischen Union (EU).[25]

Ursprünglich bestand eine Vielzahl von Mundarten innerhalb eines Dialektkontinuums, das sich aufgrund der zweiten (hochdeutschen) Lautverschiebung in hochdeutsche (oberdeutsche und mitteldeutsche) und niederdeutsche Mundarten einteilen lässt. Da die Niederdeutsche Sprache außerhalb des Hochdeutschen steht, ist sie oft nicht mitgemeint, wenn von „der deutschen Sprache“ die Rede ist. Teilweise wird Niederdeutsch bzw. „Platt“ aber auch als Dialekt des Deutschen behandelt.

Die deutsche Standardsprache ist mit ihren Standardvarietäten bundesdeutsches Deutsch, österreichisches Deutsch und schweizerisches Deutsch das Ergebnis bewusster sprachplanerischer Eingriffe. Das Standarddeutsche überspannt als Dachsprache den Großteil der Mundarten des Dialektkontinuums. Eine Ausnahme sind z. B. die Luxemburger Dialekte, die nunmehr unter Letzebuergesch und somit nur noch indirekt als Deutsch zusammengefasst werden.[26]

Die wissenschaftliche Disziplin, die die deutsche Sprache und deutschsprachige Literatur in ihren historischen und gegenwärtigen Formen behandelt, wird Germanistik genannt (dieser Ausdruck bezieht sich also meist nicht auf die germanischen Sprachen insgesamt).'''
ENCODING_ELL = '''Η ελληνική γλώσσα ανήκει στην ινδοευρωπαϊκή οικογένεια[9] secεπίσης στο βαλκανικό γλωσσικό δεσμό. ελληνική γλώσσα, έχουμε γραπτά κείμενα ήδη από τον 15ο αιώνα π.Χ.. Σαν Παγκόσμια Ημέρα Ελληνικής Γλώσσας, κάθε έτος, έχει καθιερωθεί η 9η Φεβρουαρίου. Έχει την μακροβιότερη καταγεγραμμένη ιστορία από οποιαδήποτε άλλη ζωντανή ινδοευρωπαϊκή γλώσσα με τουλάχιστον 3.400 χρόνια γραπτής ιστορίας.[10] Γράφεται με το ελληνικό αλφάβητο, το οποίο χρησιμοποιείται αδιάκοπα (αρχικά με τοπικές παραλλαγές, μετέπειτα υπό μια, ενιαία μορφή) εδώ και περίπου 2.600 χρόνια.[11][12] Προηγουμένως η ελληνική γλώσσα γραφόταν με τη Γραμμική Β και το κυπριακό συλλαβάριο.[13] Το ελληνικό αλφάβητο προέρχεται από το φοινικικό αλφάβητο, με κάποιες προσαρμογές. Στο ελληνικό αλφάβητο βασίζεται το λατινικό, το κυριλλικό, το αρμενικό, το κοπτικό, το γοτθικό και πολλά άλλα αλφάβητα.

Η ελληνική γλώσσα κατέχει υψηλή -ιστορική- θέση στην ιστορία του Δυτικού κόσμου.[14] Ξεκινώντας με τα Ομηρικά έπη, η αρχαία ελληνική λογοτεχνία περιλαμβάνει πολλά σημαντικά έργα της Ευρωπαϊκής λογοτεχνίας. Η ελληνική γλώσσα είναι η γλώσσα με την οποία συντέθηκαν πολλά από τα θεμελιώδη επιστημονικά και φιλοσοφικά κείμενα. Η Καινή Διαθήκη γράφτηκε στα ελληνικά και έπειτα μεταφράστηκε σε άλλες γλώσσες.[15][16] Μαζί με τα λατινικά κείμενα και τις παραδόσεις του Ρωμαϊκού κόσμου, τα ελληνικά κείμενα και η ελληνική κοινωνία της αρχαιότητας αποτελούν μέρος της κλασικής επιστήμης.

Κατά τη διάρκεια της αρχαιότητας, η ελληνική ήταν η κύρια γλώσσα του μεσογειακού κόσμου. Έπειτα έγινε η επίσημη γλώσσα της Βυζαντινής Αυτοκρατορίας και εξελίχθηκε στα Μεσαιωνικά Ελληνικά.[17] Στη σύγχρονη μορφή τους τα ελληνικά είναι η επίσημη γλώσσα της Ελλάδας και της Κύπρου και μια από τις 24 επίσημες γλώσσες της Ευρωπαϊκής Ένωσης. Την ομιλούν, ως μητρική γλώσσα, τουλάχιστον 13,5 εκατομμύρια άνθρωποι στην Ελλάδα, την Κύπρο, την Ιταλία, την Αλβανία, την Τουρκία και την ελληνική διασπορά. Επίσης εκατομμύρια άτομα γνωρίζουν ελληνικά, είτε την αρχαία μορφή της ή τα νέα ελληνικά.

Οι ελληνικές ρίζες χρησιμοποιούνται για αιώνες και συνεχίζουν να χρησιμοποιούνται ευρέως για να σχηματίσουν νέες λέξεις σε άλλες γλώσσες. Πολλές ελληνικές λέξεις μπορούν να εντοπιστούν στις περισσότερες κύριες γλώσσες του κόσμου. Τα ελληνικά και τα λατινικά, ως γλωσσικές δεξαμένες, είναι οι κύριες πηγές του διεθνούς επιστημονικού και τεχνολογικού λεξιλογίου.

Ο συνολικός αριθμός των ανθρώπων που μιλούν τα νέα ελληνικά ως μητρική τους γλώσσα είναι περίπου 14 εκατομμύρια άτομα. Οι περισσότεροι από αυτούς είναι Έλληνες στην εθνικότητα, αν και στην Ελλάδα χρησιμοποιείται επίσης ευρέως από αρκετούς εξελληνισμένους Αρωμάνους, Μεγλενορουμάνους, Τσιγγάνους, Αλβανούς, Σλάβους και μια σειρά από μουσουλμανικές εθνότητες στα βόρεια της χώρας. Χάρη στους αυξημένους οικονομικούς δεσμούς της Ελλάδας με άλλες βαλκανικές χώρες, καθώς και χάρη στις μαζικές μεταναστεύσεις προς την Ελλάδα και την Κύπρο τα τελευταία είκοσι χρόνια, ένας σημαντικός αριθμός κατοίκων στις χώρες που συνορεύουν με την Ελλάδα μιλάει και ελληνικά. Ελληνόγλωσσοι υπάρχουν πάρα πολλοί στην Αλβανία, όπου ομιλείται ευρέως στα νότια της χώρας και στις μεγάλες πόλεις και είναι ουσιαστικά η γλώσσα εργασίας σε τρεις δήμους της Αλβανίας. Ως σημαντική γλώσσα της διασποράς, τα ελληνικά χρησιμοποιούνται μεταξύ των Ελλήνων της Αυστραλίας, του Καναδά και των ΗΠΑ. Ο συνολικός αριθμός των ανθρώπων που μιλούν την ελληνική ως ξένη γλώσσα κυμαίνεται στα 3 με 5 εκατομμύρια άτομα.

Η ελληνική λογοτεχνία έχει πλούσια παραγωγή σε όλα τα στάδια της ιστορίας της. Στη Ρωμαϊκή Αυτοκρατορία η γνώση της ελληνικής γλώσσας θεωρούνταν υποχρέωση του κάθε μορφωμένου Ρωμαίου. Τα λατινικά έχουν δανειστεί μεγάλο αριθμό ελληνικών δανείων και αντιθέτως τα ελληνικά έχουν σημαντικό αριθμό λατινικών και ρομανικών λέξεων.

Η ελληνική ομιλείται από τουλάχιστον 13 εκατομμύρια άτομα σήμερα, κυρίως στην Ελλάδα και την Κύπρο, μαζί με μια μεγάλη ελληνόφωνη μειονότητα στην Αλβανία κοντά στα σύνορα με την Ελλάδα. Ένα σημαντικό ποσοστό των Αλβανών έχει βασική γνώση της ελληνικής λόγω του κύματος της αλβανικής μετανάστευσης στην Ελλάδα τις δεκαετίες του 1980 και του 1990. Πριν τη Μικρασιατική Εκστρατεία και την ανταλλαγή πληθυσμών του 1923, υπήρχε ένας πολύ μεγάλος αριθμός Ελληνόφωνων στη Τουρκία, αλλά σήμερα παραμένουν ελάχιστοι.[10] Μια σημαντική ελληνόφωνη κοινότητα βρίσκεται στη Βουλγαρία κοντά στα ελληνοβουλγαρικά σύνορα. Η ελληνική ομιλείται από μεγάλες κοινότητες απόδημων Ελλήνων στις Ηνωμένες Πολιτείες, την Αυστραλία, τον Καναδά, τη Νότια Αφρική, τη Χιλή, τη Βραζιλία, την Αργεντινή, τη Ρωσία, την Ουκρανία, το Ηνωμένο Βασίλειο, και στην Ευρωπαϊκή Ένωση, ιδίως στη Γερμανία.

Ιστορικά υπήρχαν σημαντικές ελληνόφωνες κοινότητες στην Ανατολική Μεσόγειο, τη νότια Ιταλία, την Τουρκία, την Κύπρο, την Συρία, τον Λίβανο, το Ισραήλ, την Αίγυπτο, τη Λιβύη, στη περιοχή της Μαύρης Θάλασσας (στις περιοχές της σημερινής Βουλγαρίας, Τουρκίας, Ρουμανίας, Ουκρανίας, Ρωσίας, Γεωργίας, Αρμενίας και Αζερμπαϊτζάν) και σε μια μικρότερη έκταση στη δυτική Μεσόγειο εντός και γύρω από αποικίες όπως η Μασσαλία, ο Μόνοικος και η Μαινάκη. Χρησιμοποιήθηκε επίσης ως λειτουργική γλώσσα στο χριστιανικό βασίλειο της Μακουρίας στο σημερινό Σουδάν.[18]

Η ελληνική υπήρξε στην αρχαιότητα η πιο διαδεδομένη γλώσσα στη Μεσόγειο και στη Νότια Ευρώπη, κυρίως εξαιτίας του πλήθους των αποικιών που είχαν ιδρυθεί από τους Έλληνες στις ακτές της Μεσογείου, ενώ έφτασε να είναι η γλώσσα του εμπορίου ακόμα και μέχρι και τα τέλη της αλεξανδρινής περιόδου. Η ελληνική σήμερα αποτελεί τη μητρική γλώσσα περίπου 12 εκατομμυρίων ανθρώπων, κυρίως στην Ελλάδα και την Κύπρο. Αποτελεί επίσης τη μητρική γλώσσα αυτοχθόνων πληθυσμών στην Αλβανία, τη Βουλγαρία, την Ιταλία, την Βόρεια Μακεδονία και την Τουρκία. Εξαιτίας της μετανάστευσης η γλώσσα ομιλείται ακόμα σε χώρες-προορισμούς ελληνόφωνων πληθυσμών μεταξύ των οποίων η Αυστραλία, η Γερμανία, οι Ηνωμένες Πολιτείες, το Ηνωμένο Βασίλειο, ο Καναδάς, η Ρωσία και άλλα κράτη της πρώην Σοβιετικής Ένωσης. Υπολογίζεται ότι ο συνολικός αριθμός ανθρώπων παγκοσμίως που μιλούν τα ελληνικά ως πρώτη ή δεύτερη γλώσσα είναι γύρω στα 25 εκατομμύρια.[εκκρεμεί παραπομπή]'''
ENCODING_HEB = '''עִבְרִית היא שפה שמית, ממשפחת השפות האפרו-אסייתיות, הידועה כשפתם של היהודים ושל השומרונים. היא שייכת למשפחת השפות הכנעניות והשפה הכנענית היחידה המדוברת כיום. העברית היא שפתה הרשמית של מדינת ישראל, מעמד שעוגן בשנת תשע"ח, 2018, בחוק יסוד: ישראל – מדינת הלאום של העם היהודי.'''
ENCODING_ISL = '''Íslenska er vesturnorrænt, germanskt og indóevrópskt tungumál sem er einkum talað og ritað á Íslandi og er móðurmál langflestra Íslendinga.[6] Það hefur tekið minni breytingum frá fornnorrænu en önnur norræn mál[6] og er skyldara norsku og færeysku en sænsku og dönsku.[3][4]

Ólík mörgum öðrum vesturevrópskum tungumálum hefur íslenskan ítarlegt beygingarkerfi. Nafnorð og lýsingarorð eru beygð jafnt sem sagnir. Fjögur föll eru í íslensku, eins og í þýsku, en íslenskar nafnorðabeygingar eru flóknari en þær þýsku. Beygingarkerfið hefur ekki breyst mikið frá víkingaöld, þegar Norðmenn komu til Íslands með norræna tungumál sitt.

Meirihluti íslenskumælenda býr á Íslandi, eða um 300.000 manns.[7] Um 8.000 íslenskumælendur búa í Danmörku, en þar af eru 3.000 nemendur. Í Bandaríkjunum eru talendur málsins um 5.000, og í Kanada 1.400. Stærsti hópur kanadískra íslenskumælenda býr í Manitoba, sérstaklega í Gimli, þar sem Vestur-Íslendingar settust að. Þó að 97% Íslendinga telji íslensku móðurmál sitt er tungumálið nokkuð í rénun utan Íslands. Þeir sem tala íslensku utan Íslands eru oftast aðfluttir Íslendingar, nema í Gimli þar sem íslenskumælendur hafa búið frá 1880.

Árnastofnun sér um varðveislu málsins og hýsir miðaldahandrit sem skrifuð voru á Íslandi. Auk þess styður hún rannsóknir á málinu. Frá 1995 hefur verið haldið upp á dag íslenskrar tungu þann 16. nóvember á hverju ári, sem var fæðingardagur Jónas Hallgrímssonar skálds.'''
ENCODING_GLE = '''Is ceann de na teangacha Ceilteacha í an Ghaeilge (nó Gaeilge na hÉireann mar a thugtar uirthi corruair), agus ceann de na trí cinn de theangacha Ceilteacha ar a dtugtar na teangacha Gaelacha (Gaeilge, Gaeilge Mhanann agus Gaeilge na hAlban) go háirithe. Labhraítear in Éirinn go príomha í, ach tá cainteoirí Gaeilge ina gcónaí in áiteanna eile ar fud an domhain.

Is í an teanga náisiúnta nó dhúchais agus an phríomhtheanga oifigiúil i bPoblacht na hÉireann í an Ghaeilge. Tá an Béarla luaite sa Bhunreacht mar theanga oifigiúil eile. Tá aitheantas oifigiúil aici chomh maith i dTuaisceart Éireann, ar cuid den Ríocht Aontaithe é. Ar an 13 Meitheamh 2005 d'aontaigh airí gnóthaí eachtracha an Aontais Eorpaigh glacadh leis an nGaeilge mar theanga oifigiúil oibre san AE. Ón 1 Eanáir 2007 cuireadh tús leis an stádas oifigiúil seo, agus ba é an tAire Nollaig Ó Treasaigh, T. D., an chéad aire Éireannach a labhair Gaeilge ag cruinniú de chuid Chomhairle na nAirí, an 22 Eanáir 2007.

Tá go leor ainmneacha eile réigiúnda nó stairiúla ar an teanga freisin: Gaedhealg, Gaedhilge agus Gaedhilg (i gConamara); Gaedhilic, Gaeilic agus Gaeilig (in áiteanna i gCúige Uladh agus Maigh Eo); Gaedhealaing, Gaoluinn agus Gaeilinn (i bPort Láirge); Gaelainn (sa Mhumhain); Gaedhlag (Ó Méith, Ard Mhacha agus Lú); agus Guithealg nó Goidelc (sa tSean-Ghaeilge). Go minic, níl i gceist leo seo ach litrithe malartacha ar an bhfocal "Gaeilge" agus iad ag baint leis an tréimhse réamhchaighdeánach (féach thíos chun a thuilleadh eolais a fháil), ach tabhair faoi deara gurb iondúil inniu a úsáidtear an leagan Muimhneach d'ainm na teanga, Gaelainn, le tagairt a dhéanamh do chanúint an chúige ina gcluinfeá an t-ainm seo uirthi. D'fheicfeá Gaoluinn, leis, toisc gur mar é fada a fhuaimnítear ao an litrithe sna canúintí deisceartacha.'''
ENCODING_JPN = '''日本語（にほんご、にっぽんご[注釈 3]）は、日本国内や、かつての日本領だった国、そして国外移民や移住者を含む日本人同士の間で使用されている言語。日本は法令によって公用語を規定していないが、法令その他の公用文は全て日本語で記述され、各種法令[注釈 4]において日本語を用いることが規定され、学校教育においては「国語」の教科として学習を行うなど、事実上日本国内において唯一の公用語となっている。

使用人口について正確な統計はないが、日本国内の人口、及び日本国外に住む日本人や日系人、日本がかつて統治した地域の一部住民など、約1億3,000万人以上と考えられている[10]。統計によって前後する場合もあるが、この数は世界の母語話者数で上位10位以内に入る人数である[11]。

また第一次世界大戦後、日本に委任統治（南洋諸島を参照）されていたパラオでは、現在も一部地域で日本語を公用語と定めている。'''
ENCODING_KAZ = '''Қазақ тілі (төте: قازاق ٴتىلى‎, латын: qazaq tılı) — Қазақстан Республикасының мемлекеттік тілі, сонымен қатар Ресей, Өзбекстан, Қытай, Моңғолия жəне т.б. елдерде тұратын қазақтардың ана тілі.

Қазақ тілі түркі тілдерінің қыпшақ тобына, соның ішінде қарақалпақ, ноғай, қарашай тілдерімен бірге қыпшақ-ноғай тармағына жатады. Сонымен қатар қырғыз, татар, башқұрт, қарашай-балқар, құмық, қарайым, қырымтатар тілдеріне жақын.

Қазақ тілі диалектілерге бөлінбейтіні ғылыми түрде дәлелденген. Барлық өлкелердің қазақтары бір-бірін жақсы түсінеді. Бірақ кейбір ғалымдардың пікірінше қазақ тілі 3 диалектіге бөлінеді: солтүстік-шығыс, оңтүстік және батыс (ескі үш жүздің орналасқан аумағы бойынша).'''
ENCODING_KOR = '''한국어(韓國語), 조선어(朝鮮語)는 대한민국과 조선민주주의인민공화국의 공용어이다. 둘은 표기나 문법, 동사 어미나 표현에서 약간의 차이가 있다.

세계 여러 지역에 한민족 인구가 이주하여 거주하자 전세계 각지에서 한국어를 사용한다. 2016년 1월 초 기준으로 한국어 사용 인구는 약 8,000만 명으로 추산한다.[1]

역사 및 현대 언어학자들은 한국어를 고립어로 분류한다.[2][3][4][5][6][7] 그러나 한국어와 제주어(제주도에서 사용하며 구별한다고 간주함)와 함께 한국어족을 구성하던 몇 개의 사라진 언어(사어)가 한 때 존재했었다.[8][9] 일부 언어학자들이 한국어를 알타이 제어에 포함하였지만, 오늘날 알타이 제어설을 더 이상 지지하지 않는다.[10]'''
ENCODING_LAV = '''Latviešu valoda ir dzimtā valoda apmēram 1,5 miljoniem cilvēku, galvenokārt Latvijā, kur tā ir vienīgā valsts valoda.[1][3] Lielākās latviešu valodas pratēju kopienas ārpus Latvijas ir Apvienotajā Karalistē, ASV, Īrijā, Austrālijā, Vācijā, Zviedrijā, Kanādā, Brazīlijā, Krievijas Federācijā. Latviešu valoda pieder pie indoeiropiešu valodu saimes baltu valodu grupas. Senākie rakstu paraugi latviešu valodā — jau no 15. gadsimta — ir atrodami Jāņa ģildes alus nesēju biedrības grāmatās. Tajā lielākoties bija latvieši, un no 1517. gada arī brālības vecākie bija latvieši. Pirmais teksts latviski iespiests 1507. gadā izdotajā baznīcas rokasgrāmatā „AGENDA”.[4]'''
ENCODING_MLT = '''Il-Malti huwa l-ilsien nazzjonali tar-Repubblika ta' Malta. Huwa l-ilsien uffiċjali flimkien mal-Ingliż; kif ukoll wieħed mill-ilsna uffiċjali u l-uniku wieħed ta' oriġini Għarbija (Semitiku) tal-Unjoni Ewropea. Dan l-ilsien għandu sisien u għerq semitiku, ta' djalett Għarbi li ġej mit-Tramuntana tal-Afrika, għalħekk qatt ma kellu rabta mill-qrib mal-Għarbi Klassiku. Iżda tul iż-żminijiet, minħabba proċess tal-Latinizzazzjoni ta' Malta, bdew deħlin bosta elementi lingwistiċi mill-Isqalli, djalett ta' art li wkoll għaddiet minn żmien ta' ħakma Għarbija. Wara l-Isqalli beda dieħel ukoll it-Taljan, fuq kollox fiż-żmien tad-daħla tal-Kavallieri tal-Ordni ta' San Ġwann sa meta l-Ingliż ħa post it-Taljan bħala l-ilsien uffiċjali fil-Kostituzzjoni Kolonjali tal-1934. Il-Malti huwa l-ilsien waħdieni ta' għajn semitika li jinkiteb b'ittri Latini. Studju tal-2016 juri li, fil-lingwaġġ bażiku ta’ kuljum, il-Maltin kapaċi jifhmu madwar terz ta’ dak li jingħad lilhom bl-Għarbi Tuneżin li huwa Għarbi tal-Maghrebi relatat mal-Għarbi Sqalli, filwaqt li dawk li jitkellmu bl-Għarbi Tuneżin (Tuneżin) huma kapaċi jifhmu madwar 40% ta’ dak li jingħad lilhom bil-Malti.[1]'''
ENCODING_FAS = '''فارسی یا پارسی یکی از زبان‌های ایرانی غربی از زیرگروه ایرانی شاخهٔ هندوایرانیِ خانوادهٔ زبان‌های هندواروپایی است که در کشورهای ایران، افغانستان، تاجیکستان، ازبکستان، پاکستان، عراق، ترکمنستان و آذربایجان به آن سخن می‌گویند. فارسی زبان چندکانونی و فراقومی است و زبان رسمی ایران، تاجیکستان و افغانستان به‌شمار می‌رود. این زبان در ایران و افغانستان به الفبای فارسی، که از خط پهلوی ریشه گرفته، و در تاجیکستان و ازبکستان به الفبای تاجیکی، که از سیریلیک آمده، نوشته می‌شود. زبانِ فارسی در افغانستان به‌طور رسمی دَری (از ۱۳۴۳ خورشیدی) و در تاجیکستان تاجیکی (از دورهٔ شوروی) خوانده می‌شود.

زبان فارسی از زبان کُهن‌تر پارسی میانه (یا پهلوی) آمده که آن نیز خود از پارسی باستان سرچشمه گرفته است. این دو زبان برخاسته از ناحیهٔ باستانی پارس (استان کرمان و فارس و بوشهر و جنوب یزد امروزی در جنوب ایران) هستند. پارسی باستان زبان رسمی شاهنشاهی هخامنشی بود و نوادهٔ آن، پارسی میانه، به‌عنوان زبان رسمی و دینی شاهنشاهی ساسانی درآمد که در این دوران در دیگر سرزمین‌های ایرانی گسترش بسیاری یافت؛ به گونه‌ای که در خراسان جایگزین زبان‌های پارتی و بلخی شد و بخش‌های بزرگی از خوارزمی‌زبانان و سُغدی‌زبانان در خوارزم و فرارود نیز فارسی‌زبان شدند. گویشی از پارسی میانه که با گذشتِ زمان فارسی دری نام گرفت، پس از اسلام به عنوان گویش معیار نوشتاری در خراسان پا گرفت و در سراسر ایران گسترده شد. گویش‌های دیگر پارسی باستان و پارسی میانه مانند مازندرانی در طبرستان، گیلکی در شمال شرقی جبال، بلوچی در مکران جنوب سیستان، آذری در آذربایجان و قفقاز، لری در لرستان، کهگیلویه و بویراحمد و چهارمحال و بختیاری، و خوزی در خوزستان پا گرفتند که همراه با دری نزدیک به یکدیگرند.

فارسی دری، در طولِ تاریخ، زبانِ فرهنگی و ارجمند امپراتوری‌های پرشماری در آسیای غربی، میانه و جنوبی بوده است. این زبان تأثیرات بزرگی را بر زبان‌های همسایه خویش، از جمله دیگر زبان‌های ایرانی، زبان‌های ترکی (به ویژه ازبکی و آذربایجانی)، ارمنی، گرجی و زبان‌های هندوآریایی (به ویژه اردو) گذاشته است. فارسی بر عربی نیز تأثیر گذاشته و از آن تأثیر پذیرفته است. این زبان حتی در میان کسانی که گویشور بومی آن نبوده‌اند، همانند ترکان عثمانی در امپراتوری عثمانی یا پشتون‌ها در افغانستان، و هند در دوره گورکانیان برای دورانی زبان رسمی دیوان‌سالاری بوده است.

در سال ۱۸۷۲ در نشست ادیبان و زبان‌شناسان اروپایی در برلین، زبان‌های یونانی، فارسی، لاتین و سانسکریت به عنوان زبان‌های کلاسیک جهان برگزیده شدند. بر پایهٔ تعریف، زبانی کلاسیک به‌شمار می‌آید که باستانی و دارای ادبیات پرباری باشد و همچنین در واپسین هزارهٔ زندگانی خود دچار دگرگونی‌های اندکی شده باشد. فارسی از نظر آثار ادبی و شمار و گوناگونی واژگان و همچنین ضرب‌المثل‌ها یکی از غنی‌ترین و پرمایه‌ترین زبان‌های جهان است. از شناخته‌شده‌ترین آثار ادبیات فارسی می‌توان شاهنامه فردوسی، آثار مولوی، رباعیات خیام، پنج گنج نظامی، دیوان حافظ، منطق‌الطیر عطار نیشابوری و گلستان و بوستان سعدی را نام برد.

بر پایهٔ برآوردها، ۷۰ میلیون تن در ایران، ۲۵ میلیون تن در افغانستان، ۹ میلیون تن در تاجیکستان و میان ۱۰ تا ۱۲ میلیون تن در ازبکستان به زبان فارسی دری گفتگو می‌کنند. فارسی همچنین در بحرین، عراق، پاکستان، کویت، امارات متحده عربی، قطر، روسیه، جمهوری آذربایجان، اقلیم کُردستان، قرقیزستان، قزاقستان، ترکمنستان، چین و هند نیز دارای گویشور بومی است.[۱۶][۱۷] با توجه به رسمی بودن فارسی در ایران، افغانستان و تاجیکستان و تسلط گویشوران دیگر زبان‌ها بِدان در کنار زبان بومی خود، روی‌هم‌رفته می‌توان شمار فارسی‌گویان جهان را بیش از ۱۲۰ میلیون تن برآورد کرد. فارسی همچنین هشتمین زبان پرکاربرد در محتوای وب است.'''
ENCODING_POR = '''A língua portuguesa, também designada português, é uma língua indo-europeia românica flexiva ocidental originada no galego-português falado no Reino da Galiza e no norte de Portugal. Com a criação do Reino de Portugal em 1139 e a expansão para o sul na sequência da Reconquista, deu-se a difusão da língua pelas terras conquistadas e, mais tarde, com as descobertas portuguesas, para o Brasil, África e outras partes do mundo.[9] O português foi usado, naquela época, não somente nas cidades conquistadas pelos portugueses, mas também por muitos governantes locais nos seus contatos com outros estrangeiros poderosos. Especialmente nessa altura, a língua portuguesa também influenciou várias línguas.[10]

Durante a Era dos Descobrimentos, marinheiros portugueses levaram o seu idioma para lugares distantes. A exploração foi seguida por tentativas de colonizar novas terras para o Império Português e, como resultado, o português dispersou-se pelo mundo. Brasil e Portugal são os dois únicos países cuja língua primária é o português. É língua oficial em antigas colônias portuguesas, nomeadamente, Moçambique, Angola, Cabo Verde, Guiné Equatorial,[11][12][13] Guiné-Bissau e São Tomé e Príncipe, todas na África.[14] Além disso, por razões históricas, falantes do português, ou de crioulos portugueses, são encontrados também em Macau (China), Timor-Leste, em Damão e Diu, nos estados de Goa (Índia) e Malaca (na Malásia, que conta com utilizadores do crioulo kristáng, ou Língua cristã), em enclaves na ilha das Flores (Indonésia), Baticaloa no (Sri Lanka) e nas ilhas ABC no Caribe.[15][16]

É uma das línguas oficiais da União Europeia, do Mercosul, da União de Nações Sul-Americanas, da Organização dos Estados Americanos, da União Africana e dos Países Lusófonos. Com aproximadamente 300 milhões de falantes, o português é a 5.ª língua mais falada no mundo, a 3.ª mais falada no hemisfério ocidental e a mais falada no hemisfério sul do planeta.[17] O português também é conhecido como "a língua de Camões"[18] (em homenagem a uma das mais conhecidas figuras literárias de Portugal, Luís Vaz de Camões, autor de Os Lusíadas) e "a última flor do Lácio" (expressão usada no soneto Língua Portuguesa, do escritor brasileiro Olavo Bilac).[19][20][21][22][23] Miguel de Cervantes, o célebre autor espanhol, considerava o idioma "doce e agradável".[24] Em março de 2006, o Museu da Língua Portuguesa, um museu interativo sobre o idioma, foi fundado em São Paulo, Brasil, a cidade com o maior número de falantes do português em todo o mundo.[25]

O Dia Internacional da Língua Portuguesa é comemorado em 5 de maio.[26] A data foi instituída em 2009, no âmbito da Comunidade dos Países de Língua Portuguesa (CPLP), com o propósito de promover o sentido de comunidade e de pluralismo dos falantes do português. A comemoração propicia também a discussão de questões idiomáticas e culturais da lusofonia, promovendo a integração entre os povos desses nove países.[27]'''
ENCODING_RON = '''Limba română ([ˈlimba roˈmɨnə]  ( audio) sau românește [romɨˈneʃte]) este limba oficială și principală a României și a Republicii Moldova. Face parte din subramura orientală a limbilor romanice, un grup lingvistic evoluat din diverse dialecte ale latinei vulgare separate de limbile romanice occidentale între secolele V și VIII.[2] Pentru a o distinge în cadrul limbilor romanice orientale, în lingvistica comparată este denumită dacoromână, spre deosebire de cele mai apropiate rude ale sale: aromâna, meglenoromâna și Istroromâna. De asemenea, este vorbită ca limbă minoritară de comunități stabile din țările învecinate României (Bulgaria, Ungaria, Serbia și Ucraina), precum și de marea diasporă românească. În total, este vorbită de aproximativ 25 de milioane de persoane ca limbă maternă.[3]

În România, Constituția din 1991, revizuită în 2003, stipulează în articolul 13 că „În România, limba oficială este limba română”.[4] Aceasta este utilizată în administrația publică, sistemul educațional și în mass-media. De asemenea, în localitățile unde o minoritate națională depășește 20% din populație, autoritățile asigură folosirea limbii respective în raport cu cetățenii, conform legislației în vigoare.[5]

În Republica Moldova, limba română a fost recunoscută oficial prin Declarația de Independență din 1991. Deși Constituția din 1994 menționa „limba moldovenească” ca limbă de stat, în 2013,[6] Curtea Constituțională a decis că Declarația de Independență prevalează, confirmând denumirea de „limba română”.[7] În martie 2023, Parlamentul a adoptat o lege care înlocuiește termenul „limba moldovenească” cu „limba română” în toate textele legislative și în Constituție, lege promulgată ulterior de președintele Maia Sandu.[8][9]

În regiunile din Ucraina cu populație românească semnificativă, precum raioanele din Cernăuți, Odesa și Transcarpatia, limba română este predată în școli ca limbă principală și există publicații, emisiuni TV și radio în limba română.[10] Universitatea din Cernăuți formează profesori pentru școlile românești în domenii precum filologia română, matematică și fizică.

În Serbia, limba română are statut oficial în comunitățile locale din Voivodina, unde există o minoritate românească semnificativă.[11] De asemenea, în Ungaria, limba română este recunoscută ca limbă a minorității române, cu drepturi în educație și cultură.[12]

În Bulgaria, comunitatea românească este concentrată în regiunile de nord-vest, precum Vidin, Vrața și Plevna, însă nu este recunoscută oficial ca minoritate națională, ci doar ca grup etnic.[13] Această nerecunoaștere limitează accesul la educație în limba română în școlile de stat și la servicii religioase în limba maternă.

La nivel internațional, limba română este una dintre limbile oficiale ale Uniunii Europene, România fiind membră din 2007. De asemenea, este utilizată în organizații precum Uniunea Latină și în comunități monahale autonome, cum ar fi Muntele Athos,[14] unde slujbele religioase se desfășoară și în limba română.'''
ENCODING_RUS = '''Русский язык (МФА: [ˈruskʲɪɪ̯ ɪ̯ɪˈzɨk]о файле)[~ 3] — язык восточнославянской группы славянской ветви индоевропейской языковой семьи, национальный язык русского народа. Является одним из наиболее распространённых языков мира — восьмым среди всех языков мира по общей численности говорящих[5] и седьмым по численности владеющих им как родным (2022)[2]. Русский является также самым распространённым славянским языком[8] и самым распространённым языком в Европе — географически и по числу носителей языка как родного[6].

Русский язык — государственный язык Российской Федерации, один из двух государственных языков Беларуси, один из официальных языков Казахстана, Кыргызстана и некоторых других стран, основной язык международного общения в Центральной Евразии, в Восточной Европе, в странах бывшего Советского Союза, один из шести рабочих языков ООН, ЮНЕСКО и других международных организаций[9][10][11]. Согласно Конституции России, русский язык является языком государствообразующего народа России[12].

Число владеющих русским языком в России составляет 137,5 млн человек (2010)[4]. Всего в мире на русском говорят 258,2 млн человек (2022)[5].

Фонологический строй русского языка характеризуется исторически усложнившейся системой консонантизма, включающей 37 согласных фонем, и менее сложной системой вокализма, в которую входят 5 или 6[~ 4] гласных фонем. При этом как в системе гласных, так и в системе согласных отмечается большое разнообразие позиционных видоизменений. В частности, гласные в безударной позиции ослабляются и в ряде случаев не различаются. Ударение в русском языке — динамическое, разноместное и подвижное[13][14].

По морфологическому строю русский язык преимущественно флективный, синтетический. Грамматическое значение лексем передаётся, как правило, с помощью флексий. Каждая флексия обычно выражает одновременно несколько значений. Наряду с синтетическими формами, в русском языке наблюдается также развитие элементов аналитизма[13].

Синтаксис русского языка характеризуется относительно свободным порядком слов, противопоставлением однокомпонентных и двухкомпонентных структур простых предложений, наличием трёх видов сложных предложений, активной ролью интонационных средств[15].

Лексический состав русского языка в своей основе — исконно русский. Средства пополнения словарного фонда — образование слов по собственным моделям и заимствования. К ранним заимствованиям относят церковнославянизмы, грецизмы и тюркизмы. C XVIII века преобладают голландские, немецкие и французские заимствования, с XX века — англицизмы[15].

Диалекты русского языка группируются в два наречия: северное и южное. Между наречиями локализуются переходные среднерусские говоры, ставшие основой современного литературного языка[9].

В истории русского языка выделяют три основных периода: древнерусский, общий для русского, белорусского и украинского языков (VI—XIV веков), старорусский или великорусский (XIV—XVII веков) и период национального русского языка (с середины XVII века)[16]. В основе письменности лежит старославянская кириллица.

Комплекс наук о русском языке называется лингвистической русистикой[9][15].'''
ENCODING_TGK = '''Забони тоҷикӣ (дар солҳои 1989—1991 — забони форсии тоҷикӣ; 1991—1999 – забони тоҷикии форсӣ, дарӣ: زبان تاجیکی) — шакли забони порсӣ буда, дар Тоҷикистон ҳамчун забони давлатӣ мебошад. Ин забон ба хонаводаи забонҳои ҳинду аврупоӣ дохил мешавад. Дар маҷмӯъ: порсигӯёни асил (форсӣ, тоҷикӣ, дарӣ) зиёда аз 122 млн нафар мебошанд. Фақат ба гӯиши тоҷикӣ (бидуни дарӣ) зиёда аз 16 миллион (2022) нафар ҳарф мезананд.

Дар рушди забони тоҷикӣ дар намуди кунуниаш Садриддин Айнӣ саҳми зиёд гузоштааст.


Забони тоҷикӣ ва забони тоҷикии дарӣ (бо ранги сабз) ва дигар забонҳои эронии шарқӣ, ва туркӣ
Забони тоҷикӣ яке аз забонҳои бостонтарини ҷаҳон ба шумор меравад. Давраи нави инкишофи он дар асрҳои VII-VIII оғоз шудааст. Бо ин забон шоирону нависандагони бузург Рӯдакӣ, Фирдавсӣ, Хайём, Сино, Ҷомӣ, Мавлоно, Ҳофиз, Аҳмади Дониш, Айнӣ, Лоҳутӣ, Турсунзода, Пайрав Сулаймонӣ, Абдусалом Деҳотӣ, Убайд Раҷаб, Наимҷон Назирӣ ва дигарон асарҳои безавол эҷод кардаанд.'''
ENCODING_THA = '''ภาษาไทย หรือ ภาษาไทยกลาง เป็นภาษาในกลุ่มภาษาไท สาขาย่อยเชียงแสน ซึ่งเป็นกลุ่มย่อยของตระกูลภาษาขร้า-ไท และเป็นภาษาราชการ และภาษาประจำชาติของประเทศไทย[3][4] มีการสันนิษฐานว่าภาษาในตระกูลนี้มีถิ่นกำเนิดจากทางตอนใต้ของประเทศจีน และนักภาษาศาสตร์บางส่วนเสนอว่า ภาษาไทยน่าจะมีความเชื่อมโยงกับตระกูลภาษาออสโตร-เอเชียติก ตระกูลภาษาออสโตรนีเซียน และตระกูลภาษาจีน-ทิเบต

ภาษาไทยเป็นภาษาที่มีระดับเสียงของคำแน่นอนหรือวรรณยุกต์เช่นเดียวกับภาษาจีน และออกเสียงแยกคำต่อคำ

ภาษาไทยปรากฏครั้งแรกในพุทธศักราช 1826 โดยพ่อขุนรามคำแหง และปรากฏอย่างสากลและใช้ในงานของราชการ เมื่อวันที่ 31 มีนาคม พุทธศักราช 2476 ด้วยการก่อตั้งสำนักงานราชบัณฑิตยสภาขึ้น และปฏิรูปภาษาไทย พุทธศักราช 2485'''
ENCODING_TUR = '''Türkçe ya da Türk dili, Güneydoğu Avrupa ve Batı Asya'da konuşulan, Türk dilleri dil ailesine ait sondan eklemeli bir dildir.[10] Türk dilleri ailesinin Oğuz dilleri grubundan bir Batı Oğuz dili olan Osmanlı Türkçesinin devamını oluşturur. Dil, başta Türkiye olmak üzere Balkanlar, Ege Adaları, Kıbrıs ve Orta Doğu'yu kapsayan eski Osmanlı İmparatorluğu coğrafyasında konuşulur.[10] Ethnologue'a göre Türkçe, yaklaşık 90 milyon konuşanı ile dünyada en çok konuşulan 18. dildir.[11] Türkçe, Türkiye, Kuzey Kıbrıs ve Kıbrıs Cumhuriyeti'nde ulusal resmî dil statüsüne sahiptir.[10]

Türkçe, diğer pek çok Türk dili ile de paylaştığı sondan eklemeli olması ve ünlü uyumu gibi dil bilgisi özellikleri ile karakterize edilir. Dil, tümce yapısı açısından genellikle özne-nesne-yüklem sırasına sahiptir. Almanca, Arapça gibi dillerin aksine gramatik cinsiyetin (erillik, dişilik, cinsiyet ayrımı) bulunmadığı Türkçede, sözcüklerin bir kısmı Arapça, Farsça ve Fransızca gibi yabancı dillerden geçmedir. Ayrıca Azerice, Gagavuzca ve Türkmence gibi diğer Oğuz dilleri ile Türkçe yüksek oranda karşılıklı anlaşılabilirlik gösterir.[12]

Türkçe, 1928'de Atatürk önderliğinde gerçekleştirilmiş Harf Devrimi'nden beri Latin alfabesini temel alan Türk alfabesi ile yazılır. Standart Türkçedeki yazım kuralları, Türk Dil Kurumu tarafından denetlenir. İstanbul Türkçesi olarak da adlandırılan İstanbul ağzı;[13] Türkçenin standart formudur ve Türkçe yazı dili, bu ağzı temel alır. Bununla birlikte Güneydoğu Avrupa ve Orta Doğu'da çeşitli Türkçe şiveleri bulunur ve bu şiveler İstanbul Türkçesi ile çeşitli ses ve dil bilgisi farklılıklarına sahiptir.'''
ENCODING_VIE = '''Tiếng Việt hay tiếng Kinh là một ngôn ngữ thuộc ngữ hệ Nam Á, được công nhận là ngôn ngữ chính thức tại Việt Nam. Đây là tiếng mẹ đẻ của khoảng 85% dân cư Việt Nam cùng với hơn 4 triệu người Việt kiều. Tiếng Việt còn là ngôn ngữ thứ hai của các dân tộc thiểu số tại Việt Nam và là ngôn ngữ dân tộc thiểu số được công nhận tại Cộng hòa Séc.

Dựa trên từ vựng cơ bản, tiếng Việt được phân loại là một ngôn ngữ thuộc ngữ hệ Nam Á. Tiếng Việt là ngôn ngữ có nhiều người nói nhất trong ngữ hệ này (nhiều hơn tổng số người nói của tất cả các ngôn ngữ còn lại trong ngữ hệ). Vì Việt Nam thuộc Vùng văn hoá Đông Á, tiếng Việt cũng chịu nhiều ảnh hưởng về từ tiếng Hán, do vậy là ngôn ngữ có ít điểm tương đồng nhất với các ngôn ngữ khác trong ngữ hệ Nam Á.'''

# Texts
TEXT_AFR = ["Afrikaans is tipologies beskou 'n Indo-Europese, Wes-Germaanse, Nederfrankiese taal,[2] wat aan die suidpunt van Afrika onder invloed van verskeie ander tale en taalgroepe ontstaan het.", ' ', "Afrikaans is op 8 Mei 1925 as 'n amptelike taal van Suid-Afrika erken en is tans die derde jongste Germaanse taal wat amptelike status geniet, naas Faroëes wat in 1948 grondwetlik erken is en Luxemburgs wat hierdie status in 1984 verkry het."]
TEXT_SQI = ['Keto gjuhe kryesisht perdoret në Shqipëri, Kosovë dhe Maqedoninë e Veriut, por edhe në zona të tjera të Evropës Juglindore ku ka një popullsi shqiptare, duke përfshirë Malin e Zi dhe Luginën e Preshevës.', ' ', 'Shqipja është gjuha zyrtare e Shqipërisë dhe Kosovës, gjuhë bashkë-zyrtare e Maqedonisë së Veriut si dhe një nga gjuhët zyrtare e Malit të Zi.']
TEXT_ARA = ['ٱللُّغَةُ ٱلْعَرَبِيَّة هي أكثر اللغات السامية تحدثًا، وإحدى أكثر اللغات انتشاراً في العالم، يتحدثها أكثر من 467 مليون نسمة.(1)', ' ', 'ويتوزع متحدثوها في الوطن العربي، بالإضافة إلى العديد من المناطق الأخرى المجاورة كالأحواز وتركيا وتشاد ومالي والسنغال وإرتيريا وإثيوبيا وجنوب السودان وإيران.']
TEXT_XCL = ['Զգոյշ լերուք ողորմութեան ձերում՝ մի առնել առաջի մարդկան՝ որպէս թե ի ցոյց ինչ նոցա, գուցէ եւ վարձս ոչ ընդունիցիք ի հաւրէ ձերմէ որ յերկինսն է:', ' ', 'Այղ յորժամ առնիցես ողորմութիւն, մի հարկաներ փող առաջի քո. որպէս կեղծաւորքն առնեն ի ժողովուրդս եւ ի հրապարակս. որպէս զի փառաւորեսցին ի մարդկանէ:']
TEXT_HYE = TEXT_HYW = ['Հայերեն (ավանդական՝ հայերէն), հնդեվրոպական լեզվաընտանիքի առանձին ճյուղ հանդիսացող լեզու։', ' ', 'Հայաստանի և Արցախի պետական լեզուն է։']
TEXT_EUS = ['Euskara Euskal Herriko hizkuntza da.[8]', ' ', 'Hizkuntza bakartua da, ez baitzaio ahaidetasunik aurkitu.']
TEXT_BEL = ['Белару́ская мо́ва — нацыянальная мова беларусаў, уваходзіць у індаеўрапейскую моўную сям’ю, славянскую групу, усходнеславянскую падгрупу.', ' ', 'Пашырана ў асноўным у Беларусі.']
TEXT_BUL = ['Бъ̀лгарският езѝк е индоевропейски език от групата на южнославянските езици, като образува неговата източна подгрупа.', ' ', 'Той е официалният език на Република България и един от 24-те официални езика на Европейския съюз.']
TEXT_MYA = ['မြန်မာဘာသာ (အင်္ဂလိပ်: Myanmar Language)သည် မြန်မာနိုင်ငံ၏ ရုံးသုံး ဘာသာစကားဖြစ်သည။', ' ', 'ဗမာလူမျိုးနှင့် ဗမာနွယ်ဝင်(ဓနု၊ အင်းသား၊ တောင်ရိုးနှင့် ယော)တို့၏ ဇာတိစကားဖြစ်သည်။']
TEXT_BXR = ['Буряад хэлэн (буряад-монгол хэлэн) Алтайн хэлэнэй изагуурай буряад арад түмэнһөө хэрэглэгдэжэ бай монгол хэлэнэй бүлэгэй xэлэн-аялгуу юм.', ' ', 'Бүгэдэ Найрамдаха Буряад Улас, Эрхүү можо, Забайкалиин хизаар, Усть-Ордын болон Агын тойрогууд, мүн Монгол Уласай хойто аймагууд, Хитадай зүүн-хойто орондо ажаһуудаг буряадууд хэлэлсэдэг.']
TEXT_CAT = ['Hi ha altres glotònims tradicionals que es fan servir com a sinònim de "català" al llarg del domini lingüístic.', ' ', "Així, per exemple, a l'Alguer se li diu alguerès, a Fraga, fragatí, a Maella, maellà i a la comarca de la Llitera, lliterà."]
TEXT_LZH = ['文言者，華夏、四裔所以書其言，而述志表情也。', '先民言語，傳乎口耳，至結繩以記，事日贅，是結繩之不足，求諸繪圖，繪圖猶逾，而創字製文，金石竹帛載之，自劉漢而書諸紙。']
TEXT_ZHO_CN = ['汉语又称华语[6][7]，是来自汉民族的语言[8][7][9]。', '汉语是汉藏语系中最大的一支语族，若把整个汉语族视为单一语言，则汉语为世界上母语使用者人数最多的语言，目前全世界有五分之一人口将其作为母语或第二语言。']
TEXT_ZHO_TW = ['漢語又稱華語[6][7]，是來自漢民族的語言[8][7][9]。', '漢語是漢藏語系中最大的一支語族，若把整個漢語族視為單一語言，則漢語為世界上母語使用者人數最多的語言，目前全世界有五分之一人口將其作為母語或第二語言。']
TEXT_CHU = ['ВЪ И҃ В҃ ДЬНЬ КЛꙆМЕНТА', ' ', 'Бъ҃ ꙇже нъи лѣта огрѧдѫцѣ блаженаго климента мѫченіка твоего ꙇ папежа чьстьѭ веселішꙇ подазь мілостівъі да егоже чьсть чьстімъ сілоѭ ѹбо мѫчениѣ его наслѣдѹемъ г҃мь']
TEXT_COP = ['ϭⲟⲗ ·', ' ', 'ⲛⲉⲛⲧⲁⲩⲕⲗⲏⲣⲟⲛⲟⲙⲉⲓ ⲉⲛⲉϩ ⲛⲧⲙⲛⲧⲣⲣⲟ ⲙⲡⲛⲟⲩⲧⲉ ·']
TEXT_HRV = ['Hrvatski jezik obuhvaća govoreni i pisani hrvatski standardni jezik i sve narodne govore kojima govore i pišu Hrvati.[4]', ' ', 'Povijesno, obuhvaća sve govore i sve književne jezike izgrađene na tim govorima, kojima su se služili Hrvati.[5][6]']
TEXT_CES = ['Čeština neboli český jazyk je západoslovanský jazyk, nejbližší slovenštině, poté lužické srbštině a polštině.', ' ', 'Patří mezi slovanské jazyky, do rodiny jazyků indoevropských.']
TEXT_DAN = ['Dansk er et østnordisk sprog indenfor den germanske gren af den indoeuropæiske sprogfamilie.', ' ', 'Det danske sprog tales af ca. seks millioner mennesker, hovedsageligt i Danmark, men også i Sydslesvig, på Færøerne og Grønland.[1]']
TEXT_NLD = ['Het Nederlands is een West-Germaanse taal, de meest gebruikte taal in Nederland en België, de officiële taal van Suriname en een van de drie officiële talen van België.', ' ', 'Binnen het Koninkrijk der Nederlanden is het Nederlands ook een officiële taal van Aruba, Curaçao en Sint-Maarten.']
TEXT_ANG = ['Ænglisc geþeode bið Westgermanisc geþeode on hwelc spræcon Engle swelce of 450 oþ 1150 gear.', ' ', 'Ænglisc boccræft ætiewde on seofoþe gearhundred.']
TEXT_ENG_GB = TEXT_ENG_US = ['English is a West Germanic language in the Indo-European language family, whose speakers, called Anglophones, originated in early medieval England on the island of Great Britain.[4][5][6]', ' ', 'The namesake of the language is the Angles, one of the Germanic peoples that migrated to Britain after its Roman occupiers left.']
TEXT_MYV = ['Э́рзянь кель те уралонь кель, кона совавтови суоми-угрань келень семиянть суоминь-равонь тарадонтень.', ' ', 'Эрзянь кельсэ кортыть эрзят.']
TEXT_EST = ['Eesti keel (varasem nimetus maakeel) on läänemeresoome lõunarühma kuuluv keel.', ' ', 'Eesti keel on Eesti riigikeel ja 2004. aastast ka üks Euroopa Liidu ametlikke keeli.']
TEXT_FAO = ['Føroyskt er høvuðsmálið í Føroyum.', ' ', 'Føroyskt er almenna málið í Føroyum, og tað er tjóðarmál føroyinga.']
TEXT_FIN = ['Suomen kieli eli suomi on uralilaisten kielten itämerensuomalaiseen ryhmään kuuluva kieli, jota puhuvat pääosin suomalaiset.', ' ', 'Suomessa suomen kieltä puhuu äidinkielenään 4,8 miljoonaa ja toisena kielenään 0,5 miljoonaa ihmistä.']
TEXT_FRA = ['Le français est une langue indo-européenne de la famille des langues romanes dont les locuteurs sont appelés « francophones ».', ' ', "Il est la cinquième langue parlée au monde après l'anglais, le mandarin, le hindi et l'espagnol."]
TEXT_FRO = ["Si l'orrat Carles, ki est as porz passant.", ' ', 'Je vos plevis, ja returnerunt Franc.']
TEXT_GLG = ['O galego ([ɡaˈleɣo̝][1]) é unha lingua indoeuropea que pertence á póla de linguas románicas.', ' ', 'É a lingua propia de Galicia,[5] onde é falada por uns 2,4 millóns de galegos.[6]']
TEXT_KAT = ['ქართული ენა — ქართველურ ენათა ოჯახის ენა.', ' ', 'ქართველების მშობლიური ენა, საქართველოს სახელმწიფო ენა (აფხაზეთის ავტონომიურ რესპუბლიკაში, მასთან ერთად სახელმწიფო ენად აღიარებულია აფხაზური ენა).']
TEXT_DEU_AT = TEXT_DEU_DE = TEXT_DEU_CH = ['Die deutsche Sprache oder Deutsch [dɔɪ̯tʃ][24] ist eine westgermanische Sprache, die weltweit etwa 90 bis 105 Millionen Menschen als Muttersprache und weiteren rund 80 Millionen als Zweit- oder Fremdsprache dient.', ' ', 'Das Deutsche ist eine plurizentrische Sprache, enthält also mehrere Standardvarietäten in verschiedenen Regionen.']
TEXT_NDS = ['Plattdüütsch, kort Platt, ook Nedderdüütsch oder Neddersassisch heten, is ene Regionaalspraak un Dialektgrupp, de rund 2 Minschen in Noorddüütschland un an de 2 Millionen Minschen in Oostnedderland snackt.', ' ', 'Besünners mit dat mennistsche Plautdietsch het sik de Spraak ook weltwied uutbreidt.']
TEXT_GOT = ['𐌲𐌿𐍄𐌰𐍂𐌰𐌶𐌳𐌰, 𐌲𐌿𐍄𐍂𐌰𐌶𐌳𐌰 𐌰𐌹𐌸𐌸𐌰𐌿 𐌲𐌿𐍄𐌹𐍃𐌺𐌰 𐍂𐌰𐌶𐌳𐌰 𐌹𐍃𐍄 𐌲𐌰𐍃𐍅𐌿𐌻𐍄𐌰𐌽𐌰 𐌰𐌿𐍃𐍄𐍂𐌰𐌲𐌰𐌹𐍂𐌼𐌰𐌽𐌹𐍃𐌺𐌰 𐍂𐌰𐌶𐌳𐌰 𐍂𐍉𐌳𐌹𐌳𐌰 𐍆𐍂𐌰𐌼 𐌲𐌿𐍄𐌰𐌼.', ' ', '𐍃𐌹 𐌹𐍃𐍄 𐌰𐌹𐌽𐌰𐌷𐍉 𐌰𐌿𐍃𐍄𐍂𐌰𐌲𐌰𐌹𐍂𐌼𐌰𐌽𐌹𐍃𐌺𐌰 𐍂𐌰𐌶𐌳𐌰 𐍃𐍉𐌴𐌹 𐌷𐌰𐌱𐌰𐌹𐌸 𐌲𐌰𐌼𐌴𐌻𐌴𐌹𐌽𐌹𐌽𐍃.']
TEXT_GRC = ['ἦλθον δὲ οἱ δύο ἄγγελοι εἰς Σόδομα ἑσπέρας· Λὼτ δὲ ἐκάθητο παρὰ τὴν πύλην Σοδόμων. ἰδὼν δὲ Λὼτ ἐξανέστη εἰς συνάντησιν αὐτοῖς καὶ προσεκύνησεν τῷ προσώπῳ ἐπὶ τὴν γῆν', ' ', 'καὶ εἶπεν, ἰδού, κύριοι, ἐκκλίνατε εἰς τὸν οἶκον τοῦ παιδὸς ὑμῶν καὶ καταλύσατε καὶ νίψασθε τοὺς πόδας ὑμῶν, καὶ ὀρθρίσαντες ἀπελεύσεσθε εἰς τὴν ὁδὸν ὑμῶν. εἶπαν δέ, οὐχί, ἀλλ᾿ ἐν τῇ πλατείᾳ καταλύσομεν.']
TEXT_ELL = ['Η ελληνική γλώσσα ανήκει στην ινδοευρωπαϊκή οικογένεια[9] secεπίσης στο βαλκανικό γλωσσικό δεσμό.', ' ', 'ελληνική γλώσσα, έχουμε γραπτά κείμενα ήδη από τον 15ο αιώνα π.Χ..']
TEXT_HBO = ['וַ֠יָּבֹאוּ שְׁנֵ֨י הַמַּלְאָכִ֤ים סְדֹ֨מָה֙ בָּעֶ֔רֶב וְלֹ֖וט יֹשֵׁ֣ב בְּשַֽׁעַר־סְדֹ֑ם וַיַּרְא־לֹוט֙ וַיָּ֣קָם לִקְרָאתָ֔ם וַיִּשְׁתַּ֥חוּ אַפַּ֖יִם אָֽרְצָה׃', ' ', 'וַיֹּ֜אמֶר הִנֶּ֣ה נָּא־אֲדֹנַ֗י ס֣וּרוּ נָ֠א אֶל־בֵּ֨ית עַבְדְּכֶ֤ם וְלִ֨ינוּ֙ וְרַחֲצ֣וּ רַגְלֵיכֶ֔ם וְהִשְׁכַּמְתֶּ֖ם וַהְלַכְתֶּ֣ם לְדַרְכְּכֶ֑ם וַיֹּאמְר֣וּ לֹּ֔א כִּ֥י בָרְחֹ֖וב נָלִֽין׃']
TEXT_HEB = ['עִבְרִית היא שפה שמית, ממשפחת השפות האפרו-אסייתיות, הידועה כשפתם של היהודים ושל השומרונים.', ' ', 'היא שייכת למשפחת השפות הכנעניות והשפה הכנענית היחידה המדוברת כיום.']
TEXT_HIN = ['हिन्दी या आधुनिक मानक हिन्दी विश्व की एक प्रमुख भाषा है और भारत की एक राजभाषा है।', ' ', 'केन्द्रीय स्तर पर भारत में सह-आधिकारिक भाषा अंग्रेज़ी है।']
TEXT_HUN = ['A magyar nyelv az uráli nyelvcsalád tagja, azon belül a finnugor nyelvek közé tartozó ugor nyelvek egyike.', ' ', 'Legközelebbi rokonai a manysi és a hanti nyelv, majd utánuk az udmurt, a komi, a mari és a mordvin nyelvek.']
TEXT_ISL = ['Íslenska er vesturnorrænt, germanskt og indóevrópskt tungumál sem er einkum talað og ritað á Íslandi og er móðurmál langflestra Íslendinga.[6]', ' ', 'Það hefur tekið minni breytingum frá fornnorrænu en önnur norræn mál[6] og er skyldara norsku og færeysku en sænsku og dönsku.[3][4]']
TEXT_IND = ['Bahasa Indonesia ([baˈhasa indoˈnesija]) merupakan bahasa resmi sekaligus bahasa nasional di Indonesia.[16]', ' ', 'Bahasa Indonesia merupakan varietas yang dibakukan dari bahasa Melayu,[17] sebuah bahasa rumpun Austronesia yang digolongkan ke dalam rumpun Melayik yang sendirinya merupakan cabang turunan dari cabang Melayu-Polinesia.']
TEXT_GLE = ['Labhraítear in Éirinn go príomha í, ach tá cainteoirí Gaeilge ina gcónaí in áiteanna eile ar fud an domhain.', ' ', 'Is í an teanga náisiúnta nó dhúchais agus an phríomhtheanga oifigiúil i bPoblacht na hÉireann í an Ghaeilge.']
TEXT_ITA = ["L'italiano è una lingua romanza parlata principalmente in Italia.", ' ', "Per ragioni storiche e geografiche, l'italiano è la lingua romanza meno divergente dal latino (complessivamente a pari merito, anche se in parametri diversi, con la lingua sarda).[2][3][4][5]"]
TEXT_JPN = ['日本語（にほんご、にっぽんご[注釈 3]）は、日本国内や、かつての日本領だった国、そして国外移民や移住者を含む日本人同士の間で使用されている言語。', '日本は法令によって公用語を規定していないが、法令その他の公用文は全て日本語で記述され、各種法令[注釈 4]において日本語を用いることが規定され、学校教育においては「国語」の教科として学習を行うなど、事実上日本国内において唯一の公用語となっている。']
TEXT_KAZ = ['Қазақ тілі (төте: قازاق ٴتىلى‎, латын: qazaq tılı) — Қазақстан Республикасының мемлекеттік тілі, сонымен қатар Ресей, Өзбекстан, Қытай, Моңғолия жəне т.б. елдерде тұратын қазақтардың ана тілі.', ' ', 'Қазақ тілі түркі тілдерінің қыпшақ тобына, соның ішінде қарақалпақ, ноғай, қарашай тілдерімен бірге қыпшақ-ноғай тармағына жатады.']
TEXT_KHM = ['ភាសាខ្មែរ គឺជាភាសាកំណើតរបស់ជនជាតិខ្មែរនិងជាភាសាផ្លូវការរបស់ប្រទេសកម្ពុជា។', ' ', 'ភាសាសំស្ក្រឹតនិងភាសាបាលីបានជួយបង្កើតខេមរភាសា ព្រោះភាសាខ្មែរបានខ្ចីពាក្យច្រើនពីភាសាទាំងពីរនេះ។']
TEXT_KPV = ['Коми кыв — финн-йӧгра кывъясысь ӧти, коми войтырлӧн чужан кыв. Коми кывйын кызь гӧгӧр сёрнисикас да кык гижӧда кыв: зырян коми да перым коми.', ' ', 'Коми кыв — Коми Республикаын каналан кыв (кыдзи и роч кыв).']
TEXT_KOR = ['한국어(韓國語), 조선어(朝鮮語)는 대한민국과 조선민주주의인민공화국의 공용어이다.', ' ', '둘은 표기나 문법, 동사 어미나 표현에서 약간의 차이가 있다.']
TEXT_KMR = ['Kurmancî, kurdiya jorîn yan jî kurdiya bakurî yek ji zaravayên zimanê kurdî ye ku ji aliyê kurdan ve tê axaftin.', ' ', 'Zaravayê kurmancî zimanê herî berfireh ê Kurdistanê ye ku li her çar parçeyên Kurdistanê bi awayekî berfireh tê axavtin.']
TEXT_KIR = ['Кыргыз тили — Кыргыз Республикасынын мамлекеттик тили, түрк тилдери курамына, анын ичинде кыргыз-кыпчак же тоо-алтай тобуна кирет.', ' ', 'Кыргыз Республикасынын түптүү калкынын, Кытайдагы, Өзбекстан, Тажикстан Республикасында Ооганстан, Түркия, Орусияда жашап жаткан кыргыздардын эне тили.']
TEXT_LAO = ['ພາສາລາວສືບທອດມາຈາກພາສາຕະກຸນໄຕ-ກະໄດ ຢູ່ພາກໃຕ້ຂອງປະເທດຈີນ ເຊິ່ງເປັນຈຸດເດີມຂອງຫຼາຍພາສາໃນຕະກຸນນີ້ທີ່ຍັງຖືກໃຊ້ ແລະ ຖືກເວົ້າຢູ່ໂດຍຫຼາຍຊົນເຜົ່າໃນປັດຈຸບັນ.', ' ', 'ເນື່ອງຈາກຖືກຄວາມກົດດັນຈາກການຂະຫຍາຍຕົວຂອງອານາຈັກຈີນ, ການບຸກຮຸກຮານຂອງຊາວມົງໂກລີ ແລະ ການປູກຝັງທຳມາຫາກິນ, ຄົນໄຕ (ໄທ) ໄດ້ຍົກຍ້າຍລົງມາທາງໃຕ້ກະຈາຍໄປຕາມແຫຼ່ງທໍາມາຫາກິນທີ່ເໝາະສົມກັບຕົນ.']
TEXT_LAT = ['Latīnum, lingua Latīna,[1] sive sermō Latīnus,[2] est lingua Indoeuropaea qua primum Latini universi et Romani antiqui in primis loquebantur quamobrem interdum etiam lingua Latia[3] (in Latio enim sueta) et lingua Rōmāna[4] (nam imperii Romani sermo sollemnis) appellabatur.', ' ', 'Nomen linguae ductum est a terra quam gentes Latine loquentes incolebant, Latium vetus interdum appellata, in paeninsula Italica inter Tiberim, Volscos, Appenninum, et mare Inferum sita.']
TEXT_LAV = ['Latviešu valoda ir dzimtā valoda apmēram 1,5 miljoniem cilvēku, galvenokārt Latvijā, kur tā ir vienīgā valsts valoda.[1][3]', ' ', 'Lielākās latviešu valodas pratēju kopienas ārpus Latvijas ir Apvienotajā Karalistē, ASV, Īrijā, Austrālijā, Vācijā, Zviedrijā, Kanādā, Brazīlijā, Krievijas Federācijā. Latviešu valoda pieder pie indoeiropiešu valodu saimes baltu valodu grupas.']
TEXT_LIJ = ["E variante ciù importanti son o zeneize, o savoneize, o spezzin, o ventemigliusu, o tabarchin, o monegasco, e o noveize, dîto ascî lìgure d'Otrazôvo.", ' ', "Tra i dialetti Liguri e o Piemonteise ciù a nord, gh'è poi de variante dite de tranxission, comme i dialetti da val Bormia, de Calissan e do Sascello."]
TEXT_LIT = ['Lietuvių kalba – iš baltų prokalbės kilusi lietuvių tautos kalba, kuri Lietuvoje yra valstybinė, o Europos Sąjungoje – viena iš oficialiųjų kalbų.', ' ', 'Lietuviškai kalba apie tris milijonus žmonių (dauguma jų gyvena Lietuvoje).']
TEXT_MKD = ['Македонски јазик — јужнословенски јазик, дел од групата словенски јазици од јазичното семејство на индоевропски јазици.', ' ', 'Македонскиот е службен и национален јазик во Македонија, а воедно е и официјално признат како регионален службен јазик во Горица и Пустец во Албанија каде што живее бројно македонско население, но и во Србија како официјален во општините Јабука и Пландиште, Романија и Косово.']
TEXT_MAL = ['ഇതു ദ്രാവിഡ ഭാഷാ കുടുംബത്തിൽപ്പെടുന്നു.', ' ', 'ഇന്ത്യയിൽ ശ്രേഷ്ഠഭാഷാ പദവി ലഭിക്കുന്ന അഞ്ചാമത്തെ ഭാഷയാണ് മലയാളം[5].']
TEXT_MLT = ["Il-Malti huwa l-ilsien nazzjonali tar-Repubblika ta' Malta.", ' ', "Huwa l-ilsien uffiċjali flimkien mal-Ingliż; kif ukoll wieħed mill-ilsna uffiċjali u l-uniku wieħed ta' oriġini Għarbija (Semitiku) tal-Unjoni Ewropea."]
TEXT_GLV = ['She Gaelg (graït: /gɪlg/) çhengey Ghaelagh Vannin.', ' ', "Haink y Ghaelg woish Shenn-Yernish, as t'ee cosoylagh rish Yernish as Gaelg ny h-Albey."]
TEXT_MAR = ['मराठी भाषा ही इंडो-युरोपीय भाषाकुळातील एक भाषा आहे.', ' ', 'मराठी ही भारताच्या २२ अधिकृत भाषांपैकी एक आहे.']
TEXT_PCM = ['Naijá langwej na popula langwej for Naija an pipul wey dey spik am for Naijá pas 75 miliọn.', ' ', 'Naijá na pijin, a langwej for oda langwej. Naijá for Inglish an wey Afrikan langwej.']
TEXT_NOB = ['Bokmål er en av to offisielle målformer av norsk skriftspråk, hvorav den andre er nynorsk.', ' ', 'I skrift har 87,3 % bokmål som hovedmål i skolen.[3]']
TEXT_NNO = ['Nynorsk, før 1929 offisielt kalla landsmål, er sidan jamstillingsvedtaket av 12. mai 1885 ei av dei to offisielle målformene av norsk; den andre forma er bokmål.', ' ', 'Nynorsk vert i dag nytta av om lag 10–15% av innbyggjarane i Noreg.[1][2]']
TEXT_FAS = ['فارسی یا پارسی یکی از زبان‌های ایرانی غربی از زیرگروه ایرانی شاخهٔ هندوایرانیِ خانوادهٔ زبان‌های هندواروپایی است که در کشورهای ایران، افغانستان، تاجیکستان، ازبکستان، پاکستان، عراق، ترکمنستان و آذربایجان به آن سخن می‌گویند.', ' ', 'فارسی زبان چندکانونی و فراقومی است و زبان رسمی ایران، تاجیکستان و افغانستان به‌شمار می‌رود.']
TEXT_POL = ['Język polski, polszczyzna – język lechicki z grupy zachodniosłowiańskiej (do której należą również czeski, kaszubski, słowacki, języki łużyckie czy wymarły język drzewiański), stanowiącej część rodziny indoeuropejskiej.', ' ', 'Jest językiem urzędowym w Polsce oraz należy do oficjalnych języków Unii Europejskiej.']
TEXT_QPM = ['Kážyjte nǽko, de!', ' ', 'Še go preskókneme!']
TEXT_POR_BR = TEXT_POR_PT = ['A língua portuguesa, também designada português, é uma língua indo-europeia românica flexiva ocidental originada no galego-português falado no Reino da Galiza e no norte de Portugal.', ' ', 'Com a criação do Reino de Portugal em 1139 e a expansão para o sul na sequência da Reconquista, deu-se a difusão da língua pelas terras conquistadas e, mais tarde, com as descobertas portuguesas, para o Brasil, África e outras partes do mundo.[9]']
TEXT_RON = ['Limba română ([ˈlimba roˈmɨnə]  ( audio) sau românește [romɨˈneʃte]) este limba oficială și principală a României și a Republicii Moldova.', ' ', 'Face parte din subramura orientală a limbilor romanice, un grup lingvistic evoluat din diverse dialecte ale latinei vulgare separate de limbile romanice occidentale între secolele V și VIII.[2]']
TEXT_RUS = ['Русский язык (МФА: [ˈruskʲɪɪ̯ ɪ̯ɪˈzɨk]о файле)[~ 3] — язык восточнославянской группы славянской ветви индоевропейской языковой семьи, национальный язык русского народа.', ' ', 'Является одним из наиболее распространённых языков мира — восьмым среди всех языков мира по общей численности говорящих[5] и седьмым по численности владеющих им как родным (2022)[2].']
TEXT_ORV = ['шаибатъ же ѿ бедерѧ г҃ мсци', ' ', 'а ѿ дабылѧ до шаибата в҃ мсца моремъ итьти']
TEXT_SME = ['Davvisámegiella gullá sámegielaid oarjesámegielaid davvejovkui ovttas julev- ja bihtánsámegielain.', ' ', 'Eará oarjesámegielat leat ubmisámegiella ja lullisámegiella.']
TEXT_SAN = ['संस्कृतं जगत एकतमातिप्राचीना समृद्धा शास्त्रीया च भाषासु वर्तते।', ' ', 'संस्कृतं भारतस्य जगतो वा भाषास्वेकतमा‌ प्राचीनतमा।']
TEXT_GLA = ["'S i cànan dùthchasach na h-Alba a th' anns a' Ghàidhlig.", ' ', "'S i ball den teaghlach de chànanan Ceilteach dhen mheur Ghoidhealach a tha anns a' Ghàidhlig."]
TEXT_SRP_CYRL = ['Српски језик припада словенској групи језика породице индоевропских језика.[12]', ' ', 'Српски језик је званичан у Србији, Босни и Херцеговини и Црној Гори и говори га око 12 милиона људи.[13]']
TEXT_SRP_LATN = ['Srpski jezik pripada slovenskoj grupi jezika porodice indoevropskih jezika.[12]', ' ', 'Srpski jezik je zvaničan u Srbiji, Bosni i Hercegovini i Crnoj Gori i govori ga oko 12 miliona ljudi.[13]']
TEXT_SND = ['سنڌي (/ˈsɪndi/[6]सिन्धी, Sindhi)ھڪ ھند-آريائي ٻولي آھي جيڪا سنڌ جي تاريخي خطي ۾ سنڌي ماڻھن پاران ڳالھائي وڃي ٿي.', ' ', 'سنڌي پاڪستان جي صوبي سنڌ جي سرڪاري ٻولي آھي.[7][8][9]']
TEXT_SLK = ['Slovenčina patrí do skupiny západoslovanských jazykov (spolu s češtinou, poľštinou, hornou a dolnou lužickou srbčinou a kašubčinou).', ' ', 'Slovenčina je oficiálne úradným jazykom Slovenska, Vojvodiny a od 1. mája 2004 jedným z jazykov Európskej únie.']
TEXT_SLV = ['Slovenščina [sloˈʋenʃtʃina] je združeni naziv za uradni knjižni jezik Slovencev in skupno ime za narečja in govore, ki jih govorijo ali so jih nekoč govorili Slovenci.', ' ', 'Govori ga okoli 2,5 (dva in pol) milijona govorcev po svetu, od katerih jih večina živi v Sloveniji.']
TEXT_DSB = ['Dolnoserbšćina gromaźe z górnoserbšćinu słušatej k kupce serbskeju rěcowu w ramiku pódwjacornosłowjańskich rěcy.', ' ', 'Licba powědajucych dolnoserbski wucynijo něnto wokoło 7000 luźi.']
TEXT_HSB = ['Hornjoserbšćina je zapadosłowjanska rěč, kotraž so w Hornjej Łužicy wokoło městow Budyšin, Kamjenc a Wojerecy rěči.', ' ', 'Wona je přiwuzna z delnjoserbšćinu w susodnej Delnjej Łužicy, čěšćinu, pólšćinu, słowakšćinu a kašubšćinu.']
TEXT_SPA = ['El español o castellano es una lengua romance procedente del latín hablado, perteneciente a la familia de lenguas indoeuropeas.', ' ', 'Forma parte del grupo ibérico y es originaria de Castilla, reino medieval de la península ibérica.']
TEXT_SWE = ['Svenska (svenska (fil)) är ett östnordiskt språk som talas av ungefär tio miljoner personer, främst i Sverige där språket har en dominant ställning som huvudspråk, men även som det ena nationalspråket i Finland och som enda officiella språk på Åland.', ' ', 'I övriga Finland talas det som modersmål framförallt i de finlandssvenska kustområdena i Österbotten, Åboland och Nyland.']
TEXT_TAM = ['தமிழ் (Tamil language) தமிழர்களினதும் தமிழ் பேசும் பலரின் தாய்மொழி ஆகும்.', ' ', 'தமிழ், உலகில் உள்ள முதன்மையான மொழிகளில் ஒன்றும் செம்மொழியும் ஆகும்.']
TEXT_TEL = ['తెలుగు ఆంధ్ర, తెలంగాణ రాష్ట్రాలలో మున్నధికారిక నుడి.', ' ', 'ఇది ద్రావిడ కుటుంబానికి చెందిన నుడి.']
TEXT_THA = ['ภาษาไทย หรือ ภาษาไทยกลาง เป็นภาษาในกลุ่มภาษาไท สาขาย่อยเชียงแสน ซึ่งเป็นกลุ่มย่อยของตระกูลภาษาขร้า-ไท และเป็นภาษาราชการ และภาษาประจำชาติของประเทศไทย[3][4]', ' ', 'มีการสันนิษฐานว่าภาษาในตระกูลนี้มีถิ่นกำเนิดจากทางตอนใต้ของประเทศจีน และนักภาษาศาสตร์บางส่วนเสนอว่า ภาษาไทยน่าจะมีความเชื่อมโยงกับตระกูลภาษาออสโตร-เอเชียติก ตระกูลภาษาออสโตรนีเซียน และตระกูลภาษาจีน-ทิเบต']
TEXT_BOD = ['བོད་ཀྱི་སྐད་ཡིག་ནི་བོད་ཡུལ་དང་ཉེ་འཁོར་གྱི་ས་ཁུལ་བལ་ཡུལ། འབྲུག་དང་འབྲས་ལྗོངས། ལ་དྭགས་ནས་ལྷོ་མོན་རོང་སོགས་སུ་བེད་སྤྱོད་བྱེད་པའི་སྐད་ཡིག་དེ།', ' ', 'ད་ཆར་ཡོངས་གྲགས་སུ་བོད་ཀྱི་ཡུལ་གྲུ་སྟོད་སྨད་བར་གསུམ་ལ་ལྟོས་ཏེ་ནང་གསེས་རིགས་གསུམ་དུ་ཕྱེ་བ་སྟེ། སྟོད་དབུས་གཙང་གི་སྐད་དང་། བར་ཁམས་པའི་སྐད་དང་། སྨད་ཨ་མདོའི་སྐད་རྣམས་སོ།']
TEXT_TUR = ["Türkçe ya da Türk dili, Güneydoğu Avrupa ve Batı Asya'da konuşulan, Türk dilleri dil ailesine ait sondan eklemeli bir dildir.[10]", ' ', 'Türk dilleri ailesinin Oğuz dilleri grubundan bir Batı Oğuz dili olan Osmanlı Türkçesinin devamını oluşturur.']
TEXT_OTA = ['Musahabeme nihayet vermeden evvel edebiyat-ı hazıra-ı ricalden ziyade edebiyat-ı nisvanın bir feyz-i latife mazhar olduğunu söylemek isterim .', ' ', 'En başında Halide Salih Hanımefendi olduğu hâlde Nesl-i Cedid Edibelerinin ateşîn musahebelerini , rengîn mensur şiirlerini , teşrih-i ruha dair küçük hikâyelerini okudum .']
TEXT_UKR = ['Украї́нська мо́ва (МФА: [ʊkrɐˈjinʲsʲkɐ ˈmɔʋɐ], історична назва — ру́ська[10][11][12][* 1]) — національна мова українців.', ' ', "Належить до східнослов'янської групи слов'янських мов, що входять до індоєвропейської мовної сім'ї, поряд із романськими, германськими, кельтськими, грецькою, албанською, вірменською та найближче спорідненими зі слов'янськими балтійськими мовами[13][14][* 2]."]
TEXT_URD = ['اُردُو، برصغیر پاک و ہند کی معیاری زبانوں میں سے ایک ہے۔', ' ', 'یہ پاکستان کی قومی اور رابطہ عامہ کی زبان ہے، جبکہ بھارت کی چھ ریاستوں کی دفتری زبان کا درجہ رکھتی ہے۔']
TEXT_UIG = ['ئۇيغۇر تىلى ئۇيغۇر جۇڭگو شىنجاڭ ئۇيغۇر ئاپتونوم رايونىنىڭ ئېيتقان بىر تۈركىي تىلى.', ' ', 'ئۇ ئۇزاق ئەسىرلىك تەرەققىيات داۋامىدا قەدىمكى تۈركىي تىللار دەۋرى، ئورخۇن ئۇيغۇر تىلى دەۋرى، ئىدىقۇت-خاقانىيە ئۇيغۇر تىلى دەۋرى، چاغاتاي ئۇيغۇر تىلى دەۋرىنى بېسىپ ئۆتكەن.']
TEXT_VIE = ['Tiếng Việt hay tiếng Kinh là một ngôn ngữ thuộc ngữ hệ Nam Á, được công nhận là ngôn ngữ chính thức tại Việt Nam.', ' ', 'Đây là tiếng mẹ đẻ của khoảng 85% dân cư Việt Nam cùng với hơn 4 triệu người Việt kiều.']
TEXT_CYM = ["Aelod o'r gangen Frythonaidd o'r ieithoedd Celtaidd a siaredir yn frodorol yng Nghymru, gan Gymry a phobl eraill ar wasgar yn Lloegr, a chan gymuned fechan yn Y Wladfa, yr Ariannin[8] yw'r Gymraeg (hefyd Cymraeg heb y fannod).", ' ', 'Yng Nghyfrifiad y DU (2011), darganfuwyd bod 19% (562,000) o breswylwyr Cymru (tair blwydd a throsodd) yn gallu siarad Cymraeg.']
TEXT_WOL = ['Wolof làkk la wu ñuy wax ci Gàmbi (Gàmbi Wolof), Gànnaar (Gànnaar Wolof), ak Senegaal (Senegaal Wolof).', ' ', 'Mi ngi bokk nag moom wolof ci bànqaasub atlas bu làkki Kongóo yu kojug nit ñu ñuul ñi.']
TEXT_OTHER = TEXT_ENG_US

# Sentences
SENTENCE_AFR = TEXT_AFR[0]
SENTENCE_SQI = TEXT_SQI[0]
SENTENCE_AMH = 'አማርኛ[1] ፡ የኢትዮጵያ ፡ መደበኛ ፡ ቋንቋ ፡ ነው ።'
SENTENCE_ARA = TEXT_ARA[0]
SENTENCE_XCL = TEXT_XCL[0]
SENTENCE_HYE = SENTENCE_HYW = TEXT_HYE[0]
SENTENCE_ASM = 'অসমীয়া ভাষা (ইংৰাজী: Assamese language) হৈছে সকলোতকৈ পূৰ্বীয় ভাৰতীয়-আৰ্য ভাষা তথা অসমৰ ৰাজ্যিক ভাষা।'
SENTENCE_AST = "L'asturianu ye una llingua romance propia d'Asturies,[1] perteneciente al subgrupu asturllionés."
SENTENCE_AZE = 'Azərbaycan dili[2][3] və ya Azərbaycan türkcəsi[4], keçmişdə Azərbaycan Respublikasında sadəcə Türk dili[5] (Güney Azərbaycanda: Türk dili[6][7]) — Azərbaycan Respublikasının və Rusiya Federasiyası Dağıstan Respublikasının[8] rəsmi dövlət dili.'
SENTENCE_EUS = TEXT_EUS[0]
SENTENCE_BEL = TEXT_BEL[0]
SENTENCE_BEN = 'বাংলা ভাষা (বাঙলা, বাঙ্গলা, তথা বাঙ্গালা নামেও পরিচিত) একটি ধ্রুপদী ইন্দো-আর্য ভাষা, যা দক্ষিণ এশিয়ার বাঙালি জাতির প্রধান কথ্য ও লেখ্য ভাষা।'
SENTENCE_BUL = TEXT_BUL[0]
SENTENCE_MYA = TEXT_MYA[0]
SENTENCE_BXR = TEXT_BXR[0]
SENTENCE_CAT = TEXT_CAT[0]
SENTENCE_LZH = TEXT_LZH[0]
SENTENCE_ZHO_CN = TEXT_ZHO_CN[0]
SENTENCE_ZHO_TW = TEXT_ZHO_TW[0]
SENTENCE_CHU = TEXT_CHU[0]
SENTENCE_COP = TEXT_COP[0]
SENTENCE_HRV = TEXT_HRV[0]
SENTENCE_CES = TEXT_CES[0]
SENTENCE_DAN = TEXT_DAN[0]
SENTENCE_NLD = TEXT_NLD[0]
SENTENCE_ENM = 'Forrþrihht anan se time comm þatt ure Drihhtin wollde ben borenn i þiss middellærd forr all mannkinne nede he chæs himm sone kinnessmenn all swillke summ he wollde and whær he wollde borenn ben he chæs all att hiss wille.'
SENTENCE_ANG = TEXT_ANG[0]
SENTENCE_ENG_GB = SENTENCE_ENG_US = TEXT_ENG_US[0]
SENTENCE_MYV = TEXT_MYV[0]
SENTENCE_EPO = 'Esperanto, origine la Lingvo Internacia[4], estas la plej disvastiĝinta internacia planlingvo[5].'
SENTENCE_EST = TEXT_EST[0]
SENTENCE_FAO = TEXT_FAO[0]
SENTENCE_FIN = TEXT_FIN[0]
SENTENCE_FRA = TEXT_FRA[0]
SENTENCE_FRO = TEXT_FRO[0]
SENTENCE_GLG = TEXT_GLG[0]
SENTENCE_GOT = TEXT_GOT[0]
SENTENCE_KAT = TEXT_KAT[0]
SENTENCE_DEU_AT = SENTENCE_DEU_DE = SENTENCE_DEU_CH = TEXT_DEU_AT[0]
SENTENCE_NDS = TEXT_NDS[0]
SENTENCE_LUG = 'Luganda/Oluganda lwe lulimi olwogerwa Abaganda e Yuganda.'
SENTENCE_GRC = TEXT_GRC[0]
SENTENCE_ELL = TEXT_ELL[0]
SENTENCE_GUJ = 'ગુજરાતી ‍(/ɡʊdʒəˈrɑːti/[૬], રોમન લિપિમાં: Gujarātī, ઉચ્ચાર: [ɡudʒəˈɾɑːtiː]) ભારત દેશના ગુજરાત રાજ્યની ઇન્ડો-આર્યન ભાષા છે અને મુખ્યત્વે ગુજરાતી લોકો દ્વારા બોલાય છે.'
SENTENCE_HBO = TEXT_HBO[0]
SENTENCE_HEB = TEXT_HEB[0]
SENTENCE_HIN = TEXT_HIN[0]
SENTENCE_HUN = TEXT_HUN[0]
SENTENCE_ISL = TEXT_ISL[0]
SENTENCE_IND = TEXT_IND[0]
SENTENCE_GLE = TEXT_GLE[0]
SENTENCE_ITA = TEXT_ITA[0]
SENTENCE_JPN = TEXT_JPN[0]
SENTENCE_KAN = 'ದ್ರಾವಿಡ ಭಾಷೆಗಳಲ್ಲಿ ಪ್ರಾಮುಖ್ಯವುಳ್ಳ ಭಾಷೆಯೂ ಭಾರತದ ಪುರಾತನವಾದ ಭಾಷೆಗಳಲ್ಲಿ ಒಂದೂ ಆಗಿರುವ ಕನ್ನಡ ಭಾಷೆಯನ್ನು ಅದರ ವಿವಿಧ ರೂಪಗಳಲ್ಲಿ ಸುಮಾರು ೪೫ ದಶಲಕ್ಷ (೪.೫ ಕೋಟಿ) ಜನರು ಆಡು ನುಡಿಯಾಗಿ ಬಳಸುತ್ತಲಿದ್ದಾರೆ.'
SENTENCE_KAZ = TEXT_KAZ[0]
SENTENCE_KHM = TEXT_KHM[0]
SENTENCE_KPV = TEXT_KPV[0]
SENTENCE_KOR = TEXT_KOR[0]
SENTENCE_KMR = TEXT_KMR[0]
SENTENCE_KIR = TEXT_KIR[0]
SENTENCE_LAO = TEXT_LAO[0]
SENTENCE_LAT = TEXT_LAT[0]
SENTENCE_LAV = TEXT_LAV[0]
SENTENCE_LIJ = TEXT_LIJ[0]
SENTENCE_LIT = TEXT_LIT[0]
SENTENCE_LTZ = "D'Lëtzebuergesch gëtt an der däitscher Dialektologie als ee westgermaneschen, mëtteldäitschen Dialekt aklasséiert, deen zum Muselfränkesche gehéiert."
SENTENCE_MKD = TEXT_MKD[0]
SENTENCE_MSA = 'Jumlah penutur bahasa ini mencakupi lebih daripada 290 juta penutur[4] (termasuk sebanyak 260 juta orang penutur bahasa Indonesia)[5] merentasi kawasan maritim Asia Tenggara.'
SENTENCE_MAL = TEXT_MAL[0]
SENTENCE_MLT = TEXT_MLT[0]
SENTENCE_GLV = TEXT_GLV[0]
SENTENCE_MAR = TEXT_MAR[0]
SENTENCE_MNI_MTEI = 'ꯃꯤꯇꯩꯂꯣꯟ (ꯃꯤꯇꯩꯂꯣꯜ) ꯅꯠꯇ꯭ꯔꯒ ꯃꯩꯇꯩꯂꯣꯟ (ꯃꯩꯇꯩꯂꯣꯜ) ꯅꯠꯇ꯭ꯔꯒ ꯃꯅꯤꯄꯨꯔꯤ ꯂꯣꯟ (ꯃꯅꯤꯄꯨꯔꯤ ꯂꯣꯜ) ꯑꯁꯤ ꯑꯋꯥꯡ-ꯅꯣꯡꯄꯣꯛ ꯏꯟꯗꯤꯌꯥꯒꯤ ꯃꯅꯤꯄꯨꯔꯗ ꯃꯄꯨꯡ ꯑꯣꯢꯅ ꯉꯥꯡꯅꯕ ꯂꯣꯟ ꯑꯃꯅꯤ ꯫'
SENTENCE_MON = 'Монгол хэл нь Монгол улсын албан ёсны хэл юм.'
SENTENCE_NEP = 'नेपाली भाषा एक आर्य भाषा हो जुन दक्षिण एसियाको हिमालय क्षेत्रमा बोलिन्छ।'
SENTENCE_PCM = TEXT_PCM[0]
SENTENCE_NOB = TEXT_NOB[0]
SENTENCE_NNO = TEXT_NNO[0]
SENTENCE_ORI = 'ଓଡ଼ିଆ (ଇଂରାଜୀ ଭାଷାରେ Odia /əˈdiːə/ or Oriya /ɒˈriːə/,) ଇଣ୍ଡୋ-ଇଉରୋପୀୟ ଭାଷାଗୋଷ୍ଠୀ ଅନ୍ତର୍ଗତ ଏକ ଇଣ୍ଡୋ-ଆର୍ଯ୍ୟ ଭାରତୀୟ ଭାଷା ।'
SENTENCE_FAS = TEXT_FAS[0]
SENTENCE_POL = TEXT_POL[0]
SENTENCE_QPM = TEXT_QPM[0]
SENTENCE_POR_BR = SENTENCE_POR_PT = TEXT_POR_BR[0]
SENTENCE_RON = TEXT_RON[0]
SENTENCE_PAN_GURU = 'ਪੰਜਾਬੀ ਭਾਸ਼ਾ (ਸ਼ਾਹਮੁਖੀ ਲਿਪੀ: ‎پنجابی, ਪੰਜਾਬੀ) ਪੰਜਾਬ ਦੀ ਭਾਸ਼ਾ ਹੈ, ਜਿਸ ਨੂੰ ਪੰਜਾਬ ਖੇਤਰ ਦੇ ਵਸਨੀਕ ਜਾਂ ਸੰਬੰਧਿਤ ਲੋਕ ਬੋਲਦੇ ਹਨ।[18]'
SENTENCE_RUS = TEXT_RUS[0]
SENTENCE_ORV = TEXT_ORV[0]
SENTENCE_SME = TEXT_SME[0]
SENTENCE_SAN = TEXT_SAN[0]
SENTENCE_GLA = TEXT_GLA[0]
SENTENCE_SRP_CYRL = TEXT_SRP_CYRL[0]
SENTENCE_SRP_LATN = TEXT_SRP_LATN[0]
SENTENCE_SND = TEXT_SND[0]
SENTENCE_SIN = 'ශ්‍රී ලංකාවේ ප්‍රධාන ජාතිය වන සිංහල ජනයාගේ මව් බස සිංහල වෙයි.'
SENTENCE_SLK = TEXT_SLK[0]
SENTENCE_SLV = TEXT_SLV[0]
SENTENCE_DSB = TEXT_DSB[0]
SENTENCE_HSB = TEXT_HSB[0]
SENTENCE_SPA = TEXT_SPA[0]
SENTENCE_SWA = 'Kiswahili (Sawāḥilī kiarabu Swahili Kiingereza) ni lugha ya Kibantu ambayo huzungumzwa Afrika Mashariki ikiwa na wasemaji kadiri milioni 200 kama lugha ya kwanza na ya pili.'
SENTENCE_SWE = TEXT_SWE[0]
SENTENCE_TGL = 'Ang wikang Tagalog[1] (Baybayin:ᜏᜒᜃᜅ᜔ ᜆᜄᜎᜓᜄ᜔), o ang Tagalog, ay isa sa mga pinakaginagamit na wika ng Pilipinas.'
SENTENCE_TGK = 'Забони тоҷикӣ (дар солҳои 1989—1991 — забони форсии тоҷикӣ; 1991—1999 – забони тоҷикии форсӣ, дарӣ: زبان تاجیکی) — шакли забони порсӣ буда, дар Тоҷикистон ҳамчун забони давлатӣ мебошад.'
SENTENCE_TAM = TEXT_TAM[0]
SENTENCE_TAT = 'Татар теле — татарларның милли теле, Татарстанның дәүләт теле, таралышы буенча Россиядә икенче тел.'
SENTENCE_TEL = TEXT_TEL[0]
SENTENCE_TDT = 'Tetun (iha portugés: tétum; iha inglés: Tetum) neke lian nasionál no co-ofisiál Timór Lorosake nian.'
SENTENCE_THA = TEXT_THA[0]
SENTENCE_BOD = TEXT_BOD[0]
SENTENCE_TIR = 'ትግርኛ ኣብ ኤርትራን ኣብ ሰሜናዊ ኢትዮጵያን ኣብ ክልል ትግራይ ዝዝረብ ሴማዊ ቋንቋ እዩ።'
SENTENCE_TSN = 'Setswana ke teme e e buiwang mo mafatsheng a Aforika Borwa, Botswana, Namibia le Zimbabwe.'
SENTENCE_TUR = TEXT_TUR[0]
SENTENCE_OTA = TEXT_OTA[0]
SENTENCE_UKR = TEXT_UKR[0]
SENTENCE_URD = TEXT_URD[0]
SENTENCE_UIG = TEXT_UIG[0]
SENTENCE_VIE = TEXT_VIE[0]
SENTENCE_CYM = TEXT_CYM[0]
SENTENCE_WOL = TEXT_WOL[0]
SENTENCE_YOR = 'Èdè Yorùbá Ni èdè tí ó ṣàkójọpọ̀ gbogbo ọmọ káàárọ̀-oò-jíire bí, ní apá Ìwọ̀-Oòrùn ilẹ̀ Nàìjíríà, tí a bá wo èdè Yorùbá, àwọn onímọ̀ pín èdè náà sábẹ́ ẹ̀yà Kwa nínú ẹbí èdè Niger-Congo.'
SENTENCE_ZUL = 'Zulu /ˈzuːluː/, noma isiZulu wulimi lwabantu base Ningizimu neAfrika abayingxenye yamaNguni.'
SENTENCE_OTHER = SENTENCE_ENG_US

SENTENCE_ZHO_CN_CHAR_TOKENIZER = '英国的全称是United Kingdom of Great Britain，由四个部分组成：England、Scotland、Wales和Northern Ireland。'
SENTENCE_ZHO_TW_CHAR_TOKENIZER = '英國的全稱是United Kingdom of Great Britain，由四個部分組成：England、Scotland、Wales和Northern Ireland。'
SENTENCE_JPN_KANJI_TOKENIZER = '''The sentence "天気がいいから、散歩しましょう。" means: The weather is good so let's take a walk.'''
SENTENCE_BOD_WORD_DETOKENIZER = 'Test this Tibetan string: དུང་དང་འོ་མར་འགྲན་པའི་ལྷག་བསམ་མཐུ། །དམན་ཡང་དཀར་པོའི་བྱས་འབྲས་ཅུང་ཟད་ཅིག །བློ་དང་འདུན་པ་བཟང་བའི་རང་རིགས་ཀུན། །རྒྱལ་ཁའི་འཕྲིན་བཟང་ལས་དོན་འགྲུབ་ཕྱིར་འབད།།. Does detokenization work as expected?'

TOKENS_LONG = [str(i) for i in range(101) for j in range(10)]

def check_lang_examples(main):
    settings_langs = settings_langs = [lang[0] for lang in main.settings_global['langs'].values()]

    for var in globals():
        if var.startswith(('TEXT_', 'SENTENCE_')):
            var_lang = var.split('_', maxsplit = 1)[1].lower()

            if (
                not var_lang.endswith(('char_tokenizer', 'kanji_tokenizer', 'detokenizer'))
                and var_lang not in settings_langs
            ):
                print(f'Found unused language example: {var}/{var_lang}!')

if __name__ == '__main__':
    main = wl_test_init.Wl_Test_Main()

    check_lang_examples(main)
