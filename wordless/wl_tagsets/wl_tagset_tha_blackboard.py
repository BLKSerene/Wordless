# ----------------------------------------------------------------------
# Wordless: Tagsets - Blackboard
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

# References:
#     https://github.com/PyThaiNLP/pythainlp/blob/dev/docs/api/tag.rst#pythainlptag
#     https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/tag/blackboard.py
#     https://bitbucket.org/kaamanita/blackboard-treebank/src/master/Blackboard-Treebank.pdf
tagset_mapping = [
    ['AJ', 'ADJ', 'Adjective: Attribute, modifier, or description of a noun', 'ใหม่, พิเศษ , ก่อน, มาก, สูง'],
    ['AV', 'ADV', 'Adverb: Word that modifies or qualifies an adjective, verb, or another adverb', 'ก่อน, ก็, เล็กน้อย, เลย, สุด'],
    ['AX', 'AUX', 'Auxiliary: Tense, aspect, mood, and voice', 'เป็น, ใช่, คือ, คล้าย'],
    ['CC', 'CCONJ', 'Connector: Conjunction and relative pronoun', 'แต่, และ, หรือ'],
    ['CL', 'NOUN', 'Classifier: Class or measurement unit to which a noun or an action belongs', 'กำมือ, พวก, สนาม, กีฬา, บัญชี'],
    ['FX', 'NOUN', 'Prefix: Inflectional (nominalizer, adjectivizer, adverbializer, and courteous verbalizer), and derivational', 'กำมือ, พวก, สนาม, กีฬา, บัญชี'],
    ['IJ', 'INTJ', 'Interjection: Exclamation word', 'อุ้ย, โอ้ย'],
    ['NG', 'PART', 'Negator: Word of negatio', ''],
    ['NN', 'NOUN', 'Noun: Person, place, thing, abstract concept, and proper name', 'กำมือ, พวก, สนาม, กีฬา, บัญชี'],
    ['NU', 'NUM', 'Number: Quantity for counting and calculation', '5,000, 103.7, 2004, หนึ่ง, ร้อย'],
    ['PA', 'PART', 'Particle: Politeness, intention, belief, question', 'มา ขึ้น ไม่ ได้ เข้า'],
    ['PR', 'PRON', 'Pronoun: Word used to refer to an element in the discourse', 'เรา, เขา, ตัวเอง, ใคร, เธอ'],
    ['PS', 'ADP', 'Preposition: Location, comparison, instrument, exemplification', 'แม้, ว่า, เมื่อ, ของ, สำหรับ'],
    ['PU', 'PUNCT', 'Punctuation: Punctuation mark', '''(, ), ", ', :'''],
    ['VV', 'VERB', 'Verb: Action, state, occurrence, and word that forms the predicate part', 'เปิด, ให้, ใช้, เผชิญ, อ่าน'],
    ['XX', 'X', 'Others: Unknown category', 'xfgh, pdl, jklw']
]
