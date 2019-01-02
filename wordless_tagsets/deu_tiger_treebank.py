#
# Wordless: Mapping Table (TIGER Treebank Tagset -> Universal POS Tags)
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

#
# TIGER Treebank Tagset: https://spacy.io/api/annotation#pos-tagging
#
# Universal POS Tags: http://universaldependencies.org/u/pos/all.html
#

mappings = [
    ['ADJA', 'ADJ', 'Adjective, attributive', ''],
    ['ADJD', 'ADJ', 'Adjective, adverbial or predicative', ''],

    ['ADV', 'ADV', 'Adverb', ''],

    ['APPO', 'ADP', 'Postposition', ''],
    ['APPR', 'ADP', 'Preposition; circumposition left', ''],
    ['APPRART', 'ADP', 'Preposition with article', ''],
    ['APZR', 'ADP', 'Circumposition right', ''],

    ['ART', 'DET', 'Definite or indefinite article', ''],
    ['CARD', 'NUM', 'Cardinal number', ''],
    ['FM', 'X', 'Foreign language material', ''],
    ['ITJ', 'INTJ', 'Interjection', ''],

    ['KOKOM', 'CONJ', 'Comparative conjunction', ''],
    ['KON', 'CCONJ', 'Coordinating conjunction', ''],
    ['KOUI', 'SCONJ', 'Subordinating conjunction with "zu" and infinitive', ''],
    ['KOUS', 'SCONJ', 'Subordinating conjunction with sentence', ''],

    ['NE', 'PROPN', 'Proper noun', ''],
    ['NNE', 'PROPN', 'Proper noun', ''],
    ['NN', 'NOUN', 'Noun, singular or mass', ''],

    ['PAV', 'ADV', 'Pronominal adverb', ''],
    ['PROAV', 'ADV', 'Pronominal adverb', ''],

    ['PDAT', 'DET', 'attributive demonstrative pronoun', ''],
    ['PDS', 'PRON', 'Substituting demonstrative pronoun', ''],
    ['PIAT', 'DET', 'Attributive indefinite pronoun without determiner', ''],
    ['PIDAT', 'DET', 'Attributive indefinite pronoun with determiner', ''],
    ['PIS', 'PRON', 'Substituting indefinite pronoun', ''],
    ['PPER', 'PRON', 'Non-reflexive personal pronoun', ''],
    ['PPOSAT', 'DET', 'Attributive possessive pronoun', ''],
    ['PPOSS', 'PRON', 'Substituting possessive pronoun', ''],
    ['PRELAT', 'DET', 'Attributive relative pronoun', ''],
    ['PRELS', 'PRON', 'Substituting relative pronoun', ''],
    ['PRF', 'PRON', 'Reflexive personal pronoun', ''],

    ['PTKA', 'PART', 'Particle with adjective or adverb', ''],
    ['PTKANT', 'PART', 'Answer particle', ''],
    ['PTKNEG', 'PART', 'Negative particle', ''],
    ['PTKVZ', 'PART', 'Separable verbal particle', ''],
    ['PTKZU', 'PART', '"zu" before infinitive', ''],

    ['PWAT', 'DET', 'Attributive interrogative pronoun', ''],
    ['PWAV', 'ADV', 'Adverbial interrogative or relative pronoun', ''],
    ['PWS', 'PRON', 'Substituting interrogative pronoun', ''],

    ['TRUNC', 'X', 'Word remnant', ''],

    ['VAFIN', 'AUX', 'Finite verb, auxiliary', ''],
    ['VAIMP', 'AUX', 'Imperative, auxiliary', ''],
    ['VAINF', 'AUX', 'Infinitive, auxiliary', ''],
    ['VAPP', 'AUX', 'Perfect particle, auxiliary', ''],

    ['VMFIN', 'VERB', 'Finite verb, modal', ''],
    ['VMINF', 'VERB', 'Infinitive, modal', ''],
    ['VMPP', 'VERB', 'Perfect participle, modal', ''],
    ['VVFIN', 'VERB', 'Finite verb, full', ''],
    ['VVIMP', 'VERB', 'Imperative, full', ''],
    ['VVINF', 'VERB', 'Infinitive, full', ''],
    ['VVIZU', 'VERB', 'Infinitive with "zu", full', ''],
    ['VVPP', 'VERB', 'Perfect participle, full', ''],

    ['$(', 'PUNCT', 'Other sentence-internal punctuation mark', ''],
    ['$,', 'PUNCT', 'Comma', ','],
    ['$.', 'PUNCT', 'Sentence-final punctuation mark', ''],

    ['XY', 'X', 'Non-word containing non-letter', ''],
    ['SP', 'X', 'Space', '']
]
