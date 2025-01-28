# ----------------------------------------------------------------------
# Wordless: Tagsets - Universal POS tags - Armenian (Classical)
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

# Universal POS Tags: https://universaldependencies.org/hy/pos/
tagset_mapping = [
    ['ADJ', 'ADJ', 'Adjective', 'ուրախ, լսելի, առաջին, երկրորդ, չորրորդ\nComparative degrees: չար քան զ(առաջինն), (ապա թե ոչ մինչդեռ) հեռագոյն (իցէ), (զի՞նչ իցէ) մեծագոյն քան զ(իմաստութիւն)'],
    ['ADP', 'ADP', 'Adposition', 'Prepositions: առ, առ ի\nPostpostions: հանդերձ\nCircumpositions։ ի (լեռնէ) անտի'],
    ['ADV', 'ADV', 'Adverb', 'արտաքոյ, կարի, ի ծածուկ'],
    ['AUX', 'AUX', 'Auxiliary', 'Copula: եին արդարք\nNegated copula: չիք ոք բարի\nPeriphrastic tenses: զայն նշան տուեալ էր նոցա\nPeriphrastic causative: ետ տանել զնա առ Հէրովդէս'],
    ['CONJ', 'CONJ', 'Coordinating/subordinating conjunction', 'See CCONJ and SCONJ'],
    ['CCONJ', 'CCONJ', 'Coordinating conjunction', 'եւ\nկամ\nբայց'],
    ['SCONJ', 'SCONJ', 'Subordinating conjunction', 'Complementizers: (եւ իմացան) թե (տեսիլ ետես ի տաճարին)\nNon-adverbial markers that introduce an adverbial clause: (եւ) իբրեւ (ոչ գտին. դարձան անդրէն յԵրուսաղեմ խնդրել զնա)\nNon-pronominal relativizers: (Եւ երեւեցաւ նմա հրեշտակ Տեառն) զի (կայր ընդ աջմէ սեղանոյ խնկոցն:)'],
    ['DET', 'DET', 'Determiner', 'Demonstrative/possessive particles: =ս, =դ, =ն\nPronominal adjectives, including indefinite pronominal adjectives: իմ, ոմն\nQuantifiers: մի, ամենայն, բազում'],
    ['INTJ', 'INTJ', 'Interjection', 'Emotive interjections: ով, վահ\nDemonstrative interjections: ահա\nFeedback interjections: այո՛'],
    ['NOUN', 'NOUN', 'Noun', 'աղջիկ, ծառ, աւդ'],
    ['PROPN', 'PROPN', 'Proper noun', 'Յիսուս, Երուսաղեմ'],
    ['NUM', 'NUM', 'Numeral', 'մի, Ա'],
    ['PART', 'PART', 'Particle', 'Emphatic particle: իսկ\nNegation particle: ոչ (and its proclitic variant չ=), մի\nMood particle: գուցէ, եթե (and its variant թե)'],
    ['PRON', 'PRON', 'Pronoun', 'Personal pronouns (PronType=Prs): ես, դու. The third person pronoun նա coincides with the demonstrative նա.\nEmphatic pronoun (PronType=Emp): ինքն\nReflexive pronouns ([PronType=Prs Reflex=Yes]()): իւր. The emphatic pronoun ինքն and the word անձն can also be used as reflexive pronouns, especially in the nominative and accusative, which իւր does not have.\nDemonstrative pronouns (PronType=Dem): սա, դա, նա; այս, այդ, այն; սոյն, դոյն, նոյն\nReciprocal pronouns (PronType=Rcp): միմեանք, իրեարք\nInterrogative pronouns (PronType=Int): ո՞վ, ո՞, զի՞, զի՞նչ. The interrogative pronominal adjective (determiner) ո՞ր, traditionally counted as a pronoun, is tagged (DET).\nIndefinite pronouns (PronType=Ind): there are two animate indefinite pronouns, ոմն and ոք, an inanimate indefinite pronoun, ինչ, and a much less frequent իմն. Like in the case of parallel pairs of adverbs (երբեմն and երբեք, ուրեմն, ուրեք, as well as unpaired ուստեք), the difference in the use of the two animate indefinite pronouns can be described in terms of polarity. The negative polarity words, ending in -ք, are typically used in negative, interrogative, conditional, and relative clauses. By contrast the pronouns in -մն are typically used in affirmative main clauses and point to a specific referent. The contrast is grasped with the Definite=Ind tag for the pronouns in -ք and Definite=Spec tag for the ones in -մն.\nRelative pronoun (PronType=Rel): որ. When the relative pronoun substitutes a noun in the relative clause and is tagged (PRON), when it functions as a pronominal adjective, it is tagged (DET).\nCollective pronouns (PronType=Tot): ամենեքեան, եւթնեքեան'],
    ['VERB', 'VERB', 'Verb', 'Finate verb: գրեմ\nInfinitive: գրել\nConverb: գալոց\nParticiple: մտեալ\nVerbal noun: գրել'],

    ['PUNCT', 'PUNCT', 'Punctuation', 'Period: ։\nComma: ,\nExclamation mark: ՜\nQuestion mark։ ՞\nEmphasis mark: ՛'],
    ['SYM', 'SYM', 'Symbol', '$, %, §, ©\n+, −, ×, ÷, =, <, >\n:), ♥‿♥, 😝'],
    ['X', 'X', 'Other', '(Եւ զինն ժամաւն գոչեաց Յիսուս ի ձայն մեծ եւ ասէ՝) էղի, էղի, ղամա սաբաքթանի՝ (այսինքն է Աստուած իմ, Աստուած իմ, ընդէ՞ր թողեր զիս:)']
]
