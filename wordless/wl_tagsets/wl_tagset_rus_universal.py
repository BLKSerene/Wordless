# ----------------------------------------------------------------------
# Wordless: Tagsets - Universal POS tags - Russian
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

# Universal POS Tags: https://universaldependencies.org/ru/pos/
tagset_mapping = [
    ['ADJ', 'ADJ', 'Adjective', 'большой, старый, зеленый\nPossessive adjectives: студенческий, учительский\nпервый, второй, третий\nPassive participial adjective: сделанный\nPresent participial adjective, derived from present transgressive: делающий\nPast participial adjective, derived from past transgressive: сделавший'],
    ['ADP', 'ADP', 'Adposition', 'в, к, на'],
    ['ADV', 'ADV', 'Adverb', 'очень, хорошо, точно, завтра, вниз, наверх\nOrdinal numeral adverbs: впервые\nMultiplicative numeral adverbs: однажды, дважды, трижды\nInterrogative adverbs: где, куда, когда, как, почему\nDemonstrative adverbs: здесь, там, сейчас, потом, так\nIndefinite adverbs: где-то, куда-то, когда-то, как-то\nTotal adverbs: везде, всегда\nNegative adverbs: нигде, никогда'],
    ['AUX', 'AUX', 'Auxiliary', 'Future tense. Finite future form of быть is combined with infinitive of the lexical verb. The auxiliary expresses person, number and tense: буду делать, будешь делать, будут делать. Note that a limited set of verbs can form future morphologically, without the auxiliary.\nConditional mood. Conditional form (historically aorist) of být is combined with past participle of the lexical verb. The auxiliary expresses person and number, the participle expresses gender and number: сделал бы, сделала бы, сделали бы.\nPassive voice. A form of быть (in various tenses and moods or in the infinitive) is combined with passive participle of the lexical verb. The auxiliary expresses person, number, tense(past and future) and mood, the participle expresses gender, number and voice: будет сделан, был сделан, был бы сделан.'],
    ['CONJ', 'CONJ', 'Coordinating/subordinating conjunction', 'See CCONJ and SCONJ'],
    ['CCONJ', 'CCONJ', 'Coordinating conjunction', 'и, или, но'],
    ['SCONJ', 'SCONJ', 'Subordinating conjunction', 'что, если, как, чем'],
    ['DET', 'DET', 'Determiner', 'Possessive determiners: мой, твой, его, её, наш, ваш, их\nReflexive possessive determiner: свой\nDemonstrative determiners: (Я видела) эту (машину вчера.)\nInterrogative determiners: Какая (машина тебе нравится?)\nRelative determiners: (Мне интересно,) которая (машина тебе нравится.)\nRelative possessive determiner: чей\nIndefinite determiners: некоторый\nTotal determiners: каждый\nNegative determiners: (У нас не осталось) никаких (машин.)'],
    ['INTJ', 'INTJ', 'Interjection', 'ах, ого, ну, ради бога'],
    ['NOUN', 'NOUN', 'Noun', 'девочка, кошка, дерево, воздух, красота, плавание'],
    ['PROPN', 'PROPN', 'Proper noun', 'ООН'],
    ['NUM', 'NUM', 'Numeral', '0, 1, 2, 3, 4, 5, 2014, 1000000, 3.14159265359\nI, II, III, IV, V, MMXIV\nодин, два, три, четыре, пять, семьдесят\nDenominators of fractions constitute a separate class of cardinal numerals: половина, треть, четверть\nCollective numerals (see specific-syntax on their morphosyntactic behavior): двое, трое, четверо, пятеро\nPronominal quantifiers of imprecise quantity: сколько, столько, предостаточно'],
    ['PART', 'PART', 'Particle', 'Sentence modality: пусть\nже\n(Мне сегодня) аж (пять писем пришло.)'],
    ['PRON', 'PRON', 'Pronoun', 'Personal pronouns: я, ты, он, она, оно, мы, вы, они\nReflexive pronouns: себе, сам\nDemonstrative pronouns: (Я видел) это (вчера.)\nInterrogative pronouns: кто, Что (ты думаешь?)\nRelative pronouns: кто, (Мне интересно,) что (ты думаешь.)\nIndefinite pronouns: кто-то, что-то\nTotal pronouns: каждый, все\nNegative pronouns: никто, ничто'],
    ['VERB', 'VERB', 'Verb', 'Infinitive: рисовать\nFinite indicative: рисую, рисуешь, рисует, рисуем, рисуете, рисуют, рисовал, рисовала, рисовало, рисовали\nFinite imperative: рисуй, рисуйте\nShort passive participle in different tenses: (на)рисован, рисуем\nParticiple in different tenses and voices, full forms: рисующий, рисовавший, рисуемый, рисованный\nConverb: рисуя, рисовав'],

    ['PUNCT', 'PUNCT', 'Punctuation', 'Period: .\nComma: ,\nParentheses: ()'],
    ['SYM', 'SYM', 'Symbol', '$, %, §, ©\n+, −, ×, ÷, =, <, >\n:), ♥‿♥, 😝\njohn.doe@universal.org, http://universaldependencies.org/, 1-800-COMPANY'],
    ['X', 'X', 'Other', '(И потом он просто) xfgh pdl jklw']
]
