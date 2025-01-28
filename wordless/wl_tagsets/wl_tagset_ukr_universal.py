# ----------------------------------------------------------------------
# Wordless: Tagsets - Universal POS tags - Ukrainian
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

# Universal POS Tags: https://universaldependencies.org/uk/pos/
tagset_mapping = [
    ['ADJ', 'ADJ', 'Adjective', 'великий, старий, зелений\nPossessive adjectives: батьків, материн\nперший, другий, третій\nPassive perfective participial adjective: зроблений\nPassive imperfective participial adjective: роблений\nPresent participial adjective (it is considered ungrammatical but still used occasionally, which is why it is encoded): роблячий\nPast participial adjective (it is considered ungrammatical but still used occasionally, which is why it is encoded): зробивший'],
    ['ADP', 'ADP', 'Adposition', 'в, до, протягом'],
    ['ADV', 'ADV', 'Adverb', 'дуже, добре, точно, завтра, вгору, вниз\nOrdinal numeral adverbs: вперше, вдруге, втретє\nMultiplicative numeral adverbs: двічі, тричі\nInterrogative adverbs: де, куди, коли, як, чому\nDemonstrative adverbs: тут, там, зараз, тоді, так\nIndefinite adverbs: десь, кудись, іноді, якось\nTotal adverbs: всюди, завжди\nNegative adverbs: ніде, ніколи'],
    ['AUX', 'AUX', 'Auxiliary', 'бути'],
    ['CONJ', 'CONJ', 'Coordinating/subordinating conjunction', 'See CCONJ and SCONJ'],
    ['CCONJ', 'CCONJ', 'Coordinating conjunction', 'і, й, та, або, але'],
    ['SCONJ', 'SCONJ', 'Subordinating conjunction', 'що, щоб, аби, якщо, як, ніж'],
    ['DET', 'DET', 'Determiner', 'Possessive determiners: мій, твій, його, її, наш, ваш, їх\nReflexive possessive determiner: свій\nDemonstrative determiners: той, Цю (машину я бачила вчора.)\nInterrogative determiners: Котра (машина тобі подобається?)\nRelative determiners: (Мені цікаво,) котра (машина тобі подобається.)\nRelative possessive determiner: чий\nIndefinite determiners: деякий, якийсь\nTotal determiners: кожен, всякий\nNegative determiners: (Ми не маємо) жодної (машини.), ніякий'],
    ['INTJ', 'INTJ', 'Interjection', 'ах, бум, ну, ба, браво'],
    ['NOUN', 'NOUN', 'Noun', 'дівчинка, кіт, дерево, повітря, краса, плавання'],
    ['PROPN', 'PROPN', 'Proper noun', 'Франкфурт (на) Майні, ООН'],
    ['NUM', 'NUM', 'Numeral', '0, 1, 2, 3, 4, 5, 2014, 1000000, 3.14159265359\nI, II, III, IV, V, MMXIV\nодин, два, три, чотири, п’ять, сімдесят\nDenominators of fractions constitute a separate class of cardinal numerals: половина, третина, четвертина (чверть). They are not considered numerals in the Ukrainian grammar. They are tagged NOUN.\nSpecial forms, so-called generic numerals: четверо, п’ятеро\nодні, двоє, троє'],
    ['PART', 'PART', 'Particle', 'Sentence modality: но, хай, нехай\nтільки, аж'],
    ['PRON', 'PRON', 'Pronoun', 'Personal pronouns: я, ти, він, вона, воно, ми, ви, вони\nReflexive pronouns: себе, се, собі, собою\nDemonstrative pronouns: Це (я бачила вчора.)\nInterrogative pronouns: хто, Що (ти думаєш?)\nRelative pronouns: хто, (Мене цікавить,) що (ти думаєш.)\nIndefinite pronouns: дехто, дещо\nTotal pronouns: кожен, всі\nNegative pronouns: ніхто, ніщо'],
    ['VERB', 'VERB', 'Verb', 'нести\nнесу, несеш, несе, несемо, несете, несуть\nImperative in different persons and numbers: неси, несімо, несіть\nPast tense forms in different genders and numbers: ніс, несла, несло, несли\nPassive impersonal form: несено\nPresent and past adverbial participles: несучи, нісши'],

    ['PUNCT', 'PUNCT', 'Punctuation', 'Period: .\nComma: ,\nParentheses: ()'],
    ['SYM', 'SYM', 'Symbol', '$, %, §, ©\n+, −, ×, ÷, =, <, >\n:), ♥‿♥, 😝\njohn.doe@universal.org, http://universaldependencies.org/, 1-800-COMPANY'],
    ['X', 'X', 'Other', '(А він тільки) xfgh pdl jklw']
]
