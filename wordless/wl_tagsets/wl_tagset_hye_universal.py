# ----------------------------------------------------------------------
# Wordless: Tagsets - Universal POS tags - Armenian
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

# Universal POS Tags: https://universaldependencies.org/hy/pos/
tagset_mapping = [
    ['ADJ', 'ADJ', 'Adjective', 'մեծ, հին, կանաչ, անընկալելի\nառաջին, երկրորդ, երրորդ\nPossessive adjectives: հայոց, վրաց, պարսից, վանա'],
    ['ADP', 'ADP', 'Adposition', 'Prepositions, postpostions: ի, առ , ըստ, համար, հանդերձ, պես\nLocalizers/postpositions։ մոտ, վրա, մեջ, տակ, առաջ, առջև, դիմաց\nCase-marking words: հետո'],
    ['ADV', 'ADV', 'Adverb', 'շատ, լավ, հստակորեն, վաղը, վեր, վար\nInterrogative adverbs: որտեղ, ուր, երբ, ինչպես, ինչու, ինչքան, ինչչափ\nDemonstrative adverbs: այստեղ, այնտեղ, այսպես, այնպես, այսքան, այնչափ\nIndefinite adverbs: երբևիցե, երբևէ'],
    ['AUX', 'AUX', 'Auxiliary', 'Present tense. Finite present form of եմ is combined with imperfective and resultative participles of the lexical verb. The auxiliary expresses aspect, person, number, mood and tense, participles expresse aspect and voice: (վազում) եմ, (կանգնած) են. Note that a limited set of verbs can form present morphologically, without the auxiliary.\nImperfect tense. Finite imperfect form of էի is combined with imperfective, perfect and resultative participles of the lexical verb. The auxiliary expresses aspect, person, number, mood and tense, participles expresse aspect and voice: (վազում) էի, (վազել) էիր, (կանգնած) էին.\nDurative/habitual aspect. The finite form of լինել (լինեմ) (in various tenses and moods or in the infinitive լինել) is combined with processual, resultative and future participles of the lexical verb. The auxiliary expresses aspect, person, number, mood, tense and aspect, participles expresse aspect and voice: (գնալու) լինեմ, (գնացած) լինեմ, (գնալիս) լինեմ, (գնալու) լինել, (գնացած) լինել, (գնալիս) լինել.\nCausative voice. The finite form of տալ (in various tenses and moods) is combined with infinitve of the content verb. The auxiliary expresses aspect, person, number, tense and mood. The auxiliary will have Voice=Cau. There will be also voice information at the infinitive: (հասկանալ) տալ, հասկացնել (morphological causative), հասկացնել տալ.\nNecessitative mood. The mood particle պիտի and the impersonal predicative պետք է are combined with subjunctive finite form of lexical verb. The auxiliary expresses mood. պիտի / պետք է (գնա), պիտի / պետք է (գնար).'],
    ['CONJ', 'CONJ', 'Coordinating/subordinating conjunction', 'See CCONJ and SCONJ'],
    ['CCONJ', 'CCONJ', 'Coordinating conjunction', 'և, կամ, բայց'],
    ['SCONJ', 'SCONJ', 'Subordinating conjunction', 'որ, թե, թեև, թեպետ, եթե, քան, ուստի'],
    ['DET', 'DET', 'Determiner', 'Indefinite article: մի\nPossessive determiners: իմ, քո, նրա, մեր, ձեր, նրանց, իրենց\nReflexive possessive determiners: իր, իրենց\nDemonstrative determiners: Այս (մեքենան ես երեկ տեսել եմ։)\nInterrogative determiners: Ո՞ր (մեքենան ես հավանում։)\nRelative determiners: (Հետաքրքիր է՝) որ (մեքենան ես հավանում։)\nRelative possessive determiners: ում, որի\nIndefinite determiners: ոմն, ինչ-որ, ինչ-ինչ, մի քանի, ուրիշ, այլ, որոշ, որևէ, որևիցե, այսինչ, այնինչ, մի\nEmphatic determiners։ (Նախագահն) ինքը (եկավ դա տեսնելու։), ինքները\nTotal determiners: ամեն, ամեն մի, բոլոր, յուրաքանչյուր, ողջ, ամբողջ, համայն, ամենյան;\nNegative determiner: (Հիմա) ոչ մի (մեքենա չունենք։)'],
    ['INTJ', 'INTJ', 'Interjection', 'ա՜հ, օհո՜, դե՛, դե՛հ'],
    ['NOUN', 'NOUN', 'Noun', 'աղջիկ, կատու, ծառ, օդ, գեղեցկություն, լող, վազք, վազելը'],
    ['PROPN', 'PROPN', 'Proper noun', 'Դոնի Ռոստով, Մայնի Ֆրանկֆուրտ\nԼյուդվիգ (վան) Բեթհովեն, Միգել (դը) Սերվանտես\n(Վերին) Սասնաշեն\nՄԱԿ, ԵԱՀԿ Մինսկի (խումբ)'],
    ['NUM', 'NUM', 'Numeral', '0, 1, 2, 3, 4, 5, 2014, 1000000, 3.14159265359\nI, II, III, IV, V, MMXIV\nմեկ, երկու, երեք, չորս, հինգ, յոթանասուն\nԱ, Ժ, Է, ԺԱ, Ն, Ռ\nDenominators of fractions constitute a separate class of cardinal numerals: կես, քառորդ'],
    ['PART', 'PART', 'Particle', 'Affirmativ particle: անպատճառ, իհարկե, հարկավ\nConcession particle: ինչևէ, այնուամենայնիվ\nDemonstration particle: ահա, ահավասիկ\nDubitation particle: ասես, գուցե, կարծես, հավանաբար\nEmphatic particle: ախար, մանավանդ, հատկապես\nLimitation particle: գեթ, լոկ, միայն\nNegation particle: ոչ, չէ, բնավ, ամենևին\nWish particle: երանի, երնեկ\nVolition particle: ապա, դե, թող\nMood particle: (չ)պիտի, (չ)պետք է'],
    ['PRON', 'PRON', 'Pronoun', 'Personal pronouns: ես, դու, նա, մենք, դուք, նրանք\nPossessive pronouns (which usually stand alone as a nominal): իմը, քոնը, նրանը, մերը, ձերը, նրանցը\nDemonstrative pronouns: սա, դա, նա\nReflexive pronouns: իր, իրեն, իրենց\nReciprocal pronouns: մեկմեկու (մեկմեկի), միմյանց, իրար\nInterrogative pronouns: ո՞վ, Ի՞նչ (ես կարծում։)\nRelative pronouns: ով; (Արա,) ինչ (ուզում ես։)\nIndefinite pronouns: մի քանիսը, մեկը, մեկնումեկը, ոմանք, ուրիշը\nEmphatic pronouns։ ինքը, իրենք\nTotal pronouns: ամենը, ամենքը, ամեն մեկը, ամեն ոք, ամեն ինչ, բոլորը, յուրաքանչյուրը, յուրաքանչյուր ոք, ողջը, ամբողջը\nNegative pronouns: ոչ ոք, ոչինչ, ոչ մեկը'],
    ['VERB', 'VERB', 'Verb', 'գրել, գրել(ը)\nգրեցի, գրեցիր, գրեց, գրեցինք, գրեցիք, գրեցին\nունեմ, ունես, ունի, ունենք, ունեք, ունեն\nImperative in different numbers: գրի՛, գրե՛ք, կարդա՛, կարդացե՛ք\nգրեմ, գրես, գրի, գրենք, գրեք, գրեն\nգնայի, գնայիր, գնար, գնայինք, գնայիք, գնային\nկգնամ, կգնաս, կգնա, կգնանք, կգնաք, կգնան\nկգրեի, կգրեիր, կգրեր, կգրեինք, կգրեիք, կգրեին\n(չեմ) գրի, (չեմ) գնա\nParticiples: գրած, կարդացած, գրելիս, կարդալիս, գրում, կարդում, գրելու, կարդալու, գրել, կարդացել, գրի, կարդա\nConverb: գրելիս, կարդալիս\nVerbal adjectives: գրող, կարդացող, գրելիք, կարդալիք'],

    ['PUNCT', 'PUNCT', 'Punctuation', 'Period: ։\nComma: ,\nParentheses: ()\nQuotation mark: «»\nExclamation mark: ՜\nQuestion mark։ ՞\nEmphasis mark, acute accent: ՛'],
    ['SYM', 'SYM', 'Symbol', '$, %, §, ©\n+, −, ×, ÷, =, <, >\n:), ♥‿♥, 😝\njohn.doe@universal.org, http://universaldependencies.org/, 1-800-COMPANY'],
    ['X', 'X', 'Other', '(Եվ ապա նա պարզապես) xfgh pdl jklw։']
]
