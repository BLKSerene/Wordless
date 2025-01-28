# ----------------------------------------------------------------------
# Wordless: Tagsets - ORCHID
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
#     https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/tag/orchid.py
tagset_mapping = [
    ['NPRP', 'PROPN', 'Proper noun', 'วินโดวส์ 95, โคโรน่า, โค้ก'],

    ['NCNM', 'NOUN/NUM', 'Cardinal number', 'หนึ่ง, สอง, สาม, 1, 2, 10'],
    ['NONM', 'ADJ', 'Ordinal number', 'ที่หนึ่ง, ที่สอง, ที่สาม, ที่1, ที่2'],

    ['NLBL', 'NUM', 'Label noun', '1, 2, 3, 4, ก, ข, a, b'],
    ['NCMN', 'NOUN', 'Common noun', 'หนังสือ, อาหาร, อาคาร, คน'],
    ['NTTL', 'NOUN', 'Title noun', 'ครู, พลเอก'],

    ['PPRS', 'PRON', 'Personal pronoun', 'คุณ, เขา, ฉัน'],
    ['PDMN', 'PRON', 'Demonstrative pronoun', 'นี่, นั้น, ที่นั่น, ที่นี่'],
    ['PNTR', 'PRON', 'Interrogative pronoun', 'ใคร, อะไร, อย่างไร'],
    ['PREL', 'SCONJ', 'Relative pronoun', 'ที่, ซึ่ง, อัน, ผู้'],

    ['VACT', 'VERB', 'Active verb', 'ทำงาน, ร้องเพลง, กิน'],
    ['VSTA', 'VERB', 'Static verb', 'เห็น, รู้, คือ'],
    ['VATT', 'ADJ', 'Attributive verb', 'อ้วน, ดี, สวย'],

    ['XVBM', 'AUX', 'Pre-verb auxiliary, before negator “ไม่”', 'เกิด, เกือบ, กำลัง'],
    ['XVAM', 'AUX', 'Pre-verb auxiliary, after negator "ไม่"', 'ค่อย, น่า, ได้'],
    ['XVMM', 'AUX', 'Pre-verb auxiliary, before or after negator "ไม่"', 'ควร, เคย, ต้อง'],
    ['XVBB', 'AUX', 'Pre-verb auxiliary, in imperative mood', 'กรุณา, จง, เชิญ, อย่า, ห้าม'],
    ['XVAE', 'AUX', 'Post-verb auxiliary', 'ไป, มา, ขึ้น'],

    ['DDAN', 'DET', 'Definite determiner,\nafter noun without classifier in between', 'ยี่, นั่น, โน่น, ทั้งหมด'],
    ['DDAC', 'DET', 'Definite determiner,\nallowing classifier in between', 'นี้, นั้น, โน้น, นู้น'],
    ['DDBQ', 'DET', 'Definite determiner,\nbetween noun and classifier or preceding quantitative expression', 'ทั้ง, อีก, เพียง'],
    ['DDAQ', 'DET', 'Definite determiner,\nfollowing quantitative expression', 'พอดี, ถ้วน'],
    ['DIAC', 'DET', 'Indefinite determiner,\nfollowing noun; allowing classfifier in between', 'ไหน, อื่น, ต่างๆ'],
    ['DIBQ', 'DET', 'Indefinite determiner,\nbetween noun and classifier or preceding quantitative expression', 'บาง, ประมาณ, เกือบ'],
    ['DIAQ', 'DET', 'Indefinite determiner,\nfollowing quantitative expression', 'กว่า, เศษ'],
    ['DCNM', 'NUM', 'Determiner,\ncardinal number expression', 'หนึ่งคน, เสือ, 2 ตัว'],
    ['DONM', 'ADJ', 'Determiner,\nordinal number expression', 'ที่หนึ่ง, ที่สอง, ที่สุดท้สย'],

    ['ADVN', 'ADV', 'Adverb with normal form', 'เก่ง, เร็ว, ช้า, สม่ำเสมอ'],
    ['ADVI', 'ADV', 'Adverb with iterative form', 'เร็วๆ, เสทอๆ, ช้าๆ'],
    ['ADVP', 'ADV', 'Adverb with prefixed form', 'โดยเร็ว'],
    ['ADVS', 'ADV', 'Sentential adverb', 'โดยปกติ, ธรรมดา'],

    ['CNIT', 'NOUN', 'Unit classifier', 'ตัว, คน, เล่ม'],
    ['CLTV', 'NOUN', 'Collective classifier', 'คู่, กลุ่ม, ฝูง, เชิง, ทาง, ด้าน, แบบ, รุ่น'],
    ['CMTR', 'NOUN', 'Measurement classifier', 'กิโลกรัม, แก้ว, ชั่วโมง'],
    ['CFQC', 'NOUN', 'Frequency classifier', 'ครั้ง, เที่ยว'],
    ['CVBL', 'NOUN', 'Verbal classifier', 'ม้วน, มัด'],

    ['JCRG', 'CCONJ', 'Coordinating conjunction', 'และ, หรือ, แต่'],
    ['JCMP', 'SCONJ', 'Comparative conjunction', 'กว่า, เหมือนกับ, เท่ากับ'],
    ['JSBR', 'SCONJ', 'Subordinating conjunctino', 'เพราะว่า, เนื่องจาก ที่, แม้ว่า, ถ้า'],

    ['RPRE', 'ADP', 'Preposition', 'จาก, ละ, ของ, ใต้, บน'],

    ['INT', 'INTJ', 'Interjection', 'โอ้บ, โอ้, เออ, เอ๋, อ๋อ'],

    ['FIXN', 'PART', 'Nominal prefix', 'การทำงาน, ความสนุนสนาน'],
    ['FIXV', 'PART', 'Adverbial prefix', 'อย่างเร็ว'],

    ['EAFF', 'PART', 'Ending for affirmative sentence', 'จ๊ะ, จ้ะ, ค่ะ, ครับ, นะ, น่า, เถอะ'],
    ['EITT', 'PART', 'Ending for interrogative sentence', 'หรือ, เหรอ, ไหม, มั้ย'],
    ['AITT', 'PART', '', ''],

    ['NEG', 'PART', 'Negator', 'ไม่, มิได้, ไม่ได้, มิ'],

    ['PUNC', 'PUNCT', 'Punctuation', '  (, ), “, ,, ;']
]
