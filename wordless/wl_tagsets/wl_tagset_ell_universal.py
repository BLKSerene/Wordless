# ----------------------------------------------------------------------
# Wordless: Tagsets - Universal POS tags - Greek (Modern)
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

# Reference: https://universaldependencies.org/el/pos/
tagset_mapping = [
    ['ADJ', 'ADJ', 'Adjective', 'μεγάλος/megalos, πράσινος/prasinos, ακατάληπτος/akataliptos\nπρώτος/protos, δεύτερος/defteros, τρίτος/tritos\n(Η Ελένη είναι) ίδια (με την μητέρα της). It is also assigned the tag DET.'],
    ['ADP', 'ADP', 'Adposition', 'σε, από, με, για, ως, εκ/εξ / se, apo, me, gia, os, ek/ex\n(μέσα) σε, (ενάντια) σε ενάντια\nμετά/εντός + ΝΟUN[Case=Gen]: μετά ληστείας, εντός δευτερολέπτων. In all other environments μετά, εντός are tagged ADV.'],
    ['ADV', 'ADV', 'Adverb', 'Locative adverbs: απέξω/apekso, εδώ/edo, εκεί/eki, πάνω/pano, κάτω/kato, δεξιά/deksia, αριστερά/aristera, κάπου/kapou, παντού/pantou, πουθενά/pouthena, πού/pou\nManner adverbs: ακριβώς/akrivos, γιατί/yiati (when it is on its own / it introduces direct questions), εντάξει/endaksi, καλά/kala, κατανάγκη/katanagki, πώς/pos, υπόψη/ipopsi\nTemporal adverbs: αύριο/avrio, κάποτε/kapote, καταρχήν/katarchin, πάντα/panta, πέρσυ/persi, πότε/pote, ποτέ/pote, σήμερα/simera, τότε/tote, τώρα/tora, χθες/chthes\nQuantity adverbs: άπαξ/apaks, καθόλου/katholou, λίγο/ligo, μόνο/mono, τόσο/toso'],
    ['AUX', 'AUX', 'Auxiliary', 'Tense auxiliaries: έχει φύγει / echi figi, θα φύγει / tha figi\nAuxiliaries with passive verb forms: έχει γραφτεί / echi grafti, θα γραφτεί / tha grafti\nAuxiliary use of είμαι: το τριαντάφυλο είναι λουλούδι / to triantafilo ine louloudi, ο Αλέξανδρος είναι ψηλός / o Alexandros ine psilos, το γράμμα είναι γραμμένο με σκούρο μελάνι / to grama ine grameno me skouro melani\nAuxiliary use of να: Να προσέχεις\nAuxiliary use of ας: Καλύτερα ας έχουμε το κεφάλι μας ήσυχο.'],
    ['CONJ', 'CONJ', 'Coordinating/subordinating conjunction', 'See CCONJ and SCONJ'],
    ['CCONJ', 'CCONJ', 'Coordinating conjunction', 'και, ή, αλλά, όμως, ωστόσο, είτε (εσύ) είτε (ο Παύλος), ούτε (εσύ) ούτε (ο Παύλος)'],
    ['SCONJ', 'SCONJ', 'Subordinating conjunction', 'Complementizers: αν/an, άρα, αφού/ara, afou, γιατί/giati, ενώ/eno, καθώς/kathos, μήπως, ότι, πως/mipos, oti, pos, ώστε/oste, ώσπου/ospou\nAdverbial clause introducers: όταν/otan, αφότου/afotou, πριν/prin, μόλις/molis (when introducing a clause, not a nominal), μια (και) / mia (ke) (with the dependency fixed between them)\nInterrogative pronouns:\n\tποιος/pios, πόσος/posos\n\tτι/ti that introduce an indirect question that serves as an argument of a verb or as a clausal modifier of a deverbal noun\n\t\tVERB: ρώτησα ποιο/πόσο/τι θέλεις; / rotisa pio/poso/ti theleis\n\t\tNOUN: (έχω μείνει με την) απορία τί (στο καλό της είπες).'],
    ['DET', 'DET', 'Determiner', 'Definite article: ο, η, το / o, i, to\nIndefinite article: ένας, μία, ένα / enas, mia, ena\nAdjectives denoting quantities and their comparatives:\n\tαρκετός/arketos, λίγος/ligos (ελάχιστος/elachistos), μερικός/merikos, μισός/misos, μόνος/monos, πολύς/polis\n\tολόκληρος/olokliros, όλος/olos, πας/άπας / pas/apas\nDemonstrative pronouns: αυτός/aftos, εκείνος/ekinos, (ε)τούτος/(e)toutos, τέτοιος/tetios, τόσος/tosos, ίδιος/idios\nIndefinite pronouns:\n\tάλλος/alos, κάποιος/kapios, κάτι/kati\n\tκάθε/kathe, καθένας/kathenas\n\tκανείς (κανένας) / kanis (kanenas), τίποτα/ε / tipota/e\nInterrogative pronouns when followed by a noun: ποιος/pios, πόσος/posos, τι/ti, e.g., ποιο/πόσο/τι φαγητό θέλεις; / pio/poso/ti fagito thelis?\nRelative pronouns when followed by a noun: όποιος/-δήποτε / opios/-dipote, όσος/-δήποτε / osos/-dipote, ό,τι/-δήποτε / oti/-dipote\nίδιος/idios'],
    ['INTJ', 'INTJ', 'Interjection', 'αμήν, άντε, βρε, καλέ, ναι/ne, όχι/ochi, ορίστε, μα, λοιπόν/lipon, καλημέρα/kalimera, καληνύχτα/kalinichta, Καλά(, πώς ήρθες εδώ;)'],
    ['NOUN', 'NOUN', 'Noun', 'γυναίκα/gineka, σκύλος/skilos, τραπέζι/trapezi, επανάσταση/epanastasi, ελευθερία/freedom\nProfessions: αστυνομικός/astinomikos, στρατιωτικός/stratiotikos. When the same words cooccur with another noun, such as αστυνομικός σκύλος / astinomikos skilos, they are assigned the tag ADJ.\nακουστικό/akoustiko, (καρτο-)κινητό / (karto-)kinito, ενδότερα/endotera, πρωϊνό/proino, μεσημεριανό/mesimeriano, βραδινό/vradino, λαδερά/ladera, λαϊκή, περιπολικό/peripoliko'],
    ['PROPN', 'PROPN', 'Proper noun', 'Κύριε/kirie\nPlace names: Ανατολή/Anatoli, Δύση/Disi, Όλυμπος/olibos\nDay names: Τρίτη/Triti, Σαββατοκύριακο/Savatokiriako\nCountries: Eλλάδα/Elada, Κύπρος/Kipros\nDiminutives productively formed by a proper noun and a suffix such as –άκι, –ίτσα, –ούλης, -άκης/-aki, -itsa, -oulis, -akis: Mαράκι/Maraki, Γιαννάκης/Gianakis\nAugmentatives (μεγεθυντικά) productively formed by a proper noun and a suffix such as -άρας/-aras: Στελάρας/Stelaras, Σουλάρα/Soulara\nNames of anniversaries, bank holidays: Ανάσταση/Anastasi, Επιτάφιος/Epitafios, Μεγάλη Εβδομάδα / Megali Vdomada, Πάσχα/Pascha, Χριστούγεννα/Christougena, Πρωτοχρονιά/Protochronia\nPlace names:\n\tStreet names in the genitive case where the noun οδός/odos is omitted: (οδός) Ερμού / (odos) Ermou .\n\tAvenue/motorway names consisting of two place names in the genitive case (starting-ending places): Αθηνών-Κορίνθου. These are productive compounds. Each part of the compound is assigned the tag PROPN and the second proper noun depends on the first one with the relation compound; the first proper noun is considered the head of the compound.'],
    ['NUM', 'NUM', 'Numeral', '0, 1, 2, 3, 4, 5, 2014, 1000000, 3.14159265359\nένα, δύο, τρία, εβδομήντα πέντε\nI, II, III, IV, V, MMXIV\nδωδεκάμιση'],
    ['PART', 'PART', 'Particle', 'ας, δεν, καν, μπας (και), μην, να, όχι, πάρα, μακάρι'],
    ['PRON', 'PRON', 'Pronoun', 'Interrogative pronouns in direct questions: Ποιο/Πόσο/Τι (θέλεις;)\nPersonal pronouns: both strong and weak types (clitics): του το (έδωσα) / (tou to) edosa\nPossessive pronouns: (το σπίτι) μου / (to spiti) mou\nReflexive pronouns: εαυτός/eaftos\nRelative pronouns: οποίος/opios'],
    ['VERB', 'VERB', 'Verb', 'τρέχω/trecho, τρώει/troi\nτρέχοντας/trechodas, τρώγοντας/trogodas'],

    ['PUNCT', 'PUNCT', 'Punctuation', 'Period: .\nComma: ,\nParentheses: ()'],
    ['SYM', 'SYM', 'Symbol', '$, %, §, ©\n+, −, ×, ÷, =, <, >\n:), ♥‿♥, 😝'],
    ['X', 'X', 'Other', '(H αναπαραγωγή δεν θα είναι εντελώς) Lossless.\n(Κάντο) φοργουόρντ (σε μένα.)']
]
